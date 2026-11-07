"""Constructed one-step/Jacobian checks, not collective target simulations.

N>2 is a declared algebraic extension of the existing pair, not a new solver
or an adopted physical rule. No root search or archived target is executed.
"""

import numpy as np
import pytest

from emergenz_knoten import FiniteMemoryState, SimulationConfig
from emergenz_knoten.kernels import (
    double_gaussian_gradient,
    double_gaussian_hessian,
    exponential_memory_weights,
)
from emergenz_knoten.reciprocal_nodes import reciprocal_pair_response
from emergenz_knoten.state import memory_centroid, place_finite_memory_state


KERNEL = dict(sigma_rep=1.0, sigma_att=2.2, amplitude_rep=1.0, amplitude_att=4.2)
WEIGHTS = exponential_memory_weights(0.2, 4, memory_mass=1.0)


def _coupling(count, total=0.18):
    if count == 1:
        return np.array([[total]])
    return total * (
        0.6 * np.eye(count)
        + 0.4 / (count - 1) * (np.ones((count, count)) - np.eye(count))
    )


def _histories(count, dim=3):
    values = np.arange(count * 4 * dim).reshape(count, 4, dim)
    return 0.4 * np.sin(0.7 * values) + 0.2 * np.cos(0.3 * values)


def _step(histories, coupling):
    result = np.empty_like(histories)
    result[:, 1:] = histories[:, :-1]
    for i in range(len(histories)):
        result[i, 0] = histories[i, 0]
        for j in range(len(histories)):
            result[i, 0] -= coupling[i, j] * double_gaussian_gradient(
                histories[i, 0], histories[j], WEIGHTS, **KERNEL
            )
    return result


def _jacobian(histories, coupling):
    count, horizon, dim = histories.shape
    result = np.zeros((count, horizon, dim, count, horizon, dim))
    for i in range(count):
        result[i, 0, :, i, 0, :] = np.eye(dim)
        for age in range(1, horizon):
            result[i, age, :, i, age - 1, :] = np.eye(dim)
        for j in range(count):
            for age in range(horizon):
                curvature = coupling[i, j] * double_gaussian_hessian(
                    histories[i, 0],
                    histories[j, age : age + 1],
                    WEIGHTS[age : age + 1],
                    **KERNEL,
                )
                result[i, 0, :, i, 0, :] -= curvature
                result[i, 0, :, j, age, :] += curvature
    return result.reshape(histories.size, histories.size)


def _modal_block(history, row_gain, source_gain):
    horizon, dim = history.shape
    result = np.zeros((horizon * dim, horizon * dim))
    result[dim:, :-dim] = np.eye((horizon - 1) * dim)
    result[:dim, :dim] = np.eye(dim)
    for age in range(horizon):
        curvature = double_gaussian_hessian(
            history[0], history[age : age + 1], WEIGHTS[age : age + 1], **KERNEL
        )
        result[:dim, :dim] -= row_gain * curvature
        result[:dim, age * dim : (age + 1) * dim] += source_gain * curvature
    return result


@pytest.mark.parametrize("count", [1, 2, 3, 4])
def test_identical_histories_follow_single_rule_at_same_row_sum(count):
    single = _histories(1)
    copies = np.repeat(single, count, axis=0)
    expected = np.repeat(_step(single, np.array([[0.18]])), count, axis=0)
    np.testing.assert_allclose(_step(copies, _coupling(count)), expected, atol=2e-16)


@pytest.mark.parametrize("count", [1, 2, 3, 4])
def test_entire_common_history_jacobian_is_lifted_unchanged(count):
    single = _histories(1)
    copies = np.repeat(single, count, axis=0)
    embedding = np.kron(np.ones((count, 1)), np.eye(single.size))
    np.testing.assert_allclose(
        _jacobian(copies, _coupling(count)) @ embedding,
        embedding @ _jacobian(single, np.array([[0.18]])),
        atol=3e-16,
    )


@pytest.mark.parametrize("count", [2, 3, 4])
def test_adding_fixed_cross_gain_changes_common_rule(count):
    single = _histories(1)
    coupling = 0.07 * np.eye(count) + 0.04 * (np.ones((count, count)) - np.eye(count))
    expected = _step(single, np.array([[0.07 + (count - 1) * 0.04]]))
    actual = _step(np.repeat(single, count, axis=0), coupling)
    np.testing.assert_allclose(actual, np.repeat(expected, count, axis=0))
    assert np.linalg.norm(actual[0] - _step(single, np.array([[0.07]]))[0]) > 1e-5


