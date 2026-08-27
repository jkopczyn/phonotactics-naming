"""Repair loop and `cluster-fallback`.

Plan Task 11; spec §12.A (which overrides §4.4) and §12.E.

`repair()` — one PASS applies every `[repair]` rule in file order, UNCONDITIONALLY: many of
these rules are active processes (Dutch final devoicing, Welsh fortition/prothesis), not fixes
for illegal parses, so they fire whether or not anything is marked illegal. After any rule that
changes the word — count-preserving or not — the word is re-syllabified, so later rules in the
same pass see fresh syllable boundaries and illegal marks. At the end of each pass, when
illegal marks remain, the file's `cluster-fallback` directive runs: `same-length` substitutes
(`cluster_fallback()`, then a re-syllabification if anything changed), `keep` leaves the
cluster alone (`cluster_keep()`, and NO re-syllabification — it clears the marks itself).

A further pass runs only while illegal marks remain AND the previous pass changed the segment
string. Cycle detection is on the segment string: every string seen at a pass boundary is
remembered, and a pass whose result has been seen before (its own starting string included)
ends the loop, so `a -> b` / `b -> a` stops after one pass rather than ten. The loop is capped
at `MAX_REPAIR_PASSES`. If illegal marks are still present when the loop ends, the word is
flagged `UNREPAIRED`; the marks are left in place for the caller.

Trace entries: each changed rule records `stage="repair"`, `rule_id="repair:<line>"` (I-21)
and the rule's own tag. Each re-syllabification records the syllabifier's own entry. Each
cluster replacement records `stage="repair"`, `rule_id="cluster-fallback"`, `tag="fallback"`,
so `Word.fallback_count()` counts it.

`cluster_fallback()` — spec §12.E. Every maximal run of illegal segments is split at any
syllable start inside it (the syllabifier places one boundary inside an unparseable
interlude). A piece that ends at a nucleus start is an ONSET span; otherwise a piece that
starts at a nucleus stop is a CODA span; any other piece (a nucleus-less domain, a ban over
vowels, a required-but-missing onset) is left alone. The span is replaced by the attested
cluster of the SAME LENGTH from the file's `onsets` / `codas` list minimising the summed
per-position segment feature distance under the file's `[weights]` (I-12); ties break by list
order (first wins). `onsets = any` / `codas = any` offer no candidates. A span with no
same-length candidate is left marked; the caller (`repair`) then flags `UNREPAIRED`.

`cluster_keep()` — `cluster-fallback = keep` (owner decision 2026-08-25 for Georgian; digest
§3.7: Georgian imports foreign clusters intact and does not repair them). The same onset/coda
spans are found, but nothing is replaced: the marks are cleared so the loop terminates without
`UNREPAIRED`, each span records `repair cluster-keep %design` and adds an
`UNATTESTED_CLUSTER:<cluster>` flag, and the fallback count does not move.
"""
from __future__ import annotations

from collections.abc import Sequence
from dataclasses import replace

from .dsl import RuleFile
from .features import FeatureTable
from .rewrite import apply_rule
from .syllabify import legal_onset, syllabify
from .word import TraceEntry, Word

__all__ = ["MAX_REPAIR_PASSES", "UNREPAIRED", "UNATTESTED_CLUSTER", "repair",
           "cluster_fallback", "cluster_keep", "overlay_undo"]

MAX_REPAIR_PASSES = 10
UNREPAIRED = "UNREPAIRED"
UNATTESTED_CLUSTER = "UNATTESTED_CLUSTER"
STAGE = "repair"
CLUSTER_FALLBACK = "cluster-fallback"
CLUSTER_KEEP = "cluster-keep"
OVERLAY_UNDO = "overlay-undo"
SUBSTITUTE = "substitute:"
SAME_LENGTH = "same-length"
KEEP = "keep"
KEEP_NOTE = ("unattested cluster kept (Georgian imports foreign clusters intact; digest §3.7)")


# ---- cluster fallback (§12.E) -------------------------------------------------------------------

