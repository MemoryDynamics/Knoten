"""Dynamic holdout for two fixed local mediator rules under common sources."""

from __future__ import annotations

import argparse
from dataclasses import asdict
from datetime import UTC, datetime
import hashlib
import json
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
    FiniteMemoryState,
    LocalMediatorGrid,
    RelaxationDiffusionMediator,
    SimulationConfig,
    TelegraphMediator,
    autonomous_oriented_source_trace,
    dynamic_external_field_response_metrics,
    initialize_oriented_memory_state,
    normalized_shape_spectra,
    paired_external_field_response,
    simulate_vector_relaxation_diffusion_mediator,
    simulate_vector_telegraph_mediator,
)


def _repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("repository root not found")


ROOT = _repo_root()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Dynamic common-source holdout for fixed local mediators."
    )
    parser.add_argument(
        "--identifiability-summary",
        type=Path,
        default=Path(
            "reports/response/oriented/oriented_source_mediator_identifiability_2026-07-28.json"
        ),
    )
    parser.add_argument("--burn-memory-times", type=float, default=20.0)
    parser.add_argument("--analysis-memory-times", type=float, default=50.0)
    parser.add_argument("--sample-every", type=int, default=10)
    parser.add_argument("--response-rms-min-r", type=float, default=1e-4)
    parser.add_argument("--response-rms-max-r", type=float, default=0.1)
    parser.add_argument("--odd-symmetry-max", type=float, default=0.1)
    parser.add_argument("--flip-rms-min", type=float, default=0.9)
    parser.add_argument("--flip-rms-max", type=float, default=1.1)
    parser.add_argument("--target-radius-max-change", type=float, default=0.1)
    parser.add_argument("--target-shape-max-change", type=float, default=0.1)
    parser.add_argument("--source-radius-max-change", type=float, default=0.5)
    parser.add_argument("--source-spectrum-max-drift", type=float, default=0.25)
    parser.add_argument("--response-monotonic-tolerance", type=float, default=0.25)
    parser.add_argument("--far-near-max-ratio", type=float, default=0.5)
    parser.add_argument("--model-trace-separation-min", type=float, default=0.25)
    parser.add_argument("--minimum-passing-pairs", type=int, default=5)
    parser.add_argument("--target-noise-seed", type=int, default=20_260_728)
    parser.add_argument("--allow-dirty", action="store_true")
    parser.add_argument(
        "--report",
        type=Path,
        default=Path(
            "reports/response/oriented/dynamic_common_source_mediator_gate_2026-07-28.md"
        ),
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=Path(
            "reports/response/oriented/dynamic_common_source_mediator_gate_2026-07-28.json"
        ),
    )
    parser.add_argument(
        "--figure",
        type=Path,
        default=Path(
            "figures/draft/response/dynamic_common_source_mediator_gate_2026-07-28.png"
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


def _sample_steps(n_steps: int, sample_every: int, required_step: int) -> np.ndarray:
    if n_steps < 1 or sample_every < 1 or not 0 <= required_step <= n_steps:
        raise ValueError("invalid sample-step request")
    return np.unique(
        np.concatenate(
            (np.arange(0, n_steps + 1, sample_every), [required_step, n_steps])
        )
    )


def relative_trace_separation(first: np.ndarray, second: np.ndarray) -> float:
    """Return RMS trace difference relative to their quadratic mean signal."""

    left = np.asarray(first, dtype=float)
    right = np.asarray(second, dtype=float)
    if left.shape != right.shape or left.ndim != 2 or not np.isfinite(left).all():
        raise ValueError("response traces must be matching finite matrices")
    if not np.isfinite(right).all():
        raise ValueError("response traces must be matching finite matrices")

    def vector_rms(values: np.ndarray) -> float:
        return float(np.sqrt(np.mean(np.sum(np.square(values), axis=1))))

    denominator = np.sqrt(0.5 * (vector_rms(left) ** 2 + vector_rms(right) ** 2))
    if denominator <= np.finfo(float).tiny:
        return 0.0
    return vector_rms(left - right) / denominator


def response_gates(
    metrics: dict[str, Any], thresholds: dict[str, float]
) -> dict[str, bool]:
    """Apply fixed response, oddness, and shape-envelope criteria."""

    return {
        "response_window": bool(
            thresholds["response_rms_min_r"]
            <= metrics["active_response_rms_r"]
            <= thresholds["response_rms_max_r"]
        ),
        "sign_flip": bool(
            metrics["odd_symmetry_relative_rms"] <= thresholds["odd_symmetry_max"]
            and thresholds["flip_rms_min"]
            <= metrics["flip_response_rms_ratio"]
            <= thresholds["flip_rms_max"]
        ),
        "shape_bounded": bool(
            metrics["target_radius_max_change"]
            <= thresholds["target_radius_max_change"]
            and metrics["target_shape_max_change"]
            <= thresholds["target_shape_max_change"]
        ),
    }


def attenuation_gates(
    responses: np.ndarray, *, tolerance: float, far_near_max_ratio: float
) -> dict[str, bool | float]:
    """Require a non-growing RMS response and a bounded far/near ratio."""

    values = np.asarray(responses, dtype=float)
    if values.ndim != 1 or values.size < 2 or np.any(values <= 0.0):
        raise ValueError("responses must be a positive distance sequence")
    monotone = bool(np.all(values[1:] <= values[:-1] * (1.0 + float(tolerance))))
    ratio = float(values[-1] / values[0])
    return {
        "response_monotone": monotone,
        "far_near_ratio": ratio,
        "far_near_bounded": bool(ratio <= far_near_max_ratio),
    }


def _compact_metrics(metrics: dict[str, Any]) -> dict[str, Any]:
    return {
        key: value
        for key, value in metrics.items()
        if key not in {"analysis_sample_steps", "trace_active_response_vector_r"}
    }


def _fmt(value: float) -> str:
    if value == 0.0:
        return "0"
    if abs(value) < 1e-3 or abs(value) >= 1e3:
        return f"{value:.3e}"
    return f"{value:.4f}"


def make_figure(payload: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    plot = payload["plot_data"]
    colors = {"relaxation_diffusion": "#2678a8", "telegraph": "#c65333"}
    labels = {
        "relaxation_diffusion": "relaxation-diffusion",
        "telegraph": "damped telegraph",
    }
    tiny = np.finfo(float).tiny
    fig, axes = plt.subplots(2, 2, figsize=(11.2, 8.0), constrained_layout=True)

    source_times = np.asarray(plot["source_times_memory"], dtype=float)
    positive_time = source_times > 0.0
    axes[0, 0].semilogy(
        source_times[positive_time],
        np.maximum(np.asarray(plot["persistent_source_norm"])[positive_time], tiny),
        color="#1f567d",
        label="persistent carrier",
    )
    axes[0, 0].semilogy(
        source_times[positive_time],
        np.maximum(np.asarray(plot["one_step_source_norm"])[positive_time], tiny),
        color="#c65333",
        linestyle="--",
        label="unit one-step direction",
    )
    axes[0, 0].axvline(payload["burn_memory_times"], color="#444444", linestyle=":")
    axes[0, 0].set_xlabel("memory times")
    axes[0, 0].set_ylabel("source-vector norm")
    axes[0, 0].set_title("Calibration-pair autonomous input")
    axes[0, 0].legend(fontsize=8)

    response_times = np.asarray(plot["target_times_memory"], dtype=float)
    for model in ("relaxation_diffusion", "telegraph"):
        axes[0, 1].semilogy(
            response_times,
            np.maximum(plot["target_response"][model]["persistent"], tiny),
            color=colors[model],
            label=f"{labels[model]}, persistent",
        )
        axes[0, 1].semilogy(
            response_times,
            np.maximum(plot["target_response"][model]["one_step"], tiny),
            color=colors[model],
            linestyle="--",
            alpha=0.75,
            label=f"{labels[model]}, one-step",
        )
    axes[0, 1].set_xlabel("analysis memory times")
    axes[0, 1].set_ylabel("paired target response / R_target")
    axes[0, 1].set_title("Calibration pair, nearest inherited distance")
    axes[0, 1].legend(fontsize=7)

    distance_ratios = np.asarray(payload["distance_ratios"], dtype=float)
    for model in ("relaxation_diffusion", "telegraph"):
        by_distance = []
        for distance_index in range(distance_ratios.size):
            values = [
                row["models"][model]["distances"][distance_index]["persistent"][
                    "active_response_rms_r"
                ]
                for row in payload["rows"]
            ]
            by_distance.append(values)
            axes[1, 0].scatter(
                np.full(len(values), distance_ratios[distance_index]),
                values,
                color=colors[model],
                alpha=0.45,
                s=22,
            )
        axes[1, 0].plot(
            distance_ratios,
            [float(np.median(values)) for values in by_distance],
            "o-",
            color=colors[model],
            label=labels[model],
        )
    axes[1, 0].axhline(
        payload["thresholds"]["response_rms_min_r"],
        color="#444444",
        linestyle=":",
        label="response minimum",
    )
    axes[1, 0].axhline(
        payload["thresholds"]["response_rms_max_r"],
        color="#444444",
        linestyle="--",
        label="linear-geometry maximum",
    )
    axes[1, 0].set_yscale("log")
    axes[1, 0].set_xlabel("distance / pair radius")
    axes[1, 0].set_ylabel("persistent target response RMS / R_target")
    axes[1, 0].set_title("Fixed pulse-calibrated coupling")
    axes[1, 0].legend(fontsize=7)

    for row in payload["rows"]:
        axes[1, 1].plot(
            distance_ratios,
            [item["persistent"] for item in row["model_separation"]],
            "o-",
            color="#2678a8",
            alpha=0.35,
        )
        axes[1, 1].plot(
            distance_ratios,
            [item["one_step"] for item in row["model_separation"]],
            "s--",
            color="#c65333",
            alpha=0.25,
        )
    axes[1, 1].axhline(
        payload["thresholds"]["model_trace_separation_min"],
        color="#444444",
        linestyle=":",
        label="separation threshold",
    )
    axes[1, 1].set_xlabel("distance / pair radius")
    axes[1, 1].set_ylabel("relative response-trace separation")
    axes[1, 1].set_title("Persistent (solid) and one-step (dashed)")
    axes[1, 1].legend(fontsize=8)
    for axis in axes.flat:
        axis.grid(alpha=0.25)
    fig.suptitle("Dynamic common-source holdout for fixed mediator laws")
    fig.savefig(path, dpi=180)
    plt.close(fig)


def build_report(payload: dict[str, Any], report_path: Path, figure_path: Path) -> str:
    decision = payload["decision"]
    lines = [
        "# Dynamic Common-Source Mediator Gate",
        "",
        f"Generated: `{payload['generated_utc']}`.",
        "",
        "## Question",
        "",
        "When the same autonomous source waveform drives the two already fixed "
        "local mediator laws under their pulse-calibrated couplings, do they "
        "produce measurable, odd, shape-bounded and dynamically distinct target "
        "responses across the inherited source-target holdouts?",
        "",
        "## Preregistered design",
        "",
        f"- common settling interval `{_fmt(payload['burn_memory_times'])}` and "
        f"analysis interval `{_fmt(payload['analysis_memory_times'])}` memory times;",
        "- six checksum-validated cyclic source-target pairs and the inherited "
        "distance ladder `2.5, 5, 10 R_pair`;",
        "- mediator grids, laws, length scale and one pulse-calibrated coupling per "
        "law are inherited without retuning;",
        "- persistent carrier and unit one-step source drive independent ambient "
        "components of the same one-dimensional relational mediator;",
        "- active, global-sign-flip and exact channel-off target branches share "
        "one future-noise path;",
        f"- persistent RMS response must lie in "
        f"`[{_fmt(payload['thresholds']['response_rms_min_r'])}, "
        f"{_fmt(payload['thresholds']['response_rms_max_r'])}] R_target`, odd "
        f"residual at most `{_fmt(payload['thresholds']['odd_symmetry_max'])}`, "
        "and target radius/shape changes at most `0.1`;",
        f"- far/near RMS response at most "
        f"`{_fmt(payload['thresholds']['far_near_max_ratio'])}` and relative "
        f"cross-model response-trace separation at least "
        f"`{_fmt(payload['thresholds']['model_trace_separation_min'])}`;",
        f"- model and separation pass require at least "
        f"`{payload['minimum_passing_pairs']}/{len(payload['rows'])}` pairs.",
        "",
        "The one-step arm is reported at the same coupling without amplitude "
        "matching. It is diagnostic and cannot rescue or invalidate the primary "
        "persistent arm by scale alone.",
        "",
        "## Decision",
        "",
        f"Status: **{decision['status']}**.",
        "",
        decision["interpretation"],
        "",
        f"![Dynamic common-source gate]({_relative_from(report_path, figure_path)})",
        "",
        "## Model summary",
        "",
        "| model | passing pairs | response RMS range | max odd residual | max radius change | max shape change |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for model in ("relaxation_diffusion", "telegraph"):
        item = payload["model_summary"][model]
        lines.append(
            f"| {model.replace('_', '-')} | {item['passing_pairs']}/{item['pair_count']} | "
            f"{_fmt(item['response_rms_min'])}..{_fmt(item['response_rms_max'])} | "
            f"{_fmt(item['odd_residual_max'])} | "
            f"{_fmt(item['target_radius_change_max'])} | "
            f"{_fmt(item['target_shape_change_max'])} |"
        )
    lines.append("")
    if all(decision.get("model_pass_status", {}).values()):
        lines.extend(
            [
                "Both model rows pass the preregistered response, sign-flip, "
                "source/target shape and attenuation gates. Any overall failure "
                "therefore occurs at the separate cross-model discrimination gate.",
                "",
            ]
        )
    lines.extend(
        [
            "## Separation by distance",
            "",
            "| distance/R_pair | passing pairs | minimum | median | maximum |",
            "| ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for item in payload["separation_summary"]:
        lines.append(
            f"| {_fmt(item['distance_ratio_pair_radius'])} | "
            f"{item['passing_pairs']}/{item['pair_count']} | "
            f"{_fmt(item['minimum'])} | {_fmt(item['median'])} | "
            f"{_fmt(item['maximum'])} |"
        )
    lines.extend(
        [
            "",
            "## Pair results",
            "",
            "| target<-source | source shape | diffusion | telegraph | min persistent separation | min one-step separation | overall |",
            "| --- | --- | --- | --- | ---: | ---: | --- |",
        ]
    )
    for row in payload["rows"]:
        lines.append(
            f"| {row['target_seed']}<-{row['source_seed']} | "
            f"{'pass' if all(row['source_gates'].values()) else 'fail'} | "
            f"{'pass' if row['models']['relaxation_diffusion']['pair_pass'] else 'fail'} | "
            f"{'pass' if row['models']['telegraph']['pair_pass'] else 'fail'} | "
            f"{_fmt(min(item['persistent'] for item in row['model_separation']))} | "
            f"{_fmt(min(item['one_step'] for item in row['model_separation']))} | "
            f"{'pass' if row['pair_pass'] else 'fail'} |"
        )
    lines.extend(
        [
            "",
            "## Source-drive scale",
            "",
            "| target<-source | persistent RMS | unit one-step RMS |",
            "| --- | ---: | ---: |",
        ]
    )
    for row in payload["rows"]:
        lines.append(
            f"| {row['target_seed']}<-{row['source_seed']} | "
            f"{_fmt(row['source_input_rms']['persistent'])} | "
            f"{_fmt(row['source_input_rms']['one_step'])} |"
        )
    lines.extend(
        [
            "",
            "## Distance-resolved persistent response",
            "",
            "| target<-source | model | distance/R_pair | persistent RMS/R | one-step RMS/R | odd residual | radius change | shape change |",
            "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in payload["rows"]:
        for model in ("relaxation_diffusion", "telegraph"):
            for item in row["models"][model]["distances"]:
                persistent = item["persistent"]
                lines.append(
                    f"| {row['target_seed']}<-{row['source_seed']} | "
                    f"{model.replace('_', '-')} | "
                    f"{_fmt(item['distance_ratio_pair_radius'])} | "
                    f"{_fmt(persistent['active_response_rms_r'])} | "
                    f"{_fmt(item['one_step']['active_response_rms_r'])} | "
                    f"{_fmt(persistent['odd_symmetry_relative_rms'])} | "
                    f"{_fmt(persistent['target_radius_max_change'])} | "
                    f"{_fmt(persistent['target_shape_max_change'])} |"
                )
    lines.extend(
        [
            "",
            "## Interpretation boundary",
            "",
            "This gate can reject a mediator architecture if its inherited "
            "coupling produces no measurable response, violates oddness or the "
            "knot envelope, fails attenuation, or remains dynamically "
            "indistinguishable from the competing architecture. It still has no "
            "independent observed target trajectory. Therefore survival or failure "
            "is an architecture result, not discovery of a physical field law.",
            "",
            "The mediator remains a one-dimensional relational axis carrying "
            "vectors in the supplied `d=3` ambient state. This neither selects "
            "three dimensions nor tests suppression of extra ambient directions. "
            "No reciprocity, conservation law, photon, spin, charge, QFT, Lorentz, "
            "or finite-signal-speed claim follows.",
            "",
            "## Reproducibility",
            "",
            f"- identifiability summary: `{payload['identifiability_summary']}`",
            f"- mediator summary: `{payload['mediator_summary']}`",
            f"- source reference: `{payload['source_reference']}`",
            f"- analysis revision: `{payload['git_revision']}`",
            f"- worktree at start: `{payload['git_status_at_start'] or 'clean'}`",
            f"- runtime: `{_fmt(payload['runtime_seconds'])} s`",
            f"- command: `{' '.join(payload['command'])}`",
            "",
        ]
    )
    return chr(10).join(lines)


def main() -> None:
    started = time.perf_counter()
    args = parse_args()
    git_status = _git_output(["status", "--short"])
    if git_status not in ("", "unavailable") and not args.allow_dirty:
        raise RuntimeError("refusing to run from a dirty worktree; use --allow-dirty")
    if min(args.burn_memory_times, args.analysis_memory_times) <= 0.0:
        raise ValueError("burn and analysis intervals must be positive")
    if args.sample_every < 1 or not 1 <= args.minimum_passing_pairs <= 6:
        raise ValueError("invalid sampling or passing-pair request")

    thresholds = {
        "response_rms_min_r": float(args.response_rms_min_r),
        "response_rms_max_r": float(args.response_rms_max_r),
        "odd_symmetry_max": float(args.odd_symmetry_max),
        "flip_rms_min": float(args.flip_rms_min),
        "flip_rms_max": float(args.flip_rms_max),
        "target_radius_max_change": float(args.target_radius_max_change),
        "target_shape_max_change": float(args.target_shape_max_change),
        "source_radius_max_change": float(args.source_radius_max_change),
        "source_spectrum_max_drift": float(args.source_spectrum_max_drift),
        "response_monotonic_tolerance": float(args.response_monotonic_tolerance),
        "far_near_max_ratio": float(args.far_near_max_ratio),
        "model_trace_separation_min": float(args.model_trace_separation_min),
    }
    if any(not np.isfinite(value) or value < 0.0 for value in thresholds.values()):
        raise ValueError("thresholds must be finite and non-negative")
    if not (0.0 < thresholds["response_rms_min_r"] < thresholds["response_rms_max_r"]):
        raise ValueError("response RMS bounds must be positive and ordered")

    ident_path = _resolve(args.identifiability_summary)
    identifiability = json.loads(ident_path.read_text(encoding="utf-8"))
    if (
        identifiability.get("decision", {}).get("selected_next_step")
        != "dynamic_common_source_prediction_gate"
    ):
        raise ValueError("identifiability summary does not authorize this gate")
    mediator_path = _resolve(Path(identifiability["mediator_summary"]))
    mediator_summary = json.loads(mediator_path.read_text(encoding="utf-8"))
    reference_path = _resolve(Path(identifiability["source_reference"]))
    reference = json.loads(reference_path.read_text(encoding="utf-8"))
    reference_rows = reference["rows"]
    pair_templates = mediator_summary["models"]["relaxation_diffusion"]["pair_rows"]
    if len(reference_rows) != 6 or len(pair_templates) != 6:
        raise ValueError("exactly six inherited source-target pairs are required")

    cases: dict[tuple[int, str], dict[str, Any]] = {}
    pair_cases = []
    for reference_row, template in zip(reference_rows, pair_templates, strict=True):
        target_key = (
            int(reference_row["target_seed"]),
            reference_row["target_case_sha256"],
        )
        source_key = (
            int(reference_row["source_seed"]),
            reference_row["source_case_sha256"],
        )
        if target_key not in cases:
            cases[target_key] = _load_case(
                Path(reference_row["target_case_path"]),
                reference_row["target_case_sha256"],
            )
        if source_key not in cases:
            cases[source_key] = _load_case(
                Path(reference_row["source_case_path"]),
                reference_row["source_case_sha256"],
            )
        if (
            int(template["target_seed"]) != target_key[0]
            or int(template["source_seed"]) != source_key[0]
        ):
            raise ValueError("mediator and source-reference pair ordering differ")
        distance_r0 = np.asarray(
            [item["distance_r0"] for item in template["distance_rows"]],
            dtype=float,
        )
        pair_cases.append(
            {
                "reference": reference_row,
                "template": template,
                "target": cases[target_key],
                "source": cases[source_key],
                "distance_r0": distance_r0,
            }
        )

    first_config = pair_cases[0]["target"]["config"]
    if any(
        item["target"]["config"] != first_config
        or item["source"]["config"] != first_config
        for item in pair_cases
    ):
        raise ValueError("all inherited source-target states must share one config")
    lambda_vector = float(identifiability["lambda_vector"])
    if not np.isclose(lambda_vector, first_config.alpha, rtol=0.0, atol=1e-15):
        raise ValueError("scalar and oriented memory clocks must match")
    if not np.isclose(
        args.burn_memory_times,
        float(identifiability["burn_memory_times"]),
        rtol=0.0,
        atol=1e-15,
    ):
        raise ValueError("dynamic gate must inherit the source-audit burn interval")
    burn_updates = int(round(args.burn_memory_times / lambda_vector))
    analysis_updates = int(round(args.analysis_memory_times / lambda_vector))
    if not np.isclose(burn_updates * lambda_vector, args.burn_memory_times):
        raise ValueError("burn interval must resolve to whole updates")
    if not np.isclose(analysis_updates * lambda_vector, args.analysis_memory_times):
        raise ValueError("analysis interval must resolve to whole updates")
    total_updates = burn_updates + analysis_updates
    source_sample_steps = np.arange(total_updates + 1, dtype=int)
    target_sample_steps = _sample_steps(total_updates, args.sample_every, burn_updates)

    grid = LocalMediatorGrid(**mediator_summary["primary_grid"])
    if not np.isclose(grid.time_step, lambda_vector, rtol=0.0, atol=1e-15):
        raise ValueError("source, target and mediator time steps must match")
    mediators = {
        "relaxation_diffusion": RelaxationDiffusionMediator(
            **mediator_summary["models"]["relaxation_diffusion"]["parameters"]
        ),
        "telegraph": TelegraphMediator(
            **mediator_summary["models"]["telegraph"]["parameters"]
        ),
    }
    couplings = {
        model: float(mediator_summary["models"][model]["coupling"])
        for model in mediators
    }
    calibration_radius = float(mediator_summary["calibration_radius"])
    distance_ratios = np.asarray(mediator_summary["distance_ratios"], dtype=float)
    if distance_ratios.shape != (3,):
        raise ValueError("the inherited distance ladder must have three points")

    rows: list[dict[str, Any]] = []
    plot_data: dict[str, Any] | None = None
    source_noise_seed = int(identifiability["noise_seed"])
    for pair_index, item in enumerate(pair_cases):
        target = item["target"]
        source = item["source"]
        reference_row = item["reference"]
        readout_positions = item["distance_r0"] * calibration_radius
        if float(np.max(readout_positions)) >= grid.coordinates[-1]:
            raise ValueError("mediator grid does not contain every inherited distance")

        source_state = initialize_oriented_memory_state(
            source["state"],
            lambda_vector=lambda_vector,
            vector_mass=float(identifiability["vector_mass"]),
            orientation_relaxation=float(identifiability["orientation_relaxation"]),
        )
        source_rng = np.random.default_rng(
            source_noise_seed + 100_003 * int(source["seed"])
        )
        source_trace = autonomous_oriented_source_trace(
            source_state,
            first_config,
            source_noise=source_rng.normal(size=(total_updates, first_config.dim)),
            sample_steps=source_sample_steps,
        )
        persistent_input = source_trace.carrier_orientations[1:]
        displacement = np.diff(source_trace.positions, axis=0)
        displacement_norm = np.linalg.norm(displacement, axis=1, keepdims=True)
        one_step_input = np.divide(
            displacement,
            displacement_norm,
            out=np.zeros_like(displacement),
            where=displacement_norm > 0.0,
        )
        analysis_slice = slice(burn_updates, total_updates)
        source_input_rms = {
            "persistent": float(
                np.sqrt(
                    np.mean(np.sum(np.square(persistent_input[analysis_slice]), axis=1))
                )
            ),
            "one_step": float(
                np.sqrt(
                    np.mean(np.sum(np.square(one_step_input[analysis_slice]), axis=1))
                )
            ),
        }
        source_spectra = normalized_shape_spectra(source_trace.shape_tensors)
        source_radius_change = float(np.max(np.abs(source_trace.radius_ratios - 1.0)))
        source_spectrum_drift = float(
            np.max(np.linalg.norm(source_spectra - source_spectra[0], axis=1))
        )
        source_gates = {
            "radius_bounded": bool(
                source_radius_change <= thresholds["source_radius_max_change"]
            ),
            "shape_bounded": bool(
                source_spectrum_drift <= thresholds["source_spectrum_max_drift"]
            ),
        }

        target_rng = np.random.default_rng(
            int(
                args.target_noise_seed
                + 10_007 * int(target["seed"])
                + 100_003 * int(source["seed"])
            )
        )
        target_noise = target_rng.normal(size=(total_updates, first_config.dim))
        target_radius = float(reference_row["target_radius"])
        model_rows: dict[str, Any] = {}
        trace_store: dict[str, dict[str, list[np.ndarray]]] = {}
        for model, mediator in mediators.items():
            simulator = (
                simulate_vector_relaxation_diffusion_mediator
                if model == "relaxation_diffusion"
                else simulate_vector_telegraph_mediator
            )
            mediator_traces = {
                "persistent": simulator(
                    grid,
                    mediator,
                    source_values=persistent_input,
                    readout_positions=readout_positions,
                ),
                "one_step": simulator(
                    grid,
                    mediator,
                    source_values=one_step_input,
                    readout_positions=readout_positions,
                ),
            }
            distance_rows = []
            trace_store[model] = {"persistent": [], "one_step": []}
            persistent_responses = []
            for distance_index, ratio in enumerate(distance_ratios):
                input_metrics = {}
                input_gates = {}
                for input_name in ("persistent", "one_step"):
                    forcing = (
                        couplings[model]
                        * mediator_traces[input_name].values[1:, distance_index, :]
                    )
                    response = paired_external_field_response(
                        target["state"],
                        first_config,
                        applied_displacements=forcing,
                        noise=target_noise,
                        sample_steps=target_sample_steps,
                    )
                    metrics = dynamic_external_field_response_metrics(
                        response,
                        radius=target_radius,
                        analysis_start_step=burn_updates,
                    )
                    trace_store[model][input_name].append(
                        np.asarray(
                            metrics["trace_active_response_vector_r"],
                            dtype=float,
                        )
                    )
                    input_metrics[input_name] = _compact_metrics(metrics)
                    input_gates[input_name] = response_gates(metrics, thresholds)
                persistent_responses.append(
                    float(input_metrics["persistent"]["active_response_rms_r"])
                )
                distance_rows.append(
                    {
                        "distance_ratio_pair_radius": float(ratio),
                        "distance_r0": float(item["distance_r0"][distance_index]),
                        "persistent": input_metrics["persistent"],
                        "one_step": input_metrics["one_step"],
                        "persistent_gates": input_gates["persistent"],
                    }
                )
            attenuation = attenuation_gates(
                np.asarray(persistent_responses),
                tolerance=thresholds["response_monotonic_tolerance"],
                far_near_max_ratio=thresholds["far_near_max_ratio"],
            )
            pair_gates = {
                "source_shape": bool(all(source_gates.values())),
                "all_distance_response": bool(
                    all(
                        all(distance["persistent_gates"].values())
                        for distance in distance_rows
                    )
                ),
                "response_monotone": bool(attenuation["response_monotone"]),
                "far_near_bounded": bool(attenuation["far_near_bounded"]),
            }
            model_rows[model] = {
                "coupling": couplings[model],
                "distances": distance_rows,
                "attenuation": attenuation,
                "gates": pair_gates,
                "pair_pass": bool(all(pair_gates.values())),
            }

        model_separation = []
        for distance_index, ratio in enumerate(distance_ratios):
            persistent_separation = relative_trace_separation(
                trace_store["relaxation_diffusion"]["persistent"][distance_index],
                trace_store["telegraph"]["persistent"][distance_index],
            )
            one_step_separation = relative_trace_separation(
                trace_store["relaxation_diffusion"]["one_step"][distance_index],
                trace_store["telegraph"]["one_step"][distance_index],
            )
            model_separation.append(
                {
                    "distance_ratio_pair_radius": float(ratio),
                    "persistent": persistent_separation,
                    "one_step": one_step_separation,
                    "persistent_gate": bool(
                        persistent_separation
                        >= thresholds["model_trace_separation_min"]
                    ),
                }
            )
        pair_pass = bool(
            all(source_gates.values())
            and all(model_rows[model]["pair_pass"] for model in mediators)
            and all(item["persistent_gate"] for item in model_separation)
        )
        rows.append(
            {
                "pair_index": pair_index,
                "target_seed": int(target["seed"]),
                "source_seed": int(source["seed"]),
                "target_case_path": _relative(target["path"]),
                "target_case_sha256": target["sha256"],
                "source_case_path": _relative(source["path"]),
                "source_case_sha256": source["sha256"],
                "source_input_rms": source_input_rms,
                "source_radius_max_change": source_radius_change,
                "source_spectrum_max_drift": source_spectrum_drift,
                "source_gates": source_gates,
                "models": model_rows,
                "model_separation": model_separation,
                "pair_pass": pair_pass,
            }
        )

        if pair_index == 0:
            padded_one_step = np.vstack(
                (np.zeros((1, first_config.dim)), one_step_input)
            )
            analysis_steps = target_sample_steps[target_sample_steps >= burn_updates]
            plot_data = {
                "source_times_memory": target_sample_steps * lambda_vector,
                "persistent_source_norm": np.linalg.norm(
                    source_trace.carrier_orientations[target_sample_steps], axis=1
                ),
                "one_step_source_norm": np.linalg.norm(
                    padded_one_step[target_sample_steps], axis=1
                ),
                "target_times_memory": (np.asarray(analysis_steps) - burn_updates)
                * lambda_vector,
                "target_response": {
                    model: {
                        input_name: np.linalg.norm(
                            trace_store[model][input_name][0], axis=1
                        )
                        for input_name in ("persistent", "one_step")
                    }
                    for model in mediators
                },
            }

    assert plot_data is not None
    model_summary = {}
    model_pass_status = {}
    for model in mediators:
        model_distances = [
            distance for row in rows for distance in row["models"][model]["distances"]
        ]
        persistent = [distance["persistent"] for distance in model_distances]
        passing = sum(bool(row["models"][model]["pair_pass"]) for row in rows)
        model_summary[model] = {
            "passing_pairs": passing,
            "pair_count": len(rows),
            "response_rms_min": min(
                item["active_response_rms_r"] for item in persistent
            ),
            "response_rms_max": max(
                item["active_response_rms_r"] for item in persistent
            ),
            "odd_residual_max": max(
                item["odd_symmetry_relative_rms"] for item in persistent
            ),
            "target_radius_change_max": max(
                item["target_radius_max_change"] for item in persistent
            ),
            "target_shape_change_max": max(
                item["target_shape_max_change"] for item in persistent
            ),
        }
        model_pass_status[model] = bool(passing >= args.minimum_passing_pairs)
    separation_passing_pairs = sum(
        all(item["persistent_gate"] for item in row["model_separation"]) for row in rows
    )
    separation_summary = []
    for distance_index, ratio in enumerate(distance_ratios):
        values = np.asarray(
            [row["model_separation"][distance_index]["persistent"] for row in rows],
            dtype=float,
        )
        separation_summary.append(
            {
                "distance_ratio_pair_radius": float(ratio),
                "passing_pairs": int(
                    np.count_nonzero(values >= thresholds["model_trace_separation_min"])
                ),
                "pair_count": len(rows),
                "minimum": float(np.min(values)),
                "median": float(np.median(values)),
                "maximum": float(np.max(values)),
            }
        )
    overall_passing_pairs = sum(bool(row["pair_pass"]) for row in rows)
    if all(model_pass_status.values()) and (
        separation_passing_pairs >= args.minimum_passing_pairs
    ):
        decision = {
            "status": "dynamic_architectures_separated_mechanism_underdetermined",
            "model_pass_status": model_pass_status,
            "separation_passing_pairs": int(separation_passing_pairs),
            "overall_passing_pairs": int(overall_passing_pairs),
            "pair_count": len(rows),
            "selected_next_step": "independent_external_criterion_required",
            "interpretation": (
                "Both inserted mediator rules remain dynamically viable and their "
                "common-source target responses are distinguishable. With no "
                "independent observed target trajectory, neither rule is selected "
                "as physical and reciprocity remains closed."
            ),
        }
    elif sum(model_pass_status.values()) == 1:
        survivor = next(model for model, passed in model_pass_status.items() if passed)
        decision = {
            "status": "single_dynamic_architecture_survives_not_physical_selection",
            "model_pass_status": model_pass_status,
            "surviving_model": survivor,
            "separation_passing_pairs": int(separation_passing_pairs),
            "overall_passing_pairs": int(overall_passing_pairs),
            "pair_count": len(rows),
            "selected_next_step": "independent_external_criterion_required",
            "interpretation": (
                "Only one inserted architecture satisfies the dynamic knot-envelope "
                "gate. This rejects an implementation branch under fixed choices; "
                "it does not establish the survivor as a physical field law."
            ),
        }
    elif all(model_pass_status.values()):
        decision = {
            "status": "dynamic_common_source_gate_fail",
            "failed_stage": "cross_model_separation",
            "model_pass_status": model_pass_status,
            "separation_passing_pairs": int(separation_passing_pairs),
            "overall_passing_pairs": int(overall_passing_pairs),
            "pair_count": len(rows),
            "selected_next_step": "stop_or_reformulate_mediator_discrimination",
            "interpretation": (
                "Both fixed mediator branches satisfy the response, oddness, "
                "source/target shape, and attenuation gates for all pairs. The "
                f"preregistered cross-model separation criterion holds for only "
                f"{separation_passing_pairs}/{len(rows)} pairs rather than the "
                f"required {args.minimum_passing_pairs}/{len(rows)}. The present "
                "autonomous-source response therefore does not robustly "
                "distinguish the two inserted transport laws."
            ),
        }
    else:
        decision = {
            "status": "dynamic_common_source_gate_fail",
            "failed_stage": "response_or_shape_or_attenuation",
            "model_pass_status": model_pass_status,
            "separation_passing_pairs": int(separation_passing_pairs),
            "overall_passing_pairs": int(overall_passing_pairs),
            "pair_count": len(rows),
            "selected_next_step": "stop_or_reformulate_local_mediator_extension",
            "interpretation": (
                "The fixed dynamic mediator extension does not satisfy its response, "
                "shape, attenuation, or model-separation requirements."
            ),
        }

    report_path = _resolve(args.report)
    summary_path = _resolve(args.summary_json)
    figure_path = _resolve(args.figure)
    payload = {
        "schema": "dynamic-common-source-mediator-gate",
        "schema_version": 1,
        "generated_utc": datetime.now(UTC).isoformat(),
        "git_revision": _git_output(["rev-parse", "HEAD"]),
        "git_status_at_start": git_status,
        "command": ["python", *os.sys.argv],
        "identifiability_summary": _relative(ident_path),
        "mediator_summary": _relative(mediator_path),
        "source_reference": _relative(reference_path),
        "formation_config": asdict(first_config),
        "lambda_vector": lambda_vector,
        "burn_memory_times": float(args.burn_memory_times),
        "analysis_memory_times": float(args.analysis_memory_times),
        "burn_updates": burn_updates,
        "analysis_updates": analysis_updates,
        "total_updates": total_updates,
        "sample_every": int(args.sample_every),
        "source_noise_seed": source_noise_seed,
        "target_noise_seed": int(args.target_noise_seed),
        "source_noise_seed_rule": "source_noise_seed + 100003 * source_seed",
        "target_noise_seed_rule": (
            "target_noise_seed + 10007 * target_seed + 100003 * source_seed"
        ),
        "grid": asdict(grid),
        "mediator_parameters": {
            model: asdict(mediator) for model, mediator in mediators.items()
        },
        "couplings": couplings,
        "distance_ratios": distance_ratios,
        "thresholds": thresholds,
        "minimum_passing_pairs": int(args.minimum_passing_pairs),
        "rows": rows,
        "model_summary": model_summary,
        "separation_summary": separation_summary,
        "decision": decision,
        "plot_data": plot_data,
        "summary_json": summary_path,
        "figure": figure_path,
    }
    make_figure(payload, figure_path)
    payload["runtime_seconds"] = time.perf_counter() - started
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(
        json.dumps(_jsonable(payload), indent=2, sort_keys=True) + chr(10),
        encoding="utf-8",
    )
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        build_report(payload, report_path, figure_path), encoding="utf-8"
    )
    print(f"wrote {_relative(report_path)}", flush=True)


if __name__ == "__main__":
    main()
