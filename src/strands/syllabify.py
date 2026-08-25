"""Nucleus-aware syllabifier: nuclei grouping, cluster legality, illegal-span marking.

Plan Task 10; spec §3 `[syllable]` (legality = template ∧ onset-set ∧ coda-set ∧ sonority ∧
¬banned; maximal onset subject to legality; on failure mark the minimal illegal span rather
than raising), §12.B (diphthongs are two segments but one nucleus when `nuclei` licenses the
pair; Georgian declares none and gets hiatus), §12.D (`onsets`/`codas` are COMPLETE sets
including singletons; the empty onset/coda is always allowed unless `onset-required = yes`).
Interpretations: I-2 (nuclei), I-13 (sonority scale, below), I-14 (bans mark their span),
S1 (`Word._pending_stress` is a segment index; this stage converts it to a syllable index).

Sonority scale (I-13), fixed in code and used only when `sonority = on`:

    vowel 5 > glide 4 > liquid 3 > nasal 2 > fricative 1 > stop/affricate 0

Onsets must rise strictly, codas fall strictly; a cluster whose outermost segment is a
coronal sibilant (`sC` onsets, `Cs` codas) is exempt for that segment only — the remainder
still has to be well-ordered. Classes are computed from features (I-11): glide = syllabic-
sonorant+ consonantal-; liquid = the LIQ definition; nasal = nasal+; fricative = continuant+
sonorant- (so `/h/` counts as a fricative); everything else non-syllabic is 0.

Algorithm (plan Task 10):
1. Domains: `domain = word` is the whole word; `domain = stem` splits at the `$` positions.
2. `group_nuclei` over each domain; a domain with no nucleus is illegal in full.
3. Interludes: the longest suffix that is a legal onset whose remainder is a legal coda;
   back off one segment at a time. If no split works, the whole interlude is marked illegal
   and the boundary goes before the segment of minimum sonority (ties: rightmost, keeping
   the maximal-onset spirit).
4. Domain-initial consonants must be a legal onset (empty is fine unless
   `onset-required = yes`, in which case the first nucleus segment is marked — as is the
   first segment of ANY later nucleus whose interlude leaves it no onset, e.g. hiatus); word-final
   consonants must be a legal coda, optionally followed by up to `len(appendix)` appendix
   segments (word-final only, never at a stem edge). An illegal edge cluster is marked whole.
5. Legality = template ∧ onset-set ∧ coda-set ∧ sonority ∧ ¬banned, skipping `any`/`off`
   components. The template contributes only its slot COUNTS (maximum onset and coda
   length); a non-optional edge slot does not make the empty cluster illegal (§12.D wins).
6. `bans` are matched over the syllabified word after the parse; in `stem` domain a matched
   span may not straddle a `$`. The matched segments are marked illegal.

Marks are recomputed from scratch on every call (earlier `illegal` and `.` boundaries are
discarded), so the function is idempotent and safe to call after every repair rule. A
`RuleError` from a ban that names an undeclared class is a rule-file bug and propagates;
nothing about the WORD ever raises.
"""
from __future__ import annotations

from dataclasses import replace
from typing import Sequence

from .dsl import CtxItem, RuleFile, SyllableSpec
from .features import FeatureTable
from .rewrite import _boundary, match_item
from .word import TraceEntry, Word

__all__ = ["SONORITY_DOC", "sonority", "group_nuclei", "legal_onset", "legal_coda", "syllabify"]

SONORITY_DOC: str = __doc__

_STAGE = "syllabify"
_RULE_ID = "syllable"


# ---- sonority (I-13) ------------------------------------------------------------------------

def sonority(segment: str, table: FeatureTable) -> int:
    v = table.value
    if v(segment, "syllabic") == "+":
        return 5
    if v(segment, "sonorant") == "+" and v(segment, "consonantal") == "-":
        return 4
    if (v(segment, "consonantal") == "+" and v(segment, "sonorant") == "+"
            and v(segment, "coronal") == "+"
            and "+" in (v(segment, "lateral"), v(segment, "tap"), v(segment, "trill"))):
        return 3
    if v(segment, "nasal") == "+":
        return 2
    if v(segment, "continuant") == "+" and v(segment, "sonorant") == "-":
        return 1
    return 0


def _is_vowel(segment: str, table: FeatureTable) -> bool:
    return table.value(segment, "syllabic") == "+"


def _is_sibilant(segment: str, table: FeatureTable) -> bool:
    v = table.value
    return (v(segment, "coronal") == "+" and v(segment, "strident") == "+"
            and v(segment, "continuant") == "+" and v(segment, "sonorant") == "-")


