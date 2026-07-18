"""Pilot for a compensated signed scalar cross-channel on frozen checkpoints."""

from __future__ import annotations

import argparse
from dataclasses import asdict, replace
from datetime import UTC, datetime
import json
import math
import os
from pathlib import Path
import subprocess
import sys
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def _repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("repository root not found")


ROOT = _repo_root()
SYNC_DIR = ROOT / "experiments" / "current" / "memory" / "synchronization"
sys.path.insert(0, str(SYNC_DIR))
sys.path.insert(0, str(ROOT / "src"))

from emergenz_knoten import (  # noqa: E402
    calibrate_signed_cross_eta,
    effective_double_gaussian_parameters,
    paired_signed_cross_response,
    two_scale_integral_coefficient,
    two_scale_local_curvature,
    zero_mean_curvature_matched_amplitudes,
)
from frozen_source_response import (  # noqa: E402
    CheckpointCase,
    load_checkpoint_cases,
)


DEFAULT_CHECKPOINT_DIR = Path(
    "data/processed/reference_states/scalar_Aatt35_N100M_d3_d10_seed1_2026-07-16"
)
LABEL_PAIRS = [(1, 1), (1, -1), (0, 1), (1, 0), (0, 0), (-1, -1), (-1, 1)]


def _utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


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


def _jsonable(value: Any) -> Any:
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        number = float(value)
        return number if math.isfinite(number) else None
    if isinstance(value, Path):
        return _rel(value)
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    return value


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Test a compensated signed scalar frozen-source cross-channel."
    )
    parser.add_argument("--checkpoint-dir", type=Path, default=DEFAULT_CHECKPOINT_DIR)
    parser.add_argument("--response-fraction", type=float, default=0.03)
    parser.add_argument("--separation-sigma-rep", type=float, default=1.0)
    parser.add_argument("--pulse-memory-times", type=float, default=1.0)
    parser.add_argument("--lag-memory-times", default="0,0.25,1,3,10")
    parser.add_argument("--sigma-comp-ratio", type=float, default=10.0)
    parser.add_argument("--noise-base-seed", type=int, default=20_260_718)
    parser.add_argument("--allow-dirty", action="store_true")
    parser.add_argument(
        "--report",
        type=Path,
        default=Path(
            "reports/response/signed_scalar_cross_channel_pilot_2026-07-18.md"
        ),
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=Path(
            "reports/response/signed_scalar_cross_channel_pilot_2026-07-18.json"
        ),
    )
    parser.add_argument(
        "--figure",
        type=Path,
        default=Path(
            "figures/draft/response/signed_scalar_cross_channel_2026-07-18/"
            "signed_cross_response.png"
        ),
    )
    return parser.parse_args()


def _float_list(value: str) -> list[float]:
    values = [float(item.strip()) for item in value.split(",") if item.strip()]
    if not values or any(not math.isfinite(item) for item in values):
        raise ValueError("expected finite comma-separated numbers")
    return values


def _max_abs(*arrays: np.ndarray) -> float:
    return float(
        max(
            (float(np.max(np.abs(array))) for array in arrays if array.size),
            default=0.0,
        )
    )


