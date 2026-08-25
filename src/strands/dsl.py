"""Rule-file DSL parser: file skeleton, simple sections, rewrite lines, structured sections.

Plan Task 5a (core) — spec §3 (rule DSL) and §12.C (inline sets, captures/backreferences,
feature aliases, quoted respell output); the plan's EBNF is the grammar implemented here.
Plan Task 5b adds `[syllable]` (spec §3, §12.B nuclei, §12.D complete onset/coda sets),
`[stress]` (I-17: `procedure = X` plus free `key = value` parameters, validated by `strands
check`), `[epithets]` (I-18), `[templates]` (I-16), the named sub-tables of `[mutations]` /
`[inflect]` (I-15) and the `[repair]` directive `cluster-fallback = same-length` (§12.E).
Interpretations: I-1 (NFC on read), I-3 (`#` in an environment is the word edge; a comment
after an environment requires an explicit %tag), I-4 (bundle syntax), I-5 (targets and
replacements), I-8 (`.`/`ˈ` are context-only), I-9 (`()`/`*` on one atom, no nesting, no
capture on a zero-or-more item), I-10 (class-name pattern), I-11 (predeclared classes),
I-21 (rule ids), I-32 (aliases and U+2212).

Semantic validation that `strands check` (Task 6) reports with codes — undeclared class
names, unknown feature names, off-inventory replacements, unreachable feature changes,
undefined backreferences — is deliberately NOT a parse error here: the parser keeps the
names verbatim (aliases resolved where known) so `check` can list every finding at once.
Unknown *segments* are hard errors (I-24).

Comment handling in the structured sections: `[syllable] bans` and `[epithets]` lines are
context sequences, so — as in a rewrite environment (I-3) — `#` in them is the word edge and
the sequence runs to end-of-line; a trailing comment is not possible on those two line kinds.
Every other structured line takes a trailing `# comment`.
"""
from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

from .features import FeatureError, FeatureTable, DERIVED_CLASSES
from .tokenize import SegmentError, tokenize

__all__ = [
    "Bundle", "ItemSpec", "CtxItem", "Rule", "Backref", "QuotedText", "RuleFile",
    "SyllableSpec", "StressSpec", "Epithet", "TemplateItem",
    "ParseError", "parse_rules", "parse_rules_file",
    "SECTION_NAMES", "REWRITE_SECTIONS", "SUBTABLE_SECTIONS", "TAGS",
    "STRESS_PROCEDURES", "TEMPLATE_ARGS", "TEMPLATE_FUNCS",
]

SECTION_NAMES: tuple[str, ...] = (
    "meta", "inventory", "classes", "weights", "substitute", "syllable", "repair",
    "post-stress", "stress", "epithets", "respell", "templates", "mutations", "inflect",
    "normalize",
)
REWRITE_SECTIONS: tuple[str, ...] = ("substitute", "repair", "post-stress", "respell", "normalize")
SUBTABLE_SECTIONS: tuple[str, ...] = ("mutations", "inflect")          # I-15
TAGS: tuple[str, ...] = ("attested", "design", "fallback")
STRESS_PROCEDURES: tuple[str, ...] = ("initial", "penult", "cairene", "dutch-weight", "keep-source")
TEMPLATE_ARGS: tuple[str, ...] = ("NAME", "FATHER", "NOUN", "ADJ", "FIRST", "SECOND")
TEMPLATE_FUNCS: tuple[str, ...] = (
    "LEN", "ECL", "HPREF", "TPREF", "GEN", "GEN_M1", "GEN_ACH", "GEN_F2", "GEN_M3",
    "VOC_M1", "ART", "LEN_IF_F")
_SYLLABLE_KEYS: frozenset[str] = frozenset((
    "template", "nuclei", "onsets", "codas", "onsets-tier", "codas-tier", "onset-required",
    "appendix", "domain", "sonority", "bans"))
_TIER_RE = re.compile(r"[A-Z][A-Z0-9]*\Z")
_SUBTABLE_HEAD_RE = re.compile(r"([A-Za-z][A-Za-z0-9_-]*)\s*:\s*(?:#.*)?\Z")

_CLASS_RE = re.compile(r"[A-Z][A-Z0-9_]*\Z")
# A section header is `[name]` alone on its line (plus an optional comment); a rewrite
# line that begins with a match bundle (`[C +back] -> ...`) is not a header.
_SECTION_RE = re.compile(r"\[\s*([a-z-]+)\s*\]\s*(?:#.*)?\Z")
_NAME_RE = re.compile(r"[A-Za-z][A-Za-z0-9_-]*\Z")
_SPECIALS = ("#", "$", ".", "ˈ")
_SIGNS = {"+": "+", "-": "-", "−": "-", "0": "0"}
# Characters that end a bare SEGMENT / class-name token (plan: reserved outside a SEGMENT).
_TERMINATORS = frozenset(' \t[](){}"\\:*_#$.ˈ/%')


# ---- data model -----------------------------------------------------------------------------

