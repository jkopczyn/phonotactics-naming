# Review: `2026-08-25-engine-plan.md` against `2026-08-25-engine-design.md`

Reviewer: Opus 5, 2026-08-25. Scope: spec conformance (§2–§8), DSL EBNF, milestone-6 linguistic
fidelity, test derivability, the repair-testing gap, dependency/ordering and task sizing.
Design decisions (spec §9) taken as fixed and not relitigated.

Overall: the plan is unusually thorough and its interpretation register (I-1…I-30) is the right
device. The problems below are concentrated in three places: (a) the DSL cannot express several
rules spec §7 requires; (b) `features.csv` as specified in Task 1 disagrees in segment *spelling*
and *coverage* with every downstream data file, which would break Tasks 3, 22 and 23–26; (c) the
Task 23–26 citation tables contain a number of claims the digests do not support, several of which
are load-bearing for the "digest-fact tests".

---

## Required changes

### A. DSL expressiveness and EBNF

**R1. The EBNF cannot express three rule types spec §7 mandates.** Hand-parsing the spec's example
lines against the plan's EBNF, the following fail:

| Spec line | Where | Why it fails |
|---|---|---|
| `VOC = "a" LEN(NAME) VOC_M1?` | §3 `[templates]` | `VOC_M1` is a bare item that is neither `quoted`, an `arg-name` (`NAME FATHER NOUN ADJ FIRST SECOND`), nor a `func-call` (no parens). `func-name` lists `VOC_M1`, but `t-item` only admits a func-*call*. The plan copies this line verbatim into Task 18's `irish.rules`, so Task 5 and Task 18 will disagree. Add a bare-function `t-item` alternative (`VOC_M1` = call on the implicit head). |
| `0 -> Vᵢ / Vᵢ C _ {l n r} #` | Task 25, Welsh §3.2 rule (1), *pobl* → [ˈpɔbɔl] | Two failures: `Vᵢ` is an indexed copy variable with no grammar support, and `{l n r}` set-braces are not in the grammar. Copy-epenthesis is not expressible at all. |
| `C θ r # -> C r θ #` | Task 25, Welsh §3.2 rule (3), *ewythr* → [ˈewɨrθ] | Three failures: `#` in target/replacement is forbidden by I-8 and by `target`/`out-item`; class name `C` in a replacement is forbidden (`out-item = SEGMENT \| quoted`); and the DSL has no metathesis primitive. |

Fix: add (i) a copy/index mechanism for epenthesis (e.g. `0 -> V₁ / V₁ C _ LIQ #` with numbered
back-references to matched context atoms), and (ii) either a metathesis rule form
(`TARGET => permutation`) or an explicit statement that Welsh §3.2 rule (3) is enumerated
segment-by-segment. Whichever is chosen, the EBNF, I-8, Task 5's fixture and Task 7's engine tests
must all carry it, because Task 5 and Task 25 will be executed by different agents.

**R2. Class names in replacements — decide and restate.** Spec §7 writes Georgian
`broad non-labial C → C v / _[V +front]`, `slender C → C i / _[V +back]`, and Dutch
`slender C → C j in onsets`. All three put a class name in the replacement, which
`out-item = SEGMENT | quoted` forbids. These *are* expressible as epenthesis
(`0 -> v / [C +back -labial] _ [V +front]`), and that is almost certainly the intent — but the plan
never says so, and Tasks 23 and 26 restate the spec's form unchanged in their rule-block tables. Add
an interpretation (I-31) stating that "C → C x" in spec §7 means an epenthesis rule, and rewrite the
Task 23 and Task 26 table rows accordingly.

