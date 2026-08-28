# Reverse tool — design spec

Status: approved in design discussion 2026-08-27 (globs in v1 unless they prove costly; no
name corpus). Extends the engine spec (`2026-08-25-engine-design.md`); everything not stated
here follows that spec and the code it describes.

## 1. Purpose

Given a strand and a target respelling — possibly a glob such as `Ar*v*` — say what shapes of
Irish word the forward engine would turn into it. The deliverable is the **constraint set**
(which Irish spellings produce each target letter, what is unconstrained, what is excluded),
then an Irish spelling pattern, then a few forward-verified concrete examples as illustration.
It is a guessing aid: approximate, over-generating, allowed to miss. It never modifies rule
files or the forward pipeline, and every claim it makes about a concrete word is checked by
running that word forward through the real engine.

Non-goals: an exact inverse; an Irish name corpus; attested-vs-coined judgements; inverting
constructions other than `DESC`; inverting the Old Irish retro grammar (lexicon lookup only).

## 2. CLI

```
strands reverse PATTERN --strand X [--examples N] [--ipa]
```

- `PATTERN`: the strand's respelling, case-insensitive, with optional glob syntax: `*` (any
  run, including empty), `?` (one letter), `[aeiou]` (one of). Letters outside the strand's
  respelling alphabet are reported (`no Irish source for 'q''`) and treated as `?`.
- `--strand X`: one of `TARGETS`; `all` not accepted (the constraint sets are per strand).
- `--examples N`: cap on verified examples printed (default 8; `0` skips verification).
- `--ipa`: `PATTERN` is target IPA in the strand's convention (segments as the forward engine
  prints them, stress and syllable marks ignored); the un-respell step is skipped.
- Multi-word patterns (spaces) are handled word by word, each word reported separately.
- Exit codes as the other commands. Usage line added to `_USAGE`; handler `cmd_reverse`.

`old-irish`: the pattern is matched (fnmatch, casefolded, NFC) against the lexicon's Old Irish
citation forms; output is the matching rows' modern citation forms with their flags. No
constraint set (§3 does not apply), and a note says so.

## 3. Method (four foreign strands)

Think of the forward engine as spelling → g2p → Irish IPA → `[substitute]`+fallback →
syllabify/`[repair]`/stress/`[post-stress]` → `[respell]`. Reverse walks it backwards with
**over-generation**: at every step the candidate set only grows, and the forward engine is
the oracle that prunes.

### 3.1 Un-respell

Invert `[respell]` of the strand: build the map *output chunk → list of (IPA segment sequence,
rule_id, context text)* from every rule whose replacement is `QuotedText`; segments no rule
mentions map to themselves. Parse the pattern greedily longest-chunk-first into a sequence of
**slots**, each slot = a set of alternative target-IPA segment sequences, or `ANY` (from `*`),
`ONE` (from `?` / a bracket class, with the class's letters un-respelled where they are
chunks). Ambiguity (Welsh `i` ← ɪ, iː, j; Georgian `y` ← i) is kept as alternatives, not
resolved.

### 3.2 Un-substitute

Invert `[substitute]` plus the inventory fallback into a **source map**: *target segment
sequence → list of Source(irish segments, rule_id, tag, context text, kind)*, `kind` in
`{rule, fallback, identity, epenthesis}`.

- Rules with segment targets and segment replacements: literal inversion.
- Class / bundle targets: expanded by running `match_item` over the Irish inventory
  (`rules/irish.rules [inventory]`), so `[SLEN] -> …` lists every slender segment.
- Feature-change replacements (`[+ejective]`): apply to each matching Irish segment through
  the same lookup the forward engine uses, record the result.
- Epenthesis (`0 -> v / …`): a Source of kind `epenthesis` with empty Irish segments and the
  context text — in the constraint set it reads "*v* may be inserted, not from any Irish
  letter, when broad non-labial C precedes a front vowel".
- Deletion (`X -> 0`): recorded as a note on the neighbouring slot ("*h* may have been dropped
  here"), never expanded (unbounded).
- Fallback: every Irish inventory segment that survives the section unchanged and is outside
  the target inventory maps to `table.nearest(...)`, kind `fallback`.
- Identity: Irish segments in the target inventory that no rule touches.

Rule ORDER is honoured only in the sense that each later rule's *output* is looked up in
earlier rules' outputs (two-step chains such as `ç -> x`, then `x -> χ`, are followed to depth
3). Contexts are **not** evaluated at inversion time; they are carried as text and as a
predicate that the verification step relies on the forward engine to enforce.