@dataclass(frozen=True)
class Bundle:
    class_name: str | None
    constraints: dict[str, str]        # canonical feature names (aliases resolved at parse)


@dataclass(frozen=True)
class ItemSpec:
    kind: str                          # "segment" | "class" | "bundle" | "set"
    value: str | Bundle | tuple[str, ...]
    capture: int | None = None         # from ":n" (I-33)


@dataclass(frozen=True)
class CtxItem:
    atom: ItemSpec | str               # str is one of "#", "$", ".", "ˈ"
    optional: bool = False
    star: bool = False


@dataclass(frozen=True)
class Backref:
    n: int


@dataclass(frozen=True)
class QuotedText:
    text: str


@dataclass(frozen=True)
class Rule:
    section: str
    line: int
    rule_id: str                       # f"{section}:{line}"
    target: tuple[ItemSpec, ...]       # () = epenthesis
    replacement: tuple[object, ...] | Bundle
    #   elements are str (segment), Backref(n), or QuotedText(s); Bundle = feature change;
    #   () = deletion
    left: tuple[CtxItem, ...]
    right: tuple[CtxItem, ...]
    tag: str
    comment: str


@dataclass(frozen=True)
class SyllableSpec:
    """`[syllable]` (spec §3, §12.B, §12.D). Absent keys take the documented defaults:
    `template`/`onsets`/`codas` None = `any`; `onset_required` False; `domain` "word";
    `sonority` off. `onsets`/`codas` are kept in FILE ORDER because cluster-fallback
    (§12.E) breaks ties by list order; the frozensets are only membership indexes."""
    template: tuple[tuple[str, bool], ...] | None   # (slot, optional); None = "any"
    nuclei: tuple[tuple[str, ...], ...]             # licensed vowel sequences (I-2)
    onsets: tuple[tuple[str, ...], ...] | None      # COMPLETE, IN FILE ORDER (spec §12.D/§12.E)
    codas: tuple[tuple[str, ...], ...] | None
    onset_set: frozenset[tuple[str, ...]] | None    # derived from `onsets`, for membership tests
    coda_set: frozenset[tuple[str, ...]] | None     # derived from `codas`
    onset_tiers: dict[tuple[str, ...], str]
    coda_tiers: dict[tuple[str, ...], str]
    onset_required: bool                            # default False (spec §12.D)
    appendix: tuple[str, ...]
    domain: str                                     # "word" | "stem"
    sonority: bool
    bans: tuple[tuple[CtxItem, ...], ...]


@dataclass(frozen=True)
class StressSpec:
    procedure: str
    params: dict[str, str]             # raw values; validated against stress/params.py by check


@dataclass(frozen=True)
class Epithet:
    name: str
    form: tuple[str, ...]
    left: tuple[CtxItem, ...]
    right: tuple[CtxItem, ...]


@dataclass(frozen=True)
class TemplateItem:
    kind: str            # "literal" | "arg" | "call"
    value: str           # literal text, argument name, or function name
    child: "TemplateItem | None" = None    # the call's argument; None = applied to the head (I-16)
    conditional: bool = False              # trailing "?"


@dataclass(frozen=True)
class RuleFile:
    path: str
    meta: dict[str, str]
    inventory: tuple[str, ...]
    marginal: frozenset[str]
    classes: dict[str, tuple[str, ...]]     # user + derived (I-11)
    weights: dict[str, float]
    sections: dict[str, tuple[Rule, ...]]
    syllable: SyllableSpec | None = None
    stress: StressSpec | None = None
    epithets: dict[str, Epithet] = field(default_factory=dict)
    templates: dict[str, tuple[TemplateItem, ...]] = field(default_factory=dict)
    mutations: dict[str, tuple[Rule, ...]] = field(default_factory=dict)   # I-15
    inflect: dict[str, tuple[Rule, ...]] = field(default_factory=dict)     # I-15
    cluster_fallback: str | None = None     # [repair] directive, "same-length" (spec §12.E)


class ParseError(Exception):
    """str(e) == f"{path}:{line}: {message}"."""

    def __init__(self, message: str, line: int, path: str = "<string>") -> None:
        self.message = message
        self.line = line
        self.path = path
        super().__init__(f"{path}:{line}: {message}")


# ---- lexical scanning of rewrite lines ------------------------------------------------------

@dataclass
class _Tok:
    """One scanned item: kind in {"word", "bundle", "set", "quoted", "backref", "special"}."""
    kind: str
    text: str
    capture: int | None = None
    optional: bool = False
    star: bool = False


