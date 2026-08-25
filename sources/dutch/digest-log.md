# digest-log — Dutch (Belgian Standard Dutch)

## Which source fed which section

| § | Sources actually used |
|---|---|
| 0 | `verhoeven2005` (PDF pp.243, 247), `bib.md` "Belgian vs. Netherlandic", Taalportaal licence note |
| 1 | `verhoeven2005` PDF pp.243–246 (consonant chart, vowel chart, all the allophone prose); `taalportaal-nuclei` (schwa, loan vowels /ɛː œː ɔː/, A/B classes); `wiki-nl-phonology` §Consonants, §Sonorants (Belgian /x ɣ/, /ʋ/, /l/, /r/); PHOIBLE row 2169 |
| 2 | `taalportaal-onsets-simple`, `-onset-clusters-2c`, `-onset-clusters-3c`, `-onsetless-syllables`, `-consonant-cluster-condition`, `-syllable-level`, `-codas`, `-coda-cooccurrence-restrictions`, `-nuclei`, `-degemination`, `-hiatus-resolution`; the four onset PNG matrices; `kager-pater2012` p.6; `booij1978-fonotactische`; `booij1999-msc`, `booij2011-msc`; `lapsyd-dutch-nld`; `wiki-nl-language` §Phonology |
| 3 | `taalportaal-final-devoicing`, `-voice-assimilation`, `-nasal-assimilation`, `-schwa-epenthesis-deletion`, `-n-deletion`, `-casual-speech`; `devoic-warner2001-epenthetic-schwa`, `devoic-schwa-mpi`, `devoic-jansen2021-schwa`, `devoic-grijzenhout-roa303`; `zonneveld1994-overzicht`; `booij1979-syllabe`; `vandersijs1996-leenwoordenboek` pp.33–34, 57–58; `loan-posthumus1988-uitspraak`; `loan-theissen2006-nasalen`; `loan-gerritsen1995-*`; `loan-kleinbreukink1999-culinair`; `nagy2008-frans`; `loan-vandijk-toename`; `wold` |
| 4 | `taalportaal-stress-*` (all nine pages); `vandersijs1996-leenwoordenboek` p.60 |
| 5 | `wiki-nl-orthography`; `names-wiki-translit`; `vandersijs1999-transcriptie`; `names-wiki-spellinguitspraak` |
| 6 | `booij2014-word-formation` pp.11–16; `taalportaal-nasal-assimilation` §diminutive; `taalportaal-coda-cooccurrence-restrictions` Table 6; `verhoeven2005` p.244; `wiki-nl-language` §Grammar |
| 7 | `attested.tsv`; provenance counts in §7 |
| 8 | assembled from §1–§4 plus `wiki-nl-phonology` §Allophony (the /Cj/ palatalization facts), `booij2011-msc` p.2056 (*Pjotr, Tjeerd, Kjeld*), `verhoeven2005` pp.244–245 |

## Sources deliberately not used
- `loan-uu-contrastief-fonemen` and `loan-brand-berns2023` — both are L2-acquisition contrastive
  analyses (Dutch speakers producing French/English), the wrong direction, as bib.md warns. No rows
  from them are in `attested.tsv` and no §3 claim rests on them.
- `twpl-clusterreduction` — cited once in §3.1 and §9 as a *tiebreaker only*, and explicitly flagged
  as child-acquisition data, not loan data.
- `nagy2007-*` (abstract + Hungarian summary) — read for framing only; contains no data tables.
  bib.md is right that the dissertation itself is unavailable (publication moratorium).
- `oostendorp2012-stress` — the practical stress rule came out of the Taalportaal stress pages,
  which state it more directly and give worked examples. Oostendorp is the source of the *scepticism*
  about the three-syllable window, which is noted in §4 via Taalportaal's summary of it.
- `vandersijs2009-loanwords-dutch` — used only for the "recent English loans are adapted least"
  point in §7.
- `names-taalunie-*`, `names-taaladvies-geo`, `names-wiki-geo*`, `names-dbnl-bakker1997`,
  `names-paardekooper2009` — these are about *which* exonym to use and how to spell place names,
  not about sound substitution. They contributed nothing beyond what §5 already has.
- `booij2003-concrete-fonologie`, `codaclusters-nl-af` — one line each (t-deletion in /xts/).

## Things bib.md or the brief got wrong, and other corrections

