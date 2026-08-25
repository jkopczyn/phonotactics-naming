"""Plan Task 6: `strands check` static checks and the stress-parameter registry (I-17)."""
import pytest
from helpers import TABLE, FIXTURES
from strands.dsl import parse_rules, parse_rules_file
from strands.check import check_rule_file


def codes(src):
    return sorted(e.code for e in check_rule_file(parse_rules(src, TABLE), TABLE))


def test_clean_file_has_no_findings():
    assert codes("[inventory]\np b\n[substitute]\np -> b\n") == []


def test_undeclared_class_reported_with_its_line():
    errs = check_rule_file(parse_rules("[inventory]\np b\n[substitute]\np -> b / _ NOSUCH\n",
                                       TABLE), TABLE)
    assert errs[0].code == "UNKNOWN_CLASS" and errs[0].line == 4


def test_unknown_feature():
    assert "UNKNOWN_FEATURE" in codes("[inventory]\np b\n[substitute]\n[C +wibble] -> b\n")


def test_alias_is_not_an_unknown_feature():
    assert "UNKNOWN_FEATURE" not in codes("[inventory]\nk kʼ\n[substitute]\nk -> [+ejective]\n")


def test_off_inventory_replacement_is_a_warning_not_an_error():
    errs = check_rule_file(parse_rules("[inventory]\np\n[substitute]\np -> b\n", TABLE), TABLE)
    assert [e.code for e in errs] == ["OFF_INVENTORY"] and errs[0].severity == "warning"


def test_epenthesis_without_context():
    assert "EPENTHESIS_NO_CONTEXT" in codes("[inventory]\np a\n[substitute]\n0 -> a\n")


def test_unknown_stress_parameter():
    assert "UNKNOWN_STRESS_PARAM" in codes(
        "[inventory]\np\n[stress]\nprocedure = penult\nwindow = 3\n")


def test_known_stress_parameter_passes():
    assert codes("[inventory]\np\n[stress]\nprocedure = dutch-weight\nwindow = 3\n") == []


def test_unreachable_feature_change():
    assert "UNREACHABLE_CHANGE" in codes("[inventory]\np\n[substitute]\np -> [+click]\n")


def test_reachable_feature_change_is_clean():
    assert codes("[inventory]\np b\n[substitute]\np -> [+voice]\n") == []


def test_cluster_off_inventory():
    assert "CLUSTER_OFF_INVENTORY" in codes("[inventory]\np a\n[syllable]\nonsets = pl\n")


def test_nucleus_off_inventory():
    assert "NUCLEUS_OFF_INVENTORY" in codes("[inventory]\np a\n[syllable]\nnuclei = ai\n")


def test_undefined_backreference():
    assert "UNDEFINED_BACKREF" in codes("[inventory]\np a\n[substitute]\n0 -> \\1 / a _ p\n")


def test_defined_backreference_is_clean():
    assert codes("[inventory]\np a\n[substitute]\n0 -> \\1 / a:1 _ p\n") == []


def test_unknown_class_in_ban_and_subtable():
    src = ("[inventory]\np a\n[syllable]\nbans = NOSUCH a\n"
           "[mutations]\nLEN:\np -> a / _ OTHER\n")
    assert codes(src) == ["UNKNOWN_CLASS", "UNKNOWN_CLASS"]


def test_findings_are_sorted_by_line():
    src = "[inventory]\np a\n[substitute]\n0 -> a\np -> a / _ NOSUCH\n"
    errs = check_rule_file(parse_rules(src, TABLE), TABLE)
    assert [e.line for e in errs] == sorted(e.line for e in errs)


def test_mini_fixture_has_no_errors():
    errs = check_rule_file(parse_rules_file(FIXTURES / "mini.rules", TABLE), TABLE)
    assert [e for e in errs if e.severity == "error"] == []


def test_registry_is_data_only():
    from strands.stress.params import PROCEDURE_PARAMS
    from strands.dsl import STRESS_PROCEDURES
    assert set(PROCEDURE_PARAMS) == set(STRESS_PROCEDURES)
    assert PROCEDURE_PARAMS["penult"] == frozenset()
    assert "window" in PROCEDURE_PARAMS["dutch-weight"]
    assert "mark" in PROCEDURE_PARAMS["initial"]


def test_cli_check_exit_codes(tmp_path, capsys):
    from strands.cli import main
    bad = tmp_path / "x.rules"; bad.write_text("[inventory]\np a\n[substitute]\n0 -> a\n",
                                               encoding="utf-8")
    assert main(["check", str(bad)]) == 1
    assert "EPENTHESIS_NO_CONTEXT" in capsys.readouterr().err
    warn = tmp_path / "w.rules"; warn.write_text("[inventory]\np\n[substitute]\np -> b\n",
                                                 encoding="utf-8")
    assert main(["check", str(warn)]) == 0        # warnings alone do not fail
    assert "OFF_INVENTORY" in capsys.readouterr().err
    ok = tmp_path / "y.rules"; ok.write_text("[inventory]\np b\n[substitute]\np -> b\n",
                                             encoding="utf-8")
    assert main(["check", str(ok)]) == 0


def test_cli_check_parse_error_exits_1(tmp_path, capsys):
    from strands.cli import main
    bad = tmp_path / "x.rules"; bad.write_text("p -> b\n", encoding="utf-8")
    assert main(["check", str(bad)]) == 1
    assert "x.rules:1:" in capsys.readouterr().err
