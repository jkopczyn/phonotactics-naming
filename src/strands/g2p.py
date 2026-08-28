"""Provisional Irish grapheme-to-phoneme (spec §5, milestone 8).

`g2p(orthography, dialect)` turns modern Irish spelling into an IPA string in this project's
convention, for input rows whose `ipa` cell is empty (the owner does not write IPA). It is a
*provisional* reader, not a lexicon: every block below is a transcription of a published table,
and where the sources disagree or a form is idiosyncratic the walk records a note instead of
guessing silently. `inputs.infer()` stores the result as `ipa` and tags the row
`ipa:constructed`, so a constructed transcription is always distinguishable from a hand one.

Everything is data. Four tables do the work, each citing the source it is copied from:

* `_CONSONANTS`      — the ⟨letter(s)⟩ → phoneme table, keyed by grapheme and quality
                       [wiki-irish-orthography §Grapheme to phoneme correspondence, consonants].
* `_VOWELS`          — the vowel digraph/trigraph table, base value plus context overrides
                       [ibid., §Vowels]; the Connacht ("C") column is the one taken.
* `_VOWEL_PLUS_H`    — short vowel + ⟨bh dh gh mh⟩ [ibid., §Short vowels followed by ⟨bh, dh,
                       gh, mh⟩].
* `_EPENTHESIS`      — sonorant + labial/dorsal, digest §2.4 [wiki-irish-phonology
                       §Post-vocalic consonant clusters and epenthesis; green1997 p.152].

Consonant quality (digest §5.1, *caol le caol agus leathan le leathan*) is read off the
flanking vowel LETTERS: slender beside ⟨e é i í⟩, broad beside ⟨a á o ó u ú⟩. A consonant run
takes the quality of the preceding vowel run's last letter, or — word-initially, where there is
no preceding vowel — of the following vowel run's first letter. ⟨ae⟩ is the stated exception:
it is followed by a broad consonant despite the ⟨e⟩ [wiki-irish-orthography §Vowels].

Stress (digest §4.1): initial for Connacht (dialect `C`, the default) and Ulster; the
weight-attracted Munster rule (σ2 if heavy, else σ3 if heavy and σ2 light, else σ1, plus the
/ax/ attraction of *bacach* /bˠəˈkax/) only when dialect `M` is asked for. Unstressed short
vowels reduce to /ə/; long vowels and diphthongs do not (Connacht tolerates an unstressed long
vowel, digest §4.2), so *-án* keeps its /aː/ and *-ach* comes out /əx/.

Known limits, reported as notes rather than hidden: lexical noninitial stress (*tobac*
/təˈbak/) is not predicted; the ⟨l n⟩ fortis/lenis choice follows the Wikipedia positional
statement, which its own examples do not apply consistently; sandhi between words is not
modelled.
"""

from __future__ import annotations

import unicodedata

__all__ = ["g2p", "G2PError"]


class G2PError(ValueError):
    """The orthography cannot be read (empty, or contains no letter this table knows)."""


# ---- letters ---------------------------------------------------------------------------------

_SLENDER_LETTERS = frozenset("eéií")
_BROAD_LETTERS = frozenset("aáoóuú")
_VOWEL_LETTERS = _SLENDER_LETTERS | _BROAD_LETTERS
_LONG_LETTERS = frozenset("áéíóú")

# Proclitics: the article, the particles and the possessives. They are never stressed and their
# short vowel reduces — *an tsúil* /ən̪ˠ t̪ˠuːlʲ/, *na héisc* /n̪ˠə heːʃc/, *a Sheáin* /ə çaːnʲ/
# [wiki-irish-orthography §Grapheme to phoneme correspondence; digest §3.4].
_PROCLITICS = frozenset({"an", "na", "a", "ar", "mo", "do", "go", "le", "ba", "is", "ná", "nach"})
# The three whose shape the sources give outright: *an tsolais* /ə(n̪ˠ) ˈt̪ˠɔlˠəʃ/, *na héisc*
# /n̪ˠə heːʃc/, *a Sheáin* /ə çaːnʲ/ [wiki-irish-orthography §Grapheme to phoneme
# correspondence; wiki-irish-phonology §Vowel backness]. The fortis /n̪ˠ/ is what the article
# has in every attested row, where the positional rule of `_liquid` would give lenis.
_PROCLITIC_IPA = {"an": "ən̪ˠ", "na": "n̪ˠə", "a": "ə", "mo": "mˠə"}

