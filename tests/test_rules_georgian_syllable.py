"""Plan Task 23b: `georgian.rules` — syllable whitelists, bans, repair (digest §2, §3.6, §3.7;
spec §12.B/D/E). Written before the rule block (spec §12.I). The full-pipeline tests of the
common set live here rather than in Task 23a's file because they need a real `[syllable]`.
"""

import subprocess
import sys

import pytest
from helpers import ROOT, TABLE, entry_of, irish, read_allow_file_for, read_test_words, target, w

from strands.inputs import Entry
from strands.pipeline import adapt, run_entry
from strands.regress import assert_ratchet, run_regression
from strands.repair import repair
from strands.syllabify import legal_onset, syllabify

TARGET = target("georgian")
IRISH = irish()


def cl(ipa: str) -> tuple[str, ...]:
    """A cluster string -> segment tuple (multi-character segments: tʃʰ, dz, kʼ …)."""
    return w(ipa).segments


# ---- harmonic clusters (digest §2.2 table (53) [butskhrikidze2002 p.103]) ----------------------

# The 32 of table (53) minus `zg` / `žg` (S8: "almost unattested", `zg` marked impossible in
# table (62) p.110). Her notation -> IPA per §2.0: t = tʰ, p = pʰ, k = kʰ, c = ts (the chart's
# spelling, features.tsv has no tsʰ row), č = tʃʰ, j = dz, ǰ = dʒ, γ = ɣ, χ' = qʼ.
HARMONIC = [
    "bɡ",
    "dɡ",
    "dzɡ",
    "dʒɡ",  # voiced + velar stop
    "pʰkʰ",
    "tʰkʰ",
    "tskʰ",
    "tʃʰkʰ",
    "skʰ",
    "ʃkʰ",  # aspirated + velar stop
    "pʼkʼ",
    "tʼkʼ",
    "tsʼkʼ",
    "tʃʼkʼ",  # ejective + velar stop
    "bɣ",
    "dɣ",
    "dzɣ",
    "dʒɣ",
    "zɣ",
    "ʒɣ",  # voiced + dorsal fricative
    "pʰx",
    "tʰx",
    "tsx",
    "tʃʰx",
    "sx",
    "ʃx",  # aspirated + dorsal fricative
    "pʼqʼ",
    "tʼqʼ",
    "tsʼqʼ",
    "tʃʼqʼ",  # ejective + uvular
]


def test_harmonic_list_has_thirty_members():
    assert len(HARMONIC) == 30 and len(set(HARMONIC)) == 30


@pytest.mark.parametrize("cluster", HARMONIC)
def test_harmonic_clusters_are_licit_onsets(cluster):
    assert legal_onset(cl(cluster), TARGET.syllable, TABLE), cluster


def test_zg_and_zhg_are_excluded_deliberately():
    """S8: §2.6's co-occurrence table marks zg impossible; n.20 p.103 calls both unattested."""
    assert not legal_onset(("z", "ɡ"), TARGET.syllable, TABLE)
    assert not legal_onset(("ʒ", "ɡ"), TARGET.syllable, TABLE)


# ---- Appendix 2 / Appendix 3 extraction (digest §2.3, §2.5; R29) --------------------------------


def _script_output(*flags: str) -> str:
    return subprocess.run(
        [
            sys.executable,
            str(ROOT / "rules" / "extract_georgian_clusters.py"),
            str(ROOT / "sources" / "georgian" / "digest.md"),
            *flags,
        ],
        capture_output=True,
        text=True,
        check=True,
    ).stdout


def test_appendix_2_extraction_is_reproducible():
    """The committed onset/coda lists contain everything the script extracts."""
    out = _script_output()
    committed = {"".join(c) for c in TARGET.syllable.onsets} | {
        "".join(c) for c in TARGET.syllable.codas
    }
    assert set(out.split()) <= committed, sorted(set(out.split()) - committed)


