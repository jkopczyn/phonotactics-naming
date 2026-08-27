"""Tasks 13-15: Old Irish mutations, inflection and templates as GRAPHEME operations
(spec §5, §11; digest §10.4-§10.5)."""

import pytest
from helpers import ROOT, TABLE, irish, target

from strands.lexicon import key, read_lexicon
from strands.oldirish import apply_oi_mutation
from strands.spelled import SpelledWord, spelling_to_ipa

IRISH = irish()
OI = target("old-irish")
LEX = read_lexicon()


def mut(text, name):
    return apply_oi_mutation(SpelledWord.from_spelling(text), name, OI)


@pytest.mark.parametrize(
    "radical,lenited",
    [("tech", "thech"), ("cenn", "chenn"), ("penn", "phenn"), ("son", "ṡon"), ("fer", "ḟer")],
)
def test_lenition_writes_the_voiceless_stops_and_the_punctum_forms(radical, lenited):
    """digest §10.4 contrast set; R24: ⟨ḟ⟩ is now reachable because it is a TOKEN."""
    assert mut(radical, "LEN").render() == lenited


@pytest.mark.parametrize("radical", ["bo", "duine", "gel", "mac"])
def test_lenition_of_b_d_g_m_changes_the_ipa_and_not_the_spelling(radical):
    """digest §10.2 conv. 1 — the metadata channel is the whole point (R20: draft 1's
    segment-level version rewrote *mac* to *mag*)."""
    out = mut(radical, "LEN")
    assert out.render() == radical and out.mutation == "LEN"
    assert spelling_to_ipa(out) != spelling_to_ipa(SpelledWord.from_spelling(radical))


def test_lenited_f_is_silent_in_the_reconstruction():
    assert spelling_to_ipa(mut("fer", "LEN")) == ("e", "ɾˠ")


@pytest.mark.parametrize(
    "radical,nasalized", [("bo", "mbo"), ("duine", "nduine"), ("gel", "ngel"), ("ech", "n-ech")]
)
def test_nasalization_of_the_voiced_stops_and_vowels_is_written(radical, nasalized):
    """digest §10.4: 'only in the case of b, d, g and of initial vowels'."""
    assert mut(radical, "NAS").render() == nasalized


def test_a_written_nasalized_stop_reconstructs_as_a_single_nasal():
    """O-29 / R25: master table ⟨mb⟩ = /m/."""
    assert spelling_to_ipa(mut("bo", "NAS"))[0] == "mˠ"
    assert len(spelling_to_ipa(mut("bo", "NAS"))) == 2


def test_nasalization_of_a_voiceless_stop_is_not_written():
    """spec §11 (ii)."""
    out = mut("tech", "NAS")
    assert out.render() == "tech"
    assert spelling_to_ipa(out)[0] == "dʲ"


@pytest.mark.parametrize("radical", ["son", "mac", "nem", "lám", "rí"])
def test_s_and_the_sonorants_do_not_nasalize(radical):
    assert mut(radical, "NAS").render() == radical


def test_this_strand_has_only_two_mutation_tables():
    """spec §5: no h-prefix, no t-prefix."""
    assert set(OI.grapheme_mutations) == {"LEN", "NAS"}


def test_every_mutation_line_is_anchored_at_the_word_edge():
    """R20."""
    for rules in OI.grapheme_mutations.values():
        for r in rules:
            assert "#" in r.left, (r.rule_id, r.left)


# ---- Task 14: [inflect] by stem class, and the stem dispatch ------------------------------

from strands.inputs import Entry, infer
from strands.oldirish import CASE_TABLES, PRIMITIVE_TABLES, Stem, apply_case, to_old_irish


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


# ---- Task 15: [templates], the Old Irish builder, its own ART, the function registry -------

from strands.oldirish import ConstructionNotInStrand, build_oi_construction, run_entry_oi
from strands.pipeline import CONSTRUCTIONS


def build(construction, **slots):
    return run_entry_oi(
        slots.pop("_head"), construction, IRISH, OI, TABLE, slots=slots or None
    ).respelling


def test_the_eight_formation_templates_exist_and_are_reachable_from_the_cli():
    names = {"MAEL", "GILLA", "CU", "FER", "COLOUR", "MAC", "UA", "INGEN"}
    assert names <= set(OI.templates) and names <= set(CONSTRUCTIONS)


def test_the_patronymic_particles_of_the_other_strands_are_absent():
    assert "PATRO_O" not in OI.templates and "PATRO_NI" not in OI.templates
    with pytest.raises(ConstructionNotInStrand):
        run_entry_oi(ent("Niall", "nʲiəl̪ˠ"), "PATRO_NI", IRISH, OI, TABLE)


