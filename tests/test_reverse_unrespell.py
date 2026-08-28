"""Task 3: un-respell, the glob parser and the IPA parser (reverse spec §3.1, §2;
V-1, V-2, V-12, V-16, V-31, V-33)."""

import pytest
from helpers import TABLE, target

from strands.dsl import parse_rules
from strands.reverse import (
    ANY,
    ONE,
    SEG,
    ReverseError,
    env_text,
    invert_respell,
    parse_ipa_pattern,
    parse_pattern,
)

GEO = target("georgian")
WEL = target("welsh")
ARA = target("arabic-egy")

SYNTH = """
[meta]
name = Synth
[inventory]
a i k s t
[classes]
STOP = k t
[respell]
k -> "kh"
[STOP] -> "q"
a i -> "ai"
0 -> "e" / # _ s
i -> "y" / V _ #
"""

SYNTH_DEL = """
[meta]
name = SynthDel
[inventory]
a x
[respell]
x -> "" / # _
a -> "a"
"""


def chunks(rf):
    return invert_respell(rf, TABLE)[0]


def _parse(rf, text):
    """V-35: both `invert_respell` values reach the pattern."""
    chunk_map, notes = invert_respell(rf, TABLE)
    return parse_pattern(text, chunk_map, notes=notes)


def alts(slot):
    return {a.segments for a in slot.alts}


def test_a_quoted_replacement_becomes_a_chunk_keyed_by_its_text():
    got = chunks(parse_rules(SYNTH, TABLE, path="synth"))
    assert ("k",) in [s.segments for s in got["kh"]]


def test_a_class_target_is_expanded_over_the_files_own_inventory():
    """V-1 / V-29: [respell] reads the TARGET's segments."""
    got = {s.segments for s in chunks(parse_rules(SYNTH, TABLE, path="synth"))["q"]}
    assert got == {("k",), ("t",)}


def test_a_multi_segment_target_keeps_its_sequence():
    got = chunks(parse_rules(SYNTH, TABLE, path="synth"))
    assert ("a", "i") in [s.segments for s in got["ai"]]


def test_an_epenthesis_respell_rule_is_skipped_with_a_note():
    _got, notes = invert_respell(parse_rules(SYNTH, TABLE, path="synth"), TABLE)
    assert any("skipped" in n and "respell:" in n for n in notes)


def test_a_context_is_carried_as_text_never_evaluated():
    got = chunks(parse_rules(SYNTH, TABLE, path="synth"))
    assert [s.context for s in got["y"]] == ["V _ #"]


def test_a_respell_source_records_its_line_for_the_chain_guard():
    """V-28."""
    got = chunks(parse_rules(SYNTH, TABLE, path="synth"))
    assert all(s.line > 0 for s in got["kh"])


def test_segments_no_rule_mentions_map_to_themselves():
    got = chunks(parse_rules(SYNTH, TABLE, path="synth"))
    assert [s.segments for s in got["s"]] == [("s",)]


def test_respell_notes_reach_pattern_notes():
    """V-35: an unreachable respell deletion is a note on the Pattern."""
    pat = _parse(parse_rules(SYNTH_DEL, TABLE, path="synth-del"), "a")
    assert any("respell:" in n and "unreachable" in n for n in pat.notes)


# ---- the real files --------------------------------------------------------------------------


def test_georgian_ambiguity_is_kept_as_alternatives():
    got = chunks(GEO)
    assert ("i",) in [s.segments for s in got["y"]]
    assert ("i",) in [s.segments for s in got["i"]]


def test_welsh_i_has_three_sources():
    got = chunks(WEL)
    assert {("ɪ",), ("iː",), ("j",)} <= {s.segments for s in got["i"]}


def test_longest_chunk_first_beats_the_prefix():
    pat = parse_pattern("ts'a", chunks(GEO))
    assert [s.text for s in pat.slots] == ["ts'", "a"]