def test_extraction_is_sectioned_and_the_onset_half_is_committed_as_onsets():
    out = _script_output("--sections")
    onsets, codas = set(), set()
    for line in out.splitlines():
        kind, _, cluster = line.partition("\t")
        (onsets if kind == "onset" else codas).add(cluster)
    assert onsets <= {"".join(c) for c in TARGET.syllable.onsets}, sorted(
        onsets - {"".join(c) for c in TARGET.syllable.onsets}
    )
    assert codas <= {"".join(c) for c in TARGET.syllable.codas}, sorted(
        codas - {"".join(c) for c in TARGET.syllable.codas}
    )
    # digest §2.3 sizes: "~150 two-member, ~60 three-member, ~21 four-member, 1 five, 2 six"
    by_len = {}
    for c in onsets:
        by_len.setdefault(len(cl(c)), set()).add(c)
    assert len(by_len[3]) >= 60 and len(by_len[4]) >= 21
    # her `c'vrtn prckvn brdγvn` (t = /tʰ/, c = /ts/, k = /kʰ/, γ = /ɣ/ per §2.0)
    assert by_len[5] == {"tsʼvrtʰn"} and by_len[6] == {"pʰrtskʰvn", "brdɣvn"}
    # Appendix 3 (§2.5): the loan-only obstruent set and the four/five-member finals
    for c in ("stʼ", "ʃtʼ", "zd", "xtʼ", "ʃkʼ", "xʃ", "ɣd", "rtʰkʰl", "rtsxl", "ndʒɡvl"):
        assert c in codas, c


def test_extraction_excludes_the_never_attested_and_initial_only_sets_from_codas():
    """§2.5 p.207: `zb xp χ'p' žb rž lž lš lj` are attested in neither position; `t'b k'b xb
    tb gd xd gǰ` only stem-initially."""
    out = _script_output("--sections")
    codas = {line.split("\t")[1] for line in out.splitlines() if line.startswith("coda")}
    for c in (
        "zb",
        "xpʰ",
        "qʼpʼ",
        "ʒb",
        "rʒ",
        "lʒ",
        "lʃ",
        "ldz",
        "tʼb",
        "kʼb",
        "xb",
        "tʰb",
        "ɡd",
        "xd",
        "ɡdʒ",
    ):
        assert c not in codas, c


def test_onsets_include_singletons():
    """spec §12.D: complete sets; §2.8 p.99 every consonant is word-initial (h included)."""
    consonants = {s for s in TARGET.inventory if TABLE.value(s, "syllabic") == "-"}
    singles = {c[0] for c in TARGET.syllable.onsets if len(c) == 1}
    assert singles == consonants
    assert ("k",) not in TARGET.syllable.onsets  # plain /k/ is not Georgian
    assert ("kʰ",) in TARGET.syllable.onsets and ("kʼ",) in TARGET.syllable.onsets


def test_codas_include_every_consonant_but_h():
    """§2.5 p.99: 'the stem can end in any of the 27 consonants (i.e. except /h/)'."""
    consonants = {s for s in TARGET.inventory if TABLE.value(s, "syllabic") == "-"}
    singles = {c[0] for c in TARGET.syllable.codas if len(c) == 1}
    assert singles == consonants - {"h"}


def test_stem_domain_is_used():
    assert TARGET.syllable.domain == "stem"
    assert TARGET.syllable.template is None  # §2.1: no syllable template
    assert TARGET.syllable.sonority is False  # §2.7 (I-13)
    assert TARGET.syllable.nuclei == ()  # §2.9 / spec §12.B hiatus


def test_h_is_barred_from_clusters():
    """§2.8 p.87: /h/ 'never occurs in consonant sequences'."""
    assert not any("h" in c for c in TARGET.syllable.onsets if len(c) > 1)
    assert not any("h" in c for c in TARGET.syllable.codas)


def test_a_geminate_interlude_is_marked_by_the_bans():
    """§2.10 n.18: no geminates; an interlude t.t would otherwise parse as coda + onset."""
    out = syllabify(w("ɑtʼtʼɑ"), TARGET, TABLE)
    assert out.illegal, out


