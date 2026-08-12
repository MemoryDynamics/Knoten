from __future__ import annotations

import numpy as np
import pytest

from emergenz_knoten import (
    FirstOrderMediatorState,
    SecondOrderMediatorState,
    advance_second_order_fixed_source,
    build_isotropic_mediator_modes,
    first_order_energy,
    instantaneous_radial_force,
    modal_source,
    modal_static_force,
    radial_gradient_mediator_green_derivative_3d,
    second_order_energy,
    second_order_fixed_source_damping_quadrature,
    selected_mode_step_response,
    step_first_order_mediator,
    step_second_order_mediator,
    zero_first_order_state,
    zero_second_order_state,
)


def _modes(**overrides):
    parameters = {
        "n_wavenumber": 48,
        "n_direction": 48,
        "k_max": 16.0,
        "spectral_shape": -1.9,
        "memory_loading": 0.3,
    }
    parameters.update(overrides)
    return build_isotropic_mediator_modes(**parameters)


def test_modal_equilibrium_has_registered_static_force_signs() -> None:
    modes = _modes(n_wavenumber=80, n_direction=80)
    forces = {radius: modal_static_force(modes, radius) for radius in (2.8, 5.0, 8.0)}
    assert forces[2.8] < 0.0
    assert forces[5.0] > 0.0
    assert forces[8.0] < 0.0
    exact = np.array(
        [
            radial_gradient_mediator_green_derivative_3d(
                radius,
                spectral_shape=-1.9,
                memory_loading=0.3,
            )
            for radius in (2.8, 5.0, 8.0)
        ]
    )
    np.testing.assert_allclose(list(forces.values()), exact, atol=1.1e-4)


def test_second_order_fixed_source_energy_loss_matches_damping_quadrature() -> None:
    modes = _modes(n_wavenumber=16, n_direction=16, k_max=3.0)
    rng = np.random.default_rng(781)
    amplitude_scale = 0.01 / np.sqrt(modes.restoring)
    state = SecondOrderMediatorState(
        5.0,
        rng.normal(size=modes.n_modes) * amplitude_scale,
        rng.normal(size=modes.n_modes) * amplitude_scale,
    )
    final = advance_second_order_fixed_source(state, modes, duration=0.7)
    energy_loss = second_order_energy(state, modes) - second_order_energy(final, modes)
    damping_loss = second_order_fixed_source_damping_quadrature(
        state,
        modes,
        duration=0.7,
        quadrature_order=48,
    )
    assert energy_loss == pytest.approx(damping_loss, rel=2.0e-12, abs=2.0e-12)


@pytest.mark.parametrize("order", ["second", "first"])
def test_split_step_closes_energy_and_cross_off_is_exact(order: str) -> None:
    modes = _modes(n_wavenumber=16, n_direction=16)
    if order == "second":
        state = zero_second_order_state(modes, separation=5.0)
        final, ledger = step_second_order_mediator(state, modes, time_step=0.2)
    else:
        state = zero_first_order_state(modes, separation=5.0)
        final, ledger = step_first_order_mediator(state, modes, time_step=0.2)
    assert final.separation != pytest.approx(state.separation, abs=1.0e-12)
    assert ledger.source_dissipation >= 0.0
    assert ledger.mediator_dissipation >= -2.0e-14
    assert abs(ledger.balance_residual) < 2.0e-13
    assert ledger.maximum_source_work_residual < 2.0e-13

    off_modes = _modes(n_wavenumber=16, n_direction=16, coupling=0.0)
    if order == "second":
        off_state = zero_second_order_state(off_modes, separation=5.0)
        off_final, off_ledger = step_second_order_mediator(
            off_state, off_modes, time_step=0.2
        )
    else:
        off_state = zero_first_order_state(off_modes, separation=5.0)
        off_final, off_ledger = step_first_order_mediator(
            off_state, off_modes, time_step=0.2
        )
    assert off_final.separation == off_state.separation
    assert off_ledger.energy_before == 0.0
    assert off_ledger.energy_after == 0.0
    assert off_ledger.source_dissipation == 0.0
    assert off_ledger.mediator_dissipation == 0.0


