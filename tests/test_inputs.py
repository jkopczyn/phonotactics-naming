"""Task 20: input TSV reader, gender / declension / genitive inference, lint (spec §5, §12.H)."""

import csv
import shutil

from helpers import FIX, ROOT, TABLE, irish

from strands.inputs import INPUT_COLUMNS, Entry, accept_guesses, infer, lint_report, read_input

IRISH = irish()


def test_reads_all_ten_columns():
    assert len(INPUT_COLUMNS) == 10
    assert read_input(FIX)[0].orthography and read_input(FIX)[0].gloss
    assert read_input(FIX)[0].gen_ipa == "ʃaːnʲ"


def test_row_without_ipa_gets_a_constructed_one():
    """Milestone 8 / spec §5: an empty `ipa` is now filled by the provisional G2P and tagged,
    instead of skipping the row."""
    e = [x for x in read_input(FIX) if x.orthography == "NoIpa"][0]
    assert e.ipa and "ipa:constructed" in e.assumptions
    assert "skipped:no-ipa" not in e.assumptions


def test_no_ipa_is_only_for_an_unreadable_orthography():
    """`skipped:no-ipa` survives for the two cases G2P cannot help with."""
    e = infer(Entry("123"), IRISH, TABLE)  # no vowel letter: g2p raises
    assert e.ipa == "" and "skipped:no-ipa" in e.assumptions


def test_g2p_notes_become_assumption_tags():
    e = infer(Entry("cnoc"), IRISH, TABLE)
    assert e.ipa == "kɾˠɔk"  # [C] ⟨cn⟩ is /kɾˠ/, one of the rules that records a note
    assert any(t.startswith("g2p:") for t in e.assumptions)


def test_constructed_ipa_feeds_the_later_inference_steps():
    """The constructed string is a real transcription, so declension and gen_ipa follow."""
    e = infer(Entry("Cormac"), IRISH, TABLE)
    assert e.ipa and e.gen_ipa and "gen_ipa:inferred-m1" in e.assumptions


def test_unknown_columns_are_ignored():
    """test-words.tsv has `features`, not the spec §5 header."""
    entries = read_input(ROOT / "sources" / "irish" / "test-words.tsv")
    assert len(entries) == 144
    assert entries[0].orthography == "Ciara" and entries[0].gender == ""


def test_missing_dialect_defaults_to_C():
    e = infer(Entry("x", ipa="kaː", dialect=""), IRISH, TABLE)
    assert e.dialect == "C" and "dialect:default-C" in e.assumptions


def test_gender_from_ending_and_default():
    e = infer(Entry("Bríd", ipa="bʲɾʲiːdʲ", gender=""), IRISH, TABLE)
    assert e.gender == "f"
    e = infer(Entry("Zzz", ipa="t̪ˠaːk", gender=""), IRISH, TABLE)
    assert e.gender == "m" and "gender:default-m" in e.assumptions


def test_gender_from_known_name_list():
    """Built from test-words.tsv glosses of the form '(f. given name)'."""
    e = infer(Entry("Oisín", ipa="ɔʃiːnʲ", gender=""), IRISH, TABLE)
    assert e.gender == "m" and "gender:known-name" in e.assumptions
    e = infer(Entry("Niamh", ipa="nʲiəw", gender=""), IRISH, TABLE)
    assert e.gender == "f" and "gender:known-name" in e.assumptions


def test_gender_from_suffix_endings():
    assert infer(Entry("fuinneog", ipa="fˠɪnʲoːɡ", gender=""), IRISH, TABLE).gender == "f"
    e = infer(Entry("cailín", ipa="kalʲiːnʲ", gender=""), IRISH, TABLE)
    assert e.gender == "m" and "gender:ending" in e.assumptions


def test_declension_is_inferred_and_tagged():
    """R24 / spec §12.H — without this, --construction all silently defaults to m1."""
    assert infer(Entry("marcach", ipa="mˠaɾˠkəx"), IRISH, TABLE).declension == "ach"
    assert infer(Entry("mac", ipa="mˠak", gender="m"), IRISH, TABLE).declension == "m1"
    assert infer(Entry("bróg", ipa="bˠɾˠoːɡ", gender="f"), IRISH, TABLE).declension == "f2"
    assert infer(Entry("bádóir", ipa="bˠaːd̪ˠoːɾʲ"), IRISH, TABLE).declension == "m3"
    assert infer(Entry("balla", ipa="bˠal̪ˠə"), IRISH, TABLE).declension == "d4"
    assert infer(Entry("cailín", ipa="kalʲiːnʲ"), IRISH, TABLE).declension == "d4"
    assert any(
        a.startswith("declension:")
        for a in infer(Entry("marcach", ipa="mˠaɾˠkəx"), IRISH, TABLE).assumptions
    )


def test_gen_ipa_uses_the_inflection_tables_not_a_second_implementation():
    e = infer(Entry("mac", ipa="mˠak", gender="m", gen_ipa=""), IRISH, TABLE)
    assert e.gen_ipa == "mʲɪc" and "gen_ipa:inferred-m1" in e.assumptions
    e = infer(Entry("bróg", ipa="bˠɾˠoːɡ", gender="f", gen_ipa=""), IRISH, TABLE)
    assert e.gen_ipa == "bˠɾˠoːɟə"
    e = infer(Entry("marcach", ipa="mˠaɾˠkəx", gen_ipa=""), IRISH, TABLE)
    assert e.gen_ipa == "mˠaɾˠkəj"
    e = infer(Entry("bádóir", ipa="bˠaːd̪ˠoːɾʲ", gen_ipa=""), IRISH, TABLE)
    assert e.gen_ipa == "bˠaːd̪ˠoːɾˠə"


