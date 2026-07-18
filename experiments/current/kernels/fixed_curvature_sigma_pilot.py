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
import time
from typing import Any, Iterable

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
DYNAMICS_DIR = ROOT / "experiments" / "current" / "dynamics"
sys.path.insert(0, str(DYNAMICS_DIR))
sys.path.insert(0, str(ROOT / "src"))

from emergenz_knoten import SimulationConfig, two_scale_local_curvature  # noqa: E402
from emergenz_knoten.knot_score import score_v0_5_against_control  # noqa: E402

import long_run_metastability as metastability_run  # noqa: E402
from kernel_compensation_audit import fixed_curvature_amplitude  # noqa: E402


METRICS = {
    "knot_score": "KnotScore v0.5",
    "memory_radius": "memory radius",
    "memory_dimension": "D_mem",
    "memory_roundness": "memory roundness",
    "dynamic_radius": "dynamic RMS radius",
    "dynamic_drift_ratio": "center drift / radius / memory time",
}


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
            "Run a one-axis sigma-ratio pilot at fixed two-scale local curvature "
            "with shared seed-matched eta=0 controls."
        )
    )
    parser.add_argument("--steps", type=int, default=1_000_000)
    parser.add_argument("--dim", type=int, default=3)
    parser.add_argument(
        "--seeds", type=_parse_int_list, default=_parse_int_list("1,2,3,4,5")
    )
    parser.add_argument(
        "--q-values", type=_parse_float_list, default=_parse_float_list("2,3,4")
    )
    parser.add_argument("--chi", type=float, default=35.0 / 9.0)
    parser.add_argument("--epsilon", type=float, default=1.0e-4)
    parser.add_argument("--eta", type=float, default=0.15)
    parser.add_argument("--alpha", type=float, default=0.01)
    parser.add_argument("--memory-mass", type=float, default=1.0)
    parser.add_argument("--sigma-rep", type=float, default=1.0)
    parser.add_argument("--amplitude-rep", type=float, default=1.0)
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
            "fixed_chi_q_slice_d3_N1M_seed1-5_eps1em4_2026-07-18"
        ),
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path(
            "reports/kernels/compensation/"
            "fixed_curvature_sigma_pilot_d3_N1M_2026-07-18.md"
        ),
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=Path(
            "reports/kernels/compensation/"
            "fixed_curvature_sigma_pilot_d3_N1M_2026-07-18.json"
        ),
    )
    parser.add_argument(
        "--figure-dir",
        type=Path,
        default=Path("figures/draft/kernels/fixed_curvature_sigma_2026-07-18"),
    )
    return parser.parse_args()


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def _rel_from(source_file: Path, target: Path) -> str:
    return Path(
        os.path.relpath(target.resolve(), source_file.resolve().parent)
    ).as_posix()


def _q_token(q: float) -> str:
    return f"q{q:.6g}".replace(".", "p")


def _case_path(directory: Path, condition: str, seed: int, steps: int) -> Path:
    return directory / f"case_{condition}_seed{seed}_steps{steps}.json"


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _nested_float(payload: Any, *keys: str) -> float | None:
    value = payload
    for key in keys:
        if not isinstance(value, dict):
            return None
        value = value.get(key)
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def _best_residence(diagnostics: dict[str, Any]) -> float | None:
    by_voxel = diagnostics.get("residence_by_voxel_size")
    if not isinstance(by_voxel, dict):
        return None
    values = [
        _nested_float(item, "max_residence_memory_times")
        for item in by_voxel.values()
        if isinstance(item, dict)
    ]
    finite = [value for value in values if value is not None]
    return max(finite) if finite else None


def _dynamic_payload(diagnostics: dict[str, Any]) -> dict[str, Any]:
    dynamic = diagnostics.get("dynamic_center_trace")
    if not isinstance(dynamic, dict):
        return {}
    trend = dynamic.get("trend")
    return trend if isinstance(trend, dict) else dynamic


