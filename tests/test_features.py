"""Task 2: feature table loader — aliases, derived classes, weighted distance."""
import pathlib, pytest
from strands.features import load_features, FeatureError, FEATURE_NAMES

TABLE = load_features(pathlib.Path(__file__).parents[1] / "rules" / "features.tsv")

def test_table_has_38_features_and_114_segments():
    assert len(FEATURE_NAMES) == 38 and len(TABLE.segments) == 114

def test_segments_are_in_file_order_c_before_v():
    classes = [TABLE.segment_class(s) for s in TABLE.segments]
    assert classes == sorted(classes, key=["C", "V"].index)

def test_value_accepts_an_alias():
    assert TABLE.value("tʼ", "ejective") == TABLE.value("tʼ", "raisedLarynxEjective") == "+"
    assert TABLE.canonical_feature("voice") == "periodicGlottalSource"

def test_distance_is_zero_on_identity_and_symmetric():
    assert TABLE.distance("k", "k") == 0
    assert TABLE.distance("k", "c") == TABLE.distance("c", "k") > 0

def test_distance_ignores_undefined_features():
    manual = sum(1 for f in FEATURE_NAMES
                 if TABLE.value("h", f) in "+-" and TABLE.value("k", f) in "+-"
                 and TABLE.value("h", f) != TABLE.value("k", f))
    assert TABLE.distance("h", "k") == manual

def test_distance_honours_weights():
    assert TABLE.distance("k", "c", weights={"front": 10.0}) > TABLE.distance("k", "c")

def test_distance_weights_accept_aliases():
    # k/kʼ differ on raisedLarynxEjective and constrictedGlottis (2 features, verified).
    assert TABLE.distance("k", "kʼ") == 2.0
    assert TABLE.distance("k", "kʼ", weights={"ejective": 5.0}) == 6.0

def test_nearest_breaks_ties_by_candidate_order():
    """S2: no tautologies — compute the real answer and hard-code it."""
    assert TABLE.nearest("pˠ", ["b", "f"]) == "b"
    assert TABLE.nearest("pˠ", ["f", "b"]) == "b"      # b is strictly nearer, order-independent
    # a genuine tie (both at distance 3, verified against the built table), resolved by order.
    # The plan's original pair m/ŋ is NOT a tie (2 vs 3) and was replaced per the plan's own
    # "verify rather than assume" instruction.
    assert TABLE.distance("n̪ˠ", "ŋ") == TABLE.distance("n̪ˠ", "nʲ") == 3.0
    assert TABLE.nearest("n̪ˠ", ["ŋ", "nʲ"]) == "ŋ"
    assert TABLE.nearest("n̪ˠ", ["nʲ", "ŋ"]) == "nʲ"
    assert TABLE.nearest("n̪ˠ", ["m", "ŋ"]) == "m"       # m is strictly nearer (2 < 3)
    assert TABLE.nearest("n̪ˠ", ["ŋ", "m"]) == "m"

def test_nearest_with_no_candidates_raises():
    with pytest.raises(FeatureError):
        TABLE.nearest("k", [])

def test_apply_changes_is_exact_lookup():
    # Every ejective row in features.tsv carries raisedLarynxEjective=+ AND constrictedGlottis=+,
    # so under exact lookup (I-4) `{ejective: +}` alone reaches no row (see next test).
    both = {"raisedLarynxEjective": "+", "constrictedGlottis": "+"}
    assert TABLE.apply_changes("k", both) == "kʼ"
    assert TABLE.apply_changes("k", {"ejective": "+", "constrictedGlottis": "+"}) == "kʼ"  # alias
    assert TABLE.apply_changes("k", {}) == "k"
    assert TABLE.apply_changes("kʼ", {"ejective": "-", "constrictedGlottis": "-"}) == "k"

def test_apply_changes_ejective_alone_is_unreachable_in_current_table():
    """Documents a data fact later tasks must know: [+ejective] alone is UNREACHABLE_CHANGE."""
    with pytest.raises(FeatureError):
        TABLE.apply_changes("k", {"ejective": "+"})

def test_apply_changes_raises_when_no_segment_has_the_vector():
    with pytest.raises(FeatureError):
        TABLE.apply_changes("h", {"lateral": "+", "trill": "+"})

def test_matches_uses_constraints_and_aliases():
    assert TABLE.matches("kʼ", {"ejective": "+"})
    assert not TABLE.matches("k", {"ejective": "+"})
    assert TABLE.matches("k", {"dorsal": "+", "voice": "-"})
    assert not TABLE.matches("k", {"dorsal": "+", "voice": "+"})
    assert TABLE.matches("k", {})

def test_derived_classes():
    inv = list(TABLE.segments)
    assert "h" in TABLE.derived_class("C", inv)          # I-11: C = syllabic-
    assert "j" in TABLE.derived_class("GLIDE", inv)
    assert set("l ɾ r".split()) <= set(TABLE.derived_class("LIQ", inv))
    assert "m" in TABLE.derived_class("NAS", inv) and "m" not in TABLE.derived_class("LIQ", inv)
    assert "k" in TABLE.derived_class("STOP", inv) and "s" in TABLE.derived_class("FRIC", inv)
    assert "a" in TABLE.derived_class("V", inv)

def test_derived_class_keeps_over_order_and_restricts_to_over():
    assert TABLE.derived_class("C", ["s", "a", "k"]) == ("s", "k")
    assert TABLE.derived_class("C", ["k", "a", "s"]) == ("k", "s")
    with pytest.raises(FeatureError):
        TABLE.derived_class("WIBBLE", ["k"])

def test_unknown_segment_and_unknown_feature_raise():
    with pytest.raises(FeatureError): TABLE.value("QQ", "front")
    with pytest.raises(FeatureError): TABLE.value("k", "wibble")

def test_contains_and_vector():
    assert "k" in TABLE and "QQ" not in TABLE
    vec = TABLE.vector("k")
    assert len(vec) == 38 and vec[FEATURE_NAMES.index("dorsal")] == "+"

def test_load_missing_file_raises():
    with pytest.raises(FeatureError):
        load_features(pathlib.Path(__file__).parent / "no-such-features.tsv")


def test_apply_changes_prefers_the_canonical_row_over_an_input_alias():
    """I-34 / I-30: alias rows (`g`, `lˠ`, `l̠ʲ`, `nˠ`, `n̠ʲ`) copy their principal's vector;
    an exact-lookup change must resolve to the principal spelling whatever the TSV order."""
    def toward(src, dst):
        return {f: y for f, x, y in zip(FEATURE_NAMES, TABLE.vector(src), TABLE.vector(dst))
                if x != y}
    assert TABLE.apply_changes("k", {"voice": "+"}) == "ɡ"
    assert TABLE.apply_changes("ɟ", {"front": "-"}) == "ɡ"
    for src, dst in [("n̪ˠ", "l̪ˠ"), ("nʲ", "lʲ"), ("l̪ˠ", "n̪ˠ"), ("lʲ", "nʲ")]:
        assert TABLE.apply_changes(src, toward(src, dst)) == dst
    assert TABLE.apply_changes("g", {}) == "g"          # identity keeps the alias spelling
