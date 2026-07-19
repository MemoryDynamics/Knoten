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

from emergenz_knoten.relaxation_diffusion_memory import (  # noqa: E402
    RelaxationDiffusionMemoryOperators,
)
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


def _parse_int_list(value: str) -> list[int]:
    values = [int(item.strip()) for item in value.split(",") if item.strip()]
    if not values or any(item < 0 for item in values):
        raise argparse.ArgumentTypeError("expected non-negative comma-separated integers")
    return values


def _parse_nonnegative_float_list(value: str) -> list[float]:
    values = [float(item.strip()) for item in value.split(",") if item.strip()]
    if not values or any(not math.isfinite(item) or item < 0.0 for item in values):
        raise argparse.ArgumentTypeError("expected non-negative comma-separated numbers")
    return values


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Controlled spectral relaxation-diffusion memory pilot. The zero-"
            "diffusion arm exactly recovers exponential memory."
        )
    )
    parser.add_argument("--steps", type=int, default=20_000)
    parser.add_argument("--burn-in", type=int, default=2_000)
    parser.add_argument("--sample-every", type=int, default=20)
    parser.add_argument(
        "--seeds",
        type=_parse_int_list,
        default=_parse_int_list("1,2,3,4,5"),
    )
    parser.add_argument(
        "--diffusion-length-ratios",
        type=_parse_nonnegative_float_list,
        default=_parse_nonnegative_float_list("0,0.3,1.0"),
        help="Heat RMS length per memory time divided by sigma_att.",
    )
    parser.add_argument("--epsilon", type=float, default=1e-4)
    parser.add_argument("--eta", type=float, default=0.15)
    parser.add_argument("--lambda-value", type=float, default=0.01)
    parser.add_argument("--memory-mass", type=float, default=1.0)
    parser.add_argument("--box-length", type=float, default=80.0)
    parser.add_argument("--n-modes", type=int, default=64)
    parser.add_argument("--deposition-sigma", type=float, default=0.0)
    parser.add_argument("--amplitude-att", type=float, default=26.0)
    parser.add_argument("--sigma-att", type=float, default=3.0)
    parser.add_argument("--sigma-comp", type=float, default=10.0)
    parser.add_argument("--grid-points", type=int, default=801)
    parser.add_argument(
        "--report",
        type=Path,
        default=Path(
            "reports/memory/relaxation_diffusion_field_pilot_2026-07-19.md"
        ),
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=Path(
            "reports/memory/relaxation_diffusion_field_pilot_2026-07-19.json"
        ),
    )
    parser.add_argument(
        "--figure",
        type=Path,
        default=Path(
            "figures/draft/memory/relaxation_diffusion_field_pilot_2026-07-19.png"
        ),
    )
    return parser.parse_args()


def _validate_args(args: argparse.Namespace) -> None:
    if args.steps < 1 or args.sample_every < 1:
        raise SystemExit("--steps and --sample-every must be positive")
    if not 0 <= args.burn_in < args.steps:
        raise SystemExit("--burn-in must satisfy 0 <= burn_in < steps")
    if args.n_modes < 1 or args.grid_points < 101:
        raise SystemExit("--n-modes must be positive and --grid-points >= 101")
    if 0.0 not in args.diffusion_length_ratios:
        raise SystemExit("--diffusion-length-ratios must include the zero control")
    if len(set(args.diffusion_length_ratios)) != len(args.diffusion_length_ratios):
        raise SystemExit("diffusion-length ratios must not contain duplicates")
    for name in (
        "epsilon",
        "eta",
        "memory_mass",
        "box_length",
        "amplitude_att",
        "sigma_att",
        "sigma_comp",
    ):
        value = float(getattr(args, name))
        if value <= 0.0 or not math.isfinite(value):
            raise SystemExit(f"--{name.replace('_', '-')} must be positive and finite")
    if not 0.0 < args.lambda_value <= 1.0:
        raise SystemExit("--lambda-value must lie in (0,1]")


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def _rel_from(source: Path, target: Path) -> str:
    return Path(os.path.relpath(target.resolve(), source.resolve().parent)).as_posix()


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


def _config(args: argparse.Namespace) -> SpectralMemoryConfig:
    return SpectralMemoryConfig(
        box_length=float(args.box_length),
        n_modes=int(args.n_modes),
        lambda_value=float(args.lambda_value),
        memory_mass=float(args.memory_mass),
        deposition_sigma=float(args.deposition_sigma),
        kernel=zero_mean_attractive_kernel(
            amplitude_att=float(args.amplitude_att),
            sigma_att=float(args.sigma_att),
            sigma_comp=float(args.sigma_comp),
        ),
    )


