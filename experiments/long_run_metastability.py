from __future__ import annotations

import argparse
from dataclasses import asdict, replace
from datetime import UTC, datetime
import json
import math
from pathlib import Path
import subprocess
import sys
import time
from typing import Iterable

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from emergenz_knoten import (  # noqa: E402
    SimulationConfig,
    covariance_dimension,
    occupancy_dimension,
    residence_statistics,
)
from emergenz_knoten.markov import vector_autocorrelation  # noqa: E402

try:
    from numba import njit

    _NUMBA_AVAILABLE = True
except ImportError:  # pragma: no cover
    _NUMBA_AVAILABLE = False

    def njit(*args, **kwargs):  # type: ignore[no-redef]
        def wrapper(func):
            return func

        return wrapper


def _parse_int_list(value: str) -> list[int]:
    values = [int(item.strip()) for item in value.split(",") if item.strip()]
    if not values:
        raise argparse.ArgumentTypeError("expected at least one integer")
    return values


def _parse_float_list(value: str) -> list[float]:
    values = [float(item.strip()) for item in value.split(",") if item.strip()]
    if not values:
        raise argparse.ArgumentTypeError("expected at least one float")
    return values


def _parse_conditions(value: str) -> list[str]:
    allowed = {"baseline", "eta_zero", "single_scale"}
    values = [item.strip() for item in value.split(",") if item.strip()]
    unknown = sorted(set(values) - allowed)
    if unknown:
        raise argparse.ArgumentTypeError(f"unknown condition(s): {', '.join(unknown)}")
    if not values:
        raise argparse.ArgumentTypeError("expected at least one condition")
    return values


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


def _utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def _horizon(config: SimulationConfig) -> int:
    return min(config.max_memory, max(1, int(config.memory_factor / config.alpha)))


def _stored_weight_mass(alpha: float, horizon: int) -> float:
    return float(1.0 - (1.0 - alpha) ** horizon)


def _apply_condition(config: SimulationConfig, condition: str) -> SimulationConfig:
    if condition == "baseline":
        return config
    if condition == "eta_zero":
        return replace(config, eta=0.0)
    if condition == "single_scale":
        return replace(config, amplitude_att=0.0)
    raise ValueError(f"unknown condition: {condition}")


@njit(cache=True)
def _simulate_circular_numba(
    steps: int,
    dim: int,
    epsilon: float,
    eta: float,
    alpha: float,
    sigma_rep: float,
    sigma_att: float,
    amplitude_rep: float,
    amplitude_att: float,
    memory_factor: float,
    max_memory: int,
    burn_in: int,
    sample_every: int,
    seed: int,
):
    np.random.seed(seed)
    horizon = int(memory_factor / alpha)
    if horizon < 1:
        horizon = 1
    if horizon > max_memory:
        horizon = max_memory

    weights = np.empty(horizon, np.float64)
    weight = alpha
    decay = 1.0 - alpha
    for age in range(horizon):
        weights[age] = weight
        weight *= decay

    memory = np.zeros((horizon, dim), np.float64)
    x = np.zeros(dim, np.float64)
    max_samples = steps // sample_every + 2
    samples = np.zeros((max_samples, dim), np.float64)
    sample_steps = np.zeros(max_samples, np.int64)
    idx = 0
    filled = 0
    n_sample = 0
    sigma_rep2 = sigma_rep * sigma_rep
    sigma_att2 = sigma_att * sigma_att

    for step in range(1, steps + 1):
        grad = np.zeros(dim, np.float64)
        if eta != 0.0:
            for age in range(filled):
                mem_idx = (idx - 1 - age) % horizon
                r2 = 0.0
                for d in range(dim):
                    diff = x[d] - memory[mem_idx, d]
                    r2 += diff * diff
                rep = amplitude_rep * np.exp(-0.5 * r2 / sigma_rep2) / sigma_rep2
                att = amplitude_att * np.exp(-0.5 * r2 / sigma_att2) / sigma_att2
                factor = weights[age] * (rep - att)
                for d in range(dim):
                    grad[d] += factor * (x[d] - memory[mem_idx, d])

        for d in range(dim):
            x[d] = x[d] + epsilon * np.random.normal(0.0, 1.0) - eta * grad[d]

        for d in range(dim):
            memory[idx, d] = x[d]
        idx = (idx + 1) % horizon
        if filled < horizon:
            filled += 1

        if step >= burn_in and step % sample_every == 0:
            for d in range(dim):
                samples[n_sample, d] = x[d]
            sample_steps[n_sample] = step
            n_sample += 1

    return samples[:n_sample], sample_steps[:n_sample], x, memory, weights, filled


def simulate_long_run(config: SimulationConfig, *, seed: int) -> dict[str, np.ndarray]:
    if not _NUMBA_AVAILABLE:
        raise ImportError("numba is required for long-run simulations")
    (
        samples,
        sample_steps,
        final_x,
        memory,
        weights,
        filled,
    ) = _simulate_circular_numba(
        config.steps,
        config.dim,
        config.epsilon,
        config.eta,
        config.alpha,
        config.sigma_rep,
        config.sigma_att,
        config.amplitude_rep,
        config.amplitude_att,
        config.memory_factor,
        config.max_memory,
        config.burn_in,
        config.sample_every,
        seed,
    )
    return {
        "samples": samples,
        "sample_steps": sample_steps,
        "final_x": final_x.copy(),
        "memory": memory[:filled].copy(),
        "weights": weights[:filled].copy(),
    }


