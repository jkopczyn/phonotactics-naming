"""Irish source-side pre-pass: mutations and inflections (plan Task 17; spec §3, §4.1, §12.J).

`irish.rules` carries the lenition / eclipsis / prothesis tables under `[mutations]` and the
named regular inflections under `[inflect]` (I-15 sub-tables). Both hold ordinary rewrite
rules, but they are run differently:

- A **mutation** is one phoneme -> phoneme table (digest §3.1, §3.2): the whole table is
  applied in a single simultaneous pass against the pre-mutation word, and a span rewritten
  by one rule is never re-matched by a later rule of the same table. Sequential application
  would feed `pˠ -> fˠ` into `fˠ -> 0` and `pˠ -> bˠ` into `bˠ -> mˠ`. Where two rules of a
  table both match the same span, the earlier rule in file order wins.
- An **inflection** is a short derivation (slenderize the final, then change the vowel, then
  add an ending): its rules apply in file order, each seeing the previous rule's output,
  exactly as any rewrite section does.
- `normalize()` (Task 19, spec §4.1) runs the `[normalize]` section as an ordinary rewrite
  section (aliases, `h -> ç`, quality inference over `UNMARKED`), then records Connacht
  initial stress. Stress is kept as a pending SEGMENT index (S1): `Word.stress` is a
  syllable index and only `syllabify()` can set it.

`build_construction()` (Task 18, spec §3 `[templates]`, I-16) assembles a construction from
`Entry` slots. Each slot is tokenized and run through the `[normalize]` rewrites first (so a
user transcription with `ɑː` or a quality-less final consonant behaves like a canonical one),
the template's functions are applied, and the finished item is normalized again as a
standalone word before it is joined: the `h -> ç / # _` allophony of *a Sheáin* /ə çaːnʲ/
has to see the name's own word edge, which the `$` join hides. Stress is not set here —
`normalize()` in the pipeline does that on the joined words.

Template function semantics (plan Task 18):
- `LEN/ECL/HPREF/TPREF(x)`   -> `apply_mutation`.
- `GEN_M1/GEN_ACH/GEN_F2/GEN_M3/VOC_M1(x)` -> `apply_inflection`.
- `GEN(x)`   uses `x`'s supplied `Entry.gen_ipa` when it is non-empty (spec §5: an irregular
  genitive is user data, never regularized away), run through the `[normalize]` rewrites like
  any slot; otherwise it dispatches on `x`'s declension (I-38): m1/ach/f2/m3 -> the named
  inflection, d4 -> identity; a missing declension takes GEN_M1 with a trace note.
- A bare function (`VOC_M1?`) applies to the word assembled so far (since the last `" "`),
  which ends in the head; `?` = only when the head's declension equals the function's tag.
- `LEN_IF_F(x)` lenites iff the construction's head (its first slot) is feminine
  (digest §3.6: *Máire Bhán*, *Pádraig Rua*).
- `ART(x)` prefixes the definite article and applies its mutation (digest §3.3, §3.4):
  masculine genitive and feminine nominative lenite, a following coronal blocks that and
  /s ʃ/ take t-prefixation instead; a masculine nominative vowel-initial noun takes
  t-prothesis; the feminine genitive article is *na* /n̪ˠə/ with h-prothesis (*na hoíche*).
  *an* is /ə n̪ˠ/ before a broad consonant or non-front vowel, /ə nʲ/ otherwise (digest §3.1:
  *an tsolais* /ə(n̪ˠ) t̪ˠ.../, *an tSín* /ə(nʲ) tʲ.../). The case is genitive iff the argument
  went through a GEN function.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import TYPE_CHECKING

from .dsl import Rule, RuleFile, TemplateItem
from .features import FeatureTable
from .rewrite import _replacement, apply_section, find_matches
from .tokenize import tokenize
from .word import TraceEntry, Word

if TYPE_CHECKING:  # inputs.py imports apply_inflection from here
    from .inputs import Entry

__all__ = [
    "IrishError",
    "MissingSlot",
    "apply_mutation",
    "apply_inflection",
    "normalize",
    "build_construction",
    "MUTATIONS",
    "INFLECTIONS",
    "UNSTRESSED_DIALECTS",
]

STAGE = "irish"
MUTATIONS = ("LEN", "ECL", "HPREF", "TPREF")
INFLECTIONS = ("GEN_M1", "GEN_ACH", "GEN_F2", "GEN_M3", "VOC_M1")
# Spec §9 row 19: Munster / Ulster rows pass through unstressed; every other dialect
# value ("C", the test-words "std", or empty) gets Connacht initial stress (digest §4.1).
UNSTRESSED_DIALECTS = frozenset({"M", "U"})


class IrishError(Exception):
    """An Irish operation cannot run: the rule file has no sub-table or template of that
    name, or a template item cannot be evaluated."""


class MissingSlot(IrishError):
    """A template argument the construction needs was not supplied."""


def _subtable(
    kind: str, tables: dict[str, tuple[Rule, ...]], name: str, rf: RuleFile
) -> tuple[Rule, ...]:
    try:
        return tables[name]
    except KeyError:
        raise IrishError(
            f"{rf.path}: no [{kind}] sub-table {name!r} "
            f"(have: {', '.join(sorted(tables)) or 'none'})"
        ) from None


def _apply_table(word: Word, rules: tuple[Rule, ...], rf: RuleFile, table: FeatureTable) -> Word:
    """One simultaneous pass over `word` with every rule of a mutation table (see module
    docstring). Edits are collected against the pre-table word; an edit whose span overlaps
    an already-claimed span is dropped (first rule in file order wins). A zero-width
    (epenthesis) edit at a position inside or at the edge of a claimed span is also dropped,
    so a prothesis rule never fires on a word whose initial was just rewritten. One trace
    entry per rule that contributed, all recording the same before/after pair."""
    claimed: list[tuple[int, int]] = []
    edits: list[tuple[int, int, tuple[str, ...], Rule]] = []
    for rule in rules:
        for start, stop, caps in find_matches(word, rule, rf, table):
            new = _replacement(word, rule, start, stop, caps, table)
            if new == word.segments[start:stop]:
                continue
            if any(start <= b and a <= stop for a, b in claimed):
                continue
            claimed.append((start, stop))
            edits.append((start, stop, new, rule))
    if not edits:
        return word
    before = word.ipa()
    out = word
    for start, stop, new, _ in sorted(edits, key=lambda e: e[0], reverse=True):
        out = out.replaced(start, stop, new)
    after = out.ipa()
    fired = []
    for rule in rules:  # file order, one entry per contributing rule
        if any(e[3] is rule for e in edits) and rule not in fired:
            fired.append(rule)
    for rule in fired:
        out = out.traced(
            TraceEntry(stage=STAGE, rule_id=rule.rule_id, tag=rule.tag, before=before, after=after)
        )
    return out


def apply_mutation(word: Word, name: str, rf: RuleFile, table: FeatureTable) -> Word:
    """name in {'LEN','ECL','HPREF','TPREF'} (digest §3.1–§3.3)."""
    return _apply_table(word, _subtable("mutations", rf.mutations, name, rf), rf, table)


def apply_inflection(word: Word, name: str, rf: RuleFile, table: FeatureTable) -> Word:
    """name in {'GEN_M1','GEN_ACH','GEN_F2','GEN_M3','VOC_M1'} — five, not the four named in
    spec §3; spec §12.J sanctions the superset (digest §3.5)."""
    return apply_section(word, _subtable("inflect", rf.inflect, name, rf), rf, table, STAGE)


def normalize(word: Word, rf: RuleFile, table: FeatureTable, *, dialect: str = "C") -> Word:
    """Spec §4.1: fold input aliases; give every quality-unmarked consonant ʲ or ˠ from
    the adjacent-vowel convention; mark Connacht initial stress; leave user-supplied
    phonemes untouched.

    The rewrite part is `irish.rules [normalize]` (applied in file order). Stress: when
    `dialect` is not Munster/Ulster and the input carried no `ˈ` (no pending segment index
    and no syllable index), the first segment becomes the pending stress (S1), with a trace
    entry `stress:irish-initial` (digest §4.1). An explicit mark is always kept."""
    out = apply_section(word, rf.sections.get("normalize", ()), rf, table, STAGE)
    if dialect in UNSTRESSED_DIALECTS or not out.segments:
        return out
    if out._pending_stress is not None or out.stress is not None:
        return out
    before = out.ipa()
    out = replace(out, _pending_stress=0)
    return out.traced(
        TraceEntry(
            stage=STAGE,
            rule_id="stress:irish-initial",
            tag="attested",
            before=before,
            after=out.ipa(),
            note=f"Connacht initial stress (digest §4.1), dialect={dialect}",
        )
    )


# ---- templates (Task 18) ---------------------------------------------------------------------

_GEN_BY_DECLENSION = {"m1": "GEN_M1", "ach": "GEN_ACH", "f2": "GEN_F2", "m3": "GEN_M3", "d4": None}
_GEN_FUNCS = frozenset({"GEN", "GEN_M1", "GEN_ACH", "GEN_F2", "GEN_M3"})
_DECLENSION_TAGS = ("M1", "ACH", "F2", "M3", "D4")
_SIBILANTS = ("sˠ", "ʃ")


@dataclass(frozen=True)
class _Val:
    """An evaluated template item: its segments as a Word, the Entry whose gender /
    declension tags it carries (None for a literal), and whether it is in the genitive."""

    word: Word
    entry: Entry | None = None
    genitive: bool = False


def _normalize_rewrites(word: Word, rf: RuleFile, table: FeatureTable) -> Word:
    return apply_section(word, rf.sections.get("normalize", ()), rf, table, STAGE)


def _join(a: Word, b: Word) -> Word:
    """`a $ b`: segments concatenated with a morpheme boundary at the seam; b's own
    boundaries (morpheme AND word, spec §3), secondary marks and trace shifted / appended.
    A pending stress on `a` wins."""
    n = len(a.segments)
    if not a.segments:
        return b
    if not b.segments:
        return a
    pending = a._pending_stress
    if pending is None and b._pending_stress is not None:
        pending = b._pending_stress + n
    orth: tuple[str, ...] = ()
    if a.orth or b.orth:  # R7: the orth channel survives a join; an
        orth = (
            (a.orth or ("",) * n)  # untagged side is padded with "" so the
            + (b.orth or ("",) * len(b.segments))
        )  # channel stays segment-length
    return Word(
        segments=a.segments + b.segments,
        orth=orth,
        morphemes=a.morphemes | {n} | frozenset(n + m for m in b.morphemes if m != 0),
        word_breaks=a.word_breaks | frozenset(n + i for i in b.word_breaks),
        flags=a.flags + tuple(f for f in b.flags if f not in a.flags),
        trace=a.trace + b.trace,
        secondary=a.secondary + tuple(n + i for i in b.secondary),
        _pending_stress=pending,
    )


def _head_name(items: tuple[TemplateItem, ...]) -> str | None:
    """The construction's head = the first argument slot in the template (I-16)."""

    def walk(item: TemplateItem) -> str | None:
        if item.kind == "arg":
            return item.value
        return walk(item.child) if item.child is not None else None

    for item in items:
        found = walk(item)
        if found is not None:
            return found
    return None


