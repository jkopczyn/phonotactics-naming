"""Longest-match tokenizer, prosodic/boundary marks, and attested-data cleaning.

Plan Task 3; spec §2 (segments are opaque tokens; tokenization is longest-match against
features.tsv; an unknown segment is a hard error naming the word and the substring) and
§12.F (the alias table applies to attested data only); interpretations I-1 (NFC on read),
I-2 (diphthongs are two segments), I-24 (unknown segment raises for user input and rule
files), I-34 (ASCII `g` is a canonical row and survives tokenize()), I-36 (cleaning pass for
attested.tsv fields), I-40 (marks, including secondary stress).
"""
from __future__ import annotations

import unicodedata
from collections.abc import Sequence
from dataclasses import dataclass

from .features import FeatureTable

__all__ = ["MARKS", "Tokenized", "SegmentError", "tokenize", "detokenize", "clean_attested"]

# I-40. Marks are never segments; each is recorded as an annotation and removed.
MARKS: dict[str, str] = {
    "ˈ": "stress",
    "ˌ": "secondary",
    ".": "syllable",
    "$": "morpheme",
    " ": "space",
}


class SegmentError(Exception):
    """A substring of the input matches no segment in the feature table (I-24)."""


@dataclass(frozen=True)
class Tokenized:
    segments: tuple[str, ...]
    stress_index: int | None          # SEGMENT index of the primary-stressed syllable's start
    secondary: tuple[int, ...]        # segment indices carrying ˌ
    syllable_starts: tuple[int, ...]  # from explicit "." marks; empty when the input has none
    morphemes: frozenset[int]         # positions 0..len carrying "$"
    words: tuple[int, ...]            # segment index each space-separated word starts at


def _longest_match(text: str, pos: int, table: FeatureTable, max_len: int) -> str | None:
    """Longest segment in `table` that is a prefix of `text[pos:]`, or None."""
    for n in range(min(max_len, len(text) - pos), 0, -1):
        candidate = text[pos:pos + n]
        if candidate in table:
            return candidate
    return None


def tokenize(text: str, table: FeatureTable) -> Tokenized:
    """Split an IPA string into feature-table segments, recording marks (I-40).

    NFC is applied first (I-1). Segments are matched longest-first against the table (spec
    §2), so `t̪ˠ` beats `t` and a diphthong such as `iə` comes out as two segments (I-2).
    ASCII `g` is a table row and is NOT folded to `ɡ` here (I-34); see `clean_attested`.
    """
    text = unicodedata.normalize("NFC", text)
    max_len = max((len(s) for s in table.segments), default=0)

    segments: list[str] = []
    stress_index: int | None = None
    secondary: list[int] = []
    syllable_starts: list[int] = []
    saw_dot = False
    morphemes: set[int] = set()
    words: list[int] = []
    at_word_start = True   # the next segment begins a word

    pos = 0
    while pos < len(text):
        ch = text[pos]
        mark = MARKS.get(ch)
        if mark is not None:
            n = len(segments)
            if mark == "stress":
                if stress_index is None:
                    stress_index = n
            elif mark == "secondary":
                secondary.append(n)
            elif mark == "syllable":
                saw_dot = True
                if n not in syllable_starts:
                    syllable_starts.append(n)
            elif mark == "morpheme":
                morphemes.add(n)
            elif mark == "space":
                at_word_start = True
            pos += 1
            continue
        seg = _longest_match(text, pos, table, max_len)
        if seg is None:
            # Name the offending substring: from here to the next mark (or end of input).
            end = pos
            while end < len(text) and text[end] not in MARKS:
                end += 1
            raise SegmentError(
                f"unknown segment {text[pos:end]!r} at position {pos} in {text!r}"
            )
        if at_word_start:
            words.append(len(segments))
            at_word_start = False
        segments.append(seg)
        pos += len(seg)

    if saw_dot and segments:
        # The first syllable of a dotted word starts at 0 even though no dot precedes it.
        if 0 not in syllable_starts:
            syllable_starts.insert(0, 0)
        syllable_starts = sorted(syllable_starts)
    else:
        syllable_starts = []

    return Tokenized(
        segments=tuple(segments),
        stress_index=stress_index,
        secondary=tuple(secondary),
        syllable_starts=tuple(syllable_starts),
        morphemes=frozenset(morphemes),
        words=tuple(words),
    )


def detokenize(segments: Sequence[str]) -> str:
    """Concatenate segments; marks are annotations and are not re-emitted."""
    return "".join(segments)


def clean_attested(text: str, target: str) -> str:
    """I-36: strip wrapping [ ] and / /, ':'->'ː', ASCII 'g'->'ɡ'. The ASCII apostrophe
    is mapped to 'ʼ' ONLY for target == 'georgian' (national-2002 ejective mark); for
    every other target it is a stress mark and is dropped. Used ONLY on attested.tsv
    fields, never on user input."""
    s = unicodedata.normalize("NFC", text).strip()
    if len(s) >= 2 and ((s[0] == "[" and s[-1] == "]") or (s[0] == "/" and s[-1] == "/")):
        s = s[1:-1].strip()
    s = s.replace(":", "ː")
    s = s.replace("'", "ʼ" if target == "georgian" else "")
    s = s.replace("g", "ɡ")
    return s
