"""Extra-coordinate algebra and off-orbit checks; no positive target evaluation."""

from dataclasses import replace
from fractions import Fraction as F
from itertools import combinations

import numpy as np
import pytest

from emergenz_knoten.core import SimulationConfig
from emergenz_knoten.kernels import double_gaussian_gradient, exponential_memory_weights
from emergenz_knoten.vector_memory import (
    VectorMemoryConfig,
    alignment_history_head_jacobian,
    normalize_orientation,
    vector_gaussian_field,
)


def _fixture(dim, eta_vector):
    history = np.zeros((5, dim))
    history[:, :3] = [
        [0.7, 0, 0.2],
        [0, -0.7, -0.2],
        [-0.7, 0, 0.2],
        [0, 0.7, -0.2],
        [0.7, 0, 0.2],
    ]
    config = VectorMemoryConfig(
        scalar=SimulationConfig(
            steps=4,
            dim=dim,
            epsilon=0,
            alpha=0.6,
            memory_factor=4,
            max_memory=4,
            memory_mass=1.1,
            eta=0.7,
            amplitude_rep=0,
            amplitude_att=1.3,
            sigma_att=1.6,
        ),
        lambda_vector=0.4,
        vector_memory_factor=4,
        max_vector_memory=4,
        vector_mass=0.8,
        sigma_vector=1.2,
        eta_vector=eta_vector,
    )
    return history, config


def _head(history, config):
    scalar = config.scalar
    directions = np.array(
        [normalize_orientation(step) for step in history[:-1] - history[1:]]
    )
    gradient = double_gaussian_gradient(
        history[0],
        history[:4],
        exponential_memory_weights(scalar.alpha, 4, memory_mass=scalar.memory_mass),
        sigma_rep=scalar.sigma_rep,
        sigma_att=scalar.sigma_att,
        amplitude_rep=scalar.amplitude_rep,
        amplitude_att=scalar.amplitude_att,
    )
    field = vector_gaussian_field(
        history[0],
        history[:4],
        directions,
        exponential_memory_weights(
            config.lambda_vector, 4, memory_mass=config.vector_mass
        ),
        sigma=config.sigma_vector,
    )
    return history[0] - scalar.eta * gradient + config.eta_vector * field


def _normal_row(s, q, g, f, b, c_one, c_two):
    return np.array(
        [
            1 - c_one * (s + s**3) - c_two * s**2 + b,
            c_one * s + b * (g * q - 1),
            c_two * s**2 + b * (f * q**2 - g * q),
            c_one * s**3 + b * (g * q**3 - f * q**2),
            -b * g * q**3,
        ]
    )


@pytest.mark.parametrize("dim", [4, 5])
@pytest.mark.parametrize("eta_vector", [-0.9, 0.9])
def test_normal_blocks_match_native_derivative_and_fixed_off_orbit_differences(
    dim, eta_vector
):
    history, config = _fixture(dim, eta_vector)
    expected_head = history[3]
    assert np.linalg.norm(_head(history, config) - expected_head) > 0.1
    scalar = config.scalar
    s, q = 1 - scalar.alpha, 1 - config.lambda_vector
    length_squared = np.sum((history[0] - history[1]) ** 2)
    opposite_squared = np.sum((history[0] - history[2]) ** 2)
    g = np.exp(-length_squared / (2 * config.sigma_vector**2))
    f = np.exp(-opposite_squared / (2 * config.sigma_vector**2))
    b = (
        config.eta_vector
        * config.lambda_vector
        * config.vector_mass
        / np.sqrt(length_squared)
    )
    prefactor = (
        scalar.eta
        * scalar.alpha
        * scalar.memory_mass
        * scalar.amplitude_att
        / scalar.sigma_att**2
    )
    c_one = prefactor * np.exp(-length_squared / (2 * scalar.sigma_att**2))
    c_two = prefactor * np.exp(-opposite_squared / (2 * scalar.sigma_att**2))
    row = _normal_row(s, q, g, f, b, c_one, c_two)
    blocks = alignment_history_head_jacobian(history, config)
    base = alignment_history_head_jacobian(
        history[:, :3], replace(config, scalar=replace(scalar, dim=3))
    )
    np.testing.assert_allclose(blocks[:, :3, :3], base, atol=2e-16)
    np.testing.assert_array_equal(blocks[:, :3, 3:], 0)
    np.testing.assert_array_equal(blocks[:, 3:, :3], 0)
    np.testing.assert_allclose(
        blocks[:, 3:, 3:], row[:, None, None] * np.eye(dim - 3), atol=3e-16
    )
    for age in range(5):
        for axis in range(3, dim):
            offset = np.zeros_like(history)
            offset[age, axis] = 1e-6
            difference = (
                _head(history + offset, config) - _head(history - offset, config)
            ) / 2e-6
            np.testing.assert_allclose(
                difference, row[age] * np.eye(dim)[axis], atol=3e-10
            )