class _LineParser:
    def __init__(self, section: str, line: int, path: str, table: FeatureTable) -> None:
        self.section = section
        self.line = line
        self.path = path
        self.table = table

    def err(self, message: str) -> ParseError:
        return ParseError(message, self.line, self.path)

    # -- top-level split ----------------------------------------------------------------------

    def _find_outside(self, text: str, needle: str, start: int = 0) -> int:
        """Index of the first `needle` in text[start:] outside [..], {..} and "..", or -1."""
        depth = 0
        quoted = False
        i = start
        while i < len(text):
            ch = text[i]
            if quoted:
                if ch == '"':
                    quoted = False
            elif ch == '"':
                quoted = True
            elif ch in "[{":
                depth += 1
            elif ch in "]}":
                depth = max(0, depth - 1)
            elif depth == 0 and text.startswith(needle, i):
                return i
            i += 1
        return -1

    def parse(self, text: str) -> Rule:
        arrow = self._find_outside(text, "->")
        if arrow < 0:
            raise self.err("rewrite line needs '->' (TARGET -> REPLACEMENT [/ ENV] [%tag])")
        target_text = text[:arrow]
        rest = text[arrow + 2:]

        # Explicit tag splits the line: everything after it may only be a comment.
        tag = "attested"
        comment = ""
        pct = self._find_outside(rest, "%")
        hash0 = self._find_outside(rest, "#")
        slash0 = self._find_outside(rest, "/")
        if hash0 >= 0 and (slash0 < 0 or hash0 < slash0) and (pct < 0 or hash0 < pct):
            # No environment before the '#': it starts a comment (which may contain '%').
            pct = -1
        if pct >= 0:
            m = re.match(r"%([A-Za-z]+)", rest[pct:])
            word = m.group(1) if m else ""
            if word not in TAGS:
                if 0 <= hash0 < pct:
                    raise self.err("comment after environment requires an explicit %tag "
                                   "(I-3: '#' inside an environment is the word edge)")
                raise self.err(f"unknown tag %{word!s}; expected one of "
                               + ", ".join("%" + t for t in TAGS))
            tag = word
            after = rest[pct + 1 + len(word):].strip()
            if after:
                if not after.startswith("#"):
                    raise self.err(f"unexpected text after %{tag}: {after!r}")
                comment = after[1:]
            body = rest[:pct]
        else:
            body = rest

        slash = self._find_outside(body, "/")
        if pct < 0:
            hash_pos = self._find_outside(body, "#")
            if hash_pos >= 0 and (slash < 0 or hash_pos < slash):
                comment = body[hash_pos + 1:]
                body = body[:hash_pos]
                slash = -1
        if slash >= 0:
            repl_text, env_text = body[:slash], body[slash + 1:]
        else:
            repl_text, env_text = body, None

        target = self._target(target_text)
        replacement = self._replacement(repl_text)
        left, right = self._environment(env_text, explicit_tag=pct >= 0)
        return Rule(section=self.section, line=self.line,
                    rule_id=f"{self.section}:{self.line}", target=target,
                    replacement=replacement, left=left, right=right, tag=tag,
                    comment=comment)

    # -- item scanner -------------------------------------------------------------------------

    def _scan(self, text: str) -> list[_Tok]:
        toks: list[_Tok] = []
        i, n = 0, len(text)
        while i < n:
            ch = text[i]
            if ch in " \t":
                i += 1
                continue
            optional = False
            if ch == "(":
                optional = True
                i += 1
                while i < n and text[i] in " \t":
                    i += 1
                if i >= n:
                    raise self.err("unclosed '('")
                ch = text[i]
            if ch == "[":
                j = text.find("]", i)
                if j < 0:
                    raise self.err("unclosed '['")
                tok = _Tok("bundle", text[i + 1:j])
                i = j + 1
            elif ch == "{":
                j = text.find("}", i)
                if j < 0:
                    raise self.err("unclosed '{'")
                tok = _Tok("set", text[i + 1:j])
                i = j + 1
            elif ch == '"':
                j = text.find('"', i + 1)
                if j < 0:
                    raise self.err("unclosed '\"'")
                tok = _Tok("quoted", text[i + 1:j])
                i = j + 1
            elif ch == "\\":
                if i + 1 >= n or text[i + 1] not in "123456789":
                    raise self.err("backreference must be \\1 .. \\9")
                tok = _Tok("backref", text[i + 1])
                i += 2
            elif ch in _SPECIALS or ch == "_":
                tok = _Tok("special", ch)
                i += 1
            elif ch in ")]}*:/%":
                raise self.err(f"unexpected {ch!r}")
            else:
                j = i
                while j < n:
                    c = text[j]
                    if c == "_" and _CLASS_RE.match(text[i:j]) and j + 1 < n \
                            and (text[j + 1].isupper() or text[j + 1].isdigit()
                                 or text[j + 1] == "_"):
                        j += 1
                        continue
                    if c in _TERMINATORS:
                        break
                    j += 1
                tok = _Tok("word", text[i:j])
                i = j
            # suffixes: ":n" capture, then "*"
            if i < n and text[i] == ":":
                if i + 1 >= n or text[i + 1] not in "123456789":
                    raise self.err("capture must be :1 .. :9")
                tok.capture = int(text[i + 1])
                i += 2
            if i < n and text[i] == "*":
                tok.star = True
                i += 1
            if optional:
                while i < n and text[i] in " \t":
                    i += 1
                if i >= n or text[i] != ")":
                    raise self.err("expected ')' after optional item")
                i += 1
                tok.optional = True
                if tok.star:
                    raise self.err("'(X*)' is not allowed: '()' and '*' do not combine (I-9)")
                if i < n and text[i] == "*":
                    raise self.err("'(X)*' is not allowed: '()' and '*' do not combine (I-9)")
            toks.append(tok)
        return toks

    # -- element builders ---------------------------------------------------------------------

    def _feature(self, name: str) -> str:
        if not name or not name[0].islower() or not name.isalpha():
            raise self.err(f"bad feature name {name!r}")
        try:
            return self.table.canonical_feature(name)
        except FeatureError:
            return name          # reported by `strands check` as UNKNOWN_FEATURE

    def _bundle(self, inner: str, *, change: bool) -> Bundle:
        parts = inner.split()
        if not parts:
            raise self.err("empty bundle '[]'")
        class_name: str | None = None
        constraints: dict[str, str] = {}
        for k, p in enumerate(parts):
            if p[0] in _SIGNS:
                if len(p) < 2:
                    raise self.err(f"feature spec {p!r} needs a name")
                constraints[self._feature(p[1:])] = _SIGNS[p[0]]
            elif k == 0 and _CLASS_RE.match(p):
                if change:
                    raise self.err(f"a feature-change bundle may not name a class ({p})")
                class_name = p
            else:
                raise self.err(f"bad bundle element {p!r}: expected ±feature"
                               + ("" if k else " or a class name"))
        if change and not constraints:
            raise self.err("a feature-change bundle needs at least one ±feature")
        return Bundle(class_name, constraints)

    def _set(self, inner: str) -> tuple[str, ...]:
        parts = inner.split()
        if not parts:
            raise self.err("empty set '{}'")
        for p in parts:
            if not _CLASS_RE.match(p) and p not in self.table:
                raise self.err(f"unknown segment {p!r} in set")
        return tuple(parts)

    def _item(self, tok: _Tok, where: str) -> ItemSpec:
        if tok.kind == "word":
            if tok.text == "0":
                raise self.err(f"'0' must stand alone in a {where}")
            if _CLASS_RE.match(tok.text):
                return ItemSpec("class", tok.text, tok.capture)
            if tok.text in self.table:
                return ItemSpec("segment", tok.text, tok.capture)
            raise self.err(f"unknown segment {tok.text!r} in {where}")
        if tok.kind == "bundle":
            return ItemSpec("bundle", self._bundle(tok.text, change=False), tok.capture)
        if tok.kind == "set":
            return ItemSpec("set", self._set(tok.text), tok.capture)
        if tok.kind == "quoted":
            raise self.err(f"quoted text is not allowed in a {where}")
        if tok.kind == "backref":
            raise self.err(f"a backreference is not allowed in a {where}")
        raise self.err(f"{tok.text!r} is not allowed in a {where} (context-only symbol)")

    def _target(self, text: str) -> tuple[ItemSpec, ...]:
        toks = self._scan(text)
        if not toks:
            raise self.err("empty target")
        if any(t.kind == "word" and t.text == "0" for t in toks):
            if len(toks) != 1:
                raise self.err("'0' must stand alone in a target")
            return ()
        out = []
        for t in toks:
            if t.optional or t.star:
                raise self.err("'()' and '*' are allowed only in the environment")
            out.append(self._item(t, "target"))
        return tuple(out)

    def _replacement(self, text: str) -> tuple[object, ...] | Bundle:
        toks = self._scan(text)
        if not toks:
            raise self.err("empty replacement (write 0 for deletion)")
        for t in toks:
            if t.optional or t.star or t.capture is not None:
                raise self.err("'()', '*' and captures are not allowed in a replacement")
        if len(toks) == 1 and toks[0].kind == "word" and toks[0].text == "0":
            return ()
        if any(t.kind == "bundle" for t in toks):
            if len(toks) != 1:
                raise self.err("a feature-change bundle must be the whole replacement")
            return self._bundle(toks[0].text, change=True)
        out: list[object] = []
        for t in toks:
            if t.kind == "word":
                if t.text == "0":
                    raise self.err("'0' must stand alone in a replacement")
                if _CLASS_RE.match(t.text):
                    raise self.err(f"bare class name {t.text!r} in a replacement; "
                                   "capture the item and use a backreference (I-5)")
                if t.text not in self.table:
                    raise self.err(f"unknown segment {t.text!r} in replacement")
                out.append(t.text)
            elif t.kind == "backref":
                out.append(Backref(int(t.text)))
            elif t.kind == "quoted":
                if self.section != "respell":
                    raise self.err("quoted text is allowed only in [respell]")
                out.append(QuotedText(t.text))
            elif t.kind == "set":
                raise self.err("an inline set is not allowed in a replacement")
            else:
                raise self.err(f"{t.text!r} is not allowed in a replacement")
        return tuple(out)

    def _ctx_seq(self, toks: list[_Tok], side: str) -> tuple[CtxItem, ...]:
        out: list[CtxItem] = []
        for k, t in enumerate(toks):
            if t.kind == "special":
                if t.capture is not None:
                    raise self.err(f"a capture cannot be attached to {t.text!r}")
                if t.text == "#":
                    edge_ok = (side == "left" and k == 0) or \
                              (side == "right" and k == len(toks) - 1) or \
                              (side == "ban" and k in (0, len(toks) - 1))
                    if not edge_ok:
                        raise self.err("comment after environment requires an explicit %tag "
                                       "(I-3: '#' inside an environment is the word edge)")
                out.append(CtxItem(t.text, optional=t.optional, star=t.star))
                continue
            if t.kind in ("quoted", "backref"):
                raise self.err(f"{t.kind} is not allowed in an environment")
            if t.capture is not None and (t.optional or t.star):
                raise self.err("a capture cannot be attached to an optional or starred item "
                               "(I-9)")
            out.append(CtxItem(self._item(t, "environment"), optional=t.optional, star=t.star))
        return tuple(out)

    def ctx_sequence(self, text: str) -> tuple[CtxItem, ...]:
        """A bare context sequence with no `_` (`[syllable] bans`, I-14). `#` may stand at
        either end as the word edge."""
        toks = self._scan(text)
        if not toks:
            raise self.err("empty context sequence")
        if any(t.kind == "special" and t.text == "_" for t in toks):
            raise self.err("'_' is not allowed here (a ban is a plain sequence, I-14)")
        return self._ctx_seq(toks, "ban")

    def _environment(self, text: str | None, *, explicit_tag: bool
                     ) -> tuple[tuple[CtxItem, ...], tuple[CtxItem, ...]]:
        if text is None:
            return (), ()
        toks = self._scan(text)
        slots = [k for k, t in enumerate(toks) if t.kind == "special" and t.text == "_"]
        if len(slots) != 1:
            raise self.err("environment needs exactly one '_'")
        k = slots[0]
        if toks[k].optional or toks[k].star or toks[k].capture is not None:
            raise self.err("'_' takes no suffix")
        return self._ctx_seq(toks[:k], "left"), self._ctx_seq(toks[k + 1:], "right")


