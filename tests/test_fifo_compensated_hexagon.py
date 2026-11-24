"""Checks for two actively compensating storage phases."""

from dataclasses import replace

import numpy as np
import pytest
from mpmath import iv

from experiments.current.reference.fifo_carrier_clock_cycle import clock_return
from experiments.current.reference.fifo_compensated_hexagon import (
    prepared_compensated_hexagon,
)
from experiments.current.reference.fifo_reversible_carrier import carrier_map


def test_two_nonresonant_phases_close_the_true_history_with_an_internal_clock():
    radius = 0.04
    model, start = prepared_compensated_hexagon(radius)
    state = start
    angle = np.pi / 3
    phase = np.exp(1j * angle)
    inverse, modes = model._modal_data(5)
    for n in range(6):
        stored = radius * phase ** (n - np.arange(1, 4))
        np.testing.assert_allclose(
            state.position[1:-1], np.c_[stored.real, stored.imag], atol=3e-11, rtol=0
        )
        np.testing.assert_allclose(state.position[-1], state.position[-2], atol=3e-11)
        arrived, event, duration = clock_return(state, model)
        assert event.crossed
        assert duration == pytest.approx(angle, abs=3e-11)
        assert event.energy_gap == pytest.approx(0, abs=3e-11)
        np.testing.assert_allclose(
            event.state.position[1], state.position[0], atol=3e-11
        )
        for normal, frequency in modes[2:]:
            assert abs(np.sin(frequency * duration)) > 0.3
            assert np.linalg.norm(normal @ event.state.position) > 0.02
            projected = normal * inverse
            before = projected @ event.state.momentum
            assert np.linalg.norm(before) > 0.01
            np.testing.assert_allclose(
                projected @ arrived.momentum, -before, atol=3e-11, rtol=0
            )
        state = arrived
    np.testing.assert_allclose(state.position, start.position, atol=3e-11, rtol=0)
    np.testing.assert_allclose(state.momentum, start.momentum, atol=3e-11, rtol=0)
    assert state.clock_momentum == pytest.approx(start.clock_momentum, abs=3e-11)


def _gate():
    return tuple(matrix.astype(int) for matrix in carrier_map(np.eye(5), np.eye(5)))


def test_interval_sign_of_compensated_normal_characteristic_polynomial():
    previous_precision = iv.dps
    iv.dps = 60
    try:
        _check_interval_determinant_signs()
    finally:
        iv.dps = previous_precision


def _check_interval_determinant_signs():
    s = iv.sqrt(3)
    gap = iv.sqrt(35223) / 112
    minus = (-31 * s - iv.sqrt(35223)) / 224
    plus = (-31 * s + iv.sqrt(35223)) / 224
    robin = iv.matrix([[15 * s, 5 * iv.sqrt(1155)], [5 * iv.sqrt(1155), -77 * s]]) / 224
    ga = iv.matrix([0, 1, 0, -1, 0]) / iv.sqrt(iv.mpf(9) / 8)
    gs = iv.matrix([iv.mpf(1) / 3, 1, -iv.mpf(8) / 3, 1, iv.mpf(1) / 3])
    gs /= iv.sqrt(iv.mpf(385) / 72)
    basis = iv.matrix([[ga[j], gs[j]] for j in range(5)])
    j0 = iv.eye(5)
    e = iv.matrix([1, 0, 0, 0, -1])
    relative = e * e.T / 2
    inverse = iv.diag([1, *([iv.mpf(9) / 16] * 3), 1])
    qq = j0 - inverse * relative / 2
    qp = (s / 2) * inverse * relative * inverse
    pq = -(s / 2) * relative
    pp = qq.T
    for target, projector, bounds in (
        (minus, (plus * iv.eye(2) - robin) / gap, ("5.63942022531", "5.63942022532")),
        (plus, (robin - minus * iv.eye(2)) / gap, ("1.01611667001", "1.01611667003")),
    ):
        lo, hi = map(iv.mpf, bounds)

        def residual(ratio):
            angle = ratio * iv.pi / 6
            return ratio * iv.sin(angle) / iv.cos(angle) - target

        assert residual(lo).b < 0 < residual(hi).a
        omega2 = iv.mpf(list(bounds)) ** 2
        denom = omega2 + target**2
        vs = basis * projector * basis.T
        c_minus_1 = -2 * target**2 / denom
        qq += c_minus_1 * inverse * vs
        qp += (2 * target / denom) * inverse * vs * inverse
        pq -= (2 * target * omega2 / denom) * vs
        pp += c_minus_1 * vs * inverse
    a, b = [iv.matrix(matrix.tolist()) for matrix in _gate()]
    qq, qp, pq, pp = qq * a, qp * b, pq * a, pp * b
    matrix = iv.matrix(
        [
            [*[qq[i, j] for j in range(5)], *[qp[i, j] for j in range(5)]]
            for i in range(5)
        ]
        + [
            [*[pq[i, j] for j in range(5)], *[pp[i, j] for j in range(5)]]
            for i in range(5)
        ]
    )
    assert iv.det(-iv.eye(10) - matrix).b < -1
    assert iv.det(-iv.mpf("1.2") * iv.eye(10) - matrix).a > 0
    assert iv.det(-iv.mpf("1.1") * iv.eye(10) - matrix).b < 0


def test_fixed_perpendicular_perturbation_reaches_the_copy_error():
    model, base = prepared_compensated_hexagon(0.04)

    def observed(probe):
        q = np.c_[base.position, probe[:5]]
        p = np.c_[base.momentum, probe[5:]]
        state, _, _ = clock_return(replace(base, position=q, momentum=p), model)
        return np.r_[state.position[:, 2], state.momentum[:, 2]]

    step = 1e-7
    basis = np.eye(10)
    jacobian = np.column_stack(
        [(observed(step * v) - observed(-step * v)) / (2 * step) for v in basis]
    )
    written = carrier_map(basis[:5], basis[5:])
    expected = np.concatenate(model.flight(*written, np.pi / 3))
    np.testing.assert_allclose(jacobian, expected, atol=3e-10, rtol=0)
    values, directions = np.linalg.eig(jacobian)
    selected = int(np.argmin(values.real))
    assert -1.2 < values[selected].real < -1.1
    assert abs(values[selected].imag) < 1e-12
    assert abs(directions[4, selected] - directions[3, selected]) > 0.01
