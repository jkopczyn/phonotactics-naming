"""The Old Irish spelled word, its grapheme table, and the one-way reconstruction.

Old Irish spec §6 and §11; plan Task 7; interpretations O-27, O-10, O-11, O-14, O-28, O-29,
O-32.

What the spelled word is (spec §11, O-27). Every Old Irish stage downstream of the
retro-filter — lookup, `[mutations]`, `[inflect]`, `[templates]` — passes around a
`SpelledWord`: an ordered tuple of lower-case GRAPHEME TOKENS plus two pieces of metadata,
`capitalized` and the initial `mutation` (`""`, `"LEN"` or `"NAS"`). The tokens come from one
table, `rules/old-irish-orthography.tsv`, which also carries each token's reconstruction, so
there is no second alphabet to keep in sync. Silent tokens (⟨ḟ⟩), the punctum forms (⟨ṡ ḟ⟩)
and the unresolved ending marker ⟨ə⟩ are ordinary tokens.

Losslessness is the point. `"".join(word.graphemes)` IS the written form (up to the stored
capital), so a grapheme rewrite can never lose the spelling and nothing has to carry
provenance for a deleted sound: lenited ⟨ḟ⟩ is a written token whose reconstruction is empty.
Draft 1's IPA-internal grammar made the mutation/reconstruction bridge lossy; this is the fix.

`spelling_to_ipa` is one-way and final (O-11). It runs once, on the finished spelled word,
and produces segments; nothing converts segments back to a spelling here, and there is no
round-trip requirement in that direction. The steps are digest §10.2 read forwards: the
unwritten initial mutation (conv. 1 — the single reason the word carries a `mutation`
field), the glide ⟨i⟩ (conv. 5 §36), row selection with conv. 4's `left` letters, the
quality pass (conv. 5), and the post-stress reduction (conv. 5 grid; digest §10.1).

The quality pass never derives the BROAD↔SLEN pairing positionally (spec §11): it reads the
explicit `quality-pairs` declaration of `old-irish.rules [meta]` by name, `w:-` marking a
segment with no partner. Until that file exists (plan Task 8 follows this one) the same
declaration is bootstrapped from `DECLARED_QUALITY_PAIRS` below; Task 8's key is authoritative
whenever it is present.

`punctum` is rendering only (O-14). `render(punctum=False)` substitutes each token's plain
form from the table's `punctum` COLUMN (⟨ṡ⟩→s, ⟨ḟ⟩→f) in the output string alone; tokens,
metadata and IPA are untouched, so the setting provably cannot change the IPA.
"""
from __future__ import annotations

import re
import unicodedata
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, replace
from pathlib import Path

__all__ = [
    "OI_ORTHOGRAPHY_PATH", "OI_RULES_PATH", "ROLES", "ENVS", "MUTATIONS",
    "DECLARED_QUALITY_PAIRS", "GraphemeRow", "GraphemeRule", "SpelledError", "SpelledWord",
    "apply_grapheme_table", "load_graphemes", "load_quality_pairs", "parse_quality_pairs",
    "spelling_to_ipa", "spelling_to_words", "tokenize_spelling", "token_roles",
]

_ROOT = Path(__file__).resolve().parents[2]
OI_ORTHOGRAPHY_PATH: Path = _ROOT / "rules" / "old-irish-orthography.tsv"
OI_RULES_PATH: Path = _ROOT / "rules" / "old-irish.rules"

