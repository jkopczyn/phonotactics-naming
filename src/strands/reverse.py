"""Reverse the forward pipeline: from a target respelling back to Irish shapes.

The forward engine is spelling → g2p → Irish IPA → `[substitute]` + fallback → syllabify /
`[repair]` / stress / `[post-stress]` → `[respell]` (reverse spec §3). Reverse walks that
backwards in four steps — un-respell (§3.1), un-substitute (§3.2), widening over `[repair]` and
`[post-stress]` (§3.3), and the reverse g2p (§3.4) — under one discipline: **at every step the
candidate set only grows, and the forward engine is the oracle that prunes.** Nothing here
evaluates a rule environment or claims a derivation is real; `strands reverse` verifies every
concrete word it prints by running it forward.

This module holds the data model and the first step. `invert_respell` builds the chunk map
*output chunk → the target-IPA sequences that print it* (V-1); `parse_pattern` parses a
respelling glob greedily, longest chunk first, into slots of alternatives (V-2); and
`parse_ipa_pattern` is the `--ipa` mode's own parser, which tokenizes literal spans with the real
segment tokenizer rather than scanning code points (V-33). Contexts are carried as **text** and
never evaluated (V-12); `[!…]` glob classes are a usage error, because `fnmatch` in the
verification step would honour them and the parser would not (V-16); every alternative carries a
`Step` so the report can say which rule produced it (V-31); and insertions widen slot *spans*
as atomic optional groups, not individual slots (V-30).

Later tasks add `source_map` / `un_substitute` (§3.2), `widen` (§3.3), `expand`, `verify` and the
report; the dataclasses they need (`Source`, `Deletion`, `OptionalGroup`) live here.
"""
from __future__ import annotations

import itertools
import re
import unicodedata
from dataclasses import dataclass

from .dsl import Bundle, CtxItem, ItemSpec, QuotedText, Rule, RuleFile
from .features import FeatureTable
from .rewrite import match_item
from .tokenize import MARKS, SegmentError, tokenize

__all__ = [
    "ANY", "ONE", "SEG", "Step", "Alternative", "RespellSource", "Source", "Deletion",
    "OptionalGroup", "Slot", "Pattern", "ReverseError", "env_text", "invert_respell",
    "parse_pattern", "parse_ipa_pattern",
]

ANY, ONE, SEG = "any", "one", "seg"

_EXPAND_CAP = 64                      # V-4: combinations per rule
# Marks are never part of a pattern's segment content (spec §2: "stress and syllable marks
# ignored"; I-8, I-40).
_MARK_CHARS = "".join(MARKS)


# ---- data model -------------------------------------------------------------------------------

@dataclass(frozen=True)
class Step:
    """One stage of the walk back from a printed letter to an Irish segment (V-31)."""
    stage: str                        # "respell" | "post-stress" | "repair" | "substitute"
    rule_id: str
    tag: str                          # "" | "attested" | "design" | "fallback"
    context: str
    kind: str                         # "rule" | "fallback" | "identity" | "epenthesis"


@dataclass(frozen=True)
class Alternative:
    """One reading of a slot: the segments at this stage, plus how they were reached.

    `steps` is stored NEWEST FIRST — the respell step, then any `[repair]`/`[post-stress]`
    step, then the `[substitute]` step (V-31)."""
    segments: tuple[str, ...]
    steps: tuple[Step, ...] = ()

    @property
    def kind(self) -> str:
        """The OLDEST step's kind — the Irish-side one; "identity" when there are none."""
        return self.steps[-1].kind if self.steps else "identity"


@dataclass(frozen=True)
class RespellSource:
    segments: tuple[str, ...]
    rule_id: str
    tag: str
    context: str
    line: int


@dataclass(frozen=True)
class Source:
    segments: tuple[str, ...]
    rule_id: str
    tag: str
    context: str
    kind: str
    line: int = 0                     # V-28: the rule's own line, for the chain order guard
    note: str = ""


@dataclass(frozen=True)
class Deletion:
    segments: tuple[str, ...]
    rule_id: str
    tag: str
    context: str


