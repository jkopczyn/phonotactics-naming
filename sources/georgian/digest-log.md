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
  in §3 and used for 6 rows of `attested.csv`. Kirvalidze independently transcribes the ფ of loans
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
8. **`ka-wiki-name-transliterations.csv` contains more translation rows than bib.md's two
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
7. **`target_ipa` in `attested.csv` for the `ka-wiki-title` rows is derived, not quoted.** The
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

---

# Revision 1 (after `review.md`)

Review reported 30 verified / 7 misquoted / 8 overstated across 45 checks. All seven required
fixes in its §6 were worked. **Two of the review's own findings are themselves wrong** and were not
applied; both are documented below with the evidence, because they would have introduced errors.

## Method change

The whole of Appendices 2 and 3 (thesis pp.197–209 = PDF pp.211–223) and the alphabet table
(p.77 = PDF p.91) were **re-read from rendered PDF page images**, not sampled. The review was right
that a 2-error sample implied more; re-reading found the root cause and one further error of my own.

## Root cause of the transcription defects: the notation key was wrong

Butskhrikidze's alphabet table (1) [butskhrikidze2002 p.77] gives **ძ = `j` = [dz]** and
**ჯ = `ǰ` = [dʒ]**. My §0/§2 key had said "`ʒ` = /dz/, `ǰ` = /dʒ/". **`ʒ` is not one of her symbols
at all** (`ž` is her [ʒ]). So the review's "bare `j` is not one of the digest's declared symbols"
was correct about the symptom but backwards about the cure: the bare `j` in `jγ`, `jv`, `jrc'`,
`γrj` is **the source's own correct symbol**, and it was my *key* that needed fixing, not those
entries. §2.0 now reproduces the full table (1) with the four traps spelled out.

Errors this actually caused, now fixed:
- `grǰn` → **`grjn`** *grjnoba* 'feeling' (გრძნობა /ɡrdznɔba/) — CCCC list.
- `rǰl` → **`rjl`** *γvarjl-i* 'spite' — stem-final CCC list.
- `lǰ` → **`lj`** — Appendix 3's never-attested set.
- Harmonic table: `ʒg`/`ʒγ` → **`jg`/`jγ`**.
- Table (1) also shows she writes ხ as **[χ]** on p.77 (and [x] on p.87 — the inconsistency
  `shosted2006` p.258 flags), and ყ as **[χʼ]**. §2.0 records both.

## Other Appendix corrections found by the full re-read

- Added **`nj`** *sp'ilenj-i* 'copper' (Persian) to the stem-final sonorant+obstruent list — I had
  dropped it. All four of `nj nǰ rj rǰ` are on that list and are distinguished only by the caron.
- **`rp` is in Appendix 3's never-attested set (p.207) and simultaneously in its stem-final loan
  list (p.208, *šarp-i* 'scarf', French).** New `CONFLICT:` line.
- Three **printing defects in the source**, now reproduced as printed with a † note rather than
  silently normalized: `brg brke` / `brk brge` appear transposed; `zrd` is filed under
  *stop*+sonorant+stop; `črd` under affricate+sonorant+*fricative*.
- Appendix 3's own gloss on its scope — stem-final "**i.e. word-medial**" (p.207) — added; it bears
  directly on §8.6, and it argues *against* the bare-stem overlay.
- Full glosses added throughout the CC, CCC and CCCC lists (previously many were bare strings).
- Final-CCCC "pattern: /r/ + harmonic cluster + /v/" → the source's "**usually**", with its own two
  counterexamples named (`nčxl` begins in /n/; `rcxl` and `nčxl` end in /l/). Review §22 upheld.

## Disagreements — two review findings not applied

1. **Review §15: "digest's CCC list omits `t'χ'n`; p.201 lists `t'χ'n t'χ'lap'i`."**
   **Not applied.** Thesis p.201 (PDF p.215), class e) stop+fricative+sonorant, has exactly five
   entries: `bγv bγvera`, `txl txle`, `txr txroba`, `t'χ'v t'χ'via`, **`t'χ'l t'χ'lap'i`**. The
   gloss 'fruit cookie' belongs to **`t'χ'l`**. There is no `t'χ'n` on the page; the review appears
   to have read the final `l` as `n`. Adding `t'χ'n` would have put an unattested cluster into a
   deterministic whitelist.
2. **Review §16 / §5: "digest gives `č'k'n`; p.202 gives `c'k'n c'k'noba` — /tsʼ/ was changed to
   /tʃʼ/."** **Not applied.** Thesis p.202 (PDF p.216), class i) affricate+stop+sonorant, prints
   **`č'k'n  č'k'noba 'fade'`** with a visible caron, alongside `c'k'l`, `c'k'm`, `c'k'r`, which do
   not have one. Changing it as directed would have introduced the exact error the review was
   trying to prevent.

Both are recorded because a future editor working from `review.md` alone would otherwise re-break
these two entries.

## A third, larger disagreement: *Connacht*

**Review §43 and §22: "the row gives კონაქტი but IPA /kʼɔnɑkʰtʼi/; Georgian კ is /kʼ/, not /kʰ/;
the derived form is /kʼɔnɑkʼtʼi/, so §8.4's `/xt/ → /kʰtʼ/` precedent is also wrong."**
**Not applied — the premise is a letter confusion.** კონაქტი is კ-ო-ნ-ა-**ქ**-ტ-ი: the initial is
**კ** *kan* /kʼ/ and the medial is **ქ** *khar* /kʰ/. They are different letters (U+10D9 vs
U+10E5). The derived IPA /kʼɔnɑkʰtʼi/ is correct as it stood, and `/xt/ → /kʰtʼ/` follows.

