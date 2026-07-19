from __future__ import annotations

import argparse
from datetime import UTC, datetime
import json
import math
import os
from pathlib import Path
import statistics
import subprocess
import sys
import time
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

from emergenz_knoten.spectral_memory_field import (  # noqa: E402
    SpectralMemoryConfig,
    circular_center,
    evaluate_real_series,
    kernel_integral_coefficient,
    periodic_displacement,
    potential_coefficients,
    potential_gradient,
    zero_mean_attractive_kernel,
)
from emergenz_knoten.spectral_memory_runtime import (  # noqa: E402
    SpectralMemoryOperators,
)


def _parse_int_list(value: str) -> list[int]:
    values = [int(item.strip()) for item in value.split(",") if item.strip()]
    if not values or any(item < 0 for item in values):
        raise argparse.ArgumentTypeError("expected non-negative comma-separated integers")
    return values


def _parse_float_list(value: str) -> list[float]:
    values = [float(item.strip()) for item in value.split(",") if item.strip()]
    if not values or any(not math.isfinite(item) or item <= 0.0 for item in values):
        raise argparse.ArgumentTypeError("expected positive comma-separated numbers")
    return values


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Resource-bounded one-dimensional Fourier-field pilot with paired "
            "eta=0 controls. This tests a representation, not a new field law."
        )
    )
    parser.add_argument("--steps", type=int, default=50_000)
    parser.add_argument("--burn-in", type=int, default=5_000)
    parser.add_argument("--sample-every", type=int, default=25)
    parser.add_argument(
        "--seeds",
        type=_parse_int_list,
        default=_parse_int_list("1,2,3,4,5"),
    )
    parser.add_argument(
        "--epsilon",
        type=_parse_float_list,
        default=_parse_float_list("1e-8,1e-6,1e-4"),
    )
    parser.add_argument("--eta", type=float, default=0.15)
    parser.add_argument("--lambda-value", type=float, default=0.01)
    parser.add_argument("--memory-mass", type=float, default=1.0)
    parser.add_argument("--box-length", type=float, default=80.0)
    parser.add_argument("--n-modes", type=int, default=64)
    parser.add_argument("--deposition-sigma", type=float, default=0.0)
    parser.add_argument("--amplitude-att", type=float, default=26.0)
    parser.add_argument("--sigma-att", type=float, default=3.0)
    parser.add_argument("--sigma-comp", type=float, default=10.0)
    parser.add_argument(
        "--convergence-modes",
        type=_parse_int_list,
        default=_parse_int_list("32,64,128"),
    )
    parser.add_argument("--grid-points", type=int, default=801)
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("reports/memory/spectral_rho_field_pilot_2026-07-19.md"),
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=Path("reports/memory/spectral_rho_field_pilot_2026-07-19.json"),
    )
    parser.add_argument(
        "--metrics-figure",
        type=Path,
        default=Path("figures/draft/memory/spectral_rho_epsilon_pilot_2026-07-19.png"),
    )
    parser.add_argument(
        "--field-figure",
        type=Path,
        default=Path("figures/draft/memory/spectral_rho_field_snapshot_2026-07-19.png"),
    )
    return parser.parse_args()


def _validate_args(args: argparse.Namespace) -> None:
    if args.steps < 1 or args.sample_every < 1:
        raise SystemExit("--steps and --sample-every must be positive")
    if not 0 <= args.burn_in < args.steps:
        raise SystemExit("--burn-in must satisfy 0 <= burn_in < steps")
    if args.n_modes < 1 or any(mode < 1 for mode in args.convergence_modes):
        raise SystemExit("mode counts must be positive")
    if args.grid_points < 101:
        raise SystemExit("--grid-points must be at least 101")
    if args.eta <= 0.0 or not math.isfinite(args.eta):
        raise SystemExit("--eta must be positive and finite")
    if not 0.0 < args.lambda_value <= 1.0:
        raise SystemExit("--lambda-value must lie in (0,1]")
    for name in (
        "memory_mass",
        "box_length",
        "amplitude_att",
        "sigma_att",
        "sigma_comp",
    ):
        if getattr(args, name) <= 0.0 or not math.isfinite(getattr(args, name)):
            raise SystemExit(f"--{name.replace('_', '-')} must be positive and finite")


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def _rel_from(source: Path, target: Path) -> str:
    return Path(os.path.relpath(target.resolve(), source.resolve().parent)).as_posix()


