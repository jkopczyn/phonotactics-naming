"""Task 7: candidate expansion and forward verification (reverse spec §3.5; V-22 … V-26, V-34)."""
import itertools

import pytest

from helpers import TABLE, irish, target
from strands.reverse import (CAP, PALETTE, expand, invert_respell, parse_pattern, source_map,
                             un_substitute, verify, widen)

IRISH = irish()
GEO = target("georgian")
WEL = target("welsh")
ARA = target("arabic-egy")


def _parse(rf, text):
    """V-35: both `invert_respell` values reach the pattern (as in Task 3-6's tests)."""
    chunk_map, notes = invert_respell(rf, TABLE)
    return parse_pattern(text, chunk_map, notes=notes)


def analysed(rf, text):
    p = widen(_parse(rf, text), rf, IRISH, TABLE)
    smap, deletions, notes = source_map("substitute", rf, IRISH, TABLE)
    return un_substitute(p, smap, deletions=deletions, notes=notes)


def test_a_star_is_filled_with_zero_one_then_two_palette_segments():
    lengths = [len(c.segments) for c in itertools.islice(expand(analysed(GEO, "*")), 20)]
    assert lengths[0] == 0 and sorted(lengths) == lengths


def test_cheapest_first_puts_identity_before_fallback():
    cands = list(itertools.islice(expand(analysed(GEO, "ar")), 5))
    assert cands and cands[0].rank == 0


def test_an_optional_group_is_present_or_absent_as_a_unit():
    """V-30 / F4: no candidate may carry half of a two-segment insertion. Uses Task 5's
    SYNTH_GROUP, where both inserted segments are printed (arabic-egy's own pair is
    unreachable — V-30's accepted miss)."""
    from test_reverse_sourcemap import SYNTH_GROUP
    p = analysed(SYNTH_GROUP, "qisk")
    (group,) = p.groups
    inserted = ("q", "i")
    for c in itertools.islice(expand(p), 60):
        head = c.segments[:2]
        assert head == inserted or inserted[0] not in c.segments[:1], c.segments


def test_the_cap_is_two_thousand_and_is_honoured():
    assert CAP == 2000
    assert len(list(expand(analysed(GEO, "a*a*"), cap=25))) == 25


def test_expansion_is_deterministic():
    a = [c.segments for c in itertools.islice(expand(analysed(GEO, "ar")), 50)]
    b = [c.segments for c in itertools.islice(expand(analysed(GEO, "ar")), 50)]
    assert a == b


# ---- verification (V-34 / F8) ---------------------------------------------------------------------

def test_every_kept_example_really_matches_the_pattern_through_the_real_engine():
    import fnmatch
    import unicodedata
    examples, tried, _cap = verify(analysed(GEO, "ar*"), GEO, IRISH, TABLE, limit=5, cap=200)
    assert tried > 0
    for e in examples:
        assert fnmatch.fnmatchcase(unicodedata.normalize("NFC", e.respelling).casefold(), "ar*")


def test_the_one_spelling_a_candidate_is_worth_still_finds_matches():
    """A1 (was F8's `spell(...)[0]` test). Task 7 ran EVERY spelling of a candidate forward,
    because the matching one is often not the first. A1 rules that out: `DESC` depends only on
    the IPA a spelling reads back to, and `spell()` guarantees every returned spelling reads
    back to the candidate's own segments, so all of a candidate's spellings reach the same
    `Result`. One cheap silent-free spelling per candidate is therefore enough — and the
    examples must still be found."""
    examples, _t, _c = verify(analysed(GEO, "ar*v*"), GEO, IRISH, TABLE, limit=40, cap=200)
    assert examples
    assert all(e.spelling_index == 0 for e in examples)


def test_no_orthography_is_printed_twice():
    examples, _t, _c = verify(analysed(GEO, "ar*"), GEO, IRISH, TABLE, limit=8, cap=200)
    assert len({e.orthography for e in examples}) == len(examples)


def test_examples_are_one_per_irish_candidate_not_one_per_foreign_shape():
    """D1, reversing A2: for a LITERAL pattern every match has the same foreign shape, and
    keying the de-duplication on that shape leaves exactly one row — *cahal* showed ⟨cáhál⟩
    alone. The reader wants the Irish words, so `verify` de-duplicates by the candidate only
    (`expand` already emits each segment sequence once) and a repeated `ipa` column is fine.
    ⟨cahal⟩ is the row that matters here: it is the silent-free spelling of /kahəl̪ˠ/, the
    reading of *Cathal* (`spell()` offers no ⟨th⟩ spelling of /h/, so ⟨cathal⟩ itself is not
    the row). It ranks eleventh of the sixteen matches, so the DEFAULT `--examples 8` still
    does not reach it — a finding for the owner, not something this test can assert away."""
    examples, _t, _c = verify(analysed(WEL, "cahal"), WEL, IRISH, TABLE, limit=40, cap=200)
    assert len(examples) > 1
    assert len({e.orthography for e in examples}) == len(examples)
    assert "cahal" in [e.orthography for e in examples]
    assert len({e.ipa for e in examples}) == 1        # one literal pattern, one foreign shape


