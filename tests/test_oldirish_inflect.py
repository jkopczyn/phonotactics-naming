"""Task 14: Old Irish [inflect] by stem class and the stem dispatch (spec §5, §11; digest §10.5)."""

import pytest
from helpers import TABLE, irish, target

from strands.inputs import Entry, infer
from strands.lexicon import key, read_lexicon
from strands.oldirish import (
    CASE_TABLES,
    PRIMITIVE_TABLES,
    Stem,
    apply_case,
    build_oi_construction,
    to_old_irish,
)
from strands.spelled import SpelledWord

IRISH = irish()
OI = target("old-irish")
LEX = read_lexicon()


def ent(orthography, ipa="sˠiː", **kw):
    return infer(Entry(orthography=orthography, ipa=ipa, **kw), IRISH, TABLE)


def infl(text, table_name):
    from strands.spelled import apply_grapheme_table

    return apply_grapheme_table(
        SpelledWord.from_spelling(text), OI.grapheme_inflect[table_name], simultaneous=False
    ).render()


@pytest.mark.parametrize(
    "table_name,nom,gen",
    [
        ("GEN_O", "fer", "fir"),
        ("GEN_O", "claideb", "claidib"),
        ("GEN_O", "ball", "baill"),
        ("GEN_O", "céile", "céili"),
        ("GEN_O", "daltae", "daltai"),
        ("GEN_O", "cellach", "cellaig"),
        ("GEN_A", "túath", "túaithe"),
        ("GEN_A", "cloch", "cloiche"),
        ("GEN_A", "guide", "guide"),
        ("GEN_A", "rígain", "rígnae"),
        ("GEN_A", "Brigit", "Brigte"),
        ("GEN_I", "cnáim", "cnámo"),
        ("GEN_I", "súil", "súlo"),
        ("GEN_U", "guth", "gotho"),
        ("GEN_N", "brithem", "brithemon"),
        ("GEN_N", "Ériu", "Érenn"),
        ("GEN_N", "ainmm", "anmae"),
        ("GEN_DENT", "carae", "carat"),
        ("GEN_DENT", "fili", "filed"),
        ("GEN_DENT", "Núadu", "Núadat"),
        ("GEN_VELAR", "rí", "ríg"),
        ("GEN_VELAR", "Lugaid", "Luigdech"),
        ("GEN_VELAR", "Echu", "Echach"),
        ("GEN_R", "athair", "athar"),
        ("GEN_R", "máthair", "máthar"),
        ("GEN_S", "nem", "nime"),
        ("GEN_S", "slíab", "sléibe"),
    ],
)
def test_each_stem_class_derives_its_attested_genitive(table_name, nom, gen):
    """digest §10.5 [strachan1909 pp.2-16; pokorny1914 pp.59-70]. Hand-run: 44/49 on the
    stratified subset, 135/163 over every attested genitive in the lexicon."""
    assert infl(nom, table_name) == gen


def test_the_derivation_rate_over_the_whole_lexicon_does_not_regress():
    """The real acceptance metric. Measured 135/163; the floor allows for Task 3 edits."""
    from strands.lexicon import FORM_STATUSES

    rows = [
        r
        for r in LEX.values()
        if r.status in FORM_STATUSES
        and r.oi_gen
        and r.stem
        and r.stem not in ("irregular", "indecl")
    ]
    table_for = {stem: name for (case, stem), name in CASE_TABLES.items() if case == "gen"}
    ok = sum(
        1 for r in rows if r.stem in table_for and infl(r.oi_nom, table_for[r.stem]) == r.oi_gen
    )
    assert ok / len(rows) >= 0.78, (ok, len(rows))


def test_the_o_stem_vocative_is_the_genitive_form_and_every_other_class_is_identity():
    """O-30 / R23: digest §10.5 [pokorny1914 p.65 §142]. Draft 1 gave *a Brigte*."""
    o = Stem(
        words=(SpelledWord.from_spelling("fer"),),
        gen=None,
        stem="o",
        gender="m",
        flag="ATTESTED",
        assumptions=(),
        trace=(),
    )
    a = Stem(
        words=(SpelledWord.from_spelling("túath"),),
        gen=None,
        stem="ā",
        gender="f",
        flag="ATTESTED",
        assumptions=(),
        trace=(),
    )
    assert apply_case(o, "voc", OI)[0].render() == "fir"
    assert apply_case(a, "voc", OI)[0].render() == "túath"


def test_an_attested_genitive_is_never_re_derived():
    """Precedence rule 1: the lexicon is authoritative. The n-stem suffix vowel and the
    u-stem -o/-a are lexical in Old Irish and cannot be derived from spelling."""
    row = LEX[key("Éire")]
    stem = to_old_irish(ent("Éire", "ˈeːɾʲə"), LEX, OI, IRISH, TABLE)
    assert apply_case(stem, "gen", OI)[0].render() == row.oi_gen


def test_an_indeclinable_stem_is_returned_unchanged():
    """digest §10.5; R31b: *Patraic* must be `indecl` or GILLA derives a genitive for it."""
    s = Stem(
        words=(SpelledWord.from_spelling("Patraic"),),
        gen=None,
        stem="indecl",
        gender="m",
        flag="ATTESTED",
        assumptions=(),
        trace=(),
    )
    assert apply_case(s, "gen", OI)[0].render() == "Patraic"


