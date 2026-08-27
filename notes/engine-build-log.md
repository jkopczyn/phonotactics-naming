# Engine build log

- 2026-08-25: spec `docs/specs/2026-08-25-engine-design.md` (+§12 amendments) approved; plan
  `docs/plans/2026-08-25-engine-plan.md` draft 3 passed GPT-5.6 + Opus review (go).
- 2026-08-25: implementation workflow launched. Run ID `wf_d249d54e-971`; script
  `/home/jkop/.claude/jobs/5f09897a/tmp/engine-workflow.js` (job-scoped; copy in this file's
  history if the job dir is gone). Resume: `Workflow({scriptPath, resumeFromRunId})`.
  Structure: tasks 0–11 → review 'core' → 12–20 → review 'stress-irish' → 21–22 → 23a/24/25/26
  parallel → 23b → review 'targets' → 27–28 → review 'final'. Each task commits itself;
  reviews write `docs/plans/review-<name>.md` and a fix agent commits "fix: address review …".
- 2026-08-25 (Targets phase): Task 25 (welsh.rules) ruling — the plan's onset tiers A–D
  excluded stop+liquid (a data artefact of closed sources); ruled: admit stop+liquid onsets
  (cite wiki-cy-phon), admit the Irish-mutation-generated onsets that Welsh's own mutations
  produce (ml mr nl nr ŋl ŋr; χr χl θr; wl wr) as attested-under-mutation, sC- via decision-15
  prothesis, `h -> 0 / #_[NAS]` %design, cluster-fallback retained as last resort only. Welsh
  Mode C denominator is 15 (four rows carry consonant ː unlicensed by features.tsv).
- 2026-08-25 17:30: workflow complete (40 agents; one API drop at 23b, resumed). Suite 841
  passed / 4 xfailed. Verification found: dorsal normalization overriding explicit broad k/ɡ
  (Cʷ never fired on dorsals); `h -> ç` overreach on lenited th-/sh-; dutch-weight stressing
  schwa; Dutch bars waived by xfail. Fix agent dispatched; Dutch bars restated (C ≥ 27/35,
  E ≥ 4/26, ratchet-held) by owner-default decision.
- 2026-08-25 evening: Georgian tuned in three single-variable steps, each with before/after
  gallery diffs: (1) `cluster-legality = pairwise` (28010a3; Butskhrikidze: constraints are
  pairwise) — 6 words rescued from bad fallbacks; (2) Cʷ left as is by owner choice (drvim,
  sp'rvi preferred); (3) `cluster-fallback = keep` + `overlay-undo = v` (895bf4f, 7e40ef8,
  8220ea5) — unattested clusters kept and flagged UNATTESTED_CLUSTER, no substitution;
  Georgian fallbacks 108 → 14 cells, Mode C 0.807 → 0.832. Welsh: Awbery pass (ab6a3f1,
  84e4b54, 151f309) settled Llanwrtyd = Southern and the penult length rule; CONFLICT-Awb-3
  resolved by owner decision (8974c34): final /m/ lexical (Irish length decides, circumflex),
  /ŋ/ short. Suite 941 passed / 2 xfailed.
- 2026-08-26: multi-word inputs fixed (d457f46: words adapted separately, joined with a
  space — 11 test rows × 4 strands changed); /ɪə/ normalized to /iə/ (b11051a); Cairene
  emphasis narrowed to Hafez's environment, before back vowels only (65af470; 18 DESC rows
  lost an emphatic, Matánach/súil keep theirs). Suite 1001 passed / 2 xfailed.
- 2026-08-26: Welsh gallery reviewed by owner; decisions: keep /iə uə/ → ɪ ʊ (Brian → Brin),
  keep native Welsh spelling (f = /v/, w = /ʊ/) — no English-reader respelling variant.
  Dutch gallery not yet reviewed by owner. Tool declared ready for trial use on real names.