**R3. Feature-name shorthand in spec §7 is not valid DSL.** Spec §7 and the Task 23/26 tables use
`[STOP −voice] → [+ejective]` and `[liquid]_C`. `voice`, `ejective` and `liquid` are not among the
38 PHOIBLE column names, so `strands check` (Task 6, check 2) rejects them as `UNKNOWN_FEATURE`.
The real names are `periodicGlottalSource` and `raisedLarynxEjective`; "liquid" must be a declared
class (Task 5's own `mini.rules` correctly declares `LIQ = l r`, and Task 25 correctly uses `[STOP]`
— the plan is inconsistent with itself). Also note spec §7's `−voice` uses U+2212 MINUS SIGN, not
ASCII hyphen. Either add a documented feature-alias table to Task 2 or normalize every §7 fragment
in Tasks 23–26 to real column names; state which.

**R4. I-8 and I-19 contradict each other.** I-8: "`.` and `ˈ` … may appear only in environments,
never in a target or a replacement." I-19: "each target's file ends with `. -> ""` and `ˈ -> ""`" —
and Task 5's `mini.rules` fixture contains exactly those two lines in `[respell]`. Resolve: carve out
`[respell]` from I-8, or replace the cleanup rules with a `strip-marks = on` key in `[respell]`.

**R5. Undefined nonterminals in the EBNF.** `key`, `value`, `name`, `number`, `uppercase`,
`lowercase`, `letter`, `digit`, `any-char`, `ws`, `blank-line`, `tier` are used but never defined.
Task 5 says "implement exactly this EBNF"; define them or the parser agent will guess (in particular
whether `name` in `epithet-entry`/`tpl-entry`/`subtable-head` is the same as `class-name`).

### B. `features.csv` — segment inventory and spelling (Task 1)

**R6. PHOIBLE's segment spellings systematically disagree with the digests, `attested.csv`, and the
plan's own test assertions.** I read `chat-imports/phoible_inventories_starter.csv` (153 rows, 91
unique phonemes, 38 features, **no cross-inventory feature conflicts** — the plan's step-2 "expected:
no conflicts" is confirmed). But PHOIBLE writes dental/retracted coronals where everything else in
the repo writes plain ones:

| PHOIBLE has | Repo data / plan tests use | Occurrences in the digest |
|---|---|---|
| `s̪ˤ t̪ˤ d̪ˤ z̪ˤ` | `sˤ tˤ dˤ` | `sˤ` 42, `tˤ` 62, `dˤ` 30 vs `s̪ˤ` 2, `t̪ˤ` 2, `d̪ˤ` 2 |
| `t̪ʼ t̪ʰ t̠ʃ t̠ʃʼ d̠ʒ` | `tʼ tʰ tʃ tʃʰ dʒ` | `tʼ` 42, `tʰ` 32, `tʃ` 31, `dʒ` 18 vs one hit each for the barred forms |
| `t̪ d̪ s̪ z̪ n̪ l̪` (Cairene) | `t d s z n l` | — |
| (no `ʋ`, no `tʃʰ`, no `c ɟ ɲ ç e o`) | Dutch `ʋ` (45 hits), Georgian `tʃʰ` (10) | — |

Consequences: Task 1's tests assert `by["tʼ"]` and `by["sˤ"]` exist "from PHOIBLE" (both comments are
false — neither string is in the CSV); Task 24's `test_broad_coronal_becomes_emphatic` asserts
`== "sˤ"`; Task 25 asserts `== "tʃ"`. **Task 1 must state an explicit normalization policy** — my
recommendation: strip PHOIBLE's `◌̪`/`◌̠` on import (they are non-contrastive here), so the committed
table uses the digests' spellings, and record the mapping in `features.README.md`. Also add
hand rows for `ʋ`, `tʃʰ`, and (see R7) the missing vowels. Task 1's step 5a guesses wrong about which
bases are absent: `ɡ ɾ ɣ w x` **are** present; `c ɟ ɲ ç e o` are the ones absent.

**R7. Task 1's Irish segment list is incomplete — Task 3's stated acceptance is unreachable.** Task 3
promises "every IPA string in `sources/irish/test-words.csv` tokenizes without error (144 rows)".
Tokenizing all 144 rows against Task 1's declared 31 consonants + 11 vowels + 6 aliases, **24 rows
fail**. Missing segments, with example rows:

