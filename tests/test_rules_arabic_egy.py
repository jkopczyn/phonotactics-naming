"""Plan Task 24: rules/arabic-egy.rules — the Cairene target.

Sources: sources/arabic-egy/digest.md §1–§6, §8; spec §7, §9 (rows 9–12), §12.G.
Common tests from the plan's "Tasks 23a–26" preamble, the Task 24 specific tests, the I-27
repair table and the Task 14 stress table re-run against the real inventory.
"""
import re

import pytest
from helpers import ROOT, TABLE, entry_of, irish, read_allow_file_for, read_test_words, target, w
from strands.check import check_rule_file
from strands.inputs import Entry
from strands.pipeline import adapt, run_entry
from strands.regress import assert_ratchet, run_regression
from strands.repair import repair
from strands.stress import assign_stress
from strands.syllabify import syllabify
from test_stress_cairene import CAIRENE_STRESS_TABLE

NAME = "arabic-egy"
TARGET = target(NAME)
IRISH = irish()
RULES_TEXT = (ROOT / "rules" / f"{NAME}.rules").read_text(encoding="utf-8")


# ---- common tests (plan, Tasks 23a–26 preamble) -----------------------------------------------

def test_rule_file_parses_and_checks_clean():
    errs = [e for e in check_rule_file(TARGET, TABLE) if e.severity == "error"]
    assert errs == [], errs


def test_every_rule_line_carries_a_citation():
    for section in TARGET.sections.values():
        for r in section:
            assert r.comment.strip(), r.rule_id
            assert ("[" in r.comment or "design:" in r.comment or "digest §" in r.comment), \
                (r.rule_id, r.comment)


def test_mutation_output_segments_all_survive():
    """User decision 2: word-initial /w x ɣ ç j h ŋ ɲ/ and mutation-onset clusters."""
    for seg in "w x ɣ ç j h ŋ ɲ".split():
        r = adapt([w(seg + "aː")], TARGET, TABLE)
        assert set(r.words[0].segments) <= set(TARGET.inventory), (seg, r.words[0].segments)
        assert "UNREPAIRED" not in r.flags, seg


def test_no_unrepaired_on_the_144_word_set():
    bad = [row["orthography"] for row in read_test_words()
           if "UNREPAIRED" in run_entry(entry_of(row), "DESC", IRISH, TARGET, TABLE).flags]
    assert set(bad) <= read_allow_file_for(NAME), sorted(bad)


def test_every_output_segment_is_in_inventory_on_the_144_word_set():
    allowed = set(TARGET.inventory)
    for row in read_test_words():
        r = run_entry(entry_of(row), "DESC", IRISH, TARGET, TABLE)
        for word in r.words:
            assert set(word.segments) <= allowed, (row["orthography"], word.segments)


# ---- Task 24 specific tests --------------------------------------------------------------------

@pytest.mark.parametrize("src,expected", [("pˠ", "b"), ("vʲ", "f")])
def test_absent_segments_substitute_per_digest_3_6(src, expected):
    assert adapt([w(src + "aː")], TARGET, TABLE).words[0].segments[0] == expected


def test_broad_coronal_becomes_emphatic():
    assert adapt([w("sˠaː")], TARGET, TABLE).words[0].segments[0] == "sˤ"


def test_slender_s_stays_sh():
    assert adapt([w("ʃaː")], TARGET, TABLE).words[0].segments[0] == "ʃ"


def test_slender_coronals_become_plain():
    assert adapt([w("tʲaː")], TARGET, TABLE).words[0].segments[0] == "t"
    assert adapt([w("dʲaː")], TARGET, TABLE).words[0].segments[0] == "d"


def test_velar_nasal_becomes_n_by_decision_9_12():
    assert adapt([w("l̪ˠɔŋ")], TARGET, TABLE).words[0].segments[-1] == "n"


def test_schwa_becomes_a_unconditionally():
    """R15: digest §8.4 line 1534 open — take the first option (/a/), no positional split."""
    out = adapt([w("mˠəl̪ˠə")], TARGET, TABLE).words[0].segments
    assert out == ("m", "a", "l", "a"), out