def test_the_ending_marker_is_realized_by_stem_class():
    """spec §11 / GPT #8: the retro-filter leaves it unresolved and [inflect] resolves it."""
    a = Stem(
        words=(SpelledWord.from_spelling("carə"),),
        gen=None,
        stem="ā",
        gender="f",
        flag="RETRO",
        assumptions=(),
        trace=(),
    )
    o = Stem(
        words=(SpelledWord.from_spelling("carə"),),
        gen=None,
        stem="o",
        gender="m",
        flag="RETRO",
        assumptions=(),
        trace=(),
    )
    assert apply_case(a, "nom", OI)[0].render() == "care"
    assert apply_case(o, "nom", OI)[0].render() == "cara"


def test_the_ending_marker_is_realized_for_an_indeclinable_stem_too():
    """spec §11: "*-e* for ā-stems, *-a* otherwise" — an inert class skips the case tables
    but not the marker. Exposed by review-oi-grammar fix 1: a RETRO vowel-final word infers
    `d4` -> `indecl`, and *an tsneachta* rendered as ⟨ə trechttə⟩."""
    s = Stem(
        words=(SpelledWord.from_spelling("carə"),),
        gen=None,
        stem="indecl",
        gender="m",
        flag="RETRO",
        assumptions=(),
        trace=(),
    )
    out = build_oi_construction("DESC", {"NOUN": s}, OI, TABLE)
    assert out[0].render() == "cara"


def test_an_unknown_stem_class_falls_back_to_the_o_stem_with_a_note():
    s = Stem(
        words=(SpelledWord.from_spelling("fer"),),
        gen=None,
        stem="",
        gender="m",
        flag="RETRO",
        assumptions=(),
        trace=(),
    )
    trace = []
    out = apply_case(s, "gen", OI, trace=trace)
    assert out[0].render() == "fir"
    assert any("gen-fallback-o" in t.note for t in trace)


def test_the_case_table_map_covers_every_stem_value_that_has_a_paradigm():
    from strands.lexicon import STEMS

    assert {s for (c, s) in CASE_TABLES if c == "gen"} == set(STEMS) - {"indecl", "irregular"}


def test_the_dative_is_identity_for_both_declensions():
    """digest §10.4: the leniting mutation is the template's; the written form is unchanged."""
    o = Stem(
        words=(SpelledWord.from_spelling("fer"),),
        gen=None,
        stem="o",
        gender="m",
        flag="ATTESTED",
        assumptions=(),
        trace=(),
    )
    a = Stem(
        words=(SpelledWord.from_spelling("túath"),),
        gen=None,
        stem="ā",
        gender="f",
        flag="ATTESTED",
        assumptions=(),
        trace=(),
    )
    assert apply_case(o, "dat", OI)[0].render() == "fer"
    assert apply_case(a, "dat", OI)[0].render() == "túath"


def test_the_shared_primitives_are_copied_verbatim_into_the_tables_that_use_them():
    """The DSL has no table inclusion, so INF (i-infection, digest §10.2 §§36-41) and DEP
    (depalatalization) are declared once as their own sub-tables and copied into the case
    tables; this keeps the copies honest."""

    def shape(rules):
        return [(r.target, r.replacement, r.left, r.right) for r in rules]

    for primitive, users in PRIMITIVE_TABLES.items():
        block = shape(OI.grapheme_inflect[primitive])
        assert block, primitive
        for user in users:
            host = shape(OI.grapheme_inflect[user])
            assert any(host[k : k + len(block)] == block for k in range(len(host))), (
                primitive,
                user,
            )


def test_run_entry_oi_resolves_the_ending_marker_before_rendering():
    """spec §11: 'Tested end-to-end from a modern f2 word'. *Saoirse* is a RETRO:late
    feminine; the filter writes ⟨-ə⟩ and NOM_A realizes it as ⟨-e⟩."""
    from strands.oldirish import run_entry_oi

    result = run_entry_oi(
        ent("Saoirse", "ˈsˠiːɾˠʃə", gender="f", declension="f2"), "DESC", IRISH, OI, TABLE
    )
    assert "ə" not in result.respelling and result.respelling.endswith("e")


def test_check_reports_a_grapheme_rule_token_outside_the_grapheme_table():
    """Task 14 step 5: GRAPHEME_UNKNOWN_TOKEN is an error."""
    from dataclasses import replace

    from strands.check import check_rule_file
    from strands.spelled import GraphemeRule

    bad = GraphemeRule(
        table="GEN_O",
        line=7,
        rule_id="inflect:7",
        target=("zz",),
        replacement=("a", "qq"),
        left=("#",),
        right=(),
        tag="design",
        comment="",
    )
    rf = replace(OI, grapheme_inflect={"GEN_O": (bad,)})
    codes = [
        (e.code, e.line, e.severity)
        for e in check_rule_file(rf, TABLE)
        if e.code == "GRAPHEME_UNKNOWN_TOKEN"
    ]
    assert codes == [("GRAPHEME_UNKNOWN_TOKEN", 7, "error")] * 2
    assert not [e for e in check_rule_file(OI, TABLE) if e.code == "GRAPHEME_UNKNOWN_TOKEN"]
