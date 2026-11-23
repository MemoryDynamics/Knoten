"""Fixed canonical, translation and energy checks for one FIFO write event."""

from dataclasses import replace

import numpy as np
import pytest

from emergenz_knoten.kernels import exponential_memory_weights, gaussian_potential
from experiments.current.reference.fifo_reversible_carrier import (
    BoundaryState,
    carrier_map,
    write_boundary,
)


def _register_energy(q, p):
    memory = q[1:-1]
    weights = exponential_memory_weights(0.5, len(memory))
    return np.sum(p**2) / 2 + gaussian_potential(q[0], memory, weights, sigma=1.0)


def _total_energy(state, clock_mass):
    return _register_energy(state.position, state.momentum) + (
        state.clock_momentum**2 / (2 * clock_mass)
    )


@pytest.mark.parametrize("horizon", [1, 2, 4])
def test_carrier_map_is_an_exact_inverse_and_cotangent_lift(horizon):
    size = horizon + 2
    z = np.zeros((size, 1))
    position_matrix, momentum_matrix = [], []
    for e in np.eye(size):
        q, p = carrier_map(e[:, None], e[:, None])
        position_matrix.append(q[:, 0])
        momentum_matrix.append(p[:, 0])
        q0, p0 = carrier_map(q, p, reverse=True)
        np.testing.assert_array_equal(q0[:, 0], e)
        np.testing.assert_array_equal(p0[:, 0], e)
    c, d = np.array(position_matrix).T, np.array(momentum_matrix).T
    np.testing.assert_array_equal(c.T @ d, np.eye(size))
    np.testing.assert_array_equal(c @ np.ones(size), np.ones(size))
    np.testing.assert_array_equal(np.ones(size) @ d, np.ones(size))
    np.testing.assert_array_equal(carrier_map(z, z), (z, z))


def test_exact_copy_requires_preparation_and_stores_the_old_tail():
    q = np.array([[3, 1], [1, 2], [2, -1], [-1, 5], [-1, 5]], dtype=float)
    p = np.array([[7, 1], [0, 2], [1, 0], [2, 1], [-2, -3]], dtype=float)
    out_q, out_p = carrier_map(q, p)
    np.testing.assert_array_equal(out_q[1:-1], q[:-2])
    np.testing.assert_array_equal(out_q[-1], q[-2])
    np.testing.assert_array_equal(out_p[0] - p[0], -p[-1])
    np.testing.assert_array_equal(out_p.sum(axis=0), p.sum(axis=0))

    again_q, _ = carrier_map(out_q, out_p)
    np.testing.assert_array_equal(again_q[1] - again_q[0], out_q[-1] - out_q[-2])
    assert np.any(again_q[1] != again_q[0])
    translation = np.array([10, 20])
    shifted_q, shifted_p = carrier_map(q + translation, p)
    np.testing.assert_array_equal(shifted_q, out_q + translation)
    np.testing.assert_array_equal(shifted_p, out_p)


def _incoming(clock):
    q = np.array([[0.0], [1.0], [2.0], [2.0]])
    p = np.array([[0.0], [0.1], [0.3], [0.2]])
    return BoundaryState(q, p, clock)


def test_clock_can_pay_write_work_and_reversed_crossing_restores_input():
    clock_mass = 1.7
    incoming = _incoming(2.0)
    event = write_boundary(incoming, _register_energy, clock_mass=clock_mass)
    result = event.state
    assert event.crossed and event.energy_gap > 0
    assert result.side == 1 and 0 < result.clock_momentum < incoming.clock_momentum
    assert _total_energy(result, clock_mass) == pytest.approx(
        _total_energy(incoming, clock_mass), abs=5e-16
    )
    reversed_result = replace(
        result, momentum=-result.momentum, clock_momentum=-result.clock_momentum
    )
    returning = write_boundary(reversed_result, _register_energy, clock_mass=clock_mass)
    assert returning.crossed and returning.state.side == -1
    assert returning.energy_gap == pytest.approx(-event.energy_gap, abs=5e-16)
    np.testing.assert_allclose(returning.state.position, incoming.position, atol=5e-16)
    np.testing.assert_allclose(returning.state.momentum, -incoming.momentum, atol=5e-16)
    assert returning.state.clock_momentum == pytest.approx(-incoming.clock_momentum)


def test_insufficient_clock_energy_reflects_without_overwriting():
    incoming = _incoming(0.02)
    event = write_boundary(incoming, _register_energy)
    assert not event.crossed and event.energy_gap > 0
    assert event.state.side == incoming.side
    assert event.state.clock_momentum == -incoming.clock_momentum
    np.testing.assert_array_equal(event.state.position, incoming.position)
    np.testing.assert_array_equal(event.state.momentum, incoming.momentum)
    assert _total_energy(event.state, 1.0) == _total_energy(incoming, 1.0)


def test_phase_preserving_action_shift_needs_a_nonperiodic_local_kick():
    # h(q)=q^2/2; old canonical order is (q, P, J, theta).
    q, theta = 2, 3
    symplectic = np.array([[0, 1, 0, 0], [-1, 0, 0, 0], [0, 0, 0, 1], [0, 0, -1, 0]])
    lift = np.array([[1, 0, 0, 0], [theta, 1, 0, q], [-q, 0, 1, 0], [0, 0, 0, 1]])
    np.testing.assert_array_equal(lift.T @ symplectic @ lift, symplectic)
    uncorrected = lift.copy()
    uncorrected[1, 0] = uncorrected[1, 3] = 0
    assert not np.array_equal(uncorrected.T @ symplectic @ uncorrected, symplectic)
    jump_after_one_phase_turn = ((theta + 2 * np.pi) * q) - theta * q
    assert jump_after_one_phase_turn == pytest.approx(2 * np.pi * q)
