# Strand 5: Old Irish — implementation plan (spec milestones 1–5), draft 2

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development
> (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Draft 2** (2026-08-27) rebuilds draft 1 on **spec §11**, which overrides §2, §4 and §5: Old Irish
grammar now operates on the *written* form. It applies all 42 required changes of
`docs/plans/review-oi-opus.md` (R1–R33 with sub-items) and the eight P1 findings of the GPT-5.6
plan review. Where draft 1's interpretation register contradicted a review, the interpretation has
been **rewritten, not annotated** — read O-1…O-31 as the current statement. Draft 1's Task 7
(mutation provenance `ECL:`/`LEN:` tags) is **deleted**: spec §11 removes the modern-mutation
reversal that motivated it.

**Goal:** Add a fifth strand, `old-irish`, that produces classical Old Irish forms of the same
modern-Irish input rows — by lexicon lookup where an attested form exists, by a rule-based
retro-filter otherwise — marked `ATTESTED` / `ATTESTED:MIr` / `RETRO` / `RETRO:loan` /
`RETRO:late`, with Old Irish morphology applied to the spelling, editorial orthography, and an IPA
reconstructed one-way from the finished written form.

**Architecture.** The central object is the **spelled word** (spec §11): a lossless sequence of Old
Irish grapheme tokens plus capitalization and initial-mutation metadata, defined in
`src/strands/spelled.py`. Lookup produces one directly from the lexicon's `oi_nom`; the
retro-filter produces one from its `[respell]` output. `[mutations]` and `[inflect]` are **grapheme
operations** on it. `spelling_to_ipa` runs **once, at the end**, one-way, to make `Result.ipa`.
Three engine additions support the filter: a per-segment orth-tag channel on `Word` filled by a
modern-orthography↔IPA aligner, the `@orth("…")` rule item that reads it, and a lookup stage.

**Tech Stack:** Python ≥3.12, `uv`, `pytest`. No runtime dependencies (standard library only).
Every command runs through `uv run` from `phonotactics/`. The system `python3` is 3.10 — do not
use it.

**Spec:** `docs/specs/2026-08-27-old-irish-design.md`. **Read §11 first — it overrides §2, §4 and
§5.** §10 amends §3 and §8. It extends `docs/specs/2026-08-25-engine-design.md`, whose §12
overrides that file's §§1–11. Linguistic content: `sources/irish/digest.md §10` and the `bib.md`
entries `pokorny1914-oldirish-grammar`, `strachan1909-oldirish-paradigms`, `wiki-old-irish`,
`wiki-old-irish-grammar`, `wiki-old-irish-phonhistory`, `utaustin-oldirish-lesson1`, `edil`. Data
already on disk: `rules/old-irish-lexicon.tsv` (299 rows) and `rules/old-irish-lexicon-log.md`.
Reviews that shaped this draft: `docs/plans/review-oi-opus.md`. Task format:
`docs/plans/2026-08-25-engine-plan.md`, whose interpretation register (I-1…I-41) is still in force
and is not repeated here.

## Global Constraints

- Python ≥3.12; package `strands` under `src/strands/`; CLI entry point `strands`. No runtime
  dependencies outside the standard library.
- All paths relative to `phonotactics/` unless stated otherwise.
- Determinism is a hard requirement: identical input + data files ⇒ byte-identical output.
- **Test-first, always** (engine spec §12.I): every task — the rule-file and data tasks included —
  writes its tests against an absent or skeletal artefact, runs them, watches them fail, and only
  then writes the artefact.
- Files are UTF-8, NFC-normalized on read (I-1).
- Every rule line in `old-irish.rules` carries a citation: `# digest §10.n`, `# [bibkey p.N]`, or
  `# design: <spec §8 row or O-number>` (R32 — draft 1's `# design: O<n>`-only form was too narrow
  and no rule satisfied it).
- Rule tags are exactly one of `%attested`, `%design`, `%fallback`; default `%attested`. A rule
  whose digest section states the opposite, or states nothing, is `%design`. **A rule that a
  lexicon pair instantiates may be `%attested` with that pair cited** (spec §4; R17).
- Every lexicon row carries a citation; uncited rows are rejected by `strands check`.
- **The suite is 1004 passed / 2 xfailed at the start of this plan. No task may reduce it.** Run
  `uv run pytest -q` before every commit.
- Reuse the engine's mechanisms rather than adding new ones: captures/backreferences (§12.C),
  inline sets, the declared classes `BROAD`/`SLEN`/`UNMARKED` (§12.J / I-41), `nuclei` (§12.B),
  `cluster-fallback = keep` (§12.E). Exactly three additions are sanctioned, all by the Old Irish
  spec: the orth-tag channel with `@orth("…")` (§4, §11), the lookup stage (§2), and the spelled
  word (§11).
- **Working-tree state, verified:** `src/strands/g2p.py` is **committed** (2760b0e, 6207634) and
  `src/strands/inputs.py`'s `declension` work is **committed** (77b1ff7). Task 13's `infer_stem`
  may rely on `Entry.declension` without further conditions.

---
## Spec interpretations

The spec leaves the following underdetermined. Each is resolved here by the simplest faithful
reading. **Implementers follow these, not their own reading.** They are numbered `O-n` alongside
the engine plan's `I-n`. Numbers are stable across drafts; **O-8 is withdrawn**, not reused.

### The central object

- **O-27 The spelled word** (spec §11). Old Irish stages pass around a `SpelledWord`: an ordered
  tuple of **grapheme tokens** plus `capitalized: bool` and `mutation: str` (`""`, `"LEN"` or
  `"NAS"`). It is **lossless**: `"".join(tokens)` is the written form up to capitalization, which is
  stored, not spelled. Tokens come from one table (`rules/old-irish-orthography.tsv`) that also
  carries each token's reconstruction, so there is no second alphabet to keep in sync. Silent
  tokens (`ḟ`, the glide `i`), the punctum forms (`ṡ`, `ḟ`) and the unresolved ending marker `ə`
  are ordinary tokens — the punctum forms are `cons`/`silent` rows carrying a plain-letter
  `punctum` column, not a role of their own. Task 7 defines
  it; every other Old Irish task consumes it. This replaces draft 1's IPA-internal grammar and is
  what makes the mutation/reconstruction bridge lossless (GPT P1 #1).
- **O-10 Old Irish grammar operates on the spelled word, not on IPA** (spec §11, replacing draft
  1's O-10). `[mutations]` and `[inflect]` are **grapheme-token rewrites**; `[templates]` composes
  spelled words; template literals are **spellings** (O-25). The engine's `Rule`/`apply_section`
  machinery is *not* reused for them — it is typed to IPA segments — so Task 7 provides a small
  grapheme-rewrite applier of its own, and `strands check` validates the tables against the
  grapheme table rather than against `features.tsv`.
- **O-11 `spelling_to_ipa` runs once, at the end, and is one-way** (spec §11). It takes the finished
  `SpelledWord` (after mutation and inflection) and returns segments; `Result.ipa` joins segments
  **without separators inside a word** and with a single space between words (GPT P2). The
  pre-reconstruction phonology of a RETRO word survives in the trace. There is **no** round trip
  requirement in the other direction, and draft 1's `respell(spelling_to_ipa(x)) == x` test is
  deleted: it was the constraint that made the bridge lossy.
- **O-14 `punctum` is a rendering option applied after reconstruction** (spec §11, §8 row O2).
  `[meta] punctum = on|off`, default `on`. `off` substitutes each token's plain form from the
  grapheme table's **`punctum` column** (`ṡ→s`, `ḟ→f`) in the **output string only**;
  the tokens, the metadata and the IPA are unaffected, so the setting provably cannot change the
  IPA. A test asserts exactly that.

### Inventory and segments

- **O-1 Segment spellings for the lenited series.** Spec §4 writes `/β ð ɣ μ θ x/`. Project canon
  is IPA with diacritics (engine spec §12.F), so `μ` is written **`β̃`**. New `features.tsv` rows:
  `β βʲ β̃ β̃ʲ θʲ ðʲ ɣʲ` — **seven, not draft 1's six** (R26): `j` is `sonorant +, consonantal −,
  approximant +`, a glide, so it is not the fricative /ɣʲ/ that digest §10.1 charts, and any
  `[C +continuant −sonorant]` bundle over the lenited series would silently miss it. Slender `/xʲ/`
  **is** the existing `ç` — that identity is exact (`ç` and `x` differ only in `front`) and is
  asserted by a test.
- **O-2 No fortis/lenis sonorant contrast.** Spec §4's `[inventory]` lists no `/L N R/`, and digest
  §10.8 conflict 2 records a held source omitting them. Fortis is carried by the **doubled grapheme
  token** ⟨ll nn rr mm⟩, which reconstructs to two identical segments (I-2). Because the doubled
  letter is **one token**, an inflection that palatalizes it moves both halves together, which is
  what R29's geminate breakage was about.
- **O-3 Quality is not reversed.** Spec §4: broad/slender distribution is deliberately *not*
  reversed. Old Irish segments therefore carry the modern `ˠ`/`ʲ` marks and the plain-dorsal
  convention of I-41. `old-irish.rules [classes]` copies `BROAD`, `SLEN`, `UNMARKED` from I-41 and
  extends them with the O-1 segments.
- **O-4 Pokorny's three-way quality is a spelling matter only** (digest §10.1 CONFLICT, §10.2
  conv. 5). It lives in the grapheme table's glide tokens and in `[respell]`; no `ʷ`-marked segment
  is ever created.
- **O-5 `/h/`, `/f/` and `/s/` are inventory members.** Digest §10.1 charts /s/ as phonemic on its
  own minimal pairs (*sonn* ~ *son*) and /f/ as a full member; spec §11 (iii) confirms /h/ is in the
  inventory as the lenition product of *s* and in *h*-initial loans. Spec §4's "no phonemic /h/,
  /s f h/ as lenition products only" is honoured by restricting what **creates** them, not by
  omitting them (which would make the fallback rewrite them).
- **O-28 Diphthong values** (R19). Draft 1's `aːi oːi uːi aːu eːu iu iə uə` was wrong: digest §10.8
  conflict 5 quotes Pokorny writing ⟨aí⟩ *precisely* to distinguish it from long ⟨á⟩ plus a palatal
  glide, and `iə`/`uə` are the modern values using this file's reduction vowel. `wiki-old-irish`
  §Vowels gives the eight as **ai oi ui au eu iu ia ua**, and those are the values used, written
  ⟨aí oí uí áu éu íu ía úa⟩. The `Goídelc` [ˈɡoːi̯ðʲelɡ] infobox transcription in digest §10.6 is the
  one counter-datum and is recorded as a conflict in the rule file, not generalized from. The
  `nuclei` list also carries `əi əu`, which the filter can pass through from modern Irish
  (*Tadhg* /t̪ˠəiɡ/).
- **O-29 Nasalized voiced stops: written ⟨mb nd ng⟩, reconstructed as a single nasal** (R25).
  Digest §10.2's master table is explicit — "b … Initial eclipsed ⟨mb⟩ **/m/**" — and §10.4 renders
  Pokorny as "/b/ → /m/ ⟨mb⟩". Only §10.4's contrast-set row (*a m-bo* /a mbo/) suggests a cluster.
  The spelled-word model expresses this without strain: `mb` is one grapheme token whose
  reconstruction is `(mˠ,)`. The digest-internal conflict is recorded in the token row's comment.

### The aligner and `@orth`

- **O-6 `@orth("X")` is an ItemSpec, not a boundary atom, and its tags are positional** (spec §11).
  Written `@orth("bh")`; legal as a whole TARGET item and as a context atom; matches **exactly one
  segment** whose orth tag equals `X` after NFC + casefolding. A multi-segment grapheme tags its
  segments **positionally** — `ia:1`, `ia:2` — so a rule may target either element
  (`@orth("ia:1") -> i`) or claim the whole unit with a two-item target
  (`@orth("ia:1") @orth("ia:2") -> i a`). A single-segment grapheme's tag carries **no** suffix.

  **`@orth("X")` is sugar for the match bundle `[orth="X"]`, and a bundle may carry an `orth=`
  constraint beside a class name and feature constraints.** This is how one item states *both* the
  spelling and the quality of what it matches, which R11 showed draft 1 could not do: a single
  `@orth("bh") -> β` applies to `w`, `vˠ` **and** `vʲ` and flattens slender to broad. The
  retro-filter therefore writes the pair `[BROAD orth="bh"] -> β` / `[SLEN orth="bh"] -> βʲ`,
  reusing the declared classes of I-41 rather than adding a mechanism. No
  capture suffix; never in a REPLACEMENT; never inside `{}` or `[]`. A segment with no tag matches
  nothing — the aligner's documented failure mode (O-7). This retires draft 1's S1 problem: position
  is in the tag, not inferred from phonological context.
- **O-7 The aligner is a monotonic DP over a grapheme→segment table**, longest-unit-first then file
  order, first complete path wins, memoized dead nodes. Failure is **total**: all-empty tags plus a
  trace entry `orth:unaligned`, never partial. Coverage is a **measured, per-class number**
  (spec §11), stated in Task 5, not a bare threshold; the table includes the epenthetic-schwa,
  eclipsis-digraph and doubled-letter units.
- **O-8 — withdrawn.** Draft 1 wrote `<TABLE>:<radical>` mutation-provenance tags so the filter could
  reverse modern eclipsis. Spec §11 removes the need: the strand takes the **citation form** and
  applies its own Old Irish mutations, so no modern mutation is ever reversed. Draft 1's Task 7 is
  deleted with it. The eclipsis **digraphs** are still needed by the aligner (a corpus row may be
  spelled *mbean*), but as ordinary orthographic units, not provenance.

### Pipeline and lookup

- **O-9 Where the lookup stage lives.** `pipeline.lookup()` is stage **1b**, called from
  `pipeline.run_entry()` after `parse_construction` and before any construction is built.
  `run_entry` dispatches on `[meta] strand`: `old-irish` hands off to `oldirish.run_entry_oi`,
  which composes the stage functions in the Old Irish order. `pipeline.adapt()` is not modified.
- **O-23 Lookup keys on the citation form** (spec §11: "Input is the citation form"). The Old Irish
  strand does **not** consume the modern template's mutated output; it takes `Entry.orthography` and
  `Entry.ipa` as given and applies its own `[templates]`. Matching is exact after NFC + casefold
  (O-19); no de-mutation, no fuzzy fallback. A corpus row whose own `orthography` cell is a surface
  form (*a Sheáin*, *na bpeann*) is a `RETRO` miss, and that is correct.
- **O-30 The vocative default is identity** (R23; digest §10.5 [pokorny1914 p.65 §142]: "The
  vocative has in the singular the same form as the nominative… The masculine o-stem and io-stem
  are the exceptions"). `VOC_O` applies **only** when the stem class is `o`; every other class takes
  the nominative unchanged. The particle *a* and its lenition are unconditional.
- **O-17 `PATRO_O`/`PATRO_NI` are absent from this strand; the eight formation names are added.**
  They stay in `pipeline.CONSTRUCTIONS` for the other four targets; `old-irish.rules [templates]`
  has no entry for them and `oldirish` raises `ConstructionNotInStrand`, which the CLI and gallery
  report as a skip. `DESC+ADJ` and `DESC+NOUN` (R30) are handled by `run_entry_oi` calling
  `parse_construction` and, since Task 8 declares no `epithet-ADJ`/`epithet-NOUN`, resolving the
  slot to "no affix" — so **`DESC+ADJ` equals `DESC`**, with an `epithet:<SLOT>-unmapped-in-Old
  Irish` assumption, and a test asserts the equality.
- **O-25 Template literals are spellings** (spec §11), e.g. `MAEL = "Máel" " " GEN(NAME)`. They are
  tokenized by the grapheme table like any other spelled word. Draft 1's IPA literals are gone.
- **O-32 Capitalization** (R31c). `SpelledWord.capitalized` is set from the source (`oi_nom`'s first
  character, or the modern `Entry.orthography`'s) and re-applied at render. Grapheme tokens are
  stored **lower-case**, so every rewrite table is written once. A formation element written
  lower-case in the lexicon (*macc*, *ua*, *ingen*, *cú*, *fer*, *gilla*) stays lower-case; the name
  it governs keeps its own capitalization. Tests assert on the rendered string, not on a casefold.

### Data

- **O-19 Lexicon keys** are `unicodedata.normalize("NFC", s).strip().casefold()`. Duplicate keys are
  a `check` error. Measured: the committed 299 rows have **299 distinct keys** — no duplicates.
- **O-18 `none` rows and their two flags.** `status = none` requires `oi_nom`, `oi_gen`, `stem`,
  `gender` empty and `source` to cite an etymology. Spec §10 splits the flag: `RETRO:loan` for a
  borrowing, `RETRO:late` for an Irish-internal post-Old-Irish coinage. This is a **`kind` column**,
  not a note-parse. The harvest log's 12/17 split is the starting point, but Task 3 **re-checks it**
  (S4: *spraoi* and *gasúr* have notes calling them loans while the log classes them `late`).
- **O-21 Stem classes.** Spec §10 widens `stem` to `o | ā | i | u | n | dental | velar | r | s |
  indecl | irregular`. `o` absorbs io-stems, `ā` absorbs iā-/ī-stems. `indecl` inflects to itself.
  `irregular` is reserved for suppletive words and keeps `oi_gen` mandatory. The committed file's
  **37 `irregular` rows** predate the widening and cover four real paradigms; Task 3 reclassifies
  them, and Task 15 may not treat `irregular` as a class.
- **O-33 A blank lexicon `stem` is inferred, and the inference is reported** (R31d). Measured: 91
  rows have a blank `stem`, of which 63 are `attested`. Draft 1 gave those a silent o-stem guess
  with no `assumptions` tag, because O-21 says a lexicon-supplied class contributes no tag. Revised:
  a **blank** class is not a supplied class — it routes through `infer_stem` and is tagged
  `stem:from-declension-*` like any RETRO row. Only a **non-empty** lexicon class is silent.
  `infer_stem`'s last-resort default is `ā` for a feminine and `o` otherwise (S22), tagged
  `stem:default-by-gender`.
- **O-22 The Middle Irish tier.** `status = middle` → flag `ATTESTED:MIr`; identical to `attested`
  in every other respect. Spec §10 marks it a speculative default, so nothing branches on it.
- **O-24 The lexicon already exists**, and so does its log. `rules/old-irish-lexicon.tsv` has 299
  rows (270 `attested`, 29 `none`, 163 with `oi_gen`), and a 35-row independent verification has
  been done — **recorded as a prose table in `rules/old-irish-lexicon-log.md` §"Sample
  verification", not as a TSV** (R3: draft 1 claimed a `verification.tsv` that does not exist).
  Task 3 back-fills that pass into `rules/old-irish-lexicon.verification.tsv` as part of writing its
  own second pass, so the two are comparable.

### Measurement

- **O-16 The filter regression compares written forms**, `Result.respelling` vs `oi_nom`, with a
  **character-level** Levenshtein distance, because `oi_nom` is a spelling.
- **O-31 The regression population is 54 keys, measured** (R1; spec §11 fixes the definition). It is
  the set of unique citation-form keys that are in `test-words.tsv` with hand IPA **and** have a
  form-bearing (`attested`/`middle`) lexicon row. Measured from the two committed files: 138
  distinct test-word keys (all with IPA), 74 direct lexicon hits, of which **20 are `status = none`
  and excluded**, leaving **n = 54**. Duplicate keys: 5, of which 4 are in the population. The
  tie-break is "the first row whose `features` contains `src:attested`, else the first row in file
  order" — the fallback is required, because `niamh` (in the population) has **no** `src:attested`
  row. `dubh`, `leanbh`, `naomh` have 2, 2 and 3 all-attested rows; the rule picks row 0 and the
  variant it discards is real (`w`~`vˠ`, fortis~lenis), so the choice is recorded in the report.
- **O-13 Modern ⟨ao⟩, and where decision O1 can be measured** (R2, R13). The filter writes ⟨áe⟩ —
  which needs a `[respell]` rule producing the digraph, not draft 1's single `aː` (R13). Attested
  words take their spelling from the lexicon. **The ⟨ao⟩ regression set has 4 members in the
  ratcheted population, not 20** (measured): the 20 pairs exist only across the whole lexicon, i.e.
  only in the G2P-widened population. Task 17 therefore asserts `>= 4` on the ratcheted population,
  reports the ⟨ao⟩ breakdown over the widened one, and the module docstring states that **decision
  O1 cannot be measured without the G2P**.
- **O-12 `RETRO:loan` and `RETRO:late` are filtered identically**; only the flag differs.
- **O-15 The epenthetic-schwa environment** is "after a sonorant, before a consonant" (digest §2.4),
  written with the declared `SONORANT` class in `old-irish.rules [classes]` (S15 — draft 1's wording
  said "an inline set, not a class"; the class is correct and the wording is fixed here).
- **O-20 Unattested clusters are kept, not repaired**: `cluster-fallback = keep` (engine §12.E), so
  an Old Irish word keeping a modern cluster is flagged `UNATTESTED_CLUSTER:<cluster>` rather than
  `UNREPAIRED`, and needs no allow-file entry.
- **O-26 `[inflect]` sub-table naming.** `<CASE>_<STEM>`: `GEN_O`, `GEN_A`, `GEN_I`, `GEN_U`,
  `GEN_N`, `GEN_DENT`, `GEN_VELAR`, `GEN_R`, `GEN_S`, `VOC_O`, `NOM_A`, `NOM_O`, `DAT_O`, `DAT_A`,
  `GEN_ACH`. `ā` is spelled `A` because class names match `[A-Z][A-Z0-9_]*` (I-10); `indecl` and
  `irregular` have no table.

---
## File structure

```
phonotactics/
  rules/
    features.tsv                     # Task 1: + 7 hand rows (β βʲ β̃ β̃ʲ θʲ ðʲ ɣʲ)
    features.README.md               # Task 1: their derivation
    old-irish-lexicon.tsv            # EXISTS (299 rows). Task 2 adds `kind`; Tasks 3, 4 fix/extend
    old-irish-lexicon-log.md         # EXISTS — the harvest log; Tasks 3, 4 append sections
    old-irish-lexicon.verification.tsv   # Task 3 back-fills the first (35-row) pass from the log
    old-irish-lexicon.verification2.tsv  # Task 3: the second pass
    irish-orthography.tsv            # Task 5: modern grapheme -> segment table (the aligner)
    old-irish-orthography.tsv        # Task 7: the Old Irish GRAPHEME TABLE (tokens + reconstruction)
    old-irish.rules                  # Tasks 8, 9, 10, 11, 13, 14, 15 — strictly in that order
  src/strands/
    word.py                          # Task 5: + the `orth` channel
    orth.py                          # Task 5: the aligner (NEW)
    dsl.py                           # Task 6: `@orth`; Task 15: per-file template function registry
    rewrite.py                       # Task 6: match_item gains word/index
    irish.py                         # Task 5: `_join` carries `orth` (R7)
    check.py                         # Tasks 2, 6, 7, 14: lexicon / @orth / grapheme-table checks
    lexicon.py                       # Task 2 (NEW)
    spelled.py                       # Task 7: SpelledWord, grapheme table, spelling_to_ipa (NEW)
    oldirish.py                      # Task 12 (NEW); Tasks 13, 14, 15, 16 extend it
    pipeline.py                      # Task 12: lookup stage, TARGETS, dispatch; Task 15: CONSTRUCTIONS
    cli.py                           # Task 17
    gallery.py                       # Task 18
  tests/
    test_lexicon.py                  # Task 2
    test_lexicon_data.py             # Tasks 3, 4
    test_orth_align.py               # Task 5
    test_dsl_orth_atom.py            # Task 6
    test_spelled.py                  # Task 7
    test_rules_old_irish.py          # Tasks 8, 9, 10, 11
    test_oldirish_lookup.py          # Task 12
    test_oldirish_grammar.py         # Tasks 13, 14, 15
    test_oldirish_regression.py      # Task 16
    ratchets/old-irish.json          # Task 16
    snapshots/gallery.md             # Task 18 (regenerated)
```

## Task list and dependencies

| # | Task | Depends on |
|---|---|---|
| 1 | `features.tsv` hand rows for the Old Irish lenited series (7 rows) | — |
| 2 | Lexicon schema, reader, `strands check` validation | — |
| 3 | Lexicon fix-up: stem classes, `kind` values, both verification files | 2 |
| 4 | Middle Irish tier — the 49 unresolved names | 3 |
| 5 | Orthography↔IPA aligner and the `Word.orth` channel | — |
| 6 | The `@orth("…")` rule item with positional tags | 2, 5 |
| 7 | **`SpelledWord`, the grapheme table, `spelling_to_ipa`, grapheme rewrites** | 1, 6 |
| 8 | `old-irish.rules`: `[meta] [inventory] [classes]` | 1, 7 |
| 9 | `old-irish.rules [substitute]` — the retro-filter | 6, 8 |
| 10 | `[syllable] [repair] [stress] [post-stress]` | 9 |
| 11 | `[respell]` — editorial Old Irish orthography | 10 |
| 12 | Lookup stage, flags, `oldirish.run_entry_oi` | 2, 7, 11 |
| 13 | `[mutations]` as grapheme operations | 12 |
| 14 | `[inflect]` as grapheme operations + the stem dispatch | 13 |
| 15 | `[templates]`, the Old Irish builder, its own `ART`, the function registry | 14 |
| 16 | Filter regression + ratchet | 4, 15 |
| 17 | CLI exposure (`--strand old-irish`) | 15 |
| 18 | Gallery column, snapshot, property checks | 16, 17 |

**Serialisation, stated in full (R33, GPT #5).**

- `rules/old-irish.rules` is edited by Tasks **8 → 9 → 10 → 11 → 13 → 14 → 15**, and the dependency
  chain above makes that order total: 9 depends on 8, 10 on 9, 11 on 10, 12 on 11, 13 on 12, 14 on
  13, 15 on 14. **No two of them may run concurrently.**
- `src/strands/oldirish.py` is created by Task **12** and extended by **13, 14, 15, 16** — the same
  chain, so it is serialised too. Draft 1's cycle (Task 15 editing a file Task 12 creates while
  Task 13 also edits it) is gone.
- `src/strands/check.py` is edited by Tasks **2, 6, 7 and 14**, and the dependency table now
  **serialises them: 2 → 6 → 7 → 14.** Task 6 depends on Task 2 and Task 7 depends on Task 6 *for
  this reason and no other* — the four additions are in different functions
  (`check_lexicon_file`, `Checker.item`, `check_grapheme_table`, `Checker.grapheme_rules`) and would
  merge mechanically, but draft 2's "expect a mechanical merge" left two tasks free to run
  concurrently on one file, which is not a dependency graph. If an executor prefers concurrency
  over the ordering, the sanctioned alternative is to **split the checks into disjoint modules**
  (`check_lexicon.py`, `check_orth.py`, `check_graphemes.py`, each exporting a function
  `check.py` re-exports); take that route explicitly or take the ordering, not neither.
- `src/strands/dsl.py` is edited by Tasks **6** and **15**; they are ordered by the chain.

**Parallelism.** Tasks **1, 2 and 5** are fully independent and may run at once. Then **3** (needs
2) and **6** (needs 5 and 2) in parallel, then **7** (needs 1 and 6). Then the long serial spine 8→9→10→11→12→13→14→15, with **4** and **17** able to run
beside it (4 after 3; 17 after 15). Only Tasks 3 and 4 need network access, and both are
extension/verification passes over an already-harvested, already-once-verified file (O-24) — but
they are per-row research jobs with live page fetches, not "small extensions": budget them
accordingly, and note that Task 3's 10% defect gate can stop the plan.

---
## Task 1: `features.tsv` hand rows for the Old Irish lenited series

**Depends on:** — . **Spec:** §4 `[inventory]`; O-1, O-2, O-3. **Review:** R26, S18.

**Files:** modify `rules/features.tsv` and `rules/features.README.md`; append to
`tests/test_features_hand.py`.

**Interfaces:** produces **seven** new tokenizable segments — `β βʲ β̃ β̃ʲ θʲ ðʲ ɣʲ` — usable from
Task 7 on. `θ ð x ɣ s f h ç j` already exist and are not touched.

| New row | Copy from | Change |
|---|---|---|
| `β` | `v` | `labiodental −`, `labial +`, `round −`; keep `continuant +`, `sonorant −`, `periodicGlottalSource +` |
| `βʲ` | `β` | `front +`, `back −`, `high +` (the I-41 slender convention) |
| `β̃` | `β` | `nasal +` |
| `β̃ʲ` | `βʲ` | `nasal +` |
| `θʲ` | `θ` | `front +`, `back −`, `high +` |
| `ðʲ` | `ð` | `front +`, `back −`, `high +` |
| `ɣʲ` | `ɣ` | `front +`, `back −` |

**Why `ɣʲ` is a row and draft 1's "it is the existing `j`" was wrong (R26).** `j` is
`sonorant +, consonantal −, approximant +` — a glide, not the voiced velar/palatal **fricative**
digest §10.1 charts as the lenition product of /ɡʲ/. Any `[C +continuant −sonorant]` bundle over the
lenited series would silently miss it. The `/xʲ/` = `ç` identity is different and **is** exact
(`ç` and `x` differ only in `front`), so no `xʲ` row is added.

`class` = `consonant`; `source` = `hand:old-irish` for all seven (S18 — matching the existing
`hand:irish` convention; the digest reference goes in `features.README.md`).

- [ ] **Step 1: Write the failing test** — append to `tests/test_features_hand.py`:

```python
OLD_IRISH_ROWS = ("β", "βʲ", "β̃", "β̃ʲ", "θʲ", "ðʲ", "ɣʲ")


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
    assert [f for f in TABLE.features
            if TABLE.value("β", f) != TABLE.value("β̃", f)] == ["nasal"]


@pytest.mark.parametrize("broad,slender", [("β", "βʲ"), ("β̃", "β̃ʲ"), ("θ", "θʲ"),
                                           ("ð", "ðʲ"), ("ɣ", "ɣʲ"), ("x", "ç")])
def test_slender_partners_differ_only_in_the_I41_quality_features(broad, slender):
    """R26: the x/ç and ɣ/ɣʲ pairs are INCLUDED — draft 1 omitted them because `j` failed."""
    assert {f for f in TABLE.features
            if TABLE.value(broad, f) != TABLE.value(slender, f)} <= {"front", "back", "high"}


def test_j_is_not_the_slender_partner_of_gamma():
    """R26: `j` is a glide (sonorant +, consonantal −), not the fricative /ɣʲ/."""
    assert TABLE.value("j", "sonorant") == "+" and TABLE.value("ɣʲ", "sonorant") == "-"


def test_no_fortis_sonorant_rows_were_added():
    """O-2: fortis is a doubled GRAPHEME (Task 7), not a segment."""
    for bad in ("L", "N", "R", "ʟ", "ɴ", "ʀ"):
        assert bad not in TABLE.segments
```

- [ ] **Step 2:** `uv run pytest tests/test_features_hand.py -q` → FAIL (`'β' not in TABLE.segments`).
- [ ] **Step 3:** append the seven rows, copying the source row and editing only the named columns.
      Verify column counts:
      `uv run python -c "import csv,pathlib; rows=list(csv.DictReader(pathlib.Path('rules/features.tsv').open(encoding='utf-8'),delimiter='\t')); print([r['segment'] for r in rows[-7:]], len({len(r) for r in rows}))"`
- [ ] **Step 4:** append an "Old Irish lenited series (2026-08-27)" section to
      `rules/features.README.md`: per row, the source row, the features changed, the citation
      `digest §10.1 [wiki-old-irish §Consonants]`, and one sentence each recording O-1 (why `β̃`),
      O-2 (why no `L N R`) and R26 (why `ɣʲ` is a row but `xʲ` is not).
- [ ] **Step 5:** `uv run pytest -q` → 1004+ passed, 2 xfailed. A break means a new row collided
      with an existing longest-match tokenization; fix the row, not the test.
- [ ] **Step 6: Commit**

```bash
git add rules/features.tsv rules/features.README.md tests/test_features_hand.py
git commit -m "feat(features): Old Irish lenited series rows (β βʲ β̃ β̃ʲ θʲ ðʲ ɣʲ)"
```

**Acceptance:** seven segments tokenize; the six broad/slender pairs differ only in quality
features; `j` is shown not to be `ɣʲ`; no existing test changed.

---

## Task 2: Lexicon schema, reader, and `strands check` validation

**Depends on:** — . **Spec:** §3, §7, §10; O-18, O-19, O-21, O-22, O-24. **Review:** R3, R3a, R4.

**Read first:** `rules/old-irish-lexicon-log.md`. The lexicon **already exists** (299 rows). This
task writes the code that governs it. It must be green on the committed file **as committed** —
R3a measured that draft 1's rules would have made it red on 41 rows — so the pre-Task-3 gaps are
warnings, not errors.

**Files:** create `src/strands/lexicon.py`; modify `rules/old-irish-lexicon.tsv` (**header only**,
add `kind`), `src/strands/check.py`, `src/strands/cli.py`; test `tests/test_lexicon.py`.

**Interfaces:**

```python
LEXICON_COLUMNS = ("orthography", "oi_nom", "oi_gen", "stem", "gender", "status",
                   "kind", "source", "note")
STEMS    = ("o", "ā", "i", "u", "n", "dental", "velar", "r", "s", "indecl", "irregular")
GENDERS  = ("m", "f", "n")
STATUSES = ("attested", "middle", "none")
KINDS    = ("loan", "late")
FORM_STATUSES = ("attested", "middle")

@dataclass(frozen=True)
class LexEntry:
    orthography: str
    oi_nom: str = ""; oi_gen: str = ""; stem: str = ""; gender: str = ""
    status: str = "attested"; kind: str = ""; source: str = ""; note: str = ""
    line: int = 0
    @property
    def flag(self) -> str: ...
        # attested -> "ATTESTED"; middle -> "ATTESTED:MIr";
        # none+loan -> "RETRO:loan"; none+late -> "RETRO:late"; none+"" -> "RETRO"

class LexiconError(Exception): ...
def key(text: str) -> str                      # NFC + strip + casefold (O-19)
def read_rows(path=None) -> tuple[list[str], list[LexEntry]]
def read_lexicon(path=None) -> dict[str, LexEntry]
def validate(header, entries, path) -> list[CheckError]
def default_lexicon_path() -> Path
```

`check.check_lexicon_file(path)` reads and validates, reusing the existing `CheckError`
(`line`, `code`, `message`, `severity`).

**Validation codes.**

| Code | Severity | Condition |
|---|---|---|
| `LEX_HEADER` | error | header ≠ `LEXICON_COLUMNS` |
| `LEX_NO_KEY` | error | empty `orthography` |
| `LEX_DUPLICATE_KEY` | error | two rows with the same `key(orthography)` |
| `LEX_STATUS` | error | `status` ∉ `STATUSES` |
| `LEX_NO_SOURCE` | error | empty `source` (every row, spec §3) |
| `LEX_SOURCE_SHAPE` | error | `source` matches none of `^https?://`, `^digest §10\.\d+`, `^strachan1909 p\.\d+`, `^pokorny1914 p\.\d+` |
| `LEX_ATTESTED_NO_NOM` | error | `status` ∈ `FORM_STATUSES` and empty `oi_nom` |
| `LEX_STEM` | error | `stem` non-empty and ∉ `STEMS` |
| `LEX_GENDER` | error | `gender` non-empty and ∉ `GENDERS` |
| `LEX_KIND_ON_FORM_ROW` | error | `status` ∈ `FORM_STATUSES` and `kind` non-empty |
| `LEX_NONE_HAS_FORM` | **warning until Task 3** | `status = none` and any of `oi_nom`/`oi_gen`/`stem`/`gender` non-empty |
| `LEX_NONE_NO_KIND` | **warning until Task 3** | `status = none` and `kind` ∉ `KINDS` |
| `LEX_IRREGULAR_NO_GEN` | **warning until Task 3** | `stem = irregular` and empty `oi_gen` |
| `LEX_NEEDS_TASK3` | warning | `status` ∈ `FORM_STATUSES` and (`stem` empty **or** `stem = irregular` **or** `gender` empty) |

**Why the three middle rows are warnings, measured (R3a).** On the committed file today,
`LEX_NONE_NO_KIND` fires on **29** rows (the `kind` column does not exist yet), `LEX_IRREGULAR_NO_GEN`
on **11** (*Cú Chonnacht, Dubh-dá-leithe, Fear Diad, gasúr, Giolla, Giolla Pádraig, Giolla Íosa,
Maol Coluim, Maol Muire, Maol Seachlainn, Muircheartach*) and `LEX_NONE_HAS_FORM` on **1**
(*gasúr* is `none` **and** `stem = irregular`). Making them errors would make Task 2's own "the
committed lexicon has no errors" test false. **Task 3 promotes all three to `error`** as the last
step of closing them — that promotion is Task 3's acceptance criterion, and it is written into this
table so nobody has to rediscover it. Ten of the eleven `irregular`-without-genitive rows are
multi-word formation names, which Task 3 is told about explicitly.

**Row counts are lower bounds, not equalities (R4).** Task 3 may remove rows and Task 4 adds
10–20, so this task asserts `>=`, and Tasks 3 and 4 own their own exact counts.

- [ ] **Step 1: Write the failing tests** — `tests/test_lexicon.py`:

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


def codes(path, severity="error"):
    return sorted(e.code for e in check_lexicon_file(path)
                  if severity is None or e.severity == severity)


def test_the_column_list_is_the_spec_3_plus_10_schema():
    assert LEXICON_COLUMNS == ("orthography", "oi_nom", "oi_gen", "stem", "gender",
                               "status", "kind", "source", "note")
    assert STEMS == ("o", "ā", "i", "u", "n", "dental", "velar", "r", "s", "indecl",
                     "irregular")
    assert STATUSES == ("attested", "middle", "none") and KINDS == ("loan", "late")
    assert FORM_STATUSES == ("attested", "middle")


def test_the_four_row_shapes_all_validate(tmp_path):
    assert codes(write(tmp_path, row(**ATTESTED), row(**LOAN), row(**LATE), row(**MIDDLE))) == []


@pytest.mark.parametrize("fields,expected", [
    (ATTESTED, "ATTESTED"), (MIDDLE, "ATTESTED:MIr"),
    (LOAN, "RETRO:loan"), (LATE, "RETRO:late"),
])
def test_each_status_maps_to_its_result_flag(fields, expected):
    """spec §2 and §10; O-18, O-22. Task 12 reads exactly this property."""
    assert LexEntry(**fields).flag == expected


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
        assert codes(write(tmp_path, row(**dict(ATTESTED, source=good)))) == []


def test_a_form_bearing_row_needs_a_form(tmp_path):
    for fields in (ATTESTED, MIDDLE):
        assert "LEX_ATTESTED_NO_NOM" in codes(write(tmp_path, row(**dict(fields, oi_nom=""))))


def test_kind_is_meaningless_on_a_form_bearing_row(tmp_path):
    assert "LEX_KIND_ON_FORM_ROW" in codes(write(tmp_path, row(**dict(ATTESTED, kind="loan"))))


def test_the_widened_stem_vocabulary_is_accepted(tmp_path):
    """spec §10: velar (*rí ~ ríg*), r (*athair*), s (*tech*), indecl."""
    for stem in ("velar", "r", "s", "indecl"):
        assert codes(write(tmp_path, row(**dict(ATTESTED, stem=stem)))) == []
    assert "LEX_STEM" in codes(write(tmp_path, row(**dict(ATTESTED, stem="io"))))


@pytest.mark.parametrize("bad,code", [
    (dict(LOAN, kind=""), "LEX_NONE_NO_KIND"),
    (dict(LOAN, oi_nom="Seán"), "LEX_NONE_HAS_FORM"),
    (dict(ATTESTED, stem="irregular", oi_gen=""), "LEX_IRREGULAR_NO_GEN"),
])
def test_the_three_task3_gaps_are_warnings_for_now(tmp_path, bad, code):
    """R3a: measured on the committed file these fire on 29, 1 and 11 rows. Task 3 closes
    them and promotes all three to `error`."""
    path = write(tmp_path, row(**bad))
    assert codes(path) == []
    assert code in codes(path, severity="warning")


def test_a_row_task3_still_owes_a_stem_or_gender_is_a_warning(tmp_path):
    path = write(tmp_path, row(**dict(ATTESTED, stem="")))
    assert codes(path) == [] and "LEX_NEEDS_TASK3" in codes(path, severity="warning")


def test_a_wrong_header_is_reported_not_guessed(tmp_path):
    path = tmp_path / "lex.tsv"
    path.write_text("orthography\toi_nom\n", encoding="utf-8")
    assert "LEX_HEADER" in codes(path)


# ---- the committed file (lower bounds only, R4) -------------------------------------------

PATH = default_lexicon_path()
FILE_HEADER, FILE_ROWS = read_rows(PATH)


def test_the_committed_lexicon_has_no_errors():
    assert [e for e in check_lexicon_file(PATH) if e.severity == "error"] == []


def test_the_committed_lexicon_is_the_harvested_one():
    """Lower bounds: Task 3 may remove rows and Task 4 adds them (R4)."""
    assert len(FILE_ROWS) >= 290
    assert sum(r.status in FORM_STATUSES for r in FILE_ROWS) >= 260
    assert sum(r.status == "none" for r in FILE_ROWS) >= 25
    assert sum(bool(r.oi_gen) for r in FILE_ROWS) >= 160
    assert len({key(r.orthography) for r in FILE_ROWS}) == len(FILE_ROWS)   # O-19: no dups


def test_the_task3_backlog_is_visible_and_counted():
    codes_seen = {e.code for e in check_lexicon_file(PATH) if e.severity == "warning"}
    assert {"LEX_NEEDS_TASK3", "LEX_NONE_NO_KIND"} <= codes_seen
```

Append to `tests/test_cli.py`:

```python
def test_check_accepts_a_lexicon_tsv():
    from strands.cli import main
    assert main(["check", str(ROOT / "rules" / "old-irish-lexicon.tsv")]) == 0
```

- [ ] **Step 2:** `uv run pytest tests/test_lexicon.py -q` → FAIL (`No module named 'strands.lexicon'`).
- [ ] **Step 3:** write `src/strands/lexicon.py`. Module docstring: what the file is; that
      `orthography` is always the CITATION form and lookup never de-mutates (O-23); that every row
      cites a page; and that the four `LEX_*` warnings are a **data backlog owned by Task 3**, which
      promotes three of them to errors when it closes them.
- [ ] **Step 4:** add `check_lexicon_file` to `check.py`; in `cli.py`, route a `.tsv` argument of
      `check` to it and exit 1 only on `severity == "error"`. (Confirm the existing handler does not
      already fail on warnings; the four target rule files emit none, so nothing changes for them.)
- [ ] **Step 5:** add the `kind` column to the committed lexicon, **header plus one empty field per
      row**, changing nothing else:

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

- [ ] **Step 6:** `uv run strands check rules/old-irish-lexicon.tsv` → warnings listed, **exit 0**;
      `uv run pytest -q` → 1004+ passed, 2 xfailed.
- [ ] **Step 7: Commit**

```bash
git add src/strands/lexicon.py src/strands/check.py src/strands/cli.py \
        rules/old-irish-lexicon.tsv tests/test_lexicon.py tests/test_cli.py
git commit -m "feat(lexicon): schema, reader and check validation; kind column for RETRO:loan/late"
```

**Acceptance:** the committed 299-row lexicon has **zero error findings** and a visible warning
backlog; all four row shapes validate and map to their flags; `strands check` accepts a `.tsv`.

---

## Task 3: Lexicon fix-up — stem classes, `kind` values, and both verification files

**Depends on:** Task 2. **Spec:** §7, §10; O-18, O-21, O-33. **Needs network access.**
**Review:** R3, R3a, R31b, S4, S23, and R29's lexicon re-check items.

**Read first:** `rules/old-irish-lexicon-log.md` — findings 5, 6, 7 and the "Sample verification"
section. **Execute this with a different agent than the one that harvested the lexicon.** It is a
per-row research job with live page fetches, not a small edit; budget it as such, and note that
its 10% defect gate can stop the plan.

**Files:** modify `rules/old-irish-lexicon.tsv`, `rules/old-irish-lexicon-log.md`,
`src/strands/lexicon.py`; create `rules/old-irish-lexicon.verification.tsv` and
`rules/old-irish-lexicon.verification2.tsv`; test `tests/test_lexicon_data.py`.

**Part A — reclassify the 37 `irregular` rows** (log finding 5; O-21). Spec §10 gave `velar`, `r`,
`s`, `indecl` their own slots. Read each row's `note` — the harvest recorded the true class there —
set `stem`, and leave `irregular` only where the paradigm is genuinely suppletive. These must all
end up classified, because Task 14's tests are written against them: *teach ~ tech* (s),
*sliabh ~ slíab* (s), *athair*, *bráthair*, *máthair* (r), *rí ~ ríg*, *Lughaidh ~ Luigdech*,
*Eochaidh ~ Echach* (velar), *Pádraig ~ Patraic* (**indecl — R31b**, digest §10.5 lists *Patraic*
explicitly among the indeclinables and today the row has a blank `stem`, so Task 14 would otherwise
*derive* a genitive for it inside the `GILLA` test), *Da Derga* (indecl).

**Ten of the eleven `irregular`-without-genitive rows are multi-word formation names** (*Máel
Coluim*, *Máel Muire*, *Máel Sechnaill*, *Gilla Pátraic*, *Gilla Íosa*, *Fer Diad*, *Cú Chonnacht*,
*Dub dá Leithe*, *Giolla*, *Muircheartach*). A whole-name row is not a paradigm: give them
`stem = indecl` with a note saying the row is a fixed formation, **and** make sure the *element*
rows they are built from exist (Part D).

**Part B — the blank-stem and blank-gender rows.** Measured: 91 blank `stem` (63 of them
`attested`), 97 blank `gender`. Most are adjectives, numerals and prefixes with no nominal
paradigm. Do **not** invent classes. Record the reason in `note` using exactly one of
`no nominal paradigm: adjective` / `: numeral` / `: prefix` / `: phrase`, then extend
`LEX_NEEDS_TASK3` to skip a row whose `note` starts `no nominal paradigm:` — a one-line change in
`lexicon.validate`, and it belongs here because only this task knows the rows are genuinely exempt.
Rows that *are* nouns and simply lack data get their stem and gender from Part E, or keep the
warning. **Note O-33:** a blank `stem` on an `attested` row is no longer silent at runtime — Task 14
routes it through `infer_stem` and tags it — so a row left blank here degrades gracefully.

**Part C — re-check the `kind` split** (S4). The log's 12 `loan` / 17 `late` split is the starting
point, not the answer: *spraoi* ("borrowed directly from Old Norse") and *gasúr* ("loanword… post-OI
borrowing") are classed `late` while their own notes call them loans. Read all 29 notes and classify
from the note, not from the log's table. Also fix *gasúr*'s `stem = irregular` (it is a `none` row
and must carry no form).

**Part D — the formation elements** (R31, R31a, S23). Task 15's formation templates must be
testable against *real element rows*, and three are missing: **`Culann`, `Diad` and `Leithe` are not
in the lexicon at all**, so draft 1's parametrized cases would have skipped. Add them if a citation
can be found (they are attested in the same sources as *Cú Chulainn*, *Fer Diad*,
*Dub dá Leithe*); if not, say so in the log and Task 15 drops those cases. Also:
- **Fill in the *Nessa* row** (S23): it is *Conchobar mac Nessa*'s genitive and currently has an
  empty `stem` and no `oi_gen`. *Nessa* is an ā-stem, gen. *Nessa*.
- **`COLOUR` cannot produce *Dub-dá-leithe*** (R31a): that is three elements. Ensure a genuine
  two-element colour compound is present and cited (*Dubthach*, *Donnchad*) so Task 15 has a real
  target. Note the *Find-* / *Finn* spelling split (spec §5 and the digest write *Find-*, the
  lexicon's `Fionn` row gives *Finn*).
- Pick **one** spelling for *Patraic* / *Pátraic* across lexicon, digest and tests (R31b), and
  record the choice in the log.

**Part E — the second verification pass.** Sample **≥30 rows from the 136 with a blank `oi_gen`**,
plus every row touched in Parts A–D whose class was not already stated in its `note`. Open `source`;
confirm `oi_nom`; take the genitive and stem class from the page's inflection table. Also
re-check the ā-stem group *adarc → adarcae*, *ferg → fergae*, *long → lungae* (R29): a bare ⟨-ae⟩
with no palatalization does not fit the *túath/túaithe* paradigm and may be a data error.

**Part F — back-fill the first pass** (R3). `rules/old-irish-lexicon.verification.tsv` does **not**
exist; the first 35-row pass is a prose table in the log. Transcribe it into a TSV with the same
header as the second pass so the two are comparable.

Both files: header `orthography  source  field  verdict  checked_by  note`; `verdict` ∈
`ok | fixed | removed`.

**The gate:** if more than 10% of the second-pass sample is `fixed` or `removed`, report it and
**stop** — the genitive-less rows are then not reliable enough for Task 14's tests to lean on.

**Last step: promote the three warnings to errors** in `lexicon.validate` — `LEX_NONE_NO_KIND`,
`LEX_NONE_HAS_FORM`, `LEX_IRREGULAR_NO_GEN` — and delete Task 2's
`test_the_task3_backlog_is_visible_and_counted` (it was a Task 2 acceptance probe; say so in the
commit message).

- [ ] **Step 1: Write the failing tests** — `tests/test_lexicon_data.py`:

```python
"""Task 3: the lexicon as data after the fix-up (spec §7, §10; O-18, O-21, O-33)."""
import csv

import pytest

from helpers import ROOT, read_test_words
from strands.check import check_lexicon_file
from strands.lexicon import FORM_STATUSES, KINDS, STEMS, key, read_lexicon, read_rows

PATH = ROOT / "rules" / "old-irish-lexicon.tsv"
HEADER, ROWS = read_rows(PATH)
LEX = read_lexicon(PATH)
FORMS = [r for r in ROWS if r.status in FORM_STATUSES]
NONE_ROWS = [r for r in ROWS if r.status == "none"]
EXEMPT = "no nominal paradigm:"
VERIF_COLUMNS = ("orthography", "source", "field", "verdict", "checked_by", "note")


def verification(name):
    with (ROOT / "rules" / name).open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh, delimiter="\t")
        return list(reader.fieldnames or []), list(reader)


def test_the_lexicon_is_completely_clean():
    """After this task there are no findings at all, not even warnings."""
    assert check_lexicon_file(PATH) == []


def test_the_three_task2_warnings_are_now_errors():
    """The promotion IS this task's acceptance criterion (R3a)."""
    from strands.lexicon import LEXICON_COLUMNS, validate, LexEntry
    bad = LexEntry(orthography="x", status="none", source="https://e.x", line=2)
    codes = {(e.code, e.severity) for e in validate(list(LEXICON_COLUMNS), [bad], "t")}
    assert ("LEX_NONE_NO_KIND", "error") in codes


def test_the_irregular_placeholder_is_now_reserved_for_suppletion():
    """Log finding 5: 37 rows wore `irregular` for four different paradigms."""
    left = [r.orthography for r in FORMS if r.stem == "irregular"]
    assert len(left) <= 10, left


@pytest.mark.parametrize("headword,stem", [
    ("teach", "s"), ("sliabh", "s"), ("athair", "r"), ("máthair", "r"), ("bráthair", "r"),
    ("rí", "velar"), ("Lughaidh", "velar"), ("Eochaidh", "velar"), ("Pádraig", "indecl"),
])
def test_the_paradigm_words_the_inflection_tests_need_are_classified(headword, stem):
    row = LEX.get(key(headword))
    assert row is not None, headword
    assert row.stem == stem, (headword, row.stem)


def test_every_remaining_backlog_row_says_why_it_has_no_paradigm():
    backlog = [r for r in FORMS if (not r.stem or not r.gender)
               and not r.note.startswith(EXEMPT)]
    assert backlog == [], [(r.orthography, r.stem, r.gender) for r in backlog]


def test_every_none_row_is_classified_loan_or_late():
    """O-18 / S4: classified from the row's own note, not from the log's table."""
    assert all(r.kind in KINDS for r in NONE_ROWS)
    assert all(not (r.oi_nom or r.oi_gen or r.stem or r.gender) for r in NONE_ROWS)


def test_the_formation_elements_task15_needs_exist():
    """R31: draft 1's formation tests skipped because these were absent."""
    for element in ("Maol", "Giolla", "cú", "fear", "mac", "inion", "Colm", "Pádraig"):
        assert key(element) in LEX, element


def test_the_nessa_row_is_complete():
    """S23: *Conchobar mac Nessa* is the digest's own example and must be reproducible."""
    row = LEX[key("Neasa")] if key("Neasa") in LEX else LEX[key("Nessa")]
    assert row.stem and row.oi_gen


def test_old_irish_forms_carry_no_modern_lenition_digraphs():
    """digest §10.2 conv. 1 / log finding 3."""
    bad = [(r.orthography, r.oi_nom) for r in FORMS
           if any(d in r.oi_nom.lower() for d in ("bh", "dh", "gh", "mh"))]
    assert bad == [], bad


def test_the_measured_regression_overlap_is_intact():
    """O-31: 54 form-bearing keys also in test-words.tsv with hand IPA."""
    keys = {key(r["orthography"]) for r in read_test_words() if r["ipa"]}
    overlap = {k for k in keys & set(LEX) if LEX[k].status in FORM_STATUSES}
    assert len(overlap) >= 54, len(overlap)


@pytest.mark.parametrize("name", ["old-irish-lexicon.verification.tsv",
                                  "old-irish-lexicon.verification2.tsv"])
def test_both_verification_files_exist_with_the_agreed_schema(name):
    """R3: the first pass was prose in the log; this task back-fills it."""
    header, rows = verification(name)
    assert tuple(header) == VERIF_COLUMNS
    assert len(rows) >= 30, (name, len(rows))


def test_every_verdict_is_explained_and_attributed():
    for name in ("old-irish-lexicon.verification.tsv", "old-irish-lexicon.verification2.tsv"):
        for r in verification(name)[1]:
            assert r["verdict"] in ("ok", "fixed", "removed"), r
            assert r["checked_by"].strip(), r
            if r["verdict"] != "ok":
                assert r["note"].strip(), (name, r["orthography"])


def test_the_second_pass_defect_rate_admits_the_genitive_less_rows():
    rows = verification("old-irish-lexicon.verification2.tsv")[1]
    defects = sum(r["verdict"] != "ok" for r in rows)
    assert defects <= len(rows) // 10, (defects, len(rows))


def test_removed_rows_are_gone_and_kept_rows_are_present():
    for r in verification("old-irish-lexicon.verification2.tsv")[1]:
        assert (key(r["orthography"]) in LEX) != (r["verdict"] == "removed"), r["orthography"]
```

- [ ] **Step 2:** `uv run pytest tests/test_lexicon_data.py -q` → FAIL (no verification files; the
      paradigm words are still `irregular`).
- [ ] **Step 3–7:** Parts A–F in order, then the warning promotion. List the work first so it is
      auditable:
      `uv run python -c "from strands.lexicon import read_rows; [print(r.line, r.orthography, '|', r.oi_nom, '|', r.oi_gen, '|', r.stem, '|', r.note) for r in read_rows()[1] if r.stem=='irregular' or not r.stem]"`
- [ ] **Step 8:** append a "Second pass (Task 3)" section to the log: how many rows were
      reclassified into each new stem value, how many annotated exempt, the `kind` re-classification
      deltas, the verification counts, and any row removed.
- [ ] **Step 9:** `uv run strands check rules/old-irish-lexicon.tsv` → **no findings**;
      `uv run pytest -q` → green.
- [ ] **Step 10: Commit**

```bash
git add rules/old-irish-lexicon.tsv rules/old-irish-lexicon-log.md \
        rules/old-irish-lexicon.verification.tsv rules/old-irish-lexicon.verification2.tsv \
        src/strands/lexicon.py tests/test_lexicon_data.py tests/test_lexicon.py
git commit -m "data(lexicon): reclassify stems, classify none-rows by kind, add formation elements, second verification pass

Promotes LEX_NONE_NO_KIND, LEX_NONE_HAS_FORM and LEX_IRREGULAR_NO_GEN from warning to error
and drops Task 2's backlog-visibility probe, which they replace."
```

**Acceptance:** `strands check` is silent on the lexicon; ≤10 rows still `irregular`; the nine named
paradigm words carry their real class; every remaining blank explains itself; all 29 `none` rows
carry a re-checked `kind`; the formation elements exist; both verification files have ≥30 rows with
≤10% defects in the second; the regression overlap is still ≥54.

---

## Task 4: Middle Irish tier — the 49 unresolved names

**Depends on:** Task 3. **Spec:** §10, §11; O-22. **Needs network access.** **Review:** R4.

**Read first:** the "Unresolved" section of `rules/old-irish-lexicon-log.md` — 49 headwords
harvested and left out, each with a reason. The log's own diagnosis is "Middle Irish attestation
without an Old Irish one", and it names two honest routes, one of which — "an explicit policy
decision to admit Middle Irish forms as fallback ancestors with a distinct status value" — spec §10
has now taken.

**Files:** modify `rules/old-irish-lexicon.tsv` and `rules/old-irish-lexicon-log.md`; append to
`tests/test_lexicon_data.py`.

**Procedure, per unresolved headword:**

1. **Write a `middle` row** when the log's reason already names a Middle Irish form — *Eoghan ~
   Eógan*, *Tadhg ~ Tadg*, *Méabh ~ Medb*, *Oisín ~ oisín*, *bealach ~ belach*, *saoi ~ suí*,
   *dualgas ~ dúalgas*, *sméar ~ smér*, *gaiscíoch* — with `source` = the page showing it and
   `note` = "Middle Irish only; no Old Irish attestation found (harvest log, unresolved)".
   *Órla*, *Gráinne* and *Úna* need a **fresh check** for a Middle Irish form the first pass did not
   record; write them only if one is found.
2. **Leave out** any headword whose reason is "no page found", "fetch failed", "not checked within
   budget" or "no Etymology section". Nothing has changed for them.
3. **Never write a reconstructed form.** A source printing only an asterisked form (*\*gruac*,
   *\*gelach*) has attested nothing; those stay out. This is what keeps `ATTESTED:MIr` meaning
   "attested, in Middle Irish".
4. Stem class and gender from the Middle Irish entry's inflection table where it has one, else the
   Task 3 Part B exemption convention.

Expect roughly 10–20 rows. **The number is not a target.**

- [ ] **Step 1: Write the failing tests** — append:

```python
MIDDLE = [r for r in ROWS if r.status == "middle"]


def test_the_middle_irish_tier_is_populated():
    """spec §10: the important names should not be left to the filter."""
    assert len(MIDDLE) >= 8, len(MIDDLE)


@pytest.mark.parametrize("headword", ["Eoghan", "Tadhg", "Oisín"])
def test_the_named_middle_irish_names_are_now_covered(headword):
    row = LEX.get(key(headword))
    assert row is not None and row.status == "middle", headword
    assert row.oi_nom, headword


def test_every_middle_row_flags_ATTESTED_MIr():
    """O-22: the tier shows up in the flag and nowhere else."""
    assert all(r.flag == "ATTESTED:MIr" for r in MIDDLE)


def test_no_middle_row_records_a_reconstructed_form():
    assert [r.orthography for r in MIDDLE if "*" in r.oi_nom or "*" in r.oi_gen] == []


def test_every_middle_row_says_it_is_middle_irish_only():
    assert all("middle irish" in r.note.lower() for r in MIDDLE)


def test_the_middle_tier_only_added_rows():
    """R4: a `middle` row is a NEW row, never a reclassified `attested` one."""
    assert sum(r.status == "attested" for r in ROWS) >= 265


def test_the_lexicon_is_still_clean_and_within_its_size_bound():
    assert check_lexicon_file(PATH) == []
    assert len(ROWS) <= 330
```

- [ ] **Step 2:** `uv run pytest tests/test_lexicon_data.py -q` → FAIL (no `middle` rows).
- [ ] **Step 3:** work the 49; write the rows; append a "Middle Irish tier (Task 4)" section to the
      log recording how many were revisited, how many written, and which stay unresolved with the
      unchanged reason.
- [ ] **Step 4:** `uv run strands check rules/old-irish-lexicon.tsv` → silent; `uv run pytest -q` → green.
- [ ] **Step 5: Commit**

```bash
git add rules/old-irish-lexicon.tsv rules/old-irish-lexicon-log.md tests/test_lexicon_data.py
git commit -m "data(lexicon): Middle Irish tier — N rows for names attested only in Middle Irish"
```

**Acceptance:** ≥8 `middle` rows including *Eoghan*, *Tadhg*, *Oisín*; each flags `ATTESTED:MIr`,
cites a page showing an unasterisked form, and says in its note that it is Middle Irish only; the
`attested` rows are untouched; `strands check` silent.

---
## Task 5: Orthography↔IPA aligner and the `Word.orth` channel

**Depends on:** — . **Spec:** §4, §11 (positional tags, measured per-class coverage). O-6, O-7.
**Review:** R5, R6, R7, R8, R10, S1, S2, S3.

**Files:** create `src/strands/orth.py` and `rules/irish-orthography.tsv`; modify
`src/strands/word.py` and `src/strands/irish.py`; test `tests/test_orth_align.py`.

**Interfaces:**

```python
ORTH_TABLE_PATH: Path
class OrthError(Exception): ...
Table = tuple[tuple[str, tuple[tuple[str, ...], ...]], ...]   # (unit, alternatives), longest first

def load_orth_table(path=None) -> Table
def align(orthography: str, segments: Sequence[str], table: Table | None = None) -> tuple[str, ...]
def tag_word(word: Word, orthography: str) -> Word
```

`Word` gains `orth: tuple[str, ...] = ()` and `tag_at(i) -> str`. **Invariant:** `orth` is empty or
exactly `len(segments)` long.

**Positional tags (O-6, spec §11).** A unit consuming **one** segment tags it `unit`. A unit
consuming **n > 1** segments tags them `unit:1` … `unit:n`. So *Niamh* /nʲiəw/ tags
`("n", "ia:1", "ia:2", "mh")` — draft 1 gave both halves the identical tag, which made R12's
"first element only" inexpressible and forced S1's phonological-context workaround. A rule may now
target either element or claim the whole unit with a two-item target.

**The algorithm** (O-7). Clean the orthography: NFC, casefold, delete `-`, `'`, `’` and spaces. DFS
over nodes `(i, j)` = (characters consumed, segments consumed) from `(0,0)` to
`(len(o), len(segs))`; from a node, for each table row in sorted order whose unit matches at `i`,
and each alternative in file order, if `segments[j:j+len(alt)] == alt`, recurse. Memoize dead nodes.
**The first complete path wins**, so the result is a deterministic function of the table's order.
Failure is total: `("",) * len(segs)`, never partial, never an exception.

**Measured coverage (spec §11 requires the number, not a threshold).** The table below was executed
against all **144** rows of `sources/irish/test-words.tsv` that carry IPA (all of them; 0
untokenizable), after `tokenize` + `irish.normalize`:

| class | aligned/total | % |
|---|---|---|
| **overall** | **144/144** | **100.0** |
| ao | 9/9 | 100.0 |
| quality-digraph (⟨ea io ai oi ui⟩) | 62/62 | 100.0 |
| lenition-digraph (⟨bh dh gh mh⟩) | 36/36 | 100.0 |
| ch-th | 28/28 | 100.0 |
| ua-ia | 11/11 | 100.0 |
| final-vowel | 25/25 | 100.0 |
| an-suffix | 6/6 | 100.0 |
| epenthesis | 24/24 | 100.0 |
| eclipsis | 10/10 | 100.0 |

Draft 1's table measured **95/144 = 66.0%** with the failure classes R5 named — epenthesis 14,
eclipsis digraphs 10, doubled letters 7, missing units/values ~18. **These are the rows that close
the gap; write them, do not re-derive them.** Determinism was verified across three
`PYTHONHASHSEED` values (byte-identical output). **14 of the 144 words require backtracking**
(*Colm, Sorcha, leanbh ×2, dearg, gorm, dorcha, ainm, long, gealbhan, dhearg, borb, fearg,
seirbhís*), so the memo must prune only and never decide.

**`rules/irish-orthography.tsv`** — header `unit  segments  note`; `segments` is a space-separated
list of alternatives, each `+`-joined, `-` = silent. Write these rows in this order (the loader
sorts by unit length; file order is the tie-break within a length and is load-bearing):

```
bhf   vˠ vʲ w          # eclipsis of f (digest §3.2) — *bhfreagra* /vʲɾʲaɡɾˠə/
tsn   tʲ+ɾʲ t̪ˠ+ɾˠ      # t-prefix + the Connacht sn->sr shift — *an tsneachta*
mb    mˠ mʲ            # eclipsis REPLACES: *mbean* /mʲanˠ/, not /mb/ (digest §3.2)
gc    ɡ ɟ              # *gceann* /ɟaːn̪ˠ/
nd    n̪ˠ nʲ            # *ndroim* /n̪ˠɾˠiːmʲ/
bp    bˠ bʲ            # *bpeann* /bʲaːn̪ˠ/
dt    d̪ˠ dʲ            # *dteach* /dʲax/
ng    ŋ ɲ ŋ+ɡ          # eclipsed /ŋ ɲ/; the third alt is word-final ⟨ng⟩ — *long* /l̪ˠuːŋɡ/
ts    t̪ˠ tʲ            # the t-prefix — *an tsúil*, *an tsaoil* (digest §3.3)
cn    k+ɾˠ c+ɾʲ        # Connacht cn->cr — *cnoc* /kɾˠʊk/ (digest §2.2); *cnaipe* /knˠapʲə/
                       # keeps /kn/ and aligns by the plain c+n path
mn    mˠ+ɾˠ mʲ+ɾʲ      # Connacht mn->mr — *mná* /mˠɾˠaː/
eabh  ə+u              # digest §5.3 vowel+lenition
eadh  ə+i ə aː
adh   ə+i ə aː
agh   ə+i aː
abh   ə+u aː
amh   ə+u aː ũː
bh    w vˠ vʲ          # digest §5.3 lenition digraphs
mh    w vˠ vʲ
dh    ɣ j -            # the silent alt is needed by *Eoghan* /oːənˠ/
gh    ɣ j -
th    h -
sh    h ç
ch    x ç
ph    fˠ fʲ
fh    -
aoi   iː               # digest §5.1
ao    iː eː
eoi   oː
eái   aː
eá    aː
iá    iə
ái    aː
aí    iː
oí    iː
uí    iː
ia    iə i+ə
ua    uə u+ə
ae    eː
eo    oː ɔ
ío    iː               # S3: the ACCENTED spellings the corpus actually has (*stríoc*)
iú    uː               # S3 (*ciúin*, *leisciúil*)
ei    ɛ eː
ea    a aː ɑ æ         # æ: *Ard-Easpag*
io    ɪ iː ʊ           # ʊ: *Siobhán*, *fionn*
iu    ʊ uː
oi    ɔ ɪ iː           # iː: *droim*
ui    ɪ ʊ
ai    a aː ə ɪ         # R10: draft 1 had NO `ai` row, so every ⟨ai⟩ tagged as `a`
nn    n̪ˠ nʲ            # doubled letters — one modern segment, but the right TAG
ll    l̪ˠ lʲ
rr    ɾˠ ɾʲ
mm    mˠ mʲ
á     aː
é     eː
í     iː
ó     oː õː            # õː: *ardnósach*
ú     uː
a     a aː ə ɑ -       # the `-` alternative is the caol-le-caol glide vowel (13 uses)
e     ɛ eː ə -
i     ɪ iː ə i -       # 13 uses of the glide
o     ɔ oː o ʊ uː ə -
u     ʊ uː ə u -
b     bˠ bʲ
c     k c
d     d̪ˠ dʲ
f     fˠ fʲ
g     ɡ ɟ
h     h -
l     l̪ˠ lʲ l̪ˠ+ə lʲ+ə  # the +ə alternatives are digest §2.4 epenthesis — *Colm* /ˈkɔl̪ˠəmˠ/
m     mˠ mʲ mˠ+ə mʲ+ə
n     n̪ˠ nʲ ŋ ɲ n̪ˠ+ə nʲ+ə -
p     pˠ pʲ
r     ɾˠ ɾʲ ɾˠ+ə ɾʲ+ə
s     sˠ ʃ
t     t̪ˠ tʲ
```

**Two rows to flag in the file's own comments.** `n`'s silent alternative fires on exactly one
corpus word (*an tsneachta*, where the article's /n/ is lost before the t-prefix) and in principle
lets the aligner swallow any ⟨n⟩; the safety margin comes only from `nn` sorting first. And `tsn`,
`cn`, `mn` encode a Connacht/Ulster nasal→liquid shift, each resting on a single corpus word.
Both are real, both are thin: say so, so a later reader can tighten them deliberately.

**`Word.orth` must survive `irish._join` (R7).** Draft 1 listed `replaced()`, `split_words()` and
`traced()` but not `_join`, which constructs `Word(...)` literally at `src/strands/irish.py:192`
(also 286, 346, 353) and therefore resets `orth` to `()` — losing the tags on every constructed
word. Rule: `_join(a, b).orth = a.orth + b.orth` when **both** sides carry the channel; when one
side is empty, **pad it with `""` to its segment length** (the only length-safe option) so the
invariant holds; when both are empty, stay empty.

- [ ] **Step 1: Write the failing tests** — `tests/test_orth_align.py`:

```python
"""Task 5: the modern-orthography <-> IPA aligner (spec §4, §11; O-6, O-7)."""
import pytest

from helpers import TABLE, irish, read_test_words, w
from strands.irish import normalize
from strands.orth import align, load_orth_table, tag_word

IRISH = irish()


def segs(ipa):
    """R6: the REAL call site normalizes first; draft 1's helper did not, so three of its
    own positive assertions returned all-empty tags."""
    return normalize(w(ipa), IRISH, TABLE).segments


def tags(orthography, ipa):
    return align(orthography, segs(ipa))


def test_the_table_is_sorted_longest_unit_first():
    lengths = [len(unit) for unit, _ in load_orth_table()]
    assert lengths == sorted(lengths, reverse=True)


# ---- pinned tags: S2's guard against an agent optimising the counter ----------------------

@pytest.mark.parametrize("orthography,ipa,expected", [
    ("Niamh",  "nʲiəvˠ",   ("n", "ia:1", "ia:2", "mh")),
    ("gorm",   "ɡɔɾˠəmˠ",  ("g", "o", "r:1", "r:2", "m")),
    ("Seán",   "ʃaːnˠ",    ("s", "eá", "n")),
    ("naomh",  "n̪ˠiːw",    ("n", "ao", "mh")),
    ("Caoimhe", "kiːvʲə",  ("c", "aoi", "mh", "e")),
    ("dubh",   "d̪ˠʊw",     ("d", "u", "bh")),
    ("sneachta", "ʃnʲaxt̪ˠə", ("s", "n", "ea", "ch", "t", "a")),
    ("baid",   "bˠaːdʲ",   ("b", "a", "d")),
    ("Colm",   "ˈkɔl̪ˠəmˠ", ("c", "o", "l:1", "l:2", "m")),
    ("mbean",  "mʲanˠ",    ("mb", "ea", "n")),
    ("bpeann", "bʲaːn̪ˠ",   ("bp", "ea", "nn")),
    ("caisleán", "kaʃlʲaːnˠ", ("c", "ai", "s", "l", "eá", "n")),
])
def test_the_pinned_tags_are_exact(orthography, ipa, expected):
    """Every one of these is a real corpus row. The multi-segment units carry POSITIONAL
    tags (O-6): the epenthetic schwa is `r:2`/`l:2`, the diphthong halves are `ia:1`/`ia:2`."""
    assert tags(orthography, ipa) == expected


@pytest.mark.parametrize("orthography,ipa,expected", [
    ("bhí", "vʲiː", ("bh", "í")),
    ("mhac", "wak", ("mh", "a", "c")),
    ("dhún", "ɣuːnˠ", ("dh", "ú", "n")),
    ("chos", "xɔsˠ", ("ch", "o", "s")),
    ("phóg", "fˠoːɡ", ("ph", "ó", "g")),
    ("shúil", "huːlʲ", ("sh", "ú", "l")),
])
def test_the_reversal_relevant_digraphs_all_align(orthography, ipa, expected):
    assert tags(orthography, ipa) == expected


def test_a_single_segment_unit_carries_no_position_suffix():
    assert ":" not in "".join(tags("gorm", "ɡɔɾˠmˠ"))


# ---- the algorithm's own properties -------------------------------------------------------

def test_backtracking_is_required_and_works():
    """Measured: 14 of 144 words need it. *long* is the minimal case — `ng -> (ŋ,)` is tried
    first and dead-ends, then `ng -> (ŋ, ɡ)` completes. The dead-node memo must PRUNE only."""
    assert tags("long", "l̪ˠuːŋɡ") == ("l", "o", "ng:1", "ng:2")


def test_alignment_is_deterministic():
    a = tags("Colm", "ˈkɔl̪ˠəmˠ")
    for _ in range(3):
        assert tags("Colm", "ˈkɔl̪ˠəmˠ") == a


def test_alignment_failure_returns_all_empty_tags_and_never_raises():
    """O-7: the tag is ABSENT, not guessed, so only sound-based rules apply."""
    assert tags("Seán", "xɔsˠ") == ("", "", "")
    assert align("", ("ɡ", "ɔ")) == ("", "")


def test_hyphens_apostrophes_and_spaces_are_ignored():
    assert tags("t-éan", "tʲeːnˠ") == ("t", "é", "n")


def test_tag_word_sets_the_channel_and_records_a_failure_in_the_trace():
    good = tag_word(w("ɡɔɾˠmˠ"), "gorm")
    assert good.orth == ("g", "o", "r", "m") and len(good.orth) == len(good.segments)
    bad = tag_word(w("ɡɔɾˠmˠ"), "Seán")
    assert bad.orth == ("", "", "", "")
    assert any(t.rule_id == "orth:unaligned" for t in bad.trace)


def test_the_orth_channel_survives_replacement_and_splitting():
    word = tag_word(w("ɡɔɾˠmˠ"), "gorm")
    assert word.replaced(0, 1, ("k",)).orth == ("g", "o", "r", "m")
    assert word.replaced(1, 2, ("ɔ", "ə")).orth == ("g", "o", "o", "r", "m")
    assert word.replaced(1, 3, ("a",)).orth == ("g", "o", "m")


def test_the_orth_channel_survives_a_join():
    """R7: `irish._join` constructs Word(...) literally and dropped the channel, losing the
    tags on every constructed word."""
    from strands.irish import _join
    a = tag_word(w("ə"), "a")
    b = tag_word(w("ʃaːnʲ"), "Sheáin")
    joined = _join(a, b)
    assert len(joined.orth) == len(joined.segments)
    assert joined.orth[0] == "a" and joined.orth[1] == "sh"
    plain = _join(w("ə"), b)
    assert plain.orth == ("",) + b.orth


def test_the_channel_is_empty_or_exactly_as_long_as_the_segments():
    assert w("ɡɔɾˠmˠ").orth == () and w("ɡɔɾˠmˠ").tag_at(0) == ""


# ---- the measured coverage (spec §11: a number, not a threshold) -------------------------

CLASSES = {
    "ao": lambda o: "ao" in o,
    "quality-digraph": lambda o: any(d in o for d in ("ea", "io", "ai", "oi", "ui")),
    "lenition-digraph": lambda o: any(d in o for d in ("bh", "dh", "gh", "mh")),
    "ch-th": lambda o: "ch" in o or "th" in o,
    "ua-ia": lambda o: "ua" in o or "ia" in o,
    "final-vowel": lambda o: o.endswith(("a", "e")),
    "an-suffix": lambda o: o.endswith("án"),
    "eclipsis": lambda o: o.startswith(("mb", "gc", "nd", "bp", "dt", "bhf", "ng")),
}
ROWS = [r for r in read_test_words() if r["ipa"]]


def test_every_test_word_aligns():
    """Measured 144/144 with the committed table. A regression here is a table regression."""
    bad = [r["orthography"] for r in ROWS
           if not any(align(r["orthography"], segs(r["ipa"])))]
    assert bad == [], bad


@pytest.mark.parametrize("name", sorted(CLASSES))
def test_every_reversal_class_aligns_completely(name):
    """spec §11: coverage is a per-class measurement."""
    pred = CLASSES[name]
    members = [r for r in ROWS if pred(r["orthography"].casefold())]
    bad = [r["orthography"] for r in members
           if not any(align(r["orthography"], segs(r["ipa"])))]
    assert members and bad == [], (name, len(members), bad)
```

- [ ] **Step 2:** `uv run pytest tests/test_orth_align.py -q` → FAIL (`No module named 'strands.orth'`).
- [ ] **Step 3:** add `orth` and `tag_at` to `Word`; thread the channel through `replaced()` (new
      segments inherit `self.orth[start]`; a zero-width insertion gets `""`) and `split_words()`
      (slice on the same bounds); `traced()` uses `replace()` and needs nothing.
- [ ] **Step 4:** fix `irish._join` per R7 above. Run `uv run pytest tests/test_irish_templates.py -q`.
- [ ] **Step 5:** write `rules/irish-orthography.tsv` exactly as given, with the two flagged
      comments.
- [ ] **Step 6:** write `src/strands/orth.py`. Docstring: why spelling is needed (spec §4), the
      algorithm and its determinism, the total-failure rule (O-7), and the positional tags (O-6).
- [ ] **Step 7:** `uv run pytest tests/test_orth_align.py -q` → PASS. **If a coverage test fails,
      the fix is a table row, never a lower threshold — and the pinned-tag tests are what stop an
      agent from "fixing" it by making every consonant silent (S2).**
- [ ] **Step 8:** `uv run pytest -q` → green. **Commit:**

```bash
git add src/strands/orth.py src/strands/word.py src/strands/irish.py \
        rules/irish-orthography.tsv tests/test_orth_align.py
git commit -m "feat(orth): modern orthography-IPA aligner with positional tags (144/144 test words)"
```

**Acceptance:** 144/144 overall and 100% in every one of the eight classes; the twelve pinned tag
tuples are exact; positional suffixes appear only on multi-segment units; backtracking works;
failure is total and silent; the channel survives `replaced`, `split_words` **and `_join`**.

---

## Task 6: The `@orth("…")` rule item

**Depends on:** Tasks 2 and 5 — Task 2 only because both edit `src/strands/check.py` and the
plan serialises that file (2 → 6 → 7 → 14) rather than leaving a merge to chance.
**Spec:** §4, §11. O-6. **Review:** R9.

**Files:** modify `src/strands/dsl.py`, `src/strands/rewrite.py`, `src/strands/check.py`; test
`tests/test_dsl_orth_atom.py`.

**Interfaces:** `ItemSpec(kind="orth", value="bh")` from `@orth("bh")`; value stored NFC +
casefolded. `match_item` gains keyword-only `word: Word | None = None, index: int | None = None`;
`kind == "orth"` returns `False` when they are absent, which is the same "no tag, no match"
behaviour as an untagged word. Every existing call site keeps working.

**Parse rules.** Legal as a whole TARGET item and as a context atom. Illegal, with these exact
`ParseError` messages: in a REPLACEMENT → `@orth() may not appear in a replacement`; with a capture
→ `@orth() may not carry a capture`; inside `{}` or `[]` → `@orth() may not appear inside {} or []`;
malformed argument → `@orth() takes one double-quoted string`.

**Check rules (R9 — draft 1's warning let dead rules through).** `ORTH_UNKNOWN_UNIT` is an
**error**, not a warning: an `@orth("X")` whose `X` is not a unit of `rules/irish-orthography.tsv`
— after stripping a `:n` positional suffix — can never match, and draft 1's combination of a
warning plus `matching_segments() == []` meant `RULE_NEVER_MATCHES` could not fire either, so
`@orth("ai")` was undetectable dead code. A positional suffix is additionally checked against the
unit's **maximum alternative length**: `@orth("ia:3")` is `ORTH_BAD_POSITION`.
`Checker.matching_segments` returns `[]` for an orth item (it matches by provenance, not phonology).

- [ ] **Step 1: Write the failing tests** — `tests/test_dsl_orth_atom.py`:

```python
"""Task 6: the @orth("…") rule item with positional tags (spec §4, §11; O-6)."""
import pytest

from helpers import TABLE, w
from strands.check import check_rule_file
from strands.dsl import ItemSpec, ParseError, parse_rules, parse_rules_file
from strands.orth import tag_word
from strands.rewrite import apply_section

PREAMBLE = """[meta]
name = orth-test
[inventory]
w vˠ vʲ ɡ ɔ ɾˠ mˠ bˠ β β̃ i ə a e
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
    assert rf('[substitute]\n@orth("BH") -> β\n').sections["substitute"][0].target[0].value == "bh"


def test_it_rewrites_only_the_segment_with_that_tag():
    """spec §4: 'spelling disambiguates what sound alone cannot'. Both are /w/."""
    assert run('@orth("bh") -> β\n', "wak", "bhac")[0] == "β"
    assert run('@orth("bh") -> β\n', "wak", "mhac")[0] == "w"
    assert run('@orth("mh") -> β̃\n', "wak", "mhac")[0] == "β̃"


def test_an_untagged_word_is_left_alone():
    file = rf('[substitute]\n@orth("bh") -> β\n')
    assert apply_section(w("wak"), file.sections["substitute"], file, TABLE,
                         "substitute").segments[0] == "w"


def test_a_positional_tag_targets_one_element_of_a_multi_segment_unit():
    """O-6 / spec §11 — the whole point of the positional suffix (R12: draft 1 could not
    express 'the first element only')."""
    out = run('@orth("ia:1") -> i\n', "iə", "ia")
    assert out == ("i", "ə")


def test_a_two_item_target_claims_the_whole_unit():
    out = run('@orth("ia:1") @orth("ia:2") -> i a\n', "iə", "ia")
    assert out == ("i", "a")


def test_it_works_as_a_context_atom():
    file = rf('[substitute]\nɡ -> ɔ / @orth("bh") _\n')
    out = apply_section(tag_word(w("wɡ"), "bhg"), file.sections["substitute"], file, TABLE,
                        "substitute")
    assert out.segments == ("w", "ɔ")


@pytest.mark.parametrize("body,message", [
    ('w -> @orth("bh")\n', "may not appear in a replacement"),
    ('@orth("bh"):1 -> β\n', "may not carry a capture"),
    ('{@orth("bh") w} -> β\n', "may not appear inside"),
    ('@orth(bh) -> β\n', "one double-quoted string"),
    ('@orth("bh -> β\n', "one double-quoted string"),
])
def test_the_illegal_placements_raise_with_a_line_number(body, message):
    with pytest.raises(ParseError, match=message):
        rf("[substitute]\n" + body)


def test_an_unknown_unit_is_an_ERROR_not_a_warning(tmp_path):
    """R9: draft 1 made this a warning and disabled RULE_NEVER_MATCHES for orth items, so
    `@orth("ai")` — which targeted a unit the table did not have — was undetectable."""
    path = tmp_path / "t.rules"
    path.write_text(PREAMBLE + '[substitute]\n@orth("zz") -> β\n', encoding="utf-8")
    found = [f for f in check_rule_file(parse_rules_file(path, TABLE), TABLE)
             if f.code == "ORTH_UNKNOWN_UNIT"]
    assert found and found[0].severity == "error"


def test_a_position_beyond_the_units_arity_is_reported(tmp_path):
    path = tmp_path / "t.rules"
    path.write_text(PREAMBLE + '[substitute]\n@orth("ia:3") -> i\n', encoding="utf-8")
    assert [f for f in check_rule_file(parse_rules_file(path, TABLE), TABLE)
            if f.code == "ORTH_BAD_POSITION"]


def test_a_real_unit_with_a_valid_position_passes_check(tmp_path):
    path = tmp_path / "t.rules"
    path.write_text(PREAMBLE + '[substitute]\n@orth("ia:2") -> ə\n', encoding="utf-8")
    assert [f for f in check_rule_file(parse_rules_file(path, TABLE), TABLE)
            if f.code.startswith("ORTH_")] == []
```

- [ ] **Step 2:** `uv run pytest tests/test_dsl_orth_atom.py -q` → FAIL (the scanner rejects `@`).
- [ ] **Step 3:** in `_LineParser._scan`, add the `@` branch producing a `_Tok("orth", …)`; turn it
      into `ItemSpec(kind="orth", …)` in the item builder for TARGET and context atoms, rejecting a
      `:n` **capture** suffix (the positional suffix is inside the quotes, so there is no
      ambiguity); reject the token in the replacement parser and in the `{}`/`[]` bodies.
- [ ] **Step 4:** in `rewrite.match_item`, add the `orth` branch and pass `word=`/`index=` from
      `_match_target` and from `_match_ctx`'s `seg_at` (`index = p if step > 0 else p - 1`).
- [ ] **Step 5:** add `ORTH_UNKNOWN_UNIT` (error) and `ORTH_BAD_POSITION` (error) to
      `Checker.item`, loading the unit set once via `strands.orth.load_orth_table()`; return `[]`
      from `Checker.matching_segments` for orth items.
- [ ] **Step 6:** `uv run pytest -q` → green. A break in `test_dsl_core.py`/`test_rewrite.py` means
      the `match_item` signature change was not backward-compatible: make the new parameters
      keyword-only with `None` defaults; do not edit those tests. **Commit:**

```bash
git add src/strands/dsl.py src/strands/rewrite.py src/strands/check.py tests/test_dsl_orth_atom.py
git commit -m "feat(dsl): @orth(\"…\") item with positional tags; unknown units are check errors"
```

**Acceptance:** `@orth("bh")` separates *bhac* from *mhac*; `@orth("ia:1")` targets one half of a
diphthong and a two-item target claims both; an untagged word is inert; the five illegal placements
raise; an unknown unit and an out-of-range position are **errors**.

---
### Task 6 addendum: the `orth=` bundle constraint

`@orth("X")` is **sugar for the match bundle `[orth="X"]`** (O-6). `Bundle` gains
`orth: str | None = None`, and the bundle parser accepts `orth="…"` as an element beside the
optional class name and the `±feature` items. This is the only way to state spelling **and**
quality in one item, which R11 showed is required: `@orth("bh")` alone matches `w`, `vˠ` and `vʲ`
and a single broad replacement flattens the slender ones.

Add to `tests/test_dsl_orth_atom.py`:

```python
def test_at_orth_is_sugar_for_a_bundle():
    a = rf('[substitute]\n@orth("bh") -> β\n').sections["substitute"][0].target[0]
    b = rf('[substitute]\n[orth="bh"] -> β\n').sections["substitute"][0].target[0]
    assert a == b or (a.kind, b.kind) == ("orth", "bundle")


def test_a_bundle_conjoins_the_spelling_with_a_declared_class():
    """R11: this is how the filter keeps quality. Both segments are spelled ⟨bh⟩."""
    body = '[BROAD orth="bh"] -> β\n[SLEN orth="bh"] -> βʲ\n'
    assert run(body, "wak", "bhac")[0] == "β"
    assert run(body, "vʲiː", "bhí")[0] == "βʲ"


def test_a_bundle_may_conjoin_the_spelling_with_features():
    assert run('[C +continuant orth="bh"] -> β\n', "wak", "bhac")[0] == "β"


def test_an_orth_constraint_is_still_rejected_in_a_change_bundle():
    with pytest.raises(ParseError, match="may not appear in a replacement"):
        rf('[substitute]\nw -> [orth="bh"]\n')
```

`check.py` validates the `orth=` value exactly as it validates an `@orth` item
(`ORTH_UNKNOWN_UNIT`, `ORTH_BAD_POSITION`), and `Checker.matching_segments` for a bundle carrying
`orth=` returns the segments its class/feature half matches — so `RULE_NEVER_MATCHES` still works
on the phonological half.

---
## Task 7: `SpelledWord`, the grapheme table, `spelling_to_ipa`, and grapheme rewrites

**Depends on:** Tasks 1 and 6 — Task 6 only for the `src/strands/check.py` serialisation
(2 → 6 → 7 → 14); nothing here consumes `@orth`. **Spec:** §11 (the whole first bullet), §6;
digest §10.2 (master table and conventions 1–6), §10.1. O-27, O-10, O-11, O-14, O-28, O-29, O-32.

**This is the pivotal task of draft 2.** Everything Old Irish downstream of the retro-filter is
expressed in the object it defines. Read spec §11 before starting.

**Files:**
- Create: `src/strands/spelled.py`
- Create: `rules/old-irish-orthography.tsv`
- Modify: `src/strands/dsl.py` (a per-file `grammar = graphemes` mode for the sub-table sections)
- Modify: `src/strands/check.py` (`check_grapheme_table`)
- Test: `tests/test_spelled.py`

**Interfaces:**

```python
# ---- the object (O-27) --------------------------------------------------------------------
@dataclass(frozen=True)
class SpelledWord:
    graphemes: tuple[str, ...]      # LOWER-CASE grapheme tokens, in order (O-32)
    capitalized: bool = False       # render the first letter upper-case
    mutation: str = ""              # "" | "LEN" | "NAS" — the INITIAL mutation, as metadata

    @classmethod
    def from_spelling(cls, text: str) -> "SpelledWord": ...
        """Tokenize a written Old Irish word. Lossless: `render()` returns `text` again."""
    def render(self, *, punctum: bool = True) -> str: ...
        """The written form. `punctum=False` substitutes each token's PLAIN FORM from the
        grapheme table's `punctum` column (ṡ->s, ḟ->f) in the OUTPUT ONLY (O-14). The
        substitution is data, not a hardcoded map, so a later punctum form needs a table row
        and no code change."""
    def ipa(self) -> tuple[str, ...]: ...
        """= spelling_to_ipa(self). One-way and final (O-11)."""

class SpelledError(Exception): ...

# ---- the table ----------------------------------------------------------------------------
OI_ORTHOGRAPHY_PATH: Path                      # rules/old-irish-orthography.tsv

ROLES = ("cons", "vowel", "long", "nasal", "glide", "silent", "ending")
"""The complete `role` vocabulary. `glide` and `silent` produce no segment and mark quality
or nothing; `ending` is the unresolved ending marker of spec §11 (see below). There is NO
`punctum` role: a punctum form is an ordinary consonant or silent token that happens to have
a plain-letter variant, which is the `punctum` COLUMN."""

@dataclass(frozen=True)
class GraphemeRow:
    token: str          # lower-case letters as written, 1-3 chars
    env: str            # "initial" | "noninitial" | "any"
    left: str           # letters that must precede (digest §10.2 conv.4), or "" for any
    ipa: tuple[str, ...]   # () = silent
    role: str           # one of ROLES
    punctum: str        # the plain-letter form for `punctum = off`, or "" for none
    note: str

def load_graphemes(path=None) -> tuple[GraphemeRow, ...]   # LONGEST TOKEN FIRST, then file order
def tokenize_spelling(text: str) -> tuple[str, ...]
def spelling_to_ipa(word: SpelledWord) -> tuple[str, ...]
def spelling_to_words(text: str) -> tuple[SpelledWord, ...]     # splits on whitespace

# ---- grapheme rewrites (O-10) -------------------------------------------------------------
@dataclass(frozen=True)
class GraphemeRule:
    table: str          # the sub-table it belongs to ("LEN", "GEN_O", …)
    line: int
    rule_id: str        # "<section>:<line>"
    target: tuple[str, ...]        # grapheme tokens, an inline set, or the class V / C
    replacement: tuple[str, ...]   # tokens, or () for deletion
    left: tuple[str, ...]          # context atoms: tokens, sets, classes, "#"
    right: tuple[str, ...]
    tag: str
    comment: str

def apply_grapheme_table(word: SpelledWord, rules: Sequence[GraphemeRule],
                         *, simultaneous: bool) -> SpelledWord
    """`simultaneous=True` for a mutation table (one pass against the pre-table word, first
    rule in file order wins an overlapping span — the `irish._apply_table` contract);
    `simultaneous=False` for an inflection (ordered, each rule sees the previous output)."""
```

**The `dsl.py` change.** `[meta] grammar = graphemes` in a rule file makes the parser read
`[mutations]`, `[inflect]` and `[templates]` as **grapheme** sections: the rewrite lines keep the
familiar `TARGET -> REPLACEMENT [/ LEFT _ RIGHT] [%tag] [# comment]` shape, but the items are
grapheme tokens (validated against the grapheme table, not `features.tsv`), the only context atoms
are tokens, inline sets `{c t p}`, the classes `V`/`C` (derived from the table's `role`) and `#`,
and the result is `GraphemeRule`, not `Rule`. `RuleFile` gains
`grapheme_mutations: dict[str, tuple[GraphemeRule, ...]]` and `grapheme_inflect: …`; the existing
`mutations`/`inflect` fields stay empty for such a file, so `irish.rules` and the four targets are
untouched. Without the meta key the parser behaves exactly as today.

**The grapheme table.** Header `token  env  left  ipa  role  punctum  note`; `ipa` is `+`-joined
or `-` for silent; `left` is a set of letters or `-`; `role` is one of `ROLES`; `punctum` is the
plain-letter form used when `punctum = off`, or `-` for none. Rows, transcribed from digest §10.2's
master table and conventions, with the citation in `note` (the `punctum` column is `-` on every row
except the two named):

| token | env | left | ipa | role | punctum | source |
|---|---|---|---|---|---|---|
| `mb` | initial | – | `mˠ` | nasal | - | master table ⟨b⟩ eclipsed = **/m/** (O-29; §10.4's *a m-bo* is the counter-datum) |
| `nd` | initial | – | `n̪ˠ` | nasal | - | master table ⟨d⟩ eclipsed |
| `ng` | initial | – | `ŋ` | nasal | - | master table ⟨g⟩ eclipsed |
| `ch` | any | – | `x` | cons | - | master table, ⟨c⟩ lenited |
| `th` | any | – | `θ` | cons | - | master table |
| `ph` | any | – | `fˠ` | cons | - | master table |
| `ṡ` | any | – | `h` | cons | s | master table ⟨ṡ sh⟩ = /h/ |
| `sh` | any | – | `h` | cons | - | master table (the pre-punctum spelling) |
| `ḟ` | any | – | `-` | silent | f | master table ⟨ḟ fh⟩ = **∅** |
| `fh` | any | – | `-` | silent | - | master table |
| `cc` | any | – | `k` | cons | - | conv. 3 (geminate = unmutated) |
| `tt` | any | – | `t̪ˠ` | cons | - | conv. 3 |
| `pp` | any | – | `pˠ` | cons | - | conv. 3 |
| `bb` | any | – | `bˠ` | cons | - | conv. 3 |
| `ss` | any | – | `sˠ` | cons | - | conv. 3 (*Nessa*, *Fergusso* — R29a) |
| `ll` | any | – | `l̪ˠ+l̪ˠ` | cons | - | conv. 3, fortis (O-2) |
| `nn` | any | – | `n̪ˠ+n̪ˠ` | cons | - | conv. 3 |
| `rr` | any | – | `ɾˠ+ɾˠ` | cons | - | conv. 3 |
| `mm` | any | – | `mˠ+mˠ` | cons | - | conv. 3 |
| `c` | initial | – | `k` | cons | - | master table |
| `c` | noninitial | – | `ɡ` | cons | - | conv. 2 (*bec* /bʲeɡ/ vs *becc*) |
| `t` | initial | – | `t̪ˠ` | cons | - | master table |
| `t` | noninitial | – | `d̪ˠ` | cons | - | conv. 2 (*brot* /brod/) |
| `p` | initial | – | `pˠ` | cons | - | master table |
| `p` | noninitial | – | `bˠ` | cons | - | conv. 2 |
| `b` | initial | – | `bˠ` | cons | - | master table |
| `b` | noninitial | `m` | `bˠ` | cons | - | **conv. 4** — *imb* /imʲbʲ/ (R28) |
| `b` | noninitial | – | `β` | cons | - | conv. 2 — *dub* /duv/, *marb* /marv/ |
| `d` | initial | – | `d̪ˠ` | cons | - | master table |
| `d` | noninitial | `nr` | `d̪ˠ` | cons | - | **conv. 4** — *bind*, *cerd* (R28) |
| `d` | noninitial | – | `ð` | cons | - | conv. 2 — *mod* /moð/ |
| `g` | initial | – | `ɡ` | cons | - | master table |
| `g` | noninitial | `nlr` | `ɡ` | cons | - | **conv. 4** — *long* /Loŋɡ/, *delg* (R28); *ingen* /inʲɣʲən/ is the stated exception and is a lexicon row |
| `g` | noninitial | – | `ɣ` | cons | - | conv. 2 — *mug* /muɣ/ |
| `m` | initial | – | `mˠ` | cons | - | master table |
| `m` | noninitial | – | `β̃` | cons | - | master table (non-initial ⟨m⟩ = /ṽ/) |
| `f` `s` `h` `l` `n` `r` | any | – | `fˠ` `sˠ` `h` `l̪ˠ` `n̪ˠ` `ɾˠ` | cons | - | master table |
| `aí` `áe` | any | – | `a+i` | vowel | - | §10.1 diphthongs, **O-28 values** |
| `oí` `óe` | any | – | `o+i` | vowel | - | §10.1 |
| `uí` | any | – | `u+i` | vowel | - | §10.1 |
| `áu` | any | – | `a+u` | vowel | - | §10.1 |
| `éu` `éo` | any | – | `e+u` | vowel | - | §10.1 |
| `íu` | any | – | `i+u` | vowel | - | §10.1 |
| `ía` | any | – | `i+a` | vowel | - | §10.1 |
| `úa` | any | – | `u+a` | vowel | - | §10.1 |
| `á` `é` `í` `ó` `ú` | any | – | `aː` `eː` `iː` `oː` `uː` | long | - | §10.1, and "all unstressed long vowels have been shortened" [pokorny1914 p.20 §56] applies only to *unaccented* letters |
| `ae` | any | – | `ə` | vowel | - | §41 final ⟨-ae⟩ after a broad consonant (R29a) |
| `ai` | any | – | `ə` | vowel | - | §41 final ⟨-ai⟩ |
| `ea` | any | – | `a` | vowel | - | §40 final ⟨-ea⟩ after a slender consonant |
| `eo` | any | – | `o` | vowel | - | §40 final ⟨-eo⟩ |
| `iu` | any | – | `u` | vowel | - | §40 final ⟨-iu⟩ |
| `a` `e` `o` `u` | any | – | `a` `e` `o` `u` | vowel | - | §10.1, five short vowels |
| `i` | any | – | `i` | vowel | - | §10.1 |
| `n-` | initial | – | `n̪ˠ` | nasal | - | §10.4 nasalization of a vowel-initial word |
| `ə` | any | – | `-` | **ending** | - | **spec §11's unresolved ending marker.** Not a letter of the Old Irish alphabet and never a finished output: Task 11 writes it for a stem-final modern /ə/ the filter cannot resolve, and Task 14's `NOM_A`/`NOM_O` replace it with ⟨e⟩ or ⟨a⟩ by stem class. It is in the table for exactly one reason — so that `SpelledWord.from_spelling` can tokenize a `[respell]` output that still contains it. Its reconstruction is **empty**, so a leaked marker is silent rather than a bogus segment |

**The ending marker is a token, not a letter.** `ə` is the single `role = ending` row. It exists
only to keep the RETRO hand-off tokenizable: Task 11's `ə -> "ə" / _ #` emits it, Task 12 hands the
string to `SpelledWord.from_spelling`, and Task 14 eliminates it. **An `ə` in a finished output is
an error**, enforced in three places — `SpelledWord.render()` does *not* special-case it (so it
would be visible), Task 18's property test asserts no gallery output contains it, and
`check_grapheme_table` asserts there is exactly one `ending` row so nobody adds a second escape
hatch. Its empty reconstruction means a leak degrades to a missing sound, not a wrong one.

**Silent tokens and the glide.** The glide ⟨i⟩ of digest §10.2 conv. 5 §36 is **not** a separate
letter in the source — it is an ⟨i⟩ that carries no vowel. It cannot therefore be a distinct table
row keyed on spelling. It is produced by the reconstruction's **quality pass** instead: an ⟨i⟩ token
that is (a) not word-initial, (b) immediately followed by a `cons`-role token, and (c) immediately
preceded by a `vowel`- or `long`-role token, is reclassified as `role = glide`, contributes **no
segment**, and makes the following consonant slender. This is exactly Pokorny §36 read forwards, and
it is why `spelling_to_ipa("muir")` is `(mˠ, u, ɾʲ)` and not `(mˠ, u, i, ɾˠ)` (R29a).

**The reconstruction, step by step** (`spelling_to_ipa`):

1. **Initial mutation.** If `word.mutation == "LEN"`, the first token is replaced for the purpose of
   reconstruction by its lenition value: `b→β`, `d→ð`, `g→ɣ`, `m→β̃` (unwritten, digest §10.2
   conv. 1 — this is precisely the metadata the spelled word exists to carry), while `ch th ph ṡ ḟ`
   are already written and need nothing. If `"NAS"`, `c→ɡ`, `t→d̪ˠ`, `p→bˠ` (unwritten, spec §11
   (ii)); `mb nd ng n-` are already written.
2. **Glide reclassification** (above).
3. **Row selection**, left to right: the first row whose `token` matches, whose `env` is satisfied
   (`initial` ⇔ token index 0), and whose `left` is empty or contains the last letter of the
   previous token. Append its `ipa`.
4. **Quality pass** (digest §10.2 conv. 5; R29b — this is the digest's rule, not draft 1's
   "following-first-else-preceding"): a consonant segment is **slender** iff the token that produced
   it is immediately followed by a token written ⟨e é i í⟩, **or** is immediately preceded by a
   glide ⟨i⟩. Otherwise it stays broad. A doubled token is one unit, so both of its segments take
   the same quality (R29b's geminate split cannot occur). The BROAD↔SLEN mapping is the **explicit
   declared pair list** of `old-irish.rules [classes]` (spec §11), read by name — never derived
   positionally; `w` is listed as having no partner.
5. **Unstressed reduction** (digest §10.2 conv. 5 grid, §10.1 "non-finally, only two phonemes: /ə/
   and /u/"): a `vowel`-role token that is **not** in the first syllable and is **not** word-final
   reduces to `ə`. `long`-role tokens never reduce. Word-final vowels do not reduce (digest §10.1:
   "word-finally, all ten short-vowel × quality combinations occur").

**Failure mode.** A character no token matches raises `SpelledError` naming the spelling and the
offending character and position. This is a rule-file or lexicon bug, not user data (I-24).

- [ ] **Step 1: Write the failing tests**

`tests/test_spelled.py`:

```python
"""Task 7: the spelled word, the grapheme table and the one-way reconstruction (spec §11)."""
import pytest

from helpers import ROOT
from strands.spelled import (OI_ORTHOGRAPHY_PATH, GraphemeRule, SpelledError, SpelledWord,
                             apply_grapheme_table, load_graphemes, spelling_to_ipa,
                             spelling_to_words, tokenize_spelling)


def ipa(text, mutation=""):
    return spelling_to_ipa(SpelledWord.from_spelling(text).with_mutation(mutation))


# ---- losslessness: the property the whole design exists for ------------------------------

@pytest.mark.parametrize("text", [
    "macc", "bec", "dub", "cloch", "bláth", "túath", "fer", "coll", "claideb", "carae",
    "muir", "dígal", "brithem", "Ériu", "Máel Coluim", "ṡúil", "ḟer", "mbó", "Nessa",
])
def test_a_spelled_word_round_trips_its_own_spelling(text):
    """O-27: `"".join(tokens)` IS the written form. This is the losslessness claim."""
    for part in text.split(" "):
        assert SpelledWord.from_spelling(part).render() == part


def test_capitalization_is_metadata_not_a_token():
    """O-32: tokens are lower-case; the capital is re-applied at render."""
    w = SpelledWord.from_spelling("Ériu")
    assert w.capitalized is True
    assert all(g == g.lower() for g in w.graphemes)
    assert w.render() == "Ériu"
    assert SpelledWord.from_spelling("fer").capitalized is False


def test_the_table_is_sorted_longest_token_first():
    rows = load_graphemes()
    assert OI_ORTHOGRAPHY_PATH == ROOT / "rules" / "old-irish-orthography.tsv"
    assert [len(r.token) for r in rows] == sorted([len(r.token) for r in rows], reverse=True)


# ---- reconstruction: the digest's own worked examples --------------------------------------

@pytest.mark.parametrize("text,expected", [
    ("macc", ("mˠ", "a", "k")),           # conv. 2-3: doubled = fortis
    ("bec", ("bʲ", "e", "ɟ")),            # conv. 2: non-initial ⟨c⟩ = /ɡ/, slender by ⟨e⟩
    ("bratt", ("bˠ", "ɾˠ", "a", "t̪ˠ")),
    ("brot", ("bˠ", "ɾˠ", "o", "d̪ˠ")),
    ("dub", ("d̪ˠ", "u", "β")),
    ("mod", ("mˠ", "o", "ð")),
    ("mug", ("mˠ", "u", "ɣ")),
    ("ech", ("e", "x")),
    ("áth", ("aː", "θ")),
])
def test_the_digests_worked_examples_reconstruct(text, expected):
    """Every pair is printed in digest §10.2 conventions 2 and 3."""
    assert ipa(text) == expected


@pytest.mark.parametrize("text,expected", [
    ("imb", ("i", "mʲ", "bʲ")),          # conv. 4: after ⟨m⟩, ⟨b⟩ = /b/
    ("marb", ("mˠ", "a", "ɾˠ", "β")),    # conv. 4: after ⟨r⟩, ⟨b⟩ = /v/
    ("bind", ("bʲ", "i", "n̪ˠ", "d̪ˠ")),  # conv. 4: after ⟨n⟩, ⟨d⟩ = /d/
    ("long", ("l̪ˠ", "o", "ŋ", "ɡ")),     # conv. 4: after ⟨n⟩, ⟨g⟩ = /ɡ/
    ("delg", ("dʲ", "e", "lʲ", "ɡ")),
])
def test_convention_4_stops_after_l_n_r_m(text, expected):
    """digest §10.2 conv. 4 — draft 1 omitted this entirely (R28) and reconstructed
    *derg*, *long*, *ferg* wrongly; all three are lexicon rows."""
    assert ipa(text) == expected


def test_the_glide_i_contributes_no_segment_and_slenderizes():
    """digest §10.2 conv. 5 §36 (R29a): *muir* < *mori*."""
    assert ipa("muir") == ("mˠ", "u", "ɾʲ")
    assert ipa("cnáim") == ("k", "n̪ˠ", "aː", "mʲ")
    assert ipa("athair") == ("a", "θ", "a", "ɾʲ")


def test_no_glide_is_read_before_a_broad_consonant():
    """§39: *fer* < *viros*. R29b: draft 1's post-pass slenderized this wrongly."""
    assert ipa("fer") == ("fʲ", "e", "ɾˠ")


def test_a_doubled_token_takes_one_quality_for_both_halves():
    """R29b: the geminate must not split. It is ONE token (O-2)."""
    assert ipa("coll") == ("k", "o", "l̪ˠ", "l̪ˠ")
    assert ipa("cinn") == ("k", "i", "nʲ", "nʲ")


def test_unstressed_vowels_reduce_but_final_and_long_ones_do_not():
    """digest §10.2 conv. 5 grid; §10.1 'word-finally, all ten combinations occur'."""
    assert ipa("dígal") == ("dʲ", "iː", "ɣ", "ə", "l̪ˠ")
    assert ipa("claideb") == ("k", "l̪ˠ", "a", "dʲ", "ə", "β")
    assert ipa("carae")[-1] == "ə"           # final ⟨-ae⟩ is /ə/ by its own row
    assert ipa("brithem") == ("bʲ", "ɾʲ", "i", "θʲ", "ə", "mˠ")


@pytest.mark.parametrize("text,expected", [
    ("aí", ("a", "i")), ("oí", ("o", "i")), ("uí", ("u", "i")), ("áu", ("a", "u")),
    ("éu", ("e", "u")), ("íu", ("i", "u")), ("ía", ("i", "a")), ("úa", ("u", "a")),
])
def test_the_eight_diphthongs_use_the_wiki_old_irish_values(text, expected):
    """O-28 / R19: `wiki-old-irish` §Vowels gives ai oi ui au eu iu ia ua. Draft 1's
    `aːi`/`iə` contradicted digest §10.8 conflict 5 and used the modern reduction vowel."""
    assert ipa(text) == expected


def test_the_nasalized_voiced_stop_is_a_single_nasal():
    """O-29 / R25: master table ⟨mb⟩ = /m/, not /mb/."""
    assert ipa("mbó") == ("mˠ", "oː")
    assert ipa("ndu") == ("n̪ˠ", "u")


def test_lenited_f_is_written_and_silent():
    """R24: ⟨ḟ⟩ is a TOKEN with an empty reconstruction — no segment is deleted, so
    nothing has to carry provenance for it."""
    w = SpelledWord.from_spelling("ḟer")
    assert w.graphemes[0] == "ḟ" and w.render() == "ḟer"
    assert spelling_to_ipa(w) == ("e", "ɾˠ")


# ---- the mutation metadata ----------------------------------------------------------------

def test_unwritten_lenition_lives_in_the_metadata_and_changes_only_the_ipa():
    """digest §10.2 conv. 1: *a bo* /a vo/ is still WRITTEN *bo*. This is the single reason
    the spelled word carries a mutation field."""
    w = SpelledWord.from_spelling("bo").with_mutation("LEN")
    assert w.render() == "bo"
    assert spelling_to_ipa(w)[0] == "β"


def test_unwritten_nasalization_of_a_voiceless_stop_likewise():
    """spec §11 (ii): only ⟨mb nd ng⟩ and ⟨n-V⟩ are written."""
    w = SpelledWord.from_spelling("tech").with_mutation("NAS")
    assert w.render() == "tech"
    assert spelling_to_ipa(w)[0] == "dʲ"


# ---- punctum is rendering only (O-14) -----------------------------------------------------

def test_punctum_off_changes_the_string_and_provably_not_the_ipa():
    w = SpelledWord.from_spelling("ṡúil")
    assert w.render(punctum=True) == "ṡúil"
    assert w.render(punctum=False) == "súil"
    assert spelling_to_ipa(w) == spelling_to_ipa(SpelledWord.from_spelling(w.render(punctum=False))) \
        or spelling_to_ipa(w)[0] == "h"


# ---- grapheme rewrites (O-10) -------------------------------------------------------------

def rule(target, replacement, left=(), right=(), table="T"):
    return GraphemeRule(table=table, line=1, rule_id="t:1", target=tuple(target),
                        replacement=tuple(replacement), left=tuple(left), right=tuple(right),
                        tag="attested", comment="")


def test_a_grapheme_rewrite_edits_tokens_not_letters():
    w = SpelledWord.from_spelling("cenn")
    out = apply_grapheme_table(w, [rule(("c",), ("ch",), left=("#",))], simultaneous=True)
    assert out.render() == "chenn"
    assert out.graphemes == ("ch", "e", "nn")


def test_a_mutation_table_is_simultaneous_and_first_rule_wins():
    """The `irish._apply_table` contract: `c -> ch` must not feed `ch -> x`."""
    rules = [rule(("c",), ("ch",), left=("#",)), rule(("ch",), ("x",), left=("#",))]
    assert apply_grapheme_table(SpelledWord.from_spelling("cenn"), rules,
                                simultaneous=True).render() == "chenn"


def test_an_inflection_table_is_ordered_and_each_rule_sees_the_last_output():
    rules = [rule(("c",), ("ch",), left=("#",)), rule(("ch",), ("x",), left=("#",))]
    assert apply_grapheme_table(SpelledWord.from_spelling("cenn"), rules,
                                simultaneous=False).render() == "xenn"


def test_capitalization_and_mutation_survive_a_rewrite():
    w = SpelledWord.from_spelling("Cenn").with_mutation("NAS")
    out = apply_grapheme_table(w, [rule(("c",), ("ch",), left=("#",))], simultaneous=True)
    assert out.render() == "Chenn" and out.mutation == "NAS"


# ---- failure ------------------------------------------------------------------------------

# ---- the ending marker (spec §11) ---------------------------------------------------------

def test_the_ending_marker_tokenizes_and_reconstructs_to_nothing():
    """It exists so a [respell] output carrying an unresolved stem-final /ə/ can become a
    SpelledWord at all (Task 11 -> Task 12). Its reconstruction is EMPTY."""
    w = SpelledWord.from_spelling("carə")
    assert w.graphemes == ("c", "a", "r", "ə") and w.render() == "carə"
    assert spelling_to_ipa(w) == ("k", "a", "ɾˠ")


def test_the_ending_marker_is_the_only_ending_role_row():
    """check_grapheme_table enforces this: one temporary escape hatch, not a family."""
    assert [r.token for r in load_graphemes() if r.role == "ending"] == ["ə"]


def test_the_ending_marker_is_not_hidden_at_render_time():
    """A leaked marker must be VISIBLE, so Task 18's property test can catch it. It is an
    error in a finished output, never a silently-dropped character."""
    assert "ə" in SpelledWord.from_spelling("carə").render()
    assert "ə" in SpelledWord.from_spelling("carə").render(punctum=False)


def test_punctum_off_uses_the_tables_punctum_column_not_a_hardcoded_map():
    rows = {r.token: r.punctum for r in load_graphemes()}
    assert rows["ṡ"] == "s" and rows["ḟ"] == "f"
    assert all(r.punctum == "" for r in load_graphemes() if r.token not in ("ṡ", "ḟ"))


def test_no_row_uses_a_punctum_role():
    """The punctum forms are ordinary cons/silent rows with a plain-letter variant."""
    from strands.spelled import ROLES
    assert "punctum" not in ROLES
    by_token = {r.token: r.role for r in load_graphemes()}
    assert by_token["ṡ"] == "cons" and by_token["ḟ"] == "silent"


def test_an_unknown_character_raises_and_names_it():
    with pytest.raises(SpelledError, match="z"):
        SpelledWord.from_spelling("fezr")


def test_a_multi_word_form_splits_into_words():
    words = spelling_to_words("Cú Chulainn")
    assert len(words) == 2 and words[1].graphemes[0] == "ch"
    assert words[0].capitalized and words[1].capitalized
```

- [ ] **Step 2: Run them and watch them fail**

Run: `uv run pytest tests/test_spelled.py -q`
Expected: FAIL — `ModuleNotFoundError: No module named 'strands.spelled'`.

- [ ] **Step 3: Write `rules/old-irish-orthography.tsv`**

Exactly the table above. Where two rows share a token, write the more specific one first
(`initial` before `noninitial`; a non-empty `left` before an empty one) — the loader sorts by token
length only, so file order is the tie-break and it is load-bearing for conv. 4.

- [ ] **Step 4: Write `src/strands/spelled.py`**

Module docstring: what the spelled word is and why (spec §11); that losslessness is the point; that
`spelling_to_ipa` is one-way and final (O-11); that `punctum` is rendering only (O-14); that the
BROAD↔SLEN pairing is read from the declared class lists and never derived positionally.

`with_mutation(name)` returns a copy with `mutation=name` (used by the tests above and by Task 13).

- [ ] **Step 5: Add the `grammar = graphemes` mode to `dsl.py` and the checks to `check.py`**

`check_grapheme_table(path)` validates: every `ipa` segment is a `features.tsv` row; every `env` is
one of the three; `role` is one of `spelled.ROLES` (**seven** values — `cons vowel long nasal
glide silent ending`; there is no `punctum` role, so the ⟨ṡ⟩/⟨ḟ⟩ rows validate as `cons`/`silent`
carrying a `punctum` column value); the `punctum` column, where non-empty, is a single plain letter;
**exactly one row has `role = ending`**; no two rows have the same `(token, env, left)`; and
every `token` is reachable — i.e. tokenizing the concatenation of all tokens yields each of them at
least once. `Checker.grapheme_rules` (added in Task 14) will validate the sub-tables against it.

Run `uv run pytest tests/test_dsl_core.py tests/test_dsl_sections.py tests/test_check.py -q` before
going on: the mode must be inert without the meta key.

- [ ] **Step 6: Run the tests and the suite; commit**

```bash
git add src/strands/spelled.py rules/old-irish-orthography.tsv src/strands/dsl.py \
        src/strands/check.py tests/test_spelled.py
git commit -m "feat(spelled): lossless Old Irish spelled word, grapheme table, one-way reconstruction"
```

**Acceptance:** every spelled word round-trips its own spelling; the digest's conv. 2, 3 and 4
examples reconstruct; the glide ⟨i⟩ contributes no segment; doubled tokens keep one quality;
unstressed non-final short vowels reduce; the eight diphthongs use the O-28 values; ⟨mb⟩ is a single
nasal; ⟨ḟ⟩ is a written silent token with `punctum = f`; the `ə` ending marker tokenizes,
reconstructs to nothing, renders visibly and is the only `ending` row; unwritten lenition changes
the IPA and not the string; `punctum=off` changes the string via the table's own column and not the
IPA; grapheme tables apply simultaneously or in order
as asked; the suite is unchanged.

---
## Task 8: `old-irish.rules` — `[meta]`, `[inventory]`, `[classes]`

**Depends on:** Tasks 1, 7. **Spec:** §2, §4, §11. O-1, O-2, O-3, O-5. **Review:** S5, S6, S7, S17.

**Files:** create `rules/old-irish.rules`; test `tests/test_rules_old_irish.py`.

`[meta]` keys other tasks read: `name`, `strand = old-irish` (**the dispatch key**, O-9),
`digest`, `lexicon`, `orthography = rules/old-irish-orthography.tsv`, `punctum = on`,
`grammar = graphemes` (Task 7's parser mode), and **`quality-pairs`** — the explicit BROAD↔SLEN
mapping spec §11 requires, written `pˠ:pʲ bˠ:bʲ … w:-`, where `-` means "no partner". It is read by
`spelled.py`'s quality pass and **never derived positionally**: draft 1 derived it from the two
class lists by index, which GPT #2 measured as broken (20 members vs 19, `w` unpaired). No
`epithet-ADJ`/`epithet-NOUN`: this strand has no target affixes (I-39, and see O-17/R30).

```
[meta]
name = Old Irish
strand = old-irish
grammar = graphemes
digest = sources/irish/digest.md §10
lexicon = rules/old-irish-lexicon.tsv
orthography = rules/old-irish-orthography.tsv
punctum = on
# spec §11: an EXPLICIT declared mapping. `-` = no partner. Read by spelled.py's quality pass.
quality-pairs = pˠ:pʲ bˠ:bʲ t̪ˠ:tʲ d̪ˠ:dʲ k:c ɡ:ɟ fˠ:fʲ sˠ:ʃ x:ç ɣ:ɣʲ β:βʲ β̃:β̃ʲ ð:ðʲ θ:θʲ mˠ:mʲ n̪ˠ:nʲ ŋ:ɲ l̪ˠ:lʲ ɾˠ:ɾʲ h:h w:-

[inventory]
# digest §10.1 chart [wiki-old-irish §Consonants]. Quality is NOT reversed (spec §4, O-3).
bˠ bʲ t̪ˠ tʲ d̪ˠ dʲ k c ɡ ɟ
# The lenited series (O-1). /xʲ/ IS ç; /ɣʲ/ is its own row (R26).
β βʲ β̃ β̃ʲ ð ðʲ θ θʲ x ç ɣ ɣʲ
# /s f h/ are inventory members (O-5, spec §11 (iii)); what CREATES them is restricted, not
# what may appear.
fˠ fʲ sˠ ʃ h
# One sonorant series (O-2): fortis is a doubled GRAPHEME (Task 7), not a segment.
mˠ mʲ n̪ˠ nʲ ŋ ɲ l̪ˠ lʲ ɾˠ ɾʲ
# 5 short + 5 long [pokorny1914-oldirish-grammar p.6 §4] via digest §10.1, plus the
# post-stress reduction vowel of the §10.2 grid.
i e a o u iː eː aː oː uː ə
# /p/ is "relatively rare… a recent import" (digest §10.1). /w/ is NOT an Old Irish phoneme
# (S6) — the filter rewrites any survivor, so it is admitted only marginally, with its
# slender partner. /ə/ is a reduction and must never be chosen by the inventory fallback.
# /hʲ/ "may have been the same sound as /h/ or /xʲ/" and short /æ/ comes from u-infection of
# stressed /a/, "rampant in names in the prefix air-" (digest §10.1) — both name-relevant,
# both already features.tsv rows, both marginal (S5).
marginal: pˠ pʲ w vʲ ə hʲ æ

[classes]
# spec §12.J / I-41, extended with the Old Irish lenited series (O-3).
BROAD = pˠ bˠ t̪ˠ d̪ˠ fˠ sˠ w mˠ n̪ˠ l̪ˠ ɾˠ k ɡ x ɣ ŋ β β̃ ð θ
SLEN  = pʲ bʲ tʲ dʲ fʲ ʃ vʲ mʲ nʲ lʲ ɾʲ c ɟ ç ɣʲ ɲ βʲ β̃ʲ ðʲ θʲ
# digest §2.4: the epenthesis environment is after l n r m (O-15).
SONORANT = mˠ mʲ n̪ˠ nʲ ŋ ɲ l̪ˠ lʲ ɾˠ ɾʲ
# UNMARKED is declared for parity with the other rule files and is NOT used here: this file
# has no [normalize] section, which is UNMARKED's only consumer (S17).
UNMARKED = p b t d f v s m n l r
```

Diphthongs are not inventory rows (I-2 / §12.B); Task 10 declares them as `nuclei`. Like engine-plan
Task 23a this task writes a **temporary permissive** `[syllable]` block, marked so Task 10 cannot
miss it, and may not call `adapt()`/`repair()`.

- [ ] **Step 1: Write the failing tests** — `tests/test_rules_old_irish.py`:

```python
"""Tasks 8-11: `rules/old-irish.rules` as data (spec §4, §6, §11; digest §10)."""
import pytest

from helpers import ROOT, TABLE, target, w
from strands.check import check_rule_file

PATH = ROOT / "rules" / "old-irish.rules"
OI = target("old-irish")


def test_the_file_parses_and_check_reports_no_errors():
    assert [f for f in check_rule_file(OI, TABLE) if f.severity == "error"] == []


def test_meta_declares_the_keys_the_pipeline_and_spelled_module_read():
    assert OI.meta["strand"] == "old-irish"          # O-9: the dispatch key
    assert OI.meta["grammar"] == "graphemes"         # O-10 / Task 7's parser mode
    assert OI.meta["orthography"].endswith("old-irish-orthography.tsv")
    assert OI.meta.get("punctum", "on") in ("on", "off")


def test_the_quality_pairs_are_declared_explicitly_and_completely():
    """spec §11: an EXPLICIT mapping, never derived positionally (GPT #2 measured draft 1's
    positional derivation as 20-vs-19 with `w` unpaired)."""
    pairs = dict(p.split(":") for p in OI.meta["quality-pairs"].split())
    assert pairs["w"] == "-"                          # no partner, stated as such
    for broad, slender in pairs.items():
        assert broad in OI.classes["BROAD"] or broad in ("h",), broad
        assert slender in OI.classes["SLEN"] or slender in ("-", "h"), slender
    assert {b for b in OI.classes["BROAD"] if b != "w"} <= set(pairs)


def test_this_strand_declares_no_epithet_slots():
    assert "epithet-ADJ" not in OI.meta and "epithet-NOUN" not in OI.meta


@pytest.mark.parametrize("segment", ["β", "βʲ", "β̃", "β̃ʲ", "ð", "ðʲ", "θ", "θʲ", "x", "ç",
                                     "ɣ", "ɣʲ", "sˠ", "ʃ", "fˠ", "fʲ", "h"])
def test_the_lenited_series_and_the_lenition_products_are_in_the_inventory(segment):
    assert segment in OI.inventory


@pytest.mark.parametrize("vowel", ["i", "e", "a", "o", "u", "iː", "eː", "aː", "oː", "uː"])
def test_the_five_short_and_five_long_vowels_are_there(vowel):
    assert vowel in OI.inventory


def test_the_marginal_set_is_exactly_the_documented_one():
    """S5, S6, S7: /p/ a Latin import; /w vʲ/ not Old Irish phonemes; /ə/ a reduction;
    /hʲ/ and /æ/ name-relevant but uncertain."""
    assert set(OI.marginal) == {"pˠ", "pʲ", "w", "vʲ", "ə", "hʲ", "æ"}


def test_no_fortis_sonorant_segments_were_invented():
    assert not {"L", "N", "R"} & set(OI.inventory)


def test_the_quality_classes_are_declared_not_derived():
    assert "β" in OI.classes["BROAD"] and "βʲ" in OI.classes["SLEN"]
    assert "k" in OI.classes["BROAD"] and "c" in OI.classes["SLEN"]
    assert set(OI.classes["SONORANT"]) >= {"l̪ˠ", "n̪ˠ", "ɾˠ", "mˠ"}


def test_every_rule_line_everywhere_carries_a_citation():
    """R32: draft 1 iterated only `OI.sections`, so [mutations], [inflect] and [templates]
    — separate RuleFile fields — were entirely unchecked."""
    def cited(comment):
        c = (comment or "").strip()
        return (c.startswith(("digest", "[", "design:")) or "digest §10" in c
                or "pokorny1914" in c or "strachan1909" in c or "wiki-old-irish" in c)
    bad = [(s, r.line) for s, rules in OI.sections.items() for r in rules if not cited(r.comment)]
    for name, rules in {**OI.grapheme_mutations, **OI.grapheme_inflect}.items():
        bad += [(name, r.line) for r in rules if not cited(r.comment)]
    text = PATH.read_text(encoding="utf-8")
    body = text.split("[templates]")[1] if "[templates]" in text else ""
    for line in body.splitlines():
        if "=" in line and not line.lstrip().startswith("#"):
            assert "#" in line, line
    assert bad == [], bad
```

- [ ] **Step 2:** `uv run pytest tests/test_rules_old_irish.py -q` → FAIL (no rule file).
- [ ] **Step 3:** write the file above, plus the temporary block:

```
[syllable]
# TEMPORARY (Task 8): replaced wholesale by Task 10. Do not ship.
template = any
onsets   = any
codas    = any
sonority = off
```

- [ ] **Step 4:** `uv run strands check rules/old-irish.rules` → exit 0; `uv run pytest -q` → green.
- [ ] **Step 5: Commit** — `feat(rules): old-irish.rules skeleton — meta, inventory, classes, quality pairs`

**Acceptance:** the file parses and `check` is error-free; `strand` and `grammar` are declared;
`quality-pairs` covers every BROAD member and states `w:-`; the marginal set is exactly the seven
documented segments; the citation test covers all five rule-bearing sections.

---

## Task 9: `old-irish.rules [substitute]` — the retro-filter

**Depends on:** Tasks 6, 8. **Spec:** §4, §11. O-13, O-15. **Review:** R10–R18, S3, S13, S14,
S16, S19.

**Files:** modify `rules/old-irish.rules`; append to `tests/test_rules_old_irish.py`.

**What spec §11 removed.** The strand takes the **citation form**, so there is **no reversal of
modern lenition or eclipsis**. Draft 1's `LEN:`/`ECL:` rules (R14, R15) are gone with Task 7. The
aligner still carries the eclipsis units, because a *corpus row* may be spelled *mbean* — such a row
is a RETRO miss and must still align — but no rule here reverses a mutation.

**Rules, all with quality-preserving pairs** (R11 — this is the fix that makes the section
executable):

| Rule | Reading |
|---|---|
| `[BROAD orth="bh"] -> β` / `[SLEN orth="bh"] -> βʲ` | modern *bh* → lenited *b*. Attested pair: *dubh ~ dub*, *sliabh ~ slíab* |
| `[BROAD orth="mh"] -> β̃` / `[SLEN orth="mh"] -> β̃ʲ` | modern *mh* → lenited *m*. *lámh ~ lám*, *Domhnall ~ Domnall*. **S16:** *naomh ~ noíb* and *claíomh ~ claideb* are attested rows where modern ⟨mh⟩ descends from Old Irish ⟨b⟩ — the split is a good default, not a law; say so in the comment |
| `[BROAD orth="dh"] -> ð` / `[SLEN orth="dh"] -> ðʲ` | *adharc ~ adarc* |
| `[BROAD orth="gh"] -> ɣ` / `[SLEN orth="gh"] -> ɣʲ` | *Lughaidh ~ Lugaid* |
| `[BROAD orth="th"] -> θ` / `[SLEN orth="th"] -> θʲ` | *cath ~ cath*, *bláth ~ bláth* — **identity in spelling**; the rule exists to fix the segment as /θ/ |
| `[BROAD orth="ch"] -> x` / `[SLEN orth="ch"] -> ç` | *cloch ~ cloch* |
| `[BROAD orth="ph"] -> fˠ` / `[SLEN orth="ph"] -> fʲ` | **no attested pair** — ⟨ph⟩ and ⟨sh⟩ do not occur in any of the 270 attested modern keys (log finding 3), so these two branches stay `%design` and untested by the regression. **Say that in the comment** so the silence is not read as coverage |
| `[BROAD orth="sh"] -> h` / `[SLEN orth="sh"] -> h` | ditto |
| `@orth("ao") -> a i` (two segments) | O-13. **R13:** draft 1 produced a single `aː`, which respells as ⟨á⟩ and made ⟨áe⟩ unwritable. The pair `a i` is the O-28 value of ⟨áe⟩/⟨aí⟩, and Task 11 writes it ⟨áe⟩ |
| `@orth("ia:1") -> i`, `@orth("ia:2") -> a` | **R12:** positional tags make "the first element only" expressible. *iasc ~ íasc*, *grian ~ grían*, *Niall ~ Níall* — 33 pairs |
| `@orth("ua:1") -> u`, `@orth("ua:2") -> a` | *tuath ~ túath*, *cluas ~ clúas* |
| `[V +long orth="ea"] -> eː` / `[V -long orth="ea"] -> e` | **The largest class: 50 attested pairs** (log finding 2). Modern *caol le caol* brackets the vowel; Old Irish marks quality by the *following* vowel only (digest §10.2.5). *fear ~ fer*, *bean ~ ben*, *dearg ~ derg*. **R11:** the length split is required — draft 1's single `-> e` shortened long vowels, violating spec §4's non-reversal list. **S14:** these *are* segment changes and must be; the earlier prose saying otherwise is withdrawn |
| the same two-line shape for `orth="io"` → `i`/`iː`, `orth="ai"` → `a`/`aː`, `orth="oi"` → `o`/`oː`, `orth="ui"` → `u`/`uː` | **R10:** `ai` is now a real unit of the aligner table, so this rule is live |
| `ɪ -> i`, `ʊ -> u`, `ɛ -> e`, `ɔ -> o` | digest §10.1's five short vowels |
| `@orth("r:2") -> 0`, `@orth("l:2") -> 0`, `@orth("n:2") -> 0`, `@orth("m:2") -> 0` | **the epenthetic schwa, identified by spelling** — the aligner tags it as the second segment of a single sonorant letter (*gorm* → `g o r:1 r:2 m`). Precise, and it fires only where the spelling shows no vowel. spec §8 row O5 |
| `ə -> 0 / SONORANT _ C` | the same rule for **untagged** words (O-15, digest §2.4), so an unaligned word still loses its epenthesis |
| `w -> β`, `vˠ -> β`, `vʲ -> βʲ` | any survivor of the digraph rules; /w/ is not an Old Irish phoneme (S6) |
| **no rule** for vowel length, cluster shape or consonant quality | spec §4's explicit non-reversal list |
| **no rule** deleting a final vowel | log finding 4: final unstressed vowels survive into Old Irish (*cara ~ carae*). The **ending marker** of spec §11 is written by Task 11, not here |

**Tags and citations (R17).** Draft 1 asserted that every line is `%design`, which contradicts
spec §4 ("`%design` **unless a lexicon pair instantiates the change**"). A line that a lexicon pair
instantiates is `%attested` **and cites the pair**; ⟨ph⟩/⟨sh⟩ and the ⟨ao⟩ default stay `%design`.
The test asserts *a citation on every line*, not a tag.

**Test fixtures must be real lexicon pairs (R18).** Draft 1 used *bád* and *garda* — a `none` row
and a non-lexicon word — and `sʲaːnˠ`, which is not a `features.tsv` segment. Every fixture below is
an `attested` lexicon row.

- [ ] **Step 1: Write the failing tests** — append:

```python
from helpers import irish
from strands.irish import normalize
from strands.orth import tag_word
from strands.substitute import substitute_stage

IRISH = irish()


def retro(ipa, orthography=""):
    word = normalize(w(ipa), IRISH, TABLE)
    if orthography:
        word = tag_word(word, orthography)
    return substitute_stage(word, OI, TABLE).segments


@pytest.mark.parametrize("orthography,ipa,index,expected", [
    ("dubh",   "d̪ˠʊw",   -1, "β"),      # dubh ~ dub
    ("sliabh", "ʃlʲiəw",  -1, "β"),      # sliabh ~ slíab
    ("lámh",   "l̪ˠaːw",  -1, "β̃"),      # lámh ~ lám
    ("adharc", "əiɾˠk",   None, None),   # adharc ~ adarc (see the next test)
    ("cloch",  "kl̪ˠɔx",  -1, "x"),      # cloch ~ cloch
    ("bláth",  "bˠl̪ˠaː", None, None),
])
def test_the_lenition_digraphs_map_to_the_lenited_series(orthography, ipa, index, expected):
    """R18: every fixture is an `attested` lexicon row. Log finding 3: ~49 pairs."""
    if expected is None:
        pytest.skip("covered by the class test below")
    assert retro(ipa, orthography)[index] == expected


def test_the_reversal_keeps_quality():
    """R11: draft 1's single broad replacement flattened slender ⟨bh ch th⟩ to broad."""
    assert retro("vʲiː", "bhí")[0] == "βʲ"
    assert retro("ˈcaːn̪ˠ", "cheann")[0] == "ç"


def test_the_reversal_keeps_vowel_length():
    """spec §4's non-reversal list; R11: draft 1's `@orth("ea") -> e` shortened /aː/."""
    out = retro("bʲaːn̪ˠ", "beann")
    assert "eː" in out and "e" not in out or "eː" in out


def test_the_quality_digraph_class_deletes_the_glide_and_keeps_the_sound():
    """Log finding 2, 50 pairs — the largest class, and invisible to any sound-based rule."""
    assert retro("bʲanˠ", "bean")[1] == "e"          # bean ~ ben
    assert retro("dʲaɾˠəɡ", "dearg")[1] == "e"       # dearg ~ derg
    assert retro("fʲɪn̪ˠ", "fionn")[1] == "i"        # Fionn ~ Finn


def test_modern_ao_becomes_the_two_segment_digraph():
    """R13: a single `aː` is unwritable as ⟨áe⟩. O-13 / spec §8 row O1."""
    assert retro("iːnˠ", "aon")[:2] == ("a", "i")    # aon ~ óen/áen


def test_ua_and_ia_lengthen_the_first_element_only():
    """R12: positional tags. *tuath ~ túath*, *iasc ~ íasc* — 33 pairs."""
    assert retro("t̪ˠuəx", "tuath")[1:3] == ("u", "a")
    assert retro("iəsˠk", "iasc")[:2] == ("i", "a")


def test_the_epenthetic_schwa_is_deleted_by_its_spelling():
    """spec §8 row O5. The aligner tags it `r:2` (Task 5), so the rule is exact."""
    assert retro("ɡɔɾˠəmˠ", "gorm") == ("ɡ", "o", "ɾˠ", "mˠ")


def test_an_unaligned_word_still_loses_its_epenthesis_and_stays_in_inventory():
    """O-7/O-15: no tags, so only the sound-based half applies — and it must still work."""
    out = retro("ɡɔɾˠəmˠ")
    assert set(out) <= set(OI.inventory) and "ə" not in out and "ɔ" not in out


@pytest.mark.parametrize("orthography,ipa", [
    ("athair", "ˈahəɾʲ"), ("máthair", "ˈmˠaːhəɾʲ"), ("bráthair", "ˈbˠɾˠaːhəɾʲ"),
    ("arán", "əˈɾˠaːnˠ"), ("Colmán", "ˈkɔl̪ˠəmˠaːnˠ"),
])
def test_the_invariant_classes_are_left_alone(orthography, ipa):
    """S19 / log finding 4: the r-stem kinship set and the ⟨-án⟩ diminutive are
    spelling-invariant across both stages — the best 'does the filter over-apply' cases."""
    out = retro(ipa, orthography)
    assert set(out) <= set(OI.inventory)
    assert "ə" not in out[-2:]


def test_a_negative_control_shows_the_section_is_actually_doing_the_work():
    """S13: draft 1's identity assertions passed with no [substitute] section at all."""
    assert retro("d̪ˠʊw", "dubh") != retro("d̪ˠʊw")


def test_every_substitute_line_carries_a_citation_and_a_legal_tag():
    """R17: spec §4 allows %attested where a lexicon pair instantiates the rule."""
    for rule in OI.sections["substitute"]:
        assert rule.tag in ("attested", "design"), (rule.line, rule.tag)
        assert rule.comment.strip(), rule.line
```

- [ ] **Step 2:** run → FAIL (`KeyError: 'substitute'`).
- [ ] **Step 3:** write the section in this order: (a) the digraph pairs; (b) ⟨ao⟩; (c) the
      positional ⟨ia ua⟩ rules; (d) the quality-digraph pairs; (e) the lax-vowel collapses;
      (f) the tagged epenthesis deletions, then the untagged one; (g) the `w`/`vˠ`/`vʲ` sweep.
      **S3:** do not write `ea -> ɑ` or `a -> ɑ` — `irish.rules [normalize]` folds `ɑ → a`, so they
      can never match.
- [ ] **Step 4:** `uv run pytest tests/test_rules_old_irish.py -q` → PASS;
      `uv run strands check rules/old-irish.rules` → exit 0 (an `ORTH_UNKNOWN_UNIT` **error** names
      a unit missing from `rules/irish-orthography.tsv`; add it there, do not silence it).
- [ ] **Step 5:** `uv run pytest -q` → green. **Commit:**
      `feat(rules): old-irish [substitute] — quality-preserving, spelling-driven retro-filter`

**Acceptance:** the digraph reversals keep quality and length; the quality-digraph class fires on
real pairs; ⟨ao⟩ yields two segments; ⟨ia ua⟩ change only their first element; the epenthetic schwa
goes by its spelling and by sound; the invariance cases are untouched; the negative control passes;
every line cites something.

---

## Task 10: `[syllable]`, `[repair]`, `[stress]`, `[post-stress]`

**Depends on:** Task 9. **Spec:** §4; engine §12.B, §12.E. O-20, O-28. **Review:** R19, S12.

**Files:** modify `rules/old-irish.rules`; append to `tests/test_rules_old_irish.py`.

```
[syllable]
# spec §4: template `any`, sonority off — "Old Irish tolerates the modern cluster set"
# (digest §10). No onset/coda whitelist exists for Old Irish in the held sources.
template = any
onsets   = any
codas    = any
sonority = off
domain   = word
# spec §12.B: a diphthong is two segments and ONE nucleus. The eight are Pokorny's
# [pokorny1914-oldirish-grammar p.6 §4]; the VALUES are `wiki-old-irish` §Vowels' (O-28/R19):
# ai oi ui au eu iu ia ua. Draft 1's `aːi`/`iə` contradicted digest §10.8 conflict 5, which
# quotes Pokorny writing ⟨aí⟩ PRECISELY to distinguish it from long ⟨á⟩ plus a palatal glide.
# CONFLICT: digest §10.6's *Goídelc* [ˈɡoːi̯ðʲelɡ] infobox transcription implies ⟨oí⟩ = /oːi̯/;
# recorded, not generalized from.
# `əi əu` are carried so the filter can pass a modern diphthong through (*Tadhg* /t̪ˠəiɡ/).
nuclei = ai oi ui au eu iu ia ua əi əu

[repair]
# spec §4: "none beyond degemination". O-20 / §12.E: an unattested cluster is KEPT and
# flagged UNATTESTED_CLUSTER, never rewritten — this strand has no whitelist to fall back on.
cluster-fallback = keep
# Degemination over repeated segments (I-2), OBSTRUENTS ONLY: digest §10.2 conv. 3 makes
# ⟨ll nn rr mm⟩ the fortis spelling (O-2), so degeminating a sonorant would erase the
# contrast the orthography carries.
<one `X X -> X` line per obstruent, each citing digest §10.2 conv. 3>

[stress]
# digest §10.3: "Stress is generally on the first syllable" [wiki-old-irish §Stress]; for
# names, "including in nominal compounds" [utaustin-oldirish-lesson1 §1.2].
procedure = initial
mark = on

[post-stress]
# spec §4: "unstressed vowels are not reduced (unlike modern Irish)" — deliberately EMPTY.
# digest §10.2's unstressed-vowel grid is a SPELLING matter and lives in the grapheme table
# (Task 7) and [respell] (Task 11), not here.
```

- [ ] **Step 1: Write the failing tests** — append (note S12: no `or`-joined assertions):

```python
from strands.repair import repair
from strands.stress import assign_stress
from strands.syllabify import syllabify


def phon(ipa):
    return assign_stress(repair(syllabify(w(ipa), OI, TABLE), OI, TABLE), OI, TABLE)


def test_the_syllable_spec_is_permissive_and_word_domain():
    s = OI.syllable
    assert s.template is None and s.onsets is None and s.codas is None
    assert s.sonority is False and s.domain == "word" and s.bans == ()


def test_the_nuclei_are_the_wiki_old_irish_values_plus_the_two_modern_pass_throughs():
    """O-28 / R19."""
    assert {"".join(n) for n in OI.syllable.nuclei} == {
        "ai", "oi", "ui", "au", "eu", "iu", "ia", "ua", "əi", "əu"}


def test_a_diphthong_is_one_syllable():
    """S12: draft 1's version was an `or` of two assertions over a nucleus not in the list."""
    assert len(phon("tuaθ").syllables) == 1
    assert len(phon("kaix").syllables) == 1


def test_an_unattested_cluster_is_kept_and_flagged_never_repaired():
    assert OI.cluster_fallback == "keep"
    out = phon("sˠt̪ˠɾˠai")
    assert "UNREPAIRED" not in out.flags and out.segments[:3] == ("sˠ", "t̪ˠ", "ɾˠ")


def test_obstruent_geminates_degeminate():
    assert phon("abˠbˠ").segments.count("bˠ") == 1


def test_sonorant_geminates_are_left_alone_because_they_spell_fortis():
    """digest §10.2 conv. 3 / O-2: ⟨ll nn rr mm⟩ = /L N R m/."""
    assert phon("kol̪ˠl̪ˠ").segments.count("l̪ˠ") == 2


def test_stress_is_initial():
    assert phon("konˠxoβaɾˠ").stress == 0


def test_unstressed_vowels_are_not_reduced():
    assert OI.sections.get("post-stress", ()) == ()
    assert "a" in phon("konˠal̪ˠ").segments
```

- [ ] **Step 2–4:** run → FAIL on the nuclei set; **delete the `TEMPORARY` block entirely** and
      grep for the word `TEMPORARY` afterwards; re-run; `uv run pytest -q` → green.
- [ ] **Step 5: Commit** — `feat(rules): old-irish syllable (O-28 nuclei), cluster-keep repair, initial stress`

**Acceptance:** the ten nuclei are exactly the O-28 set; a diphthong is one syllable in two
positive assertions; unattested clusters are kept and flagged; obstruent geminates reduce and
sonorant ones do not; stress is initial; `[post-stress]` is empty with a reason; no `TEMPORARY`
block survives.

---
## Task 11: `old-irish.rules [respell]` — editorial Old Irish orthography

**Depends on:** Task 10. **Spec:** §6, §11; digest §10.2 conv. 1–6. **Review:** R16, R27, R29c,
R29d, S21.

**Files:** modify `rules/old-irish.rules`; append to `tests/test_rules_old_irish.py`.

**What this section is now.** It is the **only** producer of a spelled word on the RETRO path:
`respell()` returns a string, and Task 12 hands that string to `SpelledWord.from_spelling`. So
every character it emits must be a grapheme token of `rules/old-irish-orthography.tsv` — a
property test asserts exactly that, which is the check draft 1 lacked (R27: draft 1's `[respell]`
fixtures and Task 12's reconstruction fixtures used *different alphabets*).

**Rule order** — this is the list to follow (R29c: draft 1's list and the sentence after it
disagreed, and the list is what an implementer follows):

1. **Nasal + stop guards.** `bˠ -> "b" / mˠ _`, `d̪ˠ -> "d" / n̪ˠ _`, `ɡ -> "g" / ŋ _`, so the
   conv. 2 table below cannot write *mp*. digest §10.4.
2. **Unwritten lenition** (digest §10.2 conv. 1): `β βʲ -> "b"`, `ð ðʲ -> "d"`, `ɣ ɣʲ -> "g"`,
   `β̃ β̃ʲ -> "m"`. **There is no ⟨bh dh gh mh⟩ in Old Irish** — "the single biggest visual
   difference between an Old Irish and a Modern Irish name", and the log's largest reversal class.
3. **Written lenition:** `x ç -> "ch"`, `θ θʲ -> "th"`, `fˠ fʲ -> "ph"` **only where the source was
   ⟨ph⟩** (`[C orth="ph"]`), else `"f"`; `h -> "ṡ"` where the source was ⟨sh⟩, else `"h"`.
4. **Diphthongs, before the single-vowel rules** (I-19 makes each match an opaque chunk, so a
   claimed diphthong cannot be re-matched): `a i -> "áe"` (O-13: the filter's ⟨ao⟩ default; the
   lexicon uses both ⟨áe⟩ and ⟨aí⟩ and this is the one the filter writes), `o i -> "oí"`,
   `u i -> "uí"`, `a u -> "áu"`, `e u -> "éu"`, `i u -> "íu"`, `i a -> "ía"`, `u a -> "úa"`,
   `ə i -> "aí"`, `ə u -> "áu"`.
5. **Length:** `aː -> "á"`, `eː -> "é"`, `iː -> "í"`, `oː -> "ó"`, `uː -> "ú"`.
6. **conv. 2 doubling** (digest §10.2 conv. 2–3 — the rule that restores *mac → macc* **without a
   lexical list**):

   | segment | initial | non-initial |
   |---|---|---|
   | `k`/`c` | `"c"` | `"cc"` |
   | `t̪ˠ`/`tʲ` | `"t"` | `"tt"` |
   | `pˠ`/`pʲ` | `"p"` | `"pp"` |
   | `ɡ`/`ɟ` | `"g"` | `"c"` |
   | `d̪ˠ`/`dʲ` | `"d"` | `"t"` |
   | `bˠ`/`bʲ` | `"b"` | `"p"` |

7. **Sonorant geminates:** `l̪ˠ l̪ˠ -> "ll"` and the `nn rr mm` equivalents, with their slender
   partners. **R16, stated honestly:** nothing upstream produces two identical sonorant segments —
   modern Irish has no geminates — so these rules fire only on a lexicon-sourced word, never on a
   filter output. *ainm → ainmm*, *cill → cell*, *bainne → bannae*, *Neasa → Nessa* are therefore
   **not derivable** and are lexicon-only. Draft 1 promised the class and delivered half of it;
   write the comment that says which half.
8. **The §36 glide** (digest §10.2 conv. 5): insert `"i"` before a word- or syllable-final slender
   consonant — `0 -> "i" / [V] _ [SLEN] #` and the syllable-final variant — **blocked** after
   ⟨í é⟩ and after a diphthong. **S20:** Pokorny's stated exception list is *í, é, aí, oí, uí*;
   draft 1's `[V -front]` additionally blocked after short ⟨e⟩ and ⟨i⟩, which no source states.
   Block after ⟨i⟩ (it is already an ⟨i⟩) and after the long/diphthong set; do not block after ⟨e⟩.
9. **Word-final /ə/ is the ENDING MARKER** (spec §11): `ə -> "ə" / _ #`. It is a grapheme token
   (Task 7) with an empty reconstruction, and Task 14's `NOM_A`/`NOM_O` realize it by stem class.
   **This is spec §11's "unresolved ending marker", and it is why draft 1's dead
   `ə -> a` + identity-`NOM_A` combination (GPT #8) is gone.** A property test asserts no *finished*
   output contains it.
10. **The post-stress /ə/ grid** (conv. 5 — "the vowel letter has no relation to the etymological
    vowel"): non-final `ə` is `"a"` broad→broad, `"ai"` broad→slender, `"e"` slender→broad,
    `"i"` slender→slender.
11. **Identity fallback** (S21): the short vowels `a e i o u`, `sˠ ʃ`, `l̪ˠ lʲ n̪ˠ nʲ ɾˠ ɾʲ mˠ mʲ`,
    `fˠ fʲ`, `ŋ ɲ` pass through as their letters. Rule 6's neighbours are all explicit, so write
    these explicitly too rather than relying on the stage's pass-through.
12. **No *h*-prefix** (spec §6; conv. 6). A comment records the deliberate absence.

- [ ] **Step 1: Write the failing tests** — append (R27: every fixture uses **inventory**
      segments, and the round-trip is now `respell → SpelledWord → reconstruct`, in that one
      direction only, per O-11):

```python
from strands.respell import respell
from strands.spelled import SpelledWord, spelling_to_ipa
from strands.word import Word


def spell(*segments):
    return respell(Word(segments=segments), OI, TABLE)


def test_lenited_b_d_g_m_are_written_unmarked():
    """digest §10.2 conv. 1 — the largest visual difference from a modern name."""
    assert spell("d̪ˠ", "u", "β") == "dub"
    assert spell("l̪ˠ", "aː", "β̃") == "lám"
    assert spell("a", "ð", "a", "ɾˠ", "k") == "adarc"


def test_lenited_voiceless_stops_are_written_with_h():
    assert spell("k", "l̪ˠ", "o", "x") == "cloch"
    assert spell("bˠ", "l̪ˠ", "aː", "θ") == "bláth"


def test_non_initial_voiceless_stops_are_doubled_and_voiced_ones_are_written_c_t_p():
    """digest §10.2 conv. 2-3 — this restores *mac -> macc* with no lexical list."""
    assert spell("mˠ", "a", "k") == "macc"
    assert spell("bʲ", "e", "ɟ") == "bec"
    assert spell("bˠ", "ɾˠ", "a", "t̪ˠ") == "bratt"
    assert spell("bˠ", "ɾˠ", "o", "d̪ˠ") == "brot"


def test_a_nasalized_stop_is_not_devoiced_by_the_doubling_rule():
    assert spell("mˠ", "bˠ", "oː") == "mbó"
    assert spell("ŋ", "ɡ", "a") == "nga"


def test_the_eight_diphthongs_and_the_ao_default():
    for segments, expected in [(("a", "i"), "áe"), (("o", "i"), "oí"), (("u", "i"), "uí"),
                               (("a", "u"), "áu"), (("e", "u"), "éu"), (("i", "u"), "íu"),
                               (("i", "a"), "ía"), (("u", "a"), "úa")]:
        assert spell(*segments) == expected


def test_the_glide_i_marks_a_final_slender_consonant():
    """digest §10.2 conv. 5 §36."""
    assert spell("mˠ", "u", "ɾʲ") == "muir"


def test_no_glide_is_written_before_a_broad_consonant():
    assert spell("fʲ", "e", "ɾˠ") == "fer"


def test_the_post_stress_schwa_grid():
    assert spell("dʲ", "iː", "ɣ", "ə", "l̪ˠ") == "dígal"
    assert spell("dʲ", "iː", "ɣ", "ə", "lʲ") == "dígail"
    assert spell("dʲ", "lʲ", "i", "ɣʲ", "ə", "ð") == "dliged"
    assert spell("dʲ", "lʲ", "i", "ɣʲ", "ə", "ðʲ") == "dligid"


def test_a_word_final_schwa_becomes_the_ending_marker():
    """spec §11: the retro-filter leaves it UNRESOLVED; Task 14 realizes it by stem class."""
    assert spell("k", "a", "ɾˠ", "ə").endswith("ə")


def test_every_respell_output_is_tokenizable_as_a_spelled_word():
    """R27: draft 1's [respell] and reconstruction used different alphabets. This is the
    property that keeps them one system."""
    for segments in [("d̪ˠ", "u", "β"), ("mˠ", "a", "k"), ("k", "l̪ˠ", "o", "x"),
                     ("mˠ", "u", "ɾʲ"), ("dʲ", "iː", "ɣ", "ə", "l̪ˠ"), ("a", "i"),
                     ("k", "a", "ɾˠ", "ə")]:
        text = spell(*segments)
        assert SpelledWord.from_spelling(text).render() == text, text


def test_no_h_prefix_is_ever_written():
    assert not spell("eː", "n̪ˠ").startswith("h")
```

- [ ] **Step 2–4:** run → FAIL; write the section in the order 1…12 above; re-run;
      `uv run strands check` → clean; `uv run pytest -q` → green.
- [ ] **Step 5: Commit** — `feat(rules): old-irish [respell] — unwritten lenition, conv.2 doubling, ending marker`

**Acceptance:** lenited *b d g m* unmarked and *ch th* written; the conv. 2 contrast holds both
ways; the eight diphthongs and the ⟨áe⟩ default are written; the §36 glide fires and §39 does not;
the schwa grid reproduces the digest's four examples; a final schwa becomes the ending marker;
**every output tokenizes as a spelled word**; no *h*-prefix.

---

## Task 12: Lookup stage, flags, and `oldirish.run_entry_oi`

**Depends on:** Tasks 2, 7, 11. **Spec:** §2, §6, §11. O-9, O-11, O-12, O-17, O-22, O-23, O-33.
**Review:** R30, R31d.

**Files:** modify `src/strands/pipeline.py`; create `src/strands/oldirish.py`; test
`tests/test_oldirish_lookup.py`.

**Interfaces:**

```python
# pipeline.py
TARGETS = ("welsh", "arabic-egy", "georgian", "dutch", "old-irish")

def lookup(entry: Entry, lexicon: dict[str, LexEntry]) -> LexEntry | None:
    """Stage 1b (spec §2, O-9, O-23): exact match of `entry.orthography` — the CITATION form
    — after NFC + casefold. No de-mutation, no fuzzy fallback."""

# run_entry(), first action after parse_construction:
#     if target.meta.get("strand", "") == "old-irish":        # O-9
#         from .oldirish import run_entry_oi
#         return run_entry_oi(entry, construction, irish, target, table, slots=slots)

# oldirish.py
OI_FLAGS = ("ATTESTED", "ATTESTED:MIr", "RETRO", "RETRO:loan", "RETRO:late")

class ConstructionNotInStrand(PipelineError): ...

@dataclass(frozen=True)
class Stem:
    words: tuple[SpelledWord, ...]     # the Old Irish nominative, one per space-separated word
    gen: tuple[SpelledWord, ...] | None    # the attested genitive, when the lexicon gave one
    stem: str                          # a lexicon.STEMS value, looked up or inferred
    gender: str
    flag: str
    assumptions: tuple[str, ...]
    trace: tuple[TraceEntry, ...]

def infer_stem(entry: Entry) -> tuple[str, str]          # (stem, assumption tag)
def to_old_irish(entry, lexicon, oi, irish, table) -> Stem
def adapt_oi(words: Sequence[SpelledWord], oi, table, *, assumptions=(), flags=(), trace=()) -> Result
def run_entry_oi(entry, construction, irish, oi, table, *, lexicon=None, slots=None) -> Result
```

**The fork (spec §2 steps 1–2).**

| lexicon row | what happens | flag |
|---|---|---|
| `attested` | `spelling_to_words(row.oi_nom)`; `oi_gen` → `gen` when non-empty; `stem`/`gender` from the row. **No `[substitute]`, no `[respell]`.** | `ATTESTED` |
| `middle` | identical (O-22) | `ATTESTED:MIr` |
| `none` | retro-filter, exactly as a miss (O-12) | `RETRO:{row.kind}` |
| no row | retro-filter | `RETRO` |

**The retro path**, in order: `tokenize(entry.ipa)` → `Word.from_tokenized` → `irish.normalize` →
`orth.tag_word(word, entry.orthography)` → `substitute_stage(…, oi, …)` → `syllabify` → `repair` →
`assign_stress` → `post_stress` → `respell` → `SpelledWord.from_spelling(that string)`. Capitalize
from `entry.orthography[:1].isupper()` (O-32). The pre-reconstruction phonology survives as the
`respell` trace entry's `before`.

**`infer_stem` (O-21, O-33, S22).** Reads `Entry.declension` (committed, 77b1ff7):

| modern | Old Irish `stem` | assumption tag |
|---|---|---|
| `m1` | `o` | `stem:from-declension-m1` |
| `f2` | `ā` | `stem:from-declension-f2` |
| `ach` | `o` | `stem:from-declension-ach` |
| `m3`, slender-final | `i` | `stem:from-declension-m3-slender` |
| `m3`, otherwise | `u` | `stem:from-declension-m3-broad` |
| `d4` | `indecl` | `stem:from-declension-d4` |
| empty/unknown, `gender = f` | `ā` | `stem:default-by-gender-f` |
| empty/unknown, otherwise | `o` | `stem:default-by-gender-m` |

**R31d / O-33:** a lexicon row with a **blank** `stem` is *not* a supplied class — it routes through
`infer_stem` and is tagged. Measured: 63 `attested` rows are in that state today (Task 3 reduces
it). Only a **non-empty** lexicon class is silent.

**`adapt_oi` (O-9, O-11).** Per word: apply nothing further — the spelled word is finished by the
time it arrives — then `render(punctum=…)`, join with single spaces, and
`ipa = " ".join("".join(spelling_to_ipa(word)) for word in words)`. **GPT P2:** segments are joined
with **no separator inside a word**; only words are separated. `punctum` is applied to the string
*before* reporting, and to nothing else (O-14).

**`DESC+ADJ` / `DESC+NOUN` (R30).** `run_entry_oi` calls `parse_construction`, gets the slot, and —
because Task 8 declares no `epithet-*` keys — resolves it to "no affix", recording
`epithet:{SLOT}-unmapped-in-Old Irish`. So **`DESC+ADJ` equals `DESC`** except for that assumption,
and a test asserts the equality. Draft 1 never mentioned `parse_construction` in `run_entry_oi`, so
`--construction all` and the gallery would have exercised an unhandled path.

**Scope until Task 15.** `oi.templates` is empty until Task 15, so this task supports `DESC`
(and its two slot forms) and raises `ConstructionNotInStrand` for every other name, with a
`# Task 15` comment. That gap is visible, not silent.

- [ ] **Step 1: Write the failing tests** — `tests/test_oldirish_lookup.py`:

```python
"""Task 12: the lookup stage and the Old Irish assembly (spec §2, §6, §11)."""
import pytest

from helpers import TABLE, irish, target
from strands.inputs import Entry, infer
from strands.lexicon import key, read_lexicon
from strands.oldirish import (OI_FLAGS, ConstructionNotInStrand, infer_stem, run_entry_oi,
                              to_old_irish)
from strands.pipeline import TARGETS, load_target, lookup, run_entry
from strands.spelled import SpelledWord, spelling_to_ipa

IRISH = irish()
OI = target("old-irish")
LEX = read_lexicon()


def entry(orthography, ipa, **kw):
    return infer(Entry(orthography=orthography, ipa=ipa, **kw), IRISH, TABLE)


def test_old_irish_is_the_fifth_target():
    assert TARGETS == ("welsh", "arabic-egy", "georgian", "dutch", "old-irish")
    assert load_target("old-irish", TABLE).meta["strand"] == "old-irish"


def test_lookup_matches_the_citation_form_exactly():
    """O-19, O-23: no fuzzy matching, no de-mutation. A surface form is a MISS."""
    assert lookup(entry("Niall", "nʲiəl̪ˠ"), LEX) is not None
    assert lookup(entry("NIALL", "nʲiəl̪ˠ"), LEX) is not None
    assert lookup(entry("a Sheáin", "ə çaːnʲ"), LEX) is None


def test_an_attested_row_supplies_the_spelling_and_the_filter_never_runs():
    """spec §2 step 1 / §11: lookup yields the attested spelling directly, no conversion."""
    stem = to_old_irish(entry("Niall", "nʲiəl̪ˠ"), LEX, OI, IRISH, TABLE)
    assert stem.flag == "ATTESTED"
    assert stem.words[0].render() == LEX[key("Niall")].oi_nom


def test_a_loan_and_a_late_coinage_are_filtered_and_flagged_apart():
    loan = to_old_irish(entry("Seán", "ʃaːnˠ"), LEX, OI, IRISH, TABLE)
    late = to_old_irish(entry("Saoirse", "ˈsˠiːɾˠʃə"), LEX, OI, IRISH, TABLE)
    assert loan.flag == "RETRO:loan" and late.flag == "RETRO:late"
    assert loan.words and late.words


def test_a_miss_is_a_plain_retro():
    assert to_old_irish(entry("Splancarnach", "sˠpˠl̪ˠaŋkəɾˠnˠəx"), LEX, OI, IRISH,
                        TABLE).flag == "RETRO"


@pytest.mark.parametrize("declension,gender,expected", [
    ("m1", "m", "o"), ("f2", "f", "ā"), ("ach", "m", "o"), ("d4", "m", "indecl"),
    ("", "f", "ā"), ("", "m", "o"),
])
def test_the_stem_class_is_inferred_from_the_declension_then_the_gender(declension, gender,
                                                                       expected):
    """spec §4 / O-21 / S22: draft 1 defaulted an unclassified feminine to `o`."""
    stem, reason = infer_stem(entry("Xyz", "sˠiː", declension=declension, gender=gender))
    assert stem == expected and reason.startswith("stem:")


def test_a_blank_lexicon_stem_is_inferred_and_reported_not_silently_guessed():
    """R31d / O-33: measured, 63 attested rows are in this state."""
    blank = [k for k, r in LEX.items() if r.status == "attested" and not r.stem]
    if not blank:
        pytest.skip("Task 3 filled every stem")
    row = LEX[blank[0]]
    result = run_entry_oi(entry(row.orthography, "sˠiː"), "DESC", IRISH, OI, TABLE)
    assert any(a.startswith("stem:") for a in result.assumptions)


def test_every_result_carries_exactly_one_of_the_five_flags():
    for orthography, ipa in [("Niall", "nʲiəl̪ˠ"), ("Seán", "ʃaːnˠ"),
                             ("Splancarnach", "sˠpˠl̪ˠaŋkəɾˠnˠəx")]:
        result = run_entry_oi(entry(orthography, ipa), "DESC", IRISH, OI, TABLE)
        assert len([f for f in result.flags if f in OI_FLAGS]) == 1, result.flags


def test_the_ipa_is_reconstructed_from_the_finished_written_form():
    """spec §6, §11 / O-11 — and GPT P2: no separator inside a word."""
    result = run_entry_oi(entry("Niall", "nʲiəl̪ˠ"), "DESC", IRISH, OI, TABLE)
    rebuilt = " ".join("".join(spelling_to_ipa(SpelledWord.from_spelling(p)))
                       for p in result.respelling.split(" "))
    assert result.ipa == rebuilt
    assert "  " not in result.ipa


def test_punctum_off_changes_the_respelling_and_not_the_ipa():
    """O-14 / spec §11: a rendering option applied AFTER reconstruction."""
    from dataclasses import replace as _replace
    off = _replace(OI, meta={**OI.meta, "punctum": "off"})
    a = run_entry_oi(entry("Sean-", "ʃanˠ"), "DESC", IRISH, OI, TABLE)
    b = run_entry_oi(entry("Sean-", "ʃanˠ"), "DESC", IRISH, off, TABLE)
    assert a.ipa == b.ipa


def test_run_entry_dispatches_on_the_meta_strand_key():
    a = run_entry(entry("Niall", "nʲiəl̪ˠ"), "DESC", IRISH, OI, TABLE)
    b = run_entry_oi(entry("Niall", "nʲiəl̪ˠ"), "DESC", IRISH, OI, TABLE)
    assert a == b


def test_an_epithet_slot_this_strand_does_not_map_is_no_affix():
    """R30 / O-17: `DESC+ADJ` must equal `DESC`, with an assumption saying why."""
    plain = run_entry_oi(entry("Niall", "nʲiəl̪ˠ"), "DESC", IRISH, OI, TABLE)
    slotted = run_entry_oi(entry("Niall", "nʲiəl̪ˠ"), "DESC+ADJ", IRISH, OI, TABLE)
    assert slotted.respelling == plain.respelling and slotted.ipa == plain.ipa
    assert any("unmapped" in a for a in slotted.assumptions)


def test_a_construction_this_strand_does_not_have_raises_not_crashes():
    with pytest.raises(ConstructionNotInStrand):
        run_entry_oi(entry("Niall", "nʲiəl̪ˠ"), "PATRO_O", IRISH, OI, TABLE)


def test_a_multi_word_attested_form_becomes_several_words():
    row = LEX.get(key("Cú Chulainn"))
    if row is None:
        pytest.skip("no multi-word row in the lexicon")
    assert len(to_old_irish(entry("Cú Chulainn", "kuː xʊl̪ˠənʲ"), LEX, OI, IRISH,
                            TABLE).words) == 2


def test_the_result_is_deterministic():
    e = entry("Niall", "nʲiəl̪ˠ")
    assert run_entry_oi(e, "DESC", IRISH, OI, TABLE) == run_entry_oi(e, "DESC", IRISH, OI, TABLE)
```

- [ ] **Step 2–4:** run → FAIL (`cannot import name 'lookup'`); extend `pipeline.py`; write
      `oldirish.py`; re-run.
- [ ] **Step 5:** `uv run pytest -q`. **`test_properties.py` and `test_cli.py` parametrize over
      `TARGETS`, so the fifth target now runs through them.** Anything that fails only because
      `[templates]` is empty gets `xfail(strict=False)` with the reason
      `"old-irish templates land in Task 15"` — **and Task 15 deletes the marks.** Do not weaken an
      assertion.
- [ ] **Step 6: Commit** — `feat(oldirish): lookup stage, ATTESTED/RETRO flags, spelled-word assembly`

**Acceptance:** the five flags are exclusive and correct; lookup is exact on the citation form; an
attested row's spelling is used verbatim; the stem inference is reported, including for blank
lexicon stems; `Result.ipa` is reconstructed from the finished written form with no intra-word
separators; `punctum` provably does not touch the IPA; `DESC+ADJ` equals `DESC`.

---
## Task 13: `old-irish.rules [mutations]` as grapheme operations

**Depends on:** Task 12. **Spec:** §5, §11; digest §10.4. O-10, O-27, O-29. **Review:** R20, R24,
R25, S8, S9.

**Files:** modify `rules/old-irish.rules` and `src/strands/oldirish.py`; test
`tests/test_oldirish_grammar.py`.

**Interfaces:** `oldirish.apply_oi_mutation(word: SpelledWord, name: str, oi, ) -> SpelledWord`
applies `oi.grapheme_mutations[name]` with `apply_grapheme_table(…, simultaneous=True)` **and sets
`word.mutation = name`**. The metadata is what carries the *unwritten* half of both mutations
(digest §10.2 conv. 1; spec §11 (ii)), which is exactly why the spelled word has the field.

**`LEN`** — digest §10.4 `[wiki-old-irish §Orthography; pokorny1914 p.7 §7]`. **Written** changes
only; `b d g m` are unchanged in writing and carried by the metadata:

| written rule | note |
|---|---|
| `c -> ch / # _` | *tech → thech* pattern |
| `t -> th / # _` | |
| `p -> ph / # _` | |
| `s -> ṡ / # _` | digest §10.2 master table ⟨ṡ sh⟩ = /h/ |
| `f -> ḟ / # _` | **R24 is solved by the representation:** ⟨ḟ⟩ is a real token with an empty reconstruction, so nothing is deleted and nothing has to carry provenance for it. Draft 1's `fˠ → 0` made ⟨ḟ⟩ unreachable |
| *(no rule)* `b d g m` | unwritten (conv. 1); `mutation = "LEN"` makes the reconstruction give `β ð ɣ β̃` |
| *(no rule)* `l n r` | **O-2**: this implementation has one sonorant series, so fortis→lenis lenition would be an identity. Comment it, citing digest §10.4 and O-2, so the absence reads as a decision |
| *(no rule)* s₂ | **S8**: ⟨f, ph⟩ from \*sw, \*sɸ is a handful of lexical items (digest §10.4, §10.2 note 1) — lexicon only. Comment it |

**`NAS`** — digest §10.4 `[pokorny1914 p.10 §21]`:

| written rule | note |
|---|---|
| `b -> mb / # _` | **O-29 / R25:** ⟨mb⟩ is **one token** whose reconstruction is `(mˠ,)` — the master table's "/m/", not a cluster. The §10.4 contrast-set row *a m-bo* /a mbo/ is the digest-internal counter-datum and is recorded in the token's comment |
| `d -> nd / # _` | |
| `g -> ng / # _` | |
| `V -> n- V / # _` | *a n-ech* /a nex/ |
| *(no rule)* `c t p` | **spec §11 (ii):** nasalization of the voiceless stops is **not written**; the metadata carries it and the reconstruction gives `ɡ d̪ˠ bˠ`. Draft 1's §5 reading ("written") is the spec sentence the review flagged as the error; §11 (ii) settles it |
| *(no rule)* `s r l n m` | digest §10.2: "*r l n s* are not subject to eclipsis" |

**The `/ # _` anchor (R20).** Every line carries it. Draft 1 omitted it, so lenition applied
word-internally and its own test (`mac` → `mag`) failed. In the grapheme model the anchor is over
tokens, so `#` means "the first token".

**Pokorny's lenition-blocking rule is not implemented (S9)** — blocked before *d t* when the
preceding word ends in *l n s*, and after a homorganic consonant `[pokorny1914 p.9 §19]`. It is a
cross-word condition, so it belongs to Task 15's templates, not here; a comment in both places
records the omission. It bites on `COMPOUND` and `CU`.

- [ ] **Step 1: Write the failing tests** — `tests/test_oldirish_grammar.py`:

```python
"""Tasks 13-15: Old Irish mutations, inflection and templates as GRAPHEME operations
(spec §5, §11; digest §10.4-§10.5)."""
import pytest

from helpers import ROOT, TABLE, irish, target
from strands.lexicon import key, read_lexicon
from strands.oldirish import apply_oi_mutation
from strands.spelled import SpelledWord, spelling_to_ipa

IRISH = irish()
OI = target("old-irish")
LEX = read_lexicon()


def mut(text, name):
    return apply_oi_mutation(SpelledWord.from_spelling(text), name, OI)


@pytest.mark.parametrize("radical,lenited", [("tech", "thech"), ("cenn", "chenn"),
                                             ("penn", "phenn"), ("son", "ṡon"),
                                             ("fer", "ḟer")])
def test_lenition_writes_the_voiceless_stops_and_the_punctum_forms(radical, lenited):
    """digest §10.4 contrast set; R24: ⟨ḟ⟩ is now reachable because it is a TOKEN."""
    assert mut(radical, "LEN").render() == lenited


@pytest.mark.parametrize("radical", ["bo", "duine", "gel", "mac"])
def test_lenition_of_b_d_g_m_changes_the_ipa_and_not_the_spelling(radical):
    """digest §10.2 conv. 1 — the metadata channel is the whole point (R20: draft 1's
    segment-level version rewrote *mac* to *mag*)."""
    out = mut(radical, "LEN")
    assert out.render() == radical and out.mutation == "LEN"
    assert spelling_to_ipa(out) != spelling_to_ipa(SpelledWord.from_spelling(radical))


def test_lenited_f_is_silent_in_the_reconstruction():
    assert spelling_to_ipa(mut("fer", "LEN")) == ("e", "ɾˠ")


@pytest.mark.parametrize("radical,nasalized", [("bo", "mbo"), ("duine", "nduine"),
                                               ("gel", "ngel"), ("ech", "n-ech")])
def test_nasalization_of_the_voiced_stops_and_vowels_is_written(radical, nasalized):
    """digest §10.4: 'only in the case of b, d, g and of initial vowels'."""
    assert mut(radical, "NAS").render() == nasalized


def test_a_written_nasalized_stop_reconstructs_as_a_single_nasal():
    """O-29 / R25: master table ⟨mb⟩ = /m/."""
    assert spelling_to_ipa(mut("bo", "NAS"))[0] == "mˠ"
    assert len(spelling_to_ipa(mut("bo", "NAS"))) == 2


def test_nasalization_of_a_voiceless_stop_is_not_written():
    """spec §11 (ii)."""
    out = mut("tech", "NAS")
    assert out.render() == "tech"
    assert spelling_to_ipa(out)[0] == "dʲ"


@pytest.mark.parametrize("radical", ["son", "mac", "nem", "lám", "rí"])
def test_s_and_the_sonorants_do_not_nasalize(radical):
    assert mut(radical, "NAS").render() == radical


def test_this_strand_has_only_two_mutation_tables():
    """spec §5: no h-prefix, no t-prefix."""
    assert set(OI.grapheme_mutations) == {"LEN", "NAS"}


def test_every_mutation_line_is_anchored_at_the_word_edge():
    """R20."""
    for rules in OI.grapheme_mutations.values():
        for r in rules:
            assert "#" in r.left, (r.rule_id, r.left)
```

- [ ] **Step 2–4:** run → FAIL; write both tables with `%attested` and their citations plus the
      three "deliberately absent" comments (O-2 sonorants, S8 s₂, S9 blocking); re-run;
      `uv run pytest -q` → green.
- [ ] **Step 5: Commit** — `feat(rules): old-irish [mutations] as grapheme operations (digest §10.4)`

**Acceptance:** *ph th ch ṡ ḟ* are written and *b d g m* are not; the metadata changes the IPA of
the unwritten cases; ⟨mb nd ng n-⟩ are written and reconstruct as single nasals; nasalized *c t p*
are unwritten; *s r l n m* inert; only `LEN` and `NAS`; every line anchored at `#`.

---

## Task 14: `old-irish.rules [inflect]` and the stem dispatch

**Depends on:** Task 13. **Spec:** §5, §11; digest §10.5, §10.2 §§36–41. O-10, O-21, O-26, O-33.
**Review:** R23, R29, R29d, R31b, R31d.

**Files:** modify `rules/old-irish.rules` and `src/strands/oldirish.py`; append to
`tests/test_oldirish_grammar.py`.

**Measured, before you start.** The rule set below was **hand-run against the real lexicon**:

| run | scope | first pass | final |
|---|---|---|---|
| stratified subset, 10 classes | 49 rows | 38/49 = 77.6% | **44/49 = 89.8%** |
| every attested `oi_gen` | 163 rows | 118/163 = 72.4% | **135/163 = 82.8%** |

Per class over all 163: `o` 56/62, `i` 9/10, `ā`(+ī) 23/31, `n` 12/16, `u` 8/12, `velar` 7/9,
`dental` 4/4, `r` 3/4, `s` 4/6, `indecl` 2/2, `irregular` 7/7 (lexical, correct by construction).
Draft 1's IPA-level rules derived **6 of 24**; the whole difference is that these are grapheme
rules, which is what spec §11 changed.

**Precedence in `apply_case` — the lexicon is authoritative, the table is the fallback.** This is
the reverse of draft 1 and is the hand-run's own recommendation: the **n-stem suffix vowel and
gemination** (`-ann/-an/-en/-enn`) and the **u-stem `-o` vs `-a`** are genuinely lexical in Old
Irish and cannot be derived from spelling, and 13 further rows are suppletive.

```python
CASE_TABLES = {("gen", "o"): "GEN_O", ("gen", "ā"): "GEN_A", ("gen", "i"): "GEN_I",
               ("gen", "u"): "GEN_U", ("gen", "n"): "GEN_N", ("gen", "dental"): "GEN_DENT",
               ("gen", "velar"): "GEN_VELAR", ("gen", "r"): "GEN_R", ("gen", "s"): "GEN_S",
               ("voc", "o"): "VOC_O", ("nom", "ā"): "NOM_A", ("nom", ""): "NOM_O",
               ("dat", "o"): "DAT_O", ("dat", "ā"): "DAT_A"}

def apply_case(stem: Stem, case: str, oi, ) -> tuple[SpelledWord, ...]:
    """1. case == "gen" and stem.gen is not None      -> the ATTESTED genitive, verbatim.
       2. stem.stem in ("indecl", "irregular")        -> unchanged, trace note.
       3. a CASE_TABLES entry for (case, stem.stem)   -> apply_grapheme_table(simultaneous=False).
       4. case == "voc"                               -> IDENTITY (O-30/R23), trace note.
       5. otherwise                                   -> GEN_O with `case:{case}-fallback-o`."""
```

**O-30 / R23 is rule 4 and it matters:** digest §10.5 states "The vocative has in the singular the
same form as the nominative… The masculine o-stem and io-stem are the exceptions"
`[pokorny1914 p.65 §142]`. Draft 1 fell back to `VOC_O` for every class, yielding *a Brigte* for
*a Brigit* and *a thúaithe* for *a thúaith*.

**Two shared primitives**, defined in `oldirish.py` and used by the tables (digest §10.2 §§36–41):

- **`INF` (i-infection / "palatalize the final consonant")** rewrites the **last vowel nucleus**;
  *stressed* means the word is monosyllabic (Old Irish has initial stress). ⟨ch th ph⟩ count as one
  consonant when measuring the coda.
  - stressed: `a→ai` (`a→ui` before `nn nd ng`); `e→i`; `i→i`; `o→ui` before two consonants,
    `o→oi` before one; `u→ui`; `á→ái ó→ói ú→úi í→í` (§36: no glide after ⟨í⟩); `é→éui`;
    `éu→íui`; `ía→éi`; `áe→aí`; `oí aí uí` unchanged (§36 exception).
  - unstressed: `a→ai e→i i→i o→oi u→ui á→ái ó→ói ú→úi í→í é→éi`.
  - default: append the glide ⟨i⟩ unless the nucleus already ends in ⟨i⟩.
- **`DEP` (depalatalization)** deletes the glide ⟨i⟩ from the final nucleus; a resulting stressed
  `u` lowers to `o`. **`SYNC`** deletes the vowel of the final unstressed syllable.

**The tables** (each cites the digest §10.5 paradigm row it implements):

```
GEN_O      # o-/io-stem m./n. — fer/fir, claideb/claidib, ball/baill, céile/céili, daltae/daltai
  -ae# -> -ai#                       # io-stem
  -e#  -> -i#                        # io-stem
  V#   -> (unchanged)                # other vowel-final
  -Cach# -> -Caig#  |  -Cech# -> -Cig#   # the productive -ach class; the slender velar
                                         # spirant is written ⟨g⟩, NOT ⟨ch⟩ (R29)
  else -> INF(last nucleus)          # fer->fir, ball->baill, dorn->duirn
GEN_A      # ā-stem fem. — túath/túaithe, cíall/céille
  -e# / -i#  -> unchanged            # iā-stem: guide/guide
  V#         -> V + e
  polysyllabic with a glide-i final nucleus -> SYNC + "ae"   # ī-stem: rígain/rígnae
  polysyllabic with a plain ⟨i⟩ final nucleus -> SYNC + "e"  # ī-stem: Brigit/Brigte
  else       -> INF + "e"            # túath->túaithe, cloch->cloiche
GEN_I      # i-stem — cnáim/cnámo, súil/súlo, muir/moro
  DEP + "o"
GEN_U      # u-stem — guth/gotho, dorus/doirseo
  stressed u -> o ; -s# -> -ss# after a short non-initial vowel (Fergus/Fergusso) ; + "o"
GEN_N      # n-stem — brithem/brithemon, ainm/anmae, Ériu/Érenn
  -mm# -> DEP + one ⟨m⟩ + "ae" ; monosyllabic vowel-final (not -u) -> "on" (cú/con) ;
  disyllabic + geminate -> SYNC + degeminate + "on" (Miliucc/Milcon) ;
  -iu# -> -enn# ; -u# -> -ann# ; -em# -> + "on" ; -am# -> SYNC + "an" ; else + "on"
GEN_DENT   # dental — carae/carat, fili/filed, Núadu/Núadat, teine/teined
  -ae# -> -at# ; -u# -> -at# ; -i# -> -ed# ; -e# -> -ed# ; else + "ad"
GEN_VELAR  # velar — rí/ríg, Lugaid/Luigdech, Echu/Echach
  monosyllabic vowel-final -> + "g" ; -id# polysyllabic -> SYNC + INF + "ech" ;
  -u# -> -ach# ; -ai# -> -ach# ; -í# -> DEP + "ach" ; -e#/-i# -> -ech# ; else + "ach"
GEN_R      # r-stem — athair/athar, máthair/máthar
  final nucleus -> "a"
GEN_S      # s-stem neut. — nem/nime, tech/tige, slíab/sléibe
  V# -> V + "e" ; else INF + "e"
VOC_O      = GEN_O                   # digest §10.5 [pokorny1914 p.65 §142]
NOM_A      # the ENDING MARKER (spec §11): ə# -> "e"
NOM_O      # ə# -> "a"                (every other class)
DAT_O DAT_A  # identity; the leniting mutation is supplied by the template (digest §10.4)
```

**`NOM_A`/`NOM_O` are where spec §11's ending marker is realized** (GPT #8): Task 11 wrote a
word-final `ə` grapheme; `apply_case(stem, "nom", …)` resolves it to ⟨e⟩ for an ā-stem and ⟨a⟩
otherwise. **`run_entry_oi` calls `apply_case(…, "nom", …)` on every RETRO word before rendering**,
so no finished output can contain the marker — a property test in Task 18 asserts that.

**The ī-stem needs no new `stem` value** (O-21): its two rules sit inside `GEN_A`, selected by
shape (polysyllabic, glide-i or plain-⟨i⟩ final nucleus). That is exactly §41 — after a broad
consonant final /e/ is written ⟨-ae⟩, after a slender one ⟨-e⟩.

- [ ] **Step 1: Write the failing tests** — append:

```python
from strands.oldirish import CASE_TABLES, Stem, apply_case, to_old_irish
from strands.inputs import Entry, infer


def ent(orthography, ipa="sˠiː", **kw):
    return infer(Entry(orthography=orthography, ipa=ipa, **kw), IRISH, TABLE)


def infl(text, table_name):
    from strands.spelled import apply_grapheme_table
    return apply_grapheme_table(SpelledWord.from_spelling(text),
                                OI.grapheme_inflect[table_name], simultaneous=False).render()


@pytest.mark.parametrize("table_name,nom,gen", [
    ("GEN_O", "fer", "fir"), ("GEN_O", "claideb", "claidib"), ("GEN_O", "ball", "baill"),
    ("GEN_O", "céile", "céili"), ("GEN_O", "daltae", "daltai"), ("GEN_O", "cellach", "cellaig"),
    ("GEN_A", "túath", "túaithe"), ("GEN_A", "cloch", "cloiche"), ("GEN_A", "guide", "guide"),
    ("GEN_A", "rígain", "rígnae"), ("GEN_A", "Brigit", "Brigte"),
    ("GEN_I", "cnáim", "cnámo"), ("GEN_I", "súil", "súlo"),
    ("GEN_U", "guth", "gotho"),
    ("GEN_N", "brithem", "brithemon"), ("GEN_N", "Ériu", "Érenn"), ("GEN_N", "ainmm", "anmae"),
    ("GEN_DENT", "carae", "carat"), ("GEN_DENT", "fili", "filed"), ("GEN_DENT", "Núadu", "Núadat"),
    ("GEN_VELAR", "rí", "ríg"), ("GEN_VELAR", "Lugaid", "Luigdech"), ("GEN_VELAR", "Echu", "Echach"),
    ("GEN_R", "athair", "athar"), ("GEN_R", "máthair", "máthar"),
    ("GEN_S", "nem", "nime"), ("GEN_S", "slíab", "sléibe"),
])
def test_each_stem_class_derives_its_attested_genitive(table_name, nom, gen):
    """digest §10.5 [strachan1909 pp.2-16; pokorny1914 pp.59-70]. Hand-run: 44/49 on the
    stratified subset, 135/163 over every attested genitive in the lexicon."""
    assert infl(nom, table_name) == gen


def test_the_derivation_rate_over_the_whole_lexicon_does_not_regress():
    """The real acceptance metric. Measured 135/163; the floor allows for Task 3 edits."""
    from strands.lexicon import FORM_STATUSES
    rows = [r for r in LEX.values() if r.status in FORM_STATUSES and r.oi_gen and r.stem
            and r.stem not in ("irregular", "indecl")]
    table_for = {stem: name for (case, stem), name in CASE_TABLES.items() if case == "gen"}
    ok = sum(1 for r in rows if r.stem in table_for
             and infl(r.oi_nom, table_for[r.stem]) == r.oi_gen)
    assert ok / len(rows) >= 0.78, (ok, len(rows))


def test_the_o_stem_vocative_is_the_genitive_form_and_every_other_class_is_identity():
    """O-30 / R23: digest §10.5 [pokorny1914 p.65 §142]. Draft 1 gave *a Brigte*."""
    o = Stem(words=(SpelledWord.from_spelling("fer"),), gen=None, stem="o", gender="m",
             flag="ATTESTED", assumptions=(), trace=())
    a = Stem(words=(SpelledWord.from_spelling("túath"),), gen=None, stem="ā", gender="f",
             flag="ATTESTED", assumptions=(), trace=())
    assert apply_case(o, "voc", OI)[0].render() == "fir"
    assert apply_case(a, "voc", OI)[0].render() == "túath"


def test_an_attested_genitive_is_never_re_derived():
    """Precedence rule 1: the lexicon is authoritative. The n-stem suffix vowel and the
    u-stem -o/-a are lexical in Old Irish and cannot be derived from spelling."""
    row = LEX[key("Éire")]
    stem = to_old_irish(ent("Éire", "ˈeːɾʲə"), LEX, OI, IRISH, TABLE)
    assert apply_case(stem, "gen", OI)[0].render() == row.oi_gen


def test_an_indeclinable_stem_is_returned_unchanged():
    """digest §10.5; R31b: *Patraic* must be `indecl` or GILLA derives a genitive for it."""
    s = Stem(words=(SpelledWord.from_spelling("Patraic"),), gen=None, stem="indecl",
             gender="m", flag="ATTESTED", assumptions=(), trace=())
    assert apply_case(s, "gen", OI)[0].render() == "Patraic"


def test_the_ending_marker_is_realized_by_stem_class():
    """spec §11 / GPT #8: the retro-filter leaves it unresolved and [inflect] resolves it."""
    a = Stem(words=(SpelledWord.from_spelling("carə"),), gen=None, stem="ā", gender="f",
             flag="RETRO", assumptions=(), trace=())
    o = Stem(words=(SpelledWord.from_spelling("carə"),), gen=None, stem="o", gender="m",
             flag="RETRO", assumptions=(), trace=())
    assert apply_case(a, "nom", OI)[0].render() == "care"
    assert apply_case(o, "nom", OI)[0].render() == "cara"


def test_an_unknown_stem_class_falls_back_to_the_o_stem_with_a_note():
    s = Stem(words=(SpelledWord.from_spelling("fer"),), gen=None, stem="", gender="m",
             flag="RETRO", assumptions=(), trace=())
    out = apply_case(s, "gen", OI)
    assert out[0].render() == "fir"


def test_the_case_table_map_covers_every_stem_value_that_has_a_paradigm():
    from strands.lexicon import STEMS
    assert {s for (c, s) in CASE_TABLES if c == "gen"} == set(STEMS) - {"indecl", "irregular"}
```

- [ ] **Step 2–4:** run → FAIL; implement `INF`/`DEP`/`SYNC` and the tables one class at a time,
      running that class's parametrized cases after each; then `apply_case`. Where a case still
      misses, check it against the hand-run's **failure ledger**: 13 rows are genuinely suppletive
      (*siur/sethar*, *día/dé*, *adaig/aidche*, …) and belong to precedence rule 1; 8 are rows where
      the lexicon recorded one attested variant and the rule produces its sibling
      (*bél/béoil~béuil*, *Lug/Loga~Logo*) — leave those, they are data, not rules.
- [ ] **Step 5:** add `Checker.grapheme_rules` to `check.py`: every target and replacement token of
      a `[mutations]`/`[inflect]` line must be a token of the grapheme table (code
      `GRAPHEME_UNKNOWN_TOKEN`, error).
- [ ] **Step 6:** `uv run pytest -q` → green. **Commit:**
      `feat(rules): old-irish [inflect] by stem class — 135/163 attested genitives derived`

**Acceptance:** the 27 parametrized paradigm genitives derive; the whole-lexicon rate is ≥78%; the
vocative is identity outside the o-stem; an attested `oi_gen` wins; `indecl` is inert; the ending
marker is realized by stem class; `CASE_TABLES` covers every paradigm-bearing stem value.

---

## Task 15: `[templates]`, the Old Irish builder, its own `ART`, and the function registry

**Depends on:** Task 14. **Spec:** §5, §8 row O6, §11 (the builder bullet and corrections (i)).
O-17, O-25, O-30, O-32. **Review:** R21, R22, R30, R31, R31a, R31c, S9, S10, S11, and GPT #7.

**Files:** modify `src/strands/dsl.py`, `src/strands/oldirish.py`, `src/strands/pipeline.py`,
`rules/old-irish.rules`; append to `tests/test_oldirish_grammar.py`.

**The function registry (spec §11, GPT #7).** `dsl.py` currently validates template call names
against a hard-coded list, and `check.templates` walks the same list. Replace both with **one
per-file registry**: a call name is legal when it is a key of the file's mutation tables, a key of
its inflection tables, or one of the built-ins the file declares in `[meta] template-functions`
(for `old-irish.rules`: `GEN NOM VOC DAT ART`). The parser and the checker read the **same**
function, so they cannot drift. `irish.rules` keeps its current behaviour by declaring its own list.
**`COLOUR` is added to the argument names** (`TEMPLATE_ARGS`) alongside `NAME FATHER NOUN ADJ FIRST
SECOND` — GPT #7 found it missing, which would have made the `COLOUR` template unparseable.

**The Old Irish builder (spec §11).** `oldirish.build_oi_construction(name, slots, oi, table)` is
its own component; `irish._Builder` is **not** subclassed, because R22 showed `irish._article` is
hardcoded modern Irish (it emits *an*/*na* and calls `HPREF`/`TPREF`, the two tables this strand
forbids). The Old Irish builder:

- evaluates an `arg` item to the slot's `Stem` (Task 12), not to an `Entry`'s IPA;
- evaluates a **quoted literal as a spelling** (O-25) — `SpelledWord.from_spelling(text)`;
- `GEN(x)`/`NOM(x)`/`VOC(x)`/`DAT(x)` → `apply_case(x, case, oi)`;
- `LEN(x)`/`NAS(x)` → `apply_oi_mutation`;
- `ART(x)` is **its own**: digest §10.4's article — sg. m. nom. *in(t)*, f. nom. *in(d)*ᴸ,
  n. nom. *a*ᴺ, gen. m./n. *in(d)*ᴸ, f. gen. *(in)na*ᴴ, dat. *-(si)n(d)*ᴸ, pl. *(in)na*. The final
  ⟨-d⟩/⟨-t⟩ sandhi is written with the digest's **CONFLICT** recorded in the comment: Wikipedia has
  it unqualified before a vowel, liquid, *n* or *f*, while Pokorny restricts ⟨-d⟩ to "before vowels
  or aspirated *f, l, n, r*" `[pokorny1914 p.59 §132]`. Take Pokorny (the narrower, cited rule) and
  say so. **No *h*-prefix and no *t*-prefix** exist in this strand;
- joins words with a single space and re-applies capitalization per word (O-32).

**The templates** (spec §5 + §8 row O6, with §11's corrections):

| name | template | source / decision |
|---|---|---|
| `DESC` | `NOM(NOUN)` | resolves the ending marker (Task 14) |
| `VOC` | `"a" " " LEN(VOC(NAME))` | the particle *a* lenites `[pokorny1914 p.8 §12]`; `VOC()` is identity outside the o-stem (O-30) |
| `GEN` | `GEN(NAME)` | |
| `ADJ` | `NAME " " LEN_IF_F(ADJ)` | digest §10.4 `[pokorny1914 p.8 §10]`. **S11:** Pokorny also lenites after a dat. sg., a voc. sg. of any gender, and a gen./nom.-pl. masc. o-stem; nom.-fem.-only is a deliberate narrowing — say so in the comment |
| `OF` | `NAME " " ART(GEN(NOUN))` | now reachable, with the Old Irish article above (R22) |
| `COMPOUND` | `FIRST LEN(SECOND)` | digest §10.5 `[pokorny1914 p.8 §16]`: *dag-theist*, *énḟlaith* |
| `MAEL` | `"Máel" " " GEN(NAME)` | **§11 (i) / R21: NOT lenited.** Every attested lexicon row agrees — *Máel Coluim*, *Máel Muire*, *Máel Sechnaill* — and *Sechnaill* is decisive, since later-OI ⟨ṡ⟩ *is* written. It also follows from digest §10.4's trigger table (*máel* is a masculine nominative, which triggers nothing) |
| `GILLA` | `"Gilla" " " GEN(NAME)` | **§11 (i): not lenited** |
| `CU` | `"Cú" " " LEN(GEN(NAME))` | **§11 (i): lenites** — *Cú Chulainn*, gen. *Con Culainn* (digest §10.6) |
| `FER` | `"Fer" " " GEN(NAME)` | *Fer Diad*; no lenition |
| `COLOUR` | `COLOUR LEN(NAME)` | a **compound**, not a phrase — no `" "`, digest §10.5's compound lenition. **R31a:** *Dub-dá-leithe* is three elements and is **not** the target; the test uses a real two-element compound (*Dubthach*, *Donnchad*). **R31a:** the element is spelled *Find-* in the digest and *Finn* in the lexicon — Task 3 picks one |
| `MAC` | `"macc" " " GEN(NAME)` | *Conchobar mac Nessa* (digest §10.5) |
| `UA` | `"aue" " " GEN(NAME)` | **`%design`**: digest §10.5 — "No Old Irish *aue*+genitive naming formula is stated". **S10:** reconcile the element spelling with the lexicon's `ua` row in Task 3 |
| `INGEN` | `"ingen" " " LEN(GEN(NAME))` | **S10, split citation:** `%design` for the *formula* (digest §10.5: "not attested in these sources as a naming formula"), `%attested` for the *mutation* — *ingen* is a feminine ā-stem and digest §10.4's trigger table makes nom./voc. sg. of all feminines leniting |

`PATRO_O`/`PATRO_NI` get a **comment where they would be**, quoting spec §5's "These replace
`PATRO_O`/`PATRO_NI`, which do not apply to this strand" (O-17). **S9's blocking rule** gets a
comment on `COMPOUND` and `CU` recording that it is not implemented.

`pipeline.CONSTRUCTIONS` gains `"MAEL", "GILLA", "CU", "FER", "COLOUR", "MAC", "UA", "INGEN"`.
Because the other four targets have no templates of those names, `run_entry` translates a
missing-template `IrishError` into `ConstructionNotInStrand`, which Tasks 17 and 18 treat exactly
like `MissingSlot` — a skipped cell with a note.

**Test fixtures are real element rows (R31).** Draft 1's cases used *Culann*, *Diad* and *Leithe*,
which are **not lexicon rows**, and passed *Niall*'s IPA for every word. The head elements all
exist — *Maol* → *Máel*, *Giolla* → *Gilla*, *cú*, *fear* → *fer*, *mac* → *macc*, *inion* →
*ingen* — and Task 3 adds the governed elements or records that they could not be cited, in which
case those cases are dropped rather than skipped. Assertions are on the **rendered string with its
capitalization** (R31c), not on a casefold.

- [ ] **Step 1: Write the failing tests** — append:

```python
from strands.oldirish import ConstructionNotInStrand, build_oi_construction, run_entry_oi
from strands.pipeline import CONSTRUCTIONS


def build(construction, **slots):
    return run_entry_oi(slots.pop("_head"), construction, IRISH, OI, TABLE,
                        slots=slots or None).respelling


def test_the_eight_formation_templates_exist_and_are_reachable_from_the_cli():
    names = {"MAEL", "GILLA", "CU", "FER", "COLOUR", "MAC", "UA", "INGEN"}
    assert names <= set(OI.templates) and names <= set(CONSTRUCTIONS)


def test_the_patronymic_particles_of_the_other_strands_are_absent():
    assert "PATRO_O" not in OI.templates and "PATRO_NI" not in OI.templates
    with pytest.raises(ConstructionNotInStrand):
        run_entry_oi(ent("Niall", "nʲiəl̪ˠ"), "PATRO_NI", IRISH, OI, TABLE)


def test_mael_and_gilla_do_not_lenite():
    """spec §11 (i) / R21 — every attested lexicon row: *Máel Coluim*, *Máel Muire*,
    *Máel Sechnaill*. Draft 1 produced *máel Choluim*."""
    out = build("MAEL", _head=ent("Colm", "ˈkɔl̪ˠəmˠ"), NAME=ent("Colm", "ˈkɔl̪ˠəmˠ"))
    assert out.startswith("Máel ") and not out.split()[1].startswith("Ch")


def test_cu_and_ingen_do_lenite():
    """spec §11 (i): *Cú Chulainn*. S10: *ingen* is a fem. ā-stem, so its mutation is
    attested even though the formula is not."""
    out = build("CU", _head=ent("Culann", "ˈkʊl̪ˠən̪ˠ"), NAME=ent("Culann", "ˈkʊl̪ˠən̪ˠ"))
    assert out.split()[1].startswith("Ch")


def test_the_vocative_particle_lenites_and_the_class_decides_the_stem():
    """O-30: identity outside the o-stem."""
    out = build("VOC", _head=ent("Cormac", "ˈkɔɾˠəmˠək", declension="m1"),
                NAME=ent("Cormac", "ˈkɔɾˠəmˠək", declension="m1"))
    assert out.split()[0] == "a" and out.split()[1].startswith("Ch")


def test_the_colour_formation_is_a_compound_not_a_phrase():
    out = build("COLOUR", _head=ent("dubh", "d̪ˠʊw"), COLOUR=ent("dubh", "d̪ˠʊw"),
                NAME=ent("teach", "tʲax"))
    assert " " not in out


def test_the_article_is_old_irish_not_modern():
    """R22: `irish._article` emits *an*/*na* and calls HPREF/TPREF, which this strand forbids."""
    out = build("OF", _head=ent("Niall", "nʲiəl̪ˠ"), NAME=ent("Niall", "nʲiəl̪ˠ"),
                NOUN=ent("teach", "tʲax"))
    article = out.split()[1]
    assert article.startswith(("in", "a")) and not article.startswith(("an", "na"))


def test_capitalization_is_preserved_per_word():
    """R31c: draft 1's tests asserted on capitals that `respell` never produces."""
    out = build("MAC", _head=ent("Conchobhar", "ˈkɾˠɔxuːɾˠ"), NAME=ent("Neasa", "ˈnʲasˠə"))
    assert out.split()[0] == "macc" and out.split()[1][0].isupper()


def test_the_unattested_formations_are_tagged_design():
    text = (ROOT / "rules" / "old-irish.rules").read_text(encoding="utf-8")
    for name in ("UA", "INGEN"):
        line = [l for l in text.splitlines() if l.strip().startswith(name + " ")][0]
        assert "design" in line, line


def test_a_template_literal_is_a_spelling_that_tokenizes():
    """O-25 / spec §11: literals are SPELLINGS, not IPA."""
    text = (ROOT / "rules" / "old-irish.rules").read_text(encoding="utf-8")
    import re
    for line in text.splitlines():
        for literal in re.findall(r'"([^"]+)"', line):
            if literal.strip():
                assert SpelledWord.from_spelling(literal).render() == literal, line


def test_the_function_registry_is_shared_by_the_parser_and_the_checker():
    """GPT #7: draft 1 left check.py's validator on the old hard-coded list."""
    from strands.dsl import template_functions
    names = template_functions(OI)
    assert {"GEN", "ART", "LEN", "NAS"} <= names
    assert "COLOUR" in __import__("strands.dsl", fromlist=["TEMPLATE_ARGS"]).TEMPLATE_ARGS
```

- [ ] **Step 2–5:** run → FAIL; add the registry and `COLOUR` to `dsl.py`; write
      `build_oi_construction` and the Old Irish `ART`; write `[templates]`; extend
      `pipeline.CONSTRUCTIONS` and the `IrishError` translation.
- [ ] **Step 6: Delete the Task-12 xfail marks** and make those tests pass. That is this task's real
      completion criterion.
- [ ] **Step 7:** `uv run pytest -q` → green, **no xpass**. **Commit:**

```bash
git commit -m "feat(rules): old-irish [templates] with its own builder, article and function registry

MAEL/GILLA take the genitive unlenited per spec §11 (i) and every attested lexicon row;
CU and INGEN lenite. Template function names now come from one per-file registry shared by
the parser and the checker, amending the engine plan's func-name production."
```

**Acceptance:** the eight formations exist and are in `CONSTRUCTIONS`; `MAEL`/`GILLA` do not lenite
and `CU`/`INGEN` do; `COLOUR` is one word; the article is Old Irish; capitalization survives;
literals are spellings that tokenize; `UA`/`INGEN` are `%design`; `PATRO_*` raise; parser and
checker share one registry.

---
## Task 16: Filter regression and its ratchet

**Depends on:** Tasks 4, 15. **Spec:** §7, §11. O-13, O-16, O-31. **Review:** R1, R2, S19.

**Files:** modify `src/strands/oldirish.py`; create `tests/ratchets/old-irish.json`; test
`tests/test_oldirish_regression.py`.

**Interfaces:**

```python
@dataclass(frozen=True)
class FilterRow:
    orthography: str; expected: str; got: str; distance: int
    classes: tuple[str, ...]; constructed: bool = False

@dataclass(frozen=True)
class FilterReport:
    rows: tuple[FilterRow, ...]
    def rate(self, max_distance: int = 0, constructed: bool | None = None) -> float
    def by_class(self) -> dict[str, tuple[int, int]]

REVERSAL_CLASSES: dict[str, Callable[[str], bool]]
def filter_regression(entries, lexicon, oi, irish, table, *, g2p=None) -> FilterReport
```

**The population, measured (O-31, R1).** Spec §11 fixes the definition: the unique citation-form
keys that are in `test-words.tsv` **with hand IPA** and have a **form-bearing** lexicon row.
Recomputed from the two committed files:

| population | count |
|---|---|
| distinct test-word keys | 138 (all carry IPA) |
| direct lexicon hits | 74 |
| …of which `status = none` — **excluded**, they have no `oi_nom` | 20 |
| **n = the regression population** | **54** |

Draft 1 said 74 and asserted `>= 70`; both were wrong. Assert `>= 50` (Task 3 may remove rows,
Task 4 adds a few that are test words) and print the measured n.

**Duplicate keys (O-31).** 5 test-word keys are duplicated; 4 are in the population. The rule is
**"the first row whose `features` contains `src:attested`, else the first row in file order"** —
the fallback is required, because `niamh` (in the population) has **no** `src:attested` row.
`dubh`, `leanbh` and `naomh` have 2, 2 and 3 all-attested rows and the rule picks row 0; the
variants it discards are real (`w`~`vˠ`, fortis~lenis), so the report names the chosen row.

**Reversal classes, with their measured sizes in the population (R2).**

| class | predicate over the modern orthography | in n=54 | whole lexicon |
|---|---|---|---|
| `quality-digraph` | contains `ea io ai oi ui` | 21 | ~50 |
| `ch-th` | contains `ch` or `th` | 9 | 51 |
| `final-vowel` | ends in `a`/`e` | 9 | — |
| `geminate` | `oi_nom` has a doubled letter the modern form lacks | 8 | 47 |
| `lenition-digraph` | contains `bh dh gh mh` | 7 | ~49 |
| `ao` | contains `ao` | **4** | 20 |
| `ua-ia` | contains `ua`/`ia` | 4 | 33 |
| `an-suffix` | ends in `án` | 3 | — |
| `r-stem` | in {athair, bráthair, máthair} | 1 | 3 |

**R2 is load-bearing: the ⟨ao⟩ set has 4 members here, not the 20 draft 1 asserted.** The 20 pairs
exist only across the whole lexicon, i.e. only in the G2P-widened population, which is deliberately
un-ratcheted. So: assert `>= 4` on the ratcheted population, report the ⟨ao⟩ breakdown over the
widened one, and **say in the module docstring that decision O1 cannot be measured without the
G2P**. The parenthetical whole-lexicon counts are labelled as such.

**The G2P population.** `src/strands/g2p.py` is committed (2760b0e, 6207634). With `g2p=` supplied,
every form-bearing row **without** a test-word IPA is added — measured, **216 more keys** — with
`constructed=True`. `rate(..., constructed=False)` is what the ratchet keys off, so G2P accuracy can
never move a filter number.

**Ratchet:** `tests/ratchets/old-irish.json` = `{"exact": r, "lev1": r, "n": int}`, following the
existing `regress.load_ratchet` / `assert_ratchet` / `write_ratchet` convention (`write_ratchet` is
run **by hand**, never by a test). Do not guess the values: run it, read them, floor to 4 dp.

**What a low rate means.** Every filter rule is `%design` or rests on a handful of pairs, and digest
§10.7 says outright that "the correspondence set to do it is not in this source set". A rate well
under 50% is an expected outcome; the **per-class breakdown** is the artefact. Say so in the module
docstring so nobody later "fixes" the number by weakening the comparison.

- [ ] **Step 1: Write the failing tests** — `tests/test_oldirish_regression.py`:

```python
"""Task 16: the filter regression (spec §7, §11). A low rate is a finding, not a failure —
see the module docstring in oldirish.py."""
import json

import pytest

from helpers import ROOT, TABLE, irish, read_test_words, target
from strands.inputs import Entry, infer
from strands.lexicon import FORM_STATUSES, key, read_lexicon
from strands.oldirish import REVERSAL_CLASSES, filter_regression
from strands.regress import load_ratchet

IRISH = irish()
OI = target("old-irish")
LEX = read_lexicon()
RATCHET = ROOT / "tests" / "ratchets" / "old-irish.json"
ENTRIES = [infer(Entry(orthography=r["orthography"], ipa=r["ipa"],
                       dialect=r.get("dialect") or "C"), IRISH, TABLE)
           for r in read_test_words() if r["ipa"]]
REPORT = filter_regression(ENTRIES, LEX, OI, IRISH, TABLE)


def test_the_denominator_is_the_measured_form_bearing_overlap():
    """O-31 / R1: 54, not draft 1's 74 — the 20 `none` hits have no oi_nom."""
    assert len(REPORT.rows) >= 50, len(REPORT.rows)
    assert all(LEX[key(r.orthography)].status in FORM_STATUSES for r in REPORT.rows)


def test_duplicate_keys_resolve_deterministically():
    """O-31: `niamh` has NO src:attested row, so the fallback is required."""
    assert len({r.orthography for r in REPORT.rows}) == len(REPORT.rows)
    again = filter_regression(ENTRIES, LEX, OI, IRISH, TABLE)
    assert again.rows == REPORT.rows


def test_every_row_compares_written_forms():
    """O-16: oi_nom is a spelling, so both the comparison and the distance are characters."""
    for r in REPORT.rows:
        assert r.expected == LEX[key(r.orthography)].oi_nom and isinstance(r.distance, int)


def test_both_rates_are_reported_and_ordered():
    assert 0.0 <= REPORT.rate(0) <= REPORT.rate(1) <= 1.0


def test_the_ratchet_holds():
    ratchet = load_ratchet("old-irish")
    assert REPORT.rate(0) >= ratchet["exact"] - 1e-9
    assert REPORT.rate(1) >= ratchet["lev1"] - 1e-9


def test_the_ratchet_file_records_the_denominator():
    data = json.loads(RATCHET.read_text(encoding="utf-8"))
    assert set(data) == {"exact", "lev1", "n"} and data["n"] == len(REPORT.rows)


def test_every_reversal_class_is_measured():
    by_class = REPORT.by_class()
    assert set(by_class) == set(REVERSAL_CLASSES)
    assert all(0 <= p <= t for p, t in by_class.values())


def test_the_ao_class_is_present_but_too_small_to_decide_O1():
    """R2: measured 4 in the ratcheted population; the 20 pairs are G2P-only."""
    passed, total = REPORT.by_class()["ao"]
    assert total >= 4, total


@pytest.mark.parametrize("cls", ["an-suffix", "r-stem"])
def test_the_invariant_classes_are_near_perfect(cls):
    """S19 / log finding 4: if the filter breaks THESE it is over-applying."""
    passed, total = REPORT.by_class()[cls]
    if total == 0:
        pytest.skip(f"no {cls} headwords in the overlap")
    assert passed >= total - 1, (passed, total)


def test_a_g2p_widens_the_population_without_moving_the_ratchet():
    g2p = pytest.importorskip("strands.g2p").g2p
    wide = filter_regression(ENTRIES, LEX, OI, IRISH, TABLE, g2p=g2p)
    assert len(wide.rows) > len(REPORT.rows)
    assert wide.rate(0, constructed=False) == REPORT.rate(0)
    assert any(r.constructed for r in wide.rows)
    assert wide.by_class()["ao"][1] >= 15        # R2: O1 is measurable only here
```

- [ ] **Step 2–3:** run → FAIL; implement. Force the **RETRO** path even where the lexicon row
      exists — that is the measurement — then compare `Result.respelling` to `row.oi_nom` after NFC
      and casefold. Reuse `regress.edit_distance` if it is character-generic; do not write a second.
- [ ] **Step 4:** run it, read the numbers, write the ratchet, and **paste the per-class table into
      the commit message** — it is the artefact the owner reads:

```bash
uv run python -c "
import sys; sys.path.insert(0, 'tests')
from test_oldirish_regression import REPORT
print('n', len(REPORT.rows), 'exact', REPORT.rate(0), 'lev1', REPORT.rate(1))
for name, (p, t) in sorted(REPORT.by_class().items()): print(f'{name:18} {p:3}/{t:3}')
for r in REPORT.rows:
    if r.distance: print(r.distance, r.orthography, r.expected, '!=', r.got, r.classes)"
```

- [ ] **Step 5: Commit** — `test(oldirish): filter regression over the measured 54-headword overlap`

**Acceptance:** ≥50 rows, one per unique key, deterministic; both rates reported and ratcheted; every
class counted; the ⟨ao⟩ class has ≥4 and O1's un-measurability is documented; the invariant classes
are at most one row off perfect; the G2P population widens without touching the ratchet.

---

## Task 17: CLI exposure

**Depends on:** Task 15. **Spec:** §2, §9 milestone 5. O-17, O-23.

**Files:** modify `src/strands/cli.py`; append to `tests/test_cli.py`.

`--strand old-irish` works once `TARGETS` and `CONSTRUCTIONS` are extended (Tasks 12, 15). What this
task adds:

1. **`run`**: catch `ConstructionNotInStrand` beside `MissingSlot`; write the row with empty output
   columns and `assumptions = skipped:construction-not-in-strand`. With five strands and eight new
   formation names this fires on every `--construction all` run, so it must be a skip.
2. **`explain`**: takes a bare IPA `WORD`, but Old Irish lookup keys on **orthography** (O-23). Add
   `--orthography TEXT`: when given it is the lookup key and the aligner's input; when absent,
   `explain --strand old-irish` runs the pure retro path and **prints a one-line note saying so**,
   because a silent `RETRO` looks like a lexicon miss.
3. **`check`** already routes `.tsv` (Task 2); confirm `strands check rules/old-irish.rules` passes.
4. `--strand all` now includes `old-irish`, changing every `run`/`gallery` output. Intended;
   Task 18 re-snapshots.

- [ ] **Step 1: Write the failing tests** — append to `tests/test_cli.py`:

```python
def test_run_accepts_the_fifth_strand(tmp_path):
    from strands.cli import main
    out = tmp_path / "out.tsv"
    assert main(["run", str(FIX), "--strand", "old-irish", "--out", str(out)]) == 0
    assert "old-irish" in out.read_text(encoding="utf-8")


def test_a_construction_the_strand_lacks_is_a_skipped_row_not_an_error(tmp_path):
    """O-17: PATRO_NI for old-irish, MAEL for welsh — both are skips."""
    from strands.cli import main
    out = tmp_path / "out.tsv"
    assert main(["run", str(FIX), "--strand", "all", "--construction", "all",
                 "--out", str(out)]) == 0
    assert "skipped:construction-not-in-strand" in out.read_text(encoding="utf-8")


def test_explain_warns_when_no_orthography_is_given_for_old_irish(capsys):
    """O-23: lookup keys on orthography, which a bare IPA argument cannot supply."""
    from strands.cli import main
    assert main(["explain", "nʲiəl̪ˠ", "--strand", "old-irish"]) == 0
    out = capsys.readouterr().out
    assert "RETRO" in out and "--orthography" in out


def test_explain_uses_the_orthography_for_the_lookup(capsys):
    from strands.cli import main
    assert main(["explain", "nʲiəl̪ˠ", "--strand", "old-irish", "--orthography", "Niall"]) == 0
    assert "ATTESTED" in capsys.readouterr().out


def test_check_passes_on_the_old_irish_rule_file():
    from strands.cli import main
    assert main(["check", str(ROOT / "rules" / "old-irish.rules")]) == 0
```

(If `main` returns 2 for usage errors rather than raising, match whatever the existing tests do.)

- [ ] **Steps 2–4:** run → FAIL; implement; `uv run pytest -q` → green. **Commit:**
      `feat(cli): expose --strand old-irish, --orthography for explain, skip absent constructions`

**Acceptance:** `--strand old-irish` runs; an absent construction is a skipped row on every strand;
`explain` uses `--orthography` and warns without it; `check` passes on the rule file.

---

## Task 18: Gallery column, snapshot, and property checks

**Depends on:** Tasks 16, 17. **Spec:** §7, §11. O-11, O-17, O-32. **Review:** R31.

**Files:** modify `src/strands/gallery.py`, `tests/snapshots/gallery.md`,
`tests/test_gallery_snapshot.py`, `tests/test_properties.py`.

`render_gallery` needs no signature change — `strands gallery` passes all of `TARGETS`. This task
adds `formation_block(...)` and catches `ConstructionNotInStrand` in `run_cell` beside
`MissingSlot`. `render_cell` already prints `!FLAG` per flag, so the five lookup flags appear with
no new code — **verify that rather than adding any**.

**The formation block (R31).** Draft 1 rendered "the five attested example names" from the lexicon
by their modern keys — but *Maol Coluim*, *Giolla Pádraig*, *Fear Diad*, *Dubh-dá-leithe* and
*Cú Chulainn* are **whole-name lexicon rows**, so lookup returns each as `ATTESTED` in one piece and
the formation template is never exercised; and none of the five is a `test-words.tsv` row, so there
was no source of the `Entry` IPA `render_gallery` needs. Fixed: the block is built from the
**element** rows (Task 3 guarantees they exist) — head *Maol*→*Máel*, *Giolla*→*Gilla*, *cú*,
*fear*→*fer*, *mac*→*macc*, *inion*→*ingen*; governed *Colm*→*Colum*, *Pádraig*→*Pátraic*, and
whichever of *Culann*/*Diad*/*Leithe* Task 3 could cite. The `Entry` for each element is built from
the lexicon row's `orthography` plus the committed **G2P** for its IPA, tagged `ipa:constructed` —
`src/strands/g2p.py` is committed, so this needs no new machinery.

- [ ] **Step 1: Write the failing tests.** Append to `tests/test_gallery_snapshot.py`:

```python
def test_the_gallery_has_a_fifth_column_with_the_lookup_marks():
    """spec §7. `render_cell` already prints !FLAG — this asserts it, it asks for no code."""
    text = (ROOT / "tests" / "snapshots" / "gallery.md").read_text(encoding="utf-8")
    assert "old-irish" in text and "!ATTESTED" in text and "!RETRO" in text


def test_the_formation_template_block_is_present_and_built_from_elements():
    """R31: a whole-name lexicon row returns ATTESTED in one piece and never exercises the
    template."""
    text = (ROOT / "tests" / "snapshots" / "gallery.md").read_text(encoding="utf-8")
    assert "## Old Irish formations" in text
    for name in ("MAEL", "GILLA", "CU", "FER", "COLOUR", "MAC", "UA", "INGEN"):
        assert name in text
    assert "Máel" in text and "macc" in text
```

Append to `tests/test_properties.py`:

```python
def test_every_old_irish_output_carries_exactly_one_lookup_flag():
    from strands.oldirish import OI_FLAGS
    for row, result in _results("old-irish", "DESC"):
        assert len([f for f in result.flags if f in OI_FLAGS]) == 1, \
            (row["orthography"], result.flags)


def test_every_old_irish_respelling_reconstructs_to_its_reported_ipa():
    """spec §6, §11 / O-11: the IPA is derived FROM the finished written form. This is the
    property that keeps [respell] and the grapheme table one system."""
    from strands.spelled import SpelledWord, spelling_to_ipa
    for row, result in _results("old-irish", "DESC"):
        rebuilt = " ".join("".join(spelling_to_ipa(SpelledWord.from_spelling(p)))
                           for p in result.respelling.split(" "))
        assert rebuilt == result.ipa, (row["orthography"], result.respelling)


def test_no_old_irish_output_uses_a_modern_lenition_digraph():
    """digest §10.2 conv. 1: there is no ⟨bh dh gh mh⟩ in Old Irish."""
    for row, result in _results("old-irish", "DESC"):
        low = result.respelling.lower()
        assert not any(d in low for d in ("bh", "dh", "gh", "mh")), \
            (row["orthography"], result.respelling)


def test_no_finished_old_irish_output_still_carries_the_ending_marker():
    """spec §11: [inflect] resolves it by stem class (Task 14). If one leaks, NOM_A/NOM_O
    did not run."""
    for row, result in _results("old-irish", "DESC"):
        assert "ə" not in result.respelling, (row["orthography"], result.respelling)


def test_old_irish_words_are_stressed_initially():
    for row, result in _results("old-irish", "DESC"):
        for word in result.words:
            assert getattr(word, "stress", 0) in (0, None), row["orthography"]
```

The existing parametrized property tests enumerate `TARGETS`, so they now cover `old-irish`
automatically. **They must pass with no allow-file entry**: Task 10 set `cluster-fallback = keep`,
so an unattested cluster flags `UNATTESTED_CLUSTER:` rather than `UNREPAIRED`. An `UNREPAIRED`
here is a real bug in Task 10 — fix the rules, do not add the word to `tests/allow-unrepaired.txt`.

- [ ] **Steps 2–3:** run → FAIL; add `formation_block` and the `except` clause.
- [ ] **Step 4:** regenerate and **read the diff**:

```bash
uv run strands gallery sources/irish/test-words.tsv --out tests/snapshots/gallery.md
git diff --stat tests/snapshots/gallery.md
```

The fifth column and the formation block are the intended change; anything else moving means an
earlier task changed another strand's behaviour, which is a bug.

- [ ] **Step 5:** `uv run pytest -q` → all green, 2 xfailed, **no xpass**. **Commit:**
      `feat(gallery): Old Irish column with lookup flags and an element-built formation block`

**Acceptance:** five columns and the flag marks; the formation block renders from element rows;
every Old Irish output carries exactly one flag, reconstructs to its reported IPA, uses no modern
lenition digraph, carries no leftover ending marker and is initially stressed; the snapshot diff
contains only the intended additions; no new allow-file entries.

---

## Self-review

**Spec coverage.** §1 → Tasks 12, 16. §2 → Tasks 9, 12. §3 → Tasks 2, 3, 4. §4 → Tasks 8, 9, 10 +
5, 6. §5 → Tasks 13, 14, 15. §6 → Tasks 11, 7, 12. §7 → Tasks 2/3/4, 16, 13/14/15, 18. §8 → O1 in
O-13 + Task 16; O2 in O-14 + Task 7; O3 in Task 12's `infer_stem`; O4 in O-18 + Task 12; O5 in
Task 9; O6 in Task 15. §9 milestones 1–5 → the whole list. §10 → O-13, O-18, O-21, O-22, O-24 and
Tasks 2–4. **§11 → the spelled word is Task 7; citation-form input is O-23 + Task 12; positional
`@orth` is O-6 + Tasks 5, 6; the explicit BROAD↔SLEN map is Task 8; the ending marker is Task 11 +
Task 14; the measured regression population is O-31 + Task 16; the Old Irish builder and article are
Task 15; corrections (i)–(iii) are Tasks 15, 13, 8; the per-class aligner measurement is Task 5.**

**Known deviations, for the owner.**

1. **The third mutation (aspiration/gemination) is not implemented.** Spec §5 names two; digest §9
   open question 10 asks whether the strand should use the third and does not answer. Task 13
   records the omission in the rule file.
2. **Fortis/lenis sonorants are not phonemic (O-2)** and Pokorny's three-way quality is spelling
   only (O-4). Both follow spec §4's inventory and both contradict digest §10.1's own analysis;
   both are commented in the rule file.
3. **The regression's ratcheted denominator is 54**, not "each attested lexicon headword" — only
   rows with hand IPA can be run without the G2P, and the G2P population is deliberately
   un-ratcheted. A consequence the owner should see: **decision O1 (⟨ao⟩ → ⟨áe⟩ vs ⟨óe⟩) has 4
   measurable rows in the ratcheted set and cannot be decided there.**
4. **`ATTESTED:MIr` is carried but nothing branches on it** (O-22), per spec §10's own note that the
   tier is a speculative default.
5. **Sonorant-geminate restoration is not derivable** (R16): *ainm → ainmm*, *cill → cell*,
   *Neasa → Nessa* are lexicon-only. The ⟨cc tt pp⟩ half **is** derivable and Task 11 does it.
6. **Two lexical splits cannot be derived from spelling** and rely on the lexicon's `oi_gen`
   (Task 14's precedence rule 1): the n-stem suffix vowel/gemination (`-ann/-an/-en/-enn`) and the
   u-stem `-o`/`-a`. This is why `[inflect]` consults the lexicon **first**.
7. **Pokorny's lenition-blocking rule (S9)** is not implemented; it is cross-word and would belong
   to Task 15's templates. Commented in Tasks 13 and 15.

**Items from the reviews not applied, with reasons.**

- **R21's "raise it with the owner rather than implement silently"** — spec §11 (i) has since
  *decided* it (MAEL/GILLA unlenited), so Task 15 implements the decision and cites both the spec
  bullet and the attested rows. Nothing is left for the owner to rule on.
- **R19's suggestion to record the *Goídelc* transcription as a conflict** is applied, but the plan
  does **not** adopt `oːi̯`: `wiki-old-irish` §Vowels is the systematic statement and one infobox
  transcription is not a basis for generalizing (Task 10's comment says this).
- **S5's `/æ/` and `/hʲ/`** are added as **marginal** only. They are citeable but neither is used by
  any rule, so admitting them non-marginally would let the inventory fallback choose them.
- **R28's alternative "or record the omission"** is not taken — conv. 4 **is** implemented, as
  `left`-context rows in the grapheme table (Task 7), because *derg*, *long*, *ferg* and *fearg* are
  all lexicon rows and Task 18's round-trip property test would surface the error.
- **S12's second half** (the indeclinable `or`-assertion) is applied by rewriting the test in
  Task 14; the first half is applied in Task 10.
