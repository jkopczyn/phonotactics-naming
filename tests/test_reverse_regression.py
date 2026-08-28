"""Task 9: the reverse round trip per strand (reverse spec §6 bullets 3-4).

The ratchet is measured at the SHIPPED cap (reverse.CAP = 2000), so it is slow; run
`uv run pytest -q -m "not slow"` to skip it. The cap=200 run below is a smoke test, not a
ratchet.

**The four ratchet files do not exist yet and the tests that read them are skipped until they
do** (`needs_ratchets`). Generating them is Task 9 step 5, and it is BLOCKED on runtime: at
`cap=CAP` one strand-row costs a `g2p_inverse.spell()` call per candidate the stream produces
(0.3-1 s each for a long word; ~1300 candidates for Welsh *llasyrchos*), and the forward-run
cap does not bound that, because a candidate that spells to nothing costs no forward run.
Measured on this branch: Dutch ~7 s/row, arabic-egy ~16 s/row, Georgian 200 s+ on a single row
and Welsh 20 min+ on a single row — hours per strand, not the ~2 minutes for four strands the
plan's F9 assumed. The plan rules out the two obvious fixes (a smaller cap, a smaller row set)
and sanctions "better pruning inside verify", which is a Task 7 change; it needs the owner's
ruling.

For reference, `uv run pytest -q -m "not slow"` — the whole suite without this module's slow
pass — takes about 13 minutes on this branch."""
import json

import pytest

from helpers import ROOT, TABLE, irish, target
from strands.reverse import CAP, read_hand_ipa_rows, reverse_regression

IRISH = irish()
STRANDS = ("welsh", "georgian", "arabic-egy", "dutch")


@pytest.fixture(scope="session")
def full():
    """F6: session-scoped, so `-m \"not slow\"` never pays for it. Only `slow` tests ask."""
    return {name: reverse_regression(name, target(name), IRISH, TABLE, cap=CAP)
            for name in STRANDS}


#: The plan calls the cap=200 run "a separate, FAST smoke test ... it asserts only that the
#: machinery runs and is deterministic". Over all 144 hand-IPA rows it is not fast — a long
#: word costs minutes at ANY cap, because `verify` pays a `g2p_inverse.spell()` call on every
#: candidate the stream produces and the forward-run cap does not bound that — and the
#: determinism check runs it twice. So the smoke run takes the first `SMOKE_ROWS` rows: the
#: assertion is about the machinery, not a rate, and no ratchet is derived from it.
SMOKE_ROWS = 2


@pytest.fixture(scope="session")
def smoke():
    return reverse_regression("georgian", target("georgian"), IRISH, TABLE, cap=200,
                              rows=read_hand_ipa_rows()[:SMOKE_ROWS])


#: The ratchet-reading tests skip themselves while `tests/ratchets/reverse-*.json` is missing:
#: as soon as step 5 has been run they run, with no further edit.
needs_ratchets = pytest.mark.skipif(
    not all((ROOT / "tests" / "ratchets" / f"reverse-{name}.json").exists()
            for name in STRANDS),
    reason="tests/ratchets/reverse-*.json not generated yet (Task 9 step 5, see docstring)")


def ratchet(name):
    return json.loads((ROOT / "tests" / "ratchets" / f"reverse-{name}.json")
                      .read_text(encoding="utf-8"))


@needs_ratchets
@pytest.mark.slow
@pytest.mark.parametrize("name", STRANDS)
def test_the_ratchet_holds_at_the_shipped_cap(name, full):
    """F9: the ratchet must describe the command the user actually runs."""
    data, rep = ratchet(name), full[name]
    assert rep.cap == CAP
    assert rep.pattern_rate >= data["pattern"] - 1e-9, rep.summary()
    assert rep.example_rate >= data["example"] - 1e-9, rep.summary()


@needs_ratchets
@pytest.mark.slow
@pytest.mark.parametrize("name", STRANDS)
def test_the_ratchet_records_its_denominators(name, full):
    data = ratchet(name)
    assert set(data) == {"pattern", "example", "n", "capped"}
    assert data["n"] == full[name].n


@needs_ratchets
@pytest.mark.slow
@pytest.mark.parametrize("name", STRANDS)
def test_the_example_rate_excludes_the_capped_rows(name, full):
    """spec §6: 'when the candidate cap is not hit'."""
    rep = full[name]
    assert rep.example_denominator == rep.n - rep.capped


@needs_ratchets
def test_the_ratchet_files_all_exist_without_running_the_slow_pass():
    """Unmarked, cheap: a missing or malformed ratchet file fails fast."""
    for name in STRANDS:
        assert set(ratchet(name)) == {"pattern", "example", "n", "capped"}


def test_the_smoke_run_is_deterministic_and_is_not_the_ratchet(smoke):
    again = reverse_regression("georgian", target("georgian"), IRISH, TABLE, cap=200,
                               rows=read_hand_ipa_rows()[:SMOKE_ROWS])
    assert again.rows == smoke.rows and smoke.cap == 200


# ---- the session case (spec §6 bullet 4) -------------------------------------------------------

