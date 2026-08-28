# Strands: Irish→target name-adaptation engine — design spec

Status: approved in design discussion 2026-08-25. Source of truth for the implementation plan.
Background: `../../notes/project-goals.md` (what and why), `../../sources/<lang>/digest.md`
(the linguistic facts, cited), `../../notes/report-2026-08-24.md` (the decisions this spec fixes).

## 1. Purpose and scope

A deterministic command-line tool that takes Irish (Gaeilge) names, descriptors and epithets
in IPA and produces, for each of four "strands", the form a speaker of that strand's target
language would make of them — Southern Welsh, Cairene Arabic, Standard Georgian, Belgian
Dutch — as IPA plus an English-reader respelling, with a derivation trace. Five strands exist
in the fiction; the fifth (Old Irish) is a lookup task and is **out of scope** here.

Non-goals: probabilistic output; perception modelling; a general Irish declension engine; a
general G2P (the *provisional* Irish G2P of milestone 8 is Irish-only); creole-style reduction layers;
any GUI.

Tooling: Python ≥3.12, `uv`, `pytest`, no runtime dependencies beyond the standard library
(PanPhon/CLTS were considered and rejected: the project's own feature table is smaller and
covers the diacritic segments Irish needs). Package `strands` at the repository root, with
`pyproject.toml` there; CLI entry point `strands`.

Repo layout:

```
<repo root>/
  pyproject.toml
  src/strands/            # the engine
  rules/
    features.csv          # segment → PHOIBLE-style features (all languages)
    irish.rules           # pre-pass: templates, mutation tables, normalization
    welsh.rules  arabic-egy.rules  georgian.rules  dutch.rules
  tests/                  # pytest; fixtures point at sources/*/attested.csv, irish/test-words.csv
  docs/specs/             # this file
  sources/  notes/  chat-imports/   # existing
```

## 2. Data model

**Segment**: an IPA string — base symbol plus diacritics — treated as an opaque token
(`tʲ`, `t̪ˠ`, `tʼ`, `sˤ`, `aː`). Tokenization is longest-match against the segment list in
`features.csv`; an input containing a segment not in the table is a hard error naming the
word and the offending substring.

**Word**: a list of segments plus parallel annotations: syllable boundaries, stress
(primary only), morpheme boundaries `$` (stem edges and affix joins), and a per-segment
"illegal" mark set by syllabification. Words carry a trace: an ordered list of
`(stage, rule_id, rule_tag, before, after)`.

**Feature table** (`rules/features.csv`): one row per segment, columns = PHOIBLE's 38 features
with values `+`, `-`, `0` (undefined). The four target inventories are copied from
`chat-imports/phoible_inventories_starter.csv`. Irish segments and all diacritic segments are
added by hand with these conventions: slender = `+front -back` on the consonant, broad =
`+back` (and `-front`); ejective = `+raisedLarynxEjective`; emphatic = `+retractedTongueRoot`
`+back`; aspirated = `+spreadGlottis`; long vowels = `+long`. Feature distance = count of
features on which both segments are defined and differ, optionally weighted by a per-language
weight vector declared in the rule file (`[weights]`, default all 1).

