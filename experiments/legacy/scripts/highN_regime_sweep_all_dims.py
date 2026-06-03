#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from emergenz_knoten import (
    SimulationConfig,
    bootstrap_mean_ci,
    covariance_dimension,
    occupancy_dimension,
    simulate_finite_memory,
    spectral_dimension,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Alpha sweep with all three dimensions (D_cov, D_occ, D_spec)"
    )
    parser.add_argument(
        "--alpha", type=float, default=0.01, help="Memory decay parameter"
    )
    parser.add_argument("--seed-start", type=int, default=1, help="Starting seed")
    parser.add_argument(
        "--n-seeds", type=int, default=5, help="Number of consecutive seeds to run"
    )
    parser.add_argument(
        "--steps", type=int, default=20000, help="Number of update steps"
    )
    parser.add_argument(
        "--sample-every", type=int, default=200, help="Sampling interval"
    )
    parser.add_argument("--output", type=str, default="", help="Output JSON file")
    return parser.parse_args()


def run_seed(cfg: SimulationConfig, seed: int) -> dict:
    result = simulate_finite_memory(cfg, seed=seed)
    samples = result["samples"]
    return {
        "seed": seed,
        "D_cov": float(covariance_dimension(samples)),
        "D_occ": float(occupancy_dimension(samples, n_scales=10, min_count=2)),
        "D_spec": float(spectral_dimension(samples)),
        "n_samples": int(len(samples)),
    }


def summarize(values: list[float]) -> dict[str, float]:
    mean, lo, hi = bootstrap_mean_ci(values, level=0.95, n_boot=1000, seed=0)
    import numpy as np

    std = float(np.std(values, ddof=1)) if len(values) > 1 else 0.0
    return {
        "mean": float(mean),
        "std": std,
        "ci_95_lo": float(lo),
        "ci_95_hi": float(hi),
    }


def main() -> None:
    args = parse_args()
    cfg = SimulationConfig(
        steps=args.steps,
        dim=7,
        epsilon=0.03,
        eta=0.15,
        alpha=args.alpha,
        sigma_rep=1.0,
        sigma_att=3.0,
        amplitude_rep=1.0,
        amplitude_att=0.35,
        memory_factor=6.0,
        max_memory=3000,
        burn_in=0,
        sample_every=args.sample_every,
    )

    runs = []
    start = time.perf_counter()
    for seed in range(args.seed_start, args.seed_start + args.n_seeds):
        print(f"Running seed={seed} with alpha={args.alpha}...")
        runs.append(run_seed(cfg, seed))
    elapsed = time.perf_counter() - start

    d_cov_values = [run["D_cov"] for run in runs]
    d_occ_values = [run["D_occ"] for run in runs if run["D_occ"] == run["D_occ"]]
    d_spec_values = [run["D_spec"] for run in runs if run["D_spec"] == run["D_spec"]]

    stats = {
        "alpha": args.alpha,
        "seed_list": list(range(args.seed_start, args.seed_start + args.n_seeds)),
        "n_seeds": args.n_seeds,
        "elapsed_seconds": float(elapsed),
        "runs": runs,
        "D_cov_stats": summarize(d_cov_values),
        "D_occ_stats": (
            summarize(d_occ_values)
            if d_occ_values
            else {
                "mean": float("nan"),
                "std": float("nan"),
                "ci_95_lo": float("nan"),
                "ci_95_hi": float("nan"),
            }
        ),
        "D_spec_stats": (
            summarize(d_spec_values)
            if d_spec_values
            else {
                "mean": float("nan"),
                "std": float("nan"),
                "ci_95_lo": float("nan"),
                "ci_95_hi": float("nan"),
            }
        ),
    }

    if args.output:
        output_path = Path(args.output)
        if not output_path.is_absolute():
            output_path = ROOT / output_path
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(stats, indent=2, sort_keys=True))
        print(f"Wrote to {output_path}")

    print(json.dumps(stats, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
