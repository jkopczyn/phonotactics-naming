# Engine build log

- 2026-08-25: spec `docs/specs/2026-08-25-engine-design.md` (+§12 amendments) approved; plan
  `docs/plans/2026-08-25-engine-plan.md` draft 3 passed GPT-5.6 + Opus review (go).
- 2026-08-25: implementation workflow launched. Run ID `wf_d249d54e-971`; script
  `/home/jkop/.claude/jobs/5f09897a/tmp/engine-workflow.js` (job-scoped; copy in this file's
  history if the job dir is gone). Resume: `Workflow({scriptPath, resumeFromRunId})`.
  Structure: tasks 0–11 → review 'core' → 12–20 → review 'stress-irish' → 21–22 → 23a/24/25/26
  parallel → 23b → review 'targets' → 27–28 → review 'final'. Each task commits itself;
  reviews write `docs/plans/review-<name>.md` and a fix agent commits "fix: address review …".
