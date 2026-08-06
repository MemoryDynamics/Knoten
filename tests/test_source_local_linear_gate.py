from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = (
    ROOT
    / "experiments"
    / "current"
    / "memory"
    / "synchronization"
    / "source_local_linear_gate.py"
)
SPEC = importlib.util.spec_from_file_location("source_local_linear_gate", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
GATE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GATE)


def test_default_gate_rejects_channel_poles_with_negligible_knot_loading(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(sys, "argv", [str(SCRIPT)])
    args = GATE.parse_args()
    payload, _, _ = GATE.run_gate(args)
    assert payload["gate"]["classification"] == (
        "source-local channel stable; reciprocal knot-mode null"
    )
    assert not payload["gate"]["primary_pass"]
    assert payload["gate"]["primary_reduction_passes"] == 0
    exact = next(
        row
        for row in payload["rows"]
        if row["emission"] == "offset"
        and row["coupling_sign"] == 1
        and row["representation"] == "exact"
    )
    assert exact["stable"]
    assert exact["frequency_per_memory_time"] == pytest.approx(
        0.0829436746,
        rel=1.0e-6,
    )
    assert exact["normalized_knot_residue"] < 1.0e-4
    assert exact["nearest_one_way_generator_distance_ratio"] < 0.01


def test_both_coupling_signs_fail_the_registered_gate(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(sys, "argv", [str(SCRIPT)])
    payload, _, _ = GATE.run_gate(GATE.parse_args())
    exact_offset = [
        row
        for row in payload["rows"]
        if row["emission"] == "offset" and row["representation"] == "exact"
    ]
    assert {row["coupling_sign"] for row in exact_offset} == {-1, 1}
    assert not any(row["passes"] for row in exact_offset)
