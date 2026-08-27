# Required fixes

- `src/strands/oldirish.py:138-143` — `infer_stem()` deliberately erases every declension produced by the normal input inference pass whenever an assumption starts with `declension:`. This contradicts the approved Task 12 interface, which says to read `Entry.declension`, and the strand spec's mapping from modern declension to Old Irish stem class. It changes real outputs for blank-stem lexicon rows: ordinary inferred `d4` entries such as `Ailbhe` are treated as o-stems and `GEN` produces `Ailbi`, while the specified mapping is `d4 -> indecl` and should leave the form unchanged. Add a failing end-to-end test using an entry passed through `inputs.infer` (not an explicitly supplied `declension`) and assert both the selected `indecl` stem and unchanged genitive.

- `src/strands/oldirish.py:383-389` — article sandhi before initial `s` applies two incompatible markings: the noun is first lenited to `ṡ-`, then the article is changed to `int`, yielding forms such as `Níall int ṡléibe`. Digest §10.4 gives the sandhi forms explicitly as `int sléibe` and `int súil`; the `t` realization replaces the ordinary written lenition here rather than accompanying punctum `ṡ`. Add a failing `OF` test with neuter `sliabh -> sléibe` expecting `int sléibe` (and the corresponding reconstructed initial, not `/h/`), then special-case the `s` sandhi before applying/rendering the noun mutation.

# Suggestions

- `tests/test_oldirish_grammar.py:242-253` — the tests named `test_mael_and_gilla_do_not_lenite` and `test_cu_and_ingen_do_lenite` exercise only `MAEL` and `CU`; `GILLA` and `INGEN` are not asserted. Split these into four tests with visible mutation controls (`C-`, `S-`, or `F-` initials).

- `tests/test_oldirish_grammar.py:263-266` — the `COLOUR` test asserts only that there is no space and uses the synthetic output `dubthech`; it does not test either source target named by the plan (`Dubthach`, `Donnchad`) or verify compound lenition. Add exact golden outputs for five rows per formation template, including capitalization, genitive selection, and mutation.

- `tests/test_oldirish_grammar.py:107-120` — the docstrings still claim `44/49` and `135/163`, while the implementing commit records `125/159` and the current mismatch scan finds 34 failures. Recompute and state one current numerator/denominator so the ratchet is auditable.

- Full suite: `1613 passed, 2 skipped, 3 xfailed` in 55.35s (`uv run pytest -q`).
