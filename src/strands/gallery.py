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

from collections.abc import Sequence

from .dsl import RuleFile
from .features import FeatureTable
from .inputs import Entry
from .irish import MissingSlot
from .lexicon import LexEntry, key, read_lexicon
from .pipeline import ConstructionNotInStrand, PipelineError, Result, run_entry
from .tokenize import SegmentError

__all__ = [
    "REFERENCE_NAMES",
    "FORMATION_TEMPLATES",
    "FORMATION_ELEMENTS",
    "FORMATION_NAMES",
    "reference_row",
    "render_cell",
    "render_gallery",
    "formation_block",
]

REFERENCE_NAMES = ("Tchaeul", "Th'tysh", "Kas'queil", "Xelxyx", "Ysclyth")
"""The five pre-existing strand-4 names (notes/project-goals.md). Spec §12.J: they are
CANON INPUTS — the gallery displays them verbatim in a reference row and never passes
them through the engine. `render_gallery` emits this row from the literal tuple; no
adapt(), run_entry() or tokenize() call touches them."""

SKIPPED = "—"

# ---- the Old Irish formation block (Old Irish spec §7, §8 row O6; plan Task 18, R31) --------
FORMATION_TEMPLATES = ("MAEL", "GILLA", "CU", "FER", "COLOUR", "MAC", "UA", "INGEN")
FORMATION_ELEMENTS = ("Maol", "Giolla", "cú", "fear", "dubh", "mac", "ua", "inion")
"""The lexicon ELEMENT rows the templates' literals come from (Task 3 guarantees them), by
their modern keys: *Máel, Gilla, cú, fer, dub, macc, aue, ingen*. Each is shown going
through lookup on its own so the reviewer sees the element the literal stands for."""
FORMATION_NAMES = ("Colm", "Pádraig", "Culann")
"""The governed names: the second elements of the attested *Máel Coluim*, *Gilla Pátraic*
and *Cú Chulainn*. R31: the whole-name rows return ATTESTED in one piece and never
exercise a template, so the block is built from these element rows instead."""
FORMATION_COLOUR = "dubh"
"""COLOUR's first slot (*Dubthach* = dub + -thach, R31a)."""


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


def run_cell(
    entry: Entry,
    construction: str,
    irish: RuleFile,
    target: RuleFile,
    table: FeatureTable,
    slots: dict[str, Entry] | None = None,
) -> Result | None:
    """`run_entry`, or None when the entry has no IPA, the template needs a slot the
    entry cannot fill, or the strand has no template of that name (the skips `strands run`
    reports as notes; Old Irish O-17)."""
    if not entry.ipa:
        return None
    try:
        return run_entry(entry, construction, irish, target, table, slots)
    except (MissingSlot, ConstructionNotInStrand):  # Old Irish O-17
        return None
    except SegmentError as e:
        raise SegmentError(f"{entry.orthography} [{construction}]: {e}") from e


def _element_entry(
    lexicon: dict[str, LexEntry], name: str, irish: RuleFile, table: FeatureTable
) -> tuple[LexEntry, Entry]:
    """The lexicon row for a modern key and an `Entry` built from its `orthography` with a
    G2P transcription, tagged `ipa:constructed` (the elements are not test-words rows)."""
    from .inputs import construct_ipa, infer

    row = lexicon.get(key(name))
    if row is None:
        raise PipelineError(f"old-irish-lexicon: no row for the formation element {name!r}")
    ipa, tags = construct_ipa(row.orthography, "C")
    entry = Entry(
        orthography=row.orthography,
        ipa=ipa,
        dialect="C",
        gender=row.gender or "m",
        assumptions=tags,
    )
    return row, infer(entry, irish, table)


def formation_block(
    irish: RuleFile,
    target: RuleFile,
    table: FeatureTable,
    lexicon: dict[str, LexEntry] | None = None,
) -> list[str]:
    """Markdown lines for the Old Irish formation block (spec §7): the element rows through
    lookup (DESC, GEN), then the eight formation templates over the governed names. Every
    cell is `render_cell` output, so the lookup flags show as in the main tables."""
    lexicon = read_lexicon() if lexicon is None else lexicon
    lines = [
        "## Old Irish formations",
        "",
        "The eight formation templates (spec §8 row O6) over lexicon ELEMENT rows; each "
        "element's IPA is constructed by the G2P (`ipa:constructed`). A whole-name row "
        "(*Máel Coluim*) returns ATTESTED in one piece and never exercises a template. "
        "The governed names are the element rows Task 3 could cite (*Colum*, *Pátraic*, "
        "*Culann*); *Fer Diad*'s *Diad* and *Dubthach*'s *-thach* have none "
        "(old-irish-lexicon-log), so FER and COLOUR run over the same three. A "
        "lower-case lexicon element (*dub*, *macc*, *aue*, *ingen*) stays lower-case "
        "(O-32).",
        "",
        "| element | Old Irish | DESC | GEN |",
        "|---|---|---|---|",
    ]
    for name in FORMATION_ELEMENTS + FORMATION_NAMES:
        row, entry = _element_entry(lexicon, name, irish, table)
        cells = [render_cell(run_cell(entry, c, irish, target, table)) for c in ("DESC", "GEN")]
        lines.append(f"| {_md(row.orthography)} | {_md(row.oi_nom)} | " + " | ".join(cells) + " |")
    lines.append("")
    _, colour = _element_entry(lexicon, FORMATION_COLOUR, irish, table)
    governed = [_element_entry(lexicon, name, irish, table)[1] for name in FORMATION_NAMES]
    lines.append("| formation | " + " | ".join(_md(e.orthography) for e in governed) + " |")
    lines.append("|---|" + "---|" * len(governed))
    for construction in FORMATION_TEMPLATES:
        cells = []
        for entry in governed:
            slots = {"COLOUR": colour, "NAME": entry} if construction == "COLOUR" else None
            cells.append(render_cell(run_cell(entry, construction, irish, target, table, slots)))
        lines.append(f"| {construction} | " + " | ".join(cells) + " |")
    lines.append("")
    return lines


def render_gallery(
    entries: Sequence[Entry],
    targets: Sequence[tuple[str, RuleFile]],
    constructions: Sequence[str],
    table: FeatureTable,
    *,
    irish: RuleFile,
) -> str:
    """Markdown: a reference table (canon names) then one table per entry. `targets` are
    `(name, rule_file)` pairs in the column order wanted."""
    names = [name for name, _ in targets]
    lines = ["# Strand gallery", "", "| | names |", "|---|---|", reference_row(), ""]
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
            cells = [
                render_cell(run_cell(entry, construction, irish, rf, table)) for _, rf in targets
            ]
            if all(cell == SKIPPED for cell in cells):
                continue
            lines.append(f"| {construction} | " + " | ".join(cells) + " |")
        lines.append("")
    for name, rf in targets:
        if name == "old-irish":  # spec §7: the formation block
            lines.extend(formation_block(irish, rf, table))
    return "\n".join(lines).rstrip("\n") + "\n"