ROLES: tuple[str, ...] = ("cons", "vowel", "long", "nasal", "glide", "silent", "ending")
"""The complete `role` vocabulary. `glide` and `silent` produce no segment; `glide` marks
quality and is assigned by the reconstruction, never written in the table. `ending` is the
unresolved ending marker of spec §11. There is NO `punctum` role: a punctum form is an
ordinary `cons`/`silent` token that happens to have a plain-letter variant, which is the
`punctum` COLUMN."""
ENVS: tuple[str, ...] = ("initial", "noninitial", "final", "any")
"""`initial` ⇔ the word's first token; `final` ⇔ its last token (the §40/§41 final digraphs
⟨-ae -ai -ea -eo -iu⟩ — without it ⟨ai⟩ would swallow the medial glide of *athair*)."""
MUTATIONS: tuple[str, ...] = ("", "LEN", "NAS")
_NUCLEUS_ROLES = frozenset({"vowel", "long"})
_CONSONANT_ROLES = frozenset({"cons", "nasal"})
_SLENDER_LETTERS = frozenset("eéií")           # digest §10.2 conv. 5 (i)
_U_GLIDE_AFTER = frozenset({"a", "e", "i"})    # [pokorny1914 §38]: the u-glide follows short a e i
_REDUCES_TO_U = frozenset({"u", "o"})          # digest §10.1: non-final /u/ is written ⟨u o⟩
_NASAL_PREFIX = "n-"

# digest §10.2 conv. 1 (unwritten lenition of the voiced stops and m) and spec §11 (ii)
# (unwritten nasalization of the voiceless stops): the initial token's reconstruction is
# replaced; the written form is untouched. Written mutations (⟨ch th ph ṡ ḟ mb nd ng n-⟩) are
# already tokens and need nothing.
_UNWRITTEN = {
    "LEN": {"b": ("β",), "d": ("ð",), "g": ("ɣ",), "m": ("β̃",)},
    "NAS": {"c": ("ɡ",), "t": ("d̪ˠ",), "p": ("bˠ",)},
}

DECLARED_QUALITY_PAIRS = (
    "pˠ:pʲ bˠ:bʲ t̪ˠ:tʲ d̪ˠ:dʲ k:c ɡ:ɟ fˠ:fʲ sˠ:ʃ x:ç ɣ:ɣʲ β:βʲ β̃:β̃ʲ ð:ðʲ θ:θʲ mˠ:mʲ n̪ˠ:nʲ "
    "ŋ:ɲ l̪ˠ:lʲ ɾˠ:ɾʲ h:h w:-")
"""Spec §11's explicit BROAD↔SLEN declaration, as `old-irish.rules [meta] quality-pairs`
states it. Bootstrap only: `load_quality_pairs` prefers the rule file when it exists."""

_META_PAIRS_RE = re.compile(r"^\s*quality-pairs\s*=\s*([^#]*)")
_SECTION_RE = re.compile(r"^\s*\[\s*([a-z-]+)\s*\]")


class SpelledError(Exception):
    """A spelling no grapheme token covers, a malformed grapheme table, or a bad mutation
    name. A rule-file or lexicon bug, not user data (I-24)."""


# ---- the table ---------------------------------------------------------------------------

@dataclass(frozen=True)
class GraphemeRow:
    token: str          # lower-case letters as written, 1-3 chars
    env: str            # one of ENVS
    left: str           # letters, one of which must END the previous token, or "" for any
    ipa: tuple[str, ...]   # () = silent
    role: str           # one of ROLES
    punctum: str        # the plain-letter form for `punctum = off`, or "" for none
    note: str
    line: int = 0       # file line, for `check_grapheme_table`


_HEADER = ("token", "env", "left", "ipa", "role", "punctum", "note")
_cache: dict[Path, tuple[GraphemeRow, ...]] = {}


def load_graphemes(path: Path | None = None) -> tuple[GraphemeRow, ...]:
    """Read the grapheme table (UTF-8, NFC per I-1). `#` lines are comments; the first
    other line is the header. Rows come back sorted by token length, LONGEST FIRST; the
    sort is stable, so file order breaks ties — and that order is load-bearing for digest
    §10.2 conv. 4 (the more specific row of a token must come first). Only the shape is
    validated here; `check.check_grapheme_table` reports the content."""
    path = OI_ORTHOGRAPHY_PATH if path is None else Path(path)
    if path in _cache:
        return _cache[path]
    rows: list[GraphemeRow] = []
    header_seen = False
    for n, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = unicodedata.normalize("NFC", raw)
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        cells = [c.strip() for c in line.split("\t")]
        if not header_seen:
            if tuple(cells[:7]) != _HEADER:
                raise SpelledError(f"{path}:{n}: expected header {' '.join(_HEADER)!r}")
            header_seen = True
            continue
        if len(cells) < 6:
            raise SpelledError(f"{path}:{n}: expected at least 6 tab-separated cells")
        cells += [""] * (7 - len(cells))
        token, env, left, ipa, role, punctum, note = cells[:7]
        if not token:
            raise SpelledError(f"{path}:{n}: empty token")
        rows.append(GraphemeRow(
            token=token, env=env, left="" if left == "-" else left,
            ipa=() if ipa in ("-", "") else tuple(ipa.split("+")), role=role,
            punctum="" if punctum == "-" else punctum, note=note, line=n))
    if not header_seen:
        raise SpelledError(f"{path}: no header line")
    out = tuple(sorted(rows, key=lambda r: -len(r.token)))
    _cache[path] = out
    return out


