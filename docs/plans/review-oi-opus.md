# Review: `2026-08-27-old-irish-plan.md` against `2026-08-27-old-irish-design.md` (+ engine §12)

Reviewer: Opus 5, 2026-08-27. Scope as commissioned: spec conformance (§2–§7, §10); linguistic
fidelity of the inventory/lenited series (Tasks 1, 8), the mutation tables (Task 14), the stem-class
paradigms (Task 15), the formation templates (Task 16) and the `[respell]` conventions (Task 11);
the retro-filter's coverage of the harvest log's reversal classes (Task 9); the aligner (Task 5);
the filter-regression denominators (Task 17); dependencies, ordering, task sizing and the
interaction with the concurrently-built `src/strands/g2p.py`. Design decisions (spec §8, §10) taken
as fixed and not relitigated.

Method: the plan was read in full; the digest §10, the lexicon (299 rows) and the harvest log were
read as primary sources; Task 5's aligner was transcribed and **executed** against the real 144
test words; ten real modern↔Old Irish lexicon pairs were hand-run through Task 9's rules as
literally written; twenty-four lexicon rows were hand-run through Task 15's paradigms (via Task 12's
reconstruction and Task 11's respelling); the Task 17 denominators and the Task 2 validation codes
were recomputed from the two data files.

**Overall.** This is a strong plan — the interpretation register (O-1…O-26), the citation
discipline, the explicit "known deviations" section and the decision to keep geminate restoration in
`[respell]` rather than `[substitute]` are all right. Spec coverage is essentially complete: every
§2–§7 and §10 item has a task, and the self-review's coverage map checks out. The problems are
concentrated in four places:

1. **Task 5's orthography table is 42 words short of its own acceptance criterion** (measured:
   68.4% vs the asserted ≥75%), and the three classes it cannot align — epenthetic schwa, doubled
   consonant letters, eclipsis digraphs — are exactly the three largest reversal classes in the
   harvest log. Everything downstream of `@orth` inherits this.
2. **Task 9's rule table is not executable as written** — dead rules, self-contradictory rules,
   broad-only replacements applied to quality-neutral tags, and no handling of the `LEN:` tags that
   O-8 says will overwrite the aligner's tags on every mutated word.
3. **Task 17's stated denominator (74) is wrong**; the real number is 54, and the `ao` regression
   set the plan promises has 4 members in that population, not the ≥15 its own test asserts.
4. **Task 15's paradigms derive 6 of 24 hand-run lexicon genitives**, and three of the plan's own
   ten parametrized paradigm cases fail — largely because Task 12's reconstruction table omits
   digest §10.2 convention 5 (the glide ⟨i⟩ and the post-stress /ə/ grid) entirely.
5. A cluster of **cross-task data inconsistencies** that will make committed tests fail — including
   Task 2's "the committed lexicon has no errors" test, which its own validation table makes false
   on 41 rows.

---

## Required changes

### A. Data and denominators (measured, not estimated)

**R1. Task 17's denominator is 54, not 74, and two of its tests will fail.**
The harvest log's "74 direct hits" counts *all* lexicon statuses. Recomputed from
`rules/old-irish-lexicon.tsv` and `sources/irish/test-words.tsv`:

| population | count |
|---|---|
| distinct test-word keys | 138 |
| direct lexicon hits | 74 |
| …of which `status = none` (no `oi_nom`, excluded by Step 3's own `FORM_STATUSES` filter) | **20** |
| **`attested`/`middle` hits with hand IPA — the actual regression population** | **54** |

`test_the_denominator_is_the_direct_test_word_overlap` asserts `>= 70` and will fail. Task 4 adds
10–20 `middle` rows, of which only a fraction are test words, so the number will not reach 70.
Restate the table, the prose ("the 74-row overlap"), the commit message, the acceptance criterion
and Known Deviation 4.

**R2. The ⟨ao⟩ regression set does not exist in the ratcheted population.** O-13 and spec §10 make
"the 20 attested ⟨ao⟩ pairs" a named regression set in Task 17, and
`test_the_ao_class_is_decision_O1s_regression_set` asserts `total >= 15`. Measured over the 54-row
population: **4**. The 20 pairs exist only across the whole lexicon, i.e. only in the `g2p`-widened
population — which the plan deliberately excludes from the ratchet. Either (a) state that the O1
measurement lives in the `constructed=True` population and depends on the G2P (a dependency the
brief says not to take), or (b) drop the assertion to what the hand-IPA population supports and say
in the module docstring that O1 cannot be measured without a G2P. Do not leave the assertion at 15.
Other measured class sizes over the 54: quality-digraph 21, geminate 12, ch-th 9, final-vowel 9,
lenition-digraph 7, ua-ia 4, an-suffix 3, r-stem 1. The plan's parenthetical counts (~50, ~49, 51,
47, 33) are whole-lexicon numbers and should be labelled as such.

**R3. `rules/old-irish-lexicon.verification.tsv` does not exist.** The File structure block and
O-24 both say it does ("EXISTS — the first (35-row) verification pass"). The first pass is recorded
as a prose table in `rules/old-irish-lexicon-log.md` §"Sample verification". Task 3 is told to
create `…verification2.tsv` with a header that has no `verification.tsv` to match. Fix the file
structure, and say whether Task 3 should also back-fill the first pass into a TSV.

**R3a. Task 2's `check` rules make the committed lexicon red, contradicting Task 2's own test.**
`test_the_committed_lexicon_has_no_errors` asserts zero `severity == "error"` findings on
`rules/old-irish-lexicon.tsv` as committed. Under Task 2's own validation table it will produce, on
today's file:

| code | rows | why |
|---|---|---|
| `LEX_NONE_NO_KIND` | **29** | Task 2 adds the `kind` column "leaving every cell empty; the values are Task 3's", but the code makes an empty `kind` on a `none` row an *error* |
| `LEX_IRREGULAR_NO_GEN` | **11** | `Cú Chonnacht, Dubh-dá-leithe, Fear Diad, gasúr, Giolla, Giolla Pádraig, Giolla Íosa, Maol Coluim, Maol Muire, Maol Seachlainn, Muircheartach` are `stem = irregular` with an empty `oi_gen` |
| `LEX_NONE_HAS_FORM` | **1** | `gasúr` is `status = none` **and** `stem = irregular` |