def test_vowel_final_gen_ipa_is_unchanged():
    e = infer(Entry("balla", ipa="bˠal̪ˠə", gen_ipa=""), IRISH, TABLE)
    assert e.gen_ipa == "bˠal̪ˠə" and "gen_ipa:inferred-d4" in e.assumptions


def test_row_read_without_ipa_is_still_fully_inferred():
    e = infer(read_input(FIX)[1], IRISH, TABLE)
    assert e.orthography == "NoIpa" and e.gender and e.declension
    assert e.ipa and e.gen_ipa and "ipa:constructed" in e.assumptions


def test_supplied_fields_are_never_overwritten():
    e = infer(Entry("x", ipa="kaː", gender="f", declension="d4", gen_ipa="kaː"), IRISH, TABLE)
    assert e.gender == "f" and e.declension == "d4" and e.assumptions == ()


def test_infer_is_idempotent():
    once = infer(read_input(FIX)[3], IRISH, TABLE)
    assert infer(once, IRISH, TABLE) == once


def test_lint_report_lists_one_line_per_guess():
    lines = lint_report([infer(x, IRISH, TABLE) for x in read_input(FIX)])
    assert any("declension" in l for l in lines) and all(l.strip() for l in lines)
    assert any("NoIpa" in l and "ipa = " in l and "ipa:constructed" in l for l in lines)
    assert any(l.startswith("Bríd") and "gender" in l for l in lines)


def test_accept_writes_the_guesses_back(tmp_path):
    dst = tmp_path / "in.tsv"
    shutil.copy(FIX, dst)
    accept_guesses(dst, [infer(x, IRISH, TABLE) for x in read_input(dst)])
    rows = list(csv.DictReader(dst.open(encoding="utf-8"), delimiter="\t"))
    assert all(r["gender"] for r in rows)
    assert all(r["dialect"] for r in rows)
    assert [r["orthography"] for r in rows] == [e.orthography for e in read_input(FIX)]
    by = {r["orthography"]: r for r in rows}
    assert by["mac"]["gen_ipa"] == "mʲɪc"
    # the constructed IPA is written into the `ipa` column, and said so in `note`
    assert by["NoIpa"]["ipa"] and by["NoIpa"]["gen_ipa"]
    assert "ipa constructed by g2p" in by["NoIpa"]["note"]
    assert by["Seán"]["ipa"] == "ʃaːn̪ˠ"  # a supplied transcription is untouched
    assert "g2p" not in by["Seán"]["note"]
    assert by["Seán"]["gen_ipa"] == "ʃaːnʲ"  # supplied value untouched


# ---- review-stress-irish fix 4: classify and inflect the NORMALIZED form -------------------


def test_alias_final_consonant_is_classified_after_normalization():
    """ASCII `g` is an input alias of `ɡ` (irish.rules [normalize]); a feminine noun ending
    in it is f2, not the m1 default."""
    e = infer(Entry("bróg", ipa="bˠɾˠoːg", gender="f"), IRISH, TABLE)
    assert e.declension == "f2" and "declension:inferred-f2" in e.assumptions
    assert e.gen_ipa == "bˠɾˠoːɟə"


def test_unmarked_input_inflects_to_the_canonical_genitive():
    e = infer(Entry("mac", ipa="mak", gender="m"), IRISH, TABLE)
    assert e.declension == "m1" and e.gen_ipa == "mʲɪc"
    assert "ˈ" not in e.gen_ipa


def test_ipa_column_accepts_slash_and_bracket_delimiters(tmp_path):
    """Owner request 2026-08-27: `/iːˈdɑːn/` is read as `iːˈdɑːn` (also `[...]`), for ipa,
    gen_ipa and pl_ipa; a bare transcription is unchanged."""
    f = tmp_path / "in.tsv"
    f.write_text(
        "orthography\tipa\tgen_ipa\nÉadan\t/iːˈdɑːn/\t[iːˈdɑːnʲ]\nSeán\tʃaːnˠ\t\n", encoding="utf-8"
    )
    rows = read_input(f)
    assert rows[0].ipa == "iːˈdɑːn" and rows[0].gen_ipa == "iːˈdɑːnʲ"
    assert rows[1].ipa == "ʃaːnˠ"


def test_declension_column_is_read_written_and_validated(tmp_path):
    """Spec §12.K (2026-08-27): `declension` is an optional column. A supplied value is
    honoured (no `declension:` assumption, GEN/VOC dispatch on it); `--accept` writes the
    inferred value back so lint stops reporting it; a bad value is an InputError."""
    import pytest

    from strands.inputs import InputError

    f = tmp_path / "in.tsv"
    f.write_text(
        "orthography\tipa\tgender\tdeclension\nSeán\tʃaːnˠ\tm\t\nBríd\tbʲɾʲiːdʲ\tf\tf2\n",
        encoding="utf-8",
    )
    entries = [infer(x, IRISH, TABLE) for x in read_input(f)]
    assert entries[0].declension == "m1" and any(
        a.startswith("declension:") for a in entries[0].assumptions
    )
    assert entries[1].declension == "f2" and not any(
        a.startswith("declension:") for a in entries[1].assumptions
    )
    accept_guesses(f, entries)
    rows = list(csv.DictReader(f.open(encoding="utf-8"), delimiter="\t"))
    assert rows[0]["declension"] == "m1" and rows[1]["declension"] == "f2"
    again = [infer(x, IRISH, TABLE) for x in read_input(f)]
    assert not any(a.startswith("declension:") for e in again for a in e.assumptions)
    f.write_text("orthography\tipa\tdeclension\nX\tʃaːnˠ\tq9\n", encoding="utf-8")
    with pytest.raises(InputError):
        infer(read_input(f)[0], IRISH, TABLE)