def test_oblique_extra_direction_has_the_same_normal_row():
    history, config = _fixture(4, 0.9)
    vector = np.array([1, 2, -1, 2], dtype=float)
    transform = np.eye(4) - 2 * np.outer(vector, vector) / np.dot(vector, vector)
    normal = transform[:, 3]
    base = alignment_history_head_jacobian(history, config)
    tilted = alignment_history_head_jacobian(history @ transform.T, config)
    np.testing.assert_allclose(
        np.einsum("i,aij,j->a", normal, tilted, normal), base[:, 3, 3], atol=3e-16
    )
    np.testing.assert_allclose(
        np.einsum("aij,j->ai", tilted, normal), base[:, 3, 3, None] * normal, atol=3e-16
    )


def test_formal_force_balances_reduce_the_normal_row_exactly():
    # Formal coefficients already used in the quotient audit, not native orbit parameters.
    f, g, q, s = map(F, ["1/3", "1/2", "3/5", "2/5"])
    delta = s**2 * (1 - g * q) - q**2 * (f - g * q)
    b = 1 / delta
    c_one, c_two = b * (1 - g * q) / s, b * q * (g - f * q) / s**2
    mu = b * q**3 * g
    np.testing.assert_array_equal(
        _normal_row(s, q, g, f, b, c_one, c_two), [mu, 0, 0, 1, -mu]
    )
    assert delta - g * q**3 == s**2 * (1 - g * q) - f * q**2


@pytest.mark.parametrize("mu", [F(-3, 2), F(0), F(2, 3), F(-1), F(1)])
def test_exact_formal_companion_quotient_and_four_step_symmetry(mu):
    # Pure companion matrices: these values are not evaluated at any positive candidate.
    matrix = np.zeros((5, 5), dtype=object)
    matrix[0] = [mu, 0, 0, 1, -mu]
    matrix[1:, :-1] = np.eye(4, dtype=int)
    identity = np.eye(5, dtype=int)
    quotient = np.array([1, 0, 0, 0, -1], dtype=object)
    np.testing.assert_array_equal(quotient @ matrix, mu * quotient)
    np.testing.assert_array_equal(
        quotient @ np.linalg.matrix_power(matrix, 4), mu**4 * quotient
    )
    np.testing.assert_array_equal(
        np.linalg.matrix_power(matrix, 5)
        - mu * np.linalg.matrix_power(matrix, 4)
        - matrix
        + mu * identity,
        np.zeros((5, 5)),
    )
    coordinates = np.array(
        [
            [1, 1, 0, F(1, 4)],
            [1, 0, -1, F(-1, 4)],
            [1, -1, 0, F(1, 4)],
            [1, 0, 1, F(-1, 4)],
            [1, 1, 0, F(1, 4)],
        ],
        dtype=object,
    )
    assert np.linalg.matrix_rank(np.asarray(coordinates, dtype=float)) == 4
    np.testing.assert_array_equal(quotient @ coordinates, np.zeros(4))
    np.testing.assert_array_equal(
        np.linalg.matrix_power(matrix, 4) @ coordinates, coordinates
    )


def test_known_negative_control_has_the_existing_rational_normal_factor():
    b, q, g = F(-24), F(1, 2), F(1, 2)
    s, c_one, c_two = F(1, 6), F(-108), F(-108)
    mu = b * q**3 * g
    assert mu == F(-3, 2)
    np.testing.assert_array_equal(
        _normal_row(s, q, g, g, b, c_one, c_two), [mu, 0, 0, 1, -mu]
    )


def _oriented_four_volume(history):
    differences = history[1:] - history[0]
    return np.array(
        [
            np.linalg.det(differences[:, axes])
            for axes in combinations(range(history.shape[1]), 4)
        ]
    )


@pytest.mark.parametrize("dim", [4, 5])
@pytest.mark.parametrize("eta_vector", [-0.9, 0.0, 0.9])
def test_native_update_multiplies_every_four_volume_minor_by_the_tail_coefficient(
    dim, eta_vector
):
    history, config = _fixture(dim, eta_vector)
    history[-1, 3:] = np.arange(1, dim - 2) * 0.23
    history[:4, 3:] += np.array([0.1, -0.2, 0.03, 0.04])[:, None]
    history += np.linspace(-0.9, 0.8, dim)
    tail = (
        -eta_vector
        * exponential_memory_weights(
            config.lambda_vector, 4, memory_mass=config.vector_mass
        )[3]
        * np.exp(-np.sum((history[0] - history[3]) ** 2) / (2 * config.sigma_vector**2))
        / np.linalg.norm(history[3] - history[4])
    )
    before = _oriented_four_volume(history)
    after = _oriented_four_volume(np.vstack([_head(history, config), history[:4]]))
    assert np.linalg.norm(before) > 0.1
    np.testing.assert_allclose(after, tail * before, atol=3e-16)
    if eta_vector != 0:
        assert np.linalg.norm(after) > 1e-3


def test_fixed_head_innovation_injects_the_normal_component_into_oriented_volume():
    history, config = _fixture(4, 0.9)
    head = _head(history, config)
    innovation = np.array([0.12, -0.21, 0.18, -0.3])
    shifted = np.vstack([head, history[:4]])
    perturbed = shifted.copy()
    perturbed[0] += innovation
    base = history[1:4, :3] - history[0, :3]
    expected = np.linalg.det(base) * innovation[3]
    assert abs(expected) > 0.1
    np.testing.assert_array_equal(_oriented_four_volume(shifted), [0])
    np.testing.assert_allclose(_oriented_four_volume(perturbed), [expected], atol=2e-16)