# ---- file parser ----------------------------------------------------------------------------

def _strip_comment(text: str) -> str:
    """Drop a trailing `# ...` from a non-rewrite entry line."""
    i = text.find("#")
    return text if i < 0 else text[:i]


def _key_value(text: str, line: int, path: str) -> tuple[str, str]:
    key, eq, value = text.partition("=")
    key, value = key.strip(), value.strip()
    if not eq or not key:
        raise ParseError("expected 'key = value'", line, path)
    if not _NAME_RE.match(key):
        raise ParseError(f"bad key {key!r}", line, path)
    return key, value


def _strip_comment_quoted(text: str) -> str:
    """Drop a trailing `# ...` that is outside double quotes (for `[templates]`)."""
    quoted = False
    for i, ch in enumerate(text):
        if ch == '"':
            quoted = not quoted
        elif ch == "#" and not quoted:
            return text[:i]
    return text


def _cluster(token: str, table: FeatureTable, line: int, path: str, where: str
             ) -> tuple[str, ...]:
    """A CLUSTER token: longest-match tokenized into one or more segments."""
    if any(ch in token for ch in "#$.ˈˌ "):
        raise ParseError(f"cluster {token!r} in {where} may only contain segments", line, path)
    try:
        segs = tokenize(token, table).segments
    except SegmentError as e:
        raise ParseError(f"unknown segment in cluster {token!r} in {where}: {e}",
                         line, path) from None
    if not segs:
        raise ParseError(f"empty cluster in {where}", line, path)
    return segs


