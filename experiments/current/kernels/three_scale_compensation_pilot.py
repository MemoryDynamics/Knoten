from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
import json
import math
import os
from pathlib import Path
import statistics
import subprocess
import sys
import time
from typing import Any, Iterable

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import brentq


def _repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("repository root not found")


ROOT = _repo_root()
DYNAMICS_DIR = ROOT / "experiments" / "current" / "dynamics"
sys.path.insert(0, str(DYNAMICS_DIR))
sys.path.insert(0, str(ROOT / "src"))

from emergenz_knoten import (  # noqa: E402
    SimulationConfig,
    two_scale_integral_coefficient,
    two_scale_local_curvature,
    zero_mean_compensator_amplitude,
    zero_mean_curvature_matched_amplitudes,
)

import fixed_curvature_sigma_pilot as common  # noqa: E402
import kernel_compensation_audit as analytic  # noqa: E402
import long_run_metastability as metastability_run  # noqa: E402


CORE_METRICS = {
    "knot_score": "KnotScore v0.5",
    "memory_radius": "memory radius",
    "memory_dimension": "D_mem",
    "memory_roundness": "memory roundness",
    "dynamic_radius": "dynamic RMS radius",
    "dynamic_drift_ratio": "center drift / radius / memory time",
}


@dataclass(frozen=True)
class KernelVariant:
    label: str
    title: str
    config: SimulationConfig
    sigma_comp: float | None
    amplitude_comp: float
    integral_coefficient: float
    local_curvature: float
    curvature_retention: float
    radial_force_crossing: float | None


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


def _parse_int_list(value: str) -> list[int]:
    values = [int(item.strip()) for item in value.split(",") if item.strip()]
    if not values or any(item < 0 for item in values):
        raise argparse.ArgumentTypeError(
            "expected non-negative comma-separated integers"
        )
    return values


def _parse_float_list(value: str) -> list[float]:
    values = [float(item.strip()) for item in value.split(",") if item.strip()]
    if not values or any(not math.isfinite(item) for item in values):
        raise argparse.ArgumentTypeError("expected finite comma-separated numbers")
    return values


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Compare the q=3 two-scale reference against exact broad "
            "zero-integral three-scale kernels with and without curvature matching."
        )
    )
    parser.add_argument("--steps", type=int, default=1_000_000)
    parser.add_argument("--dim", type=int, default=3)
    parser.add_argument(
        "--seeds", type=_parse_int_list, default=_parse_int_list("1,2,3,4,5")
    )
    parser.add_argument("--epsilon", type=float, default=1.0e-4)
    parser.add_argument("--eta", type=float, default=0.15)
    parser.add_argument("--alpha", type=float, default=0.01)
    parser.add_argument("--memory-mass", type=float, default=1.0)
    parser.add_argument("--sigma-rep", type=float, default=1.0)
    parser.add_argument("--sigma-att", type=float, default=3.0)
    parser.add_argument("--sigma-comp", type=float, default=10.0)
    parser.add_argument("--amplitude-rep", type=float, default=1.0)
    parser.add_argument("--amplitude-att", type=float, default=35.0)
    parser.add_argument("--memory-factor", type=float, default=6.0)
    parser.add_argument("--max-memory", type=int, default=600)
    parser.add_argument("--burn-in", type=int, default=0)
    parser.add_argument("--sample-every", type=int, default=1000)
    parser.add_argument("--trace-points", type=int, default=100)
    parser.add_argument(
        "--voxel-sizes",
        type=_parse_float_list,
        default=_parse_float_list("0.5,1.0,2.0"),
    )
    parser.add_argument("--max-ac-lag", type=int, default=50)
    parser.add_argument("--min-memory-times", type=float, default=10.0)
    parser.add_argument("--skip-run", action="store_true")
    parser.add_argument("--no-resume", action="store_true")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(
            "data/processed/kernel_compensation/"
            "three_scale_zero_mean_d3_N1M_seed1-5_eps1em4_2026-07-18"
        ),
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path(
            "reports/kernels/compensation/"
            "three_scale_zero_mean_pilot_d3_N1M_2026-07-18.md"
        ),
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=Path(
            "reports/kernels/compensation/"
            "three_scale_zero_mean_pilot_d3_N1M_2026-07-18.json"
        ),
    )
    parser.add_argument(
        "--figure-dir",
        type=Path,
        default=Path("figures/draft/kernels/three_scale_compensation_2026-07-18"),
    )
    return parser.parse_args()


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def _rel_from(source_file: Path, target: Path) -> str:
    return Path(
        os.path.relpath(target.resolve(), source_file.resolve().parent)
    ).as_posix()


