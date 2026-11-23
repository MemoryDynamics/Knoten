"""Checks of fixed-time geometry and endogenous clock bookkeeping."""

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
from experiments.current.reference.fifo_timing_cycle import fixed_timing_constraints


def _gram_energy(cycle, state):
    gram = state @ state.T
    return np.einsum("nij,ij->n", cycle.energy_forms, gram)


def test_variable_flight_constraints_reproduce_actual_section_and_clock_energy():
    model = MobileMemoryClock(
        body_mass=2, spring=0.5, clock_mass=1.4, circumference=1.7, record_mass=0.7
    )
    q = np.array([[0.4, 0.6], [0.2, -0.3], [0.7, 0], [0.2, 0.3], [0.2, 0.3]])
    p = np.array([[0.07, 0.03], [0.05, -0.02], [0.1, 0.4], [0.5, 0], [0, -0.4]])
    start = BoundaryState(q, p, 5.0)
    states, durations, gaps = [start], [], []
    for _ in range(3):
        state, event, dt = clock_return(states[-1], model)
        assert event.crossed
        states.append(state)
        durations.append(dt)
        gaps.append(event.energy_gap)
    assert np.ptp(durations) > 0.005

    cycle = fixed_timing_constraints(model, durations)
    phase = np.vstack([q, p])
    expected = np.array([np.vstack([s.position, s.momentum]) for s in states])
    np.testing.assert_allclose(cycle.returns @ phase, expected, atol=2e-14, rtol=0)
    np.testing.assert_allclose(
        (cycle.closure_and_copy @ phase)[10:],
        expected[:-1, 4] - expected[:-1, 3],
        atol=2e-14,
    )
    np.testing.assert_allclose(_gram_energy(cycle, phase), gaps, atol=2e-14)
    # The first cyclic loss assumes the last flight preceded the prefix.
    np.testing.assert_allclose(cycle.rotor_energy_loss[1:], gaps[1:], atol=3e-14)
    measured_start_energy = start.clock_momentum**2 / (2 * model.clock_mass)
    end_energy = states[-1].clock_momentum ** 2 / (2 * model.clock_mass)
    assert cycle.rotor_energy_loss[0] == pytest.approx(
        gaps[0] + end_energy - measured_start_energy, abs=3e-14
    )


def test_rank_of_gram_is_not_the_rank_of_the_written_geometry():
    model = MobileMemoryClock(spring=0.5)
    amplitude = np.array([0.7, 0])
    translation = np.array([0, 0.4])
    q = np.array([amplitude, -amplitude, amplitude, -amplitude, -amplitude])
    phase = np.vstack([q + translation, np.zeros_like(q)])
    cycle = fixed_timing_constraints(model, [np.pi, np.pi])
    np.testing.assert_allclose(cycle.closure_and_copy @ phase, 0, atol=2e-15)
    np.testing.assert_allclose(
        _gram_energy(cycle, phase), cycle.rotor_energy_loss, atol=2e-15
    )
    gram = phase @ phase.T
    assert np.linalg.matrix_rank(gram) == 2
    head_gram = cycle.head_offsets @ gram @ cycle.head_offsets.T
    assert np.linalg.matrix_rank(head_gram) == 1
    assert head_gram[1, 1] == pytest.approx(4 * amplitude @ amplitude)


@pytest.mark.parametrize(("horizon", "profile"), [(3, [1, 2, 4]), (5, [2, 1, 4, 3])])
def test_short_flights_lift_the_stationary_head_momentum_mode(horizon, profile):
    model = MobileMemoryClock(
        body_mass=2, record_mass=0.7, weights=(0.5, 0.5) + (0,) * (horizon - 2)
    )
    size = horizon + 2
    basis = np.eye(2 * size)
    gate = np.concatenate(carrier_map(basis[:size], basis[size:]))
    gate_only = np.linalg.matrix_power(gate, len(profile)) - basis
    translation = np.r_[np.ones(size), np.zeros(size)]
    head_momentum = basis[size]
    np.testing.assert_array_equal(gate_only @ translation, 0)
    np.testing.assert_array_equal(gate_only @ head_momentum, 0)
    np.testing.assert_array_equal(gate_only[0], 0)
    assert np.linalg.matrix_rank(gate_only) == 2 * size - 2

    epsilon = 1e-5
    cycle = fixed_timing_constraints(model, np.asarray(profile) * epsilon)
    closure = cycle.returns[-1] - basis
    slope = closure[0] @ head_momentum / epsilon
    assert slope == pytest.approx(sum(profile) / model.body_mass, abs=1e-6)
    np.testing.assert_allclose(closure @ translation, 0, atol=3e-15)
    assert np.linalg.matrix_rank(closure) == 2 * size - 1


@pytest.mark.parametrize("durations", [[], [1, 0], [np.inf], [[1, 2]]])
def test_only_positive_one_dimensional_timing_profiles_are_accepted(durations):
    with pytest.raises(ValueError, match="finite and positive"):
        fixed_timing_constraints(MobileMemoryClock(), durations)