def token_roles(rows: Sequence[GraphemeRow] | None = None) -> dict[str, str]:
    """token -> the role of its first row (a token's rows never differ in role)."""
    out: dict[str, str] = {}
    for r in rows if rows is not None else load_graphemes():
        out.setdefault(r.token, r.role)
    return out


def _row_applies(row: GraphemeRow, index: int, is_last: bool, prev: str | None) -> bool:
    if row.env == "initial" and index != 0:
        return False
    if row.env == "noninitial" and index == 0:
        return False
    if row.env == "final" and not is_last:
        return False
    if row.env not in ENVS:
        return False
    if row.left and (prev is None or prev[-1] not in row.left):
        return False
    return True


def _select_row(rows: Sequence[GraphemeRow], token: str, index: int, is_last: bool,
                prev: str | None) -> GraphemeRow | None:
    """The first row (longest-token-first, then file order) for `token` whose `env` and
    `left` are satisfied at this position."""
    for r in rows:
        if r.token == token and _row_applies(r, index, is_last, prev):
            return r
    return None


def tokenize_spelling(text: str, rows: Sequence[GraphemeRow] | None = None) -> tuple[str, ...]:
    """Greedy longest-match over the table's tokens, in table order. A token is eligible at
    a position only if one of its rows applies there (its `env` and `left`), so ⟨mb⟩ is a
    token at the start of *mbó* and two tokens inside *imb*. A character no token covers
    raises `SpelledError` naming the spelling, the character and its position."""
    rows = load_graphemes() if rows is None else rows
    text = unicodedata.normalize("NFC", text).lower()
    tokens: list[str] = []
    i, n = 0, len(text)
    while i < n:
        for r in rows:
            if text.startswith(r.token, i) and _row_applies(
                    r, len(tokens), i + len(r.token) == n, tokens[-1] if tokens else None):
                tokens.append(r.token)
                i += len(r.token)
                break
        else:
            raise SpelledError(f"cannot tokenize {text!r}: no grapheme token matches "
                               f"{text[i]!r} at position {i}")
    return tuple(tokens)


# ---- the object (O-27) --------------------------------------------------------------------

