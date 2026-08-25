# digest-log — Irish (source side) + Old Irish

Written 2026-08-24. Companion to `digest.md` and `test-words.tsv`.

## Which source carried which section

| Section | Primary | Secondary / cross-check | Unused for this section |
|---|---|---|---|
| §0 variety | `wiki-help-ipa-irish` §Comparison of transcription schemes | user's own transcriptions in `../../notes/project-goals.md` | — |
| §1.1 consonants | `wiki-irish-phonology` §Consonants, §Allophones, §On- and offglides, §Fortis and lenis sonorants | `wiki-help-ipa-irish` §Consonants + notes 1–10; `nichasaide1999` p.112–113 (Ulster) | `quiggin1906` (notation cost) |
| §1.2 vowels | `wiki-irish-phonology` §Vowels, §Vowel backness, §Nasalized vowels | `nichasaide1999` p.114–115; `wiki-help-ipa-irish` §Vowels | — |
| §2.1 syllable shapes | assembled by inspection from the ~550 harvested word+IPA pairs | `green1997` pp.55–56 | no source states an Irish maximal-syllable formula |
| §2.2 onsets | `wiki-irish-phonology` §Word-initial consonant clusters; `wiki-clusterchart-2C_cluster_nonmut.svg`, `-2C_cluster_mut2.svg` | `green1997` pp.55–56, 143–149 | Ní Chiosáin 1999 (paywalled, not held) |
| §2.3 codas | **`green1997` pp.55–56, 136–146** | `wiki-irish-phonology` §Post-vocalic consonant clusters | Wikipedia has no final-cluster list |
| §2.4 epenthesis | `wiki-irish-phonology` §Post-vocalic…; `wiki-clusterchart-Epenthesis_cluster.svg`; **`green1997` pp.149–154**; `wiki-irish-orthography` §Epenthesis | `irish-schwa-kwpl` §§4–5; `quiggin1906` §111, §138ff | — |
| §3 mutations | `wiki-irish-mutations` §Summary table, §Environments…, §Changes to vowel-initial words | `wiki-irish-orthography` §Grapheme to phoneme correspondence (for the attested IPA of every mutated form) | — |
| §3.5 gen./voc. | `wiki-irish-declension` §Declension, §Vocative | `wiki-irish-orthography` (attested *mac/mic*, *caisleán/caisleáin*) | — |
| §3.6, §6 epithets | `wiki-irish-declension` §Adjectives; `wiki-irish-mutations` §After preposed adjectives / §After most prefixes / §The second part of a compound; `wiki-irish-name` §Ó and Mac surnames, §Epithets, §Traditional Gaeltacht names | — | — |
| §4.1 stress | `wiki-irish-phonology` §Stress, §Compound words, §Munster; **`green1997` pp.94, 121–125**; `green-munster` pp.3–5 | `rowicka` pp.2, 6–8; `kukhto2019` pp.1565–1568; `nichasaide1999` p.115 | — |
| §4.2 length/weight | `wiki-irish-phonology` §Lengthening before fortis sonorants, §Devoicing; **`green1997` pp.72–77, 94, 121** | `rowicka` p.2 | — |
| §5 orthography | `wiki-irish-orthography` §Vowels, §Letters and letter names, §Alphabet, §Epenthesis, §Diacritics | `wiki-help-ipa-irish` (full IPA key read directly) | — |
| §7 test set | `wiki-irish-orthography` §Grapheme to phoneme correspondence; `wiki-irish-phonology` (all cluster/epenthesis/compound sections) | `irish-schwa-kwpl` p.5 (the 15 near-minimal pairs) | `wiki-irish-name` — **no IPA at all** |
| §8.1 broad/slender | **`nichiosain2018` pp.5–7, 31–33** (Connemara ultrasound); **`bennett-syllpos` §7.1**; `bennett-timing` §3.2, §9, p.38 | `wiki-irish-phonology` §On- and offglides; `nichasaide1999` p.113 | — |
| §8.2 voiceless sonorants | `quiggin1906` §§213, 220, 227, 232, 242, 248, 259, 264, 279, 288; `nichasaide1999` p.113 | — | none of the three UCSC papers mention them |
| §10 Old Irish | `wiki-old-irish` (inventory, orthography, stress); `wiki-oi-grammar` (mutations, declension, adjectives); **`pokorny1914` pp.5–20, 43, 56, 59–72** (glide rules, apocope/syncope, trigger lists, paradigms); `strachan1909` pp.1–20 (paradigms + the attested name list) | `utaustin-l1` §§1.1, 1.2, 2.1, 2.2; `utaustin-intro` | `wiki-oi-phonhistory` — see below |

Files in this directory that contributed **nothing** to the digest:
`ocuinneagain-thesis-irishenglish` (as `bib.md` already flagged, it is a sociolinguistic study of
Irish-English, not a description of Irish). `quiggin1906` was used for two facts only and its
1906 notation was not converted.

## Things `bib.md` describes incorrectly

1. **`wiki-oi-phonhistory` does not cover Old Irish → Modern Irish.** `bib.md` says it covers
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
4. **`green1997`'s PDF is 10 physical sheets but the complete dissertation**, as `bib.md` says —
   confirmed. The `.txt` page numbers cited in the digest are the *logical* page numbers visible
   in the extracted text, not sheet numbers.
5. `bib.md`'s note that `nichasaide1999.txt` OCR mangles the IPA superscripts is correct; the
   consonant and vowel tables were read from the **PDF**.

