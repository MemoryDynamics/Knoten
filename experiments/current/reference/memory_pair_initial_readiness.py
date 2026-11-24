"""Geometry-only remainder bounds from the saved P3.1 initial checkpoint.

No trajectory integration, new random values, fitted parameters or target replay.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np

from emergenz_knoten.kernels import (
    effective_double_gaussian_parameters,
    two_scale_local_curvature,
)


ROOT = Path(__file__).resolve().parents[3]
REPORT = "reports/response/reciprocal/reciprocal_full_knot_gate_2026-08-04.json"


def initial_readiness(root: Path) -> dict:
    text = (root / REPORT).read_text(encoding="utf-8")
    report = json.loads(text)
    checkpoint = root / report["checkpoint"]
    with np.load(checkpoint, allow_pickle=False) as saved:
        point, memory, weights = saved["x"], saved["memory"], saved["weights"]
    probabilities = weights / weights.sum()
    center = probabilities @ memory
    z, u = memory - center, point - center
    separation = np.asarray(report["derived"]["initial_center_separation"])
    rotation = np.asarray(report["derived"]["second_state_rotation"])
    config = report["config"]
    effective = effective_double_gaussian_parameters(
        **{
            key: config[key]
            for key in (
                "dim",
                "sigma_rep",
                "sigma_att",
                "amplitude_rep",
                "amplitude_att",
                "deposition_kernel",
                "deposition_sigma",
            )
        }
    )
    curvature = two_scale_local_curvature(**effective)
    coefficient = (
        abs(effective["amplitude_rep"]) / effective["sigma_rep"] ** 4
        + abs(effective["amplitude_att"]) / effective["sigma_att"] ** 4
    ) / 2
    directions = []
    for name, displacement, mean_displacement in (
        ("A_reads_B", u - separation - z @ rotation.T, u - separation),
        ("B_reads_A", rotation @ u + separation - z, rotation @ u + separation),
    ):
        third = float(probabilities @ np.linalg.norm(displacement, axis=1) ** 3)
        bound = coefficient * third
        signal = float(abs(curvature) * np.linalg.norm(mean_displacement))
        directions.append(
            {
                "direction": name,
                "max_displacement": float(np.max(np.linalg.norm(displacement, axis=1))),
                "normalized_cubic_bound": bound,
                "normalized_linear_signal": signal,
                "bound_over_linear_signal": bound / signal if signal > 0 else None,
            }
        )
    return {
        "schema": "emergenz-knoten.memory-pair-initial-readiness.v1",
        "claim_class": "initial_snapshot_bound_only_not_a_path_or_statistical_power_bound",
        "report": REPORT,
        "report_sha256_utf8_lf": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "checkpoint": report["checkpoint"],
        "checkpoint_sha256": hashlib.sha256(checkpoint.read_bytes()).hexdigest(),
        "horizon": int(len(weights)),
        "dimension": int(len(point)),
        "initial_radius": report["derived"]["initial_radius"],
        "maximum_centered_source_radius": float(np.max(np.linalg.norm(z, axis=1))),
        "current_point_offset": float(np.linalg.norm(u)),
        "separation_norm": float(np.linalg.norm(separation)),
        "effective_kernel": effective,
        "curvature": curvature,
        "cubic_coefficient": coefficient,
        "directions": directions,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-json", type=Path)
    args = parser.parse_args()
    result = json.dumps(initial_readiness(ROOT), indent=2, sort_keys=True) + "\n"
    if args.output_json is None:
        print(result, end="")
    else:
        args.output_json.write_text(result, encoding="utf-8")


if __name__ == "__main__":
    main()
