"""`cairene` stress (plan Task 14; spec §7, §8).

Source: sources/arabic-egy/digest.md §4 (Watson 2011 (29); McCarthy 1979 (2); Mitchell 1962
via LAPSyD; Broselow 1976; Abdel-Massih), worked table at digest lines 870–886.

1. Stress the final syllable if it is superheavy (CVːC, CVː, CVCC).
2. Else stress the antepenult if the penult and antepenult are both light AND the
   pre-antepenult is not also light (absent or heavy: `ˈʔabadan`, `muxˈtalifa`; all-light
   blocks it: `kataˈbitu`).
3. Else stress the penult. A heavy antepenult therefore rejects stress (`madˈrasa`,
   `jikˈtibu`) — the signature Cairene pattern.

Weight comes from `syllable_weight` (spec §12.B). A final CVː counts as superheavy for step 1
even though `syllable_weight` calls an open long syllable "heavy", because the digest lists
CVː among the stress-attracting finals (word-final CVː is otherwise banned, §4 Length).
Epenthetic vowels count (`binˈtina`) because stress runs after repair — nothing to code here.
No parameters (`params.py`).
"""
from __future__ import annotations

from ..dsl import StressSpec
from ..features import FeatureTable
from ..word import Word
from . import register, syllable_weight


def _final_is_superheavy(word: Word, table: FeatureTable) -> bool:
    last = len(word.syllables) - 1
    if syllable_weight(word, last, table) == "superheavy":
        return True
    # Final CVː: open syllable with a long nucleus.
    start = word.syllables[last]
    nucleus = next(((a, b) for a, b in word.nuclei if a >= start), None)
    if nucleus is None:
        return False
    a, b = nucleus
    return b == len(word.segments) and any(
        table.value(s, "long") == "+" for s in word.segments[a:b])


@register("cairene")
def cairene(word: Word, spec: StressSpec, table: FeatureTable) -> int | None:
    n = len(word.syllables)
    if n == 0:
        return None
    if n == 1:
        return 0
    if _final_is_superheavy(word, table):                       # step 1
        return n - 1
    penult, antepenult = n - 2, n - 3
    if antepenult >= 0:                                          # step 2
        light = lambda i: syllable_weight(word, i, table) == "light"
        if light(penult) and light(antepenult):
            pre = antepenult - 1
            if pre < 0 or not light(pre):
                return antepenult
    return penult                                                # step 3
