"""Fixed algebra/force/field substitutions; no trajectory or stability run."""

from fractions import Fraction as F

import numpy as np
import pytest

from emergenz_knoten.kernels import (
    double_gaussian_gradient,
    effective_double_gaussian_parameters,
    exponential_memory_weights,
)
from emergenz_knoten.vector_memory import normalize_orientation, vector_gaussian_field


def _symmetry():
    return np.array([[0, -1, 0], [1, 0, 0], [0, 0, -1]])


def _history(radius, height):
    return np.array(
        [
            [radius, 0, height],
            [0, -radius, -height],
            [-radius, 0, height],
            [0, radius, -height],
            [radius, 0, height],
        ]
    )


def _increments(s, q, g, f, b, c_one, c_two):
    return (
        -c_one * (s + s**3) - 2 * c_two * s**2 + b * (1 + g * q - f * q**2 - g * q**3),
        -c_one * (s - s**3) + b * (1 - g * q - f * q**2 + g * q**3),
        -2 * c_one * (s + s**3) + 2 * b * (1 - g * q + f * q**2 - g * q**3),
    )


@pytest.mark.parametrize(
    "f,g", [(F(1, 2), F(2, 3)), (F(1, 4), F(2, 5)), (F(4, 5), F(22, 25))]
)
@pytest.mark.parametrize("q", [F(1, 3), F(2, 3), F(99, 100)])
def test_exact_positive_family_identities(f, g, q):
    # A fixed algebraic substitution table, not a parameter search or fit.
    assert 0 < f < g < 1 and g**4 > f**3 and g**2 < f
    s = q * g * (g - f * q) / (f * (1 - g * q))
    delta = s**2 * (1 - g * q) - q**2 * (f - g * q)
    p_zero = g**4 - f**3
    p_one = (g - f) * (g**2 * (g - f) + f**2 * (1 - g))
    polynomial = g**4 - f**3 + f * g * q * (f**2 + f - 2 * g**2)
    assert polynomial == (1 - q) * p_zero + q * p_one
    assert delta == q**2 * polynomial / (f**2 * (1 - g * q))
    assert 0 < s < q < 1 and delta > 0
    b = 1 / delta
    c_one = b * (1 - g * q) / s
    c_two = b * q * (g - f * q) / s**2
    assert b > 0 and c_one > 0 and c_two > 0
    assert c_two / c_one == f / g
    assert _increments(s, q, g, f, b, c_one, c_two) == (-1, 1, -2)


@pytest.mark.parametrize("deposition", ["delta", "gaussian", "matched_gaussian"])
@pytest.mark.parametrize("eta_vector", [-0.9, 0.9])
def test_three_force_components_match_native_readouts_at_each_prescribed_phase(
    deposition, eta_vector
):
    radius, height, sigma, s, q = 0.7, 0.2, 1.2, 0.4, 0.6
    scalar_mass, vector_mass, eta_scalar = 1.1, 0.8, 0.7
    history, symmetry = _history(radius, height), _symmetry()
    length = np.sqrt(2 * radius**2 + 4 * height**2)
    g = np.exp(-(length**2) / (2 * sigma**2))
    f = np.exp(-2 * radius**2 / sigma**2)
    kernel = dict(
        sigma_rep=0.8,
        sigma_att=1.6,
        amplitude_rep=0.9,
        amplitude_att=1.3,
        deposition_kernel=deposition,
        deposition_sigma=0.3 if deposition == "gaussian" else 0,
    )
    effective = effective_double_gaussian_parameters(dim=3, **kernel)

    def radial(distance_squared):
        return sum(
            sign
            * effective[f"amplitude_{label}"]
            / effective[f"sigma_{label}"] ** 2
            * np.exp(-distance_squared / (2 * effective[f"sigma_{label}"] ** 2))
            for sign, label in [(-1, "rep"), (1, "att")]
        )

    c_one = eta_scalar * (1 - s) * scalar_mass * radial(length**2)
    c_two = eta_scalar * (1 - s) * scalar_mass * radial(4 * radius**2)
    b = eta_vector * (1 - q) * vector_mass / length
    predicted = np.array(_increments(s, q, g, f, b, c_one, c_two)) * [
        radius,
        radius,
        height,
    ]
    assert np.linalg.norm(predicted - (symmetry @ history[0] - history[0])) > 0.1
    for phase in range(4):
        transform = np.linalg.matrix_power(symmetry, phase)
        state = history @ transform.T
        directions = np.array(
            [normalize_orientation(step) for step in state[:-1] - state[1:]]
        )
        native = -eta_scalar * double_gaussian_gradient(
            state[0],
            state[:4],
            exponential_memory_weights(1 - s, 4, memory_mass=scalar_mass),
            **kernel,
        ) + eta_vector * vector_gaussian_field(
            state[0],
            state[:4],
            directions,
            exponential_memory_weights(1 - q, 4, memory_mass=vector_mass),
            sigma=sigma,
        )
        np.testing.assert_allclose(native, transform @ predicted, atol=3e-16)


