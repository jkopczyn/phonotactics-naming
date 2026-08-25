"""Plan Task 25: `rules/welsh.rules` — the Southern Welsh target (digest §1–§6, §8).

Written first, against an absent file (spec §12.I). The common tests every target task ships
come first; then the Task-25 specifics; then the I-27 repair table; then the regression bar.
Coordinator ruling (2026-08-25, recorded in the plan's Known Deviations §9): the onset list
admits the stop+liquid set and the clusters Welsh's own mutations produce, so tier E's
`θr χr χl` ARE onsets (attested under the aspirate mutation) while `sm sn` are not (they take
the prothetic y-), and `cluster-fallback = same-length` is the last resort, asserted NOT to
fire on the common names.
"""
import pytest
from helpers import (TABLE, entry_of, irish, read_allow_file_for, read_test_words, target, w)

from strands.check import check_rule_file
from strands.pipeline import adapt, run_entry
from strands.regress import assert_ratchet, read_attested, run_regression
from strands.repair import repair
from strands.syllabify import syllabify

TARGET = target("welsh")
IRISH = irish()


def _row(orthography: str) -> dict[str, str]:
    rows = [r for r in read_test_words() if r["orthography"] == orthography]
    assert rows, orthography
    return rows[0]


def _run(orthography: str):
    return run_entry(entry_of(_row(orthography)), "DESC", IRISH, TARGET, TABLE)


# ---- common tests (plan "Tasks 23a–26") ---------------------------------------------------------

def test_rule_file_parses_and_checks_clean():
    errs = [e for e in check_rule_file(TARGET, TABLE) if e.severity == "error"]
    assert errs == [], errs


def test_every_rule_line_carries_a_citation():
    for section in TARGET.sections.values():
        for r in section:
            assert r.comment.strip(), r.rule_id
            assert ("[" in r.comment or "design:" in r.comment or "digest §" in r.comment), \
                (r.rule_id, r.comment)


def test_mutation_output_segments_all_survive():
    """User decision 2: word-initial /w x ɣ ç j h ŋ ɲ/ and mutation-onset clusters."""
    for seg in "w x ɣ ç j h ŋ ɲ".split():
        r = adapt([w(seg + "aː")], TARGET, TABLE)
        assert set(r.words[0].segments) <= set(TARGET.inventory), (seg, r.words[0].segments)
        assert "UNREPAIRED" not in r.flags, seg


def test_no_unrepaired_on_the_144_word_set():
    bad = [row["orthography"] for row in read_test_words()
           if "UNREPAIRED" in run_entry(entry_of(row), "DESC", IRISH, TARGET, TABLE).flags]
    assert set(bad) <= read_allow_file_for("welsh"), sorted(bad)


def test_every_output_segment_is_in_the_inventory_and_no_fallback_segment():
    """Every Irish segment (and the few user-transcription vowels test-words.tsv carries)
    has an explicit [substitute] line, so the nearest-segment fallback (Task 9) never
    has to guess."""
    inv = set(TARGET.inventory)
    for row in read_test_words():
        r = run_entry(entry_of(row), "DESC", IRISH, TARGET, TABLE)
        for word in r.words:
            assert set(word.segments) <= inv, (row["orthography"], word.segments)
        assert not any(t.rule_id == "fallback" for t in r.trace), \
            (row["orthography"], [t.note for t in r.trace if t.rule_id == "fallback"])


# ---- Task 25 specifics -------------------------------------------------------------------------

def test_slender_coronals_map_to_the_welsh_palatal_series():
    assert adapt([w("ʃaː")], TARGET, TABLE).words[0].segments[0] == "ʃ"
    assert adapt([w("tʲaː")], TARGET, TABLE).words[0].segments[0] == "tʃ"
    assert adapt([w("dʲaː")], TARGET, TABLE).words[0].segments[0] == "dʒ"


def test_palatal_series_only_before_a_vowel():
    """§5 line 1264: ⟨ti di si⟩ carry /tʃ dʒ ʃ/ only before a vowel; before a consonant and
    finally the slender coronals are plain (§3.4 lines 840–841)."""
    segs = adapt([w("ʃtʲɾʲiːc")], TARGET, TABLE).words[0].segments      # stríoc
    assert "ʃ" not in segs and "tʃ" not in segs
    assert adapt([w("bʲaːʃ")], TARGET, TABLE).words[0].segments[-1] == "s"


