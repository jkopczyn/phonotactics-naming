# `strands reverse` — implementation plan (draft 4)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development
> (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Draft 3** (2026-08-27) applies the second review's five P1s and one P2 on top of draft 2. The
changes: the ordered-chain **positive** case is Georgian `pˠ -> p` → `p -> pʼ / C _`, because the
spec's Welsh illustration is not a chain in the file (V-28); the two-segment insertion `0 -> ʔ i` is
unreachable behind `arabic-egy`'s `ʔ -> "" / # _`, so it is a **recorded accepted miss** and the
atomic-group tests move to a synthetic fixture (V-30); `un_substitute` now **plumbs the substitute
deletions and notes into the `Pattern`**, which draft 2 dropped (V-7); collapsing a multi-step
alternative to one `ConstraintLine` is now **fully specified** — kind from the substitute step, tag
the weakest, context and rule ids in forward stage order, one exclusion line per context-bearing
step (V-31); `section_inventory` returns exactly `tuple(target.inventory)` and never touches the
`marginal` frozenset (V-29); and Task 9's full regression is a **session-scoped fixture** so the
`slow` marker actually saves the time.

**Draft 2** (2026-08-27) applied the eight P1s and one P2 of the first adversarial plan review, plus the
owner's ruling on deletion notes. The changes are: the reverse g2p is now a **grapheme reading
registry** over *every* forward emission path, not an inversion of two tables (F1, V-27); chain
closure honours **rule order** (F2, V-28); `[repair]`/`[post-stress]` expand over the **target**
inventory (F3, V-29); insertions widen **slot spans as atomic optional groups** (F4, V-30);
alternatives carry **structured provenance** and the report groups on context (F5, V-31); the report
has **one line formatter and golden tests** (F6, V-32); `--ipa` has a **real parser** (F7, V-33);
`verify` iterates **all** spellings with de-duplication (F8, V-34); the ratchets are measured at the
spec's **cap 2000** behind a `slow` marker (F9); and deletion notes are **once per word** (owner
ruling, V-7 revised). Interpretation numbers are stable across drafts — nothing was renumbered.

**Goal:** a `strands reverse PATTERN --strand X` command that, given a strand and a target
respelling (possibly a glob), reports the **constraint set** — which Irish spellings produce each
target letter, what is unconstrained, what is excluded — then an Irish spelling pattern, then a few
forward-verified concrete examples.

**Spec:** `docs/specs/2026-08-27-reverse-design.md` (approved 2026-08-27). It extends
`docs/specs/2026-08-25-engine-design.md`. Task format and the interpretation-register convention
come from `docs/plans/2026-08-25-engine-plan.md` (I-1…I-41, still in force) and
`docs/plans/2026-08-27-old-irish-plan.md` (O-1…O-33). This plan's own interpretations are numbered
**V-1…V-34** and implementers follow them, not their own reading.

**Tech stack:** Python ≥3.12, `uv`, `pytest`. No runtime dependencies (standard library only; the
verification step uses `fnmatch` from the stdlib). Every command runs through `uv run` from the
repo root. The system `python3` is 3.10 — do not use it.

**Working-tree baseline, measured 2026-08-27 on branch `reverse`:** `uv run pytest -q` →
**1680 passed, 2 skipped, 2 xfailed** in ~58 s. **No task may reduce it.** Run `uv run pytest -q`
before every commit.

**Global constraints**

- Nothing in `rules/`, `pipeline.py`, `substitute.py`, `respell.py`, `rewrite.py`, `irish.py` or any
  other forward stage changes behaviour. The only edits to existing forward modules are `g2p.py`
  gaining public aliases and a docstring paragraph (Task 1) and `regress.py` gaining one new
  function (Task 2) — no existing code path changes.
- Determinism is a hard requirement: identical input + data files ⇒ byte-identical output. Every
  set is turned into a sorted or file-ordered tuple before it reaches output.
- Files are UTF-8, NFC-normalized on read (I-1). Every pattern and every respelling is compared
  after `unicodedata.normalize("NFC", s).casefold()`.
- Test-first, always: every task writes its tests against an absent or skeletal artefact, runs
  them, watches them fail, and only then writes the artefact.

---

## Spec questions

Four places where the spec, read literally, is not implementable. Each is resolved below by the
nearest implementable reading; **none changes the spec's scope**, and each is flagged in the code
with the V-number so the owner can overrule it.

- **Q1 — the `exclusions` section (spec §4).** The example line
  `labial C before a front vowel does not trigger the inserted v (substitute:65 context)`
  is an English *negation* of a rule environment. Deriving negated English prose from a DSL context
  is not implementable, and R2 explicitly says contexts are carried **as text** and never evaluated.
  **Nearest reading (V-13):** `exclusions` lists, one line per context-bearing source, the source's
  own DSL environment verbatim, prefixed by the constraint it qualifies:
  `  v ← inserted, no Irish letter: only when  [BROAD -labial] _ [V +front]   (substitute:65 context)`.
  The heading and its position are the spec's; the sentence is machine-generated, not prose.
- **Q2 — the second "Irish spelling pattern" line (spec §4).**
  `(a|á)r*C(ao|ae|aoi|ia)*` is the *epenthesis* reading of the `v` slot, rendered by evaluating
  `substitute:65`'s context into Irish spelling. That is context evaluation, which R2 forbids.
  **Nearest reading (V-14):** print one rendering line; then, for each optional group that comes
  from an insertion, one extra line reading
  `  or, with <labels> inserted:  <rendering with that group dropped>   (context: <env text>)`.
  Same information, no context evaluation.
- **Q3 — the human gloss in the constraint column (spec §4).** `a ← a, á, or unstressed vowel (any
  short vowel)` and `broad non-labial C before a front vowel` are hand-written glosses.
  **Nearest reading (V-15):** the description column is generated by `g2p_inverse.describe()` from
  the Irish segments (`a, á` / `broad bh/mh`), plus a fixed phrase per source kind
  (`identity` → nothing, `fallback` → ` (nearest inventory match)`, `epenthesis` →
  `inserted, no Irish letter`). No hand prose is produced.
- **Q4 — `[!...]` glob classes.** The spec's glob grammar has `[aeiou]` but says nothing about
  `fnmatch`'s negation form, which the verification step's `fnmatch` *does* honour. Letting the two
  disagree would silently break the "every claim is forward-checked" guarantee.
  **Nearest reading (V-16):** a `!` or `^` immediately after `[` is a **usage error** (exit 2),
  message `reverse: [!…] classes are not supported`.

---

## Spec interpretations (V-1 … V-34)

### The three maps

- **V-1 The chunk map (spec §3.1).** `invert_respell(rf, table)` returns
  `(chunks: dict[str, tuple[RespellSource, ...]], notes: tuple[str, ...])`, where a key is the
  **casefolded output chunk** and `RespellSource = (segments, rule_id, tag, context, line)`. It is
  built from `rf.sections["respell"]` in file order:
  - replacement is exactly `(QuotedText(t),)` and every target item is `kind == "segment"` →
    key `t.casefold()`, segments = the target's values in order.
  - replacement is `(QuotedText(t),)` and some target item is a class / set / bundle → the item is
    **expanded** over `rf.inventory` (this section's inventory is the *target's*, V-29) with
    `rewrite.match_item(spec, seg, rf, table)` and one entry is added per combination of the
    cartesian product (product capped at `_EXPAND_CAP = 64`; on overflow the first 64 in inventory
    order are kept and a note is recorded). Expansion of a respell target is an extension of the
    spec's letter, taken because it is the same machinery §3.2 already requires and it only
    over-generates.
  - anything else (`0 -> "x"`, a backref, an IPA-segment or feature-change replacement) is
    **skipped** with the note `respell:<line> skipped: <reason>`.
  - Finally, every segment `s` in `rf.inventory` that is not the whole target of any entry above
    maps to itself: key `s.casefold()`, segments `(s,)`, rule_id `"identity"`.
- **V-2 Greedy parse, longest chunk first (spec §3.1).** `parse_pattern` scans the casefolded
  pattern left to right. At each position it tries chunk keys in order **longest first, then
  ascending by `str`** (so Georgian `ts'` beats `ts` beats `t`). `*` → an `ANY` slot; `?` → a `ONE`
  slot with no alternatives; `[...]` → a `ONE` slot whose alternatives are the union of the
  un-respelled alternatives of each letter in the class (a letter that is not a chunk contributes
  nothing and adds a note); an unclosed `[` is a usage error. A letter matching no chunk becomes a
  `ONE` slot carrying the note `no Irish source for '<letter>'`, which is also promoted to a
  pattern-level note.
- **V-3 The source map (spec §3.2).** `source_map(section, target, irish, table)` returns
  `(map, deletions, notes)` where the map is
  `dict[tuple[str, ...], tuple[Source, ...]]`: **target-side segment sequence → sources**. It is
  built rule by rule in file order from `target.sections[section]`, and for `section ==
  "substitute"` only, `fallback` and `identity` sources are added afterwards (V-8, V-9).
- **V-4 Target expansion.** Each `ItemSpec` in `rule.target` expands to the tuple of segments of the
  **section's own inventory** (V-29; declaration order, marginals included, I-23) for which
  `match_item(spec, seg, target, table)` is true — `target` is passed as the `RuleFile` because the
  rule's class names are the target file's. Multi-item targets take the cartesian product in
  inventory order, capped at `_EXPAND_CAP = 64` combinations per rule with a recorded note.