def _condition_holds(item: TemplateItem, head: Entry | None, name: str, rf: RuleFile) -> bool:
    """`FUNC_M1?`: the suffix after the last `_` is a declension tag; the item applies only
    when the head carries that declension (I-16 / R1)."""
    tag = item.value.rpartition("_")[2].upper() if item.kind == "call" else ""
    if tag not in _DECLENSION_TAGS:
        raise IrishError(
            f"{rf.path}: template {name}: conditional item {item.value!r}? "
            f"has no declension tag (one of {', '.join(_DECLENSION_TAGS)})"
        )
    if head is None:
        raise IrishError(
            f"{rf.path}: template {name}: conditional item {item.value!r}? "
            "but the template has no head slot"
        )
    return (head.declension or "").lower() == tag.lower()


def _apply_gen(val: _Val, rf: RuleFile, table: FeatureTable) -> _Val:
    """GEN(): a supplied `gen_ipa` wins (spec §5); else dispatch on the declension tag
    (I-38); missing -> GEN_M1 with a note."""
    decl = (val.entry.declension if val.entry is not None else "") or ""
    word = val.word
    supplied = val.entry.gen_ipa if val.entry is not None else ""
    if supplied:
        before = word.ipa()
        gen = Word.from_tokenized(tokenize(supplied, table))
        gen = _normalize_rewrites(replace(gen, trace=word.trace, flags=word.flags), rf, table)
        word = gen.traced(
            TraceEntry(
                stage=STAGE,
                rule_id="templates:GEN",
                tag="attested",
                before=before,
                after=gen.ipa(),
                note="supplied gen_ipa used (spec §5), not derived",
            )
        )
    elif decl not in _GEN_BY_DECLENSION:
        inflection = "GEN_M1"
        before = word.ipa()
        word = apply_inflection(word, inflection, rf, table)
        word = word.traced(
            TraceEntry(
                stage=STAGE,
                rule_id="templates:GEN",
                tag="design",
                before=before,
                after=word.ipa(),
                note=f"declension {decl!r} unknown; assumed m1 (GEN_M1, I-38)",
            )
        )
    else:
        inflection = _GEN_BY_DECLENSION[decl]
        if inflection is not None:
            word = apply_inflection(word, inflection, rf, table)
    return _Val(word, val.entry, True)


