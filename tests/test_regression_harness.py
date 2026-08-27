"""Plan Task 22: the attested-data regression harness (Modes E and C), its I-36 cleaning,
the error bucket (I-24) and the ratchet."""
import json

import pytest
from helpers import FIXTURES, TABLE, rules_exist

from strands.regress import (
    RegressionReport,
    RegressionRow,
    assert_ratchet,
    edit_distance,
    load_ratchet,
    read_attested,
    run_regression,
    write_ratchet,
)

TOY = FIXTURES / "toy-target.rules"

FAILING_ROW = RegressionRow(source_form="x", source_ipa="", target_form="y", target_ipa="ka",
                            provenance="none", mode="C", passed=False, got="ka", distance=1)
PASSING_ROW = RegressionRow(source_form="x", source_ipa="", target_form="y", target_ipa="ka",
                            provenance="none", mode="C", passed=True, got="ka", distance=0)


def test_row_counts_match_the_committed_data():
    """R10: draft 1 had three of four denominators wrong."""
    assert len(read_attested("georgian")) == 143
    assert len(read_attested("arabic-egy")) == 301        # 312 - 11 PREDICTED-NOT-ATTESTED
    assert len(read_attested("welsh")) == 751
    assert len(read_attested("dutch")) == 90


def test_target_ipa_denominators():
    def n(t):
        return len([r for r in read_attested(t) if r["target_ipa"].strip()])
    assert n("georgian") == 122 and n("arabic-egy") == 279
    assert n("welsh") == 19 and n("dutch") == 67


def test_mode_e_is_dutch_only():
    def both(t):
        return len([r for r in read_attested(t)
                    if r["source_ipa"].strip() and r["target_ipa"].strip()])
    assert both("dutch") == 32
    assert both("georgian") == both("arabic-egy") == both("welsh") == 0


def test_predicted_rows_are_dropped():
    assert not any(r["note"].startswith("PREDICTED-NOT-ATTESTED")
                   for r in read_attested("arabic-egy"))


def test_untokenizable_rows_go_to_the_error_bucket_not_an_exception():
    """I-24/I-36: a SegmentError in attested data is counted, never raised."""
    rep = run_regression("georgian", TABLE, rule_file=TOY)
    assert "error" in rep.counts()
    assert rep.counts()["error"] >= 0
    for row in rep.rows:
        if row.mode == "error":
            assert row.reason, row


def test_cleaning_pass_rescues_ascii_spellings():
    rep = run_regression("dutch", TABLE, rule_file=TOY)
    assert rep.counts().get("error", 0) < 30      # draft-1 measurement: 30/67 before cleaning


def test_every_row_is_reported_once_with_a_mode():
    rep = run_regression("dutch", TABLE, rule_file=TOY)
    assert len(rep.rows) == 90
    assert sum(rep.counts().values()) == 90
    assert set(rep.counts()) == {"E", "C", "skip", "error"}
    assert rep.counts()["skip"] == 23                      # 90 - 67 with target_ipa
    assert rep.counts()["E"] + rep.counts()["C"] + rep.counts()["error"] == 67
    assert not rep.mode_e_is_empty()


def test_mode_e_is_empty_for_one_sided_data():
    rep = run_regression("welsh", TABLE, rule_file=TOY)
    assert rep.mode_e_is_empty()
    assert rep.counts()["E"] == 0


def test_rate_is_a_fraction_of_rows_in_that_mode():
    rep = run_regression("dutch", TABLE, rule_file=TOY)
    assert 0.0 <= rep.rate("C") <= 1.0
    assert 0.0 <= rep.rate("E") <= 1.0
    two = RegressionReport(target="x", rows=(FAILING_ROW, PASSING_ROW))
    assert two.rate("C") == 0.5
    assert two.rate("E") == 0.0                             # no rows: 0.0, never a ZeroDivisionError


def test_summary_names_mode_c_as_conformance_only():
    rep = run_regression("dutch", TABLE, rule_file=TOY)
    assert "conformance" in rep.summary().lower()
    assert "dutch" in rep.summary()


