"""Task 19: `irish.rules [normalize]` and `strands.irish.normalize` (spec §4.1, §12.J)."""
import pytest

from helpers import TABLE, irish, read_test_words, w
from strands.dsl import parse_rules
from strands.irish import apply_inflection, apply_mutation, normalize
from strands.syllabify import syllabify

IRISH = irish()
# A permissive [syllable] spec for resolving the pending stress index (S1): irish.rules has
# no [syllable] section, and syllabify() needs one to check bans.
ANY = parse_rules("[inventory]\n" + " ".join(IRISH.inventory) + "\n[syllable]\ntemplate = any\n"
                  "nuclei = iə uə əi əu\n", TABLE)


def test_aliases_fold_to_the_two_way_system():
    assert normalize(w("lˠa"), IRISH, TABLE).segments == ("l̪ˠ", "a")
    assert normalize(w("n̠ʲi"), IRISH, TABLE).segments == ("nʲ", "i")
    assert normalize(w("gl̪ˠuːnʲ"), IRISH, TABLE).segments[0] == "ɡ"


def test_alpha_folds_to_a():
    assert normalize(w("l̪ˠɑsˠ"), IRISH, TABLE).segments == ("l̪ˠ", "a", "sˠ")
    assert normalize(w("mˠat̪ˠɑːnˠəx"), IRISH, TABLE).segments[3] == "aː"


def test_unmarked_consonant_takes_the_following_vowels_quality():
    assert normalize(w("ti"), IRISH, TABLE).segments[0] == "tʲ"
    assert normalize(w("tu"), IRISH, TABLE).segments[0] == "t̪ˠ"


def test_open_vowels_count_as_broad():
    """/a aː ə/ are front=- back=- in features.tsv (the ECL prothesis rule's convention):
    the broad environment is `[V -front]`, not `[V +back]`."""
    assert normalize(w("ta"), IRISH, TABLE).segments[0] == "t̪ˠ"
    assert normalize(w("saː"), IRISH, TABLE).segments[0] == "sˠ"


def test_final_unmarked_consonant_takes_the_preceding_vowels_quality():
    assert normalize(w("it"), IRISH, TABLE).segments[-1] == "tʲ"
    assert normalize(w("at"), IRISH, TABLE).segments[-1] == "t̪ˠ"


def test_following_vowel_wins_over_preceding():
    assert normalize(w("itu"), IRISH, TABLE).segments[1] == "t̪ˠ"


def test_user_supplied_quality_is_never_overwritten():
    assert normalize(w("t̪ˠiː"), IRISH, TABLE).segments[0] == "t̪ˠ"
    assert normalize(w("ʃuː"), IRISH, TABLE).segments[0] == "ʃ"


def test_broad_dental_coronals_gain_their_dental_features():
    """`t -> t̪ˠ` is not a feature-change bundle: the target row carries anterior and
    distributed as well as back (I-41)."""
    out = normalize(w("tu"), IRISH, TABLE).segments[0]
    assert out == "t̪ˠ" and TABLE.value(out, "distributed") == "+"


def test_broad_k_stays_plain_k_and_slender_k_becomes_c():
    """There is no `kˠ` row; broad /k/ IS `k` (I-41/spec §12.J)."""
    assert normalize(w("ku"), IRISH, TABLE).segments[0] == "k"
    assert normalize(w("ki"), IRISH, TABLE).segments[0] == "c"
    assert normalize(w("gi"), IRISH, TABLE).segments[0] == "ɟ"


def test_h_becomes_c_cedilla_initially_before_a_non_front_vowel():
    assert normalize(w("hoːlʲ"), IRISH, TABLE).segments[0] == "ç"      # sheoil, digest §1.1
    assert normalize(w("hiː"), IRISH, TABLE).segments[0] == "h"
    assert normalize(w("ahaː"), IRISH, TABLE).segments[1] == "h"


def test_every_unmarked_segment_is_covered_in_both_environments():
    rules = IRISH.sections["normalize"]
    targets = {r.target[0].value for r in rules
               if r.target and isinstance(r.target[0].value, str)}
    assert set(IRISH.classes["UNMARKED"]) <= targets
    for seg in IRISH.classes["UNMARKED"]:
        mine = [r for r in rules if r.target and r.target[0].value == seg]
        assert any(r.right and not r.left for r in mine), seg       # _ V
        assert any(r.left and r.right for r in mine), seg           # V _ #


def test_normalize_rules_are_tagged_and_cited():
    for r in IRISH.sections["normalize"]:
        assert r.tag in {"attested", "design"}, r.rule_id
        assert r.comment or r.tag == "attested", r.rule_id


def test_irish_rules_passes_check_with_zero_errors():
    from strands.check import check_rule_file
    assert [e for e in check_rule_file(IRISH, TABLE) if e.severity == "error"] == []


def test_vocative_of_sean_composes_to_a_sheain():
    """digest §3.5: /ʃaːnˠ/ -> LEN -> /haːnˠ/ -> [ç] before a back vowel -> VOC_M1."""
    x = apply_mutation(w("ʃaːnˠ"), "LEN", IRISH, TABLE)
    x = normalize(x, IRISH, TABLE)
    x = apply_inflection(x, "VOC_M1", IRISH, TABLE)
    assert x.ipa(marks=False) == "çaːnʲ"


def test_trace_records_the_normalize_stage():
    x = normalize(w("lˠa"), IRISH, TABLE)
    entries = [t for t in x.trace if t.stage == "irish" and t.rule_id.startswith("normalize:")]
    assert entries and entries[0].before == "lˠa" and entries[0].after == "l̪ˠa"


def test_connacht_gets_initial_stress_when_unmarked():
    """S1: normalize records the stress as a pending SEGMENT index; syllabify() turns it
    into `Word.stress == 0`."""
    x = normalize(w("mˠat̪ˠaːnˠəx"), IRISH, TABLE, dialect="C")
    assert x._pending_stress == 0
    assert syllabify(x, ANY, TABLE).stress == 0
    assert any(t.rule_id == "stress:irish-initial" for t in x.trace)


def test_an_explicit_mark_is_preserved():
    x = normalize(w("əˈwaːnʲ"), IRISH, TABLE, dialect="C")
    assert x._pending_stress == 1
    assert syllabify(x, ANY, TABLE).stress == 1
    assert not any(t.rule_id == "stress:irish-initial" for t in x.trace)


@pytest.mark.parametrize("dialect", ["M", "U"])
def test_munster_and_ulster_rows_pass_through_unstressed(dialect):
    x = normalize(w("kalʲiːnʲ"), IRISH, TABLE, dialect=dialect)
    assert x._pending_stress is None
    assert syllabify(x, ANY, TABLE).stress is None


def test_std_rows_are_treated_as_connacht_for_stress():
    assert normalize(w("ʃaːnˠ"), IRISH, TABLE, dialect="std")._pending_stress == 0


def test_every_test_word_normalizes_without_error():
    for row in read_test_words():
        normalize(w(row["ipa"]), IRISH, TABLE, dialect=row.get("dialect") or "C")