def _validate_args(args: argparse.Namespace) -> None:
    if args.steps < 1 or args.dim < 1:
        raise SystemExit("steps and dim must be positive")
    if args.burn_in < 0 or args.burn_in >= args.steps:
        raise SystemExit("--burn-in must satisfy 0 <= burn_in < steps")
    if args.sample_every < 1 or args.trace_points < 2:
        raise SystemExit("sampling values must be positive and trace-points >= 2")
    if not args.sigma_rep < args.sigma_att < args.sigma_comp:
        raise SystemExit("require sigma_rep < sigma_att < sigma_comp")
    if args.amplitude_rep <= 0.0 or args.amplitude_att <= 0.0:
        raise SystemExit("kernel amplitudes must be positive")
    if not 0.0 < args.alpha <= 1.0:
        raise SystemExit("--alpha must satisfy 0 < alpha <= 1")


def _radial_force_crossing(
    *,
    sigma_rep: float,
    sigma_att: float,
    sigma_comp: float | None,
    amplitude_rep: float,
    amplitude_att: float,
    amplitude_comp: float,
) -> float | None:
    def drift(radius: float) -> float:
        rep = amplitude_rep * math.exp(-0.5 * radius**2 / sigma_rep**2) / sigma_rep**2
        att = amplitude_att * math.exp(-0.5 * radius**2 / sigma_att**2) / sigma_att**2
        comp = 0.0
        if sigma_comp is not None and amplitude_comp != 0.0:
            comp = (
                amplitude_comp
                * math.exp(-0.5 * radius**2 / sigma_comp**2)
                / sigma_comp**2
            )
        return radius * (rep - att + comp)

    scales = np.geomspace(1.0e-8 * sigma_rep, 100.0 * (sigma_comp or sigma_att), 20_000)
    previous_x = float(scales[0])
    previous_y = drift(previous_x)
    for current_x in scales[1:]:
        current_x = float(current_x)
        current_y = drift(current_x)
        if previous_y * current_y < 0.0:
            return float(brentq(drift, previous_x, current_x))
        previous_x = current_x
        previous_y = current_y
    return None


def _base_config(args: argparse.Namespace, *, amplitude_att: float) -> SimulationConfig:
    return SimulationConfig(
        steps=args.steps,
        dim=args.dim,
        epsilon=args.epsilon,
        eta=args.eta,
        alpha=args.alpha,
        memory_mass=args.memory_mass,
        deposition_kernel="delta",
        deposition_sigma=0.0,
        sigma_rep=args.sigma_rep,
        sigma_att=args.sigma_att,
        amplitude_rep=args.amplitude_rep,
        amplitude_att=amplitude_att,
        memory_factor=args.memory_factor,
        max_memory=args.max_memory,
        burn_in=args.burn_in,
        sample_every=args.sample_every,
    )


