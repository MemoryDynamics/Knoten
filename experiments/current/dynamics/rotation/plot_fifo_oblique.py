"""Render saved attempt-1 shape observations; never execute a trajectory."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np


ROOT = Path(__file__).resolve().parents[4]
DIRECTORY = ROOT / "reports/dynamics/rotation/fifo_normal_anchor_attempt_1_2026-10-25"


def main() -> None:
    record = json.loads((DIRECTORY / "panel_80.json").read_text(encoding="utf-8"))
    probe = record["result"]["oblique_probe"]
    if record["status"] != "completed" or probe["status"] != "completed":
        raise ValueError("completed saved probe required")
    result = probe["result"]
    steps = np.asarray(result["sample_steps"])
    angles = result["settings"]["angles_degrees"]
    expected = [(angle, sign) for angle in angles for sign in (-1, 1)]
    if [(arm["angle_degrees"], arm["sign"]) for arm in result["arms"]] != expected:
        raise ValueError("incomplete saved arms")
    colors = dict(
        zip(
            angles, ["#343434", "#0072B2", "#009E73", "#D55E00", "#8B4E9F"], strict=True
        )
    )
    fig, ax = plt.subplots(figsize=(8.8, 5.2), layout="constrained")
    for arm in result["arms"]:
        values = np.asarray(arm["distances"], dtype=float) / arm["initial_distance"]
        if len(values) != len(steps) or not np.all(np.isfinite(values) & (values > 0)):
            raise ValueError("invalid saved shape observations")
        if not np.isclose(values[0], 1) or not np.isclose(
            values[-1], arm["final_ratio"]
        ):
            raise ValueError("inconsistent saved ratios")
        ax.semilogy(
            steps,
            values,
            color=colors[arm["angle_degrees"]],
            linestyle="--" if arm["sign"] < 0 else "-",
            linewidth=1.8,
            alpha=0.85,
        )
    handles = [
        Line2D([], [], color=colors[angle], label=f"{angle} deg") for angle in angles
    ]
    handles += [
        Line2D([], [], color="#555555", linestyle=style, label=f"sign {sign}")
        for style, sign in (("-", "+"), ("--", "-"))
    ]
    ax.legend(handles=handles, loc="lower left", ncol=2, fontsize=9, framealpha=0.95)
    ax.axhline(1, color="#888888", linewidth=0.8, zorder=0)
    ax.set(
        xlim=(0, 2000),
        xlabel="FIFO updates n (2000 updates = alpha*n of 20)",
        ylabel="Shape RMS / initial shape RMS",
        title="Prepared H=1200 circle: finite-window shape response",
    )
    ax.grid(axis="y", which="major", color="#DDDDDD", linewidth=0.6)
    ax.spines[["top", "right"]].set_visible(False)
    fig.savefig(DIRECTORY / "shape_response.png", dpi=160)
    plt.close(fig)


if __name__ == "__main__":
    main()
