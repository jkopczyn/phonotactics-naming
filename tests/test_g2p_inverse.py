"""Tasks 1-2: the reverse g2p (reverse spec §3.4; V-27, V-19, V-20, V-21)."""
import pytest

from strands import g2p as fwd
from strands.g2p_inverse import (BROAD_ON_THE_RIGHT, CONSONANT_READINGS, QUALITY_LEFT,
                                 QUALITY_RIGHT, READINGS, VOWEL_READINGS, describe,
                                 readings_for)


def spellings(segments):
    return tuple(r.grapheme for r in readings_for(segments))


def test_the_forward_tables_are_public_and_are_the_same_objects():
    """spec §5: the tables become module-level and documented as shared."""
    assert fwd.CONSONANTS is fwd._CONSONANTS and fwd.VOWELS is fwd._VOWELS
    assert "CONSONANTS" in fwd.__all__ and "VOWELS" in fwd.__all__


def test_every_reading_names_the_g2p_branch_it_transcribes():
    """V-27: the registry is a transcription of g2p, and must say of what."""
    assert READINGS and all(r.source for r in READINGS)


# ---- the table branches -------------------------------------------------------------------------

@pytest.mark.parametrize("segment,expected", [
    ("w", ("bh", "mh", "v", "w")),
    ("x", ("ch",)), ("ç", ("ch",)),
    ("k", ("c", "k")),
])
def test_the_table_readings_are_registered(segment, expected):
    assert set(expected) <= set(spellings((segment,)))


def test_the_eclipsis_digraphs_are_initial_only():
    got = [r for r in readings_for(("mˠ",)) if r.grapheme == "mb"]
    assert got and all(r.position == "initial" for r in got)


# ---- the PROCEDURAL branches (F1) — draft 1 had none of these ------------------------------------

@pytest.mark.parametrize("segment,grapheme", [
    ("l̪ˠ", "l"), ("l̠ʲ", "l"), ("lˠ", "l"), ("lʲ", "l"),
    ("n̪ˠ", "n"), ("n̠ʲ", "n"), ("nˠ", "n"), ("nʲ", "n"),
])
def test_single_l_and_n_read_as_both_fortis_and_lenis(segment, grapheme):
    """_liquid: draft 1 had only the doubled ⟨ll nn⟩ from _CONSONANTS."""
    assert grapheme in spellings((segment,))


def test_single_r_reads_as_the_broad_rhotic_in_both_qualities():
    """_rhotic: slender ⟨r⟩ is /ɾˠ/ initially, after ⟨s⟩ and before a coronal."""
    assert "r" in spellings(("ɾˠ",)) and "r" in spellings(("ɾʲ",))


def test_single_s_reads_as_both_sibilants():
    """_sibilant: slender ⟨s⟩ is /sˠ/ before f m p r, /ʃ/ otherwise."""
    assert "s" in spellings(("sˠ",)) and "s" in spellings(("ʃ",))


@pytest.mark.parametrize("segment,grapheme", [("j", "dh"), ("j", "gh"), ("ɣ", "dh"),
                                              ("h", "sh"), ("ç", "sh"), ("h", "th")])
def test_the_lenition_digraphs_are_registered(segment, grapheme):
    assert grapheme in spellings((segment,))


def test_the_silent_readings_exist():
    """broad ⟨dh gh⟩ noninitially, ⟨th⟩ word-finally after a long vowel, ⟨fh⟩."""
    silent = {r.grapheme for r in READINGS if r.segments == ()}
    assert {"dh", "gh", "th", "fh"} <= silent


@pytest.mark.parametrize("segments,grapheme", [(("ŋ", "ɡ"), "ng"), (("ɲ", "ɟ"), "ng"),
                                               (("ŋ", "k"), "nc"), (("k", "s"), "x")])
def test_the_two_segment_readings_are_registered_as_units(segments, grapheme):
    assert grapheme in spellings(segments)


def test_noninitial_w_also_reads_as_the_connacht_allophone():
    """V-27, the row that makes `ardmhaor` spellable: _word_segments turns a noninitial
    /w/ into /vˠ/ for dialect C, so ⟨bh mh v w⟩ all read as /vˠ/ off the word edge."""
    got = readings_for(("vˠ",))
    assert {"bh", "mh", "v", "w"} <= {r.grapheme for r in got}
    assert all(r.position == "noninitial" for r in got)


# ---- vowels ---------------------------------------------------------------------------------------

# The plan's parametrization wrote the diphthong nuclei as single segments (`("əu",)`,
# `("iə",)`); `g2p._split_nucleus` splits a diphthong into two segments (I-2), so the real
# keys are `("ə", "u")` and `("i", "ə")`. Same runs, same intent.
@pytest.mark.parametrize("nucleus,run", [(("aː",), "á"), (("iː",), "ao"), (("iː",), "aoi"),
                                         (("i", "ə"), "ia"), (("ə", "u"), "abh"),
                                         (("eː",), "ae")])
def test_the_vowel_runs_that_read_as_a_nucleus(nucleus, run):
    assert run in VOWEL_READINGS[nucleus]


def test_an_override_value_is_inverted_too_without_checking_its_condition():
    """V-27: `a` -> `aː` before ⟨rd⟩ is an override; the inverse over-generates."""
    assert "a" in VOWEL_READINGS[("aː",)]


def test_every_short_vowel_run_also_reads_as_schwa():
    """_word_segments pass 2: an unstressed short monophthong reduces."""
    assert {"a", "e", "i", "o", "u"} <= set(VOWEL_READINGS[("ə",)])