# ---- the consonant table ---------------------------------------------------------------------
# [wiki-irish-orthography §Grapheme to phoneme correspondence], consonant rows, Connacht column.
# Value: (broad, slender). `None` means "silent". Longest match wins inside a consonant run.
_CONSONANTS: dict[str, tuple[str, str]] = {
    "bhf": ("w", "vʲ"),  # eclipsis of ⟨f⟩: bhfuinneog /ˈwɪn̠ʲoːɡ/, bhfíon /vʲiːnˠ/
    "bh": ("w", "vʲ"),  # bhain /wanʲ/, bhéal /vʲeːlˠ/
    "mh": ("w", "vʲ"),  # mhór /woːɾˠ/, mhilis /ˈvʲɪlʲəʃ/
    "ph": ("fˠ", "fʲ"),  # pholl /fˠoːl̪ˠ/, phríosún /ˈfʲɾʲiːsˠuːnˠ/
    "ch": ("x", "ç"),  # cháis /xaːʃ/, cheist /çɛʃtʲ/
    "fh": (None, None),  # fhuinneog /ˈɪn̠ʲoːɡ/ — silent
    "b": ("bˠ", "bʲ"),
    "c": ("k", "c"),
    "d": ("d̪ˠ", "dʲ"),
    "f": ("fˠ", "fʲ"),
    "g": ("ɡ", "ɟ"),
    "h": ("h", "h"),  # hata /ˈhat̪ˠə/, na héisc /n̪ˠə heːʃc/
    "j": ("dʒ", "dʒ"),  # loan consonant
    "k": ("k", "c"),
    "ll": ("l̪ˠ", "l̠ʲ"),  # poll /pˠoːl̪ˠ/, coill /kəil̠ʲ/
    "m": ("mˠ", "mʲ"),
    "nn": ("n̪ˠ", "n̠ʲ"),  # ceann /caːn̪ˠ/, tinneas /ˈtʲɪn̠ʲəsˠ/
    "p": ("pˠ", "pʲ"),
    "rr": ("ɾˠ", "ɾˠ"),  # carr /kaːɾˠ/
    "t": ("t̪ˠ", "tʲ"),
    "v": ("w", "vʲ"),  # loan consonant: vóta /ˈwoːt̪ˠə/, veidhlín /ˈvʲəilʲiːnʲ/
    "w": ("w", "vʲ"),
    "z": ("zˠ", "ʒ"),  # loan consonant
}

# Word-initial eclipsis digraphs [wiki-irish-mutations §Summary table; wiki-irish-orthography].
_ECLIPSIS_INITIAL: dict[str, tuple[str, str]] = {
    "mb": ("mˠ", "mʲ"),  # mbaineann /ˈmˠanʲən̪ˠ/, mbéal /mʲeːlˠ/
    "nd": ("n̪ˠ", "n̠ʲ"),  # ndorn /n̪ˠoːɾˠn̪ˠ/, ndearg /ˈn̠ʲaɾˠəɡ/
    "bp": ("bˠ", "bʲ"),  # bpoll /bˠoːl̪ˠ/, bpríosún /ˈbʲɾʲiːsˠuːnˠ/
    "dt": ("d̪ˠ", "dʲ"),  # dtaisce /ˈd̪ˠaʃcə/, dtír /dʲiːɾʲ/
    "gc": ("ɡ", "ɟ"),  # gcáis /ɡaːʃ/, gceist /ɟɛʃtʲ/
    "ng": ("ŋ", "ɲ"),  # ngasúr /ˈŋasˠuːɾˠ/, ngeata /ˈɲat̪ˠə/
    "ts": ("t̪ˠ", "tʲ"),  # an tsolais /ə(n̪ˠ) ˈt̪ˠɔlˠəʃ/, an tSín /ə(nʲ) tʲiːnʲ/
}

# ---- the vowel table -------------------------------------------------------------------------
# [wiki-irish-orthography §Vowels], Connacht column. Each entry is (default, overrides), where
# an override is (condition-name, value) tested in order against the FOLLOWING consonant run.
# Condition names are implemented in `_vowel_value`.
_LONG_OR_DIPH = frozenset({"iː", "eː", "aː", "oː", "uː", "iə", "uə", "əi", "əu"})

