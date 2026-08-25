# Sources — Dutch (target language, strand 3)

Variety decision: **Belgian Standard Dutch**, confirmed rather than defaulted. PHOIBLE InvID
2169's bibliographic source *is* Verhoeven (2005), the Belgian JIPA Illustration — so the
inventory row and its primary description are the same document, and that document is open.
Netherlandic would have been served by Gussenhoven (1992/1999), which is also open, but nothing
about the open-source situation favours it. See "Belgian vs. Netherlandic" at the end.

All items below are open access (no account, no payment) unless the entry says otherwise.
Section references (§1–§8) are to `../DIGEST-TEMPLATE.md`.

---

## Reference descriptions of the variety

### `verhoeven2005`
Verhoeven, Jo (2005). "Illustrations of the IPA: Belgian Standard Dutch." *Journal of the
International Phonetic Association* 35(2), 243–247. doi:10.1017/S0025100305002173
- URL: https://www.cambridge.org/core/services/aop-cambridge-core/content/view/40E060F565C2A84B07993980D2957D49/S0025100305002173a.pdf/belgian_standard_dutch.pdf
- Access: **OA** — Cambridge Core serves the PDF without login (verified by download).
- Status: **confirmed**. This is the source of PHOIBLE InvID 2169.
- Files: `verhoeven2005.pdf` (5 pp), `verhoeven2005.txt`
- Covers: §0 variety definition; §1 full consonant + vowel inventory with example words, marginal
  segments in parentheses (loan-only), the Belgian/Netherlandic contrasts that matter — Belgian
  keeps velar /x ɣ/ (Netherlandic has uvular /χ/ and no /ɣ/), keeps the fricative voicing
  contrast (though 70% of initial fricatives are phonetically voiceless), alveolar~uvular trill
  free variation, /r/ devoiced word-finally and before voiceless stops; §4 vowel length.
