"""Off-orbit derivative algebra only; the pending positive target is not evaluated."""

from dataclasses import replace
from fractions import Fraction
from math import prod

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


def _fixture(sigma_scalar=0.9, eta_vector=0.7):
    radius, height = 0.8, 0.3
    history = np.array(
        [
            [radius, 0, height],
            [0, -radius, -height],
            [-radius, 0, height],
            [0, radius, -height],
            [radius, 0, height],
        ]
    )
    symmetry = np.array([[0, -1, 0], [1, 0, 0], [0, 0, -1]])
    config = VectorMemoryConfig(
        scalar=SimulationConfig(
            steps=4,
            dim=3,
            epsilon=0,
            alpha=0.6,
            memory_factor=4,
            max_memory=4,
            memory_mass=1.1,
            eta=0.7,
            amplitude_rep=0,
            amplitude_att=1.3,
            sigma_att=sigma_scalar,
        ),
        lambda_vector=0.4,
        vector_memory_factor=4,
        max_vector_memory=4,
        vector_mass=0.9,
        sigma_vector=1.2,
        eta_vector=eta_vector,
    )
    return history, symmetry, config


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
    vector = vector_gaussian_field(
        history[0],
        history[:4],
        directions,
        exponential_memory_weights(
            config.lambda_vector, 4, memory_mass=config.vector_mass
        ),
        sigma=config.sigma_vector,
    )
    return history[0] - scalar.eta * gradient + config.eta_vector * vector


def _matrix(blocks, symmetry):
    native = np.zeros((15, 15))
    native[:3] = np.concatenate(blocks, axis=1)
    native[3:, :-3] = np.eye(12)
    return np.kron(np.eye(5), symmetry.T) @ native


@pytest.mark.parametrize("sigma_scalar", [0.9, 1.4])
@pytest.mark.parametrize("eta_vector", [-0.7, 0.7])
def test_trace_and_zero_coefficient_identities_at_fixed_off_orbit_histories(
    sigma_scalar, eta_vector
):
    history, symmetry, config = _fixture(sigma_scalar, eta_vector)
    assert np.linalg.norm(_head(history, config) - symmetry @ history[0]) > 0.1
    blocks = alignment_history_head_jacobian(history, config)
    matrix = _matrix(blocks, symmetry)
    radius, height = history[0, 0], history[0, 2]
    length_squared = 2 * radius**2 + 4 * height**2
    scalar, sigma = config.scalar, config.sigma_vector
    s, q = 1 - scalar.alpha, 1 - config.lambda_vector
    g, f = np.exp(-length_squared / (2 * sigma**2)), np.exp(-2 * radius**2 / sigma**2)
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
    c_two = prefactor * np.exp(-2 * radius**2 / scalar.sigma_att**2)
    gamma = 4 * height**2 / length_squared
    expected_trace = (
        -1
        + c_one * (s + s**3)
        + c_two * s**2
        - b
        + b * gamma
        - 4 * height**2 / scalar.sigma_att**2 * c_one * (s + s**3)
        + b
        / sigma**2
        * (2 * radius**2 * (g * q + f * q**2) - 4 * height**2 * g * (q + q**3))
    )
    assert np.trace(matrix) == pytest.approx(expected_trace, abs=8e-16)
    # d det(lambda I-M)/d lambda at zero is the sum of diagonal cofactors of -M.
    derivative = sum(
        np.linalg.det(np.delete(np.delete(-matrix, j, axis=0), j, axis=1))
        for j in range(15)
    )
    expected_derivative = (b * q**3 * g) ** 2 * (
        c_one * s**3 * (4 * height**2 / scalar.sigma_att**2 - gamma)
        + 4 * b * q**3 * g * height**2 / sigma**2
    )
    assert derivative == pytest.approx(expected_derivative, abs=3e-18, rel=2e-12)
    # No symmetry factors are removed: these states are not relative orbits.


