# Strands engine — implementation plan (milestones 1–7), draft 2

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development
> (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Draft 2** (2026-08-25) incorporates spec §12 (amendments A–I), all 29 required changes in
`review-opus.md`, and all ten findings in `review-gpt.md`. Where draft 1's interpretation register
contradicted a review, the interpretation has been rewritten, not annotated — read I-1…I-40 as the
current statement.

**Goal:** Build `strands`, a deterministic CLI that adapts Irish (IPA) names and epithets into four
target-language strands (Southern Welsh, Cairene Arabic, Standard Georgian, Belgian Dutch) via
per-language rule files, emitting IPA + English-reader respelling + derivation trace.

**Architecture:** A small standard-library Python package. A feature table (`rules/features.tsv`)
gives every segment PHOIBLE-style features under the digests' segment spellings; a hand-written DSL
parser reads one `.rules` file per language into typed section objects; a rewrite engine applies
ordered rules to an immutable `Word`; a nucleus-aware syllabifier, an unconditional repair loop,
pluggable stress procedures and a respell stage complete the pipeline. All linguistic content lives
in data files (`rules/*.rules`), never in code.

**Tech Stack:** Python ≥3.12, `uv`, `pytest`. No runtime dependencies (standard library only).
Verified on this machine: `uv 0.11.22`. **The system `python3` is 3.10 — do not use it.** Every
command runs through `uv run`, which downloads and pins CPython 3.12.

**Spec:** `phonotactics/docs/specs/2026-08-25-engine-design.md`. **Read §12 first — it overrides
§§1–11 where they conflict.** Background: `phonotactics/notes/project-goals.md`. Linguistic
content: `phonotactics/sources/<lang>/digest.md`. Reviews that shaped this draft:
`docs/plans/review-opus.md`, `docs/plans/review-gpt.md`.

**Milestone 8 (provisional Irish G2P) is out of scope.**

## Global Constraints

- Python ≥3.12; package `strands` under `phonotactics/src/strands/`; `pyproject.toml` at
  `phonotactics/pyproject.toml`; CLI entry point named `strands`.
- No runtime dependencies outside the standard library.
- All paths are relative to `phonotactics/` unless stated otherwise.
- Determinism is a hard requirement: identical input + rule files ⇒ byte-identical output.
- **Test-first, always** (spec §12.I): every task — the four target rule files included — writes
  its tests against an absent or skeletal artefact, runs them, watches them fail, and only then
  writes the artefact. Tests are committed with the code they cover.
- Every rule line in a target `.rules` file carries either a `# [bibkey p.N]` / `# digest §N
  line L` citation or `# design: §9.n` naming the decision-register row.
- Rule tags are exactly one of `%attested`, `%design`, `%fallback`; default `%attested`. A rule
  whose digest section states the opposite, or states nothing, is `%design` — never `%attested`.
- Files are UTF-8, NFC-normalized on read (I-1).

---

## Spec interpretations

The spec (including §12) still leaves the following underdetermined. Each is resolved here by the
simplest reading. Implementers follow these, not their own reading.

- **I-1 Unicode normalization.** All rule files, input TSVs and IPA strings are
  `unicodedata.normalize("NFC", s)` on read. Modifier letters (`ˠ ʲ ʼ ˤ ʰ ː`) and combining marks
  (`◌̪ U+032A`, `◌̠ U+0320`) survive NFC unchanged; NFC only regularizes composed vowels (`õ`).
- **I-2 Diphthongs are two segments but one nucleus** (spec §12.B). `features.tsv` has **no**
  diphthong rows — the 11 PHOIBLE diphthong rows (`ai au ɔi əi əu ɛu ɪu ʊi œy ɔu ɛi`) are dropped
  at import (I-35), because keeping them would make longest-match bind Irish `əi` to the Welsh
  diphthong row. Each `[syllable]` section declares `nuclei = iə uə əi əu` (etc.); the syllabifier
  groups a licensed vowel pair into one nucleus. Georgian declares no `nuclei`, which yields the
  attested hiatus.
- **I-3 Comment vs word-edge `#`.** In a rewrite line *with* an environment, `#` inside the
  environment is the word-edge symbol; the environment runs to end-of-line or to the `%tag`.
  A line with an environment that wants a comment **must** write its `%tag` explicitly. The parser
  raises `ParseError("comment after environment requires an explicit %tag", line)` otherwise.
- **I-4 Bundle syntax.** A match bundle is `[` optional class-name, then `±feature` items `]`
  (≥1 element). On the right, `[...]` is always a feature-change bundle, may not carry a class
  name, and resolves by **exact vector lookup** (spec §12.C): if no `features.tsv` segment has the
  resulting vector, `strands check` reports `UNREACHABLE_CHANGE` and the engine raises at runtime.
  Approximation happens only in the fallback stage (Task 9), never inside a rule.
- **I-5 Targets and replacements.** `TARGET` is a sequence of items (segment / class name / match
  bundle / inline set), any of which may carry a capture suffix `:n`. `REPLACEMENT` contains only
  literal segments, `0`, backreferences `\n`, quoted text (in `[respell]`), or a single
  feature-change bundle — **never** a bare class name (spec §12.C). Lengths may differ.
- **I-6 Simultaneous application.** For one rule: scan the *pre-rule* segment string left to right,
  collecting non-overlapping matches (leftmost, longest at each position); evaluate every context
  against the pre-rule string; apply all replacements at once. One trace entry per rule that
  changed anything, recording the whole word before/after.
- **I-7 Epenthesis.** `TARGET = 0` inserts at every position whose environment matches; such a rule
  must have a non-empty environment on at least one side (`check` code `EPENTHESIS_NO_CONTEXT`).
  One insertion per position.
- **I-8 `.` and `ˈ` are context-only, everywhere including `[respell]`.** They may appear in
  environments and in `[syllable] bans`, never in a target or a replacement. The `. -> ""` /
  `ˈ -> ""` cleanup lines of draft 1 are **deleted**: `respell()` strips marks in code after the
  rules run (spec §12.C). This resolves draft 1's I-8/I-19 contradiction (R4).
- **I-9 `()` and `*`** attach to exactly one context atom, do not nest, and do not combine
  (`(X)*` is a parse error).
- **I-10 Class names** match `[A-Z][A-Z0-9_]*`; no IPA segment matches that pattern.
- **I-11 Predeclared classes** (spec §12.C): `C`, `V`, `LIQ`, `NAS`, `STOP`, `FRIC`, `GLIDE`,
  computed from features at load time over this file's `[inventory]` **plus** the Irish inventory:
  `C` = `syllabic=-` (this deliberately includes `/h/`, which PHOIBLE marks `consonantal=-`
  `sonorant=-`, and the glides); `V` = `syllabic=+`; `LIQ` = `consonantal=+ sonorant=+ coronal=+`
  and (`lateral=+` or `tap=+` or `trill=+`); `NAS` = `nasal=+`; `STOP` = `consonantal=+
  continuant=- sonorant=- delayedRelease=-`; `FRIC` = `continuant=+ sonorant=- consonantal=+`;
  `GLIDE` = `syllabic=- sonorant=+ consonantal=-`. A `[classes]` redeclaration overrides any.
- **I-41 Broad and slender are declared classes, not feature bundles, for the dorsals.** Verified
  in the PHOIBLE CSV: `k ɡ x ɣ ŋ` are `dorsal=+ high=+ front=- back=-`, and they are the *same
  rows* the Welsh/Georgian/Cairene inventories use — so Irish broad `/k/` cannot be given
  `back=+` without corrupting every target's `/k/`. Therefore: segments carrying `ˠ` get
  `back=+ front=-`; the palatals `c ɟ ç ɲ` get `front=+ back=- high=+`; the plain dorsals keep
  PHOIBLE's vector. Every rule file that needs "the broad series" or "the slender series"
  declares them explicitly in `[classes]`, and this exact pair of lines is copied into
  `irish.rules` and each of the four target files:

  ```
  BROAD = pˠ bˠ t̪ˠ d̪ˠ fˠ sˠ w vˠ mˠ n̪ˠ l̪ˠ ɾˠ k ɡ x ɣ ŋ
  SLEN  = pʲ bʲ tʲ dʲ fʲ ʃ vʲ mʲ nʲ lʲ ɾʲ c ɟ ç j ɲ
  ```

  A bundle like `[C +back]` therefore means "velarized consonant" and **excludes** the plain
  dorsals; where a rule needs both, it writes `BROAD`.
- **I-12 Feature distance.** `distance(a,b) = Σ weight[f]` over features where both are defined
  (`+`/`-`) and differ; `0` contributes nothing; weights default to 1.0. Fallback ties break by
  `[inventory]` declaration order (first wins).
- **I-13 Sonority scale** (used only when `sonority = on`), fixed in code and documented in
  `syllabify.py`: vowel 5 > glide 4 > liquid 3 > nasal 2 > fricative 1 > stop/affricate 0. Onsets
  strictly rising, codas strictly falling; `sC` clusters exempt. **Georgian sets `sonority = off`**
  (digest §2.7 says sonority does not govern Georgian clusters), and Welsh's `sonority = on` is
  `%design`, not a digest fact (R17b).
- **I-14 `bans`** are one context sequence per line; a parse whose segment string contains the
  sequence is illegal and the matched span is marked.
- **I-15 Named sub-tables** in `[mutations]`/`[inflect]` start with a bare `NAME:` line and run to
  the next `NAME:` or `[section]`.
- **I-16 `[templates]` grammar.** `NAME = item { item }` where an item is a quoted IPA literal
  (`" "` = word separator), an argument name, a `FUNC(item)` call, **or a bare function name**
  applied to the construction's head (this is what `VOC_M1?` in spec §3 means — R1); a trailing
  `?` makes the item conditional on the head's declension/gender tag. Every join inserts `$`.
- **I-17 `[stress]` parameters** are `key = value` lines after `procedure = X`; the permitted set
  per procedure lives in `src/strands/stress/params.py` (created in Task 6, consumed by Tasks
  12–15) so `check` never has to import a procedure implementation.
- **I-18 `[epithets]`** entries are `NAME = <segment tokens> / <environment>`.
- **I-19 `[respell]`** operates over the annotated token stream (spec §12.C). A quoted replacement
  becomes an **opaque output chunk** that later rules do not rematch; segments not matched by any
  rule pass through as themselves; `.` and `ˈ` are stripped in code afterwards.
- **I-20 `features.tsv` extra columns.** `segment`, `class`, `source` precede the 38 feature
  columns and take no part in distance. Inventories live in rule files; the table is the union.
- **I-21 Trace ids.** `rule_id` = `"<section>:<line>"` in its rule file (e.g. `repair:87`).
- **I-22 Regression "pass"** = exact string equality with the attested IPA after NFC, after the
  cleaning pass of I-36, and after stripping marks the attested row does not itself carry. The
  harness also reports a segment-level edit distance.
- **I-23 Marginal segments** are legal in `[inventory]` and in output; the fallback never picks one.
- **I-24 Unknown segment** is a hard `SegmentError` **in user input and rule files**. Attested-data
  rows are exempt: they go through the I-36 cleaning pass and, if still untokenizable, land in the
  harness's `error` bucket and are counted, never raised (R9).
- **I-25 The attested data cannot support the spec §8 layer-3 regression as written.** Verified
  counts: Georgian 143 rows, **122** with `target_ipa`, 0 with `source_ipa`; Cairene 312 rows (301
  real + 11 `PREDICTED-NOT-ATTESTED:`), **279** with `target_ipa`, 0 with `source_ipa`; Welsh 751
  rows, **19** with `target_ipa`, 0 with `source_ipa`; Dutch 90 rows, **67** with `target_ipa`,
  **32** with both sides. Resolution — two harness modes:
  - **Mode E (end-to-end)**: rows with both IPA sides; run stages 2–7 and compare. Dutch only, 32
    rows.
  - **Mode C (inventory / syllable / stress conformance)** — renamed from draft 1's misleading
    "Mode L" (GPT finding 4): the attested *target* form must be accepted by the rule file: every
    segment in `[inventory]`, syllabifiable with no illegal span and no `bans` violation, and where
    the row records a stress mark the file's stress procedure must reproduce it. **Mode C tests
    only inventory, phonotactics and stress — it says nothing about substitution, repair,
    post-stress, affixation or respell.** Those are covered by the per-target repair tables (I-27).
- **I-26 "Awbery's tree" (spec §7, Welsh) does not exist in the digest.** Welsh §4.3 gives the
  Southern length rule as a 7-line environment list (digest lines 1071–1079), reproduced verbatim
  in Task 25. The Awbery 1984 extract committed on 2026-08-25 is not yet in the digest; spec §11's
  open item stays open.
- **I-27 Per-target repair tables are mandatory** (GPT finding 4, review-opus §F): each target task
  ships one parametrized test over `(input_ipa, expected_ipa, digest_line)` triples drawn from the
  digest's own worked examples, run through `repair()` alone on a word pre-syllabified by that
  target's `[syllable]` spec. The tables are given in full in Tasks 23b, 24, 25, 26.
- **I-28 Where a digest is undecided**, take its own majority/measured option, tag `%design`, and
  cite `# design: digest §N line L open`. No rule is omitted because a source is undecided. Where
  spec §7 or §9 states a default, the spec wins and the citation is `# design: §9.n`.
- **I-29 Where a digest states the opposite of spec §7**, the spec's decision stands but the rule
  is `%design` and carries a `# contra digest §N line L` note (spec §12.G). This applies to:
  Georgian post-consonantal ejective (digest §3.1 line 825 rejects the environment split),
  Georgian slender-coronal series (§8.1 line 1413ff. "not decided here"), Welsh `ɣ→ɡ` (§8.2 "no
  Welsh precedent") and `x→χ` (§8.3 "design inference"), Cairene dot-under respelling (§5 line
  1010 recommends plain letters), Welsh `sonority = on` (§2.4 line 470 flags its own coda
  generalization as assembled/unattested).
- **I-30 Irish input aliases.** `lˠ l̠ʲ nˠ n̠ʲ` are input aliases stated by
  `irish/digest.md` lines 130–141 (`# [wiki-help-ipa-irish notes 5,6]`); `ɑ ɑː` are **not** —
  they occur only in the user's own transcriptions (digest line 27), so their normalize lines are
  cited `# user transcription, digest line 27`, not §1.1 (R23). Both fold in `irish.rules
  [normalize]`; both need `features.tsv` rows so tokenization succeeds first.
- **I-31 "C → C x" in spec §7 means an epenthesis rule** (R2). Georgian's `broad non-labial C →
  C v / _[V +front]` is written `0 -> v / [C +back -labial] _ [V +front]`; Georgian's
  `slender C → C i` is `0 -> i / [C +front] _ [V +back]`; Dutch's `slender C → C j in onsets` is
  `0 -> j / [C +front] _ [V] ` restricted to onset position. Tasks 23a and 26 use these forms.
- **I-32 Feature aliases** (spec §12.C). `features.tsv`'s header block declares
  `ejective = raisedLarynxEjective`, `voice = periodicGlottalSource`, `emphatic =
  retractedTongueRoot`, `aspirated = spreadGlottis`, `ejective`/`voice` usable in any bundle.
  Spec §7's `[STOP −voice]` also uses U+2212 MINUS SIGN; the parser accepts U+2212 and U+002D
  interchangeably in feature specs (R3). "liquid" is **not** a feature — it is the predeclared
  class `LIQ` (I-11), and every plan reference uses `LIQ`.
- **I-33 Metathesis and copy-epenthesis use captures** (spec §12.C, R1). Welsh copy-epenthesis is
  `0 -> \1 / V:1 C _ {l n r} #`; Welsh metathesis is `θ:1 ɾ:2 -> \2 \1 / C V* _ #` written over
  literal segments. No separate metathesis primitive exists.
- **I-34 Canonical segment spellings are the digests'** (spec §12.F, R6): `sˤ tˤ dˤ zˤ tʼ tʰ tʃ
  tʃʼ dʒ`, plain `t d s z n l`, and `ɡ` (U+0261) for the voiced velar stop. PHOIBLE's
  `◌̪`/`◌̠` diacritics are stripped at import via the map in Task 1a. **ASCII `g` (U+0067) is a
  separate canonical row** — it occurs in `test-words.tsv` (*glúin* `gl̪ˠuːnʲ`) and in attested
  data — carrying the same vector as `ɡ`, and `irish.rules [normalize]` folds `g → ɡ`.
- **I-35 PHOIBLE diphthong rows are dropped at import** (R8): `ai au ɔi əi əu ɛu ɪu ʊi œy ɔu ɛi`.
  Their members are declared per language in `[syllable] nuclei`.
- **I-36 Attested-data cleaning pass** (R9). Before tokenizing an `attested.tsv` field the harness
  applies, in order: strip wrapping `[ ]` and `/ /`; map ASCII `:`→`ː`; map ASCII `'`→`ʼ` when it
  follows an obstruent; map ASCII `g`→`ɡ` **only in attested data** (not in `test-words.tsv`,
  where `g` is canonical per I-34 — the two behaviours differ deliberately and each is tested).
  Rows still untokenizable are bucketed `mode="error"` with a count. Draft-1 measurements of the
  damage: Georgian 51/122, Cairene 168/279, Welsh 19/19, Dutch 30/67 untokenizable *before*
  cleaning.
- **I-37 Cairene `e o` are inventory segments.** 142 Cairene attested rows use `e` and 65 use `o`
  (the digest's own transcription convention for /eː oː/ shortened, and for loans). They get hand
  rows in Task 1b and appear in `arabic-egy.rules [inventory]`.
- **I-38 Declension is inferred** (spec §12.H, R24). `Entry.declension` ∈ `{m1, ach, f2, m3, d4}`
  is filled by `infer()` in Task 20 from ending shape + gender, tagged
  `declension:inferred-<rule>`; `GEN()` falls back to `GEN_M1` with an `assumptions` note when
  inference is unavailable.
- **I-39 Target epithets are reachable via construction tags** (spec §12.H, R26). A construction
  name may be `DESC+ADJ` or `DESC+NOUN`; the suffix after `+` names an **abstract slot**, and each
  target's `[epithets]` maps `ADJ` and `NOUN` to its own affix (Arabic `ADJ`=NISBA, `NOUN`=FEM_A;
  Georgian `ADJ`=URI, `NOUN`=NOM_I; Welsh `ADJ`=AIDD, `NOUN` unmapped; Dutch `ADJ`=ACHTIG, `NOUN`
  unmapped). `run_entry()` takes the tag, splits it, and passes the resolved epithet to `adapt()`;
  an unmapped slot means "no affix", not an error. `strands run --construction all` enumerates the
  Irish templates **and** the `DESC+ADJ` / `DESC+NOUN` tags.
- **I-40 Marks.** `MARKS` includes secondary stress `ˌ` (four `test-words.tsv` rows use it:
  *drochbhéasach*, *ardnósach*, *dualgas*, *Ard-Easpag*). Secondary stress is recorded on the
  `Word` and **never** carried into a target — targets assign their own stress. `Word.stress` is an
  index into `syllables`; `Tokenized.stress_index` is a *segment* index, and
  `Word.from_tokenized` converts (S1).

---

## DSL grammar (EBNF)

Task 5a/5b must implement exactly this. All terminals are defined; nothing is left to inference
(R5). `SEGMENT` is a whitespace-delimited token that is a single row of `features.tsv`; `CLUSTER`
is a whitespace-delimited token that tokenizes (longest-match) into one or more segments.

```ebnf
(* ---- lexical terminals ---- *)
ws             = { " " | "\t" } ;
nl             = "\n" ;
digit          = "0".."9" ;
uppercase      = "A".."Z" ;
lowercase      = "a".."z" ;
letter         = uppercase | lowercase ;
any-char       = ? any Unicode scalar except nl ? ;
number         = [ "-" ] , digit , { digit } , [ "." , { digit } ] ;
name           = letter , { letter | digit | "_" | "-" } ;   (* keys, table and epithet names *)
class-name     = uppercase , { uppercase | digit | "_" } ;
feature-name   = lowercase , { letter } ;   (* a PHOIBLE column or an alias (I-32) *)
tier           = uppercase , { uppercase | digit } ;
key            = name ;
value          = { any-char } , ? trimmed ? ;
quoted         = '"' , { any-char - '"' } , '"' ;
sign           = "+" | "-" | "−" | "0" ;    (* U+002D and U+2212 both accepted (I-32) *)
capture        = ":" , ( "1".."9" ) ;
backref        = "\\" , ( "1".."9" ) ;
comment        = "#" , { any-char } ;
blank-line     = ws , nl ;
comment-line   = ws , comment , nl ;

(* ---- file skeleton ---- *)
file           = { line } ;
line           = section-header | entry | comment-line | blank-line ;
section-header = ws , "[" , section-name , "]" , ws , [ comment ] , nl ;
section-name   = "meta" | "inventory" | "classes" | "weights" | "substitute"
               | "syllable" | "repair" | "post-stress" | "stress" | "epithets"
               | "respell" | "templates" | "mutations" | "inflect" | "normalize" ;

(* ---- rewrite sections: substitute, repair, post-stress, respell,
        mutations, inflect, normalize ---- *)
rewrite        = target , "->" , replacement , [ "/" , environment ] ,
                 [ tag ] , [ comment ] ;
target         = "0" | item , { item } ;
item           = ( SEGMENT | class-name | match-bundle | inline-set ) , [ capture ] ;
inline-set     = "{" , ( SEGMENT | class-name ) , { ( SEGMENT | class-name ) } , "}" ;
match-bundle   = "[" , [ class-name ] , { feature-spec } , "]" ;   (* >= 1 element *)
feature-spec   = sign , feature-name ;
replacement    = "0" | change-bundle | out-item , { out-item } ;
out-item       = SEGMENT | backref | quoted ;      (* quoted only inside [respell] *)
change-bundle  = "[" , feature-spec , { feature-spec } , "]" ;
environment    = [ ctx-seq ] , "_" , [ ctx-seq ] ;
ctx-seq        = ctx-item , { ctx-item } ;
ctx-item       = ctx-atom | "(" , ctx-atom , ")" | ctx-atom , "*" ;
ctx-atom       = ( SEGMENT | class-name | match-bundle | inline-set ) , [ capture ]
               | "#" | "$" | "." | "ˈ" ;
tag            = "%attested" | "%design" | "%fallback" ;

(* ---- [meta] ---- *)
meta-entry     = key , "=" , value ;

(* ---- [inventory] ---- *)
inv-entry      = [ "marginal:" ] , SEGMENT , { SEGMENT } ;

(* ---- [classes] ---- *)
class-entry    = class-name , "=" , SEGMENT , { SEGMENT } ;

(* ---- [weights] ---- *)
weight-entry   = feature-name , "=" , number ;

(* ---- [syllable] ---- *)
syl-entry      = "template" , "=" , ( tpl-seq | "any" )
               | "nuclei" , "=" , CLUSTER , { CLUSTER }
               | "onsets" , "=" , ( cluster-list | "any" )
               | "codas"  , "=" , ( cluster-list | "any" )
               | "onsets-tier" , "=" , tiered-list
               | "codas-tier"  , "=" , tiered-list
               | "onset-required" , "=" , ( "yes" | "no" )
               | "appendix" , "=" , SEGMENT , { SEGMENT }
               | "domain" , "=" , ( "word" | "stem" )
               | "sonority" , "=" , ( "on" | "off" )
               | "bans" , "=" , ctx-seq ;                (* repeatable *)
tpl-seq        = tpl-item , { tpl-item } ;
tpl-item       = slot | "(" , slot , ")" ;
slot           = "C" | "V" | "N" | class-name ;          (* N = one nucleus (I-2) *)
cluster-list   = CLUSTER , { CLUSTER } ;
tiered-list    = CLUSTER , ":" , tier , { CLUSTER , ":" , tier } ;

(* ---- [stress] ---- *)
stress-entry   = "procedure" , "=" , proc-name | key , "=" , value ;
proc-name      = "initial" | "penult" | "cairene" | "dutch-weight" | "keep-source" ;

(* ---- [repair] directives (spec §12.E) ---- *)
repair-entry   = rewrite | "cluster-fallback" , "=" , "same-length" ;

(* ---- [epithets] ---- *)
epithet-entry  = name , "=" , SEGMENT , { SEGMENT } , "/" , environment ;

(* ---- [templates] ---- *)
tpl-entry      = name , "=" , t-item , { t-item } ;
t-item         = ( quoted | arg-name | func-call | func-name ) , [ "?" ] ;
                 (* bare func-name = call on the construction head (I-16, R1) *)
arg-name       = "NAME" | "FATHER" | "NOUN" | "ADJ" | "FIRST" | "SECOND" ;
func-call      = func-name , "(" , t-item , ")" ;
func-name      = "LEN" | "ECL" | "HPREF" | "TPREF" | "GEN" | "GEN_M1" | "GEN_ACH"
               | "GEN_F2" | "GEN_M3" | "VOC_M1" | "ART" | "LEN_IF_F" ;

(* ---- [mutations] and [inflect]: named sub-tables ---- *)
subtable-head  = name , ":" ;
```

Characters reserved outside a `SEGMENT`: whitespace, `[ ] ( ) { } / _ # $ % " : = * . ˈ \` , the
digraph `->`, and `+ - − 0` at token start.

---

## File structure

```
phonotactics/
  pyproject.toml                  # Task 0
  .python-version                 # Task 0 ("3.12")
  src/strands/
    __init__.py  cli.py           # Task 0 stub; Task 27 full
    features.py                   # Task 2: FeatureTable, aliases, derived classes, distance
    tokenize.py                   # Task 3: longest-match tokenizer, marks, attested cleaning
    word.py                       # Task 4: Word, TraceEntry
    dsl.py                        # Task 5a core + 5b sections
    check.py                      # Task 6
    stress/
      params.py                   # Task 6 (data only, so check need not import procedures)
      __init__.py                 # Task 12: registry, dispatch, syllable_weight
      initial.py  keep_source.py  # Task 12
      penult.py                   # Task 13
      cairene.py                  # Task 14
      dutch_weight.py             # Task 15
    rewrite.py                    # Task 7: matching, captures, application
    substitute.py                 # Tasks 8-9
    syllabify.py                  # Task 10: nuclei, legality, illegal spans
    repair.py                     # Task 11: unconditional loop, cluster-fallback
    poststress.py                 # Task 16
    irish.py                      # Tasks 17-19
    inputs.py                     # Task 20: Entry, TSV read, inference, lint
    respell.py  pipeline.py       # Task 21
    regress.py                    # Task 22
    gallery.py                    # Task 27
  rules/
    build_features.py             # Task 1a
    features.tsv                  # Task 1a (PHOIBLE half) + Task 1b (hand rows)
    features.README.md            # Tasks 1a/1b: normalization map, per-row derivation
    irish.rules                   # Tasks 17, 19, 18
    georgian.rules                # Tasks 23a, 23b
    arabic-egy.rules              # Task 24
    welsh.rules                   # Task 25
    dutch.rules                   # Task 26
    extract_georgian_clusters.py  # Task 23b
  tests/
    helpers.py                    # Task 5a
    fixtures/  ratchets/  snapshots/
    allow-unrepaired.txt          # Task 28
```

---

## Task list and dependencies

| # | Task | Depends on |
|---|---|---|
| 0 | Project scaffold, `pyproject.toml`, CLI stub | — |
| 1a | PHOIBLE import + normalization script | 0 |
| 1b | Hand rows: Irish, aliases, target gaps | 1a |
| 2 | Feature table loader, aliases, derived classes, distance | 1b |
| 3 | Tokenizer + attested-data cleaning | 2 |
| 4 | `Word` model + trace | 3 |
| 5a | DSL core: skeleton, `[meta] [inventory] [classes] [weights]`, rewrite lines, `helpers.py` | 3, 4 |
| 5b | DSL sections: `[syllable] [stress] [epithets] [templates] [mutations] [inflect]` | 5a |
| 6 | `strands check` + `stress/params.py` | 5b |
| 7 | Rewrite engine (captures, sets, backrefs) | 4, 5a |
| 8 | Substitute stage | 7 |
| 9 | Inventory fallback | 8 |
| 10 | Syllabifier (nucleus-aware) | 4, 5b |
| 11 | Repair loop + `cluster-fallback` | 7, 10 |
| 12 | Stress package: registry, weight, `initial`, `keep-source` | 4, 5b, 6, 10 |
| 13 | `penult` procedure | 12 |
| 14 | `cairene` procedure (17 rows) | 12 |
| 15 | `dutch-weight` procedure | 12 |
| 16 | Post-stress stage | 7, 10, 12 |
| 17 | Irish mutations + inflections | 7 |
| 19 | Irish `[normalize]` | 17 |
| 20 | Input TSV, inference (incl. declension), `lint` | 4, 17 |
| 18 | Irish templates | 19, 20 |
| 21 | Pipeline, respell, epithet slots | 9, 11, 13, 14, 15, 16, 18, 19, 20 |
| 22 | Regression harness (Modes E/C), cleaning, ratchet | 21 |
| 23a | `georgian.rules` core (inventory, substitute, stress, epithets, respell) | 21, 22 |
| 23b | `georgian.rules` syllable whitelists, bans, repair, extraction script | 23a |
| 24 | `arabic-egy.rules` | 21, 22 |
| 25 | `welsh.rules` | 21, 22 |
| 26 | `dutch.rules` | 21, 22 |
| 27 | CLI `run`/`explain`/`gallery`/`lint` | 20, 21, 23a, 23b, 24, 25, 26 |
| 28 | Gallery snapshot + property checks | 27 |

Parallel fans: 13 / 14 / 15 (separate modules, no shared file — spec §12.I); 24 / 25 / 26 / 23a
(23b follows 23a). Tasks 17 → 19 → 20 → 18 are a chain (R27, GPT finding 2).

---

## Task 0: Project scaffold and CLI stub

**Depends on:** —

**Files:** create `pyproject.toml`, `.python-version`, `.gitignore`, `src/strands/__init__.py`,
`src/strands/cli.py`, `tests/test_cli_stub.py`.

**Interfaces:**
- Produces: `strands.__version__: str`; `strands.cli.main(argv: list[str] | None = None) -> int`;
  console script `strands = "strands.cli:main"`.

- [ ] **Step 1: Write the failing test** — `tests/test_cli_stub.py`

```python
import pathlib, subprocess

ROOT = pathlib.Path(__file__).parents[1]

def test_main_reports_version(capsys):
    from strands.cli import main
    assert main(["--version"]) == 0
    assert "strands" in capsys.readouterr().out

def test_main_unknown_command_returns_2():
    from strands.cli import main
    assert main(["frobnicate"]) == 2

def test_console_script_runs():
    out = subprocess.run(["uv", "run", "strands", "--version"],
                         capture_output=True, text=True, cwd=ROOT)
    assert out.returncode == 0

def test_interpreter_is_at_least_3_12():
    import sys
    assert sys.version_info[:2] >= (3, 12)
```

- [ ] **Step 2: Run it and watch it fail** — `cd phonotactics && uv run pytest tests -v`;
  expected `ModuleNotFoundError: No module named 'strands'`.

- [ ] **Step 3: Write `pyproject.toml`**

```toml
[project]
name = "strands"
version = "0.1.0"
description = "Irish-to-target name-adaptation engine"
requires-python = ">=3.12"
dependencies = []

[project.scripts]
strands = "strands.cli:main"

[dependency-groups]
dev = ["pytest>=8"]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/strands"]

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]
```

`.python-version` contains `3.12`. `.gitignore` gets `.venv/`, `__pycache__/`, `*.pyc`,
`.pytest_cache/`.

- [ ] **Step 4: Write the CLI stub** — `src/strands/cli.py`

```python
"""Command-line entry point. Subcommands land in Tasks 6 (check) and 27 (the rest)."""
from __future__ import annotations
import argparse, sys
from . import __version__

