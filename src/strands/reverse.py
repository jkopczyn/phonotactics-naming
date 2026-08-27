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

`source_map` inverts one section into *target-side sequence → the sources that can produce it*
(§3.2): every rule shape by V-5, context backrefs by V-6, deletions kept apart and never expanded
(V-7), the inventory fallback and identity sources for `[substitute]` alone (V-8/V-9), and a chain
closure that composes two rules only when the producing rule runs FIRST (V-11/V-28). Each section
expands over its own inventory (V-29). `un_substitute` walks a parsed pattern back across it.

`widen` (§3.3) adds the `[repair]`/`[post-stress]` readings and the optional groups; the
constraint set, `render_pattern` and `report` print §4; and `expand`/`verify` (§3.5) turn a
pattern into concrete Irish candidates, cheapest first under a hard cap of 2000, spell each one
with `g2p_inverse.spell` and run EVERY spelling forward through the real engine, keeping only
what `fnmatchcase` says really matches (V-22 … V-26, V-34). Nothing is printed as a concrete
word that has not been through `run_entry`. `old_irish_matches` is the one strand that
skips all of this: Old Irish is a lexicon fnmatch and nothing else (R6).
"""
from __future__ import annotations

import fnmatch
import heapq
import itertools
import re
import unicodedata
from dataclasses import dataclass
from typing import Sequence

from . import g2p_inverse
from .dsl import Backref, Bundle, CtxItem, ItemSpec, QuotedText, Rule, RuleFile
from .features import FeatureError, FeatureTable
from .rewrite import match_item
from .tokenize import MARKS, SegmentError, tokenize

__all__ = [
    "ANY", "ONE", "SEG", "Step", "Alternative", "RespellSource", "Source", "Deletion",
    "OptionalGroup", "Slot", "Pattern", "ReverseError", "env_text", "invert_respell",
    "parse_pattern", "parse_ipa_pattern", "SourceMap", "section_inventory", "expand_target",
    "source_map", "un_substitute", "WIDEN_SECTIONS", "widen", "RULE_COL", "FORWARD_STAGES",
    "ConstraintLine", "Constraint", "Example", "format_rule_line", "constraints",
    "dropped_lines", "render_pattern", "report", "CAP", "PALETTE", "STAR_LENGTHS",
    "Candidate", "rank", "expand", "verify", "old_irish_matches", "old_irish_report",
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
    targets: tuple[tuple[str, ...], ...] = ()
                                      # the distinct TARGET-side segment sequences this slot
                                      # prints, for the report's `target segments:` line. Set at
                                      # parse time — the walk back overwrites `alts` with Irish
                                      # segments, so the target side is not recoverable later.
                                      # An ambiguous chunk keeps EVERY alternative in respell
                                      # file order (spec §3.1, V-1); the report joins the
                                      # segments of one alternative with " " and the
                                      # alternatives with "|". Empty falls back to `text`.


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


def _dedupe_segments(sequences) -> tuple[tuple[str, ...], ...]:
    """The distinct segment sequences, first occurrence (respell file order) winning."""
    return tuple(dict.fromkeys(tuple(seq) for seq in sequences))


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
        sources = chunks[chunk]
        slots.append(Slot(kind=SEG, text=chunk,
                          alts=tuple(_respell_alt(s) for s in sources),
                          targets=_dedupe_segments(s.segments for s in sources)))
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


# ---- un-substitute (spec §3.2, V-3 … V-12, V-28, V-29) -----------------------------------------

SourceMap = dict[tuple[str, ...], tuple[Source, ...]]

_STAGE_OF_SECTION = {"substitute": "substitute", "repair": "repair",
                     "post-stress": "post-stress", "respell": "respell"}


def section_inventory(section: str, target: RuleFile, irish: RuleFile) -> tuple[str, ...]:
    """The inventory a section's rules are expanded over (V-29).

    `[substitute]` reads Irish segments and writes target ones, so it expands over
    `irish.inventory`; `[repair]`, `[post-stress]` and `[respell]` run *after* substitution, so
    their targets are already in the strand's phonology and they expand over `target.inventory`.
    `target.marginal` is NEVER appended: it is a frozenset (non-deterministic order) and every
    marginal segment is already a member of `inventory`.
    """
    source = irish.inventory if section == "substitute" else target.inventory
    return tuple(source)


def _item_options(spec: ItemSpec, match_rf: RuleFile, inventory: Sequence[str],
                  table: FeatureTable) -> tuple[str, ...]:
    """Every segment of `inventory` the item matches, in inventory order (V-4).

    A literal segment item yields itself whether or not it is in the inventory: georgian's
    `p -> pʼ / C _` has an Irish-side `p` that no Irish inventory row contains, and dropping it
    would break the `pˠ -> p -> pʼ` chain (V-28). This is the over-generating reading of §3.
    """
    if spec.kind == "segment":
        return (str(spec.value),)
    return tuple(seg for seg in inventory if match_item(spec, seg, match_rf, table))


def _target_combinations(rule: Rule, match_rf: RuleFile, inventory: Sequence[str],
                         table: FeatureTable):
    """Lazily, every (segment sequence, captures) the rule's target can match."""
    options = [_item_options(spec, match_rf, inventory, table) for spec in rule.target]
    for combination in itertools.product(*options):
        captures = {spec.capture: seg
                    for spec, seg in zip(rule.target, combination)
                    if spec.capture is not None}
        yield combination, captures


def expand_target(rule: Rule, match_rf: RuleFile, inventory: Sequence[str],
                  table: FeatureTable) -> tuple[tuple[tuple[str, ...], dict[int, str]], ...]:
    """Each (segment sequence, captures) the rule's TARGET can match over `inventory`, in
    inventory order, capped at `_EXPAND_CAP` (V-4). `match_rf` supplies the class names (always
    the TARGET rule file — the rule's class names are its own file's); `inventory` is chosen by
    the caller per V-29."""
    return tuple(itertools.islice(_target_combinations(rule, match_rf, inventory, table),
                                  _EXPAND_CAP))


def _capture_options(rule: Rule, n: int, match_rf: RuleFile, inventory: Sequence[str],
                     table: FeatureTable) -> tuple[str, ...]:
    """The segments the CONTEXT item capturing `\\n` can match (V-6)."""
    for item in itertools.chain(rule.left, rule.right):
        if isinstance(item.atom, ItemSpec) and item.atom.capture == n:
            return _item_options(item.atom, match_rf, inventory, table)
    return ()


