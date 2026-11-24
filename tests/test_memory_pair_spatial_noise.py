"""Geometry and Gaussian quadrature for a field-noise reference, no trajectories."""

import math

import numpy as np
from numpy.polynomial.hermite import hermgauss
import pytest


@pytest.mark.parametrize("correlation", [0.0, 0.43, -0.61, 0.99])
def test_gaussian_covariance_change_has_both_exact_log_density_moments(correlation):
    cov = np.array([[1, correlation], [correlation, 1]])
    theta = np.array([0.261, -0.13])
    inverse = np.linalg.inv(cov)
    log_det = np.linalg.slogdet(cov)[1]
    identity = np.eye(len(theta))
    abscissa, weights = hermgauss(4)
    points = math.sqrt(2) * np.stack(np.meshgrid(abscissa, abscissa), axis=-1)
    measure = np.outer(weights, weights) / math.pi

    def ratio(z):
        displacement = z - theta
        return (
            -log_det
            - np.einsum("...i,ij,...j->...", displacement, inverse, displacement)
            + np.sum(z**2, axis=-1)
        ) / 2

    forward = ratio(points)
    cholesky = np.linalg.cholesky(cov)
    reverse = -ratio(theta + points @ cholesky.T)
    for log_ratio, entropy, variance in [
        (
            forward,
            (np.trace(inverse) - 2 + log_det + theta @ inverse @ theta) / 2,
            np.trace((inverse - identity) @ (inverse - identity)) / 2
            + np.linalg.norm(inverse @ theta) ** 2,
        ),
        (
            reverse,
            (-log_det + theta @ theta) / 2,
            np.trace((cov - identity) @ (cov - identity)) / 2 + theta @ cov @ theta,
        ),
    ]:
        average = np.sum(log_ratio * measure)
        assert average == pytest.approx(-entropy, abs=2e-14)
        assert np.sum((log_ratio - average) ** 2 * measure) == pytest.approx(
            variance, rel=2e-14
        )


@pytest.mark.parametrize("independent_share", [0, 0.17])
def test_gaussian_field_preserves_marginal_noise_and_only_pure_field_degenerates(
    independent_share,
):
    epsilon, width = 0.63, 1.17
    for radius in (0, width / 2, width, 15 * width):
        c = (1 - independent_share) * math.exp(-0.5 * (radius / width) ** 2)
        covariance = epsilon**2 * np.array([[1, c], [c, 1]])
        relative = np.array([1, -1])
        assert (relative @ covariance @ relative) == pytest.approx(
            2 * epsilon**2 * (1 - c)
        )
        np.testing.assert_array_equal(covariance.diagonal(), np.full(2, epsilon**2))
        if radius == 0 and independent_share == 0:
            np.testing.assert_array_equal(covariance @ relative, np.zeros(2))
        else:
            assert np.linalg.det(covariance) > 0
    assert c < 1e-40


def test_every_small_offset_is_the_difference_of_two_equal_radius_offsets():
    radius = 1.24
    for fraction in (0, 0.37, 1, 1.75, 2):
        offset = np.array([fraction * radius, 0, 0])
        orthogonal = np.array([0, math.sqrt(radius**2 - (offset @ offset) / 4), 0])
        first, second = orthogonal + offset / 2, orthogonal - offset / 2
        np.testing.assert_allclose(
            [np.linalg.norm(first), np.linalg.norm(second)], radius
        )
        np.testing.assert_array_equal(first - second, offset)
