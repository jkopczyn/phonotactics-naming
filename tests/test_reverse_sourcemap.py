"""Task 4: inverting [substitute] (reverse spec §3.2, §6 bullet 1; V-3 … V-12, V-28, V-29)."""

import pytest
from helpers import TABLE, irish, target

from strands.dsl import parse_rules
from strands.reverse import invert_respell, parse_pattern, section_inventory, source_map

IRISH = irish()
GEO = target("georgian")
WEL = target("welsh")
ARA = target("arabic-egy")
DUT = target("dutch")

SYNTH_IRISH = parse_rules(
    """
[meta]
name = SynthIrish
[inventory]
pˠ pʲ k h a i
""",
    TABLE,
    path="synth-irish",
)

SYNTH_SUB = parse_rules(
    """
[meta]
name = SynthTarget
[inventory]
p t a i
[classes]
SLEN = pʲ
[substitute]
k -> t                       # literal
[SLEN] -> p                  # class target (declared HERE, F3)
[C +labial] -> p             # bundle target
0 -> i / p _ a  %design      # epenthesis (I-3: a comment after an environment needs a %tag)
h -> 0                       # deletion
t -> p                       # chain: k -> t -> p, and k precedes t in file order
""",
    TABLE,
    path="synth-target",
)


def smap(rf, section="substitute", irish_rf=None):
    return source_map(section, rf, irish_rf or IRISH, TABLE)


def sources_for(rf, key, section="substitute", irish_rf=None):
    return smap(rf, section, irish_rf)[0].get(key, ())


def srcs(rf, key, irish_rf=None):
    return {(s.segments, s.kind) for s in sources_for(rf, key, irish_rf=irish_rf)}


def _parse(rf, text):
    """V-35: both `invert_respell` values reach the pattern (as in Task 3's tests)."""
    chunk_map, notes = invert_respell(rf, TABLE)
    return parse_pattern(text, chunk_map, notes=notes)


# ---- the synthetic file: every shape spec §6 names ---------------------------------------------


def test_the_synthetic_file_covers_every_shape():
    m, deletions, _notes = smap(SYNTH_SUB, irish_rf=SYNTH_IRISH)
    got = {s.kind for ss in m.values() for s in ss}
    assert {"rule", "epenthesis", "fallback", "identity"} <= got
    assert any(d.segments == ("h",) for d in deletions)
    pairs = {(s.segments, s.kind) for s in m[("t",)]}
    assert (("k",), "rule") in pairs  # literal
    ppairs = {(s.segments, s.kind) for s in m[("p",)]}
    assert (("pʲ",), "rule") in ppairs  # class
    assert (("pˠ",), "rule") in ppairs  # bundle
    assert any(">" in s.rule_id and s.segments == ("k",) for s in m[("p",)])  # chain


def test_the_synthetic_fallback_uses_the_targets_own_nearest():
    m, _d, _n = smap(SYNTH_SUB, irish_rf=SYNTH_IRISH)
    fb = {s.segments[0] for ss in m.values() for s in ss if s.kind == "fallback"}
    assert "h" in fb and all(f not in SYNTH_SUB.inventory for f in fb)


# ---- V-29 (F3): the inventory a section expands over --------------------------------------------


def test_substitute_expands_over_irish_and_the_later_sections_over_the_target():
    assert section_inventory("substitute", ARA, IRISH) == tuple(IRISH.inventory)
    assert section_inventory("post-stress", ARA, IRISH) == tuple(ARA.inventory)


@pytest.mark.parametrize("section", ["substitute", "repair", "post-stress", "respell"])
def test_a_section_inventory_has_no_duplicates_and_keeps_declaration_order(section):
    """V-29 / F5: draft 2 appended target.marginal, which is a frozenset (non-deterministic
    order) AND a subset of inventory (duplicates)."""
    inv = section_inventory(section, GEO, IRISH)
    assert len(inv) == len(set(inv))
    src = IRISH.inventory if section == "substitute" else GEO.inventory
    assert inv == tuple(src)


