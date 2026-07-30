from __future__ import annotations

import argparse
from datetime import UTC, datetime
import json
import math
import os
from pathlib import Path
import subprocess
import sys
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def _repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("repository root not found")


ROOT = _repo_root()
sys.path.insert(0, str(ROOT / "src"))

from emergenz_knoten.stability import (  # noqa: E402
    checkpoint_stability_diagnostics,
    local_radius_stationarity_diagnostics,
)


CANONICAL_CHECKPOINTS = {
    1_000_000: ("beta_zero_reference_Aatt_35_N1M_d10_seed1-5_eps1em4_2026-07-14"),
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
            "Retrospective checkpoint-plus-holdout stability audit for the "
            "canonical d=10, A_att=35 long-run slice."
        )
    )
    parser.add_argument(
        "--data-root",
        type=Path,
        default=Path("data/processed/long_run_metastability"),
    )
    parser.add_argument("--seeds", type=_parse_seeds, default=_parse_seeds("1,2,3,4,5"))
    parser.add_argument("--local-window-memory-times", type=float, default=20.0)
    parser.add_argument(
        "--report",
        type=Path,
        default=Path(
            "reports/long_runs/stability/"
            "checkpoint_stability_gate_d10_A35_2026-07-30.md"
        ),
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=Path(
            "reports/long_runs/stability/"
            "checkpoint_stability_gate_d10_A35_2026-07-30.json"
        ),
    )
    parser.add_argument(
        "--figure",
        type=Path,
        default=Path(
            "figures/draft/long_runs/stability_2026-07-30/"
            "checkpoint_stability_gate_d10_A35.png"
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


def _load_case(
    data_root: Path, *, folder: str, seed: int, steps: int
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


def _shape(payload: dict[str, Any]) -> dict[str, Any]:
    return payload["diagnostics"]["memory_cloud"]["shape"]


def _trace(payload: dict[str, Any]) -> dict[str, Any]:
    return payload["diagnostics"]["dynamic_center_trace"]["trace"]


def build_payload(args: argparse.Namespace) -> dict[str, Any]:
    if (
        not math.isfinite(args.local_window_memory_times)
        or args.local_window_memory_times <= 0.0
    ):
        raise SystemExit("--local-window-memory-times must be positive")
    data_root = _resolve(args.data_root)
    checkpoint_updates = np.asarray(sorted(CANONICAL_CHECKPOINTS), dtype=float)
    rows: list[dict[str, Any]] = []
    reference_signature: dict[str, Any] | None = None

    for seed in args.seeds:
        cases = [
            _load_case(
                data_root,
                folder=CANONICAL_CHECKPOINTS[int(steps)],
                seed=seed,
                steps=int(steps),
            )
            for steps in checkpoint_updates
        ]
        signatures = [_config_signature(case["config"]) for case in cases]
        if any(signature != signatures[0] for signature in signatures[1:]):
            raise ValueError(f"configuration drift across checkpoints for seed {seed}")
        if reference_signature is None:
            reference_signature = signatures[0]
        elif signatures[0] != reference_signature:
            raise ValueError("configuration drift across seeds")

        shapes = [_shape(case) for case in cases]
        radii = np.asarray([shape["rms_radius"] for shape in shapes], dtype=float)
        eigenvalues = np.asarray(
            [shape["covariance_eigenvalues"] for shape in shapes],
            dtype=float,
        )
        checkpoint_gate = checkpoint_stability_diagnostics(
            checkpoint_updates,
            radii,
            eigenvalues,
        )

        holdout = cases[-1]
        alpha = float(holdout["config"]["alpha"])
        window_updates = int(round(args.local_window_memory_times / alpha))
        trace = _trace(holdout)
        local_gate = local_radius_stationarity_diagnostics(
            trace["steps"],
            trace["rms_radii"],
            window_updates=window_updates,
        )
        provisional = bool(
            checkpoint_gate["checkpoint_stability_pass"]
            and local_gate["local_radius_stationarity_pass"]
        )
        rows.append(
            {
                "seed": int(seed),
                "checkpoint_updates": checkpoint_updates.astype(int).tolist(),
                "checkpoint_radii": radii.tolist(),
                "checkpoint_effective_dimensions": [
                    float(shape["effective_dimension"]) for shape in shapes
                ],
                "checkpoint_gate": checkpoint_gate,
                "local_radius_gate": local_gate,
                "provisional_stability_pass": provisional,
            }
        )

    pass_count = sum(bool(row["provisional_stability_pass"]) for row in rows)
    return {
        "question": (
            "Do four age checkpoints through N=30M predict a stable radius and "
            "rotation-invariant memory shape at an untouched N=300M holdout?"
        ),
        "status": (
            "supported_method_conditional"
            if pass_count == len(rows)
            else "not_supported"
        ),
        "configuration": reference_signature,
        "checkpoint_protocol": {
            "training_updates": checkpoint_updates[:-1].astype(int).tolist(),
            "candidate_update": int(checkpoint_updates[-2]),
            "holdout_update": int(checkpoint_updates[-1]),
            "training_checkpoints": 4,
            "holdout_checkpoints": 1,
            "local_window_memory_times": float(args.local_window_memory_times),
            "local_training_windows": 4,
            "local_holdout_windows": 1,
            "radius_range_limit": 0.10,
            "radius_cv_limit": 0.15,
            "radius_trend_per_decade_limit": 0.05,
            "shape_spectrum_tv_limit": 0.10,
            "minimum_training_span_decades": 1.0,
            "minimum_holdout_factor": 3.0,
        },
        "rows": rows,
        "aggregate": {
            "seed_count": len(rows),
            "checkpoint_pass_count": sum(
                bool(row["checkpoint_gate"]["checkpoint_stability_pass"])
                for row in rows
            ),
            "local_radius_pass_count": sum(
                bool(row["local_radius_gate"]["local_radius_stationarity_pass"])
                for row in rows
            ),
            "provisional_pass_count": pass_count,
            "all_seeds_provisional_pass": pass_count == len(rows),
        },
        "claim_boundaries": {
            "first_formation_time_identified": False,
            "time_resolved_shape_stationarity_measured": False,
            "automatic_early_stopping_validated": False,
            "physical_knot_or_particle_stability_established": False,
            "retrospective_N30M_candidate_confirmed_at_N300M": (
                pass_count == len(rows)
            ),
        },
    }


def _plot(payload: dict[str, Any], output: Path) -> None:
    rows = payload["rows"]
    fig, axes = plt.subplots(2, 2, figsize=(12.8, 8.4))
    colors = plt.get_cmap("tab10")

    for index, row in enumerate(rows):
        updates = np.asarray(row["checkpoint_updates"], dtype=float)
        radii = np.asarray(row["checkpoint_radii"], dtype=float)
        axes[0, 0].plot(
            updates,
            radii,
            marker="o",
            linewidth=1.6,
            color=colors(index),
            label=f"seed {row['seed']}",
        )
    axes[0, 0].axvline(30e6, color="#444444", linestyle="--", label="candidate")
    axes[0, 0].axvline(300e6, color="#c23b22", linestyle=":", label="holdout")
    axes[0, 0].set_xscale("log")
    axes[0, 0].set_title("Memory radius across simulation age")
    axes[0, 0].set_xlabel("updates N")
    axes[0, 0].set_ylabel("memory RMS radius")

    seeds = np.asarray([row["seed"] for row in rows], dtype=int)
    checkpoint_metrics = (
        ("training_radius_relative_range", "training range", "#377eb8", 0.10),
        ("training_radius_trend_per_decade", "trend / decade", "#d06b25", 0.05),
        ("holdout_radius_relative_change", "holdout change", "#147d64", 0.10),
    )
    for key, label, color, _ in checkpoint_metrics:
        axes[0, 1].plot(
            seeds,
            [row["checkpoint_gate"][key] for row in rows],
            marker="o",
            linewidth=1.5,
            color=color,
            label=label,
        )
    axes[0, 1].axhline(0.10, color="#377eb8", linestyle=":", linewidth=1.0)
    axes[0, 1].axhline(0.05, color="#d06b25", linestyle=":", linewidth=1.0)
    axes[0, 1].set_title("Age-checkpoint radius gates")
    axes[0, 1].set_xlabel("seed")
    axes[0, 1].set_ylabel("relative change")

    axes[1, 0].plot(
        seeds,
        [row["checkpoint_gate"]["training_shape_spectrum_tv_max"] for row in rows],
        marker="o",
        label="training max TV",
    )
    axes[1, 0].plot(
        seeds,
        [row["checkpoint_gate"]["holdout_shape_spectrum_tv"] for row in rows],
        marker="s",
        label="holdout TV",
    )
    axes[1, 0].axhline(0.10, color="#c23b22", linestyle=":", label="limit")
    axes[1, 0].set_title("Rotation-invariant memory-shape gate")
    axes[1, 0].set_xlabel("seed")
    axes[1, 0].set_ylabel("total variation")

    for key, label, color, limit in (
        ("training_radius_relative_range", "training range", "#377eb8", 0.10),
        ("training_radius_cv_max", "max within-window CV", "#d06b25", 0.15),
        ("holdout_radius_relative_change", "holdout change", "#147d64", 0.10),
    ):
        axes[1, 1].plot(
            seeds,
            [row["local_radius_gate"][key] for row in rows],
            marker="o",
            linewidth=1.5,
            color=color,
            label=f"{label} (limit {limit:.2f})",
        )
    axes[1, 1].axhline(0.10, color="#377eb8", linestyle=":", linewidth=1.0)
    axes[1, 1].axhline(0.15, color="#d06b25", linestyle=":", linewidth=1.0)
    axes[1, 1].set_title("Final 100-memory-time radius gate")
    axes[1, 1].set_xlabel("seed")
    axes[1, 1].set_ylabel("relative change")

    for axis in axes.flat:
        axis.grid(True, alpha=0.22)
        axis.legend(frameon=False, fontsize=8)
    fig.suptitle("Retrospective stability gate: candidate N=30M, holdout N=300M")
    fig.tight_layout()
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=190)
    plt.close(fig)


def render_report(
    payload: dict[str, Any],
    *,
    generated: str,
    figure_link: str,
) -> str:
    aggregate = payload["aggregate"]
    lines = [
        "# Checkpoint Stability Gate: d=10, A_att=35",
        "",
        f"Date: {generated}.",
        "",
        "## Question",
        "",
        payload["question"],
        "",
        f"![Stability gate]({figure_link})",
        "",
        "## Preregistered-style gate",
        "",
        "- Four age checkpoints: `N={1M,3M,10M,30M}`.",
        "- Untouched late holdout: `N=300M`.",
        "- Radius training range `<=0.10`; radius CV `<=0.15`.",
        "- Absolute radius trend per decade `<=0.05`.",
        "- Rotation-invariant shape-spectrum TV `<=0.10`.",
        "- Final local trace: four 20-memory-time windows plus one holdout.",
        "",
        "The numerical tolerances reuse the existing v0.6 radius and shape limits;",
        "the per-decade trend and separated holdout prevent a slow monotone drift",
        "or a short terminal plateau from being accepted as convergence.",
        "",
        "## Result",
        "",
        f"- status: **{payload['status']}**",
        (
            f"- checkpoint gate: `{aggregate['checkpoint_pass_count']}/"
            f"{aggregate['seed_count']}` seeds"
        ),
        (
            f"- local radius gate: `{aggregate['local_radius_pass_count']}/"
            f"{aggregate['seed_count']}` seeds"
        ),
        (
            f"- provisional combined gate: `{aggregate['provisional_pass_count']}/"
            f"{aggregate['seed_count']}` seeds"
        ),
        "",
        "| seed | train radius range | trend/decade | holdout radius | "
        "train shape TV | holdout shape TV | local range | local max CV | pass |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in payload["rows"]:
        checkpoint = row["checkpoint_gate"]
        local = row["local_radius_gate"]
        lines.append(
            f"| {row['seed']} | "
            f"{checkpoint['training_radius_relative_range']:.4f} | "
            f"{checkpoint['training_radius_trend_per_decade']:.4f} | "
            f"{checkpoint['holdout_radius_relative_change']:.4f} | "
            f"{checkpoint['training_shape_spectrum_tv_max']:.4f} | "
            f"{checkpoint['holdout_shape_spectrum_tv']:.4f} | "
            f"{local['training_radius_relative_range']:.4f} | "
            f"{local['training_radius_cv_max']:.4f} | "
            f"{row['provisional_stability_pass']} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "The existing five-seed slice supports a **retrospective provisional**",
            "statement: a candidate accepted at N=30M remains within the fixed",
            "radius and rotation-invariant endpoint-shape limits at N=300M.",
            "This does not show that formation first occurs at N=30M; it is only",
            "the first fully testable candidate under the available checkpoint",
            "schedule.",
            "",
            "The final contiguous trace spans only 100 memory times and contains",
            "time-resolved radius but no time-resolved shape tensor. It therefore",
            "cannot exclude slower breathing or shape cycles. The result is not yet",
            "an automatic stopping rule and is not evidence for a physical particle.",
            "",
            "## Forward stopping rule",
            "",
            "1. Save resumable states at a geometric schedule such as",
            "   `N0*{1,3,10,30,100,...}` without changing parameters.",
            "2. At every checkpoint record a contiguous monitoring block with",
            "   radius and normalized shape eigenvalues.",
            "3. Declare a candidate only after four checkpoints spanning at least",
            "   one decade pass the fixed radius, trend, and shape limits.",
            "4. Continue the same seed to a holdout at least three times later.",
            "5. Stop that seed only if both the age holdout and a local",
            "   radius-plus-shape window gate pass; otherwise extend it.",
            "6. Report every planned seed. A parameter-set claim requires the rule",
            "   to pass seedwise, not only after pooling.",
            "",
            "## Claim boundary",
            "",
            "- No first-formation time is identified.",
            "- No time-resolved shape stationarity is established by the legacy data.",
            "- No metastable attractor, particle stability, or dimension selection",
            "  follows from this gate.",
            "",
            "## Provenance",
            "",
            f"- Git revision: `{payload['git_revision']}`",
            f"- Git status before generation: `{payload['git_status'] or 'clean'}`",
            "- Script: `experiments/current/dynamics/stability_gate_audit.py`",
        ]
    )
    return "\n".join(lines) + "\n"


def write_outputs(args: argparse.Namespace) -> None:
    payload = build_payload(args)
    report = _resolve(args.report)
    summary = _resolve(args.summary_json)
    figure = _resolve(args.figure)
    generated = datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")
    payload["generated_utc"] = generated
    payload["git_revision"] = _git_output(["rev-parse", "HEAD"])
    payload["git_status"] = _git_output(["status", "--porcelain"])
    payload["outputs"] = {
        "report": str(args.report),
        "summary_json": str(args.summary_json),
        "figure": str(args.figure),
    }

    _plot(payload, figure)
    report.parent.mkdir(parents=True, exist_ok=True)
    summary.parent.mkdir(parents=True, exist_ok=True)
    summary.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    report.write_text(
        render_report(
            payload,
            generated=generated,
            figure_link=_relative_link(report, figure),
        ),
        encoding="utf-8",
    )


def main() -> None:
    write_outputs(parse_args())


if __name__ == "__main__":
    main()
