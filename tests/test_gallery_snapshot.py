"""Plan Task 28: the committed gallery is the review artefact for the whole project.

Anything wrong in it is a rule-file bug, fixed in the rule files — never by editing the
snapshot. Regenerate with
    uv run strands gallery sources/irish/test-words.csv --out tests/snapshots/gallery.md
and review the diff in the commit.
"""

from helpers import ROOT

from strands.cli import main

SNAPSHOT = ROOT / "tests" / "snapshots" / "gallery.md"


def test_gallery_matches_the_committed_snapshot(tmp_path):
    out = tmp_path / "g.md"
    assert (
        main(["gallery", str(ROOT / "sources" / "irish" / "test-words.csv"), "--out", str(out)])
        == 0
    )
    assert SNAPSHOT.exists(), "no committed snapshot — generate it and review the diff"
    expected = SNAPSHOT.read_text(encoding="utf-8")
    assert out.read_text(encoding="utf-8") == expected, (
        "gallery changed — regenerate and review the diff in the commit"
    )


# ---- Old Irish plan Task 18: the fifth column and the formation block ----------------------


def test_the_gallery_has_a_fifth_column_with_the_lookup_marks():
    """spec §7. `render_cell` already prints !FLAG — this asserts it, it asks for no code."""
    text = (ROOT / "tests" / "snapshots" / "gallery.md").read_text(encoding="utf-8")
    assert "old-irish" in text and "!ATTESTED" in text and "!RETRO" in text


def test_the_formation_template_block_is_present_and_built_from_elements():
    """R31: a whole-name lexicon row returns ATTESTED in one piece and never exercises the
    template."""
    text = (ROOT / "tests" / "snapshots" / "gallery.md").read_text(encoding="utf-8")
    assert "## Old Irish formations" in text
    for name in ("MAEL", "GILLA", "CU", "FER", "COLOUR", "MAC", "UA", "INGEN"):
        assert name in text
    assert "Máel" in text and "macc" in text


def test_the_formation_block_is_a_deterministic_function_of_the_rule_files():
    """The block is rendered from the lexicon's ELEMENT rows with G2P transcriptions
    (`ipa:constructed`); two renders agree and every formation row is present."""
    from helpers import TABLE, irish

    from strands.gallery import formation_block
    from strands.pipeline import load_target

    oi = load_target("old-irish", TABLE)
    lines = formation_block(irish(), oi, TABLE)
    assert lines == formation_block(irish(), oi, TABLE)
    assert lines[0] == "## Old Irish formations"
    rows = [ln for ln in lines if ln.startswith("| ")]
    for name in ("MAEL", "GILLA", "CU", "FER", "COLOUR", "MAC", "UA", "INGEN"):
        assert any(ln.startswith(f"| {name} |") for ln in rows), name
    assert any("!ATTESTED" in ln for ln in rows)