def build_variants(args: argparse.Namespace) -> list[KernelVariant]:
    baseline_curvature = two_scale_local_curvature(
        sigma_rep=args.sigma_rep,
        sigma_att=args.sigma_att,
        amplitude_rep=args.amplitude_rep,
        amplitude_att=args.amplitude_att,
    )
    raw_comp = zero_mean_compensator_amplitude(
        dim=args.dim,
        sigma_rep=args.sigma_rep,
        sigma_att=args.sigma_att,
        sigma_comp=args.sigma_comp,
        amplitude_rep=args.amplitude_rep,
        amplitude_att=args.amplitude_att,
    )
    matched_att, matched_comp = zero_mean_curvature_matched_amplitudes(
        dim=args.dim,
        sigma_rep=args.sigma_rep,
        sigma_att=args.sigma_att,
        sigma_comp=args.sigma_comp,
        target_curvature=baseline_curvature,
        amplitude_rep=args.amplitude_rep,
    )
    specs = [
        ("two_scale", "two-scale reference", args.amplitude_att, None, 0.0),
        (
            "zero_mean_raw",
            "zero integral",
            args.amplitude_att,
            args.sigma_comp,
            raw_comp,
        ),
        (
            "zero_mean_curvature_matched",
            "zero integral + curvature matched",
            matched_att,
            args.sigma_comp,
            matched_comp,
        ),
    ]
    variants: list[KernelVariant] = []
    for label, title, amplitude_att, sigma_comp, amplitude_comp in specs:
        integral = two_scale_integral_coefficient(
            dim=args.dim,
            sigma_rep=args.sigma_rep,
            sigma_att=args.sigma_att,
            amplitude_rep=args.amplitude_rep,
            amplitude_att=amplitude_att,
        )
        if sigma_comp is not None:
            integral += amplitude_comp * sigma_comp**args.dim
        curvature = two_scale_local_curvature(
            sigma_rep=args.sigma_rep,
            sigma_att=args.sigma_att,
            amplitude_rep=args.amplitude_rep,
            amplitude_att=amplitude_att,
        )
        if sigma_comp is not None:
            curvature -= amplitude_comp / sigma_comp**2
        variants.append(
            KernelVariant(
                label=label,
                title=title,
                config=_base_config(args, amplitude_att=amplitude_att),
                sigma_comp=sigma_comp,
                amplitude_comp=amplitude_comp,
                integral_coefficient=integral,
                local_curvature=curvature,
                curvature_retention=curvature / baseline_curvature,
                radial_force_crossing=_radial_force_crossing(
                    sigma_rep=args.sigma_rep,
                    sigma_att=args.sigma_att,
                    sigma_comp=sigma_comp,
                    amplitude_rep=args.amplitude_rep,
                    amplitude_att=amplitude_att,
                    amplitude_comp=amplitude_comp,
                ),
            )
        )
    return variants


def _case_path(directory: Path, condition: str, seed: int, steps: int) -> Path:
    return directory / f"case_{condition}_seed{seed}_steps{steps}.json"


def _run_or_load(
    *,
    variant: KernelVariant,
    condition: str,
    seed: int,
    directory: Path,
    args: argparse.Namespace,
    trace_targets: np.ndarray,
) -> dict[str, Any]:
    path = _case_path(directory, condition, seed, variant.config.steps)
    if path.exists() and not args.no_resume:
        payload = json.loads(path.read_text(encoding="utf-8"))
        if payload.get("base_config") != asdict(variant.config):
            raise RuntimeError(f"existing case config mismatch: {path}")
        effective = payload.get("effective_kernel", {})
        expected_comp = (
            variant.amplitude_comp if variant.sigma_comp is not None else None
        )
        actual_comp = (
            effective.get("amplitude_comp") if isinstance(effective, dict) else None
        )
        if expected_comp is not None and not math.isclose(
            float(actual_comp), expected_comp
        ):
            raise RuntimeError(f"existing compensator mismatch: {path}")
        print(f"loading {path.relative_to(ROOT)}", flush=True)
        return payload
    if args.skip_run:
        raise FileNotFoundError(path)
    print(
        f"running variant={variant.label} condition={condition} seed={seed} "
        f"A_att={variant.config.amplitude_att:.9g} A_comp={variant.amplitude_comp:.9g} "
        f"steps={variant.config.steps}",
        flush=True,
    )
    return metastability_run.run_case(
        base_config=variant.config,
        condition=condition,
        seed=seed,
        voxel_sizes=args.voxel_sizes,
        max_ac_lag=args.max_ac_lag,
        min_memory_times=args.min_memory_times,
        output_dir=directory,
        force_components=False,
        trace_every=0,
        trace_targets=trace_targets,
        spectral_points=0,
        memory_snapshot_points=0,
        sigma_comp=variant.sigma_comp,
        amplitude_comp=variant.amplitude_comp,
    )


