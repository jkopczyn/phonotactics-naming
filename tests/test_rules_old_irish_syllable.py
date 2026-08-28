"""Task 10: old-irish.rules [syllable] [repair] [stress] [post-stress] (spec §4; O-20, O-28)."""

from helpers import TABLE, target, w

from strands.repair import repair
from strands.stress import assign_stress
from strands.syllabify import syllabify

OI = target("old-irish")


def phon(ipa):
    return assign_stress(repair(syllabify(w(ipa), OI, TABLE), OI, TABLE), OI, TABLE)


def test_the_syllable_spec_is_permissive_and_word_domain():
    s = OI.syllable
    assert s.template is None and s.onsets is None and s.codas is None
    assert s.sonority is False and s.domain == "word" and s.bans == ()


def test_the_nuclei_are_the_wiki_old_irish_values_plus_the_two_modern_pass_throughs():
    """O-28 / R19."""
    assert {"".join(n) for n in OI.syllable.nuclei} == {
        "ai",
        "oi",
        "ui",
        "au",
        "eu",
        "iu",
        "ia",
        "ua",
        "əi",
        "əu",
    }


def test_a_diphthong_is_one_syllable():
    """S12: draft 1's version was an `or` of two assertions over a nucleus not in the list."""
    assert len(phon("tuaθ").syllables) == 1
    assert len(phon("kaix").syllables) == 1


def test_an_unattested_cluster_is_kept_and_flagged_never_repaired():
    assert OI.cluster_fallback == "keep"
    out = phon("sˠt̪ˠɾˠai")
    assert "UNREPAIRED" not in out.flags and out.segments[:3] == ("sˠ", "t̪ˠ", "ɾˠ")


def test_obstruent_geminates_degeminate():
    assert phon("abˠbˠ").segments.count("bˠ") == 1


def test_sonorant_geminates_are_left_alone_because_they_spell_fortis():
    """digest §10.2 conv. 3 / O-2: ⟨ll nn rr mm⟩ = /L N R m/."""
    assert phon("kol̪ˠl̪ˠ").segments.count("l̪ˠ") == 2


def test_stress_is_initial():
    assert phon("konˠxoβaɾˠ").stress == 0


def test_unstressed_vowels_are_not_reduced():
    assert OI.sections.get("post-stress", ()) == ()
    assert "a" in phon("konˠal̪ˠ").segments
