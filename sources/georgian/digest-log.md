# Digest log — Georgian

## Which source fed which section

| Section | Primary | Secondary / cross-check |
|---|---|---|
| §0 scope | `shosted2006` | PHOIBLE row 2183 |
| §1 inventory | `shosted2006` (the JIPA Illustration; read in full) | `wiki-ka §Phonology`, `wiki-help-ipa-ka`, `butskhrikidze2002` §3.2–3.3 |
| §2 phonotactics | `butskhrikidze2002` Appendices 2 & 3 (**re-read from rendered PDF pages**), §3.5.1–3.5.2, §3.4, §2.1.2–2.1.3 | `mccoy1999`, `butskhrikidze-vanheuven-avt18`, `crouch2022-diss`, `crouch2023-intrusive-vocoids`, `wiki-ka §Phonotactics`, `self-syncope` |
| §3 repair | `gabunia2021` | `ka-wiki-title` harvest (see caveat below), `rayfield2023`, `georgian-accented-speech` (corroboration only) |
| §4 stress | `borise2023` | `jun2007` (both files), `butskhrikidze2002` §2.1.2.5/§2.1.3.3/§6.3, `wiki-ka §Prosody`, `peacecorps` |
| §5 romanization | `ungegn-georgian` | `wiki-ka-romanization`, `wiki-help-ipa-ka`, `peacecorps` |
| §6 morphology | `wiki-ka-grammar`, `wiki-ka-name` | `self-syncope`, `shosted2006` p.261 (the -uri/-uli dissimilation) |
| §7 attested | `gabunia2021` App. B (34 rows) | `ka-wiki-title` harvest (88), `rayfield2023` (15), `kirvalidze2017` + `asaturova-garibashvili` (6) |
| §8 mismatches | derived from §1–§3 + Appendix 2/3 | — |

Not used, and why:
- `begus-caucasian` — read for §1; adds nothing `shosted2006` does not say more directly about
  Georgian specifically. No citation made.
- `brosset1837` — not opened. Pre-IPA French grammar; bib.md already flags it as unusable for
  phonetics, and §6 was fully covered by `wiki-ka-grammar`.
- `linguo-cultural-pragmatic-loanwords` (Kirvalidze 2017) and `problems-regulating-english-loanwords`
  (Asaturova & Garibashvili) turned out to be **more useful than bib.md predicted**, and are cited
  in §3 and used for 6 rows of `attested.tsv`. Kirvalidze independently transcribes the ფ of loans
  as `[p]` (*flirti* [plɪrtɪ], *fantastiuri* [pantastiurɪ]), which is the strongest corroboration
  of /f/ → /pʰ/ outside `gabunia2021`; and she gives the same transphonemization typology and the
  same Russian-mediation examples, from the same source lineage. Asaturova & Garibashvili state no
  phonological rules at all, as bib.md says, but their 39 Georgian–Russian–English triples are
  usable evidence for which loans are Russian-shaped.
- Chapters 1, 4 and 7 of `butskhrikidze2002` — theory/experiment/literature-review, skipped per
  the project's "ignore theory" rule, except that ch.4's perception result is reported in §2.2
  because it bears directly on whether harmonic clusters should be transcribed as one segment or
  two.
- OT machinery in `self-syncope` — discarded entirely per project rules; only the descriptive
  generalization and the example words were taken.

## Things that turned out to be mis-described, or that a re-reader must know

1. **`butskhrikidze2002.txt` is unusable for any cluster data.** bib.md notes the PDF is fine but
   does not flag the extraction. The PDF embeds a phonetic font that `pdftotext` decodes against
   the wrong mapping, and **the mapping is not stable across the document** — `X` decodes as `χ`
   in one line and as `u` in the next; whole words come out as `äJHQWL`, `åULDPXOL`, `þRQþ[-i`.
   One passage even decodes as ROT-3. Appendix 2 (pp.197–205) and Appendix 3 (pp.207–209) were
   therefore re-read from **rendered PDF page images**, not from the .txt. **PDF page = thesis
   page + 14.** Anyone re-checking §2 must do the same.
2. **Butskhrikidze's transcription is not IPA and the thesis says so only once**, in the alphabet
   table at pp.76–77: plain `p t k c č` are the *aspirated* series, `'` marks ejectives, `χ'` is
   her symbol for /qʼ/, `x` her velar fricative, `γ` /ɣ/, `ʒ` /dz/, `ǰ` /dʒ/. Reading the
   appendices as IPA gives the wrong laryngeal series everywhere.
