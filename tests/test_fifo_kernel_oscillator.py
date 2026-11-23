"""Fixed energy and local response controls for reciprocal kernel modulation."""

from dataclasses import replace

import numpy as np
import pytest

from emergenz_knoten.kernels import (
    exponential_memory_weights,
    gaussian_gradient,
    gaussian_hessian,
    gaussian_potential,
)
from experiments.current.reference.fifo_kernel_oscillator import (
    KernelOscillator,
    KernelState,
    oscillator_write_split,
)


def _state():
    memory = np.array([[0.1, -0.2], [0.8, 0.1], [-0.4, 0.6]])
    return KernelState(memory[0].copy(), memory, 0.4, 0.37)


def test_kernel_modulation_swaps_energy_with_oscillator_not_with_writer():
    state = _state()
    model = KernelOscillator(base_sigma=1.2, modulation_sigma=0.8, stiffness=1.4)
    frozen, ledger = oscillator_write_split(state, model, write=False)
    written, write_ledger = oscillator_write_split(state, model)
    np.testing.assert_array_equal(frozen.x, written.x)
    np.testing.assert_array_equal(written.memory[1:], state.memory[:-1])
    np.testing.assert_array_equal(written.memory[0], written.x)
    assert frozen.amplitude == written.amplitude and frozen.momentum == written.momentum
    assert ledger.motion < 0 and abs(ledger.modulation) > 1e-3
    assert ledger.modulation == pytest.approx(-ledger.oscillator, abs=2e-16)
    assert ledger.write == 0
    assert ledger.net_residual == pytest.approx(0, abs=2e-16)
    rounding = 4 * np.spacing(write_ledger.initial_energy)
    assert write_ledger.net_residual == pytest.approx(0, abs=rounding)
    assert write_ledger.write == pytest.approx(
        write_ledger.final_energy - ledger.final_energy, abs=rounding
    )
    assert write_ledger.write > 0


@pytest.mark.parametrize("sign", [-1.0, 1.0])
@pytest.mark.parametrize("retention", [0.0, 0.35, 0.85])
def test_filled_write_work_equals_weighted_kernel_differences(sign, retention):
    state = _state()
    model = KernelOscillator(
        base_amplitude=sign,
        modulation_amplitude=0,
        retention=retention,
    )
    state = replace(state, amplitude=0, momentum=0)
    next_state, ledger = oscillator_write_split(state, model)
    weights = exponential_memory_weights(1 - retention, len(state.memory))
    removed = weights - np.r_[weights[1:], 0]
    distance_squared = np.sum((next_state.x - state.memory) ** 2, axis=1)
    expected = removed @ (sign * -np.expm1(-distance_squared / 2))
    assert ledger.modulation == ledger.oscillator == 0
    assert ledger.write == pytest.approx(expected, abs=2e-16)
    if retention > 0:
        assert sign * ledger.write > 0
        assert ledger.motion < 0
    else:
        assert ledger.write == ledger.motion == 0


def test_signed_modulation_can_reverse_without_external_switch_work():
    state = KernelState(np.array([0.0]), np.array([[0.0]]), 1, 0)
    model = KernelOscillator(
        base_amplitude=0,
        stiffness=4,
        retention=0,
        mobility=0,
        dt=np.pi / 2,
    )
    result, ledger = oscillator_write_split(state, model)
    assert result.amplitude == pytest.approx(-1.5)
    assert ledger.modulation == pytest.approx(-2.5)
    assert ledger.oscillator == pytest.approx(2.5)
    assert ledger.write == ledger.motion == 0
    assert ledger.net_residual == pytest.approx(0, abs=2e-16)


def test_numerical_overshoot_is_not_classified_as_passive_motion():
    with pytest.raises(ValueError, match="certified descent regime"):
        oscillator_write_split(_state(), KernelOscillator(dt=4))


@pytest.mark.parametrize("width_ratio,unstable", [(1.5, True), (3.0, False)])
def test_oscillator_static_softening_at_a_frozen_gaussian_equilibrium(
    width_ratio, unstable
):
    x, memory, weights = [1.0], [[0.0]], [1.0]
    g = np.exp(-0.5)
    a_eq = -g
    sigma = 1 / np.sqrt(width_ratio)
    amp = (g**2 / width_ratio) / np.exp(-width_ratio / 2)
    base = dict(sigma=sigma, amplitude=amp)
    assert gaussian_potential(x, memory, weights, sigma=1.0) == pytest.approx(g)
    c = gaussian_gradient(x, memory, weights, sigma=1.0)[0]
    gradient = gaussian_gradient(x, memory, weights, **base)[0]
    assert gradient + a_eq * c == pytest.approx(0, abs=2e-16)
    curvature = gaussian_hessian(x, memory, weights, **base)[0, 0]
    curvature += a_eq * gaussian_hessian(x, memory, weights, sigma=1.0)[0, 0]
    assert curvature > 0
    assert curvature - c**2 == pytest.approx((width_ratio - 2) * c**2)
    for inertia in (0.25, 4.0):
        generator = np.array([[-curvature, -c, 0], [0, 0, 1 / inertia], [-c, -1, 0]])
        eigenvalues = np.linalg.eigvals(generator)
        assert bool(eigenvalues.real.max() > 0) == unstable
        if unstable:
            growing = eigenvalues[np.argmax(eigenvalues.real)]
            assert growing.imag == pytest.approx(0, abs=2e-15)


def test_exact_opposite_external_kernel_still_pays_for_dissipation():
    x0 = 1.3
    decay = np.exp(-0.4)
    x1 = x0 * decay
    x2 = x1 / decay
    switch_work = x2**2 - x1**2
    dissipated = (x0**2 - x1**2) / 2 + (x2**2 - x1**2) / 2
    assert x2 == pytest.approx(x0)
    assert switch_work > 0
    assert switch_work == pytest.approx(dissipated)


def test_native_two_slot_ballistic_solution_has_constant_energy_and_positive_write_work():
    weights = exponential_memory_weights(0.4, 2)
    eta = 6.0
    d = np.sqrt(2 * np.log(eta * weights[1]))
    g = np.exp(-(d**2) / 2)
    head = np.array([0.0])
    memory = np.array([[0.0], [-d]])
    moved = head - eta * gaussian_gradient(head, memory, weights, sigma=1.0)
    np.testing.assert_allclose(moved, [d], atol=3e-16)
    updated = np.vstack((moved, memory[:-1]))
    e0 = gaussian_potential(head, memory, weights, sigma=1.0)
    e1 = gaussian_potential(moved, memory, weights, sigma=1.0)
    e2 = gaussian_potential(moved, updated, weights, sigma=1.0)
    expected = weights[0] * (1 - g) + weights[1] * (g - g**4)
    assert e2 == pytest.approx(e0)
    assert e2 - e1 == pytest.approx(expected)
    assert expected > 0
    assert abs(1 - d**2) < 1  # Stable speed, not a bound orbit or an energy source.
