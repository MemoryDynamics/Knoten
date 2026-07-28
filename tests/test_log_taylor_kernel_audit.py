from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments" / "current" / "kernels"))

import log_taylor_kernel_audit as audit  # noqa: E402


def _args() -> argparse.Namespace:
    return argparse.Namespace(
        dimension=3,
        sigma_rep=1.0,
        sigma_att=3.0,
        amplitude_rep=1.0,
        amplitude_att=35.0,
        memory_radius=1.94163e-4,
        max_radius_over_l=5.0,
    )


def test_current_amplitudes_map_exactly_to_effective_26() -> None:
    metrics = audit.build_metrics(_args())

    assert metrics.local_curvature == pytest.approx(26.0 / 9.0)
    assert metrics.effective_amplitude == pytest.approx(26.0)
    assert metrics.matched_attractive_amplitude == pytest.approx(26.0)


def test_log_matches_curvature_and_has_zero_total_integral() -> None:
    metrics = audit.build_metrics(_args())
    u = np.array([0.0, 1.0e-8, 1.0e-5])
    profile = audit.kernel_profiles(u, metrics)["log"]
    totals = audit.analytic_radial_integrals(metrics)

    assert profile["restoring_ratio"][0] == pytest.approx(1.0)
    assert profile["restoring_ratio"][1] == pytest.approx(1.0, abs=1.0e-12)
    assert totals["log"] == 0.0


def test_plotted_log_profile_integrates_to_zero_numerically() -> None:
    metrics = audit.build_metrics(_args())
    u = np.linspace(0.0, 10.0, 50_001)
    potential = audit.kernel_profiles(u, metrics)["log"]["potential"]
    normalized = potential / (metrics.local_curvature * metrics.sigma_att**2)

    radial_integral = np.trapezoid(u ** (metrics.dimension - 1) * normalized, u)

    assert radial_integral == pytest.approx(0.0, abs=1.0e-12)


def test_27_and_36_are_a_separate_unproved_identification() -> None:
    metrics = audit.build_metrics(_args())

    assert metrics.volume_ratio == pytest.approx(27.0)
    assert metrics.raw_amplitude_if_effective_equals_volume_ratio == pytest.approx(
        36.0
    )
    assert metrics.two_scale_zero_mean_attractive_amplitude == pytest.approx(
        1.0 / 27.0
    )
    assert metrics.log_polynomial_amplitude == pytest.approx(26.0 / 5.0)


def test_families_have_distinct_first_nonlinear_force_terms() -> None:
    coefficients = audit.dimensionless_force_cubic_coefficients(
        audit.build_metrics(_args())
    )

    assert coefficients["two_scale"] == pytest.approx(-23.0 / 26.0)
    assert coefficients["attractive_only"] == pytest.approx(0.5)
    assert coefficients["log"] == pytest.approx(0.7)