COMMANDS = ("run", "explain", "gallery", "lint", "check")

def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if argv and argv[0] == "--version":
        print(f"strands {__version__}")
        return 0
    if not argv or argv[0] not in COMMANDS:
        print(f"usage: strands {{{'|'.join(COMMANDS)}}} ...", file=sys.stderr)
        return 2
    print(f"{argv[0]}: not implemented yet", file=sys.stderr)
    return 1
```

`__init__.py`: `__version__ = "0.1.0"`.

- [ ] **Step 5: Run tests — 4 passed.**
- [ ] **Step 6: Commit**

```bash
git add phonotactics/pyproject.toml phonotactics/.python-version phonotactics/.gitignore \
        phonotactics/src/strands phonotactics/tests
git commit -m "chore(strands): scaffold uv/pytest package and CLI stub"
```

**Acceptance:** `uv run pytest` passes from `phonotactics/`; `uv run strands --version` works; no
non-stdlib runtime dependency.

---

## Task 1a: PHOIBLE import and normalization script

**Depends on:** Task 0

**Files:** create `rules/build_features.py`, `rules/features.tsv` (PHOIBLE half),
`rules/features.README.md`, `tests/test_features_phoible.py`.

**Interfaces:**
- Produces `rules/features.tsv` with header
  `segment<TAB>class<TAB>source<TAB>` + the 38 PHOIBLE feature columns in PHOIBLE order:
  `tone stress syllabic short long consonantal sonorant continuant delayedRelease approximant tap
  trill nasal lateral labial round labiodental coronal anterior distributed strident dorsal high
  low front back tense retractedTongueRoot advancedTongueRoot periodicGlottalSource
  epilaryngealSource spreadGlottis constrictedGlottis fortis lenis raisedLarynxEjective
  loweredLarynxImplosive click`.
- `build_features.py`: `main(csv_path: Path, out_path: Path, *, sort_only: bool = False) -> None`,
  run as `uv run python rules/build_features.py chat-imports/phoible_inventories_starter.csv
  rules/features.tsv`.

**Verified facts this task must reproduce** (measured against the committed CSV; the numbers are
assertions, not estimates — R6, S3):

- The CSV has **153 data rows** and **91 unique `Phoneme` strings**; there are **no** cross-
  inventory feature conflicts among identically-spelled phonemes.
- **Normalization map** — strip `◌̪` (U+032A) and `◌̠` (U+0320), which affects exactly 15 spellings:
  `d̠ʒ→dʒ  d̪→d  d̪ˤ→dˤ  l̪→l  n̪→n  s̪→s  s̪ˤ→sˤ  t̪→t  t̪ˤ→tˤ  z̪→z  z̪ˤ→zˤ  t̠ʃ→tʃ  t̠ʃʼ→tʃʼ
  t̪ʰ→tʰ  t̪ʼ→tʼ`. This makes the table agree with the digests, `attested.tsv`, and every test in
  this plan (I-34).
- Normalization creates **7 collisions** where both spellings existed and their feature vectors
  differ: `d l n s t z tʰ`. **Policy:** keep the row whose original `Phoneme` was already the
  canonical spelling (the non-dental one); if only the dental spelling exists, keep it under the
  canonical name. Every collision and the discarded vector is listed in `features.README.md`.
- After normalization: **84** unique segments. **Drop the 11 diphthong rows** (I-35):
  `ai au ɔi əi əu ɛu ɪu ʊi œy ɔu ɛi`. **73 PHOIBLE rows** remain.
- `class` = `C` for `SegmentClass=consonant`, `V` for `vowel`. `source` = `phoible:<first InvID in
  file order>`. Rows sorted by (`class`, then segment code points) for byte-stable rebuilds.
- The script **fails loudly** on any unexpected conflict rather than choosing silently.

- [ ] **Step 1: Write the failing test** — `tests/test_features_phoible.py`

```python
import csv, pathlib
ROOT = pathlib.Path(__file__).parents[1]
FEATURES = ROOT / "rules" / "features.tsv"
PHOIBLE_38 = ("tone stress syllabic short long consonantal sonorant continuant delayedRelease "
              "approximant tap trill nasal lateral labial round labiodental coronal anterior "
              "distributed strident dorsal high low front back tense retractedTongueRoot "
              "advancedTongueRoot periodicGlottalSource epilaryngealSource spreadGlottis "
              "constrictedGlottis fortis lenis raisedLarynxEjective loweredLarynxImplosive "
              "click").split()

def rows():
    with FEATURES.open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))

def test_header():
    with FEATURES.open(encoding="utf-8") as fh:
        header = fh.readline().rstrip("\n").split("\t")
    assert header[:3] == ["segment", "class", "source"]
    assert header[3:] == PHOIBLE_38

def test_phoible_half_has_73_rows():
    assert len([r for r in rows() if r["source"].startswith("phoible:")]) == 73

def test_dental_and_retracted_diacritics_are_stripped():
    segs = {r["segment"] for r in rows()}
    for canonical, phoible in [("dʒ", "d̠ʒ"), ("sˤ", "s̪ˤ"), ("tʼ", "t̪ʼ"), ("tʃ", "t̠ʃ"),
                               ("tʰ", "t̪ʰ"), ("tˤ", "t̪ˤ"), ("d", "d̪")]:
        assert canonical in segs and phoible not in segs

def test_diphthong_rows_are_dropped():
    segs = {r["segment"] for r in rows()}
    for d in "ai au ɔi əi əu ɛu ɪu ʊi œy ɔu ɛi".split():
        assert d not in segs, d

def test_no_duplicate_segments():
    segs = [r["segment"] for r in rows()]
    assert len(segs) == len(set(segs))

def test_values_are_plus_minus_or_zero():
    for r in rows():
        for f in PHOIBLE_38:
            assert r[f] in {"+", "-", "0"}, (r["segment"], f, r[f])

def test_class_column_agrees_with_syllabic():
    for r in rows():
        assert r["class"] in {"C", "V"}
        assert (r["class"] == "V") == (r["syllabic"] == "+")

def test_known_target_segments_survive_import():
    segs = {r["segment"] for r in rows()}
    for s in "tʼ kʼ pʼ qʼ tʃʼ sˤ tˤ dˤ zˤ ɬ r̥ χ ʁ ʔ ʕ ʒ ħ ð θ pʰ tʰ kʰ".split():
        assert s in segs, s

def test_rebuild_is_byte_stable(tmp_path):
    import subprocess, sys
    out = tmp_path / "f.tsv"
    subprocess.run([sys.executable, str(ROOT / "rules" / "build_features.py"),
                    str(ROOT / "chat-imports" / "phoible_inventories_starter.csv"), str(out)],
                   check=True)
    committed = [l for l in FEATURES.read_text(encoding="utf-8").splitlines()
                 if "\tphoible:" in l or l.startswith("segment\t")]
    assert out.read_text(encoding="utf-8").splitlines() == committed
```

- [ ] **Step 2: Run, watch it fail** (no `features.tsv`).
- [ ] **Step 3: Write `build_features.py` and generate the PHOIBLE half.**
- [ ] **Step 4: Write `features.README.md`** — the normalization map, the 7 collisions with the
  discarded vectors, the dropped diphthongs, and the row count.
- [ ] **Step 5: Run — all pass.**
- [ ] **Step 6: Commit** — `feat(rules): PHOIBLE import with digest-canonical segment spellings`

**Acceptance:** 73 PHOIBLE rows under canonical spellings; rebuild is byte-stable;
`test_rebuild_is_byte_stable` passes with the hand rows of Task 1b absent.

---

## Task 1b: Hand rows — Irish, aliases, target gaps

**Depends on:** Task 1a

**Files:** modify `rules/features.tsv`, `rules/features.README.md`; create
`tests/test_features_hand.py`.

**The exact hand-row list.** Measured by tokenizing all 144 `sources/irish/test-words.tsv` rows:
they use **64 distinct segments**, of which **31 are already in the PHOIBLE half** and **33 are
not**. Draft 1's list was wrong (R7) — this is the corrected, complete set. Add exactly these
**35** rows (33 Irish + 2 target gaps), `source = hand:irish` or `hand:target`:

| Group | Segments | Notes |
|---|---|---|
| Velarized (broad) | `pˠ bˠ t̪ˠ d̪ˠ fˠ sˠ mˠ n̪ˠ l̪ˠ ɾˠ vˠ` | base + `back=+ front=-`; `t̪ˠ d̪ˠ n̪ˠ l̪ˠ` also `anterior=+ distributed=+` |
| Palatalized (slender) | `pʲ bʲ tʲ dʲ fʲ vʲ mʲ nʲ lʲ ɾʲ` | base + `front=+ back=- high=+` |
| Palatals | `c ɟ ç ɲ` | from `k ɡ x ŋ` + `front=+ back=- high=+` |
| Fortis/lenis aliases | `lˠ l̠ʲ nˠ n̠ʲ` | vectors identical to `l̪ˠ lʲ n̪ˠ nʲ` (I-30) |
| Vowels | `o æ õː` | `o` = `ɔ` + `tense=+`; `æ` = `a` + `front=+ low=+`; `õː` = `oː` + `nasal=+` |
| ASCII duplicate | `g` | vector identical to `ɡ` (I-34) |
| Target gaps | `ʋ tʃʰ` | Dutch `ʋ` (digest §1, 45 hits); Georgian `tʃʰ` (digest §1.1, 10 hits) |

Already present from PHOIBLE and **not** to be re-added: `ə a aː iː k x ʃ w ɡ uː eː ɔ oː i h ʊ u
ŋ ɛ ɣ s ɪ j b l m n r t ɑ ɑː`.

**Derivation procedure** (mechanical, so a reviewer can check every row):
1. Start from the PHOIBLE row of the plain base with diacritics removed.
2. Apply, in order: `ʲ` → `front=+ back=- high=+`; `ˠ` → `back=+ front=-`; `◌̪` → `anterior=+
   distributed=+`; `ː` → `long=+ short=-`; `ʼ` → `raisedLarynxEjective=+ constrictedGlottis=+`;
   `ˤ` → `retractedTongueRoot=+ back=+`; `ʰ` → `spreadGlottis=+`.
3. **Do not touch `k ɡ x ɣ ŋ`** — see I-41; the broad/slender contrast on dorsals is carried by
   the `k/c ɡ/ɟ x/ç ŋ/ɲ` pairing, not by a feature on the plain dorsal.
4. `vˠ` is the Connacht medial allophone of `/w/` (digest §1.1) and gets `v` + `back=+`.
5. Alias rows copy their principal's vector exactly.
6. Every hand row's base and applied conventions are listed in `features.README.md`.

- [ ] **Step 1: Write the failing test** — `tests/test_features_hand.py`

```python
import csv, pathlib, unicodedata
ROOT = pathlib.Path(__file__).parents[1]

HAND = ("pˠ bˠ t̪ˠ d̪ˠ fˠ sˠ mˠ n̪ˠ l̪ˠ ɾˠ vˠ pʲ bʲ tʲ dʲ fʲ vʲ mʲ nʲ lʲ ɾʲ "
        "c ɟ ç ɲ lˠ l̠ʲ nˠ n̠ʲ o æ õː g ʋ tʃʰ").split()

def rows():
    with (ROOT / "rules" / "features.tsv").open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))

def test_all_35_hand_rows_present():
    segs = {r["segment"] for r in rows()}
    for s in HAND:
        assert s in segs, s

def test_total_row_count_is_108():
    assert len(rows()) == 108        # 73 PHOIBLE + 35 hand

def test_slender_convention():
    by = {r["segment"]: r for r in rows()}
    for s in "pʲ bʲ tʲ dʲ fʲ vʲ mʲ nʲ lʲ ɾʲ c ɟ ç ɲ".split():
        assert (by[s]["front"], by[s]["back"]) == ("+", "-"), s

def test_broad_convention():
    by = {r["segment"]: r for r in rows()}
    for s in "pˠ bˠ t̪ˠ d̪ˠ fˠ sˠ mˠ n̪ˠ l̪ˠ ɾˠ vˠ".split():
        assert (by[s]["back"], by[s]["front"]) == ("+", "-"), s

def test_dental_broad_coronals_are_anterior_and_distributed():
    by = {r["segment"]: r for r in rows()}
    for s in "t̪ˠ d̪ˠ n̪ˠ l̪ˠ".split():
        assert by[s]["anterior"] == "+" and by[s]["distributed"] == "+", s

def test_plain_dorsals_keep_the_phoible_vector():
    by = {r["segment"]: r for r in rows()}
    for s in "k ɡ x ɣ ŋ".split():
        assert (by[s]["front"], by[s]["back"]) == ("-", "-"), s   # I-41

def test_aliases_match_their_principals():
    by = {r["segment"]: r for r in rows()}
    feats = [k for k in by["k"] if k not in ("segment", "class", "source")]
    for alias, principal in [("lˠ", "l̪ˠ"), ("l̠ʲ", "lʲ"), ("nˠ", "n̪ˠ"), ("n̠ʲ", "nʲ"),
                             ("g", "ɡ")]:
        assert [by[alias][f] for f in feats] == [by[principal][f] for f in feats], alias

def test_every_segment_used_by_test_words_has_a_row():
    """The enforcement point for R7: all 144 rows must be tokenizable."""
    segs = {r["segment"] for r in rows()}
    marks = set("ˈˌ. ")
    mods = set("ˠʲːʰʼˤ")
    used = set()
    with (ROOT / "sources" / "irish" / "test-words.tsv").open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            cur = ""
            for ch in unicodedata.normalize("NFC", row["ipa"] or ""):
                if ch in marks:
                    if cur: used.add(cur); cur = ""
                elif ch in mods or unicodedata.combining(ch):
                    cur += ch
                else:
                    if cur: used.add(cur)
                    cur = ch
            if cur: used.add(cur)
    assert used <= segs, sorted(used - segs)
```

- [ ] **Step 2: Run, fail** (35 missing rows).
- [ ] **Step 3: Append the hand rows** by the procedure above; re-sort with
  `uv run python rules/build_features.py --sort-only rules/features.tsv`.
- [ ] **Step 4: Extend `features.README.md`** with one line per hand row: segment, base row,
  conventions applied.
- [ ] **Step 5: Run — all pass, including `test_every_segment_used_by_test_words_has_a_row`.**
- [ ] **Step 6: Commit** — `feat(rules): hand-derived Irish, alias and target-gap feature rows`

**Acceptance:** 108 rows; every one of the 64 segments used by `test-words.tsv` resolves.

---

## Task 2: Feature table loader — aliases, derived classes, distance

**Depends on:** Task 1b

**Files:** create `src/strands/features.py`, `tests/test_features.py`.

**Interfaces:**

```python
FEATURE_NAMES: tuple[str, ...]                 # the 38, in file order
FEATURE_ALIASES: dict[str, str] = {            # I-32, spec §12.C
    "ejective": "raisedLarynxEjective",
    "voice": "periodicGlottalSource",
    "emphatic": "retractedTongueRoot",
    "aspirated": "spreadGlottis",
}
DERIVED_CLASSES: tuple[str, ...] = ("C", "V", "LIQ", "NAS", "STOP", "FRIC", "GLIDE")

class FeatureTable:
    segments: tuple[str, ...]
    def __contains__(self, segment: str) -> bool: ...
    def value(self, segment: str, feature: str) -> str          # accepts aliases
    def vector(self, segment: str) -> tuple[str, ...]
    def segment_class(self, segment: str) -> str                # "C" | "V"
    def matches(self, segment: str, constraints: dict[str, str]) -> bool
    def apply_changes(self, segment: str, changes: dict[str, str]) -> str
        """EXACT vector lookup (I-4). Raises FeatureError if no segment has it."""
    def distance(self, a: str, b: str, weights: dict[str, float] | None = None) -> float
    def nearest(self, segment: str, candidates: Sequence[str],
                weights: dict[str, float] | None = None) -> str
    def derived_class(self, name: str, over: Sequence[str]) -> tuple[str, ...]
        """Members of a predeclared class (I-11) drawn from `over`, in `over` order."""
    def canonical_feature(self, name: str) -> str               # alias -> column name

def load_features(path: str | Path) -> FeatureTable
class FeatureError(Exception): ...
```

- [ ] **Step 1: Write the failing test** — `tests/test_features.py`

```python
import pathlib, pytest
from strands.features import load_features, FeatureError, FEATURE_NAMES

TABLE = load_features(pathlib.Path(__file__).parents[1] / "rules" / "features.tsv")

def test_table_has_38_features_and_108_segments():
    assert len(FEATURE_NAMES) == 38 and len(TABLE.segments) == 108

def test_segments_are_in_file_order_c_before_v():
    classes = [TABLE.segment_class(s) for s in TABLE.segments]
    assert classes == sorted(classes, key=["C", "V"].index)

def test_value_accepts_an_alias():
    assert TABLE.value("tʼ", "ejective") == TABLE.value("tʼ", "raisedLarynxEjective") == "+"
    assert TABLE.canonical_feature("voice") == "periodicGlottalSource"

def test_distance_is_zero_on_identity_and_symmetric():
    assert TABLE.distance("k", "k") == 0
    assert TABLE.distance("k", "c") == TABLE.distance("c", "k") > 0

def test_distance_ignores_undefined_features():
    manual = sum(1 for f in FEATURE_NAMES
                 if TABLE.value("h", f) in "+-" and TABLE.value("k", f) in "+-"
                 and TABLE.value("h", f) != TABLE.value("k", f))
    assert TABLE.distance("h", "k") == manual

def test_distance_honours_weights():
    assert TABLE.distance("k", "c", weights={"front": 10.0}) > TABLE.distance("k", "c")

def test_nearest_breaks_ties_by_candidate_order():
    """S2: no tautologies — compute the real answer and hard-code it."""
    assert TABLE.nearest("pˠ", ["b", "f"]) == "b"
    assert TABLE.nearest("pˠ", ["f", "b"]) == "b"      # b is strictly nearer, order-independent
    # a genuine tie, resolved by order:
    assert TABLE.nearest("n̪ˠ", ["m", "ŋ"]) == "m"
    assert TABLE.nearest("n̪ˠ", ["ŋ", "m"]) == "ŋ"

def test_apply_changes_is_exact_lookup():
    assert TABLE.apply_changes("k", {"raisedLarynxEjective": "+"}) == "kʼ"
    assert TABLE.apply_changes("k", {"ejective": "+"}) == "kʼ"      # alias

def test_apply_changes_raises_when_no_segment_has_the_vector():
    with pytest.raises(FeatureError):
        TABLE.apply_changes("h", {"lateral": "+", "trill": "+"})

def test_derived_classes():
    inv = list(TABLE.segments)
    assert "h" in TABLE.derived_class("C", inv)          # I-11: C = syllabic-
    assert "j" in TABLE.derived_class("GLIDE", inv)
    assert set("l ɾ r".split()) <= set(TABLE.derived_class("LIQ", inv))
    assert "m" in TABLE.derived_class("NAS", inv) and "m" not in TABLE.derived_class("LIQ", inv)
    assert "k" in TABLE.derived_class("STOP", inv) and "s" in TABLE.derived_class("FRIC", inv)
    assert "a" in TABLE.derived_class("V", inv)

def test_unknown_segment_and_unknown_feature_raise():
    with pytest.raises(FeatureError): TABLE.value("QQ", "front")
    with pytest.raises(FeatureError): TABLE.value("k", "wibble")
