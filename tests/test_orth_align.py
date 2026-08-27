"""Task 5: the modern-orthography <-> IPA aligner (spec §4, §11; O-6, O-7)."""

import pytest
from helpers import TABLE, irish, read_test_words, w

from strands.irish import normalize
from strands.orth import align, load_orth_table, tag_word

IRISH = irish()


def segs(ipa):
    """R6: the REAL call site normalizes first; draft 1's helper did not, so three of its
    own positive assertions returned all-empty tags."""
    return normalize(w(ipa), IRISH, TABLE).segments


def tags(orthography, ipa):
    return align(orthography, segs(ipa))


def test_the_table_is_sorted_longest_unit_first():
    lengths = [len(unit) for unit, _ in load_orth_table()]
    assert lengths == sorted(lengths, reverse=True)


# ---- pinned tags: S2's guard against an agent optimising the counter ----------------------


@pytest.mark.parametrize(
    "orthography,ipa,expected",
    [
        ("Niamh", "nʲiəvˠ", ("n", "ia:1", "ia:2", "mh")),
        ("gorm", "ɡɔɾˠəmˠ", ("g", "o", "r:1", "r:2", "m")),
        ("Seán", "ʃaːnˠ", ("s", "eá", "n")),
        ("naomh", "n̪ˠiːw", ("n", "ao", "mh")),
        ("Caoimhe", "kiːvʲə", ("c", "aoi", "mh", "e")),
        ("dubh", "d̪ˠʊw", ("d", "u", "bh")),
        ("sneachta", "ʃnʲaxt̪ˠə", ("s", "n", "ea", "ch", "t", "a")),
        ("baid", "bˠaːdʲ", ("b", "ai", "d")),  # R10: the `ai` row exists, so <ai> tags `ai`
        ("Colm", "ˈkɔl̪ˠəmˠ", ("c", "o", "l:1", "l:2", "m")),
        ("mbean", "mʲanˠ", ("mb", "ea", "n")),
        ("bpeann", "bʲaːn̪ˠ", ("bp", "ea", "nn")),
        ("caisleán", "kaʃlʲaːnˠ", ("c", "ai", "s", "l", "eá", "n")),
    ],
)
def test_the_pinned_tags_are_exact(orthography, ipa, expected):
    """Every one of these is a real corpus row. The multi-segment units carry POSITIONAL
    tags (O-6): the epenthetic schwa is `r:2`/`l:2`, the diphthong halves are `ia:1`/`ia:2`."""
    assert tags(orthography, ipa) == expected


@pytest.mark.parametrize(
    "orthography,ipa,expected",
    [
        ("bhí", "vʲiː", ("bh", "í")),
        ("mhac", "wak", ("mh", "a", "c")),
        ("dhún", "ɣuːnˠ", ("dh", "ú", "n")),
        ("chos", "xɔsˠ", ("ch", "o", "s")),
        ("phóg", "fˠoːɡ", ("ph", "ó", "g")),
        ("shúil", "huːlʲ", ("sh", "ú", "l")),
    ],
)
def test_the_reversal_relevant_digraphs_all_align(orthography, ipa, expected):
    assert tags(orthography, ipa) == expected


def test_a_single_segment_unit_carries_no_position_suffix():
    assert ":" not in "".join(tags("gorm", "ɡɔɾˠmˠ"))


# ---- the algorithm's own properties -------------------------------------------------------


def test_backtracking_is_required_and_works():
    """Measured: 14 of 144 words need it. *long* is the minimal case — `ng -> (ŋ,)` is tried
    first and dead-ends, then `ng -> (ŋ, ɡ)` completes. The dead-node memo must PRUNE only."""
    assert tags("long", "l̪ˠuːŋɡ") == ("l", "o", "ng:1", "ng:2")


def test_alignment_is_deterministic():
    a = tags("Colm", "ˈkɔl̪ˠəmˠ")
    for _ in range(3):
        assert tags("Colm", "ˈkɔl̪ˠəmˠ") == a


def test_alignment_failure_returns_all_empty_tags_and_never_raises():
    """O-7: the tag is ABSENT, not guessed, so only sound-based rules apply."""
    assert tags("Seán", "xɔsˠ") == ("", "", "")
    assert align("", ("ɡ", "ɔ")) == ("", "")


def test_hyphens_apostrophes_and_spaces_are_ignored():
    assert tags("t-éan", "tʲeːnˠ") == ("t", "é", "n")


def test_tag_word_sets_the_channel_and_records_a_failure_in_the_trace():
    good = tag_word(w("ɡɔɾˠmˠ"), "gorm")
    assert good.orth == ("g", "o", "r", "m") and len(good.orth) == len(good.segments)
    bad = tag_word(w("ɡɔɾˠmˠ"), "Seán")
    assert bad.orth == ("", "", "", "")
    assert any(t.rule_id == "orth:unaligned" for t in bad.trace)


def test_the_orth_channel_survives_replacement_and_splitting():
    word = tag_word(w("ɡɔɾˠmˠ"), "gorm")
    assert word.replaced(0, 1, ("k",)).orth == ("g", "o", "r", "m")
    assert word.replaced(1, 2, ("ɔ", "ə")).orth == ("g", "o", "o", "r", "m")
    assert word.replaced(1, 3, ("a",)).orth == ("g", "o", "m")


def test_the_orth_channel_survives_a_join():
    """R7: `irish._join` constructs Word(...) literally and dropped the channel, losing the
    tags on every constructed word."""
    from strands.irish import _join

    a = tag_word(w("ə"), "a")
    b = tag_word(w("çaːnʲ"), "Sheáin")  # lenited s before a slender vowel is /ç/ (digest §5.3)
    joined = _join(a, b)
    assert len(joined.orth) == len(joined.segments)
    assert joined.orth[0] == "a" and joined.orth[1] == "sh"
    plain = _join(w("ə"), b)
    assert plain.orth == ("",) + b.orth


def test_the_channel_is_empty_or_exactly_as_long_as_the_segments():
    assert w("ɡɔɾˠmˠ").orth == () and w("ɡɔɾˠmˠ").tag_at(0) == ""


# ---- the measured coverage (spec §11: a number, not a threshold) -------------------------

CLASSES = {
    "ao": lambda o: "ao" in o,
    "quality-digraph": lambda o: any(d in o for d in ("ea", "io", "ai", "oi", "ui")),
    "lenition-digraph": lambda o: any(d in o for d in ("bh", "dh", "gh", "mh")),
    "ch-th": lambda o: "ch" in o or "th" in o,
    "ua-ia": lambda o: "ua" in o or "ia" in o,
    "final-vowel": lambda o: o.endswith(("a", "e")),
    "an-suffix": lambda o: o.endswith("án"),
    "eclipsis": lambda o: o.startswith(("mb", "gc", "nd", "bp", "dt", "bhf", "ng")),
}
ROWS = [r for r in read_test_words() if r["ipa"]]


def test_every_test_word_aligns():
    """Measured 144/144 with the committed table. A regression here is a table regression."""
    bad = [r["orthography"] for r in ROWS if not any(align(r["orthography"], segs(r["ipa"])))]
    assert bad == [], bad


@pytest.mark.parametrize("name", sorted(CLASSES))
def test_every_reversal_class_aligns_completely(name):
    """spec §11: coverage is a per-class measurement."""
    pred = CLASSES[name]
    members = [r for r in ROWS if pred(r["orthography"].casefold())]
    bad = [r["orthography"] for r in members if not any(align(r["orthography"], segs(r["ipa"])))]
    assert members and bad == [], (name, len(members), bad)
