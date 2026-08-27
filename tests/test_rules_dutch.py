"""Plan Task 26: `rules/dutch.rules` — the Belgian Dutch target (sources/dutch/digest.md
§1–§6, §8; spec §7 Dutch, decisions 9.16–9.18). Written before the rule file (spec §12.I)."""

import pytest
from helpers import TABLE, entry_of, irish, read_allow_file_for, read_test_words, target, w

from strands.check import check_rule_file
from strands.pipeline import adapt, run_entry
from strands.regress import assert_ratchet, run_regression
from strands.repair import repair
from strands.syllabify import syllabify

TARGET = target("dutch")
IRISH = irish()


# ---- common tests (plan "Tasks 23a–26" preamble) ----------------------------------------------


def test_rule_file_parses_and_checks_clean():
    errs = [e for e in check_rule_file(TARGET, TABLE) if e.severity == "error"]
    assert errs == [], errs


def test_every_rule_line_carries_a_citation():
    for section in TARGET.sections.values():
        for r in section:
            assert r.comment.strip(), r.rule_id
            assert "[" in r.comment or "design:" in r.comment or "digest §" in r.comment, (
                r.rule_id,
                r.comment,
            )


def test_mutation_output_segments_all_survive():
    """User decision 2: word-initial /w x ɣ ç j h ŋ ɲ/ and mutation-onset clusters."""
    for seg in "w x ɣ ç j h ŋ ɲ".split():
        r = adapt([w(seg + "aː")], TARGET, TABLE)
        assert set(r.words[0].segments) <= set(TARGET.inventory), (seg, r.words[0].segments)
        assert "UNREPAIRED" not in r.flags, (seg, r.ipa)


def test_no_unrepaired_on_the_144_word_set():
    bad = [
        row["orthography"]
        for row in read_test_words()
        if "UNREPAIRED" in run_entry(entry_of(row), "DESC", IRISH, TARGET, TABLE).flags
    ]
    assert set(bad) <= read_allow_file_for("dutch"), sorted(bad)


# ---- task-specific tests (plan Task 26, step 1) ------------------------------------------------


@pytest.mark.parametrize("construction", ["VOC", "PATRO_O", "PATRO_NI"])
@pytest.mark.parametrize("orthography", ["shnámh", "sneachta", "sméara"])
def test_lenited_h_plus_sonorant_is_repaired_after_a_prefix_too(orthography, construction):
    """The `h -> 0 / # _ C` repair (digest §2 line 171: /h/ never enters a cluster) must also
    fire when the lenited stem follows a particle (*a shnámh*, *Ní Shméara*): the /h/ then sits
    after the `$` seam, not at `#`, and the review-final gallery showed those cells UNREPAIRED."""
    row = next(r for r in read_test_words() if r["orthography"] == orthography)
    r = run_entry(entry_of(row), construction, IRISH, TARGET, TABLE)
    assert "UNREPAIRED" not in r.flags, r.ipa
    assert "h" not in r.words[0].segments, r.ipa


def test_slender_consonant_in_an_onset_gets_a_yod_and_in_a_coda_is_plain():
    assert adapt([w("tʲaː")], TARGET, TABLE).words[0].segments[:2] == ("t", "j")
    assert adapt([w("aːtʲ")], TARGET, TABLE).words[0].segments[-1] == "t"


def test_slender_rule_uses_the_declared_slender_class_not_a_feature_bundle():
    """Spec §12.J / I-31: the Cj rule is written over a declared class (SLEN or a declared
    subset of it), never over `[C +front]`."""
    yod = [r for r in TARGET.sections["substitute"] if not r.target and r.replacement == ("j",)]
    assert yod, "no `0 -> j` rule in [substitute]"
    for r in yod:
        item = r.left[-1].atom
        name = item.value if item.kind == "class" else getattr(item.value, "class_name", None)
        assert name is not None and name.startswith("SLEN"), r.rule_id
        assert set(TARGET.classes[name]) <= set(TARGET.classes["SLEN"]), name


def test_w_becomes_the_labiodental_approximant():
    assert adapt([w("waː")], TARGET, TABLE).words[0].segments[0] == "ʋ"


def test_final_obstruent_devoicing():
    assert adapt([w("bˠaːd̪ˠ")], TARGET, TABLE).words[0].segments[-1] == "t"


def test_matanach_does_not_trigger_the_fricative_ban():
    """goals note + digest §2: the /x/ follows the schwa of -ach, not the long vowel."""
    assert adapt([w("mˠat̪ˠaːnˠəx")], TARGET, TABLE).words[0].segments[-1] == "x"


