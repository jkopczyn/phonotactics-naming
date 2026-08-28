# Report: `strands reverse` (branch `reverse`, commits 5acf06d…9557fa0)

Claude-written tour for the owner. Ordered by how much each item needs your decision.

## Try it

```sh
uv run strands reverse "Ar*v*" --strand georgian          # the Ar'ovor case, ~27 s
uv run strands reverse cahal --strand welsh               # a literal word, < 1 s
uv run strands reverse "Cathal" --strand old-irish        # lexicon lookup only
uv run strands reverse "ɑr*v*" --strand georgian --ipa    # target IPA instead of respelling
```

Output per word: `constraints` (each target letter ← the Irish spellings that produce it, with
rule ids and `%design` where no attested route exists), `possibly dropped`, `exclusions`
(contexts of substitute-stage rules, verbatim DSL), an `Irish spelling pattern`, and
`verified examples` — concrete Irish spellings actually run through the forward engine, with
their respelling, IPA, flags and fallback count. Globs `* ? [aeiou]`; `--examples N` (default
8, `0` skips verification).

## Decisions I want from you

1. **Which spelling represents a candidate.** Each verified example is one Irish *sound shape*
   printed under its cheapest silent-free spelling. For welsh `cahal` the /kahəl̪ˠ/ shape (see
   point 2: `--examples 11` to reach it) prints as *cahal*, never *Cathal* — both read
   /kahəl̪ˠ/, and ⟨th⟩ for /h/ ranks 13th among the 60 silent-free spellings. Options:
   keep (simplest); print two or three spellings per shape; prefer spellings with the "usual"
   Irish graphemes (⟨th⟩ for /h/, ⟨bh/mh⟩ for /v w/) via a small preference table. I lean to the
   preference table — it is what makes a guess look like an Irish word.
2. **Example ranking.** Candidates come out cheapest-first by rule kind (identity < attested <
   design < fallback), so for `cahal` the long-vowel *cáhál* leads and the short-vowel shape
   is 11th, past the default 8. Ranking by "fewest long vowels / fewest design routes" would
   put the plain shape first. Cheap to change; I have not.
3. **The session case — a real open call.** `Ar*v*` on georgian lists the `v` sources you
   found by hand (broad *bh/mh* twice, /vˠ/ non-initial and /w/; slender *bh/mh*; inserted *v*
   before a front vowel after a broad non-labial C, with its context under `exclusions`), plus
   a `%design` /v/+/v/ line. *ardmhaor* is admitted by the pattern (tested) but is not among
   the eight examples. The diagnosis is **enumeration order, not the cap**: every piece is on
   offer (first `*` = /d̪ˠ/, second = /iːɾˠ/), but each `*` has 421 fillings (0, 1 or 2 of a
   20-segment palette) and the two-segment ones are enumerated last, so the cross product is
   walked depth-first and never reaches that corner. 608 candidates were tried before the cap.
   A bigger cap (or the spec's unbuilt `--cap` flag, R4) does not fix it; interleaving the `*`
   fillings — breadth over the cross product — would. Left as a strict xfail carrying this
   diagnosis. **Your call**: leave it, or spend a task on the interleave.
4. **Noise level.** The constraint lines carry up to 4 rule ids then `+N`; the welsh `a` slot
   is 4 lines because Welsh reaches /a/ by ~20 post-stress and substitute routes. Say if you
   want the ids trimmed further (one id per line), the exclusions block dropped, or the
   `possibly dropped` block dropped — for welsh it lists six segments, each "anywhere in this
   word", which is true but carries little information.

## What it is, briefly

`src/strands/reverse.py` (1.9k lines) inverts the rule data: `[respell]` → chunk map;
`[substitute]` + inventory fallback → source map (class/bundle targets expanded over the Irish
inventory; feature-change replacements applied per segment; chains only in file order, so
Arabic `dʒ→ʒ` never chains into the earlier `ʒ→ʃ`); `[repair]`/`[post-stress]` only *widen*
slots and turn insertions into atomic optional groups. Contexts are never evaluated during
inversion (decision R2) — they are printed, and the forward engine is the oracle: every
example is a real `run_entry(..., "DESC")` whose respelling fnmatches the pattern. One forward
run per candidate (the output depends only on the IPA for `DESC`).
`src/strands/g2p_inverse.py` (0.6k) is the reverse g2p: a registry of every reading path in
`g2p.py` (tables and procedural branches, incl. Connacht /w/→/vˠ/), a caol-le-caol run matcher,
and `spell()` which only returns spellings `g2p` reads back to the same segments.
No rule file or forward stage changed (`g2p.py` gained public aliases only).

## Known limits (documented in spec §3/§7 and the plan's Known risks)

- Deletions are never re-inserted (`possibly dropped` lists them); a repair insertion whose
  first segment the respelling then deletes (Arabic `0 → ʔ i`, `ʔ → ""` initially) is an
  accepted miss.
- Caol le caol is over-generated in the *pattern* line when a neighbouring consonant admits
  both qualities; `verify` still checks it.
- Round-trip ratchets over `test-words.tsv` (no floor, regression-only): the row's own IPA is
  admitted by the reversed pattern for welsh 67 %, georgian 72 %, arabic 71 %, dutch 51 % of
  133 rows; the row's spelling (or a homophone) appears among examples at cap 200 for
  2/11, 5/11, 5/11, 0/11 of the first twelve rows. Dutch is low on both — its `[post-stress]` reductions and
  cluster repairs widen slots the most; not investigated further.
- Old Irish: fnmatch over the lexicon's Old Irish forms only; the retro grammar is not inverted.

## Process and cost

Spec (`docs/specs/2026-08-27-reverse-design.md`) → plan (`docs/plans/2026-08-27-reverse-plan.md`,
two GPT review rounds before implementation) → 9 Opus tasks each with a GPT review → two fix
rounds (`…-reverse-fixes.md`, `…-reverse-fixes-2.md`) after I read the first output: it was
correct but far slower than needed (one forward run per *spelling*), printed 40-line constraint
slots and eight spellings of one word. 25 commits, +5.1k lines (of which ~2.2k tests). Suite:
1958 passed, 2 skipped, 3 xfailed; fast pass (`-m 'not slow'`) 92 s, full 2 m 41 s — against a
58 s baseline before this work.
