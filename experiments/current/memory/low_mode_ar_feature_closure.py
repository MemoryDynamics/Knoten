from __future__ import annotations

import argparse
from dataclasses import asdict
from datetime import UTC, datetime
import json
import math
import os
from pathlib import Path
import statistics
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
sys.path.insert(0, str(ROOT / "src"))

from emergenz_knoten.markov.closure import (  # noqa: E402
    fit_ar_spectrum,
    leave_one_series_out_closure,
)
from emergenz_knoten.relaxation_diffusion_memory import (  # noqa: E402
    RelaxationDiffusionMemoryOperators,
)
from emergenz_knoten.spectral_memory_field import (  # noqa: E402
    SpectralMemoryConfig,
    zero_mean_attractive_kernel,
)
from emergenz_knoten.spectral_memory_trace import (  # noqa: E402
    direct_history_potential_gradient,
    low_mode_feature_groups,
    low_mode_feature_names,
    omitted_history_weight,
    simulate_spectral_memory_trace,
)


def _parse_int_list(value: str) -> list[int]:
    result = [int(item.strip()) for item in value.split(",") if item.strip()]
    if not result or any(item < 1 for item in result):
        raise argparse.ArgumentTypeError("expected positive comma-separated integers")
    return result


def _parse_float_list(value: str) -> list[float]:
    result = [float(item.strip()) for item in value.split(",") if item.strip()]
    if not result or any(not math.isfinite(item) or item < 0.0 for item in result):
        raise argparse.ArgumentTypeError(
            "expected non-negative comma-separated numbers"
        )
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Controlled low-mode AR closure gate for scalar spectral memory."
    )
    parser.add_argument("--steps", type=int, default=100_000)
    parser.add_argument("--burn-in", type=int, default=5_000)
    parser.add_argument("--sample-every", type=int, default=10)
    parser.add_argument("--seeds", type=_parse_int_list, default=_parse_int_list("1,2,3,4,5"))
    parser.add_argument(
        "--diffusion-length-ratios",
        type=_parse_float_list,
        default=_parse_float_list("0,0.3,1"),
    )
    parser.add_argument("--lags", type=_parse_int_list, default=_parse_int_list("1,2,5,10,20"))
    parser.add_argument("--epsilon", type=float, default=1e-4)
    parser.add_argument("--eta", type=float, default=0.15)
    parser.add_argument("--lambda-value", type=float, default=0.01)
    parser.add_argument("--memory-mass", type=float, default=1.0)
    parser.add_argument("--box-length", type=float, default=80.0)
    parser.add_argument("--n-modes", type=int, default=64)
    parser.add_argument("--n-low-modes", type=int, default=3)
    parser.add_argument("--amplitude-att", type=float, default=26.0)
    parser.add_argument("--sigma-att", type=float, default=3.0)
    parser.add_argument("--sigma-comp", type=float, default=10.0)
    parser.add_argument(
        "--real-offsets",
        type=_parse_float_list,
        default=_parse_float_list("0,1.5,3,6"),
    )
    parser.add_argument("--history-length", type=int, default=2_000)
    parser.add_argument("--ridge", type=float, default=1e-6)
    parser.add_argument("--shuffle-repeats", type=int, default=3)
    parser.add_argument("--resolution-seeds", type=int, default=3)
    parser.add_argument("--skip-resolution", action="store_true")
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("reports/memory/low_mode_ar_feature_closure_2026-07-19.md"),
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=Path("reports/memory/low_mode_ar_feature_closure_2026-07-19.json"),
    )
    parser.add_argument(
        "--figure",
        type=Path,
        default=Path(
            "figures/draft/memory/low_mode_ar_feature_closure_2026-07-19.png"
        ),
    )
    return parser.parse_args()


