"""Task 1 (Old Irish plan): the lenited series in features.csv (digest §10.1; O-1, O-2, R26)."""

import csv

import pytest
from helpers import ROOT

from strands.features import FEATURE_NAMES, load_features
from strands.tokenize import tokenize


def rows():
    with (ROOT / "rules" / "features.csv").open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


TABLE = load_features(ROOT / "rules" / "features.csv")
OLD_IRISH_ROWS = ("β", "βʲ", "β̃", "β̃ʲ", "θʲ", "ðʲ", "ɣʲ")


@pytest.mark.parametrize("segment", OLD_IRISH_ROWS)
def test_old_irish_lenited_rows_exist_and_tokenize(segment):
    """digest §10.1: the lenited series. O-1 spells spec §4's /μ/ as β̃."""
    assert segment in TABLE.segments
    assert tuple(tokenize(segment, TABLE).segments) == (segment,)


def test_old_irish_rows_are_hand_consonants():
    by = {r["segment"]: r for r in rows()}
    for s in OLD_IRISH_ROWS:
        assert (by[s]["class"], by[s]["source"]) == ("C", "hand:old-irish"), s


def test_beta_is_a_voiced_bilabial_fricative_not_labiodental():
    assert TABLE.value("β", "continuant") == "+"
    assert TABLE.value("β", "sonorant") == "-"
    assert TABLE.value("β", "labiodental") == "-"
    assert TABLE.value("β", "labial") == "+"
    assert TABLE.value("β", "round") == "-"
    assert TABLE.value("β", "periodicGlottalSource") == "+"


def test_the_nasalized_fricative_differs_from_beta_only_in_nasality():
    """digest §10.8 conflict 3: /ṽ/ ~ /β̃/ ~ [w̃] are one bilabial nasalized continuant."""
    assert [f for f in FEATURE_NAMES if TABLE.value("β", f) != TABLE.value("β̃", f)] == ["nasal"]
    assert [f for f in FEATURE_NAMES if TABLE.value("βʲ", f) != TABLE.value("β̃ʲ", f)] == ["nasal"]


@pytest.mark.parametrize(
    "broad,slender", [("β", "βʲ"), ("β̃", "β̃ʲ"), ("θ", "θʲ"), ("ð", "ðʲ"), ("ɣ", "ɣʲ"), ("x", "ç")]
)
def test_slender_partners_differ_only_in_the_I41_quality_features(broad, slender):
    """R26: the x/ç and ɣ/ɣʲ pairs are INCLUDED — draft 1 omitted them because `j` failed."""
    diff = {f for f in FEATURE_NAMES if TABLE.value(broad, f) != TABLE.value(slender, f)}
    assert diff and diff <= {"front", "back", "high"}, diff
    assert (TABLE.value(slender, "front"), TABLE.value(slender, "back")) == ("+", "-")


def test_j_is_not_the_slender_partner_of_gamma():
    """R26: `j` is a glide (sonorant +, consonantal −), not the fricative /ɣʲ/."""
    assert TABLE.value("j", "sonorant") == "+" and TABLE.value("ɣʲ", "sonorant") == "-"


def test_no_fortis_sonorant_rows_were_added():
    """O-2: fortis is a doubled GRAPHEME (Task 7), not a segment."""
    for bad in ("L", "N", "R", "ʟ", "ɴ", "ʀ"):
        assert bad not in TABLE.segments
