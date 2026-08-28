# digest-log — Irish (source side) + Old Irish

Written 2026-08-24. Companion to `digest.md` and `test-words.csv`.

## Which source carried which section

| Section | Primary | Secondary / cross-check | Unused for this section |
|---|---|---|---|
| §0 variety | `wiki-help-ipa-irish` §Comparison of transcription schemes | user's own transcriptions in `../../notes/project-goals.md` | — |
| §1.1 consonants | `wiki-irish-phonology` §Consonants, §Allophones, §On- and offglides, §Fortis and lenis sonorants | `wiki-help-ipa-irish` §Consonants + notes 1–10; `nichasaide1999-ipa-irish` p.112–113 (Ulster) | `quiggin1906-donegal` (notation cost) |
| §1.2 vowels | `wiki-irish-phonology` §Vowels, §Vowel backness, §Nasalized vowels | `nichasaide1999-ipa-irish` p.114–115; `wiki-help-ipa-irish` §Vowels | — |
| §2.1 syllable shapes | assembled by inspection from the ~550 harvested word+IPA pairs | `green1997-prosodic-goidelic` pp.55–56 | no source states an Irish maximal-syllable formula |
| §2.2 onsets | `wiki-irish-phonology` §Word-initial consonant clusters; `wiki-clusterchart-2C_cluster_nonmut.svg`, `-2C_cluster_mut2.svg` | `green1997-prosodic-goidelic` pp.55–56, 143–149 | Ní Chiosáin 1999 (paywalled, not held) |
| §2.3 codas | **`green1997-prosodic-goidelic` pp.55–56, 136–146** | `wiki-irish-phonology` §Post-vocalic consonant clusters | Wikipedia has no final-cluster list |
| §2.4 epenthesis | `wiki-irish-phonology` §Post-vocalic…; `wiki-clusterchart-Epenthesis_cluster.svg`; **`green1997-prosodic-goidelic` pp.149–154**; `wiki-irish-orthography` §Epenthesis | `irish-schwa-kwpl` §§4–5; `quiggin1906-donegal` §111, §138ff | — |
| §3 mutations | `wiki-irish-mutations` §Summary table, §Environments…, §Changes to vowel-initial words | `wiki-irish-orthography` §Grapheme to phoneme correspondence (for the attested IPA of every mutated form) | — |
| §3.5 gen./voc. | `wiki-irish-declension` §Declension, §Vocative | `wiki-irish-orthography` (attested *mac/mic*, *caisleán/caisleáin*) | — |
| §3.6, §6 epithets | `wiki-irish-declension` §Adjectives; `wiki-irish-mutations` §After preposed adjectives / §After most prefixes / §The second part of a compound; `wiki-irish-name` §Ó and Mac surnames, §Epithets, §Traditional Gaeltacht names | — | — |
| §4.1 stress | `wiki-irish-phonology` §Stress, §Compound words, §Munster; **`green1997-prosodic-goidelic` pp.94, 121–125**; `green-munster-stress` pp.3–5 | `rowicka-munster-stress` pp.2, 6–8; `kukhto2019-munster-stress` pp.1565–1568; `nichasaide1999-ipa-irish` p.115 | — |
| §4.2 length/weight | `wiki-irish-phonology` §Lengthening before fortis sonorants, §Devoicing; **`green1997-prosodic-goidelic` pp.72–77, 94, 121** | `rowicka-munster-stress` p.2 | — |
| §5 orthography | `wiki-irish-orthography` §Vowels, §Letters and letter names, §Alphabet, §Epenthesis, §Diacritics | `wiki-help-ipa-irish` (full IPA key read directly) | — |
| §7 test set | `wiki-irish-orthography` §Grapheme to phoneme correspondence; `wiki-irish-phonology` (all cluster/epenthesis/compound sections) | `irish-schwa-kwpl` p.5 (the 15 near-minimal pairs) | `wiki-irish-name` — **no IPA at all** |
| §8.1 broad/slender | **`nichiosain2018-ultrasound-connemara` pp.5–7, 31–33** (Connemara ultrasound); **`bennett-syllable-position-irish` §7.1**; `bennett-gestural-timing-irish` §3.2, §9, p.38 | `wiki-irish-phonology` §On- and offglides; `nichasaide1999-ipa-irish` p.113 | — |
| §8.2 voiceless sonorants | `quiggin1906-donegal` §§213, 220, 227, 232, 242, 248, 259, 264, 279, 288; `nichasaide1999-ipa-irish` p.113 | — | none of the three UCSC papers mention them |
| §10 Old Irish | `wiki-old-irish` (inventory, orthography, stress); `wiki-old-irish-grammar` (mutations, declension, adjectives); **`pokorny1914-oldirish-grammar` pp.5–20, 43, 56, 59–72** (glide rules, apocope/syncope, trigger lists, paradigms); `strachan1909-oldirish-paradigms` pp.1–20 (paradigms + the attested name list) | `utaustin-oldirish-lesson1` §§1.1, 1.2, 2.1, 2.2; `utaustin-oldirish-intro` | `wiki-old-irish-phonhistory` — see below |

