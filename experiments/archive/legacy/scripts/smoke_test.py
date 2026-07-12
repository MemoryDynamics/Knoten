from __future__ import annotations

import json
import sys
from pathlib import Path

def _repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("repository root not found")


ROOT = _repo_root()

sys.path.insert(0, str(ROOT / "src"))

from emergenz_knoten import (
    SimulationConfig,  # noqa: E402
    covariance_dimension,
    occupancy_dimension,
    residence_statistics,
    simulate_finite_memory,
)


def main() -> None:
    cfg = SimulationConfig(
        steps=2_000,
        dim=3,
        epsilon=0.03,
        eta=0.15,
        alpha=0.02,
        sigma_rep=1.0,
        sigma_att=3.0,
        sample_every=20,
        max_memory=300,
    )
    result = simulate_finite_memory(cfg, seed=1)
    samples = result["samples"]
    stats = {
        "samples": int(len(samples)),
        "dim": int(samples.shape[1]),
        "D_cov": covariance_dimension(samples),
        "D_occ": occupancy_dimension(samples),
        "residence": residence_statistics(samples, voxel_size=0.5, min_visits=3),
    }
    print(json.dumps(stats, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
