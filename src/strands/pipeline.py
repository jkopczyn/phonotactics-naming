"""The stage pipeline: spec §4 stages 1–7 over a `Word` list (plan Task 21).

`adapt()` runs stages 2–7 on already-normalized Irish words, one word at a time, and rejoins
the results with spaces: `substitute_stage` (§4.2, with the inventory fallback) →
`syllabify` (§4.3) → `repair` (§4.4 / §12.A) → `assign_stress` → `post_stress` (§4.5) →
optional epithet affixation, after which stages 3–5 run again on the affixed word (§4.6) →
`respell` (§4.7). `run_entry()` puts stage 1 in front: the Irish template
(`irish.build_construction`) and `irish.normalize`, then `adapt()`.

Epithet slots (spec §12.H, I-39). A construction tag is `NAME` or `NAME+SLOT` with `SLOT` in
`EPITHET_SLOTS`; the target's `[meta]` maps a slot to one of its `[epithets]` names
(`epithet-ADJ = NISBA`). An unmapped slot means "no affix", never an error. The affix goes on
the construction's LAST word (the head of `DESC`, the only template the tags are used with),
joined at a `$` boundary; its attach-condition is the epithet's environment, evaluated around
the affix on the joined word — when it fails, the word is left alone with a trace note.

Stress (I-40). The Irish pre-pass parks Connacht initial stress as a pending segment index;
`syllabify` turns it into a syllable index, and the target's own procedure then overrides it
(`keep-source` is the procedure that keeps it). `Result.ipa` prints the stress mark unless the
target's `[stress] mark = off` (Georgian); `Result.respelling` never carries marks at all.

Old Irish (Old Irish spec §2, O-9). `lookup()` is stage 1b: an exact match of the entry's
CITATION form against the Old Irish lexicon, keyed by `lexicon.key` (NFC + casefold), with
no de-mutation and no fuzzy fallback (O-23). `run_entry()` reads the target's `[meta] strand`
right after `parse_construction`: `old-irish` hands off to `oldirish.run_entry_oi`, which
composes the Old Irish stages in its own order (lookup or retro-filter, then the grapheme
grammar, then the one-way reconstruction). `adapt()` is not involved in that strand.

`Result.trace` is the per-word traces in word order, each followed by its respell entries;
`Result.flags` is the union of the words' flags in first-seen order; `Result.fallbacks` the
sum of `Word.fallback_count()`; `Result.assumptions` the entry's inference tags plus any note
the pipeline itself adds. Everything is a tuple, so two runs of the same input compare equal.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, replace
from pathlib import Path
from typing import TYPE_CHECKING

from .dsl import RuleFile, parse_rules_file
from .features import FeatureTable
from .irish import _head_name, build_construction, normalize
from .poststress import post_stress
from .repair import repair
from .respell import respell_traced
from .rewrite import _match_ctx
from .stress import assign_stress
from .substitute import substitute_stage
from .syllabify import syllabify
from .word import TraceEntry, Word

if TYPE_CHECKING:
    from .inputs import Entry
    from .lexicon import LexEntry

__all__ = [
    "EPITHET_SLOTS",
    "TARGETS",
    "CONSTRUCTIONS",
    "PipelineError",
    "ConstructionNotInStrand",
    "Result",
    "resolve_epithet",
    "affix_epithet",
    "adapt",
    "parse_construction",
    "lookup",
    "run_entry",
    "load_target",
    "stress_marked",
]

EPITHET_SLOTS = ("ADJ", "NOUN")  # I-39 / spec §12.H
TARGETS = ("welsh", "arabic-egy", "georgian", "dutch", "old-irish")
# The Old Irish formations (Old Irish spec §8 row O6; plan Task 15) are listed with the rest
# so the CLI and the gallery can ask every strand for them; a strand whose [templates] has
# no entry of that name raises `ConstructionNotInStrand` (O-17), which they report as a skip.
CONSTRUCTIONS = (
    "VOC",
    "GEN",
    "PATRO_O",
    "PATRO_NI",
    "ADJ",
    "OF",
    "COMPOUND",
    "DESC",
    "DESC+ADJ",
    "DESC+NOUN",
    "MAEL",
    "GILLA",
    "CU",
    "FER",
    "COLOUR",
    "MAC",
    "UA",
    "INGEN",
)
_RULES_DIR = Path(__file__).resolve().parents[2] / "rules"
_EPITHET_STAGE = "epithet"


class PipelineError(Exception):
    """A pipeline-level misuse: unknown target, slot, or epithet name."""


class ConstructionNotInStrand(PipelineError):
    """The construction is in `CONSTRUCTIONS` but the strand's templates have no entry of
    that name (Old Irish spec §5, O-17): PATRO_O/PATRO_NI for old-irish, MAEL for the other
    four. The CLI and the gallery report it as a skip, exactly like `MissingSlot`."""


@dataclass(frozen=True)
class Result:
    respelling: str
    ipa: str
    flags: tuple[str, ...]
    fallbacks: int
    assumptions: tuple[str, ...]
    trace: tuple[TraceEntry, ...]
    words: tuple[Word, ...]


# ---- epithets (§4.6, §12.H) ---------------------------------------------------------------------


def parse_construction(tag: str) -> tuple[str, str | None]:
    """'DESC+ADJ' -> ('DESC', 'ADJ'); 'VOC' -> ('VOC', None) (I-39)."""
    name, plus, slot = tag.partition("+")
    if not plus:
        return name, None
    if slot not in EPITHET_SLOTS:
        raise PipelineError(
            f"construction {tag!r}: unknown epithet slot {slot!r} "
            f"(one of {', '.join(EPITHET_SLOTS)})"
        )
    return name, slot


def resolve_epithet(target: RuleFile, slot: str) -> str | None:
    """target.meta may declare `epithet-ADJ = NISBA` / `epithet-NOUN = FEM_A`.
    Returns the [epithets] key, or None when the target maps nothing to that slot
    (which means 'no affix', not an error)."""
    if slot not in EPITHET_SLOTS:
        raise PipelineError(f"unknown epithet slot {slot!r} (one of {', '.join(EPITHET_SLOTS)})")
    name = target.meta.get(f"epithet-{slot}", "").strip()
    if not name:
        return None
    if name not in target.epithets:
        raise PipelineError(
            f"{target.path}: [meta] epithet-{slot} = {name}, but [epithets] "
            f"has no {name} (have: {', '.join(sorted(target.epithets)) or 'none'})"
        )
    return name


def affix_epithet(word: Word, name: str, rf: RuleFile, table: FeatureTable) -> Word:
    """Attach rf.epithets[name] after a `$` at the word end (spec §4.6) when its
    attach-condition holds around the affix; otherwise return the word with a trace note.
    The returned word is NOT re-syllabified; `adapt` re-runs stages 3–5."""
    try:
        ep = rf.epithets[name]
    except KeyError:
        raise PipelineError(
            f"{rf.path}: no [epithets] entry {name!r} "
            f"(have: {', '.join(sorted(rf.epithets)) or 'none'})"
        ) from None
    n = len(word.segments)
    before = word.ipa()
    joined = replace(
        word, segments=word.segments + ep.form, morphemes=word.morphemes | {n}, illegal=frozenset()
    )
    left = _match_ctx(tuple(reversed(ep.left)), 0, n, -1, joined, rf, table, {})
    right = (
        _match_ctx(ep.right, 0, n + len(ep.form), +1, joined, rf, table, {})
        if left is not None
        else None
    )
    rule_id = f"epithets:{name}"
    if right is None:
        return word.traced(
            TraceEntry(
                stage=_EPITHET_STAGE,
                rule_id=rule_id,
                tag="",
                before=before,
                after=before,
                note=f"attach-condition of {name} not met; no affix",
            )
        )
    return joined.traced(
        TraceEntry(
            stage=_EPITHET_STAGE,
            rule_id=rule_id,
            tag="",
            before=before,
            after=joined.ipa(),
            note=f"affix {name} = {''.join(ep.form)} at $",
        )
    )


# ---- stages 2–7 ---------------------------------------------------------------------------------


def stress_marked(target: RuleFile) -> bool:
    """`[stress] mark = off` (Georgian, digest §4.3) suppresses ˈ in `Result.ipa`."""
    if target.stress is None:
        return True
    return target.stress.params.get("mark", "on").strip().lower() != "off"


def _phonology(word: Word, target: RuleFile, table: FeatureTable) -> Word:
    """Stages 3–5: syllabify, repair, stress, post-stress."""
    word = syllabify(word, target, table)
    word = repair(word, target, table)
    word = assign_stress(word, target, table)
    return post_stress(word, target, table)


def _adapt_word(
    word: Word, target: RuleFile, table: FeatureTable, epithet: str | None
) -> tuple[Word, str, tuple[TraceEntry, ...]]:
    word = substitute_stage(word, target, table)
    word = _phonology(word, target, table)
    if epithet is not None:
        affixed = affix_epithet(word, epithet, target, table)
        if affixed.segments != word.segments:
            affixed = _phonology(affixed, target, table)
        word = affixed
    spelling, respell_trace = respell_traced(word, target, table)
    return word, spelling, respell_trace


def adapt(
    words: Sequence[Word],
    target: RuleFile,
    table: FeatureTable,
    *,
    epithet: str | None = None,
    assumptions: Sequence[str] = (),
) -> Result:
    """Spec §4 stages 2-7: substitute_stage -> syllabify -> repair -> assign_stress ->
    post_stress -> (epithet: affix then re-run syllabify/repair/stress/post-stress) ->
    respell. `Result.ipa` prints the stress mark unless the target's
    `[stress] mark = off` (Georgian, digest §4.3); `Result.respelling` never carries
    marks at all. The epithet goes on the last word only."""
    marks = stress_marked(target)
    out_words: list[Word] = []
    spellings: list[str] = []
    trace: list[TraceEntry] = []
    flags: list[str] = []
    last = len(words) - 1
    for i, word in enumerate(words):
        done, spelling, respell_trace = _adapt_word(
            word, target, table, epithet if i == last else None
        )
        out_words.append(done)
        spellings.append(spelling)
        trace.extend(done.trace)
        trace.extend(respell_trace)
        for flag in done.flags:
            if flag not in flags:
                flags.append(flag)
    return Result(
        respelling=" ".join(spellings),
        ipa=" ".join(wd.ipa(marks=True) if marks else wd.ipa(marks=False) for wd in out_words),
        flags=tuple(flags),
        fallbacks=sum(wd.fallback_count() for wd in out_words),
        assumptions=tuple(assumptions),
        trace=tuple(trace),
        words=tuple(out_words),
    )


# ---- stage 1b: lookup (Old Irish spec §2; O-9, O-23) ------------------------------------------


def lookup(entry: Entry, lexicon: dict[str, LexEntry]) -> LexEntry | None:
    """Stage 1b (spec §2, O-9, O-23): exact match of `entry.orthography` — the CITATION form
    — after NFC + casefold. No de-mutation, no fuzzy fallback."""
    from .lexicon import key

    return lexicon.get(key(entry.orthography))


# ---- stage 1 + the rest ------------------------------------------------------------------------


def _head_slot(irish: RuleFile, name: str) -> str | None:
    """The template's first argument slot (its head, I-16)."""
    items = irish.templates.get(name)
    return _head_name(items) if items is not None else None


