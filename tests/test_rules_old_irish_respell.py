"""Task 11: old-irish.rules [respell], editorial orthography (spec §6, §11; digest §10.2)."""

import pytest
from helpers import TABLE, target, w

from strands.respell import respell
from strands.spelled import SpelledWord
from strands.syllabify import syllabify
from strands.word import Word

OI = target("old-irish")


def spell(*segments):
    return respell(Word(segments=segments), OI, TABLE)


def test_lenited_b_d_g_m_are_written_unmarked():
    """digest §10.2 conv. 1 — the largest visual difference from a modern name."""
    assert spell("d̪ˠ", "u", "β") == "dub"
    assert spell("l̪ˠ", "aː", "β̃") == "lám"
    assert spell("a", "ð", "a", "ɾˠ", "k") == "adarc"


def test_lenited_voiceless_stops_are_written_with_h():
    assert spell("k", "l̪ˠ", "o", "x") == "cloch"
    assert spell("bˠ", "l̪ˠ", "aː", "θ") == "bláth"


def test_non_initial_voiceless_stops_are_doubled_and_voiced_ones_are_written_c_t_p():
    """digest §10.2 conv. 2-3 — this restores *mac -> macc* with no lexical list.

    Task 11 deviation: the plan's fixture spelled *bec* with slender /ɟ/, which rule 8
    (the §36 glide, NOT blocked after ⟨e⟩ per S20) would write *beic*. *bec* /bʲeɡ/ has a
    broad /ɡ/ (digest §10.2 conv. 2; modern *beag*), so the fixture uses `ɡ`."""
    assert spell("mˠ", "a", "k") == "macc"
    assert spell("bʲ", "e", "ɡ") == "bec"
    assert spell("bˠ", "ɾˠ", "a", "t̪ˠ") == "bratt"
    assert spell("bˠ", "ɾˠ", "o", "d̪ˠ") == "brot"


@pytest.mark.parametrize(
    "segments,expected",
    [
        (("ʃ", "c", "eː", "l̪ˠ"), "scél"),  # [old-irish-lexicon] scéal ~ scél
        (("sˠ", "pˠ", "l̪ˠ", "a", "n̪ˠ", "ɡ"), "splanc"),
        (("sˠ", "pʲ", "e", "l̪ˠ"), "spel"),
        (("ʃ", "pʲ", "ɾʲ", "iː"), "sprí"),
        (("ʃ", "tʲ", "ɾʲ", "iː", "k"), "strícc"),  # final /k/ IS post-vocalic
        (("tʲ", "ɾʲ", "e", "x", "t̪ˠ", "a"), "trechta"),  # /t/ after /x/, not after a vowel
    ],
)
def test_a_voiceless_stop_is_not_doubled_after_a_consonant(segments, expected):
    """Digest §10.2 conv. 2 is the wiki's §Stops following VOWELS: ⟨c t p⟩ read as /ɡ d b/
    only between vowels, so only there does the doubling have work to do. After ⟨s⟩ (and any
    other consonant not already claimed by (1)) the single letter is unambiguous. Draft 1
    doubled unconditionally and wrote *sccél*, *spplanc*, *sppel*, *spprí*, *sttrícc*."""
    assert spell(*segments) == expected


def test_the_post_vocalic_doubling_still_fires():
    """The attested rows are the guide: *macc*, *cnocc*, *baccach*, *bratt*."""
    assert spell("mˠ", "a", "k") == "macc"
    assert spell("k", "n̪ˠ", "o", "k") == "cnocc"
    assert spell("bˠ", "a", "k", "a", "x") == "baccach"
    assert spell("bˠ", "ɾˠ", "a", "t̪ˠ") == "bratt"


def test_a_nasalized_stop_is_not_devoiced_by_the_doubling_rule():
    assert spell("mˠ", "bˠ", "oː") == "mbó"
    assert spell("ŋ", "ɡ", "a") == "nga"


def test_a_stop_after_a_sonorant_is_written_single_and_keeps_its_voice():
    """digest §10.2 conv. 4: *derc* /dʲerk/ ~ /dʲerɡ/, *delg*, *cerd*, *imb*; lexicon
    dearg ~ derg, adharc ~ adarc, Colmán ~ Colmán."""
    assert spell("dʲ", "e", "ɾˠ", "ɡ") == "derg"
    assert spell("dʲ", "e", "ɾˠ", "k") == "derc"
    assert spell("k", "e", "ɾˠ", "d̪ˠ") == "cerd"
    assert spell("k", "o", "l̪ˠ", "mˠ", "aː", "n̪ˠ") == "colmán"


def test_the_eight_diphthongs_and_the_ao_default():
    for segments, expected in [
        (("a", "i"), "áe"),
        (("o", "i"), "oí"),
        (("u", "i"), "uí"),
        (("a", "u"), "áu"),
        (("e", "u"), "éu"),
        (("i", "u"), "íu"),
        (("i", "a"), "ía"),
        (("u", "a"), "úa"),
    ]:
        assert spell(*segments) == expected


