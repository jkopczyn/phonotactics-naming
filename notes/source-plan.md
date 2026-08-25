# Plan: finding and digesting sources for the rule files

Companion to `project-goals.md`. Baseline bibliography is `../chat-imports/phonology_rule_file_sources.md`
(from the 094f80f3 chat) — this plan adds to it rather than repeating it. Items marked **(verify)**
are from my own knowledge, not from the imported chats, and need an access/existence check in
step 1. **Constraint: open-access sources only** (user decision 2026-08-24); paywalled titles are
listed only so the gap is visible.

## 0. Decide the digest schema first

Extraction is only repeatable if every language is digested into the same shape. Before reading
anything, fix `phonotactics/sources/DIGEST-TEMPLATE.md` with these sections, each entry carrying a
source + page citation:

1. Inventory deltas vs. the PHOIBLE row (marginal segments, loan segments, dialect notes)
2. Syllable template; licit onsets, codas, medial clusters; sonority/cluster constraints
3. Repair: epenthesis (site, vowel quality, conditions), deletion, substitution table for
   segments absent from the inventory, gemination/glide rules, word-edge rules (final devoicing…)
4. Stress and vowel length
5. Romanization conventions (and, for strand 4, fit against the existing names)
6. Morphology snippets usable for epithets
7. Attested adaptation examples (≥30 source→target pairs) — these become the test suite
8. Irish-specific mismatch decisions (broad/slender, /ɣ/, lenition outputs, voiceless sonorants)

## 1. Acquire (one pass, mostly delegable)

Layout: `phonotactics/sources/<lang>/` holding downloaded open PDFs/HTML-as-text plus a
`bib.md` with access tier (open / free-account / paywalled / library). Paywalled scans must not
be committed; add `phonotactics/sources/**/*.pdf` to `.gitignore` except the open ones, or keep
paid material outside the repo.

### Cross-linguistic infrastructure
- PHOIBLE CLDF (`cldf-datasets/phoible`) — already used; keep the query script this time.
- CLTS (`cldf-clts/clts`) — IPA → feature bundles; alternative/complement to PanPhon.
- LAPSyD (lapsyd.huma-num.fr) — maximal syllable shape cross-check for all four.
- WOLD (wold.clld.org; data open, CLDF on GitHub `lexibank/wold`) — covers **Dutch** (van der
  Sijs chapter) and the Mayan **Q'eqchi'**; does *not* cover Welsh, Arabic, or Georgian
  **(verify)**. The companion book (Haspelmath & Tadmor 2009) is paywalled; the online chapters
  and data are what we use.
- Kang 2011 "Loanword Phonology" (open PDF on yoonjungkang.com); J.L. Smith 2024 (open PDF).
  Read once for the repair taxonomy; skip the theory.
- Wikipedia "<Language> phonology" pages for all five languages — first pass, 20 min each.

### Irish (source side)
- Wikipedia "Irish phonology" (detailed; broad/slender tables).
- Ní Chasaide 1999, "Irish", JIPA Illustration **(verify open access)**.
- Ó Siadhail, *Modern Irish* (CUP) phonology chapters — library/purchase.
- Old Irish (strand 5): Wikipedia "Old Irish" phonology section; Thurneysen, *A Grammar of Old
  Irish* (DIAS 1946; scans circulate, copyright status unclear); Stifter, *Sengoídelc* (Syracuse
  UP, purchasable); eDIL (dil.ie) for vocabulary. Lowest priority — no filter to write.

### Egyptian (Cairene) Arabic — strand 1
- Watson 2002 (OUP) — paywalled, **not used**; Google Books preview only if a specific
  question needs it.
- ASHA "Arabic Phonemic Inventory" PDF; Wikipedia "Egyptian Arabic phonology" (both in bib).
- Broselow 1976/1992 on Egyptian vs Iraqi epenthesis (ResearchGate, free account).
- "Phonological and Morphological Integration of Loanwords into Egyptian Arabic",
  Égypte/Monde arabe, journals.openedition.org/ema/1958 (open) — attested substitution tables.
  **Primary Arabic repair source under open-only.**
- "The Phonotactic Adaptation of English Loanwords in Arabic"; OT analysis of loanword adaptation
  in Cairene Arabic (academia.edu/ResearchGate) — mine the data tables only.
- Abdel-Massih et al., *A Comprehensive Study of Egyptian Arabic* (U. Michigan, 1970s) — open on
  Deep Blue **(verify)**; Gary & Gamal-Eldin 1982, *Cairene Egyptian Colloquial Arabic*
  (Lingua Descriptive Studies) — library.
- Cheap attested data: Arabic-Wikipedia renderings of Irish/English personal and place names
  (mediated by English pronunciation, so use as a substitution sanity check, not as gold).
- Already in repo: Alqarhi 2019 — skim only.

### Southern Welsh — strand 2
- Hannahs 2013 (OUP) — paywalled, **not used**. Welsh is where open-only costs most; compensate
  with Wikipedia + Wood + Parry-Williams + any open cluster paper.