@dataclass(frozen=True)
class OptionalGroup:
    """A span of slots an insertion could have produced — present or absent as a unit (V-30)."""
    start: int                        # inclusive slot index
    stop: int                         # exclusive
    steps: tuple[Step, ...]
    note: str


@dataclass(frozen=True)
class Slot:
    kind: str                         # ANY | ONE | SEG
    text: str                         # the pattern text: "a", "?", "*", "[aeiou]"
    alts: tuple[Alternative, ...] = ()
    notes: tuple[str, ...] = ()


@dataclass(frozen=True)
class Pattern:
    text: str                         # the (casefolded, NFC) word pattern
    slots: tuple[Slot, ...]
    groups: tuple[OptionalGroup, ...] = ()
    deletions: tuple[Deletion, ...] = ()
    notes: tuple[str, ...] = ()


class ReverseError(Exception):
    """A pattern that cannot be parsed: an unclosed `[`, `[!…]` (V-16), or — in --ipa mode —
    a substring that is not a segment of features.tsv (V-33)."""


# ---- contexts as text (V-12) ------------------------------------------------------------------

def _bundle_text(bundle: Bundle) -> str:
    parts: list[str] = []
    if bundle.class_name is not None:
        parts.append(bundle.class_name)
    if bundle.orth is not None:
        parts.append(f'orth="{bundle.orth}"')
    parts.extend(f"{sign}{feature}" for feature, sign in bundle.constraints.items())
    return "[" + " ".join(parts) + "]"


def _item_text(spec: ItemSpec) -> str:
    if spec.kind == "segment" or spec.kind == "class":
        return str(spec.value)
    if spec.kind == "set":
        return "{" + " ".join(spec.value) + "}"           # type: ignore[arg-type]
    if spec.kind == "orth":
        return f'@orth("{spec.value}")'
    if spec.kind == "bundle":
        assert isinstance(spec.value, Bundle)
        return _bundle_text(spec.value)
    return str(spec.value)                                 # pragma: no cover - no other kinds


def _ctx_text(item: CtxItem) -> str:
    text = item.atom if isinstance(item.atom, str) else _item_text(item.atom)
    if item.optional:
        text = f"({text})"
    if item.star:
        text = f"{text}*"
    return text


def env_text(rule: Rule) -> str:
    """The rule's environment as TEXT (V-12). Captures are not rendered — the reader of a
    constraint line wants the shape, and nothing downstream evaluates this string."""
    if not rule.left and not rule.right:
        return ""
    parts = [_ctx_text(item) for item in rule.left]
    parts.append("_")
    parts.extend(_ctx_text(item) for item in rule.right)
    return " ".join(parts)


# ---- un-respell (spec §3.1, V-1) --------------------------------------------------------------

def _fold(text: str) -> str:
    return unicodedata.normalize("NFC", text).casefold()


def _expand_item(spec: ItemSpec, rf: RuleFile, table: FeatureTable) -> tuple[str, ...]:
    """Every segment of `rf.inventory` the item matches, in declaration order (V-4/V-29)."""
    if spec.kind == "segment":
        return (str(spec.value),)
    return tuple(seg for seg in rf.inventory if match_item(spec, seg, rf, table))