3. **bib.md's chapter map is accurate**, with one addition: Appendix 1 (p.193) is Ertelishvili's
   nominal/verbal *stem-type* counts (CVCC 27.5%, CVC 25.9% of 2764 monosyllabic nominal stems) —
   useful for calibrating output shape, and not mentioned in bib.md.
4. **The bib.md claim that Chitoran (1998)'s harmonic-cluster inventory is "substantially
   recovered" is correct and can be strengthened**: `wiki-ka §Harmonic clusters` reproduces
   Chitoran's 12-cluster table in full with Georgian examples, so the canonical list is available
   directly, not only at second hand.
5. **bib.md's description of `butskhrikidze2002` §2.3.2 as "Sonority Sequencing in Georgian +
   Zubkova (1990) statistics" is misleading.** Zubkova (1990) is a cross-linguistic study of 11
   languages (Russian, Czech, Tadjik, Indonesian, Javanese, Tagalog, Turkish, Mongolian, Nanai,
   Japanese, Vietnamese) — **Georgian is not in her sample**. The only bearing on Georgian is one
   remark that prefixing languages tend to violate the SSP and "the same effect is attested in
   Georgian" [butskhrikidze2002 p.65]. There are no Georgian cluster-frequency statistics in this
   source set at all.
6. **`borise-stress.pdf` carries the journal's unedited template header** ("Volume 1, Article 3
   (2019)", dummy author names) — bib.md flags this and it is correct; cite the real details.
7. **`shosted-chikovani2006.txt` is in SIL IPA93 legacy encoding**, not Unicode: `Ó`=ʰ, `|`=ɾ,
   `A`=ɑ, `E`=ɛ, `O`=ɔ, `S`=ʃ, `Z`=ʒ, `G`=ɣ, `X`=χ, `/`=ʔ, `F`=ɸ. Readable once you know, but
   `grep` for IPA characters will find nothing.
8. **`ka-wiki-name-transliterations.tsv` contains more translation rows than bib.md's two
   examples suggest.** Discarded as translations or native-form substitutions rather than
   transliterations: Alexander the Great, Charlemagne, Christmas, Denmark (*dania*), England
   (*inglisi*), France (*sakartvelo*-pattern *sapranget-i*), Germany, Iceland, Ireland,
   Netherlands, Norway, Portugal, Spain, Star Wars, Sweden, Switzerland, Jerusalem, Kyiv
   (Russian *kievi*), Joseph Stalin (native *ioseb*), Julius Caesar (*keisari*), Elizabeth II
   (native *elisabed*), Napoleon (title added), Brussels (disambiguator), Michael Collins
   (disambiguator), Éamon de Valera (*imon*, unexplained), plus four rows left in Latin script
   (Facebook, Google, Microsoft, The Beatles) and one broken row (President). Finland (*pineti*)
   was **kept** despite being a native derivation, because the stem *pin-* is a direct
   transliteration showing /f/ → /pʰ/.

9. **`anglicisms-leiden2021` Appendix B is on PDF pp.50–51, not 51–52** as bib.md says. The `.txt`
   extraction of the table is faithful; the only thing it loses is that the `h` of `kh th ph` is
   **superscript** in the PDF (= /kʰ tʰ pʰ/). Two errors are in the published PDF itself, not the
   extraction: the *Chat* row is labelled `Geo-like` **twice**, and the *Like* row has its labels
   **swapped** relative to every other row (the ejective is tagged `Eng-like`). The column heading
   is misspelled "Pronunciaiton" in the original.
10. **bib.md attributes the ჶ *fi* claim to `gabunia2021`; she never mentions ჶ.** What she
    discusses is the 20th-century use of the **Cyrillic** ф in Georgian print (Journal *Iveria*,
    1877–1905), "later rejected" [gabunia2021 p.15]. Rayfield never mentions ჶ either. The ჶ
    facts in §1.4 come from `wiki-ka-scripts`, not from the loanword sources.
11. **`gabunia2021`'s prose on /ŋ/ contradicts her own data.** The prose says /ŋ/ "is substituted
    by /n/" [p.14]; every item in her Appendix B, and every corroborating source, gives **[nɡ]**.
    §3.2 takes the data. bib.md's summary ("/ŋ/ → /n/ or /ng/") reproduces the prose.