def test_irish_gamma_becomes_g_as_a_design_choice():
    assert adapt([w("ɣaː")], TARGET, TABLE).words[0].segments[0] == "ɡ"
    rules = [r for r in TARGET.sections["substitute"] if r.target[0].value == "ɣ"]
    assert rules and rules[0].tag == "design"        # R18


def test_irish_x_and_c_cedilla_become_chi_as_design_choices():
    assert adapt([w("xaː")], TARGET, TABLE).words[0].segments[0] == "χ"
    assert adapt([w("çaː")], TARGET, TABLE).words[0].segments[0] == "χ"
    rules = [r for r in TARGET.sections["substitute"] if r.target[0].value == "x"]
    assert rules and rules[0].tag == "design"        # R18, digest §8.3 line 1517
    assert "x" not in TARGET.inventory


def test_initial_l_and_r_fortify():
    assert adapt([w("l̪ˠaː")], TARGET, TABLE).respelling.startswith("ll")
    assert adapt([w("ɾˠaː")], TARGET, TABLE).respelling.startswith("rh")


def test_sc_prothesis_is_written_y():
    r = adapt([w("sˠkaː")], TARGET, TABLE)
    assert r.words[0].segments[0] == "ə" and r.respelling.startswith("y")


def test_sp_and_sk_are_respelled_sb_sg():
    """§8.6 line 1632: /sp sk/ are spelled ⟨sb sg⟩ [wiki-cy-phon §Stops]."""
    assert adapt([w("sˠkaː")], TARGET, TABLE).respelling.startswith("ysg")
    assert adapt([w("sˠpˠaː")], TARGET, TABLE).respelling.startswith("ysb")


def test_sm_sn_take_the_prothetic_vowel_not_a_bare_onset():
    """Coordinator ruling (c): sm-/sn- are handled by decision 15, never admitted as onsets."""
    for cl in [("s", "m"), ("s", "n")]:
        assert cl not in TARGET.syllable.onsets
    for word in ("sméara", "sneachta"):
        r = _run(word)
        assert r.words[0].segments[:2] == ("ə", "s"), (word, r.words[0].segments)
        assert r.fallbacks == 0 and "UNREPAIRED" not in r.flags


def test_template_has_exactly_one_nucleus_slot():
    """Spec §12.B/§12.J: the digest's V(V) is one nucleus; the diphthongs live in `nuclei`."""
    assert sum(1 for slot, _ in TARGET.syllable.template if slot == "N") == 1
    assert TARGET.syllable.nuclei                      # the Welsh diphthong list is declared
    assert set(TARGET.syllable.nuclei) == {tuple(d) for d in
                                           ("ai", "ɔi", "əi", "ʊi", "au", "ɛu", "əu", "ɪu")}


def test_stop_plus_liquid_onsets_are_admitted():
    """Coordinator ruling (a), overriding plan S4: the stop+liquid set is licit Welsh."""
    for cl in "pr pl br bl tr dr kr kl ɡr ɡl fr fl θr".split():
        assert tuple(cl) in TARGET.syllable.onset_set, cl


def test_mutation_derived_onsets_are_admitted():
    """Coordinator ruling (b): the onsets Welsh's own mutations produce [wiki-cy-phon
    §Consonant mutations] — nasal ml mr nl nr ŋl ŋr, aspirate fr fl θr χr χl, soft wl wr."""
    for cl in "ml mr nl nr ŋl ŋr fr fl θr χr χl wl wr".split():
        assert tuple(cl) in TARGET.syllable.onset_set, cl


def test_onset_tiers_are_recorded_and_reach_the_trace():
    assert set(TARGET.syllable.onset_tiers.values()) <= {"A", "B", "C", "D"}
    assert TARGET.syllable.onset_tiers                 # every cluster carries a tier
    for cl in TARGET.syllable.onsets:
        if len(cl) > 1:
            assert cl in TARGET.syllable.onset_tiers, cl
    assert TARGET.syllable.coda_tiers and set(TARGET.syllable.coda_tiers.values()) <= {"A", "B"}
    for cl in TARGET.syllable.codas:
        if len(cl) > 1:
            assert cl in TARGET.syllable.coda_tiers, cl