def _cluster_list(value: str, table: FeatureTable, line: int, path: str, where: str
                  ) -> tuple[tuple[str, ...], ...]:
    tokens = value.split()
    if not tokens:
        raise ParseError(f"{where} needs at least one cluster (or 'any')", line, path)
    out: list[tuple[str, ...]] = []
    for tok in tokens:
        cl = _cluster(tok, table, line, path, where)
        if cl not in out:
            out.append(cl)
    return tuple(out)


def _tiered_list(value: str, table: FeatureTable, line: int, path: str, where: str
                 ) -> dict[tuple[str, ...], str]:
    out: dict[tuple[str, ...], str] = {}
    tokens = value.split()
    if not tokens:
        raise ParseError(f"{where} needs at least one CLUSTER:TIER pair", line, path)
    for tok in tokens:
        cluster, colon, tier = tok.rpartition(":")
        if not colon or not cluster or not _TIER_RE.match(tier):
            raise ParseError(f"bad tier item {tok!r} in {where}: expected CLUSTER:TIER "
                             "with TIER matching [A-Z][A-Z0-9]*", line, path)
        out[_cluster(cluster, table, line, path, where)] = tier
    return out


def _template_slots(value: str, line: int, path: str) -> tuple[tuple[str, bool], ...]:
    """`(C)(C)N(C)(C)` -> ((slot, optional), ...). Slots are C, V, N or a class name."""
    out: list[tuple[str, bool]] = []
    i, n = 0, len(value)
    while i < n:
        ch = value[i]
        if ch in " \t":
            i += 1
            continue
        optional = ch == "("
        if optional:
            i += 1
        j = i
        while j < n and (value[j].isupper() or value[j].isdigit() or value[j] == "_"):
            j += 1
        slot = value[i:j]
        if not slot or not _CLASS_RE.match(slot):
            raise ParseError(f"bad template slot at {value[i:]!r}: expected C, V, N or a "
                             "class name, optionally in ()", line, path)
        i = j
        if optional:
            if i >= n or value[i] != ")":
                raise ParseError(f"unclosed '(' in template {value!r}", line, path)
            i += 1
        out.append((slot, optional))
    if not out:
        raise ParseError("empty template", line, path)
    return tuple(out)