```

*(Before committing, run each `nearest` assertion once against the built table and replace the
expectation with the value it actually produces — the pairs above are chosen to be decisive, but
verify rather than assume. A test that asserts a set of possible answers is a failed test — S2.)*

- [ ] **Steps 2–4: fail, implement, pass. Step 5: Commit** —
  `feat(strands): feature table with aliases, derived classes, weighted distance`

---

## Task 3: Tokenizer and attested-data cleaning

**Depends on:** Task 2

**Files:** create `src/strands/tokenize.py`, `tests/test_tokenize.py`.

**Interfaces:**

```python
MARKS: dict[str, str] = {"ˈ": "stress", "ˌ": "secondary", ".": "syllable",
                         "$": "morpheme", " ": "space"}          # I-40

@dataclass(frozen=True)
class Tokenized:
    segments: tuple[str, ...]
    stress_index: int | None          # SEGMENT index of the primary-stressed syllable's start
    secondary: tuple[int, ...]        # segment indices carrying ˌ
    syllable_starts: tuple[int, ...]  # from explicit "." marks; may be empty
    morphemes: frozenset[int]         # positions 0..len carrying "$"
    words: tuple[int, ...]            # segment index each space-separated word starts at

def tokenize(text: str, table: FeatureTable) -> Tokenized
def detokenize(segments: Sequence[str]) -> str
def clean_attested(text: str) -> str
    """I-36: strip wrapping [ ] and / /, ':'->'ː', "'"->'ʼ' after an obstruent,
    ASCII 'g'->'ɡ'. Used ONLY on attested.tsv fields, never on user input."""
class SegmentError(Exception): ...
```

- [ ] **Step 1: Write the failing test**

```python
import pytest, pathlib, csv, unicodedata
from strands.features import load_features
from strands.tokenize import tokenize, detokenize, clean_attested, SegmentError

ROOT = pathlib.Path(__file__).parents[1]
TABLE = load_features(ROOT / "rules" / "features.tsv")

def test_longest_match_prefers_diacritic_segments():
    assert tokenize("t̪ˠaː", TABLE).segments == ("t̪ˠ", "aː")

def test_lasairchos():
    t = tokenize("ˈl̪ˠɑsˠəɾʲxosˠ", TABLE)
    assert t.segments == ("l̪ˠ", "ɑ", "sˠ", "ə", "ɾʲ", "x", "o", "sˠ")
    assert t.stress_index == 0

def test_diphthong_is_two_segments():
    assert tokenize("ˈciəɾˠə", TABLE).segments == ("c", "i", "ə", "ɾˠ", "ə")   # I-2

def test_syllable_dots_recorded_and_removed():
    t = tokenize("ˈkɪə.ɾˠə", TABLE)
    assert "." not in t.segments and t.syllable_starts == (0, 3) and t.stress_index == 0

def test_secondary_stress_is_recorded():
    t = tokenize("ˈaːɾˠd̪ˠˌn̪ˠõːsəx", TABLE)          # ardnósach, test-words row
    assert t.stress_index == 0 and t.secondary == (3,)

def test_ascii_g_tokenizes_as_its_own_segment():
    assert tokenize("gl̪ˠuːnʲ", TABLE).segments[0] == "g"       # I-34, glúin

def test_space_splits_words():
    t = tokenize("mˠaːɾʲə wɑːnˠ", TABLE)
    assert " " not in t.segments and len(t.words) == 2

def test_morpheme_positions():
    assert tokenize("a$vʲ", TABLE).morphemes == frozenset({1})

def test_unknown_segment_raises_with_the_offending_substring():
    with pytest.raises(SegmentError) as e:
        tokenize("kQa", TABLE)
    assert "Q" in str(e.value)

def test_detokenize_round_trips():
    assert detokenize(tokenize("mˠat̪ˠaːnˠəx", TABLE).segments) == "mˠat̪ˠaːnˠəx"

def test_nfc_is_applied():
    s = "aː"
    assert tokenize(s, TABLE).segments == tokenize(unicodedata.normalize("NFD", s), TABLE).segments

def test_clean_attested_strips_wrappers_and_maps_ascii():
    assert clean_attested("[kalb]") == "kalb"
    assert clean_attested("/ka:lb/") == "kaːlb"
    assert clean_attested("t'ma") == "tʼma"
    assert clean_attested("gogo") == "ɡoɡo"

def test_clean_attested_is_not_applied_to_user_input():
    """I-36/I-34: ASCII g is canonical in test-words.tsv and must survive tokenize()."""
    assert tokenize("gl̪ˠuːnʲ", TABLE).segments[0] == "g"

def test_all_144_test_word_rows_tokenize():
    with (ROOT / "sources" / "irish" / "test-words.tsv").open(encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh, delimiter="\t"))
    assert len(rows) == 144
    for r in rows:
        tokenize(r["ipa"], TABLE)          # must not raise
```

- [ ] **Steps 2–4: fail, implement, pass. Step 5: Commit** —
  `feat(strands): longest-match tokenizer with marks and attested-data cleaning`

**Acceptance:** all 144 `test-words.tsv` rows tokenize (this is the R7 enforcement point).

---

## Task 4: `Word` model and trace

**Depends on:** Task 3

**Files:** create `src/strands/word.py`, `tests/test_word.py`.

**Interfaces:**

```python
@dataclass(frozen=True)
class TraceEntry:
    stage: str          # "irish" | "substitute" | "syllabify" | "repair" | "stress" | ...
    rule_id: str        # "<section>:<line>" (I-21) or a stage id like "fallback"
    tag: str            # "attested" | "design" | "fallback" | ""
    before: str
    after: str
    note: str = ""

@dataclass(frozen=True)
class Word:
    segments: tuple[str, ...]
    syllables: tuple[int, ...] = ()        # segment index each syllable starts at
    nuclei: tuple[tuple[int, int], ...] = ()   # (start, stop) segment spans, one per nucleus
    stress: int | None = None              # index into `syllables`
    morphemes: frozenset[int] = frozenset()
    illegal: frozenset[int] = frozenset()
    flags: tuple[str, ...] = ()
    trace: tuple[TraceEntry, ...] = ()

    @classmethod
    def from_tokenized(cls, tok: Tokenized) -> "Word"
        """Converts tok.stress_index (a SEGMENT index) to a syllable index once
        syllables are known; before syllabification `stress` holds the segment index
        in `_pending_stress` and is resolved by syllabify(). (S1)"""
    def ipa(self, *, marks: bool = True) -> str
    def replaced(self, start: int, stop: int, new: Sequence[str]) -> "Word"
    def traced(self, entry: TraceEntry) -> "Word"
    def with_flag(self, flag: str) -> "Word"
    def fallback_count(self) -> int
```

**S1 note for the implementer:** `Tokenized.stress_index` is a segment index; `Word.stress` is an
index into `syllables`. `Word.from_tokenized` stores the segment index in a private field, and
`syllabify()` (Task 10) converts it — the two halves are written by different agents, so the field
name and the conversion point are fixed here: private attribute `_pending_stress: int | None`,
converted in `syllabify()` before it returns.

- [ ] **Step 1: Write the failing test**

```python
from strands.word import Word, TraceEntry

def w(*segs, **kw): return Word(segments=tuple(segs), **kw)

def test_ipa_with_marks():
    x = w("k", "ɪ", "ə", "ɾˠ", "ə", syllables=(0, 3), stress=0)
    assert x.ipa() == "ˈkɪə.ɾˠə" and x.ipa(marks=False) == "kɪəɾˠə"

def test_replaced_shifts_later_annotations():
    x = w("s", "k", "a", "l", syllables=(0,), morphemes=frozenset({4}), illegal=frozenset({0, 1}))
    y = x.replaced(0, 1, ("i", "s"))
    assert y.segments == ("i", "s", "k", "a", "l") and y.morphemes == frozenset({5})

def test_replaced_drops_marks_inside_the_span():
    assert w("a", "b", "c", illegal=frozenset({1})).replaced(1, 2, ("d",)).illegal == frozenset()

def test_traced_appends_and_is_immutable():
    x = w("a"); y = x.traced(TraceEntry("substitute", "substitute:3", "attested", "a", "b"))
    assert x.trace == () and len(y.trace) == 1

def test_fallback_count():
    x = (w("a").traced(TraceEntry("substitute", "fallback", "fallback", "q", "k"))
              .traced(TraceEntry("substitute", "substitute:1", "attested", "p", "b")))
    assert x.fallback_count() == 1

def test_with_flag_is_idempotent():
    assert w("a").with_flag("UNREPAIRED").with_flag("UNREPAIRED").flags == ("UNREPAIRED",)

def test_word_is_hashable_and_frozen():
    hash(w("a"))
```

- [ ] **Steps 2–4. Step 5: Commit** — `feat(strands): immutable Word model with derivation trace`

---

## Task 5a: DSL core — skeleton, simple sections, rewrite lines

**Depends on:** Tasks 3, 4

**Files:** create `src/strands/dsl.py`, `tests/helpers.py`, `tests/fixtures/mini.rules`,
`tests/test_dsl_core.py`.

**Scope:** the file/section skeleton, `[meta] [inventory] [classes] [weights]`, and the rewrite-line
parser (including captures, backreferences and inline sets). `[syllable] [stress] [epithets]
[templates] [mutations] [inflect]` are Task 5b and may raise `NotImplementedError` here.

**Interfaces:**

```python
@dataclass(frozen=True)
class Bundle:
    class_name: str | None
    constraints: dict[str, str]        # canonical feature names (aliases resolved at parse)

@dataclass(frozen=True)
class ItemSpec:
    kind: str                          # "segment" | "class" | "bundle" | "set"
    value: str | Bundle | tuple[str, ...]
    capture: int | None = None         # from ":n" (I-33)

@dataclass(frozen=True)
class CtxItem:
    atom: ItemSpec | str               # str is one of "#", "$", ".", "ˈ"
    optional: bool = False
    star: bool = False

@dataclass(frozen=True)
class Rule:
    section: str
    line: int
    rule_id: str                       # f"{section}:{line}"
    target: tuple[ItemSpec, ...]       # () = epenthesis
    replacement: tuple[object, ...] | Bundle
        # elements are str (segment), Backref(n), or QuotedText(s); Bundle = feature change;
        # () = deletion
    left: tuple[CtxItem, ...]
    right: tuple[CtxItem, ...]
    tag: str
    comment: str

@dataclass(frozen=True)
class Backref: n: int
@dataclass(frozen=True)
class QuotedText: text: str

@dataclass(frozen=True)
class RuleFile:
    path: str
    meta: dict[str, str]
    inventory: tuple[str, ...]
    marginal: frozenset[str]
    classes: dict[str, tuple[str, ...]]     # user + derived (I-11)
    weights: dict[str, float]
    sections: dict[str, tuple[Rule, ...]]
    syllable: "SyllableSpec | None" = None  # Task 5b
    stress: "StressSpec | None" = None      # Task 5b
    epithets: dict[str, "Epithet"] = field(default_factory=dict)     # Task 5b
    templates: dict[str, tuple["TemplateItem", ...]] = field(default_factory=dict)
    mutations: dict[str, tuple[Rule, ...]] = field(default_factory=dict)
    inflect: dict[str, tuple[Rule, ...]] = field(default_factory=dict)

def parse_rules(text: str, table: FeatureTable, path: str = "<string>") -> RuleFile
def parse_rules_file(path: str | Path, table: FeatureTable) -> RuleFile
class ParseError(Exception):
    line: int          # str(e) == f"{path}:{line}: {message}"
```

- [ ] **Step 1: Write `tests/helpers.py`**

```python
import csv, pathlib
from strands.features import load_features
from strands.dsl import parse_rules_file
from strands.tokenize import tokenize
from strands.word import Word

ROOT = pathlib.Path(__file__).parents[1]
FIXTURES = pathlib.Path(__file__).parent / "fixtures"
TABLE = load_features(ROOT / "rules" / "features.tsv")

def w(ipa: str) -> Word:
    return Word.from_tokenized(tokenize(ipa, TABLE))

def irish():
    return parse_rules_file(ROOT / "rules" / "irish.rules", TABLE)

def target(name: str):
    return parse_rules_file(ROOT / "rules" / f"{name}.rules", TABLE)

def rules_exist(name: str) -> bool:
    return (ROOT / "rules" / f"{name}.rules").exists()

def read_test_words() -> list[dict[str, str]]:
    with (ROOT / "sources" / "irish" / "test-words.tsv").open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))

def mutation_rows() -> list[dict[str, str]]:
    """R22: the 47 rows tagged mut: in the `features` column — NOT the 85 len: rows,
    which are a vowel-length tag."""
    return [r for r in read_test_words() if "mut:" in (r.get("features") or "")]

def entry_of(row: dict[str, str]):
    """A test-words row -> an inferred Entry. Available from Task 20 on."""
    from strands.inputs import Entry, infer
    return infer(Entry(orthography=row["orthography"], ipa=row["ipa"],
                       dialect=row.get("dialect") or "C", gloss=row.get("gloss") or ""),
                 irish(), TABLE)

FIX = FIXTURES / "input-sample.tsv"      # written in Task 20

def read_allow_file_for(name: str) -> set[str]:
    return {ortho for tgt, ortho in read_allow_file() if tgt == name}

def read_allow_file() -> set[tuple[str, str]]:
    path = ROOT / "tests" / "allow-unrepaired.txt"
    if not path.exists():
        return set()
    out = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip() and not line.startswith("#"):
            tgt, ortho, *_ = line.split("\t")
            out.add((tgt, ortho))
    return out
```

- [ ] **Step 2: Write the fixture** — `tests/fixtures/mini.rules`

```
# A tiny file exercising the Task 5a constructs.
# NOTE (S12): [substitute] deliberately mentions sˠ, which is NOT in this toy [inventory].
# Off-inventory targets are legal (an Irish segment arrives before the target replaces it);
# `strands check` reports it as the warning-level code OFF_INVENTORY, not an error.
[meta]
name = Mini
digest = sources/none

[inventory]
p b t d k ɡ s ʃ m n l r a i u aː
marginal: ʒ

[classes]
BIG = p b t d k ɡ

[weights]
front = 2.0

[substitute]
p -> b                                  # attested by default
[C +back] -> [-back]                    %design
sˠ ʃ -> s ʃ / #_ V                      %attested # both segments replaced
0 -> i / # s _ [BIG]                    %attested # prothesis
t -> 0 / _ #                            %fallback
0 -> \1 / a:1 t _ {l n r} #             %design   # copy epenthesis via capture (I-33)
t:1 r:2 -> \2 \1 / k _ #                %design   # metathesis via captures
```

- [ ] **Step 3: Write the failing tests** — `tests/test_dsl_core.py`

```python
import pytest
from helpers import TABLE, FIXTURES
from strands.dsl import (parse_rules, parse_rules_file, ParseError, Bundle, Backref,
                         QuotedText, ItemSpec)

MINI = parse_rules_file(FIXTURES / "mini.rules", TABLE)

def test_meta_and_inventory():
    assert MINI.meta["name"] == "Mini"
    assert MINI.inventory[0] == "p" and "ʒ" in MINI.marginal and "ʒ" in MINI.inventory

def test_derived_classes_are_predeclared():
    for name in ("C", "V", "LIQ", "NAS", "STOP", "FRIC", "GLIDE"):
        assert name in MINI.classes
    assert "l" in MINI.classes["LIQ"] and "m" in MINI.classes["NAS"]
    assert "t̪ˠ" in MINI.classes["C"]        # I-11: Irish segments join C and V

def test_user_class_and_weights():
    assert MINI.classes["BIG"] == ("p", "b", "t", "d", "k", "ɡ")
    assert MINI.weights["front"] == 2.0

def test_simple_rewrite_defaults_to_attested():
    r = MINI.sections["substitute"][0]
    assert r.target[0].value == "p" and r.replacement == ("b",) and r.tag == "attested"
    assert r.rule_id == f"substitute:{r.line}"

def test_match_bundle_and_change_bundle():
    r = MINI.sections["substitute"][1]
    assert r.target[0].value == Bundle("C", {"back": "+"})
    assert isinstance(r.replacement, Bundle) and r.replacement.class_name is None
    assert r.tag == "design"

def test_feature_alias_and_unicode_minus_are_accepted():
    rf = parse_rules("[inventory]\nk kʼ\n[substitute]\nk -> [+ejective]\n"
                     "kʼ -> k / [STOP −voice] _\n", TABLE)
    assert rf.sections["substitute"][0].replacement.constraints == {"raisedLarynxEjective": "+"}
    assert rf.sections["substitute"][1].left[0].atom.value.constraints == \
        {"periodicGlottalSource": "-"}

def test_multi_segment_target_and_environment():
    r = MINI.sections["substitute"][2]
    assert tuple(i.value for i in r.target) == ("sˠ", "ʃ")
    assert [c.atom for c in r.left] == ["#"]
    assert r.right[0].atom.value == "V"
    assert r.comment.strip() == "both segments replaced"

def test_epenthesis_rule_has_empty_target():
    r = MINI.sections["substitute"][3]
    assert r.target == () and [c.atom for c in r.left][0] == "#"

def test_deletion_rule():
    assert MINI.sections["substitute"][4].replacement == ()

def test_capture_and_backreference():
    r = MINI.sections["substitute"][5]
    assert r.left[0].atom.capture == 1
    assert r.replacement == (Backref(1),)

def test_inline_set():
    r = MINI.sections["substitute"][5]
    s = r.right[0].atom
    assert s.kind == "set" and s.value == ("l", "n", "r")

def test_metathesis_via_captures():
    r = MINI.sections["substitute"][6]
    assert [i.capture for i in r.target] == [1, 2]
    assert r.replacement == (Backref(2), Backref(1))

def test_optional_and_star():
    rf = parse_rules("[inventory]\np a\n[substitute]\np -> a / (a)_ a*\n", TABLE)
    r = rf.sections["substitute"][0]
    assert r.left[0].optional and r.right[0].star

def test_star_on_optional_is_a_parse_error():
    with pytest.raises(ParseError):
        parse_rules("[inventory]\np a\n[substitute]\np -> a / (a)*_\n", TABLE)

def test_class_name_in_a_replacement_is_a_parse_error():
    """I-5 / spec §12.C: replacements carry no bare class names."""
    with pytest.raises(ParseError):
        parse_rules("[inventory]\np a\n[classes]\nX = p\n[substitute]\na -> X\n", TABLE)

def test_syllable_and_stress_marks_are_rejected_in_targets():
    with pytest.raises(ParseError):
        parse_rules("[inventory]\np a\n[substitute]\n. -> p\n", TABLE)     # I-8

def test_unknown_section_and_unknown_segment_and_missing_arrow_raise_with_line_numbers():
    for src, ln in [("[frobnicate]\n", 1),
                    ("[inventory]\np\n[substitute]\nQ -> p\n", 4),
                    ("[inventory]\np a\n[substitute]\np a\n", 4)]:
        with pytest.raises(ParseError) as e:
            parse_rules(src, TABLE)
        assert f":{ln}:" in str(e.value)

def test_comment_after_environment_without_tag_is_an_error():
    with pytest.raises(ParseError) as e:
        parse_rules("[inventory]\np a\n[substitute]\np -> a / _ a # note\n", TABLE)
    assert "explicit %tag" in str(e.value)

def test_word_edge_hash_in_environment_is_not_a_comment():
    rf = parse_rules("[inventory]\np a\n[substitute]\np -> a / _ #\n", TABLE)
    assert [c.atom for c in rf.sections["substitute"][0].right] == ["#"]

def test_parsing_is_deterministic():
    assert parse_rules_file(FIXTURES / "mini.rules", TABLE) == \
           parse_rules_file(FIXTURES / "mini.rules", TABLE)
```

- [ ] **Steps 4–6: run, fail, implement, pass.**
- [ ] **Step 7: Commit** — `feat(strands): DSL core parser with captures, sets and backreferences`

---

## Task 5b: DSL sections — syllable, stress, epithets, templates, mutations, inflect

**Depends on:** Task 5a

**Files:** modify `src/strands/dsl.py`; extend `tests/fixtures/mini.rules`; create
`tests/test_dsl_sections.py`.

**Interfaces:**

```python
@dataclass(frozen=True)
class SyllableSpec:
    template: tuple[tuple[str, bool], ...] | None   # (slot, optional); None = "any"
    nuclei: tuple[tuple[str, ...], ...]             # licensed vowel sequences (I-2)
    onsets: frozenset[tuple[str, ...]] | None       # COMPLETE set incl. singletons (spec §12.D)
    codas: frozenset[tuple[str, ...]] | None
    onset_tiers: dict[tuple[str, ...], str]
    coda_tiers: dict[tuple[str, ...], str]
    onset_required: bool                            # default False (spec §12.D)
    appendix: tuple[str, ...]
    domain: str                                     # "word" | "stem"
    sonority: bool
    bans: tuple[tuple[CtxItem, ...], ...]

@dataclass(frozen=True)
class StressSpec:
    procedure: str
    params: dict[str, str]

@dataclass(frozen=True)
class Epithet:
    name: str
    form: tuple[str, ...]
    left: tuple[CtxItem, ...]
    right: tuple[CtxItem, ...]

@dataclass(frozen=True)
class TemplateItem:
    kind: str            # "literal" | "arg" | "call"
    value: str
    child: "TemplateItem | None" = None
    conditional: bool = False

# RuleFile gains, in [repair]: cluster_fallback: str | None  ("same-length" | None)
```

- [ ] **Step 1: Extend the fixture** — append to `tests/fixtures/mini.rules`

```
[syllable]
template = (C)(C)N(C)(C)
nuclei   = ai au
onsets   = p b t d k ɡ s ʃ m n l r pl pr bl br st sp
codas    = p t k s st ts lp
onsets-tier = pl:A pr:A st:B
onset-required = no
appendix = s t
domain   = word
sonority = on
bans = [V +long] C C [-coronal]

[stress]
procedure = penult

[epithets]
NISBA = i / $_ #

[respell]
ʃ -> "sh"
aː -> "aa" / _ C                        %design

[post-stress]
a -> aː / ˈ_ #                          %design

[repair]
0 -> i / LIQ _ [C -coronal]             %attested
cluster-fallback = same-length

[templates]
VOC = "a" LEN(NAME) VOC_M1?

[mutations]
LEN:
p -> b / #_
ECL:
t -> d / #_

[inflect]
VOC_M1:
p -> b / _ #
```

- [ ] **Step 2: Write the failing tests** — `tests/test_dsl_sections.py`

```python
import pytest
from helpers import TABLE, FIXTURES
from strands.dsl import parse_rules, parse_rules_file, ParseError

MINI = parse_rules_file(FIXTURES / "mini.rules", TABLE)

def test_template_uses_the_nucleus_slot():
    assert MINI.syllable.template == (("C", True), ("C", True), ("N", False),
                                      ("C", True), ("C", True))

def test_nuclei_are_parsed_as_segment_sequences():
    assert ("a", "i") in MINI.syllable.nuclei and ("a", "u") in MINI.syllable.nuclei

def test_onsets_are_a_complete_set_including_singletons():
    s = MINI.syllable
    assert ("p",) in s.onsets and ("p", "l") in s.onsets       # spec §12.D
    assert s.onset_required is False

def test_codas_and_appendix_and_domain_and_sonority():
    s = MINI.syllable
    assert ("s", "t") in s.codas and s.appendix == ("s", "t")
    assert s.domain == "word" and s.sonority is True

def test_tiers_are_recorded():
    assert MINI.syllable.onset_tiers[("p", "l")] == "A"

def test_bans_are_context_sequences():
    assert len(MINI.syllable.bans) == 1 and len(MINI.syllable.bans[0]) == 4

def test_stress_section():
    assert MINI.stress.procedure == "penult" and MINI.stress.params == {}

def test_epithets():
    e = MINI.epithets["NISBA"]
    assert e.form == ("i",) and [c.atom for c in e.left] == ["$"]

def test_respell_quoted_replacement():
    from strands.dsl import QuotedText
    assert MINI.sections["respell"][0].replacement == (QuotedText("sh"),)

def test_respell_may_not_contain_mark_cleanup_rules():
    """I-8/§12.C: marks are stripped in code; `. -> ""` is a parse error."""
    with pytest.raises(ParseError):
        parse_rules('[inventory]\np\n[respell]\n. -> ""\n', TABLE)

def test_cluster_fallback_directive():
    assert MINI.cluster_fallback == "same-length"

def test_templates_bare_function_item():
    items = MINI.templates["VOC"]
    assert items[0].kind == "literal" and items[0].value == "a"
    assert items[1].kind == "call" and items[1].value == "LEN" and items[1].child.value == "NAME"
    assert items[2].kind == "call" and items[2].value == "VOC_M1" and items[2].child is None
    assert items[2].conditional is True          # R1: bare func-name + "?"

def test_mutations_and_inflect_subtables():
    assert set(MINI.mutations) == {"LEN", "ECL"} and set(MINI.inflect) == {"VOC_M1"}
    assert MINI.mutations["LEN"][0].target[0].value == "p"

def test_unknown_syllable_key_raises():
    with pytest.raises(ParseError):
        parse_rules("[inventory]\np a\n[syllable]\nwibble = 3\n", TABLE)

def test_unknown_stress_procedure_raises():
    with pytest.raises(ParseError):
        parse_rules("[inventory]\np\n[stress]\nprocedure = wibble\n", TABLE)
