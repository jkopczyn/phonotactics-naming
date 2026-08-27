"""The modern-orthography <-> IPA aligner and the `Word.orth` tag channel.

Old Irish spec §4 and §11; plan Task 5; interpretations O-6, O-7.

Why spelling is needed (spec §4). The Old Irish retro-filter reverses changes that modern
Irish *spelling* still records but modern *pronunciation* has merged: ⟨bh⟩ and ⟨mh⟩ are both
/w/ or /v/ today but were distinct lenited /β/ and /μ/; ⟨ao⟩, ⟨ae⟩ and ⟨aoi⟩ are all /iː/ or
/eː/ but were distinct ⟨áe óe aí⟩. A rule that can see only sound cannot choose. So the Irish
pre-pass tags every segment with the modern spelling unit it came from (`Word.orth`), and the
`@orth("…")` rule item (Task 6) reads the tag. "The modern spelling of this segment's source
is …" — that is the whole contract.

The algorithm (O-7). `align()` cleans the orthography (NFC, casefold, delete `-`, `'`, `’` and
spaces) and runs a depth-first search over nodes `(i, j)` = (characters consumed, segments
consumed) from `(0, 0)` to `(len(orthography), len(segments))`. From a node it tries every
table row whose unit matches at `i`, in table order — longest unit first, then file order —
and every alternative of that row in file order; an alternative applies when the next
segments equal it. Dead nodes are memoized so that the search is linear in practice, but the
memo only PRUNES, it never decides: the first complete path in that traversal order wins,
which makes the result a deterministic function of the table's order and nothing else (the
Python `set` used for the memo cannot change which path is found first). Fourteen of the 144
corpus words need backtracking (*long*: `ng -> (ŋ,)` is tried first and dead-ends, then
`ng -> (ŋ, ɡ)` completes).

Failure is total (O-7). When no path exists, every tag is `""` — never a partial alignment,
never an exception — and `tag_word` records `orth:unaligned` in the trace. An untagged segment
matches no `@orth` item, so only sound-based rules apply to it; that is the designed failure
mode, and the plan's measured coverage (144/144 test words, 100% in every reversal class) is a
number, not a threshold.

Positional tags (O-6, spec §11). A unit that consumes one segment tags it `unit`; a unit that
consumes n > 1 segments tags them `unit:1` … `unit:n`, so *Niamh* /nʲiəw/ is
`("n", "ia:1", "ia:2", "mh")` and the epenthetic schwa of *gorm* is `r:2`. A rule may target
either element (`@orth("ia:1") -> i`) or claim the whole unit with a two-item target. A
silent unit (`-`) consumes no segment and leaves no tag.
"""
from __future__ import annotations

import unicodedata
from pathlib import Path
from typing import Sequence

from .word import TraceEntry, Word

__all__ = ["ORTH_TABLE_PATH", "OrthError", "Table", "align", "load_orth_table", "tag_word"]

ORTH_TABLE_PATH: Path = Path(__file__).resolve().parents[2] / "rules" / "irish-orthography.tsv"

STAGE = "irish"
_DROP = str.maketrans("", "", "-'’ ")


class OrthError(Exception):
    """A malformed alignment table."""


# (unit, alternatives), longest unit first; each alternative is a segment tuple (() = silent).
Table = tuple[tuple[str, tuple[tuple[str, ...], ...]], ...]

_cache: dict[Path, Table] = {}


def load_orth_table(path: Path | None = None) -> Table:
    """Read `rules/irish-orthography.tsv` (UTF-8, NFC per I-1). `#` lines are comments; the
    first non-comment line is the header `unit  segments  note`. Rows are sorted by unit
    length, longest first; the sort is stable, so file order breaks ties (O-7)."""
    path = ORTH_TABLE_PATH if path is None else Path(path)
    if path in _cache:
        return _cache[path]
    rows: list[tuple[str, tuple[tuple[str, ...], ...]]] = []
    header_seen = False
    seen: set[str] = set()
    for n, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = unicodedata.normalize("NFC", raw)
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        cells = line.split("\t")
        if not header_seen:
            if cells[:2] != ["unit", "segments"]:
                raise OrthError(f"{path}:{n}: expected header 'unit\\tsegments\\tnote'")
            header_seen = True
            continue
        if len(cells) < 2:
            raise OrthError(f"{path}:{n}: expected at least 2 tab-separated cells")
        unit = cells[0].strip().casefold()
        if not unit:
            raise OrthError(f"{path}:{n}: empty unit")
        if unit in seen:
            raise OrthError(f"{path}:{n}: duplicate unit {unit!r}")
        seen.add(unit)
        alts: list[tuple[str, ...]] = []
        for alt in cells[1].split():
            alts.append(() if alt == "-" else tuple(alt.split("+")))
        if not alts:
            raise OrthError(f"{path}:{n}: unit {unit!r} has no alternatives")
        rows.append((unit, tuple(alts)))
    if not header_seen:
        raise OrthError(f"{path}: no header line")
    rows.sort(key=lambda r: -len(r[0]))          # stable: file order within a length
    table: Table = tuple(rows)
    _cache[path] = table
    return table


def _clean(orthography: str) -> str:
    return unicodedata.normalize("NFC", orthography).casefold().translate(_DROP)


def align(orthography: str, segments: Sequence[str],
          table: Table | None = None) -> tuple[str, ...]:
    """Positional orth tags for `segments`, one per segment, or all-`""` on failure (O-7).
    `segments` should be as they stand after `irish.normalize` (aliases folded, quality
    marked), which is what the table's values are written against."""
    segs = tuple(segments)
    table = load_orth_table() if table is None else table
    text = _clean(orthography)
    n_chars, n_segs = len(text), len(segs)
    empty = ("",) * n_segs
    if not text:
        return empty
    dead: set[tuple[int, int]] = set()

    def search(i: int, j: int) -> list[str] | None:
        if i == n_chars:
            return [] if j == n_segs else None
        if (i, j) in dead:
            return None
        for unit, alts in table:
            if not text.startswith(unit, i):
                continue
            for alt in alts:
                k = len(alt)
                if segs[j:j + k] != alt:
                    continue
                rest = search(i + len(unit), j + k)
                if rest is not None:
                    if k == 1:
                        tags = [unit]
                    else:
                        tags = [f"{unit}:{p}" for p in range(1, k + 1)]
                    return tags + rest
        dead.add((i, j))
        return None

    found = search(0, 0)
    if found is None:
        return empty
    return tuple(found)


def tag_word(word: Word, orthography: str, table: Table | None = None) -> Word:
    """Set `word.orth` from `align(orthography, word.segments)`. On failure the channel is
    all-empty (O-7) and the trace gains `orth:unaligned`."""
    tags = align(orthography, word.segments, table)
    from dataclasses import replace
    out = replace(word, orth=tags)
    if word.segments and not any(tags):
        out = out.traced(TraceEntry(stage=STAGE, rule_id="orth:unaligned", tag="",
                                    before=word.ipa(), after=out.ipa(),
                                    note=f"no alignment of {orthography!r} to the segments; "
                                         f"tags absent, only sound-based rules apply (O-7)"))
    return out