def _response_summary(response: Any, source_direction: np.ndarray) -> dict[str, Any]:
    products = np.asarray(response.label_products)
    plus_indices = np.flatnonzero(products == 1)
    minus_indices = np.flatnonzero(products == -1)
    zero_indices = np.flatnonzero(products == 0)
    if len(plus_indices) < 1 or len(minus_indices) < 1 or len(zero_indices) < 1:
        raise ValueError("response must contain positive, negative, and zero products")

    plus = int(plus_indices[0])
    minus = int(minus_indices[0])
    radius = float(response.target_radius)
    position_axis = (
        np.einsum("spi,i->sp", response.position_displacements, source_direction)
        / radius
    )
    center_axis = (
        np.einsum(
            "spi,i->sp",
            response.memory_center_displacements,
            source_direction,
        )
        / radius
    )
    radius_delta = np.asarray(response.radius_displacements)
    shape_norm = np.linalg.norm(response.shape_displacements, axis=2) / (
        radius * radius
    )

    null_error = _max_abs(
        response.position_displacements[:, zero_indices],
        response.memory_center_displacements[:, zero_indices],
        response.shape_displacements[:, zero_indices],
        response.radius_displacements[:, zero_indices],
    )
    product_error = 0.0
    for group in (plus_indices, minus_indices):
        reference = int(group[0])
        for other_value in group[1:]:
            other = int(other_value)
            product_error = max(
                product_error,
                _max_abs(
                    response.positions[:, reference] - response.positions[:, other],
                    response.memory_centers[:, reference]
                    - response.memory_centers[:, other],
                    response.shape_vectors[:, reference]
                    - response.shape_vectors[:, other],
                    response.radius_ratios[:, reference]
                    - response.radius_ratios[:, other],
                ),
            )

    plus_vector = response.position_displacements[0, plus]
    minus_vector = response.position_displacements[0, minus]
    odd_vector = 0.5 * (plus_vector - minus_vector)
    even_vector = 0.5 * (plus_vector + minus_vector)
    odd_norm = float(np.linalg.norm(odd_vector))
    even_to_odd = (
        float(np.linalg.norm(even_vector) / odd_norm) if odd_norm > 0.0 else None
    )
    plus_axis = float(position_axis[0, plus])
    minus_axis = float(position_axis[0, minus])
    maximum_radius_disturbance = float(np.max(np.abs(radius_delta)))

    return {
        "label_pairs": response.label_pairs,
        "label_products": products,
        "sample_steps": response.sample_steps,
        "position_axis_over_radius": position_axis,
        "center_axis_over_radius": center_axis,
        "radius_delta": radius_delta,
        "shape_norm_over_radius2": shape_norm,
        "null_max_abs_error": null_error,
        "product_equivalence_max_abs_error": product_error,
        "pulse_plus_axis_over_radius": plus_axis,
        "pulse_minus_axis_over_radius": minus_axis,
        "pulse_position_even_to_odd": even_to_odd,
        "pulse_label_flip_reverses_direction": bool(
            plus_axis > 0.0 and minus_axis < 0.0
        ),
        "maximum_radius_disturbance": maximum_radius_disturbance,
    }