def _invert_rule(rule: Rule, target: RuleFile, inventory: tuple[str, ...],
                 table: FeatureTable, section: str,
                 add, deletions: list[Deletion], notes: list[str],
                 covered: set[tuple[str, ...]]) -> None:
    """One rule of one section, inverted by replacement shape (V-5, V-6, V-7)."""
    rid, tag, line = rule.rule_id, rule.tag, rule.line
    context = env_text(rule)
    context_free = not rule.left and not rule.right
    replacement = rule.replacement

    combinations = list(itertools.islice(
        _target_combinations(rule, target, inventory, table), _EXPAND_CAP + 1))
    if len(combinations) > _EXPAND_CAP:
        combinations = combinations[:_EXPAND_CAP]
        notes.append(f"{rid} expanded to more than {_EXPAND_CAP} targets; kept the first "
                     f"{_EXPAND_CAP} in inventory order")

    def source(segments, kind, *, rule_id=rid, note="") -> Source:
        return Source(segments=segments, rule_id=rule_id, tag=tag, context=context,
                      kind=kind, line=line, note=note)

    if isinstance(replacement, Bundle):                      # feature change
        if not rule.target:
            notes.append(f"{rid} skipped: a feature change needs a target")
            return
        for segments, _captures in combinations:
            for seg in segments:
                try:
                    changed = table.apply_changes(seg, replacement.constraints)
                except FeatureError as exc:
                    notes.append(f"{rid} skipped {seg}: {exc}")
                    continue
                add((changed,), source((seg,), "rule"))
            if context_free:
                # V-8/V-9: only the WHOLE target is covered. `a i -> [+long]` does not fire on a
                # lone `a`, so `a` still needs its identity/fallback source; the ordinary
                # replacement branch covers `segments` for the same reason.
                covered.add(segments)
        return

    # A DELETION does not "cover" its target for V-8/V-9: `X -> 0` leaves nothing behind, so
    # the fallback still has to offer X somewhere (the plan's synthetic /h/ is exactly this).
    if replacement == ():                                    # deletion (V-7)
        if not rule.target:
            notes.append(f"{rid} skipped: a deletion needs a target")
            return
        for segments, _captures in combinations:
            deletions.append(Deletion(segments=segments, rule_id=rid, tag=tag, context=context))
        return

    if any(isinstance(part, QuotedText) for part in replacement) and section != "respell":
        notes.append(f"{rid} skipped: quoted text outside [respell]")
        return

    epenthesis = not rule.target
    for segments, captures in combinations:
        unresolved = sorted({part.n for part in replacement
                             if isinstance(part, Backref) and part.n not in captures})
        if not unresolved:
            key = tuple(captures[part.n] if isinstance(part, Backref) else str(part)
                        for part in replacement)
            if epenthesis:
                # V-5/V-30: however many segments are inserted, they are ONE key.
                add(key, source((), "epenthesis"))
            else:
                add(key, source(segments, "rule"))
                if context_free:
                    covered.add(segments)
            continue

        # V-6: the replacement copies a segment captured in the CONTEXT, so its identity is
        # unknown at inversion time — one epenthesis source per segment that item can match.
        options = [_capture_options(rule, n, target, inventory, table) for n in unresolved]
        if any(not choices for choices in options):
            notes.append(f"{rid} skipped: no context item captures "
                         f"\\{unresolved[0]}")
            continue
        note = "copies " + ", ".join(f"\\{n}" for n in unresolved) + " from the context"
        for assignment in itertools.islice(itertools.product(*options), _EXPAND_CAP):
            copied = dict(zip(unresolved, assignment))
            key = tuple(copied[part.n] if isinstance(part, Backref) and part.n in copied
                        else captures[part.n] if isinstance(part, Backref) else str(part)
                        for part in replacement)
            add(key, source((), "epenthesis", note=note))


def _close_chains(smap: dict[tuple[str, ...], list[Source]], add, depth: int) -> None:
    """V-11/V-28: compose `A -> B` with `B -> C` to depth `depth`, but ONLY when the producing
    rule runs BEFORE the consuming one — arabic-egy's `ʒ -> ʃ` (61) precedes `dʒ -> ʒ` (62), so
    forward /dʒ/ stops at /ʒ/ and must never be offered as a source of /ʃ/."""
    for _pass in range(max(depth - 1, 0)):
        additions: list[tuple[tuple[str, ...], Source]] = []
        for key, sources in list(smap.items()):
            for step in list(sources):
                if step.kind != "rule":
                    continue
                for earlier in smap.get(step.segments, ()):
                    if earlier.kind != "rule":
                        continue
                    if earlier.segments == key or earlier.segments == step.segments:
                        continue                              # cycle guard (v v -> v, …)
                    if earlier.line >= step.line:
                        continue                              # V-28: the order guard
                    tag = "design" if "design" in (step.tag, earlier.tag) else step.tag
                    context = " ; ".join(x for x in (earlier.context, step.context) if x)
                    additions.append((key, Source(
                        segments=earlier.segments,
                        rule_id=f"{earlier.rule_id}>{step.rule_id}",
                        tag=tag, context=context, kind="rule", line=step.line)))
        for key, source in additions:
            add(key, source)


def source_map(section: str, target: RuleFile, irish: RuleFile, table: FeatureTable,
               *, depth: int = 3) -> tuple[SourceMap, tuple[Deletion, ...], tuple[str, ...]]:
    """Invert one section: target-side segment sequence → the sources that can produce it (V-3).

    Built rule by rule in file order; then the ordered chain closure (V-11/V-28); then, for
    `[substitute]` only, the inventory fallback (V-8) and the identity sources (V-9). Deletions
    are never expanded into candidates — they come back separately (V-7), as do the notes.
    """
    inventory = section_inventory(section, target, irish)
    smap: dict[tuple[str, ...], list[Source]] = {}
    seen: dict[tuple[str, ...], set[tuple[tuple[str, ...], str]]] = {}
    deletions: list[Deletion] = []
    notes: list[str] = []
    covered: set[tuple[str, ...]] = set()

    def add(key: tuple[str, ...], source: Source) -> None:
        marker = (source.segments, source.rule_id)
        if marker in seen.setdefault(key, set()):
            return                                            # dedupe by (segments, rule_id)
        seen[key].add(marker)
        smap.setdefault(key, []).append(source)

    for rule in target.sections.get(section, ()):
        _invert_rule(rule, target, inventory, table, section, add, deletions, notes, covered)

    _close_chains(smap, add, depth)

    if section == "substitute":
        # V-8: everything Irish that no context-free rule claims and the strand has no segment
        # for reaches its nearest NON-MARGINAL target segment — exactly `substitute.fallback`.
        candidates = tuple(s for s in target.inventory if s not in target.marginal)
        for seg in irish.inventory:
            if (seg,) in covered:
                continue
            if seg in target.inventory:
                # V-9: the strand has this segment, so it can simply survive.
                add((seg,), Source(segments=(seg,), rule_id="identity", tag="", context="",
                                   kind="identity"))
            else:
                add((table.nearest(seg, candidates, target.weights),),
                    Source(segments=(seg,), rule_id="fallback", tag="fallback", context="",
                           kind="fallback"))

    return ({key: tuple(sources) for key, sources in smap.items()},
            tuple(deletions), tuple(notes))