**Class**: a named set of segments, declared in `[classes]`, usable in rules. Predeclared:
`C` (all consonants in the file's inventory plus any consonant in the Irish inventory), `V`
(likewise vowels).

## 3. Rule DSL

One file per language, UTF-8, `#` comments, sections introduced by `[name]`. Sections:
`[meta]`, `[inventory]`, `[classes]`, `[weights]`, `[substitute]`, `[syllable]`, `[repair]`,
`[post-stress]`, `[stress]`, `[epithets]`, `[respell]`; Irish additionally `[templates]`,
`[mutations]`, `[inflect]`, `[normalize]`.

**Rewrite rule line** (in `[substitute]`, `[repair]`, `[post-stress]`, `[respell]`,
`[mutations]`, `[normalize]`):

```
TARGET -> REPLACEMENT [/ LEFT _ RIGHT] [%tag] [# comment]
```

- `TARGET`: one or more segment tokens, a class name, or a feature bundle `[C +back -labial]`
  (class name first, then feature constraints). `0` = empty (epenthesis).
- `REPLACEMENT`: segment tokens, `0` (deletion), or a feature-change bundle `[+ejective]`
  applied to the matched segment. Multiple-segment targets may be replaced by multiple
  segments; feature-change applies to each matched segment.
- `LEFT`/`RIGHT`: sequences of segment tokens, classes, bundles, `#` (word edge), `$` (morpheme
  edge), `.` (syllable boundary), `ˈ` (stressed-syllable start); `()` optional, `*` zero-or-more
  on a single item. Either side may be empty.
- `%tag`: exactly one of `%attested`, `%design`, `%fallback`; default `%attested`. The tag is
  copied into the trace.
- Rules apply in file order; each rule scans left-to-right, non-overlapping, and applies to
  all matches before the next rule (simultaneous within a rule, ordered across rules).

**`[inventory]`**: whitespace-separated segments; `marginal:` prefix line for marginal ones
(allowed in output, never chosen by fallback).

**`[syllable]`**:
```
template = (C)(C)(C)V(C)(C)      # or: any
onsets   = pl pr bl br ... | any  # whitespace list, or 'any'
onsets-tier = pl:A pr:A str:B ... # optional evidence tiers, informational (trace only)
codas    = ... | any
appendix = s t                    # optional: extra word-final coronal obstruents (Dutch)
domain   = word | stem            # legality domain; 'stem' uses $ edges (Georgian)
sonority = on | off               # apply a sonority-sequencing check inside clusters
bans     = [V +long] C C [-coronal]   # optional extra illegal sequences, one per line
```
Legality of a parse = template ∧ onset-set ∧ coda-set ∧ sonority ∧ not-banned; any component
may be `any`/`off`. Parser: maximal onset subject to legality; on failure, mark the minimal
illegal span rather than raising.

**`[stress]`**: `procedure = initial | penult | cairene | dutch-weight | keep-source`, plus
procedure-specific parameters on following lines (documented in the implementation).

**`[epithets]`**: `NAME = form / attach-condition` lines, e.g. `NISBA = i / $_ #`.

**`[respell]`**: rewrite rules from IPA to Latin strings; the right-hand side is quoted text;
context may reference syllable/stress marks. Applied after all phonology; output is a string.

**Irish-only sections**: `[mutations]` holds named tables (`LEN`, `ECL`, `HPREF`, `TPREF`) of
`X -> Y` lines; `[inflect]` holds named regular inflections (`GEN_M1`, `GEN_ACH`, `GEN_F2`,
`VOC_M1`) as rewrite rules anchored at `#`; `[templates]` holds construction recipes:

```
VOC     = "a" LEN(NAME) VOC_M1?          # ? = only if class m1
GEN     = GEN(NAME)                       # GEN() dispatches on declension tag
PATRO_O = "ó" GEN(FATHER)
PATRO_NI = "ní" LEN(GEN(FATHER))
ADJ     = NAME " " LEN_IF_F(ADJ)
OF      = NAME " " ART(GEN(NOUN))         # ART applies article + gender/number mutation
COMPOUND= FIRST LEN(SECOND)
DESC    = NOUN
```
Every join inserts `$`. Words separated by `" "` are adapted separately by the target and
joined in the output.

## 4. Pipeline

Stages, in order; each reads one section and appends to the trace.

1. **Irish pre-pass** (`irish.rules`): apply the requested template using `[mutations]` and
   `[inflect]`; then `[normalize]` (every consonant gets ʲ or ˠ from the adjacent-vowel
   convention if unmarked; Connacht initial stress marked; user phonemes untouched).
2. **Substitute** (`[substitute]`), then the fallback: any segment not in `[inventory]` is
   replaced by the nearest non-marginal inventory segment by feature distance, tagged
   `%fallback`; ties broken by inventory order.
3. **Syllabify** (`[syllable]`): parse and mark illegal spans.
4. **Repair** (`[repair]`): apply rules; after any rule that changes the segment count,
   re-syllabify. Loop until no illegal marks remain or 10 iterations; then flag `UNREPAIRED`.
5. **Stress** (`[stress]`), then `[post-stress]` rules (length/quality adjustments that
   depend on stress).
6. **Epithet affixation** (`[epithets]`, only when the template requests a target affix):
   attach at `$`, then re-run 3–5 on the result.
7. **Respell** (`[respell]`).

Output record per (word, construction, strand): respelling, IPA (with stress and syllable
marks), flags (`UNREPAIRED`, fallback count), assumptions (from input inference), trace.

Determinism: no randomness anywhere; identical input and rule files give identical output.

## 5. Input

TSV, header row: `orthography ipa dialect gloss category gender gen_ipa pl_ipa note`.
Only `orthography` is required. Missing `ipa` → constructed from the spelling by the
provisional Irish G2P (`strands.g2p`, milestone 8, now implemented) and tagged
`ipa:constructed`; only an orthography the reader cannot read leaves the row skipped
with a note.
Missing `gender` → inferred (known-name list, then ending heuristics, else `m`), tagged.
Missing `gen_ipa` → inferred by declension shape (broad-C-final m → slenderize; `-ach` →
`-aigh`; f + C → slenderize + `-e`; vowel-final → unchanged), tagged. Missing `dialect` →
`C`. Constructions needing an absent field (`OF` without a noun, `PATRO` without a father)
are skipped for that row with a note. `strands lint` lists rows with missing fields and the
tool's guesses; `strands lint --accept` writes the guesses into the TSV.

## 6. CLI

```
strands run   INPUT.csv [--strand welsh|arabic-egy|georgian|dutch|all] [--construction NAME|all] [--out out.csv]
strands explain WORD --strand X [--construction NAME]     # derivation trace with rule tags + citations
strands gallery INPUT.csv [--out gallery.md]              # words × constructions × strands, Markdown
strands lint  INPUT.csv [--accept]
strands check RULES.rules                                  # parse + static checks (undefined segments/classes)
```

## 7. Per-target rule content (compiled from the digests)

Tags: A attested (cite in the file), D design decision (see §9), F fallback.

**Welsh (Southern)**: substitute /sʲ/→ʃ, /tʲ/→tʃ, /dʲ/→dʒ (A); other slender/broad → plain
(D); /ɣ/→g (A), /x/→χ, /h/ kept, /w/ kept, /ŋ/ kept. Syllable: template (C)(C)(C)V(C)(C),
onset list with tiers, coda list partial, sonority on. Repair: initial l→ɬ, r→r̥ (A hist.,
D ON); sC- prothesis 0→ə/#_s[stop] written as `y` (D ON); final liquid+C → epenthesis or
deletion per attested pattern; degemination. Stress: penult (Welsh-first, D); post-stress:
Southern length rule (Awbery's tree). Respell: v ff ch dd ll c si/sh, `y` for the prothetic ə.

**Egyptian Arabic (Cairene)**: substitute p→b, v→f (A); /sʲ/→ʃ; broad coronals →
emphatics (A+D); slender coronals → plain; x ɣ h kept; ŋ→n (D); /ə/ → a/i by position (A);
long vowels kept. Syllable: template CV CVC CVː CVːC# CVCC#, no onset clusters. Repair:
0→i/#C_C (A); 0→i/CC_C (A, C2–C3); final CCC epenthesis; no final obstruent devoicing; no
emphasis spread (D); vowel shortening in closed syllables (A); degemination. Stress: cairene.
Epithets: nisba -i/-iyya, fem -a, il- with sun-letter assimilation (A). Respell: kh gh q ʼ h,
emphatics dot-under (D), long vowels doubled.

**Georgian (Standard; strand 4)**: substitute /p t k/→pʰ tʰ kʰ; [STOP −voice]→[+ejective]/C_
(A); f→pʰ (A); w→v (A); h kept; ŋ→n; slender coronals → ʃ ʒ tʃʰ dʒ (D); broad non-labial
C → C v / _[V +front] (D, Cʷ); slender C → C i / _[V +back] (D); ə→a; long→short (A);
diphthongs → V.V (A editorial). Syllable: template any, onsets/codas = Butskhrikidze App. 2–3
lists, domain stem. Repair: degemination (A); whitelist miss → nearest attested cluster (F).
Stress: initial, unmarked. Epithets: nouns +i (A); -uri/-uli, -eli; syncope before -eb-.
Respell: national 2002; apostrophe after ejectives; x, gh, tch (/tʃʼ/), ch (/tʃʰ/); y for /i/
in non-initial closed syllables; personal names emitted as bare stem (A for names).

**Dutch (Belgian)**: substitute slender C → C j in onsets, plain in codas (D); broad → plain;
ɣ x h kept; ʃ kept; w→ʋ; length → tense/lax (F table); ə kept. Syllable: template + onset/coda
lists + appendix s t; bans `[V +long] C C [-coronal]`, tense-V + voiceless-fricative.
Repair: final obstruent devoicing (A); 0→ə / [liquid]_C non-homorganic, blocked before s t (A);
tense-V + voiceless fricative → voice the fricative (D); degemination. Stress: dutch-weight (D).
Epithets: -achtig, -ig, -(t)je (A). Respell: oo/ee/aa, gh/kh, w, uy/eu/oo.

Every rule line in a target file carries a `# [key p.N]` citation to its digest source, or
`# design: §9.n` for D-tagged rules.

## 8. Testing

Test-first at every milestone (`pytest`). Layers:
1. **Parser**: every DSL construct round-trips; malformed lines raise with line numbers.
2. **Stage unit tests**: mutation tables against `sources/irish/digest.md §3` exemplar triads
   and all 144 `test-words.csv` rows tagged for mutations; syllabifier against each target's
   lists (positive and negative cases); each repair rule against the attested rows that
   instantiate it; each stress procedure against the digests' worked tables (Cairene 17 rows,
   Dutch examples, Welsh length tree, Georgian initial).
3. **Regression against attested data**: for each target, run the attested *source* forms
   (where source IPA exists) through stages 2–7 and compare to attested target IPA; report
   pass rate per target, assert it does not decrease (ratchet file committed with the tests).
4. **Gallery snapshot**: `strands gallery` over `test-words.csv` committed as a snapshot;
   changes must be intentional (diff reviewed in commit).
5. **Property checks**: determinism (run twice, identical); every output segment in the
   target inventory; no `UNREPAIRED` on the 144-word set for any strand unless listed in an
   allow-file.

## 9. Decision register

One row per design default; each is one line to change in the named file.

| # | Decision | Default | Alternative(s) | Where |
|---|---|---|---|---|
| 1 | Broad/slender, general | contrast kept on coronals via native palatal series; dropped on labials/dorsals | keep on all places via onglides; collapse everywhere | each `[substitute]` |
| 2 | Slender C before back V | Welsh: via si/ti/di; Dutch: Cj (onsets); Georgian: Ci; Arabic: nothing | drop everywhere | each `[substitute]` |
| 3 | Broad non-labial C before front V (Georgian) | C+v (Cʷ) | plain | `georgian.rules` |
| 4 | Irish /p t k/ in Georgian | aspirate; ejective after C | all-ejective (prescriptive norm) | `georgian.rules` |
| 5 | Georgian word-level laryngeal harmony | off | on | `georgian.rules` |
| 6 | Georgian /w/ | → v | → u positionally | `georgian.rules` |
| 7 | Georgian personal names | bare stem | nominative -i | `georgian.rules [respell]/[epithets]` |
| 8 | Georgian `y` | /i/ in non-initial closed syllables | never | `georgian.rules [respell]` |
| 9 | Arabic broad coronals | → emphatics | plain | `arabic-egy.rules` |
| 10 | Arabic emphasis spread | off | leftward to word edge | `arabic-egy.rules` |
| 11 | Arabic emphatic respelling | dot-under | plain letters | `arabic-egy.rules [respell]` |
| 12 | Arabic /ŋ/ | → n | → ng | `arabic-egy.rules` |
| 13 | Welsh stress vs Irish length | Welsh-first | length-first | `welsh.rules [stress]` |
| 14 | Welsh initial l-/r- fortition | on (ll-, rh-) | off | `welsh.rules [repair]` |
| 15 | Welsh sC- prothesis | on, as `y` | off | `welsh.rules [repair]` |
| 16 | Dutch slender C | Cj in onsets, plain in codas | vowel colouring | `dutch.rules` |
| 17 | Dutch stress | dutch-weight | keep-source | `dutch.rules [stress]` |
| 18 | Dutch long V + voiceless fricative | voice the fricative | lax the vowel; accept | `dutch.rules [repair]` |
| 19 | Irish reference dialect | Connacht | Munster/Ulster rows pass through | `irish.rules` |
| 20 | Source stress handed to targets | marked; each target decides (13, 17) | — | `irish.rules [normalize]` |

## 10. Milestones (each: tests first, then code, then commit)

1. Feature table + tokenizer + DSL parser + `strands check`.
2. Rewrite-rule engine (substitute/repair/respell application, feature bundles, fallback).
3. Syllabifier (template ∧ lists ∧ sonority ∧ bans, stem domain) + repair loop.
4. Stress procedures (initial, penult, cairene, dutch-weight, keep-source) + post-stress.
5. Irish pre-pass: mutations, inflections, templates, normalization, input inference, lint.
6. Target rule files, one per milestone-commit each: Georgian, Arabic, Welsh, Dutch — each
   with its regression run against attested data and its section of the gallery.
7. CLI (`run`, `explain`, `gallery`, `lint`) and the committed gallery snapshot.
8. Provisional Irish G2P (`strands.g2p`), wired into input inference — **done**.

## 11. Open items carried, not blocking

- Awbery 1984 cluster tables (Welsh): when screenshots arrive, re-tier `welsh.rules
  [syllable]` and revisit decision 13's length tree.
- Georgian three-object licitness (stem vs word vs transliteration): the whitelist uses stem
  domain; word-form legality for epithets with -i is handled by re-syllabifying after
  affixation. Revisit if outputs look wrong at edges.
- Old Irish strand: separate spec.

## 12. Amendments after plan review (2026-08-25)

These override earlier sections where they conflict.

**A. Repair loop (§4 stage 4).** `[repair]` rules apply unconditionally, in order, once per
pass — many are active processes (Dutch final devoicing, Welsh fortition/prothesis), not fixes
for illegal parses. After any rule that changes the word (count-preserving or not),
re-syllabify. Run further passes only while illegal marks remain **and** the previous pass
changed something (cycle detection on the segment string); cap 10; then `UNREPAIRED`.

**B. Nuclei and diphthongs (§2, §3 `[syllable]`).** Diphthongs are tokenized as two vowel
segments but grouped into **one nucleus** when the language licenses the sequence:
`[syllable]` gains `nuclei = iə uə əi əu ...` (Irish, Welsh, Dutch lists from their digests;
Georgian: none — every V is its own nucleus, giving the attested hiatus). Stress, weight and
templates count nuclei, not vowel segments. Welsh's template is `(C)(C)(C)N(C)(C)` where N
is a nucleus.

**C. DSL additions (§3).**
- Inline sets: `{l n r}` anywhere a single item is allowed.
- Captures and backreferences: any item in TARGET or environment may be suffixed `:n`
  (n = 1–9); REPLACEMENT may contain `\n`, which copies the segment matched by capture n.
  This expresses copy-epenthesis `0 -> \1 / V:1 C _ {l n r} #`, metathesis
  `θ:1 r:2 -> \2 \1 / C _ #`, and "C → C v" as `0 -> v / [C +back -labial] _ [V +front]`.
- Class names and `#`/`$` are allowed in TARGET only via captures (a class item must be
  captured to be reproduced); REPLACEMENT contains only literal segments, `0`, backreferences
  and a single feature-change bundle.
- Feature aliases: `features.csv` header may declare aliases (`ejective = raisedLarynxEjective`,
  `voice = periodicGlottalSource`, `long = long`, `emphatic = retractedTongueRoot`); bundles
  may use either name. Predeclared classes additionally include `LIQ`, `NAS`, `STOP`, `FRIC`,
  `GLIDE`, derived from features at load time.
- Feature-change bundles: **exact** vector lookup only; if no segment has the resulting
  vector, raise at `strands check` time (`UNREACHABLE_CHANGE`). Approximation happens only in
  the inventory fallback stage, never inside a rule.
- `[respell]`: operates over the annotated IPA token stream; quoted replacements become
  opaque output chunks that later rules do not rematch; `.` and `ˈ` are stripped in code
  after the rules, not by DSL lines. Rules may still reference `.`/`ˈ` in environments.

**D. Onset/coda sets (§3 `[syllable]`).** `onsets` and `codas` are complete sets of allowed
clusters **including singletons**; the empty onset/coda is always allowed unless
`onset-required = yes`. `any` remains available.

**E. Cluster fallback (Georgian).** A `[repair]` directive `cluster-fallback = same-length`
replaces an illegal onset/coda span by the attested cluster of the same length with minimal
summed segment feature distance (ties: list order), tagged `%fallback`; no candidate →
`UNREPAIRED`. Tests are synthetic (no attested example exists).

*Amended by owner decision, 2026-08-25 (Georgian only).* `cluster-fallback` takes a second
value, `keep`: the illegal onset/coda span is left exactly as it is, its illegal marks are
cleared so the repair loop terminates without `UNREPAIRED`, each span records a
`repair cluster-keep %design` trace entry and adds a `Result.flags` entry
`UNATTESTED_CLUSTER:<cluster>`. Nothing is substituted, so the fallback count does not move.
This is Georgian's policy per digest §3.7 (Georgian imports a foreign cluster intact rather
than repairing it); `same-length` remains Welsh's last resort. A span that is neither an
onset nor a coda is still left marked and still yields `UNREPAIRED`.

