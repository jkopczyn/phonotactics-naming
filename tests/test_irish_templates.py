"""Task 18: Irish construction templates (spec §3 `[templates]`, I-16; digest §3.4–§3.6)."""
import pytest
from helpers import TABLE, irish
from strands.inputs import Entry
from strands.irish import IrishError, MissingSlot, build_construction

IRISH = irish()


def entry(ipa, **kw):
    return Entry(orthography="x", ipa=ipa, **kw)


def ipa(word):
    return word.ipa(marks=False)


# ---- the plan's tests ------------------------------------------------------------------------

def test_voc_of_a_first_declension_masculine_name():
    words = build_construction("VOC", {"NAME": entry("ʃaːnˠ", declension="m1")}, IRISH, TABLE)
    # a Sheáin: LEN /ʃ/ -> /h/ [wiki-irish-mutations §Summary table] + m1 slenderization.
    # The attested [ə çaːnʲ] is the Munster realization of that /h/; [normalize] no longer
    # derives it (see the [normalize] comment where the old `h -> ç` rule stood).
    assert len(words) == 1 and ipa(words[0]) == "əhaːnʲ"


def test_voc_outside_m1_skips_slenderization():
    words = build_construction("VOC", {"NAME": entry("bʲɾʲiːdʲ", declension="f2")}, IRISH, TABLE)
    assert ipa(words[0]).startswith("əvʲ")                                 # a Bhríd
    assert ipa(words[0]) == "əvʲɾʲiːdʲ"


def test_joins_insert_morpheme_boundaries():
    words = build_construction("VOC", {"NAME": entry("ʃaːnˠ", declension="m1")}, IRISH, TABLE)
    assert words[0].morphemes
    assert 1 in words[0].morphemes                                         # ə $ çaːnʲ


def test_space_literal_splits_into_separate_words():
    words = build_construction("ADJ", {"NAME": entry("mˠaːɾʲə", gender="f"),
                                       "ADJ": entry("bˠaːnˠ")}, IRISH, TABLE)
    assert len(words) == 2 and ipa(words[1]).startswith("w")               # Máire Bhán
    assert ipa(words[0]) == "mˠaːɾʲə"


def test_len_if_f_does_not_lenite_after_a_masculine_noun():
    words = build_construction("ADJ", {"NAME": entry("pˠaːd̪ˠɾˠəɟ", gender="m"),
                                       "ADJ": entry("ɾˠuə")}, IRISH, TABLE)
    assert ipa(words[1]).startswith("ɾˠ")                                  # Pádraig Rua


def test_patro_ni_lenites_the_genitive_father():
    words = build_construction("PATRO_NI", {"FATHER": entry("kaːnˠ", declension="m1")},
                               IRISH, TABLE)
    assert ipa(words[0]).startswith("nʲiː")
    assert ipa(words[0]) == "nʲiːxaːnʲ"                                     # Ní Cháin


def test_patro_o_takes_the_genitive_without_lenition():
    words = build_construction("PATRO_O", {"FATHER": entry("kaːnˠ", declension="m1")},
                               IRISH, TABLE)
    assert ipa(words[0]) == "oːkaːnʲ"                                       # Ó Cáin


def test_compound_lenites_the_second_element():
    words = build_construction("COMPOUND", {"FIRST": entry("l̪ˠasˠəɾʲ"), "SECOND": entry("kosˠ")},
                               IRISH, TABLE)
    assert ipa(words[0]) == "l̪ˠasˠəɾʲxosˠ"                                  # Lasairchos, digest §3.6


def test_gen_dispatches_on_the_inferred_declension():
    words = build_construction("GEN", {"NAME": entry("mˠaɾˠkəx", declension="ach")}, IRISH, TABLE)
    assert ipa(words[0]).endswith("j")


def test_missing_slot_raises():
    with pytest.raises(MissingSlot):
        build_construction("PATRO_O", {}, IRISH, TABLE)


def test_all_eight_templates_exist():
    assert set(IRISH.templates) == {"VOC", "GEN", "PATRO_O", "PATRO_NI", "ADJ", "OF",
                                    "COMPOUND", "DESC"}


# ---- further semantics ---------------------------------------------------------------------

def test_missing_slot_is_an_irish_error():
    assert issubclass(MissingSlot, IrishError)


def test_unknown_template_raises():
    with pytest.raises(IrishError):
        build_construction("NOPE", {"NAME": entry("kaːnˠ")}, IRISH, TABLE)


@pytest.mark.parametrize("decl,expected", [
    ("m1", "bˠaːdʲ"),          # bád -> báid
    ("f2", "bˠaːdʲə"),         # (as if 2nd declension) -> -e
    ("m3", "bˠaːd̪ˠə"),         # broaden + -a
    ("d4", "bˠaːd̪ˠ"),          # no change
])
def test_gen_dispatch_table(decl, expected):
    words = build_construction("GEN", {"NAME": entry("bˠaːd̪ˠ", declension=decl)}, IRISH, TABLE)
    assert ipa(words[0]) == expected