class _SyllableBuilder:
    def __init__(self, path: str, table: FeatureTable) -> None:
        self.path = path
        self.table = table
        self.seen: dict[str, int] = {}
        self.template: tuple[tuple[str, bool], ...] | None = None
        self.nuclei: tuple[tuple[str, ...], ...] = ()
        self.onsets: tuple[tuple[str, ...], ...] | None = None
        self.codas: tuple[tuple[str, ...], ...] | None = None
        self.onset_tiers: dict[tuple[str, ...], str] = {}
        self.coda_tiers: dict[tuple[str, ...], str] = {}
        self.onset_required = False
        self.appendix: tuple[str, ...] = ()
        self.domain = "word"
        self.sonority = False
        self.bans: list[tuple[CtxItem, ...]] = []

    def entry(self, line: str, lineno: int) -> None:
        path, table = self.path, self.table
        key, _, rest = line.partition("=")
        key = key.strip()
        if key not in _SYLLABLE_KEYS:
            raise ParseError(f"unknown [syllable] key {key!r}; expected one of "
                             + ", ".join(sorted(_SYLLABLE_KEYS)), lineno, path)
        if key != "bans":
            if key in self.seen:
                raise ParseError(f"[syllable] {key} given twice (first at line "
                                 f"{self.seen[key]})", lineno, path)
            self.seen[key] = lineno
            _, value = _key_value(_strip_comment(line), lineno, path)
        else:
            value = rest.strip()      # context sequence: `#` is the word edge (I-3)
        if not value:
            raise ParseError(f"[syllable] {key} has no value", lineno, path)
        if key == "template":
            self.template = None if value == "any" else _template_slots(value, lineno, path)
        elif key == "nuclei":
            self.nuclei = _cluster_list(value, table, lineno, path, "nuclei")
            for nuc in self.nuclei:
                if len(nuc) < 2:
                    raise ParseError(f"nucleus {''.join(nuc)!r} is a single segment; `nuclei` "
                                     "lists licensed vowel SEQUENCES (I-2)", lineno, path)
        elif key == "onsets":
            self.onsets = None if value == "any" else \
                _cluster_list(value, table, lineno, path, "onsets")
        elif key == "codas":
            self.codas = None if value == "any" else \
                _cluster_list(value, table, lineno, path, "codas")
        elif key == "onsets-tier":
            self.onset_tiers = _tiered_list(value, table, lineno, path, "onsets-tier")
        elif key == "codas-tier":
            self.coda_tiers = _tiered_list(value, table, lineno, path, "codas-tier")
        elif key == "onset-required":
            if value not in ("yes", "no"):
                raise ParseError("onset-required must be yes or no", lineno, path)
            self.onset_required = value == "yes"
        elif key == "appendix":
            segs = value.split()
            for seg in segs:
                if seg not in table:
                    raise ParseError(f"unknown segment {seg!r} in appendix", lineno, path)
            self.appendix = tuple(segs)
        elif key == "domain":
            if value not in ("word", "stem"):
                raise ParseError("domain must be word or stem", lineno, path)
            self.domain = value
        elif key == "sonority":
            if value not in ("on", "off"):
                raise ParseError("sonority must be on or off", lineno, path)
            self.sonority = value == "on"
        elif key == "bans":
            self.bans.append(_LineParser("syllable", lineno, path, table).ctx_sequence(value))

    def build(self) -> SyllableSpec:
        return SyllableSpec(
            template=self.template, nuclei=self.nuclei,
            onsets=self.onsets, codas=self.codas,
            onset_set=None if self.onsets is None else frozenset(self.onsets),
            coda_set=None if self.codas is None else frozenset(self.codas),
            onset_tiers=self.onset_tiers, coda_tiers=self.coda_tiers,
            onset_required=self.onset_required, appendix=self.appendix,
            domain=self.domain, sonority=self.sonority, bans=tuple(self.bans))


