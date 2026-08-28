"""Respell stage: `[respell]` over the annotated token stream (plan Task 21; spec §3, §12.C).

The section is applied rule by rule in file order against the ANNOTATED token stream — the
word's segments with their syllable starts, stress and morpheme boundaries — so a context may
use `.`, `ˈ`, `$` and `#` exactly as any other section does (I-8). Every match of a rule
replaces its span by an opaque OUTPUT CHUNK (I-19): the quoted string, or, for a rule whose
replacement is IPA segments or a feature-change bundle, the joined result. A chunk is never
rematched by a later rule's TARGET; later rules' contexts are still evaluated against the
original stream (the annotations belong to the segments, not to the chunks). Segments that no
rule matched pass through as themselves.

After the rules, `.`, `ˈ` and `ˌ` are stripped in code, unconditionally (I-8, spec §12.C): a
respelling is an English-reader form and never carries phonological marks. Whether `Result.ipa`
prints the stress mark is a separate question (`[stress] mark`, see `pipeline.adapt`).
"""

from __future__ import annotations

from .dsl import RuleFile
from .features import FeatureTable
from .rewrite import _replacement, find_matches
from .word import TraceEntry, Word

__all__ = ["STAGE", "MARKS", "respell", "respell_traced"]

STAGE = "respell"
MARKS = (".", "ˈ", "ˌ")


def _render(
    segments: tuple[str, ...], chunks: dict[int, tuple[int, str]], inserts: dict[int, list[str]]
) -> str:
    """Join chunks (start -> (stop, text)), zero-width insertions (position -> texts, rendered
    before the segment at that position; position len(segments) is the word end) and
    pass-through segments, in order. An insertion point strictly inside a chunk's span is
    never visited, so the chunk swallows it (it is opaque)."""
    out: list[str] = []
    i = 0
    while True:
        out.extend(inserts.get(i, ()))
        if i >= len(segments):
            break
        if i in chunks:
            stop, text = chunks[i]
            out.append(text)
            i = stop
        else:
            out.append(segments[i])
            i += 1
    return "".join(out)


def _strip_marks(text: str) -> str:
    for mark in MARKS:
        text = text.replace(mark, "")
    return text


def respell_traced(
    word: Word, rf: RuleFile, table: FeatureTable
) -> tuple[str, tuple[TraceEntry, ...]]:
    """`respell()` plus one TraceEntry per rule that produced a chunk (stage "respell",
    rule_id "respell:<line>"), recording the rendered stream before and after."""
    rules = rf.sections.get(STAGE, ())
    chunks: dict[int, tuple[int, str]] = {}
    inserts: dict[int, list[str]] = {}
    claimed: set[int] = set()
    trace: list[TraceEntry] = []
    for rule in rules:
        before = _render(word.segments, chunks, inserts)
        fired = False
        for start, stop, caps in find_matches(word, rule, rf, table):
            text = "".join(_replacement(word, rule, start, stop, caps, table))
            if not rule.target:  # epenthesis: a chunk of width zero
                # An insertion sits BEFORE the segment at `start` (or at the word end when
                # start == len(segments)). It claims no segment, so later rules still match
                # the segment after it; one strictly inside an existing chunk is dropped.
                if any(cs < start < ce for cs, (ce, _) in chunks.items()):
                    continue
                inserts.setdefault(start, []).append(text)
                fired = True
                continue
            span = range(start, stop)
            if any(i in claimed for i in span):
                continue  # opaque chunk (I-19): never rematched
            chunks[start] = (stop, text)
            claimed.update(span)
            fired = True
        if fired:
            trace.append(
                TraceEntry(
                    stage=STAGE,
                    rule_id=rule.rule_id,
                    tag=rule.tag,
                    before=before,
                    after=_render(word.segments, chunks, inserts),
                )
            )
    return _strip_marks(_render(word.segments, chunks, inserts)), tuple(trace)


def respell(word: Word, rf: RuleFile, table: FeatureTable) -> str:
    """Spec §12.C: apply rf.sections['respell'] over the ANNOTATED TOKEN STREAM.
    A quoted replacement becomes an opaque chunk that later rules never rematch;
    unmatched segments pass through as themselves. After the rules, `.` and `ˈ` are
    ALWAYS stripped in code (no DSL cleanup lines — I-8): a respelling is an
    English-reader form and never carries phonological marks. Georgian's
    `[stress] mark = off` therefore has nothing to do with this function — it governs
    whether `Result.ipa` prints the stress mark (see `pipeline.adapt`)."""
    return respell_traced(word, rf, table)[0]
