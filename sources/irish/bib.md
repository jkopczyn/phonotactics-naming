# Irish (Gaeilge) + Old Irish — source bibliography

Donor/source side of the project: Irish supplies the vocabulary, so this directory has to
support (a) a fully specified broad/slender phoneme inventory, (b) mutation outputs as
phonemes, (c) length and diphthongs, (d) stress incl. the Munster/non-Munster split,
(e) the initial and final clusters Irish words actually bring, (f) Irish-internal epenthesis,
(g) genitive/adjective agreement for epithets — plus Old Irish for strand 5.

Note: the baseline bibliography (`../../chat-imports/phonology_rule_file_sources.md`) has
**no Irish section at all** — it covers only the four target languages plus infrastructure.
Everything below is new, verified 2026-08-24. Section numbers (§1–§8) refer to
`../DIGEST-TEMPLATE.md`.

Access tiers: **OA** = open, no account · **PD** = public domain scan · **free-account** ·
**paywalled**.

---

## Modern Irish — core

### `wiki-irish-phonology`
Wikipedia contributors, "Irish phonology," English Wikipedia (rev. fetched 2026-08-24).
URL: https://en.wikipedia.org/wiki/Irish_phonology
Access: **OA** (CC BY-SA). Status: **confirmed**.
Files: `wiki-irish-phonology.html`, `.txt`, `.wikitext`; plus the three cluster charts below.
Covers: §1 the complete consonant inventory with every broad/slender pair
(/pˠ pʲ bˠ bʲ mˠ mʲ fˠ fʲ vˠ vʲ t̪ˠ tʲ d̪ˠ dʲ n̪ˠ nʲ l̪ˠ lʲ ɾˠ ɾʲ sˠ ʃ k c ɡ ɟ x ç ɣ j ŋ ɲ h/),
vowels and the diphthongs /iə uə əi əu/, length; §2 the fullest free statement of Irish
phonotactics anywhere — licit initial CC and CCC (obstruent+liquid/nasal, /sˠ ʃ/+stop,
/sˠ ʃ/+stop+liquid), the quality-agreement rule and its exceptions (broad /sˠ/ before slender
labials; broad /ɾˠ/ before slender coronals), the much larger mutation-environment onset set
(/wl̪ˠ vʲɾʲ çlʲ xɾˠ jɾʲ hlʲ mˠl̪ˠ n̪ˠɾˠ ɲlʲ …/), the Connacht/Ulster /Cn/→/Cɾ/ rule, and the
post-vocalic-cluster epenthesis rule with its blocking conditions (long vowel/diphthong
before, ≥3 syllables, following voiceless stop) — *gorm* /ˈɡɔɾˠəmˠ/ is the worked example
there; §4 stress (initial in Connacht/Ulster, weight-sensitive in Munster).
Caveat for the digest: the cluster material is sourced to **Ní Chiosáin 1999** (paywalled,
see below), so Wikipedia is our only route to it.

### `wiki-clusterchart-*` (3 files)
Wikimedia Commons SVGs embedded in the above: `2C_cluster_nonmut.svg` (licit 2-consonant
onsets, non-mutation), `2C_cluster_mut2.svg` (2-consonant onsets in mutation environments),
`Epenthesis_cluster.svg` (which C1–C2 combinations trigger epenthesis).
Access: **OA** (Commons). Status: **confirmed**. Files: `wiki-clusterchart-<name>.svg`.
These are the explicit cluster grids the brief asked for — SVG so the labels are extractable
as text.

### `wiki-irish-orthography`
Wikipedia contributors, "Irish orthography." https://en.wikipedia.org/wiki/Irish_orthography
Access: **OA**. Status: **confirmed**. Files: `wiki-irish-orthography.html`, `.txt`, `.wikitext`.
Covers: §5 spelling↔sound for the source side — how broad/slender is written (flanking vowel
letters), the síneadh fada, the vowel-digraph inventory, and the mutation spellings
(⟨bh ch dh fh gh mh ph sh th⟩, ⟨mb gc nd bhf ng bp dt⟩). Needed to read Irish input forms and
to sanity-check hand IPA.

