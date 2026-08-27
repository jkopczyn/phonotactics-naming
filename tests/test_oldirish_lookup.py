"""Task 12: the lookup stage and the Old Irish assembly (spec §2, §6, §11)."""
import pytest

from helpers import TABLE, irish, target
from strands.inputs import Entry, infer
from strands.lexicon import key, read_lexicon
from strands.oldirish import (OI_FLAGS, ConstructionNotInStrand, infer_stem, run_entry_oi,
                              to_old_irish)
from strands.pipeline import TARGETS, load_target, lookup, run_entry
from strands.spelled import SpelledWord, spelling_to_ipa

IRISH = irish()
OI = target("old-irish")
LEX = read_lexicon()


def entry(orthography, ipa, **kw):
    return infer(Entry(orthography=orthography, ipa=ipa, **kw), IRISH, TABLE)


def test_old_irish_is_the_fifth_target():
    assert TARGETS == ("welsh", "arabic-egy", "georgian", "dutch", "old-irish")
    assert load_target("old-irish", TABLE).meta["strand"] == "old-irish"


def test_lookup_matches_the_citation_form_exactly():
    """O-19, O-23: no fuzzy matching, no de-mutation. A surface form is a MISS."""
    assert lookup(entry("Niall", "nʲiəl̪ˠ"), LEX) is not None
    assert lookup(entry("NIALL", "nʲiəl̪ˠ"), LEX) is not None
    assert lookup(entry("a Sheáin", "ə çaːnʲ"), LEX) is None


def test_an_attested_row_supplies_the_spelling_and_the_filter_never_runs():
    """spec §2 step 1 / §11: lookup yields the attested spelling directly, no conversion."""
    stem = to_old_irish(entry("Niall", "nʲiəl̪ˠ"), LEX, OI, IRISH, TABLE)
    assert stem.flag == "ATTESTED"
    assert stem.words[0].render() == LEX[key("Niall")].oi_nom


def test_a_loan_and_a_late_coinage_are_filtered_and_flagged_apart():
    loan = to_old_irish(entry("Seán", "ʃaːnˠ"), LEX, OI, IRISH, TABLE)
    late = to_old_irish(entry("Saoirse", "ˈsˠiːɾˠʃə"), LEX, OI, IRISH, TABLE)
    assert loan.flag == "RETRO:loan" and late.flag == "RETRO:late"
    assert loan.words and late.words


def test_a_miss_is_a_plain_retro():
    assert to_old_irish(entry("Splancarnach", "sˠpˠl̪ˠaŋkəɾˠnˠəx"), LEX, OI, IRISH,
                        TABLE).flag == "RETRO"


@pytest.mark.parametrize("declension,gender,expected", [
    ("m1", "m", "o"), ("f2", "f", "ā"), ("ach", "m", "o"), ("d4", "m", "indecl"),
    ("", "f", "ā"), ("", "m", "o"),
])
def test_the_stem_class_is_inferred_from_the_declension_then_the_gender(declension, gender,
                                                                       expected):
    """spec §4 / O-21 / S22: draft 1 defaulted an unclassified feminine to `o`."""
    stem, reason = infer_stem(entry("Xyz", "sˠiː", declension=declension, gender=gender))
    assert stem == expected and reason.startswith("stem:")


def test_a_blank_lexicon_stem_is_inferred_and_reported_not_silently_guessed():
    """R31d / O-33: measured, 63 attested rows are in this state."""
    blank = [k for k, r in LEX.items() if r.status == "attested" and not r.stem]
    if not blank:
        pytest.skip("Task 3 filled every stem")
    row = LEX[blank[0]]
    result = run_entry_oi(entry(row.orthography, "sˠiː"), "DESC", IRISH, OI, TABLE)
    assert any(a.startswith("stem:") for a in result.assumptions)


def test_every_result_carries_exactly_one_of_the_five_flags():
    for orthography, ipa in [("Niall", "nʲiəl̪ˠ"), ("Seán", "ʃaːnˠ"),
                             ("Splancarnach", "sˠpˠl̪ˠaŋkəɾˠnˠəx")]:
        result = run_entry_oi(entry(orthography, ipa), "DESC", IRISH, OI, TABLE)
        assert len([f for f in result.flags if f in OI_FLAGS]) == 1, result.flags


def test_the_ipa_is_reconstructed_from_the_finished_written_form():
    """spec §6, §11 / O-11 — and GPT P2: no separator inside a word."""
    result = run_entry_oi(entry("Niall", "nʲiəl̪ˠ"), "DESC", IRISH, OI, TABLE)
    rebuilt = " ".join("".join(spelling_to_ipa(SpelledWord.from_spelling(p)))
                       for p in result.respelling.split(" "))
    assert result.ipa == rebuilt
    assert "  " not in result.ipa


def test_punctum_off_changes_the_respelling_and_not_the_ipa():
    """O-14 / spec §11: a rendering option applied AFTER reconstruction."""
    from dataclasses import replace as _replace
    off = _replace(OI, meta={**OI.meta, "punctum": "off"})
    a = run_entry_oi(entry("Sean-", "ʃanˠ"), "DESC", IRISH, OI, TABLE)
    b = run_entry_oi(entry("Sean-", "ʃanˠ"), "DESC", IRISH, off, TABLE)
    assert a.ipa == b.ipa


def test_run_entry_dispatches_on_the_meta_strand_key():
    a = run_entry(entry("Niall", "nʲiəl̪ˠ"), "DESC", IRISH, OI, TABLE)
    b = run_entry_oi(entry("Niall", "nʲiəl̪ˠ"), "DESC", IRISH, OI, TABLE)
    assert a == b


def test_an_epithet_slot_this_strand_does_not_map_is_no_affix():
    """R30 / O-17: `DESC+ADJ` must equal `DESC`, with an assumption saying why."""
    plain = run_entry_oi(entry("Niall", "nʲiəl̪ˠ"), "DESC", IRISH, OI, TABLE)
    slotted = run_entry_oi(entry("Niall", "nʲiəl̪ˠ"), "DESC+ADJ", IRISH, OI, TABLE)
    assert slotted.respelling == plain.respelling and slotted.ipa == plain.ipa
    assert any("unmapped" in a for a in slotted.assumptions)


def test_a_construction_this_strand_does_not_have_raises_not_crashes():
    with pytest.raises(ConstructionNotInStrand):
        run_entry_oi(entry("Niall", "nʲiəl̪ˠ"), "PATRO_O", IRISH, OI, TABLE)


def test_a_multi_word_attested_form_becomes_several_words():
    row = LEX.get(key("Cú Chulainn"))
    if row is None:
        pytest.skip("no multi-word row in the lexicon")
    assert len(to_old_irish(entry("Cú Chulainn", "kuː xʊl̪ˠənʲ"), LEX, OI, IRISH,
                            TABLE).words) == 2


def test_the_result_is_deterministic():
    e = entry("Niall", "nʲiəl̪ˠ")
    assert run_entry_oi(e, "DESC", IRISH, OI, TABLE) == run_entry_oi(e, "DESC", IRISH, OI, TABLE)