_VOWELS: dict[str, tuple[str, tuple[tuple[str, str], ...]]] = {
    # a, ea: fan /fˠanˠ/, bean /bʲanˠ/; garda /ˈɡaːɾˠd̪ˠə/; mall /mˠaːl̪ˠ/, am /aːmˠ/
    "a": ("a", (("rd", "aː"), ("llnn_m", "aː"))),
    "ea": ("a", (("rd", "aː"), ("llnn_m", "aː"))),
    "ai": ("a", (("rd", "aː"), ("llnn", "aː"))),  # airne /aːɾˠn̠ʲə/, crainn /kɾˠaːn̠ʲ/
    "eai": ("a", (("rd", "aː"), ("llnn", "aː"))),
    "á": ("aː", ()),
    "ái": ("aː", ()),  # bán /bˠaːnˠ/, dáil /d̪ˠaːlʲ/
    "eá": ("aː", ()),
    "eái": ("aː", ()),  # Seán /ʃaːnˠ/, caisleán /ˈkaʃl̠ʲaːnˠ/
    "ae": ("eː", ()),
    "aei": ("eː", ()),  # Gaelach /ˈɡeːlˠəx/
    "aí": ("iː", ()),
    "aío": ("iː", ()),  # gutaí /ˈɡʊt̪ˠiː/
    "ao": ("iː", ()),  # saol /sˠiːlˠ/, an tsaoil /ən̪ˠ t̪ˠiːlʲ/
    "aoi": ("iː", ()),  # gaois /ɡiːʃ/, naoi /ˈn̪ˠiː/
    # e, ei: te /tʲɛ/, ceist /cɛʃtʲ/; eirleach /ˈeːɾˠl̠ʲəx/; creimeadh /ˈcɾʲɪmʲə/; greim /ɟɾʲiːmʲ/
    "e": ("ɛ", (("rd", "eː"), ("nn_m", "iː"), ("mmhn", "ɪ"))),
    "ei": ("ɛ", (("rd", "eː"), ("nn_m", "iː"), ("mmhn", "ɪ"))),
    "é": ("eː", ()),
    "éa": ("eː", ()),
    "éi": ("eː", ()),  # sé /ʃeː/, buidéal /ˈbˠɪdʲeːlˠ/
    "eo": ("oː", ()),
    "eoi": ("oː", ()),  # ceol /coːlˠ/ (the four /ɔ/ words are lexical)
    # i: pic /pʲɪc/; cill /ciːl̠ʲ/, im /iːmʲ/
    "i": ("ɪ", (("llnn_m", "iː"),)),
    "í": ("iː", ()),
    "ío": ("iː", ()),  # cailín /ˈkalʲiːnʲ/, síol /ʃiːlˠ/
    "ia": ("iə", ()),
    "iai": ("iə", ()),  # Diarmaid /dʲiərmədʲ/, bliain /bʲlʲiənʲ/
    "iá": ("iːaː", ()),
    "iái": ("iːaː", ()),  # bián /ˈbʲiːaːnˠ/
    # io: siopa /ˈʃʊpˠə/, Siobhán /ˈʃʊwaːnˠ/; fios /fʲɪsˠ/; fionn /fʲʊn̪ˠ/
    "io": ("ʊ", (("nn", "ʊ"), ("dhlnrsst", "ɪ"))),
    "ió": ("iːoː", ()),
    "iói": ("iːoː", ()),  # sióg /ˈʃiːoːɡ/
    "iu": ("ʊ", ()),  # fliuch /fʲlʲʊx/
    "iú": ("uː", ()),
    "iúi": ("uː", ()),  # siúl /ʃuːlˠ/, ciúin /cuːnʲ/
    # o: post /pˠɔsˠt̪ˠ/; bord /bˠoːɾˠd̪ˠ/; conradh /ˈkʊnˠɾˠə/; fonn /fˠuːn̪ˠ/, long /l̪ˠuːŋɡ/
    "o": ("ɔ", (("rd", "oː"), ("nn_ng", "uː"), ("nm", "ʊ"))),
    "ó": ("oː", ()),
    "ói": ("oː", ()),  # póg /pˠoːɡ/, bádóir /ˈbˠaːd̪ˠoːɾʲ/
    # oi: scoil /sˠkɛlʲ/; cois /kɔʃ/; coirnéal /ˈkoːɾˠn̠ʲeːlˠ/; anois /əˈnˠɪʃ/; droim /d̪ˠɾˠiːmʲ/
    "oi": ("ɛ", (("rd", "oː"), ("oi_back", "ɔ"), ("nn_m", "iː"), ("ll", "əi"), ("nm", "ɪ"))),
    "oí": ("iː", ()),
    "oío": ("iː", ()),  # croíonna /ˈkɾˠiːn̪ˠə/
    # u: dubh /d̪ˠʊw/; burla /ˈbˠuːɾˠl̪ˠə/
    "u": ("ʊ", (("rd", "uː"),)),
    "ú": ("uː", ()),
    "úi": ("uː", ()),  # tús /t̪ˠuːsˠ/, súil /suːlʲ/
    "ua": ("uə", ()),
    "uai": ("uə", ()),  # fuar /fˠuəɾˠ/, fuair /fˠuəɾʲ/
    "uá": ("uːaː", ()),
    "uái": ("uːaː", ()),  # ruán /ˈɾˠuːaːnˠ/
    # ui: duine /ˈd̪ˠɪnʲə/; tuirne /ˈt̪ˠuːɾˠn̠ʲə/; suim /sˠiːmʲ/
    "ui": ("ɪ", (("rd", "uː"), ("llnn_m", "iː"))),
    "uí": ("iː", ()),
    "uío": ("iː", ()),  # buíon /bˠiːnˠ/
    "uó": ("uːoː", ()),
    "uói": ("uːoː", ()),  # cruóg /ˈkɾˠuːoːɡ/
}

