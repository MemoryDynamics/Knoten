"""Independent force and finite-history algebra controls, no target sampling."""

import importlib.util
from pathlib import Path
import sys

import mpmath as mp
import numpy as np
import pytest

from paired_residual_precision import (
    audit_full_history_step,
    audit_split_precision,
    paired_two_length_values,
    scaled_force_remainder,
    split_step,
)


KERNELS = ((0, 26, 1, 3), (1, 35, 1, 3))


@pytest.fixture(scope="module")
def production_gradient():
    path = Path(__file__).resolve().parents[3] / "src/emergenz_knoten/kernels.py"
    spec = importlib.util.spec_from_file_location("paper_i_split_kernel_control", path)
    kernels = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = kernels
    spec.loader.exec_module(kernels)
    return kernels.double_gaussian_gradient


def _direct_mp_force_remainder(u, epsilon, kernel):
    with mp.workdps(100):
        ar, aa, sr, sa = map(mp.mpf, kernel)
        eps = mp.mpf(epsilon)
        x = [eps * mp.mpf(a) for a in u]
        r2 = mp.fsum(a * a for a in x)
        factor = aa / sa**2 * mp.exp(-r2 / (2 * sa**2)) - ar / sr**2 * mp.exp(
            -r2 / (2 * sr**2)
        )
        kappa = aa / sa**2 - ar / sr**2
        return np.array([float((factor - kappa) * a / eps**3) for a in x])


@pytest.mark.parametrize("kernel", KERNELS)
@pytest.mark.parametrize("epsilon", [1e-12, 4.4e-6, 0.007, 0.2, 2.0])
def test_scaled_force_matches_full_100_digit_expression(kernel, epsilon):
    lags = np.array([[1.0, -0.25, 0.5], [3.0, 4.0, 0.0], [0, 0, 0]])
    direct = np.array([_direct_mp_force_remainder(u, epsilon, kernel) for u in lags])
    np.testing.assert_allclose(
        scaled_force_remainder(lags, epsilon, kernel), direct, rtol=2e-14, atol=1e-14
    )


@pytest.mark.parametrize("kernel", KERNELS)
def test_zero_noise_is_exact_cubic_limit_not_an_empty_force(kernel):
    u = np.array([[0.5, 0.25], [-1.0, 0.125]])
    ar, aa, sr, sa = kernel
    cubic = ar / (2 * sr**4) - aa / (2 * sa**4)
    expected = cubic * np.sum(u * u, axis=1)[:, None] * u
    np.testing.assert_allclose(
        scaled_force_remainder(u, 0, kernel), expected, rtol=1e-15
    )


@pytest.mark.parametrize("kernel", KERNELS)
def test_reconstructed_force_matches_existing_production_kernel(
    kernel, production_gradient
):
    epsilon, alpha = 0.2, 0.3
    lags = np.array([[1.0, -0.5], [0.25, 0.125], [-0.5, 0.25]])
    gamma = alpha * (1 - alpha) ** np.arange(4)
    ar, aa, sr, sa = kernel
    x = np.zeros(2)
    memory = np.vstack((x, -epsilon * lags))
    production = production_gradient(
        x, memory, gamma, sigma_rep=sr, sigma_att=sa, amplitude_rep=ar, amplitude_att=aa
    )
    kappa = aa / sa**2 - ar / sr**2
    reconstructed = gamma[1:] @ (
        epsilon * kappa * lags
        + epsilon**3 * scaled_force_remainder(lags, epsilon, kernel)
    )
    np.testing.assert_allclose(reconstructed, production, rtol=3e-14, atol=1e-16)


def test_nonzero_histories_one_step_against_direct_physical_update_and_shift(
    production_gradient,
):
    w = np.array([[0.5, -0.25], [1.0, 0.125], [0.25, 0.5]])
    r = np.array([w / 8, -w / 4])
    xi, alpha, eta, eps = np.array([0.25, -0.5]), 0.3, 0.02, 0.15
    old_w, old_r = w.copy(), r.copy()
    nw, nr = split_step(w, r, xi, alpha, eta, eps, KERNELS)
    gamma = alpha * (1 - alpha) ** np.arange(4)
    for k, (ar, aa, sr, sa) in enumerate(KERNELS):
        physical = eps * w + eps**3 * r[k]
        force = production_gradient(
            np.zeros(2),
            np.vstack((np.zeros(2), -physical)),
            gamma,
            sigma_rep=sr,
            sigma_att=sa,
            amplitude_rep=ar,
            amplitude_att=aa,
        )
        increment = eps * xi - eta * force
        direct = np.broadcast_to(increment, physical.shape).copy()
        direct[1:] += physical[:-1]
        np.testing.assert_allclose(
            eps * nw + eps**3 * nr[k], direct, rtol=3e-14, atol=1e-16
        )
    np.testing.assert_array_equal(w, old_w)
    np.testing.assert_array_equal(r, old_r)


def test_full_memory_weights_are_not_renormalized_and_age_zero_force_vanishes():
    w = np.ones((2, 1))
    r = np.zeros((2, 2, 1))
    alpha, eta = 0.4, 0.03
    nw, _ = split_step(w, r, [0.0], alpha, eta, 0, KERNELS)
    expected = -eta * (26 / 9) * alpha * ((1 - alpha) + (1 - alpha) ** 2)
    assert nw[0, 0] == pytest.approx(expected, rel=2e-15)
    assert nw[0, 0] != pytest.approx(expected / (1 - (1 - alpha) ** 3))