- **V-29 (F3) The inventory a section expands over is the section's own.**
  `expand_target(rule, match_rf, inventory, table)` takes the inventory explicitly:

  | section | `inventory` | why |
  |---|---|---|
  | `substitute` | `tuple(irish.inventory)` | `[substitute]` reads Irish segments and writes target ones |
  | `repair`, `post-stress`, `respell` | `tuple(target.inventory)` | these run *after* substitution, so their targets are already in the strand's phonology |

  **`target.marginal` is never added** (draft 2 said "+ `target.marginal`", which was wrong twice
  over: `RuleFile.marginal` is a `frozenset`, so concatenating it makes the order non-deterministic,
  and every marginal segment is **already a member of `inventory`** — the `marginal:` line marks
  rows of the inventory, it does not extend it, so the concatenation also duplicated them). The
  return value is exactly `tuple(...)` of the declared inventory, in declaration order, no
  duplicates.

  Draft 1 expanded everything over `irish.inventory`, which silently produced **zero** expansions
  for `arabic-egy [post-stress]` `[V +long] -> [-long]` (Irish `aː` is in the Irish inventory but
  `arabic-egy`'s long vowels are the ones the rule means), for `dutch [repair]`
  `{b d v z ɣ} -> [-voice]`, and for the Welsh repair sets.
- **V-5 Replacement inversion, by shape.** For each expanded source sequence `P`:

  | `rule.replacement` | target key | `Source` |
  |---|---|---|
  | all `str` (segments) | that tuple | `kind="rule"`, `segments=P` |
  | contains `Backref(n)` where `n` is captured on a **target** item | the tuple with `\n` substituted by the expanded segment | `kind="rule"`, `segments=P` |
  | contains `Backref(n)` where `n` is captured in the **context** (`0 -> \1 / … V:1 … _`) | see V-6 | `kind="epenthesis"`, `segments=()` |
  | `Bundle` (feature change) | `(table.apply_changes(p, bundle.constraints),)` for each `p` in `P`; a `FeatureError` skips that segment with a note | `kind="rule"`, `segments=(p,)` |
  | `()` (deletion) | **no map entry** — see V-7 | — |
  | `rule.target == ()` (epenthesis) | the inserted segment tuple (**one key, however many segments**, V-30) | `kind="epenthesis"`, `segments=()` |
  | contains `QuotedText` outside `[respell]` | skipped, note | — |

- **V-6 A context backref (`0 -> \1 / # C* V:1 (C) EPEN_C1 _ {l n r} #`, welsh.rules:298).** The
  inserted segment is a copy of a context segment, so its identity is unknown at inversion time.
  It is registered as **one epenthesis source per segment the capturing context item can match**:
  expand that `CtxItem`'s `ItemSpec` over the section's inventory and, for each result `s`, add
  `(s,) → Source(segments=(), kind="epenthesis", note="copies \\n from the context")`. This is the
  over-generating reading §3 asks for; it is what makes the Welsh epenthetic copy vowel show up as
  an optional group in §3.3.
- **V-7 Deletions, revised (spec §3.2, R3; owner ruling 2026-08-27).** `X -> 0` is **never**
  expanded into candidates. `source_map` returns `deletions: tuple[Deletion, ...]` with
  `Deletion(segments, rule_id, tag, context)`, one per expanded target of a deletion rule. **Every
  section's deletions reach `Pattern.deletions`**: `widen` appends the `[repair]`/`[post-stress]`
  ones, and `un_substitute(pattern, smap, *, deletions, notes)` appends the `[substitute]` ones —
  draft 2 gave `un_substitute` only the map, so the substitute deletions (`welsh.rules:161-164`
  `w -> 0`, `j -> 0`; `dutch.rules:83` `j -> 0 / $ C C _ V`) were computed and then dropped on the
  floor, and the `possibly dropped` block could never mention them. `notes` is plumbed the same
  way, so `_EXPAND_CAP` truncations and skipped rule shapes reach `Pattern.notes`. The
  report prints the deletions **once per word**, as a single block under the constraints —
  not as a note on every slot, which draft 1 did and which is far too noisy (the Welsh substitute
  section alone contributes four):

  ```
  possibly dropped
    h    may have been dropped anywhere in this word     substitute:222,224 %design
  ```

  Lines are grouped and formatted exactly like constraint lines (V-32), keyed by
  `(description, tag, context)`, ordered by first rule id. The block is omitted when there are no
  deletions.
- **V-17 — withdrawn.** Draft 1 attached each deletion as a note on every neighbouring slot. The
  owner's ruling of 2026-08-27 replaces it with the once-per-word `possibly dropped` block of V-7.
  The number is not reused.
- **V-8 Fallback sources.** For `section == "substitute"` only: for each `s` in `irish.inventory`
  such that `s` is **not** the whole target of any *context-free* rule of the section, and
  `s not in target.inventory`, add
  `(table.nearest(s, non_marginal_target_inventory, target.weights),) → Source(segments=(s,),
  rule_id="fallback", tag="fallback", kind="fallback")`. `non_marginal_target_inventory` is
  `tuple(x for x in target.inventory if x not in target.marginal)` — exactly what
  `substitute.fallback` uses, so the two cannot drift.
- **V-9 Identity sources.** For `section == "substitute"` only: for each `s` in `irish.inventory`
  with `s in target.inventory` and no context-free rule of the section targeting it, add
  `(s,) → Source(segments=(s,), rule_id="identity", tag="", kind="identity")`.
- **V-10 "Context-free" means `rule.left == () and rule.right == ()`.** A rule with any context
  **may not have fired**, so its targets still get fallback/identity sources. This is the
  over-generation R2 buys with "the forward engine enforces contexts".
- **V-11 Chains to depth 3 (spec §3.2), order-respecting (F2).** After the direct map is built
  (before fallback/identity), run two closure passes. In each pass, for every `(K, S)` and every
  source `s ∈ S` with `s.kind == "rule"`, if `s.segments` is itself a key of the map with sources
  `S'`, add for each `s' ∈ S'` that satisfies **all** of
  - `s'.kind == "rule"`,
  - `s'.segments != K` and `s'.segments != s.segments` (cycle guard: this is what stops georgian's
    `v v -> v` / `i i -> i` and dutch's degemination block from looping), and
  - **V-28 (F2): `s'.line < s.line`** — the rule that *produces* the intermediate must run
    **before** the rule that consumes it,

  a source `Source(segments=s'.segments, rule_id=f"{s'.rule_id}>{s.rule_id}", line=s.line,
  tag="design" if "design" in (s.tag, s'.tag) else s.tag,
  context=" ; ".join(x for x in (s'.context, s.context) if x), kind="rule")`.
  Dedupe by `(segments, rule_id)`.
- **V-28 (F2) Why the order guard is required.** `arabic-egy.rules` has `ʒ -> ʃ` at
  `substitute:61` and `dʒ -> ʒ` at `substitute:62`. Forward, `/dʒ/` becomes `/ʒ/` at line 62 and
  the `/ʒ/ -> /ʃ/` rule has **already run**, so `/dʒ/` never reaches `/ʃ/`. Draft 1's unordered
  closure composed them anyway and would have offered Irish `/dʒ/` as a source of Cairene `⟨sh⟩`,
  which the forward engine can never produce. `Source` therefore carries `line: int` (the rule's
  own `Rule.line`, 0 for `fallback`/`identity`), and a chain edge is admitted only when the
  producing rule's line is **strictly less** than the consuming rule's.

  **The positive case is Georgian, measured:** `georgian.rules:79` is the context-free `pˠ -> p`
  and `georgian.rules:118` is `p -> pʼ / C _`, so `/pˠ/` is a real forward source of `/pʼ/` and the
  closure must admit `substitute:79>substitute:118`. **The spec's own illustration is not a case in
  the files:** spec §3.2 offers "`ç -> x`, then `x -> χ`", but `welsh.rules` has `x -> χ` at line
  118 and `ç -> χ` **directly** at line 121 — there is no `ç -> x` rule, so nothing composes there
  and `/ç/` reaches `/χ/` in one step. The spec sentence illustrates the *mechanism*, not the file;
  Task 4 tests the mechanism on the Georgian pair and the guard on the Arabic pair, and makes **no**
  assertion about Welsh chains.
- **V-12 Contexts are text (R2).** `Source.context` is `reverse.env_text(rule)`: the left items,
  `_`, then the right items, space-joined, each `CtxItem` rendered as
  `segment` / `CLASS` / `{a b}` / `[CLASS +f -g]` / `@orth("x")` / `#` `$` `.` `ˈ`, wrapped
  `(X)` when `optional` and suffixed `*` when `star`. Both contexts empty → `""`. No context is
  ever evaluated at inversion time.

### Alternatives, provenance and optional groups

- **V-31 (F5) An alternative is a derivation, not a bare segment tuple.**

  ```python
  @dataclass(frozen=True)
  class Step:
      stage: str          # "respell" | "post-stress" | "repair" | "substitute"
      rule_id: str
      tag: str            # "" | "attested" | "design" | "fallback"
      context: str
      kind: str           # "rule" | "fallback" | "identity" | "epenthesis"

  @dataclass(frozen=True)
  class Alternative:
      segments: tuple[str, ...]      # the segments at this stage of the walk
      steps: tuple[Step, ...]        # newest first: the walk back from the printed letter
  ```

  `parse_pattern` creates one `Alternative` per `RespellSource` with a single `respell` step;
  `widen` appends a `repair`/`post-stress` step when it derives a new alternative from an old one;
  `un_substitute` appends the `substitute` step. Provenance therefore **composes**: a Welsh
  `â ← aː ← a ← Irish /a/` alternative carries three steps and can say which rule did each. Draft 1
  dropped the widening rule id entirely, so a widened alternative had no rule to print.

  **How a multi-step alternative collapses to one `ConstraintLine`** (draft 2 left this
  underspecified). `steps` is stored **newest first** (respell, then repair/post-stress, then
  substitute); `FORWARD_STAGES = ("substitute", "repair", "post-stress", "respell")` is the order
  everything is *reported* in — `sorted(steps, key=lambda s: FORWARD_STAGES.index(s.stage))`,
  a stable sort, so two steps of the same stage keep their walk order. Then:

  | field | rule |
  |---|---|
  | `description` | `g2p_inverse.describe(alt.segments)` + the kind phrase of `kind` below (V-15) |
  | `kind` | the **substitute-stage** step's kind — the Irish-side one. When the alternative has no substitute step (pure widening of a target segment that is identity on the Irish side), `kind = "identity"` |
  | `tag` | the **weakest** tag across all steps under `attested < design < fallback`; an empty tag counts as `attested` |
  | `context` | the non-empty step contexts joined `" ; "` in forward stage order |
  | `rule_ids` | every step's `rule_id` in forward stage order, deduped, first occurrence winning |

  One `ConstraintLine` per distinct `(description, kind, tag, context)` — alternatives agreeing on
  all four merge and their `rule_ids` concatenate. The **exclusions** block does *not* use the
  joined context: it prints **one line per context-bearing step**, with that step's own `rule_id`
  and its own `context`, so an alternative with two distinct non-empty contexts yields **one**
  constraint line and **two** exclusion lines.
- **V-30 (F4) Insertions widen slot SPANS, and optional material is a GROUP.** An epenthesis rule in
  `[repair]`/`[post-stress]` may insert **more than one segment** — `arabic-egy.rules:151`
  `0 -> ʔ i / # _ s [C -sonorant]` inserts two. Marking the `ʔ` slot and the `i` slot independently
  optional would admit `ʔ`-without-`i` and `i`-without-`ʔ`, neither of which the forward engine can
  produce. So:

  ```python
  @dataclass(frozen=True)
  class OptionalGroup:
      start: int                  # inclusive slot index
      stop: int                   # exclusive
      steps: tuple[Step, ...]     # the inserting rule
      note: str
  ```

  `Pattern` carries `groups: tuple[OptionalGroup, ...]`, sorted by `(start, stop)` and
  non-overlapping (on an overlap the **earlier, then longer** group wins and the other is dropped
  with a note). `widen` finds them by matching each insertion's output sequence against
  **consecutive slot spans**: for every rule with `kind == "epenthesis"` in either widened section
  and every span `[i, i + len(inserted))` where each slot in the span is a `SEG` slot with the
  corresponding inserted segment among its alternatives, record a group. `Slot.optional` is gone;
  `expand` (V-24) treats a group **atomically** — present or absent as a unit — and the report
  renders it as one `( … )?`. A single-segment insertion is just a group of width 1, so there is
  one code path.

  **Accepted miss (F2 re-check): respell deletions are not re-inserted.** A group is found only
  where every inserted segment has a slot, and a slot exists only where the respelling *prints*
  something. `arabic-egy.rules [respell]` has `ʔ -> "" / # _`, so the `ʔ` of the very rule above is
  invisible in a respelling — `isk` parses as `/i s k/`, three slots, and the pair `ʔ i` can never
  form a group from a real Arabic pattern. Inverting a respell deletion means guessing where a
  printed-nothing segment sat — unbounded, the same problem R3 rules out for phonological
  deletions — so **v1 does not do it**: a group whose first segment the respelling deletes is
  unreachable. That is recorded here, in Known risks, and as an `invert_respell` note
  `respell:<line> deletes <segments>; a group starting there is unreachable`. The atomic-group
  behaviour is therefore tested on a **synthetic** rule file where the inserted pair is fully
  visible (Tasks 5 and 7), not on `arabic-egy`.

### Widening (spec §3.3)

- **V-18 Widening runs before un-substitution.** `parse_pattern` gives slots over **target-IPA**
  sequences. `widen(pattern, target, irish, table)` builds `source_map("repair", …)` and
  `source_map("post-stress", …)` — expanded over `target.inventory` (V-29), and with **no**
  fallback and **no** identity sources (V-8/V-9 are `substitute`-only) — and, for each slot
  alternative `A` that is a key of either map, adds each rule source's `segments` as a **new
  alternative of the same slot** (these are pre-rule *target* segments, not Irish ones), extending
  `A.steps` with the rule's `Step` (V-31). Epenthesis sources become optional groups (V-30).
  Deletions in these two sections join the word-level `possibly dropped` block (V-7). Stress is
  ignored entirely: no `[stress]` handling, and `ˈ ˌ .` are stripped from any IPA comparison.

### Reverse g2p (spec §3.4)

- **V-27 (F1) The reverse g2p is a grapheme READING REGISTRY over every forward emission path, not
  an inversion of two tables.** `g2p.g2p` does not read `_CONSONANTS`/`_VOWELS` alone: `_grapheme`
  branches procedurally before it ever consults `_CONSONANTS`, `_word_segments` applies a Connacht
  post-pass and an unstressed-reduction pass, and `_epenthesis` inserts a schwa no letter spells.
  Draft 1 inverted the two tables only, which left **no grapheme at all** for `/vˠ/` and only
  ⟨rr⟩ for `/ɾˠ/` — so `spell(g2p("ardmhaor"))` (which is `ˈaːɾˠd̪ˠvˠiːɾˠ`) returned nothing, and
  the whole session case of spec §6 bullet 4 was unreachable. Task 1 therefore **reads `g2p.py`'s
  branches and enumerates what each can emit**, into an explicitly over-generating registry:

  ```python
  @dataclass(frozen=True)
  class Reading:
      grapheme: str                  # the letters, e.g. "bh", "ng", "l", "th"
      segments: tuple[str, ...]      # 0, 1 or 2 segments — () is a silent reading
      quality: str                   # "broad" | "slender" | "either"
      position: str                  # "any" | "initial" | "noninitial"
      source: str                    # the g2p branch this row transcribes
  READINGS: tuple[Reading, ...]
  ```

  Every row of the registry names the `g2p` branch it comes from in `source`, and the branches to
  cover — read them in `g2p.py`, do not work from this list alone — are:

  | `g2p` branch | readings to register |
  |---|---|
  | `_CONSONANTS` | each grapheme × (broad, slender), `None` = a silent reading `()` |
  | `_ECLIPSIS_INITIAL` | each digraph × quality, `position="initial"` |
  | `_grapheme` ⟨dh gh⟩ | slender → `("j",)`; broad → `("ɣ",)` `position="initial"`, and `()` `position="noninitial"` |
  | `_grapheme` ⟨sh⟩ | `("h",)` either; `("ç",)` slender |
  | `_grapheme` ⟨th⟩ | `("h",)` either; `()` either (the word-final-after-long-vowel silence) |
  | `_grapheme` ⟨ch⟩ | `("x",)` slender **as well as** broad (the pre-⟨t⟩ branch) |
  | `_grapheme` ⟨ng⟩ | `("ŋ", "ɡ")` broad / `("ɲ", "ɟ")` slender, `position="noninitial"` |
  | `_grapheme` ⟨nc⟩ | `("ŋ", "k")` broad / `("ɲ", "c")` slender |
  | `_grapheme` ⟨dt⟩ | `("t̪ˠ",)` / `("tʲ",)`, `position="noninitial"` |
  | `_grapheme` ⟨x⟩ | `("k", "s")` either |
  | `_liquid` | ⟨l⟩ → `l̪ˠ l̠ʲ lˠ lʲ`, ⟨n⟩ → `n̪ˠ n̠ʲ nˠ nʲ` (both fortis and lenis, both qualities); ⟨ll nn⟩ → the fortis pair; **and ⟨n⟩ → `ɾˠ`/`ɾʲ`** (the cn/gn/mn branch), `position="noninitial"` |
  | `_rhotic` | ⟨r⟩ → `ɾˠ` **either quality**, and `ɾʲ` slender; ⟨rr⟩ → `ɾˠ` either |
  | `_sibilant` | ⟨s⟩ → `sˠ` either quality, and `ʃ` slender |
  | `_word_segments` Connacht post-pass | **every reading whose segments are `("w",)` gains a twin with `("vˠ",)` and `position="noninitial"`** — this is the row that makes `ardmhaor` spellable |

  Vowels are registered the same way, keyed by segment sequence:

  | `g2p` branch | readings to register |
  |---|---|
  | `_VOWELS` default | run → `_split_nucleus(default)` |
  | `_VOWELS` overrides | run → `_split_nucleus(v)` for **every** override value, condition unchecked |
  | `_VOWEL_PLUS_H` | `run + digraph` → `_split_nucleus(stressed)` and `_split_nucleus(unstressed)` |
  | unstressed reduction (`_word_segments` pass 2, `_short`) | every run whose default is a short monophthong also reads as `("ə",)` |
  | `_epenthesis` | the **empty** reading of `("ə",)` — see V-20 step 3 |

  The registry is allowed to be wrong in the permissive direction and **only** in that direction:
  every string `spell` returns is checked with `g2p()` before it is offered (V-20 step 6).
- **V-19 The derived indexes.** From `READINGS`, build at import:
  `CONSONANT_READINGS: dict[tuple[str, ...], tuple[Reading, ...]]` (segments → readings, first-seen
  order), `VOWEL_READINGS: dict[tuple[str, ...], tuple[str, ...]]` (segment sequence → vowel runs),
  and `QUALITY_LEFT` / `QUALITY_RIGHT: dict[str, str]` — for each vowel run, the quality it imposes
  on the consonant **before** it (class of its first letter) and **after** it (class of its last
  letter) per `g2p._SLENDER_LETTERS` / `g2p._BROAD_LETTERS`, with the documented exception
  `BROAD_ON_THE_RIGHT = frozenset({"ae", "aei", "ao", "aoi"})`, which impose **broad** on the right
  despite their last letter (`g2p` module docstring).
- **V-20 `spell()`, the run matcher and caol le caol.** `spell(segments, *, limit=64) -> list[str]`:
  1. Split `segments` into alternating **consonant runs** and **vowel nuclei** (a segment is a
     nucleus member iff it is in `g2p._VOWEL_SEGMENTS`; a maximal run of them is one nucleus).
  2. A consonant run is spelled by `_spell_run(run, quality, at_word_start)`, a **recursive
     matcher**: at each position try every `Reading` whose `segments` are a prefix of the remaining
     run (1 or 2 segments), whose `quality` is `"either"` or the run's quality, and whose `position`
     admits the position; recurse on the rest. Silent readings (`segments == ()`) may be inserted at
     most **once** per run (a bound, so the search terminates). The whole run takes **one** quality;
     enumerate it once per quality that admits a complete match. Results in `READINGS` order.
  3. A nucleus is spelled by `VOWEL_READINGS[tuple(nucleus)]`. **The one exception** is an
     epenthetic schwa: a nucleus that is exactly `("ə",)` and sits between a segment in
     `g2p._EPEN_C1` and a segment in `g2p._EPEN_C2_LIQUID | g2p._EPEN_C2_NASAL` also admits the
     **empty** spelling (`gorm` /ˈɡɔɾˠəmˠ/ is spelled with no letter for the ə). An unknown nucleus
     with no reading makes the word unspellable (return `[]`).
  4. Keep only combinations where each nucleus's `QUALITY_LEFT` equals the quality chosen for the
     consonant run on its left (when there is one) and its `QUALITY_RIGHT` equals the quality of the
     run on its right. A word-initial or word-final run is unconstrained on the missing side; an
     empty-spelled epenthetic schwa imposes nothing on either side and its two neighbouring runs are
     spelled as one run.
  5. Enumerate the surviving combinations in registry order and cap at `limit`.
  6. For each candidate string `c`, run `ipa, _ = g2p.g2p(c)`; keep `c` iff
     `tuple(tokenize(_unmark(ipa), TABLE).segments) == tuple(segments)`, where `_unmark` strips
     `ˈ ˌ .`. Return the kept strings **in enumeration order**. `spell` is the only place a concrete
     spelling is ever proposed, and nothing leaves it unverified (spec §3.4 last sentence).
- **V-21 `describe()`.** `describe(segments) -> str` is the report's description column and is
  **not** g2p-checked (it is a description, not a claim). For one consonant segment: the graphemes
  that read as it, deduped in registry order, joined `/`, prefixed by the quality when every
  reading needs the same one (`broad bh/mh`, `slender d`) and unprefixed otherwise. For one vowel
  nucleus: the runs joined `, `. For a sequence: the per-element descriptions joined ` + `. For `()`
  (epenthesis): `inserted, no Irish letter`. An unknown segment renders as `/<segment>/`.

### Expansion, verification and output

- **V-22 Source rank (spec §3.5).** `rank(alternative)` uses the alternative's **oldest** step (the
  substitute one): `0` identity, `1` rule with `tag != "design"`, `2` rule with `tag == "design"`,
  `3` fallback, `4` epenthesis. An optional group offers "absent" at rank `0` and "present" at the
  group's own rank.
- **V-23 The palette (R5).** *Revised by fix-round ruling A4 (2026-08-27): the five long vowels
  join the palette.* In Irish IPA, matching the spec's letters:
  `PALETTE = ("a", "ɛ", "ɪ", "ɔ", "ʊ", "aː", "eː", "iː", "oː", "uː", "ɾˠ", "l̪ˠ", "n̪ˠ", "mˠ",
  "sˠ", "d̪ˠ", "t̪ˠ", "k", "ɡ", "bˠ")` — the five short vowels first, then their five long
  counterparts, then `r l n m s d t c g b` in the spec's order, each in its broad form. A `ONE`
  slot draws from its own inverted class when it has one, else from `PALETTE`. A `*` slot yields
  0, then 1, then 2 palette segments (`1 + 20 + 400 = 421` fillings, in that order). The long
  vowels are what the session case needs: *ardmhaor* is /aːɾˠd̪ˠvˠiːɾˠ/, so under `ar*v*` the
  trailing `*` has to supply /iː ɾˠ/, which a short-vowel-only palette can never reach.
- **V-24 Enumeration order (spec §3.5 "breadth-first, cheapest first").** Per-slot option lists are
  built rank-ordered; an optional **group** contributes a single option list (`absent`, then each
  present combination) shared by the whole span. The candidate order is by **sum of chosen option
  indices** ascending, ties broken by the index tuple lexicographically. Implemented with `heapq`
  over index tuples, so the cap can be applied without materialising the product. Hard cap
  `CAP = 2000` per word; when the cap is reached the report says so (R4 keeps `--cap` out of v1).
- **V-25 The exact fnmatch.** `_matches(text, pattern)` is
  `fnmatch.fnmatchcase(unicodedata.normalize("NFC", text).casefold(),
  unicodedata.normalize("NFC", pattern).casefold())` — `fnmatchcase`, not `fnmatch`, so the host
  OS's case rules never enter; both sides are casefolded by us. With `--ipa`, `text` is
  `_unmark(result.ipa)` (`ˈ ˌ .` stripped) and the pattern is used as given.
- **V-26 One forward run per (candidate, spelling).** A kept candidate is a real forward run:
  `entry = inputs.infer(Entry(orthography=spelling, ipa=g2p(spelling)[0]), irish, table)`,
  `result = pipeline.run_entry(entry, "DESC", irish, target, table)`. `MissingSlot`,
  `SegmentError`, `RuleError` and `ConstructionNotInStrand` on a candidate are **caught and
  counted**, never propagated: a synthetic candidate is allowed to be unpronounceable.
- **V-34 (F8) `verify` iterates every spelling, and the cap counts unique forward runs.**
  *Superseded by fix-round rulings A1-A3 (2026-08-27): `verify` runs `_forward` ONCE per
  candidate, on one cheap silent-free spelling (`spell(..., limit=1, silent=False, budget=128)`);
  `tried` counts candidates run forward, `cap` bounds that, a candidate with no silent-free
  spelling is skipped without counting, and `expand` is consumed at most `4 * cap` times.
  `Example.spelling_index` survives as 0.* Draft 1
  used `spell(candidate)[0]` only, which throws away most of what §3.4 produces: the spelling that
  actually matches the pattern is frequently not the first (Georgian `Ar*v*` wants `ardmhaor`, and
  ⟨bh⟩ precedes ⟨mh⟩ in the `g2p` table, so `ardbhaor` is proposed first). Revised:
  - for each candidate, iterate **all** strings `spell()` returns, in order, index `j`;
  - maintain `seen: set[tuple[tuple[str, ...], str]]` of `(candidate.segments, spelling)` and skip
    a repeat before any forward work — the same spelling reaches the same `Result`, so re-running it
    is pure waste;
  - `tried` counts **unique forward runs**, and the `cap` is applied to that same counter, so the
    cap means what R4 says it means;
  - `Example` gains `spelling_index: int` and the ranking key becomes
    `(fallbacks, len(flags), rank, spelling_index)`;
  - the printed examples are additionally de-duplicated **by orthography**, first occurrence
    winning, so one spelling never fills the list.
- **V-33 (F7) `--ipa` has its own parser.** `parse_ipa_pattern(pattern, target, table)` — a
  respelling and an IPA string are not the same kind of text, and code-point scanning would split
  `t̪ˠ`, `tʃʰ` and `aː`. It scans the NFC'd pattern for the glob atoms `*`, `?`, `[`…`]` and hands
  every **literal span between them** to `tokenize.tokenize(span, table)`; the resulting segments
  become one `SEG` slot each, with a single identity `Alternative` (there is no un-respell step in
  `--ipa` mode — spec §2: "the un-respell step is skipped"). Inside `[...]`, the members are
  **whole IPA segments** separated by nothing (tokenized the same way), not code points, so
  `[iɪ]` is two members and `[t̪ˠtʲ]` is two members. Rules:
  - a `SegmentError` from `tokenize` is a **usage error** naming the offending substring, exit 2
    (`reverse: 'q' is not a segment in features.tsv`);
  - a segment that tokenizes but is **not** in `target.inventory | target.marginal` is a
    pattern-level note (`no <strand> segment 'x'`), not an error — it simply never verifies;
  - `?` and `[…]` behave as in V-2; `[!…]` is the same usage error as V-16;
  - stress and syllable marks in the pattern are stripped before tokenizing (spec §2: "stress and
    syllable marks ignored").
- **V-32 (F6) One line formatter, and golden tests.** Draft 1 described the layout three different
  ways and gave no test that would catch a disagreement. Revised: **all** rule-bearing lines —
  constraint lines, exclusion lines, the `possibly dropped` block — go through

  ```python
  RULE_COL = 62      # zero-based CODE POINT index at which the rule column begins
  def format_rule_line(prefix: str, description: str, suffix: str) -> list[str]:
      """`prefix + description`, then `suffix` starting at code-point index RULE_COL.
      When `prefix + description` already reaches RULE_COL - 1 or beyond, emit it on its own
      line and put `suffix` on a continuation line indented by RULE_COL spaces. Returns 1 or 2
      lines, each rstrip()ed. Widths are Python code points (len()), not display columns —
      combining marks in the IPA make the two differ, and code points are what a test can
      assert."""
  ```

  and every layout claim is pinned by a **golden test** comparing the *entire* `report()` output
  against a literal expected string. Task 6 writes six goldens: a normal line, a continuation line,
  a wrapped description, the exclusions block, examples-present and verification-skipped, and the
  full `Ar*v*` Georgian block.

---

## File structure

```
docs/plans/2026-08-27-reverse-plan.md      # this file
src/strands/
  g2p.py               # Task 1: public aliases + docstring paragraph (no behaviour change)
  g2p_inverse.py       # Tasks 1, 2 (NEW): READINGS registry, describe(), spell()
  reverse.py           # Tasks 3-7 (NEW): dataclasses, invert_respell, parse_pattern,
                       #   parse_ipa_pattern, source_map, widen, constraints, render_pattern,
                       #   format_rule_line, expand, verify, report, reverse_regression
  regress.py           # Task 2: + write_json_ratchet (a generic writer; run by hand)
  cli.py               # Task 8: cmd_reverse, _USAGE, _HANDLERS, COMMANDS
pyproject.toml         # Task 9: [tool.pytest.ini_options] markers = ["slow: ..."]
tests/
  test_g2p_inverse.py            # Tasks 1, 2
  test_reverse_unrespell.py      # Task 3
  test_reverse_sourcemap.py      # Tasks 4, 5
  test_reverse_report.py         # Task 6
  test_reverse_verify.py         # Task 7
  test_cli_reverse.py            # Task 8
  test_reverse_regression.py     # Task 9
  ratchets/g2p_inverse.json      # Task 2
  ratchets/reverse-welsh.json    # Task 9
  ratchets/reverse-georgian.json # Task 9
  ratchets/reverse-arabic-egy.json  # Task 9
  ratchets/reverse-dutch.json    # Task 9
```

## Task list and dependencies

| # | Task | Depends on | New code (approx.) |
|---|---|---|---|
| 1 | `g2p` public aliases; the `READINGS` registry and `describe()` | — | 220 |
| 2 | `g2p_inverse.spell()`, the run matcher, the `g2p_inverse` ratchet | 1 | 230 |
| 3 | `reverse` data model, `invert_respell`, `parse_pattern`, `parse_ipa_pattern`, `env_text` | — | 280 |
| 4 | `reverse.source_map` for `[substitute]` (all shapes, ordered chains, fallback, identity) | 3 | 270 |
| 5 | `reverse.widen` over `[repair]` / `[post-stress]`, with optional groups | 4 | 150 |
| 6 | Constraint set, `format_rule_line`, `render_pattern`, `report()` + goldens | 1, 5 | 290 |
| 7 | `expand()` and `verify()` | 2, 6 | 220 |
| 8 | `cli.cmd_reverse` (incl. `--ipa`, multi-word, old-irish lookup) | 7 | 170 |
| 9 | Round-trip regression, the four ratchets, the session case | 8 | 200 |

Tasks **1** and **3** are independent and may run at once; everything after is the serial spine
1→2, 3→4→5→6→7→8→9, with 6 also needing 1. `src/strands/reverse.py` is created by Task 3 and
extended by 4, 5, 6, 7 — **no two of those may run concurrently.** `src/strands/g2p_inverse.py` is
created by Task 1 and extended by Task 2 — likewise.

---

## Task 1: `g2p` public aliases; the reading registry and `describe()`

**Depends on:** — . **Spec:** §3.4, §5, R7. **Interpretations:** V-27, V-19, V-21. **Review:** F1.

**Files:** modify `src/strands/g2p.py`; create `src/strands/g2p_inverse.py`; create
`tests/test_g2p_inverse.py`.

**Read `src/strands/g2p.py` end to end before writing anything.** V-27's table is a *checklist of
branches*, not a substitute for reading them: a branch this plan missed still has to be registered,
and a branch that has changed since is authoritative over this plan.

**`g2p.py` change (spec §5: "those become module-level, documented as shared with the inverse (no
behaviour change)").** The tables are already module-level. Add public aliases and extend `__all__`:

```python
__all__ = ["g2p", "G2PError", "CONSONANTS", "VOWELS", "VOWEL_PLUS_H", "ECLIPSIS_INITIAL",
           "SLENDER_LETTERS", "BROAD_LETTERS", "VOWEL_SEGMENTS", "EPEN_C1", "EPEN_C2_LIQUID",
           "EPEN_C2_NASAL", "split_nucleus"]

CONSONANTS = _CONSONANTS            # shared with strands.g2p_inverse (reverse spec §3.4)
ECLIPSIS_INITIAL = _ECLIPSIS_INITIAL
VOWELS = _VOWELS
VOWEL_PLUS_H = _VOWEL_PLUS_H
SLENDER_LETTERS = _SLENDER_LETTERS
BROAD_LETTERS = _BROAD_LETTERS
VOWEL_SEGMENTS = _VOWEL_SEGMENTS
EPEN_C1, EPEN_C2_LIQUID, EPEN_C2_NASAL = _EPEN_C1, _EPEN_C2_LIQUID, _EPEN_C2_NASAL
split_nucleus = _split_nucleus
```

and one docstring paragraph: "These tables and `split_nucleus` are read by
`strands.g2p_inverse`, which enumerates which Irish spellings can read as a given segment. The
inverse also transcribes the *procedural* branches of `_grapheme`, `_liquid`, `_rhotic`,
`_sibilant`, the Connacht /w/ → /vˠ/ post-pass and `_epenthesis` into its own registry — **a change
to any of those must be mirrored there**, and `tests/ratchets/g2p_inverse.json` is what notices if
it is not." **No other edit to `g2p.py`.**

**`g2p_inverse.py` interfaces (this task):**

```python
Quality = str          # "broad" | "slender" | "either"
Position = str         # "any" | "initial" | "noninitial"

@dataclass(frozen=True)
class Reading:
    grapheme: str
    segments: tuple[str, ...]
    quality: Quality
    position: Position
    source: str                        # the g2p branch, e.g. "_liquid fortis", "connacht-w"

READINGS: tuple[Reading, ...]
CONSONANT_READINGS: dict[tuple[str, ...], tuple[Reading, ...]]
VOWEL_READINGS: dict[tuple[str, ...], tuple[str, ...]]
QUALITY_LEFT: dict[str, Quality]
QUALITY_RIGHT: dict[str, Quality]
BROAD_ON_THE_RIGHT: frozenset[str] = frozenset({"ae", "aei", "ao", "aoi"})

def readings_for(segments: Sequence[str]) -> tuple[Reading, ...]
def describe(segments: Sequence[str]) -> str
```

- [ ] **Step 1: Write the failing tests** — `tests/test_g2p_inverse.py`:

```python
"""Tasks 1-2: the reverse g2p (reverse spec §3.4; V-27, V-19, V-20, V-21)."""
import pytest

from strands import g2p as fwd
from strands.g2p_inverse import (BROAD_ON_THE_RIGHT, CONSONANT_READINGS, QUALITY_LEFT,
                                 QUALITY_RIGHT, READINGS, VOWEL_READINGS, describe,
                                 readings_for)


def spellings(segments):
    return tuple(r.grapheme for r in readings_for(segments))


def test_the_forward_tables_are_public_and_are_the_same_objects():
    """spec §5: the tables become module-level and documented as shared."""
    assert fwd.CONSONANTS is fwd._CONSONANTS and fwd.VOWELS is fwd._VOWELS
    assert "CONSONANTS" in fwd.__all__ and "VOWELS" in fwd.__all__


def test_every_reading_names_the_g2p_branch_it_transcribes():
    """V-27: the registry is a transcription of g2p, and must say of what."""
    assert READINGS and all(r.source for r in READINGS)


# ---- the table branches -------------------------------------------------------------------------

@pytest.mark.parametrize("segment,expected", [
    ("w", ("bh", "mh", "v", "w")),
    ("x", ("ch",)), ("ç", ("ch",)),
    ("k", ("c", "k")),
])
def test_the_table_readings_are_registered(segment, expected):
    assert set(expected) <= set(spellings((segment,)))


def test_the_eclipsis_digraphs_are_initial_only():
    got = [r for r in readings_for(("mˠ",)) if r.grapheme == "mb"]
    assert got and all(r.position == "initial" for r in got)


# ---- the PROCEDURAL branches (F1) — draft 1 had none of these ------------------------------------

@pytest.mark.parametrize("segment,grapheme", [
    ("l̪ˠ", "l"), ("l̠ʲ", "l"), ("lˠ", "l"), ("lʲ", "l"),
    ("n̪ˠ", "n"), ("n̠ʲ", "n"), ("nˠ", "n"), ("nʲ", "n"),
])
def test_single_l_and_n_read_as_both_fortis_and_lenis(segment, grapheme):
    """_liquid: draft 1 had only the doubled ⟨ll nn⟩ from _CONSONANTS."""
    assert grapheme in spellings((segment,))


def test_single_r_reads_as_the_broad_rhotic_in_both_qualities():
    """_rhotic: slender ⟨r⟩ is /ɾˠ/ initially, after ⟨s⟩ and before a coronal."""
    assert "r" in spellings(("ɾˠ",)) and "r" in spellings(("ɾʲ",))


def test_single_s_reads_as_both_sibilants():
    """_sibilant: slender ⟨s⟩ is /sˠ/ before f m p r, /ʃ/ otherwise."""
    assert "s" in spellings(("sˠ",)) and "s" in spellings(("ʃ",))


@pytest.mark.parametrize("segment,grapheme", [("j", "dh"), ("j", "gh"), ("ɣ", "dh"),
                                              ("h", "sh"), ("ç", "sh"), ("h", "th")])
def test_the_lenition_digraphs_are_registered(segment, grapheme):
    assert grapheme in spellings((segment,))


def test_the_silent_readings_exist():
    """broad ⟨dh gh⟩ noninitially, ⟨th⟩ word-finally after a long vowel, ⟨fh⟩."""
    silent = {r.grapheme for r in READINGS if r.segments == ()}
    assert {"dh", "gh", "th", "fh"} <= silent


@pytest.mark.parametrize("segments,grapheme", [(("ŋ", "ɡ"), "ng"), (("ɲ", "ɟ"), "ng"),
                                               (("ŋ", "k"), "nc"), (("k", "s"), "x")])
def test_the_two_segment_readings_are_registered_as_units(segments, grapheme):
    assert grapheme in spellings(segments)


def test_noninitial_w_also_reads_as_the_connacht_allophone():
    """V-27, the row that makes `ardmhaor` spellable: _word_segments turns a noninitial
    /w/ into /vˠ/ for dialect C, so ⟨bh mh v w⟩ all read as /vˠ/ off the word edge."""
    got = readings_for(("vˠ",))
    assert {"bh", "mh", "v", "w"} <= {r.grapheme for r in got}
    assert all(r.position == "noninitial" for r in got)


# ---- vowels ---------------------------------------------------------------------------------------

@pytest.mark.parametrize("nucleus,run", [(("aː",), "á"), (("iː",), "ao"), (("iː",), "aoi"),
                                         (("iə",), "ia"), (("əu",), "abh"), (("eː",), "ae")])
def test_the_vowel_runs_that_read_as_a_nucleus(nucleus, run):
    assert run in VOWEL_READINGS[nucleus]


def test_an_override_value_is_inverted_too_without_checking_its_condition():
    """V-27: `a` -> `aː` before ⟨rd⟩ is an override; the inverse over-generates."""
    assert "a" in VOWEL_READINGS[("aː",)]


def test_every_short_vowel_run_also_reads_as_schwa():
    """_word_segments pass 2: an unstressed short monophthong reduces."""
    assert {"a", "e", "i", "o", "u"} <= set(VOWEL_READINGS[("ə",)])


def test_caol_le_caol_is_read_off_the_letters_with_the_ae_ao_exception():
    assert QUALITY_LEFT["ia"] == "slender" and QUALITY_RIGHT["ia"] == "broad"
    assert QUALITY_LEFT["á"] == "broad" and QUALITY_RIGHT["á"] == "broad"
    assert QUALITY_LEFT["ei"] == "slender" and QUALITY_RIGHT["ei"] == "slender"
    for run in BROAD_ON_THE_RIGHT:
        assert QUALITY_RIGHT[run] == "broad", run


# ---- describe -------------------------------------------------------------------------------------

def test_describe_prefixes_the_quality_when_every_reading_agrees():
    assert describe(("vʲ",)).startswith("slender ")
    assert describe(("aː",)).startswith("á")
    assert describe(()) == "inserted, no Irish letter"
    assert describe(("ʡ",)) == "/ʡ/"


def test_describe_is_stable_across_calls():
    assert describe(("w",)) == describe(("w",))


def test_the_indexes_are_deterministic_tuples():
    for value in list(CONSONANT_READINGS.values()) + list(VOWEL_READINGS.values()):
        assert isinstance(value, tuple)
```

- [ ] **Step 2:** `uv run pytest tests/test_g2p_inverse.py -q` → FAIL (`No module named
      'strands.g2p_inverse'`).
- [ ] **Step 3:** add the aliases and the docstring paragraph to `g2p.py`.
- [ ] **Step 4:** write `g2p_inverse.py`: `Reading`, the `READINGS` registry (built by a `_build()`
      that walks the tables **and** hand-writes one entry per procedural branch, each with its
      `source` string), the four derived indexes, `readings_for`, `describe`. Module docstring: what
      the file is, that it transcribes `g2p`'s branches and must be updated with them, that it
      **over-generates by design** (positions and conditions are advisory, `g2p()` is the judge), and
      V-27/V-19/V-21 by number.
- [ ] **Step 5:** the parametrized expectations are **measured, not guessed**: run
      `uv run python -c "from strands.g2p_inverse import readings_for; print(readings_for('w'))"` and
      friends. Where a real order differs, change the test and say why in a comment; where a reading
      is genuinely missing, that is a registry bug.
- [ ] **Step 6:** `uv run pytest -q` → 1680+ passed, 2 skipped, 2 xfailed.
- [ ] **Step 7: Commit**

```bash
git add src/strands/g2p.py src/strands/g2p_inverse.py tests/test_g2p_inverse.py
git commit -m "feat(g2p-inverse): grapheme reading registry over every g2p emission path"
```

**Acceptance:** every `g2p` emission branch — tables, `_liquid`, `_rhotic`, `_sibilant`, the
lenition digraphs, the two-segment readings, the silent readings, the Connacht /w/→/vˠ/ post-pass,
the unstressed reduction — has at least one registered reading, each naming its branch; the ⟨ae⟩/⟨ao⟩
right-broad exception is encoded; `describe` alternates and never picks.

---

## Task 2: `g2p_inverse.spell()`, the run matcher, and the ratchet

**Depends on:** Task 1. **Spec:** §3.4, §6 bullet 2. **Interpretations:** V-20. **Review:** F1.

**Files:** modify `src/strands/g2p_inverse.py`, `src/strands/regress.py`; append to
`tests/test_g2p_inverse.py`; create `tests/ratchets/g2p_inverse.json`.

**Interfaces:**

```python
# g2p_inverse.py
SPELL_LIMIT = 64
def spell(segments: Sequence[str], *, limit: int = SPELL_LIMIT) -> list[str]
def _runs(segments: Sequence[str]) -> list[tuple[str, tuple[str, ...]]]         # ("C"|"V", run)
def _spell_run(run: Sequence[str], quality: str, at_word_start: bool) -> list[str]

# regress.py — a generic ratchet writer beside the existing target-specific one
def write_json_ratchet(name: str, data: dict[str, float | int]) -> None
    """tests/ratchets/<name>.json, floats floored to 4 dp with _floor4 so the file cannot
    record a floor above the rate that produced it (review-targets.md finding). Run BY HAND,
    never by a test — the same convention as write_ratchet()."""
```

`spell` follows V-20 exactly, including the recursive run matcher (2), the epenthetic-schwa empty
reading (3) and the `g2p()` check (6). Note the traps, all measured against `g2p`:

- **`g2p` lower-cases its input** and the test-words orthographies are capitalized, so the ratchet
  compares `orthography.casefold()`.
- **`g2p` returns `(ipa, notes)` and marks stress**; the check tokenizes `_unmark(ipa)` with
  `tokenize(..., TABLE)` and compares segment tuples, never strings. `TABLE` is loaded once at
  module import from `cli.DEFAULT_FEATURES` — import the constant, do not write a second path.
- **`g2p` raises `G2PError` on a spelling with no vowel letter.** Catch it in step 6 and drop that
  candidate; a consonant-only candidate is legal to *propose* and illegal to *keep*.

- [ ] **Step 1: Write the failing tests** — append to `tests/test_g2p_inverse.py`:

```python
import json
import unicodedata

from helpers import ROOT, TABLE, read_test_words
from strands.g2p import g2p
from strands.g2p_inverse import spell
from strands.tokenize import tokenize

RATCHET = ROOT / "tests" / "ratchets" / "g2p_inverse.json"


def segs(ipa):
    for mark in ("ˈ", "ˌ", "."):
        ipa = ipa.replace(mark, "")
    return tuple(tokenize(ipa, TABLE).segments)


@pytest.mark.parametrize("orth", ["mac", "bán", "ceist", "cáis", "fíon", "dorn", "teach",
                                  "sean", "bean", "Colm", "gorm", "ardmhaor"])
def test_spelling_a_words_own_ipa_recovers_the_word(orth):
    """F1: `dorn` needs single ⟨r n⟩, `sean` single ⟨s⟩, `gorm` the epenthetic schwa with no
    letter, `ardmhaor` the noninitial /w/ -> /vˠ/ post-pass. Draft 1 recovered none of them."""
    assert orth.casefold() in [c.casefold() for c in spell(segs(g2p(orth)[0]))]


def test_the_session_case_word_is_spellable():
    """spec §6 bullet 4: `ardmhaor` is the example the whole Ar*v* case turns on."""
    assert "ardmhaor" in spell(segs(g2p("ardmhaor")[0]), limit=200)


def test_every_proposal_reads_back_to_the_intended_ipa():
    """spec §3.4 last sentence: nothing leaves `spell` unverified."""
    want = segs(g2p("bán")[0])
    for cand in spell(want):
        assert segs(g2p(cand)[0]) == want


def test_caol_le_caol_rules_out_the_mismatched_vowel_letters():
    out = spell(segs(g2p("Seán")[0]))
    assert out and all(not c.startswith("sa") for c in out)


def test_a_two_segment_reading_is_matched_as_a_unit():
    """⟨ng⟩ is /ŋɡ/: the run matcher must consume both segments at once."""
    assert "long" in [c.casefold() for c in spell(segs(g2p("long")[0]))]


def test_an_unknown_nucleus_is_unspellable_not_a_crash():
    assert spell(("ʡ",)) == []


def test_a_consonant_only_candidate_does_not_raise():
    assert spell(("k",)) == []          # g2p raises G2PError; spell drops it


def test_the_result_is_capped_and_order_is_stable():
    a = spell(segs(g2p("mac")[0]), limit=3)
    assert len(a) <= 3 and a == spell(segs(g2p("mac")[0]), limit=3)


# ---- the ratchet (spec §6 bullet 2) ----------------------------------------------------------

def hand_ipa_rows():
    return [r for r in read_test_words() if (r.get("ipa") or "").strip()]


def contains_rate():
    rows, hit, misses = hand_ipa_rows(), 0, []
    for row in rows:
        want = unicodedata.normalize("NFC", row["orthography"]).casefold()
        try:
            got = [unicodedata.normalize("NFC", c).casefold() for c in spell(segs(row["ipa"]))]
        except Exception:
            got = []
        if want in got:
            hit += 1
        else:
            misses.append((row["orthography"], row["ipa"]))
    return hit / len(rows), misses


def test_the_contains_rate_does_not_fall():
    rate, misses = contains_rate()
    ratchet = json.loads(RATCHET.read_text(encoding="utf-8"))
    assert rate >= ratchet["contains"] - 1e-9, (
        f"contains {rate:.4f} < ratchet {ratchet['contains']}\n"
        + "\n".join(f"  {o}\t{i}" for o, i in misses[:20]))


def test_the_ratchet_records_its_denominator():
    data = json.loads(RATCHET.read_text(encoding="utf-8"))
    assert set(data) == {"contains", "n"} and data["n"] == len(hand_ipa_rows())
```

- [ ] **Step 2:** run → FAIL (`cannot import name 'spell'`).
- [ ] **Step 3:** write `spell`, `_runs`, `_spell_run`; add `write_json_ratchet` to `regress.py`
      (and to its `__all__`).
- [ ] **Step 4:** the twelve `test_spelling_a_words_own_ipa_recovers_the_word` cases are the
      acceptance bar for F1. If one fails, find the missing **branch** in `g2p.py` and register it in
      Task 1's table — do not special-case it in `spell`, and do not delete the case.
- [ ] **Step 5:** write the ratchet **by hand, once**, after `spell` is working:

```bash
uv run python - <<'PY'
import unicodedata, sys
sys.path.insert(0, "tests")
from helpers import TABLE, read_test_words
from strands.g2p_inverse import spell
from strands.regress import write_json_ratchet
from strands.tokenize import tokenize
def segs(ipa):
    for m in ("ˈ", "ˌ", "."):
        ipa = ipa.replace(m, "")
    return tuple(tokenize(ipa, TABLE).segments)
rows = [r for r in read_test_words() if (r.get("ipa") or "").strip()]
hit = 0
for r in rows:
    want = unicodedata.normalize("NFC", r["orthography"]).casefold()
    try:
        got = [unicodedata.normalize("NFC", c).casefold() for c in spell(segs(r["ipa"]))]
    except Exception:
        got = []
    hit += want in got
write_json_ratchet("g2p_inverse", {"contains": hit / len(rows), "n": len(rows)})
print(hit, "/", len(rows))
PY
```

      **There is no floor requirement** (spec §6: "the ratchet only forbids regression"). Record the
      rate reached and put the number in the commit message.
- [ ] **Step 6:** `uv run pytest -q` → 1680+ passed.
- [ ] **Step 7: Commit** — `feat(g2p-inverse): spell() with the run matcher, caol-le-caol and g2p verification (contains N/145)`

**Acceptance:** the twelve fixture words all round-trip; two-segment readings are matched as units;
the epenthetic schwa can be spelled with nothing; every string `spell` returns reads back to the
segments it was asked for; the ratchet exists and records `n`.

---

## Task 3: `reverse` data model, `invert_respell`, `parse_pattern`, `parse_ipa_pattern`

**Depends on:** — . **Spec:** §3.1, §5, §2 (`--ipa`). **Interpretations:** V-1, V-2, V-12, V-16,
V-30, V-31, V-33. **Review:** F4, F5, F7.

**Files:** create `src/strands/reverse.py`; create `tests/test_reverse_unrespell.py`.

**Interfaces:**

```python
ANY, ONE, SEG = "any", "one", "seg"

@dataclass(frozen=True)
class Step:                       # V-31
    stage: str
    rule_id: str
    tag: str
    context: str
    kind: str

@dataclass(frozen=True)
class Alternative:                # V-31
    segments: tuple[str, ...]
    steps: tuple[Step, ...] = ()
    @property
    def kind(self) -> str: ...    # the OLDEST step's kind; "identity" when there are none

@dataclass(frozen=True)
class RespellSource:
    segments: tuple[str, ...]
    rule_id: str
    tag: str
    context: str
    line: int

@dataclass(frozen=True)
class Source:
    segments: tuple[str, ...]
    rule_id: str
    tag: str
    context: str
    kind: str
    line: int = 0                 # V-28: the rule's own line, for the chain order guard
    note: str = ""

@dataclass(frozen=True)
class Deletion:
    segments: tuple[str, ...]
    rule_id: str
    tag: str
    context: str

@dataclass(frozen=True)
class OptionalGroup:              # V-30
    start: int
    stop: int
    steps: tuple[Step, ...]
    note: str

@dataclass(frozen=True)
class Slot:
    kind: str                                    # ANY | ONE | SEG
    text: str                                    # the pattern text: "a", "?", "*", "[aeiou]"
    alts: tuple[Alternative, ...] = ()
    notes: tuple[str, ...] = ()

@dataclass(frozen=True)
class Pattern:
    text: str                                    # the (casefolded, NFC) word pattern
    slots: tuple[Slot, ...]
    groups: tuple[OptionalGroup, ...] = ()
    deletions: tuple[Deletion, ...] = ()
    notes: tuple[str, ...] = ()

class ReverseError(Exception):
    """A pattern that cannot be parsed: an unclosed `[`, `[!…]` (V-16), or — in --ipa mode —
    a substring that is not a segment of features.tsv (V-33)."""

def env_text(rule: Rule) -> str
def invert_respell(rf: RuleFile, table: FeatureTable) -> tuple[dict[str, tuple[RespellSource, ...]],
                                                              tuple[str, ...]]
def parse_pattern(pattern: str, chunks: dict[str, tuple[RespellSource, ...]],
                  *, notes: tuple[str, ...] = ()) -> Pattern
# V-35: `notes` is the second value of `invert_respell`; they are copied into `Pattern.notes`
# BEFORE the parser's own notes, so a respell-deletion note (the Arabic `ʔ -> "" / # _` miss)
# reaches the report and the CLI. Every caller passes `notes=`; a helper that drops them is a bug.
# Each test module that parses real rule files defines
#     def _parse(rf, text): chunks, notes = invert_respell(rf, TABLE); return parse_pattern(text, chunks, notes=notes)
# and `cmd_reverse` does the same inline (cli.py already uses the name `_parse` for its argument parser). Task 3 test: `test_respell_notes_reach_pattern_notes` — a synthetic
# `[respell]` with `x -> "" / # _` parsed via `_parse` yields a `Pattern.notes` entry containing `respell:` and `unreachable`.
def parse_ipa_pattern(pattern: str, target: RuleFile, table: FeatureTable) -> Pattern
```

`invert_respell` per V-1; `parse_pattern` per V-2; `parse_ipa_pattern` per V-33. All pure. Chunk keys
are sorted once by `_chunk_order(chunks) = sorted(chunks, key=lambda c: (-len(c), c))`.

- [ ] **Step 1: Write the failing tests** — `tests/test_reverse_unrespell.py`:

```python
"""Task 3: un-respell, the glob parser and the IPA parser (reverse spec §3.1, §2;
V-1, V-2, V-12, V-16, V-31, V-33)."""
import pytest

from helpers import TABLE, target
from strands.dsl import parse_rules
from strands.reverse import (ANY, ONE, SEG, ReverseError, env_text, invert_respell,
                             parse_ipa_pattern, parse_pattern)

GEO = target("georgian")
WEL = target("welsh")
ARA = target("arabic-egy")

SYNTH = """
[meta]
name = Synth
[inventory]
a i k s t
[classes]
STOP = k t
[respell]
k -> "kh"
[STOP] -> "q"
a i -> "ai"
0 -> "e" / # _ s
i -> "y" / V _ #
"""


def chunks(rf):
    return invert_respell(rf, TABLE)[0]


def alts(slot):
    return {a.segments for a in slot.alts}


def test_a_quoted_replacement_becomes_a_chunk_keyed_by_its_text():
    got = chunks(parse_rules(SYNTH, TABLE, path="synth"))
    assert ("k",) in [s.segments for s in got["kh"]]


def test_a_class_target_is_expanded_over_the_files_own_inventory():
    """V-1 / V-29: [respell] reads the TARGET's segments."""
    got = {s.segments for s in chunks(parse_rules(SYNTH, TABLE, path="synth"))["q"]}
    assert got == {("k",), ("t",)}


def test_a_multi_segment_target_keeps_its_sequence():
    got = chunks(parse_rules(SYNTH, TABLE, path="synth"))
    assert ("a", "i") in [s.segments for s in got["ai"]]


def test_an_epenthesis_respell_rule_is_skipped_with_a_note():
    _got, notes = invert_respell(parse_rules(SYNTH, TABLE, path="synth"), TABLE)
    assert any("skipped" in n and "respell:" in n for n in notes)


def test_a_context_is_carried_as_text_never_evaluated():
    got = chunks(parse_rules(SYNTH, TABLE, path="synth"))
    assert [s.context for s in got["y"]] == ["V _ #"]


def test_a_respell_source_records_its_line_for_the_chain_guard():
    """V-28."""
    got = chunks(parse_rules(SYNTH, TABLE, path="synth"))
    assert all(s.line > 0 for s in got["kh"])


def test_segments_no_rule_mentions_map_to_themselves():
    got = chunks(parse_rules(SYNTH, TABLE, path="synth"))
    assert [s.segments for s in got["s"]] == [("s",)]


# ---- the real files --------------------------------------------------------------------------

def test_georgian_ambiguity_is_kept_as_alternatives():
    got = chunks(GEO)
    assert ("i",) in [s.segments for s in got["y"]]
    assert ("i",) in [s.segments for s in got["i"]]


def test_welsh_i_has_three_sources():
    got = chunks(WEL)
    assert {("ɪ",), ("iː",), ("j",)} <= {s.segments for s in got["i"]}


def test_longest_chunk_first_beats_the_prefix():
    pat = parse_pattern("ts'a", chunks(GEO))
    assert [s.text for s in pat.slots] == ["ts'", "a"]


def test_the_glob_atoms_become_any_and_one_slots():
    pat = parse_pattern("a*r?", chunks(GEO))
    assert [s.kind for s in pat.slots] == [SEG, ANY, SEG, ONE]


def test_every_alternative_carries_its_respell_step():
    """V-31: provenance starts at the printed letter."""
    (slot,) = parse_pattern("a", chunks(GEO)).slots
    assert all(a.steps and a.steps[0].stage == "respell" for a in slot.alts)


def test_a_bracket_class_is_one_slot_carrying_the_unrespelled_letters():
    pat = parse_pattern("[ao]", chunks(GEO))
    (slot,) = pat.slots
    assert slot.kind == ONE and {("ɑ",), ("ɔ",)} <= alts(slot)


def test_an_unknown_letter_is_reported_and_treated_as_one():
    pat = parse_pattern("aqa", chunks(GEO))
    assert pat.slots[1].kind == ONE and pat.slots[1].alts == ()
    assert "no Irish source for 'q'" in pat.notes


def test_the_pattern_is_casefolded_and_nfc():
    assert parse_pattern("AR", chunks(GEO)).text == "ar"


@pytest.mark.parametrize("bad", ["[aeiou", "[!ao]", "[^ao]"])
def test_a_malformed_class_is_an_error_not_a_guess(bad):
    """V-16 (Q4): `[!…]` would make the parser and the verification fnmatch disagree."""
    with pytest.raises(ReverseError):
        parse_pattern(bad, chunks(GEO))


def test_env_text_renders_the_context_shapes():
    epen = next(r for r in GEO.sections["substitute"]
                if not r.target and r.replacement == ("v",))
    assert env_text(epen) == "[BROAD -labial] _ [V +front]"
    plain = next(r for r in GEO.sections["substitute"] if not r.left and not r.right)
    assert env_text(plain) == ""


# ---- --ipa mode (V-33 / F7) --------------------------------------------------------------------

def test_ipa_literals_are_tokenized_not_scanned_by_code_point():
    """A code-point scan would split `aː` and `tʃʰ`."""
    pat = parse_ipa_pattern("ɑrtʃʰ", GEO, TABLE)
    assert [s.text for s in pat.slots] == ["ɑ", "r", "tʃʰ"]


def test_a_long_vowel_is_one_slot():
    pat = parse_ipa_pattern("aː", WEL, TABLE)
    assert len(pat.slots) == 1 and pat.slots[0].alts[0].segments == ("aː",)


def test_glob_atoms_survive_between_literal_spans():
    pat = parse_ipa_pattern("ɑ*r?", GEO, TABLE)
    assert [s.kind for s in pat.slots] == [SEG, ANY, SEG, ONE]


def test_an_ipa_class_contains_whole_segments():
    pat = parse_ipa_pattern("[ɑɔ]", GEO, TABLE)
    (slot,) = pat.slots
    assert slot.kind == ONE and {a.segments for a in slot.alts} == {("ɑ",), ("ɔ",)}


def test_stress_and_syllable_marks_are_ignored():
    """spec §2."""
    assert len(parse_ipa_pattern("ˈɑ.r", GEO, TABLE).slots) == 2


def test_an_unknown_ipa_substring_is_an_error_naming_it():
    with pytest.raises(ReverseError) as exc:
        parse_ipa_pattern("ɑQ", GEO, TABLE)
    assert "Q" in str(exc.value)


def test_a_segment_outside_the_strand_is_a_note_not_an_error():
    pat = parse_ipa_pattern("θ", GEO, TABLE)          # θ tokenizes; Georgian has no /θ/
    assert any("georgian" in n.lower() or "θ" in n for n in pat.notes)


def test_ipa_mode_has_no_respell_step():
    """spec §2: 'the un-respell step is skipped'."""
    pat = parse_ipa_pattern("ɑr", GEO, TABLE)
    assert all(a.steps == () for s in pat.slots for a in s.alts)
```

- [ ] **Step 2:** run → FAIL (`No module named 'strands.reverse'`).
- [ ] **Step 3:** write `reverse.py` with the dataclasses, `env_text`, `invert_respell`,
      `parse_pattern`, `parse_ipa_pattern`, `_chunk_order`. Module docstring: the four-step method
      of spec §3, the over-generation discipline ("at every step the candidate set only grows; the
      forward engine is the oracle"), and V-1/V-2/V-12/V-16/V-31/V-33 by number.
- [ ] **Step 4:** `uv run pytest -q` → 1680+ passed.
- [ ] **Step 5: Commit** — `feat(reverse): un-respell, the glob parser and the IPA pattern parser`

**Acceptance:** literal, class and multi-segment respell targets all invert and record their line;
epenthesis and non-quoted respell rules are skipped **with a note**; contexts are text; every
alternative carries a `Step`; the glob parser is greedy longest-first, casefolds, reports unknown
letters and rejects `[!…]`; `--ipa` tokenizes literal spans and classes with the real tokenizer.

---

## Task 4: `reverse.source_map` for `[substitute]`

**Depends on:** Task 3. **Spec:** §3.2, R2, R3. **Interpretations:** V-3 … V-12, V-28, V-29, V-31.
**Review:** F2, F3, F5.

**Files:** modify `src/strands/reverse.py`; create `tests/test_reverse_sourcemap.py`.

**Interfaces:**

```python
_EXPAND_CAP = 64
SourceMap = dict[tuple[str, ...], tuple[Source, ...]]

def expand_target(rule: Rule, match_rf: RuleFile, inventory: Sequence[str],
                  table: FeatureTable) -> tuple[tuple[tuple[str, ...], dict[int, str]], ...]
    """Each (segment sequence, captures) the rule's TARGET can match over `inventory`, in
    inventory order, capped at _EXPAND_CAP (V-4). `match_rf` supplies the class names
    (always the TARGET rule file); `inventory` is chosen by the caller per V-29."""

def section_inventory(section: str, target: RuleFile, irish: RuleFile) -> tuple[str, ...]
    """V-29: irish.inventory for `substitute`; target.inventory + target.marginal for
    `repair` and `post-stress` (and for `respell`, which invert_respell calls directly)."""

def source_map(section: str, target: RuleFile, irish: RuleFile, table: FeatureTable,
               *, depth: int = 3) -> tuple[SourceMap, tuple[Deletion, ...], tuple[str, ...]]

def un_substitute(pattern: Pattern, smap: SourceMap, *,
                  deletions: Sequence[Deletion] = (), notes: Sequence[str] = ()) -> Pattern
    """Fill each SEG/ONE slot's alternatives: for each existing Alternative whose segments are
    a key of `smap`, emit one new Alternative per Source, with the Source's Step APPENDED to
    the existing steps (V-31). An alternative with no entry keeps an empty source list — it
    simply never verifies. `deletions` and `notes` are the other two members of the
    `source_map(...)` triple and are APPENDED to `pattern.deletions` / `pattern.notes`
    (V-7): callers pass all three, and the CLI never drops any of them."""
```

Replacement inversion follows V-5; the backref cases V-5 row 2 / V-6; deletions V-7; fallback V-8;
identity V-9; "context-free" V-10; chains V-11 **with the V-28 order guard**; the inventory V-29.

**The eight rule shapes, with a real line each — the tests are written against these:**

| shape | example | inversion |
|---|---|---|
| segment → segment | `iː -> i` (georgian) | `("i",) ← Source(("iː",), …, "rule")` |
| class/bundle target | `p -> pʼ / C _` (georgian) | target expanded over the section inventory; one source per expansion |
| feature-change replacement | `[V +long] -> [-long] / _ C C` (arabic-egy post-stress:172) | `apply_changes` per expanded segment; **expanded over `target.inventory`** (V-29) |
| epenthesis | `0 -> v / [BROAD -labial] _ [V +front]` (georgian) | `("v",) ← Source((), …, kind="epenthesis")`, context carried |
| multi-segment epenthesis | `0 -> ʔ i / # _ s [C -sonorant]` (arabic-egy repair:151) | one key `("ʔ","i")`, one source — never two independent keys (V-30) |
| deletion | `w -> 0 / {ʊ uː} _` (welsh) | no map entry; a `Deletion` (V-7) |
| target backref | `{a ɛ ə ɪ}:1 w -> \1 u` (welsh:165) | `("a","u") ← Source(("a","w"), …)`, and three more |
| context backref | `0 -> \1 / # C* V:1 (C) EPEN_C1 _ {l n r} #` (welsh:298) | one epenthesis source per segment `V:1` can match (V-6) |

**The synthetic fixture (spec §6 bullet 1).** §6 asks for "a five-line synthetic
`[respell]`/`[substitute]` string [covering] literal, class, bundle, epenthesis, deletion, fallback,
chain". Task 3 supplied the `[respell]` half; this task supplies `SYNTH_SUB`, parsed against a
synthetic Irish file so the expansion is over a small inventory and the expectations are exhaustive.
**`SYNTH_SUB` declares its own `SLEN` class** — draft 1 wrote `[SLEN]` in the target file while only
the synthetic *Irish* file declared it, which `match_item` would reject as an undeclared class.

- [ ] **Step 1: Write the failing tests** — `tests/test_reverse_sourcemap.py`:

```python
"""Task 4: inverting [substitute] (reverse spec §3.2, §6 bullet 1; V-3 … V-12, V-28, V-29)."""
import pytest

from helpers import TABLE, irish, target
from strands.dsl import parse_rules
from strands.reverse import section_inventory, source_map

IRISH = irish()
GEO = target("georgian")
WEL = target("welsh")
ARA = target("arabic-egy")
DUT = target("dutch")

SYNTH_IRISH = parse_rules("""
[meta]
name = SynthIrish
[inventory]
pˠ pʲ k h a i
""", TABLE, path="synth-irish")

SYNTH_SUB = parse_rules("""
[meta]
name = SynthTarget
[inventory]
p t a i
[classes]
SLEN = pʲ
[substitute]
k -> t                       # literal
[SLEN] -> p                  # class target (declared HERE, F3)
[C +labial] -> p             # bundle target
0 -> i / p _ a               # epenthesis
h -> 0                       # deletion
t -> p                       # chain: k -> t -> p, and k precedes t in file order
""", TABLE, path="synth-target")


def smap(rf, section="substitute", irish_rf=None):
    return source_map(section, rf, irish_rf or IRISH, TABLE)


def sources_for(rf, key, section="substitute", irish_rf=None):
    return smap(rf, section, irish_rf)[0].get(key, ())


def srcs(rf, key, irish_rf=None):
    return {(s.segments, s.kind) for s in sources_for(rf, key, irish_rf=irish_rf)}


# ---- the synthetic file: every shape spec §6 names ---------------------------------------------

def test_the_synthetic_file_covers_every_shape():
    m, deletions, _notes = smap(SYNTH_SUB, irish_rf=SYNTH_IRISH)
    got = {s.kind for ss in m.values() for s in ss}
    assert {"rule", "epenthesis", "fallback", "identity"} <= got
    assert any(d.segments == ("h",) for d in deletions)
    pairs = {(s.segments, s.kind) for s in m[("t",)]}
    assert (("k",), "rule") in pairs                                  # literal
    ppairs = {(s.segments, s.kind) for s in m[("p",)]}
    assert (("pʲ",), "rule") in ppairs                                # class
    assert (("pˠ",), "rule") in ppairs                                # bundle
    assert any(">" in s.rule_id and s.segments == ("k",) for s in m[("p",)])   # chain


def test_the_synthetic_fallback_uses_the_targets_own_nearest():
    m, _d, _n = smap(SYNTH_SUB, irish_rf=SYNTH_IRISH)
    fb = {s.segments[0] for ss in m.values() for s in ss if s.kind == "fallback"}
    assert "h" in fb and all(f not in SYNTH_SUB.inventory for f in fb)


# ---- V-29 (F3): the inventory a section expands over --------------------------------------------

def test_substitute_expands_over_irish_and_the_later_sections_over_the_target():
    assert section_inventory("substitute", ARA, IRISH) == tuple(IRISH.inventory)
    assert section_inventory("post-stress", ARA, IRISH) == tuple(ARA.inventory)


@pytest.mark.parametrize("section", ["substitute", "repair", "post-stress", "respell"])
def test_a_section_inventory_has_no_duplicates_and_keeps_declaration_order(section):
    """V-29 / F5: draft 2 appended target.marginal, which is a frozenset (non-deterministic
    order) AND a subset of inventory (duplicates)."""
    inv = section_inventory(section, GEO, IRISH)
    assert len(inv) == len(set(inv))
    src = IRISH.inventory if section == "substitute" else GEO.inventory
    assert inv == tuple(src)


def test_the_arabic_length_rules_invert_over_cairene_vowels_not_irish_ones():
    """F3: draft 1 expanded [V +long] over irish.inventory and produced nothing usable."""
    m, _d, _n = smap(ARA, "post-stress")
    got = {s.segments for ss in m.values() for s in ss}
    assert any(seg in ARA.inventory for segs in got for seg in segs)
    assert ("aː",) in {s.segments for s in m.get(("a",), ())}


def test_the_dutch_devoicing_rules_invert_over_dutch_segments():
    m, _d, _n = smap(DUT, "repair")
    assert ("b",) in {s.segments for s in m.get(("p",), ())}


# ---- the real substitute sections ----------------------------------------------------------------

def test_a_literal_segment_rule_inverts_literally():
    assert (("iː",), "rule") in srcs(GEO, ("i",))


def test_a_class_target_is_expanded_over_the_irish_inventory():
    ejective = {s.segments for s in sources_for(GEO, ("pʼ",))}
    assert ("pˠ",) in ejective and ("pʲ",) in ejective


def test_an_epenthesis_rule_has_no_irish_segments_and_carries_its_context():
    epen = [s for s in sources_for(GEO, ("v",)) if s.kind == "epenthesis"]
    assert epen and all(s.segments == () for s in epen)
    assert any(s.context == "[BROAD -labial] _ [V +front]" for s in epen)


def test_a_multi_segment_insertion_is_one_key():
    """V-30 / F4: arabic-egy `0 -> ʔ i` must be ONE key, not two. (Whether a real Arabic
    pattern can ever see it is a separate question — `[respell]` deletes an initial /ʔ/, so it
    cannot; see V-30's accepted miss and Task 5's synthetic fixture.)"""
    m, _d, _n = smap(ARA, "repair")
    assert ("ʔ", "i") in m
    assert all(s.kind == "epenthesis" for s in m[("ʔ", "i")])


def test_invert_respell_notes_a_deleting_respell_rule():
    """V-30 accepted miss: `ʔ -> "" / # _` makes a group starting at /ʔ/ unreachable."""
    from strands.reverse import invert_respell
    _chunks, notes = invert_respell(ARA, TABLE)
    assert any("unreachable" in n for n in notes)


def test_a_deletion_is_recorded_and_never_expanded():
    m, deletions, _n = smap(WEL)
    assert any(d.segments == ("w",) for d in deletions)
    assert all(s.kind != "deletion" for ss in m.values() for s in ss)


def test_a_target_backref_is_resolved_by_the_expansion():
    assert (("a", "w"), "rule") in srcs(WEL, ("a", "u"))
    assert (("ɪ", "w"), "rule") in srcs(WEL, ("ɪ", "u"))


def test_a_context_backref_becomes_one_epenthesis_source_per_copyable_segment():
    got = [s for s in sources_for(WEL, ("a",)) if s.kind == "epenthesis"]
    assert got and all(s.segments == () for s in got)
    assert any("copies" in s.note for s in got)


def test_a_multi_segment_rule_inverts_as_a_sequence():
    assert (("i", "ə"), "rule") in srcs(ARA, ("eː",))


# ---- fallback, identity, ORDERED chains (F2) -----------------------------------------------------

def test_the_fallback_maps_every_off_inventory_survivor():
    got = {s.segments[0] for ss in smap(GEO)[0].values() for s in ss if s.kind == "fallback"}
    assert got and all(g not in GEO.inventory for g in got)


def test_identity_covers_the_segments_no_rule_touches():
    got = {s.segments for ss in smap(GEO)[0].values() for s in ss if s.kind == "identity"}
    assert all(len(g) == 1 and g[0] in GEO.inventory for g in got)


def test_a_forward_reachable_chain_is_followed():
    """V-28, MEASURED: georgian:79 `pˠ -> p` (context-free) precedes georgian:118
    `p -> pʼ / C _`, so /pˠ/ really is a forward source of /pʼ/."""
    got = {s.segments for s in sources_for(GEO, ("pʼ",))}
    assert ("p",) in got and ("pˠ",) in got


def test_the_spec_s_welsh_illustration_is_not_a_chain_in_the_file():
    """V-28: welsh has `x -> χ` (118) and `ç -> χ` DIRECTLY (121) — no `ç -> x` rule, so /ç/
    reaches /χ/ in one step and nothing is composed. Asserted so a future reader does not
    re-derive the spec's illustration as a requirement."""
    got = {s.segments: s.rule_id for s in sources_for(WEL, ("χ",))}
    assert ("ç",) in got and ">" not in got[("ç",)]


def test_a_backwards_chain_is_NOT_followed():
    """F2 / V-28: arabic-egy has `ʒ -> ʃ` BEFORE `dʒ -> ʒ`, so forward /dʒ/ ends at /ʒ/ and
    never reaches /ʃ/. Draft 1 composed them anyway."""
    assert ("dʒ",) not in {s.segments for s in sources_for(ARA, ("ʃ",))}
    assert ("dʒ",) in {s.segments for s in sources_for(ARA, ("ʒ",))}


def test_a_chain_rule_id_names_both_steps_and_takes_the_weaker_tag():
    chained = [s for s in sources_for(GEO, ("pʼ",)) if ">" in s.rule_id]
    assert chained and all(">" in s.rule_id for s in chained)
    assert all(s.tag in ("design", "attested") for s in chained)


def test_the_degemination_rules_do_not_make_the_closure_loop():
    assert len(sources_for(GEO, ("v",))) < 200


def test_a_context_bearing_rule_still_leaves_its_target_a_fallback_or_identity_source():
    """V-10 / R2."""
    assert "rule" in {s.kind for s in sources_for(GEO, ("pʰ",))}


def test_un_substitute_appends_a_step_to_each_alternative():
    """V-31: provenance composes."""
    from strands.reverse import invert_respell, parse_pattern, un_substitute
    p = _parse(GEO, "a")
    m, deletions, notes = smap(GEO)
    out = un_substitute(p, m, deletions=deletions, notes=notes)
    assert any(len(a.steps) >= 2 and a.steps[-1].stage == "substitute"
               for a in out.slots[0].alts)


def test_un_substitute_carries_the_substitute_deletions_into_the_pattern():
    """F3: draft 2 computed them and dropped them, so `possibly dropped` could never show a
    [substitute] deletion. welsh.rules:161-164 are the real ones (`w -> 0`, `j -> 0`)."""
    from strands.reverse import invert_respell, parse_pattern, un_substitute
    p = _parse(WEL, "u")
    m, deletions, notes = smap(WEL)
    out = un_substitute(p, m, deletions=deletions, notes=notes)
    ids = {d.rule_id for d in out.deletions}
    assert any(i.startswith("substitute:") for i in ids), ids


def test_the_map_is_deterministic():
    assert smap(GEO)[0] == smap(GEO)[0]
    assert all(isinstance(v, tuple) for v in smap(GEO)[0].values())
```

      Where a parametrized expectation does not hold on the real files, **measure it first**
      (`uv run python -c "…"`), then either fix the code or replace the expectation with the
      measured one plus a comment naming the rule line. Do not delete a test to go green.

- [ ] **Step 2:** run → FAIL (`cannot import name 'source_map'`).
- [ ] **Step 3:** implement `section_inventory`, `expand_target`, `source_map`, `un_substitute`.
- [ ] **Step 4:** print the chain edges the closure admits and rejects for all four strands and check
      them by eye against file order — this is the F2 acceptance evidence:
      `uv run python -c "…"` listing `rule_id`s containing `>`.
- [ ] **Step 5:** `uv run pytest -q` → 1680+ passed.
- [ ] **Step 6: Commit** — `feat(reverse): invert [substitute] — per-section inventories, ordered chains, provenance`

**Acceptance:** all eight shapes inverted or noted; a multi-segment insertion is one key; no deletion
expanded; the fallback uses `table.nearest` with the target's own weights and non-marginal
inventory; the Georgian ordered chain (`substitute:79>substitute:118`) is followed and the Arabic
backwards chain is not; `section_inventory` is duplicate-free and in declaration order; every
alternative gains a `substitute` step and the substitute deletions and notes reach the `Pattern`.

---

## Task 5: `reverse.widen` over `[repair]` and `[post-stress]`

**Depends on:** Task 4. **Spec:** §3.3. **Interpretations:** V-18, V-29, V-30, V-31. **Review:**
F3, F4, F5.

**Files:** modify `src/strands/reverse.py`; append to `tests/test_reverse_sourcemap.py`.

**Interfaces:**

```python
WIDEN_SECTIONS = ("repair", "post-stress")

def widen(pattern: Pattern, target: RuleFile, irish: RuleFile,
          table: FeatureTable) -> Pattern
    """Spec §3.3. (a) For each SEG/ONE slot alternative that a [repair]/[post-stress] rule
    could have produced, add the rule's TARGET as a new alternative with that rule's Step
    appended (V-31). (b) For each epenthesis source of those sections, find every consecutive
    slot SPAN whose slots can spell the inserted sequence and record an OptionalGroup (V-30).
    (c) Collect the two sections' deletions into `pattern.deletions` (V-7). Stress is ignored."""
```

Called between `parse_pattern` and `un_substitute`. The two source maps are built with
`section_inventory` (V-29) and carry **no** fallback and **no** identity sources.

- [ ] **Step 1: Write the failing tests** — append:

```python
from strands.reverse import invert_respell, parse_pattern, widen

# V-30 accepted miss: no real strand shows a two-segment insertion in its respelling
# (arabic-egy deletes the /ʔ/ of `0 -> ʔ i` with `ʔ -> "" / # _`), so the ATOMIC-GROUP
# behaviour is tested on a synthetic file where both inserted segments are printed.
SYNTH_GROUP = parse_rules("""
[meta]
name = SynthGroup
[inventory]
q i s k
[repair]
0 -> q i / # _ s
[respell]
q -> "q"
i -> "i"
s -> "s"
k -> "k"
""", TABLE, path="synth-group")


def _parse(rf, text):
    """V-35: both `invert_respell` values reach the pattern."""
    chunks, notes = invert_respell(rf, TABLE)
    return parse_pattern(text, chunks, notes=notes)


def pat(rf, text):
    return widen(_parse(rf, text), rf, IRISH, TABLE)


def alt_set(p):
    return {a.segments for s in p.slots for a in s.alts}


def test_a_welsh_long_vowel_gains_its_short_partner():
    """spec §3.3: Welsh long vowels <- the short one via the §4.3 lengthening."""
    got = alt_set(pat(WEL, "â"))
    assert ("aː",) in got and ("a",) in got


def test_welsh_y_gains_every_short_vowel_it_could_have_reduced_from():
    got = alt_set(pat(WEL, "y"))
    assert ("ə",) in got and len(got) > 1


def test_welsh_initial_ll_gains_plain_l():
    got = alt_set(pat(WEL, "ll"))
    assert ("ɬ",) in got and ("l",) in got


def test_georgian_degemination_widens_a_consonant_slot():
    assert ("v", "v") in alt_set(pat(GEO, "v"))


def test_a_widened_alternative_records_the_widening_rule():
    """V-31 / F5: draft 1 lost the rule id and could not print a source for it."""
    p = pat(WEL, "â")
    widened = [a for s in p.slots for a in s.alts if a.segments == ("a",)]
    assert widened and any(st.stage in ("post-stress", "repair")
                           for a in widened for st in a.steps)


# ---- optional GROUPS (V-30 / F4) -----------------------------------------------------------------

def test_a_single_segment_insertion_is_a_width_one_group():
    """Welsh prothetic ⟨y⟩ (`0 -> ə / # _ s {p t k}`)."""
    p = pat(WEL, "ysbryd")
    assert any(g.start == 0 and g.stop == 1 for g in p.groups)


def test_a_two_segment_insertion_is_ONE_group_of_width_two():
    """F4 / V-30: the inserted pair is atomic. Synthetic, because `arabic-egy`'s own
    `0 -> ʔ i` is invisible in its respelling (`ʔ -> \"\" / # _`)."""
    p = pat(SYNTH_GROUP, "qisk")
    assert [(g.start, g.stop) for g in p.groups] == [(0, 2)]


def test_no_group_covers_only_half_an_insertion():
    p = pat(SYNTH_GROUP, "qisk")
    assert all(g.stop - g.start == 2 for g in p.groups)


def test_the_arabic_pair_is_a_recorded_miss_not_a_silent_one():
    """V-30 accepted miss: `isk` is three slots and no group is found; a note says why."""
    p = pat(ARA, "isk")
    assert p.groups == () or all(g.stop - g.start == 2 for g in p.groups)
    assert any("unreachable" in n for n in p.notes)


def test_groups_are_sorted_and_non_overlapping():
    p = pat(WEL, "ysbryd")
    spans = [(g.start, g.stop) for g in p.groups]
    assert spans == sorted(spans)
    assert all(a[1] <= b[0] for a, b in zip(spans, spans[1:]))


def test_deletions_from_the_widened_sections_reach_the_pattern():
    """V-7: one word-level list, not a note on every slot."""
    p = pat(WEL, "u")
    assert isinstance(p.deletions, tuple)


def test_stress_is_ignored():
    for s in pat(WEL, "ysbryd").slots:
        assert all(m not in seg for a in s.alts for seg in a.segments
                   for m in ("ˈ", "ˌ", "."))


def test_widening_only_grows_the_slot_set():
    before = _parse(WEL, "â")
    after = widen(before, WEL, IRISH, TABLE)
    for b, a in zip(before.slots, after.slots):
        assert {x.segments for x in b.alts} <= {x.segments for x in a.alts}
```

      **Why the group fixture is synthetic (V-30 accepted miss).** `arabic-egy`'s two-segment
      insertion `0 -> ʔ i / # _ s [C -sonorant]` is unreachable from a real Arabic pattern, because
      `arabic-egy.rules [respell]` deletes the initial `/ʔ/` (`ʔ -> "" / # _`): `isk` parses to
      three slots `/i s k/` and there is no `ʔ` slot for the group to start on. Inverting a respell
      deletion is out of scope in v1 (R3's reasoning), so the group machinery is tested on
      `SYNTH_GROUP`, where both inserted segments are printed, and the Arabic case is asserted to
      be a **recorded** miss (an `invert_respell` note), not a silent one.

- [ ] **Step 2:** run → FAIL. **Step 3:** implement `widen`.
- [ ] **Step 4:** `uv run pytest -q` → 1680+ passed.
- [ ] **Step 5: Commit** — `feat(reverse): widen from [repair]/[post-stress] with atomic optional groups`

**Acceptance:** the four §3.3 examples hold; widening is monotone and records its rule; on
`SYNTH_GROUP` a two-segment insertion produces exactly one width-two group and no half-groups;
the `arabic-egy` pair is a recorded miss with a note, not a silent one; groups are sorted and
disjoint; stress never appears in a slot.

---

## Task 6: the constraint set, `format_rule_line`, `render_pattern`, `report()`

**Depends on:** Tasks 1, 5. **Spec:** §3.4 (rendering), §4, R7. **Interpretations:** V-7, V-13,
V-14, V-15, V-21, V-30, V-31, V-32. **Review:** F5, F6.

**Files:** modify `src/strands/reverse.py`; create `tests/test_reverse_report.py`.

**Interfaces:**

```python
RULE_COL = 62

@dataclass(frozen=True)
class ConstraintLine:
    description: str
    rule_ids: tuple[str, ...]
    tag: str                        # "" | "design" | "fallback"
    kind: str
    context: str

@dataclass(frozen=True)
class Constraint:
    label: str
    target: str
    lines: tuple[ConstraintLine, ...]
    notes: tuple[str, ...]
    unconstrained: bool

def format_rule_line(prefix: str, description: str, suffix: str) -> list[str]   # V-32
def constraints(pattern: Pattern) -> tuple[Constraint, ...]
def dropped_lines(pattern: Pattern) -> tuple[ConstraintLine, ...]               # V-7
def render_pattern(pattern: Pattern) -> tuple[str, ...]
def report(word: str, strand: str, pattern: Pattern, examples: Sequence["Example"] = (),
           *, tried: int = 0, cap_hit: bool = False, verified: bool = True) -> list[str]
```

**Grouping (V-31 / F5).** Every `(slot, Alternative)` pair is turned into a `ConstraintLine` keyed
by `(kind, tag, description, context)` — **context is part of the key**, so two sources with
different environments print as two lines and the exclusions block can name each one. `description`
is `g2p_inverse.describe(alt.segments)` plus the kind phrase (V-15); `rule_ids` is every step's
`rule_id` for that group, in first-seen order, deduped. Lines are sorted by
`(_KIND_RANK[kind], 0 if tag != "design" else 1, first rule_id, description)`.

**`format_rule_line` (V-32).** `prefix + description` first; then `suffix` at code-point index
`RULE_COL`. When `len(prefix + description) >= RULE_COL - 1`, emit that as one line and `suffix`
on a second line indented `RULE_COL` spaces. Each returned line is `rstrip()`ed. **All three
rule-bearing blocks use it**, with these prefixes:

| block | first-line prefix | continuation prefix | suffix |
|---|---|---|---|
| constraints | `f"  {label:<3} ← "` | `"      ← "` | `",".join(rule_ids)` + `f" %{tag}"` when `tag in ("design","fallback")` |
| exclusions | `f"  {label} ← "` | — | `f"({rule_ids[0]} context)"` |
| possibly dropped | `f"  {label:<3} "` | — | same as constraints |

**`report()` output, line by line — the byte-exact contract** (no trailing whitespace; `report`
returns lines without newlines; the CLI joins with `"\n"` and appends one final `"\n"`):

```
1.  f"{word}  [{strand}]"
2.  "target segments: " + " ".join(c.target for c in constraints)
3.  ""
4.  "constraints"
5.  per constraint: "  {label:<3} unconstrained"  |  format_rule_line(...) per line
                    then per note: f"      note: {note}"
6.  ""
7.  "possibly dropped"          # only when pattern.deletions is non-empty (V-7)
      one format_rule_line per dropped_lines() entry
8.  ""                          # only when block 7 printed
9.  "exclusions"                # only when some line has a non-empty context (V-13)
      one format_rule_line per (constraint, line) with a context, in report order
10. ""                          # only when block 9 printed
11. "Irish spelling pattern"
      the lines of render_pattern(), each already "  "-prefixed
12. ""
13. the examples block
```

Examples block:

```
verified: f"verified examples ({len(examples)} of {tried} tried; 0 fallbacks unless shown)"
          + ("; candidate cap 2000 hit" if cap_hit else "")
          then one line per example, or "  none"
skipped:  "verified examples: skipped (--examples 0)"
```

Example line, with `w1 = max(11, max(len(e.orthography)) + 2)` and
`w2 = max(9, max(len(e.respelling)) + 2)` over the printed examples:
`"  " + e.orthography.ljust(w1) + e.respelling.ljust(w2) + e.ipa`, then `"  " + " ".join(e.flags)`
when there are flags, then `f"  fallbacks:{e.fallbacks}"` when `e.fallbacks`.

**`render_pattern` (V-14, V-30, R7).** One base line: per slot, `*` for `ANY`, `?` for `ONE` with no
alternatives, else `"|".join(graphemes)` wrapped in `(...)` when more than one, where the graphemes
come from `g2p_inverse.readings_for` / `VOWEL_READINGS` (no quality words, deduped, registry order,
capped at `_ALT_CAP = 6` with a trailing `…`). An **optional group** wraps its whole span in one
`( … )?`. Vowel-letter choice is filtered by the same caol-le-caol admissibility `spell` uses,
taking the quality from the **first-listed** reading of each neighbouring consonant slot; a slot
left empty by the filter falls back to its unfiltered alternation. Epenthesis alternatives are
**excluded** from the base line (they spell nothing); instead, per insertion group, one extra line
`f"  or, with {labels} inserted:  {base_without_that_group}   (context: {context})"`.

- [ ] **Step 1: Write the failing tests** — `tests/test_reverse_report.py`. Structure: the unit
      tests below, then **six golden tests** that compare the *entire* `report()` output to a literal
      expected string (F6). Write the goldens **last**, by running the finished code once and pasting
      the output — but only after eyeballing it against spec §4, and each golden gets a comment
      saying what it pins.

```python
"""Task 6: the constraint set and the report format (reverse spec §4; V-7, V-13 … V-15,
V-31, V-32). The golden tests are the layout contract (F6)."""
import pytest

from helpers import TABLE, irish, target
from strands.reverse import (RULE_COL, constraints, dropped_lines, format_rule_line,
                             invert_respell, parse_pattern, render_pattern, report,
                             source_map, un_substitute, widen)

IRISH = irish()
GEO = target("georgian")
WEL = target("welsh")


def analysed(rf, text):
    p = widen(_parse(rf, text), rf, IRISH, TABLE)
    smap, deletions, notes = source_map("substitute", rf, IRISH, TABLE)
    return un_substitute(p, smap, deletions=deletions, notes=notes)


def lines(rf, text, **kw):
    return report(text, rf.meta["name"].lower(), analysed(rf, text), **kw)


# ---- the formatter (V-32) ------------------------------------------------------------------------

def test_the_rule_column_starts_at_a_fixed_code_point_index():
    (line,) = format_rule_line("  a   ← ", "a, á", "substitute:44")
    assert line.index("substitute:44") == RULE_COL


def test_a_long_description_pushes_the_rules_to_a_continuation_line():
    long = "x" * (RULE_COL + 10)
    out = format_rule_line("  a   ← ", long, "substitute:44")
    assert len(out) == 2 and out[1] == " " * RULE_COL + "substitute:44"


def test_the_formatter_never_leaves_trailing_whitespace():
    for out in (format_rule_line("  a   ← ", "a", ""), format_rule_line("", "b", "r:1")):
        assert all(l == l.rstrip() for l in out)


# ---- the constraint set ---------------------------------------------------------------------------

def test_a_wildcard_slot_is_unconstrained():
    cs = constraints(analysed(GEO, "a*"))
    assert cs[1].unconstrained and cs[1].target == "*"


def test_lines_are_grouped_and_ordered_by_source_kind():
    cs = constraints(analysed(GEO, "v"))
    kinds = [line.kind for line in cs[0].lines]
    assert kinds == sorted(kinds, key=["identity", "rule", "fallback", "epenthesis"].index)


def test_two_sources_with_different_contexts_are_two_lines():
    """F5: draft 1's key omitted context and merged them."""
    cs = constraints(analysed(GEO, "v"))
    ctxs = [l.context for l in cs[0].lines]
    assert len(set(ctxs)) > 1


def test_the_epenthesis_line_says_no_irish_letter():
    (c,) = constraints(analysed(GEO, "v"))
    assert any(line.description == "inserted, no Irish letter" for line in c.lines)


def test_a_design_tag_is_shown_and_an_attested_one_is_not():
    text = "\n".join(lines(GEO, "v", verified=False))
    assert "%design" in text and "%attested" not in text


def test_deletions_are_one_block_per_word_not_a_note_per_slot():
    """V-7, owner ruling: draft 1 repeated them on every slot."""
    out = lines(WEL, "uu", verified=False)
    assert out.count("possibly dropped") <= 1
    assert dropped_lines(analysed(WEL, "uu"))


def test_a_SUBSTITUTE_deletion_reaches_the_block_and_the_report():
    """F3: welsh.rules:161-164 are `w -> 0` / `j -> 0` in [substitute]. Draft 2 dropped them
    between source_map and the Pattern, so only [repair]/[post-stress] deletions ever showed.
    The repair/post-stress ones are filtered out here so the assertion cannot pass on them."""
    subs = [l for l in dropped_lines(analysed(WEL, "uu"))
            if any(r.startswith("substitute:") for r in l.rule_ids)]
    assert subs, [l.rule_ids for l in dropped_lines(analysed(WEL, "uu"))]
    text = "\n".join(lines(WEL, "uu", verified=False))
    assert "possibly dropped" in text
    assert any(r in text for l in subs for r in l.rule_ids)


def test_a_two_context_alternative_is_one_line_and_two_exclusions():
    """F4 re-check / V-31: an alternative whose walk crosses two context-bearing rules
    collapses to ONE constraint line (contexts joined) and prints TWO exclusion lines (one per
    step, each with its own rule id). Build the Pattern by hand so the two contexts are
    guaranteed; MEASURE a real two-context walk first and use it if one exists."""
    from strands.reverse import Alternative, Constraint, Pattern, Slot, Step
    a = Alternative(("ɑ",), (
        Step("respell", "respell:330", "attested", "V _ #", "rule"),
        Step("substitute", "substitute:70", "design", "C _", "rule"),
    ))
    p = Pattern(text="a", slots=(Slot("seg", "a", (a,)),))
    (c,) = constraints(p)
    (line,) = c.lines
    assert line.context == "C _ ; V _ #"                 # forward stage order
    assert line.rule_ids == ("substitute:70", "respell:330")
    assert line.tag == "design" and line.kind == "rule"
    out = report("a", "georgian", p, verified=False)
    excl = out[out.index("exclusions") + 1:]
    excl = [l for l in excl if l.startswith("  ")][:2]
    assert len(excl) == 2
    assert "substitute:70" in excl[0] and "respell:330" in excl[1]


# ---- the report ------------------------------------------------------------------------------------

def test_the_header_and_the_target_segment_line():
    out = lines(GEO, "ar", verified=False)
    assert out[0] == "ar  [georgian]"
    assert out[1] == "target segments: ɑ r"
    assert out[2] == "" and out[3] == "constraints"


def test_no_line_has_trailing_whitespace():
    for line in lines(GEO, "ar*v*", verified=False):
        assert line == line.rstrip()


def test_the_exclusions_section_appears_only_when_a_context_exists():
    assert "exclusions" in lines(GEO, "v", verified=False)
    assert "exclusions" not in lines(GEO, "r", verified=False)


def test_the_report_is_byte_identical_across_runs():
    assert lines(GEO, "ar*v*", verified=False) == lines(GEO, "ar*v*", verified=False)


def test_examples_zero_says_it_skipped_verification():
    assert "verified examples: skipped (--examples 0)" in lines(GEO, "ar", verified=False)


# ---- the Irish spelling pattern ---------------------------------------------------------------------

def test_alternation_is_printed_never_a_pick():
    line = render_pattern(analysed(GEO, "a"))[0]
    assert line.startswith("  ") and line.count("(") == line.count(")")


def test_an_optional_group_is_one_parenthesised_span():
    out = render_pattern(analysed(WEL, "ysbryd"))[0]
    assert ")?" in out


def test_an_insertion_gets_its_own_or_line():
    """V-14 (Q2)."""
    out = render_pattern(analysed(GEO, "av"))
    assert any(l.strip().startswith("or, with") and "context:" in l for l in out)


def test_caol_le_caol_filters_the_vowel_letters_in_the_rendering():
    line = render_pattern(analysed(GEO, "ka"))[0]
    assert "e|" not in line


# ---- the six goldens (F6) ---------------------------------------------------------------------------
# Each compares the ENTIRE report() output. Regenerate deliberately, never by pasting a diff.

GOLDEN_SIMPLE = """\
<paste: report("r", "georgian", analysed(GEO, "r"), verified=False)>
"""            # pins: header, target segments, a normal constraint line at RULE_COL, no
               # exclusions block, verification skipped

GOLDEN_CONTINUATION = "..."   # pins: a description long enough to wrap to a continuation line
GOLDEN_EXCLUSIONS = "..."     # pins: the exclusions block and its (rule context) suffix
GOLDEN_DROPPED = "..."        # pins: the once-per-word `possibly dropped` block (V-7)
GOLDEN_EXAMPLES = "..."       # pins: the examples block with flags and a fallback count
GOLDEN_SESSION = "..."        # pins: the whole `Ar*v*  [georgian]` block of spec §4


@pytest.mark.parametrize("golden,args,kwargs", [
    (GOLDEN_SIMPLE, ("r", GEO), {"verified": False}),
    # ... one row per golden
])
def test_the_report_matches_its_golden(golden, args, kwargs):
    text, rf = args
    assert "\\n".join(lines(rf, text, **kwargs)) + "\\n" == golden
```

- [ ] **Step 2:** run → FAIL. **Step 3:** implement `format_rule_line`, `constraints`,
      `dropped_lines`, `render_pattern`, `report`.
- [ ] **Step 4:** generate the six goldens, **read each one against spec §4 before pasting it**, and
      paste the `Ar*v*` one into the commit message too.
- [ ] **Step 5:** `uv run pytest -q` → 1680+ passed.
- [ ] **Step 6: Commit** — `feat(reverse): constraint set, one line formatter, spelling pattern and the §4 report`

**Acceptance:** the spec's sections in the spec's order; one formatter for all three rule-bearing
blocks with a code-point-indexed rule column and a continuation line; six goldens covering normal,
continuation, wrapped, exclusions, examples/skipped and the full session block; sources with
different contexts print separately; a two-context alternative is one constraint line and two
exclusion lines; a `[substitute]` deletion reaches the once-per-word `possibly dropped` block;
alternation is never resolved to a pick.

---

## Task 7: `expand()` and `verify()`

**Depends on:** Tasks 2, 6. **Spec:** §3.5, R4, R5. **Interpretations:** V-22 … V-26, V-30, V-34.
**Review:** F8.

**Files:** modify `src/strands/reverse.py`; create `tests/test_reverse_verify.py`.

**Interfaces:**

```python
CAP = 2000
PALETTE = ("a", "ɛ", "ɪ", "ɔ", "ʊ", "ɾˠ", "l̪ˠ", "n̪ˠ", "mˠ", "sˠ",
           "d̪ˠ", "t̪ˠ", "k", "ɡ", "bˠ")
STAR_LENGTHS = (0, 1, 2)

@dataclass(frozen=True)
class Candidate:
    segments: tuple[str, ...]
    rank: int

@dataclass(frozen=True)
class Example:
    orthography: str
    respelling: str
    ipa: str
    flags: tuple[str, ...]
    fallbacks: int
    rank: int
    spelling_index: int            # V-34

def expand(pattern: Pattern, *, cap: int = CAP) -> Iterator[Candidate]
def verify(pattern: Pattern, target: RuleFile, irish: RuleFile, table: FeatureTable,
           *, limit: int = 8, cap: int = CAP, ipa_mode: bool = False,
           raw_pattern: str | None = None) -> tuple[tuple[Example, ...], int, bool]
```

`expand` per V-22/V-23/V-24, with optional groups atomic (V-30). `verify` per V-25/V-26/V-34,
returning `(examples, tried, cap_hit)`; `examples` sorted by
`(fallbacks, len(flags), rank, spelling_index)`, de-duplicated by orthography, truncated to `limit`.
`raw_pattern` defaults to `pattern.text`.

- [ ] **Step 1: Write the failing tests** — `tests/test_reverse_verify.py`:

```python
"""Task 7: candidate expansion and forward verification (reverse spec §3.5; V-22 … V-26, V-34)."""
import itertools

import pytest

from helpers import TABLE, irish, target
from strands.reverse import (CAP, PALETTE, expand, invert_respell, parse_pattern, source_map,
                             un_substitute, verify, widen)

IRISH = irish()
GEO = target("georgian")
WEL = target("welsh")
ARA = target("arabic-egy")


def analysed(rf, text):
    p = widen(_parse(rf, text), rf, IRISH, TABLE)
    smap, deletions, notes = source_map("substitute", rf, IRISH, TABLE)
    return un_substitute(p, smap, deletions=deletions, notes=notes)


def test_the_palette_is_the_spec_list_in_irish_ipa():
    assert len(PALETTE) == 15 and PALETTE[:5] == ("a", "ɛ", "ɪ", "ɔ", "ʊ")
    assert all(p in IRISH.inventory for p in PALETTE)


def test_a_star_is_filled_with_zero_one_then_two_palette_segments():
    lengths = [len(c.segments) for c in itertools.islice(expand(analysed(GEO, "*")), 20)]
    assert lengths[0] == 0 and sorted(lengths) == lengths


def test_cheapest_first_puts_identity_before_fallback():
    cands = list(itertools.islice(expand(analysed(GEO, "ar")), 5))
    assert cands and cands[0].rank == 0


def test_an_optional_group_is_present_or_absent_as_a_unit():
    """V-30 / F4: no candidate may carry half of a two-segment insertion. Uses Task 5's
    SYNTH_GROUP, where both inserted segments are printed (arabic-egy's own pair is
    unreachable — V-30's accepted miss)."""
    from test_reverse_sourcemap import SYNTH_GROUP
    p = analysed(SYNTH_GROUP, "qisk")
    (group,) = p.groups
    inserted = ("q", "i")
    for c in itertools.islice(expand(p), 60):
        head = c.segments[:2]
        assert head == inserted or inserted[0] not in c.segments[:1], c.segments


def test_the_cap_is_two_thousand_and_is_honoured():
    assert CAP == 2000
    assert len(list(expand(analysed(GEO, "a*a*"), cap=25))) == 25


def test_expansion_is_deterministic():
    a = [c.segments for c in itertools.islice(expand(analysed(GEO, "ar")), 50)]
    b = [c.segments for c in itertools.islice(expand(analysed(GEO, "ar")), 50)]
    assert a == b


# ---- verification (V-34 / F8) ---------------------------------------------------------------------

def test_every_kept_example_really_matches_the_pattern_through_the_real_engine():
    import fnmatch
    import unicodedata
    examples, tried, _cap = verify(analysed(GEO, "ar*"), GEO, IRISH, TABLE, limit=5, cap=300)
    assert tried > 0
    for e in examples:
        assert fnmatch.fnmatchcase(unicodedata.normalize("NFC", e.respelling).casefold(), "ar*")


def test_a_match_that_is_not_the_first_spelling_is_still_found():
    """F8: draft 1 used spell(...)[0] only. `ardmhaor` is not the first spelling of its own
    IPA (⟨bh⟩ precedes ⟨mh⟩ in the g2p table), and it is the spec's own example."""
    examples, _t, _c = verify(analysed(GEO, "ar*v*"), GEO, IRISH, TABLE, limit=40, cap=2000)
    orths = [e.orthography for e in examples]
    assert "ardmhaor" in orths, orths


def test_no_orthography_is_printed_twice():
    examples, _t, _c = verify(analysed(GEO, "ar*"), GEO, IRISH, TABLE, limit=8, cap=400)
    assert len({e.orthography for e in examples}) == len(examples)


def test_the_cap_counts_unique_forward_runs():
    """V-34: `tried` and the cap are the same counter, and a repeated spelling is skipped
    before any forward work."""
    _e, tried, cap_hit = verify(analysed(GEO, "a*a*"), GEO, IRISH, TABLE, limit=1, cap=10)
    assert tried <= 10 and cap_hit is True


def test_examples_are_ranked_by_fallbacks_then_flags_then_rank_then_spelling():
    examples, _t, _c = verify(analysed(GEO, "ar*"), GEO, IRISH, TABLE, limit=8, cap=400)
    keys = [(e.fallbacks, len(e.flags), e.rank, e.spelling_index) for e in examples]
    assert keys == sorted(keys)


def test_a_candidate_the_engine_cannot_run_is_counted_not_raised():
    _e, tried, _c = verify(analysed(GEO, "*"), GEO, IRISH, TABLE, limit=3, cap=120)
    assert tried >= 1


def test_ipa_mode_matches_the_unmarked_ipa():
    from strands.reverse import parse_ipa_pattern
    smap, deletions, notes = source_map("substitute", GEO, IRISH, TABLE)
    p = un_substitute(widen(parse_ipa_pattern("ɑr*", GEO, TABLE), GEO, IRISH, TABLE),
                      smap, deletions=deletions, notes=notes)
    examples, _t, _c = verify(p, GEO, IRISH, TABLE, limit=3, cap=200, ipa_mode=True,
                              raw_pattern="ɑr*")
    assert all(all(m not in e.ipa for m in ("ˈ", "ˌ", ".")) for e in examples)
```

- [ ] **Step 2:** run → FAIL. **Step 3:** implement `expand` (a `heapq` over index tuples, V-24) and
      `verify` (V-34).
- [ ] **Step 4:** time it — `uv run python -c "…"` on `Ar*v*` for Georgian at the real cap, and
      report the wall time in the commit message. **Do not lower `CAP`** (R4 fixes it at 2000); the
      sanctioned speed-ups are the `seen` set (V-34) and dropping a candidate whose `spell()` is
      empty before any forward work.
- [ ] **Step 5:** `uv run pytest -q` → 1680+ passed.
- [ ] **Step 6: Commit** — `feat(reverse): candidate expansion (cheapest first, cap 2000) and de-duplicated verification`

**Acceptance:** palette and star lengths are R5's; groups are atomic; enumeration is deterministic
and cheapest first; the cap counts unique forward runs and is reported; every printed example has
been through `run_entry` and `fnmatchcase`; a non-first spelling can win, and `ardmhaor` does.

---

## Task 8: `cli.cmd_reverse`

**Depends on:** Task 7. **Spec:** §2, §4 (old-irish), §6 bullet 5, R1, R6. **Interpretations:**
V-16, V-25, V-33.

**Files:** modify `src/strands/cli.py`, `src/strands/reverse.py`; create
`tests/test_cli_reverse.py`.

**CLI contract.**

```
strands reverse PATTERN --strand X [--examples N] [--ipa]
```

- `_parse(args, {"--strand": True, "--examples": True, "--ipa": False}, 1)`.
- `--strand` missing → `UsageError("reverse needs --strand")`, exit 2.
- `--strand all` → `UsageError("reverse takes one strand, not all (the constraint sets are per strand)")`, exit 2.
- `--strand` not in `TARGETS` → the existing `_strands` message, exit 2.
- `--examples` not a non-negative integer → `UsageError("--examples takes a non-negative integer")`, exit 2. Default 8; `0` skips verification.
- `--ipa` with `--strand old-irish` → `UsageError("--ipa is meaningless for old-irish (lexicon lookup only)")`, exit 2.
- A `ReverseError` from either parser → exit 2 via `UsageError`.
- `COMMANDS`, `_USAGE`, `_HANDLERS` all gain `"reverse"`; the module docstring gains the usage line
  and a paragraph on what the command is.
- With `--ipa` the pattern goes through `parse_ipa_pattern` (V-33); without it, through
  `invert_respell` + `parse_pattern`. Both then go through `widen` → `un_substitute` → `verify`.

**Multi-word (spec §2).** `PATTERN.split()` — each word is analysed and reported separately, blocks
joined by a blank line, in input order.

**old-irish (R6).** `reverse.old_irish_matches(pattern: str) -> tuple[tuple[str, str, str], ...]`:
read `lexicon.read_lexicon()`, keep rows whose `oi_nom` is non-empty and matches per V-25, return
`(oi_nom, orthography, flag)` sorted by `lexicon.key(orthography)`. Block:

```
<PATTERN>  [old-irish]
note: old-irish is lexicon lookup only; §3's constraint set does not apply.

matches
  <oi_nom padded to w1><orthography padded to w2><flag>
```

with `w1 = max(len(oi_nom)) + 2`, `w2 = max(len(orthography)) + 2`, and `  none` when nothing
matches. Rows with an empty `oi_nom` (`status = none`) are skipped.

- [ ] **Step 1: Write the failing tests** — `tests/test_cli_reverse.py`:

```python
"""Task 8: `strands reverse` at the CLI (reverse spec §2, §4, §6 bullet 5; R1, R6)."""
import pytest

from strands.cli import main


def run(capsys, *args):
    code = main(["reverse", *args])
    out, err = capsys.readouterr()
    return code, out, err


def test_it_is_a_command_with_a_usage_line():
    from strands.cli import COMMANDS, _HANDLERS, _USAGE
    assert "reverse" in COMMANDS and "reverse" in _HANDLERS
    assert _USAGE["reverse"] == "strands reverse PATTERN --strand X [--examples N] [--ipa]"


def test_a_simple_pattern_prints_the_spec_sections(capsys):
    code, out, _err = run(capsys, "ar", "--strand", "georgian", "--examples", "0")
    assert code == 0
    for section in ("target segments:", "constraints", "Irish spelling pattern",
                    "verified examples"):
        assert section in out
    assert out.startswith("ar  [georgian]\n")


def test_the_session_case_lists_the_three_v_sources(capsys):
    """spec §6 bullet 4."""
    code, out, _err = run(capsys, "Ar*v*", "--strand", "georgian", "--examples", "0")
    assert code == 0
    block = out.split("Irish spelling pattern")[0]
    assert "inserted, no Irish letter" in block and block.count("←") >= 4


def test_examples_are_printed_and_capped(capsys):
    code, out, _err = run(capsys, "ar*", "--strand", "georgian", "--examples", "3")
    assert code == 0 and "verified examples (" in out
    body = out.split("verified examples (")[1].splitlines()[1:]
    assert len([l for l in body if l.startswith("  ")]) <= 3


def test_examples_zero_skips_verification(capsys):
    _c, out, _e = run(capsys, "ar", "--strand", "georgian", "--examples", "0")
    assert "verified examples: skipped (--examples 0)" in out


def test_ipa_mode_uses_the_ipa_parser(capsys):
    code, out, _err = run(capsys, "ɑr*", "--strand", "georgian", "--ipa", "--examples", "0")
    assert code == 0 and out.startswith("ɑr*  [georgian]")


def test_an_unknown_letter_is_reported(capsys):
    _c, out, _e = run(capsys, "aqa", "--strand", "georgian", "--examples", "0")
    assert "no Irish source for 'q'" in out


def test_multi_word_patterns_are_reported_word_by_word(capsys):
    _c, out, _e = run(capsys, "ar va", "--strand", "georgian", "--examples", "0")
    assert out.count("[georgian]") == 2


def test_old_irish_is_a_lexicon_lookup_with_a_note(capsys):
    code, out, _err = run(capsys, "*mac*", "--strand", "old-irish")
    assert code == 0 and "lexicon lookup only" in out and "matches" in out


def test_old_irish_with_no_match_says_none(capsys):
    _c, out, _e = run(capsys, "zzzz*", "--strand", "old-irish")
    assert "  none" in out


@pytest.mark.parametrize("args,fragment", [
    (["ar"], "needs --strand"),
    (["ar", "--strand", "all"], "not all"),
    (["ar", "--strand", "klingon"], "unknown strand"),
    (["ar", "--strand", "georgian", "--examples", "-1"], "non-negative"),
    (["ar", "--strand", "georgian", "--examples", "x"], "non-negative"),
    (["[ao", "--strand", "georgian"], "["),
    (["[!ao]", "--strand", "georgian"], "["),
    (["ar", "--strand", "old-irish", "--ipa"], "old-irish"),
    (["ɑQ", "--strand", "georgian", "--ipa"], "Q"),
])
def test_usage_errors_exit_two(capsys, args, fragment):
    code = main(["reverse", *args])
    _out, err = capsys.readouterr()
    assert code == 2 and fragment in err


def test_output_is_byte_identical_across_runs(capsys):
    _c, a, _e = run(capsys, "ar*v*", "--strand", "georgian", "--examples", "2")
    _c, b, _e = run(capsys, "ar*v*", "--strand", "georgian", "--examples", "2")
    assert a == b
```

- [ ] **Step 2:** run → FAIL. **Step 3:** implement `cmd_reverse` and `old_irish_matches`; register
      the command; extend the `cli.py` docstring.
- [ ] **Step 4:** run it by hand on all four strands and paste the `Ar*v*` block into the commit
      message.
- [ ] **Step 5:** `uv run pytest -q` → 1680+ passed.
- [ ] **Step 6: Commit** — `feat(cli): strands reverse — constraint set, spelling pattern, verified examples`

**Acceptance:** every exit code in the table; `--ipa` routes to the IPA parser; multi-word works;
old-irish is lexicon fnmatch with the "§3 does not apply" note; two runs are byte-identical.

---

## Task 9: round-trip regression and the four ratchets

**Depends on:** Task 8. **Spec:** §6 bullets 3 and 4. **Interpretations:** V-25. **Review:** F9.

**Files:** create `tests/test_reverse_regression.py` and
`tests/ratchets/reverse-{welsh,georgian,arabic-egy,dutch}.json`; modify `pyproject.toml`.

**The two rates (spec §6 bullet 3), per strand, over every `sources/irish/test-words.tsv` row with
a hand IPA:**

1. **`pattern`** — run the row forward (`run_entry(entry, "DESC", …)`), take `result.respelling`,
   reverse it, and ask whether the row's own Irish IPA is **admitted by the pattern**:
   `reverse.pattern_admits(pattern, irish_segments) -> bool`, a greedy left-to-right matcher with
   backtracking over the slots (an optional group may be skipped as a unit), ~40 lines, written in
   this task.
2. **`example`** — the row's own spelling appears among the verified examples with `limit=8`,
   **counted only over rows where the cap was not hit** (spec §6). Capped rows are excluded from
   this rate's denominator and counted as `capped`.

Ratchet shape (fix-round C1): `{"admits": rate, "admits_n": int, "examples": rate,
"examples_n": int}` — the two rates are measured by two runs, `admits` over all rows with
`limit=0` and `examples` over the first twelve rows at `cap=200`. **No floor requirement.**

**F9 — the ratchet is measured at the spec's cap.** Draft 1 measured at `cap=200`, which ratchets a
number the shipped command never produces. Revised:

- `reverse_regression(..., cap=CAP)` is the **normative** run and the one the ratchet compares.
  Time it; if it exceeds ~2 minutes for the four strands, mark the ratchet test
  `@pytest.mark.slow` and add to `pyproject.toml`:

  ```toml
  [tool.pytest.ini_options]
  testpaths = ["tests"]
  pythonpath = ["src"]
  markers = ["slow: measured at the shipped candidate cap; excluded with -m 'not slow'"]
  ```

  Record in the module docstring and the commit message how to run it (`uv run pytest -q` runs
  everything; `-m "not slow"` skips it) and how long it takes. **The default `uv run pytest -q`
  still runs it** — a marker is a label, not a skip.
- A separate, **fast** `cap=200` run stays as a smoke test: it asserts only that the machinery runs
  and is deterministic, and it is **not** called a ratchet and has no ratchet file.

**F6 (P2) — the marker must actually save the time.** Draft 2 computed the full runs at **module
import**, so `-m "not slow"` still paid for them; a marker on a test body is worthless when the work
happens at collection. Revised: the full run is a **session-scoped fixture**
(`@pytest.fixture(scope="session")`, in `tests/test_reverse_regression.py` — no `conftest.py` is
needed, and the repo has none), consumed **only** by tests that are themselves
`@pytest.mark.slow`; the fast `cap=200` smoke report is a separate unmarked session fixture. Under
`-m "not slow"` the slow fixture is never requested and never runs.

- [ ] **Step 1: Write the failing tests** — `tests/test_reverse_regression.py`:

```python
"""Task 9: the reverse round trip per strand (reverse spec §6 bullets 3-4).

The ratchet is measured at the SHIPPED cap (reverse.CAP = 2000), so it is slow; run
`uv run pytest -q -m "not slow"` to skip it. The cap=200 run below is a smoke test, not a
ratchet."""
import json

import pytest

from helpers import ROOT, TABLE, irish, target
from strands.reverse import CAP, reverse_regression

IRISH = irish()
STRANDS = ("welsh", "georgian", "arabic-egy", "dutch")


@pytest.fixture(scope="session")
def full():
    """F6: session-scoped, so `-m \"not slow\"` never pays for it. Only `slow` tests ask."""
    return {name: reverse_regression(name, target(name), IRISH, TABLE, cap=CAP)
            for name in STRANDS}


@pytest.fixture(scope="session")
def smoke():
    return reverse_regression("georgian", target("georgian"), IRISH, TABLE, cap=200)


def ratchet(name):
    return json.loads((ROOT / "tests" / "ratchets" / f"reverse-{name}.json")
                      .read_text(encoding="utf-8"))


@pytest.mark.slow
@pytest.mark.parametrize("name", STRANDS)
def test_the_ratchet_holds_at_the_shipped_cap(name, full):
    """F9: the ratchet must describe the command the user actually runs."""
    data, rep = ratchet(name), full[name]
    assert rep.cap == CAP
    assert rep.pattern_rate >= data["pattern"] - 1e-9, rep.summary()
    assert rep.example_rate >= data["example"] - 1e-9, rep.summary()


@pytest.mark.slow
@pytest.mark.parametrize("name", STRANDS)
def test_the_ratchet_records_its_denominators(name, full):
    data = ratchet(name)
    assert set(data) == {"pattern", "example", "n", "capped"}
    assert data["n"] == full[name].n


@pytest.mark.slow
@pytest.mark.parametrize("name", STRANDS)
def test_the_example_rate_excludes_the_capped_rows(name, full):
    """spec §6: 'when the candidate cap is not hit'."""
    rep = full[name]
    assert rep.example_denominator == rep.n - rep.capped


def test_the_ratchet_files_all_exist_without_running_the_slow_pass():
    """Unmarked, cheap: a missing or malformed ratchet file fails fast."""
    for name in STRANDS:
        assert set(ratchet(name)) == {"pattern", "example", "n", "capped"}


def test_the_smoke_run_is_deterministic_and_is_not_the_ratchet(smoke):
    again = reverse_regression("georgian", target("georgian"), IRISH, TABLE, cap=200)
    assert again.rows == smoke.rows and smoke.cap == 200


# ---- the session case (spec §6 bullet 4) -------------------------------------------------------

def analysed_geo(text):
    from strands.reverse import (invert_respell, parse_pattern, source_map, un_substitute,
                                 widen)
    geo = target("georgian")
    p = widen(_parse(geo, text), geo, IRISH, TABLE)
    smap, deletions, notes = source_map("substitute", geo, IRISH, TABLE)
    return geo, un_substitute(p, smap, deletions=deletions, notes=notes)


def test_the_session_case_lists_exactly_the_three_v_sources():
    from strands.reverse import constraints
    _geo, p = analysed_geo("ar*v*")
    v = [c for c in constraints(p) if c.label == "v"][0]
    kinds = {(l.kind, l.description) for l in v.lines}
    assert ("epenthesis", "inserted, no Irish letter") in kinds
    assert any("bh" in d for _k, d in kinds)          # /w/ from broad bh/mh
    assert any("slender" in d for _k, d in kinds)     # /vʲ/ from slender bh/mh


def test_ardmhaor_verifies_for_the_session_case():
    from strands.reverse import verify
    geo, p = analysed_geo("ar*v*")
    examples, _t, _c = verify(p, geo, IRISH, TABLE, limit=40, cap=CAP)
    assert any(e.orthography == "ardmhaor" for e in examples), [e.orthography for e in examples]
```

- [ ] **Step 2:** run → FAIL (`cannot import name 'reverse_regression'`).
- [ ] **Step 3:** implement `pattern_admits`, `ReverseReport` (fields `rows`, `n`, `capped`, `cap`,
      `pattern_rate`, `example_rate`, `example_denominator`, `summary()`) and `reverse_regression`.
- [ ] **Step 4:** add the `markers` line to `pyproject.toml` (keeping `testpaths` and `pythonpath`).
- [ ] **Step 5:** write the four ratchets by hand. Fix-round C1 replaces the single `cap=CAP`
      run (hours per strand) with two runs: the cheap `admits` run over all rows with
      `limit=0`, and the paid `examples` run over the first twelve rows at `cap=200`. The four
      strands together take ~15 s.

```bash
uv run python - <<'PY'
import sys, time; sys.path.insert(0, "tests")
from helpers import TABLE, irish, target
from strands.regress import write_json_ratchet
from strands.reverse import read_hand_ipa_rows, reverse_regression
IR = irish()
EXAMPLE_ROWS, EXAMPLE_CAP = 12, 200        # kept in step with tests/test_reverse_regression.py
rows = read_hand_ipa_rows()[:EXAMPLE_ROWS]
for name in ("welsh", "georgian", "arabic-egy", "dutch"):
    t0 = time.time()
    admits = reverse_regression(name, target(name), IR, TABLE, limit=0)
    examples = reverse_regression(name, target(name), IR, TABLE, cap=EXAMPLE_CAP, rows=rows)
    write_json_ratchet(f"reverse-{name}",
                       {"admits": admits.admit_rate, "admits_n": admits.n,
                        "examples": examples.example_rate, "examples_n": examples.n})
    print(name, admits.summary(), "|", examples.summary(), f"{time.time()-t0:.1f}s")
PY
```

- [ ] **Step 6:** if `test_ardmhaor_verifies_for_the_session_case` fails, that is a **finding, not a
      test to delete**: report the rank *ardmhaor* reached, its `spelling_index`, and whether the
      cap, the caol-le-caol filter or a missing `g2p_inverse` reading excluded it, and stop for owner
      review.
- [ ] **Step 7:** `uv run pytest -q` → 1680+ passed. Record the new total, the four rates and the
      wall time in the commit message.
- [ ] **Step 8: Commit** — `test(reverse): per-strand round-trip ratchets at the shipped cap, and the Ar*v* session case`

**Acceptance:** four ratchet files with their denominators, measured at `reverse.CAP`; the example
rate excludes capped rows; a fast smoke run exists and is not called a ratchet; the full run is a
session-scoped fixture requested only by `slow` tests, so `-m "not slow"` genuinely skips it while
the default run still executes it; the session case lists the three `v` sources and *ardmhaor*
verifies.

---

## Known risks

- **Candidate blow-up in Georgian.** Georgian's `[substitute]` collapses broad/slender on every
  labial, coronal and dorsal, so *every* Georgian consonant slot has at least two Irish sources
  before fallback and identity are added — and the fallback maps most of the Irish inventory onto a
  handful of Georgian segments. A three-consonant pattern with two `*` slots is already past the
  2000 cap. Consequences: Georgian's round-trip `example` rate will be the lowest of the four and
  its `capped` count the highest — expected, and why spec §6 excludes capped rows; and `verify` on
  a wildcard-heavy pattern spends most of its budget inside `run_entry`. F8's de-duplication and
  the "skip a candidate whose `spell()` is empty" rule are the sanctioned speed-ups; R4 fixed the
  cap at 2000 and it stays there.
- **Task 9's runtime is the plan's biggest schedule risk.** F9 moved the ratchet from `cap=200` to
  `cap=2000` — a 10× budget over 145 rows × 4 strands, each candidate costing a `g2p` call plus a
  full `run_entry`. Time it in Task 7 before Task 9 starts. If the four strands take more than a
  few minutes, the honest responses are the `slow` marker (planned) and better pruning inside
  `verify`, not a smaller cap or a smaller row set.
- **The registry has to be kept in step with `g2p.py`.** V-27 transcribes procedural branches by
  hand; nothing in the type system links them. A future change to `_liquid` or the Connacht
  post-pass will silently shrink `spell`'s reach. The `g2p_inverse` ratchet is the tripwire, and the
  `g2p.py` docstring paragraph added in Task 1 is the notice — both are load-bearing.
- **Contexts are not evaluated at inversion time (R2).** Every source is offered as if its rule
  always fires, and V-10 additionally offers the *un*-rewritten reading of every context-bearing
  rule. The constraint set therefore over-states what is possible, and only the forward run in
  `verify` prunes it. V-28's order guard removes one class of impossible sources (backwards chains);
  nothing removes the rest. A run with `--examples 0` makes claims that nothing has checked, and the
  report's wording should keep saying so — the spec calls the tool "approximate, over-generating,
  allowed to miss".
- **Respell deletions make some insertions unreachable (V-30 accepted miss).** A `[respell]` rule
  that prints nothing — `arabic-egy.rules`' `ʔ -> "" / # _` is the only current one — erases the
  slot an optional group would have started on, so `arabic-egy`'s prothetic `ʔ i` can never be
  offered from a real pattern. Inverting a respell deletion means guessing where an unprinted
  segment sat, which is the unbounded problem R3 already refuses for phonological deletions, so v1
  records the miss (an `invert_respell` note, and the `possibly dropped` block) rather than guessing.
  If Cairene `sC`-initial words turn out to matter to the owner, the follow-up is a bounded
  "insert at most one respell-deleted segment at a word edge" rule — a scope change, not a bug fix.
- **Deletions.** `X -> 0` is unbounded, so R3 never expands it, and a target word that arises *only*
  because something was deleted (Welsh `h -> 0 / _ #`, `w -> 0 / {ʊ uː} _`) will never appear among
  the verified examples. The user sees the `possibly dropped` block and nothing more. This is a
  known miss, not a bug, and the most likely single cause of a low `example` rate for Welsh.
- **The reverse g2p inherits `g2p`'s errors.** `g2p`'s exact rate on the attested rows is 0.7327
  (`tests/ratchets/g2p.json`). `spell`'s `g2p()` check means a *wrong* spelling is never proposed,
  but a *missing* one is common: any word whose spelling `g2p` misreads is unreachable from its own
  IPA. The `g2p_inverse` ratchet measures exactly this.
- **`_EXPAND_CAP = 64` silently truncates.** A rule with a wide class target and three items could
  exceed 64 expansions; the truncation is recorded as a note, but notes are only printed where a
  slot carries them. Worth a follow-up `strands check` code if it ever bites.