# ---- short vowel + ⟨bh dh gh mh⟩ ---------------------------------------------------------------
# [wiki-irish-orthography §Short vowels followed by ⟨bh, dh, gh, mh⟩], Connacht column. Key is
# (vowel run, digraph); value is (stressed, unstressed). The digraph is consumed with the vowel,
# and a vowel run immediately following it is absorbed (adharc /əiɾˠk/, deagha /d̪ˠəi/).
_VOWEL_PLUS_H: dict[tuple[str, str], tuple[str, str]] = {
    ("a", "bh"): ("əu", "əu"),
    ("ea", "bh"): ("əu", "əu"),  # Feabhra /ˈfʲəuɾˠə/
    ("a", "dh"): ("əi", "ə"),
    ("ea", "dh"): ("əi", "ə"),  # adharc /əiɾˠk/, briseadh /ˈbʲɾʲɪʃə/
    ("a", "gh"): ("əi", "ə"),
    ("ea", "gh"): ("əi", "ə"),  # meadhg /mʲəiɡ/, margadh /ˈmˠaɾˠəɡə/
    ("ai", "dh"): ("əi", "ə"),
    ("ai", "gh"): ("əi", "ə"),  # aidhleann /ˈəilʲən̪ˠ/, bacaigh
    ("a", "mh"): ("əu", "əw"),
    ("ea", "mh"): ("əu", "əw"),  # Samhain /sˠəunʲ/, creideamh /ˈcɾʲɛdʲəw/
    ("ei", "dh"): ("əi", "əi"),
    ("ei", "gh"): ("əi", "əi"),  # feidhm /fʲəimʲ/, leigheas /l̠ʲəisˠ/
    ("i", "dh"): ("iː", "ə"),
    ("i", "gh"): ("iː", "ə"),  # ligh /l̠ʲiː/, tuillidh /ˈt̪ˠɪl̠ʲiː/
    ("ui", "dh"): ("iː", "ə"),
    ("ui", "gh"): ("iː", "ə"),
    ("o", "bh"): ("əu", "əu"),
    ("o", "dh"): ("əu", "əu"),  # lobhra /ˈl̪ˠəuɾˠə/, bodhar /bˠəuɾˠ/
    ("o", "gh"): ("əu", "əu"),
    ("oi", "dh"): ("əi", "əi"),
    ("oi", "gh"): ("əi", "əi"),  # oidhre /əiɾʲə/, oigheann /əin̪ˠ/
    ("o", "mh"): ("oː", "oː"),  # Domhnach /ˈd̪ˠoːnˠəx/, comhar /koːɾˠ/
    ("u", "bh"): ("ʊw", "ʊw"),
    ("iu", "bh"): ("ʊw", "ʊw"),  # dubh /d̪ˠʊw/, tiubh /tʲʊw/
    ("u", "mh"): ("uː", "uː"),
    ("iu", "mh"): ("uː", "uː"),  # cumhra /ˈkuːɾˠə/, ciumhais /cuːʃ/
}

# ---- epenthesis ------------------------------------------------------------------------------
# digest §2.4: ∅ → ə / {ɾˠ ɾʲ l lʲ n nʲ} _ C[labial or dorsal, except the voiceless stops]
# [wiki-irish-phonology §Post-vocalic consonant clusters and epenthesis; wiki-clusterchart].
_EPEN_C1 = frozenset({"ɾˠ", "ɾʲ", "l̪ˠ", "lˠ", "lʲ", "l̠ʲ", "n̪ˠ", "nˠ", "nʲ", "n̠ʲ"})
_EPEN_C2_LIQUID = frozenset(
    {"bˠ", "bʲ", "ɡ", "ɟ", "fˠ", "fʲ", "w", "vˠ", "vʲ", "mˠ", "mʲ", "x", "ç", "ɣ", "j"}
)  # dorcha /ˈd̪ˠɔɾˠəxə/, digest §2.4
_EPEN_C2_NASAL = frozenset({"bˠ", "bʲ", "fˠ", "fʲ", "w", "vˠ", "vʲ", "mˠ", "mʲ"})  # n rows only
_EPEN_NASALS = frozenset({"n̪ˠ", "nˠ", "nʲ", "n̠ʲ"})

_BACK_VOWELS = frozenset({"a", "aː", "ɔ", "oː", "ʊ", "uː", "əu"})

_VOWEL_SEGMENTS = frozenset(
    {"a", "aː", "e", "eː", "i", "iː", "o", "oː", "u", "uː", "ɛ", "ɔ", "ɪ", "ʊ", "ə", "æ"}
)
_LONG_SEGMENTS = frozenset({"aː", "eː", "iː", "oː", "uː", "æː"})


# ---- the walk --------------------------------------------------------------------------------


def _runs(word: str) -> list[tuple[str, str]]:
    """The word as alternating ('V', letters) / ('C', letters) runs."""
    out: list[tuple[str, str]] = []
    for ch in word:
        kind = "V" if ch in _VOWEL_LETTERS else "C"
        if out and out[-1][0] == kind:
            out[-1] = (kind, out[-1][1] + ch)
        else:
            out.append((kind, ch))
    return out


def _slender(prev_v: str | None, next_v: str | None) -> bool:
    """digest §5.1, *caol le caol*: a consonant run takes the quality of the preceding vowel
    run's last letter, or word-initially of the following run's first letter. ⟨ae⟩ is the
    stated exception — broad despite the ⟨e⟩ [wiki-irish-orthography §Vowels]."""
    if prev_v:
        if prev_v == "ae":
            return False
        return prev_v[-1] in _SLENDER_LETTERS
    if next_v:
        return next_v[0] in _SLENDER_LETTERS
    return False


