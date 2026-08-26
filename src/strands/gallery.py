"""`strands gallery`: words × constructions × strands as Markdown (plan Task 27; spec §6).

One `## <orthography>` section per input entry, with a table whose rows are constructions
and whose columns are the target strands; each cell is `respelling /ipa/` (plus `!FLAG`
markers and `+N` for N fallbacks), or `—` where the pipeline skipped the cell (no IPA, or a
multi-slot template that one entry cannot fill). A construction whose row is `—` for every
strand is left out of that word's table. Everything is emitted in input / `targets` /
`constructions` order, so the output is a deterministic function of its inputs (Task 28
snapshots it).

Spec §12.J: the five pre-existing strand-4 names are CANON INPUTS. `reference_row()` prints
them verbatim from `REFERENCE_NAMES`; nothing in this module tokenizes, adapts or otherwise
touches them.
"""
from __future__ import annotations

from typing import Sequence

from .dsl import RuleFile
from .features import FeatureTable
from .inputs import Entry
from .irish import MissingSlot
from .pipeline import Result, run_entry

__all__ = ["REFERENCE_NAMES", "reference_row", "render_cell", "render_gallery"]

REFERENCE_NAMES = ("Tchaeul", "Th'tysh", "Kas'queil", "Xelxyx", "Ysclyth")
"""The five pre-existing strand-4 names (notes/project-goals.md). Spec §12.J: they are
CANON INPUTS — the gallery displays them verbatim in a reference row and never passes
them through the engine. `render_gallery` emits this row from the literal tuple; no
adapt(), run_entry() or tokenize() call touches them."""

SKIPPED = "—"


def reference_row() -> str:
    """The canon names, verbatim (spec §12.J). No engine call is made."""
    return "| reference (canon, verbatim) | " + " · ".join(REFERENCE_NAMES) + " |"


def _md(text: str) -> str:
    return text.replace("|", "\\|")


def render_cell(result: Result | None) -> str:
    """`respelling /ipa/`, with `!FLAG` per flag and `+N` for N>0 fallbacks; `—` when the
    cell was skipped."""
    if result is None:
        return SKIPPED
    parts = [f"{result.respelling} /{result.ipa}/"]
    parts.extend(f"!{flag}" for flag in result.flags)
    if result.fallbacks:
        parts.append(f"+{result.fallbacks}")
    return _md(" ".join(parts))


def run_cell(entry: Entry, construction: str, irish: RuleFile, target: RuleFile,
             table: FeatureTable) -> Result | None:
    """`run_entry`, or None when the entry has no IPA or the template needs a slot the
    entry cannot fill (the same two skips `strands run` reports as notes)."""
    if not entry.ipa:
        return None
    try:
        return run_entry(entry, construction, irish, target, table)
    except MissingSlot:
        return None


def render_gallery(entries: Sequence[Entry], targets: Sequence[tuple[str, RuleFile]],
                   constructions: Sequence[str], table: FeatureTable, *,
                   irish: RuleFile) -> str:
    """Markdown: a reference table (canon names) then one table per entry. `targets` are
    `(name, rule_file)` pairs in the column order wanted."""
    names = [name for name, _ in targets]
    lines = ["# Strand gallery", "",
             "| | names |", "|---|---|", reference_row(), ""]
    for entry in entries:
        title = _md(entry.orthography)
        if entry.gloss:
            title += f" — {_md(entry.gloss)}"
        lines.append(f"## {title}")
        lines.append("")
        if not entry.ipa:
            lines.append("skipped: no IPA")
            lines.append("")
            continue
        lines.append(f"Irish: /{_md(entry.ipa)}/")
        lines.append("")
        lines.append("| construction | " + " | ".join(names) + " |")
        lines.append("|---|" + "---|" * len(names))
        for construction in constructions:
            cells = [render_cell(run_cell(entry, construction, irish, rf, table))
                     for _, rf in targets]
            if all(cell == SKIPPED for cell in cells):
                continue
            lines.append(f"| {construction} | " + " | ".join(cells) + " |")
        lines.append("")
    return "\n".join(lines).rstrip("\n") + "\n"
