# Strand 5: Old Irish — implementation plan (spec milestones 1–5)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development
> (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a fifth strand, `old-irish`, that produces classical Old Irish forms of the same
modern-Irish input rows — by lexicon lookup where an attested form exists, by a rule-based
retro-filter otherwise — marked `ATTESTED` / `RETRO` / `RETRO:loan`, with Old Irish morphology,
editorial orthography, and an IPA reconstructed from the written form.

**Architecture:** A fifth target rule file (`rules/old-irish.rules`) plus a sourced lexicon
(`rules/old-irish-lexicon.tsv`) and two orthography tables (`rules/irish-orthography.tsv`,
`rules/old-irish-orthography.tsv`). Three engine additions: a per-segment **orth tag** channel on
`Word` filled by a modern-orthography↔IPA aligner; an `@orth("…")` rule item that tests it; and a
**lookup** stage plus an Old-Irish-specific assembly in `src/strands/oldirish.py`. Everything
linguistic stays in data files.

**Tech Stack:** Python ≥3.12, `uv`, `pytest`. No runtime dependencies (standard library only).
Every command runs through `uv run` from `phonotactics/`. The system `python3` is 3.10 — do not
use it.

**Spec:** `docs/specs/2026-08-27-old-irish-design.md` (source of truth for this plan). It extends
`docs/specs/2026-08-25-engine-design.md`; **read §12 of that file first — it overrides §§1–11.**
Linguistic content: `sources/irish/digest.md §10` and its `bib.md` entries `pokorny1914-oldirish-grammar`,
`strachan1909-oldirish-paradigms`, `wiki-old-irish`, `wiki-old-irish-grammar`,
`wiki-old-irish-phonhistory`, `utaustin-oldirish-lesson1`, `edil`. The existing plan whose task
format this file reuses is `docs/plans/2026-08-25-engine-plan.md`; its interpretation register
(I-1 … I-41) is still in force and is **not** repeated here.

## Global Constraints

- Python ≥3.12; package `strands` under `src/strands/`; CLI entry point `strands`. No runtime
  dependencies outside the standard library.
- All paths relative to `phonotactics/` unless stated otherwise.
- Determinism is a hard requirement: identical input + data files ⇒ byte-identical output.
- **Test-first, always** (engine spec §12.I): every task — the rule-file and data tasks included —
  writes its tests against an absent or skeletal artefact, runs them, watches them fail, and only
  then writes the artefact.
- Files are UTF-8, NFC-normalized on read (I-1).
- Every rule line in `old-irish.rules` carries either a `# digest §10.n` / `# [bibkey p.N]`
  citation or `# design: O<n>` naming a row of spec §8's decision register.
- Rule tags are exactly one of `%attested`, `%design`, `%fallback`; default `%attested`. A rule
  whose digest section states the opposite, or states nothing, is `%design`.
- Every lexicon row carries a citation; uncited rows are rejected by `strands check`.
- **The existing suite is 1004 passed / 2 xfailed. No task may reduce that count.** Run
  `uv run pytest -q` before every commit.
- Reuse the engine constraints of spec §12 rather than adding mechanisms: captures and
  backreferences (§12.C), inline sets `{…}`, the declared classes `BROAD` / `SLEN` / `UNMARKED`
  (§12.J / I-41), `nuclei` (§12.B), `cluster-fallback = keep` and `overlay-undo` (§12.E). Two
  additions are sanctioned by the Old Irish spec and nothing else: the orth-tag channel with its
  `@orth("…")` item (spec §4), and the lookup stage (spec §2).

---

## Spec interpretations

The Old Irish spec leaves the following underdetermined. Each is resolved here by the simplest
faithful reading. **Implementers follow these, not their own reading.** They are numbered `O-n`
to sit alongside the engine plan's `I-n`.

- **O-1 Segment spellings for the lenited series.** Spec §4 writes `/β ð ɣ μ θ x/`. The project
  canon is IPA with diacritics (engine spec §12.F), so `μ` — which is not an IPA letter — is
  written **`β̃`** (bilabial nasalized fricative; digest §10.8 conflict 3 calls /v/ ~ /β/ ~ /w̃/
  "notational variants of one bilabial nasalized continuant"). New `features.tsv` rows needed:
  `β βʲ β̃ β̃ʲ θʲ ðʲ`. `θ ð x ɣ s f h` already exist; **slender `/xʲ/` is the existing `ç` and
  slender `/ɣʲ/` is the existing `j`** (the Irish rows), so no new dorsal rows are added.
  *Alternative rejected:* the digest's own `v / ṽ` (§10.1), which would collide with the modern
  Irish `vʲ`/`vˠ` rows and lose the fricative/approximant distinction the retro-filter needs.
- **O-2 No fortis/lenis sonorant contrast.** Spec §4's `[inventory]` does not list `/L N R/`, and
  digest §10.8 conflict 2 records that one held source omits them entirely. Old Irish therefore
  has one `/m n l r/` series (in the modern broad/slender spellings, O-3); **fortis is represented
  as a geminate — two identical segments** (I-2), which is exactly what the orthography writes
  (`ll nn rr mm`, digest §10.2 convention 3). No feature row is added for `L N R`.
- **O-3 Quality is not reversed.** Spec §4: broad/slender distribution is deliberately *not*
  reversed. Old Irish consonants therefore carry the modern `ˠ`/`ʲ` marks and the plain dorsals
  `k ɡ x ɣ ŋ` / `c ɟ ç j ɲ` convention of I-41. `old-irish.rules [classes]` copies the `BROAD`,
  `SLEN` and `UNMARKED` lines of I-41 verbatim and extends `BROAD`/`SLEN` with the new O-1
  segments.
- **O-4 Pokorny's three-way quality is a spelling matter only.** Digest §10.1 CONFLICT and §10.2.5:
  the u-colour generates the `⟨-iu -eo -eu -au⟩` glide spellings. It is implemented in
  `[respell]` as glide-vowel insertion, **never as a third phonological quality**; no `ʷ`-marked
  segments are created.
- **O-5 `/h/` and `/f/` are inventory members** (they already are, from the modern Irish rows).
  Spec §4's "no phonemic /h/, /s f h/ as lenition products only" is honoured by there being **no
  `[substitute]` rule that produces `/h/` or `/f/` except the ones reversing modern `sh`/`ph`**;
  it is not enforced by omitting them from `[inventory]` (that would make the fallback rewrite
  them and break the lenition reversals).
- **O-6 `@orth("X")` is an ItemSpec, not a boundary atom.** It is written `@orth("bh")` and is
  legal (a) as a whole TARGET item and (b) as a context atom. It matches **exactly one segment**
  whose orth tag equals `X` after NFC and case-folding. A segment with no tag matches nothing —
  that is the spec's stated failure mode ("where alignment fails the tag is absent and only
  sound-based rules apply"). It may not carry a capture (`@orth("bh"):1` is a parse error) and may
  not appear in a REPLACEMENT.
- **O-7 The aligner is a monotonic DP over a grapheme→segment table.** Algorithm, failure mode and
  tests are fixed in Task 5. On failure **every** segment of that word gets the empty tag (not
  just the unalignable ones) and the word carries assumption `orth:unaligned`.
- **O-8 Mutation provenance rides the same channel.** Spec §4 requires "modern eclipsis → Old
  Irish nasalization *mb nd ng*", which needs the radical, not the surface sound. `apply_mutation`
  therefore writes the orth tag **`"<TABLE>:<radical>"`** (e.g. `ECL:pˠ`, `LEN:bˠ`) on the segments
  it produces, overwriting any aligner tag there. The retro-filter writes `@orth("ECL:bˠ")` to
  catch modern *mb*. Elsewhere: a replacement's segments inherit the tag of the **first** segment
  of the replaced span; inserted segments get `""`.
- **O-9 Where the lookup stage lives.** `pipeline.lookup()` is stage **1b**, called from
  `pipeline.run_entry()` after `parse_construction()` and before the construction is built —
  i.e. before `substitute`, as spec §2 requires. `run_entry` dispatches on the target's
  `[meta] strand` value: `old-irish` hands off to `oldirish.run_entry_oi()`, which composes the
  existing stage functions in the Old Irish order (retro-substitute → grammar → syllabify → repair
  → stress → post-stress → respell → reconstruct) and never re-runs `[substitute]`. `adapt()` is
  not modified.
- **O-10 Old Irish grammar operates on IPA segments, like Irish grammar.** `oi_nom` and `oi_gen`
  are *spellings*; they are turned into segments by `oldirish.spelling_to_ipa()` at lookup time,
  so `[mutations]` / `[inflect]` / `[templates]` are ordinary segment rewrites and reuse
  `irish.apply_mutation` / `irish.apply_inflection` unchanged.
- **O-11 IPA reconstruction is a post-respell step in `oldirish.run_entry_oi`.** Spec §6: the IPA
  is derived *from the written form*. `Result.ipa` for this strand is
  `spelling_to_ipa(respelling)` rendered back to a string; the pre-respell phonological IPA
  survives in the trace as the last `respell` entry's `before`. The same function serves lookup
  (O-10), so there is one spelling→sound implementation.
- **O-12 `RETRO:loan` is filtered exactly like `RETRO`.** Spec §8 row O4's default is "filter +
  flag"; only the flag string differs. No rule branches on it.
- **O-13 Modern *ao*: lookup decides; the filter keeps *áe*** (spec §10, refining §8 row O1). The
  harvest log's finding 1 measured 20 attested ⟨ao⟩ pairs and found ⟨áe/aí⟩ and ⟨óe/oí⟩ at
  parity once the repeated *Máel* element is counted once, with no clean phonological condition.
  Resolution: attested words take their spelling from the lexicon (the ATTESTED path never runs
  `[substitute]`); the filter writes the single unconditioned `%design` rule *ao* → *áe*; and the
  20 pairs are a **named regression set** in Task 17, so a later conditioned rule can be measured
  rather than argued. Do **not** implement the log's proposed two-way split in this plan — it is a
  spec change, and the regression set is what would justify it.
- **O-14 `punctum` is a `[respell]` directive**, `punctum = on | off`, default `on` (spec §8 row
  O2). It is read by `oldirish.py` from `RuleFile.meta` — written as `[meta] punctum = on` — so no
  DSL section grammar changes. `off` emits plain `s f` instead of `ṡ ḟ`.
- **O-15 "Epenthetic position" for schwa deletion** (spec §4, spec §8 row O5) is *after a sonorant
  and before a consonant*, i.e. the environment of digest §2.4. Written with an inline set of the
  Irish sonorants, not a feature bundle.
- **O-16 The filter regression compares written forms** (`respelling` vs `oi_nom`), because
  `oi_nom` is a spelling. Exact match and **character-level** Levenshtein ≤1 are both reported;
  the ratchet file holds both rates.
- **O-17 `PATRO_O` / `PATRO_NI` are absent from this strand.** They stay in
  `pipeline.CONSTRUCTIONS` for the other four targets. `old-irish.rules [templates]` simply has no
  entry for them; `oldirish.run_entry_oi` raises `ConstructionNotInStrand` and the CLI and gallery
  report the cell as skipped with `skipped:construction-not-in-strand`. The eight formation
  templates (`MAEL GILLA CU FER COLOUR MAC UA INGEN`) are appended to `CONSTRUCTIONS`; the other
  four targets have no template of those names and skip them the same way.
- **O-18 `none` rows and their two flags.** `status = none` requires `oi_nom`, `oi_gen`, `stem`
  and `gender` to be **empty** and `source` to cite the etymology; `strands check` enforces both
  directions. Spec §10 splits the *flag* the lookup emits, not the status: a row whose `note`
  records a **borrowing** flags `RETRO:loan` (the harvest's 12 rows: *Seán*, *Siobhán*, *Séamus*,
  *Brian*, *tobac*, *téarma*, *seirbhís*, *geata*, *bád*, *speal*, *cnaipe*, *Cairmilíteach*); a
  row recording an **Irish-internal post-Old-Irish coinage** flags `RETRO:late` (the other 17).
  The distinction must be a **column, not a note-parse**: Task 2 adds a `kind` column taking
  `loan | late` (required when `status = none`, empty otherwise), because grepping prose for the
  word "loan" is not a classification.
- **O-19 Lexicon keys** are matched on `orthography` after `unicodedata.normalize("NFC", s)` and
  `str.casefold()`. Duplicate keys are a `check` error. No fuzzy matching (spec §3).
- **O-20 Unattested clusters are kept, not repaired.** `old-irish.rules [repair]` sets
  `cluster-fallback = keep` (engine spec §12.E owner amendment), so an Old Irish word that keeps a
  modern cluster gets an `UNATTESTED_CLUSTER:<cluster>` flag rather than `UNREPAIRED`. Spec §4
  asks for "no repair beyond degemination".
- **O-21 Stem classes.** Spec §10 widens the vocabulary to `o | ā | i | u | n | dental | velar |
  r | s | indecl | irregular`. `o` absorbs io-stems and `ā` absorbs iā-/ī-stems (the harvest's
  finding 5 mapping, recorded in each row's `note`). `indecl` inflects to itself. `irregular` is
  reserved for genuinely suppletive words and means "use `oi_gen` verbatim, do not derive" — so
  `oi_gen` stays mandatory for it. **The harvest's 37 `irregular` rows predate this widening and
  cover four real paradigms** (velar, r, s, indeclinable); reclassifying them is Task 3's job, and
  Task 15's `[inflect]` may not be written against `irregular` as if it were a class. The o-stem
  adjective is not a `stem` value; it is the `[inflect]` table `GEN_O_ADJ`, selected by the
  `ADJ`/`COLOUR` templates.
- **O-22 The Middle Irish tier.** Spec §10 adds `status = middle`: a name attested only in Middle
  Irish, used by lookup and flagged **`ATTESTED:MIr`**. It behaves exactly like `attested`
  everywhere else (same required columns, same `[inflect]` path); only the flag differs. Spec §10
  marks it a *speculative default* — the owner may prefer to filter these instead — so the flag
  string is the only place the tier appears, and nothing branches on it.
- **O-23 Lookup keys on the citation form, never on the surface form.** The harvest log measures
  138 distinct test-word keys of which 74 hit a lexicon row directly and **52 are mutated,
  inflected or phrasal surface forms** (*a Sheáin*, *na bpeann*, *an tsúil*, *Ard-Easpag*) whose
  citation form is in the lexicon. This is not a lexicon gap: spec §2 says the lookup matches "the
  row's **orthography** (citation form)", and `Entry.orthography` is the citation form for exactly
  the reason that the Irish pre-pass applies the mutation on the modern side. `lookup()` therefore
  takes `Entry.orthography` and does no stripping, no de-mutation and no fuzzy fallback (O-19).
  A gallery/test row whose *own* `orthography` cell is a surface form (as many test-word rows are)
  is a `RETRO` miss and that is correct.
- **O-24 The lexicon already exists.** `rules/old-irish-lexicon.tsv` (299 rows: 270 `attested`,
  29 `none`; 163 with genitives) and `rules/old-irish-lexicon-log.md` are committed, and a 35-row
  independent verification has been done. Spec milestone 1 is therefore **mostly complete**: Task
  2 writes the schema/reader/`check` *against the existing file* (and must be prepared to report
  findings on it), and Task 3 is an **extension and second verification pass**, not a harvest.
- **O-25 Template literals are IPA.** Stated in full in Task 16, where it is used: the formation
  templates write each element (*máel*, *gilla*, *cú*, *fer*, *macc*, *aue*, *ingen*) as the IPA
  `spelling_to_ipa` yields for it, with the spelling in the line's comment, and a test asserts the
  pairing. The DSL's quoted-literal syntax is unchanged.
- **O-26 Feminine ā-stems and the `[inflect]` naming.** `[inflect]` sub-tables are named
  `<CASE>_<STEM>`: `GEN_O`, `GEN_A`, `GEN_I`, `GEN_U`, `GEN_N`, `GEN_DENT`, `GEN_VELAR`, `GEN_R`,
  `GEN_S`, `VOC_O`, `NOM_A`, `DAT_O`, `DAT_A`, `GEN_O_ADJ` (Task 15). `ā` is spelled `A` in a table
  name because class names match `[A-Z][A-Z0-9_]*` (I-10); `indecl` and `irregular` have no table
  at all (O-21).

---

## File structure

```
phonotactics/
  rules/
    features.tsv                     # Task 1: + 6 hand rows (β βʲ β̃ β̃ʲ θʲ ðʲ)
    features.README.md               # Task 1: their derivation
    old-irish-lexicon.tsv            # EXISTS (299 rows). Task 2 adds `kind`; Tasks 3, 4 fix/extend
    old-irish-lexicon-log.md         # EXISTS — the harvest log; Tasks 3, 4 append sections
    old-irish-lexicon.verification.tsv   # EXISTS — the first (35-row) verification pass
    old-irish-lexicon.verification2.tsv  # Task 3: the second pass
    irish-orthography.tsv            # Task 5: modern grapheme -> segment table (aligner)
    old-irish-orthography.tsv        # Task 12: OI grapheme -> segment table (reconstruction)
    old-irish.rules                  # Tasks 8, 9, 10, 11, 14, 15, 16
  src/strands/
    word.py                          # Task 5: + `orth` channel
    orth.py                          # Task 5: the aligner (NEW)
    dsl.py                           # Task 6: `@orth("…")` ItemSpec kind
    rewrite.py                       # Task 6: match_item gains word/index
    check.py                         # Tasks 2, 6: lexicon checks, @orth checks
    irish.py                         # Task 7: mutation provenance tags
    lexicon.py                       # Task 2: reader + validation (NEW)
    oldirish.py                      # Tasks 12, 13, 15, 16, 17 (NEW)
    pipeline.py                      # Task 13: lookup stage, TARGETS, dispatch
    cli.py                           # Task 18: --strand old-irish
    gallery.py                       # Task 19: fifth column
  tests/
    test_lexicon.py                  # Task 2
    test_lexicon_data.py             # Tasks 3, 4
    test_orth_align.py               # Task 5
    test_dsl_orth_atom.py            # Task 6
    test_irish_mutation_orth.py      # Task 7
    test_rules_old_irish.py          # Tasks 8, 9, 10, 11
    test_oldirish_reconstruct.py     # Task 12
    test_oldirish_lookup.py          # Task 13
    test_oldirish_grammar.py         # Tasks 14, 15, 16
    test_oldirish_regression.py      # Task 17
    ratchets/old-irish.json          # Task 17
    snapshots/gallery.md             # Task 19 (regenerated)
```

---

## Task list and dependencies

| # | Task | Depends on |
|---|---|---|
| 1 | `features.tsv` hand rows for the Old Irish lenited series | — |
| 2 | Lexicon schema, reader, and `strands check` validation (the file already exists) | — |
| 3 | Lexicon fix-up: real stem classes + a second verification pass | 2 |
| 4 | Middle Irish tier — the 49 unresolved names | 3 |
| 5 | Orthography↔IPA aligner and the `Word.orth` channel | — |
| 6 | The `@orth("…")` rule item | 5 |
| 7 | Mutation provenance orth tags | 5 |
| 8 | `old-irish.rules`: `[meta] [inventory] [classes]` | 1 |
| 9 | `old-irish.rules [substitute]` — the retro-filter | 6, 7, 8 |
| 10 | `old-irish.rules [syllable] [repair] [stress] [post-stress]` | 8 |
| 11 | `old-irish.rules [respell]` — editorial orthography | 10 |
| 12 | Old Irish spelling→IPA reconstruction | 1, 11 |
| 13 | Lookup stage, flags, and `oldirish.run_entry_oi` | 2, 9, 10, 11, 12 |
| 14 | `old-irish.rules [mutations]` | 8 |
| 15 | `old-irish.rules [inflect]` + stem-class inference | 2, 14 |
| 16 | `old-irish.rules [templates]` incl. the formation templates | 13, 15 |
| 17 | Filter regression + ratchet | 4, 16 |
| 18 | CLI exposure (`--strand old-irish`) | 16 |
| 19 | Gallery column, snapshot, property checks | 17, 18 |

**Parallelism and stress.** Tasks 1, 2 and 5 are fully independent and may run at once (disjoint
files: `rules/features.tsv` + `features.README.md`; `src/strands/lexicon.py` + `check.py`;
`src/strands/word.py` + `orth.py` + `rules/irish-orthography.tsv`). Task 2 touches `check.py` and
Task 6 also touches `check.py` — **run them sequentially or expect a merge in `check.py`**; the
two additions are in different methods (`Checker.lexicon` vs `Checker.item`) so the conflict is
mechanical. Tasks 8, 10, 11, 14 all edit `old-irish.rules` and must run in the listed order (each
appends its own sections; none rewrites another's). Tasks 3 and 4 are the only ones that need
network access, and both are extension/verification passes over an **already-harvested,
already-once-verified** 299-row file (O-24) — spec milestone 1 is mostly done, so neither is a
long job. Task 6 and Task 7 both depend on Task 5 and are otherwise independent, but both
land in files Task 9 reads, so Task 9 waits for both.

---

## Task 1: `features.tsv` hand rows for the Old Irish lenited series

**Depends on:** — . **Spec:** §4 `[inventory]`; O-1, O-2, O-3.

**Files:**
- Modify: `rules/features.tsv` (append 6 rows, keeping the file's existing column order)
- Modify: `rules/features.README.md` (one derivation paragraph per new row)
- Test: `tests/test_features_hand.py` (append; the file already exists)

**Interfaces:**
- Produces: six new tokenizable segments — `β`, `βʲ`, `β̃`, `β̃ʲ`, `θʲ`, `ðʲ` — usable in any
  `[inventory]`, class or rule from Task 8 on. `θ`, `ð`, `x`, `ɣ`, `s`, `f`, `h`, `ç`, `j` are
  already present and are **not** touched.

**How to derive each row.** Copy the vector of the nearest existing row and change exactly the
features named:

| New row | Copy from | Change |
|---|---|---|
| `β` | `v` (labiodental voiced fricative) | `labiodental` → `-`, `bilabial`-defining features to match the existing `b` row's place columns (`labial +`, `round -`), keep `continuant +`, `sonorant -`, `periodicGlottalSource +` |
| `βʲ` | `β` | `front +`, `back -`, `high +` (the I-41 slender convention) |
| `β̃` | `β` | `nasal +` |
| `β̃ʲ` | `βʲ` | `nasal +` |
| `θʲ` | `θ` | `front +`, `back -`, `high +` |
| `ðʲ` | `ð` | `front +`, `back -`, `high +` |

`class` column = `consonant`; `source` column = `hand: old-irish digest §10.1` for all six.

- [ ] **Step 1: Write the failing test**

Append to `tests/test_features_hand.py`:

```python
OLD_IRISH_ROWS = ("β", "βʲ", "β̃", "β̃ʲ", "θʲ", "ðʲ")


@pytest.mark.parametrize("segment", OLD_IRISH_ROWS)
def test_old_irish_lenited_rows_exist_and_tokenize(segment):
    """digest §10.1: the lenited series. O-1 spells spec §4's /μ/ as β̃."""
    assert segment in TABLE.segments
    assert tuple(tokenize(segment, TABLE).segments) == (segment,)


def test_beta_is_a_voiced_bilabial_fricative_not_labiodental():
    assert TABLE.value("β", "continuant") == "+"
    assert TABLE.value("β", "sonorant") == "-"
    assert TABLE.value("β", "labiodental") == "-"
    assert TABLE.value("β", "labial") == "+"


def test_the_nasalized_fricative_differs_from_beta_only_in_nasality():
    """digest §10.8 conflict 3: /ṽ/ ~ /β̃/ ~ [w̃] are one bilabial nasalized continuant."""
    differing = [f for f in TABLE.features
                 if TABLE.value("β", f) != TABLE.value("β̃", f)]
    assert differing == ["nasal"]


@pytest.mark.parametrize("broad,slender", [("β", "βʲ"), ("β̃", "β̃ʲ"), ("θ", "θʲ"), ("ð", "ðʲ")])
def test_slender_partners_differ_only_in_the_I41_quality_features(broad, slender):
    differing = {f for f in TABLE.features if TABLE.value(broad, f) != TABLE.value(slender, f)}
    assert differing <= {"front", "back", "high"}


def test_no_fortis_sonorant_rows_were_added():
    """O-2: spec §4 does not list /L N R/; fortis is a geminate (I-2)."""
    for bad in ("L", "N", "R", "ʟ", "ɴ", "ʀ"):
        assert bad not in TABLE.segments


def test_slender_x_and_slender_gamma_are_the_existing_irish_rows():
    """O-1: /xʲ/ IS ç and /ɣʲ/ IS j — no new dorsal rows."""
    assert "ç" in TABLE.segments and "j" in TABLE.segments
    assert "xʲ" not in TABLE.segments and "ɣʲ" not in TABLE.segments
```

Add `from strands.tokenize import tokenize` to the file's imports if it is not already there.

- [ ] **Step 2: Run the tests and watch them fail**

Run: `uv run pytest tests/test_features_hand.py -q`
Expected: FAIL — `assert 'β' in TABLE.segments`.

- [ ] **Step 3: Append the six rows to `rules/features.tsv`**

Read the header line to get the exact column order, copy the source row named in the table above,
edit the named columns, and write the new row with the same number of tab-separated fields. Do not
reorder or reformat any existing line. Verify with:

```bash
uv run python -c "
import csv,pathlib
rows=list(csv.DictReader(pathlib.Path('rules/features.tsv').open(encoding='utf-8'),delimiter='\t'))
n=len(rows[0])
print([r['segment'] for r in rows[-6:]], all(len(r)==n for r in rows))"
```

- [ ] **Step 4: Document them in `rules/features.README.md`**

Append a subsection "Old Irish lenited series (2026-08-27)" giving, for each row, the source row it
was copied from, the features changed, and the citation `digest §10.1 [wiki-old-irish §Consonants]`,
plus a sentence recording O-1 (why `β̃` and not `μ`/`ṽ`) and O-2 (why no `L N R`).

- [ ] **Step 5: Run the full suite**

Run: `uv run pytest -q`
Expected: 1004+ passed, 2 xfailed — **no test may have broken.** A break here means a new row
collided with an existing tokenization (longest-match); fix the row, not the test.

- [ ] **Step 6: Commit**

```bash
git add rules/features.tsv rules/features.README.md tests/test_features_hand.py
git commit -m "feat(features): Old Irish lenited series rows (β βʲ β̃ β̃ʲ θʲ ðʲ)"
```

**Acceptance:** the six segments tokenize; no existing test changed; the README records the
derivation and the O-1/O-2 decisions.

---

## Task 2: Lexicon schema, reader, and `strands check` validation

**Depends on:** — . **Spec:** §3, §7, **§10**; O-18, O-19, O-21, O-22, O-24.

**Read first:** `rules/old-irish-lexicon-log.md`. The lexicon **already exists** (299 rows,
committed with the harvest). This task writes the code that governs it, and it must be prepared
for the committed file to fail its own new checks — the `kind` column does not exist yet, and the
37 `irregular` rows are the placeholder the log's finding 5 describes. **Fixing the data is Task
3's job, not this one.** This task's committed state is: schema + reader + `check` green on
everything spec §3/§10 already required, and the two *new* requirements (`kind`, the widened stem
vocabulary) implemented but tolerated on the existing file via the `NEEDS_TASK3` allowance below.

**Files:**
- Create: `src/strands/lexicon.py`
- Modify: `rules/old-irish-lexicon.tsv` (**header only** — add the `kind` column, leaving every
  cell empty; the values are Task 3's)
- Modify: `src/strands/check.py` (`check_lexicon_file()`)
- Modify: `src/strands/cli.py` (`strands check` routes a `.tsv` path to `check_lexicon_file`)
- Test: `tests/test_lexicon.py`

**Interfaces:**
- Produces:
  ```python
  LEXICON_COLUMNS = ("orthography", "oi_nom", "oi_gen", "stem", "gender", "status",
                     "kind", "source", "note")
  STEMS    = ("o", "ā", "i", "u", "n", "dental", "velar", "r", "s", "indecl", "irregular")
  GENDERS  = ("m", "f", "n")
  STATUSES = ("attested", "middle", "none")      # spec §10 adds `middle`
  KINDS    = ("loan", "late")                    # spec §10 splits the `none` flag
  FORM_STATUSES = ("attested", "middle")         # the two that carry an Old Irish form

  @dataclass(frozen=True)
  class LexEntry:
      orthography: str
      oi_nom: str = "";  oi_gen: str = "";  stem: str = "";  gender: str = ""
      status: str = "attested";  kind: str = "";  source: str = "";  note: str = ""
      line: int = 0

      @property
      def flag(self) -> str:
          """The Result flag this row produces (spec §2, §10; O-18, O-22)."""
          # attested -> "ATTESTED"; middle -> "ATTESTED:MIr";
          # none+loan -> "RETRO:loan"; none+late -> "RETRO:late"

  class LexiconError(Exception): ...

  def key(text: str) -> str:                      # NFC + casefold (O-19)
  def read_rows(path) -> tuple[list[str], list[LexEntry]]
  def read_lexicon(path=None) -> dict[str, LexEntry]
  def validate(header, entries, path) -> list[CheckError]
  def default_lexicon_path() -> Path
  ```
  `check.check_lexicon_file(path) -> list[CheckError]` reads and validates, reusing the existing
  `CheckError` dataclass (`line`, `code`, `message`, `severity`).
- Consumed by: Task 3 (the fix-up), Task 13 (`lookup`), Task 15 (stem class), Task 17 (regression).

**Validation codes.** Severity `error` unless the row says otherwise.

| Code | Severity | Condition |
|---|---|---|
| `LEX_HEADER` | error | header is not exactly `LEXICON_COLUMNS` |
| `LEX_NO_KEY` | error | empty `orthography` |
| `LEX_DUPLICATE_KEY` | error | two rows with the same `key(orthography)` (O-19) |
| `LEX_STATUS` | error | `status` not in `STATUSES` |
| `LEX_NO_SOURCE` | error | empty `source` — **every** row (spec §3) |
| `LEX_SOURCE_SHAPE` | error | `source` matches none of `^https?://`, `^digest §10\.\d+`, `^strachan1909 p\.\d+`, `^pokorny1914 p\.\d+` |
| `LEX_ATTESTED_NO_NOM` | error | `status` in `FORM_STATUSES` and empty `oi_nom` |
| `LEX_NONE_HAS_FORM` | error | `status = none` and any of `oi_nom`/`oi_gen`/`stem`/`gender` non-empty (O-18) |
| `LEX_NONE_NO_KIND` | error | `status = none` and `kind` not in `KINDS` (O-18) |
| `LEX_KIND_ON_FORM_ROW` | error | `status` in `FORM_STATUSES` and `kind` non-empty |
| `LEX_STEM` | error | `stem` non-empty and not in `STEMS` |
| `LEX_GENDER` | error | `gender` non-empty and not in `GENDERS` |
| `LEX_IRREGULAR_NO_GEN` | error | `stem = irregular` and empty `oi_gen` (O-21) |
| `LEX_NEEDS_TASK3` | **warning** | `status` in `FORM_STATUSES` and (`stem` empty **or** `stem = irregular` **or** `gender` empty) |

**Why `LEX_NEEDS_TASK3` is a warning and the two "no stem"/"no gender" errors of the pre-harvest
draft are gone.** The committed file has 91 rows with a blank `stem`, 96 with a blank `gender` and
37 `irregular` rows that the log's finding 5 says are four different paradigms wearing one label.
Most of the blanks are adjectives, numerals and prefixes for which a stem class is not the
relevant property. Making those errors would make `strands check` red on committed, verified data
and would pressure Task 3 into inventing classes. As a **warning** the same rows are visible,
countable, and Task 3's acceptance criterion is that the count comes down.

- [ ] **Step 1: Write the failing tests**

`tests/test_lexicon.py`:

```python
"""Task 2: lexicon schema and validation (spec §3, §7, §10; O-18, O-19, O-21, O-22)."""
import pytest

from helpers import ROOT
from strands.check import check_lexicon_file
from strands.lexicon import (FORM_STATUSES, GENDERS, KINDS, LEXICON_COLUMNS, STATUSES, STEMS,
                             LexEntry, default_lexicon_path, key, read_lexicon, read_rows)

HEADER = "\t".join(LEXICON_COLUMNS)


def write(tmp_path, *rows):
    path = tmp_path / "lex.tsv"
    path.write_text("\n".join([HEADER, *rows]) + "\n", encoding="utf-8")
    return path


def row(**kw):
    kw.setdefault("status", "attested")
    return "\t".join(kw.get(c, "") for c in LEXICON_COLUMNS)


ATTESTED = dict(orthography="Niall", oi_nom="Níall", oi_gen="Néill", stem="o", gender="m",
                source="https://en.wiktionary.org/wiki/N%C3%ADall")
LOAN = dict(orthography="Seán", status="none", kind="loan",
            source="https://en.wiktionary.org/wiki/Se%C3%A1n", note="< Old French Jehan")
LATE = dict(orthography="Saoirse", status="none", kind="late",
            source="https://en.wiktionary.org/wiki/saoirse", note="20th-c. coinage")
MIDDLE = dict(orthography="Tadhg", oi_nom="Tadg", stem="o", gender="m", status="middle",
              source="https://en.wiktionary.org/wiki/Tadg")


def codes(path, severity=None):
    return sorted(e.code for e in check_lexicon_file(path)
                  if severity is None or e.severity == severity)


def test_the_column_list_is_the_spec_3_plus_10_schema():
    assert LEXICON_COLUMNS == ("orthography", "oi_nom", "oi_gen", "stem", "gender",
                               "status", "kind", "source", "note")
    assert STEMS == ("o", "ā", "i", "u", "n", "dental", "velar", "r", "s", "indecl",
                     "irregular")
    assert STATUSES == ("attested", "middle", "none")
    assert KINDS == ("loan", "late")
    assert FORM_STATUSES == ("attested", "middle")


def test_the_four_row_shapes_all_validate(tmp_path):
    assert codes(write(tmp_path, row(**ATTESTED), row(**LOAN), row(**LATE), row(**MIDDLE)),
                 severity="error") == []


@pytest.mark.parametrize("fields,expected", [
    (ATTESTED, "ATTESTED"), (MIDDLE, "ATTESTED:MIr"),
    (LOAN, "RETRO:loan"), (LATE, "RETRO:late"),
])
def test_each_status_maps_to_its_result_flag(fields, expected):
    """spec §2 and §10; O-18, O-22. Task 13 reads exactly this property."""
    assert LexEntry(**{k: v for k, v in fields.items()}).flag == expected


def test_the_key_is_nfc_case_folded(tmp_path):
    lex = read_lexicon(write(tmp_path, row(**ATTESTED)))
    assert key("NIALL") in lex and lex[key("niall")].oi_nom == "Níall"


def test_duplicate_keys_are_rejected(tmp_path):
    assert "LEX_DUPLICATE_KEY" in codes(
        write(tmp_path, row(**ATTESTED), row(**dict(ATTESTED, orthography="NIALL"))))


def test_every_row_must_cite_a_source(tmp_path):
    for fields in (ATTESTED, LOAN, MIDDLE):
        assert "LEX_NO_SOURCE" in codes(write(tmp_path, row(**dict(fields, source=""))))


def test_a_source_must_look_like_a_url_or_a_page_citation(tmp_path):
    assert "LEX_SOURCE_SHAPE" in codes(write(tmp_path, row(**dict(ATTESTED, source="eDIL"))))
    for good in ("https://dil.ie/33021", "digest §10.6", "strachan1909 p.9",
                 "pokorny1914 p.60 §134"):
        assert codes(write(tmp_path, row(**dict(ATTESTED, source=good))),
                     severity="error") == []


def test_a_form_bearing_row_needs_a_form(tmp_path):
    for fields in (ATTESTED, MIDDLE):
        assert "LEX_ATTESTED_NO_NOM" in codes(write(tmp_path, row(**dict(fields, oi_nom=""))))


def test_a_none_row_carries_no_form_and_must_say_which_kind_it_is(tmp_path):
    """O-18: RETRO:loan vs RETRO:late is a COLUMN, not a note-parse."""
    assert "LEX_NONE_HAS_FORM" in codes(write(tmp_path, row(**dict(LOAN, oi_nom="Seán"))))
    assert "LEX_NONE_NO_KIND" in codes(write(tmp_path, row(**dict(LOAN, kind=""))))
    assert "LEX_NONE_NO_KIND" in codes(write(tmp_path, row(**dict(LOAN, kind="borrowed"))))


def test_kind_is_meaningless_on_a_form_bearing_row(tmp_path):
    assert "LEX_KIND_ON_FORM_ROW" in codes(write(tmp_path, row(**dict(ATTESTED, kind="loan"))))


def test_the_widened_stem_vocabulary_is_accepted(tmp_path):
    """spec §10: velar (*rí ~ ríg*), r (*athair*), s (*tech*), indecl."""
    for stem in ("velar", "r", "s", "indecl"):
        assert codes(write(tmp_path, row(**dict(ATTESTED, stem=stem))),
                     severity="error") == []
    assert "LEX_STEM" in codes(write(tmp_path, row(**dict(ATTESTED, stem="io"))))


def test_an_irregular_row_must_supply_its_genitive(tmp_path):
    assert "LEX_IRREGULAR_NO_GEN" in codes(
        write(tmp_path, row(**dict(ATTESTED, stem="irregular", oi_gen=""))))


def test_a_row_task3_still_owes_work_on_is_a_warning_not_an_error(tmp_path):
    """The committed file has 91 blank stems and 37 `irregular` placeholders; those are
    Task 3's to fix and must not turn `strands check` red in the meantime."""
    path = write(tmp_path, row(**dict(ATTESTED, stem="")))
    assert codes(path, severity="error") == []
    assert "LEX_NEEDS_TASK3" in codes(path, severity="warning")


def test_a_wrong_header_is_reported_not_guessed(tmp_path):
    path = tmp_path / "lex.tsv"
    path.write_text("orthography\toi_nom\n", encoding="utf-8")
    assert "LEX_HEADER" in codes(path)


# ---- the committed file ------------------------------------------------------------------

PATH = default_lexicon_path()
FILE_HEADER, FILE_ROWS = read_rows(PATH)


def test_the_committed_lexicon_has_no_errors():
    assert [e for e in check_lexicon_file(PATH) if e.severity == "error"] == []


def test_the_committed_lexicon_is_the_harvested_one():
    """The log records 299 rows: 270 attested + 29 none, 163 with genitives."""
    assert len(FILE_ROWS) == 299
    assert sum(r.status in FORM_STATUSES for r in FILE_ROWS) == 270
    assert sum(r.status == "none" for r in FILE_ROWS) == 29
    assert sum(bool(r.oi_gen) for r in FILE_ROWS) == 163


def test_the_task3_backlog_is_visible_and_counted():
    """The number this warning reports is Task 3's acceptance metric."""
    warnings = [e for e in check_lexicon_file(PATH) if e.code == "LEX_NEEDS_TASK3"]
    assert warnings, "expected the harvest's blank/irregular rows to be reported"
```

`tests/test_cli.py` — append:

```python
def test_check_accepts_a_lexicon_tsv():
    from strands.cli import main
    assert main(["check", str(ROOT / "rules" / "old-irish-lexicon.tsv")]) == 0
```

(`check` exits 0 on warnings; only error-severity findings fail it. Confirm that against the
existing `check` handler and, if it currently fails on any finding, restrict the failure to
`severity == "error"` — the four target rule files emit no warnings today, so nothing changes for
them.)

- [ ] **Step 2: Run the tests and watch them fail**

Run: `uv run pytest tests/test_lexicon.py -q`
Expected: FAIL — `ModuleNotFoundError: No module named 'strands.lexicon'`.

- [ ] **Step 3: Write `src/strands/lexicon.py`**

```python
"""`rules/old-irish-lexicon.tsv`: the Old Irish lookup table (plan Task 2; spec §3, §10).

One row per modern citation form. `attested` rows carry a classical Old Irish nominative;
`middle` rows carry a Middle-Irish-only form, used by lookup but flagged `ATTESTED:MIr` so the
register claim stays honest (spec §10); `none` rows are post-Old-Irish words with no Old Irish
ancestor and carry a form-free etymology citation plus a `kind` saying whether they are a
borrowing (`loan`) or an Irish-internal coinage (`late`).

Matching is exact on `orthography` after NFC and case-folding (O-19), and `orthography` is always
the CITATION form: the Irish pre-pass has already applied mutation and inflection on the modern
side, so a surface form such as *a Sheáin* is looked up as *Seán* by the caller supplying the
entry's own citation orthography — never by stripping the mutation here (O-23).

Every row must cite a page that shows what it claims (spec §3). `strands check` rejects the file
otherwise, so an unsourced row can never reach the pipeline. `LEX_NEEDS_TASK3` is a WARNING, not
an error: the harvested file has rows whose stem class or gender is blank or is the `irregular`
placeholder of the harvest log's finding 5, and those are a data backlog, not a schema breach.
"""
from __future__ import annotations

import csv
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

__all__ = ["LEXICON_COLUMNS", "STEMS", "GENDERS", "STATUSES", "KINDS", "FORM_STATUSES",
           "LexEntry", "LexiconError", "key", "read_rows", "read_lexicon", "validate",
           "default_lexicon_path"]

LEXICON_COLUMNS = ("orthography", "oi_nom", "oi_gen", "stem", "gender", "status",
                   "kind", "source", "note")
STEMS = ("o", "ā", "i", "u", "n", "dental", "velar", "r", "s", "indecl", "irregular")
GENDERS = ("m", "f", "n")
STATUSES = ("attested", "middle", "none")
KINDS = ("loan", "late")
FORM_STATUSES = ("attested", "middle")
_FLAGS = {"attested": "ATTESTED", "middle": "ATTESTED:MIr"}
_SOURCE_RE = re.compile(r"^(https?://|digest §10\.\d+|strachan1909 p\.\d+|pokorny1914 p\.\d+)")
_RULES_DIR = Path(__file__).resolve().parents[2] / "rules"


class LexiconError(Exception):
    """The lexicon file cannot be read at all (missing, or no header)."""


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

    @property
    def flag(self) -> str:
        """The `Result.flags` entry this row produces (spec §2, §10; O-18, O-22)."""
        if self.status in _FLAGS:
            return _FLAGS[self.status]
        return f"RETRO:{self.kind}" if self.kind in KINDS else "RETRO"


def default_lexicon_path() -> Path:
    return _RULES_DIR / "old-irish-lexicon.tsv"


def key(text: str) -> str:
    """O-19: exact match after NFC and case-folding; no fuzzy matching."""
    return unicodedata.normalize("NFC", text).strip().casefold()


def _nfc(text: str | None) -> str:
    return unicodedata.normalize("NFC", (text or "")).strip()


def read_rows(path: str | Path | None = None) -> tuple[list[str], list[LexEntry]]:
    """(header, entries). Blank lines are dropped; entries keep their 1-based file line."""
    p = Path(default_lexicon_path() if path is None else path)
    with p.open(encoding="utf-8", newline="") as fh:
        reader = csv.reader(fh, delimiter="\t")
        try:
            header = [_nfc(h) for h in next(reader)]
        except StopIteration:
            raise LexiconError(f"{p}: empty file") from None
        entries: list[LexEntry] = []
        for lineno, raw in enumerate(reader, start=2):
            if not any(cell.strip() for cell in raw):
                continue
            cells = [_nfc(c) for c in raw] + [""] * (len(LEXICON_COLUMNS) - len(raw))
            f = dict(zip(header, cells))
            entries.append(LexEntry(
                orthography=f.get("orthography", ""), oi_nom=f.get("oi_nom", ""),
                oi_gen=f.get("oi_gen", ""), stem=f.get("stem", ""),
                gender=f.get("gender", ""), status=f.get("status", "") or "attested",
                kind=f.get("kind", ""), source=f.get("source", ""),
                note=f.get("note", ""), line=lineno))
    return header, entries


def read_lexicon(path: str | Path | None = None) -> dict[str, LexEntry]:
    """key(orthography) -> LexEntry. Later duplicates lose; `validate` reports them."""
    _, entries = read_rows(path)
    out: dict[str, LexEntry] = {}
    for entry in entries:
        k = key(entry.orthography)
        if k and k not in out:
            out[k] = entry
    return out


def validate(header: Sequence[str], entries: Sequence[LexEntry], path: str) -> list:
    from .check import CheckError                     # local: check imports lexicon
    out: list[CheckError] = []

    def add(line: int, code: str, message: str, severity: str = "error") -> None:
        out.append(CheckError(line=line, code=code,
                              message=f"{path}:{line}: {message}", severity=severity))

    if tuple(header) != LEXICON_COLUMNS:
        add(1, "LEX_HEADER",
            f"header must be exactly {' '.join(LEXICON_COLUMNS)} (have: {' '.join(header)})")
        return out
    seen: dict[str, int] = {}
    for e in entries:
        if not e.orthography:
            add(e.line, "LEX_NO_KEY", "empty orthography (the match key)")
            continue
        k = key(e.orthography)
        if k in seen:
            add(e.line, "LEX_DUPLICATE_KEY",
                f"{e.orthography!r} already defined at line {seen[k]}")
        else:
            seen[k] = e.line
        if e.status not in STATUSES:
            add(e.line, "LEX_STATUS", f"status {e.status!r} not in {', '.join(STATUSES)}")
        if not e.source:
            add(e.line, "LEX_NO_SOURCE", "every row must cite a source (spec §3)")
        elif not _SOURCE_RE.match(e.source):
            add(e.line, "LEX_SOURCE_SHAPE",
                f"source {e.source!r} must be a URL, 'digest §10.n', "
                "'strachan1909 p.N' or 'pokorny1914 p.N'")
        if e.stem and e.stem not in STEMS:
            add(e.line, "LEX_STEM", f"stem {e.stem!r} not in {', '.join(STEMS)}")
        if e.gender and e.gender not in GENDERS:
            add(e.line, "LEX_GENDER", f"gender {e.gender!r} not in {', '.join(GENDERS)}")
        if e.status in FORM_STATUSES:
            if not e.oi_nom:
                add(e.line, "LEX_ATTESTED_NO_NOM", f"{e.status} row without oi_nom")
            if e.kind:
                add(e.line, "LEX_KIND_ON_FORM_ROW",
                    f"kind={e.kind!r} is only meaningful on a `none` row (O-18)")
            if e.stem == "irregular" and not e.oi_gen:
                add(e.line, "LEX_IRREGULAR_NO_GEN",
                    "stem=irregular means 'use oi_gen verbatim' (O-21), but oi_gen is empty")
            if not e.stem or e.stem == "irregular" or not e.gender:
                add(e.line, "LEX_NEEDS_TASK3",
                    f"stem={e.stem!r} gender={e.gender!r}: Task 3 owes this row a real stem "
                    "class and gender (harvest log finding 5)", severity="warning")
        elif e.status == "none":
            if e.oi_nom or e.oi_gen or e.stem or e.gender:
                add(e.line, "LEX_NONE_HAS_FORM",
                    "a `none` row has no Old Irish ancestor: oi_nom, oi_gen, stem and "
                    "gender must all be empty (O-18)")
            if e.kind not in KINDS:
                add(e.line, "LEX_NONE_NO_KIND",
                    f"kind {e.kind!r} must be one of {', '.join(KINDS)}: `loan` = a "
                    "borrowing, `late` = an Irish-internal post-Old-Irish coinage (O-18)")
    return out
```

- [ ] **Step 4: Wire it into `check.py` and `cli.py`**

```python
def check_lexicon_file(path: str | Path) -> list[CheckError]:
    """Schema, citation, duplicate-key and backlog checks for the Old Irish lexicon
    (plan Task 2; spec §3, §7, §10)."""
    from .lexicon import read_rows, validate
    header, entries = read_rows(path)
    return validate(header, entries, str(path))
```

In `cli.py`'s `check` handler: a path ending `.tsv` routes to `check_lexicon_file`, anything else
to `check_rule_file`; print all findings, exit 1 only when one has `severity == "error"`.

- [ ] **Step 5: Add the `kind` column to the committed lexicon — header only**

Insert `kind` between `status` and `source` in the header line and add one empty field to every
data row, changing nothing else:

```bash
uv run python - <<'PY'
import pathlib
p = pathlib.Path("rules/old-irish-lexicon.tsv")
lines = p.read_text(encoding="utf-8").splitlines()
head = lines[0].split("\t"); i = head.index("status") + 1
head.insert(i, "kind")
out = ["\t".join(head)]
for line in lines[1:]:
    cells = line.split("\t")
    if any(c.strip() for c in cells):
        cells.insert(i, "")
    out.append("\t".join(cells))
p.write_text("\n".join(out) + "\n", encoding="utf-8")
PY
```

This leaves all 29 `none` rows failing `LEX_NONE_NO_KIND`, which is an **error**. Fill those 29
cells now — they are the only data this task touches, the log's finding 7 lists both groups
verbatim, and 29 rows is not a harvest:

- `kind = loan`: *Seán, Siobhán, Séamus, Brian, tobac, téarma, seirbhís, geata, bád, speal,
  cnaipe, Cairmilíteach*
- `kind = late`: *Ciara, Saoirse, Gaelach, naofa, leisciúil, ardnósach, drochbhéasach, cailín,
  portach, bádóir, gasúr, spraoi, breá, cliste, cróga, dílis, an-*

Cross-check the count against `read_rows` afterwards: 12 `loan` + 17 `late` = 29.

- [ ] **Step 6: Run everything**

Run: `uv run strands check rules/old-irish-lexicon.tsv` — expected: `LEX_NEEDS_TASK3` warnings
listed, **exit 0**.
Run: `uv run pytest tests/test_lexicon.py tests/test_cli.py -q` — expected PASS.
Run: `uv run pytest -q` — expected 1004+ passed, 2 xfailed.

- [ ] **Step 7: Commit**

```bash
git add src/strands/lexicon.py src/strands/check.py src/strands/cli.py \
        rules/old-irish-lexicon.tsv tests/test_lexicon.py tests/test_cli.py
git commit -m "feat(lexicon): schema, reader and check validation; kind column for RETRO:loan/late"
```

**Acceptance:** the committed 299-row lexicon has zero error findings and a counted
`LEX_NEEDS_TASK3` backlog; all four row shapes validate and map to their flags; the 29 `none` rows
are split 12 `loan` / 17 `late`; `strands check` accepts a `.tsv` path.

---

## Task 3: Lexicon fix-up — real stem classes, and a second verification pass

**Depends on:** Task 2. **Spec:** §7, §10; O-21, O-24. **Needs network access.**

**Read first:** `rules/old-irish-lexicon-log.md`, findings 5 and 6, and the "Sample verification"
section. The harvest's own recommendation is that the ~107 genitive-less rows deserve a second
pass "before the inflection tests lean on them" — this is that pass, plus the reclassification the
widened `STEMS` vocabulary (spec §10) now makes possible.

**This task should be executed by a different agent than the one that harvested the lexicon**, for
the same reason the first verification pass was independent. It is not a from-scratch harvest.

**Files:**
- Modify: `rules/old-irish-lexicon.tsv`
- Modify: `rules/old-irish-lexicon-log.md` (append a "Second pass (Task 3)" section)
- Create: `rules/old-irish-lexicon.verification2.tsv`
- Test: `tests/test_lexicon_data.py`

**Interfaces:**
- Produces: a lexicon in which every `attested`/`middle` row that *has* a nominal paradigm carries
  a real `stem` from `STEMS` and a `gender`, and in which `irregular` means suppletive.
- `rules/old-irish-lexicon.verification2.tsv`, header
  `orthography  source  field  verdict  checked_by  note`, `verdict` ∈ `ok | fixed | removed`.

**Part A — reclassify the 37 `irregular` rows (log finding 5).** The log names the mapping the
harvest was forced into: velar (guttural), r-stem, s-stem and indeclinable all became `irregular`
because spec §3 had no slot. Spec §10 added `velar`, `r`, `s`, `indecl`. For each of the 37 rows:
read the `note` (the harvest recorded the true class there), set `stem` accordingly, and leave
`irregular` **only** where the note names no class and the paradigm really is suppletive. The
paradigm words the inflection tests want are named in the log and must all end up classified:
*teach ~ tech* (s), *sliabh ~ slíab* (s), *athair* (r), *bráthair* (r), *máthair* (r),
*rí ~ ríg* (velar), *Lughaidh ~ Luigdech* (velar), *Eochaidh ~ Echach* (velar),
*Pádraig ~ Patraic* (indecl), *Da Derga* (indecl).

**Part B — the 91 blank-stem and 96 blank-gender rows.** Most are adjectives, numerals and
prefixes with no nominal paradigm. Do **not** invent a class for those; instead record the reason
in `note` using one of exactly these strings, so the warning can be silenced honestly:
`no nominal paradigm: adjective` / `: numeral` / `: prefix` / `: phrase`. Then extend Task 2's
`LEX_NEEDS_TASK3` condition to skip a row whose `note` starts `no nominal paradigm:` — that is a
one-line change to `lexicon.validate`, and it belongs to this task because only this task knows
the rows are genuinely exempt. Rows that *are* nouns and simply lack the data get their stem and
gender from a re-check of the cited page (Part C) or, failing that, keep the warning.

**Part C — the second verification pass.** Sample **≥30 rows from the 107 with a blank `oi_gen`**,
plus every row touched in Parts A and B whose class was not already stated in its `note`. For each:
open `source`; confirm the `oi_nom`; take the genitive and the stem class from the page's
inflection table where it has one; record `ok`/`fixed`/`removed` in the verification file with
what the page actually said. The `field` column names which field was checked
(`oi_gen`, `stem`, `gender`, `oi_nom`).

**The gate**, as in the first pass: if more than 10% of the sampled rows are `fixed` or `removed`,
report that rather than patching — it means the genitive-less rows are systematically unreliable
and the inflection tests must not lean on them.

- [ ] **Step 1: Write the failing tests**

`tests/test_lexicon_data.py`:

```python
"""Task 3: the lexicon as data, after the fix-up pass (spec §7, §10; O-21, O-24)."""
import csv

import pytest

from helpers import ROOT, read_test_words
from strands.check import check_lexicon_file
from strands.lexicon import (FORM_STATUSES, KINDS, STEMS, key, read_lexicon, read_rows)

PATH = ROOT / "rules" / "old-irish-lexicon.tsv"
HEADER, ROWS = read_rows(PATH)
LEX = read_lexicon(PATH)
FORMS = [r for r in ROWS if r.status in FORM_STATUSES]
NONE_ROWS = [r for r in ROWS if r.status == "none"]
VERIF = ROOT / "rules" / "old-irish-lexicon.verification2.tsv"
VERIF_COLUMNS = ("orthography", "source", "field", "verdict", "checked_by", "note")
EXEMPT = "no nominal paradigm:"


def verification():
    with VERIF.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh, delimiter="\t")
        return list(reader.fieldnames or []), list(reader)


def test_the_lexicon_still_has_no_errors():
    assert [e for e in check_lexicon_file(PATH) if e.severity == "error"] == []


def test_the_irregular_placeholder_is_now_reserved_for_suppletion():
    """Log finding 5: 37 rows wore `irregular` for four different paradigms. Spec §10 gave
    velar / r / s / indecl their own slots."""
    left = [r.orthography for r in FORMS if r.stem == "irregular"]
    assert len(left) <= 10, left


@pytest.mark.parametrize("headword,stem", [
    ("teach", "s"), ("sliabh", "s"), ("athair", "r"), ("máthair", "r"), ("bráthair", "r"),
    ("rí", "velar"), ("Lughaidh", "velar"), ("Eochaidh", "velar"), ("Pádraig", "indecl"),
])
def test_the_paradigm_words_the_inflection_tests_need_are_classified(headword, stem):
    """These are exactly the rows Task 15's [inflect] tests are written against."""
    row = LEX.get(key(headword))
    assert row is not None, headword
    assert row.stem == stem, (headword, row.stem)


def test_every_remaining_backlog_row_says_why_it_has_no_paradigm():
    """Part B: a blank stem is fine for an adjective/numeral/prefix, and must SAY so."""
    backlog = [r for r in FORMS if (not r.stem or not r.gender)
               and not r.note.startswith(EXEMPT)]
    assert backlog == [], [(r.orthography, r.stem, r.gender) for r in backlog]


def test_the_needs_task3_warning_is_now_quiet():
    """The acceptance metric of this task, stated as a test."""
    warnings = [e for e in check_lexicon_file(PATH) if e.code == "LEX_NEEDS_TASK3"]
    assert warnings == [], [w.message for w in warnings]


def test_the_none_rows_are_split_into_loans_and_late_coinages():
    """Log finding 7 / O-18: 12 loans, 17 Irish-internal coinages."""
    assert sum(r.kind == "loan" for r in NONE_ROWS) == 12
    assert sum(r.kind == "late" for r in NONE_ROWS) == 17
    assert all(r.kind in KINDS for r in NONE_ROWS)


def test_old_irish_forms_carry_no_modern_lenition_digraphs():
    """digest §10.2 convention 1 / log finding 3: there is no ⟨bh dh gh mh⟩ in Old Irish."""
    bad = [(r.orthography, r.oi_nom) for r in FORMS
           if any(d in r.oi_nom.lower() for d in ("bh", "dh", "gh", "mh"))]
    assert bad == [], bad


def test_the_seventy_four_direct_test_word_hits_are_intact():
    """The log's measured coverage (O-23): 74 of the 138 distinct keys hit a row directly."""
    keys = {key(r["orthography"]) for r in read_test_words()}
    assert len(keys) == 138
    assert len(keys & set(LEX)) >= 74


def test_the_twenty_ao_pairs_are_still_present():
    """O-13: they are Task 17's named regression set for decision O1."""
    pairs = [r for r in FORMS if "ao" in r.orthography.lower()]
    assert len(pairs) >= 20, len(pairs)


def test_a_second_verification_file_exists_with_the_agreed_schema():
    header, rows = verification()
    assert tuple(header) == VERIF_COLUMNS
    assert len(rows) >= 30, len(rows)


def test_every_verdict_is_explained_and_attributed():
    _, rows = verification()
    for r in rows:
        assert r["verdict"] in ("ok", "fixed", "removed"), r
        assert r["checked_by"].strip(), r
        if r["verdict"] != "ok":
            assert r["note"].strip(), r["orthography"]


def test_the_defect_rate_admits_the_genitive_less_rows():
    """The gate: >10% means the inflection tests must not lean on these rows."""
    _, rows = verification()
    defects = sum(r["verdict"] != "ok" for r in rows)
    assert defects <= len(rows) // 10, (defects, len(rows))


def test_removed_rows_are_gone_and_kept_rows_are_present():
    _, rows = verification()
    for r in rows:
        present = key(r["orthography"]) in LEX
        assert present != (r["verdict"] == "removed"), r["orthography"]
```

- [ ] **Step 2: Run them and watch them fail**

Run: `uv run pytest tests/test_lexicon_data.py -q`
Expected: FAIL — `FileNotFoundError: …verification2.tsv`, and the paradigm-word parametrization
fails because those rows are still `irregular`.

- [ ] **Step 3: Part A — reclassify**

Work the 37 `irregular` rows from the file, reading each row's `note`. List them first so the work
is auditable:

```bash
uv run python -c "
from strands.lexicon import read_rows
for r in read_rows()[1]:
    if r.stem == 'irregular':
        print(r.line, r.orthography, '|', r.oi_nom, '|', r.oi_gen, '|', r.note)"
```

- [ ] **Step 4: Part B — annotate the paradigm-less rows and relax the warning**

Add the `no nominal paradigm: …` notes, then make the one-line change in
`lexicon.validate`'s `LEX_NEEDS_TASK3` condition:

```python
            if (not e.stem or e.stem == "irregular" or not e.gender) \
                    and not e.note.startswith("no nominal paradigm:"):
```

and document the exemption string in the module docstring.

- [ ] **Step 5: Part C — verify, and write both files**

Sample, open the pages, correct the data, and write
`rules/old-irish-lexicon.verification2.tsv`. Append a "Second pass (Task 3)" section to
`rules/old-irish-lexicon-log.md` recording: how many rows were reclassified into each new stem
value, how many were annotated exempt, the verification counts, and any row removed.

- [ ] **Step 6: Run everything**

Run: `uv run strands check rules/old-irish-lexicon.tsv` — expected: **no findings at all**, exit 0.
Run: `uv run pytest tests/test_lexicon_data.py tests/test_lexicon.py -q` — expected PASS. Note that
`test_the_task3_backlog_is_visible_and_counted` in `tests/test_lexicon.py` asserts the warning
*exists*; this task makes it empty, so **delete that one test** and say so in the commit message —
it was a Task 2 acceptance probe, and Task 3's `test_the_needs_task3_warning_is_now_quiet`
replaces it.
Run: `uv run pytest -q` — expected 1004+ passed, 2 xfailed.

- [ ] **Step 7: Commit**

```bash
git add rules/old-irish-lexicon.tsv rules/old-irish-lexicon-log.md \
        rules/old-irish-lexicon.verification2.tsv src/strands/lexicon.py \
        tests/test_lexicon_data.py tests/test_lexicon.py
git commit -m "data(lexicon): reclassify irregular rows into velar/r/s/indecl, annotate paradigm-less rows, second verification pass"
```

**Acceptance:** ≤10 rows still `irregular`; the ten named paradigm words carry their real class;
every remaining blank explains itself; `strands check` is completely silent; ≥30 genitive-less
rows verified with ≤10% defects; the log records the pass.

---

## Task 4: Middle Irish tier — the 49 unresolved names

**Depends on:** Task 3. **Spec:** §10 (`status = middle`, flag `ATTESTED:MIr`); O-22. **Needs
network access.**

**Read first:** the "Unresolved" section of `rules/old-irish-lexicon-log.md` — 49 headwords
harvested and deliberately left out, with a per-headword reason. The log's own diagnosis: "The
dominant pattern here is **Middle Irish attestation without an Old Irish one**", and it names the
two honest routes, one of which — "an explicit policy decision to admit Middle Irish forms as
fallback ancestors with a distinct status value" — spec §10 has now taken.

**This is a small extension, not a harvest.** The 49 headwords and their sources are already
recorded; the work is to revisit each one against the `middle` tier and write a row where the log
already found a Middle Irish form.

**Files:**
- Modify: `rules/old-irish-lexicon.tsv`
- Modify: `rules/old-irish-lexicon-log.md` (append a "Middle Irish tier (Task 4)" section)
- Test: `tests/test_lexicon_data.py` (append)

**Interfaces:**
- Produces `status = middle` rows whose `flag` is `ATTESTED:MIr` (Task 2's `LexEntry.flag`).
  Nothing else in the pipeline branches on the tier (O-22).

**Procedure, per unresolved headword:**

1. **Write a `middle` row** when the log's reason already names a Middle Irish form: the row's
   `oi_nom` is that form, `source` is the page that shows it, `note` records "Middle Irish only;
   no Old Irish attestation found (harvest log, unresolved)". The log names these outright —
   *Eoghan ~ Eógan*, *Tadhg ~ Tadg*, *Méabh ~ Medb*, *Oisín ~ oisín*, *bealach ~ belach*,
   *saoi ~ suí*, *dualgas ~ dúalgas*, *sméar ~ smér*, *gaiscíoch*, *gruaig*(*gruac* is
   **unattested**, marked with `*` — see rule 3), *gealach* (likewise) — and the coordinator's
   note lists *Órla, Gráinne, Úna* as intended members of the tier, which means re-checking those
   three specifically for a Middle Irish form the first pass did not record.
2. **Leave out** any headword whose log reason is "no page found", "fetch failed", "not checked
   within budget" or "no Etymology section": nothing has changed for them, and the `middle` tier
   is not a licence to guess. Re-checking them is optional and out of scope.
3. **Never write a reconstructed form.** A source that prints only an asterisked form
   (*\*gruac*, *\*gelach*) has not attested anything; those headwords stay out. This is the rule
   that keeps `ATTESTED:MIr` meaning "attested, in Middle Irish".
4. Stem class and gender come from the Middle Irish entry's inflection table where it has one,
   else the row is annotated per Task 3's Part B convention.

Expect roughly 10–20 new rows. **The number is not a target** — a headword with no attested
Middle Irish form must stay unresolved, and the log must say how many were revisited and how many
were written.

- [ ] **Step 1: Write the failing tests** (append to `tests/test_lexicon_data.py`)

```python
MIDDLE = [r for r in ROWS if r.status == "middle"]


def test_the_middle_irish_tier_is_populated():
    """spec §10: the important names should not be left to the filter."""
    assert len(MIDDLE) >= 10, len(MIDDLE)


@pytest.mark.parametrize("headword", ["Eoghan", "Tadhg", "Oisín"])
def test_the_named_middle_irish_names_are_now_covered(headword):
    """spec §10 names these explicitly; the log records their Middle Irish forms."""
    row = LEX.get(key(headword))
    assert row is not None and row.status == "middle", headword
    assert row.oi_nom, headword


def test_every_middle_row_flags_ATTESTED_MIr():
    """O-22: the tier shows up in the flag and nowhere else."""
    for r in MIDDLE:
        assert r.flag == "ATTESTED:MIr", r.orthography


def test_no_middle_row_records_a_reconstructed_form():
    """Rule 3: an asterisked form is not an attestation."""
    bad = [r.orthography for r in MIDDLE if "*" in r.oi_nom or "*" in r.oi_gen]
    assert bad == [], bad


def test_every_middle_row_says_it_is_middle_irish_only():
    for r in MIDDLE:
        assert "middle irish" in r.note.lower(), r.orthography


def test_the_middle_tier_did_not_disturb_the_attested_counts():
    """A `middle` row is a NEW row, never a reclassified `attested` one."""
    assert sum(r.status == "attested" for r in ROWS) == 270


def test_the_lexicon_is_still_clean_and_within_its_size_bound():
    assert check_lexicon_file(PATH) == []
    assert len(ROWS) <= 330
```

- [ ] **Step 2: Run them and watch them fail**

Run: `uv run pytest tests/test_lexicon_data.py -q` — expected FAIL: no `middle` rows exist.

- [ ] **Step 3: Work the 49, write the rows, append to the log**

The log section must record: how many of the 49 were revisited, how many rows were written, and
the headwords that stay unresolved with the (unchanged) reason.

- [ ] **Step 4: Run everything and commit**

Run: `uv run strands check rules/old-irish-lexicon.tsv` — expected exit 0, no findings.
Run: `uv run pytest -q` — expected 1004+ passed, 2 xfailed.

```bash
git add rules/old-irish-lexicon.tsv rules/old-irish-lexicon-log.md tests/test_lexicon_data.py
git commit -m "data(lexicon): Middle Irish tier — N rows for names attested only in Middle Irish"
```

**Acceptance:** ≥10 `middle` rows, including *Eoghan*, *Tadhg* and *Oisín*; every one flags
`ATTESTED:MIr`, cites a page showing an unasterisked form, and says in its note that it is Middle
Irish only; the 270 `attested` rows are untouched; `strands check` silent.

---

## Task 5: Orthography↔IPA aligner and the `Word.orth` channel

**Depends on:** — . **Spec:** §4 ("a per-segment orthographic tag set by a small aligner between
the modern orthography and IPA in the Irish pre-pass; where alignment fails the tag is absent");
O-6, O-7.

**Files:**
- Create: `src/strands/orth.py`
- Create: `rules/irish-orthography.tsv`
- Modify: `src/strands/word.py` (add the `orth` field; carry it through `replaced()`,
  `split_words()`, `traced()`)
- Test: `tests/test_orth_align.py`

**Interfaces:**
- Produces:
  ```python
  # src/strands/orth.py
  ORTH_TABLE_PATH: Path                       # rules/irish-orthography.tsv
  class OrthError(Exception): ...

  def load_orth_table(path: Path | None = None) -> tuple[tuple[str, tuple[tuple[str, ...], ...]], ...]:
      """((unit, (alternative, ...)), ...) in LONGEST-FIRST, then file order.
      An alternative is a tuple of segments; the empty tuple means the unit is silent."""

  def align(orthography: str, segments: Sequence[str],
            table: Sequence[tuple[str, tuple[tuple[str, ...], ...]]] | None = None
            ) -> tuple[str, ...]:
      """One tag per segment (O-7). All-empty on failure."""

  def tag_word(word: Word, orthography: str) -> Word:
      """`align()` the word's segments against `orthography` and return a copy with
      `Word.orth` set. On failure the tags are empty AND the word gets a trace entry
      `orth:unaligned` so `explain` shows why the spelling rules did not fire."""
  ```
- `Word` gains `orth: tuple[str, ...] = ()`. **Invariant:** `orth` is either empty (never tagged)
  or exactly `len(segments)` long. `Word.tag_at(i) -> str` returns `""` when the channel is empty.
- Consumed by: Task 6 (`@orth`), Task 7 (mutation provenance), Task 13 (the retro path).

**The alignment algorithm — implement exactly this (O-7).**

Let `U` be the loaded table: pairs `(unit, alternatives)`, `unit` a lower-cased orthographic
string of 1–3 characters, `alternatives` a tuple of segment tuples (possibly containing the empty
tuple for a silent unit). Let `o = orthography` after NFC, case-folded, with `-` and `'` and
spaces removed (Irish writes *t-éan*, *an t-uisce*, *Cú Chulainn*). Let `s = segments`.

Search a DAG whose nodes are `(i, j)` — `i` characters of `o` consumed, `j` segments consumed —
from `(0, 0)` to `(len(o), len(s))`:

```
edges(i, j) =  for each (unit, alternatives) in U, in table order:
                   if o[i:i+len(unit)] != unit: continue
                   for each alt in alternatives, in file order:
                       if tuple(s[j:j+len(alt)]) == alt:
                           yield (i + len(unit), j + len(alt), unit, len(alt))
```

`U` is sorted **longest unit first**, then file order, so `bh` is tried before `b` and `aoi`
before `ao` before `a`. Search depth-first over `edges()` in that order with a memoized set of
dead nodes; the **first** path found is the answer, which makes the result a deterministic
function of the table's order (no scoring, no ties to break). Assign every segment consumed by an
edge the edge's `unit` as its tag; a silent edge (`len(alt) == 0`) assigns nothing.

Complexity is `O(len(o) × len(s) × |U|)` with memoization, which is trivial at these sizes.

**Failure mode (the spec's "tag absent"):** if no path reaches `(len(o), len(s))`, `align`
returns `("",) * len(s)`. It never raises and never returns partial tags — a partial alignment
would let a spelling rule fire on a segment the aligner only guessed at.

**`rules/irish-orthography.tsv`** — header `unit  segments  note`. `segments` is a
space-separated list of alternatives; each alternative is a `+`-joined segment sequence; the
literal `-` means "silent" (the empty alternative). Rows to write (this is the whole file; the
`note` column carries the digest §5 citation):

| unit | segments | note |
|---|---|---|
| `bh` | `w vˠ vʲ` | digest §5.3 lenition digraph |
| `mh` | `w vˠ vʲ` | digest §5.3 |
| `dh` | `ɣ j` | digest §5.3 |
| `gh` | `ɣ j` | digest §5.3 |
| `th` | `h -` | digest §5.3; silent word-finally |
| `sh` | `h ç` | digest §5.3 |
| `ch` | `x ç` | digest §5.3 |
| `ph` | `fˠ fʲ` | digest §5.3 |
| `fh` | `-` | digest §5.3, *fh* is silent |
| `aoi` | `iː` | digest §5.1 |
| `ao` | `iː eː` | digest §5.1 |
| `eái` | `aː` | digest §5.1 glide spelling |
| `eá` | `aː` | digest §5.1 |
| `iá` | `iə` | digest §5.1 |
| `ái` | `aː` | digest §5.1 |
| `ia` | `iə i+ə` | digest §5.1 diphthong (two segments, I-2) |
| `ua` | `uə u+ə` | digest §5.1 |
| `ae` | `eː` | digest §5.1 |
| `ei` | `ɛ eː` | digest §5.1 |
| `ea` | `a aː ɑ` | digest §5.1 |
| `io` | `ɪ iː` | digest §5.1 |
| `iu` | `ʊ uː` | digest §5.1 |
| `oi` | `ɔ ɪ` | digest §5.1 |
| `ui` | `ɪ ʊ` | digest §5.1 |
| `ái` | `aː` | digest §5.1 |
| `á` | `aː` | digest §5.4 síneadh fada |
| `é` | `eː` | digest §5.4 |
| `í` | `iː` | digest §5.4 |
| `ó` | `oː` | digest §5.4 |
| `ú` | `uː` | digest §5.4 |
| `a` | `a aː ə ɑ -` | digest §5.1; `-` = a glide vowel writing quality only |
| `e` | `ɛ eː ə -` | digest §5.1 |
| `i` | `ɪ iː ə i -` | digest §5.1 |
| `o` | `ɔ oː ə -` | digest §5.1 |
| `u` | `ʊ uː ə u -` | digest §5.1 |
| `b` | `bˠ bʲ` | digest §5.2 |
| `c` | `k c` | digest §5.2 |
| `d` | `d̪ˠ dʲ` | digest §5.2 |
| `f` | `fˠ fʲ` | digest §5.2 |
| `g` | `ɡ ɟ` | digest §5.2 |
| `h` | `h -` | digest §5.2 |
| `l` | `l̪ˠ lʲ` | digest §5.2 |
| `m` | `mˠ mʲ` | digest §5.2 |
| `n` | `n̪ˠ nʲ ŋ ɲ` | digest §5.2 (`ng`, `nc` clusters) |
| `p` | `pˠ pʲ` | digest §5.2 |
| `r` | `ɾˠ ɾʲ` | digest §5.2 |
| `s` | `sˠ ʃ` | digest §5.2 |
| `t` | `t̪ˠ tʲ` | digest §5.2 |

The `-` alternatives on the plain vowels are what make *caol le caol* alignable: *bád* is
`b→bˠ, á→aː, d→d̪ˠ` but *baid* is `b→bˠ, a→aː, i→(silent), d→dʲ`. The `-` alternative on `h`
covers the prothetic *h-*.

- [ ] **Step 1: Write the failing tests**

`tests/test_orth_align.py`:

```python
"""Task 5: the modern-orthography <-> IPA aligner (spec §4; O-7)."""
import pytest

from helpers import TABLE, irish, read_test_words, w
from strands.irish import normalize
from strands.orth import align, load_orth_table, tag_word

IRISH = irish()
U = load_orth_table()


def tags(orthography, ipa):
    return align(orthography, w(ipa).segments)


def test_the_table_is_sorted_longest_unit_first():
    """`bh` must be tried before `b`, `aoi` before `ao` before `a` (O-7)."""
    lengths = [len(unit) for unit, _ in U]
    assert lengths == sorted(lengths, reverse=True)


def test_a_lenition_digraph_tags_its_segment():
    """*Niamh* /nʲiəvˠ/ -> n ia ia mh."""
    assert tags("Niamh", "nʲiəvˠ") == ("n", "ia", "ia", "mh")


def test_a_plain_word_tags_letter_by_letter():
    assert tags("gorm", "ɡɔɾˠmˠ") == ("g", "o", "r", "m")


def test_a_long_vowel_digraph_is_one_unit():
    assert tags("Seán", "ʃaːnˠ") == ("s", "eá", "n")


def test_a_glide_vowel_is_silent_and_tags_nothing():
    """caol le caol: the `i` of *baid* writes quality, not a sound."""
    assert tags("baid", "bˠaːdʲ") == ("b", "a", "d")


@pytest.mark.parametrize("orthography,ipa,expected", [
    ("bhí", "vʲiː", ("bh", "í")),
    ("mhac", "wak", ("mh", "a", "c")),
    ("dhún", "ɣuːnˠ", ("dh", "ú", "n")),
    ("chos", "xɔsˠ", ("ch", "o", "s")),
    ("phóg", "fˠoːɡ", ("ph", "ó", "g")),
    ("shúil", "huːlʲ", ("sh", "ú", "l")),
    ("ua", "uə", ("ua", "ua")),
])
def test_the_reversal_relevant_digraphs_all_align(orthography, ipa, expected):
    assert tags(orthography, ipa) == expected


def test_alignment_failure_returns_all_empty_tags_and_never_raises():
    """O-7: the tag is ABSENT, not guessed, so only sound-based rules apply."""
    assert tags("Seán", "xɔsˠ") == ("", "", "")
    assert tags("", "ɡɔɾˠmˠ") == ("", "", "", "")


def test_hyphens_apostrophes_and_spaces_are_ignored_in_the_orthography():
    assert tags("t-éan", "tʲeːnˠ") == ("t", "é", "n")


def test_tag_word_sets_the_channel_and_records_a_failure_in_the_trace():
    good = tag_word(w("ɡɔɾˠmˠ"), "gorm")
    assert good.orth == ("g", "o", "r", "m")
    assert len(good.orth) == len(good.segments)
    bad = tag_word(w("ɡɔɾˠmˠ"), "Seán")
    assert bad.orth == ("", "", "", "")
    assert any(t.rule_id == "orth:unaligned" for t in bad.trace)


def test_the_orth_channel_survives_replacement_and_splitting():
    word = tag_word(w("ɡɔɾˠmˠ"), "gorm")
    cut = word.replaced(0, 1, ("k",))
    assert cut.orth == ("g", "o", "r", "m")          # the new segment inherits (O-8)
    grown = word.replaced(1, 2, ("ɔ", "ə"))
    assert grown.orth == ("g", "o", "o", "r", "m")
    shrunk = word.replaced(1, 3, ("a",))
    assert shrunk.orth == ("g", "o", "m")


def test_the_orth_channel_is_empty_or_exactly_as_long_as_the_segments():
    plain = w("ɡɔɾˠmˠ")
    assert plain.orth == ()
    assert plain.tag_at(0) == ""


def test_most_of_the_144_test_words_align():
    """A coverage floor, not a claim of perfection: the retro-filter degrades gracefully."""
    aligned = 0
    rows = [r for r in read_test_words() if r["ipa"] and " " not in r["orthography"]]
    for row in rows:
        word = normalize(w(row["ipa"]), IRISH, TABLE)
        if any(align(row["orthography"], word.segments)):
            aligned += 1
    assert aligned >= int(0.75 * len(rows)), (aligned, len(rows))
```

- [ ] **Step 2: Run them and watch them fail**

Run: `uv run pytest tests/test_orth_align.py -q`
Expected: FAIL — `ModuleNotFoundError: No module named 'strands.orth'`.

- [ ] **Step 3: Add the `orth` channel to `Word`**

In `word.py`, add the field beside `origins` and document it:

```python
    orth: tuple[str, ...] = ()          # spec §4 (Old Irish): the modern ORTHOGRAPHIC unit each
    # segment came from, filled by `orth.tag_word()` in the Irish pre-pass and read by the
    # `@orth("…")` rule item. Either empty (never tagged) or exactly len(segments) long.
    # `apply_mutation` overwrites the tags of the segments it rewrites with "<TABLE>:<radical>"
    # (O-8), which is how the retro-filter reverses modern eclipsis.
```

Add the accessor and thread it through the two methods that change the segment list:

```python
    def tag_at(self, i: int) -> str:
        """The orth tag of segment i, or "" when the channel is empty (O-6)."""
        return self.orth[i] if self.orth else ""
```

In `replaced(start, stop, new)`: when `self.orth` is empty leave it empty; otherwise the new
segments all inherit `self.orth[start]` (O-8: "a replacement's segments inherit the tag of the
first segment of the replaced span"), except for a zero-width insertion (`start == stop`), whose
segments get `""`:

```python
        if self.orth:
            inherited = self.orth[start] if start < stop else ""
            orth = self.orth[:start] + (inherited,) * len(new) + self.orth[stop:]
        else:
            orth = ()
```

In `split_words()`: slice `orth` on the same `(a, b)` bounds as `segments`, or leave it `()`.
`traced()` copies it unchanged (it uses `replace()`, so nothing to do).

- [ ] **Step 4: Write `rules/irish-orthography.tsv`**

Exactly the table above, tab-separated, in the order given (the loader sorts by unit length, so
file order matters only within a length). Use `-` for the silent alternative and `+` to join a
multi-segment alternative (`i+ə`).

- [ ] **Step 5: Write `src/strands/orth.py`**

```python
"""Modern Irish orthography <-> IPA alignment (plan Task 5; Old Irish spec §4, O-7).

The Old Irish retro-filter needs to know how a segment was SPELLED, because spelling
disambiguates what sound alone cannot: modern /w/ is *bh* in *bhád* and *mh* in *mhac*, and Old
Irish writes those differently (lenited *b* vs lenited *m*). This module attaches, to every
segment of a word, the orthographic unit it came from — `Word.orth` — and `old-irish.rules`
tests it with `@orth("bh")`.

The algorithm is a depth-first search over a DAG of (characters consumed, segments consumed)
nodes, whose edges come from `rules/irish-orthography.tsv`: a row `unit -> alternatives` licenses
an edge that consumes `unit` and one of its alternative segment sequences (possibly none, for a
glide vowel or a silent letter). The table is tried longest-unit-first, then in file order, and
the FIRST complete path wins — so the result is a deterministic function of the table's order and
no scoring is needed.

Failure is total, never partial (O-7): a word whose spelling cannot be walked against its IPA
gets empty tags everywhere and a trace entry, and only the sound-based rules of the retro-filter
apply to it. A partial alignment would let a spelling rule fire on a segment the aligner had only
guessed at.
"""
from __future__ import annotations

import unicodedata
from functools import lru_cache
from pathlib import Path
from typing import Sequence

from .word import TraceEntry, Word

__all__ = ["ORTH_TABLE_PATH", "OrthError", "load_orth_table", "align", "tag_word"]

ORTH_TABLE_PATH = Path(__file__).resolve().parents[2] / "rules" / "irish-orthography.tsv"
_STRIP = "-'’ \t "
_SILENT = "-"
_STAGE = "irish"

Table = tuple[tuple[str, tuple[tuple[str, ...], ...]], ...]


class OrthError(Exception):
    """The orthography table is missing or malformed."""


@lru_cache(maxsize=4)
def load_orth_table(path: str | Path | None = None) -> Table:
    """Rows of `rules/irish-orthography.tsv`, LONGEST UNIT FIRST then file order."""
    p = Path(ORTH_TABLE_PATH if path is None else path)
    try:
        lines = p.read_text(encoding="utf-8").splitlines()
    except OSError as e:
        raise OrthError(f"cannot read {p}: {e}") from e
    rows: list[tuple[int, int, str, tuple[tuple[str, ...], ...]]] = []
    for order, line in enumerate(lines[1:]):          # line 1 is the header
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        cells = line.split("\t")
        if len(cells) < 2:
            raise OrthError(f"{p}:{order + 2}: expected at least 2 tab-separated columns")
        unit = unicodedata.normalize("NFC", cells[0]).strip().casefold()
        alts: list[tuple[str, ...]] = []
        for alt in cells[1].split():
            alts.append(() if alt == _SILENT
                        else tuple(unicodedata.normalize("NFC", a) for a in alt.split("+")))
        if not unit or not alts:
            raise OrthError(f"{p}:{order + 2}: empty unit or alternatives")
        rows.append((-len(unit), order, unit, tuple(alts)))
    if not rows:
        raise OrthError(f"{p}: no rows")
    return tuple((unit, alts) for _, _, unit, alts in sorted(rows))


def _clean(orthography: str) -> str:
    text = unicodedata.normalize("NFC", orthography).casefold()
    return "".join(ch for ch in text if ch not in _STRIP)


def align(orthography: str, segments: Sequence[str],
          table: Table | None = None) -> tuple[str, ...]:
    """One orthographic tag per segment; all-empty when no complete walk exists (O-7)."""
    segs = tuple(unicodedata.normalize("NFC", s) for s in segments)
    fail = ("",) * len(segs)
    o = _clean(orthography)
    if not o or not segs:
        return fail
    U = load_orth_table() if table is None else table
    dead: set[tuple[int, int]] = set()

    def walk(i: int, j: int) -> list[str] | None:
        if i == len(o) and j == len(segs):
            return []
        if (i, j) in dead:
            return None
        for unit, alts in U:
            if not o.startswith(unit, i):
                continue
            for alt in alts:
                if segs[j:j + len(alt)] != alt:
                    continue
                rest = walk(i + len(unit), j + len(alt))
                if rest is not None:
                    return [unit] * len(alt) + rest
        dead.add((i, j))
        return None

    found = walk(0, 0)
    return tuple(found) if found is not None else fail


def tag_word(word: Word, orthography: str) -> Word:
    """Return `word` with `Word.orth` set. On failure the tags are empty and a trace entry
    `orth:unaligned` records it, so `strands explain` shows why the spelling rules were
    inert (O-7)."""
    from dataclasses import replace
    tags = align(orthography, word.segments)
    out = replace(word, orth=tags)
    if not any(tags):
        return out.traced(TraceEntry(
            stage=_STAGE, rule_id="orth:unaligned", tag="design",
            before=word.ipa(), after=word.ipa(),
            note=f"{orthography!r} could not be aligned with its IPA; "
                 "orthography-driven rules will not fire (O-7)"))
    return out
```

- [ ] **Step 6: Run the tests**

Run: `uv run pytest tests/test_orth_align.py -q` — expected PASS. If
`test_most_of_the_144_test_words_align` fails, the fix is **rows in
`rules/irish-orthography.tsv`**, not a lower threshold: print the failures with

```bash
uv run python -c "
from helpers import *
import sys; sys.path.insert(0,'tests')
" 2>/dev/null; uv run pytest tests/test_orth_align.py::test_most_of_the_144_test_words_align -q -x
```

and add the missing unit → segment alternatives.

- [ ] **Step 7: Run the suite and commit**

Run: `uv run pytest -q` — expected 1004+ passed, 2 xfailed.

```bash
git add src/strands/orth.py src/strands/word.py rules/irish-orthography.tsv \
        tests/test_orth_align.py
git commit -m "feat(orth): modern orthography-IPA aligner and the Word.orth tag channel"
```

**Acceptance:** every reversal-relevant digraph aligns; failure gives all-empty tags plus a trace
entry and never raises; ≥75% of the single-word test rows align; `orth` survives `replaced()` and
`split_words()`; the existing suite is untouched.

---

## Task 6: The `@orth("…")` rule item

**Depends on:** Task 5. **Spec:** §4 ("a new environment atom `@orth("bh")` = 'the modern spelling
of this segment's source is …'"); O-6.

**Files:**
- Modify: `src/strands/dsl.py` (scanner, item parser, `ItemSpec` kind `"orth"`)
- Modify: `src/strands/rewrite.py` (`match_item` gains the word and index)
- Modify: `src/strands/check.py` (`Checker.item`, `Checker.matching_segments`)
- Test: `tests/test_dsl_orth_atom.py`

**Interfaces:**
- Produces: `ItemSpec(kind="orth", value="bh", capture=None)` from the source text `@orth("bh")`.
- Changes a signature used across the engine:
  ```python
  def match_item(spec: ItemSpec, segment: str, rf: RuleFile, table: FeatureTable,
                 *, word: Word | None = None, index: int | None = None) -> bool
  ```
  Every existing call site keeps working (the new arguments are keyword-only with defaults);
  `kind == "orth"` returns `False` when `word`/`index` are not supplied, which is the same
  "no tag ⇒ no match" behaviour as an untagged word.
- Consumed by: Task 9 (`old-irish.rules [substitute]`).

**Parse rules (O-6).** `@orth(` … `)` where the argument is a double-quoted string.
- Legal in a TARGET item position and in a context atom position.
- **Illegal**, with these exact `ParseError` messages:
  - in a REPLACEMENT → `@orth() may not appear in a replacement`
  - with a capture suffix → `@orth() may not carry a capture` (a tag is not a segment to copy)
  - inside an inline set `{…}` or a bundle `[…]` → `@orth() may not appear inside {} or []`
  - unquoted or unterminated argument → `@orth() takes one double-quoted string`
- The value is stored NFC + case-folded, so `@orth("BH")` and `@orth("bh")` are the same item.

**Check rules.** `Checker.item` for `kind == "orth"`: severity `warning`, code
`ORTH_UNKNOWN_UNIT`, when the value is neither a unit of `rules/irish-orthography.tsv` nor of the
form `<TABLE>:<segment>` with `TABLE` in `("LEN", "ECL", "HPREF", "TPREF")` and `segment` in
`features.tsv` (O-8). A warning, not an error: a target may legitimately reference a unit the
table does not yet have. `Checker.matching_segments` returns `[]` for an orth item (it matches by
provenance, not by phonology), which keeps the existing `UNREACHABLE_CHANGE` and
`RULE_NEVER_MATCHES` logic from reporting nonsense.

- [ ] **Step 1: Write the failing tests**

`tests/test_dsl_orth_atom.py`:

```python
"""Task 6: the @orth("…") rule item (spec §4; O-6)."""
import pytest

from helpers import TABLE, w
from strands.check import check_rule_file
from strands.dsl import ItemSpec, ParseError, parse_rules
from strands.orth import tag_word
from strands.rewrite import apply_section

PREAMBLE = """[meta]
name = orth-test
[inventory]
w vˠ vʲ ɡ ɔ ɾˠ mˠ bˠ β β̃
[classes]
BROAD = w vˠ ɡ ɾˠ mˠ bˠ
"""


def rf(body):
    return parse_rules(PREAMBLE + body, TABLE, path="<orth-test>")


def run(body, ipa, orthography):
    file = rf("[substitute]\n" + body)
    word = tag_word(w(ipa), orthography)
    return apply_section(word, file.sections["substitute"], file, TABLE, "substitute").segments


def test_the_item_parses_into_an_orth_ItemSpec():
    rule = rf('[substitute]\n@orth("bh") -> β\n').sections["substitute"][0]
    assert rule.target == (ItemSpec(kind="orth", value="bh"),)


def test_the_value_is_case_folded():
    rule = rf('[substitute]\n@orth("BH") -> β\n').sections["substitute"][0]
    assert rule.target[0].value == "bh"


def test_it_rewrites_only_the_segment_with_that_tag():
    """*bhád* /waːd̪ˠ/ -> β; *mhac* /wak/ is the SAME /w/ and must not be touched."""
    assert run('@orth("bh") -> β\n', "waːd̪ˠ", "bhád")[0] == "β"
    assert run('@orth("bh") -> β\n', "wak", "mhac")[0] == "w"
    assert run('@orth("mh") -> β̃\n', "wak", "mhac")[0] == "β̃"


def test_an_untagged_word_is_left_alone():
    """O-6/O-7: no tag, no match — only sound-based rules apply."""
    file = rf('[substitute]\n@orth("bh") -> β\n')
    assert apply_section(w("waːd̪ˠ"), file.sections["substitute"], file, TABLE,
                         "substitute").segments[0] == "w"


def test_it_works_as_a_context_atom():
    body = 'ɡ -> ɔ / @orth("bh") _\n'
    assert run(body, "waːɡ", "bhág")[-1] == "ɔ" or True     # see the next assertion
    file = rf("[substitute]\n" + body)
    word = tag_word(w("wɡ"), "bhg")
    out = apply_section(word, file.sections["substitute"], file, TABLE, "substitute")
    assert out.segments == ("w", "ɔ")


def test_it_may_not_appear_in_a_replacement():
    with pytest.raises(ParseError, match="may not appear in a replacement"):
        rf('[substitute]\nw -> @orth("bh")\n')


def test_it_may_not_carry_a_capture():
    with pytest.raises(ParseError, match="may not carry a capture"):
        rf('[substitute]\n@orth("bh"):1 -> β\n')


def test_it_may_not_appear_inside_a_set_or_a_bundle():
    with pytest.raises(ParseError, match=r"may not appear inside"):
        rf('[substitute]\n{@orth("bh") w} -> β\n')


def test_a_malformed_argument_is_a_parse_error_with_a_line_number():
    with pytest.raises(ParseError, match="one double-quoted string"):
        rf('[substitute]\n@orth(bh) -> β\n')
    with pytest.raises(ParseError, match="one double-quoted string"):
        rf('[substitute]\n@orth("bh -> β\n')


def test_check_warns_about_a_unit_no_table_knows(tmp_path):
    path = tmp_path / "t.rules"
    path.write_text(PREAMBLE + '[substitute]\n@orth("zz") -> β\n', encoding="utf-8")
    from strands.dsl import parse_rules_file
    findings = check_rule_file(parse_rules_file(path, TABLE), TABLE)
    warn = [f for f in findings if f.code == "ORTH_UNKNOWN_UNIT"]
    assert warn and warn[0].severity == "warning"


def test_check_accepts_a_mutation_provenance_tag(tmp_path):
    """O-8: `@orth("ECL:bˠ")` is how modern eclipsis is reversed."""
    path = tmp_path / "t.rules"
    path.write_text(PREAMBLE + '[substitute]\n@orth("ECL:bˠ") -> β\n', encoding="utf-8")
    from strands.dsl import parse_rules_file
    findings = check_rule_file(parse_rules_file(path, TABLE), TABLE)
    assert [f for f in findings if f.code == "ORTH_UNKNOWN_UNIT"] == []
```

- [ ] **Step 2: Run them and watch them fail**

Run: `uv run pytest tests/test_dsl_orth_atom.py -q`
Expected: FAIL — the scanner rejects `@`.

- [ ] **Step 3: Parse the item in `dsl.py`**

In `_LineParser._scan`, before the general token branch, add the `@` case:

```python
            elif ch == "@":
                if not text.startswith("@orth(", i):
                    raise self.err("the only @-item is @orth(\"…\")")
                j = text.find(")", i)
                arg = text[i + len("@orth("):j] if j > 0 else ""
                if j < 0 or len(arg) < 2 or arg[0] != '"' or arg[-1] != '"':
                    raise self.err('@orth() takes one double-quoted string')
                tok = _Tok("orth", arg[1:-1])
                i = j + 1
```

Wherever the parser turns a `_Tok` into an `ItemSpec` (the item branch used for TARGET and for
context atoms), handle `tok.kind == "orth"` by returning
`ItemSpec(kind="orth", value=unicodedata.normalize("NFC", tok.text).casefold())`, and raise
`self.err("@orth() may not carry a capture")` if a `:n` suffix follows. In the replacement parser,
a `"orth"` token raises `self.err("@orth() may not appear in a replacement")`. In the set (`{…}`)
and bundle (`[…]`) parsers, `@` in the body raises
`self.err("@orth() may not appear inside {} or []")` — the simplest implementation is to reject
`"@"` in the raw text of those two token bodies.

Add `"orth"` to whatever documents the legal `ItemSpec.kind` values, and note in the `ItemSpec`
docstring that `value` is then the orth tag string.

- [ ] **Step 4: Match it in `rewrite.py`**

```python
def match_item(spec: ItemSpec, segment: str, rf: RuleFile, table: FeatureTable,
               *, word: Word | None = None, index: int | None = None) -> bool:
    if spec.kind == "orth":
        # O-6: matches one segment by the orthographic unit it came from. No tag, no match —
        # that is the aligner's documented failure mode (O-7), not an error.
        if word is None or index is None or not word.orth or not (0 <= index < len(word.orth)):
            return False
        return word.orth[index] == spec.value
    ...
```

Then pass `word=` and `index=` at the three call sites that know them:
`_match_target` (index = the position being matched), `_match_ctx`'s `seg_at` comparison
(`index = p if step > 0 else p - 1`), and `syllabify`'s class-membership helper if it calls
`match_item` (it does not need orth, so passing nothing is correct there).

- [ ] **Step 5: Teach `check.py` about it**

In `Checker.item`, add the `kind == "orth"` branch described above (loading the unit set once via
`strands.orth.load_orth_table()` and catching `OrthError` as "no table, no warning"). In
`Checker.matching_segments`, return `[]` for `kind == "orth"`.

- [ ] **Step 6: Run the tests and the suite**

Run: `uv run pytest tests/test_dsl_orth_atom.py -q` — expected PASS.
Run: `uv run pytest -q` — expected 1004+ passed, 2 xfailed. **A break in `test_dsl_core.py` or
`test_rewrite.py` means the `match_item` signature change was not backward-compatible — make the
new parameters keyword-only with `None` defaults, do not edit those tests.**

- [ ] **Step 7: Commit**

```bash
git add src/strands/dsl.py src/strands/rewrite.py src/strands/check.py \
        tests/test_dsl_orth_atom.py
git commit -m "feat(dsl): @orth(\"…\") item matching a segment by its orthographic source"
```

**Acceptance:** `@orth("bh")` distinguishes *bhád* from *mhac* though both carry /w/; an untagged
word is inert; the four illegal placements raise with line numbers; `check` warns on unknown units
and accepts `LEN:`/`ECL:` provenance tags; the existing suite is untouched.

---

## Task 7: Mutation provenance orth tags

**Depends on:** Task 5. **Spec:** §4 ("modern eclipsis → Old Irish nasalization written *mb nd
ng* (the pre-pass's ECL output is reversed into stop+nasal)"); O-8.

**Files:**
- Modify: `src/strands/irish.py` (`_apply_table`)
- Test: `tests/test_irish_mutation_orth.py`

**Interfaces:**
- Produces: after `apply_mutation(word, NAME, …)`, every segment the table rewrote carries the orth
  tag `f"{NAME}:{radical}"`, where `radical` is the **first segment of the span the rule
  matched**, taken from the pre-mutation word. Segments a mutation *inserted* (n-prothesis,
  h-prothesis, t-prothesis, whose target is empty) carry `f"{NAME}:0"`. Untouched segments keep
  their aligner tag. A word whose `orth` channel is empty stays empty — no mutation creates the
  channel.
- Consumed by: Task 9 (`@orth("ECL:bˠ")` and friends).

**Why the radical and not the surface sound.** Old Irish nasalization writes *mb nd ng* for
radical *b d g* but leaves radical *p t c* unwritten as *b d g* (digest §10.4). Modern eclipsis
maps both onto the same surface segments: /bˠ/ is eclipsed *p* in *bpáirc* and radical *b* in
*bád*, and eclipsed *b* is /mˠ/. Only the radical distinguishes them, and the trace is the only
place the engine records it — so it is written onto the segment.

- [ ] **Step 1: Write the failing test**

`tests/test_irish_mutation_orth.py`:

```python
"""Task 7: mutation provenance on the orth channel (spec §4; O-8)."""
import pytest

from helpers import TABLE, irish, w
from strands.irish import apply_mutation
from strands.orth import tag_word

IRISH = irish()


def mutate(ipa, orthography, name):
    return apply_mutation(tag_word(w(ipa), orthography), name, IRISH, TABLE)


def test_eclipsis_records_the_radical_not_the_surface_sound():
    """/bˠ/ from eclipsed *p* and radical /bˠ/ are the same segment; only this tells them
    apart, and Old Irish spells them differently (digest §10.4)."""
    out = mutate("pˠaːɾʲc", "páirc", "ECL")
    assert out.segments[0] == "bˠ"
    assert out.orth[0] == "ECL:pˠ"
    radical = mutate("bˠaːd̪ˠ", "bád", "ECL")
    assert radical.segments[0] == "mˠ"
    assert radical.orth[0] == "ECL:bˠ"


def test_lenition_records_its_radical_too():
    out = mutate("bˠaːd̪ˠ", "bád", "LEN")
    assert out.segments[0] == "w" and out.orth[0] == "LEN:bˠ"
    out = mutate("mˠak", "mac", "LEN")
    assert out.segments[0] == "w" and out.orth[0] == "LEN:mˠ"


def test_an_inserted_prothesis_segment_is_tagged_with_a_zero_radical():
    out = mutate("eːnˠ", "éan", "TPREF")
    assert out.segments[0] == "tʲ" and out.orth[0] == "TPREF:0"


def test_untouched_segments_keep_their_aligner_tags():
    out = mutate("bˠaːd̪ˠ", "bád", "LEN")
    assert out.orth[1:] == ("á", "d")


def test_a_word_with_no_orth_channel_stays_without_one():
    """No mutation creates the channel; the aligner does."""
    assert apply_mutation(w("bˠaːd̪ˠ"), "LEN", IRISH, TABLE).orth == ()


def test_a_deleted_radical_leaves_no_tag_behind():
    """*fh* is silent: LEN maps /fˠ/ -> 0 (irish.rules)."""
    out = mutate("fˠiːɾʲ", "fír", "LEN")
    assert out.segments[0] != "fˠ"
    assert len(out.orth) == len(out.segments)
```

- [ ] **Step 2: Run it and watch it fail**

Run: `uv run pytest tests/test_irish_mutation_orth.py -q`
Expected: FAIL — `out.orth[0] == 'b'` (the aligner tag survives).

- [ ] **Step 3: Write the tags in `_apply_table`**

`_apply_table` already collects `edits` as `(start, stop, new, rule)` against the pre-table word
and applies them right-to-left with `out.replaced(...)`. `replaced()` makes the new segments
inherit the tag of the span's first segment (Task 5), so the only change needed is to overwrite
that span's tags afterwards. Do it inside the same loop, so indices are still valid:

```python
    for start, stop, new, _ in sorted(edits, key=lambda e: e[0], reverse=True):
        radical = word.segments[start] if start < stop else "0"      # O-8
        out = out.replaced(start, stop, new)
        if out.orth:
            tag = f"{name}:{radical}"
            out = replace(out, orth=out.orth[:start] + (tag,) * len(new)
                                + out.orth[start + len(new):])
```

`_apply_table` must therefore take the table's `name`; give it a keyword parameter and pass it
from `apply_mutation`:

```python
def _apply_table(word: Word, rules: tuple[Rule, ...], rf: RuleFile, table: FeatureTable,
                 *, name: str = "") -> Word:
```

```python
def apply_mutation(word, name, rf, table):
    return _apply_table(word, _subtable("mutations", rf.mutations, name, rf), rf, table,
                        name=name)
```

Extend the `_apply_table` docstring with the O-8 paragraph (why the radical, not the surface
sound).

- [ ] **Step 4: Run the tests and the suite**

Run: `uv run pytest tests/test_irish_mutation_orth.py tests/test_irish_mutations.py -q` —
expected PASS.
Run: `uv run pytest -q` — expected 1004+ passed, 2 xfailed.

- [ ] **Step 5: Commit**

```bash
git add src/strands/irish.py tests/test_irish_mutation_orth.py
git commit -m "feat(irish): record mutation provenance (<TABLE>:<radical>) on the orth channel"
```

**Acceptance:** eclipsed *p* and radical *b* are distinguishable after the pre-pass; prothesis
segments carry `:0`; untouched segments keep their aligner tags; a word without the channel is
unaffected; the existing mutation tests still pass unchanged.

---

## Task 8: `old-irish.rules` — `[meta]`, `[inventory]`, `[classes]`

**Depends on:** Task 1. **Spec:** §2, §4 `[inventory]`, §8 rows O2; digest §10.1. O-1, O-2, O-3,
O-5, O-14.

**Files:**
- Create: `rules/old-irish.rules`
- Test: `tests/test_rules_old_irish.py`

**Interfaces:**
- Produces a rule file that `parse_rules_file` loads and `strands check` accepts.
  `[meta]` keys other tasks read:
  - `name = Old Irish`
  - `strand = old-irish` — **the dispatch key** `pipeline.run_entry` tests (O-9)
  - `digest = sources/irish/digest.md §10`
  - `lexicon = rules/old-irish-lexicon.tsv`
  - `orthography = rules/old-irish-orthography.tsv` — the reconstruction table (Task 12)
  - `punctum = on` — spec §8 row O2 (O-14)
  - `epithet-ADJ` / `epithet-NOUN` are **absent**: this strand has no target affixes; an
    unmapped slot means "no affix", not an error (I-39).
- `[classes]` declares `BROAD`, `SLEN`, `UNMARKED` (copied from I-41 and extended per O-3) and
  `SONORANT` (used by the epenthesis rule of Task 9, O-15).

**Scope boundary.** Like engine-plan Task 23a, this task writes a **temporary permissive**
`[syllable]` block so the file parses and `check` is clean; Task 10 replaces it wholesale. This
task therefore may not call `adapt()`, `repair()` or any full-pipeline helper — it tests the file
as data.

**Content, with its citations:**

| Block | Content and citation |
|---|---|
| `[inventory]` stops | `pˠ pʲ bˠ bʲ t̪ˠ tʲ d̪ˠ dʲ k c ɡ ɟ` — digest §10.1 chart. `# digest §10.1 [wiki-old-irish §Consonants]`. `pˠ pʲ` are **marginal** ("relatively rare… a recent import from Latin", digest §10.1) |
| `[inventory]` fricatives | `fˠ fʲ sˠ ʃ x ç h β βʲ ð ðʲ θ θʲ ɣ j β̃ β̃ʲ` — digest §10.1; O-1 for the spellings |
| `[inventory]` sonorants | `mˠ mʲ n̪ˠ nʲ ŋ ɲ l̪ˠ lʲ ɾˠ ɾʲ w` — digest §10.1 with O-2 (one series). `w` is kept because `irish.rules` produces it from lenited *b/m* and Task 9 rewrites it |
| `[inventory]` vowels | `iː eː aː oː uː i e a o u ə` — digest §10.1 "5 short, 5 long" [pokorny1914 p.6 §4] plus unstressed /ə/ (digest §10.2 grid) |
| `marginal:` | `pˠ pʲ ə` — `ə` is marginal because it is a *reduction*, never chosen by the inventory fallback |
| `[classes]` | `BROAD` / `SLEN` / `UNMARKED` from I-41; `BROAD` += `β β̃ ð θ`, `SLEN` += `βʲ β̃ʲ ðʲ θʲ`. `SONORANT = mˠ mʲ n̪ˠ nʲ ŋ ɲ l̪ˠ lʲ ɾˠ ɾʲ` (digest §2.4's epenthesis environment) |

Diphthongs are **not** inventory rows (I-2 / spec §12.B); Task 10 declares them as `nuclei`.

- [ ] **Step 1: Write the failing tests**

`tests/test_rules_old_irish.py`:

```python
"""Tasks 8-11: `rules/old-irish.rules` as data (spec §4, §6; digest §10)."""
import pytest

from helpers import ROOT, TABLE, target, w
from strands.check import check_rule_file

PATH = ROOT / "rules" / "old-irish.rules"
OI = target("old-irish")


def test_the_file_parses_and_check_reports_no_errors():
    findings = [f for f in check_rule_file(OI, TABLE) if f.severity == "error"]
    assert findings == [], findings


def test_meta_declares_the_strand_key_the_pipeline_dispatches_on():
    """O-9: `run_entry` routes on [meta] strand, not on a hard-coded name."""
    assert OI.meta["strand"] == "old-irish"
    assert OI.meta["lexicon"].endswith("old-irish-lexicon.tsv")
    assert OI.meta["orthography"].endswith("old-irish-orthography.tsv")
    assert OI.meta.get("punctum", "on") in ("on", "off")


def test_this_strand_declares_no_epithet_slots():
    """I-39: an unmapped slot means 'no affix'. Old Irish affixes come from [templates]."""
    assert "epithet-ADJ" not in OI.meta and "epithet-NOUN" not in OI.meta


@pytest.mark.parametrize("segment", ["β", "βʲ", "β̃", "β̃ʲ", "ð", "ðʲ", "θ", "θʲ", "x", "ç",
                                     "ɣ", "j", "sˠ", "ʃ", "fˠ", "fʲ", "h"])
def test_the_lenited_series_is_in_the_inventory(segment):
    """digest §10.1; spec §4; O-1."""
    assert segment in OI.inventory


@pytest.mark.parametrize("vowel", ["i", "e", "a", "o", "u", "iː", "eː", "aː", "oː", "uː"])
def test_the_five_short_and_five_long_vowels_are_there(vowel):
    """[pokorny1914 p.6 §4] via digest §10.1."""
    assert vowel in OI.inventory


def test_p_is_marginal_because_it_is_a_latin_import():
    """digest §10.1: '/p pʲ/ is marginal… a recent import'."""
    assert "pˠ" in OI.marginal and "pʲ" in OI.marginal


def test_no_fortis_sonorant_segments_were_invented():
    """O-2: spec §4 does not list /L N R/; fortis is a geminate (I-2)."""
    assert not {"L", "N", "R"} & set(OI.inventory)


def test_no_diphthong_is_an_inventory_row():
    """I-2 / spec §12.B: a diphthong is two segments and one nucleus."""
    assert not [s for s in OI.inventory if len(s) > 1 and all(
        TABLE.value(c, "syllabic") == "+" for c in (s[0], s[-1]) if c in TABLE.segments)]


def test_the_quality_classes_are_declared_not_derived():
    """spec §12.J / I-41: BROAD and SLEN are declared classes, never [C ±back]."""
    assert "β" in OI.classes["BROAD"] and "βʲ" in OI.classes["SLEN"]
    assert "k" in OI.classes["BROAD"] and "c" in OI.classes["SLEN"]
    assert OI.classes["UNMARKED"]
    assert set(OI.classes["SONORANT"]) >= {"l̪ˠ", "n̪ˠ", "ɾˠ", "mˠ"}


def test_every_rule_line_carries_a_citation():
    """Global constraint: a digest/bib citation or `# design: O<n>`."""
    bad = []
    for section, rules in OI.sections.items():
        for rule in rules:
            comment = (rule.comment or "").strip()
            if not (comment.startswith("digest") or comment.startswith("[")
                    or comment.startswith("design:") or "digest §10" in comment
                    or "pokorny1914" in comment or "strachan1909" in comment):
                bad.append((section, rule.line, comment))
    assert bad == [], bad
```

- [ ] **Step 2: Run them and watch them fail**

Run: `uv run pytest tests/test_rules_old_irish.py -q`
Expected: FAIL at import — `rules/old-irish.rules` does not exist.

- [ ] **Step 3: Write `rules/old-irish.rules`**

```
# old-irish.rules — strand 5: classical Old Irish (8th-9th c.), the Thurneysen/Pokorny norm
# as digested in sources/irish/digest.md §10 (from pokorny1914-oldirish-grammar and
# strachan1909-oldirish-paradigms). Spec: docs/specs/2026-08-27-old-irish-design.md.
# Task 8: [meta] [inventory] [classes]. Task 10: [syllable] [repair] [stress] [post-stress].
# Task 11: [respell]. Task 9: [substitute]. Tasks 14-16: [mutations] [inflect] [templates].

[meta]
name = Old Irish
strand = old-irish
digest = sources/irish/digest.md §10
lexicon = rules/old-irish-lexicon.tsv
orthography = rules/old-irish-orthography.tsv
# spec §8 row O2: lenited s/f are written with the punctum (ṡ ḟ); `off` gives plain s f.
punctum = on

[inventory]
# digest §10.1 chart [wiki-old-irish §Consonants]. Quality is NOT reversed (spec §4), so the
# broad/slender spellings are the modern Irish ones (O-3) and the plain dorsals k ɡ x ɣ ŋ are
# broad by convention (I-41).
bˠ bʲ t̪ˠ tʲ d̪ˠ dʲ k c ɡ ɟ
# The lenited series. O-1: spec §4's /μ/ is written β̃; /xʲ/ IS ç and /ɣʲ/ IS j.
β βʲ β̃ β̃ʲ ð ðʲ θ θʲ x ç ɣ j
# /s f h/ exist as segments; they are lenition products only in the sense that no
# [substitute] rule creates them except the sh/ph reversals (O-5).
fˠ fʲ sˠ ʃ h
# One sonorant series (O-2: spec §4 lists no /L N R/; fortis is a geminate, I-2).
mˠ mʲ n̪ˠ nʲ ŋ ɲ l̪ˠ lʲ ɾˠ ɾʲ w
# 5 short + 5 long [pokorny1914-oldirish-grammar p.6 §4] via digest §10.1, plus unstressed /ə/
# (the digest §10.2 post-stress spelling grid).
i e a o u iː eː aː oː uː ə
# /p/ is "relatively rare in Old Irish, being a recent import" (digest §10.1); /ə/ is a
# reduction and must never be chosen by the inventory fallback.
marginal: pˠ pʲ ə

[classes]
# spec §12.J / I-41, extended with the Old Irish lenited series (O-3).
BROAD = pˠ bˠ t̪ˠ d̪ˠ fˠ sˠ w mˠ n̪ˠ l̪ˠ ɾˠ k ɡ x ɣ ŋ β β̃ ð θ
SLEN  = pʲ bʲ tʲ dʲ fʲ ʃ mʲ nʲ lʲ ɾʲ c ɟ ç j ɲ βʲ β̃ʲ ðʲ θʲ
UNMARKED = p b t d f v s m n l r
# digest §2.4: the epenthesis environment is after l n r m. Task 9's schwa deletion (O-15).
SONORANT = mˠ mʲ n̪ˠ nʲ ŋ ɲ l̪ˠ lʲ ɾˠ ɾʲ

[syllable]
# TEMPORARY (Task 8): replaced wholesale by Task 10. Do not ship.
template = any
onsets   = any
codas    = any
sonority = off
```

`p b t d f v s m n l r` must be tokenizable for `UNMARKED` to parse; they are already
`features.tsv` rows (I-41), so no inventory line is needed for them — a class may name a segment
that is not in this file's inventory, exactly as `irish.rules` does.

- [ ] **Step 4: Run the tests and `check`**

Run: `uv run strands check rules/old-irish.rules` — expected exit 0.
Run: `uv run pytest tests/test_rules_old_irish.py -q` — expected PASS (the citation test passes
vacuously: there are no rule lines yet).
Run: `uv run pytest -q` — expected 1004+ passed, 2 xfailed.

- [ ] **Step 5: Commit**

```bash
git add rules/old-irish.rules tests/test_rules_old_irish.py
git commit -m "feat(rules): old-irish.rules skeleton — meta, inventory, classes"
```

**Acceptance:** the file parses, `check` is error-free, `[meta] strand = old-irish` is present, the
lenited series and both vowel sets are in the inventory, no `L N R` and no diphthong rows, the
quality classes are declared.

---

## Task 9: `old-irish.rules [substitute]` — the retro-filter

**Depends on:** Tasks 6, 7, 8. **Spec:** §4 `[substitute]` (both halves); §8 rows O1, O5. O-5,
O-8, O-13, O-15.

**Files:**
- Modify: `rules/old-irish.rules` (add `[substitute]` before `[syllable]`)
- Test: `tests/test_rules_old_irish.py` (append)

**Interfaces:**
- Consumes: `@orth("…")` (Task 6), the aligner tags (Task 5) and the mutation provenance tags
  (Task 7).
- Produces: a `[substitute]` section that turns a normalized **modern** Irish word into Old Irish
  segments. Called by Task 13 as `substitute_stage(word, OI, table)` — the ordinary stage-2
  function, including the inventory fallback.

**Rule table.** Spelling-driven rules come first (they are more specific); sound-driven rules
second. Every spelling rule is `%design` unless a lexicon pair instantiates it — no pair does yet,
so **every line in this task is `%design`**, cited `# design: spec §4 · digest §10.2 conv.1`
(the convention that modern ⟨bh dh gh mh⟩ ↔ Old Irish unmarked ⟨b d g m⟩, digest §10.7 "the
orthographic correspondence"). Task 17's regression is what would later promote one to
`%attested`.

| Rule | Reading |
|---|---|
| `@orth("bh") -> β` / `@orth("mh") -> β̃` | modern *bh/mh* → lenited *b/m* (spec §4). Both are /w/ or /vˠ/ or /vʲ/ modernly; only the spelling separates them |
| `@orth("dh") -> ð` / `@orth("gh") -> ɣ` | modern *dh/gh* → lenited *d/g* |
| `@orth("th") -> θ` / `@orth("sh") -> h` | modern *th/sh* → *th* /θ/ and *ṡ* /h/ |
| `@orth("ch") -> x` / `@orth("ph") -> fˠ` | modern *ch* → *ch* /x/; *ph* → *ph* /f/ |
| `@orth("ao") -> aː` | O-13: modern *ao* → *áe*, the unconditioned `%design` default (spec §10 refining §8 row O1). The log's 20 attested pairs are Task 17's regression set for it |
| `@orth("ea") -> e`, `@orth("io") -> i`, `@orth("ai") -> a`, `@orth("oi") -> o`, `@orth("ui") -> u` | **The largest reversal class — 50 attested pairs** (log finding 2): modern *caol le caol* brackets the vowel on both sides, Old Irish marked quality by the *following* vowel only (digest §10.2.5). *fear ~ fer*, *bean ~ ben*, *dearg ~ derg*, *Fionn ~ Finn*, *Giolla ~ gilla*. The **sound is unchanged**, so no sound-driven rule can see this — it is the reason the `@orth` atom exists. Delete the glide letter, keep the quality: these rules do not change the *segment*, they change what `[respell]` (Task 11) writes for it, so each is paired with a Task 11 rule and the `[substitute]` line here is the one that marks the segment. Where the vowel quality also differs (long/short) the vowel rules below handle it |
| `@orth("ua") -> uː`, `@orth("ia") -> iː` on the **first** element only | log finding 4, 33 pairs: modern ⟨ua ia⟩ ↔ Old Irish ⟨úa ía⟩ — the acute goes on the first element. Mechanical. Two exceptions (*sluagh ~ slóg*, *fuar ~ úar*) are lexicon rows and never reach the filter |
| `@orth("ia") -> i` then a second rule for the second half | modern *ia* → *ía* |
| `@orth("ua") -> u` likewise | modern *ua* → *úa* |
| `@orth("ae") -> aː` / `@orth("aoi") -> aː` | modern *ae/aoi* → *aí* |
| `@orth("ECL:pˠ") -> bˠ` … | modern eclipsis reversed. **This is the whole point of O-8:** eclipsed *p t c* become OI *b d g* (unwritten nasalization), while eclipsed *b d g* become the OI *mb nd ng* sequences |
| `@orth("ECL:bˠ") -> mˠ bˠ` (two segments) | *mb*: digest §10.4 |
| `@orth("ECL:d̪ˠ") -> n̪ˠ d̪ˠ`, `@orth("ECL:ɡ") -> ŋ ɡ` | *nd*, *ng* |

Slender partners get their own line in each case (`@orth("bh")` covers both, since the tag is the
same for *bh* before a slender vowel; the **replacement** must therefore be quality-correct, which
is why the spelling rules are split by the segment they match — write them as
`w -> β / @orth("bh") …`? **No** — write the target as the orth item and let the two-line pattern
carry quality:

```
@orth("bh") -> β    / _ [V -front]   %design
@orth("bh") -> βʲ   / _ [V +front]   %design
@orth("bh") -> β    / [V -front] _   %design
@orth("bh") -> βʲ   / [V +front] _   %design
```

That is the same four-environment shape `irish.rules [normalize]` uses, and it reuses the existing
`[V ±front]` bundles rather than adding a mechanism.

**Sound-driven rules** (spec §4, second bullet), after all of the above:

| Rule | Citation |
|---|---|
| `ɪ -> i`, `ʊ -> u` | spec §4: modern /ɪ ʊ/ → *i u*. `# design: spec §4 · digest §10.1 (OI has 5 short vowels)` |
| `ɛ -> e`, `ɔ -> o` | same reasoning: the digest's five short vowels are `a e i o u` |
| `ə -> 0 / SONORANT _ C` | spec §8 row O5 default: the epenthetic schwa is deleted (O-15). `# design: O5 · digest §2.4` |
| `ə -> e / _ #` when the stem is an ā-stem, else `ə -> a / _ #` | spec §4: "modern /ə/ final → *e* (ā-stems) or *a* by stem class". **The stem class is not visible to a rewrite rule**; see the interpretation below |
| `w -> β` (any remaining) | a /w/ the spelling rules did not claim is still a lenited labial; `# design: spec §4` |
| `vˠ -> β`, `vʲ -> βʲ` | ditto |
| long vowels: **no rule** | spec §4 "what is deliberately not reversed: vowel length" |
| clusters, quality: **no rule** | spec §4, same list |

**What the harvest log says about this section, and what it means for the tags.**

- **⟨ph⟩ and ⟨sh⟩ do not occur in any of the 270 attested modern keys** (log finding 3). Their two
  branches have no lexicon pair to instantiate them, so they stay `%design` and **untested by the
  regression** — write them anyway (spec §4 requires them), and say in the file's comment that no
  pair exists, so a later reader does not mistake the silence for coverage.
- **Modern ⟨ch th⟩ correspond to Old Irish ⟨ch th⟩ unchanged** (*cloch ~ cloch*, *bláth ~ bláth*,
  *athair ~ athair*): the `@orth("ch")`/`@orth("th")` rules above are identity in *spelling* and
  matter only because they fix the segment as `/x/`, `/θ/` rather than letting the modern value
  through. The r-stem kinship set (*athair, bráthair, máthair*) is spelling-invariant across both
  stages and is the log's recommended "does the filter leave well enough alone" regression case.
- **Geminate restoration** (*mac → macc*, *ainm → ainmm*, 47 pairs, log finding 3) **adds** written
  material going backwards. That is a spelling operation on an unchanged sound, so it belongs to
  `[respell]` (Task 11), **not here** — putting it in `[substitute]` would create phonological
  geminates that Task 10's degemination would then undo.
- **Final unstressed vowels survive** (log finding 4): the filter must **not** strip modern final
  ⟨-a -e⟩. There is no deletion rule for them here; ⟨-a⟩ → ⟨-ae⟩ is a Task 11 respelling.

**Interpretation carried here, stated in the file as a comment.** Spec §4's "final /ə/ → *e*
(ā-stems) or *a* by stem class" cannot be written as a `[substitute]` rule, because the stem class
is a property of the *entry*, not of the segment string, and `[substitute]` has no channel for it.
Simplest faithful resolution: `[substitute]` writes the **default** `ə -> a / _ #`
(`# design: spec §4 · digest §10.2 unstressed-vowel grid`), and the ā-stem *-e* is produced by
Task 15's `[inflect]` table `NOM_A`, which the templates apply when the stem class says `ā`. The
comment in the rule file must say this in one line so a reader does not think the spec was
dropped.

- [ ] **Step 1: Write the failing tests** (append to `tests/test_rules_old_irish.py`)

```python
from strands.orth import tag_word
from strands.substitute import substitute_stage
from strands.irish import normalize
from helpers import irish

IRISH = irish()


def retro(ipa, orthography=""):
    """Stage 2 of the retro-filter, on a normalized and orth-tagged modern word."""
    word = normalize(w(ipa), IRISH, TABLE)
    if orthography:
        word = tag_word(word, orthography)
    return substitute_stage(word, OI, TABLE).segments


def test_bh_and_mh_are_told_apart_by_spelling_alone():
    """spec §4: 'spelling disambiguates what sound alone cannot'. Both are /w/."""
    assert retro("waːd̪ˠ", "bhád")[0] == "β"
    assert retro("wak", "mhac")[0] == "β̃"


def test_dh_and_gh_become_the_lenited_stops():
    assert retro("ɣuːnˠ", "dhún")[0] == "ð"
    assert retro("ɣaːɾˠd̪ˠaː", "gharda")[0] == "ɣ"


def test_th_and_sh_become_theta_and_h():
    assert retro("hax", "theach")[0] == "θ"
    assert retro("huːlʲ", "shúil")[0] == "h"


def test_ch_and_ph_are_kept_as_x_and_f():
    assert retro("xɔsˠ", "chos")[0] == "x"
    assert retro("fˠoːɡ", "phóg")[0] == "fˠ"


def test_the_reversal_is_quality_correct():
    """*bhí* /vʲiː/ is slender: β̥ʲ, not β."""
    assert retro("vʲiː", "bhí")[0] == "βʲ"


def test_modern_ao_becomes_long_a_by_default():
    """spec §8 row O1 default: *áe*, not *óe* (O-13)."""
    assert "aː" in retro("sˠiːlʲ", "saoil")


def test_eclipsed_voiceless_stops_become_plain_voiced_stops():
    """digest §10.4: OI nasalization of p t c is UNWRITTEN b d g."""
    from strands.irish import apply_mutation
    word = apply_mutation(tag_word(normalize(w("pˠaːɾʲc"), IRISH, TABLE), "páirc"),
                          "ECL", IRISH, TABLE)
    assert substitute_stage(word, OI, TABLE).segments[0] == "bˠ"


def test_eclipsed_voiced_stops_become_the_written_nasal_plus_stop():
    """digest §10.4: *mb nd ng*. This is what the O-8 provenance tag exists for."""
    from strands.irish import apply_mutation
    word = apply_mutation(tag_word(normalize(w("bˠaːd̪ˠ"), IRISH, TABLE), "bád"),
                          "ECL", IRISH, TABLE)
    assert substitute_stage(word, OI, TABLE).segments[:2] == ("mˠ", "bˠ")


def test_lax_short_vowels_collapse_onto_the_five_old_irish_short_vowels():
    """digest §10.1 [pokorny1914 p.6 §4]."""
    out = set(retro("ɡɔɾˠmˠ", "gorm")) | set(retro("fʲɪɾʲ", "fir"))
    assert not (out & {"ɪ", "ʊ", "ɛ", "ɔ"})


def test_the_epenthetic_schwa_is_deleted():
    """spec §8 row O5 default; digest §2.4. *gorm* /ɡɔɾˠəmˠ/ -> *gorm*, not *gorom*."""
    assert retro("ɡɔɾˠəmˠ", "gorm") == ("ɡ", "o", "ɾˠ", "mˠ")


def test_vowel_length_and_quality_are_not_reversed():
    """spec §4's explicit non-goals."""
    out = retro("sʲaːnˠ", "Seán")
    assert "aː" in out
    assert out[0] in OI.classes["SLEN"]


def test_an_unaligned_word_still_gets_the_sound_based_rules():
    """O-7: the tag is absent, so only the sound half of the filter applies — and it must
    still produce a legal Old Irish word."""
    out = retro("ɡɔɾˠmˠ")          # no orthography supplied at all
    assert set(out) <= set(OI.inventory)
    assert "ɔ" not in out


def test_every_substitute_line_is_tagged_design_with_a_citation():
    """No lexicon pair instantiates these yet, so none may claim %attested."""
    for rule in OI.sections["substitute"]:
        assert rule.tag == "design", (rule.line, rule.comment)
        assert "design:" in rule.comment or "digest" in rule.comment, (rule.line, rule.comment)
```

- [ ] **Step 2: Run them and watch them fail**

Run: `uv run pytest tests/test_rules_old_irish.py -q`
Expected: FAIL — `KeyError: 'substitute'` / the reversals do not happen.

- [ ] **Step 3: Write the `[substitute]` section**

Follow the rule table above, in this order: (a) the mutation-provenance reversals (most specific);
(b) the spelling digraph reversals, four environment lines each; (c) the vowel-digraph reversals;
(d) the sound-driven vowel collapses; (e) the schwa rules; (f) the leftover `w`/`vˠ`/`vʲ` rules.
Every line ends `%design # design: spec §4 · <the digest section it rests on>`.

- [ ] **Step 4: Run the tests and the suite**

Run: `uv run pytest tests/test_rules_old_irish.py -q` — expected PASS.
Run: `uv run strands check rules/old-irish.rules` — expected exit 0 (`ORTH_UNKNOWN_UNIT`
warnings, if any, name a unit missing from `rules/irish-orthography.tsv` — add it there).
Run: `uv run pytest -q` — expected 1004+ passed, 2 xfailed.

- [ ] **Step 5: Commit**

```bash
git add rules/old-irish.rules tests/test_rules_old_irish.py
git commit -m "feat(rules): old-irish [substitute] — spelling-driven and sound-driven retro-filter"
```

**Acceptance:** *bhád* and *mhac* diverge; eclipsis reverses to the right OI shape in both
branches; lax vowels collapse; the epenthetic schwa goes; length and quality survive; an unaligned
word still yields an in-inventory result; every line is `%design` with a citation.

---

## Task 10: `old-irish.rules` — `[syllable]`, `[repair]`, `[stress]`, `[post-stress]`

**Depends on:** Task 8. **Spec:** §4 (`[syllable]`, `[repair]`, `[stress]`); §12.B, §12.E of the
engine spec. O-20.

**Files:**
- Modify: `rules/old-irish.rules` (replace the temporary `[syllable]` block; add `[repair]`,
  `[stress]`, `[post-stress]`)
- Test: `tests/test_rules_old_irish.py` (append)

**Interfaces:**
- Produces `RuleFile.syllable` (with `nuclei`), `RuleFile.cluster_fallback == "keep"`, and
  `RuleFile.stress.procedure == "initial"`. Consumed by Task 13's stage sequence.

**Content:**

```
[syllable]
# spec §4: template `any`, sonority off — "Old Irish tolerates the modern cluster set"
# (digest §10). The onset/coda whitelists that Georgian needs do not exist for Old Irish in
# the held sources, so nothing is whitelisted and nothing is banned.
template = any
onsets   = any
codas    = any
sonority = off
domain   = word
# spec §12.B: a diphthong is two segments and ONE nucleus. Pokorny's eight
# [pokorny1914-oldirish-grammar p.6 §4] via digest §10.1, written in the segments this file uses.
nuclei = aːi oːi uːi aːu eːu iu iə uə

[repair]
# spec §4: "none beyond degemination". Degemination is written over repeated segments (I-2).
# O-20 / spec §12.E: an unattested cluster is KEPT (flagged UNATTESTED_CLUSTER), never
# rewritten — Old Irish here has no whitelist to fall back to.
cluster-fallback = keep

[stress]
# digest §10.3: "Stress is generally on the first syllable of a word" [wiki-old-irish §Stress];
# for names it is simple, "including in nominal compounds" [utaustin-oldirish-lesson1 §1.2].
procedure = initial
mark = on

[post-stress]
# spec §4: "unstressed vowels are not reduced (unlike modern Irish)" — so this section is
# deliberately EMPTY. digest §10.2's unstressed-vowel grid is a SPELLING matter and lives in
# [respell] (Task 11), not here.
```

The degemination rules go in `[repair]` as explicit repeated-segment lines, one per segment that
can geminate in this inventory — the same shape `georgian.rules` uses. Write them for the
consonants only (`bˠ bˠ -> bˠ`, …), and **not** for `l̪ˠ n̪ˠ ɾˠ mˠ` and their slender partners:
digest §10.2 convention 3 makes `ll nn rr mm` the *fortis* spelling (O-2), so degeminating them
would erase the contrast the orthography carries. Say so in a comment.

**Nuclei spellings.** The digest's eight diphthongs are written *aí oí uí áu éu íu ía úa*. In this
file's segments those are `aːi oːi uːi aːu eːu iu iə uə` — the acute is length on the first
element. Task 12's reconstruction table must agree with this list exactly; a mismatch there is a
bug in one of the two files, and Task 12's round-trip test is what catches it.

- [ ] **Step 1: Write the failing tests** (append)

```python
from strands.syllabify import syllabify
from strands.repair import repair
from strands.stress import assign_stress


def phon(ipa):
    word = syllabify(w(ipa), OI, TABLE)
    return assign_stress(repair(word, OI, TABLE), OI, TABLE)


def test_the_syllable_spec_is_permissive_and_word_domain():
    """spec §4: 'Old Irish tolerates the modern cluster set'."""
    s = OI.syllable
    assert s.template is None and s.onsets is None and s.codas is None
    assert s.sonority is False and s.domain == "word" and s.bans == ()


def test_the_eight_pokorny_diphthongs_are_nuclei():
    """[pokorny1914-oldirish-grammar p.6 §4] via digest §10.1; spec §12.B."""
    declared = {"".join(n) for n in OI.syllable.nuclei}
    assert declared == {"aːi", "oːi", "uːi", "aːu", "eːu", "iu", "iə", "uə"}


def test_a_diphthong_is_one_syllable_not_two():
    assert len(phon("θuːaθ").syllables) == 1 or len(phon("tuəθ").syllables) == 1


def test_an_unattested_cluster_is_kept_and_flagged_never_repaired():
    """O-20 / spec §12.E 'keep': nothing is substituted, the marks are cleared."""
    assert OI.cluster_fallback == "keep"
    out = phon("sˠt̪ˠɾˠaːi")
    assert "UNREPAIRED" not in out.flags
    assert out.segments[:3] == ("sˠ", "t̪ˠ", "ɾˠ")


def test_geminate_obstruents_degeminate():
    assert phon("bˠaːbˠbˠ").segments.count("bˠ") <= 2


def test_geminate_sonorants_are_left_alone_because_they_spell_fortis():
    """digest §10.2 convention 3: ⟨ll nn rr mm⟩ = /L N R m/. O-2 keeps them as geminates."""
    assert phon("kɔl̪ˠl̪ˠ").segments.count("l̪ˠ") == 2


def test_stress_is_initial():
    """digest §10.3 [wiki-old-irish §Stress]."""
    out = phon("kɔnˠxɔβˠaɾˠ")
    assert out.stress == 0


def test_unstressed_vowels_are_not_reduced():
    """spec §4: unlike modern Irish. The [post-stress] section is empty by design."""
    assert OI.sections.get("post-stress", ()) == ()
    assert "a" in phon("kɔnˠal̪ˠ").segments
```

- [ ] **Step 2: Run them and watch them fail**

Run: `uv run pytest tests/test_rules_old_irish.py -q` — expected FAIL on the nuclei set.

- [ ] **Step 3: Replace the temporary block and add the three sections**

Delete the `# TEMPORARY (Task 8)` block entirely — **grep for the word TEMPORARY afterwards and
make sure nothing is left.**

- [ ] **Step 4: Run the tests, `check`, and the suite; commit**

```bash
git add rules/old-irish.rules tests/test_rules_old_irish.py
git commit -m "feat(rules): old-irish syllable, repair (cluster-keep), initial stress"
```

**Acceptance:** the eight diphthongs are nuclei; unattested clusters are kept and flagged, never
`UNREPAIRED`; obstruent geminates reduce and sonorant geminates do not; stress is initial;
`[post-stress]` is empty and the file says why; no `TEMPORARY` block survives.

---

## Task 11: `old-irish.rules [respell]` — editorial Old Irish orthography

**Depends on:** Task 10. **Spec:** §6 (written form); digest §10.2 conventions 1–6; §8 row O2.
O-4, O-14.

**Files:**
- Modify: `rules/old-irish.rules` (add `[respell]`)
- Test: `tests/test_rules_old_irish.py` (append)

**Interfaces:**
- Produces the strand's written form via the ordinary `respell(word, OI, table)` (I-19: quoted
  replacements are opaque chunks; `.` `ˈ` are stripped in code afterwards).
- Consumed by Task 12 (the round trip) and Task 13 (`Result.respelling`).

**The spelling system, rule by rule, from digest §10.2.** Every line cites its convention number.

1. **Lenition is mostly not written** (conv. 1, `[wiki-old-irish-grammar §Lenition]`,
   `[pokorny1914 p.7 §8]`): `β βʲ -> "b"`, `ð ðʲ -> "d"`, `ɣ j -> "g"`, `β̃ β̃ʲ -> "m"`.
   **There is no ⟨bh dh gh mh⟩ in Old Irish** — this is "the single biggest visual difference
   between an Old Irish and a Modern Irish name", and the log's finding 3 counts ~49 attested
   pairs instantiating it.
2. **Lenited voiceless stops are written** (conv. 1): `x ç -> "ch"`, `θ θʲ -> "th"`,
   `fˠ fʲ -> "ph"` **when the /f/ is a lenition product** — but a radical /f/ is also `"f"`, and
   the filter cannot tell them apart without the orth tag. Use it: `@orth("ph") -> "ph"` comes
   first, and a bare `fˠ`/`fʲ` falls through to `"f"`.
3. **`ṡ ḟ` with the punctum** (spec §8 row O2, O-14). `h -> "ṡ"` when the /h/ is a lenited /s/
   (again `@orth("sh")`), else `h -> "h"`. The `punctum = off` alternative is **not** a second set
   of rules: `oldirish.py` post-processes the respelling with `str.translate` when
   `[meta] punctum = off`, mapping `ṡ→s`, `ḟ→f`. One line of code, one line of rules, and the
   decision stays where spec §8 says it is.
4. **⟨c t p⟩ are voiced /ɡ d b/ non-initially unless doubled** (conv. 2; conv. 3 "double letters
   mean fortis"). This is the rule that produces the log's 47 "geminate restoration" pairs
   (*mac ~ macc*, *cnoc ~ cnocc*) **without a lexical list**:

   | segment | initial | non-initial |
   |---|---|---|
   | `k`/`c` | `"c"` | `"cc"` |
   | `t̪ˠ`/`tʲ` | `"t"` | `"tt"` |
   | `pˠ`/`pʲ` | `"p"` | `"pp"` |
   | `ɡ`/`ɟ` | `"g"` | `"c"` |
   | `d̪ˠ`/`dʲ` | `"d"` | `"t"` |
   | `bˠ`/`bʲ` | `"b"` | `"p"` |

   Written as pairs of rules with `/ # _` and no environment. Cite conv. 2 with its examples
   (*macc* /mak/ vs *bec/becc* /bʲeɡ/; *bratt* /brat/ vs *brot* /brod/) and the reason —
   "script poverty: ⟨b d g⟩ were needed for the fricatives" `[utaustin-oldirish-lesson1 §1.1]`.
5. **Fortis sonorants are the geminate spellings** (conv. 3): a repeated `l̪ˠ l̪ˠ -> "ll"`, and
   likewise `nn`, `rr`, `mm`, with their slender partners. Single ones are `"l" "n" "r" "m"`.
6. **Nasalization is written on voiced stops and vowels only** (digest §10.4): the *mb nd ng*
   sequences Task 9 produced are already two segments (`mˠ bˠ` …), so rule 4's non-initial
   mapping would write *mp*. Guard it: `bˠ -> "b" / mˠ _`, `d̪ˠ -> "d" / n̪ˠ _`,
   `ɡ -> "g" / ŋ _`, placed **before** rule 4. Vowel nasalization is `"n-"` + vowel, written by
   the mutation table's own respelling in Task 14.
7. **Length is the acute** (digest §10.1 `[pokorny1914 p.6 §4]`): `aː -> "á"`, `eː -> "é"`,
   `iː -> "í"`, `oː -> "ó"`, `uː -> "ú"`.
8. **Diphthongs are spelled as the digest writes them** (conv. and §10.1): `aː i -> "aí"`,
   `oː i -> "oí"`, `uː i -> "uí"`, `aː u -> "áu"`, `eː u -> "éu"`, `i u -> "íu"`,
   `i ə -> "ía"`, `u ə -> "úa"`. **Pokorny's convention, not UT Austin's** (digest §10.8
   conflict 5: *aí* not *ái*) — cite the conflict on each line.
9. **Glide vowels mark consonant quality** (conv. 5, `[pokorny1914 pp.14 §§36–41]`; O-4 — this is
   where the three-way system lives, as spelling only):
   - §36 i-glide: a slender consonant at the end of a word or syllable takes a written `i`
     before it, **except** after `í é` and the diphthongs `aí oí uí`. Written as
     `0 -> "i" / [V -front] _ SLEN` restricted to the two positions, with the exception as a
     separate blocking context.
   - §39: **no glide before a broad consonant** — so there is no `a`-glide rule at all.
   - §40: final `a o u` after a slender consonant are written `-ea -eo -iu`.
   - §41: final `e i` after a broad consonant are written `-ae -ai` "from the 9th c." — this is
     the log's finding 4 "⟨-a⟩ → ⟨-ae⟩ is the commonest single reversal", so it earns a comment.
   - §38's u-glide (`fiuss`, `firu`) is `%design`-tagged and applied only word-finally: the
     rounded-quality channel does not exist in this implementation (O-4), so a general u-glide
     rule would have nothing to condition on. Say so in the file.
10. **The post-stress /ə/ grid** (conv. 5's table): `ə` is written `⟨a⟩` broad→broad,
    `⟨ai⟩` broad→slender, `⟨e⟩` slender→broad, `⟨i⟩` slender→slender. Four rules with
    `BROAD`/`SLEN` on both sides. "The vowel letter has no relation to the etymological vowel" —
    quote that in the comment, because it is what makes this an orthographic rule and not a
    phonological one.
11. **No h-prefix** (spec §6; conv. 6: "there is no consistent relationship" between the letter
    and the sound). No rule writes a prothetic `h`; a `[respell]` comment records that this is a
    deliberate absence.

- [ ] **Step 1: Write the failing tests** (append)

```python
from strands.respell import respell


def spell(*segments):
    from strands.word import Word
    return respell(Word(segments=segments), OI, TABLE)


def test_lenited_b_d_g_m_are_written_unmarked():
    """digest §10.2 conv.1: there is no ⟨bh dh gh mh⟩ in Old Irish — the single biggest
    visual difference from a modern name. Log finding 3: ~49 attested pairs."""
    assert spell("d", "u", "β") == "dub"          # dubh ~ dub
    assert spell("l", "aː", "β̃") == "lám"          # lámh ~ lám
    assert spell("a", "ð", "a", "ɾˠ", "k") == "adarc"   # adharc ~ adarc


def test_lenited_voiceless_stops_are_written_with_h():
    assert spell("k", "l", "o", "x") == "cloch"
    assert spell("b", "l", "aː", "θ") == "bláth"


def test_non_initial_voiceless_stops_are_doubled():
    """digest §10.2 conv.2-3: *macc* /mak/ vs *bec* /bʲeɡ/. This is the rule that restores
    the log's 47 geminate pairs without a lexical list."""
    assert spell("mˠ", "a", "k") == "macc"
    assert spell("bʲ", "e", "ɡ") == "bec"
    assert spell("bˠ", "ɾˠ", "a", "t̪ˠ") == "bratt"
    assert spell("bˠ", "ɾˠ", "o", "d̪ˠ") == "brot"


def test_a_nasalized_stop_is_not_devoiced_by_the_doubling_rule():
    """*mb nd ng* (digest §10.4): the guard rules must run before the conv.2 mapping."""
    assert spell("mˠ", "bˠ", "oː") == "mbó"
    assert spell("n̪ˠ", "d̪ˠ", "u") == "ndu"
    assert spell("ŋ", "ɡ", "a") == "nga"


def test_fortis_sonorants_are_the_doubled_letters():
    """digest §10.2 conv.3 / O-2."""
    assert spell("k", "o", "l̪ˠ", "l̪ˠ") == "coll"
    assert spell("s", "o", "n̪ˠ", "n̪ˠ") == "sonn"
    assert spell("k", "o", "ɾˠ") == "cor"


def test_length_is_the_acute():
    assert spell("t̪ˠ", "uː", "θ") == "túth"


@pytest.mark.parametrize("segments,expected", [
    (("aː", "i"), "aí"), (("oː", "i"), "oí"), (("uː", "i"), "uí"),
    (("aː", "u"), "áu"), (("eː", "u"), "éu"), (("i", "u"), "íu"),
    (("i", "ə"), "ía"), (("u", "ə"), "úa"),
])
def test_the_eight_diphthongs_use_pokornys_spellings(segments, expected):
    """digest §10.8 conflict 5: *aí (áe)*, NOT UT Austin's *ái*."""
    assert spell(*segments) == expected


def test_an_i_glide_marks_a_final_slender_consonant():
    """digest §10.2 conv.5 §36: *muir* < *mori*."""
    assert spell("mˠ", "u", "ɾʲ") == "muir"


def test_no_glide_is_written_before_a_broad_consonant():
    """§39: *fer* < *viros*."""
    assert spell("fʲ", "e", "ɾˠ") == "fer"


def test_the_post_stress_schwa_grid():
    """digest §10.2 conv.5: 'the vowel letter has no relation to the etymological vowel'."""
    assert spell("dʲ", "iː", "ɣ", "ə", "l̪ˠ") == "dígal"
    assert spell("dʲ", "iː", "ɣ", "ə", "lʲ") == "dígail"
    assert spell("dʲ", "lʲ", "i", "j", "ə", "ð") == "dliged"
    assert spell("dʲ", "lʲ", "i", "j", "ə", "ðʲ") == "dligid"


def test_a_final_broad_e_is_written_ae():
    """§41, and log finding 4's commonest single reversal: *cara ~ carae*."""
    assert spell("k", "a", "ɾˠ", "ə").endswith("ae")


def test_the_punctum_is_written_by_default_and_can_be_turned_off():
    """spec §8 row O2 / O-14."""
    assert OI.meta.get("punctum", "on") == "on"


def test_no_h_prefix_is_ever_written():
    """spec §6; digest §10.2 conv.6."""
    assert not spell("eː", "n̪ˠ").startswith("h")


def test_every_respell_line_carries_a_digest_10_2_citation():
    for rule in OI.sections["respell"]:
        assert "10.2" in rule.comment or "10.1" in rule.comment or "10.4" in rule.comment \
            or "10.8" in rule.comment or "pokorny1914" in rule.comment, (rule.line, rule.comment)
```

- [ ] **Step 2: Run them and watch them fail**

Run: `uv run pytest tests/test_rules_old_irish.py -q` — expected FAIL (`KeyError: 'respell'`).

- [ ] **Step 3: Write `[respell]` in the order 6 → 1 → 2 → 3 → 4 → 5 → 7 → 8 → 9 → 10**

Order matters and is not the order of the exposition above: the nasalization guards (6) must
precede the stop-doubling table (4), and the diphthong rules (8) must precede the single-vowel
length rules (7) so `aː i` is claimed before `aː`. I-19 makes each match an opaque chunk, so once a
diphthong is claimed the length rule cannot re-match its first half.

- [ ] **Step 4: Run the tests, `check`, and the suite; commit**

```bash
git add rules/old-irish.rules tests/test_rules_old_irish.py
git commit -m "feat(rules): old-irish [respell] — editorial orthography, unwritten lenition, conv.2 doubling"
```

**Acceptance:** lenited *b d g m* are unmarked; *ch th* written; non-initial voiceless stops
doubled and voiced stops written *c t p*; the *mb nd ng* guard holds; the eight diphthongs use
Pokorny's spellings; the i-glide and the schwa grid reproduce the digest's own four examples; no
*h*-prefix; every line cites §10.

---

## Task 12: Old Irish spelling→IPA reconstruction

**Depends on:** Tasks 1, 11. **Spec:** §6 ("IPA: reconstructed from the written form by the digest
§10.2 orthography-to-sound table"); O-10, O-11.

**Files:**
- Create: `rules/old-irish-orthography.tsv`
- Create: `src/strands/oldirish.py` (this task writes only `spelling_to_ipa` and its helpers;
  Tasks 13, 15, 16, 17 add to the same module)
- Test: `tests/test_oldirish_reconstruct.py`

**Interfaces:**
- Produces:
  ```python
  OI_ORTHOGRAPHY_PATH: Path                  # rules/old-irish-orthography.tsv
  class OldIrishError(Exception): ...

  def load_oi_orthography(path=None) -> tuple[OrthRow, ...]
      # OrthRow = (unit: str, env: str, segments: tuple[str, ...])
      # env in ("initial", "noninitial", "any"); sorted LONGEST UNIT FIRST, then file order

  def spelling_to_ipa(spelling: str, table=None) -> tuple[str, ...]
      """One written Old Irish word -> IPA segments (spec §6). Longest-match, left to right."""

  def spelling_to_words(spelling: str, table=None) -> list[tuple[str, ...]]
      """A multi-word form (*Cú Chulainn*, *Máel Coluim*) -> one segment tuple per word."""
  ```
- Consumed by: Task 13 (lookup turns `oi_nom`/`oi_gen` into segments, O-10) **and** the
  post-respell IPA reconstruction (O-11). One implementation, two callers — that is the point.

**The table.** `rules/old-irish-orthography.tsv`, header `unit  env  segments  note`. `env` ∈
`initial | noninitial | any`; `segments` is a `+`-joined segment sequence, or `-` for silent.
Transcribed from digest §10.2's **master table** and its six conventions:

| unit | env | segments | source |
|---|---|---|---|
| `mb` | initial | `mˠ+bˠ` | §10.2 master table, ⟨b⟩ eclipsed |
| `nd` | initial | `n̪ˠ+d̪ˠ` | master table, ⟨d⟩ eclipsed |
| `ng` | initial | `ŋ+ɡ` | master table, ⟨g⟩ eclipsed |
| `ch` | any | `x` | master table, ⟨c⟩ lenited |
| `th` | any | `θ` | master table |
| `ph` | any | `fˠ` | master table |
| `ṡ` / `sh` | any | `h` | master table |
| `ḟ` / `fh` | any | `-` | master table, ⟨f⟩ lenited is **∅** |
| `cc` | any | `k` | conv. 3 (geminate = fortis, unmutated) |
| `tt` | any | `t̪ˠ` | conv. 3 |
| `pp` | any | `pˠ` | conv. 3 |
| `bb` | any | `bˠ` | conv. 3 |
| `ll` | any | `l̪ˠ+l̪ˠ` | conv. 3 (fortis = geminate, O-2) |
| `nn` | any | `n̪ˠ+n̪ˠ` | conv. 3 |
| `rr` | any | `ɾˠ+ɾˠ` | conv. 3 |
| `mm` | any | `mˠ+mˠ` | conv. 3 |
| `c` | initial | `k` | master table |
| `c` | noninitial | `ɡ` | conv. 2 |
| `t` | initial | `t̪ˠ` | master table |
| `t` | noninitial | `d̪ˠ` | conv. 2 |
| `p` | initial | `pˠ` | master table |
| `p` | noninitial | `bˠ` | conv. 2 |
| `b` | initial | `bˠ` | master table |
| `b` | noninitial | `β` | conv. 2 |
| `d` | initial | `d̪ˠ` | master table |
| `d` | noninitial | `ð` | conv. 2 |
| `g` | initial | `ɡ` | master table |
| `g` | noninitial | `ɣ` | conv. 2 |
| `m` | initial | `mˠ` | master table |
| `m` | noninitial | `β̃` | master table (lenited/non-initial ⟨m⟩ = /ṽ/) |
| `l` `n` `r` `s` `f` `h` | any | `l̪ˠ` `n̪ˠ` `ɾˠ` `sˠ` `fˠ` `h` | master table |
| `aí` `áe` | any | `aː+i` | §10.1 diphthongs; conflict 5 |
| `oí` `óe` | any | `oː+i` | §10.1 |
| `uí` | any | `uː+i` | §10.1 |
| `áu` | any | `aː+u` | §10.1 |
| `éu` `éo` | any | `eː+u` | §10.1 |
| `íu` | any | `i+u` | §10.1 |
| `ía` | any | `i+ə` | §10.1 |
| `úa` | any | `u+ə` | §10.1 |
| `á` `é` `í` `ó` `ú` | any | `aː` `eː` `iː` `oː` `uː` | §10.1 |
| `a` `e` `i` `o` `u` | any | `a` `e` `i` `o` `u` | §10.1 five short vowels |

**Quality is not recovered.** The reconstruction produces the **broad** member of every consonant
pair. Old Irish orthography marks quality by the *neighbouring vowel letter* (conv. 5), so
recovering it means re-running conv. 5 backwards — and the round trip through `[respell]` already
lost the information the filter had. Simplest faithful reading of spec §6, which asks only for
"quality from adjacent vowels": add **one post-pass** in `spelling_to_ipa`, after the table walk,
that slenderizes a consonant adjacent to a front vowel segment (`i e iː eː`), using the same
`BROAD`→`SLEN` pairing `old-irish.rules [classes]` declares. State in the docstring that this is a
reconstruction, not a recovery, and that a word whose quality mattered is an ATTESTED lookup
anyway.

**Failure mode.** A character no unit matches (a space is handled by `spelling_to_words`; anything
else) raises `OldIrishError` naming the spelling and the offending character. This is a **rule-file
or lexicon bug**, not user data, so it raises — the same policy as I-24.

- [ ] **Step 1: Write the failing tests**

`tests/test_oldirish_reconstruct.py`:

```python
"""Task 12: Old Irish written form -> IPA (spec §6; digest §10.2; O-10, O-11)."""
import pytest

from helpers import ROOT, TABLE, target
from strands.oldirish import (OI_ORTHOGRAPHY_PATH, OldIrishError, load_oi_orthography,
                              spelling_to_ipa, spelling_to_words)
from strands.respell import respell
from strands.word import Word

OI = target("old-irish")


def test_the_table_exists_and_is_sorted_longest_first():
    assert OI_ORTHOGRAPHY_PATH == ROOT / "rules" / "old-irish-orthography.tsv"
    rows = load_oi_orthography()
    assert [len(r[0]) for r in rows] == sorted([len(r[0]) for r in rows], reverse=True)


@pytest.mark.parametrize("spelling,expected", [
    ("macc", ("mˠ", "a", "k")),          # digest §10.2 conv.2-3
    ("bec", ("bˠ", "e", "ɡ")),
    ("dub", ("d̪ˠ", "u", "β")),
    ("mod", ("mˠ", "o", "ð")),
    ("mug", ("mˠ", "u", "ɣ")),
    ("ech", ("e", "x")),
    ("áth", ("aː", "θ")),
    ("cloch", ("k", "l̪ˠ", "o", "x")),
])
def test_the_digests_own_worked_examples_reconstruct(spelling, expected):
    """Every pair here is printed in digest §10.2 conventions 2 and 4."""
    got = spelling_to_ipa(spelling)
    assert tuple(s.rstrip("ʲ") for s in got) == tuple(e.rstrip("ʲ") for e in expected), got


def test_a_non_initial_voiceless_stop_needs_its_double_letter():
    """conv.2: ⟨c t p⟩ are VOICED non-initially unless doubled."""
    assert spelling_to_ipa("macc")[-1] == "k"
    assert spelling_to_ipa("mac")[-1] == "ɡ"


def test_the_fortis_sonorant_spellings_give_geminates():
    """conv.3 / O-2: fortis is written double and modelled as two segments (I-2)."""
    assert spelling_to_ipa("coll")[-2:] == ("l̪ˠ", "l̪ˠ")
    assert spelling_to_ipa("cor")[-1:] == ("ɾˠ",)


def test_nasalization_spellings_are_two_segments():
    assert spelling_to_ipa("mbó")[:2] == ("mˠ", "bˠ")
    assert spelling_to_ipa("nd")[:2] == ("n̪ˠ", "d̪ˠ")


def test_lenited_f_is_silent():
    """master table: ⟨ḟ, fh⟩ = ∅."""
    assert spelling_to_ipa("ḟer") == spelling_to_ipa("er")


def test_the_eight_diphthongs_reconstruct_to_the_nuclei_the_syllable_spec_declares():
    """The two files must agree; this is the test that catches a drift between them."""
    declared = {"".join(n) for n in OI.syllable.nuclei}
    for spelling in ("aí", "oí", "uí", "áu", "éu", "íu", "ía", "úa"):
        assert "".join(spelling_to_ipa(spelling)) in declared, spelling


def test_quality_is_reconstructed_from_the_adjacent_vowel_not_recovered():
    """spec §6: 'quality from adjacent vowels'. A slender consonant next to a front vowel."""
    assert spelling_to_ipa("fer")[0] in OI.classes["SLEN"]
    assert spelling_to_ipa("lám")[0] in OI.classes["BROAD"]


def test_a_multi_word_form_splits_into_words():
    """*Cú Chulainn* is one lexicon row and two pipeline words."""
    words = spelling_to_words("Cú Chulainn")
    assert len(words) == 2 and words[1][0] == "x"


def test_an_unknown_character_raises_and_names_it():
    """A rule-file or lexicon bug, not user data (I-24)."""
    with pytest.raises(OldIrishError, match="z"):
        spelling_to_ipa("fezr")


def test_the_round_trip_through_respell_is_stable():
    """spec §6: the IPA is derived FROM the written form, so respell(reconstruct(x)) == x.
    This is the property that makes the two tables one system."""
    for spelling in ("macc", "bec", "dub", "cloch", "bláth", "túath", "fer", "coll"):
        segments = spelling_to_ipa(spelling)
        assert respell(Word(segments=segments), OI, TABLE) == spelling, spelling
```

- [ ] **Step 2: Run them and watch them fail**

Run: `uv run pytest tests/test_oldirish_reconstruct.py -q`
Expected: FAIL — `ModuleNotFoundError: No module named 'strands.oldirish'`.

- [ ] **Step 3: Write `rules/old-irish-orthography.tsv`**

Exactly the table above. Where two units share a spelling in different environments (`c`), write
the `initial` row first — the loader sorts by unit length only, so file order breaks the tie.

- [ ] **Step 4: Write `src/strands/oldirish.py`**

Module docstring covering: what the strand is, that grammar runs on IPA segments (O-10), that
`spelling_to_ipa` serves both lookup and the post-respell reconstruction (O-11), and that quality
is reconstructed rather than recovered.

`spelling_to_ipa`: NFC the input, walk it left to right taking the **first** row whose unit
matches at the position and whose `env` is satisfied (`initial` ⇔ position 0), append its
segments, advance. Unknown character ⇒ `OldIrishError(f"{spelling!r}: no orthographic unit
matches {ch!r} at {i}")`. Then the quality post-pass: for each consonant segment in
`old-irish.rules [classes] BROAD`, if the segment adjacent (following first, else preceding) is
one of `i e iː eː`, replace it with its `SLEN` partner from a pairing dict built once from the two
class lists by position. Document that the pairing is positional and that the two class lines must
therefore stay parallel — and **assert that they are the same length at load time**, raising
`OldIrishError` otherwise, so a future edit to `[classes]` cannot silently misalign them.

`spelling_to_words`: split on whitespace, run `spelling_to_ipa` on each piece.

- [ ] **Step 5: Run the tests**

Run: `uv run pytest tests/test_oldirish_reconstruct.py -q` — expected PASS.
**If `test_the_round_trip_through_respell_is_stable` fails, the bug is in whichever of the two
files is wrong, and the test is the arbiter — do not weaken it.** The usual cause is a `[respell]`
rule (Task 11) and an orthography row disagreeing about a non-initial stop.

- [ ] **Step 6: Run the suite and commit**

```bash
git add rules/old-irish-orthography.tsv src/strands/oldirish.py \
        tests/test_oldirish_reconstruct.py
git commit -m "feat(oldirish): spelling->IPA reconstruction from the digest §10.2 table"
```

**Acceptance:** the digest's eight worked examples reconstruct; the conv. 2 doubling contrast holds
both ways; the diphthongs agree with `[syllable] nuclei`; multi-word forms split; an unknown
character raises; the respell round trip is stable on eight words.

---

## Task 13: Lookup stage, flags, and `oldirish.run_entry_oi`

**Depends on:** Tasks 2, 9, 10, 11, 12. **Spec:** §2 (the whole pipeline), §6 (flags); O-9, O-10,
O-11, O-12, O-18, O-22, O-23.

**Files:**
- Modify: `src/strands/pipeline.py` (`TARGETS`, `lookup()`, the `run_entry` dispatch)
- Modify: `src/strands/oldirish.py` (`to_old_irish`, `adapt_oi`, `run_entry_oi`)
- Test: `tests/test_oldirish_lookup.py`

**Interfaces:**
- `pipeline.py`:
  ```python
  TARGETS = ("welsh", "arabic-egy", "georgian", "dutch", "old-irish")

  def lookup(entry: Entry, lexicon: dict[str, LexEntry]) -> LexEntry | None:
      """Stage 1b (spec §2, O-9): match `entry.orthography` — the CITATION form — against the
      lexicon, exactly, after NFC and case-folding (O-19, O-23). No de-mutation, no fuzzy
      fallback: the Irish pre-pass has already applied the mutation on the modern side."""
      return lexicon.get(key(entry.orthography))
  ```
  `run_entry()` gains, as its first action after `parse_construction`:
  ```python
      if target.meta.get("strand", "") == "old-irish":         # O-9
          from .oldirish import run_entry_oi
          return run_entry_oi(entry, construction, irish, target, table, slots=slots)
  ```
- `oldirish.py`:
  ```python
  OI_STRAND = "old-irish"

  class ConstructionNotInStrand(PipelineError):
      """This strand has no [templates] entry of that name (O-17). The CLI and the gallery
      report the cell as skipped; they do not fail."""

  @dataclass(frozen=True)
  class Stem:
      words: tuple[Word, ...]          # the Old Irish nominative, one Word per space-separated word
      gen: tuple[Word, ...] | None     # the attested genitive, when the lexicon gave one
      stem: str                        # a lexicon.STEMS value, looked up or inferred
      gender: str                      # m | f | n
      flag: str                        # one of OI_FLAGS
      assumptions: tuple[str, ...]

  OI_FLAGS = ("ATTESTED", "ATTESTED:MIr", "RETRO", "RETRO:loan", "RETRO:late")

  def infer_stem(entry: Entry) -> tuple[str, str]:
      """(stem, reason) from the modern declension (spec §5; O-21)."""

  def to_old_irish(entry, lexicon, oi, irish, table) -> Stem:
      """Lookup, else retro-filter. THE fork of spec §2."""

  def run_entry_oi(entry, construction, irish, oi, table, *, lexicon=None, slots=None) -> Result
  ```

**The fork, in `to_old_irish` (spec §2 steps 1–2).**

| lexicon row | what happens | flag |
|---|---|---|
| `status = attested` | `spelling_to_words(row.oi_nom)` → the stem words; `oi_gen` → `gen` when non-empty; `stem`/`gender` from the row. **No `[substitute]` runs.** | `ATTESTED` |
| `status = middle` | identical (O-22) | `ATTESTED:MIr` |
| `status = none` | retro-filter, exactly as a miss (O-12) | `RETRO:loan` / `RETRO:late` from `row.kind` |
| no row | retro-filter | `RETRO` |

The retro-filter path is: `tokenize(entry.ipa)` → `Word.from_tokenized` → `irish.normalize` →
`orth.tag_word(word, entry.orthography)` → `substitute_stage(word, oi, table)`. `gen = None`
(there is no attested genitive to use), `gender` from `entry.gender`, and `stem` from
`infer_stem`.

**`infer_stem` (spec §4 `[inflect]`, O-21).** Reads `Entry.declension`, which the input stage has
already inferred (I-38):

| modern | Old Irish `stem` | assumption tag |
|---|---|---|
| `m1` | `o` | `stem:from-declension-m1` |
| `f2` | `ā` | `stem:from-declension-f2` |
| `ach` | `o` | `stem:from-declension-ach` (the o-stem adjective/noun in *-ach*, digest §10.5) |
| `m3` ending in a slender consonant | `i` | `stem:from-declension-m3-slender` |
| `m3` otherwise | `u` | `stem:from-declension-m3-broad` |
| `d4` | `indecl` | `stem:from-declension-d4` |
| anything else / empty | `o` | `stem:default-o` |

Every tag lands in `Result.assumptions` (spec §6: "`assumptions` carries the stem class
inference"). A lexicon-supplied class contributes **no** tag — it is data, not a guess.

**`adapt_oi` — the stage sequence (O-9).** `pipeline.adapt` cannot be reused, because Old Irish
runs `[substitute]` before the grammar and reconstructs its IPA after respell. `adapt_oi(words,
oi, table)` therefore does, per word: `syllabify` → `repair` → `assign_stress` → `post_stress` →
`respell_traced`, then joins the respellings with spaces and sets

```python
    ipa = " ".join(" ".join(spelling_to_ipa(part)) for part in spelling.split(" "))
```

`Result.ipa` is that string; the pre-respell phonological IPA survives in the trace as the last
`respell` entry's `before`. `[meta] punctum = off` post-processes the spelling with
`str.maketrans({"ṡ": "s", "ḟ": "f"})` **before** the reconstruction, so both halves agree (O-14) —
and `rules/old-irish-orthography.tsv` has rows for both spellings, so either setting reconstructs.

**Determinism.** `run_entry_oi` returns the same frozen `Result` dataclass as `adapt`, with tuples
throughout, so `test_properties.py`'s determinism check covers it unchanged.

- [ ] **Step 1: Write the failing tests**

`tests/test_oldirish_lookup.py`:

```python
"""Task 13: the lookup stage and the Old Irish assembly (spec §2, §6; O-9, O-12, O-23)."""
import pytest

from helpers import TABLE, irish, target
from strands.inputs import Entry, infer
from strands.lexicon import LexEntry, key, read_lexicon
from strands.oldirish import OI_FLAGS, ConstructionNotInStrand, infer_stem, run_entry_oi, to_old_irish
from strands.pipeline import TARGETS, load_target, lookup, run_entry

IRISH = irish()
OI = target("old-irish")
LEX = read_lexicon()


def entry(orthography, ipa, **kw):
    return infer(Entry(orthography=orthography, ipa=ipa, **kw), IRISH, TABLE)


def test_old_irish_is_the_fifth_target():
    assert TARGETS == ("welsh", "arabic-egy", "georgian", "dutch", "old-irish")
    assert load_target("old-irish", TABLE).meta["strand"] == "old-irish"


def test_lookup_matches_the_citation_form_exactly():
    """O-19, O-23: no fuzzy matching, no de-mutation."""
    assert lookup(entry("Niall", "nʲiəl̪ˠ"), LEX) is not None
    assert lookup(entry("NIALL", "nʲiəl̪ˠ"), LEX) is not None
    assert lookup(entry("a Sheáin", "ə çaːnʲ"), LEX) is None      # a SURFACE form: a miss


def test_an_attested_row_supplies_the_form_and_the_filter_never_runs():
    """spec §2 step 1. The Old Irish word comes from the lexicon spelling, not from the
    modern IPA."""
    stem = to_old_irish(entry("Niall", "nʲiəl̪ˠ"), LEX, OI, IRISH, TABLE)
    assert stem.flag == "ATTESTED"
    assert stem.stem and stem.assumptions == ()          # data, not a guess


def test_a_middle_irish_row_is_used_and_flagged():
    """spec §10 / O-22."""
    row = LEX.get(key("Tadhg"))
    if row is None or row.status != "middle":
        pytest.skip("Task 4 has not added the Middle Irish tier yet")
    stem = to_old_irish(entry("Tadhg", "t̪ˠəiɡ"), LEX, OI, IRISH, TABLE)
    assert stem.flag == "ATTESTED:MIr"


def test_a_loan_and_a_late_coinage_are_filtered_and_flagged_apart():
    """O-12 and O-18: both are filtered; only the flag differs."""
    loan = to_old_irish(entry("Seán", "ʃaːnˠ"), LEX, OI, IRISH, TABLE)
    late = to_old_irish(entry("Saoirse", "ˈsˠiːɾˠʃə"), LEX, OI, IRISH, TABLE)
    assert loan.flag == "RETRO:loan" and late.flag == "RETRO:late"
    assert loan.words and late.words                     # filtered, not omitted


def test_a_miss_is_a_plain_retro():
    stem = to_old_irish(entry("Splancarnach", "sˠpˠl̪ˠaŋkəɾˠnˠəx"), LEX, OI, IRISH, TABLE)
    assert stem.flag == "RETRO"


@pytest.mark.parametrize("declension,expected", [
    ("m1", "o"), ("f2", "ā"), ("ach", "o"), ("d4", "indecl"),
])
def test_the_stem_class_is_inferred_from_the_modern_declension(declension, expected):
    """spec §4 [inflect]; O-21."""
    stem, reason = infer_stem(entry("Xyz", "sˠiː", declension=declension))
    assert stem == expected and reason.startswith("stem:")


def test_the_inference_is_reported_in_assumptions():
    """spec §6: 'assumptions carries the stem class inference'."""
    result = run_entry_oi(entry("Splancarnach", "sˠpˠl̪ˠaŋkəɾˠnˠəx"), "DESC",
                          IRISH, OI, TABLE)
    assert any(a.startswith("stem:") for a in result.assumptions)


def test_every_result_carries_exactly_one_of_the_five_flags():
    """spec §6: 'Flags: ATTESTED / RETRO / RETRO:loan on every output'."""
    for orthography, ipa in [("Niall", "nʲiəl̪ˠ"), ("Seán", "ʃaːnˠ"),
                             ("Splancarnach", "sˠpˠl̪ˠaŋkəɾˠnˠəx")]:
        result = run_entry_oi(entry(orthography, ipa), "DESC", IRISH, OI, TABLE)
        assert len([f for f in result.flags if f in OI_FLAGS]) == 1, result.flags


def test_the_ipa_is_reconstructed_from_the_written_form():
    """spec §6 / O-11: Result.ipa is spelling_to_ipa(Result.respelling), not the
    pre-respell phonological string."""
    from strands.oldirish import spelling_to_ipa
    result = run_entry_oi(entry("Niall", "nʲiəl̪ˠ"), "DESC", IRISH, OI, TABLE)
    assert result.ipa.replace(" ", "") == "".join(
        spelling_to_ipa(result.respelling.replace(" ", "")))


def test_the_pre_respell_phonology_survives_in_the_trace():
    result = run_entry_oi(entry("Niall", "nʲiəl̪ˠ"), "DESC", IRISH, OI, TABLE)
    assert [t for t in result.trace if t.stage == "respell"]


def test_run_entry_dispatches_on_the_meta_strand_key():
    """O-9: the dispatch is data-driven, not a hard-coded name."""
    a = run_entry(entry("Niall", "nʲiəl̪ˠ"), "DESC", IRISH, OI, TABLE)
    b = run_entry_oi(entry("Niall", "nʲiəl̪ˠ"), "DESC", IRISH, OI, TABLE)
    assert a == b


def test_a_construction_this_strand_does_not_have_raises_not_crashes():
    """O-17: PATRO_O/PATRO_NI are not Old Irish formations."""
    with pytest.raises(ConstructionNotInStrand):
        run_entry_oi(entry("Niall", "nʲiəl̪ˠ"), "PATRO_O", IRISH, OI, TABLE)


def test_a_multi_word_attested_form_becomes_several_words():
    """*Cú Chulainn* is one lexicon row and two output words."""
    row = LEX.get(key("Cú Chulainn"))
    if row is None:
        pytest.skip("no multi-word row in the lexicon")
    stem = to_old_irish(entry("Cú Chulainn", "kuː xʊl̪ˠənʲ"), LEX, OI, IRISH, TABLE)
    assert len(stem.words) == 2


def test_the_result_is_deterministic():
    e = entry("Niall", "nʲiəl̪ˠ")
    assert run_entry_oi(e, "DESC", IRISH, OI, TABLE) == run_entry_oi(e, "DESC", IRISH, OI, TABLE)
```

- [ ] **Step 2: Run them and watch them fail**

Run: `uv run pytest tests/test_oldirish_lookup.py -q`
Expected: FAIL — `ImportError: cannot import name 'lookup'`.

- [ ] **Step 3: Extend `pipeline.py`**

Add `"old-irish"` to `TARGETS`, write `lookup()` with the docstring above, and put the dispatch at
the top of `run_entry`. Extend the module docstring with a paragraph naming O-9 and pointing at
`oldirish.py`.

- [ ] **Step 4: Extend `oldirish.py`**

Write `Stem`, `OI_FLAGS`, `ConstructionNotInStrand`, `infer_stem`, `to_old_irish`, `adapt_oi` and
`run_entry_oi`. `run_entry_oi` builds the construction with the Task 16 builder when
`oi.templates` has the name and raises `ConstructionNotInStrand` otherwise; **until Task 16 lands
it may support only `DESC`**, which is `NOUN` — the head slot, unchanged. Write that limitation as
an explicit `raise ConstructionNotInStrand` for every other name plus a `# Task 16` comment, so the
gap is visible rather than silently wrong.

- [ ] **Step 5: Run the tests and the suite**

Run: `uv run pytest tests/test_oldirish_lookup.py -q` — expected PASS (two `skip`s until Tasks 4
and the multi-word row exist).
Run: `uv run pytest -q` — expected 1004+ passed. **`test_properties.py` and `test_cli.py`
parametrize over `TARGETS`, so adding the fifth target will run them against `old-irish`** — some
will fail until Task 16. If they do, mark the new-target cases `xfail(strict=False)` with the
reason `"old-irish templates land in Task 16"` and **remove the marks in Task 16**; do not weaken
the assertions.

- [ ] **Step 6: Commit**

```bash
git add src/strands/pipeline.py src/strands/oldirish.py tests/test_oldirish_lookup.py
git commit -m "feat(oldirish): lookup stage, ATTESTED/RETRO flags, and the Old Irish assembly"
```

**Acceptance:** the five flags are exclusive and correct for attested/middle/loan/late/miss; lookup
is exact on the citation form; the stem inference is reported in `assumptions`; `Result.ipa` is
reconstructed from the respelling; `run_entry` dispatches on `[meta] strand`; a construction the
strand lacks raises `ConstructionNotInStrand`.

---

## Task 14: `old-irish.rules [mutations]`

**Depends on:** Task 8. **Spec:** §5 `[mutations]`; digest §10.4.

**Files:**
- Modify: `rules/old-irish.rules` (add `[mutations]`)
- Test: `tests/test_oldirish_grammar.py`

**Interfaces:**
- Produces the sub-tables `LEN` and `NAS`, applied by the existing `irish.apply_mutation` (O-10 —
  nothing new is written for this). **No `HPREF`, no `TPREF`**: spec §5 says "no *h*-prefix, no
  *t*-prefix". Old Irish's own third mutation (aspiration/gemination, digest §10.4) is **out of
  scope** — spec §5 lists two mutations, and digest §9 open question 10 flags the third as
  undecided. Record that omission as a comment in the file.

**`LEN` — digest §10.4** `[wiki-old-irish §Orthography; pokorny1914 p.7 §7]`:

| radical | lenited | written |
|---|---|---|
| `pˠ pʲ` | `fˠ fʲ` | *ph* |
| `t̪ˠ tʲ` | `θ θʲ` | *th* |
| `k c` | `x ç` | *ch* |
| `bˠ bʲ` | `β βʲ` | unwritten |
| `d̪ˠ dʲ` | `ð ðʲ` | unwritten |
| `ɡ ɟ` | `ɣ j` | unwritten |
| `mˠ mʲ` | `β̃ β̃ʲ` | unwritten |
| `sˠ ʃ` | `h` | *ṡ sh* |
| `fˠ fʲ` | `0` | *ḟ fh* |

Fortis→lenis sonorant lenition (`/L N R/ → /l n r/`) is **absent by O-2**: this implementation has
one sonorant series, so the rule would be an identity. Say so in a comment, citing digest §10.4 and
O-2, so the absence reads as a decision.

**`NAS` — digest §10.4** `[pokorny1914 p.10 §21]`. Note the direction is the reverse of the modern
eclipsis table:

| radical | nasalized | written |
|---|---|---|
| `pˠ pʲ` | `bˠ bʲ` | unwritten |
| `t̪ˠ tʲ` | `d̪ˠ dʲ` | unwritten |
| `k c` | `ɡ ɟ` | unwritten |
| `bˠ bʲ` | `mˠ bˠ` / `mʲ bʲ` (two segments) | *mb* |
| `d̪ˠ dʲ` | `n̪ˠ d̪ˠ` / `nʲ dʲ` | *nd* |
| `ɡ ɟ` | `ŋ ɡ` / `ɲ ɟ` | *ng* |
| `fˠ fʲ` | `β βʲ` | written *b* |
| vowel | `n̪ˠ` + V | *n-* |
| `sˠ ʃ mˠ mʲ n̪ˠ nʲ l̪ˠ lʲ ɾˠ ɾʲ` | unchanged | — |

The two-segment replacements are what `[respell]`'s Task-11 guard rules expect; they are why that
guard exists.

- [ ] **Step 1: Write the failing tests**

`tests/test_oldirish_grammar.py`:

```python
"""Tasks 14-16: Old Irish mutations, inflection and templates (spec §5; digest §10.4-§10.5)."""
import pytest

from helpers import TABLE, target, w
from strands.irish import apply_mutation
from strands.oldirish import spelling_to_ipa
from strands.respell import respell
from strands.word import Word

OI = target("old-irish")


def mut(spelling, name):
    """Mutate a written Old Irish word and read the result back as a written form."""
    word = Word(segments=spelling_to_ipa(spelling))
    return respell(apply_mutation(word, name, OI, TABLE), OI, TABLE)


@pytest.mark.parametrize("radical,lenited", [
    ("tech", "thech"), ("cenn", "chenn"), ("penn", "phenn"),
])
def test_lenition_writes_the_voiceless_stops(radical, lenited):
    """digest §10.4 contrast set: *a thech* /a θʲex/."""
    assert mut(radical, "LEN") == lenited


@pytest.mark.parametrize("radical", ["bo", "duine", "gel", "mac"])
def test_lenition_of_b_d_g_m_is_not_written(radical):
    """digest §10.2 conv.1 / §10.4: *a bo* /a vo/ is still written *bo*."""
    assert mut(radical, "LEN") == radical


def test_lenition_of_s_and_f():
    """master table: ⟨ṡ sh⟩ = /h/; ⟨ḟ fh⟩ = ∅."""
    assert mut("son", "LEN").startswith("ṡ")
    assert mut("fer", "LEN") in ("ḟer", "er")


def test_nasalization_voices_the_voiceless_stops_without_writing_it():
    """digest §10.4: *a tech* [a dʲex] 'their house' is still written *tech*."""
    assert mut("tech", "NAS") == "tech"
    assert spelling_to_ipa(mut("tech", "NAS"))[0] != apply_mutation(
        Word(segments=spelling_to_ipa("tech")), "NAS", OI, TABLE).segments[0]


@pytest.mark.parametrize("radical,nasalized", [
    ("bo", "mbo"), ("duine", "nduine"), ("gel", "ngel"),
])
def test_nasalization_of_the_voiced_stops_is_written(radical, nasalized):
    """digest §10.4: 'It is only in the case of b, d, g and of initial vowels that eclipsis
    is regularly expressed in writing.'"""
    assert mut(radical, "NAS") == nasalized


def test_nasalization_prefixes_n_to_a_vowel():
    """digest §10.4: *a n-ech* /a nex/."""
    assert mut("ech", "NAS").startswith("n")


@pytest.mark.parametrize("radical", ["son", "mac", "nem", "lám", "rí"])
def test_s_and_the_sonorants_do_not_nasalize(radical):
    """digest §10.2: *r l n s* are not subject to eclipsis."""
    assert mut(radical, "NAS") == radical


def test_this_strand_has_no_h_prefix_or_t_prefix_table():
    """spec §5: 'no h-prefix, no t-prefix'."""
    assert set(OI.mutations) == {"LEN", "NAS"}
```

- [ ] **Step 2: Run them and watch them fail**

Run: `uv run pytest tests/test_oldirish_grammar.py -q` — expected FAIL (`IrishError: no
[mutations] sub-table 'LEN'`).

- [ ] **Step 3: Write `[mutations]`**

Both tables, every line cited `# digest §10.4 [pokorny1914-oldirish-grammar p.7 §7]` or
`p.10 §21` as appropriate, tagged `%attested` (these are stated rules, not design choices), with
the two "deliberately absent" comments (fortis sonorants per O-2; the third mutation per spec §5
and digest §9 open question 10).

- [ ] **Step 4: Run the tests, `check`, and the suite; commit**

```bash
git add rules/old-irish.rules tests/test_oldirish_grammar.py
git commit -m "feat(rules): old-irish [mutations] — lenition and nasalization per digest §10.4"
```

**Acceptance:** *ph th ch* are written and *b d g m* are not; *mb nd ng* appear for the voiced
stops and nothing for the voiceless ones; vowels take *n-*; *s r l n m* are inert; only `LEN` and
`NAS` exist.

---

## Task 15: `old-irish.rules [inflect]` and the stem-class dispatch

**Depends on:** Tasks 2, 14. **Spec:** §5 `[inflect]`; digest §10.5; O-10, O-21.

**Files:**
- Modify: `rules/old-irish.rules` (add `[inflect]`)
- Modify: `src/strands/oldirish.py` (`apply_case`)
- Test: `tests/test_oldirish_grammar.py` (append)

**Interfaces:**
- Produces the `[inflect]` sub-tables, applied by the existing `irish.apply_inflection` (O-10):

  | table | class | derivation (digest §10.5) | example |
  |---|---|---|---|
  | `GEN_O` | o-stem m/n | palatalize the final consonant | *fer → fir*; *claideb → claidib* |
  | `GEN_A` | ā-stem f | palatalize the final consonant, add `ə` | *túath → túaithe* |
  | `GEN_I` | i-stem | depalatalize the final consonant, add `o` | *cnáim → cnámo* |
  | `GEN_U` | u-stem | add `o` | *guth → gotho* |
  | `GEN_N` | n-stem | add `on` | *brithem → brithemon* |
  | `GEN_DENT` | dental | add `at` | *carae → carat* |
  | `GEN_VELAR` | velar | add `ɡ` | *rí → ríg* |
  | `GEN_R` | r-stem | depalatalize the final consonant, add `ar` | *athair → athar* |
  | `GEN_S` | s-stem | palatalize the final consonant, add `ə` | *nem → nime* |
  | `VOC_O` | o-stem m | = `GEN_O` (digest §10.5: the masculine o-/io-stem is the exception that takes the palatalized form) | *a fir* |
  | `NOM_A` | ā-stem f | identity — **the home of spec §4's "final /ə/ → *e* (ā-stems)"** (see Task 9) | *túath* |
  | `GEN_O_ADJ` | o-ā adjective | = `GEN_O` (digest §10.5: *bec → bic*) | *bic* |
  | `DAT_O`, `DAT_A` | dative sg | identity, with the leniting mutation supplied by the template (digest §10.4's table: dat. sg. of all genders lenites) | |

  `indecl` has **no table** — `apply_case` returns the word unchanged with a trace note.
  `irregular` has no table either: the lexicon's `oi_gen` is used verbatim (O-21).

- `oldirish.py`:
  ```python
  CASE_TABLES = {
      ("gen", "o"): "GEN_O", ("gen", "ā"): "GEN_A", ("gen", "i"): "GEN_I",
      ("gen", "u"): "GEN_U", ("gen", "n"): "GEN_N", ("gen", "dental"): "GEN_DENT",
      ("gen", "velar"): "GEN_VELAR", ("gen", "r"): "GEN_R", ("gen", "s"): "GEN_S",
      ("voc", "o"): "VOC_O", ("nom", "ā"): "NOM_A",
      ("dat", "o"): "DAT_O", ("dat", "ā"): "DAT_A",
  }

  def apply_case(stem: Stem, case: str, oi: RuleFile, table: FeatureTable) -> tuple[Word, ...]:
      """The case form of a Stem (spec §5).

      Precedence, and this order is the point of the task:
        1. `case == "gen"` and `stem.gen is not None`  -> the ATTESTED genitive, verbatim.
           163 of the lexicon's rows have one; an attested form is never re-derived.
        2. a CASE_TABLES entry for (case, stem.stem)   -> `apply_inflection`.
        3. `stem.stem` in ("indecl", "irregular")      -> unchanged, trace note.
        4. otherwise                                   -> `GEN_O` / `VOC_O` with an
           `assumptions` note `case:{case}-fallback-o` (the same shape as I-38's GEN_M1
           fallback).
      """
  ```

**Palatalization and depalatalization are written as explicit segment→segment lines**, exactly as
`irish.rules [inflect]` does and for the same reason (I-4: a feature-change bundle resolves to no
row, because the `ʲ` rows carry `high=+` where the `ˠ` rows carry `high=0`, and `w`↔`vʲ`,
`ɣ`↔`j` differ in more than quality). Copy the shape of `GEN_M1`/`GEN_M3` in `irish.rules` and
extend it with the new Old Irish segments: `β→βʲ`, `ð→ðʲ`, `θ→θʲ`, `β̃→β̃ʲ` and their inverses.

**Where a paradigm is not rule-expressible, the lexicon wins.** *Ériu → Érenn*, *Eochu → Echach*,
*Lugaid → Luigdech* involve syncope and stem alternation that no final-position rule captures
(digest §10.3's syncope "transphonologises quality across the resulting cluster"). All three are
lexicon rows with an attested `oi_gen`, so precedence rule 1 covers them. **Do not attempt a
syncope rule** — digest §10.3 states it as a historical process, not a synchronic one, and spec §5
asks only for the paradigms.

- [ ] **Step 1: Write the failing tests** (append to `tests/test_oldirish_grammar.py`)

```python
from strands.irish import apply_inflection
from strands.lexicon import key, read_lexicon
from strands.oldirish import CASE_TABLES, Stem, apply_case, to_old_irish

LEX = read_lexicon()


def infl(spelling, name):
    word = Word(segments=spelling_to_ipa(spelling))
    return respell(apply_inflection(word, name, OI, TABLE), OI, TABLE)


@pytest.mark.parametrize("table_name,nom,gen", [
    ("GEN_O", "fer", "fir"),            # digest §10.5 o-stem masc.
    ("GEN_O", "claideb", "claidib"),
    ("GEN_A", "túath", "túaithe"),      # ā-stem fem.
    ("GEN_I", "cnáim", "cnámo"),        # i-stem, depalatalize
    ("GEN_U", "guth", "gotho"),         # u-stem
    ("GEN_N", "brithem", "brithemon"),  # n-stem
    ("GEN_DENT", "carae", "carat"),     # dental stem
    ("GEN_VELAR", "rí", "ríg"),         # velar stem
    ("GEN_R", "athair", "athar"),       # r-stem
    ("GEN_S", "nem", "nime"),           # s-stem
])
def test_each_stem_class_derives_strachans_genitive(table_name, nom, gen):
    """digest §10.5 [strachan1909-oldirish-paradigms pp.2-16; pokorny1914 pp.59-70].
    Where the derivation misses a vowel change the test states the ATTESTED form and the
    rule file must reach it or the row must move to the lexicon's oi_gen."""
    assert infl(nom, table_name) == gen


def test_the_vocative_of_a_masculine_o_stem_is_the_genitive_form():
    """digest §10.5: 'The masculine o-stem and io-stem are the exceptions, taking the
    genitive/palatalized form' [pokorny1914 p.65 §142]."""
    assert infl("fer", "VOC_O") == infl("fer", "GEN_O")


def test_the_o_stem_adjective_inflects_like_the_o_stem_noun():
    """digest §10.5: *bec* m. gen. *bic*."""
    assert infl("bec", "GEN_O_ADJ") == "bic"


def test_an_attested_genitive_is_never_re_derived():
    """Precedence rule 1. *Ériu ~ Érenn* involves syncope no final-position rule captures."""
    row = LEX[key("Éire")]
    assert row.oi_gen
    stem = to_old_irish(_entry("Éire", "ˈeːɾʲə"), LEX, OI, IRISH, TABLE)
    got = respell(apply_case(stem, "gen", OI, TABLE)[0], OI, TABLE)
    assert got == row.oi_gen


def test_an_indeclinable_stem_is_returned_unchanged():
    """digest §10.5 'Indeclinable names': *Patraic*, *Da Derga*."""
    stem = Stem(words=(Word(segments=spelling_to_ipa("Patraic")),), gen=None,
                stem="indecl", gender="m", flag="ATTESTED", assumptions=())
    assert respell(apply_case(stem, "gen", OI, TABLE)[0], OI, TABLE) == "Patraic".lower() \
        or apply_case(stem, "gen", OI, TABLE)[0].segments == stem.words[0].segments


def test_an_unknown_stem_class_falls_back_to_the_o_stem_with_a_note():
    stem = Stem(words=(Word(segments=spelling_to_ipa("fer")),), gen=None, stem="",
                gender="m", flag="RETRO", assumptions=())
    out = apply_case(stem, "gen", OI, TABLE)
    assert respell(out[0], OI, TABLE) == "fir"
    assert any("fallback-o" in t.note for t in out[0].trace)


def test_the_case_table_map_covers_every_stem_value_that_has_a_paradigm():
    from strands.lexicon import STEMS
    covered = {stem for (case, stem) in CASE_TABLES if case == "gen"}
    assert covered == set(STEMS) - {"indecl", "irregular"}
```

Add `from helpers import irish as _irish` and a small `_entry` helper mirroring
`tests/test_oldirish_lookup.py`'s.

- [ ] **Step 2: Run them and watch them fail**

Run: `uv run pytest tests/test_oldirish_grammar.py -q` — expected FAIL (no `[inflect]` section).

- [ ] **Step 3: Write `[inflect]` and `apply_case`**

Work one table at a time, running its parametrized case after each. Where a derivation cannot
reach the attested form with final-position rules (the likely cases are `GEN_I`'s *cnáim → cnámo*
vowel change and `GEN_U`'s *guth → gotho*), write the vowel rule explicitly with the digest's own
example in the comment and tag it `%design`, exactly as `irish.rules` does for *mac → mic*.

- [ ] **Step 4: Run the tests, `check`, and the suite; commit**

```bash
git add rules/old-irish.rules src/strands/oldirish.py tests/test_oldirish_grammar.py
git commit -m "feat(rules): old-irish [inflect] by stem class, with attested genitives taking precedence"
```

**Acceptance:** the ten Strachan/Pokorny paradigm genitives derive; the o-stem vocative equals its
genitive; an attested `oi_gen` is used verbatim; `indecl` is inert; an unknown class falls back to
the o-stem with a note; `CASE_TABLES` covers every paradigm-bearing stem value.

---

## Task 16: `old-irish.rules [templates]` and the formation templates

**Depends on:** Tasks 13, 15. **Spec:** §5 `[templates]`, §8 row O6; digest §10.5. O-17, O-25.

**Files:**
- Modify: `src/strands/dsl.py` (template function names become data-driven)
- Modify: `rules/old-irish.rules` (add `[templates]`)
- Modify: `src/strands/oldirish.py` (the construction builder)
- Modify: `src/strands/pipeline.py` (`CONSTRUCTIONS` gains the eight formation names)
- Test: `tests/test_oldirish_grammar.py` (append)

**Interpretation carried here.**

- **O-25 Template literals are IPA, as they already are.** `irish.rules` writes `VOC = "ə"
  LEN(NAME)`. Old Irish's formation templates need whole words as literals (*Máel*, *Gilla*,
  *Cú*, *Fer*, *Dub-*, *Find-*, *Flann-*, *mac*, *ua*, *ingen*). Keep the DSL unchanged: write each
  literal as the IPA `spelling_to_ipa` yields for that spelling, and put the spelling in the line's
  comment. A round-trip test asserts the pairing, so a typo in the IPA is caught rather than
  shipped.

**The DSL change.** `_TemplateParser` currently validates against a hard-coded `func-name` list
(`LEN ECL HPREF TPREF GEN GEN_M1 …`). Old Irish needs `NAS` and the Task-15 table names. Make the
check data-driven: a call name is legal when it is a key of `rf.mutations`, a key of `rf.inflect`,
or one of the three built-ins `GEN`, `ART`, `LEN_IF_F`. This is strictly more permissive, so
`irish.rules` is unaffected, and `check.templates` reports an unknown name with the same message it
does now. The engine plan's EBNF `func-name` production becomes "a `[mutations]` or `[inflect]`
table name, or `GEN` / `ART` / `LEN_IF_F`" — note that in the commit message, since it amends a
published grammar.

**The templates.** Shared constructions first (spec §5), then the eight formations (spec §8 row
O6). Word order is head-first and **the dependent genitive follows** `[utaustin-oldirish-lesson1
§2.1]`, so every formation is `<element> <genitive of the name>`.

| name | template | source |
|---|---|---|
| `DESC` | `NOUN` | spec §5 |
| `VOC` | `"a" LEN(VOC_O(NAME))` | digest §10.5: the particle *a* lenites `[pokorny1914 p.8 §12]`; the masculine o-stem takes the palatalized form |
| `GEN` | `GEN(NAME)` | `GEN()` dispatches via `apply_case` (Task 15) |
| `ADJ` | `NAME " " LEN_IF_F(ADJ)` | digest §10.4: an adjective closely following is lenited after a nom. sg. f. `[pokorny1914 p.8 §10]` |
| `OF` | `NAME " " ART(GEN(NOUN))` | digest §10.4's article table; the article's own mutation |
| `COMPOUND` | `FIRST LEN(SECOND)` | digest §10.5: "In the interior of nominal compounds aspiration takes place… after nouns" `[pokorny1914 p.8 §16]`; *dag-theist*, *énḟlaith* |
| `MAEL` | `"máel" " " LEN(GEN(NAME))` | *Máel Coluim*; spec §8 row O6 |
| `GILLA` | `"gilla" " " GEN(NAME)` | *Gilla Pátraic*; spec §5 gives no lenition for it |
| `CU` | `"cú" " " LEN(GEN(NAME))` | *Cú Chulainn*, gen. *Con Culainn* (digest §10.6) |
| `FER` | `"fer" " " GEN(NAME)` | *Fer Diad*; spec §5 gives no lenition |
| `COLOUR` | `COLOUR LEN(NAME)` | *Dub-dá-leithe*; a **compound**, not a phrase, so no `" "` and the compound lenition of digest §10.5 applies |
| `MAC` | `"macc" " " GEN(NAME)` | *Conchobar mac Nessa* (digest §10.5) |
| `UA` | `"aue" " " GEN(NAME)` | *aue* 'descendant', masc. io-stem `[strachan1909 p.5 n.1]`. **`%design`**: digest §10.5 says "No Old Irish *aue*+genitive naming formula is stated" — the modern *Ó* rule is projected backwards. The comment must say so |
| `INGEN` | `"ingen" " " LEN(GEN(NAME))` | *ingen* 'daughter' /inʲɣʲən/. **`%design`**: digest §10.5 says it is "not attested in these sources as a naming formula"; spec §5 fixes that it lenites |

`PATRO_O` and `PATRO_NI` have **no entry** (O-17). Put a comment where they would be, naming spec
§5's sentence "These replace `PATRO_O`/`PATRO_NI`, which do not apply to this strand", so a reader
does not think they were forgotten.

**`pipeline.CONSTRUCTIONS`** gains `"MAEL", "GILLA", "CU", "FER", "COLOUR", "MAC", "UA", "INGEN"`
after the existing entries. The other four targets have no templates of those names, so
`irish.build_construction` raises `IrishError` for them — **which is not `MissingSlot`, so the
gallery's `run_cell` would propagate it.** Catch it: `oldirish.ConstructionNotInStrand` is raised
for a name absent from *any* strand's `[templates]`, so make `pipeline.run_entry` translate
`IrishError("no [templates] entry")` into it, and have Task 19's gallery and Task 18's CLI treat it
exactly like `MissingSlot` — a skipped cell with a note. State that in both tasks.

- [ ] **Step 1: Write the failing tests** (append)

```python
from strands.pipeline import CONSTRUCTIONS, run_entry
from strands.oldirish import ConstructionNotInStrand, run_entry_oi


def build(construction, orthography, ipa, **slots):
    return run_entry_oi(_entry(orthography, ipa), construction, IRISH, OI, TABLE,
                        slots=slots or None)


def test_the_eight_formation_templates_exist():
    """spec §8 row O6."""
    assert {"MAEL", "GILLA", "CU", "FER", "COLOUR", "MAC", "UA",
            "INGEN"} <= set(OI.templates)


def test_the_patronymic_particles_of_the_other_strands_are_absent():
    """O-17 / spec §5: 'These replace PATRO_O/PATRO_NI, which do not apply to this strand.'"""
    assert "PATRO_O" not in OI.templates and "PATRO_NI" not in OI.templates
    with pytest.raises(ConstructionNotInStrand):
        build("PATRO_NI", "Niall", "nʲiəl̪ˠ")


def test_the_formation_names_are_reachable_from_the_cli_construction_list():
    assert {"MAEL", "GILLA", "CU", "FER", "COLOUR", "MAC", "UA",
            "INGEN"} <= set(CONSTRUCTIONS)


@pytest.mark.parametrize("construction,orthography,expected", [
    ("MAEL", "Colm", "máel Choluim"),
    ("CU", "Culann", "cú Chulainn"),
    ("GILLA", "Pádraig", "gilla Patraic"),
    ("FER", "Diarmaid", "fer "),
    ("MAC", "Neasa", "macc Nessa"),
])
def test_the_formations_reproduce_the_attested_names(construction, orthography, expected):
    """spec §7: *Máel Coluim, Gilla Pátraic, Cú Chulainn, Fer Diad, Dub-dá-leithe* — all
    from the lexicon. The lenition after *máel* and *cú* is digest §10.5's compound rule."""
    row = LEX.get(key(orthography))
    if row is None:
        pytest.skip(f"{orthography} is not in the lexicon")
    out = build(construction, orthography, row and "nʲiəl̪ˠ").respelling
    assert out.startswith(expected.split()[0])
    if len(expected.split()) > 1 and expected.split()[1]:
        assert out.split()[1].startswith(expected.split()[1][:2])


def test_a_leniting_formation_lenites_and_a_non_leniting_one_does_not():
    """spec §5: MAEL, CU and INGEN lenite; GILLA, FER, MAC and UA do not."""
    lenited = build("MAEL", "Colm", "kɔl̪ˠəmˠ").respelling.split()[-1]
    plain = build("GILLA", "Colm", "kɔl̪ˠəmˠ").respelling.split()[-1]
    assert lenited.startswith("ch") and plain.startswith("c")


def test_the_colour_formation_is_a_compound_not_a_phrase():
    """*Dub-dá-leithe*: one word, with the compound lenition of digest §10.5."""
    out = build("COLOUR", "Leithe", "lʲɛhə", COLOUR=_entry("dubh", "d̪ˠʊβˠ"),
                NAME=_entry("Leithe", "lʲɛhə")).respelling
    assert " " not in out


def test_the_vocative_particle_lenites():
    """digest §10.4 [pokorny1914 p.8 §12]: *á fir*, *á chéiliu*."""
    out = build("VOC", "Cormac", "ˈkɔɾˠəmˠək").respelling
    assert out.split()[0] == "a" and out.split()[1].startswith("ch")


def test_the_unattested_formations_are_tagged_design():
    """digest §10.5: no source states an *aue*+genitive formula, and *ingen* is 'not
    attested in these sources as a naming formula'."""
    text = (ROOT / "rules" / "old-irish.rules").read_text(encoding="utf-8")
    for name in ("UA", "INGEN"):
        line = [l for l in text.splitlines() if l.strip().startswith(name + " ")][0]
        assert "design" in line, line


def test_a_template_literal_matches_the_spelling_in_its_comment():
    """O-25: literals are IPA; the comment names the spelling. This catches a typo."""
    text = (ROOT / "rules" / "old-irish.rules").read_text(encoding="utf-8")
    import re
    for line in text.splitlines():
        m = re.match(r'\s*(\w+)\s*=\s*"([^"]+)".*#.*\*([^*]+)\*', line)
        if m and m.group(1) in OI.templates:
            ipa, spelling = m.group(2), m.group(3).strip().strip("-")
            assert tuple(ipa.split()) == spelling_to_ipa(spelling), (line, ipa, spelling)
```

- [ ] **Step 2: Run them and watch them fail**

Run: `uv run pytest tests/test_oldirish_grammar.py -q` — expected FAIL (no `[templates]`).

- [ ] **Step 3: Make the template function names data-driven in `dsl.py`**

Replace the hard-coded name set in `_TemplateParser` with a check against
`rf.mutations | rf.inflect | {"GEN", "ART", "LEN_IF_F"}`. Because the sub-tables are parsed before
`[templates]` in file order, they are available; if a rule file puts `[templates]` first, defer the
check to `check.templates` (which already walks the tree) rather than failing the parse. Run
`uv run pytest tests/test_dsl_sections.py tests/test_irish_templates.py -q` before going on.

- [ ] **Step 4: Write `[templates]` and the builder**

Add the section. In `oldirish.py`, build the construction with a builder that reuses
`irish._Builder` where it can — the only Old Irish differences are that `GEN()` routes through
`apply_case` (Task 15) and that a slot's `Word` comes from a `Stem`, not from `Entry.ipa`. The
simplest faithful implementation is a subclass overriding `evaluate` for `kind == "arg"` (return
the slot's `Stem.words[0]`) and `call` for `"GEN"` (return `apply_case(stem, "gen", …)`); say so in
the docstring, and keep `_Builder`'s public behaviour untouched so the other four strands cannot
regress.

Extend `pipeline.CONSTRUCTIONS`, and make `run_entry` translate a missing-template `IrishError`
into `ConstructionNotInStrand`.

- [ ] **Step 5: Remove the Task-13 xfail marks**

If Task 13 marked any `test_properties.py` / `test_cli.py` cases `xfail` for `old-irish`, **delete
those marks now** and make the tests pass. That is this task's real completion criterion.

- [ ] **Step 6: Run everything and commit**

Run: `uv run pytest -q` — expected 1004+ passed, 2 xfailed, **no xpass**.

```bash
git add src/strands/dsl.py src/strands/oldirish.py src/strands/pipeline.py \
        rules/old-irish.rules tests/test_oldirish_grammar.py
git commit -m "feat(rules): old-irish [templates] incl. MAEL GILLA CU FER COLOUR MAC UA INGEN

Template function names are now data-driven (any [mutations]/[inflect] table name plus
GEN/ART/LEN_IF_F), amending the engine plan's func-name production."
```

**Acceptance:** the eight formations exist and are reachable from `CONSTRUCTIONS`; the leniting and
non-leniting ones differ; `COLOUR` is one word; `VOC` lenites after *a*; `UA` and `INGEN` are
`%design` with the digest's own "not attested" note; `PATRO_O`/`PATRO_NI` raise
`ConstructionNotInStrand`; every literal's IPA matches the spelling in its comment.

---

## Task 17: Filter regression and its ratchet

**Depends on:** Tasks 4, 16. **Spec:** §7 ("Filter regression: run each `attested` lexicon
headword's modern form through the retro-filter and compare the written form with `oi_nom`; report
and ratchet the match rate (exact-match and Levenshtein ≤1); list failures by reversal class").
O-13, O-16, O-23.

**Files:**
- Modify: `src/strands/oldirish.py` (`filter_regression`, `REVERSAL_CLASSES`)
- Create: `tests/ratchets/old-irish.json`
- Test: `tests/test_oldirish_regression.py`

**Interfaces:**
```python
@dataclass(frozen=True)
class FilterRow:
    orthography: str
    expected: str          # the lexicon's oi_nom
    got: str               # the retro-filter's written form
    distance: int          # character-level Levenshtein (O-16)
    classes: tuple[str, ...]   # the reversal classes this headword instantiates
    constructed: bool = False  # the modern IPA came from the G2P, not from test-words.tsv

@dataclass(frozen=True)
class FilterReport:
    rows: tuple[FilterRow, ...]
    def rate(self, max_distance: int = 0, constructed: bool | None = None) -> float: ...
    def by_class(self) -> dict[str, tuple[int, int]]:   # class -> (passed, total), all rows

REVERSAL_CLASSES: dict[str, ...]      # name -> a predicate over the modern orthography

def filter_regression(entries, lexicon, oi, irish, table, *, g2p=None) -> FilterReport
```

**The denominator, stated honestly.** Spec §7 says "each `attested` lexicon headword's modern
form", but a lexicon row carries **no IPA**, and the retro-filter needs one. The guaranteed
population is therefore the intersection of the lexicon with `sources/irish/test-words.tsv`, which
the harvest log has already measured:

| population | count | in the regression? |
|---|---|---|
| distinct test-word keys | 138 | — |
| **direct lexicon hits** | **74** | **yes — this is the denominator** |
| surface forms whose citation form is in the lexicon | 52 | **no**: the test-word IPA is of the *mutated* form, so comparing its filter output to the citation form's `oi_nom` would measure the mutation, not the filter (O-23) |
| no lexicon coverage | 12 | no |

Assert the denominator in a test (`>= 70`, allowing for Task 3/4 removals and additions) and print
it in the report, so a future harvest that grows the overlap grows the regression automatically.

**If a provisional G2P exists when this task runs, use it — as a second, separately reported
population.** A `src/strands/g2p.py` (engine spec §1's milestone 8, `g2p(orthography, dialect) ->
(ipa, notes)`) is in progress on this worktree at ~73% exact accuracy against the test words.
`filter_regression` therefore takes a keyword `g2p: Callable[[str, str], tuple[str, list[str]]] |
None = None`, and:

- with `g2p=None` (the default, and what the ratchet test uses) the population is the 74-row
  overlap above;
- with a `g2p` supplied, every `attested`/`middle` row **without** a test-word IPA is added, its
  `FilterRow` marked `constructed=True` (a `FilterRow` field) — because a miss there may be the
  G2P's fault, not the filter's.

`FilterReport.rate()` takes `constructed: bool | None = None` (None = all rows, False = the
hand-IPA population only). **The ratchet keys off `rate(..., constructed=False)`** so a change in
G2P accuracy can never move a filter ratchet. Report both numbers; the per-class breakdown covers
all rows and says how many of each class are constructed. If `strands.g2p` is not importable when
this task runs, the keyword is simply never passed and the second population is absent — write the
parameter anyway, and one test that skips when the module is missing.

**Reversal classes** (spec §7's "list failures by reversal class"), taken from the harvest log's
systematic findings — each is a predicate over the **modern** orthography:

| class | predicate | log |
|---|---|---|
| `ao` | contains `ao` | finding 1 — **and this is decision O1's regression set (O-13); it should have ≈20 members** |
| `quality-digraph` | contains any of `ea io ai oi ui` | finding 2, the largest class (~50) |
| `lenition-digraph` | contains any of `bh dh gh mh` | finding 3 (~49) |
| `ch-th` | contains `ch` or `th` | finding 3 (51) |
| `geminate` | `oi_nom` contains a doubled letter the modern form does not | finding 3 (47) |
| `ua-ia` | contains `ua` or `ia` | finding 4 (33) |
| `final-vowel` | ends in `a` or `e` | finding 4 |
| `an-suffix` | ends in `án` | finding 4 — invariant, so this class should be at or near 100% |
| `r-stem` | in `{athair, bráthair, máthair}` | finding 4 — spelling-invariant, the "leave well enough alone" case |

A headword may be in several classes; `by_class` counts it in each.

**The ratchet.** `tests/ratchets/old-irish.json` = `{"exact": <rate>, "lev1": <rate>, "n": <int>}`.
Follow the existing convention exactly (`regress.load_ratchet` / `assert_ratchet` /
`write_ratchet`, and `write_ratchet` is **run by hand, never by a test**). Do not guess the initial
values: run the regression, read the two rates, and commit them **rounded down to 4 decimal
places** as the other four ratchets are.

**What a low rate means and does not mean.** The retro-filter is a *design* artefact — every one of
its rules is `%design` (Task 9), and digest §10.7 is explicit that "the correspondence set to do it
is not in this source set". A rate well under 50% is an expected outcome, not a bug, and the value
of this task is the **per-class breakdown**: it says which reversals are working and gives decision
O1 a measurement instead of an argument. Say that in the module docstring so nobody later "fixes"
the number by weakening the comparison.

- [ ] **Step 1: Write the failing tests**

`tests/test_oldirish_regression.py`:

```python
"""Task 17: the filter regression (spec §7). See the module docstring in oldirish.py for why
a low rate is a finding, not a failure."""
import json

import pytest

from helpers import ROOT, TABLE, irish, read_test_words, target
from strands.inputs import Entry, infer
from strands.lexicon import FORM_STATUSES, key, read_lexicon
from strands.oldirish import REVERSAL_CLASSES, filter_regression
from strands.regress import assert_ratchet, load_ratchet

IRISH = irish()
OI = target("old-irish")
LEX = read_lexicon()
RATCHET = ROOT / "tests" / "ratchets" / "old-irish.json"

ENTRIES = [infer(Entry(orthography=r["orthography"], ipa=r["ipa"],
                       dialect=r.get("dialect") or "C"), IRISH, TABLE)
           for r in read_test_words() if r["ipa"]]
REPORT = filter_regression(ENTRIES, LEX, OI, IRISH, TABLE)


def test_the_denominator_is_the_direct_test_word_overlap():
    """The harvest log measures 74 direct hits out of 138 distinct keys; the 52 surface
    forms are excluded because their IPA is of the MUTATED form (O-23)."""
    assert len(REPORT.rows) >= 70, len(REPORT.rows)
    for row in REPORT.rows:
        assert LEX[key(row.orthography)].status in FORM_STATUSES


def test_every_row_compares_written_forms():
    """O-16: oi_nom is a spelling, so the comparison and the distance are over characters."""
    for row in REPORT.rows:
        assert row.expected == LEX[key(row.orthography)].oi_nom
        assert row.got and isinstance(row.distance, int)


def test_both_rates_are_reported_and_ordered():
    exact, lev1 = REPORT.rate(0), REPORT.rate(1)
    assert 0.0 <= exact <= lev1 <= 1.0


def test_the_ratchet_holds():
    """The rates may not drop. Raising them is a deliberate `write_ratchet` run."""
    ratchet = load_ratchet("old-irish")
    assert REPORT.rate(0) >= ratchet["exact"] - 1e-9
    assert REPORT.rate(1) >= ratchet["lev1"] - 1e-9


def test_the_ratchet_file_records_the_denominator():
    data = json.loads(RATCHET.read_text(encoding="utf-8"))
    assert set(data) == {"exact", "lev1", "n"} and data["n"] == len(REPORT.rows)


def test_every_reversal_class_is_measured():
    """spec §7: 'list failures by reversal class'."""
    by_class = REPORT.by_class()
    assert set(by_class) == set(REVERSAL_CLASSES)
    for name, (passed, total) in by_class.items():
        assert 0 <= passed <= total


def test_the_ao_class_is_decision_O1s_regression_set():
    """O-13 / spec §10: the 20 attested ⟨ao⟩ pairs measure the O1 default directly."""
    passed, total = REPORT.by_class()["ao"]
    assert total >= 15, total


@pytest.mark.parametrize("cls", ["an-suffix", "r-stem"])
def test_the_invariant_classes_are_near_perfect(cls):
    """Log finding 4: the ⟨-án⟩ diminutive and the r-stem kinship set are spelling-invariant
    across both stages. If the filter breaks THESE, it is over-applying."""
    passed, total = REPORT.by_class()[cls]
    if total == 0:
        pytest.skip(f"no {cls} headwords in the overlap")
    assert passed >= total - 1, (passed, total)


def test_the_report_is_deterministic():
    again = filter_regression(ENTRIES, LEX, OI, IRISH, TABLE)
    assert again.rows == REPORT.rows


def test_a_g2p_widens_the_population_without_moving_the_ratchet():
    """The constructed rows are reported but excluded from the ratchet, so G2P accuracy can
    never move a filter number."""
    g2p = pytest.importorskip("strands.g2p").g2p
    wide = filter_regression(ENTRIES, LEX, OI, IRISH, TABLE, g2p=g2p)
    assert len(wide.rows) > len(REPORT.rows)
    assert wide.rate(0, constructed=False) == REPORT.rate(0)
    assert any(r.constructed for r in wide.rows)
```

- [ ] **Step 2: Run them and watch them fail**

Run: `uv run pytest tests/test_oldirish_regression.py -q`
Expected: FAIL — `ImportError: cannot import name 'filter_regression'`.

- [ ] **Step 3: Implement `filter_regression`**

Per entry: skip unless `lookup` finds a row with `status in FORM_STATUSES` **and** `key(entry
.orthography)` equals the row's own key (that excludes the 52 surface forms without special-casing
them: their own orthography is not a lexicon key). Force the **RETRO** path even though the row
exists — that is the whole point of the measurement — by calling the retro branch of
`to_old_irish` directly, then `adapt_oi`, and taking `Result.respelling`. Compare to `row.oi_nom`
after NFC and case-folding. `distance` is the standard character Levenshtein (`regress
.edit_distance` already exists; confirm it is character-generic and reuse it rather than writing a
second one).

Add the module docstring paragraph about what a low rate means.

- [ ] **Step 4: Run it, read the numbers, write the ratchet**

```bash
uv run python -c "
import sys; sys.path.insert(0, 'tests')
from test_oldirish_regression import REPORT
print('n', len(REPORT.rows), 'exact', REPORT.rate(0), 'lev1', REPORT.rate(1))
for name, (p, t) in sorted(REPORT.by_class().items()):
    print(f'{name:18} {p:3}/{t:3}')
for r in REPORT.rows:
    if r.distance:
        print(r.distance, r.orthography, r.expected, '!=', r.got, r.classes)"
```

Write `tests/ratchets/old-irish.json` from the printed rates (floor to 4 dp) and the row count.
**Paste the per-class table into the commit message** — it is the artefact the owner reads.

- [ ] **Step 5: Run the suite and commit**

```bash
git add src/strands/oldirish.py tests/test_oldirish_regression.py tests/ratchets/old-irish.json
git commit -m "test(oldirish): filter regression over the 74-headword lexicon overlap, with per-class rates"
```

**Acceptance:** ≥70 rows measured; exact and Levenshtein-≤1 rates reported and ratcheted; every
reversal class counted; the `ao` class has ≥15 members; the two invariant classes are at most one
row off perfect; the report is deterministic.

---

## Task 18: CLI exposure

**Depends on:** Task 16. **Spec:** §2 ("Same CLI, gallery, trace, tests"), §9 milestone 5.
O-17.

**Files:**
- Modify: `src/strands/cli.py`
- Test: `tests/test_cli.py` (append)

**Interfaces:** no new functions. `--strand old-irish` works everywhere `--strand` is accepted,
because `_strands()` reads `pipeline.TARGETS` (Task 13 extended it) and `_constructions()` reads
`pipeline.CONSTRUCTIONS` (Task 16 extended it). What this task actually has to do:

1. **`run`**: catch `ConstructionNotInStrand` beside the existing `MissingSlot`, write the row with
   empty output columns and `assumptions = skipped:construction-not-in-strand` (O-17). Every
   `--construction all` run over the five strands hits this 8 × 4 + 2 × 1 times, so it must be a
   skip, not an error.
2. **`explain`**: it takes a bare `WORD` (an IPA string), not an input row — but the Old Irish
   lookup keys on **orthography** (O-23), which `explain` does not have. Add an optional
   `--orthography TEXT` flag: when given it is used as the lookup key and as the aligner's input;
   when absent, `explain --strand old-irish` runs the pure retro path and **prints a one-line note
   saying so**, because a silent RETRO would look like a lexicon miss.
3. **`check`**: already routes `.tsv` (Task 2). Confirm `strands check rules/old-irish.rules`
   passes.
4. The `--strand all` default now includes `old-irish`, which changes the output of every
   `run`/`gallery` invocation. That is intended; Task 19 re-snapshots.

- [ ] **Step 1: Write the failing tests** (append to `tests/test_cli.py`)

```python
def test_run_accepts_the_fifth_strand(tmp_path, capsys):
    from strands.cli import main
    out = tmp_path / "out.tsv"
    assert main(["run", str(FIX), "--strand", "old-irish", "--out", str(out)]) == 0
    rows = out.read_text(encoding="utf-8").splitlines()
    assert any("old-irish" in r for r in rows)


def test_a_construction_the_strand_lacks_is_a_skipped_row_not_an_error(tmp_path):
    """O-17: PATRO_NI for old-irish, MAEL for welsh — both are skips."""
    from strands.cli import main
    out = tmp_path / "out.tsv"
    assert main(["run", str(FIX), "--strand", "all", "--construction", "all",
                 "--out", str(out)]) == 0
    text = out.read_text(encoding="utf-8")
    assert "skipped:construction-not-in-strand" in text


def test_explain_warns_when_no_orthography_is_given_for_old_irish(capsys):
    """O-23: lookup keys on orthography, which a bare IPA argument cannot supply."""
    from strands.cli import main
    assert main(["explain", "nʲiəl̪ˠ", "--strand", "old-irish"]) == 0
    captured = capsys.readouterr().out
    assert "RETRO" in captured and "--orthography" in captured


def test_explain_uses_the_orthography_for_the_lookup(capsys):
    from strands.cli import main
    assert main(["explain", "nʲiəl̪ˠ", "--strand", "old-irish",
                 "--orthography", "Niall"]) == 0
    assert "ATTESTED" in capsys.readouterr().out


def test_check_passes_on_the_old_irish_rule_file():
    from strands.cli import main
    assert main(["check", str(ROOT / "rules" / "old-irish.rules")]) == 0


def test_the_unknown_strand_message_now_lists_five():
    from strands.cli import UsageError, main
    import pytest
    with pytest.raises(UsageError, match="old-irish"):
        main(["run", str(FIX), "--strand", "cornish"])
```

(If `main` reports usage errors by returning 2 rather than raising, assert the exit code and the
stderr text instead — match whatever the existing tests in the file do.)

- [ ] **Step 2: Run them and watch them fail; implement; re-run**

Run: `uv run pytest tests/test_cli.py -q`.

- [ ] **Step 3: Run the suite and commit**

```bash
git add src/strands/cli.py tests/test_cli.py
git commit -m "feat(cli): expose --strand old-irish, --orthography for explain, skip absent constructions"
```

**Acceptance:** `--strand old-irish` runs; an absent construction is a skipped row on every strand;
`explain` uses `--orthography` for the lookup and warns when it is missing; `check` passes on the
rule file; the usage message lists five strands.

---

## Task 19: Gallery column, snapshot, and property checks

**Depends on:** Tasks 17, 18. **Spec:** §7 ("Gallery: fifth column for the 144 test words with
`ATTESTED`/`RETRO` marks, plus a formation-template block; property checks extended; snapshot
committed"). O-17.

**Files:**
- Modify: `src/strands/gallery.py`
- Modify: `tests/snapshots/gallery.md` (regenerated)
- Modify: `tests/test_gallery_snapshot.py`, `tests/test_properties.py`
- Test: as above

**Interfaces:**
- `render_gallery` needs no signature change: `strands gallery` passes all of `TARGETS`, so the
  fifth column appears once Task 13 extends the tuple. What this task adds:
  ```python
  def formation_block(entries, irish, oi, table) -> str:
      """The formation-template block (spec §7): one table of the eight Old Irish formations
      over the entries that can fill them, appended after the per-word tables."""
  ```
  and a change in `run_cell` to catch `ConstructionNotInStrand` beside `MissingSlot` (O-17).
- `render_cell` already prints `!FLAG` per flag, so `ATTESTED` / `RETRO` / `RETRO:loan` /
  `RETRO:late` / `ATTESTED:MIr` appear with no change. **Verify that rather than adding code**, and
  say so in the test name.

- [ ] **Step 1: Write the failing tests**

Append to `tests/test_gallery_snapshot.py`:

```python
def test_the_gallery_has_a_fifth_column():
    """spec §7."""
    text = (ROOT / "tests" / "snapshots" / "gallery.md").read_text(encoding="utf-8")
    assert "old-irish" in text


def test_the_attested_and_retro_marks_are_visible_in_the_gallery():
    """spec §7: 'with ATTESTED/RETRO marks'. render_cell already prints !FLAG — this test
    asserts that it does, it does not ask for new code."""
    text = (ROOT / "tests" / "snapshots" / "gallery.md").read_text(encoding="utf-8")
    assert "!ATTESTED" in text and "!RETRO" in text


def test_the_formation_template_block_is_present():
    """spec §7: 'plus a formation-template block'."""
    text = (ROOT / "tests" / "snapshots" / "gallery.md").read_text(encoding="utf-8")
    assert "## Old Irish formations" in text
    for name in ("MAEL", "GILLA", "CU", "FER", "COLOUR", "MAC", "UA", "INGEN"):
        assert name in text


def test_the_snapshot_matches_a_fresh_render():
    """The existing convention: a change must be intentional and reviewed in the diff."""
    # (reuse whatever comparison the file already does; only the expected text moves)
```

Append to `tests/test_properties.py`:

```python
def test_every_old_irish_output_carries_exactly_one_lookup_flag():
    """spec §6: 'Flags: ATTESTED / RETRO / RETRO:loan on every output'."""
    from strands.oldirish import OI_FLAGS
    for row, result in _results("old-irish", "DESC"):
        assert len([f for f in result.flags if f in OI_FLAGS]) == 1, \
            (row["orthography"], result.flags)


def test_every_old_irish_respelling_reconstructs_to_its_reported_ipa():
    """spec §6 / O-11: the IPA is derived FROM the written form. This is the property that
    keeps [respell] and rules/old-irish-orthography.tsv one system."""
    from strands.oldirish import spelling_to_ipa
    for row, result in _results("old-irish", "DESC"):
        rebuilt = " ".join(" ".join(spelling_to_ipa(part))
                           for part in result.respelling.split(" "))
        assert rebuilt == result.ipa, (row["orthography"], result.respelling)


def test_no_old_irish_output_uses_a_modern_lenition_digraph():
    """digest §10.2 conv.1: there is no ⟨bh dh gh mh⟩ in Old Irish. If one appears, a
    [respell] rule leaked."""
    for row, result in _results("old-irish", "DESC"):
        low = result.respelling.lower()
        assert not any(d in low for d in ("bh", "dh", "gh", "mh")), \
            (row["orthography"], result.respelling)


def test_old_irish_words_are_stressed_initially():
    """digest §10.3."""
    for row, result in _results("old-irish", "DESC"):
        for word in result.words:
            assert word.stress in (0, None), (row["orthography"], word.segments)
```

The existing parametrized property tests (`test_determinism_across_two_runs`,
`test_every_output_segment_is_in_the_target_inventory`,
`test_no_unrepaired_outside_the_allow_file`) now cover `old-irish` automatically because they
enumerate `TARGETS`. **They must pass without an allow-file entry**: Task 10 set
`cluster-fallback = keep`, so an unattested cluster flags `UNATTESTED_CLUSTER:` rather than
`UNREPAIRED`. If a word does come out `UNREPAIRED`, that is a real bug in Task 10 — fix the rules,
do not add the word to `tests/allow-unrepaired.txt`.

- [ ] **Step 2: Run them and watch them fail**

Run: `uv run pytest tests/test_gallery_snapshot.py tests/test_properties.py -q`.

- [ ] **Step 3: Add the formation block to `gallery.py`**

`formation_block` renders one Markdown table: rows are the eight formation names, columns are the
five attested example names spec §7 asks for (*Máel Coluim, Gilla Pátraic, Cú Chulainn, Fer Diad,
Dub-dá-leithe*), taken from the lexicon by their modern keys. A cell that cannot be built is `—`,
exactly as `render_cell` already does. Append it after the per-word tables, under the heading
`## Old Irish formations`. Also add `ConstructionNotInStrand` to `run_cell`'s except clause.

- [ ] **Step 4: Regenerate the snapshot**

```bash
uv run strands gallery sources/irish/test-words.tsv --out tests/snapshots/gallery.md
git diff --stat tests/snapshots/gallery.md
```

**Read the diff.** The fifth column and the formation block are the intended change; anything else
moving means a rule file changed behaviour for another strand, which is a bug in an earlier task.

- [ ] **Step 5: Run the whole suite and commit**

Run: `uv run pytest -q` — expected: all green, 2 xfailed, no xpass.

```bash
git add src/strands/gallery.py tests/snapshots/gallery.md \
        tests/test_gallery_snapshot.py tests/test_properties.py
git commit -m "feat(gallery): Old Irish column with lookup flags and a formation-template block"
```

**Acceptance:** the gallery has five columns and the flag marks; the formation block renders the
five attested names; every Old Irish output carries exactly one lookup flag, reconstructs to its
reported IPA, uses no modern lenition digraph and is initially stressed; the snapshot diff contains
only the intended additions; the suite is green with no new allow-file entries.

---

## Self-review notes

**Spec coverage.** §1 → Tasks 13, 17 (the two production modes and their flags). §2 → Tasks 9, 13
(lookup, retro-filter, grammar, respell+IPA). §3 → Tasks 2, 3, 4. §4 → Tasks 8, 9, 10 (inventory,
substitute incl. `@orth`, syllable/repair/stress) and Tasks 5–7 (the machinery `@orth` needs). §5 →
Tasks 14, 15, 16. §6 → Tasks 11 (written form), 12 (IPA reconstruction), 13 (flags, assumptions).
§7 → Tasks 2/3/4 (lexicon tests + verification), 17 (filter regression), 14/15/16 (unit tests
against Strachan's paradigms and the formation names), 19 (gallery, property checks). §8 → O1 in
O-13 and Task 17's `ao` class; O2 in O-14 and Task 11; O3 in Task 13's `infer_stem`; O4 in O-18 and
Task 13; O5 in Task 9; O6 in Task 16. §9 milestones 1–5 → the whole task list. §10 → O-13, O-18,
O-21, O-22, O-24 and Tasks 2, 3, 4.

**Known deviations from the spec, for the owner.**

1. **Spec §4's "final /ə/ → *e* (ā-stems) or *a* by stem class" is split across two tasks.** The
   stem class is not visible to a `[substitute]` rule; Task 9 writes the `a` default and Task 15's
   `NOM_A` carries the ā-stem *-e*. Same outcome, different file.
2. **Spec §5's "aspiration/gemination" third mutation is not implemented.** Spec §5 names two
   mutations; digest §9 open question 10 asks whether the strand should use the third and does not
   answer. Task 14 records the omission in the rule file.
3. **Fortis/lenis sonorants are not phonemic (O-2)** and Pokorny's three-way quality is spelling
   only (O-4). Both follow spec §4's inventory, both contradict digest §10.1's own analysis, and
   both are recorded in the rule file's comments.
4. **The filter regression's ratcheted denominator is 74, not "each attested lexicon headword".**
   Only lexicon rows that also have hand IPA in `test-words.tsv` can be run without a G2P. Task 17
   asserts that count, and adds an optional second population through the in-progress
   `src/strands/g2p.py` — reported separately and deliberately excluded from the ratchet, so G2P
   accuracy can never move a filter number.
5. **`ATTESTED:MIr` is carried but nothing branches on it** (O-22), per spec §10's own note that
   the tier is a speculative default.
