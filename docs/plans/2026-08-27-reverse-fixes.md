# `strands reverse` — fix round after first implementation (owner rulings 2026-08-27)

Applies on top of `2026-08-27-reverse-plan.md` (draft 4) and commits 46319ec…b53d85e. Each
ruling below overrides the plan where they conflict; V-numbers cited are the plan's. Three
tasks, serial (all touch `src/strands/reverse.py`). Test-first as before; full suite green
before each commit; no change to `rules/` or any forward stage.

Measured facts driving this: `strands reverse "Ar*v*" --strand georgian` takes >120 s and prints
eight spellings of the same word (*árubh, árrubh, árubhfh…*); `cahal --strand welsh` prints ~40
constraint lines for the `a` slot that all say "a/á"; Task 9's ratchets could not be generated
(hours per strand); `uv run pytest -q -m "not slow"` is 12:51 against a 58 s baseline.

## Task A — verification cost, example diversity, palette  (reverse.py, g2p_inverse.py)

- **A1 One forward run per candidate.** For `DESC` the forward result depends only on the IPA
  the spelling reads back to: no foreign strand's rules reference the orthography (`grep
  '@orth\|orth=' rules/{welsh,georgian,arabic-egy,dutch}.rules` is empty) and
  `inputs.infer`'s ending heuristics only set declension/gender, which `DESC` never uses.
  `spell()` already guarantees every returned spelling reads back to `candidate.segments`. So
  `verify` runs `_forward` ONCE per candidate (V-26/V-34 revised): `tried` counts candidates
  run forward; `cap` bounds that. `Example.spelling_index` stays (always 0 now) so the golden
  format does not move; document the revision in the `verify` docstring.
- **A2 Cheap spelling in verify.** `g2p_inverse.spell` gains keyword-only `silent: bool = True`
  (False = silent-free readings only: no ⟨fh⟩, no silent ⟨dh gh th⟩, no `VOWEL_PLUS_H` runs
  such as ⟨adh⟩) and `budget: int = _PROPOSAL_BUDGET`. `verify` calls
  `spell(segments, limit=1, silent=False, budget=128)`; a candidate with no silent-free
  spelling is skipped (does not count as tried). The Task 2 ratchet test keeps the defaults.
- **A3 Examined-candidate bound.** `expand` is consumed at most `4 * cap` times per word
  regardless of how many candidates are unspellable, so a word can never loop for minutes;
  `cap_hit` is true when either bound is reached.
- **A4 Palette (R5 revised).** `PALETTE` = the five short vowels, then their five long
  counterparts `aː eː iː oː uː`, then the ten consonants as before (20 entries; a `*` yields
  0, 1, 2 segments → 1 + 20 + 400 fillings). Update V-23 text in the plan.
- **A5 Report header wording.** `verified examples (N of M candidates tried; …)` where M is
  the number run forward; `candidate cap C hit` unchanged. Adjust golden tests.
- **Acceptance:** `time uv run strands reverse "Ar*v*" --strand georgian` < 30 s wall on this
  machine; its examples are ≥ 6 DISTINCT Irish IPA shapes (no two examples with the same
  `ipa` column); no example spelling contains ⟨fh⟩ or a silent ⟨dh gh th⟩; `ardmhaor`
  (/aːɾˠd̪ˠvˠiːɾˠ/ → *ardvyr*) is admitted by the pattern (`pattern_admits`) — whether it
  appears among the examples at cap 2000 is REPORTED in the task result, not required.

## Task B — report noise and descriptions  (reverse.py, g2p_inverse.py, plan V-31)

- **B1 Grouping (owner reverses ruling 4 of the review round).** Constraint lines group by
  `(kind, tag, description)` ONLY; `context` leaves the key. A line's rule ids are the union
  over the group, ordered by forward stage (substitute, repair, post-stress, respell) then
  line number, deduplicated; print at most 4 ids, then `+N`. The `exclusions` block lists
  ONLY (a) epenthesis sources and (b) `substitute`-stage steps that carry a context —
  repair/post-stress/respell contexts are noise for the reader — deduplicated by
  `(label, context)`. Deletion notes unchanged. Rewrite V-31's aggregation table to match.
- **B2 Silent readings out of descriptions and patterns.** `describe()` and
  `render_pattern()` use silent-free readings only (same set as A2's `silent=False`); the
  `VOWEL_PLUS_H` runs (⟨adh eadh agh …⟩) never appear in a description or a pattern.
- **B3 Vowel-set summaries.** When a slot's Irish alternatives (after un-substitution) cover
  every short vowel `{a ɛ ɪ ɔ ʊ}`, its description is `any short vowel` (plus ` (unstressed)`
  when every contributing source is a reduction/post-stress step); every long vowel → `any
  long vowel`; both → `any vowel`. Otherwise the per-run listing as now, but a run list longer
  than 6 items prints the first 6 then `…`.
- **B4 Positional readings labelled.** The `_liquid` cn/gn/mn ⟨n⟩ → /ɾˠ ɾʲ/ reading describes
  as `n (after c/g/m)`; readings restricted to `position="initial"` (eclipsis ⟨bhf⟩, ⟨mb⟩…)
  describe with ` (initial)`; `noninitial` ones with ` (non-initial)`.
- **Acceptance:** `strands reverse cahal --strand welsh --examples 0` prints ≤ 4 lines for
  the `a` slot; `Ar*v*` georgian's `v` slot prints exactly three sources (/w/-side, /vʲ/-side,
  inserted) plus at most one `%design` line for `v v -> v`; the golden tests are regenerated
  by hand and READ before committing (the diff must be explainable line by line).

## Task C — tests, ratchets, suite time, spec text  (tests/, ratchets/, docs/specs)

- **C1 Ratchets (spec §6 revised).** Per strand, two rates over `sources/irish/test-words.tsv`
  hand-IPA rows: `admits` = share of rows whose forward respelling, reversed with
  `--examples 0` machinery, yields a pattern that `pattern_admits` the row's own IPA (all
  rows; unmarked; cheap); `examples` = share of rows whose orthography (or any spelling that
  reads to the same IPA) appears among verified examples at `cap=200`, over the FIRST 12
  hand-IPA rows only, marked `slow`. Files `tests/ratchets/reverse-<strand>.json` with keys
  `admits`, `admits_n`, `examples`, `examples_n`; generated by the plan's Step-5 script
  (updated), committed. No floor.
- **C2 Session case.** `test_ardmhaor_is_admitted` (unmarked, must pass);
  `test_ardmhaor_verifies_for_the_session_case` stays, `slow`, and is a plain test if it
  passes after Task A, else `xfail(strict=True)` with the reason — report which.
- **C3 Suite time.** `uv run pytest -q -m "not slow"` ≤ 3 min wall. CLI tests that run
  verification monkeypatch `reverse.CAP` to ≤ 30 or pass `--examples 0`; no test outside the
  `slow` mark runs more than 200 forward candidates. Report before/after timings.
- **C4 Spec text.** Edit `docs/specs/2026-08-27-reverse-design.md`: §3.5 (one forward run per
  candidate; examined bound; palette with long vowels; silent-free spellings), §4 (grouping
  and exclusions per B1; header wording per A5), §6 (ratchets per C1; session case per C2),
  §7 R5. Keep the edits minimal and in the spec's voice.
- **Acceptance:** full `uv run pytest -q` (including slow) green; ratchet files present;
  `git diff --stat` shows no `rules/` change.