@dataclass(frozen=True)
class SpelledWord:
    graphemes: tuple[str, ...]      # LOWER-CASE grapheme tokens, in order (O-32)
    capitalized: bool = False       # render the first letter upper-case
    mutation: str = ""              # "" | "LEN" | "NAS" — the INITIAL mutation, as metadata

    @classmethod
    def from_spelling(cls, text: str) -> SpelledWord:
        """Tokenize a written Old Irish word. Lossless: `render()` returns `text` again."""
        text = unicodedata.normalize("NFC", text).strip()
        if not text:
            raise SpelledError("empty spelling")
        tokens = tokenize_spelling(text)
        # The written nasal prefix is not the name's first letter (O-32): *n-Ériu* is
        # capitalized at the letter after ⟨n-⟩, exactly where `render` re-applies it.
        k = len(_NASAL_PREFIX) if tokens[0] == _NASAL_PREFIX else 0
        return cls(tokens, capitalized=k < len(text) and text[k].isupper())

    def with_mutation(self, name: str) -> SpelledWord:
        if name not in MUTATIONS:
            raise SpelledError(f"unknown mutation {name!r}; expected one of "
                               + ", ".join(repr(m) for m in MUTATIONS))
        return replace(self, mutation=name)

    def render(self, *, punctum: bool = True) -> str:
        """The written form. `punctum=False` substitutes each token's PLAIN FORM from the
        grapheme table's `punctum` column (ṡ->s, ḟ->f) in the OUTPUT ONLY (O-14). The
        substitution is data, not a hardcoded map, so a later punctum form needs a table
        row and no code change. The ending marker ⟨ə⟩ is NOT special-cased: a leaked one is
        visible in the output, which is what makes it catchable."""
        tokens = self.graphemes
        if not punctum:
            plain = {r.token: r.punctum for r in reversed(load_graphemes()) if r.punctum}
            tokens = tuple(plain.get(t, t) for t in tokens)
        text = "".join(tokens)
        if self.capitalized and text:
            # A written nasal prefix is not the name's first letter: *n-Ériu*, not *N-ériu*.
            k = len(_NASAL_PREFIX) if self.graphemes[0] == _NASAL_PREFIX else 0
            if k < len(text):
                text = text[:k] + text[k].upper() + text[k + 1:]
        return text

    def ipa(self) -> tuple[str, ...]:
        """= spelling_to_ipa(self). One-way and final (O-11)."""
        return spelling_to_ipa(self)


def spelling_to_words(text: str) -> tuple[SpelledWord, ...]:
    """Split on whitespace; each part is one spelled word."""
    return tuple(SpelledWord.from_spelling(part) for part in text.split())


# ---- the quality pairs (spec §11) --------------------------------------------------------

def parse_quality_pairs(text: str) -> dict[str, str]:
    """`pˠ:pʲ bˠ:bʲ … w:-` -> {broad: slender}; a `-` partner means none and is omitted."""
    out: dict[str, str] = {}
    for item in text.split():
        broad, colon, slender = item.partition(":")
        if not colon or not broad or not slender:
            raise SpelledError(f"bad quality pair {item!r}; expected BROAD:SLENDER or BROAD:-")
        if slender != "-":
            out[broad] = slender
    return out


_pairs_cache: dict[Path, dict[str, str]] = {}


def load_quality_pairs(path: Path | None = None) -> dict[str, str]:
    """The declared BROAD->SLENDER mapping: `[meta] quality-pairs` of `old-irish.rules`
    when the file exists (read by name, never derived positionally — spec §11), else the
    bootstrap `DECLARED_QUALITY_PAIRS`."""
    path = OI_RULES_PATH if path is None else Path(path)
    if path in _pairs_cache:
        return _pairs_cache[path]
    declared: str | None = None
    if path.exists():
        section = None
        for raw in path.read_text(encoding="utf-8").splitlines():
            line = unicodedata.normalize("NFC", raw)
            head = _SECTION_RE.match(line)
            if head:
                section = head.group(1)
                continue
            m = _META_PAIRS_RE.match(line)
            if section == "meta" and m:
                declared = m.group(1)
                break
    pairs = parse_quality_pairs(DECLARED_QUALITY_PAIRS if declared is None else declared)
    _pairs_cache[path] = pairs
    return pairs


# ---- the reconstruction (O-11) -----------------------------------------------------------

def _is_vowel_letter(role: str | None) -> bool:
    return role in _NUCLEUS_ROLES


