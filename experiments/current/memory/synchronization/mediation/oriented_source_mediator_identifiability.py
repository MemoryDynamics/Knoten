"""Audit whether autonomous oriented sources can distinguish two mediators."""

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
    autonomous_oriented_source_trace,
    initialize_oriented_memory_state,
    normalized_shape_spectra,
    simulate_relaxation_diffusion_mediator,
    simulate_telegraph_mediator,
    transfer_identifiability_metrics,
    vector_segment_power,
)


def _repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("repository root not found")


ROOT = _repo_root()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Autonomous-source eligibility for fixed local mediators."
    )
    parser.add_argument(
        "--mediator-summary",
        type=Path,
        default=Path(
            "reports/response/oriented/local_oriented_mediator_gate_2026-07-28.json"
        ),
    )
    parser.add_argument("--burn-memory-times", type=float, default=20.0)
    parser.add_argument("--segments", type=int, default=2)
    parser.add_argument("--segment-updates", type=int, default=8192)
    parser.add_argument("--minimum-frequency-contrast", type=float, default=0.25)
    parser.add_argument("--weighted-contrast-min", type=float, default=0.25)
    parser.add_argument("--distinguishable-power-min", type=float, default=0.20)
    parser.add_argument("--transmitted-power-min", type=float, default=0.01)
    parser.add_argument("--segment-drift-max", type=float, default=0.25)
    parser.add_argument("--orientation-rms-min", type=float, default=1e-3)
    parser.add_argument("--source-radius-max-change", type=float, default=0.5)
    parser.add_argument("--source-spectrum-max-drift", type=float, default=0.25)
    parser.add_argument("--minimum-passing-pairs", type=int, default=5)
    parser.add_argument("--noise-seed", type=int, default=20_260_728)
    parser.add_argument("--plot-omega-max", type=float, default=10.0)
    parser.add_argument("--allow-dirty", action="store_true")
    parser.add_argument(
        "--report",
        type=Path,
        default=Path(
            "reports/response/"
            "oriented_source_mediator_identifiability_2026-07-28.md"
        ),
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=Path(
            "reports/response/"
            "oriented_source_mediator_identifiability_2026-07-28.json"
        ),
    )
    parser.add_argument(
        "--figure",
        type=Path,
        default=Path(
            "figures/draft/response/"
            "oriented_source_mediator_identifiability_2026-07-28.png"
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
    if isinstance(value, np.bool_):
        return bool(value)
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
    config = SimulationConfig(**payload["config"])
    snapshot = payload["diagnostics"]["memory_cloud"]["snapshot"]
    points = np.asarray(snapshot["points"], dtype=float)
    weights = np.asarray(snapshot["weights"], dtype=float)
    return {
        "path": resolved,
        "sha256": digest,
        "seed": int(payload["seed"]),
        "config": config,
        "state": FiniteMemoryState(x=points[0], memory=points, weights=weights),
    }


def relative_segment_drift(values: np.ndarray) -> float:
    """Return full segment range divided by the segment mean."""

    numbers = np.asarray(values, dtype=float)
    if numbers.ndim != 1 or numbers.size < 2 or np.any(numbers < 0.0):
        raise ValueError("segment values must be a non-negative vector")
    mean = float(np.mean(numbers))
    if mean <= 0.0:
        return 0.0 if np.all(numbers == 0.0) else float("inf")
    return float((np.max(numbers) - np.min(numbers)) / mean)


def pair_gate(
    distance_rows: list[dict[str, Any]],
    *,
    orientation_rms: float,
    radius_change: float,
    spectrum_drift: float,
    thresholds: dict[str, float],
) -> dict[str, bool]:
    """Apply the preregistered source and all-distance eligibility criteria."""

    return {
        "orientation_amplitude": bool(
            orientation_rms >= thresholds["orientation_rms_min"]
        ),
        "source_shape_bounded": bool(
            radius_change <= thresholds["source_radius_max_change"]
            and spectrum_drift <= thresholds["source_spectrum_max_drift"]
        ),
        "weighted_contrast": bool(
            all(
                row["persistent"]["pooled_weighted_contrast"]
                >= thresholds["weighted_contrast_min"]
                for row in distance_rows
            )
        ),
        "distinguishable_power": bool(
            all(
                row["persistent"]["pooled_distinguishable_power_fraction"]
                >= thresholds["distinguishable_power_min"]
                for row in distance_rows
            )
        ),
        "transmitted_power": bool(
            all(
                row["persistent"]["pooled_transmitted_power_fraction"]
                >= thresholds["transmitted_power_min"]
                for row in distance_rows
            )
        ),
        "segment_stability": bool(
            all(
                row["persistent"]["weighted_contrast_segment_drift"]
                <= thresholds["segment_drift_max"]
                for row in distance_rows
            )
        ),
    }


def _compact_identifiability(metrics: dict[str, Any]) -> dict[str, Any]:
    return {
        "weighted_contrast": metrics["weighted_contrast"],
        "distinguishable_power_fraction": metrics[
            "distinguishable_power_fraction"
        ],
        "transmitted_power_fraction": metrics["transmitted_power_fraction"],
        "pooled_weighted_contrast": metrics["pooled_weighted_contrast"],
        "pooled_distinguishable_power_fraction": metrics[
            "pooled_distinguishable_power_fraction"
        ],
        "pooled_transmitted_power_fraction": metrics[
            "pooled_transmitted_power_fraction"
        ],
        "weighted_contrast_segment_drift": relative_segment_drift(
            metrics["weighted_contrast"]
        ),
    }


def _fmt(value: float) -> str:
    if value == 0.0:
        return "0"
    if abs(value) < 1e-3 or abs(value) >= 1e3:
        return f"{value:.3e}"
    return f"{value:.4f}"


def _dc_normalized_transfer(values: np.ndarray) -> np.ndarray:
    response = np.fft.rfft(np.asarray(values, dtype=float), axis=0)
    static = response[0]
    if np.any(np.abs(static) <= np.finfo(float).tiny):
        raise ValueError("mediator impulse response has zero finite-horizon DC gain")
    return response / static[None, :]


def make_figure(payload: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    plot = payload["plot_data"]
    omega = np.asarray(plot["angular_frequency"], dtype=float)
    persistent_power = np.asarray(plot["persistent_source_power"], dtype=float)
    one_step_power = np.asarray(plot["one_step_source_power"], dtype=float)
    tiny = np.finfo(float).tiny
    colors = plt.cm.viridis(np.linspace(0.08, 0.92, len(payload["rows"])))
    fig, axes = plt.subplots(2, 2, figsize=(11.2, 8.0), constrained_layout=True)

    for row, spectrum, color in zip(
        payload["rows"], persistent_power, colors, strict=True
    ):
        axes[0, 0].loglog(
            omega,
            np.maximum(spectrum, tiny),
            color=color,
            alpha=0.35,
            linewidth=0.9,
            label=f"source {row['source_seed']}",
        )
    axes[0, 0].loglog(
        omega,
        np.maximum(np.median(persistent_power, axis=0), tiny),
        color="#1f567d",
        linewidth=2.2,
        label="persistent median",
    )
    axes[0, 0].loglog(
        omega,
        np.maximum(np.median(one_step_power, axis=0), tiny),
        color="#c65333",
        linestyle="--",
        linewidth=1.8,
        label="one-step median",
    )
    axes[0, 0].set_xlabel("angular frequency [memory-time^-1]")
    axes[0, 0].set_ylabel("fraction of non-DC source power")
    axes[0, 0].set_title("Autonomous source spectra")
    axes[0, 0].legend(fontsize=7, ncol=2)

    transfer = plot["transfer_examples"]
    transfer_colors = {
        "relaxation_diffusion": "#2678a8",
        "telegraph": "#c65333",
    }
    for distance_name, linestyle in (("near", "-"), ("far", "--")):
        for model in ("relaxation_diffusion", "telegraph"):
            axes[0, 1].loglog(
                omega,
                np.maximum(
                    np.asarray(transfer[distance_name][model], dtype=float), tiny
                ),
                color=transfer_colors[model],
                linestyle=linestyle,
                label=f"{model.replace('_', '-')}, {distance_name}",
            )
    axes[0, 1].set_xlabel("angular frequency [memory-time^-1]")
    axes[0, 1].set_ylabel("absolute transfer / static gain")
    axes[0, 1].set_title("Frozen discrete transfer responses")
    axes[0, 1].legend(fontsize=7)

    for row, color in zip(payload["rows"], colors, strict=True):
        distances = [item["distance_ratio_pair_radius"] for item in row["distances"]]
        contrast = [
            item["persistent"]["pooled_weighted_contrast"]
            for item in row["distances"]
        ]
        distinguishable = [
            item["persistent"]["pooled_distinguishable_power_fraction"]
            for item in row["distances"]
        ]
        axes[1, 0].plot(distances, contrast, "o-", color=color, alpha=0.75)
        axes[1, 1].plot(
            distances,
            distinguishable,
            "o-",
            color=color,
            alpha=0.75,
            label=f"source {row['source_seed']}",
        )
    axes[1, 0].axhline(
        payload["thresholds"]["weighted_contrast_min"],
        color="#444444",
        linestyle="--",
        label="eligibility threshold",
    )
    axes[1, 0].set_xlabel("distance / pair radius")
    axes[1, 0].set_ylabel("source-weighted complex contrast")
    axes[1, 0].set_title("Persistent channel at every holdout distance")
    axes[1, 0].legend(fontsize=8)
    axes[1, 1].axhline(
        payload["thresholds"]["distinguishable_power_min"],
        color="#444444",
        linestyle="--",
        label="eligibility threshold",
    )
    axes[1, 1].set_xlabel("distance / pair radius")
    axes[1, 1].set_ylabel("distinguishable output-power fraction")
    axes[1, 1].set_ylim(-0.03, 1.03)
    axes[1, 1].set_title("Power carried in contrasting frequencies")
    axes[1, 1].legend(fontsize=7, ncol=2)
    for axis in axes.flat:
        axis.grid(alpha=0.25)
    fig.suptitle("Autonomous-source eligibility for two fixed mediator laws")
    fig.savefig(path, dpi=180)
    plt.close(fig)


def build_report(
    payload: dict[str, Any], report_path: Path, figure_path: Path
) -> str:
    decision = payload["decision"]
    lines = [
        "# Autonomous Oriented-Source Mediator Identifiability",
        "",
        f"Generated: `{payload['generated_utc']}`.",
        "",
        "## Question",
        "",
        "Do the six already frozen scalar knots, evolved autonomously with the "
        "previously introduced persistent orientation channel, carry stable "
        "non-DC power where the two fixed local mediator rules make different "
        "complex transfer predictions?",
        "",
        "This is an eligibility audit. It does not fit either mediator to the "
        "source spectrum and cannot select a physical field law.",
        "",
        "## Preregistered design",
        "",
        f"- source burn-in: `{_fmt(payload['burn_memory_times'])}` memory times;",
        f"- `{payload['segments']}` non-overlapping segments of "
        f"`{payload['segment_updates']}` updates each;",
        "- persistent carrier orientation is the inferential source; normalized "
        "one-step displacement is retained only as a diagnostic comparator;",
        "- exact finite-grid impulse responses are evaluated at all 18 inherited "
        "source-target distances;",
        "- each model and distance is independently normalized to unit finite-"
        "horizon static gain. No coupling amplitude is calibrated here;",
        f"- a frequency is contrasting when its relative complex transfer "
        f"separation is at least `{_fmt(payload['thresholds']['minimum_frequency_contrast'])}`;",
        f"- pair pass requires all three distances and every source/segment gate; "
        f"overall pass requires `{payload['minimum_passing_pairs']}` of "
        f"`{len(payload['rows'])}` independent sources.",
        "",
        "## Decision",
        "",
        f"Status: **{decision['status']}** "
        f"({decision['passing_pairs']}/{decision['pair_count']} source pairs).",
        "",
        decision["interpretation"],
        "",
        "Across the inherited distances, persistent/one-step weighted-transfer "
        f"contrast spans `{_fmt(decision['persistent_to_one_step_contrast_min'])}` "
        f"to `{_fmt(decision['persistent_to_one_step_contrast_max'])}` "
        f"(median `{_fmt(decision['persistent_to_one_step_contrast_median'])}`). "
        "This comparator is diagnostic and was not used as a pass gate.",
        "",
        f"![Mediator identifiability]({_relative_from(report_path, figure_path)})",
        "",
        "## Source results",
        "",
        "| source | orientation RMS | radius max change | shape-spectrum drift | min contrast | min distinguishable power | min transmitted power | max segment drift | pass |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in payload["rows"]:
        persistent = [item["persistent"] for item in row["distances"]]
        lines.append(
            f"| {row['source_seed']} | {_fmt(row['orientation_rms'])} | "
            f"{_fmt(row['source_radius_max_change'])} | "
            f"{_fmt(row['source_spectrum_max_drift'])} | "
            f"{_fmt(min(item['pooled_weighted_contrast'] for item in persistent))} | "
            f"{_fmt(min(item['pooled_distinguishable_power_fraction'] for item in persistent))} | "
            f"{_fmt(min(item['pooled_transmitted_power_fraction'] for item in persistent))} | "
            f"{_fmt(max(item['weighted_contrast_segment_drift'] for item in persistent))} | "
            f"{'pass' if row['pair_pass'] else 'fail'} |"
        )
    lines.extend(
        [
            "",
            "## Distance-resolved contrast",
            "",
            "| source | distance/R_pair | persistent contrast | persistent distinguishable | one-step contrast | one-step distinguishable |",
            "| ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in payload["rows"]:
        for item in row["distances"]:
            lines.append(
                f"| {row['source_seed']} | "
                f"{_fmt(item['distance_ratio_pair_radius'])} | "
                f"{_fmt(item['persistent']['pooled_weighted_contrast'])} | "
                f"{_fmt(item['persistent']['pooled_distinguishable_power_fraction'])} | "
                f"{_fmt(item['one_step']['pooled_weighted_contrast'])} | "
                f"{_fmt(item['one_step']['pooled_distinguishable_power_fraction'])} |"
            )
    lines.extend(
        [
            "",
            "## Interpretation boundary",
            "",
            "A pass means only that the autonomous source is spectrally capable "
            "of exposing different predictions from the two already inserted "
            "mediator laws. A fail means that a further constructive source-target "
            "run cannot distinguish them under this source channel and should be "
            "stopped rather than rescued by parameter tuning.",
            "",
            "The persistent orientation is itself an added low-pass state; it is "
            "not derived from scalar memory. The one-step comparator is therefore "
            "diagnostic, not a null that can validate the oriented channel. No "
            "reciprocity, conservation law, photon, spin, charge, particle, QFT, "
            "Lorentz, or finite-signal-speed claim follows.",
            "",
            "## Three-dimensional selection",
            "",
            "Fields do not select three dimensions merely by being introduced: "
            "both tested laws can be written in any supplied dimension, while this "
            "audit uses the same one-dimensional relational transport axis as the "
            "architecture gate. A later selection test must freeze one law and one "
            "absolute dimensionless parameter set across ambient dimensions, then "
            "show that the external response or slow-mode rank converges to three "
            "and that extra directions are dynamically suppressed. A 3D field grid "
            "would assume that result.",
            "",
            "## Reproducibility",
            "",
            f"- mediator summary: `{payload['mediator_summary']}`",
            f"- source reference: `{payload['source_reference']}`",
            f"- analysis revision: `{payload['git_revision']}`",
            f"- worktree at start: `{payload['git_status_at_start'] or 'clean'}`",
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
    if args.segments < 2 or args.segment_updates < 16:
        raise ValueError("at least two segments and 16 updates per segment are required")
    if args.burn_memory_times < 0.0 or args.plot_omega_max <= 0.0:
        raise ValueError("burn time must be non-negative and plot limit positive")
    if not 1 <= args.minimum_passing_pairs <= 6:
        raise ValueError("minimum-passing-pairs must lie in [1, 6]")

    thresholds = {
        "minimum_frequency_contrast": float(args.minimum_frequency_contrast),
        "weighted_contrast_min": float(args.weighted_contrast_min),
        "distinguishable_power_min": float(args.distinguishable_power_min),
        "transmitted_power_min": float(args.transmitted_power_min),
        "segment_drift_max": float(args.segment_drift_max),
        "orientation_rms_min": float(args.orientation_rms_min),
        "source_radius_max_change": float(args.source_radius_max_change),
        "source_spectrum_max_drift": float(args.source_spectrum_max_drift),
    }
    if any(not np.isfinite(value) or value < 0.0 for value in thresholds.values()):
        raise ValueError("all thresholds must be finite and non-negative")
    if thresholds["minimum_frequency_contrast"] <= 0.0:
        raise ValueError("minimum frequency contrast must be positive")

    mediator_path = _resolve(args.mediator_summary)
    mediator_summary = json.loads(mediator_path.read_text(encoding="utf-8"))
    if (
        mediator_summary.get("decision", {}).get("selected_next_step")
        != "autonomous_source_spectrum_identifiability_audit"
    ):
        raise ValueError("mediator summary does not authorize this audit")
    reference_path = _resolve(Path(mediator_summary["reference_summary"]))
    reference = json.loads(reference_path.read_text(encoding="utf-8"))
    reference_rows = reference["rows"]
    pair_templates = mediator_summary["models"]["relaxation_diffusion"][
        "pair_rows"
    ]
    if len(reference_rows) != 6 or len(pair_templates) != len(reference_rows):
        raise ValueError("exactly six inherited independent source pairs are required")

    source_cases = []
    distance_ratios = np.asarray(mediator_summary["distance_ratios"], dtype=float)
    if distance_ratios.shape != (3,):
        raise ValueError("the inherited mediator gate must contain three distances")
    for reference_row, template in zip(
        reference_rows, pair_templates, strict=True
    ):
        if (
            int(reference_row["source_seed"]) != int(template["source_seed"])
            or reference_row["source_case_path"] != template["source_case_path"]
        ):
            raise ValueError("mediator and source-reference pair ordering differ")
        distances = np.asarray(
            [item["distance_r0"] for item in template["distance_rows"]],
            dtype=float,
        )
        if distances.shape != distance_ratios.shape:
            raise ValueError("a pair is missing inherited mediator distances")
        source_cases.append(
            {
                "reference": reference_row,
                "template": template,
                "case": _load_case(
                    Path(reference_row["source_case_path"]),
                    reference_row["source_case_sha256"],
                ),
                "distance_r0": distances,
            }
        )

    first_config = source_cases[0]["case"]["config"]
    if any(item["case"]["config"] != first_config for item in source_cases):
        raise ValueError("all autonomous sources must share one simulation config")
    lambda_vector = float(mediator_summary["lambda_vector"])
    if not np.isclose(lambda_vector, first_config.alpha, rtol=0.0, atol=1e-15):
        raise ValueError("scalar and oriented memory clocks must match")
    vector_mass = float(reference["vector_mass"])
    orientation_relaxation = float(reference["orientation_relaxation"])
    burn_updates = int(round(args.burn_memory_times / lambda_vector))
    if not np.isclose(burn_updates * lambda_vector, args.burn_memory_times):
        raise ValueError("burn-memory-times must resolve to whole source updates")
    analysis_updates = int(args.segments * args.segment_updates)
    total_updates = burn_updates + analysis_updates
    sample_steps = np.arange(total_updates + 1, dtype=int)

    grid = LocalMediatorGrid(**mediator_summary["primary_grid"])
    if not np.isclose(grid.time_step, lambda_vector, rtol=0.0, atol=1e-15):
        raise ValueError("source and mediator frequency grids must share one time step")
    diffusion = RelaxationDiffusionMediator(
        **mediator_summary["models"]["relaxation_diffusion"]["parameters"]
    )
    telegraph = TelegraphMediator(
        **mediator_summary["models"]["telegraph"]["parameters"]
    )
    calibration_radius = float(mediator_summary["calibration_radius"])
    readout_positions = np.concatenate(
        [item["distance_r0"] * calibration_radius for item in source_cases]
    )
    if float(np.max(readout_positions)) >= grid.coordinates[-1]:
        raise ValueError("inherited mediator grid does not contain every readout")
    impulse = np.zeros(args.segment_updates, dtype=float)
    impulse[0] = 1.0
    diffusion_trace = simulate_relaxation_diffusion_mediator(
        grid,
        diffusion,
        source_values=impulse,
        readout_positions=readout_positions,
    )
    telegraph_trace = simulate_telegraph_mediator(
        grid,
        telegraph,
        source_values=impulse,
        readout_positions=readout_positions,
    )
    diffusion_transfer = _dc_normalized_transfer(diffusion_trace.values[1:])
    telegraph_transfer = _dc_normalized_transfer(telegraph_trace.values[1:])

    rows: list[dict[str, Any]] = []
    persistent_powers: list[np.ndarray] = []
    one_step_powers: list[np.ndarray] = []
    angular_frequency: np.ndarray | None = None
    for pair_index, item in enumerate(source_cases):
        case = item["case"]
        source_state = initialize_oriented_memory_state(
            case["state"],
            lambda_vector=lambda_vector,
            vector_mass=vector_mass,
            orientation_relaxation=orientation_relaxation,
        )
        rng = np.random.default_rng(
            int(args.noise_seed + 100_003 * int(case["seed"]))
        )
        trace = autonomous_oriented_source_trace(
            source_state,
            first_config,
            source_noise=rng.normal(size=(total_updates, first_config.dim)),
            sample_steps=sample_steps,
        )
        persistent_values = trace.carrier_orientations[burn_updates + 1 :]
        displacement = np.diff(trace.positions, axis=0)[burn_updates:]
        displacement_norm = np.linalg.norm(displacement, axis=1, keepdims=True)
        one_step_values = np.divide(
            displacement,
            displacement_norm,
            out=np.zeros_like(displacement),
            where=displacement_norm > 0.0,
        )
        expected_shape = (analysis_updates, first_config.dim)
        if persistent_values.shape != expected_shape or one_step_values.shape != expected_shape:
            raise RuntimeError("source trace slicing produced an unexpected shape")
        persistent_segments = persistent_values.reshape(
            args.segments, args.segment_updates, first_config.dim
        )
        one_step_segments = one_step_values.reshape(
            args.segments, args.segment_updates, first_config.dim
        )
        omega, persistent_power = vector_segment_power(
            persistent_segments, time_step=lambda_vector
        )
        one_step_omega, one_step_power = vector_segment_power(
            one_step_segments, time_step=lambda_vector
        )
        if angular_frequency is None:
            angular_frequency = omega
        elif not np.array_equal(angular_frequency, omega):
            raise RuntimeError("source frequency grids differ")
        if not np.array_equal(omega, one_step_omega):
            raise RuntimeError("persistent and one-step frequency grids differ")
        persistent_powers.append(persistent_power)
        one_step_powers.append(one_step_power)

        spectra = normalized_shape_spectra(trace.shape_tensors)
        source_spectrum_drift = float(
            np.max(np.linalg.norm(spectra - spectra[0], axis=1))
        )
        source_radius_change = float(np.max(np.abs(trace.radius_ratios - 1.0)))
        orientation_rms = float(
            np.sqrt(np.mean(np.sum(np.square(persistent_values), axis=1)))
        )
        distance_rows = []
        for distance_index, (ratio, distance_r0) in enumerate(
            zip(distance_ratios, item["distance_r0"], strict=True)
        ):
            transfer_index = pair_index * len(distance_ratios) + distance_index
            persistent_metrics = transfer_identifiability_metrics(
                persistent_power,
                diffusion_transfer[:, transfer_index],
                telegraph_transfer[:, transfer_index],
                minimum_frequency_contrast=thresholds[
                    "minimum_frequency_contrast"
                ],
            )
            one_step_metrics = transfer_identifiability_metrics(
                one_step_power,
                diffusion_transfer[:, transfer_index],
                telegraph_transfer[:, transfer_index],
                minimum_frequency_contrast=thresholds[
                    "minimum_frequency_contrast"
                ],
            )
            persistent_compact = _compact_identifiability(persistent_metrics)
            one_step_compact = _compact_identifiability(one_step_metrics)
            distance_rows.append(
                {
                    "distance_ratio_pair_radius": float(ratio),
                    "distance_r0": float(distance_r0),
                    "physical_distance": float(readout_positions[transfer_index]),
                    "persistent": persistent_compact,
                    "one_step": one_step_compact,
                    "persistent_to_one_step_contrast_ratio": float(
                        persistent_compact["pooled_weighted_contrast"]
                        / max(
                            one_step_compact["pooled_weighted_contrast"],
                            np.finfo(float).tiny,
                        )
                    ),
                }
            )
        gates = pair_gate(
            distance_rows,
            orientation_rms=orientation_rms,
            radius_change=source_radius_change,
            spectrum_drift=source_spectrum_drift,
            thresholds=thresholds,
        )
        rows.append(
            {
                "pair_index": pair_index,
                "target_seed": int(item["reference"]["target_seed"]),
                "source_seed": int(case["seed"]),
                "source_case_path": _relative(case["path"]),
                "source_case_sha256": case["sha256"],
                "orientation_rms": orientation_rms,
                "source_radius_max_change": source_radius_change,
                "source_spectrum_max_drift": source_spectrum_drift,
                "distances": distance_rows,
                "gates": gates,
                "pair_pass": bool(all(gates.values())),
            }
        )

    assert angular_frequency is not None
    passing_pairs = sum(bool(row["pair_pass"]) for row in rows)
    contrast_ratios = np.asarray(
        [
            item["persistent_to_one_step_contrast_ratio"]
            for row in rows
            for item in row["distances"]
        ],
        dtype=float,
    )
    comparator_summary = {
        "persistent_to_one_step_contrast_min": float(np.min(contrast_ratios)),
        "persistent_to_one_step_contrast_median": float(
            np.median(contrast_ratios)
        ),
        "persistent_to_one_step_contrast_max": float(np.max(contrast_ratios)),
    }
    if passing_pairs >= args.minimum_passing_pairs:
        decision = {
            "status": "source_eligible_mechanism_still_underdetermined",
            "passing_pairs": passing_pairs,
            "pair_count": len(rows),
            "selected_next_step": "dynamic_common_source_prediction_gate",
            **comparator_summary,
            "interpretation": (
                "The autonomous persistent source carries stable power in frequency "
                "bands where the two fixed mediator laws differ. A dynamic holdout "
                "prediction can now be discriminating, but this audit does not select "
                "which inserted law is physical. Comparable one-step contrast means "
                "the pass does not specifically support persistent vector memory."
            ),
        }
    else:
        decision = {
            "status": "source_not_identifiable",
            "passing_pairs": passing_pairs,
            "pair_count": len(rows),
            "selected_next_step": "stop_constructive_mediator_runs",
            **comparator_summary,
            "interpretation": (
                "The autonomous persistent source does not satisfy the preregistered "
                "spectral eligibility gate. A dynamic mediator run would not "
                "distinguish the two laws without changing the source or thresholds."
            ),
        }

    plot_mask = (angular_frequency > 0.0) & (
        angular_frequency <= float(args.plot_omega_max)
    )
    if not np.any(plot_mask):
        raise ValueError("plot-omega-max excludes every non-DC frequency")

    def normalized_pooled_plot(power: np.ndarray) -> np.ndarray:
        pooled = np.mean(power, axis=0)
        total = float(np.sum(pooled[1:]))
        if total <= 0.0:
            raise ValueError("source spectrum has no non-DC power")
        return pooled[plot_mask] / total

    report_path = _resolve(args.report)
    summary_path = _resolve(args.summary_json)
    figure_path = _resolve(args.figure)
    payload = {
        "schema": "oriented-source-mediator-identifiability",
        "schema_version": 1,
        "generated_utc": datetime.now(UTC).isoformat(),
        "git_revision": _git_output(["rev-parse", "HEAD"]),
        "git_status_at_start": git_status,
        "command": ["python", *os.sys.argv],
        "mediator_summary": _relative(mediator_path),
        "source_reference": _relative(reference_path),
        "reference_git_revision": reference.get("git_revision", "unavailable"),
        "formation_config": asdict(first_config),
        "lambda_vector": lambda_vector,
        "vector_mass": vector_mass,
        "orientation_relaxation": orientation_relaxation,
        "burn_memory_times": float(args.burn_memory_times),
        "burn_updates": burn_updates,
        "segments": int(args.segments),
        "segment_updates": int(args.segment_updates),
        "analysis_updates": analysis_updates,
        "total_updates": total_updates,
        "noise_seed_rule": "noise_seed + 100003 * source_seed",
        "noise_seed": int(args.noise_seed),
        "grid": asdict(grid),
        "mediator_parameters": {
            "relaxation_diffusion": asdict(diffusion),
            "telegraph": asdict(telegraph),
        },
        "transfer_normalization": "unit finite-horizon DC gain per model-distance",
        "distance_ratios": distance_ratios,
        "thresholds": thresholds,
        "minimum_passing_pairs": int(args.minimum_passing_pairs),
        "rows": rows,
        "decision": decision,
        "plot_data": {
            "angular_frequency": angular_frequency[plot_mask],
            "persistent_source_power": [
                normalized_pooled_plot(power) for power in persistent_powers
            ],
            "one_step_source_power": [
                normalized_pooled_plot(power) for power in one_step_powers
            ],
            "transfer_examples": {
                "near": {
                    "relaxation_diffusion": np.abs(
                        diffusion_transfer[plot_mask, 0]
                    ),
                    "telegraph": np.abs(telegraph_transfer[plot_mask, 0]),
                },
                "far": {
                    "relaxation_diffusion": np.abs(
                        diffusion_transfer[plot_mask, 2]
                    ),
                    "telegraph": np.abs(telegraph_transfer[plot_mask, 2]),
                },
            },
        },
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
