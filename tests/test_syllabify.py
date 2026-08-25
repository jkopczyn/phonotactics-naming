"""Plan Task 10: nucleus-aware syllabifier (spec §3 `[syllable]`, §12.B, §12.D; I-2, I-13, I-14)."""
import pytest
from helpers import TABLE, w
from strands.dsl import parse_rules
from strands.word import Word
from strands.syllabify import syllabify, group_nuclei, legal_onset

# The inventory line must not contain a diphthong row (I-2/I-35): diphthongs are two segments.
CV = ("[inventory]\np t k b s l r a i u aː\n"
      "[syllable]\ntemplate = (C)(C)N(C)\nonsets = p t k b s l r pl pr st\n"
      "codas = p t k s st\nsonority = on\n")


def syl(src, ipa):
    rf = parse_rules(src, TABLE)
    return syllabify(w(ipa), rf, TABLE)


def test_simple_cv_parse():
    out = syl(CV, "pata")
    assert out.syllables == (0, 2) and out.illegal == frozenset()


def test_maximal_onset_subject_to_legality():
    assert syl(CV, "apla").syllables == (0, 1)      # a.pla, 'pl' is a legal onset
    assert syl(CV, "apta").syllables == (0, 2)      # ap.ta, 'pt' is not


def test_singleton_absent_from_the_onset_list_is_illegal():
    """Spec §12.D: the list is complete, so an unlisted singleton is not licensed."""
    src = CV.replace("onsets = p t k b s l r pl pr st", "onsets = p t")
    assert syl(src, "kata").illegal


def test_illegal_initial_cluster_is_marked_not_raised():
    out = syl(CV, "kta")
    assert out.illegal == frozenset({0, 1}) and "syllabify" in [t.stage for t in out.trace]


def test_minimal_illegal_span():
    out = syl(CV, "apkta")
    assert 0 not in out.illegal and out.illegal


def test_appendix_licenses_extra_final_coronals():
    src = CV + "appendix = s t\n"
    assert syl(src, "apst").illegal == frozenset()


def test_nuclei_grouping_makes_a_diphthong_one_syllable():
    src = ("[inventory]\np i ə a\n[syllable]\ntemplate = (C)N(C)\nnuclei = iə\n"
           "onsets = p\ncodas = p\nsonority = off\n")
    out = syl(src, "piə")
    assert len(out.syllables) == 1 and out.nuclei == ((1, 3),)


def test_without_a_nuclei_declaration_the_same_string_is_hiatus():
    src = ("[inventory]\np i ə a\n[syllable]\ntemplate = (C)N(C)\n"
           "onsets = p\ncodas = p\nsonority = off\n")
    out = syl(src, "piə")
    assert len(out.syllables) == 2                 # Georgian behaviour (spec §12.B)


def test_sonority_on_rejects_falling_onsets_and_off_accepts_them():
    on = ("[inventory]\np l a\n[syllable]\ntemplate = (C)(C)N(C)\nonsets = any\nsonority = on\n")
    off = on.replace("sonority = on", "sonority = off")
    assert syl(on, "lpa").illegal and syl(off, "lpa").illegal == frozenset()


def test_sc_clusters_are_exempt_from_sonority():
    src = "[inventory]\ns t a\n[syllable]\ntemplate = (C)(C)N(C)\nonsets = any\nsonority = on\n"
    assert syl(src, "sta").illegal == frozenset()


def test_bans_mark_their_span():
    src = ("[inventory]\np t a aː\n[syllable]\ntemplate = any\nonsets = any\ncodas = any\n"
           "sonority = off\nbans = [V +long] C C\n")
    assert 0 in syl(src, "aːpta").illegal


def test_stem_domain_uses_morpheme_boundaries():
    src = ("[inventory]\np t a\n[syllable]\ntemplate = any\nonsets = any\ncodas = any\n"
           "sonority = off\ndomain = stem\n")
    rf = parse_rules(src, TABLE)
    out = syllabify(Word(segments=("p", "a", "t", "a"), morphemes=frozenset({2})), rf, TABLE)
    assert out.syllables == (0, 2)


def test_pending_stress_is_converted_to_a_syllable_index():
    """S1: tokenize gives a segment index; syllabify converts it."""
    out = syl(CV, "paˈta")
    assert out.stress == 1


def test_syllabify_is_idempotent():
    rf = parse_rules(CV, TABLE)
    a = syl(CV, "pata")
    assert syllabify(a, rf, TABLE).syllables == a.syllables


# ---- helper-level tests -----------------------------------------------------------------------

def test_group_nuclei_pairs_only_licensed_sequences():
    rf = parse_rules("[inventory]\np i ə a\n[syllable]\nnuclei = iə\n", TABLE)
    assert group_nuclei(("p", "i", "ə", "a", "i"), rf.syllable, TABLE) == [(1, 3), (3, 4), (4, 5)]


def test_legal_onset_respects_list_and_sonority():
    rf = parse_rules(CV, TABLE)
    assert legal_onset(("p", "l"), rf.syllable, TABLE)
    assert not legal_onset(("p", "t"), rf.syllable, TABLE)
    assert legal_onset((), rf.syllable, TABLE)


def test_domain_without_a_nucleus_is_illegal_in_full():
    out = syl(CV, "pst")
    assert out.illegal == frozenset({0, 1, 2}) and out.syllables == ()


def test_onset_required_marks_a_vowel_initial_word():
    src = CV + "onset-required = yes\n"
    assert 0 in syl(src, "apa").illegal and syl(CV, "apa").illegal == frozenset()


def test_onset_required_marks_every_onsetless_syllable_not_only_the_first():
    """Spec §12.D: the empty onset is allowed UNLESS onset-required = yes — for every
    syllable, not just the domain-initial one. Hiatus creates an empty onset."""
    src = CV + "onset-required = yes\n"
    out = syl(src, "aa")                       # no nuclei licensed: two syllables, both onsetless
    assert out.syllables == (0, 1) and out.illegal == frozenset({0, 1})
    src2 = ("[inventory]\np a i\n[syllable]\ntemplate = (C)N(C)\nnuclei = ai\n"
            "onsets = p\ncodas = p\nsonority = off\nonset-required = yes\n")
    out2 = syl(src2, "paia")                   # pai.a — the vowel after the diphthong is onsetless
    assert out2.nuclei == ((1, 3), (3, 4)) and out2.illegal == frozenset({3})
    assert syl(src2, "papa").illegal == frozenset()
