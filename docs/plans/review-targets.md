# Required fixes

- `src/strands/pipeline.py:180-182` — Sort flags (or otherwise preserve a defined order) before building `Result.flags`. `Word.flags` is a `frozenset`, and iterating it changes with `PYTHONHASHSEED`; the same input produced both `('AAA', 'ZZZ')` and `('ZZZ', 'AAA')` in separate processes, violating the byte-identical determinism requirement. Failing test to add: run the same two-flag adaptation in subprocesses under several hash seeds and assert identical serialized results.

- `src/strands/respell.py:29-41,65-74` — Represent zero-width respell insertions independently from the segment at the insertion point. A word-final rule such as `0 -> "Z" / _ #` currently fires in the trace but renders `a`, not `aZ`, because `_render` never visits `chunks[len(segments)]`; a word-initial insertion also folds the following segment into the opaque chunk and claims it, so `0 -> "Z" / # _` followed by `a -> "A"` yields `Za` rather than `ZA`. This violates the DSL epenthesis semantics and opacity rule. Add both failing cases to `tests/test_pipeline.py`.

- `src/strands/regress.py:282` — Do not round a ratchet floor upward. `write_ratchet()` can write a floor higher than the report that created it: a 2/3 report is saved as `0.6667`, after which `assert_ratchet()` immediately rejects the unchanged report (`0.666666… < 0.6667`). Store exact numerator/denominator or full precision, or round/floor in a direction that cannot create a regression. Add a round-trip test using a non-terminating rate such as 2/3 and call `assert_ratchet()` after writing.

- `tests/test_rules_dutch.py:241-278` — Meet Task 26's acceptance criteria instead of disabling them and weakening the cap. The committed target has Mode C `0.7428` rather than the required `>= 0.80`, Mode E `0.12` rather than `>= 0.25`, and 7 error rows rather than the required `<= 6`; both bar tests are strict xfails and the error assertion was changed to `<= 7`. These tests make the suite green while the task remains unaccepted. Fix the rule/data-cleaning or harness treatment, then make the specified thresholds ordinary passing assertions.

- `tests/test_welsh_rules.py:334-348` — Restore Task 25's required 19-row Mode C denominator and zero error bucket. The implementation accepts four consonant-length-mark rows (`mapː`, `ʃopː`, `matː`, `klokː`) as tokenizer errors and silently rewrites the acceptance test to 15 Mode C rows / at most 4 errors, although the plan explicitly requires all 19 cleaned rows to reach Mode C and `error == 0`. Normalize the attested geminate notation to the engine's repeated-segment representation (I-2), or otherwise resolve the data representation without shrinking the denominator.

- `tests/test_welsh_rules.py:319-322` — Remove the unconditional `xfail` whose body is only `assert False`. It tests no behavior and permanently consumes an xfail merely to document that the digest lacks an IPA example; the real synthetic degemination behavior is already tested immediately below. Keep the limitation as a comment/metadata assertion, or replace it with a genuine executable claim.

# Suggestions

- Full test run: `uv run pytest -q` reports **677 passed, 5 xfailed** in 12.20s. Besides the three scoped xfails above, the Cairene stress xfail is the plan-required explicit inventory limitation.

- The 10-rule-per-target citation spot-check found the sampled rule text consistent with the cited digest passages. Georgian collapse rules at `rules/georgian.rules:88-97,108-109` use `%attested` for Irish broad/slender-to-single-target mappings whose cited §8.2 evidence is primarily target-inventory/allophony evidence; consider a final tagging audit against the strict “no adaptation claim => `%design`” rule, though the digest does state the proposed landing segments.
