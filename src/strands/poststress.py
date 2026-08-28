"""Post-stress stage: `[post-stress]` rules applied after stress assignment.

Plan Task 16; spec §4.5 ("Stress, then `[post-stress]` rules (length/quality adjustments
that depend on stress)"). The rules are ordinary rewrite lines run in file order, each
seeing the previous rule's output, with the stress mark `ˈ` available as a context atom
(the stressed syllable's START, spec §3).

Re-syllabification. Unlike `[repair]`, this stage re-syllabifies only once, at the end, and
only if some rule changed the segment count (checked rule by rule: an insertion followed by a
deletion nets to zero but still invalidates the parse). `Word.replaced` shifts the existing
syllable starts and nuclei consistently through every edit, so count-preserving changes leave
the parse valid. The stressed syllable keeps its identity by NUCLEUS, not by position: before
any rule runs, the stressed syllable's nucleus start in the PRE-edit word is parked in
`Word._pending_stress`, which `replaced` shifts through every edit exactly as it does the
tokenizer's stress index (S1), and `syllabify()` re-attaches stress to whichever new syllable
contains that segment. Thus `0 -> i / # _ s k` on `ˈska` yields `i.ˈska`, not `ˈi.ska`, and
`p -> 0 / # _` on `ˈpat` yields `ˈat` even though the syllable START was deleted (which
drops `Word.stress`). If the nucleus itself is rewritten the parked index is lost; the
stressed syllable's start in the edited word is used instead, when it survived.
"""

from __future__ import annotations

from dataclasses import replace

from .dsl import RuleFile
from .features import FeatureTable
from .rewrite import apply_rule
from .syllabify import syllabify
from .word import Word

__all__ = ["STAGE", "post_stress"]

STAGE = "post-stress"


def _stressed_anchor(word: Word) -> int | None:
    """Segment index identifying the stressed syllable: its nucleus start if the nucleus
    record survived the edits, else its syllable start; None when unstressed."""
    if word.stress is None or not (0 <= word.stress < len(word.syllables)):
        return None
    start = word.syllables[word.stress]
    stop = (
        word.syllables[word.stress + 1]
        if word.stress + 1 < len(word.syllables)
        else len(word.segments)
    )
    for a, _ in word.nuclei:
        if start <= a < stop:
            return a
    return start


def post_stress(word: Word, rf: RuleFile, table: FeatureTable) -> Word:
    """Spec §4.5: apply rf.sections['post-stress'] in file order after assign_stress;
    re-syllabify at the end if any rule changed the segment count, preserving the
    stressed syllable's identity."""
    rules = rf.sections.get(STAGE, ())
    if not rules:
        return word
    anchor = _stressed_anchor(word)  # identity of the stressed syllable, pre-edit
    out = word if anchor is None else replace(word, _pending_stress=anchor)
    changed = False
    for rule in rules:
        count = len(out.segments)
        out = apply_rule(out, rule, rf, table, STAGE)
        changed = changed or len(out.segments) != count
    if not changed:
        return out if anchor is None else replace(out, _pending_stress=word._pending_stress)
    if out._pending_stress is None:  # nucleus rewritten: fall back to the start
        out = replace(out, _pending_stress=_stressed_anchor(out))
    return syllabify(out, rf, table)
