# bib.md — cross-linguistic infrastructure (`sources/infra/`)

Scope: the databases and general (non-language-specific) literature that all five per-language
digests draw on. Assembled 2026-08-24. Everything listed under "Sources" below is **open access,
no account, no payment**, and is downloaded into this directory unless a "local file" line says
otherwise. Paywalled items are in the last section.

Section numbers in the coverage notes refer to `../DIGEST-TEMPLATE.md` §0–§9.

---

## Databases

### `wold` — World Loanword Database (CLDF)

- **Citation.** Haspelmath, Martin & Tadmor, Uri (eds.). 2009. *World Loanword Database.*
  Leipzig: MPI-EVA. CLDF edition: `lexibank/wold` v4.2 (2026-07-17).
- **URL.** https://wold.clld.org · https://github.com/lexibank/wold (data:
  `https://raw.githubusercontent.com/lexibank/wold/v4.2/cldf/*.csv`)
- **Access tier.** OA (CC BY; site and CLDF data both open, no login).
- **Verification.** Confirmed. `lexibank/wold` is the live CLDF derivation; `clld/wold-data`
  also exists and is the older clld-app data repo — use `lexibank/wold`.
- **Local files.** `wold-languages.csv` (all 41 recipient languages),
  `wold-dutch-forms.csv` (1 588 Dutch forms), `wold-dutch-loanpairs.csv` (339 donor→Dutch rows),
  `wold-chapter-12-dutch-vandersijs.md`, `wold-chapter-34-qeqchi.md`,
  `wold-dutch-extract.py` (the regeneration script; documents the table shapes).

**Recipient-language coverage — the question the plan asked (verify).** WOLD has exactly 41
recipient languages (`wold-languages.csv`). Of our targets:

| Language | In WOLD? |
|---|---|
| **Dutch** | **YES** — `Dutch`, WOLD_ID 12, van der Sijs, 1 588 entries |
| Welsh | no |
| Arabic (any variety) | **no** — the nearest Afro-Asiatic entries are Iraqw, Gawwada, Hausa, Tarifiyt Berber |
| Georgian | no |
| Irish | no |
| Mayan | **YES, two** — Zinacantán Tzotzil (33) and **Q'eqchi'** (34) |

So the baseline bibliography's claim is confirmed: Dutch and Q'eqchi' yes, Welsh/Arabic/Georgian no.

**How to filter to Dutch and get source→adapted pairs.** `forms.csv` has `Language_ID == 'Dutch'`;
`Segments` is space-separated IPA, so the **adapted side is already phonemic**. `borrowings.csv`
links `Target_Form_ID` (a `forms.csv` ID) to the donor etymon. Run `wold-dutch-extract.py`.

**Caveat that matters for §7.** `Source_Form_ID` is **empty for every row in the whole database**
— the donor side exists only as the *orthographic* string `Source_word` plus `Source_languoid`.
There is no source-side IPA. Donor mix for Dutch: French 117, Latin 112, High German 42,
English 23, Spanish 10, French (Picard) 7, Celtic 5, other ≤4. Most pairs are medieval
French/Latin, so they document historical integration, not modern loan repair; the 23 English
items (1662–2000) are the modern set. Using these as a gold set requires supplying the donor
pronunciation yourself.

- **Digest coverage.** §7 (attested adaptations, Dutch only), §1/§2 indirectly (the Dutch IPA
  segmentation shows which segments and clusters the compiler treats as Dutch), §3 (repair, by
  inference from pairs). Nothing for Welsh/Arabic/Georgian/Irish.
- **Note for the Dutch agent.** van der Sijs's transcription is **Netherlandic**: `ʋ` for /w/,
  `ɛi ɑu` for the diphthongs, final devoicing written out (`l ɑ n t` *land*), and `ɣ` vs `x`
  distributed by position (`k ɑ ŋ ɣ uː r uː` *kangoeroe* vs `x r ɔ t` *grot*). This bears on the
  open Belgian-vs-Netherlandic decision in source-plan.md.

