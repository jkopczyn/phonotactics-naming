"""Task 7: the spelled word, the grapheme table and the one-way reconstruction (spec §11).

Deviations from the plan's listed expectations, each backed by digest §10.2 (the source the
plan's tests say they quote):
  * *bec* is /bʲeɡ/ (conv. 2) and *delg* /dʲelɡ/ (conv. 4) — a following ⟨c⟩/⟨l⟩ after ⟨e⟩
    is BROAD; the plan's `ɟ`/`lʲ` contradicted both the digest and its own rule 4.
  * conv. 5 (ii): a consonant is slender "after a written i, when not followed by a vowel
    letter", and conv. 4's own *imb* /imʲbʲ/ shows the quality holds through the cluster,
    so *bind* is /bʲinʲdʲ/, not the plan's broad `n̪ˠ d̪ˠ`.
  * master table: a non-initial single ⟨m⟩ is /ṽ/ (β̃), so *cnáim* ends in β̃ʲ and *brithem*
    in β̃ (modern *cnáimh*, *breitheamh* agree); the plan's `mʲ`/`mˠ` contradicted its own
    table row. Conv. 5 (i) makes the ⟨c⟩ of *cinn* slender and conv. 2 makes the ⟨d⟩ of
    *claideb* /ðʲ/ (digest /klaðʲəv/).
"""

import pytest
from helpers import ROOT, TABLE

from strands.check import check_grapheme_table
from strands.dsl import parse_rules
from strands.spelled import (
    OI_ORTHOGRAPHY_PATH,
    ROLES,
    GraphemeRule,
    SpelledError,
    SpelledWord,
    apply_grapheme_table,
    load_graphemes,
    spelling_to_ipa,
    spelling_to_words,
    tokenize_spelling,
)


def ipa(text, mutation=""):
    return spelling_to_ipa(SpelledWord.from_spelling(text).with_mutation(mutation))


# ---- losslessness: the property the whole design exists for ------------------------------


@pytest.mark.parametrize(
    "text",
    [
        "macc",
        "bec",
        "dub",
        "cloch",
        "bláth",
        "túath",
        "fer",
        "coll",
        "claideb",
        "carae",
        "muir",
        "dígal",
        "brithem",
        "Ériu",
        "Máel Coluim",
        "ṡúil",
        "ḟer",
        "mbó",
        "Nessa",
    ],
)
def test_a_spelled_word_round_trips_its_own_spelling(text):
    """O-27: `"".join(tokens)` IS the written form. This is the losslessness claim."""
    for part in text.split(" "):
        assert SpelledWord.from_spelling(part).render() == part


def test_capitalization_is_metadata_not_a_token():
    """O-32: tokens are lower-case; the capital is re-applied at render."""
    w = SpelledWord.from_spelling("Ériu")
    assert w.capitalized is True
    assert all(g == g.lower() for g in w.graphemes)
    assert w.render() == "Ériu"
    assert SpelledWord.from_spelling("fer").capitalized is False


def test_a_capital_after_the_written_nasal_prefix_is_kept():
    """O-32 / lossless: *n-Ériu* is capitalized after the ⟨n-⟩ token, as `render` already
    assumes (review oi-data-aligner finding 5)."""
    w = SpelledWord.from_spelling("n-Ériu")
    assert w.capitalized is True
    assert w.render() == "n-Ériu"
    assert SpelledWord.from_spelling("n-ériu").render() == "n-ériu"


def test_the_table_is_sorted_longest_token_first():
    rows = load_graphemes()
    assert OI_ORTHOGRAPHY_PATH == ROOT / "rules" / "old-irish-orthography.csv"
    assert [len(r.token) for r in rows] == sorted([len(r.token) for r in rows], reverse=True)


