"""Feature table loader: aliases, predeclared (derived) classes, weighted distance.

Plan Task 2; spec §2 (feature table) and §12.C (aliases, exact-lookup feature changes);
interpretations I-1 (NFC on read), I-4 (exact vector lookup), I-11 (predeclared classes),
I-12 (distance), I-20 (extra columns), I-32 (feature aliases).
"""
from __future__ import annotations

import unicodedata
from collections.abc import Sequence
from pathlib import Path

__all__ = [
    "FEATURE_NAMES", "FEATURE_ALIASES", "DERIVED_CLASSES", "SEGMENT_ALIASES",
    "FeatureTable", "FeatureError", "load_features",
]

# The 38 PHOIBLE features, in features.tsv column order.
FEATURE_NAMES: tuple[str, ...] = (
    "tone", "stress", "syllabic", "short", "long", "consonantal", "sonorant", "continuant",
    "delayedRelease", "approximant", "tap", "trill", "nasal", "lateral", "labial", "round",
    "labiodental", "coronal", "anterior", "distributed", "strident", "dorsal", "high", "low",
    "front", "back", "tense", "retractedTongueRoot", "advancedTongueRoot",
    "periodicGlottalSource", "epilaryngealSource", "spreadGlottis", "constrictedGlottis",
    "fortis", "lenis", "raisedLarynxEjective", "loweredLarynxImplosive", "click",
)

# I-32 / spec §12.C. A `# alias = column` line in the features.tsv header block may add more.
FEATURE_ALIASES: dict[str, str] = {
    "ejective": "raisedLarynxEjective",
    "voice": "periodicGlottalSource",
    "emphatic": "retractedTongueRoot",
    "aspirated": "spreadGlottis",
}

# I-11: predeclared classes, computed from features at load time.
DERIVED_CLASSES: tuple[str, ...] = ("C", "V", "LIQ", "NAS", "STOP", "FRIC", "GLIDE")

# Input-alias rows whose vector copies a principal's exactly (I-30 fortis/lenis spellings,
# I-34 ASCII `g`). Exact-lookup feature changes resolve to the principal, never the alias.
SEGMENT_ALIASES: dict[str, str] = {
    "g": "ɡ", "lˠ": "l̪ˠ", "l̠ʲ": "lʲ", "nˠ": "n̪ˠ", "n̠ʲ": "nʲ",
}

# Non-feature columns that precede the feature block (I-20).
_EXTRA_COLUMNS: tuple[str, ...] = ("segment", "class", "source")
_VALUES = frozenset("+-0")


class FeatureError(Exception):
    """Unknown segment/feature, unreachable feature change, or malformed table."""