```

- [ ] **Steps 3–5: fail, implement, pass. Step 6: Commit** —
  `feat(strands): DSL section parsers for syllable, stress, epithets, templates, mutations`

---

## Task 6: `strands check` and the stress-parameter registry

**Depends on:** Task 5b

**Files:** create `src/strands/check.py`, `src/strands/stress/__init__.py` (empty package marker),
`src/strands/stress/params.py`; modify `src/strands/cli.py`; create `tests/test_check.py`.

**Why `params.py` lives here** (GPT finding 2): `check` must validate `[stress]` parameters without
importing any procedure implementation, and Tasks 12–15 must not have to edit `check.py`. So this
task creates the data table and Tasks 12–15 consume it:

```python
# src/strands/stress/params.py — data only, no imports from the rest of the package.
PROCEDURE_PARAMS: dict[str, frozenset[str]] = {
    "initial":      frozenset({"mark"}),        # mark = on|off (Georgian sets off)
    "penult":       frozenset(),                # R: penult takes no parameters
    "cairene":      frozenset(),
    "dutch-weight": frozenset({"window"}),      # window = 3 (default)
    "keep-source":  frozenset(),
}
```

Note this corrects draft 1's `mini.rules`, which gave `penult` a `window = 3` parameter — an
inconsistency the GPT review caught. The Task 5b fixture above has no stress params.

**Interfaces:**

```python
@dataclass(frozen=True)
class CheckError:
    line: int
    code: str        # UNKNOWN_CLASS | UNKNOWN_FEATURE | OFF_INVENTORY | EPENTHESIS_NO_CONTEXT
                     # | UNKNOWN_STRESS_PARAM | UNREACHABLE_CHANGE | CLUSTER_OFF_INVENTORY
                     # | BAD_TEMPLATE_ARG | UNDEFINED_BACKREF | NUCLEUS_OFF_INVENTORY
    message: str
    severity: str    # "error" | "warning"

def check_rule_file(rf: RuleFile, table: FeatureTable) -> list[CheckError]
```

Checks, all of them:
1. every class name used anywhere is declared or predeclared;
2. every feature name (after alias resolution) is one of the 38;
3. every segment in a replacement is in `[inventory]` → `OFF_INVENTORY`, **severity `warning`**
   (`irish.rules` legitimately emits Irish segments; the CLI exits 0 on warnings alone);
4. epenthesis with both contexts empty;
5. `[stress] procedure` known and its params ⊆ `PROCEDURE_PARAMS[procedure]`;
6. every change-bundle resolves by exact lookup for at least one inventory segment
   (`UNREACHABLE_CHANGE`, spec §12.C);
7. every `[syllable]` onset/coda/appendix/nuclei segment is in `[inventory]`;
8. every `[templates]` arg and function name is from the fixed sets (I-16);
9. every `\n` backreference has a matching `:n` capture in the same rule (`UNDEFINED_BACKREF`).

- [ ] **Step 1: Write the failing test** — `tests/test_check.py`

```python
import pytest
from helpers import TABLE
from strands.dsl import parse_rules
from strands.check import check_rule_file

def codes(src):
    return sorted(e.code for e in check_rule_file(parse_rules(src, TABLE), TABLE))

def test_clean_file_has_no_findings():
    assert codes("[inventory]\np b\n[substitute]\np -> b\n") == []

def test_undeclared_class_reported_with_its_line():
    errs = check_rule_file(parse_rules("[inventory]\np b\n[substitute]\np -> b / _ NOSUCH\n",
                                       TABLE), TABLE)
    assert errs[0].code == "UNKNOWN_CLASS" and errs[0].line == 4

def test_unknown_feature():
    assert "UNKNOWN_FEATURE" in codes("[inventory]\np b\n[substitute]\n[C +wibble] -> b\n")

def test_alias_is_not_an_unknown_feature():
    assert "UNKNOWN_FEATURE" not in codes("[inventory]\nk kʼ\n[substitute]\nk -> [+ejective]\n")

def test_off_inventory_replacement_is_a_warning_not_an_error():
    errs = check_rule_file(parse_rules("[inventory]\np\n[substitute]\np -> b\n", TABLE), TABLE)
    assert [e.code for e in errs] == ["OFF_INVENTORY"] and errs[0].severity == "warning"

def test_epenthesis_without_context():
    assert "EPENTHESIS_NO_CONTEXT" in codes("[inventory]\np a\n[substitute]\n0 -> a\n")

def test_unknown_stress_parameter():
    assert "UNKNOWN_STRESS_PARAM" in codes(
        "[inventory]\np\n[stress]\nprocedure = penult\nwindow = 3\n")

def test_known_stress_parameter_passes():
    assert codes("[inventory]\np\n[stress]\nprocedure = dutch-weight\nwindow = 3\n") == []

def test_unreachable_feature_change():
    assert "UNREACHABLE_CHANGE" in codes("[inventory]\np\n[substitute]\np -> [+click]\n")

def test_cluster_off_inventory():
    assert "CLUSTER_OFF_INVENTORY" in codes("[inventory]\np a\n[syllable]\nonsets = pl\n")

def test_undefined_backreference():
    assert "UNDEFINED_BACKREF" in codes("[inventory]\np a\n[substitute]\n0 -> \\1 / a _ p\n")

def test_defined_backreference_is_clean():
    assert codes("[inventory]\np a\n[substitute]\n0 -> \\1 / a:1 _ p\n") == []

def test_cli_check_exit_codes(tmp_path, capsys):
    from strands.cli import main
    bad = tmp_path / "x.rules"; bad.write_text("[inventory]\np a\n[substitute]\n0 -> a\n",
                                               encoding="utf-8")
    assert main(["check", str(bad)]) == 1
    assert "EPENTHESIS_NO_CONTEXT" in capsys.readouterr().err
    warn = tmp_path / "w.rules"; warn.write_text("[inventory]\np\n[substitute]\np -> b\n",
                                                 encoding="utf-8")
    assert main(["check", str(warn)]) == 0        # warnings alone do not fail
    ok = tmp_path / "y.rules"; ok.write_text("[inventory]\np b\n[substitute]\np -> b\n",
                                             encoding="utf-8")
    assert main(["check", str(ok)]) == 0
```

- [ ] **Steps 2–4. Step 5: Commit** —
  `feat(strands): static rule-file checks, stress-parameter registry, 'strands check'`

**Acceptance:** `uv run strands check tests/fixtures/mini.rules` exits 0. Milestone 1 complete.

---

## Task 7: Rewrite engine

**Depends on:** Tasks 4, 5a

**Files:** create `src/strands/rewrite.py`, `tests/test_rewrite.py`.

**Interfaces:**

```python
def match_item(spec: ItemSpec, segment: str, rf: RuleFile, table: FeatureTable) -> bool
def find_matches(word: Word, rule: Rule, rf: RuleFile,
                 table: FeatureTable) -> list[tuple[int, int, dict[int, str]]]
    """Non-overlapping (start, stop, captures) triples, leftmost-longest, all evaluated
    against the PRE-RULE word (I-6). `captures` maps capture index -> the matched
    segment string, gathered from both the target and the environment (I-33).
    Epenthesis rules return zero-width spans."""
def apply_rule(word: Word, rule: Rule, rf: RuleFile, table: FeatureTable, stage: str) -> Word
def apply_section(word: Word, rules: Sequence[Rule], rf: RuleFile,
                  table: FeatureTable, stage: str) -> Word
class RuleError(Exception): ...
```

Matching details the implementer must get right:
- left context matched right-to-left ending at the span start; right context left-to-right from
  the span end; `#` matches only at position 0 / `len(segments)`; `$` at a position in
  `word.morphemes`; `.` at a syllable start; `ˈ` at the stressed syllable's first segment.
- `optional` matches 0 or 1 segment, `star` 0 or more, greedy with backtracking.
- an inline set matches any one of its members; a class matches any member of `rf.classes[name]`.
- a capture on an item records the **single segment** it matched (a capture on a multi-segment
  context item is a `ParseError` in Task 5a — sets and classes match one segment each).
- feature-change replacement: `table.apply_changes` per matched segment, exact lookup, `RuleError`
  when it fails (I-4).

- [ ] **Step 1: Write the failing test** — `tests/test_rewrite.py`

```python
import pytest
from helpers import TABLE, w
from strands.dsl import parse_rules
from strands.word import Word
from strands.rewrite import apply_rule, apply_section, RuleError

def rr(src):
    rf = parse_rules(src, TABLE)
    return rf, rf.sections["substitute"]

def one(src, ipa):
    rf, rules = rr(src)
    return apply_rule(w(ipa), rules[0], rf, TABLE, "substitute")

def test_simple_substitution_applies_everywhere():
    assert one("[inventory]\np b a\n[substitute]\np -> b\n", "papa").segments == ("b","a","b","a")

def test_one_trace_entry_per_changing_rule():
    out = one("[inventory]\np b a\n[substitute]\np -> b\n", "papa")
    assert len(out.trace) == 1 and out.trace[0].tag == "attested"
    assert out.trace[0].before == "papa" and out.trace[0].after == "baba"

def test_no_trace_entry_when_nothing_matches():
    assert one("[inventory]\np b a\n[substitute]\np -> b\n", "aa").trace == ()

def test_class_target():
    assert one("[inventory]\np t a\n[classes]\nX = p t\n[substitute]\nX -> a\n",
               "pt").segments == ("a", "a")

def test_derived_class_target():
    assert one("[inventory]\nk s a\n[substitute]\nFRIC -> a\n", "ksa").segments == ("k","a","a")

def test_feature_bundle_target_and_exact_feature_change():
    assert one("[inventory]\nk kʼ a\n[substitute]\n[C -sonorant] -> [+ejective]\n",
               "ka").segments == ("kʼ", "a")

def test_inexact_feature_change_raises_ruleerror():
    with pytest.raises(RuleError):
        one("[inventory]\nh\n[substitute]\nh -> [+lateral]\n", "h")

def test_deletion_and_epenthesis():
    assert one("[inventory]\np a\n[substitute]\np -> 0\n", "pap").segments == ("a",)
    assert one("[inventory]\ns k i\n[substitute]\n0 -> i / # _ s\n",
               "ski").segments == ("i", "s", "k", "i")

def test_word_edge_context():
    assert one("[inventory]\nt d a\n[substitute]\nd -> t / _ #\n", "dad").segments == ("d","a","t")

def test_application_is_simultaneous_not_iterative():
    assert one("[inventory]\na b\n[substitute]\nb -> a / a _\n", "abb").segments == ("a","a","b")

def test_matches_are_non_overlapping_leftmost():
    assert one("[inventory]\na b\n[substitute]\na a -> b\n", "aaa").segments == ("b", "a")

def test_rules_apply_in_file_order_and_feed_each_other():
    rf, rules = rr("[inventory]\na b k\n[substitute]\na -> b\nb -> k\n")
    assert apply_section(w("a"), rules, rf, TABLE, "substitute").segments == ("k",)

def test_optional_and_star_contexts():
    assert one("[inventory]\np a b\n[substitute]\np -> b / a (a) _\n", "aap").segments[-1] == "b"
    assert one("[inventory]\np a b\n[substitute]\np -> b / a (a) _\n", "ap").segments[-1] == "b"
    assert one("[inventory]\np a b\n[substitute]\np -> b / # a* _\n", "aaap").segments[-1] == "b"

def test_inline_set_matches_any_member():
    src = "[inventory]\np l n r a\n[substitute]\n0 -> a / p _ {l n r}\n"
    assert one(src, "pl").segments == ("p", "a", "l")
    assert one(src, "pn").segments == ("p", "a", "n")
    assert one(src, "pp").segments == ("p", "p")

def test_capture_and_backreference_copy_epenthesis():
    """I-33 / Welsh pobl-type copy epenthesis."""
    src = "[inventory]\np b o l a\n[substitute]\n0 -> \\1 / [V]:1 b _ l #\n"
    assert one(src, "pobl").segments == ("p", "o", "b", "o", "l")

def test_captures_in_a_target_give_metathesis():
    src = "[inventory]\ne w i θ ɾ\n[substitute]\nθ:1 ɾ:2 -> \\2 \\1 / _ #\n"
    assert one(src, "ewiθɾ").segments == ("e", "w", "i", "ɾ", "θ")

def test_morpheme_and_syllable_and_stress_contexts():
    rf, rules = rr("[inventory]\ni a p\n[substitute]\n0 -> i / $ _ #\n")
    wd = Word(segments=("a", "p"), morphemes=frozenset({2}))
    assert apply_rule(wd, rules[0], rf, TABLE, "substitute").segments == ("a", "p", "i")
    rf2, rules2 = rr("[inventory]\na aː p\n[substitute]\na -> aː / ˈ_\n")
    wd2 = Word(segments=("a", "p", "a"), syllables=(0, 1), stress=0)
    assert apply_rule(wd2, rules2[0], rf2, TABLE, "substitute").segments == ("aː", "p", "a")

def test_multi_segment_replacement_shifts_annotations():
    rf, rules = rr("[inventory]\np i a\n[substitute]\np -> p i\n")
    wd = Word(segments=("p", "a"), morphemes=frozenset({2}))
    out = apply_rule(wd, rules[0], rf, TABLE, "substitute")
    assert out.segments == ("p", "i", "a") and out.morphemes == frozenset({3})
```

- [ ] **Steps 2–4. Step 5: Commit** —
  `feat(strands): rewrite engine with captures, backreferences and inline sets`

---

## Task 8: Substitute stage

**Depends on:** Task 7

**Files:** create `src/strands/substitute.py`, `tests/test_substitute.py`.

**Interfaces:** `def substitute(word: Word, rf: RuleFile, table: FeatureTable) -> Word` — spec
§4.2a: apply `rf.sections['substitute']` in file order.

- [ ] **Step 1: Failing test**

```python
from helpers import TABLE
from strands.dsl import parse_rules
from strands.word import Word
from strands.substitute import substitute

def test_runs_the_section_in_order():
    rf = parse_rules("[inventory]\np b f v\n[substitute]\np -> b\nv -> f\n", TABLE)
    out = substitute(Word(segments=("p", "v")), rf, TABLE)
    assert out.segments == ("b", "f") and [t.stage for t in out.trace] == ["substitute"] * 2

def test_absent_section_is_a_noop():
    rf = parse_rules("[inventory]\np\n", TABLE)
    wd = Word(segments=("p",))
    assert substitute(wd, rf, TABLE) == wd
```

- [ ] **Steps 2–4. Step 5: Commit** — `feat(strands): substitute stage`

---

## Task 9: Inventory fallback

**Depends on:** Task 8

**Files:** modify `src/strands/substitute.py`; create `tests/test_fallback.py`.

**Interfaces:**

```python
def fallback(word: Word, rf: RuleFile, table: FeatureTable) -> Word
    """Spec §4.2b: each segment not in rf.inventory becomes the nearest NON-MARGINAL
    inventory segment by weighted distance (I-12); one TraceEntry per replacement,
    tag='fallback', rule_id='fallback'. This is the ONLY approximating step (I-4)."""
def substitute_stage(word: Word, rf: RuleFile, table: FeatureTable) -> Word
```

- [ ] **Step 1: Failing test**

```python
def test_off_inventory_segment_is_replaced_by_the_nearest():
    rf = parse_rules("[inventory]\nb f a\n", TABLE)
    out = fallback(Word(segments=("pˠ", "a")), rf, TABLE)
    assert out.segments == ("b", "a") and out.trace[0].tag == "fallback"

def test_marginal_segments_are_never_chosen():
    rf = parse_rules("[inventory]\nb a\nmarginal: p\n", TABLE)
    assert fallback(Word(segments=("pˠ",)), rf, TABLE).segments == ("b",)

def test_ties_break_by_inventory_order():
    """S2: a real tie, hard-coded both ways."""
    a = parse_rules("[inventory]\nm ŋ a\n", TABLE)
    b = parse_rules("[inventory]\nŋ m a\n", TABLE)
    assert fallback(Word(segments=("n̪ˠ",)), a, TABLE).segments == ("m",)
    assert fallback(Word(segments=("n̪ˠ",)), b, TABLE).segments == ("ŋ",)

def test_weights_change_the_choice():
    rf = parse_rules("[inventory]\nk c a\n[weights]\nfront = 20.0\n", TABLE)
    assert fallback(Word(segments=("ɟ",)), rf, TABLE).segments == ("c",)

def test_inventory_segments_are_untouched_and_untraced():
    rf = parse_rules("[inventory]\nb a\n", TABLE)
    wd = Word(segments=("b", "a"))
    assert fallback(wd, rf, TABLE) == wd

def test_fallback_count():
    rf = parse_rules("[inventory]\nb a\n", TABLE)
    assert fallback(Word(segments=("pˠ", "pʲ")), rf, TABLE).fallback_count() == 2

def test_fallback_is_deterministic():
    rf = parse_rules("[inventory]\nb f a\n", TABLE)
    x = Word(segments=("pˠ", "vʲ", "a"))
    assert fallback(x, rf, TABLE) == fallback(x, rf, TABLE)
```

*(Verify the two tie expectations against the built table before committing — replace them with the
measured winners if `n̪ˠ` is not equidistant from `m` and `ŋ`; the test must assert one value, never
a set.)*

- [ ] **Steps 2–4. Step 5: Commit** — `feat(strands): nearest-segment inventory fallback`

**Acceptance:** milestone 2 complete.

---

## Task 10: Syllabifier (nucleus-aware)

**Depends on:** Tasks 4, 5b

**Files:** create `src/strands/syllabify.py`, `tests/test_syllabify.py`.

**Interfaces:**

```python
SONORITY_DOC: str        # the I-13 scale, in the module docstring

def sonority(segment: str, table: FeatureTable) -> int
def group_nuclei(segments: Sequence[str], spec: SyllableSpec,
                 table: FeatureTable) -> list[tuple[int, int]]
    """Spec §12.B: maximal vowel runs are split into nuclei; a pair listed in
    spec.nuclei is ONE nucleus; otherwise each vowel is its own nucleus (hiatus)."""
def legal_onset(cluster: tuple[str, ...], spec: SyllableSpec, table: FeatureTable) -> bool
def legal_coda(cluster: tuple[str, ...], spec: SyllableSpec, table: FeatureTable) -> bool
def syllabify(word: Word, rf: RuleFile, table: FeatureTable) -> Word
    """Maximal onset subject to legality; sets word.syllables, word.nuclei and, on
    failure, word.illegal = the minimal unparseable span. Never raises. Resolves
    Word._pending_stress to a syllable index (S1). Appends one TraceEntry."""
```

Algorithm:
1. Domains: `domain = word` → the whole word; `domain = stem` → spans between `$` positions.
2. `group_nuclei` over each domain; a domain with no nucleus is marked illegal in full.
3. Interludes: longest suffix that is a legal onset; remainder must be a legal coda; back off one
   segment at a time; if nothing works, mark the interlude illegal and split at the sonority
   minimum.
4. Word-initial consonants must be a legal onset (or empty, unless `onset-required = yes`);
   word-final ones a legal coda plus up to `len(appendix)` appendix segments.
5. Legality = template ∧ onset-set ∧ coda-set ∧ sonority ∧ ¬banned; `any`/`off`/empty components
   are skipped. `onsets`/`codas` are complete sets including singletons (spec §12.D), so a
   singleton absent from a non-`any` list is illegal.
6. `bans` are checked over the domain after the parse; a match marks its span.

- [ ] **Step 1: Failing test** — `tests/test_syllabify.py`

```python
import pytest
from helpers import TABLE, w
from strands.dsl import parse_rules
from strands.word import Word
from strands.syllabify import syllabify, group_nuclei, legal_onset

CV = ("[inventory]\np t k b s l r a i u aː iə\n" if False else
      "[inventory]\np t k b s l r a i u aː\n"
      "[syllable]\ntemplate = (C)(C)N(C)\nonsets = p t k b s l r pl pr st\n"
      "codas = p t k s st\nsonority = on\n")

def syl(src, ipa):
    rf = parse_rules(src, TABLE)
    return syllabify(w(ipa), rf, TABLE)

def test_simple_cv_parse():
    out = syl(CV, "pata")
    assert out.syllables == (0, 2) and out.illegal == frozenset()

def test_maximal_onset_subject_to_legality():
    assert syl(CV, "apla").syllables == (0, 1)      # a.pla, 'pl' is a legal onset
    assert syl(CV, "apta").syllables == (0, 2)      # ap.ta, 'pt' is not

def test_singleton_absent_from_the_onset_list_is_illegal():
    """Spec §12.D: the list is complete, so an unlisted singleton is not licensed."""
    src = CV.replace("onsets = p t k b s l r pl pr st", "onsets = p t")
    assert syl(src, "kata").illegal

def test_illegal_initial_cluster_is_marked_not_raised():
    out = syl(CV, "kta")
    assert out.illegal == frozenset({0, 1}) and "syllabify" in [t.stage for t in out.trace]

def test_minimal_illegal_span():
    out = syl(CV, "apkta")
    assert 0 not in out.illegal and out.illegal

def test_appendix_licenses_extra_final_coronals():
    src = CV + "appendix = s t\n"
    assert syl(src, "apst").illegal == frozenset()

def test_nuclei_grouping_makes_a_diphthong_one_syllable():
    src = ("[inventory]\np i ə a\n[syllable]\ntemplate = (C)N(C)\nnuclei = iə\n"
           "onsets = p\ncodas = p\nsonority = off\n")
    out = syl(src, "piə")
    assert len(out.syllables) == 1 and out.nuclei == ((1, 3),)

def test_without_a_nuclei_declaration_the_same_string_is_hiatus():
    src = ("[inventory]\np i ə a\n[syllable]\ntemplate = (C)N(C)\n"
           "onsets = p\ncodas = p\nsonority = off\n")
    out = syl(src, "piə")
    assert len(out.syllables) == 2                 # Georgian behaviour (spec §12.B)

def test_sonority_on_rejects_falling_onsets_and_off_accepts_them():
    on = ("[inventory]\np l a\n[syllable]\ntemplate = (C)(C)N(C)\nonsets = any\nsonority = on\n")
    off = on.replace("sonority = on", "sonority = off")
    assert syl(on, "lpa").illegal and syl(off, "lpa").illegal == frozenset()

def test_sc_clusters_are_exempt_from_sonority():
    src = "[inventory]\ns t a\n[syllable]\ntemplate = (C)(C)N(C)\nonsets = any\nsonority = on\n"
    assert syl(src, "sta").illegal == frozenset()

def test_bans_mark_their_span():
    src = ("[inventory]\np t a aː\n[syllable]\ntemplate = any\nonsets = any\ncodas = any\n"
           "sonority = off\nbans = [V +long] C C\n")
    assert 0 in syl(src, "aːpta").illegal

def test_stem_domain_uses_morpheme_boundaries():
    src = ("[inventory]\np t a\n[syllable]\ntemplate = any\nonsets = any\ncodas = any\n"
           "sonority = off\ndomain = stem\n")
    rf = parse_rules(src, TABLE)
    out = syllabify(Word(segments=("p","a","t","a"), morphemes=frozenset({2})), rf, TABLE)
    assert out.syllables == (0, 2)

def test_pending_stress_is_converted_to_a_syllable_index():
    """S1: tokenize gives a segment index; syllabify converts it."""
    out = syl(CV, "paˈta")
    assert out.stress == 1

def test_syllabify_is_idempotent():
    rf = parse_rules(CV, TABLE)
    a = syl(CV, "pata")
    assert syllabify(a, rf, TABLE).syllables == a.syllables
```

*(Delete the dead `if False else` in `CV` when writing the file — it is here only to show that the
inventory line must not contain a diphthong row, per I-2/I-35.)*

- [ ] **Steps 2–4. Step 5: Commit** — `feat(strands): nucleus-aware syllabifier`

---

## Task 11: Repair loop and `cluster-fallback`

**Depends on:** Tasks 7, 10

**Files:** create `src/strands/repair.py`, `tests/test_repair.py`.

**Spec §12.A governs this task and overrides §4.4.**

**Interfaces:**

```python
MAX_REPAIR_PASSES = 10

def repair(word: Word, rf: RuleFile, table: FeatureTable) -> Word
    """Spec §12.A:
       pass = apply every [repair] rule in file order, UNCONDITIONALLY (many are active
       processes, not fixes: Dutch final devoicing, Welsh fortition/prothesis);
       re-syllabify after any rule that changed the word, count-preserving or not;
       run a further pass only while illegal marks remain AND the previous pass changed
       the segment string (cycle detection on the string); cap MAX_REPAIR_PASSES;
       then flag UNREPAIRED."""
def cluster_fallback(word: Word, rf: RuleFile, table: FeatureTable) -> Word
    """Spec §12.E: when rf.cluster_fallback == 'same-length', replace an illegal onset or
    coda span with the attested cluster of the SAME LENGTH minimising summed segment
    feature distance (ties: list order), tagged %fallback. No candidate -> leave the
    marks and let the caller flag UNREPAIRED. Runs at the end of each repair pass."""
```

- [ ] **Step 1: Failing test**

