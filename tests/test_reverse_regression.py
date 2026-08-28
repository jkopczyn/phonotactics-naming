"""Task 9 (fix round C1): the reverse round trip per strand (reverse spec §6).

Two rates per strand, measured by two different runs because they cost very differently:

- **`admits`** — every `sources/irish/test-words.tsv` hand-IPA row, run forward and then
  reversed with the **`--examples 0` machinery** (no verification at all), asking only whether
  the row's own Irish IPA is admitted by the resulting pattern (`pattern_admits`). No forward
  run is spent per candidate, so the whole thing is cheap and its ratchet test is unmarked.
- **`examples`** — the FIRST `EXAMPLE_ROWS` hand-IPA rows only, at `cap=EXAMPLE_CAP`, asking
  whether the row's own spelling — or any spelling that reads to the same Irish IPA — is among
  the verified examples. Every row here pays up to `EXAMPLE_CAP` forward runs, so the fixture
  is requested only by `slow` tests and `-m "not slow"` never builds it.

`tests/ratchets/reverse-<strand>.json` holds `admits`, `admits_n`, `examples`, `examples_n`.
There is no floor (spec §6): the ratchet only forbids regression. Regenerate it by hand with
the script in Task 9 Step 5 of `docs/plans/2026-08-27-reverse-plan.md`.
"""

import json

import pytest
from helpers import ROOT, TABLE, irish, target

from strands.reverse import read_hand_ipa_rows, reverse_regression

IRISH = irish()
STRANDS = ("welsh", "georgian", "arabic-egy", "dutch")

#: C1: the example rate is measured over the first twelve hand-IPA rows, at cap 200.
EXAMPLE_ROWS = 12
EXAMPLE_CAP = 200


@pytest.fixture(scope="session")
def admits():
    """The cheap run: `limit=0`, so `verify` is never called (F6 keeps it session-scoped)."""
    return {name: reverse_regression(name, target(name), IRISH, TABLE, limit=0) for name in STRANDS}


@pytest.fixture(scope="session")
def examples():
    """The paid run. Session-scoped and requested only by `slow` tests, so `-m "not slow"`
    never pays for it."""
    rows = read_hand_ipa_rows()[:EXAMPLE_ROWS]
    return {
        name: reverse_regression(name, target(name), IRISH, TABLE, cap=EXAMPLE_CAP, rows=rows)
        for name in STRANDS
    }


def ratchet(name):
    return json.loads(
        (ROOT / "tests" / "ratchets" / f"reverse-{name}.json").read_text(encoding="utf-8")
    )


# ---- the ratchets ------------------------------------------------------------------------------


def test_the_ratchet_files_all_exist_and_carry_the_four_keys():
    """Unmarked and cheap: a missing or malformed ratchet file fails fast."""
    for name in STRANDS:
        assert set(ratchet(name)) == {"admits", "admits_n", "examples", "examples_n"}


@pytest.mark.parametrize("name", STRANDS)
def test_the_admit_ratchet_holds(name, admits):
    """C1: all rows, unmarked, cheap — no verification is involved."""
    data, rep = ratchet(name), admits[name]
    assert rep.admit_rate >= data["admits"] - 1e-9, rep.summary()
    assert rep.n == data["admits_n"], rep.summary()


@pytest.mark.parametrize("name", STRANDS)
def test_the_admit_run_spends_no_forward_runs(name, admits):
    """`limit=0` is the `--examples 0` path: nothing is verified, so nothing is tried."""
    rep = admits[name]
    assert rep.cap == 0 and all(row.tried == 0 and not row.found for row in rep.rows)


@pytest.mark.slow
@pytest.mark.parametrize("name", STRANDS)
def test_the_example_ratchet_holds(name, examples):
    """C1: the first twelve rows at cap 200 — the expensive half of the round trip."""
    data, rep = ratchet(name), examples[name]
    assert rep.cap == EXAMPLE_CAP
    assert rep.example_rate >= data["examples"] - 1e-9, rep.summary()
    assert rep.n == data["examples_n"], rep.summary()


@pytest.mark.slow
@pytest.mark.parametrize("name", STRANDS)
def test_the_example_run_reads_at_most_the_first_twelve_rows(name, examples):
    assert examples[name].n <= EXAMPLE_ROWS


def test_a_row_is_found_by_any_spelling_that_reads_to_its_own_ipa():
    """C1: the row's orthography OR any spelling that reads to the same IPA counts. `verify`
    returns one silent-free spelling per candidate (A2), which is frequently not the row's own
    spelling of that reading — ⟨arbha⟩ for ⟨arḃa⟩-style variants — and the round trip is about
    the reading, not the choice of letters."""
    from strands.reverse import _reads_the_same

    assert _reads_the_same("ardmhaor", "Ardmhaor")  # the fold survives
    assert _reads_the_same("bord", "bhord") is False  # a real minimal pair does not
    assert not _reads_the_same("ardmhaor", "carraig")
    assert not _reads_the_same("ardmhaor", "qqq")  # unreadable is not a match