Either give these three the `LEX_NEEDS_TASK3` warning treatment for the pre-Task-3 state, or move
the assertion to "no errors other than …" and make Task 3 close them. Note also that ten of the
eleven `irregular`-without-genitive rows are multi-word formation names (*Máel Coluim*, *Gilla
Pátraic*, *Fer Diad*, *Dub dá Leithe*, *Cú Chonnacht*, *Gilla Isa*, *Máel Muire*, *Máel
Sechnaill*): they arguably want a status or stem value of their own rather than `irregular`, and
Task 3 should be told so explicitly.

**R4. Hard-coded row counts will break across tasks.** Task 2's committed-file tests assert
`len(FILE_ROWS) == 299`, `attested == 270`, `none == 29`, `oi_gen == 163` (all four verified
correct today). Task 4 adds 10–20 rows and Task 3 Part C may `remove` rows — so Task 2's tests
break at Task 4, and Task 4's own `test_the_middle_tier_did_not_disturb_the_attested_counts`
(`attested == 270`) breaks if Task 3 removed anything. Either make Task 2's counts a lower bound /
move them into Task 3's and Task 4's own acceptance, or state explicitly in Tasks 3 and 4 that they
update Task 2's numbers. Also: Task 4's `assert check_lexicon_file(PATH) == []` demands *zero
findings*, but Task 3 Part B explicitly leaves `LEX_NEEDS_TASK3` **warnings** on rows that are
nouns and simply lack data. Task 2's own equivalent test correctly filters to `severity == "error"`.
Make Task 4 match. (Minor: Task 3 says "96 blank-gender rows"; the file has 97.)

### B. The aligner and `@orth` (Tasks 5–7) — the load-bearing machinery

**R5. Task 5 does not meet its own coverage floor.** Running the plan's exact algorithm and its
exact table over the real corpus: **91/133 = 68.4%**, against an asserted `>= 99` (≥75%). The 42
failures are: epenthetic schwa 14, eclipsis digraphs 10, doubled letters ⟨nn ll rr⟩ 7, missing
units/vowel values 11. Adding ~30 rows (`mb gc nd bp dt bhf ng`; `nn ll rr mm`; `eo eoi ío iú aí oí
uí`; `adh agh abh amh eabh eadh`; epenthesis alternatives `r → ɾˠ+ə`, `l → l̪ˠ+ə`, `n → n̪ˠ+ə`,
`m → mˠ+ə`) reaches **129/133 = 97.0%**. So the floor is reachable, but the table the plan presents
as "the whole file" is roughly 60% short. Write the missing rows into the plan rather than leaving
Step 6 as an open-ended "keep adding rows until the counter passes" loop.

**R6. Three of Task 5's own hand-written positive assertions fail as written.** `tags()` (the test
helper) skips `normalize`, so input aliases never reach canonical form:
`tags("Seán","ʃaːnˠ")`, `tags("dhún","ɣuːnˠ")` and `tags("t-éan","tʲeːnˠ")` all return
`("","",…)`. The real call site (Task 13) does `normalize` → `tag_word`. Make `tags()` normalize.
Task 7's `test_an_inserted_prothesis_segment_is_tagged_with_a_zero_radical` has the same defect and
passes only because an all-`""` tuple is truthy.

**R7. `Word.orth` is silently dropped by `irish._join`.** Task 5's Files list names `replaced()`,
`split_words()` and `traced()`, but not `_join`, which constructs `Word(...)` literally at
`src/strands/irish.py:192` (also 286, 346, 353) and therefore resets `orth` to `()`. Every
construction built by `build_construction` loses its tags — i.e. the whole `a Sheáin` / `an tsúil` /
`deich bpeann` path. Add `_join` with the concatenation rule and a decision on the
one-side-empty case (padding with `""` is the only length-safe option).

**R8. Epenthesis and eclipsis are unreachable by both tag mechanisms.** The ten eclipsed test words
(*mbean, bpeann, gceann, dteach, ndroim, nglúin, bhfreagra, ngasúr, ngeata, mbláth*) arrive in the
corpus **already mutated**, so they go down the retro path where `apply_mutation` never runs and
Task 7's `ECL:` tags are never written — and the aligner has no `mb gc nd …` rows either. Add the
rows, and say in Task 9 that `@orth("ECL:…")` covers only construction-built words. Likewise,
spec §4's sound-driven bullet ("other schwa → *a/e* **by the modern spelling**") needs a tag on the
schwa, which the table cannot produce.

**R9. Dead `@orth` rules are not caught.** Task 6 makes an unknown unit a *warning*
(`ORTH_UNKNOWN_UNIT`) and makes `Checker.matching_segments` return `[]` for orth items, so
`RULE_NEVER_MATCHES` cannot fire either. Combined with R10 below, `@orth("ai")` is dead code that
nothing reports. Either make an unknown unit an error, or add a test that every `@orth` unit
referenced by `old-irish.rules` is a unit of `rules/irish-orthography.tsv`.

### C. Task 9, the retro-filter

**R10. `@orth("ai")` targets a unit that does not exist.** The Task 5 table has no `ai` row (it
lists `ái` twice and never `ai`), so every ⟨ai⟩ tags as `a` — measured: *caisleán* → `c a s l eá n`.
Task 9's rule is dead, and spec §10's last bullet names ⟨ai⟩ as part of the largest reversal class.
Either add `ai` to the table (noting that longest-first ordering will re-baseline tags corpus-wide)
or drop the line.

**R11. Task 9 violates spec §4's explicit non-reversal list in two ways.**
- *Vowel length.* The table gives `ea → a aː ɑ` and `io → ɪ iː`, so `@orth("ea") -> e` and
  `@orth("io") -> i` shorten long vowels. Split each into a length-preserving pair.
