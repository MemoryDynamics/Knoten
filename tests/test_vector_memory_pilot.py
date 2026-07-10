from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from experiments.vector_memory_pilot import build_report, run_pilot  # noqa: E402


def test_vector_memory_pilot_runs_small_case() -> None:
    args = argparse.Namespace(
        steps=120,
        burn_in=0,
        sample_every=10,
        dim=2,
        seeds=[1, 2],
        amplitude_att=[0.35, 8.0, 20.0],
        eta_vector=[0.0, 0.01],
        force_mode="transverse_2d",
        epsilon=0.03,
        eta=0.15,
        alpha=0.05,
        memory_mass=1.0,
        lambda_vector=None,
        vector_mass=1.0,
        sigma_vector=1.0,
        sigma_rep=1.0,
        sigma_att=3.0,
        amplitude_rep=1.0,
        memory_factor=6.0,
        max_memory=40,
        lags=[1, 2],
        pca_components=4,
        ridge=1e-6,
        imag_tol=1e-3,
        unstable_tol=1.05,
        slow_abs_min=0.2,
        output_json="ignored.json",
        report="ignored.md",
    )

    payload = run_pilot(args)

    assert len(payload["scenarios"]) == 6
    assert payload["scenarios"][0]["feature_dim_raw"] == 16
    assert {s["amplitude_att"] for s in payload["scenarios"]} == {0.35, 8.0, 20.0}
    assert {s["eta_vector"] for s in payload["scenarios"]} == {0.0, 0.01}
    assert "Initial Vector-Memory Pilot" in build_report(payload)
