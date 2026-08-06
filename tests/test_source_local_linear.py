from __future__ import annotations

import numpy as np
import pytest

from emergenz_knoten.local_mediator import LocalMediatorGrid, TelegraphMediator
from emergenz_knoten.source_local_linear import (
    diagnose_reciprocal_poles,
    reciprocal_source_local_matrix,
    telegraph_channel_realization,
)


def _channel():
    return telegraph_channel_realization(
        LocalMediatorGrid(
            spacing=0.25,
            time_step=0.01,
            points_left=12,
            points_right=18,
        ),
        TelegraphMediator(
            wave_speed=0.5,
            damping_rate=0.1,
            natural_frequency=0.1,
        ),
        readout_position=2.5,
    )


def test_channel_has_unit_dc_readout() -> None:
    channel = _channel()
    stationary = np.linalg.solve(
        np.eye(channel.order) - channel.transition,
        channel.source,
    )
    assert channel.readout @ stationary == pytest.approx(1.0)


def test_mass_emission_has_no_dynamic_channel_state() -> None:
    channel = _channel()
    matrix = reciprocal_source_local_matrix(
        channel,
        lambda_value=0.01,
        self_gain=0.4,
        cross_gain=0.02,
        emission="mass",
    )
    assert matrix.shape == (1, 1)
    assert matrix[0, 0] == pytest.approx(0.99 * 0.6)


def test_offset_emission_is_source_local_and_reciprocal() -> None:
    channel = _channel()
    matrix = reciprocal_source_local_matrix(
        channel,
        lambda_value=0.01,
        self_gain=0.4,
        cross_gain=0.02,
        emission="offset",
    )
    source_state = np.zeros(matrix.shape[0])
    source_state[0] = 1.0
    advanced = matrix @ source_state
    assert np.allclose(advanced[1:], channel.source)
    assert advanced[0] == pytest.approx(
        0.99 * 0.6 + 0.99 * 0.02 * (channel.readout @ channel.source)
    )


def test_current_emission_uses_only_two_emitter_offsets() -> None:
    channel = _channel()
    matrix = reciprocal_source_local_matrix(
        channel,
        lambda_value=0.01,
        self_gain=0.4,
        cross_gain=0.02,
        emission="current",
    )
    state = np.zeros(matrix.shape[0])
    state[:2] = (1.0, 1.0)
    advanced = matrix @ state
    expected_source = channel.source * (1.0 / 0.99 - 1.0)
    assert np.allclose(advanced[2:], expected_source)
    assert advanced[1] == pytest.approx(1.0)


def test_exact_diagnostic_is_finite() -> None:
    channel = _channel()
    matrix = reciprocal_source_local_matrix(
        channel,
        lambda_value=0.01,
        self_gain=0.43229116264043155,
        cross_gain=0.02,
        emission="offset",
    )
    result = diagnose_reciprocal_poles(matrix, channel, lambda_value=0.01)
    assert result.stable
    assert np.isfinite(result.eigenvector_condition)


def test_invalid_emission_is_rejected() -> None:
    with pytest.raises(ValueError, match="emission"):
        reciprocal_source_local_matrix(
            _channel(),
            lambda_value=0.01,
            self_gain=0.4,
            cross_gain=0.02,
            emission="target_gradient",
        )
