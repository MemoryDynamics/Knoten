from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from emergenz_knoten import (  # noqa: E402
    two_scale_integral_coefficient,
    two_scale_local_curvature,
    zero_mean_attractive_amplitude,
    zero_mean_compensator_amplitude,
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
