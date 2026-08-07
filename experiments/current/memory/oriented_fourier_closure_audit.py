"""Audit whether passive oriented memory contains spatial feedback coefficients."""

from __future__ import annotations

import argparse
from dataclasses import asdict
from datetime import UTC, datetime
import glob
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
    SimulationConfig,
    advance_oriented_memory_state,
    helmholtz_mode_components,
    initialize_oriented_memory_state,
    memory_shape_tensor,
    source_conditioned_fourier_transition,
)


def _repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("repository root not found")


ROOT = _repo_root()
DEFAULT_CASE_GLOBS = (
    "data/processed/long_run_metastability/"
    "raw_memory_snapshot_retest_Aatt35_N3M_d3_seed1-5_2026-07-16/"
    "case_baseline_seed*.json",
    "data/processed/long_run_metastability/"
    "raw_memory_snapshot_retest_Aatt35_N3M_d3_seed6_2026-07-22/"
    "case_baseline_seed*.json",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Source-conditioned Fourier closure of passive vector memory."
    )
    parser.add_argument("--case-glob", action="append", default=None)
    parser.add_argument("--seeds", default="1,2,3,4,5,6")
    parser.add_argument("--memory-times", type=float, default=20.0)
    parser.add_argument("--lambda-vector", type=float, default=None)
    parser.add_argument("--orientation-relaxation", type=float, default=None)
    parser.add_argument("--vector-mass", type=float, default=1.0)
    parser.add_argument("--kr-values", default="0.5,1,2,4")
    parser.add_argument("--coefficient-tolerance", type=float, default=1e-10)
    parser.add_argument("--residual-tolerance", type=float, default=1e-10)
    parser.add_argument("--noise-seed", type=int, default=20_260_807)
    parser.add_argument("--allow-dirty", action="store_true")
    parser.add_argument(
        "--report",
        type=Path,
        default=Path(
            "reports/memory/oriented_fourier_closure_audit_2026-08-07.md"
        ),
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=Path(
            "reports/memory/oriented_fourier_closure_audit_2026-08-07.json"
        ),
    )
    parser.add_argument(
        "--figure",
        type=Path,
        default=Path(
            "figures/draft/memory/oriented_fourier_closure_audit_2026-08-07.png"
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


def parse_csv(text: str, *, positive: bool = False) -> list[float]:
    values = [float(item.strip()) for item in text.split(",") if item.strip()]
    if not values or not np.isfinite(values).all():
        raise ValueError("list must contain finite values")
    if positive and any(value <= 0.0 for value in values):
        raise ValueError("list values must be positive")
    return values


def parse_seeds(text: str) -> list[int]:
    seeds = [int(item.strip()) for item in text.split(",") if item.strip()]
    if not seeds or len(seeds) != len(set(seeds)) or any(seed < 0 for seed in seeds):
        raise ValueError("seeds must be unique non-negative integers")
    return seeds


def discover_cases(patterns: list[str], seeds: list[int]) -> list[Path]:
    paths: list[Path] = []
    for pattern in patterns:
        resolved = pattern if Path(pattern).is_absolute() else str(ROOT / pattern)
        paths.extend(Path(path) for path in glob.glob(resolved))
    selected: dict[int, Path] = {}
    for path in sorted(set(item.resolve() for item in paths)):
        payload = json.loads(path.read_text(encoding="utf-8"))
        seed = int(payload["seed"])
        if seed in seeds:
            if seed in selected:
                raise ValueError(f"duplicate case for seed {seed}")
            selected[seed] = path
    missing = sorted(set(seeds) - set(selected))
    if missing:
        raise ValueError(f"missing cases for seeds {missing}")
    return [selected[seed] for seed in seeds]


def load_case(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    payload = json.loads(raw.decode("utf-8"))
    config = SimulationConfig(**payload["config"])
    snapshot = payload["diagnostics"]["memory_cloud"]["snapshot"]
    points = np.asarray(snapshot["points"], dtype=float)
    weights = np.asarray(snapshot["weights"], dtype=float)
    return {
        "path": path,
        "sha256": hashlib.sha256(raw).hexdigest(),
        "seed": int(payload["seed"]),
        "config": config,
        "state": FiniteMemoryState(x=points[0], memory=points, weights=weights),
    }


def mode_directions(dim: int) -> np.ndarray:
    """Return axes plus one body diagonal without choosing a fit direction."""

    axes = np.eye(dim)
    diagonal = np.ones((1, dim), dtype=float) / np.sqrt(dim)
    return np.vstack((axes, diagonal))


def wavevectors_for_state(
    state: FiniteMemoryState,
    kr_values: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, float]:
    radius = float(np.sqrt(np.trace(memory_shape_tensor(state))))
    if radius <= 0.0:
        raise ValueError("memory radius must be positive")
    directions = mode_directions(state.dim)
    vectors = np.vstack(
        [(kr / radius) * directions for kr in np.asarray(kr_values, dtype=float)]
    )
    groups = np.repeat(np.arange(kr_values.size), directions.shape[0])
    return vectors, groups, radius


def _empty_statistics(n_segments: int, n_channels: int, n_kr: int) -> np.ndarray:
    return np.zeros((n_segments, n_channels, n_kr, 3), dtype=float)


def _accumulate(
    statistics: np.ndarray,
    segment: int,
    channel: int,
    group: int,
    previous: np.ndarray,
    target: np.ndarray,
) -> None:
    statistics[segment, channel, group, 0] += float(
        np.vdot(previous, previous).real
    )
    statistics[segment, channel, group, 1] += float(
        np.vdot(previous, target).real
    )
    statistics[segment, channel, group, 2] += float(np.vdot(target, target).real)


def summarize_statistics(
    statistics: np.ndarray,
    kr_values: np.ndarray,
    expected_q: float,
) -> dict[str, Any]:
    xx = statistics[..., 0]
    xy = statistics[..., 1]
    yy = statistics[..., 2]
    q_hat = np.divide(xy, xx, out=np.full_like(xy, np.nan), where=xx > 0.0)
    sse = yy - 2.0 * q_hat * xy + np.square(q_hat) * xx
    roundoff = 128.0 * np.finfo(float).eps * np.maximum(xx, yy)
    sse = np.where(np.abs(sse) <= roundoff, 0.0, sse)
    normalized_residual = np.sqrt(
        np.divide(
            np.maximum(sse, 0.0),
            yy,
            out=np.zeros_like(yy),
            where=yy > 0.0,
        )
    )
    coefficients = np.empty((statistics.shape[0], 2, 3), dtype=float)
    design = np.column_stack(
        (np.ones(kr_values.size), np.square(kr_values), np.power(kr_values, 4))
    )
    for segment in range(statistics.shape[0]):
        for channel in range(2):
            coefficients[segment, channel] = np.linalg.lstsq(
                design,
                1.0 - q_hat[segment, channel],
                rcond=None,
            )[0]
    return {
        "q_hat": q_hat,
        "q_error": q_hat - expected_q,
        "normalized_residual": normalized_residual,
        "defect_coefficients": coefficients,
        "max_abs_q_error": float(np.nanmax(np.abs(q_hat - expected_q))),
        "max_normalized_residual": float(np.nanmax(normalized_residual)),
        "max_abs_spatial_coefficient": float(
            np.nanmax(np.abs(coefficients[..., 1:]))
        ),
    }


def run_case(
    case: dict[str, Any],
    args: argparse.Namespace,
    kr_values: np.ndarray,
) -> dict[str, Any]:
    config = case["config"]
    lambda_vector = (
        config.alpha if args.lambda_vector is None else args.lambda_vector
    )
    relaxation = (
        lambda_vector
        if args.orientation_relaxation is None
        else args.orientation_relaxation
    )
    state = initialize_oriented_memory_state(
        case["state"],
        lambda_vector=lambda_vector,
        vector_mass=args.vector_mass,
        orientation_relaxation=relaxation,
    )
    wavevectors, groups, radius = wavevectors_for_state(
        state.scalar_state,
        kr_values,
    )
    n_steps = int(round(args.memory_times / lambda_vector))
    rng = np.random.default_rng(args.noise_seed + 10_007 * case["seed"])
    noise = rng.normal(size=(n_steps, config.dim))
    statistics = _empty_statistics(2, 2, kr_values.size)
    q = 1.0 - lambda_vector

    for update in range(n_steps):
        following = advance_oriented_memory_state(
            state,
            config,
            noise_increment=noise[update],
        )
        transition = source_conditioned_fourier_transition(
            state,
            following,
            wavevectors,
            forgetting_factor=q,
        )
        old_l, old_t = helmholtz_mode_components(
            transition.previous_modes,
            wavevectors,
        )
        target_l, target_t = helmholtz_mode_components(
            transition.homogeneous_target_modes,
            wavevectors,
        )
        segment = min(1, 2 * update // n_steps)
        for mode, group in enumerate(groups):
            _accumulate(
                statistics,
                segment,
                0,
                int(group),
                old_l[mode],
                target_l[mode],
            )
            _accumulate(
                statistics,
                segment,
                1,
                int(group),
                old_t[mode],
                target_t[mode],
            )
        state = following

    summary = summarize_statistics(statistics, kr_values, q)
    passed = bool(
        summary["max_abs_q_error"] <= args.coefficient_tolerance
        and summary["max_abs_spatial_coefficient"] <= args.coefficient_tolerance
        and summary["max_normalized_residual"] <= args.residual_tolerance
    )
    return {
        "seed": case["seed"],
        "case_path": _relative(case["path"]),
        "case_sha256": case["sha256"],
        "memory_radius": radius,
        "lambda_vector": lambda_vector,
        "orientation_relaxation": relaxation,
        "expected_q": q,
        "n_steps": n_steps,
        **summary,
        "pass": passed,
    }


def plot_results(payload: dict[str, Any], path: Path) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.2))
    tiny = np.finfo(float).tiny
    kr = np.asarray(payload["kr_values"], dtype=float)
    for row in payload["rows"]:
        errors = np.asarray(row["q_error"], dtype=float)
        residual = np.asarray(row["normalized_residual"], dtype=float)
        axes[0].plot(
            kr,
            np.maximum(np.max(np.abs(errors), axis=(0, 1)), tiny),
            "o-",
            alpha=0.75,
            label=f"seed {row['seed']}",
        )
        axes[1].plot(
            kr,
            np.maximum(np.max(residual, axis=(0, 1)), tiny),
            "o-",
            alpha=0.75,
            label=f"seed {row['seed']}",
        )
    axes[0].axhline(payload["coefficient_tolerance"], color="black", linestyle="--")
    axes[1].axhline(payload["residual_tolerance"], color="black", linestyle="--")
    axes[0].set_title("Forgetting-factor error")
    axes[1].set_title("Source-conditioned residual")
    for axis in axes:
        axis.set_xlabel("dimensionless wave number kR")
        axis.set_yscale("log")
        axis.grid(alpha=0.25)
    axes[0].set_ylabel("maximum over channel and segment")
    axes[1].set_ylabel("normalized RMS")
    axes[0].legend(ncol=2, fontsize=8)
    fig.suptitle("Passive oriented-memory Fourier closure")
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=180)
    plt.close(fig)


def write_report(payload: dict[str, Any], report: Path, figure: Path) -> None:
    lines = [
        "# Passive oriented-memory Fourier closure audit",
        "",
        f"Date: {payload['generated_at']}",
        "",
        "## Question",
        "",
        "After subtracting the exact new directed deposit and finite-horizon tail,",
        "does the full retained vector memory contain any wave-number-dependent",
        "homogeneous feedback beyond the known forgetting factor?",
        "",
        "## Exact null",
        "",
        "For every Fourier vector mode, the finite update predicts",
        "",
        r"\[",
        r"m_{n+1,k}-J_{n+1,k}+T_{n,k}=(1-\lambda_v)m_{n,k}.",
        r"\]",
        "",
        "The audit separates longitudinal and transverse components over four",
        "dimensionless wave numbers and two time segments for six mature sources.",
        "",
        "## Decision",
        "",
        f"Status: **{payload['decision']['status']}** "
        f"({payload['decision']['passing']}/{payload['decision']['seed_count']} seeds).",
        "",
        "A pass here confirms the homogeneous passive null. It is evidence against,",
        "not for, emergent active spatial feedback in the implemented update.",
        "",
        "## Seed results",
        "",
        "| seed | max abs(q_hat-q) | max normalized residual | max abs(b_hat,c_hat) | pass |",
        "| ---: | ---: | ---: | ---: | --- |",
    ]
    for row in payload["rows"]:
        lines.append(
            f"| {row['seed']} | {row['max_abs_q_error']:.3e} | "
            f"{row['max_normalized_residual']:.3e} | "
            f"{row['max_abs_spatial_coefficient']:.3e} | "
            f"{'pass' if row['pass'] else 'fail'} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "The complete passive memory is exactly source plus exponential forgetting",
            "within floating-point error. No longitudinal/transverse splitting or",
            "k-squared/k-fourth coefficient is selected by these continuations.",
            "",
            "Consequently, coefficients of an active covariant field cannot be read",
            "from this passive law as microscopic constants. They must either arise",
            "in a separately validated coarse-graining that omits resolved source",
            "variables, or be declared as a new model increment. Longer runs cannot",
            "change this exact source-conditioned identity.",
            "",
            "The result does not exclude nonlinear feedback after adding a new field",
            "law. It prevents calling such a law parameter-free or already emergent.",
            "",
            "## Figure",
            "",
            f"![Fourier closure]({_relative_from(report, figure)})",
            "",
            "## Reproducibility",
            "",
            f"- Analysis revision: {payload['git_revision']}",
            f"- Worktree at start: {payload['git_status_at_start'] or 'clean'}",
            f"- Memory times: {payload['memory_times']}",
            f"- kR values: {list(np.asarray(payload['kr_values'], dtype=float))}",
            f"- Command: {payload['command']}",
        ]
    )
    for row in payload["rows"]:
        lines.append(
            f"- Seed {row['seed']}: {row['case_path']}, SHA-256 {row['case_sha256']}"
        )
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(chr(10).join(lines) + chr(10), encoding="utf-8")


