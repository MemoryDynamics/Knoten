"""Compare local mediator extensions under one fixed calibration.

The mediator is evolved on the one-dimensional source-target axis. This is a
controlled transport channel and does not reduce or select the ambient knot
dimension.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict
from datetime import UTC, datetime
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
    LocalMediatorGrid,
    RelaxationDiffusionMediator,
    SimulationConfig,
    TelegraphMediator,
    external_field_response_metrics,
    initialize_oriented_memory_state,
    paired_external_field_response,
    rectangular_source,
    simulate_relaxation_diffusion_mediator,
    simulate_telegraph_mediator,
)


def _repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("repository root not found")


ROOT = _repo_root()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fixed-calibration local oriented-mediator gate."
    )
    parser.add_argument(
        "--reference-summary",
        type=Path,
        default=Path(
            "reports/response/"
            "oriented_vector_fixed_pair_distance_gate_2026-07-26.json"
        ),
    )
    parser.add_argument("--pulse-memory-times", type=float, default=1.0)
    parser.add_argument("--horizon-memory-times", type=float, default=50.0)
    parser.add_argument("--sample-every", type=int, default=10)
    parser.add_argument("--grid-spacing-r0", type=float, default=0.25)
    parser.add_argument("--grid-left-r0", type=float, default=30.0)
    parser.add_argument("--grid-right-r0", type=float, default=45.0)
    parser.add_argument("--correlation-length-r0", type=float, default=5.0)
    parser.add_argument("--relaxation-memory-times", type=float, default=10.0)
    parser.add_argument("--fine-resolution-factor", type=int, default=2)
    parser.add_argument("--onset-fraction", type=float, default=0.05)
    parser.add_argument("--trial-coupling", type=float, default=1e-12)
    parser.add_argument("--prediction-max-relative-error", type=float, default=0.15)
    parser.add_argument("--resolution-max-relative-drift", type=float, default=0.10)
    parser.add_argument("--calibration-max-relative-error", type=float, default=0.01)
    parser.add_argument("--linearity-max-relative-error", type=float, default=0.01)
    parser.add_argument("--response-min-r", type=float, default=1e-5)
    parser.add_argument("--flip-cosine-max", type=float, default=-0.99)
    parser.add_argument("--flip-magnitude-min", type=float, default=0.9)
    parser.add_argument("--flip-magnitude-max", type=float, default=1.1)
    parser.add_argument("--target-radius-max-change", type=float, default=0.1)
    parser.add_argument("--target-shape-max-change", type=float, default=0.1)
    parser.add_argument("--response-monotonic-tolerance", type=float, default=0.1)
    parser.add_argument("--minimum-passing-holdout-pairs", type=int, default=4)
    parser.add_argument("--noise-seed", type=int, default=20_260_728)
    parser.add_argument("--allow-dirty", action="store_true")
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("reports/response/oriented/local_oriented_mediator_gate_2026-07-28.md"),
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=Path(
            "reports/response/oriented/local_oriented_mediator_gate_2026-07-28.json"
        ),
    )
    parser.add_argument(
        "--figure",
        type=Path,
        default=Path(
            "figures/draft/response/local_oriented_mediator_gate_2026-07-28.png"
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


def _load_case(path: Path, expected_sha256: str) -> dict[str, Any]:
    resolved = _resolve(path)
    raw = resolved.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if digest != expected_sha256:
        raise ValueError(f"snapshot checksum mismatch for {resolved}")
    payload = json.loads(raw.decode("utf-8"))
    if payload.get("condition") != "baseline":
        raise ValueError(f"{resolved} is not a baseline case")
    config = SimulationConfig(**payload["config"])
    snapshot = payload["diagnostics"]["memory_cloud"]["snapshot"]
    points = np.asarray(snapshot["points"], dtype=float)
    weights = np.asarray(snapshot["weights"], dtype=float)
    if points.ndim != 2 or points.shape[1] != config.dim:
        raise ValueError(f"invalid memory snapshot shape in {resolved}")
    if weights.shape != (points.shape[0],) or points.shape[0] < 2:
        raise ValueError(f"invalid memory weights in {resolved}")
    return {
        "path": resolved,
        "sha256": digest,
        "seed": int(payload["seed"]),
        "config": config,
        "state": FiniteMemoryState(x=points[0], memory=points, weights=weights),
    }


def trace_lags(
    times: np.ndarray,
    values: np.ndarray,
    *,
    onset_fraction: float,
) -> dict[str, float]:
    """Return relative-threshold onset and absolute-peak time."""

    if not 0.0 < onset_fraction < 1.0:
        raise ValueError("onset_fraction must lie in (0, 1)")
    magnitude = np.abs(np.asarray(values, dtype=float))
    if magnitude.ndim != 1 or magnitude.shape != np.asarray(times).shape:
        raise ValueError("times and values must be matching vectors")
    peak_index = int(np.argmax(magnitude))
    peak_value = float(magnitude[peak_index])
    if peak_value <= 0.0:
        return {"onset": float("nan"), "peak": float("nan"), "amplitude": 0.0}
    onset_candidates = np.flatnonzero(magnitude >= onset_fraction * peak_value)
    return {
        "onset": float(times[int(onset_candidates[0])]),
        "peak": float(times[peak_index]),
        "amplitude": peak_value,
    }


def relaxation_diffusion_peak_prediction(
    distance: float,
    *,
    diffusivity: float,
    decay_rate: float,
    pulse_duration: float,
) -> float:
    """Approximate rectangular-pulse peak from the killed heat kernel."""

    if min(distance, diffusivity, pulse_duration) <= 0.0 or decay_rate < 0.0:
        raise ValueError("peak-prediction parameters are outside their domain")
    if decay_rate == 0.0:
        impulse_peak = distance**2 / (2.0 * diffusivity)
    else:
        discriminant = 1.0 + 4.0 * decay_rate * distance**2 / diffusivity
        impulse_peak = (np.sqrt(discriminant) - 1.0) / (4.0 * decay_rate)
    return float(impulse_peak + 0.5 * pulse_duration)


def _sample_steps(n_steps: int, sample_every: int) -> np.ndarray:
    if n_steps < 1 or sample_every < 1:
        raise ValueError("n_steps and sample_every must be positive")
    return np.unique(np.concatenate((np.arange(0, n_steps + 1, sample_every), [n_steps])))


def _simulate_mediator_pair(
    *,
    model: str,
    grid: LocalMediatorGrid,
    source_values: np.ndarray,
    readout_positions: np.ndarray,
    correlation_length: float,
    relaxation_time: float,
):
    if model == "relaxation_diffusion":
        parameters = RelaxationDiffusionMediator(
            diffusivity=correlation_length**2 / relaxation_time,
            decay_rate=1.0 / relaxation_time,
        )
        trace = simulate_relaxation_diffusion_mediator(
            grid,
            parameters,
            source_values=source_values,
            readout_positions=readout_positions,
        )
    elif model == "telegraph":
        parameters = TelegraphMediator(
            wave_speed=correlation_length / relaxation_time,
            damping_rate=1.0 / relaxation_time,
            natural_frequency=1.0 / relaxation_time,
        )
        trace = simulate_telegraph_mediator(
            grid,
            parameters,
            source_values=source_values,
            readout_positions=readout_positions,
        )
    else:
        raise ValueError(f"unknown mediator model {model}")
    return trace, parameters


def _target_metrics(
    *,
    target_case: dict[str, Any],
    target_radius: float,
    orientation: np.ndarray,
    field_values: np.ndarray,
    coupling: float,
    noise: np.ndarray,
    sample_steps: np.ndarray,
) -> dict[str, Any]:
    forcing = coupling * field_values[1:, None] * orientation[None, :]
    response = paired_external_field_response(
        target_case["state"],
        target_case["config"],
        applied_displacements=forcing,
        noise=noise,
        sample_steps=sample_steps,
    )
    return external_field_response_metrics(response, radius=target_radius)


def _response_gates(metrics: dict[str, Any], thresholds: dict[str, float]) -> dict[str, bool]:
    return {
        "response": bool(metrics["active_response_r"] >= thresholds["response_min_r"]),
        "sign_flip": bool(
            metrics["flip_cosine"] <= thresholds["flip_cosine_max"]
            and thresholds["flip_magnitude_min"]
            <= metrics["flip_magnitude_ratio"]
            <= thresholds["flip_magnitude_max"]
        ),
        "shape_bounded": bool(
            metrics["target_radius_max_change"]
            <= thresholds["target_radius_max_change"]
            and metrics["target_shape_max_change"]
            <= thresholds["target_shape_max_change"]
        ),
    }


def _fmt(value: float) -> str:
    if value == 0.0:
        return "0"
    if abs(value) < 1e-3 or abs(value) >= 1e3:
        return f"{value:.3e}"
    return f"{value:.4f}"


def make_figure(payload: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(2, 2, figsize=(11.2, 8.0), constrained_layout=True)
    colors = {"relaxation_diffusion": "#2678a8", "telegraph": "#c65333"}
    labels = {
        "relaxation_diffusion": "relaxation-diffusion",
        "telegraph": "damped telegraph",
    }
    distance_ratios = np.asarray(payload["distance_ratios"], dtype=float)
    for model in ("relaxation_diffusion", "telegraph"):
        model_payload = payload["models"][model]
        calibration_trace = model_payload["transport_rows"][: len(distance_ratios)]
        for index, row in enumerate(calibration_trace):
            magnitude = np.abs(row["trace_values"])
            normalized = magnitude / max(float(np.max(magnitude)), np.finfo(float).tiny)
            axes[0, 0].plot(
                payload["trace_times_memory"],
                normalized,
                color=colors[model],
                alpha=0.35 + 0.25 * index,
                label=(
                    f"{labels[model]}, {distance_ratios[index]:g} R pair"
                    if index in (0, len(distance_ratios) - 1)
                    else None
                ),
            )
        measured = np.asarray(
            [row[model_payload["lag_metric"]] for row in model_payload["transport_rows"]]
        )
        predicted = np.asarray(
            [row["predicted_lag"] for row in model_payload["transport_rows"]]
        )
        axes[0, 1].scatter(
            predicted,
            measured,
            s=26,
            alpha=0.75,
            color=colors[model],
            label=labels[model],
        )
        responses_by_distance = []
        shape_by_distance = []
        for distance_index in range(len(distance_ratios)):
            response_values = []
            shape_values = []
            for pair in model_payload["pair_rows"]:
                metrics = pair["distance_rows"][distance_index]["target_metrics"]
                response_values.append(metrics["active_response_r"])
                shape_values.append(metrics["target_shape_max_change"])
            responses_by_distance.append(response_values)
            shape_by_distance.append(shape_values)
        for values, ratio in zip(responses_by_distance, distance_ratios, strict=True):
            axes[1, 0].scatter(
                np.full(len(values), ratio),
                values,
                color=colors[model],
                alpha=0.65,
                s=24,
            )
        axes[1, 0].plot(
            distance_ratios,
            [float(np.median(values)) for values in responses_by_distance],
            "o-",
            color=colors[model],
            label=labels[model],
        )
        axes[1, 1].plot(
            distance_ratios,
            [float(np.median(values)) for values in shape_by_distance],
            "o-",
            color=colors[model],
            label=labels[model],
        )

    axes[0, 0].set_xlim(0.0, payload["horizon_memory_times"])
    axes[0, 0].set_xlabel("memory times")
    axes[0, 0].set_ylabel("absolute readout / trace peak")
    axes[0, 0].set_title("Normalized source pulse, calibration-pair distances")
    axes[0, 0].legend(fontsize=8, ncol=2)
    maximum = max(axes[0, 1].get_xlim()[1], axes[0, 1].get_ylim()[1])
    axes[0, 1].plot([0.0, maximum], [0.0, maximum], "k--", lw=1.0)
    axes[0, 1].set_xlabel("predeclared lag prediction [memory times]")
    axes[0, 1].set_ylabel("measured lag [memory times]")
    axes[0, 1].set_title("All calibration and holdout distances")
    axes[0, 1].legend(fontsize=8)
    axes[1, 0].set_yscale("log")
    axes[1, 0].set_xlabel("distance / pair radius")
    axes[1, 0].set_ylabel("final target response / target radius")
    axes[1, 0].set_title("One global coupling per mediator law")
    axes[1, 0].legend(fontsize=8)
    axes[1, 1].set_yscale("log")
    axes[1, 1].axhline(
        payload["thresholds"]["target_shape_max_change"],
        color="black",
        linestyle="--",
        linewidth=1.0,
        label="shape bound",
    )
    axes[1, 1].set_xlabel("distance / pair radius")
    axes[1, 1].set_ylabel("median paired shape change")
    axes[1, 1].set_title("Target shape envelope")
    axes[1, 1].legend(fontsize=8)
    fig.savefig(path, dpi=180)
    plt.close(fig)


def build_report(
    payload: dict[str, Any],
    report_path: Path,
    figure_path: Path,
) -> str:
    lines = [
        "# Local Oriented-Mediator Gate",
        "",
        f"Generated: `{payload['generated_utc']}`.",
        "",
        "## Decision",
        "",
        f"Overall status: **{payload['decision']['status']}**.",
        "",
        payload["decision"]["interpretation"],
        "",
        f"![Mediator gate]({_relative_from(report_path, figure_path)})",
        "",
        "## Fixed design",
        "",
        "- The field is evolved locally on the one-dimensional relational axis "
        "between source and target. This is a transport-channel approximation, "
        "not an ambient-dimension claim.",
        "- A rectangular oriented source pulse lasts "
        f"`{_fmt(payload['pulse_memory_times'])}` memory time(s); the horizon is "
        f"`{_fmt(payload['horizon_memory_times'])}` memory times.",
        "- Both laws share the calibration-pair length "
        f"`R0={_fmt(payload['calibration_radius'])}`, correlation length "
        f"`{_fmt(payload['correlation_length']/payload['calibration_radius'])} R0`, "
        "and nominal zero-mode relaxation time "
        f"`{_fmt(payload['relaxation_memory_times'])}` memory times.",
        "- Exactly one scalar coupling per mediator law is calibrated on the first "
        "pair at the nearest distance. Every other pair and distance is a holdout; "
        "neither the length unit nor coupling is rescaled.",
        "- Active, global-sign-flip, and exact channel-off target paths share the "
        "same future noise. The source knot itself is frozen while its added "
        "oriented channel is pulsed.",
        "",
        "## Transport law",
        "",
        "The parabolic arm uses `d_t a = D d_xx a - mu a + s`. Its impulse "
        "Green function is proportional to "
        "`t^(-1/2) exp[-r^2/(4Dt)-mu t]`. Consequently, `t_peak ~ r^2` is "
        "only the near/weak-decay limit. The predeclared peak prediction is",
        "",
        "```text",
        "t_peak = [sqrt(1 + 4 mu r^2/D) - 1]/(4 mu) + pulse_duration/2.",
        "```",
        "",
        "At large distance it crosses toward a linear peak lag. The hyperbolic "
        "arm uses a critically damped field/momentum state and tests the onset "
        "against `r/c`. Thus a bare `r^2` versus `r` dichotomy would have been "
        "mathematically incorrect for the actual relaxation-diffusion law.",
        "",
    ]
    for model in ("relaxation_diffusion", "telegraph"):
        item = payload["models"][model]
        lines.extend(
            [
                f"### {model.replace('_', ' ').title()}",
                "",
                f"- calibrated coupling: `{_fmt(item['coupling'])}`",
                f"- calibration relative error: "
                f"`{_fmt(item['calibration']['relative_error'])}`",
                f"- half-amplitude linearity error: "
                f"`{_fmt(item['calibration']['linearity_error'])}`",
                f"- holdout lag median/max relative error: "
                f"`{_fmt(item['lag_prediction_median_relative_error'])}` / "
                f"`{_fmt(item['lag_prediction_max_relative_error'])}`",
                f"- primary/fine lag maximum relative drift: "
                f"`{_fmt(item['lag_resolution_max_relative_drift'])}`",
                f"- passing holdout pairs: "
                f"`{item['passing_holdout_pairs']}/{item['holdout_pair_count']}`",
                f"- architecture status: **{item['status']}**",
                "",
            ]
        )

    lines.extend(
        [
            "## Claim boundary",
            "",
            "A passing arm verifies the implementation, fixed-coupling holdout "
            "pipeline, and compatibility with the current scalar knot envelope. "
            "It does not discover a propagation law: diffusion or finite-front "
            "transport was inserted in the corresponding update rule. The two "
            "constructed transfer functions can be distinguished only if an "
            "independent source waveform excites their differing frequency bands. "
            "Choosing a physical law still needs an external criterion or data.",
            "",
            "No reciprocal interaction, photon, spin, charge, particle, Lorentz, "
            "QFT, or finite-signal-speed claim follows. A finite-difference "
            "diffusion stencil also has a grid cone at finite resolution; that is "
            "a numerical property, not a causal continuum bound.",
            "",
            "## When could three dimensions be selected?",
            "",
            "Not in this gate. A local field equation can be written in any "
            "supplied ambient dimension, and this runner uses only a relational "
            "axis. Fields may later provide a mechanism that gaps or suppresses "
            "directions, but the present code has no dynamical ambient-dimension "
            "variable. A defensible selection test must freeze one mediator law "
            "and the same absolute dimensionless parameters across several "
            "ambient dimensions, then show that an external response or slow-mode "
            "rank converges reproducibly to three while additional directions are "
            "suppressed. Merely running a field on a 3D grid assumes, rather than "
            "derives, three dimensions.",
            "",
            "## Reproducibility",
            "",
            f"- reference: `{payload['reference_summary']}`",
            f"- git revision: `{payload['git_revision']}`",
            f"- git status at start: `{payload['git_status_at_start'] or 'clean'}`",
            f"- command: `{' '.join(payload['command'])}`",
            "",
        ]
    )
    return chr(10).join(lines)


def main() -> None:
    args = parse_args()
    git_status = _git_output(["status", "--short"])
    if git_status not in ("", "unavailable") and not args.allow_dirty:
        raise RuntimeError("refusing to run from a dirty worktree; use --allow-dirty")
    reference_path = _resolve(args.reference_summary)
    reference = json.loads(reference_path.read_text(encoding="utf-8"))
    reference_rows = reference["rows"]
    distance_ratios = np.asarray(reference["distance_ratios"], dtype=float)
    if len(reference_rows) < 2 or len(distance_ratios) < 3:
        raise ValueError("reference summary lacks independent pairs or distances")

    cases: dict[tuple[int, str], dict[str, Any]] = {}
    pair_cases = []
    for row in reference_rows:
        target_key = (int(row["target_seed"]), row["target_case_sha256"])
        source_key = (int(row["source_seed"]), row["source_case_sha256"])
        if target_key not in cases:
            cases[target_key] = _load_case(
                Path(row["target_case_path"]), row["target_case_sha256"]
            )
        if source_key not in cases:
            cases[source_key] = _load_case(
                Path(row["source_case_path"]), row["source_case_sha256"]
            )
        pair_cases.append((row, cases[target_key], cases[source_key]))

    first_config = pair_cases[0][1]["config"]
    if any(
        target["config"] != first_config or source["config"] != first_config
        for _, target, source in pair_cases
    ):
        raise ValueError("all reference cases must share one simulation config")
    lambda_vector = float(reference["lambda_vector"])
    if not np.isclose(lambda_vector, first_config.alpha, rtol=0.0, atol=1e-15):
        raise ValueError("this gate requires scalar and oriented memory times to match")
    if min(
        args.pulse_memory_times,
        args.horizon_memory_times,
        args.grid_spacing_r0,
        args.grid_left_r0,
        args.grid_right_r0,
        args.correlation_length_r0,
        args.relaxation_memory_times,
        args.trial_coupling,
    ) <= 0.0:
        raise ValueError("time, grid, length, and trial-coupling values must be positive")
    if args.pulse_memory_times >= args.horizon_memory_times:
        raise ValueError("source pulse must end before the simulation horizon")
    if args.fine_resolution_factor < 2:
        raise ValueError("fine-resolution-factor must be at least two")

    n_steps = int(round(args.horizon_memory_times / lambda_vector))
    pulse_steps = int(round(args.pulse_memory_times / lambda_vector))
    if not np.isclose(n_steps * lambda_vector, args.horizon_memory_times):
        raise ValueError("horizon must resolve to an integer number of updates")
    if not np.isclose(pulse_steps * lambda_vector, args.pulse_memory_times):
        raise ValueError("pulse duration must resolve to an integer number of updates")
    sample_steps = _sample_steps(n_steps, args.sample_every)
    calibration_radius = float(reference_rows[0]["pair_radius"])
    spacing = args.grid_spacing_r0 * calibration_radius
    correlation_length = args.correlation_length_r0 * calibration_radius
    primary_grid = LocalMediatorGrid(
        spacing=spacing,
        time_step=lambda_vector,
        points_left=int(np.ceil(args.grid_left_r0 / args.grid_spacing_r0)),
        points_right=int(np.ceil(args.grid_right_r0 / args.grid_spacing_r0)),
    )
    all_distances = np.asarray(
        [
            float(row["pair_radius"] * ratio)
            for row in reference_rows
            for ratio in distance_ratios
        ],
        dtype=float,
    )
    if float(np.max(all_distances)) >= primary_grid.coordinates[-1]:
        raise ValueError("right grid extent does not contain every readout")

    source_values = rectangular_source(n_steps, pulse_steps=pulse_steps)
    refinement = int(args.fine_resolution_factor)
    substeps = refinement**2
    fine_grid = LocalMediatorGrid(
        spacing=spacing / refinement,
        time_step=lambda_vector / substeps,
        points_left=primary_grid.points_left * refinement,
        points_right=primary_grid.points_right * refinement,
    )
    fine_source = rectangular_source(
        n_steps * substeps,
        pulse_steps=pulse_steps * substeps,
    )
    thresholds = {
        "prediction_max_relative_error": args.prediction_max_relative_error,
        "resolution_max_relative_drift": args.resolution_max_relative_drift,
        "calibration_max_relative_error": args.calibration_max_relative_error,
        "linearity_max_relative_error": args.linearity_max_relative_error,
        "response_min_r": args.response_min_r,
        "flip_cosine_max": args.flip_cosine_max,
        "flip_magnitude_min": args.flip_magnitude_min,
        "flip_magnitude_max": args.flip_magnitude_max,
        "target_radius_max_change": args.target_radius_max_change,
        "target_shape_max_change": args.target_shape_max_change,
        "response_monotonic_tolerance": args.response_monotonic_tolerance,
        "minimum_passing_holdout_pairs": args.minimum_passing_holdout_pairs,
    }

    model_payloads: dict[str, dict[str, Any]] = {}
    for model in ("relaxation_diffusion", "telegraph"):
        trace, parameters = _simulate_mediator_pair(
            model=model,
            grid=primary_grid,
            source_values=source_values,
            readout_positions=all_distances,
            correlation_length=correlation_length,
            relaxation_time=args.relaxation_memory_times,
        )
        fine_trace, _ = _simulate_mediator_pair(
            model=model,
            grid=fine_grid,
            source_values=fine_source,
            readout_positions=all_distances,
            correlation_length=correlation_length,
            relaxation_time=args.relaxation_memory_times,
        )
        lag_metric = "peak" if model == "relaxation_diffusion" else "onset"
        transport_rows = []
        for index, distance in enumerate(all_distances):
            pair_index, distance_index = divmod(index, len(distance_ratios))
            primary_lags = trace_lags(
                trace.times,
                trace.values[:, index],
                onset_fraction=args.onset_fraction,
            )
            fine_lags = trace_lags(
                fine_trace.times,
                fine_trace.values[:, index],
                onset_fraction=args.onset_fraction,
            )
            if model == "relaxation_diffusion":
                prediction = relaxation_diffusion_peak_prediction(
                    float(distance),
                    diffusivity=parameters.diffusivity,
                    decay_rate=parameters.decay_rate,
                    pulse_duration=args.pulse_memory_times,
                )
            else:
                prediction = float(distance / parameters.wave_speed)
            measured_lag = float(primary_lags[lag_metric])
            fine_lag = float(fine_lags[lag_metric])
            row = {
                "pair_index": pair_index,
                "distance_index": distance_index,
                "distance": float(distance),
                "distance_r0": float(distance / calibration_radius),
                "distance_ratio_pair_radius": float(distance_ratios[distance_index]),
                **primary_lags,
                "fine_onset": float(fine_lags["onset"]),
                "fine_peak": float(fine_lags["peak"]),
                "predicted_lag": prediction,
                "prediction_relative_error": float(
                    abs(measured_lag - prediction) / prediction
                ),
                "resolution_relative_drift": float(
                    abs(measured_lag - fine_lag) / max(abs(fine_lag), np.finfo(float).tiny)
                ),
            }
            if pair_index == 0:
                row["trace_values"] = trace.values[sample_steps, index]
            transport_rows.append(row)

        calibration_row, calibration_target, calibration_source = pair_cases[0]
        calibration_orientation = initialize_oriented_memory_state(
            calibration_source["state"],
            lambda_vector=lambda_vector,
            vector_mass=float(reference["vector_mass"]),
            orientation_relaxation=float(reference["orientation_relaxation"]),
        ).carrier_orientation
        calibration_rng = np.random.default_rng(
            args.noise_seed
            + 10_007 * calibration_target["seed"]
            + 100_003 * calibration_source["seed"]
        )
        calibration_noise = calibration_rng.normal(
            size=(n_steps, first_config.dim)
        )
        reference_response = float(
            calibration_row["distance_rows"][0]["persistent"]["active_response_r"]
        )
        trial_metrics = _target_metrics(
            target_case=calibration_target,
            target_radius=float(calibration_row["target_radius"]),
            orientation=calibration_orientation,
            field_values=trace.values[:, 0],
            coupling=args.trial_coupling,
            noise=calibration_noise,
            sample_steps=sample_steps,
        )
        trial_response = float(trial_metrics["active_response_r"])
        if trial_response <= 1e-12:
            raise RuntimeError("trial coupling produces an unresolved response")
        coupling = float(args.trial_coupling * reference_response / trial_response)
        calibrated_metrics = _target_metrics(
            target_case=calibration_target,
            target_radius=float(calibration_row["target_radius"]),
            orientation=calibration_orientation,
            field_values=trace.values[:, 0],
            coupling=coupling,
            noise=calibration_noise,
            sample_steps=sample_steps,
        )
        half_metrics = _target_metrics(
            target_case=calibration_target,
            target_radius=float(calibration_row["target_radius"]),
            orientation=calibration_orientation,
            field_values=trace.values[:, 0],
            coupling=0.5 * coupling,
            noise=calibration_noise,
            sample_steps=sample_steps,
        )
        calibrated_response = float(calibrated_metrics["active_response_r"])
        calibration_error = abs(calibrated_response / reference_response - 1.0)
        linearity_error = abs(
            float(half_metrics["active_response_r"])
            / max(0.5 * calibrated_response, np.finfo(float).tiny)
            - 1.0
        )

        pair_rows = []
        for pair_index, (reference_row, target_case, source_case) in enumerate(pair_cases):
            orientation = initialize_oriented_memory_state(
                source_case["state"],
                lambda_vector=lambda_vector,
                vector_mass=float(reference["vector_mass"]),
                orientation_relaxation=float(reference["orientation_relaxation"]),
            ).carrier_orientation
            rng = np.random.default_rng(
                args.noise_seed
                + 10_007 * target_case["seed"]
                + 100_003 * source_case["seed"]
            )
            noise = rng.normal(size=(n_steps, first_config.dim))
            distance_rows = []
            responses = []
            lags = []
            for distance_index, ratio in enumerate(distance_ratios):
                trace_index = pair_index * len(distance_ratios) + distance_index
                metrics = _target_metrics(
                    target_case=target_case,
                    target_radius=float(reference_row["target_radius"]),
                    orientation=orientation,
                    field_values=trace.values[:, trace_index],
                    coupling=coupling,
                    noise=noise,
                    sample_steps=sample_steps,
                )
                gates = _response_gates(metrics, thresholds)
                responses.append(float(metrics["active_response_r"]))
                lags.append(float(transport_rows[trace_index][lag_metric]))
                stored_metrics = {
                    key: value
                    for key, value in metrics.items()
                    if key != "trace_active_response_r"
                }
                distance_rows.append(
                    {
                        "distance_ratio_pair_radius": float(ratio),
                        "distance_r0": float(
                            all_distances[trace_index] / calibration_radius
                        ),
                        "target_metrics": stored_metrics,
                        "gates": gates,
                    }
                )
            response_monotone = bool(
                np.all(
                    np.asarray(responses[1:])
                    <= np.asarray(responses[:-1])
                    * (1.0 + args.response_monotonic_tolerance)
                )
            )
            lag_monotone = bool(np.all(np.diff(lags) > 0.0))
            pair_gates = {
                "all_distance_controls": bool(
                    all(all(item["gates"].values()) for item in distance_rows)
                ),
                "response_monotone": response_monotone,
                "lag_monotone": lag_monotone,
            }
            pair_rows.append(
                {
                    "pair_index": pair_index,
                    "target_seed": int(target_case["seed"]),
                    "source_seed": int(source_case["seed"]),
                    "target_case_path": _relative(target_case["path"]),
                    "source_case_path": _relative(source_case["path"]),
                    "source_orientation_norm": float(np.linalg.norm(orientation)),
                    "distance_rows": distance_rows,
                    "gates": pair_gates,
                    "pair_pass": bool(all(pair_gates.values())),
                    "role": "calibration_pair" if pair_index == 0 else "holdout_pair",
                }
            )

        holdout_transport = transport_rows[1:]
        prediction_errors = np.asarray(
            [item["prediction_relative_error"] for item in holdout_transport]
        )
        resolution_drifts = np.asarray(
            [item["resolution_relative_drift"] for item in transport_rows]
        )
        holdout_pairs = pair_rows[1:]
        passing_holdout_pairs = sum(bool(item["pair_pass"]) for item in holdout_pairs)
        model_gates = {
            "calibration": bool(
                calibration_error <= args.calibration_max_relative_error
            ),
            "linearity": bool(linearity_error <= args.linearity_max_relative_error),
            "lag_prediction": bool(
                float(np.max(prediction_errors))
                <= args.prediction_max_relative_error
            ),
            "lag_resolution": bool(
                float(np.max(resolution_drifts))
                <= args.resolution_max_relative_drift
            ),
            "holdout_pairs": bool(
                passing_holdout_pairs >= args.minimum_passing_holdout_pairs
            ),
        }
        model_payloads[model] = {
            "parameters": asdict(parameters),
            "coupling": coupling,
            "lag_metric": lag_metric,
            "calibration": {
                "target_seed": int(calibration_target["seed"]),
                "source_seed": int(calibration_source["seed"]),
                "reference_response_r": reference_response,
                "trial_response_r": trial_response,
                "calibrated_response_r": calibrated_response,
                "relative_error": calibration_error,
                "half_response_r": float(half_metrics["active_response_r"]),
                "linearity_error": linearity_error,
            },
            "transport_rows": transport_rows,
            "pair_rows": pair_rows,
            "lag_prediction_median_relative_error": float(
                np.median(prediction_errors)
            ),
            "lag_prediction_max_relative_error": float(np.max(prediction_errors)),
            "lag_resolution_max_relative_drift": float(np.max(resolution_drifts)),
            "passing_holdout_pairs": int(passing_holdout_pairs),
            "holdout_pair_count": len(holdout_pairs),
            "gates": model_gates,
            "status": "pass" if all(model_gates.values()) else "fail",
        }

    passing_models = [
        model for model, item in model_payloads.items() if item["status"] == "pass"
    ]
    if len(passing_models) == 2:
        decision = {
            "status": "architecture_pass_mechanism_underdetermined",
            "passing_models": passing_models,
            "selected_next_step": "autonomous_source_spectrum_identifiability_audit",
            "interpretation": (
                "Both inserted mediator laws pass their own implementation and "
                "fixed-coupling knot-envelope gates. The current experiment cannot "
                "choose a physical law because each transport behavior is a model input."
            ),
        }
    elif len(passing_models) == 1:
        decision = {
            "status": "single_architecture_pass",
            "passing_models": passing_models,
            "selected_next_step": "autonomous_source_spectrum_identifiability_audit",
            "interpretation": (
                "Only one inserted mediator law remains compatible with the fixed "
                "numerical and knot-envelope gates. This is an architecture result, "
                "not discovery of a physical propagation law."
            ),
        }
    else:
        decision = {
            "status": "fail",
            "passing_models": [],
            "selected_next_step": "revise_or_stop_local_mediator_extension",
            "interpretation": (
                "Neither inserted mediator law passes the preregistered numerical "
                "and holdout knot-envelope gates."
            ),
        }

    report_path = _resolve(args.report)
    summary_path = _resolve(args.summary_json)
    figure_path = _resolve(args.figure)
    payload = {
        "generated_utc": datetime.now(UTC).isoformat(),
        "git_revision": _git_output(["rev-parse", "HEAD"]),
        "git_status_at_start": git_status,
        "command": ["python", *os.sys.argv],
        "reference_summary": _relative(reference_path),
        "reference_git_revision": reference.get("git_revision", "unavailable"),
        "formation_config": asdict(first_config),
        "distance_ratios": distance_ratios,
        "calibration_radius": calibration_radius,
        "lambda_vector": lambda_vector,
        "pulse_memory_times": float(args.pulse_memory_times),
        "horizon_memory_times": float(args.horizon_memory_times),
        "n_steps": n_steps,
        "pulse_steps": pulse_steps,
        "trace_times_memory": sample_steps * lambda_vector,
        "correlation_length": correlation_length,
        "relaxation_memory_times": float(args.relaxation_memory_times),
        "primary_grid": asdict(primary_grid),
        "fine_grid": asdict(fine_grid),
        "fine_substeps_per_target_update": substeps,
        "onset_fraction": float(args.onset_fraction),
        "thresholds": thresholds,
        "models": model_payloads,
        "decision": decision,
        "summary_json": summary_path,
        "figure": figure_path,
    }
    make_figure(payload, figure_path)
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(
        json.dumps(_jsonable(payload), indent=2, sort_keys=True) + chr(10),
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
