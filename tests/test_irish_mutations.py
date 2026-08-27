"""Task 17: Irish mutations and inflections (digest §3.1–§3.5)."""

import pytest
from helpers import TABLE, irish, mutation_rows, w

from strands.irish import apply_inflection, apply_mutation

IRISH = irish()


def ipa(x):
    return x.ipa(marks=False)


@pytest.mark.parametrize(
    "radical,lenited",
    [
        ("pˠ", "fˠ"),
        ("pʲ", "fʲ"),
        ("bˠ", "w"),
        ("bʲ", "vʲ"),
        ("mˠ", "w"),
        ("mʲ", "vʲ"),
        ("t̪ˠ", "h"),
        ("tʲ", "h"),
        ("d̪ˠ", "ɣ"),
        ("dʲ", "j"),
        ("sˠ", "h"),
        ("ʃ", "h"),
        ("k", "x"),
        ("c", "ç"),
        ("ɡ", "ɣ"),
        ("ɟ", "j"),
    ],
)
def test_lenition_table_digest_3_1(radical, lenited):
    assert ipa(apply_mutation(w(radical + "a"), "LEN", IRISH, TABLE)) == lenited + "a"


def test_fh_lenites_to_nothing():
    assert ipa(apply_mutation(w("fˠaː"), "LEN", IRISH, TABLE)) == "aː"


def test_vowels_and_taps_do_not_lenite():
    for s in ("aː", "ɾˠa", "ɾʲa"):
        assert ipa(apply_mutation(w(s), "LEN", IRISH, TABLE)) == s


@pytest.mark.parametrize(
    "radical,eclipsed",
    [
        ("pˠ", "bˠ"),
        ("pʲ", "bʲ"),
        ("t̪ˠ", "d̪ˠ"),
        ("tʲ", "dʲ"),
        ("k", "ɡ"),
        ("c", "ɟ"),
        ("bˠ", "mˠ"),
        ("bʲ", "mʲ"),
        ("d̪ˠ", "n̪ˠ"),
        ("dʲ", "nʲ"),
        ("ɡ", "ŋ"),
        ("ɟ", "ɲ"),
        ("fˠ", "w"),
        ("fʲ", "vʲ"),
    ],
)
def test_eclipsis_table_digest_3_2(radical, eclipsed):
    assert ipa(apply_mutation(w(radical + "a"), "ECL", IRISH, TABLE)) == eclipsed + "a"


def test_eclipsis_of_a_vowel_initial_word_prefixes_n():
    assert ipa(apply_mutation(w("iːʃ"), "ECL", IRISH, TABLE)) == "nʲiːʃ"


def test_eclipsis_of_a_back_or_open_vowel_initial_word_prefixes_broad_n():
    # digest §3.3: *a n-aois* /n̪ˠV/ — open /a aː ə/ are front=- in features.tsv
    assert ipa(apply_mutation(w("aːsˠ"), "ECL", IRISH, TABLE)) == "n̪ˠaːsˠ"
    assert ipa(apply_mutation(w("uːlʲ"), "ECL", IRISH, TABLE)) == "n̪ˠuːlʲ"


def test_h_prothesis_only_before_vowels():
    assert ipa(apply_mutation(w("iːʃ"), "HPREF", IRISH, TABLE)) == "hiːʃ"
    assert ipa(apply_mutation(w("kaː"), "HPREF", IRISH, TABLE)) == "kaː"


def test_t_prefixation_replaces_s_lenition_after_the_article():
    assert ipa(apply_mutation(w("ʃiːnʲ"), "TPREF", IRISH, TABLE)) == "tʲiːnʲ"  # an tSín


def test_t_prothesis_on_vowel_initial_words():
    assert ipa(apply_mutation(w("eːnˠ"), "TPREF", IRISH, TABLE)) == "tʲeːnˠ"  # an t-éan
    assert ipa(apply_mutation(w("ɪʃcə"), "TPREF", IRISH, TABLE)) == "tʲɪʃcə"  # an t-uisce
    assert ipa(apply_mutation(w("aɾˠəmˠ"), "TPREF", IRISH, TABLE)) == "t̪ˠaɾˠəmˠ"


def test_unknown_mutation_or_inflection_raises():
    from strands.irish import IrishError

    with pytest.raises(IrishError):
        apply_mutation(w("kaː"), "NOPE", IRISH, TABLE)
    with pytest.raises(IrishError):
        apply_inflection(w("kaː"), "NOPE", IRISH, TABLE)


def test_mutation_leaves_a_trace_entry():
    out = apply_mutation(w("kaː"), "LEN", IRISH, TABLE)
    assert out.trace and out.trace[-1].stage == "irish"
    assert out.trace[-1].rule_id.startswith("mutations:")


def test_genitive_of_mac_is_mic():
    assert ipa(apply_inflection(w("mˠak"), "GEN_M1", IRISH, TABLE)) == "mʲɪc"


def test_genitive_of_bad_is_baid():
    # digest §3.5: *bád* → *báid*; the long vowel does not change
    assert ipa(apply_inflection(w("bˠaːd̪ˠ"), "GEN_M1", IRISH, TABLE)) == "bˠaːdʲ"


def test_vocative_m1_is_the_slenderized_stem():
    assert ipa(apply_inflection(w("mˠak"), "VOC_M1", IRISH, TABLE)) == "mʲɪc"


def test_gen_ach_marcach_to_marcaigh():
    assert ipa(apply_inflection(w("mˠaɾˠkəx"), "GEN_ACH", IRISH, TABLE)) == "mˠaɾˠkəj"


def test_gen_f2_brog_to_broige():
    assert ipa(apply_inflection(w("bˠɾˠoːɡ"), "GEN_F2", IRISH, TABLE)).endswith("ə")


def test_gen_f2_slenderizes_before_the_ending():
    assert ipa(apply_inflection(w("bˠɾˠoːɡ"), "GEN_F2", IRISH, TABLE)) == "bˠɾˠoːɟə"


def test_gen_m3_broadens_and_adds_a():
    # digest §3.5: *bádóir* → *bádóra*
    assert ipa(apply_inflection(w("bˠaːd̪ˠoːɾʲ"), "GEN_M3", IRISH, TABLE)) == "bˠaːd̪ˠoːɾˠə"


def test_all_five_inflections_exist():
    """Spec §12.J: a superset of §3's four is sanctioned."""
    assert set(IRISH.inflect) == {"GEN_M1", "GEN_ACH", "GEN_F2", "GEN_M3", "VOC_M1"}


def test_all_four_mutations_exist():
    assert set(IRISH.mutations) == {"LEN", "ECL", "HPREF", "TPREF"}


def test_broad_and_slender_classes_are_declared():
    """I-41 / spec §12.J."""
    assert "k" in IRISH.classes["BROAD"] and "mˠ" in IRISH.classes["BROAD"]
    assert "c" in IRISH.classes["SLEN"] and "mʲ" in IRISH.classes["SLEN"]


def test_the_47_mutation_tagged_rows_apply_without_error():
    """R22: test-words.tsv tags mutations as `mut:` in the `features` column — 47 rows.
    (The 85 `len:` rows are a VOWEL LENGTH tag and are not mutation data.)"""
    rows = mutation_rows()
    assert len(rows) == 47
    for row in rows:
        apply_mutation(w(row["ipa"]), "LEN", IRISH, TABLE)  # must not raise