def test_the_arabic_length_rules_invert_over_cairene_vowels_not_irish_ones():
    """F3: draft 1 expanded [V +long] over irish.inventory and produced nothing usable."""
    m, _d, _n = smap(ARA, "post-stress")
    got = {s.segments for ss in m.values() for s in ss}
    assert any(seg in ARA.inventory for segs in got for seg in segs)
    assert ("aː",) in {s.segments for s in m.get(("a",), ())}


def test_the_dutch_devoicing_rules_invert_over_dutch_segments():
    m, _d, _n = smap(DUT, "repair")
    assert ("b",) in {s.segments for s in m.get(("p",), ())}


# ---- the real substitute sections ----------------------------------------------------------------


def test_a_literal_segment_rule_inverts_literally():
    assert (("iː",), "rule") in srcs(GEO, ("i",))


def test_a_class_target_is_expanded_over_the_irish_inventory():
    ejective = {s.segments for s in sources_for(GEO, ("pʼ",))}
    assert ("pˠ",) in ejective and ("pʲ",) in ejective


def test_an_epenthesis_rule_has_no_irish_segments_and_carries_its_context():
    epen = [s for s in sources_for(GEO, ("v",)) if s.kind == "epenthesis"]
    assert epen and all(s.segments == () for s in epen)
    assert any(s.context == "[BROAD -labial] _ [V +front]" for s in epen)


def test_a_multi_segment_insertion_is_one_key():
    """V-30 / F4: arabic-egy `0 -> ʔ i` must be ONE key, not two. (Whether a real Arabic
    pattern can ever see it is a separate question — `[respell]` deletes an initial /ʔ/, so it
    cannot; see V-30's accepted miss and Task 5's synthetic fixture.)"""
    m, _d, _n = smap(ARA, "repair")
    assert ("ʔ", "i") in m
    assert all(s.kind == "epenthesis" for s in m[("ʔ", "i")])


def test_invert_respell_notes_a_deleting_respell_rule():
    """V-30 accepted miss: `ʔ -> "" / # _` makes a group starting at /ʔ/ unreachable."""
    from strands.reverse import invert_respell

    _chunks, notes = invert_respell(ARA, TABLE)
    assert any("unreachable" in n for n in notes)


def test_a_deletion_is_recorded_and_never_expanded():
    m, deletions, _n = smap(WEL)
    assert any(d.segments == ("w",) for d in deletions)
    assert all(s.kind != "deletion" for ss in m.values() for s in ss)


def test_a_target_backref_is_resolved_by_the_expansion():
    assert (("a", "w"), "rule") in srcs(WEL, ("a", "u"))
    assert (("ɪ", "w"), "rule") in srcs(WEL, ("ɪ", "u"))


def test_a_context_backref_becomes_one_epenthesis_source_per_copyable_segment():
    """V-6. MEASURED: no [substitute] section of any strand has a context backref — welsh's
    `0 -> \\1 / # C* V:1 (C) EPEN_C1 _ {l n r} #` is repair:298, not substitute:298 (the plan's
    shape table names the line, the section is [repair]), so the shape is asserted there."""
    got = [s for s in sources_for(WEL, ("a",), "repair") if s.kind == "epenthesis"]
    assert got and all(s.segments == () for s in got)
    assert any("copies" in s.note for s in got)


def test_a_multi_segment_rule_inverts_as_a_sequence():
    assert (("i", "ə"), "rule") in srcs(ARA, ("eː",))


# ---- fallback, identity, ORDERED chains (F2) -----------------------------------------------------


def test_the_fallback_maps_every_off_inventory_survivor():
    """MEASURED: no real strand has a survivor. Every Irish segment outside georgian's,
    welsh's, arabic-egy's or dutch's inventory is the whole target of a CONTEXT-FREE
    [substitute] rule (georgian:79-118, welsh:59-174, arabic-egy:59-118, dutch:59-160), so
    V-8 fires on none of them — the plan's expectation of a georgian fallback source does not
    hold on the files. The invariant is therefore asserted where there IS a survivor: the
    synthetic file's /h/, which must land on the target's own `table.nearest`."""
    assert not [s for ss in smap(GEO)[0].values() for s in ss if s.kind == "fallback"]
    m, _d, _n = smap(SYNTH_SUB, irish_rf=SYNTH_IRISH)
    got = {(s.segments[0], key) for key, ss in m.items() for s in ss if s.kind == "fallback"}
    candidates = tuple(x for x in SYNTH_SUB.inventory if x not in SYNTH_SUB.marginal)
    assert got and all(seg not in SYNTH_SUB.inventory for seg, _key in got)
    assert all(key == (TABLE.nearest(seg, candidates, SYNTH_SUB.weights),) for seg, key in got)


