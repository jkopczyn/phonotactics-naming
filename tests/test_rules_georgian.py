"""Plan Task 23a: `georgian.rules` core — inventory, substitute, stress, epithets, respell.

Stage-level only (plan fix 2): there is no real `[syllable]` until Task 23b, so nothing here
calls `adapt()`, `repair()` or the regression harness. Substitution is tested through
`substitute_stage()`, respelling through `respell()` on hand-built Words, and the epithet
follow-ups (-uli dissimilation, syncope before -eb-) through `post_stress()` on hand-built
affixed Words.
"""

from helpers import TABLE, target, w

from strands.check import check_rule_file
from strands.poststress import post_stress
from strands.respell import respell
from strands.substitute import substitute_stage
from strands.word import Word

TARGET = target("georgian")


def sub(ipa):
    """Stage-level: substitution only. 23a has no real [syllable] yet (fix 2)."""
    return substitute_stage(w(ipa), TARGET, TABLE).segments


def spell(*segments):
    return respell(Word(segments=tuple(segments)), TARGET, TABLE)


# ---- common tests (parse / citation half; the pipeline half lives in Task 23b) -------------


def test_rule_file_parses_and_checks_clean():
    errs = [e for e in check_rule_file(TARGET, TABLE) if e.severity == "error"]
    assert errs == [], errs


def test_every_rule_line_carries_a_citation():
    for section in TARGET.sections.values():
        for r in section:
            assert r.comment.strip(), r.rule_id
            assert "[" in r.comment or "design:" in r.comment or "digest §" in r.comment, (
                r.rule_id,
                r.comment,
            )


def test_tags_are_design_where_the_digest_leaves_the_question_open():
    """I-28/I-29: the plan names these blocks %design; %attested would claim digest support."""
    subs = TARGET.sections["substitute"]
    by_repl = {}
    for r in subs:
        for seg in r.replacement if isinstance(r.replacement, tuple) else ():
            by_repl.setdefault(seg, []).append(r)
    for seg in ("pʰ", "kʼ", "tʃʰ", "dʒ"):
        assert seg in by_repl, seg
    for r in by_repl["kʼ"] + by_repl["tʃʰ"] + by_repl["dʒ"]:
        assert r.tag == "design", (r.rule_id, r.tag)
    f_rules = [
        r
        for r in subs
        if r.target and r.target[0].kind == "segment" and r.target[0].value in ("fˠ", "fʲ", "f")
    ]
    assert f_rules and all(r.tag == "attested" for r in f_rules)


# ---- inventory / classes --------------------------------------------------------------------


def test_inventory_is_the_shosted_chart():
    """digest §1.1 [shosted2006 p.255]: 28 consonants + 5 vowels; tʃʰ from the Task 1b rows."""
    inv = set(TARGET.inventory)
    for seg in "pʰ pʼ b tʰ tʼ d kʰ kʼ ɡ qʼ ts tsʼ dz tʃʰ tʃʼ dʒ m n v s z ʃ ʒ x ɣ h l".split():
        assert seg in inv, seg
    assert {"i", "ɛ", "ɑ", "ɔ", "u"} <= inv
    assert "f" not in inv and "ŋ" not in inv and "w" not in inv  # §1.4, §3.2
    assert not any(s.endswith("ː") for s in inv)  # §4.4


def test_broad_and_slender_are_declared_classes():
    assert TARGET.classes["BROAD"] == tuple("pˠ bˠ t̪ˠ d̪ˠ fˠ sˠ w vˠ mˠ n̪ˠ l̪ˠ ɾˠ k ɡ x ɣ ŋ".split())
    assert TARGET.classes["SLEN"] == tuple("pʲ bʲ tʲ dʲ fʲ ʃ vʲ mʲ nʲ lʲ ɾʲ c ɟ ç j ɲ".split())


def test_syllable_block_is_loadable():
    """Task 23a shipped a TEMPORARY permissive block; Task 23b replaced it wholesale (the
    whitelists are tested in test_rules_georgian_syllable.py). The file must still parse."""
    assert TARGET.syllable is not None
    assert TARGET.syllable.template is None
    assert TARGET.syllable.sonority is False and TARGET.syllable.domain == "stem"


# ---- substitute ---------------------------------------------------------------------------------


