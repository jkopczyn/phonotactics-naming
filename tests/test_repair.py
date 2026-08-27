"""Plan Task 11: the unconditional repair loop and `cluster-fallback` (spec §12.A, §12.E)."""
import pytest
from helpers import TABLE, w

from strands.dsl import ParseError, parse_rules
from strands.repair import MAX_REPAIR_PASSES, cluster_fallback, cluster_keep, overlay_undo, repair
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


# ---- cluster-fallback = keep (owner decision 2026-08-25; digest §3.7) ---------------------------

KEEP_SRC = ("[inventory]\np t k s l a\n[syllable]\ntemplate = (C)(C)N\nonsets = p t k s l pl kl\n"
            "codas = any\nsonority = off\n[repair]\ncluster-fallback = keep\n")


def test_cluster_keep_leaves_the_span_unchanged_and_clears_the_marks():
    """Owner decision 2026-08-25: Georgian imports a foreign cluster intact (digest §3.7),
    so an illegal onset is kept and the repair loop terminates without UNREPAIRED."""
    rf = parse_rules(KEEP_SRC, TABLE)
    out = repair(syllabify(w("tla"), rf, TABLE), rf, TABLE)
    assert out.segments == ("t", "l", "a")
    assert out.illegal == frozenset()
    assert "UNREPAIRED" not in out.flags


def test_cluster_keep_flags_the_kept_cluster():
    rf = parse_rules(KEEP_SRC, TABLE)
    out = repair(syllabify(w("tla"), rf, TABLE), rf, TABLE)
    assert "UNATTESTED_CLUSTER:tl" in out.flags


def test_cluster_keep_does_not_count_as_a_fallback():
    """Nothing was substituted, so the fallback count must not move."""
    rf = parse_rules(KEEP_SRC, TABLE)
    out = repair(syllabify(w("tla"), rf, TABLE), rf, TABLE)
    assert out.fallback_count() == 0
    assert not any(t.tag == "fallback" for t in out.trace)


def test_cluster_keep_trace_entry_shape():
    rf = parse_rules(KEEP_SRC, TABLE)
    out = repair(syllabify(w("tla"), rf, TABLE), rf, TABLE)
    (t,) = [t for t in out.trace if t.rule_id == "cluster-keep"]
    assert (t.stage, t.rule_id, t.tag) == ("repair", "cluster-keep", "design")
    assert (t.before, t.after) == ("tla", "tla")
    assert t.note == ("tl: unattested cluster kept (Georgian imports foreign clusters intact; "
                      "digest §3.7)")


def test_cluster_keep_handles_a_coda_span():
    src = ("[inventory]\np t k l a\n[syllable]\ntemplate = (C)N(C)(C)\nonsets = p t k l\n"
           "codas = p t k l lp lt\nsonority = off\n[repair]\ncluster-fallback = keep\n")
    rf = parse_rules(src, TABLE)
    out = repair(syllabify(w("alk"), rf, TABLE), rf, TABLE)
    assert out.segments == ("a", "l", "k") and out.illegal == frozenset()
    assert "UNATTESTED_CLUSTER:lk" in out.flags


def test_cluster_keep_flags_one_cluster_per_span():
    src = ("[inventory]\np t k l a\n[syllable]\ntemplate = (C)(C)N(C)(C)\nonsets = p t k l tl\n"
           "codas = p t k l lp\nsonority = off\n[repair]\ncluster-fallback = keep\n")
    rf = parse_rules(src, TABLE)
    out = repair(syllabify(w("plalk"), rf, TABLE), rf, TABLE)
    assert out.segments == ("p", "l", "a", "l", "k")
    assert [f for f in out.flags if f.startswith("UNATTESTED_CLUSTER")] == \
        ["UNATTESTED_CLUSTER:pl", "UNATTESTED_CLUSTER:lk"]


def test_cluster_keep_is_off_unless_declared():
    src = ("[inventory]\np t k s l a\n[syllable]\ntemplate = (C)(C)N\nonsets = p t k s l pl kl\n"
           "codas = any\nsonority = off\n")
    rf = parse_rules(src, TABLE)
    x = syllabify(w("tla"), rf, TABLE)
    assert cluster_keep(x, rf, TABLE) == x
    assert "UNREPAIRED" in repair(x, rf, TABLE).flags


