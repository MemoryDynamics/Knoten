"""Synthetic one-step witnesses for the direct pair's physical claim limits."""

from __future__ import annotations

from dataclasses import replace

import numpy as np
import pytest

from emergenz_knoten import FiniteMemoryState, SimulationConfig
from emergenz_knoten.kernels import double_gaussian_gradient, exponential_memory_weights
from emergenz_knoten.reciprocal_nodes import reciprocal_pair_response
from emergenz_knoten.vector_memory import vector_gaussian_field


def _state(radius: float = 0.2, *, dim: int = 3) -> FiniteMemoryState:
    memory = np.zeros((5, dim))
    memory[1, 0], memory[2, 0] = -radius, radius
    memory[3, 1], memory[4, 1] = -radius, radius
    return FiniteMemoryState(
        x=np.zeros(dim),
        memory=memory,
        weights=np.array([0.4, 0.15, 0.15, 0.15, 0.15]),
    )


def _config(dim: int = 3) -> SimulationConfig:
    return SimulationConfig(
        steps=1,
        dim=dim,
        epsilon=0.0,
        eta=0.0,
        alpha=0.2,
        memory_mass=1.0,
        deposition_kernel="delta",
        deposition_sigma=0.0,
        sigma_rep=1.0,
        sigma_att=2.0,
        amplitude_rep=1.0,
        amplitude_att=3.0,
        memory_factor=1.0,
        max_memory=5,
        burn_in=0,
        sample_every=1,
    )


def _pair(first, second, config=None, second_config=None):
    separation = np.zeros(first.dim)
    separation[0] = 2.0
    return reciprocal_pair_response(
        first,
        second,
        _config(first.dim) if config is None else config,
        second_config=second_config,
        initial_center_separation=separation,
        first_noise=np.zeros((1, first.dim)),
        second_noise=np.zeros((1, first.dim)),
        sample_steps=[0, 1],
        cross_eta=0.02,
    )


def _cross_increments(response):
    return response.positions[1, 2] - response.positions[1, 0]


def _effective_terms(config):
    for amplitude, sigma in (
        (config.amplitude_rep, config.sigma_rep),
        (-config.amplitude_att, config.sigma_att),
    ):
        width2 = sigma**2 + config.deposition_sigma**2
        yield amplitude * (sigma**2 / width2) ** (config.dim / 2), width2


def _explicit_gradient(x, memory, weights, config):
    result = np.zeros(config.dim)
    for amplitude, width2 in _effective_terms(config):
        for point, weight in zip(memory, weights, strict=True):
            delta = x - point
            result -= (
                weight
                * amplitude
                / width2
                * np.exp(-np.dot(delta, delta) / (2 * width2))
                * delta
            )
    return result


@pytest.mark.parametrize("deposition_sigma", [0.0, 0.7])
def test_synchronous_cross_readout_matches_independent_one_step_sum(deposition_sigma):
    first, second = _state(), _state(0.8)
    config = replace(
        _config(),
        deposition_kernel="gaussian" if deposition_sigma else "delta",
        deposition_sigma=deposition_sigma,
    )
    response = _pair(first, second, config)
    shift = np.array([1.0, 0.0, 0.0])
    expected = -response.cross_eta * np.array(
        [
            _explicit_gradient(
                first.x - shift, second.memory + shift, second.weights, config
            ),
            _explicit_gradient(
                second.x + shift, first.memory - shift, first.weights, config
            ),
        ]
    )
    np.testing.assert_allclose(
        _cross_increments(response), expected, rtol=1e-12, atol=2e-16
    )


def test_equal_weight_mass_does_not_balance_arbitrary_history_readouts():
    first, second = _state(), _state(0.8)
    assert first.weights.sum() == second.weights.sum()
    response = _pair(first, second)
    increments = _cross_increments(response)
    assert np.linalg.norm(increments.sum(axis=0)) > 1e-5
    center_increments = response.memory_centers[1, 2] - response.memory_centers[1, 0]
    np.testing.assert_allclose(
        center_increments, first.weights[0] * increments, atol=1e-15
    )
    assert np.linalg.norm(center_increments.mean(axis=0)) > 1e-6

    # The counterexample also holds with the native exponential age law.
    weights = exponential_memory_weights(0.2, 5)
    native_states = []
    for state in (first, second):
        memory = state.memory.copy()
        memory[2] *= weights[1] / weights[2]
        memory[4] *= weights[3] / weights[4]
        native_states.append(FiniteMemoryState(state.x, memory, weights))
    native = _pair(*native_states)
    native_increments = _cross_increments(native)
    assert np.linalg.norm(native_increments.sum(axis=0)) > 1e-5
    np.testing.assert_allclose(
        native.memory_centers[1, 2] - native.memory_centers[1, 0],
        weights[0] / weights.sum() * native_increments,
        atol=1e-15,
    )