def test_irish_p_t_k_are_aspirated_by_default_per_decision_9_4():
    """Named for the decision, not for a digest fact: digest §3.1 line 868 recommends the
    ejective as the UNCONDITIONAL default and line 818 rejects the environment split."""
    assert sub("pˠaː")[0] == "pʰ"


def test_post_consonantal_stops_are_ejective_per_decision_9_4():
    assert "kʼ" in sub("sˠkaː")


def test_f_becomes_aspirated_p():
    assert "pʰ" in sub("fˠaː")


def test_f_stays_aspirated_after_a_consonant():
    """digest §3.1 contrast preservation (Apridonidze): f -> pʰ, p -> pʼ, never merged."""
    assert sub("sˠfˠaː") == ("s", "pʰ", "ɑ")


def test_broad_nonlabial_before_a_front_vowel_gets_v():  # Cʷ, decision 5
    assert sub("kiː")[1] == "v"


def test_the_cw_rule_uses_the_BROAD_class():
    """Spec §12.J: `[C +back]` would exclude plain /k/, the very segment this targets."""
    rule = [r for r in TARGET.sections["substitute"] if r.replacement == ("v",) and r.target == ()][
        0
    ]
    assert rule.left[-1].atom.value.class_name == "BROAD"


def test_broad_labials_do_not_get_v():
    assert "v" not in sub("bˠiː") and "v" not in sub("mˠiː")


def test_slender_consonant_before_a_back_vowel_gets_i():
    assert "i" in sub("tʲuː")


def test_slender_consonant_before_irish_a_gets_i():
    """Vowels are mapped before the Ci rule so Irish /a aː ə/ (back=- in PHOIBLE) count as
    back vowels once they are Georgian /ɑ/."""
    assert sub("nʲaː") == ("n", "i", "ɑ")


def test_slender_coronals_become_the_postalveolar_series():
    assert sub("tʲiː")[0] == "tʃʰ"
    assert sub("dʲiː")[0] == "dʒ"
    assert sub("ʃiː")[0] == "ʃ"


def test_vv_degeminates():
    """decision 5: /vv/ from collision with lenited b/m degeminates (repeated segments)."""
    assert sub("wiː").count("v") <= 1
    assert sub("wvˠaː").count("v") == 1


def test_w_becomes_v():
    assert sub("waː")[0] == "v"


def test_long_vowels_shorten_and_schwa_is_a():
    assert sub("t̪ˠaː") == ("tʰ", "ɑ")
    assert sub("mˠoːɾˠ") == ("m", "ɔ", "r")
    assert sub("pˠeː") == ("pʰ", "ɛ")  # labial: no Cʷ
    assert sub("bˠə") == ("b", "ɑ")


def test_eng_becomes_n_per_spec_not_digest():
    assert sub("ŋaː") == ("n", "ɑ")


def test_j_becomes_i():
    assert sub("jaː") == ("i", "ɑ")


def test_substitute_output_is_all_inventory():
    for ipa in ("bʲiːlʲə", "ʃaːnˠ", "kaːɾˠə", "ɣiːɾʲ", "çaːnʲ", "ɲiːtʲ"):
        assert set(sub(ipa)) <= set(TARGET.inventory), (ipa, sub(ipa))


# ---- stress -------------------------------------------------------------------------------------


def test_stress_is_initial_and_unmarked():
    assert TARGET.stress is not None
    assert TARGET.stress.procedure == "initial"  # §4.1
    assert TARGET.stress.params.get("mark") == "off"  # §4.3


# ---- epithets -----------------------------------------------------------------------------------


def test_epithets_declared():
    for name in ("NOM_I", "URI", "ELI", "SHVILI", "DZE", "EBI"):
        assert name in TARGET.epithets, name
    assert TARGET.epithets["NOM_I"].form == ("i",)
    assert TARGET.epithets["URI"].form == ("u", "r", "i")
    assert TARGET.epithets["ELI"].form == ("ɛ", "l", "i")
    assert TARGET.epithets["SHVILI"].form == ("ʃ", "v", "i", "l", "i")
    assert TARGET.epithets["DZE"].form == ("dz", "ɛ")


def test_epithet_slots_map_to_uri_and_nom_i():
    assert TARGET.meta["epithet-ADJ"] == "URI" and TARGET.meta["epithet-NOUN"] == "NOM_I"


