"""Task 16: the filter regression (spec §7, §11). A low rate is a finding, not a failure —
see the module docstring in oldirish.py."""

import json

import pytest
from helpers import ROOT, TABLE, irish, read_test_words, target

from strands.inputs import Entry, infer
from strands.lexicon import FORM_STATUSES, key, read_lexicon
from strands.oldirish import REVERSAL_CLASSES, filter_regression
from strands.regress import load_ratchet

IRISH = irish()
OI = target("old-irish")
LEX = read_lexicon()
RATCHET = ROOT / "tests" / "ratchets" / "old-irish.json"
ENTRIES = [
    infer(
        Entry(orthography=r["orthography"], ipa=r["ipa"], dialect=r.get("dialect") or "C"),
        IRISH,
        TABLE,
    )
    for r in read_test_words()
    if r["ipa"]
]
REPORT = filter_regression(ENTRIES, LEX, OI, IRISH, TABLE)


def test_the_denominator_is_the_measured_form_bearing_overlap():
    """O-31 / R1: 54, not draft 1's 74 — the 20 `none` hits have no oi_nom."""
    assert len(REPORT.rows) >= 50, len(REPORT.rows)
    assert all(LEX[key(r.orthography)].status in FORM_STATUSES for r in REPORT.rows)


def test_duplicate_keys_resolve_deterministically():
    """O-31: `niamh` has NO src:attested row, so the fallback is required."""
    assert len({r.orthography for r in REPORT.rows}) == len(REPORT.rows)
    again = filter_regression(ENTRIES, LEX, OI, IRISH, TABLE)
    assert again.rows == REPORT.rows


def test_every_row_compares_written_forms():
    """O-16: oi_nom is a spelling, so both the comparison and the distance are characters."""
    for r in REPORT.rows:
        assert r.expected == LEX[key(r.orthography)].oi_nom and isinstance(r.distance, int)


def test_both_rates_are_reported_and_ordered():
    assert 0.0 <= REPORT.rate(0) <= REPORT.rate(1) <= 1.0


def test_the_ratchet_holds():
    ratchet = load_ratchet("old-irish")
    assert REPORT.rate(0) >= ratchet["exact"] - 1e-9
    assert REPORT.rate(1) >= ratchet["lev1"] - 1e-9


def test_the_ratchet_file_records_the_denominator():
    data = json.loads(RATCHET.read_text(encoding="utf-8"))
    assert set(data) == {"exact", "lev1", "n"} and data["n"] == len(REPORT.rows)


def test_every_reversal_class_is_measured():
    by_class = REPORT.by_class()
    assert set(by_class) == set(REVERSAL_CLASSES)
    assert all(0 <= p <= t for p, t in by_class.values())


def test_the_ao_class_is_present_but_too_small_to_decide_O1():
    """R2: measured 4 in the ratcheted population; the 20 pairs are G2P-only."""
    passed, total = REPORT.by_class()["ao"]
    assert total >= 4, total


@pytest.mark.parametrize("cls", ["an-suffix", "r-stem"])
def test_the_invariant_classes_are_near_perfect(cls):
    """S19 / log finding 4: if the filter breaks THESE it is over-applying."""
    passed, total = REPORT.by_class()[cls]
    if total == 0:
        pytest.skip(f"no {cls} headwords in the overlap")
    assert passed >= total - 1, (passed, total)


def test_a_g2p_widens_the_population_without_moving_the_ratchet():
    g2p = pytest.importorskip("strands.g2p").g2p
    wide = filter_regression(ENTRIES, LEX, OI, IRISH, TABLE, g2p=g2p)
    assert len(wide.rows) > len(REPORT.rows)
    assert wide.rate(0, constructed=False) == REPORT.rate(0)
    assert any(r.constructed for r in wide.rows)
    assert wide.by_class()["ao"][1] >= 15  # R2: O1 is measurable only here
