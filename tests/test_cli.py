"""Plan Task 27: `strands run / explain / gallery / lint` (spec §6, §12.J; I-39)."""

import csv
import shutil

from helpers import FIX, ROOT

from strands.cli import main
from strands.pipeline import TARGETS


def _rows(path):
    return list(csv.DictReader(path.open(encoding="utf-8"), delimiter="\t"))


def test_run_writes_one_row_per_word_construction_strand(tmp_path):
    out = tmp_path / "o.tsv"
    assert (
        main(["run", str(FIX), "--strand", "all", "--construction", "DESC", "--out", str(out)]) == 0
    )
    rows = _rows(out)
    assert {r["strand"] for r in rows} == set(TARGETS)
    assert set(rows[0]) == {
        "orthography",
        "construction",
        "strand",
        "respelling",
        "ipa",
        "flags",
        "fallbacks",
        "assumptions",
    }
    assert {r["construction"] for r in rows} == {"DESC"}


def test_construction_all_includes_the_epithet_tags(tmp_path):
    out = tmp_path / "o.tsv"
    main(["run", str(FIX), "--strand", "arabic-egy", "--construction", "all", "--out", str(out)])
    rows = _rows(out)
    assert "DESC+ADJ" in {r["construction"] for r in rows}  # I-39 reachability
    assert {r["strand"] for r in rows} == {"arabic-egy"}


def test_run_is_deterministic(tmp_path):
    a, b = tmp_path / "a.tsv", tmp_path / "b.tsv"
    main(["run", str(FIX), "--out", str(a)])
    main(["run", str(FIX), "--out", str(b)])
    assert a.read_bytes() == b.read_bytes()


def test_run_without_out_prints_the_tsv(capsys):
    assert main(["run", str(FIX), "--strand", "welsh", "--construction", "DESC"]) == 0
    out = capsys.readouterr().out
    assert out.startswith("orthography\tconstruction\tstrand\t")


def test_run_rejects_an_unknown_strand_and_construction():
    assert main(["run", str(FIX), "--strand", "klingon"]) == 2
    assert main(["run", str(FIX), "--construction", "NOPE"]) == 2


def test_explain_prints_stages_rule_ids_and_citations(capsys):
    assert main(["explain", "ˈciəɾˠə", "--strand", "welsh"]) == 0
    out = capsys.readouterr().out
    assert "substitute" in out and "syllabify" in out and "->" in out and "[" in out


def test_explain_with_a_construction(capsys):
    assert main(["explain", "ʃaːn̪ˠ", "--strand", "dutch", "--construction", "VOC"]) == 0
    out = capsys.readouterr().out
    assert "VOC" in out and "respell" in out


def test_explain_rejects_an_unknown_strand():
    assert main(["explain", "kaː", "--strand", "klingon"]) == 2


def test_explain_requires_a_strand():
    assert main(["explain", "kaː"]) == 2


def test_gallery_emits_markdown(tmp_path):
    out = tmp_path / "g.md"
    assert main(["gallery", str(FIX), "--out", str(out)]) == 0
    text = out.read_text(encoding="utf-8")
    assert text.startswith("#")
    assert "Seán" in text
    assert "| welsh |" in text  # a column header names the strand


def test_gallery_shows_the_five_canon_names_verbatim(tmp_path):
    """Spec §12.J: the pre-existing strand-4 names are canon inputs, displayed in a
    reference row exactly as written and never adapted."""
    out = tmp_path / "g.md"
    main(["gallery", str(FIX), "--out", str(out)])
    text = out.read_text(encoding="utf-8")
    for name in ("Tchaeul", "Th'tysh", "Kas'queil", "Xelxyx", "Ysclyth"):
        assert name in text, name


