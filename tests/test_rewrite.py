"""Plan Task 7: rewrite engine — matching, captures, backreferences, inline sets (I-5..I-9,
I-33), simultaneous application (I-6), trace entries (I-21)."""
import pytest
from helpers import TABLE, w
from strands.dsl import parse_rules
from strands.word import Word
from strands.rewrite import apply_rule, apply_section, find_matches, RuleError


def rr(src):
    rf = parse_rules(src, TABLE)
    return rf, rf.sections["substitute"]


def one(src, ipa):
    rf, rules = rr(src)
    return apply_rule(w(ipa), rules[0], rf, TABLE, "substitute")


def test_simple_substitution_applies_everywhere():
    assert one("[inventory]\np b a\n[substitute]\np -> b\n", "papa").segments == ("b", "a", "b", "a")


def test_one_trace_entry_per_changing_rule():
    out = one("[inventory]\np b a\n[substitute]\np -> b\n", "papa")
    assert len(out.trace) == 1 and out.trace[0].tag == "attested"
    assert out.trace[0].before == "papa" and out.trace[0].after == "baba"
    assert out.trace[0].stage == "substitute"
    assert out.trace[0].rule_id == "substitute:4"


def test_no_trace_entry_when_nothing_matches():
    assert one("[inventory]\np b a\n[substitute]\np -> b\n", "aa").trace == ()


def test_class_target():
    assert one("[inventory]\np t a\n[classes]\nX = p t\n[substitute]\nX -> a\n",
               "pt").segments == ("a", "a")


def test_derived_class_target():
    assert one("[inventory]\nk s a\n[substitute]\nFRIC -> a\n", "ksa").segments == ("k", "a", "a")


def test_feature_bundle_target_and_exact_feature_change():
    # The plan's test writes `[+ejective]` alone, but in the committed features.tsv PHOIBLE's
    # kʼ also carries constrictedGlottis=+ (Task 2 records the same deviation), so exact
    # lookup (I-4) needs both features; `[+ejective]` alone is a RuleError (next test).
    assert one("[inventory]\nk kʼ a\n[substitute]\n[C -sonorant] -> [+ejective +constrictedGlottis]\n",
               "ka").segments == ("kʼ", "a")


def test_ejective_alone_is_unreachable_in_current_table():
    with pytest.raises(RuleError):
        one("[inventory]\nk kʼ a\n[substitute]\n[C -sonorant] -> [+ejective]\n", "ka")


def test_inexact_feature_change_raises_ruleerror():
    with pytest.raises(RuleError):
        one("[inventory]\nh\n[substitute]\nh -> [+lateral]\n", "h")


def test_deletion_and_epenthesis():
    assert one("[inventory]\np a\n[substitute]\np -> 0\n", "pap").segments == ("a",)
    assert one("[inventory]\ns k i\n[substitute]\n0 -> i / # _ s\n",
               "ski").segments == ("i", "s", "k", "i")


def test_word_edge_context():
    assert one("[inventory]\nt d a\n[substitute]\nd -> t / _ #\n", "dad").segments == ("d", "a", "t")


def test_application_is_simultaneous_not_iterative():
    assert one("[inventory]\na b\n[substitute]\nb -> a / a _\n", "abb").segments == ("a", "a", "b")


def test_matches_are_non_overlapping_leftmost():
    assert one("[inventory]\na b\n[substitute]\na a -> b\n", "aaa").segments == ("b", "a")


def test_rules_apply_in_file_order_and_feed_each_other():
    rf, rules = rr("[inventory]\na b k\n[substitute]\na -> b\nb -> k\n")
    out = apply_section(w("a"), rules, rf, TABLE, "substitute")
    assert out.segments == ("k",)
    assert [t.rule_id for t in out.trace] == ["substitute:4", "substitute:5"]


def test_optional_and_star_contexts():
    assert one("[inventory]\np a b\n[substitute]\np -> b / a (a) _\n", "aap").segments[-1] == "b"
    assert one("[inventory]\np a b\n[substitute]\np -> b / a (a) _\n", "ap").segments[-1] == "b"
    assert one("[inventory]\np a b\n[substitute]\np -> b / # a* _\n", "aaap").segments[-1] == "b"
    assert one("[inventory]\np a b\n[substitute]\np -> b / # a* _\n", "p").segments == ("b",)
    assert one("[inventory]\np a b\n[substitute]\np -> b / # a a _\n", "ap").segments == ("a", "p")


def test_inline_set_matches_any_member():
    src = "[inventory]\np l n r a\n[substitute]\n0 -> a / p _ {l n r}\n"
    assert one(src, "pl").segments == ("p", "a", "l")
    assert one(src, "pn").segments == ("p", "a", "n")
    assert one(src, "pp").segments == ("p", "p")


