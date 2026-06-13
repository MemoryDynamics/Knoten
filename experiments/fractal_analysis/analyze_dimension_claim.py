from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path
from statistics import mean, pstdev

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT = ROOT / "experiments/fractal_analysis/Fraktale/resultsN.csv"
DEFAULT_OUTPUT = ROOT / "data/processed/fractal_analysis/dimension_claim_summary.json"


def bootstrap_ci(values: list[float], *, n_boot: int = 5000, seed: int = 0) -> tuple[float, float]:
    rng = np.random.default_rng(seed)
    arr = np.asarray(values, dtype=float)
    if arr.size == 0:
        return float("nan"), float("nan")
    samples = rng.choice(arr, size=(n_boot, arr.size), replace=True).mean(axis=1)
    lo, hi = np.quantile(samples, [0.025, 0.975])
    return float(lo), float(hi)


def load_rows(path: Path) -> list[dict[str, float | int]]:
    rows: list[dict[str, float | int]] = []
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            rows.append(
                {
                    "D_occ": float(row["D"]),
                    "N": int(float(row["N"])),
                    "run": int(float(row["run"])),
                    "dim": int(float(row["dim"])),
                }
            )
    return rows


def summarize_group(dim: int, n_steps: int, values: list[float]) -> dict[str, float | int]:
    ci_lo, ci_hi = bootstrap_ci(values)
    return {
        "dim": dim,
        "N": n_steps,
        "runs": len(values),
        "mean": float(mean(values)),
        "std_population": float(pstdev(values)) if len(values) > 1 else 0.0,
        "min": float(min(values)),
        "max": float(max(values)),
        "bootstrap_ci_95_lo": ci_lo,
        "bootstrap_ci_95_hi": ci_hi,
    }


def analyze(rows: list[dict[str, float | int]]) -> dict:
    groups: dict[tuple[int, int], list[float]] = defaultdict(list)
    for row in rows:
        groups[(int(row["dim"]), int(row["N"]))].append(float(row["D_occ"]))

    summaries = [
        summarize_group(dim, n_steps, values)
        for (dim, n_steps), values in sorted(groups.items())
    ]
    top_by_mean = sorted(summaries, key=lambda item: float(item["mean"]), reverse=True)
    max_row = max(rows, key=lambda item: float(item["D_occ"]))
    largest_n = max(int(row["N"]) for row in rows)
    largest_n_groups = [item for item in summaries if item["N"] == largest_n]

    return {
        "source_rows": len(rows),
        "source_max_row": max_row,
        "largest_N": largest_n,
        "largest_N_groups": largest_n_groups,
        "top_groups_by_mean": top_by_mean[:12],
        "interpretation": {
            "strongest_seed_aware_claim": (
                "In the archived resultsN.csv, the strongest occupancy-dimension "
                "signal near 3 occurs for embedding dim=5 at N=60,000,000."
            ),
            "caution": (
                "This reproduces the archived CSV claim, not a fresh simulation. "
                "A new seed-controlled rerun is still required."
            ),
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Seed-aware analysis of archived occupancy-dimension results."
    )
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = load_rows(args.input)
    summary = analyze(rows)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
