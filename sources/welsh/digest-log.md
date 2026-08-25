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

---

# Revision 1 (after adversarial review, `review.md`)

Review verdict: 35 claims checked — 27 verified, 2 misquoted, 1 not found, 5 overstated. All seven
assigned required fixes are done. Required fix 8 (rule ordering) was **deliberately not decided**,
per instruction: the options are laid out and left open.

## Changes to `digest.md`

**1. §2 rebuilt by evidence level** (review §6.1, §2.1–2.3, §5.1).
- Onsets are now split into four labelled tiers instead of one `STATED` table:
  **A — STATED CLASS** (`/fl tl pr sl sr st sp sk stl spr skl/`, all `breit2019 p.252`);
  **B — LEXICALLY ATTESTED ONLY** (`/str bl ɡl dl ɡn/`, each with its word and citation);
  **C — TYPO-CONJECTURE** (`/fr/` alone);
  **D — DISPUTED ANALYSIS** (`ɡw-`, `χw-`, `sC-` — sequences whose *syllabic analysis* is contested);
  **E — ASSEMBLED / UNVERIFIED** (the generalised stop+liquid set, `/sm sn/`, `/θr χr χl/`).
- `/fr/` moved out of STATED. The digest previously emended `breit2019`'s printed `[fl, pr]` to
  `[fl, fr]` and then cited the emended form as stated. The emendation is retained as a labelled
  conjecture with its cost spelled out ("if wrong, fricative+liquid has exactly one member").
- `/dl/` moved to level B with the source's actual scope stated: one token, *dlos*, offered to
  illustrate `[ɫ]` after `/d/` as a Southern exception, not a `/dl/` class.
- **`/vl/ *gwefl*` removed** — *gwefl* is in no held source and the member carried no citation.
- **`/lt/ *gwallt*` corrected to `/ɬt/`** — Welsh ⟨ll⟩ is `/ɬ/`; this was a transcription error, not
  a dialect conflict. `/rθ/` and `/ns/` also removed (no cited word).
- The coda list is now a per-member table with a word and a citation for every entry, plus an
  explicit "Removed in revision 1" note.
- "Southern surface maximum is very likely CC" → marked **(unattested inference)**, with the reason
  (`williams1994` states one epenthesis class, not a maximum, and does not exclude other CCC codas).
- "Southern word-final CC is restricted to falling or level sonority" → downgraded to a heuristic
  and marked **(unattested inference — stronger than the source)**.

**2. Historical/modern layering made explicit at claim level** (review §6.2, §2.11–2.13, §4.5, §5.2).
- **§8.1 rewritten.** It previously read "every foreign palatal collapses onto /ʃ/" in the present
  tense, sourced entirely from Parry. It is now split into **LAYER 1 — ME/early NE** (initial
  `/tʃ dʒ/ → /ʃ/`, flagged *do not encode as a modern rule*, with the positional exceptions the old
  text erased: final `/dʒ/ → /-s -ts -ds/`, late `/tʃ/` loans keeping the dental) and **LAYER 2 —
  modern** (`/tʃ dʒ/` retained; in **South Welsh** `/dʒ/` additionally arises natively from `/t d/`
  before `/i/`, so it is not even loan-restricted in the target variety). A `CONFLICT:` line marks
  the period clash, which was previously recorded in §1 and §3 but suppressed in §8.1 — the section
  where the Irish mapping is actually decided.
- Every `parry1923`-derived bullet in **§3.6** now carries an inline period tag. The front-glide
  rule additionally carries its dialect: Caernarfonshire, i.e. **North** Welsh, and obsolescent.
- **§8.5**'s initial `l/r` fortition tagged *(ME/early NE; explicitly receding by the late layer)*.
- **§5**'s load-bearing romanization rows (`/ʃ/ /dʒ/ /tʃ/ /z/`) now carry per-row source and period
  notes, since the historical and modern conventions differ on exactly those four.

**3. §8.9 donor-side unlenition removed as a Welsh rule** (review §6.3, §1.33, §4.7).
The digest turned `wood1988 p.231` ("the usual way of accommodating loanwords into Welsh" = assign
an unmutated **Welsh** radical) into "an Irish lenited form should be un-lenited before adaptation".
That does not follow, and the review is right. The Welsh fact is retained with an explicit warning
against over-reading it; the Irish-side normalisation is marked
`(design decision, not a Welsh adaptation fact)` and assigned to the Irish digest.

**4. §8.7 long-vowel rule weakened to the source's strength** (review §6.4, §1.32).
"An Irish long vowel in a final stressed syllable **is** preserved by voicing/leniting the following
consonant … the one clean, attested answer" → now states Wood's "**usually**", names the size of the
evidence (one worked example, *clog*, plus *grâd* from `morrisjones1913 §51 ii`), notes it is an
English→Welsh pattern not an Irish→Welsh rule, marks it `(unattested for Irish)`, and records the
competing outcome (short vowel + geminate final) that Wood gives in the same passage.

**5. Y Bowyseg separated from administrative Powys** (review §6.5, §1.35, §4.8, §5.3).
Both §0 and §9.1 rewritten. The digest previously wrote "Llanwrtyd is in Powys, and `breit2019`
groups Powyseg with North Welsh", which invites an administrative-area ⇒ dialect inference. Now
stated as three separate facts: Breit groups the *traditional dialect* **Y Bowyseg** with North/Mid
Welsh [breit2019 pp.53–54]; Llanwrtyd sits in the modern *administrative county* of Powys, a 1974
local-government unit; **no source connects the two**, and Llanwrtyd is named in no source file. So
this is a **gap, not a dialect conflict**. §9.1 adds the explicit instruction that "Llanwrtyd is in
Powys" must not be used as evidence for Northern or Powyseg rules.