def test_bach_does_trigger_it():
    """digest line 308: the ban bites when a long vowel directly precedes."""
    out = adapt([w("bˠaːx")], TARGET, TABLE).words[0].segments
    assert out[-1] == "ɣ"  # decision 9.18: voice the fricative


def test_appendix_narrowing_is_declared():
    """R21: the digest licenses up to three coronal obstruents; `s t` is a narrowing and
    must say so, or the set must be the full coronal-obstruent list."""
    coronal_obstruents = {
        seg for seg in TARGET.inventory if TABLE.matches(seg, {"coronal": "+", "sonorant": "-"})
    }
    if set(TARGET.syllable.appendix) < coronal_obstruents:
        assert "appendix-narrowed" in TARGET.meta
    else:
        assert set(TARGET.syllable.appendix) == coronal_obstruents


def test_onset_list_sizes_match_the_digest():
    """R21: the digest's 30 native CC + 27 loan CC (lines 179–187) + 7 CCC (lines 210–211),
    plus singletons. Two of the 27 loan entries, `ts` (tsaar) and `tʃ` (chip), are single
    segments under the I-34 canon, so they count as digest entries but not as CC clusters.
    The Cj onsets that decision 9.16 adds are tiered DESIGN and counted separately."""
    tiers = TARGET.syllable.onset_tiers
    native = {c for c, t in tiers.items() if t == "NATIVE"}
    loan = {c for c, t in tiers.items() if t == "LOAN"}
    design = {c for c, t in tiers.items() if t == "DESIGN"}
    norm = {c for c, t in tiers.items() if t == "NORM"}  # Belgian ɣl ɣr ɣn (§0 line 35)
    assert set(tiers.values()) == {"NATIVE", "LOAN", "DESIGN", "NORM"}
    assert len([c for c in native if len(c) == 2]) == 30
    assert len([c for c in loan if len(c) == 2]) == 25
    assert {("ts",), ("tʃ",)} <= loan  # the two affricate "clusters"
    assert len([c for c in native | loan if len(c) == 3]) == 7
    assert len([c for c in native if len(c) == 3]) == 4
    assert design and all(len(c) == 2 and c[1] == "j" for c in design), design
    assert set(tiers) <= TARGET.syllable.onset_set
    cc = {c for c in TARGET.syllable.onsets if len(c) == 2}
    ccc = {c for c in TARGET.syllable.onsets if len(c) == 3}
    assert norm == {("ɣ", "l"), ("ɣ", "r"), ("ɣ", "n")}
    assert cc == {c for c in native | loan | design | norm if len(c) == 2}
    assert len(ccc) == 7
    # every consonant but /ŋ/ is a singleton onset (digest §2 line 166)
    singles = {c[0] for c in TARGET.syllable.onsets if len(c) == 1}
    consonants = {s for s in TARGET.inventory if TABLE.value(s, "syllabic") == "-"}
    assert singles == consonants - {"ŋ"}


def test_coda_lists_exclude_h_and_include_the_digest_tables():
    """digest §2 lines 244–264 (Tables 1–4) and line 324 (/h/ barred from codas)."""
    codas = TARGET.syllable.coda_set
    assert ("h",) not in codas
    for cl in "lm rm rn lf ls lp lt lk rf rs rp rt rk mp nt ŋk pt ps kt ks ft sp st sk xt".split():
        assert tuple(cl) in codas, cl
    for cl in "ln rl lb rb mb".split():
        assert tuple(cl) not in codas, cl


def test_dutch_weight_stress_is_used():
    assert TARGET.stress.procedure == "dutch-weight"
    assert "ˈ" in adapt([w("mˠat̪ˠaːnˠəx")], TARGET, TABLE).ipa


def test_epithet_slots():
    """I-39: ADJ = ACHTIG, NOUN unmapped; the diminutive allomorphs are declared (§6)."""
    assert TARGET.meta.get("epithet-ADJ") == "ACHTIG"
    assert "epithet-NOUN" not in TARGET.meta
    for name in ("ACHTIG", "IG", "TJE", "JE", "PJE", "ETJE", "KJE"):
        assert name in TARGET.epithets, name
    assert "".join(TARGET.epithets["ACHTIG"].form) == "ɑxtəx"


def test_achtig_attaches_and_devoices_the_stem_final_obstruent():
    """digest §6 row 8: -achtig is non-cohering, so *rood* → *roodachtig* [rotaxtəx]."""
    r = adapt([w("ɾˠoːd̪ˠ")], TARGET, TABLE, epithet="ACHTIG")
    assert "".join(r.words[0].segments) == "roːtɑxtəx"
    assert r.respelling == "rootachtech"


