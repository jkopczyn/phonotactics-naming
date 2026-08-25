"""Plan Task 15: the `dutch-weight` stress procedure (sources/dutch/digest.md §4 "The
practical rule", lines 671–687 — constructed by the digest, not stated by any source)."""
import pytest
from helpers import TABLE, w
from strands.dsl import parse_rules
from strands.syllabify import syllabify
from strands.stress import assign_stress

# The plan's inventory lists a short `ø`; rules/features.tsv has no `ø` row (only `øː`), and
# [inventory] rejects unknown segments, so `ø` is omitted here. No test word uses it.
DUTCH = ("[inventory]\np b t d k ɡ f v s z ʃ ʒ x ɣ h m n ŋ l r ʋ j "
         "ɑ ɛ ɪ ɔ ʏ ə a e i o u y aː eː iː oː uː yː øː\n"
         "[syllable]\ntemplate = (C)(C)(C)N(C)(C)\nonsets = any\ncodas = any\nsonority = off\n"
         "[stress]\nprocedure = dutch-weight\n")

# digest §4 line 683-685: (plain, stressed, rule)
DUTCH_STRESS_TABLE = [
    ("avɔntyr",  "a.vɔn.ˈtyr", 2),
    ("aɣɛnda",   "a.ˈɣɛn.da",  3),
    ("ɑlbatrɔs", "ˈɑl.ba.trɔs", 4),
    ("arena",    "a.ˈre.na",   5),
    ("avokado",  "a.vo.ˈka.do", 5),
    ("mirakəl",  "mi.ˈra.kəl", 1),
]


def stressed(plain, src=DUTCH):
    rf = parse_rules(src, TABLE)
    return assign_stress(syllabify(w(plain), rf, TABLE), rf, TABLE)


@pytest.mark.parametrize("plain,expected,rule", DUTCH_STRESS_TABLE)
def test_dutch_worked_examples(plain, expected, rule):
    out = stressed(plain)
    if out.ipa() != expected:
        # Syllable dots are the digest's own; our syllabifier (Task 10, onsets = any) puts
        # avontuur's `nt` in the onset (a.vɔ.ˈntyr). Compare stress position only: the
        # index of the syllable carrying ˈ.
        want = expected[:expected.index("ˈ")].count(".")
        assert out.stress == want, f"{out.ipa()} != {expected}"


def test_schwa_is_never_stressed():
    out = stressed("mirakəl")
    assert out.segments[out.syllables[out.stress]] != "ə"
    assert out.stress == 1


def test_three_syllable_window_is_respected():
    out = stressed("avokadokado")
    assert out.stress >= len(out.syllables) - 3


def test_window_parameter_is_read():
    rf = parse_rules(DUTCH + "window = 3\n", TABLE)
    assert rf.stress.params["window"] == "3"


def test_monosyllable_and_disyllable():
    assert stressed("tyr").stress == 0
    assert stressed("kata").stress == 0          # rule 5, penult
    assert stressed("katɔs").stress == 0         # rule 4 has no antepenult -> penult


def test_final_diphthong_takes_stress():
    src = DUTCH.replace("sonority = off\n", "sonority = off\nnuclei = ɛi\n")
    assert stressed("lakɛi", src).stress == 1     # digest gen. 5, lakei [la.ˈkɛi]


def test_lax_final_with_two_codas_is_superheavy():
    assert stressed("dokymɛnt").stress == 2      # digest gen. 4, document [do.ky.ˈmɛnt]


def test_trace_entry():
    out = stressed("arena")
    assert out.trace[-1].stage == "stress" and out.trace[-1].rule_id == "stress:dutch-weight"
