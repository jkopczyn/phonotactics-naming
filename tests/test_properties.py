"""Plan Task 28 (spec §8 layer 5): cross-target property checks over every test word."""
import pytest

from helpers import TABLE, entry_of, irish, read_allow_file, read_test_words
from strands.pipeline import TARGETS, load_target, run_entry

IRISH = irish()
ROWS = read_test_words()
ENTRIES = [entry_of(row) for row in ROWS]
RF = {name: load_target(name, TABLE) for name in TARGETS}


def _results(name):
    for row, e in zip(ROWS, ENTRIES):
        yield row, run_entry(e, "DESC", IRISH, RF[name], TABLE)


@pytest.mark.parametrize("name", TARGETS)
def test_determinism_across_two_runs(name):
    for e in ENTRIES:
        assert run_entry(e, "DESC", IRISH, RF[name], TABLE) == \
            run_entry(e, "DESC", IRISH, RF[name], TABLE)


@pytest.mark.parametrize("name", TARGETS)
def test_every_output_segment_is_in_the_target_inventory(name):
    inventory = set(RF[name].inventory)
    for row, result in _results(name):
        for word in result.words:
            assert set(word.segments) <= inventory, (name, row["orthography"], word.segments)


def test_no_unrepaired_outside_the_allow_file():
    allowed = read_allow_file()
    bad = [(name, row["orthography"])
           for name in TARGETS
           for row, result in _results(name)
           if "UNREPAIRED" in result.flags and (name, row["orthography"]) not in allowed]
    assert bad == [], bad


@pytest.mark.parametrize("name", TARGETS)
def test_every_word_gets_exactly_one_primary_stress(name):
    for row, result in _results(name):
        for word in result.words:
            assert word.stress is not None, (name, row["orthography"])
            assert 0 <= word.stress < len(word.syllables), (name, row["orthography"])


@pytest.mark.parametrize("name", TARGETS)
def test_traces_are_never_empty(name):
    assert run_entry(ENTRIES[0], "DESC", IRISH, RF[name], TABLE).trace
