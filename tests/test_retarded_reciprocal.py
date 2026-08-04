from __future__ import annotations

import numpy as np
import pytest

from emergenz_knoten import FiniteMemoryState, SimulationConfig
from emergenz_knoten.local_mediator import LocalMediatorGrid, TelegraphMediator
from emergenz_knoten.reciprocal_nodes import reciprocal_pair_response
from emergenz_knoten.retarded_reciprocal import (
    retarded_reciprocal_pair_response,
    telegraph_static_readout_gain,
)


def _state() -> FiniteMemoryState:
    return FiniteMemoryState(
        x=np.array([0.0, 0.0]),
        memory=np.array(
            [
                [0.0, 0.0],
                [-0.1, 0.0],
                [0.1, 0.0],
                [0.0, -0.1],
                [0.0, 0.1],
            ]
        ),
        weights=np.array([0.4, 0.15, 0.15, 0.15, 0.15]),
    )


def _config(*, epsilon: float = 0.01, eta: float = 0.15) -> SimulationConfig:
    return SimulationConfig(
        steps=20,
        dim=2,
        epsilon=epsilon,
        eta=eta,
        alpha=0.1,
        memory_mass=1.0,
        deposition_kernel="delta",
        deposition_sigma=0.0,
        sigma_rep=1.0,
        sigma_att=3.0,
        amplitude_rep=1.0,
        amplitude_att=20.0,
        memory_factor=1.0,
        max_memory=5,
        burn_in=0,
        sample_every=1,
    )


def _mediator() -> tuple[LocalMediatorGrid, TelegraphMediator]:
    return (
        LocalMediatorGrid(
            spacing=0.25,
            time_step=0.1,
            points_left=20,
            points_right=30,
        ),
        TelegraphMediator(
            wave_speed=0.5,
            damping_rate=0.1,
            natural_frequency=0.1,
        ),
    )


def _run(*, cross_eta: float, steps: int = 20, epsilon: float = 0.01):
    grid, mediator = _mediator()
    first_noise = np.arange(2 * steps, dtype=float).reshape(steps, 2) / 100.0
    second_noise = first_noise[::-1].copy()
    return retarded_reciprocal_pair_response(
        _state(),
        _state(),
        _config(epsilon=epsilon),
        initial_center_separation=[1.0, 0.0],
        first_noise=first_noise,
        second_noise=second_noise,
        sample_steps=np.arange(steps + 1),
        cross_eta=cross_eta,
        mediator_grid=grid,
        mediator=mediator,
        mediator_readout_position=1.0,
    )


def test_static_readout_gain_matches_long_constant_source() -> None:
    from emergenz_knoten.local_mediator import simulate_telegraph_mediator

    grid, mediator = _mediator()
    expected = telegraph_static_readout_gain(
        grid,
        mediator,
        readout_position=1.0,
    )
    trace = simulate_telegraph_mediator(
        grid,
        mediator,
        source_values=np.ones(10_000),
        readout_positions=[1.0],
    )

    assert trace.values[-1, 0] == pytest.approx(expected, rel=2e-3)


def test_zero_cross_makes_all_conditions_bitwise_identical() -> None:
    response = _run(cross_eta=0.0)

    for condition in (1, 2, 3):
        np.testing.assert_array_equal(
            response.positions[:, condition],
            response.positions[:, 0],
        )
        np.testing.assert_array_equal(
            response.memory_centers[:, condition],
            response.memory_centers[:, 0],
        )


def test_instantaneous_control_matches_existing_reciprocal_arm() -> None:
    steps = 12
    response = _run(cross_eta=1e-3, steps=steps)
    first_noise = np.arange(2 * steps, dtype=float).reshape(steps, 2) / 100.0
    second_noise = first_noise[::-1].copy()
    direct = reciprocal_pair_response(
        _state(),
        _state(),
        _config(),
        initial_center_separation=[1.0, 0.0],
        first_noise=first_noise,
        second_noise=second_noise,
        sample_steps=np.arange(steps + 1),
        cross_eta=1e-3,
    )

    np.testing.assert_array_equal(response.positions[:, 1], direct.positions[:, 2])
    np.testing.assert_array_equal(
        response.memory_centers[:, 1],
        direct.memory_centers[:, 2],
    )


def test_retarded_readout_has_a_finite_grid_delay() -> None:
    response = _run(cross_eta=1e-3, steps=40, epsilon=0.0)
    one_way = 2

    assert np.count_nonzero(response.mediator_inputs[1, one_way, 0]) > 0
    # Four grid edges separate source and target; the local stencil cannot
    # reach the readout before traversing them.
    np.testing.assert_array_equal(
        response.mediator_readouts[:4, one_way, 0],
        0.0,
    )
    assert np.count_nonzero(response.mediator_readouts[4:, one_way, 0]) > 0


def test_retarded_one_way_leaves_source_on_channel_off_path() -> None:
    response = _run(cross_eta=1e-3, steps=40)

    np.testing.assert_array_equal(
        response.positions[:, 2, 0],
        response.positions[:, 0, 0],
    )
    assert not np.array_equal(
        response.positions[-1, 2, 1],
        response.positions[-1, 0, 1],
    )
