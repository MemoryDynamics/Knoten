from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments" / "current" / "kernels"))
sys.path.insert(0, str(ROOT / "src"))

import fixed_curvature_sigma_pilot as sigma_pilot  # noqa: E402
import kernel_compensation_audit as audit  # noqa: E402


def test_reference_record_quantifies_q3_constraint_gap() -> None:
    record = audit.reference_record(dim=3, q=3.0, amplitude_att=35.0)

    assert record["chi"] == pytest.approx(35.0 / 9.0)
    assert record["restoring_curvature"] == pytest.approx(35.0 / 9.0 - 1.0)
    assert record["integrated_attraction_to_repulsion"] == pytest.approx(945.0)
    assert record["zero_mean_amplitude_att"] == pytest.approx(1.0 / 27.0)
    assert record["zero_mean_chi"] == pytest.approx(1.0 / 243.0)


def test_compensation_record_has_zero_integral_and_convergent_curvature() -> None:
    narrow = audit.compensation_record(
        dim=3,
        q=3.0,
        amplitude_att=35.0,
        sigma_comp=10.0,
    )
    broad = audit.compensation_record(
        dim=3,
        q=3.0,
        amplitude_att=35.0,
        sigma_comp=30.0,
    )

    assert narrow["integral_residual"] == pytest.approx(0.0, abs=1e-10)
    assert broad["integral_residual"] == pytest.approx(0.0, abs=2e-10)
    assert broad["curvature_retention"] > narrow["curvature_retention"]
    assert broad["curvature_retention"] > 0.999


def test_radial_profile_compensator_changes_far_field() -> None:
    radius = np.array([0.0, 3.0, 20.0])
    amplitude_comp = float(
        audit.compensation_record(
            dim=3,
            q=3.0,
            amplitude_att=35.0,
            sigma_comp=10.0,
        )["amplitude_comp"]
    )
    _, baseline_drift = audit.radial_profile(radius, q=3.0, amplitude_att=35.0)
    _, compensated_drift = audit.radial_profile(
        radius,
        q=3.0,
        amplitude_att=35.0,
        sigma_comp=10.0,
        amplitude_comp=amplitude_comp,
    )

    assert compensated_drift[0] == 0.0
    assert compensated_drift[-1] > baseline_drift[-1]


def test_fixed_curvature_aggregate_keeps_seed_robust_summary() -> None:
    rows = [
        {"q": 2.0, "amplitude_att": 16.0, "local_curvature": 3.0, "knot_score": 0.6},
        {"q": 2.0, "amplitude_att": 16.0, "local_curvature": 3.0, "knot_score": 0.8},
    ]

    aggregate = sigma_pilot._aggregate(rows, [2.0])

    assert aggregate[0]["n_seeds"] == 2
    assert aggregate[0]["knot_score_median"] == pytest.approx(0.7)
    assert aggregate[0]["amplitude_att"] == pytest.approx(16.0)