def test_cluster_fallback_directive_rejects_an_unknown_value():
    src = ("[inventory]\np a\n[syllable]\ntemplate = (C)N\nonsets = p\ncodas = any\n"
           "sonority = off\n[repair]\ncluster-fallback = nearest\n")
    with pytest.raises(ParseError):
        parse_rules(src, TABLE)


# ---- overlay-undo (owner decision 2026-08-25) ---------------------------------------------------

UNDO_SRC = ("[inventory]\nn v i r m\n[substitute]\n0 -> v / {n r} _ i   %design\n"
            "[syllable]\ntemplate = (C)(C)(C)N(C)\nonsets = n v r m nr nrv rv\ncodas = m\n"
            "sonority = off\n[repair]\noverlay-undo = v\ncluster-fallback = keep\n")


def _substituted(src, ipa):
    rf = parse_rules(src, TABLE)
    from strands.substitute import substitute_stage
    return rf, syllabify(substitute_stage(w(ipa), rf, TABLE), rf, TABLE)


def test_overlay_undo_deletes_an_inserted_segment_that_makes_the_onset_legal():
    """`nvi` is not a licensed onset; dropping the epenthetic v leaves `ni`, which is."""
    src = UNDO_SRC.replace("onsets = n v r m nr nrv rv", "onsets = n v r m nr rv")
    rf, x = _substituted(src, "ni")
    out = repair(x, rf, TABLE)
    assert out.segments == ("n", "i")
    assert out.illegal == frozenset() and "UNREPAIRED" not in out.flags
    assert not any(f.startswith("UNATTESTED_CLUSTER") for f in out.flags)


def test_overlay_undo_trace_entry_shape():
    src = UNDO_SRC.replace("onsets = n v r m nr nrv rv", "onsets = n v r m nr rv")
    rf, x = _substituted(src, "ni")
    (t,) = [t for t in repair(x, rf, TABLE).trace if t.rule_id == "overlay-undo"]
    assert (t.stage, t.rule_id, t.tag) == ("repair", "overlay-undo", "design")
    assert (t.before, t.after) == ("nvi", "ni")


def test_overlay_undo_keeps_the_segment_when_the_onset_is_still_illegal():
    """`nrv` is not licensed and `nr` is not either, so the v stays and cluster-keep takes it."""
    src = UNDO_SRC.replace("onsets = n v r m nr nrv rv", "onsets = n v r m rv")
    rf, x = _substituted(src, "nrim")
    out = repair(x, rf, TABLE)
    assert out.segments == ("n", "r", "v", "i", "m")
    assert not any(t.rule_id == "overlay-undo" for t in out.trace)
    assert "UNATTESTED_CLUSTER:nrv" in out.flags


def test_overlay_undo_does_not_fire_on_a_legal_onset():
    rf, x = _substituted(UNDO_SRC, "nrim")
    out = repair(x, rf, TABLE)
    assert out.segments == ("n", "r", "v", "i", "m") and out.trace[-1].rule_id != "overlay-undo"


def test_overlay_undo_only_deletes_segments_the_substitute_stage_inserted():
    """A `v` that was in the input keeps its place: only overlay material is undone."""
    src = UNDO_SRC.replace("onsets = n v r m nr nrv rv", "onsets = n v r m nr rv")
    rf = parse_rules(src, TABLE)
    out = repair(syllabify(w("nvim"), rf, TABLE), rf, TABLE)
    assert out.segments == ("n", "v", "i", "m")
    assert "UNATTESTED_CLUSTER:nv" in out.flags


def test_overlay_undo_is_off_unless_declared():
    src = UNDO_SRC.replace("overlay-undo = v\n", "").replace(
        "onsets = n v r m nr nrv rv", "onsets = n v r m nr rv")
    rf, x = _substituted(src, "ni")
    assert overlay_undo(x, rf, TABLE) is x
    out = repair(x, rf, TABLE)
    assert out.segments == ("n", "v", "i") and "UNATTESTED_CLUSTER:nv" in out.flags


def test_overlay_undo_directive_rejects_an_unknown_segment():
    src = UNDO_SRC.replace("overlay-undo = v", "overlay-undo = ")
    with pytest.raises(ParseError):
        parse_rules(src, TABLE)