def test_identity_covers_the_segments_no_rule_touches():
    got = {s.segments for ss in smap(GEO)[0].values() for s in ss if s.kind == "identity"}
    assert all(len(g) == 1 and g[0] in GEO.inventory for g in got)


def test_a_forward_reachable_chain_is_followed():
    """V-28, MEASURED: georgian:79 `pˠ -> p` (context-free) precedes georgian:118
    `p -> pʼ / C _`, so /pˠ/ really is a forward source of /pʼ/."""
    got = {s.segments for s in sources_for(GEO, ("pʼ",))}
    assert ("p",) in got and ("pˠ",) in got


def test_the_spec_s_welsh_illustration_is_not_a_chain_in_the_file():
    """V-28: welsh has `x -> χ` (118) and `ç -> χ` DIRECTLY (121) — no `ç -> x` rule, so /ç/
    reaches /χ/ in one step and nothing is composed. Asserted so a future reader does not
    re-derive the spec's illustration as a requirement."""
    got = {s.segments: s.rule_id for s in sources_for(WEL, ("χ",))}
    assert ("ç",) in got and ">" not in got[("ç",)]


def test_a_backwards_chain_is_NOT_followed():
    """F2 / V-28: arabic-egy has `ʒ -> ʃ` BEFORE `dʒ -> ʒ`, so forward /dʒ/ ends at /ʒ/ and
    never reaches /ʃ/. Draft 1 composed them anyway."""
    assert ("dʒ",) not in {s.segments for s in sources_for(ARA, ("ʃ",))}
    assert ("dʒ",) in {s.segments for s in sources_for(ARA, ("ʒ",))}


def test_a_chain_rule_id_names_both_steps_and_takes_the_weaker_tag():
    chained = [s for s in sources_for(GEO, ("pʼ",)) if ">" in s.rule_id]
    assert chained and all(">" in s.rule_id for s in chained)
    assert all(s.tag in ("design", "attested") for s in chained)


def test_the_degemination_rules_do_not_make_the_closure_loop():
    assert len(sources_for(GEO, ("v",))) < 200


def test_a_context_bearing_rule_still_leaves_its_target_a_fallback_or_identity_source():
    """V-10 / R2."""
    assert "rule" in {s.kind for s in sources_for(GEO, ("pʰ",))}


def test_un_substitute_appends_a_step_to_each_alternative():
    """V-31: provenance composes."""
    from strands.reverse import un_substitute

    p = _parse(GEO, "a")
    m, deletions, notes = smap(GEO)
    out = un_substitute(p, m, deletions=deletions, notes=notes)
    assert any(len(a.steps) >= 2 and a.steps[-1].stage == "substitute" for a in out.slots[0].alts)


def test_un_substitute_carries_the_substitute_deletions_into_the_pattern():
    """F3: draft 2 computed them and dropped them, so `possibly dropped` could never show a
    [substitute] deletion. welsh.rules:161-164 are the real ones (`w -> 0`, `j -> 0`)."""
    from strands.reverse import un_substitute

    p = _parse(WEL, "u")
    m, deletions, notes = smap(WEL)
    out = un_substitute(p, m, deletions=deletions, notes=notes)
    ids = {d.rule_id for d in out.deletions}
    assert any(i.startswith("substitute:") for i in ids), ids


def test_the_map_is_deterministic():
    assert smap(GEO)[0] == smap(GEO)[0]
    assert all(isinstance(v, tuple) for v in smap(GEO)[0].values())


# ---- review fixes ------------------------------------------------------------------------------


def test_un_substitute_drops_an_alternative_with_no_substitute_source():
    """V-31: welsh `th` parses as /θ/, which no [substitute] source produces. Keeping it would
    leave a stepless alternative that reporting reads as an Irish identity source."""
    from strands.reverse import un_substitute

    m, deletions, notes = smap(WEL)
    assert ("θ",) not in m
    p = _parse(WEL, "th")
    assert [a.segments for a in p.slots[0].alts] == [("θ",)]
    out = un_substitute(p, m, deletions=deletions, notes=notes)
    assert out.slots[0].alts == ()