@pytest.mark.parametrize("gap_factor", [0.5, 2.0])
def test_exact_defect_root_and_binding_boundary_on_opposite_sides(gap_factor):
    radius, height, sigma = 0.7, 0.2, 1.2
    history, symmetry = _history(radius, height), _symmetry()
    length = np.sqrt(2 * radius**2 + 4 * height**2)
    threshold = 2 * height**2 * radius**2 / (sigma**2 * (radius**2 + 4 * height**2))
    q = np.exp(-gap_factor * threshold)
    u = sigma**2 * np.log(q)
    root = np.array([u / radius, -u / radius, u / (2 * height)])
    barycentric = np.array(
        [
            0.25 + u / (8 * height**2) + u / (2 * radius**2),
            0.25 - u / (8 * height**2) + u / (2 * radius**2),
            0.25 + u / (8 * height**2) - u / (2 * radius**2),
            0.25 - u / (8 * height**2) - u / (2 * radius**2),
        ]
    )
    np.testing.assert_allclose(barycentric @ history[:4], root, atol=2e-16)
    assert barycentric.sum() == pytest.approx(1)
    assert bool(np.all(barycentric > 0)) == (gap_factor < 1)
    directions = (history[:-1] - history[1:]) / length
    assert np.linalg.matrix_rank(directions) == 3
    np.testing.assert_allclose(directions.sum(axis=0), 0, atol=1e-16)
    weights = exponential_memory_weights(1 - q, 4)
    coefficients = weights * np.exp(
        -np.sum((root - history[:4]) ** 2, axis=1) / (2 * sigma**2)
    )
    np.testing.assert_allclose(coefficients, coefficients[0], atol=3e-17)
    jacobian = (
        coefficients[0]
        / (sigma**2 * length)
        * np.array(
            [
                [2 * radius**2, -2 * radius**2, 0],
                [2 * radius**2, 2 * radius**2, 0],
                [0, 0, 8 * height**2],
            ]
        )
    )
    determinant = (
        (coefficients[0] / sigma**2) ** 3 * 64 * radius**4 * height**2 / length**3
    )
    assert np.linalg.det(jacobian) == pytest.approx(determinant, rel=2e-15)
    assert determinant > 0
    for axis in np.eye(3):
        plus = vector_gaussian_field(
            root + 1e-6 * axis, history[:4], directions, weights, sigma=sigma
        )
        minus = vector_gaussian_field(
            root - 1e-6 * axis, history[:4], directions, weights, sigma=sigma
        )
        np.testing.assert_allclose((plus - minus) / 2e-6, jacobian @ axis, atol=1e-11)
    for phase in range(4):
        transform = np.linalg.matrix_power(symmetry, phase)
        field = vector_gaussian_field(
            transform @ root,
            history[:4] @ transform.T,
            directions @ transform.T,
            weights,
            sigma=sigma,
        )
        np.testing.assert_allclose(field, 0, atol=3e-17)


@pytest.mark.parametrize("q", [F(1, 3), F(2, 3), F(99, 100)])
def test_equal_distance_limit_recovers_the_regular_positive_gain_obstruction(q):
    g = f = F(1, 2)
    s = q * g * (g - f * q) / (f * (1 - g * q))
    delta = s**2 * (1 - g * q) - q**2 * (f - g * q)
    assert s == g * q * (1 - q) / (1 - g * q)
    assert delta < 0


def test_proposed_fixed_stability_witness_has_a_rational_binding_margin():
    # log(2)>0.69 and log(9/8)>2/17 by log(x)=2*atanh((x-1)/(x+1)).
    assert 2 * (F(1, 3) + F(1, 81)) > F(69, 100)
    radius_squared_lower, height_squared_lower = F(69, 200), F(1, 34)
    threshold_lower = (
        2
        * height_squared_lower
        * radius_squared_lower
        / (radius_squared_lower + 4 * height_squared_lower)
    )
    # -log(99/100)<1/99. This checks an analytic margin, not a stability run.
    assert F(1, 99) < threshold_lower