def test_same_place_labial_obstruents_are_banned_in_sequence():
    """§2.6 p.102: "Obstruents with identical place of articulation never combine" (*bp, *pv).
    The nasal is NOT in the ban: the digest's own *mb is contradicted by Appendix 2's `bm`
    (§2.3) and by the attested loans *Cambridge, Hamburg, Istanbul* (§7), which keep /mb/."""
    assert syllabify(w("ɑbpʰɑ"), TARGET, TABLE).illegal
    assert syllabify(w("ɑpʰvɑ"), TARGET, TABLE).illegal
    assert not syllabify(w("ɑmbɑ"), TARGET, TABLE).illegal
    assert not syllabify(w("ɑmɑ"), TARGET, TABLE).illegal


def test_bans_are_checked_against_the_attested_loans():
    """Each ban is a categorical §2.6/§2.7 statement that the §3.7 loan data do not contradict;
    the dorsal-pair and /h/-in-cluster restrictions are deliberately NOT bans (§3.7 *background*
    /bɛkʼɡraundi/ keeps /kʼɡ/; §7 *Beethoven, Stockholm* keep /tʰh kʼh/)."""
    for ipa in ("bɛkʼɡrɑundi", "bɛtʰhɔvɛni", "stʼɔkʼhɔlmi", "hɑmburɡi"):
        assert syllabify(w(ipa), TARGET, TABLE).illegal == frozenset(), ipa
    assert syllabify(w("ɑrlnɑ"), TARGET, TABLE).illegal  # §2.7 three sonorants
    assert syllabify(w("ɑdtsɑ"), TARGET, TABLE).illegal  # §2.6 p.86 *dc
    assert syllabify(w("ɑtsʼsɑ"), TARGET, TABLE).illegal  # §2.6 p.86 *c's


def test_coronal_ordering_ban():
    """§2.6 p.102: 'A posterior coronal may precede an anterior coronal, but never follow it.'"""
    assert syllabify(w("ɑʃtʰɑ"), TARGET, TABLE).illegal == frozenset()
    assert syllabify(w("ɑtʰʃɑ"), TARGET, TABLE).illegal


def test_attested_loan_interludes_parse():
    """§3.7: nst (Instagram), kʼɡr (background), ndʒ (Cambridge) are licensed by §2 lists."""
    for ipa in ("instʼɑɡrɑmi", "bɛkʼɡrɑundi", "kʼɛmbridʒi", "snɛkʼi", "spʼikʼɛri"):
        out = syllabify(w(ipa), TARGET, TABLE)
        assert out.illegal == frozenset(), (ipa, out)


# ---- I-27 repair table — Georgian's only attested repair is degemination (review-opus §F) ------
# Geminates are repeated segments, never `ː` (I-2).
GEORGIAN_REPAIRS = [
    ("tʼvitʼtʼɛri", "tʼvitʼɛri", "digest §3.6 line 989 (Twitter, attested.tsv row 4)"),
    ("pʼazzli", "pʼazli", "digest line 948/989/1006 (puzzle, row 16)"),
    ("ʃɔpʼpʼinɡi", "ʃɔpʼinɡi", "digest line 879/989 (shopping, row 18)"),
    ("alɛɡɡoria", "alɛɡoria", "digest line 992 (native)"),
    ("kʼllasi", "kʼlasi", "digest line 992 (native)"),
]


@pytest.mark.parametrize("before,after,cite", GEORGIAN_REPAIRS)
def test_repair_table(before, after, cite):
    got = repair(syllabify(w(before), TARGET, TABLE), TARGET, TABLE)
    assert got.ipa(marks=False) == after, cite


def test_degemination_is_attested_and_exceptionless():
    """§3.6: every degemination line is %attested; every consonant but /h/ has one."""
    rules = [
        r
        for r in TARGET.sections["repair"]
        if len(r.target) == 2
        and r.target[0].kind == "segment"
        and r.target[0].value == r.target[1].value
    ]
    assert {r.target[0].value for r in rules} == {
        s for s in TARGET.inventory if TABLE.value(s, "syllabic") == "-"
    } - {"h"}
    assert all(r.tag == "attested" for r in rules), [
        r.rule_id for r in rules if r.tag != "attested"
    ]


