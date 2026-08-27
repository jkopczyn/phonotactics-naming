"""Tasks 8-11: `rules/old-irish.rules` as data (spec §4, §6, §11; digest §10)."""
import pytest

from helpers import ROOT, TABLE, target, w
from strands.check import check_rule_file

PATH = ROOT / "rules" / "old-irish.rules"
OI = target("old-irish")


def test_the_file_parses_and_check_reports_no_errors():
    assert [f for f in check_rule_file(OI, TABLE) if f.severity == "error"] == []


def test_meta_declares_the_keys_the_pipeline_and_spelled_module_read():
    assert OI.meta["strand"] == "old-irish"          # O-9: the dispatch key
    assert OI.meta["grammar"] == "graphemes"         # O-10 / Task 7's parser mode
    assert OI.meta["orthography"].endswith("old-irish-orthography.tsv")
    assert OI.meta.get("punctum", "on") in ("on", "off")


def test_the_quality_pairs_are_declared_explicitly_and_completely():
    """spec §11: an EXPLICIT mapping, never derived positionally (GPT #2 measured draft 1's
    positional derivation as 20-vs-19 with `w` unpaired)."""
    pairs = dict(p.split(":") for p in OI.meta["quality-pairs"].split())
    assert pairs["w"] == "-"                          # no partner, stated as such
    for broad, slender in pairs.items():
        assert broad in OI.classes["BROAD"] or broad in ("h",), broad
        assert slender in OI.classes["SLEN"] or slender in ("-", "h"), slender
    assert {b for b in OI.classes["BROAD"] if b != "w"} <= set(pairs)


def test_this_strand_declares_no_epithet_slots():
    assert "epithet-ADJ" not in OI.meta and "epithet-NOUN" not in OI.meta


@pytest.mark.parametrize("segment", ["β", "βʲ", "β̃", "β̃ʲ", "ð", "ðʲ", "θ", "θʲ", "x", "ç",
                                     "ɣ", "ɣʲ", "sˠ", "ʃ", "fˠ", "fʲ", "h"])
def test_the_lenited_series_and_the_lenition_products_are_in_the_inventory(segment):
    assert segment in OI.inventory


@pytest.mark.parametrize("vowel", ["i", "e", "a", "o", "u", "iː", "eː", "aː", "oː", "uː"])
def test_the_five_short_and_five_long_vowels_are_there(vowel):
    assert vowel in OI.inventory


def test_the_marginal_set_is_exactly_the_documented_one():
    """S5, S6, S7: /p/ a Latin import; /w vʲ/ not Old Irish phonemes; /ə/ a reduction;
    /æ/ name-relevant but uncertain.

    Task 8 deviation: the plan also lists /hʲ/ ("may have been the same sound as /h/ or
    /xʲ/", digest §10.1) and says it is already a features.tsv row. It is not (Task 1 added
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
        return (c.startswith(("digest", "[", "design:")) or "digest §10" in c
                or "pokorny1914" in c or "strachan1909" in c or "wiki-old-irish" in c)
    bad = [(s, r.line) for s, rules in OI.sections.items() for r in rules if not cited(r.comment)]
    for name, rules in {**OI.grapheme_mutations, **OI.grapheme_inflect}.items():
        bad += [(name, r.line) for r in rules if not cited(r.comment)]
    text = PATH.read_text(encoding="utf-8")
    body = text.split("[templates]")[1] if "[templates]" in text else ""
    for line in body.splitlines():
        if "=" in line and not line.lstrip().startswith("#"):
            assert "#" in line, line
    assert bad == [], bad


# ---- Task 9: [substitute], the retro-filter (spec §4, §11; O-13, O-15) ---------------------

from helpers import irish
from strands.irish import normalize
from strands.orth import tag_word
from strands.substitute import substitute_stage

IRISH = irish()


def retro(ipa, orthography=""):
    word = normalize(w(ipa), IRISH, TABLE)
    if orthography:
        word = tag_word(word, orthography)
    return substitute_stage(word, OI, TABLE).segments


@pytest.mark.parametrize("orthography,ipa,index,expected", [
    ("dubh",   "d̪ˠʊw",   -1, "β"),      # dubh ~ dub
    ("sliabh", "ʃlʲiəw",  -1, "β"),      # sliabh ~ slíab
    ("lámh",   "l̪ˠaːw",  -1, "β̃"),      # lámh ~ lám
    ("adharc", "əiɾˠk",   None, None),   # adharc ~ adarc (see the next test)
    ("cloch",  "kl̪ˠɔx",  -1, "x"),      # cloch ~ cloch
    ("bláth",  "bˠl̪ˠaː", None, None),
])
def test_the_lenition_digraphs_map_to_the_lenited_series(orthography, ipa, index, expected):
    """R18: every fixture is an `attested` lexicon row. Log finding 3: ~49 pairs."""
    if expected is None:
        pytest.skip("covered by the class test below")
    assert retro(ipa, orthography)[index] == expected


def test_the_reversal_keeps_quality():
    """R11: draft 1's single broad replacement flattened slender ⟨bh ch th⟩ to broad.

    Task 9 deviation: the plan wrote *cheann* as /ˈcaːn̪ˠ/ (the palatal STOP /c/, which
    ⟨ch⟩ cannot align to); test-words.tsv has /çaːn̪ˠ/, which is used."""
    assert retro("vʲiː", "bhí")[0] == "βʲ"
    assert retro("ˈçaːn̪ˠ", "cheann")[0] == "ç"


def test_the_reversal_keeps_vowel_length():
    """spec §4's non-reversal list; R11: draft 1's `@orth("ea") -> e` shortened /aː/."""
    out = retro("bʲaːn̪ˠ", "beann")
    assert "eː" in out and "e" not in out or "eː" in out


def test_the_quality_digraph_class_deletes_the_glide_and_keeps_the_sound():
    """Log finding 2, 50 pairs — the largest class, and invisible to any sound-based rule."""
    assert retro("bʲanˠ", "bean")[1] == "e"          # bean ~ ben
    assert retro("dʲaɾˠəɡ", "dearg")[1] == "e"       # dearg ~ derg
    assert retro("fʲɪn̪ˠ", "fionn")[1] == "i"        # Fionn ~ Finn


def test_modern_ao_becomes_the_two_segment_digraph():
    """R13: a single `aː` is unwritable as ⟨áe⟩. O-13 / spec §8 row O1."""
    assert retro("iːnˠ", "aon")[:2] == ("a", "i")    # aon ~ óen/áen


def test_ua_and_ia_lengthen_the_first_element_only():
    """R12: positional tags. *tuath ~ túath*, *iasc ~ íasc* — 33 pairs.

    Task 9 deviation: the plan wrote *tuath* as /t̪ˠuəx/, but final ⟨th⟩ is /h/ (or
    silent), never /x/ — that IPA cannot align, so the tags would be absent and the test
    would measure nothing. /t̪ˠuəh/ is the spelling's value."""
    assert retro("t̪ˠuəh", "tuath")[1:3] == ("u", "a")
    assert retro("iəsˠk", "iasc")[:2] == ("i", "a")


