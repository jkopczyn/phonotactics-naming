"""Build the PHOIBLE half of ``rules/features.csv`` from the starter CSV (plan Task 1a).

Usage::

    uv run python rules/build_features.py chat-imports/phoible_inventories_starter.csv rules/features.csv

Normalization (plan I-34, spec §12.F): PHOIBLE's dental ``◌̪`` (U+032A) and retracted ``◌̠``
(U+0320) diacritics are stripped so segment spellings agree with the digests. Where the stripped
spelling collides with a spelling PHOIBLE already used (``d l n s t z tʰ``), the row that was
already canonical wins and the dental vector is discarded (they differ only in ``distributed``).
The 11 PHOIBLE diphthong rows are dropped (plan I-2, I-35).

The script refuses to guess: any conflict or collision not listed below raises ``BuildError``.
Standard library only.
"""
from __future__ import annotations

import csv
import io
import sys
import unicodedata
from pathlib import Path

PHOIBLE_38 = ("tone stress syllabic short long consonantal sonorant continuant delayedRelease "
              "approximant tap trill nasal lateral labial round labiodental coronal anterior "
              "distributed strident dorsal high low front back tense retractedTongueRoot "
              "advancedTongueRoot periodicGlottalSource epilaryngealSource spreadGlottis "
              "constrictedGlottis fortis lenis raisedLarynxEjective loweredLarynxImplosive "
              "click").split()
HEADER = ["segment", "class", "source", *PHOIBLE_38]

STRIP_MARKS = {"̪": "", "̠": ""}  # dental, retracted
STRIP_TABLE = str.maketrans(STRIP_MARKS)

# Every spelling the map is expected to change, and the collisions it is expected to create.
# The script fails if the CSV disagrees, so a silently different import cannot happen.
EXPECTED_RENAMES = {
    "d̠ʒ": "dʒ", "d̪": "d", "d̪ˤ": "dˤ", "l̪": "l", "n̪": "n", "s̪": "s", "s̪ˤ": "sˤ",
    "t̪": "t", "t̪ˤ": "tˤ", "z̪": "z", "z̪ˤ": "zˤ", "t̠ʃ": "tʃ", "t̠ʃʼ": "tʃʼ",
    "t̪ʰ": "tʰ", "t̪ʼ": "tʼ",
}
EXPECTED_COLLISIONS = {"d", "l", "n", "s", "t", "z", "tʰ"}
DROPPED_DIPHTHONGS = "ai au ɔi əi əu ɛu ɪu ʊi œy ɔu ɛi".split()
CLASS_OF = {"consonant": "C", "vowel": "V"}


class BuildError(Exception):
    """Raised on any conflict the script is not allowed to resolve silently."""


def normalize(phoneme: str) -> str:
    return unicodedata.normalize("NFC", phoneme).translate(STRIP_TABLE)


def _read_csv(csv_path: Path) -> list[dict[str, str]]:
    with csv_path.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    missing = [f for f in PHOIBLE_38 if f not in rows[0]]
    if missing:
        raise BuildError(f"CSV lacks feature columns: {missing}")
    return rows


def _vector(row: dict[str, str]) -> tuple[str, ...]:
    return tuple(row[f] for f in PHOIBLE_38)