def spelling_to_ipa(word: SpelledWord, *, pairs: Mapping[str, str] | None = None
                    ) -> tuple[str, ...]:
    """Reconstruct the segments of a finished spelled word (digest §10.2 read forwards).

    1. Initial mutation (conv. 1; spec §11 (ii)): an unwritten `LEN`/`NAS` replaces the
       first token's reconstruction (`_UNWRITTEN`).
    2. Glide reclassification (conv. 5 §36, §38): an ⟨i⟩ that is not word-initial, follows a
       vowel or long token and precedes a consonant token contributes NO segment; likewise a
       ⟨u⟩ after a short ⟨a e i⟩ before a consonant token (*fiuss*) — the u-glide marks
       Pokorny's rounded quality, which is a spelling matter only (O-4), so it is neither a
       segment nor a nucleus.
    3. Row selection, left to right: the first row whose token matches, whose `env` holds
       and whose `left` (conv. 4) contains the last letter of the previous token.
    4. Quality (conv. 5): a consonant is SLENDER iff (i) the next non-consonant token is
       written with a first letter ⟨e é i í⟩ (an onset cluster takes its vowel's quality:
       the grid's *dliged* /ˈdʲlʲiɣʲəð/), or (ii) a written ⟨i⟩ — glide or vowel, never ⟨í⟩ or a
       diphthong token — precedes it with only consonant tokens between, and it is not
       followed by a vowel letter (*muir*, *fir*, *cinn*; conv. 4's *imb* /imʲbʲ/ is the
       datum for "through the cluster"). A doubled token is one unit: both halves take the
       same quality. The mapping is the declared `quality-pairs`, never positional.
    5. Reduction (conv. 5 grid; digest §10.1 "non-finally, only two phonemes: /ə/ and /u/"):
       a `vowel`-role token outside the first syllable and not word-final becomes /u/ when
       written ⟨u o⟩ (*lebor* /ˈLʲevur/, *domun* /ˈdoṽun/) and /ə/ otherwise (⟨a ai e i⟩).
       `long` tokens never reduce; word-final vowels never reduce (§10.1: all ten occur).
    """
    rows = load_graphemes()
    pairs = load_quality_pairs() if pairs is None else pairs
    tokens = word.graphemes
    n = len(tokens)
    if n == 0:
        return ()

    # 3 (row selection happens first because the roles come from the rows)
    selected: list[GraphemeRow] = []
    for k, tok in enumerate(tokens):
        row = _select_row(rows, tok, k, k == n - 1, tokens[k - 1] if k else None)
        if row is None:
            raise SpelledError(f"no grapheme row for {tok!r} at token {k} of "
                               f"{''.join(tokens)!r}")
        selected.append(row)
    roles = [r.role for r in selected]
    segs: list[list[str]] = [list(r.ipa) for r in selected]

    # 1
    if word.mutation:
        override = _UNWRITTEN[word.mutation].get(tokens[0])
        if override is not None:
            segs[0] = list(override)

    # 2
    for k in range(1, n - 1):
        if roles[k + 1] not in _CONSONANT_ROLES:
            continue
        if (tokens[k] == "i" and roles[k - 1] in _NUCLEUS_ROLES) \
                or (tokens[k] == "u" and tokens[k - 1] in _U_GLIDE_AFTER):
            roles[k] = "glide"
            segs[k] = []

    # 4
    for k in range(n):
        if roles[k] not in _CONSONANT_ROLES:
            continue
        j = k + 1
        while j < n and roles[j] in _CONSONANT_ROLES:
            j += 1
        slender = j < n and tokens[j][0] in _SLENDER_LETTERS
        if not slender and not (k + 1 < n and _is_vowel_letter(roles[k + 1])):
            j = k - 1
            while j >= 0 and roles[j] in _CONSONANT_ROLES:
                j -= 1
            slender = j >= 0 and tokens[j] == "i"
        if slender:
            segs[k] = [pairs.get(s, s) for s in segs[k]]

    # 5
    nuclei = 0
    for k in range(n):
        if roles[k] in _NUCLEUS_ROLES:
            nuclei += 1
            if roles[k] == "vowel" and nuclei > 1 and k != n - 1 and segs[k]:
                segs[k] = ["u"] if tokens[k] in _REDUCES_TO_U else ["ə"]

    return tuple(s for group in segs for s in group)


# ---- grapheme rewrites (O-10) -------------------------------------------------------------

@dataclass(frozen=True)
class GraphemeRule:
    table: str          # the sub-table it belongs to ("LEN", "GEN_O", …)
    line: int
    rule_id: str        # "<section>:<line>"
    target: tuple[str, ...]        # grapheme tokens, an inline set "{c t p}", or the class V / C
    replacement: tuple[str, ...]   # tokens, or () for deletion
    left: tuple[str, ...]          # context atoms: tokens, sets, classes, "#"
    right: tuple[str, ...]
    tag: str
    comment: str