def _strictly(values: Sequence[int], rising: bool) -> bool:
    return all((b > a) if rising else (b < a) for a, b in zip(values, values[1:]))


def _sonority_ok(cluster: tuple[str, ...], table: FeatureTable, *, onset: bool) -> bool:
    if len(cluster) < 2:
        return True
    core = cluster
    if onset and _is_sibilant(cluster[0], table):
        core = cluster[1:]
    elif not onset and _is_sibilant(cluster[-1], table):
        core = cluster[:-1]
    return _strictly([sonority(s, table) for s in core], rising=onset)


# ---- nuclei (§12.B) -------------------------------------------------------------------------

def group_nuclei(segments: Sequence[str], spec: SyllableSpec,
                 table: FeatureTable) -> list[tuple[int, int]]:
    """Spec §12.B: maximal vowel runs are split into nuclei; a sequence listed in
    spec.nuclei is ONE nucleus (longest licensed sequence first); otherwise each vowel is
    its own nucleus (hiatus). Returns half-open (start, stop) spans in order."""
    licensed = sorted(spec.nuclei, key=len, reverse=True)
    out: list[tuple[int, int]] = []
    i, n = 0, len(segments)
    while i < n:
        if not _is_vowel(segments[i], table):
            i += 1
            continue
        width = 1
        for nuc in licensed:
            k = len(nuc)
            if (i + k <= n and tuple(segments[i:i + k]) == nuc
                    and all(_is_vowel(s, table) for s in nuc)):
                width = k
                break
        out.append((i, i + width))
        i += width
    return out


# ---- cluster legality (§3, §12.D) ---------------------------------------------------------------

def _template_limits(spec: SyllableSpec) -> tuple[int | None, int | None]:
    """(max onset length, max coda length) from the template's slot counts; None = any."""
    if spec.template is None:
        return None, None
    slots = [slot for slot, _ in spec.template]
    for k, slot in enumerate(slots):
        if slot in ("N", "V"):
            return k, len(slots) - k - 1
    return None, None


def legal_onset(cluster: tuple[str, ...], spec: SyllableSpec, table: FeatureTable) -> bool:
    cluster = tuple(cluster)
    if not cluster:
        return True                                   # §12.D; onset-required is checked by the caller
    limit, _ = _template_limits(spec)
    if limit is not None and len(cluster) > limit:
        return False
    if spec.onset_set is not None and cluster not in spec.onset_set:
        return False
    if spec.sonority and not _sonority_ok(cluster, table, onset=True):
        return False
    return True


def legal_coda(cluster: tuple[str, ...], spec: SyllableSpec, table: FeatureTable) -> bool:
    cluster = tuple(cluster)
    if not cluster:
        return True
    _, limit = _template_limits(spec)
    if limit is not None and len(cluster) > limit:
        return False
    if spec.coda_set is not None and cluster not in spec.coda_set:
        return False
    if spec.sonority and not _sonority_ok(cluster, table, onset=False):
        return False
    return True


def _legal_final_coda(cluster: tuple[str, ...], spec: SyllableSpec, table: FeatureTable,
                      *, word_final: bool) -> bool:
    """A coda, optionally followed (word-finally only) by up to len(appendix) appendix
    segments."""
    if legal_coda(cluster, spec, table):
        return True
    if not word_final or not spec.appendix:
        return False
    allowed = set(spec.appendix)
    for k in range(1, min(len(spec.appendix), len(cluster)) + 1):
        tail = cluster[len(cluster) - k:]
        if all(s in allowed for s in tail) and legal_coda(cluster[:len(cluster) - k], spec, table):
            return True
    return False


# ---- bans (I-14) ---------------------------------------------------------------------------------

def _ban_end(items: Sequence[CtxItem], k: int, pos: int, word: Word, rf: RuleFile,
             table: FeatureTable) -> int | None:
    """Longest end position of a match of items[k:] starting at boundary `pos`, or None."""
    if k == len(items):
        return pos
    item = items[k]
    atom = item.atom
    if isinstance(atom, str):
        if not _boundary(atom, pos, word):
            return None
        return _ban_end(items, k + 1, pos, word, rf, table)
    n = len(word.segments)
    limit = n - pos if item.star else 1
    count = 0
    while count < limit and pos + count < n and match_item(atom, word.segments[pos + count], rf, table):
        count += 1
    minimum = 0 if (item.star or item.optional) else 1
    while count >= minimum:
        end = _ban_end(items, k + 1, pos + count, word, rf, table)
        if end is not None:
            return end
        count -= 1
    return None