### `wiki-irish-mutations`
Wikipedia contributors, "Irish initial mutations."
https://en.wikipedia.org/wiki/Irish_initial_mutations
Access: **OA**. Status: **confirmed**. Files: `.html`, `.txt`, `.wikitext`.
Covers: §6/§8 lenition and eclipsis stated as phoneme→phoneme maps —
lenition /pˠ→fˠ, bˠ→wˠ~vˠ, mˠ→wˠ~vˠ, t̪ˠ→h, d̪ˠ→ɣ, sˠ→h, fˠ→∅, k→x, ɡ→ɣ/ (and slender
counterparts /pʲ→fʲ, bʲ mʲ→vʲ, tʲ→h, dʲ→j, ʃ→h, c→ç, ɟ→j/); eclipsis
/pˠ→bˠ, t̪ˠ→d̪ˠ, k→ɡ, bˠ→mˠ, d̪ˠ→n̪ˠ, ɡ→ŋ, fˠ→wˠ/; plus the grammatical triggers, which is
what epithet formation needs.

### `wiki-help-ipa-irish`
Wikipedia, "Help:IPA/Irish." https://en.wikipedia.org/wiki/Help:IPA/Irish
Access: **OA**. Status: **confirmed**. Files: `.html`, `.txt`, `.wikitext`.
Covers: §1/§5 a one-page IPA↔spelling key with an example word per symbol. Fast lookup table
for hand-transcribing input names; redundant with the two above but much shorter.