12. **`georgian-accented-speech` is bibliographically identifiable**, which bib.md leaves open:
    Sopio Zhgenti, *The Most Common Pronunciation Mistakes in Georgian-Accented Speech and the
    Issue of Intelligibility*, MA dissertation, Universiteit Leiden, 18 June 2015 — same
    supervisor (Dick Smakman) as `gabunia2021`. **Method caveat that limits its weight**: it is not
    an instrumental or transcription study. Fifteen judges listened to ten recordings of Tbilisi
    schoolchildren and wrote comments; the "substitutions" are what judges *reported hearing*
    (pp.32–35). It never uses the word *ejective* and gives no Georgian phoneme inventory. Its
    summary tables on pp.44 and 48 print two substitution directions **opposite** to its own prose
    — cite the prose. Used in §3 as corroboration only, exactly as bib.md advises.
13. **The /w/ rule in bib.md ("/w/ → /v/ (Georgian-like) or /u/ (English-like)") reproduces
    `gabunia2021`'s framing, which appears to be wrong.** Four sources' data fit a **positional**
    split — initial /w/ → /u/, medial /w/ → /v/ — including Gabunia's own *weekend* (u in both
    variants) and *forward* → *poruardi*. Set out as a `CONFLICT:` in §3.3 with a proposed
    resolution that no single source states.

## What I could not resolve

1. **No Russian→Georgian adaptation source exists in the open literature we could locate**
   (bib.md already says this). Consequence: **there is no attested precedent for how Georgian
   treats foreign palatalized consonants**, which is the single most important mismatch for this
   project (§8.1). The `Ci` spellings in the Wikipedia harvest (*brius*, *miunkheni*,
   *niu-iork'i*) are editorial transliteration practice, themselves usually Russian-mediated, and
   are cited as such — they are not evidence about Georgian speech.
2. **The `zg` / `žg` harmonic clusters** are listed in two of Butskhrikidze's own publications,
   footnoted as "almost unattested" in one of them, and marked impossible in her own
   co-occurrence table. Left as a `CONFLICT:` in §2.2.
3. **Table (62)'s row `š` omits `k`** while the harmonic-cluster table includes `šk`. An internal
   inconsistency in the thesis; flagged in §8.4, not resolved.
4. **Whether `/sn/` is a genuine gap or an artefact** of Appendix 2 being "not exhaustive"
   (§8.4). `zn`, `šn`, `xn` are all attested; `sn` is not. Cannot be settled from these sources.
5. **Maximum onset length: six vs seven vs eight** (§2.1). Depends on whether verbal prefixes
   /ɡv-/ and /m-/ are counted. Nobody in the source set acknowledges anybody else's figure.
6. **Syllabic sonorants: Butskhrikidze yes, Crouch flatly no** (§2.11). Both are recent and both
   argue from data. Left as `CONFLICT:`.
7. **`target_ipa` in `attested.tsv` for the `ka-wiki-title` rows is derived, not quoted.** The
   source (Georgian Wikipedia article titles) gives Mkhedruli only. The IPA column was produced by
   mechanical letter-by-letter transliteration, which is defensible because Georgian orthography
   is stated to be one-to-one with the phoneme inventory [shosted2006 p.255] — but it is a
   derivation, and the provenance field says so on every row. Do not treat those IPA strings as
   observed pronunciations; in particular they will not show the intrusive vocoids, cluster
   reductions, or the /qʼ/ → [ʔ] variation that real speech has.
8. **Nothing was found on how Georgian treats donor-side morphological alternations** (Irish
   initial mutations, genitives) — loans arrive as fixed citation forms. Left for the Irish
   digest (§8.5).

9. **Whether Gabunia's ejective norm is descriptively real.** Her 24 items are recent loans, and
   she explicitly excludes older Russian-mediated ones as "fully adapted" [gabunia2021 p.26]. So
   her 59.6%-aspirate result may be a fact about very new borrowings only, and the ejective may
   dominate the established lexicon. Nothing in the source set settles it.
10. **The one palatalized Georgian form in the entire source set** is *costume* →
    /kɔsʲtʲˈʉmi/, reported as a "partially Russian-like version" and excluded from Gabunia's study
    for that reason [gabunia2021 p.18]. It shows palatalization is sayable and heard as foreign.
    It is not a productive rule, and it is all we have (§3.8, §8.1).
11. **Stress in loans: unresolved and possibly contradicted.** Gabunia's initial-stress claim is a
    bare citation of Chikobava [gabunia2021 p.19]. `georgian-accented-speech` reports Georgian
    speakers shifting English stress **rightward** off the correct syllable (pp.43–44), which
    points the other way. Neither source tests loan stress directly.
