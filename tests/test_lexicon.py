"""Task 2: lexicon schema and validation (spec §3, §7, §10; O-18, O-19, O-21, O-22)."""

import pytest

from strands.check import check_lexicon_file
from strands.lexicon import (
    FORM_STATUSES,
    KINDS,
    LEXICON_COLUMNS,
    STATUSES,
    STEMS,
    LexEntry,
    LexiconError,
    default_lexicon_path,
    key,
    read_lexicon,
    read_rows,
)

HEADER = "\t".join(LEXICON_COLUMNS)


def write(tmp_path, *rows):
    path = tmp_path / "lex.tsv"
    path.write_text("\n".join([HEADER, *rows]) + "\n", encoding="utf-8")
    return path


def row(**kw):
    kw.setdefault("status", "attested")
    return "\t".join(kw.get(c, "") for c in LEXICON_COLUMNS)


ATTESTED = dict(
    orthography="Niall",
    oi_nom="Níall",
    oi_gen="Néill",
    stem="o",
    gender="m",
    source="https://en.wiktionary.org/wiki/N%C3%ADall",
)
LOAN = dict(
    orthography="Seán",
    status="none",
    kind="loan",
    source="https://en.wiktionary.org/wiki/Se%C3%A1n",
    note="< Old French Jehan",
)
LATE = dict(
    orthography="Saoirse",
    status="none",
    kind="late",
    source="https://en.wiktionary.org/wiki/saoirse",
    note="20th-c. coinage",
)
MIDDLE = dict(
    orthography="Tadhg",
    oi_nom="Tadg",
    stem="o",
    gender="m",
    status="middle",
    source="https://en.wiktionary.org/wiki/Tadg",
)


def codes(path, severity="error"):
    return sorted(
        e.code for e in check_lexicon_file(path) if severity is None or e.severity == severity
    )


def test_the_column_list_is_the_spec_3_plus_10_schema():
    assert LEXICON_COLUMNS == (
        "orthography",
        "oi_nom",
        "oi_gen",
        "stem",
        "gender",
        "status",
        "kind",
        "source",
        "note",
    )
    assert STEMS == ("o", "ā", "i", "u", "n", "dental", "velar", "r", "s", "indecl", "irregular")
    assert STATUSES == ("attested", "middle", "none") and KINDS == ("loan", "late")
    assert FORM_STATUSES == ("attested", "middle")


def test_the_four_row_shapes_all_validate(tmp_path):
    assert codes(write(tmp_path, row(**ATTESTED), row(**LOAN), row(**LATE), row(**MIDDLE))) == []


@pytest.mark.parametrize(
    "fields,expected",
    [
        (ATTESTED, "ATTESTED"),
        (MIDDLE, "ATTESTED:MIr"),
        (LOAN, "RETRO:loan"),
        (LATE, "RETRO:late"),
    ],
)
def test_each_status_maps_to_its_result_flag(fields, expected):
    """spec §2 and §10; O-18, O-22. Task 12 reads exactly this property."""
    assert LexEntry(**fields).flag == expected


def test_the_key_is_nfc_case_folded(tmp_path):
    lex = read_lexicon(write(tmp_path, row(**ATTESTED)))
    assert key("NIALL") in lex and lex[key("niall")].oi_nom == "Níall"


def test_duplicate_keys_are_rejected(tmp_path):
    assert "LEX_DUPLICATE_KEY" in codes(
        write(tmp_path, row(**ATTESTED), row(**dict(ATTESTED, orthography="NIALL")))
    )


def test_every_row_must_cite_a_source(tmp_path):
    for fields in (ATTESTED, LOAN, MIDDLE):
        assert "LEX_NO_SOURCE" in codes(write(tmp_path, row(**dict(fields, source=""))))


def test_a_source_must_look_like_a_url_or_a_page_citation(tmp_path):
    assert "LEX_SOURCE_SHAPE" in codes(write(tmp_path, row(**dict(ATTESTED, source="eDIL"))))
    for good in (
        "https://dil.ie/33021",
        "digest §10.6",
        "strachan1909 p.9",
        "pokorny1914 p.60 §134",
    ):
        assert codes(write(tmp_path, row(**dict(ATTESTED, source=good)))) == []