def un_substitute(pattern: Pattern, smap: SourceMap, *,
                  deletions: Sequence[Deletion] = (), notes: Sequence[str] = ()) -> Pattern:
    """Walk each slot's alternatives back across `[substitute]` (V-3, V-31).

    For every alternative whose segments are a key of `smap`, one new alternative per `Source`,
    with that source's `Step` APPENDED (steps are newest first, so the substitute step lands
    oldest). An alternative with NO entry keeps an empty source list and so emits nothing: it has
    no Irish source, and preserving the target-side alternative stepless would let the report
    claim an Irish source it does not have (V-31). `deletions` and `notes` are the other two
    members of the
    `source_map(...)` triple and are appended to the pattern's own (V-7), so the report's
    `possibly dropped` block can name a `[substitute]` deletion.
    """
    slots: list[Slot] = []
    for slot in pattern.slots:
        if slot.kind == ANY or not slot.alts:
            slots.append(slot)
            continue
        alts: list[Alternative] = []
        seen: set[tuple[tuple[str, ...], tuple[Step, ...]]] = set()

        def keep(alt: Alternative) -> None:
            marker = (alt.segments, alt.steps)
            if marker not in seen:
                seen.add(marker)
                alts.append(alt)

        for alt in slot.alts:
            # V-31: an alternative with no entry in the map has no [substitute] source and is
            # DROPPED — keeping it would leave a stepless alternative that later reporting would
            # read as an Irish identity source (welsh `th` -> /θ/, which no Irish segment reaches).
            for source in smap.get(alt.segments, ()):
                keep(Alternative(segments=source.segments,
                                 steps=alt.steps + (Step(stage="substitute",
                                                         rule_id=source.rule_id,
                                                         tag=source.tag, context=source.context,
                                                         kind=source.kind),)))
        slots.append(Slot(kind=slot.kind, text=slot.text, alts=tuple(alts),
                          notes=slot.notes, targets=slot.targets))

    extra = tuple(note for note in notes if note not in pattern.notes)
    return Pattern(text=pattern.text, slots=tuple(slots), groups=pattern.groups,
                   deletions=pattern.deletions + tuple(deletions),
                   notes=pattern.notes + extra)


# ---- widening over [repair] / [post-stress] (spec §3.3, V-18, V-29, V-30, V-31) ----------------

WIDEN_SECTIONS = ("repair", "post-stress")


def _group_note(steps: Sequence[Step], extra: Sequence[str] = ()) -> str:
    """`could be an insertion (id, id, …)`, followed by any source notes (backref copies)."""
    ids = list(dict.fromkeys(step.rule_id for step in steps))
    parts = [f"could be an insertion ({', '.join(ids)})"]
    parts.extend(note for note in dict.fromkeys(extra) if note)
    return "; ".join(parts)


def _epenthesis_groups(slots: Sequence[Slot], smap: SourceMap, section: str
                       ) -> list[OptionalGroup]:
    """Every consecutive slot SPAN an insertion of this section could have produced (V-30).

    A group is found only where EVERY inserted segment has a slot that can read as it, so a
    two-segment insertion is one width-two group and never two independent optional slots. A
    group whose first segment the `[respell]` section deletes is unreachable — that is V-30's
    accepted miss, recorded as an `invert_respell` note.

    EVERY epenthesis source of the span is kept, not just the first: Welsh `repair:272`
    (`# _ s {p t k}`) and `repair:276` (`# _ s {m n}`) both insert `/ə/`, and a span they can
    both explain is ONE optional group carrying BOTH steps, so reporting can name each
    insertion context. Which source's environment the surrounding slots actually satisfy is not
    decided here — the over-generating reading (spec §3); `verify` re-runs the forward engine.
    """
    spans: dict[tuple[int, int], list[Source]] = {}
    for inserted, sources in smap.items():
        epenthetic = [s for s in sources if s.kind == "epenthesis"]
        if not epenthetic or not inserted:
            continue
        width = len(inserted)
        for start in range(0, len(slots) - width + 1):
            span = slots[start:start + width]
            if any(slot.kind != SEG for slot in span):
                continue
            if not all(any(alt.segments == (seg,) for alt in slot.alts)
                       for slot, seg in zip(span, inserted)):
                continue
            bucket = spans.setdefault((start, start + width), [])
            for source in epenthetic:
                if source not in bucket:
                    bucket.append(source)
    found: list[OptionalGroup] = []
    for (start, stop), sources in sorted(spans.items()):
        steps = tuple(dict.fromkeys(
            Step(stage=section, rule_id=s.rule_id, tag=s.tag, context=s.context,
                 kind="epenthesis") for s in sources))
        found.append(OptionalGroup(start=start, stop=stop, steps=steps,
                                   note=_group_note(steps, [s.note for s in sources])))
    return found


def _merge_spans(candidates: Sequence[OptionalGroup]) -> list[OptionalGroup]:
    """One group per span: two sections (or a pattern's own group and a new one) that mark the
    SAME slots optional are one optional group, and their steps merge rather than one being
    dropped — V-30's provenance must survive."""
    merged: dict[tuple[int, int], tuple[list[Step], list[str]]] = {}
    for group in candidates:
        steps, notes = merged.setdefault((group.start, group.stop), ([], []))
        for step in group.steps:
            if step not in steps:
                steps.append(step)
        if group.note and group.note not in notes:
            notes.append(group.note)
    out: list[OptionalGroup] = []
    for (start, stop), (steps, notes) in merged.items():
        note = notes[0] if len(notes) == 1 else _group_note(steps)
        out.append(OptionalGroup(start=start, stop=stop, steps=tuple(steps), note=note))
    return out