def test_mirror_symmetric_histories_retain_the_balanced_control():
    response = _pair(_state(), _state())
    increments = _cross_increments(response)
    assert np.linalg.norm(increments[0]) > 1e-4
    np.testing.assert_allclose(increments.sum(axis=0), 0.0, atol=1e-15)


def test_weight_mass_rescales_source_readout_not_receiver_inertia():
    first, second = _state(), _state()
    scaled = FiniteMemoryState(second.x, second.memory, 5.0 * second.weights)
    base = _pair(first, second)
    changed = _pair(first, scaled)
    expected = _cross_increments(base) * np.array([[5.0], [1.0]])
    np.testing.assert_allclose(
        _cross_increments(changed), expected, rtol=1e-12, atol=1e-15
    )
    np.testing.assert_allclose(
        changed.shape_tensors[0], base.shape_tensors[0], atol=1e-15
    )


def test_cross_deposition_uses_first_configuration_in_both_directions():
    delta = _config()
    gaussian = replace(delta, deposition_kernel="gaussian", deposition_sigma=0.7)
    base = _pair(_state(), _state(), delta, delta)
    changed_second = _pair(_state(), _state(), delta, gaussian)
    changed_first = _pair(_state(), _state(), gaussian, delta)
    np.testing.assert_array_equal(base.positions, changed_second.positions)
    assert (
        np.linalg.norm(_cross_increments(base) - _cross_increments(changed_first))
        > 1e-5
    )


def test_same_projected_histories_can_have_different_external_updates():
    first, second = _state(dim=4), _state(dim=4)
    lifted_memory = second.memory.copy()
    lifted_memory[:, 3] = [0.0, 1.0, -1.0, 2.0, -2.0]
    lifted = FiniteMemoryState(second.x, lifted_memory, second.weights)
    np.testing.assert_array_equal(second.memory[:, :3], lifted.memory[:, :3])
    np.testing.assert_allclose(
        np.average(lifted.memory, axis=0, weights=lifted.weights), 0.0
    )
    base = _pair(first, second)
    changed = _pair(first, lifted)
    np.testing.assert_array_equal(
        base.positions[0, ..., :3], changed.positions[0, ..., :3]
    )
    np.testing.assert_array_equal(base.memory_centers[0], changed.memory_centers[0])
    assert (
        np.linalg.norm(
            _cross_increments(base)[0, :3] - _cross_increments(changed)[0, :3]
        )
        > 1e-5
    )


@pytest.mark.parametrize("dim", [3, 4, 6])
@pytest.mark.parametrize("deposition_sigma", [0.0, 0.7])
def test_direct_scalar_readout_obeys_localized_gaussian_tail_bound(
    dim, deposition_sigma
):
    state = _state(0.8, dim=dim)
    memory = state.memory.copy()
    if dim > 3:
        memory[:, 3:] = np.arange(5)[:, None] / 3
    config = replace(
        _config(dim),
        deposition_kernel="gaussian" if deposition_sigma else "delta",
        deposition_sigma=deposition_sigma,
    )
    radius = np.linalg.norm(memory[:, :3], axis=1).max()
    mass = state.weights.sum()
    for distance in [2.0, 8.0, 20.0, 48.0]:
        x = np.zeros(dim)
        x[0] = distance
        gradient = double_gaussian_gradient(
            x,
            memory,
            state.weights,
            sigma_rep=config.sigma_rep,
            sigma_att=config.sigma_att,
            amplitude_rep=config.amplitude_rep,
            amplitude_att=config.amplitude_att,
            deposition_kernel=config.deposition_kernel,
            deposition_sigma=config.deposition_sigma,
        )
        bound = (
            mass
            * (distance + radius)
            * sum(
                abs(amplitude)
                / width2
                * np.exp(-((distance - radius) ** 2) / (2 * width2))
                for amplitude, width2 in _effective_terms(config)
            )
        )
        assert np.linalg.norm(gradient[:3]) <= bound * (1 + 1e-13)
    assert distance**2 * bound < 1e-80


@pytest.mark.parametrize("dim", [3, 4, 6])
def test_oriented_readout_has_a_gaussian_tail_with_bounded_current_mass(dim):
    state = _state(0.8, dim=dim)
    orientations = np.zeros_like(state.memory)
    orientations[:, 0] = [1.0, -1.0, 1.0, -1.0, 0.0]
    orientations[-1, 1] = 1.0
    if dim > 3:
        orientations[0, 0] = 0.0
        orientations[0, 3] = 1.0
    current_mass = np.dot(state.weights, np.linalg.norm(orientations, axis=1))
    radius = np.linalg.norm(state.memory[:, :3], axis=1).max()
    for distance in [2.0, 8.0, 20.0, 48.0]:
        x = np.zeros(dim)
        x[0] = distance
        field = vector_gaussian_field(
            x, state.memory, orientations, state.weights, sigma=2.0
        )
        bound = current_mass * np.exp(-((distance - radius) ** 2) / 8.0)
        assert np.linalg.norm(field[:3]) <= bound * (1 + 1e-13)
    assert distance**2 * bound < 1e-80
