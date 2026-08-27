"""The Old Irish strand: lookup or retro-filter, then the spelled-word assembly.

Old Irish spec §2, §6, §11; plan Task 12; interpretations O-9, O-11, O-12, O-14, O-17, O-22,
O-23, O-32, O-33.

`pipeline.run_entry` hands an `old-irish` target to `run_entry_oi` (O-9), which composes the
stages in this strand's own order. The input is the CITATION form (spec §11): the entry's
orthography and IPA are taken as given — the modern template's mutated output is never
consumed — and the strand applies its own grammar afterwards.

The fork (spec §2 steps 1–2), on `pipeline.lookup`:

| lexicon row       | what happens                                             | flag            |
|-------------------|----------------------------------------------------------|-----------------|
| `attested`        | the attested spelling is tokenized as-is; no filter runs | `ATTESTED`      |
| `middle`          | identical (O-22)                                         | `ATTESTED:MIr`  |
| `none`            | retro-filter, exactly as a miss (O-12)                   | `RETRO:<kind>`  |
| no row            | retro-filter                                             | `RETRO`         |

The retro path is the engine's stages on IPA — `tokenize` → `Word.from_tokenized` →
`irish.normalize` → `orth.tag_word` → `substitute_stage` → `syllabify` → `repair` →
`assign_stress` → `post_stress` → `respell` — and the `[respell]` output IS the spelled word
(spec §11): `SpelledWord.from_spelling` tokenizes it. The pre-reconstruction phonology survives
as the `respell` trace entry's `before`.

The stem class (O-21, O-33, S22). A NON-EMPTY lexicon `stem` is a supplied class and contributes
no assumption tag; a blank one is not a supplied class — it goes through `infer_stem` like a
RETRO word and is tagged `stem:from-declension-*` or `stem:default-by-gender-*`. The same
reading applies one level down: a modern `declension` that `inputs.infer` guessed (tagged
`declension:*`) is not a supplied class either, and the entry falls to the gender default.

`adapt_oi` (O-11, O-14). The spelled words are finished by the time they arrive; each is
rendered (with `[meta] punctum` applied to the STRING only) and reconstructed once by
`spelling_to_ipa`. `Result.ipa` joins segments with no separator inside a word and one space
between words (GPT P2). `Result.words` holds the reconstructed segments syllabified and
stressed by this target's `[syllable]` / `[stress]`, so the cross-target property checks
(inventory membership, one primary stress) see the same object they see elsewhere; the IPA
string itself is the reconstruction, unmarked.

Inflection (spec §5, §11; digest §10.5; plan Task 14). `apply_case` is the stem dispatch over
the `[inflect]` grapheme tables (O-26 names). The LEXICON is authoritative and the table is
the fallback: an attested `oi_gen` is returned verbatim, because the n-stem suffix vowel and
the u-stem `-o`/`-a` are lexical in Old Irish and cannot be derived from spelling. The
vocative is identity outside the masculine o-stem (O-30; digest §10.5 [pokorny1914 p.65
§142]), whose vocative IS the genitive table. `NOM_A`/`NOM_O` realize spec §11's ending
marker ⟨ə⟩ (⟨-e⟩ for an ā-stem, ⟨-a⟩ otherwise); `run_entry_oi` applies the nominative to
every word before rendering, so no finished output carries the marker.

Constructions. `DESC` and its two slot forms are supported here: this strand declares no
`epithet-*` keys, so a slot resolves to "no affix" with an `epithet:<SLOT>-unmapped-in-Old
Irish` assumption and `DESC+ADJ` equals `DESC` (R30, O-17). Every other name raises
`ConstructionNotInStrand` until `[templates]` lands (plan Task 15).
"""
from __future__ import annotations

import functools
from dataclasses import dataclass
from typing import TYPE_CHECKING, Sequence

from .dsl import RuleFile
from .features import FeatureTable
from .irish import normalize
from .lexicon import LexEntry, read_lexicon
from .orth import tag_word
from .pipeline import (PipelineError, Result, lookup, parse_construction, resolve_epithet)
from .poststress import post_stress
from .repair import repair
from .respell import respell_traced
from .spelled import (SpelledWord, apply_grapheme_table, parse_quality_pairs, spelling_to_ipa,
                      spelling_to_words)
