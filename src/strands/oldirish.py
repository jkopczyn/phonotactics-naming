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

Constructions (spec §5, §11; plan Task 15). `build_oi_construction` is this strand's own
template builder — `irish._Builder` is not reused, because its `ART` is hardcoded modern
Irish (*an*/*na*, HPREF/TPREF; R22). It evaluates an `arg` item to the slot's `Stem`, a
quoted literal as a SPELLING (O-25), `GEN NOM VOC DAT` through `apply_case`, `LEN NAS`
through `apply_oi_mutation`, `LEN_IF_F` as lenition when the head is feminine, and `ART`
as digest §10.4's article (`_article`: *in/ind/int*, *a*ᴺ, *inna*; no h- or t-prefix).
A `" "` literal separates words; adjacent items without one are joined into a compound
(`COLOUR LEN(NAME)`), which keeps the first element's capitalization and mutation. Every
word re-applies its own capitalization at render (O-32). A construction with no template
in this file (`PATRO_O`, `PATRO_NI`) raises `ConstructionNotInStrand` (O-17); an unsupplied
slot raises `irish.MissingSlot`, so the CLI's skip logic is shared. `DESC` = `NOM(NOUN)`
and its two slot forms resolve to "no affix" with an `epithet:<SLOT>-unmapped-in-Old
Irish` assumption, so `DESC+ADJ` equals `DESC` (R30, O-17).
"""
from __future__ import annotations

import functools
from dataclasses import dataclass, replace
from typing import TYPE_CHECKING, Sequence

from .dsl import RuleFile, TemplateItem
from .features import FeatureTable
from .irish import MissingSlot, _head_name, normalize
from .lexicon import LexEntry, read_lexicon
from .orth import tag_word
from .pipeline import (ConstructionNotInStrand, PipelineError, Result, lookup,
                       parse_construction, resolve_epithet)
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

__all__ = ["OI_FLAGS", "LOOKUP_STAGE", "RECONSTRUCT_STAGE", "TEMPLATE_STAGE",
           "ConstructionNotInStrand", "Stem", "infer_stem", "to_old_irish", "apply_oi_mutation",
           "CASE_TABLES", "PRIMITIVE_TABLES", "apply_case", "CASE_FUNCTIONS", "article",
           "build_oi_construction", "adapt_oi", "run_entry_oi"]

OI_FLAGS = ("ATTESTED", "ATTESTED:MIr", "RETRO", "RETRO:loan", "RETRO:late")
LOOKUP_STAGE = "lookup"
RECONSTRUCT_STAGE = "reconstruct"
TEMPLATE_STAGE = "templates"
_SLENDER_LETTERS = frozenset("eiéí")
_VOWEL_LETTERS = frozenset("aeiouáéíóú")
_ENDING_MARKER = "ə"                     # spec §11's unresolved ending token (Task 11)


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


# ---- the templates (spec §5, §11; digest §10.4-§10.5; plan Task 15) ------------------------

CASE_FUNCTIONS: dict[str, str] = {"GEN": "gen", "NOM": "nom", "VOC": "voc", "DAT": "dat"}
"""Template function name -> `apply_case` case (the built-ins `[meta] template-functions`
declares besides ART and LEN_IF_F)."""

_LIQUIDS_AND_F = frozenset({"ḟ", "f", "l", "n", "r"})    # [pokorny1914 p.59 §132]
_S_TOKENS = frozenset({"s", "ṡ"})


@dataclass(frozen=True)
class _Val:
    """A template item's value: spelled words, the stem they came from (None for a literal)
    and the case last applied (the article reads it)."""
    words: tuple[SpelledWord, ...]
    stem: Stem | None = None
    case: str = "nom"


def article(words: tuple[SpelledWord, ...], gender: str, case: str, oi: RuleFile, *,
            trace: list[TraceEntry] | None = None) -> tuple[SpelledWord, ...]:
    """digest §10.4's article, singular, as (article word, mutated noun words):

    | case / gender | form | mutation |
    |---|---|---|
    | nom. m.       | *in* (*int* before ⟨s⟩ is the leniting forms' sandhi, see below) | none |
    | nom. f.       | *in(d)*ᴸ | LEN |
    | nom. n.       | *a*ᴺ | NAS |
    | gen. m./n.    | *in(d)*ᴸ | LEN |
    | gen. f.       | *(in)na*ᴴ → *inna*; ᴴ is unwritten (digest §10.4) | none |
    | dat.          | *-(si)n(d)*ᴸ → *in(d)* | LEN |

    Final-consonant sandhi, the CONFLICT of digest §10.4 resolved for Pokorny (plan Task 15):
    ⟨-d⟩ stays only on a leniting form "before vowels or aspirated f, l, n, r"
    [pokorny1914-oldirish-grammar p.59 §132] — the lenited ⟨f⟩ is ⟨ḟ⟩ and lenited ⟨l n r⟩
    are unwritten, so the test is on the mutated word's first token; ⟨-t⟩ before ⟨s⟩ on the
    same forms (digest §10.4: *int sléibe*, *int súil*), written here before the lenited
    ⟨ṡ⟩. The parenthesized ⟨t⟩ of the m. nom. *in(t)* has no environment stated in the
    digest and is not realized. Wikipedia's unqualified ⟨-d⟩ is the alternative reading."""
    if not words:
        raise PipelineError(f"{oi.path}: ART() of an empty construction")
    gender = (gender or "m").strip().lower()[:1] or "m"
    lenites = (case == "nom" and gender == "f") or (case == "gen" and gender != "f") \
        or case == "dat"
    nasalizes = case == "nom" and gender == "n"
    noun = words[0]
    if case == "gen" and gender == "f":
        form, note = "inna", "gen. f. (in)naᴴ; the aspiration is unwritten"
    elif nasalizes:
        noun = apply_oi_mutation(noun, "NAS", oi)
        form, note = "a", "nom. n. aᴺ"
    else:
        if lenites:
            noun = apply_oi_mutation(noun, "LEN", oi)
        first = noun.graphemes[0]
        if lenites and first in _S_TOKENS:
            form = "int"
        elif lenites and (first[0] in _VOWEL_LETTERS or first in _LIQUIDS_AND_F):
            form = "ind"
        else:
            form = "in"
        note = (f"{case}. {gender}. in(d)ᴸ; -d/-t sandhi per [pokorny1914 p.59 §132]"
                if lenites else f"{case}. {gender}. in(t); no mutation")
    out = (SpelledWord.from_spelling(form), noun, *words[1:])
    if trace is not None:
        trace.append(TraceEntry(stage=TEMPLATE_STAGE, rule_id="templates:ART", tag="attested",
                                before=" ".join(w.render() for w in words),
                                after=" ".join(w.render() for w in out),
                                note=f"article, {note} (digest §10.4)"))
    return out


def _join_compound(a: tuple[SpelledWord, ...], b: tuple[SpelledWord, ...]
                   ) -> tuple[SpelledWord, ...]:
    """Adjacent template items with no `" "` between them form ONE written word (digest
    §10.5 compounding; spec §5 COLOUR): the last word of `a` absorbs the first of `b`,
    keeping `a`'s capitalization and initial mutation. The second element's own initial
    mutation is then word-internal, where `spelling_to_ipa` reads ⟨b d g⟩ as lenited
    post-vocalically by conv. 1 anyway; a written mutation (⟨th⟩, ⟨ṡ⟩) is in the tokens."""
    if not a:
        return b
    if not b:
        return a
    joined = replace(a[-1], graphemes=a[-1].graphemes + b[0].graphemes)
    return (*a[:-1], joined, *b[1:])


class _OiBuilder:
    def __init__(self, name: str, slots: dict[str, Stem], oi: RuleFile,
                 trace: list[TraceEntry]) -> None:
        self.name, self.slots, self.oi, self.trace = name, slots, oi, trace
        try:
            self.items = oi.templates[name]
        except KeyError:
            raise ConstructionNotInStrand(
                f"{oi.path}: no [templates] entry {name!r} in this strand "
                f"(have: {', '.join(sorted(oi.templates)) or 'none'})") from None
        head = _head_name(self.items)
        self.head: Stem | None = self.slot(head) if head is not None else None

    def slot(self, arg: str) -> Stem:
        try:
            return self.slots[arg]
        except KeyError:
            raise MissingSlot(f"template {self.name} needs slot {arg!r} "
                              f"(given: {', '.join(sorted(self.slots)) or 'none'})") from None

    def evaluate(self, item: TemplateItem) -> _Val:
        if item.conditional:
            raise PipelineError(f"{self.oi.path}: template {self.name}: conditional items "
                                "(`?`) are declension-tagged and have no meaning on the "
                                "spelled word")
        if item.kind == "literal":                               # O-25: a spelling
            return _Val(spelling_to_words(item.value))
        if item.kind == "arg":
            stem = self.slot(item.value)
            return _Val(stem.words, stem, "nom")
        if item.child is None:
            raise PipelineError(f"{self.oi.path}: template {self.name}: bare {item.value} "
                                "may not be nested")
        return self.call(item.value, self.evaluate(item.child))

    def call(self, func: str, val: _Val) -> _Val:
        oi = self.oi
        if func in oi.grapheme_mutations:                        # LEN, NAS
            if not val.words:
                return val
            mutated = (apply_oi_mutation(val.words[0], func, oi), *val.words[1:])
            return replace(val, words=mutated)
        if func in CASE_FUNCTIONS:
            case = CASE_FUNCTIONS[func]
            if val.stem is None:
                raise PipelineError(f"{oi.path}: template {self.name}: {func}() of a literal")
            # The case tables run on the CURRENT words (a mutation applied earlier is kept
            # as metadata; an attested genitive replaces the words wholesale, so the
            # metadata is re-applied afterwards).
            stem = replace(val.stem, words=val.words)
            words = apply_case(stem, case, oi, trace=self.trace)
            initial = val.words[0].mutation if val.words else ""
            if initial and words and not words[0].mutation:
                words = (words[0].with_mutation(initial), *words[1:])
            return _Val(words, val.stem, case)
        if func == "LEN_IF_F":
            # digest §10.4 [pokorny1914 p.8 §10]: lenited after a nom. sg. f. (S11: a
            # deliberate narrowing of Pokorny's fuller trigger list — see the rule file).
            if self.head is not None and (self.head.gender or "").lower().startswith("f"):
                return self.call("LEN", val)
            return val
        if func == "ART":
            gender = val.stem.gender if val.stem is not None else "m"
            return _Val(article(val.words, gender, val.case, oi, trace=self.trace),
                        val.stem, val.case)
        raise PipelineError(f"{oi.path}: template {self.name}: unknown function {func!r}")

    def build(self) -> tuple[SpelledWord, ...]:
        words: list[SpelledWord] = []
        current: tuple[SpelledWord, ...] = ()
        case = "nom"
        for item in self.items:
            if item.kind == "literal" and not item.value.strip():      # " " = separator
                words.extend(current)
                current = ()
                continue
            if item.kind == "call" and item.child is None:            # bare FUNC (I-16)
                val = self.call(item.value, _Val(current, self.head, case))
                current, case = val.words, val.case
                continue
            val = self.evaluate(item)
            current = _join_compound(current, val.words)
            case = val.case
        words.extend(current)
        rendered = " ".join(w.render() for w in words)
        self.trace.append(TraceEntry(stage=TEMPLATE_STAGE, rule_id=f"templates:{self.name}",
                                     tag="", before="", after=rendered,
                                     note=f"construction {self.name}, {len(words)} word(s)"))
        return tuple(words)


def _resolve_marker(stem: Stem, oi: RuleFile, trace: list[TraceEntry]) -> Stem:
    """spec §11: a RETRO word may carry the unresolved ending marker ⟨ə⟩; the nominative
    table realizes it by stem class BEFORE any case function sees the word, so no
    genitive is derived from a marker."""
    if not any(_ENDING_MARKER in w.graphemes for w in stem.words):
        return stem
    return replace(stem, words=apply_case(stem, "nom", oi, trace=trace))


def build_oi_construction(name: str, slots: dict[str, Stem], oi: RuleFile,
                          table: FeatureTable, *, trace: list[TraceEntry] | None = None
                          ) -> tuple[SpelledWord, ...]:
    """Apply `oi.templates[name]` to the slots' stems (spec §11; plan Task 15): one
    spelled word per written word, capitalization per word (O-32). Raises
    `ConstructionNotInStrand` for a name this file has no template for (O-17) and
    `irish.MissingSlot` for an unsupplied slot. `table` is accepted for signature parity
    with `irish.build_construction`; the grapheme grammar does not consult it."""
    if trace is None:
        trace = []
    stems = {arg: _resolve_marker(stem, oi, trace) for arg, stem in slots.items()}
    return _OiBuilder(name, stems, oi, trace).build()


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
    """The Old Irish `run_entry` (O-9): fork each slot's entry, build the template, assemble.
    `slots` defaults to `{head: entry}` — the template's first argument slot (I-16), as in
    `pipeline.run_entry`; a multi-slot template (ADJ, OF, COMPOUND, COLOUR) needs them
    supplied and raises `MissingSlot` otherwise. Flags, assumptions and traces are the union
    over the slots used, in template order."""
    name, slot = parse_construction(construction)
    if name not in oi.templates:                                # O-17
        raise ConstructionNotInStrand(f"{oi.path}: no template for {name!r} in this strand "
                                      f"(have: {', '.join(sorted(oi.templates))})")
    if lexicon is None:
        lexicon = _default_lexicon()
    items = oi.templates[name]
    if slots is None:
        head = _head_name(items)
        slots = {head: entry} if head is not None else {}
    used = [arg for arg in _template_args(items) if arg in slots]
    stems = {arg: to_old_irish(slots[arg], lexicon, oi, irish, table) for arg in used}
    assumptions: list[str] = []
    flags: list[str] = []
    trace: list[TraceEntry] = []
    for arg in used:
        stem = stems[arg]
        for tag in (*slots[arg].assumptions, *stem.assumptions):
            if tag not in assumptions:
                assumptions.append(tag)
        for flag in (stem.flag, *stem.engine_flags):
            if flag not in flags:
                flags.append(flag)
        trace.extend(stem.trace)
    if slot is not None:
        epithet = resolve_epithet(oi, slot)
        if epithet is not None:
            raise PipelineError(f"{oi.path}: [meta] epithet-{slot} = {epithet}, but this "
                                "strand's grammar is on graphemes and has no epithet affixation")
        assumptions.append(f"epithet:{slot}-unmapped-in-{oi.meta.get('name', oi.path)}")
    words = build_oi_construction(name, stems, oi, table, trace=trace)
    return adapt_oi(words, oi, table, assumptions=assumptions, flags=flags, trace=trace)


def _template_args(items: tuple[TemplateItem, ...]) -> list[str]:
    """The argument slots a template names, in order, without repeats."""
    out: list[str] = []
    for item in items:
        node: TemplateItem | None = item
        while node is not None:
            if node.kind == "arg" and node.value not in out:
                out.append(node.value)
            node = node.child
    return out