**Online per-language chapters.** Open. `https://wold.clld.org/vocabulary/12` returns 200 with no
login, and the same prose is in the CLDF release under `cldf/descriptions/vocabulary_<n>.md` (all
41 present). These are the *short* online chapters. Separately, the **full book chapter** for
Dutch is open on a repository — see `vandersijs2009` below. The Haspelmath & Tadmor 2009 volume
as a whole is not open (see the paywalled list).

### `lapsyd` — Lyon-Albuquerque Phonological Systems Database

- **Citation.** Maddieson, Ian, Sébastien Flavier, Egidio Marsico, Christophe Coupé &
  François Pellegrino. LAPSyD: Lyon-Albuquerque Phonological Systems Database. Lyon: DDL / UNM.
- **URL.** https://lapsyd.huma-num.fr/lapsyd/
- **Access tier.** OA (CC BY-NC-ND 3.0). Public layer needs no registration; a "Private" layer
  (mostly stale UPSID inheritance) needs a free account — none of our five languages needed it.
- **Verification.** Confirmed reachable and **all five languages have public entries.** Language
  pages are at `index.php?data=view&code=<n>`; the code list is at `index.php?data=iso`.
- **Local files.** For each language, the saved page `lapsyd-<lang>.html` and a structured text
  extraction `lapsyd-<lang>.txt` (inventory tables, syllable canon, stress, tone, the compiler's
  consonant/vowel notes, and LAPSyD's own source list).

| Language | code | LAPSyD variety | Canonical form | Syll. index (O/N/C) | Stress |
|---|---|---|---|---|---|
| Irish | 217 | **Donegal dialect** | (C)(C)(C)V(V)(C)(C) | 7 (3/2/2) | fixed initial, weight = V: |
| Welsh | 10008 | **Northern only** | (C)(C)(C)V(V)(C)(C) | 7 (3/2/2) | penult, no weight-sensitivity |
| Egyptian Arabic | 142 | Cairene | **(C)V(C)(C)** | **4 (0/2/2)** | see note below |
| Georgian | 98 | Standard | (C)(C)(C)(C)(C)(C)V(C)(C)(C) | 7 (3/1/3) | antepenult, weak |
| Dutch | 683 | Netherlandic | (C)(C)(C)V(V)(C)(C)(C)(C) | **8 (3/2/3)** | lexical, coda-sensitive |

- **Two variety mismatches to carry forward.** LAPSyD's Welsh is **Northern** (Bangor), but the
  project targets Southern Welsh; LAPSyD's Irish is **Donegal**. Neither is fatal for a coarse
  syllable canon but both must be flagged in the digests' §0.
- **Digest coverage.** §2 (maximal syllable template, with the compiler's own worked examples —
  Georgian's are especially good: /pɾtskβna/, /βχetkt/), §4 (stress: LAPSyD carries a fixed-stress
  slot and a weight slot), §1 (inventory cross-check against PHOIBLE, plus prose notes on marginal
  and loan-only segments, e.g. Cairene /q/ surviving only in a few words; Welsh /tʃ dʒ/ as
  English-loan-only).
- Arabic's onset value **0** (one onset consonant max) versus Georgian's and Dutch's **3** is the
  cleanest quantitative statement of the "restrictive vs permissive extremes" framing in
  project-goals.md.

### `clts` — Cross-Linguistic Transcription Systems

- **Citation.** List, Johann-Mattis, Cormac Anderson, Tiago Tresoldi & Robert Forkel (eds.).
  *CLTS: Cross-Linguistic Transcription Systems* v2.3.0 (2024-04-19). Jena: MPI-SHH.
  (Editor list per the repo; check `data/references.bib` in the release before citing formally.)
- **URL.** https://clts.clld.org · https://github.com/cldf-clts/clts (releases; Zenodo concept DOI
  10.5281/zenodo.3515744; licence CC BY 4.0) · API: https://github.com/cldf-clts/pyclts (PyPI `pyclts` 4.0.2)