def _resolve_groups(candidates: Sequence[OptionalGroup], notes: list[str]
                    ) -> tuple[OptionalGroup, ...]:
    """Sorted by `(start, stop)` and non-overlapping; equal spans MERGE (`_merge_spans`), and on
    a partial overlap the earlier, then longer group wins and the other is dropped with a note
    (V-30)."""
    ordered = sorted(_merge_spans(candidates),
                     key=lambda g: (g.start, -(g.stop - g.start), g.steps[0].rule_id))
    kept: list[OptionalGroup] = []
    for group in ordered:
        clash = next((k for k in kept if k.start < group.stop and group.start < k.stop), None)
        if clash is None:
            kept.append(group)
            continue
        note = (f"{group.steps[0].rule_id} could insert slots "
                f"{group.start}-{group.stop - 1}, which overlaps "
                f"{clash.steps[0].rule_id}; dropped")
        if note not in notes:
            notes.append(note)
    return tuple(sorted(kept, key=lambda g: (g.start, g.stop)))


def widen(pattern: Pattern, target: RuleFile, irish: RuleFile,
          table: FeatureTable) -> Pattern:
    """Widen a parsed pattern over `[repair]` and `[post-stress]` (spec §3.3, V-18).

    (a) Every slot alternative one of those rules could have PRODUCED gains that rule's target
    as a further alternative, with the rule's `Step` appended (V-31), so a Welsh `â` also reads
    as the short `/a/` the §4.3 lengthening acted on. (b) Every insertion of those sections
    becomes an `OptionalGroup` over the slot span that spells it — atomically, so a two-segment
    insertion can never be half-present (V-30). (c) Their deletions and notes join the
    word-level lists (V-7).

    The two maps carry NO fallback and NO identity sources — V-8/V-9 are `[substitute]`-only —
    and each expands over `target.inventory` (V-29). The sections are walked in REVERSE forward
    order (post-stress, then repair) so a post-stress-widened alternative can be widened again
    by a repair rule. Stress is ignored entirely: the forward engine re-derives it, and no
    `[stress]` section is read.
    """
    slots = list(pattern.slots)
    deletions = list(pattern.deletions)
    notes = list(pattern.notes)
    candidates: list[OptionalGroup] = []

    for section in reversed(WIDEN_SECTIONS):
        smap, section_deletions, section_notes = source_map(section, target, irish, table)
        deletions.extend(section_deletions)
        notes.extend(note for note in section_notes if note not in notes)

        widened: list[Slot] = []
        for slot in slots:
            if slot.kind == ANY or not slot.alts:
                widened.append(slot)
                continue
            alts = list(slot.alts)
            seen = {(alt.segments, alt.steps) for alt in alts}
            for alt in slot.alts:
                for source in smap.get(alt.segments, ()):
                    if source.kind != "rule":
                        continue                     # epenthesis becomes a group, not an alt
                    new = Alternative(
                        segments=source.segments,
                        steps=alt.steps + (Step(stage=section, rule_id=source.rule_id,
                                                tag=source.tag, context=source.context,
                                                kind=source.kind),))
                    if (new.segments, new.steps) not in seen:
                        seen.add((new.segments, new.steps))
                        alts.append(new)
            widened.append(Slot(kind=slot.kind, text=slot.text, alts=tuple(alts),
                                notes=slot.notes, targets=slot.targets))
        slots = widened
        candidates.extend(_epenthesis_groups(slots, smap, section))

    return Pattern(text=pattern.text, slots=tuple(slots),
                   groups=_resolve_groups(pattern.groups + tuple(candidates), notes),
                   deletions=tuple(deletions), notes=tuple(notes))


# ---- the constraint set and the report (spec §4; V-7, V-13 … V-15, V-21, V-31, V-32) -----------

RULE_COL = 62                         # V-32: a CODE-POINT index, not a display column
_ALT_CAP = 6                          # V-14: alternatives printed per slot in the rendering

#: The order everything is REPORTED in — the forward engine's order, not the walk's (V-31).
FORWARD_STAGES = ("substitute", "repair", "post-stress", "respell")

_KIND_RANK = {"identity": 0, "rule": 1, "fallback": 2, "epenthesis": 3}
_TAG_RANK = {"": 0, "attested": 0, "design": 1, "fallback": 2}
_TAG_NAME = ("", "design", "fallback")
# V-15: a fixed phrase per source kind, never hand prose. `describe(())` is already
# "inserted, no Irish letter", so epenthesis needs no suffix of its own.
_KIND_PHRASE = {"identity": "", "rule": "", "fallback": " (nearest inventory match)",
                "epenthesis": ""}
_DROPPED_PHRASE = "may have been dropped anywhere in this word"


@dataclass(frozen=True)
class ConstraintLine:
    """One printed line of the constraint set: a group of alternatives that agree on
    `(kind, tag, description, context)` (V-31)."""
    description: str
    rule_ids: tuple[str, ...]
    tag: str                          # "" | "design" | "fallback"
    kind: str
    context: str                      # every context-bearing step's context, joined " ; "
    label: str = ""                   # only the `possibly dropped` block uses this: its lines
                                      # are not attached to a slot, so they carry their own
                                      # label (the deleted segments)
    contexts: tuple[tuple[str, str], ...] = ()
    # ^ (rule_id, context) per context-bearing STEP, in forward stage order. `context` above is
    # these joined; the exclusions block needs them apart, because it prints one line per step
    # with that step's own rule id (V-13, V-31).


@dataclass(frozen=True)
class Constraint:
    label: str                        # the pattern text of the slot: "a", "*", "[aeiou]"
    target: str                       # the target-side segments the slot prints
    lines: tuple[ConstraintLine, ...]
    notes: tuple[str, ...]
    unconstrained: bool


@dataclass(frozen=True)
class Example:
    """One forward-verified concrete word (spec §3.5). Filled in by `verify` (Task 7); defined
    here because `report` prints it."""
    orthography: str
    respelling: str
    ipa: str
    flags: tuple[str, ...]
    fallbacks: int
    rank: int
    spelling_index: int


def format_rule_line(prefix: str, description: str, suffix: str) -> list[str]:
    """`prefix + description`, then `suffix` starting at code-point index RULE_COL.

    When `prefix + description` already reaches RULE_COL - 1 or beyond, emit it on its own
    line and put `suffix` on a continuation line indented by RULE_COL spaces. Returns 1 or 2
    lines, each rstrip()ed. Widths are Python code points (len()), not display columns —
    combining marks in the IPA make the two differ, and code points are what a test can
    assert (V-32).
    """
    head = prefix + description
    if not suffix:
        return [head.rstrip()]
    if len(head) >= RULE_COL - 1:
        return [head.rstrip(), (" " * RULE_COL + suffix).rstrip()]
    return [(head.ljust(RULE_COL) + suffix).rstrip()]