def _utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def _git_output(args: list[str]) -> str:
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=ROOT,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except (OSError, subprocess.CalledProcessError):
        return "unavailable"
    return completed.stdout.strip()


def _config(args: argparse.Namespace, *, n_modes: int) -> SpectralMemoryConfig:
    return SpectralMemoryConfig(
        box_length=float(args.box_length),
        n_modes=int(n_modes),
        lambda_value=float(args.lambda_value),
        memory_mass=float(args.memory_mass),
        deposition_sigma=float(args.deposition_sigma),
        kernel=zero_mean_attractive_kernel(
            amplitude_att=float(args.amplitude_att),
            sigma_att=float(args.sigma_att),
            sigma_comp=float(args.sigma_comp),
        ),
    )


def _quantile(values: list[float], probability: float) -> float:
    return float(np.quantile(np.asarray(values, dtype=float), probability))


def run_case(
    args: argparse.Namespace,
    *,
    epsilon: float,
    eta: float,
    seed: int,
    n_modes: int,
    noise: np.ndarray,
    keep_snapshot: bool = False,
) -> tuple[dict[str, Any], dict[str, np.ndarray] | None]:
    config = _config(args, n_modes=n_modes)
    operators = SpectralMemoryOperators(config)
    x = 0.5 * config.box_length
    rho = operators.deposition(x)
    initial_x = x
    unwrapped_x = x
    relative_positions: list[float] = []
    forces: list[float] = []
    unwrapped_samples: list[float] = []
    started = time.perf_counter()

    for update_index, noise_value in enumerate(noise, start=1):
        gradient = operators.gradient(rho, x=x)
        x_new = float(
            (
                x
                + float(epsilon) * float(noise_value)
                - float(eta) * gradient
            )
            % config.box_length
        )
        unwrapped_x += periodic_displacement(x_new, x, config.box_length)
        x = x_new
        rho = operators.update_rho(rho, deposited_at=x)
        if update_index > args.burn_in and update_index % args.sample_every == 0:
            center = circular_center(config, rho)
            if center is None:
                raise RuntimeError("first Fourier mode vanished; center is undefined")
            relative_positions.append(
                periodic_displacement(x, center, config.box_length)
            )
            forces.append(gradient)
            unwrapped_samples.append(unwrapped_x)

    elapsed = time.perf_counter() - started
    relative = np.asarray(relative_positions, dtype=float)
    force_values = np.asarray(forces, dtype=float)
    unwrapped_values = np.asarray(unwrapped_samples, dtype=float)
    expected_eta_zero = initial_x + epsilon * float(np.sum(noise))
    rho_energy = float(np.sum(np.abs(rho[1:]) ** 2))
    tail_start = max(1, int(math.ceil(0.75 * rho.size)))
    tail_energy = float(np.sum(np.abs(rho[tail_start:]) ** 2))
    mass_error = abs(config.box_length * float(rho[0].real) - config.memory_mass)
    radius = float(np.sqrt(np.mean(relative**2)))
    force_rms = float(np.sqrt(np.mean(force_values**2)))
    row: dict[str, Any] = {
        "epsilon": float(epsilon),
        "eta": float(eta),
        "condition": "active" if eta > 0.0 else "eta_zero",
        "seed": int(seed),
        "n_modes": int(n_modes),
        "sample_count": int(relative.size),
        "relative_radius_rms": radius,
        "relative_radius_q95": _quantile(np.abs(relative).tolist(), 0.95),
        "relative_radius_over_epsilon": radius / epsilon,
        "force_rms": force_rms,
        "feedback_step_rms_over_epsilon": eta * force_rms / epsilon,
        "unwrapped_path_span": float(np.ptp(unwrapped_values)),
        "final_unwrapped_displacement": float(unwrapped_x - initial_x),
        "eta_zero_random_walk_error": (
            abs(unwrapped_x - expected_eta_zero) if eta == 0.0 else None
        ),
        "memory_mass_absolute_error": mass_error,
        "spectral_tail_energy_fraction": tail_energy / rho_energy if rho_energy else 0.0,
        "state_bytes": operators.state_bytes,
        "runtime_seconds": elapsed,
        "updates_per_second": args.steps / elapsed,
    }

    snapshot = None
    if keep_snapshot:
        center = circular_center(config, rho)
        if center is None:
            raise RuntimeError("first Fourier mode vanished; center is undefined")
        offsets = np.linspace(
            -0.5 * config.box_length,
            0.5 * config.box_length,
            args.grid_points,
        )
        coordinates = (center + offsets) % config.box_length
        phi = potential_coefficients(config, rho)
        rho_grid = np.asarray(
            [
                evaluate_real_series(
                    rho,
                    x=float(coordinate),
                    box_length=config.box_length,
                )
                for coordinate in coordinates
            ],
            dtype=float,
        )
        phi_grid = np.asarray(
            [
                evaluate_real_series(
                    phi,
                    x=float(coordinate),
                    box_length=config.box_length,
                )
                for coordinate in coordinates
            ],
            dtype=float,
        )
        force_grid = np.asarray(
            [
                -eta
                * potential_gradient(
                    config,
                    rho,
                    x=float(coordinate),
                )
                for coordinate in coordinates
            ],
            dtype=float,
        )
        dx = float(offsets[1] - offsets[0])
        row["reconstructed_rho_min"] = float(np.min(rho_grid))
        row["reconstructed_negative_mass"] = float(
            np.sum(np.maximum(-rho_grid, 0.0)) * dx
        )
        snapshot = {
            "offset": offsets,
            "rho": rho_grid,
            "potential": phi_grid,
            "force": force_grid,
            "particle_offset": np.asarray(
                [periodic_displacement(x, center, config.box_length)]
            ),
        }
    return row, snapshot