def test_the_glide_i_marks_a_final_slender_consonant():
    """digest §10.2 conv. 5 §36."""
    assert spell("mˠ", "u", "ɾʲ") == "muir"
    assert spell("k", "a", "ɾʲ", "tʲ") == "cairt"  # the whole final cluster
    assert spell("bˠ", "ɾʲ", "i", "a", "nʲ") == "bríain"  # after ⟨ía⟩ (gen. *Bríain*)
    # Medially, "at the end of a syllable" = before a consonant (conv. 5 (ii)); [syllable]
    # has `onsets = any`, so a `.`-based rule would never fire on a real medial cluster.
    word = syllabify(w("mˠuɾʲçeɾˠt̪ˠax"), OI, TABLE)
    assert respell(word, OI, TABLE) == "muirchertach"
    assert spell("a", "lʲ", "βʲ", "ə") == "ailbə"
    assert spell("k", "a", "ɾʲ", "e") == "care"  # before a vowel letter: no glide


def test_no_glide_is_written_before_a_broad_consonant():
    assert spell("fʲ", "e", "ɾˠ") == "fer"


def test_the_glide_is_blocked_after_i_and_the_long_front_vowels_but_not_after_e():
    """S20: Pokorny's exception list is í, é, aí, oí, uí — not short ⟨e⟩."""
    assert spell("mˠ", "iː", "nʲ") == "mín"
    assert spell("eː", "nʲ") == "én"
    assert spell("k", "a", "i", "lʲ") == "cáel"  # c + áe + l, no second i
    assert spell("k", "e", "lʲ") == "ceil"


def test_the_post_stress_schwa_grid():
    assert spell("dʲ", "iː", "ɣ", "ə", "l̪ˠ") == "dígal"
    assert spell("dʲ", "iː", "ɣ", "ə", "lʲ") == "dígail"
    assert spell("dʲ", "lʲ", "i", "ɣʲ", "ə", "ð") == "dliged"
    assert spell("dʲ", "lʲ", "i", "ɣʲ", "ə", "ðʲ") == "dligid"


def test_a_word_final_schwa_becomes_the_ending_marker():
    """spec §11: the retro-filter leaves it UNRESOLVED; Task 14 realizes it by stem class."""
    assert spell("k", "a", "ɾˠ", "ə").endswith("ə")


def test_sonorant_geminates_are_written_doubled():
    """digest §10.2 conv. 3. R16: nothing upstream produces two identical sonorants, so this
    fires only on a lexicon-sourced word; the rule exists so the section is complete."""
    assert spell("k", "o", "l̪ˠ", "l̪ˠ") == "coll"
    assert spell("k", "e", "nʲ", "nʲ") == "ceinn"


def test_written_lenition_of_p_and_s_follows_the_source_spelling():
    """digest §10.2 conv. 1: ⟨ph⟩ where the source was ⟨ph⟩, else ⟨f⟩; ⟨ṡ⟩ where ⟨sh⟩."""
    from strands.orth import tag_word

    assert respell(tag_word(Word(segments=("a", "fˠ", "aː", "l̪ˠ")), "aphál"), OI, TABLE) == "aphál"
    assert spell("fʲ", "e", "ɾˠ") == "fer"
    assert respell(tag_word(Word(segments=("a", "h", "aː", "l̪ˠ")), "ashál"), OI, TABLE) == "aṡál"
    assert spell("h", "aː", "l̪ˠ") == "hál"


def test_every_respell_output_is_tokenizable_as_a_spelled_word():
    """R27: draft 1's [respell] and reconstruction used different alphabets. This is the
    property that keeps them one system."""
    for segments in [
        ("d̪ˠ", "u", "β"),
        ("mˠ", "a", "k"),
        ("k", "l̪ˠ", "o", "x"),
        ("mˠ", "u", "ɾʲ"),
        ("dʲ", "iː", "ɣ", "ə", "l̪ˠ"),
        ("a", "i"),
        ("k", "a", "ɾˠ", "ə"),
        ("mˠ", "bˠ", "oː"),
        ("k", "o", "l̪ˠ", "l̪ˠ"),
        ("bʲ", "e", "ɡ"),
        ("dʲ", "lʲ", "i", "ɣʲ", "ə", "ðʲ"),
    ]:
        text = spell(*segments)
        assert SpelledWord.from_spelling(text).render() == text, text


def test_every_inventory_segment_respells_to_grapheme_tokens_only():
    """S21 + R27 as a property: no inventory segment leaks through as IPA."""
    for seg in OI.inventory:
        text = spell(seg)
        assert SpelledWord.from_spelling(text).render() == text, (seg, text)


def test_no_h_prefix_is_ever_written():
    assert not spell("eː", "n̪ˠ").startswith("h")


def test_every_respell_line_carries_a_citation_and_a_legal_tag():
    rules = OI.sections["respell"]
    assert rules, "the [respell] section is empty"
    for r in rules:
        assert r.tag in ("attested", "design", "fallback"), r.line
        assert r.comment, r.line