def test_tokenization_respects_the_env_of_the_only_rows_a_token_has():
    """⟨mb nd ng⟩ are INITIAL nasal tokens; inside a word the letters are two tokens."""
    assert tokenize_spelling("mbó") == ("mb", "ó")
    assert tokenize_spelling("imb") == ("i", "mb")  # conv. 4: the /mb/ cluster
    assert tokenize_spelling("marb") == ("m", "a", "r", "b")
    assert tokenize_spelling("delg") == ("d", "e", "l", "g")


def test_the_final_digraphs_do_not_swallow_a_medial_glide():
    """§41 ⟨-ai -ae⟩ and §40 ⟨-ea -eo -iu⟩ are FINAL spellings: *athair* is a+th+a+i+r."""
    assert tokenize_spelling("athair") == ("a", "th", "a", "i", "r")
    assert tokenize_spelling("carae") == ("c", "a", "r", "ae")
    assert tokenize_spelling("Ériu") == ("é", "r", "iu")


# ---- reconstruction: the digest's own worked examples --------------------------------------


@pytest.mark.parametrize(
    "text,expected",
    [
        ("macc", ("mˠ", "a", "k")),  # conv. 2-3: doubled = fortis
        ("bec", ("bʲ", "e", "ɡ")),  # conv. 2: non-initial ⟨c⟩ = /ɡ/ — digest /bʲeɡ/
        ("bratt", ("bˠ", "ɾˠ", "a", "t̪ˠ")),
        ("brot", ("bˠ", "ɾˠ", "o", "d̪ˠ")),
        ("dub", ("d̪ˠ", "u", "β")),
        ("mod", ("mˠ", "o", "ð")),
        ("mug", ("mˠ", "u", "ɣ")),
        ("ech", ("e", "x")),
        ("áth", ("aː", "θ")),
    ],
)
def test_the_digests_worked_examples_reconstruct(text, expected):
    """Every pair is printed in digest §10.2 conventions 2 and 3."""
    assert ipa(text) == expected


@pytest.mark.parametrize(
    "text,expected",
    [
        ("imb", ("i", "mʲ", "bʲ")),  # conv. 4: after ⟨m⟩, ⟨b⟩ = /b/ — digest /imʲbʲ/
        ("marb", ("mˠ", "a", "ɾˠ", "β")),  # conv. 4: after ⟨r⟩, ⟨b⟩ = /v/
        ("bind", ("bʲ", "i", "nʲ", "dʲ")),  # conv. 4: after ⟨n⟩, ⟨d⟩ = /d/; conv. 5 (ii) slender
        ("long", ("l̪ˠ", "o", "ŋ", "ɡ")),  # conv. 4: after ⟨n⟩, ⟨g⟩ = /ɡ/
        ("delg", ("dʲ", "e", "l̪ˠ", "ɡ")),  # digest /dʲelɡ/
    ],
)
def test_convention_4_stops_after_l_n_r_m(text, expected):
    """digest §10.2 conv. 4 — draft 1 omitted this entirely (R28) and reconstructed
    *derg*, *long*, *ferg* wrongly; all three are lexicon rows."""
    assert ipa(text) == expected


def test_the_glide_i_contributes_no_segment_and_slenderizes():
    """digest §10.2 conv. 5 §36 (R29a): *muir* < *mori*."""
    assert ipa("muir") == ("mˠ", "u", "ɾʲ")
    assert ipa("cnáim") == ("k", "n̪ˠ", "aː", "β̃ʲ")  # master table: non-initial ⟨m⟩ = /ṽ/
    assert ipa("athair") == ("a", "θ", "ə", "ɾʲ")  # 2nd-syllable ⟨a⟩ reduces (step 5)


def test_an_onset_cluster_takes_the_quality_of_its_vowel():
    """conv. 5 grid: *dliged* /ˈdʲlʲiɣʲəð/ — both onset consonants are slender before ⟨i⟩."""
    assert ipa("dliged") == ("dʲ", "lʲ", "i", "ɣʲ", "ə", "ð")


def test_no_glide_is_read_before_a_broad_consonant():
    """§39: *fer* < *viros*. R29b: draft 1's post-pass slenderized this wrongly."""
    assert ipa("fer") == ("fʲ", "e", "ɾˠ")