## CONFLICT lines in the digest

| # | Where | The disagreement |
|---|---|---|
| 1 | §2.4 | Epenthesis blockers: `wiki-irish-phonology` gives long-vowel + ≥3-syllable; `wiki-irish-orthography` gives long-vowel + morpheme-boundary (and carries an "uncited" banner). **Resolved by `green1997`**, which supplies both plus homorganicity, and shows the ≥3-syllable blocker is **Connacht-specific** (Munster and Ulster epenthesize in long words). |
| 2 | §3.1 | Lenition of ⟨bh mh⟩ / ⟨dh gh⟩: `wiki-irish-mutations` gives a single phonemic /w/, /ɣ/; `wiki-irish-phonology` gives the [w]/[vˠ] realization as dialect- and position-conditioned. Phonemic vs. allophonic — both kept. |
| 3 | §4.1 | **Why -ach attracts Munster stress**: `green1997`/`green-munster` posit underlying schwa in σ1 *and* special /ax/ prominence; `kukhto2019` pp.1566–1568 argues the /ax/ mechanism is unnecessary (counter-example *macalla* [maˈkalə]). **Both predict the same surface stress**, so the tool need not choose. |
| 4 | §4.1 | **The Munster three-syllable stress window.** `green1997` p.123 depends on it; `green-munster` p.3 reports Gussmann (1995) finding 4th-syllable stress "thereby disproving" it; `rowicka` pp.7–8 also predicts non-window patterns. Three-way disagreement on *imigéiniúla*: penultimate (Gussmann, Rowicka) vs. antepenultimate (`green1997` p.125 fn.18, citing Ó Sé p.c. and calling Gussmann's citation unreliable). `rowicka` p.6 further disputes that initial stress is the Munster default at all. **Only bites if the reference dialect is switched to Munster.** |
| 5 | §10.1 | **Old Irish consonant quality: two-way or three-way.** `wiki-old-irish`/`wiki-oi-phonhistory` = broad/slender; `pokorny1914` pp.13–14 §35 = palatal / neutral / **rounded (u)**. The three-way system is what generates the ⟨-iu -eo -eu -au⟩ spellings. |
| 6 | §10.1 | Old Irish fortis/lenis sonorants are phonemic in `wiki-old-irish` and `pokorny1914` §7, **absent from `utaustin-l1`'s chart**. |
| 7 | §10.1 | Value of lenited *b*, *m*: /v ṽ/ vs. /β β̃/ vs. [w̃]. Notational. |
| 8 | §10.4 | Article's final ⟨-d⟩: `wiki-oi-grammar` says before "a vowel, a liquid, *n*, or *f*"; `pokorny1914` p.59 §132 says before vowels or **aspirated** *f l n r*. |
| 9 | §10.8 | **⟨aí⟩ vs. ⟨ái⟩.** `pokorny1914` p.6 §4 writes *aí (áe)* **explicitly to distinguish it from long *á* + palatal glide**; `wiki-old-irish` agrees. `utaustin-l1` §1.1 writes *ái (áe)* — on Pokorny's convention that spells a different thing. **Matters for spelling names.** |

## What could not be resolved

1. **The Irish cluster inventory has a single source.** Every licit-onset statement traces to
   Ní Chiosáin 1999 (paywalled, not held). Wikipedia and the three Commons SVGs are all we have;
   `green1997`'s independent table (pp.55–56) agrees with them but is coarser. **We have the
   lists but not the author's own conditions, exceptions, or statement of what is excluded.**
2. **The three Commons cluster charts have their text converted to paths** — no extractable
   labels. They were rendered to PNG with ImageMagick and read visually. The transcriptions in
   §2.2 and §2.4 are therefore my reading of images, not text extraction. They agree with the
   article prose everywhere I could check, but a second reading would be cheap insurance.
3. **No exhaustive list of licit word-final clusters from a Modern Irish descriptive source.**
   `green1997` p.55 gives one and it is the best available, but it is stated inside a prosodic
   analysis and its notation is pre-IPA (′ for slender).
4. **No IPA for Irish personal names anywhere in this source set.** `wiki-irish-name` has two
   large tables of names and zero pronunciations. eDIL has no bulk download or API. Hence 20
   constructed rows in `test-words.tsv`.
5. **Noun+noun compound lenition in Modern Irish** (the *Lasairchos* case) is unattested here.
   Old Irish **does** state it (`pokorny1914` p.8 §16: "in the interior of nominal compounds
   aspiration takes place… after nouns"), so §10.5 gives the modern case an ancestor, but the
   modern sources are silent.
6. **Whether /ˈkɪə.ɾˠə/ for *Ciara* is deliberate.** The spelling ⟨Cia-⟩ and the attested
   *ciall* /ciəl̪ˠ/ predict a **slender** /c/ + /iə/, i.e. /ˈciəɾˠə/. The user's transcription
   has broad /k/ + /ɪə/. Flagged as §9.2 rather than silently corrected.
7. **`quiggin1906` was not converted.** Its 1906 notation would need a transcription key before
   its dialect detail could be used; only two facts were taken from it.
8. **Munster syllabification detail** (`green1997` pp.147–149: no cluster licensed at a plain
   syllable edge, only stop+liquid at a foot edge) is stated inside a prosodic-licensing
   analysis. The digest reports the input→output generalization (Munster epenthesizes more) and
   the examples, and drops the machinery, per the brief.
