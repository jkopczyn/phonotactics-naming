"""Plan Task 8: the substitute stage (spec §4.2a)."""

from helpers import TABLE

from strands.dsl import parse_rules
from strands.substitute import substitute
from strands.word import Word


def test_runs_the_section_in_order():
    rf = parse_rules("[inventory]\np b f v\n[substitute]\np -> b\nv -> f\n", TABLE)
    out = substitute(Word(segments=("p", "v")), rf, TABLE)
    assert out.segments == ("b", "f") and [t.stage for t in out.trace] == ["substitute"] * 2


def test_absent_section_is_a_noop():
    rf = parse_rules("[inventory]\np\n", TABLE)
    wd = Word(segments=("p",))
    assert substitute(wd, rf, TABLE) == wd