def diffusion_per_update(args: argparse.Namespace, ratio: float) -> float:
    """Map a memory-time heat RMS ratio to the per-update heat parameter."""

    length = float(ratio) * float(args.sigma_att)
    return float(0.5 * args.lambda_value * length**2)


def run_case(
    args: argparse.Namespace,
    *,
    diffusion_length_ratio: float,
    eta: float,
    seed: int,
    noise: np.ndarray,
    keep_profile: bool = False,
) -> tuple[dict[str, Any], dict[str, np.ndarray] | None]:
    config = _config(args)
    nu = diffusion_per_update(args, diffusion_length_ratio)
    operators = RelaxationDiffusionMemoryOperators(
        config,
        diffusion_per_update=nu,
    )
    x = 0.5 * config.box_length
    initial_x = x
    unwrapped_x = x
    rho = operators.deposition(x)
    relative_positions: list[float] = []
    forces: list[float] = []
    started = time.perf_counter()

    for update_index, noise_value in enumerate(noise, start=1):
        gradient = operators.gradient(rho, x=x)
        x_new = float(
            (x + args.epsilon * float(noise_value) - eta * gradient)
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

    elapsed = time.perf_counter() - started
    relative = np.asarray(relative_positions, dtype=float)
    force_values = np.asarray(forces, dtype=float)
    radius = float(np.sqrt(np.mean(relative**2)))
    force_rms = float(np.sqrt(np.mean(force_values**2)))
    expected_eta_zero = initial_x + args.epsilon * float(np.sum(noise))
    row: dict[str, Any] = {
        "diffusion_length_ratio": float(diffusion_length_ratio),
        "diffusion_per_update": nu,
        "diffusion_length_per_memory_time": (
            operators.diffusion_length_per_memory_time
        ),
        "condition": "active" if eta > 0.0 else "eta_zero",
        "eta": float(eta),
        "seed": int(seed),
        "relative_radius_rms": radius,
        "relative_radius_over_epsilon": radius / args.epsilon,
        "force_rms": force_rms,
        "feedback_step_rms_over_epsilon": eta * force_rms / args.epsilon,
        "final_unwrapped_displacement": float(unwrapped_x - initial_x),
        "eta_zero_random_walk_error": (
            abs(unwrapped_x - expected_eta_zero) if eta == 0.0 else None
        ),
        "memory_mass_absolute_error": abs(
            config.box_length * float(rho[0].real) - config.memory_mass
        ),
        "runtime_seconds": elapsed,
        "updates_per_second": args.steps / elapsed,
        "state_bytes": operators.state_bytes,
    }

    profile = None
    if keep_profile:
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
            ]
        )
        phi_grid = np.asarray(
            [
                evaluate_real_series(
                    phi,
                    x=float(coordinate),
                    box_length=config.box_length,
                )
                for coordinate in coordinates
            ]
        )
        force_grid = np.asarray(
            [
                -eta * potential_gradient(config, rho, x=float(coordinate))
                for coordinate in coordinates
            ]
        )
        dx = float(offsets[1] - offsets[0])
        row["reconstructed_rho_min"] = float(np.min(rho_grid))
        row["reconstructed_negative_mass"] = float(
            np.sum(np.maximum(-rho_grid, 0.0)) * dx
        )
        profile = {
            "offset": offsets,
            "rho": rho_grid,
            "potential": phi_grid,
            "force": force_grid,
        }
    return row, profile


def _median_summary(rows: list[dict[str, Any]]) -> list[dict[str, float]]:
    summary: list[dict[str, float]] = []
    ratios = sorted({float(row["diffusion_length_ratio"]) for row in rows})
    for ratio in ratios:
        active = [
            row
            for row in rows
            if row["diffusion_length_ratio"] == ratio
            and row["condition"] == "active"
        ]
        control = [
            row
            for row in rows
            if row["diffusion_length_ratio"] == ratio
            and row["condition"] == "eta_zero"
        ]
        pair_ratios = [
            next(row for row in active if row["seed"] == seed)[
                "relative_radius_rms"
            ]
            / next(row for row in control if row["seed"] == seed)[
                "relative_radius_rms"
            ]
            for seed in sorted({row["seed"] for row in active})
        ]
        summary.append(
            {
                "diffusion_length_ratio": ratio,
                "diffusion_per_update": active[0]["diffusion_per_update"],
                "active_radius_median": statistics.median(
                    row["relative_radius_rms"] for row in active
                ),
                "eta_zero_radius_median": statistics.median(
                    row["relative_radius_rms"] for row in control
                ),
                "active_over_control_radius_median": statistics.median(
                    pair_ratios
                ),
                "active_over_control_radius_min": min(pair_ratios),
                "active_over_control_radius_max": max(pair_ratios),
                "feedback_over_epsilon_median": statistics.median(
                    row["feedback_step_rms_over_epsilon"] for row in active
                ),
            }
        )
    return summary


