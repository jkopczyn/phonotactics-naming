"""Rewrite engine: matching, captures, backreferences and rule application.

Plan Task 7; spec §3 (rule DSL) and §12.C (inline sets, captures/backreferences, exact
feature-change lookup). Interpretations implemented here:

- I-5  a target is a sequence of one-segment items; a replacement is literal segments, `0`,
       backreferences, quoted text or one feature-change bundle.
- I-6  simultaneous application: every match and every context is evaluated against the
       PRE-RULE word; all replacements are applied at once; one trace entry per rule that
       changed anything, recording the whole word before/after.
- I-7  `0 -> X` (epenthesis) inserts once at every position whose environment matches.
- I-8  `.` and `ˈ` are context-only (the parser enforces it; here they are zero-width atoms).
- I-9  `(X)` matches 0 or 1 segment, `X*` 0 or more; both greedy with backtracking.
- I-4  a feature-change bundle resolves by exact vector lookup; failure is a `RuleError`.
- I-33 captures record the single segment an item matched; `\\n` copies it.

Context conventions: the left context is matched right-to-left ending at the span start, the
right context left-to-right from the span end. Zero-width atoms test a BOUNDARY position
`0..len(segments)`: `#` is 0 / len, `$` a member of `word.morphemes`, `.` a syllable start,
`ˈ` the stressed syllable's first segment (or the parked pre-syllabification stress index).

Quoted text (`[respell]` only) is emitted as its literal string; the opaque-chunk semantics
of I-19 (later rules never rematch it) belong to `respell.py` (Task 21).
"""
from __future__ import annotations

from collections.abc import Sequence

from .dsl import Backref, Bundle, CtxItem, ItemSpec, QuotedText, Rule, RuleFile
from .features import FeatureError, FeatureTable
from .word import TraceEntry, Word

__all__ = ["RuleError", "match_item", "find_matches", "apply_rule", "apply_section"]

Captures = dict[int, str]
Match = tuple[int, int, Captures]


class RuleError(Exception):
    """A rule cannot be applied at runtime: undeclared class, unknown feature, undefined
    backreference, or a feature change with no exact segment (I-4)."""


# ---- item matching --------------------------------------------------------------------------

def _class_members(name: str, rf: RuleFile, rule: Rule | None = None) -> tuple[str, ...]:
    try:
        return rf.classes[name]
    except KeyError:
        where = f" in {rule.rule_id}" if rule else ""
        raise RuleError(f"undeclared class {name!r}{where}") from None


def match_item(spec: ItemSpec, segment: str, rf: RuleFile, table: FeatureTable, *,
               word: Word | None = None, index: int | None = None) -> bool:
    """Does one target/context item match one segment? `word`/`index` locate the segment
    for the orth-tag channel (Old Irish spec §4/§11, O-6): an `@orth("…")` item or an
    `orth=` bundle constraint compares against `word.tag_at(index)`, and matches nothing
    when they are absent — the same "no tag, no match" behaviour as an untagged word."""
    kind, value = spec.kind, spec.value
    if kind == "orth":
        return _orth_ok(value, word, index)                         # type: ignore[arg-type]
    if kind == "segment":
        return segment == value
    if kind == "class":
        return segment in _class_members(value, rf)
    if kind == "set":
        for member in value:
            if member == segment:
                return True
            if member[0].isupper() and member in rf.classes and segment in rf.classes[member]:
                return True
        return False
    if kind == "bundle":
        assert isinstance(value, Bundle)
        if value.orth is not None and not _orth_ok(value.orth, word, index):
            return False
        if value.class_name is not None and segment not in _class_members(value.class_name, rf):
            return False
        try:
            return table.matches(segment, value.constraints)
        except FeatureError as e:
            raise RuleError(str(e)) from None
    raise RuleError(f"unknown item kind {kind!r}")


def _orth_ok(tag: str, word: Word | None, index: int | None) -> bool:
    if word is None or index is None:
        return False
    return word.tag_at(index) == tag


# ---- context matching -----------------------------------------------------------------------

def _boundary(atom: str, pos: int, word: Word) -> bool:
    if atom == "#":
        return pos == 0 or pos == len(word.segments)
    if atom == "$":
        return pos in word.morphemes
    if atom == ".":
        return pos in word.syllables
    if atom == "ˈ":
        if word.stress is not None and word.stress < len(word.syllables):
            return pos == word.syllables[word.stress]
        return word._pending_stress is not None and pos == word._pending_stress
    raise RuleError(f"unknown context symbol {atom!r}")


def _edge_ok(atom: str, pos: int, word: Word, step: int) -> bool:
    """`#` is directional: in a left context (step -1) it is the word start, in a right
    context (step +1) the word end."""
    if atom == "#":
        return pos == (0 if step < 0 else len(word.segments))
    return _boundary(atom, pos, word)


def _match_ctx(items: Sequence[CtxItem], k: int, pos: int, step: int, word: Word,
               rf: RuleFile, table: FeatureTable, caps: Captures) -> Captures | None:
    """Match items[k:] starting at boundary `pos`, consuming segments in direction `step`
    (+1: segment at pos; -1: segment at pos-1). Greedy with backtracking. Returns the
    captures gathered (a new dict) or None."""
    if k == len(items):
        return caps
    item = items[k]
    atom = item.atom
    if isinstance(atom, str):
        if not _edge_ok(atom, pos, word, step):
            return None
        return _match_ctx(items, k + 1, pos, step, word, rf, table, caps)

    def seg_at(p: int) -> str | None:
        i = p if step > 0 else p - 1
        if 0 <= i < len(word.segments):
            return word.segments[i]
        return None

    # how many segments can this item consume, greedily?
    if item.star:
        limit = len(word.segments)
    elif item.optional:
        limit = 1
    else:
        limit = 1
    count = 0
    p = pos
    while count < limit:
        s = seg_at(p)
        if s is None or not match_item(atom, s, rf, table, word=word,
                                       index=p if step > 0 else p - 1):
            break
        count += 1
        p += step
    minimum = 0 if (item.star or item.optional) else 1
    while count >= minimum:
        p = pos + count * step
        new_caps = caps
        if atom.capture is not None and count == 1:
            new_caps = dict(caps)
            new_caps[atom.capture] = seg_at(pos)  # type: ignore[assignment]
        result = _match_ctx(items, k + 1, p, step, word, rf, table, new_caps)
        if result is not None:
            return result
        count -= 1
    return None


