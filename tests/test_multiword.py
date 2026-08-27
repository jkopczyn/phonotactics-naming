"""Multi-word inputs (spec §3 `[templates]`: "Words separated by " " are adapted separately
by the target and joined in the output"), plus the /ɪə/ transcription variant of the /iə/
diphthong (digest §1.2).

A multi-word Irish input (*Ní Bhriain* /nʲiː vʲɾʲiənʲ/, *an tsúil* /ən̪ˠ t̪ˠuːlʲ/) must stay
several words through the Irish pre-pass, so that each word runs through the target's stages
2-7 on its own — its own syllabification, stress and word-edge rules — and the respelling and
IPA join with a single space.
"""
import pytest

from helpers import TABLE, irish, read_test_words
from strands.inputs import Entry, infer
from strands.pipeline import TARGETS, load_target, run_entry

IRISH = irish()
RF = {name: load_target(name, TABLE) for name in TARGETS}

# The test-words rows whose `ipa` column holds more than one word.
MULTI = [row for row in read_test_words() if " " in row["ipa"].strip()]

_ROW_STRANDS = [
    pytest.param(row, name, id=f"{row['orthography']}-{name}")
    for row in MULTI for name in TARGETS]


def _run(ipa: str, strand: str):
    entry = infer(Entry(orthography=ipa, ipa=ipa), IRISH, TABLE)
    return run_entry(entry, "DESC", IRISH, RF[strand], TABLE)


def test_the_test_words_file_still_has_multi_word_rows():
    assert len(MULTI) >= 8


def test_ni_bhriain_stays_two_words_in_cairene():
    r = _run("nʲiː vʲɾʲiənʲ", "arabic-egy")
    assert len(r.words) == 2
    assert len(r.respelling.split()) == 2
    assert len(r.ipa.split()) == 2


def test_ni_bhriain_first_word_long_vowel_is_not_shortened_by_the_next_word():
    """/nʲiː/ is an open syllable of its own; only the merged parse made it a closed
    `nif.` and shortened it."""
    r = _run("nʲiː vʲɾʲiənʲ", "arabic-egy")
    assert "iː" in r.words[0].segments
    assert r.respelling.split()[0] == "nii"


def test_each_word_gets_its_own_cairene_glottal_onset():
    """Cairene puts ʔ before a vowel-initial word — before EACH one (spec §4.3)."""
    r = _run("ə bʲaːn̪ˠ", "arabic-egy")
    assert len(r.words) == 2
    assert r.words[0].segments[0] == "ʔ"


def test_an_tsuil_stays_two_words_in_georgian():
    r = _run("ən̪ˠ t̪ˠuːlʲ", "georgian")
    assert len(r.words) == 2
    assert len(r.respelling.split()) == 2
    assert r.respelling.split()[0] == "an"


@pytest.mark.parametrize("row,strand", _ROW_STRANDS)
def test_word_count_is_preserved_for_every_multi_word_row(row, strand):
    ipa = row["ipa"].strip()
    r = _run(ipa, strand)
    n = len(ipa.split())
    assert len(r.words) == n
    assert len(r.respelling.split()) == n
    assert len(r.ipa.split()) == n


@pytest.mark.parametrize("strand", TARGETS)
def test_single_word_input_is_still_one_word(strand):
    r = _run("ˈmˠaːɾʲə", strand)
    assert len(r.words) == 1
    assert " " not in r.respelling
    assert " " not in r.ipa
