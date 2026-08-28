"""Task 6: the constraint set and the report format (reverse spec §4; V-7, V-13 … V-15,
V-31, V-32). The golden tests are the layout contract (F6)."""
import pytest

from helpers import TABLE, irish, target
from strands.reverse import (FORWARD_STAGES, RULE_COL, Example, _id_order, _rule_suffix,
                             constraints, dropped_lines, format_rule_line,
                             invert_respell, parse_pattern, render_pattern, report,
                             source_map, un_substitute, widen)

IRISH = irish()
GEO = target("georgian")
WEL = target("welsh")


def _parse(rf, text):
    """V-35: both `invert_respell` values reach the pattern (as in Task 3-5's tests)."""
    chunk_map, notes = invert_respell(rf, TABLE)
    return parse_pattern(text, chunk_map, notes=notes)


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


def test_context_no_longer_splits_a_line():
    """B1 (the owner reverses ruling 4 of the review round): two alternatives that agree on
    kind and description are ONE line however many contexts they carry between them. The `a` of
    *cahal* reaches /a/ through eleven post-stress rules with eleven different environments."""
    cs = constraints(analysed(WEL, "cahal"))
    (line,) = [l for l in cs[1].lines if l.description == "a, ea, ai, eai"]
    assert len(line.contexts) > 1 and len(line.rule_ids) > 4


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


def test_a_two_context_alternative_is_one_line_and_one_exclusion():
    """F4 re-check / V-31, revised by B1: an alternative whose walk crosses two context-bearing
    rules collapses to ONE constraint line (contexts joined), and the exclusions block prints
    only the SUBSTITUTE-stage step — a repair/post-stress/respell environment is noise there."""
    from strands.reverse import Alternative, Pattern, Slot, Step
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
    rest = out[out.index("exclusions") + 1:]
    excl = rest[:rest.index("")]
    assert len(excl) == 1                     # B1: the respell context is noise, and is gone
    assert "substitute:70" in excl[0] and "respell:330" not in "".join(excl)


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
# GOLDEN_SIMPLE       pins: header, target segments, two normal constraint lines at RULE_COL,
#                     the `possibly dropped` block, no exclusions, verification skipped.
# GOLDEN_CONTINUATION pins: B3's vowel-set summary and six-run cap in the description column,
#                     and the _ALT_CAP `…` in the rendering. (The RULE_COL continuation line
#                     itself is pinned by GOLDEN_EXCLUSIONS, whose exclusion line is long.)
# GOLDEN_EXCLUSIONS   pins: the exclusions block, its `(rule context)` suffix on a continuation
#                     line, and the `or, with … inserted` line of V-14.
# GOLDEN_DROPPED      pins: the once-per-word `possibly dropped` block (V-7), substitute
#                     deletions included, and a slot note.
# GOLDEN_EXAMPLES     pins: the examples block — header, columns, flags and a fallback count.
# GOLDEN_SESSION      pins: the whole `ar*v*  [georgian]` block of spec §4.

GOLDEN_SIMPLE = """\
r  [georgian]
target segments: r

constraints
  r   ← rr/n (after c/g/m)/r                                  substitute:96,respell:354
      ← slender n (after c/g/m)/r                             substitute:97,respell:354

possibly dropped
  ɑ   may have been dropped anywhere in this word             post-stress:316
  ɛ   may have been dropped anywhere in this word             post-stress:316

Irish spelling pattern
  (rr|n|r)

verified examples: skipped (--examples 0)
"""

GOLDEN_CONTINUATION = """\
a  [georgian]
target segments: ɑ

constraints
  a   ← á, ái, eá, eái, a, ea, …                              substitute:49,respell:349
      ← a, ea, ai, eai                                        substitute:52,respell:349
      ← any short vowel (unstressed)                          substitute:57,respell:349 %design

possibly dropped
  ɑ   may have been dropped anywhere in this word             post-stress:316
  ɛ   may have been dropped anywhere in this word             post-stress:316

Irish spelling pattern
  (á|ái|eá|eái|a|ea|…)

verified examples: skipped (--examples 0)
"""

GOLDEN_EXCLUSIONS = """\
v  [georgian]
target segments: v

constraints
  v   ← broad bhf/bh/mh/v/w (non-initial)                     substitute:108
      ← slender bhf/bh/mh/v/w                                 substitute:109
      ← broad bhf/bh/mh/v/w                                   substitute:107 %design
      ← /v/ + /v/                                             substitute:129 %design
      ← inserted, no Irish letter                             substitute:65 %design

possibly dropped
  ɑ   may have been dropped anywhere in this word             post-stress:316
  ɛ   may have been dropped anywhere in this word             post-stress:316

exclusions
  v ← inserted, no Irish letter: only when  [BROAD -labial] _ [V +front]
                                                              (substitute:65 context)

Irish spelling pattern
  (bhf|bh|mh|v|w)
  or, with v inserted:  (nothing)   (context: [BROAD -labial] _ [V +front])

verified examples: skipped (--examples 0)
"""

