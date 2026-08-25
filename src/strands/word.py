"""Immutable `Word` model and derivation trace.

Plan Task 4; spec §2 (a Word is a list of segments plus parallel annotations: syllable
boundaries, primary stress, morpheme boundaries `$`, a per-segment "illegal" mark, and an
ordered trace of `(stage, rule_id, rule_tag, before, after)`), §4 (output IPA carries stress
and syllable marks; flags carry `UNREPAIRED` and the fallback count); interpretations I-21
(`rule_id` = "<section>:<line>"), I-40 (secondary stress is recorded and never carried into a
target), S1 (`Tokenized.stress_index` is a SEGMENT index, `Word.stress` is an index into
`syllables`; the segment index waits in `_pending_stress` until `syllabify()` converts it).

Index conventions:
- `syllables`, `illegal`, `secondary`, `_pending_stress`: segment indices.
- `nuclei`: half-open `(start, stop)` segment spans.
- `morphemes`: boundary positions `0..len(segments)` (a `$` sits BEFORE segment i).
- `stress`: index into `syllables`.
"""
from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Sequence

from .tokenize import Tokenized

__all__ = ["TraceEntry", "Word"]


@dataclass(frozen=True)
class TraceEntry:
    stage: str          # "irish" | "substitute" | "syllabify" | "repair" | "stress" | ...
    rule_id: str        # "<section>:<line>" (I-21) or a stage id like "fallback"
    tag: str            # "attested" | "design" | "fallback" | ""
    before: str
    after: str
    note: str = ""


@dataclass(frozen=True)
class Word:
    segments: tuple[str, ...]
    syllables: tuple[int, ...] = ()                 # segment index each syllable starts at
    nuclei: tuple[tuple[int, int], ...] = ()        # (start, stop) segment spans, one per nucleus
    stress: int | None = None                       # index into `syllables`
    morphemes: frozenset[int] = frozenset()
    illegal: frozenset[int] = frozenset()
    flags: tuple[str, ...] = ()
    trace: tuple[TraceEntry, ...] = ()
    secondary: tuple[int, ...] = ()                 # I-40: segment indices carrying ˌ; never output
    _pending_stress: int | None = field(default=None)   # S1: segment index awaiting syllabify()

    @classmethod
    def from_tokenized(cls, tok: Tokenized) -> "Word":
        """Build a Word from tokenizer output. `tok.stress_index` is a SEGMENT index; it is
        parked in `_pending_stress` and converted to a syllable index by `syllabify()`
        (Task 10), so `stress` is always None here (S1). Explicit "." boundaries are kept
        as `syllables`. `tok.words` is ignored: a Word is one word."""
        return cls(
            segments=tuple(tok.segments),
            syllables=tuple(tok.syllable_starts),
            morphemes=frozenset(tok.morphemes),
            secondary=tuple(tok.secondary),
            _pending_stress=tok.stress_index,
        )

    def ipa(self, *, marks: bool = True) -> str:
        """Segments joined, with "." before every non-initial syllable start and "ˈ" before
        the stressed syllable when `marks` is true. Morpheme and secondary-stress marks are
        never printed."""
        if not marks or not self.syllables:
            return "".join(self.segments)
        stressed = self.syllables[self.stress] if self.stress is not None else None
        starts = set(self.syllables)
        out: list[str] = []
        for i, seg in enumerate(self.segments):
            if i in starts and i != 0:
                out.append(".")
            if i == stressed:
                out.append("ˈ")
            out.append(seg)
        return "".join(out)

    def replaced(self, start: int, stop: int, new: Sequence[str], *,
                 before_boundary: bool = False) -> "Word":
        """Return a copy with `segments[start:stop]` replaced by `new`. Annotations before the
        span are kept, those after it are shifted by the length change, and those inside it
        are dropped — except a syllable start at exactly `start`, which survives when `new`
        is non-empty. `stress` follows its syllable (None if that syllable vanished).

        A morpheme boundary at exactly `start` normally stays BEFORE the new material
        (`$ new`); with `before_boundary=True` an insertion (`start == stop`) is placed on
        the left side instead (`new $`), so a rule written `_ $` keeps its material in the
        stem. Rewrite application chooses the side from the rule's environment."""
        if not (0 <= start <= stop <= len(self.segments)):
            raise IndexError(f"replaced({start}, {stop}) outside 0..{len(self.segments)}")
        new = tuple(new)
        delta = len(new) - (stop - start)

        def seg_index(i: int) -> int | None:
            if i < start:
                return i
            if i >= stop:
                return i + delta
            return None

        def start_index(i: int) -> int | None:
            if i == start and new:
                return i
            return seg_index(i)

        def boundary(i: int) -> int | None:
            if i == start and start == stop and before_boundary:
                return i + delta
            if i <= start:
                return i
            if i >= stop:
                return i + delta
            return None

        new_syllables: list[int] = []
        stress_syll: int | None = None
        for k, s in enumerate(self.syllables):
            j = start_index(s)
            if j is None or j in new_syllables:
                continue
            if k == self.stress:
                stress_syll = len(new_syllables)
            new_syllables.append(j)

        nuclei = tuple(
            (a + (delta if a >= stop else 0), b + (delta if a >= stop else 0))
            for a, b in self.nuclei
            if b <= start or a >= stop
        )
        pending = None if self._pending_stress is None else start_index(self._pending_stress)
        return replace(
            self,
            segments=self.segments[:start] + new + self.segments[stop:],
            syllables=tuple(new_syllables),
            nuclei=nuclei,
            stress=stress_syll,
            morphemes=frozenset(j for i in self.morphemes if (j := boundary(i)) is not None),
            illegal=frozenset(j for i in self.illegal if (j := seg_index(i)) is not None),
            secondary=tuple(j for i in self.secondary if (j := seg_index(i)) is not None),
            _pending_stress=pending,
        )

    def traced(self, entry: TraceEntry) -> "Word":
        return replace(self, trace=self.trace + (entry,))

    def with_flag(self, flag: str) -> "Word":
        if flag in self.flags:
            return self
        return replace(self, flags=self.flags + (flag,))

    def fallback_count(self) -> int:
        """Number of trace entries tagged "fallback" (the inventory fallback stage and any
        `%fallback`-tagged rule)."""
        return sum(1 for t in self.trace if t.tag == "fallback")