def main() -> None:
    args = parse_args()
    git_status = _git_output(["status", "--short"])
    if git_status and not args.allow_dirty:
        raise SystemExit("worktree must be clean; use --allow-dirty only for development")
    seeds = parse_seeds(args.seeds)
    kr_values = np.asarray(parse_csv(args.kr_values, positive=True), dtype=float)
    patterns = list(DEFAULT_CASE_GLOBS if args.case_glob is None else args.case_glob)
    cases = [load_case(path) for path in discover_cases(patterns, seeds)]
    configs = [asdict(case["config"]) for case in cases]
    if any(config != configs[0] for config in configs[1:]):
        raise SystemExit("all cases must share one SimulationConfig")

    rows = []
    for case in cases:
        print(f"running Fourier closure seed={case['seed']}", flush=True)
        rows.append(run_case(case, args, kr_values))
    passing = sum(row["pass"] for row in rows)
    payload = {
        "schema_version": 1,
        "generated_at": datetime.now(UTC).isoformat(),
        "git_revision": _git_output(["rev-parse", "HEAD"]),
        "git_status_at_start": git_status,
        "command": "python experiments/current/memory/oriented_fourier_closure_audit.py",
        "formation_config": configs[0],
        "memory_times": args.memory_times,
        "kr_values": kr_values,
        "coefficient_tolerance": args.coefficient_tolerance,
        "residual_tolerance": args.residual_tolerance,
        "rows": rows,
        "decision": {
            "status": "pass" if passing == len(rows) else "fail",
            "passing": passing,
            "seed_count": len(rows),
            "interpretation": "passive_homogeneous_null",
        },
    }
    report = _resolve(args.report)
    summary = _resolve(args.summary_json)
    figure = _resolve(args.figure)
    plot_results(payload, figure)
    write_report(payload, report, figure)
    summary.parent.mkdir(parents=True, exist_ok=True)
    summary.write_text(
        json.dumps(_jsonable(payload), indent=2, sort_keys=True) + chr(10),
        encoding="utf-8",
    )
    print(json.dumps(payload["decision"], sort_keys=True))


if __name__ == "__main__":
    main()