from __future__ import annotations

import numpy as np
import pytest

from emergenz_knoten import (
    LocalMediatorGrid,
    RelaxationDiffusionMediator,
    TelegraphMediator,
    relaxation_diffusion_frequency_response,
    rectangular_source,
    simulate_relaxation_diffusion_mediator,
    simulate_telegraph_mediator,
    telegraph_frequency_response,
)


def _grid() -> LocalMediatorGrid:
    return LocalMediatorGrid(
        spacing=0.25,
        time_step=0.01,
        points_left=80,
        points_right=120,
    )


def test_rectangular_source_has_exact_requested_support() -> None:
    source = rectangular_source(12, pulse_steps=4, amplitude=-2.0)

    np.testing.assert_array_equal(source[:4], -2.0)
    np.testing.assert_array_equal(source[4:], 0.0)


def test_zero_source_keeps_both_local_mediators_exactly_zero() -> None:
    grid = _grid()
    source = np.zeros(100)
    distances = [1.0, 2.0]

    diffusion = simulate_relaxation_diffusion_mediator(
        grid,
        RelaxationDiffusionMediator(diffusivity=1.0, decay_rate=0.1),
        source_values=source,
        readout_positions=distances,
    )
    telegraph = simulate_telegraph_mediator(
        grid,
        TelegraphMediator(
            wave_speed=1.0,
            damping_rate=0.1,
            natural_frequency=0.1,
        ),
        source_values=source,
        readout_positions=distances,
    )

    np.testing.assert_array_equal(diffusion.values, 0.0)
    np.testing.assert_array_equal(telegraph.values, 0.0)


@pytest.mark.parametrize("model", ["diffusion", "telegraph"])
def test_local_mediator_is_linear_under_global_source_sign_flip(model: str) -> None:
    grid = _grid()
    source = rectangular_source(400, pulse_steps=20)
    distances = [1.0, 3.0]
    if model == "diffusion":
        parameters = RelaxationDiffusionMediator(
            diffusivity=1.0,
            decay_rate=0.1,
        )
        positive = simulate_relaxation_diffusion_mediator(
            grid,
            parameters,
            source_values=source,
            readout_positions=distances,
        )
        negative = simulate_relaxation_diffusion_mediator(
            grid,
            parameters,
            source_values=-source,
            readout_positions=distances,
        )
    else:
        parameters = TelegraphMediator(
            wave_speed=1.0,
            damping_rate=0.1,
            natural_frequency=0.1,
        )
        positive = simulate_telegraph_mediator(
            grid,
            parameters,
            source_values=source,
            readout_positions=distances,
        )
        negative = simulate_telegraph_mediator(
            grid,
            parameters,
            source_values=-source,
            readout_positions=distances,
        )

    np.testing.assert_allclose(negative.values, -positive.values, atol=1e-15)


def test_telegraph_stencil_has_no_precursor_outside_its_discrete_cone() -> None:
    grid = LocalMediatorGrid(
        spacing=1.0,
        time_step=0.1,
        points_left=20,
        points_right=20,
    )
    source = rectangular_source(4, pulse_steps=1)
    trace = simulate_telegraph_mediator(
        grid,
        TelegraphMediator(
            wave_speed=1.0,
            damping_rate=0.0,
            natural_frequency=0.0,
        ),
        source_values=source,
        readout_positions=[4.0],
    )

    np.testing.assert_array_equal(trace.values, 0.0)


def test_unstable_relaxation_diffusion_step_is_rejected() -> None:
    with pytest.raises(ValueError, match="CFL"):
        simulate_relaxation_diffusion_mediator(
            LocalMediatorGrid(
                spacing=0.1,
                time_step=0.1,
                points_left=20,
                points_right=20,
            ),
            RelaxationDiffusionMediator(diffusivity=1.0, decay_rate=0.0),
            source_values=np.ones(2),
            readout_positions=[0.5],
        )


def test_normalized_frequency_responses_equal_one_at_zero_frequency() -> None:
    wavenumber = np.array([0.0, 0.5, 1.0])
    diffusion = relaxation_diffusion_frequency_response(
        wavenumber,
        0.0,
        RelaxationDiffusionMediator(diffusivity=2.0, decay_rate=0.1),
        normalize_static=True,
    )
    telegraph = telegraph_frequency_response(
        wavenumber,
        0.0,
        TelegraphMediator(
            wave_speed=1.0,
            damping_rate=0.1,
            natural_frequency=0.1,
        ),
        normalize_static=True,
    )

    np.testing.assert_allclose(diffusion, 1.0)
    np.testing.assert_allclose(telegraph, 1.0)


def test_diffusive_and_telegraph_transfer_functions_separate_off_dc() -> None:
    angular_frequency = np.linspace(0.0, 1.0, 50)
    diffusion = relaxation_diffusion_frequency_response(
        0.2,
        angular_frequency,
        RelaxationDiffusionMediator(diffusivity=2.0, decay_rate=0.1),
        normalize_static=True,
    )
    telegraph = telegraph_frequency_response(
        0.2,
        angular_frequency,
        TelegraphMediator(
            wave_speed=1.0,
            damping_rate=0.1,
            natural_frequency=0.1,
        ),
        normalize_static=True,
    )

    assert np.max(np.abs(diffusion[1:] - telegraph[1:])) > 0.1
