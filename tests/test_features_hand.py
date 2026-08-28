"""Task 1b: hand-derived Irish, alias and target-gap rows in rules/features.tsv."""

import csv
import pathlib
import unicodedata

ROOT = pathlib.Path(__file__).parents[1]

HAND = (
    "pˠ bˠ t̪ˠ d̪ˠ fˠ sˠ mˠ n̪ˠ l̪ˠ ɾˠ vˠ pʲ bʲ tʲ dʲ fʲ vʲ mʲ nʲ lʲ ɾʲ "
    "c ɟ ç ɲ lˠ l̠ʲ nˠ n̠ʲ o æ õː g ʋ tʃʰ e y œ ɔː ɛː œ̃"
).split()


def rows():
    with (ROOT / "rules" / "features.tsv").open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def test_all_41_hand_rows_present():
    segs = {r["segment"] for r in rows()}
    for s in HAND:
        assert s in segs, s


def test_total_row_count_is_124():
    assert (
        len(rows()) == 124
    )  # 73 PHOIBLE + 41 hand + 3 input aliases (dˠ tˠ rˠ) + 7 hand:old-irish


def test_no_length_marked_consonant_rows():
    """Gemination is repeated segments, not a length diacritic (I-2)."""
    for r in rows():
        assert not (r["class"] == "C" and r["segment"].endswith("ː")), r["segment"]


def test_dutch_nuclei_tokenize():
    """`ɛi œy ɔu` are declared nuclei in dutch.rules; each member needs a row."""
    segs = {r["segment"] for r in rows()}
    for s in "ɛ i œ y ɔ u".split():
        assert s in segs, s


def test_slender_convention():
    by = {r["segment"]: r for r in rows()}
    for s in "pʲ bʲ tʲ dʲ fʲ vʲ mʲ nʲ lʲ ɾʲ c ɟ ç ɲ".split():
        assert (by[s]["front"], by[s]["back"]) == ("+", "-"), s


def test_broad_convention():
    by = {r["segment"]: r for r in rows()}
    for s in "pˠ bˠ t̪ˠ d̪ˠ fˠ sˠ mˠ n̪ˠ l̪ˠ ɾˠ vˠ".split():
        assert (by[s]["back"], by[s]["front"]) == ("+", "-"), s


def test_dental_broad_coronals_are_anterior_and_distributed():
    by = {r["segment"]: r for r in rows()}
    for s in "t̪ˠ d̪ˠ n̪ˠ l̪ˠ".split():
        assert by[s]["anterior"] == "+" and by[s]["distributed"] == "+", s


def test_plain_dorsals_keep_the_phoible_vector():
    by = {r["segment"]: r for r in rows()}
    for s in "k ɡ x ɣ ŋ".split():
        assert (by[s]["front"], by[s]["back"]) == ("-", "-"), s  # I-41


def test_aliases_match_their_principals():
    by = {r["segment"]: r for r in rows()}
    feats = [k for k in by["k"] if k not in ("segment", "class", "source")]
    for alias, principal in [("lˠ", "l̪ˠ"), ("l̠ʲ", "lʲ"), ("nˠ", "n̪ˠ"), ("n̠ʲ", "nʲ"), ("g", "ɡ")]:
        assert [by[alias][f] for f in feats] == [by[principal][f] for f in feats], alias


def test_every_segment_used_by_test_words_has_a_row():
    """The enforcement point for R7: all 144 rows must be tokenizable."""
    segs = {r["segment"] for r in rows()}
    marks = set("ˈˌ. ")
    mods = set("ˠʲːʰʼˤ")
    used = set()
    with (ROOT / "sources" / "irish" / "test-words.tsv").open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            cur = ""
            for ch in unicodedata.normalize("NFC", row["ipa"] or ""):
                if ch in marks:
                    if cur:
                        used.add(cur)
                        cur = ""
                elif ch in mods or unicodedata.combining(ch):
                    cur += ch
                else:
                    if cur:
                        used.add(cur)
                    cur = ch
            if cur:
                used.add(cur)
    assert used <= segs, sorted(used - segs)
