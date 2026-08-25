"""Task 4: immutable Word model and derivation trace."""
import dataclasses

import pytest

from strands.tokenize import Tokenized
from strands.word import TraceEntry, Word


def w(*segs, **kw):
    return Word(segments=tuple(segs), **kw)


def test_ipa_with_marks():
    x = w("k", "ɪ", "ə", "ɾˠ", "ə", syllables=(0, 3), stress=0)
    assert x.ipa() == "ˈkɪə.ɾˠə" and x.ipa(marks=False) == "kɪəɾˠə"


def test_ipa_stress_on_a_later_syllable():
    x = w("p", "a", "t", "a", syllables=(0, 2), stress=1)
    assert x.ipa() == "pa.ˈta"


def test_ipa_without_syllables_prints_no_marks():
    assert w("p", "a").ipa() == "pa"


def test_replaced_shifts_later_annotations():
    x = w("s", "k", "a", "l", syllables=(0,), morphemes=frozenset({4}), illegal=frozenset({0, 1}))
    y = x.replaced(0, 1, ("i", "s"))
    assert y.segments == ("i", "s", "k", "a", "l") and y.morphemes == frozenset({5})


def test_replaced_drops_marks_inside_the_span():
    assert w("a", "b", "c", illegal=frozenset({1})).replaced(1, 2, ("d",)).illegal == frozenset()


def test_replaced_shifts_syllables_nuclei_and_illegal_after_the_span():
    x = w("p", "a", "t", "a", syllables=(0, 2), nuclei=((1, 2), (3, 4)), stress=1,
          illegal=frozenset({3}))
    y = x.replaced(0, 1, ("s", "p"))
    assert y.segments == ("s", "p", "a", "t", "a")
    assert y.syllables == (0, 3) and y.nuclei == ((2, 3), (4, 5))
    assert y.stress == 1 and y.illegal == frozenset({4})


def test_replaced_deletion_shrinks_indices():
    x = w("a", "p", "t", "a", syllables=(0, 2), morphemes=frozenset({4}))
    y = x.replaced(1, 2, ())
    assert y.segments == ("a", "t", "a") and y.syllables == (0, 1) and y.morphemes == frozenset({3})


def test_replaced_remaps_stress_when_a_syllable_is_dropped():
    # syllables 0 and 1 are inside the replaced span and vanish; stress on syllable 2 moves to 0
    x = w("a", "b", "a", "t", "a", syllables=(0, 1, 3), stress=2)
    y = x.replaced(0, 3, ("k",))
    assert y.syllables == (0, 1) and y.stress == 1


def test_replaced_keeps_pending_stress_in_segment_terms():
    x = Word.from_tokenized(Tokenized(("p", "a", "t", "a"), 2, (), (), frozenset(), (0,)))
    assert x._pending_stress == 2 and x.stress is None
    assert x.replaced(0, 1, ("s", "p"))._pending_stress == 3


def test_from_tokenized_copies_annotations():
    tok = Tokenized(("p", "a", "t", "a"), 0, (2,), (0, 2), frozenset({2}), (0,))
    x = Word.from_tokenized(tok)
    assert x.segments == ("p", "a", "t", "a") and x.syllables == (0, 2)
    assert x.morphemes == frozenset({2}) and x._pending_stress == 0 and x.stress is None
    assert x.secondary == (2,) and x.trace == ()


def test_traced_appends_and_is_immutable():
    x = w("a")
    y = x.traced(TraceEntry("substitute", "substitute:3", "attested", "a", "b"))
    assert x.trace == () and len(y.trace) == 1


def test_fallback_count():
    x = (w("a").traced(TraceEntry("substitute", "fallback", "fallback", "q", "k"))
              .traced(TraceEntry("substitute", "substitute:1", "attested", "p", "b")))
    assert x.fallback_count() == 1


def test_with_flag_is_idempotent():
    assert w("a").with_flag("UNREPAIRED").with_flag("UNREPAIRED").flags == ("UNREPAIRED",)


def test_word_is_hashable_and_frozen():
    hash(w("a"))
    with pytest.raises(dataclasses.FrozenInstanceError):
        w("a").segments = ("b",)


def test_replaced_insertion_can_sit_before_a_morpheme_boundary():
    x = w("p", morphemes=frozenset({1}))
    assert x.replaced(1, 1, ("i",)).morphemes == frozenset({1})                          # $ i
    assert x.replaced(1, 1, ("i",), before_boundary=True).morphemes == frozenset({2})    # i $
    # a non-empty span: a boundary at `start` stays put either way
    y = w("p", "a", morphemes=frozenset({1}))
    assert y.replaced(1, 2, ("i", "u"), before_boundary=True).morphemes == frozenset({1})