def _vowel_value(run: str, nxt: str | None, word_final_run: bool, notes: list[str]) -> str:
    """The stressed value of a vowel run, applying the context overrides of `_VOWELS`."""
    entry = _VOWELS.get(run)
    if entry is None:
        # An unlisted sequence: read the first two letters, then the first, so that a spelling
        # the table does not cover still produces something legal (note recorded).
        for key in (run[:2], run[:1]):
            if key in _VOWELS:
                notes.append(f"vowel-{run}-read-as-{key}")
                entry = _VOWELS[key]
                break
        else:
            raise G2PError(f"unknown vowel sequence {run!r}")
    default, overrides = entry
    c = nxt or ""
    for name, value in overrides:
        if _vowel_condition(name, c, word_final_run):
            return value
    return default


def _vowel_condition(name: str, c: str, final: bool) -> bool:
    """The named context conditions of the `_VOWELS` overrides, over the FOLLOWING letters."""
    if name == "rd":  # before ⟨rd, rl, rn, rr⟩
        return c[:2] in ("rd", "rl", "rn", "rr")
    if name == "ll":  # before syllable-final ⟨ll⟩
        return c[:2] == "ll"
    if name == "llnn":  # before syllable-final ⟨ll, nn⟩
        return c[:2] in ("ll", "nn")
    if name == "llnn_m":  # before syllable-final ⟨ll, nn⟩ and word-final -⟨m⟩
        return c[:2] in ("ll", "nn") or (final and c == "m")
    if name == "nn":  # before syllable-final ⟨nn⟩
        return c[:2] == "nn"
    if name == "nn_m":  # before syllable-final ⟨nn⟩ and word-final -⟨m⟩
        return c[:2] == "nn" or (final and c == "m")
    if name == "nn_ng":  # before syllable-final ⟨nn⟩ and word-final -⟨ng⟩. The C column
        # also lengthens before final -⟨m⟩, but the attested *chrom* /xɾˠɔmˠ/ does not.
        return c[:2] == "nn" or (final and c == "ng")
    if name == "mmhn":  # ⟨e⟩ before ⟨m, mh, n⟩
        return c[:2] == "mh" or c[:1] in ("m", "n")
    if name == "nm":  # next to ⟨m⟩, ⟨n⟩ — conradh /ˈkʊnˠɾˠə/, cromóg /ˈkɾˠʊmˠoːɡ/.
        # Not when the nasal is word-final: the attested *chrom* is /xɾˠɔmˠ/, not */xɾˠʊmˠ/.
        return c[:1] in ("m", "n") and not final
    if name == "dhlnrsst":  # ⟨io⟩ before /d h l n ɾ s ʃ t/
        return c[:1] in ("d", "h", "l", "n", "r", "s", "t")
    if name == "oi_back":  # ⟨oi⟩ before /ɾh ɾʃ ɾtʲ ʃ xtʲ/
        return c in ("rth", "rs", "rt", "s") or c[:3] == "cht"
    return False


def _consonant_segments(
    run: str, slender: bool, word: str, start: int, dialect: str, notes: list[str]
) -> list[str]:
    """One consonant run → segments, longest match first. `start` is the run's offset in the
    word, so that the "initially" rows of the table can be told apart from the rest."""
    out: list[str] = []
    i = 0
    while i < len(run):
        at_word_start = (start + i) == 0
        run_initial = start == 0
        for size in (3, 2, 1):
            g = run[i : i + size]
            if not g:
                continue
            seg = _grapheme(
                g, slender, at_word_start, run_initial, run, i, word, start + i, dialect, notes
            )
            if seg is not None:
                out.extend(seg)
                i += size
                break
        else:
            notes.append(f"unknown-letter-{run[i]}")
            i += 1
    return out


def _grapheme(
    g: str,
    slender: bool,
    at_word_start: bool,
    run_initial: bool,
    run: str,
    i: int,
    word: str,
    pos: int,
    dialect: str,
    notes: list[str],
) -> list[str] | None:
    """A single grapheme → 0..2 segments, or None when `g` is not in the tables."""
    idx = 1 if slender else 0

    # Word-initial eclipsis digraphs [wiki-irish-mutations §Summary table].
    if at_word_start and g in _ECLIPSIS_INITIAL:
        return [_ECLIPSIS_INITIAL[g][idx]]

    if g in ("dh", "gh"):
        # broad: /ɣ/ initially, silent elsewhere; slender: /j/
        # [wiki-irish-orthography §Grapheme to phoneme correspondence].
        if slender:
            return ["j"]
        return ["ɣ"] if at_word_start else []

    if g == "sh":
        # sh → /h/; as the lenition of a SLENDER /ʃ/ it is [ç] before a back vowel —
        # *a Sheáin* [ə çaːnʲ], *sheoil* [çoːlʲ] (digest §1.1 [wiki-irish-phonology §Allophones]).
        if slender and _next_nucleus(word, pos + 2) in _BACK_VOWELS:
            return ["ç"]
        return ["h"]

    if g == "th":
        # usually /h/; silent word-finally after a long vowel or diphthong (*bláth* /bˠl̪ˠaː/).
        if i + 2 == len(run) and word.endswith(run):
            prev = _prev_vowel_run(word, run)
            if prev and (set(prev) & _LONG_LETTERS or prev in ("ia", "ua", "ao", "aoi")):
                return []
        return ["h"]

    if g == "ch" and slender and run[i + 2 : i + 3] == "t":
        return ["x"]  # slender ⟨ch⟩ before ⟨t⟩ is /x/: boichte /bˠɔxtʲə/

    if g == "ng" and not at_word_start:
        return ["ŋ", "ɡ"] if not slender else ["ɲ", "ɟ"]  # long /l̪ˠuːŋɡ/, cuing /kɪɲɟ/

    if g == "nc":
        return ["ŋ", "k"] if not slender else ["ɲ", "c"]  # ancaire /ˈaŋkəɾʲə/, rinc /ɾˠɪɲc/

    if g == "dt" and not at_word_start:
        return ["t̪ˠ"] if not slender else ["tʲ"]  # greadta /ˈɟɾʲat̪ˠə/

    if g == "x":
        return ["k", "s"]

    if g in ("l", "n"):
        return _liquid(
            g,
            slender,
            at_word_start,
            run_initial,
            run,
            i,
            dialect,
            notes,
            prevocalic=i + 1 == len(run) and pos + 1 < len(word),
        )

    if g in ("r", "rr"):
        return [_rhotic(g, slender, at_word_start, run, i, word)]

    if g == "s":
        return [_sibilant(slender, at_word_start, run, i)]

    if g in _CONSONANTS:
        seg = _CONSONANTS[g][idx]
        return [] if seg is None else [seg]
    return None


