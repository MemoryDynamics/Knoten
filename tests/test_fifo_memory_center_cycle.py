"""Fixed checks of reciprocal forces read from a synchronized FIFO."""

from dataclasses import replace

import numpy as np
import pytest

from experiments.current.reference.fifo_carrier_clock_cycle import (
    MemoryCenterClock,
    clock_return,
)
from experiments.current.reference.fifo_reversible_carrier import BoundaryState


def _model(weights):
    return MemoryCenterClock(2.0, 3.1, 1.4, 1.7, weights)


def _prepared(model):
    amplitude = np.array([0.7, 0.0])
    rows = [(-1) ** (j + 1) * amplitude for j in range(len(model.weights))]
    positions = np.vstack([amplitude, *rows, -amplitude])
    interval = np.pi / model.frequency
    clock = model.clock_mass * model.circumference / interval
    return BoundaryState(positions, np.zeros_like(positions), clock)


def _closed_position_block(weights):
    size = len(weights) + 2
    x, *memory, b = np.eye(size)
    tail = memory[-1]
    shifted = np.array([x + b - tail, *memory[:-1]])
    twice_center = 2 * (np.asarray(weights) @ shifted)
    return np.vstack([twice_center - x, shifted, twice_center - tail])


@pytest.mark.parametrize("weights", [(0.5, 0.5, 0), (0.125, 0, 0, 0.5, 0.375)])
def test_two_writes_are_exact_and_energy_neutral(weights):
    model = _model(weights)
    initial = current = _prepared(model)
    for _ in range(2):
        next_state, event, interval = clock_return(current, model)
        assert event.crossed
        assert event.energy_gap == pytest.approx(0, abs=4e-15)
        assert interval == pytest.approx(np.pi / model.frequency)
        assert next_state.clock_momentum == pytest.approx(initial.clock_momentum)
        np.testing.assert_allclose(
            event.state.position[1], current.position[0], atol=2e-15
        )
        np.testing.assert_allclose(next_state.position, -current.position, atol=2e-15)
        np.testing.assert_allclose(next_state.momentum, 0, atol=3e-15)
        current = next_state
    np.testing.assert_allclose(current.position, initial.position, atol=2e-15)


def test_flight_transfers_memory_momentum_and_preserves_energy_and_momenta():
    model = _model((0.5, 0.5, 0))
    q = np.array([[0.4, 0.6], [0.2, -0.3], [0.7, 0], [0.2, 0.3], [0.1, 0.8]])
    p = np.array([[0.07, 0.03], [0.05, -0.02], [0.1, 0.4], [0.5, 0], [0, -0.4]])
    moved, impulse = model.flight(q, p, 0.7)
    np.testing.assert_array_equal(moved[1:-1], q[1:-1])
    assert np.linalg.norm(impulse[1:-1] - p[1:-1]) > 0.1
    assert model.internal_energy(moved, impulse) == pytest.approx(
        model.internal_energy(q, p), abs=2e-15
    )
    np.testing.assert_allclose(impulse.sum(axis=0), p.sum(axis=0), atol=5e-16)

    def angular(a, b):
        return a[:, 0] @ b[:, 1] - a[:, 1] @ b[:, 0]

    assert angular(moved, impulse) == pytest.approx(angular(q, p), abs=5e-16)


@pytest.mark.parametrize(
    "weights", [(0.5, 0.5, 0), (0.125, 0, 0, 0.5, 0.375), (0, 0.5, 0.5)]
)
def test_transverse_return_and_characteristic_polynomial(weights):
    model = _model(weights)
    start = _prepared(model)
    size = len(weights) + 2

    def observed(probe):
        q, p = start.position.copy(), start.momentum.copy()
        q[:, 1], p[:, 1] = probe.reshape(2, size)
        arrived, _, _ = clock_return(replace(start, position=q, momentum=p), model)
        return np.r_[arrived.position[:, 1], arrived.momentum[:, 1]]

    step = 3e-8
    derivative = np.column_stack(
        [
            (observed(e * step) - observed(-e * step)) / (2 * step)
            for e in np.eye(2 * size)
        ]
    )
    block = _closed_position_block(weights)
    expected = np.block(
        [[block, np.zeros_like(block)], [np.zeros_like(block), np.linalg.inv(block).T]]
    )
    np.testing.assert_allclose(derivative, expected, atol=4e-13, rtol=0)
    weight_poly = np.poly1d(weights)
    z = np.poly1d([1, 0])
    polynomial = z ** (len(weights) + 1) * (z + 1) - 2 * z * (2 * z + 1) * weight_poly
    polynomial += (z + 1) ** 2
    np.testing.assert_allclose(np.poly(block), polynomial.c, atol=3e-13)


def test_recent_center_has_expanding_head_and_mismatch_mode():
    values, vectors = np.linalg.eig(_closed_position_block((0.5, 0.5, 0)))
    i = int(np.argmax(values.real))
    assert values[i].imag == 0
    assert 2 < values[i].real < 1 + np.sqrt(2)
    assert abs(vectors[0, i]) > 0.01
    assert abs(vectors[-1, i] - vectors[-2, i]) > 0.01


def test_unit_eigenvalues_allow_linear_growth_of_the_write_error():
    block = _closed_position_block((0, 0.5, 0.5))
    state = np.array([5, -3, 1, 0, 1])
    for writes in range(5):
        assert state[-1] - state[-2] == (-1) ** writes * (1 + 2 * writes)
        state = block @ state
