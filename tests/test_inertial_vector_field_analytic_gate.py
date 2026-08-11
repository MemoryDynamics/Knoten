from __future__ import annotations

from experiments.current.memory.closure.inertial_vector_field_analytic_gate import (
    _jsonable,
    run_audit,
)


def test_analytic_gate_passes_all_registered_identities() -> None:
    result = run_audit()
    assert result["decision"] == "structural-pass"
    assert all(result["gates"].values())
    assert result["negative_control"]["classification"] == "restoring_instability"


def test_json_conversion_replaces_nonstandard_infinity() -> None:
    assert _jsonable(float("inf")) == "Infinity"
    assert _jsonable(float("-inf")) == "-Infinity"