Files in this directory that contributed **nothing** to the digest:
`ocuinneagain-thesis-irishenglish` (as `bib.md` already flagged, it is a sociolinguistic study of
Irish-English, not a description of Irish). `quiggin1906-donegal` was used for two facts only and its
1906 notation was not converted.

## Things `bib.md` describes incorrectly

1. **`wiki-old-irish-phonhistory` does not cover Old Irish → Modern Irish.** `bib.md` says it covers
   "the systematic correspondences between Old Irish and Modern Irish forms" and that "that
   correspondence set is what lets strand 5 be generated from the same Irish lexicon as the
   other four." The article is entirely **Proto-Celtic / Primitive Irish → Old Irish**; its one
   forward-looking sentence is that nasalization "gave rise to the eclipsis mutation in modern
   Irish". **This is the most consequential correction in this digest** — see §10.7, which
   proposes eDIL lookup instead of derivation.
2. **`bib.md`'s summary of the mutation outputs is slightly off** where it lists lenition
   /bˠ→wˠ~vˠ/ and /mˠ→wˠ~vˠ/. The mutations article gives a single phonemic output **/w/**
   (broad) / **/vʲ/** (slender) with no dialect split; the [w]~[vˠ] split is stated in
   `wiki-irish-phonology` §Allophones as **allophony of /w/**, and it is positional in Connacht
   ([w] initially, [vˠ] elsewhere), not free variation. Digest §3.1 flags this as a CONFLICT.
3. **`bib.md` says the project-goals note's "Irish lenition outputs [v w j h] and voiceless
   sonorants" is a fact about the inventory.** Half of it is: [v w j h] (plus /ɣ x ç/) are real
   phonemic lenition outputs. **The voiceless sonorants are not.** No source describes them as
   contrastive segments; Quiggin documents them as arising from historical sonorant + *th*/*f(h)*
   clusters, mainly in the **future tense**, and Ní Chasaide as allophonic devoicing next to
   voiceless plosives and prepausally. §8.2 recommends keeping them out of the input inventory.
4. **`green1997-prosodic-goidelic`'s PDF is 10 physical sheets but the complete dissertation**, as `bib.md` says —
   confirmed. The `.txt` page numbers cited in the digest are the *logical* page numbers visible
   in the extracted text, not sheet numbers.
5. `bib.md`'s note that `nichasaide1999-ipa-irish.txt` OCR mangles the IPA superscripts is correct; the
   consonant and vowel tables were read from the **PDF**.

## CONFLICT lines in the digest

