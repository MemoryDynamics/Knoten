"""Apply the preregistered identity gate to stored reduced DMD poles."""

from __future__ import annotations

from itertools import combinations, product
import math
from typing import Any

import numpy as np


RANKS = (8, 16, 32)
DEPTHS = (100, 150, 200, 250)
MATCH_REQUIRED = 10
CONTROL_MATCH_MAX = 5
RELATIVE_TOLERANCE = 0.25
DAMPING_FLOOR = 0.05
MIN_FREQUENCY = 0.05
MAX_DAMPING = 1.0


def _fit(audits: list[dict[str, Any]], depth: int, rank: int) -> dict[str, Any]:
    audit = next(row for row in audits if int(row["delay_depth"]) == depth)
    return next(row for row in audit["rank_fits"] if int(row["retained_rank"]) == rank)


def candidate_poles(
    fit: dict[str, Any], sample_interval: float
) -> list[dict[str, float]]:
    """Return one member of each registered stable complex conjugate pair."""

    result = []
    for encoded in fit["eigenvalues"]:
        value = complex(float(encoded["real"]), float(encoded["imag"]))
        if value.imag <= 1e-8 or not 0.0 < abs(value) < 1.0:
            continue
        frequency = abs(math.atan2(value.imag, value.real)) / sample_interval
        damping = -math.log(abs(value)) / sample_interval
        if frequency >= MIN_FREQUENCY and damping <= MAX_DAMPING:
            result.append({"frequency": frequency, "damping": damping})
    return result


def _relative_errors(
    anchor: dict[str, float], candidate: dict[str, float]
) -> tuple[float, float]:
    frequency = abs(candidate["frequency"] - anchor["frequency"]) / anchor["frequency"]
    damping = abs(candidate["damping"] - anchor["damping"]) / max(
        anchor["damping"], DAMPING_FLOOR
    )
    return frequency, damping


def fit_track(
    audits: list[dict[str, Any]],
    anchor: dict[str, float],
    sample_interval: float,
) -> dict[str, Any]:
    """Match one fixed anchor across the preregistered rank-depth grid."""

    matches = []
    for depth, rank in product(DEPTHS, RANKS):
        eligible = []
        for candidate in candidate_poles(_fit(audits, depth, rank), sample_interval):
            frequency_error, damping_error = _relative_errors(anchor, candidate)
            if max(frequency_error, damping_error) <= RELATIVE_TOLERANCE:
                eligible.append(
                    (
                        max(frequency_error, damping_error),
                        candidate,
                        frequency_error,
                        damping_error,
                    )
                )
        if eligible:
            _, candidate, frequency_error, damping_error = min(
                eligible, key=lambda row: row[0]
            )
            matches.append(
                {
                    "depth": depth,
                    "rank": rank,
                    **candidate,
                    "frequency_error": frequency_error,
                    "damping_error": damping_error,
                }
            )
    identity_pass = bool(
        len(matches) >= MATCH_REQUIRED
        and {row["rank"] for row in matches} == set(RANKS)
        and {row["depth"] for row in matches} == set(DEPTHS)
    )
    return {
        "anchor_frequency": anchor["frequency"],
        "anchor_damping": anchor["damping"],
        "matching_cells": len(matches),
        "median_frequency": (
            float(np.median([row["frequency"] for row in matches]))
            if matches
            else math.nan
        ),
        "median_damping": (
            float(np.median([row["damping"] for row in matches]))
            if matches
            else math.nan
        ),
        "median_error": (
            float(
                np.median(
                    [
                        max(row["frequency_error"], row["damping_error"])
                        for row in matches
                    ]
                )
            )
            if matches
            else math.inf
        ),
        "identity_pass": identity_pass,
        "matches": matches,
    }


def _relative_spread(rows: tuple[dict[str, Any], ...]) -> tuple[float, float]:
    frequencies = [row["median_frequency"] for row in rows]
    dampings = [row["median_damping"] for row in rows]
    frequency = (max(frequencies) - min(frequencies)) / float(np.median(frequencies))
    damping = (max(dampings) - min(dampings)) / max(
        float(np.median(dampings)), DAMPING_FLOOR
    )
    return frequency, damping


def seed_clusters(
    tracks_by_seed: dict[int, list[dict[str, Any]]],
) -> list[dict[str, Any]]:
    """Find pole identities shared by at least two independent seeds."""

    seeds = sorted(tracks_by_seed)
    result = []
    for size in range(len(seeds), 1, -1):
        for selected_seeds in combinations(seeds, size):
            choices = [tracks_by_seed[seed] for seed in selected_seeds]
            if any(not rows for rows in choices):
                continue
            for selected in product(*choices):
                frequency_spread, damping_spread = _relative_spread(selected)
                if max(frequency_spread, damping_spread) > RELATIVE_TOLERANCE:
                    continue
                control_separated = sum(
                    row["control_matching_cells"] <= CONTROL_MATCH_MAX
                    for row in selected
                )
                result.append(
                    {
                        "seeds": list(selected_seeds),
                        "median_frequency": float(
                            np.median([row["median_frequency"] for row in selected])
                        ),
                        "median_damping": float(
                            np.median([row["median_damping"] for row in selected])
                        ),
                        "frequency_relative_range": frequency_spread,
                        "damping_relative_range": damping_spread,
                        "control_separated_seed_count": control_separated,
                        "control_separated": bool(
                            control_separated / len(selected) >= 2.0 / 3.0
                        ),
                    }
                )
    return sorted(
        result,
        key=lambda row: (
            -len(row["seeds"]),
            max(row["frequency_relative_range"], row["damping_relative_range"]),
        ),
    )
