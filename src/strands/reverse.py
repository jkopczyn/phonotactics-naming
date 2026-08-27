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

Later tasks add `widen` (§3.3), `expand`, `verify` and the report; the dataclasses they need
(`Source`, `Deletion`, `OptionalGroup`) live here.
"""
from __future__ import annotations

import itertools
import re
import unicodedata
from dataclasses import dataclass
from typing import Sequence

from .dsl import Backref, Bundle, CtxItem, ItemSpec, QuotedText, Rule, RuleFile
from .features import FeatureError, FeatureTable
from .rewrite import match_item
from .tokenize import MARKS, SegmentError, tokenize

__all__ = [
    "ANY", "ONE", "SEG", "Step", "Alternative", "RespellSource", "Source", "Deletion",
    "OptionalGroup", "Slot", "Pattern", "ReverseError", "env_text", "invert_respell",
    "parse_pattern", "parse_ipa_pattern", "SourceMap", "section_inventory", "expand_target",
    "source_map", "un_substitute",
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
                    covered.add((seg,))
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
    oldest). An alternative with no entry is kept as it is, without a substitute step — the
    over-generating reading of §3: it simply never verifies, and V-31 already gives a stepless
    alternative the kind `identity`. `deletions` and `notes` are the other two members of the
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
            sources = smap.get(alt.segments, ())
            if not sources:
                keep(alt)
                continue
            for source in sources:
                keep(Alternative(segments=source.segments,
                                 steps=alt.steps + (Step(stage="substitute",
                                                         rule_id=source.rule_id,
                                                         tag=source.tag, context=source.context,
                                                         kind=source.kind),)))
        slots.append(Slot(kind=slot.kind, text=slot.text, alts=tuple(alts), notes=slot.notes))

    extra = tuple(note for note in notes if note not in pattern.notes)
    return Pattern(text=pattern.text, slots=tuple(slots), groups=pattern.groups,
                   deletions=pattern.deletions + tuple(deletions),
                   notes=pattern.notes + extra)
