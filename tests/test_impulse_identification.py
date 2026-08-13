from __future__ import annotations

import numpy as np

from emergenz_knoten import (
    fit_damped_second_order_recurrence,
    fit_shared_recurrence,
    impulse_hankel_spectrum,
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

    assert second.test_rollout_rmse < 1e-8
    assert damped.test_rollout_rmse < 1e-6
    assert first.test_rollout_rmse > 100.0 * second.test_rollout_rmse
    assert damped.underdamped
    assert damped.stable
    np.testing.assert_allclose(
        np.sort_complex(damped.poles),
        np.sort_complex(np.asarray(poles)),
        atol=1e-6,
    )


def test_hankel_spectrum_detects_rank_one_exponential() -> None:
    response = _panel_response((0.87,))

    spectrum = impulse_hankel_spectrum(
        response,
        block_rows=12,
        block_columns=10,
    )

    assert spectrum.numerical_rank_1e6 == 1
    np.testing.assert_allclose(spectrum.stable_rank, 1.0, atol=1e-12)