### 3.3 Un-repair / un-stress / un-post-stress

Same source-map construction over `[repair]` and `[post-stress]`, but used only to **widen**
slots: a segment that a rule in those sections could have produced gains that rule's target
as an extra alternative (Welsh `y`/ə ← any short vowel via reduction; Welsh initial `ll` ←
*l*; Welsh long vowels ← the short one via §4.3 lengthening). Insertions from these sections
(Welsh prothetic `y`, epenthetic copy vowels, Cairene breakers, Georgian *v*/*i*) make the
corresponding slot **optional**. Stress is ignored: the forward engine re-derives it.

### 3.4 Irish spelling rendering (reverse g2p)

An Irish-IPA slot is described in spelling terms by inverting `g2p._CONSONANTS` and
`_VOWELS`: each Irish segment → the graphemes that read as it, with the quality that
grapheme needs ("broad *bh/mh*", "slender *d*", "*á*", "*ao/ae*"). A pattern is rendered
left to right with caol-le-caol respected: the vowel letters chosen beside a consonant are
those that yield its quality (`c` + broad → *ca/co/cu*). Alternatives print as `(a|o)`,
optional material as `(…)?`, `ANY` as `*`. The rendering is a description, not a claim; every
concrete spelling proposed is passed through `g2p` to confirm it reads back to the intended
IPA before it is used as an example.

### 3.5 Verification

Expand the Irish-IPA pattern to concrete candidates, breadth-first, cheapest first:
alternatives ordered by source kind (`identity` < `rule attested` < `rule design` <
`fallback` < `epenthesis`), optional slots first absent then present, `ONE` filled from the
inverted class or from a fixed palette (the five short vowels *a e i o u*, then their five
long counterparts *aː eː iː oː uː*, then *r l n m s d t c g b* — 20 entries), `*` filled with
0, 1, then 2 palette segments. Hard cap 2000 candidates **run forward** per word (`log` the
cap when hit); since a candidate that cannot be spelled costs no forward run, the candidate
stream itself is consumed at most 4 × that.

Each candidate is spelled ONCE (§3.4) and run through `run_entry(... "DESC" ...)` for the
strand: the forward result depends only on the Irish IPA the spelling reads back to, and
`spell()` guarantees every spelling it returns reads back to the candidate's own segments, so
one spelling per candidate is enough. That one is asked for **silent-free** — no ⟨fh⟩, no
silent ⟨dh gh th⟩, no vowel-plus-h run — so the eight spellings of one word collapse to the
one a reader can use. A candidate with no silent-free spelling is skipped and does not count
against the cap. The run is kept when `fnmatch(respelling, PATTERN)` (or, with `--ipa`, when
the unmarked IPA matches). Kept examples are ranked by `(fallbacks, len(flags), candidate
rank)`, de-duplicated by the printed foreign shape, and the first `--examples` printed with
their respelling, IPA, flags and fallback count — the same quality signal the hand-run used.

## 4. Output

Plain text, per word:

```
Ar*v*  [georgian]
target segments: ɑ r * v *

constraints
  a   ← a, á, or unstressed vowel (any short vowel)           substitute:44,45,53
  r   ← broad or slender r                                    substitute:98,99
  *   unconstrained
  v   ← broad bh/mh, v, w (/w/)                               substitute:79 %design
      ← slender bh/mh (/vʲ/)                                  substitute:81
      ← inserted, no Irish letter: broad non-labial C before a front vowel
                                                              substitute:65 %design
  *   unconstrained

exclusions
  labial C before a front vowel does not trigger the inserted v (substitute:65 context)

Irish spelling pattern
  (a|á)r*(bh|mh|v|w)*     or     (a|á)r*C(ao|ae|aoi|ia)*

verified examples (6 of 40 tried; 0 fallbacks unless shown)
  ardmhaor   ardvar   ɑrdvɑr
  arbha      arva     ɑrvɑ
  arv        arv      ɑrv      UNATTESTED_CLUSTER:rv
  …
```

Section order and content are the spec; exact spacing is the implementer's; the rule ids above are illustrative. Rule ids are
`section:line` as in `explain`. Tags print only when `%design` or `%fallback`.

Constraint lines are grouped by `(kind, tag, description)` alone — a context does not split a
line. A line's rule ids are the union over its group, ordered by forward stage (substitute,
repair, post-stress, respell) and then by line number, with at most four printed and the rest
as `+N`. The `exclusions` block lists only epenthesis sources and `substitute`-stage sources
that carry a context; a repair, post-stress or respell context is noise for the reader and is
not printed. Descriptions and the spelling pattern are built from silent-free readings only.
A slot whose Irish alternatives cover every short vowel describes as `any short vowel` (with
` (unstressed)` when every contributing source is a reduction), every long vowel as `any long
vowel`, both as `any vowel`; any other run list longer than six items is cut at six with `…`.
The examples header reads `verified examples (N of M candidates tried; …)`, where M is the
number of candidates actually run forward.

## 5. Code

- `src/strands/reverse.py`: `invert_respell`, `source_map` (per section), `parse_pattern`,
  `Pattern`/`Slot`/`Source` dataclasses, `expand`, `verify`, `report`. Pure functions over
  `RuleFile` + `FeatureTable`; no I/O except through `pipeline`.
- `src/strands/g2p_inverse.py`: `spell(ipa_segments) -> list[str]` (candidates, g2p-checked)
  and `describe(segment) -> str` (spelling description). Reads `g2p._CONSONANTS`/`_VOWELS`;
  those become module-level, documented as shared with the inverse (no behaviour change).
- `src/strands/cli.py`: `cmd_reverse`, usage, dispatch.
- No change to `rules/`, `pipeline.py`, or any forward stage.

## 6. Tests

- Unit: inversion of a five-line synthetic `[respell]`/`[substitute]` string covers literal,
  class, bundle, epenthesis, deletion, fallback, chain.
- `g2p_inverse`: for every row of `sources/irish/test-words.tsv` with a hand IPA,
  `spell(g2p(orth))` contains `orth` (casefolded) — ratcheted in `tests/ratchets/g2p_inverse.json`.
- Round trip per strand, two rates measured by two runs because they cost very differently.
  **`admits`**: for every test-words row with a hand IPA, `reverse(forward(row).respelling)`
  — run with the `--examples 0` machinery, so nothing is verified — yields a pattern that
  admits the row's own Irish IPA. All rows; cheap, so it is not marked `slow`.
  **`examples`**: the row's spelling, or any spelling that reads to the same IPA, is among the
  verified examples at `cap=200`, over the first twelve hand-IPA rows only; marked `slow`.
  Both rates ratcheted in `tests/ratchets/reverse-<strand>.json` as `admits`, `admits_n`,
  `examples`, `examples_n` (no floor requirement; the ratchet only forbids regression).
- Session case: `reverse("Ar*v*", georgian)` lists exactly the three `v` sources
  (/w/, /vʲ/, epenthesis) and the pattern admits *ardmhaor*'s /aːɾˠd̪ˠvˠiːɾˠ/; that the word
  itself reaches the verified examples is a separate `slow` test.
- CLI: exit codes, `--ipa`, unknown letter note, old-irish lookup, multi-word.

## 7. Decisions

| # | Decision | Default | Alternative | Where |
|---|---|---|---|---|
| R1 | Input form | respelling glob | IPA (`--ipa`) | `cli` |
| R2 | Context handling in inversion | carry as text; forward engine enforces | evaluate contexts symbolically | `reverse.source_map` |
| R3 | Deletions | note only, never expanded | expand at literal-context edges | `reverse` |
| R4 | Candidate cap | 2000 / word | `--cap` flag | `reverse.expand` |
| R5 | Palette for wildcards | 5 short + 5 long vowels + 10 consonants, ≤2 segments per `*` | larger; from Irish frequency | `reverse.expand` |
| R6 | Old Irish | lexicon fnmatch only | invert retro grammar | `reverse` |
| R7 | Rendering ambiguity | alternation `(a|o)`, never a pick | pick most common | `g2p_inverse` |
