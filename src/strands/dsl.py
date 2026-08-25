"""Rule-file DSL parser: file skeleton, simple sections, rewrite lines.

Plan Task 5a (core) — spec §3 (rule DSL) and §12.C (inline sets, captures/backreferences,
feature aliases, quoted respell output); the plan's EBNF is the grammar implemented here.
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

Sections `[syllable] [stress] [epithets] [templates] [mutations] [inflect]` and the
`[repair]` `cluster-fallback` directive belong to Task 5b and raise NotImplementedError
when an entry line appears under them.
"""
from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

from .features import FeatureError, FeatureTable, DERIVED_CLASSES

__all__ = [
    "Bundle", "ItemSpec", "CtxItem", "Rule", "Backref", "QuotedText", "RuleFile",
    "ParseError", "parse_rules", "parse_rules_file",
    "SECTION_NAMES", "REWRITE_SECTIONS", "TAGS",
]

SECTION_NAMES: tuple[str, ...] = (
    "meta", "inventory", "classes", "weights", "substitute", "syllable", "repair",
    "post-stress", "stress", "epithets", "respell", "templates", "mutations", "inflect",
    "normalize",
)
REWRITE_SECTIONS: tuple[str, ...] = ("substitute", "repair", "post-stress", "respell", "normalize")
_TASK_5B_SECTIONS: frozenset[str] = frozenset(
    ("syllable", "stress", "epithets", "templates", "mutations", "inflect"))
TAGS: tuple[str, ...] = ("attested", "design", "fallback")

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
class RuleFile:
    path: str
    meta: dict[str, str]
    inventory: tuple[str, ...]
    marginal: frozenset[str]
    classes: dict[str, tuple[str, ...]]     # user + derived (I-11)
    weights: dict[str, float]
    sections: dict[str, tuple[Rule, ...]]
    syllable: object | None = None          # SyllableSpec, Task 5b
    stress: object | None = None            # StressSpec, Task 5b
    epithets: dict[str, object] = field(default_factory=dict)             # Task 5b
    templates: dict[str, tuple[object, ...]] = field(default_factory=dict)  # Task 5b
    mutations: dict[str, tuple[Rule, ...]] = field(default_factory=dict)  # Task 5b
    inflect: dict[str, tuple[Rule, ...]] = field(default_factory=dict)    # Task 5b


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
                              (side == "right" and k == len(toks) - 1)
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


def parse_rules(text: str, table: FeatureTable, path: str = "<string>") -> RuleFile:
    text = unicodedata.normalize("NFC", text)
    meta: dict[str, str] = {}
    inventory: list[str] = []
    marginal: set[str] = set()
    user_classes: dict[str, tuple[str, ...]] = {}
    weights: dict[str, float] = {}
    sections: dict[str, list[Rule]] = {name: [] for name in REWRITE_SECTIONS}
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
            continue
        if section is None:
            raise ParseError("entry before any [section] header", lineno, path)

        if section in REWRITE_SECTIONS:
            if section == "repair" and re.match(r"cluster-fallback\s*=", line):
                raise NotImplementedError(
                    f"{path}:{lineno}: [repair] cluster-fallback directive is Task 5b")
            sections[section].append(_LineParser(section, lineno, path, table).parse(line))
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
        elif section in _TASK_5B_SECTIONS:
            raise NotImplementedError(f"{path}:{lineno}: [{section}] entries are Task 5b")
        else:  # pragma: no cover - every SECTION_NAMES member is handled above
            raise ParseError(f"unhandled section [{section}]", lineno, path)

    # I-11: predeclared classes over this file's inventory first, then the rest of the table
    # (the Irish inventory is a subset of the table; irish.rules is not available at parse
    # time, so the whole table stands in). A [classes] redeclaration overrides.
    over = list(inventory) + [s for s in table.segments if s not in inventory]
    classes: dict[str, tuple[str, ...]] = {
        name: table.derived_class(name, over) for name in DERIVED_CLASSES}
    classes.update(user_classes)

    return RuleFile(
        path=str(path),
        meta=meta,
        inventory=tuple(inventory),
        marginal=frozenset(marginal),
        classes=classes,
        weights=weights,
        sections={name: tuple(rules) for name, rules in sections.items()},
    )


def parse_rules_file(path: str | Path, table: FeatureTable) -> RuleFile:
    path = Path(path)
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as e:
        raise ParseError(f"cannot read rule file: {e}", 0, str(path)) from e
    return parse_rules(text, table, str(path))