def run_entry(
    entry: Entry,
    construction: str,
    irish: RuleFile,
    target: RuleFile,
    table: FeatureTable,
    slots: dict[str, Entry] | None = None,
) -> Result:
    """Stage 1 (template + normalize) then adapt(), passing the resolved epithet.
    `slots` defaults to `{head: entry}` — the template's first argument slot; a template
    with further slots (ADJ, OF, COMPOUND) needs them supplied and raises `MissingSlot`
    otherwise (the CLI reports that as a skip)."""
    name, slot = parse_construction(construction)
    if target.meta.get("strand", "").strip() == "old-irish":  # O-9
        from .oldirish import run_entry_oi

        return run_entry_oi(entry, construction, irish, target, table, slots=slots)
    if name not in irish.templates:  # O-17
        raise ConstructionNotInStrand(
            f"{irish.path}: no [templates] entry {name!r} for target {target.path} "
            f"(have: {', '.join(sorted(irish.templates)) or 'none'})"
        )
    if slots is None:
        head = _head_slot(irish, name)
        slots = {head: entry} if head is not None else {}
    words = build_construction(name, slots, irish, table)
    words = [normalize(wd, irish, table, dialect=entry.dialect or "C") for wd in words]
    assumptions = list(entry.assumptions)
    epithet = None
    if slot is not None:
        epithet = resolve_epithet(target, slot)
        if epithet is None:
            assumptions.append(f"epithet:{slot}-unmapped-in-{target.meta.get('name', target.path)}")
    return adapt(words, target, table, epithet=epithet, assumptions=assumptions)


def load_target(name: str, table: FeatureTable) -> RuleFile:
    """rules/<name>.rules for a name in TARGETS."""
    if name not in TARGETS:
        raise PipelineError(f"unknown target {name!r} (one of {', '.join(TARGETS)})")
    return parse_rules_file(_RULES_DIR / f"{name}.rules", table)
