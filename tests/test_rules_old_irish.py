"""Tasks 8-11: `rules/old-irish.rules` as data (spec §4, §6, §11; digest §10)."""

import pytest
from helpers import ROOT, TABLE, target

from strands.check import check_rule_file

PATH = ROOT / "rules" / "old-irish.rules"
OI = target("old-irish")


def test_the_file_parses_and_check_reports_no_errors():
    assert [f for f in check_rule_file(OI, TABLE) if f.severity == "error"] == []


def test_meta_declares_the_keys_the_pipeline_and_spelled_module_read():
    assert OI.meta["strand"] == "old-irish"  # O-9: the dispatch key
    assert OI.meta["grammar"] == "graphemes"  # O-10 / Task 7's parser mode
    assert OI.meta["orthography"].endswith("old-irish-orthography.csv")
    assert OI.meta.get("punctum", "on") in ("on", "off")


def test_the_quality_pairs_are_declared_explicitly_and_completely():
    """spec §11: an EXPLICIT mapping, never derived positionally (GPT #2 measured draft 1's
    positional derivation as 20-vs-19 with `w` unpaired)."""
    pairs = dict(p.split(":") for p in OI.meta["quality-pairs"].split())
    assert pairs["w"] == "-"  # no partner, stated as such
    for broad, slender in pairs.items():
        assert broad in OI.classes["BROAD"] or broad in ("h",), broad
        assert slender in OI.classes["SLEN"] or slender in ("-", "h"), slender
    assert {b for b in OI.classes["BROAD"] if b != "w"} <= set(pairs)


def test_this_strand_declares_no_epithet_slots():
    assert "epithet-ADJ" not in OI.meta and "epithet-NOUN" not in OI.meta


@pytest.mark.parametrize(
    "segment",
    ["β", "βʲ", "β̃", "β̃ʲ", "ð", "ðʲ", "θ", "θʲ", "x", "ç", "ɣ", "ɣʲ", "sˠ", "ʃ", "fˠ", "fʲ", "h"],
)
def test_the_lenited_series_and_the_lenition_products_are_in_the_inventory(segment):
    assert segment in OI.inventory


@pytest.mark.parametrize("vowel", ["i", "e", "a", "o", "u", "iː", "eː", "aː", "oː", "uː"])
def test_the_five_short_and_five_long_vowels_are_there(vowel):
    assert vowel in OI.inventory


def test_the_marginal_set_is_exactly_the_documented_one():
    """S5, S6, S7: /p/ a Latin import; /w vʲ/ not Old Irish phonemes; /ə/ a reduction;
    /æ/ name-relevant but uncertain.

    Task 8 deviation: the plan also lists /hʲ/ ("may have been the same sound as /h/ or
    /xʲ/", digest §10.1) and says it is already a features.csv row. It is not (Task 1 added
    only the seven lenited-series rows), and a rule file may not name a segment the table
    lacks, so /hʲ/ is left out until a row exists."""
    assert set(OI.marginal) == {"pˠ", "pʲ", "w", "vʲ", "ə", "æ"}


def test_no_fortis_sonorant_segments_were_invented():
    assert not {"L", "N", "R"} & set(OI.inventory)


def test_the_quality_classes_are_declared_not_derived():
    assert "β" in OI.classes["BROAD"] and "βʲ" in OI.classes["SLEN"]
    assert "k" in OI.classes["BROAD"] and "c" in OI.classes["SLEN"]
    assert set(OI.classes["SONORANT"]) >= {"l̪ˠ", "n̪ˠ", "ɾˠ", "mˠ"}


def test_every_rule_line_everywhere_carries_a_citation():
    """R32: draft 1 iterated only `OI.sections`, so [mutations], [inflect] and [templates]
    — separate RuleFile fields — were entirely unchecked."""

    def cited(comment):
        c = (comment or "").strip()
        return (
            c.startswith(("digest", "[", "design:"))
            or "digest §10" in c
            or "pokorny1914" in c
            or "strachan1909" in c
            or "wiki-old-irish" in c
        )

    bad = [(s, r.line) for s, rules in OI.sections.items() for r in rules if not cited(r.comment)]
    for name, rules in {**OI.grapheme_mutations, **OI.grapheme_inflect}.items():
        bad += [(name, r.line) for r in rules if not cited(r.comment)]
    text = PATH.read_text(encoding="utf-8")
    body = text.split("[templates]")[1] if "[templates]" in text else ""
    for line in body.splitlines():
        if "=" in line and not line.lstrip().startswith("#"):
            assert "#" in line, line
    assert bad == [], bad