def _affixed(stem, affix):
    """A hand-built affixed word: stem + affix with `$` at the join, one V per syllable."""
    segs = tuple(stem) + tuple(affix)
    vowels = [i for i, s in enumerate(segs) if s in "iɛɑɔu"]
    syll = tuple([0] + [v for v in vowels[1:]])
    return Word(segments=segs, syllables=syll, stress=0, morphemes=frozenset({len(stem)}))


def test_uri_dissimilates_to_uli_after_a_rhotic_stem():
    """digest §6.4 [shosted2006 p.261]: /kʰɑrtʰuli/ but /tʰbilisuri/."""
    got = post_stress(_affixed(("kʰ", "ɑ", "r", "tʰ"), ("u", "r", "i")), TARGET, TABLE)
    assert got.segments == ("kʰ", "ɑ", "r", "tʰ", "u", "l", "i")
    got = post_stress(_affixed(("tʰ", "b", "i", "l", "i", "s"), ("u", "r", "i")), TARGET, TABLE)
    assert got.segments == ("tʰ", "b", "i", "l", "i", "s", "u", "r", "i")


def test_syncope_before_eb():
    """digest §6.2 [wiki-ka §Morphophonology]: megobari -> megobrebi."""
    got = post_stress(_affixed(("m", "ɛ", "ɡ", "ɔ", "b", "ɑ", "r"), ("ɛ", "b", "i")), TARGET, TABLE)
    assert "".join(got.segments) == "mɛɡɔbrɛbi"


# ---- respell ------------------------------------------------------------------------------------


def test_personal_names_are_emitted_as_a_bare_stem():
    assert not spell("kʰ", "a", "n").endswith("i")


def test_respelling_follows_the_5_3_deviations():
    """digest §5.3: D1 `x`, D2 `tch` for /tʃʼ/, D3 `y`, D4 bare stem,
    D5 apostrophe placement UNCHANGED (line 1213)."""
    assert spell("x", "a") == "xa"
    assert spell("tʃʼ", "a").startswith("tch")


def test_d5_places_the_apostrophe_after_the_consonant():
    """digest §5.3 line 1213: 'Not an overlay — follow the standard.' Tested on a
    synthetic ejective, not on a pre-existing name (those are canon inputs, spec §12.J)."""
    out = spell("kʼ", "a")
    assert out.startswith("k'") and out == "k'a"


def test_national_2002_table():
    """[ungegn-georgian p.1], the 33-letter table, minus the D1/D2 overlays."""
    pairs = {
        "pʰ": "p",
        "pʼ": "p'",
        "tʰ": "t",
        "tʼ": "t'",
        "kʰ": "k",
        "kʼ": "k'",
        "qʼ": "q'",
        "ts": "ts",
        "tsʼ": "ts'",
        "dz": "dz",
        "tʃʰ": "ch",
        "dʒ": "j",
        "ʃ": "sh",
        "ʒ": "zh",
        "ɣ": "gh",
        "ɡ": "g",
        "ɑ": "a",
        "ɛ": "e",
        "ɔ": "o",
        "r": "r",
    }
    for seg, letters in pairs.items():
        assert spell(seg, "u") == letters + "u", seg


def test_y_for_i_in_a_non_initial_closed_syllable():
    """digest §5.3 D3 / spec §9.8: Xelxyx = /xɛlxix/."""
    word = Word(segments=("x", "ɛ", "l", "x", "i", "x"), syllables=(0, 3), stress=0)
    assert respell(word, TARGET, TABLE) == "xelxyx"
    word = Word(segments=("tʰ", "tʼ", "i", "ʃ"), syllables=(0,), stress=0)  # initial: stays i
    assert respell(word, TARGET, TABLE) == "tt'ish"
    word = Word(segments=("b", "ɑ", "k", "i"), syllables=(0, 2), stress=0)  # open: stays i
    assert respell(word, TARGET, TABLE) == "baki"


def test_respelling_carries_no_marks():
    word = Word(segments=("kʼ", "ɑ", "tsʼ", "i"), syllables=(0, 2), stress=0)
    assert respell(word, TARGET, TABLE) == "k'atsi"[:0] + "k'ats'i"