def test_a_vowel_i_before_a_final_consonant_slenderizes_it():
    """conv. 5 (ii): slender 'after a written i, when not followed by a vowel letter' —
    *fir* gen. of *fer*; and NOT after ⟨í⟩ or the diphthongs ⟨aí oí uí⟩."""
    assert ipa("fir") == ("fʲ", "i", "ɾʲ")
    assert ipa("dín")[-1] == "n̪ˠ"
    assert ipa("Máel")[-1] == "l̪ˠ"


def test_a_doubled_token_takes_one_quality_for_both_halves():
    """R29b: the geminate must not split. It is ONE token (O-2)."""
    assert ipa("coll") == ("k", "o", "l̪ˠ", "l̪ˠ")
    assert ipa("cinn") == ("c", "i", "nʲ", "nʲ")  # conv. 5 (i): ⟨c⟩ before ⟨i⟩ is slender


def test_unstressed_vowels_reduce_but_final_and_long_ones_do_not():
    """digest §10.2 conv. 5 grid; §10.1 'word-finally, all ten combinations occur'."""
    assert ipa("dígal") == ("dʲ", "iː", "ɣ", "ə", "l̪ˠ")
    assert ipa("claideb") == ("k", "l̪ˠ", "a", "ðʲ", "ə", "β")  # digest /klaðʲəv/
    assert ipa("carae")[-1] == "e"  # §41: final ⟨-ae⟩ WRITES /e/ after a broad C
    assert ipa("daltai")[-1] == "i"  # §41: final ⟨-ai⟩ writes /i/
    assert ipa("brithem") == ("bʲ", "ɾʲ", "i", "θʲ", "ə", "β̃")  # non-initial ⟨m⟩ = /ṽ/


@pytest.mark.parametrize(
    "text,final",
    [
        ("marba", "a"),
        ("léicea", "a"),
        ("marbae", "e"),
        ("léice", "e"),
        ("marbai", "i"),
        ("léici", "i"),
        ("súlo", "o"),
        ("doirseo", "o"),
        ("marbu", "u"),
        ("léiciu", "u"),
    ],
)
def test_the_ten_final_vowel_spellings_of_digest_10_1(text, final):
    """digest §10.1: word-finally all ten short-vowel × quality combinations occur, and the
    §40/§41 digraphs ⟨-ea -eo -iu -ae -ai⟩ spell the vowel, not a schwa (review oi-data-aligner
    finding 1)."""
    assert ipa(text)[-1] == final


def test_medial_u_and_o_reduce_to_u_not_schwa():
    """digest §10.1: non-finally only /ə/ (written ⟨a ai e i⟩) and /u/ (written ⟨u o⟩) —
    *lebor* /ˈLʲevur/, *domun* /ˈdoṽun/ (review oi-data-aligner finding 2)."""
    assert ipa("lebor") == ("lʲ", "e", "β", "u", "ɾˠ")
    assert ipa("domun") == ("d̪ˠ", "o", "β̃", "u", "n̪ˠ")


def test_the_u_glide_is_not_a_nucleus():
    """[pokorny1914-oldirish-grammar §38]: *fiuss* — a ⟨u⟩ glide after short ⟨a e i⟩ before a
    syllable-final consonant. Under O-4 (three-way quality is spelling only) it contributes no
    segment and never becomes a /ə/ syllable (review oi-data-aligner finding 3)."""
    assert ipa("fiuss") == ("fʲ", "i", "sˠ")
    assert ipa("firu")[-1] == "u"  # §38's other example: word-FINAL ⟨u⟩ is a vowel


