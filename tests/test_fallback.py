"""Plan Task 9: the inventory fallback (spec §4.2b, I-12, I-23)."""
from helpers import TABLE
from strands.dsl import parse_rules
from strands.word import Word
from strands.substitute import fallback, substitute_stage


def test_off_inventory_segment_is_replaced_by_the_nearest():
    rf = parse_rules("[inventory]\nb f a\n", TABLE)
    out = fallback(Word(segments=("pˠ", "a")), rf, TABLE)
    assert out.segments == ("b", "a") and out.trace[0].tag == "fallback"


def test_trace_entry_shape():
    rf = parse_rules("[inventory]\nb f a\n", TABLE)
    out = fallback(Word(segments=("pˠ", "a")), rf, TABLE)
    (t,) = out.trace
    assert (t.stage, t.rule_id, t.tag, t.before, t.after) == (
        "fallback", "fallback", "fallback", "pˠa", "ba")


def test_marginal_segments_are_never_chosen():
    rf = parse_rules("[inventory]\nb a\nmarginal: p\n", TABLE)
    assert fallback(Word(segments=("pˠ",)), rf, TABLE).segments == ("b",)


def test_marginal_segments_in_the_word_are_kept():
    """I-23: marginal segments are legal in output, only never picked."""
    rf = parse_rules("[inventory]\nb a\nmarginal: p\n", TABLE)
    wd = Word(segments=("p", "a"))
    assert fallback(wd, rf, TABLE) == wd


def test_ties_break_by_inventory_order():
    """S2: a real tie, hard-coded both ways. Measured against the built table:
    distance(pˠ, b) == distance(pˠ, pʰ) == 1.0 (the plan's n̪ˠ/m/ŋ pair is 2.0 vs 3.0,
    not a tie, so it is used for the weights test instead)."""
    assert TABLE.distance("pˠ", "b") == TABLE.distance("pˠ", "pʰ")
    a = parse_rules("[inventory]\nb pʰ a\n", TABLE)
    b = parse_rules("[inventory]\npʰ b a\n", TABLE)
    assert fallback(Word(segments=("pˠ",)), a, TABLE).segments == ("b",)
    assert fallback(Word(segments=("pˠ",)), b, TABLE).segments == ("pʰ",)


def test_weights_change_the_choice():
    """Measured: n̪ˠ is 2.0 from m and 3.0 from ŋ unweighted; the only differing feature that
    m carries is labial, so weighting it flips the winner. (The plan's ɟ/k/c example is not a
    flip: c already wins unweighted.)"""
    plain = parse_rules("[inventory]\nm ŋ a\n", TABLE)
    weighted = parse_rules("[inventory]\nm ŋ a\n[weights]\nlabial = 20.0\n", TABLE)
    assert fallback(Word(segments=("n̪ˠ",)), plain, TABLE).segments == ("m",)
    assert fallback(Word(segments=("n̪ˠ",)), weighted, TABLE).segments == ("ŋ",)


def test_inventory_segments_are_untouched_and_untraced():
    rf = parse_rules("[inventory]\nb a\n", TABLE)
    wd = Word(segments=("b", "a"))
    assert fallback(wd, rf, TABLE) == wd


def test_fallback_count():
    rf = parse_rules("[inventory]\nb a\n", TABLE)
    assert fallback(Word(segments=("pˠ", "pʲ")), rf, TABLE).fallback_count() == 2


def test_fallback_is_deterministic():
    rf = parse_rules("[inventory]\nb f a\n", TABLE)
    x = Word(segments=("pˠ", "vʲ", "a"))
    assert fallback(x, rf, TABLE) == fallback(x, rf, TABLE)


def test_fallback_keeps_annotations():
    rf = parse_rules("[inventory]\nb a\n", TABLE)
    wd = Word(segments=("pˠ", "a", "pʲ", "a"), syllables=(0, 2), morphemes=frozenset({2}))
    out = fallback(wd, rf, TABLE)
    assert out.segments == ("b", "a", "b", "a")
    assert out.syllables == (0, 2) and out.morphemes == frozenset({2})


def test_substitute_stage_runs_rules_then_fallback():
    rf = parse_rules("[inventory]\nb f a\n[substitute]\nvʲ -> f\n", TABLE)
    out = substitute_stage(Word(segments=("pˠ", "vʲ", "a")), rf, TABLE)
    assert out.segments == ("b", "f", "a")
    assert [t.stage for t in out.trace] == ["substitute", "fallback"]
    assert out.fallback_count() == 1
