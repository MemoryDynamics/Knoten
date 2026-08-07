"""Gate full retained oriented-memory moments against deposit-sign nulls."""

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
    initialize_oriented_memory_state,
    memory_shape_tensor,
    oriented_memory_moments,
    random_sign_memory_coherences,
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
        description="Source-local eligibility gate for full oriented memory."
    )
    parser.add_argument("--case-glob", action="append", default=None)
    parser.add_argument("--seeds", default="1,2,3,4,5,6")
    parser.add_argument("--memory-times", type=float, default=20.0)
    parser.add_argument("--trace-points", type=int, default=100)
    parser.add_argument("--lambda-vector", type=float, default=None)
    parser.add_argument("--orientation-relaxation", type=float, default=None)
    parser.add_argument("--vector-mass", type=float, default=1.0)
    parser.add_argument("--randomizations", type=int, default=256)
    parser.add_argument("--random-quantile", type=float, default=0.99)
    parser.add_argument("--null-separation-min", type=float, default=2.0)
    parser.add_argument("--axis-cosine-min", type=float, default=0.8)
    parser.add_argument("--amplitude-cv-max", type=float, default=0.5)
    parser.add_argument("--source-radius-max-change", type=float, default=0.5)
    parser.add_argument("--source-spectrum-max-drift", type=float, default=0.25)
    parser.add_argument("--minimum-passing-seeds", type=int, default=5)
    parser.add_argument("--noise-seed", type=int, default=20_260_807)
    parser.add_argument("--allow-dirty", action="store_true")
    parser.add_argument(
        "--report",
        type=Path,
        default=Path(
            "reports/response/oriented_memory_source_eligibility_gate_2026-08-07.md"
        ),
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=Path(
            "reports/response/oriented_memory_source_eligibility_gate_2026-08-07.json"
        ),
    )
    parser.add_argument(
        "--figure",
        type=Path,
        default=Path(
            "figures/draft/response/"
            "oriented_memory_source_eligibility_gate_2026-08-07.png"
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


def parse_seeds(text: str) -> list[int]:
    seeds = [int(part.strip()) for part in text.split(",") if part.strip()]
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


def load_snapshot_case(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    payload = json.loads(raw.decode("utf-8"))
    if payload.get("condition") != "baseline":
        raise ValueError(f"{path} is not a baseline case")
    config = SimulationConfig(**payload["config"])
    snapshot = payload["diagnostics"]["memory_cloud"]["snapshot"]
    points = np.asarray(snapshot["points"], dtype=float)
    weights = np.asarray(snapshot["weights"], dtype=float)
    state = FiniteMemoryState(x=points[0], memory=points, weights=weights)
    return {
        "path": path,
        "sha256": hashlib.sha256(raw).hexdigest(),
        "seed": int(payload["seed"]),
        "config": config,
        "state": state,
        "formation_revision": payload.get("git_revision", "unavailable"),
    }


def sample_steps(n_steps: int, trace_points: int) -> np.ndarray:
    if n_steps < 1 or trace_points < 4:
        raise ValueError("n_steps and trace_points must be positive")
    return np.unique(np.rint(np.linspace(0, n_steps, trace_points + 1)).astype(int))


def _normalized_shape_spectrum(state: FiniteMemoryState) -> np.ndarray:
    values = np.clip(np.linalg.eigvalsh(memory_shape_tensor(state)), 0.0, None)
    total = float(np.sum(values))
    return values / total if total > 0.0 else np.zeros_like(values)


def _cosine(left: np.ndarray, right: np.ndarray) -> float:
    a = np.asarray(left, dtype=float).ravel()
    b = np.asarray(right, dtype=float).ravel()
    denominator = float(np.linalg.norm(a) * np.linalg.norm(b))
    if denominator <= np.finfo(float).tiny:
        return 0.0
    return float(np.dot(a, b) / denominator)


def channel_metrics(
    values: np.ndarray,
    coherences: np.ndarray,
    null_quantiles: np.ndarray,
    *,
    late_mask: np.ndarray,
) -> dict[str, float]:
    late_values = np.asarray(values[late_mask], dtype=float)
    late_coherence = np.asarray(coherences[late_mask], dtype=float)
    late_null = np.asarray(null_quantiles[late_mask], dtype=float)
    split = max(1, late_values.shape[0] // 2)
    first = np.mean(late_values[:split], axis=0)
    second = np.mean(late_values[split:], axis=0)
    amplitudes = np.linalg.norm(late_values.reshape(late_values.shape[0], -1), axis=1)
    mean_amplitude = float(np.mean(amplitudes))
    ratios = np.divide(
        late_coherence,
        late_null,
        out=np.zeros_like(late_coherence),
        where=late_null > 0.0,
    )
    return {
        "null_separation_median": float(np.median(ratios)),
        "axis_cosine": _cosine(first, second),
        "amplitude_mean": mean_amplitude,
        "amplitude_cv": float(np.std(amplitudes) / mean_amplitude)
        if mean_amplitude > 0.0
        else float("inf"),
        "coherence_median": float(np.median(late_coherence)),
        "null_quantile_median": float(np.median(late_null)),
    }


def classify_channel(
    metrics: dict[str, float],
    shape_metrics: dict[str, float],
    thresholds: dict[str, float],
) -> tuple[dict[str, bool], bool]:
    gates = {
        "random_sign_separation": bool(
            metrics["null_separation_median"]
            >= thresholds["null_separation_min"]
        ),
        "axis_identity": bool(
            metrics["axis_cosine"] >= thresholds["axis_cosine_min"]
        ),
        "amplitude_bounded": bool(
            metrics["amplitude_cv"] <= thresholds["amplitude_cv_max"]
        ),
        "source_shape_bounded": bool(
            shape_metrics["radius_max_change"]
            <= thresholds["source_radius_max_change"]
            and shape_metrics["spectrum_max_drift"]
            <= thresholds["source_spectrum_max_drift"]
        ),
    }
    return gates, all(gates.values())


def run_case(
    case: dict[str, Any],
    args: argparse.Namespace,
    steps: np.ndarray,
    thresholds: dict[str, float],
) -> dict[str, Any]:
    config = case["config"]
    lambda_vector = (
        float(config.alpha) if args.lambda_vector is None else args.lambda_vector
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
    rng = np.random.default_rng(args.noise_seed + 10_007 * case["seed"])
    sign_rng = np.random.default_rng(args.noise_seed + 100_003 * case["seed"])
    noise = rng.normal(size=(int(steps[-1]), config.dim))
    step_lookup = set(int(value) for value in steps)

    polarizations: list[np.ndarray] = []
    circulations: list[np.ndarray] = []
    polar_coherence: list[float] = []
    circulation_coherence: list[float] = []
    polar_null: list[float] = []
    circulation_null: list[float] = []
    radii: list[float] = []
    spectra: list[np.ndarray] = []

    for update in range(int(steps[-1]) + 1):
        if update in step_lookup:
            moments = oriented_memory_moments(state)
            signs = 2.0 * sign_rng.integers(
                0,
                2,
                size=(args.randomizations, state.scalar_state.n_memory),
            ) - 1.0
            null_polar, null_circulation = random_sign_memory_coherences(
                state,
                signs,
            )
            polarizations.append(moments.polarization)
            circulations.append(moments.circulation_bivector)
            polar_coherence.append(moments.polarization_coherence)
            circulation_coherence.append(moments.circulation_coherence)
            polar_null.append(float(np.quantile(null_polar, args.random_quantile)))
            circulation_null.append(
                float(np.quantile(null_circulation, args.random_quantile))
            )
            radii.append(moments.rms_radius)
            spectra.append(_normalized_shape_spectrum(state.scalar_state))
        if update < int(steps[-1]):
            state = advance_oriented_memory_state(
                state,
                config,
                noise_increment=noise[update],
            )

    polarization_values = np.asarray(polarizations)
    circulation_values = np.asarray(circulations)
    polar_coherence_values = np.asarray(polar_coherence)
    circulation_coherence_values = np.asarray(circulation_coherence)
    polar_null_values = np.asarray(polar_null)
    circulation_null_values = np.asarray(circulation_null)
    radii_values = np.asarray(radii)
    spectra_values = np.asarray(spectra)
    late_mask = steps >= 0.5 * steps[-1]
    initial_radius = float(radii_values[0])
    shape = {
        "radius_max_change": float(
            np.max(np.abs(radii_values / initial_radius - 1.0))
        ),
        "spectrum_max_drift": float(
            np.max(np.linalg.norm(spectra_values - spectra_values[0], axis=1))
        ),
    }
    polar_metrics = channel_metrics(
        polarization_values,
        polar_coherence_values,
        polar_null_values,
        late_mask=late_mask,
    )
    circulation_metrics = channel_metrics(
        circulation_values,
        circulation_coherence_values,
        circulation_null_values,
        late_mask=late_mask,
    )
    polar_gates, polar_pass = classify_channel(
        polar_metrics,
        shape,
        thresholds,
    )
    circulation_gates, circulation_pass = classify_channel(
        circulation_metrics,
        shape,
        thresholds,
    )
    return {
        "seed": case["seed"],
        "case_path": _relative(case["path"]),
        "case_sha256": case["sha256"],
        "formation_revision": case["formation_revision"],
        "lambda_vector": lambda_vector,
        "orientation_relaxation": relaxation,
        "retained_points": int(state.scalar_state.n_memory),
        "retained_tail_fraction": float(1.0 - np.sum(state.weights) / args.vector_mass)
        if args.vector_mass > 0.0
        else 0.0,
        "shape": shape,
        "polarization": polar_metrics,
        "circulation": circulation_metrics,
        "polarization_gates": polar_gates,
        "circulation_gates": circulation_gates,
        "polarization_pass": polar_pass,
        "circulation_pass": circulation_pass,
        "trace": {
            "steps": steps,
            "memory_times": steps * lambda_vector,
            "polarization_coherence": polar_coherence_values,
            "polarization_null_q": polar_null_values,
            "circulation_coherence": circulation_coherence_values,
            "circulation_null_q": circulation_null_values,
        },
    }


def plot_results(payload: dict[str, Any], path: Path) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(11, 8))
    for row in payload["rows"]:
        trace = row["trace"]
        x = np.asarray(trace["memory_times"])
        axes[0, 0].plot(x, trace["polarization_coherence"], label=f"seed {row['seed']}")
        axes[0, 1].plot(x, trace["circulation_coherence"], label=f"seed {row['seed']}")
    axes[0, 0].set_title("Polarization coherence")
    axes[0, 1].set_title("Circulation-bivector coherence")
    for axis in axes[0]:
        axis.set_xlabel("continuation [memory times]")
        axis.set_ylabel("coherence")
        axis.grid(alpha=0.25)
    axes[0, 0].legend(ncol=2, fontsize=8)

    seeds = [row["seed"] for row in payload["rows"]]
    width = 0.35
    x = np.arange(len(seeds))
    axes[1, 0].bar(
        x - width / 2,
        [row["polarization"]["null_separation_median"] for row in payload["rows"]],
        width,
        label="polar",
    )
    axes[1, 0].bar(
        x + width / 2,
        [row["circulation"]["null_separation_median"] for row in payload["rows"]],
        width,
        label="circulation",
    )
    axes[1, 0].axhline(
        payload["thresholds"]["null_separation_min"],
        color="black",
        linestyle="--",
        linewidth=1,
    )
    axes[1, 0].set_xticks(x, seeds)
    axes[1, 0].set_ylabel("median observed / random q99")
    axes[1, 0].set_xlabel("formation seed")
    axes[1, 0].legend()
    axes[1, 0].grid(axis="y", alpha=0.25)

    axes[1, 1].plot(
        seeds,
        [row["polarization"]["axis_cosine"] for row in payload["rows"]],
        "o-",
        label="polar axis",
    )
    axes[1, 1].plot(
        seeds,
        [row["circulation"]["axis_cosine"] for row in payload["rows"]],
        "s--",
        label="circulation axis",
    )
    axes[1, 1].axhline(
        payload["thresholds"]["axis_cosine_min"],
        color="black",
        linestyle="--",
        linewidth=1,
    )
    axes[1, 1].set_xlabel("formation seed")
    axes[1, 1].set_ylabel("late-half axis cosine")
    axes[1, 1].legend()
    axes[1, 1].grid(alpha=0.25)
    fig.suptitle("Full retained oriented-memory source eligibility")
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=180)
    plt.close(fig)


def write_report(payload: dict[str, Any], report: Path, figure: Path) -> None:
    decision = payload["decision"]
    lines = [
        "# Full oriented-memory source eligibility gate",
        "",
        f"Date: {payload['generated_at']}",
        "",
        "## Question",
        "",
        "Does the persistent directed deposition history of six mature scalar",
        "sources carry a source-local polar or circulation-bivector moment that",
        "remains bounded and exceeds a depositwise random-sign null?",
        "",
        "This is an eligibility test for an explicitly added passive vector fibre.",
        "It is not a spin, charge, flavor, particle, phase, or QFT test.",
        "",
        "## Preregistered design",
        "",
        "- six independent d=3, N=3M scalar formation states;",
        "- 20 memory times with 100 linear trace intervals;",
        "- all retained deposits, not reduced carrier-only features;",
        "- 256 deposit-sign randomizations and q=0.99 at every sample;",
        "- late-half median observed/null >= 2, axis cosine >= 0.8,",
        "  amplitude CV <= 0.5, and the existing source shape bounds;",
        "- each channel is decided separately and requires at least 5/6 seeds.",
        "",
        "## Decision",
        "",
        f"Polarization eligibility: **{decision['polarization_status']}** "
        f"({decision['polarization_passing']}/{decision['seed_count']} seeds).",
        "",
        f"Circulation-bivector eligibility: **{decision['circulation_status']}** "
        f"({decision['circulation_passing']}/{decision['seed_count']} seeds).",
        "",
        "## Seed results",
        "",
        "| seed | polar/null | polar axis | polar CV | polar | circ/null | circ axis | circ CV | circ | radius drift | spectrum drift |",
        "| ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | --- | ---: | ---: |",
    ]
    for row in payload["rows"]:
        polar = row["polarization"]
        circulation = row["circulation"]
        lines.append(
            f"| {row['seed']} | {polar['null_separation_median']:.4f} | "
            f"{polar['axis_cosine']:.4f} | {polar['amplitude_cv']:.4f} | "
            f"{'pass' if row['polarization_pass'] else 'fail'} | "
            f"{circulation['null_separation_median']:.4f} | "
            f"{circulation['axis_cosine']:.4f} | "
            f"{circulation['amplitude_cv']:.4f} | "
            f"{'pass' if row['circulation_pass'] else 'fail'} | "
            f"{row['shape']['radius_max_change']:.4f} | "
            f"{row['shape']['spectrum_max_drift']:.4f} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation boundary",
            "",
            "A polar pass would mainly validate that the inserted persistent carrier",
            "survives its own sign-randomized control; persistence is a model input.",
            "A circulation pass would make the antisymmetric full-memory moment an",
            "eligible observable for a later interaction test. In d dimensions it",
            "is a bivector; calling it spin, especially quantized or half-integer",
            "spin, would be unsupported.",
            "",
            "The state contains no rotationally invariant signed scalar or internal",
            "species index. Charge and flavor are therefore undefined in this model,",
            "not merely unmeasured. A later extension would need an explicit source",
            "law, conservation/flux test, or internal representation.",
            "",
            "The oriented source is passive: vector memory does not feed back on its",
            "own trajectory in this gate. No self-consistent vector-knot mechanism",
            "has yet been established.",
            "",
            "## Figure",
            "",
            f"![Source eligibility]({_relative_from(report, figure)})",
            "",
            "## Reproducibility",
            "",
            f"- Analysis revision: {payload['git_revision']}",
            f"- Worktree at start: {payload['git_status_at_start'] or 'clean'}",
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
    if args.randomizations < 32:
        raise SystemExit("randomizations must be at least 32")
    if not 0.5 < args.random_quantile < 1.0:
        raise SystemExit("random-quantile must lie between 0.5 and 1")
    if not 1 <= args.minimum_passing_seeds <= len(seeds):
        raise SystemExit("minimum-passing-seeds must fit seed count")

    patterns = list(DEFAULT_CASE_GLOBS if args.case_glob is None else args.case_glob)
    cases = [load_snapshot_case(path) for path in discover_cases(patterns, seeds)]
    configs = [asdict(case["config"]) for case in cases]
    if any(config != configs[0] for config in configs[1:]):
        raise SystemExit("all formation cases must share one SimulationConfig")
    lambda_vector = (
        cases[0]["config"].alpha
        if args.lambda_vector is None
        else args.lambda_vector
    )
    n_steps = int(round(args.memory_times / lambda_vector))
    steps = sample_steps(n_steps, args.trace_points)
    thresholds = {
        "null_separation_min": args.null_separation_min,
        "axis_cosine_min": args.axis_cosine_min,
        "amplitude_cv_max": args.amplitude_cv_max,
        "source_radius_max_change": args.source_radius_max_change,
        "source_spectrum_max_drift": args.source_spectrum_max_drift,
    }
    rows = []
    for case in cases:
        print(f"running source eligibility seed={case['seed']}", flush=True)
        rows.append(run_case(case, args, steps, thresholds))

    polar_passing = sum(row["polarization_pass"] for row in rows)
    circulation_passing = sum(row["circulation_pass"] for row in rows)
    payload = {
        "schema_version": 1,
        "generated_at": datetime.now(UTC).isoformat(),
        "git_revision": _git_output(["rev-parse", "HEAD"]),
        "git_status_at_start": git_status,
        "command": (
            "python experiments/current/memory/synchronization/"
            "oriented_memory_source_eligibility_gate.py"
        ),
        "formation_config": configs[0],
        "memory_times": args.memory_times,
        "n_steps": n_steps,
        "trace_points": int(steps.size),
        "randomizations": args.randomizations,
        "random_quantile": args.random_quantile,
        "thresholds": thresholds,
        "minimum_passing_seeds": args.minimum_passing_seeds,
        "rows": rows,
        "decision": {
            "polarization_passing": polar_passing,
            "circulation_passing": circulation_passing,
            "seed_count": len(rows),
            "polarization_status": "pass"
            if polar_passing >= args.minimum_passing_seeds
            else "fail",
            "circulation_status": "pass"
            if circulation_passing >= args.minimum_passing_seeds
            else "fail",
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