"""Plan Task 21: the stage pipeline, token-stream respell and epithet slots (spec §4,
§12.C, §12.H; I-8, I-19, I-39)."""
import os
import pathlib
import subprocess
import sys

import pytest

from helpers import FIXTURES, TABLE, irish, w
from strands.dsl import parse_rules, parse_rules_file
from strands.inputs import Entry
from strands.pipeline import (CONSTRUCTIONS, TARGETS, Result, adapt, affix_epithet,
                              load_target, parse_construction, resolve_epithet, run_entry)
from strands.respell import respell
from strands.word import Word

TOY = parse_rules_file(FIXTURES / "toy-target.rules", TABLE)
IRISH = irish()


def test_stage_order_in_the_trace():
    r = adapt([w("pˠaːd̪ˠɾˠəɟ")], TOY, TABLE)
    seen = [t.stage for t in r.trace]
    order = ["substitute", "syllabify", "repair", "stress", "post-stress", "respell"]
    idx = [order.index(s) for s in seen if s in order]
    assert idx == sorted(idx)
    assert "respell" in seen


def test_result_fields():
    r = adapt([w("pˠaːd̪ˠɾˠəɟ")], TOY, TABLE)
    assert isinstance(r, Result)
    assert r.ipa and r.respelling and isinstance(r.flags, tuple) and r.fallbacks >= 0
    assert isinstance(r.assumptions, tuple) and len(r.words) == 1


def test_multiword_constructions_are_adapted_separately_and_rejoined():
    r = adapt([w("mˠaːɾʲə"), w("bˠaːnˠ")], TOY, TABLE)
    assert " " in r.respelling and " " in r.ipa
    assert len(r.words) == 2


def test_respell_chunks_are_opaque():
    """§12.C: a rule that outputs "sh" must not be rematched by a later s- rule."""
    rf = parse_rules('[inventory]\nʃ s a\n[respell]\nʃ -> "sh"\ns -> "z"\n', TABLE)
    assert respell(Word(segments=("ʃ", "a")), rf, TABLE) == "sha"


def test_respell_always_strips_marks():
    rf = parse_rules('[inventory]\np a\n[respell]\np -> "b"\n', TABLE)
    out = respell(Word(segments=("p", "a"), syllables=(0,), stress=0), rf, TABLE)
    assert out == "ba"                      # no "." and no "ˈ", unconditionally


def test_respell_contexts_see_marks_and_boundaries():
    """I-8 / §12.C: `.` and `ˈ` remain usable in [respell] environments."""
    rf = parse_rules('[inventory]\np a\n[respell]\na -> "A" / ˈ p _\n', TABLE)
    word = Word(segments=("p", "a", "p", "a"), syllables=(0, 2), stress=1)
    assert respell(word, rf, TABLE) == "papA"


def test_stress_mark_off_affects_the_ipa_not_the_respelling():
    """Georgian's [stress] mark = off governs Result.ipa formatting only."""
    rf = parse_rules('[inventory]\np a\n[syllable]\ntemplate = any\nonsets = any\n'
                     'codas = any\nsonority = off\n[stress]\nprocedure = initial\n'
                     'mark = off\n[respell]\np -> "b"\n', TABLE)
    r = adapt([w("pa")], rf, TABLE)
    assert "ˈ" not in r.ipa and r.respelling == "ba"


def test_stress_mark_defaults_to_on():
    rf = parse_rules('[inventory]\np a\n[syllable]\ntemplate = any\nonsets = any\n'
                     'codas = any\nsonority = off\n[stress]\nprocedure = initial\n'
                     '[respell]\np -> "b"\n', TABLE)
    r = adapt([w("papa")], rf, TABLE)
    assert r.ipa == "ˈpa.pa" and r.respelling == "baba"


def test_respell_word_final_insertion_is_rendered():
    """DSL epenthesis at `_ #` inserts AFTER the last segment (review-targets fix 2)."""
    rf = parse_rules('[inventory]\na\n[respell]\n0 -> "Z" / _ #\n', TABLE)
    assert respell(Word(segments=("a",)), rf, TABLE) == "aZ"


def test_respell_insertion_does_not_claim_the_following_segment():
    """An insertion is a chunk of width zero: the segment after it stays matchable (I-19)."""
    rf = parse_rules('[inventory]\na\n[respell]\n0 -> "Z" / # _\na -> "A"\n', TABLE)
    assert respell(Word(segments=("a",)), rf, TABLE) == "ZA"


def test_respell_insertion_inside_an_opaque_chunk_is_not_rendered():
    """A later insertion whose point lies strictly inside an earlier chunk is swallowed
    by the chunk (the chunk is opaque); one at the chunk's edges renders."""
    rf = parse_rules('[inventory]\np a\n[respell]\np a -> "X"\n0 -> "Z" / p _ a\n'
                     '0 -> "Y" / # _\n0 -> "W" / _ #\n', TABLE)
    assert respell(Word(segments=("p", "a")), rf, TABLE) == "YXW"