def run_case(
    case: CheckpointCase,
    *,
    response_fraction: float,
    separation_sigma_rep: float,
    pulse_memory_times: float,
    lag_memory_times: list[float],
    sigma_comp_ratio: float,
    noise_base_seed: int,
) -> dict[str, Any]:
    if case.config.deposition_kernel != "delta":
        raise ValueError(
            "the curvature-matched pilot currently requires delta deposition"
        )
    tau_updates = 1.0 / case.config.alpha
    pulse_steps = max(1, int(round(pulse_memory_times * tau_updates)))
    lag_updates = np.asarray(
        [int(round(lag * tau_updates)) for lag in lag_memory_times],
        dtype=int,
    )
    sample_steps = pulse_steps + lag_updates
    if len(np.unique(sample_steps)) != len(sample_steps):
        raise ValueError("lag values collapse to duplicate sample steps")

    effective = effective_double_gaussian_parameters(
        dim=case.dim,
        sigma_rep=case.config.sigma_rep,
        sigma_att=case.config.sigma_att,
        amplitude_rep=case.config.amplitude_rep,
        amplitude_att=case.config.amplitude_att,
        deposition_kernel=case.config.deposition_kernel,
        deposition_sigma=case.config.deposition_sigma,
    )
    source_offset = np.zeros(case.dim, dtype=float)
    source_offset[0] = separation_sigma_rep * float(effective["sigma_rep"])
    sigma_comp = sigma_comp_ratio * case.config.sigma_rep
    target_curvature = two_scale_local_curvature(
        sigma_rep=case.config.sigma_rep,
        sigma_att=case.config.sigma_att,
        amplitude_rep=case.config.amplitude_rep,
        amplitude_att=case.config.amplitude_att,
    )
    matched_att, amplitude_comp = zero_mean_curvature_matched_amplitudes(
        dim=case.dim,
        sigma_rep=case.config.sigma_rep,
        sigma_att=case.config.sigma_att,
        sigma_comp=sigma_comp,
        target_curvature=target_curvature,
        amplitude_rep=case.config.amplitude_rep,
    )
    source_config = replace(case.config, amplitude_att=matched_att)
    integral_coefficient = (
        two_scale_integral_coefficient(
            dim=case.dim,
            sigma_rep=source_config.sigma_rep,
            sigma_att=source_config.sigma_att,
            amplitude_rep=source_config.amplitude_rep,
            amplitude_att=source_config.amplitude_att,
        )
        + amplitude_comp * sigma_comp**case.dim
    )
    matched_curvature = (
        two_scale_local_curvature(
            sigma_rep=source_config.sigma_rep,
            sigma_att=source_config.sigma_att,
            amplitude_rep=source_config.amplitude_rep,
            amplitude_att=source_config.amplitude_att,
        )
        - amplitude_comp / sigma_comp**2
    )

    calibration = calibrate_signed_cross_eta(
        case.state,
        case.state,
        case.config,
        source_center_offset=source_offset,
        response_fraction=response_fraction,
        pulse_steps=pulse_steps,
        source_config=source_config,
        sigma_comp=sigma_comp,
        amplitude_comp=amplitude_comp,
    )
    noise_seed = int(noise_base_seed + 1009 * case.dim + case.seed)
    noise = np.random.default_rng(noise_seed).normal(
        size=(int(sample_steps[-1]), case.dim)
    )
    common = {
        "label_pairs": LABEL_PAIRS,
        "source_center_offset": source_offset,
        "noise": noise,
        "sample_steps": sample_steps,
        "cross_eta": calibration.cross_eta,
        "pulse_steps": pulse_steps,
        "source_config": source_config,
        "sigma_comp": sigma_comp,
        "amplitude_comp": amplitude_comp,
    }
    active = paired_signed_cross_response(
        case.state,
        case.state,
        case.config,
        **common,
    )
    bare = paired_signed_cross_response(
        case.state,
        case.state,
        replace(case.config, eta=0.0),
        **common,
    )
    direction = source_offset / np.linalg.norm(source_offset)
    active_summary = _response_summary(active, direction)
    bare_summary = _response_summary(bare, direction)

    analytic_gate = bool(
        abs(integral_coefficient) <= 1.0e-9
        and math.isclose(matched_curvature, target_curvature, rel_tol=1.0e-12)
    )
    exact_controls = bool(
        active_summary["null_max_abs_error"] == 0.0
        and bare_summary["null_max_abs_error"] == 0.0
        and active_summary["product_equivalence_max_abs_error"] == 0.0
        and bare_summary["product_equivalence_max_abs_error"] == 0.0
    )
    label_flip_gate = bool(
        active_summary["pulse_label_flip_reverses_direction"]
        and bare_summary["pulse_label_flip_reverses_direction"]
        and active_summary["pulse_position_even_to_odd"] is not None
        and active_summary["pulse_position_even_to_odd"] <= 0.05
        and bare_summary["pulse_position_even_to_odd"] is not None
        and bare_summary["pulse_position_even_to_odd"] <= 0.05
    )
    nondestructive_gate = bool(
        active_summary["maximum_radius_disturbance"] <= 0.05
        and bare_summary["maximum_radius_disturbance"] <= 0.05
    )
    return {
        "checkpoint": _rel(case.path),
        "dim": case.dim,
        "formation_seed": case.seed,
        "update_index": case.update_index,
        "formation_revision": case.formation_revision,
        "target_config": asdict(case.config),
        "source_config": asdict(source_config),
        "initial_radius": case.initial_radius,
        "noise_seed": noise_seed,
        "pulse_steps": pulse_steps,
        "lag_memory_times": lag_memory_times,
        "sample_steps": sample_steps,
        "source_center_offset": source_offset,
        "cross_eta": calibration.cross_eta,
        "initial_canonical_directional_drift": (
            calibration.canonical_directional_drift
        ),
        "sigma_comp": sigma_comp,
        "amplitude_comp": amplitude_comp,
        "integral_coefficient": integral_coefficient,
        "target_curvature": target_curvature,
        "matched_curvature": matched_curvature,
        "active": active_summary,
        "eta_zero": bare_summary,
        "acceptance": {
            "analytic_compensation_and_curvature": analytic_gate,
            "exact_zero_and_product_controls": exact_controls,
            "pulse_label_flip": label_flip_gate,
            "radius_disturbance_below_five_percent": nondestructive_gate,
            "case_gate_pass": (
                analytic_gate
                and exact_controls
                and label_flip_gate
                and nondestructive_gate
            ),
        },
    }


