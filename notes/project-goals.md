# Project goals — phonotactics / naming-language tool

Claude-written working notes, distilled from the three imported claude.ai conversations
(`../chat-imports/`: 6e61633e dated 2026-04-17, 2f456675 dated 2026-06-01, 094f80f3 undated on the
share page — per the user, none is later than 2026-06-01). Where they conflict, 094f80f3 (the one
that pulled the PHOIBLE inventories and wrote the bibliography) is the most developed position.

## What is being built

A **naming-language generator** for a fictional setting. Five cultural "strands" split from one
culture; to keep them recognisably related they all draw vocabulary from **Irish Gaelic**; to make
them sound different, four of them run that vocabulary through the **phonology of a different real
language** (inventory + phonotactics + loanword repair, plus optionally a few morphological endings).
The fifth strand uses **Old Irish** instead of modern Irish and gets no foreign filter.

Inputs are Irish names, descriptive words, and epithets, given in IPA with the broad/slender
diacritics marked, e.g. Ciara /ˈkɪə.ɾˠə/, Matánach 'Burly' /ˈmˠat̪ˠɑːnˠəx/, Lasairchos 'Flamefoot'
/ˈl̪ˠɑsˠəɾʲxosˠ/. Output is the adapted form in IPA **and** a per-target romanization an English
reader can pronounce approximately right. Epithets may need a little grammar (Irish genitive /
mutations on the source side; e.g. nisba, feminine -a, al- on the Arabic side).

Direction is fixed: **Irish is the lexifier (supplies words); the target language supplies all
rules.** The user frames this as lexifier/substrate (creolistics terms); the earlier chat relabelled it
loanword adaptation. Mechanically they coincide (substrate L1 phonology filtering lexifier words), and
the loanword literature is used because it is the only place per-target repair data is attested — no
creole has any of the four targets as substrate. A creole-style *reduction layer* (CV bias, cluster
reduction beyond what the target requires) is an optional add-on, not planned yet.

## Target languages (state as of 2026-08-24)

| Strand | Target | Status | PHOIBLE inventory (in `../phoible_inventories_starter.csv`) |
|---|---|---|---|
| 1 | Egyptian (Cairene) Arabic | pinned | InvID 231 (UPSID; dental diacritics = plain coronals) |
| 2 | Southern Welsh | pinned | InvID 2406 (Llanwrtyd; no /ɨ/) |
| 3 | Dutch | chosen, but user is flexible if something better-documented is nearby | InvID 2169 (Belgian Standard; Booij's reference is Netherlandic) |
| 4 | Georgian | chosen (flexible as above); the harsh/alien strand | InvID 2183 (Standard/literary) |
| 5 | Old Irish | fixed, no filter | — |

Strand 4 has **pre-existing names** that any output must sit beside convincingly: *Tchaeul,
Th'tysh, Kas'queil, Xelxyx, Ysclyth*. Their signature: all-voiceless obstruents, no nasals,
apostrophe = ejective/glottal break, uvular q and velar x, heavy onset+coda clusters, lax y-vowel,
every word consonant-final. The June conversation recommended Georgian (clusters, ejectives, q, x)
with Mayan (K'iche'/Yucatec: ready-made apostrophe romanization) as the sleeper alternative and NW
Caucasian as the extreme; it also warned that Xelxyx/Ysclyth read pseudo-Welsh and the strand-4
romanization should be pulled away from Welsh territory. The 094f80f3 conversation then said
"probably Georgian" without revisiting. **Open question:** the June advice was to use a
*feature filter* for strand 4 (devoice, drop nasals, ejectivize, uvularize, keep clusters, force
C-final) rather than Georgian's grammar wholesale; the 094f80f3 position is "real languages' rules,
maybe with small inventory tweaks". Reconcile before writing the Georgian rule file — the likely
answer is Georgian rules + a small documented overlay.

Arabic choice rationale: Cairene has the most freely available material (only fully-open loanword
paper of the four), is Watson's focus dialect, and is MENA-mainstream. Known Cairene quirks for
Irish input: no /p/ (→/b/), no /v/ (→/f/), /g/ for ج, foreign /q/ → /ʔ/ or /k/, epenthesis into
CCC between C2 and C3 (contrast Iraqi C1–C2), emphatics available as a home for Irish broad
consonants.

## What the user does and does not want

- **Real languages' real rules**, not invented ones. Small deliberate deviations allowed (e.g.
  admitting a forbidden phoneme that is very common in Irish input).