def _validate_args(args: argparse.Namespace) -> None:
    if args.steps < 100 or not 0 <= args.burn_in < args.steps:
        raise SystemExit("steps must be >= 100 and burn-in must be smaller")
    if args.sample_every < 1 or args.history_length < 1:
        raise SystemExit("sample-every and history-length must be positive")
    if 0.0 not in args.diffusion_length_ratios:
        raise SystemExit("diffusion ratios must include the nu=0 control")
    if args.n_low_modes > args.n_modes:
        raise SystemExit("n-low-modes cannot exceed n-modes")
    if args.resolution_seeds < 1:
        raise SystemExit("resolution-seeds must be positive")


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def _relative(source: Path, target: Path) -> str:
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


def _config(
    args: argparse.Namespace,
    *,
    box_length: float | None = None,
    n_modes: int | None = None,
) -> SpectralMemoryConfig:
    return SpectralMemoryConfig(
        box_length=float(args.box_length if box_length is None else box_length),
        n_modes=int(args.n_modes if n_modes is None else n_modes),
        lambda_value=float(args.lambda_value),
        memory_mass=float(args.memory_mass),
        deposition_sigma=0.0,
        kernel=zero_mean_attractive_kernel(
            amplitude_att=float(args.amplitude_att),
            sigma_att=float(args.sigma_att),
            sigma_comp=float(args.sigma_comp),
        ),
    )


def _diffusion_per_update(args: argparse.Namespace, ratio: float) -> float:
    length = float(ratio) * float(args.sigma_att)
    return float(0.5 * args.lambda_value * length**2)


def _active_indices(series: list[np.ndarray], candidates: list[int]) -> list[int]:
    pooled = np.concatenate([values[:, candidates] for values in series], axis=0)
    scales = pooled.std(axis=0)
    reference = max(float(np.max(scales)), np.finfo(float).eps)
    selected = [
        index
        for index, scale in zip(candidates, scales, strict=True)
        if float(scale) > 1e-10 * reference
    ]
    if not selected:
        raise RuntimeError("feature group has no varying observables")
    return selected


def _top_modes(spectrum: Any, limit: int = 6) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    for eigenvalue, rate, frequency in zip(
        spectrum.eigenvalues[:limit],
        spectrum.rates_per_update[:limit],
        spectrum.angular_frequencies_per_update[:limit],
        strict=True,
    ):
        rows.append(
            {
                "real": float(eigenvalue.real),
                "imag": float(eigenvalue.imag),
                "modulus": float(abs(eigenvalue)),
                "rate_per_update": float(rate),
                "angular_frequency_per_update": float(frequency),
            }
        )
    return rows


def _run_case(
    args: argparse.Namespace,
    *,
    config: SpectralMemoryConfig,
    ratio: float,
    eta: float,
    seed: int,
    noise: np.ndarray,
) -> tuple[np.ndarray, dict[str, Any]]:
    nu = _diffusion_per_update(args, ratio)
    trace = simulate_spectral_memory_trace(
        config,
        noise=noise,
        diffusion_per_update=nu,
        epsilon=float(args.epsilon),
        eta=float(eta),
        burn_in=int(args.burn_in),
        sample_every=int(args.sample_every),
        n_low_modes=int(args.n_low_modes),
        real_offsets=args.real_offsets,
        history_length=int(args.history_length),
    )
    operators = RelaxationDiffusionMemoryOperators(
        config,
        diffusion_per_update=nu,
    )
    direct_checks: list[dict[str, float]] = []
    for offset in (0.5 * args.sigma_att, args.sigma_att, args.sigma_comp):
        evaluation_x = trace.final_x + float(offset)
        spectral = operators.gradient(
            trace.final_rho_coefficients,
            x=evaluation_x,
        )
        direct = direct_history_potential_gradient(
            config,
            evaluation_x=evaluation_x,
            initial_x=0.5 * config.box_length,
            recent_positions_newest_first=trace.recent_positions_newest_first,
            total_updates=trace.update_count,
            diffusion_per_update=nu,
        )
        direct_checks.append(
            {
                "offset": float(offset),
                "spectral_gradient": float(spectral),
                "direct_history_gradient": float(direct),
                "absolute_error": abs(float(spectral - direct)),
                "scaled_error": abs(float(spectral - direct))
                / max(1.0, abs(float(spectral)), abs(float(direct))),
            }
        )
    row = {
        "diffusion_length_ratio": float(ratio),
        "diffusion_per_update": nu,
        "condition": "active" if eta > 0.0 else "eta_zero",
        "eta": float(eta),
        "seed": int(seed),
        "box_length": float(config.box_length),
        "n_modes": int(config.n_modes),
        "relative_radius_rms": float(np.sqrt(np.mean(trace.values[:, 0] ** 2))),
        "force_rms": float(np.sqrt(np.mean(trace.values[:, 1] ** 2))),
        "direct_history_checks": direct_checks,
        "omitted_history_weight": omitted_history_weight(
            config.lambda_value,
            len(trace.recent_positions_newest_first),
        ),
    }
    return trace.values, row


