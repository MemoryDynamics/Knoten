from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

def _repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("repository root not found")


ROOT = _repo_root()

sys.path.insert(0, str(ROOT / "src"))

from emergenz_knoten import (
    SimulationConfig,
    covariance_dimension,
    occupancy_dimension,
    residence_statistics,
    simulate_finite_memory,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a pilot simulation for the legacy high-N 3D regime."
    )
    parser.add_argument("--seed", type=int, default=1, help="RNG seed")
    parser.add_argument(
        "--steps", type=int, default=10_000, help="Number of update steps"
    )
    parser.add_argument(
        "--sample-every",
        type=int,
        default=2_000,
        help="Sampling interval for post-burn-in samples",
    )
    parser.add_argument("--burn-in", type=int, default=0, help="Burn-in steps")
    parser.add_argument(
        "--max-memory", type=int, default=3_000, help="Maximum memory horizon"
    )
    parser.add_argument(
        "--output", type=str, default="highN_regime.json", help="Output JSON file"
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cfg = SimulationConfig(
        steps=args.steps,
        dim=7,
        epsilon=0.03,
        eta=0.15,
        alpha=0.002,
        sigma_rep=1.0,
        sigma_att=3.0,
        amplitude_rep=1.0,
        amplitude_att=0.35,
        memory_factor=6.0,
        max_memory=args.max_memory,
        burn_in=args.burn_in,
        sample_every=args.sample_every,
    )

    start = time.perf_counter()
    result = simulate_finite_memory(cfg, seed=args.seed)
    elapsed = time.perf_counter() - start

    samples = result["samples"]
    stats = {
        "seed": args.seed,
        "steps": args.steps,
        "sample_every": args.sample_every,
        "burn_in": args.burn_in,
        "max_memory": args.max_memory,
        "n_samples": int(len(samples)),
        "elapsed_seconds": float(elapsed),
        "steps_per_second": float(args.steps / elapsed) if elapsed > 0 else None,
        "D_cov": float(covariance_dimension(samples)),
        "D_occ": float(occupancy_dimension(samples)),
        "residence": residence_statistics(samples, voxel_size=0.5, min_visits=3),
    }

    output_path = Path(args.output)
    if not output_path.is_absolute():
        output_path = ROOT / output_path
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(stats, indent=2, sort_keys=True))

    print(f"Wrote high-N regime pilot results to {output_path}")
    print(json.dumps(stats, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