def test_gen_without_a_declension_falls_back_to_m1_with_a_note():
    words = build_construction("GEN", {"NAME": entry("bˠaːd̪ˠ", declension="")}, IRISH, TABLE)
    assert ipa(words[0]) == "bˠaːdʲ"
    assert any("m1" in t.note for t in words[0].trace)


def test_desc_is_the_bare_noun():
    words = build_construction("DESC", {"NOUN": entry("kosˠ")}, IRISH, TABLE)
    assert len(words) == 1 and ipa(words[0]) == "kosˠ" and not words[0].morphemes


def test_of_masculine_genitive_article_lenites():
    words = build_construction("OF", {"NAME": entry("ʃaːnˠ"),
                                      "NOUN": entry("bˠaːd̪ˠ", gender="m", declension="m1")},
                               IRISH, TABLE)
    assert len(words) == 2 and ipa(words[1]) == "ən̪ˠwaːdʲ"                # Seán an bháid
    assert 2 in words[1].morphemes                                         # ən̪ˠ $ waːdʲ


def test_article_blocks_lenition_before_a_coronal():
    words = build_construction("OF", {"NAME": entry("ʃaːnˠ"),
                                      "NOUN": entry("tʲiː", gender="m", declension="d4")},
                               IRISH, TABLE)
    assert ipa(words[1]) == "ənʲtʲiː"                                       # an tí (digest §3.4)


def test_article_gives_s_the_t_prefix():
    words = build_construction("OF", {"NAME": entry("ʃaːnˠ"),
                                      "NOUN": entry("sˠɔl̪ˠəsˠ", gender="m", declension="m1")},
                               IRISH, TABLE)
    assert ipa(words[1]) == "ən̪ˠt̪ˠɔl̪ˠəʃ"                                   # an tsolais, digest §3.1


def test_article_feminine_genitive_is_na_with_h_prothesis():
    words = build_construction("OF", {"NAME": entry("ʃaːnˠ"),
                                      "NOUN": entry("iːhə", gender="f", declension="d4")},
                               IRISH, TABLE)
    assert ipa(words[1]) == "n̪ˠəhiːhə"                                      # na hoíche, digest §3.3


def test_slot_input_is_normalized_before_the_functions_run():
    # user-style transcription: ɑː alias and a quality-less final /n/ (digest line 27, §5.1)
    words = build_construction("VOC", {"NAME": entry("ʃɑːn", declension="m1")}, IRISH, TABLE)
    assert ipa(words[0]) == "əhaːnʲ"


def test_construction_leaves_a_trace():
    words = build_construction("VOC", {"NAME": entry("ʃaːnˠ", declension="m1")}, IRISH, TABLE)
    assert any(t.stage == "irish" and t.rule_id.startswith("templates:") for t in words[0].trace)
    assert any(t.rule_id.startswith("mutations:") for t in words[0].trace)


# ---- review-stress-irish fix 2: a supplied gen_ipa is used, not regularized -----------------

def test_gen_uses_a_supplied_irregular_genitive():
    """The supplied string is used verbatim (bar [normalize]'s aliases): a plain `k` is the
    BROAD dorsal and is not re-marked from the following /iː/ — a slender one is supplied
    as `c` (see below)."""
    e = entry("mˠak", gen_ipa="mˠəkiː", declension="m1")
    words = build_construction("GEN", {"NAME": e}, IRISH, TABLE)
    assert ipa(words[0]) == "mˠəkiː"                      # supplied, not regularized
    assert ipa(words[0]) != "mʲɪc"
    assert any(t.rule_id == "templates:GEN" and "gen_ipa" in t.note for t in words[0].trace)
    e = entry("mˠak", gen_ipa="mˠəciː", declension="m1")
    words = build_construction("GEN", {"NAME": e}, IRISH, TABLE)
    assert ipa(words[0]) == "mˠəciː"


def test_nested_mutation_applies_to_the_supplied_genitive():
    e = entry("mˠak", gen_ipa="mˠəkiː", declension="m1")
    words = build_construction("PATRO_NI", {"FATHER": e}, IRISH, TABLE)
    assert ipa(words[0]) == "nʲiːwəkiː"                   # Ní + LEN(gen_ipa)
    words = build_construction("PATRO_O", {"FATHER": e}, IRISH, TABLE)
    assert ipa(words[0]) == "oːmˠəkiː"


def test_empty_gen_ipa_still_derives_the_regular_genitive():
    words = build_construction("GEN", {"NAME": entry("mˠak", gen_ipa="", declension="m1")},
                               IRISH, TABLE)
    assert ipa(words[0]) == "mʲɪc"