def run_or_load_cases(
    args: argparse.Namespace,
    output_dir: Path,
    variants: list[KernelVariant],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    trace_targets = metastability_run._trace_targets(
        steps=args.steps,
        burn_in=args.burn_in,
        trace_every=0,
        trace_points=args.trace_points,
        trace_spacing="log",
    )
    baseline = variants[0]
    controls: dict[int, dict[str, Any]] = {}
    for seed in args.seeds:
        controls[seed] = _run_or_load(
            variant=baseline,
            condition="eta_zero",
            seed=seed,
            directory=output_dir / "shared_eta_zero",
            args=args,
            trace_targets=trace_targets,
        )

    rows: list[dict[str, Any]] = []
    for variant in variants:
        for seed in args.seeds:
            case = _run_or_load(
                variant=variant,
                condition="baseline",
                seed=seed,
                directory=output_dir / variant.label,
                args=args,
                trace_targets=trace_targets,
            )
            row = common._row_from_case(
                case, q=args.sigma_att / args.sigma_rep, control=controls[seed]
            )
            row.update(
                {
                    "variant": variant.label,
                    "title": variant.title,
                    "sigma_comp": variant.sigma_comp,
                    "amplitude_comp": variant.amplitude_comp,
                    "integral_coefficient": variant.integral_coefficient,
                    "local_curvature": variant.local_curvature,
                    "curvature_retention": variant.curvature_retention,
                    "radial_force_crossing": variant.radial_force_crossing,
                }
            )
            rows.append(row)
    control_rows = [
        common._row_from_case(case, q=None, control=None) for case in controls.values()
    ]
    return rows, control_rows


def _median(values: Iterable[Any]) -> float | None:
    finite: list[float] = []
    for value in values:
        try:
            number = float(value)
        except (TypeError, ValueError):
            continue
        if math.isfinite(number):
            finite.append(number)
    return statistics.median(finite) if finite else None


def _aggregate(
    rows: list[dict[str, Any]], variants: list[KernelVariant]
) -> list[dict[str, Any]]:
    metrics = [
        *CORE_METRICS,
        "memory_compactness_gain",
        "covariance_dimension",
        "occupancy_window_dimension",
        "best_residence_memory_times",
    ]
    out: list[dict[str, Any]] = []
    for variant in variants:
        group = [row for row in rows if row["variant"] == variant.label]
        record: dict[str, Any] = {
            "variant": variant.label,
            "title": variant.title,
            "n_seeds": len(group),
            "amplitude_att": variant.config.amplitude_att,
            "sigma_comp": variant.sigma_comp,
            "amplitude_comp": variant.amplitude_comp,
            "integral_coefficient": variant.integral_coefficient,
            "local_curvature": variant.local_curvature,
            "curvature_retention": variant.curvature_retention,
            "radial_force_crossing": variant.radial_force_crossing,
        }
        for metric in metrics:
            record[f"{metric}_median"] = _median(row.get(metric) for row in group)
        out.append(record)
    return out


def _paired_differences(
    rows: list[dict[str, Any]], variants: list[KernelVariant]
) -> list[dict[str, Any]]:
    baseline = {int(row["seed"]): row for row in rows if row["variant"] == "two_scale"}
    out: list[dict[str, Any]] = []
    for variant in variants[1:]:
        variant_rows = {
            int(row["seed"]): row for row in rows if row["variant"] == variant.label
        }
        for metric, label in CORE_METRICS.items():
            relative: list[float] = []
            for seed, base in baseline.items():
                candidate = variant_rows.get(seed)
                if (
                    candidate is None
                    or base.get(metric) is None
                    or candidate.get(metric) is None
                ):
                    continue
                base_value = float(base[metric])
                candidate_value = float(candidate[metric])
                scale = abs(base_value)
                relative.append(
                    abs(candidate_value - base_value) / scale
                    if scale > 0.0
                    else abs(candidate_value)
                )
            out.append(
                {
                    "variant": variant.label,
                    "metric": metric,
                    "label": label,
                    "n_seeds": len(relative),
                    "median_relative_difference": _median(relative),
                    "max_relative_difference": max(relative) if relative else None,
                }
            )
    return out


def _plot_static_field(variants: list[KernelVariant], output: Path) -> None:
    radius = np.linspace(0.0, 30.0, 1600)
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.4))
    colors = ["#202020", "#147d64", "#c23b22"]
    for variant, color in zip(variants, colors, strict=True):
        potential, drift = analytic.radial_profile(
            radius,
            q=variant.config.sigma_att / variant.config.sigma_rep,
            amplitude_att=variant.config.amplitude_att,
            sigma_comp=variant.sigma_comp,
            amplitude_comp=variant.amplitude_comp,
        )
        axes[0].plot(radius, potential, color=color, linewidth=1.8, label=variant.title)
        axes[1].plot(radius, drift, color=color, linewidth=1.8, label=variant.title)
        if variant.radial_force_crossing is not None:
            axes[1].axvline(
                variant.radial_force_crossing, color=color, linestyle=":", alpha=0.65
            )
    axes[0].set_ylabel("K(r)")
    axes[1].set_ylabel("-dK/dr (outward positive)")
    for axis in axes:
        axis.axhline(0.0, color="#777777", linewidth=0.8)
        axis.set_xlabel("r / sigma_rep")
        axis.grid(True, alpha=0.22)
        axis.legend(frameon=False, fontsize=8)
    axes[0].set_title("point-deposit potential")
    axes[1].set_title("local attraction and outer repulsive shell")
    fig.tight_layout()
    fig.savefig(output, dpi=190)
    plt.close(fig)


