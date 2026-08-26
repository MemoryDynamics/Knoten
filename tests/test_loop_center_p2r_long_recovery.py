from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = (
    ROOT
    / "experiments"
    / "current"
    / "dynamics"
    / "rotation"
    / "scalar_memory_loop_center_p2r_long_recovery.py"
)
SPEC = importlib.util.spec_from_file_location(
    "scalar_memory_loop_center_p2r_long_recovery",
    SCRIPT,
)
assert SPEC is not None and SPEC.loader is not None
gate = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = gate
SPEC.loader.exec_module(gate)


def test_exponential_tail_has_negative_slope_and_registered_log_rate() -> None:
    steps = np.arange(1, gate.TOTAL_UPDATES + 1, dtype=float)
    distances = np.exp(-0.6 * gate.CANDIDATE.alpha * steps)
    metrics = gate.window_metrics(
        distances,
        checkpoint_peak=float(distances[0]),
        start=3201,
        end=3600,
    )

    assert metrics["signed_slope_fraction_per_memory_time"] < 0.0
    assert abs(metrics["log_decay_rate_per_memory_time"] - 0.6) < 2.0e-15
    assert metrics["maximum_sampled_ten_update_increase"] < 0.0
    assert metrics["pass"] is True


def test_complete_p2_payload_replays_itself_exactly() -> None:
    old = json.loads((ROOT / gate.P2_RESULT).read_text(encoding="utf-8"))
    replay = gate._compare_full_replay(old, old)

    assert replay["metric_count"] > 100
    assert replay["maximum_error_to_tolerance_ratio"] == 0.0
    assert replay["mismatches"] == []
    assert replay["pass"] is True


def _synthetic_row(*, signal: bool = True, passed: bool = True) -> dict[str, object]:
    return {
        "complete_and_finite": True,
        "checkpoint_replay": {"pass": True},
        "plus": {"gates": {"signal_floor": signal}},
        "minus": {"gates": {"signal_floor": signal}},
        "pass": passed,
    }


def test_p2r_decision_keeps_replay_failures_inconclusive() -> None:
    decision, components = gate._evaluate_decision(
        full_replay={"pass": True},
        rows=[_synthetic_row()],
        probe_off_pass=True,
    )
    assert decision == "p2r-sign-sensitive-long-recovery-pass"
    assert all(components.values())

    decision, components = gate._evaluate_decision(
        full_replay={"pass": True},
        rows=[_synthetic_row(passed=False)],
        probe_off_pass=True,
    )
    assert decision == "p2r-sign-sensitive-long-recovery-fail"
    assert components["recovery"] is False

    decision, _ = gate._evaluate_decision(
        full_replay={"pass": False},
        rows=[_synthetic_row()],
        probe_off_pass=True,
    )
    assert decision == "p2r-sign-sensitive-long-recovery-inconclusive"

    decision, _ = gate._evaluate_decision(
        full_replay={"pass": True},
        rows=[_synthetic_row(signal=False)],
        probe_off_pass=True,
    )
    assert decision == "p2r-sign-sensitive-long-recovery-inconclusive"