def invert_respell(rf: RuleFile, table: FeatureTable
                   ) -> tuple[dict[str, tuple[RespellSource, ...]], tuple[str, ...]]:
    """The chunk map of V-1: casefolded output chunk → the segment sequences that print it.

    Built from `rf.sections["respell"]` in file order. A quoted replacement whose target items
    are all segments contributes one entry; a class / set / bundle target is expanded over the
    file's OWN inventory (V-29: `[respell]` runs on the strand's phonology), one entry per
    combination of the cartesian product. Every other rule shape — epenthesis, a backref, an
    IPA-segment or feature-change replacement — is skipped with a note. Finally every segment
    no entry claims as its whole target maps to itself.
    """
    chunks: dict[str, list[RespellSource]] = {}
    notes: list[str] = []
    claimed: set[tuple[str, ...]] = set()

    for rule in rf.sections.get("respell", ()):
        rid = rule.rule_id
        replacement = rule.replacement
        if (isinstance(replacement, Bundle) or len(replacement) != 1
                or not isinstance(replacement[0], QuotedText)):
            notes.append(f"{rid} skipped: replacement is not a single quoted chunk")
            continue
        if not rule.target:
            notes.append(f"{rid} skipped: epenthesis has no source segments")
            continue

        expanded = [_expand_item(spec, rf, table) for spec in rule.target]
        if any(not values for values in expanded):
            notes.append(f"{rid} skipped: a target item matches no segment of the inventory")
            continue
        combinations = list(itertools.islice(itertools.product(*expanded), _EXPAND_CAP + 1))
        if len(combinations) > _EXPAND_CAP:
            combinations = combinations[:_EXPAND_CAP]
            notes.append(f"{rid} expanded to more than {_EXPAND_CAP} targets; kept the first "
                         f"{_EXPAND_CAP} in inventory order")

        text = _fold(replacement[0].text)
        for segments in combinations:
            # A respell rule that prints NOTHING cannot be inverted: a slot exists only where
            # the respelling prints something, so a group starting at a deleted segment is
            # unreachable (V-30, accepted miss). The target still counts as claimed, so no
            # identity chunk is invented for a segment the strand never prints.
            claimed.add(segments)
            if text == "":
                notes.append(f"{rid} deletes {' '.join(segments)}; a group starting there "
                             f"is unreachable")
                continue
            chunks.setdefault(text, []).append(
                RespellSource(segments=segments, rule_id=rid, tag=rule.tag,
                              context=env_text(rule), line=rule.line))

    for seg in rf.inventory:
        if (seg,) in claimed:
            continue
        chunks.setdefault(_fold(seg), []).append(
            RespellSource(segments=(seg,), rule_id="identity", tag="", context="", line=0))

    return {chunk: tuple(sources) for chunk, sources in chunks.items()}, tuple(notes)


# ---- the glob parser (spec §3.1, V-2) ---------------------------------------------------------

def _chunk_order(chunks: dict[str, tuple[RespellSource, ...]]) -> tuple[str, ...]:
    """Longest chunk first, then ascending by `str` — so Georgian `ts'` beats `ts` beats `t`."""
    return tuple(sorted(chunks, key=lambda chunk: (-len(chunk), chunk)))


def _respell_alt(source: RespellSource) -> Alternative:
    kind = "identity" if source.rule_id == "identity" else "rule"
    return Alternative(segments=source.segments,
                       steps=(Step(stage="respell", rule_id=source.rule_id, tag=source.tag,
                                   context=source.context, kind=kind),))


def _class_body(text: str, start: int) -> tuple[str, int]:
    """The body of the `[...]` opening at `start`, and the index just past its `]` (V-2/V-16)."""
    end = text.find("]", start + 1)
    if end == -1:
        raise ReverseError(f"unclosed '[' in pattern {text!r}")
    body = text[start + 1:end]
    if body[:1] in ("!", "^"):
        raise ReverseError("[!…] classes are not supported")
    return body, end + 1