def _forward_steps(steps: Sequence[Step]) -> tuple[Step, ...]:
    """The walk's steps in FORWARD stage order — a stable sort, so two steps of one stage keep
    their walk order (V-31)."""
    return tuple(sorted(steps, key=lambda step: FORWARD_STAGES.index(step.stage)))


def _weakest_tag(steps: Sequence[Step]) -> str:
    """The weakest tag across the walk under `attested < design < fallback`; an empty tag
    counts as attested (V-31)."""
    return _TAG_NAME[max((_TAG_RANK.get(step.tag, 0) for step in steps), default=0)]


def _dedupe(values: Sequence[str]) -> tuple[str, ...]:
    return tuple(dict.fromkeys(values))


def _line_of(alt: Alternative) -> ConstraintLine:
    """Collapse one alternative's whole walk into a single constraint line (V-31)."""
    steps = _forward_steps(alt.steps)
    kind = next((step.kind for step in steps if step.stage == "substitute"), "identity")
    contexts = tuple((step.rule_id, step.context) for step in steps if step.context)
    return ConstraintLine(
        description=g2p_inverse.describe(alt.segments) + _KIND_PHRASE.get(kind, ""),
        rule_ids=_dedupe([step.rule_id for step in steps]),
        tag=_weakest_tag(steps),
        kind=kind,
        context=" ; ".join(context for _rid, context in contexts),
        contexts=contexts,
    )


def _merge_lines(lines: Sequence[ConstraintLine]) -> tuple[ConstraintLine, ...]:
    """One line per distinct `(description, kind, tag, context)`; merged lines concatenate
    their rule ids, first occurrence winning (V-31). Sorted by kind, then design last, then
    first rule id, then description."""
    merged: dict[tuple[str, str, str, str], ConstraintLine] = {}
    for line in lines:
        key = (line.description, line.kind, line.tag, line.context)
        seen = merged.get(key)
        if seen is None:
            merged[key] = line
            continue
        merged[key] = ConstraintLine(
            description=seen.description,
            rule_ids=_dedupe(seen.rule_ids + line.rule_ids),
            tag=seen.tag, kind=seen.kind, context=seen.context, label=seen.label,
            contexts=tuple(dict.fromkeys(seen.contexts + line.contexts)))
    return tuple(sorted(merged.values(),
                        key=lambda l: (_KIND_RANK.get(l.kind, 9),
                                       1 if l.tag == "design" else 0,
                                       l.rule_ids[0] if l.rule_ids else "",
                                       l.description)))


def _target_text(slot: Slot) -> str:
    """The slot's cell of the `target segments:` line: every distinct target alternative, the
    segments of one joined by " " and the alternatives by "|" (spec §3.1, V-1). No pick is
    made — an ambiguous respell chunk shows all of its sources."""
    if not slot.targets:
        return slot.text
    return "|".join(" ".join(alt) for alt in slot.targets)


def constraints(pattern: Pattern) -> tuple[Constraint, ...]:
    """One `Constraint` per slot: its label, the target segments it prints, and its lines."""
    out: list[Constraint] = []
    for slot in pattern.slots:
        lines = _merge_lines([_line_of(alt) for alt in slot.alts])
        out.append(Constraint(label=slot.text,
                              target=_target_text(slot),
                              lines=lines, notes=slot.notes, unconstrained=not lines))
    return tuple(out)


def dropped_lines(pattern: Pattern) -> tuple[ConstraintLine, ...]:
    """The `possibly dropped` block: one line per `(segments, tag, context)`, once per WORD and
    never a note on a slot (V-7, owner ruling).

    The key includes the deleted segments — V-7 writes it as `(description, tag, context)`, but
    the description of a deletion is the fixed phrase, so keying on it alone would merge
    Welsh's `w -> 0` and `j -> 0` into one line and lose which segment went.

    The label is the segment the SECTION deleted, so a `[substitute]` deletion labels an Irish
    segment and a `[repair]`/`[post-stress]` one labels a segment of the strand — each is the
    segment that would have gone missing at that stage, which is what the reader needs.
    """
    merged: dict[tuple[str, str, str], ConstraintLine] = {}
    for deletion in pattern.deletions:
        label = "".join(deletion.segments)
        tag = _TAG_NAME[_TAG_RANK.get(deletion.tag, 0)]
        key = (label, tag, deletion.context)
        seen = merged.get(key)
        rule_ids = (deletion.rule_id,) if seen is None else seen.rule_ids + (deletion.rule_id,)
        merged[key] = ConstraintLine(
            description=_DROPPED_PHRASE, rule_ids=_dedupe(rule_ids), tag=tag, kind="rule",
            context=deletion.context, label=label,
            contexts=((deletion.rule_id, deletion.context),) if deletion.context else ())
    return tuple(sorted(merged.values(), key=lambda l: (l.rule_ids[0], l.label)))


# ---- the Irish spelling pattern (spec §3.4, §4; V-14, V-30, R7) --------------------------------

def _graphemes_of(segments: tuple[str, ...]) -> tuple[str, ...]:
    """The Irish letters that read as this segment sequence — vowel runs first, then the
    consonant registry (V-27/V-19). No quality words: this is the pattern line, not the
    description column."""
    runs = g2p_inverse.VOWEL_READINGS.get(segments)
    if runs:
        return tuple(runs)
    return _dedupe([reading.grapheme for reading in g2p_inverse.readings_for(segments)])


def _is_nucleus(segments: tuple[str, ...]) -> bool:
    return bool(segments) and all(seg in g2p_inverse.g2p.VOWEL_SEGMENTS for seg in segments)


def _slot_quality(slot: Slot) -> str:
    """The quality of a consonant slot: the first-listed reading's (V-14). `""` when the slot
    is a nucleus, has no reading, or its reading admits either quality."""
    for alt in slot.alts:
        if not alt.segments or _is_nucleus(alt.segments):
            return ""
        readings = g2p_inverse.readings_for(alt.segments)
        if readings:
            quality = readings[0].quality
            return "" if quality == g2p_inverse.EITHER else quality
    return ""


