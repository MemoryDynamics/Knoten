"""Validate one fixed oriented-memory coupling across independent knot pairs."""

from __future__ import annotations

import argparse
from dataclasses import asdict
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

from emergenz_knoten import (
    FiniteMemoryState,
    SimulationConfig,
    initialize_oriented_memory_state,
    memory_centroid,
    memory_shape_tensor,
    one_way_oriented_response,
    oriented_response_metrics,
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
        description="Fixed-coupling distance gate for independent oriented states."
    )
    parser.add_argument("--case-glob", action="append", default=None)
    parser.add_argument("--seeds", default="1,2,3,4,5,6")
    parser.add_argument("--memory-times", type=float, default=20.0)
    parser.add_argument("--trace-points", type=int, default=100)
    parser.add_argument("--lambda-vector", type=float, default=None)
    parser.add_argument("--orientation-relaxation", type=float, default=None)
    parser.add_argument("--vector-mass", type=float, default=1.0)
    parser.add_argument("--vector-eta", type=float, default=5.079e-6)
    parser.add_argument("--sigma-ratio", type=float, default=2.5)
    parser.add_argument("--distance-ratios", default="2.5,5,10")
    parser.add_argument("--randomizations", type=int, default=64)
    parser.add_argument("--random-quantile", type=float, default=0.95)
    parser.add_argument("--response-min-r", type=float, default=1e-3)
    parser.add_argument("--null-separation-min", type=float, default=2.0)
    parser.add_argument("--memory-gain-min", type=float, default=1.25)
    parser.add_argument("--flip-cosine-max", type=float, default=-0.9)
    parser.add_argument("--flip-magnitude-min", type=float, default=0.5)
    parser.add_argument("--flip-magnitude-max", type=float, default=2.0)
    parser.add_argument("--target-radius-max-change", type=float, default=0.1)
    parser.add_argument("--target-shape-max-change", type=float, default=0.1)
    parser.add_argument("--source-radius-max-change", type=float, default=0.5)
    parser.add_argument("--source-spectrum-max-drift", type=float, default=0.25)
    parser.add_argument("--distance-monotonic-tolerance", type=float, default=0.1)
    parser.add_argument("--far-near-max-ratio", type=float, default=0.1)
    parser.add_argument("--minimum-passing-pairs", type=int, default=5)
    parser.add_argument("--noise-seed", type=int, default=20_260_726)
    parser.add_argument("--allow-dirty", action="store_true")
    parser.add_argument(
        "--report",
        type=Path,
        default=Path(
            "reports/response/oriented_vector_fixed_pair_distance_gate_2026-07-26.md"
        ),
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=Path(
            "reports/response/oriented_vector_fixed_pair_distance_gate_2026-07-26.json"
        ),
    )
    parser.add_argument(
        "--figure",
        type=Path,
        default=Path(
            "figures/draft/response/oriented_vector_fixed_pair_distance_gate_2026-07-26.png"
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


def parse_distance_ratios(text: str) -> list[float]:
    distances = [float(part.strip()) for part in text.split(",") if part.strip()]
    invalid = any(not np.isfinite(value) or value <= 0.0 for value in distances)
    unordered = any(right <= left for left, right in zip(distances, distances[1:]))
    if len(distances) < 3 or invalid or unordered:
        raise ValueError(
            "distance ratios must contain at least three increasing positives"
        )
    return distances


def cyclic_seed_pairs(seeds: list[int]) -> list[tuple[int, int]]:
    if len(seeds) < 2:
        raise ValueError("at least two seeds are required for independent pairs")
    return [(seed, seeds[(index + 1) % len(seeds)]) for index, seed in enumerate(seeds)]


def make_sample_steps(n_steps: int, trace_points: int) -> np.ndarray:
    if n_steps < 1 or trace_points < 3:
        raise ValueError("n_steps and trace_points must be positive")
    linear = np.rint(np.linspace(0, n_steps, trace_points + 1)).astype(int)
    logarithmic = np.rint(np.geomspace(1, n_steps, trace_points)).astype(int)
    return np.unique(np.concatenate(([0, n_steps], linear, logarithmic)))


def discover_cases(patterns: list[str], seeds: list[int]) -> list[Path]:
    paths: list[Path] = []
    for pattern in patterns:
        resolved = pattern if Path(pattern).is_absolute() else str(ROOT / pattern)
        paths.extend(Path(path) for path in glob.glob(resolved))
    selected: dict[int, Path] = {}
    for path in sorted(set(path.resolve() for path in paths)):
        seed = int(json.loads(path.read_text(encoding="utf-8"))["seed"])
        if seed in seeds:
            if seed in selected:
                raise ValueError(f"duplicate case for seed {seed}")
            selected[seed] = path
    missing = sorted(set(seeds) - set(selected))
    if missing:
        raise ValueError(f"missing cases for seeds {missing}")
    return [selected[seed] for seed in seeds]


def load_snapshot_case(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    payload = json.loads(raw.decode("utf-8"))
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
    return {
        "path": path,
        "case_sha256": hashlib.sha256(raw).hexdigest(),
        "seed": int(payload["seed"]),
        "config": config,
        "state": FiniteMemoryState(x=points[0], memory=points, weights=weights),
        "formation_revision": payload.get("git_revision", "unavailable"),
        "formation_updates": int(payload["config"]["steps"]),
        "formation_git_status": payload.get("git_status", "unavailable"),
    }


def classify_near_response(
    persistent: dict[str, Any],
    one_step: dict[str, Any],
    thresholds: dict[str, float],
) -> tuple[dict[str, bool], float]:
    tiny = np.finfo(float).tiny
    memory_gain = float(
        persistent["null_separation"] / max(one_step["null_separation"], tiny)
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
    return gates, memory_gain


def classify_distance_profile(
    distance_rows: list[dict[str, Any]],
    *,
    monotonic_tolerance: float,
    far_near_max_ratio: float,
) -> dict[str, Any]:
    if len(distance_rows) < 3:
        raise ValueError("distance profile requires at least three rows")
    responses = np.asarray(
        [row["persistent"]["active_response_r"] for row in distance_rows], dtype=float
    )
    fields = np.asarray(
        [row["initial_field_norm"] for row in distance_rows], dtype=float
    )
    tiny = np.finfo(float).tiny
    response_ratios = responses / max(float(responses[0]), tiny)
    field_ratios = fields / max(float(fields[0]), tiny)
    response_monotone = bool(
        np.all(responses[1:] <= responses[:-1] * (1.0 + monotonic_tolerance))
    )
    field_monotone = bool(
        np.all(fields[1:] <= fields[:-1] * (1.0 + monotonic_tolerance))
    )
    far_to_near = float(response_ratios[-1])
    return {
        "response_ratios_to_near": response_ratios,
        "initial_field_ratios_to_near": field_ratios,
        "response_monotone_pass": response_monotone,
        "initial_field_monotone": field_monotone,
        "far_to_near_response": far_to_near,
        "far_null_pass": bool(far_to_near <= far_near_max_ratio),
        "attenuation_pass": bool(
            response_monotone and far_to_near <= far_near_max_ratio
        ),
    }


def run_pair(
    target_case: dict[str, Any],
    source_case: dict[str, Any],
    args: argparse.Namespace,
    sample_steps: np.ndarray,
    distance_ratios: list[float],
    thresholds: dict[str, float],
) -> dict[str, Any]:
    target_state = target_case["state"]
    source_scalar_state = source_case["state"]
    config = target_case["config"]
    if source_case["config"] != config:
        raise ValueError("target and source configurations must match")
    lambda_vector = (
        float(config.alpha) if args.lambda_vector is None else float(args.lambda_vector)
    )
    orientation_relaxation = (
        lambda_vector
        if args.orientation_relaxation is None
        else float(args.orientation_relaxation)
    )
    target_radius = float(np.sqrt(np.trace(memory_shape_tensor(target_state))))
    source_radius = float(np.sqrt(np.trace(memory_shape_tensor(source_scalar_state))))
    if min(target_radius, source_radius) <= 0.0:
        raise ValueError("target and source memory radii must be positive")
    pair_radius = 0.5 * (target_radius + source_radius)
    vector_sigma = float(args.sigma_ratio * source_radius)
    persistent_state = initialize_oriented_memory_state(
        source_scalar_state,
        lambda_vector=lambda_vector,
        vector_mass=args.vector_mass,
        orientation_relaxation=orientation_relaxation,
    )
    one_step_state = initialize_oriented_memory_state(
        source_scalar_state,
        lambda_vector=1.0,
        vector_mass=args.vector_mass,
        orientation_relaxation=1.0,
    )
    n_steps = int(sample_steps[-1])
    pair_seed = (
        args.noise_seed + 10_007 * target_case["seed"] + 100_003 * source_case["seed"]
    )
    rng = np.random.default_rng(pair_seed)
    target_noise = rng.normal(size=(n_steps, config.dim))
    source_noise = rng.normal(size=(n_steps, config.dim))
    random_seed = pair_seed + 1_000_003
    distance_rows: list[dict[str, Any]] = []
    for distance_ratio in distance_ratios:
        offset = np.zeros(config.dim, dtype=float)
        offset[0] = float(distance_ratio * pair_radius)
        placed = place_oriented_memory_state(
            persistent_state, memory_centroid(target_state) + offset
        )
        initial_field = vector_gaussian_field(
            memory_centroid(target_state),
            placed.scalar_state.memory,
            placed.orientations,
            placed.weights,
            sigma=vector_sigma,
        )
        common = {
            "source_center_offset": offset,
            "target_noise": target_noise,
            "source_noise": source_noise,
            "sample_steps": sample_steps,
            "vector_eta": args.vector_eta,
            "vector_sigma": vector_sigma,
            "randomization_count": args.randomizations,
            "random_seed": random_seed,
        }
        persistent_response = one_way_oriented_response(
            target_state, persistent_state, config, **common
        )
        one_step_response = one_way_oriented_response(
            target_state, one_step_state, config, **common
        )
        radial_direction = -offset / np.linalg.norm(offset)
        persistent_metrics = oriented_response_metrics(
            persistent_response,
            radius=target_radius,
            radial_direction=radial_direction,
            random_quantile=args.random_quantile,
        )
        one_step_metrics = oriented_response_metrics(
            one_step_response,
            radius=target_radius,
            radial_direction=radial_direction,
            random_quantile=args.random_quantile,
        )
        distance_rows.append(
            {
                "distance_ratio_pair_radius": float(distance_ratio),
                "distance_over_source_radius": float(
                    distance_ratio * pair_radius / source_radius
                ),
                "initial_field_norm": float(np.linalg.norm(initial_field)),
                "persistent": persistent_metrics,
                "one_step": one_step_metrics,
            }
        )
    near_gates, memory_gain = classify_near_response(
        distance_rows[0]["persistent"], distance_rows[0]["one_step"], thresholds
    )
    profile = classify_distance_profile(
        distance_rows,
        monotonic_tolerance=args.distance_monotonic_tolerance,
        far_near_max_ratio=args.far_near_max_ratio,
    )
    gates = {**near_gates, "distance_attenuation": profile["attenuation_pass"]}
    return {
        "target_seed": int(target_case["seed"]),
        "source_seed": int(source_case["seed"]),
        "target_case_path": _relative(target_case["path"]),
        "source_case_path": _relative(source_case["path"]),
        "target_case_sha256": target_case["case_sha256"],
        "source_case_sha256": source_case["case_sha256"],
        "target_radius": target_radius,
        "source_radius": source_radius,
        "pair_radius": pair_radius,
        "vector_sigma": vector_sigma,
        "vector_sigma_over_source_radius": float(args.sigma_ratio),
        "vector_eta": float(args.vector_eta),
        "lambda_vector": lambda_vector,
        "orientation_relaxation": orientation_relaxation,
        "distance_rows": distance_rows,
        "near_memory_gain": memory_gain,
        "profile": profile,
        "gates": gates,
        "pair_pass": bool(all(gates.values())),
    }


def _fmt(value: float) -> str:
    if value == 0.0:
        return "0"
    if abs(value) < 1e-3 or abs(value) >= 1e3:
        return f"{value:.3e}"
    return f"{value:.4f}"


def make_figure(
    rows: list[dict[str, Any]], payload: dict[str, Any], path: Path
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    colors = plt.cm.viridis(np.linspace(0.08, 0.92, len(rows)))
    fig, axes = plt.subplots(2, 2, figsize=(10.8, 7.4), constrained_layout=True)
    tiny = np.finfo(float).tiny
    for row, color in zip(rows, colors, strict=True):
        items = row["distance_rows"]
        distances = np.asarray([item["distance_ratio_pair_radius"] for item in items])
        responses = np.asarray(
            [item["persistent"]["active_response_r"] for item in items]
        )
        random_q95 = np.asarray(
            [item["persistent"]["random_threshold_r"] for item in items]
        )
        label = f"T{row['target_seed']}<-S{row['source_seed']}"
        axes[0, 0].plot(
            distances, np.maximum(responses, tiny), "o-", color=color, label=label
        )
        axes[0, 0].plot(
            distances, np.maximum(random_q95, tiny), ":", color=color, alpha=0.65
        )
        axes[0, 1].plot(
            distances,
            np.maximum(row["profile"]["response_ratios_to_near"], tiny),
            "o-",
            color=color,
            label=label,
        )
        axes[0, 1].plot(
            distances,
            np.maximum(row["profile"]["initial_field_ratios_to_near"], tiny),
            ":",
            color=color,
            alpha=0.65,
        )
    axes[0, 0].set_yscale("log")
    axes[0, 0].set_xlabel("distance / R_pair")
    axes[0, 0].set_ylabel("response / R_target")
    axes[0, 0].set_title("Active (solid) vs random-sign q95 (dotted)")
    axes[0, 0].legend(fontsize=7, ncol=2)
    axes[0, 1].set_yscale("log")
    axes[0, 1].axhline(
        payload["thresholds"]["far_near_max_ratio"],
        color="#555555",
        linestyle="--",
        label="far/near limit",
    )
    axes[0, 1].set_xlabel("distance / R_pair")
    axes[0, 1].set_ylabel("ratio to near")
    axes[0, 1].set_title("Observed response vs initial-field profile")

    labels = [f"{row['target_seed']}<-{row['source_seed']}" for row in rows]
    indices = np.arange(len(rows))
    near_sep = np.asarray(
        [row["distance_rows"][0]["persistent"]["null_separation"] for row in rows]
    )
    one_step_sep = np.asarray(
        [row["distance_rows"][0]["one_step"]["null_separation"] for row in rows]
    )
    axes[1, 0].plot(indices, near_sep, "o-", label="persistent")
    axes[1, 0].plot(indices, one_step_sep, "s--", label="one-step")
    axes[1, 0].axhline(
        payload["thresholds"]["null_separation_min"], color="#555555", linestyle=":"
    )
    axes[1, 0].set_xticks(indices, labels, rotation=35, ha="right")
    axes[1, 0].set_ylabel("active / random-sign q95")
    axes[1, 0].set_title("Near-field conditional separation")
    axes[1, 0].legend(fontsize=8)

    target_shape = np.asarray(
        [
            row["distance_rows"][0]["persistent"]["target_shape_max_change"]
            for row in rows
        ]
    )
    source_shape = np.asarray(
        [
            row["distance_rows"][0]["persistent"]["source_spectrum_max_drift"]
            for row in rows
        ]
    )
    far_ratio = np.asarray([row["profile"]["far_to_near_response"] for row in rows])
    axes[1, 1].plot(indices, np.maximum(target_shape, tiny), "o-", label="target shape")
    axes[1, 1].plot(
        indices, np.maximum(source_shape, tiny), "s--", label="source spectrum"
    )
    axes[1, 1].plot(
        indices, np.maximum(far_ratio, tiny), "^:", label="far/near response"
    )
    axes[1, 1].set_yscale("log")
    axes[1, 1].set_xticks(indices, labels, rotation=35, ha="right")
    axes[1, 1].set_ylabel("dimensionless")
    axes[1, 1].set_title("Shape and attenuation gates")
    axes[1, 1].legend(fontsize=8)
    for axis in axes.flat:
        axis.grid(alpha=0.25)
    fig.suptitle("Fixed oriented coupling across independent scalar knots")
    fig.savefig(path, dpi=180)
    plt.close(fig)


def build_report(payload: dict[str, Any], report_path: Path, figure_path: Path) -> str:
    decision = payload["decision"]
    lines = [
        "# Fixed-coupling independent-pair distance gate",
        "",
        f"Date: {payload['generated_utc']}",
        "",
        "## Question",
        "",
        "Does the introduced oriented-memory readout generalize from cloned",
        "source/target states to cyclically paired independent scalar formations",
        "under one globally fixed coupling, and does its response attenuate over",
        "a preregistered distance ladder?",
        "",
        "This tests one fixed phenomenological channel. The vector state,",
        "instantaneous Gaussian readout, passive source, and width rule",
        "`sigma_v=2.5 R_source` remain model inputs. This is a fixed",
        "dimensionless rule, not yet one universal absolute length scale.",
        "",
        "## Preregistered design",
        "",
        f"- cyclic independent pairs: `{payload['pairs']}`;",
        f"- global `eta_v={payload['vector_eta']:.6g}` without pairwise calibration;",
        f"- distances `{payload['distance_ratios']}` in `R_pair=(R_source+R_target)/2`;",
        f"- {payload['randomizations']} random-sign controls plus channel-off, global flip, and one-step memory;",
        "- common target/source future noise and identical random signs across",
        "  distances and memory arms within each pair;",
        "- tangential fraction is reported but is not a gate because the pair",
        "  axis is arbitrary relative to independently formed source orientation.",
        "",
        "Near pass requires response, random-sign separation, persistent-memory",
        "gain, sign reversal, and source/target shape bounds. Distance pass requires",
        f"non-increasing response within {payload['thresholds']['distance_monotonic_tolerance']:.0%} tolerance and far/near <= {payload['thresholds']['far_near_max_ratio']:.3g}.",
        f"Overall pass requires at least {payload['minimum_passing_pairs']} of {len(payload['rows'])} pairs.",
        "",
        "## Decision",
        "",
        f"Gate status: **{decision['status']}** ({decision['passing_pairs']}/{decision['pair_count']} pairs).",
        "",
        f"Selected next step: **{decision['selected_next_step']}**.",
        "",
        "## Pair results",
        "",
        "| target<-source | near active/R | near active/q95 | one-step/q95 | memory gain | flip cos | tangent | far/near | monotone | shape bounded | pass |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- | --- |",
    ]
    for row in payload["rows"]:
        near = row["distance_rows"][0]
        persistent = near["persistent"]
        one_step = near["one_step"]
        shape_pass = (
            row["gates"]["target_shape_bounded"]
            and row["gates"]["source_shape_bounded"]
        )
        lines.append(
            f"| {row['target_seed']}<-{row['source_seed']} | "
            f"{_fmt(persistent['active_response_r'])} | "
            f"{_fmt(persistent['null_separation'])} | "
            f"{_fmt(one_step['null_separation'])} | "
            f"{_fmt(row['near_memory_gain'])} | "
            f"{_fmt(persistent['flip_cosine'])} | "
            f"{_fmt(persistent['tangential_fraction'])} | "
            f"{_fmt(row['profile']['far_to_near_response'])} | "
            f"{'yes' if row['profile']['response_monotone_pass'] else 'no'} | "
            f"{'yes' if shape_pass else 'no'} | "
            f"{'pass' if row['pair_pass'] else 'fail'} |"
        )
    lines.extend(
        [
            "",
            "## Distance-resolved results",
            "",
            "| target<-source | distance/R_pair | distance/R_source | initial field | active/R | random q95/R | active/q95 | target shape | source spectrum |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in payload["rows"]:
        for item in row["distance_rows"]:
            metrics = item["persistent"]
            lines.append(
                f"| {row['target_seed']}<-{row['source_seed']} | "
                f"{_fmt(item['distance_ratio_pair_radius'])} | "
                f"{_fmt(item['distance_over_source_radius'])} | "
                f"{_fmt(item['initial_field_norm'])} | "
                f"{_fmt(metrics['active_response_r'])} | "
                f"{_fmt(metrics['random_threshold_r'])} | "
                f"{_fmt(metrics['null_separation'])} | "
                f"{_fmt(metrics['target_shape_max_change'])} | "
                f"{_fmt(metrics['source_spectrum_max_drift'])} |"
            )
    lines.extend(["", "## Interpretation boundary", ""])
    if decision["status"] == "pass":
        lines.extend(
            [
                "The pass supports only cross-state reproducibility and spatial",
                "attenuation of the deliberately introduced instantaneous oriented",
                "Gaussian readout under its fixed coupling and width rule. It does",
                "not establish a universal potential, reciprocity, retardation, a",
                "conservation law, QFT, spin, charge, photons, or particles.",
                "A local/retarded mediator is the next discriminating mechanism test.",
            ]
        )
    else:
        lines.extend(
            [
                "The fixed channel does not satisfy its cross-state/distance gate.",
                "Pairwise retuning is prohibited. The failure must be localized to",
                "near response, null separation, memory gain, shape, or attenuation",
                "before any local/retarded mediator or reciprocal coupling is opened.",
            ]
        )
    lines.extend(
        [
            "",
            "## Figure",
            "",
            f"![Fixed-pair distance gate]({_relative_from(report_path, figure_path)})",
            "",
            "## Reproducibility",
            "",
            f"- Formation config: `{json.dumps(payload['formation_config'], sort_keys=True)}`",
        ]
    )
    for row in payload["rows"]:
        lines.append(
            f"- Pair {row['target_seed']}<-{row['source_seed']}: target "
            f"`{row['target_case_path']}` SHA-256 `{row['target_case_sha256']}`; "
            f"source `{row['source_case_path']}` SHA-256 `{row['source_case_sha256']}`"
        )
    lines.extend(
        [
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
        distance_ratios = parse_distance_ratios(args.distance_ratios)
        pairs = cyclic_seed_pairs(seeds)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    if args.memory_times <= 0.0 or args.trace_points < 3:
        raise SystemExit("memory-times and trace-points must be positive")
    if args.vector_mass <= 0.0 or args.vector_eta <= 0.0 or args.sigma_ratio <= 0.0:
        raise SystemExit("vector mass, eta, and sigma ratio must be positive")
    if args.randomizations < 16 or not 0.5 < args.random_quantile < 1.0:
        raise SystemExit("randomizations must be >=16 and quantile in (0.5, 1)")
    if (
        args.orientation_relaxation is not None
        and not 0.0 < args.orientation_relaxation <= 1.0
    ):
        raise SystemExit("orientation-relaxation must lie in (0, 1]")
    if (
        args.distance_monotonic_tolerance < 0.0
        or not 0.0 < args.far_near_max_ratio < 1.0
    ):
        raise SystemExit("invalid distance attenuation thresholds")
    if not 1 <= args.minimum_passing_pairs <= len(pairs):
        raise SystemExit("minimum-passing-pairs must fit the pair count")

    git_revision = _git_output(["rev-parse", "HEAD"])
    git_status = _git_output(["status", "--short"])
    if git_status and not args.allow_dirty:
        raise SystemExit("fixed-pair gate requires a clean worktree")
    patterns = list(DEFAULT_CASE_GLOBS if args.case_glob is None else args.case_glob)
    try:
        paths = discover_cases(patterns, seeds)
        cases = [load_snapshot_case(path) for path in paths]
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        raise SystemExit(str(exc)) from exc
    cases_by_seed = {case["seed"]: case for case in cases}
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
        "target_radius_max_change": float(args.target_radius_max_change),
        "target_shape_max_change": float(args.target_shape_max_change),
        "source_radius_max_change": float(args.source_radius_max_change),
        "source_spectrum_max_drift": float(args.source_spectrum_max_drift),
        "distance_monotonic_tolerance": float(args.distance_monotonic_tolerance),
        "far_near_max_ratio": float(args.far_near_max_ratio),
    }
    rows: list[dict[str, Any]] = []
    for target_seed, source_seed in pairs:
        print(
            f"running fixed pair target={target_seed} source={source_seed}", flush=True
        )
        rows.append(
            run_pair(
                cases_by_seed[target_seed],
                cases_by_seed[source_seed],
                args,
                sample_steps,
                distance_ratios,
                thresholds,
            )
        )
    passing = sum(row["pair_pass"] for row in rows)
    status = "pass" if passing >= args.minimum_passing_pairs else "fail"
    decision = {
        "status": status,
        "passing_pairs": passing,
        "pair_count": len(rows),
        "selected_next_step": (
            "local_or_retarded_oriented_mediator_gate"
            if status == "pass"
            else "localize_fixed_channel_failure_without_retuning"
        ),
    }
    report_path = _resolve(args.report)
    summary_path = _resolve(args.summary_json)
    figure_path = _resolve(args.figure)
    payload = {
        "schema": "emergenz-knoten.oriented-vector-fixed-pair-distance-gate",
        "schema_version": 1,
        "generated_utc": datetime.now(UTC).isoformat(timespec="seconds"),
        "git_revision": git_revision,
        "git_status_at_start": git_status,
        "command": ["python", *os.sys.argv],
        "case_globs": patterns,
        "pairs": [f"{target}<-{source}" for target, source in pairs],
        "formation_updates": int(first_config.steps),
        "formation_config": asdict(first_config),
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
        "vector_eta": float(args.vector_eta),
        "sigma_ratio": float(args.sigma_ratio),
        "distance_ratios": distance_ratios,
        "randomizations": int(args.randomizations),
        "random_quantile": float(args.random_quantile),
        "minimum_passing_pairs": int(args.minimum_passing_pairs),
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
        build_report(payload, report_path, figure_path), encoding="utf-8"
    )
    print(f"wrote {_relative(report_path)}", flush=True)


if __name__ == "__main__":
    main()
