# Phonological rule-file sources

**Project.** Simulate contact-language name forms by running **Irish (Gaeilge)** vocabulary through the phonological grammar of a target language. Targets: **Welsh, Egyptian (Cairene) Arabic, Georgian, Dutch.** Working format: IPA / CLDF-CLTS.

Access tags: **[OA]** = open access, no login · **[Free*]** = free with account or substantial preview · **[Buy]** = purchasable (preview only online).

---

## How a rule file decomposes, and where each piece comes from

No single source supplies all of it:

| Component | Best source(s) |
|---|---|
| Phoneme inventory + distinctive features | PHOIBLE (+ CLTS for IPA→feature mapping) |
| Syllable template (coarse) | LAPSyD |
| Licit onsets / codas, cluster co-occurrence | the per-language phonology monograph |
| Repair: epenthesis site & vowel, deletion, metathesis | the per-language loanword papers — use the **data tables** |
| Segment substitution (Irish phoneme absent in target) | loanword papers (attested mappings) first; CLTS feature-distance as fallback |

Two project-wide points:

- **Irish is the source in every pairing, so substitution does most of the work.** Irish carries a broad (velarized) vs. slender (palatalized) contrast on nearly every consonant. **None of the four targets has a phonemic palatalization contrast**, so each grammar must decide how to collapse it — depalatalize, or re-express as a Cⱼ/Cˠ sequence. Decide this once per target; it shapes more output than cluster repair does.
- **Theory is separable from the data.** The repair literature is mostly framed in Optimality Theory, and some of it leans on markedness-universal / UG-style reasoning. For a grammar-based generator you only need the attested input→output mappings in the tables. Read those; ignore the tableaux.

---

## Cross-linguistic infrastructure (all four languages)

**PHOIBLE 2.0** — phoneme inventories with per-segment distinctive features and allophone data; distributed as a CLDF dataset, queryable with `pycldf`. This is your inventory layer, already in IPA/feature form. Has **no** phonotactic or syllable data.
- **[OA]** phoible.org · GitHub `cldf-datasets/phoible`
- Caveat: multiple inventories per language (especially Arabic). You pick one per target — relevant when you extract the starter inventories.

**CLTS — Cross-Linguistic Transcription Systems** — maps any IPA string to a feature bundle. Use it to compute nearest-segment substitutions when Irish has a phoneme the target lacks and no attested mapping exists.
- **[OA]** clts.clld.org · GitHub `cldf-clts/clts`

**LAPSyD — Lyon-Albuquerque Phonological Systems Database** — inventories + **syllable structure** + stress/tone summaries, ~700 languages. Use for the coarse syllable template; not detailed enough for cluster phonotactics.
- **[OA]** lapsyd.huma-num.fr

---

## Welsh

*Inventory (free cross-check):* /p b t d k g/; fricatives incl. /f v θ ð s ʃ χ h/; lateral fricative /ɬ/; voiceless sonorants /m̥ n̥ ŋ̊ r̥/; /l r j w/. Vowels carry a length contrast; Northern adds central /ɨ/. PHOIBLE has Welsh; the Wikipedia "Welsh phonology" article is a fine free orientation.

