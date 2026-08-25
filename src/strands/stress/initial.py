"""`initial` stress: syllable 0 (plan Task 12; spec §3, §7 Georgian).

Parameter `mark = on|off` (default `on`; see `params.py`). `off` means the respell stage
prints no stress mark (Georgian, digest §4.3) — the stress index is still set so that the
post-stress stage can see it.
"""
from __future__ import annotations

from ..dsl import StressSpec
from ..features import FeatureTable
from ..word import Word
from . import register


@register("initial")
def initial(word: Word, spec: StressSpec, table: FeatureTable) -> int | None:
    return 0 if word.syllables else None
