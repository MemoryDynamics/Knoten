"""Gate a passive oriented source memory against randomized controls."""

from __future__ import annotations

import argparse
from datetime import UTC, datetime
import glob
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
    initialize_oriented_memory_state,
    memory_centroid,
    memory_shape_tensor,
    one_way_oriented_response,
    place_oriented_memory_state,
    vector_gaussian_field,
)


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
        description="One-way gate for an independently relaxing oriented source state."
    )
    parser.add_argument("--case-glob", action="append", default=None)
    parser.add_argument("--seeds", default="1,2,3,4,5,6")
    parser.add_argument("--memory-times", type=float, default=20.0)
    parser.add_argument("--trace-points", type=int, default=100)
    parser.add_argument("--lambda-vector", type=float, default=None)
    parser.add_argument("--orientation-relaxation", type=float, default=None)
    parser.add_argument("--vector-mass", type=float, default=1.0)
    parser.add_argument("--sigma-ratio", type=float, default=2.5)
    parser.add_argument("--separation-ratio", type=float, default=2.5)
    parser.add_argument("--response-fraction", type=float, default=0.03)
    parser.add_argument("--randomizations", type=int, default=16)
    parser.add_argument("--random-quantile", type=float, default=0.95)
    parser.add_argument("--response-min-r", type=float, default=1e-3)
    parser.add_argument("--null-separation-min", type=float, default=2.0)
    parser.add_argument("--memory-gain-min", type=float, default=1.25)
    parser.add_argument("--flip-cosine-max", type=float, default=-0.9)
    parser.add_argument("--flip-magnitude-min", type=float, default=0.5)
    parser.add_argument("--flip-magnitude-max", type=float, default=2.0)
    parser.add_argument("--tangential-fraction-min", type=float, default=0.5)
    parser.add_argument("--target-radius-max-change", type=float, default=0.1)
    parser.add_argument("--target-shape-max-change", type=float, default=0.1)
    parser.add_argument("--source-radius-max-change", type=float, default=0.5)
    parser.add_argument("--source-spectrum-max-drift", type=float, default=0.25)
    parser.add_argument("--minimum-passing-seeds", type=int, default=5)
    parser.add_argument("--noise-seed", type=int, default=20_260_725)
    parser.add_argument("--allow-dirty", action="store_true")
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("reports/response/oriented_vector_one_way_gate_2026-07-25.md"),
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=Path("reports/response/oriented_vector_one_way_gate_2026-07-25.json"),
    )
    parser.add_argument(
        "--figure",
        type=Path,
        default=Path(
            "figures/draft/response/oriented_vector_one_way_gate_2026-07-25.png"
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


def _jsonable(value: Any) -> Any:
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        number = float(value)
        return number if np.isfinite(number) else None
    if isinstance(value, Path):
        return _relative(value)
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    return value


def parse_seeds(text: str) -> list[int]:
    seeds = [int(part.strip()) for part in text.split(",") if part.strip()]
    if not seeds or len(seeds) != len(set(seeds)) or any(seed < 0 for seed in seeds):
        raise ValueError("seeds must be unique non-negative integers")
    return seeds


def make_sample_steps(n_steps: int, trace_points: int) -> np.ndarray:
    if n_steps < 1 or trace_points < 3:
        raise ValueError("n_steps and trace_points must be positive")
    linear = np.rint(np.linspace(0, n_steps, trace_points + 1)).astype(int)
    logarithmic = np.rint(np.geomspace(1, n_steps, trace_points, endpoint=True)).astype(
        int
    )
    return np.unique(np.concatenate(([0, n_steps], linear, logarithmic)))


def discover_cases(patterns: list[str], seeds: list[int]) -> list[Path]:
    paths: list[Path] = []
    for pattern in patterns:
        resolved = pattern if Path(pattern).is_absolute() else str(ROOT / pattern)
        paths.extend(Path(path) for path in glob.glob(resolved))
    unique = sorted(set(path.resolve() for path in paths))
    selected: dict[int, Path] = {}
    for path in unique:
        payload = json.loads(path.read_text(encoding="utf-8"))
        seed = int(payload["seed"])
        if seed in seeds:
            if seed in selected:
                raise ValueError(f"duplicate case for seed {seed}")
            selected[seed] = path
    missing = sorted(set(seeds) - set(selected))
    if missing:
        raise ValueError(f"missing cases for seeds {missing}")
    return [selected[seed] for seed in seeds]


def load_snapshot_case(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("condition") != "baseline":
        raise ValueError(f"{path} is not a baseline case")
    config = SimulationConfig(**payload["config"])
    snapshot = payload["diagnostics"]["memory_cloud"]["snapshot"]
    points = np.asarray(snapshot["points"], dtype=float)
    weights = np.asarray(snapshot["weights"], dtype=float)
    if points.ndim != 2 or points.shape[1] != config.dim:
        raise ValueError(f"invalid memory snapshot shape in {path}")
    if weights.shape != (points.shape[0],) or points.shape[0] < 2:
        raise ValueError(f"invalid memory weights in {path}")
    state = FiniteMemoryState(x=points[0], memory=points, weights=weights)
    return {
        "path": path,
        "seed": int(payload["seed"]),
        "config": config,
        "state": state,
        "formation_revision": payload.get("git_revision", "unavailable"),
        "formation_updates": int(payload["config"]["steps"]),
        "formation_git_status": payload.get("git_status", "unavailable"),
    }


def _shape_spectra(tensors: np.ndarray) -> np.ndarray:
    values = np.linalg.eigvalsh(np.asarray(tensors, dtype=float))
    values = np.clip(values, 0.0, None)
    totals = np.sum(values, axis=-1, keepdims=True)
    return np.divide(values, totals, out=np.zeros_like(values), where=totals > 0.0)


def response_metrics(
    response: Any,
    *,
    radius: float,
    radial_direction: np.ndarray,
    random_quantile: float,
) -> dict[str, Any]:
    centers = np.asarray(response.target_memory_centers, dtype=float)
    active_delta = centers[:, 0] - centers[:, 2]
    flip_delta = centers[:, 1] - centers[:, 2]
    random_delta = centers[:, 3:] - centers[:, 2, None, :]
    active_norm = np.linalg.norm(active_delta, axis=1)
    flip_norm = np.linalg.norm(flip_delta, axis=1)
    random_norm = np.linalg.norm(random_delta, axis=2)
    random_threshold = np.quantile(random_norm, random_quantile, axis=1)
    final_active = active_delta[-1]
    final_flip = flip_delta[-1]
    final_active_norm = float(active_norm[-1])
    final_flip_norm = float(flip_norm[-1])
    denominator = max(final_active_norm * final_flip_norm, np.finfo(float).tiny)
    flip_cosine = float(np.dot(final_active, final_flip) / denominator)
    tangential = (
        final_active - np.dot(final_active, radial_direction) * radial_direction
    )
    tangential_fraction = float(
        np.linalg.norm(tangential) / max(final_active_norm, np.finfo(float).tiny)
    )
    target_radius_change = float(
        np.max(
            np.abs(
                response.target_radius_ratios[:, 0]
                / response.target_radius_ratios[:, 2]
                - 1.0
            )
        )
    )
    active_tensors = np.asarray(response.target_shape_tensors[:, 0], dtype=float)
    off_tensors = np.asarray(response.target_shape_tensors[:, 2], dtype=float)
    tensor_denominator = np.maximum(
        np.trace(off_tensors, axis1=1, axis2=2),
        np.finfo(float).tiny,
    )
    target_shape_change = float(
        np.max(
            np.linalg.norm(active_tensors - off_tensors, axis=(1, 2))
            / tensor_denominator
        )
    )
    source_spectra = _shape_spectra(response.source_shape_tensors)
    source_spectrum_drift = float(
        np.max(np.linalg.norm(source_spectra - source_spectra[0], axis=1))
    )
    final_random_threshold = float(random_threshold[-1])
    return {
        "active_response_r": final_active_norm / radius,
        "random_threshold_r": final_random_threshold / radius,
        "null_separation": final_active_norm
        / max(final_random_threshold, np.finfo(float).tiny),
        "flip_cosine": flip_cosine,
        "flip_magnitude_ratio": final_flip_norm
        / max(final_active_norm, np.finfo(float).tiny),
        "tangential_fraction": tangential_fraction,
        "target_radius_max_change": target_radius_change,
        "target_shape_max_change": target_shape_change,
        "source_radius_max_change": float(
            np.max(np.abs(response.source_radius_ratios - 1.0))
        ),
        "source_spectrum_max_drift": source_spectrum_drift,
        "carrier_initial_norm": float(
            np.linalg.norm(response.source_carrier_orientations[0])
        ),
        "carrier_final_norm": float(
            np.linalg.norm(response.source_carrier_orientations[-1])
        ),
        "trace_active_response_r": active_norm / radius,
        "trace_random_threshold_r": random_threshold / radius,
    }


def classify_case(
    persistent: dict[str, Any],
    one_step: dict[str, Any],
    thresholds: dict[str, float],
) -> tuple[dict[str, bool], float, bool]:
    memory_gain = float(
        persistent["null_separation"]
        / max(one_step["null_separation"], np.finfo(float).tiny)
    )
    gates = {
        "response": bool(
            persistent["active_response_r"] >= thresholds["response_min_r"]
        ),
        "random_sign": bool(
            persistent["null_separation"] >= thresholds["null_separation_min"]
        ),
        "persistent_memory": bool(memory_gain >= thresholds["memory_gain_min"]),
        "sign_flip": bool(
            persistent["flip_cosine"] <= thresholds["flip_cosine_max"]
            and thresholds["flip_magnitude_min"]
            <= persistent["flip_magnitude_ratio"]
            <= thresholds["flip_magnitude_max"]
        ),
        "transverse": bool(
            persistent["tangential_fraction"] >= thresholds["tangential_fraction_min"]
        ),
        "target_shape_bounded": bool(
            persistent["target_radius_max_change"]
            <= thresholds["target_radius_max_change"]
            and persistent["target_shape_max_change"]
            <= thresholds["target_shape_max_change"]
        ),
        "source_shape_bounded": bool(
            persistent["source_radius_max_change"]
            <= thresholds["source_radius_max_change"]
            and persistent["source_spectrum_max_drift"]
            <= thresholds["source_spectrum_max_drift"]
        ),
    }
    return gates, memory_gain, all(gates.values())


def run_case(
    case: dict[str, Any],
    args: argparse.Namespace,
    sample_steps: np.ndarray,
    thresholds: dict[str, float],
) -> dict[str, Any]:
    state = case["state"]
    config = case["config"]
    lambda_vector = (
        float(config.alpha) if args.lambda_vector is None else float(args.lambda_vector)
    )
    orientation_relaxation = (
        lambda_vector
        if args.orientation_relaxation is None
        else float(args.orientation_relaxation)
    )
    radius = float(np.sqrt(np.trace(memory_shape_tensor(state))))
    if radius <= 0.0:
        raise ValueError(f"seed {case['seed']} has zero memory radius")
    vector_sigma = float(args.sigma_ratio * radius)
    offset = np.zeros(config.dim, dtype=float)
    offset[0] = float(args.separation_ratio * radius)
    persistent_state = initialize_oriented_memory_state(
        state,
        lambda_vector=lambda_vector,
        vector_mass=args.vector_mass,
        orientation_relaxation=orientation_relaxation,
    )
    placed = place_oriented_memory_state(
        persistent_state,
        memory_centroid(state) + offset,
    )
    initial_field = vector_gaussian_field(
        memory_centroid(state),
        placed.scalar_state.memory,
        placed.orientations,
        placed.weights,
        sigma=vector_sigma,
    )
    initial_field_norm = float(np.linalg.norm(initial_field))
    if initial_field_norm <= np.finfo(float).tiny:
        raise ValueError(f"seed {case['seed']} has zero calibrated vector field")
    vector_eta = float(
        args.response_fraction * radius * lambda_vector / initial_field_norm
    )
    n_steps = int(sample_steps[-1])
    rng = np.random.default_rng(args.noise_seed + 10_007 * case["seed"])
    target_noise = rng.normal(size=(n_steps, config.dim))
    source_noise = rng.normal(size=(n_steps, config.dim))
    sign_seed = args.noise_seed + 100_003 * case["seed"]
    persistent_response = one_way_oriented_response(
        state,
        persistent_state,
        config,
        source_center_offset=offset,
        target_noise=target_noise,
        source_noise=source_noise,
        sample_steps=sample_steps,
        vector_eta=vector_eta,
        vector_sigma=vector_sigma,
        randomization_count=args.randomizations,
        random_seed=sign_seed,
    )
    one_step_state = initialize_oriented_memory_state(
        state,
        lambda_vector=1.0,
        vector_mass=args.vector_mass,
        orientation_relaxation=1.0,
    )
    one_step_response = one_way_oriented_response(
        state,
        one_step_state,
        config,
        source_center_offset=offset,
        target_noise=target_noise,
        source_noise=source_noise,
        sample_steps=sample_steps,
        vector_eta=vector_eta,
        vector_sigma=vector_sigma,
        randomization_count=args.randomizations,
        random_seed=sign_seed,
    )
    radial_direction = -offset / np.linalg.norm(offset)
    persistent_metrics = response_metrics(
        persistent_response,
        radius=radius,
        radial_direction=radial_direction,
        random_quantile=args.random_quantile,
    )
    one_step_metrics = response_metrics(
        one_step_response,
        radius=radius,
        radial_direction=radial_direction,
        random_quantile=args.random_quantile,
    )
    gates, memory_gain, case_pass = classify_case(
        persistent_metrics,
        one_step_metrics,
        thresholds,
    )
    return {
        "seed": case["seed"],
        "case_path": _relative(case["path"]),
        "formation_revision": case["formation_revision"],
        "formation_updates": case["formation_updates"],
        "formation_git_status": case["formation_git_status"],
        "dim": config.dim,
        "memory_radius": radius,
        "lambda_vector": lambda_vector,
        "orientation_relaxation": orientation_relaxation,
        "vector_mass": float(args.vector_mass),
        "vector_sigma": vector_sigma,
        "vector_sigma_over_radius": float(args.sigma_ratio),
        "separation_over_radius": float(args.separation_ratio),
        "separation_over_combined_radius": float(args.separation_ratio / 2.0),
        "initial_field_norm": initial_field_norm,
        "vector_eta": vector_eta,
        "persistent": persistent_metrics,
        "one_step": one_step_metrics,
        "memory_gain": memory_gain,
        "gates": gates,
        "case_pass": case_pass,
    }


def make_figure(
    rows: list[dict[str, Any]], payload: dict[str, Any], path: Path
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    colors = plt.cm.viridis(np.linspace(0.08, 0.92, len(rows)))
    memory_times = np.asarray(payload["trace_memory_times"], dtype=float)
    tiny = np.finfo(float).tiny
    fig, axes = plt.subplots(2, 2, figsize=(10.8, 7.2), constrained_layout=True)
    for row, color in zip(rows, colors, strict=True):
        persistent = row["persistent"]
        axes[0, 0].plot(
            memory_times,
            np.maximum(persistent["trace_active_response_r"], tiny),
            color=color,
            label=f"seed {row['seed']}",
        )
        axes[0, 0].plot(
            memory_times,
            np.maximum(persistent["trace_random_threshold_r"], tiny),
            color=color,
            linestyle=":",
            alpha=0.75,
        )
    axes[0, 0].set_yscale("log")
    axes[0, 0].set_xlabel("persistent vector-memory times")
    axes[0, 0].set_ylabel("response / R_mem")
    axes[0, 0].set_title("Active (solid) vs random-sign q95 (dotted)")
    axes[0, 0].legend(fontsize=7, ncol=2)

    seeds = np.asarray([row["seed"] for row in rows])
    persistent_separation = np.asarray(
        [row["persistent"]["null_separation"] for row in rows]
    )
    one_step_separation = np.asarray(
        [row["one_step"]["null_separation"] for row in rows]
    )
    axes[0, 1].plot(seeds, persistent_separation, "o-", label="persistent")
    axes[0, 1].plot(seeds, one_step_separation, "s--", label="one-step")
    axes[0, 1].axhline(
        payload["thresholds"]["null_separation_min"],
        color="#555555",
        linestyle=":",
        label="persistent threshold",
    )
    axes[0, 1].set_xlabel("formation seed")
    axes[0, 1].set_ylabel("active / random-sign q95")
    axes[0, 1].set_title("Conditional null separation")
    axes[0, 1].legend(fontsize=8)

    flip = np.asarray([row["persistent"]["flip_cosine"] for row in rows])
    transverse = np.asarray([row["persistent"]["tangential_fraction"] for row in rows])
    axes[1, 0].plot(seeds, flip, "o-", label="flip cosine")
    axes[1, 0].plot(seeds, transverse, "s--", label="tangential fraction")
    axes[1, 0].axhline(
        payload["thresholds"]["flip_cosine_max"],
        color="#555555",
        linestyle=":",
    )
    axes[1, 0].axhline(
        payload["thresholds"]["tangential_fraction_min"],
        color="#888888",
        linestyle=":",
    )
    axes[1, 0].set_xlabel("formation seed")
    axes[1, 0].set_ylabel("dimensionless")
    axes[1, 0].set_title("Relational orientation controls")
    axes[1, 0].legend(fontsize=8)

    source_radius = np.asarray(
        [row["persistent"]["source_radius_max_change"] for row in rows]
    )
    target_radius = np.asarray(
        [row["persistent"]["target_radius_max_change"] for row in rows]
    )
    target_shape = np.asarray(
        [row["persistent"]["target_shape_max_change"] for row in rows]
    )
    axes[1, 1].plot(seeds, np.maximum(source_radius, tiny), "o-", label="source radius")
    axes[1, 1].plot(
        seeds, np.maximum(target_radius, tiny), "s--", label="target radius"
    )
    axes[1, 1].plot(seeds, np.maximum(target_shape, tiny), "^:", label="target shape")
    axes[1, 1].set_yscale("log")
    axes[1, 1].set_xlabel("formation seed")
    axes[1, 1].set_ylabel("maximum relative change")
    axes[1, 1].set_title("Shape-boundedness diagnostics")
    axes[1, 1].legend(fontsize=8)
    for axis in axes.flat:
        axis.grid(alpha=0.25)
    fig.suptitle("Passive oriented source: one-way controlled gate")
    fig.savefig(path, dpi=180)
    plt.close(fig)


def _fmt(value: float) -> str:
    if value == 0.0:
        return "0"
    if abs(value) < 1e-3 or abs(value) >= 1e3:
        return f"{value:.3e}"
    return f"{value:.4f}"


def build_report(payload: dict[str, Any], report_path: Path, figure_path: Path) -> str:
    decision = payload["decision"]
    lines = [
        "# Oriented vector one-way gate",
        "",
        f"Date: {payload['generated_utc']}",
        "",
        "## Question and model increment",
        "",
        "Does one additional passively generated vector-memory fibre produce a",
        "reproducible transverse one-way response beyond sign-randomized deposits",
        "while source and target remain shape-bounded? The added orientation obeys",
        "",
        "```text",
        "u[n+1] = (1-kappa) u[n] + kappa normalize(x[n+1]-x[n])",
        "p[n+1] = (1-lambda_v) p[n] + lambda_v M_v u[n+1] G_v",
        "x_T[n+1] = F_scalar(x_T[n], rho_T[n], xi_T[n]) + eta_v p[n](x_T[n])",
        "```",
        "",
        "with `kappa=lambda_v=alpha` in the primary arm. The source remains",
        "autonomous and scalar; the target reads `p` instantaneously. This is not",
        "a retardation, propagation-speed, phase, spin, photon, or particle test.",
        "",
        "## Preregistered controls and stop rule",
        "",
        f"- six independent d=3 scalar formations at N={payload['formation_updates']:,};",
        f"- stop after {payload['memory_times']:g} persistent memory times;",
        f"- {payload['randomizations']} depositwise random-sign paths and q={payload['random_quantile']:.2f};",
        "- exact channel-off path, global sign flip, and lambda_v=kappa=1 one-step control;",
        "- common target/source future noise within each seed;",
        "- coupling calibrated before continuation to 0.03 R_mem per persistent memory time",
        "  from the initial field by the same predefined statewise normalization.",
        "",
        "A seed passes only if response, random-sign separation, persistent-memory",
        "gain, sign reversal, transverse fraction, and both shape bounds pass.",
        (
            f"Numerical gates: active/R >= {_fmt(payload['thresholds']['response_min_r'])}; "
            f"active/random-q95 >= {_fmt(payload['thresholds']['null_separation_min'])}; "
            f"persistent/one-step separation >= {_fmt(payload['thresholds']['memory_gain_min'])}; "
            f"flip cosine <= {_fmt(payload['thresholds']['flip_cosine_max'])}; "
            f"tangential fraction >= {_fmt(payload['thresholds']['tangential_fraction_min'])}."
        ),
        (
            f"Shape bounds: target radius <= {_fmt(payload['thresholds']['target_radius_max_change'])}; "
            f"target tensor <= {_fmt(payload['thresholds']['target_shape_max_change'])}; "
            f"source radius <= {_fmt(payload['thresholds']['source_radius_max_change'])}; "
            f"source spectrum <= {_fmt(payload['thresholds']['source_spectrum_max_drift'])}."
        ),
        f"Overall pass requires at least {payload['minimum_passing_seeds']} of {len(payload['rows'])} seeds.",
        "",
        "## Decision",
        "",
        f"Gate status: **{decision['status']}** ({decision['passing_seeds']}/{decision['seed_count']} seeds).",
        "",
        f"Selected next step: **{decision['selected_next_step']}**.",
        "",
        "## Seed results",
        "",
        "| seed | active/R | random q95/R | active/q95 | one-step/q95 | memory gain | flip cos | tangent frac | target radius | target shape | source radius | source spectrum | pass |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in payload["rows"]:
        persistent = row["persistent"]
        one_step = row["one_step"]
        lines.append(
            f"| {row['seed']} | {_fmt(persistent['active_response_r'])} | "
            f"{_fmt(persistent['random_threshold_r'])} | "
            f"{_fmt(persistent['null_separation'])} | "
            f"{_fmt(one_step['null_separation'])} | {_fmt(row['memory_gain'])} | "
            f"{_fmt(persistent['flip_cosine'])} | "
            f"{_fmt(persistent['tangential_fraction'])} | "
            f"{_fmt(persistent['target_radius_max_change'])} | "
            f"{_fmt(persistent['target_shape_max_change'])} | "
            f"{_fmt(persistent['source_radius_max_change'])} | "
            f"{_fmt(persistent['source_spectrum_max_drift'])} | "
            f"{'pass' if row['case_pass'] else 'fail'} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation boundary",
            "",
            "A pass would establish only that the deliberately introduced",
            "persistent orientation state carries a controlled relational signal",
            "more coherently than its randomized and one-step controls. Persistence",
            "is part of the model increment, not an emergent discovery. It would",
            "justify a longer locality/retardation test, not physical wave language.",
            "",
            "A fail stops this exact vector-state formulation; coupling amplitudes",
            "must not be retuned seed by seed after observing the outcome.",
            "",
            "## Figure",
            "",
            f"![Oriented one-way gate]({_relative_from(report_path, figure_path)})",
            "",
            "## Reproducibility",
            "",
            f"- Analysis revision: {payload['git_revision']}",
            f"- Worktree at start: `{payload['git_status_at_start'] or 'clean'}`",
            f"- Summary: {_relative(payload['summary_json'])}",
            f"- Command: {' '.join(payload['command'])}",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    args = parse_args()
    try:
        seeds = parse_seeds(args.seeds)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    if args.memory_times <= 0.0 or args.trace_points < 3:
        raise SystemExit("memory-times and trace-points must be positive")
    if args.vector_mass <= 0.0:
        raise SystemExit("vector-mass must be positive for field calibration")
    if args.sigma_ratio <= 0.0 or args.separation_ratio <= 0.0:
        raise SystemExit("sigma and separation ratios must be positive")
    if args.response_fraction <= 0.0 or args.randomizations < 8:
        raise SystemExit("response-fraction must be positive and randomizations >= 8")
    if not 0.5 < args.random_quantile < 1.0:
        raise SystemExit("random-quantile must lie between 0.5 and 1")
    if args.orientation_relaxation is not None and not (
        0.0 < args.orientation_relaxation <= 1.0
    ):
        raise SystemExit("orientation-relaxation must lie in (0, 1]")
    if args.response_min_r <= 0.0:
        raise SystemExit("response-min-r must be positive")
    if args.null_separation_min <= 0.0 or args.memory_gain_min <= 0.0:
        raise SystemExit("null-separation-min and memory-gain-min must be positive")
    if not -1.0 <= args.flip_cosine_max <= 1.0:
        raise SystemExit("flip-cosine-max must lie in [-1, 1]")
    if args.flip_magnitude_min < 0.0 or (
        args.flip_magnitude_max < args.flip_magnitude_min
    ):
        raise SystemExit("flip magnitude bounds must be non-negative and ordered")
    if not 0.0 <= args.tangential_fraction_min <= 1.0:
        raise SystemExit("tangential-fraction-min must lie in [0, 1]")
    shape_bounds = (
        args.target_radius_max_change,
        args.target_shape_max_change,
        args.source_radius_max_change,
        args.source_spectrum_max_drift,
    )
    if any(bound < 0.0 for bound in shape_bounds):
        raise SystemExit("shape-change bounds must be non-negative")
    if not 1 <= args.minimum_passing_seeds <= len(seeds):
        raise SystemExit("minimum-passing-seeds must fit the seed count")
    git_revision = _git_output(["rev-parse", "HEAD"])
    git_status = _git_output(["status", "--short"])
    if git_status and not args.allow_dirty:
        raise SystemExit("oriented vector gate requires a clean worktree")
    patterns = list(DEFAULT_CASE_GLOBS if args.case_glob is None else args.case_glob)
    try:
        paths = discover_cases(patterns, seeds)
        cases = [load_snapshot_case(path) for path in paths]
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        raise SystemExit(str(exc)) from exc
    configurations = [case["config"] for case in cases]
    first_config = configurations[0]
    if any(config != first_config for config in configurations[1:]):
        raise SystemExit("all formation cases must share one SimulationConfig")
    lambda_vector = (
        float(first_config.alpha)
        if args.lambda_vector is None
        else float(args.lambda_vector)
    )
    if not 0.0 < lambda_vector <= 1.0:
        raise SystemExit("lambda-vector must lie in (0, 1]")
    n_steps = int(np.ceil(args.memory_times / lambda_vector))
    sample_steps = make_sample_steps(n_steps, args.trace_points)
    thresholds = {
        "response_min_r": float(args.response_min_r),
        "null_separation_min": float(args.null_separation_min),
        "memory_gain_min": float(args.memory_gain_min),
        "flip_cosine_max": float(args.flip_cosine_max),
        "flip_magnitude_min": float(args.flip_magnitude_min),
        "flip_magnitude_max": float(args.flip_magnitude_max),
        "tangential_fraction_min": float(args.tangential_fraction_min),
        "target_radius_max_change": float(args.target_radius_max_change),
        "target_shape_max_change": float(args.target_shape_max_change),
        "source_radius_max_change": float(args.source_radius_max_change),
        "source_spectrum_max_drift": float(args.source_spectrum_max_drift),
    }
    rows = []
    for case in cases:
        print(f"running oriented gate seed={case['seed']}", flush=True)
        rows.append(run_case(case, args, sample_steps, thresholds))
    passing = sum(row["case_pass"] for row in rows)
    status = "pass" if passing >= args.minimum_passing_seeds else "fail"
    decision = {
        "status": status,
        "passing_seeds": passing,
        "seed_count": len(rows),
        "selected_next_step": (
            "localized_or_retarded_oriented_transport_validation"
            if status == "pass"
            else "stop_or_reformulate_oriented_state"
        ),
    }
    report_path = _resolve(args.report)
    summary_path = _resolve(args.summary_json)
    figure_path = _resolve(args.figure)
    payload = {
        "schema": "emergenz-knoten.oriented-vector-one-way-gate",
        "schema_version": 1,
        "generated_utc": datetime.now(UTC).isoformat(timespec="seconds"),
        "git_revision": git_revision,
        "git_status_at_start": git_status,
        "command": ["python", *os.sys.argv],
        "case_globs": patterns,
        "formation_updates": int(first_config.steps),
        "dim": int(first_config.dim),
        "memory_times": float(args.memory_times),
        "n_steps": n_steps,
        "sample_steps": sample_steps,
        "trace_memory_times": sample_steps * lambda_vector,
        "lambda_vector": lambda_vector,
        "orientation_relaxation": (
            lambda_vector
            if args.orientation_relaxation is None
            else float(args.orientation_relaxation)
        ),
        "vector_mass": float(args.vector_mass),
        "sigma_ratio": float(args.sigma_ratio),
        "separation_ratio": float(args.separation_ratio),
        "response_fraction": float(args.response_fraction),
        "randomizations": int(args.randomizations),
        "random_quantile": float(args.random_quantile),
        "minimum_passing_seeds": int(args.minimum_passing_seeds),
        "thresholds": thresholds,
        "rows": rows,
        "decision": decision,
        "summary_json": summary_path,
        "figure": figure_path,
    }
    make_figure(rows, payload, figure_path)
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
    print(f"wrote {_relative(report_path)}", flush=True)


if __name__ == "__main__":
    main()