**Hannahs, S. J. (2013). *The Phonology of Welsh.* Oxford: OUP (Phonology of the World's Languages).** The modern standard reference — syllabification, phonotactics, the (bisyllabic/bimoraic) minimal word, penultimate stress.
- **[Buy]** OUP; substantial Google Books preview.

**Wood, S. A. J. (1986). "Vowel Quantity and Syllable Structure in Welsh." *Lund Working Papers in Linguistics.*** Free, and explicitly treats how loanword syllable structure is adapted to Welsh.
- **[OA]** swphonetics.com/wp-content/uploads/2011/12/welshsyllstruct1986.pdf

**"Word-Initial Clusters in Welsh: A Typological Analysis."** Cluster phonotactics and the syncope that produces word-initial clusters.
- **[Free*]** ResearchGate.

*Phonotactics summary:* syllable ≈ (C)(C)V(C); onsets allow obstruent + liquid (/pl pr bl br/) but ban obstruent + nasal (*/pn tn/). Moderate restriction.

*Irish → Welsh:* main work is palatalization collapse. Welsh lacks /ɣ/ (Irish broad *dh/gh*) → substitute /g/ or delete; lacks native /z ʒ dʒ/ (loan-only). Irish /p f v x h/ all have Welsh equivalents. Welsh /ɬ χ/ are target-only — unused unless you deploy them as repair outputs.

---

## Egyptian (Cairene) Arabic

**Why this variety.** Free-resource availability was set to outrank the specific dialect, with a mild lean toward a MENA dialect. Cairene satisfies both: most-studied Arabic dialect, de facto media-standard spoken variety, one of Watson's two focus dialects, and the only target here with a fully open-access loanword paper.

*Inventory (free):* Cairene has **/g/** (not /dʒ/); lacks /p v/ and the interdentals /θ ð/ (merged); has emphatics /tˤ dˤ sˤ ðˤ/ plus marginal /rˤ mˤ bˤ/. Vowels /i iː e eː a aː o oː u uː/.
- **[OA]** ASHA "Arabic Phonemic Inventory" PDF (asha.org); Wikipedia "Egyptian Arabic phonology" (inventory + adaptation notes, incl. /q/ → /ʔ/ or /k/).

**Watson, Janet C. E. (2002). *The Phonology and Morphology of Arabic.* Oxford: OUP.** Authoritative; Cairene + San'ani. Chapters on the phoneme system, syllabification, and stress.
- **[Buy]** OUP; good Google Books preview (id `lLQSDAAAQBAJ`).

**"Phonological and Morphological Integration of Loanwords into Egyptian Arabic." *Égypte/Monde arabe.*** **The repair source.** Open access, with concrete attested-substitution tables: /θ/ → /s/ or /t/ (*thermos* → /tormos/); /ʒ/ → /s/ (Coptic substrate); etc.
- **[OA]** journals.openedition.org/ema/1958

**"Arabic Phonology" (comparative chapter). *English Linguistics Research.*** MSA vs. the six dialect groups on sound system, syllable structure, and stress — useful for situating Cairene.
- **[OA]** sciedupress.com → ELR article 16452 (`/download/16452/10555`).

**Broselow, Ellen — Arabic epenthesis (e.g. 1983, 1992).** Foundational for repair *direction*: Cairene epenthesizes between **C2–C3**, Iraqi between **C1–C2**. This is your headline cluster-repair rule.
- **[varies]** in proceedings / edited volumes — search by title.

*Phonotactics summary:* no complex onsets (one onset C max); CVC and CVːC/CVCC syllables; three-consonant sequences broken by the C2–C3 epenthetic vowel. **Restrictive, epenthesis-heavy** — your opposite extreme from Georgian/Dutch.

*Irish → Egyptian Arabic:* /p/ → /b/, /v/ → /f/ (both absent). Palatalization collapses. Irish /x ɣ h/ map cleanly (/x/, /ɣ~ʁ/, /h/). **Option worth trying:** Irish broad/velarized consonants have a loose auditory analogue in Arabic **emphatics** — mapping them onto /tˤ dˤ sˤ/ rather than plain consonants gives a more "Arabic" flavor (not a clean phonemic match, but defensible for a name generator). Irish onset clusters trigger heavy epenthesis.

---

## Georgian

*Inventory (free):* 28 consonants; vowels /i e a o u/ (no length contrast); three-way stop/affricate contrast — voiced / voiceless-aspirated / **ejective** — across five places; velar and uvular fricatives present. /f/ is marginal (loan).
- **[OA]** Self (n.d.), "An OT Analysis of Vowel Syncope in Georgian" (diu.edu) summarizes the inventory; PHOIBLE has Georgian.

**Butskhrikidze, Marika (2002). *The Consonant Phonotactics of Georgian.* Leiden diss. (LOT 63).** The definitive source, and a full open-access PDF. Surface CCC clusters derive from CVCVCV structures via vowel reduction; underlying clusters are maximally biconsonantal.
- **[OA]** lotpublications.nl/Documents/063_fulltext.pdf (mirror: pure.mpg.de).

*Phonotactics summary:* extremely permissive — Georgian tolerates long word-initial consonant sequences. As a filter it barely repairs clusters: **your permissive extreme.**

*Irish → Georgian:* almost no cluster repair needed. Irish stops map onto the voiced or voiceless-aspirated series (leave ejectives as outputs only if you want them). Palatalization collapses. Irish long vowels shorten. Irish /f/ either imports as /f/ or shifts to /pʰ/. Irish /x ɣ/ map cleanly.

---

## Dutch

*Inventory (free):* PHOIBLE has Dutch. Standard inventory includes /x ɣ/ (the voiced/voiceless "g" varies North vs. South), front rounded vowels, a tense/lax vowel system, and word-final devoicing.

**Booij, Geert (1995). *The Phonology of Dutch.* Oxford: OUP (Phonology of the World's Languages).** Standard reference — syllable structure, **final devoicing**, nasal assimilation, loanword treatment.
- **[Buy]** OUP; older, often library-available; Google Books preview.

**Nagy, Roland. "The phonological integration of loanwords in Dutch."** Repair source.
- **[Free*]** academia.edu.

**Kager, René. "Phonotactics as phonology: knowledge of a complex restriction in Dutch."** Dutch phonotactic restrictions.
- **[Free*]** academia.edu.

*Phonotactics summary:* permissive clusters (complex onsets and codas). Cleanest implementable repair = **final devoicing** (any voiced-obstruent-final Irish word loses voicing). Permissive side, with Georgian.

*Irish → Dutch:* /p f v x h/ all fine. Palatalization collapses. Final devoicing hits Irish voiced-final forms. Dutch front rounded vowels are target-only (unused unless as repair outputs).

---

## Optional: repair-type orientation (skip the theory)

**Kang, Yoonjung (2011). "Loanword Phonology." *The Blackwell Companion to Phonology.*** Useful only as a **catalogue of repair types** (epenthesis vs. deletion vs. substitution; what governs epenthetic vowel quality) and of attested cross-language patterns. Framing is OT / markedness-universals — read the descriptive generalizations, ignore the rest. This is the longer of the two overviews; the shorter circulating chapter leans harder on UG, so skip that one.
- **[OA]** yoonjungkang.com/uploads/1/1/6/2/11625099/tbc_100.kang.pdf

---

*URLs are as located at time of writing; access tiers can change. ResearchGate / academia.edu items generally need a free account.*
