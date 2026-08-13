from __future__ import annotations

import numpy as np

from emergenz_knoten import (
    fit_conservative_recurrence_with_held_out_readout,
    fit_conservative_second_order_recurrence,
    fit_damped_second_order_recurrence,
    fit_recurrence_with_held_out_readout,
    fit_shared_recurrence,
    impulse_hankel_spectrum,
    interpret_continuous_second_order,
)


def _panel_response(poles: tuple[complex, ...], n_steps: int = 120) -> np.ndarray:
    time = np.arange(n_steps, dtype=float)
    panels = []
    for panel in range(3):
        features = []
        for feature in range(2):
            amplitudes = np.arange(1, len(poles) + 1, dtype=float)
            amplitudes *= 1.0 + 0.2 * panel + 0.1 * feature
            values = sum(
                amplitude * np.power(pole, time)
                for amplitude, pole in zip(amplitudes, poles, strict=True)
            )
            features.append(np.real(values))
        panels.append(np.column_stack(features))
    return np.stack(panels, axis=1)


def test_shared_recurrence_selects_exact_first_order_response() -> None:
    response = _panel_response((0.91,))

    first = fit_shared_recurrence(response, order=1)
    second = fit_shared_recurrence(response, order=2)

    np.testing.assert_allclose(first.coefficients, [0.91], atol=1e-12)
    assert first.test_rollout_rmse < 1e-10
    assert second.test_rollout_rmse < 1e-10
    assert first.stable


def test_second_order_and_damped_constraint_recover_oscillatory_response() -> None:
    radius = 0.96
    angle = 0.18
    poles = (radius * np.exp(1j * angle), radius * np.exp(-1j * angle))
    response = _panel_response(poles)

    first = fit_shared_recurrence(response, order=1)
    second = fit_shared_recurrence(response, order=2)
    damped = fit_damped_second_order_recurrence(response)
    conservative = fit_conservative_second_order_recurrence(response)

    assert second.test_rollout_rmse < 1e-8
    np.testing.assert_array_equal(damped.coefficients, second.coefficients)
    assert damped.test_rollout_rmse == second.test_rollout_rmse
    assert damped.equivalent_to_unconstrained
    assert first.test_rollout_rmse > 100.0 * second.test_rollout_rmse
    assert damped.underdamped
    assert damped.stable
    assert conservative.test_rollout_rmse > second.test_rollout_rmse
    np.testing.assert_allclose(
        np.sort_complex(damped.poles),
        np.sort_complex(np.asarray(poles)),
        atol=1e-6,
    )


def test_continuous_interpretation_does_not_create_an_independent_fit() -> None:
    underdamped = interpret_continuous_second_order(np.array([1.6, -0.81]))
    overdamped = interpret_continuous_second_order(np.array([1.1, -0.18]))
    invalid = interpret_continuous_second_order(np.array([0.4, 0.2]))

    assert underdamped.classification == "underdamped"
    assert underdamped.embeddable
    assert overdamped.classification == "overdamped"
    assert overdamped.embeddable
    assert not invalid.embeddable


def test_held_out_readout_does_not_influence_fitted_coefficients() -> None:
    radius = 0.94
    angle = 0.14
    poles = (radius * np.exp(1j * angle), radius * np.exp(-1j * angle))
    fit_response = _panel_response(poles)
    readout = 3.0 * fit_response[:, :, :1]

    baseline = fit_recurrence_with_held_out_readout(
        fit_response[:, :, 1:],
        readout,
        order=2,
        start_index=8,
    )
    altered = fit_recurrence_with_held_out_readout(
        fit_response[:, :, 1:],
        readout + 0.2 * np.sin(np.arange(readout.shape[0]))[:, None, None],
        order=2,
        start_index=8,
    )

    np.testing.assert_array_equal(altered.coefficients, baseline.coefficients)
    assert baseline.readout_test_rollout_rmse < 1e-8
    conservative = fit_conservative_recurrence_with_held_out_readout(
        fit_response[:, :, 1:],
        readout,
        start_index=8,
    )
    assert conservative.readout_test_rollout_rmse > baseline.readout_test_rollout_rmse
    np.testing.assert_allclose(np.abs(conservative.poles), 1.0)


def test_hankel_spectrum_detects_rank_one_exponential() -> None:
    response = _panel_response((0.87,))

    spectrum = impulse_hankel_spectrum(
        response,
        block_rows=12,
        block_columns=10,
    )

    assert spectrum.numerical_rank_1e6 == 1
    np.testing.assert_allclose(spectrum.stable_rank, 1.0, atol=1e-12)


def test_hankel_spectrum_keeps_a_common_layout_with_quiet_panel_channels() -> None:
    response = _panel_response((0.87,))
    response[:, 0, 1] = 0.0
    response[:, 1, 0] = 0.0

    spectrum = impulse_hankel_spectrum(
        response,
        block_rows=12,
        block_columns=10,
    )

    assert spectrum.active_channels == 4
    assert spectrum.numerical_rank_1e6 == 1
