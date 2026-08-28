"""Plan milestone 8 / spec §5: the provisional Irish G2P.

Two kinds of test:

* **Unit tests per rule block**, each taking its expected value from the Wikipedia table the
  corresponding block of `strands.g2p` cites.
* **A regression** over every `src:attested` / `src:user` row of `sources/irish/test-words.csv`,
  reporting the exact-match rate and a looser rate that ignores stress marks and syllable dots.
  Both are ratcheted in `tests/ratchets/g2p.json`.
"""

import json

import pytest
from helpers import ROOT, TABLE, read_test_words

from strands.g2p import g2p
from strands.tokenize import tokenize

RATCHET = ROOT / "tests" / "ratchets" / "g2p.json"


def attested_rows() -> list[dict[str, str]]:
    """The rows whose IPA is regression truth: held sources plus the owner's own hand."""
    out = []
    for row in read_test_words():
        feats = row.get("features") or ""
        tags = feats.split(";")
        if "src:attested" in tags or "src:user" in tags:
            out.append(row)
    return out


def _loose(ipa: str) -> str:
    for mark in ("ˈ", "ˌ", "."):
        ipa = ipa.replace(mark, "")
    return ipa


def rates() -> tuple[float, float, list[tuple[str, str, str]]]:
    rows = attested_rows()
    exact = loose = 0
    misses: list[tuple[str, str, str]] = []
    for row in rows:
        got, _notes = g2p(row["orthography"], row.get("dialect") or "C")
        if got == row["ipa"]:
            exact += 1
        else:
            misses.append((row["orthography"], row["ipa"], got))
        if _loose(got) == _loose(row["ipa"]):
            loose += 1
    return exact / len(rows), loose / len(rows), misses


# ---- unit tests, one block at a time ---------------------------------------------------------


@pytest.mark.parametrize(
    "orth,ipa",
    [
        # [wiki-irish-orthography §Grapheme to phoneme correspondence], consonant table
        ("mac", "mˠak"),
        ("mic", "mʲɪc"),
        ("bán", "bˠaːnˠ"),
        # ⟨l⟩ after a vowel: lenis prevocalically, fortis otherwise — the measured half of the
        # "/lˠ/ or /l̪ˠ/" row (see `_liquid`), so these two differ from the row's own examples
        # béal /bʲeːlˠ/ and speal /sˠpʲalˠ/.
        ("béal", "bʲeːl̪ˠ"),
        ("speal", "sˠpʲal̪ˠ"),
        ("Gaelach", "ˈɡeːlˠəx"),
        ("fós", "fˠoːsˠ"),
        ("fíon", "fʲiːnˠ"),
        ("dorn", "d̪ˠoːɾˠn̪ˠ"),
        ("ceist", "cɛʃtʲ"),
        ("cáis", "kaːʃ"),
        ("teach", "tʲax"),
        ("tír", "tʲiːɾʲ"),
        ("beirt", "bʲɛɾˠtʲ"),  # slender ⟨r⟩ before ⟨t⟩ is /ɾˠ/
        ("sméara", "ˈsˠmʲeːɾˠə"),  # slender ⟨s⟩ before /m/ is /sˠ/
        ("scéal", "ʃceːl̪ˠ"),
        ("cois", "kɔʃ"),
        ("ceann", "caːn̪ˠ"),
        ("long", "l̪ˠuːŋɡ"),
    ],
)
def test_consonant_and_vowel_letters(orth, ipa):
    assert g2p(orth)[0] == ipa


@pytest.mark.parametrize(
    "orth,ipa",
    [
        # lenition and eclipsis spellings [wiki-irish-mutations §Summary table]
        ("bhean", "vʲanˠ"),
        ("mbean", "mʲanˠ"),
        ("cheann", "çaːn̪ˠ"),
        ("gceann", "ɟaːn̪ˠ"),
        ("dhorn", "ɣoːɾˠn̪ˠ"),
        ("ndorn", "n̪ˠoːɾˠn̪ˠ"),
        ("pheann", "fʲaːn̪ˠ"),
        ("bpeann", "bʲaːn̪ˠ"),
        ("shúil", "huːlʲ"),
        ("ngasúr", "ˈŋasˠuːɾˠ"),
        ("ngeata", "ˈɲat̪ˠə"),
        ("mhór", "woːɾˠ"),
        ("héan", "heːnˠ"),
        ("n-éan", "n̠ʲeːnˠ"),
        ("t-éan", "tʲeːnˠ"),
    ],
)
def test_mutation_spellings(orth, ipa):
    assert g2p(orth)[0] == ipa


@pytest.mark.parametrize(
    "orth,ipa",
    [
        # epenthesis, digest §2.4 [wiki-irish-phonology §Post-vocalic consonant clusters]
        ("gorm", "ˈɡɔɾˠəmˠ"),
        ("dearg", "ˈdʲaɾˠəɡ"),
        ("borb", "ˈbˠɔɾˠəbˠ"),
        ("fearg", "ˈfʲaɾˠəɡ"),
        ("ainm", "ˈanʲəmʲ"),
        # blocked by a long vowel / diphthong
        ("téarma", "ˈtʲeːɾˠmˠə"),
        ("dualgas", "ˈd̪ˠuəl̪ˠɡəsˠ"),
        # blocked by the ≥3-syllable Connacht condition
        ("Cairmilíteach", "ˈkaɾʲmʲəlʲiːtʲəx"),
    ],
)
def test_epenthesis(orth, ipa):
    assert g2p(orth)[0] == ipa


def test_multiword_is_space_separated():
    assert g2p("na héisc")[0] == "n̪ˠə heːʃc"


def test_munster_stress_differs_from_connacht():
    """digest §4.1: /a/ before /x/ in σ2 attracts Munster stress (*bacach* /bˠəˈkax/)."""
    assert g2p("bacach", "M")[0] == "bˠəˈkax"
    assert g2p("bacach", "C")[0] != g2p("bacach", "M")[0]


def test_notes_are_returned_for_uncertain_rules():
    ipa, notes = g2p("Sadhbh")
    assert ipa and isinstance(notes, list)


def test_empty_orthography_raises():
    with pytest.raises(ValueError):
        g2p("")


# ---- the regression --------------------------------------------------------------------------


def test_every_constructed_output_tokenizes():
    """Requirement (8): whatever g2p emits must be a legal string over features.csv."""
    for row in read_test_words():
        ipa, _ = g2p(row["orthography"], row.get("dialect") or "C")
        for word in ipa.split(" "):
            tokenize(word, TABLE)


def test_regression_rate_does_not_fall():
    exact, loose, misses = rates()
    ratchet = json.loads(RATCHET.read_text(encoding="utf-8"))
    assert exact >= ratchet["exact"] - 1e-9, (
        f"exact {exact:.4f} < ratchet {ratchet['exact']}\n"
        + "\n".join(f"  {o}\twant {w}\tgot {g}" for o, w, g in misses[:20])
    )
    assert loose >= ratchet["loose"] - 1e-9, f"loose {loose:.4f} < ratchet {ratchet['loose']}"
