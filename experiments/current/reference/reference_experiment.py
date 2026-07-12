from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

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
        description="Run a reproducible reference experiment for the finite-memory model."
    )
    parser.add_argument("--seed", type=int, default=1, help="RNG seed")
    parser.add_argument("--steps", type=int, default=10_000, help="Number of update steps")
    parser.add_argument("--sample-every", type=int, default=25, help="Sampling interval")
    parser.add_argument("--burn-in", type=int, default=1_000, help="Burn-in steps")
    parser.add_argument(
        "--voxel-size",
        type=float,
        default=0.5,
        help="Voxel size for residence statistics",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="reference_experiment.json",
        help="Output JSON file",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cfg = SimulationConfig(
        steps=args.steps,
        dim=3,
        epsilon=0.03,
        eta=0.15,
        alpha=0.02,
        sigma_rep=1.0,
        sigma_att=3.0,
        amplitude_rep=1.0,
        amplitude_att=0.35,
        memory_factor=6.0,
        max_memory=800,
        burn_in=args.burn_in,
        sample_every=args.sample_every,
    )
    result = simulate_finite_memory(cfg, seed=args.seed)
    samples = result["samples"]

    if len(samples) < 2:
        raise ValueError(
            "Not enough post-burn-in samples for diagnostics. "
            "Increase steps, lower burn-in, or reduce sample_every."
        )

    stats = {
        "seed": args.seed,
        "steps": args.steps,
        "sample_every": args.sample_every,
        "burn_in": args.burn_in,
        "n_samples": int(len(samples)),
        "D_cov": float(covariance_dimension(samples)),
        "D_occ": float(occupancy_dimension(samples)),
        "residence": residence_statistics(
            samples, voxel_size=args.voxel_size, min_visits=3
        ),
    }

    output_path = Path(args.output)
    if not output_path.is_absolute():
        output_path = ROOT / output_path
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(stats, indent=2, sort_keys=True), encoding="utf-8")
    print(f"Wrote reference experiment results to {output_path}")
    print(json.dumps(stats, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
