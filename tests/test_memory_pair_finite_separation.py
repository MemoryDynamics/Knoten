"""Finite-distance Taylor bounds and conditional ensemble reciprocity.

Constructed one-step states and finite phase sums only, not orbit formation,
stability, averaging-limit or particle-emergence tests.
"""

from dataclasses import replace
from itertools import product

import numpy as np
import pytest

from emergenz_knoten import FiniteMemoryState, SimulationConfig
from emergenz_knoten.kernels import (
    double_gaussian_gradient,
    double_gaussian_hessian,
    effective_double_gaussian_parameters,
    exponential_memory_weights,
    gaussian_gradient,
)
from emergenz_knoten.quasistatic_pair import rigid_full_memory_pair_interaction
from emergenz_knoten.reciprocal_nodes import reciprocal_pair_response
from emergenz_knoten.state import memory_centroid, memory_shape_tensor


PARAMETERS = dict(sigma_rep=1.0, sigma_att=2.0, amplitude_rep=1.0, amplitude_att=3.0)


def _terms(parameters):
    return (
        (parameters["amplitude_rep"], parameters["sigma_rep"]),
        (-parameters["amplitude_att"], parameters["sigma_att"]),
    )


def _g(point, parameters=PARAMETERS):
    return double_gaussian_gradient(point, [np.zeros_like(point)], [1.0], **parameters)


def _hessian(point, parameters):
    return double_gaussian_hessian(point, [np.zeros_like(point)], [1.0], **parameters)


def _third_contraction(point, matrix, parameters):
    result = np.zeros_like(point)
    for amplitude, sigma in _terms(parameters):
        factor = amplitude * np.exp(-np.dot(point, point) / (2 * sigma**2))
        result += factor * (
            (np.trace(matrix) * point + 2 * matrix @ point) / sigma**4
            - np.dot(point, matrix @ point) * point / sigma**6
        )
    return result


def _derivative_bound(order, point, radius, parameters):
    low = max(0.0, np.linalg.norm(point) - radius)
    high = np.linalg.norm(point) + radius
    result = 0.0
    for amplitude, sigma in _terms(parameters):
        polynomial = (
            high**3 / sigma**6 + 3 * high / sigma**4
            if order == 3
            else high**4 / sigma**8 + 6 * high**2 / sigma**6 + 3 / sigma**4
        )
        result += abs(amplitude) * np.exp(-(low**2) / (2 * sigma**2)) * polynomial
    return result


def _config(dim, deposition_sigma):
    return SimulationConfig(
        steps=1,
        dim=dim,
        epsilon=0.0,
        eta=0.0,
        alpha=0.2,
        memory_mass=1.0,
        deposition_kernel="gaussian" if deposition_sigma else "delta",
        deposition_sigma=deposition_sigma,
        **PARAMETERS,
        memory_factor=1.0,
        max_memory=5,
        burn_in=0,
        sample_every=1,
    )


def _state(config, scale, phase):
    memory = scale * np.sin(np.arange(5 * config.dim).reshape(5, config.dim) + phase)
    weights = exponential_memory_weights(
        config.alpha, 5, memory_mass=config.memory_mass
    )
    memory -= np.average(memory, axis=0, weights=weights)
    return FiniteMemoryState(memory[0], memory, weights)


def _expansion(r, receiver, source, parameters):
    offset = receiver.x - memory_centroid(receiver)
    centered = source.memory - memory_centroid(source)
    weights = source.weights / source.weights.sum()
    covariance = memory_shape_tensor(source)
    radius = np.linalg.norm(offset) + np.linalg.norm(centered, axis=1).max()
    displacements = offset - centered
    exact = double_gaussian_gradient(r + offset, centered, weights, **parameters)
    approximation = (
        _g(r, parameters)
        + _hessian(r, parameters) @ offset
        + 0.5 * _third_contraction(r, np.outer(offset, offset) + covariance, parameters)
    )
    third_moment = np.dot(weights, np.linalg.norm(displacements, axis=1) ** 3)
    remainder_bound = _derivative_bound(4, r, radius, parameters) * third_moment / 6
    monopole_bound = np.linalg.norm(_hessian(r, parameters), ord=2) * np.linalg.norm(
        offset
    ) + 0.5 * _derivative_bound(3, r, radius, parameters) * (
        np.dot(offset, offset) + np.trace(covariance)
    )
    return exact, approximation, remainder_bound, monopole_bound


