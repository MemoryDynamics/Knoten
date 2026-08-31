"""Target-free primitives for resolved-noise rotating-wave stress tests."""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Iterable, Mapping

import numpy as np

from .rotating_wave_stability import native_fifo_step, translation_reduced_features


@dataclass(frozen=True)
class NoisyStep:
    """One FIFO update with audited intended and effective innovation."""

    history: np.ndarray
    intended_increment: np.ndarray
    effective_increment: np.ndarray


def noisy_native_fifo_step(
    history: np.ndarray,
    *,
    epsilon: float,
    noise: np.ndarray,
    **parameters: float,
) -> NoisyStep:
    """Apply innovation only to the newest slot after the native FIFO step."""

    amplitude = float(epsilon)
    innovation = np.asarray(noise, dtype=float)
    if not math.isfinite(amplitude) or amplitude < 0.0:
        raise ValueError("epsilon must be finite and nonnegative")
    if innovation.shape != (2,) or not np.isfinite(innovation).all():
        raise ValueError("noise must be a finite two-vector")
    deterministic = native_fifo_step(history, **parameters)
    intended = amplitude * innovation
    result = deterministic.copy()
    result[0] = deterministic[0] + intended
    effective = result[0] - deterministic[0]
    return NoisyStep(result, intended, effective)


def brownian_refinement_paths(
    seed: int,
    *,
    fine_steps: int = 4000,
) -> tuple[np.ndarray, np.ndarray]:
    """Return the registered fine path and pair-aggregated coarse path."""

    if isinstance(seed, bool) or not isinstance(seed, int):
        raise ValueError("seed must be an integer")
    if (
        isinstance(fine_steps, bool)
        or not isinstance(fine_steps, int)
        or fine_steps < 2
        or fine_steps % 2
    ):
        raise ValueError("fine_steps must be a positive even integer")
    fine = np.random.Generator(np.random.PCG64(seed)).standard_normal(
        (fine_steps, 2)
    )
    coarse = (fine[0::2] + fine[1::2]) / math.sqrt(2.0)
    return fine, coarse


def dimensionless_noise_amplitude(
    *, chi: float, radius: float, alpha: float
) -> float:
    """Map the common Paper-I diffusion coordinate chi to raw epsilon."""

    values = (float(chi), float(radius), float(alpha))
    if not all(math.isfinite(value) for value in values):
        raise ValueError("chi, radius and alpha must be finite")
    if chi < 0.0 or radius <= 0.0 or not 0.0 < alpha < 1.0:
        raise ValueError("require chi>=0, radius>0 and 0<alpha<1")
    return float(chi * radius * math.sqrt(alpha))


def injection_resolution(
    intended: np.ndarray,
    effective: np.ndarray,
) -> dict[str, float | str]:
    """Classify whether a nonzero intended innovation survives binary64."""

    wanted = np.asarray(intended, dtype=float)
    actual = np.asarray(effective, dtype=float)
    if wanted.shape != actual.shape or wanted.size == 0:
        raise ValueError("increments must have the same nonempty shape")
    if not np.isfinite(wanted).all() or not np.isfinite(actual).all():
        raise ValueError("increments must be finite")
    intended_rms = float(np.sqrt(np.mean(wanted * wanted)))
    effective_rms = float(np.sqrt(np.mean(actual * actual)))
    if intended_rms == 0.0:
        label = "deterministic-control"
        ratio = 1.0 if effective_rms == 0.0 else math.inf
    else:
        ratio = effective_rms / intended_rms
        fraction = float(np.count_nonzero(actual) / actual.size)
        if ratio <= 0.1 or fraction <= 0.1:
            label = "unresolved"
        elif ratio >= 0.5 and fraction >= 0.5:
            label = "resolved"
        else:
            label = "partially-resolved"
    fraction = float(np.count_nonzero(actual) / actual.size)
    return {
        "classification": label,
        "intended_rms": intended_rms,
        "effective_rms": effective_rms,
        "effective_to_intended_rms": ratio,
        "nonzero_fraction": fraction,
    }


def visible_orbit_observables(
    history: np.ndarray,
    *,
    alpha: float,
    memory_mass: float,
    target_theta: float,
) -> dict[str, float | bool]:
    """Return centre-reduced radius and translation-invariant edge phase."""

    features, _ = translation_reduced_features(
        history, alpha=alpha, memory_mass=memory_mass
    )
    newest = features[0, 0] + 1j * features[0, 1]
    state = np.asarray(history, dtype=float)
    if features.shape[0] < 3:
        raise ValueError("phase observation requires at least three history slots")
    newest_edge = complex(*(state[0] - state[1]))
    previous_edge = complex(*(state[1] - state[2]))
    phase_increment = float(np.angle(newest_edge * np.conjugate(previous_edge)))
    error = float(np.angle(np.exp(1j * (phase_increment - target_theta))))
    return {
        "visible_radius": float(abs(newest)),
        "phase_increment": phase_increment,
        "wrapped_phase_error": error,
        "positive_chirality": bool(phase_increment > 0.0),
    }


def resolved_arm_pass(metrics: Mapping[str, float | bool]) -> bool:
    """Apply the frozen N0 resolved-arm thresholds."""

    return bool(
        metrics["completed"]
        and metrics["finite"]
        and float(metrics["maximum_d0_fraction"]) <= 0.10
        and float(metrics["late_rms_d0_fraction"]) <= 0.05
        and float(metrics["maximum_radius_relative_error"]) <= 0.05
        and float(metrics["late_rms_phase_error_over_theta"]) <= 0.20
        and float(metrics["positive_chirality_fraction"]) >= 0.99
        and float(metrics["maximum_pair_growth"]) <= 10.0
        and float(metrics["final_pair_ratio"]) <= 0.1
        and not metrics["stopped"]
    )


def grid_cell_decision(resolution_and_pass: Iterable[tuple[str, bool]]) -> str:
    """Combine both candidates and all seeds at one nonzero chi."""

    rows = list(resolution_and_pass)
    if not rows:
        raise ValueError("at least one arm is required")
    if any(label == "resolved" and not passed for label, passed in rows):
        return "stress-fail"
    if all(label == "resolved" and passed for label, passed in rows):
        return "all-cell-stable"
    return "inconclusive"


def ladder_decision(decisions: Iterable[str]) -> str:
    """Apply the registered ordered-grid decision without interpolation."""

    rows = list(decisions)
    allowed = {"all-cell-stable", "stress-fail", "inconclusive"}
    if not rows or any(row not in allowed for row in rows):
        raise ValueError("invalid or empty decision ladder")
    stable_indices = [i for i, row in enumerate(rows) if row == "all-cell-stable"]
    if not stable_indices:
        return "n0-noise-robustness-fail"
    if rows[-1] == "all-cell-stable" and not any(
        row == "stress-fail" for row in rows
    ):
        return "n0-noise-stable-through-grid"
    for start in range(len(rows) - 2):
        if rows[start : start + 3] != ["all-cell-stable"] * 3:
            continue
        later_failures = [
            i for i in range(start + 3, len(rows)) if rows[i] == "stress-fail"
        ]
        if not later_failures:
            continue
        first_failure = later_failures[0]
        if "inconclusive" in rows[start + 3 : first_failure]:
            continue
        if "all-cell-stable" not in rows[first_failure + 1 :]:
            return "n0-noise-stability-window-bracketed"
    return "n0-inconclusive"
