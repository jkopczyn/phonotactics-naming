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
V-20 (`spell`, the run matcher and caol le caol),
V-21 (`describe`).
"""
from __future__ import annotations

import heapq
import itertools
from dataclasses import dataclass
from typing import Sequence

from . import g2p

__all__ = ["Reading", "READINGS", "CONSONANT_READINGS", "VOWEL_READINGS",
           "QUALITY_LEFT", "QUALITY_RIGHT", "BROAD_ON_THE_RIGHT", "readings_for", "describe",
           "spell", "SPELL_LIMIT"]

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


def _split_vowel_run(run: tuple[str, ...]) -> list[str]:
    """An all-vowel run with no `VOWEL_READINGS` row of its own, as its longest registered
    sub-runs, greedily left to right; a segment with no run of its own renders `/x/`.

    `describe`'s mixed-sequence loop treats a maximal vowel run as one nucleus, so without this
    an unregistered run (Welsh `i` reaches ('ɪ', 'ə')) recursed on itself forever. Splitting
    over-generates rather than under-generates (spec §3), as V-21's ` + ` join already does.
    """
    parts: list[str] = []
    i = 0
    while i < len(run):
        for j in range(len(run), i, -1):
            sub = run[i:j]
            if sub == run:
                continue                   # the whole run is exactly what has no reading
            described = _describe_nucleus(sub)
            if described is not None:
                parts.append(described)
                i = j
                break
        else:
            parts.append(f"/{run[i]}/")
            i += 1
    return parts


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
            run = segments[i:j]
            if run == segments:
                parts.extend(_split_vowel_run(run))   # the progress guard, see above
            else:
                parts.append(describe(run))
            i = j
            continue
        parts.append(describe(segments[i:i + 1]))
        i += 1
    return " + ".join(parts)


# ---- spell(): the run matcher (V-20) ---------------------------------------------------------

SPELL_LIMIT = 64
_PROPOSAL_BUDGET = 1024  # spellings tried through `g2p` before a word is given up on

_TABLE = None


def _table():
    """The feature table `g2p`'s output is tokenized with, loaded once.

    `cli.DEFAULT_FEATURES` is imported lazily: `cli` imports `reverse`, which imports this
    module, so a module-level import would close a cycle. The path constant is still the one
    place it is written down.
    """
    global _TABLE
    if _TABLE is None:
        from .cli import DEFAULT_FEATURES
        from .features import load_features
        _TABLE = load_features(DEFAULT_FEATURES)
    return _TABLE


def _unmark(ipa: str) -> str:
    for mark in ("ˈ", "ˌ", "."):
        ipa = ipa.replace(mark, "")
    return ipa


def _runs(segments: Sequence[str]) -> list[tuple[str, tuple[str, ...]]]:
    """The segments as alternating ("C", run) / ("V", nucleus) units (V-20 step 1).

    A segment is a nucleus member iff it is in `g2p._VOWEL_SEGMENTS`; a maximal run of them is
    one nucleus.
    """
    out: list[tuple[str, list[str]]] = []
    for seg in segments:
        kind = "V" if seg in g2p.VOWEL_SEGMENTS else "C"
        if out and out[-1][0] == kind:
            out[-1][1].append(seg)
        else:
            out.append((kind, [seg]))
    return [(kind, tuple(run)) for kind, run in out]


def _run_spellings(run: tuple[str, ...], quality: Quality, at_word_start: bool):
    """Every spelling of one consonant run at one quality, lazily (V-20 step 2).

    A recursive matcher: at each position, every `Reading` whose segments are a prefix of what
    is left, whose quality admits `quality` and whose position admits the position. Silent
    readings consume nothing and may be used at most **once** per run; with a finite run, a
    finite `READINGS` and that once-per-run bound the recursion terminates on its own — no cap
    on the results is needed to make it stop.

    Two passes, silent-free spellings first, `READINGS` order within each: a silent reading is
    admissible everywhere, so in one pass the *dorn* spelling of /ɾˠn̪ˠ/ would sit behind five
    ⟨rrnn+silent⟩ ones and the caller's cap would cut it off.
    """
    def walk(i: int, at_start: bool, silent_used: bool, acc: list[str], want_silent: bool):
        if i == len(run) and silent_used == want_silent:
            yield "".join(acc)
        # Segment-consuming readings first, silent ones after.
        for silent in (False, True):
            if silent and (silent_used or not want_silent):
                continue
            for reading in READINGS:
                if (len(reading.segments) == 0) != silent:
                    continue
                if reading.quality != EITHER and reading.quality != quality:
                    continue
                if reading.position == "initial" and not at_start:
                    continue
                if reading.position == "noninitial" and at_start:
                    continue
                if silent:
                    yield from walk(i, False, True, acc + [reading.grapheme], want_silent)
                    continue
                width = len(reading.segments)
                if run[i:i + width] != reading.segments:
                    continue
                yield from walk(i + width, False, silent_used, acc + [reading.grapheme],
                                want_silent)

    for want_silent in (False, True):
        yield from walk(0, at_word_start, False, [], want_silent)


def _spell_run(run: Sequence[str], quality: Quality, at_word_start: bool, *,
               cap: int = _PROPOSAL_BUDGET) -> list[str]:
    """The spellings of one consonant run, in registry order, bounded by `cap`.

    The bound belongs to the top-level enumeration, not to the matcher: `cap` is the caller's
    proposal budget (`spell` never runs more than that many candidates through `g2p`), so a run
    spelling past it is one no caller could reach anyway, and everything up to it is in the
    order V-20 asks for. An internal cap smaller than the budget would instead drop ordinary
    spellings the caller did ask for — the IPA of *akkkkkkka* stopped recovering that spelling.
    """
    return list(itertools.islice(_run_spellings(tuple(run), quality, at_word_start), cap))


def _epenthetic(units: Sequence[tuple[str, tuple[str, ...]]], i: int) -> bool:
    """Is unit `i` a schwa `g2p._epenthesis` could have inserted (V-20 step 3)?

    Over-generating on purpose: the union of `_EPEN_C2_LIQUID` and `_EPEN_C2_NASAL` is used,
    and none of `_epenthesis`'s blocking conditions is re-checked — `g2p()` is the judge.
    """
    kind, run = units[i]
    if kind != "V" or run != ("ə",):
        return False
    if i == 0 or i + 1 >= len(units):
        return False
    left, right = units[i - 1], units[i + 1]
    if left[0] != "C" or right[0] != "C":
        return False
    return left[1][-1] in g2p.EPEN_C1 and right[1][0] in (g2p.EPEN_C2_LIQUID | g2p.EPEN_C2_NASAL)


def _layouts(units: list[tuple[str, tuple[str, ...]]]) -> list[list[tuple[str, tuple[str, ...]]]]:
    """The unit lists to try: an epenthetic schwa may be spelled with **no letter**, and then
    its two neighbouring consonant runs are spelled as one run (V-20 steps 3 and 4).

    The dropped reading comes first: an epenthetic schwa is the one `g2p` actually inserts, so
    *gorm* must be reachable well inside `limit`.
    """
    epen = [i for i in range(len(units)) if _epenthetic(units, i)]
    if not epen:
        return [units]
    out: list[list[tuple[str, tuple[str, ...]]]] = []
    for drops in itertools.product((True, False), repeat=len(epen)):
        dropped = {i for i, drop in zip(epen, drops) if drop}
        layout: list[tuple[str, tuple[str, ...]]] = []
        for i, (kind, run) in enumerate(units):
            if i in dropped:
                continue
            if layout and layout[-1][0] == kind == "C":
                layout[-1] = ("C", layout[-1][1] + run)
            else:
                layout.append((kind, run))
        if layout not in out:
            out.append(layout)
    return out


def _options(units: Sequence[tuple[str, tuple[str, ...]]], i: int,
             pending: Quality, cap: int) -> list[tuple[str, Quality]]:
    """The spellings unit `i` admits, given the quality imposed from its left, each paired with
    the quality it imposes on its right (V-20 step 4).

    A consonant run takes **one** quality, enumerated once per quality that admits a complete
    match; a nucleus admits only the runs whose `QUALITY_LEFT` is the quality already chosen for
    the run on its left. A word-edge run is unconstrained on the missing side.
    """
    kind, run = units[i]
    out: list[tuple[str, Quality]] = []
    if kind == "C":
        qualities = [pending] if pending in (BROAD, SLENDER) else [BROAD, SLENDER]
        for quality in qualities:
            for text in _spell_run(run, quality, at_word_start=(i == 0), cap=cap):
                out.append((text, quality))
        return out
    for spelling in VOWEL_READINGS.get(run, ()):
        if pending in (BROAD, SLENDER) and QUALITY_LEFT.get(spelling, EITHER) not in (
                pending, EITHER):
            continue
        out.append((spelling, QUALITY_RIGHT.get(spelling, EITHER)))
    return out


def _candidates(units: Sequence[tuple[str, tuple[str, ...]]], cap: int):
    """Every spelling of one layout, shortest first (V-20 step 5).

    "Registry order" over more than one unit has to be made a *total* order, and the nested
    product (leftmost unit slowest) is the wrong one: the ⟨o⟩ of *dorn* and the ⟨a⟩ of
    *ardmhaor* are `_VOWELS` context overrides, which sit at the end of their run lists, so a
    nested product does not reach either one within any usable `limit`. The order used instead
    is **by letter count ascending, ties broken lexicographically by the per-unit option index
    tuple** — so each unit's own options stay in registry order, and a spelling that reads a
    segment with one letter is offered before one that spends three on it. It is a best-first
    walk over partial spellings (`heapq`, the shape V-24 uses), so `spell` can stop early
    without materialising the product.
    """
    heap: list[tuple[int, tuple[int, ...], int, Quality, tuple[str, ...]]] = [
        (0, (), 0, EITHER, ())]
    while heap:
        cost, indices, i, pending, acc = heapq.heappop(heap)
        if i == len(units):
            yield "".join(acc)
            continue
        for j, (text, imposed) in enumerate(_options(units, i, pending, cap)):
            heapq.heappush(heap,
                           (cost + len(text), indices + (j,), i + 1, imposed, acc + (text,)))


def spell(segments: Sequence[str], *, limit: int = SPELL_LIMIT) -> list[str]:
    """Irish IPA segments → the Irish spellings that read back as them (V-20).

    Candidates are enumerated shortest-first (`_candidates`) and every one is run through
    `g2p()`, kept only if it reads back to exactly `segments`: nothing leaves here unverified
    (spec §3.4, last sentence). `limit` caps the **kept** spellings, and `_PROPOSAL_BUDGET`
    bounds the search behind it — V-20 step 5 caps the enumeration instead, but the registry
    over-generates hard enough that a cap of 64 *proposals* returns only junk for a word like
    *ardmhaor* (247 shorter spellings precede it, almost none of which `g2p` accepts), and
    every caller wants `limit` real spellings. A word `g2p` refuses (no vowel letter) or one
    whose nucleus has no registered run simply yields nothing.
    """
    from .tokenize import SegmentError, tokenize

    if limit <= 0:                     # V-20 step 5 caps the enumeration: nothing is asked for.
        return []
    want = tuple(segments)
    budget = max(_PROPOSAL_BUDGET, 16 * limit)
    kept: list[str] = []
    seen: set[str] = set()
    tried = 0
    for layout in _layouts(_runs(want)):
        for text in _candidates(layout, budget):
            if text in seen:
                continue
            seen.add(text)
            tried += 1
            if tried > budget:
                break
            try:
                ipa, _notes = g2p.g2p(text)
                got = tuple(tokenize(_unmark(ipa), _table()).segments)
            except (g2p.G2PError, SegmentError):
                continue
            if got == want:
                kept.append(text)
                if len(kept) >= limit:
                    break
        if len(kept) >= limit or tried > budget:
            break
    return kept