I did act on the review's *general* point about this datum, which is sound: §8.4 now weights it
low — one editorial spelling of one word, and `kʰtʼ` is not itself a harmonic cluster, so the
adaptation does not satisfy §2's stem-final restriction either. It is presented as suggestive, not
as a rule.

To stop this recurring, all 88 `ka-wiki-title` IPA strings were **re-derived mechanically** from a
stated letter→IPA table (now printed in §7), and the table's კ/ქ distinction is called out there.

## Everything else in review §6, as applied

| Required fix | What changed |
|---|---|
| Appendix transcription | §2.0 added (full alphabet table + four traps); `grjn`, `rjl`, `lj`, `jg/jγ` corrected; `nj` restored; CCC/CCCC lists re-issued complete with glosses and † source-defect notes; final-CCCC de-generalized |
| Six-slot template not the whole grammar | §2.4 rewritten: it is a **generator of canonical long clusters**, with the four classes it does not generate named (/s/+C, /r/+C, sonorant+obstruent, the loan set) and her own four-way summary (66) quoted |
| §3.0/§3.7 repair headline | Retitled "**no cluster repair is observed in this dataset**"; a bounded-negative-result paragraph added, noting Gabunia's items were selected for /p t k w f eɪ/ and that **the corpus contains no input Georgian would reject**, so its silence says nothing about illicit clusters; safe-vs-unsafe implementation stated; §3.7 gains a coverage check showing every cluster in the list is independently licensed by §2 |
| Geo-like/Eng-like labels | "nativized/prestige" removed everywhere except the paragraph that explains why it was dropped; §3.1 retitled and opens with Gabunia's four actual labels; **OPEN DECISION** block added saying which column to implement is a project choice, not her result |
| Percentages as tendencies | The categorical "after a consonant, ejective; between vowels, aspirate" is withdrawn with a `CONFLICT:` line quoting her "still too small to make any assumptions" and "merely presenting the tendencies"; "plosive+labial **blocks**" → disfavours; within-word harmony marked as observed in 3 of 24 items |
| §5 five-name assessment | §5.2 replaced by a **literal parse** table whose verdict is that **none of the five is readable** under the national system, listing the exact non-national conventions each needs; the backwards *Kas'queil* and *Th'tysh* analyses are withdrawn and the standard's consonant-then-apostrophe direction is restated; `tch` ≈ `t'ch` equivalence withdrawn; `aeu` requalified as violating *native monomorphemic* phonotactics only, per §2.9; §5.3 relabels D1–D4 a **project overlay on the national base**, with D5 noting that following the standard respells *Kas'queil* → *Kasq'ueil*; an honest "poor matches" summary added |
| /h/ and *Stockholm* | §8.2's "delete elsewhere" **withdrawn**; new `CONFLICT:` — *Stockholm* /stʼɔkʼhɔlmi/ and *Beethoven* /bɛtʰhɔvɛni/ both put /h/ in a cluster, while the one deletion (*Tehran*) is intervocalic, i.e. the position the native rule allows, so the old rule was backwards relative to its own data. Marked unresolved; §9 gains an entry |
| `/st/` | §8.4 no longer calls it cluster repair: the cluster is retained and only the stop series changes, so it belongs to the §3.1 rule and must not be encoded separately; "single most reliable repair" withdrawn; *casting* → კასტინგი noted as a counterexample |
| attested.csv — Gabunia | 24 Appendix-B rows now say in `provenance` that `target_ipa` is as printed but the **Mkhedruli `target_form` is DERIVED** (Appendix B gives IPA only) |
| attested.csv — donor language | `source_lang` on all 88 wiki rows changed `eng` → **`und`**; provenance now reads "en.wikipedia article title = editorial source string, NOT a known historical donor form; mediation unknown/mixed"; asserted routes in notes softened to "(route inferred)" |
| attested.csv — IPA defects | *O'Connor*'s ASCII apostrophe → word boundary; three hyphens → boundaries; all 88 re-derived from the stated table |
| attested.csv — nominative -i | All 63 rows tagged `epenthesis` now begin their `note` with "nominative -i = morphological case suffix, NOT phonological epenthesis". The tag itself is kept for schema compliance (`ATTESTED-FORMAT.md` has no morphological tag) and §7 gains a numbered disclosure warning that **no row in the file instantiates phonological epenthesis** |
| Overlays and OPEN DECISIONs | §9 gains a summary table listing all nine — bare-stem output, `y`=/i/, `x`/`tch`, positional /w/, Irish diphthongs, /ə/, palatalization options A–D, ejective default, word-level harmony — each with its evidential status. Individually tagged in place: §3.1, §3.3, §8.1, §8.2, §8.3, §8.6, §5.3 |
| Under-cited inferences | `(unattested)` added to the positional /w/ rule, the Irish diphthong mappings, /æ/→/ɛ~ɑ/, /ʌ/→/ɑ/, and the /ə/ fallback; /ð/ → /t d z/ flagged as prose-only with no example anywhere in the source set |
| §6.1 bare stem | "*k'ats-* is as much a Georgian word-form as *k'atsi*" **withdrawn** — a bare stem is a bound form; what the source licenses is the weaker point that the stem's segmental material is well-formed Georgian. The -i rule's scope narrowed to "the right edge of the inflected nominal", and a new `CONFLICT:` records that no source explains why native consonant-final personal names (Davit, Tamar) escape it |

## Still unresolved after Revision 1

The review's §5.2 point — that native stem phonotactics, ordinary inflected word forms, and
editorial foreign-name transliteration are three different objects with different edge and /h/
behaviour — is now stated (§8.2, §9.12) but **not** worked through into three separate licitness
tests. A rule writer building one combined test will still get the edges wrong. That is the largest
remaining gap in this digest.