def _article(val: _Val, rf: RuleFile, table: FeatureTable) -> _Val:
    """ART(x): see the module docstring. Returns `article $ mutated-noun`."""
    gender = (val.entry.gender if val.entry is not None else "m") or "m"
    noun = val.word
    if not noun.segments:
        raise IrishError(f"{rf.path}: ART() of an empty word")
    first = noun.segments[0]
    vowel_initial = table.value(first, "syllabic") == "+"
    feminine = gender == "f"
    if feminine and val.genitive:  # *na hoíche* (digest §3.3, §6 row 9)
        art_segments: tuple[str, ...] = ("n̪ˠ", "ə")
        if vowel_initial:
            noun = apply_mutation(noun, "HPREF", rf, table)
    else:
        lenites = val.genitive != feminine  # masc. gen. or fem. nom. (digest §3.4)
        if lenites:
            if first in _SIBILANTS:  # *an tsolais*, *an tSín* (digest §3.1)
                noun = apply_mutation(noun, "TPREF", rf, table)
            elif not vowel_initial and table.value(first, "coronal") != "+":
                noun = apply_mutation(noun, "LEN", rf, table)
            # a coronal blocks lenition (*an deoch*, *an tí*); a vowel takes nothing
        elif vowel_initial:  # masc. nom.: *an t-éan* (digest §3.3)
            noun = apply_mutation(noun, "TPREF", rf, table)
        first = noun.segments[0]
        slender = first in rf.classes.get("SLEN", ()) or (
            table.value(first, "syllabic") == "+" and table.value(first, "front") == "+"
        )
        art_segments = ("ə", "nʲ" if slender else "n̪ˠ")
    before = noun.ipa()
    out = _join(Word(segments=art_segments), noun)
    out = out.traced(
        TraceEntry(
            stage=STAGE,
            rule_id="templates:ART",
            tag="attested",
            before=before,
            after=out.ipa(),
            note=f"article, gender={gender}, case={'gen' if val.genitive else 'nom'} (digest §3.4)",
        )
    )
    return _Val(out, val.entry, val.genitive)


