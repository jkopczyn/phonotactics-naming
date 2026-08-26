"""`dutch-weight` stress (plan Task 15; sources/dutch/digest.md §4 "The practical rule",
lines 671–687 — CONSTRUCTED BY THE DIGEST, not stated by any source, hence `%design` in
dutch.rules). Six ordered steps:

1. a syllable containing schwa is unstressable; prefer the syllable immediately before it;
2. final syllable superheavy (A-vowel/diphthong + C(+coronals), or B-vowel + CC) or ending
   in a diphthong -> stress the final;
3. else penult closed with a full vowel -> stress the penult (never skip it);
4. else final syllable closed and B-class (lax) -> stress the antepenult (weak);
5. else -> stress the penult;
6. never stress outside the last `window` syllables (param `window`, default 3).

Readings the digest leaves open (kept as simple as possible):
- A-class (tense) = `tense=+` or `long=+`; everything else is B-class (lax). `ɑ` has
  `tense=0` in features.tsv and so falls to B-class, which is what the digest says of it.
- "Schwa" is the segment `ə` itself (spec I-1: NFC; no other reduced vowel is in play).
- A diphthong is a branching nucleus (spec §12.B) — the `[syllable] nuclei =` list decides.
- Step 1 uses the RIGHTMOST schwa syllable that has a non-schwa syllable before it, and
  stresses the nearest non-schwa syllable to its left. A schwa in syllable 0 with nothing
  before it is simply skipped by the later steps.
- Steps 3–5 need a penult/antepenult; a monosyllable stresses its only syllable and a
  disyllable's step 4 (no antepenult) falls to step 5.
- Step 6 clamps the result rightwards into the window, and step 1's ban on stressing
  schwa is enforced at every candidate: a schwa syllable is never returned while the
  word has a non-schwa one (see `_clamp`).
"""
from __future__ import annotations

from ..dsl import StressSpec
from ..features import FeatureTable
from ..word import Word
from . import register

SCHWA = "ə"
DEFAULT_WINDOW = 3


def _span(word: Word, i: int) -> tuple[int, int]:
    start = word.syllables[i]
    stop = word.syllables[i + 1] if i + 1 < len(word.syllables) else len(word.segments)
    return start, stop


def _nucleus(word: Word, i: int) -> tuple[int, int] | None:
    start, stop = _span(word, i)
    return next(((a, b) for a, b in word.nuclei if start <= a < stop), None)


def _has_schwa(word: Word, i: int) -> bool:
    nuc = _nucleus(word, i)
    return nuc is not None and any(s == SCHWA for s in word.segments[nuc[0]:nuc[1]])


def _is_a_class(word: Word, i: int, table: FeatureTable) -> bool:
    nuc = _nucleus(word, i)
    if nuc is None:
        return False
    return any(table.value(s, "tense") == "+" or table.value(s, "long") == "+"
               for s in word.segments[nuc[0]:nuc[1]])


def _is_diphthong(word: Word, i: int) -> bool:
    nuc = _nucleus(word, i)
    return nuc is not None and nuc[1] - nuc[0] >= 2


def _coda_count(word: Word, i: int) -> int:
    nuc = _nucleus(word, i)
    if nuc is None:
        return 0
    return _span(word, i)[1] - nuc[1]


def _superheavy(word: Word, i: int, table: FeatureTable) -> bool:
    """Dutch superheavy: (A-vowel | diphthong) + >=1 C, or B-vowel + >=2 C."""
    coda = _coda_count(word, i)
    if _is_a_class(word, i, table) or _is_diphthong(word, i):
        return coda >= 1
    return coda >= 2


@register("dutch-weight")
def dutch_weight(word: Word, spec: StressSpec, table: FeatureTable) -> int | None:
    n = len(word.syllables)
    if n == 0:
        return None
    window = int(spec.params.get("window", DEFAULT_WINDOW))
    lo = max(0, n - window)
    final, penult, antepenult = n - 1, n - 2, n - 3

    # step 1: schwa
    for s in range(n - 1, 0, -1):
        if _has_schwa(word, s):
            for t in range(s - 1, -1, -1):
                if not _has_schwa(word, t):
                    return _clamp(word, t, lo)
    # step 2: superheavy or diphthong-final
    if _superheavy(word, final, table) or _is_diphthong(word, final):
        return _clamp(word, final, lo)
    if n == 1:
        return 0
    # step 3: closed penult with a full vowel
    if _coda_count(word, penult) >= 1 and not _has_schwa(word, penult):
        return penult
    # step 4: closed lax final -> antepenult
    if n >= 3 and _coda_count(word, final) >= 1 and not _is_a_class(word, final, table) \
            and not _has_schwa(word, antepenult):
        return _clamp(word, antepenult, lo)
    # step 5: default penult
    return _clamp(word, penult, lo)


def _clamp(word: Word, i: int, lo: int) -> int:
    """Step 6 plus step 1's standing ban: move a too-far-left result rightwards into the
    window, and never return a schwa syllable.

    Step 1 only triggers on a schwa syllable at index >= 1, so a WORD-INITIAL schwa reaches
    steps 2-5 and can be chosen there (*an bhean* /ənvjɑn/: the schwa is the penult, and
    step 5 took it). Dutch never stresses schwa, so the candidate moves to the nearest
    non-schwa syllable — leftwards first, as step 1 prefers the syllable before the schwa,
    then rightwards. A word with no non-schwa syllable at all keeps the candidate; there is
    nowhere to move it to and every word needs exactly one stress."""
    if i < lo:
        i = lo
    if not _has_schwa(word, i):
        return i
    for t in range(i - 1, lo - 1, -1):
        if not _has_schwa(word, t):
            return t
    for t in range(i + 1, len(word.syllables)):
        if not _has_schwa(word, t):
            return t
    for t in range(lo - 1, -1, -1):
        if not _has_schwa(word, t):
            return t
    return i
