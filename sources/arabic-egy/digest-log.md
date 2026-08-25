# digest-log.md — Egyptian (Cairene) Arabic

## Which source was used for which section

| section | primary | secondary / cross-check |
|---|---|---|
| §0 variety | `alqarhi2019-arabic-phonology`, `ema1952-woidich` (what to exclude) | `lapsyd-arz` for what the PHOIBLE row actually is |
| §1 inventory | `wiki-egy-phonology` (which sources its chart to Watson 2002), `abdelmassih-intro` Table 1 (PDF-verified) | `hassig2011-cairene` p.13, `wiki-help-ipa-egy`, `lapsyd-arz`; `ema1958` §12–22 for the loan-segment behaviour |
| §2 syllable/clusters | `broselow1976` ch.1, `ijllnet-cairene-english-syll` (Khalifa 2018) pp.92–99, `abdelmassih-intro` §7 | `broselow-arabic-syll`, `hassig2011-cairene` p.31, `ojml-cairene-syllable`, `lapsyd-arz`, `kwpl-ot-cairene-loan` p.4 |
| §3 repair | `ema1958` §12–38 and `kwpl-ot-cairene-loan` (Galal 2004) — the two dedicated loanword sources | `broselow-position-quality` (2015) for the sonority split and vowel quality; `broselow1976` for the native rules and their ordering; `abdelmassih-v3` morphophonemic entries |
| §4 stress/length | `watson2011-word-stress`, `mccarthy1979-stress-syll` | `broselow1976` pp.7–8, `abdelmassih-v3` p.254, `lapsyd-arz`, `wiki-egy-phonology §Stress`; `ema1958` §26, §33–35 for loans |
| §5 romanization | `wiki-help-ipa-egy` (the "commonly used form in Egypt"), `wiki-egy-arabic §Romanization` | `abdelmassih-intro` p.2, `wiki-romanization-arabic` |
| §6 morphology | `abdelmassih-v3` (article, nisba, feminine, elative, measures, plurals) | `broselow1976` ch.2 (nisba + construct), `ema1958` §30, §40–53 (loan morphology), `wiki-sun-moon-letters`, `wiki-nisba`, `wiki-egy-arabic §Plurals`, `§Color/defect nouns` |
| §7 attested | `ema1958` (231 rows), `kwpl-ot-cairene-loan` (20, PDF-verified), Abdel-Massih (28, PDF-verified), `broselow-position-quality` (11), Wikipedia (13), `ijllnet-cairene-english-syll` (11, L2 data) | — |
| §8 Irish mismatches | `broselow1976` §1.8 (emphasis, the key section), `ema1958` §19–21 (emphasis assigned in loans) | `wiki-egy-phonology §Emphasis spreading`; abdelmassih loan rows corroborate |
| §9 open questions | — | — |

Sources consulted but contributing little: `broselow-marginal-phonology` (case study is Balantak;
not used), `hellmuth2007-prosodic` (phrase-level, not needed), `asha-arabic-inventory` (generic
Arabic, correctly flagged in bib.md as low value; not used), `alqarhi2019-arabic-phonology` (one
citation only).

## bib.md corrections

These are descriptions in `bib.md` that turned out to be wrong. All were found by opening the
files.

1. **`broselow-stress-epenthesis`** — bib.md: "whether epenthetic vowels count for stress (Cairene
   among the cases)". **It contains no Cairene data at all.** Its Arabic case study is *Iraqi*
   only (kitábit / kítbat); the other cases are Selayarese, North Kyungsang Korean and Winnebago.
   The Cairene answer had to come from `watson2011-word-stress` p.2992 and
   `watson2007-syllabification` p.340 instead. *(Cairene does count epenthetic vowels for stress —
   the fact is right, the attribution was wrong.)*
2. **`broselow-stress-adaptation`** — bib.md: "§3/§4 — what happens to source-language stress in
   loans". **It contains no Arabic loanword data whatsoever.** Case studies: Spanish→Huave,
   English→Fijian, Spanish→K'ichee', Indonesian→Selayarese. Arabic appears once, in a footnote
   about a stress-*perception* experiment [p.482]. The only source we have for loan stress in
   Cairene is `ema1958` §26, §33–35.
3. **"Not found: No JIPA 'Illustrations of the IPA' for Egyptian/Cairene Arabic."** — **There is
   one**: Thelwall, Robin & M. Akram Sa'adeddin (1990), "Illustrations of the IPA: Egyptian
   Arabic", *JIPA* 20: 37–39, also in the *Handbook of the IPA* pp.51–54. It is the stated source
   of the phonetic values in the LAPSyD entry for `arz`, and hence transitively of the PHOIBLE row
   the project is using. It was not acquired. Worth getting — it is the source of the /χ ʁ/ and
   /æː/ transcriptions that conflict with the Wikipedia/Watson chart (§0).