def test_zero_eta_and_identical_kernel_null_controls():
    w, r = np.zeros((3, 2)), np.zeros((2, 3, 2))
    xi = np.array([0.5, -0.25])
    nw, nr = split_step(w, r, xi, 0.2, 0, 0.01, KERNELS)
    np.testing.assert_array_equal(nw, np.broadcast_to(xi, nw.shape))
    np.testing.assert_array_equal(nr, np.zeros_like(nr))
    w[:] = 0.5
    r[:] = 0.125
    _, nr = split_step(w, r, xi, 0.2, 0.02, 0.01, [KERNELS[1], KERNELS[1]])
    np.testing.assert_array_equal(nr[0], nr[1])
    blocks = np.array([[0.5, 0.25], [-0.5, 0.5]])
    residual = np.stack((blocks, blocks))
    np.testing.assert_array_equal(
        paired_two_length_values(blocks, residual, 0.01, 2), [0.0]
    )


def test_reflection_and_coordinate_permutation_covariance():
    w = np.array([[0.5, -0.25], [0.125, 0.5]])
    r = np.stack((w / 4, -w / 8))
    xi = np.array([0.5, 0.25])
    expected_w, expected_r = split_step(w, r, xi, 0.3, 0.02, 0.01, KERNELS)
    actual_w, actual_r = split_step(
        -w[:, ::-1], -r[:, :, ::-1], -xi[::-1], 0.3, 0.02, 0.01, KERNELS
    )
    np.testing.assert_allclose(actual_w, -expected_w[:, ::-1], atol=1e-16)
    np.testing.assert_allclose(actual_r, -expected_r[:, :, ::-1], atol=1e-16)


@pytest.mark.parametrize("epsilon", [0, 1e-12, 0.01, 0.2])
def test_statistic_against_independent_high_precision_square_differences(epsilon):
    w = np.array([[0.5, -0.25], [0.75, 0.125], [0.25, 0.5], [-0.5, 0.25]])
    r = np.stack((w / 8, -w / 4))
    result = paired_two_length_values(w, r, epsilon, 3)
    if epsilon == 0:
        d = r[1] - r[0]
        direct = []
        for first in (0, 2):
            wa, wb, da, db = w[first], w[first + 1], d[first], d[first + 1]
            direct.append((wa @ da + wb @ db + 2 * wa @ db + 2 * wb @ da) / 12)
    else:
        with mp.workdps(100):
            eps = mp.mpf(epsilon)
            direct = []
            for first in (0, 2):
                values = []
                for kernel in range(2):
                    a = [
                        eps * mp.mpf(w[first, c]) + eps**3 * mp.mpf(r[kernel, first, c])
                        for c in range(2)
                    ]
                    b = [
                        eps * mp.mpf(w[first + 1, c])
                        + eps**3 * mp.mpf(r[kernel, first + 1, c])
                        for c in range(2)
                    ]
                    value = (
                        mp.fsum(
                            2 * (x + y) ** 2 - x * x - y * y
                            for x, y in zip(a, b, strict=True)
                        )
                        / 24
                    )
                    values.append(value)
                direct.append(float((values[1] - values[0]) / eps**4))
    np.testing.assert_allclose(result, direct, rtol=5e-14, atol=1e-17)


@pytest.mark.parametrize("epsilon", [-1.0, np.inf, np.nan, 1e200, 1e-200])
def test_force_rejects_invalid_noise(epsilon):
    with pytest.raises(ValueError):
        scaled_force_remainder([1.0], epsilon, KERNELS[0])


@pytest.mark.parametrize("kernel", [(0, 26, 0, 3), (0, np.nan, 1, 3), (0, 26, 1)])
def test_force_rejects_invalid_kernel(kernel):
    with pytest.raises(ValueError):
        scaled_force_remainder([1.0], 0.1, kernel)


def test_curvature_mismatch_and_history_shape_rejected():
    w, r = np.zeros((3, 2)), np.zeros((2, 3, 2))
    with pytest.raises(ValueError, match="curvatures"):
        split_step(w, r, [0, 0], 0.2, 0.01, 0.1, [KERNELS[0], (1, 35.000001, 1, 3)])
    with pytest.raises(ValueError, match="states"):
        split_step(w, r[:, :-1], [0, 0], 0.2, 0.01, 0.1, KERNELS)
    with pytest.raises(ValueError, match="even number"):
        paired_two_length_values(np.zeros((3, 2)), np.zeros((2, 3, 2)), 0.1, 2)


def test_fixed_deterministic_audit_resolves_residual_where_direct_subtraction_fails():
    result = audit_split_precision()
    assert result["steps"] == 48
    assert "not Gaussian" in result["innovation_rule"]
    for cell in result["cells"]:
        assert cell["residual_increment_relative_max_error"] < 3e-13
        assert cell["paired_statistic_relative_max_error"] < 3e-13
        assert cell["reference_80_110_residual_relative_max_difference"] < 1e-40
        assert cell["reference_80_110_statistic_relative_max_difference"] < 1e-40
    assert result["cells"][0]["rounded_physical_subtraction_relative_max_error"] == 1.0
    assert result["cells"][1]["rounded_physical_subtraction_relative_max_error"] > 1e-4


def test_full_horizon_single_step_agrees_with_direct_high_precision():
    result = audit_full_history_step()
    assert "no time evolution" in result["scope"]
    for cell in result["cells"]:
        assert cell["linear_increment_relative_max_error"] < 3e-13
        assert cell["residual_increment_relative_max_error"] < 3e-12
        assert cell["reference_80_110_residual_relative_max_difference"] < 1e-40