- *Broad/slender quality.* `@orth("ch") -> x`, `@orth("ph") -> fˠ`, `@orth("th") -> θ`,
  `@orth("dh") -> ð`, `@orth("sh") -> h` are single broad-only replacements applied to tags that
  match both qualities: slender `ç` (*cheann*, *oíche*) becomes broad `x`, `fʲ` (*pheann*) becomes
  `fˠ`, and `θʲ`/`ðʲ` — the feature rows Task 1 adds *for this purpose* — are never produced. The
  prose at line 2308 claims "slender partners get their own line in each case"; the table does not.
  Write the four-line shape for all of them, and key it on the **source segment**, not the
  neighbouring vowel (the current four-line shape at 2315–2318 discards the quality the source
  segment already carries, and matches none of its four lines when the neighbour is `ə` or a
  consonant — *Niamh* /nʲiəw/ is exactly that case).

**R12. The ⟨ua ia⟩ rules are mutually contradictory and unexecutable.** Lines 2300–2302 give both
`@orth("ua") -> uː` and `@orth("ua") -> u` (same for `ia`) against the same tag, and "on the
**first** element only" has no expression in the rule — the aligner gives *both* segments the
identical tag (verified: *Niamh* → `n ia ia mh`). Write explicit contexts and reconcile with
Task 11 rule 8, which needs the **two-segment** `i ə` / `u ə` to survive into `[respell]` — the
single-segment `iː`/`uː` of Task 9 makes ⟨ía úa⟩ unwritable. This is a 33-pair class.

**R13. O-13's chosen ⟨áe⟩ default is unwritable.** `@orth("ao") -> aː` produces a single `aː`,
which Task 11 rule 7 respells as ⟨á⟩. There is no `[respell]` rule producing ⟨áe⟩ or ⟨óe⟩ at all
(rule 8 lists only the eight diphthongs). Add the spelling, or state that the filter's ⟨ao⟩ output
is ⟨á⟩ and amend O-13.