def test_irish_mutation_clusters_survive_without_fallback():
    """Coordinator ruling (b)/(d): eclipsed and lenited Irish onsets land on Welsh
    mutation onsets; cluster-fallback must not fire on them."""
    expect = {"mbláth": ("m", "l"), "ndroim": ("n", "r"), "nglúin": ("ŋ", "l"),
              "chrom": ("χ", "r"), "dhroim": ("ɡ", "r"), "bhlas": ("w", "l"),
              "Bríd": ("b", "r"), "Brian": ("b", "r"), "Gráinne": ("ɡ", "r"),
              "droim": ("d", "r"), "cnoc": ("k", "r"), "cnaipe": ("k", "n")}
    for word, onset in expect.items():
        r = _run(word)
        assert r.words[0].segments[:2] == onset, (word, r.words[0].segments)
        assert r.fallbacks == 0, (word, r.trace)
        assert not any(t.rule_id == "cluster-fallback" for t in r.trace), word
        assert "UNREPAIRED" not in r.flags, word


def test_h_before_a_nasal_is_dropped():
    """Coordinator ruling (c): Welsh has no /hN/ onset; lenited s before a nasal loses h."""
    r = _run("shnámh")
    assert r.words[0].segments[0] == "n", r.words[0].segments
    assert r.fallbacks == 0


def test_cluster_fallback_is_declared_as_last_resort():
    assert TARGET.cluster_fallback == "same-length"


def test_final_schwa_is_repaired():
    """§1 line 200 / §2.5 line 521: /ə/ is barred from final syllables and monosyllables."""
    r = adapt([w("mˠaːɾʲə")], TARGET, TABLE)           # Máire
    assert r.words[0].segments[-1] != "ə" and "UNREPAIRED" not in r.flags


def test_irish_length_is_discarded_welsh_first():
    """§9.13 / digest §4.4 L1: Irish length vanishes; §4.3 recomputes it from the coda."""
    assert adapt([w("bˠaːd̪ˠ")], TARGET, TABLE).words[0].segments == ("b", "aː", "d")   # mab-type
    assert adapt([w("kaːt̪ˠ")], TARGET, TABLE).words[0].segments == ("k", "a", "t")     # clap-type


def test_southern_length_rule_open_final_syllable():
    """§4.3 line 1076: V → Vː / ˈ_ #  (tŷ, da)."""
    assert adapt([w("d̪ˠa")], TARGET, TABLE).words[0].segments == ("d", "aː")


def test_southern_length_rule_before_a_voiced_fricative():
    """§4.3 line 1077, row 2: mab, gradd, rhaff, brath, cath, bach."""
    assert adapt([w("mab")], TARGET, TABLE).words[0].segments == ("m", "aː", "b")
    assert adapt([w("kaθ")], TARGET, TABLE).words[0].segments == ("k", "aː", "θ")
    assert adapt([w("bax")], TARGET, TABLE).words[0].segments == ("b", "aː", "χ")


def test_southern_length_rule_before_s_is_long_south_only():
    """§4.3 line 1078: glas, nes (South: long)."""
    assert adapt([w("ɡlas")], TARGET, TABLE).words[0].segments == ("ɡ", "l", "aː", "s")


def test_southern_length_rule_short_before_fortis_stops_nasals_and_cc():
    """§4.3 lines 1079, 1081: twp, clap, cam, trwm; plant, corff."""
    assert adapt([w("klap")], TARGET, TABLE).words[0].segments == ("k", "l", "a", "p")
    assert adapt([w("kam")], TARGET, TABLE).words[0].segments == ("k", "a", "m")
    assert adapt([w("plant")], TARGET, TABLE).words[0].segments == ("p", "l", "a", "n", "t")