class _Builder:
    def __init__(
        self, name: str, slots: dict[str, Entry], rf: RuleFile, table: FeatureTable
    ) -> None:
        self.name, self.slots, self.rf, self.table = name, slots, rf, table
        try:
            self.items = rf.templates[name]
        except KeyError:
            raise IrishError(
                f"{rf.path}: no [templates] entry {name!r} "
                f"(have: {', '.join(sorted(rf.templates)) or 'none'})"
            ) from None
        head = _head_name(self.items)
        self.head: Entry | None = self.slot(head) if head is not None else None

    def slot(self, arg: str) -> Entry:
        try:
            return self.slots[arg]
        except KeyError:
            raise MissingSlot(
                f"template {self.name} needs slot {arg!r} "
                f"(given: {', '.join(sorted(self.slots)) or 'none'})"
            ) from None

    def evaluate(self, item: TemplateItem) -> _Val:
        """A literal or a slot, or a function of one; never a bare function (those act on
        the word under construction, see `build`)."""
        if item.kind == "literal":
            return _Val(Word(segments=tuple(tokenize(item.value.strip(), self.table).segments)))
        if item.kind == "arg":
            e = self.slot(item.value)
            word = Word.from_tokenized(tokenize(e.ipa, self.table))
            return _Val(_normalize_rewrites(word, self.rf, self.table), e)
        if item.child is None:
            raise IrishError(
                f"{self.rf.path}: template {self.name}: bare {item.value} may not be nested"
            )
        return self.call(item.value, self.evaluate(item.child))

    def call(self, func: str, val: _Val) -> _Val:
        rf, table = self.rf, self.table
        if func in MUTATIONS:
            return _Val(apply_mutation(val.word, func, rf, table), val.entry, val.genitive)
        if func in INFLECTIONS:
            return _Val(
                apply_inflection(val.word, func, rf, table),
                val.entry,
                val.genitive or func in _GEN_FUNCS,
            )
        if func == "GEN":
            return _apply_gen(val, rf, table)
        if func == "LEN_IF_F":
            if self.head is not None and self.head.gender == "f":
                return _Val(apply_mutation(val.word, "LEN", rf, table), val.entry, val.genitive)
            return val
        if func == "ART":
            return _article(val, rf, table)
        raise IrishError(f"{rf.path}: template {self.name}: unknown function {func!r}")

    def build(self) -> list[Word]:
        words: list[Word] = []
        current = Word(segments=())
        for item in self.items:
            if item.conditional and not _condition_holds(item, self.head, self.name, self.rf):
                continue
            if item.kind == "literal" and not item.value.strip():  # " " = word separator
                if current.segments:
                    words.extend(current.split_words())
                current = Word(segments=())
                continue
            if item.kind == "call" and item.child is None:
                current = self.call(item.value, _Val(current, self.head)).word
                continue
            val = self.evaluate(item)
            word = val.word
            if item.kind != "literal":
                word = _normalize_rewrites(word, self.rf, self.table)
            current = _join(current, word)
        if current.segments:
            words.extend(current.split_words())
        joined = " ".join(w.ipa() for w in words)
        return [
            w.traced(
                TraceEntry(
                    stage=STAGE,
                    rule_id=f"templates:{self.name}",
                    tag="",
                    before="",
                    after=joined,
                    note=f"construction {self.name}, word {i + 1} of {len(words)}",
                )
            )
            for i, w in enumerate(words)
        ]


def build_construction(
    name: str, slots: dict[str, Entry], rf: RuleFile, table: FeatureTable
) -> list[Word]:
    """Apply rf.templates[name]; one Word per space-separated word (I-16) — both the `" "`
    separators written in the template and any spaces inside a slot's own IPA (*an tsúil*
    /ən̪ˠ t̪ˠuːlʲ/, spec §3). The construction is assembled and mutated as ONE object, so a
    mutation still reaches across a boundary; `Word.split_words()` takes it apart at the end,
    and stages 2-7 then run per word.
    Raises MissingSlot when a required slot is absent; IrishError for an unknown template."""
    return _Builder(name, slots, rf, table).build()
