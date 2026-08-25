# Review: stress and Irish engine (Tasks 12–20)

`uv run pytest -q`: **385 passed, 1 xfailed**.

## Required fixes

1. **`src/strands/poststress.py:54-61` — Track whether any individual rule changes segment count, and preserve the stressed nucleus from the pre-edit word through all edits.** The code compares only the initial and final lengths, so an insertion plus deletion with net zero length skips required re-syllabification. It also computes the stress anchor only after edits; deleting a stressed syllable's onset drops `Word.stress`, so the surviving nucleus becomes unstressed. Both violate Task 16's interface (“re-syllabify … if any rule changed the segment count, preserving the stressed syllable's identity”). Add failing tests such as: (a) on stressed `pat`, `0 -> i / # _ p` followed by `t -> 0 / _ #` must re-syllabify `ipa` as `i.ˈpa`, not retain one stale syllable as `ˈipa`; (b) `p -> 0 / # _` on `ˈpat` must produce stressed `ˈat`, not unstressed `at`.

2. **`src/strands/irish.py:225-241` — `GEN()` ignores `Entry.gen_ipa` and always derives a regular genitive from the nominative.** Consequently a user-supplied irregular genitive is dead input, and the engine silently regularizes it despite the spec's explicit `gen_ipa` field and its non-goal of being a general Irish declension engine. This will affect `GEN`, `PATRO_O`, `PATRO_NI`, and `OF`. Add a failing test where `Entry(ipa="mˠak", gen_ipa="mˠəkiː", declension="m1")` passed through `build_construction("GEN", ...)` yields the supplied and normalized `mˠəkiː`, not derived `mʲɪc`; nested mutation templates should mutate that supplied form.

3. **`rules/irish.rules:255-303` — `[normalize]` leaves unmarked consonants in clusters unnormalized.** The rules only cover a consonant directly before a vowel or word-final directly after one. Inputs such as `stra`, `skri`, and `ant` retain plain `s/t`, `s/k`, or `n/t`, contradicting spec §4.1 (“every consonant gets ʲ or ˠ”) and the digest's rule that consonant clusters generally share quality. This leaks quality-less consonants into target substitution and fallback. Add failing tests asserting broad `stra -> sˠ t̪ˠ ɾˠ a`, slender `stri -> ʃ tʲ ɾʲ i`, and final-cluster propagation, while retaining explicit-quality mismatch exceptions unchanged.

4. **`src/strands/inputs.py:197-221` — Inference classifies and inflects raw IPA instead of the accepted normalized Irish form.** Alias or unmarked input therefore gives wrong declension and noncanonical `gen_ipa`: for example feminine `bˠɾˠoːg` is classified as default `m1` because final ASCII `g` is not in `BROAD`, and `mak` infers `mɪc` rather than normalized `mʲɪc`. Since Task 19 deliberately accepts aliases and quality-less consonants, Task 20 must normalize before `_final_quality` and before regular inflection (without adding source stress to the stored `gen_ipa`). Add failing tests for alias-final `g` inferring `f2` and for unmarked `mak` producing canonical `mʲɪc`.

## Suggestions

- The scoped tests contain no `or True` or `assert True`. The sole xfail is strict, names the exact Cairene digest row, and is explicitly permitted by Task 14; keep it visible until the transcription/length discrepancy is resolved.
- `tests/test_stress_framework.py:66-68` catches `(StressError, Exception)`, which is equivalent to catching any exception. The later direct-dispatch test is specific, but this parser-path test would be more informative if it asserted the intended parse/check exception type.
- Preserve explicit evidence of the red test run for future tasks. The scoped feature commits contain tests and implementation together, and the build log does not record the required fail-first runs, so repository history cannot verify TDD order even though the tests themselves are substantive.