def _finite_float(value: float | np.floating | None) -> float | None:
    if value is None:
        return None
    out = float(value)
    return out if math.isfinite(out) else None


def _sample_span(samples: np.ndarray) -> list[float]:
    if samples.size == 0:
        return []
    return (samples.max(axis=0) - samples.min(axis=0)).astype(float).tolist()


def metastability_diagnostics(
    samples: np.ndarray,
    *,
    config: SimulationConfig,
    voxel_sizes: Iterable[float],
    max_ac_lag: int,
    min_memory_times: float,
) -> dict[str, object]:
    if len(samples) < 2:
        raise ValueError("at least two samples are required")

    memory_persistence_updates = 1.0 / config.alpha
    voxel_results: dict[str, dict[str, float | bool | None]] = {}
    for voxel_size in voxel_sizes:
        residence = residence_statistics(samples, voxel_size=voxel_size, min_visits=3)
        mean_updates = float(residence["mean_residence"] * config.sample_every)
        max_updates = float(residence["max_residence"] * config.sample_every)
        voxel_results[str(voxel_size)] = {
            **residence,
            "mean_residence_updates": mean_updates,
            "max_residence_updates": max_updates,
            "mean_residence_memory_times": mean_updates / memory_persistence_updates,
            "max_residence_memory_times": max_updates / memory_persistence_updates,
            "candidate_long_lived": bool(
                max_updates >= min_memory_times * memory_persistence_updates
            ),
        }

    lag = min(max_ac_lag, len(samples) - 1)
    autocorrelation = vector_autocorrelation(samples, max_lag=lag)
    increments = np.linalg.norm(np.diff(samples, axis=0), axis=1)
    centered = samples - samples.mean(axis=0, keepdims=True)
    radii = np.linalg.norm(centered, axis=1)

    return {
        "n_samples": int(len(samples)),
        "memory_persistence_updates": float(memory_persistence_updates),
        "sample_every": int(config.sample_every),
        "sample_span": _sample_span(samples),
        "mean_sample_increment": _finite_float(increments.mean()),
        "max_sample_increment": _finite_float(increments.max()),
        "mean_centered_radius": _finite_float(radii.mean()),
        "max_centered_radius": _finite_float(radii.max()),
        "covariance_dimension": _finite_float(covariance_dimension(samples)),
        "occupancy_dimension": _finite_float(occupancy_dimension(samples)),
        "autocorrelation": [_finite_float(value) for value in autocorrelation],
        "residence_by_voxel_size": voxel_results,
    }


def _case_filename(condition: str, seed: int, steps: int) -> str:
    return f"case_{condition}_seed{seed}_steps{steps}.json"


def run_case(
    *,
    base_config: SimulationConfig,
    condition: str,
    seed: int,
    voxel_sizes: Iterable[float],
    max_ac_lag: int,
    min_memory_times: float,
    output_dir: Path,
) -> dict[str, object]:
    config = _apply_condition(base_config, condition)
    started = time.perf_counter()
    result = simulate_long_run(config, seed=seed)
    elapsed = time.perf_counter() - started
    samples = result["samples"]
    horizon = _horizon(config)
    diagnostics = metastability_diagnostics(
        samples,
        config=config,
        voxel_sizes=voxel_sizes,
        max_ac_lag=max_ac_lag,
        min_memory_times=min_memory_times,
    )
    payload: dict[str, object] = {
        "condition": condition,
        "seed": int(seed),
        "git_revision": _git_output(["rev-parse", "--short", "HEAD"]),
        "git_status": _git_output(["status", "--short"]),
        "started_utc": _utc_now(),
        "elapsed_seconds": float(elapsed),
        "steps_per_second": float(config.steps / elapsed) if elapsed > 0 else None,
        "config": asdict(config),
        "memory_horizon": int(horizon),
        "stored_weight_mass": _stored_weight_mass(config.alpha, horizon),
        "diagnostics": diagnostics,
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    case_path = output_dir / _case_filename(condition, seed, config.steps)
    case_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True, allow_nan=False),
        encoding="utf-8",
    )
    return payload


def summarize_cases(cases: list[dict[str, object]]) -> list[dict[str, object]]:
    rows = []
    for case in cases:
        diagnostics = case["diagnostics"]
        assert isinstance(diagnostics, dict)
        residence = diagnostics["residence_by_voxel_size"]
        assert isinstance(residence, dict)
        best_ratio = 0.0
        candidate = False
        for metrics in residence.values():
            assert isinstance(metrics, dict)
            ratio = metrics.get("max_residence_memory_times")
            if isinstance(ratio, (float, int)) and math.isfinite(float(ratio)):
                best_ratio = max(best_ratio, float(ratio))
            candidate = candidate or bool(metrics.get("candidate_long_lived"))
        rows.append(
            {
                "condition": case["condition"],
                "seed": case["seed"],
                "steps": case["config"]["steps"],  # type: ignore[index]
                "elapsed_seconds": case["elapsed_seconds"],
                "steps_per_second": case["steps_per_second"],
                "covariance_dimension": diagnostics["covariance_dimension"],
                "occupancy_dimension": diagnostics["occupancy_dimension"],
                "best_max_residence_memory_times": best_ratio,
                "candidate_long_lived": candidate,
            }
        )
    return rows