def _median_rows(rows: list[dict[str, Any]], *, condition: str) -> list[dict[str, float]]:
    summary: list[dict[str, float]] = []
    epsilons = sorted({float(row["epsilon"]) for row in rows})
    for epsilon in epsilons:
        selected = [
            row
            for row in rows
            if row["condition"] == condition and row["epsilon"] == epsilon
        ]
        summary.append(
            {
                "epsilon": epsilon,
                "radius_median": statistics.median(
                    row["relative_radius_rms"] for row in selected
                ),
                "radius_over_epsilon_median": statistics.median(
                    row["relative_radius_over_epsilon"] for row in selected
                ),
                "feedback_over_epsilon_median": statistics.median(
                    row["feedback_step_rms_over_epsilon"] for row in selected
                ),
            }
        )
    return summary


def _build_payload(args: argparse.Namespace) -> tuple[dict[str, Any], dict[str, np.ndarray]]:
    rows: list[dict[str, Any]] = []
    primary_snapshot: dict[str, np.ndarray] | None = None
    max_epsilon = max(args.epsilon)
    first_seed = args.seeds[0]
    noise_by_seed = {
        seed: np.random.default_rng(seed).normal(size=args.steps) for seed in args.seeds
    }

    for epsilon in sorted(args.epsilon):
        for seed in args.seeds:
            noise = noise_by_seed[seed]
            for eta in (0.0, float(args.eta)):
                keep_snapshot = (
                    epsilon == max_epsilon
                    and seed == first_seed
                    and eta == float(args.eta)
                )
                row, snapshot = run_case(
                    args,
                    epsilon=float(epsilon),
                    eta=eta,
                    seed=seed,
                    n_modes=args.n_modes,
                    noise=noise,
                    keep_snapshot=keep_snapshot,
                )
                rows.append(row)
                if snapshot is not None:
                    primary_snapshot = snapshot

    convergence: list[dict[str, Any]] = []
    noise = noise_by_seed[first_seed]
    for n_modes in sorted(set(args.convergence_modes)):
        row, _ = run_case(
            args,
            epsilon=float(max_epsilon),
            eta=float(args.eta),
            seed=first_seed,
            n_modes=int(n_modes),
            noise=noise,
        )
        convergence.append(row)

    active_summary = _median_rows(rows, condition="active")
    control_summary = _median_rows(rows, condition="eta_zero")
    log_epsilon = np.log([row["epsilon"] for row in active_summary])
    log_radius = np.log([row["radius_median"] for row in active_summary])
    epsilon_slope = float(np.polyfit(log_epsilon, log_radius, 1)[0])
    normalized = [row["radius_over_epsilon_median"] for row in active_summary]
    normalized_spread = float(max(normalized) / min(normalized) - 1.0)
    consistent_linear = abs(epsilon_slope - 1.0) <= 0.05 and normalized_spread <= 0.10
    pair_ratios: list[dict[str, float | int]] = []
    for epsilon in sorted(args.epsilon):
        for seed in args.seeds:
            active = next(
                row
                for row in rows
                if row["epsilon"] == epsilon
                and row["seed"] == seed
                and row["condition"] == "active"
            )
            control = next(
                row
                for row in rows
                if row["epsilon"] == epsilon
                and row["seed"] == seed
                and row["condition"] == "eta_zero"
            )
            pair_ratios.append(
                {
                    "epsilon": float(epsilon),
                    "seed": int(seed),
                    "active_over_control_radius": float(
                        active["relative_radius_rms"]
                        / control["relative_radius_rms"]
                    ),
                }
            )

    reference = convergence[-1]
    convergence_summary = []
    for row in convergence:
        convergence_summary.append(
            {
                **row,
                "radius_relative_to_highest_mode": float(
                    row["relative_radius_rms"] / reference["relative_radius_rms"]
                ),
            }
        )

    if primary_snapshot is None:
        raise RuntimeError("primary snapshot was not generated")
    payload = {
        "description": "Resource-bounded spectral scalar-memory field pilot.",
        "created_utc": _utc_now(),
        "git_revision": _git_output(["rev-parse", "HEAD"]),
        "git_status": _git_output(["status", "--short"]),
        "parameters": {
            key: (str(value) if isinstance(value, Path) else value)
            for key, value in vars(args).items()
        },
        "kernel_integral_coefficient": kernel_integral_coefficient(
            _config(args, n_modes=args.n_modes)
        ),
        "rows": rows,
        "active_summary": active_summary,
        "eta_zero_summary": control_summary,
        "paired_radius_ratios": pair_ratios,
        "epsilon_scaling": {
            "active_log_log_slope": epsilon_slope,
            "active_normalized_radius_relative_spread": normalized_spread,
            "consistent_with_linear_scaling_gate": consistent_linear,
        },
        "mode_convergence": convergence_summary,
        "max_eta_zero_random_walk_error": max(
            float(row["eta_zero_random_walk_error"])
            for row in rows
            if row["condition"] == "eta_zero"
        ),
    }
    return payload, primary_snapshot