- short `i`, `u` (needed by I-2, which splits /iə uə əi əu/ into two segments): *Ciara* `ˈciəɾˠə`,
  *Nuala* `ˈn̪ˠuəl̪ˠə`, *Tadhg* `t̪ˠəiɡ`, *leabhair* `l̠ʲəuɾʲ` — 13 rows;
- short `o`: *Lasairchos* `ˈl̪ˠɑsˠəɾʲxosˠ` (Task 3's own test punts on this with a live conditional);
- broad `vˠ`: *Niamh* `nʲiəvˠ`, *dubh* `d̪ˠʊvˠ`, *naomh* `n̪ˠiːvˠ`;
- quality-unmarked plain consonants `s l n m r t` (Task 19 `[normalize]` is supposed to assign their
  quality, but the tokenizer runs first and I-24 makes an unknown segment a *hard error*):
  *speal* `sˠpʲal`, *súil* `suːlʲ`, *an-mhaith* `ˈanˈwa`, *tobac* `təˈbak`;
- ASCII `g` (U+0067) for `ɡ`: *glúin* `gl̪ˠuːnʲ`;
- `æ`: *Ard-Easpag* `ˈaːɾˠd̪ˠˈæsˠpˠəɡ`; `õː`: *ardnósach* `ˈaːɾˠd̪ˠˌn̪ˠõːsəx`;
- secondary stress `ˌ`, which `MARKS` (Task 3) does not list, in *drochbhéasach*, *ardnósach*,
  *dualgas*.

Extend the Task 1 list, add the ASCII-`g` and `ˌ` handling to I-1/I-30, and make the Task 3
acceptance test the enforcement point.

**R8. I-2 (no diphthong rows) contradicts Task 1 step 1 (take `Phoneme` verbatim).** PHOIBLE supplies
Welsh `ai au ɔi əi əu ɛu ɪu ʊi`, Dutch `œy ɔu ɛi`, Cairene `æː` as single rows. Task 1 must say
explicitly whether these are dropped, kept as target-only segments, or split — and if kept, whether
the tokenizer's longest-match will wrongly bind Irish `əi` to the Welsh diphthong row.

### C. Regression harness (Task 22) and Mode L

**R9. Mode L will hard-error, not fail, on most rows.** I tokenized every `target_ipa` against a
PHOIBLE-union + Irish segment set: **Georgian 51/122 untokenizable, Cairene 168/279, Welsh 19/19,
Dutch 30/67.** The offenders are mostly data-hygiene, not phonology: ASCII `g` for `ɡ` (Georgian 4,
Cairene 19, Welsh 4), ASCII `:` for `ː` and ASCII `'` for `ʼ` (Dutch), `[ ] / /` wrappers (Welsh, 16
of 19 rows), and `e`/`o` (Cairene 142/65 — the digest's own transcription convention). Under I-24 a
SegmentError is a hard error, so Mode L would crash the suite rather than score. Task 22 must add
(a) a documented input-cleaning pass for `attested.csv` (strip `[]//`, map `g→ɡ`, `:→ː`, `'→ʼ`), and
(b) a `mode="error"` bucket so an untokenizable row is reported, not raised.

**R10. Three of the four stated Mode L denominators are wrong.** Verified: Georgian has `target_ipa`
on **122** of 143 rows (not "all 143"); Cairene on **279** of 312 (the plan's bar is stated over "301
real rows"); Welsh 19/751 ✓; Dutch 67/90 and 32 with both sides ✓; Welsh `layer=modern` = 93 ✓;
`source_ipa` = 0 everywhere except Dutch ✓. Restate the Task 23/24 acceptance bars over the true
denominators, and add the denominators to `test_row_counts_match_the_committed_data`.

### D. Milestone-6 linguistic fidelity

**R11. Georgian /p t k/ (Task 23) cites a digest section that forbids the rule.** `digest.md` §3.1
(lines ~803–812, ~825) says of exactly this rule: *"an earlier draft turned this into 'after a
consonant, ejective; between vowels, aspirate'. **That is not what the source supports**… Do not
encode the 84.1%/26.5% split as a categorical environment rule"*, and its own recommendation
(line ~838) is unconditional ejective. Spec §9 row 4 fixes the default as aspirate-with-ejective-
after-C, which is a design decision and stands — but Task 23 must not cite §3.1 as the *source*.
Retag those lines `%design`, cite `# design: §9.4` plus a `# contra digest §3.1 line 825` note, and
rename the test `test_irish_p_t_k_become_aspirates_by_default` so it does not read as a digest fact.

**R12. Georgian slender coronals → `ʃ ʒ tʃʰ dʒ` has no digest source.** §8.1 (lines 1413–1450) lists
four options and concludes *"None is a sourced Georgian rule… Not decided here"*; §8.2's table offers
`/tʰ tʼ d/` **or** `/tʃʰ tʃʼ dʒ/` for `/tʲ dʲ/`, marked "(unattested for Georgian)". `ʃ ʒ` as outputs
of slender coronals appear nowhere. Task 23 currently cites "§8.1, §8.2" as if transcribing. Retag
`%design` per I-29 with `# design: digest §8.1 open`.

**R13. Two more Georgian citation errors in Task 23.** (a) The Cʷ restriction "before /i e/" is an
engineering addition — §8.1 Option C states Cʲ→C+i / Cˠ→C+v unconditionally, with no vowel
condition; keep the restriction (it is decision 5) but do not cite §8.1 for it. (b) The §5.3
deviation list is wrong: the digest's D1–D5 (lines 1197–1230) are `x`, `tch`, `y`, bare stem, and
*apostrophe placement unchanged* ("**Not an overlay — follow the standard**", the item that forces
*Kas'queil* → *Kasq'ueil*). The plan drops D5 and invents a "`ch`" deviation (`ch` is the
unmodified native digraph). Fix both, and note that Task 23's
`test_the_five_existing_strand4_names_are_reachable_shapes` will fail on *Kas'queil* as spelled.

**R14. Cairene: three rule rows cite sections that say the opposite.** (a) **Degemination** — Task 24
lists it in `[repair]` citing "§2 gemination, §3.9". `digest.md:324–326` states: *"**No degemination
rule is stated for Cairene** in any source consulted"* (Watson's degemination analysis is San'ani
data). Drop the rule, or retag `%design` with no digest citation. There is consequently no in-text
example to test it with. (b) **"No final devoicing"** is documented at §3.7 (line 645), not §3.9.
(c) **Respell dot-under emphatics** — §5 (line 1010) explicitly recommends *plain* letters
("accept the merger. Every practical Egyptian convention writes them plain"); dot-under is
Abdel-Massih's scholarly system at line 988. Spec §9 row 11 fixes dot-under as the project default,
which stands — but the citation must be `# design: §9.11`, not `§5`.

**R15. Cairene: `/sʲ/→ʃ` and `/ə/ → a/i by position` are unsourced.** `sʲ` has zero hits in
`arabic-egy/digest.md`. For /ə/, §8.4 (lines 1534–1536) and §3.8 (715–718) both say Irish /ə/ is
`not covered`, with two undecided options (general preference for /a/ unstressed; vowel-copy
harmony) — "a/i by position" appears nowhere, and the plan cites §8.3, which is about a different
topic. Resolve both under I-29 (pick the digest's majority option, tag `%design`) and fix the
section pointers. Also: §3.6 gives θ→**t or s** by stratum and states ð→z is Arabic-internal, "not
covered" for loans (digest.md:586–587) — Task 24 presents both as settled.

**R16. Cairene stress table is 17 rows, not 16.** `digest.md:868–886` has 17 data rows
(katabt, ʔabe(h), sakakiːn, tˤalabaːt, ʔabadan, muxtalifa, katabitu, jiktibu, ʕamalti, martaba,
beːtak, madrasa, bintina, katab, katabit, katba, maktaba), each as `syllabified-plain | stressed-IPA`
— directly usable as parametrize pairs. Spec §8 says 17; plan Task 14 (line 1855) and Task 24 both
say 16. Fix both.

**R17. Welsh: two wrong section citations in Task 25.** (a) Degemination is cited to §2.7, but §2.7
is *gemination* (`C → Cː / V́ _ V`); the degemination rule `CC → C / [unstressed σ] _` is §2.4 line
499. (b) `sonority = on` is cited to §2.2, where the word "sonority" never occurs (it appears only at
lines 426, 473–476, 496, 711 = §2.1/§2.3/§2.4), and the digest flags its only coda sonority
generalization as *"ASSEMBLED generalisation (unattested inference — stronger than the source)"*
(line 470). Recite and retag `%design`.

**R18. Welsh: `ɣ→g` and `x→χ` are spec-§7-tagged (A) but the digest calls them design choices.**
§8.2 lists four options for /ɣ/ and says option 3 (→ɡ) has *"no Welsh precedent"*; §8.3 calls the
/x/ treatment a "(design inference)" with an unresolved [x]/[χ] CONFLICT. Under the plan's own I-29
and its citation-discipline test (`test_every_rule_line_carries_a_citation`), these must be
`%design` + `# design: digest §8.2 open`, not `%attested`.

**R19. Welsh syllable template — the plan is right and the spec is wrong; say so.** Digest §2.1 line
289 gives `(C)(C)(C)V(V)(C)(C)`, marked **(North)**. Task 25 transcribes it faithfully; spec §7
drops the `(V)`. Add this to the plan's "Known deviations" list (it currently lists only I-25 and
I-26) so the owner sees it, and surface the North-Welsh provenance caveat.

**R20. Dutch: `w→ʋ` and the `herfst` claim are mis-cited.** `w→ʋ` is not in §8.2 or §3.4; it is the
§0 normalization-layer entry at line 32. And *herfst* [hɛr(ə)fst] is a **positive** epenthesis
example (line 457), not a blocking case — only *hals* (homorganic, line 465) and *hart* (coronal C2,
line 467) block. Task 26's `test_epenthesis_is_blocked_before_a_coronal_appendix_obstruent` should
use *hart*, and a separate test should assert *herfst* **does** epenthesize.

**R21. Dutch: onset-list counts and the appendix set.** The digest's lists (lines 179–186) contain
**30** native CC and **27** loan CC, not "~28 / ~24"; CCC is a separate 7-item list (4 native + 3
loan, lines 209–213), not a property of the CC entries. And the digest's appendix is "up to three
*coronal obstruents*" (line 158), which Task 26 narrows to literally `appendix = s t` — flag the
narrowing as `%design` or widen the set.

**R22. Irish: "all 144 `test-words.csv` rows tagged for mutations" (spec §8, plan Task 17) is false.**
The file has 144 data rows; mutation tagging lives in the `features` column as `mut:` and **47 rows**
carry it (`mut:lenition|eclipsis|hproth|tproth|nproth`). The 85 rows carrying `len:` are a *length*
tag, unrelated to mutations. Restate the Task 17 test as "the 47 `mut:`-tagged rows"; the "144-word
set" used elsewhere (property checks, no-UNREPAIRED) is fine as a row count.

**R23. Task 19's alias citation over-attributes.** I-30 correctly separates `lˠ l̠ʲ nˠ n̠ʲ` (genuinely
stated at `irish/digest.md:130–141` as input aliases) from `ɑ ɑː` (only in the user's own
transcriptions, digest.md:27). Task 19's rule line merges both under `# tooling alias, digest §1.1`;
§1.1 is consonants-only. Split the comment.

**R24. `declension` is inferred nowhere.** Task 18's `GEN()` dispatches on `Entry.declension`
(`m1|ach|f2|m3|4`) and `VOC_M1?` gates on it, but Task 20's `infer()` covers only gender, gen_ipa and
dialect (spec §5 says nothing about declension either), and `test-words.csv` has no such column.
Every construction test in Task 18 passes `declension=` by hand, so the gap is invisible until Task
27 runs `--construction all` over the real file, where everything silently defaults to `m1`. Add a
declension inference rule to Task 20 (ending-based, mirroring the gen_ipa heuristics) with its own
`assumptions` tag, or state that `GEN` falls back to `GEN_M1` with a note.

**R25. Spec/plan mismatch on `[inflect]` membership.** Spec §3 names `GEN_M1, GEN_ACH, GEN_F2,
VOC_M1`; Tasks 17/18 add `GEN_M3`, but Task 5's `RuleFile.inflect` docstring still lists the spec's
four. Additive and probably right — make it consistent in one direction.

**R26. Target epithets are never requested by anything.** Spec §4 stage 6 fires "only when the
template requests a target affix", but `[templates]` (Irish-side, I-16) has no syntax for requesting
one, `run_entry()` has no `epithet` parameter (only `adapt()` does), and Task 27's `cmd_run` never
passes one. As written, no epithet rule in any target file is reachable from the CLI, yet Tasks
23/24/26 all specify `[epithets]` blocks and Task 24 tests `NISBA`. Define how a construction selects
a target epithet, and thread it through `run_entry` and the CLI.

### E. Dependencies, ordering, task size

**R27. Missing dependencies (each would block a subagent on a fresh checkout).**
- Tasks **12, 13, 14, 15, 16** all call `syllabify()` in their tests but depend only on 4, 5 (and 7).
  Add Task 10.
- Task **5** creates `tests/helpers.py`, which imports `strands.word.Word` (Task 4). Task 5 depends
  only on Task 3. Add Task 4.
- Task **20**'s `test_gen_ipa_inferred_by_slenderizing_a_broad_final` expects `mˠak → mʲɪc`, which is
  Task 17's `GEN_M1` content. Either add Task 17 as a dependency or state that `infer()` reimplements
  slenderization in Python (and then Tasks 17 and 20 must be kept in sync — say which is canonical).
- Task **27** asserts `{r["strand"] for r in rows} == set(TARGETS)` and runs `explain --strand welsh`;
  both need Tasks 23–26. Declare 23–26 as dependencies of 27, or make the Task 27 tests use the
  `toy-target.rules` fixture.

**R28. Internal contradiction in Task 22's test.** `test_report_rate_is_a_fraction_of_non_skipped_rows`
runs `run_regression("dutch", TABLE)` with the comment "against the toy file until Task 26 lands", but
the declared `run_regression(target, table)` signature loads `rules/<target>.rules` and the
surrounding note says it must raise `FileNotFoundError`. Give `run_regression` an optional
`rule_file` override, or mark the test `skipif(not rules_exist("dutch"))` like the others.

**R29. Two tasks are too large for one agent context; split them.**
- **Task 23 (`georgian.rules`)** — the syllable whitelists alone are a prose-extraction job:
  Appendix 2 (digest lines 324–421) is ~150 two-member sequences plus ~60 three-member, ~21
  four-member, 1 five-member, 2 six-member forms, written as `cluster *example* 'gloss'` prose, not a
  table; Appendix 3 (lines 468–525) adds ~48 CC plus ~25 longer. Split into **23a** (inventory,
  substitute, stress, epithets, respell + their digest-fact tests) and **23b** (the `[syllable]`
  whitelists + `bans` + repair + the Mode L run), with 23b delivering an extraction script committed
  beside the rule file so the transcription is reproducible and reviewable.
- **Task 5 (DSL parser)** — 15 section types, ~30 tests, plus the fixture and `helpers.py`. Split
  into **5a** (file/section skeleton, `[meta] [inventory] [classes] [weights]`, the rewrite-line
  parser, `mini.rules`, helpers) and **5b** (`[syllable] [stress] [epithets] [templates]` and the
  `[mutations]`/`[inflect]` sub-tables).

Task 1 is borderline (91 PHOIBLE rows + ~50 hand rows with a per-row derivation procedure); if R6/R7
are adopted it grows and should also split into "PHOIBLE import + normalization script" and "hand
Irish/diacritic rows".

### F. The repair-testing gap — a concrete design

The plan flags that its repair rules have no derivation-level tests. Cheapest fix that costs no new
machinery: **one parametrized test per target, over a table of `(input_ipa, expected_ipa, digest_line)`
triples taken from the digests' own worked examples, run through `repair()` alone** (not the whole
pipeline), with the input pre-syllabified by the target's own `[syllable]` spec. Put the table in the
target's test module beside the digest-fact tests. The examples exist and are already transcribed:

