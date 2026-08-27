"""Stress package: procedure registry, syllable weight, dispatch.

Plan Task 12; spec §3 `[stress]` (`procedure = initial | penult | cairene | dutch-weight |
keep-source` plus procedure-specific `key = value` parameters), §12.B (weight counts NUCLEI,
not vowel segments: a licensed diphthong is one branching nucleus). I-17: the permitted
parameter set per procedure is the data-only table in `params.py`, shared with `strands
check`; I-40: secondary stress is never carried into a target — every target assigns its own.

Registry. Each procedure lives in its own module (`initial.py`, `keep_source.py`, and Tasks
13–15's `penult.py`, `cairene.py`, `dutch_weight.py`) and registers itself with
`@register("<name>")`. Importing this package imports every sibling module (sorted, so the
order is deterministic) — a new procedure module therefore needs no edit here.

Weight. `syllable_weight(word, i, table)` classifies syllable `i`:
- `light`      — open syllable, single short nucleus segment;
- `heavy`      — long (`long=+`) or branching (≥2-segment) nucleus with no coda, OR a short
                 nucleus with exactly one coda segment;
- `superheavy` — long/branching nucleus with ≥1 coda segment, OR ≥2 coda segments.
The coda is everything from the nucleus end to the next syllable start (or word end).
"""
from __future__ import annotations

import importlib
import pkgutil
from collections.abc import Callable
from dataclasses import replace

from ..dsl import RuleFile, StressSpec
from ..features import FeatureTable
from ..word import TraceEntry, Word
from .params import PROCEDURE_PARAMS

__all__ = ["PROCEDURE_PARAMS", "PROCEDURES", "Procedure", "StressError", "register",
           "syllable_weight", "assign_stress"]

Procedure = Callable[[Word, StressSpec, FeatureTable], "int | None"]
PROCEDURES: dict[str, Procedure] = {}

_STAGE = "stress"


class StressError(Exception):
    """An unknown stress procedure, or a procedure returning an out-of-range syllable."""


def register(name: str) -> Callable[[Procedure], Procedure]:
    """Decorator: `@register("initial")` puts the procedure in `PROCEDURES`. Registering a
    name twice is a programming error (two modules claiming one procedure)."""
    def deco(fn: Procedure) -> Procedure:
        if name in PROCEDURES and PROCEDURES[name] is not fn:
            raise StressError(f"stress procedure {name!r} registered twice")
        PROCEDURES[name] = fn
        return fn
    return deco


# ---- weight (spec §12.B) ---------------------------------------------------------------------

def _syllable_span(word: Word, i: int) -> tuple[int, int]:
    if not (0 <= i < len(word.syllables)):
        raise IndexError(f"syllable {i} outside 0..{len(word.syllables) - 1}")
    start = word.syllables[i]
    stop = word.syllables[i + 1] if i + 1 < len(word.syllables) else len(word.segments)
    return start, stop


def syllable_weight(word: Word, i: int, table: FeatureTable) -> str:
    """'light' (open, short nucleus) | 'heavy' (long/branching nucleus, or one coda C)
    | 'superheavy' (long nucleus + coda, or two coda C). Counts NUCLEI, not vowel
    segments (spec §12.B). A syllable without a nucleus (an illegal parse) is 'light'."""
    start, stop = _syllable_span(word, i)
    nucleus = next(((a, b) for a, b in word.nuclei if start <= a < stop), None)
    if nucleus is None:
        return "light"
    a, b = nucleus
    branching = (b - a) >= 2
    long = any(table.value(s, "long") == "+" for s in word.segments[a:b])
    coda = min(stop, len(word.segments)) - b
    if long or branching:
        return "superheavy" if coda >= 1 else "heavy"
    if coda >= 2:
        return "superheavy"
    if coda == 1:
        return "heavy"
    return "light"


# ---- dispatch ----------------------------------------------------------------------------------

def assign_stress(word: Word, rf: RuleFile, table: FeatureTable) -> Word:
    """Dispatch on rf.stress.procedure; sets word.stress; appends a TraceEntry
    (stage='stress', rule_id=f'stress:{procedure}'). Unknown name -> StressError.
    A rule file without `[stress]` leaves the word untouched (no trace entry)."""
    spec = rf.stress
    if spec is None:
        return word
    try:
        proc = PROCEDURES[spec.procedure]
    except KeyError:
        raise StressError(f"unknown stress procedure {spec.procedure!r}; registered: "
                          f"{', '.join(sorted(PROCEDURES))}") from None
    index = proc(word, spec, table)
    if index is not None and not (0 <= index < len(word.syllables)):
        raise StressError(f"procedure {spec.procedure!r} returned syllable {index} for "
                          f"{word.ipa()!r} with {len(word.syllables)} syllables")
    out = replace(word, stress=index)
    note = "" if index is not None else "no syllables"
    return out.traced(TraceEntry(stage=_STAGE, rule_id=f"{_STAGE}:{spec.procedure}", tag="",
                                 before=word.ipa(), after=out.ipa(), note=note))


# ---- load every procedure module (deterministic order) --------------------------------------

for _info in sorted(pkgutil.iter_modules(__path__), key=lambda m: m.name):
    if _info.name != "params":
        importlib.import_module(f"{__name__}.{_info.name}")
del _info
