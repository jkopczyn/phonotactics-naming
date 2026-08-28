"""Substitute stage: the target's `[substitute]` section, then the inventory fallback.

Plan Tasks 8–9; spec §4.2a–b. `substitute()` applies the section in file order: each rule sees
the previous rule's output (`apply_section`), and every change records a trace entry with
`stage="substitute"`. A rule file without a `[substitute]` section leaves the word untouched.

`fallback()` then replaces every segment still outside `rf.inventory` by the nearest
NON-MARGINAL inventory segment under the file's weighted feature distance (I-12; ties break by
`[inventory]` declaration order). Marginal segments already in the word stay (I-23: legal in
output, never chosen). This is the ONLY approximating step in the engine (I-4): feature-change
bundles inside rules resolve by exact lookup. One trace entry per replaced segment, with
`stage="fallback"`, `rule_id="fallback"`, `tag="fallback"`, so `Word.fallback_count()` counts
them. `substitute_stage()` is the two in sequence.
"""

from __future__ import annotations

from .dsl import RuleFile
from .features import FeatureTable
from .rewrite import apply_section
from .word import TraceEntry, Word

__all__ = ["substitute", "fallback", "substitute_stage"]

STAGE = "substitute"
FALLBACK = "fallback"


def substitute(word: Word, rf: RuleFile, table: FeatureTable) -> Word:
    """Apply `rf.sections["substitute"]` in file order (spec §4.2a)."""
    rules = rf.sections.get(STAGE, ())
    if not rules:
        return word
    return apply_section(word, rules, rf, table, STAGE)


def fallback(word: Word, rf: RuleFile, table: FeatureTable) -> Word:
    """Spec §4.2b: each segment not in rf.inventory becomes the nearest NON-MARGINAL
    inventory segment by weighted distance (I-12); one TraceEntry per replacement,
    tag='fallback', rule_id='fallback'. This is the ONLY approximating step (I-4)."""
    allowed = set(rf.inventory)
    candidates = tuple(s for s in rf.inventory if s not in rf.marginal)
    out = word
    for i, seg in enumerate(word.segments):
        if seg in allowed:
            continue
        new = table.nearest(seg, candidates, rf.weights)
        before = out.ipa()
        out = out.replaced(i, i + 1, (new,))
        out = out.traced(
            TraceEntry(
                stage=FALLBACK,
                rule_id=FALLBACK,
                tag=FALLBACK,
                before=before,
                after=out.ipa(),
                note=f"{seg} -> {new}",
            )
        )
    return out


def substitute_stage(word: Word, rf: RuleFile, table: FeatureTable) -> Word:
    """Spec §4.2: `[substitute]` rules, then the inventory fallback."""
    return fallback(substitute(word, rf, table), rf, table)
