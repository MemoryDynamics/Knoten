"""Deterministic controls for the fixed-width escape proof, without trajectories."""

import math

import numpy as np
import pytest
from scipy.special import gammainc

from emergenz_knoten.kernels import double_gaussian_gradient


def _log_gaussian(residual, deviation):
    return -0.5 * np.sum((residual / deviation) ** 2) - np.sum(
        np.log(np.broadcast_to(deviation, residual.shape) * math.sqrt(math.tau))
    )


@pytest.mark.parametrize("dimension", [3, 5])
def test_gaussian_minorizing_bound_is_attained_at_the_opposite_mean(dimension):
    mean = np.linspace(-0.28, 0.51, dimension)
    sigma = 0.73
    bound = -dimension * math.log(2) / 2 - (mean @ mean) / sigma**2
    for shift in [0, -0.31, 0.45]:
        at = -mean + shift
        ratio = _log_gaussian(at - mean, sigma) - _log_gaussian(
            at, sigma / math.sqrt(2)
        )
        assert ratio == pytest.approx(
            bound + dimension * shift**2 / (2 * sigma**2), abs=5e-15
        )


@pytest.mark.parametrize("dimension", [3, 5])
def test_formal_regeneration_mixture_has_the_gaussian_small_ball_bound(dimension):
    cycles, success, radius, variance = 31, 0.4, 0.78, 1.12
    # The non-Gaussian component here is a point mass; no path is drawn.
    probabilities = [
        math.comb(cycles, k) * success**k * (1 - success) ** (cycles - k)
        for k in range(cycles + 1)
    ]
    exact = probabilities[0] + sum(
        probabilities[k] * gammainc(dimension / 2, radius**2 / (2 * variance * k))
        for k in range(1, cycles + 1)
    )
    threshold = cycles * success / 2
    rare_count = sum(probabilities[: math.ceil(threshold)])
    volume = math.pi ** (dimension / 2) * radius**dimension
    volume /= math.gamma(dimension / 2 + 1)
    bound = rare_count + volume / (math.tau * variance * threshold) ** (dimension / 2)
    assert 0 < rare_count < bound < 1
    assert exact <= bound


def test_finite_gaussian_path_ratio_uses_the_drifts_of_the_same_prefix():
    deviations = np.array([0.63, 0.63, 0.81, 0.81])
    rows = np.array([[0.4, -0.3, -0.5, 0.16], [-0.6, 0.2, 0.15, 0.49]])
    previous = np.array([0.1, -0.38, 0.23, -0.45])
    quotient, exponent = 0.0, 0.0
    for step in rows:
        free_mean = -0.24 * np.tanh(previous)
        extra = 0.47 * np.tanh(previous[::-1])
        residual = step - free_mean
        quotient += _log_gaussian(residual - extra, deviations)
        quotient -= _log_gaussian(residual, deviations)
        theta = extra / deviations
        exponent += theta @ (residual / deviations) - (theta @ theta) / 2
        previous = step
    assert quotient == pytest.approx(exponent, abs=2e-15)


@pytest.mark.parametrize("separation", [50.0, 100.0])
def test_nearby_aged_source_breaks_a_uniform_bound_in_head_separation(separation):
    receiver = np.zeros(3)
    locations = np.array([[separation, 0, 0], [-0.5, 0, 0]])
    gradient = double_gaussian_gradient(
        receiver,
        locations,
        np.array([0.7, 0.3]),
        amplitude_rep=0,
        amplitude_att=1,
        sigma_rep=1,
        sigma_att=1,
    )
    assert gradient[0] == pytest.approx(0.15 * math.exp(-0.125))
    assert np.linalg.norm(gradient) > 0.1
