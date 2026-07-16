"""Calibrate local frozen-source translation response from checkpoints."""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass, replace
from datetime import UTC, datetime
import json
import os
from pathlib import Path
import subprocess
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from emergenz_knoten import (
    FiniteMemoryState,
    SimulationConfig,
    calibrate_frozen_source_cross_eta,
    effective_double_gaussian_parameters,
    load_finite_memory_checkpoint,
    memory_shape_tensor,
    paired_frozen_source_response,
    response_rank,
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


@dataclass(frozen=True)
class CheckpointCase:
    path: Path
    seed: int
    update_index: int
    formation_revision: str
    config: SimulationConfig
    state: FiniteMemoryState
    initial_radius: float

    @property
    def dim(self) -> int:
        return self.state.dim


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run local source-translation probes on frozen z_N checkpoints."
    )
    parser.add_argument("--checkpoint-dir", type=Path, default=DEFAULT_CHECKPOINT_DIR)
    parser.add_argument("--interaction-fraction", type=float, default=0.03)
    parser.add_argument("--perturbation-sigma-rep", default="0.03,0.10")
    parser.add_argument("--separation-sigma-rep", type=float, default=1.0)
    parser.add_argument("--pulse-memory-times", type=float, default=1.0)
    parser.add_argument("--lag-memory-times", default="0,0.25,1,3,10")
    parser.add_argument("--noise-base-seed", type=int, default=20_260_717)
    parser.add_argument("--allow-dirty", action="store_true")
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("reports/response/frozen_source_pilot_2026-07-16.md"),
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=Path("reports/response/frozen_source_pilot_summary_2026-07-16.json"),
    )
    parser.add_argument(
        "--figure-dir",
        type=Path,
        default=Path("figures/draft/response/frozen_source_pilot_2026-07-16"),
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
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        number = float(value)
        return number if np.isfinite(number) else None
    if isinstance(value, Path):
        return _rel(value)
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    return value


def load_checkpoint_cases(checkpoint_dir: Path) -> list[CheckpointCase]:
    cases: list[CheckpointCase] = []
    for path in sorted(_resolve(checkpoint_dir).glob("*.npz")):
        checkpoint = load_finite_memory_checkpoint(path)
        radius = float(
            np.sqrt(max(np.trace(memory_shape_tensor(checkpoint.state)), 0.0))
        )
        if radius <= 0.0:
            raise ValueError(f"checkpoint has degenerate memory radius: {path}")
        cases.append(
            CheckpointCase(
                path=path,
                seed=checkpoint.formation_seed,
                update_index=checkpoint.update_index,
                formation_revision=checkpoint.git_revision,
                config=checkpoint.config,
                state=checkpoint.state,
                initial_radius=radius,
            )
        )
    cases.sort(key=lambda case: (case.dim, case.seed))
    if not cases:
        raise ValueError(f"no checkpoint NPZ files found in {_resolve(checkpoint_dir)}")
    return cases


def _relative_difference(first: np.ndarray, second: np.ndarray) -> float:
    denominator = float(np.linalg.norm(first) + np.linalg.norm(second))
    if denominator <= np.finfo(float).eps:
        return 0.0
    return float(2.0 * np.linalg.norm(first - second) / denominator)


def _zero_cross_error(response: Any) -> float:
    arrays = (
        response.position_jacobians,
        response.memory_center_jacobians,
        response.shape_jacobians,
        response.position_even_offsets,
        response.memory_center_even_offsets,
        response.shape_even_vectors,
        response.radius_even_offsets,
        response.baseline_positions - response.free_positions,
        response.baseline_memory_centers - response.free_memory_centers,
        response.baseline_shape_vectors - response.free_shape_vectors,
        response.baseline_radius_ratios - response.free_radius_ratios,
    )
    return float(max(np.max(np.abs(array)) for array in arrays))


def run_checkpoint_case(
    case: CheckpointCase,
    *,
    interaction_fraction: float,
    perturbation_sigma_rep: list[float],
    separation_sigma_rep: float,
    pulse_memory_times: float,
    lag_memory_times: list[float],
    noise_base_seed: int,
) -> list[dict[str, Any]]:
    if not np.isfinite(interaction_fraction) or interaction_fraction <= 0.0:
        raise ValueError("interaction_fraction must be positive and finite")
    if any(value <= 0.0 for value in perturbation_sigma_rep):
        raise ValueError("perturbation_sigma_rep values must be positive")
    if not np.isfinite(separation_sigma_rep) or separation_sigma_rep <= 0.0:
        raise ValueError("separation_sigma_rep must be positive and finite")
    if not np.isfinite(pulse_memory_times) or pulse_memory_times <= 0.0:
        raise ValueError("pulse_memory_times must be positive and finite")
    if any(not np.isfinite(lag) or lag < 0.0 for lag in lag_memory_times):
        raise ValueError("lag_memory_times must be finite and non-negative")

    tau_updates = 1.0 / case.config.alpha
    pulse_steps = max(1, int(round(pulse_memory_times * tau_updates)))
    lag_updates = np.asarray(
        [int(round(lag * tau_updates)) for lag in lag_memory_times],
        dtype=int,
    )
    sample_steps = pulse_steps + lag_updates
    if len(np.unique(sample_steps)) != len(sample_steps):
        raise ValueError("lag_memory_times collapse to duplicate integer sample steps")

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
    separation = float(separation_sigma_rep * sigma_rep)
    source_offset = np.zeros(case.dim, dtype=float)
    source_offset[0] = separation
    directions = np.eye(case.dim, dtype=float)
    noise_seed = int(noise_base_seed + 1009 * case.dim + case.seed)
    noise = np.random.default_rng(noise_seed).normal(
        size=(int(sample_steps[-1]), case.dim)
    )
    eta_zero = replace(case.config, eta=0.0)
    calibration = calibrate_frozen_source_cross_eta(
        case.state,
        case.state,
        case.config,
        source_center_offset=source_offset,
        response_fraction=interaction_fraction,
        pulse_steps=pulse_steps,
    )

    common = {
        "directions": directions,
        "source_center_offset": source_offset,
        "noise": noise,
        "sample_steps": sample_steps,
        "pulse_steps": pulse_steps,
    }
    zero_cross = paired_frozen_source_response(
        case.state,
        case.state,
        case.config,
        perturbation=min(perturbation_sigma_rep) * sigma_rep,
        cross_eta=0.0,
        **common,
    )
    zero_error = _zero_cross_error(zero_cross)

    results: list[dict[str, Any]] = []
    for perturbation_fraction in perturbation_sigma_rep:
        perturbation = float(perturbation_fraction * sigma_rep)
        kwargs = {
            **common,
            "perturbation": perturbation,
            "cross_eta": calibration.cross_eta,
        }
        active = paired_frozen_source_response(
            case.state,
            case.state,
            case.config,
            **kwargs,
        )
        bare = paired_frozen_source_response(
            case.state,
            case.state,
            eta_zero,
            **kwargs,
        )
        radius = case.initial_radius
        responses = {
            "active_position": active.position_jacobians,
            "bare_position": bare.position_jacobians,
            "position_feedback": active.position_jacobians - bare.position_jacobians,
            "active_memory_center": active.memory_center_jacobians,
            "bare_memory_center": bare.memory_center_jacobians,
            "memory_center_feedback": (
                active.memory_center_jacobians - bare.memory_center_jacobians
            ),
            "active_shape": active.shape_jacobians / radius,
            "bare_shape": bare.shape_jacobians / radius,
            "shape_feedback": (active.shape_jacobians - bare.shape_jacobians) / radius,
        }
        baseline_effects = {
            "active_position": (active.baseline_positions - active.free_positions)
            / radius,
            "bare_position": (bare.baseline_positions - bare.free_positions) / radius,
            "active_memory_center": (
                active.baseline_memory_centers - active.free_memory_centers
            )
            / radius,
            "bare_memory_center": (
                bare.baseline_memory_centers - bare.free_memory_centers
            )
            / radius,
            "active_shape": (active.baseline_shape_vectors - active.free_shape_vectors)
            / (radius * radius),
            "bare_shape": (bare.baseline_shape_vectors - bare.free_shape_vectors)
            / (radius * radius),
            "active_radius": (
                active.baseline_radius_ratios - active.free_radius_ratios
            ),
            "bare_radius": bare.baseline_radius_ratios - bare.free_radius_ratios,
        }
        baseline_direction = source_offset / np.linalg.norm(source_offset)
        bare_pulse_offset = bare.baseline_positions[0] - bare.free_positions[0]
        realized_fraction = float(
            np.dot(baseline_direction, bare_pulse_offset) / radius
        )
        branch_radius_difference = (
            active.radius_ratios - (active.baseline_radius_ratios[:, None, None])
        )
        initial_norms = active.initial_source_gradient_norms
        results.append(
            {
                "checkpoint": _rel(case.path),
                "dim": case.dim,
                "seed": case.seed,
                "update_index": case.update_index,
                "formation_revision": case.formation_revision,
                "config": asdict(case.config),
                "initial_radius": radius,
                "noise_seed": noise_seed,
                "interaction_fraction": float(interaction_fraction),
                "perturbation_sigma_rep": float(perturbation_fraction),
                "perturbation": perturbation,
                "perturbation_radii": perturbation / radius,
                "separation": separation,
                "separation_sigma_rep": float(separation_sigma_rep),
                "separation_radii": separation / radius,
                "source_center_offset": source_offset,
                "pulse_steps": pulse_steps,
                "pulse_memory_times": float(pulse_memory_times),
                "lag_memory_times": np.asarray(lag_memory_times, dtype=float),
                "lag_updates": lag_updates,
                "sample_steps": sample_steps,
                "calibration": {
                    "cross_eta": calibration.cross_eta,
                    "baseline_initial_gradient_norm": (
                        calibration.baseline_gradient_norm
                    ),
                    "perturbed_gradient_norm_min": float(np.min(initial_norms)),
                    "perturbed_gradient_norm_max": float(np.max(initial_norms)),
                },
                "responses": responses,
                "baseline_effects": baseline_effects,
                "quality": {
                    "zero_cross_max_abs": zero_error,
                    "bare_baseline_pulse_fraction": realized_fraction,
                    "branch_baseline_radius_max_abs": float(
                        np.max(np.abs(branch_radius_difference))
                    ),
                    "baseline_free_radius_max_abs": float(
                        np.max(
                            np.abs(
                                active.baseline_radius_ratios
                                - active.free_radius_ratios
                            )
                        )
                    ),
                    "radius_even_max_abs": float(
                        np.max(np.abs(active.radius_even_offsets))
                    ),
                    "source_gradient_relative_spread": float(
                        (np.max(initial_norms) - np.min(initial_norms))
                        / calibration.baseline_gradient_norm
                    ),
                },
            }
        )
    return results


def rank_rows(case_results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for result in case_results:
        for lag_index, lag in enumerate(result["lag_memory_times"]):
            for observable, matrices in result["responses"].items():
                matrix = np.asarray(matrices[lag_index], dtype=float)
                rows.append(
                    {
                        "dim": result["dim"],
                        "seed": result["seed"],
                        "perturbation_sigma_rep": result["perturbation_sigma_rep"],
                        "lag_memory_times": float(lag),
                        "observable": observable,
                        "energy_rank": response_rank(matrix).rank,
                        "singular_values": np.linalg.svd(
                            matrix,
                            compute_uv=False,
                        ),
                        "frobenius_norm": float(np.linalg.norm(matrix)),
                    }
                )
    return rows


def symmetry_rows(case_results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Audit radial/transverse sectors in the source-aligned response basis."""

    rows: list[dict[str, Any]] = []
    for result in case_results:
        if result["dim"] < 2:
            continue
        for lag_index, lag in enumerate(result["lag_memory_times"]):
            for observable in (
                "bare_position",
                "active_memory_center",
                "memory_center_feedback",
                "position_feedback",
            ):
                matrix = np.asarray(result["responses"][observable][lag_index])
                diagonal = np.diag(matrix)
                transverse = diagonal[1:]
                matrix_norm = float(np.linalg.norm(matrix))
                transverse_scale = float(np.mean(np.abs(transverse)))
                off_diagonal = matrix - np.diag(diagonal)
                rows.append(
                    {
                        "dim": result["dim"],
                        "seed": result["seed"],
                        "perturbation_sigma_rep": result["perturbation_sigma_rep"],
                        "lag_memory_times": float(lag),
                        "observable": observable,
                        "radial_response": float(diagonal[0]),
                        "transverse_response_mean": float(np.mean(transverse)),
                        "radial_transverse_abs_ratio": float(
                            abs(diagonal[0])
                            / max(transverse_scale, np.finfo(float).tiny)
                        ),
                        "transverse_relative_spread": float(
                            np.std(transverse)
                            / max(transverse_scale, np.finfo(float).tiny)
                        ),
                        "off_diagonal_fraction": float(
                            np.linalg.norm(off_diagonal)
                            / max(matrix_norm, np.finfo(float).tiny)
                        ),
                    }
                )
    return rows


def linearity_rows(case_results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    keys = sorted({(row["dim"], row["seed"]) for row in case_results})
    for dim, seed in keys:
        selected = sorted(
            [row for row in case_results if row["dim"] == dim and row["seed"] == seed],
            key=lambda row: row["perturbation_sigma_rep"],
        )
        if len(selected) != 2:
            raise ValueError("linearity requires exactly two perturbations per case")
        low, high = selected
        for observable in low["responses"]:
            differences = np.asarray(
                [
                    _relative_difference(first, second)
                    for first, second in zip(
                        np.asarray(low["responses"][observable]),
                        np.asarray(high["responses"][observable]),
                        strict=True,
                    )
                ]
            )
            rows.append(
                {
                    "dim": dim,
                    "seed": seed,
                    "observable": observable,
                    "low_perturbation_sigma_rep": low["perturbation_sigma_rep"],
                    "high_perturbation_sigma_rep": high["perturbation_sigma_rep"],
                    "relative_difference_by_lag": differences,
                    "relative_difference_max": float(np.max(differences)),
                }
            )
    return rows


def make_figures(
    case_results: list[dict[str, Any]],
    figure_dir: Path,
) -> tuple[Path, Path, Path]:
    dims = sorted({int(row["dim"]) for row in case_results})
    perturbations = sorted(
        {float(row["perturbation_sigma_rep"]) for row in case_results}
    )

    fig, axes = plt.subplots(
        len(dims),
        len(perturbations),
        figsize=(5.4 * len(perturbations), 3.8 * len(dims)),
        squeeze=False,
        constrained_layout=True,
    )
    styles = {
        "bare_position": ("Bare position Jacobian", "#222222", "--"),
        "active_memory_center": ("Active center Jacobian", "#167d9a", "-"),
        "memory_center_feedback": ("Center feedback", "#d1495b", "-"),
        "shape_feedback": ("Shape feedback", "#5b7f3a", ":"),
    }
    for row_index, dim in enumerate(dims):
        for col_index, delta in enumerate(perturbations):
            result = next(
                row
                for row in case_results
                if row["dim"] == dim and row["perturbation_sigma_rep"] == delta
            )
            ax = axes[row_index, col_index]
            lags = np.asarray(result["lag_memory_times"])
            for observable, (label, color, linestyle) in styles.items():
                values = np.linalg.norm(
                    np.asarray(result["responses"][observable]),
                    axis=(1, 2),
                )
                ax.plot(
                    lags,
                    np.maximum(values, 1e-16),
                    marker="o",
                    label=label,
                    color=color,
                    linestyle=linestyle,
                )
            ax.set_xscale("symlog", linthresh=0.25)
            ax.set_yscale("log")
            ax.set_xlabel("Lag after pulse [memory times]")
            ax.set_ylabel("Dimensionless Frobenius norm")
            ax.set_title(f"d={dim}, delta={delta:g} sigma_rep")
            ax.grid(alpha=0.25)
            if row_index == 0 and col_index == 0:
                ax.legend(fontsize=8)
    figure_dir.mkdir(parents=True, exist_ok=True)
    response_path = figure_dir / "frozen_source_response_norms.png"
    fig.savefig(response_path, dpi=180)
    plt.close(fig)

    fig, axes = plt.subplots(
        1,
        len(dims),
        figsize=(5.4 * len(dims), 4.0),
        squeeze=False,
        constrained_layout=True,
    )
    for col_index, dim in enumerate(dims):
        ax = axes[0, col_index]
        for delta in perturbations:
            result = next(
                row
                for row in case_results
                if row["dim"] == dim and row["perturbation_sigma_rep"] == delta
            )
            lags = np.asarray(result["lag_memory_times"])
            lag_index = int(np.argmin(np.abs(lags - 1.0)))
            matrix = np.asarray(
                result["responses"]["memory_center_feedback"][lag_index]
            )
            singular_values = np.linalg.svd(matrix, compute_uv=False)
            ax.plot(
                np.arange(1, len(singular_values) + 1),
                np.maximum(singular_values, 1e-18),
                marker="o",
                label=f"delta={delta:g}",
            )
        ax.set_yscale("log")
        ax.set_xlabel("Singular-value index")
        ax.set_ylabel("Center-feedback singular value")
        ax.set_title(f"d={dim}, lag=1 memory time")
        ax.grid(alpha=0.25)
        ax.legend(fontsize=8)
    spectra_path = figure_dir / "frozen_source_center_feedback_spectra.png"
    fig.savefig(spectra_path, dpi=180)
    plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.0), constrained_layout=True)
    for dim in dims:
        selected = sorted(
            [row for row in case_results if row["dim"] == dim],
            key=lambda row: row["perturbation_sigma_rep"],
        )
        deltas = [row["perturbation_sigma_rep"] for row in selected]
        gradient_spread = [
            row["quality"]["source_gradient_relative_spread"] for row in selected
        ]
        radius_change = [
            row["quality"]["branch_baseline_radius_max_abs"] for row in selected
        ]
        axes[0].plot(
            deltas,
            np.maximum(gradient_spread, 1e-18),
            marker="o",
            label=f"d={dim}",
        )
        axes[1].plot(
            deltas,
            np.maximum(radius_change, 1e-18),
            marker="o",
            label=f"d={dim}",
        )
    axes[0].set_ylabel("Gradient spread / baseline gradient")
    axes[0].set_title("Finite-difference locality")
    axes[1].set_ylabel("Max |branch radius - baseline radius|")
    axes[1].set_title("Perturbation disturbance")
    for ax in axes:
        ax.set_xlabel("Source perturbation / sigma_rep")
        ax.set_yscale("log")
        ax.grid(alpha=0.25)
        ax.legend(fontsize=8)
    quality_path = figure_dir / "frozen_source_quality.png"
    fig.savefig(quality_path, dpi=180)
    plt.close(fig)
    return response_path, spectra_path, quality_path


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
    results = payload["case_results"]
    rank_lookup = {
        (
            row["dim"],
            row["perturbation_sigma_rep"],
            row["lag_memory_times"],
            row["observable"],
        ): row["energy_rank"]
        for row in payload["rank_rows"]
    }
    lines = [
        "# Frozen localized source pilot",
        "",
        f"Date: {payload['generated_utc']}",
        "",
        "## Decision",
        "",
        "A complete cloned source is placed at one fixed offset from the target.",
        "Its full state is translated locally by plus/minus delta along every",
        "input direction. This differentiates one source configuration instead",
        "of repeating an opposite-side radial basis test.",
        "",
        "All perturbed branches, an unperturbed baseline-source branch, and a free",
        "no-source branch share future noise. eta_zero retains the source field",
        "but removes target self-feedback. eta_cross=0 must reproduce free",
        "propagation exactly.",
        "",
        "One checkpoint per dimension validates the architecture only. It cannot",
        "establish a seed-reproducible rank or an emergent dimension.",
        "",
        "## Cases",
        "",
        "| d | N | radius | separation/radius | interaction fraction |",
        "| ---: | ---: | ---: | ---: | ---: |",
    ]
    for dim in sorted({int(row["dim"]) for row in results}):
        result = next(row for row in results if row["dim"] == dim)
        lines.append(
            f"| {dim} | {result['update_index']} | "
            f"{_fmt(result['initial_radius'])} | "
            f"{_fmt(result['separation_radii'])} | "
            f"{_fmt(result['interaction_fraction'])} |"
        )
    lines.extend(
        [
            "",
            "The fixed source is one effective sigma_rep from the target, which is",
            "thousands of internal memory radii for these checkpoints.",
            "",
            "## Results",
            "",
            "The ranks are descriptive 95%-energy ranks at lag one memory time.",
            "",
            "| d | delta/sigma_rep | delta/radius | eta_cross | realized baseline fraction | max radius perturbation | center rank | shape rank |",
            "| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for result in results:
        key = (result["dim"], result["perturbation_sigma_rep"], 1.0)
        lines.append(
            f"| {result['dim']} | "
            f"{_fmt(result['perturbation_sigma_rep'])} | "
            f"{_fmt(result['perturbation_radii'])} | "
            f"{_fmt(result['calibration']['cross_eta'])} | "
            f"{_fmt(result['quality']['bare_baseline_pulse_fraction'])} | "
            f"{_fmt(result['quality']['branch_baseline_radius_max_abs'])} | "
            f"{rank_lookup[(*key, 'memory_center_feedback')]} | "
            f"{rank_lookup[(*key, 'shape_feedback')]} |"
        )
    lines.extend(
        [
            "",
            "## Controls and convergence",
            "",
            "| d | zero-cross error | center-Jacobian difference | shape-Jacobian difference |",
            "| ---: | ---: | ---: | ---: |",
        ]
    )
    for dim in sorted({int(row["dim"]) for row in results}):
        zero_error = max(
            row["quality"]["zero_cross_max_abs"] for row in results if row["dim"] == dim
        )
        center = next(
            row["relative_difference_max"]
            for row in payload["linearity_rows"]
            if row["dim"] == dim and row["observable"] == "memory_center_feedback"
        )
        shape = next(
            row["relative_difference_max"]
            for row in payload["linearity_rows"]
            if row["dim"] == dim and row["observable"] == "shape_feedback"
        )
        lines.append(f"| {dim} | {_fmt(zero_error)} | {_fmt(center)} | {_fmt(shape)} |")
    lines.extend(
        [
            "",
            "## Source-aligned symmetry audit",
            "",
            "The baseline source lies on axis 1. The table resolves the center-",
            "feedback Jacobian into its radial entry, the mean transverse entry,",
            "and leakage away from this diagonal radial/transverse form.",
            "",
            "| d | delta/sigma_rep | radial | transverse mean | abs ratio | off-diagonal fraction | transverse spread |",
            "| ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    symmetry = [
        row
        for row in payload["symmetry_rows"]
        if row["lag_memory_times"] == 1.0
        and row["observable"] == "memory_center_feedback"
    ]
    for row in symmetry:
        lines.append(
            f"| {row['dim']} | {_fmt(row['perturbation_sigma_rep'])} | "
            f"{_fmt(row['radial_response'])} | "
            f"{_fmt(row['transverse_response_mean'])} | "
            f"{_fmt(row['radial_transverse_abs_ratio'])} | "
            f"{_fmt(row['off_diagonal_fraction'])} | "
            f"{_fmt(row['transverse_relative_spread'])} |"
        )
    lines.extend(
        [
            "",
            "The full ambient ranks split into one radial and d-1 nearly",
            "degenerate transverse responses. This is the symmetry expected from",
            "an isotropic scalar kernel. It is not evidence for selection of three",
            "external dimensions.",
        ]
    )
    response_path, spectra_path, quality_path = figure_paths
    lines.extend(
        [
            "",
            "## Guardrails",
            "",
            "The source is frozen, so this is not synchronization, reciprocal",
            "interaction, retardation, charge, spin, or a particle model. A",
            "descriptive rank from one cloned state must not be interpreted as an",
            "emergent dimension. Independent source and target seeds are required.",
            "",
            "## Figures",
            "",
            f"![Response norms]({_rel_from(report_path, response_path)})",
            "",
            f"![Center spectra]({_rel_from(report_path, spectra_path)})",
            "",
            f"![Quality]({_rel_from(report_path, quality_path)})",
            "",
            "## Next gate",
            "",
            "1. Require exact zero-cross control, non-destructive baseline coupling,",
            "   and agreement of both local finite-difference Jacobians.",
            "2. Form at least six, preferably ten, independent source-target pairs.",
            "3. Test common basis rotations and a small discrete distance set before",
            "   one-way dynamic coupling.",
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
        perturbations = _float_list(args.perturbation_sigma_rep)
        lag_memory_times = _float_list(args.lag_memory_times)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    if len(perturbations) != 2:
        raise SystemExit("--perturbation-sigma-rep must contain exactly two values")
    if 1.0 not in lag_memory_times:
        raise SystemExit("--lag-memory-times must include 1 for the report gate")

    git_revision = _git_output(["rev-parse", "HEAD"])
    git_status = _git_output(["status", "--short"])
    if git_status and not args.allow_dirty:
        raise SystemExit(
            "frozen-source analysis requires a clean worktree; commit changes first"
        )

    case_results: list[dict[str, Any]] = []
    for case in load_checkpoint_cases(args.checkpoint_dir):
        print(f"running frozen source d={case.dim} seed={case.seed}", flush=True)
        case_results.extend(
            run_checkpoint_case(
                case,
                interaction_fraction=args.interaction_fraction,
                perturbation_sigma_rep=perturbations,
                separation_sigma_rep=args.separation_sigma_rep,
                pulse_memory_times=args.pulse_memory_times,
                lag_memory_times=lag_memory_times,
                noise_base_seed=args.noise_base_seed,
            )
        )

    report_path = _resolve(args.report)
    summary_path = _resolve(args.summary_json)
    figure_paths = make_figures(case_results, _resolve(args.figure_dir))
    payload = {
        "schema": "emergenz-knoten.frozen-source-pilot",
        "schema_version": 3,
        "generated_utc": datetime.now(UTC).isoformat(timespec="seconds"),
        "git_revision": git_revision,
        "git_status_at_start": git_status,
        "command": ["python", *os.sys.argv],
        "checkpoint_dir": _rel(_resolve(args.checkpoint_dir)),
        "interaction_fraction": float(args.interaction_fraction),
        "perturbation_sigma_rep": perturbations,
        "separation_sigma_rep": float(args.separation_sigma_rep),
        "pulse_memory_times": float(args.pulse_memory_times),
        "lag_memory_times": lag_memory_times,
        "noise_base_seed": int(args.noise_base_seed),
        "case_results": case_results,
        "rank_rows": rank_rows(case_results),
        "symmetry_rows": symmetry_rows(case_results),
        "linearity_rows": linearity_rows(case_results),
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