def test_length_before_n_l_r_is_left_unchanged():
    """§4.3 line 1082: lexically determined, not predictable — tal [ˈtal] vs tâl [ˈtaːl].
    The engine leaves the vowel as it arrives, and the line is %design. The Irish length is
    the lexical choice (the only place it survives L1): Seán → Siân; Rónán → Rhonan, the
    penult /oː/ (not before a FINAL n) and the unstressed ultima both short."""
    assert adapt([w("tal")], TARGET, TABLE).words[0].segments == ("t", "a", "l")
    assert adapt([w("taːl")], TARGET, TABLE).words[0].segments == ("t", "aː", "l")
    assert adapt([w("pɛn")], TARGET, TABLE).words[0].segments == ("p", "ɛ", "n")
    assert adapt([w("ʃaːn̪ˠ")], TARGET, TABLE).respelling == "siân"
    r = adapt([w("ɾˠoːn̪ˠaːn̪ˠ")], TARGET, TABLE)
    assert r.words[0].segments == ("r̥", "ɔ", "n", "a", "n") and r.respelling == "rhonan"
    rows = [r for r in TARGET.sections["post-stress"] if "1082" in r.comment]
    assert rows and all(r.tag == "design" for r in rows)


def test_glide_next_to_its_own_vowel_drops():
    """§2.6 line 528 [morrisjones1913 §36 i]: w drops before/after w (= ʊ), i before/after i."""
    assert adapt([w("ʃʊwaːn̪ˠ")], TARGET, TABLE).respelling == "siwan"       # Siobhán
    assert adapt([w("d̪ˠʊw")], TARGET, TABLE).words[0].segments == ("d", "uː")   # dubh


def test_unstressed_vowels_stay_short():
    """§4.3 line 1063: long vowels are restricted to stressed syllables."""
    segs = adapt([w("t̪ˠad̪ˠa")], TARGET, TABLE).words[0].segments           # tadau-type
    assert "aː" not in segs[:-1]


def test_epithets_and_slot_mapping():
    """§6 lines 1300–1307: 7 suffixes; -in ('made of', material nouns only) is dropped;
    I-39: ADJ = -aidd, NOUN unmapped."""
    names = set(TARGET.epithets)
    assert {"OG", "OL", "AIDD", "US", "GAR", "LYD", "YN"} <= names
    assert "IN" not in names
    assert TARGET.meta.get("epithet-ADJ") == "AIDD"
    assert not TARGET.meta.get("epithet-NOUN")
    r = run_entry(entry_of(_row("Bríd")), "DESC+ADJ", IRISH, TARGET, TABLE)
    assert r.respelling.endswith("aidd"), r.respelling
    r = run_entry(entry_of(_row("Bríd")), "DESC+NOUN", IRISH, TARGET, TABLE)
    assert any("NOUN-unmapped" in a for a in r.assumptions)


def test_respelling_uses_welsh_letter_values():
    """§5 lines 1199–1230: v→f, f→ff, χ→ch, ð→dd, ɬ→ll, k→c, ʃ→si/sh, ə→y."""
    assert adapt([w("vʲaː")], TARGET, TABLE).respelling == "fa"
    assert adapt([w("fˠaː")], TARGET, TABLE).respelling == "ffa"
    assert adapt([w("xaː")], TARGET, TABLE).respelling == "cha"
    assert adapt([w("kaː")], TARGET, TABLE).respelling == "ca"
    assert adapt([w("ʃaː")], TARGET, TABLE).respelling == "sia"
    assert adapt([w("ɡaː")], TARGET, TABLE).respelling == "ga"
    assert adapt([w("bˠaːd̪ˠ")], TARGET, TABLE).respelling == "bad"
    assert adapt([w("kaːθ")], TARGET, TABLE).respelling == "cath"
    assert "ə" not in adapt([w("sˠkaː")], TARGET, TABLE).respelling


def test_respelling_carries_no_ipa():
    """§5: Welsh letters only (plus the circumflex vowels) — no IPA leaks through."""
    for row in read_test_words():
        out = run_entry(entry_of(row), "DESC", IRISH, TARGET, TABLE).respelling
        assert out, row["orthography"]
        assert all(ch.isascii() or ch in "âêîôûŵŷ" for ch in out), (row["orthography"], out)