def _illegal_runs(word: Word) -> list[tuple[int, int]]:
    """Maximal contiguous illegal spans, split at syllable starts, as (start, stop)."""
    marked = sorted(word.illegal)
    if not marked:
        return []
    runs: list[tuple[int, int]] = []
    start = prev = marked[0]
    for i in marked[1:]:
        if i != prev + 1:
            runs.append((start, prev + 1))
            start = i
        prev = i
    runs.append((start, prev + 1))
    inner = set(word.syllables)
    pieces: list[tuple[int, int]] = []
    for a, b in runs:
        cut = a
        for s in sorted(inner):
            if a < s < b:
                pieces.append((cut, s))
                cut = s
        pieces.append((cut, b))
    return pieces


def _span_role(word: Word, a: int, b: int) -> str | None:
    """"onset" if the span ends at a nucleus start, "coda" if it starts at a nucleus stop."""
    if any(a_n == b for a_n, _ in word.nuclei):
        return "onset"
    if any(b_n == a for _, b_n in word.nuclei):
        return "coda"
    return None


def _best_cluster(span: Sequence[str], candidates: Sequence[tuple[str, ...]],
                  rf: RuleFile, table: FeatureTable) -> tuple[str, ...] | None:
    best: tuple[str, ...] | None = None
    best_d = 0.0
    for cand in candidates:
        if len(cand) != len(span):
            continue
        d = sum(table.distance(x, y, rf.weights) for x, y in zip(span, cand))
        if best is None or d < best_d:
            best, best_d = cand, d
    return best


def cluster_fallback(word: Word, rf: RuleFile, table: FeatureTable) -> Word:
    """Spec §12.E: when rf.cluster_fallback == 'same-length', replace an illegal onset or
    coda span with the attested cluster of the SAME LENGTH minimising summed segment
    feature distance (ties: list order), tagged %fallback. No candidate -> leave the
    marks and let the caller flag UNREPAIRED. Runs at the end of each repair pass.
    Does not re-syllabify; the returned word's marks are stale wherever it changed."""
    if rf.cluster_fallback != SAME_LENGTH or not word.illegal or rf.syllable is None:
        return word
    spec = rf.syllable
    edits: list[tuple[int, int, tuple[str, ...]]] = []
    for a, b in _illegal_runs(word):
        role = _span_role(word, a, b)
        if role is None:
            continue
        candidates = spec.onsets if role == "onset" else spec.codas
        if not candidates:
            continue
        span = word.segments[a:b]
        best = _best_cluster(span, candidates, rf, table)
        if best is None or best == span:
            continue
        edits.append((a, b, best))
    out = word
    for a, b, new in reversed(edits):             # right-to-left keeps earlier indices valid
        before = out.ipa()
        old = "".join(out.segments[a:b])
        out = out.replaced(a, b, new)
        out = out.traced(TraceEntry(stage=STAGE, rule_id=CLUSTER_FALLBACK, tag="fallback",
                                    before=before, after=out.ipa(),
                                    note=f"{old} -> {''.join(new)}"))
    return out


def cluster_keep(word: Word, rf: RuleFile, table: FeatureTable) -> Word:
    """`cluster-fallback = keep` (owner decision 2026-08-25; digest §3.7): an illegal onset or
    coda span is LEFT AS IT IS. Its illegal marks are cleared, so the repair loop terminates
    normally instead of flagging UNREPAIRED, and each kept span records a
    `repair cluster-keep %design` trace entry and an `UNATTESTED_CLUSTER:<cluster>` flag.
    Nothing is substituted, so no `%fallback` entry is made and the fallback count is unmoved.

    A span that is neither an onset nor a coda (a nucleus-less domain, a ban over vowels, a
    required-but-missing onset) is NOT kept: its marks stay and the caller flags UNREPAIRED,
    exactly as under `same-length`. The word's segments never change, so the caller must not
    re-syllabify afterwards — that would put the cleared marks straight back."""
    if rf.cluster_fallback != KEEP or not word.illegal or rf.syllable is None:
        return word
    kept: list[tuple[int, int]] = []
    for a, b in _illegal_runs(word):
        if _span_role(word, a, b) is None:
            continue
        kept.append((a, b))
    if not kept:
        return word
    out = word
    cleared = set(out.illegal)
    for a, b in kept:
        cluster = "".join(out.segments[a:b])
        here = out.ipa()
        out = out.traced(TraceEntry(stage=STAGE, rule_id=CLUSTER_KEEP, tag="design",
                                    before=here, after=here,
                                    note=f"{cluster}: {KEEP_NOTE}"))
        out = out.with_flag(f"{UNATTESTED_CLUSTER}:{cluster}")
        cleared -= set(range(a, b))
    return replace(out, illegal=frozenset(cleared))