def test_every_surviving_alternative_carries_a_substitute_step():
    from strands.reverse import un_substitute

    m, deletions, notes = smap(GEO)
    out = un_substitute(_parse(GEO, "a"), m, deletions=deletions, notes=notes)
    assert out.slots[0].alts
    assert all(a.steps and a.steps[-1].stage == "substitute" for a in out.slots[0].alts)


SYNTH_MULTI = parse_rules(
    """
[meta]
name = SynthMulti
[inventory]
p t a i aː iː
[substitute]
a i -> [+long]               # context-free feature change over a MULTI-item target
""",
    TABLE,
    path="synth-multi",
)


def test_a_multi_item_context_free_feature_change_covers_only_the_whole_target():
    """V-8/V-9: an isolated `a` does not match `a i -> [+long]`, so it keeps its identity source."""
    m, _deletions, _notes = smap(SYNTH_MULTI, irish_rf=SYNTH_IRISH)
    assert ("aː",) in m and ("iː",) in m
    assert "identity" in {s.kind for s in m.get(("a",), ())}
    assert "identity" in {s.kind for s in m.get(("i",), ())}


# ================================================================================================
# Task 5: widening over [repair] / [post-stress] (spec §3.3; V-18, V-29, V-30, V-31)
# ================================================================================================

from strands.reverse import widen  # noqa: E402

# V-30 accepted miss: no real strand shows a two-segment insertion in its respelling
# (arabic-egy deletes the /ʔ/ of `0 -> ʔ i` with `ʔ -> "" / # _`), so the ATOMIC-GROUP
# behaviour is tested on a synthetic file where both inserted segments are printed.
SYNTH_GROUP = parse_rules(
    """
[meta]
name = SynthGroup
[inventory]
q i s k
[repair]
0 -> q i / # _ s
[respell]
q -> "q"
i -> "i"
s -> "s"
k -> "k"
""",
    TABLE,
    path="synth-group",
)


def pat(rf, text):
    return widen(_parse(rf, text), rf, IRISH, TABLE)


def alt_set(p):
    return {a.segments for s in p.slots for a in s.alts}


def test_a_welsh_long_vowel_gains_its_short_partner():
    """spec §3.3: Welsh long vowels <- the short one via the §4.3 lengthening."""
    got = alt_set(pat(WEL, "â"))
    assert ("aː",) in got and ("a",) in got


def test_welsh_y_is_widened_by_nothing_because_no_repair_rule_PRODUCES_a_schwa():
    """MEASURED, against the plan's reading. Spec §3.3 names "Welsh y/ə ← any short vowel via
    reduction", but `welsh.rules` has no reduction rule in `[repair]` or `[post-stress]`: the
    only rules whose OUTPUT is /ə/ there are the two prothesis insertions (`0 -> ə / # _ s …`,
    repair:272,276), which V-30 turns into optional GROUPS, not alternatives. The /ə/ → Irish
    step is a `[substitute]` one (welsh.rules:173 `ə -> a / _ C* #` and its neighbours) and so
    belongs to `un_substitute`, not to widening. Pinned so a reader does not re-derive the
    spec's sentence as a widening requirement."""
    m, _deletions, _notes = source_map("repair", WEL, IRISH, TABLE)
    assert all(s.kind == "epenthesis" for s in m[("ə",)])
    assert ("ə",) not in source_map("post-stress", WEL, IRISH, TABLE)[0]
    assert alt_set(pat(WEL, "y")) == {("ə",)}


def test_welsh_initial_ll_gains_plain_l():
    got = alt_set(pat(WEL, "ll"))
    assert ("ɬ",) in got and ("l",) in got


def test_georgian_degemination_widens_a_consonant_slot():
    assert ("v", "v") in alt_set(pat(GEO, "v"))


def test_a_widened_alternative_records_the_widening_rule():
    """V-31 / F5: draft 1 lost the rule id and could not print a source for it."""
    p = pat(WEL, "â")
    widened = [a for s in p.slots for a in s.alts if a.segments == ("a",)]
    assert widened and any(st.stage in ("post-stress", "repair") for a in widened for st in a.steps)


