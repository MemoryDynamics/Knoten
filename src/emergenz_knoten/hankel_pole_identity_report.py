"""Run and report the preregistered stored-pole identity audit."""

from __future__ import annotations

from datetime import UTC, datetime
from itertools import product
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from .hankel_pole_identity import (
    CONTROL_MATCH_MAX,
    DEPTHS,
    MATCH_REQUIRED,
    RANKS,
    RELATIVE_TOLERANCE,
    _fit,
    _relative_spread,
    candidate_poles,
    fit_track,
    seed_clusters,
)


def analyze(payload: dict[str, Any]) -> dict[str, Any]:
    """Apply the rank, depth, seed, correlation, and control gates."""

    sample_interval = float(payload["config"]["alpha"]) * int(
        payload["parameters"]["closure_stride_updates"]
    )
    correlations = sorted({float(row["noise_correlation"]) for row in payload["rows"]})
    seeds = sorted({int(row["future_seed"]) for row in payload["rows"]})
    passing = {corr: {seed: [] for seed in seeds} for corr in correlations}
    rows = []
    for source in payload["rows"]:
        seed = int(source["future_seed"])
        correlation = float(source["noise_correlation"])
        reciprocal = source["conditions"]["retarded_reciprocal"]["hankel_audit"]["base"]
        control = source["conditions"]["retarded_one_way"]["hankel_audit"]["base"]
        anchors = candidate_poles(
            _fit(reciprocal, DEPTHS[-1], RANKS[-1]), sample_interval
        )
        tracks = []
        for anchor in anchors:
            track = fit_track(reciprocal, anchor, sample_interval)
            control_track = fit_track(control, anchor, sample_interval)
            track["control_matching_cells"] = control_track["matching_cells"]
            track["control_identity_pass"] = control_track["identity_pass"]
            tracks.append(track)
            if track["identity_pass"]:
                passing[correlation][seed].append(track)
        best = min(
            tracks,
            key=lambda row: (-row["matching_cells"], row["median_error"]),
            default=None,
        )
        rows.append(
            {
                "future_seed": seed,
                "noise_correlation": correlation,
                "anchor_count": len(anchors),
                "identity_track_count": sum(row["identity_pass"] for row in tracks),
                "best_track": best,
            }
        )

    correlation_rows = []
    for correlation in correlations:
        clusters = seed_clusters(passing[correlation])
        correlation_rows.append(
            {
                "noise_correlation": correlation,
                "candidate_count": len(clusters),
                "control_separated_candidate_count": sum(
                    row["control_separated"] for row in clusters
                ),
                "candidates": clusters,
            }
        )

    cross_correlation = []
    if all(row["candidates"] for row in correlation_rows):
        for selected in product(*(row["candidates"] for row in correlation_rows)):
            comparison = tuple(
                {
                    "median_frequency": row["median_frequency"],
                    "median_damping": row["median_damping"],
                }
                for row in selected
            )
            frequency_spread, damping_spread = _relative_spread(comparison)
            if max(frequency_spread, damping_spread) <= RELATIVE_TOLERANCE:
                cross_correlation.append(
                    {
                        "median_frequency": float(
                            np.median([row["median_frequency"] for row in selected])
                        ),
                        "median_damping": float(
                            np.median([row["median_damping"] for row in selected])
                        ),
                        "frequency_relative_range": frequency_spread,
                        "damping_relative_range": damping_spread,
                        "control_separated": all(
                            row["control_separated"] for row in selected
                        ),
                    }
                )
    passed = any(row["control_separated"] for row in cross_correlation)
    return {
        "schema": "emergenz-knoten.hankel-pole-identity-audit",
        "schema_version": 1,
        "created_utc": datetime.now(UTC).isoformat(timespec="seconds"),
        "source_git_revision": payload["git_revision"],
        "sample_interval_memory_times": sample_interval,
        "registered": {
            "ranks": RANKS,
            "depths": DEPTHS,
            "matching_cells_required": MATCH_REQUIRED,
            "control_matching_cells_max": CONTROL_MATCH_MAX,
            "relative_tolerance": RELATIVE_TOLERANCE,
        },
        "rows": rows,
        "correlations": correlation_rows,
        "cross_correlation_candidate_count": len(cross_correlation),
        "control_separated_cross_correlation_candidate_count": sum(
            row["control_separated"] for row in cross_correlation
        ),
        "classification": (
            "control-separated pole identity candidate"
            if passed
            else "no control-separated pole identity"
        ),
        "pass": passed,
    }


def plot_result(result: dict[str, Any], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    rows = result["rows"]
    correlations = sorted({row["noise_correlation"] for row in rows})
    seeds = sorted({row["future_seed"] for row in rows})
    fig, axes = plt.subplots(2, 2, figsize=(11.5, 8.2))
    for seed in seeds:
        selected = sorted(
            (row for row in rows if row["future_seed"] == seed),
            key=lambda row: row["noise_correlation"],
        )
        reciprocal = [
            row["best_track"]["matching_cells"] if row["best_track"] else 0
            for row in selected
        ]
        control = [
            row["best_track"]["control_matching_cells"] if row["best_track"] else 0
            for row in selected
        ]
        axes[0, 0].plot(correlations, reciprocal, marker="o", label=f"seed {seed}")
        axes[0, 1].plot(correlations, control, marker="o", label=f"seed {seed}")
        axes[1, 0].scatter(reciprocal, control, label=f"seed {seed}")
    axes[0, 0].axhline(MATCH_REQUIRED, color="#D55E00", linestyle="--")
    axes[0, 1].axhline(CONTROL_MATCH_MAX, color="#D55E00", linestyle="--")
    axes[1, 0].axvline(MATCH_REQUIRED, color="#D55E00", linestyle="--")
    axes[1, 0].axhline(CONTROL_MATCH_MAX, color="#D55E00", linestyle="--")
    axes[0, 0].set(
        xlabel="node-noise correlation",
        ylabel="best reciprocal matches / 12",
        title="rank-depth pole identity",
    )
    axes[0, 1].set(
        xlabel="node-noise correlation",
        ylabel="same-pole one-way matches / 12",
        title="one-way control overlap",
    )
    axes[1, 0].set(
        xlabel="reciprocal matching cells",
        ylabel="one-way matching cells",
        title="control-separation gate",
    )
    axes[1, 1].axis("off")
    axes[1, 1].text(
        0.04,
        0.80,
        result["classification"],
        fontsize=13,
        fontweight="bold",
        transform=axes[1, 1].transAxes,
    )
    axes[1, 1].text(
        0.04,
        0.60,
        f"cross-correlation candidates: {result['cross_correlation_candidate_count']}\n"
        "control-separated survivors: "
        f"{result['control_separated_cross_correlation_candidate_count']}",
        fontsize=11,
        transform=axes[1, 1].transAxes,
    )
    for axis in axes.ravel()[:3]:
        axis.grid(alpha=0.25)
        axis.legend(fontsize=8)
    fig.suptitle("P3.2 stored-pole identity and control audit")
    fig.tight_layout()
    fig.savefig(output, dpi=180)
    plt.close(fig)