A second `[repair]` directive, `overlay-undo = <segment>`, runs before it: where a target
writes a secondary-articulation overlay as an epenthesis in `[substitute]` (Georgian's Cʷ,
`0 -> v / [BROAD -labial] _ [V +front]`) and that insertion is the only reason an onset is
unlicensed, the inserted segment is deleted again (`repair overlay-undo %design`) instead of
the cluster being repaired. If the onset is unlicensed without it too, the overlay is kept and
the span falls through to `cluster-fallback`. Provenance comes from `Word.origins`, which
`rewrite.apply_rule` fills for insertion rules only — a segment the input itself contained is
never undone.

**F. Segment spelling canon.** Canonical segment spellings are the digests' (`sˤ tʼ tʃ dʒ`,
plain `g`), not PHOIBLE's (`s̪ˤ t̪ʼ t̠ʃ d̠ʒ ɡ`). `features.csv` is built with a normalization
map from PHOIBLE spellings; the tokenizer accepts an alias table (ASCII `g`→`ɡ` is *not*
applied — `g` is canonical; `:`→`ː`, `'`→`ʼ` in ejective context, bracket stripping) for
reading attested data, and regression harnesses report untokenizable rows as skipped with
counts, never as errors.

**G. Corrections to §7.** Cairene: **no degemination** (geminates are phonemic); remove the
line. Georgian post-consonantal ejective and slender-coronal series are `%design` (decision
register 4 and 1), cited to §3.1/§8.1 as evidence, not as sourced rules. Welsh `ɣ→g`,
`x→χ` are `%design`. Cairene dot-under respelling is decision 11 (design), overriding the
digest's plain-letter recommendation.

