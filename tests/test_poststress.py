"""Plan Task 16: the `[post-stress]` stage (spec §4.5 — rules that depend on stress)."""
from helpers import TABLE, w
from strands.dsl import parse_rules
from strands.poststress import post_stress
from strands.stress import assign_stress
from strands.syllabify import syllabify

BASE = ("[inventory]\np t s k a aː i\n[syllable]\ntemplate = (C)(C)N(C)\nonsets = p t s k sk\n"
        "codas = p t s k\nsonority = off\n[stress]\nprocedure = penult\n")


def stressed(ipa: str, rf):
    return assign_stress(syllabify(w(ipa), rf, TABLE), rf, TABLE)


def test_post_stress_rule_sees_the_stress_mark():
    # `ˈ` is the stressed syllable's START (spec §3), so the stressed vowel of `pata` is
    # `ˈ C _`. The plan's sketch wrote `ˈ_ C N`; `N` is template syntax, not a class.
    rf = parse_rules(BASE + "[post-stress]\na -> aː / ˈ C _ C V   %design\n", TABLE)
    out = post_stress(stressed("pata", rf), rf, TABLE)
    assert out.segments == ("p", "aː", "t", "a")
    assert out.ipa() == "ˈpaː.ta"


def test_unstressed_vowel_is_not_touched_by_a_stress_conditioned_rule():
    rf = parse_rules(BASE + "[post-stress]\na -> aː / ˈ C _   %design\n", TABLE)
    out = post_stress(stressed("tapa", rf), rf, TABLE)
    assert out.segments == ("t", "aː", "p", "a")


def test_post_stress_resyllabifies_and_keeps_the_stressed_syllable():
    rf = parse_rules(BASE + "[post-stress]\n0 -> i / t _ #   %design\n", TABLE)
    out = post_stress(stressed("pat", rf), rf, TABLE)
    assert out.segments == ("p", "a", "t", "i") and out.stress == 0
    assert out.syllables == (0, 2) and out.ipa() == "ˈpa.ti"


def test_initial_epenthesis_keeps_stress_on_the_original_nucleus():
    rf = parse_rules(BASE + "[post-stress]\n0 -> i / # _ s k   %design\n", TABLE)
    out = post_stress(stressed("ska", rf), rf, TABLE)
    assert out.segments == ("i", "s", "k", "a")
    assert out.syllables == (0, 1) and out.stress == 1 and out.ipa() == "i.ˈska"


def test_count_preserving_rule_does_not_resyllabify():
    rf = parse_rules(BASE + "[post-stress]\na -> aː / ˈ C _   %design\n", TABLE)
    out = post_stress(stressed("pata", rf), rf, TABLE)
    assert [t.stage for t in out.trace].count("syllabify") == 1
    assert out.trace[-1].stage == "post-stress"
    assert out.trace[-1].rule_id == "post-stress:11" and out.trace[-1].tag == "design"


def test_rules_apply_in_file_order_each_seeing_the_previous_output():
    rf = parse_rules(BASE + "[post-stress]\na -> aː / ˈ C _   %design\n"
                     "aː -> i / _ t   %design\n", TABLE)
    out = post_stress(stressed("pata", rf), rf, TABLE)
    assert out.segments == ("p", "i", "t", "a")


def test_absent_section_is_a_noop():
    rf = parse_rules(BASE, TABLE)
    x = stressed("pata", rf)
    assert post_stress(x, rf, TABLE) == x


def test_non_matching_rules_leave_the_word_identical():
    rf = parse_rules(BASE + "[post-stress]\nk -> t / ˈ _   %design\n", TABLE)
    x = stressed("pata", rf)
    assert post_stress(x, rf, TABLE) == x


def test_net_zero_length_change_still_resyllabifies():
    """review-stress-irish fix 1: an insertion plus a deletion leaves the count unchanged
    overall, but each rule changed it, so the stale one-syllable parse must be redone."""
    rf = parse_rules(BASE + "[post-stress]\n0 -> i / # _ p   %design\nt -> 0 / _ #   %design\n",
                     TABLE)
    out = post_stress(stressed("pat", rf), rf, TABLE)
    assert out.segments == ("i", "p", "a")
    assert out.syllables == (0, 1) and out.stress == 1 and out.ipa() == "i.ˈpa"


def test_deleting_the_stressed_onset_keeps_the_stress():
    """review-stress-irish fix 1: the stressed syllable is identified by its nucleus in the
    PRE-edit word, so deleting its onset (its syllable start) does not lose the stress."""
    rf = parse_rules(BASE + "[post-stress]\np -> 0 / # _   %design\n", TABLE)
    out = post_stress(stressed("pat", rf), rf, TABLE)
    assert out.segments == ("a", "t")
    assert out.stress == 0 and out.ipa() == "ˈat"