4. **`wiki-egy-arabic`'s romanization comparison table mis-describes Abdel-Massih.** bib.md
   repeats it, and the extraction brief did too. Wikipedia says Abdel-Massih writes `ɢ ʃ ʂ ɖ ʈ ᶎ
   ƹ ꞕ`. Checked against the books: he writes `ʔ` and a separate `q`; dotted `ṭ ḍ ṣ ẓ ḷ ṛ`;
   `š ž`; `ħ ʕ`; `x ɣ`. Only the doubled-vowel length convention matches. A /ʔ/ deriving from qāf
   is marked in the *lexicon* with a parenthesised "(Q)", not with a distinct symbol
   [abdelmassih-intro p.29].
5. **`kwpl-ot-cairene-loan.txt` and `broselow-arabic-syll.txt` have identical byte sizes
   (54419)** — this was checked and is a **coincidence**, not a duplicated file. Both contain the
   right paper. No correction needed; noted so nobody else spends time on it.

## What could not be resolved

1. **The `ema1958` appendix and six data tables are images only.** The article's own transcription
   key lives at `docannexe/image/1958/img-7.png`, and the four derivational-paradigm tables (§40),
   the masculine sound-plural list (§47) and the both-plurals list (§48) are `img-1..6.png`. The
   machine had no network access during extraction, so all seven were fetched empty. **The symbol
   key used for 231 attested rows is therefore reconstructed from the article's own usage**:
   `š`=/ʃ/, `ğ`=/ʒ/, `dğ`=/dʒ/, `tš`=/tʃ/, `ø`=/θ/, `X`=/ʁ~ɣ/, `?`=/ʔ/, `c`=/ʕ/, `x`=/χ~x/,
   doubled vowel = long, doubled consonant = geminate, `'` = stress. The reading of **`â/ââ` as
   the backed allophone /ɑ(ː)/** is the weakest link: it is inferred from the fact that `â` occurs
   exactly in the words that had emphatics in the print original. A future pass with network
   access should fetch those seven images and verify.
2. **`ema1958`'s emphatics are stripped in the online text** (the journal says so). This is a
   known, documented gap, not a resolvable one without the print original. Every affected row is
   tagged. It means the file cannot be used to answer "does Cairene put an emphatic here?" — only
   Hafez's *prose* rule (§19–20) can, and it is quoted in digest §3.6 and §8.1.
3. **Whether /sm sn/ take prothesis or anaptyxis.** `broselow-position-quality` p.295 has /sl/ and
   /sw/ taking anaptyxis and /sk st sp/ taking prothesis. No source has an /sm/ or /sn/ example.
   Irish has both. Left as open question §9.4.
4. **Stop+nasal onsets (/kn gn mn/).** Irish has them; no Cairene source has an example. Their
   sonority profile is falling, like /s/+stop, which would predict prothesis — but that is an
   inference, not a finding. §9.4.
5. **Whether the emphatic set is 4 or 6 members.** Broselow [p.xiii] and Abdel-Massih
   [intro p.6] both give **six** phonemic emphatics /tˤ dˤ sˤ zˤ lˤ rˤ/. Watson (via Wikipedia)
   gives four phonemic plus /rˤ bˤ mˤ lˤ/ as *marginal*. Hassig [p.13] gives four phonemic and
   analyses [lˤ rˤ] as allophones. Recorded as a CONFLICT in digest §1; the practical difference
   is whether /lˤ rˤ/ can be used freely as targets for Irish broad /l r/. Two of three sources
   say yes.
6. **The digest could not settle the palatalization question**, and says so. There is no Cairene
   data on it in any of the nine sources. That is a finding, not a failure, but it means §8.1 is
   options-with-arguments rather than a rule.

## Cross-source conflicts recorded in the digest

| topic | positions | where |
|---|---|---|
| /x ɣ/ velar vs /χ ʁ/ uvular | `wiki-egy-phonology §Emphasis spreading` (velar in Cairene, uvular is Ṣaʿīdi) vs `lapsyd-arz`/PHOIBLE 231 and `hassig2011-cairene` (uvular). `abdelmassih-v3` p.40 sides with velar ("back-velar") | §0.3 |
| /dʒ/ in the inventory | PHOIBLE 231 and `lapsyd-arz` list it; `wiki-egy-phonology`, `hassig2011-cairene` p.15/47–48 and every descriptive source deny it (→ /g/) | §0.2 |
| /q/ marginal | `wiki-egy-phonology`, `lapsyd-arz`, `abdelmassih-intro` p.15, `broselow1976` p.25 (marginal/MSA-only) vs `hassig2011-cairene` p.13, p.47 (fully regular). Also `ema1958` §18 vs §19–20, reconciled by register | §0.5, §1 |
| the vowel system | PHOIBLE/Wikipedia/LAPSyD 5-long-3-short vs `hassig2011-cairene` p.13 4-quality with allophonic RTR | §0.6 |
| are short /e o/ phonemes | `ema1958` §24 yes (with a minimal pair) vs Watson 2002 p.22 no ("not used by most speakers") vs Woidich 2006 p.7 only in careful slow speech vs `abdelmassih-intro` p.21 yes but "not common" | §1, §9.6 |
| emphatic set size | see item 5 above | §1, §9.5 |
| emphasis-spread domain | `broselow1976` pp.41–46 (syllable + conditioned RES + word-bounded LES) vs `wiki-egy-phonology §Emphasis spreading` (whole phonological word, bidirectional, no blockers — and that section is `{{Unreferenced}}`) | §8.2 |
| word-initial epenthesis | `broselow1976` p.23 unconditional prothesis vs `broselow-position-quality` p.295 sonority-conditioned mixed. Resolved: 1976 = native morphology, 2015 = borrowing | §3.1 |
| C2–C3 epenthesis | `broselow1976`, `kiparsky-syll-moras`, `abdelmassih-intro` p.24, `wiki-egy-phonology`, `kwpl-ot-cairene-loan` all agree; `ema1958` §29 simply does not discuss it (a gap, not a disagreement) | §3.2 |
| medial cluster maximum | `kwpl-ot-cairene-loan` p.4 rule (4c) "max two word-medially" vs Khalifa/Aquil "max one". Resolved: Galal counts the heterosyllabic C.C, the others the medial coda. Not a real conflict | §2 |
| word-initial CC licit? | `broselow1976` p.20 never vs `abdelmassih-intro` p.26 "very rare" (kwajjis, braavo) vs `ema1958` §38/§60 tolerated in prestige speech. Live register question | §9.7 |
| /θ/ in a foreign loan | `ema1958` §16 → /t/ (English loans) vs `wiki-egy-phonology §Consonants note 5` → /s/ | §3.6, §9.5 |
| shortened /eː oː/ written high or mid | `broselow1976` pp.18–19 → /i u/ vs `wiki-egy-phonology §Vowel shortening` → [e o]. Same neutralization, different notation | §3.8 |
| sun-letter set | `wiki-sun-moon-letters` Classical set (incl. ث ذ ظ, which Cairene lacks) vs `abdelmassih-v3` pp.83–84 Cairene set (dentals + /ʃ/, optional before /k g/) | §6.1 |
| 'television', 'Belgium' | `abdelmassih-intro` p.14 `tilivizyóon`, `balžíka` vs `abdelmassih-v4` p.78 `tilivisyoon`, `abdelmassih-v3` p.142 `baljiika`. Internal to one author | §7 note |

## Post-review corrections (applied)

An adversarial review pass (one reviewer fanning out to five citation-verification agents plus a
format audit) was run against the finished digest. Findings applied:

**Corrected — substantive:**
1. **§4 stress: the algorithm was inverted and has been rewritten.** The earlier draft's step 3
   read "stress the antepenult, unless the pre-antepenult is also light", dropping Watson's
   condition that *the penult and antepenult must both be light*, and omitting his step (c)
   "otherwise, stress the penult". It also asserted that "a heavy antepenult attracts stress when
   the penult is light" and printed `ˈmadrasa`. Both are the reverse of the sources: Watson
   p.2991 — "In words with a heavy antepenult, **Cairene stresses the light penult** … Cairene
   [madˈrasa] contrasts with Beirut/Damascene [ˈmadrase]"; McCarthy p.446 gives `marˈtaba` under
   "otherwise stress the penult". The rule, the worked-example table (now 17 rows, each with its
   own citation and rule step) and the Abdel-Massih paragraph were all rewritten. **This was the
   one defect that would have mis-stressed a large share of generated names.**
2. **attested.tsv: eleven invented `source_ipa` values removed.** The Khalifa rows carried English
   IPA transcriptions that are not in Khalifa, who gives the donor word in orthography only.
   `source_ipa` is now empty in all 314 rows, and §7's claim about it corrected.
3. **The Khalifa rows are *predicted* errors, not observed ones** — from a starred table headed
   "Error", introduced "it is expected that the Cairene learners will … tend to…". Re-tagged in
   all 11 notes and in §7; §3.4 now says its three-member-coda evidence is correspondingly weak.
4. **§8.1: `bṛaavo` removed from the loan-emphasis evidence.** Abdel-Massih prints it plain. The
   argument stands on the three verified cases (`lukanḍa`, `ṣaloon`, `tiṛamwaay`).
5. **§5: the Abdel-Massih romanization row was repeating Wikipedia's description of his system**,
   which correction 4 above records as wrong. Replaced with the system as printed in his books.
6. **§0: the Alqarhi quotation was overstated** ("de facto standard spoken dialect of the Arab
   world"); the source says "in certain segments of the Arabic speaking population", p.14 not p.9.
7. **§1/§3.6: `talaata` was on the wrong side of the /θ/ split** — it is Hafez's /t/ example.
8. **§6.3: the `-it` ~ `-et` construct vowel is now flagged as a CONFLICT** (Abdel-Massih vs
   Hafez) rather than silently normalized to `-it`.
9. **§8.5 no longer decides /sm sn/**, which §9.4 declares open; Broselow's own hedge ("and
   possibly some or all S-resonant clusters", p.295) supports leaving it open. /sl sr/ stay with
   anaptyxis, which her Cairene data does settle.
10. **§8.4's /əi/→/aj/, /əu/→/aw/ mapping is now tagged `(unattested)`.**
11. **attested.tsv: Hafez's `ç` was decoded two ways** (emphatic in `bââçâ`, plain in `çâlsâ`).
    Both now read /sˤ/, with the mojibake noted.
12. Smaller: the §2/§3.4 final-CC loan list no longer claims to come from §29/§32; `n → l`
    (journal) now records that Hafez's stated direction and her datum disagree; /g/ removed from
    the "no assimilation" list in §6.1; CVːCC re-attributed to Khalifa; the "no sonority
    hierarchy" wording re-attributed to Hassig's gloss; Galal, Abdel-Massih, Hassig, Broselow and
    Watson page pointers corrected where they had drifted.
13. **Citation key `lapsyd-arz` corrected to `lapsyd arabic-egy-arz`** — the bib key is `lapsyd`
    and the file lives in `../infra/`, not in this directory.

**Reported by the review but NOT applied — the review was wrong, verified against the sources:**
- *"§3.7's `/ʃugl ʔibnak/ → ʃugli ʔibnak` is an invented output form; Broselow shows the glottal
  stop deleting."* — It is not invented. broselow1976 (87a) prints `sugl` + raised epenthetic
  vowel + `?ibnak ~ sugl ibnak`, and the following sentence reads: "In the forms of (87) an
  initial glottal stop is counted as a third consonant, triggering the application of I Ep."
  The digest's claim and its ordering point are both correct; only the page was widened to 25–26.
- *"§3.8's closed-syllable-shortening examples are not in the source."* — The reviewer checked
  only broselow1976. The citation was a joint one: `kitaab+na → ki.tab.na` is
  broselow-arabic-syll ex.(6), and `baab+ha → babha` / `kaatib-a → katba` are
  watson2007-syllabification p.340, both verified. The examples have now been attached to their
  individual sources so the joint citation cannot mislead again.
- *"§4's `sibita`/`numura` broken-plural sub-exception is not in Abdel-Massih; it is Watson
  p.3004."* — It **is** in Abdel-Massih, verbatim, at v3 p.254: "primary stress is usually on the
  penult if the structure CVCVCVCC constitutes a broken plural form with identical high vowels in
  the first two syllables, e.g., sibíta 'baskets', numura 'tigers'." Retained. (The reviewer was
  right that `ʕarabi` did not belong in his antepenult list; it is now `inkasarit`.)

## Process notes

Extraction was split across seven sub-agents, one per source cluster (Hafez; Hassig; the Broselow
set; Galal+Khalifa+Aquil; the stress set; the Abdel-Massih volumes; Wikipedia, done by the lead).
Sub-agents wrote cited findings files to a scratchpad; none wrote into this directory. Two
extractions were spot-checked by the lead against the PDF page images — Galal's two data sets
(pp.2–3), because the `.txt` garbles several forms, and the Khalifa coda/onset statements
(pp.92–99), because bib.md flags the venue as low-selectivity. Both checked out; the Galal forms
in `attested.tsv` are the PDF readings, not the `.txt` ones.
