"""Regression harness over `sources/<target>/attested.tsv` (plan Task 22; spec §8 layer 3 as
re-scoped by I-25).

Two modes, decided per row:

- **Mode E (end-to-end)** — the row carries BOTH `source_ipa` and `target_ipa` (Dutch only,
  32 rows). The source form runs through stages 2–7 (`pipeline.adapt`) and the output is
  compared to the attested target IPA.
- **Mode C (conformance)** — the row carries `target_ipa` only. **Mode C tests inventory,
  phonotactics and stress conformance ONLY**: every segment of the attested form must be in
  the rule file's `[inventory]` (marginals included, I-23), the form must syllabify with no
  illegal span and no `bans` violation, and where the row records a primary stress mark the
  file's stress procedure must reproduce it. A Mode C pass says NOTHING about substitution,
  repair, post-stress, affixation or respell — those are covered by the per-target repair
  tables (I-27).

Other buckets: `skip` (no `target_ipa`), `error` (still untokenizable after the I-36
cleaning pass; `reason` names the substring). Attested data never raises (I-24): a
`SegmentError` is counted, not propagated. Engine errors caused by the RULE FILE (a
`StressError`, an unreachable feature change) are bugs and do propagate.

"Pass" (I-22) is exact string equality after NFC, after `clean_attested`, and after stripping
from the engine output the marks (`.`, `ˈ`) the attested row does not itself carry. Secondary
stress `ˌ` is dropped from the attested string too (I-40: the engine never emits it).
`distance` is a segment-level Levenshtein distance in Mode E; in Mode C it counts the
offending segments (off-inventory + illegal) plus one for a stress mismatch.

Ratchet: `tests/ratchets/<target>.json` holds `{"C": rate, "E": rate}` for the modes that have
rows; `assert_ratchet` fails loudly when a rate drops below it. `write_ratchet` is run by
hand after a target's bar is met — never by a test.
"""

from __future__ import annotations

import csv
import json
import math
import unicodedata
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

from .dsl import RuleFile, parse_rules_file
from .features import FeatureTable
from .pipeline import adapt
from .stress import assign_stress
from .syllabify import syllabify
from .tokenize import SegmentError, clean_attested, tokenize
from .word import Word

__all__ = [
    "RegressionRow",
    "RegressionReport",
    "MODES",
    "PREDICTED_PREFIX",
    "RATCHET_DIR",
    "read_attested",
    "run_regression",
    "edit_distance",
    "load_ratchet",
    "assert_ratchet",
    "write_ratchet",
]

_ROOT = Path(__file__).resolve().parents[2]
SOURCES_DIR = _ROOT / "sources"
RULES_DIR = _ROOT / "rules"
RATCHET_DIR = _ROOT / "tests" / "ratchets"
MODES = ("E", "C", "skip", "error")
PREDICTED_PREFIX = "PREDICTED-NOT-ATTESTED:"
_CONFORMANCE_NOTE = (
    "Mode C = inventory/syllable/stress conformance only; it says nothing "
    "about substitution, repair, post-stress, affixation or respell (I-25)."
)


@dataclass(frozen=True)
class RegressionRow:
    source_form: str
    source_ipa: str
    target_form: str
    target_ipa: str
    provenance: str
    mode: str  # "E" | "C" | "skip" | "error"
    passed: bool
    got: str
    distance: int
    reason: str = ""  # for mode="error": the untokenizable substring


