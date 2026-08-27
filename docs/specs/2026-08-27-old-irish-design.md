# Strand 5: Old Irish — design spec

Status: approved in design discussion 2026-08-27. Extends the engine spec
(`2026-08-25-engine-design.md`, incl. §12); everything not stated here follows that spec.

## 1. Purpose

The fifth strand is a liturgical/classical register — culturally like Classical Arabic: a
learned, monastic class's language, recognisable and mostly intelligible to the other four,
nobody's birth language. It should read as *older* than the vernacular strands. It is
produced from the same modern-Irish input rows as the others, by (c) **lookup where an
attested Old Irish form exists, a rule-based retro-filter otherwise**, with the output
marked which it was. Period: classical Old Irish (8th–9th c., the Thurneysen/Pokorny norm as
digested in `sources/irish/digest.md §10`, from Pokorny 1914 and Strachan 1909).

Non-goals: Middle Irish; a general Old→Modern derivation (the sources do not give one);
manuscript-diplomatic transcription; verse/prose composition.

## 2. Architecture

A fifth target in the existing engine: `rules/old-irish.rules` plus a lookup pre-pass fed by
`rules/old-irish-lexicon.tsv`. Strand id `old-irish`. Same CLI, gallery, trace, tests.

Pipeline for a row (per word, after the Irish pre-pass template has been built as for the
other strands, so mutations/inflections are already applied on the modern side):

1. **Lookup** (new stage, before substitute): match the row's **orthography** (citation form)
   against the lexicon. Hit → the attested Old Irish nominative (and genitive, stem class,
   gender) replace the modern word for the requested construction; flag `ATTESTED`.
   `none` row (documented loan with no Old Irish ancestor, e.g. *Seán*) → filter, flag
   `RETRO:loan`. Miss → filter, flag `RETRO`.
2. **Retro-filter**: stages 2–7 of the engine with `old-irish.rules`. Uniquely, the
   `[substitute]` stage may reference the modern **orthography** via a per-word context
   (see §4), because spelling disambiguates what sound alone cannot.
3. **Grammar** (`[mutations]`, `[inflect]`, `[templates]` in `old-irish.rules`): Old Irish
   morphology applied to the Old Irish stem, for the shared constructions and the new
   formation templates (§5).
4. **Respell** = Old Irish editorial orthography; **IPA** = reconstructed pronunciation
   derived from the written form (§6).

Multi-word constructions are one word per template slot, as elsewhere.

## 3. Lexicon (`rules/old-irish-lexicon.tsv`)

Columns: `orthography` (modern citation form, the match key) · `oi_nom` · `oi_gen` ·
`stem` (o | ā | i | u | n | dental | irregular) · `gender` (m | f | n) · `status`
(`attested` | `none`) · `source` (Wiktionary URL / Wikipedia article / digest §10.n /
strachan1909 p.N) · `note`. Every `attested` row cites a page that shows the Old Irish form;
every `none` row cites the etymology that makes it a loan. Uncited rows are rejected by
`strands check`. Target 150–300 rows, built from: `sources/irish/digest.md §10` (≈40
attested names), Wiktionary (Old Irish lemmas; "Irish terms inherited from Old Irish";
"Irish given names" with etymologies), Wikipedia name articles, Strachan's paradigm words.
The 144 test words are the first harvest targets. Matching is exact on orthography after NFC
and case-folding; no fuzzy matching.

## 4. Retro-filter rules (`old-irish.rules`)

- `[inventory]`: Old Irish consonants incl. the lenited series /β ð ɣ μ θ x/, /s f h/ as
  lenition products only, no phonemic /h/, vowels /a e i o u/ ± length, diphthongs /aí oí uí
  éu íu áu ía úa/ as nuclei.
- `[substitute]` — spelling-driven reversals (the rule may test the modern orthography of the
  current word; a new environment atom `@orth("bh")` = "the modern spelling of this segment's
  source is …", implemented as a per-segment orthographic tag set by a small aligner between
  the modern orthography and IPA in the Irish pre-pass; where alignment fails the tag is
  absent and only sound-based rules apply):
  modern *bh/mh* → lenited *b/m* (/β μ/); *dh/gh* → lenited *d/g* (/ð ɣ/); *th/sh* → *th/ṡ*
  (/θ/ / /h/); *ch* → *ch* (/x/); *ph* → *ph* (/f/); modern *ao* → *áe* (default) / *óe*
  (lexicon-attested only); *ia* → *ía*; *ua* → *úa*; *ae/aoi* → *aí*; modern eclipsis → Old
  Irish nasalization written *mb nd ng* (the pre-pass's ECL output is reversed into
  stop+nasal). All tagged `%design` unless a lexicon pair instantiates the change (then the
  citation is added and the tag is `%attested`).
- `[substitute]` — sound-driven: modern /ɪ ʊ/ → *i u*; modern schwa in an epenthetic
  position (between sonorant and consonant, digest §2.4) → deleted (*gorm* → *gorm*); other
  schwa → *a/e* by the modern spelling; long vowels kept; modern /ə/ final → *e* (ā-stems) or
  *a* by stem class.