def _next_nucleus(word: str, pos: int) -> str:
    """The stressed value of the next vowel run at or after `pos` ('' when there is none)."""
    while pos < len(word) and word[pos] not in _VOWEL_LETTERS:
        pos += 1
    end = pos
    while end < len(word) and word[end] in _VOWEL_LETTERS:
        end += 1
    run = word[pos:end]
    if not run:
        return ""
    entry = _VOWELS.get(run) or _VOWELS.get(run[:2]) or _VOWELS.get(run[:1])
    return entry[0] if entry else ""


def _prev_vowel_run(word: str, run: str) -> str:
    prev = ""
    for kind, text in _runs(word):
        if kind == "C" and text == run:
            return prev
        if kind == "V":
            prev = text
    return prev


def _liquid(
    g: str,
    slender: bool,
    at_word_start: bool,
    run_initial: bool,
    run: str,
    i: int,
    dialect: str,
    notes: list[str],
    prevocalic: bool = True,
) -> list[str]:
    """⟨l n⟩: fortis /l̪ˠ l̠ʲ n̪ˠ n̠ʲ/ word-initially and for ⟨ll nn⟩ [wiki-irish-orthography
    §Grapheme to phoneme correspondence]. The non-initial row of that table reads "/lˠ/ or
    /l̪ˠ/" and its own examples do not choose consistently, so the rest is PROVISIONAL and was
    settled by measuring the attested rows of test-words.tsv:

    * fortis after another consonant letter — *dorn* /d̪ˠoːɾˠn̪ˠ/, *glúin* /ɡl̪ˠuːnʲ/,
      *caisleán* /ˈkaʃl̠ʲaːnˠ/, *splanc* /sˠpˠl̪ˠaŋk/ — except ⟨n⟩ after ⟨s⟩, *sneachta*
      /ˈʃnʲaxt̪ˠə/;
    * after a vowel, lenis — *bean* /bʲanˠ/, *Gaelach* /ˈɡeːlˠəx/ — except a broad ⟨l⟩ that is
      not prevocalic, which is fortis: *Colm* /ˈkɔl̪ˠəmˠ/, *scéal* /ʃceːl̪ˠ/.

    Whole-file exact match: 0.57 with the bare Wikipedia rule, 0.47 with fortis everywhere,
    0.73 with this."""
    if g == "n" and run_initial and i > 0 and dialect == "C" and not run[:i].endswith(("s", "sh")):
        # [C] ⟨n⟩ after a non-⟨s(h)⟩ word-initial consonant is /ɾˠ ɾʲ/: mná /mˠɾˠaː/,
        # cnaipe /ˈkɾˠapʲə/ [wiki-irish-orthography]. Only inside a word-initial cluster.
        notes.append("cn-gn-mn-as-r")
        return ["ɾʲ" if slender else "ɾˠ"]
    fortis = at_word_start
    if i > 0:  # after another consonant letter in the same run
        fortis = not (g == "n" and run[:i].endswith("s"))  # sneachta /ˈʃnʲaxt̪ˠə/
    elif g == "l" and not slender and not prevocalic:
        fortis = True  # Colm /ˈkɔl̪ˠəmˠ/, dualgas /ˈd̪ˠuəl̪ˠɡəsˠ/, scéal /ʃceːl̪ˠ/
    if fortis:
        return [("l̠ʲ" if slender else "l̪ˠ") if g == "l" else ("n̠ʲ" if slender else "n̪ˠ")]
    return [("lʲ" if slender else "lˠ") if g == "l" else ("nʲ" if slender else "nˠ")]


