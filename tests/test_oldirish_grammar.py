"""Tasks 13-15: Old Irish mutations, inflection and templates as GRAPHEME operations
(spec §5, §11; digest §10.4-§10.5)."""

import pytest
from helpers import irish, target

from strands.lexicon import read_lexicon
from strands.oldirish import apply_oi_mutation
from strands.spelled import SpelledWord, spelling_to_ipa

IRISH = irish()
OI = target("old-irish")
LEX = read_lexicon()


def mut(text, name):
    return apply_oi_mutation(SpelledWord.from_spelling(text), name, OI)


@pytest.mark.parametrize(
    "radical,lenited",
    [("tech", "thech"), ("cenn", "chenn"), ("penn", "phenn"), ("son", "ṡon"), ("fer", "ḟer")],
)
def test_lenition_writes_the_voiceless_stops_and_the_punctum_forms(radical, lenited):
    """digest §10.4 contrast set; R24: ⟨ḟ⟩ is now reachable because it is a TOKEN."""
    assert mut(radical, "LEN").render() == lenited


@pytest.mark.parametrize("radical", ["bo", "duine", "gel", "mac"])
def test_lenition_of_b_d_g_m_changes_the_ipa_and_not_the_spelling(radical):
    """digest §10.2 conv. 1 — the metadata channel is the whole point (R20: draft 1's
    segment-level version rewrote *mac* to *mag*)."""
    out = mut(radical, "LEN")
    assert out.render() == radical and out.mutation == "LEN"
    assert spelling_to_ipa(out) != spelling_to_ipa(SpelledWord.from_spelling(radical))


def test_lenited_f_is_silent_in_the_reconstruction():
    assert spelling_to_ipa(mut("fer", "LEN")) == ("e", "ɾˠ")


@pytest.mark.parametrize(
    "radical,nasalized", [("bo", "mbo"), ("duine", "nduine"), ("gel", "ngel"), ("ech", "n-ech")]
)
def test_nasalization_of_the_voiced_stops_and_vowels_is_written(radical, nasalized):
    """digest §10.4: 'only in the case of b, d, g and of initial vowels'."""
    assert mut(radical, "NAS").render() == nasalized


def test_a_written_nasalized_stop_reconstructs_as_a_single_nasal():
    """O-29 / R25: master table ⟨mb⟩ = /m/."""
    assert spelling_to_ipa(mut("bo", "NAS"))[0] == "mˠ"
    assert len(spelling_to_ipa(mut("bo", "NAS"))) == 2


def test_nasalization_of_a_voiceless_stop_is_not_written():
    """spec §11 (ii)."""
    out = mut("tech", "NAS")
    assert out.render() == "tech"
    assert spelling_to_ipa(out)[0] == "dʲ"


@pytest.mark.parametrize("radical", ["son", "mac", "nem", "lám", "rí"])
def test_s_and_the_sonorants_do_not_nasalize(radical):
    assert mut(radical, "NAS").render() == radical


def test_this_strand_has_only_two_mutation_tables():
    """spec §5: no h-prefix, no t-prefix."""
    assert set(OI.grapheme_mutations) == {"LEN", "NAS"}


def test_every_mutation_line_is_anchored_at_the_word_edge():
    """R20."""
    for rules in OI.grapheme_mutations.values():
        for r in rules:
            assert "#" in r.left, (r.rule_id, r.left)