1. **WOLD is not orthography-only.** Both bib.md's `wold-dutch` entry and the task brief say WOLD
   gives orthographic forms with no adapted IPA, so `target_ipa` would have to stay blank. In fact
   `sources/infra/wold-dutch-loanpairs.tsv` carries a `target_ipa` column with van der Sijs's
   space-separated phonemic segmentation for every row (e.g. *juist* `j œy s t`). The 20 WOLD rows
   in `attested.tsv` therefore have `target_ipa` filled. The *donor* side genuinely has no IPA
   anywhere in WOLD, as `infra/bib.md` correctly notes. The transcription is **Netherlandic**
   (`ʋ`, `ɛi ɑu`, positional `ɣ`/`x`), so each such row is tagged in its note.
2. **"A-class" / "B-class" are used with opposite polarity by Taalportaal and by Kager & Pater.**
   Taalportaal: A = tense/long. Kager & Pater 2012 p.5–6: Class A = the lax set. This is not flagged
   anywhere in bib.md and is an easy way to invert every rule in §2. The digest uses Taalportaal's
   polarity throughout and says so in §1.
3. **The Taalportaal PNGs were worth opening, as bib.md said** — the CC-onset matrices are where the
   banned clusters live. Confirmed: `-fig-onset-cc-matrix.png`, `-fig-onset-cc-matrix-native.png`,
   `-fig-onset-cc-coronal.png` and `-fig-sonority-profile.png` all render legibly and the exclusion
   list in §2 comes from them plus the accompanying prose. The three rhyme/coda figures
   (`-fig-rhymes-all`, `-fig-rhymes-disallowed`, `-fig-coda-cc-coronal`) were not needed: the
   `-nuclei` and `-coda-cooccurrence-restrictions` prose states the same restrictions in words.
4. **`verhoeven2005.txt` and `gussenhoven1992.txt` IPA are mangled, as bib.md warns.** The PDF was
   read instead (5 pages), and bib.md's decoding key is accurate. Everything in §1 comes from the
   rendered PDF, not the .txt. `gussenhoven1992` was not needed at all once the variety was fixed as
   Belgian.
5. **`loan-mars1994-vreemde` is weaker than bib.md implies.** It argues *prescriptively* that
   French /ʒ/ "should" be pronounced as the g of *gaan*; it is not a description of an established
   substitution with a data set. §3.4 marks it as prescriptive.
6. **`loan-vandijk-toename` is as good as advertised** — the appendix tables give Dutch IPA and
   English IPA side by side per token. Column order is: time | Dutch context | **Dutch IPA** | Dutch
   word class | English source word | **English IPA** | English word class | integration stage
   (1–3). The .txt extraction preserves this well enough to read directly; the PDF was not needed.
7. **`loan-theissen2006-nasalen` N/B split is real and is the single most Belgian-specific dataset
   here.** The North has 5 words with a clear nasal preference; the South has 39. Corroborated
   independently by `nagy2008-frans` (*parfum*: 95% nasal in the South, 87% denasalized in the
   North) and by `loan-kleinbreukink1999-culinair`.

## What could not be resolved

- **§8 broad/slender has no attested precedent**, exactly as bib.md's "Gaps" section predicted. The
  transliteration guides handle Cyrillic by respelling *consonant qualities* (ж→zj, ш→sj, ч→tsj) and
  say nothing about palatalization or the soft sign. The §8.1 hooks (Dutch /Cj/ → palatal outputs;
  Belgian /l/'s [lˠ]~[lʲ̠] allophony; *Pjotr/Tjeerd/Kjeld*) are the closest thing to evidence, and
  they are suggestive, not decisive. The digest lists options and does not choose.
- **No source states the Flemish rate of /n/-deletion after schwa**, which affects every generated
  *-en* ending.
- **Family-name morphology (*-sen*, *van*, *de*, *van der*) is not covered by any file here.** §6
  says so rather than supplying it from general knowledge.
- **Which member of an illicit onset cluster gets deleted in adult loan adaptation** is not
  documented — only in child language (`twpl-clusterreduction`).
- **Secondary stress** was left at the level of "alternating, hammock-shaped"; Taalportaal has eight
  further sub-pages that were not extracted.
- **`vandevelde2002`** (the Belgian /g/ numbers for *buggy, goal, goulash, guillotine, mango*) was
  not attempted — bib.md records it as 403-blocked to automated requests but probably fetchable in a
  real browser. It would sharpen §3.4's /g/ row; the Gerritsen and Klein Breukink data cover the
  same ground less precisely.

## Process notes
- Work was split across four extraction sub-agents (Taalportaal onsets + the PNG matrices; the
  process rules; the loan-substitution repertoire including the Belgian survey columns; and one that
  could not be scheduled). Codas, rhymes, stress, the van Dijk corpus, orthography, morphology and
  all of §8 were extracted directly. Concurrency limits meant several planned sub-agents could not
  run; nothing was skipped as a result, but the loan-word substitution table is the only section
  that rests wholly on a sub-agent's reading.
- Nothing was committed; no files outside `sources/dutch/` were written.