def _slot_graphemes(slots: Sequence[Slot], index: int) -> tuple[str, ...]:
    """The alternation printed for one slot, caol le caol respected (V-14).

    Epenthesis alternatives are excluded — they spell nothing, and the rendering says so on its
    own `or, with … inserted` line instead. A nucleus slot keeps only the vowel runs whose
    imposed qualities match the first-listed reading of the consonant slot on each side; when
    the filter empties the slot it falls back to the unfiltered alternation.
    """
    slot = slots[index]
    graphemes: list[str] = []
    nucleus = False
    for alt in slot.alts:
        if not alt.segments:
            continue                                  # epenthesis: no letter (V-14)
        nucleus = nucleus or _is_nucleus(alt.segments)
        for grapheme in _graphemes_of(alt.segments):
            if grapheme not in graphemes:
                graphemes.append(grapheme)
    if not nucleus or not graphemes:
        return tuple(graphemes)
    left = _slot_quality(slots[index - 1]) if index else ""
    right = _slot_quality(slots[index + 1]) if index + 1 < len(slots) else ""
    kept = [g for g in graphemes
            if (not left or g2p_inverse.QUALITY_LEFT.get(g, g2p_inverse.EITHER)
                in (left, g2p_inverse.EITHER))
            and (not right or g2p_inverse.QUALITY_RIGHT.get(g, g2p_inverse.EITHER)
                 in (right, g2p_inverse.EITHER))]
    return tuple(kept or graphemes)


def _slot_text(slots: Sequence[Slot], index: int) -> str:
    slot = slots[index]
    if slot.kind == ANY:
        return "*"
    graphemes = list(_slot_graphemes(slots, index))
    if not graphemes:
        return "?"
    if len(graphemes) > _ALT_CAP:
        graphemes = graphemes[:_ALT_CAP] + ["…"]
    return graphemes[0] if len(graphemes) == 1 else "(" + "|".join(graphemes) + ")"


def _insertions(pattern: Pattern) -> tuple[tuple[int, int, tuple[Step, ...]], ...]:
    """Every span the engine could have inserted: the optional groups of `[repair]` /
    `[post-stress]` (V-30), plus each slot carrying a `[substitute]` epenthesis alternative
    (the Georgian *v* of spec §4 is one of those, not a group)."""
    spans: dict[tuple[int, int], list[Step]] = {}
    for group in pattern.groups:
        spans.setdefault((group.start, group.stop), []).extend(group.steps)
    for index, slot in enumerate(pattern.slots):
        steps = [step for alt in slot.alts if not alt.segments for step in alt.steps
                 if step.kind == "epenthesis"]
        if steps:
            spans.setdefault((index, index + 1), []).extend(steps)
    return tuple((start, stop, tuple(dict.fromkeys(steps)))
                 for (start, stop), steps in sorted(spans.items()))


def _base_line(pattern: Pattern, *, drop: tuple[int, int] | None = None) -> str:
    """The rendering, with an optional group wrapped `( … )?` and `drop`'s span left out."""
    slots = pattern.slots
    groups = {(g.start, g.stop) for g in pattern.groups}
    parts: list[str] = []
    index = 0
    while index < len(slots):
        span = next((s for s in sorted(groups) if s[0] == index), None)
        if drop is not None and index == drop[0]:
            index = drop[1]
            continue
        if span is not None and span != drop:
            inner = "".join(_slot_text(slots, i) for i in range(span[0], span[1]))
            parts.append(f"({inner})?")
            index = span[1]
            continue
        parts.append(_slot_text(slots, index))
        index += 1
    return "  " + "".join(parts)


def render_pattern(pattern: Pattern) -> tuple[str, ...]:
    """The Irish spelling pattern: one base line, then one line per insertion (V-14, Q2).

    Alternation is printed, never resolved to a pick (R7); the rendering is a description, not
    a claim — `verify` is what checks a concrete spelling.
    """
    lines = [_base_line(pattern)]
    for start, stop, steps in _insertions(pattern):
        labels = "".join(pattern.slots[i].text for i in range(start, stop)) or "?"
        contexts = _dedupe([step.context for step in steps if step.context])
        detail = " ; ".join(contexts) if contexts else "no environment"
        without = _base_line(pattern, drop=(start, stop)).strip() or "(nothing)"
        lines.append(f"  or, with {labels} inserted:  {without}   (context: {detail})")
    return tuple(lines)


# ---- the report (spec §4; V-13, V-32) ----------------------------------------------------------

#: `identity` and `fallback` are not rule ids — they are the pseudo-ids V-8/V-9 give a source
#: with no rule behind it. The tag and the description already say so, and spec §4's own `v`
#: line (a respell identity plus `substitute:79`) prints the rule id alone, so they are dropped
#: from the rule column whenever a real rule id is on the line.
_PSEUDO_IDS = ("identity", "fallback")


def _rule_suffix(line: ConstraintLine) -> str:
    tag = f" %{line.tag}" if line.tag in ("design", "fallback") else ""
    ids = tuple(r for r in line.rule_ids if r not in _PSEUDO_IDS) or line.rule_ids
    return ",".join(ids) + tag


def _example_lines(examples: Sequence[Example]) -> list[str]:
    width1 = max([11] + [len(e.orthography) + 2 for e in examples])
    width2 = max([9] + [len(e.respelling) + 2 for e in examples])
    out: list[str] = []
    for example in examples:
        text = "  " + example.orthography.ljust(width1) + example.respelling.ljust(width2)
        text += example.ipa
        if example.flags:
            text += "  " + " ".join(example.flags)
        if example.fallbacks:
            text += f"  fallbacks:{example.fallbacks}"
        out.append(text.rstrip())
    return out


def report(word: str, strand: str, pattern: Pattern, examples: Sequence[Example] = (),
           *, tried: int = 0, cap_hit: bool = False, verified: bool = True) -> list[str]:
    """The whole §4 block for one word, as lines without newlines.

    Section order and content are the spec's; every rule-bearing line goes through the one
    formatter (V-32), so the rule column cannot drift between blocks.
    """
    found = constraints(pattern)
    out = [f"{word}  [{strand}]",
           "target segments: " + " ".join(c.target for c in found),
           "",
           "constraints"]

    for constraint in found:
        if constraint.unconstrained:
            out.append(f"  {constraint.label:<3} unconstrained".rstrip())
        for index, line in enumerate(constraint.lines):
            prefix = f"  {constraint.label:<3} ← " if index == 0 else "      ← "
            out.extend(format_rule_line(prefix, line.description, _rule_suffix(line)))
        for note in constraint.notes:
            out.append(f"      note: {note}")
    printed = {note for c in found for note in c.notes}
    for note in pattern.notes:
        if note not in printed:            # a slot already printed its own note above
            out.append(f"  note: {note}")

    dropped = dropped_lines(pattern)
    if dropped:
        out.extend(["", "possibly dropped"])
        for line in dropped:
            out.extend(format_rule_line(f"  {line.label:<3} ", line.description,
                                        _rule_suffix(line)))

    # V-13 (Q1): one line per context-bearing STEP, carrying that step's own environment
    # verbatim. Nothing here negates or evaluates a context (R2).
    exclusions: list[str] = []
    for constraint in found:
        for line in constraint.lines:
            for rule_id, context in line.contexts:
                exclusions.extend(format_rule_line(
                    f"  {constraint.label} ← ",
                    f"{line.description}: only when  {context}", f"({rule_id} context)"))
    if exclusions:
        out.extend(["", "exclusions"] + exclusions)

    out.extend(["", "Irish spelling pattern"])
    out.extend(render_pattern(pattern))

    out.append("")
    if not verified:
        out.append("verified examples: skipped (--examples 0)")
        return out
    header = (f"verified examples ({len(examples)} of {tried} tried; "
              "0 fallbacks unless shown)")
    if cap_hit:
        header += "; candidate cap 2000 hit"
    out.append(header)
    out.extend(_example_lines(examples) if examples else ["  none"])
    return out