def run_pilot(
    args: argparse.Namespace,
) -> tuple[dict[str, Any], dict[float, dict[str, np.ndarray]]]:
    rows: list[dict[str, Any]] = []
    profiles: dict[float, dict[str, np.ndarray]] = {}
    first_seed = args.seeds[0]
    for seed in args.seeds:
        noise = np.random.default_rng(seed).normal(size=args.steps)
        for ratio in sorted(args.diffusion_length_ratios):
            for eta in (0.0, float(args.eta)):
                row, profile = run_case(
                    args,
                    diffusion_length_ratio=float(ratio),
                    eta=eta,
                    seed=seed,
                    noise=noise,
                    keep_profile=(seed == first_seed and eta == float(args.eta)),
                )
                rows.append(row)
                if profile is not None:
                    profiles[float(ratio)] = profile
    summary = _median_summary(rows)
    zero = next(row for row in summary if row["diffusion_length_ratio"] == 0.0)
    largest = summary[-1]
    payload = {
        "description": "Controlled spectral relaxation-diffusion field pilot.",
        "created_utc": datetime.now(UTC).isoformat(timespec="seconds").replace(
            "+00:00", "Z"
        ),
        "git_revision": _git_output(["rev-parse", "HEAD"]),
        "git_status": _git_output(["status", "--short"]),
        "parameters": {
            key: (str(value) if isinstance(value, Path) else value)
            for key, value in vars(args).items()
        },
        "kernel_integral_coefficient": kernel_integral_coefficient(_config(args)),
        "rows": rows,
        "summary": summary,
        "largest_over_zero_active_radius": float(
            largest["active_radius_median"] / zero["active_radius_median"]
        ),
        "largest_over_zero_confinement_ratio": float(
            largest["active_over_control_radius_median"]
            / zero["active_over_control_radius_median"]
        ),
        "max_eta_zero_random_walk_error": max(
            float(row["eta_zero_random_walk_error"])
            for row in rows
            if row["condition"] == "eta_zero"
        ),
        "max_memory_mass_absolute_error": max(
            float(row["memory_mass_absolute_error"]) for row in rows
        ),
    }
    return payload, profiles


def plot_results(
    payload: dict[str, Any],
    profiles: dict[float, dict[str, np.ndarray]],
    output: Path,
) -> None:
    summary = payload["summary"]
    ratios = [row["diffusion_length_ratio"] for row in summary]
    fig, axes = plt.subplots(2, 2, figsize=(10.5, 7.5), constrained_layout=True)

    axes[0, 0].plot(
        ratios,
        [row["active_radius_median"] for row in summary],
        "o-",
        label="active",
    )
    axes[0, 0].plot(
        ratios,
        [row["eta_zero_radius_median"] for row in summary],
        "s--",
        label=r"$\eta=0$",
    )
    axes[0, 0].set(
        xlabel=r"diffusion length per memory time / $L$",
        ylabel="RMS distance to field center",
    )
    axes[0, 0].legend(frameon=False)

    axes[0, 1].errorbar(
        ratios,
        [row["active_over_control_radius_median"] for row in summary],
        yerr=[
            [
                row["active_over_control_radius_median"]
                - row["active_over_control_radius_min"]
                for row in summary
            ],
            [
                row["active_over_control_radius_max"]
                - row["active_over_control_radius_median"]
                for row in summary
            ],
        ],
        fmt="o-",
        capsize=4,
    )
    axes[0, 1].axhline(1.0, color="0.4", linestyle=":")
    axes[0, 1].set(
        xlabel=r"diffusion length per memory time / $L$",
        ylabel=r"active radius / $\eta=0$ radius",
    )

    for ratio, profile in sorted(profiles.items()):
        axes[1, 0].plot(
            profile["offset"],
            profile["rho"],
            label=f"{ratio:g} L",
        )
        axes[1, 1].plot(
            profile["offset"],
            profile["force"],
            label=f"{ratio:g} L",
        )
    axes[1, 0].set(xlabel="displacement", ylabel=r"truncated $\rho(x)$")
    axes[1, 1].set(xlabel="displacement", ylabel=r"$-\eta\,\partial_x\Phi$")
    axes[1, 0].legend(frameon=False, title="diffusion RMS")
    axes[1, 1].legend(frameon=False, title="diffusion RMS")
    fig.suptitle("Relaxation-diffusion memory: one controlled model axis")
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=180)
    plt.close(fig)