def _rhotic(g: str, slender: bool, at_word_start: bool, run: str, i: int, word: str) -> str:
    """Broad ⟨r⟩ and ⟨rr⟩ are /ɾˠ/. Slender ⟨r⟩ is /ɾˠ/ word-initially, after ⟨s⟩, and before
    /d h l n ɾ s ʃ t/; /ɾʲ/ otherwise [wiki-irish-orthography §Grapheme to phoneme
    correspondence]."""
    if not slender or g == "rr":
        return "ɾˠ"
    if at_word_start:
        return "ɾˠ"
    if i > 0 and run[i - 1] == "s":
        return "ɾˠ"
    nxt = run[i + 1 : i + 2]
    if nxt and (nxt in "dhlnrst" or run[i + 1 : i + 3] == "th"):
        return "ɾˠ"
    return "ɾʲ"


def _sibilant(slender: bool, at_word_start: bool, run: str, i: int) -> str:
    """Slender ⟨s⟩ is /sˠ/ initially before /f m p ɾ/, /ʃ/ otherwise: speal /sˠpʲal/,
    sméar /sˠmʲeːɾˠ/ vs sean /ʃanˠ/ [wiki-irish-orthography]."""
    if not slender:
        return "sˠ"
    if at_word_start and run[i + 1 : i + 2] in ("f", "m", "p", "r"):
        return "sˠ"
    return "ʃ"


# ---- stress ----------------------------------------------------------------------------------


def _stress_index(nuclei: list[str], dialect: str, orth: str) -> int:
    """Which syllable carries primary stress (digest §4.1). Connacht/Ulster: the first.
    Munster: σ2 if heavy, else σ3 if heavy and σ2 light, else σ1; plus the /ax/ attraction
    of *bacach* /bˠəˈkax/ [wiki-irish-phonology §Munster; green1997 p.123]."""
    if dialect != "M" or len(nuclei) < 2:
        return 0
    heavy = [n in _LONG_OR_DIPH or n in ("iːaː", "uːaː", "iːoː", "uːoː") for n in nuclei]
    if heavy[1]:
        return 1
    if len(nuclei) > 2 and heavy[2]:
        return 2
    if nuclei[1] == "a" and not heavy[0] and not (len(nuclei) > 2 and heavy[2]):
        return 1
    return 0


# ---- the word --------------------------------------------------------------------------------


def _word_segments(word: str, dialect: str, notes: list[str], proclitic: bool) -> list[str]:
    runs = _runs(word)
    if not any(k == "V" for k, _ in runs):
        raise G2PError(f"{word!r}: no vowel letter")

    # Pass 1: the nuclei, read as if stressed, so that syllable weight is known before stress
    # is placed; `absorbed` marks a vowel run swallowed by a `_VOWEL_PLUS_H` match.
    v_indices = [i for i, (k, _) in enumerate(runs) if k == "V"]
    nuclei: list[str] = []
    plus_h: dict[int, tuple[str, str]] = {}  # vowel-run index -> (stressed, unstressed)
    absorbed: set[int] = set()
    for i in v_indices:
        if i in absorbed:
            continue
        nxt = runs[i + 1][1] if i + 1 < len(runs) else None
        key = (runs[i][1], (nxt or "")[:2])
        if key in _VOWEL_PLUS_H and nxt is not None:
            plus_h[i] = _VOWEL_PLUS_H[key]
            nuclei.append(_VOWEL_PLUS_H[key][0])
            if i + 2 < len(runs) and len(nxt) == 2:
                absorbed.add(i + 2)  # adharc /əiɾˠk/: the second ⟨a⟩ is not read
            continue
        nuclei.append(_vowel_value(runs[i][1], nxt, i + 2 >= len(runs), notes))
    live = [i for i in v_indices if i not in absorbed]
    stress = 0 if proclitic else _stress_index(nuclei, dialect, word)

    # Pass 2: emit.
    out: list[str] = []
    stress_at: int | None = None
    for i, (kind, text) in enumerate(runs):
        if kind == "C":
            prev_v = next((runs[j][1] for j in range(i - 1, -1, -1) if runs[j][0] == "V"), None)
            next_v = next((runs[j][1] for j in range(i + 1, len(runs)) if runs[j][0] == "V"), None)
            slen = _slender(prev_v, next_v)
            skip = 2 if (i - 1) in plus_h and text[:2] in ("bh", "dh", "gh", "mh") else 0
            out.extend(
                _consonant_segments(
                    text[skip:], slen, word, _offset(runs, i) + skip, dialect, notes
                )
            )
            continue
        if i in absorbed:
            continue
        k = live.index(i)
        value = nuclei[k]
        if k == stress and not proclitic:
            stress_at = _onset_start(out)
        if k != stress or proclitic:
            if i in plus_h:
                value = plus_h[i][1]
            else:
                # The lengthening overrides of `_VOWELS` are listed under "stressed" in the
                # source table, so an unstressed syllable falls back to the row's default and
                # reduces if that is short: *Muireann* /ˈmˠɪɾʲən̪ˠ/, not */ˈmˠɪɾʲaːn̪ˠ/.
                base = (
                    _VOWELS.get(runs[i][1])
                    or _VOWELS.get(runs[i][1][:2])
                    or _VOWELS.get(runs[i][1][:1])
                    or (value, ())
                )[0]
                value = "ə" if _short(base) else base
        out.extend(_split_nucleus(value))

    if dialect == "C":
        out = [("vˠ" if seg == "w" and k else seg) for k, seg in enumerate(out)]
    before = len(out)
    out = _epenthesis(out, len(live), notes)
    syllables = len(live) + (len(out) - before)
    if syllables >= 2 and stress_at is not None and not proclitic:
        out.insert(stress_at, "ˈ")
    return out