def test_common_rule_requires_equal_row_sums():
    copies = np.repeat(_histories(1), 2, axis=0)
    result = _step(copies, np.array([[0.14, 0.04], [0.04, 0.18]]))
    assert np.linalg.norm(result[0, 0] - result[1, 0]) > 1e-5


@pytest.mark.parametrize("count", [2, 3, 4])
def test_relative_graph_modes_have_their_own_memory_feedback(count):
    history = _histories(1)[0]
    coupling = _coupling(count)
    values, vectors = np.linalg.eigh(coupling)
    full = _jacobian(np.repeat(history[None], count, axis=0), coupling)
    for value, vector in zip(values, vectors.T, strict=True):
        embedding = np.kron(vector[:, None], np.eye(history.size))
        np.testing.assert_allclose(
            full @ embedding,
            embedding @ _modal_block(history, 0.18, value),
            atol=3e-16,
        )


@pytest.mark.parametrize("count", [2, 3])
def test_full_noncoincident_jacobian_matches_one_step_finite_differences(count):
    histories = _histories(count)
    coupling = _coupling(count)
    step = 1e-6
    numerical = np.empty((histories.size, histories.size))
    for column in range(histories.size):
        direction = np.zeros_like(histories)
        direction.flat[column] = step
        numerical[:, column] = (
            _step(histories + direction, coupling)
            - _step(histories - direction, coupling)
        ).ravel() / (2 * step)
    np.testing.assert_allclose(_jacobian(histories, coupling), numerical, atol=8e-11)


@pytest.mark.parametrize("dim", [3, 4])
def test_backreaction_preserves_translation_but_frozen_sources_do_not(dim):
    histories = _histories(3, dim)
    coupling = _coupling(3)
    direction = np.arange(1, dim + 1, dtype=float)
    common_translation = np.broadcast_to(direction, histories.shape).ravel()
    np.testing.assert_allclose(
        _jacobian(histories, coupling) @ common_translation,
        common_translation,
        atol=2e-15,
    )
    frozen = np.eye(dim)
    for j in range(3):
        frozen -= coupling[0, j] * double_gaussian_hessian(
            histories[0, 0], histories[j], WEIGHTS, **KERNEL
        )
    assert np.linalg.norm(frozen @ direction - direction) > 1e-4


def test_declared_two_node_map_matches_existing_native_pair_one_step():
    histories = _histories(2)
    states = [FiniteMemoryState(row[0], row, WEIGHTS) for row in histories]
    midpoint = sum(memory_centroid(state) for state in states) / 2
    separation = np.array([0.6, -0.2, 0.1])
    placed = [
        place_finite_memory_state(state, midpoint + sign * separation / 2)
        for state, sign in zip(states, [-1, 1], strict=True)
    ]
    config = SimulationConfig(
        steps=1,
        dim=3,
        epsilon=0.0,
        eta=0.07,
        alpha=0.2,
        memory_mass=1.0,
        max_memory=4,
        burn_in=0,
        sample_every=1,
        **KERNEL,
    )
    response = reciprocal_pair_response(
        *states,
        config,
        initial_center_separation=separation,
        first_noise=np.zeros((1, 3)),
        second_noise=np.zeros((1, 3)),
        sample_steps=[0, 1],
        cross_eta=0.04,
    )
    expected = _step(
        np.stack([state.memory for state in placed]),
        np.array([[0.07, 0.04], [0.04, 0.07]]),
    )
    np.testing.assert_allclose(response.positions[1, 2], expected[:, 0], atol=2e-16)


def _polygon(count, radius=0.7, angle=0.3):
    phases = 2 * np.pi * np.arange(count) / count
    angles = phases[:, None] - angle * np.arange(4)
    histories = np.zeros((count, 4, 3))
    histories[:, :, 0] = radius * np.cos(angles)
    histories[:, :, 1] = radius * np.sin(angles)
    return histories


