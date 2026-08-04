"""P3.2a/b: measurement-closure and relative-noise falsification gate."""

from __future__ import annotations

import argparse
from dataclasses import asdict
from datetime import UTC, datetime
from itertools import product
import json
import math
import os
from pathlib import Path
import subprocess
import time
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from emergenz_knoten import (
    LocalMediatorGrid,
    TelegraphMediator,
    load_finite_memory_checkpoint,
    memory_shape_tensor,
)
from emergenz_knoten.kernels import (
    effective_double_gaussian_parameters,
    two_scale_local_curvature,
)
from emergenz_knoten.reciprocal_diagnostics import (
    PanelDelayModeFit,
    PanelHankelAudit,
    correlated_pair_noise,
    fit_panel_delay_mode,
    fit_panel_hankel_audit,
)
from emergenz_knoten.retarded_reciprocal import (
    RETARDED_RECIPROCAL_CONDITIONS,
    retarded_reciprocal_pair_response,
)


def _repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("repository root not found")


ROOT = _repo_root()
DEFAULT_CHECKPOINT = Path(
    "data/processed/reference_states/"
    "scalar_Aatt35_N100M_d3_d10_seed1_2026-07-16/"
    "scalar_Aatt35_d3_seed1_N100000000.npz"
)
RETARDED = ("retarded_one_way", "retarded_reciprocal")
COLORS = {
    "channel_off": "#666666",
    "instantaneous_reciprocal": "#D55E00",
    "retarded_one_way": "#0072B2",
    "retarded_reciprocal": "#009E73",
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint", type=Path, default=DEFAULT_CHECKPOINT)
    parser.add_argument("--future-seeds", default="1,2,3")
    parser.add_argument("--noise-correlations", default="0,0.9,0.99")
    parser.add_argument("--updates", type=int, default=50_000)
    parser.add_argument("--closure-stride-updates", type=int, default=50)
    parser.add_argument("--delay-depths", default="1,2,5,10,20")
    parser.add_argument("--mode-depths", default="5,10,20")
    parser.add_argument("--hankel-depths", default="")
    parser.add_argument("--hankel-ranks", default="")
    parser.add_argument("--hankel-conditions", default="")
    parser.add_argument("--hankel-material-change", type=float, default=0.02)
    parser.add_argument("--train-fraction", type=float, default=0.6)
    parser.add_argument("--distance-ratio", type=float, default=2.5)
    parser.add_argument("--cross-gain", type=float, default=0.02)
    parser.add_argument("--correlation-length-r", type=float, default=5.0)
    parser.add_argument("--relaxation-memory-times", type=float, default=10.0)
    parser.add_argument("--grid-spacing-r", type=float, default=0.25)
    parser.add_argument("--grid-points-left", type=int, default=120)
    parser.add_argument("--grid-points-right", type=int, default=180)
    parser.add_argument("--analysis-burn-memory-times", type=float, default=100.0)
    parser.add_argument("--segments", type=int, default=4)
    parser.add_argument("--min-mode-segments", type=int, default=3)
    parser.add_argument("--min-candidate-seeds", type=int, default=2)
    parser.add_argument("--max-control-candidate-seeds", type=int, default=1)
    parser.add_argument("--prediction-ratio-max", type=float, default=0.9)
    parser.add_argument("--delay-plateau-relative-max", type=float, default=0.1)
    parser.add_argument("--fit-condition-max", type=float, default=1e8)
    parser.add_argument("--frequency-min-per-memory-time", type=float, default=0.05)
    parser.add_argument("--damping-max-per-memory-time", type=float, default=1.0)
    parser.add_argument("--mode-relative-range-max", type=float, default=0.25)
    parser.add_argument("--noise-seed-offset", type=int, default=20_260_804)
    parser.add_argument("--allow-dirty", action="store_true")
    parser.add_argument(
        "--report",
        type=Path,
        default=Path(
            "reports/response/measurement_closure_relative_noise_gate_2026-08-04.md"
        ),
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=Path(
            "reports/response/measurement_closure_relative_noise_gate_2026-08-04.json"
        ),
    )
    parser.add_argument(
        "--figure",
        type=Path,
        default=Path(
            "figures/draft/response/"
            "measurement_closure_relative_noise_gate_2026-08-04.png"
        ),
    )
    return parser


def parse_args() -> argparse.Namespace:
    return build_parser().parse_args()


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def _relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _relative_from(source: Path, target: Path) -> str:
    return Path(os.path.relpath(target.resolve(), source.resolve().parent)).as_posix()


def _git(arguments: list[str]) -> str:
    try:
        return subprocess.run(
            ["git", *arguments],
            cwd=ROOT,
            check=True,
            text=True,
            capture_output=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "unavailable"


def _jsonable(value: Any) -> Any:
    if isinstance(value, np.ndarray):
        return _jsonable(value.tolist())
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        number = float(value)
        return number if np.isfinite(number) else None
    if isinstance(value, (complex, np.complexfloating)):
        return {"real": float(value.real), "imag": float(value.imag)}
    if isinstance(value, Path):
        return _relative(value)
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    return value


def _integers(text: str, name: str) -> list[int]:
    values = [int(part.strip()) for part in text.split(",") if part.strip()]
    if (
        not values
        or len(values) != len(set(values))
        or any(value < 0 for value in values)
    ):
        raise ValueError(f"{name} must contain unique non-negative integers")
    return values


def _correlations(text: str) -> list[float]:
    values = [float(part.strip()) for part in text.split(",") if part.strip()]
    if (
        not values
        or len(values) != len(set(values))
        or any(value < 0.0 or value >= 1.0 for value in values)
    ):
        raise ValueError("correlations must be unique values in [0, 1)")
    return values


def _rotation(dim: int) -> np.ndarray:
    result = np.roll(np.eye(dim), shift=1, axis=0) if dim > 1 else np.eye(1)
    if np.linalg.det(result) < 0.0:
        result[[0, 1]] = result[[1, 0]]
    return result


def _fit_row(fit: PanelDelayModeFit) -> dict[str, Any]:
    return {
        "delay_depth": fit.delay_depth,
        "eigenvalues": fit.eigenvalues,
        "design_condition": fit.design_condition,
        "test_score_rmse": fit.test_score_rmse,
        "test_persistence_rmse": fit.test_persistence_rmse,
        "test_residual_ratio": fit.test_residual_ratio,
    }


def _hankel_row(audit: PanelHankelAudit) -> dict[str, Any]:
    return {
        "delay_depth": audit.delay_depth,
        "common_max_depth": audit.common_max_depth,
        "singular_values": audit.singular_values,
        "stable_rank": audit.stable_rank,
        "entropy_rank": audit.entropy_rank,
        "numerical_rank_1e6": audit.numerical_rank_1e6,
        "numerical_rank_1e8": audit.numerical_rank_1e8,
        "train_transitions": audit.train_transitions,
        "test_transitions": audit.test_transitions,
        "rank_fits": [
            {
                "retained_rank": fit.retained_rank,
                "eigenvalues": fit.eigenvalues,
                "retained_condition": fit.retained_condition,
                "train_score_rmse": fit.train_score_rmse,
                "test_score_rmse": fit.test_score_rmse,
                "test_persistence_rmse": fit.test_persistence_rmse,
                "test_residual_ratio": fit.test_residual_ratio,
            }
            for fit in audit.rank_fits
        ],
    }


def _candidate_modes(
    fit: PanelDelayModeFit,
    args: argparse.Namespace,
    sample_interval: float,
) -> list[dict[str, float]]:
    rows = []
    for value in fit.eigenvalues:
        if value.imag <= 1e-8 or not 0.0 < abs(value) < 1.0:
            continue
        frequency = float(abs(np.angle(value)) / sample_interval)
        damping = float(-math.log(abs(value)) / sample_interval)
        if (
            frequency >= args.frequency_min_per_memory_time
            and damping <= args.damping_max_per_memory_time
        ):
            rows.append({"frequency": frequency, "damping": damping})
    return rows


def _mode_spreads(
    rows: tuple[dict[str, float], ...],
    floor: float,
) -> tuple[float, float]:
    frequencies = [row["frequency"] for row in rows]
    dampings = [row["damping"] for row in rows]
    frequency = (max(frequencies) - min(frequencies)) / max(
        float(np.median(frequencies)), floor
    )
    damping = (max(dampings) - min(dampings)) / max(float(np.median(dampings)), floor)
    return float(frequency), float(damping)


def _consistent_mode(
    fits: list[PanelDelayModeFit],
    args: argparse.Namespace,
    sample_interval: float,
) -> dict[str, Any]:
    candidates = [_candidate_modes(fit, args, sample_interval) for fit in fits]
    if any(not rows for rows in candidates):
        return {"pass": False}
    ranked = []
    for combination in product(*candidates):
        frequency, damping = _mode_spreads(
            combination, args.frequency_min_per_memory_time
        )
        ranked.append((max(frequency, damping), frequency, damping, combination))
    _, frequency, damping, selected = min(ranked, key=lambda item: item[0])
    return {
        "pass": bool(
            frequency <= args.mode_relative_range_max
            and damping <= args.mode_relative_range_max
        ),
        "frequency_relative_range": frequency,
        "damping_relative_range": damping,
        "frequency": float(np.median([row["frequency"] for row in selected])),
        "damping": float(np.median([row["damping"] for row in selected])),
    }


def _mode_identity(
    state: np.ndarray,
    depths: list[int],
    args: argparse.Namespace,
    sample_interval: float,
    score_features: int,
) -> dict[str, Any]:
    boundaries = np.rint(np.linspace(0, state.shape[0], args.segments + 1)).astype(int)
    rows = []
    for segment in range(args.segments):
        subset = state[boundaries[segment] : boundaries[segment + 1]]
        fits = [
            fit_panel_delay_mode(
                subset,
                delay_depth=depth,
                train_fraction=args.train_fraction,
                score_features=score_features,
            )
            for depth in depths
        ]
        row = _consistent_mode(fits, args, sample_interval)
        row["segment"] = segment + 1
        rows.append(row)
    passed = [row for row in rows if row["pass"]]
    if len(passed) >= args.min_mode_segments:
        frequency, damping = _mode_spreads(
            tuple(
                {"frequency": row["frequency"], "damping": row["damping"]}
                for row in passed
            ),
            args.frequency_min_per_memory_time,
        )
    else:
        frequency = damping = math.inf
    return {
        "segments": rows,
        "matching_segments": len(passed),
        "frequency_relative_range": frequency,
        "damping_relative_range": damping,
        "identity_pass": bool(
            len(passed) >= args.min_mode_segments
            and frequency <= args.mode_relative_range_max
            and damping <= args.mode_relative_range_max
        ),
    }


def _closure(
    state: np.ndarray,
    depths: list[int],
    mode_depths: list[int],
    args: argparse.Namespace,
    sample_interval: float,
) -> dict[str, Any]:
    fits = [
        fit_panel_delay_mode(
            state,
            delay_depth=depth,
            train_fraction=args.train_fraction,
            score_features=2,
        )
        for depth in depths
    ]
    terminal, penultimate = fits[-1], fits[-2]
    plateau = abs(terminal.test_score_rmse - penultimate.test_score_rmse) / max(
        penultimate.test_score_rmse, np.finfo(float).tiny
    )
    closure_pass = bool(
        terminal.test_residual_ratio <= args.prediction_ratio_max
        and plateau <= args.delay_plateau_relative_max
    )
    identifiable = bool(terminal.design_condition <= args.fit_condition_max)
    identity = _mode_identity(
        state,
        mode_depths,
        args,
        sample_interval,
        score_features=2,
    )
    return {
        "fits": [_fit_row(fit) for fit in fits],
        "terminal_prediction_ratio": terminal.test_residual_ratio,
        "terminal_delay_plateau_change": plateau,
        "terminal_design_condition": terminal.design_condition,
        "closure_pass": closure_pass,
        "spectral_identifiability_pass": identifiable,
        "mode_identity": identity,
        "complex_candidate_pass": bool(
            closure_pass and identifiable and identity["identity_pass"]
        ),
    }


def _measured_states(
    response: Any,
    condition: int,
    start: int,
    stride: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    positions = 0.5 * (
        response.positions[start::stride, condition, 1]
        - response.positions[start::stride, condition, 0]
    )
    centers = 0.5 * (
        response.memory_centers[start::stride, condition, 1]
        - response.memory_centers[start::stride, condition, 0]
    )
    ambient = np.concatenate((positions, centers), axis=1)[:, None, :]
    base = np.stack((positions, centers), axis=-1)
    if response.conditions[condition] not in RETARDED:
        return base, base, ambient
    field = 0.5 * (
        response.mediator_readouts[start::stride, condition, 0]
        - response.mediator_readouts[start::stride, condition, 1]
    )
    momentum = 0.5 * (
        response.mediator_momentum_readouts[start::stride, condition, 0]
        - response.mediator_momentum_readouts[start::stride, condition, 1]
    )
    selected = np.stack((positions, centers, field, momentum), axis=-1)
    return base, selected, ambient


def run_gate(args: argparse.Namespace) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    checkpoint_path = _resolve(args.checkpoint)
    checkpoint = load_finite_memory_checkpoint(checkpoint_path)
    config = checkpoint.config
    seeds = _integers(args.future_seeds, "future seeds")
    correlations = _correlations(args.noise_correlations)
    depths = _integers(args.delay_depths, "delay depths")
    mode_depths = _integers(args.mode_depths, "mode depths")
    hankel_depths = (
        _integers(args.hankel_depths, "Hankel depths")
        if getattr(args, "hankel_depths", "")
        else []
    )
    hankel_ranks = (
        tuple(_integers(args.hankel_ranks, "Hankel ranks"))
        if getattr(args, "hankel_ranks", "")
        else ()
    )
    hankel_conditions = (
        tuple(
            part.strip() for part in args.hankel_conditions.split(",") if part.strip()
        )
        if getattr(args, "hankel_conditions", "")
        else ()
    )
    if correlations != sorted(correlations):
        raise SystemExit("noise correlations must be sorted")
    if any(depth < 1 for depth in depths + mode_depths):
        raise SystemExit("delay and mode depths must be positive")
    if depths != sorted(depths) or depths[-2:] != [10, 20]:
        raise SystemExit("registered delay ladder must end with 10,20")
    if not set(mode_depths).issubset(depths):
        raise SystemExit("mode depths must belong to delay ladder")
    if hankel_depths:
        if hankel_depths != sorted(hankel_depths) or any(
            depth < 1 for depth in hankel_depths
        ):
            raise SystemExit("Hankel depths must be increasing and positive")
        if not hankel_ranks:
            raise SystemExit("Hankel ranks are required with Hankel depths")
        if hankel_depths[-1] * args.closure_stride_updates <= 10_000:
            raise SystemExit("registered Hankel horizon must exceed 10000 updates")
        unknown = set(hankel_conditions) - set(RETARDED_RECIPROCAL_CONDITIONS)
        required = {"retarded_one_way", "retarded_reciprocal"}
        if unknown or not required.issubset(hankel_conditions):
            raise SystemExit(
                "Hankel conditions must include reciprocal and one-way arms"
            )
    if args.updates % args.closure_stride_updates:
        raise SystemExit("updates must be divisible by closure stride")
    if not args.allow_dirty and _git(["status", "--porcelain"]):
        raise SystemExit("working tree is dirty; commit first or pass --allow-dirty")

    radius = float(np.sqrt(np.trace(memory_shape_tensor(checkpoint.state))))
    separation = np.zeros(config.dim)
    separation[0] = args.distance_ratio * radius
    effective = effective_double_gaussian_parameters(
        dim=config.dim,
        sigma_rep=config.sigma_rep,
        sigma_att=config.sigma_att,
        amplitude_rep=config.amplitude_rep,
        amplitude_att=config.amplitude_att,
        deposition_kernel=config.deposition_kernel,
        deposition_sigma=config.deposition_sigma,
    )
    curvature = two_scale_local_curvature(**effective)
    if curvature <= 0.0:
        raise SystemExit("registered positive cross gain requires positive curvature")
    memory_mass = float(np.sum(checkpoint.state.weights))
    cross_eta = args.cross_gain / (memory_mass * curvature)
    relaxation = args.relaxation_memory_times
    grid = LocalMediatorGrid(
        spacing=args.grid_spacing_r * radius,
        time_step=config.alpha,
        points_left=args.grid_points_left,
        points_right=args.grid_points_right,
    )
    mediator = TelegraphMediator(
        wave_speed=args.correlation_length_r * radius / relaxation,
        damping_rate=1.0 / relaxation,
        natural_frequency=1.0 / relaxation,
    )
    sample_steps = np.arange(args.updates + 1)
    burn_updates = int(round(args.analysis_burn_memory_times / config.alpha))
    start_index = int(np.searchsorted(sample_steps, burn_updates))
    sample_interval = config.alpha * args.closure_stride_updates
    closure_samples = sample_steps[start_index :: args.closure_stride_updates].size
    if closure_samples // args.segments <= max(mode_depths) + 10:
        raise SystemExit("post-burn segments are too short for registered delays")
    if hankel_depths:
        split_target = int(math.floor(args.train_fraction * (closure_samples - 1)))
        if split_target - hankel_depths[-1] + 1 < 3:
            raise SystemExit(
                "post-burn trace is too short for the common Hankel train window"
            )
    rows: list[dict[str, Any]] = []
    traces: list[dict[str, Any]] = []
    started = time.perf_counter()
    static_gain = source_normalization = 0.0

    for seed in seeds:
        rng = np.random.default_rng(args.noise_seed_offset + seed)
        common_base = rng.standard_normal((args.updates, config.dim))
        relative_base = rng.standard_normal((args.updates, config.dim))
        for correlation in correlations:
            first_noise, second_noise = correlated_pair_noise(
                common_base, relative_base, correlation
            )
            response = retarded_reciprocal_pair_response(
                checkpoint.state,
                checkpoint.state,
                config,
                initial_center_separation=separation,
                first_noise=first_noise,
                second_noise=second_noise,
                sample_steps=sample_steps,
                cross_eta=cross_eta,
                mediator_grid=grid,
                mediator=mediator,
                mediator_readout_position=float(np.linalg.norm(separation)),
                second_rotation=_rotation(config.dim),
            )
            static_gain = response.static_readout_gain
            source_normalization = response.source_normalization
            conditions = {}
            for index, name in enumerate(response.conditions):
                base, selected, ambient = _measured_states(
                    response, index, start_index, args.closure_stride_updates
                )
                base_closure = _closure(
                    base, depths, mode_depths, args, sample_interval
                )
                closure = _closure(selected, depths, mode_depths, args, sample_interval)
                ambient_fit = fit_panel_delay_mode(
                    ambient,
                    train_fraction=args.train_fraction,
                    score_features=2 * config.dim,
                )
                condition_row = {
                    "feature_count": selected.shape[2],
                    "base_closure": base_closure,
                    "readout_gain_vs_base": float(
                        1.0
                        - closure["fits"][0]["test_score_rmse"]
                        / max(
                            base_closure["fits"][0]["test_score_rmse"],
                            np.finfo(float).tiny,
                        )
                    ),
                    "selected_gain_vs_base_delay": float(
                        1.0
                        - closure["fits"][-1]["test_score_rmse"]
                        / max(
                            base_closure["fits"][-1]["test_score_rmse"],
                            np.finfo(float).tiny,
                        )
                    ),
                    "terminal_delay_gain_vs_readout": float(
                        1.0
                        - closure["fits"][-1]["test_score_rmse"]
                        / max(
                            closure["fits"][0]["test_score_rmse"],
                            np.finfo(float).tiny,
                        )
                    ),
                    "closure": closure,
                    "ambient_full_ar1": _fit_row(ambient_fit),
                    "ambient_complex": bool(
                        ambient_fit.stable_complex_eigenvalues.size
                    ),
                    "final_distance_r": float(
                        np.linalg.norm(
                            response.memory_centers[-1, index, 1]
                            - response.memory_centers[-1, index, 0]
                        )
                        / radius
                    ),
                    "max_radius_ratio": float(np.max(response.radius_ratios[:, index])),
                }
                if hankel_depths and name in hankel_conditions:
                    maximum_depth = hankel_depths[-1]
                    condition_row["hankel_audit"] = {
                        "base": [
                            _hankel_row(
                                fit_panel_hankel_audit(
                                    base,
                                    delay_depth=depth,
                                    common_max_depth=maximum_depth,
                                    retained_ranks=hankel_ranks,
                                    train_fraction=args.train_fraction,
                                    score_features=2,
                                )
                            )
                            for depth in hankel_depths
                        ],
                        "selected": [
                            _hankel_row(
                                fit_panel_hankel_audit(
                                    selected,
                                    delay_depth=depth,
                                    common_max_depth=maximum_depth,
                                    retained_ranks=hankel_ranks,
                                    train_fraction=args.train_fraction,
                                    score_features=2,
                                )
                            )
                            for depth in hankel_depths
                        ],
                    }
                conditions[name] = condition_row
            node_rms = (
                config.epsilon
                * np.sqrt(np.mean(np.sum(first_noise * first_noise, axis=1)))
                / radius
            )
            relative_rms = (
                0.5
                * config.epsilon
                * np.sqrt(np.mean(np.sum((second_noise - first_noise) ** 2, axis=1)))
                / radius
            )
            row = {
                "future_seed": seed,
                "noise_correlation": correlation,
                "noise": {
                    "first_variance": float(np.var(first_noise)),
                    "second_variance": float(np.var(second_noise)),
                    "empirical_correlation": float(
                        np.corrcoef(first_noise.ravel(), second_noise.ravel())[0, 1]
                    ),
                    "node_noise_rms_r": float(node_rms),
                    "relative_half_noise_rms_r": float(relative_rms),
                },
                "conditions": conditions,
            }
            rows.append(row)
            traces.append(
                {
                    "future_seed": seed,
                    "noise_correlation": correlation,
                    "prediction_ratios": [
                        fit["test_residual_ratio"]
                        for fit in conditions["retarded_reciprocal"]["closure"]["fits"]
                    ],
                    "relative_noise_r": relative_rms,
                    "node_noise_r": node_rms,
                }
            )

    hankel_gate = None
    if hankel_depths:
        primary_deltas = []
        for row in rows:
            audits = row["conditions"]["retarded_reciprocal"]["hankel_audit"]["base"]
            for rank_index in range(len(hankel_ranks)):
                primary_deltas.append(
                    audits[-1]["rank_fits"][rank_index]["test_residual_ratio"]
                    - audits[0]["rank_fits"][rank_index]["test_residual_ratio"]
                )
        median_delta = float(np.median(primary_deltas))
        positive_fraction = float(np.mean(np.asarray(primary_deltas) > 0.0))
        negative_fraction = float(np.mean(np.asarray(primary_deltas) < 0.0))
        if median_delta >= args.hankel_material_change and positive_fraction >= 0.8:
            trend_classification = "longer history degrades held-out prediction"
        elif median_delta <= -args.hankel_material_change and negative_fraction >= 0.8:
            trend_classification = "longer history improves held-out prediction"
        else:
            trend_classification = "no rank-robust material long-history trend"
        hankel_gate = {
            "classification": trend_classification,
            "median_terminal_minus_initial_ratio": median_delta,
            "positive_delta_fraction": positive_fraction,
            "negative_delta_fraction": negative_fraction,
            "material_change_threshold": args.hankel_material_change,
            "maximum_horizon_updates": (
                hankel_depths[-1] * args.closure_stride_updates
            ),
            "common_train_and_test_targets": True,
            "pole_claim_allowed": False,
        }

    def counts(field: str) -> dict[str, dict[str, int]]:
        return {
            str(correlation): {
                name: sum(
                    row["noise_correlation"] == correlation
                    and row["conditions"][name]["closure"][field]
                    for row in rows
                )
                for name in RETARDED_RECIPROCAL_CONDITIONS
            }
            for correlation in correlations
        }

    closure_counts = counts("closure_pass")
    identifiable_counts = counts("spectral_identifiability_pass")
    candidate_counts = counts("complex_candidate_pass")
    low, high = str(correlations[0]), str(correlations[-1])
    controls_bounded = all(
        candidate_counts[str(correlation)][name] <= args.max_control_candidate_seeds
        for correlation in correlations
        for name in RETARDED_RECIPROCAL_CONDITIONS[:-1]
    )
    noise_unmasking = bool(
        candidate_counts[high]["retarded_reciprocal"] >= args.min_candidate_seeds
        and candidate_counts[low]["retarded_reciprocal"]
        <= args.max_control_candidate_seeds
        and controls_bounded
    )
    closure_high = bool(
        closure_counts[high]["retarded_reciprocal"] >= args.min_candidate_seeds
    )
    identifiable_high = bool(
        identifiable_counts[high]["retarded_reciprocal"] >= args.min_candidate_seeds
    )
    no_primary_candidates = all(
        candidate_counts[str(correlation)]["retarded_reciprocal"] == 0
        for correlation in correlations
    )
    if noise_unmasking:
        classification = "control-separated relative-noise unmasking candidate"
    elif closure_high and identifiable_high and no_primary_candidates:
        classification = "predictive closure; identifiable complex-mode null"
    elif closure_high:
        classification = "predictive closure candidate; spectrum non-identifiable"
    else:
        classification = "inconclusive measurement closure or mode identity"

    runtime = time.perf_counter() - started
    payload = {
        "schema": "emergenz-knoten.measurement-closure-relative-noise-gate",
        "schema_version": 1,
        "created_utc": datetime.now(UTC).isoformat(timespec="seconds"),
        "git_revision": _git(["rev-parse", "HEAD"]),
        "git_status": _git(["status", "--porcelain"]),
        "checkpoint": _relative(checkpoint_path),
        "checkpoint_update_index": checkpoint.update_index,
        "formation_seed": checkpoint.formation_seed,
        "config": asdict(config),
        "parameters": vars(args),
        "runtime_seconds": runtime,
        "derived": {
            "initial_radius": radius,
            "cross_eta": cross_eta,
            "closure_sample_interval_memory_times": sample_interval,
            "static_readout_gain": static_gain,
            "source_normalization": source_normalization,
            "expected_node_noise_rms_r": (
                config.epsilon * math.sqrt(config.dim) / radius
            ),
            "expected_relative_half_noise_rms_r": {
                str(correlation): (
                    config.epsilon
                    * math.sqrt(0.5 * config.dim * (1.0 - correlation))
                    / radius
                )
                for correlation in correlations
            },
        },
        "mediator_grid": asdict(grid),
        "mediator": asdict(mediator),
        "thresholds": {
            "prediction_ratio_max": args.prediction_ratio_max,
            "delay_plateau_relative_max": args.delay_plateau_relative_max,
            "fit_condition_max": args.fit_condition_max,
            "min_mode_segments": args.min_mode_segments,
            "mode_relative_range_max": args.mode_relative_range_max,
        },
        "rows": rows,
        "gate": {
            "closure_seed_counts": closure_counts,
            "spectrally_identifiable_seed_counts": identifiable_counts,
            "complex_candidate_seed_counts": candidate_counts,
            "controls_bounded_pass": controls_bounded,
            "high_correlation_closure_sufficient": closure_high,
            "high_correlation_spectral_identifiability_sufficient": (identifiable_high),
            "relative_noise_unmasking_candidate_pass": noise_unmasking,
            "classification": classification,
            "hankel_long_horizon": hankel_gate,
        },
    }
    return _jsonable(payload), traces


def _plot_hankel(payload: dict[str, Any], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    correlations = _correlations(payload["parameters"]["noise_correlations"])
    depths = _integers(payload["parameters"]["hankel_depths"], "Hankel depths")
    ranks = _integers(payload["parameters"]["hankel_ranks"], "Hankel ranks")
    stride = int(payload["parameters"]["closure_stride_updates"])
    horizons = np.asarray(depths) * stride
    rank_colors = plt.cm.viridis(np.linspace(0.12, 0.88, len(ranks)))
    fig, axes = plt.subplots(2, 2, figsize=(12.0, 8.4))

    for axis, correlation in zip(axes[0], (correlations[0], correlations[-1])):
        selected_rows = [
            row for row in payload["rows"] if row["noise_correlation"] == correlation
        ]
        for rank_index, (rank, color) in enumerate(zip(ranks, rank_colors)):
            values = [
                [
                    audit["rank_fits"][rank_index]["test_residual_ratio"]
                    for audit in row["conditions"]["retarded_reciprocal"][
                        "hankel_audit"
                    ]["base"]
                ]
                for row in selected_rows
            ]
            axis.plot(
                horizons,
                np.median(values, axis=0),
                marker="o",
                color=color,
                label=f"rank {rank}",
            )
        axis.axhline(1.0, color="#777777", linestyle="--", linewidth=1.0)
        axis.set_xscale("log")
        axis.set(
            xlabel="history horizon [updates]",
            ylabel="held-out RMSE / persistence",
            title=f"reciprocal visible state, rho={correlation:g}",
        )

    terminal_index = -1
    for condition, linestyle in (
        ("retarded_one_way", "--"),
        ("retarded_reciprocal", "-"),
    ):
        for correlation, marker in (
            (correlations[0], "o"),
            (correlations[-1], "s"),
        ):
            values = []
            for rank_index in range(len(ranks)):
                values.append(
                    np.median(
                        [
                            row["conditions"][condition]["hankel_audit"]["base"][
                                terminal_index
                            ]["rank_fits"][rank_index]["test_residual_ratio"]
                            for row in payload["rows"]
                            if row["noise_correlation"] == correlation
                        ]
                    )
                )
            axes[1, 0].plot(
                ranks,
                values,
                marker=marker,
                linestyle=linestyle,
                label=f"{condition}, rho={correlation:g}",
            )
    axes[1, 0].axhline(1.0, color="#777777", linestyle=":")
    axes[1, 0].set(
        xlabel="retained rank",
        ylabel="held-out RMSE / persistence",
        title=f"control separation at {horizons[-1]:g} updates",
    )

    for layer, color in (("base", "#0072B2"), ("selected", "#D55E00")):
        stable = []
        entropy = []
        for depth_index in range(len(depths)):
            audits = [
                row["conditions"]["retarded_reciprocal"]["hankel_audit"][layer][
                    depth_index
                ]
                for row in payload["rows"]
            ]
            stable.append(np.median([audit["stable_rank"] for audit in audits]))
            entropy.append(np.median([audit["entropy_rank"] for audit in audits]))
        axes[1, 1].plot(
            horizons,
            stable,
            color=color,
            marker="o",
            label=f"{layer} stable rank",
        )
        axes[1, 1].plot(
            horizons,
            entropy,
            color=color,
            marker="s",
            linestyle="--",
            label=f"{layer} entropy rank",
        )
    axes[1, 1].set_xscale("log")
    axes[1, 1].set_yscale("log")
    axes[1, 1].set(
        xlabel="history horizon [updates]",
        ylabel="effective rank",
        title="Hankel rank growth",
    )

    axes[0, 0].legend(fontsize=8)
    axes[1, 0].legend(fontsize=7)
    axes[1, 1].legend(fontsize=8)
    for axis in axes.ravel():
        axis.grid(alpha=0.25)
    fig.suptitle("P3.2 long-horizon persistence / reduced-rank audit")
    fig.tight_layout()
    fig.savefig(output, dpi=180)
    plt.close(fig)


def _plot_hankel(payload: dict[str, Any], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    correlations = _correlations(payload["parameters"]["noise_correlations"])
    depths = _integers(payload["parameters"]["hankel_depths"], "Hankel depths")
    ranks = _integers(payload["parameters"]["hankel_ranks"], "Hankel ranks")
    stride = int(payload["parameters"]["closure_stride_updates"])
    horizons = np.asarray(depths) * stride
    rank_colors = plt.cm.viridis(np.linspace(0.12, 0.88, len(ranks)))
    fig, axes = plt.subplots(2, 2, figsize=(12.0, 8.4))

    for axis, correlation in zip(axes[0], (correlations[0], correlations[-1])):
        selected_rows = [
            row for row in payload["rows"] if row["noise_correlation"] == correlation
        ]
        for rank_index, (rank, color) in enumerate(zip(ranks, rank_colors)):
            values = [
                [
                    audit["rank_fits"][rank_index]["test_residual_ratio"]
                    for audit in row["conditions"]["retarded_reciprocal"][
                        "hankel_audit"
                    ]["base"]
                ]
                for row in selected_rows
            ]
            axis.plot(
                horizons,
                np.median(values, axis=0),
                marker="o",
                color=color,
                label=f"rank {rank}",
            )
        axis.axhline(1.0, color="#777777", linestyle="--", linewidth=1.0)
        axis.set_xscale("log")
        axis.set(
            xlabel="history horizon [updates]",
            ylabel="held-out RMSE / persistence",
            title=f"reciprocal visible state, rho={correlation:g}",
        )

    for condition, linestyle in (
        ("retarded_one_way", "--"),
        ("retarded_reciprocal", "-"),
    ):
        for correlation, marker in (
            (correlations[0], "o"),
            (correlations[-1], "s"),
        ):
            values = []
            for rank_index in range(len(ranks)):
                values.append(
                    np.median(
                        [
                            row["conditions"][condition]["hankel_audit"]["base"][-1][
                                "rank_fits"
                            ][rank_index]["test_residual_ratio"]
                            for row in payload["rows"]
                            if row["noise_correlation"] == correlation
                        ]
                    )
                )
            axes[1, 0].plot(
                ranks,
                values,
                marker=marker,
                linestyle=linestyle,
                label=f"{condition}, rho={correlation:g}",
            )
    axes[1, 0].axhline(1.0, color="#777777", linestyle=":")
    axes[1, 0].set(
        xlabel="retained rank",
        ylabel="held-out RMSE / persistence",
        title=f"control separation at {horizons[-1]:g} updates",
    )

    for layer, color in (("base", "#0072B2"), ("selected", "#D55E00")):
        stable = []
        entropy = []
        for depth_index in range(len(depths)):
            audits = [
                row["conditions"]["retarded_reciprocal"]["hankel_audit"][layer][
                    depth_index
                ]
                for row in payload["rows"]
            ]
            stable.append(np.median([audit["stable_rank"] for audit in audits]))
            entropy.append(np.median([audit["entropy_rank"] for audit in audits]))
        axes[1, 1].plot(
            horizons,
            stable,
            color=color,
            marker="o",
            label=f"{layer} stable rank",
        )
        axes[1, 1].plot(
            horizons,
            entropy,
            color=color,
            marker="s",
            linestyle="--",
            label=f"{layer} entropy rank",
        )
    axes[1, 1].set_xscale("log")
    axes[1, 1].set_yscale("log")
    axes[1, 1].set(
        xlabel="history horizon [updates]",
        ylabel="effective rank",
        title="Hankel rank growth",
    )

    axes[0, 0].legend(fontsize=8)
    axes[1, 0].legend(fontsize=7)
    axes[1, 1].legend(fontsize=8)
    for axis in axes.ravel():
        axis.grid(alpha=0.25)
    fig.suptitle("P3.2 long-horizon persistence / reduced-rank audit")
    fig.tight_layout()
    fig.savefig(output, dpi=180)
    plt.close(fig)


def _plot(payload: dict[str, Any], traces: list[dict[str, Any]], output: Path) -> None:
    if payload["parameters"].get("hankel_depths"):
        _plot_hankel(payload, output)
        return
    output.parent.mkdir(parents=True, exist_ok=True)
    correlations = _correlations(payload["parameters"]["noise_correlations"])
    depths = _integers(payload["parameters"]["delay_depths"], "delay depths")
    fig, axes = plt.subplots(2, 2, figsize=(12.0, 8.4))

    for correlation in correlations:
        selected = [
            trace for trace in traces if trace["noise_correlation"] == correlation
        ]
        for trace in selected:
            axes[0, 0].plot(depths, trace["prediction_ratios"], alpha=0.22)
        axes[0, 0].plot(
            depths,
            np.median([trace["prediction_ratios"] for trace in selected], axis=0),
            marker="o",
            linewidth=1.8,
            label=f"rho={correlation:g}",
        )
    axes[0, 0].axhline(
        payload["thresholds"]["prediction_ratio_max"],
        color="#999999",
        linestyle="--",
    )
    axes[0, 0].set_xscale("log")
    axes[0, 0].set(
        xlabel="delay depth",
        ylabel="held-out RMSE / persistence",
        title="augmented predictive closure",
    )
    axes[0, 0].legend()

    for trace in traces:
        axes[0, 1].scatter(
            trace["noise_correlation"],
            trace["node_noise_r"],
            color="#0072B2",
            alpha=0.35,
        )
        axes[0, 1].scatter(
            trace["noise_correlation"],
            trace["relative_noise_r"],
            color="#D55E00",
            alpha=0.35,
        )
    axes[0, 1].axhline(
        payload["derived"]["expected_node_noise_rms_r"],
        color="#0072B2",
        label="node marginal",
    )
    axes[0, 1].plot(
        correlations,
        [
            payload["derived"]["expected_relative_half_noise_rms_r"][str(correlation)]
            for correlation in correlations
        ],
        color="#D55E00",
        marker="o",
        label="relative half-noise",
    )
    axes[0, 1].set(
        xlabel="rho",
        ylabel="RMS step / R",
        title="fixed marginals, reduced relative noise",
    )
    axes[0, 1].legend()

    width = 0.18
    for index, name in enumerate(RETARDED_RECIPROCAL_CONDITIONS):
        values = [
            payload["gate"]["complex_candidate_seed_counts"][str(correlation)][name]
            for correlation in correlations
        ]
        axes[1, 0].bar(
            np.arange(len(correlations)) + (index - 1.5) * width,
            values,
            width,
            color=COLORS[name],
            label=name,
        )
    axes[1, 0].set_xticks(
        np.arange(len(correlations)), [str(value) for value in correlations]
    )
    axes[1, 0].set(
        xlabel="rho",
        ylabel="candidate seeds",
        title="registered augmented mode gate",
    )
    axes[1, 0].legend(fontsize=7)

    for name in RETARDED_RECIPROCAL_CONDITIONS:
        for correlation in correlations:
            values = [
                row["conditions"][name]["final_distance_r"]
                for row in payload["rows"]
                if row["noise_correlation"] == correlation
            ]
            axes[1, 1].scatter(
                [correlation] * len(values),
                values,
                color=COLORS[name],
                alpha=0.35,
            )
            axes[1, 1].plot(
                correlation,
                np.median(values),
                marker="D",
                color=COLORS[name],
            )
        axes[1, 1].plot([], [], color=COLORS[name], label=name)
    axes[1, 1].set(
        xlabel="rho",
        ylabel="final memory-centre distance / R",
        title="binding response",
    )
    axes[1, 1].set_yscale("log")
    axes[1, 1].legend(fontsize=7)

    for axis in axes.ravel():
        axis.grid(alpha=0.25)
    fig.suptitle("P3.2a/b measurement closure and relative noise")
    fig.tight_layout()
    fig.savefig(output, dpi=180)
    plt.close(fig)


def _hankel_report_lines(payload: dict[str, Any]) -> list[str]:
    depths = _integers(payload["parameters"]["hankel_depths"], "Hankel depths")
    ranks = _integers(payload["parameters"]["hankel_ranks"], "Hankel ranks")
    correlations = _correlations(payload["parameters"]["noise_correlations"])
    stride = int(payload["parameters"]["closure_stride_updates"])
    gate = payload["gate"]["hankel_long_horizon"]
    lines = [
        "",
        "## Long-horizon reduced-rank follow-up",
        "",
        f"The fixed delay ladder {depths} corresponds to history horizons",
        f"{depths[0] * stride}..{depths[-1] * stride} updates at unchanged",
        f"{stride}-update cadence. Fixed retained ranks are {ranks}. Every depth",
        "uses identical train-target and held-out target times; only the amount",
        "of represented history changes.",
        "",
        f"Registered trend classification: **{gate['classification']}**.",
        "",
        f"The median terminal-minus-initial prediction ratio is "
        f"{gate['median_terminal_minus_initial_ratio']:.4g}; the fractions of",
        f"positive/negative pathwise changes are {gate['positive_delta_fraction']:.3g}/"
        f"{gate['negative_delta_fraction']:.3g}. A material change required an",
        f"absolute ratio shift of at least {gate['material_change_threshold']:.3g}",
        "with at least 80% sign agreement.",
        "",
        "| rho | rank | reciprocal start | reciprocal terminal | delta | one-way terminal |",
        "| ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for correlation in correlations:
        selected_rows = [
            row for row in payload["rows"] if row["noise_correlation"] == correlation
        ]
        for rank_index, rank in enumerate(ranks):
            reciprocal = [
                row["conditions"]["retarded_reciprocal"]["hankel_audit"]["base"]
                for row in selected_rows
            ]
            one_way = [
                row["conditions"]["retarded_one_way"]["hankel_audit"]["base"]
                for row in selected_rows
            ]
            start = float(
                np.median(
                    [
                        row[0]["rank_fits"][rank_index]["test_residual_ratio"]
                        for row in reciprocal
                    ]
                )
            )
            terminal = float(
                np.median(
                    [
                        row[-1]["rank_fits"][rank_index]["test_residual_ratio"]
                        for row in reciprocal
                    ]
                )
            )
            control = float(
                np.median(
                    [
                        row[-1]["rank_fits"][rank_index]["test_residual_ratio"]
                        for row in one_way
                    ]
                )
            )
            lines.append(
                f"| {correlation:g} | {rank} | {start:.4g} | {terminal:.4g} | "
                f"{terminal - start:+.4g} | {control:.4g} |"
            )
    base_terminal = [
        row["conditions"]["retarded_reciprocal"]["hankel_audit"]["base"][-1]
        for row in payload["rows"]
    ]
    selected_terminal = [
        row["conditions"]["retarded_reciprocal"]["hankel_audit"]["selected"][-1]
        for row in payload["rows"]
    ]
    lines.extend(
        [
            "",
            "At the terminal horizon, median stable/entropy ranks are "
            f"{np.median([row['stable_rank'] for row in base_terminal]):.3g}/"
            f"{np.median([row['entropy_rank'] for row in base_terminal]):.3g} for the "
            "visible state and "
            f"{np.median([row['stable_rank'] for row in selected_terminal]):.3g}/"
            f"{np.median([row['entropy_rank'] for row in selected_terminal]):.3g} for the "
            "field/momentum-augmented state.",
            "",
            "Reduced DMD poles are stored for audit but are not promoted to a mode",
            "result here. Rank-, depth-, segment-, and one-way-control stability is",
            "still required before spectral interpretation.",
        ]
    )
    return lines


def _report(payload: dict[str, Any], report: Path, figure: Path) -> str:
    gate = payload["gate"]
    primary_rows = [row["conditions"]["retarded_reciprocal"] for row in payload["rows"]]
    base_rows = [row["base_closure"] for row in primary_rows]
    selected_rows = [row["closure"] for row in primary_rows]
    correlations = _correlations(payload["parameters"]["noise_correlations"])

    def value_range(values: list[float]) -> tuple[float, float]:
        return float(min(values)), float(max(values))

    base_conditions = value_range(
        [row["terminal_design_condition"] for row in base_rows]
    )
    selected_conditions = value_range(
        [row["terminal_design_condition"] for row in selected_rows]
    )
    selected_gains = value_range(
        [row["selected_gain_vs_base_delay"] for row in primary_rows]
    )
    observed_node_noise = value_range(
        [row["noise"]["node_noise_rms_r"] for row in payload["rows"]]
    )
    observed_relative_noise = {
        correlation: value_range(
            [
                row["noise"]["relative_half_noise_rms_r"]
                for row in payload["rows"]
                if row["noise_correlation"] == correlation
            ]
        )
        for correlation in correlations
    }
    mean_distances = {
        correlation: float(
            np.mean(
                [
                    row["conditions"]["retarded_reciprocal"]["final_distance_r"]
                    for row in payload["rows"]
                    if row["noise_correlation"] == correlation
                ]
            )
        )
        for correlation in correlations
    }
    base_matching = sum(row["mode_identity"]["matching_segments"] for row in base_rows)
    selected_matching = sum(
        row["mode_identity"]["matching_segments"] for row in selected_rows
    )
    base_identifiable = sum(row["spectral_identifiability_pass"] for row in base_rows)
    selected_identifiable = sum(
        row["spectral_identifiability_pass"] for row in selected_rows
    )
    base_candidates = sum(row["complex_candidate_pass"] for row in base_rows)
    selected_candidates = sum(row["complex_candidate_pass"] for row in selected_rows)
    ambient_primary = sum(row["ambient_complex"] for row in primary_rows)
    ambient_off = sum(
        row["conditions"]["channel_off"]["ambient_complex"] for row in payload["rows"]
    )
    total = len(primary_rows)
    total_segments = total * int(payload["parameters"]["segments"])

    lines = [
        "# P3.2a/b measurement closure and relative-noise gate",
        "",
        f"Date: {payload['created_utc']}.",
        "",
        "## Design",
        "",
        "The fixed P3.2 checkpoint, kernel, lambda, epsilon, gain, distance, and",
        "Telegraph mediator are unchanged. The visible (x-minus,m-minus) delay",
        "ladder and the field/momentum-augmented ladder use depths 1,2,5,10,20",
        "at 0.5-memory-time cadence with one common chronological 60/40 holdout.",
        "Only held-out visible/memory prediction is scored against persistence.",
        "",
        "Node-noise marginals remain fixed while rho = 0, 0.9, 0.99 changes only",
        "relative noise. Channel-off, instantaneous reciprocal, and retarded",
        "one-way remain controls. All paths continue one formation checkpoint.",
        "",
        "## Registered result",
        "",
        f"Classification: **{gate['classification']}**.",
        "",
        f"- augmented predictive closure: {sum(row['closure_pass'] for row in selected_rows)}/{total};",
        f"- augmented spectral identifiability: {selected_identifiable}/{total};",
        f"- augmented complex candidates: {selected_candidates}/{total};",
        f"- controls bounded: {gate['controls_bounded_pass']};",
        f"- relative-noise unmasking candidate: {gate['relative_noise_unmasking_candidate_pass']}.",
        "",
        "The registered augmented spectrum is therefore inconclusive, not a",
        "complex-mode null: its terminal design matrices are rank-deficient or",
        f"near-rank-deficient (condition {selected_conditions[0]:.3e}..{selected_conditions[1]:.3e}).",
        "",
        "## Reconciliation",
        "",
        "The visible delay layer is substantially better identified:",
        "",
        f"- visible predictive closure: {sum(row['closure_pass'] for row in base_rows)}/{total};",
        f"- visible spectral identifiability: {base_identifiable}/{total}, condition {base_conditions[0]:.3g}..{base_conditions[1]:.3g};",
        f"- visible depth-stable matching segments: {base_matching}/{total_segments};",
        f"- visible complex candidates: {base_candidates}/{total}.",
        "",
        "Adding target field and momentum readouts does not improve held-out",
        f"prediction relative to the visible delay ladder: gain {100 * selected_gains[0]:.3g}%..{100 * selected_gains[1]:.3g}%.",
        f"The augmented fits nevertheless match complex poles in {selected_matching}/{total_segments}",
        "segments. Because these poles occur with severe rank deficiency and the",
        "inserted Telegraph channel already contains complex internal poles,",
        "they are not identifiable knot modes.",
        "",
        "The separate full ambient AR(1) fit is also not control-separated:",
        f"complex in {ambient_primary}/{total} retarded-reciprocal paths and {ambient_off}/{total}",
        "channel-off paths. It supplies no ambient-rotation candidate.",
        "",
        "## Relative noise",
        "",
        f"The observed node RMS remains {observed_node_noise[0]:.4g}..{observed_node_noise[1]:.4g} R",
        f"around the expected {payload['derived']['expected_node_noise_rms_r']:.4g} R.",
    ]
    for correlation in correlations:
        expected = payload["derived"]["expected_relative_half_noise_rms_r"][
            str(correlation)
        ]
        observed = observed_relative_noise[correlation]
        lines.append(
            f"- rho={correlation:g}: relative RMS {observed[0]:.4g}..{observed[1]:.4g} R "
            f"(expected {expected:.4g} R), mean final reciprocal distance "
            f"{mean_distances[correlation]:.4g} R;"
        )
    lines.extend(
        [
            "",
            "Lower relative diffusion strengthens binding but leaves the closure",
            "curves nearly unchanged. This is not evidence for an unmasked",
            "oscillation.",
            "",
            f"![Gate summary]({_relative_from(report, figure)})",
            "",
            "| seed | rho | visible ratio | augmented ratio | augmented gain | condition | matching segments | relative noise/R | final distance/R |",
            "| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in payload["rows"]:
        primary = row["conditions"]["retarded_reciprocal"]
        closure = primary["closure"]
        lines.append(
            f"| {row['future_seed']} | {row['noise_correlation']:.2g} | "
            f"{primary['base_closure']['terminal_prediction_ratio']:.4g} | "
            f"{closure['terminal_prediction_ratio']:.4g} | "
            f"{100 * primary['selected_gain_vs_base_delay']:.3g}% | "
            f"{closure['terminal_design_condition']:.3e} | "
            f"{closure['mode_identity']['matching_segments']} | "
            f"{row['noise']['relative_half_noise_rms_r']:.4g} | "
            f"{primary['final_distance_r']:.4g} |"
        )
    if payload["parameters"].get("hankel_depths"):
        lines.extend(_hankel_report_lines(payload))
        next_measurement = [
            "This completes the common-window long-history prediction and rank",
            "stage. The remaining spectral step is a preregistered pole-identity",
            "audit across fixed ranks, delay depths, time segments, and the one-way",
            "control; no gain, lambda, epsilon, or kernel retuning is allowed.",
        ]
    else:
        next_measurement = [
            *next_measurement,
        ]
    lines.extend(
        [
            "",
            "## Boundary and decision",
            "",
            "A passed predictive gate is cadence- and horizon-specific, not an exact",
            "Markov theorem. The complete mediator grid remains hidden. The current",
            "data support a well-conditioned visible delay-state null at the",
            "registered cadence, but not an augmented-system null.",
            "",
            *next_measurement,
            "",
            "No spin, d=3 selection, particle, photon, Lorentz, QFT, or",
            "Standard-Model claim follows.",
            "",
            "## Reproducibility",
            "",
            f"- checkpoint: {payload['checkpoint']};",
            f"- git revision: {payload['git_revision']};",
            f"- git status at start: {'clean' if not payload['git_status'] else payload['git_status']};",
            f"- runtime: {payload['runtime_seconds']:.3f} s;",
            "- command: python experiments/current/memory/synchronization/"
            "measurement_closure_relative_noise_gate.py;",
            "- [machine-readable summary]"
            f"({_relative_from(report, _resolve(Path(payload['parameters']['summary_json'])))}).",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    args = parse_args()
    payload, traces = run_gate(args)
    report = _resolve(args.report)
    summary = _resolve(args.summary_json)
    figure = _resolve(args.figure)
    summary.parent.mkdir(parents=True, exist_ok=True)
    summary.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    _plot(payload, traces, figure)
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(_report(payload, report, figure), encoding="utf-8")


if __name__ == "__main__":
    main()