# ---- expansion and verification (spec §3.5; V-22 … V-26, V-30, V-34) ---------------------------

CAP = 2000                            # R4: candidates per word; no --cap flag in v1

#: R5's palette in Irish IPA: the five short vowels, then `r l n m s d t c g b` broad (V-23).
PALETTE = ("a", "ɛ", "ɪ", "ɔ", "ʊ", "ɾˠ", "l̪ˠ", "n̪ˠ", "mˠ", "sˠ",
           "d̪ˠ", "t̪ˠ", "k", "ɡ", "bˠ")
STAR_LENGTHS = (0, 1, 2)              # R5: a `*` is filled with 0, 1 then 2 palette segments

_RANK_OF_KIND = {"identity": 0, "rule": 1, "fallback": 3, "epenthesis": 4}
#: `ˈ ˌ .` only — `$` and the space of `MARKS` are not stress marks (V-25).
_STRESS_MARKS = "ˈˌ."


@dataclass(frozen=True)
class Candidate:
    segments: tuple[str, ...]
    rank: int


@dataclass(frozen=True)
class _Option:
    """One filling of one unit — a slot, or a whole optional group (V-24)."""
    segments: tuple[str, ...]
    rank: int


def _unmark(text: str) -> str:
    """`ˈ ˌ .` stripped: stress is ignored everywhere in reverse (V-18, V-25)."""
    return "".join(ch for ch in text if ch not in _STRESS_MARKS)


def _rank_of_steps(steps: Sequence[Step]) -> int:
    """V-22's cost from a step trail: the OLDEST step (the `[substitute]` one) decides.
    `0` identity, `1` rule, `2` rule tagged `%design`, `3` fallback, `4` epenthesis."""
    if not steps:
        return 0
    step = steps[-1]
    base = _RANK_OF_KIND.get(step.kind, 1)
    return 2 if base == 1 and step.tag == "design" else base


def rank(alt: Alternative) -> int:
    """V-22: the alternative's OLDEST step — the `[substitute]` one — decides its cost."""
    return _rank_of_steps(alt.steps)


def _alt_options(alts: Sequence[Alternative]) -> list[_Option]:
    """A slot's alternatives as options, cheapest first — a STABLE sort, so alternatives of
    equal rank keep their file order (V-22, V-24)."""
    options = [_Option(segments=alt.segments, rank=rank(alt)) for alt in alts]
    return sorted(options, key=lambda option: option.rank)


def _palette_options() -> list[_Option]:
    """A `ONE` slot with no inverted class draws from the palette (V-23). A palette segment is
    an Irish segment taken as itself, so it costs what an identity source costs."""
    return [_Option(segments=(seg,), rank=0) for seg in PALETTE]


def _star_options() -> list[_Option]:
    """0, then 1, then 2 palette segments — 1 + 15 + 225 = 241 fillings, in that order
    (V-23)."""
    options = [_Option(segments=(), rank=0)]
    for length in STAR_LENGTHS[1:]:
        for combination in itertools.product(PALETTE, repeat=length):
            options.append(_Option(segments=combination, rank=0))
    return options


def _slot_options(slot: Slot) -> list[_Option]:
    """The option list of one slot.

    A `SEG` slot whose alternatives were all dropped by `un_substitute` has NO Irish source at
    all (Welsh `th` ← /θ/, which no Irish segment reaches), so its option list is empty and the
    word has no candidates. That is the one place reverse does not over-generate: inventing a
    palette filling there would claim an Irish source the map denies.
    """
    if slot.kind == ANY:
        return _star_options()
    if slot.alts:
        return _alt_options(slot.alts)
    if slot.kind == ONE:
        return _palette_options()
    return []


def _group_options(slots: Sequence[Slot], group: OptionalGroup) -> list[_Option]:
    """One option list shared by the whole span, so the group is present or absent ATOMICALLY
    (V-30): a two-segment insertion can never be half-filled.

    Option 0 is `absent` at rank 0 (V-22) — the span's letters were inserted by the rule, so
    the Irish word carries nothing for them. Then EVERY present combination (V-24: the option
    list holds each of them, uncapped — a group spans SEG slots only, so the product is the
    product of a few alternative lists), each at the GROUP's own rank (V-22: present costs the
    group's epenthesis provenance, not its constituents'). Within `present`, combinations are
    stably ordered by the summed rank of their constituent slot options, so the group's own
    option list is still cheapest first (V-24).
    """
    options = [_Option(segments=(), rank=0)]
    per_slot = [_slot_options(slot) for slot in slots[group.start:group.stop]]
    if any(not column for column in per_slot):
        return options
    present_rank = _rank_of_steps(group.steps)
    combinations = list(itertools.product(*per_slot))
    combinations.sort(key=lambda combo: sum(option.rank for option in combo))
    options.extend(
        _Option(segments=tuple(seg for option in combo for seg in option.segments),
                rank=present_rank)
        for combo in combinations)
    return options


def _units(pattern: Pattern) -> list[list[_Option]]:
    """The pattern as independent option lists, left to right: one per slot, except that an
    optional group's whole span is a SINGLE unit (V-24, V-30)."""
    groups = {group.start: group for group in pattern.groups}
    units: list[list[_Option]] = []
    index = 0
    while index < len(pattern.slots):
        group = groups.get(index)
        if group is not None:
            units.append(_group_options(pattern.slots, group))
            index = group.stop
            continue
        units.append(_slot_options(pattern.slots[index]))
        index += 1
    return units


