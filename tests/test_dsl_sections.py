import pytest
from helpers import FIXTURES, TABLE

from strands.dsl import ParseError, parse_rules, parse_rules_file

MINI = parse_rules_file(FIXTURES / "mini.rules", TABLE)

def test_template_uses_the_nucleus_slot():
    assert MINI.syllable.template == (("C", True), ("C", True), ("N", False),
                                      ("C", True), ("C", True))

def test_nuclei_are_parsed_as_segment_sequences():
    assert ("a", "i") in MINI.syllable.nuclei and ("a", "u") in MINI.syllable.nuclei

def test_onsets_are_a_complete_set_including_singletons():
    s = MINI.syllable
    assert ("p",) in s.onset_set and ("p", "l") in s.onset_set     # spec §12.D
    assert s.onset_required is False

def test_onsets_preserve_file_order_for_cluster_fallback_tie_breaks():
    """Spec §12.E breaks ties by list order, so the ordered tuple is the authority and
    `onset_set` is only a membership index."""
    s = MINI.syllable
    assert s.onsets[:3] == (("p",), ("b",), ("t",))
    assert frozenset(s.onsets) == s.onset_set

def test_codas_and_appendix_and_domain_and_sonority():
    s = MINI.syllable
    assert ("s", "t") in s.coda_set and s.appendix == ("s", "t")
    assert s.domain == "word" and s.sonority is True

def test_tiers_are_recorded():
    assert MINI.syllable.onset_tiers[("p", "l")] == "A"

def test_bans_are_context_sequences():
    assert len(MINI.syllable.bans) == 1 and len(MINI.syllable.bans[0]) == 4

def test_stress_section():
    assert MINI.stress.procedure == "penult" and MINI.stress.params == {}

def test_epithets():
    e = MINI.epithets["NISBA"]
    assert e.form == ("i",) and [c.atom for c in e.left] == ["$"]

def test_respell_quoted_replacement():
    from strands.dsl import QuotedText
    assert MINI.sections["respell"][0].replacement == (QuotedText("sh"),)

def test_respell_may_not_contain_mark_cleanup_rules():
    """I-8/§12.C: marks are stripped in code; `. -> ""` is a parse error."""
    with pytest.raises(ParseError):
        parse_rules('[inventory]\np\n[respell]\n. -> ""\n', TABLE)

def test_cluster_fallback_directive():
    assert MINI.cluster_fallback == "same-length"

def test_templates_bare_function_item():
    items = MINI.templates["VOC"]
    assert items[0].kind == "literal" and items[0].value == "a"
    assert items[1].kind == "call" and items[1].value == "LEN" and items[1].child.value == "NAME"
    assert items[2].kind == "call" and items[2].value == "VOC_M1" and items[2].child is None
    assert items[2].conditional is True          # R1: bare func-name + "?"

def test_mutations_and_inflect_subtables():
    assert set(MINI.mutations) == {"LEN", "ECL"} and set(MINI.inflect) == {"VOC_M1"}
    assert MINI.mutations["LEN"][0].target[0].value == "p"

def test_unknown_syllable_key_raises():
    with pytest.raises(ParseError):
        parse_rules("[inventory]\np a\n[syllable]\nwibble = 3\n", TABLE)

def test_unknown_stress_procedure_raises():
    with pytest.raises(ParseError):
        parse_rules("[inventory]\np\n[stress]\nprocedure = wibble\n", TABLE)


def test_nuclei_must_be_vowel_sequences():
    """`nuclei` lists licensed VOWEL sequences (I-2, spec §12.B); a consonant inside one is a
    rule-file bug, not something group_nuclei() should silently ignore."""
    with pytest.raises(ParseError, match="nucle"):
        parse_rules("[inventory]\np a\n[syllable]\nnuclei = pa\n", TABLE)
