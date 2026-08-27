"""Command-line entry point (spec §6; plan Tasks 6 and 27).

    strands run   INPUT.tsv [--strand X|all] [--construction NAME|all] [--out out.tsv]
    strands explain WORD --strand X [--construction NAME] [--orthography TEXT]
    strands gallery INPUT.tsv [--out gallery.md]
    strands lint  INPUT.tsv [--accept]
    strands check [--features PATH] RULES.rules|LEXICON.tsv ...

Exit codes: 0 ok; 1 a runtime failure (unreadable input, parse error in a rule file, an
input IPA containing a segment not in `features.tsv` — reported with the word and the
offending substring, spec §2 — an unwritable `--out`, `check` findings); 2 a usage error
(unknown subcommand, strand or construction, missing argument). Runtime failures are
diagnostics on stderr, never tracebacks.

`run` writes one TSV row per (entry, construction, strand) — columns `orthography,
construction, strand, respelling, ipa, flags, fallbacks, assumptions` — in input /
`CONSTRUCTIONS` / `TARGETS` order, so the file is byte-identical across runs. An entry
without IPA, or a multi-slot template (ADJ, OF, COMPOUND) that a single entry cannot fill,
is SKIPPED: the row is still written, with empty output columns and a `skipped:...` note in
`assumptions`. `--construction all` covers the Irish templates AND the `DESC+ADJ` /
`DESC+NOUN` epithet tags (I-39). `explain` prints the derivation trace of one IPA word
(default construction `DESC`): stage, rule id, tag, before -> after, and the rule's own
`#` citation comment where the id names a rule line. `gallery` is `gallery.render_gallery`.
`lint` prints `inputs.lint_report`; `--accept` writes the guesses back — including an `ipa`
constructed from the spelling by `strands.g2p` (spec §5, milestone 8), which also gets a
`note` saying so.

Old Irish (plan Task 17; O-17, O-23): a construction the strand has no template for
(`PATRO_NI` for old-irish, `MAEL` for welsh) is a `skipped:construction-not-in-strand` row.
The Old Irish lookup keys on the **orthography**, which a bare IPA `WORD` cannot supply, so
`explain --orthography TEXT` makes TEXT the lookup key and the aligner's input; without it,
`explain --strand old-irish` runs the pure retro path and says so in a one-line note, since a
silent `RETRO` looks like a lexicon miss.
"""

from __future__ import annotations

import csv
import io
import sys
from pathlib import Path
from typing import Sequence

from . import __version__

COMMANDS = ("run", "explain", "gallery", "lint", "check")
DEFAULT_FEATURES = Path(__file__).resolve().parents[2] / "rules" / "features.tsv"
RUN_COLUMNS = ("orthography", "construction", "strand", "respelling", "ipa",
               "flags", "fallbacks", "assumptions")
_DEFAULT_CONSTRUCTION = "DESC"


class UsageError(Exception):
    """Bad arguments: reported on stderr, exit 2."""


# ---- argument parsing -------------------------------------------------------------------------

def _parse(argv: Sequence[str], flags: dict[str, bool], positional: int) -> tuple[list[str], dict[str, str | bool]]:
    """Tiny option parser: `flags` maps `--name` to whether it takes a value. Returns
    (positionals, options). Raises UsageError."""
    pos: list[str] = []
    opts: dict[str, str | bool] = {}
    it = iter(argv)
    for arg in it:
        if arg.startswith("--"):
            if arg not in flags:
                raise UsageError(f"unknown option {arg}")
            if flags[arg]:
                try:
                    opts[arg] = next(it)
                except StopIteration:
                    raise UsageError(f"{arg} needs a value") from None
            else:
                opts[arg] = True
        else:
            pos.append(arg)
    if len(pos) != positional:
        raise UsageError(f"expected {positional} argument(s), got {len(pos)}")
    return pos, opts


def _strands(value: str | None) -> list[str]:
    from .pipeline import TARGETS
    if value is None or value == "all":
        return list(TARGETS)
    if value not in TARGETS:
        raise UsageError(f"unknown strand {value!r} (one of {', '.join(TARGETS)}, all)")
    return [value]


def _constructions(value: str | None, default: str) -> list[str]:
    from .pipeline import CONSTRUCTIONS
    if value is None:
        value = default
    if value == "all":
        return list(CONSTRUCTIONS)
    if value not in CONSTRUCTIONS:
        raise UsageError(f"unknown construction {value!r} "
                         f"(one of {', '.join(CONSTRUCTIONS)}, all)")
    return [value]


# ---- shared loading ---------------------------------------------------------------------------

def _load(strands: Sequence[str]):
    """(table, irish, [(name, target)...]) — parse errors surface as RuntimeError."""
    from .dsl import ParseError, parse_rules_file
    from .features import FeatureError, load_features
    from .pipeline import load_target
    try:
        table = load_features(DEFAULT_FEATURES)
        irish = parse_rules_file(DEFAULT_FEATURES.parent / "irish.rules", table)
        targets = [(name, load_target(name, table)) for name in strands]
    except (OSError, FeatureError, ParseError) as e:
        raise RuntimeError(str(e)) from e
    return table, irish, targets


