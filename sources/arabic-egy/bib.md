# bib.md — Egyptian (Cairene) Arabic, target language

Acquired 2026-08-24 per `../ACQUISITION-BRIEF.md`. Open access only. Section numbers (§1–§8)
refer to `../DIGEST-TEMPLATE.md`.

Text extraction: PDFs via `pdftotext -layout`; OpenEdition and Wikipedia pages saved as
`.html` + a `.txt` extraction (Wikipedia also as `.wikitext`); the Abdel-Massih scans use
archive.org's OCR (`_djvu.txt`) because the PDFs carry only a cover-page text layer.

---

## Primary repair source

### `ema1958`
Hafez, Ola (1996). "Phonological and Morphological Integration of Loanwords into Egyptian
Arabic." *Égypte/Monde arabe*, Première série, 27–28 (*Les langues en Égypte*), pp. 383–410.
DOI 10.4000/ema.1958. Online since 08 July 2008.
- URL: https://journals.openedition.org/ema/1958
- Access: **OA** (no login; the site fronts an Anubis JS challenge for browser-like
  user-agents — a plain `curl/7.x` UA is served the article directly).
- Verified: **confirmed**, and the baseline bibliography's description is accurate. Author and
  year were unattributed in the baseline; now pinned to Ola Hafez 1996.
- Files: `ema1958.html`, `ema1958.txt` (full text, ~72 KB), `ema1958.pdf` (2-page OpenEdition
  cover stub only — the real content is in the HTML/TXT).
- Covers: §3 almost entirely — sections on consonant alteration, vowel alteration, intrusive
  vowels and consonants, gemination, syllabic omission, stress shifting, metathesis, and
  "resistance to phonological integration"; plus §6 (derivational paradigms, gender, broken
  plurals on loans) and §7 (dozens of source→EA pairs in running text). Also §1 (which foreign
  segments EA lacks and what replaces them).
- **Caveat, stated by the journal**: the online transcriptions, unlike the print original, do
  **not** mark emphatic consonants. Any emphatic in an example taken from this file is
  unrecoverable and must be marked as such in `attested.csv`. The article's own transcription
  key is in its Appendix ("symbols used").

### `kwpl-ot-cairene-loan`
Galal, Mohamed (2004). "An OT Approach to Loanword Adaptation in Cairene Arabic."
*Kansas Working Papers in Linguistics*, vol. 27. University of Kansas, ISSN 1043-3805.
- URL: https://journals.ku.edu/kwpl/article/download/17171/15446
- Access: **OA**. Verified: **confirmed** (found in acquisition, not in the baseline).
- Files: `kwpl-ot-cairene-loan.pdf`, `.txt`
- Covers: §3 — vowel epenthesis in English→Cairene loans (site and quality), and the special
  behaviour of s+obstruent onsets. §2 for the onset ban that drives it. Theory is OT; take the
  data tables.

---

## Phonology / phonotactics / stress

