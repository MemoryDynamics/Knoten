from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest

from emergenz_knoten.reciprocal_diagnostics import PanelDelayModeFit


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = (
    ROOT
    / "experiments"
    / "current"
    / "memory"
    / "synchronization"
    / "measurement_closure_relative_noise_gate.py"
)
SPEC = importlib.util.spec_from_file_location(
    "measurement_closure_relative_noise_gate",
    SCRIPT,
)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def _fit(eigenvalues: list[complex]) -> PanelDelayModeFit:
    size = len(eigenvalues)
    return PanelDelayModeFit(
        transition=np.eye(size),
        coefficients=np.eye(size),
        predictor_means=np.zeros((1, size)),
        response_means=np.zeros((1, size)),
        feature_scales=np.ones(size),
        eigenvalues=np.asarray(eigenvalues),
        design_condition=1.0,
        train_score_rmse=0.1,
        test_score_rmse=0.1,
        test_persistence_rmse=1.0,
        test_residual_ratio=0.1,
        delay_depth=1,
        score_features=1,
        train_transitions=100,
        test_transitions=50,
    )


def test_registered_defaults_freeze_closure_and_noise_ladders(monkeypatch) -> None:
    monkeypatch.setattr("sys.argv", [str(SCRIPT)])
    args = MODULE.parse_args()

    assert args.noise_correlations == "0,0.9,0.99"
    assert args.delay_depths == "1,2,5,10,20"
    assert args.mode_depths == "5,10,20"
    assert args.closure_stride_updates == 50
    assert args.train_fraction == 0.6


def test_mode_match_requires_depth_stability() -> None:
    args = SimpleNamespace(
        frequency_min_per_memory_time=0.05,
        damping_max_per_memory_time=1.0,
        mode_relative_range_max=0.25,
    )
    stable = [
        _fit([0.97 * np.exp(0.2j), 0.97 * np.exp(-0.2j)])
        for _ in range(3)
    ]
    shifted = stable[:2] + [
        _fit([0.80 * np.exp(0.8j), 0.80 * np.exp(-0.8j)])
    ]

    assert MODULE._consistent_mode(stable, args, 0.5)["pass"]
    assert not MODULE._consistent_mode(shifted, args, 0.5)["pass"]


def test_main_persists_summary_before_plot_failure(tmp_path, monkeypatch) -> None:
    args = SimpleNamespace(
        report=tmp_path / "report.md",
        summary_json=tmp_path / "summary.json",
        figure=tmp_path / "figure.png",
    )
    payload = {"gate": {"classification": "test"}, "value": 23}
    monkeypatch.setattr(MODULE, "parse_args", lambda: args)
    monkeypatch.setattr(MODULE, "run_gate", lambda _args: (payload, []))

    def fail_plot(*_args) -> None:
        raise PermissionError("plot unavailable")

    monkeypatch.setattr(MODULE, "_plot", fail_plot)
    with pytest.raises(PermissionError, match="plot unavailable"):
        MODULE.main()

    assert json.loads(args.summary_json.read_text(encoding="utf-8")) == payload
    assert not args.report.exists()