def _row_from_case(
    case: dict[str, Any],
    *,
    q: float | None,
    control: dict[str, Any] | None,
) -> dict[str, Any]:
    diagnostics = case.get("diagnostics")
    if not isinstance(diagnostics, dict):
        raise ValueError("case has no diagnostics payload")
    memory_shape = diagnostics.get("memory_cloud", {})
    if isinstance(memory_shape, dict):
        memory_shape = memory_shape.get("shape", {})
    if not isinstance(memory_shape, dict):
        memory_shape = {}
    occupancy = diagnostics.get("occupancy")
    occupancy_window = (
        occupancy.get("scaling_window", {}) if isinstance(occupancy, dict) else {}
    )
    dynamic = _dynamic_payload(diagnostics)
    score: dict[str, float | None] = {}
    if control is not None:
        control_diagnostics = control.get("diagnostics")
        if not isinstance(control_diagnostics, dict):
            raise ValueError("control has no diagnostics payload")
        score = score_v0_5_against_control(diagnostics, control_diagnostics)
    config = case.get("config", {})
    sigma_rep = float(config.get("sigma_rep", 1.0)) if isinstance(config, dict) else 1.0
    memory_radius = _nested_float(memory_shape, "mean_radius")
    return {
        "condition": case.get("condition"),
        "seed": int(case["seed"]),
        "q": q,
        "amplitude_att": float(config.get("amplitude_att"))
        if isinstance(config, dict)
        else None,
        "local_curvature": (
            two_scale_local_curvature(
                sigma_rep=float(config["sigma_rep"]),
                sigma_att=float(config["sigma_att"]),
                amplitude_rep=float(config["amplitude_rep"]),
                amplitude_att=float(config["amplitude_att"]),
            )
            if isinstance(config, dict)
            else None
        ),
        "knot_score": score.get("score"),
        "memory_compactness_gain": score.get("memory_compactness_gain"),
        "memory_radius": memory_radius,
        "memory_radius_over_sigma_rep": (
            memory_radius / sigma_rep if memory_radius is not None else None
        ),
        "memory_dimension": _nested_float(memory_shape, "effective_dimension"),
        "memory_roundness": _nested_float(memory_shape, "axis_ratio_min_max"),
        "dynamic_radius": _nested_float(dynamic, "rms_radius_median"),
        "dynamic_drift_ratio": _nested_float(
            dynamic, "center_drift_radius_fraction_per_memory_time_median"
        ),
        "covariance_dimension": _nested_float(diagnostics, "covariance_dimension"),
        "occupancy_window_dimension": _nested_float(occupancy_window, "dimension"),
        "occupancy_window_valid": bool(occupancy_window.get("valid_scaling", False))
        if isinstance(occupancy_window, dict)
        else False,
        "best_residence_memory_times": _best_residence(diagnostics),
        "elapsed_seconds": _nested_float(case, "elapsed_seconds"),
        "git_revision": case.get("git_revision"),
        "git_status": case.get("git_status"),
    }


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


def _iqr(values: Iterable[Any]) -> tuple[float | None, float | None]:
    finite: list[float] = []
    for value in values:
        try:
            number = float(value)
        except (TypeError, ValueError):
            continue
        if math.isfinite(number):
            finite.append(number)
    finite.sort()
    if not finite:
        return None, None
    if len(finite) == 1:
        return finite[0], finite[0]
    q1, _, q3 = statistics.quantiles(finite, n=4, method="inclusive")
    return q1, q3


def _aggregate(
    rows: list[dict[str, Any]], q_values: list[float]
) -> list[dict[str, Any]]:
    metrics = [
        "knot_score",
        "memory_compactness_gain",
        "memory_radius",
        "memory_radius_over_sigma_rep",
        "memory_dimension",
        "memory_roundness",
        "dynamic_radius",
        "dynamic_drift_ratio",
        "covariance_dimension",
        "occupancy_window_dimension",
        "best_residence_memory_times",
    ]
    out: list[dict[str, Any]] = []
    for q in q_values:
        group = [row for row in rows if row["q"] == q]
        record: dict[str, Any] = {
            "q": q,
            "amplitude_att": _median(row["amplitude_att"] for row in group),
            "local_curvature": _median(row["local_curvature"] for row in group),
            "n_seeds": len(group),
        }
        for metric in metrics:
            values = [row.get(metric) for row in group]
            record[f"{metric}_median"] = _median(values)
            low, high = _iqr(values)
            record[f"{metric}_q1"] = low
            record[f"{metric}_q3"] = high
        out.append(record)
    return out


