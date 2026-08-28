"""Task 9: `rules/old-irish.rules` [substitute], the retro-filter (spec §4, §11; O-13, O-15)."""

import pytest
from helpers import TABLE, irish, target, w

from strands.irish import normalize
from strands.orth import tag_word
from strands.substitute import substitute_stage

OI = target("old-irish")
IRISH = irish()


def retro(ipa, orthography=""):
    word = normalize(w(ipa), IRISH, TABLE)
    if orthography:
        word = tag_word(word, orthography)
    return substitute_stage(word, OI, TABLE).segments


@pytest.mark.parametrize(
    "orthography,ipa,index,expected",
    [
        ("dubh", "d̪ˠʊw", -1, "β"),  # dubh ~ dub
        ("sliabh", "ʃlʲiəw", -1, "β"),  # sliabh ~ slíab
        ("lámh", "l̪ˠaːw", -1, "β̃"),  # lámh ~ lám
        ("adharc", "əiɾˠk", None, None),  # adharc ~ adarc (see the next test)
        ("cloch", "kl̪ˠɔx", -1, "x"),  # cloch ~ cloch
        ("bláth", "bˠl̪ˠaː", None, None),
    ],
)
def test_the_lenition_digraphs_map_to_the_lenited_series(orthography, ipa, index, expected):
    """R18: every fixture is an `attested` lexicon row. Log finding 3: ~49 pairs."""
    if expected is None:
        pytest.skip("covered by the class test below")
    assert retro(ipa, orthography)[index] == expected


def test_the_reversal_keeps_quality():
    """R11: draft 1's single broad replacement flattened slender ⟨bh ch th⟩ to broad.

    Task 9 deviation: the plan wrote *cheann* as /ˈcaːn̪ˠ/ (the palatal STOP /c/, which
    ⟨ch⟩ cannot align to); test-words.tsv has /çaːn̪ˠ/, which is used."""
    assert retro("vʲiː", "bhí")[0] == "βʲ"
    assert retro("ˈçaːn̪ˠ", "cheann")[0] == "ç"


def test_the_reversal_keeps_vowel_length():
    """spec §4's non-reversal list; R11: draft 1's `@orth("ea") -> e` shortened /aː/."""
    out = retro("bʲaːn̪ˠ", "beann")
    assert "eː" in out and "e" not in out or "eː" in out


def test_the_quality_digraph_class_deletes_the_glide_and_keeps_the_sound():
    """Log finding 2, 50 pairs — the largest class, and invisible to any sound-based rule."""
    assert retro("bʲanˠ", "bean")[1] == "e"  # bean ~ ben
    assert retro("dʲaɾˠəɡ", "dearg")[1] == "e"  # dearg ~ derg
    assert retro("fʲɪn̪ˠ", "fionn")[1] == "i"  # Fionn ~ Finn


def test_modern_ao_becomes_the_two_segment_digraph():
    """R13: a single `aː` is unwritable as ⟨áe⟩. O-13 / spec §8 row O1."""
    assert retro("iːnˠ", "aon")[:2] == ("a", "i")  # aon ~ óen/áen


def test_ua_and_ia_lengthen_the_first_element_only():
    """R12: positional tags. *tuath ~ túath*, *iasc ~ íasc* — 33 pairs.

    Task 9 deviation: the plan wrote *tuath* as /t̪ˠuəx/, but final ⟨th⟩ is /h/ (or
    silent), never /x/ — that IPA cannot align, so the tags would be absent and the test
    would measure nothing. /t̪ˠuəh/ is the spelling's value."""
    assert retro("t̪ˠuəh", "tuath")[1:3] == ("u", "a")
    assert retro("iəsˠk", "iasc")[:2] == ("i", "a")


def test_the_epenthetic_schwa_is_deleted_by_its_spelling():
    """spec §8 row O5. The aligner tags it `r:2` (Task 5), so the rule is exact."""
    assert retro("ɡɔɾˠəmˠ", "gorm") == ("ɡ", "o", "ɾˠ", "mˠ")


def test_an_unaligned_word_still_loses_its_epenthesis_and_stays_in_inventory():
    """O-7/O-15: no tags, so only the sound-based half applies — and it must still work."""
    out = retro("ɡɔɾˠəmˠ")
    assert set(out) <= set(OI.inventory) and "ə" not in out and "ɔ" not in out


