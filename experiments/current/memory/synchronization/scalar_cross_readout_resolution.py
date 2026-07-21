"""Audit whether an independent scalar cross-readout resolves knot shape."""

from __future__ import annotations

import argparse
from datetime import UTC, datetime
import json
import os
from pathlib import Path
import subprocess
from typing import Any, Iterable

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from emergenz_knoten import (
    FiniteMemoryState,
    ScalarReadoutKernel,
    SimulationConfig,
    calibrate_frozen_source_cross_eta,
    double_gaussian_gradient,
    load_finite_memory_checkpoint,
    memory_centroid,
    memory_shape_tensor,
    place_finite_memory_state,
)


def _repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("repository root not found")


ROOT = _repo_root()
DEFAULT_CHECKPOINT_DIR = Path(
    "data/processed/reference_states/scalar_Aatt35_N100M_d3_d10_seed1_2026-07-16"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Resolve frozen-knot shape with an independent scalar readout."
    )
    parser.add_argument("--checkpoint-dir", type=Path, default=DEFAULT_CHECKPOINT_DIR)
    parser.add_argument("--resolution-ratios", default="1000,300,100,30,10,5,3,2.5")
    parser.add_argument("--response-fraction", type=float, default=0.03)
    parser.add_argument("--shape-threshold", type=float, default=0.01)
    parser.add_argument("--minimum-distinctness", type=float, default=1.25)
    parser.add_argument("--allow-dirty", action="store_true")
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("reports/response/scalar_cross_readout_resolution_2026-07-21.md"),
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=Path(
            "reports/response/scalar_cross_readout_resolution_2026-07-21.json"
        ),
    )
    parser.add_argument(
        "--figure",
        type=Path,
        default=Path(
            "figures/draft/response/scalar_cross_readout_resolution_2026-07-21.png"
        ),
    )
    return parser.parse_args()


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def _rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _rel_from(source: Path, target: Path) -> str:
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


def _jsonable(value: Any) -> Any:
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        number = float(value)
        return number if np.isfinite(number) else None
    if isinstance(value, Path):
        return _rel(value)
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    return value


def parse_resolution_ratios(text: str) -> list[float]:
    """Parse unique positive readout widths in units of memory radius."""

    values = [float(part.strip()) for part in text.split(",") if part.strip()]
    if not values or any(not np.isfinite(value) or value <= 0.0 for value in values):
        raise ValueError("resolution ratios must be positive finite values")
    if len(values) != len(set(values)):
        raise ValueError("resolution ratios must not contain duplicates")
    return sorted(values, reverse=True)


def principal_axis_rotations(state: FiniteMemoryState) -> tuple[np.ndarray, np.ndarray]:
    """Map each source principal axis onto the common radial axis."""

    eigenvalues, eigenvectors = np.linalg.eigh(memory_shape_tensor(state))
    rotations = []
    for selected in range(state.dim):
        order = [selected, *(index for index in range(state.dim) if index != selected)]
        rotations.append(eigenvectors[:, order].T)
    return eigenvalues, np.asarray(rotations)


def _source_drift(
    target_x: np.ndarray,
    memory: np.ndarray,
    weights: np.ndarray,
    config: SimulationConfig,
    readout: ScalarReadoutKernel,
) -> np.ndarray:
    return -double_gaussian_gradient(
        target_x,
        memory,
        weights,
        sigma_rep=readout.sigma_rep,
        sigma_att=readout.sigma_att,
        amplitude_rep=readout.amplitude_rep,
        amplitude_att=readout.amplitude_att,
        deposition_kernel=config.deposition_kernel,
        deposition_sigma=config.deposition_sigma,
    )


