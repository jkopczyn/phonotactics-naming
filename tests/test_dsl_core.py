import pytest
from helpers import FIXTURES, TABLE

from strands.dsl import (
    Backref,
    Bundle,
    ItemSpec,
    ParseError,
    QuotedText,
    parse_rules,
    parse_rules_file,
)

MINI = parse_rules_file(FIXTURES / "mini.rules", TABLE)

def test_meta_and_inventory():
    assert MINI.meta["name"] == "Mini"
    assert MINI.inventory[0] == "p" and "ʒ" in MINI.marginal and "ʒ" in MINI.inventory

def test_derived_classes_are_predeclared():
    for name in ("C", "V", "LIQ", "NAS", "STOP", "FRIC", "GLIDE"):
        assert name in MINI.classes
    assert "l" in MINI.classes["LIQ"] and "m" in MINI.classes["NAS"]
    assert "t̪ˠ" in MINI.classes["C"]        # I-11: Irish segments join C and V

def test_user_class_and_weights():
    assert MINI.classes["BIG"] == ("p", "b", "t", "d", "k", "ɡ")
    assert MINI.weights["front"] == 2.0

def test_simple_rewrite_defaults_to_attested():
    r = MINI.sections["substitute"][0]
    assert r.target[0].value == "p" and r.replacement == ("b",) and r.tag == "attested"
    assert r.rule_id == f"substitute:{r.line}"

def test_match_bundle_and_change_bundle():
    r = MINI.sections["substitute"][1]
    assert r.target[0].value == Bundle("C", {"back": "+"})
    assert isinstance(r.replacement, Bundle) and r.replacement.class_name is None
    assert r.tag == "design"

def test_feature_alias_and_unicode_minus_are_accepted():
    rf = parse_rules("[inventory]\nk kʼ\n[substitute]\nk -> [+ejective]\n"
                     "kʼ -> k / [STOP −voice] _\n", TABLE)
    assert rf.sections["substitute"][0].replacement.constraints == {"raisedLarynxEjective": "+"}
    assert rf.sections["substitute"][1].left[0].atom.value.constraints == \
        {"periodicGlottalSource": "-"}

def test_multi_segment_target_and_environment():
    r = MINI.sections["substitute"][2]
    assert tuple(i.value for i in r.target) == ("sˠ", "ʃ")
    assert [c.atom for c in r.left] == ["#"]
    assert r.right[0].atom.value == "V"
    assert r.comment.strip() == "both segments replaced"

def test_epenthesis_rule_has_empty_target():
    r = MINI.sections["substitute"][3]
    assert r.target == () and [c.atom for c in r.left][0] == "#"

def test_deletion_rule():
    assert MINI.sections["substitute"][4].replacement == ()

def test_capture_and_backreference():
    r = MINI.sections["substitute"][5]
    assert r.left[0].atom.capture == 1
    assert r.replacement == (Backref(1),)

def test_inline_set():
    r = MINI.sections["substitute"][5]
    s = r.right[0].atom
    assert s.kind == "set" and s.value == ("l", "n", "r")

def test_metathesis_via_captures():
    r = MINI.sections["substitute"][6]
    assert [i.capture for i in r.target] == [1, 2]
    assert r.replacement == (Backref(2), Backref(1))

def test_optional_and_star():
    rf = parse_rules("[inventory]\np a\n[substitute]\np -> a / (a)_ a*\n", TABLE)
    r = rf.sections["substitute"][0]
    assert r.left[0].optional and r.right[0].star

def test_star_on_optional_is_a_parse_error():
    with pytest.raises(ParseError):
        parse_rules("[inventory]\np a\n[substitute]\np -> a / (a)*_\n", TABLE)

@pytest.mark.parametrize("env", ["(a:1) _", "a:1* _"])
def test_capture_on_an_optional_or_starred_item_is_a_parse_error(env):
    """I-9: a zero-or-more item cannot define a backreference."""
    with pytest.raises(ParseError):
        parse_rules(f"[inventory]\np a\n[substitute]\n0 -> \\1 / {env} p\n", TABLE)

