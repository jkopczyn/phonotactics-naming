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


def test_the_palette_is_the_spec_list_in_irish_ipa():
    assert len(PALETTE) == 15 and PALETTE[:5] == ("a", "ɛ", "ɪ", "ɔ", "ʊ")
    assert all(p in IRISH.inventory for p in PALETTE)


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
    examples, tried, _cap = verify(analysed(GEO, "ar*"), GEO, IRISH, TABLE, limit=5, cap=300)
    assert tried > 0
    for e in examples:
        assert fnmatch.fnmatchcase(unicodedata.normalize("NFC", e.respelling).casefold(), "ar*")


def test_a_match_that_is_not_the_first_spelling_is_still_found():
    """F8: draft 1 used `spell(...)[0]` only, which throws away most of what §3.4 produces —
    the spelling that matches the pattern is frequently not the first one.

    MEASURED deviation from the plan, which asserts `ardmhaor` here. That word's IPA is
    /aːɾˠd̪ˠvˠiːɾˠ/, so under `ar*v*` the trailing `*` would have to supply /iː ɾˠ/ — and R5's
    palette (V-23) is five SHORT vowels plus ten consonants, with no /iː/ in it. The candidate
    is therefore unreachable by construction, not by the `spell(...)[0]` bug this test is
    about; `spell(("aː","ɾˠ","d̪ˠ","vˠ","iː","ɾˠ"))` does return it, and Task 9's round trip is
    where a real word re-enters. What F8 is actually about is pinned instead: a spelling at
    index > 0 wins a place among the examples, which `spell(...)[0]` could never produce.
    """
    examples, _t, _c = verify(analysed(GEO, "ar*v*"), GEO, IRISH, TABLE, limit=40, cap=2000)
    assert examples
    assert any(e.spelling_index > 0 for e in examples), [
        (e.orthography, e.spelling_index) for e in examples]


def test_no_orthography_is_printed_twice():
    examples, _t, _c = verify(analysed(GEO, "ar*"), GEO, IRISH, TABLE, limit=8, cap=400)
    assert len({e.orthography for e in examples}) == len(examples)


def test_the_cap_counts_unique_forward_runs():
    """V-34: `tried` and the cap are the same counter, and a repeated spelling is skipped
    before any forward work."""
    _e, tried, cap_hit = verify(analysed(GEO, "a*a*"), GEO, IRISH, TABLE, limit=1, cap=10)
    assert tried <= 10 and cap_hit is True


def test_examples_are_ranked_by_fallbacks_then_flags_then_rank_then_spelling():
    examples, _t, _c = verify(analysed(GEO, "ar*"), GEO, IRISH, TABLE, limit=8, cap=400)
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
