"""Input TSV, inference of missing fields, and `strands lint` (plan Task 20; spec §5, §12.H).

An input file is a TSV whose header carries some of `INPUT_COLUMNS`; only `orthography` is
required. Columns the spec does not name (test-words.tsv's `features`) are ignored; absent
columns read as "". `infer()` fills what is missing and records every guess in
`Entry.assumptions` as a `field:reason` tag, so `lint_report()` can list the guesses and
`accept_guesses()` can write them back into the file.

Inference order (spec §5, I-38):

1. `dialect` "" -> "C"                                       `dialect:default-C`
2. `gender` "" -> the known-name list (built from test-words.tsv glosses that say
   "(m. given name)" / "(f. given name)"), then orthographic endings, else "m"
                                    `gender:known-name` / `gender:ending` / `gender:default-m`
3. `declension` from ending shape + gender          `declension:inferred-<rule>`
4. `gen_ipa` "" -> `apply_inflection(word, GEN_<DECL>)` (`d4` = stem unchanged), so the
   genitive has exactly one implementation (R27)          `gen_ipa:inferred-<decl>`

Steps 3–4 look at the `ipa` AFTER the `irish.rules [normalize]` rewrites (Task 19 accepts
aliases such as ASCII `g` and quality-less consonants, which are in neither `BROAD` nor
`SLEN`), so an alias-final feminine noun is `f2`, not the `m1` default, and the inferred
`gen_ipa` is canonical. No stress is added to the stored `gen_ipa`.

A row with no `ipa` is kept, tagged `skipped:no-ipa`; steps 1–3 still run on its
orthography, step 4 is skipped. Supplied values are never overwritten.

`declension` is not an input column, so its dataclass default "m1" (the `GEN()` fallback of
I-38) is treated as "not yet inferred": `infer()` re-derives it whenever it is "" or "m1"
and keeps any other value. A row that really is `m1` therefore always carries a
`declension:inferred-m1` tag.
"""
from __future__ import annotations

import csv
import functools
import re
import unicodedata
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Sequence

from .dsl import RuleFile
from .features import FeatureTable
from .irish import _normalize_rewrites, apply_inflection
from .tokenize import tokenize
from .word import Word

__all__ = ["INPUT_COLUMNS", "DECLENSIONS", "Entry", "read_input", "infer", "lint_report",
           "accept_guesses", "known_names"]

INPUT_COLUMNS = ("orthography", "ipa", "dialect", "gloss", "category",
                 "gender", "gen_ipa", "pl_ipa", "note")
DECLENSIONS = ("m1", "ach", "f2", "m3", "d4")
_INFERRED_COLUMNS = ("dialect", "gender", "gen_ipa")    # what accept_guesses writes back
_DEFAULT_DECLENSION = "m1"

# Spec §5 ending heuristics, over NFC orthography (lower-cased). Order matters: the
# masculine diminutive -ín ends in a slender consonant, so it is tested before the
# slender-final rule. -óir/-eoir agent nouns are masculine (digest §3.5's 3rd declension
# example *bádóir*); listing them here keeps gender and declension consistent.
_FEM_ENDINGS = ("óg", "eog")
_MASC_ENDINGS = ("ach", "án", "ín", "óir", "eoir")
_M3_ENDINGS = ("óir", "eoir", "úil")
_VOWEL_LETTERS = "aeiouáéíóú"
_SLENDER_LETTERS = "eiéí"
_NAME_GLOSS_RE = re.compile(r"\(([mf])\. given name\)")
_TEST_WORDS = Path(__file__).resolve().parents[2] / "sources" / "irish" / "test-words.tsv"


@dataclass(frozen=True)
class Entry:
    orthography: str
    ipa: str = ""
    dialect: str = "C"
    gloss: str = ""
    category: str = ""
    gender: str = "m"
    declension: str = _DEFAULT_DECLENSION      # m1 | ach | f2 | m3 | d4   (I-38)
    gen_ipa: str = ""
    pl_ipa: str = ""
    note: str = ""
    assumptions: tuple[str, ...] = ()