def _plot(cases: list[dict[str, Any]], output: Path) -> None:
    fig, axes = plt.subplots(len(cases), 2, figsize=(10.8, 4.0 * len(cases)))
    if len(cases) == 1:
        axes = np.asarray([axes])
    styles = {
        "active": ("-", 1.9),
        "eta_zero": ("--", 1.45),
    }
    colors = {1: "#147d64", -1: "#c23b22", 0: "#777777"}
    for row, case in enumerate(cases):
        labels = np.asarray(case["active"]["label_pairs"])
        products = np.prod(labels, axis=1)
        for channel, (linestyle, width) in styles.items():
            summary = case[channel]
            lag = np.asarray(case["lag_memory_times"], dtype=float)
            for product in (1, -1, 0):
                index = int(np.flatnonzero(products == product)[0])
                label = f"product {product:+d}, {channel}"
                axes[row, 0].plot(
                    lag,
                    np.asarray(summary["position_axis_over_radius"])[:, index],
                    color=colors[product],
                    linestyle=linestyle,
                    linewidth=width,
                    label=label,
                )
                axes[row, 1].plot(
                    lag,
                    np.asarray(summary["radius_delta"])[:, index],
                    color=colors[product],
                    linestyle=linestyle,
                    linewidth=width,
                    label=label,
                )
        axes[row, 0].axhline(0.0, color="#888888", linewidth=0.8)
        axes[row, 1].axhline(0.0, color="#888888", linewidth=0.8)
        axes[row, 0].set_ylabel(f"d={case['dim']} axial displacement / R_mem")
        axes[row, 1].set_ylabel(f"d={case['dim']} radius change / R_mem")
        for axis in axes[row]:
            axis.set_xlabel("lag after pulse [memory times]")
            axis.grid(True, alpha=0.22)
        axes[row, 0].legend(frameon=False, fontsize=7, ncol=2)
    axes[0, 0].set_title("signed center-of-particle response")
    axes[0, 1].set_title("non-destructive radius control")
    fig.tight_layout()
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=190)
    plt.close(fig)


def _fmt(value: Any, digits: int = 5) -> str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return "n/a"
    if not math.isfinite(number):
        return "n/a"
    if number == 0.0:
        return "0"
    if abs(number) < 1.0e-3 or abs(number) >= 1.0e4:
        return f"{number:.{digits}e}"
    return f"{number:.{digits}f}"