def _fmt(value: float, digits: int = 5) -> str:
    return f"`{value:.{digits}g}`"


def build_report(
    args: argparse.Namespace,
    payload: dict[str, Any],
    report: Path,
    summary_json: Path,
    figure: Path,
) -> str:
    lines = [
        "# Relaxation-Diffusion Memory Field Pilot",
        "",
        f"Date: {payload['created_utc']}.",
        "",
        "## Scope",
        "",
        "This pilot changes one mechanism relative to exponential scalar memory:",
        "after forgetting and deposition, the memory field undergoes one exact",
        "heat-semigroup step. In Fourier space the update is",
        "",
        "```text",
        "rho_new_hat(k) = exp(-nu k^2) [(1-lambda) rho_hat(k) + lambda G_hat_x(k)].",
        "```",
        "",
        "The `nu=0` arm is exactly the previous model. Positive `nu` is a model",
        "extension, not a coarse-graining identity. It remains diffusive and therefore",
        "does not create a hard finite propagation speed.",
        "",
        f"![Relaxation-diffusion pilot]({_rel_from(report, figure)})",
        "",
        "## Controlled Design",
        "",
        f"- updates: `{args.steps}`; burn-in cut: `{args.burn_in}`; seeds: `{args.seeds}`",
        f"- fixed epsilon: `{args.epsilon}`; active eta: `{args.eta}`; paired `eta=0`",
        f"- diffusion RMS per memory time / L: `{args.diffusion_length_ratios}`",
        f"- lambda: `{args.lambda_value}`; M0: `{args.memory_mass}`; modes: `{args.n_modes}`",
        f"- zero-integral kernel: `A_att={args.amplitude_att}`, `sigma_att={args.sigma_att}`, `sigma_comp={args.sigma_comp}`",
        "",
        "## Results",
        "",
        "| diffusion RMS/L | nu/update | active radius | eta=0 radius | active/control | feedback step/epsilon |",
        "| ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in payload["summary"]:
        lines.append(
            f"| {_fmt(row['diffusion_length_ratio'])} | "
            f"{_fmt(row['diffusion_per_update'])} | "
            f"{_fmt(row['active_radius_median'])} | "
            f"{_fmt(row['eta_zero_radius_median'])} | "
            f"{_fmt(row['active_over_control_radius_median'])} | "
            f"{_fmt(row['feedback_over_epsilon_median'])} |"
        )
    lines.extend(
        [
            "",
            f"Largest-diffusion / zero-diffusion active radius: {_fmt(payload['largest_over_zero_active_radius'])}.",
            f"Largest-diffusion / zero-diffusion confinement ratio: {_fmt(payload['largest_over_zero_confinement_ratio'])}.",
            "",
            "## Validation and Interpretation",
            "",
            f"- kernel integral coefficient: {_fmt(payload['kernel_integral_coefficient'])}",
            f"- maximum eta=0 random-walk replay error: {_fmt(payload['max_eta_zero_random_walk_error'])}",
            f"- maximum memory-mass error: {_fmt(payload['max_memory_mass_absolute_error'])}",
            "- the zero-diffusion package test is bitwise equal to the original spectral update",
            "",
            "A change with diffusion demonstrates sensitivity to a newly introduced spatial",
            "field law. It does not by itself demonstrate metastability, propagation, or a",
            "physical mediator. The next gate must ask whether any new mode or timescale is",
            "control-separated and stable across lag, seed, box size, and mode count.",
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
    payload, profiles = run_pilot(args)
    report = _resolve(args.report)
    summary_json = _resolve(args.summary_json)
    figure = _resolve(args.figure)
    plot_results(payload, profiles, figure)
    summary_json.parent.mkdir(parents=True, exist_ok=True)
    summary_json.write_text(
        json.dumps(payload, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(
        build_report(args, payload, report, summary_json, figure),
        encoding="utf-8",
    )
    print(f"wrote {report}")
    print(f"wrote {summary_json}")
    print(f"wrote {figure}")


if __name__ == "__main__":
    main()