from .stress import assign_stress
from .substitute import substitute_stage
from .syllabify import syllabify
from .tokenize import tokenize
from .word import TraceEntry, Word

if TYPE_CHECKING:
    from .inputs import Entry

__all__ = ["OI_FLAGS", "LOOKUP_STAGE", "RECONSTRUCT_STAGE", "ConstructionNotInStrand", "Stem",
           "infer_stem", "to_old_irish", "apply_oi_mutation", "CASE_TABLES", "PRIMITIVE_TABLES",
           "apply_case", "adapt_oi", "run_entry_oi"]

OI_FLAGS = ("ATTESTED", "ATTESTED:MIr", "RETRO", "RETRO:loan", "RETRO:late")
LOOKUP_STAGE = "lookup"
RECONSTRUCT_STAGE = "reconstruct"
_SUPPORTED = ("DESC",)          # Task 15 adds the rest via [templates]
_SLENDER_LETTERS = frozenset("eiéí")
_VOWEL_LETTERS = frozenset("aeiouáéíóú")


class ConstructionNotInStrand(PipelineError):
    """The construction exists for the other targets but this strand has no template for
    it (O-17). The CLI and gallery report it as a skip."""


@dataclass(frozen=True)
class Stem:
    words: tuple[SpelledWord, ...]          # the Old Irish nominative, one per written word
    gen: tuple[SpelledWord, ...] | None     # the attested genitive, when the lexicon gave one
    stem: str                               # a lexicon.STEMS value, looked up or inferred
    gender: str
    flag: str                               # one of OI_FLAGS
    assumptions: tuple[str, ...]
    trace: tuple[TraceEntry, ...]
    engine_flags: tuple[str, ...] = ()      # the retro-filter's own flags (UNATTESTED_CLUSTER:…,
    # O-20), kept apart from `flag` so the lookup flag stays exactly one of OI_FLAGS


@functools.lru_cache(maxsize=1)
def _default_lexicon() -> dict[str, LexEntry]:
    return read_lexicon()


# ---- the stem class (O-21, O-33, S22) ------------------------------------------------------

def _slender_final(orthography: str) -> bool:
    """A consonant-final word whose last vowel letter is ⟨e i é í⟩ (the orthographic test
    `inputs` uses when no IPA is available)."""
    orth = orthography.strip().lower()
    if not orth or orth[-1] in _VOWEL_LETTERS:
        return False
    vowels = [ch for ch in orth if ch in _VOWEL_LETTERS]
    return bool(vowels) and vowels[-1] in _SLENDER_LETTERS


def infer_stem(entry: "Entry") -> tuple[str, str]:
    """(Old Irish stem class, assumption tag) from `Entry.declension`, else the gender
    (plan Task 12 table; S22: an unclassified feminine is an ā-stem, not an o-stem).

    Only a SUPPLIED modern declension counts. `inputs.infer` fills a blank one and tags the
    entry `declension:inferred-*` / `declension:default-*`; that guess is not a class the
    input gave (the O-33 reading), so such an entry takes the gender default and says so."""
    declension = (entry.declension or "").strip().lower()
    if any(tag.startswith("declension:") for tag in entry.assumptions):
        declension = ""
    if declension == "m1":
        return "o", "stem:from-declension-m1"
    if declension == "f2":
        return "ā", "stem:from-declension-f2"
    if declension == "ach":
        return "o", "stem:from-declension-ach"
    if declension == "m3":
        if _slender_final(entry.orthography):
            return "i", "stem:from-declension-m3-slender"
        return "u", "stem:from-declension-m3-broad"
    if declension == "d4":
        return "indecl", "stem:from-declension-d4"
    if (entry.gender or "").strip().lower() == "f":
        return "ā", "stem:default-by-gender-f"
    return "o", "stem:default-by-gender-m"


# ---- the retro path (spec §2 step 2, §11) ----------------------------------------------------