def _match_env(word: Word, rule: Rule, start: int, stop: int, rf: RuleFile,
               table: FeatureTable, caps: Captures) -> Captures | None:
    left = _match_ctx(tuple(reversed(rule.left)), 0, start, -1, word, rf, table, caps)
    if left is None:
        return None
    return _match_ctx(rule.right, 0, stop, +1, word, rf, table, left)


def _match_target(word: Word, rule: Rule, start: int, rf: RuleFile,
                  table: FeatureTable) -> Captures | None:
    caps: Captures = {}
    if start + len(rule.target) > len(word.segments):
        return None
    for j, spec in enumerate(rule.target):
        seg = word.segments[start + j]
        if not match_item(spec, seg, rf, table, word=word, index=start + j):
            return None
        if spec.capture is not None:
            caps[spec.capture] = seg
    return caps


def find_matches(word: Word, rule: Rule, rf: RuleFile,
                 table: FeatureTable) -> list[Match]:
    """Non-overlapping (start, stop, captures) triples, leftmost-longest, all evaluated
    against the PRE-RULE word (I-6). `captures` maps capture index -> the matched
    segment string, gathered from both the target and the environment (I-33).
    Epenthesis rules return zero-width spans."""
    out: list[Match] = []
    n = len(word.segments)
    if not rule.target:                              # epenthesis (I-7)
        for pos in range(n + 1):
            caps = _match_env(word, rule, pos, pos, rf, table, {})
            if caps is not None:
                out.append((pos, pos, caps))
        return out
    width = len(rule.target)
    i = 0
    while i + width <= n:
        caps = _match_target(word, rule, i, rf, table)
        if caps is not None:
            caps = _match_env(word, rule, i, i + width, rf, table, caps)
        if caps is not None:
            out.append((i, i + width, caps))
            i += width
        else:
            i += 1
    return out


# ---- application ----------------------------------------------------------------------------

def _replacement(word: Word, rule: Rule, start: int, stop: int, caps: Captures,
                 table: FeatureTable) -> tuple[str, ...]:
    repl = rule.replacement
    if isinstance(repl, Bundle):
        out = []
        for seg in word.segments[start:stop]:
            try:
                out.append(table.apply_changes(seg, repl.constraints))
            except FeatureError as e:
                raise RuleError(f"{rule.rule_id}: {e}") from None
        return tuple(out)
    out = []
    for el in repl:
        if isinstance(el, str):
            out.append(el)
        elif isinstance(el, Backref):
            if el.n not in caps:
                raise RuleError(f"{rule.rule_id}: backreference \\{el.n} is undefined "
                                f"(captures: {sorted(caps)})")
            out.append(caps[el.n])
        elif isinstance(el, QuotedText):
            out.append(el.text)
        else:  # pragma: no cover
            raise RuleError(f"{rule.rule_id}: bad replacement element {el!r}")
    return tuple(out)


def apply_rule(word: Word, rule: Rule, rf: RuleFile, table: FeatureTable, stage: str) -> Word:
    """Apply one rule simultaneously at every match (I-6). Returns the word unchanged (no
    trace entry) when nothing matches or every replacement equals its span."""
    matches = find_matches(word, rule, rf, table)
    edits = []
    for start, stop, caps in matches:
        new = _replacement(word, rule, start, stop, caps, table)
        if new != word.segments[start:stop]:
            edits.append((start, stop, new))
    if not edits:
        return word
    before = word.ipa()
    out = word
    # Insertion affinity at a `$`: an epenthesis rule whose right context starts with `$`
    # inserts on the left (stem) side of the boundary (`p _ $` -> `pi$`); any other rule,
    # `$ _` included, leaves the boundary before the new material (`$ _` -> `p$i`).
    left_side = (not rule.target and bool(rule.right)
                 and isinstance(rule.right[0].atom, str) and rule.right[0].atom == "$")
    for start, stop, new in reversed(edits):     # right-to-left keeps earlier indices valid
        out = out.replaced(start, stop, new, before_boundary=left_side)
    if not rule.target:
        # Pure epenthesis: remember which segments this rule INSERTED, so a later stage can
        # tell overlay material from the word's own (`[repair] overlay-undo`). Indices are the
        # post-edit ones: `edits` is in ascending order, so a running offset places each one.
        inserted: list[int] = []
        offset = 0
        for start, stop, new in edits:
            inserted.extend(range(start + offset, start + offset + len(new)))
            offset += len(new) - (stop - start)
        out = out.with_origins(inserted, rule.rule_id)
    return out.traced(TraceEntry(stage=stage, rule_id=rule.rule_id, tag=rule.tag,
                                 before=before, after=out.ipa()))


def apply_section(word: Word, rules: Sequence[Rule], rf: RuleFile,
                  table: FeatureTable, stage: str) -> Word:
    """Apply rules in file order; each rule sees the previous rule's output."""
    for rule in rules:
        word = apply_rule(word, rule, rf, table, stage)
    return word
