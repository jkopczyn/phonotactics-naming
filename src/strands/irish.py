"""Irish source-side pre-pass: mutations and inflections (plan Task 17; spec §3, §4.1, §12.J).

`irish.rules` carries the lenition / eclipsis / prothesis tables under `[mutations]` and the
named regular inflections under `[inflect]` (I-15 sub-tables). Both hold ordinary rewrite
rules, but they are run differently:

- A **mutation** is one phoneme -> phoneme table (digest §3.1, §3.2): the whole table is
  applied in a single simultaneous pass against the pre-mutation word, and a span rewritten
  by one rule is never re-matched by a later rule of the same table. Sequential application
  would feed `pˠ -> fˠ` into `fˠ -> 0` and `pˠ -> bˠ` into `bˠ -> mˠ`. Where two rules of a
  table both match the same span, the earlier rule in file order wins.
- An **inflection** is a short derivation (slenderize the final, then change the vowel, then
  add an ending): its rules apply in file order, each seeing the previous rule's output,
  exactly as any rewrite section does.

Task 19 adds `normalize()`; Task 18 the templates.
"""
from __future__ import annotations

from .dsl import Rule, RuleFile
from .features import FeatureTable
from .rewrite import _replacement, apply_section, find_matches
from .word import TraceEntry, Word

__all__ = ["IrishError", "apply_mutation", "apply_inflection", "MUTATIONS", "INFLECTIONS"]

STAGE = "irish"
MUTATIONS = ("LEN", "ECL", "HPREF", "TPREF")
INFLECTIONS = ("GEN_M1", "GEN_ACH", "GEN_F2", "GEN_M3", "VOC_M1")


class IrishError(Exception):
    """An Irish operation cannot run: the rule file has no sub-table of that name."""


def _subtable(kind: str, tables: dict[str, tuple[Rule, ...]], name: str,
              rf: RuleFile) -> tuple[Rule, ...]:
    try:
        return tables[name]
    except KeyError:
        raise IrishError(f"{rf.path}: no [{kind}] sub-table {name!r} "
                         f"(have: {', '.join(sorted(tables)) or 'none'})") from None


def _apply_table(word: Word, rules: tuple[Rule, ...], rf: RuleFile, table: FeatureTable) -> Word:
    """One simultaneous pass over `word` with every rule of a mutation table (see module
    docstring). Edits are collected against the pre-table word; an edit whose span overlaps
    an already-claimed span is dropped (first rule in file order wins). A zero-width
    (epenthesis) edit at a position inside or at the edge of a claimed span is also dropped,
    so a prothesis rule never fires on a word whose initial was just rewritten. One trace
    entry per rule that contributed, all recording the same before/after pair."""
    claimed: list[tuple[int, int]] = []
    edits: list[tuple[int, int, tuple[str, ...], Rule]] = []
    for rule in rules:
        for start, stop, caps in find_matches(word, rule, rf, table):
            new = _replacement(word, rule, start, stop, caps, table)
            if new == word.segments[start:stop]:
                continue
            if any(start <= b and a <= stop for a, b in claimed):
                continue
            claimed.append((start, stop))
            edits.append((start, stop, new, rule))
    if not edits:
        return word
    before = word.ipa()
    out = word
    for start, stop, new, _ in sorted(edits, key=lambda e: e[0], reverse=True):
        out = out.replaced(start, stop, new)
    after = out.ipa()
    fired = []
    for rule in rules:                       # file order, one entry per contributing rule
        if any(e[3] is rule for e in edits) and rule not in fired:
            fired.append(rule)
    for rule in fired:
        out = out.traced(TraceEntry(stage=STAGE, rule_id=rule.rule_id, tag=rule.tag,
                                    before=before, after=after))
    return out


def apply_mutation(word: Word, name: str, rf: RuleFile, table: FeatureTable) -> Word:
    """name in {'LEN','ECL','HPREF','TPREF'} (digest §3.1–§3.3)."""
    return _apply_table(word, _subtable("mutations", rf.mutations, name, rf), rf, table)


def apply_inflection(word: Word, name: str, rf: RuleFile, table: FeatureTable) -> Word:
    """name in {'GEN_M1','GEN_ACH','GEN_F2','GEN_M3','VOC_M1'} — five, not the four named in
    spec §3; spec §12.J sanctions the superset (digest §3.5)."""
    return apply_section(word, _subtable("inflect", rf.inflect, name, rf), rf, table, STAGE)