**Welsh** (`sources/welsh/digest.md`)
| Rule | Case | Digest line |
|---|---|---|
| copy epenthesis | *pobl* → [ˈpɔbɔl] | 682 (also 477, 705) |
| copy epenthesis | *cancr* → [ˈkankar] | 682 |
| liquid deletion | *ffenestr* → [ˈfɛnɛst] | 522, 689 |
| liquid deletion | *posibl* → [ˈpɔsib] | 689 |
| metathesis | *ewythr* → [ˈewɨrθ] | 696 |
| initial l-fortition | *loft* → *lloft* [ɬ-]; *leopard* → *llewpard* | 812 |
| initial r-fortition | *remedy* → *rhymedi* [r̥-] | 812 |
| sC- prothesis | *scarlet* → *ysgarlat*; *steward* → *ystiwart* | 618 |
| degemination | no IPA-transcribed before/after pair exists (only orthographic *cannu*/*canu*, line 508) → `xfail` with that line number, per the plan's own elided-test rule |

**Cairene** (`sources/arabic-egy/digest.md`)
| Rule | Case | Digest line |
|---|---|---|
| anaptyxis `0→i/#C_CV` | *plastic* → *bilastik* | 348 (rule), 356 (form) |
| prothesis `0→ʔi/#_sC` | *ski* → *ʔiskii* | 379, 386 |
| CCC epenthesis after C2 | *banknote* → *bankinut*; *postman* → *bustiman* | 442, 456, 458 |
| epenthetic quality harmony | *group* → *guruub* (u) vs *filaʃ*/*kilaʃ* (i) | 361, 499–503 |
| glottal insertion `0→ʔ/#_V` | *hôtel* → *ʔoteel* | 628, 630 |
| closed-syllable shortening | /kitaab+na/ → *ki.tab.na* | 728 |
| one-long-vowel-per-word | *ʃaalu*+*-u* → *ʃaluu* | 749 |
| degemination | none — see R14(a); drop the rule rather than write a synthetic test |

**Dutch** (`sources/dutch/digest.md`)
| Rule | Case | Digest line |
|---|---|---|
| schwa epenthesis | *melk* → [mɛl(ə)k]; *kalm* → [kɑl(ə)m] | 457, 456 |
| schwa epenthesis (positive) | *herfst* → [hɛr(ə)fst] | 457, 470 |
| blocked, homorganic | *hals* [hɑls] | 465 |
| blocked, coronal C2 | *hart* [hɑrt] | 467 |
| final devoicing | *hand* → [hɑnt] | 363, 561 |
| degemination | *eet, grootte, zette, gevoed, onmiddellijk* | 353–355 |
| tense-V + voiceless fricative | *bách* /bˠɑːx/ | 308 |
| ban, non-trigger (control) | *Matánach* — /x/ follows schwa | §8.6 derivation, 1025–1091 |

**Georgian** (`sources/georgian/digest.md`)
| Rule | Case | Digest line |
|---|---|---|
| degemination | *Twitter* → /tʼvitʼɛri/ | 989 (+ attested.csv row 4) |
| degemination | *puzzle* → /pʼazli/ | 948, 989, 1006 (+ row 16) |
| degemination | *shopping* → /ʃɔpʼinɡi/ | 879, 989 (+ row 18) |
| degemination (native) | /aleɡoria/, /kʼlasi/ | 992 |
| whitelist-miss fallback | none — §3.7 (999–1027) states *"no cluster repair is observed"* | mark the test synthetic and `%fallback`; do not present it as a digest fact |

Cost: four parametrized tests, ~35 rows total, no new engine surface. It also gives the four
target-file agents a hard target other than the Mode L percentage.

---

## Suggestions

- **S1.** State the `Tokenized.stress_index` (a *segment* index, Task 3) vs `Word.stress` (an index
  into `syllables`, Task 4) conversion explicitly in `Word.from_tokenized`. Task 12's
  `test_keep_source_preserves_an_existing_mark` silently assumes it; two different agents write the
  two halves.
- **S2.** Three tests are tautological or self-defeating as written and should be tightened before an
  agent "passes" them: Task 2 `test_loads_all_segments_in_file_order` ends in `or True`;
  Task 2 `test_nearest_breaks_ties_by_candidate_order` asserts `in {("d",),("t",)}` for the second
  case; Task 9 `test_ties_break_by_inventory_order` does the same. Compute the real expected values
  once `features.csv` exists and hard-code them.
- **S3.** Task 1 step 4 estimates "roughly 110 PHOIBLE unique" rows; the true count is **91**. Update
  the eyeball check (`wc -l` ≈ 145, not 155–165).
- **S4.** Welsh onset tiers: the digest has a **fifth** tier, "E — ASSEMBLED/UNVERIFIED (do not encode
  without a check)" (§2.2 line 397), covering generalized stop+liquid onsets, `sm sn`, `θr χr χl`.
  Task 25 says "tiers A/B/C/D exactly as the digest labels them" — add a note that E is excluded
  deliberately, so the agent does not silently fold E-tier clusters into the onset list.