def _analyze_groups(
    args: argparse.Namespace,
    traces: dict[tuple[float, str], list[np.ndarray]],
    feature_names: tuple[str, ...],
) -> list[dict[str, Any]]:
    groups = low_mode_feature_groups(args.n_low_modes, args.real_offsets)
    results: list[dict[str, Any]] = []
    for (ratio, condition), raw_series in sorted(traces.items()):
        for group_name, candidate_indices in groups.items():
            indices = _active_indices(raw_series, candidate_indices)
            series = [values[:, indices] for values in raw_series]
            for lag in args.lags:
                closure = leave_one_series_out_closure(
                    series,
                    lag=int(lag),
                    ridge=float(args.ridge),
                    shuffle_repeats=int(args.shuffle_repeats),
                    random_seed=20260719 + int(lag),
                )
                lag_updates = int(lag) * int(args.sample_every)
                spectrum = fit_ar_spectrum(
                    series,
                    lag=int(lag),
                    lag_updates=lag_updates,
                    ridge=float(args.ridge),
                )
                seed_top_modes = [
                    _top_modes(
                        fit_ar_spectrum(
                            [seed_series],
                            lag=int(lag),
                            lag_updates=lag_updates,
                            ridge=float(args.ridge),
                        )
                    )
                    for seed_series in series
                ]
                row = asdict(closure)
                row.update(
                    {
                        "diffusion_length_ratio": float(ratio),
                        "condition": condition,
                        "feature_group": group_name,
                        "feature_names": [feature_names[index] for index in indices],
                        "lag_updates": lag_updates,
                        "lag_memory_times": lag_updates * args.lambda_value,
                        "residual_rms": spectrum.residual_rms,
                        "top_modes": _top_modes(spectrum),
                        "seed_top_modes": seed_top_modes,
                    }
                )
                results.append(row)
    return results


def _resolution_specs(args: argparse.Namespace) -> list[tuple[str, float, int]]:
    density = args.n_modes / args.box_length
    return [
        ("modes_32", args.box_length, max(args.n_low_modes, 32)),
        ("default", args.box_length, args.n_modes),
        ("modes_128", args.box_length, max(args.n_low_modes, 128)),
        ("box_60", 60.0, max(args.n_low_modes, round(60.0 * density))),
        ("box_120", 120.0, max(args.n_low_modes, round(120.0 * density))),
    ]


def _run_resolution(
    args: argparse.Namespace,
    noises: dict[int, np.ndarray],
    ratio: float,
) -> list[dict[str, Any]]:
    if args.skip_resolution:
        return []
    rows: list[dict[str, Any]] = []
    seeds = args.seeds[: min(args.resolution_seeds, len(args.seeds))]
    for name, box_length, n_modes in _resolution_specs(args):
        config = _config(args, box_length=box_length, n_modes=n_modes)
        for seed in seeds:
            _, row = _run_case(
                args,
                config=config,
                ratio=ratio,
                eta=args.eta,
                seed=seed,
                noise=noises[seed],
            )
            row["resolution_name"] = name
            rows.append(row)
    return rows