def import_phoible(csv_path: Path) -> list[list[str]]:
    """Return output rows (lists in HEADER order) for the PHOIBLE half, sorted."""
    rows = _read_csv(csv_path)

    # 1. One vector per original spelling; cross-inventory conflicts are fatal.
    by_orig: dict[str, tuple[tuple[str, ...], str, str]] = {}  # spelling -> (vec, InvID, class)
    for row in rows:
        p = unicodedata.normalize("NFC", row["Phoneme"])
        vec = _vector(row)
        cls = CLASS_OF.get(row["SegmentClass"])
        if cls is None:
            raise BuildError(f"{p!r}: unknown SegmentClass {row['SegmentClass']!r}")
        if p in by_orig:
            if by_orig[p][0] != vec:
                raise BuildError(f"{p!r}: feature vectors differ across inventories")
            if by_orig[p][2] != cls:
                raise BuildError(f"{p!r}: SegmentClass differs across inventories")
        else:
            by_orig[p] = (vec, row["InventoryID"], cls)

    # 2. Normalize spellings; check the map does exactly what the plan says.
    renames = {p: normalize(p) for p in by_orig if normalize(p) != p}
    if renames != EXPECTED_RENAMES:
        raise BuildError(f"normalization map changed: got {renames}")

    # 3. Resolve collisions: canonical original spelling wins.
    groups: dict[str, list[str]] = {}
    for p in by_orig:  # file order preserved
        groups.setdefault(normalize(p), []).append(p)
    collisions = {k for k, v in groups.items() if len(v) > 1}
    if collisions != EXPECTED_COLLISIONS:
        raise BuildError(f"collision set changed: got {sorted(collisions)}")
    kept: dict[str, tuple[tuple[str, ...], str, str]] = {}
    for canon, originals in groups.items():
        if len(originals) == 1:
            kept[canon] = by_orig[originals[0]]
        elif canon in originals:
            kept[canon] = by_orig[canon]
        else:
            raise BuildError(f"{canon!r}: collision with no canonical original: {originals}")

    # 4. Drop diphthongs (plan I-35).
    for d in DROPPED_DIPHTHONGS:
        if d not in kept:
            raise BuildError(f"expected diphthong row {d!r} not in CSV")
        del kept[d]

    # 5. Contour values. The dropped diphthongs carried several ("-,+"); the only ones left are
    #    the pharyngealized consonants' retractedTongueRoot = "-,+" (PHOIBLE encodes the
    #    secondary articulation as an offglide). The whole segment is pharyngealized, and this
    #    is the sole feature separating sˤ from s, so it resolves to "+". Anything else is fatal.
    out = []
    for seg, (vec, inv, cls) in kept.items():
        vec = tuple(_resolve_contour(seg, f, v) for f, v in zip(PHOIBLE_38, vec))
        out.append([seg, cls, f"phoible:{inv}", *vec])
    return sort_rows(out)


def _resolve_contour(seg: str, feature: str, value: str) -> str:
    if value in {"+", "-", "0"}:
        return value
    if seg.endswith("ˤ") and feature == "retractedTongueRoot" and value == "-,+":
        return "+"
    raise BuildError(f"{seg!r}: unexpected feature value {value!r} for {feature}")


def sort_rows(rows: list[list[str]]) -> list[list[str]]:
    """Sort by (class, segment code points) for byte-stable rebuilds."""
    return sorted(rows, key=lambda r: (r[1], r[0]))


def read_csv(path: Path) -> list[list[str]]:
    with path.open(encoding="utf-8", newline="") as fh:
        reader = csv.reader(fh)
        header = next(reader)
        if header != HEADER:
            raise BuildError(f"{path}: unexpected header")
        return [row for row in reader if row]


def write_csv(rows: list[list[str]], out_path: Path) -> None:
    buf = io.StringIO()
    writer = csv.writer(buf, lineterminator="\n")
    writer.writerow(HEADER)
    writer.writerows(rows)
    lines = buf.getvalue().splitlines()
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def main(csv_path: Path, out_path: Path, *, sort_only: bool = False) -> None:
    """Build ``out_path``.

    With ``sort_only=True``, ``csv_path`` is instead an existing ``features.csv`` (PHOIBLE rows plus
    any hand rows) that is re-sorted into canonical order without re-importing PHOIBLE.
    """
    rows = read_csv(csv_path) if sort_only else import_phoible(csv_path)
    if len({r[0] for r in rows}) != len(rows):
        raise BuildError("duplicate segments in output")
    write_csv(sort_rows(rows), out_path)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = {a for a in sys.argv[1:] if a.startswith("--")}
    if len(args) != 2 or flags - {"--sort-only"}:
        sys.exit("usage: build_features.py [--sort-only] <phoible.csv | features.csv> <features.csv>")
    main(Path(args[0]), Path(args[1]), sort_only="--sort-only" in flags)