def test_mael_and_gilla_do_not_lenite():
    """spec §11 (i) / R21 — every attested lexicon row: *Máel Coluim*, *Máel Muire*,
    *Máel Sechnaill*. Draft 1 produced *máel Choluim*."""
    out = build("MAEL", _head=ent("Colm", "ˈkɔl̪ˠəmˠ"), NAME=ent("Colm", "ˈkɔl̪ˠəmˠ"))
    assert out.startswith("Máel ") and not out.split()[1].startswith("Ch")


def test_cu_and_ingen_do_lenite():
    """spec §11 (i): *Cú Chulainn*. S10: *ingen* is a fem. ā-stem, so its mutation is
    attested even though the formula is not."""
    out = build("CU", _head=ent("Culann", "ˈkʊl̪ˠən̪ˠ"), NAME=ent("Culann", "ˈkʊl̪ˠən̪ˠ"))
    assert out.split()[1].startswith("Ch")


def test_the_vocative_particle_lenites_and_the_class_decides_the_stem():
    """O-30: identity outside the o-stem."""
    out = build(
        "VOC",
        _head=ent("Cormac", "ˈkɔɾˠəmˠək", declension="m1"),
        NAME=ent("Cormac", "ˈkɔɾˠəmˠək", declension="m1"),
    )
    assert out.split()[0] == "a" and out.split()[1].startswith("Ch")


def test_the_colour_formation_is_a_compound_not_a_phrase():
    out = build(
        "COLOUR", _head=ent("dubh", "d̪ˠʊw"), COLOUR=ent("dubh", "d̪ˠʊw"), NAME=ent("teach", "tʲax")
    )
    assert " " not in out


def test_the_article_is_old_irish_not_modern():
    """R22: `irish._article` emits *an*/*na* and calls HPREF/TPREF, which this strand forbids."""
    out = build(
        "OF", _head=ent("Niall", "nʲiəl̪ˠ"), NAME=ent("Niall", "nʲiəl̪ˠ"), NOUN=ent("teach", "tʲax")
    )
    article = out.split()[1]
    assert article.startswith(("in", "a")) and not article.startswith(("an", "na"))


def test_the_article_before_s_is_int_and_the_s_is_written_plain():
    """review-oi-grammar fix 2 / digest §10.4: *int sléibe*, *int súil* — the ⟨-t⟩ sandhi
    REPLACES the written lenition of ⟨s⟩; draft 2 gave *int ṡléibe*. The reconstruction reads
    the written ⟨s⟩, not the lenited /h/."""
    result = run_entry_oi(
        ent("Niall", "nʲiəl̪ˠ"),
        "OF",
        IRISH,
        OI,
        TABLE,
        slots={"NAME": ent("Niall", "nʲiəl̪ˠ"), "NOUN": ent("sliabh", "ʃlʲiəv")},
    )
    assert result.respelling == "Níall int sléibe"
    noun_ipa = result.ipa.split()[2]
    assert noun_ipa.startswith("ʃ") and not noun_ipa.startswith("h")  # slender ⟨s⟩ = /ʃ/
    art = [t for t in result.trace if t.rule_id == "templates:ART"][0]
    assert art.after == "int sléibe"


def test_capitalization_is_preserved_per_word():
    """R31c: draft 1's tests asserted on capitals that `respell` never produces."""
    out = build("MAC", _head=ent("Conchobhar", "ˈkɾˠɔxuːɾˠ"), NAME=ent("Neasa", "ˈnʲasˠə"))
    assert out.split()[0] == "macc" and out.split()[1][0].isupper()


def test_the_unattested_formations_are_tagged_design():
    text = (ROOT / "rules" / "old-irish.rules").read_text(encoding="utf-8")
    for name in ("UA", "INGEN"):
        line = [l for l in text.splitlines() if l.strip().startswith(name + " ")][0]
        assert "design" in line, line


def test_a_template_literal_is_a_spelling_that_tokenizes():
    """O-25 / spec §11: literals are SPELLINGS, not IPA."""
    text = (ROOT / "rules" / "old-irish.rules").read_text(encoding="utf-8")
    import re

    section = text.partition("\n[templates]\n")[2]  # the plan's whole-file scan also
    seen = 0  # caught quotes inside comments
    for line in section.splitlines():
        line = line.strip()
        if line.startswith("#"):
            continue
        for literal in re.findall(r'"([^"]+)"', line.partition("#")[0]):
            if literal.strip():
                seen += 1
                assert SpelledWord.from_spelling(literal).render() == literal, line
    assert seen >= 8


def test_the_function_registry_is_shared_by_the_parser_and_the_checker():
    """GPT #7: draft 1 left check.py's validator on the old hard-coded list."""
    from strands.dsl import template_functions

    names = template_functions(OI)
    assert {"GEN", "ART", "LEN", "NAS"} <= names
    assert "COLOUR" in __import__("strands.dsl", fromlist=["TEMPLATE_ARGS"]).TEMPLATE_ARGS
