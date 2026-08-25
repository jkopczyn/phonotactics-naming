# digest-log.md — Welsh (Southern)

## Which source served which section

| § | Primary sources | Notes |
|---|---|---|
| 0 | `williams1995` (PDF pages read visually), `mayr-davies2011`, `iosad2017`, `breit2019`, `wiki-cy-lang` | `asmus2020` used only for the fortis/lenis reading of the PHOIBLE stop row |
| 1 | `williams1995` Tables 1–2 (from the PDF), `breit2019`, `wiki-cy-phon`, `mayr-davies2011`, `jipa-north` (tagged North), `lapsyd-cy` (North) | |
| 2 | `breit2019` p.252 (the only explicit cluster statement anywhere open), `breit-harris2014`, `williams1994`, `wiki-cy-phon`, `wood1988`, `grawunder2015`, `jipa-north` (North), `lapsyd-cy` (North) | `morrisjones1913` used for syllabification, glide hiatus, final -Cw, gemination — **not** for a cluster list; see below |
| 3 | `parry1923` Ch. V §§76–131 and Ch. III–IV §§7–75, `wiki-cy-phon` (the pobl/ffenestr/ewythr triad), `williams1994` (the epenthesis contexts), `wood1988`, `buczek2014`, `bmj-mutations` | |
| 4 | `liu2018` (Southern, instrumental), `iosad2017`, `wiki-cy-phon`, `wood1988`, `breit2019`, `williams1983`, `grawunder2015`, `buczek2014`, `coleman-stress`, `pmc-lexical-stress` | |
| 5 | `wiki-cy-orth`, `williams1994`, `cy-wiki-arddull` | |
| 6 | `morrisjones1913` §§114, 126, 146, 153, `bmj-mutations` | |
| 7 | `parry1923` (653 rows), `buczek2014` (48), `wiki-cy-orth` (21), `wood1988` (9), `cy-wiki-arddull` (5), `bmj-mutations` (4), misc. (11) | 751 rows |
| 8 | `parry1923`, `morrisjones1913`, `wiki-cy-phon`, `breit2019`, `wood1988`, `jipa-north`, `williams1995`, `wikt-cy-from-gle` | |

## Things in `bib.md` that turned out to be mis-described

1. **`morrisjones1913` does NOT contain a list of initial consonant combinations.** `bib.md` says it
   covers "§2 initial combinations and consonant groups". Its "Sounds in Combination" chapter
   (Contents p.xi) is *Syllabic Division* (p.30), *Diphthongs* (pp.31–41), *Ambiguous Groups* (p.41),
   *Accentuation* (p.47), *Quantity* (p.65). There is no consonant-group section in the volume.
   What it *does* give, and what the digest uses it for: §23 ii (the s+C prothetic vowel, with the
   crucial "not heard except when accented" caveat), §27 (medial syllabification and degemination),
   §36 (glide hiatus), §42 (final -Cw), §54 (gemination and quantity), §26 iii (gw-), plus the whole
   of §6.
   **Consequence: the explicit-cluster-list gap is one source wider than `bib.md` implies.** The
   nearest thing that exists is one sentence in `breit2019` p.252, offered incidentally as a preamble
   to an argument about Italian. §2 labels every cluster STATED or ASSEMBLED accordingly.
2. **`williams1994` is underweighted in `bib.md`.** It is described as a §5 romanization source. It
   is in fact the best §2 source for **Southern** final-cluster phonotactics: it describes a
   **south-central Wales** accent (near Llandovery), and because its first pass must enumerate every
   consonant that can precede an epenthetic vowel, its rule set is a negative image of the licit
   Southern final-cluster inventory.
3. **`cyg-enwau-tramor` contains no name list at all.** The page points at BydTermCymru, which
   `bib.md` correctly notes is 403-blocked. `bib.md` describes it as covering "the process by which
   foreign names get Welsh forms"; in practice it contributed nothing. `cyg-canllawiau-enwau` was
   likewise not needed. `cy-wicipedia-arddull` *did* deliver: it states the three competing
   conventions for foreign names with examples (§5).
4. **`williams1995`'s garbled tables**: `bib.md` flags this correctly, and reading the PDF pages
   visually did recover both tables. Worth recording that the paper is **unpaginated** — citations
   are by PDF page (p.1–p.4), not the published Eurospeech pagination.
5. **`parry1923`'s OCR is better than `bib.md` fears.** Running headers survive, so page numbers are
   recoverable for every extracted item. The prose of Ch. V is clean throughout; losses were confined
   to individual example forms (about a dozen), which were dropped rather than guessed. Italics are
   lost, so E etyma and W forms are distinguished only by his glossing convention.

## What could not be resolved

- **Whether the PHOIBLE variety (Llanwrtyd, Powys) is Southern at all.** `breit2019` pp.53–54 groups
  Powyseg with **North** Welsh ("Mid Welsh"); `wiki-cy-lang` lists it as north/central-eastern.
  Llanwrtyd is never named in any source file. The inventory in the row is unambiguously Southern
  (no /ɨ/, eight diphthongs), but the N/S tagging that runs through §§2–4 and §8 may be pointed at
  the wrong dialect. Flagged as §9 item 1.
- **The Southern dorsal fricative, [x] or [χ]** — four sources, three positions, and `breit2019`
  contradicts itself within two pages. Directly load-bearing for Irish /x/.
- **The direction of the duration cue to stress** — `williams1983` (shorter) vs `liu2018` (longer,
  on Southern speakers, with a proper control group). Opposite instructions for the romanization.
- **Whether length is contrastive in Southern penults** — four sources say yes, `liu2018` says no.
- **`williams1995` p.3's length-conditioning consonant list includes /m n ŋ/**, against
  `iosad2017`, `wiki-cy-phon` and `breit2019`, and against `wood1988`'s explanation of *why* /m/ is
  absent ("Final m is always geminate"). Three sources to one; treated as a TTS simplification, but
  not resolved.
- **Initial /mn/ in Welsh** — no statement either way, no headword.
- **Irish /ç/** — no source names [ç] in connection with Welsh at all.
- **Foreign centring diphthongs** — no coverage.
- **Any Irish→Welsh adaptation evidence.** `wikt-cy-from-gle` is a bare category list: no etymons,
  no phonology, no dates. `morrisjones1913` names one Irish loan in passing (*brat*). Two of the
  Wiktionary headwords (*chwedl*, *ochr*) are treated by Morris Jones as **inherited cognates, not
  loans**, which thins the corpus further. `bib.md` is right that Welsh Journals Online is
  **blocked rather than missing** — that is the place to look by hand.

## Method notes

- Six sub-agents ran in parallel (inventory/§0–1; phonotactics/§2; Parry-Williams consonants;
  Parry-Williams vowels; stress and length/§4; Irish mismatches/§8). §5, §6 and the modern-loan
  attested rows were extracted by the lead. No sub-agent wrote `digest.md`.
- `attested.tsv` was assembled from four scratch TSVs, deduplicated on
  (source_form, target_form, provenance). All 751 data rows have exactly 8 fields.
- `iosad2017` page numbers are from the **preprint** (pp.1–50), not *Phonology* 34(1):121–162.
  `williams1994`, `williams1995`, `grawunder2015`, `coleman-stress`, `pmc-lexical-stress` have no
  usable pagination and are cited by section or PDF page.
- `buczek2014`'s tables mark stress by underlining, which the text extraction drops. The stress
  *class* in the attested rows is taken from her explicit table headings and is reliable; the exact
  syllable in polysyllables ending in `-io`, `-au`, `-iau` is the digest author's syllabification.