### `nichasaide1999-ipa-irish`
Ní Chasaide, Ailbhe (1999). "Irish." In *Handbook of the International Phonetic Association:
A Guide to the Use of the International Phonetic Alphabet*, pp. 111–116. Cambridge: CUP.
URL: https://archive.org/details/rosettaproject_gle_phon-1
Access: **OA** (freely downloadable, no account; hosted by the Long Now Rosetta Project —
underlying copyright is CUP's, so treat as free-to-read rather than licensed-open).
Status: **confirmed, but the baseline description was wrong** — this is the *Handbook*
illustration, **not** a JIPA 29(1) article. Cambridge Core has no open JIPA "Irish"
illustration; the Handbook chapter is paywalled on Cambridge Core and open only via this scan.
Files: `nichasaide1999-ipa-irish.pdf`, `.txt`.
Covers: §1 the authoritative consonant table laid out as velarized/palatalized pairs, vowel
chart, §4 stress note, §5 an orthographic + phonetic "North Wind and the Sun." Dialect base is
**Ulster (Gaoth Dobhair, Donegal)** — note that when it conflicts with Connacht-based sources.
OCR quality of the .txt is mediocre for the IPA (e.g. superscripts rendered as `Y`/`J`); use
the PDF for the tables.

### `nichiosain2018-ultrasound-connemara`
Ní Chiosáin, Máire; Padgett, Jaye; McGuire, Grant; Bennett, Ryan (2018). "An ultrasound study
of Connemara Irish palatalization and velarization." *Journal of the International Phonetic
Association* 48(3): 261–304. doi:10.1017/S0025100317000494.
URL (author copy): https://people.ucsc.edu/~rbennett/papers.html
Access: **OA** author preprint on the UCSC faculty page (journal version paywalled).
Status: **confirmed**. Files: `.pdf`, `.txt`.
Covers: §1/§8 — the single most important source for what "broad" and "slender" actually *are*
articulatorily (velarized vs. palatalized tongue-body gestures, place-by-place, Connemara
speakers). This is the evidence base for deciding, per target language, whether broad/slender
collapses to plain, to Cʲ/Cˠ sequences, or to a marked series (e.g. Arabic emphatics).

### `bennett-syllable-position-irish`
Padgett, Ní Chiosáin, McGuire, Bellik & Bennett (2024). "Effects of syllable position and place
of articulation on secondary dorsal contrasts: an ultrasound study of Irish." *Journal of
Phonetics* 107: 101368. Access: **OA** author preprint (UCSC). Status: **confirmed**.
Files: `.pdf`, `.txt`.
Covers: §8 — the broad/slender contrast is realized **less robustly in codas than in onsets**.
Directly relevant if we decide to neutralize quality in coda position when adapting.

### `bennett-gestural-timing-irish`
Padgett, McGuire, Ní Chiosáin, Bellik & Bennett (2025). "Gestural timing and contrast: an Irish
case study." In Carnie et al. (eds.), *Foundational Approaches to Celtic Linguistics*, 283–341.
Berlin: Language Science Press. doi:10.5281/zenodo.15532992.
Access: **OA** (CC BY, Language Science Press / Zenodo). Status: **confirmed**.
Files: `.pdf`, `.txt`.
Covers: §1/§8 timing of the secondary articulation relative to the primary — background for
whether Cʲ is better modelled as a unit segment or as C+j when exported to a target language.

---

## Stress, syllabification, epenthesis

### `green1997-prosodic-goidelic`
Green, Antony Dubach (1997). *The Prosodic Structure of Irish, Scots Gaelic, and Manx.*
Ph.D. dissertation, Cornell University. ROA-196.
URL: https://roa.rutgers.edu/files/196-0597/196-0597-GREEN-0-0.PDF
(same file mirrored at https://rucore.libraries.rutgers.edu/rutgers-lib/38484/)
Access: **OA** (Rutgers Optimality Archive). Status: **confirmed** — the PDF is only 10 physical
sheets but is the *complete* dissertation typeset many-logical-pages-per-sheet (~547 KB of
extracted text, ending in the full bibliography).
Files: `.pdf`, `.txt`.
Covers: §2 and §4, the backbone source here. Stress in all three dialect groups, the Munster
"forward stress" pattern and its conditions, weight (only long vowels and diphthongs are heavy;
coda consonants are not), syllabification of consonants and clusters, ambisyllabicity after
stressed short vowels, sonority conditions on rising-sonority clusters, and epenthesis into
falling-sonority clusters (93 mentions of epenthesis, 45 of syllabification, 131 of Munster).
Framing is OT + prosodic hierarchy ("the colon"); per project policy, take the data and the
descriptive generalizations only.

### `green-munster-stress`
Green, Antony Dubach (1996). "Stress Placement in Munster Irish." ROA-120.
URL: https://roa.rutgers.edu/files/120-0496/120-0496-GREEN-0-0.PDF
Access: **OA**. Status: **confirmed** (marked "work in progress" by the author).
Files: `.pdf`, `.txt`.
Covers: §4 — the Munster stress rule in isolation, with the dialect contrast stated plainly:
Connacht and Ulster have initial stress on almost all words; Munster attracts stress to heavy
syllables (long vowel or diphthong; *not* CVC). Shorter and more usable than the dissertation
if all we need is the rule.

### `rowicka-munster-stress`
Rowicka, Grażyna. "2+2=3: Stress in Munster Irish." To appear in Kardela & Szymanek (eds.),
*Festschrift for Prof. E. Gussmann*, Lublin: KUL. ROA-116.
URL: https://roa.rutgers.edu/files/116-0000/116-0000-ROWICKA-0-0.PDF
Access: **OA**. Status: **confirmed**. Files: `.pdf`, `.txt`.
Covers: §4 — a second, independent statement of the Munster facts (Government Phonology rather
than OT). Useful as a cross-check on Green; keep both where they disagree.

### `kukhto2019-munster-stress`
Kukhto, Anton (2019). "Exceptional stress and reduced vowels in Munster Irish."
*Proceedings of ICPhS 2019*, paper 1614. Access: **OA** (IPA proceedings site).
Status: **confirmed**. Files: `.pdf`, `.txt`.
Covers: §4 — the exceptions to the Munster rule (the /ax/ ~ "-ach attracts stress" pattern;
reduced vowels). Relevant because Irish epithets in *-ach* (e.g. *Matánach*) are exactly the
class this paper is about.

### `irish-schwa-kwpl`
McCullough, Kerry (2017). "The value of Irish schwa: An acoustic analysis of epenthetic vowels."
*Kansas Working Papers in Linguistics* 38: 1–11.
URL: https://journals.ku.edu/kwpl/article/view/17198
Access: **OA** (CC BY 4.0). Status: **confirmed**. Files: `.pdf`, `.txt`.
Covers: §2/§3 — Irish-internal epenthesis measured across all three dialects (3 Cork, 2 Donegal,
1 Connemara speakers), with a 30-word near-minimal-pair list (*anam* vs *ainm* type). Confirms
the epenthetic vowel is a real schwa but durationally distinct from underlying schwa. The word
list is a usable seed for the Irish side of the test suite.

### `quiggin1906-donegal`
Quiggin, E. C. (1906). *A Dialect of Donegal: Being the Speech of Meenawannia in the Parish of
Glenties. Phonology and Texts.* Cambridge: CUP.
URL: https://archive.org/details/dialectofdonegal00quig
Access: **PD** (archive.org, NOT_IN_COPYRIGHT). Status: **confirmed**. Files: `.pdf` (15.9 MB),
`.txt` (OCR).
Covers: §1/§2/§4 — a full pre-standard phonetic description of one Ulster dialect: segment
inventory with broad/slender throughout, cluster behaviour, epenthesis, stress, plus texts.
Uses a 1906 phonetic notation, not IPA, so it needs transcription-key work before use; value is
as an independent check on the Wikipedia/Ní Chasaide picture and as a source of dialect detail
nothing else open supplies.

---

## Morphology for epithets

### `wiki-irish-grammar`, `wiki-irish-declension`
Wikipedia contributors, "Irish grammar" (https://en.wikipedia.org/wiki/Irish_grammar) and
"Irish declension" (https://en.wikipedia.org/wiki/Irish_declension).
Access: **OA**. Status: **confirmed**. Files: `wiki-irish-grammar.{html,txt,wikitext}`,
`wiki-irish-declension.{html,txt,wikitext}`.
Covers: §6 — the five noun declensions and their genitive-singular formations (slenderization,
*-a*, *-e*, *-each/-igh*, broadening), adjective agreement (gender/number/case, initial mutation
of the adjective after a feminine noun, plural *-a/-e*), and the article's mutation effects.
This is the machinery behind epithets of the *Lasairchos* / *X na Y* type. Note "Irish
morphology" is a redirect to "Irish grammar," not a separate article.

### `wiki-irish-name`
Wikipedia contributors, "Irish name." https://en.wikipedia.org/wiki/Irish_name
Access: **OA**. Status: **confirmed**. Files: `.html`, `.txt`, `.wikitext`.
Covers: §6 — naming patterns proper: *Mac/Ó/Ní/Nic/Uí/Mhic* and the mutations each triggers,
feminine forms, epithets and bynames. Directly the shape the generator's output has to take.

---

## Old Irish (strand 5)

### `wiki-old-irish`
Wikipedia contributors, "Old Irish." https://en.wikipedia.org/wiki/Old_Irish
Access: **OA**. Status: **confirmed**. Files: `.html`, `.txt`, `.wikitext`.
Covers: §1 consonant inventory (the three-way lenited/unlenited and broad/slender interaction),
vowels, §4 stress ("generally the first syllable; in verbs the second when the first is a
clitic prefix, marked with ·"), §5 orthography with the letter↔sound conventions, and the
initial mutations. This is the fastest route to reading and producing Old Irish name forms.

### `wiki-old-irish-grammar`
Wikipedia contributors, "Old Irish grammar." https://en.wikipedia.org/wiki/Old_Irish_grammar
Access: **OA**. Status: **confirmed**. Files: `.html`, `.txt`, `.wikitext` (the largest of the
Wikipedia items, ~95 KB text).
Covers: §6 — noun declensions (o-, ā-, i-, u-, consonant stems), adjective classes and
agreement, article, so that Old Irish epithets can be inflected rather than guessed.

### `wiki-old-irish-phonhistory`
Wikipedia contributors, "Phonological history of Old Irish."
https://en.wikipedia.org/wiki/Phonological_history_of_Old_Irish
Access: **OA**. Status: **confirmed**. Files: `.html`, `.txt`, `.wikitext`.
Covers: §1/§5 — how the Old Irish system arose and, more usefully here, the systematic
correspondences between Old Irish and Modern Irish forms. That correspondence set is what lets
strand 5 be generated from the same Irish lexicon as the other four.

### `pokorny1914-oldirish-grammar`
Pokorny, Julius (1914). *A Concise Old Irish Grammar and Reader. Part I: Grammar.*
Halle: Niemeyer / Dublin: Hodges, Figgis.
URL: https://archive.org/details/conciseoldirishg01pokouoft
Access: **PD** (archive.org, NOT_IN_COPYRIGHT). Status: **confirmed**. Files: `.pdf` (8 MB),
`.txt` (OCR).
Covers: §1/§4/§5 — a full Phonology part (pp. ~5–25 in the scan) with orthography-to-sound
rules, lenition/aspiration and nasalization, the accent and its behaviour in stressed, enclitic
and proclitic syllables, plus the declensions. The legitimately open substitute for Thurneysen.
OCR is imperfect on diacritics; use the PDF for anything delicate.

### `strachan1909-oldirish-paradigms`
Strachan, John. *Old-Irish Paradigms and Selections from the Old-Irish Glosses.* 3rd edn.,
revised by Osborn Bergin. Dublin: Royal Irish Academy / Hodges, Figgis.
URL: https://archive.org/details/oldirishparadigm00stra
Access: **PD** (archive.org, NOT_IN_COPYRIGHT). Status: **confirmed**. Files: `.pdf` (6.5 MB),
`.txt` (OCR).
Covers: §6 — the paradigm tables in compact form (nouns by stem class, adjectives, pronouns,
verbs), plus a vocabulary. Complements Pokorny: Pokorny for the phonology, Strachan for the
endings.

### `utaustin-oldirish-intro`, `utaustin-oldirish-lesson1`
de Bernardo Stempel, Patrizia & Esser, Caren. *Old Irish Online.* Linguistics Research Center,
University of Texas at Austin. URLs: https://lrc.la.utexas.edu/eieol/iriol/00 and
https://lrc.la.utexas.edu/eieol/iriol/10
Access: **OA**. Status: **confirmed**. Files: `.html`, `.txt` each.
Covers: §5 — Lesson 1 contains a section titled "Phonological System and its Orthographical
Representations," a modern, compact statement of how Old Irish spelling maps to sound
(including the manuscript inconsistencies). The Series Introduction gives the Celtic/Goidelic
background. Good as the readable orientation before the 1914 grammars.

### `edil` — reference only, nothing downloaded
*electronic Dictionary of the Irish Language* (eDIL 2019), based on the RIA *Dictionary of the
Irish Language* (1913–76). URL: https://dil.ie/ ; search endpoint https://dil.ie/search ;
individual headwords resolve as `https://dil.ie/<numeric-id>`.
Access: **OA** (free to use, no account). Status: **confirmed as a website; no bulk download or
documented public API found** — the QUB/Ulster project pages advertise the web interface only.
Covers: vocabulary for Old/Middle Irish name and epithet coinage. Query it per word during
generation rather than digesting it.

---

## Marginal / low value

### `ocuinneagain-thesis-irishenglish`
Ó Cuinneagáin (2019). "Irish Phonological Features in Irish English." MA dissertation,
University of Sheffield (White Rose eTheses 27111).
URL: https://etheses.whiterose.ac.uk/id/eprint/27111/1/OCuinneagain_109031243_Thesis.pdf
Access: **OA**. Status: **confirmed, but misjudged on the way in** — it is a sociolinguistic
study of a small set of Irish-English focus variables, not a description of Irish phonology.
Files: `.pdf`, `.txt`. Keep only if a substrate-transfer example is wanted; contributes nothing
to §1–§4.

---

## Not used (paywalled or restricted)

- **Ní Chiosáin, Máire (1999). "Syllables and phonotactics in Irish." In van der Hulst & Ritter
  (eds.), *The Syllable: Views and Facts*, 551–75. Berlin: Mouton de Gruyter.** Paywalled.
  **This is the biggest single loss.** It is the source Wikipedia's entire cluster inventory is
  built on; without it we have the lists but not their conditions, exceptions, or the author's
  own statement of what is excluded.
- **Ó Siadhail, Mícheál (1989). *Modern Irish: Grammatical Structure and Dialectal Variation.*
  CUP.** Paywalled; no legitimately open chapter found. Loss: the systematic three-dialect
  comparison, and the *Learning Irish* appendices are likewise closed.
- **Thurneysen, Rudolf (1946). *A Grammar of Old Irish.* Dublin: DIAS.** In copyright (DIAS
  still sells it). A scan exists at https://archive.org/details/thurneysen-a-grammar-of-old-irish
  but it sits in archive.org's user-uploaded `opensource`/`community` collection with no rights
  statement — **deliberately not downloaded** per the acquisition brief. Loss: the standard
  reference; Pokorny 1914 + Strachan + the Wikipedia articles cover our needs (inventory,
  orthography, stress, declension) at lower resolution.
- **Stifter, David (2006). *Sengoídelc: Old Irish for Beginners.* Syracuse UP.** Purchasable only.
- **McCone, Kim (1996). *Towards a Relative Chronology of Ancient and Medieval Celtic Sound
  Change.* Maynooth.** Purchasable; his *A First Old Irish Grammar and Reader* likewise. No open
  copy found.
- **Ó Cuív, Brian (1944). *The Irish of West Muskerry, Co. Cork*; de Bhaldraithe, Tomás (1945).
  *The Irish of Cois Fhairrge*; Breatnach, R. (1947). *The Irish of Ring.*** All DIAS, all still
  in print and for sale; no open scans. Loss: the only book-length phonetic descriptions of the
  Munster and Connacht dialects. Quiggin 1906 (PD) gives us the Ulster equivalent only.
- **Ó Sé, Diarmuid (2000). *Gaeilge Chorca Dhuibhne.*** ITÉ; not open. Loss: the fullest modern
  Munster description, incl. stress detail.
- **"Acquisition of Irish Phonology," ch. 5 of *The Acquisition of Celtic Languages* (CUP,
  2025).** Paywalled; described as outlining the full range of possible Irish clusters — would
  have been a second independent cluster list.
- **Wagner, Heinrich (1958–69). *Linguistic Atlas and Survey of Irish Dialects.* 4 vols. DIAS.**
  Not open. Loss: dialect-by-dialect segment maps.

---

## Verification notes

- Baseline error corrected: **Ní Chasaide 1999 is a chapter in the IPA *Handbook*, not an
  article in *JIPA* 29(1).** Cambridge Core has no open Irish Illustration; the only free copy
  is the Rosetta Project scan listed above.
- The abair.ie / TCD Phonetics and Speech Lab publication list was checked
  (https://www.abair.tcd.ie/publications): its open output is speech-technology work (TTS, ASR,
  dialect ID) rather than descriptive phonology, and the phonology-adjacent items are on
  ResearchGate behind a login. Nothing acquired from it.
- The Ulster University rhotics paper (`.../942502/0716.pdf`, "The Phonetics and Phonology of
  Rhotics in Modern Irish") is blocked by Cloudflare on direct fetch; not acquired.
  URL: https://www.ulster.ac.uk/__data/assets/pdf_file/0004/942502/0716.pdf — worth a retry from
  a browser if /ɾˠ/ vs /ɾʲ/ detail is needed.
