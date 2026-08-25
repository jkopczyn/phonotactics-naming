"""Command-line entry point. Subcommands land in Tasks 6 (check) and 27 (the rest)."""

from __future__ import annotations

import sys

from . import __version__

COMMANDS = ("run", "explain", "gallery", "lint", "check")


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if argv and argv[0] == "--version":
        print(f"strands {__version__}")
        return 0
    if not argv or argv[0] not in COMMANDS:
        print(f"usage: strands {{{'|'.join(COMMANDS)}}} ...", file=sys.stderr)
        return 2
    print(f"{argv[0]}: not implemented yet", file=sys.stderr)
    return 1