def test_unmatched_segments_pass_through():
    rf = parse_rules('[inventory]\np a\n[respell]\np -> "b"\n', TABLE)
    assert respell(Word(segments=("p", "a")), rf, TABLE) == "ba"


def test_parse_construction_splits_epithet_slots():
    assert parse_construction("DESC+ADJ") == ("DESC", "ADJ")
    assert parse_construction("VOC") == ("VOC", None)


def test_parse_construction_rejects_an_unknown_slot():
    with pytest.raises(Exception):
        parse_construction("DESC+VERB")


def test_epithet_slot_resolves_through_target_meta():
    assert resolve_epithet(TOY, "ADJ") == "NISBA"
    assert resolve_epithet(TOY, "NOUN") is None          # unmapped = no affix, not an error


def test_affix_epithet_attaches_at_a_morpheme_boundary():
    out = affix_epithet(w("ka"), "NISBA", TOY, TABLE)
    assert out.segments == ("k", "a", "i") and 2 in out.morphemes
    assert any(t.stage == "epithet" for t in out.trace)


def test_affix_epithet_unknown_name_raises():
    with pytest.raises(Exception):
        affix_epithet(w("ka"), "NOPE", TOY, TABLE)


def test_epithet_affixation_reruns_syllabification_and_stress():
    plain = adapt([w("kaː")], TOY, TABLE)
    affixed = adapt([w("kaː")], TOY, TABLE, epithet="NISBA")
    assert affixed.ipa != plain.ipa and affixed.ipa.rstrip().endswith("i")
    assert len(affixed.words[0].syllables) == 2


def test_run_entry_applies_the_irish_prepass_then_the_target():
    r = run_entry(Entry("Seán", ipa="ʃaːnˠ", declension="m1"), "VOC", IRISH, TOY, TABLE)
    assert any(t.stage in {"mutation", "normalize", "irish"} for t in r.trace)
    stages = [t.stage for t in r.trace]
    assert stages.index("irish") < stages.index("substitute")


def test_run_entry_with_an_epithet_tag_affixes():
    r = run_entry(Entry("cos", ipa="kosˠ"), "DESC+ADJ", IRISH, TOY, TABLE)
    assert r.ipa.endswith("i") and any(t.stage == "epithet" for t in r.trace)


def test_run_entry_with_an_unmapped_epithet_slot_is_not_an_error():
    r = run_entry(Entry("cos", ipa="kosˠ"), "DESC+NOUN", IRISH, TOY, TABLE)
    assert r.ipa
    assert not any(t.stage == "epithet" for t in r.trace)


def test_run_entry_carries_the_entry_assumptions():
    e = Entry("cos", ipa="kosˠ", assumptions=("gender:inferred-x",))
    assert "gender:inferred-x" in run_entry(e, "DESC", IRISH, TOY, TABLE).assumptions


def test_every_output_segment_is_in_the_target_inventory():
    r = adapt([w("ˈl̪ˠasˠəɾʲxosˠ")], TOY, TABLE)
    for word in r.words:
        assert set(word.segments) <= set(TOY.inventory)


def test_pipeline_is_deterministic():
    assert adapt([w("pˠaːd̪ˠɾˠəɟ")], TOY, TABLE) == adapt([w("pˠaːd̪ˠɾˠəɟ")], TOY, TABLE)


_SEED_SCRIPT = """
from helpers import FIXTURES, TABLE, w
from strands.dsl import parse_rules_file
from strands.pipeline import adapt
rf = parse_rules_file(FIXTURES / "toy-target.rules", TABLE)
print(repr(adapt([w("pa").with_flag("ZZZ").with_flag("AAA"), w("ka")], rf, TABLE)))
"""


def test_serialized_result_is_identical_across_hash_seeds():
    """Byte-identical determinism (review-targets fix 1): a two-flag adaptation serializes the
    same under several PYTHONHASHSEED values in separate processes."""
    root = pathlib.Path(__file__).parents[1]
    env = {**os.environ, "PYTHONPATH": os.pathsep.join([str(root / "src"), str(root / "tests")])}
    outs = set()
    for seed in ("0", "1", "2", "42", "4242"):
        proc = subprocess.run([sys.executable, "-c", _SEED_SCRIPT], capture_output=True,
                              text=True, check=True, env={**env, "PYTHONHASHSEED": seed})
        outs.add(proc.stdout)
    assert len(outs) == 1, outs
    assert "('ZZZ', 'AAA')" in next(iter(outs))


def test_unknown_target_name_raises():
    with pytest.raises(Exception):
        load_target("klingon", TABLE)


def test_constants():
    assert set(TARGETS) == {"welsh", "arabic-egy", "georgian", "dutch", "old-irish"}
    assert "DESC+ADJ" in CONSTRUCTIONS and "DESC+NOUN" in CONSTRUCTIONS
    assert all(parse_construction(c)[0] in IRISH.templates for c in CONSTRUCTIONS)
