from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[2]


def _metric_value(row: dict[str, Any], metric: str) -> float:
    value = row.get(metric)
    if isinstance(value, dict):
        value = value.get("mean")
    if value is None:
        return math.nan
    return float(value)


def matrix_for_step(
    summary: list[dict[str, Any]],
    *,
    metric: str,
    condition: str,
    step: int,
    dims: list[int],
    alphas: list[float],
) -> np.ndarray:
    matrix = np.full((len(dims), len(alphas)), np.nan, dtype=float)
    dim_index = {dim: idx for idx, dim in enumerate(dims)}
    alpha_index = {alpha: idx for idx, alpha in enumerate(alphas)}
    for row in summary:
        if row.get("condition") != condition or int(row.get("steps")) != step:
            continue
        dim = int(row["dim"])
        alpha = float(row["alpha"])
        if dim not in dim_index or alpha not in alpha_index:
            continue
        matrix[dim_index[dim], alpha_index[alpha]] = _metric_value(row, metric)
    return matrix


def _format_alpha(alpha: float) -> str:
    return f"{alpha:g}"


def make_heatmap(
    summary: list[dict[str, Any]],
    *,
    metric: str,
    condition: str,
    output_path: Path,
    title: str | None = None,
) -> None:
    dims = sorted({int(row["dim"]) for row in summary if row.get("condition") == condition})
    alphas = sorted({float(row["alpha"]) for row in summary if row.get("condition") == condition})
    steps = sorted({int(row["steps"]) for row in summary if row.get("condition") == condition})
    if not dims or not alphas or not steps:
        raise ValueError(f"no rows for condition={condition!r}")

    ncols = len(steps)
    fig_width = max(5.0, 4.2 * ncols)
    fig, axes = plt.subplots(1, ncols, figsize=(fig_width, 5.2), squeeze=False)

    matrices = [
        matrix_for_step(
            summary,
            metric=metric,
            condition=condition,
            step=step,
            dims=dims,
            alphas=alphas,
        )
        for step in steps
    ]
    finite_chunks = [m[np.isfinite(m)] for m in matrices if np.isfinite(m).any()]
    if not finite_chunks:
        raise ValueError(f"metric={metric!r} has no finite values")
    finite_values = np.concatenate(finite_chunks)
    vmin = float(np.nanmin(finite_values))
    vmax = float(np.nanmax(finite_values))
    if metric in {"D_occ", "D_occ_reference", "D_cov", "D_spec"}:
        vmin = min(vmin, 0.0)
        vmax = max(vmax, 3.0)

    image = None
    for ax, step, matrix in zip(axes[0], steps, matrices, strict=True):
        image = ax.imshow(matrix, aspect="auto", origin="lower", vmin=vmin, vmax=vmax, cmap="viridis")
        ax.set_title(f"N={step:,}")
        ax.set_xticks(np.arange(len(alphas)))
        ax.set_xticklabels([_format_alpha(alpha) for alpha in alphas], rotation=45, ha="right")
        ax.set_yticks(np.arange(len(dims)))
        ax.set_yticklabels([str(dim) for dim in dims])
        ax.set_xlabel("alpha")
        ax.set_ylabel("embedding dimension d")
        for i, dim in enumerate(dims):
            for j, alpha in enumerate(alphas):
                value = matrix[i, j]
                if math.isfinite(value):
                    color = "white" if value < (vmin + vmax) / 2 else "black"
                    ax.text(j, i, f"{value:.2f}", ha="center", va="center", fontsize=8, color=color)

    assert image is not None
    cbar = fig.colorbar(image, ax=axes.ravel().tolist(), shrink=0.85)
    cbar.set_label(metric)
    if metric in {"D_occ", "D_occ_reference", "D_cov", "D_spec"}:
        cbar.ax.axhline(3.0, color="white", linewidth=1.2)
    fig.suptitle(title or f"{condition}: {metric} over d-alpha-N", y=0.98)
    fig.subplots_adjust(left=0.08, right=0.9, top=0.85, bottom=0.18, wspace=0.32)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=220)
    plt.close(fig)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Plot d-alpha-N intensity maps from reproduce_dimension_pilot JSON."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("data/processed/fractal_analysis/d_alpha_n_pilot.json"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("figures/draft/d_alpha_n_intensity_D_occ.png"),
    )
    parser.add_argument("--metric", default="D_occ", choices=["D_occ", "D_occ_reference", "D_cov", "D_spec"])
    parser.add_argument("--condition", default="baseline")
    parser.add_argument("--title", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_path = args.input if args.input.is_absolute() else ROOT / args.input
    output_path = args.output if args.output.is_absolute() else ROOT / args.output
    payload = json.loads(input_path.read_text(encoding="utf-8"))
    summary = payload.get("summary")
    if not isinstance(summary, list):
        raise SystemExit("input JSON does not contain a list field named 'summary'")
    make_heatmap(
        summary,
        metric=args.metric,
        condition=args.condition,
        output_path=output_path,
        title=args.title,
    )
    print(f"wrote {output_path}")


if __name__ == "__main__":
    main()