def test_class_name_in_a_replacement_is_a_parse_error():
    """I-5 / spec §12.C: replacements carry no bare class names."""
    with pytest.raises(ParseError):
        parse_rules("[inventory]\np a\n[classes]\nX = p\n[substitute]\na -> X\n", TABLE)

def test_syllable_and_stress_marks_are_rejected_in_targets():
    with pytest.raises(ParseError):
        parse_rules("[inventory]\np a\n[substitute]\n. -> p\n", TABLE)     # I-8

def test_unknown_section_and_unknown_segment_and_missing_arrow_raise_with_line_numbers():
    # Deviation from the plan text: it used `Q -> p` for the unknown-segment case, but `Q`
    # is a class name by I-10, and Task 6 requires undeclared class names to PARSE so that
    # `check` can report UNKNOWN_CLASS with a line number. `ʘ` is not a features.tsv row.
    for src, ln in [("[frobnicate]\n", 1),
                    ("[inventory]\np\n[substitute]\nʘ -> p\n", 4),
                    ("[inventory]\np a\n[substitute]\np a\n", 4)]:
        with pytest.raises(ParseError) as e:
            parse_rules(src, TABLE)
        assert f":{ln}:" in str(e.value)

def test_undeclared_class_name_parses_for_check_to_report():
    """Task 6 reports UNKNOWN_CLASS / UNKNOWN_FEATURE; the parser must not pre-empt it."""
    rf = parse_rules("[inventory]\np b\n[substitute]\np -> b / _ NOSUCH\n[C +wibble] -> b\n",
                     TABLE)
    assert rf.sections["substitute"][0].right[0].atom == ItemSpec("class", "NOSUCH")
    assert rf.sections["substitute"][1].target[0].value.constraints == {"wibble": "+"}

def test_comment_after_environment_without_tag_is_an_error():
    with pytest.raises(ParseError) as e:
        parse_rules("[inventory]\np a\n[substitute]\np -> a / _ a # note\n", TABLE)
    assert "explicit %tag" in str(e.value)

def test_word_edge_hash_in_environment_is_not_a_comment():
    rf = parse_rules("[inventory]\np a\n[substitute]\np -> a / _ #\n", TABLE)
    assert [c.atom for c in rf.sections["substitute"][0].right] == ["#"]

def test_quoted_text_only_in_respell():
    rf = parse_rules('[inventory]\nʃ\n[respell]\nʃ -> "sh"\n', TABLE)
    assert rf.sections["respell"][0].replacement == (QuotedText("sh"),)
    with pytest.raises(ParseError):
        parse_rules('[inventory]\nʃ\n[substitute]\nʃ -> "sh"\n', TABLE)

def test_parse_error_shape():
    with pytest.raises(ParseError) as e:
        parse_rules("[inventory]\np\nfoo = bar\n", TABLE, path="x.rules")
    assert e.value.line == 3 and str(e.value).startswith("x.rules:3: ")

def test_parsing_is_deterministic():
    assert parse_rules_file(FIXTURES / "mini.rules", TABLE) == \
           parse_rules_file(FIXTURES / "mini.rules", TABLE)

def test_percent_inside_a_comment_is_not_a_tag():
    rf = parse_rules("[inventory]\np b\n[substitute]\np -> b # 50% of cases\n", TABLE)
    r = rf.sections["substitute"][0]
    assert r.tag == "attested" and r.comment.strip() == "50% of cases"
    with pytest.raises(ParseError) as e:
        parse_rules("[inventory]\np a\n[substitute]\np -> a / _ a # 50%\n", TABLE)
    assert "explicit %tag" in str(e.value)

def test_bad_tag_is_a_parse_error():
    with pytest.raises(ParseError):
        parse_rules("[inventory]\np b\n[substitute]\np -> b %guess\n", TABLE)
