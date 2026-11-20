"""Exact read/write bookkeeping, not a physical heat or work assignment.

Only constructed H=2/H=5 states and at most seven native updates are used.
"""

from dataclasses import replace

import numpy as np
import pytest
from scipy.integrate import quad

from emergenz_knoten import FiniteMemoryState, SimulationConfig
from emergenz_knoten.kernels import (
    double_gaussian_gradient,
    double_gaussian_potential,
    effective_double_gaussian_parameters,
    exponential_memory_weights,
)
from emergenz_knoten.reciprocal_nodes import reciprocal_pair_response
from emergenz_knoten.state import memory_centroid, place_finite_memory_state


def _config(dim=3, horizon=5, steps=7, **kwargs):
    config = SimulationConfig(
        steps=steps,
        dim=dim,
        epsilon=0.03,
        eta=0.07,
        alpha=0.2,
        memory_mass=1.0,
        deposition_kernel="delta",
        deposition_sigma=0.0,
        sigma_rep=1.0,
        sigma_att=2.0,
        amplitude_rep=1.0,
        amplitude_att=3.0,
        memory_factor=1.0,
        max_memory=horizon,
        burn_in=0,
        sample_every=1,
    )
    return replace(config, **kwargs)


def _parameters(config):
    return effective_double_gaussian_parameters(
        dim=config.dim,
        sigma_rep=config.sigma_rep,
        sigma_att=config.sigma_att,
        amplitude_rep=config.amplitude_rep,
        amplitude_att=config.amplitude_att,
        deposition_kernel=config.deposition_kernel,
        deposition_sigma=config.deposition_sigma,
    )


def _response(configs, memories, cross_eta):
    states = [
        FiniteMemoryState(
            memory[0],
            memory,
            exponential_memory_weights(
                config.alpha,
                len(memory),
                memory_mass=config.memory_mass,
            ),
        )
        for config, memory in zip(configs, memories, strict=True)
    ]
    midpoint = 0.5 * sum(memory_centroid(state) for state in states)
    separation = np.zeros(configs[0].dim)
    separation[0] = 0.4
    placed = [
        place_finite_memory_state(state, midpoint + sign * separation / 2)
        for state, sign in zip(states, [-1, 1], strict=True)
    ]
    shape = (configs[0].steps, configs[0].dim)
    result = reciprocal_pair_response(
        *states,
        configs[0],
        second_config=configs[1],
        cross_eta=cross_eta,
        initial_center_separation=separation,
        first_noise=np.sin(np.arange(np.prod(shape)).reshape(shape)),
        second_noise=np.cos(np.arange(np.prod(shape)).reshape(shape)),
        sample_steps=range(configs[0].steps + 1),
    )
    return placed, result.positions[:, 2]


@pytest.mark.parametrize("dim,deposition_sigma", [(3, 0.0), (4, 0.4)])
def test_native_pair_read_write_energy_split_and_exact_frozen_line_work(
    dim, deposition_sigma
):
    first = _config(
        dim,
        deposition_kernel="gaussian" if deposition_sigma else "delta",
        deposition_sigma=deposition_sigma,
    )
    configs = [
        first,
        replace(
            first,
            alpha=0.35,
            memory_mass=1.7,
            eta=0.11,
            epsilon=0.04,
            amplitude_att=7.0,
            sigma_att=2.2,
        ),
    ]
    memories = [
        scale * np.sin(np.arange(5 * dim).reshape(5, dim) + phase)
        for scale, phase in [(0.13, 0.0), (0.21, 0.4)]
    ]
    cross_eta = 0.09
    placed, positions = _response(configs, memories, cross_eta)
    histories = [state.memory.copy() for state in placed]
    weights = [state.weights for state in placed]
    parameters = [_parameters(config) for config in configs]
    coefficients = np.array([[configs[0].eta, cross_eta], [cross_eta, configs[1].eta]])
    mobility = np.array([0.7, 1.4])
    accumulated = np.zeros(2)
    starting_energy = final_energy = 0.0

    def channel(i, j, x, history):
        params = parameters[i] if i == j else parameters[0]
        return double_gaussian_potential(x, history, weights[j], **params)

    for n in range(7):
        advanced = [np.vstack([positions[n + 1, j], histories[j][:-1]]) for j in (0, 1)]
        before = frozen = after = memory_formula = integrated_work = 0.0
        for i in (0, 1):
            displacement = positions[n + 1, i] - positions[n, i]
            native_drift = np.zeros(dim)
            for j in (0, 1):
                coefficient = coefficients[i, j] / mobility[i]
                old = channel(i, j, positions[n, i], histories[j])
                held = channel(i, j, positions[n + 1, i], histories[j])
                new = channel(i, j, positions[n + 1, i], advanced[j])
                params = parameters[i] if i == j else parameters[0]
                native_drift -= coefficients[i, j] * double_gaussian_gradient(
                    positions[n, i], histories[j], weights[j], **params
                )

                def kernel(point):
                    return double_gaussian_potential(
                        positions[n + 1, i], point[None, :], [1.0], **params
                    )

                q = 1 - configs[j].alpha
                write = weights[j][0] * kernel(positions[n + 1, j])
                drop = weights[j][0] * q**5 * kernel(histories[j][-1])
                delta = -configs[j].alpha * held + write - drop
                assert new - held == pytest.approx(delta, abs=2e-15)
                before += coefficient * old
                frozen += coefficient * held
                after += coefficient * new
                memory_formula += coefficient * delta

                def integrand(theta):
                    gradient = double_gaussian_gradient(
                        positions[n, i] + theta * displacement,
                        histories[j],
                        weights[j],
                        **params,
                    )
                    return -coefficient * np.dot(gradient, displacement)

                integrated_work += quad(integrand, 0, 1, epsabs=1e-12, epsrel=1e-12)[0]
            phase = np.arange(n * dim, (n + 1) * dim)
            noise = configs[i].epsilon * (np.sin(phase) if i == 0 else np.cos(phase))
            np.testing.assert_allclose(displacement, native_drift + noise, atol=2e-15)
        np.testing.assert_allclose(
            after - before, frozen - before + memory_formula, atol=3e-15
        )
        np.testing.assert_allclose(integrated_work, before - frozen, atol=3e-15)
        if n == 0:
            starting_energy = before
        accumulated += [frozen - before, memory_formula]
        final_energy = after
        histories = advanced
    assert accumulated.sum() == pytest.approx(final_energy - starting_energy, abs=5e-15)
    assert abs(accumulated[1]) > 1e-6