def test_mode_c_passes_a_conforming_form_and_fails_a_nonconforming_one():
    """The toy target: inventory p b t d k ɡ f s ʃ x h m n l r j w / a e i o u aː iː oː,
    onsets include `tr`, `sp`; stress = penult."""
    rows = {r.target_ipa: r for r in run_regression("dutch", TABLE, rule_file=TOY).rows}
    # a row we synthesize through the same code path: check via helper on a Report built by
    # the harness's row runner
    from strands.dsl import parse_rules_file
    from strands.regress import _run_row
    rf = parse_rules_file(TOY, TABLE)
    ok = _run_row({"source_form": "", "source_ipa": "", "target_form": "", "target_ipa": "trapa",
                   "provenance": ""}, "dutch", rf, TABLE)
    assert ok.mode == "C" and ok.passed, ok
    off = _run_row({"source_form": "", "source_ipa": "", "target_form": "", "target_ipa": "ʒapa",
                    "provenance": ""}, "dutch", rf, TABLE)
    # ʒ is marginal, so inventory-legal (I-23) — but the toy's complete onset set (§12.D)
    # lacks it, so the only failure is the illegal onset: distance exactly 1.
    assert off.mode == "C" and not off.passed and off.distance == 1, off
    bad_seg = _run_row({"source_form": "", "source_ipa": "", "target_form": "",
                        "target_ipa": "ɣapa", "provenance": ""}, "dutch", rf, TABLE)
    # ɣ is off-inventory AND an illegal onset: both counted.
    assert bad_seg.mode == "C" and not bad_seg.passed and bad_seg.distance == 2, bad_seg
    bad_syl = _run_row({"source_form": "", "source_ipa": "", "target_form": "",
                        "target_ipa": "ptapa", "provenance": ""}, "dutch", rf, TABLE)  # pt onset
    assert bad_syl.mode == "C" and not bad_syl.passed
    good_stress = _run_row({"source_form": "", "source_ipa": "", "target_form": "",
                            "target_ipa": "ˈtrapa", "provenance": ""}, "dutch", rf, TABLE)
    assert good_stress.passed
    bad_stress = _run_row({"source_form": "", "source_ipa": "", "target_form": "",
                           "target_ipa": "traˈpa", "provenance": ""}, "dutch", rf, TABLE)
    assert not bad_stress.passed
    assert rows                                              # the real data went through too


def test_mode_e_compares_after_stripping_marks_the_row_lacks():
    from strands.dsl import parse_rules_file
    from strands.regress import _run_row
    rf = parse_rules_file(TOY, TABLE)
    row = {"source_form": "", "source_ipa": "trapa", "target_form": "", "target_ipa": "trapa",
           "provenance": ""}
    res = _run_row(row, "dutch", rf, TABLE)
    assert res.mode == "E" and res.passed and res.distance == 0, res
    row = {"source_form": "", "source_ipa": "trapa", "target_form": "", "target_ipa": "trapo",
           "provenance": ""}
    res = _run_row(row, "dutch", rf, TABLE)
    assert res.mode == "E" and not res.passed and res.distance == 1, res


def test_ratchet_failure_is_loud(monkeypatch):
    rep = RegressionReport(target="x", rows=(FAILING_ROW,))
    monkeypatch.setattr("strands.regress.load_ratchet", lambda t: {"C": 1.0})
    with pytest.raises(AssertionError):
        assert_ratchet(rep)


def test_ratchet_passes_when_rate_holds_or_no_ratchet_exists(monkeypatch):
    rep = RegressionReport(target="x", rows=(PASSING_ROW,))
    monkeypatch.setattr("strands.regress.load_ratchet", lambda t: {"C": 1.0})
    assert_ratchet(rep)
    monkeypatch.setattr("strands.regress.load_ratchet", lambda t: {})
    assert_ratchet(RegressionReport(target="x", rows=(FAILING_ROW,)))
    assert load_ratchet("no-such-target") == {}


def test_ratchet_tolerance(monkeypatch):
    rep = RegressionReport(target="x", rows=(FAILING_ROW, PASSING_ROW))
    monkeypatch.setattr("strands.regress.load_ratchet", lambda t: {"C": 0.6})
    with pytest.raises(AssertionError):
        assert_ratchet(rep)
    assert_ratchet(rep, tolerance=0.1)


def test_write_ratchet_round_trips(tmp_path, monkeypatch):
    monkeypatch.setattr("strands.regress.RATCHET_DIR", tmp_path)
    rep = RegressionReport(target="x", rows=(FAILING_ROW, PASSING_ROW))
    write_ratchet(rep)
    data = json.loads((tmp_path / "x.json").read_text(encoding="utf-8"))
    assert data == {"C": 0.5}                                # only modes with rows
    assert load_ratchet("x") == {"C": 0.5}
    assert_ratchet(rep)


def test_write_ratchet_never_records_a_floor_above_the_rate(tmp_path, monkeypatch):
    """A 2/3 report must not be saved as 0.6667 and then fail its own assert_ratchet
    (review-targets fix 3): the stored floor is <= the exact rate."""
    monkeypatch.setattr("strands.regress.RATCHET_DIR", tmp_path)
    rep = RegressionReport(target="x", rows=(PASSING_ROW, PASSING_ROW, FAILING_ROW))
    write_ratchet(rep)
    assert load_ratchet("x")["C"] <= rep.rate("C")
    assert_ratchet(rep)


def test_edit_distance_is_reported():
    assert edit_distance(("k", "a", "l", "b"), ("k", "a", "l", "p")) == 1
    assert edit_distance((), ("a",)) == 1
    assert edit_distance(("a", "b"), ("a", "b")) == 0
    assert edit_distance(("a", "b", "c"), ("b", "c")) == 1


@pytest.mark.skipif(not rules_exist("dutch"), reason="dutch.rules lands in Task 26")
def test_real_rule_file_runs():
    assert run_regression("dutch", TABLE).counts()