def _retro_words(entry: "Entry", oi: RuleFile, irish: RuleFile, table: FeatureTable
                 ) -> tuple[tuple[SpelledWord, ...], tuple[str, ...], tuple[TraceEntry, ...]]:
    """Stages 2–7 on the citation-form IPA, one written word per space-separated word; the
    `[respell]` output is tokenized into the spelled word. Returns (words, flags, trace)."""
    pieces = Word.from_tokenized(tokenize(entry.ipa, table)).split_words()
    orth_words = entry.orthography.split()
    if len(orth_words) != len(pieces):
        orth_words = [entry.orthography] * len(pieces)
    dialect = entry.dialect or "C"
    words: list[SpelledWord] = []
    flags: list[str] = []
    trace: list[TraceEntry] = []
    for piece, orth in zip(pieces, orth_words):
        word = normalize(piece, irish, table, dialect=dialect)
        word = tag_word(word, orth)
        word = substitute_stage(word, oi, table)
        word = syllabify(word, oi, table)
        word = repair(word, oi, table)
        word = assign_stress(word, oi, table)
        word = post_stress(word, oi, table)
        spelling, respell_trace = respell_traced(word, oi, table)
        spelled = SpelledWord.from_spelling(spelling)
        if orth[:1].isupper():                              # O-32
            spelled = SpelledWord(spelled.graphemes, capitalized=True)
        words.append(spelled)
        trace.extend(word.trace)
        trace.extend(respell_trace)
        for flag in word.flags:
            if flag not in flags:
                flags.append(flag)
    return tuple(words), tuple(flags), tuple(trace)


# ---- the fork (spec §2 steps 1–2) ----------------------------------------------------------

def to_old_irish(entry: "Entry", lexicon: dict[str, LexEntry], oi: RuleFile, irish: RuleFile,
                 table: FeatureTable) -> Stem:
    """Lookup on the citation form (O-23); a form-bearing row supplies its spelling verbatim
    and the filter never runs; a `none` row or a miss goes through the retro-filter."""
    row = lookup(entry, lexicon)
    assumptions: list[str] = []
    if row is not None and row.status in ("attested", "middle"):
        words = spelling_to_words(row.oi_nom)
        gen = spelling_to_words(row.oi_gen) if row.oi_gen else None
        if row.stem:
            stem = row.stem
        else:                                               # O-33 / R31d
            stem, tag = infer_stem(entry)
            assumptions.append(tag)
        gender = row.gender or entry.gender
        trace = (TraceEntry(stage=LOOKUP_STAGE, rule_id="lookup:hit", tag="attested",
                            before=entry.orthography, after=row.oi_nom,
                            note=f"{row.status} row, line {row.line}: {row.source}"),)
        return Stem(words, gen, stem, gender, row.flag, tuple(assumptions), trace)
    words, flags, retro_trace = _retro_words(entry, oi, irish, table)
    stem, tag = infer_stem(entry)
    assumptions.append(tag)
    if row is None:
        head = TraceEntry(stage=LOOKUP_STAGE, rule_id="lookup:miss", tag="",
                          before=entry.orthography, after=entry.orthography,
                          note="no lexicon row for the citation form; retro-filter")
        flag = "RETRO"
    else:                                                   # O-12, O-18
        head = TraceEntry(stage=LOOKUP_STAGE, rule_id="lookup:none", tag="",
                          before=entry.orthography, after=entry.orthography,
                          note=f"none row ({row.kind}), line {row.line}: {row.source}; "
                               "retro-filter")
        flag = row.flag
    return Stem(words, None, stem, entry.gender, flag, tuple(assumptions),
                (head, *retro_trace), engine_flags=flags)


# ---- the mutations (spec §5, §11; digest §10.4; plan Task 13) ------------------------------

def apply_oi_mutation(word: SpelledWord, name: str, oi: RuleFile) -> SpelledWord:
    """Apply `oi.grapheme_mutations[name]` (`LEN` or `NAS`) to a spelled word and set
    `word.mutation = name`. The table rewrites the WRITTEN half (⟨ch th ph ṡ ḟ⟩, ⟨mb nd ng
    n-⟩); the metadata carries the unwritten half — lenited *b d g m* and nasalized *c t p*
    (digest §10.2 conv. 1; spec §11 (ii)) — which `spelling_to_ipa` reads. A mutation table
    is applied simultaneously, like the segment engine's (`irish._apply_table`)."""
    if name not in oi.grapheme_mutations:
        raise PipelineError(f"{oi.path}: no [mutations] table {name!r} (have: "
                            + ", ".join(sorted(oi.grapheme_mutations)) + ")")
    rules = oi.grapheme_mutations[name]
    return apply_grapheme_table(word, rules, simultaneous=True).with_mutation(name)  # type: ignore[arg-type]