- **S5.** Welsh `[epithets]` is called a "10-suffix table"; §6's table (1298–1316) has 10 rows but only
  8 suffixes (one row is the w→o/y→e adjective ablaut, one is the article). The plan then selects 7,
  silently dropping `-in`. Say so.
- **S6.** Georgian `w→v` is flatter than §3.3, whose (unattested, overlay) recommendation is positional
  — /w/→/u/ word-initially, /v/ elsewhere — and which specifically flags that Irish /w/ arrives
  word-initially from lenited b/m and would land on /u/. Decision 6 fixes flat `→ v`, so this is only
  a citation/comment fix, but the digest's warning is worth carrying into the rule's comment.
- **S7.** Georgian `[epithets]` cites §6.3 wholesale but omits its headline content, the `-shvili` /
  `-dze` patronymics, which the digest calls "the readiest epithet machinery in the language"
  (1301–1326). Given `PATRO_O`/`PATRO_NI` are core constructions, consider adding them.
- **S8.** Georgian "all 32 harmonic clusters are licit onsets" (Task 23's test) contradicts the digest
  for 2 of the 32: `zg`/`žg` are "almost unattested" and `zg` is marked **impossible** in the
  co-occurrence table (~305–309). Also only 24 of the 32 are given as IPA in prose (285–286); the
  other 8 are Latin-only and need the §1.1/§2.0 correspondence charts. Note both in the task.
- **S9.** Cairene §3.8 has exactly 6 items (726–763), but Task 24's prose names only 5 — item 5,
  "vowel lengthening" (final short vowel lengthens under suffix stress-shift, 755–756), is missing.
- **S10.** Cairene §6.2 has exactly 11 nisba examples ✓ and §5's respell table 21 rows (~20 ✓) — both
  claims check out; consider asserting the counts in the tests so a truncated transcription is caught.
- **S11.** Add the Welsh template discrepancy (R19) and the Georgian §3.1 conflict (R11) to the plan's
  "Self-review notes → Known deviations" list. That list is what the owner will read; it currently
  names only I-25 and I-26.
- **S12.** `mini.rules` (Task 5 fixture) uses `sˠ` in `[substitute]` while `[inventory]` is a toy Latin
  set. That is legal (targets may be off-inventory) but will confuse the `check` tests; add a comment.
