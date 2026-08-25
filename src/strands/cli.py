"""Command-line entry point. `check` lands in Task 6; the rest in Task 27."""

from __future__ import annotations

import sys
from pathlib import Path

from . import __version__

COMMANDS = ("run", "explain", "gallery", "lint", "check")
DEFAULT_FEATURES = Path(__file__).resolve().parents[2] / "rules" / "features.tsv"


def _check(argv: list[str]) -> int:
    """`strands check [--features PATH] RULES...`: parse + static checks (Task 6).
    Findings go to stderr as `path:line: CODE: message`. Exit 1 on a parse error or any
    error-severity finding; warnings alone exit 0."""
    from .check import check_rule_file
    from .dsl import ParseError, parse_rules_file
    from .features import FeatureError, load_features

    features = DEFAULT_FEATURES
    paths: list[str] = []
    it = iter(argv)
    for arg in it:
        if arg == "--features":
            try:
                features = Path(next(it))
            except StopIteration:
                print("check: --features needs a path", file=sys.stderr)
                return 2
        else:
            paths.append(arg)
    if not paths:
        print("usage: strands check [--features PATH] RULES.rules ...", file=sys.stderr)
        return 2
    try:
        table = load_features(features)
    except (OSError, FeatureError) as e:
        print(f"check: cannot load {features}: {e}", file=sys.stderr)
        return 1
    failed = False
    for path in paths:
        try:
            rf = parse_rules_file(path, table)
        except ParseError as e:
            print(f"{e}: PARSE_ERROR", file=sys.stderr)
            failed = True
            continue
        for err in check_rule_file(rf, table):
            print(f"{path}:{err.line}: {err.code}: {err.message} [{err.severity}]",
                  file=sys.stderr)
            if err.severity == "error":
                failed = True
    return 1 if failed else 0


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if argv and argv[0] == "--version":
        print(f"strands {__version__}")
        return 0
    if not argv or argv[0] not in COMMANDS:
        print(f"usage: strands {{{'|'.join(COMMANDS)}}} ...", file=sys.stderr)
        return 2
    if argv[0] == "check":
        return _check(argv[1:])
    print(f"{argv[0]}: not implemented yet", file=sys.stderr)
    return 1