**H. Input and CLI.** `declension` is inferred in the input stage (shape + gender, §5) and
recorded in `assumptions`. Target `[epithets]` are reachable through construction tags of the
form `DESC+ADJ` / `DESC+NOUN`: each target maps `ADJ` and `NOUN` to its own affix (Arabic
nisba / fem -a; Georgian -uri / -i; Welsh -aidd / none; Dutch -achtig / none).

**I. Plan discipline.** Every task, including the four target rule files, writes its tests
first against an absent or skeletal artefact; stress procedures live in separate modules
(`stress/initial.py`, …) so their tasks are conflict-free; the dependency graph must be
acyclic and honest about test fixtures (a test that needs another task's output depends on
that task).

**J. (added after re-check)** `BROAD` and `SLEN` are declared classes (ˠ-bearing consonants;
ʲ-bearing plus the palatals), copied into every rule file; rules that mean "Irish broad
consonant" write `BROAD`, never `[C +back]` (which under PHOIBLE vectors would exclude plain
dorsals and include uvulars/pharyngeals). Plain unmarked consonants have `front/back = 0`;
normalization rules that target them use an `UNMARKED` class, not feature bundles. `[inflect]`
contains whichever named regular inflections the plan enumerates (superset of the four in
§3). Welsh's template is one nucleus per syllable, as §12.B states; hiatus is two syllables.
The five pre-existing strand-4 names are canon inputs, displayed verbatim in the gallery's
reference row and never passed through the engine.

**K. (2026-08-27)** The input TSV has an optional `declension` column (`m1 | ach | f2 | m3 |
d4`). Supplied values are honoured and validated; when empty it is inferred and reported in
`assumptions`; `strands lint --accept` writes the inference back like `gender` and `gen_ipa`.
IPA cells may be wrapped in `/…/` or `[…]`.
