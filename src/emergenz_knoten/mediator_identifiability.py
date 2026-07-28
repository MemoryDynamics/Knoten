"""Spectral eligibility metrics for comparing fixed mediator responses."""

from __future__ import annotations

from typing import Any

import numpy as np


def vector_segment_power(
    segments: np.ndarray,
    *,
    time_step: float,
) -> tuple[np.ndarray, np.ndarray]:
    """Return angular frequencies and summed-component Hann periodograms."""

    values = np.asarray(segments, dtype=float)
    if (
        values.ndim != 3
        or values.shape[0] < 1
        or values.shape[1] < 4
        or values.shape[2] < 1
        or not np.isfinite(values).all()
    ):
        raise ValueError("segments must have finite shape (segments, samples, dim)")
    if not np.isfinite(time_step) or time_step <= 0.0:
        raise ValueError("time_step must be positive and finite")
    centered = values - np.mean(values, axis=1, keepdims=True)
    window = np.hanning(values.shape[1])
    window_power = float(np.sum(np.square(window)))
    transformed = np.fft.rfft(centered * window[None, :, None], axis=1)
    power = np.sum(np.square(np.abs(transformed)), axis=2) / window_power
    power[:, 0] = 0.0
    angular_frequency = 2.0 * np.pi * np.fft.rfftfreq(
        values.shape[1], d=float(time_step)
    )
    return angular_frequency, power


def transfer_identifiability_metrics(
    source_power: np.ndarray,
    response_a: np.ndarray,
    response_b: np.ndarray,
    *,
    minimum_frequency_contrast: float,
) -> dict[str, Any]:
    """Measure source-weighted separation of two normalized transfer responses."""

    power = np.asarray(source_power, dtype=float)
    first = np.asarray(response_a, dtype=np.complex128)
    second = np.asarray(response_b, dtype=np.complex128)
    if power.ndim != 2 or power.shape[0] < 1 or power.shape[1] < 2:
        raise ValueError("source_power must have shape (segments, frequencies)")
    if first.shape != (power.shape[1],) or second.shape != first.shape:
        raise ValueError("transfer responses must match the frequency axis")
    if (
        not np.isfinite(power).all()
        or np.any(power < 0.0)
        or not np.isfinite(first).all()
        or not np.isfinite(second).all()
    ):
        raise ValueError("power and transfer responses must be finite")
    if not np.isfinite(minimum_frequency_contrast) or minimum_frequency_contrast <= 0:
        raise ValueError("minimum_frequency_contrast must be positive")

    average_gain2 = 0.5 * (np.square(np.abs(first)) + np.square(np.abs(second)))
    difference2 = np.square(np.abs(first - second))
    relative_frequency_contrast = np.sqrt(
        np.divide(
            difference2,
            average_gain2,
            out=np.zeros_like(difference2),
            where=average_gain2 > 0.0,
        )
    )
    distinguishable = relative_frequency_contrast >= minimum_frequency_contrast
    source_totals = np.sum(power, axis=1)
    output_power = power * average_gain2[None, :]
    output_totals = np.sum(output_power, axis=1)
    if np.any(source_totals <= 0.0) or np.any(output_totals <= 0.0):
        raise ValueError("every segment must carry source and transmitted power")
    weighted_contrast = np.sqrt(
        np.sum(power * difference2[None, :], axis=1) / output_totals
    )
    distinguishable_fraction = (
        np.sum(output_power[:, distinguishable], axis=1) / output_totals
    )
    transmitted_fraction = output_totals / source_totals
    pooled_power = np.mean(power, axis=0)
    pooled_output = pooled_power * average_gain2
    pooled_output_total = float(np.sum(pooled_output))
    return {
        "relative_frequency_contrast": relative_frequency_contrast,
        "distinguishable_mask": distinguishable,
        "pooled_source_power": pooled_power,
        "pooled_output_power": pooled_output,
        "weighted_contrast": weighted_contrast,
        "distinguishable_power_fraction": distinguishable_fraction,
        "transmitted_power_fraction": transmitted_fraction,
        "pooled_weighted_contrast": float(
            np.sqrt(np.sum(pooled_power * difference2) / pooled_output_total)
        ),
        "pooled_distinguishable_power_fraction": float(
            np.sum(pooled_output[distinguishable]) / pooled_output_total
        ),
        "pooled_transmitted_power_fraction": float(
            pooled_output_total / np.sum(pooled_power)
        ),
    }