def _plot_kpis(
    rows: list[dict[str, Any]],
    control_rows: list[dict[str, Any]],
    variants: list[KernelVariant],
    output: Path,
) -> None:
    fig, axes = plt.subplots(2, 3, figsize=(13.0, 7.5))
    colors = ["#202020", "#147d64", "#c23b22"]
    x = np.arange(len(variants), dtype=float)
    rng = np.random.default_rng(20260718)
    for axis, (metric, label) in zip(axes.flat, CORE_METRICS.items(), strict=True):
        for index, (variant, color) in enumerate(zip(variants, colors, strict=True)):
            values = [
                float(row[metric])
                for row in rows
                if row["variant"] == variant.label and row.get(metric) is not None
            ]
            if values:
                jitter = rng.uniform(-0.055, 0.055, len(values))
                axis.scatter(index + jitter, values, color=color, alpha=0.55, s=25)
                axis.scatter(
                    index,
                    statistics.median(values),
                    color=color,
                    marker="s",
                    s=58,
                    zorder=4,
                )
        control = [
            float(row[metric]) for row in control_rows if row.get(metric) is not None
        ]
        if control:
            axis.axhline(
                statistics.median(control),
                color="#777777",
                linestyle="--",
                label="eta=0 median",
            )
        axis.set_xticks(
            x, ["two scale", "zero mean", "zero mean\n+ curvature"], rotation=0
        )
        axis.set_ylabel(label)
        axis.grid(True, alpha=0.22)
        if metric in {"memory_radius", "dynamic_radius", "dynamic_drift_ratio"}:
            all_values = [
                float(row[metric])
                for row in rows + control_rows
                if row.get(metric) not in (None, 0.0)
            ]
            if all_values and min(all_values) > 0.0:
                axis.set_yscale("log")
        handles, labels = axis.get_legend_handles_labels()
        if handles:
            axis.legend(handles, labels, frameon=False, fontsize=7)
    fig.suptitle("Three-scale compensation pilot: seeds and medians")
    fig.tight_layout()
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