@pytest.mark.parametrize(
    "ipa,spelling,why",
    [
        ("mˠaːnˠ", "maan", "§5 step 2: long V in a closed syllable doubles the vowel letter"),
        ("mˠaːnˠə", "mane", "§5 step 2: long V in an open syllable is written single (ma-nen)"),
        ("l̪ˠat̪ˠ", "lat", "§5 step 4: no double consonant at the end of a word"),
        ("l̪ˠat̪ˠə", "latte", "§5 step 3: short V before a single intervocalic C doubles the C"),
        ("bˠoːnˠ", "boon", "§5 table: /oː/ checked = oo"),
        ("bˠoːnˠə", "bone", "§5 table: /oː/ free = o"),
        ("mˠʊsˠ", "mus", "§5 table: /ʏ/ = u (mus)"),
        ("dʲiːfˠ", "dief", "§5 table: /i/ = ie; slender onset dʲ → dj"),
    ],
)
def test_doubling_algorithm_in_the_respelling(ipa, spelling, why):
    got = adapt([w(ipa)], TARGET, TABLE).respelling
    assert got == spelling.replace("dief", "djief"), why


def test_respelling_of_the_dutch_specific_letters():
    """§5 "Phoneme → spelling": ɣ→g, x→ch, ʋ→w, u→oe, øː→eu, ɛi→ei, œy→ui, ɔu→ou, ŋ→ng."""

    def sp(ipa):
        return adapt([w(ipa)], TARGET, TABLE).respelling

    assert sp("ɣaːl̪ˠ") == "gaal"
    assert sp("bˠɔx") == "boch"
    assert sp("waːl̪ˠ") == "waal"
    assert sp("bˠuːk") == "boek"
    assert sp("bˠəil̪ˠ") == "beil"  # Irish /əi/ → Dutch /ɛi/ (§8.3 line 986)
    assert sp("bˠəul̪ˠ") == "boul"  # Irish /əu/ → Dutch /ɔu/
    assert sp("ɾˠɪŋ") == "ring"


# ---- I-27 repair table (review-opus §F, digest line refs) ---------------------------------------

DUTCH_REPAIRS = [
    ("mɛlk", "mɛlək", "§3.2 line 457 — melk, schwa epenthesis"),
    ("kɑlm", "kɑləm", "§3.2 line 456 — kalm"),
    ("hɛrfst", "hɛrəfst", "§3.2 line 457/470 — herfst DOES epenthesize (R20b)"),
    ("hɑls", "hɑls", "§3.2 line 465 — hals blocks (homorganic)"),
    ("hɑrt", "hɑrt", "§3.2 line 467 — hart blocks (coronal C2)"),
    ("hɑnd", "hɑnt", "§3.5 line 363/561 — hand, final devoicing"),
    ("ett", "et", "§2 lines 353-355 — eet, degemination (repeated segments, I-2)"),
    ("ɡroːttə", "ɡroːtə", "§2 lines 353-355 — grootte"),
    ("bɑːx", "bɑːɣ", "§8.6 line 308 — bách, tense-V + voiceless fricative (design 9.18)"),
    ("hoːrn", "hoːrən", "§3.2 line 458 — hoorn: r + n is NOT homorganic, epenthesis applies"),
    ("kɑft", "kɑft", "§3.2 line 470 — kaft: no schwa inside a consonant + appendix"),
]


@pytest.mark.parametrize("before,after,cite", DUTCH_REPAIRS)
def test_repair_table(before, after, cite):
    assert repair(syllabify(w(before), TARGET, TABLE), TARGET, TABLE).ipa(marks=False) == after, (
        cite
    )


def test_matanach_control_row():
    """The §8.6 worked derivation A, lines 1050–1069 — the ban's non-trigger control.
    Segmentally [mɑtaːnəx] (line 1057); under the re-stress policy (decision 9.17,
    dutch-weight) the schwa blocks final stress and the penult is stressed, [mɑˈtaːnəx]
    (line 1064); romanized with the doubled consonant keeping σ1 short, ⟨Mattanech⟩
    (line 1066)."""
    r = adapt([w("ˈmˠat̪ˠaːn̪ˠəx")], TARGET, TABLE)
    assert "".join(r.words[0].segments) == "mɑtaːnəx"
    assert r.ipa.replace(".", "") == "mɑˈtaːnəx"
    assert r.respelling == "mattanech"
    assert "UNREPAIRED" not in r.flags
    assert not [t for t in r.trace if t.stage == "fallback"]  # no inventory fallback fired


def test_lasairchos_control_row():
    """§8.6 derivation B, lines 1071–1086: /rx/ is heterosyllabic, so no schwa epenthesis;
    initial stress retained there, but decision 9.17 re-stresses: the schwa syllable blocks
    itself and the closed penult /sər/ ... — the segmental form [lɑsərxɔs] is the claim."""
    r = adapt([w("ˈl̪ˠasˠəɾʲxɔsˠ")], TARGET, TABLE)
    assert "".join(r.words[0].segments) == "lɑsərxɔs"
    assert "UNREPAIRED" not in r.flags


