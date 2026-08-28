# Review of notes/report-2026-08-25-engine.md (guided tour, 2026-08-25)

Reviewer verification actually run (worktree `.worktrees/phonotactics`, HEAD `546a96b`):
all four "Try it" commands; `strands run` over the six report words (dialect C, `--strand all
--construction DESC`); `uv run pytest -q`; the rule files, the plan's Known-deviations list and
the four review files behind each "decision" claim.

---

## 1. Inaccuracies

**A. Decision 4 (ejectives) is wrong in two of its three clauses. — the only material error.**

Report: "Ejectives in the feature table carry both `+ejective` and `+constrictedGlottis`
(PHOIBLE does), so a rule written `[+ejective]` reaches nothing; **Georgian rules write both
features**. Cosmetic, but it's why the Georgian file reads oddly in that block."

- There is no feature named `ejective`. The column is **`raisedLarynxEjective`**
  (`rules/features.csv` header, col 39); `constrictedGlottis` is col 36. `[+ejective]` would
  not "reach nothing" — it would be a parse error on an unknown feature.
- Georgian rules **do not write both features**. They write no feature bundle at all:
  `rules/georgian.rules:118-121` is seven explicit segment→segment lines
  (`p -> pʼ / C _`, `t -> tʼ / C _`, `k -> kʼ / C _`, `tʃʰ -> tʃʼ / C _`, then `p -> pʰ`,
  `t -> tʰ`, `k -> kʰ`). The file's own comment (line 116-117) states the reason: a bundle
  `[STOP -voice] -> [+ejective]` is `UNREACHABLE_CHANGE` because PHOIBLE's `pʼ` differs from
  `p` in *more than one* feature.
- Verified: `p` and `pʼ` differ in exactly `constrictedGlottis` and `raisedLarynxEjective`
  (both `-` → `+`), so the underlying premise (one feature is not enough) is sound; the
  consequence stated in the report is not what the file does.
- Therefore the closing clause ("why the Georgian file reads oddly in that block") explains the
  wrong oddity. The block reads as a hand-written segment list, not as a double-feature bundle.

Recommendation: cut the bullet outright (see §3) and spend the Georgian slot on the aspirate/
ejective decision (see §2, omission C).

**B. Decision 1: "~30 lines, one block" — it is two blocks in two sections.**
The Welsh length carve-out is 20 conditioned shortening lines in `[substitute]`
(`rules/welsh.rules:135-154`, 5 vowels × 4 environments = the complement of `_ {n l r} #`)
**plus** 6 lines in `[post-stress]` (`rules/welsh.rules:366-371`: the identity tag-carrier
`a -> a / ˈ C* _ {n l r} #` and five unstressed-ultima shorteners). 26 rule lines, ~30 with
comments — but dropping it means editing two sections, not deleting one block. "Easy to drop"
still holds (the 20 lines collapse to 5 unconditional ones).
The output claims in that bullet are all correct: `Seán → siân`, `mór → môr`, `bán → bân`
(run and confirmed).

**C. Decision 2: "the clusters Irish mutations create are *exactly* the onsets Welsh's own
mutations create" overstates it.** Irish `sn-`/`sm-` are the exception and are deliberately
*not* admitted: Known Deviation 9(c) keeps them out and routes them through Morris Jones's
prothetic y-. Confirmed by running: `sneachta` → **ysnachta** [əs.ˈnaχ.ta], not *snachta*.
Suggest "almost exactly, except Irish s+nasal, which takes a prothetic y- (*sneachta* →
*ysnachta*)" — the exception is visible in the gallery, so it is worth the half-line.

**D. "each task test-first with its own commit" is asserted, not established.**
Three of the four reviews say the opposite is unverifiable: "the commits contain tests and
implementation together, so repository history alone cannot verify that each test was actually
observed failing first" (review-core; near-identical in review-stress-irish). The reviewers did
confirm the tests are substantive and free of `or True` / `assert True` abuse. Either soften to
"test-first by instruction; reviewers confirmed the tests are substantive" or drop the clause
as process (§3).

**Everything else checked out.** Specifically:

- All 24 table cells reproduce exactly under `strands run --strand all --construction DESC`
  with the stated IPA and dialect C. (The earlier draft's two placeholders are now filled
  correctly: Georgian *kviara*, Dutch *kiere*.)
- Test count: **862 passed, 2 xfailed** (7m30s) — matches.
- All four "Try it" commands exit 0 and do what the comment says; `explain` prints one line per
  rule with `%attested`/`%design` tag and a `[bibkey p.N]` / `digest §N line L` citation.
- `sources/irish/test-words.csv` holds exactly 144 data rows.
- Decision 3: `tests/test_rules_dutch.py` now asserts `rate("C") >= 0.7714` (27/35) and
  `rate("E") >= 0.1538` (4/26) as ordinary assertions, with `test_ratchet_does_not_slip`; the
  eight named Mode C misses are seven French final-stress loans plus `roos`. Correct.
- Decision 5: `rules/irish.rules:27,36,40` — `BROAD` contains `k ɡ x ɣ ŋ`, `SLEN` contains
  `c ɟ ç j ɲ`, `BROAD_MARKED` excludes plain `k ɡ` so they cannot re-mark. Correct, and
  *Ciara* → Georgian *kviara* confirms the consequence.
- Welsh `sonority = off` (`rules/welsh.rules:233`) — correct, and the file gives the report's
  reason (the whitelists are complete; soft-mutation `wl wr wn` fall in sonority).
- The three defects and the dialect-gating / *stríoc* costs are accurately stated; the fix
  commits (`352f8fb`, `9762863`, `73141f4`, `81d7637`) match.