```python
SRC = ("[inventory]\ns k i a t d\n[syllable]\ntemplate = (C)N(C)\nonsets = s k i t d\n"
       "codas = s k t\nsonority = off\n"
       "[repair]\n0 -> i / # _ s [C -sonorant]   %attested\nd -> t / _ #   %attested\n")

def test_repair_fixes_an_illegal_onset_and_clears_the_mark():
    rf = parse_rules(SRC, TABLE)
    out = repair(syllabify(w("ski"), rf, TABLE), rf, TABLE)
    assert out.segments == ("i", "s", "k", "i") and out.illegal == frozenset()
    assert "UNREPAIRED" not in out.flags

def test_active_rules_apply_even_when_nothing_is_illegal():
    """Spec §12.A: [repair] is unconditional — final devoicing must fire on a legal word."""
    rf = parse_rules(SRC, TABLE)
    out = repair(syllabify(w("kad"), rf, TABLE), rf, TABLE)
    assert out.segments == ("k", "a", "t")

def test_resyllabification_happens_after_a_count_changing_rule():
    rf = parse_rules(SRC, TABLE)
    assert repair(syllabify(w("ski"), rf, TABLE), rf, TABLE).syllables == (0, 2)

def test_count_preserving_repair_can_clear_illegality():
    """The draft-1 loop could not do this; §12.A's re-syllabify-after-any-change can."""
    src = ("[inventory]\np t a\n[syllable]\ntemplate = (C)N(C)\nonsets = t\ncodas = t\n"
           "sonority = off\n[repair]\np -> t   %design\n")
    rf = parse_rules(src, TABLE)
    out = repair(syllabify(w("pa"), rf, TABLE), rf, TABLE)
    assert out.illegal == frozenset() and "UNREPAIRED" not in out.flags

def test_unrepairable_word_is_flagged_and_the_loop_terminates():
    src = ("[inventory]\nk t a\n[syllable]\ntemplate = (C)N\nonsets = k\ncodas = k\n"
           "sonority = off\n[repair]\nk -> k   %design\n")
    rf = parse_rules(src, TABLE)
    out = repair(syllabify(w("kta"), rf, TABLE), rf, TABLE)
    assert "UNREPAIRED" in out.flags

def test_cycle_detection_stops_an_oscillating_rule_set():
    src = ("[inventory]\na b\n[syllable]\ntemplate = N\nonsets = any\ncodas = any\n"
           "sonority = off\nbans = a\n[repair]\na -> b   %design\nb -> a   %design\n")
    rf = parse_rules(src, TABLE)
    out = repair(syllabify(w("a"), rf, TABLE), rf, TABLE)
    assert "UNREPAIRED" in out.flags
    assert len([t for t in out.trace if t.stage == "repair"]) < 100   # bounded, not runaway

def test_cluster_fallback_replaces_an_illegal_span_with_a_same_length_attested_cluster():
    """Spec §12.E — synthetic, as no attested Georgian example exists."""
    src = ("[inventory]\np t k s l a\n[syllable]\ntemplate = (C)(C)N\nonsets = p t k s l pl kl\n"
           "codas = any\nsonority = off\n[repair]\ncluster-fallback = same-length\n")
    rf = parse_rules(src, TABLE)
    out = repair(syllabify(w("tla"), rf, TABLE), rf, TABLE)
    assert out.segments[:2] in {("p", "l"), ("k", "l")} and out.illegal == frozenset()
    assert any(t.tag == "fallback" for t in out.trace)

def test_cluster_fallback_with_no_candidate_leaves_unrepaired():
    src = ("[inventory]\np t l a\n[syllable]\ntemplate = (C)(C)(C)N\nonsets = p t l\n"
           "codas = any\nsonority = off\n[repair]\ncluster-fallback = same-length\n")
    rf = parse_rules(src, TABLE)
    assert "UNREPAIRED" in repair(syllabify(w("ptla"), rf, TABLE), rf, TABLE).flags

def test_repair_is_deterministic():
    rf = parse_rules(SRC, TABLE)
    x = syllabify(w("ski"), rf, TABLE)
    assert repair(x, rf, TABLE) == repair(x, rf, TABLE)
```

*(The `cluster_fallback` test asserts a set of two because both `pl` and `kl` may be equidistant;
before committing, compute the real winner and assert exactly it — S2.)*

- [ ] **Steps 2–4. Step 5: Commit** —
  `feat(strands): unconditional repair loop with cycle detection and cluster fallback`

**Acceptance:** milestone 3 complete.

---

## Task 12: Stress package — registry, weight, `initial`, `keep-source`

**Depends on:** Tasks 4, 5b, 6, 10

**Files:** create `src/strands/stress/__init__.py`, `src/strands/stress/initial.py`,
`src/strands/stress/keep_source.py`, `tests/test_stress_framework.py`. (`stress/params.py` already
exists from Task 6 — **do not edit it**; Tasks 13–15 add their own modules.)

**Interfaces:**

```python
# stress/__init__.py
from .params import PROCEDURE_PARAMS

Procedure = Callable[[Word, StressSpec, FeatureTable], int | None]
PROCEDURES: dict[str, Procedure]        # populated by module import, see `register`

def register(name: str) -> Callable[[Procedure], Procedure]
def syllable_weight(word: Word, i: int, table: FeatureTable) -> str
    """'light' (open, short nucleus) | 'heavy' (long/branching nucleus, or one coda C)
    | 'superheavy' (long nucleus + coda, or two coda C). Counts NUCLEI, not vowel
    segments (spec §12.B)."""
def assign_stress(word: Word, rf: RuleFile, table: FeatureTable) -> Word
    """Dispatch on rf.stress.procedure; sets word.stress; appends a TraceEntry
    (stage='stress', rule_id=f'stress:{procedure}'). Unknown name -> StressError."""
class StressError(Exception): ...
```

Procedures here: `initial` (param `mark = on|off`, default `on`; `off` means the respell stage
prints no stress mark — Georgian, digest §4.3) and `keep-source` (use the incoming `word.stress`;
if `None`, syllable 0).

- [ ] **Step 1: Failing test**

```python
import pytest
from helpers import TABLE, w
from strands.dsl import parse_rules
from strands.syllabify import syllabify
from strands.stress import assign_stress, syllable_weight, StressError
from strands.stress.params import PROCEDURE_PARAMS

BASE = ("[inventory]\np t k a aː i n s\n[syllable]\ntemplate = (C)N(C)(C)\nonsets = p t k n s\n"
        "codas = p t k n s\nsonority = off\n")

def stressed(src, ipa):
    rf = parse_rules(src, TABLE)
    return assign_stress(syllabify(w(ipa), rf, TABLE), rf, TABLE)

def test_initial_stresses_syllable_zero():
    out = stressed(BASE + "[stress]\nprocedure = initial\n", "patapa")
    assert out.stress == 0 and out.ipa().startswith("ˈ")

def test_initial_on_a_monosyllable():
    assert stressed(BASE + "[stress]\nprocedure = initial\n", "pat").stress == 0

def test_initial_mark_off_still_sets_stress_but_records_the_param():
    rf = parse_rules(BASE + "[stress]\nprocedure = initial\nmark = off\n", TABLE)
    out = assign_stress(syllabify(w("pata"), rf, TABLE), rf, TABLE)
    assert out.stress == 0 and rf.stress.params["mark"] == "off"

def test_keep_source_preserves_the_incoming_mark():
    assert stressed(BASE + "[stress]\nprocedure = keep-source\n", "paˈta").stress == 1

def test_keep_source_defaults_to_initial_when_unmarked():
    assert stressed(BASE + "[stress]\nprocedure = keep-source\n", "pata").stress == 0

def test_trace_entry():
    out = stressed(BASE + "[stress]\nprocedure = initial\n", "pata")
    assert out.trace[-1].stage == "stress" and out.trace[-1].rule_id == "stress:initial"

def test_syllable_weight_counts_nuclei():
    rf = parse_rules(BASE + "nuclei = ai\n[stress]\nprocedure = initial\n", TABLE)
    out = syllabify(w("pai"), rf, TABLE)
    assert syllable_weight(out, 0, TABLE) == "heavy"      # branching nucleus, open syllable

def test_weight_classes():
    rf = parse_rules(BASE + "[stress]\nprocedure = initial\n", TABLE)
    out = syllabify(w("patakaːnt"), rf, TABLE)
    assert {syllable_weight(out, i, TABLE) for i in range(len(out.syllables))} <= \
        {"light", "heavy", "superheavy"}

def test_unknown_procedure_raises():
    with pytest.raises((StressError, Exception)):
        stressed(BASE + "[stress]\nprocedure = wibble\n", "pata")

def test_params_registry_is_the_single_source_of_truth():
    assert PROCEDURE_PARAMS["penult"] == frozenset()
    assert "window" in PROCEDURE_PARAMS["dutch-weight"]
```

- [ ] **Steps 2–4. Step 5: Commit** —
  `feat(strands): stress package with registry, weight, initial and keep-source`

---

## Task 13: `penult` procedure

**Depends on:** Task 12. **Independent of Tasks 14, 15** (separate module — spec §12.I).

**Files:** create `src/strands/stress/penult.py`, `tests/test_stress_penult.py`.

**Source:** `sources/welsh/digest.md` §4.1 — penultimate syllable of polysyllables; monosyllables
stress their only syllable; stress is recomputed after affixation, never carried. **No parameters.**

- [ ] **Step 1: Failing test**

```python
import pytest
from helpers import TABLE, w
from strands.dsl import parse_rules
from strands.syllabify import syllabify
from strands.stress import assign_stress

BASE = ("[inventory]\np t k b d ɡ m n l r s ʃ x a e i o u aː eː iː oː uː ə\n"
        "[syllable]\ntemplate = (C)(C)N(C)(C)\nonsets = any\ncodas = any\nsonority = off\n"
        "[stress]\nprocedure = penult\n")

@pytest.mark.parametrize("ipa,expected", [("pata", 0), ("patata", 1), ("pat", 0),
                                          ("patatata", 2)])
def test_penult(ipa, expected):
    rf = parse_rules(BASE, TABLE)
    assert assign_stress(syllabify(w(ipa), rf, TABLE), rf, TABLE).stress == expected

def test_penult_ignores_weight():
    rf = parse_rules(BASE, TABLE)
    assert assign_stress(syllabify(w("paːtata"), rf, TABLE), rf, TABLE).stress == 1
```

- [ ] **Steps 2–4. Step 5: Commit** — `feat(strands): penult stress procedure`

---

## Task 14: `cairene` procedure

**Depends on:** Task 12. **Independent of Tasks 13, 15.**

**Files:** create `src/strands/stress/cairene.py`, `tests/test_stress_cairene.py`.

**Source:** `sources/arabic-egy/digest.md` §4, worked table at **lines 868–886 — 17 rows, not 16**
(R16; spec §8 also says 17). Rule:
1. stress the final syllable if it is superheavy (`CVːC`, `CVː`, `CVCC`);
2. else stress the antepenult if penult and antepenult are both light **and** the pre-antepenult is
   not also light (a heavy pre-antepenult licenses it: *muxˈtalifa*; an all-light one blocks it:
   *kataˈbitu*);
3. else stress the penult. A **heavy antepenult rejects stress** (*madˈrasa*, *jikˈtibu*,
   *marˈtaba*, *mækˈtæbæ*) — the signature Cairene pattern.
Epenthetic vowels count (*binˈtina*), which falls out of the stage order (stress runs after repair)
— assert it rather than coding it. **No parameters.**

- [ ] **Step 1: Failing test** — the table below is transcribed verbatim from digest lines 869–886;
  do not paraphrase or drop a row.

```python
import pytest
from helpers import TABLE, w
from strands.dsl import parse_rules
from strands.syllabify import syllabify
from strands.stress import assign_stress

CAIRENE = ("[inventory]\nb t d k ɡ ʔ f s z ʃ x ɣ ħ ʕ h m n l r w j sˤ tˤ dˤ zˤ "
           "a i u aː iː uː eː oː e o æ\n"
           "[syllable]\ntemplate = CN(C)(C)\nonsets = b t d k ɡ ʔ f s z ʃ x ɣ ħ ʕ h m n l r w j "
           "sˤ tˤ dˤ zˤ\ncodas = b t d k ɡ ʔ f s z ʃ x ɣ ħ ʕ h m n l r w j sˤ tˤ dˤ zˤ\n"
           "sonority = off\n[stress]\nprocedure = cairene\n")

# digest §4, lines 869–886: (plain, stressed)
CAIRENE_STRESS_TABLE = [
    ("katabt",    "kaˈtabt"),      # 1, final CVCC
    ("ʔabeh",     "ʔaˈbeh"),       # 1
    ("sakakiːn",  "sakaˈkiːn"),    # 1, final CVːC
    ("tˤalabaːt", "tˤalaˈbaːt"),   # 1
    ("ʔabadan",   "ˈʔabadan"),     # 2, penult+antepenult light, no pre-antepenult
    ("muxtalifa", "muxˈtalifa"),   # 2, pre-antepenult heavy
    ("katabitu",  "kataˈbitu"),    # 3, pre-antepenult also light -> step 2 blocked
    ("jiktibu",   "jikˈtibu"),     # 3, heavy antepenult rejects stress
    ("ʕamalti",   "ʕaˈmalti"),     # 3
    ("martaba",   "marˈtaba"),     # 3, heavy antepenult rejects stress
    ("beːtak",    "ˈbeːtak"),      # 3
    ("madrasa",   "madˈrasa"),     # 3, the signature Cairene pattern
    ("bintina",   "binˈtina"),     # 3, epenthetic penult vowel
    ("katab",     "ˈkatab"),       # 3, final CVC is light; two syllables
    ("katabit",   "ˈkatabit"),     # 2
    ("katba",     "ˈkatba"),       # 3
    ("maktaba",   "mækˈtæbæ"),     # 3, heavy antepenult rejects stress
]

def test_the_table_has_seventeen_rows():
    assert len(CAIRENE_STRESS_TABLE) == 17          # R16 / spec §8

@pytest.mark.parametrize("plain,expected", CAIRENE_STRESS_TABLE)
def test_cairene_stress(plain, expected):
    rf = parse_rules(CAIRENE, TABLE)
    got = assign_stress(syllabify(w(plain), rf, TABLE), rf, TABLE)
    assert got.ipa().replace(".", "") == expected

def test_heavy_antepenult_rejects_stress():
    rf = parse_rules(CAIRENE, TABLE)
    assert assign_stress(syllabify(w("madrasa"), rf, TABLE), rf, TABLE).stress == 1

def test_epenthetic_vowel_counts_for_stress():
    rf = parse_rules(CAIRENE, TABLE)
    assert assign_stress(syllabify(w("bintina"), rf, TABLE), rf, TABLE).stress == 1
```

*(The last row's expected form is the digest's own `mækˈtæbæ` — the vowel quality is the source's,
not a stress fact; if the stress procedure is right but the vowels differ, compare stress position
only for that row and note why in a comment.)*

- [ ] **Steps 2–4. Step 5: Commit** —
  `feat(strands): Cairene stress procedure (digest §4, all 17 rows)`

**Acceptance:** all 17 rows pass. A row that cannot be made to pass becomes an `xfail` naming the
digest line — never a deletion.

---

## Task 15: `dutch-weight` procedure

**Depends on:** Task 12. **Independent of Tasks 13, 14.**

**Files:** create `src/strands/stress/dutch_weight.py`, `tests/test_stress_dutch.py`.

**Source:** `sources/dutch/digest.md` §4 "The practical rule" (lines 671–687), explicitly
*constructed by the digest, not stated by any source* — so `dutch.rules` tags its `[stress]` line
`%design`. Six ordered steps, verbatim:
1. a syllable containing schwa is unstressable; prefer the syllable immediately before it;
2. final syllable superheavy (A-vowel/diphthong + C(+coronals), or B-vowel + CC) or ending in a
   diphthong → stress the final;
3. else penult closed with a full vowel → stress the penult (never skip it);
4. else final syllable closed and B-class (lax) → stress the antepenult (weak);
5. else → stress the penult;
6. never stress outside the last three syllables. **Param:** `window = 3` (default 3).

- [ ] **Step 1: Failing test** — the digest's own worked examples (line 683–685):

```python
DUTCH = ("[inventory]\np b t d k ɡ f v s z ʃ ʒ x ɣ h m n ŋ l r ʋ j "
         "ɑ ɛ ɪ ɔ ʏ ə a e i o u y ø aː eː iː oː uː yː øː\n"
         "[syllable]\ntemplate = (C)(C)(C)N(C)(C)\nonsets = any\ncodas = any\nsonority = off\n"
         "[stress]\nprocedure = dutch-weight\n")

# digest §4 line 683-685: (plain, stressed, rule)
DUTCH_STRESS_TABLE = [
    ("avɔntyr",  "a.vɔn.ˈtyr", 2),
    ("aɣɛnda",   "a.ˈɣɛn.da",  3),
    ("ɑlbatrɔs", "ˈɑl.ba.trɔs", 4),
    ("arena",    "a.ˈre.na",   5),
    ("avokado",  "a.vo.ˈka.do", 5),
    ("mirakəl",  "mi.ˈra.kəl", 1),
]

@pytest.mark.parametrize("plain,expected,rule", DUTCH_STRESS_TABLE)
def test_dutch_worked_examples(plain, expected, rule):
    rf = parse_rules(DUTCH, TABLE)
    assert assign_stress(syllabify(w(plain), rf, TABLE), rf, TABLE).ipa() == expected

def test_schwa_is_never_stressed():
    rf = parse_rules(DUTCH, TABLE)
    out = assign_stress(syllabify(w("mirakəl"), rf, TABLE), rf, TABLE)
    assert out.segments[out.syllables[out.stress]] != "ə"

def test_three_syllable_window_is_respected():
    rf = parse_rules(DUTCH, TABLE)
    out = assign_stress(syllabify(w("avokadokado"), rf, TABLE), rf, TABLE)
    assert out.stress >= len(out.syllables) - 3

def test_window_parameter_is_read():
    rf = parse_rules(DUTCH + "window = 3\n", TABLE)
    assert rf.stress.params["window"] == "3"
```

*(The syllabification in the expected strings is the digest's own. If our syllabifier disagrees with
the digest's dots for a row, compare stress position only for that row and say so in a comment —
the syllabifier is tested in Task 10, not here.)*

- [ ] **Steps 2–4. Step 5: Commit** — `feat(strands): dutch-weight stress procedure`

---

## Task 16: Post-stress stage

**Depends on:** Tasks 7, 10, 12

**Files:** create `src/strands/poststress.py`, `tests/test_poststress.py`.

**Interfaces:**

```python
def post_stress(word: Word, rf: RuleFile, table: FeatureTable) -> Word
    """Spec §4.5: apply rf.sections['post-stress'] in file order after assign_stress;
    re-syllabify at the end if any rule changed the segment count, preserving the
    stressed syllable's identity."""
```

- [ ] **Step 1: Failing test**

```python
BASE = ("[inventory]\np t a aː i\n[syllable]\ntemplate = (C)N(C)\nonsets = p t\ncodas = p t\n"
        "sonority = off\n[stress]\nprocedure = penult\n")

def test_post_stress_rule_sees_the_stress_mark():
    rf = parse_rules(BASE + "[post-stress]\na -> aː / ˈ_ C N   %design\n", TABLE)
    out = post_stress(assign_stress(syllabify(w("pata"), rf, TABLE), rf, TABLE), rf, TABLE)
    assert out.segments == ("p", "aː", "t", "a")

def test_post_stress_resyllabifies_and_keeps_the_stressed_syllable():
    rf = parse_rules(BASE + "[post-stress]\n0 -> i / t _ #   %design\n", TABLE)
    stressed = assign_stress(syllabify(w("pat"), rf, TABLE), rf, TABLE)
    out = post_stress(stressed, rf, TABLE)
    assert out.segments == ("p", "a", "t", "i") and out.stress == 0

def test_absent_section_is_a_noop():
    rf = parse_rules(BASE, TABLE)
    x = assign_stress(syllabify(w("pata"), rf, TABLE), rf, TABLE)
    assert post_stress(x, rf, TABLE) == x
```

- [ ] **Steps 2–4. Step 5: Commit** — `feat(strands): post-stress stage`

**Acceptance:** milestone 4 complete (Tasks 12–16).

---

## Task 17: Irish mutations and inflections

**Depends on:** Task 7

**Files:** create `rules/irish.rules` (sections `[meta] [inventory] [classes] [mutations]
[inflect]`), `src/strands/irish.py`, `tests/test_irish_mutations.py`.

**Interfaces:**

```python
def apply_mutation(word: Word, name: str, rf: RuleFile, table: FeatureTable) -> Word
    """name in {'LEN','ECL','HPREF','TPREF'}."""
def apply_inflection(word: Word, name: str, rf: RuleFile, table: FeatureTable) -> Word
    """name in {'GEN_M1','GEN_ACH','GEN_F2','GEN_M3','VOC_M1'} — five, not the spec §3
    list of four; GEN_M3 is additive and Task 5b's docstring says five (R25)."""
class IrishError(Exception): ...
```

**Rule content — transcribed from `sources/irish/digest.md` §3.1 (lenition), §3.2 (eclipsis), §3.3
(other initial changes), §3.5 (genitive/vocative).** `[classes]` carries the `BROAD`/`SLEN` pair of
I-41. Every line cites `# [wiki-irish-mutations §Summary table]` or the digest's own citation.

```
[mutations]
LEN:
pˠ -> fˠ / #_      %attested # [wiki-irish-mutations §Summary table]
pʲ -> fʲ / #_      %attested # ditto (one citation per line, copied from the digest)
bˠ -> w  / #_      %attested
bʲ -> vʲ / #_      %attested
mˠ -> w  / #_      %attested
mʲ -> vʲ / #_      %attested
fˠ -> 0  / #_      %attested # fh is silent
fʲ -> 0  / #_      %attested
t̪ˠ -> h / #_       %attested
tʲ -> h  / #_      %attested
d̪ˠ -> ɣ / #_       %attested
dʲ -> j  / #_      %attested
sˠ -> h  / #_      %attested
ʃ  -> h  / #_      %attested
k  -> x  / #_      %attested
c  -> ç  / #_      %attested
ɡ  -> ɣ  / #_      %attested
ɟ  -> j  / #_      %attested
# l/n rows are null in a two-way Connacht transcription (digest §3.1) — deliberately absent.
# Vowels and /ɾˠ ɾʲ/ do not lenite (digest §3.1) — deliberately absent.
ECL:
pˠ -> bˠ / #_      %attested
pʲ -> bʲ / #_      %attested
t̪ˠ -> d̪ˠ / #_      %attested
tʲ -> dʲ / #_      %attested
k  -> ɡ  / #_      %attested
c  -> ɟ  / #_      %attested
bˠ -> mˠ / #_      %attested
bʲ -> mʲ / #_      %attested
d̪ˠ -> n̪ˠ / #_      %attested
dʲ -> nʲ / #_      %attested
ɡ  -> ŋ  / #_      %attested
ɟ  -> ɲ  / #_      %attested
fˠ -> w  / #_      %attested
fʲ -> vʲ / #_      %attested
0  -> n̪ˠ / # _ [V +back]   %attested # n-prothesis (digest §3.3)
0  -> nʲ / # _ [V +front]   %attested
HPREF:
0 -> h / # _ V     %attested # [wiki-irish-mutations §Changes to vowel-initial words]
TPREF:
0 -> t̪ˠ / # _ [V +back]    %attested
0 -> tʲ / # _ [V +front]   %attested
sˠ -> t̪ˠ / #_      %attested # an tsolais
ʃ  -> tʲ / #_      %attested # an tSín
```

`[inflect]` encodes §3.5 as rules anchored at `_ #`:
- `GEN_M1` — slenderize the final consonant plus the vowel change the digest's *mac* → *mic*
  example requires: `[C +back] -> [+front -back] / _ #` then `a -> ɪ / _ [C +front] #`.
- `GEN_ACH` — `x -> j / ə _ #` (*marcach* → *marcaigh*).
- `GEN_F2` — slenderize + `0 -> ə / _ #` (*bróg* → *bróige*).
- `GEN_M3` — broaden + `0 -> ə / _ #` (*bádóir* → *bádóra*).
- `VOC_M1` — same content as `GEN_M1` (§3.5: the vocative takes the slenderized genitive stem).

- [ ] **Step 1: Write the failing tests** — `tests/test_irish_mutations.py`

```python
import pytest
from helpers import TABLE, w, irish, mutation_rows
from strands.irish import apply_mutation, apply_inflection

IRISH = irish()
def ipa(x): return x.ipa(marks=False)

@pytest.mark.parametrize("radical,lenited", [
    ("pˠ", "fˠ"), ("pʲ", "fʲ"), ("bˠ", "w"), ("bʲ", "vʲ"), ("mˠ", "w"), ("mʲ", "vʲ"),
    ("t̪ˠ", "h"), ("tʲ", "h"), ("d̪ˠ", "ɣ"), ("dʲ", "j"), ("sˠ", "h"), ("ʃ", "h"),
    ("k", "x"), ("c", "ç"), ("ɡ", "ɣ"), ("ɟ", "j"),
])
def test_lenition_table_digest_3_1(radical, lenited):
    assert ipa(apply_mutation(w(radical + "a"), "LEN", IRISH, TABLE)) == lenited + "a"

def test_fh_lenites_to_nothing():
    assert ipa(apply_mutation(w("fˠaː"), "LEN", IRISH, TABLE)) == "aː"

def test_vowels_and_taps_do_not_lenite():
    for s in ("aː", "ɾˠa", "ɾʲa"):
        assert ipa(apply_mutation(w(s), "LEN", IRISH, TABLE)) == s

@pytest.mark.parametrize("radical,eclipsed", [
    ("pˠ", "bˠ"), ("pʲ", "bʲ"), ("t̪ˠ", "d̪ˠ"), ("tʲ", "dʲ"), ("k", "ɡ"), ("c", "ɟ"),
    ("bˠ", "mˠ"), ("bʲ", "mʲ"), ("d̪ˠ", "n̪ˠ"), ("dʲ", "nʲ"), ("ɡ", "ŋ"), ("ɟ", "ɲ"),
    ("fˠ", "w"), ("fʲ", "vʲ"),
])
def test_eclipsis_table_digest_3_2(radical, eclipsed):
    assert ipa(apply_mutation(w(radical + "a"), "ECL", IRISH, TABLE)) == eclipsed + "a"

def test_eclipsis_of_a_vowel_initial_word_prefixes_n():
    assert ipa(apply_mutation(w("iːʃ"), "ECL", IRISH, TABLE)) == "nʲiːʃ"

def test_h_prothesis_only_before_vowels():
    assert ipa(apply_mutation(w("iːʃ"), "HPREF", IRISH, TABLE)) == "hiːʃ"
    assert ipa(apply_mutation(w("kaː"), "HPREF", IRISH, TABLE)) == "kaː"

def test_t_prefixation_replaces_s_lenition_after_the_article():
    assert ipa(apply_mutation(w("ʃiːnʲ"), "TPREF", IRISH, TABLE)) == "tʲiːnʲ"   # an tSín

def test_genitive_of_mac_is_mic():
    assert ipa(apply_inflection(w("mˠak"), "GEN_M1", IRISH, TABLE)) == "mʲɪc"

def test_gen_ach_marcach_to_marcaigh():
    assert ipa(apply_inflection(w("mˠaɾˠkəx"), "GEN_ACH", IRISH, TABLE)) == "mˠaɾˠkəj"

def test_gen_f2_brog_to_broige():
    assert ipa(apply_inflection(w("bˠɾˠoːɡ"), "GEN_F2", IRISH, TABLE)).endswith("ə")

def test_all_five_inflections_exist():
    assert set(IRISH.inflect) == {"GEN_M1", "GEN_ACH", "GEN_F2", "GEN_M3", "VOC_M1"}   # R25

def test_the_47_mutation_tagged_rows_apply_without_error():
    """R22: test-words.tsv tags mutations as `mut:` in the `features` column — 47 rows.
    (The 85 `len:` rows are a VOWEL LENGTH tag and are not mutation data.)"""
    rows = mutation_rows()
    assert len(rows) == 47
    for row in rows:
        apply_mutation(w(row["ipa"]), "LEN", IRISH, TABLE)      # must not raise
```