# ---- regression (I-25 Mode C and Mode E) --------------------------------------------------------


def test_row_accounting():
    """I-25: 90 rows, 67 with target_ipa, 32 with both sides. The 32 two-sided rows go to
    Mode E (or the error bucket when the ENGLISH source side does not tokenize), so Mode C's
    denominator is the remaining 35 minus its own errors — not the plan's "≥ 61", which
    forgot to subtract the Mode E rows."""
    rep = run_regression("dutch", TABLE)
    c = rep.counts()
    assert c["skip"] == 23 and c["C"] + c["E"] + c["error"] == 67, rep.summary()
    two_sided = [r for r in rep.rows if r.source_ipa.strip() and r.target_ipa.strip()]
    assert len(two_sided) == 32 and all(r.mode in ("E", "error") for r in two_sided)


def test_regression_meets_the_bar():
    """Mode C >= 27/35 = 0.7714, ratchet-held (tests/ratchets/dutch.json).

    RESTATED 2026-08-25 by owner decision. The plan's Task 26 bar was ">= 0.80 over >= 61
    rows", whose denominator forgot to subtract the 32 Mode E rows (see test_row_accounting).
    Against the real 35-row denominator the remaining 8 failures are all excluded by
    decisions 9.17/9.18: 7 are French loans with lexical FINAL stress (digest §4 lines
    691-696, *anarchie* [ɑ.nɑr.ˈxi]) which the dutch-weight procedure cannot reproduce
    without keep-source, and *roos* [roːs] fails the word-final tense-V + voiceless-fricative
    ban (the 9.18 repair is ordered after final devoicing, so the file predicts [roːz])."""
    rep = run_regression("dutch", TABLE)
    assert rep.rate("C") >= 0.7714, rep.summary()


def test_regression_measured_rate():
    """The failing Mode C rows behind the restated bar above: every one is either a French
    final-stress loan or the one attested surface form the word-final pact ban rejects."""
    rep = run_regression("dutch", TABLE)
    assert rep.rate("C") >= 0.77, rep.summary()
    failing = {r.target_ipa for r in rep.rows if r.mode == "C" and not r.passed}
    assert failing <= {
        "ɑ.lə.ɣo.ˈri",
        "ɑ.nɑr.ˈxi",
        "ɑ.na.to.ˈmi",
        "e.nɛr.ˈʒi",
        "me.laŋ.xo.ˈli",
        "pro.fe.ˈsi",
        "ɛn.si.klo.pe.ˈdi",
        "roːs",
    }, failing


def test_mode_e_meets_the_bar():
    """Mode E >= 4/26 = 0.1538, ratchet-held (tests/ratchets/dutch.json).

    RESTATED 2026-08-25 by owner decision. The plan's ">= 0.25" was structurally
    unreachable: 9 of the 26 tokenizable rows carry the English infinitive particle *tu:*
    against a Dutch -en form, 6 keep Netherlandic short `e o` for /eː oː/, and the rest are
    score-2 loans reproduced with English phonology (digest §3.4 lines 530-535). The plan's
    own note applies — "the ratchet, not the absolute number, is the value"."""
    rep = run_regression("dutch", TABLE)
    assert rep.rate("E") >= 0.1538, rep.summary()


def test_error_bucket_is_small():
    """Plan cap: ≤ 6 (10% of 67). Every error is an untokenizable SOURCE-side English symbol
    (ʌ ×4, ɒ, the t̯ diacritic): features.tsv (Task 1b) has no rows for them. The French
    nasal œ̃ of *parfum* tokenizes (Belgian speakers keep it, digest §3.2.1 via nagy2008)."""
    rep = run_regression("dutch", TABLE)
    errors = [r for r in rep.rows if r.mode == "error"]
    assert len(errors) <= 6, rep.summary()
    assert {r.reason[0] for r in errors} <= set("ʌɒ̯"), [r.reason for r in errors]


def test_ratchet_does_not_slip():
    assert_ratchet(run_regression("dutch", TABLE))


def test_vowel_mapping_rules_are_design_not_fallback():
    """The explicit Irish→Dutch vowel mappings (spec §7 "F table") are deliberate, cited rules;
    `%fallback` is reserved for the engine's nearest-segment guess, so the fallbacks column
    means "the engine guessed" (owner review of the Dutch gallery, 2026-08-27)."""
    subs = TARGET.sections["substitute"]
    assert not [r for r in subs if r.tag == "fallback"]