def _entries(path: str, irish, table):
    from .inputs import InputError, infer, read_input
    from .tokenize import SegmentError
    try:
        raw = read_input(path)
    except (OSError, InputError) as e:
        raise RuntimeError(f"cannot read {path}: {e}") from e
    entries = []
    for e in raw:
        try:
            entries.append(infer(e, irish, table))
        except SegmentError as exc:
            raise RuntimeError(f"{path}: {e.orthography}: {exc}") from exc
    return raw, entries


def _write(text: str, out: str | None) -> None:
    """stdout, or `out`; an unwritable path is a runtime failure."""
    if out is None:
        sys.stdout.write(text)
        return
    try:
        Path(out).write_text(text, encoding="utf-8")
    except OSError as e:
        raise RuntimeError(f"cannot write {out}: {e}") from e


# ---- run ------------------------------------------------------------------------------------

def run_rows(entries, constructions: Sequence[str], irish, targets, table) -> list[dict[str, str]]:
    """One row per entry × construction × strand, in that order. Skips (no IPA, missing
    slot) keep their row with a `skipped:` note (module docstring)."""
    from .irish import MissingSlot
    from .pipeline import ConstructionNotInStrand, run_entry
    from .tokenize import SegmentError
    rows: list[dict[str, str]] = []
    for entry in entries:
        for construction in constructions:
            for name, rf in targets:
                row = {"orthography": entry.orthography, "construction": construction,
                       "strand": name, "respelling": "", "ipa": "", "flags": "",
                       "fallbacks": "", "assumptions": ""}
                notes = list(entry.assumptions)
                if not entry.ipa:
                    if "skipped:no-ipa" not in notes:
                        notes.append("skipped:no-ipa")
                else:
                    try:
                        result = run_entry(entry, construction, irish, rf, table)
                    except MissingSlot as e:
                        slot = str(e).split("slot ", 1)[-1].split(" ", 1)[0].strip("'\"")
                        notes.append(f"skipped:missing-slot-{slot}")
                    except ConstructionNotInStrand:                 # Old Irish O-17
                        notes.append("skipped:construction-not-in-strand")
                    except SegmentError as e:
                        raise RuntimeError(f"{entry.orthography} [{construction}, {name}]: {e}") from e
                    else:
                        row.update(respelling=result.respelling, ipa=result.ipa,
                                   flags=" ".join(result.flags),
                                   fallbacks=str(result.fallbacks))
                        notes = list(result.assumptions)
                row["assumptions"] = " ".join(notes)
                rows.append(row)
    return rows


def _write_tsv(rows: Sequence[dict[str, str]], out: str | None) -> None:
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=RUN_COLUMNS, delimiter="\t",
                            lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    _write(buf.getvalue(), out)


def cmd_run(args: Sequence[str]) -> int:
    (path,), opts = _parse(args, {"--strand": True, "--construction": True, "--out": True}, 1)
    strands = _strands(opts.get("--strand"))
    constructions = _constructions(opts.get("--construction"), "all")
    table, irish, targets = _load(strands)
    _, entries = _entries(path, irish, table)
    _write_tsv(run_rows(entries, constructions, irish, targets, table), opts.get("--out"))
    return 0


# ---- explain --------------------------------------------------------------------------------

def _citations(*rule_files) -> dict[str, str]:
    """rule_id -> the rule line's `#` comment, over every rule-bearing section."""
    out: dict[str, str] = {}
    for rf in rule_files:
        groups = list(rf.sections.values()) + list(rf.mutations.values()) + list(rf.inflect.values())
        for rules in groups:
            for rule in rules:
                if rule.comment.strip():
                    out.setdefault(rule.rule_id, rule.comment.strip())
    return out


def format_trace(result, citations: dict[str, str]) -> list[str]:
    """`stage  rule_id  %tag  before -> after  # citation` per trace entry."""
    lines: list[str] = []
    for t in result.trace:
        tag = f"%{t.tag}" if t.tag else "-"
        line = f"{t.stage:<11} {t.rule_id:<22} {tag:<10} {t.before} -> {t.after}"
        cite = citations.get(t.rule_id)
        if cite:
            line += f"   # {cite}"
        if t.note:
            line += f"   ({t.note})"
        lines.append(line)
    return lines