# ---- the inflection (spec §5, §11; digest §10.5; plan Task 14) -----------------------------

CASE_TABLES: dict[tuple[str, str], str] = {
    ("gen", "o"): "GEN_O", ("gen", "ā"): "GEN_A", ("gen", "i"): "GEN_I", ("gen", "u"): "GEN_U",
    ("gen", "n"): "GEN_N", ("gen", "dental"): "GEN_DENT", ("gen", "velar"): "GEN_VELAR",
    ("gen", "r"): "GEN_R", ("gen", "s"): "GEN_S",
    # VOC_O = GEN_O (digest §10.5 [pokorny1914 p.65 §142]): the DSL has no table aliasing,
    # so the o-stem vocative resolves to the genitive table by name here.
    ("voc", "o"): "GEN_O",
    ("nom", "ā"): "NOM_A", ("nom", ""): "NOM_O",        # "" = every other class
    ("dat", "o"): "DAT_O", ("dat", "ā"): "DAT_A",
}
"""(case, lexicon stem) -> `[inflect]` sub-table (O-26). `indecl` and `irregular` have no
table (they are inert in `apply_case`)."""

PRIMITIVE_TABLES: dict[str, tuple[str, ...]] = {
    "INF": ("GEN_O", "GEN_A", "GEN_S"),
    "DEP": ("GEN_I",),
}
"""The shared primitives (digest §10.2 §§36-41) declared once as their own `[inflect]`
sub-tables and copied verbatim into the case tables named here; a test asserts the copies
are identical to the declaration. SYNC is table-specific (its replacement carries the
suffix) and is written inline."""

_INERT_STEMS = ("indecl", "irregular")


def _case_note(trace: list[TraceEntry] | None, case: str, stem: Stem, rule_id: str, note: str,
               after: str) -> None:
    if trace is None:
        return
    before = " ".join(w.render() for w in stem.words)
    trace.append(TraceEntry(stage="inflect", rule_id=rule_id, tag="", before=before,
                            after=after, note=f"{case}: {note}"))


def apply_case(stem: Stem, case: str, oi: RuleFile, *,
               trace: list[TraceEntry] | None = None) -> tuple[SpelledWord, ...]:
    """The case form of a stem, one spelled word per written word. Precedence — the lexicon
    is authoritative, the table is the fallback (plan Task 14):

    1. `case == "gen"` and `stem.gen` is not None   -> the ATTESTED genitive, verbatim.
    2. `stem.stem` in (`indecl`, `irregular`)        -> unchanged, trace note.
    3. a `CASE_TABLES` entry for (case, stem.stem)   -> `apply_grapheme_table(ordered)`.
    4. `case == "voc"`                               -> IDENTITY (O-30 / R23), trace note.
    5. otherwise                                     -> `GEN_O`, tagged `case:<case>-fallback-o`.

    For `nom`, every class but `ā` takes `NOM_O` (the `("nom", "")` entry). A table is
    applied to every written word of the stem; `trace`, when given, receives one entry."""
    after = lambda words: " ".join(w.render() for w in words)      # noqa: E731
    if case == "gen" and stem.gen is not None:
        _case_note(trace, case, stem, "inflect:attested", "attested genitive, verbatim "
                   "(precedence rule 1)", after(stem.gen))
        return stem.gen
    if stem.stem in _INERT_STEMS:
        _case_note(trace, case, stem, f"inflect:{stem.stem}", f"{stem.stem} stem: unchanged",
                   after(stem.words))
        return stem.words
    key = (case, stem.stem)
    if case == "nom" and stem.stem != "ā":
        key = ("nom", "")
    name = CASE_TABLES.get(key)
    note = f"table {name}"
    if name is None and case == "voc":
        _case_note(trace, case, stem, "inflect:voc-identity",
                   "vocative = nominative outside the masculine o-stem (O-30; digest §10.5 "
                   "[pokorny1914 p.65 §142])", after(stem.words))
        return stem.words
    if name is None:
        name = "GEN_O"
        note = f"case:{case}-fallback-o (no table for stem {stem.stem!r})"
    if name not in oi.grapheme_inflect:
        raise PipelineError(f"{oi.path}: no [inflect] table {name!r} (have: "
                            + ", ".join(sorted(oi.grapheme_inflect)) + ")")
    rules = oi.grapheme_inflect[name]
    words = tuple(apply_grapheme_table(w, rules, simultaneous=False)  # type: ignore[arg-type]
                  for w in stem.words)
    _case_note(trace, case, stem, f"inflect:{name}", note, after(words))
    return words