class InputError(Exception):
    """The input file has no usable header."""


def _nfc(s: str | None) -> str:
    return unicodedata.normalize("NFC", (s or "").strip())


def _read_rows(path: str | Path) -> tuple[list[str], list[dict[str, str]]]:
    with Path(path).open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh, delimiter="\t")
        header = [_nfc(h) for h in (reader.fieldnames or [])]
        rows = [{_nfc(k): _nfc(v) for k, v in row.items() if k is not None} for row in reader]
    return header, rows


def read_input(path: str | Path) -> list[Entry]:
    """Header must contain `orthography`; unknown columns (e.g. test-words.tsv's `features`)
    are ignored; missing ones read as "" (so `infer()` fills and tags them). A row with no
    `ipa` returns ipa='' and assumption 'skipped:no-ipa'. Blank rows are dropped."""
    header, rows = _read_rows(path)
    if "orthography" not in header:
        raise InputError(f"{path}: header must contain 'orthography' (have: {header})")
    out: list[Entry] = []
    for row in rows:
        if not row.get("orthography"):
            continue
        fields = {c: row.get(c, "") for c in INPUT_COLUMNS}
        assumptions = ("skipped:no-ipa",) if not fields["ipa"] else ()
        out.append(Entry(**fields, assumptions=assumptions))
    return out


@functools.lru_cache(maxsize=None)
def known_names(path: str | Path = _TEST_WORDS) -> dict[str, str]:
    """orthography (lower-cased NFC) -> 'm' | 'f', from glosses stating a gender. Empty when
    the file is absent (installed package without the sources tree)."""
    path = Path(path)
    if not path.exists():
        return {}
    _, rows = _read_rows(path)
    names: dict[str, str] = {}
    for row in rows:
        m = _NAME_GLOSS_RE.search(row.get("gloss", ""))
        if m and row.get("orthography"):
            names.setdefault(row["orthography"].lower(), m.group(1))
    return names


def _word(entry: Entry, rf: RuleFile, table: FeatureTable) -> Word | None:
    """The entry's `ipa` after the `[normalize]` rewrites (aliases folded, unmarked consonants
    given a quality), so that `_final_quality` sees BROAD/SLEN members and the inferred
    `gen_ipa` is canonical. Only the rewrites: no stress is added (that is `normalize()`)."""
    if not entry.ipa:
        return None
    return _normalize_rewrites(Word.from_tokenized(tokenize(entry.ipa, table)), rf, table)


def _final(word: Word | None) -> str | None:
    return word.segments[-1] if word is not None and word.segments else None


def _orth_slender_final(orth: str) -> bool | None:
    """Orthographic fallback when no IPA: True/False for a consonant-final word by the quality
    of its last vowel letter, None when vowel-final or vowel-less."""
    if not orth or orth[-1] in _VOWEL_LETTERS:
        return None
    vowels = [ch for ch in orth if ch in _VOWEL_LETTERS]
    if not vowels:
        return None
    return vowels[-1] in _SLENDER_LETTERS


def _final_quality(entry: Entry, word: Word | None, rf: RuleFile, table: FeatureTable) -> str | None:
    """'broad' | 'slender' for a consonant-final word, 'vowel' when vowel-final, None unknown."""
    seg = _final(word)
    if seg is not None:
        if table.value(seg, "syllabic") == "+":
            return "vowel"
        if seg in rf.classes.get("SLEN", ()):
            return "slender"
        if seg in rf.classes.get("BROAD", ()):
            return "broad"
        return None
    orth = entry.orthography.lower()
    if orth and orth[-1] in _VOWEL_LETTERS:
        return "vowel"
    s = _orth_slender_final(orth)
    return None if s is None else ("slender" if s else "broad")


def _infer_gender(entry: Entry, quality: str | None) -> tuple[str, str]:
    orth = entry.orthography.lower()
    if orth in known_names():
        return known_names()[orth], "gender:known-name"
    if orth.endswith(_MASC_ENDINGS):
        return "m", "gender:ending"
    if orth.endswith(_FEM_ENDINGS) or quality == "slender":
        return "f", "gender:ending"
    return "m", "gender:default-m"