@pytest.mark.parametrize("value", [1 / 3, -0.8, 0.2 + 0.3j])
def test_block_companion_characteristic_identity_without_orbit_assumption(value):
    history, symmetry, config = _fixture()
    blocks = alignment_history_head_jacobian(history, config)
    matrix = _matrix(blocks, symmetry)
    polynomial = value**5 * symmetry - sum(
        value ** (4 - age) * blocks[age] @ np.linalg.matrix_power(symmetry, -age)
        for age in range(5)
    )
    direct = np.linalg.det(value * np.eye(15) - matrix)
    compressed = np.linalg.det(symmetry.T) * np.linalg.det(polynomial)
    assert direct == pytest.approx(compressed, abs=3e-15, rel=2e-12)


@pytest.mark.parametrize(
    "scale,amplitude,scalar_mass,vector_mass",
    [
        (0.5, 1.0, 1.0, 1.0),
        (2.0, 1.0, 1.0, 1.0),
        (1.0, 1.7, 2.3, 0.6),
        (2.0, 1.7, 2.3, 0.6),
    ],
)
def test_common_scale_and_compensated_normalizations_leave_local_blocks_unchanged(
    scale, amplitude, scalar_mass, vector_mass
):
    history, _, config = _fixture()
    scalar = config.scalar
    scaled = replace(
        config,
        scalar=replace(
            scalar,
            sigma_rep=scale * scalar.sigma_rep,
            sigma_att=scale * scalar.sigma_att,
            amplitude_att=amplitude * scalar.amplitude_att,
            memory_mass=scalar_mass * scalar.memory_mass,
            eta=scale**2 * scalar.eta / (amplitude * scalar_mass),
        ),
        sigma_vector=scale * config.sigma_vector,
        vector_mass=vector_mass * config.vector_mass,
        eta_vector=scale * config.eta_vector / vector_mass,
    )
    np.testing.assert_allclose(
        _head(scale * history, scaled), scale * _head(history, config), atol=8e-16
    )
    np.testing.assert_allclose(
        alignment_history_head_jacobian(scale * history, scaled),
        alignment_history_head_jacobian(history, config),
        atol=6e-16,
    )


def test_trace_and_product_inside_their_bounds_do_not_prove_stability():
    roots = [Fraction(6, 5)] + [Fraction(1, 5)] * 7
    assert abs(sum(roots)) < 8
    assert abs(prod(roots)) < 1
    assert roots[0] > 1  # Pure polynomial countercontrol, not a native state.


def test_force_elimination_simplifies_trace_and_product_as_exact_formal_identities():
    # Independent formal coefficients, not a geometry or a target parameter set.
    f, g, q, s = map(Fraction, ["1/3", "1/2", "3/5", "2/5"])
    radial, height = Fraction(2, 5), Fraction(1, 20)
    gamma = 4 * height / (2 * radial + 4 * height)
    b = 1 / (s**2 * (1 - g * q) - q**2 * (f - g * q))
    c_one, c_two = b * (1 - g * q) / s, b * q * (g - f * q) / s**2
    raw_trace = (
        -1
        + c_one * (s + s**3)
        + c_two * s**2
        - b
        + b * gamma
        - 4 * height * c_one * (s + s**3)
        + b * (2 * radial * (g * q + f * q**2) - 4 * height * g * (q + q**3))
    )
    simplified_trace = -4 * height + b * (
        gamma
        - g * q**3
        + 2 * radial * g * q
        + (2 * radial - 4 * height) * f * q**2
        - 4 * height
    )
    assert raw_trace == simplified_trace
    raw_product = (b * q**3 * g) ** 2 * (
        c_one * s**3 * (gamma - 4 * height) - 4 * b * q**3 * g * height
    )
    simplified_product = (
        b**3
        * q**6
        * g**2
        * (s**2 * (1 - g * q) * (gamma - 4 * height) - 4 * q**3 * g * height)
    )
    assert raw_product == simplified_product