@pytest.mark.parametrize(
    "text,expected",
    [
        ("aí", ("a", "i")),
        ("oí", ("o", "i")),
        ("uí", ("u", "i")),
        ("áu", ("a", "u")),
        ("éu", ("e", "u")),
        ("íu", ("i", "u")),
        ("ía", ("i", "a")),
        ("úa", ("u", "a")),
    ],
)
def test_the_eight_diphthongs_use_the_wiki_old_irish_values(text, expected):
    """O-28 / R19: `wiki-old-irish` §Vowels gives ai oi ui au eu iu ia ua. Draft 1's
    `aːi`/`iə` contradicted digest §10.8 conflict 5 and used the modern reduction vowel."""
    assert ipa(text) == expected


def test_the_nasalized_voiced_stop_is_a_single_nasal():
    """O-29 / R25: master table ⟨mb⟩ = /m/, not /mb/."""
    assert ipa("mbó") == ("mˠ", "oː")
    assert ipa("ndu") == ("n̪ˠ", "u")


def test_lenited_f_is_written_and_silent():
    """R24: ⟨ḟ⟩ is a TOKEN with an empty reconstruction — no segment is deleted, so
    nothing has to carry provenance for it."""
    w = SpelledWord.from_spelling("ḟer")
    assert w.graphemes[0] == "ḟ" and w.render() == "ḟer"
    assert spelling_to_ipa(w) == ("e", "ɾˠ")


# ---- the mutation metadata ----------------------------------------------------------------


def test_unwritten_lenition_lives_in_the_metadata_and_changes_only_the_ipa():
    """digest §10.2 conv. 1: *a bo* /a vo/ is still WRITTEN *bo*. This is the single reason
    the spelled word carries a mutation field."""
    w = SpelledWord.from_spelling("bo").with_mutation("LEN")
    assert w.render() == "bo"
    assert spelling_to_ipa(w)[0] == "β"


def test_unwritten_nasalization_of_a_voiceless_stop_likewise():
    """spec §11 (ii): only ⟨mb nd ng⟩ and ⟨n-V⟩ are written."""
    w = SpelledWord.from_spelling("tech").with_mutation("NAS")
    assert w.render() == "tech"
    assert spelling_to_ipa(w)[0] == "dʲ"


def test_an_unknown_mutation_name_is_rejected():
    with pytest.raises(SpelledError, match="ECL"):
        SpelledWord.from_spelling("bo").with_mutation("ECL")


# ---- punctum is rendering only (O-14) -----------------------------------------------------


def test_punctum_off_changes_the_string_and_provably_not_the_ipa():
    w = SpelledWord.from_spelling("ṡúil")
    assert w.render(punctum=True) == "ṡúil"
    assert w.render(punctum=False) == "súil"
    assert (
        spelling_to_ipa(w) == spelling_to_ipa(SpelledWord.from_spelling(w.render(punctum=False)))
        or spelling_to_ipa(w)[0] == "h"
    )


# ---- grapheme rewrites (O-10) -------------------------------------------------------------


def rule(target, replacement, left=(), right=(), table="T"):
    return GraphemeRule(
        table=table,
        line=1,
        rule_id="t:1",
        target=tuple(target),
        replacement=tuple(replacement),
        left=tuple(left),
        right=tuple(right),
        tag="attested",
        comment="",
    )


def test_a_grapheme_rewrite_edits_tokens_not_letters():
    w = SpelledWord.from_spelling("cenn")
    out = apply_grapheme_table(w, [rule(("c",), ("ch",), left=("#",))], simultaneous=True)
    assert out.render() == "chenn"
    assert out.graphemes == ("ch", "e", "nn")


def test_a_mutation_table_is_simultaneous_and_first_rule_wins():
    """The `irish._apply_table` contract: `c -> ch` must not feed `ch -> x`."""
    rules = [rule(("c",), ("ch",), left=("#",)), rule(("ch",), ("x",), left=("#",))]
    assert (
        apply_grapheme_table(SpelledWord.from_spelling("cenn"), rules, simultaneous=True).render()
        == "chenn"
    )


def test_an_inflection_table_is_ordered_and_each_rule_sees_the_last_output():
    rules = [rule(("c",), ("ch",), left=("#",)), rule(("ch",), ("x",), left=("#",))]
    assert (
        apply_grapheme_table(SpelledWord.from_spelling("cenn"), rules, simultaneous=False).render()
        == "xenn"
    )