def _plot_metrics(
    payload: dict[str, Any],
    output: Path,
) -> None:
    rows = payload["rows"]
    active = payload["active_summary"]
    control = payload["eta_zero_summary"]
    eps = np.asarray([row["epsilon"] for row in active], dtype=float)
    active_radius = np.asarray([row["radius_median"] for row in active], dtype=float)
    control_radius = np.asarray([row["radius_median"] for row in control], dtype=float)

    fig, axes = plt.subplots(2, 2, figsize=(10.5, 7.4), constrained_layout=True)
    ax = axes[0, 0]
    ax.loglog(eps, active_radius, "o-", label="active")
    ax.loglog(eps, control_radius, "s--", label=r"$\eta=0$")
    reference = active_radius[-1] * eps / eps[-1]
    ax.loglog(eps, reference, ":", color="0.35", label="slope 1")
    ax.set(xlabel=r"$\epsilon$", ylabel="RMS distance to memory center")
    ax.legend(frameon=False)

    ax = axes[0, 1]
    for condition, marker, color in (
        ("active", "o", "tab:blue"),
        ("eta_zero", "s", "tab:orange"),
    ):
        selected = [row for row in rows if row["condition"] == condition]
        ax.scatter(
            [row["epsilon"] for row in selected],
            [row["relative_radius_over_epsilon"] for row in selected],
            marker=marker,
            color=color,
            alpha=0.7,
            label=condition,
        )
    ax.set_xscale("log")
    ax.set(xlabel=r"$\epsilon$", ylabel=r"RMS radius / $\epsilon$")
    ax.legend(frameon=False)

    ax = axes[1, 0]
    paired = payload["paired_radius_ratios"]
    for seed in sorted({row["seed"] for row in paired}):
        selected = [row for row in paired if row["seed"] == seed]
        ax.semilogx(
            [row["epsilon"] for row in selected],
            [row["active_over_control_radius"] for row in selected],
            "o-",
            alpha=0.7,
            label=f"seed {seed}",
        )
    ax.axhline(1.0, color="0.35", linestyle=":")
    ax.set(xlabel=r"$\epsilon$", ylabel=r"active radius / $\eta=0$ radius")
    ax.legend(frameon=False, ncol=2, fontsize=8)

    ax = axes[1, 1]
    convergence = payload["mode_convergence"]
    relative_error_units = [
        (row["radius_relative_to_highest_mode"] - 1.0) * 1e14
        for row in convergence
    ]
    ax.plot(
        [row["n_modes"] for row in convergence],
        relative_error_units,
        "o-",
    )
    ax.axhline(0.0, color="0.35", linestyle=":")
    ax.set(
        xlabel="retained positive Fourier modes",
        ylabel=r"relative radius difference ($10^{-14}$)",
    )
    ax.set_xscale("log", base=2)
    ax.set_xticks([row["n_modes"] for row in convergence])
    ax.set_xticklabels([str(row["n_modes"]) for row in convergence])

    fig.suptitle("Spectral rho pilot: epsilon scaling and representation gate")
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=180)
    plt.close(fig)


