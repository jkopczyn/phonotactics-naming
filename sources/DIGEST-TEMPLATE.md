# Source digest: <Language (variety)>

One digest per target language (and one for Irish as source). Fill from the sources in this
directory's `bib.md`. Every factual entry carries a citation `[key p.N]` where `key` is the
bib.md key and N a page or section; Wikipedia gets `[wiki-<lang> §Section]`. An entry with no
citation is a guess and must be marked `(unattested)`. When two sources disagree, keep both
with their citations under a `CONFLICT:` line — do not pick silently.

Write for a reader who will turn this into rewrite rules: concrete segments, concrete
environments, concrete examples. No theoretical framing (no constraint rankings, no
markedness arguments) — only the generalizations and the data.

Notation: IPA throughout; `C` consonant, `V` vowel, `#` word edge, `.` syllable boundary,
`_` target position; `X → Y / A _ B` for rules.

## 0. Variety and scope

Which variety this digest describes, why, and what sources it rests on. Note anything in the
PHOIBLE row (`../../chat-imports/phoible_inventories_starter.csv`) that the sources contradict.

## 1. Inventory deltas

Segments the sources add to / remove from / mark marginal in the PHOIBLE row. Loan-only
segments and their status (integrated vs. nativized). Notational quirks of the PHOIBLE row
(e.g. UPSID dental diacritics).

## 2. Syllable structure and phonotactics

- Maximal syllable template, with examples of each attested shape.
- Onset clusters: full list of licit CC (and CCC) onsets if the sources give one; otherwise
  the generalization plus the explicit exclusions.
- Coda clusters: same.
- Medial cluster limits (across a syllable boundary).
- Segment-position restrictions (segments barred word-initially / finally / before or after
  certain vowels).
- Vowel sequences / hiatus; glides.
- Gemination: does it exist, where.

## 3. Repair strategies (loanword adaptation)

For each violation type the language actually encounters, what happens. Every rule wants at
least one attested example from §7.

- **Illicit onset cluster** → epenthesis (site: before C1 / between C1–C2 / …; vowel quality
  and what conditions it) / deletion (which member) / prothesis.
- **Illicit coda cluster** → same.
- **Three-consonant sequences** → same.
- **Absent segment → substitute**: a table, one row per source-side segment that matters for
  Irish input (§8 lists which). Attested mappings first; feature-nearest fallback marked
  `(fallback)`.
- **Word-edge processes**: final devoicing, final-vowel addition, initial-glottal insertion, …
- **Vowel adaptation**: length (kept / lost / reinterpreted as quality), reduced vowels,
  diphthongs.
- **Anything else the loanword literature reports** (gemination of loan consonants, glide
  insertion, metathesis, stress-driven vowel changes).

## 4. Stress and length

Stress assignment rule; interaction with vowel length and syllable weight; what happens to
source stress in loans. Vowel-length contrast: present / absent / positional.

## 5. Romanization

The orthographic conventions the output should use, segment by segment, with the ambiguities
an English reader will hit. For strand 4 (Georgian) also assess fit against the existing names
*Tchaeul, Th'tysh, Kas'queil, Xelxyx, Ysclyth* and propose the conventions that match them.

## 6. Morphology usable for epithets

A short list (≤10) of productive, recognisable affixes or patterns: gender/agreement endings,
adjective-from-noun derivation, definite article and its sandhi, diminutives. Form, meaning,
attachment conditions, example.

## 7. Attested adaptations

Pointer to `attested.csv` in this directory (format in `../ATTESTED-FORMAT.md`) and a count.
Summarize the provenance mix (loanword-paper tables vs. dictionary vs. transliteration
practice) and any bias (e.g. all examples English-sourced).

## 8. Irish-specific mismatch notes

For each of these, what the sources say or imply, and what is left as a design decision:

- Broad (velarized) vs. slender (palatalized) consonants — the target has no such contrast.
  Options: depalatalize; Cʲ → Cj / Cʲ colours the following vowel; broad → some marked
  series in the target (e.g. Arabic emphatics). Any target-internal precedent for treating
  foreign palatalized consonants?
- Irish segments with no target equivalent: /ɣ/, /x/, /h/, voiceless sonorants, /ɾ/ vs /r/,
  /l̪ˠ lʲ n̪ˠ nʲ/, /w/ from lenited b/m, /v/, /f/, /p/ (rare in native Irish), /ŋ/.
- Irish vowel length and the diphthongs /iə uə əi əu/.
- Irish initial clusters that the target bans (e.g. /sp st sk sm sn sl sr/, /kn gn mn/,
  /bl br gl gr dr tr kr kl fl fr/) — which rule in §3 each falls under.
- Initial mutations / genitive forms on the source side (only if the sources say anything
  useful about how the target treats such alternations in loans; otherwise leave for the
  Irish digest).

## 9. Open questions

Things the sources didn't settle and the digest author couldn't resolve.