@pytest.mark.parametrize("dim,deposition_sigma", [(3, 0.0), (5, 0.4)])
def test_finite_distance_shape_expansion_bounds_and_native_center_response(
    dim, deposition_sigma
):
    first_config = _config(dim, deposition_sigma)
    second_config = replace(first_config, alpha=0.35, memory_mass=1.7)
    first = _state(first_config, 0.04, 0.0)
    second = _state(second_config, 0.07, 0.4)
    r = np.linspace(0.1, 0.3, dim)
    r[0] = 2.3
    parameters = effective_double_gaussian_parameters(
        dim=dim,
        deposition_kernel=first_config.deposition_kernel,
        deposition_sigma=deposition_sigma,
        **PARAMETERS,
    )
    a = _expansion(r, first, second, parameters)
    b = _expansion(-r, second, first, parameters)
    for origin, (exact, approximation, remainder, monopole) in ((r, a), (-r, b)):
        assert np.linalg.norm(exact - approximation) <= remainder + 1e-15
        assert remainder > 0
        assert np.linalg.norm(exact - approximation) > 1e-9
        assert np.linalg.norm(exact - _g(origin, parameters)) <= monopole + 1e-15

    u_a, u_b = first.x, second.x
    imbalance_approximation = _hessian(r, parameters) @ (u_a + u_b)
    imbalance_approximation += 0.5 * _third_contraction(
        r,
        np.outer(u_a, u_a)
        - np.outer(u_b, u_b)
        + memory_shape_tensor(second)
        - memory_shape_tensor(first),
        parameters,
    )
    np.testing.assert_allclose(a[1] + b[1], imbalance_approximation, atol=1e-15)
    assert np.linalg.norm(a[0] + b[0] - imbalance_approximation) <= a[2] + b[2]

    chi = 0.02
    response = reciprocal_pair_response(
        first,
        second,
        first_config,
        second_config=second_config,
        initial_center_separation=-r,
        cross_eta=chi,
        first_noise=np.zeros((1, dim)),
        second_noise=np.zeros((1, dim)),
        sample_steps=[0, 1],
    )
    increments = response.positions[1, 2] - response.positions[1, 0]
    expected = -chi * np.array(
        [second.weights.sum() * a[0], first.weights.sum() * b[0]]
    )
    np.testing.assert_allclose(increments, expected, atol=2e-15)
    beta = np.array([s.weights[0] / s.weights.sum() for s in (first, second)])
    np.testing.assert_allclose(
        response.memory_centers[1, 2] - response.memory_centers[1, 0],
        beta[:, None] * increments,
        atol=2e-15,
    )


def test_third_derivative_contraction_matches_independent_hessian_differences():
    r = np.array([1.7, 0.3, -0.4])
    factors = np.array([[0.1, 0.2], [0.3, -0.1], [0.2, 0.1]])
    matrix = factors @ factors.T
    step = 1e-5
    finite_difference = np.zeros(3)
    for vector in factors.T:
        finite_difference += (
            (
                _hessian(r + step * vector, PARAMETERS)
                - _hessian(r - step * vector, PARAMETERS)
            )
            @ vector
            / (2 * step)
        )
    np.testing.assert_allclose(
        _third_contraction(r, matrix, PARAMETERS),
        finite_difference,
        rtol=2e-8,
        atol=1e-10,
    )


def test_equal_rms_radius_does_not_fix_shape_response():
    cloud = np.array(
        [[0, 0, 0], [0.06, 0, 0], [-0.06, 0, 0], [0, 0.14, 0], [0, -0.14, 0]]
    )
    weights = np.array([0.4, 0.15, 0.15, 0.15, 0.15])
    rotation = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]])
    first = FiniteMemoryState(np.zeros(3), cloud, weights)
    second = FiniteMemoryState(np.zeros(3), cloud @ rotation.T, weights)
    assert np.trace(memory_shape_tensor(first)) == pytest.approx(
        np.trace(memory_shape_tensor(second))
    )
    r = np.array([2.0, 0.3, 0.0])
    a = _expansion(r, first, first, PARAMETERS)
    b = _expansion(r, first, second, PARAMETERS)
    assert np.linalg.norm(a[0] - b[0]) > 1e-4
    assert np.linalg.norm(a[0] - b[0] - (a[1] - b[1])) <= a[2] + b[2]


def test_small_radius_over_distance_does_not_control_relative_gaussian_force_error():
    radius = 0.2
    ratios = []
    for distance in (4.0, 8.0, 16.0):
        point = np.array([distance])
        exact = gaussian_gradient(point, [[radius], [-radius]], [0.5, 0.5], sigma=1.0)[
            0
        ]
        monopole = gaussian_gradient(point, [[0.0]], [1.0], sigma=1.0)[0]
        ratio = np.exp(-(radius**2) / 2) * (
            np.cosh(distance * radius) - radius / distance * np.sinh(distance * radius)
        )
        assert exact / monopole == pytest.approx(ratio, rel=3e-14)
        ratios.append(ratio)
    assert np.all(np.diff(ratios) > 0)
    assert radius / distance < 0.02 and ratios[-1] > 10


def _cycle(count, radius, aspect=1.0):
    angle = np.arange(count) * 2 * np.pi / count
    return radius * np.column_stack(
        [np.cos(angle), aspect * np.sin(angle), np.zeros(count)]
    )


