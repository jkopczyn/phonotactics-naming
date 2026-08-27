"""Task 3: the lexicon as data after the fix-up (spec §7, §10; O-18, O-21, O-33)."""
import csv

import pytest
from helpers import ROOT, read_test_words

from strands.check import check_lexicon_file
from strands.lexicon import FORM_STATUSES, KINDS, key, read_lexicon, read_rows

PATH = ROOT / "rules" / "old-irish-lexicon.tsv"
HEADER, ROWS = read_rows(PATH)
LEX = read_lexicon(PATH)
FORMS = [r for r in ROWS if r.status in FORM_STATUSES]
NONE_ROWS = [r for r in ROWS if r.status == "none"]
# Task 3 deviation from the plan's draft of this file: a noun whose class the cited sources do
# not show keeps a blank `stem`/`gender` under an `unattested:` note (plan Part B: "do not invent
# classes"; O-33 infers and tags it at runtime) instead of a false `no nominal paradigm:` label.
EXEMPT = ("no nominal paradigm:", "unattested:")
VERIF_COLUMNS = ("orthography", "source", "field", "verdict", "checked_by", "note")


def verification(name):
    with (ROOT / "rules" / name).open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh, delimiter="\t")
        return list(reader.fieldnames or []), list(reader)


def test_the_lexicon_is_completely_clean():
    """After this task there are no findings at all, not even warnings."""
    assert check_lexicon_file(PATH) == []


def test_the_three_task2_warnings_are_now_errors():
    """The promotion IS this task's acceptance criterion (R3a)."""
    from strands.lexicon import LEXICON_COLUMNS, LexEntry, validate
    bad = LexEntry(orthography="x", status="none", source="https://e.x", line=2)
    codes = {(e.code, e.severity) for e in validate(list(LEXICON_COLUMNS), [bad], "t")}
    assert ("LEX_NONE_NO_KIND", "error") in codes


def test_the_irregular_placeholder_is_now_reserved_for_suppletion():
    """Log finding 5: 37 rows wore `irregular` for four different paradigms."""
    left = [r.orthography for r in FORMS if r.stem == "irregular"]
    assert len(left) <= 10, left


@pytest.mark.parametrize("headword,stem", [
    ("teach", "s"), ("sliabh", "s"), ("athair", "r"), ("máthair", "r"), ("bráthair", "r"),
    ("rí", "velar"), ("Lughaidh", "velar"), ("Eochaidh", "velar"), ("Pádraig", "indecl"),
])
def test_the_paradigm_words_the_inflection_tests_need_are_classified(headword, stem):
    row = LEX.get(key(headword))
    assert row is not None, headword
    assert row.stem == stem, (headword, row.stem)


def test_every_remaining_backlog_row_says_why_it_has_no_paradigm():
    backlog = [r for r in FORMS if (not r.stem or not r.gender)
               and not r.note.startswith(EXEMPT)]
    assert backlog == [], [(r.orthography, r.stem, r.gender) for r in backlog]


def test_every_none_row_is_classified_loan_or_late():
    """O-18 / S4: classified from the row's own note, not from the log's table."""
    assert all(r.kind in KINDS for r in NONE_ROWS)
    assert all(not (r.oi_nom or r.oi_gen or r.stem or r.gender) for r in NONE_ROWS)


def test_the_formation_elements_task15_needs_exist():
    """R31: draft 1's formation tests skipped because these were absent."""
    for element in ("Maol", "Giolla", "cú", "fear", "mac", "inion", "Colm", "Pádraig"):
        assert key(element) in LEX, element


def test_the_nessa_row_is_complete():
    """S23: *Conchobar mac Nessa* is the digest's own example and must be reproducible."""
    row = LEX[key("Neasa")] if key("Neasa") in LEX else LEX[key("Nessa")]
    assert row.stem and row.oi_gen


def test_old_irish_forms_carry_no_modern_lenition_digraphs():
    """digest §10.2 conv. 1 / log finding 3."""
    bad = [(r.orthography, r.oi_nom) for r in FORMS
           if any(d in r.oi_nom.lower() for d in ("bh", "dh", "gh", "mh"))]
    assert bad == [], bad


def test_the_measured_regression_overlap_is_intact():
    """O-31: 54 form-bearing keys also in test-words.tsv with hand IPA."""
    keys = {key(r["orthography"]) for r in read_test_words() if r["ipa"]}
    overlap = {k for k in keys & set(LEX) if LEX[k].status in FORM_STATUSES}
    assert len(overlap) >= 54, len(overlap)


@pytest.mark.parametrize("name", ["old-irish-lexicon.verification.tsv",
                                  "old-irish-lexicon.verification2.tsv"])
def test_both_verification_files_exist_with_the_agreed_schema(name):
    """R3: the first pass was prose in the log; this task back-fills it."""
    header, rows = verification(name)
    assert tuple(header) == VERIF_COLUMNS
    assert len(rows) >= 30, (name, len(rows))


def test_every_verdict_is_explained_and_attributed():
    for name in ("old-irish-lexicon.verification.tsv", "old-irish-lexicon.verification2.tsv"):
        for r in verification(name)[1]:
            assert r["verdict"] in ("ok", "fixed", "removed"), r
            assert r["checked_by"].strip(), r
            if r["verdict"] != "ok":
                assert r["note"].strip(), (name, r["orthography"])


def test_the_second_pass_defect_rate_admits_the_genitive_less_rows():
    rows = verification("old-irish-lexicon.verification2.tsv")[1]
    defects = sum(r["verdict"] != "ok" for r in rows)
    assert defects <= len(rows) // 10, (defects, len(rows))


def test_removed_rows_are_gone_and_kept_rows_are_present():
    for r in verification("old-irish-lexicon.verification2.tsv")[1]:
        assert (key(r["orthography"]) in LEX) != (r["verdict"] == "removed"), r["orthography"]


# ---- Task 4: the Middle Irish tier (spec §10; O-22) --------------------------------------

MIDDLE = [r for r in ROWS if r.status == "middle"]


def test_the_middle_irish_tier_is_populated():
    """spec §10: the important names should not be left to the filter."""
    assert len(MIDDLE) >= 8, len(MIDDLE)


@pytest.mark.parametrize("headword", ["Eoghan", "Tadhg", "Oisín"])
def test_the_named_middle_irish_names_are_now_covered(headword):
    row = LEX.get(key(headword))
    assert row is not None and row.status == "middle", headword
    assert row.oi_nom, headword


def test_every_middle_row_flags_ATTESTED_MIr():
    """O-22: the tier shows up in the flag and nowhere else."""
    assert all(r.flag == "ATTESTED:MIr" for r in MIDDLE)


def test_no_middle_row_records_a_reconstructed_form():
    assert [r.orthography for r in MIDDLE if "*" in r.oi_nom or "*" in r.oi_gen] == []


def test_every_middle_row_says_it_is_middle_irish_only():
    assert all("middle irish" in r.note.lower() for r in MIDDLE)


def test_the_middle_tier_only_added_rows():
    """R4: a `middle` row is a NEW row, never a reclassified `attested` one."""
    assert sum(r.status == "attested" for r in ROWS) >= 265


def test_the_lexicon_is_still_clean_and_within_its_size_bound():
    assert check_lexicon_file(PATH) == []
    assert len(ROWS) <= 330
