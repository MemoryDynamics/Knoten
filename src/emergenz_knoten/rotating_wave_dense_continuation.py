"""Dense scalar continuation for reconstructible rotating-wave summaries.

The historical ``run_continuation`` implementation is frozen by earlier
experiment provenance.  This module keeps that routine untouched and exposes
the smallest single-pass extension needed by the G5 v2 record: one scalar
quotient distance for every computed step in addition to the sparse readable
sample trace.
"""

from __future__ import annotations

import math
from typing import Any

import numpy as np

from .rotating_wave_stability import (
    co_rotating_fifo_step,
    rotation_translation_quotient_distance,
)
from .rotating_wave_stability_gate import (
    RotatingWaveCandidate,
    StabilityThresholds,
)


def run_dense_continuation(
    name: str,
    perturbation: np.ndarray,
    history: np.ndarray,
    reference_norm: float,
    candidate: RotatingWaveCandidate,
    thresholds: StabilityThresholds,
) -> dict[str, Any]:
    """Run one continuation while retaining every scalar quotient distance."""

    state = history + perturbation
    distance, phase = rotation_translation_quotient_distance(
        state,
        history,
        alpha=candidate.alpha,
        memory_mass=candidate.memory_mass,
    )
    initial_distance = distance
    maximum_distance = distance
    distance_trace = [distance]
    trace = [{"step": 0, "distance": distance, "alignment_phase": phase}]
    stop_radius = thresholds.stopping_radius_fraction * reference_norm
    stopped = False
    stop_reason = "completed"
    final_step = 0
    for step in range(1, thresholds.continuation_steps + 1):
        state = co_rotating_fifo_step(
            state,
            theta=candidate.theta,
            **candidate.step_parameters(),
        )
        distance, phase = rotation_translation_quotient_distance(
            state,
            history,
            alpha=candidate.alpha,
            memory_mass=candidate.memory_mass,
        )
        distance_trace.append(distance)
        maximum_distance = max(maximum_distance, distance)
        final_step = step
        if step % thresholds.sample_every == 0:
            trace.append(
                {
                    "step": step,
                    "distance": distance,
                    "alignment_phase": phase,
                }
            )
        if not math.isfinite(distance):
            stopped = True
            stop_reason = "nonfinite-distance"
            break
        if name != "exact" and distance > stop_radius:
            stopped = True
            stop_reason = "registered-stopping-radius"
            break
    if trace[-1]["step"] != final_step:
        trace.append(
            {
                "step": final_step,
                "distance": distance,
                "alignment_phase": phase,
            }
        )
    growth_factor = (
        maximum_distance / initial_distance if initial_distance > 0.0 else None
    )
    final_ratio = distance / initial_distance if initial_distance > 0.0 else None
    return {
        "name": name,
        "initial_distance": initial_distance,
        "maximum_distance": maximum_distance,
        "final_distance": distance,
        "growth_factor": growth_factor,
        "final_ratio": final_ratio,
        "stopped": stopped,
        "stop_reason": stop_reason,
        "final_step": final_step,
        "distance_trace": distance_trace,
        "trace": trace,
    }