def evaluate_readout_resolution(
    state: FiniteMemoryState,
    config: SimulationConfig,
    *,
    radius_ratio: float,
    response_fraction: float,
    shape_threshold: float,
    minimum_distinctness: float,
) -> dict[str, Any]:
    """Compare rotated full sources with a matched point-monopole null."""

    if config.deposition_kernel != "delta":
        raise ValueError("resolution audit currently requires delta deposition")
    if radius_ratio <= 0.0 or not np.isfinite(radius_ratio):
        raise ValueError("radius_ratio must be positive and finite")
    shape = memory_shape_tensor(state)
    radius = float(np.sqrt(max(np.trace(shape), 0.0)))
    if radius <= 0.0:
        raise ValueError("memory radius must be positive")
    q = config.sigma_att / config.sigma_rep
    readout = ScalarReadoutKernel(
        sigma_rep=radius_ratio * radius,
        sigma_att=q * radius_ratio * radius,
        amplitude_rep=config.amplitude_rep,
        amplitude_att=config.amplitude_att,
    )
    eigenvalues, rotations = principal_axis_rotations(state)
    radial_axis = np.zeros(state.dim)
    radial_axis[0] = 1.0
    offset = readout.sigma_rep * radial_axis
    source_center = memory_centroid(state) + offset

    drifts = []
    for rotation in rotations:
        placed = place_finite_memory_state(state, source_center, rotation=rotation)
        drifts.append(
            _source_drift(state.x, placed.memory, placed.weights, config, readout)
        )
    drifts_array = np.asarray(drifts)
    point_drift = _source_drift(
        state.x,
        source_center[None, :],
        np.asarray([float(np.sum(state.weights))]),
        config,
        readout,
    )
    point_norm = float(np.linalg.norm(point_drift))
    if point_norm <= np.finfo(float).tiny:
        raise ValueError("point-source drift is too small for a relative audit")
    point_direction = point_drift / point_norm
    pairwise = drifts_array[:, None, :] - drifts_array[None, :, :]
    residuals = drifts_array - point_drift[None, :]
    radial_residuals = residuals @ point_direction
    tangential = residuals - radial_residuals[:, None] * point_direction[None, :]
    orientation_spread = float(np.max(np.linalg.norm(pairwise, axis=2)) / point_norm)
    monopole_errors = np.linalg.norm(residuals, axis=1) / point_norm
    radial_components = drifts_array @ point_direction
    distinctness = float(radius_ratio / 2.0)
    calibration = calibrate_frozen_source_cross_eta(
        state,
        state,
        config,
        source_center_offset=offset,
        response_fraction=response_fraction,
        pulse_steps=max(1, int(round(1.0 / config.alpha))),
        cross_readout=readout,
        source_rotation=rotations[0],
    )
    reconstructed_fraction = (
        calibration.cross_eta
        * calibration.baseline_directional_drift
        * calibration.pulse_steps
        / calibration.target_radius
    )
    orientation_response_fraction = (
        calibration.cross_eta
        * float(np.max(np.linalg.norm(pairwise, axis=2)))
        * calibration.pulse_steps
        / calibration.target_radius
    )

    normalized_eigenvalues = eigenvalues / max(float(np.sum(eigenvalues)), 1e-300)
    eligible = distinctness >= minimum_distinctness
    return {
        "dim": state.dim,
        "radius": radius,
        "radius_ratio": float(radius_ratio),
        "sigma_rep": readout.sigma_rep,
        "sigma_att": readout.sigma_att,
        "q": q,
        "separation_over_combined_radius": distinctness,
        "shape_eigenvalues_normalized": normalized_eigenvalues,
        "shape_anisotropy": float(
            normalized_eigenvalues[-1] - normalized_eigenvalues[0]
        ),
        "orientation_spread": orientation_spread,
        "radial_orientation_spread": float(np.ptp(radial_components) / point_norm),
        "monopole_error_median": float(np.median(monopole_errors)),
        "monopole_error_max": float(np.max(monopole_errors)),
        "tangential_residual_max": float(
            np.max(np.linalg.norm(tangential, axis=1)) / point_norm
        ),
        "point_drift_norm": point_norm,
        "cross_eta": calibration.cross_eta,
        "reconstructed_response_fraction": float(reconstructed_fraction),
        "orientation_response_fraction": float(orientation_response_fraction),
        "eligible_distinctness": eligible,
        "shape_resolved": bool(eligible and orientation_spread >= shape_threshold),
        "finite_source_resolved": bool(
            eligible and float(np.max(monopole_errors)) >= shape_threshold
        ),
    }