- [ ] **Steps 2–4: fail, write `irish.rules` + `irish.py`, pass.**
- [ ] **Step 5: Commit** —
  `feat(rules): irish.rules mutation and inflection tables (digest §3.1-§3.5)`

**Note on *a Sheáin*:** the attested vocative /çaːnʲ/ needs lenition (`ʃ → h`) **and** the
`h → ç / #_[V +back]` allophony rule, which belongs to `[normalize]` (Task 19), **and**
slenderization. It is therefore tested in Task 19, not here. Do not bend the lenition table to
produce `ç` directly.

---

## Task 19: Irish `[normalize]`

**Depends on:** Task 17 (same file — spec §12.I/GPT finding 2 fix the order 17 → 19 → 18)

**Files:** modify `rules/irish.rules` (add `[normalize]`), `src/strands/irish.py`; create
`tests/test_irish_normalize.py`.

**Interfaces:**

```python
def normalize(word: Word, rf: RuleFile, table: FeatureTable, *, dialect: str = "C") -> Word
    """Spec §4.1: fold input aliases; give every quality-unmarked consonant ʲ or ˠ from
    the adjacent-vowel convention; mark Connacht initial stress; leave user-supplied
    phonemes untouched."""
```

Rule content, with the citations split as R23 requires:

```
[normalize]
lˠ  -> l̪ˠ           %design # input alias, digest §1.1 lines 130-141 [wiki-help-ipa-irish note 5]
l̠ʲ  -> lʲ           %design # ditto, note 5
nˠ  -> n̪ˠ           %design # ditto, note 6
n̠ʲ  -> nʲ           %design # ditto, note 6
g   -> ɡ            %design # ASCII duplicate, tooling only (I-34)
ɑ   -> a            %design # user transcription only, digest line 27 — NOT a digest §1.1 claim
ɑː  -> aː           %design # ditto, line 27
h -> ç / # _ [V +back]      %attested # [wiki-irish-phonology §Allophones], digest §1.1
[C -front -back] -> [+front -back] / _ [V +front]   %attested # caol le caol, digest §5.1
[C -front -back] -> [+back -front] / _ [V +back]    %attested # leathan le leathan, digest §5.1
[C -front -back] -> [+front -back] / [V +front] _ # %attested # final C takes the preceding V
[C -front -back] -> [+back -front] / [V +back] _ #  %attested
```

Connacht initial stress is **not** a rewrite rule: `normalize()` sets `word.stress = 0` when
`dialect == "C"` and the input carried no mark, appending a trace entry `stress:irish-initial`
(digest §4.1). `dialect == "M"`/`"U"` rows pass through unstressed (spec §9 row 19).

- [ ] **Step 1: Failing test**

```python
def test_aliases_fold_to_the_two_way_system():
    assert normalize(w("lˠa"), IRISH, TABLE).segments == ("l̪ˠ", "a")
    assert normalize(w("gl̪ˠuːnʲ"), IRISH, TABLE).segments[0] == "ɡ"

def test_alpha_folds_to_a():
    assert normalize(w("l̪ˠɑsˠ"), IRISH, TABLE).segments == ("l̪ˠ", "a", "sˠ")

def test_unmarked_consonant_takes_the_following_vowels_quality():
    assert normalize(w("ti"), IRISH, TABLE).segments[0] == "tʲ"
    assert normalize(w("tu"), IRISH, TABLE).segments[0] == "t̪ˠ"

def test_final_unmarked_consonant_takes_the_preceding_vowels_quality():
    assert normalize(w("it"), IRISH, TABLE).segments[-1] == "tʲ"

def test_user_supplied_quality_is_never_overwritten():
    assert normalize(w("t̪ˠiː"), IRISH, TABLE).segments[0] == "t̪ˠ"

def test_vocative_of_sean_composes_to_a_sheain():
    """digest §3.5: /ʃaːnˠ/ -> LEN -> /haːnˠ/ -> [ç] before a back vowel -> VOC_M1."""
    x = apply_mutation(w("ʃaːnˠ"), "LEN", IRISH, TABLE)
    x = normalize(x, IRISH, TABLE)
    x = apply_inflection(x, "VOC_M1", IRISH, TABLE)
    assert x.ipa(marks=False) == "çaːnʲ"

def test_connacht_gets_initial_stress_when_unmarked():
    assert normalize(w("mˠat̪ˠaːnˠəx"), IRISH, TABLE, dialect="C").stress == 0

def test_an_explicit_mark_is_preserved():
    assert normalize(w("əˈwaːnʲ"), IRISH, TABLE, dialect="C").stress == 1

def test_munster_rows_pass_through_unstressed():
    assert normalize(w("kalʲiːnʲ"), IRISH, TABLE, dialect="M").stress is None

def test_every_test_word_normalizes_without_error():
    for row in read_test_words():
        normalize(w(row["ipa"]), IRISH, TABLE, dialect=row.get("dialect") or "C")
```

- [ ] **Steps 2–4. Step 5: Commit** — `feat(rules): irish.rules normalization pre-pass`

---

## Task 20: Input TSV, inference (gender, declension, gen_ipa), `lint`

**Depends on:** Tasks 4, 17 (`infer()` calls `apply_inflection`, so slenderization has exactly one
implementation — R27)

**Files:** create `src/strands/inputs.py`, `tests/fixtures/input-sample.tsv`,
`tests/test_inputs.py`.

**Interfaces:**

```python
INPUT_COLUMNS = ("orthography", "ipa", "dialect", "gloss", "category",
                 "gender", "gen_ipa", "pl_ipa", "note")

@dataclass(frozen=True)
class Entry:
    orthography: str
    ipa: str = ""
    dialect: str = "C"
    gloss: str = ""
    category: str = ""
    gender: str = "m"
    declension: str = "m1"          # m1 | ach | f2 | m3 | d4   (I-38)
    gen_ipa: str = ""
    pl_ipa: str = ""
    note: str = ""
    assumptions: tuple[str, ...] = ()

def read_input(path) -> list[Entry]
    """Header must contain `orthography`; unknown columns (e.g. test-words.tsv's
    `features`) are ignored; missing ones default. A row with no `ipa` returns
    ipa='' and assumption 'skipped:no-ipa'."""
def infer(entry: Entry, irish: RuleFile, table: FeatureTable) -> Entry
def lint_report(entries: Sequence[Entry]) -> list[str]
def accept_guesses(path, entries: Sequence[Entry]) -> None
```

Inference, in order (spec §5 + spec §12.H):
1. `dialect` empty → `C`, tag `dialect:default-C`.
2. `gender` empty → known-name list (built from `test-words.tsv` glosses stating a gender), then
   endings (`-óg -eog` or a final slender consonant → `f`; `-ach -án -ín` → `m`), else `m`; tag
   `gender:known-name` / `gender:ending` / `gender:default-m`.
3. **`declension`** (I-38, R24) → `-ach` final → `ach`; masculine + broad final C → `m1`;
   feminine + final C → `f2`; `-óir -eoir -úil` → `m3`; vowel-final or `-ín` → `d4`; tag
   `declension:inferred-<rule>`.
4. `gen_ipa` empty → `apply_inflection(word, GEN_<declension>)`, tag `gen_ipa:inferred-<decl>`.
   `d4` returns the stem unchanged.
5. A construction whose slot is absent is **skipped with a note**, never an error.

- [ ] **Step 1: Write the fixture** — `tests/fixtures/input-sample.tsv`, 7 rows with the spec §5
  header, covering: a complete row; `NoIpa` (no `ipa`); no `gender`; no `gen_ipa`; a vowel-final
  name; an `-ach` epithet; an `-óir` agent noun.

- [ ] **Step 2: Write the failing tests**

```python
def test_reads_all_nine_columns():
    assert read_input(FIX)[0].orthography and read_input(FIX)[0].gloss

def test_row_without_ipa_is_flagged_not_dropped():
    e = [x for x in read_input(FIX) if x.orthography == "NoIpa"][0]
    assert e.ipa == "" and "skipped:no-ipa" in e.assumptions

def test_unknown_columns_are_ignored():
    """test-words.tsv has `features`, not the spec §5 header."""
    entries = read_input(ROOT / "sources" / "irish" / "test-words.tsv")
    assert len(entries) == 144

def test_missing_dialect_defaults_to_C():
    assert infer(Entry("x", ipa="kaː", dialect=""), IRISH, TABLE).dialect == "C"

def test_gender_from_ending_and_default():
    assert infer(Entry("Bríd", ipa="bʲɾʲiːdʲ", gender=""), IRISH, TABLE).gender == "f"
    e = infer(Entry("Zzz", ipa="t̪ˠaːk", gender=""), IRISH, TABLE)
    assert e.gender == "m" and "gender:default-m" in e.assumptions

def test_declension_is_inferred_and_tagged():
    """R24 / spec §12.H — without this, --construction all silently defaults to m1."""
    assert infer(Entry("marcach", ipa="mˠaɾˠkəx"), IRISH, TABLE).declension == "ach"
    assert infer(Entry("mac", ipa="mˠak", gender="m"), IRISH, TABLE).declension == "m1"
    assert infer(Entry("bróg", ipa="bˠɾˠoːɡ", gender="f"), IRISH, TABLE).declension == "f2"
    assert infer(Entry("bádóir", ipa="bˠaːd̪ˠoːɾʲ"), IRISH, TABLE).declension == "m3"
    assert infer(Entry("balla", ipa="bˠal̪ˠə"), IRISH, TABLE).declension == "d4"
    assert any(a.startswith("declension:") for a in
               infer(Entry("marcach", ipa="mˠaɾˠkəx"), IRISH, TABLE).assumptions)

def test_gen_ipa_uses_the_inflection_tables_not_a_second_implementation():
    e = infer(Entry("mac", ipa="mˠak", gender="m", gen_ipa=""), IRISH, TABLE)
    assert e.gen_ipa == "mʲɪc" and "gen_ipa:inferred-m1" in e.assumptions

def test_vowel_final_gen_ipa_is_unchanged():
    assert infer(Entry("balla", ipa="bˠal̪ˠə", gen_ipa=""), IRISH, TABLE).gen_ipa == "bˠal̪ˠə"

def test_supplied_fields_are_never_overwritten():
    e = infer(Entry("x", ipa="kaː", gender="f", declension="d4", gen_ipa="kaː"), IRISH, TABLE)
    assert e.gender == "f" and e.declension == "d4" and e.assumptions == ()

def test_lint_report_lists_one_line_per_guess():
    lines = lint_report([infer(x, IRISH, TABLE) for x in read_input(FIX)])
    assert any("declension" in l for l in lines) and all(l.strip() for l in lines)

def test_accept_writes_the_guesses_back(tmp_path):
    dst = tmp_path / "in.tsv"; shutil.copy(FIX, dst)
    accept_guesses(dst, [infer(x, IRISH, TABLE) for x in read_input(dst)])
    rows = list(csv.DictReader(dst.open(encoding="utf-8"), delimiter="\t"))
    assert all(r["gender"] for r in rows)
```

- [ ] **Steps 3–5. Step 6: Commit** —
  `feat(strands): input reader with gender, declension and genitive inference`

---

## Task 18: Irish templates

**Depends on:** Tasks 19, 20

**Files:** modify `rules/irish.rules` (add `[templates]`), `src/strands/irish.py`; create
`tests/test_irish_templates.py`.

**Interfaces:**

```python
def build_construction(name: str, slots: dict[str, Entry], rf: RuleFile,
                       table: FeatureTable) -> list[Word]
    """Apply rf.templates[name]; one Word per space-separated word (I-16).
    Raises MissingSlot when a required slot is absent."""
class MissingSlot(IrishError): ...
```

`[templates]` content — the eight from spec §3, with IPA literals (orthography in the comment):

```
[templates]
VOC      = "ə" LEN(NAME) VOC_M1?        # a + lenited name; VOC_M1 only if declension m1
GEN      = GEN(NAME)
PATRO_O  = "oː" GEN(FATHER)             # Ó
PATRO_NI = "nʲiː" LEN(GEN(FATHER))      # Ní
ADJ      = NAME " " LEN_IF_F(ADJ)
OF       = NAME " " ART(GEN(NOUN))
COMPOUND = FIRST LEN(SECOND)
DESC     = NOUN
```

Function semantics in `irish.py`:
- `LEN/ECL/HPREF/TPREF(x)` → `apply_mutation`.
- `GEN(x)` → dispatch on `x.declension` (I-38): `m1→GEN_M1`, `ach→GEN_ACH`, `f2→GEN_F2`,
  `m3→GEN_M3`, `d4→` identity. Missing declension → `GEN_M1` plus an `assumptions` note.
- `VOC_M1?` (bare function + `?`, I-16/R1) → applied only when the head's `declension == "m1"`.
- `LEN_IF_F(x)` → lenite iff the head noun's `gender == "f"` (digest §3.6).
- `ART(x)` → article segments (`ə n̪ˠ` / `ə nʲ`) + its mutation: masculine genitive and feminine
  nominative lenite; a following coronal blocks lenition; `s` takes `TPREF` (digest §3.4).
- Every join inserts `$`; `" "` splits into separately-adapted words.

- [ ] **Step 1: Failing test**

```python
def entry(ipa, **kw): return Entry(orthography="x", ipa=ipa, **kw)

def test_voc_of_a_first_declension_masculine_name():
    words = build_construction("VOC", {"NAME": entry("ʃaːnˠ", declension="m1")}, IRISH, TABLE)
    assert len(words) == 1 and words[0].ipa(marks=False) == "əçaːnʲ"      # a Sheáin

def test_voc_outside_m1_skips_slenderization():
    words = build_construction("VOC", {"NAME": entry("bʲɾʲiːdʲ", declension="f2")}, IRISH, TABLE)
    assert words[0].ipa(marks=False).startswith("əvʲ")                    # a Bhríd

def test_joins_insert_morpheme_boundaries():
    words = build_construction("VOC", {"NAME": entry("ʃaːnˠ", declension="m1")}, IRISH, TABLE)
    assert words[0].morphemes

def test_space_literal_splits_into_separate_words():
    words = build_construction("ADJ", {"NAME": entry("mˠaːɾʲə", gender="f"),
                                       "ADJ": entry("bˠaːnˠ")}, IRISH, TABLE)
    assert len(words) == 2 and words[1].ipa(marks=False).startswith("w")   # Máire Bhán

def test_len_if_f_does_not_lenite_after_a_masculine_noun():
    words = build_construction("ADJ", {"NAME": entry("pˠaːd̪ˠɾˠəɟ", gender="m"),
                                       "ADJ": entry("ɾˠuə")}, IRISH, TABLE)
    assert words[1].ipa(marks=False).startswith("ɾˠ")                      # Pádraig Rua

def test_patro_ni_lenites_the_genitive_father():
    words = build_construction("PATRO_NI", {"FATHER": entry("kaːnˠ", declension="m1")},
                               IRISH, TABLE)
    assert words[0].ipa(marks=False).startswith("nʲiː")

def test_compound_lenites_the_second_element():
    words = build_construction("COMPOUND", {"FIRST": entry("l̪ˠasˠəɾʲ"), "SECOND": entry("kosˠ")},
                               IRISH, TABLE)
    assert words[0].ipa(marks=False) == "l̪ˠasˠəɾʲxosˠ"        # Lasairchos, digest §3.6

def test_gen_dispatches_on_the_inferred_declension():
    words = build_construction("GEN", {"NAME": entry("mˠaɾˠkəx", declension="ach")}, IRISH, TABLE)
    assert words[0].ipa(marks=False).endswith("j")

def test_missing_slot_raises():
    with pytest.raises(MissingSlot):
        build_construction("PATRO_O", {}, IRISH, TABLE)

def test_all_eight_templates_exist():
    assert set(IRISH.templates) == {"VOC", "GEN", "PATRO_O", "PATRO_NI", "ADJ", "OF",
                                    "COMPOUND", "DESC"}
```

- [ ] **Steps 2–4. Step 5: Commit** — `feat(rules): irish.rules construction templates`

**Acceptance:** milestone 5 complete (Tasks 17, 19, 20, 18).

---

## Task 21: Pipeline, respell, epithet slots

**Depends on:** Tasks 9, 11, 13, 14, 15, 16, 18, 19, 20

**Files:** create `src/strands/respell.py`, `src/strands/pipeline.py`,
`tests/fixtures/toy-target.rules`, `tests/test_pipeline.py`.

**Interfaces:**

```python
def respell(word: Word, rf: RuleFile, table: FeatureTable, *, mark_stress: bool = True) -> str
    """Spec §12.C: apply rf.sections['respell'] over the ANNOTATED TOKEN STREAM.
    A quoted replacement becomes an opaque chunk that later rules never rematch;
    unmatched segments pass through as themselves. After the rules, marks are stripped
    IN CODE (no DSL cleanup lines — I-8); `mark_stress=False` (Georgian's
    `[stress] mark = off`) drops the stress mark too."""

EPITHET_SLOTS = ("ADJ", "NOUN")      # I-39 / spec §12.H

def resolve_epithet(target: RuleFile, slot: str) -> str | None
    """target.meta may declare `epithet-ADJ = NISBA` / `epithet-NOUN = FEM_A`.
    Returns the [epithets] key, or None when the target maps nothing to that slot
    (which means 'no affix', not an error)."""
def affix_epithet(word: Word, name: str, rf: RuleFile, table: FeatureTable) -> Word

@dataclass(frozen=True)
class Result:
    respelling: str
    ipa: str
    flags: tuple[str, ...]
    fallbacks: int
    assumptions: tuple[str, ...]
    trace: tuple[TraceEntry, ...]
    words: tuple[Word, ...]

def adapt(words: Sequence[Word], target: RuleFile, table: FeatureTable,
          *, epithet: str | None = None) -> Result
    """Spec §4 stages 2-7: substitute_stage -> syllabify -> repair -> assign_stress ->
    post_stress -> (epithet: affix then re-run syllabify/repair/stress/post-stress) ->
    respell."""
def parse_construction(tag: str) -> tuple[str, str | None]
    """'DESC+ADJ' -> ('DESC', 'ADJ'); 'VOC' -> ('VOC', None) (I-39)."""
def run_entry(entry: Entry, construction: str, irish: RuleFile, target: RuleFile,
              table: FeatureTable, slots: dict[str, Entry] | None = None) -> Result
    """Stage 1 (normalize + template) then adapt(), passing the resolved epithet."""
def load_target(name: str, table: FeatureTable) -> RuleFile
TARGETS = ("welsh", "arabic-egy", "georgian", "dutch")
CONSTRUCTIONS = ("VOC", "GEN", "PATRO_O", "PATRO_NI", "ADJ", "OF", "COMPOUND", "DESC",
                 "DESC+ADJ", "DESC+NOUN")
```

- [ ] **Step 1: Write `tests/fixtures/toy-target.rules`** — a complete, ~40-line target file with
  every section, an `[epithets]` block containing `NISBA`, and `[meta] epithet-ADJ = NISBA`. It is
  the pipeline's test double so Task 21 can be finished and reviewed before any real target exists.

- [ ] **Step 2: Write the failing tests**

```python
def test_stage_order_in_the_trace():
    r = adapt([w("pˠaːd̪ˠɾˠəɟ")], TOY, TABLE)
    seen = [t.stage for t in r.trace]
    order = ["substitute", "syllabify", "repair", "stress", "post-stress", "respell"]
    idx = [order.index(s) for s in seen if s in order]
    assert idx == sorted(idx)

def test_result_fields():
    r = adapt([w("pˠaːd̪ˠɾˠəɟ")], TOY, TABLE)
    assert r.ipa and r.respelling and isinstance(r.flags, tuple) and r.fallbacks >= 0

def test_multiword_constructions_are_adapted_separately_and_rejoined():
    r = adapt([w("mˠaːɾʲə"), w("bˠaːnˠ")], TOY, TABLE)
    assert " " in r.respelling and " " in r.ipa

def test_respell_chunks_are_opaque():
    """§12.C: a rule that outputs "sh" must not be rematched by a later s- rule."""
    rf = parse_rules('[inventory]\nʃ s a\n[respell]\nʃ -> "sh"\ns -> "z"\n', TABLE)
    assert respell(Word(segments=("ʃ", "a")), rf, TABLE) == "sha"

def test_respell_strips_marks_in_code():
    rf = parse_rules('[inventory]\np a\n[respell]\np -> "b"\n', TABLE)
    out = respell(Word(segments=("p", "a"), syllables=(0,), stress=0), rf, TABLE)
    assert "." not in out and out.startswith("ˈ") or out == "ba"

def test_respell_can_suppress_the_stress_mark():
    rf = parse_rules('[inventory]\np a\n[respell]\np -> "b"\n', TABLE)
    assert "ˈ" not in respell(Word(segments=("p", "a"), syllables=(0,), stress=0), rf, TABLE,
                              mark_stress=False)

def test_unmatched_segments_pass_through():
    rf = parse_rules('[inventory]\np a\n[respell]\np -> "b"\n', TABLE)
    assert respell(Word(segments=("p", "a")), rf, TABLE) == "ba"

def test_parse_construction_splits_epithet_slots():
    assert parse_construction("DESC+ADJ") == ("DESC", "ADJ")
    assert parse_construction("VOC") == ("VOC", None)

def test_epithet_slot_resolves_through_target_meta():
    assert resolve_epithet(TOY, "ADJ") == "NISBA"
    assert resolve_epithet(TOY, "NOUN") is None          # unmapped = no affix, not an error

def test_epithet_affixation_reruns_syllabification_and_stress():
    plain = adapt([w("kaː")], TOY, TABLE)
    affixed = adapt([w("kaː")], TOY, TABLE, epithet="NISBA")
    assert affixed.ipa != plain.ipa and affixed.ipa.rstrip().endswith("i")

def test_run_entry_applies_the_irish_prepass_then_the_target():
    r = run_entry(Entry("Seán", ipa="ʃaːnˠ", declension="m1"), "VOC", IRISH, TOY, TABLE)
    assert any(t.stage in {"mutation", "normalize", "irish"} for t in r.trace)

def test_run_entry_with_an_unmapped_epithet_slot_is_not_an_error():
    r = run_entry(Entry("cos", ipa="kosˠ"), "DESC+NOUN", IRISH, TOY, TABLE)
    assert r.ipa

def test_every_output_segment_is_in_the_target_inventory():
    r = adapt([w("ˈl̪ˠasˠəɾʲxosˠ")], TOY, TABLE)
    for word in r.words:
        assert set(word.segments) <= set(TOY.inventory)

def test_pipeline_is_deterministic():
    assert adapt([w("pˠaːd̪ˠɾˠəɟ")], TOY, TABLE) == adapt([w("pˠaːd̪ˠɾˠəɟ")], TOY, TABLE)

def test_unknown_target_name_raises():
    with pytest.raises(Exception):
        load_target("klingon", TABLE)
```

- [ ] **Steps 3–5. Step 6: Commit** —
  `feat(strands): stage pipeline, token-stream respell, epithet slots`

---

## Task 22: Regression harness — Modes E and C

**Depends on:** Task 21

**Files:** create `src/strands/regress.py`, `tests/test_regression_harness.py`,
`tests/ratchets/` (empty directory with a `.gitkeep`).

**Read I-25 and I-36 before starting.**

**Interfaces:**

```python
@dataclass(frozen=True)
class RegressionRow:
    source_form: str
    source_ipa: str
    target_form: str
    target_ipa: str
    provenance: str
    mode: str          # "E" | "C" | "skip" | "error"
    passed: bool
    got: str
    distance: int
    reason: str = ""   # for mode="error": the untokenizable substring

@dataclass(frozen=True)
class RegressionReport:
    target: str
    rows: tuple[RegressionRow, ...]
    def counts(self) -> dict[str, int]        # by mode
    def rate(self, mode: str) -> float        # passed / (rows in that mode)
    def summary(self) -> str

def read_attested(target: str) -> list[dict[str, str]]
    """Drops rows whose `note` starts with 'PREDICTED-NOT-ATTESTED:'."""
def run_regression(target: str, table: FeatureTable,
                   rule_file: Path | None = None) -> RegressionReport
    """`rule_file` overrides rules/<target>.rules so the harness can be tested against
    the toy fixture before any real target file exists (R28)."""
def load_ratchet(target: str) -> dict[str, float]
def assert_ratchet(report: RegressionReport, tolerance: float = 0.0) -> None
def write_ratchet(report: RegressionReport) -> None     # run by hand, never by a test
```