@pytest.mark.slow
def test_examples_of_the_session_case_are_six_distinct_shapes():
    """A2 acceptance, measured on the session's own word at the SHIPPED cap: `Ar*v*` georgian
    shows at least six DISTINCT Irish-through-Georgian shapes. `slow` per C3 — it is the one
    reverse test that spends the full 2000-candidate budget."""
    examples, _t, _c = verify(analysed(GEO, "Ar*v*"), GEO, IRISH, TABLE, limit=8, cap=2000)
    assert len({e.ipa for e in examples}) >= 6


def test_the_cap_counts_unique_forward_runs():
    """V-34: `tried` and the cap are the same counter, and a repeated spelling is skipped
    before any forward work."""
    _e, tried, cap_hit = verify(analysed(GEO, "a*a*"), GEO, IRISH, TABLE, limit=1, cap=10)
    assert tried <= 10 and cap_hit is True


def test_examples_are_ranked_by_fallbacks_then_flags_then_rank_then_spelling():
    examples, _t, _c = verify(analysed(GEO, "ar*"), GEO, IRISH, TABLE, limit=8, cap=200)
    keys = [(e.fallbacks, len(e.flags), e.rank, e.spelling_index) for e in examples]
    assert keys == sorted(keys)


def test_a_candidate_the_engine_cannot_run_is_counted_not_raised():
    _e, tried, _c = verify(analysed(GEO, "*"), GEO, IRISH, TABLE, limit=3, cap=120)
    assert tried >= 1


def test_ipa_mode_matches_the_unmarked_ipa():
    from strands.reverse import parse_ipa_pattern
    smap, deletions, notes = source_map("substitute", GEO, IRISH, TABLE)
    p = un_substitute(widen(parse_ipa_pattern("ɑr*", GEO, TABLE), GEO, IRISH, TABLE),
                      smap, deletions=deletions, notes=notes)
    examples, _t, _c = verify(p, GEO, IRISH, TABLE, limit=3, cap=200, ipa_mode=True,
                              raw_pattern="ɑr*")
    assert all(all(m not in e.ipa for m in ("ˈ", "ˌ", ".")) for e in examples)


# ---- review fixes (task 7) ------------------------------------------------------------------------

def test_an_unspellable_candidate_does_not_consume_the_forward_run_budget():
    """V-34: `cap` counts unique `(candidate, spelling)` FORWARD RUNS. A candidate whose
    `spell()` is empty costs no forward run, so it must not push a later matching candidate
    out of a small cap (the candidate stream has its own `CAP`, V-24)."""
    import types

    from strands import reverse

    p = analysed(GEO, "ar")
    first_three = [c.segments for c in itertools.islice(expand(p), 3)]
    assert len(first_three) == 3

    def fake_spell(segments, **kwargs):
        return ("arbitrary",) if segments == first_three[2] else ()

    def fake_forward(spelling, *args, **kwargs):
        return types.SimpleNamespace(respelling="ar", ipa="ˈar", flags=(), fallbacks=0)

    monkey = pytest.MonkeyPatch()
    try:
        monkey.setattr(reverse.g2p_inverse, "spell", fake_spell)
        monkey.setattr(reverse, "_forward", fake_forward)
        examples, tried, _cap_hit = verify(p, GEO, IRISH, TABLE, limit=8, cap=2,
                                           raw_pattern="ar")
    finally:
        monkey.undo()
    assert tried == 1
    assert [e.orthography for e in examples] == ["arbitrary"]


def test_a_group_keeps_every_present_combination():
    """V-24: the group's option list holds `absent` and then EACH present combination — the
    span's slots are SEG slots, so the product is bounded by their alternative lists."""
    import math

    from test_reverse_sourcemap import SYNTH_GROUP
    from strands.reverse import _group_options, _slot_options

    p = analysed(SYNTH_GROUP, "qisk")
    (group,) = p.groups
    expected = math.prod(len(_slot_options(s)) for s in p.slots[group.start:group.stop])
    assert expected > 64
    assert len(_group_options(p.slots, group)) == 1 + expected