# ---- the smoke run -----------------------------------------------------------------------------

#: The determinism check runs the machinery twice, so it takes the first two rows only.
SMOKE_ROWS = 2


def test_the_smoke_run_is_deterministic_and_is_not_the_ratchet():
    rows = read_hand_ipa_rows()[:SMOKE_ROWS]
    kw = dict(cap=EXAMPLE_CAP, rows=rows)
    a = reverse_regression("georgian", target("georgian"), IRISH, TABLE, **kw)
    b = reverse_regression("georgian", target("georgian"), IRISH, TABLE, **kw)
    assert a.rows == b.rows and a.cap == EXAMPLE_CAP


# ---- the session case (spec §6 bullet 4) -------------------------------------------------------


def _parse(rf, text):
    """The plan's Task 9 listing calls `_parse(geo, text)` without defining it; this is the
    parse half of `cli.cmd_reverse`'s own sequence (invert_respell -> parse_pattern)."""
    from strands.reverse import invert_respell, parse_pattern

    chunks, chunk_notes = invert_respell(rf, TABLE)
    return parse_pattern(text, chunks, notes=chunk_notes)


def analysed_geo(text):
    from strands.reverse import source_map, un_substitute, widen

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
    assert any("bh" in d for _k, d in kinds)  # /w/ from broad bh/mh
    assert any("slender" in d for _k, d in kinds)  # /vʲ/ from slender bh/mh


def test_ardmhaor_is_admitted():
    """C2: unmarked and cheap — the pattern `Ar*v*` must ADMIT /aːɾˠd̪ˠvˠiːɾˠ/, which is what
    A4's long-vowel palette was widened for."""
    from strands import g2p
    from strands.reverse import pattern_admits, tokenize

    _geo, p = analysed_geo("ar*v*")
    segments = tokenize(g2p.g2p("ardmhaor")[0], TABLE).segments
    assert pattern_admits(p, segments)


@pytest.mark.slow
@pytest.mark.xfail(
    strict=True,
    reason=(
        "C2 FINDING, for owner review, not a test to delete; RE-MEASURED after D6. After A4 widened "
        "the palette the pattern ADMITS /aːɾˠd̪ˠvˠiːɾˠ/ (the test above) and every piece is on "
        "offer — the first `*` can be /d̪ˠ/ and the second /iːɾˠ/ — but that filling is nowhere "
        "near the front of the stream. D6 raised `expand`'s own cap from 2000 to EXAMINE_FACTOR * "
        "cap = 8000, which took `Ar*v*` from 106 candidates tried to 608 and from 1 example to the "
        "full 8 asked for; *ardmhaor* is still not among them, because both `*` slots offer 421 "
        "fillings each and the two-segment ones are ranked last. So this remains an ENUMERATION "
        "ORDER limit, not a cap that one more factor would fix: interleaving the `*` fillings "
        "(breadth over the cross product rather than depth) is what would reach it — the owner's "
        "call. `Ar*v*` costs 27 s at the shipped cap after D6."
    ),
)
def test_ardmhaor_verifies_for_the_session_case():
    """C2/spec §6 bullet 4: the word itself among the verified examples at the shipped cap."""
    from strands.reverse import CAP, verify

    geo, p = analysed_geo("ar*v*")
    examples, _t, _c = verify(p, geo, IRISH, TABLE, limit=40, cap=CAP)
    assert any(e.orthography == "ardmhaor" for e in examples), [e.orthography for e in examples]


# ---- `pattern_admits` itself (the plan lists no unit test for it; these are cheap and unmarked,
# so the matcher's semantics are not covered by the slow pass alone) -----------------------------

from strands.reverse import (  # noqa: E402
    ANY,
    ONE,
    SEG,
    Alternative,
    OptionalGroup,
    Pattern,
    Slot,
    pattern_admits,
)


def _seg(text, *sequences):
    return Slot(kind=SEG, text=text, alts=tuple(Alternative(segments=tuple(s)) for s in sequences))


def test_a_seg_slot_admits_any_one_of_its_alternatives_in_full():
    p = Pattern(text="ab", slots=(_seg("a", ("a",), ("ɪ", "ə")), _seg("b", ("bˠ",))))
    assert pattern_admits(p, ("a", "bˠ"))
    assert pattern_admits(p, ("ɪ", "ə", "bˠ"))  # a two-segment alternative, whole
    assert not pattern_admits(p, ("ɪ", "bˠ"))  # half of one is not an alternative


def test_an_optional_group_is_skipped_as_a_unit_never_half():
    slots = (_seg("a", ("a",)), _seg("i", ("i",)), _seg("b", ("bˠ",)))
    p = Pattern(
        text="aib", slots=slots, groups=(OptionalGroup(start=0, stop=2, steps=(), note=""),)
    )
    assert pattern_admits(p, ("a", "i", "bˠ"))  # present
    assert pattern_admits(p, ("bˠ",))  # absent
    assert not pattern_admits(p, ("i", "bˠ"))  # V-30: not half-present


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
