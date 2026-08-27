"""Task 1a: PHOIBLE half of rules/features.tsv (plan I-34, I-35)."""

import csv
import pathlib

ROOT = pathlib.Path(__file__).parents[1]
FEATURES = ROOT / "rules" / "features.tsv"
PHOIBLE_38 = (
    "tone stress syllabic short long consonantal sonorant continuant delayedRelease "
    "approximant tap trill nasal lateral labial round labiodental coronal anterior "
    "distributed strident dorsal high low front back tense retractedTongueRoot "
    "advancedTongueRoot periodicGlottalSource epilaryngealSource spreadGlottis "
    "constrictedGlottis fortis lenis raisedLarynxEjective loweredLarynxImplosive "
    "click"
).split()


def rows():
    with FEATURES.open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def test_header():
    with FEATURES.open(encoding="utf-8") as fh:
        header = fh.readline().rstrip("\n").split("\t")
    assert header[:3] == ["segment", "class", "source"]
    assert header[3:] == PHOIBLE_38


def test_phoible_half_has_73_rows():
    assert len([r for r in rows() if r["source"].startswith("phoible:")]) == 73


def test_dental_and_retracted_diacritics_are_stripped():
    segs = {r["segment"] for r in rows()}
    for canonical, phoible in [
        ("dʒ", "d̠ʒ"),
        ("sˤ", "s̪ˤ"),
        ("tʼ", "t̪ʼ"),
        ("tʃ", "t̠ʃ"),
        ("tʰ", "t̪ʰ"),
        ("tˤ", "t̪ˤ"),
        ("d", "d̪"),
    ]:
        assert canonical in segs and phoible not in segs


def test_diphthong_rows_are_dropped():
    segs = {r["segment"] for r in rows()}
    for d in "ai au ɔi əi əu ɛu ɪu ʊi œy ɔu ɛi".split():
        assert d not in segs, d


def test_no_duplicate_segments():
    segs = [r["segment"] for r in rows()]
    assert len(segs) == len(set(segs))


def test_values_are_plus_minus_or_zero():
    for r in rows():
        for f in PHOIBLE_38:
            assert r[f] in {"+", "-", "0"}, (r["segment"], f, r[f])


def test_class_column_agrees_with_syllabic():
    for r in rows():
        assert r["class"] in {"C", "V"}
        assert (r["class"] == "V") == (r["syllabic"] == "+")


def test_known_target_segments_survive_import():
    segs = {r["segment"] for r in rows()}
    for s in "tʼ kʼ pʼ qʼ tʃʼ sˤ tˤ dˤ zˤ ɬ r̥ χ ʁ ʔ ʕ ʒ ħ ð θ pʰ tʰ kʰ".split():
        assert s in segs, s


def test_rebuild_is_byte_stable(tmp_path):
    import subprocess
    import sys

    out = tmp_path / "f.tsv"
    subprocess.run(
        [
            sys.executable,
            str(ROOT / "rules" / "build_features.py"),
            str(ROOT / "chat-imports" / "phoible_inventories_starter.csv"),
            str(out),
        ],
        check=True,
    )
    committed = [
        l
        for l in FEATURES.read_text(encoding="utf-8").splitlines()
        if "\tphoible:" in l or l.startswith("segment\t")
    ]
    assert out.read_text(encoding="utf-8").splitlines() == committed
