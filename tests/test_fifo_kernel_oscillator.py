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
    energy_closed_step,
    energy_matched_fifo_write,
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


def _paid_fixture():
    x = np.array([0.0])
    history = np.array([[0.0], [np.sqrt(2 * np.log(2))]])
    model = KernelOscillator(retention=0.5, modulation_amplitude=0.5)
    return KernelState(x, history, 0.4375, 0.0), model


def test_shell_write_can_pay_at_an_oscillator_turning_point():
    state, model = _paid_fixture()
    written, ledger = energy_matched_fifo_write(state, model)
    assert ledger.minimum_change == pytest.approx(53 / 512)
    assert ledger.excitation_before == pytest.approx(9 / 32)
    assert ledger.excitation_after == pytest.approx(91 / 512)
    assert state.momentum == written.momentum == 0
    assert (written.amplitude + 0.375) > 0
    assert ledger.energy_residual == pytest.approx(0, abs=3e-16)
    assert 0.125 + state.amplitude * 0.0625 > 0  # Fixed-amplitude write cannot use p=0.
    np.testing.assert_array_equal(written.memory, [[0.0], [0.0]])


def test_write_is_unavailable_if_total_energy_is_below_new_minimum():
    state, model = _paid_fixture()
    low = replace(state, amplitude=-0.3125, momentum=0.08)
    with pytest.raises(ValueError, match="minimum exceeds"):
        energy_matched_fifo_write(low, model)
    np.testing.assert_array_equal(low.memory, state.memory)


def test_released_energy_at_zero_excitation_needs_an_explicit_initial_phase():
    state, model = _paid_fixture()
    model = replace(model, base_amplitude=0)
    weights = exponential_memory_weights(0.5, len(state.memory))
    minimum = -gaussian_potential(
        state.x, state.memory, weights, sigma=1, amplitude=0.5
    )
    ground = replace(state, amplitude=minimum)
    with pytest.raises(ValueError, match="requires a declared phase"):
        energy_matched_fifo_write(ground, model)
    new, ledger = energy_matched_fifo_write(ground, model, birth_phase=np.pi / 2)
    assert ledger.excitation_before == 0
    assert ledger.excitation_after == pytest.approx(11 / 512)
    assert new.amplitude == pytest.approx(-0.375)
    assert new.momentum > 0
    assert ledger.energy_residual == pytest.approx(0, abs=3e-16)


def test_phase_innovations_change_future_drift_but_not_energy():
    state = _state()
    model = KernelOscillator()
    heads = []
    amplitudes = []
    for angle in (0.0, np.pi / 2, np.pi):
        result, before, paid = energy_closed_step(state, model, phase_shift=angle)
        assert before.motion < 0
        assert paid.energy_residual == pytest.approx(0, abs=4e-16)
        assert before.final_energy + paid.energy_residual == pytest.approx(
            before.initial_energy + before.motion
        )
        amplitudes.append(result.amplitude)
        out, _ = oscillator_write_split(result, model, write=False)
        heads.append(out.x)
    assert len(set(amplitudes)) == 3
    for a, b in zip(heads[:-1], heads[1:], strict=True):
        assert not np.allclose(a, b)


@pytest.mark.parametrize("phase_shift", [0.0, 1.3])
def test_oscillator_submap_preserves_area_when_old_and_new_memory_are_held(phase_shift):
    state, model = _paid_fixture()

    def chart(z):
        result, _ = energy_matched_fifo_write(
            replace(state, amplitude=z[0], momentum=z[1]),
            model,
            phase_shift=phase_shift,
        )
        return np.array([result.amplitude, result.momentum])

    center = np.array([0.4375, 0.2])
    scale = 1e-6
    derivative = np.column_stack(
        [
            (chart(center + e * scale) - chart(center - e * scale)) / (2 * scale)
            for e in np.eye(2)
        ]
    )
    assert np.linalg.det(derivative) == pytest.approx(1, abs=2e-10, rel=0)


def test_paid_fifo_still_discards_the_old_tail_at_fixed_head():
    model = KernelOscillator(mobility=0)
    x = np.zeros(2)
    a = KernelState(x, np.array([[0.0, 0.0], [1.0, 0.0]]), 1, 0.3)
    b = replace(a, memory=np.array([[0.0, 0.0], [-1.0, 0.0]]))
    plus, _, _ = energy_closed_step(a, model, phase_shift=0.26)
    minus, _, _ = energy_closed_step(b, model, phase_shift=0.26)
    assert not np.array_equal(a.memory, b.memory)
    np.testing.assert_array_equal(plus.memory, minus.memory)
    np.testing.assert_array_equal(plus.x, minus.x)
    assert plus.momentum == minus.momentum and plus.amplitude == minus.amplitude
