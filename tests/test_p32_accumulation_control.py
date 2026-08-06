from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

import numpy as np
import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = (
    ROOT
    / "experiments"
    / "current"
    / "memory"
    / "synchronization"
    / "p32_accumulation_control.py"
)
SPEC = importlib.util.spec_from_file_location("p32_accumulation_control", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
CONTROL = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CONTROL)


def test_registered_base_args_freeze_the_two_seed_500k_control(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(sys, "argv", [str(SCRIPT)])
    args = CONTROL._base_args(CONTROL.parse_args())

    assert args.future_seeds == "1,2"
    assert args.updates == 500_000
    assert args.sample_every == 10
    assert args.min_complex_seeds == 2
    assert args.max_control_complex_seeds == 0
    assert args.cross_gain == 0.02


def test_window_metrics_measure_control_subtracted_accumulation() -> None:
    times = np.arange(100.0, 501.0, 10.0)
    off = np.ones(times.size)
    distances = off + 0.2 + 0.001 * (times - 100.0)
    row = CONTROL._window_row(
        times,
        distances,
        off,
        100.0,
        500.0,
        include_upper=True,
    )

    assert row["median_pair_distance_r"] == pytest.approx(1.4)
    assert row["median_absolute_delta_from_off_r"] == pytest.approx(0.4)
    assert row["slope_r_per_1000_memory_times"] == pytest.approx(1.0)


def test_fixed_epochs_preserve_seed_and_condition_labels() -> None:
    sample_steps = np.arange(10_000, 500_001, 1000)
    times = sample_steps * 0.01
    off = np.ones(times.size)
    pair_distances = np.column_stack(
        (off, off + 0.1, off + 0.02, off + 0.05 + 0.00002 * times)
    )
    rows = CONTROL._accumulation_rows(
        [
            {
                "future_seed": 7,
                "sample_steps": sample_steps,
                "pair_distances_r": pair_distances,
            }
        ],
        alpha=0.01,
    )

    assert rows[0]["future_seed"] == 7
    assert set(rows[0]["conditions"]) == set(CONTROL.CONDITIONS)
    assert len(rows[0]["conditions"]["retarded_reciprocal"]["epochs"]) == 4
    assert rows[0]["conditions"]["retarded_reciprocal"][
        "late_minus_early_absolute_delta_from_off_r"
    ] > 0.0