def test_capture_and_backreference_copy_epenthesis():
    """I-33 / Welsh pobl-type copy epenthesis."""
    src = "[inventory]\np b o l a\n[substitute]\n0 -> \\1 / [V]:1 b _ l #\n"
    assert one(src, "pobl").segments == ("p", "o", "b", "o", "l")


def test_captures_in_a_target_give_metathesis():
    src = "[inventory]\ne w i θ ɾ\n[substitute]\nθ:1 ɾ:2 -> \\2 \\1 / _ #\n"
    assert one(src, "ewiθɾ").segments == ("e", "w", "i", "ɾ", "θ")


def test_undefined_backreference_raises_ruleerror():
    with pytest.raises(RuleError):
        one("[inventory]\np a\n[substitute]\np -> \\1\n", "pa")


def test_morpheme_and_syllable_and_stress_contexts():
    rf, rules = rr("[inventory]\ni a p\n[substitute]\n0 -> i / $ _ #\n")
    wd = Word(segments=("a", "p"), morphemes=frozenset({2}))
    assert apply_rule(wd, rules[0], rf, TABLE, "substitute").segments == ("a", "p", "i")
    rf2, rules2 = rr("[inventory]\na aː p\n[substitute]\na -> aː / ˈ_\n")
    wd2 = Word(segments=("a", "p", "a"), syllables=(0, 1), stress=0)
    assert apply_rule(wd2, rules2[0], rf2, TABLE, "substitute").segments == ("aː", "p", "a")
    rf3, rules3 = rr("[inventory]\na aː p\n[substitute]\na -> aː / . _\n")
    wd3 = Word(segments=("a", "p", "a"), syllables=(0, 1))
    assert apply_rule(wd3, rules3[0], rf3, TABLE, "substitute").segments == ("aː", "p", "a")
    wd4 = Word(segments=("a", "p", "a"), syllables=(0, 2))
    assert apply_rule(wd4, rules3[0], rf3, TABLE, "substitute").segments == ("aː", "p", "aː")


def test_multi_segment_replacement_shifts_annotations():
    rf, rules = rr("[inventory]\np i a\n[substitute]\np -> p i\n")
    wd = Word(segments=("p", "a"), morphemes=frozenset({2}))
    out = apply_rule(wd, rules[0], rf, TABLE, "substitute")
    assert out.segments == ("p", "i", "a") and out.morphemes == frozenset({3})


def test_find_matches_returns_spans_and_captures():
    rf, rules = rr("[inventory]\np b o l a\n[substitute]\n0 -> \\1 / [V]:1 b _ l #\n")
    assert find_matches(w("pobl"), rules[0], rf, TABLE) == [(3, 3, {1: "o"})]
    rf2, rules2 = rr("[inventory]\na b\n[substitute]\na a -> b\n")
    assert find_matches(w("aaaa"), rules2[0], rf2, TABLE) == [(0, 2, {}), (2, 4, {})]


def test_bundle_with_class_name_restricts_members():
    src = "[inventory]\np k a i\n[classes]\nBROAD = p k\n[substitute]\n0 -> i / [BROAD -labial] _ a\n"
    assert one(src, "ka").segments == ("k", "i", "a")
    assert one(src, "pa").segments == ("p", "a")


def test_undeclared_class_raises_ruleerror():
    with pytest.raises(RuleError):
        one("[inventory]\np a\n[substitute]\nNOPE -> a\n", "pa")


def test_epenthesis_keeps_its_side_of_a_morpheme_boundary():
    """`_ $` inserts on the stem side of the boundary (p i $), `$ _` on the suffix side
    (p $ i); later rules that inspect `$` must see the right morpheme."""
    wd = Word(segments=("p",), morphemes=frozenset({1}))
    rf, rules = rr("[inventory]\ni p\n[substitute]\n0 -> i / p _ $\n")
    out = apply_rule(wd, rules[0], rf, TABLE, "substitute")
    assert out.segments == ("p", "i") and out.morphemes == frozenset({2})
    rf2, rules2 = rr("[inventory]\ni p\n[substitute]\n0 -> i / $ _ #\n")
    out2 = apply_rule(wd, rules2[0], rf2, TABLE, "substitute")
    assert out2.segments == ("p", "i") and out2.morphemes == frozenset({1})
    wd3 = Word(segments=("p", "p"), morphemes=frozenset({1}))
    rf3, rules3 = rr("[inventory]\ni p\n[substitute]\n0 -> i / $ _ p\n")
    out3 = apply_rule(wd3, rules3[0], rf3, TABLE, "substitute")
    assert out3.segments == ("p", "i", "p") and out3.morphemes == frozenset({1})
