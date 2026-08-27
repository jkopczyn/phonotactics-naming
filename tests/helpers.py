"""Shared test helpers (plan Task 5a). Imported as `from helpers import ...`."""
import csv
import pathlib

from strands.dsl import parse_rules_file
from strands.features import load_features
from strands.tokenize import tokenize
from strands.word import Word

ROOT = pathlib.Path(__file__).parents[1]
FIXTURES = pathlib.Path(__file__).parent / "fixtures"
TABLE = load_features(ROOT / "rules" / "features.tsv")


def w(ipa: str) -> Word:
    return Word.from_tokenized(tokenize(ipa, TABLE))


def irish():
    return parse_rules_file(ROOT / "rules" / "irish.rules", TABLE)


def target(name: str):
    return parse_rules_file(ROOT / "rules" / f"{name}.rules", TABLE)


def rules_exist(name: str) -> bool:
    return (ROOT / "rules" / f"{name}.rules").exists()


def read_test_words() -> list[dict[str, str]]:
    with (ROOT / "sources" / "irish" / "test-words.tsv").open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def mutation_rows() -> list[dict[str, str]]:
    """R22: the 47 rows tagged mut: in the `features` column — NOT the 85 len: rows,
    which are a vowel-length tag."""
    return [r for r in read_test_words() if "mut:" in (r.get("features") or "")]


def entry_of(row: dict[str, str]):
    """A test-words row -> an inferred Entry. Available from Task 20 on."""
    from strands.inputs import Entry, infer
    return infer(Entry(orthography=row["orthography"], ipa=row["ipa"],
                       dialect=row.get("dialect") or "C", gloss=row.get("gloss") or ""),
                 irish(), TABLE)


FIX = FIXTURES / "input-sample.tsv"      # written in Task 20


def read_allow_file_for(name: str) -> set[str]:
    return {ortho for tgt, ortho in read_allow_file() if tgt == name}


def read_allow_file() -> set[tuple[str, str]]:
    path = ROOT / "tests" / "allow-unrepaired.txt"
    if not path.exists():
        return set()
    out = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip() and not line.startswith("#"):
            tgt, ortho, *_ = line.split("\t")
            out.add((tgt, ortho))
    return out
