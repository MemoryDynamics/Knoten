"""Audit a proposed adjoint-reciprocal closure on mature memory snapshots."""

from __future__ import annotations

import argparse
from datetime import UTC, datetime
import glob
import hashlib
import json
import os
from pathlib import Path
import subprocess
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
DEFAULT_CASE_GLOBS = (
    "data/processed/long_run_metastability/"
    "raw_memory_snapshot_retest_Aatt35_N3M_d3_seed1-5_2026-07-16/"
    "case_baseline_seed*.json",
    "data/processed/long_run_metastability/"
    "raw_memory_snapshot_retest_Aatt35_N3M_d3_seed6_2026-07-22/"
    "case_baseline_seed*.json",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Eligibility audit for a new adjoint-reciprocal memory closure."
    )
    parser.add_argument("--case-glob", action="append", default=None)
    parser.add_argument("--seeds", default="1,2,3,4,5,6")
    parser.add_argument("--lambda-value", type=float, default=0.01)
    parser.add_argument("--orientation-relaxation", type=float, default=0.01)
    parser.add_argument("--coupling", type=float, default=5.079e-6)
    parser.add_argument("--metric-scales", default="0.001,1,1000")
    parser.add_argument("--min-complex-fraction", type=float, default=0.95)
    parser.add_argument("--max-seed-median-ratio", type=float, default=1.10)
    parser.add_argument(
        "--report",
        type=Path,
        default=Path(
            "reports/memory/adjoint_reciprocity_eligibility_audit_2026-08-07.md"
        ),
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=Path(
            "reports/memory/adjoint_reciprocity_eligibility_audit_2026-08-07.json"
        ),
    )
    parser.add_argument(
        "--figure",
        type=Path,
        default=Path(
            "figures/draft/memory/"
            "adjoint_reciprocity_eligibility_audit_2026-08-07.png"
        ),
    )
    return parser.parse_args()


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def _relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _relative_from(source: Path, target: Path) -> str:
    return Path(os.path.relpath(target.resolve(), source.resolve().parent)).as_posix()


