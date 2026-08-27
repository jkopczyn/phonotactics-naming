"""Plan Task 14: the `cairene` stress procedure.

Source: sources/arabic-egy/digest.md §4, worked table at lines 870–886 (17 data rows; R16,
spec §8). Transcribed verbatim — no row paraphrased or dropped.
"""

import pytest
from helpers import TABLE, w

from strands.dsl import parse_rules
from strands.stress import assign_stress
from strands.stress.params import PROCEDURE_PARAMS
from strands.syllabify import syllabify

CAIRENE = (
    "[inventory]\nb t d k ɡ ʔ f s z ʃ x ɣ ħ ʕ h m n l r w j sˤ tˤ dˤ zˤ "
    "a i u aː iː uː eː oː e o æ\n"
    "[syllable]\ntemplate = CN(C)(C)\nonsets = b t d k ɡ ʔ f s z ʃ x ɣ ħ ʕ h m n l r w j "
    "sˤ tˤ dˤ zˤ\ncodas = b t d k ɡ ʔ f s z ʃ x ɣ ħ ʕ h m n l r w j sˤ tˤ dˤ zˤ\n"
    "sonority = off\n[stress]\nprocedure = cairene\n"
)

# digest §4, lines 870–886, all 17 data rows: (plain, stressed)
CAIRENE_STRESS_TABLE = [
    ("katabt", "kaˈtabt"),  # 1, final CVCC
    # digest line 871 (Watson 2011 p.3003 "[ʔaˈbe(h)]"): the source's `e` is a shortened
    # /eː/ (ʔabuːh -> ʔabeː(h)); as transcribed, `beh` is CVC = heavy, not superheavy, so no
    # weight-based procedure can stress it. Strict xfail, never dropped (Task 14 acceptance);
    # see test_abeh_with_its_length_restored for the same row with the underlying /eː/.
    pytest.param(
        "ʔabeh",
        "ʔaˈbeh",
        marks=pytest.mark.xfail(
            strict=True, reason="digest line 871: final `beh` is CVC (heavy); source's e is /eː/"
        ),
    ),  # 1
    ("sakakiːn", "sakaˈkiːn"),  # 1, final CVːC
    ("tˤalabaːt", "tˤalaˈbaːt"),  # 1
    ("ʔabadan", "ˈʔabadan"),  # 2, penult+antepenult light, no pre-antepenult
    ("muxtalifa", "muxˈtalifa"),  # 2, pre-antepenult heavy
    ("katabitu", "kataˈbitu"),  # 3, pre-antepenult also light -> step 2 blocked
    ("jiktibu", "jikˈtibu"),  # 3, heavy antepenult rejects stress
    ("ʕamalti", "ʕaˈmalti"),  # 3
    ("martaba", "marˈtaba"),  # 3, heavy antepenult rejects stress
    ("beːtak", "ˈbeːtak"),  # 3
    ("madrasa", "madˈrasa"),  # 3, the signature Cairene pattern
    ("bintina", "binˈtina"),  # 3, epenthetic penult vowel
    ("katab", "ˈkatab"),  # 3, final CVC is light; two syllables
    ("katabit", "ˈkatabit"),  # 2
    ("katba", "ˈkatba"),  # 3
    ("maktaba", "mækˈtæbæ"),  # 3, heavy antepenult rejects stress
]


def test_the_table_has_seventeen_rows():
    assert len(CAIRENE_STRESS_TABLE) == 17  # R16 / spec §8


@pytest.mark.parametrize("plain,expected", CAIRENE_STRESS_TABLE)
def test_cairene_stress(plain, expected):
    rf = parse_rules(CAIRENE, TABLE)
    got = assign_stress(syllabify(w(plain), rf, TABLE), rf, TABLE)
    # The last row's expected form is the digest's own `mækˈtæbæ` (wiki-egy-phonology's
    # phonetic vowels); the vowel quality is the source's transcription, not a stress fact.
    # For that row compare stress position (and consonants) only, by folding æ -> a.
    assert got.ipa().replace(".", "") == expected.replace("æ", "a")


def test_abeh_with_its_length_restored():
    # digest line 871 with the vowel length Watson's `e` stands for: final CVːC, step 1.
    rf = parse_rules(CAIRENE, TABLE)
    got = assign_stress(syllabify(w("ʔabeːh"), rf, TABLE), rf, TABLE)
    assert got.ipa().replace(".", "") == "ʔaˈbeːh"


def test_heavy_antepenult_rejects_stress():
    rf = parse_rules(CAIRENE, TABLE)
    assert assign_stress(syllabify(w("madrasa"), rf, TABLE), rf, TABLE).stress == 1


def test_epenthetic_vowel_counts_for_stress():
    rf = parse_rules(CAIRENE, TABLE)
    assert assign_stress(syllabify(w("bintina"), rf, TABLE), rf, TABLE).stress == 1


def test_monosyllable():
    rf = parse_rules(CAIRENE, TABLE)
    assert assign_stress(syllabify(w("bint"), rf, TABLE), rf, TABLE).stress == 0


def test_final_cvv_is_superheavy():
    # step 1: a final CVː also takes stress (digest §4 "CVːC, CVː, CVCC").
    rf = parse_rules(CAIRENE, TABLE)
    assert assign_stress(syllabify(w("kataba" + "ː"), rf, TABLE), rf, TABLE).stress == 2


def test_trace_entry_names_the_procedure():
    rf = parse_rules(CAIRENE, TABLE)
    got = assign_stress(syllabify(w("madrasa"), rf, TABLE), rf, TABLE)
    assert got.trace[-1].stage == "stress" and got.trace[-1].rule_id == "stress:cairene"


def test_cairene_takes_no_parameters():
    assert PROCEDURE_PARAMS["cairene"] == frozenset()