def test_a_form_bearing_row_needs_a_form(tmp_path):
    for fields in (ATTESTED, MIDDLE):
        assert "LEX_ATTESTED_NO_NOM" in codes(write(tmp_path, row(**dict(fields, oi_nom=""))))


def test_kind_is_meaningless_on_a_form_bearing_row(tmp_path):
    assert "LEX_KIND_ON_FORM_ROW" in codes(write(tmp_path, row(**dict(ATTESTED, kind="loan"))))


def test_the_widened_stem_vocabulary_is_accepted(tmp_path):
    """spec §10: velar (*rí ~ ríg*), r (*athair*), s (*tech*), indecl."""
    for stem in ("velar", "r", "s", "indecl"):
        assert codes(write(tmp_path, row(**dict(ATTESTED, stem=stem)))) == []
    assert "LEX_STEM" in codes(write(tmp_path, row(**dict(ATTESTED, stem="io"))))


@pytest.mark.parametrize(
    "bad,code",
    [
        (dict(LOAN, kind=""), "LEX_NONE_NO_KIND"),
        (dict(LOAN, oi_nom="Seán"), "LEX_NONE_HAS_FORM"),
        (dict(ATTESTED, stem="irregular", oi_gen=""), "LEX_IRREGULAR_NO_GEN"),
    ],
)
def test_the_three_former_task3_gaps_are_errors(tmp_path, bad, code):
    """R3a: these were warnings while the harvest was a Task 3 backlog (29, 1 and 11 rows);
    Task 3 closed it and promoted all three to `error`."""
    assert code in codes(write(tmp_path, row(**bad)))


def test_a_row_that_still_owes_a_stem_or_gender_is_a_warning(tmp_path):
    path = write(tmp_path, row(**dict(ATTESTED, stem="")))
    assert codes(path) == [] and "LEX_NEEDS_TASK3" in codes(path, severity="warning")


@pytest.mark.parametrize("prefix", ["no nominal paradigm: adjective", "unattested: stem class"])
def test_a_blank_that_explains_itself_is_not_a_warning(tmp_path, prefix):
    """Task 3: adjectives, numerals and prefixes have no nominal paradigm; a noun whose class
    the sources do not show is inferred at runtime (O-33). Neither is a backlog."""
    path = write(tmp_path, row(**dict(ATTESTED, stem="", note=prefix + " x")))
    assert codes(path) == [] and codes(path, severity="warning") == []


@pytest.mark.parametrize("cells", [8, 10])
def test_a_row_with_the_wrong_cell_count_is_an_error(tmp_path, cells):
    """The schema applies to every row, not only the header: a short row is not padded and a
    long one is not truncated silently (review oi-data-aligner finding 4)."""
    good = row(**ATTESTED).split("\t")
    bad = good[:cells] if cells < len(good) else good + ["stray"]
    path = write(tmp_path, "\t".join(bad))
    assert "LEX_ROW_SHAPE" in codes(path)
    assert [e.line for e in check_lexicon_file(path) if e.code == "LEX_ROW_SHAPE"] == [2]
    with pytest.raises(LexiconError):
        read_lexicon(path)


def test_a_wrong_header_is_reported_not_guessed(tmp_path):
    path = tmp_path / "lex.tsv"
    path.write_text("orthography\toi_nom\n", encoding="utf-8")
    assert "LEX_HEADER" in codes(path)


# ---- the committed file (lower bounds only, R4) -------------------------------------------

PATH = default_lexicon_path()
FILE_HEADER, FILE_ROWS = read_rows(PATH)


def test_the_committed_lexicon_has_no_errors():
    assert [e for e in check_lexicon_file(PATH) if e.severity == "error"] == []


def test_the_committed_lexicon_is_the_harvested_one():
    """Lower bounds: Task 3 may remove rows and Task 4 adds them (R4)."""
    assert len(FILE_ROWS) >= 290
    assert sum(r.status in FORM_STATUSES for r in FILE_ROWS) >= 260
    assert sum(r.status == "none" for r in FILE_ROWS) >= 25
    assert sum(bool(r.oi_gen) for r in FILE_ROWS) >= 160
    assert len({key(r.orthography) for r in FILE_ROWS}) == len(FILE_ROWS)  # O-19: no dups
