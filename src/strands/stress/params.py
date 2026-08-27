"""Stress-parameter registry (plan Task 6, I-17). DATA ONLY: no imports from the rest of
the package, so `strands check` can validate `[stress]` parameters without importing any
procedure implementation, and Tasks 12–15 consume this table rather than editing check.py."""

PROCEDURE_PARAMS: dict[str, frozenset[str]] = {
    "initial": frozenset({"mark"}),  # mark = on|off (Georgian sets off)
    "penult": frozenset(),  # penult takes no parameters
    "cairene": frozenset(),
    "dutch-weight": frozenset({"window"}),  # window = 3 (default)
    "keep-source": frozenset(),
}