def test_capitalization_and_mutation_survive_a_rewrite():
    w = SpelledWord.from_spelling("Cenn").with_mutation("NAS")
    out = apply_grapheme_table(w, [rule(("c",), ("ch",), left=("#",))], simultaneous=True)
    assert out.render() == "Chenn" and out.mutation == "NAS"


def test_sets_classes_and_insertion_are_the_only_other_atoms():
    """Inline set in a target; V/C classes in a context; an empty target inserts."""
    w = SpelledWord.from_spelling("tech")
    out = apply_grapheme_table(w, [rule(("{c t p}",), ("th",), left=("#",))], simultaneous=True)
    assert out.render() == "thech"
    nas = [rule((), ("n-",), left=("#",), right=("V",))]
    assert (
        apply_grapheme_table(SpelledWord.from_spelling("Ériu"), nas, simultaneous=True).render()
        == "n-Ériu"
    )
    assert apply_grapheme_table(w, nas, simultaneous=True).render() == "tech"
    drop = [rule(("C",), (), left=("V",), right=("#",))]
    assert (
        apply_grapheme_table(SpelledWord.from_spelling("fer"), drop, simultaneous=False).render()
        == "fe"
    )


# ---- the ending marker (spec §11) ---------------------------------------------------------


def test_the_ending_marker_tokenizes_and_reconstructs_to_nothing():
    """It exists so a [respell] output carrying an unresolved stem-final /ə/ can become a
    SpelledWord at all (Task 11 -> Task 12). Its reconstruction is EMPTY."""
    w = SpelledWord.from_spelling("carə")
    assert w.graphemes == ("c", "a", "r", "ə") and w.render() == "carə"
    assert spelling_to_ipa(w) == ("k", "a", "ɾˠ")


def test_the_ending_marker_is_the_only_ending_role_row():
    """check_grapheme_table enforces this: one temporary escape hatch, not a family."""
    assert [r.token for r in load_graphemes() if r.role == "ending"] == ["ə"]


def test_the_ending_marker_is_not_hidden_at_render_time():
    """A leaked marker must be VISIBLE, so Task 18's property test can catch it. It is an
    error in a finished output, never a silently-dropped character."""
    assert "ə" in SpelledWord.from_spelling("carə").render()
    assert "ə" in SpelledWord.from_spelling("carə").render(punctum=False)


def test_punctum_off_uses_the_tables_punctum_column_not_a_hardcoded_map():
    rows = {r.token: r.punctum for r in load_graphemes()}
    assert rows["ṡ"] == "s" and rows["ḟ"] == "f"
    assert all(r.punctum == "" for r in load_graphemes() if r.token not in ("ṡ", "ḟ"))


def test_no_row_uses_a_punctum_role():
    """The punctum forms are ordinary cons/silent rows with a plain-letter variant."""
    assert "punctum" not in ROLES
    by_token = {r.token: r.role for r in load_graphemes()}
    assert by_token["ṡ"] == "cons" and by_token["ḟ"] == "silent"


# ---- failure ------------------------------------------------------------------------------


def test_an_unknown_character_raises_and_names_it():
    with pytest.raises(SpelledError, match="z"):
        SpelledWord.from_spelling("fezr")


def test_a_multi_word_form_splits_into_words():
    words = spelling_to_words("Cú Chulainn")
    assert len(words) == 2 and words[1].graphemes[0] == "ch"
    assert words[0].capitalized and words[1].capitalized


# ---- check_grapheme_table -----------------------------------------------------------------


def test_the_committed_table_passes_check():
    assert check_grapheme_table(OI_ORTHOGRAPHY_PATH, TABLE) == []