- `[syllable]`: template `any`, `sonority = off`; Old Irish tolerates the modern cluster set
  (digest §10). `[repair]`: none beyond degemination; `cluster-fallback = keep`.
- `[stress]`: `initial`; unstressed vowels are not reduced (unlike modern Irish).
- What is deliberately *not* reversed: broad/slender distribution; consonant clusters;
  vowel length (Old Irish long ≈ modern long, digest §10.1).

## 5. Grammar

- `[mutations]`: lenition (*c t p* → *ch th ph*; *b d g m* → lenited but unwritten; *s f* →
  *ṡ ḟ*), nasalization (voiceless stops voiced: *c t* → *g d* written; voiced stops prefixed
  *m/n*: *mb nd ng*; vowels prefixed *n-*), no *h*-prefix, no *t*-prefix. Triggers as in
  Strachan/Thurneysen for the constructions used.
- `[inflect]`: nominative/genitive/vocative/dative for o-stems, ā-stems, i-stems, u-stems,
  n-stems, dental stems, plus the o-stem adjective (*-ach*). Stem class from the lexicon,
  else inferred from the modern declension (m1 → o; f2 → ā; m3 → i or u by ending; *-ach*
  → o-stem adj.; d4 → indeclinable) and tagged in `assumptions`.
- `[templates]`: the shared constructions with Old Irish morphology — `DESC`, `VOC` (*a* +
  lenition + vocative form), `GEN`, `ADJ` (agreement + lenition after feminine), `OF` (article
  *in/ind/inna* + genitive with its mutation), `COMPOUND` — and the **formation templates
  unique to this strand**: `MAEL` (*Máel* + GEN, lenited: *Máel Choluim*), `GILLA` (*Gilla* +
  GEN), `CU` (*Cú* + GEN lenited), `FER` (*Fer* + GEN), `COLOUR` (*Dub-/Find-/Flann-* +
  nominative, compound lenition), `MAC`/`UA`/`INGEN` (*mac/ua/ingen* + GEN; *ingen* lenites).
  These replace `PATRO_O`/`PATRO_NI`, which do not apply to this strand.

## 6. Output

- **Written form** in editorial Old Irish orthography: lenited *b d g m* unmarked; *ch th
  ph*; *ṡ ḟ* with punctum (`punctum = off` → plain *s f*); nasalization *mb nd ng*; acute
  for length; diphthongs as spelled; no *h*-prefix.
- **IPA**: reconstructed from the written form by the digest §10 orthography-to-sound table
  (initial stress, lenited stops as fricatives, /μ/ nasalized β, quality from adjacent
  vowels), emitted as the strand's `ipa`.
- Flags: `ATTESTED` / `RETRO` / `RETRO:loan` on every output; `assumptions` carries the stem
  class inference.

## 7. Tests

- Lexicon: schema, citation-present, no duplicate keys; a cross-family sample verification
  of ≥30 rows against the cited pages before the file is admitted.
- **Filter regression**: run each `attested` lexicon headword's modern form through the
  retro-filter and compare the written form with `oi_nom`; report and ratchet the match
  rate (exact-match and Levenshtein ≤1); list failures by reversal class.
- Unit: each mutation/inflection against Strachan's paradigms (digest §10); each reversal
  rule against a lexicon pair; formation templates against *Máel Coluim, Gilla Pátraic,
  Cú Chulainn, Fer Diad, Dub-dá-leithe* (from the lexicon).
- Gallery: fifth column for the 144 test words with `ATTESTED`/`RETRO` marks, plus a
  formation-template block; property checks extended; snapshot committed.

## 8. Decision register (this strand)

| # | Decision | Default | Alternative | Where |
|---|---|---|---|---|
| O1 | Modern *ao* | *áe* | *óe* | `old-irish.rules [substitute]` |
| O2 | Lenited *s f* | *ṡ ḟ* (punctum) | plain *s f* | `[respell] punctum` |
| O3 | Stem class when not in lexicon | from modern declension | always o/ā by gender | `[inflect]` inference |
| O4 | Loans with no OI ancestor | filter + `RETRO:loan` | omit | lookup stage |
| O5 | Epenthetic schwa | deleted | kept | `[substitute]` |
| O6 | Formation templates | MAEL GILLA CU FER COLOUR MAC UA INGEN | subset | `[templates]` |

## 9. Milestones

1. Lexicon harvest + verification (sourced-data task; two agents).
2. Lookup stage + `ATTESTED/RETRO` flags + orthography aligner (`@orth` atom).
3. `old-irish.rules`: inventory, substitute, syllable, stress, respell + IPA reconstruction.
4. Grammar: mutations, inflection by stem class, templates incl. formation templates.
5. Filter regression + gallery column + property checks; CLI exposure (`--strand old-irish`).