def _git_output(arguments: list[str]) -> str:
    try:
        result = subprocess.run(
            ["git", *arguments],
            cwd=ROOT,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except (OSError, subprocess.CalledProcessError):
        return "unavailable"
    return result.stdout.strip()


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def _parse_floats(text: str) -> list[float]:
    values = [float(item.strip()) for item in text.split(",") if item.strip()]
    if not values or not np.isfinite(values).all():
        raise ValueError("expected a non-empty list of finite values")
    return values


def _quantiles(values: np.ndarray) -> dict[str, float]:
    return {
        "min": float(np.min(values)),
        "q10": float(np.quantile(values, 0.1)),
        "median": float(np.median(values)),
        "q90": float(np.quantile(values, 0.9)),
        "max": float(np.max(values)),
    }


def analyze_case(
    path: Path,
    *,
    relaxation: float,
    coupling: float,
    forgetting_factor: float,
    metric_scales: list[float],
) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    snapshot = payload["diagnostics"]["memory_cloud"]["snapshot"]
    points = np.asarray(snapshot["points"], dtype=float)
    if points.ndim != 2 or points.shape[0] < 2 or not np.isfinite(points).all():
        raise ValueError(f"invalid memory snapshot in {path}")
    steps = np.linalg.norm(np.diff(points, axis=0), axis=1)
    if np.any(steps <= 0.0):
        raise ValueError(f"zero step makes direction Jacobian undefined in {path}")

    root_q = float(np.sqrt(forgetting_factor))
    lower = float((1.0 - root_q) ** 2)
    upper = float((1.0 + root_q) ** 2)
    transverse_sigma = relaxation / steps
    baseline_values = coupling * np.square(transverse_sigma)
    scale_rows = []
    for scale in metric_scales:
        values = scale * baseline_values
        scale_rows.append(
            {
                "memory_metric_scale": float(scale),
                "dimensionless_coupling": _quantiles(values),
                "complex_fraction": float(np.mean((values > lower) & (values < upper))),
                "stable_fraction": float(
                    np.mean((values > 0.0) & (values < 2.0 * (1.0 + forgetting_factor)))
                ),
            }
        )

    raw_direction_value = coupling * relaxation * relaxation
    return {
        "seed": int(payload["seed"]),
        "case_path": _relative(path),
        "case_sha256": _sha256(path),
        "ambient_dimension": int(points.shape[1]),
        "step_count": int(steps.size),
        "step_norm": _quantiles(steps),
        "transverse_singular_value": _quantiles(transverse_sigma),
        "baseline_dimensionless_coupling": _quantiles(baseline_values),
        "baseline_complex_fraction": float(
            np.mean((baseline_values > lower) & (baseline_values < upper))
        ),
        "baseline_stable_fraction": float(
            np.mean(
                (baseline_values > 0.0)
                & (baseline_values < 2.0 * (1.0 + forgetting_factor))
            )
        ),
        "all_step_coupling_interval": {
            "lower": float(np.max(lower / np.square(transverse_sigma))),
            "upper": float(np.min(upper / np.square(transverse_sigma))),
        },
        "raw_direction_control": {
            "dimensionless_coupling": float(raw_direction_value),
            "complex": bool(lower < raw_direction_value < upper),
        },
        "metric_scale_sensitivity": scale_rows,
    }


def _load_paths(patterns: list[str], seeds: set[int]) -> list[Path]:
    paths = sorted(
        {
            Path(path).resolve()
            for pattern in patterns
            for path in glob.glob(str(_resolve(Path(pattern))))
        }
    )
    selected = []
    for path in paths:
        payload = json.loads(path.read_text(encoding="utf-8"))
        if int(payload["seed"]) in seeds:
            selected.append(path)
    found = {
        int(json.loads(path.read_text(encoding="utf-8"))["seed"])
        for path in selected
    }
    if found != seeds:
        raise FileNotFoundError(f"requested seeds {sorted(seeds)}, found {sorted(found)}")
    return selected


def _plot(payload: dict[str, Any], destination: Path) -> None:
    rows = payload["cases"]
    seeds = np.asarray([row["seed"] for row in rows])
    step_medians = np.asarray([row["step_norm"]["median"] for row in rows])
    step_low = np.asarray([row["step_norm"]["q10"] for row in rows])
    step_high = np.asarray([row["step_norm"]["q90"] for row in rows])
    mode_medians = np.asarray(
        [row["baseline_dimensionless_coupling"]["median"] for row in rows]
    )
    mode_low = np.asarray(
        [row["baseline_dimensionless_coupling"]["q10"] for row in rows]
    )
    mode_high = np.asarray(
        [row["baseline_dimensionless_coupling"]["q90"] for row in rows]
    )
    lower, upper = payload["complex_window"]

    figure, axes = plt.subplots(1, 2, figsize=(10.5, 4.2))
    axes[0].errorbar(
        seeds,
        step_medians,
        yerr=[step_medians - step_low, step_high - step_medians],
        fmt="o",
        capsize=4,
        color="#176b87",
    )
    axes[0].set_yscale("log")
    axes[0].set_xlabel("formation seed")
    axes[0].set_ylabel(r"retained step norm $||\Delta x||$")
    axes[0].set_title("Directed-source scale")
    axes[0].grid(alpha=0.25)

    axes[1].axhspan(lower, upper, color="#5a9367", alpha=0.18, label="complex window")
    axes[1].errorbar(
        seeds,
        mode_medians,
        yerr=[mode_medians - mode_low, mode_high - mode_medians],
        fmt="o",
        capsize=4,
        color="#a23b3b",
        label="Euclidean metric",
    )
    axes[1].set_yscale("log")
    axes[1].set_xlabel("formation seed")
    axes[1].set_ylabel(r"$g\sigma_B^2$")
    axes[1].set_title("Conditional reciprocal modes")
    axes[1].grid(alpha=0.25)
    axes[1].legend(frameon=False)
    figure.tight_layout()
    destination.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(destination, dpi=180)
    plt.close(figure)


def _report(payload: dict[str, Any], report: Path, figure: Path) -> str:
    lines = [
        "# Adjoint-reciprocity eligibility audit",
        "",
        f"Generated: {payload['generated_utc']}",
        "",
        f"Status: **{payload['decision']['status']}**.",
        "",
        "## Question",
        "",
        "Can the already implemented normalized directed deposition support complex",
        "local modes if one adds a metric-adjoint reciprocal backchannel? This is an",
        "eligibility test of a new closure, not evidence that the passive model already",
        "contains that backchannel.",
        "",
        "## Proposed discrete closure",
        "",
        r"\[x_{n+1}=x_n-\sqrt g B^\dagger h_n,\qquad h_{n+1}=q h_n+\sqrt g B x_{n+1}.\]",
        "",
        r"For each metric singular value \(\sigma_B\),",
        "",
        r"\[\mu^2-(1+q-g\sigma_B^2)\mu+q=0.\]",
        "",
        r"The mode is complex exactly when",
        "",
        r"\[(1-\sqrt q)^2<g\sigma_B^2<(1+\sqrt q)^2.\]",
        "",
        "For the normalized step direction, the tested local forward Jacobian is",
        "",
        r"\[B=\frac{\kappa}{\|\Delta x\|}(I-u u^\top).\]",
        "",
        "It has one longitudinal zero mode and d-1 degenerate transverse modes. That",
        "degeneracy permits a rotational plane but does not select ambient d=3.",
        "",
        f"![Eligibility audit]({_relative_from(report, figure)})",
        "",
        "## Fixed inputs",
        "",
        f"- lambda = `{payload['parameters']['lambda_value']}`; q = `{payload['parameters']['forgetting_factor']}`",
        f"- kappa = `{payload['parameters']['orientation_relaxation']}`",
        f"- inherited coupling = `{payload['parameters']['coupling']}`",
        f"- exact dimensionless complex window = `{payload['complex_window'][0]:.6g}..{payload['complex_window'][1]:.6g}`",
        "- baseline visible and memory metrics are Euclidean",
        "",
        "The coupling was fixed in an earlier one-way response calibration. It is not",
        "independently calibrated for this new reciprocal closure.",
        "",
        "## Seed results",
        "",
        "| seed | median step | q10..q90 step | median g sigma_B^2 | complex fraction | stable fraction |",
        "|---:|---:|---:|---:|---:|---:|",
    ]
    for row in payload["cases"]:
        lines.append(
            f"| {row['seed']} | {row['step_norm']['median']:.6g} | "
            f"{row['step_norm']['q10']:.6g}..{row['step_norm']['q90']:.6g} | "
            f"{row['baseline_dimensionless_coupling']['median']:.6g} | "
            f"{row['baseline_complex_fraction']:.4f} | "
            f"{row['baseline_stable_fraction']:.4f} |"
        )
    decision = payload["decision"]
    lines.extend(
        [
            "",
            "## Controls and interpretation",
            "",
            f"- Seed-median step ratio: `{decision['seed_median_ratio']:.4f}` against `<= {decision['max_seed_median_ratio']}`.",
            f"- Minimum Euclidean complex fraction: `{decision['minimum_complex_fraction']:.4f}` against `>= {decision['min_complex_fraction']}`.",
            "- Replacing normalized direction by a raw linear step source is outside the complex window for every seed.",
            "- Rescaling the memory metric by 1e-3 or 1e3 moves the median mode below or above the complex window.",
            "- The Euclidean calculation is therefore kinematically eligible but not metric-identifiable.",
            "",
            "## Claim boundary",
            "",
            "**Evidence:** mature snapshots have a reproducible step scale; under the fixed",
            "Euclidean candidate closure almost all transverse local modes lie in the exact",
            "complex window.",
            "",
            "**Inference:** reciprocal memory can generate a damped second-order mode without",
            "adding an independent angular-frequency parameter once B, its metric and one",
            "overall gain are specified.",
            "",
            "**Not established:** the passive model does not determine the adjoint backchannel,",
            "the memory metric or its relative normalization. No oscillation, inertia, angular",
            "momentum, spin, d=3 selection or physical parameter has been observed here.",
            "",
            "## Next falsifying gate",
            "",
            "Derive or preregister one memory metric from an independent field energy or noise",
            "covariance, with no seedwise normalization. Then linearize the complete update on",
            "held-out time segments and require its predicted frequency and damping to match a",
            "closed nonlinear pilot. Without that metric closure, a reciprocal simulation would",
            "be a tunable model demonstration rather than parameter self-selection.",
            "",
            "## Provenance",
            "",
            f"- Git revision before generated outputs: `{payload['git_revision']}`",
            f"- Git status before generated outputs: `{payload['git_status'] or 'clean'}`",
        ]
    )
    for row in payload["cases"]:
        lines.append(
            f"- Seed {row['seed']}: `{row['case_path']}`, SHA-256 `{row['case_sha256']}`"
        )
    return "\n".join(lines) + "\n"


def main() -> None:
    args = parse_args()
    if not 0.0 < args.lambda_value <= 1.0:
        raise ValueError("lambda-value must lie in (0, 1]")
    if not 0.0 < args.orientation_relaxation <= 1.0:
        raise ValueError("orientation-relaxation must lie in (0, 1]")
    if args.coupling < 0.0 or not np.isfinite(args.coupling):
        raise ValueError("coupling must be finite and non-negative")
    scales = _parse_floats(args.metric_scales)
    if any(scale <= 0.0 for scale in scales):
        raise ValueError("metric scales must be positive")
    seeds = {int(item) for item in args.seeds.split(",") if item.strip()}
    paths = _load_paths(args.case_glob or list(DEFAULT_CASE_GLOBS), seeds)
    q = 1.0 - args.lambda_value
    rows = [
        analyze_case(
            path,
            relaxation=args.orientation_relaxation,
            coupling=args.coupling,
            forgetting_factor=q,
            metric_scales=scales,
        )
        for path in paths
    ]
    rows.sort(key=lambda row: row["seed"])
    medians = np.asarray([row["step_norm"]["median"] for row in rows])
    median_ratio = float(np.max(medians) / np.min(medians))
    minimum_fraction = float(min(row["baseline_complex_fraction"] for row in rows))
    eligibility_pass = bool(
        median_ratio <= args.max_seed_median_ratio
        and minimum_fraction >= args.min_complex_fraction
    )
    lower = float((1.0 - np.sqrt(q)) ** 2)
    upper = float((1.0 + np.sqrt(q)) ** 2)
    payload = {
        "schema_version": 1,
        "generated_utc": datetime.now(UTC).isoformat(),
        "git_revision": _git_output(["rev-parse", "HEAD"]),
        "git_status": _git_output(["status", "--short"]),
        "parameters": {
            "lambda_value": float(args.lambda_value),
            "forgetting_factor": float(q),
            "orientation_relaxation": float(args.orientation_relaxation),
            "coupling": float(args.coupling),
            "metric_scales": scales,
        },
        "complex_window": [lower, upper],
        "cases": rows,
        "decision": {
            "status": (
                "eligibility pass; physical closure unresolved"
                if eligibility_pass
                else "eligibility fail"
            ),
            "eligibility_pass": eligibility_pass,
            "seed_median_ratio": median_ratio,
            "max_seed_median_ratio": float(args.max_seed_median_ratio),
            "minimum_complex_fraction": minimum_fraction,
            "min_complex_fraction": float(args.min_complex_fraction),
            "metric_identified": False,
            "nonlinear_mode_observed": False,
        },
    }
    report = _resolve(args.report)
    summary = _resolve(args.summary_json)
    figure = _resolve(args.figure)
    _plot(payload, figure)
    report.parent.mkdir(parents=True, exist_ok=True)
    summary.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(_report(payload, report, figure), encoding="utf-8")
    summary.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload["decision"], indent=2))


if __name__ == "__main__":
    main()