def test_cluster_repair_is_declined_rather_than_synthesised():
    """§3.7 lines 999-1027: no cluster repair is observed in the data. Under the owner
    decision of 2026-08-25 the file therefore declines to repair at all (`keep`) instead of
    substituting a synthetic nearest cluster, and undoes the Cʷ overlay first."""
    assert TARGET.cluster_fallback == "keep"
    assert TARGET.overlay_undo == "v"


def test_an_unlicensed_onset_is_kept_intact_and_flagged():
    """/hr/ is barred (§2.8 p.87: /h/ never in a sequence). §3.7 — Georgian imports the
    foreign cluster rather than fixing it, so /hr/ survives, flagged and free of charge."""
    out = adapt([w("hɾˠaː")], TARGET, TABLE)
    assert "UNREPAIRED" not in out.flags
    assert out.words[0].segments[:2] == ("h", "r")
    assert not legal_onset(out.words[0].segments[:2], TARGET.syllable, TABLE)
    assert "UNATTESTED_CLUSTER:hr" in out.flags
    assert out.fallbacks == 0
    assert not any(t.rule_id == "cluster-fallback" for t in out.words[0].trace)


def test_the_temporary_syllable_block_from_23a_is_gone():
    assert TARGET.syllable.onsets is not None and TARGET.syllable.codas is not None
    assert "TEMPORARY" not in (ROOT / "rules" / "georgian.rules").read_text(encoding="utf-8")


# ---- the full-pipeline tests, moved here from 23a (fix 2): they need [syllable] ------------


def test_rule_file_parses_and_checks_clean():
    from strands.check import check_rule_file

    errs = [e for e in check_rule_file(TARGET, TABLE) if e.severity == "error"]
    assert errs == [], errs


def test_diphthongs_become_hiatus():
    """§12.B: Georgian declares no `nuclei`, so /iə/ is two syllables."""
    assert len(adapt([w("ciəɾˠə")], TARGET, TABLE).words[0].syllables) >= 3


def test_stress_is_initial_and_the_ipa_carries_no_mark():
    r = adapt([w("mˠat̪ˠaːnˠəx")], TARGET, TABLE)
    assert r.words[0].stress == 0 and "ˈ" not in r.ipa  # §4.3, [stress] mark = off


def test_common_noun_epithets_keep_the_nominative_i():
    r = run_entry(Entry("cos", ipa="kosˠ"), "DESC+NOUN", IRISH, TARGET, TABLE)
    assert r.respelling.endswith("i")


def test_mutation_output_segments_all_survive():
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
    assert set(bad) <= read_allow_file_for("georgian"), sorted(bad)


def test_regression_and_ratchet():
    rep = run_regression("georgian", TABLE)
    assert rep.rate("C") >= 0.80, rep.summary()
    assert rep.mode_e_is_empty()
    assert_ratchet(rep)


def test_error_bucket_is_small():
    """Plan cap: ≤ 15% of the 122 rows with target_ipa after the I-36 cleaning pass."""
    rep = run_regression("georgian", TABLE)
    with_ipa = [r for r in rep.rows if r.target_ipa.strip()]
    assert rep.counts().get("error", 0) <= 0.15 * len(with_ipa), rep.summary()


# ---- the Cʷ rule needs the Irish broad dorsals to reach it unchanged ---------------------


def _desc(ortho, ipa):
    from strands.inputs import infer

    return run_entry(infer(Entry(ortho, ipa=ipa), IRISH, TABLE), "DESC", IRISH, TARGET, TABLE)


@pytest.mark.parametrize("ortho,ipa", [("caoin", "kiːnʲ"), ("gaoth", "ɡiː"), ("Ciara", "ˈkɪə.ɾˠə")])
def test_a_broad_dorsal_before_a_front_vowel_gets_the_epenthetic_v(ortho, ipa):
    """`k ɡ` are broad by convention, so [normalize] leaves them plain and the Cʷ rule
    `0 -> v / [BROAD -labial] _ [V +front]` fires. Before the fix, [normalize] turned them
    into `c ɟ` from the following vowel and the Cʷ rule never saw a broad dorsal."""
    segs = _desc(ortho, ipa).words[0].segments
    assert "v" in segs, segs
    assert segs[1] == "v", segs


