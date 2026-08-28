"""The Old Irish lexicon: `rules/old-irish-lexicon.csv` (Old Irish spec §3, §7, §10; plan Task 2).

The file maps a modern Irish CITATION form (`orthography`) to its attested Old Irish nominative
and genitive spellings, stem class and gender, or records that no Old Irish form exists
(`status = none`) with a `kind` of `loan` or `late` (spec §10). Lookup (plan Task 12) keys on
`key(orthography)` — NFC + strip + casefold (O-19) — and never de-mutates: a corpus row whose
own orthography is a surface form (*a Sheáin*) is a RETRO miss by design (O-23).

Every row cites a page (`source`): a URL, `digest §10.n`, `strachan1909 p.N` or
`pokorny1914 p.N`. Uncited or oddly-cited rows are errors (spec §3).

Validation findings are `check.CheckError`s. `LEX_NONE_HAS_FORM`, `LEX_NONE_NO_KIND` and
`LEX_IRREGULAR_NO_GEN` were warnings while the harvest was a Task 3 backlog and are errors since
that task closed it (R3a). The one remaining warning, `LEX_NEEDS_TASK3`, marks a form-bearing row
with a blank `stem` or `gender` that does not explain itself: a `note` starting
`no nominal paradigm:` (adjective / numeral / prefix / phrase) or `unattested:` (a noun whose
class the cited sources do not show; Task 14 infers and tags it, O-33) is exempt.
"""

from __future__ import annotations

import csv
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path

__all__ = [
    "EXEMPT_NOTE_PREFIXES",
    "FORM_STATUSES",
    "GENDERS",
    "KINDS",
    "LEXICON_COLUMNS",
    "STATUSES",
    "STEMS",
    "LexEntry",
    "LexiconError",
    "default_lexicon_path",
    "key",
    "read_lexicon",
    "read_rows",
    "validate",
]

LEXICON_COLUMNS = (
    "orthography",
    "oi_nom",
    "oi_gen",
    "stem",
    "gender",
    "status",
    "kind",
    "source",
    "note",
)
STEMS = ("o", "ā", "i", "u", "n", "dental", "velar", "r", "s", "indecl", "irregular")
GENDERS = ("m", "f", "n")
STATUSES = ("attested", "middle", "none")
KINDS = ("loan", "late")
FORM_STATUSES = ("attested", "middle")
EXEMPT_NOTE_PREFIXES = ("no nominal paradigm:", "unattested:")

_SOURCE_SHAPES = (
    re.compile(r"^https?://"),
    re.compile(r"^digest §10\.\d+"),
    re.compile(r"^strachan1909 p\.\d+"),
    re.compile(r"^pokorny1914 p\.\d+"),
)


class LexiconError(Exception):
    """Raised for a file that cannot be read as a lexicon at all (missing, bad header)."""


@dataclass(frozen=True)
class LexEntry:
    orthography: str
    oi_nom: str = ""
    oi_gen: str = ""
    stem: str = ""
    gender: str = ""
    status: str = "attested"
    kind: str = ""
    source: str = ""
    note: str = ""
    line: int = 0
    cells: int = len(LEXICON_COLUMNS)  # the row's ACTUAL cell count (LEX_ROW_SHAPE)

    @property
    def flag(self) -> str:
        """The Result flag this row yields on a lookup hit (spec §2, §10; O-18, O-22)."""
        if self.status == "middle":
            return "ATTESTED:MIr"
        if self.status == "none":
            return f"RETRO:{self.kind}" if self.kind else "RETRO"
        return "ATTESTED"


def key(text: str) -> str:
    """Lookup key: NFC + strip + casefold (O-19)."""
    return unicodedata.normalize("NFC", text).strip().casefold()


def default_lexicon_path() -> Path:
    return Path(__file__).resolve().parents[2] / "rules" / "old-irish-lexicon.csv"


def _nfc(s: str) -> str:
    return unicodedata.normalize("NFC", s)