def test_voiceless_sonorants_never_arrive_from_irish():
    """§8.5: /m̥ n̥ ŋ̥ r̥ ɬ/ are not Irish phonemes; only the [repair] fortition creates ɬ, r̥."""
    for seg in ("m̥", "n̥", "ŋ̥", "r̥", "ɬ"):
        assert seg not in IRISH.inventory
    assert not any(seg in ("m̥", "n̥", "ŋ̥") for r in TARGET.sections["substitute"]
                   for seg in r.replacement if isinstance(seg, str))


# ---- I-27 repair table (review-opus §F, digest line refs) --------------------------------------
# Every row is written over the SOUTHERN inventory: /r/ (not Irish /ɾ/) and no /ɨ/.
WELSH_REPAIRS = [
    ("pɔbl",     "pɔbɔl",   "§3.2 rule 1, line 680 (also 477, 705) — pobl"),
    ("kankr",    "kankar",  "§3.2 rule 1, line 680 — cancr"),
    ("fɛnɛstr",  "fɛnɛst",  "§3.2 rule 2, lines 522, 687 — ffenestr"),
    ("pɔsibl",   "pɔsib",   "§3.2 rule 2, line 687 — posibl"),
    ("ewəθr",    "ewərθ",   "§3.2 rule 3, line 694 — ewythr. The digest prints [ˈewɨrθ]; "
                            "Southern has no /ɨ/ (§1, PHOIBLE 2406), so the carrier vowel is "
                            "/ə/ here. The metathesis being tested is unchanged"),
    ("lɔft",     "ɬɔft",    "§3.3 line 810 — loft > lloft"),
    ("rəmedi",   "r̥əmedi",  "§3.3 line 810 — remedy > rhymedi"),
    ("skarlat",  "əskarlat","§3.1 line 621 — scarlet > ysgarlat"),
    ("stiwart",  "əstiwart","§3.1 line 621 — steward > ystiwart"),
]


@pytest.mark.parametrize("before,after,cite", WELSH_REPAIRS)
def test_repair_table(before, after, cite):
    assert repair(syllabify(w(before), TARGET, TABLE), TARGET, TABLE).ipa(marks=False) == after, cite


@pytest.mark.xfail(reason="digest line 508 gives only the orthographic pair cannu/canu; "
                          "no IPA before/after pair exists for degemination")
def test_degemination_has_no_attested_ipa_example():
    assert False


def test_degemination_is_encoded_over_repeated_segments():
    """§2.4 line 499 (R17a): CC → C after an unstressed syllable; geminates are repeated
    segments (I-2). Synthetic: pɔ.tta.da (unstressed first syllable) → pɔtada."""
    word = adapt([w("pɔttada")], TARGET, TABLE).words[0]
    assert "".join(word.segments) == "pɔtada", word.segments


# ---- regression (Mode C; Mode E is empty for Welsh, I-25) ---------------------------------------

def test_regression_meets_the_bar():
    rep = run_regression("welsh", TABLE)
    counts = rep.counts()
    assert counts["E"] == 0 and rep.mode_e_is_empty()
    # 19 rows carry target_ipa; 4 carry a consonant-length ː (mapː ʃopː matː klokː) that no
    # features.tsv row licenses (I-2) and land in the error bucket, so 15 reach Mode C.
    assert counts["C"] == 15, rep.summary()
    assert rep.rate("C") >= 0.70, rep.summary()


def test_error_bucket_is_small():
    rep = run_regression("welsh", TABLE)
    errors = [r for r in rep.rows if r.mode == "error"]
    assert len(errors) <= 4, rep.summary()
    assert all(r.reason == "ː" for r in errors), [(r.target_ipa, r.reason) for r in errors]


def test_modern_orthography_only_rows_are_skipped_not_compared():
    """The 93 layer=modern rows: 19 carry IPA; the rest are orthography-only and must be
    classified `skip` without any attempt at orthographic comparison (needs a Welsh G2P)."""
    rows = read_attested("welsh")
    modern = [r for r in rows if r.get("layer") == "modern"]
    assert len(modern) == 93
    ortho_only = {r["target_form"] for r in modern if not r["target_ipa"].strip()}
    rep = run_regression("welsh", TABLE)
    for r in rep.rows:
        if r.target_form in ortho_only and not r.target_ipa.strip():
            assert r.mode == "skip", r


def test_ratchet_does_not_slip():
    assert_ratchet(run_regression("welsh", TABLE))
