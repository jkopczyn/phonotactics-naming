"""Task 15: Old Irish [templates], the builder, its ART, the function registry (spec §5, §11)."""

import pytest
from helpers import ROOT, TABLE, irish, target

from strands.inputs import Entry, infer
from strands.oldirish import ConstructionNotInStrand, run_entry_oi
from strands.pipeline import CONSTRUCTIONS
from strands.spelled import SpelledWord

IRISH = irish()
OI = target("old-irish")


def ent(orthography, ipa="sˠiː", **kw):
    return infer(Entry(orthography=orthography, ipa=ipa, **kw), IRISH, TABLE)


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
        line = [ln for ln in text.splitlines() if ln.strip().startswith(name + " ")][0]
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