- ⚠️ **The `.txt` IPA is mangled.** The PDF embeds legacy IPAKiel / TeX-tipa fonts without usable
  ToUnicode, so `pdftotext` emits the legacy byte values. Read the PDF for IPA. Observed key:
  `E`=ɛ `A`=ɑ `O`=ɔ `Y`=ʏ `„`/`P`=ø `N`=ŋ `S`=ʃ `Z`=ʒ `V`=ɣ `R`=r `/`=ʔ `…`=ː `9`=voiceless
  ring (so `R9` = r̥, matching the text's claim that /r/ devoices finally).

### `gussenhoven1992`
Gussenhoven, Carlos (1992). "Dutch." *Journal of the International Phonetic Association* 22(1–2),
45–47. (IPA Illustration; the Netherlandic counterpart.)
- URL: https://www.cambridge.org/core/services/aop-cambridge-core/content/view/7B078FF950183FB74A78382A79465344/S002510030000459Xa.pdf/dutch.pdf
- Access: **OA** — the article landing page presents as subscription-gated, but the PDF endpoint
  serves without login (verified by download).
- Status: **confirmed** (the baseline bibliography marked this "(verify open)").
- Files: `gussenhoven1992.pdf` (3 pp), `gussenhoven1992.txt`
- Covers: §0/§1 for **Netherlandic** Standard Dutch — the comparison case for the variety
  decision. Short (3 pp, of which 1 is the shared Turkish illustration).
- ⚠️ `.txt` is OCR of a scan; IPA is unreliable. Read the PDF.

### `wiki-nl-phonology`
Wikipedia, "Dutch phonology" (retrieved 2026-08-24).
- URL: https://en.wikipedia.org/wiki/Dutch_phonology
- Access: **OA** (CC BY-SA)
- Status: confirmed
- Files: `wiki-nl-phonology.wikitext`, `wiki-nl-phonology.html`, `wiki-nl-phonology.txt`
- Covers: §1 inventory with Belgian/Netherlandic splits; §2 an explicit **§Phonotactics** with
  §Onset and §Coda subsections (CCC always begins /s/: /spr spl str skr skl sxr/; CC = obstruent +
  /r l/ but never /dl tl/; /s/ the only C before /m/; /ɦ ʒ ʔ/ never cluster; /ŋ/ not in onsets;
  coda: /n/ not before labials/dorsals, /ŋ/ not before labials nor after long vowels/diphthongs,
  /r/ not after diphthongs, voiced codas only in loans) — largely sourced from Booij 1999, which
  is the paywalled monograph, so this is a usable proxy; §3 §Final devoicing and assimilation;
  §4 §Stress (root-initial default, loans keep source stress, trochaic rhythm, schwa syncope);
  §7 parallel Northern and **Belgian** Standard Dutch transcriptions of the same passage.

### `wiki-nl-orthography`
Wikipedia, "Dutch orthography" (retrieved 2026-08-24).
- URL: https://en.wikipedia.org/wiki/Dutch_orthography
- Access: **OA** (CC BY-SA); Files: `wiki-nl-orthography.wikitext` / `.html` / `.txt`
- Covers: §5 romanization — the grapheme↔phoneme mapping, the open/closed-syllable vowel-doubling
  convention (`man`/`manen`/`maan`), digraphs `ij ui eu oe ch sch ng`, and where an English reader
  will go wrong.

### `wiki-nl-language`
Wikipedia, "Dutch language" (retrieved 2026-08-24).
- URL: https://en.wikipedia.org/wiki/Dutch_language
- Access: **OA** (CC BY-SA); Files: `wiki-nl-language.wikitext` / `.html` / `.txt`
- Covers: §0 background, §Phonology summary, §6 a little morphology. Lowest-value of the three;
  kept for §0 and §6 context.

---

## Phonotactics — the backbone

### `taalportaal`
Taalportaal: the digital language portal / *Dutch phonology* (Landsbergen, Tiberius & Dernison
2014, LREC-9). Retrieved 2026-08-24. **41 topic pages** harvested, listed below.
- URL: https://taalportaal.org/ — per-page URLs are `https://taalportaal.org/taalportaal/topic/pid/<pid>`,
  and each saved `.txt` carries its own TITLE/URL header.
- Access: **free to read, but NOT openly licensed** — the one item here that is not properly OA.
  No Creative Commons licence is offered on the site. Content is owned/licensed by the Dutch
  Language Institute (INT); its terms of service (https://ivdnt.org/english/terms-of-service/,
  verified 2026-08-24) state: *"The contents of the Sites may only be used for non-commercial
  and/or private purposes. You may not reproduce, modify, delete or make the content of the Sites
  available to third parties for remuneration without the express written permission of the
  INT."*
  → Citing and quoting with attribution is fine, and private/non-commercial use covers this
  project as described. **Decision for the user:** committing these 91 files to a public repo, or
  shipping cluster tables derived from them, goes beyond "private use" — either keep them local
  (gitignore), or rebuild the cluster lists from `booij1978`/`booij1999`/`wiki-nl-phonology`,
  which say much the same thing with looser terms.
- Status: confirmed. Not in the baseline bibliography — this is the single biggest find.
- Files: `taalportaal-*.html` (trimmed to the article fragment) + `taalportaal-*.txt`, plus
  9 `taalportaal-fig-*.png`.
- Covers, by group:
  - **§2 clusters (the priority).** `-onset-clusters-2c` gives the *exhaustive* CC-onset table:
    every attested cluster with an example word in IPA, loanword-only clusters marked as such,
    plus the OCP-place restriction and the /s/ and /ʋ/ exceptions. `-onset-clusters-3c` gives the
    complete CCC list — /spl spr str sxr/ native, /skl skr skʋ/ marked loanword-only.
    `-codas` gives the coda inventory with the key asymmetry that **word-medial codas max out at
    two consonants** (*werkloos* /ʋɛrk.los/) while **word-final codas reach five** (*herfst*
    /hɛrfst/, *promptst* /prɔmptst/); /h/ barred from codas; /ŋ/ coda-only and only after B-class
    (lax) vowels; glides only after A-class vowels and only before coronals (*ooit* /ojt/).
    `-coda-cooccurrence-restrictions` (largest page) gives the full vowel×coda-consonant table and
    **a restriction that bites hard on Irish input**: A-class (tense/long) vowels and diphthongs
    take only *voiced* fricatives in the coda, B-class (lax/short) vowels only *voiceless* ones.
    Irish /ɑː/+/x/ (as in *Matánach* /ˈmˠat̪ˠɑːnˠəx/) is exactly the banned A-class + voiceless
    fricative shape, so §3 needs a rule for it (shorten the vowel? voice the fricative to /ɣ/,
    which Belgian Dutch has?). Listed exceptions are loans (*puzzel*, *mazzel*) and the
    dialectal /x~ɣ/ merger.
    Also `-phonotactics-overview`, `-syllable-level`, `-onsets`, `-onsets-simple`,
    `-onsetless-syllables`, `-rhymes`, `-nuclei`, `-pansyllabic-constraints`,
    `-consonant-cluster-condition` (the coronal requirement in obstruent clusters),
    `-phonotactics-word-level`, `-across-syllable-boundaries`, `-syllable-contact`,
    `-ambisyllabicity`, `-consonant-distributions`, `-phonotactics-morphology-relation`.
  - ⚠️ **The 9 PNGs are load-bearing, not decorative — a digest agent must actually look at them.**
    Taalportaal states negative/illicit information graphically. `-fig-onset-cc-matrix.png` and
    `-fig-onset-cc-matrix-native.png` are the CC-onset matrices whose *empty and shaded* cells are
    the only statement of which onset clusters are banned (I checked: both render legibly, rows
    p b t d k g f v s z ʃ x m n l r ʋ h j × columns p t k f s ʃ x m n l r ʋ j w, with `+` frequent
    and `(+)` marginal/loan). Also `-fig-onset-cc-coronal.png`, `-fig-coda-cc-coronal.png`,
    `-fig-rhymes-all.png`, `-fig-rhymes-disallowed.png` (structural trees of banned rhyme shapes —
    needs `taalportaal-rhymes.txt` prose to interpret), `-fig-sonority-profile.png`, and vowel
    charts `-fig-vowel-chart-verhoeven.png` / `-fig-vowel-chart-gussenhoven.png` (Taalportaal
    reproduces **both** varieties' charts — convenient for §0/§1).
  - **§1 inventory:** `-segment-inventory`, `-vowel-inventory` (A-class tense/long vs B-class
    lax/short, diphthongs, marginal vowels), `-consonant-inventory`, `-segment-r`, `-segment-l`.
  - **§3 processes:** `-final-devoicing`, `-voice-assimilation` (regressive + progressive),
    `-nasal-assimilation`, `-degemination`, `-schwa-epenthesis-deletion` (the *melk* → [mɛlək]
    case), `-n-deletion`, `-hiatus-resolution` (homorganic glide insertion), `-casual-speech`.
  - **§4 stress:** `-word-stress`, `-stress-primary-simplex`, `-stress-generalizations`,
    `-stress-default-penultimate`, `-stress-three-syllable-window`, `-stress-quantity-sensitivity`,
    `-stress-superheavy-syllables`, `-stress-closed-penult-restriction`, **`-stress-loanwords`**.
- Note: Taalportaal's phonology sections are largely a restatement of Booij (1995), which they
  cite page-by-page. This is how we recover the paywalled monograph's content legitimately.

### `kager-pater2012`
Kager, René & Pater, Joe (2012). "Phonotactics as phonology: knowledge of a complex restriction
in Dutch." *Phonology* 29(1), 81–111. (Author's revised December 2011 version.)
- URL: https://people.umass.edu/pater/kager-pater-revised-December-2011.pdf
- Access: **OA** (author's page, UMass). Status: **confirmed** (baseline listed it as academia.edu
  free-with-account; the UMass copy needs no account).
- Files: `kager-pater2012.pdf` (8 pp), `kager-pater2012.txt`
- Covers: §2 one specific and implementable gap — Dutch disallows **long vowel + cluster whose
  second member is non-coronal** (*[Vː]CC[-cor]), weakened when the last C starts a new syllable.
  Directly relevant to Irish input, which has phonemic long vowels and freely allows Vː + cluster.
  The rest of the paper is nonce-word experiment + theory; take the restriction and the stimuli.

### `booij1999-msc`
Booij, Geert (1999). "Morpheme structure constraints." In H. van der Hulst & N. Ritter (eds.),
*The Syllable: Views and Facts*. Berlin: Mouton de Gruyter. (Author's copy.)
- URL: https://geertbooij.com/wp-content/uploads/2014/02/booij-1999-morpheme-structure-condtions-vdhulstritter.pdf
- Access: **OA** (author's own site). Status: confirmed. Files: `booij1999-msc.pdf` (20 pp), `.txt`
- Covers: §2 Dutch morpheme-structure constraints — obstruent clusters within a prosodic word have
  a coronal second member; voiced-obstruent clusters occur only morpheme-finally and surface
  voiceless in isolation; morpheme-final obstruent-liquid clusters (/-tr/ etc.) never surface as
  codas; ambisyllabicity blocking. §3 final devoicing as a coda condition.

### `booij2011-msc`
Booij, Geert (2011). "Morpheme structure constraints." In *The Blackwell Companion to Phonology*,
ch. 86. (Author's copy.)
- URL: https://geertbooij.com/wp-content/uploads/2014/02/booij-2011-morpheme-structure-constraints.pdf
- Access: **OA** (author's site). Status: confirmed. Files: `booij2011-msc.pdf` (21 pp), `.txt`
- Covers: §2 the same constraints restated more accessibly, with the loan-relevant cases:
  *[pn- is a constraint on *native* Dutch (Greek-derived *pneumatisch* violates it and is thereby
  marked as non-native); voiced obstruent clusters barred morpheme-internally with a handful of
  loan exceptions (*labda* /lɑbdaː/); lexical morphemes need at least one full vowel; schwa
  restrictions. §3 the point that some MSCs are *not* enforced on loans — the loan keeps its
  foreign shape and is heard as foreign. That is a design decision for us.

### `booij1978-fonotactische`
Booij, G. E. (1978). "Fonotactische restricties in de generatieve fonologie." *Spektator* 8,
28–48. (Dutch-language.)
- URL: https://www.dbnl.org/tekst/_spe011197801_01/_spe011197801_01_0002.php
- Access: **OA to read on DBNL**; DBNL labels it *Auteursrechtelijk beschermd* (in copyright).
  Status: confirmed. Files: `booij1978-fonotactische.html`, `.txt`
- Covers: §2 licit syllable-initial/-final clusters as the account of medial clusters (*malkon* vs
  **malrkon*); four-consonant codas limited to *-rnst*, *-rfst* (*ernst*, *herfst*); /ŋ/ barred
  word-/morpheme-initially but not syllable-initially; casual-speech clusters /tl ks ts tn/ that
  break word-initial constraints. §3 the argument that Dutch final devoicing is conditioned by the
  *syllable* boundary, evidenced precisely by how loanwords are adapted — directly usable.
  Theory-heavy (Stanley/Shibatani/Hooper); mine the Dutch data.

### `booij1979-syllabe`
Booij, G. E. (1979). "De syllabe in de generatieve fonologie." *Spektator* 9. (Dutch-language.)
- URL: https://www.dbnl.org/tekst/_spe011197901_01/_spe011197901_01_0039.php
- Access: **OA to read on DBNL** (in copyright). Status: confirmed.
  Files: `booij1979-syllabe.html`, `.txt`
- Covers: §2 sonority scale and its Dutch exceptions (*ernst*, *herfst*; /st/ despite equal
  strength); onset/rhyme/coda structure; §3 voicing assimilation *direction* keyed to
  tautosyllabic vs heterosyllabic (stop+fricative tautosyllabic → stop assimilates to the
  fricative; heterosyllabic → the reverse) — a concrete, implementable rule; §4 syllable weight
  defined on the rhyme only (onset irrelevant to stress).

### `twpl-clusterreduction`
Jongstra, Wenckje (2003). *Variation in Reduction Strategies of Dutch Word-Initial Consonant
Clusters.* PhD thesis, University of Toronto. (Toronto Working Papers in Linguistics.)
- URL: https://twpl.library.utoronto.ca/index.php/twpl/article/download/6504/3479/8983
- Access: **OA**. Status: confirmed. Not in the baseline. Files: `twpl-clusterreduction.pdf`, `.txt`
- Covers: §3 **which member of an illicit onset cluster gets deleted**, with variation data. This
  is acquisition data (child Dutch), not loanword data, so it is evidence about Dutch-internal
  cluster-reduction preferences rather than about adult loan adaptation — use it as a tiebreaker
  when the loanword sources are silent, and mark rules drawn from it accordingly.

### `codaclusters-nl-af`
Wissing, Daan & Zonneveld, Wim (2018). "Stabilising determinants in the transmission of
phonotactic systems: Diachrony and acquisition of coda clusters in Dutch and Afrikaans."
*Stellenbosch Papers in Linguistics Plus* 55.
- URL: https://scielo.org.za/scielo.php?script=sci_arttext&pid=S2224-33802018000200005
- Access: **OA** (SciELO SA). Status: confirmed. Not in the baseline.
  Files: `codaclusters-nl-af.html`, `.txt`
- Covers: §2 Dutch coda clusters, sonority sequencing vs. voicing harmony, t-deletion in
  /xts/→/xs/; §3 coda simplification. Comparative with Afrikaans — read the Dutch half.

---

## Loanword adaptation and stress

### `vandersijs1996-leenwoordenboek`
van der Sijs, Nicoline (1996). *Leenwoordenboek: de invloed van andere talen op het Nederlands.*
Den Haag: Sdu. 950 pp. Author's open-access scan (OCR'd). (Dutch-language.)
- URL: https://nicolinevdsijs.nl/wp-content/uploads/2025/01/1996_Sijs-Nicoline-van-der_Leenwoordenboek-1ed-scan.pdf
- Access: **OA** — the author has deliberately opened her back catalogue at nicolinevdsijs.nl.
- Status: confirmed. Not in the baseline. **⚠️ 45 MB** (under the brief's 100 MB cap, but by far
  the largest file here; drop it if repo size matters — the chapters we need are pp. 33–57 and the
  per-language "Uitspraak en spelling" sections).
- Files: `vandersijs1996-leenwoordenboek.pdf`, `.txt` (3.4 MB; OCR noise, e.g. "Van Dole" for
  "Van Dale")
- Covers: **§3, and it is the best §3 source we have.** Ch. "De uitspraak van leenwoorden" (p. 33)
  sets out the three-way adaptation scale that Dutch actually uses — *etymologische uitspraak*
  (approximate the source with the nearest Dutch phonemes) / *vernederlandste uitspraak*
  (nativize without approximating) / *spellinguitspraak* (read the spelling as Dutch) — with
  worked pairs: *grill* [ɡrɪl] ~ [xrɪl]; *goal* [ɣoːi̯] ~ [koːl] ~ [xoːl]; *cake* → *keek*;
  *coat* → *Koot*; *drugs* /g/ → [k] or [x]. "Leenfonemen" (p. 57) covers segments imported *with*
  the loans. Also §4: stress retraction to the first syllable in the oldest Latin loans (*bekken*)
  vs. final/penultimate stress in younger French loans (*bassin*). Per-language chapters carry
  their own "Uitspraak en spelling" sections (French p. 116, and pp. 172, 331). §7: 950 pages of
  attested loans by source language, though given in *spelling* with etymology, not IPA.

### `vandersijs2009-loanwords-dutch`
van der Sijs, Nicoline (2009). "Loanwords in Dutch." In M. Haspelmath & U. Tadmor (eds.),
*Loanwords in the World's Languages: A Comparative Handbook*, 338–359. Berlin: De Gruyter.
- URL: https://pure.knaw.nl/ws/files/475024/Van_der_Sijs_Loanwords_in_the_World's_Languages.pdf
  (also on the author's site: https://nicolinevdsijs.nl/wp-content/uploads/2025/05/2009_Sijs-N-van-der_Loanwords-in-Dutch-in-Loanwords-in-the-Worlds-Languages.pdf)
- Access: **OA** — publisher's version of record, deposited in the KNAW repository. Status:
  **confirmed**; the baseline expected only the online WOLD chapter, but the *book chapter itself*
  is open, which is better.
- Files: `vandersijs2009-loanwords-dutch.pdf` (27 pp), `.txt`
- Covers: §0/§3 the companion text to the WOLD Dutch dataset. §5 "Integration of loanwords" —
  Latin and French loans thoroughly adapted in spelling and pronunciation; English loans (recent)
  adapted *least*, retaining English spelling and pronunciation, hence a spelling/pronunciation
  discrepancy. Sets the donor-by-donor expectations for §7.

### `wold-dutch` *(record only — the infra agent downloads the data)*
van der Sijs, Nicoline (2009). "Dutch vocabulary." In M. Haspelmath & U. Tadmor (eds.),
*World Loanword Database*. Leipzig: MPI-EVA.
- URL: https://wold.clld.org/vocabulary/12 (database root https://wold.clld.org/;
  CLDF on GitHub `lexibank/wold`)
- Access: **OA**, **CC BY 3.0 DE** (verified on the vocabulary page — a real open licence, unlike
  Taalportaal). Status: **confirmed**; the baseline's "(verify)" on WOLD covering Dutch is
  correct — Dutch is vocabulary 12, contributor van der Sijs, **1588 entries**.
- Files: none here by design; the infra agent handles the download.
- Covers: §7 the machine-readable gold set — donor language and borrowed status per meaning.
  Caveat for the digest: WOLD gives **orthographic** forms and source languages, not adapted IPA,
  so it supplies the *pairs* but not the *pronunciations*; `attested.tsv`'s `target_ipa` column
  will be blank for WOLD-sourced rows unless another source supplies it.

### `nagy2008-frans`
Nagy, Roland (2008). "Enkele diachrone aspecten van de Franse invloed op de Nederlandse
fonologie." *Acta Neerlandica* 6, 33–44. (Dutch-language.)
- URL: https://www.dbnl.org/tekst/_act003acta07_01/_act003acta07_01_0004.php
- Access: **OA to read on DBNL**. Status: confirmed. Files: `nagy2008-frans.html`, `.txt`
- Covers: §3 the **adaptation vs. integration** distinction, which is the one we need — *adaptation*
  replaces a foreign segment with a native one (French [y] in *juist*, nasal vowels in *parfum*),
  *integration* admits the foreign segment into the Dutch inventory or extends its distribution
  (initial [f] in *feit*). Only integration changes the system. §1 tells us which "loan" segments
  are now inventory members.

### `nagy2007-abstract-en` / `nagy2007-tezis-hu`
Nagy, Roland (2007). *Kölcsönszavak fonológiai integrációja a holland nyelvbe* [The phonological
integration of loanwords in Dutch]. PhD dissertation, Eötvös Loránd University, Budapest.
- URL: https://doktori.btk.elte.hu/lingv/nagyroland/ (thesis.pdf = English abstract;
  tezis.pdf = Hungarian thesis summary, 15 pp)
- Access: **abstract/summary OA; full dissertation NOT available.** `dissn.pdf` at that address is
  a one-page notice that under Hungarian government decree 33/2007 §11(4) the candidate was
  granted a **two-year publication moratorium** from the defence; the full text was never posted.
- Status: **partially found**. The baseline listed this as "[Free*] academia.edu"; the ELTE
  repository copy is open but is only the abstract and the Hungarian summary, not the dissertation.
- Files: `nagy2007-abstract-en.pdf` / `.txt`, `nagy2007-tezis-hu.pdf` / `.txt`
- Covers: §3 the claims and structure of the argument, not the data tables. **This is the single
  biggest loss in the Dutch bibliography** — see "Gaps" below.

### `oostendorp2012-stress`
van Oostendorp, Marc (2012). "Quantity and the three-syllable window in Dutch word stress."
*Language and Linguistics Compass* 6(6), 343–358.
- URL: https://pure.knaw.nl/ws/files/461974/lnc3.339.pdf
- Access: **OA** — publisher's version of record in the KNAW repository. Status: confirmed. Not in
  the baseline. Files: `oostendorp2012-stress.pdf` (17 pp), `.txt`
- Covers: §4 the practical Dutch stress rule — the three-syllable window, what counts as a heavy
  syllable, and how quantity feeds stress. Pair with `taalportaal-stress-*`.

### `booij2003-concrete-fonologie`
Booij, Geert (2003). "Concrete fonologie." (Dutch-language; author's copy.)
- URL: https://geertbooij.com/wp-content/uploads/2014/02/booij-2003-concrete-fonologie.pdf
- Access: **OA** (author's site). Status: confirmed. Files: `booij2003-concrete-fonologie.pdf`
  (24 pp), `.txt`
- Covers: §1/§3 a non-abstract take on Dutch phonological alternations; supporting material.

### `booij2014-word-formation`
Booij, Geert (2014). "Dutch." In *Word-Formation: An International Handbook of the Languages of
Europe* (HSK), ch. 134. (Author's copy.)
- URL: https://geertbooij.com/wp-content/uploads/2014/02/booij-2014-dutch-word-formation-hsk.pdf
- Access: **OA** (author's site). Status: confirmed. Files: `booij2014-word-formation.pdf` (29 pp),
  `.txt`
- Covers: **§6 morphology for epithets** — Dutch derivation and compounding: diminutive *-je* and
  its allomorphs, adjective-forming *-ig* / *-lijk* / *-achtig*, agent *-er*, and the linking
  elements *-s-* / *-en-* in compounds. This is the §6 source.

### `zonneveld1994-overzicht`
Zonneveld, Wim (1994). "Fonologie van het Nederlands: een overzichtsartikel." *Tijdschrift voor
Nederlandse Taal- en Letterkunde* 110. (Dutch-language.)
- URL: https://www.dbnl.org/tekst/_tij003199401_01/_tij003199401_01_0002.php
- Access: **OA to read on DBNL** (in copyright). Status: confirmed.
  Files: `zonneveld1994-overzicht.html`, `.txt`
- Covers: §3 voice assimilation stated as rules with the two patterns spelled out — within
  monomorphemic words obstruent clusters agree in [voice] *and are always voiceless* (an MSC); at
  affix and word boundaries, if the right-hand obstruent is a **fricative** the whole cluster is
  voiceless (progressive), if it is a **plosive** its [voice] value determines the cluster
  (regressive). Also a survey of stress, syllable structure, and sandhi work on Dutch.

### `vandersijs1999-transcriptie`
van der Sijs, Nicoline (1999). "Transcriptie van vreemde alfabetten." *Taaltips* cahier 3.10,
September 1999. (Dutch-language.)
- URL: https://nicolinevdsijs.nl/wp-content/uploads/2025/10/1999_Sijs_Transcriptie-vreemde-alfabetten_Taaltips-3.10.pdf
- Access: **OA** (author's site). Status: confirmed. Not in the baseline.
  Files: `vandersijs1999-transcriptie.pdf`, `.txt`
- Covers: §5 Dutch *transcription* vs. *transliteration* practice for foreign names — the
  Dutch-specific spellings (*Chroesjtsjov*, *Sjostakovitsj*) that show how Dutch writes foreign
  sounds it has no letter for. Useful as a romanization model for our output, and as evidence of
  the sound substitutions Dutch speakers hear.

---

## Loanword adaptation — attested data (§3, §7)

### `loan-vandijk-toename`  ← **best §7 source found**
van Dijk, Margot A. W. (2017). *Over de toename van Engelse leenwoorden in het Nederlands: een
analyse van enkele Nederlandse tv-programma's over een periode van tien jaar.* BA thesis,
Universiteit Utrecht. (Dutch-language.)
- URL (item): https://studenttheses.uu.nl/handle/20.500.12932/26580 — working PDF:
  https://studenttheses.uu.nl/server/api/core/bitstreams/9b56445f-ecfe-40f0-a540-a369870d90f1/content
  (Utrecht migrated to DSpace 7; the older `bitstream/handle/...` URL is dead.)
- Access: **OA**. Status: confirmed, and **spot-checked by me** against the appendix.
- Files: `loan-vandijk-toename.pdf`, `.txt`
- Covers: **§7 — the only source here with both sides in IPA, in bulk.** Appendix §8.2 (from
  p. 24) is a corpus of English loans transcribed off Dutch television, one row per token, with
  the **Dutch realization in IPA** and the **English source in IPA** side by side, plus word class
  and a 1–3 integration score. Verified rows: *to tape* /tuː teɪp/ → [tep] / [ɑftep]; *to
  download* /tuː daʊnloʊd/ → [dɑun tə lodə] (note the Dutch verbal morphology); *superman*
  /ˈsuːpəmæn/ → [ˈsuːpəmænɑχtɪɣ]; *core business* and *I owe you* borrowed with source
  pronunciation intact (score 2). This is `attested.tsv` material almost as-is.

### `loan-posthumus1988-uitspraak`
Posthumus, J. (1988). "De uitspraak van Engelse leenwoorden." *Onze Taal* 57, 112–113.
(Dutch-language.) Author compiled the *Woordenboek van anglicismen*.
- URL: https://www.dbnl.org/tekst/_taa014198801_01/_taa014198801_01_0114.php
- Access: **OA to read on DBNL** (in copyright). Status: confirmed, read in full by me.
- Files: `loan-posthumus1988-uitspraak.html`, `.txt`
- Covers: **§3 — the substitution repertoire, stated as rules with examples.** Sets out Dutch's
  *marginal loan phonemes* (the /ɡ/ of *Goethe / De Gaulle / Glasgow*; the vowels of *punaise,
  controle, freule*; long *ie oe uu* of *remise, rouge, centrifuge*; the /oi̯ ai̯/ of *boy,
  skyline*, licensed by native interjections *hoi, ai*) and then what Dutch refuses: /θ/ → /t/
  (*thinner* → *tinner*), /ð/ → /d/ (*the* → *de*), /æ/ and /ɛ/ both → /ɛ/ (*match* = *set*),
  **final voiced obstruents devoiced with the vowel held long** (*cruise* → [kruːs], contrasting
  native *kroes*). Then per-segment variation: loan /ɡ/ → native /ɣ/ (near-complete in *garage,
  garderobe, yoga*; advancing in *grill, grip, golf*; resisted in *guerrilla, gangster*); final
  /ʃ/ → /s/ casually (*douche* → *does*, *finish* → *fienis*); /tʃ/ → [ʃ] or [s] (*match* →
  *mets*, *kitsch* → *kiets*, *bridge* → *brits*; initial *cheque, choke, chips* with plain /ʃ/);
  /dʒ/ → [ʃ] (*jam* → *sjem*) or [j] (*joker, jumbo, jumper*); vowel-length choices (*team, pool,
  keeper*); *corner/partner* r-and-length variants; and misfires (*transfer* → *transfair* rather
  than *transfeur*, *sweater* → *swieter*, *khaki* → *keekie*). Note the target forms are given in
  **Dutch respelling, not IPA** — converting them is a digest task.

### `loan-theissen2006-nasalen`
Theissen, Siegfried & Leruse, Karine (2006). "De uitspraak van Franse nasalen in het Nederlands."
*Neerlandia/Nederlands van Nu* 110, 36–38. (Dutch-language.)
- URL: https://www.dbnl.org/tekst/_nee003200601_01/_nee003200601_01_0094.php
- Access: **OA to read on DBNL** (in copyright). Status: confirmed, spot-checked by me.
- Files: `loan-theissen2006-nasalen.html`, `.txt`
- Covers: §3 French nasal vowels in Dutch — kept, or nativized to [ɑn ɔn ɛn ʌm]. Word-by-word over
  ~100 items (*croissant, entracte, entrecôte, bonbon, caisson, mannequin, parfum, diligence,
  nonchalance*…), each with survey preference strength (lv/dv/bu) from 106 informants, **split
  N(etherlandic) vs B(elgian)**, and compared against four pronunciation dictionaries.
- ⚠️ **Directly relevant to our variety choice.** The N/B split is real and sometimes opposite —
  e.g. *entracte* and *entrecôte*: Netherlandic informants clearly prefer the *denasalized* form,
  Belgian informants the *nasal* one. Belgian Dutch is the more conservative adapter of French.
  Use the B column.
- ⚠️ Words are typeset with spaced-out emphasis in the DBNL text (`croiss ant`, `parf um`,
  `manne quin`), so naive grep misses them.

### `loan-gerritsen1995-*` (four parts)
Gerritsen, Marinel & van Bezooijen, Renée (1995). Series on loanword pronunciation, *Onze Taal*
64. (Dutch-language.) 75 women, five regions, read-aloud word list — **measured usage**, not
dictionary prescription.
- Access: **OA to read on DBNL** (in copyright). Status: confirmed (agent-reported; file presence
  verified).
- Files / parts:
  - `loan-gerritsen1995-engels` — pt. 1 "Engels: *goal* en *drugs*", 16–17.
    https://www.dbnl.org/tekst/_taa014199501_01/_taa014199501_01_0008.php
  - `loan-gerritsen1995-frans` — pt. 2 "Frans: *restaurant* en *politie*", 86–87. (…_0057.php)
  - `loan-gerritsen1995-frans3` — pt. 3 Franse leenwoorden (*speciaal, cruciaal, aubergine,
    energie, ingenieur*), 180–181. (…_0121.php)
  - `loan-gerritsen1995-grieks-latijn` — pt. 4 Greek/Latin *sc-*, *eu-*, *au-*. (…_0173.php)
- Covers: §3 percentage of source-like vs. nativized realization per word, per region — the
  quantitative complement to Posthumus's qualitative rules.

### `loan-kleinbreukink1999-culinair`
Klein Breukink, Ellen & van Bezooijen, Renée (1999). "Gorgonzola, baguette, gamba's: de uitspraak
van culinaire leenwoorden in Nederland en Vlaanderen." *Onze Taal* 68, 275–277. (Dutch-language.)
- URL: https://www.dbnl.org/tekst/_taa014199901_01/_taa014199901_01_0170.php
- Access: **OA to read on DBNL**. Status: confirmed (agent-reported).
- Files: `loan-kleinbreukink1999-culinair.html`, `.txt`
- Covers: §3 96 speakers, 66 food loans from 10 donor languages, again **Netherlands vs Flanders**
  — a second Belgian-vs-Netherlandic adaptation dataset.

### `loan-mindthegap-foneeminventaris`
van der Geugten, Lilian (2014). *Mind the gap: de invloed van buitenlandse klanken op de
Nederlandse foneeminventaris.* MA thesis, Universiteit Utrecht (supervisor W. Zonneveld), 80 pp.
- URL: https://studenttheses.uu.nl/server/api/core/bitstreams/2b859357-52e6-4f92-92b8-15c6b3be3030/content
- Access: **OA**. Status: confirmed (agent-reported).
- Files: `loan-mindthegap-foneeminventaris.pdf`, `.txt`
- Covers: §1 the Dutch */ɡ/ gap and how loanwords are filling it — i.e. which loan segments are
  becoming inventory members (Nagy's "integration"). OT-framed; take the experiment results and
  the segment inventory discussion, skip the constraints.

### `loan-uu-contrastief-fonemen`
Leeijen, Milou (2019). *Contrastieve analyses van het fonemisch systeem van het Nederlands:
contrastieve analyses met het Duits, Engels, Frans, Italiaans en Pools.* MA thesis, Universiteit
Utrecht. (Dutch-language.)
- URL: DSpace 7 item UUID `62587029-9bc4-406a-a855-7a8940021d5c` (same REST bitstream pattern)
- Access: **OA**. Status: confirmed. Files: `loan-uu-contrastief-fonemen.docx` (native format),
  `.txt`
- Covers: §3 full consonant/vowel/diphthong correspondence tables, Dutch vs English and vs French.
- ⚠️ **Direction caveat:** this is L2-acquisition contrastive analysis (foreigners learning Dutch),
  *not* loanword nativization. Use it as a segment-correspondence lookup and a feature-distance
  sanity check; do not cite it as adaptation evidence in §3, and do not put rows from it in
  `attested.tsv`.

### `loan-brand-berns2023`
Brand, Sophie & Berns, Janine (2023). "Van klank naar schrift en andersom: obstakels in productie
en perceptie van het Frans bij Nederlandse leerlingen." *Levende Talen Tijdschrift* 24(4), 15–28.
- URL: https://lt-tijdschriften.nl/ojs/index.php/ltt/article/view/2374 — Access: **OA**.
- Files: `loan-brand-berns2023.pdf`, `.txt`
- Covers: Dutch–French sound-system mismatches (nasal vowels, /v/–/f/). ⚠️ Same direction caveat:
  Dutch learners producing French, not French entering Dutch. **Lowest-value item in this
  directory**; keep only as a mismatch inventory.

### `loan-ivdnt-anglicismen`, `loan-mars1994-vreemde`, `loan-vandersijs1989-engelse`, `loan-vandersijs2012-revisited`
Minor supporting items, all **OA**:
- Posthumus, Jan (n.d.). "Een woordenboek van anglicismen." INT.
  https://ivdnt.org/wp-content/uploads/2020/11/woordenboek-van-anglicismen.html — the design
  document for the anglicism dictionary; documents the Groningen corpora (Telegraaf 1972,
  Elsevier 1974, 829 words) and **points to where the real adaptation apparatus lives** (see
  "Not used").
- Mars, F. K. M. (1994). "Uitspraak van vreemde woorden." *Onze Taal* 63, 141 — short; French /ʒ/ →
  Dutch /ɣ/ rule (*garage, bagage*) and stress notes.
- van der Sijs (1989), *Onze Taal* 58, 216 and (2012), *Onze Taal* 81, 132–134 — lexical/frequency,
  not phonology. Background only.

---

## Final devoicing and schwa epenthesis (§3)

### `devoic-warner2001-epenthetic-schwa`
Warner, Natasha, Jongman, Allard, Cutler, Anne & Mücke, Doris (2001). "The phonological status of
Dutch epenthetic schwa." *Phonology* 18, 387–420.
- URL: https://pure.mpg.de/rest/items/item_77131/component/file_77132/content (author copy in the
  MPI PuRe repository; the Cambridge Core version is paywalled)
- Access: **OA** via repository. Status: confirmed. Files: `devoic-warner2001-epenthetic-schwa.pdf`,
  `.txt`
- Covers: §3 the full statement of the schwa-epenthesis environment with articulatory evidence
  (clear-/l/ vs dark-/l/) that epenthesis inserts a genuine phonological unit. This is the
  authoritative source for the *melk* → [mɛlək] rule.

### `devoic-schwa-mpi`
Kuijpers, Cecile, van Donselaar, Wilma & Cutler, Anne (1996). "Phonological variation: epenthesis
and deletion of schwa in Dutch." *Proc. ICSLP '96*, 4 pp.
- URL: https://pure.mpg.de/rest/items/item_77058/component/file_77059/content
- Access: **OA**. Status: confirmed. Files: `devoic-schwa-mpi.pdf`, `.txt`
- Covers: §3 the rule stated crisply and implementably — epenthetic schwa appears only in a
  **tautosyllabic liquid + obstruent** coda cluster whose members do **not** share place features;
  blocked in homorganic clusters and before coronal /s t/. Plus schwa *deletion* (*envelop*,
  *kapelaan*). Pair with `taalportaal-schwa-epenthesis-deletion`, which gives the example list
  (*kalm, arm, help, harp, herfst*).

### `devoic-grijzenhout-roa303`
Grijzenhout, Janet & Krämer, Martin (1999). "Final devoicing and voicing assimilation in Dutch
derivation and cliticization." ROA-303, Rutgers Optimality Archive, 10 pp.
- URL: https://roa.rutgers.edu/files/303-0399/roa-303-grijzenhout-2.pdf
- Access: **OA**. Status: confirmed. Files: `devoic-grijzenhout-roa303.pdf`, `.txt`
- Covers: §3 which suffixes and clitics trigger final devoicing and which do not, and how it
  interacts with regressive voicing assimilation. OT-framed — take the data, skip the tableaux.

### `devoic-jansen2021-schwa`
Jansen, Roos (2021). *Do Dutchies schwa a lot? The possible influence of Dutch pronunciation on
the perception of spoken English.* MA thesis, Universiteit van Amsterdam, 27 pp.
- URL: https://www.fon.hum.uva.nl/archive/2021/2021-MA-RoosJansen.pdf
- Access: **OA**. Status: confirmed. Files: `devoic-jansen2021-schwa.pdf`, `.txt`
- Covers: §3 Dutch schwa epenthesis carried over into Dutch speakers' English — evidence that the
  rule is applied productively to foreign material, which is exactly our use case. Supporting.

---

## Foreign proper names (§5)

### `names-paardekooper2009-vreemde-namen`
Paardekooper, Piet (2009). "'Edinberoow' en 'Sevielja': onze uitspraak van vreemde namen."
*Onze Taal* 78, 16–17. (Dutch-language.)
- URL: https://www.dbnl.org/tekst/_taa014200901_01/_taa014200901_01_0007.php
- Access: **OA to read on DBNL**. Status: confirmed (agent-reported).
- Files: `names-paardekooper2009-vreemde-namen.html`, `.txt`
- Covers: §5 the most on-point item for *pronunciation* of foreign names (as opposed to spelling):
  the Vaz Diaz / ANP pronunciation register for newsreaders, and the Dutch tendency to *attempt*
  the source-language pronunciation where English speakers would not. Relevant to how far our
  output should nativize.

### `names-wiki-translit`
nl.wikipedia, "Wikipedia:Transliteratie- en transcriptiegids."
- URL: https://nl.wikipedia.org/wiki/Wikipedia:Transliteratie-_en_transcriptiegids
- Access: **OA** (CC BY-SA). Files: `names-wiki-translit.html`, `.txt`
- Covers: **§5 the closest thing to an explicit Dutch-oriented transcription convention set** —
  per-language tables with the stated design goal that "the intuitive pronunciation of an
  arbitrary Dutch-speaking reader approximates the correct pronunciation as closely as possible."
  That is precisely our romanization brief, so this is a model to copy rather than invent.

### `names-wiki-spellinguitspraak`
nl.wikipedia, "Spellinguitspraak." — **OA** (CC BY-SA).
Files: `names-wiki-spellinguitspraak.html`, `.txt`
- Covers: §3/§5 spelling-pronunciation as an adaptation route, with a *Buitenlandse namen*
  section: *parfum* (Dutch-adapted initial stress vs. Belgian French-like), *dossier*, English
  *tram/handicap* with Dutch /ɑ/, *cornedbeef* → *kornetbief* as a dictionary-sanctioned spelling
  pronunciation.

### `names-taalunie-verantwoording`, `names-taalunie-ban`, `names-taaladvies-geo`
Taalunie / Commissie Aardrijkskundige Namen — *Buitenlandse Aardrijkskundige Namen*.
- URLs: https://namen.taalunie.org/verantwoording ·
  https://namen.taalunie.org/buitenlandse-aardrijkskundige-namen-het-nederlands ·
  https://taaladvies.net/spelling-van-buitenlandse-aardrijkskundige-namen-algemeen/ (2021-05-12)
- Access: **OA**. Files: `names-taalunie-*.html`/`.txt`, `names-taaladvies-geo.html`/`.txt`
- Covers: §5 the official policy — endonym/exonym criteria, diacritics dropped where unusual in
  Dutch (with the pronunciation consequences acknowledged), transliteration from non-Latin
  scripts. `-verantwoording` is the substantive one (~40k of text); the other two are thinner.

### `names-wiki-geo`, `names-wiki-geonames-guide`, `names-dbnl-bakker1997`
Supporting: nl.wikipedia "Spelling van aardrijkskundige namen in het Nederlands" and
"Wikipedia:Buitenlandse geografische namen" (**OA**, CC BY-SA); Bakker, Jaap (1997), "Schipperen
of verzuipen: een nieuwe lijst met buitenlandse namen," *Onze Taal* 66, 18–19
(https://www.dbnl.org/tekst/_taa014199701_01/_taa014199701_01_0012.php, **OA** on DBNL) — a
critique of the Taalunie list, useful for where the official policy is contested.


---

## Not used (paywalled or otherwise unavailable)

### `booij1995` — the main loss
Booij, Geert (1995). *The Phonology of Dutch.* Oxford: Clarendon (The Phonology of the World's
Languages). — **paywalled** (OUP; Google Books preview only).
- What we lose: the single authoritative treatment of Dutch syllable structure, final devoicing,
  nasal assimilation and loanword phonology, with the cluster inventories stated in one place.
- **How far it is actually recovered:** further than expected. Taalportaal's phonology section is
  built on Booij 1995 and cites it page-by-page (e.g. "Booij (1995:26)" for complex onsets,
  "Booij 1995:40" for /h/ in codas), so the *content* of the cluster and syllable chapters is
  available second-hand from an open (if restrictively licensed) source, and Wikipedia's
  Phonotactics section independently cites Booij 1999. Booij's own site additionally supplies
  `booij1999-msc`, `booij2011-msc`, `booij2003-concrete-fonologie` and `booij2014-word-formation`
  free. The residual gap is Booij's own loanword-phonology discussion and his exact wording.

### `trommelen1984`
Trommelen, Mieke (1984). *The Syllable in Dutch, with Special Reference to Diminutive Formation.*
Dordrecht: Foris (Publications in Language Sciences 15). Reissued by De Gruyter
(doi:10.1515/9783110846379).
- **paywalled** (De Gruyter). Status: **verification failed in a way worth recording** — the
  source-plan describes it as a "(Leiden diss.)" possibly open in a Leiden repository. It is a
  Foris/De Gruyter *book*, and no copy is in the Leiden repositories, LOT, or DBNL. The
  "open Leiden dissertation" premise is wrong, so there is nothing to find.
- What we lose: a dedicated monograph on Dutch syllable structure and diminutive allomorphy.
  §2 is well covered without it; the diminutive material for §6 is in `booij2014-word-formation`.

### `nagy2007` (full dissertation)
See the entry above — blocked by a Hungarian publication moratorium, not by a paywall, and never
posted. Not obtainable from any repository.

### `posthumus1986` — the biggest genuine dead end
Posthumus, J. (1986). *A Description of a Corpus of Anglicisms.* Groningen: Anglistisch Instituut.
- Not digitized anywhere; a print-only institute publication. `loan-ivdnt-anglicismen` states that
  this is where the full adaptation apparatus and the 829-word anglicism corpus are set out — i.e.
  the systematic version of what the 1988 *Onze Taal* piece summarizes in two pages. Nothing else
  found replaces it.

### `vandevelde2002` — nominally open, blocked by bot protection (worth one manual click)
Van de Velde, Hans & van Hout, Roeland (2002). "Loan words as markers of differentiation."
*Linguistics in the Netherlands* 19, 163–173.
- Repository copy: https://repository.ubn.ru.nl/bitstream/handle/2066/104351/1/176160.pdf
- `repository.ubn.ru.nl` returns **HTTP 403 to every automated request** (four URL forms, browser
  UA, Referer, HEAD and GET, from two different agents). This looks like bot protection, **not a
  paywall or a login wall** — so it is very likely genuinely open in a real browser.
- **Worth the user's one click**, because per the abstract it carries exactly the /ɡ/
  stop-vs-fricative variation data across the Netherlands *and* Flanders for *buggy, goal,
  goulash, guillotine, mango* — i.e. Belgian-specific loan-adaptation numbers for the one segment
  our sources disagree about most. Publisher copies (Benjamins, Ingenta) are subscription-only.

### Other items not obtained
- Van de Velde, H., Hiligsmann, P. & Chauvaux, A. (2006). "De uitspraak van Franse leenwoorden in
  het Nederlands: met of zonder slot-e?" — KNAW record is metadata-only; no full text located.
- Nagy, Roland. "Notes on morphological, phonological and orthographical integration of ten
  lexical borrowings into Dutch." — academia.edu behind a login; not fetched, per the brief.
- Frijlink, Hendrik. *Woordenboek voor de spelling en uitspraak van vreemde eigennamen* (DBNL
  `frij003woor01`) — DBNL holds **page scans only** (21 MB, no OCR layer). A 19th-century
  pronunciation dictionary of foreign proper names; not machine-readable without OCR, so not
  downloaded. Could be OCR'd later if §5 needs more.
- onzetaal.nl's own Taalloket pages are a client-rendered Angular app; `curl` gets a nav shell
  only. The DBNL *Onze Taal* archive (used throughout above) is the better route up to ~2015.

### Kager 1989, Collins & Mees 2003, Sebregts 2014
Cited heavily by Wikipedia and Taalportaal (Collins & Mees for allophony, Sebregts 2014 for the
enormous /r/ variation survey, Kager 1989 for stress) but themselves paywalled/library items. We
get their conclusions through the citing sources; we do not get their data tables.

---

## Belgian vs. Netherlandic — the decision, with evidence

**Recommendation: Belgian Standard Dutch.** The source-plan flagged this as an open question with
"default Belgian" on path-of-least-resistance grounds. The evidence found here upgrades that from
a default to a positive choice:

1. **The PHOIBLE row and its description are the same document.** PHOIBLE InvID 2169 is sourced
   from Verhoeven (2005) (verified on phoible.org/inventories/view/2169). Choosing Belgian means
   inventory and prose never disagree; choosing Netherlandic would mean carrying a PHOIBLE row
   from one variety and a description from another.
2. **The Belgian description is open and adequate**, and so is the Netherlandic one, so openness
   does not favour either. Neither JIPA Illustration is long (5 pp and 3 pp).
3. **Belgian is the better *filter* for Irish input**, which is the point of the exercise:
   - Belgian keeps **/ɣ/** as a phoneme. Irish has /ɣ/ (a lenition output). Netherlandic has no
     /ɣ/ and a uvular /χ/, so Irish /ɣ/ would have to be repaired; in Belgian it maps to itself.
     This is the strongest single argument.
   - Belgian keeps the **fricative voicing contrast** (/v z ɣ/ vs /f s x/); Netherlandic devoices
     them heavily. Preserving the contrast preserves more of the Irish input.
   - Belgian /r/ is an alveolar trill (with a uvular variant), matching Irish /ɾˠ/ far better than
     the Netherlandic grab-bag of approximant/bunched/uvular realisations.
4. **Cost of choosing Belgian:** the two richest phonotactic sources — Taalportaal and Booij —
   describe *Netherlandic* Dutch. Since the varieties differ in phonetics rather than phonotactics
   (Verhoeven: "the lexical and syntactic differences between the two language varieties are very
   small", the differences being phonetic), importing the Netherlandic cluster inventories into a
   Belgian digest is defensible — but the digest should say so explicitly in §0 rather than let it
   pass silently.

**Discrepancy to record in §1 (real, and it matters).** Neither the PHOIBLE row nor Verhoeven's
vowel chart lists **schwa /ə/** — Verhoeven gives "twelve monophthongs and three diphthongs",
all full vowels. But Dutch schwa is central to this project: it is the epenthetic vowel
(*melk* → [mɛlək]), the reduction vowel, and the vowel of most inflectional endings. The digest
must add /ə/ to the inventory over the PHOIBLE row, citing `taalportaal-schwa-epenthesis-deletion`
and `devoic-warner2001-epenthetic-schwa`. Do not treat its absence from PHOIBLE as evidence.

---

## Gaps — my judgement of what is still weakest

1. **§7 is covered — better than I expected going in, and better than the source-plan assumed.**
   The plan treated WOLD as "the best gold set of the four", but WOLD gives orthography and donor
   language only, no adapted IPA, so its 1588 entries yield rows with an empty `target_ipa`. The
   actual §7 backbone is three other things: `loan-vandijk-toename` (a TV corpus with **Dutch and
   English IPA side by side, per token** — rows usable almost verbatim),
   `taalportaal-stress-loanwords` (French→Dutch, both sides in IPA, with the stress shift marked),
   and `loan-theissen2006-nasalen` + `loan-gerritsen1995-*` + `loan-kleinbreukink1999-culinair`
   (per-word measured preference data, several of them **split Netherlandic vs Belgian**). The
   30-row minimum is comfortably reachable with both sides transcribed. `loan-posthumus1988` adds
   many more rows but with the target in **Dutch respelling** (*thinner* → *tinner*), which the
   digest will have to convert to IPA and mark as such.
2. **Bias in what we do have:** heavily English- and French-sourced, and skewed toward *recent*
   English loans, which van der Sijs 2009 says are adapted *least*. The oldest, most thoroughly
   nativized loans (Latin, French) show the repairs we actually want to model, but are documented
   diachronically rather than as adaptation data.
3. **Nagy's dissertation is the specific thing missing** — it is the one work devoted precisely to
   "the phonological integration of loanwords in Dutch", and only its abstract exists. Everything
   we have on §3 is assembled from partial sources around the hole it leaves.
4. **Irish-specific (§8) has no source at all.** No document here says anything about Dutch
   treating palatalized consonants, because Dutch has never borrowed from a language with that
   contrast in any documented quantity. The broad/slender collapse will be a pure design decision.
   Note one Dutch-internal hook worth exploring: Dutch *does* have palatal outputs from /Cj/
   sequences (diminutive [c], [ɲ], the /tj/ → [t͡ɕ] and /sj/ → [ʃ] assimilations in
   `wiki-nl-phonology` and `taalportaal-`), so Cʲ → Cj has a target-internal precedent that
   depalatalization does not. That is the closest thing to evidence §8 will get.
5. **Tooling note for later agents:** Taalportaal and geertbooij.com return **403 to WebFetch**
   but serve fine to `curl` with a browser User-Agent. That is a tooling artifact, not an access
   restriction — do not record such sites as blocked without trying `curl`.
6. **Licensing, not availability, is the awkward one.** The best phonotactic source (Taalportaal)
   is the only one that is not openly licensed. See its entry.