def test_the_reference_row_is_not_produced_by_the_engine(monkeypatch):
    """Guard: render_gallery must not call adapt() for the reference row."""
    from strands import pipeline

    calls = []
    real = pipeline.adapt
    monkeypatch.setattr(pipeline, "adapt", lambda *a, **k: calls.append(a) or real(*a, **k))
    from strands.gallery import REFERENCE_NAMES, reference_row

    row = reference_row()
    assert calls == [] and "Kas'queil" in row
    assert REFERENCE_NAMES == ("Tchaeul", "Th'tysh", "Kas'queil", "Xelxyx", "Ysclyth")


def test_gallery_is_deterministic(tmp_path):
    a, b = tmp_path / "a.md", tmp_path / "b.md"
    main(["gallery", str(FIX), "--out", str(a)])
    main(["gallery", str(FIX), "--out", str(b)])
    assert a.read_bytes() == b.read_bytes()


def test_lint_lists_inferred_fields(capsys):
    assert main(["lint", str(FIX)]) == 0
    assert "declension" in capsys.readouterr().out


def test_lint_accept_rewrites_the_file(tmp_path):
    dst = tmp_path / "in.tsv"
    shutil.copy(FIX, dst)
    before = dst.read_text(encoding="utf-8")
    assert main(["lint", str(dst), "--accept"]) == 0
    assert dst.read_text(encoding="utf-8") != before


def test_an_unreadable_orthography_is_skipped_with_a_note(tmp_path):
    """Since milestone 8 a missing `ipa` is constructed, so `skipped:no-ipa` is left only for
    an orthography `g2p` cannot read — and the row is kept, never an error."""
    src = tmp_path / "in.tsv"
    src.write_text("orthography\tipa\n123\t\nSeán\tʃaːn̪ˠ\n", encoding="utf-8")
    out = tmp_path / "o.tsv"
    assert main(["run", str(src), "--out", str(out)]) == 0
    rows = _rows(out)
    skipped = [r for r in rows if "skipped:no-ipa" in r["assumptions"]]
    assert skipped and all(r["ipa"] == "" and r["respelling"] == "" for r in skipped)
    assert any("skipped" not in r["assumptions"] for r in rows)


def test_a_constructed_ipa_row_is_processed_normally(tmp_path):
    src = tmp_path / "in.tsv"
    src.write_text("orthography\tipa\nAisling\t\n", encoding="utf-8")
    out = tmp_path / "o.tsv"
    assert main(["run", str(src), "--out", str(out)]) == 0
    rows = _rows(out)
    assert rows and all("ipa:constructed" in r["assumptions"] for r in rows)
    assert all(r["respelling"] for r in rows if "skipped" not in r["assumptions"])


def test_missing_slot_is_skipped_with_a_note(tmp_path):
    # a two-slot template cannot be built from one entry: skipped, never an error
    out2 = tmp_path / "o2.tsv"
    assert (
        main(["run", str(FIX), "--strand", "welsh", "--construction", "ADJ", "--out", str(out2)])
        == 0
    )
    rows2 = _rows(out2)
    assert all("skipped:" in r["assumptions"] for r in rows2)
    assert all(
        "skipped:missing-slot-ADJ" in r["assumptions"]
        for r in rows2
        if "no-ipa" not in r["assumptions"]
    )


def test_run_reports_a_missing_input_file(tmp_path):
    assert main(["run", str(tmp_path / "nope.tsv")]) == 1


def test_explain_rejects_construction_all():
    """`explain` is one construction only: `all` is a usage error (2), never a traceback."""
    assert main(["explain", "kaː", "--strand", "welsh", "--construction", "all"]) == 2


# ---- runtime-error boundary (spec §2: an unknown segment is a hard error naming the word and
#      the offending substring; module docstring: runtime failures exit 1, no traceback) -------


def _bad_ipa(tmp_path):
    src = tmp_path / "bad.tsv"
    src.write_text("orthography\tipa\nSeán\tʃaːn̪ˠ\nBad\tQ\n", encoding="utf-8")
    return src