- **Access tier.** OA. **Verification.** Confirmed; not bulk-downloaded, per instructions.
- **Local file.** `pyclts-README.md` (the install + usage doc, saved so the recipe is offline).
- **Install path.** `pip install pyclts`, then clone or unzip a *matching* CLTS data release —
  `pyclts` ≥ 3.0 requires CLTS data ≥ 2.0. Point the API at it:
  `from pyclts import CLTS; clts = CLTS('PATH/TO/clts')`. Alternatively `pip install cldfbench`
  and run `cldfbench catconfig` to have the path registered in the `cldfcatalog` config.
- **IPA → features.** `clts.bipa['tˠ']` parses an arbitrary IPA string, including diacritics it
  has never seen, into a sound object; `.name` is the canonical feature bundle
  (`'voiceless alveolar sibilant-affricate consonant'`), `.generated` / `.alias` flag inferred
  and variant spellings. Translation between transcription systems and to sound classes
  (`clts.soundclass('sca')`) is built in. This is the mechanism for the feature-nearest
  substitution fallback in §3 — and note it handles the **velarized/palatalized diacritics on
  Irish input** natively, which PanPhon handles less gracefully.
- **Digest coverage.** §3 (fallback substitution), §1 (feature vocabulary).

### `phoible` — PHOIBLE 2.0 (CLDF)

- **Citation.** Moran, Steven & Daniel McCloy (eds.). 2019. *PHOIBLE 2.0.* Jena: MPI-SHH.
- **URL.** https://phoible.org · https://github.com/cldf-datasets/phoible (release **v2.0.1**,
  2019-05-08 — the latest; PHOIBLE has not re-released since)
- **Access tier.** OA (CC BY-SA). **Verification.** Confirmed. Not re-downloaded: the four target
  inventories are already in `../../chat-imports/phoible_inventories_starter.csv`.
- **Local file.** `phoible-query.py` — the query recipe the source-plan asked to keep, so the
  starter CSV can be regenerated or extended without redoing the exploration.
- **Query approach.** The CLDF release is a *StructureDataset* at
  `https://raw.githubusercontent.com/cldf-datasets/phoible/v2.0.1/cldf/{values,inventories,languages,parameters}.csv`.
  Plain `csv` is enough — `pycldf` is optional. Joins: `values.csv` has one row per
  segment-in-inventory with `Contribution_ID` = the PHOIBLE **InventoryID** (the number to filter
  on — 231, 2406, 2169, 2183), `Language_ID` = glottocode, `Value` = the segment, plus `Marginal`
  and `Allophones`; the 37 distinctive features live on `parameters.csv` keyed by
  `Parameter_ID`. `values.csv` is ~8.6 MB.
- **Digest coverage.** §1 only. PHOIBLE has **no** phonotactic, syllable or stress data — that gap
  is what LAPSyD, WALS 12A and the per-language monographs fill.

### `wals-12a` / `wals-14a` / `wals-15a` — WALS syllable-structure and stress chapters

- **Citation.** Maddieson, Ian. 2013. Syllable Structure. Goedemans, Rob & Harry van der Hulst.
  2013. Fixed Stress Locations (14A); Weight-Sensitive Stress (15A). In Dryer & Haspelmath (eds.),
  *WALS Online* (v2020.4). Zenodo. doi:10.5281/zenodo.13950591.
- **URL.** https://wals.info/chapter/12 · /14 · /15 (values as TSV at `/feature/12A.tab` etc.)
- **Access tier.** OA (CC BY 4.0). **Verification.** Confirmed.
- **Local files.** `wals-12-syllable-structure.{html,txt}`, `wals-12A-values.csv`,
  `wals-14-stress.{html,txt}`, `wals-14A-values.csv`, `wals-15-stress.{html,txt}`,
  `wals-15A-values.csv`.

