from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = (
    ROOT
    / "experiments"
    / "current"
    / "memory"
    / "synchronization"
    / "retarded_reciprocal_full_knot_gate.py"
)
SPEC = importlib.util.spec_from_file_location(
    "retarded_reciprocal_full_knot_gate",
    SCRIPT,
)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def _trace(matrix: np.ndarray, *, samples: int = 600) -> tuple[np.ndarray, np.ndarray]:
    state = np.empty((samples, 3, 2), dtype=float)
    state[0] = np.array([[1.0, 0.2], [-0.4, 0.7], [0.3, -0.8]])
    for index in range(1, samples):
        state[index] = state[index - 1] @ matrix.T
    return state[:, :, 0], state[:, :, 1]


def _thresholds() -> dict[str, float]:
    return {
        "min_complex_segments": 3,
        "frequency_min_per_memory_time": 0.05,
        "mode_relative_range_max": 0.25,
        "phase_coherence_min": 0.5,
        "fit_residual_ratio_max": 0.8,
        "fit_condition_max": 1e8,
    }


def test_mode_gate_accepts_a_stable_repeated_complex_mode() -> None:
    matrix = np.array([[0.995, -0.02], [0.02, 0.995]])
    positions, centers = _trace(matrix, samples=1200)

    rows, summary = MODULE._segment_modes(
        positions,
        centers,
        start_index=0,
        segments=4,
        alpha=0.01,
        sample_every=1,
        thresholds=_thresholds(),
    )

    assert len(rows) == 4
    assert summary["meaningful_complex_segments"] == 4
    assert summary["segment_identity_pass"]


def test_main_persists_summary_before_plot_failure(tmp_path, monkeypatch) -> None:
    report = tmp_path / "report.md"
    summary = tmp_path / "summary.json"
    figure = tmp_path / "figure.png"
    args = SimpleNamespace(
        report=report,
        summary_json=summary,
        figure=figure,
    )
    payload = {
        "gate": {"classification": "test"},
        "value": 17,
    }

    monkeypatch.setattr(MODULE, "parse_args", lambda: args)
    monkeypatch.setattr(MODULE, "run_gate", lambda _args: (payload, []))

    def fail_plot(*_args) -> None:
        raise PermissionError("plot destination is unavailable")

    monkeypatch.setattr(MODULE, "_plot", fail_plot)

    with pytest.raises(PermissionError, match="plot destination"):
        MODULE.main()

    assert json.loads(summary.read_text(encoding="utf-8")) == payload
    assert not report.exists()


def test_registered_mediator_defaults_match_inherited_architecture(monkeypatch) -> None:
    monkeypatch.setattr("sys.argv", [str(SCRIPT)])
    defaults = MODULE.parse_args()

    assert defaults.correlation_length_r == 5.0
    assert defaults.relaxation_memory_times == 10.0
    assert defaults.grid_spacing_r == 0.25
    assert defaults.cross_gain == 0.02
