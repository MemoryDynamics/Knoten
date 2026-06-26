from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from emergenz_knoten import SimulationConfig, covariance_dimension, residence_statistics
from emergenz_knoten.anchor import (
    estimate_transfer_operator,
    simulate_augmented_features,
    vector_autocorrelation,
)


def _float_list(values: np.ndarray, *, limit: int | None = None) -> list[float]:
    arr = np.asarray(values)
    if limit is not None:
        arr = arr[:limit]
    return [float(v) for v in arr]


def _complex_summary(values: np.ndarray, *, limit: int = 8) -> list[dict[str, float]]:
    out = []
    for value in np.asarray(values)[:limit]:
        out.append(
            {
                "real": float(np.real(value)),
                "imag": float(np.imag(value)),
                "abs": float(abs(value)),
            }
        )
    return out


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Run a reproducible Paper-0 anchor sweep with augmented-state "
            "features and a simple transfer-operator estimate."
        )
    )
    parser.add_argument("--steps", type=int, default=3000)
    parser.add_argument("--burn-in", type=int, default=300)
    parser.add_argument("--sample-every", type=int, default=10)
    parser.add_argument("--dim", type=int, default=3)
    parser.add_argument("--seeds", type=int, nargs="+", default=[1, 2])
    parser.add_argument("--alpha", type=float, nargs="+", default=[0.02, 0.05])
    parser.add_argument("--epsilon", type=float, default=0.03)
    parser.add_argument("--eta", type=float, default=0.15)
    parser.add_argument("--sigma-rep", type=float, default=1.0)
    parser.add_argument("--sigma-att", type=float, default=3.0)
    parser.add_argument("--amplitude-rep", type=float, default=1.0)
    parser.add_argument("--amplitude-att", type=float, default=0.35)
    parser.add_argument("--max-memory", type=int, default=800)
    parser.add_argument("--memory-factor", type=float, default=6.0)
    parser.add_argument("--voxel-size", type=float, default=0.75)
    parser.add_argument("--feature-voxel-size", type=float, default=1.0)
    parser.add_argument("--lag", type=int, default=3)
    parser.add_argument("--max-ac-lag", type=int, default=10)
    parser.add_argument(
        "--output",
        type=str,
        default="results/anchor_paper/pipeline_summary.json",
        help="JSON output path relative to the repository root unless absolute.",
    )
    return parser.parse_args()


def run_case(args: argparse.Namespace, *, alpha: float, seed: int) -> dict[str, Any]:
    config = SimulationConfig(
        steps=args.steps,
        dim=args.dim,
        epsilon=args.epsilon,
        eta=args.eta,
        alpha=alpha,
        sigma_rep=args.sigma_rep,
        sigma_att=args.sigma_att,
        amplitude_rep=args.amplitude_rep,
        amplitude_att=args.amplitude_att,
        memory_factor=args.memory_factor,
        max_memory=args.max_memory,
        burn_in=args.burn_in,
        sample_every=args.sample_every,
    )
    result = simulate_augmented_features(config, seed=seed)
    samples = result["samples"]
    features = result["augmented_features"]

    if len(samples) <= args.lag:
        raise ValueError("not enough samples for the requested transfer lag")

    transfer = estimate_transfer_operator(
        features,
        voxel_size=args.feature_voxel_size,
        lag=args.lag,
        lag_time=float(args.lag * args.sample_every),
    )
    ac = vector_autocorrelation(samples, max_lag=args.max_ac_lag)

    return {
        "seed": seed,
        "alpha": alpha,
        "n_samples": int(len(samples)),
        "feature_names": result["feature_names"].tolist(),
        "covariance_dimension": float(covariance_dimension(samples)),
        "residence": residence_statistics(
            samples, voxel_size=args.voxel_size, min_visits=3
        ),
        "position_autocorrelation": _float_list(ac),
        "transfer": {
            "lag_samples": int(args.lag),
            "lag_updates": int(args.lag * args.sample_every),
            "n_states": int(transfer.transition_matrix.shape[0]),
            "nonzero_transitions": int(np.count_nonzero(transfer.counts)),
            "empty_rows_handled": int(len(transfer.empty_rows)),
            "eigenvalues": _complex_summary(transfer.eigenvalues),
            "relaxation_rates": _float_list(transfer.relaxation_rates, limit=8),
        },
    }


def main() -> None:
    args = parse_args()
    cases = [
        run_case(args, alpha=alpha, seed=seed)
        for alpha in args.alpha
        for seed in args.seeds
    ]
    payload: dict[str, Any] = {
        "description": "Paper-0 anchor sweep: augmented features and transfer diagnostics.",
        "parameters": {
            "steps": args.steps,
            "burn_in": args.burn_in,
            "sample_every": args.sample_every,
            "dim": args.dim,
            "epsilon": args.epsilon,
            "eta": args.eta,
            "sigma_rep": args.sigma_rep,
            "sigma_att": args.sigma_att,
            "amplitude_rep": args.amplitude_rep,
            "amplitude_att": args.amplitude_att,
            "max_memory": args.max_memory,
            "memory_factor": args.memory_factor,
            "voxel_size": args.voxel_size,
            "feature_voxel_size": args.feature_voxel_size,
            "lag": args.lag,
            "max_ac_lag": args.max_ac_lag,
        },
        "cases": cases,
    }

    output_path = Path(args.output)
    if not output_path.is_absolute():
        output_path = ROOT / output_path
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(f"Wrote anchor pipeline summary to {output_path}")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
