"""Reproduce dimension diagnostics over N from matched scalar endpoints."""

from __future__ import annotations

import argparse
from datetime import UTC, datetime
import json
import math
import os
from pathlib import Path
import subprocess
from typing import Any

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def _repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("repository root not found")


ROOT = _repo_root()

CHECKPOINTS = {
    200_000: "raw_memory_snapshot_pilot_Aatt35_N200k_d10_seed1-3_2026-07-15",
    1_000_000: "beta_zero_reference_Aatt_35_N1M_d10_seed1-5_eps1em4_2026-07-14",
    3_000_000: "raw_memory_snapshot_retest_Aatt35_N3M_d10_seed1-5_2026-07-16",
    10_000_000: "Aatt_sweep_d10_N10M_Aatt_35_seed1-5_eps1em4_2026-07-14",
    30_000_000: (
        "ambient_dim_memory_shape_Aatt_35_N30M_d10_seed1-5_eps1em4_2026-07-13"
    ),
    300_000_000: (
        "ambient_dim_memory_shape_Aatt_35_N300M_d10_seed1-5_eps1em4_"
        "foreground_2026-07-14"
    ),
}

CONFIG_KEYS = (
    "dim",
    "epsilon",
    "eta",
    "alpha",
    "memory_mass",
    "deposition_kernel",
    "deposition_sigma",
    "sigma_rep",
    "sigma_att",
    "amplitude_rep",
    "amplitude_att",
    "memory_factor",
    "max_memory",
)


def _parse_seeds(value: str) -> list[int]:
    seeds = [int(item.strip()) for item in value.split(",") if item.strip()]
    if not seeds or any(seed < 0 for seed in seeds):
        raise argparse.ArgumentTypeError("expected non-negative comma-separated seeds")
    return seeds


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Reproduce D_cov, D_occ, automatic D_win, and D_mem over N for "
            "the matched d=10, A_att=35 endpoint ensemble."
        )
    )
    parser.add_argument(
        "--data-root",
        type=Path,
        default=Path("data/processed/long_run_metastability"),
    )
    parser.add_argument(
        "--seeds",
        type=_parse_seeds,
        default=_parse_seeds("1,2,3"),
        help="Matched seeds available at every checkpoint.",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("reports/dimensions/dimension_over_n_d10_A35_2026-07-30.md"),
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=Path(
            "reports/dimensions/dimension_over_n_d10_A35_summary_2026-07-30.json"
        ),
    )
    parser.add_argument(
        "--figure",
        type=Path,
        default=Path(
            "figures/draft/dimensions/dimension_over_n_2026-07-30/"
            "dimension_over_n_d10_A35.png"
        ),
    )
    return parser.parse_args(argv)


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def _relative_link(source: Path, target: Path) -> str:
    return Path(os.path.relpath(target.resolve(), source.resolve().parent)).as_posix()


def _git_output(args: list[str]) -> str:
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=ROOT,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except (OSError, subprocess.CalledProcessError):
        return "unavailable"
    return completed.stdout.strip()


