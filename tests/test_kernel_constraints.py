from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from emergenz_knoten import (  # noqa: E402
    three_scale_gaussian_gradient,
    three_scale_gaussian_potential,
    two_scale_integral_coefficient,
    two_scale_local_curvature,
    zero_mean_attractive_amplitude,
    zero_mean_compensator_amplitude,
    zero_mean_curvature_matched_amplitudes,
)


def test_zero_mean_two_scale_kernel_is_not_locally_restoring_for_broad_attraction() -> (
    None
):
    dim = 3
    sigma_rep = 1.0
    sigma_att = 3.0
    amplitude_att = zero_mean_attractive_amplitude(
        dim=dim,
        sigma_rep=sigma_rep,
        sigma_att=sigma_att,
    )

    integral = two_scale_integral_coefficient(
        dim=dim,
        sigma_rep=sigma_rep,
        sigma_att=sigma_att,
        amplitude_att=amplitude_att,
    )
    curvature = two_scale_local_curvature(
        sigma_rep=sigma_rep,
        sigma_att=sigma_att,
        amplitude_att=amplitude_att,
    )

    assert integral == pytest.approx(0.0, abs=1e-14)
    assert curvature < 0.0
    assert amplitude_att / sigma_att**2 == pytest.approx(
        (sigma_rep / sigma_att) ** (dim + 2)
    )


def test_broad_third_scale_compensator_preserves_integral_and_local_curvature() -> None:
    dim = 3
    sigma_rep = 1.0
    sigma_att = 3.0
    sigma_comp = 30.0
    amplitude_rep = 1.0
    amplitude_att = 35.0
    amplitude_comp = zero_mean_compensator_amplitude(
        dim=dim,
        sigma_rep=sigma_rep,
        sigma_att=sigma_att,
        sigma_comp=sigma_comp,
        amplitude_rep=amplitude_rep,
        amplitude_att=amplitude_att,
    )

    residual = (
        two_scale_integral_coefficient(
            dim=dim,
            sigma_rep=sigma_rep,
            sigma_att=sigma_att,
            amplitude_rep=amplitude_rep,
            amplitude_att=amplitude_att,
        )
        + amplitude_comp * sigma_comp**dim
    )
    original_curvature = two_scale_local_curvature(
        sigma_rep=sigma_rep,
        sigma_att=sigma_att,
        amplitude_rep=amplitude_rep,
        amplitude_att=amplitude_att,
    )
    compensated_curvature = original_curvature - amplitude_comp / sigma_comp**2

    assert residual == pytest.approx(0.0, abs=1e-10)
    assert amplitude_comp > 0.0
    assert compensated_curvature / original_curvature > 0.999


def test_fixed_curvature_path_scales_attractive_amplitude_quadratically() -> None:
    chi = 35.0 / 9.0
    q_values = np.array([2.0, 3.0, 4.0])
    amplitudes = chi * q_values**2

    for q, amplitude in zip(q_values, amplitudes, strict=True):
        curvature = two_scale_local_curvature(
            sigma_rep=1.0,
            sigma_att=float(q),
            amplitude_rep=1.0,
            amplitude_att=float(amplitude),
        )
        assert curvature == pytest.approx(chi - 1.0)


def test_kernel_constraint_helpers_validate_geometry() -> None:
    with pytest.raises(ValueError, match="dim"):
        two_scale_integral_coefficient(dim=0, sigma_rep=1.0, sigma_att=3.0)
    with pytest.raises(ValueError, match="sigma_comp"):
        zero_mean_compensator_amplitude(
            dim=3,
            sigma_rep=1.0,
            sigma_att=3.0,
            sigma_comp=0.0,
        )


def test_curvature_matched_compensator_satisfies_both_constraints() -> None:
    target = two_scale_local_curvature(
        sigma_rep=1.0,
        sigma_att=3.0,
        amplitude_rep=1.0,
        amplitude_att=35.0,
    )
    amplitude_att, amplitude_comp = zero_mean_curvature_matched_amplitudes(
        dim=3,
        sigma_rep=1.0,
        sigma_att=3.0,
        sigma_comp=10.0,
        target_curvature=target,
        amplitude_rep=1.0,
    )

    residual = (
        two_scale_integral_coefficient(
            dim=3,
            sigma_rep=1.0,
            sigma_att=3.0,
            amplitude_rep=1.0,
            amplitude_att=amplitude_att,
        )
        + amplitude_comp * 10.0**3
    )
    curvature = (
        two_scale_local_curvature(
            sigma_rep=1.0,
            sigma_att=3.0,
            amplitude_rep=1.0,
            amplitude_att=amplitude_att,
        )
        - amplitude_comp / 10.0**2
    )

    assert amplitude_att == pytest.approx(35.08516695570236)
    assert amplitude_comp == pytest.approx(0.9462995078039638)
    assert residual == pytest.approx(0.0, abs=2e-10)
    assert curvature == pytest.approx(target)


def test_three_scale_potential_gradient_matches_finite_difference() -> None:
    x = np.array([0.7, -0.2])
    memory = np.array([[0.0, 0.0], [0.4, -0.5]])
    weights = np.array([0.6, 0.3])
    step = 1e-6
    finite_difference = np.empty_like(x)
    kwargs = {
        "sigma_rep": 1.0,
        "sigma_att": 3.0,
        "sigma_comp": 10.0,
        "amplitude_rep": 1.0,
        "amplitude_att": 35.0,
        "amplitude_comp": 0.944,
    }
    for coordinate in range(x.size):
        offset = np.zeros_like(x)
        offset[coordinate] = step
        finite_difference[coordinate] = (
            three_scale_gaussian_potential(x + offset, memory, weights, **kwargs)
            - three_scale_gaussian_potential(x - offset, memory, weights, **kwargs)
        ) / (2.0 * step)

    gradient = three_scale_gaussian_gradient(x, memory, weights, **kwargs)

    np.testing.assert_allclose(finite_difference, gradient, rtol=5e-8, atol=4e-9)