def _fmt(value: Any, digits: int = 4) -> str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return "n/a"
    if not math.isfinite(number):
        return "n/a"
    if number == 0.0:
        return "0"
    if abs(number) < 1e-3 or abs(number) >= 1e4:
        return f"{number:.{digits}e}"
    return f"{number:.{digits}f}"


def _plot_metrics(
    rows: list[dict[str, Any]],
    control_rows: list[dict[str, Any]],
    *,
    q_values: list[float],
    output: Path,
) -> None:
    fig, axes = plt.subplots(2, 3, figsize=(13.0, 7.5))
    colors = ["#147d64", "#c23b22", "#377eb8", "#7a4eab", "#d98900"]
    for axis, (metric, label) in zip(axes.flat, METRICS.items(), strict=True):
        for seed, color in zip(
            sorted({int(row["seed"]) for row in rows}), colors, strict=False
        ):
            seed_rows = sorted(
                (row for row in rows if int(row["seed"]) == seed),
                key=lambda row: float(row["q"]),
            )
            x = [float(row["q"]) for row in seed_rows if row.get(metric) is not None]
            y = [float(row[metric]) for row in seed_rows if row.get(metric) is not None]
            if x:
                axis.plot(x, y, marker="o", alpha=0.42, linewidth=1.0, color=color)
        medians = []
        for q in q_values:
            medians.append(_median(row.get(metric) for row in rows if row["q"] == q))
        valid = [
            (q, value)
            for q, value in zip(q_values, medians, strict=True)
            if value is not None
        ]
        if valid:
            axis.plot(
                [item[0] for item in valid],
                [item[1] for item in valid],
                color="#202020",
                marker="s",
                linewidth=2.4,
                label="active median",
            )
        control_median = _median(row.get(metric) for row in control_rows)
        if control_median is not None:
            axis.axhline(
                control_median,
                color="#777777",
                linestyle="--",
                linewidth=1.4,
                label="shared eta=0 median",
            )
        axis.set_xlabel("q = sigma_att / sigma_rep")
        axis.set_ylabel(label)
        axis.grid(True, alpha=0.22)
        if metric in {"memory_radius", "dynamic_radius", "dynamic_drift_ratio"}:
            values = [
                float(row[metric])
                for row in rows + control_rows
                if row.get(metric) not in (None, 0.0)
            ]
            if values and min(values) > 0.0:
                axis.set_yscale("log")
        axis.legend(frameon=False, fontsize=7)
    fig.suptitle("Fixed-curvature sigma-ratio pilot: seed paths and medians")
    fig.tight_layout()
    fig.savefig(output, dpi=190)
    plt.close(fig)


def _validate_args(args: argparse.Namespace) -> None:
    if args.steps < 1:
        raise SystemExit("--steps must be positive")
    if args.dim < 1:
        raise SystemExit("--dim must be positive")
    if args.burn_in < 0 or args.burn_in >= args.steps:
        raise SystemExit("--burn-in must satisfy 0 <= burn_in < steps")
    if args.sample_every < 1 or args.trace_points < 2:
        raise SystemExit("sampling values must be positive and trace-points >= 2")
    if args.sigma_rep <= 0.0 or args.amplitude_rep <= 0.0:
        raise SystemExit("repulsive scale and amplitude must be positive")
    if args.chi <= 1.0 or not math.isfinite(args.chi):
        raise SystemExit("--chi must be finite and greater than one")
    if any(q <= 1.0 for q in args.q_values):
        raise SystemExit("all q values must exceed one")


def _run_or_load(
    *,
    config: SimulationConfig,
    condition: str,
    seed: int,
    directory: Path,
    args: argparse.Namespace,
    trace_targets: np.ndarray,
) -> dict[str, Any]:
    path = _case_path(directory, condition, seed, config.steps)
    if path.exists() and not args.no_resume:
        payload = _load_json(path)
        stored = payload.get("base_config")
        if stored == asdict(config):
            print(f"loading {path.relative_to(ROOT)}", flush=True)
            return payload
        raise RuntimeError(f"existing case config mismatch: {path}")
    if args.skip_run:
        raise FileNotFoundError(path)
    print(
        f"running condition={condition} seed={seed} q={config.sigma_att / config.sigma_rep:g} "
        f"A_att={config.amplitude_att:g} steps={config.steps}",
        flush=True,
    )
    return metastability_run.run_case(
        base_config=config,
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
    )