- The one thing the fix agents refused is correctly surfaced: `3117381`'s "Not applied: the
  Dutch Mode C / Mode E xfails … left for the user", which decision 3 then resolves. No other
  required fix was rejected in any of the four reviews.

---

## 2. Important omissions

**A. Cairene respelling uses dot-under emphatics — against the source's own advice.**
The report's own table shows *maṭaanakh* and *laṣarkhuṣ*. Known Deviation 6: "Cairene
dot-under respelling **contradicts §5's own recommendation of plain letters**; kept as decision
9.11, cited as design." It also sits badly with the owner's standing decision that romanization
is *English-reader respelling* for all five strands (project-goals, decision 3 of 2026-08-24) —
`ṭ` and `ṣ` are exactly what an English reader cannot pronounce. This is the most likely thing
in the table for the owner to object to, it is one line of `arabic-egy.rules [respell]` to
change, and the report does not mention it. **Add it as a decision bullet.**

**B. "Which Welsh" — the Southern target is running on partly North evidence.**
Known Deviation 3: the syllable template is the digest's `(C)(C)(C)V(V)(C)(C)` **marked
(North)**. Known Deviation 9(a): the tier-A stop+liquid statement leans on `jipa-north p.505`
alongside `breit2019`. The owner already has "Welsh which-Southern … CONFLICT" as an open
project question (project-goals). One clause in the Welsh gap bullet would close the loop;
right now the Welsh gaps read as only "Awbery's tables pending".

**C. The Georgian /p t k/ default is the decision that shapes strand 4's harshness, and it is
contra the digest.** `rules/georgian.rules:111-121` + Known Deviation 4: the file follows spec
§9 row 4 (aspirate by default, ejective only post-consonantally), tagged `%design` with a
`contra` note, while digest §3.1 lines 862-868 explicitly recommends the **unconditional**
ejective and says of exactly this environment split "That is not what the source supports".
The owner did pick the measured pattern on 2026-08-24 (project-goals decision 4), so this is
not a surprise — but it is (a) the single biggest lever on whether strand-4 output sits beside
*Kas'queil* / *Th'tysh*, and (b) the one place the build knowingly runs against its source.
Worth one bullet, in place of the (incorrect) ejective-features bullet.

**D. Georgian has no syllable template and no declared nuclei.**
`rules/georgian.rules:130-135`: the stem, not the syllable, is the phonotactic domain, and the
stem-edge inventories are the whitelists; no `nuclei` means hiatus is preserved. That is why
every Georgian output in the table has bare vowel sequences (*kviara*, *grania*, *niav*) and no
stress mark. One clause; it pre-answers the "why does Georgian look like that" reaction the
gallery hour will produce.

**E. (Minor, optional) The `%attested` tags on the Georgian collapse rules are unaudited.**
review-targets' open suggestion: `rules/georgian.rules:88-97,108-109` tag Irish broad/slender →
single-target mappings `%attested` on evidence that is target-inventory/allophony, not an
adaptation claim; a final tagging audit was suggested and not done. Since "every cell is
traceable … with its tag" is the report's traceability claim, half a sentence of caveat is
honest. Skip if space is tight.

Deliberately **not** recommended for inclusion (checked, judged not owner-facing): the
`derived_class` scope suggestion in review-core (still computed over the whole feature table as
a documented stand-in, `src/strands/dsl.py:944-949`); the identity of the 2 remaining xfails
(one Cairene stress row, plan-permitted; that is the only real one); Known Deviations 1, 2, 5,
7, 8 (already covered by the gaps section or settled).

---

## 3. Cut / compress

- **Decision 4 in full** — wrong (§1A) and self-described as "cosmetic". Replace with omission
  C above. Net zero length, large gain.
- **The build-path sentence** (lines 7-10): "spec (approved in chat, §12 amendments after plan
  review) → plan (3 drafts, GPT-5.6 + Opus reviews) → 40-agent workflow, each task test-first
  with its own commit → four cross-family reviews with fixes → my own verification pass". This
  is entirely process. Compress to one clause: "Built by a 40-agent workflow against a reviewed
  plan; four review passes plus my own verification found and fixed three defects." (Also
  removes the unverifiable test-first claim, §1D.)
- **"(4 commits, … tree clean)"** (line 71) — process. Keep "suite 862 passed / 2 xfailed".
- **"~30 lines, one block"** (line 41) — the count is filler and the "one block" part is wrong
  (§1B). "Easy to drop (two short blocks in `welsh.rules`)" carries the whole payload.
- **"Recorded as Known Deviation 9"** (line 48) — keep; it is a pointer, not detail.
- Consider dropping **"(my call, low stakes)"** in decision 3: the bullet then either earns the
  owner's attention or does not, and the parenthetical only invites a re-read.

Everything else is at the right altitude. The report is short (94 lines) and the gaps and
next-step sections are already well-compressed; do not lengthen them beyond the two clauses in
omissions B and D.

---

## 4. Ready?

**Not yet — one revision, ~20 minutes.** The table, the test count, the commands, the defects
and three of the five decisions all verify exactly, which is most of the report's value. But
one of the five "decisions yours to revisit" is factually wrong about what the code does
(§1A), and the most likely thing in the report's own table for the owner to object to — the
Cairene `ṭ`/`ṣ` respelling, which contradicts both the source's recommendation and the owner's
own romanization decision — is missing (§2A).

Required before showing it: fix or cut decision 4; add the Cairene respelling bullet. Strongly
recommended: swap in the Georgian aspirate/ejective decision (§2C), add the one-clause Welsh
North-provenance caveat (§2B), and apply the §3 cuts. After that it is ready.