def parse_pattern(pattern: str, chunks: dict[str, tuple[RespellSource, ...]],
                  *, notes: tuple[str, ...] = ()) -> Pattern:
    """Parse one respelling glob into slots, greedily longest chunk first (V-2).

    `notes` is the second value of `invert_respell` and is copied in BEFORE the parser's own
    notes (V-35), so a respell-deletion note reaches the report.
    """
    text = _fold(pattern)
    order = _chunk_order(chunks)
    slots: list[Slot] = []
    pattern_notes: list[str] = list(notes)

    pos = 0
    while pos < len(text):
        ch = text[pos]
        if ch == "*":
            slots.append(Slot(kind=ANY, text="*"))
            pos += 1
            continue
        if ch == "?":
            slots.append(Slot(kind=ONE, text="?"))
            pos += 1
            continue
        if ch == "[":
            body, pos = _class_body(text, pos)
            alts: list[Alternative] = []
            seen: set[tuple[tuple[str, ...], tuple[Step, ...]]] = set()
            slot_notes: list[str] = []
            for letter in body:
                for source in chunks.get(letter, ()):
                    alt = _respell_alt(source)
                    if (alt.segments, alt.steps) not in seen:
                        seen.add((alt.segments, alt.steps))
                        alts.append(alt)
                if letter not in chunks:
                    note = f"no Irish source for {letter!r}"
                    slot_notes.append(note)
                    if note not in pattern_notes:
                        pattern_notes.append(note)
            slots.append(Slot(kind=ONE, text=f"[{body}]", alts=tuple(alts),
                              notes=tuple(slot_notes)))
            continue
        chunk = next((c for c in order if c and text.startswith(c, pos)), None)
        if chunk is None:
            note = f"no Irish source for {ch!r}"
            slots.append(Slot(kind=ONE, text=ch, notes=(note,)))
            if note not in pattern_notes:
                pattern_notes.append(note)
            pos += 1
            continue
        slots.append(Slot(kind=SEG, text=chunk,
                          alts=tuple(_respell_alt(s) for s in chunks[chunk])))
        pos += len(chunk)

    return Pattern(text=text, slots=tuple(slots), notes=tuple(pattern_notes))


# ---- --ipa mode (spec §2, V-33) ---------------------------------------------------------------

_UNKNOWN_SEGMENT_RE = re.compile(r"unknown segment (['\"])(.*?)\1")


def _tokenize_span(span: str, table: FeatureTable) -> tuple[str, ...]:
    try:
        return tokenize(span, table).segments
    except SegmentError as exc:
        match = _UNKNOWN_SEGMENT_RE.search(str(exc))
        bad = match.group(2) if match else span
        raise ReverseError(f"{bad!r} is not a segment in features.tsv") from None


def parse_ipa_pattern(pattern: str, target: RuleFile, table: FeatureTable) -> Pattern:
    """Parse a target-IPA glob (V-33). No un-respell step happens in `--ipa` mode (spec §2).

    Literal spans between the glob atoms are handed to the real tokenizer, so `t̪ˠ`, `tʃʰ` and
    `aː` stay whole; the members of a `[...]` class are whole segments too. A segment that
    tokenizes but is outside the strand is a NOTE, not an error — it simply never verifies.
    The pattern is NOT casefolded: IPA is not a spelling, and folding it could merge segments.
    """
    text = unicodedata.normalize("NFC", pattern)
    text = "".join(ch for ch in text if ch not in _MARK_CHARS)
    strand = (target.meta.get("name") or target.path).casefold()
    inventory = set(target.inventory) | set(target.marginal)
    slots: list[Slot] = []
    notes: list[str] = []

    def note_unknown(seg: str) -> tuple[str, ...]:
        if seg in inventory:
            return ()
        note = f"no {strand} segment {seg!r}"
        if note not in notes:
            notes.append(note)
        return (note,)

    pos = 0
    span_start = 0

    def flush(end: int) -> None:
        span = text[span_start:end]
        if not span:
            return
        for seg in _tokenize_span(span, table):
            slots.append(Slot(kind=SEG, text=seg, alts=(Alternative(segments=(seg,)),),
                              notes=note_unknown(seg)))

    while pos < len(text):
        ch = text[pos]
        if ch not in "*?[":
            pos += 1
            continue
        flush(pos)
        if ch == "*":
            slots.append(Slot(kind=ANY, text="*"))
            pos += 1
        elif ch == "?":
            slots.append(Slot(kind=ONE, text="?"))
            pos += 1
        else:
            body, pos = _class_body(text, pos)
            members = _tokenize_span(body, table) if body else ()
            slot_notes: list[str] = []
            for seg in members:
                slot_notes.extend(note_unknown(seg))
            slots.append(Slot(kind=ONE, text=f"[{body}]",
                              alts=tuple(Alternative(segments=(seg,)) for seg in members),
                              notes=tuple(slot_notes)))
        span_start = pos
    flush(len(text))

    return Pattern(text=text, slots=tuple(slots), notes=tuple(notes))