@dataclass(frozen=True)
class RegressionReport:
    target: str
    rows: tuple[RegressionRow, ...]

    def counts(self) -> dict[str, int]:
        """Row counts by mode; every mode in MODES is present (zero when empty)."""
        out = {m: 0 for m in MODES}
        for r in self.rows:
            out[r.mode] = out.get(r.mode, 0) + 1
        return out

    def rate(self, mode: str) -> float:
        """passed / rows in `mode`; 0.0 when the mode has no rows."""
        rows = [r for r in self.rows if r.mode == mode]
        if not rows:
            return 0.0
        return sum(1 for r in rows if r.passed) / len(rows)

    def mode_e_is_empty(self) -> bool:
        """True when no row carries both IPA sides (every target but Dutch, I-25)."""
        return not any(r.mode == "E" for r in self.rows)

    def summary(self) -> str:
        c = self.counts()
        lines = [
            f"regression {self.target}: {len(self.rows)} rows — "
            f"E {c['E']}, C {c['C']}, skip {c['skip']}, error {c['error']}"
        ]
        for mode in ("E", "C"):
            n = c[mode]
            if n:
                passed = sum(1 for r in self.rows if r.mode == mode and r.passed)
                lines.append(f"  Mode {mode}: {passed}/{n} passed = {self.rate(mode):.3f}")
            else:
                lines.append(f"  Mode {mode}: no rows")
        lines.append("  " + _CONFORMANCE_NOTE)
        return "\n".join(lines)


# ---- data ----------------------------------------------------------------------------------


def read_attested(target: str) -> list[dict[str, str]]:
    """Rows of sources/<target>/attested.tsv, NFC-normalized (I-1). Drops rows whose `note`
    starts with 'PREDICTED-NOT-ATTESTED:' (the 11 Cairene predictions)."""
    path = SOURCES_DIR / target / "attested.tsv"
    out: list[dict[str, str]] = []
    with path.open(encoding="utf-8", newline="") as fh:
        for raw in csv.DictReader(fh, delimiter="\t"):
            row = {k: unicodedata.normalize("NFC", v or "") for k, v in raw.items() if k}
            if row.get("note", "").startswith(PREDICTED_PREFIX):
                continue
            out.append(row)
    return out


# ---- comparison helpers ----------------------------------------------------------------------


def edit_distance(a: Sequence[str], b: Sequence[str]) -> int:
    """Levenshtein distance over two segment sequences."""
    prev = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        cur = [i]
        for j, y in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (x != y)))
        prev = cur
    return prev[-1]


def _strip(text: str, marks: str) -> str:
    for m in marks:
        text = text.replace(m, "")
    return text


def _comparable(got: str, attested: str) -> tuple[str, str]:
    """Strip from `got` the marks the attested row does not carry (I-22); drop ˌ from both."""
    attested = attested.replace("ˌ", "")
    got = got.replace("ˌ", "")
    for mark in ".ˈ":
        if mark not in attested:
            got = got.replace(mark, "")
    return got, attested


def _words(text: str, table: FeatureTable) -> list[Word]:
    """One Word per space-separated word (SegmentError propagates to the caller)."""
    return [Word.from_tokenized(tokenize(piece, table)) for piece in text.split()]


def _segments(text: str, table: FeatureTable) -> tuple[str, ...]:
    """Segment sequence of a multi-word string, with " " between words, marks dropped."""
    out: list[str] = []
    for i, piece in enumerate(text.split()):
        if i:
            out.append(" ")
        out.extend(tokenize(piece, table).segments)
    return tuple(out)


def _reason(exc: SegmentError) -> str:
    """The untokenizable substring named by the tokenizer's message."""
    msg = str(exc)
    if msg.startswith("unknown segment "):
        head = msg[len("unknown segment ") :]
        return head.split(" at position ")[0].strip("'")
    return msg


# ---- one row ----------------------------------------------------------------------------------


def _mode_c(word: Word, attested: str, rf: RuleFile, table: FeatureTable) -> tuple[bool, str, int]:
    """Inventory ∧ legal syllabification ∧ (stress reproduced, when the row marks it)."""
    allowed = set(rf.inventory)
    off = [s for s in word.segments if s not in allowed]
    parsed = syllabify(word, rf, table)
    attested_stress = parsed.stress  # from the row's ˈ, if any (S1)
    stressed = assign_stress(parsed, rf, table)
    mismatch = 0
    if "ˈ" in attested and stressed.stress != attested_stress:
        mismatch = 1
    distance = len(off) + len(parsed.illegal) + mismatch
    got, _ = _comparable(stressed.ipa(marks=True), attested)
    return distance == 0, got, distance


