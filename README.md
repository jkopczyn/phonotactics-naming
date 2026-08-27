# strands

Takes Irish (Gaeilge) names and words, spelled normally, and produces the form each of five
fictional cultures would make of them: **Southern Welsh, Cairene Arabic, Standard Georgian,
Belgian Dutch** (each applying its real phonology to the Irish word) and **Old Irish** (attested
forms where they exist, a rule-based reconstruction otherwise). Output is a readable respelling,
IPA, and a rule-by-rule trace with citations. Deterministic; Python ≥ 3.12 and
[`uv`](https://docs.astral.sh/uv/) only. Run everything from this directory.

## Usual usage

You have an Irish word — say *indeagó* — and want its adaptations.

**1. Put it in a TSV.** One column is enough:

```
orthography
indeagó
```

**2. Let the tool fill in what it needs, and check its guesses:**

```sh
uv run strands lint names.tsv
```
```
indeagó	ipa = ˈɪnʲdʲəɡoː	ipa:constructed
indeagó	gender = m	gender:default-m
indeagó	declension = d4	declension:inferred-d4
…
```

The IPA is constructed from the spelling. It is right about three times in four on ordinary
words; compounds are the weak spot (write them hyphenated, *Ard-ghal*, or give the IPA yourself).
Fix anything wrong by adding the column to the file; then write the rest back:

```sh
uv run strands lint names.tsv --accept
```

**3. Adapt:**

```sh
uv run strands run names.tsv --construction DESC        # citation form, all five strands
uv run strands run names.tsv                            # every construction, all strands
uv run strands gallery names.tsv --out names.md         # the same as a Markdown table
```
```
indeagó  welsh       injygo    ɪn.ˈdʒə.ɡɔ
indeagó  arabic-egy  indagoo   ʔin.da.ˈɡoː
indeagó  georgian    injiago   indʒiɑɡɔ
indeagó  dutch       indjego   ˈɪn.djə.ɣoː
indeagó  old-irish   indecó    inʲdʲəɡoː     RETRO
```

**4. To see why**, give `explain` the IPA from the file (it does not take spelling as its
argument) plus the spelling, which some rules read:

```sh
uv run strands explain "ˈɪnʲdʲəɡoː" --strand welsh --orthography indeagó
```

## Commands

```
strands run INPUT.tsv [--strand X|all] [--construction NAME|all] [--out FILE]
strands gallery INPUT.tsv [--out FILE]
strands lint INPUT.tsv [--accept]
strands explain IPA --strand X [--construction NAME] [--orthography TEXT]
strands check RULES.rules … | LEXICON.tsv
```

Defaults: `--strand all`; `--construction all` for `run`, `DESC` for `explain`; output to stdout
without `--out`. Exit `0` ok, `1` runtime failure (printed on stderr), `2` usage error.

Strands: `welsh` `arabic-egy` `georgian` `dutch` `old-irish`.

## Input

TSV, header from: `orthography ipa dialect gloss category gender declension gen_ipa pl_ipa note`.
Only `orthography` is required; anything else missing is inferred and tagged. IPA may be wrapped
in `/…/`. Irish IPA conventions are those of `sources/irish/test-words.tsv` (144 worked rows):
ʲ/ˠ on consonants, plain *k ɡ x ɣ ŋ* broad and *c ɟ ç j ɲ* slender, `ː` length; `dˠ tˠ rˠ` and
`ɪə` are accepted as variants. Multi-word inputs are adapted word by word. `dialect` is
Connacht (`C`) unless set; `declension` is one of `m1 ach f2 m3 d4`.

## Constructions

| tag | shape |
|---|---|
| `DESC` | citation form — the usual one |
| `VOC` · `GEN` | vocative (*a Sheáin*) · genitive |
| `PATRO_O` · `PATRO_NI` | *Ó X* · *Ní X* (not in Old Irish) |
| `ADJ` · `OF` · `COMPOUND` | need a second word; skipped for single-word rows |
| `DESC+ADJ` · `DESC+NOUN` | plus the target's own epithet affix |
| `MAEL` `GILLA` `CU` `FER` `COLOUR` `MAC` `UA` `INGEN` | Old Irish only: *Máel Coluim, Gilla Pátraic, Cú Chulainn, mac X, aue X, ingen X* |

## Output

Columns: `orthography construction strand respelling ipa flags fallbacks assumptions`.

- **respelling** — English-reader spelling in the target's convention (Welsh uses native spelling:
  single *f* = /v/, *w* = /u/).
- **fallbacks** — how many segments had no rule and were approximated; `0` means every step was
  a cited rule.
- **flags** — `UNREPAIRED` (rules could not make the word legal; report it), `UNATTESTED_CLUSTER`
  (Georgian/Dutch kept a cluster the language does not attest — intended), and for Old Irish
  `ATTESTED` / `ATTESTED:MIr` (looked up) vs `RETRO` / `RETRO:loan` / `RETRO:late` (reconstructed).
- **assumptions** — every inferred field, incl. `ipa:constructed`.

## Changing a strand

All language behaviour is data in `rules/` (`<strand>.rules`, `irish.rules` for the source side,
`features.tsv`, and for Old Irish `old-irish-lexicon.tsv`). Each rule line carries `%attested` or
`%design` and a citation; `explain` prints them. After editing:

```sh
uv run strands check rules/georgian.rules
uv run pytest -q
uv run strands gallery sources/irish/test-words.tsv --out tests/snapshots/gallery.md   # if the snapshot test fails: regenerate, then read the diff before committing
```

## Layout

```
src/strands/   engine          rules/      rule files, features, Old Irish lexicon
sources/       digests + citations per language   tests/   pytest, snapshots/, ratchets/
docs/specs/    design specs (authoritative)       notes/   project goals, reports, build log
```