def _plot_field(
    args: argparse.Namespace,
    snapshot: dict[str, np.ndarray],
    output: Path,
) -> None:
    fig, axes = plt.subplots(3, 1, figsize=(9.5, 7.8), sharex=True, constrained_layout=True)
    offset = snapshot["offset"]
    particle = float(snapshot["particle_offset"][0])
    for ax in axes:
        ax.axvline(0.0, color="0.45", linestyle=":", label="memory center")
        ax.axvline(particle, color="tab:red", linestyle="--", label="particle")
    axes[0].plot(offset, snapshot["rho"], color="tab:blue")
    axes[0].set_ylabel(r"truncated $\rho(x)$")
    axes[1].plot(offset, snapshot["potential"], color="tab:purple")
    axes[1].set_ylabel(r"$\Phi(x)$")
    axes[2].plot(offset, snapshot["force"], color="tab:green")
    axes[2].axhline(0.0, color="0.6", linewidth=0.8)
    axes[2].set(xlabel="periodic displacement", ylabel=r"$-\eta\,\partial_x\Phi$")
    axes[0].legend(frameon=False, ncol=2)
    fig.suptitle(
        f"Band-limited field snapshot, M={args.n_modes}, epsilon={max(args.epsilon):.0e}"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=180)
    plt.close(fig)


def _fmt(value: float, digits: int = 5) -> str:
    return f"`{value:.{digits}g}`"