def test_there_is_no_degemination_rule():
    """R14a: geminates are phonemic; digest lines 324-326."""
    src = " ".join(r.comment for r in TARGET.sections.get("repair", ()))
    assert "degemination" not in src.lower()
    out = adapt([w("bˠal̪ˠl̪ˠa")], TARGET, TABLE).words[0].segments
    assert out.count("l") == 2


def test_no_final_obstruent_devoicing():
    assert adapt([w("bˠaːd̪ˠ")], TARGET, TABLE).words[0].segments[-1] == "dˤ"
    assert adapt([w("bˠaːdʲ")], TARGET, TABLE).words[0].segments[-1] == "d"


def test_only_one_long_vowel_survives():
    out = adapt([w("bˠaːt̪ˠaːnˠ")], TARGET, TABLE).words[0].segments
    assert sum(1 for s in out if s.endswith("ː")) <= 1        # §3.8 item 4


def test_closed_syllable_shortening_runs_after_stress():
    # §3.8 item 1: /kitaːb+na/ -> kitabna (digest line 728)
    out = adapt([w("kitaːbna")], TARGET, TABLE).words[0]
    assert "aː" not in out.segments and out.segments.count("a") == 2


def test_mid_vowels_raise_on_shortening():
    # §3.8 item 3: /beːt+ha/ -> bitha (digest lines 738-742)
    out = adapt([w("beːtha")], TARGET, TABLE).words[0].segments
    assert out[1] == "i", out


def test_nisba_epithet_attaches_and_restresses():
    r = run_entry(Entry("Muster", ipa="mˠʊsˠt̪ˠəɾˠ"), "DESC+ADJ", IRISH, TARGET, TABLE)
    assert r.ipa.rstrip().endswith("i")
    assert "ˈ" in r.ipa


def test_nisba_deletes_a_stem_final_vowel():
    # digest §6.2: "The termination -V ... is deleted before suffixing /-i/" (madrasa -> madrasi)
    r = adapt([w("madrasa")], TARGET, TABLE, epithet="NISBA")
    assert r.words[0].segments == ("m", "a", "d", "r", "a", "s", "i"), r.words[0].segments


def test_feminine_a_epithet_attaches_after_a_consonant():
    r = run_entry(Entry("Muster", ipa="mˠʊsˠt̪ˠəɾˠ"), "DESC+NOUN", IRISH, TARGET, TABLE)
    assert r.words[0].segments[-1] == "a"


def test_definite_article_assimilates_to_sun_letters():
    """digest §6.1 [abdelmassih-v3 pp.83-84]: il- assimilates before t tˤ d dˤ s sˤ z zˤ r n ʃ;
    not before b f k ... (moon letters). The article is a `$`-joined prefix (see the note in
    the rule file: the epithet mechanism attaches suffixes only)."""
    for sun in "t tˤ d dˤ s sˤ z zˤ r n ʃ".split():
        out = adapt([w(f"il${sun}amaka")], TARGET, TABLE).words[0].segments
        assert out[:4] == ("ʔ", "i", sun, sun), (sun, out)
    for moon in "b f k m w j h x ɣ".split():
        out = adapt([w(f"il${moon}amaka")], TARGET, TABLE).words[0].segments
        assert out[:4] == ("ʔ", "i", "l", moon), (moon, out)


def test_nisba_table_has_eleven_examples_and_respell_table_21_rows():
    """S10: assert the counts so a truncated transcription is caught."""
    assert len(TARGET.sections["respell"]) >= 21
    nisba_examples = re.findall(r"^#\s*nisba:\s", RULES_TEXT, flags=re.MULTILINE)
    assert len(nisba_examples) == 11, len(nisba_examples)


def test_emphatics_are_respelled_dot_under_by_decision_9_11():
    assert "ṣ" in adapt([w("sˠaː")], TARGET, TABLE).respelling
    assert "ṭ" in adapt([w("t̪ˠaː")], TARGET, TABLE).respelling