def run_or_load_cases(
    args: argparse.Namespace, output_dir: Path
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    trace_targets = metastability_run._trace_targets(
        steps=args.steps,
        burn_in=args.burn_in,
        trace_every=0,
        trace_points=args.trace_points,
        trace_spacing="log",
    )
    controls: dict[int, dict[str, Any]] = {}
    control_q = min(args.q_values, key=lambda q: abs(q - 3.0))
    control_config = SimulationConfig(
        steps=args.steps,
        dim=args.dim,
        epsilon=args.epsilon,
        eta=args.eta,
        alpha=args.alpha,
        memory_mass=args.memory_mass,
        deposition_kernel="delta",
        deposition_sigma=0.0,
        sigma_rep=args.sigma_rep,
        sigma_att=args.sigma_rep * control_q,
        amplitude_rep=args.amplitude_rep,
        amplitude_att=fixed_curvature_amplitude(
            q=control_q,
            chi=args.chi,
            amplitude_rep=args.amplitude_rep,
        ),
        memory_factor=args.memory_factor,
        max_memory=args.max_memory,
        burn_in=args.burn_in,
        sample_every=args.sample_every,
    )
    for seed in args.seeds:
        controls[seed] = _run_or_load(
            config=control_config,
            condition="eta_zero",
            seed=seed,
            directory=output_dir / "shared_eta_zero",
            args=args,
            trace_targets=trace_targets,
        )

    cases: list[dict[str, Any]] = []
    rows: list[dict[str, Any]] = []
    for q in args.q_values:
        amplitude_att = fixed_curvature_amplitude(
            q=q,
            chi=args.chi,
            amplitude_rep=args.amplitude_rep,
        )
        config = SimulationConfig(
            steps=args.steps,
            dim=args.dim,
            epsilon=args.epsilon,
            eta=args.eta,
            alpha=args.alpha,
            memory_mass=args.memory_mass,
            deposition_kernel="delta",
            deposition_sigma=0.0,
            sigma_rep=args.sigma_rep,
            sigma_att=args.sigma_rep * q,
            amplitude_rep=args.amplitude_rep,
            amplitude_att=amplitude_att,
            memory_factor=args.memory_factor,
            max_memory=args.max_memory,
            burn_in=args.burn_in,
            sample_every=args.sample_every,
        )
        for seed in args.seeds:
            case = _run_or_load(
                config=config,
                condition="baseline",
                seed=seed,
                directory=output_dir / _q_token(q),
                args=args,
                trace_targets=trace_targets,
            )
            cases.append(case)
            rows.append(_row_from_case(case, q=q, control=controls[seed]))
    control_rows = [
        _row_from_case(case, q=None, control=None) for case in controls.values()
    ]
    return rows, control_rows


def write_outputs(
    *,
    args: argparse.Namespace,
    rows: list[dict[str, Any]],
    control_rows: list[dict[str, Any]],
    report_path: Path,
    summary_path: Path,
    figure_path: Path,
    elapsed_seconds: float,
    source_git_revision: str,
    source_git_status: str,
) -> None:
    aggregate = _aggregate(rows, args.q_values)
    max_sampled_radius = max(
        (
            float(row["memory_radius_over_sigma_rep"])
            for row in rows
            if row["memory_radius_over_sigma_rep"] is not None
        ),
        default=float("nan"),
    )
    payload = {
        "description": "Fixed-local-curvature sigma-ratio mechanism pilot.",
        "generated_utc": _utc_now(),
        "git_revision": source_git_revision,
        "git_status": source_git_status,
        "elapsed_seconds": elapsed_seconds,
        "parameters": {
            "steps": args.steps,
            "dim": args.dim,
            "seeds": args.seeds,
            "q_values": args.q_values,
            "chi": args.chi,
            "epsilon": args.epsilon,
            "eta": args.eta,
            "alpha": args.alpha,
            "memory_mass": args.memory_mass,
            "sigma_rep": args.sigma_rep,
            "amplitude_rep": args.amplitude_rep,
            "burn_in": args.burn_in,
            "sample_every": args.sample_every,
            "trace_points": args.trace_points,
        },
        "shared_control_reason": "At eta=0 the kernel term vanishes exactly, so the seed-matched trajectory is q-independent.",
        "rows": rows,
        "control_rows": control_rows,
        "aggregate": aggregate,
        "max_memory_radius_over_sigma_rep": max_sampled_radius,
        "figure": figure_path.relative_to(ROOT).as_posix(),
    }
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True, allow_nan=False),
        encoding="utf-8",
    )

    lines = [
        "# Fixed-Curvature Sigma Pilot",
        "",
        f"Date: {payload['generated_utc']}.",
        "",
        "## Scope",
        "",
        "This mechanism pilot varies only `q=sigma_att/sigma_rep` while holding",
        f"the local curvature ratio fixed at `chi={args.chi:.8g}`. It uses",
        f"`N={args.steps:,}`, seeds `{','.join(str(seed) for seed in args.seeds)}`,",
        f"`d={args.dim}`, `epsilon={args.epsilon:g}`, `eta={args.eta:g}`,",
        f"`lambda={args.alpha:g}`, `M0={args.memory_mass:g}`, delta deposition,",
        "`sigma_rep=1`, `burn_in=0`, and 100 logarithmic center traces.",
        "",
        "The five `eta=0` cases are shared across q: with `eta=0` the kernel",
        "term vanishes exactly, so rerunning an identical random walk for every",
        "kernel geometry would add no independent control information.",
        "",
        "## Results",
        "",
        "| q | A_att | curvature | score | memory radius | radius/sigma_rep | D_mem | roundness | dynamic radius | drift/r | D_cov | D_occ win | residence |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in aggregate:
        lines.append(
            "| "
            f"{_fmt(row['q'])} | {_fmt(row['amplitude_att'])} | {_fmt(row['local_curvature'])} | "
            f"{_fmt(row['knot_score_median'])} | {_fmt(row['memory_radius_median'])} | "
            f"{_fmt(row['memory_radius_over_sigma_rep_median'])} | "
            f"{_fmt(row['memory_dimension_median'])} | {_fmt(row['memory_roundness_median'])} | "
            f"{_fmt(row['dynamic_radius_median'])} | {_fmt(row['dynamic_drift_ratio_median'])} | "
            f"{_fmt(row['covariance_dimension_median'])} | "
            f"{_fmt(row['occupancy_window_dimension_median'])} | "
            f"{_fmt(row['best_residence_memory_times_median'])} |"
        )
    lines.extend(
        [
            "",
            f"![Fixed-curvature KPI slice]({_rel_from(report_path, figure_path)})",
            "",
            "## Interpretation Guardrails",
            "",
            f"- The largest observed final memory radius is `{_fmt(max_sampled_radius)}`",
            "  times `sigma_rep`. If this is far below one, all q cases sample only",
            "  the local Taylor region and near-collapse is expected by construction.",
            "- Equal outcomes would show that the current compact branch identifies",
            "  local curvature, not the two nominal Gaussian scales separately.",
            "- Different outcomes would identify scale separation as an independent",
            "  mechanism and justify one narrower follow-up, not a broad sigma sweep.",
            "- This `N=1M` slice is a mechanism gate, not new long-run knot evidence.",
            "- Zero integral is not tested here; the exact compensated third scale is",
            "  the next pilot only after this q-axis is understood.",
            "",
            "## Provenance",
            "",
            f"- Git revision: `{payload['git_revision']}`",
            f"- Git status at report generation: `{payload['git_status'] or 'clean'}`",
            "- Raw cases: `data/processed/kernel_compensation/` (ignored bulk data)",
            "- Script: `experiments/current/kernels/fixed_curvature_sigma_pilot.py`",
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
    figure_path = figure_dir / "fixed_curvature_sigma_kpis.png"

    started = time.perf_counter()
    rows, control_rows = run_or_load_cases(args, output_dir)
    elapsed = time.perf_counter() - started
    _plot_metrics(rows, control_rows, q_values=args.q_values, output=figure_path)
    write_outputs(
        args=args,
        rows=rows,
        control_rows=control_rows,
        report_path=report_path,
        summary_path=summary_path,
        figure_path=figure_path,
        elapsed_seconds=elapsed,
        source_git_revision=source_git_revision,
        source_git_status=source_git_status,
    )
    print(f"wrote {report_path}")
    print(f"wrote {summary_path}")
    print(f"wrote {figure_path}")


if __name__ == "__main__":
    main()