def test_run_reports_an_unknown_segment_naming_the_word(tmp_path, capsys):
    assert main(["run", str(_bad_ipa(tmp_path)), "--strand", "welsh"]) == 1
    err = capsys.readouterr().err
    assert "Bad" in err and "'Q'" in err and "Traceback" not in err


def test_gallery_reports_an_unknown_segment_naming_the_word(tmp_path, capsys):
    assert main(["gallery", str(_bad_ipa(tmp_path))]) == 1
    err = capsys.readouterr().err
    assert "Bad" in err and "'Q'" in err


def test_lint_reports_an_unknown_segment_naming_the_word(tmp_path, capsys):
    assert main(["lint", str(_bad_ipa(tmp_path))]) == 1
    err = capsys.readouterr().err
    assert "Bad" in err and "'Q'" in err


def test_unwritable_out_is_a_runtime_error(tmp_path, capsys):
    out = tmp_path / "no-such-dir" / "o.tsv"
    assert (
        main(["run", str(FIX), "--strand", "welsh", "--construction", "DESC", "--out", str(out)])
        == 1
    )
    assert "no-such-dir" in capsys.readouterr().err
    assert main(["gallery", str(FIX), "--out", str(out)]) == 1
    assert "no-such-dir" in capsys.readouterr().err