class _TemplateParser:
    """`NAME = t-item { t-item }` (I-16). Items: "quoted", ARG, FUNC(item), FUNC; `?` suffix."""

    def __init__(self, line: int, path: str) -> None:
        self.line, self.path = line, path

    def err(self, message: str) -> ParseError:
        return ParseError(message, self.line, self.path)

    def parse(self, text: str) -> tuple[TemplateItem, ...]:
        self.text, self.i = text, 0
        items: list[TemplateItem] = []
        self._ws()
        while self.i < len(self.text):
            items.append(self._item())
            self._ws()
        if not items:
            raise self.err("template has no items")
        return tuple(items)

    def _ws(self) -> None:
        while self.i < len(self.text) and self.text[self.i] in " \t":
            self.i += 1

    def _item(self) -> TemplateItem:
        text = self.text
        if text[self.i] == '"':
            j = text.find('"', self.i + 1)
            if j < 0:
                raise self.err("unclosed '\"' in template")
            item = TemplateItem("literal", text[self.i + 1:j])
            self.i = j + 1
        else:
            j = self.i
            while j < len(text) and (text[j].isalnum() or text[j] == "_"):
                j += 1
            name = text[self.i:j]
            if not name:
                raise self.err(f"unexpected {text[self.i]!r} in template")
            self.i = j
            if name in TEMPLATE_ARGS:
                item = TemplateItem("arg", name)
            elif name in TEMPLATE_FUNCS:
                self._ws()
                if self.i < len(text) and text[self.i] == "(":
                    self.i += 1
                    self._ws()
                    if self.i >= len(text) or text[self.i] == ")":
                        raise self.err(f"{name}() needs an argument")
                    child = self._item()
                    self._ws()
                    if self.i >= len(text) or text[self.i] != ")":
                        raise self.err(f"expected ')' after the argument of {name}")
                    self.i += 1
                    item = TemplateItem("call", name, child)
                else:
                    item = TemplateItem("call", name)   # applied to the head (I-16, R1)
            else:
                raise self.err(f"unknown template item {name!r}: expected a quoted literal, "
                               "an argument (" + ", ".join(TEMPLATE_ARGS) + ") or a function ("
                               + ", ".join(TEMPLATE_FUNCS) + ")")
        if self.i < len(text) and text[self.i] == "?":
            self.i += 1
            item = TemplateItem(item.kind, item.value, item.child, True)
        return item


def _epithet(line: str, lineno: int, path: str, table: FeatureTable) -> Epithet:
    """`NAME = SEGMENT { SEGMENT } / environment` (I-18). Everything after `/` is the
    environment, in which `#` is the word edge (I-3)."""
    name, eq, rest = line.partition("=")
    name = name.strip()
    if not eq or not _NAME_RE.match(name):
        raise ParseError("expected 'NAME = form / environment'", lineno, path)
    form_text, slash, env_text = rest.partition("/")
    if not slash:
        raise ParseError(f"epithet {name} needs '/ environment' (I-18)", lineno, path)
    form = tuple(form_text.split())
    if not form:
        raise ParseError(f"epithet {name} has an empty form", lineno, path)
    for seg in form:
        if seg not in table:
            raise ParseError(f"unknown segment {seg!r} in epithet {name}", lineno, path)
    lp = _LineParser("epithets", lineno, path, table)
    left, right = lp._environment(env_text, explicit_tag=True)
    return Epithet(name, form, left, right)


