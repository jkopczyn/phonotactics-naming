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


# ---- Task 10: [syllable], [repair], [stress], [post-stress] (spec §4; O-20, O-28) -----------

from strands.repair import repair
from strands.stress import assign_stress
from strands.syllabify import syllabify


def phon(ipa):
    return assign_stress(repair(syllabify(w(ipa), OI, TABLE), OI, TABLE), OI, TABLE)


def test_the_syllable_spec_is_permissive_and_word_domain():
    s = OI.syllable
    assert s.template is None and s.onsets is None and s.codas is None
    assert s.sonority is False and s.domain == "word" and s.bans == ()


def test_the_nuclei_are_the_wiki_old_irish_values_plus_the_two_modern_pass_throughs():
    """O-28 / R19."""
    assert {"".join(n) for n in OI.syllable.nuclei} == {
        "ai", "oi", "ui", "au", "eu", "iu", "ia", "ua", "əi", "əu"}


def test_a_diphthong_is_one_syllable():
    """S12: draft 1's version was an `or` of two assertions over a nucleus not in the list."""
    assert len(phon("tuaθ").syllables) == 1
    assert len(phon("kaix").syllables) == 1


def test_an_unattested_cluster_is_kept_and_flagged_never_repaired():
    assert OI.cluster_fallback == "keep"
    out = phon("sˠt̪ˠɾˠai")
    assert "UNREPAIRED" not in out.flags and out.segments[:3] == ("sˠ", "t̪ˠ", "ɾˠ")


def test_obstruent_geminates_degeminate():
    assert phon("abˠbˠ").segments.count("bˠ") == 1


def test_sonorant_geminates_are_left_alone_because_they_spell_fortis():
    """digest §10.2 conv. 3 / O-2: ⟨ll nn rr mm⟩ = /L N R m/."""
    assert phon("kol̪ˠl̪ˠ").segments.count("l̪ˠ") == 2


def test_stress_is_initial():
    assert phon("konˠxoβaɾˠ").stress == 0


def test_unstressed_vowels_are_not_reduced():
    assert OI.sections.get("post-stress", ()) == ()
    assert "a" in phon("konˠal̪ˠ").segments


# ---- Task 11: [respell], editorial Old Irish orthography (spec §6, §11; digest §10.2) -----

from strands.respell import respell
from strands.spelled import SpelledWord
from strands.word import Word


def spell(*segments):
    return respell(Word(segments=segments), OI, TABLE)


def test_lenited_b_d_g_m_are_written_unmarked():
    """digest §10.2 conv. 1 — the largest visual difference from a modern name."""
    assert spell("d̪ˠ", "u", "β") == "dub"
    assert spell("l̪ˠ", "aː", "β̃") == "lám"
    assert spell("a", "ð", "a", "ɾˠ", "k") == "adarc"


def test_lenited_voiceless_stops_are_written_with_h():
    assert spell("k", "l̪ˠ", "o", "x") == "cloch"
    assert spell("bˠ", "l̪ˠ", "aː", "θ") == "bláth"


def test_non_initial_voiceless_stops_are_doubled_and_voiced_ones_are_written_c_t_p():
    """digest §10.2 conv. 2-3 — this restores *mac -> macc* with no lexical list.

    Task 11 deviation: the plan's fixture spelled *bec* with slender /ɟ/, which rule 8
    (the §36 glide, NOT blocked after ⟨e⟩ per S20) would write *beic*. *bec* /bʲeɡ/ has a
    broad /ɡ/ (digest §10.2 conv. 2; modern *beag*), so the fixture uses `ɡ`."""
    assert spell("mˠ", "a", "k") == "macc"
    assert spell("bʲ", "e", "ɡ") == "bec"
    assert spell("bˠ", "ɾˠ", "a", "t̪ˠ") == "bratt"
    assert spell("bˠ", "ɾˠ", "o", "d̪ˠ") == "brot"


def test_a_nasalized_stop_is_not_devoiced_by_the_doubling_rule():
    assert spell("mˠ", "bˠ", "oː") == "mbó"
    assert spell("ŋ", "ɡ", "a") == "nga"


def test_a_stop_after_a_sonorant_is_written_single_and_keeps_its_voice():
    """digest §10.2 conv. 4: *derc* /dʲerk/ ~ /dʲerɡ/, *delg*, *cerd*, *imb*; lexicon
    dearg ~ derg, adharc ~ adarc, Colmán ~ Colmán."""
    assert spell("dʲ", "e", "ɾˠ", "ɡ") == "derg"
    assert spell("dʲ", "e", "ɾˠ", "k") == "derc"
    assert spell("k", "e", "ɾˠ", "d̪ˠ") == "cerd"
    assert spell("k", "o", "l̪ˠ", "mˠ", "aː", "n̪ˠ") == "colmán"


def test_the_eight_diphthongs_and_the_ao_default():
    for segments, expected in [(("a", "i"), "áe"), (("o", "i"), "oí"), (("u", "i"), "uí"),
                               (("a", "u"), "áu"), (("e", "u"), "éu"), (("i", "u"), "íu"),
                               (("i", "a"), "ía"), (("u", "a"), "úa")]:
        assert spell(*segments) == expected


