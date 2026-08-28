"""Static checks over a parsed rule file (plan Task 6; spec §12.C for UNREACHABLE_CHANGE).

`check_rule_file` never raises for a finding: it returns every finding at once, sorted by
line then code, so `strands check` can list them. Severity "error" fails the CLI; "warning"
(only OFF_INVENTORY: irish.rules legitimately emits Irish segments) does not.

Line numbers: rewrite rules carry their own line. `[syllable]`, `[stress]` and `[templates]`
entries do not (the parser keeps no line for them), so those findings are located by
re-reading the file at `rf.path` and finding the entry's `key =` line inside its section;
when the file is not readable (a rule file parsed from a string) the line is 0.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from .dsl import (
    TEMPLATE_ARGS,
    Backref,
    Bundle,
    CtxItem,
    ItemSpec,
    Rule,
    RuleFile,
    TemplateItem,
    template_functions,
)
from .features import FeatureError, FeatureTable
from .stress.params import PROCEDURE_PARAMS

__all__ = ["CheckError", "check_grapheme_table", "check_lexicon_file", "check_rule_file"]

_CLASS_RE = re.compile(r"[A-Z][A-Z0-9_]*\Z")
_TEMPLATE_SPECIAL_SLOTS = frozenset({"C", "V", "N"})


@dataclass(frozen=True)
class CheckError:
    line: int
    code: str  # UNKNOWN_CLASS | UNKNOWN_FEATURE | OFF_INVENTORY | EPENTHESIS_NO_CONTEXT
    # | UNKNOWN_STRESS_PARAM | UNREACHABLE_CHANGE | CLUSTER_OFF_INVENTORY
    # | BAD_TEMPLATE_ARG | UNDEFINED_BACKREF | NUCLEUS_OFF_INVENTORY
    # | ORTH_UNKNOWN_UNIT | ORTH_BAD_POSITION (Old Irish Task 6, R9)
    # | GRAPHEME_UNKNOWN_TOKEN (Old Irish Task 14)
    message: str
    severity: str  # "error" | "warning"


class _Checker:
    def __init__(self, rf: RuleFile, table: FeatureTable) -> None:
        self.rf = rf
        self.table = table
        self.inventory = frozenset(rf.inventory)
        self.out: list[CheckError] = []
        self._lines: list[str] | None = None
        self._orth_units: dict[str, int] | None = None  # unit -> max alternative length

    def add(self, line: int, code: str, message: str, severity: str = "error") -> None:
        self.out.append(CheckError(line, code, message, severity))

    # -- locating non-rule entries ---------------------------------------------------------------

    def locate(self, section: str, key: str) -> int:
        """Line of the first `key =` entry in `[section]` of the file at rf.path, else 0."""
        if self._lines is None:
            try:
                self._lines = Path(self.rf.path).read_text(encoding="utf-8").splitlines()
            except (OSError, ValueError):
                self._lines = []
        current: str | None = None
        for lineno, raw in enumerate(self._lines, 1):
            line = raw.strip()
            head = re.match(r"\[\s*([a-z-]+)\s*\]\s*(?:#.*)?\Z", line)
            if head:
                current = head.group(1)
                continue
            if current == section and re.match(rf"{re.escape(key)}\s*=", line):
                return lineno
        return 0

    # -- element visitors ------------------------------------------------------------------------

    def orth(self, tag: str, line: int) -> None:
        """`@orth("X")` / `orth="X"` (Old Irish O-6; R9): `X`, less a `:n` positional
        suffix, must be a unit of `rules/irish-orthography.csv`, else the item can never
        match — an ERROR, since draft 1's warning let dead rules through. `n` must lie
        within the unit's longest alternative."""
        if self._orth_units is None:
            from .orth import load_orth_table

            self._orth_units = {
                unit: max(len(alt) for alt in alts) for unit, alts in load_orth_table()
            }
        unit, sep, suffix = tag.rpartition(":")
        if not (sep and suffix.isdigit()):
            unit, suffix = tag, ""
        arity = self._orth_units.get(unit)
        if arity is None:
            self.add(
                line,
                "ORTH_UNKNOWN_UNIT",
                f"orth unit {unit!r} is not in rules/irish-orthography.csv; "
                f"@orth({tag!r}) can never match",
            )
            return
        if suffix:
            n = int(suffix)
            if arity < 2:
                self.add(
                    line,
                    "ORTH_BAD_POSITION",
                    f"orth unit {unit!r} is single-segment, so its tag carries no "
                    f"position; @orth({tag!r}) can never match",
                )
            elif not 1 <= n <= arity:
                self.add(
                    line,
                    "ORTH_BAD_POSITION",
                    f"orth unit {unit!r} has at most {arity} segments; position {n} "
                    f"of @orth({tag!r}) can never match",
                )

    def class_name(self, name: str, line: int) -> None:
        if name not in self.rf.classes:
            self.add(line, "UNKNOWN_CLASS", f"class {name} is not declared")

    def bundle(self, b: Bundle, line: int) -> bool:
        """Report the bundle's problems; True when every feature name is known."""
        if b.class_name is not None:
            self.class_name(b.class_name, line)
        if b.orth is not None:
            self.orth(b.orth, line)
        ok = True
        for feature in b.constraints:
            try:
                self.table.canonical_feature(feature)
            except FeatureError:
                ok = False
                self.add(line, "UNKNOWN_FEATURE", f"unknown feature {feature!r}")
        return ok

    def item(self, it: ItemSpec, line: int) -> None:
        if it.kind == "class":
            self.class_name(it.value, line)  # type: ignore[arg-type]
        elif it.kind == "bundle":
            self.bundle(it.value, line)  # type: ignore[arg-type]
        elif it.kind == "set":
            for member in it.value:  # type: ignore[union-attr]
                if _CLASS_RE.match(member):
                    self.class_name(member, line)
        elif it.kind == "orth":
            self.orth(it.value, line)  # type: ignore[arg-type]

    def context(self, seq: tuple[CtxItem, ...], line: int) -> None:
        for c in seq:
            if isinstance(c.atom, ItemSpec):
                self.item(c.atom, line)

    def matching_segments(self, it: ItemSpec) -> list[str]:
        """Inventory segments an item can match (empty when the item names unknown things).
        An `@orth` item matches by provenance, not phonology: []. A bundle carrying `orth=`
        returns what its class/feature half matches."""
        inv = list(self.rf.inventory)
        if it.kind == "orth":
            return []
        if it.kind == "segment":
            return [it.value] if it.value in self.inventory else []  # type: ignore
        if it.kind == "class":
            return [s for s in self.rf.classes.get(it.value, ()) if s in self.inventory]
        if it.kind == "set":
            out: list[str] = []
            for member in it.value:  # type: ignore
                if _CLASS_RE.match(member):
                    out.extend(s for s in self.rf.classes.get(member, ()) if s in self.inventory)
                elif member in self.inventory:
                    out.append(member)
            return out
        b: Bundle = it.value  # type: ignore
        pool = (
            inv
            if b.class_name is None
            else [s for s in self.rf.classes.get(b.class_name, ()) if s in self.inventory]
        )
        try:
            return [s for s in pool if self.table.matches(s, b.constraints)]
        except FeatureError:
            return []

    # -- rules -----------------------------------------------------------------------------------

    def rule(self, r: Rule) -> None:
        line = r.line
        for it in r.target:
            self.item(it, line)
        self.context(r.left, line)
        self.context(r.right, line)

        # 4. epenthesis needs an environment (I-7)
        if not r.target and not r.left and not r.right:
            self.add(
                line,
                "EPENTHESIS_NO_CONTEXT",
                "epenthesis (target 0) needs a non-empty environment (I-7)",
            )

        captures = {it.capture for it in r.target if it.capture is not None}
        for side in (r.left, r.right):
            for c in side:
                if isinstance(c.atom, ItemSpec) and c.atom.capture is not None:
                    captures.add(c.atom.capture)

        if isinstance(r.replacement, Bundle):
            # 6. change bundle resolves by exact lookup for EVERY segment each target
            #    position can match: rewrite._replacement applies it to each matched segment,
            #    so one failing candidate is a runtime RuleError (spec §12.C).
            if self.bundle(r.replacement, line):
                failing: list[str] = []
                for it in r.target:
                    candidates = self.matching_segments(it)
                    if not candidates and it.kind == "segment":
                        candidates = [it.value]  # type: ignore[list-item]
                    for seg in candidates:
                        try:
                            self.table.apply_changes(seg, r.replacement.constraints)
                        except FeatureError:
                            if seg not in failing:
                                failing.append(seg)
                if failing:
                    self.add(
                        line,
                        "UNREACHABLE_CHANGE",
                        "no features.csv segment has the vector produced by the "
                        "feature-change bundle for "
                        + ", ".join(repr(s) for s in failing)
                        + " (spec §12.C)",
                    )
            return

        for el in r.replacement:
            if isinstance(el, str):
                # 3. off-inventory replacement segment: a warning
                if el not in self.inventory:
                    self.add(
                        line,
                        "OFF_INVENTORY",
                        f"replacement segment {el!r} is not in [inventory]",
                        "warning",
                    )
            elif isinstance(el, Backref):
                # 9. every \n has a matching :n capture in the same rule
                if el.n not in captures:
                    self.add(
                        line,
                        "UNDEFINED_BACKREF",
                        f"backreference \\{el.n} has no :{el.n} capture in this rule",
                    )

    # -- sections --------------------------------------------------------------------------------

    def syllable(self) -> None:
        sy = self.rf.syllable
        if sy is None:
            return
        # 7. cluster/appendix/nuclei segments in inventory
        for key, clusters in (
            ("onsets", sy.onsets),
            ("codas", sy.codas),
            ("onsets-tier", tuple(sy.onset_tiers)),
            ("codas-tier", tuple(sy.coda_tiers)),
            ("appendix", tuple((s,) for s in sy.appendix)),
        ):
            if not clusters:
                continue
            line = self.locate("syllable", key)
            for cl in clusters:
                for seg in cl:
                    if seg not in self.inventory:
                        self.add(
                            line,
                            "CLUSTER_OFF_INVENTORY",
                            f"[syllable] {key}: segment {seg!r} of {''.join(cl)!r} "
                            "is not in [inventory]",
                        )
        if sy.nuclei:
            line = self.locate("syllable", "nuclei")
            for nuc in sy.nuclei:
                for seg in nuc:
                    if seg not in self.inventory:
                        self.add(
                            line,
                            "NUCLEUS_OFF_INVENTORY",
                            f"[syllable] nuclei: segment {seg!r} of {''.join(nuc)!r} "
                            "is not in [inventory]",
                        )
        if sy.template:
            line = self.locate("syllable", "template")
            for slot, _ in sy.template:
                if slot not in _TEMPLATE_SPECIAL_SLOTS:
                    self.class_name(slot, line)
        if sy.bans:
            line = self.locate("syllable", "bans")
            for ban in sy.bans:
                self.context(ban, line)

    def stress(self) -> None:
        st = self.rf.stress
        if st is None:
            return
        # 5. procedure known and params ⊆ registry
        allowed = PROCEDURE_PARAMS.get(st.procedure)
        line = self.locate("stress", "procedure")
        if allowed is None:
            self.add(line, "UNKNOWN_STRESS_PARAM", f"unknown stress procedure {st.procedure!r}")
            return
        for key in st.params:
            if key not in allowed:
                where = self.locate("stress", key) or line
                self.add(
                    where,
                    "UNKNOWN_STRESS_PARAM",
                    f"procedure {st.procedure} does not take parameter {key!r}"
                    + (
                        f" (allowed: {', '.join(sorted(allowed))})"
                        if allowed
                        else " (it takes none)"
                    ),
                )

    def templates(self) -> None:
        # 8. every arg name is from the fixed set (I-16); every function name is in the
        # file's own registry (Old Irish spec §11, GPT #7) — the same `template_functions`
        # the parser validates against, so the two cannot drift.
        legal = template_functions(self.rf)

        def visit(item: TemplateItem, line: int) -> None:
            if item.kind == "arg" and item.value not in TEMPLATE_ARGS:
                self.add(line, "BAD_TEMPLATE_ARG", f"unknown template argument {item.value!r}")
            elif item.kind == "call" and item.value not in legal:
                self.add(
                    line,
                    "BAD_TEMPLATE_ARG",
                    f"unknown template function {item.value!r} "
                    f"(not a sub-table of this file nor in [meta] template-functions)",
                )
            if item.child is not None:
                visit(item.child, line)

        for name, items in self.rf.templates.items():
            line = self.locate("templates", name)
            for item in items:
                visit(item, line)

    def epithets(self) -> None:
        for name, ep in self.rf.epithets.items():
            line = self.locate("epithets", name)
            self.context(ep.left, line)
            self.context(ep.right, line)

    def grapheme_rules(self) -> None:
        """Old Irish Task 14 (O-10): every target and replacement token of a `[mutations]`
        / `[inflect]` line of a `grammar = graphemes` file must be a token of the grapheme
        table named by `[meta] orthography` (else the Old Irish default). The parser already
        refuses unknown tokens, so this catches a table edited AFTER the rule file was
        written, or a `GraphemeRule` built by hand. `V`, `C` and inline sets are checked by
        member; `#` is an environment atom and never a target."""
        tables = [t for t in (self.rf.grapheme_mutations, self.rf.grapheme_inflect) if t]
        if not tables:
            return
        from .spelled import OI_ORTHOGRAPHY_PATH, SpelledError, load_graphemes

        path = OI_ORTHOGRAPHY_PATH
        orthography = self.rf.meta.get("orthography")
        if orthography:
            path = Path(orthography)
            if not path.is_absolute():
                path = OI_ORTHOGRAPHY_PATH.parents[1] / path
        try:
            tokens = frozenset(r.token for r in load_graphemes(path))
        except (OSError, SpelledError) as e:
            self.add(0, "GRAPHEME_UNKNOWN_TOKEN", f"cannot load grapheme table {path}: {e}")
            return

        def atoms(seq: tuple[str, ...]) -> list[str]:
            out: list[str] = []
            for a in seq:
                if a in ("V", "C", "#"):
                    continue
                if a.startswith("{") and a.endswith("}"):
                    out.extend(a[1:-1].split())
                else:
                    out.append(a)
            return out

        for table in tables:
            for name, rules in table.items():
                for r in rules:
                    for where, seq in (("target", r.target), ("replacement", r.replacement)):
                        for tok in atoms(seq):
                            if tok not in tokens:
                                self.add(
                                    r.line,
                                    "GRAPHEME_UNKNOWN_TOKEN",
                                    f"[{r.rule_id.partition(':')[0]}] {name}: {where} "
                                    f"token {tok!r} is not in {path.name}",
                                )

    def run(self) -> list[CheckError]:
        for rules in self.rf.sections.values():
            for r in rules:
                self.rule(r)
        for table in (self.rf.mutations, self.rf.inflect):
            for rules in table.values():
                for r in rules:
                    self.rule(r)
        self.grapheme_rules()
        self.syllable()
        self.stress()
        self.templates()
        self.epithets()
        return sorted(self.out, key=lambda e: (e.line, e.code, e.message))


