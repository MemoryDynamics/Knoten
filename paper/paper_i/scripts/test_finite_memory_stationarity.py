"""Synthetic bounds and an exact countercheck, not trajectory evidence."""

import importlib.util
from pathlib import Path
import sys

import numpy as np
import pytest
from scipy.stats import multivariate_normal


@pytest.fixture(scope="module")
def kernels():
    path = Path(__file__).resolve().parents[3] / "src/emergenz_knoten/kernels.py"
    spec = importlib.util.spec_from_file_location("stationarity_kernel_control", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize("dimension", [1, 3, 7])
@pytest.mark.parametrize("bound", [0.0, 0.7])
def test_uniform_gaussian_minorization_in_log_density(dimension, bound):
    epsilon = 0.35
    direction = np.arange(1, dimension + 1, dtype=float)
    direction /= np.linalg.norm(direction)
    reference = multivariate_normal(
        mean=np.zeros(dimension), cov=epsilon**2 / 2 * np.eye(dimension)
    )
    log_c = -dimension / 2 * np.log(2) - (bound / epsilon) ** 2
    for fraction in (0.0, 0.5, 1.0):
        shift = fraction * bound * direction
        actual = multivariate_normal(mean=shift, cov=epsilon**2 * np.eye(dimension))
        for scale in (-5.0, -bound, 0.0, bound, 5.0):
            point = scale * direction
            slack = actual.logpdf(point) - log_c - reference.logpdf(point)
            expected = (
                0.5 * np.sum((point + shift) ** 2) + bound**2 - np.sum(shift**2)
            ) / epsilon**2
            assert slack >= -2e-13
            assert slack == pytest.approx(expected, rel=2e-13, abs=2e-13)


@pytest.mark.parametrize("dimension", [1, 3])
def test_full_gaussian_gradient_obeys_global_bound(kernels, dimension):
    amplitudes = (1.4, 15.0)
    widths = (1.0, 3.0)
    bound = np.exp(-0.5) * sum(a / s for a, s in zip(amplitudes, widths))
    direction = np.ones(dimension) / np.sqrt(dimension)
    for radius in np.concatenate(([0.0, 1.0, 3.0], np.geomspace(1e-4, 100, 40))):
        gradient = kernels.double_gaussian_gradient(
            radius * direction,
            np.zeros((1, dimension)),
            [1.0],
            sigma_rep=widths[0],
            sigma_att=widths[1],
            amplitude_rep=amplitudes[0],
            amplitude_att=amplitudes[1],
        )
        assert np.linalg.norm(gradient) <= bound


def test_locally_stable_collapse_coexists_with_exact_stable_two_cycle(kernels):
    a = (1 - 0.25 * np.exp(-4.5)) / (np.exp(-0.5) - np.exp(-4.5))
    b = a - 0.25
    alpha, eta = 0.5, 4.0
    gamma_one = alpha * (1 - alpha)
    mass = 1 - (1 - alpha) ** 2
    parameters = {
        "sigma_rep": 1.0,
        "sigma_att": 3.0,
        "amplitude_rep": b,
        "amplitude_att": 9 * a,
    }
    curvature = kernels.two_scale_local_curvature(**parameters)
    assert eta * mass * curvature == pytest.approx(0.75)
    assert 0 < b < 2

    # The age-zero displacement is identically zero, also when differentiating.
    def advance(value):
        return (
            -eta
            * kernels.double_gaussian_gradient(
                [value], [[0.0]], [gamma_one], **parameters
            )[0]
        )

    def derivative(value):
        return (
            -eta
            * kernels.double_gaussian_hessian(
                [value], [[0.0]], [gamma_one], **parameters
            )[0, 0]
        )

    assert advance(0.0) == 0.0
    assert derivative(0.0) == pytest.approx(-0.25)
    assert advance(3.0) == pytest.approx(-3.0, abs=2e-14)
    assert advance(-3.0) == pytest.approx(3.0, abs=2e-14)
    multiplier = -8 * b * np.exp(-4.5)
    assert derivative(3.0) == pytest.approx(multiplier, abs=2e-14)
    assert derivative(-3.0) == pytest.approx(multiplier, abs=2e-14)
    assert derivative(3.0) * derivative(-3.0) < 1
    assert abs(multiplier) < 16 * np.exp(-4.5) < 1