def test_cli_entry_point_prints_no_traceback(tmp_path):
    """The same boundary through the installed console script."""
    import subprocess
    import sys

    proc = subprocess.run(
        [sys.executable, "-m", "strands.cli", "run", str(_bad_ipa(tmp_path)), "--strand", "welsh"],
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 1, proc.stderr
    assert "Traceback" not in proc.stderr and "Bad" in proc.stderr


def test_check_accepts_a_lexicon_tsv():
    from strands.cli import main

    assert main(["check", str(ROOT / "rules" / "old-irish-lexicon.tsv")]) == 0


# ---- Old Irish (plan Task 17; O-17, O-23) ------------------------------------------------------


def test_run_accepts_the_fifth_strand(tmp_path):
    from strands.cli import main

    out = tmp_path / "out.tsv"
    assert main(["run", str(FIX), "--strand", "old-irish", "--out", str(out)]) == 0
    assert "old-irish" in out.read_text(encoding="utf-8")


def test_a_construction_the_strand_lacks_is_a_skipped_row_not_an_error(tmp_path):
    """O-17: PATRO_NI for old-irish, MAEL for welsh — both are skips."""
    from strands.cli import main

    out = tmp_path / "out.tsv"
    assert (
        main(["run", str(FIX), "--strand", "all", "--construction", "all", "--out", str(out)]) == 0
    )
    assert "skipped:construction-not-in-strand" in out.read_text(encoding="utf-8")


def test_explain_warns_when_no_orthography_is_given_for_old_irish(capsys):
    """O-23: lookup keys on orthography, which a bare IPA argument cannot supply."""
    from strands.cli import main

    assert main(["explain", "nʲiəl̪ˠ", "--strand", "old-irish"]) == 0
    out = capsys.readouterr().out
    assert "RETRO" in out and "--orthography" in out


def test_explain_without_orthography_is_the_pure_retro_path_even_for_a_lexicon_key(capsys):
    """review-oi-final #1: the bare IPA argument doubles as the orthography, so an IPA that
    happens to be a lexicon key (*mac*) would hit while the note says it cannot. Lookup is
    disabled outright, so the interface is not input-dependent."""
    from strands.cli import main

    assert main(["explain", "mac", "--strand", "old-irish"]) == 0
    out = capsys.readouterr().out
    assert "RETRO" in out and "ATTESTED" not in out and "--orthography" in out


def test_explain_rejects_a_construction_whose_slots_it_cannot_fill(capsys):
    """review-oi-final #2: COLOUR/ADJ/OF/COMPOUND need a second slot that `explain` has no
    way to supply; that is a usage error, not a traceback."""
    from strands.cli import main

    rc = main(
        [
            "explain",
            "d̪ˠʊw",
            "--strand",
            "old-irish",
            "--orthography",
            "dubh",
            "--construction",
            "COLOUR",
        ]
    )
    err = capsys.readouterr().err
    assert rc == 2
    assert "Traceback" not in err and "NAME" in err and "COLOUR" in err


def test_explain_missing_slot_is_a_usage_error_in_the_modern_strands_too(capsys):
    from strands.cli import main

    rc = main(["explain", "nʲiəl̪ˠ", "--strand", "welsh", "--construction", "ADJ"])
    err = capsys.readouterr().err
    assert rc == 2 and "Traceback" not in err and "ADJ" in err


def test_explain_uses_the_orthography_for_the_lookup(capsys):
    from strands.cli import main

    assert main(["explain", "nʲiəl̪ˠ", "--strand", "old-irish", "--orthography", "Niall"]) == 0
    assert "ATTESTED" in capsys.readouterr().out


def test_check_passes_on_the_old_irish_rule_file():
    from strands.cli import main

    assert main(["check", str(ROOT / "rules" / "old-irish.rules")]) == 0


# ---- word: one spelling in, all strands out, no file ------------------------------------------


def test_word_takes_a_spelling_and_prints_every_strand(capsys):
    assert main(["word", "indeagó"]) == 0
    out = capsys.readouterr().out
    assert "ipa:constructed" in out  # g2p built the source IPA
    for name in TARGETS:
        assert name in out
    assert "injygo" in out  # the README's welsh line


def test_word_trace_needs_one_strand_and_prints_the_derivation(capsys):
    assert main(["word", "Niall", "--strand", "old-irish", "--trace"]) == 0
    out = capsys.readouterr().out
    assert "ATTESTED" in out  # spelling is the lexicon key
    assert "->" in out
    assert main(["word", "Niall", "--trace"]) == 2  # all strands + trace is a usage error


def test_word_rejects_unknown_strand_and_unfillable_construction(capsys):
    assert main(["word", "Niall", "--strand", "klingon"]) == 2
    rc = main(["word", "Niall", "--strand", "welsh", "--construction", "ADJ"])
    err = capsys.readouterr().err
    assert rc == 2 and "Traceback" not in err and "ADJ" in err


def test_word_save_writes_the_lint_accept_tsv(tmp_path, capsys):
    """--save FILE is byte-identical to `lint --accept` on the one-column file."""
    ref = tmp_path / "ref.tsv"
    ref.write_text("orthography\nindeagó\n", encoding="utf-8")
    main(["lint", str(ref), "--accept"])
    out = tmp_path / "saved.tsv"
    assert main(["word", "indeagó", "--save", str(out)]) == 0
    assert out.read_bytes() == ref.read_bytes()
    assert main(["word", "--save", str(out), "indeagó"]) == 0  # flag before the positional


def test_word_save_defaults_to_a_timestamped_name(tmp_path, monkeypatch, capsys):
    import re

    monkeypatch.chdir(tmp_path)
    assert main(["word", "indeagó", "--save"]) == 0
    (saved,) = tmp_path.iterdir()
    assert re.fullmatch(r"\d{8}-\d{6}-indeagó\.tsv", saved.name)
    assert saved.name in capsys.readouterr().err
    assert "ipa\t" in saved.read_text(encoding="utf-8")


def test_explain_save_keeps_the_given_ipa(tmp_path, capsys):
    out = tmp_path / "s.tsv"
    assert (
        main(
            ["explain", "nʲiəl̪ˠ", "--strand", "welsh", "--orthography", "Niall", "--save", str(out)]
        )
        == 0
    )
    rows = _rows(out)
    assert rows == [
        dict(
            orthography="Niall",
            ipa="nʲiəl̪ˠ",
            dialect="C",
            gender="m",
            declension="m1",
            gen_ipa=rows[0]["gen_ipa"],
        )
    ]