def check_rule_file(rf: RuleFile, table: FeatureTable) -> list[CheckError]:
    """All findings for `rf`, sorted by line then code. Never raises for a finding."""
    return _Checker(rf, table).run()


# ---- the Old Irish lexicon (Old Irish plan Task 2) -------------------------------------------


def check_lexicon_file(path: str | Path) -> list[CheckError]:
    """Read and validate `old-irish-lexicon.csv` (codes `LEX_*`, see `lexicon.validate`).
    An unreadable file is a single LEX_HEADER error at line 1 rather than an exception."""
    from .lexicon import LexiconError, read_rows, validate

    try:
        header, entries = read_rows(path)
    except LexiconError as e:
        return [CheckError(1, "LEX_HEADER", str(e), "error")]
    return validate(header, entries, path)


# ---- the Old Irish grapheme table (Old Irish plan Task 7) ------------------------------------


def check_grapheme_table(
    path: str | Path | None = None, table: FeatureTable | None = None
) -> list[CheckError]:
    """Validate `rules/old-irish-orthography.csv` (codes `GRAPH_*`): every `ipa` segment is
    a features.csv row; `env` is one of `spelled.ENVS`; `role` one of `spelled.ROLES` (seven
    values — no `punctum` role, so the ⟨ṡ⟩/⟨ḟ⟩ rows validate as cons/silent carrying a
    `punctum` column); a non-empty `punctum` is a single plain letter; EXACTLY one row has
    `role = ending` (spec §11: one temporary escape hatch, not a family); no two rows share
    `(token, env, left)`; and every token is reachable — some spelling that honours the
    token's own `env`/`left` tokenizes to it (a token only ever shadowed by a longer one is
    dead data). An unreadable table is a single GRAPH_HEADER error."""
    from .features import load_features
    from .spelled import (
        ENVS,
        OI_ORTHOGRAPHY_PATH,
        ROLES,
        SpelledError,
        load_graphemes,
        tokenize_spelling,
    )

    path = OI_ORTHOGRAPHY_PATH if path is None else Path(path)
    if table is None:
        table = load_features(OI_ORTHOGRAPHY_PATH.parent / "features.csv")
    try:
        rows = load_graphemes(path)
    except (OSError, SpelledError) as e:
        return [CheckError(1, "GRAPH_HEADER", str(e), "error")]

    out: list[CheckError] = []
    seen: dict[tuple[str, str, str], int] = {}
    endings: list[int] = []
    for r in rows:
        for seg in r.ipa:
            if seg not in table:
                out.append(
                    CheckError(
                        r.line,
                        "GRAPH_UNKNOWN_SEGMENT",
                        f"token {r.token!r}: ipa segment {seg!r} is not a features.csv row",
                        "error",
                    )
                )
        if r.env not in ENVS:
            out.append(
                CheckError(
                    r.line,
                    "GRAPH_BAD_ENV",
                    f"token {r.token!r}: env {r.env!r} is not one of " + ", ".join(ENVS),
                    "error",
                )
            )
        if r.role not in ROLES:
            out.append(
                CheckError(
                    r.line,
                    "GRAPH_BAD_ROLE",
                    f"token {r.token!r}: role {r.role!r} is not one of " + ", ".join(ROLES),
                    "error",
                )
            )
        if r.punctum and not (len(r.punctum) == 1 and r.punctum.isalpha()):
            out.append(
                CheckError(
                    r.line,
                    "GRAPH_BAD_PUNCTUM",
                    f"token {r.token!r}: punctum {r.punctum!r} must be a single plain letter",
                    "error",
                )
            )
        if r.role == "ending":
            endings.append(r.line)
        key = (r.token, r.env, r.left)
        if key in seen:
            out.append(
                CheckError(
                    r.line,
                    "GRAPH_DUPLICATE_ROW",
                    f"token {r.token!r} env {r.env!r} left {r.left or '-'!r} "
                    f"repeats line {seen[key]}",
                    "error",
                )
            )
        else:
            seen[key] = r.line
    if len(endings) != 1:
        out.append(
            CheckError(
                endings[1] if len(endings) > 1 else 0,
                "GRAPH_ENDING_COUNT",
                f"exactly one row must have role = ending (spec §11); found {len(endings)}",
                "error",
            )
        )

    # Reachability: build the smallest spellings the token's rows allow and see whether
    # tokenizing them yields the token.
    first_line: dict[str, int] = {}
    reachable: set[str] = set()
    for r in rows:
        first_line.setdefault(r.token, r.line)
        if r.token in reachable:
            continue
        pres = [""] if r.env == "initial" else ([r.left[0]] if r.left else ["t", "a"])
        posts = [""] if r.env == "final" else ["", "t", "a"]
        for pre in pres:
            for post in posts:
                try:
                    if r.token in tokenize_spelling(pre + r.token + post, rows):
                        reachable.add(r.token)
                except SpelledError:
                    continue
    for token, line in first_line.items():
        if token not in reachable:
            out.append(
                CheckError(
                    line,
                    "GRAPH_UNREACHABLE_TOKEN",
                    f"token {token!r} is never produced by tokenization "
                    "(shadowed by a longer token or its own env/left)",
                    "error",
                )
            )
    return sorted(out, key=lambda e: (e.line, e.code, e.message))