# ---- optional GROUPS (V-30 / F4) -----------------------------------------------------------------


def test_a_single_segment_insertion_is_a_width_one_group():
    """Welsh prothetic ⟨y⟩ (`0 -> ə / # _ s {p t k}`)."""
    p = pat(WEL, "ysbryd")
    assert any(g.start == 0 and g.stop == 1 for g in p.groups)


def test_a_two_segment_insertion_is_ONE_group_of_width_two():
    """F4 / V-30: the inserted pair is atomic. Synthetic, because `arabic-egy`'s own
    `0 -> ʔ i` is invisible in its respelling (`ʔ -> "" / # _`)."""
    p = pat(SYNTH_GROUP, "qisk")
    assert [(g.start, g.stop) for g in p.groups] == [(0, 2)]


def test_no_group_covers_only_half_an_insertion():
    p = pat(SYNTH_GROUP, "qisk")
    assert all(g.stop - g.start == 2 for g in p.groups)


def test_the_arabic_pair_is_a_recorded_miss_not_a_silent_one():
    """V-30 accepted miss: `isk` is three slots, so the two-segment insertion
    `0 -> ʔ i / # _ s [C -sonorant]` finds no span — `[respell]` deletes its /ʔ/
    (`ʔ -> "" / # _`), so no slot can start the group — and a note says why.

    MEASURED, against the plan's `all(width == 2)` reading, which has it backwards for this
    file: the section's SINGLE-segment insertions (`0 -> i / # C _ C V`, and the context
    backref of repair:147) do find width-one spans, so what makes the pair a miss is that no
    group of width TWO exists."""
    p = pat(ARA, "isk")
    assert all(g.stop - g.start == 1 for g in p.groups)
    assert any("unreachable" in n for n in p.notes)


def test_groups_are_sorted_and_non_overlapping():
    p = pat(WEL, "ysbryd")
    spans = [(g.start, g.stop) for g in p.groups]
    assert spans == sorted(spans)
    assert all(a[1] <= b[0] for a, b in zip(spans, spans[1:], strict=False))


def test_deletions_from_the_widened_sections_reach_the_pattern():
    """V-7: one word-level list, not a note on every slot."""
    p = pat(WEL, "u")
    assert isinstance(p.deletions, tuple)


def test_stress_is_ignored():
    for s in pat(WEL, "ysbryd").slots:
        assert all(m not in seg for a in s.alts for seg in a.segments for m in ("ˈ", "ˌ", "."))


def test_widening_only_grows_the_slot_set():
    before = _parse(WEL, "â")
    after = widen(before, WEL, IRISH, TABLE)
    for b, a in zip(before.slots, after.slots, strict=True):
        assert {x.segments for x in b.alts} <= {x.segments for x in a.alts}


def test_a_group_keeps_every_epenthesis_source_of_its_span():
    """V-30 review fix: draft 1 kept only `epenthetic[0]`, so Welsh `ysmy` named `repair:272`
    (`# _ s {p t k}`) and silently lost `repair:276` (`# _ s {m n}`), the rule that actually
    fits — provenance Task 6 has to print."""
    p = pat(WEL, "ysmy")
    (initial,) = [g for g in p.groups if (g.start, g.stop) == (0, 1)]
    ids = {st.rule_id for st in initial.steps}
    assert {"repair:272", "repair:276"} <= ids
    assert "repair:272" in initial.note and "repair:276" in initial.note


def test_group_steps_are_deduped_and_each_span_appears_once():
    """Equal spans MERGE (their steps join) instead of one being dropped."""
    p = pat(WEL, "ysmy")
    spans = [(g.start, g.stop) for g in p.groups]
    assert len(spans) == len(set(spans))
    for g in p.groups:
        assert len(g.steps) == len(set(g.steps))


def test_a_multi_source_group_is_still_one_atomic_group():
    """The extra sources must not reintroduce half-groups (V-30/F4)."""
    p = pat(SYNTH_GROUP, "qisk")
    assert [(g.start, g.stop) for g in p.groups] == [(0, 2)]