def test_a_broad_labial_before_a_front_vowel_does_not_get_v():
    """The Cʷ rule excludes labials (§1.6): *buí* /bˠiː/ stays plain."""
    segs = _desc("buí", "bˠiː").words[0].segments
    assert "v" not in segs, segs


# ---- owner decision 2026-08-25: Georgian keeps unattested clusters (digest §3.7) ---------------


def _desc_by_ortho(ortho: str) -> list[str]:
    """Every test-words row with this orthography, run through DESC, as respellings."""
    rows = [r for r in read_test_words() if r["orthography"] == ortho]
    assert rows, ortho
    return [run_entry(entry_of(r), "DESC", IRISH, TARGET, TABLE).respelling for r in rows]


# The owner's table (2026-08-25). Left: the words whose DESC output the decision changes;
# the cluster is now kept (or the Cʷ overlay undone) instead of substituted.
CHANGED = [
    ("naomh", {"niv"}),  # nv -> the overlay v is undone, not repaired to dv
    ("ndroim", {"nrvim"}),  # nrv: undoing v leaves nr, also unlicensed, so v stays
    ("nglúin", {"nlun"}),
    ("mná", {"mra"}),
    ("mbláth", {"mla"}),
    ("shnámh", {"hnav"}),
    ("scéal", {"shk'el"}),
    # Owner's table says `shch'rik` / `berch'`; the engine's IPA is exactly that
    # (/ʃtʃʼrikʰ/, /bɛrtʃʼ/) — the spelling differs only by the project's own D2 overlay
    # (digest §5.3 D2: ჭ /tʃʼ/ is `tch`, not national `ch'`, after the canon name Tchaeul).
    ("stríoc", {"shtchrik"}),
    ("beirt", {"bertch"}),
    ("dorn", {"dorn"}),
    ("dhorn", {"ghorn"}),
]

# Controls: the decision must not move these.
UNCHANGED = [
    ("Ciara", {"kviara", "kiara"}),
    ("Seán", {"shian"}),
    ("Gaelach", {"gvelax"}),
    ("taoiseach", {"tvishiax"}),
    ("Saoirse", {"svirshia"}),
    ("Lasairchos", {"lasarxos"}),
    ("Matánach", {"matanax"}),
    # Two words (spec §3): each is adapted on its own, so /t̪ˠ/ is WORD-INITIAL and
    # takes the aspirated `t` of §9.4, not the ejective the merged `ant'ul` parse gave it.
    ("an tsúil", {"an tul"}),
    ("sneachta", {"shniaxt'a"}),
    ("droim", {"drvim"}),  # `drv` is licensed, so overlay-undo never fires
    ("splanc", {"sp'lank'"}),
    ("spraoi", {"sp'rvi"}),
]


@pytest.mark.parametrize("ortho,expected", CHANGED + UNCHANGED)
def test_desc_matches_the_owner_table(ortho, expected):
    assert set(_desc_by_ortho(ortho)) == expected


def test_a_kept_cluster_is_flagged_and_costs_no_fallback():
    rows = [r for r in read_test_words() if r["orthography"] == "shnámh"]
    r = run_entry(entry_of(rows[0]), "DESC", IRISH, TARGET, TABLE)
    assert "UNATTESTED_CLUSTER:hn" in r.flags
    assert r.fallbacks == 0
    assert not any(t.rule_id == "cluster-fallback" for t in r.trace)


def test_the_overlay_undo_is_traced_on_naomh():
    rows = [r for r in read_test_words() if r["orthography"] == "naomh"]
    r = run_entry(entry_of(rows[0]), "DESC", IRISH, TARGET, TABLE)
    assert any(t.rule_id == "overlay-undo" and t.stage == "repair" for t in r.trace)
