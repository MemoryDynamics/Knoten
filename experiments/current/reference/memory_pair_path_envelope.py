"""Read one saved preparation and evaluate fixed analytical constants only."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np

from emergenz_knoten.kernels import ScalarReadoutKernel
from emergenz_knoten.pair_path_envelope import (
    pair_path_envelope,
    truncated_contrast_budget,
)


ROOT = Path(__file__).resolve().parents[3]
REPORT = "reports/response/reciprocal/reciprocal_full_knot_gate_2026-08-04.json"


def evaluate(root):
    text = (root / REPORT).read_text(encoding="utf-8")
    report = json.loads(text)
    checkpoint = root / report["checkpoint"]
    with np.load(checkpoint, allow_pickle=False) as saved:
        point, memory, weights = saved["x"], saved["memory"], saved["weights"]
    config, derived = report["config"], report["derived"]
    if config["deposition_kernel"] != "delta":
        raise ValueError("this archival illustration requires delta deposition")
    center = np.average(memory, weights=weights, axis=0)
    u, y = point - center, memory - center
    r = np.asarray(derived["initial_center_separation"])
    rotation = np.asarray(derived["second_state_rotation"])
    points = np.array([u - r / 2, rotation @ u + r / 2])
    histories = np.array([y - r / 2, y @ rotation.T + r / 2])
    geometric = (
        config["memory_mass"]
        * config["alpha"]
        * (1 - config["alpha"]) ** np.arange(len(weights))
    )
    result = pair_path_envelope(
        points,
        histories,
        alpha=config["alpha"],
        eta=config["eta"],
        cross_eta=derived["cross_eta"],
        epsilon=config["epsilon"],
        memory_mass=config["memory_mass"],
        kernel=ScalarReadoutKernel(
            **{
                key: config[key]
                for key in ("sigma_rep", "sigma_att", "amplitude_rep", "amplitude_att")
            }
        ),
        updates=50000,
        diameter=0.01,
        gaussian_threshold=10.0,
    )
    return dict(
        schema="emergenz-knoten.memory-pair-path-envelope.v1",
        source_report=REPORT,
        source_report_sha256_utf8_lf=hashlib.sha256(text.encode("utf-8")).hexdigest(),
        checkpoint=report["checkpoint"],
        checkpoint_sha256=hashlib.sha256(checkpoint.read_bytes()).hexdigest(),
        geometric_weight_max_binary64_difference=float(
            np.max(np.abs(weights - geometric))
        ),
        target_trajectories_generated=0,
        parameter_search=False,
        envelope=result,
        hypothetical_two_pair_budget=truncated_contrast_budget(
            result, float(np.linalg.norm(r)), independent_pairs=2, family_size=6
        )
        if result["closes_numerically"]
        else None,
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-json", type=Path)
    args = parser.parse_args()
    text = json.dumps(evaluate(ROOT), indent=2, sort_keys=True) + "\n"
    if args.output_json:
        args.output_json.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
