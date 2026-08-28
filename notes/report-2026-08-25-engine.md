# Report: the strands engine (spec → plan → build), 2026-08-25

## Outcome

The engine exists and runs end-to-end. the repository (then `phonotactics/`, now the root) holds a Python package `strands`
(no runtime dependencies), five rule files (`rules/irish.rules` + one per target), a feature
table, and a test suite of 862 tests (2 expected-fail). Four cross-family reviews were
applied during the build; my own verification pass afterwards found three defects (below),
now fixed.

Try it:
```
cd phonotactics
uv run strands gallery sources/irish/test-words.csv --out /tmp/gallery.md   # 144 words × constructions × 4 strands
uv run strands run my.csv --strand all --construction DESC                   # TSV in, TSV out
uv run strands explain ˈl̪ˠɑsˠəɾʲxosˠ --strand georgian                     # derivation with rule tags + citations
uv run strands lint my.csv [--accept]                                        # fill missing columns from inferences
```
`DESC` is the citation-form construction (the spec's `NAME`); `explain` takes IPA.

## What the four strands do to six words

| Irish | Welsh | Cairene | Georgian | Dutch |
|---|---|---|---|---|
| Ciara /ˈkɪəɾˠə/ | cira | kiʼara | kviara | kiere |
| Matánach | matanach | maṭaanakh | matanax | mattanech |
| Lasairchos | llasyrchos | laṣarkhuṣ | lasarxos | lasserchos |
| Seán | siân | shaan | shian | sjaan |
| Gráinne | grana | giraana | grania | granje |
| Niamh | niw | neew | niav | njief |

Every cell is traceable: `explain` prints each rule that fired with its `%attested` /
`%design` / `%fallback` tag and digest citation.

## Decisions made during the build that are yours to revisit

1. **Welsh keeps Irish vowel length before a final n/l/r as Welsh lexical length** (written
   with the circumflex): *Seán* → *Siân*, *mór* → *môr*, *bán* → *bân*. Southern Welsh length in
   that position is lexically determined (digest §4.3), so the agent read the Irish length as
   the lexical choice. Without it every such vowel would be short (*Sian*). 26 rule lines in
   two blocks, easy to drop. The most visible Welsh choice in the output. Related open point:
   the Welsh syllable template and part of the onset evidence are North-marked in the digest
   while the target is Southern — the "which Welsh" question from the source phase is still
   open.
2. **Welsh onsets**: the plan's evidence tiers (built from what open sources *state*) excluded
   stop+liquid and produced *Bríd* → *Prid*; I ruled during the build that stop+liquid onsets
   are attested (Wikipedia, Breit) and that the clusters Irish mutations create are exactly the
   onsets Welsh's own mutations create (*fy mlodyn, ei chrys, ei wlad*), so *mbláth* → *ml-*,
   *chrom* → *chr-*; Irish *sn-/sm-* instead take the prothetic *y-* (*sneachta* → *ysnachta*).
   Sonority checking is off for Welsh as a consequence (its soft-mutation onsets *wl- wr-*
   have falling sonority). Recorded as Known Deviation 9.
3. **Dutch regression bars restated** (my call, low stakes): the plan's Mode C bar forgot to
   subtract the end-to-end rows, and Mode E's 25% is unreachable because the attested English
   rows include particles and Netherlandic vowels. Now Mode C ≥ 27/35, Mode E ≥ 4/26, both
   ratchet-held (can only rise). The eight Mode C misses are seven French final-stress loans
   (excluded by your Dutch-weight stress decision) and *roos*, which your "voice the
   fricative" decision predicts as [roːz].
4. **Georgian cluster legality is now pairwise** (experiment 2026-08-25, `28010a3`, awaiting
   your confirmation): Butskhrikidze's finding that underlying clusters are biconsonantal,
   applied as "every adjacent pair must be attested". Six words stopped hitting the cluster
   fallback (*splanc* → *sp'lank'*, not *ts'k'lank'*). You then kept Cʷ on all broad
   non-labials (*drvim, sp'rvi*) and chose `cluster-fallback = keep`: unattested clusters are
   left intact and flagged (*mná* → *mra*, *dorn* → *dorn*), with one narrow undo of the Cʷ
   *v* where it alone made a cluster illegal (*naomh* → *niv*). Georgian fallbacks 108 → 14.
5. **Georgian /p t k/: aspirate by default, ejective only after a consonant** — your decision
   4, implemented as seven explicit segment lines (a feature bundle can't reach the ejective
   rows). It is tagged `%design` and runs *contra* the digest's recommendation of unconditional
   ejectives. This is the single biggest lever on whether strand-4 output sits beside
   *Kas'queil*; flipping it is one block. Also: Georgian has no syllable template and no
   nucleus list, which is why its outputs show bare vowel sequences (*kviara*, *grania*) and
   no stress marks — both as designed.
6. **Cairene emphatics**: narrowed 2026-08-26 to Hafez's attested environment — broad
   coronals become emphatic only before a back vowel (*maṭaanakh, ṣuul* keep it; *sheemas,
   sirsha, badrag* lose it), which took emphatics from a quarter of all words to the attested
   pattern. Still respelled with a dot-under; one rule line to strip if unwanted.
7. **Irish transcription convention is load-bearing**: plain `k ɡ x ɣ ŋ` are broad, `c ɟ ç j
   ɲ` slender, and the normalizer must not infer dorsal quality from the vowel (defect 1
   below). So your *Ciara* /k/ is taken literally as broad → Georgian *kv-*; if you meant
   slender, write /c/. The digest's flag on that transcription stands.

## Defects found in my verification (fixed after the workflow)

- Normalizer re-marked plain dorsals from the following vowel, so the Cʷ rule never fired on
  *caoin, gaoth, Ciara* (Georgian *kin* instead of *kvin*).
- A `h → ç` allophone rule fired outside its slender context: lenited *theach, shúil* came out
  *chach, chŵl* in Welsh and Dutch.
- Dutch weight-stress could stress a schwa syllable (*an bhean* → *ˈən.vjɑn*).

All three fixed. One genuine cost surfaced: the `h → ç` rule was the only thing producing the Munster vocative
*a Sheáin* [ə çaːnʲ]; removing it gives /əhaːnʲ/ everywhere. A correct fix needs per-rule
dialect gating, which the DSL doesn't have — a small feature if you want it. Also: with plain
*k* now broad, *stríoc*'s inferred declension flipped f2 → m1 (a dictionary question).

## Known gaps (not defects)

- Welsh: four attested rows carry consonant length the feature table can't tokenize. Awbery
  1984 is now fully transcribed (`sources/welsh/awbery1984-digest.md`): she gives constraint
  sets rather than cluster lists (homorganic nasal+stop, voicing agreement, CCC = s/nasal +
  stop + liquid; South bans all final obstruent+sonorant), which the rule file now cites.
- Dutch end-to-end regression is thin (26 usable rows); Georgian/Arabic/Welsh have none
  (no donor IPA in the sources) — their "Mode C" checks only that attested target forms are
  accepted by the rule file.
- Old Irish strand: not started (lookup task, separate spec).
- The gallery is the acceptance test. Nobody has read it yet except the agents.

## What I'd do next

Read the gallery for an hour and note which outputs feel wrong per strand; each complaint
will map to one decision-register row or one rule line. Then the Awbery pass for Welsh, and
the Old Irish spec.

Reviews and logs: `docs/plans/review-{core,stress-irish,targets,final}.md`,
`notes/engine-build-log.md`.

## Addendum 2026-08-27: G2P and the Old Irish strand

- **G2P** (`src/strands/g2p.py`): rows without IPA get a constructed transcription (73% exact
  against the attested test words; compounds are the weak class — hyphenate or supply IPA).
  `lint` shows it, `--accept` writes it, outputs carry `ipa:constructed`.
- **Old Irish strand** (`--strand old-irish`): lookup of attested forms (lexicon of 302 rows,
  270 attested + 10 Middle Irish tier, 12% sample-verified twice) else a spelling-aware
  retro-filter; grammar runs on the written form; formation templates MAEL GILLA CU FER
  COLOUR MAC UA INGEN. On the 144 test words: 63 attested, 60 retro, 21 loan/late. Filter
  regression 0.31 exact / 0.69 within one edit over 58 headwords — the filter is a designed
  reversal, as the spec says; lookup carries the names that matter.
- Decisions to revisit: `ua` renders as the attested Old Irish *aue* (later *úa*); `mac` as
  *macc*; *stríoc* → *strícc* (post-vocalic doubling incl. after long vowels); MAEL/GILLA
  unlenited per attestation, CU/INGEN lenite.
