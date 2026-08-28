"""Task 8: `strands reverse` at the CLI (reverse spec §2, §4, §6 bullet 5; R1, R6)."""

import pytest

from strands.cli import main


@pytest.fixture
def small_cap(monkeypatch):
    """C3: the CLI takes `verify`'s cap from `reverse.CAP` (there is no `--cap` flag, R4), so a
    CLI test that verifies anything lowers the module global rather than paying 2000 forward
    runs per word. Every other CLI test passes `--examples 0` and verifies nothing."""
    from strands import reverse

    monkeypatch.setattr(reverse, "CAP", 30)


def run(capsys, *args):
    code = main(["reverse", *args])
    out, err = capsys.readouterr()
    return code, out, err


def test_it_is_a_command_with_a_usage_line():
    from strands.cli import _HANDLERS, _USAGE, COMMANDS

    assert "reverse" in COMMANDS and "reverse" in _HANDLERS
    assert _USAGE["reverse"] == "strands reverse PATTERN --strand X [--examples N] [--ipa]"


def test_a_simple_pattern_prints_the_spec_sections(capsys):
    code, out, _err = run(capsys, "ar", "--strand", "georgian", "--examples", "0")
    assert code == 0
    for section in (
        "target segments:",
        "constraints",
        "Irish spelling pattern",
        "verified examples",
    ):
        assert section in out
    assert out.startswith("ar  [georgian]\n")


def test_the_session_case_lists_the_three_v_sources(capsys):
    """spec §6 bullet 4."""
    code, out, _err = run(capsys, "Ar*v*", "--strand", "georgian", "--examples", "0")
    assert code == 0
    block = out.split("Irish spelling pattern")[0]
    assert "inserted, no Irish letter" in block and block.count("←") >= 4


def test_examples_are_printed_and_capped(capsys, small_cap):
    code, out, _err = run(capsys, "ar*", "--strand", "georgian", "--examples", "3")
    assert code == 0 and "verified examples (" in out
    body = out.split("verified examples (")[1].splitlines()[1:]
    assert len([l for l in body if l.startswith("  ")]) <= 3


def test_examples_zero_skips_verification(capsys):
    _c, out, _e = run(capsys, "ar", "--strand", "georgian", "--examples", "0")
    assert "verified examples: skipped (--examples 0)" in out


def test_ipa_mode_uses_the_ipa_parser(capsys):
    code, out, _err = run(capsys, "ɑr*", "--strand", "georgian", "--ipa", "--examples", "0")
    assert code == 0 and out.startswith("ɑr*  [georgian]")


def test_an_unknown_letter_is_reported(capsys):
    _c, out, _e = run(capsys, "aqa", "--strand", "georgian", "--examples", "0")
    assert "no Irish source for 'q'" in out


def test_multi_word_patterns_are_reported_word_by_word(capsys):
    _c, out, _e = run(capsys, "ar va", "--strand", "georgian", "--examples", "0")
    assert out.count("[georgian]") == 2


def test_old_irish_is_a_lexicon_lookup_with_a_note(capsys):
    code, out, _err = run(capsys, "*mac*", "--strand", "old-irish")
    assert code == 0 and "lexicon lookup only" in out and "matches" in out


def test_old_irish_with_no_match_says_none(capsys):
    _c, out, _e = run(capsys, "zzzz*", "--strand", "old-irish")
    assert "  none" in out


@pytest.mark.parametrize(
    "args,fragment",
    [
        (["ar"], "needs --strand"),
        (["ar", "--strand", "all"], "not all"),
        (["ar", "--strand", "klingon"], "unknown strand"),
        (["ar", "--strand", "georgian", "--examples", "-1"], "non-negative"),
        (["ar", "--strand", "georgian", "--examples", "x"], "non-negative"),
        (["[ao", "--strand", "georgian"], "["),
        (["[!ao]", "--strand", "georgian"], "["),
        (["ar", "--strand", "old-irish", "--ipa"], "old-irish"),
        (["ɑQ", "--strand", "georgian", "--ipa"], "Q"),
    ],
)
def test_usage_errors_exit_two(capsys, args, fragment):
    code = main(["reverse", *args])
    _out, err = capsys.readouterr()
    assert code == 2 and fragment in err


def test_output_is_byte_identical_across_runs(capsys, small_cap):
    _c, a, _e = run(capsys, "ar*v*", "--strand", "georgian", "--examples", "2")
    _c, b, _e = run(capsys, "ar*v*", "--strand", "georgian", "--examples", "2")
    assert a == b