def test_first_and_second_order_controls_share_static_susceptibility() -> None:
    modes = _modes(n_wavenumber=20, n_direction=20)
    source = modal_source(modes, 5.0)
    equilibrium = source / modes.restoring
    second = SecondOrderMediatorState(5.0, equilibrium, np.zeros(modes.n_modes))
    first = FirstOrderMediatorState(5.0, equilibrium)
    assert instantaneous_radial_force(5.0, second.field, modes) == pytest.approx(
        instantaneous_radial_force(5.0, first.field, modes), abs=1.0e-15
    )
    assert second_order_energy(second, modes) == pytest.approx(
        first_order_energy(first, modes), abs=1.0e-15
    )


def test_selected_mode_second_order_overshoots_but_first_order_is_monotone() -> None:
    times = np.linspace(0.0, 40.0, 2001)
    restoring = 0.42310724601601946
    damping = 2.0 * np.sqrt(0.3)
    second = selected_mode_step_response(
        times,
        restoring=restoring,
        damping=damping,
        dynamic_order="second",
    )
    first = selected_mode_step_response(
        times,
        restoring=restoring,
        damping=damping,
        dynamic_order="first",
    )
    assert np.max(second) > 1.005
    assert np.any(np.diff(second) < 0.0)
    assert np.all(np.diff(first) >= 0.0)
    assert np.max(first) < 1.0


def test_source_discrete_gradient_remains_stable_for_tiny_motion() -> None:
    modes = _modes(n_wavenumber=16, n_direction=16)
    state = zero_second_order_state(modes, separation=5.0)
    for _ in range(10):
        state, ledger = step_second_order_mediator(
            state,
            modes,
            time_step=0.03,
            relative_mobility=0.01,
        )
        assert abs(ledger.balance_residual) < 2.0e-13
        assert ledger.maximum_source_work_residual < 2.0e-13


def test_parameter_validation_rejects_inconsistent_or_unstable_modes() -> None:
    with pytest.raises(ValueError, match="must equal memory_loading"):
        build_isotropic_mediator_modes(
            memory_loading=0.3,
            memory_decay=0.2,
            conjugate_decay=0.2,
        )
    with pytest.raises(ValueError, match="strictly positive"):
        build_isotropic_mediator_modes(
            spectral_shape=-3.0,
            memory_loading=0.01,
        )


def test_state_arrays_are_immutable_copies() -> None:
    modes = _modes(n_wavenumber=8, n_direction=8)
    field = np.zeros(modes.n_modes)
    velocity = np.zeros(modes.n_modes)
    state = SecondOrderMediatorState(5.0, field, velocity)
    field[0] = 1.0
    velocity[0] = 1.0
    assert state.field[0] == 0.0
    assert state.conjugate_velocity[0] == 0.0
    with pytest.raises(ValueError):
        state.field[0] = 2.0


def test_split_trajectory_has_second_order_step_refinement() -> None:
    modes = _modes(n_wavenumber=24, n_direction=24)

    def simulate(time_step: float) -> tuple[float, np.ndarray, np.ndarray]:
        state = zero_second_order_state(modes, separation=5.0)
        for _ in range(round(100.0 / time_step)):
            state, _ = step_second_order_mediator(
                state,
                modes,
                time_step=time_step,
                relative_mobility=0.3,
            )
        return state.separation, state.field, state.conjugate_velocity

    reference = simulate(0.125)
    errors = []
    for time_step in (1.0, 0.5, 0.25):
        candidate = simulate(time_step)
        error = np.sqrt(
            (candidate[0] - reference[0]) ** 2
            + np.dot(
                modes.restoring * (candidate[1] - reference[1]),
                candidate[1] - reference[1],
            )
            + np.dot(candidate[2] - reference[2], candidate[2] - reference[2])
        )
        errors.append(float(error))
    assert errors[0] > errors[1] > errors[2]
    assert errors[0] / errors[1] > 3.0
    assert errors[1] / errors[2] > 3.0
