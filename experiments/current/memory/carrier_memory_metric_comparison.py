"""Compare covariance, predictive and RKHS metrics on one carrier feature space."""

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

from emergenz_knoten import (
    FiniteMemoryState,
    OrientedMemoryState,
    SimulationConfig,
    advance_oriented_memory_state,
    initialize_oriented_memory_state,
    memory_shape_tensor,
    normalized_direction_jacobian,
    one_way_oriented_response,
)
from emergenz_knoten.memory_metrics import (
    covariance_precision_metric,
    gaussian_rkhs_emission_norms,
    isotropic_rkhs_observability_metric,
    metric_pullback,
    observability_gramian,
    supported_subspace_overlap,
    trace_normalized_distance,
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
METRIC_NAMES = ("covariance", "predictive", "kernel")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Three-metric comparison on the persistent carrier feature."
    )
    parser.add_argument("--case-glob", action="append", default=None)
    parser.add_argument("--seeds", default="1,2,3,4,5,6")
    parser.add_argument("--lambda-vector", type=float, default=0.01)
    parser.add_argument("--orientation-relaxation", type=float, default=0.01)
    parser.add_argument("--vector-mass", type=float, default=1.0)
    parser.add_argument("--vector-eta", type=float, default=5.079e-6)
    parser.add_argument("--distance-ratio", type=float, default=2.5)
    parser.add_argument("--sigma-ratio", type=float, default=2.5)
    parser.add_argument("--horizons-memory-times", default="1,2,5,10")
    parser.add_argument("--cadences", default="1,5,10")
    parser.add_argument("--segments", type=int, default=2)
    parser.add_argument("--finite-difference", type=float, default=1e-4)
    parser.add_argument("--covariance-cutoff", type=float, default=1e-6)
    parser.add_argument("--noise-seed", type=int, default=20_260_808)
    parser.add_argument("--max-linearity-error", type=float, default=0.05)
    parser.add_argument("--max-cadence-scale-drift", type=float, default=0.20)
    parser.add_argument("--max-cadence-shape-drift", type=float, default=0.10)
    parser.add_argument("--max-segment-shape-drift", type=float, default=0.25)
    parser.add_argument("--max-horizon-scale-drift", type=float, default=0.25)
    parser.add_argument("--min-subspace-overlap", type=float, default=0.90)
    parser.add_argument("--required-pairs", type=int, default=5)
    parser.add_argument("--allow-dirty", action="store_true")
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("reports/memory/carrier_memory_metric_comparison_2026-08-08.md"),
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=Path("reports/memory/carrier_memory_metric_comparison_2026-08-08.json"),
    )
    parser.add_argument(
        "--figure",
        type=Path,
        default=Path(
            "figures/draft/memory/carrier_memory_metric_comparison_2026-08-08.png"
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


def _parse_floats(text: str) -> list[float]:
    values = [float(item.strip()) for item in text.split(",") if item.strip()]
    if not values or not np.isfinite(values).all():
        raise ValueError("expected finite comma-separated values")
    return values


def _parse_ints(text: str) -> list[int]:
    values = [int(item.strip()) for item in text.split(",") if item.strip()]
    if not values or any(value < 1 for value in values):
        raise ValueError("expected positive comma-separated integers")
    return values


def _discover_cases(patterns: list[str], seeds: list[int]) -> dict[int, dict[str, Any]]:
    paths = {
        Path(path).resolve()
        for pattern in patterns
        for path in glob.glob(str(_resolve(Path(pattern))))
    }
    cases = {}
    for path in sorted(paths):
        case = load_snapshot_case(path)
        if case["seed"] in seeds:
            if case["seed"] in cases:
                raise ValueError(f"duplicate case for seed {case['seed']}")
            cases[case["seed"]] = case
    missing = sorted(set(seeds) - set(cases))
    if missing:
        raise FileNotFoundError(f"missing cases for seeds {missing}")
    return cases


def load_snapshot_case(path: Path) -> dict[str, Any]:
    """Load one complete baseline finite-memory snapshot."""

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
    }

def perturb_carrier(state: OrientedMemoryState, perturbation: np.ndarray) -> OrientedMemoryState:
    """Change only the reduced carrier feature, leaving deposited history fixed."""

    delta = np.asarray(perturbation, dtype=float)
    if delta.shape != (state.dim,) or not np.isfinite(delta).all():
        raise ValueError("perturbation must match carrier dimension")
    return OrientedMemoryState(
        scalar_state=state.scalar_state,
        orientations=state.orientations,
        weights=state.weights,
        carrier_orientation=state.carrier_orientation + delta,
        orientation_relaxation=state.orientation_relaxation,
    )


def _advance_states(
    source: OrientedMemoryState,
    target: OrientedMemoryState,
    config: Any,
    source_noise: np.ndarray,
    target_noise: np.ndarray,
) -> tuple[OrientedMemoryState, OrientedMemoryState]:
    for source_increment, target_increment in zip(source_noise, target_noise):
        source = advance_oriented_memory_state(
            source, config, noise_increment=source_increment
        )
        target = advance_oriented_memory_state(
            target, config, noise_increment=target_increment
        )
    return source, target


def response_tangent(
    target_state: Any,
    source_state: OrientedMemoryState,
    config: Any,
    *,
    offset: np.ndarray,
    target_noise: np.ndarray,
    source_noise: np.ndarray,
    vector_eta: float,
    vector_sigma: float,
    finite_difference: float,
    random_seed: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Central finite-difference response to each initial carrier component."""

    n_steps = target_noise.shape[0]
    sample_steps = np.arange(n_steps + 1, dtype=int)
    dim = source_state.dim
    jacobian = np.empty((n_steps + 1, dim, dim), dtype=float)
    source_positions = None
    carrier_trace = None
    for axis in range(dim):
        delta = np.zeros(dim, dtype=float)
        delta[axis] = finite_difference
        common = {
            "source_center_offset": offset,
            "target_noise": target_noise,
            "source_noise": source_noise,
            "sample_steps": sample_steps,
            "vector_eta": vector_eta,
            "vector_sigma": vector_sigma,
            "randomization_count": 1,
            "random_seed": random_seed,
        }
        plus = one_way_oriented_response(
            target_state, perturb_carrier(source_state, delta), config, **common
        )
        minus = one_way_oriented_response(
            target_state, perturb_carrier(source_state, -delta), config, **common
        )
        jacobian[:, :, axis] = (
            plus.target_positions[:, 0] - minus.target_positions[:, 0]
        ) / (2.0 * finite_difference)
        if axis == 0:
            source_positions = 0.5 * (plus.source_positions + minus.source_positions)
            carrier_trace = 0.5 * (
                plus.source_carrier_orientations + minus.source_carrier_orientations
            )
    assert source_positions is not None and carrier_trace is not None
    return jacobian, source_positions, carrier_trace


def _classification(value: float, q: float) -> str:
    lower = (1.0 - np.sqrt(q)) ** 2
    upper = (1.0 + np.sqrt(q)) ** 2
    stable_upper = 2.0 * (1.0 + q)
    tolerance = 1e-12 * max(1.0, value, stable_upper)
    if value <= tolerance:
        return "null"
    if value < lower:
        return "overdamped"
    if value < upper:
        return "complex"
    if value < stable_upper:
        return "alternating"
    return "unstable"


def summarize_metric(metric: np.ndarray, forward: np.ndarray, *, gain: float, q: float) -> dict[str, Any]:
    values = np.maximum(np.linalg.eigvalsh(0.5 * (metric + metric.T)), 0.0)
    pullback = metric_pullback(forward, metric)
    pullback_values = np.maximum(np.linalg.eigvalsh(pullback), 0.0)
    couplings = gain * pullback_values
    return {
        "metric": metric,
        "metric_eigenvalues": values,
        "metric_trace": float(np.trace(metric)),
        "pullback": pullback,
        "pullback_eigenvalues": pullback_values,
        "dimensionless_couplings": couplings,
        "classifications": [_classification(float(value), q) for value in couplings],
        "complex_count": int(sum(_classification(float(value), q) == "complex" for value in couplings)),
    }


def _indices(horizon: int, cadence: int) -> np.ndarray:
    values = np.arange(0, horizon + 1, cadence, dtype=int)
    if values[-1] != horizon:
        values = np.append(values, horizon)
    return values


def run_segment(
    target_case: dict[str, Any],
    source_case: dict[str, Any],
    target_state: OrientedMemoryState,
    source_state: OrientedMemoryState,
    *,
    segment: int,
    reference_geometry: dict[str, float],
    horizons: list[int],
    cadences: list[int],
    args: argparse.Namespace,
) -> dict[str, Any]:
    config = target_case["config"]
    source_radius = float(np.sqrt(np.trace(memory_shape_tensor(source_state.scalar_state))))
    target_radius = float(np.sqrt(np.trace(memory_shape_tensor(target_state.scalar_state))))
    offset = np.zeros(config.dim)
    offset[0] = reference_geometry["offset_magnitude"]
    vector_sigma = reference_geometry["vector_sigma"]
    n_steps = max(horizons)
    pair_seed = (
        args.noise_seed
        + 10_007 * target_case["seed"]
        + 100_003 * source_case["seed"]
        + 1_000_003 * segment
    )
    rng = np.random.default_rng(pair_seed)
    target_noise = rng.normal(size=(n_steps, config.dim))
    source_noise = rng.normal(size=(n_steps, config.dim))
    full, source_positions, carriers = response_tangent(
        target_state.scalar_state,
        source_state,
        config,
        offset=offset,
        target_noise=target_noise,
        source_noise=source_noise,
        vector_eta=args.vector_eta,
        vector_sigma=vector_sigma,
        finite_difference=args.finite_difference,
        random_seed=pair_seed + 17,
    )
    half, _, _ = response_tangent(
        target_state.scalar_state,
        source_state,
        config,
        offset=offset,
        target_noise=target_noise,
        source_noise=source_noise,
        vector_eta=args.vector_eta,
        vector_sigma=vector_sigma,
        finite_difference=0.5 * args.finite_difference,
        random_seed=pair_seed + 17,
    )
    denominator = max(float(np.linalg.norm(half)), np.finfo(float).tiny)
    linearity_error = float(np.linalg.norm(full - half) / denominator)
    emission_norms = gaussian_rkhs_emission_norms(
        source_positions,
        deposition_weight=args.lambda_vector * args.vector_mass,
        carrier_decay=1.0 - args.orientation_relaxation,
        memory_decay=1.0 - args.lambda_vector,
        kernel_sigma=vector_sigma,
    )
    step = source_state.scalar_state.memory[0] - source_state.scalar_state.memory[1]
    forward = normalized_direction_jacobian(
        step, relaxation=args.orientation_relaxation
    )
    q = 1.0 - args.lambda_vector
    rows = []
    for horizon in horizons:
        for cadence in cadences:
            selected = _indices(horizon, cadence)
            covariance = covariance_precision_metric(
                carriers[selected], relative_cutoff=args.covariance_cutoff
            )
            predictive = observability_gramian(
                full[selected],
                selected,
                forgetting_factor=q,
                output_scale=reference_geometry["target_radius"],
            )
            kernel = isotropic_rkhs_observability_metric(
                emission_norms[selected],
                selected,
                forgetting_factor=q,
                feature_dimension=config.dim,
            )
            metrics = {
                "covariance": covariance.metric,
                "predictive": predictive,
                "kernel": kernel,
            }
            summaries = {
                name: summarize_metric(metric, forward, gain=args.vector_eta, q=q)
                for name, metric in metrics.items()
            }
            comparisons = {}
            for left, right in (
                ("covariance", "predictive"),
                ("covariance", "kernel"),
                ("predictive", "kernel"),
            ):
                comparisons[f"{left}_vs_{right}"] = {
                    "shape_distance": trace_normalized_distance(
                        summaries[left]["pullback"], summaries[right]["pullback"]
                    ),
                    "subspace_overlap": supported_subspace_overlap(
                        summaries[left]["pullback"], summaries[right]["pullback"]
                    ),
                }
            rows.append(
                {
                    "horizon_updates": horizon,
                    "horizon_memory_times": args.lambda_vector * horizon,
                    "cadence": cadence,
                    "covariance_rank": covariance.rank,
                    "metrics": summaries,
                    "comparisons": comparisons,
                }
            )
    return {
        "segment": segment,
        "target_radius": target_radius,
        "source_radius": source_radius,
        "vector_sigma": vector_sigma,
        "linearity_error": linearity_error,
        "rows": rows,
        "advance_noise": {"source": source_noise, "target": target_noise},
    }


def _jsonable(value: Any) -> Any:
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        return float(value)
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    return value


def _find_row(segment: dict[str, Any], horizon: int, cadence: int) -> dict[str, Any]:
    return next(
        row
        for row in segment["rows"]
        if row["horizon_updates"] == horizon and row["cadence"] == cadence
    )


def evaluate_gates(
    pairs: list[dict[str, Any]],
    *,
    horizons: list[int],
    cadences: list[int],
    args: argparse.Namespace,
) -> dict[str, Any]:
    final_horizon = max(horizons)
    previous_horizon = sorted(horizons)[-2]
    base_cadence = min(cadences)
    pair_gates = []
    for pair in pairs:
        segments = pair["segments"]
        linearity = max(segment["linearity_error"] for segment in segments)
        cadence_scale = 0.0
        cadence_shape = 0.0
        horizon_scale = 0.0
        cross_shape = 0.0
        cross_overlap = 1.0
        signatures = []
        for segment in segments:
            base = _find_row(segment, final_horizon, base_cadence)
            signatures.append(
                tuple(
                    tuple(base["metrics"][name]["classifications"])
                    for name in METRIC_NAMES
                )
            )
            previous = _find_row(segment, previous_horizon, base_cadence)
            for name in METRIC_NAMES:
                trace = base["metrics"][name]["metric_trace"]
                old_trace = previous["metrics"][name]["metric_trace"]
                horizon_scale = max(
                    horizon_scale,
                    abs(trace - old_trace) / max(abs(trace), np.finfo(float).tiny),
                )
            for cadence in cadences[1:]:
                coarse = _find_row(segment, final_horizon, cadence)
                trace = base["metrics"]["predictive"]["metric_trace"]
                coarse_trace = coarse["metrics"]["predictive"]["metric_trace"]
                cadence_scale = max(
                    cadence_scale,
                    abs(trace - coarse_trace) / max(abs(trace), np.finfo(float).tiny),
                )
                cadence_shape = max(
                    cadence_shape,
                    trace_normalized_distance(
                        np.asarray(base["metrics"]["predictive"]["pullback"]),
                        np.asarray(coarse["metrics"]["predictive"]["pullback"]),
                    ),
                )
            for comparison in base["comparisons"].values():
                cross_shape = max(cross_shape, comparison["shape_distance"])
                cross_overlap = min(cross_overlap, comparison["subspace_overlap"])
        segment_shape = 0.0
        if len(segments) > 1:
            for name in METRIC_NAMES:
                first = _find_row(segments[0], final_horizon, base_cadence)
                second = _find_row(segments[1], final_horizon, base_cadence)
                segment_shape = max(
                    segment_shape,
                    trace_normalized_distance(
                        np.asarray(first["metrics"][name]["pullback"]),
                        np.asarray(second["metrics"][name]["pullback"]),
                    ),
                )
        classification_agreement = len(set(signatures)) == 1
        metric_signature = signatures[0]
        cross_metric_agreement = len(set(metric_signature)) == 1
        gates = {
            "linearity": linearity <= args.max_linearity_error,
            "cadence_scale": cadence_scale <= args.max_cadence_scale_drift,
            "cadence_shape": cadence_shape <= args.max_cadence_shape_drift,
            "segment_shape": segment_shape <= args.max_segment_shape_drift,
            "horizon_scale": horizon_scale <= args.max_horizon_scale_drift,
            "subspace": cross_overlap >= args.min_subspace_overlap,
            "segment_classification": classification_agreement,
            "cross_metric_classification": cross_metric_agreement,
        }
        pair_gates.append(
            {
                "target_seed": pair["target_seed"],
                "source_seed": pair["source_seed"],
                "linearity_error": linearity,
                "cadence_scale_drift": cadence_scale,
                "cadence_shape_drift": cadence_shape,
                "segment_shape_drift": segment_shape,
                "horizon_scale_drift": horizon_scale,
                "cross_metric_shape_distance": cross_shape,
                "minimum_subspace_overlap": cross_overlap,
                "classification_signature": metric_signature,
                "gates": gates,
                "pass": all(gates.values()),
            }
        )
    pass_count = sum(row["pass"] for row in pair_gates)
    return {
        "pairs": pair_gates,
        "pass_count": pass_count,
        "required_pairs": args.required_pairs,
        "pass": pass_count >= args.required_pairs,
        "status": (
            "metric reconciliation pass; nonlinear validation still required"
            if pass_count >= args.required_pairs
            else "metric reconciliation fail"
        ),
    }


def _plot(payload: dict[str, Any], destination: Path) -> None:
    final_horizon = max(payload["horizon_updates"])
    cadence = min(payload["cadences"])
    q = 1.0 - payload["parameters"]["lambda_vector"]
    lower = (1.0 - np.sqrt(q)) ** 2
    upper = (1.0 + np.sqrt(q)) ** 2
    colors = {"covariance": "#176b87", "predictive": "#a23b3b", "kernel": "#5a7d4f"}
    figure, axes = plt.subplots(2, 2, figsize=(11.0, 8.0))
    for metric in METRIC_NAMES:
        for pair_index, pair in enumerate(payload["pairs"]):
            for segment in pair["segments"]:
                row = _find_row(segment, final_horizon, cadence)
                values = np.asarray(row["metrics"][metric]["dimensionless_couplings"])
                axes[0, 0].scatter(
                    np.full(values.size, pair_index + 1) + 0.04 * segment["segment"],
                    np.maximum(values, np.finfo(float).tiny),
                    color=colors[metric],
                    alpha=0.55,
                    s=18,
                )
        traces = []
        for horizon in payload["horizon_updates"]:
            values = []
            for pair in payload["pairs"]:
                for segment in pair["segments"]:
                    row = _find_row(segment, horizon, cadence)
                    values.append(row["metrics"][metric]["metric_trace"])
            traces.append(float(np.median(values)))
        axes[0, 1].plot(
            payload["horizons_memory_times"], traces, "o-", color=colors[metric], label=metric
        )
    axes[0, 0].axhspan(lower, upper, color="#5a9367", alpha=0.15)
    axes[0, 0].set_yscale("log")
    axes[0, 0].set_xlabel("cyclic source-target pair")
    axes[0, 0].set_ylabel(r"$g\,\lambda(B^T G_h B)$")
    axes[0, 0].set_title("Reciprocal classification by metric")
    axes[0, 1].set_yscale("log")
    axes[0, 1].set_xlabel("horizon / memory time")
    axes[0, 1].set_ylabel("median metric trace")
    axes[0, 1].set_title("Horizon dependence")
    axes[0, 1].legend(frameon=False)
    gate_rows = payload["decision"]["pairs"]
    names = ["linearity_error", "cadence_scale_drift", "segment_shape_drift", "horizon_scale_drift"]
    values = np.asarray([[row[name] for name in names] for row in gate_rows])
    image = axes[1, 0].imshow(values, aspect="auto", cmap="viridis")
    axes[1, 0].set_xticks(np.arange(len(names)), ["linearity", "cadence", "segment", "horizon"], rotation=20)
    axes[1, 0].set_yticks(np.arange(len(gate_rows)), [str(row["source_seed"]) for row in gate_rows])
    axes[1, 0].set_ylabel("source seed")
    axes[1, 0].set_title("Stability diagnostics")
    figure.colorbar(image, ax=axes[1, 0], fraction=0.046)
    shape = [row["cross_metric_shape_distance"] for row in gate_rows]
    overlap = [row["minimum_subspace_overlap"] for row in gate_rows]
    positions = np.arange(1, len(gate_rows) + 1)
    axes[1, 1].bar(positions - 0.18, shape, 0.36, label="shape distance", color="#a23b3b")
    axes[1, 1].bar(positions + 0.18, overlap, 0.36, label="subspace overlap", color="#176b87")
    axes[1, 1].set_xlabel("cyclic pair")
    axes[1, 1].set_title("Cross-metric geometry")
    axes[1, 1].legend(frameon=False)
    for axis in axes.flat:
        axis.grid(alpha=0.2)
    figure.tight_layout()
    destination.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(destination, dpi=180)
    plt.close(figure)


def _report(payload: dict[str, Any], report: Path, figure: Path) -> str:
    decision = payload["decision"]
    lines = [
        "# Carrier memory metric comparison",
        "",
        f"Generated: {payload['generated_utc']}",
        "",
        f"Status: **{decision['status']}** ({decision['pass_count']}/{decision['required_pairs']} pairs).",
        "",
        "## Scope",
        "",
        "This audit compares three metrics on the same reduced carrier feature",
        r"\(h=p_n\in\mathbb R^3\). It does not claim a metric on the complete",
        r"Markov state \((x,\rho,p,m)\). The predictive metric uses an independent",
        "probe knot and the already fixed one-way readout, so it does not assume the",
        "new reciprocal backchannel that it is intended to constrain.",
        "",
        "## Metrics",
        "",
        r"\[G_{\rm cov}=\operatorname{Cov}(p)^+,\]",
        r"\[G_{\rm pred}(T)=\sum_{\tau\le T}w_\tau J_\tau^T J_\tau/R_T^2,\]",
        r"\[G_{\rm kernel}(T)=\sum_{\tau\le T}w_\tau\|\delta m_\tau\|_{\mathcal H_K}^2 I.\]",
        "",
        r"Here \(J_\tau=\partial x^{(T)}_{n+\tau}/\partial p_n\) is measured by",
        "central finite differences. Covariance null directions are retained as null",
        "through a truncated pseudoinverse; no ridge is allowed to create stiffness.",
        "",
        f"![Metric comparison]({_relative_from(report, figure)})",
        "",
        "## Fixed design",
        "",
        f"- cyclic pairs: `{[(row['target_seed'], row['source_seed']) for row in payload['pairs']]}`",
        f"- horizons in memory times: `{payload['horizons_memory_times']}`",
        f"- cadences: `{payload['cadences']}` updates",
        f"- segments: `{payload['parameters']['segments']}`",
        f"- inherited gain: `{payload['parameters']['vector_eta']}`; no retuning",
        f"- distance: `{payload['parameters']['distance_ratio']} R_pair`; sigma: `{payload['parameters']['sigma_ratio']} R_source`",
        "",
        "## Pair decisions",
        "",
        "| target<-source | linearity | cadence scale | segment shape | horizon scale | cross shape | subspace | metric signatures | pass |",
        "|---|---:|---:|---:|---:|---:|---:|---|---|",
    ]
    for row in decision["pairs"]:
        signatures = "; ".join("/".join(item) for item in row["classification_signature"])
        lines.append(
            f"| {row['target_seed']}<-{row['source_seed']} | {row['linearity_error']:.3g} | "
            f"{row['cadence_scale_drift']:.3g} | {row['segment_shape_drift']:.3g} | "
            f"{row['horizon_scale_drift']:.3g} | {row['cross_metric_shape_distance']:.3g} | "
            f"{row['minimum_subspace_overlap']:.3g} | `{signatures}` | "
            f"{'pass' if row['pass'] else 'fail'} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "A common transverse support is partly structural because the normalized-direction",
            "Jacobian has rank two in d=3. Subspace overlap alone is therefore not evidence for",
            "an emergent metric. Scale, anisotropy, segment stability and held-out classification",
            "must agree as well.",
            "",
            "A reconciliation pass would nominate a reduced effective metric for a nonlinear",
            "holdout pilot; it would not establish microscopic geometry. A fail means that the",
            "Euclidean reciprocal eligibility result is representation- or normalization-sensitive",
            "and must not be promoted to an inertia or oscillation result.",
            "",
            "## Claim boundary",
            "",
            "The one-way readout, its Gaussian width and the carrier update remain model inputs.",
            "The covariance metric is observational, the predictive metric is probe-conditional,",
            "and the RKHS metric inherits the chosen Gaussian kernel. None is fundamental by itself.",
            "",
            "## Provenance",
            "",
            f"- Analysis revision: `{payload['git_revision']}`",
            f"- Worktree at start: `{payload['git_status'] or 'clean'}`",
        ]
    )
    for pair in payload["pairs"]:
        lines.append(
            f"- target {pair['target_seed']} <- source {pair['source_seed']}: "
            f"`{pair['source_case_path']}` and `{pair['target_case_path']}`"
        )
    return "\n".join(lines) + "\n"


def main() -> None:
    args = parse_args()
    git_status = _git_output(["status", "--short"])
    if git_status and not args.allow_dirty:
        raise SystemExit("refusing dirty worktree; commit preregistration or use --allow-dirty")
    seeds = _parse_ints(args.seeds)
    if len(seeds) < 2 or len(seeds) != len(set(seeds)):
        raise ValueError("at least two unique seeds are required")
    horizons_memory = _parse_floats(args.horizons_memory_times)
    if any(value <= 0.0 for value in horizons_memory):
        raise ValueError("horizons must be positive")
    cadences = sorted(set(_parse_ints(args.cadences)))
    if args.segments != 2:
        raise ValueError("this preregistration requires exactly two segments")
    if not 0.0 < args.lambda_vector < 1.0:
        raise ValueError("lambda-vector must lie in (0, 1)")
    horizons = [int(round(value / args.lambda_vector)) for value in horizons_memory]
    if any(horizon < 2 for horizon in horizons) or horizons != sorted(set(horizons)):
        raise ValueError("horizons must map to increasing update counts")
    cases = _discover_cases(args.case_glob or list(DEFAULT_CASE_GLOBS), seeds)
    pairs = []
    for target_seed, source_seed in zip(seeds, seeds[1:] + seeds[:1]):
        target_case = cases[target_seed]
        source_case = cases[source_seed]
        if target_case["config"] != source_case["config"]:
            raise ValueError("paired configurations must match")
        source_state = initialize_oriented_memory_state(
            source_case["state"],
            lambda_vector=args.lambda_vector,
            vector_mass=args.vector_mass,
            orientation_relaxation=args.orientation_relaxation,
        )
        target_state = initialize_oriented_memory_state(
            target_case["state"],
            lambda_vector=args.lambda_vector,
            vector_mass=args.vector_mass,
            orientation_relaxation=args.orientation_relaxation,
        )
        reference_source_radius = float(
            np.sqrt(np.trace(memory_shape_tensor(source_state.scalar_state)))
        )
        reference_target_radius = float(
            np.sqrt(np.trace(memory_shape_tensor(target_state.scalar_state)))
        )
        reference_pair_radius = 0.5 * (
            reference_source_radius + reference_target_radius
        )
        reference_geometry = {
            "source_radius": reference_source_radius,
            "target_radius": reference_target_radius,
            "offset_magnitude": args.distance_ratio * reference_pair_radius,
            "vector_sigma": args.sigma_ratio * reference_source_radius,
        }
        segments = []
        for segment in range(args.segments):
            result = run_segment(
                target_case,
                source_case,
                target_state,
                source_state,
                segment=segment,
                reference_geometry=reference_geometry,
                horizons=horizons,
                cadences=cadences,
                args=args,
            )
            advance_noise = result.pop("advance_noise")
            segments.append(result)
            source_state, target_state = _advance_states(
                source_state,
                target_state,
                target_case["config"],
                advance_noise["source"],
                advance_noise["target"],
            )
        pairs.append(
            {
                "target_seed": target_seed,
                "source_seed": source_seed,
                "target_case_path": _relative(target_case["path"]),
                "source_case_path": _relative(source_case["path"]),
                "target_case_sha256": target_case["case_sha256"],
                "source_case_sha256": source_case["case_sha256"],
                "reference_geometry": reference_geometry,
                "segments": segments,
            }
        )
    decision = evaluate_gates(
        pairs, horizons=horizons, cadences=cadences, args=args
    )
    payload = {
        "schema": "emergenz-knoten.carrier-memory-metric-comparison.v1",
        "generated_utc": datetime.now(UTC).isoformat(),
        "git_revision": _git_output(["rev-parse", "HEAD"]),
        "git_status": git_status,
        "parameters": {
            "lambda_vector": args.lambda_vector,
            "orientation_relaxation": args.orientation_relaxation,
            "vector_mass": args.vector_mass,
            "vector_eta": args.vector_eta,
            "distance_ratio": args.distance_ratio,
            "sigma_ratio": args.sigma_ratio,
            "segments": args.segments,
            "finite_difference": args.finite_difference,
            "covariance_cutoff": args.covariance_cutoff,
        },
        "thresholds": {
            key: getattr(args, key)
            for key in (
                "max_linearity_error",
                "max_cadence_scale_drift",
                "max_cadence_shape_drift",
                "max_segment_shape_drift",
                "max_horizon_scale_drift",
                "min_subspace_overlap",
                "required_pairs",
            )
        },
        "horizons_memory_times": horizons_memory,
        "horizon_updates": horizons,
        "cadences": cadences,
        "pairs": pairs,
        "decision": decision,
    }
    report = _resolve(args.report)
    summary = _resolve(args.summary_json)
    figure = _resolve(args.figure)
    _plot(payload, figure)
    report.parent.mkdir(parents=True, exist_ok=True)
    summary.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(_report(payload, report, figure), encoding="utf-8")
    summary.write_text(json.dumps(_jsonable(payload), indent=2) + "\n", encoding="utf-8")
    print(json.dumps(decision, indent=2))


if __name__ == "__main__":
    main()
