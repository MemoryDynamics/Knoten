from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from emergenz_knoten import (  # noqa: E402
    SimulationConfig,
    ballistic_scaling_slope,
    exponential_weights,
    mean_squared_displacement,
    repulsive_gaussian_gradient,
)
from emergenz_knoten.markov.validation import (  # noqa: E402
    critical_gamma,
    self_consistency_residual,
    vector_autocorrelation,
)


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


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Probe ballistic scaling in the dimensionless kernel model")
    parser.add_argument("--steps", type=int, default=20000)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--dim", type=int, default=1)

    parser.add_argument("--sample-every", type=int, default=5)
    parser.add_argument("--burn-in", type=int, default=1000)
    parser.add_argument("--max-memory", type=int, default=800)
    parser.add_argument("--output", type=Path, default=Path("data/processed/propagation_speed/ballistic_kernel_probe.json"))
    return parser.parse_args()


def _sweep_cases() -> list[dict[str, float]]:
    lambdas = [0.05, 0.10, 0.20]
    rs = [0.90, 0.95, 0.98, 1.00, 1.02, 1.05, 1.10]
    deltas = [0.0, 1e-4, 1e-3, 1e-2]
    cases: list[dict[str, float]] = []
    for lambda_value in lambdas:
        gamma_c = critical_gamma(lambda_value)
        for r_value in rs:
            eta = r_value * gamma_c
            for delta in deltas:
                cases.append({
                    "lambda": float(lambda_value),
                    "r": float(r_value),
                    "delta": float(delta),
                    "eta": float(eta),
                    "gamma_c": float(gamma_c),
                })
    return cases


def _simulate_repulsive_probe(
    config: SimulationConfig,
    *,
    seed: int,
    lambda_value: float,
    eta: float,
    epsilon: float,
) -> np.ndarray:
    rng = np.random.default_rng(seed)
    horizon = min(config.max_memory, max(1, int(config.memory_factor / lambda_value)))
    weights = exponential_weights(lambda_value, horizon)

    history = np.zeros((horizon, config.dim), dtype=float)
    filled = 0
    x = np.zeros(config.dim, dtype=float)
    direction = np.zeros(config.dim, dtype=float)
    direction[0] = 1.0
    seed_count = max(1, int(np.ceil(5.0 / lambda_value)))
    seed_spacing = 0.01

    for step in range(1, seed_count + 1):
        prior = -step * seed_spacing * direction
        if filled < horizon:
            if filled > 0:
                history[1 : filled + 1] = history[:filled]
            filled += 1
        else:
            history[1:] = history[:-1]
        history[0] = prior

    samples: list[np.ndarray] = []
    for step in range(1, config.steps + 1):
        if filled:
            grad = repulsive_gaussian_gradient(
                x,
                history[:filled],
                weights[:filled],
                sigma=1.0,
                amplitude=1.0,
            )
        else:
            grad = np.zeros(config.dim, dtype=float)

        x = x + epsilon * rng.normal(size=config.dim) + eta * grad
        if filled < horizon:
            if filled > 0:
                history[1 : filled + 1] = history[:filled]
            filled += 1
        else:
            history[1:] = history[:-1]
        history[0] = x

        if step >= config.burn_in and step % config.sample_every == 0:
            samples.append(x.copy())

    return np.asarray(samples, dtype=float)


def run_probe(args: argparse.Namespace) -> dict[str, Any]:
    results: list[dict[str, Any]] = []
    for case in _sweep_cases():
        config = SimulationConfig(
            steps=args.steps,
            dim=args.dim,
            epsilon=case["delta"],
            eta=case["eta"],
            alpha=case["lambda"],
            sample_every=args.sample_every,
            burn_in=args.burn_in,
            max_memory=args.max_memory,
        )
        samples = _simulate_repulsive_probe(
            config,
            seed=args.seed,
            lambda_value=case["lambda"],
            eta=case["eta"],
            epsilon=case["delta"],
        )
        if len(samples) < 3:
            continue

        increments = np.diff(samples, axis=0)
        velocity_autocorr = vector_autocorrelation(increments, max_lag=min(20, len(increments) - 1))
        msd = mean_squared_displacement(samples, max_lag=min(40, len(samples) - 1))
        slope = ballistic_scaling_slope(samples, fit_window=(5, min(40, len(samples) - 1)))
        residual = self_consistency_residual(
            float(np.mean(np.linalg.norm(increments, axis=1))) if len(increments) else 0.0,
            gamma=case["eta"],
            lambda_value=case["lambda"],
        )
        results.append({
            "lambda": case["lambda"],
            "r": case["r"],
            "delta": case["delta"],
            "eta": case["eta"],
            "gamma_c": case["gamma_c"],
            "n_samples": int(samples.shape[0]),
            "velocity_autocorr": velocity_autocorr.tolist(),
            "msd": msd.tolist(),
            "ballistic_slope": float(slope),
            "self_consistency_residual": float(residual),
            "mean_step": float(np.mean(np.linalg.norm(increments, axis=1))),
            "mean_radius": float(np.mean(np.linalg.norm(samples - samples.mean(axis=0, keepdims=True), axis=1))),
            "drift_sign": "plus_repulsive_gradient",
        })

    summary = {
        "timestamp": _utc_now(),
        "git_revision": _git_output(["rev-parse", "HEAD"]),
        "seed": args.seed,
        "steps": int(args.steps),
        "dim": int(args.dim),

        "sample_every": int(args.sample_every),
        "burn_in": int(args.burn_in),
        "max_memory": int(args.max_memory),
        "cases": results,
    }
    return summary


def main() -> None:
    args = _parse_args()
    output_path = args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    summary = run_probe(args)
    output_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