def _atom_matches(atom: str, token: str, roles: Mapping[str, str]) -> bool:
    if atom == "V":
        return roles.get(token) in _NUCLEUS_ROLES
    if atom == "C":
        return roles.get(token) in _CONSONANT_ROLES
    if atom.startswith("{") and atom.endswith("}"):
        return token in atom[1:-1].split()
    return atom == token


def _context_ok(tokens: Sequence[str], start: int, stop: int, rule: GraphemeRule,
                roles: Mapping[str, str]) -> bool:
    p = start - 1
    for atom in reversed(rule.left):
        if atom == "#":
            if p != -1:
                return False
            continue
        if p < 0 or not _atom_matches(atom, tokens[p], roles):
            return False
        p -= 1
    p = stop
    for atom in rule.right:
        if atom == "#":
            if p != len(tokens):
                return False
            continue
        if p >= len(tokens) or not _atom_matches(atom, tokens[p], roles):
            return False
        p += 1
    return True


def _matches(tokens: Sequence[str], rule: GraphemeRule, roles: Mapping[str, str]
             ) -> list[tuple[int, int]]:
    """Every (start, stop) span of `tokens` the rule matches, left to right, overlapping
    spans included (callers decide the policy)."""
    width = len(rule.target)
    out: list[tuple[int, int]] = []
    for start in range(len(tokens) - width + 1):
        stop = start + width
        if all(_atom_matches(a, tokens[start + i], roles) for i, a in enumerate(rule.target)) \
                and _context_ok(tokens, start, stop, rule, roles):
            out.append((start, stop))
    return out


def _splice(tokens: tuple[str, ...], edits: list[tuple[int, int, tuple[str, ...]]]
            ) -> tuple[str, ...]:
    out = list(tokens)
    for start, stop, new in sorted(edits, key=lambda e: e[0], reverse=True):
        out[start:stop] = list(new)
    return tuple(out)


def apply_grapheme_table(word: SpelledWord, rules: Sequence[GraphemeRule],
                         *, simultaneous: bool) -> SpelledWord:
    """`simultaneous=True` for a mutation table (one pass against the pre-table word, first
    rule in file order wins an overlapping span — the `irish._apply_table` contract, edge
    contact included); `simultaneous=False` for an inflection (ordered, each rule sees the
    previous output; within one rule, matches are taken left to right without overlap).
    An edit that changes nothing is skipped. Capitalization and mutation are carried."""
    roles = token_roles()
    tokens = word.graphemes
    if simultaneous:
        claimed: list[tuple[int, int]] = []
        edits: list[tuple[int, int, tuple[str, ...]]] = []
        for rule in rules:
            for start, stop in _matches(tokens, rule, roles):
                if rule.replacement == tokens[start:stop]:
                    continue
                if any(start <= b and a <= stop for a, b in claimed):
                    continue
                claimed.append((start, stop))
                edits.append((start, stop, rule.replacement))
        if edits:
            tokens = _splice(tokens, edits)
    else:
        for rule in rules:
            edits = []
            last_stop = -1
            for start, stop in _matches(tokens, rule, roles):
                if start < last_stop or rule.replacement == tokens[start:stop]:
                    continue
                edits.append((start, stop, rule.replacement))
                last_stop = max(stop, start + 1)
            if edits:
                tokens = _splice(tokens, edits)
    if tokens == word.graphemes:
        return word
    # O-11 (plan Task 18): the IPA is read FROM the finished written form, so the tokens must
    # be the ones `from_spelling` reads back from the rendered string. A rewrite that splices
    # tokens can leave a sequence the table reads as one grapheme (*dí* + the marker's *a* is
    # written ⟨ía⟩, the diphthong /ia/, not ⟨í⟩⟨a⟩ /iːa/), so the spliced word is re-tokenized.
    try:
        tokens = tokenize_spelling("".join(tokens))
    except SpelledError:        # a hand-built rule writing a non-token; `check` rejects it in a file
        pass
    return replace(word, graphemes=tokens)
