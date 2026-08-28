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
| 7 | `attested.csv`; provenance counts in §7 |
| 8 | assembled from §1–§4 plus `wiki-nl-phonology` §Allophony (the /Cj/ palatalization facts), `booij2011-msc` p.2056 (*Pjotr, Tjeerd, Kjeld*), `verhoeven2005` pp.244–245 |

## Sources deliberately not used
- `loan-uu-contrastief-fonemen` and `loan-brand-berns2023` — both are L2-acquisition contrastive
  analyses (Dutch speakers producing French/English), the wrong direction, as bib.md warns. No rows
  from them are in `attested.csv` and no §3 claim rests on them.
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
   `sources/infra/wold-dutch-loanpairs.csv` carries a `target_ipa` column with van der Sijs's
   space-separated phonemic segmentation for every row (e.g. *juist* `j œy s t`). The 20 WOLD rows
   in `attested.csv` therefore have `target_ipa` filled. The *donor* side genuinely has no IPA
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

---

## Revision 1 (after the cross-family adversarial review in `review.md`)

Reviewer's tally: 22/33 sampled claims verified, 4 misquoted, 2 not found, 5 overstated. All eleven
"required fixes" were addressed except nos. 6 and 10, which the coordinator reserved as user
decisions; for those the digest now states the options and the evidence for each and leaves them
open. Changes, by review item:

**§6.1 — schwa epenthesis (was MISQUOTED).** The formula `∅ → ə / [+liquid] __ C[-coronal]` was
wrong: it would have blocked the source's own *urn* [ʏr(ə)n] and *hoorn* [hor(ə)n]. Replaced with
the source's actual statement — insertion in a **complex coda** whose first member is **/l/ or /r/**
and whose members are **non-homorganic** — plus the two separate blocks (homorganic C1C2; C2 = the
coronal obstruent /s/ or /t/), the full twelve-item example list as printed, the fact that the
process is **optional and register-graded** (Taalportaal prints every example with the schwa in
parentheses), and the tautosyllabic domain [taalportaal-schwa-epenthesis-deletion §quickinfo,
§General information; devoic-schwa-mpi §Introduction].

**§6.2 — unsupported deterministic repairs.** Four claims relabelled `(design fallback)` and moved
out of the sourced-rule voice: initial-cluster deletion (§3.1, now headed "no adult loan repair for
an illicit initial cluster is attested in any source in this directory"); Irish coda /h/ (§8.2, four
options listed, none attested); the length→A/B conversion (§3.6, now a `CONFLICT:` with the evidence
on both sides); and the Irish diphthong mappings (§8.3, both /iə uə/ and /əi əu/).

**§6.3 — coda lists.** Added a `CONFLICT:` block on the maximal coda reconciling LAPSyD (Coda=3 but
four printed slots), Wikipedia (four), `taalportaal-codas` (five word-finally, two word-medially)
and `taalportaal-nuclei` (rhyme coda ≤2), with the resolution to encode: **rhyme coda ≤2 plus up to
three coronal-obstruent appendix positions**. Coda cluster tables now carry a header saying they are
**underlying** forms, with the surface neutralizations spelled out (/-lv/→[-lf], /-rd/→[-rt], …), and
a new "true coda vs appendix" paragraph giving the source's own diagnostic: schwa epenthesis breaks
coda + extra-syllabic sequences but never consonant + appendix ones.

**§6.4 — gemination and hiatus (both MISQUOTED).** "Gemination: none/never" replaced by the
domain-sensitive rule: obligatory degemination **within a prosodic word**, optional across a
compound/phrase boundary, with the source's [ˈbɛrxːɛit] / [vɛrːɑsə(n)] cases and the note that
final devoicing does not apply across such a seam. The front/back two-way hiatus summary replaced by
the source's four cases: [j] after unrounded front vowels, [ʋ] (Belgian [w]) after back vowels, [ɥ]
after front rounded vowels, and after /a/ or schwa **no glide at all** — [ʔ] if the next syllable is
foot-initial, otherwise the hiatus is kept.

**§6.5 — substitution variation.** New "Making the variable rows executable" block after the §3.4
table. It identifies the one conditioning factor the data actually supply — van Dijk's 1–3
integration score, which the substitutions track — and adds explicit `CONFLICT:` lines for /æ/, /ʌ/,
foreign /g/ and the French nasals rather than choosing. Table rows rewritten accordingly.

**§6.7 — normalization.** §0 now carries an executable **normalization layer**: an eight-row
source-symbol → Belgian-target-symbol table plus the full normalized Belgian phoneme list to encode
rules over. Netherlandic-only data is tagged at the point of use.

**§6.8 — attested.csv.** The 15 Taalportaal rows had a stress-marked orthographic form
(`ad.mis.'sion`) in `source_ipa`; that field is now blank on those rows and the form is carried in
`note` with a warning. All 20 WOLD rows now carry `process tag inferred (WOLD gives no donor IPA)`
in the note. The *rapskills* row no longer claims `/æ/ → /ɛ/`: `source_form` is *skills* (what the
donor column actually gives), the process is `none`, and the note says the *rap-* half is not in the
source. §7 updated to match.

**§6.9 — Irish mappings.** §8.3 rewritten with an explicit `(design fallback)` label on the whole
subsection, a full **Irish monophthong → Belgian vowel table** (including /u/ → /ʏ/ or /ɔ/ as
unresolved), and the ordered list of sourced Dutch constraints that any mapping must then satisfy.
The false shortcut "Irish short vowel is already B-class" is gone. §8.1 gained a three-column option
table whose middle column is **coda behaviour** — the point being that option (b) *must* collapse in
codas, since /j/ is admitted there only after a tense vowel and only before a coronal. §8.2's rows
for voiceless sonorants, coda /h/, /ŋ/ and /l̪ˠ lʲ n̪ˠ nʲ/ were expanded with labelled fallbacks.

