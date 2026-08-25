# GPT-5.6 plan-reviewer findings on plan draft 1 (saved verbatim by the lead)

P1 Repair loop skips mandatory active rules and can't clear illegality after count-preserving
   repairs → run [repair] unconditionally once per pass; re-syllabify after any change;
   continue only while illegal marks remain and progress is made; cycle detection + cap.
P1 Dependency failures: Task 6 needs Task 12's PROCEDURE_PARAMS (mini fixture `window=3`
   contradicts penult having no params); Task 17's vocative test expects /ç/ produced only by
   Task 19; Task 19 modifies irish.rules created by Task 17; Task 18 needs 19; Task 27's tests
   need 23–26; Tasks 13–15 all edit stress.py.
P1 Diphthongs as two nuclei breaks Irish/Welsh/Dutch (13 test rows); need nucleus grouping
   per language; Georgian forces hiatus.
P1 Mode L bypasses substitution, fallback, repair, post-stress, affixation, respell — keep it
   but call it inventory/syllable/stress conformance; add per-target parametrized repair
   tables (post-substitution IPA → post-repair IPA + trace entry): Welsh pobl/ffenestr/ewythr;
   Cairene ski/street/banknote/group; Dutch melk/hart/hand; Georgian class (degemination),
   cluster fallback tested synthetically.
P1 Respell grammar forbids the `. -> ""` cleanup rules the plan requires; define respell
   over annotated tokens with opaque output chunks; strip marks in code.
P1 Feature-change bundles must be exact lookup; approximation only in fallback stage.
P1 Onset/coda lists: contradictory singleton semantics in fixtures; define as complete sets
   incl. singletons.
P1 Georgian "nearest attested cluster" has no mechanism; define or drop.
P2 Georgian Mode L denominator is 122 (rows with target_ipa), not 143.
P2 Target-rule tasks are ordered code-first; must be test-first.
