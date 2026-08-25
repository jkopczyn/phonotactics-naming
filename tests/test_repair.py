"""Plan Task 11: the unconditional repair loop and `cluster-fallback` (spec §12.A, §12.E)."""
from helpers import TABLE, w
from strands.dsl import parse_rules
from strands.repair import MAX_REPAIR_PASSES, cluster_fallback, repair
from strands.syllabify import syllabify

SRC = ("[inventory]\ns k i a t d\n[syllable]\ntemplate = (C)N(C)\nonsets = s k i t d\n"
       "codas = s k t\nsonority = off\n"
       "[repair]\n0 -> i / # _ s [C -sonorant]   %attested\nd -> t / _ #   %attested\n")


def test_repair_fixes_an_illegal_onset_and_clears_the_mark():
    rf = parse_rules(SRC, TABLE)
    out = repair(syllabify(w("ski"), rf, TABLE), rf, TABLE)
    assert out.segments == ("i", "s", "k", "i") and out.illegal == frozenset()
    assert "UNREPAIRED" not in out.flags


def test_active_rules_apply_even_when_nothing_is_illegal():
    """Spec §12.A: [repair] is unconditional — final devoicing must fire on a legal word."""
    rf = parse_rules(SRC, TABLE)
    out = repair(syllabify(w("kad"), rf, TABLE), rf, TABLE)
    assert out.segments == ("k", "a", "t")


def test_resyllabification_happens_after_a_count_changing_rule():
    rf = parse_rules(SRC, TABLE)
    assert repair(syllabify(w("ski"), rf, TABLE), rf, TABLE).syllables == (0, 2)


def test_count_preserving_repair_can_clear_illegality():
    """The draft-1 loop could not do this; §12.A's re-syllabify-after-any-change can."""
    src = ("[inventory]\np t a\n[syllable]\ntemplate = (C)N(C)\nonsets = t\ncodas = t\n"
           "sonority = off\n[repair]\np -> t   %design\n")
    rf = parse_rules(src, TABLE)
    out = repair(syllabify(w("pa"), rf, TABLE), rf, TABLE)
    assert out.illegal == frozenset() and "UNREPAIRED" not in out.flags


def test_repair_trace_entries_carry_the_stage_and_rule_id():
    rf = parse_rules(SRC, TABLE)
    out = repair(syllabify(w("ski"), rf, TABLE), rf, TABLE)
    entries = [t for t in out.trace if t.stage == "repair"]
    assert [t.rule_id for t in entries] == ["repair:9"]
    assert entries[0].tag == "attested" and entries[0].before == "ski"


def test_unrepairable_word_is_flagged_and_the_loop_terminates():
    src = ("[inventory]\nk t a\n[syllable]\ntemplate = (C)N\nonsets = k\ncodas = k\n"
           "sonority = off\n[repair]\nk -> k   %design\n")
    rf = parse_rules(src, TABLE)
    out = repair(syllabify(w("kta"), rf, TABLE), rf, TABLE)
    assert "UNREPAIRED" in out.flags


def test_cycle_detection_stops_an_oscillating_rule_set():
    src = ("[inventory]\na b\n[syllable]\ntemplate = N\nonsets = any\ncodas = any\n"
           "sonority = off\nbans = a\n[repair]\na -> b   %design\nb -> a   %design\n")
    rf = parse_rules(src, TABLE)
    out = repair(syllabify(w("a"), rf, TABLE), rf, TABLE)
    assert "UNREPAIRED" in out.flags
    assert len([t for t in out.trace if t.stage == "repair"]) < 100   # bounded, not runaway
    # the string returned to its starting point after one pass: cycle detected, one pass run
    assert len([t for t in out.trace if t.stage == "repair"]) == 2


def test_pass_cap_bounds_a_rule_set_that_keeps_changing():
    """A word that grows every pass never repeats a string; only the cap stops it."""
    src = ("[inventory]\na b\n[syllable]\ntemplate = N\nonsets = any\ncodas = any\n"
           "sonority = off\nbans = a\n[repair]\n0 -> b / _ #   %design\n")
    rf = parse_rules(src, TABLE)
    out = repair(syllabify(w("a"), rf, TABLE), rf, TABLE)
    assert "UNREPAIRED" in out.flags
    assert len([t for t in out.trace if t.stage == "repair"]) == MAX_REPAIR_PASSES