GOLDEN_DROPPED = """\
uu  [welsh]
target segments: u u

constraints
  u   unconstrained
      note: no Irish source for 'u'
  u   unconstrained
      note: no Irish source for 'u'

possibly dropped
  h   may have been dropped anywhere in this word             repair:280 %design
  h   may have been dropped anywhere in this word             repair:282 %design
  ɡ   may have been dropped anywhere in this word             repair:293 %design
  l   may have been dropped anywhere in this word             repair:308
  r   may have been dropped anywhere in this word             repair:308
  w   may have been dropped anywhere in this word             substitute:161
  w   may have been dropped anywhere in this word             substitute:162
  j   may have been dropped anywhere in this word             substitute:163
  j   may have been dropped anywhere in this word             substitute:164

Irish spelling pattern
  ??

verified examples: skipped (--examples 0)
"""

GOLDEN_EXAMPLES = """\
r  [georgian]
target segments: r

constraints
  r   ← rr/n (after c/g/m)/r                                  substitute:96,respell:354
      ← slender n (after c/g/m)/r                             substitute:97,respell:354

possibly dropped
  ɑ   may have been dropped anywhere in this word             post-stress:316
  ɛ   may have been dropped anywhere in this word             post-stress:316

Irish spelling pattern
  (rr|n|r)

verified examples (2 of 40 candidates tried; 0 fallbacks unless shown)
  ardmhaor   ardvar   ɑrdvɑr
  arv        arv      ɑrv  UNATTESTED_CLUSTER:rv  fallbacks:1
"""

GOLDEN_SESSION = """\
ar*v*  [georgian]
target segments: ɑ r * v *

constraints
  a   ← á, ái, eá, eái, a, ea, …                              substitute:49,respell:349
      ← a, ea, ai, eai                                        substitute:52,respell:349
      ← any short vowel (unstressed)                          substitute:57,respell:349 %design
  r   ← rr/n (after c/g/m)/r                                  substitute:96,respell:354
      ← slender n (after c/g/m)/r                             substitute:97,respell:354
  *   unconstrained
  v   ← broad bhf/bh/mh/v/w (non-initial)                     substitute:108
      ← slender bhf/bh/mh/v/w                                 substitute:109
      ← broad bhf/bh/mh/v/w                                   substitute:107 %design
      ← /v/ + /v/                                             substitute:129 %design
      ← inserted, no Irish letter                             substitute:65 %design
  *   unconstrained

possibly dropped
  ɑ   may have been dropped anywhere in this word             post-stress:316
  ɛ   may have been dropped anywhere in this word             post-stress:316

exclusions
  v ← inserted, no Irish letter: only when  [BROAD -labial] _ [V +front]
                                                              (substitute:65 context)

Irish spelling pattern
  (á|eá|a|ea|io|iu|…)(rr|n|r)*(bhf|bh|mh|v|w)*
  or, with v inserted:  (á|eá|a|ea|io|iu|…)(rr|n|r)**   (context: [BROAD -labial] _ [V +front])

verified examples: skipped (--examples 0)
"""


EXAMPLES = (
    Example("ardmhaor", "ardvar", "ɑrdvɑr", (), 0, 0, 0),
    Example("arv", "arv", "ɑrv", ("UNATTESTED_CLUSTER:rv",), 1, 2, 1),
)


@pytest.mark.parametrize("golden,text,rf,kwargs", [
    (GOLDEN_SIMPLE, "r", GEO, {"verified": False}),
    (GOLDEN_CONTINUATION, "a", GEO, {"verified": False}),
    (GOLDEN_EXCLUSIONS, "v", GEO, {"verified": False}),
    (GOLDEN_DROPPED, "uu", WEL, {"verified": False}),
    (GOLDEN_EXAMPLES, "r", GEO, {"examples": EXAMPLES, "tried": 40}),
    (GOLDEN_SESSION, "ar*v*", GEO, {"verified": False}),
])
def test_the_report_matches_its_golden(golden, text, rf, kwargs):
    assert "\n".join(lines(rf, text, **kwargs)) + "\n" == golden


# ---- task 6 review fixes -------------------------------------------------------------------------

DUT = target("dutch")
ARA = target("arabic-egy")


