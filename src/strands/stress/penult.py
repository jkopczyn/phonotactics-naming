"""`penult` stress: the penultimate syllable of a polysyllable, the only syllable of a
monosyllable (plan Task 13; spec §3; sources/welsh/digest.md §4.1 [liu2018 p.6;
williams1983 p.22; breit2019 pp.74–75 "regardless of length or diachronic origin"]).

No parameters (`params.py`). Weight is ignored. Stress is recomputed from the syllable
count every time — never carried from the source and never from an earlier run — so that
affixation (an epithet suffix, an Irish inflection) shifts it rightward as in *ysgrif* →
*ysgrifen* → *ysgrifennydd* [breit2019 p.74].
"""

from __future__ import annotations

from ..dsl import StressSpec
from ..features import FeatureTable
from ..word import Word
from . import register


@register("penult")
def penult(word: Word, spec: StressSpec, table: FeatureTable) -> int | None:
    n = len(word.syllables)
    if n == 0:
        return None
    return max(n - 2, 0)