def build_report(payload: dict[str, Any], report_path: Path, figure: Path) -> str:
    lines = [
        "# Signed Scalar Cross-Channel Pilot",
        "",
        f"Date: {payload['generated_utc']}.",
        "",
        "## Scope",
        "",
        "This is a channel-architecture test on frozen scalar-memory checkpoints.",
        "The externally assigned labels s_target and s_source enter only through",
        "their product in the cross force. The established non-negative self-memory",
        "and self-confinement dynamics are unchanged.",
        "",
        "The cross potential uses the broad three-scale compensation that enforces",
        "zero spatial integral and exactly matches the local curvature of the",
        "two-scale A_att=35 reference in each ambient dimension.",
        "",
        f"![Signed response]({_rel_from(report_path, figure)})",
        "",
        "## Gate Results",
        "",
        "| d | A_att cross | A_comp | integral | curvature error | eta_cross | null error | product error | active even/odd | max radius disturbance | pass |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for case in payload["cases"]:
        active = case["active"]
        acceptance = case["acceptance"]
        lines.append(
            f"| {case['dim']} | {_fmt(case['source_config']['amplitude_att'])} | "
            f"{_fmt(case['amplitude_comp'])} | {_fmt(case['integral_coefficient'])} | "
            f"{_fmt(case['matched_curvature'] - case['target_curvature'])} | "
            f"{_fmt(case['cross_eta'])} | {_fmt(active['null_max_abs_error'])} | "
            f"{_fmt(active['product_equivalence_max_abs_error'])} | "
            f"{_fmt(active['pulse_position_even_to_odd'])} | "
            f"{_fmt(active['maximum_radius_disturbance'])} | "
            f"{acceptance['case_gate_pass']} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            f"- Overall mechanism gate: {payload['acceptance']['mechanism_gate_pass']}.",
            "- The zero-label branches and the explicit free path are bitwise",
            "  identical. Source-zero and target-zero are therefore exact null arms.",
            "- Equal label products generate identical paths, while changing the",
            "  product reverses the pulse response under common future noise.",
            "- Product +1 retains the canonical attractive sign at one sigma_rep;",
            "  product -1 reverses it. This sign convention is explicit and can be",
            "  changed only as a separately declared model choice.",
            "- Passing this test establishes only a mathematically consistent signed",
            "  scalar cross-channel. The labels are assigned inputs, not emergent,",
            "  conserved, quantized, or identified with electric charge.",
            "- One checkpoint per dimension is an architecture validation, not",
            "  seed-level evidence. No reciprocal dynamics or source backreaction",
            "  is present.",
            "",
            "## Next Decision",
            "",
            "1. Form at least six, preferably ten independent reference states and",
            "   repeat the null/sign/nondestruction gates without retuning.",
            "2. Test the static compensated force at distances below and above its",
            "   force crossing without recalibrating each distance.",
            "3. Only then promote the source to one-way dynamics; reciprocal two-knot",
            "   coupling follows after identity and energy-accounting diagnostics.",
            "",
            "## Provenance",
            "",
            f"- Git revision: {payload['git_revision']}",
            f"- Git status at generation: {payload['git_status'] or 'clean'}",
            f"- Checkpoint directory: {payload['checkpoint_dir']}",
            "- Script: experiments/current/memory/synchronization/signed_cross_channel_pilot.py",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    lag_memory_times = _float_list(args.lag_memory_times)
    if any(value < 0.0 for value in lag_memory_times):
        raise SystemExit("lag-memory-times must be non-negative")
    if args.response_fraction <= 0.0 or args.separation_sigma_rep <= 0.0:
        raise SystemExit("response fraction and separation must be positive")
    if args.pulse_memory_times <= 0.0 or args.sigma_comp_ratio <= 1.0:
        raise SystemExit("pulse time must be positive and compensator ratio > 1")

    git_revision = _git_output(["rev-parse", "HEAD"])
    git_status = _git_output(["status", "--short"])
    if git_status not in {"", "unavailable"} and not args.allow_dirty:
        raise SystemExit("refusing to generate evidence from a dirty worktree")

    cases = [
        run_case(
            case,
            response_fraction=args.response_fraction,
            separation_sigma_rep=args.separation_sigma_rep,
            pulse_memory_times=args.pulse_memory_times,
            lag_memory_times=lag_memory_times,
            sigma_comp_ratio=args.sigma_comp_ratio,
            noise_base_seed=args.noise_base_seed,
        )
        for case in load_checkpoint_cases(args.checkpoint_dir)
    ]
    mechanism_gate = all(case["acceptance"]["case_gate_pass"] for case in cases)
    figure = _resolve(args.figure)
    _plot(cases, figure)
    payload = {
        "description": "Compensated signed scalar frozen-source channel pilot.",
        "generated_utc": _utc_now(),
        "git_revision": git_revision,
        "git_status": git_status,
        "checkpoint_dir": _rel(_resolve(args.checkpoint_dir)),
        "parameters": {
            "response_fraction": args.response_fraction,
            "separation_sigma_rep": args.separation_sigma_rep,
            "pulse_memory_times": args.pulse_memory_times,
            "lag_memory_times": lag_memory_times,
            "sigma_comp_ratio": args.sigma_comp_ratio,
            "label_pairs": LABEL_PAIRS,
            "noise_base_seed": args.noise_base_seed,
        },
        "cases": cases,
        "acceptance": {"mechanism_gate_pass": mechanism_gate},
        "figure": _rel(figure),
    }
    summary_path = _resolve(args.summary_json)
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(
        json.dumps(_jsonable(payload), indent=2, sort_keys=True, allow_nan=False),
        encoding="utf-8",
    )
    report_path = _resolve(args.report)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        build_report(_jsonable(payload), report_path, figure),
        encoding="utf-8",
    )
    print(f"wrote {report_path}")
    print(f"wrote {summary_path}")
    print(f"wrote {figure}")


if __name__ == "__main__":
    main()