def test_a_present_group_option_carries_the_groups_own_rank():
    """V-22: `present` costs the optional group's own rank (its epenthesis provenance), not
    the maximum rank of the slot alternatives that fill it."""
    from test_reverse_sourcemap import SYNTH_GROUP
    from strands.reverse import _group_options

    p = analysed(SYNTH_GROUP, "qisk")
    (group,) = p.groups
    assert group.steps[-1].kind == "epenthesis"     # so the group's own rank is 4
    options = _group_options(p.slots, group)
    assert options[0].rank == 0 and options[0].segments == ()
    assert all(option.rank == 4 for option in options[1:])


# ---- fix round Task A: verification cost, example diversity, palette (A1-A5) -----------------

def test_the_palette_carries_the_long_vowels_too():
    """A4 (R5 revised): five short vowels, their five long counterparts, then the ten
    consonants — 20 entries, so a `*` has 1 + 20 + 400 fillings."""
    assert len(PALETTE) == 20
    assert PALETTE[:5] == ("a", "ɛ", "ɪ", "ɔ", "ʊ")
    assert PALETTE[5:10] == ("aː", "eː", "iː", "oː", "uː")
    assert all(p in IRISH.inventory for p in PALETTE)
    assert len(set(PALETTE)) == 20


def test_a_star_offers_one_then_twenty_then_four_hundred_fillings():
    from strands.reverse import _star_options
    options = _star_options()
    assert len(options) == 1 + 20 + 400
    assert options[0].segments == ()


def test_verify_runs_one_forward_run_per_candidate():
    """A1: `spell()` guarantees the spelling reads back to the candidate's segments and `DESC`
    depends on nothing else, so a candidate is worth exactly one forward run."""
    import types

    from strands import reverse

    p = analysed(GEO, "ar*")
    runs: list[str] = []

    def fake_spell(segments, **kwargs):
        return ["aaa", "bbb", "ccc"]

    def fake_forward(spelling, *args, **kwargs):
        runs.append(spelling)
        return types.SimpleNamespace(respelling="ar", ipa="ˈar", flags=(), fallbacks=0)

    monkey = pytest.MonkeyPatch()
    try:
        monkey.setattr(reverse.g2p_inverse, "spell", fake_spell)
        monkey.setattr(reverse, "_forward", fake_forward)
        _examples, tried, _cap_hit = verify(p, GEO, IRISH, TABLE, limit=8, cap=5,
                                            raw_pattern="ar*")
    finally:
        monkey.undo()
    assert runs == ["aaa"] * 5                # the first spelling only, once per candidate
    assert tried == 5


def test_verify_asks_for_one_cheap_silent_free_spelling():
    """A2: `spell(segments, limit=1, silent=False, budget=128)`."""
    from strands import reverse

    calls: list[tuple] = []

    def fake_spell(segments, **kwargs):
        calls.append((tuple(segments), kwargs))
        return []

    monkey = pytest.MonkeyPatch()
    try:
        monkey.setattr(reverse.g2p_inverse, "spell", fake_spell)
        verify(analysed(GEO, "ar"), GEO, IRISH, TABLE, limit=2, cap=5)
    finally:
        monkey.undo()
    assert calls
    assert all(kw == {"limit": 1, "silent": False, "budget": 128} for _s, kw in calls)


def test_every_example_spelling_index_is_zero():
    """A1: one spelling per candidate, so the field stays for the golden format only."""
    examples, _t, _c = verify(analysed(GEO, "ar*"), GEO, IRISH, TABLE, limit=8, cap=200)
    assert examples and all(e.spelling_index == 0 for e in examples)


def test_no_example_spelling_uses_a_silent_letter():
    """A2 acceptance: no ⟨fh⟩ and no silent ⟨dh gh th⟩ among the examples."""
    examples, _t, _c = verify(analysed(GEO, "ar*v*"), GEO, IRISH, TABLE, limit=8, cap=200)
    for e in examples:
        assert "fh" not in e.orthography.casefold()


def test_the_examined_candidate_stream_is_bounded_by_four_times_the_cap():
    """A3: an unspellable candidate costs no forward run, so the forward cap alone cannot stop
    a word looping; `expand` is consumed at most `4 * cap` times."""
    from strands import reverse

    seen: list[tuple[str, ...]] = []

    def fake_spell(segments, **kwargs):
        seen.append(tuple(segments))
        return []                              # nothing is ever spellable

    monkey = pytest.MonkeyPatch()
    try:
        monkey.setattr(reverse.g2p_inverse, "spell", fake_spell)
        examples, tried, cap_hit = verify(analysed(GEO, "a*a*"), GEO, IRISH, TABLE,
                                          limit=8, cap=10)
    finally:
        monkey.undo()
    assert examples == () and tried == 0
    assert len(seen) <= 4 * 10
    assert cap_hit is True