**R14. Task 9 does not handle `LEN:<radical>` tags, which is where the design's central claim
fails.** O-8 says `apply_mutation` **overwrites** the aligner tag. So in any leniting construction,
*bhean* / *mhór* / *dhorn* arrive tagged `LEN:bˠ` / `LEN:mˠ` / `LEN:d̪ˠ` — the `@orth("bh")` family
cannot fire, and the fallback `w/vˠ/vʲ -> β` collapses exactly the *b*/*m* distinction the `@orth`
atom exists to preserve. Task 9's tests hide this because `retro()` calls `tag_word` and never
`apply_mutation`. Add the `LEN:` reversals or state the limitation explicitly.

**R15. The eclipsis reversals cover broad radicals only.** `ECL:pˠ bˠ d̪ˠ ɡ` are written; missing
are `ECL:pʲ bʲ tʲ dʲ c ɟ` (*bpeann, mbean, dteach, gceann, ngeata* are all test words) and
`ECL:fˠ/fʲ` for ⟨bhf⟩ (*bhfreagra* currently falls through to `vʲ -> βʲ` and respells as ⟨b⟩).

**R16. Two reversal classes have a rule in neither Task 9 nor Task 11.** Task 9 defers geminate
restoration and ⟨-a⟩ → ⟨-ae⟩ to Task 11 (correctly, to avoid Task 10's degemination). But Task 11
rule 4 covers only the *voiceless-stop* half of the geminate class (`mac → macc`); rule 5 requires
two identical segments for ⟨ll nn rr mm⟩, which nothing upstream ever produces — so *ainm → ainmm*,
*droim → druimm*, *cill → cell*, *bainne → bannae*, *Neasa → Nessa*, *croiceann → croiccenn* have no
rule anywhere. And Task 11 §41 covers final `e i` after a broad consonant, not final `a` — so
*cara → carae*, *sneachta → snechtae*, *freagra → frecrae* cannot be produced, though the log calls
⟨-a⟩ → ⟨-ae⟩ "the commonest single reversal". One of the two tasks must own both.

**R17. Task 9's blanket `%design` assertion contradicts spec §4.** Lines 2286–2287 assert "no pair
does yet, so every line in this task is `%design`", enforced by
`test_every_substitute_line_is_tagged_design_with_a_citation`. Spec §4 says `%design` "**unless a
lexicon pair instantiates the change** (then the citation is added and the tag is `%attested`)" —
and the plan's own rule table two lines later cites "50 attested pairs" and "33 pairs". As written
the test locks the file into `%design` permanently. Make the test "every line carries a citation".

**R18. Test fixtures drawn from non-lexicon or `none` rows.** `retro("waːd̪ˠ","bhád")` — *bád* is a
`status = none` loan row; `retro("ɣaːɾˠd̪ˠaː","gharda")` — *garda* is not in the lexicon and the rule
is an identity, so the assertion is vacuous; the two eclipsis tests use *páirc* (absent) and *bád*;
`retro("sʲaːnˠ","Seán")` uses `sʲ`, which is not a `features.tsv` row (the segment is `ʃ`), on
another `none` row. Spec §7 requires "each reversal rule against a lexicon pair". Replace with real
pairs: ⟨bh⟩ *dubh ~ dub* / *sliabh ~ slíab*; ⟨gh⟩ *Lughaidh ~ Lugaid*; ⟨ao⟩ *aon ~ óen* /
*caol ~ coíl*; the digraph class *bean ~ ben* / *dearg ~ derg*; ⟨ua ia⟩ *tuath ~ túath* /
*iasc ~ íasc*; the invariance cases *athair*, *cloch*, *bláth*. Also
`test_modern_ao_becomes_long_a_by_default` uses *saoil*, which aligns as `aoi` and therefore tests
the wrong rule (and *saol ~ saegul* is one of the log's "neither" cases).

### D. Linguistic fidelity

**R19. The diphthong IPA values are wrong and uncited.** Task 10 declares
`nuclei = aːi oːi uːi aːu eːu iu iə uə`, justified as "the acute is length on the first element" —
which is self-refuting for ⟨aí oí uí⟩, where the acute is on the *second* letter. Digest §10.8
conflict 5 quotes Pokorny writing ⟨aí (áe)⟩ *precisely* "in order to distinguish these diphthongs
from long *á, ó, ú*, followed by a palatal glide" — `aːi` is exactly what ⟨aí⟩ is not. And `iə`/`uə`
for ⟨ía úa⟩ are the *modern* values, using a `ə` this file declares to be the unstressed-reduction
vowel. `wiki-old-irish` §Vowels lists them as **ai oi ui au eu iu ia ua**. The *set* of eight is
right; the values are not. This propagates to Task 11 rule 8, Task 12's table and Task 9's
⟨ua ia⟩ reversal, and the round-trip test will bake it in. (The `Goídelc` [ˈɡoːi̯ðʲelɡ] infobox
transcription in digest §10.6 is the one counter-datum; record it as a conflict rather than
generalising from it.) Separately: the nuclei list has no `əi`/`əu`, which modern Irish has and the
filter can pass through (*Tadhg* /t̪ˠəiɡ/).

**R20. Task 14's mutation rules omit the `/ #_` environment.** `irish.rules [mutations]` writes
every line as `pˠ -> fˠ / #_`; Task 14's tables state no environment. Without it lenition applies
word-internally and the plan's own test fails: `spelling_to_ipa("mac")` = (`mˠ`,`a`,`ɡ`), LEN gives
(`β̃`,`a`,`ɣ`), respell gives ⟨mag⟩, so `test_lenition_of_b_d_g_m_is_not_written("mac")` breaks.
State `/ #_` on every line.

**R21. `MAEL` should not lenite.** Spec §5 and the plan both produce *máel Choluim*. Every attested
instance in this repo's own lexicon says otherwise — rows 203–205: `Máel Coluim`, `Máel Muire`,
`Máel Sechnaill`, all cited, none lenited; *Sechnaill* is decisive, since later-OI ⟨ṡ⟩ *is* written.
It also follows from digest §10.4's trigger table: *máel* here is a masculine nominative, which
triggers nothing (unlike *ingen*, a feminine nominative, which does). This contradicts a spec
sentence, so it is the owner's call — but it should be raised, not implemented silently. Three
places change if taken: the template line, the parametrized expectation, and
`test_a_leniting_formation_lenites_and_a_non_leniting_one_does_not`, which uses MAEL as its
leniting exemplar (swap in `CU` or `INGEN`). `CU` keeping lenition is attested and fine.

**R22. `OF = NAME " " ART(GEN(NOUN))` cannot work in this strand.** `ART` is hardcoded modern Irish
in `src/strands/irish.py:257–291`: it emits *an* / *na* and calls `apply_mutation(…, "HPREF")` and
`"TPREF"` — the two tables Task 14's own test forbids (`set(OI.mutations) == {"LEN","NAS"}`). Old
Irish needs *in / ind / int / inna* (digest §10.4). No task modifies `_article` and no test covers
`OF`. Either add an Old Irish article path (with the ⟨-d⟩/⟨-t⟩ sandhi and the digest §10.4 CONFLICT
that Pokorny restricts final ⟨-d⟩ to "before vowels or aspirated *f, l, n, r*"), or drop `OF` from
this strand explicitly.

**R23. The vocative is applied as if every name were an o-stem.** `VOC = "a" LEN(VOC_O(NAME))`
hard-wires the palatalising table, and `apply_case`'s precedence rule 4 falls back to `VOC_O` for
any class with no entry. Digest §10.5 states the opposite default: "**The vocative has in the
singular the same form as the nominative**… The masculine o-stem and io-stem are the exceptions"
[pokorny1914 p.65 §142]. As written this yields *a Brigte* for *a Brigit* and *a thúaithe* for
*a thúaith*. The fallback must be identity; `irish.rules`'s conditional form (`VOC_M1?`) already
expresses this. The particle *a* + lenition itself is correct.

**R24. Lenited /f/ can never surface as ⟨ḟ⟩.** `LEN: fˠ fʲ → 0` deletes the segment, and Task 7
specifies that a deleted radical leaves no tag, so `[respell]` has nothing to key on and
`mut("fer","LEN")` is always ⟨er⟩. The Task 14 test hides this by accepting `in ("ḟer","er")`.
Spec §6 requires ⟨ḟ⟩ under `punctum = on`. Decide it (null-but-tagged placeholder, word-level
provenance, or amend spec §6). The /s/ → /h/ case is fine.

**R25. The nasalized voiced stops contradict the digest's own master table.** Task 14 gives
`bˠ → mˠ bˠ`, `d̪ˠ → n̪ˠ d̪ˠ`, `ɡ → ŋ ɡ` (two segments), citing pokorny1914 p.10 §21 — but digest
§10.4's rendering of that section reads "/b/ → /m/ ⟨mb⟩; /d/ → /N/ ⟨nd⟩; /ɡ/ → /ŋ/ ⟨ng⟩" (a single
nasal), and §10.2's master table agrees ("b … Initial eclipsed ⟨mb⟩ **/m/**"). Only the §10.4
contrast-set row (*a m-bo* /a mbo/) supports a cluster. This is load-bearing: O-11 reconstructs the
reported IPA *from the written form*, so Task 12's table must agree with whichever is chosen, and
the strand would otherwise emit /mb/ where the source says /m/. Pick one and record the
digest-internal conflict in the rule comment.

**R26. O-1's "/ɣʲ/ is the existing `j`" is featurally false.** For /xʲ/ = `ç` it is exact (`ç` and
`x` differ only in `front`). `j` is `sonorant +, consonantal −, approximant +` — a glide, not the
fricative digest §10.1 charts. The plan's own Task 1 test conspicuously omits the `x/ç` and `ɣ/j`
pairs from `test_slender_partners_differ_only_in_the_I41_quality_features`, and Task 15 already
works around it. Reuse may still be the right pragmatic call; say so as a *substitution*, not an
identity, or add a `ʝ`/`ɣʲ` row — otherwise any `[C +continuant −sonorant]` bundle over the lenited
series silently misses it.

**R27. Task 11's tests use segments outside the declared inventory, and contradict Task 12.**
`spell("d","u","β")`, `spell("k","l","o","x")`, `spell("b","l","aː","θ")`, `spell("s","o","n̪ˠ","n̪ˠ")`
use plain `d b l s`, which Task 8's `[inventory]` does not contain (they appear only inside the
`UNMARKED` class, which the plan itself says may name non-inventory segments). Task 12 asserts the
same words as `("d̪ˠ","u","β")` and `("k","l̪ˠ","o","x")`, and its round-trip test requires
`respell(spelling_to_ipa("dub")) == "dub"` — so the two tasks disagree about the alphabet, and
Task 19's `test_every_output_segment_is_in_the_target_inventory` would fail. Rewrite Task 11's
fixtures in Task 12's segments.

**R28. Digest §10.2 convention 4 is not implemented anywhere.** Stops after ⟨l n r m⟩ are
genuinely ambiguous: *long* /Loŋɡ/, *delg* /dʲelɡ/, *bind*, *cerd*, *imb* /imʲbʲ/ vs *delb*
/dʲelv/, *marb* /marv/. Task 12's table applies a blanket noninitial ⟨b d g⟩ → `β ð ɣ`, so
*derg*, *long*, *ferg*, *fearg* — all lexicon rows — reconstruct wrongly, and the Task 19
round-trip property test will surface it. The convention is stated with worked examples and rules
of thumb in the digest; implement it or record the omission.

**R29. Task 15's paradigm table is broken in seven distinct ways; hand-run, 6 of 24 rows derive.**
Twenty-four lexicon rows were run literally through `spelling_to_ipa` (Task 12) → the `GEN_*` rule
(Task 15) → `respell` (Task 11). Six matched. The failures are systematic, not incidental, and
**three of the plan's own ten parametrized paradigm cases fail** (`GEN_VELAR`, `GEN_R`, `GEN_S`):

- **`GEN_VELAR` and `GEN_DENT` add the wrong segments.** These are IPA-segment rules, but the
  endings are stated orthographically. Task 11 rule 4 writes non-initial `ɡ` as ⟨c⟩ and non-initial
  `t̪ˠ` as ⟨tt⟩ — so *rí* + `ɡ` respells **⟨ríc⟩** and *carae* + `a t̪ˠ` respells **⟨…att⟩**. The
  endings must be `/ɣ/` and `/a d̪ˠ/`, which is also the correct phonology (*ríg* /rʲiːɣ/, *carat*
  /karad/, digest §10.2 conv. 2). This trap applies to every ending stated as a letter.
- **`GEN_R`'s "+ `ar`" is a duplication**: *athair* + *ar* = \**athairar*. Once the glide ⟨i⟩ is
  handled (R29a), plain depalatalization gives *athar, máthar, bráthar*. Delete the affix.
- **`GEN_DENT` must *replace* the final vowel, not append**: *carae → carat*, *fili → filed*,
  *Núadu → Núadat*, *teine → teined* — and the vowel is not always *a*.
- **The stressed-vowel change is missing from `GEN_O` and `GEN_S`.** The plan anticipates a vowel
  rule only for `GEN_I`/`GEN_U`, but `GEN_O`'s own headline example needs one: /fʲ e ɾʲ/ respells
  *feir*, not *fir*. The same e→i raising drives *cell → cille*, *cenn → cinn*, *nem → nime*.
- **`GEN_O` is undefined for vowel-final stems.** O-21 folds io-stems into `o`, so it must handle
  *céile → céili*, *cride → cridi*, *duine → duini*, *uisce → uisci*, *bannae → bannai*,
  *snechtae → snechtai* — a final-vowel change with no consonant to palatalize. `MAC`'s own test
  slot (*Nessa*) hits exactly this. Likewise `GEN_A` absorbing iā-stems (*guide → guide*: identity,
  but the rule appends `ə`).
- **The *-ach* class needs its own line.** *Cellach → Cellaig*, *toísech → toísig*: final /x/
  becomes **/ɣʲ/** (lenis and slender), not /ç/. "Palatalize the final consonant" gives
  \**Cellaich*. This is the productive class spec §5 singles out, so `GEN_O_ADJ` must state it.
- **Geminates break.** "Palatalize the final consonant" on *ball* /bal̪ˠl̪ˠ/ leaves a mixed
  `l̪ˠ lʲ` pair that Task 11 rule 5's "a repeated `l̪ˠ l̪ˠ`" no longer matches. Both halves must
  change together (*ball → baill*, *cenn → cinn*, *cill → cille*, *penn*, *crann*).

Structural coverage against the lexicon's 163 genitives, treating "derivable" generously:
o-stem 36/58, ā-stem ~12/30, u-stem 8/12, **i-stem 0/10, dental 0/4, n-stem 1/16** (`GEN_N`'s
"+ `on`" fits the *brithem* subtype only, not the *Ériu/Érenn*, *Bricriu/Bricrenn*, *Albu/Alban*
subtype, which is 14 of the 16). At runtime precedence rule 1 rescues all of these, since they have
an attested `oi_gen` — the exposure is the RETRO path and the plan's own paradigm tests. Two smaller
points: `GEN_U` hard-codes ⟨-o⟩ where the digest gives ⟨-o/-a⟩ (3 of 12 lexicon rows take ⟨-a⟩); and
the ā-stem group *adarc → adarcae*, *ferg → fergae*, *long → lungae* takes a bare ⟨-ae⟩ with no
palatalization, which does not fit the *túath/túaithe* paradigm at all and is worth a lexicon
re-check in Task 3.

**R29a. Task 12's reconstruction table omits digest §10.2 convention 5 entirely — and it is the
upstream cause of most of R29.** The table maps every vowel letter to a full vowel. It has no rows
for:
- the **glide ⟨i⟩** (*muir*, *cnáim*, *súil*, *flaith*, *athair*), which becomes a spurious /i/
  segment — this alone breaks `GEN_I` and `GEN_R` outright, and it contradicts Task 11's own test
  `spell("mˠ","u","ɾʲ") == "muir"`;
- **post-stress /ə/** written ⟨a ai e i⟩ — so *claideb* reconstructs with /e/, the Task 11 schwa
  grid never fires, and even the nominative fails to round-trip (*claideb* → *claideib*);
- **§40/§41 final ⟨-ae -ai -ea -eo -iu⟩** — ⟨ae⟩ is absent, though Task 11's own test asserts the
  reverse mapping exists (`spell("k","a","ɾˠ","ə").endswith("ae")`);
- **⟨ss⟩**, which the lexicon contains (*Nessa*, *Fergusso*).

**R29b. Task 12's quality post-pass is not the digest's rule.** "Following first, else preceding,
∈ {i e iː eː}" slenderizes any final consonant after ⟨e⟩. Digest §10.2 conv. 5 says: slender
**before** ⟨e é i í⟩, or **after** ⟨i⟩ with no following vowel. As specified,
`spelling_to_ipa("fer")` = /fʲ e ɾʲ/ and `("bec")` = /bʲ e ɟ/ — both wrong, and both are in the
plan's own round-trip test. The post-pass also splits geminates (*Érenn* → `nʲ n̪ˠ`, *cell* →
`lʲ l̪ˠ`); it must treat a geminate as one unit. Separately, the round-trip test's eight
monosyllables are exactly the set that hides all of these gaps — add *claideb*, *carae*, *muir*,
*dígal*, *brithem*.

**R29c. Task 11's Step 3 rule order contradicts its own next sentence.** The list reads
"6 → 1 → 2 → 3 → 4 → 5 → **7 → 8** → 9 → 10"; the sentence immediately after says "the diphthong
rules (8) must precede the single-vowel length rules (7)". The list is the thing an implementer
will follow. Make it … 5 → **8 → 7** → 9 → 10.

**R29d. Two `[respell]` rules spec §6 and Task 15 both need are absent.**
- **§37, the intervocalic i-glide.** Only §36 (word-/syllable-final) is implemented. But every
  `GEN_A`/`GEN_S` output is *…Cʲ + ə*, where the slender consonant is an onset: *túaithe*,
  *cloiche*, *nime*, *cille*, *sróine*. Without §37 the `GEN_A` acceptance test cannot pass.
  Pokorny calls §37 irregular, so it needs a `%design` tag and a stated scope.
- **Nothing writes word-final /ə/.** Rule 10's grid requires a following consonant, and §41 is
  about final ⟨e i⟩ letters, not /ə/. Add the two final-ə lines (broad → ⟨ae⟩, slender → ⟨e⟩) and
  state that the §36 glide must not fire before them, or *claidib* becomes \**claidiib*.

### E. Plumbing and coverage gaps

**R30. `DESC+ADJ` / `DESC+NOUN` are unhandled on the Old Irish path.** `pipeline.CONSTRUCTIONS`
contains both, `parse_construction` returns `(name, slot)`, and `run_entry` resolves the epithet
before `adapt`. Task 8 correctly declares no `epithet-ADJ`/`epithet-NOUN`, but Task 13's
`run_entry_oi` signature and body never mention `parse_construction`, the slot, or `affix_epithet`,
and Task 16 does not add them. `--construction all` and the gallery will exercise both. State the
behaviour (an unmapped slot is "no affix", so `DESC+ADJ` should equal `DESC`) and test it.

**R31. Task 19's formation block has no source of modern IPA.** It renders "the five attested
example names… taken from the lexicon by their modern keys" — *Maol Coluim*, *Giolla Pádraig*,
*Fear Diad*, *Dubh-dá-leithe*, *Cú Chulainn*. None of these is a row of `sources/irish/test-words.tsv`
(only *Colm* and *Pádraig* are), and `render_gallery` takes `Entry` objects with IPA. Say where the
`Entry` comes from. Note also that all five *are* whole-name lexicon rows, so the lookup returns
them `ATTESTED` as a unit and the formation template is never exercised — spec §7 wants the
templates tested, which means building them from the **element** rows (*Maol → máel*,
*Colm → Colum*, *Pádraig → Pátraic*, *cú*, *fear → fer*). Task 16's own parametrized test does not
do this either: it passes *Niall*'s IPA for every word, expects `"fer "` (trailing space, empty
second element) for a headword *Diarmaid* that is not the *Fer Diad* element, expects
⟨gilla Patraic⟩ where the lexicon has *Pátraic*, and uses *Culann*, which is not a lexicon row.
Rewrite it against real element rows. Concretely: the **head** elements all exist — *máel* (`Maol`,
ā f, gen *maíle*), *gilla* (`Giolla`), *cú* (`cú`, n m, gen *con*), *fer* (`fear`, o m, gen *fir*),
*macc* (`mac`, o m, gen *maicc*), *ingen* (`inion`, ā f, gen *ingine*) — but **`Culann`, `Diad` and
`Leithe` are not in the lexicon at all**, so two of the five parametrized cases `pytest.skip`, one
(`FER`) has the empty expectation `"fer "` that asserts nothing, and spec §7's requirement to test
against *Cú Chulainn* and *Fer Diad* is simply not met.

**R31a. `COLOUR` cannot produce *Dub-dá-leithe*.** The attested form is three elements
(`Dub dá Leithe`); the template `COLOUR LEN(NAME)` is two-slot and emits no hyphen. Cite a real
two-element compound (*Dubthach*, *Donnchad*) or drop the claim. Relatedly, spec §5 and the digest
write the element *Find-* while the lexicon's `Fionn` row gives `Finn`, so the template would emit
*Finn-*.

**R31b. `Pádraig` needs `stem = indecl`.** Digest §10.5 lists *Patraic* explicitly among the
indeclinable nouns, but the lexicon row has an empty `stem`, so Task 15's precedence rule 4 falls
back to `GEN_O` and *derives* a genitive for it — inside the `GILLA` test. Also pick one spelling:
lexicon *Pátraic*, digest *Patraic*, spec §7 *Gilla Pátraic*, the test *"gilla Patraic"*.

**R31c. Capitalization is unspecified.** All `respell` output is lowercase, but Task 16's tests
assert `"Ch"`, `"Pa"`, `"Nessa"`. Either the tests casefold, or the plan must say where a name is
re-capitalized.

**R31d. 63 attested lexicon rows have a blank `stem` and get a silent o-stem guess.** `infer_stem`
never returns empty, so `apply_case`'s precedence rule 4 (`case:{case}-fallback-o`) is reachable
*only* for lexicon rows with a blank `stem` — of which there are 63 `attested` (plus the 37
`irregular`). Those are ATTESTED hits that take an o-stem guess with **no** `assumptions` tag,
because O-21 says a lexicon-supplied class contributes no tag. Either route blank-stem lexicon rows
through `infer_stem` too, or make the fallback emit its own assumption. Task 3 is meant to fill
these in, but Task 15's behaviour on them is a decision, not a leftover, and should be stated.

**R32. The citation constraint is not enforced where it matters.**
`test_every_rule_line_carries_a_citation` iterates `OI.sections` — but `mutations`, `inflect` and
`templates` are **separate fields** on `RuleFile` (`src/strands/dsl.py:172–193`), so Tasks 14, 15
and 16 are entirely unchecked. Extend it over `OI.mutations` and `OI.inflect`, plus a text-level
check for `[templates]`. Relatedly, Task 9's citation form (`# design: spec §4 · digest §10.2
conv.1`) does not match the Global Constraint's `# design: O<n>`; either broaden the constraint or
renumber to the O-rows the rules implement.

**R33. Task 9 also edits `old-irish.rules`, but the parallelism note omits it.** "Tasks 8, 10, 11,
14 all edit `old-irish.rules` and must run in the listed order" — Tasks 9, 15 and 16 do too. As
written, Task 9 (depends on 6, 7, 8) could run concurrently with Task 10 (depends on 8) and
conflict. State the full serialisation on that file.

---

## Suggestions

- **S1. `ia`/`ua` tags are position-blind.** The aligner gives both segments the same tag
  (*Niamh* → `n ia ia mh`); only a phonological context (`_ ə` vs `i _`) can separate them. Worth a
  sentence so an implementer does not try to encode position in the tag.
- **S2. Task 5's Step 6 remedy loop is unguarded.** There is no test that any tag is *correct*
  beyond the eleven hand cases, so an agent optimising the counter can add `-` (silent) to every
  consonant and destroy tag fidelity. Add pinned expected-tag assertions from the real corpus —
  *naomh* → `n ao mh`, *Caoimhe* → `c aoi mh e`, *dubh* → `d u bh`, *sneachta* → `s n ea ch t a` all
  pass under the plan's current table.
- **S3. Dead/duplicate table entries.** `ái` appears twice (lines 1348, 1358). `ea → ɑ` and `a → ɑ`
  never match after `normalize` (`irish.rules` folds `ɑ → a`). `io → ɪ iː` and `iu → ʊ uː` never
  match the accented spellings ⟨ío iú⟩ the corpus actually contains (*stríoc*, *ciúin*, *leisciúil*),
  which currently align by an accidental `í` + silent-`o` route, producing tag `í` where Task 9
  wants `io`.
- **S4. `none`-row `kind` classification.** O-18's list follows the log, but *spraoi* ("borrowed
  directly from Old Norse") and *gasúr* ("loanword… post-OI borrowing") are classed `late` while
  their own notes call them loans. Worth an explicit review pass in Task 3 rather than transcribing
  the log's split.
- **S5. Inventory gaps, both citeable.** `/hʲ/` (digest §10.1: "may have been the same sound as /h/
  or /xʲ/") and the marginal short `/æ ~ œ/` (from u-infection of stressed /a/, "rampant in names in
  the prefix *air-*" — i.e. name-relevant; both rows already exist in `features.tsv`).
- **S6. `w` is not an Old Irish phoneme.** Digest §10.1 has no /w/. Task 9 rewrites any survivor, so
  mark it `marginal:` rather than a full inventory member; its slender partner `vʲ` is in neither
  the inventory nor `SLEN`, an asymmetry `irish.rules` does not have.
- **S7. `pˠ pʲ`** are on the `[inventory]` stops line in Task 8's summary table but only under
  `marginal:` in the rule text. The rule text matches `irish.rules` convention and is the one to
  keep; fix the table.
- **S8. `s₂` (⟨f, ph⟩ from \*sw, \*sɸ) is absent from the LEN table.** Lexical rather than
  rule-derivable, but a "deliberately absent, lexicon only" comment would keep the omission legible
  (digest §10.4 and §10.2 note 1 name the handful of words).
- **S9. Pokorny's lenition-blocking rule is neither implemented nor mentioned** (blocked before
  *d t* when the preceding word ends in *l n s*; blocked after a homorganic consonant,
  pokorny1914 p.9 §19). It bites on `COMPOUND`, `CU`, `COLOUR` — and on `MAEL`, whose *máel* ends in
  /l/, which is a second argument for R21. Cheap to state and testable.
- **S10. `INGEN` need not be blanket `%design`.** The *formula* is unattested, granted; but *ingen*
  is a feminine ā-stem and digest §10.4's trigger table makes nom./voc. sg. of all feminines
  leniting. Split the citation: `%design` for the formula, `%attested` for the mutation. Conversely
  `MAC`/`UA` correctly take no lenition, though digest §10.5 gives io-stem masc. nom. sg. (*céile*ᴴ,
  hence *aue*) the ᴴ mutation this strand drops — worth one comment so the absence reads as a
  decision. Also: O-25 writes the UA element as *aue* while the lexicon row gives *ua*; reconcile.
- **S11. `ADJ = NAME " " LEN_IF_F(ADJ)` undercovers Pokorny §10** (also lenited after a dat. sg.,
  after a voc. sg. of any gender, after a gen. sg. masc./neut. o-stem, after nom. pl. masc.
  o-stem). Nom.-fem.-only is a defensible narrowing, not an error, but say so.
- **S12. Two near-vacuous tests.** `test_a_diphthong_is_one_syllable_not_two` is an `or` of two
  assertions (and `θuːaθ` is not in the nuclei list); `test_an_indeclinable_stem_is_returned_
  unchanged` is likewise an `or`. Both pass without the behaviour they name.
- **S13. Identity assertions with no negative control.** `retro("ɣaːɾˠd̪ˠaː","gharda")[0] == "ɣ"` and
  `@orth("ECL:pˠ") -> bˠ` on an input already holding the expected value pass with no `[substitute]`
  section at all.
- **S14. `@orth("ea")`'s stated semantics are self-contradictory.** The prose says these rules "do
  not change the *segment*, they change what `[respell]` writes for it" — but `-> e` is a segment
  change, and it needs to be (*fear* /fʲaɾˠ/ → *fer* /fʲeɾˠ/). Restate.
- **S15. O-15 wording.** It says the epenthesis environment is "an inline set of the Irish
  sonorants, **not** a feature bundle"; Task 8 declares a `SONORANT` class and Task 9 uses it. The
  implementation is fine; reconcile the wording so nobody rewrites it.
- **S16. ⟨bh⟩/⟨mh⟩ are not always distinct in origin.** *naomh ~ noíb*, *claíomh ~ claideb* are both
  `attested` rows where modern ⟨mh⟩ descends from Old Irish ⟨b⟩. The filter never sees them, but the
  regression will; worth a comment so the split is not over-trusted.
- **S17. `UNMARKED` is dead weight here.** In `irish.rules` it exists as the `[normalize]`
  quality-inference source and nothing else consumes it; `old-irish.rules` has no `[normalize]`.
  Harmless, but worth a comment.
- **S18. `source` column convention.** Existing hand rows in `features.tsv` use `hand:irish`; Task 1
  specifies `hand: old-irish digest §10.1`. Prefer `hand:old-irish`, with the digest reference in
  `features.README.md` where Step 4 already puts it.
- **S19. Add the cheap invariance regressions the log recommends** — the ⟨-án⟩ diminutive
  (*arán ~ arán*, *Colmán ~ Colmán*) and the r-stem kinship set (*athair*, *bráthair*, *máthair*).
  Task 17 has classes for both; Task 9 has no test for either, and they are the best "does the
  filter leave well enough alone" cases in the file.
- **S20. §36's exception list is over-formalized.** The prose quotes Pokorny's exceptions
  (í, é, aí, oí, uí), but the rule `0 -> "i" / [V -front] _ SLEN` additionally blocks the glide
  after short ⟨e⟩ and ⟨i⟩. Blocking after ⟨i⟩ is right; blocking after ⟨e⟩ is not stated by any
  source. Pick one and cite it.
- **S21. State the identity fallback.** No `[respell]` rule writes the short vowels /a e i o u/ or
  /sˠ/. Presumably identity, but rule 4's neighbours are all explicit, so say so.
- **S22. `infer_stem`'s default ignores gender.** "anything else / empty → `o`" makes an
  unclassified feminine an o-stem. Spec §8 row O3's alternative was "always o/**ā by gender**";
  defaulting f → ā costs nothing and sits between the two branches.
- **S23. Fill in the *Nessa* row.** `MAC`'s test slot has no `oi_gen` and an empty `stem`, so the
  derived genitive is undefined. *Nessa* is an ā-stem with gen *Nessa*; filling the row makes the
  digest's own *Conchobar mac Nessa* actually reproducible.

---

## Two spec sentences the plan is right to diverge from

Worth propagating back to `docs/specs/2026-08-27-old-irish-design.md`:

- **Spec §5: nasalized *c t* → *g d* "written".** Digest §10.4 says the opposite — "It is only in
  the case of *b, d, g* and of initial vowels that eclipsis is regularly expressed in writing" — and
  §10.2's master table gives eclipsed initial ⟨c⟩ = /ɡ/ unwritten. Task 14 implements it unwritten
  and tests `mut("tech","NAS") == "tech"`. The plan is right; the spec sentence is the error.
- **Spec §4: "no phonemic /h/, /s f h/ as lenition products only".** Digest §10.1 charts /s/ as
  phonemic on its own minimal pairs (*sonn* /soN/ ~ *son* /son/) and /f/ as a full member (only
  /p pʲ/ is marginal). O-5's resolution — keep them in the inventory, restrict what creates them —
  is the correct reading; the spec sentence should be softened to match.

---

## Things the plan gets right and should not be "fixed"

Recorded so a later reader does not undo them: geminate restoration living in `[respell]` rather
than `[substitute]` (it would otherwise be undone by Task 10's degemination); `[respell]` ordering
8-before-7 so ⟨aí⟩ is claimed before ⟨á⟩; the honest statement that a low filter-regression rate is
the expected outcome and the per-class breakdown is the artefact; excluding the 52 mutated surface
forms from the regression (O-23); excluding the G2P population from the ratchet; `cluster-fallback
= keep` so no allow-file entry is needed; the empty `[post-stress]` with a comment saying why.

## Task sizing and ordering

The dependency graph is acyclic and honest. Sizes are workable — Task 2 (504 plan lines, but mostly
committed test text) and Task 5 (437) are the largest, and both fit one context. Two caveats:
**Task 3** (reclassify 37 rows, exempt ~91, verify ≥30 rows against live pages) and **Task 4**
(revisit 49 headwords against live pages) are described as "small extensions" but are network-bound
research jobs with a per-row judgement; budget them as such, and note that Task 3's own 10%
`fixed`/`removed` gate could stop the plan. See R33 for the `old-irish.rules` serialisation.

## G2P interaction

`src/strands/g2p.py` is **committed** (2760b0e), not uncommitted as the brief supposed. Task 17
handles it correctly: optional keyword, `constructed=True` rows reported separately, ratchet keyed
off `constructed=False`, and an `importorskip` test. The only coupling problem is R2 — the ⟨ao⟩
regression set the plan promises exists only in the G2P-widened population. Note also that
`src/strands/inputs.py` has **uncommitted** working-tree changes adding the `declension` column
(engine spec §12.K); Task 13's `infer_stem` depends on `Entry.declension`, so that work must land
before Task 13.