def test_repair_without_a_repair_section_is_a_no_op_on_a_legal_word():
    rf = parse_rules("[inventory]\nk a\n[syllable]\ntemplate = (C)N\nonsets = k\ncodas = any\n"
                     "sonority = off\n", TABLE)
    x = syllabify(w("ka"), rf, TABLE)
    assert repair(x, rf, TABLE) == x


def test_cluster_fallback_replaces_an_illegal_span_with_a_same_length_attested_cluster():
    """Spec §12.E — synthetic, as no attested Georgian example exists. `tl` is exactly
    two features from both `pl` and `kl` (plan S2: the real winner was computed), so list
    order decides and `pl`, listed first, wins."""
    src = ("[inventory]\np t k s l a\n[syllable]\ntemplate = (C)(C)N\nonsets = p t k s l pl kl\n"
           "codas = any\nsonority = off\n[repair]\ncluster-fallback = same-length\n")
    rf = parse_rules(src, TABLE)
    assert TABLE.distance("t", "p") == TABLE.distance("t", "k")
    out = repair(syllabify(w("tla"), rf, TABLE), rf, TABLE)
    assert out.segments[:2] == ("p", "l") and out.illegal == frozenset()
    assert any(t.tag == "fallback" for t in out.trace)
    assert "UNREPAIRED" not in out.flags


def test_cluster_fallback_ties_break_by_list_order():
    src = ("[inventory]\np t k s l a\n[syllable]\ntemplate = (C)(C)N\nonsets = p t k s l kl pl\n"
           "codas = any\nsonority = off\n[repair]\ncluster-fallback = same-length\n")
    rf = parse_rules(src, TABLE)
    # `sl` is equidistant (4.0) from `kl` and `pl`; `kl` is listed first here.
    assert TABLE.distance("s", "k") == TABLE.distance("s", "p")
    out = cluster_fallback(syllabify(w("sla"), rf, TABLE), rf, TABLE)
    assert out.segments[:2] == ("k", "l")


def test_cluster_fallback_handles_a_coda_span():
    src = ("[inventory]\np t k l a\n[syllable]\ntemplate = (C)N(C)(C)\nonsets = p t k l\n"
           "codas = p t k l lp lt\nsonority = off\n[repair]\ncluster-fallback = same-length\n")
    rf = parse_rules(src, TABLE)
    out = repair(syllabify(w("alk"), rf, TABLE), rf, TABLE)
    # `lk` is equidistant from `lp` and `lt`; `lp` is listed first.
    assert out.segments == ("a", "l", "p") and out.illegal == frozenset()


def test_cluster_fallback_trace_entry_shape():
    src = ("[inventory]\np t k s l a\n[syllable]\ntemplate = (C)(C)N\nonsets = p t k s l pl kl\n"
           "codas = any\nsonority = off\n[repair]\ncluster-fallback = same-length\n")
    rf = parse_rules(src, TABLE)
    out = cluster_fallback(syllabify(w("tla"), rf, TABLE), rf, TABLE)
    (t,) = [t for t in out.trace if t.tag == "fallback"]
    assert (t.stage, t.rule_id, t.before, t.after) == ("repair", "cluster-fallback", "tla", "pla")


def test_cluster_fallback_with_no_candidate_leaves_unrepaired():
    src = ("[inventory]\np t l a\n[syllable]\ntemplate = (C)(C)(C)N\nonsets = p t l\n"
           "codas = any\nsonority = off\n[repair]\ncluster-fallback = same-length\n")
    rf = parse_rules(src, TABLE)
    assert "UNREPAIRED" in repair(syllabify(w("ptla"), rf, TABLE), rf, TABLE).flags


def test_cluster_fallback_is_off_unless_declared():
    src = ("[inventory]\np t k s l a\n[syllable]\ntemplate = (C)(C)N\nonsets = p t k s l pl kl\n"
           "codas = any\nsonority = off\n")
    rf = parse_rules(src, TABLE)
    x = syllabify(w("tla"), rf, TABLE)
    assert cluster_fallback(x, rf, TABLE) == x
    assert "UNREPAIRED" in repair(x, rf, TABLE).flags


def test_repair_is_deterministic():
    rf = parse_rules(SRC, TABLE)
    x = syllabify(w("ski"), rf, TABLE)
    assert repair(x, rf, TABLE) == repair(x, rf, TABLE)
