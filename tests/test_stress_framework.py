"""Plan Task 12: stress package — registry, syllable weight, `initial`, `keep-source`."""

import pytest
from helpers import TABLE, w

from strands.dsl import parse_rules
from strands.stress import PROCEDURES, StressError, assign_stress, syllable_weight
from strands.stress.params import PROCEDURE_PARAMS
from strands.syllabify import syllabify

BASE = (
    "[inventory]\np t k a aː i n s\n[syllable]\ntemplate = (C)N(C)(C)\nonsets = p t k n s\n"
    "codas = p t k n s\nsonority = off\n"
)


def stressed(src, ipa):
    rf = parse_rules(src, TABLE)
    return assign_stress(syllabify(w(ipa), rf, TABLE), rf, TABLE)


def test_initial_stresses_syllable_zero():
    out = stressed(BASE + "[stress]\nprocedure = initial\n", "patapa")
    assert out.stress == 0 and out.ipa().startswith("ˈ")


def test_initial_on_a_monosyllable():
    assert stressed(BASE + "[stress]\nprocedure = initial\n", "pat").stress == 0


def test_initial_mark_off_still_sets_stress_but_records_the_param():
    rf = parse_rules(BASE + "[stress]\nprocedure = initial\nmark = off\n", TABLE)
    out = assign_stress(syllabify(w("pata"), rf, TABLE), rf, TABLE)
    assert out.stress == 0 and rf.stress.params["mark"] == "off"


def test_keep_source_preserves_the_incoming_mark():
    assert stressed(BASE + "[stress]\nprocedure = keep-source\n", "paˈta").stress == 1


def test_keep_source_defaults_to_initial_when_unmarked():
    assert stressed(BASE + "[stress]\nprocedure = keep-source\n", "pata").stress == 0


def test_trace_entry():
    out = stressed(BASE + "[stress]\nprocedure = initial\n", "pata")
    assert out.trace[-1].stage == "stress" and out.trace[-1].rule_id == "stress:initial"


def test_syllable_weight_counts_nuclei():
    rf = parse_rules(BASE + "nuclei = ai\n[stress]\nprocedure = initial\n", TABLE)
    out = syllabify(w("pai"), rf, TABLE)
    assert syllable_weight(out, 0, TABLE) == "heavy"  # branching nucleus, open syllable


def test_weight_classes():
    rf = parse_rules(BASE + "[stress]\nprocedure = initial\n", TABLE)
    out = syllabify(w("patakaːnt"), rf, TABLE)
    assert {syllable_weight(out, i, TABLE) for i in range(len(out.syllables))} <= {
        "light",
        "heavy",
        "superheavy",
    }


def test_weight_each_class():
    rf = parse_rules(BASE + "[stress]\nprocedure = initial\n", TABLE)
    out = syllabify(w("pa.taː.pan.taːn.pant"), rf, TABLE)
    assert [syllable_weight(out, i, TABLE) for i in range(5)] == [
        "light",
        "heavy",
        "heavy",
        "superheavy",
        "superheavy",
    ]


def test_unknown_procedure_raises():
    with pytest.raises((StressError, Exception)):
        stressed(BASE + "[stress]\nprocedure = wibble\n", "pata")


def test_assign_stress_rejects_unregistered_procedure_directly():
    from dataclasses import replace

    from strands.dsl import StressSpec

    rf = parse_rules(BASE + "[stress]\nprocedure = initial\n", TABLE)
    bogus = replace(rf, stress=StressSpec("wibble", {}))
    with pytest.raises(StressError):
        assign_stress(syllabify(w("pata"), rf, TABLE), bogus, TABLE)


def test_registry_contains_this_tasks_procedures():
    assert {"initial", "keep-source"} <= set(PROCEDURES)


def test_params_registry_is_the_single_source_of_truth():
    assert PROCEDURE_PARAMS["penult"] == frozenset()
    assert "window" in PROCEDURE_PARAMS["dutch-weight"]