**Values for our languages** (verbatim from the TSVs; blank = not in that chapter's sample):

| Language | 12A Syllable Structure | 14A Fixed Stress | 15A Weight-Sensitive Stress |
|---|---|---|---|
| Irish (Donegal) | Complex | — | — |
| Welsh | — | Penultimate | Fixed stress (no weight-sensitivity) |
| Arabic (Egyptian) | Complex | No fixed stress | Right-oriented: one of the last three |
| Georgian | Complex | Antepenultimate | Fixed stress (no weight-sensitivity) |
| Dutch | — | No fixed stress | Right-oriented: one of the last three |
| *(Breton, proxy Celtic)* | Complex | Penultimate | Fixed stress |
| *(German/English, proxy Gmc)* | Complex | No fixed stress | Right-oriented: last three |

- **Gaps found.** **Welsh and Dutch are absent from the 12A sample** (486 languages), and Irish is
  absent from 14A/15A. WALS 12A is also a coarse 3-way classification (Simple / Moderately complex
  / Complex: 61 / 274 / 151) that puts Egyptian Arabic and Georgian in the *same* bucket — which
  is exactly the distinction this project needs, so **12A is not usable as the syllable-typology
  cross-check; LAPSyD's O/N/C index is** (Arabic 0/2/2 vs Georgian 3/1/3).
- **Digest coverage.** §2 (coarse), §4 (stress — 14A/15A are more directly useful than 12A).

---

## Literature

### `kang2011` — Kang, Loanword Phonology

- **Citation.** Kang, Yoonjung. 2011. Loanword Phonology. In Marc van Oostendorp, Colin J. Ewen,
  Elizabeth Hume & Keren Rice (eds.), *The Blackwell Companion to Phonology*, ch. 100. Malden, MA:
  Wiley-Blackwell.
- **URL.** https://yoonjungkang.com/uploads/1/1/6/2/11625099/tbc_100.kang.pdf
- **Access tier.** OA (author's page, direct PDF, no login).
- **Verification.** Confirmed — the URL in the baseline bibliography is live and is the chapter
  it claims to be. 25 pp.
- **Local files.** `kang2011-loanword-phonology.pdf`, `.txt`.
- **Digest coverage.** §3, cross-linguistically. The repair taxonomy the project needs:
  §100.3 segmental adaptation (what governs which native segment a foreign one maps to),
  §100.4 phonotactic adaptation — epenthesis vs deletion, epenthesis site, and **epenthetic
  vowel quality** (this is the section that substitutes for the paywalled Uffmann 2006).
  As warned, the framing is OT/markedness; mine the generalizations and the language examples.

### `smith2024` — Smith, Loanword Phonology

- **Citation.** Smith, Jennifer L. In press. Loanword Phonology. In Adam Jardine & Paul de Lacy
  (eds.), *The Cambridge Handbook of Phonology*, 2nd edn. Cambridge: CUP. Draft, version date
  2025-04-01.
- **URL.** https://users.castle.unc.edu/~jlsmith/home/pdf/smith2024_CHoP2_LoanwordPhonology_circulate.pdf
- **Access tier.** OA (author's page, circulating draft).
- **Verification.** Confirmed, **but the baseline description was wrong on two points**: it is a
  *Cambridge* Handbook chapter, not Blackwell (Smith's Blackwell 2e chapter is "Category-specific
  effects", a different topic), and it is **not linked from her publications page** — the file is
  only discoverable by direct URL. 29 pp.
- **Local files.** `smith2024-loanword-phonology.pdf`, `.txt`.
- **Digest coverage.** §3, and §0/§7 methodology. Deliberately picks up *after* Kang 2011, so the
  two complement rather than duplicate. §3 of the chapter is the useful part for us: the
  non-phonological determinants of adaptation — **orthography** (very relevant: our Irish input is
  hand-IPA, so the tool models an ear-mediated loan, not an eye-mediated one, and the chapter says
  which repairs that choice commits us to), perception, and social context. §4 is theory; skip.

### `easterday2019` — Highly complex syllable structure

- **Citation.** Easterday, Shelece. 2019. *Highly complex syllable structure: A typological and
  diachronic study* (Studies in Laboratory Phonology 9). Berlin: Language Science Press.
  doi:10.5281/zenodo.3268721. 616 pp.
- **URL.** https://zenodo.org/records/3268721 (langsci-press.org/catalog/book/249 was
  unreachable from here on 2026-08-24; the Zenodo API file endpoint worked)
- **Access tier.** OA (CC BY 4.0).
- **Verification.** Confirmed; downloaded (3.4 MB).
- **Local files.** `easterday2019-highly-complex-syllable-structure.pdf`, `.txt`.
- **Digest coverage.** §2, and it is the best open **catalogue of syllable-structure typology**
  found — far more use than WALS 12A because it is built precisely to sub-classify the languages
  WALS lumps as "Complex". **Georgian is one of its core cases** and it quotes attested Georgian
  cluster inventories directly from Butskhrikidze 2002 (e.g. onsets /t’k’b, p’t͡s’k’, psk’,
  txzβ̞, t͡s’q’ɾt, brt͡s’q’, p’ɾt͡s’k’β̞, ɡβ̞pɾt͡skβ̞n/; the coda /ɾt’q’l/; a count that 10% of
  stem-initial onset patterns are "highly complex"). Chapter on cluster typology also gives the
  sonority-profile vocabulary the Georgian and Welsh digests will want in §2.

### `kenstowicz-enhancement` — Loanword Phonology and Enhancement

- **Citation.** Kenstowicz, Michael. 2003. Loanword Phonology and Enhancement. In Young-Se Kang
  et al. (eds.), *Lectures on Universal Grammar and Individual Languages* (Seoul International
  Conference on Linguistics), 104–112.
- **URL.** https://dspace.mit.edu/server/api/core/bitstreams/425c5858-af6b-4fe7-9af3-f6564d9c07d9/content
- **Access tier.** OA (MIT Open Access Articles / DSpace).
- **Verification.** Confirmed; 8 pp.
- **Local files.** `kenstowicz-loanword-phonology-enhancement.pdf`, `.txt`.
- **Digest coverage.** §3, specifically the **absent-segment→substitute** table: why a foreign
  segment maps to one native segment rather than the feature-nearest one. Short; a useful sanity
  check on any substitution row that CLTS feature distance would decide differently.

### `kenstowicz-suchato-thai` — Issues in Loanword Adaptation: a Case Study from Thai

- **Citation.** Kenstowicz, Michael & Atiwong Suchato. Issues in Loanword Adaptation: a Case
  Study from Thai. MIT/Chulalongkorn ms.; published as *Lingua* 116 (2006). The PDF carries no
  volume/page line — confirm pagination before citing it in a digest.
- **URL.** http://lingphil.mit.edu/papers/kenstowicz/loanword_adaptation.pdf
- **Access tier.** OA (MIT author page).
- **Verification.** Confirmed; 6 pp. (condensed author version, not the full journal article).
- **Local files.** `kenstowicz-suchato-thai-loanword-adaptation.pdf`, `.txt`.
- **Digest coverage.** §3. Secondary. An 800-word corpus study; useful because it is explicit
  about **how a language with a restrictive syllable template (CRVC) accommodates foreign
  clusters** — deletion vs epenthesis vs template-fitting — which is the Egyptian Arabic problem
  in a different language. Use as a comparandum, not as data.

### `vandersijs2009` — Loanwords in Dutch (the full book chapter)

- **Citation.** van der Sijs, Nicoline. 2009. Loanwords in Dutch. In Martin Haspelmath & Uri
  Tadmor (eds.), *Loanwords in the World's Languages: A Comparative Handbook*, 338–359. Berlin:
  Mouton de Gruyter.
- **URL.** https://pure.knaw.nl/ws/files/475024/Van_der_Sijs_Loanwords_in_the_World%27s_Languages.pdf
- **Access tier.** OA — publisher's version of record, deposited in the **KNAW research portal**.
  (The parent volume itself is paywalled; this single chapter is legitimately open.)
- **Verification.** Confirmed; 10 pp. of PDF (the chapter proper plus the repository cover sheet).
- **Local files.** `vandersijs2009-dutch-loanwords-chapter.pdf`, `.txt`.
- **Digest coverage.** The prose companion to `wold-dutch-loanpairs.csv` — §7 provenance and §3
  by inference (which donor languages, which periods, how the compiler judged integration).
  Also `wold-chapter-12-dutch-vandersijs.md` is the shorter online version of the same author's
  methodology notes (analyzability, dating, borrowed-status scale). **Hand this to the Dutch
  agent.**

---

## Not used (paywalled or login-walled)

- **Uffmann, Christian. 2006. Epenthetic vowel quality in loanwords: Empirical and formal issues.
  *Lingua* 116(7): 1079–1111.** ScienceDirect, paywalled; no author-page or repository mirror
  found. *What we lose:* the one large-corpus statistical decomposition of epenthetic vowel
  quality into (a) vowel harmony, (b) local assimilation to the preceding consonant, (c) default
  insertion — across Shona, Sranan, Samoan, Kinyarwanda. That three-way decomposition is exactly
  the shape a §3 epenthesis rule wants. **Partly recoverable** from Kang 2011 §100.4, which
  summarizes it; the corpus statistics are not.
- **Uffmann, Christian. 2007. *Vowel Epenthesis in Loanword Adaptation* (Linguistische Arbeiten
  510). Tübingen: Niemeyer.** The book version. Purchase only.
- **Haspelmath, Martin & Uri Tadmor (eds.). 2009. *Loanwords in the World's Languages: A
  Comparative Handbook.* Berlin: Mouton de Gruyter.** doi:10.1515/9783110218442 — not open.
  *What we lose:* little, for our purposes. The **data** are fully open in WOLD/CLDF, the short
  online chapters are open, and the one chapter we actually want (Dutch) is open via KNAW.
- **Paradis, Carole & Darlene LaCharité. 2011. Loanword adaptation: from lessons learned to
  findings. In Goldsmith, Riggle & Yu (eds.), *The Handbook of Phonological Theory*, 2nd edn.**
  Paywalled. *What we lose:* the main rival synthesis to Kang's, and the source of the
  "minimality / preservation" generalizations about *how many* repairs a loan undergoes. Both
  Kang 2011 and Smith 2024 summarize its claims.
- **Kang, Yoonjung. 2013. Loanword phonology. *Oxford Bibliographies in Linguistics.*** Paywalled
  annotated bibliography. *What we lose:* a curated reading list; not data.
- **LAPSyD "Private" data layer** — free account required. Not needed: all five of our languages
  are in the public layer.

---

## Not found / not verified

- No open cross-linguistic survey devoted specifically to **epenthesis-vs-deletion choice** was
  located beyond the Kang 2011 / Smith 2024 chapters. Searches for one returned only
  single-language case studies (Persian, Javanese, Italian, Dolgan, Japanese), all either
  paywalled or on academia.edu/ResearchGate.
- Sharon Peperkamp's perception-based loanword papers (BLS 2005 etc.) are open at
  journals.linguisticsociety.org, but they argue *why* adaptation happens rather than cataloguing
  repairs, and the project has ruled theory out of scope. Not downloaded; noted here so a later
  agent doesn't re-search for them.
