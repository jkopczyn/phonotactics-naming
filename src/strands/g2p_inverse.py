"""The reverse g2p: which Irish spellings can read as a given segment (reverse spec §3.4).

This module is a **transcription of `strands.g2p`**, not an inversion of two of its tables.
`g2p` does not decide a grapheme's value from `_CONSONANTS` alone: `_grapheme` branches
procedurally (⟨dh gh sh th ch ng nc dt x⟩), `_liquid`/`_rhotic`/`_sibilant` decide ⟨l n r s⟩
positionally, `_word_segments` turns a noninitial /w/ into /vˠ/ for Connacht and reduces an
unstressed short vowel to /ə/, and `_epenthesis` inserts a schwa no letter spells. Every one of
those emission paths has rows here, and each row names the branch it came from in `Reading.source`
(V-27). **A change to any of those branches must be mirrored here**;
`tests/ratchets/g2p_inverse.json` is what notices if it is not.

The registry **over-generates by design**, and only in that direction: `quality` and `position` are
advisory, the `_VOWELS` context overrides are registered without checking their conditions, and no
row is a claim that `g2p` would in fact read the grapheme that way in a given word. `g2p()` itself
is the only judge — `spell()` runs every candidate spelling back through it before offering it
(spec §3.4, last sentence).

Interpretations: V-27 (the registry over every emission path), V-19 (the derived indexes),
V-21 (`describe`).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from . import g2p

__all__ = ["Reading", "READINGS", "CONSONANT_READINGS", "VOWEL_READINGS",
           "QUALITY_LEFT", "QUALITY_RIGHT", "BROAD_ON_THE_RIGHT", "readings_for", "describe"]

Quality = str          # "broad" | "slender" | "either"
Position = str         # "any" | "initial" | "noninitial"

BROAD = "broad"
SLENDER = "slender"
EITHER = "either"


@dataclass(frozen=True)
class Reading:
    """One way a grapheme can be read. `segments` is 0, 1 or 2 segments; `()` is silent."""
    grapheme: str
    segments: tuple[str, ...]
    quality: Quality
    position: Position
    source: str                        # the g2p branch, e.g. "_liquid fortis", "connacht-w"


# ---- the consonant registry --------------------------------------------------------------------

def _build_readings() -> tuple[Reading, ...]:
    out: list[Reading] = []

    def add(grapheme: str, segments: Sequence[str] | None, quality: Quality,
            position: Position, source: str) -> None:
        out.append(Reading(grapheme, tuple(segments or ()), quality, position, source))

    # `_CONSONANTS`: each grapheme × (broad, slender); `None` is a silent reading.
    for grapheme, (broad, slender) in g2p.CONSONANTS.items():
        add(grapheme, None if broad is None else [broad], BROAD, "any", "_CONSONANTS")
        add(grapheme, None if slender is None else [slender], SLENDER, "any", "_CONSONANTS")

    # `_ECLIPSIS_INITIAL`: word-initial only.
    for grapheme, (broad, slender) in g2p.ECLIPSIS_INITIAL.items():
        add(grapheme, [broad], BROAD, "initial", "_ECLIPSIS_INITIAL")
        add(grapheme, [slender], SLENDER, "initial", "_ECLIPSIS_INITIAL")

    # `_grapheme` ⟨dh gh⟩: slender /j/; broad /ɣ/ initially, silent elsewhere.
    for grapheme in ("dh", "gh"):
        add(grapheme, ["j"], SLENDER, "any", "_grapheme dh/gh")
        add(grapheme, ["ɣ"], BROAD, "initial", "_grapheme dh/gh")
        add(grapheme, (), BROAD, "noninitial", "_grapheme dh/gh silent")

    # `_grapheme` ⟨sh⟩: /h/, or [ç] as the lenition of a slender /ʃ/ before a back vowel.
    add("sh", ["h"], EITHER, "any", "_grapheme sh")
    add("sh", ["ç"], SLENDER, "any", "_grapheme sh")

    # `_grapheme` ⟨th⟩: /h/, silent word-finally after a long vowel or diphthong.
    add("th", ["h"], EITHER, "any", "_grapheme th")
    add("th", (), EITHER, "any", "_grapheme th silent")

    # `_grapheme` ⟨ch⟩: slender ⟨ch⟩ before ⟨t⟩ is /x/, not /ç/ (the table gives the rest).
    add("ch", ["x"], SLENDER, "any", "_grapheme ch before t")

    # `_grapheme` ⟨ng nc dt x⟩: the two-segment and positional branches.
    add("ng", ["ŋ", "ɡ"], BROAD, "noninitial", "_grapheme ng")
    add("ng", ["ɲ", "ɟ"], SLENDER, "noninitial", "_grapheme ng")
    add("nc", ["ŋ", "k"], BROAD, "any", "_grapheme nc")
    add("nc", ["ɲ", "c"], SLENDER, "any", "_grapheme nc")
    add("dt", ["t̪ˠ"], BROAD, "noninitial", "_grapheme dt")
    add("dt", ["tʲ"], SLENDER, "noninitial", "_grapheme dt")
    add("x", ["k", "s"], EITHER, "any", "_grapheme x")

    # `_liquid`: ⟨l n⟩ are fortis or lenis by position, and the doubled ⟨ll nn⟩ are always
    # fortis. Which one `g2p` picks is a positional judgement this registry does not repeat.
    for grapheme, fortis, lenis in (("l", ("l̪ˠ", "l̠ʲ"), ("lˠ", "lʲ")),
                                    ("n", ("n̪ˠ", "n̠ʲ"), ("nˠ", "nʲ"))):
        add(grapheme, [fortis[0]], BROAD, "any", "_liquid fortis")
        add(grapheme, [fortis[1]], SLENDER, "any", "_liquid fortis")
        add(grapheme, [lenis[0]], BROAD, "any", "_liquid lenis")
        add(grapheme, [lenis[1]], SLENDER, "any", "_liquid lenis")
        add(grapheme * 2, [fortis[0]], BROAD, "any", "_liquid fortis")
        add(grapheme * 2, [fortis[1]], SLENDER, "any", "_liquid fortis")
    # The cn/gn/mn branch: ⟨n⟩ after a non-⟨s⟩ word-initial consonant is /ɾˠ ɾʲ/ (mná, cnaipe).
    add("n", ["ɾˠ"], BROAD, "noninitial", "_liquid cn-gn-mn")
    add("n", ["ɾʲ"], SLENDER, "noninitial", "_liquid cn-gn-mn")

    # `_rhotic`: broad ⟨r⟩ and ⟨rr⟩ are /ɾˠ/; slender ⟨r⟩ is /ɾˠ/ initially, after ⟨s⟩ and
    # before a coronal, /ɾʲ/ otherwise — so ⟨r⟩ reads as /ɾˠ/ in *either* quality.
    add("r", ["ɾˠ"], EITHER, "any", "_rhotic")
    add("r", ["ɾʲ"], SLENDER, "any", "_rhotic")
    add("rr", ["ɾˠ"], EITHER, "any", "_rhotic")

    # `_sibilant`: slender ⟨s⟩ is /sˠ/ initially before ⟨f m p r⟩, /ʃ/ otherwise.
    add("s", ["sˠ"], EITHER, "any", "_sibilant")
    add("s", ["ʃ"], SLENDER, "any", "_sibilant")

    # `_word_segments` Connacht post-pass: a NONINITIAL /w/ surfaces as /vˠ/ (dialect "C").
    # This is the row that makes *ardmhaor* /ˈaːɾˠd̪ˠvˠiːɾˠ/ spellable at all.
    for reading in list(out):
        if reading.segments == ("w",):
            add(reading.grapheme, ["vˠ"], reading.quality, "noninitial", "connacht-w")

    # Dedupe on identity, first source winning, so the registry stays a set of distinct rows.
    seen: set[tuple[str, tuple[str, ...], str, str]] = set()
    kept: list[Reading] = []
    for reading in out:
        key = (reading.grapheme, reading.segments, reading.quality, reading.position)
        if key in seen:
            continue
        seen.add(key)
        kept.append(reading)
    return tuple(kept)


READINGS: tuple[Reading, ...] = _build_readings()


def _consonant_index() -> dict[tuple[str, ...], tuple[Reading, ...]]:
    index: dict[tuple[str, ...], list[Reading]] = {}
    for reading in READINGS:
        index.setdefault(reading.segments, []).append(reading)
    return {segments: tuple(rows) for segments, rows in index.items()}


CONSONANT_READINGS: dict[tuple[str, ...], tuple[Reading, ...]] = _consonant_index()


# ---- the vowel registry --------------------------------------------------------------------

def _vowel_index() -> dict[tuple[str, ...], tuple[str, ...]]:
    """Segment sequence → the vowel runs that read as it (V-19).

    Built in `g2p`'s own emission order — defaults, then the context overrides (registered
    without checking their conditions), then `_VOWEL_PLUS_H`, then the unstressed reduction —
    so the *canonical* run for a nucleus comes first and `describe` leads with it.
    """
    index: dict[tuple[str, ...], list[str]] = {}

    def add(nucleus: str, run: str) -> None:
        key = tuple(g2p.split_nucleus(nucleus))
        rows = index.setdefault(key, [])
        if run not in rows:
            rows.append(run)

    for run, (default, _overrides) in g2p.VOWELS.items():
        add(default, run)
    for run, (_default, overrides) in g2p.VOWELS.items():
        for _condition, value in overrides:
            add(value, run)
    for (run, digraph), (stressed, unstressed) in g2p.VOWEL_PLUS_H.items():
        add(stressed, run + digraph)
        add(unstressed, run + digraph)
    # `_word_segments` pass 2: an unstressed short monophthong reduces to /ə/.
    for run, (default, _overrides) in g2p.VOWELS.items():
        if len(default) == 1 and default != "ə":
            add("ə", run)
    return {key: tuple(rows) for key, rows in index.items()}


VOWEL_READINGS: dict[tuple[str, ...], tuple[str, ...]] = _vowel_index()

# `_slender` reads quality off the flanking vowel LETTERS. ⟨ae⟩ is the exception `g2p` states;
# V-19 extends it to the ⟨ae ao⟩ family, which is stricter than `_slender` for ⟨aei aoi⟩ (there
# `g2p` follows the final ⟨i⟩). Advisory either way: `g2p()` is the judge.
BROAD_ON_THE_RIGHT: frozenset[str] = frozenset({"ae", "aei", "ao", "aoi"})


def _letter_quality(letter: str) -> Quality:
    if letter in g2p.SLENDER_LETTERS:
        return SLENDER
    if letter in g2p.BROAD_LETTERS:
        return BROAD
    return EITHER


def _vowel_part(run: str) -> str:
    """The vowel-letter prefix of a run: a `_VOWEL_PLUS_H` key carries its ⟨bh dh gh mh⟩."""
    end = len(run)
    while end and _letter_quality(run[end - 1]) == EITHER:
        end -= 1
    return run[:end] or run


def _quality_maps() -> tuple[dict[str, Quality], dict[str, Quality]]:
    left: dict[str, Quality] = {}
    right: dict[str, Quality] = {}
    runs: list[str] = list(g2p.VOWELS)
    runs += [run + digraph for run, digraph in g2p.VOWEL_PLUS_H]
    for run in runs:
        letters = _vowel_part(run)
        left.setdefault(run, _letter_quality(letters[0]))
        right[run] = BROAD if letters in BROAD_ON_THE_RIGHT else _letter_quality(letters[-1])
    return left, right


QUALITY_LEFT, QUALITY_RIGHT = _quality_maps()


# ---- lookups ---------------------------------------------------------------------------------

def readings_for(segments: Sequence[str]) -> tuple[Reading, ...]:
    """Every registered reading of exactly this segment sequence, in registry order."""
    return CONSONANT_READINGS.get(tuple(segments), ())


def _describe_consonant(segments: tuple[str, ...]) -> str | None:
    rows = readings_for(segments)
    if not rows:
        return None
    graphemes: list[str] = []
    for reading in rows:
        if reading.grapheme not in graphemes:
            graphemes.append(reading.grapheme)
    qualities = {reading.quality for reading in rows}
    prefix = f"{qualities.pop()} " if len(qualities) == 1 and EITHER not in qualities else ""
    return prefix + "/".join(graphemes)


def _describe_nucleus(segments: tuple[str, ...]) -> str | None:
    runs = VOWEL_READINGS.get(segments)
    return ", ".join(runs) if runs else None


def describe(segments: Sequence[str]) -> str:
    """The report's description column for a segment sequence (V-21).

    Never a pick: every reading is listed (R7). Not g2p-checked — it is a description of what
    the tables say, not a claim about a concrete word.
    """
    segments = tuple(segments)
    if not segments:
        return "inserted, no Irish letter"
    whole = _describe_consonant(segments) or _describe_nucleus(segments)
    if whole is not None:
        return whole
    if len(segments) == 1:
        return f"/{segments[0]}/"
    # A mixed sequence: consonants one at a time, a maximal vowel run as one nucleus.
    parts: list[str] = []
    i = 0
    while i < len(segments):
        if segments[i] in g2p.VOWEL_SEGMENTS:
            j = i
            while j < len(segments) and segments[j] in g2p.VOWEL_SEGMENTS:
                j += 1
            parts.append(describe(segments[i:j]))
            i = j
            continue
        parts.append(describe(segments[i:i + 1]))
        i += 1
    return " + ".join(parts)