def parse_rules(text: str, table: FeatureTable, path: str = "<string>") -> RuleFile:
    text = unicodedata.normalize("NFC", text)
    meta: dict[str, str] = {}
    inventory: list[str] = []
    marginal: set[str] = set()
    user_classes: dict[str, tuple[str, ...]] = {}
    weights: dict[str, float] = {}
    sections: dict[str, list[Rule]] = {name: [] for name in REWRITE_SECTIONS}
    syllable: _SyllableBuilder | None = None
    stress_procedure: str | None = None
    stress_params: dict[str, str] = {}
    stress_line: int | None = None
    epithets: dict[str, Epithet] = {}
    templates: dict[str, tuple[TemplateItem, ...]] = {}
    subtables: dict[str, dict[str, list[Rule]]] = {name: {} for name in SUBTABLE_SECTIONS}
    current_subtable: str | None = None
    cluster_fallback: str | None = None
    section: str | None = None

    for lineno, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        header = _SECTION_RE.match(line)
        if header:
            name = header.group(1)
            if name not in SECTION_NAMES:
                raise ParseError(f"unknown section [{name}]", lineno, path)
            section = name
            current_subtable = None
            if name == "syllable" and syllable is None:
                syllable = _SyllableBuilder(path, table)
            if name == "stress" and stress_line is None:
                stress_line = lineno
            continue
        if section is None:
            raise ParseError("entry before any [section] header", lineno, path)

        if section in REWRITE_SECTIONS:
            if section == "repair" and re.match(r"cluster-fallback\s*=", line):
                _, value = _key_value(_strip_comment(line), lineno, path)
                if value != "same-length":
                    raise ParseError(f"cluster-fallback must be 'same-length', not {value!r} "
                                     "(spec §12.E)", lineno, path)
                if cluster_fallback is not None:
                    raise ParseError("cluster-fallback given twice", lineno, path)
                cluster_fallback = value
                continue
            sections[section].append(_LineParser(section, lineno, path, table).parse(line))
        elif section in SUBTABLE_SECTIONS:
            head = _SUBTABLE_HEAD_RE.match(line)
            if head and "->" not in line:
                current_subtable = head.group(1)
                if current_subtable in subtables[section]:
                    raise ParseError(f"[{section}] table {current_subtable} declared twice",
                                     lineno, path)
                subtables[section][current_subtable] = []
                continue
            if current_subtable is None:
                raise ParseError(f"[{section}] rule before any 'NAME:' sub-table head (I-15)",
                                 lineno, path)
            subtables[section][current_subtable].append(
                _LineParser(section, lineno, path, table).parse(line))
        elif section == "syllable":
            assert syllable is not None
            syllable.entry(line, lineno)
        elif section == "stress":
            key, value = _key_value(_strip_comment(line), lineno, path)
            if key == "procedure":
                if value not in STRESS_PROCEDURES:
                    raise ParseError(f"unknown stress procedure {value!r}; expected one of "
                                     + ", ".join(STRESS_PROCEDURES), lineno, path)
                if stress_procedure is not None:
                    raise ParseError("stress procedure given twice", lineno, path)
                stress_procedure = value
            else:
                if stress_procedure is None:
                    raise ParseError("[stress] parameters must follow 'procedure = ...' "
                                     "(I-17)", lineno, path)
                if key in stress_params:
                    raise ParseError(f"stress parameter {key} given twice", lineno, path)
                stress_params[key] = value
        elif section == "epithets":
            ep = _epithet(line, lineno, path, table)
            if ep.name in epithets:
                raise ParseError(f"epithet {ep.name} declared twice", lineno, path)
            epithets[ep.name] = ep
        elif section == "templates":
            key, value = _key_value(_strip_comment_quoted(line), lineno, path)
            if key in templates:
                raise ParseError(f"template {key} declared twice", lineno, path)
            templates[key] = _TemplateParser(lineno, path).parse(value)
        elif section == "meta":
            key, value = _key_value(_strip_comment(line), lineno, path)
            meta[key] = value
        elif section == "inventory":
            body = _strip_comment(line).strip()
            is_marginal = body.startswith("marginal:")
            if is_marginal:
                body = body[len("marginal:"):]
            for seg in body.split():
                if seg not in table:
                    raise ParseError(f"unknown segment {seg!r} in [inventory]", lineno, path)
                if seg not in inventory:
                    inventory.append(seg)
                if is_marginal:
                    marginal.add(seg)
        elif section == "classes":
            key, value = _key_value(_strip_comment(line), lineno, path)
            if not _CLASS_RE.match(key):
                raise ParseError(f"class name {key!r} must match [A-Z][A-Z0-9_]*", lineno, path)
            members = value.split()
            if not members:
                raise ParseError(f"class {key} has no members", lineno, path)
            for seg in members:
                if seg not in table:
                    raise ParseError(f"unknown segment {seg!r} in class {key}", lineno, path)
            user_classes[key] = tuple(members)
        elif section == "weights":
            key, value = _key_value(_strip_comment(line), lineno, path)
            try:
                feature = table.canonical_feature(key)
            except FeatureError:
                raise ParseError(f"unknown feature {key!r} in [weights]", lineno, path) from None
            try:
                weights[feature] = float(value)
            except ValueError:
                raise ParseError(f"bad weight {value!r} for {key}", lineno, path) from None
        else:  # pragma: no cover - every SECTION_NAMES member is handled above
            raise ParseError(f"unhandled section [{section}]", lineno, path)

    # I-11: predeclared classes over this file's inventory first, then the rest of the table
    # (the Irish inventory is a subset of the table; irish.rules is not available at parse
    # time, so the whole table stands in). A [classes] redeclaration overrides.
    over = list(inventory) + [s for s in table.segments if s not in inventory]
    classes: dict[str, tuple[str, ...]] = {
        name: table.derived_class(name, over) for name in DERIVED_CLASSES}
    classes.update(user_classes)

    stress: StressSpec | None = None
    if stress_line is not None:
        if stress_procedure is None:
            raise ParseError("[stress] needs 'procedure = ...'", stress_line, path)
        stress = StressSpec(stress_procedure, stress_params)

    return RuleFile(
        path=str(path),
        meta=meta,
        inventory=tuple(inventory),
        marginal=frozenset(marginal),
        classes=classes,
        weights=weights,
        sections={name: tuple(rules) for name, rules in sections.items()},
        syllable=None if syllable is None else syllable.build(),
        stress=stress,
        epithets=epithets,
        templates=templates,
        mutations={k: tuple(v) for k, v in subtables["mutations"].items()},
        inflect={k: tuple(v) for k, v in subtables["inflect"].items()},
        cluster_fallback=cluster_fallback,
    )


def parse_rules_file(path: str | Path, table: FeatureTable) -> RuleFile:
    path = Path(path)
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as e:
        raise ParseError(f"cannot read rule file: {e}", 0, str(path)) from e
    return parse_rules(text, table, str(path))