@pytest.mark.parametrize("speed", [0.0, 0.02])
def test_freezing_a_moving_source_center_has_a_weighted_age_error_bound(speed):
    cycle = _cycle(4, 0.35)
    weights = exponential_memory_weights(0.35, 3, memory_mass=1.7)
    ages = np.arange(3)
    history = cycle[(-ages) % len(cycle)]
    velocity = speed * np.array([1.0, -0.5, 0.25])
    moving_history = history - ages[:, None] * velocity
    point = np.array([2.0, 0.4, 0.1])
    frozen = double_gaussian_gradient(point, history, weights, **PARAMETERS)
    actual = double_gaussian_gradient(point, moving_history, weights, **PARAMETERS)
    global_lipschitz = sum(abs(a) / sigma**2 for a, sigma in _terms(PARAMETERS))
    bound = global_lipschitz * np.linalg.norm(velocity) * np.dot(weights, ages)
    assert np.linalg.norm(actual - frozen) <= bound + 1e-15
    if speed:
        assert np.linalg.norm(actual - frozen) > 1e-4
    else:
        np.testing.assert_array_equal(actual, frozen)


def _phase_gradients(r, cycles, weights, phases):
    a, b = phases
    first, second = cycles
    a_history = first[(a - np.arange(len(weights[0]))) % len(first)]
    b_history = second[(b - np.arange(len(weights[1]))) % len(second)]
    return np.array(
        [
            double_gaussian_gradient(r + first[a], b_history, weights[1], **PARAMETERS),
            double_gaussian_gradient(
                -r + second[b], a_history, weights[0], **PARAMETERS
            ),
        ]
    )


def _cloud_interaction(r, cycles, masses, chi):
    states = [
        FiniteMemoryState(cycle[0], cycle, np.full(len(cycle), mass / len(cycle)))
        for cycle, mass in zip(cycles, masses, strict=True)
    ]

    def potential(radius):
        return chi * sum(
            a * np.exp(-(radius**2) / (2 * s**2)) for a, s in _terms(PARAMETERS)
        )

    def derivative(radius):
        return chi * sum(
            -a * radius / s**2 * np.exp(-(radius**2) / (2 * s**2))
            for a, s in _terms(PARAMETERS)
        )

    return rigid_full_memory_pair_interaction(
        *states,
        -r,
        radial_pair_energy=potential,
        radial_pair_energy_derivative=derivative,
    )


@pytest.mark.parametrize("second_alpha", [0.2, 0.45])
def test_independent_stationary_phase_average_matches_existing_rigid_cloud_law(
    second_alpha,
):
    cycles = [_cycle(4, 0.25), _cycle(6, 0.5, 0.6)]
    weights = [
        exponential_memory_weights(0.2, 3),
        exponential_memory_weights(second_alpha, 3, memory_mass=1.7),
    ]
    masses = np.array([w.sum() for w in weights])
    r = np.array([2.0, 0.4, 0.1])
    averaged = np.mean(
        [
            _phase_gradients(r, cycles, weights, phases)
            for phases in product(range(4), range(6))
        ],
        axis=0,
    )
    chi = 0.02
    declared_forces = -chi * masses[:, None] * averaged
    interaction = _cloud_interaction(r, cycles, masses, chi)
    np.testing.assert_allclose(declared_forces.sum(axis=0), 0, atol=1e-16)
    np.testing.assert_allclose(
        declared_forces[0], interaction.force_on_first, atol=1e-16
    )
    np.testing.assert_allclose(
        declared_forces[1], interaction.force_on_second, atol=1e-16
    )


def test_stationary_locked_phases_preserve_a_lag_reciprocity_defect():
    cycle = _cycle(4, 0.35)
    cycles = [cycle, cycle]
    weights = [exponential_memory_weights(0.5, 2)] * 2
    mass = weights[0].sum()
    probability = weights[0] / mass
    r = np.array([2.0, 0.4, 0.1])

    def lag_gradient(lag, phase_difference):
        return np.mean(
            [
                _g(r + cycle[t] - cycle[(t - lag + phase_difference) % 4])
                for t in range(4)
            ],
            axis=0,
        )

    # A uniform common phase is stationary but is not a product ensemble.
    for phase_difference in (0, 1):
        averaged = np.mean(
            [
                _phase_gradients(r, cycles, weights, (t, (t + phase_difference) % 4))
                for t in range(4)
            ],
            axis=0,
        )
        predicted = sum(
            probability[lag]
            * (
                lag_gradient(lag, phase_difference)
                - lag_gradient(-lag, phase_difference)
            )
            for lag in range(2)
        )
        np.testing.assert_allclose(averaged.sum(axis=0) / mass, predicted, atol=1e-15)
        if phase_difference == 0:
            np.testing.assert_allclose(predicted, 0, atol=1e-15)
            cloud = _cloud_interaction(r, cycles, [mass, mass], 1.0)
            assert np.linalg.norm(-mass * averaged[0] - cloud.force_on_first) > 1e-4
        else:
            assert np.linalg.norm(predicted) > 1e-3
            np.testing.assert_allclose(lag_gradient(1, 1), _g(r), atol=1e-15)
            np.testing.assert_allclose(
                lag_gradient(-1, 1),
                np.mean([_g(r + 2 * u) for u in cycle], axis=0),
                atol=1e-15,
            )