def _banned_spans(word: Word, rf: RuleFile, table: FeatureTable,
                  inner_boundaries: frozenset[int]) -> set[int]:
    spec = rf.syllable
    assert spec is not None
    marked: set[int] = set()
    n = len(word.segments)
    for ban in spec.bans:
        for start in range(n + 1):
            end = _ban_end(ban, 0, start, word, rf, table)
            if end is None or end <= start:
                continue
            if any(start < b < end for b in inner_boundaries):
                continue                              # stem domain: a ban never straddles `$`
            marked.update(range(start, end))
    return marked


# ---- the parse -----------------------------------------------------------------------------------

def _split_interlude(cluster: tuple[str, ...], spec: SyllableSpec, table: FeatureTable
                     ) -> tuple[int, bool]:
    """(onset start offset within the interlude, legal?). Maximal onset subject to legality;
    when nothing works the boundary goes before the minimum-sonority segment (rightmost
    on ties)."""
    m = len(cluster)
    for k in range(m, -1, -1):                        # k = onset length, longest first
        split = m - k
        if legal_onset(cluster[split:], spec, table) and legal_coda(cluster[:split], spec, table):
            return split, True
    best, best_son = m, None
    for j in range(m):
        son = sonority(cluster[j], table)
        if best_son is None or son <= best_son:
            best, best_son = j, son
    return best, False


def syllabify(word: Word, rf: RuleFile, table: FeatureTable) -> Word:
    """Maximal onset subject to legality; sets word.syllables, word.nuclei and, on
    failure, word.illegal = the minimal unparseable span. Never raises on a word.
    Resolves Word._pending_stress to a syllable index (S1). Appends one TraceEntry."""
    spec = rf.syllable
    if spec is None:
        spec = _ANY
    segs = word.segments
    n = len(segs)

    if spec.domain == "stem":
        cuts = sorted(b for b in word.morphemes if 0 < b < n)
    else:
        cuts = []
    edges = [0, *cuts, n]
    domains = [(edges[i], edges[i + 1]) for i in range(len(edges) - 1)] if n else []

    starts: list[int] = []
    nuclei: list[tuple[int, int]] = []
    illegal: set[int] = set()

    for a, b in domains:
        local = group_nuclei(segs[a:b], spec, table)
        if not local:
            illegal.update(range(a, b))
            continue
        nucs = [(a + s, a + e) for s, e in local]
        nuclei.extend(nucs)
        # domain-initial onset
        first = nucs[0][0]
        starts.append(a)
        onset = segs[a:first]
        if not onset:
            if spec.onset_required:
                illegal.add(first)
        elif not legal_onset(onset, spec, table):
            illegal.update(range(a, first))
        # interludes
        for (_, stop), (nxt, _) in zip(nucs, nucs[1:]):
            inter = segs[stop:nxt]
            split, ok = _split_interlude(inter, spec, table)
            if not ok:
                illegal.update(range(stop, nxt))
            elif split == len(inter) and spec.onset_required:
                illegal.add(nxt)                      # §12.D: an onsetless syllable (hiatus)
            starts.append(stop + split)
        # domain-final coda
        last_stop = nucs[-1][1]
        coda = segs[last_stop:b]
        if coda and not _legal_final_coda(coda, spec, table, word_final=(b == n)):
            illegal.update(range(last_stop, b))

    syllables = tuple(starts)
    out = replace(word, syllables=syllables, nuclei=tuple(nuclei), stress=None,
                  illegal=frozenset())
    illegal |= _banned_spans(out, rf, table, frozenset(cuts))

    # S1: stress index conversion (pending segment index, or an earlier syllable index)
    seg_index: int | None = word._pending_stress
    if seg_index is None and word.stress is not None and word.stress < len(word.syllables):
        seg_index = word.syllables[word.stress]
    stress: int | None = None
    if seg_index is not None and syllables:
        stress = max((i for i, s in enumerate(syllables) if s <= seg_index), default=0)

    out = replace(out, stress=stress, illegal=frozenset(illegal), _pending_stress=None)
    note = ""
    if illegal:
        note = "illegal: " + " ".join(
            f"{i}:{segs[i]}" for i in sorted(illegal))
    return out.traced(TraceEntry(stage=_STAGE, rule_id=_RULE_ID, tag="",
                                 before=word.ipa(), after=out.ipa(), note=note))


_ANY = SyllableSpec(template=None, nuclei=(), onsets=None, codas=None, onset_set=None,
                    coda_set=None, onset_tiers={}, coda_tiers={}, onset_required=False,
                    appendix=(), domain="word", sonority=False, bans=())
