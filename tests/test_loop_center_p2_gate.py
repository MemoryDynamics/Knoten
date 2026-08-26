from __future__ import annotations

import importlib.util
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = (
    ROOT
    / "experiments"
    / "current"
    / "dynamics"
    / "rotation"
    / "scalar_memory_loop_center_p2_gate.py"
)
SPEC = importlib.util.spec_from_file_location("scalar_memory_loop_center_p2_gate", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
gate = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = gate
SPEC.loader.exec_module(gate)


def _response_row() -> dict[str, object]:
    return {
        "complete_and_finite": True,
        "state_tangent_relative_rms": 1.0e-4,
        "center_velocity_tangent_relative_rms": 2.0e-4,
        "even_state_relative_rms": 3.0e-4,
        "single_sign_remainder_relative_rms": 4.0e-4,
        "normalized_odd_collapse_relative_rms": 2.0e-4,
        "signal_above_floor": True,
        "maximum_d0_fraction": 5.0e-4,
        "final_d0_ratio": 1.0e-3,
        "tail_slope_fraction_per_memory_time": 1.0e-5,
    }


def test_l3_scalar_origin_comparator_is_analytically_ineligible() -> None:
    comparator = gate._scalar_origin_comparator()

    assert comparator["decision"] == "scalar-origin-ineligible"
    assert comparator["eligible"] is False
    assert comparator["refit_allowed"] is False
    assert abs(comparator["g_h"] - (-0.0458330600738561)) < 2.0e-16
    assert abs(comparator["untruncated_scalar_pole"] - 1.0406038947734868) < 2.0e-16


def test_gate_pass_requires_controls_primary_slope_and_holdout() -> None:
    controls = {"control": {"pass": True}}
    primary = [_response_row()]
    holdout = [_response_row()]
    slopes = [{"pass": True}]

    decision, components = gate._evaluate_decision(
        controls=controls,
        primary=primary,
        slopes=slopes,
        holdout=holdout,
    )

    assert decision == "loop-center-matrix-local-pass"
    assert all(components.values())

    holdout[0]["center_velocity_tangent_relative_rms"] = 0.02
    decision, components = gate._evaluate_decision(
        controls=controls,
        primary=primary,
        slopes=slopes,
        holdout=holdout,
    )
    assert decision == "loop-center-matrix-local-fail"
    assert components["waveform_holdout"] is False


def test_control_or_signal_failure_is_inconclusive() -> None:
    row = _response_row()
    decision, _ = gate._evaluate_decision(
        controls={"control": {"pass": False}},
        primary=[row],
        slopes=[{"pass": True}],
        holdout=[row],
    )
    assert decision == "loop-center-matrix-local-inconclusive"

    row["signal_above_floor"] = False
    decision, _ = gate._evaluate_decision(
        controls={"control": {"pass": True}},
        primary=[row],
        slopes=[{"pass": True}],
        holdout=[row],
    )
    assert decision == "loop-center-matrix-local-inconclusive"