**Mode C is inventory/syllable/stress conformance only** (I-25, GPT finding 4) — the docstring must
say so, and the summary line must print it, so nobody reads a Mode C rate as evidence that
substitution or repair is right. Those live in the per-target repair tables (I-27).

- [ ] **Step 1: Failing test**

```python
import pytest
from helpers import TABLE, FIXTURES, rules_exist
from strands.regress import read_attested, run_regression, assert_ratchet, RegressionReport

def test_row_counts_match_the_committed_data():
    """R10: draft 1 had three of four denominators wrong."""
    assert len(read_attested("georgian")) == 143
    assert len(read_attested("arabic-egy")) == 301        # 312 - 11 PREDICTED-NOT-ATTESTED
    assert len(read_attested("welsh")) == 751
    assert len(read_attested("dutch")) == 90

def test_target_ipa_denominators():
    def n(t): return len([r for r in read_attested(t) if r["target_ipa"].strip()])
    assert n("georgian") == 122 and n("arabic-egy") == 279
    assert n("welsh") == 19 and n("dutch") == 67

def test_mode_e_is_dutch_only():
    def both(t): return len([r for r in read_attested(t)
                             if r["source_ipa"].strip() and r["target_ipa"].strip()])
    assert both("dutch") == 32
    assert both("georgian") == both("arabic-egy") == both("welsh") == 0

def test_predicted_rows_are_dropped():
    assert not any(r["note"].startswith("PREDICTED-NOT-ATTESTED")
                   for r in read_attested("arabic-egy"))

def test_untokenizable_rows_go_to_the_error_bucket_not_an_exception():
    """I-24/I-36: a SegmentError in attested data is counted, never raised."""
    rep = run_regression("georgian", TABLE, rule_file=FIXTURES / "toy-target.rules")
    assert "error" in rep.counts()
    assert rep.counts()["error"] >= 0

def test_cleaning_pass_rescues_ascii_spellings():
    rep = run_regression("dutch", TABLE, rule_file=FIXTURES / "toy-target.rules")
    assert rep.counts().get("error", 0) < 30      # draft-1 measurement: 30/67 before cleaning

def test_rate_is_a_fraction_of_rows_in_that_mode():
    rep = run_regression("dutch", TABLE, rule_file=FIXTURES / "toy-target.rules")
    assert 0.0 <= rep.rate("C") <= 1.0

def test_summary_names_mode_c_as_conformance_only():
    rep = run_regression("dutch", TABLE, rule_file=FIXTURES / "toy-target.rules")
    assert "conformance" in rep.summary().lower()

def test_ratchet_failure_is_loud(tmp_path, monkeypatch):
    rep = RegressionReport(target="x", rows=(FAILING_ROW,))
    monkeypatch.setattr("strands.regress.load_ratchet", lambda t: {"C": 1.0})
    with pytest.raises(AssertionError):
        assert_ratchet(rep)

def test_edit_distance_is_reported():
    from strands.regress import edit_distance
    assert edit_distance(("k", "a", "l", "b"), ("k", "a", "l", "p")) == 1

@pytest.mark.skipif(not rules_exist("dutch"), reason="dutch.rules lands in Task 26")
def test_real_rule_file_runs():
    assert run_regression("dutch", TABLE).counts()
```

*(Build `FAILING_ROW` inline in the test as a `RegressionRow(..., mode="C", passed=False, ...)`.)*

- [ ] **Steps 2–4. Step 5: Commit** —
  `feat(strands): attested-data regression harness with cleaning, error bucket and ratchet`

**Acceptance:** the denominators above are reproduced exactly; the harness never raises on
attested data; it runs against the toy fixture with no real rule file present.

---

## Tasks 23a–26: the target rule files

Tasks 23a, 24, 25 and 26 are **mutually independent** and run in parallel once Tasks 21 and 22 are
committed; 23b follows 23a. They share the shape below, stated once.

**Method — test-first, per spec §12.I** (this ordering is mandatory; draft 1 had it backwards,
GPT finding 10):
1. **Write the task's tests first**, against an absent or skeletal `rules/<target>.rules`. Run
   them; they must fail (`FileNotFoundError` or assertion).
2. Read the named digest sections and transcribe them into rule lines, each with its citation.
3. `uv run strands check rules/<target>.rules` — no `error`-severity findings.
4. Run the tests until green, then the regression harness; record the measured Mode C (and, for
   Dutch, Mode E) rates in `tests/ratchets/<target>.json` **after** the bar is met.
5. Commit rule file + tests + ratchet together.

**Tagging discipline** (spec §12.G, I-28, I-29): a rule whose digest section states the opposite,
or explicitly leaves the question open, is `%design` with a `# contra digest §N line L` or
`# design: digest §N line L open` comment. `%attested` means the digest asserts it.

**Common tests every target task includes:**

```python
TARGET = target("<name>")

def test_rule_file_parses_and_checks_clean():
    errs = [e for e in check_rule_file(TARGET, TABLE) if e.severity == "error"]
    assert errs == [], errs

def test_every_rule_line_carries_a_citation():
    for section in TARGET.sections.values():
        for r in section:
            assert r.comment.strip(), r.rule_id
            assert ("[" in r.comment or "design:" in r.comment or "digest §" in r.comment), \
                (r.rule_id, r.comment)

def test_mutation_output_segments_all_survive():
    """User decision 2: word-initial /w x ɣ ç j h ŋ ɲ/ and mutation-onset clusters."""
    for seg in "w x ɣ ç j h ŋ ɲ".split():
        r = adapt([w(seg + "aː")], TARGET, TABLE)
        assert set(r.words[0].segments) <= set(TARGET.inventory)
        assert "UNREPAIRED" not in r.flags

def test_no_unrepaired_on_the_144_word_set():
    bad = [row["orthography"] for row in read_test_words()
           if "UNREPAIRED" in run_entry(entry_of(row), "DESC", IRISH, TARGET, TABLE).flags]
    assert set(bad) <= read_allow_file_for("<name>"), sorted(bad)

def test_repair_table():           # I-27 — the per-target table below
    ...

def test_regression_meets_the_bar():
    rep = run_regression("<name>", TABLE)
    assert rep.rate("C") >= <bar>, rep.summary()

def test_error_bucket_is_small():
    rep = run_regression("<name>", TABLE)
    assert rep.counts().get("error", 0) <= <cap>, rep.summary()

def test_ratchet_does_not_slip():
    assert_ratchet(run_regression("<name>", TABLE))
```

---

### Task 23a: `georgian.rules` — inventory, substitute, stress, epithets, respell

**Depends on:** 21, 22. **Digest:** `sources/georgian/digest.md`. Split from 23b per R29.

| Rule block | Source, and the tag it must carry |
|---|---|
| `[inventory]` | §1.1 chart [shosted2006 p.255], §1.2–§1.8 deltas, §1.9 net delta vs PHOIBLE 2183. `tʃʰ` comes from the Task 1b hand rows |
| `[classes]` | the `BROAD`/`SLEN` pair of I-41 |
| `/p t k/ → pʰ tʰ kʰ` | §3.1 — `%design`, `# design: §9.4` |
| `[STOP -voice] -> [+ejective] / C _` | **`%design`, `# design: §9.4 · contra digest §3.1 line 825`** — R11: §3.1 explicitly rejects turning the 84.1%/26.5% split into a categorical environment rule, and recommends unconditional ejective. Spec §9 row 4 fixes our default; the digest is evidence, not authority. Name the test accordingly |
| `f → pʰ` | §3.2 — `%attested` |
| `ŋ → n` | §3.2 gives `/ng/`; spec §7 fixes `n`. `%design`, `# design: §7 · contra digest §3.2` |
| `w → v` | §3.3 — `%design`, `# design: §9.6`. **Carry the digest's warning in the comment** (S6): §3.3's own (unattested, overlay) recommendation is positional, /w/→/u/ word-initially, and Irish /w/ arrives word-initially from lenited b/m |
| slender coronals → `ʃ ʒ tʃʰ dʒ` | **`%design`, `# design: digest §8.1 line 1413 open`** — R12: §8.1 lists four options and decides none; §8.2 offers `tʰ tʼ d` *or* `tʃʰ tʃʼ dʒ` "(unattested for Georgian)"; `ʃ ʒ` as outputs appear nowhere |
| Cʷ: `0 -> v / [C +back -labial] _ [V +front]` | I-31 (epenthesis form, R2). `%design`, `# design: goals decision 5 (2026-08-25)`. The "before /i e/, onsets only" restriction is **ours** — §8.1 Option C is unconditional (R13a), so do not cite §8.1 for the restriction |
| slender C before back V: `0 -> i / [C +front] _ [V +back]` | §8.1 Option C — `%design`, `# design: §9.2` |
| long → short; `nuclei` empty (hiatus) | §3.4, §8.3 — `%attested` |
| `[stress] procedure = initial`, `mark = off` | §4.1, §4.3 — `%attested` |
| `[epithets]` `NOM_I` (+i), `URI` (-uri/-uli), `ELI` (-eli), syncope before `-eb-` | §6.1, §6.2, §6.4. **Also add `SHVILI` and `DZE`** (S7): §6.3 lines 1301–1326 calls the patronymics "the readiest epithet machinery in the language", and `PATRO_O`/`PATRO_NI` are core constructions |
| `[meta] epithet-ADJ = URI`, `epithet-NOUN = NOM_I` | I-39 / spec §12.H |
| `[respell]` national 2002 + overlays | §5.1 (33-letter table) and §5.3's **actual** D1–D5 (lines 1197–1230): `x`, `tch`, `y`, bare stem, and **apostrophe placement unchanged** ("Not an overlay — follow the standard"). R13b: draft 1 dropped D5 and invented a "`ch`" deviation — `ch` is the unmodified native digraph |

- [ ] **Step 1: Write the tests first** (they fail: no `georgian.rules`)

```python
def test_irish_p_t_k_are_aspirated_by_default_per_decision_9_4():
    """Named for the decision, not for a digest fact — R11."""
    assert adapt([w("pˠaː")], TARGET, TABLE).words[0].segments[0] == "pʰ"

def test_post_consonantal_stops_are_ejective_per_decision_9_4():
    out = adapt([w("sˠkaː")], TARGET, TABLE).words[0].segments
    assert "kʼ" in out

def test_f_becomes_aspirated_p():
    assert "pʰ" in adapt([w("fˠaː")], TARGET, TABLE).words[0].segments

def test_broad_nonlabial_before_a_front_vowel_gets_v():      # Cʷ, decision 5
    out = adapt([w("kiː")], TARGET, TABLE).words[0].segments
    assert out[1] == "v"

def test_slender_consonant_before_a_back_vowel_gets_i():
    assert "i" in adapt([w("tʲuː")], TARGET, TABLE).words[0].segments

def test_vv_degeminates():
    """decision 5: /vv/ from collision with lenited b/m degeminates."""
    out = adapt([w("wiː")], TARGET, TABLE).words[0].segments
    assert out.count("v") <= 1

def test_diphthongs_become_hiatus():
    """§12.B: Georgian declares no `nuclei`, so /iə/ is two syllables."""
    assert len(adapt([w("ciəɾˠə")], TARGET, TABLE).words[0].syllables) >= 3

def test_stress_is_initial_and_unmarked_in_the_respelling():
    r = adapt([w("mˠat̪ˠaːnˠəx")], TARGET, TABLE)
    assert r.words[0].stress == 0 and "ˈ" not in r.respelling      # §4.3, mark = off

def test_personal_names_are_emitted_as_a_bare_stem():
    assert not adapt([w("kaːnˠ")], TARGET, TABLE).respelling.endswith("i")

def test_common_noun_epithets_keep_the_nominative_i():
    r = run_entry(Entry("cos", ipa="kosˠ"), "DESC+NOUN", IRISH, TARGET, TABLE)
    assert r.respelling.endswith("i")

def test_respelling_follows_the_five_5_3_deviations():
    """D1 x, D2 tch, D3 y, D4 bare stem, D5 apostrophe placement UNCHANGED (R13b)."""
    assert "x" in adapt([w("xaː")], TARGET, TABLE).respelling
    assert "tch" in adapt([w("tʲuː")], TARGET, TABLE).respelling or True   # see note
    ej = adapt([w("sˠkaː")], TARGET, TABLE).respelling
    assert "'" in ej and ej.index("'") == ej.index("k") + 1   # apostrophe AFTER the letter

def test_kasqueil_is_spelled_the_standard_way():
    """R13b: under D5 the existing name *Kas'queil* is respelled *Kasq'ueil*.
    This is a known, accepted divergence from the pre-existing name list; assert the
    engine's form so the divergence is visible rather than silent."""
    ...
```

*(Replace the `or True` in the `tch` assertion with the real expectation once the respell table is
written — a test that cannot fail is a failed test, S2.)*

- [ ] **Steps 2–5** per the common method. **Commit:**
  `feat(rules): georgian.rules core — inventory, substitute, stress, epithets, respell`

---

### Task 23b: `georgian.rules` — syllable whitelists, bans, repair

**Depends on:** Task 23a

**Files:** modify `rules/georgian.rules`; create `rules/extract_georgian_clusters.py`,
`tests/test_rules_georgian_syllable.py`, `tests/ratchets/georgian.json`.

**Why this is its own task (R29):** the whitelists are a prose-extraction job, not a table copy.
Appendix 2 (digest lines 324–421) holds ~150 two-member, ~60 three-member, ~21 four-member, 1
five-member and 2 six-member stem-initial sequences, written as `cluster *example* 'gloss'` prose;
Appendix 3 (lines 468–525) adds ~48 CC plus ~25 longer stem-final sequences. **Commit the
extraction script beside the rule file** so the transcription is reproducible and reviewable.

| Rule block | Source |
|---|---|
| `template = any`, `domain = stem`, `sonority = off` | §2.1 (the syllable is not the domain), §2.7 (sonority does not govern Georgian clusters) — I-13, I-27 |
| `nuclei` — **absent** | §2.9; produces the attested hiatus (spec §12.B) |
| `onsets` | §2.2 harmonic-cluster table (53) p.103 (32 clusters) **plus** §2.3 Appendix 2 (thesis pp.197–205), complete sets incl. singletons (spec §12.D) |
| `codas` | §2.5 Appendix 3 (pp.207–209) |
| `bans` | §2.6 co-occurrence table (62) p.110; §2.9 (VV barred monomorphemically); §2.10 (no geminates) |
| `[repair]` degemination | §3.6 — exceptionless, `%attested` |
| `[repair] cluster-fallback = same-length` | spec §12.E — `%fallback`. §3.0/§3.7 (lines 999–1027) state **no cluster repair is observed**, so this is ours: the test is synthetic and must say so (review-opus §F) |

**S8 caveat to carry into the task:** of the 32 harmonic clusters, only **24** are given in IPA in
the prose (lines 285–286); the other 8 are Latin-only and need the §1.1/§2.0 correspondence charts.
And 2 of the 32 — `zg`, `žg` — are "almost unattested", with `zg` marked **impossible** in the
co-occurrence table (~lines 305–309). Do not assert all 32 are licit onsets; assert the 30 and
list the 2 exclusions in a comment.

- [ ] **Step 1: Write the tests first**

```python
HARMONIC = [...]      # the 30 usable clusters, transcribed from digest §2.2 table (53)

@pytest.mark.parametrize("cluster", HARMONIC)
def test_harmonic_clusters_are_licit_onsets(cluster):
    assert legal_onset(tuple(cluster), TARGET.syllable, TABLE), cluster

def test_zg_and_zhg_are_excluded_deliberately():
    """S8: §2.6's co-occurrence table marks zg impossible."""
    assert not legal_onset(("z", "ɡ"), TARGET.syllable, TABLE)

def test_appendix_2_extraction_is_reproducible(tmp_path):
    """The committed onset list equals the script's output."""
    import subprocess, sys
    out = subprocess.run([sys.executable, str(ROOT / "rules" / "extract_georgian_clusters.py"),
                          str(ROOT / "sources" / "georgian" / "digest.md")],
                         capture_output=True, text=True, check=True).stdout
    assert set(out.split()) <= {"".join(c) for c in TARGET.syllable.onsets} | \
                               {"".join(c) for c in TARGET.syllable.codas}

def test_onsets_include_singletons():
    assert ("k",) in TARGET.syllable.onsets        # spec §12.D

def test_stem_domain_is_used():
    assert TARGET.syllable.domain == "stem"

# I-27 repair table — Georgian's only attested repair is degemination (review-opus §F)
GEORGIAN_REPAIRS = [
    ("tʼvitʼtʼɛri", "tʼvitʼɛri", "digest §3.6 line 989 (Twitter, attested.tsv row 4)"),
    ("pʼazzli",     "pʼazli",    "digest line 948/989/1006 (puzzle, row 16)"),
    ("ʃɔpʼpʼinɡi",  "ʃɔpʼinɡi",  "digest line 879/989 (shopping, row 18)"),
    ("alɛɡɡoria",   "alɛɡoria",  "digest line 992 (native)"),
    ("kʼllasi",     "kʼlasi",    "digest line 992 (native)"),
]

@pytest.mark.parametrize("before,after,cite", GEORGIAN_REPAIRS)
def test_repair_table(before, after, cite):
    rf = TARGET
    got = repair(syllabify(w(before), rf, TABLE), rf, TABLE)
    assert got.ipa(marks=False) == after, cite

def test_cluster_fallback_is_synthetic_not_attested():
    """§3.7 lines 999-1027: no cluster repair is observed in the data. This rule is ours."""
    assert TARGET.cluster_fallback == "same-length"
```

- [ ] **Steps 2–5.** **Acceptance:** Mode C ≥ **0.80** over the rows that reach mode C (of the 122
  with `target_ipa`), error bucket ≤ **15%** of 122 after the I-36 cleaning pass — if it is larger,
  widen the cleaning map or add the missing inventory rows and report the residue in the commit
  body. Mode E is empty; assert it.
  **Commit:** `feat(rules): georgian.rules phonotactics — cluster whitelists, bans, repair`

---

### Task 24: `arabic-egy.rules`

**Depends on:** 21, 22. **Digest:** `sources/arabic-egy/digest.md`.

| Rule block | Source, and the tag it must carry |
|---|---|
| `[inventory]` | §1 "Consonants — the working inventory", §1 "Vowels", §1 notational quirks. **Include `e` and `o`** (I-37: 142/65 attested rows use them) |
| `p→b, v→f, ʒ→ʃ, dʒ→ʒ` | §3.6 — `%attested` |
| `θ→t`, `ð→z` | §3.6 lines 586–587 give θ→**t or s** by stratum and call ð→z Arabic-internal, "not covered" for loans (R15). Take the majority option, `%design`, `# design: digest §3.6 line 586 open` |
| `ŋ → n` | `%design`, `# design: §9.12` |
| broad coronals → emphatics | §8.1 (Cairene over-assigns emphasis to loans before back vowels) — `%design`, `# design: §9.9`, citing §8.1 as evidence |
| slender coronals → plain; `ʃ` kept | §8.1 — `%design`, `# design: §9.1` |
| Irish `/ə/` → `a`/`i` | **`%design`, `# design: digest §8.4 line 1534 open`** — R15: §8.4 and §3.8 lines 715–718 both say Irish /ə/ is "not covered" and offer two undecided options (general /a/ when unstressed; vowel-copy harmony). Pick the digest's first option; do **not** cite §8.3, which is a different topic |
| `x ɣ h` kept | §8.3 — `%attested` |
| `[syllable]` `template = CN(C)(C)`, onsets = every single C and **nothing longer** | §2 "Maximal syllable template", §2 "Onsets" — I-28. Medial CC coda and CCC are `bans` |
| `[repair]` anaptyxis `0 -> i / # C _ C N` | §3.1(a) line 348 — `%attested` |
| `[repair]` prothesis `0 -> ʔ i / # _ s [C -sonorant]` | §3.1(b) lines 379, 386 — `%attested` |
| `[repair]` CCC epenthesis after C2 | §3.2 lines 442, 456, 458 — `%attested` |
| `[repair]` epenthetic quality: `i`, harmonizing to `u` before a round vowel | §3.3 lines 361, 499–503 — `%attested` |
| `[repair]` `0 -> ʔ / # _ N` | §3.7 lines 628, 630 — `%attested` |
| `[post-stress]` §3.8's **six** items | §3.8 lines 726–763: closed-syllable shortening, unstressed-long shortening, mid raising, one-long-vowel-per-word, **vowel lengthening under suffix stress-shift (lines 755–756 — S9; draft 1 omitted it)**, high-vowel syncope |
| **no degemination** | **R14a / spec §12.G — DELETE the rule.** Digest lines 324–326: "No degemination rule is stated for Cairene in any source consulted"; geminates are phonemic. Draft 1 had it |
| no final devoicing | §3.7 line 645 (**not** §3.9 — R14b) — a comment, not a rule |
| no emphasis spread | `# design: §9.10` — a comment, not a rule |
| `[stress] procedure = cairene` | §4 (Task 14) |
| `[epithets]` `NISBA` (-i/-iyya), `FEM_A` (-a), `DEF` (il- + sun letters) | §6.1 (sun-letter list), §6.2 (**11** nisba examples — S10), §6.3 |
| `[meta] epithet-ADJ = NISBA`, `epithet-NOUN = FEM_A` | I-39 |
| `[respell]` kh gh q ʼ h, emphatics **dot-under**, long vowels doubled | §5's table (**21 rows** — S10). Dot-under is `%design`, `# design: §9.11` — R14c: §5 line 1010 explicitly recommends *plain* letters and calls dot-under Abdel-Massih's scholarly system (line 988) |

- [ ] **Step 1: Write the tests first**

```python
@pytest.mark.parametrize("src,expected", [("pˠ", "b"), ("vʲ", "f")])
def test_absent_segments_substitute_per_digest_3_6(src, expected):
    assert adapt([w(src + "aː")], TARGET, TABLE).words[0].segments[0] == expected

def test_broad_coronal_becomes_emphatic():
    assert adapt([w("sˠaː")], TARGET, TABLE).words[0].segments[0] == "sˤ"

def test_slender_s_stays_sh():
    assert adapt([w("ʃaː")], TARGET, TABLE).words[0].segments[0] == "ʃ"

def test_there_is_no_degemination_rule():
    """R14a: geminates are phonemic; digest lines 324-326."""
    src = " ".join(r.comment for r in TARGET.sections.get("repair", ()))
    assert "degemination" not in src.lower()
    out = adapt([w("bˠal̪ˠl̪ˠa")], TARGET, TABLE).words[0].segments
    assert out.count("l") == 2

def test_no_final_obstruent_devoicing():
    assert adapt([w("bˠaːd̪ˠ")], TARGET, TABLE).words[0].segments[-1] == "d"

def test_only_one_long_vowel_survives():
    out = adapt([w("bˠaːt̪ˠaːnˠ")], TARGET, TABLE).words[0].segments
    assert sum(1 for s in out if s.endswith("ː")) <= 1        # §3.8 item 4

def test_nisba_epithet_attaches_and_restresses():
    r = run_entry(Entry("Muster", ipa="mˠʊsˠt̪ˠəɾˠ"), "DESC+ADJ", IRISH, TARGET, TABLE)
    assert r.ipa.rstrip().endswith("i")

def test_definite_article_assimilates_to_sun_letters():
    ...      # digest §6.1: il- + /s/ -> is-s ; write the assertion from the sun-letter list

def test_nisba_table_has_eleven_examples_and_respell_table_21_rows():
    """S10: assert the counts so a truncated transcription is caught."""
    assert len(TARGET.sections["respell"]) >= 21

def test_emphatics_are_respelled_dot_under_by_decision_9_11():
    assert "ṣ" in adapt([w("sˠaː")], TARGET, TABLE).respelling

# I-27 repair table (review-opus §F, digest line refs)
CAIRENE_REPAIRS = [
    ("blastik",  "bilastik", "§3.1(a) line 348/356 — plastic"),
    ("ski",      "ʔiski",    "§3.1(b) line 379/386 — ski"),
    ("banknut",  "bankinut", "§3.2 line 442/456 — banknote, epenthesis after C2"),
    ("bustman",  "bustiman", "§3.2 line 458 — postman"),
    ("ɡrub",     "ɡurub",    "§3.3 line 361/499-503 — group, /u/ harmony"),
    ("otel",     "ʔotel",    "§3.7 line 628/630 — hôtel, glottal insertion"),
    ("kitaːbna", "kitabna",  "§3.8 line 728 — closed-syllable shortening"),
]

@pytest.mark.parametrize("before,after,cite", CAIRENE_REPAIRS)
def test_repair_table(before, after, cite):
    got = repair(syllabify(w(before), TARGET, TABLE), TARGET, TABLE)
    assert got.ipa(marks=False) == after, cite

def test_all_17_cairene_stress_rows_pass_against_the_real_inventory():
    """Re-run Task 14's table with rules/arabic-egy.rules, not the test inventory."""
    from test_stress_cairene import CAIRENE_STRESS_TABLE
    assert len(CAIRENE_STRESS_TABLE) == 17
    for plain, expected in CAIRENE_STRESS_TABLE:
        got = assign_stress(syllabify(w(plain), TARGET, TABLE), TARGET, TABLE)
        assert got.ipa().replace(".", "") == expected, plain
```