- **Deterministic, grammar-based** rewrite tool. No probabilistic output. At most a lightweight
  perception-side idea (per-language feature weights for nearest-segment substitution).
- **Ignore theory.** Mine loanword papers for their *data tables* (attested source→target
  mappings); skip OT tableaux and any UG framing. User regards UG/OT as robustly disproven and
  statistical-learning accounts as superior; has said twice not to relitigate. Using a
  grammar-style rule engine is acceptable to them on convenience grounds.
- **Open-access sources only** (decided 2026-08-24). No purchases; paywalled monographs are
  noted for completeness but not planned for.
- **Irish input stays hand-transcribed IPA**; no G2P work.
- Cultural associations of donor languages: not a concern.
- Budget: ~"a weekend per language" of rule transcription; three-or-more targets, so the
  per-language process must be repeatable and mostly delegable to LLM extraction from source
  text, verified against attested data.
- Tooling (from the April chat, not yet contradicted): Python; Unicode IPA; features via
  PanPhon/CLTS; rules as per-language text files (adding a language = data task); SPE-style
  rewrite rules, either via foma/HFST or a small in-house interpreter; a test harness of
  "Ciara → X" expectations. Rule extraction from grammar chapters was expected to happen in
  claude.ai chat with uploaded PDFs; that work is now being pulled into this repo.

## What each per-language rule file needs (and where each part comes from)

1. **Inventory + features** — PHOIBLE (done: starter CSV, 153 rows, 38 features).
2. **Phonotactics** — syllable template, licit onsets/codas, cluster co-occurrence, hiatus.
   Wikipedia phonology page for first pass; descriptive monograph for detail; LAPSyD as a
   cross-check on maximal syllable shape.
3. **Repair** — epenthesis site and vowel quality, deletion targets, substitution for absent
   segments, gemination/glide insertion. Only documented in the loanword-adaptation literature
   (WOLD where covered, per-language loanword papers, transliteration practice).
4. **Stress/prosody** and vowel-length handling (Irish has phonemic length; targets differ).
5. **Romanization** for output (per target; for strand 4 must match the existing names).
6. **Optional morphology** for epithets (Arabic nisba/-a/al-; others TBD).
7. **Irish → target mismatch list** — above all: what happens to the broad/slender contrast
   (depalatalize? Cʲ → Cj? colour the adjacent vowel? broad → emphatic in Arabic?). This single
   decision shapes output more than cluster repair does. Also: /ɣ/ has no home in Welsh or
   Arabic (→ /ʁ/), Georgian lacks /f/, Welsh lacks voiced-obstruent problems but needs /ɬ/ etc.
   left unused; Irish lenition outputs [v w j h]. (Voiceless sonorants are allophonic/verbal-
   morphological in Irish, not phonemes — keep them out of the input inventory; irish/digest.md.)

Source-side needs (Irish): an Irish phoneme inventory with the broad/slender pairs spelled out
(inputs arrive as hand-transcribed IPA); Old Irish inventory/orthography for strand 5.

## Repo state

- `chat-imports/` — three conversations (markdown + two raw JSON), plus the two files produced
  in the 094f80f3 chat: `phonology_rule_file_sources.md` (the bibliography, with access tiers
  and per-language Irish→target notes) and `phoible_inventories_starter.csv` (the four target
  inventories, long format, 153 segments × 38 PHOIBLE features).
- `arabic-phonology.pdf` — Alqarhi 2019 (English Linguistics Research 8(4)). Low-value: a
  general survey, cited in the chat only for "Egyptian is the de facto standard dialect".
- Nothing else yet: no code, no rule files, no bibliography.

## Corrections from the digest phase (2026-08-24)