def expand(pattern: Pattern, *, cap: int = CAP):
    """Concrete Irish candidates, breadth-first and cheapest first (spec §3.5, V-24).

    Per-unit option lists are rank-ordered (V-22), so a candidate's cost is the SUM of its
    chosen option indices; candidates come out by ascending cost, ties broken lexicographically
    by the index tuple. A `heapq` over index tuples means the cap can be applied without
    materialising the product. `Candidate.rank` is that cost — 0 for the cheapest candidate,
    which is the one whose every unit took its cheapest source.

    Duplicate segment sequences (two index tuples that spell the same Irish word) are emitted
    once; `cap` counts what is emitted.
    """
    units = _units(pattern)
    if any(not unit for unit in units):
        return
    if not units:
        yield Candidate(segments=(), rank=0)
        return

    start = (0,) * len(units)
    heap: list[tuple[int, tuple[int, ...]]] = [(0, start)]
    queued = {start}
    emitted: set[tuple[str, ...]] = set()
    count = 0
    while heap and count < cap:
        cost, indexes = heapq.heappop(heap)
        segments = tuple(seg for unit, i in zip(units, indexes) for seg in unit[i].segments)
        if segments not in emitted:
            emitted.add(segments)
            count += 1
            yield Candidate(segments=segments, rank=cost)
        for position, index in enumerate(indexes):
            if index + 1 < len(units[position]):
                nxt = indexes[:position] + (index + 1,) + indexes[position + 1:]
                if nxt not in queued:
                    queued.add(nxt)
                    heapq.heappush(heap, (cost + 1, nxt))


def _matches(text: str, pattern: str) -> bool:
    """V-25: `fnmatchcase` on both sides NFC-normalized and casefolded BY US, so the host OS's
    case rules never enter."""
    return fnmatch.fnmatchcase(_fold(text), _fold(pattern))


def _forward(spelling: str, irish: RuleFile, target: RuleFile, table: FeatureTable):
    """One real forward run, or `None` when the engine cannot run this candidate (V-26).

    A synthetic candidate is allowed to be unpronounceable: `MissingSlot`, `SegmentError`,
    `RuleError` and `ConstructionNotInStrand` are caught and counted, never propagated.
    """
    from . import g2p, inputs, pipeline
    from .irish import MissingSlot
    from .rewrite import RuleError

    try:
        entry = inputs.infer(inputs.Entry(orthography=spelling, ipa=g2p.g2p(spelling)[0]),
                             irish, table)
        return pipeline.run_entry(entry, "DESC", irish, target, table)
    except (MissingSlot, SegmentError, RuleError, pipeline.ConstructionNotInStrand,
            g2p.G2PError):
        return None


def verify(pattern: Pattern, target: RuleFile, irish: RuleFile, table: FeatureTable,
           *, limit: int = 8, cap: int = CAP, ipa_mode: bool = False,
           raw_pattern: str | None = None) -> tuple[tuple[Example, ...], int, bool]:
    """Run candidates forward and keep the ones that really match (spec §3.5, V-26, V-34).

    Every spelling `g2p_inverse.spell` returns is tried, not just the first: the spelling that
    matches is frequently not the first one (Georgian `Ar*v*` wants *ardmhaor*, and ⟨bh⟩
    precedes ⟨mh⟩ in the `g2p` table). A `(segments, spelling)` pair already tried is skipped
    before any forward work — the same spelling reaches the same `Result` — so `tried` counts
    UNIQUE forward runs, and `cap` bounds THAT counter only. The candidate stream keeps its own
    `CAP` (V-24): a candidate whose `spell()` is empty costs no forward run, so it must not
    consume the forward-run budget and hide a later candidate that matches.

    Returns `(examples, tried, cap_hit)`; examples are sorted by
    `(fallbacks, len(flags), rank, spelling_index)`, de-duplicated by orthography and truncated
    to `limit`.
    """
    wanted = pattern.text if raw_pattern is None else raw_pattern
    found: list[Example] = []
    seen: set[tuple[tuple[str, ...], str]] = set()
    tried = 0
    produced = 0
    cap_hit = False

    for candidate in expand(pattern, cap=CAP):
        produced += 1
        if tried >= cap:
            cap_hit = True
            break
        for index, spelling in enumerate(g2p_inverse.spell(candidate.segments)):
            key = (candidate.segments, spelling)
            if key in seen:
                continue
            seen.add(key)
            if tried >= cap:
                cap_hit = True
                break
            tried += 1
            result = _forward(spelling, irish, target, table)
            if result is None:
                continue
            text = _unmark(result.ipa) if ipa_mode else result.respelling
            if not _matches(text, wanted):
                continue
            found.append(Example(orthography=spelling, respelling=result.respelling,
                                 # Stress is ignored everywhere in reverse (V-18), and spec §4's
                                 # own example block prints unmarked IPA.
                                 ipa=_unmark(result.ipa), flags=result.flags,
                                 fallbacks=result.fallbacks, rank=candidate.rank,
                                 spelling_index=index))
    if produced >= CAP:
        cap_hit = True

    ordered = sorted(found, key=lambda e: (e.fallbacks, len(e.flags), e.rank, e.spelling_index))
    examples: list[Example] = []
    printed: set[str] = set()
    for example in ordered:
        if example.orthography in printed:
            continue
        printed.add(example.orthography)
        examples.append(example)
        if len(examples) == limit:
            break
    return tuple(examples), tried, cap_hit


# ---- old-irish (R6, spec §2) -------------------------------------------------------------------

def old_irish_matches(pattern: str, path=None) -> tuple[tuple[str, str, str], ...]:
    """Old Irish is a lexicon lookup only (R6): no constraint set, no inversion.

    Every lexicon row with a non-empty `oi_nom` whose citation form matches `pattern` under the
    same fnmatch as everything else (V-25), as `(oi_nom, orthography, flag)`, sorted by
    `lexicon.key(orthography)`. Rows with no `oi_nom` (`status = none`) are skipped: there is no
    Old Irish form to match against.
    """
    from . import lexicon
    rows = [(entry.oi_nom, entry.orthography, entry.flag)
            for entry in lexicon.read_lexicon(path).values()
            if entry.oi_nom and _matches(entry.oi_nom, pattern)]
    return tuple(sorted(rows, key=lambda row: lexicon.key(row[1])))


def old_irish_report(word: str, matches: Sequence[tuple[str, str, str]]) -> list[str]:
    """The old-irish block: the header, the "§3 does not apply" note, and the match table."""
    out = [f"{word}  [old-irish]",
           "note: old-irish is lexicon lookup only; §3's constraint set does not apply.",
           "",
           "matches"]
    if not matches:
        out.append("  none")
        return out
    w1 = max(len(row[0]) for row in matches) + 2
    w2 = max(len(row[1]) for row in matches) + 2
    for oi_nom, orthography, flag in matches:
        out.append(f"  {oi_nom:<{w1}}{orthography:<{w2}}{flag}".rstrip())
    return out
