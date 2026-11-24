"""Fixed mobile-register checks, not a scan of the native dynamics."""

from dataclasses import replace

import numpy as np
import pytest

from experiments.current.reference.fifo_carrier_clock_cycle import (
    MobileMemoryClock,
    clock_return,
)
from experiments.current.reference.fifo_reversible_carrier import (
    BoundaryState,
    carrier_map,
)


def _model(horizon, mass):
    return MobileMemoryClock(
        spring=0.5,
        weights=(0.5, 0.5) + (0,) * (horizon - 2),
        record_mass=mass,
    )


def _prepared(model):
    amplitude = np.array([0.7, 0.0])
    rows = [(-1) ** (j + 1) * amplitude for j in range(len(model.weights))]
    q = np.vstack([amplitude, *rows, -amplitude])
    return BoundaryState(q, np.zeros_like(q), model.frequency / np.pi)


@pytest.mark.parametrize("mass", [1, 1 / 3, 1 / 8])
def test_mobile_records_leave_the_prepared_orbit_exact(mass):
    model = _model(3, mass)
    initial = current = _prepared(model)
    for _ in range(2):
        arrived, event, dt = clock_return(current, model)
        assert event.crossed
        assert event.energy_gap == pytest.approx(0, abs=2e-15)
        assert dt == pytest.approx(np.pi)
        assert arrived.clock_momentum == pytest.approx(initial.clock_momentum)
        np.testing.assert_allclose(
            event.state.position[1], current.position[0], atol=2e-15
        )
        np.testing.assert_allclose(arrived.position, -current.position, atol=3e-15)
        np.testing.assert_allclose(arrived.momentum, 0, atol=3e-15)
        current = arrived
    np.testing.assert_allclose(current.position, initial.position, atol=3e-15)


def test_mobile_flight_moves_records_and_preserves_hamiltonian_invariants():
    model = _model(3, 1 / 3)
    q = np.array([[0.4, 0.6], [0.2, -0.3], [0.7, 0], [0.2, 0.3], [0.1, 0.8]])
    p = np.array([[0.07, 0.03], [0.05, -0.02], [0.1, 0.4], [0.5, 0], [0, -0.4]])
    moved, impulse = model.flight(q, p, 0.7)
    assert np.linalg.norm(moved[1:-1] - q[1:-1]) > 0.1
    assert model.internal_energy(moved, impulse) == pytest.approx(
        model.internal_energy(q, p), abs=2e-15
    )
    np.testing.assert_allclose(impulse.sum(axis=0), p.sum(axis=0), atol=6e-16)

    def angular(a, b):
        return a[:, 0] @ b[:, 1] - a[:, 1] @ b[:, 0]

    assert angular(moved, impulse) == pytest.approx(angular(q, p), abs=6e-16)
    restored_q, restored_p = model.flight(moved, impulse, -0.7)
    np.testing.assert_allclose(restored_q, q, atol=7e-16)
    np.testing.assert_allclose(restored_p, p, atol=7e-16)


def _flight_after_write(model):
    size = len(model.weights) + 2
    columns = []
    for basis in np.eye(2 * size):
        q, p = basis.reshape(2, size, 1)
        wq, wp = carrier_map(q, p)
        flowed = model.flight(wq, wp, np.pi / model.frequency)
        columns.append(np.concatenate(flowed).ravel())
    return np.array(columns).T


@pytest.mark.parametrize(("horizon", "ratio"), [(3, 2), (3, 3), (5, 3)])
def test_commensurate_position_polynomials_and_reciprocal_momentum(horizon, ratio):
    model = _model(horizon, 1 / (ratio**2 - 1))
    assert model.balance_frequency / model.frequency == pytest.approx(ratio)
    jacobian = _flight_after_write(model)
    size = horizon + 2
    block = jacobian[:size, :size]
    np.testing.assert_allclose(jacobian[size:, :size], 0, atol=5e-15)
    np.testing.assert_allclose(
        jacobian[size:, size:], np.linalg.inv(block).T, atol=5e-15
    )
    z = np.poly1d([1, 0])
    if ratio % 2 == 0:
        polynomial = z ** (horizon + 2) + z**2 - z - 1
    else:
        alpha = 1 / ratio**2
        p0 = (z + 1) * (z ** (horizon + 1) - 2 * z**2 + 1)
        p1 = (z + 1) * (z ** (horizon - 1) * (z**2 - 2 * z - 1) + z + 1)
        polynomial = p0 + (p1 - p0) * alpha
    np.testing.assert_allclose(np.poly(block), polynomial.c, atol=2e-13)


def test_equal_mass_full_jacobian_has_observable_expanding_mode():
    model = _model(3, 1)
    size = 5
    start = _prepared(model)
    expected = _flight_after_write(model)

    def observed(probe):
        q, p = start.position.copy(), start.momentum.copy()
        q[:, 1], p[:, 1] = probe.reshape(2, size)
        arrived, _, _ = clock_return(replace(start, position=q, momentum=p), model)
        return np.r_[arrived.position[:, 1], arrived.momentum[:, 1]]

    step = 2e-8
    jacobian = np.column_stack(
        [
            (observed(e * step) - observed(-e * step)) / (2 * step)
            for e in np.eye(2 * size)
        ]
    )
    np.testing.assert_allclose(jacobian, expected, atol=6e-13, rtol=0)
    eye = np.eye(2 * size)
    assert np.linalg.det(-2 * eye - expected) > 190
    assert np.linalg.det(-1.5 * eye - expected) < -4
    values, vectors = np.linalg.eig(expected)
    found = [
        i for i, z in enumerate(values) if abs(z.imag) < 1e-12 and -2 < z.real < -1.5
    ]
    assert len(found) == 1
    chosen = vectors[:, found[0]]
    assert abs(chosen[4] - chosen[3]) > 0.02
