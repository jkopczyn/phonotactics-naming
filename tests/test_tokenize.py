"""Task 3: longest-match tokenizer, marks (I-40), attested-data cleaning (I-36)."""

import csv
import pathlib
import unicodedata

import pytest

from strands.features import load_features
from strands.tokenize import SegmentError, clean_attested, detokenize, tokenize

ROOT = pathlib.Path(__file__).parents[1]
TABLE = load_features(ROOT / "rules" / "features.tsv")


def test_longest_match_prefers_diacritic_segments():
    assert tokenize("t̪ˠaː", TABLE).segments == ("t̪ˠ", "aː")


def test_lasairchos():
    t = tokenize("ˈl̪ˠɑsˠəɾʲxosˠ", TABLE)
    assert t.segments == ("l̪ˠ", "ɑ", "sˠ", "ə", "ɾʲ", "x", "o", "sˠ")
    assert t.stress_index == 0


def test_diphthong_is_two_segments():
    assert tokenize("ˈciəɾˠə", TABLE).segments == ("c", "i", "ə", "ɾˠ", "ə")  # I-2


def test_syllable_dots_recorded_and_removed():
    t = tokenize("ˈkɪə.ɾˠə", TABLE)
    assert "." not in t.segments and t.syllable_starts == (0, 3) and t.stress_index == 0


def test_secondary_stress_is_recorded():
    t = tokenize("ˈaːɾˠd̪ˠˌn̪ˠõːsəx", TABLE)  # ardnósach, test-words row
    assert t.stress_index == 0 and t.secondary == (3,)


def test_ascii_g_tokenizes_as_its_own_segment():
    assert tokenize("gl̪ˠuːnʲ", TABLE).segments[0] == "g"  # I-34, glúin


def test_space_splits_words():
    t = tokenize("mˠaːɾʲə wɑːnˠ", TABLE)
    assert " " not in t.segments and len(t.words) == 2


def test_morpheme_positions():
    assert tokenize("a$vʲ", TABLE).morphemes == frozenset({1})


def test_unknown_segment_raises_with_the_offending_substring():
    with pytest.raises(SegmentError) as e:
        tokenize("kQa", TABLE)
    assert "Q" in str(e.value)


def test_detokenize_round_trips():
    assert detokenize(tokenize("mˠat̪ˠaːnˠəx", TABLE).segments) == "mˠat̪ˠaːnˠəx"


def test_nfc_is_applied():
    s = "aː"
    assert tokenize(s, TABLE).segments == tokenize(unicodedata.normalize("NFD", s), TABLE).segments


def test_clean_attested_strips_wrappers_and_maps_ascii():
    assert clean_attested("[kalb]", "arabic-egy") == "kalb"
    assert clean_attested("/ka:lb/", "dutch") == "kaːlb"
    assert clean_attested("gogo", "georgian") == "ɡoɡo"


def test_apostrophe_is_an_ejective_mark_only_for_georgian():
    """I-36: in the Dutch data ' is a stress mark, not an ejective (fix 10)."""
    assert clean_attested("t'ma", "georgian") == "tʼma"
    assert clean_attested("'kanto", "dutch") == "kanto"


def test_clean_attested_is_not_applied_to_user_input():
    """I-36/I-34: ASCII g is canonical in test-words.tsv and must survive tokenize()."""
    assert tokenize("gl̪ˠuːnʲ", TABLE).segments[0] == "g"


def test_all_144_test_word_rows_tokenize():
    with (ROOT / "sources" / "irish" / "test-words.tsv").open(encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh, delimiter="\t"))
    assert len(rows) == 144
    for r in rows:
        tokenize(r["ipa"], TABLE)  # must not raise
