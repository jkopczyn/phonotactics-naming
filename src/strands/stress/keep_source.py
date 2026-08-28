"""`keep-source` stress: keep the incoming (Irish) primary stress; default syllable 0
(plan Task 12; spec §3). Takes no parameters. The syllabifier has already converted the
source's segment-index mark to a syllable index (S1); secondary stress is ignored (I-40).
"""

from __future__ import annotations

from ..dsl import StressSpec
from ..features import FeatureTable
from ..word import Word
from . import register


@register("keep-source")
def keep_source(word: Word, spec: StressSpec, table: FeatureTable) -> int | None:
    if not word.syllables:
        return None
    if word.stress is not None and 0 <= word.stress < len(word.syllables):
        return word.stress
    return 0
