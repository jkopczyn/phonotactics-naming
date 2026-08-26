"""Plan Task 28: the committed gallery is the review artefact for the whole project.

Anything wrong in it is a rule-file bug, fixed in the rule files — never by editing the
snapshot. Regenerate with
    uv run strands gallery sources/irish/test-words.tsv --out tests/snapshots/gallery.md
and review the diff in the commit.
"""
from helpers import ROOT
from strands.cli import main

SNAPSHOT = ROOT / "tests" / "snapshots" / "gallery.md"


def test_gallery_matches_the_committed_snapshot(tmp_path):
    out = tmp_path / "g.md"
    assert main(["gallery", str(ROOT / "sources" / "irish" / "test-words.tsv"),
                 "--out", str(out)]) == 0
    assert SNAPSHOT.exists(), "no committed snapshot — generate it and review the diff"
    expected = SNAPSHOT.read_text(encoding="utf-8")
    assert out.read_text(encoding="utf-8") == expected, \
        "gallery changed — regenerate and review the diff in the commit"
