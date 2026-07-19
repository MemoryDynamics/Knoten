from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = (
    ROOT
    / "experiments"
    / "current"
    / "memory"
    / "reconcile_low_mode_ar_runs.py"
)
SPEC = importlib.util.spec_from_file_location("reconcile_low_mode_ar_runs", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def _mode(rate: float, lambda_value: float = 0.01) -> dict[str, float]:
    import math

    eigenvalue = math.exp(-rate * lambda_value)
    return {
        "real": eigenvalue,
        "imag": 0.0,
        "modulus": eigenvalue,
        "rate_per_update": rate * lambda_value,
        "angular_frequency_per_update": 0.0,
    }


def _payload(
    *,
    steps: int,
    rate: float,
    frequency: float,
    control_pass: bool,
) -> dict:
    rows = [
        {
            "feature_group": "low_modes",
            "diffusion_length_ratio": 0.3,
            "condition": "active",
            "lag_memory_times": lag,
            "closure_lift": 0.3,
            "top_modes": [_mode(rate)],
        }
        for lag in (0.2, 1.0)
    ]
    return {
        "parameters": {"steps": steps, "lambda_value": 0.01},
        "gate": {
            "selected_ratio": 0.3,
            "active_rate_per_memory_time": rate,
            "eta_zero_rate_per_memory_time": 0.25,
            "complex_frequency_per_memory_time": frequency,
            "complex_quality_factor": 0.3,
            "eta_zero_complex_rows": 5,
            "control_separation_pass": True,
            "closure_pass": True,
            "complex_control_pass": control_pass,
            "complex_stability_pass": True,
        },
        "analyses": rows,
    }


def test_reconciliation_separates_real_stability_from_complex_failure() -> None:
    short = _payload(
        steps=100_000,
        rate=0.73,
        frequency=0.48,
        control_pass=False,
    )
    long = _payload(
        steps=1_000_000,
        rate=0.77,
        frequency=0.21,
        control_pass=False,
    )

    result = MODULE.reconcile(short, long)

    assert result["real_mode_n_stability_pass"] is True
    assert result["common_active_lag_count"] == 2
    assert result["common_active_lag_max_abs_rate_change"] < 0.1
    assert result["complex_mode_n_stability_pass"] is False
    assert result["common_lag_comparisons"][0]["interpretable"] is True