def _build_report(
    args: argparse.Namespace,
    payload: dict[str, Any],
    report: Path,
    summary_json: Path,
    metrics_figure: Path,
    field_figure: Path,
) -> str:
    scaling = payload["epsilon_scaling"]
    lines = [
        "# Spectral rho Field Pilot",
        "",
        f"Date: {payload['created_utc']}.",
        "",
        "## Scope",
        "",
        "This is a one-dimensional representation and numerical-identification gate.",
        "It rewrites the existing exponentially weighted scalar memory in a finite",
        "Fourier basis. It does **not** introduce a new field equation, finite signal",
        "speed, vector memory, or a particle/space-dimension claim.",
        "",
        "The compensated kernel has zero spatial integral (`K_hat(0)=0`). This removes",
        "the constant potential mode but is not an energy-conservation law. Because the",
        "trajectory responds to the potential gradient, any constant mode is dynamically",
        "unobservable even without this constraint.",
        "",
        f"![Epsilon and mode diagnostics]({_rel_from(report, metrics_figure)})",
        "",
        f"![Final spectral field snapshot]({_rel_from(report, field_figure)})",
        "",
        "## Fixed Design",
        "",
        f"- updates: `{args.steps}`; burn-in cut: `{args.burn_in}`; seeds: `{args.seeds}`",
        f"- epsilon: `{args.epsilon}`; active eta: `{args.eta}`; paired control: `eta=0`",
        f"- lambda: `{args.lambda_value}`; M0: `{args.memory_mass}`",
        f"- box length: `{args.box_length}`; primary modes: `{args.n_modes}`",
        f"- mode gate: `{args.convergence_modes}`; deposition sigma: `{args.deposition_sigma}`",
        f"- kernel: `-A_att G_sigma_att + A_comp G_sigma_comp` with "
        f"`A_att={args.amplitude_att}`, `sigma_att={args.sigma_att}`, "
        f"`sigma_comp={args.sigma_comp}` and exact 1D zero integral",
        f"- one field state uses `{payload['rows'][0]['state_bytes']}` bytes at the primary mode count",
        "",
        "## Epsilon Scaling",
        "",
        "| epsilon | active radius median | eta=0 radius median | active radius/epsilon | feedback step/epsilon |",
        "| ---: | ---: | ---: | ---: | ---: |",
    ]
    for active, control in zip(
        payload["active_summary"],
        payload["eta_zero_summary"],
        strict=True,
    ):
        lines.append(
            f"| {_fmt(active['epsilon'])} | {_fmt(active['radius_median'])} | "
            f"{_fmt(control['radius_median'])} | "
            f"{_fmt(active['radius_over_epsilon_median'])} | "
            f"{_fmt(active['feedback_over_epsilon_median'])} |"
        )
    lines.extend(
        [
            "",
            f"Active log-log radius slope: {_fmt(scaling['active_log_log_slope'])}.",
            f"Spread of the median normalized radius: {_fmt(scaling['active_normalized_radius_relative_spread'])}.",
            f"Predefined linear-scaling gate: `{scaling['consistent_with_linear_scaling_gate']}`.",
            "",
            "## Mode Convergence",
            "",
            "| modes | state bytes | radius | radius/highest-mode radius | tail energy fraction |",
            "| ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in payload["mode_convergence"]:
        lines.append(
            f"| `{row['n_modes']}` | `{row['state_bytes']}` | "
            f"{_fmt(row['relative_radius_rms'])} | "
            f"{_fmt(row['radius_relative_to_highest_mode'])} | "
            f"{_fmt(row['spectral_tail_energy_fraction'])} |"
        )
    primary = next(
        row
        for row in payload["rows"]
        if row["condition"] == "active"
        and row["epsilon"] == max(args.epsilon)
        and row["seed"] == args.seeds[0]
    )
    lines.extend(
        [
            "",
            "## Validation and Reading",
            "",
            f"- kernel integral coefficient: {_fmt(payload['kernel_integral_coefficient'])}",
            f"- maximum eta=0 random-walk replay error: {_fmt(payload['max_eta_zero_random_walk_error'])}",
            f"- maximum primary memory-mass error: {_fmt(max(row['memory_mass_absolute_error'] for row in payload['rows']))}",
            f"- primary truncated-field minimum: {_fmt(primary['reconstructed_rho_min'])}",
            f"- primary reconstructed negative mass: {_fmt(primary['reconstructed_negative_mass'])}",
            "",
            "A negative pointwise reconstructed rho is expected for a sharply deposited",
            "delta represented by finitely many Fourier modes. The underlying memory",
            "measure remains non-negative and normalized; only the band-limited pointwise",
            "reconstruction has Gibbs lobes. Force convergence, rather than pointwise",
            "positivity of this delta reconstruction, is the relevant representation gate.",
            "",
            "If the linear-scaling gate passes, lowering epsilon further has not revealed",
            "a new intrinsic length in this slice. It only scales the same local stochastic",
            "response. That is a stopping rule for the epsilon axis, not evidence against",
            "the existence of scalar feedback confinement at other dimensionless ratios.",
            "",
            "## Artifacts",
            "",
            f"- machine-readable summary: [{summary_json.name}]({_rel_from(report, summary_json)})",
            f"- git revision before generated artifacts: `{payload['git_revision']}`",
            f"- recorded worktree status: `{payload['git_status'] or 'clean'}`",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    args = parse_args()
    _validate_args(args)
    payload, snapshot = _build_payload(args)
    report = _resolve(args.report)
    summary_json = _resolve(args.summary_json)
    metrics_figure = _resolve(args.metrics_figure)
    field_figure = _resolve(args.field_figure)
    _plot_metrics(payload, metrics_figure)
    _plot_field(args, snapshot, field_figure)
    summary_json.parent.mkdir(parents=True, exist_ok=True)
    summary_json.write_text(
        json.dumps(payload, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(
        _build_report(
            args,
            payload,
            report,
            summary_json,
            metrics_figure,
            field_figure,
        ),
        encoding="utf-8",
    )
    print(f"wrote {report}")
    print(f"wrote {summary_json}")
    print(f"wrote {metrics_figure}")
    print(f"wrote {field_figure}")


if __name__ == "__main__":
    main()
