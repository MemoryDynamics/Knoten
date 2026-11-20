"""Synthetic identities for the native pair and its conditional local closure.

No archived target, parameter search, or proposed physical force is simulated.
The longest native continuation is seven updates of two constructed H=5 states.
"""

from dataclasses import replace

import numpy as np
import pytest
from scipy.linalg import expm

from emergenz_knoten import FiniteMemoryState, SimulationConfig
from emergenz_knoten.kernels import (
    double_gaussian_gradient,
    effective_double_gaussian_parameters,
    exponential_memory_weights,
    two_scale_local_curvature,
)
from emergenz_knoten.reciprocal_nodes import reciprocal_pair_response
from emergenz_knoten.state import memory_centroid, place_finite_memory_state


def _config(dim, deposition_sigma):
    return SimulationConfig(
        steps=7,
        dim=dim,
        epsilon=0.03,
        eta=0.07,
        alpha=0.2,
        memory_mass=1.0,
        deposition_kernel="gaussian" if deposition_sigma else "delta",
        deposition_sigma=deposition_sigma,
        sigma_rep=1.0,
        sigma_att=2.0,
        amplitude_rep=1.0,
        amplitude_att=3.0,
        memory_factor=1.0,
        max_memory=5,
        burn_in=0,
        sample_every=1,
    )


def _state(config, radius):
    memory = np.zeros((5, config.dim))
    memory[:, :3] = radius * np.array(
        [[0, 0, 0], [1, 0, 0], [-1, 0.5, 0], [0, -1, 0.5], [0.3, 0.2, -0.4]]
    )
    if config.dim > 3:
        memory[:, 3] = radius * np.array([0, 0.3, -0.1, 0.8, -0.2])
    weights = exponential_memory_weights(
        config.alpha, 5, memory_mass=config.memory_mass
    )
    memory -= np.average(memory, weights=weights, axis=0)
    return FiniteMemoryState(memory[0], memory, weights)


def _effective(config):
    return effective_double_gaussian_parameters(
        dim=config.dim,
        sigma_rep=config.sigma_rep,
        sigma_att=config.sigma_att,
        amplitude_rep=config.amplitude_rep,
        amplitude_att=config.amplitude_att,
        deposition_kernel=config.deposition_kernel,
        deposition_sigma=config.deposition_sigma,
    )


def _gradient_and_bound(x, memory, weights, parameters):
    gradient = double_gaussian_gradient(x, memory, weights, **parameters)
    curvature = two_scale_local_curvature(**parameters)
    center = np.average(memory, weights=weights, axis=0)
    linear = curvature * weights.sum() * (x - center)
    coefficient = abs(parameters["amplitude_rep"]) / (
        2 * parameters["sigma_rep"] ** 4
    ) + abs(parameters["amplitude_att"]) / (2 * parameters["sigma_att"] ** 4)
    bound = coefficient * np.dot(weights, np.linalg.norm(x - memory, axis=1) ** 3)
    return gradient, linear, bound