def overlay_undo(word: Word, rf: RuleFile, table: FeatureTable) -> Word:
    """`[repair] overlay-undo = <segment>` (owner decision 2026-08-25, Georgian Cʷ).

    The target's secondary-articulation overlay is written as an epenthesis in `[substitute]`
    (Georgian: `0 -> v / [BROAD -labial] _ [V +front]`). When that insertion is what makes an
    onset unlicensed, the overlay is undone rather than the word repaired: the inserted segment
    is deleted, the onset is rechecked, and the edit is kept only if the onset is now legal.
    Otherwise the segment stays and the caller falls through to `cluster_keep()` — the overlay
    is preferred to a substitution.

    Provenance comes from `Word.origins`, which `apply_rule` fills for insertion rules only, so
    a `v` the input itself contained is never touched. Only `substitute`-stage insertions count
    (the overlay stage); a `[repair]` epenthesis is the repair loop's own work.
    Does not re-syllabify; the caller does when the word changed."""
    seg = rf.overlay_undo
    if seg is None or not word.illegal or rf.syllable is None:
        return word
    edits: list[int] = []
    for a, b in _illegal_runs(word):
        if _span_role(word, a, b) != "onset":
            continue
        overlay = sorted((i for i, rule_id in word.origins
                          if a <= i < b and word.segments[i] == seg
                          and rule_id.startswith(SUBSTITUTE)), reverse=True)
        for i in overlay:
            trial = word.segments[a:i] + word.segments[i + 1:b]
            if legal_onset(trial, rf.syllable, table):
                edits.append(i)
                break
    out = word
    for i in sorted(edits, reverse=True):          # right-to-left keeps earlier indices valid
        before = out.ipa()
        out = out.replaced(i, i + 1, ())
        out = out.traced(TraceEntry(stage=STAGE, rule_id=OVERLAY_UNDO, tag="design",
                                    before=before, after=out.ipa(),
                                    note=f"overlay {seg} undone: the cluster it created is "
                                         "not licensed"))
    return out


# ---- the loop (§12.A) ---------------------------------------------------------------------------

def repair(word: Word, rf: RuleFile, table: FeatureTable) -> Word:
    """Spec §12.A:
       pass = apply every [repair] rule in file order, UNCONDITIONALLY (many are active
       processes, not fixes: Dutch final devoicing, Welsh fortition/prothesis);
       re-syllabify after any rule that changed the word, count-preserving or not;
       run a further pass only while illegal marks remain AND the previous pass changed
       the segment string (cycle detection on the string); cap MAX_REPAIR_PASSES;
       then flag UNREPAIRED.
    The input is expected to be syllabified already (its `illegal` marks are trusted)."""
    rules = rf.sections.get(STAGE, ())
    seen: set[tuple[str, ...]] = {word.segments}
    for _ in range(MAX_REPAIR_PASSES):
        for rule in rules:
            new = apply_rule(word, rule, rf, table, STAGE)
            if new is not word:
                word = syllabify(new, rf, table)
        if word.illegal and rf.overlay_undo is not None:
            new = overlay_undo(word, rf, table)
            if new is not word:
                word = syllabify(new, rf, table)
        if word.illegal and rf.cluster_fallback == SAME_LENGTH:
            new = cluster_fallback(word, rf, table)
            if new is not word:
                word = syllabify(new, rf, table)
        elif word.illegal and rf.cluster_fallback == KEEP:
            word = cluster_keep(word, rf, table)   # no re-syllabify: it would re-mark the span
        if not word.illegal:
            return word
        if word.segments in seen:                   # unchanged, or a longer cycle
            break
        seen.add(word.segments)
    return word.with_flag(UNREPAIRED)