def _median(values: list[float]) -> float:
    return float(statistics.median(values))


def _dominant_mode(row: dict[str, Any]) -> dict[str, float] | None:
    for mode in row["top_modes"]:
        if 0.05 < mode["modulus"] < 1.0 and math.isfinite(mode["rate_per_update"]):
            return mode
    return None


def _first_complex_mode(modes: list[dict[str, float]]) -> dict[str, float] | None:
    for mode in modes:
        if (
            0.05 < mode["modulus"] < 1.0
            and abs(mode["imag"]) > 1e-6
            and math.isfinite(mode["rate_per_update"])
        ):
            return mode
    return None


def _seed_complex_summary(
    row: dict[str, Any],
    lambda_value: float,
) -> dict[str, Any]:
    frequencies: list[float] = []
    rates: list[float] = []
    for modes in row["seed_top_modes"]:
        mode = _first_complex_mode(modes)
        if mode is None:
            continue
        frequencies.append(
            abs(mode["angular_frequency_per_update"]) / lambda_value
        )
        rates.append(mode["rate_per_update"] / lambda_value)
    required = max(2, math.ceil(0.8 * len(row["seed_top_modes"])))
    if not frequencies:
        return {
            "seed_count": 0,
            "required_seed_count": required,
            "stable": False,
        }
    frequency = _median(frequencies)
    frequency_mad = _median([abs(value - frequency) for value in frequencies])
    rate = _median(rates)
    return {
        "seed_count": len(frequencies),
        "required_seed_count": required,
        "frequency_per_memory_time": frequency,
        "frequency_relative_mad": frequency_mad / max(abs(frequency), 1e-12),
        "rate_per_memory_time": rate,
        "quality_factor": frequency / max(2.0 * rate, 1e-12),
        "stable": bool(
            len(frequencies) >= required
            and frequency_mad / max(abs(frequency), 1e-12) < 0.25
        ),
    }


def _preferred_diffusion_ratio(
    args: argparse.Namespace,
    analyses: list[dict[str, Any]],
) -> float:
    positive = [value for value in args.diffusion_length_ratios if value > 0.0]
    if not positive:
        return 0.0
    counts = {
        ratio: sum(
            _seed_complex_summary(row, args.lambda_value)["stable"]
            for row in analyses
            if row["feature_group"] == "low_modes"
            and row["condition"] == "active"
            and row["diffusion_length_ratio"] == ratio
        )
        for ratio in positive
    }
    if max(counts.values()) == 0:
        return max(positive)
    return max(positive, key=lambda ratio: (counts[ratio], -ratio))