def test_the_glob_atoms_become_any_and_one_slots():
    pat = parse_pattern("a*r?", chunks(GEO))
    assert [s.kind for s in pat.slots] == [SEG, ANY, SEG, ONE]


def test_every_alternative_carries_its_respell_step():
    """V-31: provenance starts at the printed letter."""
    (slot,) = parse_pattern("a", chunks(GEO)).slots
    assert all(a.steps and a.steps[0].stage == "respell" for a in slot.alts)


def test_a_bracket_class_is_one_slot_carrying_the_unrespelled_letters():
    pat = parse_pattern("[ao]", chunks(GEO))
    (slot,) = pat.slots
    assert slot.kind == ONE and {("ɑ",), ("ɔ",)} <= alts(slot)


def test_an_unknown_letter_is_reported_and_treated_as_one():
    pat = parse_pattern("aqa", chunks(GEO))
    assert pat.slots[1].kind == ONE and pat.slots[1].alts == ()
    assert "no Irish source for 'q'" in pat.notes


def test_the_pattern_is_casefolded_and_nfc():
    assert parse_pattern("AR", chunks(GEO)).text == "ar"


@pytest.mark.parametrize("bad", ["[aeiou", "[!ao]", "[^ao]"])
def test_a_malformed_class_is_an_error_not_a_guess(bad):
    """V-16 (Q4): `[!…]` would make the parser and the verification fnmatch disagree."""
    with pytest.raises(ReverseError):
        parse_pattern(bad, chunks(GEO))


def test_env_text_renders_the_context_shapes():
    epen = next(r for r in GEO.sections["substitute"] if not r.target and r.replacement == ("v",))
    assert env_text(epen) == "[BROAD -labial] _ [V +front]"
    plain = next(r for r in GEO.sections["substitute"] if not r.left and not r.right)
    assert env_text(plain) == ""


# ---- --ipa mode (V-33 / F7) --------------------------------------------------------------------


def test_ipa_literals_are_tokenized_not_scanned_by_code_point():
    """A code-point scan would split `aː` and `tʃʰ`."""
    pat = parse_ipa_pattern("ɑrtʃʰ", GEO, TABLE)
    assert [s.text for s in pat.slots] == ["ɑ", "r", "tʃʰ"]


def test_a_long_vowel_is_one_slot():
    pat = parse_ipa_pattern("aː", WEL, TABLE)
    assert len(pat.slots) == 1 and pat.slots[0].alts[0].segments == ("aː",)


def test_glob_atoms_survive_between_literal_spans():
    pat = parse_ipa_pattern("ɑ*r?", GEO, TABLE)
    assert [s.kind for s in pat.slots] == [SEG, ANY, SEG, ONE]


def test_an_ipa_class_contains_whole_segments():
    pat = parse_ipa_pattern("[ɑɔ]", GEO, TABLE)
    (slot,) = pat.slots
    assert slot.kind == ONE and {a.segments for a in slot.alts} == {("ɑ",), ("ɔ",)}


def test_stress_and_syllable_marks_are_ignored():
    """spec §2."""
    assert len(parse_ipa_pattern("ˈɑ.r", GEO, TABLE).slots) == 2


def test_an_unknown_ipa_substring_is_an_error_naming_it():
    with pytest.raises(ReverseError) as exc:
        parse_ipa_pattern("ɑQ", GEO, TABLE)
    assert "Q" in str(exc.value)


def test_a_segment_outside_the_strand_is_a_note_not_an_error():
    pat = parse_ipa_pattern("θ", GEO, TABLE)  # θ tokenizes; Georgian has no /θ/
    assert any("georgian" in n.lower() or "θ" in n for n in pat.notes)


def test_ipa_mode_has_no_respell_step():
    """spec §2: 'the un-respell step is skipped'."""
    pat = parse_ipa_pattern("ɑr", GEO, TABLE)
    assert all(a.steps == () for s in pat.slots for a in s.alts)
