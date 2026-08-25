"""Substitute stage: the target's `[substitute]` section applied in file order.

Plan Task 8; spec §4.2a. Each rule sees the previous rule's output (`apply_section`), and every
change records a trace entry with `stage="substitute"`. A rule file without a `[substitute]`
section leaves the word untouched.
"""
from __future__ import annotations

from .dsl import RuleFile
from .features import FeatureTable
from .rewrite import apply_section
from .word import Word

__all__ = ["substitute"]

STAGE = "substitute"


def substitute(word: Word, rf: RuleFile, table: FeatureTable) -> Word:
    """Apply `rf.sections["substitute"]` in file order (spec §4.2a)."""
    rules = rf.sections.get(STAGE, ())
    if not rules:
        return word
    return apply_section(word, rules, rf, table, STAGE)