def test_caol_le_caol_is_read_off_the_letters_with_the_ae_ao_exception():
    assert QUALITY_LEFT["ia"] == "slender" and QUALITY_RIGHT["ia"] == "broad"
    assert QUALITY_LEFT["á"] == "broad" and QUALITY_RIGHT["á"] == "broad"
    assert QUALITY_LEFT["ei"] == "slender" and QUALITY_RIGHT["ei"] == "slender"
    for run in BROAD_ON_THE_RIGHT:
        assert QUALITY_RIGHT[run] == "broad", run


# ---- describe -------------------------------------------------------------------------------------

def test_describe_prefixes_the_quality_when_every_reading_agrees():
    assert describe(("vʲ",)).startswith("slender ")
    assert describe(("aː",)).startswith("á")
    assert describe(()) == "inserted, no Irish letter"
    assert describe(("ʡ",)) == "/ʡ/"


def test_describe_is_stable_across_calls():
    assert describe(("w",)) == describe(("w",))


def test_the_indexes_are_deterministic_tuples():
    for value in list(CONSONANT_READINGS.values()) + list(VOWEL_READINGS.values()):
        assert isinstance(value, tuple)


# ---- Task 2: spell(), the run matcher and the ratchet (V-20) -------------------------------------

import json
import unicodedata

from helpers import ROOT, TABLE, read_test_words
from strands.g2p import g2p
from strands.g2p_inverse import spell
from strands.tokenize import tokenize

RATCHET = ROOT / "tests" / "ratchets" / "g2p_inverse.json"


def segs(ipa):
    for mark in ("ˈ", "ˌ", "."):
        ipa = ipa.replace(mark, "")
    return tuple(tokenize(ipa, TABLE).segments)


@pytest.mark.parametrize("orth", ["mac", "bán", "ceist", "cáis", "fíon", "dorn", "teach",
                                  "sean", "bean", "Colm", "gorm", "ardmhaor"])
def test_spelling_a_words_own_ipa_recovers_the_word(orth):
    """F1: `dorn` needs single ⟨r n⟩, `sean` single ⟨s⟩, `gorm` the epenthetic schwa with no
    letter, `ardmhaor` the noninitial /w/ -> /vˠ/ post-pass. Draft 1 recovered none of them."""
    assert orth.casefold() in [c.casefold() for c in spell(segs(g2p(orth)[0]))]


def test_the_session_case_word_is_spellable():
    """spec §6 bullet 4: `ardmhaor` is the example the whole Ar*v* case turns on."""
    assert "ardmhaor" in spell(segs(g2p("ardmhaor")[0]), limit=200)


def test_every_proposal_reads_back_to_the_intended_ipa():
    """spec §3.4 last sentence: nothing leaves `spell` unverified."""
    want = segs(g2p("bán")[0])
    for cand in spell(want):
        assert segs(g2p(cand)[0]) == want


def test_caol_le_caol_rules_out_the_mismatched_vowel_letters():
    out = spell(segs(g2p("Seán")[0]))
    assert out and all(not c.startswith("sa") for c in out)


def test_a_two_segment_reading_is_matched_as_a_unit():
    """⟨ng⟩ is /ŋɡ/: the run matcher must consume both segments at once."""
    assert "long" in [c.casefold() for c in spell(segs(g2p("long")[0]))]


def test_an_unknown_nucleus_is_unspellable_not_a_crash():
    assert spell(("ʡ",)) == []


def test_a_consonant_only_candidate_does_not_raise():
    assert spell(("k",)) == []          # g2p raises G2PError; spell drops it


@pytest.mark.parametrize("limit", [0, -1])
def test_a_non_positive_limit_asks_for_nothing(limit):
    """V-20 step 5: `limit` caps the kept spellings, so a cap of 0 keeps none."""
    assert spell(segs(g2p("mac")[0]), limit=limit) == []
    assert spell(("a",), limit=limit) == []


def test_a_long_consonant_run_is_still_enumerated_in_full():
    """The run matcher terminates on its own; no internal cap may drop ordinary spellings."""
    assert "akkkkkkka" in spell(segs(g2p("akkkkkkka")[0]), limit=1000)


def test_the_result_is_capped_and_order_is_stable():
    a = spell(segs(g2p("mac")[0]), limit=3)
    assert len(a) <= 3 and a == spell(segs(g2p("mac")[0]), limit=3)


# ---- the ratchet (spec §6 bullet 2) ----------------------------------------------------------

def hand_ipa_rows():
    return [r for r in read_test_words() if (r.get("ipa") or "").strip()]


def contains_rate():
    rows, hit, misses = hand_ipa_rows(), 0, []
    for row in rows:
        want = unicodedata.normalize("NFC", row["orthography"]).casefold()
        try:
            got = [unicodedata.normalize("NFC", c).casefold() for c in spell(segs(row["ipa"]))]
        except Exception:
            got = []
        if want in got:
            hit += 1
        else:
            misses.append((row["orthography"], row["ipa"]))
    return hit / len(rows), misses


def test_the_contains_rate_does_not_fall():
    rate, misses = contains_rate()
    ratchet = json.loads(RATCHET.read_text(encoding="utf-8"))
    assert rate >= ratchet["contains"] - 1e-9, (
        f"contains {rate:.4f} < ratchet {ratchet['contains']}\n"
        + "\n".join(f"  {o}\t{i}" for o, i in misses[:20]))


def test_the_ratchet_records_its_denominator():
    data = json.loads(RATCHET.read_text(encoding="utf-8"))
    assert set(data) == {"contains", "n"} and data["n"] == len(hand_ipa_rows())
