from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
from types import SimpleNamespace
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = (
    ROOT
    / "experiments"
    / "current"
    / "memory"
    / "closure"
    / "emergent_modal_state_reconciliation.py"
)
SPEC = importlib.util.spec_from_file_location(
    "emergent_modal_state_reconciliation",
    SCRIPT,
)
reconciliation = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = reconciliation
SPEC.loader.exec_module(reconciliation)


def _args() -> argparse.Namespace:
    return argparse.Namespace(
        train_fraction=0.6,
        common_start_index=8,
        kr_values="0.5,1,2,4,8",
        perturbation_fractions="0.005,0.01",
        extinction_updates=800,
        sample_every=5,
    )


def test_signal_gate_requires_energy_inside_chronological_holdout() -> None:
    steps = np.arange(0, 605, 5)
    time = np.arange(steps.size, dtype=float)
    persistent = np.power(0.99, time)[:, None, None]
    early_only = persistent.copy()
    early_only[40:] = 0.0

    persistent_result = reconciliation._balanced_signal_diagnostics(
        persistent,
        steps,
        _args(),
    )
    early_result = reconciliation._balanced_signal_diagnostics(
        early_only,
        steps,
        _args(),
    )

    assert persistent_result["pass"]
    assert persistent_result["holdout_energy_fraction"] >= 0.05
    assert not early_result["pass"]
    assert early_result["support_updates"] < early_result["holdout_start_update"]


def test_rank_two_gate_checks_energy_and_third_singular_value() -> None:
    rank_two = reconciliation._rank_two_diagnostics(
        SimpleNamespace(singular_values=np.array([10.0, 3.0, 0.2, 0.1]))
    )
    higher_rank = reconciliation._rank_two_diagnostics(
        SimpleNamespace(singular_values=np.array([10.0, 5.0, 4.0, 3.0]))
    )

    assert rank_two["rank_two_pass"]
    assert not higher_rank["rank_two_pass"]


def test_archive_retains_diagonal_features_and_full_cross_modes(tmp_path: Path) -> None:
    features = np.arange(30, dtype=float).reshape(2, 1, 5, 3)
    modes = np.arange(50, dtype=float).reshape(2, 1, 5, 5).astype(complex)
    records = {
        ("case", "active", 0.005, 0): {
            "features": features[:, 0],
            "modes": modes[:, 0],
        }
    }
    case_rows = [{"profile_grams": np.eye(5)[None, :, :]}]
    path = tmp_path / "responses.npz"

    metadata = reconciliation.write_archive(records, case_rows, path, _args())
    names = metadata["record_keys"]["case|active|0.005|0"]

    with np.load(path, allow_pickle=False) as archive:
        np.testing.assert_array_equal(archive[names["features"]], features[:, 0])
        np.testing.assert_array_equal(archive[names["modes"]], modes[:, 0])