def run_resolution_ladder(
    checkpoint_dir: Path,
    *,
    resolution_ratios: Iterable[float],
    response_fraction: float,
    shape_threshold: float,
    minimum_distinctness: float,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    paths = sorted(_resolve(checkpoint_dir).glob("*.npz"))
    if not paths:
        raise ValueError(f"no checkpoints found in {_resolve(checkpoint_dir)}")
    for path in paths:
        checkpoint = load_finite_memory_checkpoint(path)
        state = checkpoint.state
        radius = float(np.sqrt(np.trace(memory_shape_tensor(state))))
        baseline_ratio = checkpoint.config.sigma_rep / radius
        ratios = [baseline_ratio, *resolution_ratios]
        unique_ratios: list[float] = []
        for ratio in ratios:
            if not any(np.isclose(ratio, existing) for existing in unique_ratios):
                unique_ratios.append(float(ratio))
        for ratio in unique_ratios:
            print(f"running d={state.dim}, sigma_rep/R={ratio:.6g}", flush=True)
            row = evaluate_readout_resolution(
                state,
                checkpoint.config,
                radius_ratio=ratio,
                response_fraction=response_fraction,
                shape_threshold=shape_threshold,
                minimum_distinctness=minimum_distinctness,
            )
            row.update(
                {
                    "checkpoint": _rel(path),
                    "seed": checkpoint.formation_seed,
                    "update_index": checkpoint.update_index,
                    "formation_revision": checkpoint.git_revision,
                    "self_readout": bool(np.isclose(ratio, baseline_ratio)),
                }
            )
            rows.append(row)
    return rows


def summarize_cases(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    summaries = []
    for dim in sorted({int(row["dim"]) for row in rows}):
        selected = [row for row in rows if row["dim"] == dim]
        baseline = next(row for row in selected if row["self_readout"])
        shape = [row for row in selected if row["shape_resolved"]]
        finite = [row for row in selected if row["finite_source_resolved"]]
        summaries.append(
            {
                "dim": dim,
                "baseline_ratio": baseline["radius_ratio"],
                "baseline_orientation_spread": baseline["orientation_spread"],
                "shape_onset_ratio": max(
                    (row["radius_ratio"] for row in shape), default=None
                ),
                "finite_source_onset_ratio": max(
                    (row["radius_ratio"] for row in finite), default=None
                ),
                "maximum_orientation_spread": max(
                    row["orientation_spread"] for row in selected
                ),
            }
        )
    return summaries


def make_figure(rows: list[dict[str, Any]], path: Path, threshold: float) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    dims = sorted({int(row["dim"]) for row in rows})
    colors = {dim: color for dim, color in zip(dims, ("#1261a0", "#d1495b"))}
    fig, axes = plt.subplots(1, 3, figsize=(13.2, 4.0), constrained_layout=True)
    series = (
        ("orientation_spread", "Principal-orientation spread"),
        ("monopole_error_max", "Max point-monopole error"),
        ("tangential_residual_max", "Max tangential residual"),
    )
    for dim in dims:
        selected = sorted(
            (row for row in rows if row["dim"] == dim),
            key=lambda row: row["radius_ratio"],
        )
        x = np.asarray([row["radius_ratio"] for row in selected])
        for axis, (key, label) in zip(axes, series):
            y = np.maximum(np.asarray([row[key] for row in selected]), 1e-18)
            axis.plot(x, y, marker="o", color=colors[dim], label=f"d={dim}")
            axis.set_xscale("log")
            axis.set_yscale("log")
            axis.axhline(threshold, color="#555555", linestyle="--", linewidth=0.9)
            axis.set_xlabel("Cross sigma_rep / R_mem")
            axis.set_ylabel(label)
            axis.grid(alpha=0.25)
            axis.invert_xaxis()
    for axis in axes:
        axis.legend(fontsize=8)
    fig.suptitle("Scalar cross-readout: broad far field to shape-resolving near field")
    fig.savefig(path, dpi=180)
    plt.close(fig)


def _fmt(value: float | None) -> str:
    if value is None:
        return "none"
    if value == 0.0:
        return "0"
    if abs(value) < 1e-3 or abs(value) >= 1e3:
        return f"{value:.3e}"
    return f"{value:.4f}"


def build_report(payload: dict[str, Any], report_path: Path, figure_path: Path) -> str:
    lines = [
        "# Scalar cross-readout resolution gate",
        "",
        f"Date: {payload['generated_utc']}",
        "",
        "## Preregistered question",
        "",
        "Can an independent instantaneous scalar cross-readout distinguish rigid",
        "orientations of one complete N=100M source checkpoint before source and",
        "target memory clouds overlap? This is an operator-resolution test, not a",
        "dynamical interaction, mediator, synchronization, or particle claim.",
        "",
        "Only cross sigma_rep is varied. The source checkpoint and self-dynamics,",
        "sigma_att/sigma_rep, amplitudes, and requested bare centre response",
        f"({payload['response_fraction']:.3f} R_mem per memory time) remain fixed.",
        "Every row is recalibrated to that response, so cross_eta is not a second",
        "independent scan. The point monopole is the null model.",
        "",
        "Primary shape signal: maximum drift difference between principal-axis",
        f"orientations divided by point drift. Threshold: {payload['shape_threshold']:.1%};",
        f"minimum centre distinctness: {payload['minimum_distinctness']:.2f} times the",
        "sum of target and source memory radii.",
        "",
        "## Results",
        "",
        "| d | self | sigma_rep/R | separation/(R_t+R_s) | orientation spread | orientation response/R | point error | eta_cross | calibrated fraction | shape gate |",
        "| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    ordered = sorted(
        payload["rows"], key=lambda row: (row["dim"], -row["radius_ratio"])
    )
    for row in ordered:
        lines.append(
            f"| {row['dim']} | {'yes' if row['self_readout'] else 'no'} | "
            f"{_fmt(row['radius_ratio'])} | "
            f"{_fmt(row['separation_over_combined_radius'])} | "
            f"{_fmt(row['orientation_spread'])} | "
            f"{_fmt(row['orientation_response_fraction'])} | "
            f"{_fmt(row['monopole_error_max'])} | "
            f"{_fmt(row['cross_eta'])} | "
            f"{_fmt(row['reconstructed_response_fraction'])} | "
            f"{'pass' if row['shape_resolved'] else 'fail'} |"
        )
    lines.extend(
        [
            "",
            "## Preliminary onset",
            "",
            "| d | self sigma_rep/R | self orientation spread | finite-source onset | orientation onset | max orientation spread |",
            "| ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for summary in payload["case_summaries"]:
        lines.append(
            f"| {summary['dim']} | {_fmt(summary['baseline_ratio'])} | "
            f"{_fmt(summary['baseline_orientation_spread'])} | "
            f"{_fmt(summary['finite_source_onset_ratio'])} | "
            f"{_fmt(summary['shape_onset_ratio'])} | "
            f"{_fmt(summary['maximum_orientation_spread'])} |"
        )
    lines.extend(
        [
            "",
            "An onset means only that this frozen scalar field can statically",
            "resolve finite extent or orientation at the listed scale. One source",
            "checkpoint per ambient dimension is pipeline evidence, not seed-level",
            "inference. Ratios near the distinctness boundary require an explicit",
            "cloud-overlap check in any later dynamic experiment.",
            "",
            "## Mechanism decision",
            "",
            "A reproducible orientation onset would justify testing a local or",
            "retarded scalar mediator first: it can transport an already measurable",
            "scalar shape signal without adding internal components. Failure before",
            "overlap would instead prioritize an oriented memory/current channel.",
            "Neither outcome establishes phase, polarization, spin, charge, finite",
            "signal speed, or an external three-dimensional sector.",
            "",
            "The next dynamical gate must still preregister at least six independent",
            "formation states, common future noise, channel-off and point-source",
            "controls, bounded source shape, and a stop rule.",
            "",
            "## Figure",
            "",
            f"![Cross-readout resolution]({_rel_from(report_path, figure_path)})",
            "",
            "## Reproducibility",
            "",
            f"- Analysis revision: {payload['git_revision']}",
            f"- Summary: {_rel(payload['summary_json'])}",
            f"- Command: {' '.join(payload['command'])}",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    args = parse_args()
    try:
        ratios = parse_resolution_ratios(args.resolution_ratios)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    if not 0.0 < args.response_fraction < 1.0:
        raise SystemExit("--response-fraction must lie between zero and one")
    if not 0.0 < args.shape_threshold < 1.0:
        raise SystemExit("--shape-threshold must lie between zero and one")
    if args.minimum_distinctness <= 0.0:
        raise SystemExit("--minimum-distinctness must be positive")
    git_revision = _git_output(["rev-parse", "HEAD"])
    git_status = _git_output(["status", "--short"])
    if git_status and not args.allow_dirty:
        raise SystemExit("resolution audit requires a clean worktree")

    rows = run_resolution_ladder(
        args.checkpoint_dir,
        resolution_ratios=ratios,
        response_fraction=args.response_fraction,
        shape_threshold=args.shape_threshold,
        minimum_distinctness=args.minimum_distinctness,
    )
    report_path = _resolve(args.report)
    summary_path = _resolve(args.summary_json)
    figure_path = _resolve(args.figure)
    make_figure(rows, figure_path, args.shape_threshold)
    payload = {
        "schema": "emergenz-knoten.scalar-cross-readout-resolution",
        "schema_version": 1,
        "generated_utc": datetime.now(UTC).isoformat(timespec="seconds"),
        "git_revision": git_revision,
        "git_status_at_start": git_status,
        "command": ["python", *os.sys.argv],
        "checkpoint_dir": _rel(_resolve(args.checkpoint_dir)),
        "resolution_ratios": ratios,
        "response_fraction": float(args.response_fraction),
        "shape_threshold": float(args.shape_threshold),
        "minimum_distinctness": float(args.minimum_distinctness),
        "rows": rows,
        "case_summaries": summarize_cases(rows),
        "summary_json": summary_path,
        "figure": figure_path,
    }
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(
        json.dumps(_jsonable(payload), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        build_report(payload, report_path, figure_path),
        encoding="utf-8",
    )
    print(f"wrote {_rel(report_path)}", flush=True)


if __name__ == "__main__":
    main()