@pytest.mark.parametrize("rf,text", [(WEL, "i"), (WEL, "w"), (DUT, "e"), (DUT, "o")])
def test_a_real_strand_letter_whose_source_is_an_unregistered_vowel_run_reports(rf, text):
    """These reach `Alternative.segments` such as ('ɪ', 'ə'), which had no `VOWEL_READINGS`
    row and sent `describe()` into infinite recursion."""
    out = lines(rf, text, verified=False)
    assert out[0].startswith(f"{text}  [")
    assert "constraints" in out


@pytest.mark.parametrize("rf,text,want", [
    (WEL, "g", "k|ɡ"),
    (DUT, "a", "aː|ɑ|a"),
    (ARA, "ʼ", "ʔ|ʕ"),
])
def test_an_ambiguous_chunk_keeps_every_target_alternative(rf, text, want):
    """Spec §3.1 / V-1: ambiguity is kept, not resolved to the first-listed source."""
    (constraint,) = constraints(analysed(rf, text))
    assert constraint.target == want
    assert lines(rf, text, verified=False)[1] == f"target segments: {want}"


# ---- fix round Task B: report noise (B1 … B4) --------------------------------------------------

def test_the_a_slot_of_cahal_prints_at_most_four_lines():
    """B1's acceptance: the `a` of *cahal* printed ~40 lines that all said "a/á"."""
    cs = constraints(analysed(WEL, "cahal"))
    assert len(cs[1].lines) <= 4, [l.description for l in cs[1].lines]


def test_a_line_prints_at_most_four_rule_ids_then_a_count():
    """B1: the union of a group's rule ids can be twenty; four and `+N` is what is printed."""
    cs = constraints(analysed(WEL, "cahal"))
    (line,) = [l for l in cs[1].lines if l.description == "a, ea, ai, eai"]
    suffix = _rule_suffix(line)
    ids, _, rest = suffix.partition(" +")
    assert len(ids.split(",")) == 4
    printed = [r for r in line.rule_ids if r not in ("identity", "fallback")]
    assert int(rest) == len(printed) - 4


def test_rule_ids_are_ordered_by_forward_stage_then_line():
    """B1: substitute, repair, post-stress, respell — then line number within a stage."""
    cs = constraints(analysed(WEL, "cahal"))
    for line in cs[1].lines:
        order = [_id_order(r) for r in line.rule_ids]
        assert order == sorted(order), line.rule_ids
        assert FORWARD_STAGES.index("substitute") == 0


def test_the_v_slot_of_the_session_case_prints_its_sources_once_each():
    """B1's acceptance: one line per Irish source of the Georgian ⟨v⟩ — the broad /w/ and
    /vˠ/ readings, the slender one, the inserted one, and `v v -> v`."""
    cs = constraints(analysed(GEO, "ar*v*"))
    assert [l.description for l in cs[3].lines] == [
        "broad bhf/bh/mh/v/w (non-initial)",     # vˠ -> v, the Connacht reading of ⟨bh mh⟩
        "slender bhf/bh/mh/v/w",                 # vʲ -> v
        "broad bhf/bh/mh/v/w",                   # w -> v %design
        "/v/ + /v/",                             # v v -> v %design
        "inserted, no Irish letter",             # 0 -> v %design
    ]


def test_only_substitute_and_epenthesis_contexts_reach_the_exclusions():
    """B1: *cahal* printed twenty-odd exclusion lines, every one of them a post-stress
    environment. Only the `[substitute]` steps and the epenthesis sources are left."""
    out = lines(WEL, "cahal", verified=False)
    excl = out[out.index("exclusions") + 1:out.index("Irish spelling pattern") - 1]
    assert excl and not any("post-stress:" in l or "respell:" in l for l in excl)


def test_the_exclusions_dedupe_by_label_and_context():
    out = lines(WEL, "cahal", verified=False)
    excl = [l for l in out[out.index("exclusions") + 1:out.index("Irish spelling pattern") - 1]
            if l.startswith("  ")]
    assert len(excl) == len(set(excl))
    assert len(excl) <= 6


def test_the_pattern_shows_no_vowel_plus_h_run():
    """B2: ⟨adh eadh agh …⟩ are silent-letter readings and leave the rendering too."""
    for line in render_pattern(analysed(GEO, "ar*v*")):
        assert "adh" not in line and "agh" not in line


def test_a_schwa_slot_says_any_short_vowel():
    """B3: the /ə/ line of the Welsh `a` slot, which listed twenty-three runs."""
    cs = constraints(analysed(WEL, "cahal"))
    assert "any short vowel (unstressed)" in [l.description for l in cs[1].lines]
