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
    residence_statistics,
    simulate_finite_memory,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Run an ensemble of high-N regime pilot simulations across multiple seeds. "
            "This script computes mean/std/CI for D_cov and D_occ."
        )
    )
    parser.add_argument("--seed-start", type=int, default=1, help="Starting seed")
    parser.add_argument(
        "--n-seeds", type=int, default=5, help="Number of consecutive seeds to run"
    )
    parser.add_argument(
        "--seeds", type=str, default="", help="Comma-separated explicit seed list"
    )
    parser.add_argument(
        "--steps", type=int, default=20000, help="Number of update steps"
    )
    parser.add_argument(
        "--sample-every",
        type=int,
        default=2000,
        help="Sampling interval for post-burn-in samples",
    )
    parser.add_argument("--burn-in", type=int, default=0, help="Burn-in steps")
    parser.add_argument(
        "--max-memory", type=int, default=3000, help="Maximum memory horizon"
    )
    parser.add_argument("--epsilon", type=float, default=0.03, help="Noise step size")
    parser.add_argument("--eta", type=float, default=0.15, help="Gradient strength")
    parser.add_argument(
        "--alpha", type=float, default=0.002, help="Memory decay parameter"
    )
    parser.add_argument(
        "--sigma-rep", type=float, default=1.0, help="Repulsive kernel width"
    )
    parser.add_argument(
        "--sigma-att", type=float, default=3.0, help="Attractive kernel width"
    )
    parser.add_argument(
        "--amplitude-rep", type=float, default=1.0, help="Repulsive kernel amplitude"
    )
    parser.add_argument(
        "--amplitude-att", type=float, default=0.35, help="Attractive kernel amplitude"
    )
    parser.add_argument(
        "--memory-factor", type=float, default=6.0, help="Memory factor for horizon"
    )
    parser.add_argument(
        "--voxel-size",
        type=float,
        default=0.5,
        help="Voxel size for residence statistics",
    )
    parser.add_argument(
        "--n-scales",
        type=int,
        default=10,
        help="Number of box scales for occupancy dimension fit",
    )
    parser.add_argument(
        "--min-count",
        type=int,
        default=2,
        help="Minimum number of occupied boxes per scale",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="highN_regime_ensemble.json",
        help="Output JSON file",
    )
    parser.add_argument(
        "--fast",
        action="store_true",
        help=(
            "Use a smaller memory horizon for a quicker smoke validation run. "
            "This changes only the validation convenience, not the main regime parameters."
        ),
    )
    return parser.parse_args()


def parse_seed_list(seed_text: str, start: int, count: int) -> list[int]:
    if not seed_text:
        return [start + i for i in range(count)]
    seeds = [int(item.strip()) for item in seed_text.split(",") if item.strip()]
    if not seeds:
        raise ValueError("--seeds must contain at least one integer")
    return seeds


def run_seed(
    cfg: SimulationConfig,
    seed: int,
    *,
    voxel_size: float,
    n_scales: int,
    min_count: int,
) -> dict:
    result = simulate_finite_memory(cfg, seed=seed)
    samples = result["samples"]
    d_cov = covariance_dimension(samples)
    occ_result = occupancy_dimension(
        samples,
        n_scales=n_scales,
        min_count=min_count,
        return_details=True,
    )
    return {
        "seed": seed,
        "D_cov": float(d_cov),
        "D_occ": float(occ_result.dimension),
        "occupancy_scales": occ_result.scales.tolist(),
        "occupancy_counts": occ_result.counts.tolist(),
        "residence": residence_statistics(samples, voxel_size=voxel_size, min_visits=3),
        "n_samples": int(len(samples)),
    }


def summarize(values: list[float], name: str) -> dict[str, float]:
    mean, lo, hi = bootstrap_mean_ci(values, level=0.95, n_boot=1000, seed=0)
    std = float(__import__("numpy").std(values, ddof=1)) if len(values) > 1 else 0.0
    return {
        "mean": float(mean),
        "std": std,
        "ci_95_lo": float(lo),
        "ci_95_hi": float(hi),
    }


def main() -> None:
    args = parse_args()
    if args.fast and args.max_memory == 3000:
        args.max_memory = 1000

    seeds = parse_seed_list(args.seeds, args.seed_start, args.n_seeds)
    cfg = SimulationConfig(
        steps=args.steps,
        dim=7,
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

    runs = []
    start = time.perf_counter()
    for seed in seeds:
        print(f"Running seed={seed}...")
        runs.append(
            run_seed(
                cfg,
                seed,
                voxel_size=args.voxel_size,
                n_scales=args.n_scales,
                min_count=args.min_count,
            )
        )
    elapsed = time.perf_counter() - start

    d_cov_values = [run["D_cov"] for run in runs]
    d_occ_values = [
        run["D_occ"] for run in runs if not __import__("math").isnan(run["D_occ"])
    ]

    stats = {
        "seed_list": seeds,
        "steps": args.steps,
        "sample_every": args.sample_every,
        "burn_in": args.burn_in,
        "max_memory": args.max_memory,
        "fast_mode": bool(args.fast),
        "voxel_size": args.voxel_size,
        "n_seeds": len(seeds),
        "elapsed_seconds": float(elapsed),
        "steps_per_second": (
            float(args.steps * len(seeds) / elapsed) if elapsed > 0 else None
        ),
        "regime": {
            "dim": 7,
            "epsilon": args.epsilon,
            "eta": args.eta,
            "alpha": args.alpha,
            "sigma_rep": args.sigma_rep,
            "sigma_att": args.sigma_att,
            "amplitude_rep": args.amplitude_rep,
            "amplitude_att": args.amplitude_att,
            "memory_factor": args.memory_factor,
        },
        "runs": runs,
        "D_cov_stats": summarize(d_cov_values, "D_cov"),
        "D_occ_stats": (
            summarize(d_occ_values, "D_occ")
            if d_occ_values
            else {
                "mean": float("nan"),
                "std": float("nan"),
                "ci_95_lo": float("nan"),
                "ci_95_hi": float("nan"),
            }
        ),
    }

    output_path = Path(args.output)
    if not output_path.is_absolute():
        output_path = ROOT / output_path
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(stats, indent=2, sort_keys=True))

    print(f"Wrote ensemble result to {output_path}")
    print(json.dumps(stats, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