def _finite(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def _load_case(
    data_root: Path,
    *,
    folder: str,
    seed: int,
    steps: int,
) -> dict[str, Any]:
    path = data_root / folder / f"case_baseline_seed{seed}_steps{steps}.json"
    if not path.exists():
        raise FileNotFoundError(path)
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("condition") != "baseline" or int(payload.get("seed", -1)) != seed:
        raise ValueError(f"case identity mismatch: {path}")
    if int(payload.get("config", {}).get("steps", -1)) != steps:
        raise ValueError(f"step count mismatch: {path}")
    return payload


def _config_signature(config: dict[str, Any]) -> dict[str, Any]:
    return {key: config.get(key) for key in CONFIG_KEYS}


def _row(payload: dict[str, Any], *, steps: int, seed: int) -> dict[str, Any]:
    diagnostics = payload["diagnostics"]
    scaling_window = diagnostics["occupancy"]["scaling_window"]
    return {
        "steps": int(steps),
        "seed": int(seed),
        "sample_every": int(payload["config"]["sample_every"]),
        "sample_count": int(diagnostics["n_samples"]),
        "D_cov": _finite(diagnostics["sample_shape"]["effective_dimension"]),
        "D_occ": _finite(diagnostics.get("occupancy_dimension")),
        "D_win": _finite(scaling_window.get("dimension")),
        "D_win_valid": bool(scaling_window.get("valid_scaling", False)),
        "D_mem": _finite(diagnostics["memory_cloud"]["shape"]["effective_dimension"]),
        "source_git_revision": str(payload.get("git_revision", "unavailable")),
        "source_git_clean": not bool(str(payload.get("git_status", "")).strip()),
    }


def _quantiles(values: list[float | None]) -> dict[str, float | None]:
    finite = np.asarray([value for value in values if value is not None], dtype=float)
    if finite.size == 0:
        return {"median": None, "q1": None, "q3": None}
    return {
        "median": float(np.median(finite)),
        "q1": float(np.quantile(finite, 0.25)),
        "q3": float(np.quantile(finite, 0.75)),
    }


def build_payload(args: argparse.Namespace) -> dict[str, Any]:
    data_root = _resolve(args.data_root)
    rows: list[dict[str, Any]] = []
    reference_signature: dict[str, Any] | None = None
    for steps, folder in sorted(CHECKPOINTS.items()):
        for seed in args.seeds:
            case = _load_case(data_root, folder=folder, seed=seed, steps=steps)
            signature = _config_signature(case["config"])
            if reference_signature is None:
                reference_signature = signature
            elif signature != reference_signature:
                raise ValueError(
                    f"configuration drift at N={steps}, seed={seed}: {signature}"
                )
            rows.append(_row(case, steps=steps, seed=seed))

    summary: list[dict[str, Any]] = []
    for steps in sorted(CHECKPOINTS):
        group = [row for row in rows if row["steps"] == steps]
        item: dict[str, Any] = {
            "steps": int(steps),
            "seed_count": len(group),
            "sample_every": int(group[0]["sample_every"]),
            "sample_count": int(group[0]["sample_count"]),
            "D_win_valid_count": sum(bool(row["D_win_valid"]) for row in group),
        }
        for metric in ("D_cov", "D_occ", "D_win", "D_mem"):
            values = [row[metric] for row in group]
            if metric == "D_win":
                values = [
                    value if row["D_win_valid"] else None
                    for row, value in zip(group, values, strict=True)
                ]
            item[metric] = _quantiles(values)
        summary.append(item)

    memory_medians = np.asarray(
        [item["D_mem"]["median"] for item in summary],
        dtype=float,
    )
    sample_cadences = sorted({int(item["sample_every"]) for item in summary})
    return {
        "question": (
            "How do four existing dimension diagnostics vary with N for the "
            "matched d=10, A_att=35 scalar endpoint ensemble?"
        ),
        "status": "reproduced_with_sampling_caveat",
        "configuration": reference_signature,
        "matched_seeds": args.seeds,
        "checkpoints": sorted(CHECKPOINTS),
        "rows": rows,
        "summary": summary,
        "diagnostics": {
            "D_mem_median_min": float(np.min(memory_medians)),
            "D_mem_median_max": float(np.max(memory_medians)),
            "D_mem_median_range": float(np.ptp(memory_medians)),
            "sample_cadences": sample_cadences,
            "sample_cadence_changes": len(sample_cadences) > 1,
            "late_cadence_ratio": float(
                summary[-1]["sample_every"] / summary[-2]["sample_every"]
            )
            if len(summary) >= 2
            else 1.0,
        },
        "claim_boundaries": {
            "ambient_independent_dimension_selection": False,
            "D_occ_N_only_dependence_established": False,
            "continuous_same_revision_trajectory": False,
            "D_mem_endpoint_shape_reproduced": True,
        },
    }


def _plot_metric(
    ax: Any,
    payload: dict[str, Any],
    metric: str,
    title: str,
    *,
    mark_invalid: bool = False,
) -> None:
    colors = {1: "#2563eb", 2: "#dc2626", 3: "#059669"}
    for seed in payload["matched_seeds"]:
        rows = [row for row in payload["rows"] if row["seed"] == seed]
        x = np.asarray([row["steps"] for row in rows], dtype=float)
        y = np.asarray(
            [row[metric] if row[metric] is not None else np.nan for row in rows],
            dtype=float,
        )
        ax.plot(
            x,
            y,
            color=colors.get(seed, "#555555"),
            alpha=0.42,
            linewidth=1.0,
            marker=".",
            label=f"seed {seed}",
        )
        if mark_invalid and metric == "D_win":
            invalid = np.asarray([not row["D_win_valid"] for row in rows])
            finite = np.isfinite(y)
            ax.scatter(
                x[invalid & finite],
                y[invalid & finite],
                facecolors="none",
                edgecolors=colors.get(seed, "#555555"),
                marker="o",
                s=50,
                linewidths=1.0,
            )

    summary = payload["summary"]
    x = np.asarray([item["steps"] for item in summary], dtype=float)
    med = np.asarray(
        [
            item[metric]["median"] if item[metric]["median"] is not None else np.nan
            for item in summary
        ]
    )
    q1 = np.asarray(
        [
            item[metric]["q1"] if item[metric]["q1"] is not None else np.nan
            for item in summary
        ]
    )
    q3 = np.asarray(
        [
            item[metric]["q3"] if item[metric]["q3"] is not None else np.nan
            for item in summary
        ]
    )
    ax.plot(x, med, color="#111827", linewidth=2.2, marker="o", label="median")
    ax.fill_between(x, q1, q3, color="#6b7280", alpha=0.18, label="IQR")
    ax.axvline(30_000_000, color="#a16207", linestyle=":", linewidth=1.2)
    ax.text(
        35_000_000,
        0.04,
        "sampling 1k -> 10k",
        transform=ax.get_xaxis_transform(),
        fontsize=8,
        color="#854d0e",
    )
    ax.set_xscale("log")
    ax.set_title(title)
    ax.set_xlabel("N updates")
    ax.set_ylabel("dimension estimate")
    ax.grid(True, which="both", alpha=0.22)


def write_figure(payload: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(2, 2, figsize=(12.5, 8.2), sharex=True)
    _plot_metric(axes[0, 0], payload, "D_cov", "Sample covariance dimension")
    _plot_metric(axes[0, 1], payload, "D_occ", "Raw occupancy dimension")
    _plot_metric(
        axes[1, 0],
        payload,
        "D_win",
        "Automatic occupancy-window dimension",
        mark_invalid=True,
    )
    _plot_metric(axes[1, 1], payload, "D_mem", "Memory shape dimension")
    axes[0, 0].legend(frameon=False, fontsize=8, ncol=2)
    axes[1, 0].text(
        0.02,
        0.96,
        "open circle: invalid automatic fit",
        transform=axes[1, 0].transAxes,
        va="top",
        fontsize=8,
    )
    fig.suptitle(
        "Dimension diagnostics over N: d=10, A_att=35, matched seeds 1-3",
        y=1.01,
    )
    fig.tight_layout()
    fig.savefig(path, dpi=220, bbox_inches="tight")
    plt.close(fig)


def _fmt(value: float | None, digits: int = 3) -> str:
    return "n/a" if value is None else f"{value:.{digits}f}"


def render_report(
    payload: dict[str, Any],
    *,
    generated: str,
    figure_link: str,
) -> str:
    lines = [
        "# Dimension Diagnostics over N: d=10, A_att=35",
        "",
        f"Date: {generated}.",
        "",
        "## Question",
        "",
        payload["question"],
        "",
        f"![Dimension diagnostics over N]({figure_link})",
        "",
        "## Matched endpoint set",
        "",
        "- Core parameters are identical at all endpoints.",
        "- Seeds `1,2,3` are present at every endpoint.",
        "- Endpoints: `N={200k,1M,3M,10M,30M,300M}`.",
        "- The source files were produced at several revisions; the 200k source",
        "  records unrelated untracked analysis files. This is an endpoint",
        "  reconciliation, not a single continuously checkpointed run.",
        "- Sampling is every 1,000 updates through `N=30M` and every 10,000 at",
        "  `N=300M`. Therefore `D_cov`, `D_occ`, and `D_win` mix N-dependence",
        "  with sampling-cadence sensitivity at the final point.",
        "",
        "## Summary",
        "",
        "| N | samples | cadence | D_cov | D_occ | D_win | valid D_win | D_mem |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for item in payload["summary"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"{item['steps']:,}",
                    f"{item['sample_count']:,}",
                    f"{item['sample_every']:,}",
                    _fmt(item["D_cov"]["median"]),
                    _fmt(item["D_occ"]["median"]),
                    _fmt(item["D_win"]["median"]),
                    f"{item['D_win_valid_count']}/{item['seed_count']}",
                    _fmt(item["D_mem"]["median"]),
                ]
            )
            + " |"
        )

    diagnostics = payload["diagnostics"]
    lines.extend(
        [
            "",
            "## Reading",
            "",
            f"- Median `D_mem` remains between "
            f"`{diagnostics['D_mem_median_min']:.3f}` and "
            f"`{diagnostics['D_mem_median_max']:.3f}`. This is consistent with",
            "  a near-isotropic cloud in the prescribed ten-dimensional ambient",
            "  space; it is not evidence for selection of three dimensions.",
            "- `D_cov` fluctuates rather than converging monotonically. It describes",
            "  the sampled visible path, not the rank of the memory state.",
            "- Raw `D_occ` and valid `D_win` rise through `N=30M`. Their decrease",
            "  at `N=300M` coincides with the tenfold coarser cadence and cannot be",
            "  assigned to N alone from these files.",
            "- The earliest automatic occupancy fits are invalid. They are shown",
            "  for auditability but must not be interpreted as measured plateaus.",
            "",
            "## Decision",
            "",
            "The earlier qualitative dimension-over-N plot is reproduced, now with",
            "matched seed curves and explicit fit/cadence guards. It does not sharpen",
            "a 3D claim. A discriminating follow-up would use one continuously",
            "checkpointed run with fixed sampling cadence or online covariance/",
            "occupancy accumulators; another endpoint sweep would otherwise repeat",
            "the same sampling ambiguity.",
            "",
            "## Claim boundary",
            "",
            "- No ambient-independent dimension selection is established.",
            "- No N-only law for occupancy dimension is established.",
            "- `D_mem` is a rotation-invariant endpoint-shape diagnostic, not an",
            "  external spacetime dimension.",
            "",
            "## Provenance",
            "",
            f"- Git revision: `{payload['git_revision']}`",
            f"- Git status before generation: `{payload['git_status'] or 'clean'}`",
            "- Script: `experiments/current/dynamics/dimension_over_n_reproduction.py`",
            "",
        ]
    )
    return "\n".join(lines)


def write_outputs(args: argparse.Namespace) -> None:
    report_path = _resolve(args.report)
    summary_path = _resolve(args.summary_json)
    figure_path = _resolve(args.figure)
    payload = build_payload(args)
    payload["generated_utc"] = (
        datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")
    )
    payload["git_revision"] = _git_output(["rev-parse", "HEAD"])
    payload["git_status"] = _git_output(["status", "--short"])
    payload["outputs"] = {
        "report": str(args.report),
        "summary_json": str(args.summary_json),
        "figure": str(args.figure),
    }

    write_figure(payload, figure_path)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        render_report(
            payload,
            generated=payload["generated_utc"],
            figure_link=_relative_link(report_path, figure_path),
        ),
        encoding="utf-8",
    )
    summary_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    write_outputs(parse_args())


if __name__ == "__main__":
    main()
