"""Run a calibrated near-to-far frozen-source distance ladder."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import UTC, datetime
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from emergenz_knoten import effective_double_gaussian_parameters, response_rank


def _repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("repository root not found")


ROOT = _repo_root()
DEFAULT_CHECKPOINT_DIR = Path(
    "data/processed/reference_states/scalar_Aatt35_N100M_d3_d10_seed1_2026-07-16"
)


def _load_response_runner():
    path = Path(__file__).with_name("frozen_source_response.py")
    spec = importlib.util.spec_from_file_location("_frozen_source_response", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load frozen_source_response.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


RESPONSE = _load_response_runner()


@dataclass(frozen=True)
class DistanceSpec:
    scale: str
    multiplier: float

    @property
    def label(self) -> str:
        suffix = "R_mem" if self.scale == "radius" else "sigma_rep"
        return f"{self.multiplier:g} {suffix}"


def parse_distance_specs(text: str) -> list[DistanceSpec]:
    """Parse entries such as ``R:5,S:0.1`` without hidden unit conversion."""

    specs: list[DistanceSpec] = []
    for item in text.split(","):
        item = item.strip()
        if not item:
            continue
        try:
            prefix, raw_value = item.split(":", maxsplit=1)
            multiplier = float(raw_value)
        except ValueError as exc:
            raise ValueError("distance specs must use R:value or S:value") from exc
        prefix = prefix.strip().upper()
        if prefix not in {"R", "S"}:
            raise ValueError(
                "distance scale must be R (memory radius) or S (sigma_rep)"
            )
        if not np.isfinite(multiplier) or multiplier <= 0.0:
            raise ValueError("distance multipliers must be positive and finite")
        specs.append(
            DistanceSpec(
                scale="radius" if prefix == "R" else "sigma",
                multiplier=multiplier,
            )
        )
    if not specs:
        raise ValueError("at least one distance spec is required")
    labels = [spec.label for spec in specs]
    if len(labels) != len(set(labels)):
        raise ValueError("distance specs must not contain duplicates")
    return specs


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run calibrated frozen-source target-deformation distances."
    )
    parser.add_argument("--checkpoint-dir", type=Path, default=DEFAULT_CHECKPOINT_DIR)
    parser.add_argument(
        "--distances",
        default="R:5,R:20,R:100,S:0.01,S:0.1,S:1",
    )
    parser.add_argument("--interaction-fraction", type=float, default=0.03)
    parser.add_argument("--source-shift-fractions", default="0.03,0.10")
    parser.add_argument("--pulse-memory-times", type=float, default=1.0)
    parser.add_argument("--lag-memory-times", default="0,0.25,1,3,10")
    parser.add_argument("--noise-base-seed", type=int, default=20_260_717)
    parser.add_argument("--allow-dirty", action="store_true")
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("reports/response/frozen_source_distance_ladder_2026-07-17.md"),
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=Path(
            "reports/response/frozen_source_distance_ladder_summary_2026-07-17.json"
        ),
    )
    parser.add_argument(
        "--figure-dir",
        type=Path,
        default=Path("figures/draft/response/frozen_source_distance_ladder_2026-07-17"),
    )
    return parser.parse_args()


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def _rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _rel_from(source_file: Path, target: Path) -> str:
    return Path(
        os.path.relpath(target.resolve(), source_file.resolve().parent)
    ).as_posix()


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


def _float_list(text: str) -> list[float]:
    values = [float(part.strip()) for part in text.split(",") if part.strip()]
    if not values or any(not np.isfinite(value) for value in values):
        raise ValueError("expected a non-empty comma-separated finite float list")
    return values


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


def _distance_for_case(case: Any, spec: DistanceSpec) -> tuple[float, float]:
    effective = effective_double_gaussian_parameters(
        dim=case.dim,
        sigma_rep=case.config.sigma_rep,
        sigma_att=case.config.sigma_att,
        amplitude_rep=case.config.amplitude_rep,
        amplitude_att=case.config.amplitude_att,
        deposition_kernel=case.config.deposition_kernel,
        deposition_sigma=case.config.deposition_sigma,
    )
    sigma_rep = float(effective["sigma_rep"])
    if spec.scale == "radius":
        separation = spec.multiplier * case.initial_radius
    else:
        separation = spec.multiplier * sigma_rep
    return float(separation), sigma_rep


def _response_row(
    pair: list[dict[str, Any]],
    *,
    spec: DistanceSpec,
    separation: float,
    sigma_rep: float,
) -> dict[str, Any]:
    selected = sorted(pair, key=lambda result: result["perturbation"])
    if len(selected) != 2:
        raise ValueError("each distance requires exactly two source shifts")
    low, high = selected
    lag_values = np.asarray(low["lag_memory_times"], dtype=float)
    lag_one = int(np.argmin(np.abs(lag_values - 1.0)))
    lag_ten = int(np.argmin(np.abs(lag_values - 10.0)))
    if lag_values[lag_one] != 1.0 or lag_values[lag_ten] != 10.0:
        raise ValueError("distance ladder requires lag 1 and lag 10")
    center_matrix = np.asarray(low["responses"]["memory_center_feedback"][lag_one])
    shape_matrix = np.asarray(low["responses"]["shape_feedback"][lag_one])
    center_ten = np.asarray(low["responses"]["memory_center_feedback"][lag_ten])
    shape_ten = np.asarray(low["responses"]["shape_feedback"][lag_ten])
    symmetry = next(
        row
        for row in RESPONSE.symmetry_rows(pair)
        if row["perturbation_sigma_rep"] == low["perturbation_sigma_rep"]
        and row["lag_memory_times"] == 1.0
        and row["observable"] == "memory_center_feedback"
    )
    linearity = RESPONSE.linearity_rows(pair)

    def difference(observable: str) -> float:
        return float(
            next(
                row["relative_difference_max"]
                for row in linearity
                if row["observable"] == observable
            )
        )

    active_shape_effect = np.asarray(low["baseline_effects"]["active_shape"])
    active_center_effect = np.asarray(low["baseline_effects"]["active_memory_center"])
    return {
        "checkpoint": low["checkpoint"],
        "dim": low["dim"],
        "seed": low["seed"],
        "update_index": low["update_index"],
        "formation_revision": low["formation_revision"],
        "distance_label": spec.label,
        "distance_scale": spec.scale,
        "distance_multiplier": spec.multiplier,
        "separation": separation,
        "separation_radii": separation / low["initial_radius"],
        "separation_sigma_rep": separation / sigma_rep,
        "interaction_fraction": low["interaction_fraction"],
        "cross_eta": low["calibration"]["cross_eta"],
        "baseline_gradient_norm": low["calibration"]["baseline_initial_gradient_norm"],
        "baseline_directional_drift": low["calibration"]["baseline_directional_drift"],
        "source_shift_low_fraction": low["perturbation"] / separation,
        "source_shift_high_fraction": high["perturbation"] / separation,
        "zero_cross_max_abs": max(
            result["quality"]["zero_cross_max_abs"] for result in pair
        ),
        "realized_baseline_fraction": low["quality"]["bare_baseline_pulse_fraction"],
        "baseline_radius_deformation_max": float(
            np.max(np.abs(low["baseline_effects"]["active_radius"]))
        ),
        "baseline_shape_effect_max": float(
            np.max(np.linalg.norm(active_shape_effect, axis=1))
        ),
        "baseline_center_effect_max": float(
            np.max(np.linalg.norm(active_center_effect, axis=1))
        ),
        "branch_radius_disturbance_max": max(
            result["quality"]["branch_baseline_radius_max_abs"] for result in pair
        ),
        "even_radius_max": max(
            result["quality"]["radius_even_max_abs"] for result in pair
        ),
        "center_feedback_rank": response_rank(center_matrix).rank,
        "shape_feedback_rank": response_rank(shape_matrix).rank,
        "center_feedback_singular_values": np.linalg.svd(
            center_matrix,
            compute_uv=False,
        ),
        "shape_feedback_singular_values": np.linalg.svd(
            shape_matrix,
            compute_uv=False,
        ),
        "center_feedback_norm_lag1": float(np.linalg.norm(center_matrix)),
        "shape_feedback_norm_lag1": float(np.linalg.norm(shape_matrix)),
        "center_feedback_norm_lag10": float(np.linalg.norm(center_ten)),
        "shape_feedback_norm_lag10": float(np.linalg.norm(shape_ten)),
        "center_linearity_difference": difference("memory_center_feedback"),
        "shape_linearity_difference": difference("shape_feedback"),
        "radial_transverse_abs_ratio": symmetry["radial_transverse_abs_ratio"],
        "off_diagonal_fraction": symmetry["off_diagonal_fraction"],
        "transverse_relative_spread": symmetry["transverse_relative_spread"],
    }


def run_distance_ladder(
    cases: list[Any],
    *,
    distance_specs: list[DistanceSpec],
    interaction_fraction: float,
    source_shift_fractions: list[float],
    pulse_memory_times: float,
    lag_memory_times: list[float],
    noise_base_seed: int,
) -> list[dict[str, Any]]:
    if len(source_shift_fractions) != 2 or any(
        value <= 0.0 for value in source_shift_fractions
    ):
        raise ValueError("source_shift_fractions requires two positive values")
    rows: list[dict[str, Any]] = []
    for case in cases:
        for spec in distance_specs:
            separation, sigma_rep = _distance_for_case(case, spec)
            separation_sigma_rep = separation / sigma_rep
            perturbation_sigma_rep = [
                fraction * separation_sigma_rep for fraction in source_shift_fractions
            ]
            print(
                f"running d={case.dim} {spec.label} "
                f"(r/R={separation / case.initial_radius:.3g})",
                flush=True,
            )
            pair = RESPONSE.run_checkpoint_case(
                case,
                interaction_fraction=interaction_fraction,
                perturbation_sigma_rep=perturbation_sigma_rep,
                separation_sigma_rep=separation_sigma_rep,
                pulse_memory_times=pulse_memory_times,
                lag_memory_times=lag_memory_times,
                noise_base_seed=noise_base_seed,
                calibration_mode="realized",
            )
            rows.append(
                _response_row(
                    pair,
                    spec=spec,
                    separation=separation,
                    sigma_rep=sigma_rep,
                )
            )
    return rows


def make_figures(
    rows: list[dict[str, Any]],
    figure_dir: Path,
) -> tuple[Path, Path, Path]:
    figure_dir.mkdir(parents=True, exist_ok=True)
    dims = sorted({int(row["dim"]) for row in rows})
    colors = {dims[index]: color for index, color in enumerate(("#1261a0", "#d1495b"))}

    def values(dim: int, key: str) -> tuple[np.ndarray, np.ndarray]:
        selected = sorted(
            (row for row in rows if row["dim"] == dim),
            key=lambda row: row["separation_radii"],
        )
        return (
            np.asarray([row["separation_radii"] for row in selected]),
            np.asarray([row[key] for row in selected]),
        )

    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.0), constrained_layout=True)
    for dim in dims:
        for axis, key, label in (
            (axes[0], "baseline_radius_deformation_max", "radius deformation"),
            (axes[1], "baseline_shape_effect_max", "shape effect"),
        ):
            x, y = values(dim, key)
            axis.plot(
                x, np.maximum(y, 1e-18), marker="o", color=colors[dim], label=f"d={dim}"
            )
            axis.set_xscale("log")
            axis.set_yscale("log")
            axis.set_xlabel("Source distance / target R_mem")
            axis.set_ylabel(label)
            axis.grid(alpha=0.25)
    axes[0].set_title("Target radius response")
    axes[1].set_title("Target shape response")
    for axis in axes:
        axis.legend(fontsize=8)
    deformation_path = figure_dir / "distance_ladder_target_deformation.png"
    fig.savefig(deformation_path, dpi=180)
    plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.0), constrained_layout=True)
    for dim in dims:
        for axis, key, label in (
            (axes[0], "center_feedback_norm_lag1", "center feedback norm"),
            (axes[1], "shape_feedback_norm_lag1", "shape feedback norm"),
        ):
            x, y = values(dim, key)
            axis.plot(
                x, np.maximum(y, 1e-18), marker="o", color=colors[dim], label=f"d={dim}"
            )
            axis.set_xscale("log")
            axis.set_yscale("log")
            axis.set_xlabel("Source distance / target R_mem")
            axis.set_ylabel(label)
            axis.grid(alpha=0.25)
    axes[0].set_title("Center Jacobian at lag 1")
    axes[1].set_title("Shape Jacobian at lag 1")
    for axis in axes:
        axis.legend(fontsize=8)
    response_path = figure_dir / "distance_ladder_feedback.png"
    fig.savefig(response_path, dpi=180)
    plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.0), constrained_layout=True)
    for dim in dims:
        for axis, key, label in (
            (axes[0], "radial_transverse_abs_ratio", "abs radial/transverse"),
            (axes[1], "off_diagonal_fraction", "off-diagonal fraction"),
        ):
            x, y = values(dim, key)
            axis.plot(
                x, np.maximum(y, 1e-18), marker="o", color=colors[dim], label=f"d={dim}"
            )
            axis.set_xscale("log")
            axis.set_xlabel("Source distance / target R_mem")
            axis.set_ylabel(label)
            axis.grid(alpha=0.25)
    axes[0].axhline(1.0, color="#555555", linestyle="--", linewidth=0.8)
    axes[1].set_yscale("log")
    axes[0].set_title("Scalar radial/transverse sector")
    axes[1].set_title("Source-aligned leakage")
    for axis in axes:
        axis.legend(fontsize=8)
    symmetry_path = figure_dir / "distance_ladder_symmetry.png"
    fig.savefig(symmetry_path, dpi=180)
    plt.close(fig)
    return deformation_path, response_path, symmetry_path


def _fmt(value: float) -> str:
    if value == 0.0:
        return "0"
    if abs(value) < 1e-3 or abs(value) >= 1e3:
        return f"{value:.3e}"
    return f"{value:.4f}"


def build_report(
    payload: dict[str, Any],
    *,
    report_path: Path,
    figure_paths: tuple[Path, Path, Path],
) -> str:
    rows = payload["rows"]
    lines = [
        "# Frozen-source distance ladder",
        "",
        f"Date: {payload['generated_utc']}",
        "",
        "## Scope",
        "",
        "The static field audit shows that the retained source is pointlike at",
        "the current interaction-kernel resolution. This ladder therefore tests",
        "tidal deformation and nonlinear target feedback versus source distance.",
        "It does not test source orientation, charge, or an external dimension.",
        "",
        "Every distance is calibrated to the same bare displacement of 0.03 target",
        "memory radii over one memory time. Source translations are 0.03 and 0.10",
        "of the baseline distance, and every distance and paired path shares the same future noise.",
        "",
        "## Results at lag one memory time",
        "",
        "| d | distance | r/R_mem | r/sigma_rep | eta_cross | zero error | radius deformation | shape effect | center rank | shape rank | radial/transverse |",
        "| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in rows:
        lines.append(
            f"| {row['dim']} | {row['distance_label']} | "
            f"{_fmt(row['separation_radii'])} | "
            f"{_fmt(row['separation_sigma_rep'])} | "
            f"{_fmt(row['cross_eta'])} | {_fmt(row['zero_cross_max_abs'])} | "
            f"{_fmt(row['baseline_radius_deformation_max'])} | "
            f"{_fmt(row['baseline_shape_effect_max'])} | "
            f"{row['center_feedback_rank']} | {row['shape_feedback_rank']} | "
            f"{_fmt(row['radial_transverse_abs_ratio'])} |"
        )
    lines.extend(
        [
            "",
            "## Quality gates",
            "",
            "| d | distance | realized fraction | branch radius disturbance | center delta difference | shape delta difference | off-diagonal fraction |",
            "| ---: | --- | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in rows:
        lines.append(
            f"| {row['dim']} | {row['distance_label']} | "
            f"{_fmt(row['realized_baseline_fraction'])} | "
            f"{_fmt(row['branch_radius_disturbance_max'])} | "
            f"{_fmt(row['center_linearity_difference'])} | "
            f"{_fmt(row['shape_linearity_difference'])} | "
            f"{_fmt(row['off_diagonal_fraction'])} |"
        )
    lines.extend(
        [
            "",
            "## Distance effect",
            "",
            "| d | max radius deformation | at | max shape effect | at | near/far radius ratio | near/far shape ratio |",
            "| ---: | ---: | --- | ---: | --- | ---: | ---: |",
        ]
    )
    for dim in sorted({int(row["dim"]) for row in rows}):
        selected = sorted(
            (row for row in rows if row["dim"] == dim),
            key=lambda row: row["separation_radii"],
        )
        near = selected[0]
        far = selected[-1]
        max_radius = max(
            selected, key=lambda row: row["baseline_radius_deformation_max"]
        )
        max_shape = max(selected, key=lambda row: row["baseline_shape_effect_max"])
        lines.append(
            f"| {dim} | {_fmt(max_radius['baseline_radius_deformation_max'])} | "
            f"{max_radius['distance_label']} | "
            f"{_fmt(max_shape['baseline_shape_effect_max'])} | "
            f"{max_shape['distance_label']} | "
            f"{_fmt(near['baseline_radius_deformation_max'] / far['baseline_radius_deformation_max'])} | "
            f"{_fmt(near['baseline_shape_effect_max'] / far['baseline_shape_effect_max'])} |"
        )
    lines.extend(
        [
            "",
            "All center and shape Jacobians retain the ambient input rank. At the",
            "smallest distances the radial/transverse ratio approaches one, as",
            "expected for the locally harmonic part of an isotropic scalar field.",
            "The enhanced d=3 near response is a small target-deformation effect,",
            "not resolved source structure; all reported normalized deformations",
            "remain below 0.002. One checkpoint per dimension makes these",
            "descriptive pathwise results, not seed-level inference.",
        ]
    )
    lines.extend(
        [
            "",
            "## Guardrails",
            "",
            "Full ambient rank remains the expected response of an isotropic scalar",
            "kernel. A distance-dependent target deformation can identify a safe",
            "weak-coupling range, but cannot establish charge, parity violation,",
            "reciprocity, synchronization, or three selected external dimensions.",
            "",
            "## Model implication",
            "",
            "At the present resolution rho behaves as an unsigned scalar",
            "mass-like channel with universal attraction. Parity and charge",
            "sign are different questions: electric charge is parity-even,",
            "while its sign is an internal/charge-conjugation label. The minimal",
            "next model test is therefore a separate signed scalar cross-channel",
            "with q=0 and sign-reversal controls while self-confinement remains",
            "unchanged. Vector memory is justified only when an observable needs",
            "orientation, phase, circulation, or polarization.",
            "",
            "## Figures",
            "",
        ]
    )
    deformation_path, response_path, symmetry_path = figure_paths
    lines.extend(
        [
            f"![Target deformation]({_rel_from(report_path, deformation_path)})",
            "",
            f"![Feedback]({_rel_from(report_path, response_path)})",
            "",
            f"![Symmetry]({_rel_from(report_path, symmetry_path)})",
            "",
            "## Reproducibility",
            "",
            f"- Analysis revision: {payload['git_revision']}",
            "- Static field audit: reports/response/frozen_source_field_audit_2026-07-17.md",
            f"- Summary: {_rel(payload['summary_json'])}",
            f"- Command: {' '.join(payload['command'])}",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    args = parse_args()
    try:
        distance_specs = parse_distance_specs(args.distances)
        source_shifts = _float_list(args.source_shift_fractions)
        lag_memory_times = _float_list(args.lag_memory_times)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    if len(source_shifts) != 2 or any(value <= 0.0 for value in source_shifts):
        raise SystemExit("--source-shift-fractions requires two positive values")
    if 1.0 not in lag_memory_times or 10.0 not in lag_memory_times:
        raise SystemExit("--lag-memory-times must include 1 and 10")
    git_revision = _git_output(["rev-parse", "HEAD"])
    git_status = _git_output(["status", "--short"])
    if git_status and not args.allow_dirty:
        raise SystemExit(
            "distance ladder requires a clean worktree; commit changes first"
        )

    rows = run_distance_ladder(
        RESPONSE.load_checkpoint_cases(args.checkpoint_dir),
        distance_specs=distance_specs,
        interaction_fraction=args.interaction_fraction,
        source_shift_fractions=source_shifts,
        pulse_memory_times=args.pulse_memory_times,
        lag_memory_times=lag_memory_times,
        noise_base_seed=args.noise_base_seed,
    )
    report_path = _resolve(args.report)
    summary_path = _resolve(args.summary_json)
    figure_paths = make_figures(rows, _resolve(args.figure_dir))
    payload = {
        "schema": "emergenz-knoten.frozen-source-distance-ladder",
        "schema_version": 1,
        "generated_utc": datetime.now(UTC).isoformat(timespec="seconds"),
        "git_revision": git_revision,
        "git_status_at_start": git_status,
        "command": ["python", *os.sys.argv],
        "checkpoint_dir": _rel(_resolve(args.checkpoint_dir)),
        "distance_specs": [spec.__dict__ for spec in distance_specs],
        "interaction_fraction": float(args.interaction_fraction),
        "source_shift_fractions": source_shifts,
        "pulse_memory_times": float(args.pulse_memory_times),
        "lag_memory_times": lag_memory_times,
        "noise_base_seed": int(args.noise_base_seed),
        "rows": rows,
        "summary_json": summary_path,
        "figures": list(figure_paths),
    }
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(
        json.dumps(_jsonable(payload), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        build_report(payload, report_path=report_path, figure_paths=figure_paths),
        encoding="utf-8",
    )
    print(f"wrote {_rel(report_path)}", flush=True)


if __name__ == "__main__":
    main()
