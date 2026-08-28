# `strands reverse` — fix round 2 (owner rulings 2026-08-27, after commits b4eee86…7f5605e)

Overrides `2026-08-27-reverse-fixes.md` where they conflict. One task; test-first; full suite
green; no `rules/` or forward-stage change; fast suite stays ≤ 3 min.

- **D1 Examples: one per Irish candidate, not per foreign shape.** Ruling A2's "no two examples
  with the same ipa column" was wrong for literal (non-glob) patterns, where every match has
  the same foreign shape and the reader wants to see *which Irish words* reach it (`cahal`
  must list *Cathal*). `verify` de-duplicates by `candidate.segments` only (already distinct
  from `expand`), never by foreign IPA. Drop `test_no_ipa_shape_is_printed_twice`; keep the
  "≥ 6 distinct shapes for `Ar*v*`" test only if it still holds — report. The Task C `examples`
  ratchet becomes meaningful with this change: regenerate all four `reverse-<strand>.json`.
- **D2 Grouping: `(kind, description)`, attested wins.** Owner resolves the B1 conflict in
  favour of the first implementer's reading: constraint lines group by `(kind, description)`;
  the printed tag is the STRONGEST across merged routes (attested if any route is attested,
  else design, else fallback) — the line claims "this Irish spelling can produce this letter",
  and one attested route makes that claim attested. Rule ids merged as before. Turn the two
  strict xfails from 731e614 into the plain acceptance tests they encode
  (`cahal` `a` slot ≤ 4 lines; `Ar*v*` `v` slot ≤ 4 lines + at most one `/v/ + /v/` line — the
  `(non-initial)` split is accepted, so 4 sources is the bar now, not 3). Update spec §4.
- **D3 `possibly dropped`: one line per segment.** Merge by the deleted segment's label; ids
  merged and capped as constraint lines; the tag rule of D2.
- **D4 Spelling-pattern insertion lines cite ids, not context dumps.** The `or, with X
  inserted:` line ends `(repair:298 +4)` style — the first rule id in forward order, then
  `+N`; no context text (the exclusions block is where contexts live, and B1 keeps
  repair/post-stress contexts out of it deliberately).
- **D5 Pattern rendering must show the same runs as the constraint lines.** For `cahal`
  welsh the first vowel slot renders `((eá|ea|io|iu))?` while its constraint lines list
  `a, ea, ai, eai` and `á, …`. Find the cause (suspected: the renderer filters runs by the
  quality of a NEIGHBOURING slot that itself has both qualities, or takes the runs of only
  one alternative) and fix it so a slot's rendered alternation is the union of its
  alternatives' silent-free runs, capped at 6 with `…`, filtered by quality only when the
  neighbouring consonant slot admits a single quality. Also drop the doubled parentheses
  `((…))?` → `(…)?`. Add a test on the `cahal` pattern: it must admit the literal spelling
  `cathal` (write a small helper that turns the rendered pattern into a regex; `(x|y)`,
  `(…)?`, `*`, `…` → `[^ ]*`).
- **D6 Expansion bound.** `expand` is consumed up to `EXAMINE_FACTOR * cap` candidates
  (A3's bound) — currently `expand(pattern, cap=CAP)` binds first at 2000 produced, so only
  106 spellable candidates were tried for `Ar*v*`. Pass `cap=EXAMINE_FACTOR * cap` to
  `expand`; `tried` still bounded by `cap`; `cap_hit` means either bound. Report whether
  `ardmhaor` now appears in the `Ar*v*` examples at cap 2000 (limit 40); if it does, the
  session-case test loses its xfail. Keep `Ar*v*` wall time < 30 s (measure).
- **Goldens:** regenerate by hand, read every changed line, and explain each by D1–D6 in the
  commit body. **Ratchets:** regenerate; the `examples` rates must be > 0 for at least three
  strands after D1 (report the numbers).