| # | Where | The disagreement |
|---|---|---|
| 1 | §2.4 | Epenthesis blockers: `wiki-irish-phonology` gives long-vowel + ≥3-syllable; `wiki-irish-orthography` gives long-vowel + morpheme-boundary (and carries an "uncited" banner). **Resolved by `green1997-prosodic-goidelic`**, which supplies both plus homorganicity, and shows the ≥3-syllable blocker is **Connacht-specific** (Munster and Ulster epenthesize in long words). |
| 2 | §3.1 | Lenition of ⟨bh mh⟩ / ⟨dh gh⟩: `wiki-irish-mutations` gives a single phonemic /w/, /ɣ/; `wiki-irish-phonology` gives the [w]/[vˠ] realization as dialect- and position-conditioned. Phonemic vs. allophonic — both kept. |
| 3 | §4.1 | **Why -ach attracts Munster stress**: `green1997-prosodic-goidelic`/`green-munster-stress` posit underlying schwa in σ1 *and* special /ax/ prominence; `kukhto2019-munster-stress` pp.1566–1568 argues the /ax/ mechanism is unnecessary (counter-example *macalla* [maˈkalə]). **Both predict the same surface stress**, so the tool need not choose. |
| 4 | §4.1 | **The Munster three-syllable stress window.** `green1997-prosodic-goidelic` p.123 depends on it; `green-munster-stress` p.3 reports Gussmann (1995) finding 4th-syllable stress "thereby disproving" it; `rowicka-munster-stress` pp.7–8 also predicts non-window patterns. Three-way disagreement on *imigéiniúla*: penultimate (Gussmann, Rowicka) vs. antepenultimate (`green1997-prosodic-goidelic` p.125 fn.18, citing Ó Sé p.c. and calling Gussmann's citation unreliable). `rowicka-munster-stress` p.6 further disputes that initial stress is the Munster default at all. **Only bites if the reference dialect is switched to Munster.** |
| 5 | §10.1 | **Old Irish consonant quality: two-way or three-way.** `wiki-old-irish`/`wiki-old-irish-phonhistory` = broad/slender; `pokorny1914-oldirish-grammar` pp.13–14 §35 = palatal / neutral / **rounded (u)**. The three-way system is what generates the ⟨-iu -eo -eu -au⟩ spellings. |
| 6 | §10.1 | Old Irish fortis/lenis sonorants are phonemic in `wiki-old-irish` and `pokorny1914-oldirish-grammar` §7, **absent from `utaustin-oldirish-lesson1`'s chart**. |
| 7 | §10.1 | Value of lenited *b*, *m*: /v ṽ/ vs. /β β̃/ vs. [w̃]. Notational. |
| 8 | §10.4 | Article's final ⟨-d⟩: `wiki-old-irish-grammar` says before "a vowel, a liquid, *n*, or *f*"; `pokorny1914-oldirish-grammar` p.59 §132 says before vowels or **aspirated** *f l n r*. |
| 9 | §10.8 | **⟨aí⟩ vs. ⟨ái⟩.** `pokorny1914-oldirish-grammar` p.6 §4 writes *aí (áe)* **explicitly to distinguish it from long *á* + palatal glide**; `wiki-old-irish` agrees. `utaustin-oldirish-lesson1` §1.1 writes *ái (áe)* — on Pokorny's convention that spells a different thing. **Matters for spelling names.** |

## What could not be resolved

1. **The Irish cluster inventory has a single source.** Every licit-onset statement traces to
   Ní Chiosáin 1999 (paywalled, not held). Wikipedia and the three Commons SVGs are all we have;
   `green1997-prosodic-goidelic`'s independent table (pp.55–56) agrees with them but is coarser. **We have the
   lists but not the author's own conditions, exceptions, or statement of what is excluded.**
2. **The three Commons cluster charts have their text converted to paths** — no extractable
   labels. They were rendered to PNG with ImageMagick and read visually. The transcriptions in
   §2.2 and §2.4 are therefore my reading of images, not text extraction. They agree with the
   article prose everywhere I could check, but a second reading would be cheap insurance.
3. **No exhaustive list of licit word-final clusters from a Modern Irish descriptive source.**
   `green1997-prosodic-goidelic` p.55 gives one and it is the best available, but it is stated inside a prosodic
   analysis and its notation is pre-IPA (′ for slender).
4. **No IPA for Irish personal names anywhere in this source set.** `wiki-irish-name` has two
   large tables of names and zero pronunciations. eDIL has no bulk download or API. Hence 20
   constructed rows in `test-words.csv`.
5. **Noun+noun compound lenition in Modern Irish** (the *Lasairchos* case) is unattested here.
   Old Irish **does** state it (`pokorny1914-oldirish-grammar` p.8 §16: "in the interior of nominal compounds
   aspiration takes place… after nouns"), so §10.5 gives the modern case an ancestor, but the
   modern sources are silent.
6. **Whether /ˈkɪə.ɾˠə/ for *Ciara* is deliberate.** The spelling ⟨Cia-⟩ and the attested
   *ciall* /ciəl̪ˠ/ predict a **slender** /c/ + /iə/, i.e. /ˈciəɾˠə/. The user's transcription
   has broad /k/ + /ɪə/. Flagged as §9.2 rather than silently corrected.
7. **`quiggin1906-donegal` was not converted.** Its 1906 notation would need a transcription key before
   its dialect detail could be used; only two facts were taken from it.
8. **Munster syllabification detail** (`green1997-prosodic-goidelic` pp.147–149: no cluster licensed at a plain
   syllable edge, only stop+liquid at a foot edge) is stated inside a prosodic-licensing
   analysis. The digest reports the input→output generalization (Munster epenthesizes more) and
   the examples, and drops the machinery, per the brief.

---

# Revision 1 — response to `review.md`

Adversarial cross-family review (26/30 verified, 1 misquoted, 3 overstated). All eight required
fixes applied, plus the four suggestions. **Where this section conflicts with the text above, this
section wins**; the superseded statements are named below rather than silently edited out.

## Required fixes

**1. Coda-inventory contradiction (review §4.1, §6.1).** The review is right and §9.5 was wrong.
`green1997-prosodic-goidelic` pp.55–56 **does** supply a closed licit-coda inventory. §9.5
rewritten: it now names the held baseline and lists what is genuinely missing instead —
(a) independent confirmation, (b) a statement of dialect scope, (c) surface vs. underlying
word-final realizations. **Supersedes** the old §9.5 "assembled by inspection" and the
digest-log "What could not be resolved" item 3, which should now be read as "single-sourced and
dialect scope unstated", not "does not exist".

**2. §8.2 /ɣ/ and /h/ (review §4.3, §4.4, §6.2).** Both were errors of mine.
- **/ɣ/ source corrected to lenition only.** Eclipsed /d̪ˠ/ → /n̪ˠ/ and /ɡ/ → /ŋ/ (§3.2), so
  eclipsis is not a source of /ɣ/. The row now says so explicitly, and the same correction is
  applied to the /j/ row (also lenition-only). New test rows *ndroim* /n̪ˠɾˠiːmʲ/ and
  *nglúin* /ŋl̪ˠuːnʲ/ make the correct eclipsis outputs testable.
- **/h/ sentence rewritten.** "Every target has /h/ except Georgian (which has /h/)" was
  self-contradictory nonsense. Replaced with a source-side statement (what produces /h/, how
  often, that it elides intervocalically) and an explicit hand-off of the target question.

**3. Overstatements downgraded (review items 13, 21, 24 / §6.3).**
- **Item 24, coda neutralization.** Recast as an explicitly fictional target-side design option.
  §8.1 now states that Padgett et al. report **gradient articulatory weakening** and treat Irish
  as retaining the contrast in codas, that no categorical Irish coda neutralization is documented,
  and that the data can *motivate* a simplification but must not be presented as transferring an
  Irish rule. The option-5 contradiction the review caught (option 5 dropped quality in codas
  including coronals, contradicting the place ranking two paragraphs above) is fixed: any
  coda-only simplification applies to labials and dorsals only.
- **Item 21, "every word".** Replaced with "every consonant except /h/ comes in a pair"
  (which is what the source says) plus an explicit note that vowel-only and vowel-initial words
  display no quality, marked as a digest generalization.
- **Item 13, morpheme-boundary blocker.** Now labelled **PROVISIONAL** and separated from the
  four Green-confirmed blockers. I also checked the three cited examples and found only
  *garmhac* and *an-chiúin* actually bear on it — *carrbhealach* is independently blocked by its
  long vowel. That is noted in §2.4 and on both test rows.

**4. Citation keys (review §1 "Citation-form defect", §6.4).** Every key in all three files
normalized to the exact `bib.md` key: `green1997-prosodic-goidelic`, `green-munster-stress`,
`rowicka-munster-stress`, `kukhto2019-munster-stress`, `nichasaide1999-ipa-irish`,
`nichiosain2018-ultrasound-connemara`, `bennett-syllable-position-irish`,
`bennett-gestural-timing-irish`, `quiggin1906-donegal`, `pokorny1914-oldirish-grammar`,
`strachan1909-oldirish-paradigms`, `utaustin-oldirish-lesson1`, `utaustin-oldirish-intro`,
`wiki-old-irish-grammar`, `wiki-old-irish-phonhistory`, and the three cluster charts as
`wiki-clusterchart-2C_cluster_nonmut` / `-2C_cluster_mut2` / `-Epenthesis_cluster`. Bare
`project-goals` → the path `../../notes/project-goals.md`, since it is not a bib.md entry at all.

**5. Representation level defined (review §3 "Feature-tag vocabulary", §5.2, §6.5).** New
**§8.6** states the policy once: the **`ipa` column is verbatim as the source printed it**;
**`features` tags name underlying phonemes of the Connacht/standard system of §1.1.** Consequences
for the adapter and for `std` vs `C/M/U` fixtures are spelled out there. Every flagged row fixed:
- *Ciara* — `dip:iə` kept (correct under the underlying-phoneme policy for a surface [ɪə]) with a
  TAG NOTE on the row.
- *Diarmaid* — `seg:ɾˠ` **removed**. The source prints plain ⟨r⟩ and unmarked ⟨m⟩; the row now
  asserts no `seg:` tag for either and says why.
- *tobac* — `str:initial` → new tag **`str:exceptional`**. The review is right that it was the
  opposite of the cited fact.
- **`seg:d̪ˠ` added** and applied to the 12 rows that contain /d̪ˠ/ but no /t̪ˠ/ (*ard, dorn,
  dubh, dorcha, dualgas, Dónall, bádóir, droim, Ard-Easpag, ardnósach, droch-dhuine,
  drochbhéasach*).
- **L/N aliasing documented**, not silently applied: rows whose source string prints /lˠ l̠ʲ nˠ
  n̠ʲ/ keep it and carry a TAG NOTE. New tag **`seg:fortis-lenis`** marks the two rows whose
  point *is* that contrast, with the note that they are intentionally inapplicable under the
  two-way normalization.
- **`syl:medialCC` added** and separated from `syl:codaCC` (*Pádraig, caisleán, caisleáin,
  sneachta, dualgas* reclassified).
- A mechanical consistency checker was run over all 144 rows: every `seg:` tag's segment is
  present in the row's `ipa` (modulo the documented aliases), every `dip:` tag's diphthong is
  present, and every `len:V` row contains ⟨ː⟩. **0 mismatches.**

**6. Constructed rows (review §2.6, §3, §5.4, §6.6).** The claim that every constructed row
names its model **was false** and is removed. Provenance is now a machine-filterable tag:
`src:attested` (113) / `src:constructed` (14, model named) / `src:provisional` (13) /
`src:user` (3) / `src:inferred` (1). All rows the review found under-supported are demoted to
**`src:provisional`** with a note naming what is unmodelled: *Rónán, Oisín, Úna, Máire, Séamus,
Dónall* (no model at all), *Aoife, Pádraig, Cathal, Tadhg, Gráinne, Saoirse, Ní Bhriain* (partial).
§7 states they are examples, not regression truth, and should be excluded from pass/fail runs.
**Connacht *Niamh* resolved** by splitting it into two rows — `std` /nʲiəw/ (pan-dialectal
phoneme) and `C` [nʲiəvˠ] (Connacht realization, per *naomh* [n̪ˠiːvˠ]). *dubh* given the same
two-row treatment with the conflict named on both rows, per review §4.8.

**7. *Ciara* (review §3 "*Ciara* verification", §6.7).** The slender-/c/ conclusion is kept and
now stated as a **source-backed diagnosis** (caol le caol + the /iə/-after-broad restriction).
The complete form **/ˈciəɾˠə/ is labelled inferred**, not attested, with the explicit note that
no held source gives any pronunciation for the name. Both forms are in the TSV: the user's as
`src:user`, the reconstruction as `src:inferred`.

**8. §3 test coverage (review §3 "rules with no test instantiation", §6.8).** The single biggest
content gain of this revision. I had missed that **`wiki-irish-mutations §Summary table` carries a
full radical/lenited/eclipsed exemplar triad *with IPA* for every mutable initial** — it was in
the file all along and my first pass harvested only the orthography and phonology articles.
Adding it takes the file from 102 to **144 rows** and closes every gap the review listed:
- Lenition /fˠ fʲ → ∅/: *fhreagra* /ɾʲaɡɾˠə/.
- Fortis→lenis /l n/: *leanbh* /lʲanˠəw/, *naomh* /nˠiːw/ — with the note that the test is
  **intentionally inapplicable** under the two-way normalization, which is what the review asked for.
- Eclipsis /pʲ→bʲ/ *bpeann*, /tʲ→dʲ/ *dteach*, /c→ɟ/ *gceann*, /d̪ˠ→n̪ˠ/ *ndroim*,
  /fʲ→vʲ/ *bhfreagra*, /ɡ→ŋ/ *nglúin*, /bʲ→mʲ/ *mbean*.
- **N-prothesis**: *n-éan* /n̠ʲeːnˠ/ (with *éan*, *t-éan*, *héan* as the full contrast set).
- **Triggers**: attested *an tsúil* (article + fem. nom.) and *an tsaoil* (article + masc. gen.);
  constructed-from-two-attested-strings *an bhean*, *mo pheann* (possessive lenition),
  *a bpeann* (plural possessive eclipsis), *na bpeann* (genitive plural), *deich bpeann*
  (numeral eclipsis).
- **Adjective agreement**: *bhán* /waːnˠ/, the *Máire Bhán* form, replacing bare *bán* as the
  agreement test.
**Supersedes** the digest-log "What could not be resolved" item 4 (the personal-name IPA gap is
real and unchanged, but the general "no IPA for mutations" implication was wrong) and the old §7
row counts.

## Suggestions taken

- **Green's notation kept beside a normalized IPA table** (§2.3). Green's table (27) is now
  printed verbatim in his own notation *and* converted to this digest's IPA, with the conversion
  explicitly labelled as the digest's so it stays auditable.
- **Canonical Connacht vs. pan-dialectal separated** (§8.6 + the `dialect` column note in §7):
  `std` and `C/M/U` are now described as separate fixtures to be filtered on, not variants, and
  the two scheme-vs-dialect pairs are carried as explicit row pairs.
- **§6 suffix semantics** (review §2.4, §2.5): a sourcing caveat now heads §6 stating that no
  held source is a grammar or dictionary of Irish derivation, that only the declension classes
  and the pronunciations are sourced, and that **the affix meanings and productivity claims are
  (unattested)**. Row 8 (noun+noun compound) is relabelled **PROVISIONAL** in the table itself.
- **Other under-cited claims marked** (review §2): §0's dialect diagnosis, §2.1's name-shape and
  -ach generalizations, §8.2's whole Frequency column, §10.1's "≈46", and §10.7's "converts most
  of a name's spelling" are each now explicitly marked as digest inference rather than source claim.

## Not taken, with reasons

1. **No Old Irish TSV** (review §5.7, suggestion 3). Correct in principle and I agree §10 is not
   machine-ready — but the blocker is §10.7, not the file format: there is no Modern→Old
   derivation in the held sources and no bulk eDIL access, so an Old Irish fixture file would be
   40-odd hand-copied attested names with no rule to test them against. That is a decision for
   the user (§9.8) about what strand 5 even is, and building the file first would prejudge it.
2. **`ipa` column not renormalized to one canonical scheme** (review §5.5). I kept source-verbatim
   strings and defined the level instead (§8.6). Renormalizing would destroy the audit trail back
   to the source, which is the point of this step; the normalization belongs in the adapter, and
   §8.6 now says so and says what it has to do.
3. **§8.2's target-side notes retained but demoted.** The review is right that a source digest
   should not settle target inventories (§5.6). Rather than delete them I marked the whole Notes
   column as pointers to be verified in each target digest, and re-attributed the specific claims
   (Georgian /f/, Arabic /v/) to `../../notes/project-goals.md`, which is where they came from.
   Deleting them would lose the cross-reference the target digests need.
4. **Review §3's suggestion to normalize *Ciara*'s IPA to /iə/ was not applied.** Under the §8.6
   policy the surface string stays as the user wrote it and the tag carries the underlying
   phoneme; changing the user's transcription would be exactly the silent renormalization
   point 2 rejects.
