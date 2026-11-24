"""Exact prepared six-write orbit and its transverse instability."""

from dataclasses import replace

import numpy as np
import pytest

from experiments.current.reference.fifo_carrier_clock_cycle import (
    clock_return,
    prepared_hexagon,
)
from experiments.current.reference.fifo_reversible_carrier import carrier_map


def _plane_weights(model):
    offset = model.profile_offset
    return np.array(
        [[0.25 + offset, 0.5, 0.25 - offset], [0.25 - offset, 0.5, 0.25 + offset]]
    )


def test_two_convex_profiles_give_the_exact_balance_frequencies():
    model, start = prepared_hexagon()
    weights = _plane_weights(model)
    np.testing.assert_allclose(weights.sum(axis=1), 1)
    assert np.all(weights > 0)
    assert np.linalg.matrix_rank(weights) == 2
    assert model.balance_frequencies == pytest.approx((12, 6), abs=2e-15)
    momentum = start.momentum
    np.testing.assert_allclose(momentum.sum(axis=0), 0, atol=8e-16)
    np.testing.assert_allclose(np.array([1, -1, 1]) @ momentum[1:-1], 0, atol=8e-16)


def test_six_autonomous_writes_preserve_true_past_samples_and_close():
    radius = 0.02
    model, start = prepared_hexagon(radius)
    state = start
    clock = start.clock_momentum
    angle = np.pi / 3
    direction = np.exp(1j * angle)
    previous_heads = [radius * direction**n for n in range(-3, 0)]
    for n in range(6):
        stored = np.array(previous_heads[-3:][::-1])
        np.testing.assert_allclose(
            state.position[1:-1], np.c_[stored.real, stored.imag], atol=2e-9, rtol=0
        )
        np.testing.assert_allclose(
            state.position[-1], state.position[-2], atol=2e-9, rtol=0
        )
        expected_head = radius * direction**n
        np.testing.assert_allclose(
            state.position[0],
            [expected_head.real, expected_head.imag],
            atol=2e-9,
            rtol=0,
        )
        previous_heads.append(complex(*state.position[0]))
        arrived, event, dt = clock_return(state, model)
        assert event.crossed
        assert event.energy_gap == pytest.approx(0, abs=2e-9)
        assert dt == pytest.approx(angle, abs=2e-9)
        assert arrived.clock_momentum == pytest.approx(clock, abs=2e-9)
        np.testing.assert_allclose(
            event.state.position[1], state.position[0], atol=2e-9
        )
        state = arrived
    np.testing.assert_allclose(state.position, start.position, atol=2e-9, rtol=0)
    np.testing.assert_allclose(state.momentum, start.momentum, atol=2e-9, rtol=0)


def test_each_prepared_phase_maps_to_the_next_at_larger_radius():
    model, start = prepared_hexagon(0.7)

    def phase(n):
        angle = n * np.pi / 3
        c, s = np.cos(angle), np.sin(angle)
        rotation = np.array([[c, -s], [s, c]])
        return replace(
            start,
            position=start.position @ rotation.T,
            momentum=start.momentum @ rotation.T,
        )

    for n in range(6):
        arrived, event, dt = clock_return(phase(n), model)
        expected = phase(n + 1)
        assert event.crossed
        assert event.energy_gap == pytest.approx(0, abs=2e-11)
        assert dt == pytest.approx(np.pi / 3, abs=2e-11)
        np.testing.assert_allclose(
            arrived.position, expected.position, atol=2e-10, rtol=0
        )
        np.testing.assert_allclose(
            arrived.momentum, expected.momentum, atol=2e-10, rtol=0
        )


def test_two_center_flight_is_reversible_and_conservative_away_from_the_hexagon():
    model, start = prepared_hexagon()
    q, p = start.position.copy(), start.momentum.copy()
    q[2] += [0.03, -0.11]
    p[1] += [-0.13, 0.06]
    moved_q, moved_p = model.flight(q, p, 0.31)
    restored_q, restored_p = model.flight(moved_q, moved_p, -0.31)
    np.testing.assert_allclose(restored_q, q, atol=3e-14, rtol=0)
    np.testing.assert_allclose(restored_p, p, atol=3e-14, rtol=0)
    assert model.internal_energy(moved_q, moved_p) == pytest.approx(
        model.internal_energy(q, p), rel=1e-13
    )
    np.testing.assert_allclose(moved_p.sum(axis=0), p.sum(axis=0), atol=1e-14)


def test_full_autonomous_transverse_jacobian_has_a_growing_copy_error():
    model, planar = prepared_hexagon()
    base_q = np.c_[planar.position, np.zeros(5)]
    base_p = np.c_[planar.momentum, np.zeros(5)]

    def observed(probe):
        q, p = base_q.copy(), base_p.copy()
        q[:, 2], p[:, 2] = probe.reshape(2, 5)
        result, event, _ = clock_return(replace(planar, position=q, momentum=p), model)
        assert event.crossed
        return np.r_[result.position[:, 2], result.momentum[:, 2]]

    eps = 1e-8
    basis = np.eye(10)
    difference = np.column_stack(
        [(observed(v * eps) - observed(-v * eps)) / (2 * eps) for v in basis]
    )
    q, p = carrier_map(basis[:5], basis[5:])
    matrix = np.concatenate(model.flight(q, p, np.pi / 3))
    np.testing.assert_allclose(difference, matrix, atol=1e-9, rtol=0)
    assert np.trace(matrix @ matrix) == pytest.approx(
        -164879 * np.pi / (5184 * np.sqrt(3)), abs=3e-11
    )
    values, vectors = np.linalg.eig(matrix)
    index = np.argmax(np.abs(values))
    assert abs(values[index]) > 2.4
    mode = vectors[:, index]
    assert abs(mode[4] - mode[3]) > 0.02