# ---- the assembly (O-11, O-14) ---------------------------------------------------------------

def _punctum(oi: RuleFile) -> bool:
    return oi.meta.get("punctum", "on").strip().lower() != "off"


def _phonology_of(segments: tuple[str, ...], oi: RuleFile, table: FeatureTable) -> Word:
    """A `Word` over the reconstructed segments, syllabified and stressed by this target's
    own `[syllable]` / `[stress]` for `Result.words`; nothing here feeds `Result.ipa`."""
    word = Word(segments=segments)
    if not segments:
        return word
    return assign_stress(syllabify(word, oi, table), oi, table)


def adapt_oi(words: Sequence[SpelledWord], oi: RuleFile, table: FeatureTable, *,
             assumptions: Sequence[str] = (), flags: Sequence[str] = (),
             trace: Sequence[TraceEntry] = ()) -> Result:
    """Render and reconstruct finished spelled words. `punctum` touches the written string
    only (O-14); `ipa` is `spelling_to_ipa` per word, segments joined with no separator
    inside a word and a single space between words (O-11, GPT P2)."""
    pairs = (parse_quality_pairs(oi.meta["quality-pairs"])
             if "quality-pairs" in oi.meta else None)
    punctum = _punctum(oi)
    spellings: list[str] = []
    ipas: list[str] = []
    out_words: list[Word] = []
    out_trace = list(trace)
    for word in words:
        spelling = word.render(punctum=punctum)
        segments = spelling_to_ipa(word, pairs=pairs)
        ipa = "".join(segments)
        spellings.append(spelling)
        ipas.append(ipa)
        out_words.append(_phonology_of(segments, oi, table))
        out_trace.append(TraceEntry(stage=RECONSTRUCT_STAGE, rule_id="spelling_to_ipa", tag="",
                                    before=word.render(), after=ipa,
                                    note=f"mutation={word.mutation or '-'}"))
    return Result(
        respelling=" ".join(spellings),
        ipa=" ".join(ipas),
        flags=tuple(flags),
        fallbacks=sum(1 for t in trace if t.tag == "fallback"),
        assumptions=tuple(assumptions),
        trace=tuple(out_trace),
        words=tuple(out_words),
    )


def run_entry_oi(entry: "Entry", construction: str, irish: RuleFile, oi: RuleFile,
                 table: FeatureTable, *, lexicon: dict[str, LexEntry] | None = None,
                 slots: "dict[str, Entry] | None" = None) -> Result:
    """The Old Irish `run_entry` (O-9): fork, then assemble. `slots` is accepted for the
    multi-slot templates of Task 15; `DESC` takes its head from `entry`."""
    name, slot = parse_construction(construction)
    if lexicon is None:
        lexicon = _default_lexicon()
    stem = to_old_irish(entry, lexicon, oi, irish, table)
    assumptions = list(entry.assumptions) + list(stem.assumptions)
    if slot is not None:
        epithet = resolve_epithet(oi, slot)
        if epithet is not None:
            raise PipelineError(f"{oi.path}: [meta] epithet-{slot} = {epithet}, but this "
                                "strand's grammar is on graphemes and has no epithet affixation")
        assumptions.append(f"epithet:{slot}-unmapped-in-{oi.meta.get('name', oi.path)}")
    if name not in _SUPPORTED:                              # Task 15
        raise ConstructionNotInStrand(f"{oi.path}: no template for {name!r} in this strand "
                                      f"(have: {', '.join(_SUPPORTED)})")
    flags = [stem.flag]
    for flag in stem.engine_flags:
        if flag not in flags:
            flags.append(flag)
    trace = list(stem.trace)
    words = apply_case(stem, "nom", oi, trace=trace)      # realizes the ending marker (spec §11)
    return adapt_oi(words, oi, table, assumptions=assumptions, flags=flags, trace=trace)
