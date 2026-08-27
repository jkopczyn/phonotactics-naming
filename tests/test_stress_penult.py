"""Plan Task 13: the `penult` stress procedure (sources/welsh/digest.md §4.1)."""
import pytest
from helpers import TABLE, w

from strands.dsl import parse_rules
from strands.stress import assign_stress
from strands.syllabify import syllabify

BASE = ("[inventory]\np t k b d ɡ m n l r s ʃ x a e i o u aː eː iː oː uː ə\n"
        "[syllable]\ntemplate = (C)(C)N(C)(C)\nonsets = any\ncodas = any\nsonority = off\n"
        "[stress]\nprocedure = penult\n")


@pytest.mark.parametrize("ipa,expected", [("pata", 0), ("patata", 1), ("pat", 0),
                                          ("patatata", 2)])
def test_penult(ipa, expected):
    rf = parse_rules(BASE, TABLE)
    assert assign_stress(syllabify(w(ipa), rf, TABLE), rf, TABLE).stress == expected


def test_penult_ignores_weight():
    # digest §4.1: "regardless of length or diachronic origin" [breit2019 pp.74-75]
    rf = parse_rules(BASE, TABLE)
    assert assign_stress(syllabify(w("paːtata"), rf, TABLE), rf, TABLE).stress == 1


def test_penult_recomputes_rather_than_carrying_source_stress():
    # digest §4.1: stress shifts rightward under suffixation; never carried from the source
    rf = parse_rules(BASE, TABLE)
    assert assign_stress(syllabify(w("ˈpatata"), rf, TABLE), rf, TABLE).stress == 1


def test_penult_trace_entry():
    rf = parse_rules(BASE, TABLE)
    out = assign_stress(syllabify(w("patata"), rf, TABLE), rf, TABLE)
    assert out.trace[-1].stage == "stress" and out.trace[-1].rule_id == "stress:penult"