def test_stationary_point_can_gain_read_potential_only_through_fifo_update():
    config = _config(
        horizon=2, steps=1, alpha=0.5, eta=0.01, epsilon=0.0, amplitude_att=2.0
    )
    distance = np.sqrt(8 * np.log(2) / 3)
    memory = np.array([[0.0, 0.0, 0.0], [distance, 0.0, 0.0]])
    placed, positions = _response([config, config], [memory, memory], 0.0)
    state = placed[0]
    np.testing.assert_allclose(positions[1, 0], positions[0, 0], rtol=0, atol=1e-16)
    parameters = _parameters(config)

    def read(x, history):
        return config.eta * double_gaussian_potential(
            x, history, state.weights, **parameters
        )

    before = read(positions[0, 0], state.memory)
    frozen = read(positions[1, 0], state.memory)
    after = read(positions[1, 0], np.vstack([positions[1, 0], state.memory[:-1]]))
    assert frozen == pytest.approx(before, abs=1e-17)
    assert after - before == pytest.approx(
        config.eta / 4 * (3 * 2 ** (-4 / 3) - 1), abs=1e-17
    )
    assert after > before


def test_fifo_change_can_also_decrease_read_potential_with_attraction_only():
    config = _config(
        horizon=2,
        steps=1,
        alpha=0.5,
        eta=0.01,
        epsilon=0.0,
        amplitude_rep=0.0,
        amplitude_att=1.0,
        sigma_att=1.0,
    )
    memory = np.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]])
    placed, positions = _response([config, config], [memory, memory], 0.0)
    state = placed[0]
    parameters = _parameters(config)
    frozen = double_gaussian_potential(
        positions[1, 0], state.memory, state.weights, **parameters
    )
    advanced = np.vstack([positions[1, 0], state.memory[:-1]])
    after = double_gaussian_potential(
        positions[1, 0], advanced, state.weights, **parameters
    )
    assert after < frozen


def test_prepoint_force_times_displacement_is_not_exact_frozen_work():
    parameters = dict(
        sigma_rep=1.0, sigma_att=2.0, amplitude_rep=1.0, amplitude_att=0.0
    )
    memory, weights = np.zeros((1, 3)), np.ones(1)
    start, end = np.array([0.4, 0.0, 0.0]), np.array([0.8, 0.0, 0.0])
    exact = double_gaussian_potential(start, memory, weights, **parameters)
    exact -= double_gaussian_potential(end, memory, weights, **parameters)
    prepoint = -np.dot(
        double_gaussian_gradient(start, memory, weights, **parameters), end - start
    )
    assert abs(prepoint - exact) > 0.01


@pytest.mark.parametrize("scale", [0.2, 7.0])
def test_declared_energy_and_mobility_scaling_leaves_native_increment_unchanged(scale):
    drift = np.array([0.3, -0.7])
    mobility = np.array([0.4, 1.2])
    force = drift / mobility
    changed_mobility = mobility / scale
    changed_force = scale * force
    np.testing.assert_allclose(changed_mobility * changed_force, drift)
    # This is an identifiability/unit freedom, not a proof that all energy notions fail.


def test_one_way_memory_readout_is_not_a_diagonal_gradient_flow_in_full_state():
    q = np.array(
        [[-1.2, 0.2, 0, 1], [1, -1, 0, 0], [0, 0.4, -1.1, 0.7], [0, 0, 2, -2]],
        dtype=float,
    )
    # Q[xA,cB] != 0 but Q[cB,xA] = 0: no positive diagonal scaling can symmetrize it.
    assert q[0, 3] > 0 and q[3, 0] == 0
    diagonal_mobility = np.array([0.3, 0.7, 2.0, 1.2])
    hessian_candidate = -q / diagonal_mobility[:, None]
    assert hessian_candidate[0, 3] != hessian_candidate[3, 0]
