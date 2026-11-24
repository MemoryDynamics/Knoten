"""Reversible binding of the last free coordinate of the FIFO hexagon."""

from dataclasses import replace
from fractions import Fraction as F

import numpy as np
import pytest

from experiments.current.reference.fifo_carrier_clock_cycle import (
    RestoredCenterClock,
    clock_return,
    prepared_hexagon,
)
from experiments.current.reference.fifo_reversible_carrier import carrier_map


@pytest.mark.parametrize("ratio", [6, 12])
def test_full_restoring_turn_preserves_six_autonomous_writes(ratio):
    _, start = prepared_hexagon(0.02)
    model = RestoredCenterClock(spring=0.5, restoring_ratio=ratio)
    phase = np.exp(1j * np.pi / 3)
    state = start
    for n in range(6):
        rotation = phase**n
        positions = (start.position[:, 0] + 1j * start.position[:, 1]) * rotation
        np.testing.assert_allclose(
            state.position, np.c_[positions.real, positions.imag], rtol=0, atol=2e-10
        )
        arrived, event, duration = clock_return(state, model)
        assert event.crossed
        assert event.energy_gap == pytest.approx(0, abs=2e-10)
        assert duration == pytest.approx(np.pi / 3, abs=2e-10)
        np.testing.assert_allclose(
            event.state.position[1], state.position[0], atol=2e-10
        )
        state = arrived
    np.testing.assert_allclose(state.position, start.position, atol=2e-10, rtol=0)
    np.testing.assert_allclose(state.momentum, start.momentum, atol=2e-10, rtol=0)
    assert state.clock_momentum == pytest.approx(start.clock_momentum, abs=2e-10)


def test_half_turn_of_excited_restoring_mode_does_not_keep_the_history():
    _, start = prepared_hexagon(0.7)
    model = RestoredCenterClock(spring=0.5, restoring_ratio=9)
    arrived, event, duration = clock_return(start, model)
    assert event.crossed
    assert duration == pytest.approx(np.pi / 3, abs=2e-12)
    w = np.array([-0.5, 1 + 3 / 572, -1 - 6 / 572, 1 + 3 / 572, -0.5])
    coordinate = w @ event.state.position
    assert np.linalg.norm(coordinate) > 0.003
    np.testing.assert_allclose(w @ arrived.position, -coordinate, atol=5e-12, rtol=0)
    assert np.linalg.norm(arrived.position[1:-1] - event.state.position[1:-1]) > 0.001


def test_reciprocal_characteristic_polynomial_is_exact_after_translation_removal():
    e = np.array([1, 0, 0, 0, -1])
    p2 = np.outer(e, e)
    u4 = 4 * np.eye(5, dtype=int) - p2
    c, g = [part.astype(int) for part in carrier_map(np.eye(5), np.eye(5))]
    scaled = np.block([[2 * u4 @ c, 3 * p2 @ g], [-4 * p2 @ c, 2 * u4 @ g]])
    scaled = scaled.astype(object)
    power = np.eye(10, dtype=int).astype(object)
    traces = [F(0)]
    coefficients = [F(1)]
    for k in range(1, 11):
        power = power @ scaled
        traces.append(F(np.trace(power), 8**k))
        coefficients.append(
            -sum(c * traces[k - j] for j, c in enumerate(coefficients)) / k
        )
    assert coefficients == [
        1,
        -2,
        2,
        F(1, 4),
        F(-15, 4),
        5,
        F(-15, 4),
        F(1, 4),
        2,
        -2,
        1,
    ]

    def cubic(u):
        return u**3 + u**2 - 2 * u + F(1, 4)

    assert cubic(F(-41, 20)) < 0 < cubic(F(-61, 30))


def test_autonomous_perpendicular_map_still_has_growing_observable_error():
    _, base = prepared_hexagon(0.02)
    model = RestoredCenterClock(spring=0.5)

    def observed(v):
        q = np.c_[base.position, v[:5]]
        p = np.c_[base.momentum, v[5:]]
        state, _, _ = clock_return(replace(base, position=q, momentum=p), model)
        return np.r_[state.position[:, 2], state.momentum[:, 2]]

    step = 1e-8
    basis = np.eye(10)
    jacobian = np.column_stack(
        [(observed(step * v) - observed(-step * v)) / (2 * step) for v in basis]
    )
    q, p = carrier_map(basis[:5], basis[5:])
    np.testing.assert_allclose(
        jacobian, np.concatenate(model.flight(q, p, np.pi / 3)), atol=1e-9, rtol=0
    )
    values, vectors = np.linalg.eig(jacobian)
    index = np.argmin(values.real)
    assert -1.25 < values[index].real < -1.2
    assert abs(values[index].imag) < 1e-12
    assert abs(vectors[4, index] - vectors[3, index]) > 0.01