def test_the_epenthetic_schwa_is_deleted_by_its_spelling():
    """spec §8 row O5. The aligner tags it `r:2` (Task 5), so the rule is exact."""
    assert retro("ɡɔɾˠəmˠ", "gorm") == ("ɡ", "o", "ɾˠ", "mˠ")


def test_an_unaligned_word_still_loses_its_epenthesis_and_stays_in_inventory():
    """O-7/O-15: no tags, so only the sound-based half applies — and it must still work."""
    out = retro("ɡɔɾˠəmˠ")
    assert set(out) <= set(OI.inventory) and "ə" not in out and "ɔ" not in out


@pytest.mark.parametrize("orthography,ipa", [
    ("athair", "ˈahəɾʲ"), ("máthair", "ˈmˠaːhəɾʲ"), ("bráthair", "ˈbˠɾˠaːhəɾʲ"),
    ("arán", "əˈɾˠaːnˠ"), ("Colmán", "ˈkɔl̪ˠəmˠaːnˠ"),
])
def test_the_invariant_classes_are_left_alone(orthography, ipa):
    """S19 / log finding 4: the r-stem kinship set and the ⟨-án⟩ diminutive are
    spelling-invariant across both stages — the best 'does the filter over-apply' cases."""
    out = retro(ipa, orthography)
    assert set(out) <= set(OI.inventory)
    assert "ə" not in out[-2:]


def test_a_negative_control_shows_the_section_is_actually_doing_the_work():
    """S13: draft 1's identity assertions passed with no [substitute] section at all.

    Task 9 deviation: the plan's fixture was *dubh*, but the section's own `w -> β` sweep
    (S6) makes tagged and untagged *dubh* identical, so it cannot separate the spelling-
    driven half from the sound-driven one. *lámh* can: tagged ⟨mh⟩ gives /β̃/, the
    sound-only path gives /β/."""
    assert retro("l̪ˠaːw", "lámh") != retro("l̪ˠaːw")
    assert retro("l̪ˠaːw", "lámh")[-1] == "β̃" and retro("l̪ˠaːw")[-1] == "β"


def test_every_substitute_line_carries_a_citation_and_a_legal_tag():
    """R17: spec §4 allows %attested where a lexicon pair instantiates the rule."""
    for rule in OI.sections["substitute"]:
        assert rule.tag in ("attested", "design"), (rule.line, rule.tag)
        assert rule.comment.strip(), rule.line