def _parse(rf, text):
    """The plan's Task 9 listing calls `_parse(geo, text)` without defining it; this is the
    parse half of `cli.cmd_reverse`'s own sequence (invert_respell -> parse_pattern)."""
    from strands.reverse import invert_respell, parse_pattern
    chunks, chunk_notes = invert_respell(rf, TABLE)
    return parse_pattern(text, chunks, notes=chunk_notes)


def analysed_geo(text):
    from strands.reverse import (invert_respell, parse_pattern, source_map, un_substitute,
                                 widen)
    geo = target("georgian")
    p = widen(_parse(geo, text), geo, IRISH, TABLE)
    smap, deletions, notes = source_map("substitute", geo, IRISH, TABLE)
    return geo, un_substitute(p, smap, deletions=deletions, notes=notes)


def test_the_session_case_lists_exactly_the_three_v_sources():
    from strands.reverse import constraints
    _geo, p = analysed_geo("ar*v*")
    v = [c for c in constraints(p) if c.label == "v"][0]
    kinds = {(l.kind, l.description) for l in v.lines}
    assert ("epenthesis", "inserted, no Irish letter") in kinds
    assert any("bh" in d for _k, d in kinds)          # /w/ from broad bh/mh
    assert any("slender" in d for _k, d in kinds)     # /vʲ/ from slender bh/mh


@pytest.mark.xfail(strict=True, reason=(
    "Task 9 step 5/6 FINDING, for owner review, not a test to delete. `ardmhaor` really is a "
    "verifying example — g2p reads it as /aːɾˠd̪ˠvˠiːɾˠ/, the forward run respells it 'ardvyr' "
    "(/ɑrdvir/), which matches ar*v*, the pattern ADMITS its segments, and spell() proposes it "
    "at spelling_index 27 of 64. It is excluded by R5's PALETTE (V-23): the second `*` has to "
    "supply /iː ɾˠ/ and the palette holds the five SHORT vowels only, so no filling of that "
    "slot ever reaches /iː/. Not the cap, not caol-le-caol, not a missing g2p_inverse reading. "
    "The spec's own §4 illustration assumed 'ardmhaor' ends in /aː/ ('ardvar', /ɑrdvɑr/); the "
    "engine's g2p says /iː/. Fixing it means widening the palette (an R5 decision) or letting "
    "a `*` draw the long counterpart of each palette vowel — the owner's call."))
def test_ardmhaor_verifies_for_the_session_case():
    from strands.reverse import verify
    geo, p = analysed_geo("ar*v*")
    examples, _t, _c = verify(p, geo, IRISH, TABLE, limit=40, cap=CAP)
    assert any(e.orthography == "ardmhaor" for e in examples), [e.orthography for e in examples]


# ---- `pattern_admits` itself (the plan lists no unit test for it; these are cheap and unmarked,
# so the matcher's semantics are not covered by the slow pass alone) -----------------------------

from strands.reverse import (ANY, ONE, SEG, Alternative, OptionalGroup,  # noqa: E402
                             Pattern, Slot, pattern_admits)


def _seg(text, *sequences):
    return Slot(kind=SEG, text=text,
                alts=tuple(Alternative(segments=tuple(s)) for s in sequences))


def test_a_seg_slot_admits_any_one_of_its_alternatives_in_full():
    p = Pattern(text="ab", slots=(_seg("a", ("a",), ("ɪ", "ə")), _seg("b", ("bˠ",))))
    assert pattern_admits(p, ("a", "bˠ"))
    assert pattern_admits(p, ("ɪ", "ə", "bˠ"))          # a two-segment alternative, whole
    assert not pattern_admits(p, ("ɪ", "bˠ"))           # half of one is not an alternative


def test_an_optional_group_is_skipped_as_a_unit_never_half():
    slots = (_seg("a", ("a",)), _seg("i", ("i",)), _seg("b", ("bˠ",)))
    p = Pattern(text="aib", slots=slots,
                groups=(OptionalGroup(start=0, stop=2, steps=(), note=""),))
    assert pattern_admits(p, ("a", "i", "bˠ"))          # present
    assert pattern_admits(p, ("bˠ",))                   # absent
    assert not pattern_admits(p, ("i", "bˠ"))           # V-30: not half-present


def test_a_star_consumes_any_run_and_a_bare_one_consumes_exactly_one():
    p = Pattern(text="*?", slots=(Slot(kind=ANY, text="*"), Slot(kind=ONE, text="?")))
    assert pattern_admits(p, ("a",)) and pattern_admits(p, ("a", "bˠ", "k"))
    assert not pattern_admits(p, ())


def test_a_slot_with_no_irish_source_admits_nothing():
    """The one place reverse does not over-generate (`_slot_options`): Welsh th ← /θ/."""
    assert not pattern_admits(Pattern(text="x", slots=(Slot(kind=SEG, text="x"),)), ("x",))


def test_stress_and_syllable_marks_in_the_ipa_are_ignored():
    p = Pattern(text="a", slots=(_seg("a", ("a",)),))
    assert pattern_admits(p, ("ˈ", "a", "."))