def read_rows(path: str | Path | None = None) -> tuple[list[str], list[LexEntry]]:
    """Read the file as-is: header cells and one LexEntry per non-blank data line, in file
    order, with 1-based line numbers. Does NOT validate — a wrong header still yields entries
    (cells mapped positionally onto LEXICON_COLUMNS) so `validate` can report LEX_HEADER;
    a row of the wrong width is likewise padded/cut for the entry but keeps its true count in
    `cells` so `validate` can report LEX_ROW_SHAPE."""
    path = default_lexicon_path() if path is None else Path(path)
    try:
        text = _nfc(path.read_text(encoding="utf-8"))
    except OSError as e:
        raise LexiconError(f"cannot read lexicon {path}: {e}") from e
    lines = text.splitlines()
    if not lines:
        raise LexiconError(f"empty lexicon {path}")
    header = [c.strip() for c in next(csv.reader([lines[0]]))]
    entries: list[LexEntry] = []
    for lineno, line in enumerate(lines[1:], start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        cells = [c.strip() for c in next(csv.reader([line]))]
        width = len(LEXICON_COLUMNS)
        entries.append(LexEntry(*(cells + [""] * width)[:width], line=lineno, cells=len(cells)))
    return header, entries


def read_lexicon(path: str | Path | None = None) -> dict[str, LexEntry]:
    """`key(orthography)` -> entry. Raises LexiconError on a wrong header or any error-severity
    finding; the first row wins nothing — duplicates are an error, not a tie-break."""
    path = default_lexicon_path() if path is None else Path(path)
    header, entries = read_rows(path)
    errors = [e for e in validate(header, entries, path) if e.severity == "error"]
    if errors:
        first = errors[0]
        raise LexiconError(
            f"{path}:{first.line}: {first.code}: {first.message}"
            + (f" (+{len(errors) - 1} more)" if len(errors) > 1 else "")
        )
    return {key(e.orthography): e for e in entries}


def validate(header: list[str], entries: list[LexEntry], path: str | Path | None = None) -> list:
    """Every finding at once (never raises), sorted by line then code. Codes and severities
    are the plan Task 2 table; the `path` is only echoed in messages."""
    from .check import CheckError

    out: list[CheckError] = []

    def add(line: int, code: str, message: str, severity: str = "error") -> None:
        out.append(CheckError(line, code, message, severity))

    if tuple(header) != LEXICON_COLUMNS:
        add(1, "LEX_HEADER", f"header is {header!r}; expected {list(LEXICON_COLUMNS)!r}")

    seen: dict[str, int] = {}
    for e in entries:
        if e.cells != len(LEXICON_COLUMNS):
            add(
                e.line,
                "LEX_ROW_SHAPE",
                f"{e.orthography!r}: {e.cells} comma-separated cells; expected "
                f"{len(LEXICON_COLUMNS)}",
            )
        k = key(e.orthography)
        if not k:
            add(e.line, "LEX_NO_KEY", "empty orthography")
        elif k in seen:
            add(e.line, "LEX_DUPLICATE_KEY", f"key {k!r} already on line {seen[k]}")
        else:
            seen[k] = e.line

        if e.status not in STATUSES:
            add(e.line, "LEX_STATUS", f"status {e.status!r} not in {STATUSES}")
        if not e.source:
            add(e.line, "LEX_NO_SOURCE", f"{e.orthography!r}: no source cited")
        elif not any(p.match(e.source) for p in _SOURCE_SHAPES):
            add(
                e.line,
                "LEX_SOURCE_SHAPE",
                f"{e.orthography!r}: source {e.source!r} is not a URL, 'digest §10.n', "
                "'strachan1909 p.N' or 'pokorny1914 p.N'",
            )
        if e.stem and e.stem not in STEMS:
            add(e.line, "LEX_STEM", f"{e.orthography!r}: stem {e.stem!r} not in {STEMS}")
        if e.gender and e.gender not in GENDERS:
            add(e.line, "LEX_GENDER", f"{e.orthography!r}: gender {e.gender!r} not in {GENDERS}")

        if e.status in FORM_STATUSES:
            if not e.oi_nom:
                add(
                    e.line,
                    "LEX_ATTESTED_NO_NOM",
                    f"{e.orthography!r}: status {e.status} but no oi_nom",
                )
            if e.kind:
                add(
                    e.line,
                    "LEX_KIND_ON_FORM_ROW",
                    f"{e.orthography!r}: kind {e.kind!r} on a {e.status} row",
                )
            if (not e.stem or not e.gender) and not e.note.startswith(EXEMPT_NOTE_PREFIXES):
                add(
                    e.line,
                    "LEX_NEEDS_TASK3",
                    f"{e.orthography!r}: stem={e.stem or '-'} gender={e.gender or '-'} "
                    "(blank, and the note does not explain it)",
                    "warning",
                )
        elif e.status == "none":
            if e.oi_nom or e.oi_gen or e.stem or e.gender:
                add(
                    e.line,
                    "LEX_NONE_HAS_FORM",
                    f"{e.orthography!r}: status none but carries a form/stem/gender",
                )
            if e.kind not in KINDS:
                add(
                    e.line,
                    "LEX_NONE_NO_KIND",
                    f"{e.orthography!r}: status none needs kind in {KINDS}",
                )
        if e.stem == "irregular" and not e.oi_gen:
            add(e.line, "LEX_IRREGULAR_NO_GEN", f"{e.orthography!r}: stem irregular needs oi_gen")

    out.sort(key=lambda c: (c.line, c.code))
    return out