def _polygon_normal_coefficients(count, coupling, radius=0.7, angle=0.3):
    coefficients = np.empty((4, count, count))
    for age in range(4):
        phase = (
            age * angle
            + 2
            * np.pi
            * (np.arange(count)[:, None] - np.arange(count)[None, :])
            / count
        )
        distance_squared = 2 * radius**2 * (1 - np.cos(phase))
        factor = -KERNEL["amplitude_rep"] / KERNEL["sigma_rep"] ** 2 * np.exp(
            -distance_squared / (2 * KERNEL["sigma_rep"] ** 2)
        ) + KERNEL["amplitude_att"] / KERNEL["sigma_att"] ** 2 * np.exp(
            -distance_squared / (2 * KERNEL["sigma_att"] ** 2)
        )
        coefficients[age] = coupling * WEIGHTS[age] * factor
    return coefficients


@pytest.mark.parametrize("count", [1, 2, 3, 4])
def test_polygon_existence_residual_matches_actual_one_step(count):
    radius, angle = 0.7, 0.3
    histories = _polygon(count, radius, angle)
    coupling = _coupling(count)
    coefficients = _polygon_normal_coefficients(count, coupling, radius, angle)
    phases = 2 * np.pi * np.arange(count) / count
    relative_angles = (
        np.arange(4)[:, None, None] * angle
        + phases[None, :, None]
        - phases[None, None, :]
    )
    residual = np.expm1(1j * angle) + (
        coefficients * (1 - np.exp(-1j * relative_angles))
    ).sum(axis=(0, 2))
    moved = _step(histories, coupling)[:, 0]
    actual_complex = moved[:, 0] + 1j * moved[:, 1]
    target = radius * np.exp(1j * (phases + angle))
    np.testing.assert_allclose(
        actual_complex - target,
        -radius * np.exp(1j * phases) * residual,
        atol=3e-16,
    )


@pytest.mark.parametrize("count", [2, 3, 4])
def test_phase_polygon_normal_blocks_match_full_jacobian(count):
    histories = _polygon(count)
    coupling = _coupling(count)
    full = _jacobian(histories, coupling)
    indices = np.arange(histories.size).reshape(histories.shape)[:, :, 2].ravel()
    normal = full[np.ix_(indices, indices)]
    coefficients = _polygon_normal_coefficients(count, coupling)
    row_sums = coefficients.sum(axis=2)
    np.testing.assert_allclose(row_sums, np.repeat(row_sums[:, :1], count, axis=1))
    for mode in range(count):
        vector = np.exp(2j * np.pi * mode * np.arange(count) / count)
        eigenvalues = coefficients[:, 0, :] @ vector
        block = np.zeros((4, 4), dtype=complex)
        block[0] = eigenvalues
        block[0, 0] += 1 - row_sums[:, 0].sum()
        block[1:, :-1] = np.eye(3)
        embedding = np.kron(vector[:, None], np.eye(4))
        np.testing.assert_allclose(normal @ embedding, embedding @ block, atol=3e-16)
    # Prepared points test a derivative identity, not existence of an orbit.
    rotated = _polygon(count, angle=0.3)
    rotation = np.array([[np.cos(0.3), -np.sin(0.3)], [np.sin(0.3), np.cos(0.3)]])
    expected = rotated[:, 0, :2] @ rotation.T
    assert np.linalg.norm(_step(histories, coupling)[:, 0, :2] - expected) > 0.01


def test_phase_offsets_change_common_feedback_even_at_fixed_row_sum():
    coupling = _coupling(3)
    actual = _polygon_normal_coefficients(3, coupling).sum(axis=2)[:, 0]
    one = _polygon_normal_coefficients(1, np.array([[0.18]]))[:, 0, 0]
    assert np.linalg.norm(actual[1:] - one[1:]) > 1e-3


def _normal_companion(coefficients):
    result = np.zeros((len(coefficients) + 1, len(coefficients) + 1))
    result[0, 0] = 1 - sum(coefficients)
    result[0, 1:] = coefficients
    result[1:, :-1] = np.eye(len(coefficients))
    return result


def test_negative_slope_has_growing_mode_in_constructed_polynomial():
    coefficients = np.array([-1.2, 0.0])
    slope = 1 + np.arange(1, 3) @ coefficients
    assert slope < 0
    np.testing.assert_allclose(
        np.sort(np.linalg.eigvals(_normal_companion(coefficients))),
        [0, 1, 1.2],
        atol=2e-15,
    )


def test_nonnegative_slope_does_not_certify_normal_stability():
    coefficients = np.array([0.0, 2.0])
    assert 1 + np.arange(1, 3) @ coefficients > 0
    roots = np.linalg.eigvals(_normal_companion(coefficients))
    np.testing.assert_allclose(np.sort(np.abs(roots)), [1, np.sqrt(2), np.sqrt(2)])
