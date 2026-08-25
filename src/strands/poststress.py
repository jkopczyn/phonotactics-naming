"""Post-stress stage: `[post-stress]` rules applied after stress assignment.

Plan Task 16; spec §4.5 ("Stress, then `[post-stress]` rules (length/quality adjustments
that depend on stress)"). The rules are ordinary rewrite lines run in file order, each
seeing the previous rule's output, with the stress mark `ˈ` available as a context atom
(the stressed syllable's START, spec §3).

Re-syllabification. Unlike `[repair]`, this stage re-syllabifies only once, at the end, and
only if some rule changed the segment count: `Word.replaced` shifts the existing syllable
starts and nuclei consistently through every edit, so count-preserving changes leave the
parse valid. When a re-parse is needed the stressed syllable keeps its identity by NUCLEUS,
not by position: the stressed syllable's nucleus is looked up in the edited word, its first
segment is parked in `Word._pending_stress`, and `syllabify()` (S1) re-attaches stress to
whichever new syllable contains that segment. Thus `0 -> i / # _ s k` on `ˈska` yields
`i.ˈska`, not `ˈi.ska`. If the stressed nucleus itself was rewritten (a same-count change
overlapping it drops the nucleus record), the syllable's start segment is used instead.
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
    stop = (word.syllables[word.stress + 1] if word.stress + 1 < len(word.syllables)
            else len(word.segments))
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
    count = len(word.segments)
    out = word
    for rule in rules:
        out = apply_rule(out, rule, rf, table, STAGE)
    if len(out.segments) == count:
        return out
    anchor = _stressed_anchor(out)
    return syllabify(replace(out, _pending_stress=anchor), rf, table)
