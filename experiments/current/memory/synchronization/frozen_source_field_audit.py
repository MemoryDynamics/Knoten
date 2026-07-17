"""Audit the static potential and drift field of frozen knot checkpoints."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
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
    effective_double_gaussian_parameters,
    load_finite_memory_checkpoint,
    memory_centroid,
    memory_shape_tensor,
    two_scale_force_crossing_radius,
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
class FieldCase:
    path: Path
    seed: int
    update_index: int
    formation_revision: str
    config: SimulationConfig
    state: FiniteMemoryState
    center: np.ndarray
    radius: float
    stored_mass: float

    @property
    def dim(self) -> int:
        return self.state.dim


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit frozen checkpoint potential, force sign, and anisotropy."
    )
    parser.add_argument("--checkpoint-dir", type=Path, default=DEFAULT_CHECKPOINT_DIR)
    parser.add_argument("--radial-points", type=int, default=180)
    parser.add_argument("--random-direction-pairs", type=int, default=48)
    parser.add_argument("--direction-seed", type=int, default=20_260_717)
    parser.add_argument("--allow-dirty", action="store_true")
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("reports/response/frozen_source_field_audit_2026-07-17.md"),
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=Path(
            "reports/response/frozen_source_field_audit_summary_2026-07-17.json"
        ),
    )
    parser.add_argument(
        "--figure-dir",
        type=Path,
        default=Path("figures/draft/response/frozen_source_field_audit_2026-07-17"),
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


def load_field_cases(checkpoint_dir: Path) -> list[FieldCase]:
    cases: list[FieldCase] = []
    for path in sorted(_resolve(checkpoint_dir).glob("*.npz")):
        checkpoint = load_finite_memory_checkpoint(path)
        center = memory_centroid(checkpoint.state)
        radius = float(
            np.sqrt(max(np.trace(memory_shape_tensor(checkpoint.state)), 0.0))
        )
        if radius <= 0.0:
            raise ValueError(f"checkpoint has degenerate memory radius: {path}")
        cases.append(
            FieldCase(
                path=path,
                seed=checkpoint.formation_seed,
                update_index=checkpoint.update_index,
                formation_revision=checkpoint.git_revision,
                config=checkpoint.config,
                state=checkpoint.state,
                center=center,
                radius=radius,
                stored_mass=float(np.sum(checkpoint.state.weights)),
            )
        )
    cases.sort(key=lambda case: (case.dim, case.seed))
    if not cases:
        raise ValueError(f"no checkpoint files found in {_resolve(checkpoint_dir)}")
    return cases


def paired_direction_set(
    state: FiniteMemoryState,
    *,
    random_pairs: int,
    seed: int,
) -> np.ndarray:
    """Return principal-axis and random directions with exact parity partners."""

    if random_pairs < 0:
        raise ValueError("random_pairs must be non-negative")
    _, eigenvectors = np.linalg.eigh(memory_shape_tensor(state))
    principal = eigenvectors.T
    rng = np.random.default_rng(seed)
    random = rng.normal(size=(random_pairs, state.dim))
    if random_pairs:
        random /= np.linalg.norm(random, axis=1)[:, None]
        base = np.vstack([principal, random])
    else:
        base = principal
    return np.vstack([base, -base])


def _radial_grid(
    *,
    radius: float,
    sigma_rep: float,
    sigma_att: float,
    points: int,
) -> np.ndarray:
    if points < 20:
        raise ValueError("radial_points must be at least 20")
    minimum = max(0.25 * radius, np.finfo(float).eps * sigma_rep)
    maximum = 6.0 * sigma_att
    logarithmic = np.geomspace(minimum, maximum, points)
    landmarks = radius * np.asarray([1, 2, 5, 10, 20, 50, 100], dtype=float)
    kernel_scales = sigma_rep * np.asarray(
        [0.003, 0.01, 0.03, 0.1, 0.3, 1.0, 2.0, 3.0],
        dtype=float,
    )
    return np.unique(np.concatenate([logarithmic, landmarks, kernel_scales, [maximum]]))


def _field_on_points(
    points: np.ndarray,
    memory: np.ndarray,
    weights: np.ndarray,
    *,
    sigma_rep: float,
    sigma_att: float,
    amplitude_rep: float,
    amplitude_att: float,
) -> tuple[np.ndarray, np.ndarray]:
    displacement = points[:, None, :] - memory[None, :, :]
    radius2 = np.einsum("nmd,nmd->nm", displacement, displacement)
    rep_exp = np.exp(-0.5 * radius2 / (sigma_rep * sigma_rep))
    att_exp = np.exp(-0.5 * radius2 / (sigma_att * sigma_att))
    potential = amplitude_rep * (rep_exp @ weights) - amplitude_att * (
        att_exp @ weights
    )
    factors = weights[None, :] * (
        -amplitude_rep * rep_exp / (sigma_rep * sigma_rep)
        + amplitude_att * att_exp / (sigma_att * sigma_att)
    )
    gradient = np.einsum("nm,nmd->nd", factors, displacement)
    return potential, gradient


def _relative_rms(numerator: np.ndarray, denominator: np.ndarray) -> float:
    scale = float(np.sqrt(np.mean(np.square(denominator))))
    return float(
        np.sqrt(np.mean(np.square(numerator))) / max(scale, np.finfo(float).tiny)
    )


def _crossings(radii: np.ndarray, values: np.ndarray) -> list[float]:
    crossings: list[float] = []
    for index in range(len(radii) - 1):
        first = float(values[index])
        second = float(values[index + 1])
        if first == 0.0:
            crossings.append(float(radii[index]))
        elif first * second < 0.0:
            fraction = abs(first) / (abs(first) + abs(second))
            log_radius = (1.0 - fraction) * np.log(radii[index]) + fraction * np.log(
                radii[index + 1]
            )
            crossings.append(float(np.exp(log_radius)))
    return crossings


def evaluate_field_case(
    case: FieldCase,
    *,
    radial_points: int,
    random_direction_pairs: int,
    direction_seed: int,
) -> dict[str, Any]:
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
    sigma_att = float(effective["sigma_att"])
    amplitude_rep = float(effective["amplitude_rep"])
    amplitude_att = float(effective["amplitude_att"])
    radii = _radial_grid(
        radius=case.radius,
        sigma_rep=sigma_rep,
        sigma_att=sigma_att,
        points=radial_points,
    )
    directions = paired_direction_set(
        case.state,
        random_pairs=random_direction_pairs,
        seed=direction_seed + 1009 * case.dim + case.seed,
    )
    pair_count = len(directions) // 2
    centered_memory = case.state.memory - case.center[None, :]

    metric_names = (
        "potential_mean",
        "potential_std",
        "potential_min",
        "potential_max",
        "radial_force_mean",
        "radial_force_std",
        "radial_force_min",
        "radial_force_max",
        "tangential_force_rms",
        "tangential_force_max",
        "potential_parity_odd_fraction",
        "radial_force_parity_odd_fraction",
        "force_directional_spread",
        "tangential_force_fraction",
    )
    metrics = {name: np.empty(len(radii), dtype=float) for name in metric_names}
    for radius_index, radial_distance in enumerate(radii):
        points = radial_distance * directions
        potential, gradient = _field_on_points(
            points,
            centered_memory,
            case.state.weights,
            sigma_rep=sigma_rep,
            sigma_att=sigma_att,
            amplitude_rep=amplitude_rep,
            amplitude_att=amplitude_att,
        )
        drift = -gradient
        radial_force = np.einsum("nd,nd->n", drift, directions)
        tangential = drift - radial_force[:, None] * directions
        tangential_norm = np.linalg.norm(tangential, axis=1)
        force_norm = np.linalg.norm(drift, axis=1)
        potential_even = 0.5 * (potential[:pair_count] + potential[pair_count:])
        potential_odd = 0.5 * (potential[:pair_count] - potential[pair_count:])
        force_even = 0.5 * (radial_force[:pair_count] + radial_force[pair_count:])
        force_odd = 0.5 * (radial_force[:pair_count] - radial_force[pair_count:])
        metrics["potential_mean"][radius_index] = np.mean(potential)
        metrics["potential_std"][radius_index] = np.std(potential)
        metrics["potential_min"][radius_index] = np.min(potential)
        metrics["potential_max"][radius_index] = np.max(potential)
        metrics["radial_force_mean"][radius_index] = np.mean(radial_force)
        metrics["radial_force_std"][radius_index] = np.std(radial_force)
        metrics["radial_force_min"][radius_index] = np.min(radial_force)
        metrics["radial_force_max"][radius_index] = np.max(radial_force)
        metrics["tangential_force_rms"][radius_index] = np.sqrt(
            np.mean(np.square(tangential_norm))
        )
        metrics["tangential_force_max"][radius_index] = np.max(tangential_norm)
        metrics["potential_parity_odd_fraction"][radius_index] = _relative_rms(
            potential_odd,
            potential_even,
        )
        metrics["radial_force_parity_odd_fraction"][radius_index] = _relative_rms(
            force_odd,
            force_even,
        )
        metrics["force_directional_spread"][radius_index] = float(
            np.std(radial_force)
            / max(np.sqrt(np.mean(np.square(radial_force))), np.finfo(float).tiny)
        )
        metrics["tangential_force_fraction"][radius_index] = float(
            np.sqrt(np.mean(np.square(tangential_norm)))
            / max(np.sqrt(np.mean(np.square(force_norm))), np.finfo(float).tiny)
        )

    rep_exp = np.exp(-0.5 * np.square(radii / sigma_rep))
    att_exp = np.exp(-0.5 * np.square(radii / sigma_att))
    point_potential = case.stored_mass * (
        amplitude_rep * rep_exp - amplitude_att * att_exp
    )
    point_repulsive_force = (
        case.stored_mass * radii * amplitude_rep * rep_exp / (sigma_rep * sigma_rep)
    )
    point_attractive_force = (
        -case.stored_mass * radii * amplitude_att * att_exp / (sigma_att * sigma_att)
    )
    point_radial_force = point_repulsive_force + point_attractive_force
    potential_scale = np.maximum(
        np.abs(point_potential),
        np.finfo(float).eps * max(abs(point_potential[0]), 1.0),
    )
    force_scale = np.maximum(
        np.abs(point_radial_force),
        np.finfo(float).eps * max(np.max(np.abs(point_radial_force)), 1.0),
    )
    metrics["monopole_potential_relative_error"] = (
        np.abs(metrics["potential_mean"] - point_potential) / potential_scale
    )
    metrics["monopole_force_relative_error"] = (
        np.abs(metrics["radial_force_mean"] - point_radial_force) / force_scale
    )

    crossing = two_scale_force_crossing_radius(
        amplitude_rep=amplitude_rep,
        length_rep=sigma_rep,
        amplitude_att=amplitude_att,
        length_att=sigma_att,
    )
    potential_curvature = amplitude_att / (sigma_att * sigma_att) - amplitude_rep / (
        sigma_rep * sigma_rep
    )
    return {
        "checkpoint": _rel(case.path),
        "dim": case.dim,
        "seed": case.seed,
        "update_index": case.update_index,
        "formation_revision": case.formation_revision,
        "radius": case.radius,
        "stored_mass": case.stored_mass,
        "sigma_rep": sigma_rep,
        "sigma_att": sigma_att,
        "amplitude_rep": amplitude_rep,
        "amplitude_att": amplitude_att,
        "radius_sigma_rep": case.radius / sigma_rep,
        "potential_curvature_at_origin": potential_curvature,
        "analytic_point_force_crossing": crossing,
        "measured_mean_force_crossings": _crossings(
            radii,
            metrics["radial_force_mean"],
        ),
        "direction_count": len(directions),
        "radii": radii,
        "radii_over_radius": radii / case.radius,
        "radii_over_sigma_rep": radii / sigma_rep,
        "point_potential": point_potential,
        "point_radial_force": point_radial_force,
        "point_repulsive_force": point_repulsive_force,
        "point_attractive_force": point_attractive_force,
        **metrics,
    }


def landmark_rows(results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    landmark_specs = (
        ("5 R_mem", "radius", 5.0),
        ("20 R_mem", "radius", 20.0),
        ("100 R_mem", "radius", 100.0),
        ("0.01 sigma_rep", "sigma", 0.01),
        ("0.1 sigma_rep", "sigma", 0.1),
        ("1 sigma_rep", "sigma", 1.0),
    )
    for result in results:
        radii = np.asarray(result["radii"])
        for label, scale, multiplier in landmark_specs:
            target = multiplier * (
                result["radius"] if scale == "radius" else result["sigma_rep"]
            )
            index = int(np.argmin(np.abs(radii - target)))
            minimum = float(result["radial_force_min"][index])
            maximum = float(result["radial_force_max"][index])
            if maximum < 0.0:
                sign = "all inward"
            elif minimum > 0.0:
                sign = "all outward"
            else:
                sign = "mixed"
            rows.append(
                {
                    "dim": result["dim"],
                    "label": label,
                    "radius": float(radii[index]),
                    "radii_over_radius": float(result["radii_over_radius"][index]),
                    "radii_over_sigma_rep": float(
                        result["radii_over_sigma_rep"][index]
                    ),
                    "radial_force_mean": float(result["radial_force_mean"][index]),
                    "force_sign": sign,
                    "force_directional_spread": float(
                        result["force_directional_spread"][index]
                    ),
                    "tangential_force_fraction": float(
                        result["tangential_force_fraction"][index]
                    ),
                    "potential_parity_odd_fraction": float(
                        result["potential_parity_odd_fraction"][index]
                    ),
                    "monopole_force_relative_error": float(
                        result["monopole_force_relative_error"][index]
                    ),
                }
            )
    return rows


def make_figures(
    results: list[dict[str, Any]],
    figure_dir: Path,
) -> tuple[Path, Path, Path]:
    figure_dir.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(
        1,
        len(results),
        figsize=(5.4 * len(results), 4.1),
        squeeze=False,
        constrained_layout=True,
    )
    for column, result in enumerate(results):
        ax = axes[0, column]
        x = np.asarray(result["radii_over_sigma_rep"])
        mass = float(result["stored_mass"])
        mean = np.asarray(result["potential_mean"]) / mass
        ax.fill_between(
            x,
            np.asarray(result["potential_min"]) / mass,
            np.asarray(result["potential_max"]) / mass,
            color="#6aaed6",
            alpha=0.22,
            label="directional range",
        )
        ax.plot(x, mean, color="#1261a0", label="checkpoint mean")
        ax.plot(
            x,
            np.asarray(result["point_potential"]) / mass,
            color="#222222",
            linestyle="--",
            label="point monopole",
        )
        ax.axvline(result["radius_sigma_rep"], color="#d1495b", linestyle=":")
        ax.set_xscale("log")
        ax.set_yscale("symlog", linthresh=1e-5)
        ax.set_xlabel("Distance / sigma_rep")
        ax.set_ylabel("Potential / stored mass")
        ax.set_title(f"d={result['dim']} frozen source")
        ax.grid(alpha=0.25)
        if column == 0:
            ax.legend(fontsize=8)
    potential_path = figure_dir / "frozen_source_potential.png"
    fig.savefig(potential_path, dpi=180)
    plt.close(fig)

    fig, axes = plt.subplots(
        1,
        len(results),
        figsize=(5.4 * len(results), 4.1),
        squeeze=False,
        constrained_layout=True,
    )
    for column, result in enumerate(results):
        ax = axes[0, column]
        x = np.asarray(result["radii_over_sigma_rep"])
        mass = float(result["stored_mass"])
        ax.fill_between(
            x,
            np.asarray(result["radial_force_min"]) / mass,
            np.asarray(result["radial_force_max"]) / mass,
            color="#6aaed6",
            alpha=0.22,
            label="directional range",
        )
        ax.plot(
            x,
            np.asarray(result["radial_force_mean"]) / mass,
            color="#1261a0",
            label="checkpoint radial drift",
        )
        ax.plot(
            x,
            np.asarray(result["point_repulsive_force"]) / mass,
            color="#d1495b",
            linestyle=":",
            label="repulsive component",
        )
        ax.plot(
            x,
            np.asarray(result["point_attractive_force"]) / mass,
            color="#3a7d44",
            linestyle=":",
            label="attractive component",
        )
        ax.plot(
            x,
            np.asarray(result["point_radial_force"]) / mass,
            color="#222222",
            linestyle="--",
            label="point net drift",
        )
        ax.axhline(0.0, color="#555555", linewidth=0.8)
        ax.axvline(result["radius_sigma_rep"], color="#d1495b", linestyle=":")
        ax.set_xscale("log")
        ax.set_yscale("symlog", linthresh=1e-7)
        ax.set_xlabel("Distance / sigma_rep")
        ax.set_ylabel("Outward radial drift / stored mass")
        ax.set_title(f"d={result['dim']}: negative is attraction")
        ax.grid(alpha=0.25)
        if column == 0:
            ax.legend(fontsize=7)
    force_path = figure_dir / "frozen_source_radial_force.png"
    fig.savefig(force_path, dpi=180)
    plt.close(fig)

    fig, axes = plt.subplots(
        1,
        len(results),
        figsize=(5.4 * len(results), 4.1),
        squeeze=False,
        constrained_layout=True,
    )
    for column, result in enumerate(results):
        ax = axes[0, column]
        x = np.asarray(result["radii_over_sigma_rep"])
        series = (
            ("force directional spread", "force_directional_spread", "#1261a0"),
            ("tangential force fraction", "tangential_force_fraction", "#d1495b"),
            (
                "potential parity-odd fraction",
                "potential_parity_odd_fraction",
                "#3a7d44",
            ),
            ("monopole force error", "monopole_force_relative_error", "#6f4e7c"),
        )
        for label, key, color in series:
            ax.plot(
                x,
                np.maximum(np.asarray(result[key]), 1e-18),
                label=label,
                color=color,
            )
        ax.axvline(result["radius_sigma_rep"], color="#d1495b", linestyle=":")
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_xlabel("Distance / sigma_rep")
        ax.set_ylabel("Relative diagnostic")
        ax.set_title(f"d={result['dim']} source structure")
        ax.grid(alpha=0.25)
        if column == 0:
            ax.legend(fontsize=7)
    structure_path = figure_dir / "frozen_source_structure_decay.png"
    fig.savefig(structure_path, dpi=180)
    plt.close(fig)
    return potential_path, force_path, structure_path


def _fmt(value: float | None) -> str:
    if value is None:
        return "none"
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
    lines = [
        "# Frozen-source potential and force audit",
        "",
        f"Date: {payload['generated_utc']}",
        "",
        "## Decision",
        "",
        "The observed displacement toward the cloned source is already fixed by",
        "the selected scalar kernel. For the current A_att=35 slice, the broad",
        "attractive curvature exceeds the short repulsive curvature at the origin",
        "and remains dominant at larger radius. The point-source branch therefore",
        "has no force-sign crossing.",
        "",
        "This audit evaluates the complete retained checkpoint field without",
        "renormalizing its truncated memory mass. Potential zero is at infinity;",
        "negative radial drift means attraction toward the source centre.",
        "",
        "The landmarks cover 5, 20, and 100 memory radii and 0.01, 0.1, and",
        "1 effective repulsive-kernel width.",
        "",
        "## Kernel and source scale",
        "",
        "| d | R_mem/sigma_rep | stored mass | Phi'' point at 0 | point crossing | measured mean crossings |",
        "| ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for result in results:
        measured = result["measured_mean_force_crossings"]
        measured_text = ", ".join(_fmt(value) for value in measured) or "none"
        lines.append(
            f"| {result['dim']} | {_fmt(result['radius_sigma_rep'])} | "
            f"{_fmt(result['stored_mass'])} | "
            f"{_fmt(result['potential_curvature_at_origin'])} | "
            f"{_fmt(result['analytic_point_force_crossing'])} | {measured_text} |"
        )
    lines.extend(
        [
            "",
            "Positive Phi'' at the point-source origin is a local potential minimum,",
            "so the canonical update -eta grad(Phi) is restoring/attractive there.",
            "For q=sigma_att/sigma_rep=3, a repulsive point core would require",
            "A_att/A_rep < 9; the present ratio is 35.",
            "",
            "## Distance landmarks",
            "",
            "| d | distance | r/R_mem | r/sigma_rep | radial drift | sign over directions | directional spread | tangential fraction | parity-odd Phi | monopole-force error |",
            "| ---: | --- | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in payload["landmark_rows"]:
        lines.append(
            f"| {row['dim']} | {row['label']} | "
            f"{_fmt(row['radii_over_radius'])} | "
            f"{_fmt(row['radii_over_sigma_rep'])} | "
            f"{_fmt(row['radial_force_mean'])} | {row['force_sign']} | "
            f"{_fmt(row['force_directional_spread'])} | "
            f"{_fmt(row['tangential_force_fraction'])} | "
            f"{_fmt(row['potential_parity_odd_fraction'])} | "
            f"{_fmt(row['monopole_force_relative_error'])} |"
        )
    landmark_values = payload["landmark_rows"]
    max_monopole_error = max(
        row["monopole_force_relative_error"] for row in landmark_values
    )
    max_directional_spread = max(
        row["force_directional_spread"] for row in landmark_values
    )
    max_tangential_fraction = max(
        row["tangential_force_fraction"] for row in landmark_values
    )
    lines.extend(
        [
            "",
            "Across the listed near-to-far landmarks, the maximum point-monopole",
            f"force error is {_fmt(max_monopole_error)}, directional spread is",
            f"{_fmt(max_directional_spread)}, and tangential fraction is",
            f"{_fmt(max_tangential_fraction)}. The current read kernel therefore",
            "does not resolve the internal source cloud even at five memory radii.",
            "One checkpoint per dimension makes this a pathwise scale audit.",
        ]
    )
    lines.extend(
        [
            "",
            "## Interpretation guardrails",
            "",
            "The memory density is non-negative and supplies a positive scalar",
            "monopole. It currently has no knot-specific charge sign. A scalar",
            "field is parity-even; an individual finite cloud can still carry small",
            "odd higher moments, measured here by the parity-paired directions.",
            "Parity does not supply electric-charge sign; that is an internal",
            "or charge-conjugation label.",
            "Charge neutrality would suppress a leading signed monopole, not explain",
            "this universal attraction. A signed scalar channel is the minimal way",
            "to test like/unlike charge. Vector memory is a separate candidate for",
            "orientation, phase, circulation, or polarization.",
            "",
            "The source remains frozen and the target is absent from this static",
            "calculation. This is a one-way field audit, not evidence for reciprocal",
            "two-knot attraction, conservation laws, electromagnetism, or gravity.",
            "",
            "## Next gate",
            "",
            "1. The calibrated distance ladder now tests these six landmarks",
            "   as target-deformation scales, not as source-structure probes.",
            "2. Treat the present rho channel as an unsigned scalar mass-like",
            "   interaction unless a separate charge observable is introduced.",
            "3. Specify a signed scalar cross-channel with q=0 and sign-reversal",
            "   controls before adding oriented memory solely to obtain charge.",
            "4. Reserve vector memory for phase, circulation, or polarization.",
            "",
            "## Figures",
            "",
        ]
    )
    potential_path, force_path, structure_path = figure_paths
    lines.extend(
        [
            f"![Potential]({_rel_from(report_path, potential_path)})",
            "",
            f"![Radial force]({_rel_from(report_path, force_path)})",
            "",
            f"![Structure decay]({_rel_from(report_path, structure_path)})",
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
    if args.radial_points < 20:
        raise SystemExit("--radial-points must be at least 20")
    if args.random_direction_pairs < 0:
        raise SystemExit("--random-direction-pairs must be non-negative")
    git_revision = _git_output(["rev-parse", "HEAD"])
    git_status = _git_output(["status", "--short"])
    if git_status and not args.allow_dirty:
        raise SystemExit("field audit requires a clean worktree; commit changes first")

    case_results = [
        evaluate_field_case(
            case,
            radial_points=args.radial_points,
            random_direction_pairs=args.random_direction_pairs,
            direction_seed=args.direction_seed,
        )
        for case in load_field_cases(args.checkpoint_dir)
    ]
    report_path = _resolve(args.report)
    summary_path = _resolve(args.summary_json)
    figure_paths = make_figures(case_results, _resolve(args.figure_dir))
    payload = {
        "schema": "emergenz-knoten.frozen-source-field-audit",
        "schema_version": 1,
        "generated_utc": datetime.now(UTC).isoformat(timespec="seconds"),
        "git_revision": git_revision,
        "git_status_at_start": git_status,
        "command": ["python", *os.sys.argv],
        "checkpoint_dir": _rel(_resolve(args.checkpoint_dir)),
        "radial_points": int(args.radial_points),
        "random_direction_pairs": int(args.random_direction_pairs),
        "direction_seed": int(args.direction_seed),
        "case_results": case_results,
        "landmark_rows": landmark_rows(case_results),
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