**6. The s+C scope/ordering contradiction stated precisely** (review §6.6, §4.2, §4.3).
A new subsection in §3.1 separates three things that were previously conflated, **without choosing
between them**:
- **Scope** — `morrisjones1913 §23 ii` states the rule over **s + any consonant**;
  `parry1923 §84` states the loan rule over **s + stop only**. The formal rule is now given at
  s+stop scope with the wider native scope shown beside it. §8.6 correspondingly notes that Irish
  `/sp st sk/` fall under both statements while **`/sm sn sl sr/` fall only under the wider native
  rule, for which there is no loan evidence**.
- **Medium** — both sources say the vowel is written but not pronounced unless accented, in nearly
  the same words; Old Welsh did not write it at all.
- **Conditioning** — the stress condition is quoted from both sources; the *derivation* of when
  stress will fall on it is the digest author's and is now marked `(unattested inference)`.
Three self-consistent encodings (**P** pronunciation-only, **S** spelling-only, **C** conditioned
epenthesis) are tabulated with their costs. This resolves the apparent §2.2-vs-§3.1 contradiction:
`/sp st sk sl sr/` are licit onsets in every source, and the *y-* is orthographic/stress-conditioned,
not a repair of an illicit cluster.

**7. Four `wood1988` citations corrected** (review §6.7, §3): `p.233` → **`p.235`** for *map, siop,
mat, cloc* in `attested.tsv`. The in-text §3.3 and §8.7 references were already correct
(`pp.234–235` / `p.235`); the remaining `p.233` references in §2.7 and §4.3 are to Wood's *length
rule*, a different passage, and are unchanged.

**8. Rule ordering — NOT decided, per instruction** (review §6.8, §4.6, §5.6).
New **§4.4 OPEN**. The contradiction is real and was previously invisible because §4.1 ("length
assigned after stress, not carried from the input") and §3.7/§4.3/§8.7 ("loan length is preserved
and attracts stress") each state one side in a different section. Both source statements are quoted;
four orderings (**L1** Welsh-first, **L2** length-first, **L3** Welsh-first with consonant repair,
**L4** nativisation-grade switch) are tabulated with their consequences for Irish input, plus three
knock-on effects to check. **No recommendation is made — this is the user's decision.**

## Other review points taken

- **§1 heading fixed.** "Mark marginal (… all should be)" contradicted its own `/tʃ dʒ/` row, which
  concludes "not marginal in the South". Retitled, with a lead-in saying `/tʃ dʒ ʃ/` are the
  exceptions and to read the Status column rather than the heading.
- **Optionality words preserved**, per the review's suggestion — "usually", "tendency", "may",
  "occasionally" now survive into §3.2, §8.5 and §8.7 rather than being flattened.
- **§8.3's "either way no repair is needed"** labelled `(design inference)`, with the one piece of
  actual /x/-adaptation evidence in the corpus noted (the *reverse* case: English ⟨gh⟩ /x/ retained
  as Welsh ⟨ch⟩, *dracht, fflicht, slachtar*).
- **Two unciteable citations withdrawn**: `/ɡn/` from *gnawd* (etymological aside, no page) and the
  `/bl br ɡl ɡr dr tr kr kl fl fr/` row's "[morrisjones1913 passim]", which is not a citation. That
  §8.6 row is now split into individually cited members plus an explicit "not licensed by any class
  statement in this corpus" group.

## Change to `attested.tsv`

- **751 rows unchanged in content**; the four `wood1988 p.233` provenances corrected to `p.235`.
- **A ninth column, `layer`, added**: `historical` (653), `modern` (93), `translit` (5). The eight
  columns specified in `../ATTESTED-FORMAT.md` keep their order and positions, so a positional
  8-column reader is unaffected. This implements the review's "split into modern-rule and
  historical-evidence views without discarding either layer" as a tag rather than a file split, so
  nothing is duplicated. Documented in §7, including the filter
  `awk -F'\t' '$9=="modern"' attested.tsv`.
- The review's separate point that the file "is weak for phonetic testing" (653/751 rows have blank
  IPA on both sides) stands and is **not** fixable from these sources: Parry-Williams gives no
  pronunciations. The `layer` column at least makes the 93-row testable subset addressable.

## Where I did not follow the review

1. **`/fr/` retained as a labelled conjecture rather than deleted.** The review calls the STATED
   label a misquotation, which it was, and I have removed it. But `breit2019 p.252` printing the
   identical string `[pr]` for two different classes one clause apart is stronger evidence of a typo
   than of a genuine claim that `/pr/` is a fricative+liquid cluster. Deleting the conjecture would
   lose that signal; keeping it as level C with the failure mode stated costs nothing.
2. **The four levels are A–E in prose, not the `explicitly_licensed` / `lexically_attested_only` /
   `northern_only` / `unverified` **fields** the review asks for** (§5.1). Northern-only is already
   carried by the existing **(North)** tag on every affected member, so a separate field would
   duplicate it. A machine-readable cluster table is a rule-file artefact, not a digest artefact —
   the digest's job here is to say what each claim rests on, which the tiers now do.
3. **I did not restate the §3 rules with source hedges in the formal `X → Y / A _ B` lines**
   (review §5.7). The arrow notation cannot carry "tendency" without becoming unreadable; instead
   the hedge sits in the prose immediately around each rule, and §3.2's three repairs keep the
   source's own conditioning (the antepenult ban is the only *stated* condition, and it is marked as
   the only one).
4. **Review §1.21's point that `/kn-/` retention is "historical evidence, not a modern productivity
   experiment"** is correct and I have not added a hedge, because §3.1 already presents it inside a
   section headed as historical and the modern corpus contains no counter-evidence. Flagging it
   further would imply a doubt no source raises.