@pytest.mark.parametrize("dim,deposition_sigma", [(3, 0.0), (4, 0.4)])
def test_exact_center_recurrence_retains_tail_and_nonlinearity_in_native_pair(
    dim,
    deposition_sigma,
):
    first = _config(dim, deposition_sigma)
    second = replace(
        first,
        alpha=0.35,
        memory_mass=1.7,
        eta=0.11,
        epsilon=0.04,
        amplitude_att=7.0,
        sigma_att=2.2,
    )
    configs = [first, second]
    initial = [_state(first, 0.13), _state(second, 0.21)]
    separation = np.zeros(dim)
    separation[0] = 0.4
    midpoint = 0.5 * sum(memory_centroid(s) for s in initial)
    placed = [
        place_finite_memory_state(s, midpoint + sign * separation / 2)
        for s, sign in zip(initial, [-1, 1], strict=True)
    ]
    noise = [np.sin(np.arange(7 * dim).reshape(7, dim) + phase) for phase in (0.0, 0.7)]
    cross_eta = 0.09
    result = reciprocal_pair_response(
        *initial,
        first,
        second_config=second,
        initial_center_separation=separation,
        first_noise=noise[0],
        second_noise=noise[1],
        sample_steps=range(8),
        cross_eta=cross_eta,
    )
    positions = result.positions[:, 2]
    centers = result.memory_centers[:, 2]
    histories = [s.memory.copy() for s in placed]
    effective = [_effective(c) for c in configs]
    weights = [s.weights for s in placed]
    q = 1 - np.array([c.alpha for c in configs])
    alpha = 1 - q
    beta = alpha / (1 - q**5)
    g = np.array(
        [
            c.eta * weights[i].sum() * two_scale_local_curvature(**effective[i])
            for i, c in enumerate(configs)
        ]
    )
    h = (
        cross_eta
        * two_scale_local_curvature(**effective[0])
        * np.array([weights[1].sum(), weights[0].sum()])
    )
    s = 1 - g - h
    tails = np.zeros((8, 2, dim))
    remainders = np.zeros((7, 2, dim))
    for n in range(7):
        for i in (0, 1):
            k = 1 - i
            self_gradient, self_linear, self_bound = _gradient_and_bound(
                positions[n, i], histories[i], weights[i], effective[i]
            )
            cross_gradient, cross_linear, cross_bound = _gradient_and_bound(
                positions[n, i], histories[k], weights[k], effective[0]
            )
            remainder = -configs[i].eta * (self_gradient - self_linear)
            remainder -= cross_eta * (cross_gradient - cross_linear)
            remainders[n, i] = remainder
            assert np.linalg.norm(remainder) <= (
                configs[i].eta * self_bound + cross_eta * cross_bound + 1e-15
            )
            drive = configs[i].epsilon * noise[i][n]
            np.testing.assert_allclose(
                positions[n + 1, i],
                s[i] * positions[n, i]
                + g[i] * centers[n, i]
                + h[i] * centers[n, k]
                + drive
                + remainder,
                atol=2e-15,
            )
            tails[n + 1, i] = (
                beta[i] * q[i] ** 5 * (positions[n + 1, i] - histories[i][-1])
            )
            np.testing.assert_allclose(
                centers[n + 1, i],
                q[i] * centers[n, i] + alpha[i] * positions[n + 1, i] + tails[n + 1, i],
                atol=2e-15,
            )
            if n > 0:
                without_rest = (
                    q[i] * s[i] * (centers[n, i] - centers[n - 1, i])
                    - alpha[i] * h[i] * (centers[n, i] - centers[n, k])
                    + alpha[i] * drive
                )
                tail_difference = tails[n + 1, i] - s[i] * tails[n, i]
                np.testing.assert_allclose(
                    centers[n + 1, i] - centers[n, i],
                    without_rest + alpha[i] * remainder + tail_difference,
                    atol=2e-15,
                )
        # Both cross readouts must see the old pair before either FIFO is shifted.
        histories = [
            np.vstack([positions[n + 1, i], histories[i][:-1]]) for i in (0, 1)
        ]
    assert np.linalg.norm(tails[2:] - s[None, :, None] * tails[1:-1]) > 1e-5
    assert np.linalg.norm(alpha[None, :, None] * remainders[1:]) > 1e-6


@pytest.mark.parametrize("alpha,horizon", [(1.0, 5), (0.2, 1), (0.2, 5)])
def test_geometric_fifo_center_identity_including_endpoint_cases(alpha, horizon):
    q = 1 - alpha
    beta = alpha / (1 - q**horizon)
    weights = exponential_memory_weights(alpha, horizon)
    history = np.arange(horizon * 2).reshape(horizon, 2) / 5
    new_x = np.array([1.7, -0.4])
    old_center = np.average(history, weights=weights, axis=0)
    actual = np.average(np.vstack([new_x, history[:-1]]), weights=weights, axis=0)
    tail = beta * q**horizon * (new_x - history[-1])
    np.testing.assert_allclose(
        actual, q * old_center + alpha * new_x + tail, atol=1e-15
    )


@pytest.mark.parametrize("dim,deposition_sigma", [(3, 0.0), (4, 0.4)])
def test_gaussian_gradient_has_explicit_cubic_remainder_bound(dim, deposition_sigma):
    config = _config(dim, deposition_sigma)
    state = _state(config, 0.8)
    for scale in (1.0, 0.1, 0.01):
        x = scale * np.linspace(-0.4, 0.7, dim)
        gradient, linear, bound = _gradient_and_bound(
            x, scale * state.memory, state.weights, _effective(config)
        )
        assert np.linalg.norm(gradient - linear) <= bound + 1e-15


def _continuous_matrix(a, b, tau):
    return np.array(
        [
            [-(a[0] + b[0]), a[0], 0, b[0]],
            [1 / tau[0], -1 / tau[0], 0, 0],
            [0, b[1], -(a[1] + b[1]), a[1]],
            [0, 0, 1 / tau[1], -1 / tau[1]],
        ]
    )


