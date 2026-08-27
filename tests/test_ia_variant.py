"""/ɪə/ as a transcription variant of the /iə/ diphthong (digest §1.2, `irish.rules`
[normalize] `ɪ -> i / _ ə`). Irish has no /ɪə/ distinct from /iə/, so the user's own
*Ciara* /ˈkɪə.ɾˠə/ must adapt exactly as /ˈkiəɾˠə/ does — before the rule the targets saw
no diphthong nucleus and syllabified it as hiatus."""
import pytest

from helpers import TABLE, irish
from strands.inputs import Entry, infer
from strands.irish import normalize
from strands.pipeline import TARGETS, load_target, run_entry
from strands.tokenize import tokenize
from strands.word import Word

IRISH = irish()
RF = {name: load_target(name, TABLE) for name in TARGETS}


def _run(ipa: str, strand: str):
    entry = infer(Entry(orthography=ipa, ipa=ipa), IRISH, TABLE)
    return run_entry(entry, "DESC", IRISH, RF[strand], TABLE)


def test_normalize_folds_the_variant_onto_the_diphthong():
    assert normalize(Word.from_tokenized(tokenize("kɪəɾˠə", TABLE)),
                     IRISH, TABLE).segments[:3] == ("k", "i", "ə")


def test_the_rule_only_applies_before_schwa():
    """`ɪ -> i / _ ə` must not touch a plain /ɪ/ elsewhere (*cuid* /kɪdʲ/)."""
    assert normalize(Word.from_tokenized(tokenize("kɪdʲ", TABLE)),
                     IRISH, TABLE).segments == ("k", "ɪ", "dʲ")


@pytest.mark.parametrize("strand", TARGETS)
def test_ciara_adapts_the_same_either_way(strand):
    variant = _run("ˈkɪə.ɾˠə", strand)
    canonical = _run("ˈkiəɾˠə", strand)
    assert variant.ipa == canonical.ipa
    assert variant.respelling == canonical.respelling