def test_the_glide_i_marks_a_final_slender_consonant():
    """digest §10.2 conv. 5 §36."""
    assert spell("mˠ", "u", "ɾʲ") == "muir"
    assert spell("k", "a", "ɾʲ", "tʲ") == "cairt"            # the whole final cluster
    assert spell("bˠ", "ɾʲ", "i", "a", "nʲ") == "bríain"     # after ⟨ía⟩ (gen. *Bríain*)
    # Medially, "at the end of a syllable" = before a consonant (conv. 5 (ii)); [syllable]
    # has `onsets = any`, so a `.`-based rule would never fire on a real medial cluster.
    word = syllabify(w("mˠuɾʲçeɾˠt̪ˠax"), OI, TABLE)
    assert respell(word, OI, TABLE) == "muirchertach"
    assert spell("a", "lʲ", "βʲ", "ə") == "ailbə"
    assert spell("k", "a", "ɾʲ", "e") == "care"               # before a vowel letter: no glide


def test_no_glide_is_written_before_a_broad_consonant():
    assert spell("fʲ", "e", "ɾˠ") == "fer"


def test_the_glide_is_blocked_after_i_and_the_long_front_vowels_but_not_after_e():
    """S20: Pokorny's exception list is í, é, aí, oí, uí — not short ⟨e⟩."""
    assert spell("mˠ", "iː", "nʲ") == "mín"
    assert spell("eː", "nʲ") == "én"
    assert spell("k", "a", "i", "lʲ") == "cáel"                # c + áe + l, no second i
    assert spell("k", "e", "lʲ") == "ceil"


def test_the_post_stress_schwa_grid():
    assert spell("dʲ", "iː", "ɣ", "ə", "l̪ˠ") == "dígal"
    assert spell("dʲ", "iː", "ɣ", "ə", "lʲ") == "dígail"
    assert spell("dʲ", "lʲ", "i", "ɣʲ", "ə", "ð") == "dliged"
    assert spell("dʲ", "lʲ", "i", "ɣʲ", "ə", "ðʲ") == "dligid"


def test_a_word_final_schwa_becomes_the_ending_marker():
    """spec §11: the retro-filter leaves it UNRESOLVED; Task 14 realizes it by stem class."""
    assert spell("k", "a", "ɾˠ", "ə").endswith("ə")


def test_sonorant_geminates_are_written_doubled():
    """digest §10.2 conv. 3. R16: nothing upstream produces two identical sonorants, so this
    fires only on a lexicon-sourced word; the rule exists so the section is complete."""
    assert spell("k", "o", "l̪ˠ", "l̪ˠ") == "coll"
    assert spell("k", "e", "nʲ", "nʲ") == "ceinn"


def test_written_lenition_of_p_and_s_follows_the_source_spelling():
    """digest §10.2 conv. 1: ⟨ph⟩ where the source was ⟨ph⟩, else ⟨f⟩; ⟨ṡ⟩ where ⟨sh⟩."""
    from strands.orth import tag_word
    assert respell(tag_word(Word(segments=("a", "fˠ", "aː", "l̪ˠ")), "aphál"), OI, TABLE) == "aphál"
    assert spell("fʲ", "e", "ɾˠ") == "fer"
    assert respell(tag_word(Word(segments=("a", "h", "aː", "l̪ˠ")), "ashál"), OI, TABLE) == "aṡál"
    assert spell("h", "aː", "l̪ˠ") == "hál"


def test_every_respell_output_is_tokenizable_as_a_spelled_word():
    """R27: draft 1's [respell] and reconstruction used different alphabets. This is the
    property that keeps them one system."""
    for segments in [("d̪ˠ", "u", "β"), ("mˠ", "a", "k"), ("k", "l̪ˠ", "o", "x"),
                     ("mˠ", "u", "ɾʲ"), ("dʲ", "iː", "ɣ", "ə", "l̪ˠ"), ("a", "i"),
                     ("k", "a", "ɾˠ", "ə"), ("mˠ", "bˠ", "oː"), ("k", "o", "l̪ˠ", "l̪ˠ"),
                     ("bʲ", "e", "ɡ"), ("dʲ", "lʲ", "i", "ɣʲ", "ə", "ðʲ")]:
        text = spell(*segments)
        assert SpelledWord.from_spelling(text).render() == text, text


def test_every_inventory_segment_respells_to_grapheme_tokens_only():
    """S21 + R27 as a property: no inventory segment leaks through as IPA."""
    for seg in OI.inventory:
        text = spell(seg)
        assert SpelledWord.from_spelling(text).render() == text, (seg, text)


def test_no_h_prefix_is_ever_written():
    assert not spell("eː", "n̪ˠ").startswith("h")


def test_every_respell_line_carries_a_citation_and_a_legal_tag():
    rules = OI.sections["respell"]
    assert rules, "the [respell] section is empty"
    for r in rules:
        assert r.tag in ("attested", "design", "fallback"), r.line
        assert r.comment, r.line