def _onset_start(out: list[str]) -> int:
    """The index the stress mark belongs at: before the onset consonants of the syllable whose
    nucleus is about to be emitted (spec §4; marks precede the syllable, never the vowel)."""
    i = len(out)
    while i > 0 and out[i - 1] not in _VOWEL_SEGMENTS and out[i - 1] not in _LONG_SEGMENTS:
        i -= 1
    return i


def _short(value: str) -> bool:
    """A nucleus that is a short monophthong — the only kind an unstressed syllable reduces
    [wiki-irish-orthography §Vowels: "Unstressed short vowels are generally reduced to /ə/"]."""
    return len(value) == 1 and value not in ("ə",)


def _offset(runs: list[tuple[str, str]], i: int) -> int:
    return sum(len(t) for _, t in runs[:i])


def _split_nucleus(value: str) -> list[str]:
    """A nucleus string → segments. Diphthongs are two segments (I-2)."""
    out: list[str] = []
    i = 0
    while i < len(value):
        if value[i + 1 : i + 2] == "ː":
            out.append(value[i : i + 2])
            i += 2
        else:
            out.append(value[i])
            i += 1
    return out


def _epenthesis(segs: list[str], syllables: int, notes: list[str]) -> list[str]:
    """digest §2.4. Blocked by a preceding long vowel or diphthong, by a voiceless-stop or
    homorganic C2 (neither is in `_EPEN_C2_*`), and — in Connacht — in words of ≥3 syllables
    [green1997 pp.152-153]."""
    if syllables >= 3:
        return segs
    out: list[str] = []
    for i, seg in enumerate(segs):
        out.append(seg)
        nxt = segs[i + 1] if i + 1 < len(segs) else None
        if seg not in _EPEN_C1 or nxt is None:
            continue
        allowed = _EPEN_C2_NASAL if seg in _EPEN_NASALS else _EPEN_C2_LIQUID
        if nxt not in allowed:
            continue
        prev = segs[i - 1] if i else None
        if prev in _LONG_SEGMENTS or (
            i >= 2 and segs[i - 1] == "ə" and segs[i - 2] in ("i", "u", "ə")
        ):
            continue  # long vowel or diphthong before the cluster
        if prev is not None and prev in ("i", "u") and i >= 1:
            continue
        out.append("ə")
        notes.append("epenthesis")
    return out


# ---- the entry point -------------------------------------------------------------------------


def g2p(orthography: str, dialect: str = "C") -> tuple[str, list[str]]:
    """Modern Irish spelling → (IPA in this project's convention, notes).

    `notes` names the rules that were uncertain for this word, so `inputs.infer()` can tag the
    row `g2p:<note>` and `strands lint` can show it. Raises `G2PError` on an empty or
    unreadable orthography.
    """
    text = unicodedata.normalize("NFC", (orthography or "").strip()).lower()
    if not text:
        raise G2PError("empty orthography")
    notes: list[str] = []
    words: list[str] = []
    for token in text.split():
        parts = token.split("-")
        pieces: list[str] = []
        for k, part in enumerate(parts):
            if not part:
                continue
            if k == 0 and len(parts) > 1 and part in ("n", "t", "h") and parts[1]:
                # n-/t-/h-prothesis: the prefix takes its quality from the following vowel
                # letter [wiki-irish-mutations §Changes to vowel-initial words].
                rest = "-".join(parts[1:])
                slen = rest[0] in _SLENDER_LETTERS if rest else False
                pref = {"n": ("n̪ˠ", "n̠ʲ"), "t": ("t̪ˠ", "tʲ"), "h": ("h", "h")}[part]
                seg = pref[1 if slen else 0]
                inner = _word_segments(rest, dialect, notes, proclitic=False)
                if inner and inner[0] == "ˈ":
                    inner = inner[1:]
                    pieces.append("ˈ")
                pieces.append(seg)
                pieces.extend(inner)
                break
            if len(parts) == 1 and part in _PROCLITIC_IPA:
                pieces.append(_PROCLITIC_IPA[part])
                continue
            segs = _word_segments(
                part, dialect, notes, proclitic=len(parts) == 1 and part in _PROCLITICS
            )
            if len(parts) > 1 and segs and segs[0] != "ˈ":
                segs = ["ˈ"] + segs
            if k > 0:
                # A hyphenated compound takes a second PRIMARY stress: droch-dhuine
                # /ˈd̪ˠɾˠɔxˈɣinʲə/, Fíor-Dhia /ˈfʲiːɾˠˈjiːə/, Ard-Easpag /ˈaːɾˠd̪ˠˈæsˠpˠəɡ/
                # (digest §4.1 compound pattern 4 [wiki-irish-phonology §Compound words]).
                notes.append("compound-stress")
            pieces.extend(segs)
        words.append("".join(pieces))
    return " ".join(words), sorted(set(notes))