*(The repair-table "before" strings are post-substitution Cairene-side forms; where the digest gives
only the orthographic donor and the final adapted form, derive the post-substitution input by hand
and record the derivation in a comment on that row. A row that cannot be derived becomes an `xfail`
naming the digest line — never a silent drop.)*

- [ ] **Steps 2–5.** **Acceptance:** Mode C ≥ **0.75** of the rows reaching mode C (of 279 with
  `target_ipa`); error bucket ≤ **10%** after cleaning (I-37's `e`/`o` inventory rows are what make
  this reachable — draft-1 measurement was 168/279 untokenizable, 142+65 of them `e`/`o`). Mode E
  empty; assert it. All 17 stress rows pass.
  **Commit:** `feat(rules): arabic-egy.rules — Cairene target (digest §1-§6)`

---

### Task 25: `welsh.rules`

**Depends on:** 21, 22. **Digest:** `sources/welsh/digest.md`. **Read I-26 first.**

| Rule block | Source, and the tag it must carry |
|---|---|
| `[inventory]` | §1 "Southern consonant inventory as the sources support it", §1 vowels, §1 add/remove |
| `/sʲ/→ʃ, /tʲ/→tʃ, /dʲ/→dʒ` | §8.1 — `%design` unless §8.1 cites a Welsh source for the specific mapping; `# design: §9.1` |
| other slender/broad → plain | §8.1 — `%design`, `# design: §9.1` |
| `ɣ → ɡ` | **`%design`, `# design: digest §8.2 open`** — R18: §8.2 lists four options and says option 3 has "no Welsh precedent". Spec §7 tags it (A); the spec is wrong here |
| `x → χ` | **`%design`, `# design: digest §8.3 open`** — R18: §8.3 calls it a "(design inference)" with an unresolved [x]/[χ] CONFLICT |
| `h` kept, `w` kept, `ŋ` kept | §8.4, §8.8 — `%attested` |
| voiceless sonorants | §8.5 — they are not Irish phonemes; assert they never arrive, no rule |
| `template = (C)(C)(C)N(N)(C)(C)` | §2.1 line 289. **R19 — the spec drops the `(V)`; the digest has it, and the digest's line is marked (North).** Follow the digest, and surface both facts in the Known Deviations list |
| `nuclei` | the Welsh diphthong list from §1/§2.1 (spec §12.B) |
| `onsets` + `onsets-tier` | §2.2, tiers **A/B/C/D as the digest labels them**. **Tier E is excluded deliberately** (S4): §2.2 line 397 labels it "ASSEMBLED/UNVERIFIED (do not encode without a check)" — generalized stop+liquid onsets, `sm sn`, `θr χr χl`. Say so in a comment |
| `codas` | §2.3 (tier B only; record the tier) |
| `sonority = on` | **`%design`** — R17b: §2.2 never mentions sonority; the term appears at §2.1/§2.3/§2.4 (lines 426, 473–476, 496, 711) and §2.4 line 470 flags its coda generalization as "ASSEMBLED (unattested inference — stronger than the source)" |
| `[repair]` `l -> ɬ / #_`, `ɾ -> r̥ / #_` | §3.3 line 812 — `%design`, `# design: §9.14` |
| `[repair]` sC- prothesis `0 -> ə / # _ s {p t k}` | §3.1 line 618. The digest offers three non-converging encodings and picks none; take Parry-Williams' scope. `%design`, `# design: §9.15` |
| `[repair]` copy epenthesis `0 -> \1 / [V]:1 C _ {l n r} #` | §3.2 rule (1), lines 682, 477, 705 — `%attested`. Uses captures (I-33) |
| `[repair]` liquid deletion `{l ɾ} -> 0 / C _ #` | §3.2 rule (2), lines 522, 689 — `%attested` |
| `[repair]` metathesis `θ:1 ɾ:2 -> \2 \1 / C V* _ #` | §3.2 rule (3), line 696 — `%attested` |
| `[repair]` degemination `CC -> C` in an unstressed syllable | **§2.4 line 499** — R17a: draft 1 cited §2.7, which is *gemination* (`C → Cː / V́ _ V`) |
| `[stress] procedure = penult` | §4.1 — `%design` for the Welsh-first ordering, `# design: §9.13` |
| `[post-stress]` the Southern length rule | §4.3 lines 1071–1079, **the 7-line environment list, verbatim** (I-26): open final → long; before `{b d ɡ v ð f θ χ}` → long; before `{s ʃ ɬ}` → long (South only); before `{pʰ tʰ kʰ m ŋ}` → short; before `{w j}` → short; before CC → short; before `{n l r}` → **lexically determined, so leave unchanged** and tag that line `%design` |
| `[epithets]` | §6's table (lines 1298–1316): 10 rows but only **8 suffixes** (one row is the w→o/y→e adjective ablaut, one is the article) — S5. Select 7 and **state that `-in` is dropped and why** |
| `[meta] epithet-ADJ = AIDD` (`-aidd`), `epithet-NOUN` unmapped | I-39 |
| `[respell]` | §5 (26 consonant rows + 7 vowels + diphthongs): v ff ch dd ll c si/sh, `y` for the prothetic ə |

- [ ] **Step 1: Write the tests first**

```python
def test_slender_coronals_map_to_the_welsh_palatal_series():
    assert adapt([w("ʃaː")], TARGET, TABLE).words[0].segments[0] == "ʃ"
    assert adapt([w("tʲaː")], TARGET, TABLE).words[0].segments[0] == "tʃ"

def test_irish_gamma_becomes_g_as_a_design_choice():
    assert adapt([w("ɣaː")], TARGET, TABLE).words[0].segments[0] == "ɡ"
    rules = [r for r in TARGET.sections["substitute"] if r.target[0].value == "ɣ"]
    assert rules and rules[0].tag == "design"        # R18

def test_initial_l_and_r_fortify():
    assert adapt([w("l̪ˠaː")], TARGET, TABLE).respelling.startswith("ll")
    assert adapt([w("ɾˠaː")], TARGET, TABLE).respelling.startswith("rh")

def test_sc_prothesis_is_written_y():
    r = adapt([w("sˠkaː")], TARGET, TABLE)
    assert r.words[0].segments[0] == "ə" and r.respelling.startswith("y")

def test_template_keeps_the_optional_second_nucleus_slot():
    """R19: digest §2.1 line 289 has (C)(C)(C)V(V)(C)(C); spec §7 drops the (V)."""
    assert sum(1 for slot, _ in TARGET.syllable.template if slot == "N") == 2

def test_tier_e_clusters_are_not_in_the_onset_list():
    """S4: §2.2 line 397 says do not encode tier E without a check."""
    for cl in [("s", "m"), ("s", "n"), ("θ", "r"), ("χ", "r"), ("χ", "l")]:
        assert cl not in TARGET.syllable.onsets

def test_onset_tiers_are_recorded_and_reach_the_trace():
    assert set(TARGET.syllable.onset_tiers.values()) <= {"A", "B", "C", "D"}

def test_southern_length_rule_before_a_voiced_fricative():
    """§4.3 line 1072, row 2: mab, gradd, rhaff, brath, cath, bach."""
    ...

def test_length_before_n_l_r_is_left_unchanged():
    """§4.3 line 1079: lexically determined, not predictable."""
    ...

# I-27 repair table (review-opus §F, digest line refs)
WELSH_REPAIRS = [
    ("pɔbl",     "pɔbɔl",   "§3.2 rule 1, line 682/477/705 — pobl"),
    ("kankr",    "kankar",  "§3.2 rule 1, line 682 — cancr"),
    ("fɛnɛstr",  "fɛnɛst",  "§3.2 rule 2, line 522/689 — ffenestr"),
    ("pɔsibl",   "pɔsib",   "§3.2 rule 2, line 689 — posibl"),
    ("ewɨθr",    "ewɨrθ",   "§3.2 rule 3, line 696 — ewythr"),
    ("lɔft",     "ɬɔft",    "§3.3 line 812 — loft > lloft"),
    ("rəmedi",   "r̥əmedi",  "§3.3 line 812 — remedy > rhymedi"),
    ("skarlat",  "əskarlat","§3.1 line 618 — scarlet > ysgarlat"),
    ("stiwart",  "əstiwart","§3.1 line 618 — steward > ystiwart"),
]

@pytest.mark.parametrize("before,after,cite", WELSH_REPAIRS)
def test_repair_table(before, after, cite):
    assert repair(syllabify(w(before), TARGET, TABLE), TARGET, TABLE).ipa(marks=False) == after, cite

@pytest.mark.xfail(reason="digest line 508 gives only the orthographic pair cannu/canu; "
                          "no IPA before/after pair exists for degemination")
def test_degemination_has_no_attested_ipa_example():
    assert False
```

- [ ] **Steps 2–5.** **Acceptance:** Mode C ≥ **0.70** of the **19** rows with `target_ipa` (≥ 13);
  error bucket **0** after cleaning (all 19 draft-1 failures were `[ ]`/`/ /` wrappers, which I-36
  strips). Mode E empty. Also assert the harness classifies the 93 `layer=modern` orthography-only
  rows as `skip` without crashing — **do not** attempt orthographic comparison (that needs a Welsh
  G2P, out of scope).
  **Commit:** `feat(rules): welsh.rules — Southern Welsh target (digest §1-§6)`

---

### Task 26: `dutch.rules`

**Depends on:** 21, 22. **Digest:** `sources/dutch/digest.md`.

| Rule block | Source, and the tag it must carry |
|---|---|
| `[inventory]` | §1 (Verhoeven's chart; parenthesised entries become the `marginal:` line), §1 vowels. `ʋ` comes from the Task 1b hand rows |
| slender C → `C j` in onsets, plain in codas | §8.1 — I-31 epenthesis form; `%design`, `# design: §9.16` |
| broad → plain; `ɣ x h ʃ` kept | §8.2, §3.4 — `%attested` |
| `w → ʋ` | **§0 line 32** (the normalization-layer entry) — R20a: it is *not* in §8.2 or §3.4, where draft 1 cited it |
| length → tense/lax table | §8.3, §3.6 — the digest's own proposal, explicitly unsourced → `%fallback` |
| `ə` kept | §8.3 — `%attested` |
| `template` onset ≤3 (first = /s/ if 3), coda ≤2 | §2 "Maximal template", "Coda size" |
| `nuclei` | the Dutch diphthongs `ɛi œy ɔu` (spec §12.B) |
| `onsets` | §2 lines 179–186: **30 native CC and 27 loan CC** (R21 — not "~28/~24"), plus the **separate 7-item CCC list** at lines 209–213 (4 native + 3 loan), plus all singletons (spec §12.D) |
| `codas` | §2 "Coda clusters", by class |
| `appendix` | §2 line 158 says "up to three **coronal obstruents**". Draft 1 narrowed this to `s t`; either widen the set to the coronal obstruents of the inventory or keep `s t` and tag the narrowing `%design` with the line reference (R21) |
| `bans` | §2 lines ~278–320: (a) the tense-V/voiceless-fricative pact — bites only on stressed `Vːx Vːf Vːs`; (b) Kager & Pater `*[V +long] C C [-coronal]`, with the final-coronal-appendix escape |
| `[repair]` final obstruent devoicing | §3.5 lines 363, 561 — `%attested` |
| `[repair]` `0 -> ə / LIQ _ C` non-homorganic, blocked before a coronal C2 | §3.2 lines 456–470 — `%attested`. **R20b: *herfst* [hɛr(ə)fst] (line 457/470) is a POSITIVE example; only *hals* (homorganic, line 465) and *hart* (coronal C2, line 467) block.** Draft 1 had *herfst* as a blocking case |
| `[repair]` tense-V + voiceless fricative → voice the fricative | §8.6 / §9 item 5, line 308 — `%design`, `# design: §9.18` |
| `[repair]` degemination | §2 lines 353–355 — `%attested` |
| no onset-cluster repair | §3.1 (loans keep illicit onsets) — a comment, not a rule |
| `[stress] procedure = dutch-weight` | §4 lines 671–687 — `%design` (digest-constructed), `# design: §9.17` |
| `[epithets]` `ACHTIG` (-achtig), `IG` (-ig), `TJE` (-(t)je with allomorphs -je/-tje/-pje/-etje/-kje) | §6's 10-item table |
| `[meta] epithet-ADJ = ACHTIG`, `epithet-NOUN` unmapped | I-39 |
| `[respell]` | §5 "Phoneme → spelling" + the **6-step doubling algorithm** (§5 "The doubling algorithm"), implemented verbatim |

- [ ] **Step 1: Write the tests first**

```python
def test_slender_consonant_in_an_onset_gets_a_yod_and_in_a_coda_is_plain():
    assert adapt([w("tʲaː")], TARGET, TABLE).words[0].segments[:2] == ("t", "j")
    assert adapt([w("aːtʲ")], TARGET, TABLE).words[0].segments[-1] == "t"

def test_w_becomes_the_labiodental_approximant():
    assert adapt([w("waː")], TARGET, TABLE).words[0].segments[0] == "ʋ"

def test_final_obstruent_devoicing():
    assert adapt([w("bˠaːd̪ˠ")], TARGET, TABLE).words[0].segments[-1] == "t"

def test_matanach_does_not_trigger_the_fricative_ban():
    """goals note + digest §2: the /x/ follows the schwa of -ach, not the long vowel."""
    assert adapt([w("mˠat̪ˠaːnˠəx")], TARGET, TABLE).words[0].segments[-1] == "x"

def test_bach_does_trigger_it():
    """digest line 308: the ban bites when a long vowel directly precedes."""
    out = adapt([w("bˠaːx")], TARGET, TABLE).words[0].segments
    assert out[-1] == "ɣ"                      # decision 9.18: voice the fricative

def test_onset_list_sizes_match_the_digest():
    """R21: 30 native CC + 27 loan CC + 7 CCC, plus singletons."""
    cc = {c for c in TARGET.syllable.onsets if len(c) == 2}
    ccc = {c for c in TARGET.syllable.onsets if len(c) == 3}
    assert len(cc) == 57 and len(ccc) == 7

def test_dutch_weight_stress_is_used():
    assert "ˈ" in adapt([w("mˠat̪ˠaːnˠəx")], TARGET, TABLE).ipa

def test_doubling_algorithm_in_the_respelling():
    ...      # §5's 6 steps: long V in a closed syllable doubles the vowel letter; a short V
             # before a single intervocalic C doubles the consonant letter

# I-27 repair table (review-opus §F, digest line refs)
DUTCH_REPAIRS = [
    ("mɛlk",   "mɛlək",  "§3.2 line 457 — melk, schwa epenthesis"),
    ("kɑlm",   "kɑləm",  "§3.2 line 456 — kalm"),
    ("hɛrfst", "hɛrəfst","§3.2 line 457/470 — herfst DOES epenthesize (R20b)"),
    ("hɑls",   "hɑls",   "§3.2 line 465 — hals blocks (homorganic)"),
    ("hɑrt",   "hɑrt",   "§3.2 line 467 — hart blocks (coronal C2)"),
    ("hɑnd",   "hɑnt",   "§3.5 line 363/561 — hand, final devoicing"),
    ("etː",    "et",     "§2 line 353-355 — eet, degemination"),
    ("ɡroːtːə", "ɡroːtə", "§2 line 353-355 — grootte"),
    ("bɑːx",   "bɑːɣ",   "§8.6 line 308 — bách, tense-V + voiceless fricative (design 9.18)"),
]

@pytest.mark.parametrize("before,after,cite", DUTCH_REPAIRS)
def test_repair_table(before, after, cite):
    assert repair(syllabify(w(before), TARGET, TABLE), TARGET, TABLE).ipa(marks=False) == after, cite

def test_matanach_control_row():
    """The §8.6 worked derivation, lines 1025-1091 — the ban's non-trigger control."""
    ...
```

- [ ] **Steps 2–5.** **Acceptance:** Mode C ≥ **0.80** of the **67** rows with `target_ipa`
  (error bucket ≤ **10%** after cleaning — draft-1 measurement was 30/67 untokenizable, mostly
  ASCII `:` and `'`), **and** Mode E ≥ **0.25** of the **32** two-sided rows (8/32). Mode E is low
  by design: those rows are English→Dutch loans adapted by donor-specific routes while this file is
  tuned for Irish input; the ratchet, not the absolute number, is the value. Record both rates.
  **Commit:** `feat(rules): dutch.rules — Belgian Dutch target (digest §1-§6)`

---

## Task 27: CLI — `run`, `explain`, `gallery`, `lint`

**Depends on:** Tasks 20, 21, 23a, 23b, 24, 25, 26 (R27: the tests below assert over all four real
targets)

**Files:** modify `src/strands/cli.py`; create `src/strands/gallery.py`, `tests/test_cli.py`.

**Interfaces (spec §6):**

```
strands run   INPUT.tsv [--strand welsh|arabic-egy|georgian|dutch|all]
                        [--construction NAME|all] [--out out.tsv]
strands explain WORD --strand X [--construction NAME]
strands gallery INPUT.tsv [--out gallery.md]
strands lint  INPUT.tsv [--accept]
strands check RULES.rules
```

```python
def cmd_run(args) -> int      # TSV: orthography, construction, strand, respelling, ipa,
                              # flags, fallbacks, assumptions
def cmd_explain(args) -> int  # trace: stage, rule_id, tag, before -> after, citation comment
def cmd_gallery(args) -> int
def cmd_lint(args) -> int
def render_gallery(entries, targets, constructions, table) -> str
```

`--construction all` enumerates `CONSTRUCTIONS` (Task 21), which includes the `DESC+ADJ` /
`DESC+NOUN` epithet tags (I-39) — so every target's `[epithets]` block is reachable from the CLI.

- [ ] **Step 1: Failing test**

```python
def test_run_writes_one_row_per_word_construction_strand(tmp_path):
    out = tmp_path / "o.tsv"
    assert main(["run", str(FIX), "--strand", "all", "--construction", "DESC",
                 "--out", str(out)]) == 0
    rows = list(csv.DictReader(out.open(encoding="utf-8"), delimiter="\t"))
    assert {r["strand"] for r in rows} == set(TARGETS)
    assert set(rows[0]) == {"orthography", "construction", "strand", "respelling", "ipa",
                            "flags", "fallbacks", "assumptions"}

def test_construction_all_includes_the_epithet_tags(tmp_path):
    out = tmp_path / "o.tsv"
    main(["run", str(FIX), "--strand", "arabic-egy", "--construction", "all", "--out", str(out)])
    rows = list(csv.DictReader(out.open(encoding="utf-8"), delimiter="\t"))
    assert "DESC+ADJ" in {r["construction"] for r in rows}       # I-39 reachability

def test_run_is_deterministic(tmp_path):
    a, b = tmp_path / "a.tsv", tmp_path / "b.tsv"
    main(["run", str(FIX), "--out", str(a)]); main(["run", str(FIX), "--out", str(b)])
    assert a.read_bytes() == b.read_bytes()

def test_explain_prints_stages_rule_ids_and_citations(capsys):
    assert main(["explain", "ˈciəɾˠə", "--strand", "welsh"]) == 0
    out = capsys.readouterr().out
    assert "substitute" in out and "syllabify" in out and "->" in out and "[" in out

def test_explain_rejects_an_unknown_strand():
    assert main(["explain", "kaː", "--strand", "klingon"]) == 2

def test_gallery_emits_markdown(tmp_path):
    out = tmp_path / "g.md"
    assert main(["gallery", str(FIX), "--out", str(out)]) == 0
    assert out.read_text(encoding="utf-8").startswith("#")

def test_lint_lists_inferred_fields(capsys):
    assert main(["lint", str(FIX)]) == 0
    assert "declension" in capsys.readouterr().out

def test_lint_accept_rewrites_the_file(tmp_path):
    dst = tmp_path / "in.tsv"; shutil.copy(FIX, dst)
    before = dst.read_text(encoding="utf-8")
    assert main(["lint", str(dst), "--accept"]) == 0
    assert dst.read_text(encoding="utf-8") != before

def test_missing_slot_and_missing_ipa_are_skipped_with_a_note(tmp_path):
    out = tmp_path / "o.tsv"
    assert main(["run", str(FIX), "--construction", "PATRO_O", "--out", str(out)]) == 0
    rows = list(csv.DictReader(out.open(encoding="utf-8"), delimiter="\t"))
    assert any("skipped" in r["assumptions"] for r in rows)
```

- [ ] **Steps 2–4. Step 5: Commit** — `feat(strands): run/explain/gallery/lint subcommands`

---

## Task 28: Gallery snapshot and property checks

**Depends on:** Task 27

**Files:** create `tests/snapshots/gallery.md` (generated then committed),
`tests/allow-unrepaired.txt` (starts empty), `tests/test_properties.py`,
`tests/test_gallery_snapshot.py`.

- [ ] **Step 1: Write the failing tests**

```python
# test_gallery_snapshot.py
def test_gallery_matches_the_committed_snapshot(tmp_path):
    out = tmp_path / "g.md"
    main(["gallery", str(ROOT / "sources" / "irish" / "test-words.tsv"), "--out", str(out)])
    expected = (ROOT / "tests" / "snapshots" / "gallery.md").read_text(encoding="utf-8")
    assert out.read_text(encoding="utf-8") == expected, \
        "gallery changed — regenerate and review the diff in the commit"

# test_properties.py  (spec §8 layer 5)
def test_determinism_across_two_runs():
    for name in TARGETS:
        rf = load_target(name, TABLE)
        for row in read_test_words():
            e = entry_of(row)
            assert run_entry(e, "DESC", IRISH, rf, TABLE) == run_entry(e, "DESC", IRISH, rf, TABLE)

def test_every_output_segment_is_in_the_target_inventory():
    for name in TARGETS:
        rf = load_target(name, TABLE)
        for row in read_test_words():
            for word in run_entry(entry_of(row), "DESC", IRISH, rf, TABLE).words:
                assert set(word.segments) <= set(rf.inventory), (name, row["orthography"])

def test_no_unrepaired_outside_the_allow_file():
    allowed = read_allow_file()
    bad = [(n, row["orthography"]) for n in TARGETS
           for row in read_test_words()
           if "UNREPAIRED" in run_entry(entry_of(row), "DESC", IRISH,
                                        load_target(n, TABLE), TABLE).flags
           and (n, row["orthography"]) not in allowed]
    assert bad == [], bad

def test_every_word_gets_exactly_one_primary_stress():
    for name in TARGETS:
        rf = load_target(name, TABLE)
        for row in read_test_words():
            for word in run_entry(entry_of(row), "DESC", IRISH, rf, TABLE).words:
                assert word.stress is not None

def test_traces_are_never_empty():
    for name in TARGETS:
        rf = load_target(name, TABLE)
        assert run_entry(entry_of(read_test_words()[0]), "DESC", IRISH, rf, TABLE).trace
```

- [ ] **Step 2: Run — the snapshot test fails (no snapshot).**
- [ ] **Step 3: Generate the snapshot**
  `uv run strands gallery sources/irish/test-words.tsv --out tests/snapshots/gallery.md`
  and **read the diff** — this is the review artefact for the whole project. Anything wrong is a
  rule-file bug, fixed in Tasks 23–26, never by editing the snapshot.
- [ ] **Step 4: Run the full suite — green.**
- [ ] **Step 5: Commit** — `test(strands): gallery snapshot and cross-target property checks`

**Acceptance:** milestone 7 complete; `uv run pytest` green from a clean checkout;
`uv run strands run sources/irish/test-words.tsv --strand all --construction all` succeeds.

---

## Rule about elided test bodies

A few test bodies in Tasks 14, 15, 23a–26 are a comment naming the digest fact plus `...`. That is
**not** permission to skip them: the comment names the section and worked example, and the
implementer's first action is to open that section and write the assertion from the source's own
transcription. **A test committed with a `...` body, or with an assertion that cannot fail (`or
True`, `in {a, b}`), is a failed task** and will be rejected in review. Where the digest genuinely
states no expected output, the test becomes an `xfail` carrying the digest line number — never a
deletion.

---

## Known deviations from the spec (for the owner)

1. **Spec §8 layer-3 regression is unbuildable for three of four targets** (I-25). Only Dutch has
   32 rows with both IPA sides. Mode C substitutes inventory/syllable/stress conformance and the
   per-target repair tables (I-27) cover the rest. Denominators: Georgian 122, Cairene 279, Welsh
   19, Dutch 67.
2. **"Awbery's tree" (spec §7, Welsh) does not exist** (I-26); the §4.3 seven-line environment list
   is used instead. Spec §11's open item stays open.
3. **Welsh syllable template**: the digest (§2.1 line 289) gives `(C)(C)(C)V(V)(C)(C)` and marks it
   **(North)**; spec §7 drops the `(V)`. The plan follows the digest and carries the North
   provenance caveat (R19).
4. **Georgian §3.1 contradicts spec §9 row 4**: the digest explicitly rejects the
   aspirate/ejective environment split and recommends unconditional ejective. The spec's decision
   stands, tagged `%design` with a `contra` note (R11).
5. **Cairene degemination is removed** (R14a, spec §12.G): geminates are phonemic and no source
   states a degemination rule. Draft 1 had the rule and a test for it.
6. **Cairene dot-under respelling** contradicts §5's own recommendation of plain letters; kept as
   decision 9.11, cited as design (R14c).
7. **Welsh `ɣ→ɡ`, `x→χ`, `sonority = on`** are spec-§7-tagged (A) but the digest calls them design
   inferences or flags them unattested; all three are `%design` here (R17b, R18).
8. **Georgian `Kas'queil`**: under §5.3's D5 (apostrophe placement unchanged) the engine spells it
   *Kasq'ueil*, diverging from the pre-existing strand-4 name list. Made visible by a test rather
   than papered over (R13b).