def _run_row(row: dict[str, str], target: str, rf: RuleFile, table: FeatureTable) -> RegressionRow:
    base = dict(
        source_form=row.get("source_form", ""),
        source_ipa=row.get("source_ipa", ""),
        target_form=row.get("target_form", ""),
        target_ipa=row.get("target_ipa", ""),
        provenance=row.get("provenance", ""),
    )
    if not base["target_ipa"].strip():
        return RegressionRow(**base, mode="skip", passed=False, got="", distance=0)
    attested = clean_attested(base["target_ipa"], target)
    try:
        target_words = _words(attested, table)
    except SegmentError as exc:
        return RegressionRow(
            **base, mode="error", passed=False, got="", distance=0, reason=_reason(exc)
        )
    if not target_words:
        return RegressionRow(**base, mode="skip", passed=False, got="", distance=0)

    if base["source_ipa"].strip():
        source = clean_attested(base["source_ipa"], target)
        try:
            source_words = _words(source, table)
        except SegmentError as exc:
            return RegressionRow(
                **base, mode="error", passed=False, got="", distance=0, reason=_reason(exc)
            )
        result = adapt(source_words, rf, table)
        got, want = _comparable(result.ipa, attested)
        distance = edit_distance(_segments(got, table), _segments(want, table))
        return RegressionRow(**base, mode="E", passed=(got == want), got=got, distance=distance)

    # Mode C: conformance of the attested target form, word by word.
    passed = True
    gots: list[str] = []
    distance = 0
    pieces = attested.split()
    for word, piece in zip(target_words, pieces):
        ok, got, d = _mode_c(word, piece, rf, table)
        passed = passed and ok
        gots.append(got)
        distance += d
    return RegressionRow(**base, mode="C", passed=passed, got=" ".join(gots), distance=distance)


# ---- the run ----------------------------------------------------------------------------------


def run_regression(
    target: str, table: FeatureTable, rule_file: Path | None = None
) -> RegressionReport:
    """Run every attested row of `target` in its mode (E when both IPA sides exist, else C).
    `rule_file` overrides rules/<target>.rules so the harness can be tested against the toy
    fixture before any real target file exists (R28). Mode C is inventory/syllable/stress
    conformance only — see the module docstring."""
    path = Path(rule_file) if rule_file is not None else RULES_DIR / f"{target}.rules"
    rf = parse_rules_file(path, table)
    rows = tuple(_run_row(row, target, rf, table) for row in read_attested(target))
    return RegressionReport(target=target, rows=rows)


# ---- ratchet ----------------------------------------------------------------------------------


def load_ratchet(target: str) -> dict[str, float]:
    """tests/ratchets/<target>.json as {mode: rate}; {} when absent."""
    path = RATCHET_DIR / f"{target}.json"
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return {str(k): float(v) for k, v in data.items()}


def assert_ratchet(report: RegressionReport, tolerance: float = 0.0) -> None:
    """AssertionError when any recorded mode's rate has dropped by more than `tolerance`."""
    ratchet = load_ratchet(report.target)
    failures = []
    for mode, floor in sorted(ratchet.items()):
        rate = report.rate(mode)
        if rate + tolerance < floor - 1e-9:
            failures.append(f"Mode {mode}: {rate:.4f} < ratchet {floor:.4f}")
    if failures:
        raise AssertionError(
            f"regression ratchet slipped for {report.target}: "
            + "; ".join(failures)
            + "\n"
            + report.summary()
        )


def _floor4(rate: float) -> float:
    """Truncate to four decimals. Never rounds UP: a 2/3 report saved as 0.6667 would fail its
    own assert_ratchet (0.6666… < 0.6667); 0.6666 cannot create a regression."""
    return math.floor(rate * 10_000) / 10_000


def write_ratchet(report: RegressionReport) -> None:
    """Record the current rates (floored to 4 decimals) for the modes that have rows.
    Run by hand, never by a test."""
    counts = report.counts()
    data = {mode: _floor4(report.rate(mode)) for mode in ("E", "C") if counts.get(mode)}
    RATCHET_DIR.mkdir(parents=True, exist_ok=True)
    (RATCHET_DIR / f"{report.target}.json").write_text(
        json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