def test_respell_digraphs_and_long_vowels():
    assert adapt([w("xaː")], TARGET, TABLE).respelling == "khaa"
    assert adapt([w("ɣiː")], TARGET, TABLE).respelling == "ghii"
    assert adapt([w("ʃuː")], TARGET, TABLE).respelling == "shuu"
    assert adapt([w("jaː")], TARGET, TABLE).respelling == "yaa"
    assert adapt([w("ɡaː")], TARGET, TABLE).respelling == "gaa"       # U+0261 -> ASCII g


def test_initial_glottal_stop_is_unwritten_and_medial_is_an_apostrophe():
    r = adapt([w("aːmˠa")], TARGET, TABLE)
    assert r.words[0].segments[0] == "ʔ"
    assert not r.respelling.startswith("ʼ") and not r.respelling.startswith("'")
    assert "ʼ" in adapt([w("saʔal")], TARGET, TABLE).respelling


def test_mode_e_is_empty():
    assert run_regression(NAME, TABLE).mode_e_is_empty()


# I-27 repair table (review-opus §F, digest line refs). "before" strings are the
# post-substitution Cairene-side forms; where the digest gives only the donor and the adapted
# form the input is derived by hand (comment on the row).
CAIRENE_REPAIRS = [
    ("blastik",  "bilastik", "§3.1(a) line 348/356 — plastic (p->b already applied, §3.6)"),
    ("ski",      "ʔiski",    "§3.1(b) line 379/386 — ski"),
    ("banknut",  "bankinut", "§3.2 line 442/456 — banknote, epenthesis after C2"),
    ("bustman",  "bustiman", "§3.2 line 458 — postman (p->b already applied)"),
    ("ɡrub",     "ɡurub",    "§3.3 line 361/499-503 — group, /u/ harmony"),
    ("otel",     "ʔotel",    "§3.7 line 628/630 — hôtel, glottal insertion"),
    ("kitaːbna", "kitabna",  "§3.8 line 728 — closed-syllable shortening"),
    ("striːt",   "ʔistiriːt", "§3.1(c) line 408 — street, prothesis + anaptyxis"),
    ("silajd",   "silajd",   "§3.1(a) line 357 — slide: /sl/ takes anaptyxis (input already repaired)"),
    ("slajd",    "silajd",   "§3.1(a) line 357 — slide"),
    ("swetar",   "siwetar",  "§3.1(a) line 358 — sweater"),
]


@pytest.mark.parametrize("before,after,cite", CAIRENE_REPAIRS)
def test_repair_table(before, after, cite):
    word = syllabify(w(before), TARGET, TABLE)
    if "§3.8" in cite:
        # closed-syllable shortening is a [post-stress] rule (digest: runs after stress)
        got = adapt([w(before)], TARGET, TABLE).words[0]
    else:
        got = repair(word, TARGET, TABLE)
    assert got.ipa(marks=False) == after, cite
    assert "UNREPAIRED" not in got.flags


def test_the_stress_table_has_seventeen_rows():
    assert len(CAIRENE_STRESS_TABLE) == 17


@pytest.mark.parametrize("plain,expected", CAIRENE_STRESS_TABLE)
def test_all_17_cairene_stress_rows_pass_against_the_real_inventory(plain, expected):
    """Re-run Task 14's table with rules/arabic-egy.rules, not the test inventory."""
    got = assign_stress(syllabify(w(plain), TARGET, TABLE), TARGET, TABLE)
    assert got.ipa().replace(".", "") == expected.replace("æ", "a"), plain


# ---- regression harness ------------------------------------------------------------------------

def test_regression_meets_the_bar():
    rep = run_regression(NAME, TABLE)
    assert rep.rate("C") >= 0.75, rep.summary()


def test_error_bucket_is_small():
    rep = run_regression(NAME, TABLE)
    assert rep.counts().get("error", 0) <= 28, rep.summary()      # 10% of 279


def test_ratchet_does_not_slip():
    assert (ROOT / "tests" / "ratchets" / f"{NAME}.json").exists()
    assert_ratchet(run_regression(NAME, TABLE))