def _gate_summary(
    args: argparse.Namespace,
    cases: list[dict[str, Any]],
    analyses: list[dict[str, Any]],
    resolution: list[dict[str, Any]],
) -> dict[str, Any]:
    direct_max = max(
        check["scaled_error"]
        for case in cases
        for check in case["direct_history_checks"]
    )
    resolution_changes: dict[str, dict[str, float]] = {}
    if resolution:
        grouped: dict[str, list[dict[str, Any]]] = {}
        for row in resolution:
            grouped.setdefault(row["resolution_name"], []).append(row)
        reference_radius = _median(
            [row["relative_radius_rms"] for row in grouped["default"]]
        )
        reference_force = _median([row["force_rms"] for row in grouped["default"]])
        for name, rows in grouped.items():
            radius = _median([row["relative_radius_rms"] for row in rows])
            force = _median([row["force_rms"] for row in rows])
            resolution_changes[name] = {
                "radius_relative_change": abs(radius / reference_radius - 1.0),
                "force_relative_change": abs(force / reference_force - 1.0),
            }
    max_resolution_change = max(
        (
            max(values.values())
            for name, values in resolution_changes.items()
            if name != "default"
        ),
        default=0.0,
    )

    active_positive = [
        row
        for row in analyses
        if row["feature_group"] == "low_modes"
        and row["condition"] == "active"
        and row["diffusion_length_ratio"] > 0.0
    ]
    closure_pass_count = sum(row["closure_lift"] > 0.02 for row in active_positive)
    closure_required = max(1, math.ceil(0.6 * len(active_positive)))

    rates_by_arm: dict[tuple[float, str], list[float]] = {}
    complex_by_arm: dict[tuple[float, str], list[dict[str, Any]]] = {}
    for row in analyses:
        if row["feature_group"] != "low_modes":
            continue
        key = (row["diffusion_length_ratio"], row["condition"])
        mode = _dominant_mode(row)
        if mode is not None:
            rates_by_arm.setdefault(key, []).append(
                mode["rate_per_update"] / args.lambda_value
            )
        complex_summary = _seed_complex_summary(row, args.lambda_value)
        row["seed_complex_summary"] = complex_summary
        if complex_summary["stable"]:
            complex_by_arm.setdefault(key, []).append(complex_summary)

    rate_stability: dict[str, float] = {}
    for key, values in rates_by_arm.items():
        median = _median(values)
        if median != 0.0:
            mad = _median([abs(value - median) for value in values])
            rate_stability[f"{key[0]}:{key[1]}"] = mad / abs(median)

    selected_ratio = _preferred_diffusion_ratio(args, analyses)
    active_rates = rates_by_arm.get((selected_ratio, "active"), [])
    eta_zero_rates = rates_by_arm.get((selected_ratio, "eta_zero"), [])
    nu_zero_rates = rates_by_arm.get((0.0, "active"), [])
    active_rate = _median(active_rates) if active_rates else float("nan")
    eta_zero_rate = _median(eta_zero_rates) if eta_zero_rates else float("nan")
    nu_zero_rate = _median(nu_zero_rates) if nu_zero_rates else float("nan")
    control_separation = min(
        abs(active_rate - eta_zero_rate) / max(abs(active_rate), 1e-12),
        abs(active_rate - nu_zero_rate) / max(abs(active_rate), 1e-12),
    )

    complex_rows = complex_by_arm.get((selected_ratio, "active"), [])
    complex_frequencies = [
        row["frequency_per_memory_time"] for row in complex_rows
    ]
    complex_rates = [row["rate_per_memory_time"] for row in complex_rows]
    complex_quality = [row["quality_factor"] for row in complex_rows]
    if complex_frequencies:
        complex_frequency = _median(complex_frequencies)
        complex_frequency_relative_mad = _median(
            [abs(value - complex_frequency) for value in complex_frequencies]
        ) / max(abs(complex_frequency), 1e-12)
        complex_rate = _median(complex_rates)
        complex_quality_factor = _median(complex_quality)
    else:
        complex_frequency = float("nan")
        complex_frequency_relative_mad = float("nan")
        complex_rate = float("nan")
        complex_quality_factor = float("nan")
    eta_zero_complex_rows = len(
        complex_by_arm.get((selected_ratio, "eta_zero"), [])
    )
    nu_zero_complex_rows = len(complex_by_arm.get((0.0, "active"), []))
    complex_stability_pass = bool(
        len(complex_rows) >= 3 and complex_frequency_relative_mad < 0.25
    )
    complex_control_pass = bool(
        eta_zero_complex_rows <= 1 and nu_zero_complex_rows <= 1
    )
    return {
        "direct_real_space_pass": direct_max < 1e-6,
        "direct_real_space_max_scaled_error": direct_max,
        "resolution_pass": max_resolution_change < 0.05,
        "max_resolution_relative_change": max_resolution_change,
        "resolution_changes": resolution_changes,
        "closure_pass": closure_pass_count >= closure_required,
        "closure_pass_count": closure_pass_count,
        "closure_required": closure_required,
        "closure_row_count": len(active_positive),
        "rate_stability_mad_over_median": rate_stability,
        "selected_ratio": selected_ratio,
        "active_rate_per_memory_time": active_rate,
        "eta_zero_rate_per_memory_time": eta_zero_rate,
        "nu_zero_rate_per_memory_time": nu_zero_rate,
        "control_separation_fraction": control_separation,
        "control_separation_pass": control_separation > 0.2,
        "complex_mode_rows_selected_arm": len(complex_rows),
        "complex_frequency_per_memory_time": complex_frequency,
        "complex_frequency_relative_mad": complex_frequency_relative_mad,
        "complex_rate_per_memory_time": complex_rate,
        "complex_quality_factor": complex_quality_factor,
        "eta_zero_complex_rows": eta_zero_complex_rows,
        "nu_zero_complex_rows": nu_zero_complex_rows,
        "complex_stability_pass": complex_stability_pass,
        "complex_control_pass": complex_control_pass,
        "long_confirmation_recommended": bool(
            direct_max < 1e-6
            and max_resolution_change < 0.05
            and closure_pass_count >= closure_required
        ),
        "new_mode_discovery_long_run_justified": bool(
            direct_max < 1e-6
            and max_resolution_change < 0.05
            and closure_pass_count >= closure_required
            and control_separation > 0.2
            and complex_stability_pass
            and complex_control_pass
        ),
    }