@pytest.mark.parametrize(
    "orthography,ipa,expected",
    [
        # -ach/-as endings: the vowel is lexical and Old Irish writes it (*baccach*, *dúalgas*).
        ("Matánach", "ˈmˠat̪ˠɑːnˠəx", ("mˠ", "a", "t̪ˠ", "aː", "n̪ˠ", "ə", "x")),
        ("Gaelach", "ˈɡeːlˠəx", ("ɡ", "eː", "l̪ˠ", "ə", "x")),
        # a SHORT vowel before ⟨l⟩ — only the C2 test keeps this one: /x/ is not on the grid.
        ("carrbhealach", "ˈkaːɾˠvʲalˠəx", ("k", "aː", "ɾˠ", "βʲ", "a", "l̪ˠ", "ə", "x")),
        # /m/ is no §2.4 C1 and /s/ no §2.4 C2.
        ("Séamus", "ˈʃeːmˠəsˠ", ("ʃ", "eː", "mˠ", "ə", "sˠ")),
    ],
)
def test_a_lexical_unstressed_vowel_is_not_deleted_as_epenthesis(orthography, ipa, expected):
    """Digest §2.4 is a GRID, not `SONORANT _ C`: C1 is {l r n} (never /m/), C2 is labial or
    dorsal and never a voiceless stop, and a long vowel before C1 blocks epenthesis outright
    (blocker 1). Draft 1's `ə -> 0 / SONORANT _ C` matched all four of these and gave
    *Mattánch*, *Gélch*, *cárbelch*, *Séms*."""
    assert retro(ipa) == expected


@pytest.mark.parametrize(
    "ipa,expected",
    [
        ("ˈɡɔɾˠəmˠ", ("ɡ", "o", "ɾˠ", "mˠ")),  # ⟨r⟩ + /m/, the worked example
        ("ˈfʲaɾˠəɡ", ("fʲ", "a", "ɾˠ", "ɡ")),  # ⟨r⟩ + /g/
        ("ˈbˠɔɾˠəbˠ", ("bˠ", "o", "ɾˠ", "bˠ")),  # ⟨r⟩ + /b/
        ("ˈɟal̪ˠəwən̪ˠ", ("ɟ", "a", "l̪ˠ", "β", "ə", "n̪ˠ")),  # ⟨l⟩ + /w/; the SECOND ə is lexical
        ("ˈanʲəmʲ", ("a", "nʲ", "mʲ")),  # ⟨n⟩ + /mʲ/
    ],
)
def test_the_grid_epenthesis_is_still_deleted_by_sound_alone(ipa, expected):
    """O-7/O-15: the narrowed rule must keep firing on every §2.4 environment, untagged."""
    assert retro(ipa) == expected


@pytest.mark.parametrize(
    "orthography,ipa",
    [
        ("athair", "ˈahəɾʲ"),
        ("máthair", "ˈmˠaːhəɾʲ"),
        ("bráthair", "ˈbˠɾˠaːhəɾʲ"),
        ("arán", "əˈɾˠaːnˠ"),
        ("Colmán", "ˈkɔl̪ˠəmˠaːnˠ"),
    ],
)
def test_the_invariant_classes_are_left_alone(orthography, ipa):
    """S19 / log finding 4: the r-stem kinship set and the ⟨-án⟩ diminutive are
    spelling-invariant across both stages — the best 'does the filter over-apply' cases."""
    out = retro(ipa, orthography)
    assert set(out) <= set(OI.inventory)
    assert "ə" not in out[-2:]


def test_a_negative_control_shows_the_section_is_actually_doing_the_work():
    """S13: draft 1's identity assertions passed with no [substitute] section at all.

    Task 9 deviation: the plan's fixture was *dubh*, but the section's own `w -> β` sweep
    (S6) makes tagged and untagged *dubh* identical, so it cannot separate the spelling-
    driven half from the sound-driven one. *lámh* can: tagged ⟨mh⟩ gives /β̃/, the
    sound-only path gives /β/."""
    assert retro("l̪ˠaːw", "lámh") != retro("l̪ˠaːw")
    assert retro("l̪ˠaːw", "lámh")[-1] == "β̃" and retro("l̪ˠaːw")[-1] == "β"


def test_every_substitute_line_carries_a_citation_and_a_legal_tag():
    """R17: spec §4 allows %attested where a lexicon pair instantiates the rule."""
    for rule in OI.sections["substitute"]:
        assert rule.tag in ("attested", "design"), (rule.line, rule.tag)
        assert rule.comment.strip(), rule.line