### `broselow1976`
Broselow, Ellen (1976). *The Phonology of Egyptian Arabic.* PhD dissertation, University of
Massachusetts Amherst. 218 pp. (UMI microfilm scan, OCR'd).
- URL: https://linguistics.stonybrook.edu/faculty/ellen.broselow/files/broselow1976.pdf
  (author's own faculty page at Stony Brook)
- Access: **OA**. Verified: **confirmed**. Note: not found openly on ScholarWorks@UMass; the
  author page is the open copy. ProQuest's listing is paywalled.
- Files: `broselow1976.pdf` (7.5 MB), `broselow1976.txt`
- Covers: §2/§3/§4 at the finest grain available openly. Ch. 1 = epenthesis (1.1), high-vowel
  deletion, stress (1.3), vowel shortening (1.4), **word-initial epenthesis (1.5)**, glottal
  stop insertion (1.6), emphasis and the syllable incl. emphasis spread (1.8), ordering of
  syllabification rules (1.9). Ch. 2 covers long vowels, vowel lengthening/shortening, and
  nisba adjectives (§6). OCR is readable but imperfect; check IPA/transcription against the
  page images before quoting.

### `broselow-arabic-syll`
Broselow, Ellen (2018). "Syllable Structure in the Dialects of Arabic." (Revised paper;
author's manuscript.)
- URL: https://www.stonybrook.edu/commcms/linguistics/faculty/ellen.broselow/files/Broselow_ArabicSyllStrPaper_revised.pdf
- Access: **OA**. Verified: **confirmed**.
- Covers: §2 and §3 — the cross-dialect typology of syllable shapes and, centrally for us,
  the **Cairene C2–C3 vs. Iraqi C1–C2 epenthesis parameter** that the baseline attributes to
  Broselow 1983/1992. This open paper is the usable replacement for those two paywalled items.
- Files: `broselow-arabic-syll.pdf`, `.txt`

### `broselow-position-quality`
Broselow, Ellen (2015). "The Typology of Position-Quality Interactions in Loanword Vowel
Insertion." (Book chapter 12, author's manuscript.)
- URL: https://www.stonybrook.edu/commcms/linguistics/faculty/ellen.broselow/files/Position-Quality%20Interactions.pdf
- Access: **OA**. Verified: **confirmed**.
- Covers: §3 — where the epenthetic vowel goes in initial CC and **what quality it takes**,
  cross-linguistically with Arabic cases. This is the source for epenthetic vowel quality.
- Files: `broselow-position-quality.pdf`, `.txt`

### `broselow-stress-epenthesis`
Broselow, Ellen (2008). "Stress-Epenthesis Interactions." (Author's manuscript.)
- URL: https://www.stonybrook.edu/commcms/linguistics/faculty/ellen.broselow/files/p2kpaper_rev.pdf
- Access: **OA**. Verified: **confirmed**.
- Covers: §4 — whether epenthetic vowels count for stress (Cairene among the cases). Needed to
  order the stress rule against the epenthesis rule in the rule file.
- Files: `broselow-stress-epenthesis.pdf`, `.txt`

### `broselow-stress-adaptation`
Broselow, Ellen (2009). "Stress Adaptation in Loanword Phonology: Perception and
Learnability." (Author's manuscript; Boersma & Hamann volume.)
- URL: https://www.stonybrook.edu/commcms/linguistics/faculty/ellen.broselow/files/boersmahamannpaper_march09.pdf
- Access: **OA**. Verified: **confirmed**.
- Covers: §3/§4 — what happens to source-language stress in loans.
- Files: `broselow-stress-adaptation.pdf`, `.txt`

### `broselow-marginal-phonology`
Broselow, Ellen. "Marginal Phonology: Phonotactics on the Edge." (Author's manuscript.)
- URL: https://www.stonybrook.edu/commcms/linguistics/faculty/ellen.broselow/files/MarginalPhonology.pdf
- Access: **OA**. Verified: **confirmed**.
- Covers: §2 — word-edge vs. word-interior cluster asymmetries (i.e. why a cluster licit
  medially may be banned initially/finally). Main case study is Balantak, not Arabic; keep as
  a secondary/conceptual source, low priority.
- Files: `broselow-marginal-phonology.pdf`, `.txt`

### `watson2011-word-stress`
Watson, Janet C. E. (2011). "Word Stress in Arabic." In *The Blackwell Companion to
Phonology*, ch. 135, pp. 2990–3019. Oxford: Wiley-Blackwell.
- URL: https://eprints.whiterose.ac.uk/id/eprint/75747/9/watsonjce3a.pdf (White Rose
  Research Online, author accepted manuscript)
- Access: **OA** (repository copy of an otherwise paywalled chapter). Verified: **confirmed**.
- Covers: §4 — the stress rule proper, per dialect including Cairene, with the syncope/
  epenthesis/stress interactions spelled out. This is the best open substitute for Watson 2002.
- Files: `watson2011-word-stress.pdf`, `.txt`

### `watson2007-syllabification`
Watson, Janet C. E. (2007). "Syllabification Patterns in Arabic Dialects: Long Segments and
Mora Sharing." *Phonology* 24(2), 335–356.
- URL: https://eprints.whiterose.ac.uk/id/eprint/75742/2/watson.242Syllabification.pdf
- Access: **OA** via White Rose (the Cambridge Core copy is paywalled). Verified: **confirmed**.
- Covers: §2 — syllable templates, superheavy syllables, gemination and long-segment
  behaviour across dialects.
- Files: `watson2007-syllabification.pdf`, `.txt`

### `mccarthy1979-stress-syll`
McCarthy, John J. (1979). "On Stress and Syllabification." *Linguistic Inquiry* 10, 443–466.
- URL: https://scholarworks.umass.edu/bitstreams/a28117ff-0acd-4a44-b0eb-94acbab83188/download
  (record: https://scholarworks.umass.edu/linguist_faculty_pubs/53/)
- Access: **OA**. Verified: **confirmed**.
- Covers: §4/§2 — the classic Cairene syllable-weight/stress analysis that later work
  (Broselow, Watson, Kiparsky) argues with. Use for the stress rule statement and as the
  reference point for `CONFLICT:` lines.
- Files: `mccarthy1979-stress-syll.pdf`, `.txt`

### `kiparsky-syll-moras`
Kiparsky, Paul. "Syllables and Moras in Arabic." (Author's manuscript, Stanford.)
- URL: https://web.stanford.edu/~kiparsky/Papers/syll.pdf
- Access: **OA**. Verified: **confirmed**.
- Covers: §2/§3 — a dialect typology (C-dialects / VC-dialects / CV-dialects) built precisely
  on epenthesis site and syllabification; Cairene is one of the anchors. Good cross-check on
  Broselow's parameter.
- Files: `kiparsky-syll-moras.pdf`, `.txt`

### `ojml-cairene-syllable`
Aquil, Rajaa (2013). "Cairene Arabic Syllable Structure through Different Phonological
Theories." *Open Journal of Modern Linguistics* 3(3), 259–267. DOI 10.4236/ojml.2013.33034.
- URL: https://www.scirp.org/pdf/OJML_2013082215322842.pdf
- Access: **OA** (CC-BY). Verified: **confirmed** (title in the journal is misspelled
  "Cairne").
- Covers: §2 — a survey of the Cairene syllable inventory (CV, CVC, CVV, CVCC, CVVC) and the
  competing analyses, with the epenthesis facts restated. Convenient orientation piece;
  everything in it is derivative of the primary sources above.
- Files: `ojml-cairene-syllable.pdf`, `.txt`

### `ijllnet-cairene-english-syll`
Khalifa, Mohamed Fathy (2018). "Cairene Colloquial Arabic and English Syllable Structures and
Implications for L2 English Syllable Acquisition." *International Journal of Language and
Linguistics* 5(3). DOI 10.30845/ijll.v5n3p9.
- URL: https://ijllnet.thebrpi.org/journals/Vol_5_No_3_September_2018/9.pdf
- Access: **OA**. Verified: **confirmed**.
- Covers: §2 and §3 — an explicit side-by-side of licit English vs. Cairene onsets/codas and
  the repair strategies Cairene speakers apply to English clusters. Directly usable as a
  cluster inventory even though the framing is L2 acquisition, not loanwords. (Publisher is a
  low-selectivity venue; cross-check its cluster lists against Broselow/Watson.)
- Files: `ijllnet-cairene-english-syll.pdf`, `.txt`

### `hassig2011-cairene`
Hassig, Hannah (2011). *Deriving Cairene Arabic from Modern Standard Arabic: A Framework for
Using Modern Standard Arabic Text to Synthesize Cairene Arabic Speech from Phonetic
Transcription.* MA thesis (Research Linguistics), Universiteit Utrecht (UiL-OTS).
Supervisors: René Kager, Hugo Quené. 166 pp.
- URL: https://studenttheses.uu.nl/handle/20.500.12932/8367 (PDF via the DSpace REST
  bitstream endpoint; the `/bitstream/handle/...` path now returns the SPA shell)
- Access: **OA**. Verified: **confirmed** (found in acquisition, not in the baseline).
- Covers: §1, §2, §4, §5 — the single most rule-file-shaped source in this directory: an
  explicit grapheme→IPA mapping for Cairene, an inventory, syllabification and stress rules
  written as an ordered procedure, and a worked constraint set. Written for a speech
  synthesizer, so it is unusually explicit about defaults and edge cases.
- Files: `hassig2011-cairene.pdf`, `.txt`

### `hellmuth2007-prosodic`
Hellmuth, Sam (2007). "The Relationship between Prosodic Structure and Pitch Accent
Distribution: Evidence from Egyptian Arabic." *The Linguistic Review* 24(2–3).
(White Rose pre-publication version.)
- URL: https://eprints.whiterose.ac.uk/43996/1/Hellmuth_2007_TLR_prepublication_version.pdf
- Access: **OA**. Verified: **confirmed**.
- Covers: §4 — phrase-level prosody in Cairene. Peripheral to a word-level rewrite tool; keep
  only if the digest needs a second opinion on word stress.
- Files: `hellmuth2007-prosodic.pdf`, `.txt`

---

## Reference grammar / inventory

### `abdelmassih-intro`
Abdel-Massih, Ernest T. (1975; 1981 printing; MPublishing reissue 2011). *An Introduction to
Egyptian Arabic.* Ann Arbor: Center for Near Eastern and North African Studies, University of
Michigan. Part One is a dedicated **Phonology** section.
- URL (open host of record): https://deepblue.lib.umich.edu/handle/2027.42/94559 (UMich Deep
  Blue, Open Educational Resources)
- URL actually used: https://archive.org/details/egyptian-arabic-ernest-t-abdel-massih
  (unrestricted mirror; Deep Blue blocks non-browser clients with Cloudflare, so the file was
  taken from archive.org)
- Access: **OA** (Deep Blue OER). Verified: **confirmed**.
- Files: `abdelmassih-intro.pdf` (18 MB, searchable text layer), `abdelmassih-intro.txt`
  (archive.org OCR)
- Covers: §1, §2, §5, and some of §4 — a teaching-grammar description of the Cairene segment
  inventory, syllable and cluster patterns, stress, and the book's own transcription system.
  Contemporary Americanist transcription, not IPA; convert carefully.

### `abdelmassih-v3`
Abdel-Massih, Ernest T., Zaki N. Abdel-Malek & El-Said M. Badawi, in association with Ernest
N. McCarus (1979; MPublishing reissue 2011). *A Comprehensive Study of Egyptian Arabic,
Volume Three: A Reference Grammar of Egyptian Arabic* (preliminary edition). Ann Arbor:
University of Michigan. ISBN 978-1-60785-216-2.
- URL (open host of record): Deep Blue, UMich — the series' handles are in the range
  2027.42/94559–94564 (v.1 = 2027.42/94560); the exact per-volume handle was not confirmed
  because Deep Blue blocks non-browser clients
- URL actually used: https://archive.org/details/a-comprehensive-study-of-egyptian-arabic
- Access: **public domain** — the volume's own copyright page states "Copyright is claimed
  until June 1989. Thereafter all portions of this work covered by this copyright will be in
  the public domain" (US Office of Education grant). Verified: **confirmed**; the baseline's
  "(verify) open on Deep Blue" guess is correct.
- Files: `abdelmassih-v3.pdf` (19 MB), `abdelmassih-v3.txt` (archive.org OCR, ~460 KB —
  moderate quality, transcription diacritics are frequently mangled)
- Covers: §2, §6, and parts of §3 — morphophonemic rules (vowel elision, vowel shortening),
  the noun/adjective system, nisba and feminine endings, definite article behaviour, and an
  explicit note on how loanwords ending in a vowel are treated.

### `abdelmassih-v4`
Same authors (1979; reissue 2011). *A Comprehensive Study of Egyptian Arabic, Volume Four:
Lexicon Part 1 Egyptian Arabic–English; Part 2 English–Egyptian Arabic.*
- URL: as above (same Deep Blue series; file taken from the same archive.org item).
- Access: **public domain** (same statement). Verified: **confirmed**.
- Files: `abdelmassih-v4.pdf` (18 MB), `abdelmassih-v4.txt` (OCR)
- Covers: §7 — a dictionary in which established loans appear in their Cairene shape; usable
  to confirm or add attested adaptations. OCR quality limits automated harvesting.

### `asha-arabic-inventory`
American Speech-Language-Hearing Association. "Arabic Phonemic Inventory." (Phonemic
Inventories and Cultural and Linguistic Information Across Languages series; undated, 2 pp.)
- URL: https://www.asha.org/siteassets/uploadedfiles/multicultural/arabicphonemicinventory.pdf
  (index: https://www.asha.org/practice/multicultural/phono/)
- Access: **OA**. Verified: **confirmed**; the baseline's description is accurate.
- Files: `asha-arabic-inventory.pdf`, `asha-arabic-inventory.txt`
- Covers: §1 only, and thinly — a one-page IPA consonant chart for **Arabic generally**, not
  Cairene, with a note that emphatics are written plain in the chart and should be read
  /tˤ dˤ sˤ ðˤ/. Its chart includes /θ ð q/, which Cairene lacks or realizes differently; do
  not use it as the Cairene inventory. Low value now that better sources are in hand.

### `alqarhi2019-arabic-phonology`
Alqarhi, Awaad (2019). "Arabic Phonology." *English Linguistics Research* 8(4), 9–.
DOI 10.5430/elr.v8n4p9.
- URL: https://www.sciedupress.com/journal/index.php/elr/article/download/16452/10555
- Access: **OA**. Verified: **confirmed** (same file as `../../chat-imports/`'s
  `arabic-phonology.pdf`; copied here for self-containment).
- Files: `alqarhi2019-arabic-phonology.pdf`, `.txt`
- Covers: §0/§1 — MSA vs. dialect-group survey. As the project notes already say, low value:
  a general survey with no Cairene-specific rules. Cite only for "Egyptian is the de facto
  standard spoken dialect".

### `ema1952-woidich`
Woidich, Manfred (1996). "Rural Dialect of Egyptian Arabic: An Overview." *Égypte/Monde
arabe*, Première série, 27–28. DOI 10.4000/ema.1952.
- URL: https://journals.openedition.org/ema/1952
- Access: **OA**. Verified: **confirmed** (sibling article in the same issue as `ema1958`).
- Files: `ema1952-woidich.html`, `ema1952-woidich.txt`
- Covers: §0 — what is *not* Cairene. Useful for keeping rural features (e.g. /g/~/dʒ/, /q/
  reflexes, different stress) out of the digest. No loanword data.

---

## Wikipedia (first-pass and orthography/morphology reference)

All fetched 2026-08-24 via the REST HTML endpoint plus `action=raw` wikitext; `.txt` is a
plain-text extraction of the rendered HTML.

| key | article | files | covers |
|---|---|---|---|
| `wiki-egy-phonology` | "Egyptian Arabic phonology" | `.html/.txt/.wikitext` | §1 inventory incl. /p v ʒ tʃ/ status; §2 syllable structure and clusters; §3 /q/→/ʔ~k/, /θ ð/ merger; §4 stress rule |
| `wiki-egy-arabic` | "Egyptian Arabic" | `.html/.txt/.wikitext` | §0 variety, §5 orthography practice, §6 grammar (article, gender, nisba, plurals) |
| `wiki-arabic-phonology` | "Standard Arabic phonology" (the title "Arabic phonology" is now a redirect to this) | `.html/.txt/.wikitext` | §0/§1 the MSA baseline Cairene is described against |
| `wiki-help-ipa-egy` | "Help:IPA/Egyptian Arabic" | `.html/.txt/.wikitext` | §1/§5 the segment-by-segment IPA key Wikipedia uses for Cairene |
| `wiki-sun-moon-letters` | "Sun and moon letters" | `.html/.txt/.wikitext` | §6 definite-article assimilation, stated concisely with the full letter lists |
| `wiki-nisba` | "Nisba (onomastics)" | `.html/.txt/.wikitext` | §6 the nisba suffix -iyy / -i / fem. -iyya and its use in names |
| `wiki-romanization-arabic` | "Romanization of Arabic" | `.html/.txt/.wikitext` | §5 the competing transliteration conventions and where they diverge |
| `wiki-arabic-diacritics` | "Arabic diacritics" | `.html/.txt/.wikitext` | §5 shadda (gemination), tāʾ marbūṭa, sukūn — needed to read any Arabic-script example |

---

## Not used (paywalled, login-walled, or blocked)

- **Watson, Janet C. E. (2002). *The Phonology and Morphology of Arabic.* OUP.** [Buy]
  The authoritative Cairene reference. What we lose: a single consistent statement of the
  inventory, syllabification, stress and morphophonology. Mitigated by `watson2011-word-stress`
  + `watson2007-syllabification` (same author, open) and `broselow1976`.
- **Gary, Judith O. & Saad Gamal-Eldin (1982). *Cairene Egyptian Colloquial Arabic.*
  Lingua Descriptive Studies 6.** [Buy/library] What we lose: a compact descriptive grammar
  with a clean phonotactics section. Largely covered by `abdelmassih-v3` + `abdelmassih-intro`.
- **Broselow, Ellen (1983). "Nonobvious Transfer: On Predicting Epenthesis Errors."** and
  **Broselow (1992). "Parametric Variation in Arabic Dialect Phonology"** (*Perspectives on
  Arabic Linguistics IV*, Benjamins). [Buy/library] Not open anywhere checked, including the
  author's own page. What we lose: nothing essential — `broselow-arabic-syll` (2018) restates
  the Cairene C2–C3 vs. Iraqi C1–C2 epenthesis parameter, and `kiparsky-syll-moras` gives an
  independent version.
- **"Non-concatenative morphological domains constrain phonotactics: a case study of Egyptian
  Arabic", *Phonology* (Cambridge Core).** [Buy] Would sharpen §2 (which clusters are barred
  within a root vs. across morpheme boundaries). No open copy found.
- **"Phonological Adaptation of Loanword into Egyptian Arabic" (2020), an Egyptian Knowledge
  Bank journal (jfhsc); author not verified.**
  https://jfhsc.journals.ekb.eg/article_158923_55589625843c11e6564b571f77b4c47b.pdf —
  nominally **OA**, but journals.ekb.eg **blocked this machine** (HTTP 429,
  "Access Restricted … automated scraping"), so it could not be downloaded or its authorship
  verified. Worth retrieving by hand in a browser: it is a second Egyptian-Arabic loanword
  paper and would independently corroborate `ema1958`.
- **"Phonological Adaptation of English Borrowings in the Egyptian Press with Reference to
  Al-Ahram Newspaper" (2018), *Bulletin of the Faculty of Arts* (EKB).**
  https://bfa.journals.ekb.eg/article_188161_3d50511686e40b48f34ecf2d7a6976a8.pdf — same EKB
  block. Nominally OA; a press-corpus source would be a good extra §7 data set.
- **academia.edu / ResearchGate only** (login wall, no repository mirror found):
  "The Phonotactic Adaptation of English Loanwords in Arabic"; "A Moraic Account of English
  Loanwords into Egyptian Arabic"; "Stress and Syllable Repair in Egyptian Arabic Loanwords
  from English and French"; "Bootlegging Monosyllable Loanwords into Cairene Arabic";
  "English Loanwords in the Egyptian Variety of Arabic". Several of these are the same handful
  of authors; the last two would add §7 rows.
- **"The lexicalization of English loanwords into Egyptian Arabic" (2015), Univ. de Navarra,
  hdl 10171/39961.** Landing page returns 403 to this machine; not retrieved.

## Not found

- **No JIPA "Illustrations of the IPA" for Egyptian/Cairene Arabic.** Searched; the Arabic
  illustrations in JIPA cover MSA and other varieties, none Cairene. §1 phonetic detail must
  come from `broselow1976` / `hassig2011-cairene` instead.
- **No open paper found on Arabic transcription of foreign proper names with a segment-mapping
  table** (taʿrīb of proper nouns). Searched OpenAlex and the web; the near hits are NLP
  transliteration papers with no phonological mapping table. Per the brief, Arabic-Wikipedia
  renderings of foreign names remain the fallback attested-data source for §7 — **not scraped
  yet**, and any rows from it must be tagged as transliteration practice.
- **Abdel-Massih volumes 1 and 2** (conversations; proverbs) are equally open on the same
  archive.org item but were not downloaded — no phonology content.
