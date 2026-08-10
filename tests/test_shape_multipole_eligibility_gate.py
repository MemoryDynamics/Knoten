from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path

import numpy as np
import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = (
    ROOT
    / "experiments" / "current" / "memory" / "synchronization" / "reciprocity" / "shape_multipole_eligibility_gate.py"
)
SPEC = importlib.util.spec_from_file_location("shape_multipole_gate", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
GATE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GATE)


def _analysis_args() -> argparse.Namespace:
    return argparse.Namespace(
        frequency_min=0.05,
        frequency_max=2.0,
        peak_ratio_min=5.0,
        peak_fraction_min=0.10,
        segment_fraction_min=0.05,
        frequency_relative_range_max=0.25,
        min_segment_passes=3,
        segments=4,
        shuffle_block_memory_times=1.0,
        shuffle_count=32,
    )


def test_normalized_traceless_shape_is_scale_free_and_traceless() -> None:
    tensors = np.asarray(
        [np.diag([1.0, 2.0, 3.0]), np.diag([5.0, 10.0, 15.0])]
    )
    values = GATE.normalized_traceless_shape_components(tensors).reshape(2, 3, 3)

    assert np.allclose(values[0], values[1])
    assert np.allclose(np.trace(values, axis1=1, axis2=2), 0.0, atol=1e-15)


def test_registered_spectral_analysis_accepts_persistent_tensor_line() -> None:
    dt = 0.1
    times = np.arange(0.0, 1400.0, dt)
    rng = np.random.default_rng(7)
    signal = np.column_stack(
        (
            np.sin(2.0 * np.pi * 0.2 * times),
            np.cos(2.0 * np.pi * 0.2 * times),
            0.05 * rng.standard_normal(times.size),
        )
    )
    result = GATE.analyze_source(
        signal,
        sample_interval=dt,
        args=_analysis_args(),
        null_seed=99,
    )

    assert result["candidate_pass"]
    assert result["full"]["peak_frequency_cycles_per_memory_time"] == pytest.approx(
        0.2, abs=0.01
    )


def test_registered_defaults_freeze_p32d_design(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("sys.argv", [str(SCRIPT)])
    args = GATE.parse_args()

    assert args.future_seeds == "1,2,3,4,5"
    assert args.updates == 150_000
    assert args.sample_every == 10
    assert args.shuffle_count == 64
    assert args.min_baseline_seeds == 4
    assert args.max_control_seeds == 1

def test_report_metric_formats_nonfinite_json_value() -> None:
    assert GATE._format_metric(None) == "inf"
    assert GATE._format_metric(0.125, ".3g") == "0.125"

def test_compact_summary_removes_only_reproducible_plot_arrays() -> None:
    spectral = {
        "full": {"peak_to_background": 7.0, "frequencies": [0.1], "power_spectrum": [2.0]},
        "segments": [
            {"segment": 1, "frequencies": [0.1], "power_spectrum": [1.0]}
        ],
    }
    payload = {
        "rows": [
            {
                "conditions": {
                    condition: {"sources": {source: spectral for source in GATE.SOURCES}}
                    for condition in GATE.CONDITIONS
                }
            }
        ],
        "plot_traces": [{"times": [0.0]}],
    }

    compact = GATE.compact_summary(payload)

    assert "plot_traces" not in compact
    assert compact["spectral_arrays"].startswith("not persisted")
    kept = compact["rows"][0]["conditions"]["baseline"]["sources"]["shape"]
    assert kept["full"] == {"peak_to_background": 7.0}
    assert kept["segments"] == [{"segment": 1}]
    assert "plot_traces" in payload
