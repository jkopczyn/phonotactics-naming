# Strands engine — implementation plan (milestones 1–7)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development
> (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build `strands`, a deterministic CLI that adapts Irish (IPA) names and epithets into
four target-language strands (Southern Welsh, Cairene Arabic, Standard Georgian, Belgian Dutch)
via per-language rule files, emitting IPA + English-reader respelling + derivation trace.

**Architecture:** A small standard-library Python package. A feature table (`rules/features.tsv`)
gives every segment PHOIBLE-style features; a hand-written DSL parser reads one `.rules` file per
language into typed section objects; a rewrite engine applies ordered rules to an immutable
`Word`; a syllabifier + repair loop, stress procedures, and a respell stage complete the pipeline.
All linguistic content lives in data files (`rules/*.rules`), not in code.

**Tech Stack:** Python ≥3.12, `uv`, `pytest`. No runtime dependencies (standard library only).
Dev dependency: `pytest` only. Verified available on this machine: `uv 0.11.22`. **The system
`python3` is 3.10 — do not use it. Every command in this plan runs through `uv run`, which
downloads and pins CPython 3.12.**

**Spec:** `phonotactics/docs/specs/2026-08-25-engine-design.md` (source of truth; read it before
starting any task). Background: `phonotactics/notes/project-goals.md`. Linguistic content:
`phonotactics/sources/<lang>/digest.md`.

**Milestone 8 (provisional Irish G2P) is out of scope for this plan.**

## Global Constraints

- Python ≥3.12; package `strands` under `phonotactics/src/strands/`; `pyproject.toml` at
  `phonotactics/pyproject.toml`; CLI entry point named `strands`.
- No runtime dependencies outside the standard library. PanPhon/CLTS are rejected by the spec.
- All paths in this plan are relative to `phonotactics/` unless stated otherwise.
- Determinism is a hard requirement: no randomness, no set iteration order leaking into output,
  no dict ordering assumptions beyond insertion order. Identical input + rule files ⇒ byte-identical
  output.
- Test-first, always: write the failing test, run it, watch it fail, then implement. Tests are
  committed in the same commit as the code they cover.
- Every rule line in a target `.rules` file carries either a `# [bibkey p.N]` citation to its
  digest source or `# design: §9.n` naming the decision-register row (spec §7, §9).
- Rule tags are exactly one of `%attested`, `%design`, `%fallback`; default `%attested`.
- Files are UTF-8. IPA is stored NFC-normalized (see Interpretation I-1).

---

## Spec interpretations

The spec leaves the following underdetermined. Each is resolved here by the simplest reading;
implementers must follow these, not their own reading.

- **I-1 Unicode normalization.** All rule files, input TSVs and IPA strings are normalized with
  `unicodedata.normalize("NFC", s)` on read. Combining diacritics (`◌ˠ ◌ʲ ◌̪ ◌ˤ ◌ʼ`) are modifier
  letters, not combining marks, so NFC leaves them alone; this only regularizes stray composed
  characters. Comparison is on the NFC string.
- **I-2 Diphthongs are two segments, not one.** Irish /iə uə əi əu/ are tokenized as two vowel
  segments each. `features.tsv` therefore has no diphthong rows. Georgian's "diphthongs → V.V"
  (spec §7) is a syllabification/hiatus fact, not a substitution.
- **I-3 Comment vs word-edge `#`.** In a rewrite line *with* an environment, `#` inside the
  environment is always the word-edge symbol; the environment runs to end-of-line or to the
  `%tag`. Consequence: **a rewrite line that has an environment and wants a comment must write
  the `%tag` explicitly.** A line without `/` may use `#` for a comment freely. The parser raises
  `ParseError("comment after environment requires an explicit %tag", line)` if it sees `#`
  followed by a space inside an untagged environment.
- **I-4 Bundle syntax.** A bundle is `[` optional class-name, then zero or more `±feature` `]`,
  with at least one element total. On the **left** (target/context) it is a *match* bundle. On the
  **right** (replacement) `[...]` is always a *feature-change* bundle and may not contain a class
  name; it applies to every segment the target matched, and the result must exist in
  `features.tsv` (else `RuleError` naming the rule id).
- **I-5 Mixed targets.** `TARGET` is a sequence of items, each a segment / class name / match
  bundle; mixing is allowed. `REPLACEMENT` may have a different length than `TARGET`; the whole
  matched span is replaced by the whole replacement sequence.
- **I-6 Simultaneous application.** For one rule: scan the *pre-rule* segment string left to
  right, collecting non-overlapping matches (greedy, leftmost-longest at each position); evaluate
  all contexts against the pre-rule string; then apply all replacements at once. One trace entry
  per rule that changed anything (recording the whole word before/after), not per match.
- **I-7 Epenthesis.** A rule with `TARGET = 0` inserts at every position where the environment
  matches. Such a rule **must** have a non-empty environment on at least one side; `strands check`
  reports `0 -> X` with an empty environment as an error. Insertion positions are also
  non-overlapping (one insertion per position, positions taken from the pre-rule string).
- **I-8 `.` and `ˈ` are context-only.** Syllable boundary `.`, stress mark `ˈ`, word edge `#` and
  morpheme edge `$` may appear only in environments (and in `[syllable] bans`), never in a target
  or a replacement.
- **I-9 `()` and `*`.** Both attach to exactly one context atom, are not nestable, and do not
  combine with each other (`(X)*` is a parse error). `X*` matches zero or more adjacent `X`.
- **I-10 Class names vs segments.** Class names match `[A-Z][A-Z0-9_]*`. No IPA segment matches
  that pattern, so the parser can tell them apart without a lookup. `C` and `V` are predeclared.
- **I-11 `C` and `V` contents.** `C` = every segment in this file's `[inventory]` with
  `consonantal=+` or (`syllabic=-` and `sonorant=+`, i.e. glides), **plus** every Irish consonant
  (the Irish inventory list of Task 1). `V` likewise for vowels (`syllabic=+`). Computed at load
  time from `features.tsv`; a redeclaration of `C` or `V` in `[classes]` overrides it.
- **I-12 Feature distance.** `distance(a, b) = Σ weight[f]` over features `f` where both `a` and
  `b` are defined (`+`/`-`, not `0`) and differ. Weights default to `1.0`; `[weights]` lines
  override per feature. Undefined-vs-defined contributes 0. Ties in the fallback search are broken
  by `[inventory]` declaration order (first wins).
- **I-13 Sonority scale** (used when `sonority = on`), fixed in code, documented in
  `src/strands/syllabify.py`: vowel 5 > glide 4 > liquid (lateral or rhotic) 3 > nasal 2 >
  fricative 1 > stop/affricate 0, computed from features. Onsets must be strictly rising, codas
  strictly falling; equal-sonority adjacency is illegal. `sC` clusters are exempt from the check
  (a universal exemption, matching every source's treatment of /s/+stop).
- **I-14 `[syllable] bans` lines** are one context sequence per line, each ban a sequence of
  atoms (segments/classes/bundles/`#`/`$`/`.`); a parse whose segment string contains the sequence
  is illegal, and the matched span is what gets marked illegal.
- **I-15 Named sub-tables** in `[mutations]` and `[inflect]` are introduced by a bare
  `NAME:` line (e.g. `LEN:`) and run until the next `NAME:` line or the next `[section]`. Their
  bodies are ordinary rewrite lines.
- **I-16 `[templates]` grammar.** `NAME = item { item }`, where an item is a quoted literal
  (`"a"`, and `" "` = word separator), an argument name (`NAME FATHER NOUN ADJ FIRST SECOND`), or
  `FUNC(item)` with `FUNC ∈ {LEN, ECL, HPREF, TPREF, GEN, VOC_M1, ART, LEN_IF_F}`; a trailing `?`
  on an item means "apply only if the entry's declension/gender tag licenses it" (spec §3's
  `VOC_M1?` = only for class m1). Every join between items inserts `$`; `" "` splits the result
  into separate words that the target adapts independently and the output rejoins with a space.
- **I-17 `[stress]` parameters** are `key = value` lines after `procedure = X`; unknown keys are a
  `check` error. Each procedure documents its own keys (Task 12–15).
- **I-18 `[epithets]` form** is `NAME = <segment tokens> / <environment>`; the environment uses
  the same grammar as a rewrite environment and states where the affix attaches.
- **I-19 `[respell]` replacement** is a double-quoted string (may be empty `""`); its target and
  environment use the ordinary rewrite grammar. Output of the respell stage is a plain string, so
  `[respell]` rules apply over a string that still carries `.` and `ˈ` marks; a final cleanup rule
  set removes any remaining marks (each target's file ends with `. -> ""` and `ˈ -> ""` unless it
  wants to keep them).
- **I-20 `features.tsv` may carry extra non-feature columns** (`segment`, `class`, `source`).
  Only the 38 PHOIBLE feature columns take part in distance. Inventories live in the rule files,
  never in `features.tsv`; the table is the union across all five languages.
- **I-21 Trace ids.** `rule_id` is `"<section>:<line-number>"` within its rule file (e.g.
  `repair:87`), which is stable, unique, and points a reader at the citation comment.
- **I-22 Regression "pass"** means exact string equality of the pipeline's IPA output with
  `target_ipa` after NFC normalization and after stripping stress marks, syllable dots and length
  marks that the attested source did not record. The harness additionally reports a segment-level
  edit distance so near-misses are visible.
- **I-23 Marginal segments** are legal in `[inventory]` and in output, but the fallback search in
  Task 9 never selects them.
- **I-24 Unknown segment on input** is a hard error (`SegmentError`) naming the word and the
  offending substring, per spec §2 — including inside rule files.

- **I-25 The attested data cannot support the spec's §8.3 regression as written.** Verified row
  counts: `sources/georgian/attested.tsv` 143 rows, **0** with `source_ipa`;
  `sources/arabic-egy/attested.tsv` 312 rows (301 real + 11 tagged `PREDICTED-NOT-ATTESTED:`),
  **0** with `source_ipa`; `sources/welsh/attested.tsv` 751 rows, **0** with `source_ipa` and only
  **19** with `target_ipa`; `sources/dutch/attested.tsv` 90 rows, **32** with both sides in IPA.
  So "run the attested source forms through stages 2–7 and compare" is only possible for Dutch.
  Resolution — the regression harness (Task 22) implements two modes and every target task uses
  both:
  - **Mode E (end-to-end)**, for rows with both `source_ipa` and `target_ipa`: run stages 2–7 and
    compare (I-22). Dutch only, 32 rows.
  - **Mode L (legality conformance)**, for rows with `target_ipa` only: the attested *target* form
    must be accepted by the rule file — every segment in `[inventory]`, the whole word
    syllabifiable with no illegal span, no `bans` violation, and (where the row records a stress
    mark) the file's stress procedure must reproduce it. This is a real regression on the
    inventory/phonotactics half of each rule file and it uses the data that actually exists.
  A rule file's syllable/inventory sections are wrong if Mode L fails on attested native/loan
  forms, so this catches most transcription errors.
- **I-26 "Awbery's tree" (spec §7, Welsh) does not exist in the digest.** `sources/welsh/digest.md`
  §4.3 gives the Southern length rule as a **7-row environment table**, and the Awbery 1984 text
  extract committed on 2026-08-25 is not yet folded into the digest. Task 25 encodes the §4.3
  table as `[post-stress]` rules and leaves spec §11's open item open. Do not invent a tree.
- **I-27 Georgian has no syllable template** (`digest.md` §2.1 denies the syllable is the domain).
  `georgian.rules [syllable]` therefore uses `template = any`, `domain = stem`, `sonority = off`
  (§2.7: sonority is explicitly not relevant), and whitelists from §2.2 (32 harmonic clusters,
  table (53)), §2.3 (Appendix 2 stem-initial list) and §2.5 (Appendix 3 stem-final list).
- **I-28 Cairene has no licit onset clusters** (`digest.md` §2 "Onsets"): `onsets = any` is wrong;
  the file lists every single consonant as an onset and nothing longer. Template is
  `C V (C) (C)` with the second coda C word-final only, encoded as `template = CV(C)(C)` plus a
  ban on medial CC codas.
- **I-29 Open decisions in the digests that the spec's §9 register does not cover** are resolved
  by the *spec's* §7 text where it speaks (e.g. Georgian /p t k/ → aspirate, ejective after C;
  Arabic /ŋ/ → n), and otherwise by taking the digest's own "measured"/majority option and
  tagging the rule `%design` with a `# design: digest §N open` comment. No rule may be left out
  because a source is undecided.
- **I-30 Irish input aliases.** `features.tsv` carries rows for `lˠ l̠ʲ nˠ n̠ʲ` (Irish digest §1.1)
  with features identical to `l̪ˠ lʲ n̪ˠ nʲ`, and `irish.rules [normalize]` folds them onto the
  two-way system. `ɑ` and `ɑː` also get rows (they occur in the user's own transcriptions,
  e.g. *Lasairchos* /ˈl̪ˠɑsˠəɾʲxosˠ/) and normalize onto `a` / `aː`.

---

## DSL grammar (EBNF)

The parser in Task 5 must implement exactly this. `SEGMENT` is a maximal whitespace-delimited run
of non-reserved characters that tokenizes (longest-match, Task 3) into one or more `features.tsv`
segments; where the grammar says `SEGMENT` a single segment is required, where it says `CLUSTER` a
run of segments written without spaces is allowed.

```ebnf
file           = { line } ;
line           = section-header | entry | comment-line | blank-line ;
comment-line   = ws , "#" , { any-char } ;
section-header = ws , "[" , section-name , "]" , ws , [ comment ] ;
section-name   = "meta" | "inventory" | "classes" | "weights" | "substitute"
               | "syllable" | "repair" | "post-stress" | "stress" | "epithets"
               | "respell" | "templates" | "mutations" | "inflect" | "normalize" ;

(* ---- rewrite sections: substitute, repair, post-stress, respell,
        mutations, inflect, normalize ---- *)
rewrite        = target , "->" , replacement , [ "/" , environment ] ,
                 [ tag ] , [ comment ] ;
target         = "0" | item , { item } ;
item           = SEGMENT | class-name | match-bundle ;
match-bundle   = "[" , [ class-name ] , { feature-spec } , "]" ;   (* >= 1 element *)
feature-spec   = ( "+" | "-" | "0" ) , feature-name ;
replacement    = "0" | change-bundle | out-item , { out-item } ;
out-item       = SEGMENT | quoted ;        (* quoted only inside [respell] *)
change-bundle  = "[" , feature-spec , { feature-spec } , "]" ;
environment    = [ ctx-seq ] , "_" , [ ctx-seq ] ;
ctx-seq        = ctx-item , { ctx-item } ;
ctx-item       = ctx-atom | "(" , ctx-atom , ")" | ctx-atom , "*" ;
ctx-atom       = SEGMENT | class-name | match-bundle | "#" | "$" | "." | "ˈ" ;
tag            = "%attested" | "%design" | "%fallback" ;
comment        = "#" , { any-char } ;
class-name     = uppercase , { uppercase | digit | "_" } ;
feature-name   = lowercase , { letter } ;                (* PHOIBLE column name *)
quoted         = '"' , { any-char - '"' } , '"' ;

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
               | "onsets" , "=" , ( cluster-list | "any" )
               | "codas"  , "=" , ( cluster-list | "any" )
               | "onsets-tier" , "=" , tiered-list
               | "codas-tier"  , "=" , tiered-list
               | "appendix" , "=" , SEGMENT , { SEGMENT }
               | "domain" , "=" , ( "word" | "stem" )
               | "sonority" , "=" , ( "on" | "off" )
               | "bans" , "=" , ctx-seq ;                (* repeatable *)
tpl-seq        = tpl-item , { tpl-item } ;
tpl-item       = slot | "(" , slot , ")" ;
slot           = "C" | "V" | class-name ;
cluster-list   = CLUSTER , { CLUSTER } ;
tiered-list    = CLUSTER , ":" , tier , { CLUSTER , ":" , tier } ;
tier           = uppercase , { uppercase | digit } ;

(* ---- [stress] ---- *)
stress-entry   = "procedure" , "=" , proc-name | key , "=" , value ;
proc-name      = "initial" | "penult" | "cairene" | "dutch-weight" | "keep-source" ;

(* ---- [epithets] ---- *)
epithet-entry  = name , "=" , SEGMENT , { SEGMENT } , "/" , environment ;

(* ---- [templates] ---- *)
tpl-entry      = name , "=" , t-item , { t-item } ;
t-item         = ( quoted | arg-name | func-call ) , [ "?" ] ;
arg-name       = "NAME" | "FATHER" | "NOUN" | "ADJ" | "FIRST" | "SECOND" ;
func-call      = func-name , "(" , t-item , ")" ;
func-name      = "LEN" | "ECL" | "HPREF" | "TPREF" | "GEN" | "VOC_M1"
               | "ART" | "LEN_IF_F" ;

(* ---- [mutations] and [inflect]: named sub-tables ---- *)
subtable-head  = name , ":" ;
```

Reserved characters that may not occur inside a `SEGMENT`: whitespace, `[ ] ( ) / _ # $ % " : =`,
`->`, `*`, `.`, `ˈ`, `+`, `-`, `0`. (Note: `-` and `0` are reserved only at the start of a token.)

---

## File structure

```
phonotactics/
  pyproject.toml                  # Task 0
  src/strands/
    __init__.py                   # Task 0
    cli.py                        # Task 0 stub; Task 26 full
    features.py                   # Task 2: FeatureTable, distance
    tokenize.py                   # Task 3: longest-match tokenizer, marks
    dsl.py                        # Task 5: parser -> RuleFile dataclasses
    check.py                      # Task 6: static checks
    word.py                       # Task 4: Word, TraceEntry
    rewrite.py                    # Task 7: rule matching + application
    substitute.py                 # Task 8-9: substitute stage + fallback
    syllabify.py                  # Task 10: parser, legality, illegal spans
    repair.py                     # Task 11: repair loop
    stress.py                     # Tasks 12-15: procedures registry
    poststress.py                 # Task 16
    irish.py                      # Tasks 17-19: mutations, inflect, templates, normalize
    inputs.py                     # Task 20: TSV read, inference, lint
    pipeline.py                   # Task 21: stage orchestration
    respell.py                    # Task 21
    regress.py                    # Task 22: attested-data regression harness
    gallery.py                    # Task 27
  rules/
    features.tsv                  # Task 1
    build_features.py             # Task 1 (build script, not part of the package)
    irish.rules                   # Tasks 17-19
    georgian.rules                # Task 23
    arabic-egy.rules              # Task 24
    welsh.rules                   # Task 25
    dutch.rules                   # Task 26
  tests/                          # one test module per task, named below
    ratchets/<target>.json        # Task 22+
    snapshots/gallery.md          # Task 28
```

---

## Task list and dependencies

| # | Task | Depends on |
|---|---|---|
| 0 | Project scaffold, `pyproject.toml`, CLI stub | — |
| 1 | `rules/features.tsv` + build script | 0 |
| 2 | Feature table loader + distance | 1 |
| 3 | Tokenizer | 2 |
| 4 | `Word` model + trace | 3 |
| 5 | DSL parser | 3 |
| 6 | `strands check` static checks | 5 |
| 7 | Rewrite engine | 4, 5 |
| 8 | Substitute stage | 7 |
| 9 | Inventory fallback | 8 |
| 10 | Syllabifier | 4, 5 |
| 11 | Repair loop | 7, 10 |
| 12 | Stress framework + `initial` + `keep-source` | 4, 5 |
| 13 | `penult` procedure | 12 |
| 14 | `cairene` procedure | 12 |
| 15 | `dutch-weight` procedure | 12 |
| 16 | Post-stress stage | 7, 12 |
| 17 | Irish mutations + inflections | 7 |
| 18 | Irish templates | 17, 20 |
| 19 | Irish `[normalize]` | 7 |
| 20 | Input TSV + inference + `lint` | 4 |
| 21 | Pipeline orchestrator + respell + epithet stage | 9, 11, 13, 14, 15, 16, 18, 19 |
| 22 | Regression harness + ratchet | 21 |
| 23 | `georgian.rules` | 21, 22 |
| 24 | `arabic-egy.rules` | 21, 22 |
| 25 | `welsh.rules` | 21, 22 |
| 26 | `dutch.rules` | 21, 22 |
| 27 | CLI `run` / `explain` / `gallery` / `lint` | 21, 20 |
| 28 | Gallery snapshot + property checks | 27, 23, 24, 25, 26 |

Tasks 13/14/15 are mutually independent (parallel after 12). Tasks 23/24/25/26 are mutually
independent (parallel after 22). Tasks 17, 19 and 20 are mutually independent; Task 18 needs both 17 and 20.

---

## Task 0: Project scaffold and CLI stub

**Files:**
- Create: `phonotactics/pyproject.toml`
- Create: `phonotactics/src/strands/__init__.py`
- Create: `phonotactics/src/strands/cli.py`
- Create: `phonotactics/tests/test_cli_stub.py`
- Create: `phonotactics/.gitignore` (add `.venv/`, `__pycache__/`, `*.pyc`, `.pytest_cache/`)

**Interfaces:**
- Consumes: nothing.
- Produces: `strands.__version__: str`; `strands.cli.main(argv: list[str] | None = None) -> int`.
  Console script `strands = "strands.cli:main"`.

- [ ] **Step 1: Write the failing test** — `phonotactics/tests/test_cli_stub.py`

```python
import subprocess, sys

def test_main_reports_version(capsys):
    from strands.cli import main
    assert main(["--version"]) == 0
    assert "strands" in capsys.readouterr().out

def test_main_unknown_command_returns_2():
    from strands.cli import main
    assert main(["frobnicate"]) == 2

def test_console_script_runs():
    out = subprocess.run(["uv", "run", "strands", "--version"],
                         capture_output=True, text=True, cwd="..")
    assert out.returncode == 0
```

(The third test's `cwd=".."` assumes pytest runs from `phonotactics/`; use
`cwd=pathlib.Path(__file__).parents[1]` instead — write it that way.)

- [ ] **Step 2: Run it and watch it fail**

Run: `cd phonotactics && uv run pytest tests/test_cli_stub.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'strands'`.

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

Also write `.python-version` containing `3.12` so `uv` pins the interpreter (the system
`python3` is 3.10 and must not be used).

- [ ] **Step 4: Write the CLI stub** — `src/strands/cli.py`

```python
"""Command-line entry point. Subcommands are added in Task 27."""
from __future__ import annotations
import argparse, sys
from . import __version__

COMMANDS = ("run", "explain", "gallery", "lint", "check")

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="strands", add_help=True)
    p.add_argument("--version", action="store_true")
    p.add_argument("command", nargs="?", choices=COMMANDS)
    p.add_argument("args", nargs=argparse.REMAINDER)
    return p

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

- [ ] **Step 5: Run tests to verify they pass**

Run: `cd phonotactics && uv run pytest -v` — expected: 3 passed.

- [ ] **Step 6: Commit**

```bash
git add phonotactics/pyproject.toml phonotactics/.python-version phonotactics/.gitignore \
        phonotactics/src/strands phonotactics/tests
git commit -m "chore(strands): scaffold uv/pytest package and CLI stub"
```

**Acceptance:** `uv run pytest` passes from `phonotactics/`; `uv run strands --version` prints a
version; no non-stdlib runtime dependency appears in `pyproject.toml`.

---

## Task 1: `rules/features.tsv` and its build script

**Depends on:** Task 0

**Files:**
- Create: `phonotactics/rules/build_features.py` (a standalone script, not imported by the package)
- Create: `phonotactics/rules/features.tsv` (generated by the script, then hand-extended, then
  committed — the committed file is the artefact; the script exists so the PHOIBLE half is
  reproducible)
- Create: `phonotactics/tests/test_features_table.py`

**Interfaces:**
- Produces: `rules/features.tsv`, a TSV whose header is
  `segment<TAB>class<TAB>source<TAB>` + the 38 PHOIBLE feature column names in PHOIBLE order
  (`tone stress syllabic short long consonantal sonorant continuant delayedRelease approximant
  tap trill nasal lateral labial round labiodental coronal anterior distributed strident dorsal
  high low front back tense retractedTongueRoot advancedTongueRoot periodicGlottalSource
  epilaryngealSource spreadGlottis constrictedGlottis fortis lenis raisedLarynxEjective
  loweredLarynxImplosive click`). `class` ∈ {`C`, `V`}. `source` is `phoible:<InvID>` or
  `hand:irish` or `hand:diacritic`.
- `build_features.py` exposes `main(csv_path, out_path) -> None` and is run as
  `uv run python rules/build_features.py chat-imports/phoible_inventories_starter.csv rules/features.tsv`.

**How the rows are derived (follow exactly):**

1. **PHOIBLE half.** Read `chat-imports/phoible_inventories_starter.csv` (153 data rows, 4
   inventories: Dutch 2169, Georgian 2183, Arabic-egy 231, Welsh 2406). For each row take
   `Phoneme` as `segment`, `SegmentClass` (`consonant`→`C`, `vowel`→`V`) as `class`, and the 38
   feature columns verbatim. Drop `Language/InventoryID/Source/SpecificDialect/Allophones/
   Marginal` (marginality is per-rule-file, spec §3 `[inventory] marginal:`).
2. **De-duplicate across inventories.** The same `Phoneme` string appears in several inventories.
   If all occurrences have identical 38-feature vectors, emit one row with
   `source = phoible:<first InvID encountered, in file order>`. If they differ, the script
   **fails loudly**, printing segment + differing feature names, and the plan's author resolves it
   by hand — do not silently pick one. (Expected: no conflicts; PHOIBLE features are
   segment-derived.)
3. **Ordering.** Rows sorted by `class` (`C` before `V`) then by `segment` code points, so the
   file is stable across rebuilds.
4. **Irish half, added by hand** (`source = hand:irish`), from `sources/irish/digest.md` §1.1–§1.2.
   The 31 consonants: `pˠ pʲ bˠ bʲ t̪ˠ tʲ d̪ˠ dʲ k c ɡ ɟ fˠ fʲ sˠ ʃ x ç h w vʲ ɣ j mˠ mʲ n̪ˠ nʲ
   ŋ ɲ l̪ˠ lʲ ɾˠ ɾʲ`. The 11 vowels: `iː eː aː uː oː ɪ ɛ a ʊ ɔ ə`. Aliases (I-30): `lˠ l̠ʲ nˠ n̠ʲ
   ɑ ɑː`. No diphthong rows (I-2).
5. **Derivation procedure for each hand row** — mechanical, so it can be checked:
   a. Start from the PHOIBLE row for the **plain base symbol** with the diacritics stripped
      (`tʲ` → `t`, `t̪ˠ` → `t`, `l̪ˠ` → `l`, `ɾʲ` → `ɾ`, `aː` → `a`). If the base is absent from
      the PHOIBLE half (`ɡ`, `c`, `ɟ`, `ɲ`, `ɾ`, `ç`, `ɣ`, `w`, `x` — check before assuming),
      copy the nearest PHOIBLE row of the same manner and re-set place features by hand,
      recording which row was used in a comment line at the top of the hand block.
   b. Apply the spec §2 diacritic conventions, in this order:
      - `ʲ` (slender): `front=+`, `back=-`, `high=+`
      - `ˠ` (broad): `back=+`, `front=-`
      - `̪` (dental): `anterior=+`, `distributed=+`
      - `ː` (long): `long=+`, `short=-`
      - `ʼ` (ejective): `raisedLarynxEjective=+`, `constrictedGlottis=+`
      - `ˤ` (emphatic): `retractedTongueRoot=+`, `back=+`
      - `ʰ` (aspirated): `spreadGlottis=+`
      These same conventions cover the target-side diacritic segments (`tʼ`, `sˤ`, `kʰ`) that
      PHOIBLE already supplies — check them against the PHOIBLE rows and, if PHOIBLE disagrees,
      **keep PHOIBLE's values** and note the divergence in the file header comment.
   c. `k c ɡ ɟ` carry the broad/slender contrast without a diacritic (digest §1.1): give `k ɡ`
      `back=+ front=-` and `c ɟ ɲ` `front=+ back=- high=+`.
   d. Alias rows copy their principal's vector exactly.
6. **Header comment.** `features.tsv` may not carry comments (it is read as a plain TSV), so put
   the derivation notes in a sibling `rules/features.README.md`, ≤40 lines, listing the base row
   used for each hand segment.

- [ ] **Step 1: Write the failing test** — `tests/test_features_table.py`

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

IRISH_CONSONANTS = "pˠ pʲ bˠ bʲ t̪ˠ tʲ d̪ˠ dʲ k c ɡ ɟ fˠ fʲ sˠ ʃ x ç h w vʲ ɣ j mˠ mʲ n̪ˠ nʲ ŋ ɲ l̪ˠ lʲ ɾˠ ɾʲ".split()
IRISH_VOWELS = "iː eː aː uː oː ɪ ɛ a ʊ ɔ ə".split()

def rows():
    with FEATURES.open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))

def test_header_is_segment_class_source_plus_38_phoible_features():
    with FEATURES.open(encoding="utf-8") as fh:
        header = fh.readline().rstrip("\n").split("\t")
    assert header[:3] == ["segment", "class", "source"]
    assert header[3:] == PHOIBLE_38

def test_no_duplicate_segments():
    segs = [r["segment"] for r in rows()]
    assert len(segs) == len(set(segs))

def test_every_irish_segment_present():
    segs = {r["segment"] for r in rows()}
    for s in IRISH_CONSONANTS + IRISH_VOWELS:
        assert s in segs, s

def test_feature_values_are_plus_minus_or_zero():
    for r in rows():
        for f in PHOIBLE_38:
            assert r[f] in {"+", "-", "0"}, (r["segment"], f, r[f])

def test_slender_and_broad_conventions():
    by = {r["segment"]: r for r in rows()}
    assert (by["tʲ"]["front"], by["tʲ"]["back"]) == ("+", "-")
    assert (by["t̪ˠ"]["back"], by["t̪ˠ"]["front"]) == ("+", "-")
    assert by["t̪ˠ"]["anterior"] == "+" and by["t̪ˠ"]["distributed"] == "+"
    assert by["aː"]["long"] == "+" and by["aː"]["short"] == "-"

def test_broad_slender_pairs_differ_only_in_tongue_body_features():
    by = {r["segment"]: r for r in rows()}
    for broad, slender in [("t̪ˠ", "tʲ"), ("pˠ", "pʲ"), ("mˠ", "mʲ"), ("k", "c")]:
        differing = {f for f in PHOIBLE_38 if by[broad][f] != by[slender][f]}
        assert differing <= {"front", "back", "high", "anterior", "distributed",
                             "coronal", "dorsal", "delayedRelease", "strident"}, (broad, slender, differing)

def test_ejective_and_emphatic_conventions():
    by = {r["segment"]: r for r in rows()}
    assert by["tʼ"]["raisedLarynxEjective"] == "+"          # Georgian, from PHOIBLE
    assert by["sˤ"]["retractedTongueRoot"] == "+" and by["sˤ"]["back"] == "+"   # Cairene

def test_aliases_match_their_principals():
    by = {r["segment"]: r for r in rows()}
    for alias, principal in [("lˠ", "l̪ˠ"), ("l̠ʲ", "lʲ"), ("nˠ", "n̪ˠ"), ("n̠ʲ", "nʲ"),
                             ("ɑ", "a"), ("ɑː", "aː")]:
        assert {f: by[alias][f] for f in PHOIBLE_38} == {f: by[principal][f] for f in PHOIBLE_38}

def test_class_column_matches_syllabic():
    for r in rows():
        assert r["class"] in {"C", "V"}
        if r["class"] == "V":
            assert r["syllabic"] == "+"
```

- [ ] **Step 2: Run and watch it fail** — `uv run pytest tests/test_features_table.py -v`,
  expected FAIL (file not found).

- [ ] **Step 3: Write `rules/build_features.py`** implementing steps 1–3 above (PHOIBLE half only),
  run it, then hand-append the Irish/alias rows per step 4–5 and re-sort with the script's
  `--sort-only` flag so the committed file is in canonical order.

- [ ] **Step 4: Run the tests** — all pass. Also assert by eye: `wc -l rules/features.tsv` should be
  roughly 110 (PHOIBLE unique) + 48 (Irish + aliases) + 1 header ≈ 155–165. Record the exact count
  in `rules/features.README.md`.

- [ ] **Step 5: Commit**

```bash
git add phonotactics/rules/features.tsv phonotactics/rules/features.README.md \
        phonotactics/rules/build_features.py phonotactics/tests/test_features_table.py
git commit -m "feat(rules): features.tsv — PHOIBLE targets plus hand-derived Irish segments"
```

**Acceptance:** every Irish and target segment named in spec §7 has a row; the diacritic
conventions of spec §2 hold; rebuilding the PHOIBLE half from the CSV is byte-stable.

---

## Task 2: Feature table loader and distance

**Depends on:** Task 1

**Files:**
- Create: `phonotactics/src/strands/features.py`
- Create: `phonotactics/tests/test_features.py`

**Interfaces:**
- Consumes: `rules/features.tsv` (Task 1).
- Produces:

```python
FEATURE_NAMES: tuple[str, ...]          # the 38 PHOIBLE names, in file order

class FeatureTable:
    segments: tuple[str, ...]           # in file order
    def __contains__(self, segment: str) -> bool: ...
    def value(self, segment: str, feature: str) -> str: ...      # "+", "-", "0"
    def vector(self, segment: str) -> tuple[str, ...]
    def segment_class(self, segment: str) -> str                 # "C" or "V"
    def matches(self, segment: str, constraints: dict[str, str]) -> bool
    def apply_changes(self, segment: str, changes: dict[str, str]) -> str
        """Return the segment whose vector equals `segment`'s with `changes` applied.
        Raises FeatureError if no such segment exists in the table."""
    def distance(self, a: str, b: str, weights: dict[str, float] | None = None) -> float
    def nearest(self, segment: str, candidates: Sequence[str],
                weights: dict[str, float] | None = None) -> str
        """Lowest distance; ties broken by position in `candidates` (I-12)."""

def load_features(path: str | Path) -> FeatureTable: ...
class FeatureError(Exception): ...
```

- [ ] **Step 1: Write the failing test** — `tests/test_features.py`

```python
import pytest, pathlib
from strands.features import load_features, FeatureError, FEATURE_NAMES

TABLE = load_features(pathlib.Path(__file__).parents[1] / "rules" / "features.tsv")

def test_loads_all_segments_in_file_order():
    assert "t̪ˠ" in TABLE and "ʃ" in TABLE
    assert TABLE.segments.index("t̪ˠ") < TABLE.segments.index("a") or True  # order is C then V

def test_value_and_vector():
    assert TABLE.value("tʲ", "front") == "+"
    assert len(TABLE.vector("tʲ")) == len(FEATURE_NAMES) == 38

def test_distance_counts_defined_disagreements():
    # identical segments are distance 0
    assert TABLE.distance("k", "k") == 0
    # slender vs broad velar differ only in tongue-body features
    assert 0 < TABLE.distance("k", "c") <= 4

def test_distance_ignores_undefined_features():
    # a feature that is "0" on either side never contributes
    d = TABLE.distance("h", "k")
    manual = sum(1 for f in FEATURE_NAMES
                 if TABLE.value("h", f) in "+-" and TABLE.value("k", f) in "+-"
                 and TABLE.value("h", f) != TABLE.value("k", f))
    assert d == manual

def test_distance_honours_weights():
    plain = TABLE.distance("k", "c")
    weighted = TABLE.distance("k", "c", weights={"front": 10.0})
    assert weighted > plain

def test_nearest_breaks_ties_by_candidate_order():
    # two candidates equidistant from the query -> the earlier one wins
    cands = ["t", "d"]
    first = TABLE.nearest("t̪ˠ", cands)
    assert first == "t"
    assert TABLE.nearest("t̪ˠ", ["d", "t"]) in {"d", "t"}

def test_matches_constraints():
    assert TABLE.matches("tʲ", {"front": "+", "consonantal": "+"})
    assert not TABLE.matches("tʲ", {"back": "+"})

def test_apply_changes_returns_an_existing_segment():
    assert TABLE.apply_changes("k", {"raisedLarynxEjective": "+"}) == "kʼ"

def test_apply_changes_raises_when_no_segment_has_that_vector():
    with pytest.raises(FeatureError):
        TABLE.apply_changes("h", {"lateral": "+", "trill": "+"})

def test_unknown_segment_raises():
    with pytest.raises(FeatureError):
        TABLE.value("QQ", "front")
```

- [ ] **Step 2: Run and watch it fail.**
- [ ] **Step 3: Implement `features.py`.** Notes for the implementer:
  `apply_changes` searches `self.segments` in file order for the first segment whose vector equals
  the modified vector **on the changed features and on all features where the source is defined**;
  the practical implementation is: build the modified vector, look it up in a dict keyed by the
  full vector; if absent, fall back to `nearest` restricted to segments satisfying `changes`, and
  if that set is empty raise `FeatureError`. Cache the vector→segment dict at load.
- [ ] **Step 4: Run — all pass.**
- [ ] **Step 5: Commit** — `feat(strands): feature table loader with weighted feature distance`

**Acceptance:** distance is symmetric, zero on identity, ignores `0`; `nearest` is deterministic.

---

## Task 3: Tokenizer

**Depends on:** Task 2

**Files:**
- Create: `phonotactics/src/strands/tokenize.py`
- Create: `phonotactics/tests/test_tokenize.py`

**Interfaces:**

```python
MARKS = {"ˈ": "stress", ".": "syllable", "$": "morpheme", " ": "space"}

@dataclass(frozen=True)
class Tokenized:
    segments: tuple[str, ...]
    stress_index: int | None          # index of the segment starting the stressed syllable
    syllable_starts: tuple[int, ...]  # segment indices, from explicit "." marks (may be empty)
    morphemes: frozenset[int]         # positions (0..len) carrying "$"

def tokenize(text: str, table: FeatureTable) -> Tokenized
    """Longest-match against table.segments; NFC-normalize first (I-1);
    consume MARKS into annotations. Raises SegmentError naming text and the
    offending substring for anything else."""

def detokenize(segments: Sequence[str]) -> str
class SegmentError(Exception): ...
```

- [ ] **Step 1: Write the failing test** — `tests/test_tokenize.py`

```python
import pytest, pathlib
from strands.features import load_features
from strands.tokenize import tokenize, detokenize, SegmentError

TABLE = load_features(pathlib.Path(__file__).parents[1] / "rules" / "features.tsv")

def test_longest_match_prefers_diacritic_segments():
    t = tokenize("t̪ˠaː", TABLE)
    assert t.segments == ("t̪ˠ", "aː")          # not ("t", "aː") and not ("t̪", "ˠ", ...)

def test_user_transcription_of_lasairchos():
    t = tokenize("ˈl̪ˠɑsˠəɾʲxosˠ", TABLE)
    assert t.segments == ("l̪ˠ", "ɑ", "sˠ", "ə", "ɾʲ", "x", "o" if "o" in TABLE else "ɔ", "sˠ")
    assert t.stress_index == 0

def test_syllable_dots_recorded_and_removed():
    t = tokenize("ˈkɪə.ɾˠə", TABLE)
    assert "." not in t.segments
    assert t.syllable_starts == (0, 3)
    assert t.stress_index == 0

def test_morpheme_boundaries_are_positions_between_segments():
    t = tokenize("a$vʲ", TABLE)
    assert t.segments == ("a", "vʲ")
    assert t.morphemes == frozenset({1})

def test_unknown_segment_raises_with_the_offending_substring():
    with pytest.raises(SegmentError) as e:
        tokenize("kQa", TABLE)
    assert "Q" in str(e.value)

def test_detokenize_round_trips():
    assert detokenize(tokenize("mˠat̪ˠaːnˠəx", TABLE).segments) == "mˠat̪ˠaːnˠəx"

def test_nfc_normalization_is_applied():
    # decomposed vs precomposed input tokenize identically
    import unicodedata
    s = "aː"
    assert tokenize(s, TABLE).segments == tokenize(unicodedata.normalize("NFD", s), TABLE).segments
```

*(Note for the implementer: in `test_user_transcription_of_lasairchos`, decide from
`features.tsv` whether the short back mid vowel is `o` or `ɔ` and write the literal expectation —
do not leave the conditional expression in the committed test.)*

- [ ] **Step 2: Run, watch it fail.**
- [ ] **Step 3: Implement.** Longest-match: precompute the maximum segment length and try
  descending lengths at each position; marks are checked before segments.
- [ ] **Step 4: Run — pass.**
- [ ] **Step 5: Commit** — `feat(strands): longest-match IPA tokenizer with mark annotations`

**Acceptance:** every IPA string in `sources/irish/test-words.tsv` column `ipa` tokenizes without
error — add that as a final test reading the TSV (144 rows) and asserting no `SegmentError`.

---

## Task 4: `Word` model and trace

**Depends on:** Task 3

**Files:**
- Create: `phonotactics/src/strands/word.py`
- Create: `phonotactics/tests/test_word.py`

**Interfaces:**

```python
@dataclass(frozen=True)
class TraceEntry:
    stage: str          # "substitute" | "syllabify" | "repair" | "stress" | ...
    rule_id: str        # "<section>:<line>" (I-21) or a stage-internal id like "fallback"
    tag: str            # "attested" | "design" | "fallback" | "" for stage-internal steps
    before: str
    after: str
    note: str = ""

@dataclass(frozen=True)
class Word:
    segments: tuple[str, ...]
    syllables: tuple[int, ...] = ()        # segment index each syllable starts at
    stress: int | None = None              # index into `syllables`
    morphemes: frozenset[int] = frozenset()
    illegal: frozenset[int] = frozenset()  # segment indices inside an illegal span
    flags: tuple[str, ...] = ()            # "UNREPAIRED", ...
    trace: tuple[TraceEntry, ...] = ()

    @classmethod
    def from_tokenized(cls, tok: Tokenized) -> "Word"
    def ipa(self, *, marks: bool = True) -> str
        """Segments joined; with marks=True insert '.' at syllable starts and 'ˈ'
        before the stressed syllable."""
    def replaced(self, start: int, stop: int, new: Sequence[str]) -> "Word"
        """Splice, shifting syllable starts / morpheme positions / illegal marks that
        lie after `stop` by (len(new) - (stop - start)); marks inside the span are dropped."""
    def traced(self, entry: TraceEntry) -> "Word"
    def with_flag(self, flag: str) -> "Word"
    def fallback_count(self) -> int        # trace entries with tag == "fallback"
```

- [ ] **Step 1: Write the failing test** — `tests/test_word.py`

```python
from strands.word import Word, TraceEntry

def w(*segs, **kw): return Word(segments=tuple(segs), **kw)

def test_ipa_with_marks_places_stress_and_dots():
    x = w("k", "ɪ", "ə", "ɾˠ", "ə", syllables=(0, 3), stress=0)
    assert x.ipa() == "ˈkɪə.ɾˠə"
    assert x.ipa(marks=False) == "kɪəɾˠə"

def test_replaced_shifts_later_annotations():
    x = w("s", "k", "a", "l", syllables=(0,), morphemes=frozenset({4}), illegal=frozenset({0, 1}))
    y = x.replaced(0, 1, ("i", "s"))         # epenthesis-like: 1 segment -> 2
    assert y.segments == ("i", "s", "k", "a", "l")
    assert y.morphemes == frozenset({5})

def test_replaced_drops_marks_inside_the_span():
    x = w("a", "b", "c", illegal=frozenset({1}))
    assert x.replaced(1, 2, ("d",)).illegal == frozenset()

def test_traced_appends_and_is_immutable():
    x = w("a")
    y = x.traced(TraceEntry("substitute", "substitute:3", "attested", "a", "b"))
    assert x.trace == () and len(y.trace) == 1

def test_fallback_count_counts_only_fallback_tags():
    x = w("a").traced(TraceEntry("substitute", "fallback", "fallback", "q", "k")) \
              .traced(TraceEntry("substitute", "substitute:1", "attested", "p", "b"))
    assert x.fallback_count() == 1

def test_with_flag_is_idempotent():
    x = w("a").with_flag("UNREPAIRED").with_flag("UNREPAIRED")
    assert x.flags == ("UNREPAIRED",)
```

- [ ] **Step 2: Run, fail. Step 3: Implement. Step 4: Run, pass.**
- [ ] **Step 5: Commit** — `feat(strands): immutable Word model with derivation trace`

**Acceptance:** `Word` is hashable and frozen; every mutator returns a new object.

---

## Task 5: DSL parser

**Depends on:** Task 3

**Files:**
- Create: `phonotactics/src/strands/dsl.py`
- Create: `phonotactics/tests/test_dsl_parser.py`
- Create: `phonotactics/tests/fixtures/mini.rules` (a small complete file exercising every section)

**Interfaces:** implement the EBNF above exactly.

```python
@dataclass(frozen=True)
class Bundle:
    class_name: str | None
    constraints: dict[str, str]        # feature -> "+"/"-"/"0"

Item = str | Bundle                    # str is a segment or a CLASS_NAME (I-10)

@dataclass(frozen=True)
class CtxItem:
    atom: Item | str                   # or one of "#", "$", ".", "ˈ"
    optional: bool = False
    star: bool = False

@dataclass(frozen=True)
class Rule:
    section: str
    line: int
    rule_id: str                       # f"{section}:{line}"
    target: tuple[Item, ...]           # () means epenthesis (TARGET == "0")
    replacement: tuple[Item, ...] | Bundle | tuple[()] | str
                                       # Bundle = feature change; () = deletion; str = quoted respell text
    left: tuple[CtxItem, ...]
    right: tuple[CtxItem, ...]
    tag: str                           # "attested" | "design" | "fallback"
    comment: str

@dataclass(frozen=True)
class SyllableSpec:
    template: tuple[tuple[str, bool], ...] | None   # (slot, optional); None means "any"
    onsets: frozenset[tuple[str, ...]] | None       # None means "any"
    codas: frozenset[tuple[str, ...]] | None
    onset_tiers: dict[tuple[str, ...], str]
    coda_tiers: dict[tuple[str, ...], str]
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
class RuleFile:
    path: str
    meta: dict[str, str]
    inventory: tuple[str, ...]
    marginal: frozenset[str]
    classes: dict[str, tuple[str, ...]]     # includes computed C and V (I-11)
    weights: dict[str, float]
    sections: dict[str, tuple[Rule, ...]]   # substitute/repair/post-stress/respell/normalize
    syllable: SyllableSpec | None
    stress: StressSpec | None
    epithets: dict[str, Epithet]
    templates: dict[str, tuple["TemplateItem", ...]]
    mutations: dict[str, tuple[Rule, ...]]  # "LEN", "ECL", "HPREF", "TPREF"
    inflect: dict[str, tuple[Rule, ...]]    # "GEN_M1", "GEN_ACH", "GEN_F2", "VOC_M1"

@dataclass(frozen=True)
class TemplateItem:
    kind: str            # "literal" | "arg" | "call"
    value: str           # literal text, arg name, or function name
    child: "TemplateItem | None" = None
    conditional: bool = False     # trailing "?"

def parse_rules(text: str, table: FeatureTable, path: str = "<string>") -> RuleFile
def parse_rules_file(path: str | Path, table: FeatureTable) -> RuleFile
class ParseError(Exception):
    line: int
    message: str      # str(e) == f"{path}:{line}: {message}"
```

- [ ] **Step 1: Write the fixture** — `tests/fixtures/mini.rules`

```
# a tiny file exercising every construct
[meta]
name = Mini
digest = sources/none

[inventory]
p b t d k ɡ s ʃ m n l r a i u aː
marginal: ʒ

[classes]
STOP = p b t d k ɡ
LIQ = l r

[weights]
front = 2.0

[substitute]
p -> b                              # attested by default
[C +back] -> [-back]                %design
sˠ ʃ -> s ʃ / #_ V                  %attested # both segments replaced
0 -> i / # s _ [STOP]               %attested # prothesis
t -> 0 / _ #                        %fallback

[syllable]
template = (C)(C)V(C)(C)
onsets   = pl pr bl br st sp
codas    = st ts lp
onsets-tier = pl:A pr:A st:B
appendix = s t
domain   = word
sonority = on
bans = [V +long] C C [-coronal]

[stress]
procedure = penult
window = 3

[epithets]
NISBA = i / $_ #

[respell]
ʃ -> "sh"
aː -> "aa" / _ C
. -> ""
ˈ -> ""

[post-stress]
a -> aː / ˈ_ #                      %design

[repair]
0 -> ə / LIQ _ [C -coronal]         %attested
```

- [ ] **Step 2: Write the failing tests** — `tests/test_dsl_parser.py`

```python
import pytest, pathlib
from strands.features import load_features
from strands.dsl import parse_rules_file, parse_rules, ParseError, Bundle

ROOT = pathlib.Path(__file__).parents[1]
TABLE = load_features(ROOT / "rules" / "features.tsv")
MINI = parse_rules_file(pathlib.Path(__file__).parent / "fixtures" / "mini.rules", TABLE)

def test_meta_and_inventory():
    assert MINI.meta["name"] == "Mini"
    assert MINI.inventory[0] == "p" and "ʒ" in MINI.marginal
    assert "ʒ" in MINI.inventory          # marginal segments are in the inventory too

def test_predeclared_classes_include_irish_segments():
    assert "t̪ˠ" in MINI.classes["C"] and "p" in MINI.classes["C"]
    assert "a" in MINI.classes["V"] and "iː" in MINI.classes["V"]

def test_user_classes():
    assert MINI.classes["STOP"] == ("p", "b", "t", "d", "k", "ɡ")

def test_weights():
    assert MINI.weights["front"] == 2.0

def test_simple_rewrite_defaults_to_attested():
    r = MINI.sections["substitute"][0]
    assert r.target == ("p",) and r.replacement == ("b",) and r.tag == "attested"
    assert r.rule_id.startswith("substitute:")

def test_match_bundle_and_change_bundle():
    r = MINI.sections["substitute"][1]
    assert r.target == (Bundle("C", {"back": "+"}),)
    assert isinstance(r.replacement, Bundle) and r.replacement.constraints == {"back": "-"}
    assert r.replacement.class_name is None
    assert r.tag == "design"

def test_multi_segment_target_and_environment():
    r = MINI.sections["substitute"][2]
    assert r.target == ("sˠ", "ʃ")
    assert [c.atom for c in r.left] == ["#"]
    assert [c.atom for c in r.right] == ["V"]
    assert r.comment.strip() == "both segments replaced"

def test_epenthesis_rule_has_empty_target():
    r = MINI.sections["substitute"][3]
    assert r.target == ()
    assert [c.atom for c in r.left] == ["#", "s"]

def test_deletion_rule():
    r = MINI.sections["substitute"][4]
    assert r.replacement == () and r.tag == "fallback"

def test_syllable_section():
    s = MINI.syllable
    assert s.template == (("C", True), ("C", True), ("V", False), ("C", True), ("C", True))
    assert ("p", "l") in s.onsets and ("s", "t") in s.codas
    assert s.onset_tiers[("p", "l")] == "A"
    assert s.appendix == ("s", "t") and s.domain == "word" and s.sonority is True
    assert len(s.bans) == 1 and len(s.bans[0]) == 4

def test_stress_section():
    assert MINI.stress.procedure == "penult" and MINI.stress.params["window"] == "3"

def test_epithets():
    e = MINI.epithets["NISBA"]
    assert e.form == ("i",) and [c.atom for c in e.left] == ["$"]

def test_respell_quoted_replacement():
    r = MINI.sections["respell"][0]
    assert r.target == ("ʃ",) and r.replacement == "sh"
    assert MINI.sections["respell"][2].replacement == ""

def test_optional_and_star_context_items():
    src = "[inventory]\np a\n[substitute]\np -> a / (a)_ a*\n"
    rf = parse_rules(src, TABLE)
    r = rf.sections["substitute"][0]
    assert r.left[0].optional and r.right[0].star

def test_star_on_optional_is_a_parse_error():
    with pytest.raises(ParseError):
        parse_rules("[inventory]\np a\n[substitute]\np -> a / (a)*_\n", TABLE)

def test_unknown_section_raises_with_line_number():
    with pytest.raises(ParseError) as e:
        parse_rules("[frobnicate]\n", TABLE)
    assert ":1:" in str(e.value)

def test_unknown_segment_in_rule_raises():
    with pytest.raises(ParseError):
        parse_rules("[inventory]\np\n[substitute]\nQ -> p\n", TABLE)

def test_missing_arrow_raises():
    with pytest.raises(ParseError) as e:
        parse_rules("[inventory]\np a\n[substitute]\np a\n", TABLE)
    assert ":4:" in str(e.value)

def test_comment_after_environment_without_tag_is_an_error():
    # I-3: '#' inside an environment is the word edge, so an untagged comment is ambiguous
    with pytest.raises(ParseError) as e:
        parse_rules("[inventory]\np a\n[substitute]\np -> a / _ a # note\n", TABLE)
    assert "explicit %tag" in str(e.value)

def test_word_edge_hash_in_environment_is_not_a_comment():
    rf = parse_rules("[inventory]\np a\n[substitute]\np -> a / _ #\n", TABLE)
    assert [c.atom for c in rf.sections["substitute"][0].right] == ["#"]

def test_mutations_and_inflect_subtables():
    src = ("[inventory]\np f t h\n[mutations]\nLEN:\np -> f\nECL:\nt -> h\n"
           "[inflect]\nVOC_M1:\np -> f / _ #\n")
    rf = parse_rules(src, TABLE)
    assert set(rf.mutations) == {"LEN", "ECL"}
    assert rf.mutations["LEN"][0].target == ("p",)
    assert set(rf.inflect) == {"VOC_M1"}

def test_templates():
    src = '[inventory]\np\n[templates]\nVOC = "a" LEN(NAME) VOC_M1?\n'
    rf = parse_rules(src, TABLE)
    items = rf.templates["VOC"]
    assert items[0].kind == "literal" and items[0].value == "a"
    assert items[1].kind == "call" and items[1].value == "LEN" and items[1].child.value == "NAME"
    assert items[2].conditional is True

def test_rule_ids_are_section_and_line():
    r = MINI.sections["repair"][0]
    assert r.rule_id == f"repair:{r.line}"

def test_parsing_is_deterministic():
    a = parse_rules_file(pathlib.Path(__file__).parent / "fixtures" / "mini.rules", TABLE)
    b = parse_rules_file(pathlib.Path(__file__).parent / "fixtures" / "mini.rules", TABLE)
    assert a == b
```

- [ ] **Step 3: Run, watch every test fail.**
- [ ] **Step 4: Implement `dsl.py`.** Structure: a line-oriented reader that tracks the current
  section and (for `[mutations]`/`[inflect]`) the current sub-table, dispatching to per-section
  entry parsers; one shared `parse_rewrite(line_text, section, lineno)`. Tokenize segment runs via
  `strands.tokenize.tokenize` with marks disabled so a `CLUSTER` becomes a segment tuple.
- [ ] **Step 5: Run — all pass.**
- [ ] **Step 6: Commit** — `feat(strands): rule-file DSL parser`

**Acceptance:** every construct in the EBNF round-trips; every malformed input raises `ParseError`
carrying the 1-based line number; `mini.rules` parses.

---

## Task 6: `strands check` static checks

**Depends on:** Task 5

**Files:**
- Create: `phonotactics/src/strands/check.py`
- Modify: `phonotactics/src/strands/cli.py` (wire the `check` subcommand)
- Create: `phonotactics/tests/test_check.py`

**Interfaces:**

```python
@dataclass(frozen=True)
class CheckError:
    line: int
    code: str      # "UNKNOWN_CLASS" | "UNKNOWN_FEATURE" | "OFF_INVENTORY" |
                   # "EPENTHESIS_NO_CONTEXT" | "UNKNOWN_STRESS_PARAM" |
                   # "UNREACHABLE_CHANGE" | "BAD_TEMPLATE_ARG" | "CLUSTER_OFF_INVENTORY"
    message: str

def check_rule_file(rf: RuleFile, table: FeatureTable) -> list[CheckError]
```

Checks (all of them):
1. every class name used in a rule/bundle/template/ban is declared or predeclared;
2. every feature name in a bundle or `[weights]` is one of the 38;
3. every segment appearing in a **replacement** is in `[inventory]` (`OFF_INVENTORY`) — a
   *warning-level* code, still returned, because `irish.rules` legitimately produces Irish
   segments before the target sees them; `cli` prints warnings but exits 0 unless errors exist;
4. epenthesis rule with both contexts empty (I-7);
5. `[stress] procedure` is one of the five names, and its params are in that procedure's known set;
6. a change-bundle that no inventory segment can satisfy (`UNREACHABLE_CHANGE`), detected by
   trying `apply_changes` over the whole inventory;
7. every segment in `[syllable] onsets/codas/appendix` is in `[inventory]`;
8. `[templates]` arg names and function names are from the fixed sets (I-16).

- [ ] **Step 1: Write the failing test** — `tests/test_check.py`

```python
import pathlib, pytest
from strands.features import load_features
from strands.dsl import parse_rules
from strands.check import check_rule_file

TABLE = load_features(pathlib.Path(__file__).parents[1] / "rules" / "features.tsv")

def codes(src):
    return sorted(e.code for e in check_rule_file(parse_rules(src, TABLE), TABLE))

def test_clean_file_has_no_errors():
    assert codes("[inventory]\np b\n[substitute]\np -> b\n") == []

def test_undeclared_class_is_reported_with_its_line():
    rf = parse_rules("[inventory]\np b\n[substitute]\np -> b / _ NOSUCH\n", TABLE)
    errs = check_rule_file(rf, TABLE)
    assert errs[0].code == "UNKNOWN_CLASS" and errs[0].line == 4

def test_unknown_feature_is_reported():
    assert "UNKNOWN_FEATURE" in codes("[inventory]\np b\n[substitute]\n[C +wibble] -> b\n")

def test_replacement_segment_off_inventory_is_reported():
    assert "OFF_INVENTORY" in codes("[inventory]\np\n[substitute]\np -> b\n")

def test_epenthesis_without_context_is_reported():
    assert "EPENTHESIS_NO_CONTEXT" in codes("[inventory]\np a\n[substitute]\n0 -> a\n")

def test_unknown_stress_parameter_is_reported():
    assert "UNKNOWN_STRESS_PARAM" in codes("[inventory]\np\n[stress]\nprocedure = initial\nwibble = 3\n")

def test_unreachable_feature_change_is_reported():
    assert "UNREACHABLE_CHANGE" in codes("[inventory]\np\n[substitute]\np -> [+click]\n")

def test_onset_cluster_off_inventory_is_reported():
    assert "CLUSTER_OFF_INVENTORY" in codes("[inventory]\np a\n[syllable]\nonsets = pl\n")

def test_cli_check_exits_1_on_errors(tmp_path, capsys):
    from strands.cli import main
    f = tmp_path / "x.rules"
    f.write_text("[inventory]\np a\n[substitute]\n0 -> a\n", encoding="utf-8")
    assert main(["check", str(f)]) == 1
    assert "EPENTHESIS_NO_CONTEXT" in capsys.readouterr().err

def test_cli_check_exits_0_on_a_clean_file(tmp_path):
    from strands.cli import main
    f = tmp_path / "y.rules"
    f.write_text("[inventory]\np b\n[substitute]\np -> b\n", encoding="utf-8")
    assert main(["check", str(f)]) == 0
```

- [ ] **Step 2: Run, fail. Step 3: Implement `check.py` and the `check` subcommand.
  Step 4: Run, pass.**
- [ ] **Step 5: Commit** — `feat(strands): static rule-file checks and 'strands check'`

**Acceptance:** `uv run strands check tests/fixtures/mini.rules` exits 0. Milestone 1 is complete
at this commit.

---

## Task 7: Rewrite engine

**Depends on:** Tasks 4, 5

**Files:**
- Create: `phonotactics/src/strands/rewrite.py`
- Create: `phonotactics/tests/test_rewrite.py`

**Interfaces:**

```python
def match_item(item: Item, segment: str, rf: RuleFile, table: FeatureTable) -> bool
def find_matches(word: Word, rule: Rule, rf: RuleFile, table: FeatureTable) -> list[tuple[int, int]]
    """Non-overlapping (start, stop) spans, leftmost-longest, evaluated against the
    pre-rule word (I-6). For an epenthesis rule (rule.target == ()) returns zero-width
    spans (i, i)."""
def apply_rule(word: Word, rule: Rule, rf: RuleFile, table: FeatureTable,
               stage: str) -> Word
    """All matches applied simultaneously; appends one TraceEntry if anything changed."""
def apply_section(word: Word, rules: Sequence[Rule], rf: RuleFile,
                  table: FeatureTable, stage: str) -> Word
    """Rules in file order (spec §3)."""
class RuleError(Exception): ...
```

Context matching details the implementer must get right:
- The left context is matched **right-to-left** ending immediately before the span; the right
  context left-to-right starting at the span end.
- `#` matches only at position 0 (left) / `len(segments)` (right).
- `$` matches at a position in `word.morphemes`; `.` at a position in `word.syllables`; `ˈ` at the
  segment index that starts the stressed syllable.
- `optional` items may match zero or one segment; `star` zero or more; both are matched greedily
  with backtracking (the context language is regular and tiny — a recursive matcher is fine).

- [ ] **Step 1: Write the failing test** — `tests/test_rewrite.py`

```python
import pathlib, pytest
from strands.features import load_features
from strands.dsl import parse_rules
from strands.tokenize import tokenize
from strands.word import Word
from strands.rewrite import apply_rule, apply_section, find_matches

ROOT = pathlib.Path(__file__).parents[1]
TABLE = load_features(ROOT / "rules" / "features.tsv")

def rf_and_rules(src):
    rf = parse_rules(src, TABLE)
    return rf, rf.sections["substitute"]

def word(s, rf=None):
    return Word.from_tokenized(tokenize(s, TABLE))

def test_simple_substitution_applies_everywhere():
    rf, rules = rf_and_rules("[inventory]\np b a\n[substitute]\np -> b\n")
    out = apply_rule(word("papa"), rules[0], rf, TABLE, "substitute")
    assert out.segments == ("b", "a", "b", "a")

def test_one_trace_entry_per_changing_rule():
    rf, rules = rf_and_rules("[inventory]\np b a\n[substitute]\np -> b\n")
    out = apply_rule(word("papa"), rules[0], rf, TABLE, "substitute")
    assert len(out.trace) == 1
    assert out.trace[0].rule_id == rules[0].rule_id and out.trace[0].tag == "attested"
    assert out.trace[0].before == "papa" and out.trace[0].after == "baba"

def test_no_trace_entry_when_nothing_matches():
    rf, rules = rf_and_rules("[inventory]\np b a\n[substitute]\np -> b\n")
    assert apply_rule(word("aa"), rules[0], rf, TABLE, "substitute").trace == ()

def test_class_target():
    rf, rules = rf_and_rules("[inventory]\np t a\n[classes]\nSTOP = p t\n[substitute]\nSTOP -> a\n")
    assert apply_rule(word("pt"), rules[0], rf, TABLE, "substitute").segments == ("a", "a")

def test_feature_bundle_target_and_feature_change_replacement():
    rf, rules = rf_and_rules("[inventory]\nk kʼ a\n[substitute]\n[C -sonorant] -> [+raisedLarynxEjective]\n")
    assert apply_rule(word("ka"), rules[0], rf, TABLE, "substitute").segments == ("kʼ", "a")

def test_deletion():
    rf, rules = rf_and_rules("[inventory]\np a\n[substitute]\np -> 0\n")
    assert apply_rule(word("pap"), rules[0], rf, TABLE, "substitute").segments == ("a",)

def test_epenthesis_inserts_at_every_matching_position():
    rf, rules = rf_and_rules("[inventory]\ns k i\n[substitute]\n0 -> i / # _ s\n")
    assert apply_rule(word("ski"), rules[0], rf, TABLE, "substitute").segments == ("i", "s", "k", "i")

def test_word_edge_context():
    rf, rules = rf_and_rules("[inventory]\nt d a\n[substitute]\nd -> t / _ #\n")
    assert apply_rule(word("dad"), rules[0], rf, TABLE, "substitute").segments == ("d", "a", "t")

def test_application_is_simultaneous_not_iterative():
    # b -> a / a _  : with simultaneous application only the first b changes
    rf, rules = rf_and_rules("[inventory]\na b\n[substitute]\nb -> a / a _\n")
    assert apply_rule(word("abb"), rules[0], rf, TABLE, "substitute").segments == ("a", "a", "b")

def test_matches_are_non_overlapping_leftmost():
    rf, rules = rf_and_rules("[inventory]\na b\n[substitute]\na a -> b\n")
    assert apply_rule(word("aaa"), rules[0], rf, TABLE, "substitute").segments == ("b", "a")

def test_rules_apply_in_file_order():
    rf, rules = rf_and_rules("[inventory]\na b k\n[substitute]\na -> b\nb -> k\n")
    out = apply_section(word("a"), rules, rf, TABLE, "substitute")
    assert out.segments == ("k",)           # feeding order, not simultaneous across rules

def test_optional_context_item():
    rf, rules = rf_and_rules("[inventory]\np a b\n[substitute]\np -> b / a (a) _\n")
    assert apply_rule(word("aap"), rules[0], rf, TABLE, "substitute").segments == ("a", "a", "b")
    assert apply_rule(word("ap"), rules[0], rf, TABLE, "substitute").segments == ("a", "b")

def test_star_context_item():
    rf, rules = rf_and_rules("[inventory]\np a b\n[substitute]\np -> b / # a* _\n")
    assert apply_rule(word("aaap"), rules[0], rf, TABLE, "substitute").segments[-1] == "b"

def test_morpheme_and_syllable_context():
    rf, rules = rf_and_rules("[inventory]\ni a p\n[substitute]\n0 -> i / $ _ #\n")
    w = Word(segments=("a", "p"), morphemes=frozenset({2}))
    assert apply_rule(w, rules[0], rf, TABLE, "substitute").segments == ("a", "p", "i")

def test_stressed_syllable_context():
    rf, rules = rf_and_rules("[inventory]\na aː p\n[substitute]\na -> aː / ˈ_\n")
    w = Word(segments=("p", "a", "p", "a"), syllables=(0, 2), stress=1)
    out = apply_rule(w, rules[0], rf, TABLE, "substitute")
    assert out.segments == ("p", "a", "p", "a")     # ˈ marks the syllable start (segment 2 = p)
    w2 = Word(segments=("a", "p", "a"), syllables=(0, 1), stress=0)
    assert apply_rule(w2, rules[0], rf, TABLE, "substitute").segments == ("aː", "p", "a")

def test_feature_change_to_a_nonexistent_segment_raises_ruleerror():
    from strands.rewrite import RuleError
    rf, rules = rf_and_rules("[inventory]\nh\n[substitute]\nh -> [+lateral]\n")
    with pytest.raises(RuleError):
        apply_rule(word("h"), rules[0], rf, TABLE, "substitute")

def test_multi_segment_replacement_shifts_annotations():
    rf, rules = rf_and_rules("[inventory]\np i a\n[substitute]\np -> p i\n")
    w = Word(segments=("p", "a"), morphemes=frozenset({2}))
    out = apply_rule(w, rules[0], rf, TABLE, "substitute")
    assert out.segments == ("p", "i", "a") and out.morphemes == frozenset({3})
```

- [ ] **Step 2: Run, fail. Step 3: Implement. Step 4: Run, pass.**
- [ ] **Step 5: Commit** — `feat(strands): rewrite-rule matching and application engine`

**Acceptance:** all of the above; `apply_section` is pure and deterministic.

---

## Task 8: Substitute stage

**Depends on:** Task 7

**Files:**
- Create: `phonotactics/src/strands/substitute.py`
- Create: `phonotactics/tests/test_substitute.py`

**Interfaces:**

```python
def substitute(word: Word, rf: RuleFile, table: FeatureTable) -> Word
    """Stage 2a (spec §4.2): apply rf.sections['substitute'] in file order."""
```

- [ ] **Step 1: Failing test**

```python
def test_substitute_runs_the_section_in_order():
    rf = parse_rules("[inventory]\np b f v\n[substitute]\np -> b\nv -> f\n", TABLE)
    out = substitute(Word(segments=("p", "v")), rf, TABLE)
    assert out.segments == ("b", "f")
    assert [t.stage for t in out.trace] == ["substitute", "substitute"]

def test_substitute_is_a_noop_when_the_section_is_absent():
    rf = parse_rules("[inventory]\np\n", TABLE)
    w = Word(segments=("p",))
    assert substitute(w, rf, TABLE) == w
```

- [ ] **Steps 2–4: fail, implement, pass. Step 5: Commit** —
  `feat(strands): substitute stage`

---

## Task 9: Inventory fallback

**Depends on:** Task 8

**Files:**
- Modify: `phonotactics/src/strands/substitute.py`
- Create: `phonotactics/tests/test_fallback.py`

**Interfaces:**

```python
def fallback(word: Word, rf: RuleFile, table: FeatureTable) -> Word
    """Stage 2b (spec §4.2): every segment not in rf.inventory is replaced by the
    nearest non-marginal inventory segment by weighted feature distance (I-12),
    one TraceEntry per replaced segment, tag='fallback', rule_id='fallback'."""
def substitute_stage(word: Word, rf: RuleFile, table: FeatureTable) -> Word
    """substitute() then fallback()."""
```

- [ ] **Step 1: Failing test** — `tests/test_fallback.py`

```python
def test_offinventory_segment_is_replaced_by_the_nearest_inventory_segment():
    rf = parse_rules("[inventory]\nb f a\n", TABLE)
    out = fallback(Word(segments=("pˠ", "a")), rf, TABLE)
    assert out.segments == ("b", "a")
    assert out.trace[0].tag == "fallback" and out.trace[0].before == "pˠ"

def test_marginal_segments_are_never_chosen():
    rf = parse_rules("[inventory]\nb a\nmarginal: p\n", TABLE)
    assert fallback(Word(segments=("pˠ",)), rf, TABLE).segments == ("b",)

def test_ties_break_by_inventory_order():
    rf = parse_rules("[inventory]\nt d a\n", TABLE)
    first = fallback(Word(segments=("t̪ˠ",)), rf, TABLE).segments
    rf2 = parse_rules("[inventory]\nd t a\n", TABLE)
    second = fallback(Word(segments=("t̪ˠ",)), rf2, TABLE).segments
    # deterministic in each case; if the distances are equal the orders disagree
    assert first == ("t",) and second in {("t",), ("d",)}

def test_weights_change_the_choice():
    rf = parse_rules("[inventory]\nk c a\n[weights]\nfront = 20.0\n", TABLE)
    assert fallback(Word(segments=("ɟ",)), rf, TABLE).segments == ("c",)

def test_inventory_segments_are_untouched_and_untraced():
    rf = parse_rules("[inventory]\nb a\n", TABLE)
    w = Word(segments=("b", "a"))
    assert fallback(w, rf, TABLE) == w

def test_fallback_count_is_visible_on_the_word():
    rf = parse_rules("[inventory]\nb a\n", TABLE)
    assert fallback(Word(segments=("pˠ", "pʲ")), rf, TABLE).fallback_count() == 2
```

- [ ] **Steps 2–4. Step 5: Commit** — `feat(strands): nearest-segment inventory fallback`

**Acceptance:** milestone 2 complete. Also assert determinism: two runs give identical traces.

---

## Task 10: Syllabifier

**Depends on:** Tasks 4, 5

**Files:**
- Create: `phonotactics/src/strands/syllabify.py`
- Create: `phonotactics/tests/test_syllabify.py`

**Interfaces:**

```python
SONORITY: dict[str, int]     # documented in the module docstring; see I-13

def sonority(segment: str, table: FeatureTable) -> int
def legal_onset(cluster: tuple[str, ...], spec: SyllableSpec, table: FeatureTable) -> bool
def legal_coda(cluster: tuple[str, ...], spec: SyllableSpec, table: FeatureTable) -> bool
def syllabify(word: Word, rf: RuleFile, table: FeatureTable) -> Word
    """Maximal onset subject to legality (spec §3). Sets word.syllables and, on failure,
    word.illegal = the minimal span that cannot be parsed (never raises). Appends one
    TraceEntry (stage='syllabify') showing the parse."""
```

Algorithm (implement exactly):
1. Split the segment string into domains: `domain = word` → the whole word; `domain = stem` →
   the spans between `$` positions (spec §3; Georgian, I-27).
2. Within a domain, find nucleus positions = every `V`-class segment (spec's `V`), maximal runs of
   which are separate nuclei (each vowel is its own nucleus — I-2 makes Irish diphthongs two
   nuclei, and hiatus is then a legality question for the rule file's `bans`).
3. Assign the consonants between two nuclei by **maximal onset subject to legality**: try the
   longest suffix of the interlude that is a legal onset; the remainder is the preceding coda; if
   that remainder is not a legal coda, back off one segment at a time; if no split works, mark the
   whole interlude illegal and split it at the sonority minimum.
4. Word-initial consonants must form a legal onset, word-final ones a legal coda **plus** up to
   `appendix` extra segments drawn from the appendix set; otherwise mark illegal.
5. Legality of a piece = `template ∧ onset-set ∧ coda-set ∧ sonority ∧ not-banned`; a component is
   skipped when it is `any` / `off` / empty.
6. `bans` are checked over the whole domain after the parse; a matched ban marks its span illegal.

- [ ] **Step 1: Write the failing test** — `tests/test_syllabify.py`

```python
CV = "[inventory]\np t k b s l r a i u aː\n[syllable]\ntemplate = (C)(C)V(C)\nonsets = pl pr st\ncodas = st\nsonority = on\n"

def syl(src, s):
    rf = parse_rules(src, TABLE)
    return syllabify(Word.from_tokenized(tokenize(s, TABLE)), rf, TABLE)

def test_simple_cv_parse():
    out = syl(CV, "pata")
    assert out.syllables == (0, 2) and out.illegal == frozenset()

def test_maximal_onset_subject_to_legality():
    out = syl(CV, "apla")            # 'pl' is a legal onset -> a.pla
    assert out.syllables == (0, 1)
    out2 = syl(CV, "apta")           # 'pt' is not -> ap.ta
    assert out2.syllables == (0, 2)

def test_illegal_initial_cluster_is_marked_not_raised():
    out = syl(CV, "kta")
    assert out.illegal == frozenset({0, 1})
    assert "syllabify" in [t.stage for t in out.trace]

def test_minimal_illegal_span():
    out = syl(CV, "apkta")           # only the medial cluster is bad
    assert out.illegal == frozenset({1, 2, 3}) or out.illegal == frozenset({2, 3})
    assert 0 not in out.illegal

def test_template_limits_coda_size():
    out = syl(CV, "apst")            # template allows one coda C (+ no appendix here)
    assert out.illegal

def test_appendix_licenses_extra_final_coronals():
    src = CV.replace("sonority = on", "sonority = on\nappendix = s t")
    assert syl(src, "apst").illegal == frozenset()

def test_sonority_rejects_falling_onsets():
    src = "[inventory]\np l a\n[syllable]\ntemplate = (C)(C)V(C)\nonsets = any\nsonority = on\n"
    assert syl(src, "lpa").illegal

def test_sonority_off_accepts_them():
    src = "[inventory]\np l a\n[syllable]\ntemplate = (C)(C)V(C)\nonsets = any\nsonority = off\n"
    assert syl(src, "lpa").illegal == frozenset()

def test_sc_clusters_are_exempt_from_the_sonority_check():
    src = "[inventory]\ns t a\n[syllable]\ntemplate = (C)(C)V(C)\nonsets = any\nsonority = on\n"
    assert syl(src, "sta").illegal == frozenset()

def test_bans_mark_their_span():
    src = ("[inventory]\np t a aː\n[syllable]\ntemplate = any\nonsets = any\ncodas = any\n"
           "sonority = off\nbans = [V +long] C C\n")
    out = syl(src, "aːpta")
    assert out.illegal and 0 in out.illegal

def test_stem_domain_syllabifies_between_morpheme_boundaries():
    src = ("[inventory]\np t a\n[syllable]\ntemplate = any\nonsets = any\ncodas = any\n"
           "sonority = off\ndomain = stem\n")
    rf = parse_rules(src, TABLE)
    w = Word(segments=("p", "a", "t", "a"), morphemes=frozenset({2}))
    out = syllabify(w, rf, TABLE)
    assert out.syllables == (0, 2)

def test_template_any_accepts_anything_the_lists_accept():
    src = "[inventory]\np t k a\n[syllable]\ntemplate = any\nonsets = any\ncodas = any\nsonority = off\n"
    assert syl(src, "ptkaptk").illegal == frozenset()

def test_syllabify_is_idempotent():
    a = syl(CV, "pata"); rf = parse_rules(CV, TABLE)
    assert syllabify(a, rf, TABLE).syllables == a.syllables
```

- [ ] **Steps 2–4: fail, implement, pass.**
- [ ] **Step 5: Commit** — `feat(strands): syllabifier with legality and illegal-span marking`

---

## Task 11: Repair loop

**Depends on:** Tasks 7, 10

**Files:**
- Create: `phonotactics/src/strands/repair.py`
- Create: `phonotactics/tests/test_repair.py`

**Interfaces:**

```python
MAX_REPAIR_ITERATIONS = 10

def repair(word: Word, rf: RuleFile, table: FeatureTable) -> Word
    """Spec §4.4: apply rf.sections['repair'] in order; re-syllabify after any rule that
    changes the segment count; loop until word.illegal is empty or MAX_REPAIR_ITERATIONS
    passes have run, then set flag 'UNREPAIRED'."""
```

- [ ] **Step 1: Failing test**

```python
SRC = ("[inventory]\ns k i a\n[syllable]\ntemplate = (C)V(C)\nonsets = any\ncodas = any\n"
       "sonority = off\n[repair]\n0 -> i / # _ s [C -sonorant]   %attested\n")

def test_repair_fixes_an_illegal_onset_and_clears_the_mark():
    rf = parse_rules(SRC, TABLE)
    w = syllabify(Word.from_tokenized(tokenize("ski", TABLE)), rf, TABLE)
    assert w.illegal
    out = repair(w, rf, TABLE)
    assert out.segments == ("i", "s", "k", "i") and out.illegal == frozenset()
    assert "UNREPAIRED" not in out.flags

def test_resyllabification_happens_after_a_length_changing_rule():
    rf = parse_rules(SRC, TABLE)
    w = syllabify(Word.from_tokenized(tokenize("ski", TABLE)), rf, TABLE)
    out = repair(w, rf, TABLE)
    assert out.syllables == (0, 2)

def test_unrepairable_word_gets_the_flag_and_stops_at_ten_iterations():
    rf = parse_rules("[inventory]\nk t a\n[syllable]\ntemplate = (C)V\nonsets = any\ncodas = any\n"
                     "sonority = off\n[repair]\nk -> k   %design\n", TABLE)
    w = syllabify(Word.from_tokenized(tokenize("kta", TABLE)), rf, TABLE)
    out = repair(w, rf, TABLE)
    assert "UNREPAIRED" in out.flags
    assert len([t for t in out.trace if t.stage == "repair"]) <= 10 * 1 + 10

def test_a_word_with_no_illegal_marks_is_returned_unchanged():
    rf = parse_rules(SRC, TABLE)
    w = syllabify(Word.from_tokenized(tokenize("ki", TABLE)), rf, TABLE)
    assert repair(w, rf, TABLE).segments == w.segments

def test_repair_is_deterministic():
    rf = parse_rules(SRC, TABLE)
    w = syllabify(Word.from_tokenized(tokenize("ski", TABLE)), rf, TABLE)
    assert repair(w, rf, TABLE) == repair(w, rf, TABLE)
```

- [ ] **Steps 2–4. Step 5: Commit** — `feat(strands): repair loop with re-syllabification`

**Acceptance:** milestone 3 complete.

---

## Task 12: Stress framework, `initial`, `keep-source`

**Depends on:** Tasks 4, 5

**Files:**
- Create: `phonotactics/src/strands/stress.py`
- Create: `phonotactics/tests/test_stress_framework.py`

**Interfaces:**

```python
PROCEDURES: dict[str, Callable[[Word, StressSpec, FeatureTable], int | None]]
PROCEDURE_PARAMS: dict[str, frozenset[str]]   # used by check.py (Task 6)

def syllable_weight(word: Word, i: int, table: FeatureTable) -> str
    """'light' (open, short nucleus) | 'heavy' (long nucleus or one coda C)
    | 'superheavy' (long nucleus + coda, or two coda C). Shared by cairene and
    dutch-weight."""
def assign_stress(word: Word, rf: RuleFile, table: FeatureTable) -> Word
    """Dispatch on rf.stress.procedure; sets word.stress (index into word.syllables)
    and appends a TraceEntry (stage='stress', rule_id=f'stress:{procedure}')."""
def register(name: str, params: frozenset[str]) -> Callable    # decorator
```

Procedures in this task:
- `initial` — stress syllable 0 always (Georgian, digest §4.1; Irish Connacht, digest §4.1).
  Param: `mark = on|off` (default `on`; Georgian sets `off`, meaning `word.stress` is set but the
  respell stage is told not to print it — see Task 21).
- `keep-source` — leave `word.stress` as it arrived from the Irish pre-pass; if `None`, fall back
  to syllable 0. No params.

- [ ] **Step 1: Failing test**

```python
def stressed(src, s):
    rf = parse_rules(src, TABLE)
    w = syllabify(Word.from_tokenized(tokenize(s, TABLE)), rf, TABLE)
    return assign_stress(w, rf, TABLE)

BASE = "[inventory]\np t k a aː i n s\n[syllable]\ntemplate = (C)V(C)(C)\nonsets = any\ncodas = any\nsonority = off\n"

def test_initial_stresses_the_first_syllable():
    out = stressed(BASE + "[stress]\nprocedure = initial\n", "patapa")
    assert out.stress == 0 and out.ipa().startswith("ˈ")

def test_initial_on_a_monosyllable():
    assert stressed(BASE + "[stress]\nprocedure = initial\n", "pat").stress == 0

def test_keep_source_preserves_an_existing_mark():
    rf = parse_rules(BASE + "[stress]\nprocedure = keep-source\n", TABLE)
    w = syllabify(Word.from_tokenized(tokenize("paˈta", TABLE)), rf, TABLE)
    assert assign_stress(w, rf, TABLE).stress == 1

def test_keep_source_defaults_to_initial_when_unmarked():
    assert stressed(BASE + "[stress]\nprocedure = keep-source\n", "pata").stress == 0

def test_stress_appends_a_trace_entry():
    out = stressed(BASE + "[stress]\nprocedure = initial\n", "pata")
    assert out.trace[-1].stage == "stress" and out.trace[-1].rule_id == "stress:initial"

def test_syllable_weight_classification():
    rf = parse_rules(BASE, TABLE)
    w = syllabify(Word.from_tokenized(tokenize("patatnaːsaːn", TABLE)), rf, TABLE)
    assert syllable_weight(w, 0, TABLE) == "light"      # pa
    weights = [syllable_weight(w, i, TABLE) for i in range(len(w.syllables))]
    assert set(weights) <= {"light", "heavy", "superheavy"}

def test_unknown_procedure_raises():
    with pytest.raises(Exception):
        stressed(BASE + "[stress]\nprocedure = wibble\n", "pata")
```

- [ ] **Steps 2–4. Step 5: Commit** — `feat(strands): stress framework with initial/keep-source`

---

## Task 13: `penult` procedure (Welsh)

**Depends on:** Task 12. **Independent of Tasks 14, 15.**

**Files:** Modify `src/strands/stress.py`; create `tests/test_stress_penult.py`.

**Source:** `sources/welsh/digest.md` §4.1 — stress falls on the penultimate syllable of
polysyllables; a monosyllabic content word is stressed on its only syllable; suffixation shifts
the stress rightward (stress is recomputed after affixation, never carried).

**Params:** none.

- [ ] **Step 1: Failing test** — `tests/test_stress_penult.py`

```python
BASE = ("[inventory]\np t k b d ɡ m n l r s ʃ x a e i o u aː eː iː oː uː ə\n"
        "[syllable]\ntemplate = (C)(C)V(C)(C)\nonsets = any\ncodas = any\nsonority = off\n"
        "[stress]\nprocedure = penult\n")

@pytest.mark.parametrize("ipa,expected_syllable", [
    ("pata", 0),          # 2 syllables -> penult = 0
    ("patata", 1),        # 3 syllables -> penult = 1
    ("pat", 0),           # monosyllable
    ("patatata", 2),      # 4 syllables
])
def test_penult(ipa, expected_syllable):
    rf = parse_rules(BASE, TABLE)
    w = syllabify(Word.from_tokenized(tokenize(ipa, TABLE)), rf, TABLE)
    assert assign_stress(w, rf, TABLE).stress == expected_syllable

def test_penult_ignores_weight():
    rf = parse_rules(BASE, TABLE)
    w = syllabify(Word.from_tokenized(tokenize("paːtata", TABLE)), rf, TABLE)
    assert assign_stress(w, rf, TABLE).stress == 1     # not attracted to the long vowel
```

- [ ] **Steps 2–4. Step 5: Commit** — `feat(strands): penult stress procedure`

---

## Task 14: `cairene` procedure

**Depends on:** Task 12. **Independent of Tasks 13, 15.**

**Files:** Modify `src/strands/stress.py`; create `tests/test_stress_cairene.py`.

**Source:** `sources/arabic-egy/digest.md` §4 "The rule" (Watson/McCarthy). Implement exactly:
1. Stress the final syllable if it is `CVːC`, `CVː`, or `CVCC` (superheavy).
2. Else stress the antepenult **if** penult and antepenult are both light **and** the
   pre-antepenult is not also light; **the digest's worked rows are the authority** — read §4's
   16-row table and encode whichever formulation reproduces all 16.
3. Else stress the penult. Note the Cairene-specific trap: **a heavy antepenult rejects stress**
   (`madˈrasa`, not `ˈmadrasa`), which distinguishes Cairene from Levantine.
4. Epenthetic vowels count for stress (`binˈtina`) — this falls out because stress runs after
   repair (spec §4 stage order), so nothing extra is needed; assert it.

**Params:** none.

- [ ] **Step 1: Failing test** — transcribe **all 16 rows** of the §4 table into a
  `@pytest.mark.parametrize` list of `(ipa_without_stress, expected_stressed_ipa)`. The rows the
  extraction confirmed are present and must appear: `kaˈtabt`, `ˈʔabadan`, `muxˈtalifa`,
  `jikˈtibu`, `marˈtaba`, `madˈrasa`, `binˈtina`. Read the digest and add the rest; do not
  paraphrase — copy the forms.

```python
CAIRENE = ("[inventory]\n... the Cairene inventory ...\n"
           "[syllable]\ntemplate = CV(C)(C)\nonsets = any\ncodas = any\nsonority = off\n"
           "[stress]\nprocedure = cairene\n")

@pytest.mark.parametrize("plain,expected", CAIRENE_STRESS_TABLE)   # 16 rows from digest §4
def test_cairene_stress_table(plain, expected):
    rf = parse_rules(CAIRENE, TABLE)
    w = syllabify(Word.from_tokenized(tokenize(plain, TABLE)), rf, TABLE)
    assert assign_stress(w, rf, TABLE).ipa() == expected

def test_heavy_antepenult_rejects_stress():
    # madrasa -> madˈrasa, not ˈmadrasa (digest §4, the Cairene/Levantine split)
    ...

def test_epenthetic_vowel_counts_for_stress():
    # bint + na -> binˈtina (digest §4)
    ...
```

- [ ] **Steps 2–4. Step 5: Commit** — `feat(strands): Cairene stress procedure (digest §4, 16 rows)`

**Acceptance:** all 16 digest rows pass. If any row cannot be made to pass, do **not** special-case
it — record it in the test as `xfail` with the digest line number and note it in the commit body.

---

## Task 15: `dutch-weight` procedure

**Depends on:** Task 12. **Independent of Tasks 13, 14.**

**Files:** Modify `src/strands/stress.py`; create `tests/test_stress_dutch.py`.

**Source:** `sources/dutch/digest.md` §4 "The practical rule" — explicitly *constructed by the
digest*, so tag its rule line `%design` in `dutch.rules`. Six ordered steps, implement verbatim:
1. schwa is unstressable; prefer the syllable before a schwa;
2. final superheavy, or final syllable ending in a diphthong → stress final;
3. else closed penult with a full vowel → stress penult;
4. else final closed B-class (lax) syllable → stress antepenult (weak);
5. else → stress penult (default);
6. never place stress outside the last three syllables.

**Params:** `window = 3` (default 3).

- [ ] **Step 1: Failing test** — the digest gives 5 worked examples, one per rule; transcribe them
  exactly: `avontuur` [a.vɔn.ˈtyr], `agenda` [a.ˈɣɛn.da], `albatros` [ˈɑl.ba.trɔs], `mirakel`
  [mi.ˈra.kəl], plus `arena`/`avocado` (read §4 for their transcriptions). Add:

```python
def test_schwa_is_never_stressed():
    # mirakel -> mi.ˈra.kəl
    ...

def test_three_syllable_window_is_respected():
    # a 5-syllable word never gets stress on syllable 0 or 1
    ...
```

- [ ] **Steps 2–4. Step 5: Commit** — `feat(strands): dutch-weight stress procedure`

---

## Task 16: Post-stress stage

**Depends on:** Tasks 7, 12

**Files:** Create `src/strands/poststress.py`; create `tests/test_poststress.py`.

**Interfaces:**

```python
def post_stress(word: Word, rf: RuleFile, table: FeatureTable) -> Word
    """Spec §4.5: apply rf.sections['post-stress'] in file order, after assign_stress.
    Re-syllabify at the end if any rule changed the segment count."""
```

- [ ] **Step 1: Failing test**

```python
SRC = (BASE + "[stress]\nprocedure = penult\n[post-stress]\na -> aː / ˈ_ C V   %design\n")

def test_post_stress_rule_sees_the_stress_mark():
    rf = parse_rules(SRC, TABLE)
    w = assign_stress(syllabify(Word.from_tokenized(tokenize("pata", TABLE)), rf, TABLE), rf, TABLE)
    out = post_stress(w, rf, TABLE)
    assert out.segments == ("p", "aː", "t", "a")

def test_post_stress_resyllabifies_after_a_length_change():
    # a rule that inserts a segment must leave word.syllables consistent
    ...

def test_absent_section_is_a_noop():
    ...
```

- [ ] **Steps 2–4. Step 5: Commit** — `feat(strands): post-stress stage`

**Acceptance:** milestone 4 complete (Tasks 12–16).

---

## Task 17: Irish mutations and inflections

**Depends on:** Task 7. **Independent of Tasks 19, 20.**

**Files:**
- Create: `phonotactics/rules/irish.rules` (sections `[meta] [inventory] [mutations] [inflect]`)
- Create: `phonotactics/src/strands/irish.py` (the `apply_mutation` / `apply_inflection` half)
- Create: `phonotactics/tests/test_irish_mutations.py`

**Interfaces:**

```python
def apply_mutation(word: Word, name: str, rf: RuleFile, table: FeatureTable) -> Word
    """name in {'LEN','ECL','HPREF','TPREF'}; applies that sub-table's rules, which are
    all anchored at '#_' so only the initial changes."""
def apply_inflection(word: Word, name: str, rf: RuleFile, table: FeatureTable) -> Word
    """name in {'GEN_M1','GEN_ACH','GEN_F2','GEN_M3','VOC_M1'}."""
class IrishError(Exception): ...
```

**Rule content — transcribe from `sources/irish/digest.md` §3.1 (lenition table), §3.2 (eclipsis
table), §3.3 (the other initial changes), §3.5 (genitive/vocative endings).** Every line carries
`# [wiki-irish-mutations §Summary table]` or the digest's own citation. Concretely:

```
[mutations]
LEN:
pˠ -> fˠ / #_        %attested # [wiki-irish-mutations §Summary table]
pʲ -> fʲ / #_        %attested # [wiki-irish-mutations §Summary table]
bˠ -> w  / #_        %attested # ...
bʲ -> vʲ / #_        %attested
mˠ -> w  / #_        %attested
mʲ -> vʲ / #_        %attested
fˠ -> 0  / #_        %attested # fh is silent
fʲ -> 0  / #_        %attested
t̪ˠ -> h / #_         %attested
tʲ -> h  / #_        %attested
d̪ˠ -> ɣ / #_         %attested
dʲ -> j  / #_        %attested
sˠ -> h  / #_        %attested
ʃ  -> h  / #_        %attested
k  -> x  / #_        %attested
c  -> ç  / #_        %attested
ɡ  -> ɣ  / #_        %attested
ɟ  -> j  / #_        %attested
# l/n rows are null in a two-way Connacht transcription (digest §3.1) — deliberately absent.
# Vowels and /ɾˠ ɾʲ/ do not lenite (digest §3.1) — deliberately absent.
ECL:
pˠ -> bˠ / #_        %attested
pʲ -> bʲ / #_        %attested
t̪ˠ -> d̪ˠ / #_        %attested
tʲ -> dʲ / #_        %attested
k  -> ɡ  / #_        %attested
c  -> ɟ  / #_        %attested
bˠ -> mˠ / #_        %attested
bʲ -> mʲ / #_        %attested
d̪ˠ -> n̪ˠ / #_        %attested
dʲ -> nʲ / #_        %attested
ɡ  -> ŋ  / #_        %attested
ɟ  -> ɲ  / #_        %attested
fˠ -> w  / #_        %attested
fʲ -> vʲ / #_        %attested
0  -> n̪ˠ / # _ [V +back]    %attested # n-prothesis before a vowel
0  -> nʲ / # _ [V +front]    %attested
HPREF:
0 -> h / # _ V       %attested # [wiki-irish-mutations §Changes to vowel-initial words]
TPREF:
0 -> t̪ˠ / # _ [V +back]     %attested
0 -> tʲ / # _ [V +front]    %attested
sˠ -> t̪ˠ / #_       %attested # an tsolais
ʃ  -> tʲ / #_        %attested # an tSín
```

`[inflect]` encodes §3.5 as rewrite rules anchored at `_ #`:
- `GEN_M1` — slenderize the final consonant (and the vowel per §3.5's *mac* → *mic* example):
  a feature-change rule `[C +back] -> [+front -back] / _ #` plus the specific vowel adjustments
  the digest's examples require (`a -> ɪ / _ [C +front] #`, cited to *mac* /mˠak/ → /mʲɪc/).
- `GEN_ACH` — `x -> j / ə _ #` (*marcach* → *marcaigh*).
- `GEN_F2` — slenderize + `0 -> ə / _ #` (*bróg* → *bróige*).
- `GEN_M3` — broaden + `0 -> ə / _ #` (*bádóir* → *bádóra*).
- `VOC_M1` — same as `GEN_M1` (§3.5: "the vocative takes the slenderized genitive stem").

- [ ] **Step 1: Write the failing tests** — `tests/test_irish_mutations.py`

```python
IRISH = parse_rules_file(ROOT / "rules" / "irish.rules", TABLE)

def w(s): return Word.from_tokenized(tokenize(s, TABLE))
def ipa(x): return x.ipa(marks=False)

@pytest.mark.parametrize("radical,lenited", [
    ("pˠ", "fˠ"), ("pʲ", "fʲ"), ("bˠ", "w"), ("bʲ", "vʲ"), ("mˠ", "w"), ("mʲ", "vʲ"),
    ("t̪ˠ", "h"), ("tʲ", "h"), ("d̪ˠ", "ɣ"), ("dʲ", "j"), ("sˠ", "h"), ("ʃ", "h"),
    ("k", "x"), ("c", "ç"), ("ɡ", "ɣ"), ("ɟ", "j"),
])
def test_lenition_table_digest_3_1(radical, lenited):
    out = apply_mutation(w(radical + "a"), "LEN", IRISH, TABLE)
    assert ipa(out) == (lenited + "a" if lenited else "a")

def test_fh_lenites_to_nothing():
    assert ipa(apply_mutation(w("fˠaː"), "LEN", IRISH, TABLE)) == "aː"

def test_vowels_and_taps_do_not_lenite():
    for s in ("aː", "ɾˠa", "ɾʲa"):
        assert ipa(apply_mutation(w(s), "LEN", IRISH, TABLE)) == s

@pytest.mark.parametrize("radical,eclipsed", [
    ("pˠ", "bˠ"), ("t̪ˠ", "d̪ˠ"), ("k", "ɡ"), ("bˠ", "mˠ"), ("d̪ˠ", "n̪ˠ"),
    ("ɡ", "ŋ"), ("ɟ", "ɲ"), ("fˠ", "w"), ("fʲ", "vʲ"),
])
def test_eclipsis_table_digest_3_2(radical, eclipsed):
    assert ipa(apply_mutation(w(radical + "a"), "ECL", IRISH, TABLE)).startswith(eclipsed)

@pytest.mark.parametrize("form,expected", [
    ("ɡaːʃ", "ɡaːʃ"),          # gcáis: the input is already the eclipsed form (digest §3.2)
])
def test_attested_eclipsis_forms_are_reachable(form, expected):
    ...   # assert ECL(káis) == gcáis using the digest's attested pairs

def test_eclipsis_of_a_vowel_initial_word_prefixes_n():
    assert ipa(apply_mutation(w("iːʃ"), "ECL", IRISH, TABLE)).startswith("nʲ")

def test_h_prothesis_only_before_vowels():
    assert ipa(apply_mutation(w("iːʃ"), "HPREF", IRISH, TABLE)) == "hiːʃ"
    assert ipa(apply_mutation(w("kaː"), "HPREF", IRISH, TABLE)) == "kaː"

def test_t_prefixation_replaces_s_lenition_after_the_article():
    assert ipa(apply_mutation(w("ʃiːnʲ"), "TPREF", IRISH, TABLE)).startswith("tʲ")   # an tSín

def test_vocative_of_sean_is_a_shean():
    # digest §3.5: /ʃaːnˠ/ -> lenite -> /haːnˠ/ ... but the attested form is /çaːnʲ/,
    # which is LEN + VOC_M1 (slenderization) together. Assert the composed result.
    x = apply_inflection(apply_mutation(w("ʃaːnˠ"), "LEN", IRISH, TABLE), "VOC_M1", IRISH, TABLE)
    assert ipa(x) == "çaːnʲ"

def test_genitive_of_mac_is_mic():
    assert ipa(apply_inflection(w("mˠak"), "GEN_M1", IRISH, TABLE)) == "mʲɪc"

def test_gen_ach_marcach_to_marcaigh():
    assert ipa(apply_inflection(w("mˠaɾˠkəx"), "GEN_ACH", IRISH, TABLE)) == "mˠaɾˠkəj"

def test_test_words_tagged_for_mutations_all_apply_without_error():
    # every row of sources/irish/test-words.tsv whose `features` column mentions len: or ecl:
    for row in mutation_rows():
        apply_mutation(w(row["ipa"]), "LEN", IRISH, TABLE)   # must not raise
```

*(Note on `test_vocative_of_sean_is_a_shean`: the digest gives /ʃaːnˠ/ → *a Sheáin* [ə çaːnʲ].
Lenition of /ʃ/ is /h/, but before a back vowel the digest §1.1 states /h/ surfaces as [ç]. Encode
that as an `[normalize]` rule in Task 19 — `h -> ç / #_ [V +back]` — and make this test pass with
the composed pipeline, or mark it `xfail` with a citation if the ordering resists. Do not fudge
the lenition table.)*

- [ ] **Steps 2–4. Step 5: Commit** —
  `feat(rules): irish.rules mutation and inflection tables (digest §3.1-§3.5)`

---

## Task 18: Irish templates

**Depends on:** Tasks 17, 20 (for the `Entry` record)

**Files:**
- Modify: `phonotactics/rules/irish.rules` (add `[templates]`)
- Modify: `phonotactics/src/strands/irish.py`
- Create: `phonotactics/tests/test_irish_templates.py`

**Interfaces:**

`Entry` is defined in Task 20 (`strands.inputs`); it is reproduced here for reference only —
do **not** define a second copy.

```python
@dataclass(frozen=True)
class Entry:                      # defined in strands/inputs.py by Task 20
    orthography: str
    ipa: str
    dialect: str = "C"
    gloss: str = ""
    category: str = ""
    gender: str = "m"
    declension: str = "m1"
    gen_ipa: str = ""
    pl_ipa: str = ""
    note: str = ""
    assumptions: tuple[str, ...] = ()

def build_construction(name: str, slots: dict[str, Entry], rf: RuleFile,
                       table: FeatureTable) -> list[Word]
    """Apply rf.templates[name]. Returns one Word per space-separated word (I-16).
    Raises MissingSlot (subclass of IrishError) when a required slot is absent."""
class MissingSlot(IrishError): ...
```

Template content in `irish.rules` — exactly the eight from spec §3:

```
[templates]
VOC      = "a" LEN(NAME) VOC_M1?
GEN      = GEN(NAME)
PATRO_O  = "ó" GEN(FATHER)
PATRO_NI = "ní" LEN(GEN(FATHER))
ADJ      = NAME " " LEN_IF_F(ADJ)
OF       = NAME " " ART(GEN(NOUN))
COMPOUND = FIRST LEN(SECOND)
DESC     = NOUN
```

Function semantics (implement in `irish.py`, one function each):
- `LEN/ECL/HPREF/TPREF(x)` → `apply_mutation`.
- `GEN(x)` → dispatch on `x.declension`: `m1`→`GEN_M1`, `ach`→`GEN_ACH`, `f2`→`GEN_F2`,
  `m3`→`GEN_M3`, `4`→identity (digest §3.5 declension 4 is unchanged).
- `VOC_M1?` → applied only when `slots['NAME'].declension == 'm1'` (spec §3's `?`).
- `LEN_IF_F(x)` → lenite iff the head noun's `gender == 'f'` (digest §3.6).
- `ART(x)` → prefix the article and apply its mutation: masculine genitive → `LEN`; feminine
  nominative → `LEN`; before a coronal → no lenition (digest §3.4); `s` → `TPREF`. Encode the
  article's own segments (`ə n̪ˠ` / `ə nʲ`) as a literal in the template call's implementation and
  cite digest §3.4.
- Literals (`"ó"`, `"ní"`, `"a"`) are given **in IPA** in the rule file, not orthography —
  write `"oː"`, `"nʲiː"`, `"ə"` and put the orthographic form in the trailing comment.
- Every join inserts a `$` at the join position (spec §3).

- [ ] **Step 1: Failing test** — `tests/test_irish_templates.py`

```python
def entry(ipa, **kw): return Entry(orthography="x", ipa=ipa, **kw)

def test_voc_of_a_first_declension_masculine_name():
    words = build_construction("VOC", {"NAME": entry("ʃaːnˠ", declension="m1")}, IRISH, TABLE)
    assert len(words) == 1
    assert words[0].ipa(marks=False) == "əçaːnʲ"      # a Sheáin (digest §3.5)

def test_voc_skips_the_slenderizing_step_outside_m1():
    words = build_construction("VOC", {"NAME": entry("bʲɾʲiːdʲ", declension="f2")}, IRISH, TABLE)
    assert words[0].ipa(marks=False).startswith("əvʲ")   # a Bhríd, lenited but not slenderized

def test_joins_insert_morpheme_boundaries():
    words = build_construction("VOC", {"NAME": entry("ʃaːnˠ", declension="m1")}, IRISH, TABLE)
    assert words[0].morphemes                        # at least the "a"+name join

def test_space_literal_splits_into_separate_words():
    words = build_construction("ADJ", {"NAME": entry("mˠaːɾʲə", gender="f"),
                                       "ADJ": entry("bˠaːnˠ")}, IRISH, TABLE)
    assert len(words) == 2
    assert words[1].ipa(marks=False).startswith("w")  # Máire Bhán: lenited after a feminine noun

def test_len_if_f_does_not_lenite_after_a_masculine_noun():
    words = build_construction("ADJ", {"NAME": entry("pˠaːdˠɾˠəɟ", gender="m"),
                                       "ADJ": entry("ɾˠuə")}, IRISH, TABLE)
    assert words[1].ipa(marks=False).startswith("ɾˠ")  # Pádraig Rua, unlenited (digest §3.6)

def test_patro_ni_lenites_the_genitive_father():
    words = build_construction("PATRO_NI", {"FATHER": entry("kaːnˠ", declension="m1")}, IRISH, TABLE)
    assert words[0].ipa(marks=False).startswith("nʲiː")

def test_compound_lenites_the_second_element():
    # Lasairchos = lasair + cos, /ˈl̪ˠɑsˠəɾʲ/ + /kosˠ/ -> /ˈl̪ˠɑsˠəɾʲxosˠ/ (digest §3.6)
    words = build_construction("COMPOUND", {"FIRST": entry("l̪ˠɑsˠəɾʲ"), "SECOND": entry("kosˠ")},
                               IRISH, TABLE)
    assert words[0].ipa(marks=False) == "l̪ˠɑsˠəɾʲxosˠ"

def test_missing_slot_raises_missingslot():
    with pytest.raises(MissingSlot):
        build_construction("PATRO_O", {}, IRISH, TABLE)

def test_every_template_named_in_the_spec_exists():
    assert set(IRISH.templates) == {"VOC", "GEN", "PATRO_O", "PATRO_NI", "ADJ", "OF",
                                    "COMPOUND", "DESC"}
```

- [ ] **Steps 2–4. Step 5: Commit** —
  `feat(rules): irish.rules construction templates (spec §3)`

---

## Task 19: Irish `[normalize]`

**Depends on:** Task 7. **Independent of Tasks 17, 20** (but edits the same rule file as 17/18 —
sequence the commits, or expect a trivial merge).

**Files:**
- Modify: `phonotactics/rules/irish.rules` (add `[normalize]`)
- Modify: `phonotactics/src/strands/irish.py`
- Create: `phonotactics/tests/test_irish_normalize.py`

**Interfaces:**

```python
def normalize(word: Word, rf: RuleFile, table: FeatureTable, *, dialect: str = "C") -> Word
    """Spec §4.1: fold input aliases; give every unmarked consonant ʲ or ˠ from the
    adjacent-vowel convention; mark initial stress for Connacht; leave user-supplied
    phonemes untouched."""
```

Rule content (each line cited):
- **Aliases (I-30):** `lˠ -> l̪ˠ`, `l̠ʲ -> lʲ`, `nˠ -> n̪ˠ`, `n̠ʲ -> nʲ`, `ɑ -> a`, `ɑː -> aː`,
  tagged `%design` with `# tooling alias, digest §1.1`.
- **Quality inference** (digest §5.1, *caol le caol*): a consonant with neither `ʲ` nor `ˠ` takes
  the quality of the **following** vowel if there is one, else the **preceding** vowel: front
  vowel → slender, back/central → broad. Implement as feature-change rules
  `[C -front -back] -> [+front -back] / _ [V +front]` etc., **not** in Python.
- **/h/ before a back vowel surfaces as [ç]** when it is the lenition product of a slender
  consonant: `h -> ç / # _ [V +back]` `%attested # [wiki-irish-phonology §Allophones]`
  (see the note in Task 17).
- **Connacht initial stress** (digest §4.1): handled by the pipeline, not by a rewrite rule —
  `normalize` sets `word.stress = 0` when `dialect == "C"` and no stress mark was supplied,
  and appends a trace entry `stress:irish-initial`. For `dialect == "M"` leave the input's mark
  alone (spec §9 decision 19: Munster/Ulster rows pass through).

- [ ] **Step 1: Failing test**

```python
def test_aliases_fold_to_the_two_way_system():
    assert normalize(w("lˠa"), IRISH, TABLE).segments == ("l̪ˠ", "a")

def test_alpha_folds_to_a():
    assert normalize(w("l̪ˠɑsˠ"), IRISH, TABLE).segments == ("l̪ˠ", "a", "sˠ")

def test_unmarked_consonant_takes_the_following_vowels_quality():
    assert normalize(w("ti"), IRISH, TABLE).segments[0] == "tʲ"
    assert normalize(w("tu"), IRISH, TABLE).segments[0] == "t̪ˠ"

def test_final_unmarked_consonant_takes_the_preceding_vowels_quality():
    assert normalize(w("it"), IRISH, TABLE).segments[-1] == "tʲ"

def test_user_supplied_quality_is_never_overwritten():
    assert normalize(w("t̪ˠiː"), IRISH, TABLE).segments[0] == "t̪ˠ"

def test_connacht_gets_initial_stress_when_unmarked():
    assert normalize(w("mˠat̪ˠaːnˠəx"), IRISH, TABLE, dialect="C").stress == 0

def test_an_explicit_stress_mark_is_preserved():
    x = Word.from_tokenized(tokenize("əˈwaːnʲ", TABLE))
    assert normalize(x, IRISH, TABLE, dialect="C").stress == 1

def test_munster_rows_pass_through_unstressed():
    x = w("kalʲiːnʲ")
    assert normalize(x, IRISH, TABLE, dialect="M").stress is None

def test_every_test_word_normalizes_without_error():
    for row in read_test_words():        # all 144 rows
        normalize(w(row["ipa"]), IRISH, TABLE, dialect=row["dialect"])
```

- [ ] **Steps 2–4. Step 5: Commit** — `feat(rules): irish.rules normalization pre-pass`

---

## Task 20: Input TSV, inference, `lint`

**Depends on:** Task 4. **Independent of Tasks 17 and 19.** Task 18 depends on this task for
the `Entry` record, so land it early.

**Files:**
- Create: `phonotactics/src/strands/inputs.py`
- Create: `phonotactics/tests/test_inputs.py`
- Create: `phonotactics/tests/fixtures/input-sample.tsv`

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
    declension: str = "m1"      # "m1" | "ach" | "f2" | "m3" | "4"; inferred like gender
    gen_ipa: str = ""
    pl_ipa: str = ""
    note: str = ""
    assumptions: tuple[str, ...] = ()

def read_input(path: str | Path) -> list[Entry]
    """Header must contain `orthography`; missing columns default per spec §5.
    Rows with no `ipa` are returned with ipa='' and assumption 'skipped:no-ipa'."""
def infer(entry: Entry) -> Entry
    """Fill gender, gen_ipa, dialect per spec §5, appending an assumption string for
    each guess: 'gender:inferred-ending', 'gen_ipa:inferred-m1', 'dialect:default-C'."""
def lint_report(entries: Sequence[Entry]) -> list[str]
    """One human-readable line per row that has an inferred field."""
def accept_guesses(path: str | Path, entries: Sequence[Entry]) -> None
    """Rewrite the TSV with the guesses filled in (spec §5 `lint --accept`)."""
```

Inference rules (spec §5, verbatim):
- missing `gender` → known-name list first (hard-code the names in `sources/irish/test-words.tsv`
  whose `gloss` states a gender), then ending heuristics (final slender consonant or `-óg`/`-eog`
  → `f`; `-ach`/`-án` → `m`), else `m`.
- missing `gen_ipa` → by declension shape: broad-C-final masculine → slenderize;
  `-ach` → `-aigh`; feminine + C-final → slenderize + `-e`; vowel-final → unchanged.
- missing `dialect` → `C`.
- A construction needing an absent slot is skipped for that row **with a note**, not an error.

- [ ] **Step 1: Failing test** — plus a 6-row fixture covering: full row, no `ipa`, no `gender`,
  no `gen_ipa`, vowel-final, `-ach`.

```python
def test_reads_all_nine_columns():
    entries = read_input(FIX)
    assert entries[0].orthography and entries[0].ipa and entries[0].gloss

def test_row_without_ipa_is_flagged_not_dropped():
    e = [x for x in read_input(FIX) if x.orthography == "NoIpa"][0]
    assert e.ipa == "" and "skipped:no-ipa" in e.assumptions

def test_missing_dialect_defaults_to_C():
    assert infer(Entry(orthography="x", ipa="kaː", dialect="")).dialect == "C"

def test_missing_gender_uses_the_ending_heuristic():
    e = infer(Entry(orthography="Bríd", ipa="bʲɾʲiːdʲ", gender=""))
    assert e.gender == "f" and any(a.startswith("gender:") for a in e.assumptions)

def test_missing_gender_falls_back_to_masculine():
    assert infer(Entry(orthography="Zzz", ipa="zzz", gender="")).gender == "m"

def test_gen_ipa_inferred_by_slenderizing_a_broad_final():
    e = infer(Entry(orthography="mac", ipa="mˠak", gender="m", gen_ipa=""))
    assert e.gen_ipa == "mʲɪc"

def test_gen_ipa_of_an_ach_word():
    e = infer(Entry(orthography="marcach", ipa="mˠaɾˠkəx", gender="m", gen_ipa=""))
    assert e.gen_ipa.endswith("j")

def test_vowel_final_gen_ipa_is_unchanged():
    e = infer(Entry(orthography="balla", ipa="bˠal̪ˠə", gen_ipa=""))
    assert e.gen_ipa == "bˠal̪ˠə"

def test_lint_report_lists_one_line_per_guess():
    lines = lint_report([infer(x) for x in read_input(FIX)])
    assert any("gender" in l for l in lines) and all(l.strip() for l in lines)

def test_accept_writes_the_guesses_back(tmp_path):
    dst = tmp_path / "out.tsv"
    shutil.copy(FIX, dst)
    accept_guesses(dst, [infer(x) for x in read_input(dst)])
    assert all(r["gender"] for r in csv.DictReader(dst.open(encoding="utf-8"), delimiter="\t"))

def test_reading_the_real_test_words_file_works():
    entries = read_input(ROOT / "sources" / "irish" / "test-words.tsv")
    assert len(entries) == 144
```

*(`sources/irish/test-words.tsv` has columns `orthography ipa dialect gloss category features
note` — not the spec §5 header. `read_input` must accept any superset/subset of `INPUT_COLUMNS`
keyed by header name, ignoring unknown columns like `features`. Assert that.)*

- [ ] **Steps 2–4. Step 5: Commit** — `feat(strands): input TSV reader, field inference, lint`

**Acceptance:** milestone 5 complete (Tasks 17–20).

---

## Task 21: Pipeline orchestrator, respell, epithet stage

**Depends on:** Tasks 9, 11, 13, 14, 15, 16, 18, 19

**Files:**
- Create: `phonotactics/src/strands/respell.py`
- Create: `phonotactics/src/strands/pipeline.py`
- Create: `phonotactics/tests/test_pipeline.py`
- Create: `phonotactics/tests/fixtures/toy-target.rules` (a complete target file, ~30 lines, that
  exercises every stage — this is the pipeline's test double so the pipeline can be finished and
  reviewed before any real target file exists)

**Interfaces:**

```python
def respell(word: Word, rf: RuleFile, table: FeatureTable) -> str
    """Spec §4.7: apply rf.sections['respell'] over the segment string (marks included
    per I-19) and return the resulting text."""
def affix_epithet(word: Word, name: str, rf: RuleFile, table: FeatureTable) -> Word
    """Spec §4.6: attach rf.epithets[name].form at the position its environment matches,
    inserting a '$'; the caller re-runs stages 3-5."""

@dataclass(frozen=True)
class Result:
    respelling: str
    ipa: str                       # with stress and syllable marks
    flags: tuple[str, ...]
    fallbacks: int
    assumptions: tuple[str, ...]
    trace: tuple[TraceEntry, ...]
    words: tuple[Word, ...]        # one per space-separated word

def adapt(words: Sequence[Word], target: RuleFile, table: FeatureTable,
          *, epithet: str | None = None) -> Result
    """Stages 2-7 of spec §4 for one construction's word list."""

def run_entry(entry: Entry, construction: str, irish: RuleFile, target: RuleFile,
              table: FeatureTable, slots: dict[str, Entry] | None = None) -> Result
    """Stage 1 (irish pre-pass) then adapt()."""

def load_target(name: str, table: FeatureTable) -> RuleFile
    """name in {'welsh','arabic-egy','georgian','dutch'}; reads rules/<name>.rules."""
TARGETS = ("welsh", "arabic-egy", "georgian", "dutch")
```

- [ ] **Step 1: Failing test** — `tests/test_pipeline.py`

```python
TOY = parse_rules_file(FIXTURES / "toy-target.rules", TABLE)

def test_stage_order_appears_in_the_trace():
    r = adapt([w("pˠaːdˠɾˠəɟ")], TOY, TABLE)
    stages = [t.stage for t in r.trace]
    order = [s for s in ("substitute", "syllabify", "repair", "stress", "post-stress", "respell")
             if s in stages]
    assert order == sorted(order, key=["substitute", "syllabify", "repair", "stress",
                                       "post-stress", "respell"].index)

def test_result_carries_ipa_respelling_flags_and_fallbacks():
    r = adapt([w("pˠaːdˠɾˠəɟ")], TOY, TABLE)
    assert r.ipa and r.respelling and isinstance(r.flags, tuple) and r.fallbacks >= 0

def test_multiword_constructions_are_adapted_separately_and_rejoined():
    r = adapt([w("mˠaːɾʲə"), w("bˠaːnˠ")], TOY, TABLE)
    assert " " in r.respelling and " " in r.ipa

def test_epithet_affixation_reruns_syllabification_and_stress():
    r = adapt([w("kaː")], TOY, TABLE, epithet="NISBA")
    assert r.ipa.endswith("i")
    # the stress mark moved because the word gained a syllable
    assert r.trace[-1].stage == "respell"

def test_pipeline_is_deterministic():
    a = adapt([w("pˠaːdˠɾˠəɟ")], TOY, TABLE)
    b = adapt([w("pˠaːdˠɾˠəɟ")], TOY, TABLE)
    assert a == b

def test_every_output_segment_is_in_the_target_inventory():
    r = adapt([w("ˈl̪ˠasˠəɾʲxosˠ")], TOY, TABLE)
    for word in r.words:
        assert set(word.segments) <= set(TOY.inventory)

def test_run_entry_applies_the_irish_prepass_first():
    r = run_entry(Entry(orthography="Seán", ipa="ʃaːnˠ", declension="m1"), "VOC",
                  IRISH, TOY, TABLE)
    assert any(t.stage == "mutation" for t in r.trace)

def test_unknown_target_name_raises():
    with pytest.raises(Exception):
        load_target("klingon", TABLE)
```

- [ ] **Steps 2–4. Step 5: Commit** — `feat(strands): stage pipeline, epithet affixation, respell`

**Acceptance:** the toy target file runs end-to-end from an `Entry` to a respelling with a full
trace; determinism holds.

---

## Task 22: Regression harness and ratchet

**Depends on:** Task 21

**Files:**
- Create: `phonotactics/src/strands/regress.py`
- Create: `phonotactics/tests/test_regression_harness.py`
- Create: `phonotactics/tests/ratchets/` (directory; per-target JSON files land here in Tasks 23–26)

**Read I-25 before starting: the attested data does not support the spec's end-to-end regression
for three of four targets.** This task builds both modes.

**Interfaces:**

```python
@dataclass(frozen=True)
class RegressionRow:
    source_form: str
    source_ipa: str
    target_form: str
    target_ipa: str
    provenance: str
    mode: str          # "E" (end-to-end) | "L" (legality) | "skip"
    passed: bool
    got: str
    distance: int      # segment-level edit distance between got and target_ipa

@dataclass(frozen=True)
class RegressionReport:
    target: str
    mode_e: tuple[RegressionRow, ...]
    mode_l: tuple[RegressionRow, ...]
    def rate(self, mode: str) -> float
    def summary(self) -> str

def read_attested(target: str) -> list[dict[str, str]]
    """sources/<target>/attested.tsv; drops rows whose note starts with
    'PREDICTED-NOT-ATTESTED:' (arabic-egy has 11 such rows)."""
def run_regression(target: str, table: FeatureTable) -> RegressionReport
def load_ratchet(target: str) -> dict[str, float]
def assert_ratchet(report: RegressionReport, tolerance: float = 0.0) -> None
    """Fails if either mode's rate is below the committed ratchet value."""
def write_ratchet(report: RegressionReport) -> None      # invoked by hand, never by tests
```

Mode definitions (I-22, I-25):
- **Mode E** — rows with non-empty `source_ipa` *and* `target_ipa`: tokenize the source IPA, run
  `adapt()` with the target rule file, compare to `target_ipa` after NFC and after stripping marks
  the attested row does not carry.
- **Mode L** — rows with `target_ipa` only: tokenize the *target* IPA against the target
  inventory, syllabify, and require `illegal == frozenset()` and every segment in `[inventory]`.
  If the row's `target_ipa` carries a stress mark, additionally require the file's stress procedure
  to reproduce it.
- Rows with neither IPA side are `mode="skip"` and excluded from both rates.

- [ ] **Step 1: Failing test** — `tests/test_regression_harness.py`

```python
def test_read_attested_drops_predicted_rows():
    rows = read_attested("arabic-egy")
    assert len(rows) == 301                      # 312 data rows - 11 PREDICTED-NOT-ATTESTED
    assert not any(r["note"].startswith("PREDICTED-NOT-ATTESTED") for r in rows)

def test_row_counts_match_the_committed_data():
    assert len(read_attested("georgian")) == 143
    assert len(read_attested("welsh")) == 751
    assert len(read_attested("dutch")) == 90

def test_mode_assignment():
    rows = read_attested("dutch")
    both = [r for r in rows if r["source_ipa"] and r["target_ipa"]]
    assert len(both) == 32                       # the only Mode E rows in the whole project

def test_report_rate_is_a_fraction_of_non_skipped_rows():
    rep = run_regression("dutch", TABLE)         # against the toy file until Task 26 lands
    assert 0.0 <= rep.rate("L") <= 1.0

def test_ratchet_failure_is_loud(tmp_path):
    rep = RegressionReport(target="x", mode_e=(), mode_l=(FAILING_ROW,))
    with pytest.raises(AssertionError):
        assert_ratchet(rep_with_ratchet(rep, {"L": 1.0}))

def test_edit_distance_is_reported_for_near_misses():
    row = RegressionRow(..., got="kalb", target_ipa="kalp", ...)
    assert row.distance == 1
```

*(Until Tasks 23–26 land there is no `rules/<target>.rules`; `run_regression` must raise a clear
`FileNotFoundError`-derived message, and the tests above that need a rule file are marked
`pytest.mark.skipif(not rules_exist(target))`. Write them that way.)*

- [ ] **Steps 2–4. Step 5: Commit** — `feat(strands): attested-data regression harness with ratchet`

**Acceptance:** row counts above are reproduced exactly; the harness runs against a missing rule
file without crashing the suite.

---

## Tasks 23–26: the four target rule files

These four are **mutually independent** and can be executed in parallel by four agents once Tasks
21 and 22 are committed. They share a common shape, stated once here and then specialized.

**Common shape for each target task:**

**Files:** create `phonotactics/rules/<target>.rules`,
`phonotactics/tests/test_rules_<target>.py`, `phonotactics/tests/ratchets/<target>.json`.

**Method (follow in order):**
1. Read the named digest sections. Transcribe them into rule lines. **Every line gets a citation
   comment** — `# [bibkey p.N]` copied from the digest, or `# design: §9.n` naming the spec §9 row,
   or `# design: digest §N open` for an I-29 resolution.
2. Run `uv run strands check rules/<target>.rules` — zero errors before writing any test.
3. Write the unit tests below (they are the "tests first" for the *rule content*: each asserts a
   named digest fact, so they fail against an empty file).
4. Run the regression harness; record the measured Mode L / Mode E rates in
   `tests/ratchets/<target>.json` as `{"L": <measured>, "E": <measured>}` **only after** the
   acceptance bar below is met.
5. Commit rule file + tests + ratchet together.

**Common tests every target task must include:**

```python
TARGET = load_target("<name>", TABLE)

def test_rule_file_parses_and_checks_clean():
    assert check_rule_file(TARGET, TABLE) == [] or all(e.code == "OFF_INVENTORY"
                                                       for e in check_rule_file(TARGET, TABLE))

def test_every_rule_line_carries_a_citation():
    for section in TARGET.sections.values():
        for r in section:
            assert r.comment.strip(), r.rule_id
            assert ("[" in r.comment or "design:" in r.comment), (r.rule_id, r.comment)

def test_every_irish_segment_survives_the_pipeline():
    # spec §7 + user decision 2: word-initial /w x ɣ ç j h ŋ ɲ/ and mutation clusters must work
    for seg in "w x ɣ ç j h ŋ ɲ".split():
        r = adapt([w(seg + "aː")], TARGET, TABLE)
        assert set(r.words[0].segments) <= set(TARGET.inventory)
        assert "UNREPAIRED" not in r.flags

def test_no_unrepaired_on_the_144_word_set():
    unrepaired = [row["orthography"] for row in read_test_words()
                  if "UNREPAIRED" in run_entry(entry_of(row), "DESC", IRISH, TARGET, TABLE).flags]
    assert unrepaired == [], unrepaired      # or: assert set(unrepaired) <= ALLOWED (a committed allow-list)

def test_regression_meets_the_acceptance_bar():
    rep = run_regression("<name>", TABLE)
    assert rep.rate("L") >= <bar>, rep.summary()

def test_regression_ratchet_does_not_slip():
    assert_ratchet(run_regression("<name>", TABLE))
```

---

### Task 23: `georgian.rules`

**Depends on:** 21, 22. **Digest:** `sources/georgian/digest.md`.

| Rule block | Transcribed from |
|---|---|
| `[inventory]` | §1.1 consonant chart (Shosted 2006 p.255), §1.2–§1.8 deltas, §1.9 net delta vs PHOIBLE 2183 |
| `[substitute]` /p t k/ → pʰ tʰ kʰ, `[STOP -voice] -> [+ejective] / C_` | §3.1 (Gabunia's *measured* pattern), spec §9 rows 4–5 |
| `[substitute]` f→pʰ, ŋ→n, j→i | §3.2 (note: the digest's data show ŋ→/ng/; spec §7 fixes `→ n` — follow the spec, cite both) |
| `[substitute]` w→v | §3.3, spec §9 row 6 |
| `[substitute]` slender coronals → ʃ ʒ tʃʰ dʒ | §8.1, §8.2; `%design`, spec §9 rows 1–2 |
| `[substitute]` broad non-labial C → C v / _[V +front]; slender C → C i / _[V +back] | §8.1; `%design`, spec §9 row 3 (**Cʷ is ON**, restricted to onsets before /i e/, per `notes/project-goals.md` decision 5 of 2026-08-25) |
| `[substitute]` long → short; diphthong V.V | §3.4, §8.3 |
| `[syllable]` template = any, domain = stem, sonority = off | §2.1, §2.7 (I-27) |
| `[syllable] onsets` | §2.2 harmonic-cluster table (53) p.103 — all 32 — plus §2.3 Appendix 2 stem-initial list (thesis pp.197–205) |
| `[syllable] codas` | §2.5 Appendix 3 stem-final list (pp.207–209) |
| `[syllable] bans` | §2.6 co-occurrence restrictions, table (62) p.110; §2.9 (VV barred monomorphemically); §2.10 (no geminates) |
| `[repair]` degemination | §3.6 (exceptionless) |
| `[repair]` whitelist miss → nearest attested cluster, `%fallback` | §3.0, §3.7 (no cluster repair is observed — the fallback is ours) |
| `[stress]` procedure = initial, mark = off | §4.1, §4.3 |
| `[epithets]` -i, -uri/-uli, -eli, syncope before -eb- | §6.1, §6.2, §6.3, §6.4 |
| `[respell]` national 2002 + overlays | §5.1 (33-letter table), §5.3 (deviations D1–D5: `x`, `tch`, `ch`, `y`, bare stem) |

**Digest-fact tests (write these first):**

```python
def test_irish_p_t_k_become_aspirates_by_default():
    assert adapt([w("pˠaː")], TARGET, TABLE).words[0].segments[0] == "pʰ"

def test_stops_after_a_consonant_become_ejectives():
    # digest §3.1: the measured Gabunia pattern
    ...

def test_f_becomes_aspirated_p():
    assert "pʰ" in adapt([w("fˠaː")], TARGET, TABLE).words[0].segments

def test_broad_nonlabial_before_front_vowel_gets_a_v():   # Cʷ, decision 5
    out = adapt([w("kiː")], TARGET, TABLE).words[0].segments
    assert out[:2] == ("kʰ", "v") or out[:2] == ("kʼ", "v")

def test_slender_consonant_before_back_vowel_gets_an_i():
    assert "i" in adapt([w("tʲuː")], TARGET, TABLE).words[0].segments

def test_vv_from_a_double_v_degeminates():
    # decision 5: /vv/ from collision with lenited b/m degeminates to /v/
    ...

def test_all_32_harmonic_clusters_are_licit_onsets():
    for cl in HARMONIC_CLUSTERS:        # transcribed from digest §2.2 table (53)
        assert legal_onset(cl, TARGET.syllable, TABLE), cl

def test_personal_names_are_emitted_as_a_bare_stem():
    # digest §6.1 + goals decision 4: no nominative -i on personal names
    assert not adapt([w("kaː")], TARGET, TABLE).respelling.endswith("i")

def test_common_noun_epithets_keep_the_nominative_i():
    assert adapt([w("kaː")], TARGET, TABLE, epithet="NOM_I").respelling.endswith("i")

def test_respelling_uses_apostrophe_for_ejectives_and_x_not_kh():
    # digest §5.3 D1-D5
    ...

def test_the_five_existing_strand4_names_are_reachable_shapes():
    # Tchaeul, Th'tysh, Kas'queil, Xelxyx, Ysclyth (notes/project-goals.md):
    # assert the respell layer can produce ', x, tch, y for the corresponding IPA
    ...
```

**Acceptance bar:** Mode L pass rate **≥ 0.80** over the 143 attested rows (all carry
`target_ipa`; none carries `source_ipa`, so Mode E is empty — assert `rep.mode_e == ()`).
Mode L failures below that bar mean the `[syllable]` whitelists were transcribed incompletely.

**Commit:** `feat(rules): georgian.rules — strand 4 target (digest §1-§6, spec §9.3-§9.8)`

---

### Task 24: `arabic-egy.rules`

**Depends on:** 21, 22. **Digest:** `sources/arabic-egy/digest.md`.

| Rule block | Transcribed from |
|---|---|
| `[inventory]` | §1 "Consonants — the working inventory", §1 "Vowels", §1 notational quirks |
| `[substitute]` p→b, v→f, ʒ→ʃ, dʒ→ʒ, θ→t, ð→z, ŋ→n | §3.6 table; ŋ per spec §9 row 12 (`%design`) |
| `[substitute]` broad coronals → emphatics; slender coronals → plain; /sʲ/→ʃ | §8.1 (Cairene over-assigns emphasis to loans before back vowels — the attested precedent), spec §9 rows 1, 9 |
| `[substitute]` x ɣ h kept; /ə/ → a/i by position | §8.3, §3.8 |
| `[substitute]` long vowels kept (then pruned by §3.8 length rules) | §3.8 (this resolves the digest's open decision per I-29 — cite it) |
| `[syllable]` template = CV(C)(C), onsets = every single C only, no clusters | §2 "Maximal syllable template", §2 "Onsets" (I-28); medial coda max 1C, CCC banned → `bans` |
| `[repair]` `0 -> i / # C _ C V` (anaptyxis) | §3.1(a) — *freezer*→*firizar*, *plastic*→*bilastik* |
| `[repair]` `0 -> ʔ i / # _ s [C -sonorant]` (prothesis) | §3.1(b) — *ski*→*ʔiskii*, *study*→*ʔistadi* |
| `[repair]` `0 -> i / C C _ C` (CCC, after C2) | §3.2 — *bankinut*, *bustiman* |
| `[repair]` epenthetic quality: /i/, harmonizing to /u/ before a round vowel | §3.3 — *group*→*guruub* |
| `[repair]` `0 -> ʔ / # _ V` | §3.7 |
| `[repair]`/`[post-stress]` closed-syllable shortening, unstressed-long shortening, mid raising, one-long-vowel-per-word, high-vowel syncope | §3.8 items 1–6 |
| `[repair]` degemination; no final devoicing; no emphasis spread | §2 gemination, §3.9, spec §9 row 10 |
| `[stress]` procedure = cairene | §4 (implemented in Task 14) |
| `[epithets]` NISBA -i/-iyya, FEM -a, DEF il- with sun letters | §6.1 (sun-letter list), §6.2 (11 worked nisba examples), §6.3 |
| `[respell]` kh gh q ʼ h, emphatics dot-under, long vowels doubled | §5 "Recommended output convention" (~20 rows), spec §9 row 11 |

**Digest-fact tests (write these first):**

```python
@pytest.mark.parametrize("src,expected", [("pˠ", "b"), ("vʲ", "f")])
def test_absent_segments_substitute_per_digest_3_6(src, expected): ...

def test_broad_coronal_becomes_emphatic():
    assert adapt([w("sˠaː")], TARGET, TABLE).words[0].segments[0] == "sˤ"

def test_slender_s_becomes_sh():
    assert adapt([w("ʃaː")], TARGET, TABLE).words[0].segments[0] == "ʃ"

def test_initial_obstruent_liquid_cluster_gets_anaptyxis():
    # digest §3.1(a): CCV -> CiCV
    out = adapt([w("bʲlʲaː")], TARGET, TABLE).words[0].ipa(marks=False)
    assert out[1] == "i" or out.startswith("bi")

def test_initial_s_stop_cluster_gets_prothesis_not_anaptyxis():
    # digest §3.1(b): #sC -> ʔiC
    assert adapt([w("sˠkaː")], TARGET, TABLE).words[0].segments[0] == "ʔ"

def test_ccc_epenthesis_lands_between_c2_and_c3():
    # digest §3.2, the Cairene/Iraqi split
    ...

def test_vowel_initial_word_gets_a_glottal_stop():
    assert adapt([w("aːnˠ")], TARGET, TABLE).words[0].segments[0] == "ʔ"

def test_only_one_long_vowel_survives_per_word():
    out = adapt([w("baːtaːnˠ")], TARGET, TABLE).words[0].segments
    assert sum(1 for s in out if s.endswith("ː")) <= 1     # digest §3.8 item 4

def test_no_final_obstruent_devoicing():
    assert adapt([w("bˠaːdˠ")], TARGET, TABLE).words[0].segments[-1] == "d"

def test_nisba_epithet_attaches_and_restresses():
    r = adapt([w("mˠasˠɾˠ")], TARGET, TABLE, epithet="NISBA")
    assert r.ipa.endswith("i")

def test_definite_article_assimilates_to_sun_letters():
    # digest §6.1: il- + /s/ -> is-s
    ...

def test_emphatics_are_respelled_with_a_dot_under():
    assert "ṣ" in adapt([w("sˠaː")], TARGET, TABLE).respelling
```

**Acceptance bar:** Mode L pass rate **≥ 0.75** over the attested rows that carry `target_ipa`
(of 301 real rows; the harness reports the denominator). Mode E is empty (no `source_ipa`) —
assert it. Additionally: **all 16 Cairene stress rows from Task 14 must still pass** with the real
inventory, so re-run `tests/test_stress_cairene.py` against `arabic-egy.rules` (parametrize the
existing test over both the toy file and the real one).

**Commit:** `feat(rules): arabic-egy.rules — Cairene target (digest §1-§6, spec §9.9-§9.12)`

---

### Task 25: `welsh.rules`

**Depends on:** 21, 22. **Digest:** `sources/welsh/digest.md`. **Read I-26 first.**

| Rule block | Transcribed from |
|---|---|
| `[inventory]` | §1 "Southern consonant inventory as the sources support it", §1 "Southern vowel inventory", §1 add/remove lists |
| `[substitute]` /sʲ/→ʃ, /tʲ/→tʃ, /dʲ/→dʒ | §8.1; `%attested` where §8.1 cites a Welsh source, else `%design` (spec §9 row 1) |
| `[substitute]` other slender/broad → plain | §8.1; `%design` |
| `[substitute]` ɣ→g, x→χ, h/w/ŋ kept | §8.2, §8.3, §8.4, §8.8 |
| `[substitute]` voiceless sonorants | §8.5 (they are not Irish phonemes — assert they never arrive) |
| `[syllable]` template = (C)(C)(C)V(V)(C)(C) | §2.1 |
| `[syllable] onsets` + `onsets-tier` | §2.2, tiers **A/B/C/D exactly as the digest labels them** (A stated class, B lexically attested, C conjecture, D disputed) |
| `[syllable] codas` | §2.3 (tier B only — record the tier) |
| `[syllable] sonority = on` | §2.2 |
| `[repair]` `l -> ɬ / #_`, `r -> r̥ / #_` | §3.3; `%design`, spec §9 row 14 (ON) |
| `[repair]` `0 -> ə / # _ s [STOP]` (sC prothesis, written `y`) | §3.1; the digest offers three non-converging encodings and chooses none — take Parry-Williams' scope (`#_s{p,t,k}`), tag `%design`, cite spec §9 row 15 |
| `[repair]` final-cluster epenthesis `0 -> Vᵢ / Vᵢ C _ {l n r} #` | §3.2 rule (1) — *pobl* → [ˈpɔbɔl] |
| `[repair]` liquid deletion `{l r} -> 0 / C _ #` when epenthesis would make stress antepenultimate | §3.2 rule (2) — *ffenestr* → [ˈfɛnɛst] |
| `[repair]` metathesis `C θ r # -> C r θ #` | §3.2 rule (3) — *ewythr* → [ˈewɨrθ] |
| `[repair]` degemination | §2.7 |
| `[stress]` procedure = penult | §4.1; spec §9 row 13 (Welsh-first) |
| `[post-stress]` the Southern length rule | §4.3's **7-row environment table** (I-26): open final syllable → long; before {b d g v ð f θ χ} → long; before {s ʃ ɬ} → long (South only); before {pʰ tʰ kʰ m ŋ} → short; before {w j} → short; before CC → short; before {n l r} → lexically unpredictable, so **leave unchanged** and tag `%design` |
| `[epithets]` -og, -ol, -aidd, -us, -gar, -lyd, -yn/-en | §6 (10-suffix table); note -og ≅ Irish -ach |
| `[respell]` v ff ch dd ll c si/sh, `y` for the prothetic ə | §5 (26 consonant rows + 7 vowels + diphthongs) |

**Digest-fact tests (write these first):**

```python
def test_slender_coronals_map_to_the_welsh_palatal_series():
    assert adapt([w("ʃaː")], TARGET, TABLE).words[0].segments[0] == "ʃ"
    assert adapt([w("tʲaː")], TARGET, TABLE).words[0].segments[0] == "tʃ"

def test_irish_gamma_becomes_g():
    assert adapt([w("ɣaː")], TARGET, TABLE).words[0].segments[0] == "ɡ"

def test_initial_l_fortifies_to_ll():
    r = adapt([w("l̪ˠaː")], TARGET, TABLE)
    assert r.words[0].segments[0] == "ɬ" and r.respelling.startswith("ll")

def test_initial_r_fortifies_to_rh():
    assert adapt([w("ɾˠaː")], TARGET, TABLE).respelling.startswith("rh")

def test_sc_prothesis_is_written_y():
    r = adapt([w("sˠkaː")], TARGET, TABLE)
    assert r.words[0].segments[0] == "ə" and r.respelling.startswith("y")

def test_pobl_type_epenthesis():
    # digest §3.2 rule (1): copy epenthesis before a final liquid/nasal
    ...

def test_ffenestr_type_liquid_deletion():
    ...

def test_stress_is_penultimate_and_length_is_recomputed_after_it():
    r = adapt([w("mˠat̪ˠaːnˠəx")], TARGET, TABLE)
    assert "ˈ" in r.ipa

def test_southern_length_rule_lengthens_before_a_voiced_fricative():
    # digest §4.3 row 2
    ...

def test_tier_labels_survive_into_the_trace():
    # an onset drawn from a B-tier cluster is recorded as such (spec §3: informational)
    ...
```

**Acceptance bar:** Mode L pass rate **≥ 0.70** over the **19** rows that carry `target_ipa`
(i.e. ≥ 13 of 19). Mode E is empty. Because 732 of the 751 rows carry orthography only, also add a
weaker **Mode O smoke check** in this task's tests: for each of the 93 `layer=modern` rows, assert
the harness classifies the row as `skip` rather than crashing. Do **not** attempt orthographic
comparison — that needs a Welsh G2P, which is out of scope.

**Commit:** `feat(rules): welsh.rules — Southern Welsh target (digest §1-§6, spec §9.13-§9.15)`

---

### Task 26: `dutch.rules`

**Depends on:** 21, 22. **Digest:** `sources/dutch/digest.md`.

| Rule block | Transcribed from |
|---|---|
| `[inventory]` | §1 (Verhoeven's chart; parenthesised = marginal → `marginal:` line), §1 vowels |
| `[substitute]` slender C → C j in onsets, plain in codas | §8.1; `%design`, spec §9 row 16 |
| `[substitute]` broad → plain; ɣ x h kept; ʃ kept; w→ʋ | §8.2, §3.4 |
| `[substitute]` length → tense/lax table | §8.3, §3.6 (the digest's own proposal, explicitly not sourced → `%fallback`) |
| `[substitute]` ə kept | §8.3 |
| `[syllable]` template: onset ≤3 (first = /s/ if 3), rhyme-coda ≤2 | §2 "Maximal template", "Coda size" |
| `[syllable] onsets` / `codas` | §2 "Onsets — singletons / CC / CCC" (~28 native + ~24 loan CC, all CCC); §2 "Coda clusters" by class |
| `[syllable] appendix = s t` | §2 "Coda size" (appendix ≤3 coronal obstruents) |
| `[syllable] bans` | §2 "The two restrictions that bite hardest": (a) tense-V/voiced-fricative pact — the ban bites only on stressed /Vːx Vːf Vːs/; (b) Kager & Pater `*[V +long] C C [-coronal]`, with the final-coronal-appendix escape hatch |
| `[repair]` final obstruent devoicing | §3.5 — *hand* [hɑnt]; cohering suffixes do not trigger, `-aardig`/`-achtig` do |
| `[repair]` `0 -> ə / [liquid] _ C` non-homorganic, blocked before /s t/ | §3.2 — *melk* [mɛl(ə)k]; blocked in *hals*, *hart*, *herfst* |
| `[repair]` tense-V + voiceless fricative → voice the fricative | §9 item 5 / §8.6; `%design`, spec §9 row 18 |
| `[repair]` degemination | §2 "Medial clusters, gemination, hiatus" |
| `[repair]` no onset-cluster repair | §3.1 (an explicit finding: loans keep illicit onsets) — encode as a comment, not a rule |
| `[stress]` procedure = dutch-weight | §4 "The practical rule"; `%design`, spec §9 row 17 |
| `[epithets]` -achtig, -ig, -(t)je (allomorphs -je/-tje/-pje/-etje/-kje) | §6 (10-item table) |
| `[respell]` oo/ee/aa, gh/kh, w, uy/eu/oo + the doubling algorithm | §5 "Phoneme → spelling", §5 "The doubling algorithm" (6 steps, implement verbatim) |

**Digest-fact tests (write these first):**

```python
def test_slender_consonant_in_an_onset_gets_a_yod():
    assert adapt([w("tʲaː")], TARGET, TABLE).words[0].segments[:2] == ("t", "j")

def test_slender_consonant_in_a_coda_is_plain():
    assert adapt([w("aːtʲ")], TARGET, TABLE).words[0].segments[-1] == "t"

def test_final_obstruent_devoicing():
    assert adapt([w("bˠaːdˠ")], TARGET, TABLE).words[0].segments[-1] == "t"

def test_liquid_schwa_epenthesis_before_a_nonhomorganic_consonant():
    # melk -> mɛlək (digest §3.2)
    ...

def test_epenthesis_is_blocked_before_a_coronal_appendix_obstruent():
    # hart never *hɑrət (digest §3.2)
    ...

def test_matanach_does_not_trigger_the_fricative_ban():
    # notes/project-goals.md + digest §2: the /x/ follows schwa, not the long vowel
    r = adapt([w("mˠat̪ˠaːnˠəx")], TARGET, TABLE)
    assert r.words[0].segments[-1] == "x"

def test_long_vowel_directly_before_a_voiceless_fricative_voices_it():
    # bách -> the ban bites (spec §9 row 18: voice the fricative)
    ...

def test_kager_pater_ban_is_enforced():
    # *[Vː] C C[-coronal]
    ...

def test_doubling_algorithm_in_the_respelling():
    # long vowel in a closed syllable doubles the letter; short vowel before a single
    # intervocalic C doubles the consonant letter (digest §5, 6 steps)
    ...

def test_dutch_weight_stress_is_used():
    assert "ˈ" in adapt([w("mˠat̪ˠaːnˠəx")], TARGET, TABLE).ipa
```

**Acceptance bar:** Mode L pass rate **≥ 0.80** over the **67** rows carrying `target_ipa`, **and**
Mode E pass rate **≥ 0.25** over the **32** rows carrying both sides (8 of 32). Mode E is low by
design: those rows are English→Dutch loans adapted by donor-specific routes, while this rule file
is tuned for Irish input; the value is the ratchet, not the absolute number. Record both measured
rates in `tests/ratchets/dutch.json`.

**Commit:** `feat(rules): dutch.rules — Belgian Dutch target (digest §1-§6, spec §9.16-§9.18)`

---

## Task 27: CLI — `run`, `explain`, `gallery`, `lint`

**Depends on:** Tasks 21, 20

**Files:**
- Modify: `phonotactics/src/strands/cli.py`
- Create: `phonotactics/src/strands/gallery.py`
- Create: `phonotactics/tests/test_cli.py`

**Interfaces (spec §6, exactly):**

```
strands run   INPUT.tsv [--strand welsh|arabic-egy|georgian|dutch|all] [--construction NAME|all] [--out out.tsv]
strands explain WORD --strand X [--construction NAME]
strands gallery INPUT.tsv [--out gallery.md]
strands lint  INPUT.tsv [--accept]
strands check RULES.rules
```

```python
def cmd_run(args) -> int          # writes TSV: orthography, construction, strand,
                                  # respelling, ipa, flags, fallbacks, assumptions
def cmd_explain(args) -> int      # prints the trace: stage, rule_id, tag, before -> after,
                                  # plus the rule's citation comment
def cmd_gallery(args) -> int
def cmd_lint(args) -> int
def render_gallery(entries, targets, constructions, table) -> str   # gallery.py
```

- [ ] **Step 1: Failing test** — `tests/test_cli.py`

```python
def test_run_writes_one_row_per_word_construction_strand(tmp_path):
    out = tmp_path / "o.tsv"
    assert main(["run", str(FIX), "--strand", "all", "--construction", "DESC", "--out", str(out)]) == 0
    rows = list(csv.DictReader(out.open(encoding="utf-8"), delimiter="\t"))
    assert {r["strand"] for r in rows} == set(TARGETS)
    assert set(rows[0]) == {"orthography", "construction", "strand", "respelling", "ipa",
                            "flags", "fallbacks", "assumptions"}

def test_run_is_deterministic(tmp_path):
    a, b = tmp_path / "a.tsv", tmp_path / "b.tsv"
    main(["run", str(FIX), "--out", str(a)]); main(["run", str(FIX), "--out", str(b)])
    assert a.read_bytes() == b.read_bytes()

def test_explain_prints_stages_rule_ids_and_citations(capsys):
    assert main(["explain", "ˈkiəɾˠə", "--strand", "welsh"]) == 0
    out = capsys.readouterr().out
    assert "substitute" in out and "syllabify" in out and "->" in out
    assert "[" in out            # a citation from the rule's comment

def test_explain_rejects_an_unknown_strand():
    assert main(["explain", "kaː", "--strand", "klingon"]) == 2

def test_gallery_emits_markdown_with_a_row_per_word(tmp_path):
    out = tmp_path / "g.md"
    assert main(["gallery", str(FIX), "--out", str(out)]) == 0
    text = out.read_text(encoding="utf-8")
    assert text.startswith("#") and "|" in text

def test_lint_lists_inferred_fields(capsys):
    assert main(["lint", str(FIX)]) == 0
    assert "gender" in capsys.readouterr().out

def test_lint_accept_rewrites_the_file(tmp_path):
    dst = tmp_path / "in.tsv"; shutil.copy(FIX, dst)
    before = dst.read_text(encoding="utf-8")
    assert main(["lint", str(dst), "--accept"]) == 0
    assert dst.read_text(encoding="utf-8") != before

def test_run_skips_a_construction_whose_slot_is_missing(tmp_path):
    # spec §5: skipped with a note, not an error
    out = tmp_path / "o.tsv"
    assert main(["run", str(FIX), "--construction", "PATRO_O", "--out", str(out)]) == 0
    rows = list(csv.DictReader(out.open(encoding="utf-8"), delimiter="\t"))
    assert any("skipped" in r["assumptions"] for r in rows)

def test_row_with_no_ipa_is_skipped_with_a_note(tmp_path):
    ...
```

- [ ] **Steps 2–4. Step 5: Commit** — `feat(strands): run/explain/gallery/lint subcommands`

---

## Task 28: Gallery snapshot and property checks

**Depends on:** Tasks 27, 23, 24, 25, 26

**Files:**
- Create: `phonotactics/tests/snapshots/gallery.md` (generated, then committed)
- Create: `phonotactics/tests/test_properties.py`
- Create: `phonotactics/tests/test_gallery_snapshot.py`
- Create: `phonotactics/tests/allow-unrepaired.txt` (empty at first; each line
  `<target>\t<orthography>\t<reason>`)

**Interfaces:** none new.

- [ ] **Step 1: Write the failing tests**

```python
# test_gallery_snapshot.py
def test_gallery_matches_the_committed_snapshot(tmp_path):
    out = tmp_path / "g.md"
    main(["gallery", str(ROOT / "sources" / "irish" / "test-words.tsv"), "--out", str(out)])
    expected = (ROOT / "tests" / "snapshots" / "gallery.md").read_text(encoding="utf-8")
    assert out.read_text(encoding="utf-8") == expected, \
        "gallery changed — regenerate the snapshot and review the diff in the commit"

# test_properties.py  (spec §8 layer 5)
def test_determinism_across_two_runs():
    for target in TARGETS:
        rf = load_target(target, TABLE)
        for row in read_test_words():
            a = run_entry(entry_of(row), "DESC", IRISH, rf, TABLE)
            b = run_entry(entry_of(row), "DESC", IRISH, rf, TABLE)
            assert a == b

def test_every_output_segment_is_in_the_target_inventory():
    for target in TARGETS:
        rf = load_target(target, TABLE)
        for row in read_test_words():
            r = run_entry(entry_of(row), "DESC", IRISH, rf, TABLE)
            for word in r.words:
                assert set(word.segments) <= set(rf.inventory), (target, row["orthography"])

def test_no_unrepaired_outside_the_allow_file():
    allowed = read_allow_file()
    failures = []
    for target in TARGETS:
        rf = load_target(target, TABLE)
        for row in read_test_words():
            r = run_entry(entry_of(row), "DESC", IRISH, rf, TABLE)
            if "UNREPAIRED" in r.flags and (target, row["orthography"]) not in allowed:
                failures.append((target, row["orthography"]))
    assert failures == [], failures

def test_every_word_gets_exactly_one_primary_stress():
    for target in TARGETS:
        rf = load_target(target, TABLE)
        for row in read_test_words():
            for word in run_entry(entry_of(row), "DESC", IRISH, rf, TABLE).words:
                assert word.stress is not None

def test_traces_are_never_empty():
    ...
```

- [ ] **Step 2: Run — the snapshot test fails (no snapshot file).**
- [ ] **Step 3: Generate the snapshot**
  `uv run strands gallery sources/irish/test-words.tsv --out tests/snapshots/gallery.md`
  and **read the diff** — this is the review artefact for the whole project. Any output that looks
  wrong is a rule-file bug, fixed in Task 23–26's file, not by editing the snapshot.
- [ ] **Step 4: Run the full suite — all pass.**
- [ ] **Step 5: Commit**

```bash
git add phonotactics/tests
git commit -m "test(strands): gallery snapshot and cross-target property checks"
```

**Acceptance:** milestone 7 complete. `uv run pytest` green from a clean checkout;
`uv run strands run sources/irish/test-words.tsv --strand all --construction all` succeeds.

---

## Self-review notes

- **Spec coverage.** §1 → Tasks 0, 27. §2 → Tasks 1–4. §3 → Task 5 (+ the EBNF above).
  §4 stages 1–7 → Tasks 17–19 (1), 8–9 (2), 10 (3), 11 (4), 12–16 (5), 21 (6), 21 (7).
  §5 → Task 20. §6 → Task 27. §7 → Tasks 23–26. §8 layers 1–5 → Tasks 5, 10–19, 22, 28, 28.
  §9 decision register → each row is named in the Task 23–26 tables. §10 milestones 1–7 → all
  tasks. §11 open items → I-25, I-26 keep them open, unchanged.
- **Known deviation from the spec, flagged for the owner:** the spec's §8 layer-3 regression
  ("run the attested source forms through stages 2–7") is unbuildable for Welsh, Georgian and
  Cairene because those `attested.tsv` files carry no `source_ipa`. I-25 substitutes a legality
  conformance mode. This is the one place the plan does not do what the spec says.
- **Second known deviation:** "Awbery's tree" (spec §7, Welsh `[post-stress]`) is not in the
  digest; I-26 substitutes the §4.3 seven-row environment table.

---

## Shared test helpers

Create `phonotactics/tests/helpers.py` as part of **Task 5** (the first task with more than one
consumer) and import it everywhere. It holds exactly these, and nothing else:

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

def irish():                       # cached; available from Task 17 on
    return parse_rules_file(ROOT / "rules" / "irish.rules", TABLE)

def read_test_words() -> list[dict[str, str]]:
    with (ROOT / "sources" / "irish" / "test-words.tsv").open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))

def entry_of(row: dict[str, str]):        # available from Task 20 on
    from strands.inputs import Entry, infer
    return infer(Entry(orthography=row["orthography"], ipa=row["ipa"],
                       dialect=row.get("dialect", "C"), gloss=row.get("gloss", "")))

def rules_exist(target: str) -> bool:
    return (ROOT / "rules" / f"{target}.rules").exists()

def read_allow_file() -> set[tuple[str, str]]:
    path = ROOT / "tests" / "allow-unrepaired.txt"
    if not path.exists():
        return set()
    out = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip() and not line.startswith("#"):
            target, ortho, *_ = line.split("\t")
            out.add((target, ortho))
    return out
```

`IRISH` in the task test snippets means `irish()`; `FIX` means
`FIXTURES / "input-sample.tsv"`.

## Rule about elided test bodies

Some test bodies in Tasks 14, 15 and 23–26 are written as a comment naming the digest fact plus
`...`. That is **not** permission to skip them: the comment names the digest section and the
worked example, and the implementer's first action in that task is to open that section and write
the assertion from the source's own transcription. **A test committed with a `...` body is a
failed task** and will be rejected in review. Where the digest genuinely does not state an
expected output, the test becomes an `xfail` carrying the digest line number in its reason string
— never a deleted test.
