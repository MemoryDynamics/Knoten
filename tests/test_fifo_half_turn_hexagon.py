"""Faithful hexagon with one genuine half-turn in register phase space."""

from dataclasses import replace
from fractions import Fraction as F

import numpy as np
import pytest

from experiments.current.reference.fifo_carrier_clock_cycle import (
    clock_return,
    prepared_half_turn_hexagon,
)
from experiments.current.reference.fifo_reversible_carrier import carrier_map


@pytest.mark.parametrize("record_mass", [1.0, 0.5])
def test_the_half_turn_flips_nonzero_impulse_and_keeps_true_history(record_mass):
    radius = 0.05
    model, start = prepared_half_turn_hexagon(radius, record_mass)
    phase = np.exp(1j * np.pi / 3)
    state = start
    normal = np.array([-0.5, 1, -1, 1, -0.5])
    inverse = np.array([1, 1 / record_mass, 1 / record_mass, 1 / record_mass, 1])
    for n in range(6):
        history = radius * phase ** (n - np.arange(1, 4))
        np.testing.assert_allclose(
            state.position[1:-1], np.c_[history.real, history.imag], rtol=0, atol=3e-11
        )
        np.testing.assert_allclose(state.position[-1], state.position[-2], atol=3e-11)
        arrived, event, duration = clock_return(state, model)
        assert event.crossed
        assert duration == pytest.approx(np.pi / 3, abs=3e-11)
        assert event.energy_gap == pytest.approx(0, abs=3e-11)
        np.testing.assert_allclose(
            event.state.position[1], state.position[0], atol=3e-11
        )
        np.testing.assert_allclose(normal @ event.state.position, 0, atol=3e-11)
        impulse = (normal * inverse) @ event.state.momentum
        assert np.linalg.norm(impulse) > 0.01
        np.testing.assert_allclose(
            (normal * inverse) @ arrived.momentum, -impulse, atol=3e-11, rtol=0
        )
        state = arrived
    np.testing.assert_allclose(state.position, start.position, atol=3e-11, rtol=0)
    np.testing.assert_allclose(state.momentum, start.momentum, atol=3e-11, rtol=0)
    assert state.clock_momentum == pytest.approx(start.clock_momentum, abs=3e-11)


def _rational_matrix(tau):
    e = np.array([1, 0, 0, 0, -1], dtype=object)
    normal = np.array([F(-1, 2), 1, -1, 1, F(-1, 2)], dtype=object)
    direction = normal * np.array([2 * tau, *([(1 - tau) / 3] * 3), 2 * tau])
    p = F(1, 2) * np.outer(e, e)
    a = np.eye(5, dtype=int).astype(object) - p / 2 - 2 * np.outer(direction, normal)
    c, g = [
        part.astype(int).astype(object) for part in carrier_map(np.eye(5), np.eye(5))
    ]
    return np.block([[a @ c, F(3, 4) * p @ g], [-p @ c, a.T @ g]])


@pytest.mark.parametrize("tau", [F(0), F(1, 2), F(1)])
def test_exact_polynomial_at_three_algebraic_interpolation_nodes(tau):
    matrix = _rational_matrix(tau)
    power = np.eye(10, dtype=int).astype(object)
    coefficients, traces = [F(1)], [F(0)]
    for k in range(1, 11):
        power = power @ matrix
        traces.append(F(np.trace(power)))
        coefficients.append(
            -sum(c * traces[k - j] for j, c in enumerate(coefficients)) / k
        )

    b = (37 - 2 * tau - 8 * tau**2) / 18

    def reduced(u):
        return u**3 - 3 * u**2 + b * (u + 2) - F(17, 4)

    for z in map(F, range(1, 12)):
        u = z + 1 / z
        expected = z**5 * (u - 2) * (u - 1) * reduced(u)
        assert sum(c * z ** (10 - k) for k, c in enumerate(coefficients)) == expected
    assert reduced(F(2)) == -((1 + 8 * tau) ** 2) / 36 < 0
    assert reduced(F(221, 110)) < 0


def test_perpendicular_instability_reaches_the_copy_error_at_equal_masses():
    model, base = prepared_half_turn_hexagon(0.05)

    def observed(probe):
        q = np.c_[base.position, probe[:5]]
        p = np.c_[base.momentum, probe[5:]]
        state, _, _ = clock_return(replace(base, position=q, momentum=p), model)
        return np.r_[state.position[:, 2], state.momentum[:, 2]]

    step = 1e-7
    jacobian = np.column_stack(
        [(observed(v * step) - observed(-v * step)) / (2 * step) for v in np.eye(10)]
    )
    values, vectors = np.linalg.eig(jacobian)
    selected = int(np.argmax(values.real))
    assert values[selected].real > 1.1
    assert abs(values[selected].imag) < 1e-12
    assert abs(vectors[4, selected] - vectors[3, selected]) > 0.01
