"""Plan Task 28: the committed gallery is the review artefact for the whole project.

Anything wrong in it is a rule-file bug, fixed in the rule files — never by editing the
snapshot. Regenerate with
    uv run strands gallery sources/irish/test-words.tsv --out tests/snapshots/gallery.md
and review the diff in the commit.
"""
import pytest

from helpers import ROOT
from strands.cli import main

SNAPSHOT = ROOT / "tests" / "snapshots" / "gallery.md"

# Old Irish plan Task 15 added the fifth strand's templates and the eight formations to
# CONSTRUCTIONS, so the committed gallery is stale until Task 18 regenerates it and reviews
# the diff (its step 4). Task 18 deletes this mark.
@pytest.mark.xfail(strict=False, reason="gallery re-snapshot lands in Old Irish plan Task 18")
def test_gallery_matches_the_committed_snapshot(tmp_path):
    out = tmp_path / "g.md"
    assert main(["gallery", str(ROOT / "sources" / "irish" / "test-words.tsv"),
                 "--out", str(out)]) == 0
    assert SNAPSHOT.exists(), "no committed snapshot — generate it and review the diff"
    expected = SNAPSHOT.read_text(encoding="utf-8")
    assert out.read_text(encoding="utf-8") == expected, \
        "gallery changed — regenerate and review the diff in the commit"