def run_probe(args: argparse.Namespace) -> dict[str, Any]:
    config = _config(args)
    noises = {
        seed: np.random.default_rng(seed).normal(size=args.steps)
        for seed in args.seeds
    }
    traces: dict[tuple[float, str], list[np.ndarray]] = {}
    cases: list[dict[str, Any]] = []
    feature_names: tuple[str, ...] | None = None
    for ratio in args.diffusion_length_ratios:
        for condition, eta in (("active", args.eta), ("eta_zero", 0.0)):
            key = (float(ratio), condition)
            traces[key] = []
            for seed in args.seeds:
                values, row = _run_case(
                    args,
                    config=config,
                    ratio=ratio,
                    eta=eta,
                    seed=seed,
                    noise=noises[seed],
                )
                traces[key].append(values)
                cases.append(row)
                if feature_names is None:
                    feature_names = low_mode_feature_names(
                        args.n_low_modes,
                        args.real_offsets,
                    )
    assert feature_names is not None
    analyses = _analyze_groups(args, traces, feature_names)
    preferred_ratio = _preferred_diffusion_ratio(args, analyses)
    resolution = _run_resolution(args, noises, preferred_ratio)
    gate = _gate_summary(args, cases, analyses, resolution)
    return {
        "description": "Controlled scalar spectral-memory low-mode AR closure gate.",
        "created_utc": datetime.now(UTC).isoformat(),
        "git_revision": _git_output(["rev-parse", "HEAD"]),
        "git_status": _git_output(["status", "--short"]),
        "parameters": {
            key: value
            for key, value in vars(args).items()
            if key not in {"report", "summary_json", "figure"}
        },
        "feature_names": list(feature_names),
        "cases": cases,
        "analyses": analyses,
        "resolution": resolution,
        "gate": gate,
    }