def test_check_reports_bad_rows(tmp_path):
    bad = tmp_path / "bad.csv"
    bad.write_text(
        "token,env,left,ipa,role,punctum,note\n"
        "ch,any,-,x,cons,-,ok\n"
        "c,any,-,qq,cons,-,unknown ipa\n"
        "c,any,-,k,cons,-,duplicate key\n"
        "t,medial,-,t̪ˠ,cons,-,bad env\n"
        "p,any,-,pˠ,stop,-,bad role\n"
        "ṡ,any,-,h,cons,ss,bad punctum\n"
        "ə,any,-,-,ending,-,one\n"
        "ɨ,any,-,-,ending,-,two\n"
        "ll,any,-,l̪ˠ+l̪ˠ,cons,-,fine\n",
        encoding="utf-8",
    )
    codes = {e.code for e in check_grapheme_table(bad, TABLE)}
    assert codes >= {
        "GRAPH_UNKNOWN_SEGMENT",
        "GRAPH_DUPLICATE_ROW",
        "GRAPH_BAD_ENV",
        "GRAPH_BAD_ROLE",
        "GRAPH_BAD_PUNCTUM",
        "GRAPH_ENDING_COUNT",
    }


def test_check_reports_an_unreachable_token(tmp_path):
    """`c` can never be tokenized when `cc` exists and `c` appears only inside it — i.e.
    a token that no spelling reaches."""
    bad = tmp_path / "bad.csv"
    bad.write_text(
        "token,env,left,ipa,role,punctum,note\n"
        "ab,any,-,a+bˠ,cons,-,-\n"
        "a,any,-,a,vowel,-,-\n"
        'b,noninitial,a,bˠ,cons,-,"only after a, where ab wins"\n'
        "ə,any,-,-,ending,-,-\n",
        encoding="utf-8",
    )
    codes = [e.code for e in check_grapheme_table(bad, TABLE)]
    assert "GRAPH_UNREACHABLE_TOKEN" in codes


# ---- dsl: grammar = graphemes -------------------------------------------------------------

GRAPHEME_FILE = """
[meta]
name = t
grammar = graphemes

[mutations]
LEN:
{c t p} -> ch / # _ %attested  # digest §10.2 conv. 1
b -> b / # _ %design       # marked in metadata only
NAS:
0 -> n- / # _ V %attested  # digest §10.4

[inflect]
GEN_O:
C -> 0 / V _ #
"""


def test_grammar_graphemes_reads_subtables_as_grapheme_rules():
    rf = parse_rules(GRAPHEME_FILE, TABLE)
    assert rf.mutations == {} and rf.inflect == {}
    assert set(rf.grapheme_mutations) == {"LEN", "NAS"}
    r = rf.grapheme_mutations["LEN"][0]
    assert isinstance(r, GraphemeRule)
    assert r.target == ("{c t p}",) and r.replacement == ("ch",) and r.left == ("#",)
    assert r.table == "LEN" and r.rule_id == "mutations:8" and r.tag == "attested"
    assert "conv. 1" in r.comment
    nas = rf.grapheme_mutations["NAS"][0]
    assert nas.target == () and nas.replacement == ("n-",) and nas.right == ("V",)
    gen = rf.grapheme_inflect["GEN_O"][0]
    assert gen.target == ("C",) and gen.replacement == () and gen.left == ("V",)
    assert gen.right == ("#",)


def test_grammar_graphemes_rejects_a_non_grapheme_item():
    from strands.dsl import ParseError

    with pytest.raises(ParseError, match="grapheme"):
        parse_rules(GRAPHEME_FILE.replace("{c t p} -> ch", "z -> ch"), TABLE)
    with pytest.raises(ParseError, match="grapheme"):
        parse_rules(GRAPHEME_FILE.replace("{c t p} -> ch", "[C +voice] -> ch"), TABLE)


def test_without_the_meta_key_the_subtables_are_segment_rules():
    rf = parse_rules("[meta]\nname = t\n[mutations]\nLEN:\nk -> x / # _\n", TABLE)
    assert rf.grapheme_mutations == {} and "LEN" in rf.mutations
