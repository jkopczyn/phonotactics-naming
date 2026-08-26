# strands

A deterministic command-line tool that takes Irish (Gaeilge) names, descriptors and epithets in
IPA and produces, for each of four "strands", the form a speaker of that strand's target language
would make of them — **Southern Welsh, Cairene Arabic, Standard Georgian, Belgian Dutch** — as IPA
plus an English-reader respelling, with a full derivation trace.

Irish is the lexifier (it supplies the words); the target language supplies all the rules. Every
rule lives in a plain-text rule file and cites the source digest section or design decision it
implements, so any output can be traced back to a citation.

Same input, same output, every time: no randomness, no model calls, no runtime dependencies
beyond the Python standard library.

## Requirements

Python ≥ 3.12 and [`uv`](https://docs.astral.sh/uv/). Nothing else. Run everything from this
`phonotactics/` directory:

```sh
uv run strands --version
```

`uv` builds the venv on first use. There is no separate install step.

## Quick start

Adapt one word into one strand, with its derivation:

```sh
uv run strands explain "d̪ˠɾˠiːmʲ" --strand georgian
```

```
d̪ˠɾˠiːmʲ  [georgian, DESC]
respelling: drvim
ipa:        drvim
fallbacks:  0
assumptions: declension:default-m1 gen_ipa:inferred-m1

irish       templates:DESC         -           -> d̪ˠɾˠiːmʲ   (construction DESC, word 1 of 1)
irish       stress:irish-initial   %attested  d̪ˠɾˠiːmʲ -> d̪ˠɾˠiːmʲ   (Connacht initial stress (digest §4.1), dialect=C)
substitute  substitute:45          %attested  d̪ˠɾˠiːmʲ -> d̪ˠɾˠimʲ   # digest §8.3 [gabunia2021 p.13; shosted2006 p.262]
substitute  substitute:65          %design    d̪ˠɾˠimʲ -> d̪ˠɾˠvimʲ   # design: goals decision 5 (2026-08-25); digest §8.1 lines 1440-1442 open
…                                                                    (six more substitute/syllabify/stress/respell steps)
respell     respell:354            %attested  drvim -> drvim   # digest §5.1 [ungegn-georgian p.1] რ
```

The `WORD` argument to `explain` is **IPA, not orthography** — broad/slender diacritics and all.

Run a whole input file into every strand and every construction:

```sh
uv run strands run sources/irish/test-words.tsv --out /tmp/out.tsv
```

Render the human-readable comparison table (the project's review artefact):

```sh
uv run strands gallery sources/irish/test-words.tsv --out /tmp/gallery.md
```

## Commands

| command | what it does |
|---|---|
| `strands run INPUT.tsv [--strand X\|all] [--construction NAME\|all] [--out FILE]` | batch adaptation → TSV |
| `strands explain WORD --strand X [--construction NAME]` | one IPA word → result + full trace |
| `strands gallery INPUT.tsv [--out FILE]` | words × constructions × strands → Markdown |
| `strands lint INPUT.tsv [--accept]` | list the fields the tool had to guess; `--accept` writes them back |
| `strands check [--features PATH] RULES.rules …` | static checks on rule files |

Without `--out`, output goes to stdout. `--strand` defaults to `all`; `--construction` defaults to
`all` for `run` and `DESC` for `explain`.

**Exit codes.** `0` ok; `1` a runtime failure (unreadable input, a rule-file parse error, an input
IPA containing a segment that is not in `rules/features.tsv`, an unwritable `--out`, or `check`
findings); `2` a usage error. Failures print a diagnostic on stderr, never a traceback.

### Strands

`welsh`, `arabic-egy`, `georgian`, `dutch`. (The fiction has a fifth, Old Irish, which is a lookup
task and is out of scope for this engine.)

### Constructions

What Irish grammatical shape to build before adapting it:

| tag | shape |
|---|---|
| `DESC` | the bare noun — the usual starting point |
| `VOC` | vocative: *a Sheáin* |
| `GEN` | genitive, dispatched on declension |
| `PATRO_O` / `PATRO_NI` | *Ó X* / *Ní X* patronymics |
| `ADJ` | name + adjective (*Máire Bhán*) |
| `OF` | name + article + genitive noun |
| `COMPOUND` | two-element compound (*Lasairchos*) |
| `DESC+ADJ` / `DESC+NOUN` | `DESC` plus the target's own epithet affix |

`ADJ`, `OF` and `COMPOUND` need more than one word, so a single-entry input cannot fill them: those
rows are written with empty output columns and a `skipped:missing-slot-…` note rather than failing.

## Input format

A TSV whose header names some of:

```
orthography  ipa  dialect  gloss  category  gender  gen_ipa  pl_ipa  note
```

Only `orthography` is required. Unknown columns are ignored; absent ones read as empty. A row with
no `ipa` is kept but skipped, tagged `skipped:no-ipa`.

Anything missing is **inferred** — dialect (default Connacht), gender (known-name list, then
orthographic endings, then masculine), declension, and the genitive IPA — and every guess is
recorded as a `field:reason` tag in the row's `assumptions`. Review the guesses before trusting a
run:

```sh
uv run strands lint mynames.tsv          # list them
uv run strands lint mynames.tsv --accept # write dialect/gender/gen_ipa back into the file
```

`sources/irish/test-words.tsv` is the project's own 144-word input and doubles as a worked example.

## Output

`strands run` writes one row per (entry × construction × strand), in input / construction / strand
order, so the file is byte-identical across runs:

```
orthography  construction  strand  respelling  ipa  flags  fallbacks  assumptions
```

- **respelling** — an English-reader romanization, per target's own scheme. No stress or length marks.
- **ipa** — the adapted form. Stress is marked unless the target suppresses it (Georgian does).
- **fallbacks** — how many segments or clusters had to be approximated to fit the target. It is a
  cost signal, not an error: `0` means everything mapped exactly.
- **flags** — `UNREPAIRED` (the repair loop could not make the word legal — a rule-file bug worth
  investigating) and `UNATTESTED_CLUSTER:<cluster>` (the target deliberately kept a cluster its
  own phonotactics do not license; Georgian does this on purpose).
- **assumptions** — the inference tags above, plus any `skipped:…` note.

## Rule files

Everything language-specific is data, in `rules/`:

```
features.tsv     segment → feature vectors, for every language
irish.rules      the source-side pre-pass: templates, mutations, normalization
welsh.rules  arabic-egy.rules  georgian.rules  dutch.rules
```

A target file declares its inventory, `[substitute]` rules, `[syllable]` phonotactics, `[repair]`
processes, stress, epithets and `[respell]`. Each rule line carries a `%attested` or `%design` tag
and a `#` comment citing the digest section or decision behind it — those citations are what
`explain` prints beside each step.

To change how a strand sounds, edit its rule file, then:

```sh
uv run strands check rules/georgian.rules   # static checks
uv run pytest -q                            # the suite, including the gallery snapshot
```

The gallery snapshot is the review artefact for the whole project. When a rule change moves it,
regenerate and **review the diff in the commit** — never edit the snapshot by hand:

```sh
uv run strands gallery sources/irish/test-words.tsv --out tests/snapshots/gallery.md
```

## Layout

```
src/strands/     the engine (pipeline stages: substitute → syllabify → repair → stress → respell)
rules/           features.tsv and the five rule files
sources/         per-language digests, citations and attested loanword data
tests/           pytest, plus snapshots/ and ratchets/
docs/specs/      the design spec — the source of truth for engine behaviour
notes/           project goals and working notes
```

`docs/specs/2026-08-25-engine-design.md` is the authority on what the engine is meant to do;
`sources/<lang>/digest.md` is the authority on the linguistic facts, with citations.