- **Ciara**: the user's /ˈkɪə.ɾˠə/ has a broad /k/; spelling ⟨ci⟩ and attested *ciall* /ciəl̪ˠ/
  predict slender /c/ → /ˈciəɾˠə/ (inferred). Flagged, not silently corrected
  (irish/digest.md §9.2, test-words.csv).
- **Matánach and the Dutch fricative constraint**: the /x/ follows the schwa of *-ach*, not /ɑː/,
  so it passes Dutch's tense-vowel/voiceless-fricative ban unaltered; the ban bites only where a
  long vowel directly precedes a voiceless fricative (*bách*). Earlier notes said otherwise.
- **Welsh PHOIBLE row 2406 (Llanwrtyd)**: the inventory is Southern (no /ɨ/), but Llanwrtyd is in
  administrative Powys and Breit 2019 groups traditional Y Bowyseg with North/Mid Welsh; the
  locality's dialect affiliation is unverified in any held source. Open gap, not a conflict.
- **WOLD Dutch**: the adapted (Dutch) side *does* carry segmented IPA; what is missing is donor-side
  pronunciation. Earlier note ("orthography only") was wrong on the Dutch side.
- **Strand 4 reframed**: "overlay vs pure Georgian" reduces to a few explicit project overlays on a
  Georgian base — national-2002 romanization (apostrophe = ejective) with deviations `x`, `tch`,
  `y`=/i/, bare-stem (no nominative -i) output; word-level ejective-vs-aspirate choice for Irish
  /p t k/ (both attested); broad/slender options incl. broad→Cʷ via Georgian's labialization slot;
  syncope as a native cluster-creation lever. Only "devoice everything / drop nasals" would be
  pure overlay. Georgian shows no loan repair in the held data (preservation whitelist, not a
  proven no-repair grammar).
- **Digest reliability**: cross-family reviews sampled 30–45 claims per digest; verified rates
  67–87%. All required fixes were sent back and applied (Dutch, Welsh, Irish done; Georgian,
  Arabic in progress). Digests remain secondary sources — cite the underlying `[key p.N]` when a
  rule matters.

## Decisions from the user, 2026-08-24 (after the step-2 report)

1. **Broad/slender**: user has no view; asked for speculative defaults. Working defaults proposed
   by Claude (see report follow-up in chat; to be written into each rule file as a labelled
   design choice): keep the contrast on coronals only, via each target's native palatal
   series (/ʃ tʃ dʒ/ where available); drop it on labials and dorsals; slender C before a back
   vowel gets a yod onglide where the target has a device for it (Welsh ⟨si/di/ti⟩, Dutch Cj,
   Georgian Ci) and nothing in Arabic; broad coronals → emphatics in Arabic, no emphasis
   spread implemented.
2. **The generator emits mutated/inflected Irish forms** (vocative, genitive chains, article
   phrases). Every target rule file must handle word-initial /w x ɣ ç j h ŋ ɲ/ and the
   mutation-onset clusters.
3. **Romanization: English-reader respelling** for all five outputs (not authentic target
   orthography + key).
4. **Strand 4: reduce deviations from actual Georgian.** Consequence: spelling choices (`x`,
   `tch`, `y`) belong to the respelling layer under (3) and are not phonological deviations;
   the phonological overlays should shrink to inventory-forced repairs only. Bare-stem output
   for *personal names* is attested Georgian practice (Davit, Tamar, Levan, Zurab, Nikoloz are
   consonant-final in citation form) and so is not a deviation; common-noun epithets keep -i.
   Default to Gabunia's *measured* pattern (aspirate by default, ejective post-consonantally)
   rather than the prescriptive all-ejective norm; drop word-level laryngeal harmony.
5. **Cʷ is ON for strand 4 (Georgian), restricted form** (decided 2026-08-25): non-labial broad
   consonant before /i e/ in onsets → C+/v/ (Georgian slot-V labialization), spelled with *v* in
   the respelling (never *w*, to avoid Welsh drift); paired with slender C before a back vowel →
   Ci; /vv/ from collision with lenited b/m → /v/ degeminates. Accepted as the one deliberate
   deviation for strand 4 because it preserves an Irish contrast, yields native Georgian cluster
   shapes, and delivers the harsh look without an aesthetic filter.
