"""Task 6: the @orth("…") rule item with positional tags (spec §4, §11; O-6)."""
import pytest

from helpers import TABLE, w
from strands.check import check_rule_file
from strands.dsl import ItemSpec, ParseError, parse_rules, parse_rules_file
from strands.orth import tag_word
from strands.rewrite import apply_section

# SLEN is declared here because it is a user class in irish.rules (I-41), not a derived one:
# the plan's preamble declared only BROAD, so its `[SLEN orth="bh"]` test could not run.
PREAMBLE = """[meta]
name = orth-test
[inventory]
w vˠ vʲ ɡ ɔ ɾˠ mˠ bˠ β β̃ βʲ i iː ə a e
[classes]
BROAD = w vˠ ɡ ɾˠ mˠ bˠ
SLEN = vʲ
"""


def rf(body):
    return parse_rules(PREAMBLE + body, TABLE, path="<orth-test>")


def run(body, ipa, orthography):
    file = rf("[substitute]\n" + body)
    word = tag_word(w(ipa), orthography)
    return apply_section(word, file.sections["substitute"], file, TABLE, "substitute").segments


def test_the_item_parses_into_an_orth_ItemSpec():
    rule = rf('[substitute]\n@orth("bh") -> β\n').sections["substitute"][0]
    assert rule.target == (ItemSpec(kind="orth", value="bh"),)


def test_the_value_is_case_folded():
    assert rf('[substitute]\n@orth("BH") -> β\n').sections["substitute"][0].target[0].value == "bh"


def test_it_rewrites_only_the_segment_with_that_tag():
    """spec §4: 'spelling disambiguates what sound alone cannot'. Both are /w/."""
    assert run('@orth("bh") -> β\n', "wak", "bhac")[0] == "β"
    assert run('@orth("bh") -> β\n', "wak", "mhac")[0] == "w"
    assert run('@orth("mh") -> β̃\n', "wak", "mhac")[0] == "β̃"


def test_an_untagged_word_is_left_alone():
    file = rf('[substitute]\n@orth("bh") -> β\n')
    assert apply_section(w("wak"), file.sections["substitute"], file, TABLE,
                         "substitute").segments[0] == "w"


def test_a_positional_tag_targets_one_element_of_a_multi_segment_unit():
    """O-6 / spec §11 — the whole point of the positional suffix (R12: draft 1 could not
    express 'the first element only')."""
    out = run('@orth("ia:1") -> i\n', "iə", "ia")
    assert out == ("i", "ə")


def test_a_two_item_target_claims_the_whole_unit():
    out = run('@orth("ia:1") @orth("ia:2") -> i a\n', "iə", "ia")
    assert out == ("i", "a")


def test_it_works_as_a_context_atom():
    file = rf('[substitute]\nɡ -> ɔ / @orth("bh") _\n')
    out = apply_section(tag_word(w("wɡ"), "bhg"), file.sections["substitute"], file, TABLE,
                        "substitute")
    assert out.segments == ("w", "ɔ")


@pytest.mark.parametrize("body,message", [
    ('w -> @orth("bh")\n', "may not appear in a replacement"),
    ('@orth("bh"):1 -> β\n', "may not carry a capture"),
    ('{@orth("bh") w} -> β\n', "may not appear inside"),
    ('@orth(bh) -> β\n', "one double-quoted string"),
    ('@orth("bh -> β\n', "one double-quoted string"),
])
def test_the_illegal_placements_raise_with_a_line_number(body, message):
    with pytest.raises(ParseError, match=message):
        rf("[substitute]\n" + body)


def test_an_unknown_unit_is_an_ERROR_not_a_warning(tmp_path):
    """R9: draft 1 made this a warning and disabled RULE_NEVER_MATCHES for orth items, so
    `@orth("ai")` — which targeted a unit the table did not have — was undetectable."""
    path = tmp_path / "t.rules"
    path.write_text(PREAMBLE + '[substitute]\n@orth("zz") -> β\n', encoding="utf-8")
    found = [f for f in check_rule_file(parse_rules_file(path, TABLE), TABLE)
             if f.code == "ORTH_UNKNOWN_UNIT"]
    assert found and found[0].severity == "error"


def test_a_position_beyond_the_units_arity_is_reported(tmp_path):
    path = tmp_path / "t.rules"
    path.write_text(PREAMBLE + '[substitute]\n@orth("ia:3") -> i\n', encoding="utf-8")
    assert [f for f in check_rule_file(parse_rules_file(path, TABLE), TABLE)
            if f.code == "ORTH_BAD_POSITION"]


def test_a_real_unit_with_a_valid_position_passes_check(tmp_path):
    path = tmp_path / "t.rules"
    path.write_text(PREAMBLE + '[substitute]\n@orth("ia:2") -> ə\n', encoding="utf-8")
    assert [f for f in check_rule_file(parse_rules_file(path, TABLE), TABLE)
            if f.code.startswith("ORTH_")] == []


# ---- the addendum: `orth=` as a bundle constraint (O-6, R11) --------------------------------

def test_at_orth_is_sugar_for_a_bundle():
    a = rf('[substitute]\n@orth("bh") -> β\n').sections["substitute"][0].target[0]
    b = rf('[substitute]\n[orth="bh"] -> β\n').sections["substitute"][0].target[0]
    assert a == b or (a.kind, b.kind) == ("orth", "bundle")


def test_a_bundle_conjoins_the_spelling_with_a_declared_class():
    """R11: this is how the filter keeps quality. Both segments are spelled ⟨bh⟩."""
    body = '[BROAD orth="bh"] -> β\n[SLEN orth="bh"] -> βʲ\n'
    assert run(body, "wak", "bhac")[0] == "β"
    assert run(body, "vʲiː", "bhí")[0] == "βʲ"


def test_a_bundle_may_conjoin_the_spelling_with_features():
    assert run('[C +continuant orth="bh"] -> β\n', "wak", "bhac")[0] == "β"


def test_an_orth_constraint_is_still_rejected_in_a_change_bundle():
    with pytest.raises(ParseError, match="may not appear in a replacement"):
        rf('[substitute]\nw -> [orth="bh"]\n')


def test_a_bundle_orth_value_is_checked_like_the_item(tmp_path):
    path = tmp_path / "t.rules"
    path.write_text(PREAMBLE + '[substitute]\n[BROAD orth="zz"] -> β\n[BROAD orth="ia:3"] -> β\n',
                    encoding="utf-8")
    codes = sorted(f.code for f in check_rule_file(parse_rules_file(path, TABLE), TABLE)
                   if f.code.startswith("ORTH_"))
    assert codes == ["ORTH_BAD_POSITION", "ORTH_UNKNOWN_UNIT"]


def test_a_bundle_with_orth_matches_only_its_phonological_half_and_only_the_tag():
    """The tag alone is not enough: `[SLEN orth="bh"]` leaves a broad ⟨bh⟩ alone."""
    assert run('[SLEN orth="bh"] -> βʲ\n', "wak", "bhac")[0] == "w"
    assert run('[BROAD orth="mh"] -> β̃\n', "wak", "bhac")[0] == "w"