def test_heterogeneous_continuous_elimination_is_a_similarity_not_new_dynamics():
    a, b, tau = np.array([0.2, 0.7]), np.array([0.9, 0.4]), np.array([0.6, 1.3])
    q = _continuous_matrix(a, b, tau)
    # z=(xA,cA,xB,cB) -> (cA,vA,cB,vB), where v=(x-c)/tau.
    transform = np.array(
        [
            [0, 1, 0, 0],
            [1 / tau[0], -1 / tau[0], 0, 0],
            [0, 0, 0, 1],
            [0, 0, 1 / tau[1], -1 / tau[1]],
        ]
    )
    expected = np.array(
        [
            [0, 1, 0, 0],
            [-b[0] / tau[0], -1 / tau[0] - a[0] - b[0], b[0] / tau[0], 0],
            [0, 0, 0, 1],
            [b[1] / tau[1], 0, -b[1] / tau[1], -1 / tau[1] - a[1] - b[1]],
        ]
    )
    np.testing.assert_allclose(
        transform @ q @ np.linalg.inv(transform), expected, atol=1e-15
    )
    mobility = np.array([0.4, 0.9])
    input_map = np.array([[mobility[0], 0], [0, 0], [0, mobility[1]], [0, 0]])
    np.testing.assert_allclose(
        transform @ input_map,
        [[0, 0], [mobility[0] / tau[0], 0], [0, 0], [0, mobility[1] / tau[1]]],
    )


def test_reciprocal_energy_requires_the_declared_mobility_condition():
    weights = np.array([2.0, 5.0])
    b = 0.3 * weights[::-1]
    tau, a = np.array([0.7, 1.2]), np.array([0.4, 0.2])
    center, velocity, force = (
        np.array([0.8, -0.3]),
        np.array([0.4, -0.7]),
        np.array([0.2, 0.6]),
    )
    mobility = 1 / weights
    stiffness = b / mobility
    assert stiffness[0] == pytest.approx(stiffness[1])
    mass = tau / mobility
    assert mass[0] / mass[1] == pytest.approx(
        tau[0] * weights[0] / (tau[1] * weights[1])
    )
    friction = (1 + tau * (a + b)) / mobility
    acceleration = (
        mobility * force - (1 + tau * (a + b)) * velocity - b * (center - center[::-1])
    ) / tau
    energy_rate = np.dot(mass * velocity, acceleration)
    energy_rate += stiffness[0] * (center[0] - center[1]) * (velocity[0] - velocity[1])
    np.testing.assert_allclose(
        energy_rate, np.dot(force, velocity) - np.dot(friction, velocity**2)
    )
    # Equal mobilities do not give a common reciprocal potential for unequal weights.
    assert not np.isclose(b[0], b[1])
    # Declaring a different actuator scale changes inferred mass, not free poles.
    np.testing.assert_allclose(tau / (3 * mobility), mass / 3)


@pytest.mark.parametrize(
    "a,b,tau",
    [
        ([0, 0], [1, 1], [1, 1]),
        ([0.2, 0.7], [0.9, 0.4], [0.6, 1.3]),
        ([3, 0.01], [0.4, 2], [4, 0.3]),
    ],
)
def test_attractive_four_state_generator_has_the_laplacian_sector(a, b, tau):
    q = _continuous_matrix(a, b, tau)
    np.testing.assert_allclose(q.sum(axis=1), 0, atol=1e-15)
    assert np.all(q - np.diag(np.diag(q)) >= 0)
    eigenvalues = np.linalg.eigvals(q)
    assert np.count_nonzero(abs(eigenvalues) < 1e-12) == 1
    nonzero = eigenvalues[abs(eigenvalues) >= 1e-12]
    assert np.all(nonzero.real < 0)
    assert np.all(abs(nonzero.imag) <= -nonzero.real + 1e-12)


def test_directed_four_cycle_saturates_one_period_modal_attenuation_bound():
    q = _continuous_matrix([0, 0], [1, 1], [1, 1])
    eigenvalues, eigenvectors = np.linalg.eig(q)
    index = np.argmax(eigenvalues.imag)
    assert eigenvalues[index] == pytest.approx(-1 + 1j)
    mode = eigenvectors[:, index]
    np.testing.assert_allclose(
        expm(2 * np.pi * q) @ mode, np.exp(-2 * np.pi) * mode, atol=1e-15
    )


def test_negative_self_curvature_is_outside_the_sector_claim():
    q = _continuous_matrix([-1, -1], [1, 1], [1, 1])
    eigenvalues = np.linalg.eigvals(q)
    assert np.any(abs(eigenvalues.imag) > -eigenvalues.real + 1e-8)
    assert np.any(q - np.diag(np.diag(q)) < 0)