**§6.11 — *-achtig* (was NOT FOUND) and citations.** The *-achtig* row was wrong in the way the
reviewer says: `taalportaal-final-devoicing §The influence of suffixes` lists *-aardig* and
*-achtig* as the two **vowel-initial** exceptions that are non-cohering and therefore trigger
devoicing. Row corrected, with the cohering *-ig* contrast (*rood* [rot] → *rodig* [rodəɣ]) added.
Every `[ibid.]` (16 of them), `[p.244]`, `[wold]`, `[wold, van der Sijs]`, `[vandersijs1996 p.57]`
and bare-key citation was replaced with a resolvable `bib.md` key + locator; the file now contains
no `ibid.`.

**Review §1 nos. 19, 21, 22, 23.**
- **19 (pneumatisch).** Corrected. Booij's "no difficulty pronouncing *pneumatisk*" is about
  **Norwegian** [booij2011-msc p.2062]; the Dutch claim is now sourced to Taalportaal's own
  transcription *pneumonie* /pnø.mo.ni/ [taalportaal-onset-clusters-2c §Examples], with Booij cited
  only for `*[pn-` being a **native**-morpheme constraint, and his point that English (not Dutch)
  repairs /pn-/ to /n/ added.
- **21 (t-deletion).** Rescoped. It is now presented as a native morphological / casual-speech
  process with its exact environments (obligatory in obstruent-final diminutives and before *-s*
  /*-st*; blocked after a sonorant; optional in compounds and phrases, graded plosive > nasal >
  liquid/glide > pause), with an explicit note that extending it to an arbitrary illicit donor CCC
  is **not licensed** by these sources.
- **22 (foreign /g/).** Wording changed throughout to "not observed in these Belgian samples" /
  "0/96 observed", never "Netherlandic-only repair".
- **23 (French nasals).** Row rewritten as word-specific, with the nasal-in-both (*croissant*) and
  denasalized-in-both (*plafond, campagne, restaurant*) sets shown alongside the split ones, and the
  counts (5 clear-nasal words in the North vs 39 in the South).

**Also softened or requalified** (review §2): "phonologically stable" now quotes Verhoeven's hedge;
final devoicing "without exception" now carries the source's weaker wording plus the counter-case
*groupies* [ɡrupiz]; "typically restored from spelling" is now "in the two tokens observed"; "no
final-vowel addition, no prothesis" is now an explicit `not covered` naming the sources searched;
the uncited "Dutch orthography is shallow" opener is gone.

**Added beyond the review** (both from review §5's "no ordered repair pipeline" and "no worked
derivation" blockers): a new **§8.6** giving an 11-step rule-order pipeline — with the one sourced
ordering fact marked (final devoicing feeds progressive voice assimilation
[devoic-grijzenhout-roa303 pp.2–8]) — and step-by-step derivations of ***Matánach*** and
***Lasairchos***, each showing where the unresolved policies branch. §9 was rewritten and reordered
by impact, now 15 items.

### A correction to bib.md that the review did not catch

bib.md's `taalportaal` entry, and the task brief after it, assert that "Irish /ɑː/+/x/ (as in
*Matánach* /ˈmˠat̪ˠɑːnˠəx/) is exactly the banned A-class + voiceless fricative shape". **In that
word it is not.** The long /ɑː/ is followed by /nˠ/; the /x/ is preceded by the **schwa** of
unstressed *-ach*, and Taalportaal's Table 1 shows schwa patterning with the lax vowels — *gannef*,
*hannes*, *jarig* for /f s x/, and a dash for /v z ɣ/ [taalportaal-coda-cooccurrence-restrictions
Table 1]. So *Matánach* passes the constraint unaltered, as the §8.6 derivation shows. The
constraint is real and does bite Irish input, but only where a long vowel **directly** precedes a
voiceless fricative (a stressed /Vːx Vːf Vːs/ syllable, e.g. *bách* /bˠɑːx/). Two consequences: the
required "§3 must give a rule for *Matánach*" premise is void as stated, and the "voice the
fricative" repair is **unavailable after schwa**, since /əɣ/ is unattested. Flagged in §2, §8.3 and
§9.

### Where I disagreed with the review

- **Review §1 no.24 and §1 no.27 are half-right and were only partly followed.** Final devoicing is
  weakened in wording, but it stays classified as an *active rule* rather than a violable
  morpheme-structure constraint, because Booij states exactly that contrast and gives *labda*
  [lɑbda] — a loan that violates the voiced-cluster MSC and still devoices
  [booij2011-msc p.2052; booij1999-msc p.59]. Likewise the stress procedure is now labelled as the
  digest's construction, but it is kept, because a rule file needs *some* default and the reviewer's
  alternative is to supply none.
- **Review §2's "WOLD is being asked to prove more than it contains" is right about the process
  tags** (now labelled inferred) **but not about the pairs**: WOLD's Dutch IPA column is direct
  evidence of the adapted form, which is the side the tool has to produce.
- **Review §5's "the digest is not yet usable" framing** conflates "does not decide" with "does not
  say". The three big questions (broad/slender, stress precedence, romanization) are the user's by
  explicit instruction, and per the project brief this digest's job is to lay out the options with
  their evidence, not to pick.