def cmd_explain(args: Sequence[str]) -> int:
    (word,), opts = _parse(args, {"--strand": True, "--construction": True,
                                  "--orthography": True}, 1)
    if "--strand" not in opts:
        raise UsageError("explain needs --strand")
    strand = _strands(str(opts["--strand"]))
    if len(strand) != 1:
        raise UsageError("explain takes exactly one strand")
    constructions = _constructions(opts.get("--construction"), _DEFAULT_CONSTRUCTION)
    if len(constructions) != 1:
        raise UsageError("explain takes exactly one construction, not `all`")
    (construction,) = constructions
    table, irish, targets = _load(strand)
    name, rf = targets[0]
    from .inputs import Entry, infer
    from .irish import MissingSlot
    from .pipeline import run_entry
    from .tokenize import SegmentError
    orthography = opts.get("--orthography")
    is_old_irish = rf.meta.get("strand", "").strip() == "old-irish"
    try:
        entry = infer(Entry(orthography=str(orthography or word), ipa=word), irish, table)
        if is_old_irish and orthography is None:
            # O-23: with no citation spelling the lookup is disabled outright (an empty
            # lexicon), so the printed "pure RETRO path" note is true even when the IPA
            # argument happens to spell a lexicon key (*mac*).
            from .oldirish import run_entry_oi
            result = run_entry_oi(entry, construction, irish, rf, table, lexicon={})
        else:
            result = run_entry(entry, construction, irish, rf, table)
    except MissingSlot as e:
        raise UsageError(f"{e}; explain takes one word and cannot fill a second slot") from e
    except SegmentError as e:
        raise RuntimeError(f"{word}: {e}") from e
    print(f"{word}  [{name}, {construction}]")
    if orthography is not None:
        print(f"orthography: {orthography}")
    elif is_old_irish:
        print("note: no --orthography given, so the lexicon lookup (which keys on the "
              "citation spelling, O-23) is disabled; this is the pure RETRO path")
    print(f"respelling: {result.respelling}")
    print(f"ipa:        {result.ipa}")
    if result.flags:
        print(f"flags:      {' '.join(result.flags)}")
    print(f"fallbacks:  {result.fallbacks}")
    if result.assumptions:
        print(f"assumptions: {' '.join(result.assumptions)}")
    print()
    for line in format_trace(result, _citations(irish, rf)):
        print(line)
    return 0


# ---- gallery --------------------------------------------------------------------------------

def cmd_gallery(args: Sequence[str]) -> int:
    from .gallery import render_gallery
    from .pipeline import CONSTRUCTIONS
    (path,), opts = _parse(args, {"--out": True}, 1)
    table, irish, targets = _load(_strands(None))
    _, entries = _entries(path, irish, table)
    text = render_gallery(entries, targets, CONSTRUCTIONS, table, irish=irish)
    _write(text, opts.get("--out"))
    return 0


# ---- lint -----------------------------------------------------------------------------------

def cmd_lint(args: Sequence[str]) -> int:
    from .inputs import accept_guesses, lint_report
    (path,), opts = _parse(args, {"--accept": False}, 1)
    table, irish, _ = _load(())
    _, entries = _entries(path, irish, table)
    for line in lint_report(entries):
        print(line)
    if opts.get("--accept"):
        try:
            accept_guesses(path, entries)
        except OSError as e:
            raise RuntimeError(f"cannot write {path}: {e}") from e
        print(f"lint: wrote inferred fields to {path}", file=sys.stderr)
    return 0


# ---- check (Task 6) -------------------------------------------------------------------------

def _check(argv: list[str]) -> int:
    """`strands check [--features PATH] RULES... | LEXICON.tsv`: parse + static checks (Task 6);
    a `.tsv` argument is validated as the Old Irish lexicon instead.
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
        print("usage: strands check [--features PATH] RULES.rules|LEXICON.tsv ...", file=sys.stderr)
        return 2
    try:
        table = load_features(features)
    except (OSError, FeatureError) as e:
        print(f"check: cannot load {features}: {e}", file=sys.stderr)
        return 1
    failed = False
    for path in paths:
        if path.endswith(".tsv"):
            # Old Irish plan Task 2: a lexicon TSV routes to the LEX_* checks; warnings
            # (the Task 3 backlog) are listed but do not fail the run.
            from .check import check_lexicon_file
            for err in check_lexicon_file(path):
                print(f"{path}:{err.line}: {err.code}: {err.message} [{err.severity}]",
                      file=sys.stderr)
                if err.severity == "error":
                    failed = True
            continue
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


# ---- dispatch -------------------------------------------------------------------------------

_USAGE = {
    "run": "strands run INPUT.tsv [--strand X|all] [--construction NAME|all] [--out out.tsv]",
    "explain": "strands explain WORD --strand X [--construction NAME] [--orthography TEXT]",
    "gallery": "strands gallery INPUT.tsv [--out gallery.md]",
    "lint": "strands lint INPUT.tsv [--accept]",
}
_HANDLERS = {"run": cmd_run, "explain": cmd_explain, "gallery": cmd_gallery, "lint": cmd_lint}


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if argv and argv[0] == "--version":
        print(f"strands {__version__}")
        return 0
    if not argv or argv[0] not in COMMANDS:
        print(f"usage: strands {{{'|'.join(COMMANDS)}}} ...", file=sys.stderr)
        return 2
    command, rest = argv[0], argv[1:]
    if command == "check":
        return _check(rest)
    from .pipeline import PipelineError
    from .tokenize import SegmentError
    try:
        return _HANDLERS[command](rest)
    except UsageError as e:
        print(f"{command}: {e}\nusage: {_USAGE[command]}", file=sys.stderr)
        return 2
    except (RuntimeError, SegmentError, PipelineError, OSError) as e:
        # RuntimeError is the annotated form; the bare types are the boundary's last line
        # of defence (a SegmentError raised inside the gallery, a stray OSError).
        print(f"{command}: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
