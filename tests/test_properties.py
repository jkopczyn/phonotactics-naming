"""Plan Task 28 (spec §8 layer 5): cross-target property checks over every test word, for
every construction the CLI can build from a single entry (`run --construction all`, the
gallery). Multi-slot templates (ADJ, OF, COMPOUND) raise MissingSlot and are skipped, exactly
as `strands run` skips them."""
import functools

import pytest

from helpers import TABLE, entry_of, irish, read_allow_file, read_test_words
from strands.irish import MissingSlot
from strands.pipeline import CONSTRUCTIONS, TARGETS, load_target, run_entry

IRISH = irish()
ROWS = read_test_words()
ENTRIES = [entry_of(row) for row in ROWS]
RF = {name: load_target(name, TABLE) for name in TARGETS}
CASES = [(name, construction) for name in TARGETS for construction in CONSTRUCTIONS]


def _run(name, construction, i):
    try:
        return run_entry(ENTRIES[i], construction, IRISH, RF[name], TABLE)
    except MissingSlot:
        return None


@functools.lru_cache(maxsize=None)
def _first(name, construction, i):
    return _run(name, construction, i)


def _results(name, construction):
    """(row, result) for every entry the construction can be built from."""
    for i, row in enumerate(ROWS):
        result = _first(name, construction, i)
        if result is not None:
            yield row, result


@pytest.mark.parametrize("name,construction", CASES)
def test_determinism_across_two_runs(name, construction):
    for i, row in enumerate(ROWS):
        assert _first(name, construction, i) == _run(name, construction, i), \
            (name, construction, row["orthography"])


@pytest.mark.parametrize("name,construction", CASES)
def test_every_output_segment_is_in_the_target_inventory(name, construction):
    inventory = set(RF[name].inventory)
    for row, result in _results(name, construction):
        for word in result.words:
            assert set(word.segments) <= inventory, \
                (name, construction, row["orthography"], word.segments)


def test_no_unrepaired_outside_the_allow_file():
    allowed = read_allow_file()
    bad = [(name, construction, row["orthography"])
           for name, construction in CASES
           for row, result in _results(name, construction)
           if "UNREPAIRED" in result.flags and (name, row["orthography"]) not in allowed]
    assert bad == [], bad


@pytest.mark.parametrize("name,construction", CASES)
def test_every_word_gets_exactly_one_primary_stress(name, construction):
    for row, result in _results(name, construction):
        for word in result.words:
            assert word.stress is not None, (name, construction, row["orthography"])
            assert 0 <= word.stress < len(word.syllables), \
                (name, construction, row["orthography"])


@pytest.mark.parametrize("name", TARGETS)
def test_traces_are_never_empty(name):
    assert run_entry(ENTRIES[0], "DESC", IRISH, RF[name], TABLE).trace


def test_every_single_entry_construction_is_covered():
    """The multi-slot templates are the only ones skipped for every entry."""
    skipped = {c for name, c in CASES if not any(True for _ in _results(name, c))}
    assert skipped == {"ADJ", "OF", "COMPOUND"}, skipped


# ---- lenition /h/ is not a dorsal fricative in any target -------------------------------

@pytest.mark.parametrize("orthography", ["theach", "shúil"])
@pytest.mark.parametrize("name", TARGETS)
def test_initial_lenition_h_never_surfaces_as_a_dorsal_fricative(name, orthography):
    """*theach* /hax/ and *shúil* /huːlʲ/ are lenited forms whose initial is /h/. Irish
    [ç] is an allophone of /h/ only where the /h/ is the lenition of the SLENDER /tʲ ʃ/
    (digest §1.1 [wiki-irish-phonology §Allophones]); [normalize] cannot see that
    provenance, so it must leave /h/ alone. Before the fix a blanket `h -> ç` turned both
    into /ç/ and every target then rendered them with a dorsal fricative (*chach*, *chŵl*).
    """
    row = next(r for r in ROWS if r["orthography"] == orthography)
    result = run_entry(entry_of(row), "DESC", IRISH, RF[name], TABLE)
    first = result.words[0].segments[0]
    assert first not in ("x", "χ", "ç", "ʁ", "ɣ"), (name, orthography, result.ipa)