def _infer_declension(entry: Entry, gender: str, quality: str | None) -> tuple[str, str]:
    orth = entry.orthography.lower()
    if orth.endswith("ach"):
        return "ach", "declension:inferred-ach"
    if orth.endswith(_M3_ENDINGS):
        return "m3", "declension:inferred-m3"
    if quality == "vowel" or orth.endswith("ín"):
        return "d4", "declension:inferred-d4"
    if gender == "m" and quality == "broad":
        return "m1", "declension:inferred-m1"
    if gender == "f" and quality in ("broad", "slender"):
        return "f2", "declension:inferred-f2"
    return _DEFAULT_DECLENSION, "declension:default-m1"


def infer(entry: Entry, irish: RuleFile, table: FeatureTable) -> Entry:
    """Fill dialect, gender, declension and gen_ipa where missing (module docstring)."""
    tags: list[str] = list(entry.assumptions)
    if not entry.ipa and "skipped:no-ipa" not in tags:
        tags.append("skipped:no-ipa")
    word = _word(entry, irish, table)
    quality = _final_quality(entry, word, irish, table)

    dialect = entry.dialect
    if not dialect:
        dialect, tag = "C", "dialect:default-C"
        tags.append(tag)

    gender = entry.gender
    if not gender:
        gender, tag = _infer_gender(entry, quality)
        tags.append(tag)

    declension = entry.declension
    if declension in ("", _DEFAULT_DECLENSION) and not any(
            t.startswith("declension:") for t in tags):
        declension, tag = _infer_declension(entry, gender, quality)
        tags.append(tag)

    gen_ipa = entry.gen_ipa
    if not gen_ipa and word is not None:
        if declension == "d4":
            gen_ipa = word.ipa(marks=False)
        else:
            gen_ipa = apply_inflection(word, f"GEN_{declension.upper()}", irish, table).ipa(marks=False)
        tags.append(f"gen_ipa:inferred-{declension}")

    return replace(entry, dialect=dialect, gender=gender, declension=declension,
                   gen_ipa=gen_ipa, assumptions=tuple(tags))


def _field_of(tag: str) -> str:
    return tag.split(":", 1)[0]


def lint_report(entries: Sequence[Entry]) -> list[str]:
    """One line per guess: `<orthography>\\t<field> = <value>\\t<tag>` (`skipped:no-ipa`
    lines carry no value)."""
    lines: list[str] = []
    for e in entries:
        for tag in e.assumptions:
            field_name = _field_of(tag)
            if field_name == "skipped":
                lines.append(f"{e.orthography}\t{tag}")
            else:
                lines.append(f"{e.orthography}\t{field_name} = {getattr(e, field_name, '')}\t{tag}")
    return lines


def accept_guesses(path: str | Path, entries: Sequence[Entry]) -> None:
    """`strands lint --accept`: write the inferred dialect / gender / gen_ipa into the TSV.
    Rows pair with `entries` by order (blank rows are skipped, as `read_input` does);
    existing columns — spec or not — are kept in place, and a missing spec column is
    appended to the header. Only empty cells are filled; nothing supplied is changed.
    `declension` is not a spec §5 column and is not written."""
    path = Path(path)
    header, rows = _read_rows(path)
    data_rows = [r for r in rows if r.get("orthography")]
    if len(data_rows) != len(entries):
        raise InputError(f"{path}: {len(data_rows)} rows but {len(entries)} entries")
    for col in _INFERRED_COLUMNS:
        if col not in header:
            header.append(col)
    for row, entry in zip(data_rows, entries):
        if row.get("orthography") != entry.orthography:
            raise InputError(f"{path}: row {row.get('orthography')!r} does not match entry "
                             f"{entry.orthography!r}")
        for col in _INFERRED_COLUMNS:
            if not row.get(col):
                row[col] = getattr(entry, col)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=header, delimiter="\t", extrasaction="ignore",
                                lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({h: row.get(h, "") for h in header})
