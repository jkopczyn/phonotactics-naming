# Project goals — phonotactics / naming-language tool

Claude-written working notes, distilled from the three imported claude.ai conversations
(`../chat-imports/`, dated 2026-04-17, 2026-06-01, 2026-08-24). Later conversations override
earlier ones where they conflict.

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
rules.** The correct technical frame is *loanword-adaptation phonology*, not creolization (the
tool's working name "creolization/loanword tool" notwithstanding). A creole-flavoured reduction
layer could be stacked on later but is not planned.

## Target languages (state as of 2026-08-24)

| Strand | Target | Status | PHOIBLE inventory (in `../phoible_inventories_starter.csv`) |
|---|---|---|---|
| 1 | Egyptian (Cairene) Arabic | pinned | InvID 231 (UPSID; dental diacritics = plain coronals) |
| 2 | Southern Welsh | pinned | InvID 2406 (Llanwrtyd; no /ɨ/) |
| 3 | Dutch | "probably" | InvID 2169 (Belgian Standard; Booij's reference is Netherlandic) |
| 4 | Georgian | "probably"; the harsh/alien strand | InvID 2183 (Standard/literary) |
| 5 | Old Irish | fixed, no filter | — |

Strand 4 has **pre-existing names** that any output must sit beside convincingly: *Tchaeul,
Th'tysh, Kas'queil, Xelxyx, Ysclyth*. Their signature: all-voiceless obstruents, no nasals,
apostrophe = ejective/glottal break, uvular q and velar x, heavy onset+coda clusters, lax y-vowel,
every word consonant-final. The June conversation recommended Georgian (clusters, ejectives, q, x)
with Mayan (K'iche'/Yucatec: ready-made apostrophe romanization) as the sleeper alternative and NW
Caucasian as the extreme; it also warned that Xelxyx/Ysclyth read pseudo-Welsh and the strand-4
romanization should be pulled away from Welsh territory. The August conversation then said
"probably Georgian" without revisiting. **Open question:** the June advice was to use a
*feature filter* for strand 4 (devoice, drop nasals, ejectivize, uvularize, keep clusters, force
C-final) rather than Georgian's grammar wholesale; the August position is "real languages' rules,
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
  mappings); skip OT tableaux and any UG framing. User regards UG as discredited; don't relitigate.
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
   left unused; Irish lenition outputs [v w j h] and voiceless sonorants.

Source-side needs (Irish): an Irish phoneme inventory with the broad/slender pairs spelled out;
a way to get IPA for new inputs (hand transcription so far; a G2P would help); Old Irish
inventory/orthography for strand 5.

## Repo state

- `chat-imports/` — three conversations (markdown + two raw JSON). Tool-call detail is absent
  from the August one; in particular the **bibliography markdown Claude wrote in that chat was
  never exported** — its content is recoverable from the chat text and is reconstructed in
  `source-plan.md`.
- `phoible_inventories_starter.csv` — the four target inventories, long format.
- `arabic-phonology.pdf` — Alqarhi 2019 (English Linguistics Research 8(4)). Low-value: a
  general survey, cited in the chat only for "Egyptian is the de facto standard dialect".
- Nothing else yet: no code, no rule files, no bibliography.