def write_summary(output_dir: Path, payload: dict[str, object]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "summary.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True, allow_nan=False),
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Run long-N metastability diagnostics for the canonical finite-memory "
            "model. This is an evidence campaign, not a Paper-0 structural proof."
        )
    )
    parser.add_argument("--steps", type=int, default=10_000_000)
    parser.add_argument("--dim", type=int, default=3)
    parser.add_argument("--seeds", type=_parse_int_list, default=_parse_int_list("1"))
    parser.add_argument(
        "--conditions",
        type=_parse_conditions,
        default=_parse_conditions("baseline"),
    )
    parser.add_argument("--epsilon", type=float, default=0.03)
    parser.add_argument("--eta", type=float, default=0.15)
    parser.add_argument("--alpha", type=float, default=0.01)
    parser.add_argument("--sigma-rep", type=float, default=1.0)
    parser.add_argument("--sigma-att", type=float, default=3.0)
    parser.add_argument("--amplitude-rep", type=float, default=1.0)
    parser.add_argument("--amplitude-att", type=float, default=0.35)
    parser.add_argument("--memory-factor", type=float, default=6.0)
    parser.add_argument("--max-memory", type=int, default=800)
    parser.add_argument("--burn-in", type=int, default=1_000_000)
    parser.add_argument("--sample-every", type=int, default=1000)
    parser.add_argument(
        "--voxel-sizes",
        type=_parse_float_list,
        default=_parse_float_list("0.5,1.0,2.0"),
    )
    parser.add_argument("--max-ac-lag", type=int, default=50)
    parser.add_argument("--min-memory-times", type=float, default=10.0)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/processed/long_run_metastability/2026-06-29_initial"),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.steps < 1:
        raise SystemExit("--steps must be positive")
    if args.burn_in < 0 or args.burn_in >= args.steps:
        raise SystemExit("--burn-in must satisfy 0 <= burn_in < steps")
    if args.sample_every < 1:
        raise SystemExit("--sample-every must be positive")
    if args.max_memory < 1:
        raise SystemExit("--max-memory must be positive")
    if not 0.0 < args.alpha <= 1.0:
        raise SystemExit("--alpha must satisfy 0 < alpha <= 1")
    if not _NUMBA_AVAILABLE:
        raise SystemExit("numba is required for long-run simulations")

    output_dir = args.output_dir
    if not output_dir.is_absolute():
        output_dir = ROOT / output_dir

    base_config = SimulationConfig(
        steps=args.steps,
        dim=args.dim,
        epsilon=args.epsilon,
        eta=args.eta,
        alpha=args.alpha,
        sigma_rep=args.sigma_rep,
        sigma_att=args.sigma_att,
        amplitude_rep=args.amplitude_rep,
        amplitude_att=args.amplitude_att,
        memory_factor=args.memory_factor,
        max_memory=args.max_memory,
        burn_in=args.burn_in,
        sample_every=args.sample_every,
    )

    run_started = _utc_now()
    cases: list[dict[str, object]] = []
    total_started = time.perf_counter()
    for condition in args.conditions:
        for seed in args.seeds:
            print(
                "running "
                f"condition={condition} seed={seed} steps={base_config.steps} "
                f"alpha={base_config.alpha:g} dim={base_config.dim}",
                flush=True,
            )
            cases.append(
                run_case(
                    base_config=base_config,
                    condition=condition,
                    seed=seed,
                    voxel_sizes=args.voxel_sizes,
                    max_ac_lag=args.max_ac_lag,
                    min_memory_times=args.min_memory_times,
                    output_dir=output_dir,
                )
            )

    total_elapsed = time.perf_counter() - total_started
    summary_payload: dict[str, object] = {
        "description": "Long-N metastability diagnostics for the canonical finite-memory model.",
        "started_utc": run_started,
        "finished_utc": _utc_now(),
        "total_elapsed_seconds": float(total_elapsed),
        "git_revision": _git_output(["rev-parse", "--short", "HEAD"]),
        "git_status": _git_output(["status", "--short"]),
        "parameters": {
            "conditions": args.conditions,
            "seeds": args.seeds,
            "voxel_sizes": args.voxel_sizes,
            "max_ac_lag": args.max_ac_lag,
            "min_memory_times": args.min_memory_times,
        },
        "base_config": asdict(base_config),
        "case_summaries": summarize_cases(cases),
        "case_files": [
            _case_filename(str(case["condition"]), int(case["seed"]), base_config.steps)
            for case in cases
        ],
    }
    write_summary(output_dir, summary_payload)
    print(f"wrote summary to {output_dir / 'summary.json'}", flush=True)


if __name__ == "__main__":
    main()
