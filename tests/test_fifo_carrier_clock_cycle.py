"""Fixed synchronized returns and their transverse linearization."""

from dataclasses import replace

import numpy as np
import pytest
from scipy.optimize import brentq

from experiments.current.reference.fifo_carrier_clock_cycle import (
    CarrierClock,
    clock_return,
)
from experiments.current.reference.fifo_reversible_carrier import (
    BoundaryState,
    carrier_map,
)


MODEL = CarrierClock(body_mass=2.0, spring=3.1, clock_mass=1.4, circumference=1.7)


def _prepared(horizon, detuning=0.0):
    amplitude = np.array([0.7, 0.0])
    memory = np.array([(-1) ** (i + 1) * amplitude for i in range(horizon)])
    q = np.vstack((amplitude, memory, -amplitude))
    travel_time = (np.pi + detuning) / MODEL.frequency
    clock = MODEL.clock_mass * MODEL.circumference / travel_time
    return BoundaryState(q, np.zeros_like(q), clock)


def _energy(state):
    return MODEL.internal_energy(state.position, state.momentum) + (
        state.clock_momentum**2 / (2 * MODEL.clock_mass)
    )


@pytest.mark.parametrize("horizon", [1, 3, 5])
def test_same_carrier_and_free_clock_repeat_the_exact_prepared_writes(horizon):
    start = _prepared(horizon)
    current = start
    for _ in range(2):
        assert current.side == -1
        assert current.clock_momentum > 0
        np.testing.assert_allclose(
            current.position[-1], current.position[-2], atol=2e-15
        )
        arrived, event, interval = clock_return(current, MODEL)
        assert event.crossed
        assert event.energy_gap == pytest.approx(0, abs=3e-15)
        assert interval == pytest.approx(np.pi / MODEL.frequency)
        np.testing.assert_allclose(
            event.state.position[1], current.position[0], atol=2e-15
        )
        np.testing.assert_allclose(
            event.state.position[-1], current.position[-2], atol=2e-15
        )
        np.testing.assert_allclose(arrived.position, -current.position, atol=3e-15)
        assert _energy(arrived) == pytest.approx(_energy(start), abs=3e-15)
        current = arrived
    np.testing.assert_allclose(current.position, start.position, atol=3e-15)
    np.testing.assert_allclose(current.momentum, start.momentum, atol=4e-15)
    assert current.clock_momentum == pytest.approx(start.clock_momentum)


def test_clock_detuning_misses_the_next_oldest_deposit_without_an_external_reset():
    detuning = 0.2
    start = _prepared(3, detuning)
    arrived, event, _ = clock_return(start, MODEL)
    assert event.crossed and event.energy_gap == 0
    assert arrived.clock_momentum == pytest.approx(start.clock_momentum)
    error = arrived.position[-1] - arrived.position[-2]
    np.testing.assert_allclose(error, [0.7 * (np.cos(detuning) - 1), 0], atol=5e-16)
    assert error[0] < 0


def _position_block(horizon):
    columns = []
    for basis in np.eye(horizon + 2):
        updated, _ = carrier_map(basis[:, None], np.zeros((horizon + 2, 1)))
        updated[[0, -1]] = updated[[-1, 0]]
        columns.append(updated[:, 0])
    return np.array(columns).T


@pytest.mark.parametrize("horizon", [3, 5])
def test_full_transverse_return_contains_the_unstable_head_momentum_branch(horizon):
    start = _prepared(horizon)
    size = horizon + 2

    def observed(q_y, p_y):
        q, p = start.position.copy(), start.momentum.copy()
        q[:, 1] = q_y
        p[:, 1] = p_y
        current, _, _ = clock_return(replace(start, position=q, momentum=p), MODEL)
        return np.r_[current.position[:, 1], current.momentum[:, 1]]

    step = 2e-7
    basis = np.eye(2 * size)
    actual = np.column_stack(
        [
            (
                observed(*(e.reshape(2, size) * step))
                - observed(*(-e.reshape(2, size) * step))
            )
            / (2 * step)
            for e in basis
        ]
    )
    a = _position_block(horizon)
    d = np.linalg.inv(a).T
    np.testing.assert_allclose(actual[:size, :size], a, atol=5e-13)
    np.testing.assert_allclose(actual[size:, :size], 0, atol=5e-13)
    np.testing.assert_allclose(actual[size:, size:], d, atol=5e-12)

    contraction = brentq(
        lambda z: 1 + z * sum(z ** (2 * i) for i in range((horizon + 1) // 2)),
        -0.75,
        0,
    )
    expanding = 1 / contraction
    assert expanding < -4 / 3
    values, directions = np.linalg.eig(d)
    index = np.argmin(np.abs(values - expanding))
    assert values[index] == pytest.approx(expanding, abs=1e-11)
    assert abs(directions[0, index]) > 0.01