class FeatureTable:
    def __init__(self, rows: list[tuple[str, str, tuple[str, ...]]],
                 aliases: dict[str, str]) -> None:
        self._vectors: dict[str, tuple[str, ...]] = {}
        self._classes: dict[str, str] = {}
        for segment, klass, vector in rows:
            if segment in self._vectors:
                raise FeatureError(f"duplicate segment row: {segment!r}")
            self._vectors[segment] = vector
            self._classes[segment] = klass
        self.segments: tuple[str, ...] = tuple(s for s, _, _ in rows)
        self._aliases = dict(aliases)
        self._index = {f: i for i, f in enumerate(FEATURE_NAMES)}
        # Reverse map for exact-lookup feature changes. Alias rows (SEGMENT_ALIASES) copy
        # their principal's vector exactly, so among identical vectors the first NON-alias
        # row in file order wins; an alias is chosen only when nothing else has the vector.
        self._by_vector: dict[tuple[str, ...], str] = {}
        for s in self.segments:
            if s not in SEGMENT_ALIASES:
                self._by_vector.setdefault(self._vectors[s], s)
        for s in self.segments:
            self._by_vector.setdefault(self._vectors[s], s)

    # -- basic access -------------------------------------------------------------------------

    def __contains__(self, segment: object) -> bool:
        return segment in self._vectors

    def __len__(self) -> int:
        return len(self.segments)

    def canonical_feature(self, name: str) -> str:
        """Resolve an alias (or a column name) to the features.tsv column name."""
        if name in self._index:
            return name
        if name in self._aliases:
            return self._aliases[name]
        raise FeatureError(f"unknown feature: {name!r}")

    def _seg(self, segment: str) -> tuple[str, ...]:
        try:
            return self._vectors[segment]
        except KeyError:
            raise FeatureError(f"unknown segment: {segment!r}") from None

    def vector(self, segment: str) -> tuple[str, ...]:
        return self._seg(segment)

    def value(self, segment: str, feature: str) -> str:
        return self._seg(segment)[self._index[self.canonical_feature(feature)]]

    def segment_class(self, segment: str) -> str:
        self._seg(segment)
        return self._classes[segment]

    # -- bundles --------------------------------------------------------------------------------

    def _resolve(self, spec: dict[str, str]) -> dict[int, str]:
        out: dict[int, str] = {}
        for feature, val in spec.items():
            if val not in _VALUES:
                raise FeatureError(f"bad feature value {val!r} for {feature!r}")
            out[self._index[self.canonical_feature(feature)]] = val
        return out

    def matches(self, segment: str, constraints: dict[str, str]) -> bool:
        vec = self._seg(segment)
        return all(vec[i] == v for i, v in self._resolve(constraints).items())

    def apply_changes(self, segment: str, changes: dict[str, str]) -> str:
        """EXACT vector lookup (I-4). Raises FeatureError if no segment has it."""
        vec = list(self._seg(segment))
        for i, v in self._resolve(changes).items():
            vec[i] = v
        target = tuple(vec)
        if target == self._vectors[segment]:
            return segment
        try:
            return self._by_vector[target]
        except KeyError:
            raise FeatureError(
                f"no segment has the vector produced by {changes!r} applied to {segment!r}"
            ) from None

    # -- distance -------------------------------------------------------------------------------

    def _weights(self, weights: dict[str, float] | None) -> tuple[float, ...]:
        w = [1.0] * len(FEATURE_NAMES)
        for feature, val in (weights or {}).items():
            w[self._index[self.canonical_feature(feature)]] = float(val)
        return tuple(w)

    def distance(self, a: str, b: str, weights: dict[str, float] | None = None) -> float:
        """I-12: sum of weights over features where both are defined (+/-) and differ."""
        va, vb = self._seg(a), self._seg(b)
        w = self._weights(weights)
        return sum(w[i] for i, (x, y) in enumerate(zip(va, vb))
                   if x != y and x != "0" and y != "0")

    def nearest(self, segment: str, candidates: Sequence[str],
                weights: dict[str, float] | None = None) -> str:
        """Candidate with minimal distance; ties break by candidate order (first wins)."""
        best: str | None = None
        best_d = 0.0
        for c in candidates:
            d = self.distance(segment, c, weights)
            if best is None or d < best_d:
                best, best_d = c, d
        if best is None:
            raise FeatureError(f"nearest({segment!r}): no candidates")
        return best

    # -- predeclared classes (I-11) ---------------------------------------------------------------

    def _is_member(self, name: str, segment: str) -> bool:
        v = self.value
        if name == "C":
            return v(segment, "syllabic") == "-"
        if name == "V":
            return v(segment, "syllabic") == "+"
        if name == "LIQ":
            return (v(segment, "consonantal") == "+" and v(segment, "sonorant") == "+"
                    and v(segment, "coronal") == "+"
                    and "+" in (v(segment, "lateral"), v(segment, "tap"), v(segment, "trill")))
        if name == "NAS":
            return v(segment, "nasal") == "+"
        if name == "STOP":
            return (v(segment, "consonantal") == "+" and v(segment, "continuant") == "-"
                    and v(segment, "sonorant") == "-" and v(segment, "delayedRelease") == "-")
        if name == "FRIC":
            return (v(segment, "continuant") == "+" and v(segment, "sonorant") == "-"
                    and v(segment, "consonantal") == "+")
        if name == "GLIDE":
            return (v(segment, "syllabic") == "-" and v(segment, "sonorant") == "+"
                    and v(segment, "consonantal") == "-")
        raise FeatureError(f"not a predeclared class: {name!r}")

    def derived_class(self, name: str, over: Sequence[str]) -> tuple[str, ...]:
        """Members of a predeclared class (I-11) drawn from `over`, in `over` order."""
        if name not in DERIVED_CLASSES:
            raise FeatureError(f"not a predeclared class: {name!r}")
        return tuple(s for s in over if self._is_member(name, s))


def load_features(path: str | Path) -> FeatureTable:
    """Read features.tsv (UTF-8, NFC per I-1). `# alias = column` header lines add aliases."""
    path = Path(path)
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as e:
        raise FeatureError(f"cannot read feature table {path}: {e}") from e
    text = unicodedata.normalize("NFC", text)

    aliases = dict(FEATURE_ALIASES)
    header: list[str] | None = None
    rows: list[tuple[str, str, tuple[str, ...]]] = []
    for lineno, raw in enumerate(text.splitlines(), 1):
        line = raw.rstrip("\r\n")
        if not line.strip():
            continue
        if line.startswith("#"):
            body = line[1:].strip()
            if "=" in body and header is None:
                alias, _, target = (p.strip() for p in body.partition("="))
                if target not in FEATURE_NAMES:
                    raise FeatureError(f"{path}:{lineno}: alias {alias!r} -> unknown feature {target!r}")
                aliases[alias] = target
            continue
        fields = line.split("\t")
        if header is None:
            header = fields
            expected = list(_EXTRA_COLUMNS) + list(FEATURE_NAMES)
            if header != expected:
                raise FeatureError(f"{path}:{lineno}: unexpected header columns: {header}")
            continue
        if len(fields) != len(header):
            raise FeatureError(f"{path}:{lineno}: expected {len(header)} columns, got {len(fields)}")
        segment, klass = fields[0], fields[1]
        vector = tuple(fields[len(_EXTRA_COLUMNS):])
        if klass not in ("C", "V"):
            raise FeatureError(f"{path}:{lineno}: class must be C or V, got {klass!r}")
        bad = [v for v in vector if v not in _VALUES]
        if bad:
            raise FeatureError(f"{path}:{lineno}: bad feature values {bad!r}")
        rows.append((segment, klass, vector))
    if header is None:
        raise FeatureError(f"{path}: no header row")
    for alias in aliases:
        if alias in FEATURE_NAMES:
            raise FeatureError(f"alias {alias!r} shadows a feature column")
    return FeatureTable(rows, aliases)