def _plot(payload: dict[str, Any], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    analyses = [
        row
        for row in payload["analyses"]
        if row["feature_group"] == "low_modes"
    ]
    fig, axes = plt.subplots(2, 2, figsize=(12.0, 8.2))
    colors = {0.0: "black", 0.3: "#0072B2", 1.0: "#D55E00"}
    for ratio in sorted({row["diffusion_length_ratio"] for row in analyses}):
        for condition, linestyle in (("active", "-"), ("eta_zero", "--")):
            rows = sorted(
                [
                    row
                    for row in analyses
                    if row["diffusion_length_ratio"] == ratio
                    and row["condition"] == condition
                ],
                key=lambda row: row["lag_memory_times"],
            )
            label = f"ratio={ratio:g}, {condition}"
            x = [row["lag_memory_times"] for row in rows]
            axes[0, 0].plot(
                x,
                [row["closure_lift"] for row in rows],
                marker="o",
                linestyle=linestyle,
                color=colors.get(ratio),
                label=label,
            )
            rates = []
            frequencies = []
            for row in rows:
                mode = _dominant_mode(row)
                rates.append(
                    mode["rate_per_update"] / payload["parameters"]["lambda_value"]
                    if mode is not None
                    else np.nan
                )
                frequencies.append(
                    abs(mode["angular_frequency_per_update"])
                    / payload["parameters"]["lambda_value"]
                    if mode is not None and abs(mode["imag"]) > 1e-6
                    else np.nan
                )
            axes[0, 1].plot(
                x,
                rates,
                marker="o",
                linestyle=linestyle,
                color=colors.get(ratio),
            )
            axes[1, 0].plot(
                x,
                frequencies,
                marker="o",
                linestyle=linestyle,
                color=colors.get(ratio),
            )
    axes[0, 0].axhline(0.02, color="#666666", linewidth=1)
    axes[0, 0].set_ylabel("closure lift")
    axes[0, 0].legend(fontsize=7, ncol=2)
    axes[0, 1].set_ylabel("dominant rate per memory time")
    axes[1, 0].set_ylabel("complex frequency per memory time")
    for axis in axes.flat[:3]:
        axis.set_xscale("log")
        axis.set_xlabel("lag / memory time")
        axis.grid(alpha=0.25)

    resolution = payload["gate"]["resolution_changes"]
    names = [name for name in resolution if name != "default"]
    x = np.arange(len(names))
    axes[1, 1].bar(
        x - 0.18,
        [resolution[name]["radius_relative_change"] for name in names],
        width=0.36,
        label="relative radius",
        color="#009E73",
    )
    axes[1, 1].bar(
        x + 0.18,
        [resolution[name]["force_relative_change"] for name in names],
        width=0.36,
        label="force RMS",
        color="#CC79A7",
    )
    axes[1, 1].axhline(0.05, color="#666666", linewidth=1)
    axes[1, 1].set_xticks(x, names, rotation=25, ha="right")
    axes[1, 1].set_ylabel("relative change from default")
    axes[1, 1].legend(fontsize=8)
    axes[1, 1].grid(axis="y", alpha=0.25)
    fig.suptitle("Low-mode AR closure with representation and null controls")
    fig.tight_layout()
    fig.savefig(output, dpi=180)
    plt.close(fig)


def _report(payload: dict[str, Any], report_path: Path, figure_path: Path) -> str:
    gate = payload["gate"]
    lines = [
        "# Low-Mode / AR Feature-Closure Gate",
        "",
        f"Date: {payload['created_utc']}.",
        "",
        "## Question",
        "",
        "Do low scalar-memory modes form a predictive reduced state, and does",
        "relaxation diffusion add a control-separated, lag-stable mode? The",
        "Fourier basis is computational; a direct finite real-space history is",
        "used as a representation check.",
        "",
        "## Pre-registered controls",
        "",
        "- nu=0 recovers the original spectral exponential memory.",
        "- eta=0 replays identical noise without field feedback.",
        "- Shuffled futures test spurious regression skill.",
        "- Persistence tests whether AR adds more than short-lag continuity.",
        "- 32/64/128 modes and matched-resolution boxes test discretization.",
        "",
        "## Gate result",
        "",
        f"- Direct real-space validation: {gate['direct_real_space_pass']} "
        f"(max scaled error {gate['direct_real_space_max_scaled_error']:.3e}).",
        f"- Resolution control: {gate['resolution_pass']} "
        f"(max relative change {gate['max_resolution_relative_change']:.3e}).",
        f"- Closure gate: {gate['closure_pass']} "
        f"({gate['closure_pass_count']} passing; "
        f"required {gate['closure_required']} of "
        f"{gate['closure_row_count']} rows).",
        f"- Selected diffusion-length ratio: {gate['selected_ratio']:.3g}.",
        f"- Control-separated dominant rate: {gate['control_separation_pass']} "
        f"(fraction {gate['control_separation_fraction']:.3f}).",
        f"- Seed-stable complex rows in selected arm: "
        f"{gate['complex_mode_rows_selected_arm']} "
        f"(eta=0: {gate['eta_zero_complex_rows']}, "
        f"nu=0: {gate['nu_zero_complex_rows']}).",
        f"- Complex-mode lag stability: {gate['complex_stability_pass']} "
        f"(relative MAD {gate['complex_frequency_relative_mad']:.3f}).",
        f"- Candidate omega, Gamma, Q per memory time: "
        f"{gate['complex_frequency_per_memory_time']:.4g}, "
        f"{gate['complex_rate_per_memory_time']:.4g}, "
        f"{gate['complex_quality_factor']:.4g}.",
        f"- Long stability confirmation recommended: "
        f"{gate['long_confirmation_recommended']}.",
        f"- New-mode discovery long run justified: "
        f"{gate['new_mode_discovery_long_run_justified']}.",
        "",
        "The rate comparison is diagnostic. A fitted complex eigenpair is not",
        "called an oscillator unless frequency is seed- and lag-stable and absent",
        "from both controls. Q below 0.5 is a strongly damped transient, not a",
        "persistent wave.",
        "",
        f"![Low-mode AR gate]({_relative(report_path, figure_path)})",
        "",
        "## Low-mode closure by lag",
        "",
        "| ratio | condition | lag / memory time | AR R2 | AR-persistence | "
        "AR-shuffled | closure lift | dominant rate / memory time | frequency |",
        "|---:|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in payload["analyses"]:
        if row["feature_group"] != "low_modes":
            continue
        mode = _dominant_mode(row)
        rate = (
            mode["rate_per_update"] / payload["parameters"]["lambda_value"]
            if mode is not None
            else float("nan")
        )
        frequency = (
            abs(mode["angular_frequency_per_update"])
            / payload["parameters"]["lambda_value"]
            if mode is not None and abs(mode["imag"]) > 1e-6
            else 0.0
        )
        lines.append(
            f"| {row['diffusion_length_ratio']:.1f} | {row['condition']} | "
            f"{row['lag_memory_times']:.2f} | {row['ar_r2_median']:.3f} | "
            f"{row['ar_minus_persistence']:.3f} | "
            f"{row['ar_minus_shuffled']:.3f} | {row['closure_lift']:.3f} | "
            f"{rate:.4g} | {frequency:.4g} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation limits",
            "",
            "- Recovery of the known forgetting/heat decay is implementation",
            "  validation, not emergent physics.",
            "- Closure of selected observables does not prove exact Markov closure.",
            "- The selected positive diffusion ratio is an exploratory short-run",
            "  choice based on candidate-mode stability; it must be frozen before",
            "  any longer confirmation and is not an optimized nu estimate.",
            "- The experiment is one-dimensional and does not establish a knot,",
            "  physical propagation, a photon, or an internal phase degree of freedom.",
            "- Positive heat diffusion has infinite mathematical propagation speed.",
            "",
            "## Reproduction",
            "",
            "Run:",
            "",
            "    python experiments/current/memory/low_mode_ar_feature_closure.py",
            "",
            f"Git revision: {payload['git_revision']}.",
            f"Git status at generation: {payload['git_status'] or 'clean'}.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    _validate_args(args)
    payload = run_probe(args)
    report_path = _resolve(args.report)
    summary_path = _resolve(args.summary_json)
    figure_path = _resolve(args.figure)
    _plot(payload, figure_path)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(_report(payload, report_path, figure_path), encoding="utf-8")
    summary_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True, default=str) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload["gate"], indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
