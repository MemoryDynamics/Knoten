"""Fixed-window Gaussian moment arithmetic from archived parameters, no paths."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from time import perf_counter

import numpy as np

from emergenz_knoten.kernels import ScalarReadoutKernel
from emergenz_knoten.pair_gaussian_readout import linear_gaussian_pair_readout


ROOT = Path(__file__).resolve().parents[3]
ENVELOPE = "reports/reference/memory_pair_path_envelope_2026-11-01.json"


def evaluate(root):
    before = perf_counter()
    envelope_text = (root / ENVELOPE).read_text(encoding="utf-8")
    archive = json.loads(envelope_text)
    source_text = (root / archive["source_report"]).read_text(encoding="utf-8")
    source = json.loads(source_text)
    checkpoint = root / archive["checkpoint"]
    if (
        hashlib.sha256(source_text.encode()).hexdigest()
        != archive["source_report_sha256_utf8_lf"]
        or hashlib.sha256(checkpoint.read_bytes()).hexdigest()
        != archive["checkpoint_sha256"]
    ):
        raise ValueError("archived source identity changed")
    with np.load(checkpoint, allow_pickle=False) as saved:
        point, memory, weights = saved["x"], saved["memory"], saved["weights"]
    center = np.average(memory, weights=weights, axis=0)
    u, y = point - center, memory - center
    config, derived = source["config"], source["derived"]
    r = np.asarray(derived["initial_center_separation"])
    rotation = np.asarray(derived["second_state_rotation"])
    points = np.array([u - r / 2, rotation @ u + r / 2])
    histories = np.array([y - r / 2, y @ rotation.T + r / 2])
    e = archive["envelope"]
    alpha, q = config["alpha"], 1 - config["alpha"]
    probabilities = alpha * q ** np.arange(len(weights)) / (1 - q ** len(weights))
    centers = np.einsum("h,ihd->id", probabilities, histories)
    result = linear_gaussian_pair_readout(
        alpha=alpha,
        self_gain=e["self_gain"],
        cross_gain=e["cross_gain"],
        epsilon=config["epsilon"],
        points=points,
        centers=centers,
        separation=-r,
        weights=probabilities,
        start=10000,
        stop=50000,
        kernel=ScalarReadoutKernel(
            **{
                key: config[key]
                for key in ("sigma_rep", "sigma_att", "amplitude_rep", "amplitude_att")
            }
        ),
    )
    lam, g, h = e["common_multiplier"], e["self_gain"], e["cross_gain"]
    inner_error = (q / (1 - lam) + 1 / h) * e["nonlinear_update_bound"] + (
        1 / (1 - lam) + g / (alpha * h)
    ) * e["tail_update_bound"]
    readout_radius = np.linalg.norm(r) + 2 * e["inner_bound"]
    good_error = 12 * e["cubic_coefficient"] * readout_radius**2 * inner_error
    bad_error = (
        4 * e["global_gradient_bound"] * min(1, 2 * e["failure_probability_bound"])
    )
    return dict(
        schema="emergenz-knoten.memory-pair-gaussian-readout.v1",
        source_envelope=ENVELOPE,
        source_envelope_sha256_utf8_lf=hashlib.sha256(
            envelope_text.encode()
        ).hexdigest(),
        source_report=archive["source_report"],
        source_report_sha256_utf8_lf=archive["source_report_sha256_utf8_lf"],
        checkpoint=archive["checkpoint"],
        checkpoint_sha256=archive["checkpoint_sha256"],
        gaussian_comparison=result,
        comparison_transfer_budget=dict(
            claim_class="upper_bound_evaluation_not_actual_error_or_interval_certificate",
            inner_path_difference_bound=inner_error,
            paired_contrast_good_event_error_bound=float(good_error),
            paired_contrast_bad_event_expectation_bound=float(bad_error),
            paired_contrast_total_expectation_error_bound=float(good_error + bad_error),
        ),
        parameter_search=False,
        target_trajectories_generated=0,
        elapsed_seconds=perf_counter() - before,
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