- Ball & Jones (eds.) 1984, *Welsh Phonology* (U. Wales Press), esp. Awbery's chapter on
  phonotactic constraints **(verify)**; Ball & Williams 2001, *Welsh Phonetics* (Mellen) — library.
- Wood 1986, "Vowel Quantity and Syllable Structure in Welsh" (swphonetics.com, open) — treats
  loanword syllable adaptation.
- "Word-Initial Clusters in Welsh" (ResearchGate).
- Parry-Williams 1923, *The English Element in Welsh* (Cymmrodorion; public domain, archive.org)
  **(verify)** — a large corpus of attested English→Welsh adaptations; ideal gold-set source.
- Historical **Irish → Welsh loanwords** exist (Irish settlement in Dyfed/Gwynedd; e.g. work
  following Jackson, *Language and History in Early Britain*) — the only place a real
  Irish-into-target adaptation is attested for any of the four. Worth a targeted search
  **(verify)**.

### Dutch — strand 3
- Booij 1995 (OUP) — paywalled, **not used**; WOLD + JIPA + Wikipedia cover the gap well.
- Gussenhoven 1992, "Dutch", JIPA Illustration **(verify open)**.
- Trommelen 1984, *The Syllable in Dutch* (Leiden diss.) — possibly open **(verify)**.
- Kager, "Phonotactics as phonology…" and Nagy, "The phonological integration of loanwords in
  Dutch" (academia.edu).
- WOLD Dutch dataset + van der Sijs chapter — attested adaptations, machine-readable. Best gold
  set of the four.
- Decide Belgian vs Netherlandic early (affects /ɣ/ vs [x], /v z/ devoicing, /r/).

### Georgian — strand 4
- Butskhrikidze 2002, *The Consonant Phonotactics of Georgian* (LOT 063, fully open PDF) — the
  backbone. Long; digest the cluster chapters, not the derivational argument.
- Shosted & Chikovani 2006, "Standard Georgian", JIPA Illustration **(verify open)**.
- Hewitt 1995, *Georgian: A Structural Reference Grammar* (Benjamins); Aronson, *Georgian: A
  Reading Grammar* — library, for stress and morphology snippets.
- Self (n.d.) "OT Analysis of Vowel Syncope in Georgian" (diu.edu, open) — inventory prose.
- Attested data: Georgian adaptation of Russian/English loans (search for a paper with tables);
  Georgian-Wikipedia transliterations of foreign names.
- Romanization: none standard for our purpose; must be designed to match *Tchaeul, Kas'queil…*
  Keep the Mayan (K'iche') option's apostrophe orthography in view as the model for that.

## 2. Digest (per language, delegable, parallel)

For each language, one agent per source reads the text (pdftotext / HTML) and fills the
template sections it can support, with page cites; then one agent per language merges the
per-source digests into `sources/<lang>/digest.md`, marking conflicts between sources
explicitly rather than resolving them silently. A separate review agent spot-checks every
repair rule and every substitution claim against the attested-examples section (rule that has
no example → flagged "unattested"). Wikipedia is the cheap first source per language; the
monograph pass then only fills gaps and sharpens cluster constraints.

Model choice: Opus 5 medium for reading/digesting; a GPT-5.6 reviewer for the cross-check;
Fable only for the merge of the harsh-strand (Georgian + overlay) where the judgment call is.

Order: Arabic and Welsh (pinned) → Georgian (backbone is open, and the existing-names
constraint makes it the riskiest) → Dutch → Irish source inventory (needed before any rule can
be tested, so actually runs in parallel from the start) → Old Irish last.

## 3. Outputs of this phase

- `sources/<lang>/bib.md` — reconstructed bibliography with access tier (replaces the lost
  claude.ai file).
- `sources/<lang>/digest.md` — filled template.
- `sources/<lang>/attested.tsv` — source form, target form, provenance; seed of the test suite.
- `sources/irish/inventory.md` — broad/slender pairs, lenition outputs, length, stress.
- A short decisions list for the user: broad/slender treatment per target; Belgian vs
  Netherlandic; strand-4 overlay vs pure Georgian; which paywalled monographs to buy/borrow.

## Decisions (2026-08-24)

- Open-only: **decided**.
- Georgian and Dutch: kept. User is indifferent between these and any better-documented
  neighbour; under open-only, Georgian is the best-served target (Butskhrikidze) and Dutch has
  WOLD, so neither needs swapping.
- Bibliography: **recovered** (`../chat-imports/phonology_rule_file_sources.md`).
- Irish input: hand IPA; **no G2P**.

## Still open (resolve while digesting, not before)

1. Strand 4: overlay-on-Georgian vs pure Georgian rules — decide once the Georgian digest shows
   how far pure Georgian gets toward *Tchaeul / Kas'queil / Xelxyx*.
2. Dutch: Belgian (matches the PHOIBLE row, keeps voiced /ɣ v z/) vs Netherlandic — with Booij
   out of scope the PHOIBLE row is the path of least resistance; default Belgian.
3. Whether to add a creole-style reduction layer (user not fully persuaded by the loanword
   framing; see project-goals.md).
