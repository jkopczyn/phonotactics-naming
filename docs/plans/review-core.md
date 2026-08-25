# Core engine review (tasks 0–11)

`uv run pytest -q`: **203 passed in 0.31s**.

## Required fixes

1. **`src/strands/syllabify.py:284-295` — `onset-required = yes` is enforced only on the first syllable of each domain.** Hiatus creates an empty onset in `_split_interlude`, but `legal_onset(())` always returns true, so `aa` is accepted except for the first vowel (`illegal == {0}`) rather than marking the second onsetless syllable too. Spec §12.D says the empty onset is allowed *unless* `onset-required = yes`, not merely word-initially. Add a failing test with `onset-required = yes`, no licensed nuclei, and `aa`; segment 1 must be illegal (and similarly after a diphthong followed by a vowel).

2. **`src/strands/check.py:149-166` — static reachability checks only the first item of a multi-segment feature-change target and accept the rule if any candidate succeeds.** At runtime `rewrite._replacement()` applies the change to every matched segment, so `strands check` can exit clean and the checked file can then crash. Reproducer: `[inventory] a b; [substitute] a b -> [+syllabic]` produces no check finding, but applying it to `ab` raises `RuleError` for `b`. Check every segment that each target position can match (not just `r.target[0]`) and report `UNREACHABLE_CHANGE` if any reachable match position can fail; add this reproducer as a checker test.

3. **`src/strands/features.py:61-65,113-126` — exact feature changes choose the first duplicate vector in TSV order, which can emit a noncanonical alias.** Because ASCII `g` precedes `ɡ` and shares its vector, `TABLE.apply_changes("k", {"voice": "+"})` returns `g`, contrary to plan I-34's target spelling canon (`ɡ`; ASCII `g` is the Irish-input duplicate). This can create a spurious inventory fallback and increment the fallback count for an exact, ordinary voicing change. Make exact lookup choose the canonical/principal segment rather than an input-alias row (or make the lookup inventory-aware without compromising determinism), and add the failing assertion `apply_changes("k", {"voice": "+"}) == "ɡ"` plus equivalent alias-vector cases.

4. **`src/strands/word.py:103-108` — insertion at a morpheme boundary always leaves `$` before the inserted material, even when the rule inserts on the left side of `$`.** For `Word(("p",), morphemes={1})` and `0 -> i / p _ $`, the result is `pi` with boundary `{1}` (`p$i`) instead of `{2}` (`pi$`). Conversely, `$ _` insertion does need the current behavior, so `Word.replaced()` alone lacks enough directional information. Preserve the side of the boundary in rewrite application (or explicitly encode insertion affinity), and add tests for both `p _ $` and `$ _ p`; otherwise later repair/epithet rules that inspect `$` see the wrong morpheme.

5. **`src/strands/dsl.py:672-677` and `src/strands/check.py:201-208` — `[syllable] nuclei` accepts consonant-containing sequences and then silently ignores them.** The DSL/spec defines nuclei as licensed vowel sequences, but `nuclei = pa` parses and checks clean as long as both segments are in the inventory; `group_nuclei()` later refuses to group it because of its private vowel guard. Reject or statically flag every declared nucleus containing a non-vowel segment, with a failing parser/check test for `nuclei = pa`, so a misspelled rule cannot silently change syllable count and stress.

## Suggestions

- **`src/strands/dsl.py:403-423`** — reject duplicate/contradictory feature specifications such as `[+voice -voice]` instead of silently taking the last dictionary value.
- **`src/strands/dsl.py:926-935`** — validate weights against the plan's `number` grammar and reject non-finite values (`nan`, `inf`); currently `float()` accepts both.
- **`src/strands/dsl.py:939-945`** — derived classes are computed over the entire feature table, not the rule inventory plus Irish inventory required by I-11. This broadens `C/V/...` to unrelated target-only segments; introduce an explicit shared Irish inventory when Task 17 makes it available.
- **`tests/test_syllabify.py:40-42`** — `test_minimal_illegal_span` only asserts that something noninitial is illegal; assert the exact minimal span so over-marking regressions cannot pass.
- No `or True`, `assert True`, `xfail`, or skip abuse was found in the task 0–11 tests. The determinism tests are simple repeated-call comparisons but are not tautologies. The commits contain tests and implementation together, so repository history alone cannot verify that each test was actually observed failing first.