def write_outputs(
    *,
    args: argparse.Namespace,
    variants: list[KernelVariant],
    rows: list[dict[str, Any]],
    control_rows: list[dict[str, Any]],
    report_path: Path,
    summary_path: Path,
    field_figure: Path,
    kpi_figure: Path,
    elapsed_seconds: float,
    source_git_revision: str,
    source_git_status: str,
) -> None:
    aggregate = _aggregate(rows, variants)
    paired = _paired_differences(rows, variants)
    variant_max_differences = {
        variant.label: max(
            float(item["max_relative_difference"])
            for item in paired
            if item["variant"] == variant.label
            and item["max_relative_difference"] is not None
        )
        for variant in variants[1:]
    }
    exact_zero = all(
        abs(variant.integral_coefficient) <= 1.0e-9 for variant in variants[1:]
    )
    crossings_present = all(
        variant.radial_force_crossing is not None for variant in variants[1:]
    )
    local_metrics_retained = all(
        value <= 0.05 for value in variant_max_differences.values()
    )
    gate_pass = exact_zero and crossings_present and local_metrics_retained
    payload = {
        "description": "Three-scale exact-zero-integral compensation mechanism pilot.",
        "generated_utc": _utc_now(),
        "git_revision": source_git_revision,
        "git_status": source_git_status,
        "elapsed_seconds": elapsed_seconds,
        "parameters": {
            "steps": args.steps,
            "dim": args.dim,
            "seeds": args.seeds,
            "epsilon": args.epsilon,
            "eta": args.eta,
            "alpha": args.alpha,
            "memory_mass": args.memory_mass,
            "sigma_rep": args.sigma_rep,
            "sigma_att": args.sigma_att,
            "sigma_comp": args.sigma_comp,
            "amplitude_rep": args.amplitude_rep,
            "amplitude_att_reference": args.amplitude_att,
            "burn_in": args.burn_in,
            "sample_every": args.sample_every,
            "trace_points": args.trace_points,
        },
        "variants": [
            {
                "label": variant.label,
                "title": variant.title,
                "config": asdict(variant.config),
                "sigma_comp": variant.sigma_comp,
                "amplitude_comp": variant.amplitude_comp,
                "integral_coefficient": variant.integral_coefficient,
                "local_curvature": variant.local_curvature,
                "curvature_retention": variant.curvature_retention,
                "radial_force_crossing": variant.radial_force_crossing,
            }
            for variant in variants
        ],
        "rows": rows,
        "control_rows": control_rows,
        "aggregate": aggregate,
        "paired_relative_differences": paired,
        "variant_max_relative_differences": variant_max_differences,
        "acceptance": {
            "exact_zero_integral": exact_zero,
            "outer_force_crossing_present": crossings_present,
            "local_kpis_within_five_percent_of_baseline": local_metrics_retained,
            "mechanism_gate_pass": gate_pass,
        },
        "figures": [
            field_figure.relative_to(ROOT).as_posix(),
            kpi_figure.relative_to(ROOT).as_posix(),
        ],
    }
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True, allow_nan=False), encoding="utf-8"
    )

    lines = [
        "# Three-Scale Zero-Integral Pilot",
        "",
        f"Date: {payload['generated_utc']}.",
        "",
        "## Scope",
        "",
        "This is one controlled extension of the corrected q=3 scalar kernel,",
        "not a new parameter sweep. It compares the two-scale reference with",
        "an exact zero-integral broad compensator and a second zero-integral",
        "variant whose local point-deposit curvature is matched exactly.",
        "",
        f"Fixed simulation parameters: `N={args.steps:,}`, seeds `{','.join(str(seed) for seed in args.seeds)}`,",
        f"`d={args.dim}`, `epsilon={args.epsilon:g}`, `eta={args.eta:g}`,",
        f"`lambda={args.alpha:g}`, `M0={args.memory_mass:g}`, delta deposition,",
        f"`sigma_rep={args.sigma_rep:g}`, `sigma_att={args.sigma_att:g}`,",
        f"`sigma_comp={args.sigma_comp:g}`, `burn_in={args.burn_in}`. {len(args.seeds)}",
        "seed-matched `eta=0` paths provide the shared null control.",
        "",
        "## Analytic Kernel Checks",
        "",
        "| variant | A_att | A_comp | integral coefficient | curvature | retention | force crossing |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for variant in variants:
        lines.append(
            f"| {variant.title} | {_fmt(variant.config.amplitude_att)} | "
            f"{_fmt(variant.amplitude_comp)} | {_fmt(variant.integral_coefficient)} | "
            f"{_fmt(variant.local_curvature)} | {_fmt(variant.curvature_retention)} | "
            f"{_fmt(variant.radial_force_crossing)} |"
        )
    lines.extend(
        [
            "",
            f"![Static compensated field]({_rel_from(report_path, field_figure)})",
            "",
            "The compensated kernels retain inward drift on knot scales but add",
            "an outer repulsive shell beyond the listed crossing. `integral K=0`",
            "is exact in the current unnormalized d-dimensional Gaussian convention.",
            "",
            "## Simulation KPIs",
            "",
            "| variant | score | memory radius | D_mem | roundness | dynamic radius | drift/r | D_cov | D_occ win | residence |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in aggregate:
        lines.append(
            f"| {row['title']} | {_fmt(row['knot_score_median'])} | "
            f"{_fmt(row['memory_radius_median'])} | {_fmt(row['memory_dimension_median'])} | "
            f"{_fmt(row['memory_roundness_median'])} | {_fmt(row['dynamic_radius_median'])} | "
            f"{_fmt(row['dynamic_drift_ratio_median'])} | {_fmt(row['covariance_dimension_median'])} | "
            f"{_fmt(row['occupancy_window_dimension_median'])} | "
            f"{_fmt(row['best_residence_memory_times_median'])} |"
        )
    lines.extend(
        [
            "",
            f"![Three-scale KPI comparison]({_rel_from(report_path, kpi_figure)})",
            "",
            "## Paired Difference from Two-Scale Reference",
            "",
            "| variant | KPI | seeds | median relative difference | maximum relative difference |",
            "| --- | --- | ---: | ---: | ---: |",
        ]
    )
    for item in paired:
        lines.append(
            f"| {item['variant']} | {item['label']} | {item['n_seeds']} | "
            f"{_fmt(item['median_relative_difference'])} | {_fmt(item['max_relative_difference'])} |"
        )
    lines.extend(
        [
            "",
            "## Decision",
            "",
            f"- Exact zero integral: `{exact_zero}`.",
            f"- Outer force-sign crossing present: `{crossings_present}`.",
            f"- All reported local KPIs remain within 5% of the paired two-scale reference: `{local_metrics_retained}`.",
            f"- Controlled compensation mechanism gate: `{gate_pass}`.",
            "- Passing this gate means only that a broad third scale can preserve",
            "  the current local compact branch while changing its static outer field.",
            "  It is not evidence for electric charge, physical screening, or a",
            "  reciprocal two-knot force law.",
            "- The zero-integral amplitude depends strongly on ambient dimension",
            "  under the current unnormalized Gaussian convention. Paper-II use",
            "  requires either explicit dimension-dependent calibration or normalized",
            "  component kernels before cross-dimension universality is discussed.",
            "- Next: use the compensated field in the signed scalar cross-channel",
            "  with null, label-flip, common-noise, distance, and reciprocity controls.",
            "",
            "## Provenance",
            "",
            f"- Git revision: `{source_git_revision}`",
            f"- Git status at report generation: `{source_git_status or 'clean'}`",
            "- Raw cases: `data/processed/kernel_compensation/` (ignored bulk data)",
            "- Script: `experiments/current/kernels/three_scale_compensation_pilot.py`",
            "",
        ]
    )
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    _validate_args(args)
    source_git_revision = _git_output(["rev-parse", "HEAD"])
    source_git_status = _git_output(["status", "--short"])
    output_dir = _resolve(args.output_dir)
    report_path = _resolve(args.report)
    summary_path = _resolve(args.summary_json)
    figure_dir = _resolve(args.figure_dir)
    figure_dir.mkdir(parents=True, exist_ok=True)
    field_figure = figure_dir / "three_scale_static_field.png"
    kpi_figure = figure_dir / "three_scale_kpis.png"

    variants = build_variants(args)
    started = time.perf_counter()
    rows, control_rows = run_or_load_cases(args, output_dir, variants)
    elapsed = time.perf_counter() - started
    _plot_static_field(variants, field_figure)
    _plot_kpis(rows, control_rows, variants, kpi_figure)
    write_outputs(
        args=args,
        variants=variants,
        rows=rows,
        control_rows=control_rows,
        report_path=report_path,
        summary_path=summary_path,
        field_figure=field_figure,
        kpi_figure=kpi_figure,
        elapsed_seconds=elapsed,
        source_git_revision=source_git_revision,
        source_git_status=source_git_status,
    )
    print(f"wrote {report_path}")
    print(f"wrote {summary_path}")
    print(f"wrote {field_figure}")
    print(f"wrote {kpi_figure}")


if __name__ == "__main__":
    main()
