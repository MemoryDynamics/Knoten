"""Independently recompute the registered N0 decision from its immutable JSON."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[4]
RESULT = ROOT / (
    "reports/dynamics/rotation/"
    "scalar_memory_rotating_wave_noise_stress_2026-08-31.json"
)
REPORT = RESULT.with_suffix(".md")
FIGURE = RESULT.with_suffix(".png")
DEFAULT_OUTPUT = ROOT / (
    "reports/project/meta/reviews/"
    "scalar_memory_rotating_wave_noise_stress_independent_recompute_2026-09-01.json"
)
EXPECTED_SEEDS = [2026083101, 2026083102, 2026083103]
EXPECTED_CHI = [0.0] + [10.0**exponent for exponent in range(-22, -1)]


def classify_resolution(row: dict[str, Any], chi: float) -> str:
    ratio = float(row["effective_to_intended_rms"])
    fraction = float(row["nonzero_fraction"])
    if chi == 0.0:
        return "deterministic-control"
    if ratio <= 0.1 or fraction <= 0.1:
        return "unresolved"
    if ratio >= 0.5 and fraction >= 0.5:
        return "resolved"
    return "partially-resolved"


def arm_pass(metrics: dict[str, Any]) -> bool:
    return bool(
        metrics["completed"]
        and metrics["finite"]
        and float(metrics["maximum_d0_fraction"]) <= 0.10
        and float(metrics["late_rms_d0_fraction"]) <= 0.05
        and float(metrics["maximum_radius_relative_error"]) <= 0.05
        and float(metrics["late_rms_phase_error_over_theta"]) <= 0.20
        and float(metrics["positive_chirality_fraction"]) >= 0.99
        and float(metrics["maximum_pair_growth"]) <= 10.0
        and float(metrics["final_pair_ratio"]) <= 0.1
        and not metrics["stopped"]
    )


def cell_decision(rows: list[tuple[str, bool]]) -> str:
    if any(label == "resolved" and not passed for label, passed in rows):
        return "stress-fail"
    if rows and all(label == "resolved" and passed for label, passed in rows):
        return "all-cell-stable"
    return "inconclusive"


def study_decision(decisions: list[str]) -> str:
    if "all-cell-stable" not in decisions:
        return "n0-noise-robustness-fail"
    if decisions[-1] == "all-cell-stable" and "stress-fail" not in decisions:
        return "n0-noise-stable-through-grid"
    for start in range(len(decisions) - 2):
        if decisions[start : start + 3] != ["all-cell-stable"] * 3:
            continue
        later_failures = [
            index
            for index in range(start + 3, len(decisions))
            if decisions[index] == "stress-fail"
        ]
        if not later_failures:
            continue
        first = later_failures[0]
        if "inconclusive" in decisions[start + 3 : first]:
            continue
        if "all-cell-stable" not in decisions[first + 1 :]:
            return "n0-noise-stability-window-bracketed"
    return "n0-inconclusive"


def scaling_fit(
    results: list[dict[str, Any]], candidate_name: str, start_chi: float
) -> float:
    grid_start = EXPECTED_CHI.index(start_chi)
    window = EXPECTED_CHI[grid_start : grid_start + 4]
    x_values = []
    y_values = []
    for chi in window:
        rows = [
            row
            for row in results
            if row["candidate_name"] == candidate_name
            and float(row["chi"]) == chi
        ]
        if len(rows) != 3:
            raise AssertionError("scaling window is incomplete")
        radius = float(rows[0]["radius_decimal"])
        x_seed = [
            float(row["resolutions"]["base"]["effective_rms"]) / radius
            for row in rows
        ]
        y_seed = [float(row["metrics"]["late_rms_d0_fraction"]) for row in rows]
        x_values.append(float(np.exp(np.mean(np.log(x_seed)))))
        y_values.append(float(np.exp(np.mean(np.log(y_seed)))))
    slope, _ = np.polyfit(np.log(x_values), np.log(y_values), 1)
    return float(slope)


def audit() -> dict[str, Any]:
    raw = RESULT.read_bytes()
    repository_raw = subprocess.run(
        ["git", "show", "HEAD:reports/dynamics/rotation/"
         "scalar_memory_rotating_wave_noise_stress_2026-08-31.json"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    ).stdout
    payload = json.loads(raw)
    normalized = raw.replace(b"\r\n", b"\n")
    report_text = REPORT.read_text(encoding="utf-8")
    digest_match = re.search(r"JSON SHA256: `([0-9a-f]+)`", report_text)
    if digest_match is None:
        raise AssertionError("report does not contain a JSON digest")
    byte_digest = hashlib.sha256(raw).hexdigest()
    repository_digest = hashlib.sha256(repository_raw).hexdigest()
    normalized_digest = hashlib.sha256(normalized).hexdigest()
    embedded_digest = digest_match.group(1)

    results = payload["results"]
    expected_order = [
        (candidate, chi, seed)
        for candidate in ("Anchor", "L3")
        for chi in EXPECTED_CHI
        for seed in EXPECTED_SEEDS
    ]
    actual_order = [
        (row["candidate_name"], float(row["chi"]), int(row["seed"]))
        for row in results
    ]
    resolution_mismatches = []
    gate_mismatches = []
    for index, row in enumerate(results):
        for arm in ("base", "pair"):
            recomputed = classify_resolution(row["resolutions"][arm], float(row["chi"]))
            stored = row["resolutions"][arm]["classification"]
            if recomputed != stored:
                resolution_mismatches.append([index, arm, stored, recomputed])
        recomputed_pass = arm_pass(row["metrics"])
        if recomputed_pass != bool(row["dynamic_pass"]):
            gate_mismatches.append([index, row["dynamic_pass"], recomputed_pass])

    grid = []
    for chi in EXPECTED_CHI[1:]:
        rows = [row for row in results if float(row["chi"]) == chi]
        arms = [
            (row["resolutions"][arm]["classification"], arm_pass(row["metrics"]))
            for row in rows
            for arm in ("base", "pair")
        ]
        grid.append({"chi": chi, "decision": cell_decision(arms)})
    recomputed_decision = study_decision([row["decision"] for row in grid])
    stable = [row["chi"] for row in grid if row["decision"] == "all-cell-stable"]
    failed = [row["chi"] for row in grid if row["decision"] == "stress-fail"]
    slopes = {
        name: {
            "registered_window": scaling_fit(results, name, 1.0e-15),
            "exploratory_next_window": scaling_fit(results, name, 1.0e-14),
        }
        for name in ("Anchor", "L3")
    }
    stored_grid = [
        {"chi": float(row["chi"]), "decision": row["decision"]}
        for row in payload["grid"]
    ]
    figure_signature = FIGURE.read_bytes()[:8]
    return {
        "schema": "scalar-memory-rotating-wave-noise-stress-independent-audit-v1",
        "source_revision": payload["provenance"]["revision"],
        "byte_sha256": byte_digest,
        "repository_blob_sha256": repository_digest,
        "lf_normalized_sha256": normalized_digest,
        "embedded_sha256": embedded_digest,
        "embedded_matches_bytes": embedded_digest == byte_digest,
        "embedded_matches_repository_blob": embedded_digest == repository_digest,
        "embedded_matches_lf_normalized": embedded_digest == normalized_digest,
        "integrity_finding": (
            "canonical-repository-hash-agrees"
            if embedded_digest == repository_digest and embedded_digest == byte_digest
            else (
                "working-tree-line-ending-transform-canonical-repository-hash-agrees"
                if embedded_digest == repository_digest
                and embedded_digest == normalized_digest
                else "unexpected-digest-state"
            )
        ),
        "json_valid": True,
        "png_signature_valid": figure_signature == b"\x89PNG\r\n\x1a\n",
        "exact_result_count": len(results) == 132,
        "exact_order": actual_order == expected_order,
        "resolution_mismatches": resolution_mismatches,
        "gate_mismatches": gate_mismatches,
        "grid_agrees": grid == stored_grid,
        "stored_decision": payload["decision"],
        "recomputed_decision": recomputed_decision,
        "decision_agrees": recomputed_decision == payload["decision"],
        "last_stable_chi": max(stable),
        "first_higher_failing_chi": min(value for value in failed if value > max(stable)),
        "scaling_slopes": slopes,
        "all_primary_checks_pass": bool(
            len(results) == 132
            and actual_order == expected_order
            and not resolution_mismatches
            and not gate_mismatches
            and grid == stored_grid
            and recomputed_decision == payload["decision"]
            and figure_signature == b"\x89PNG\r\n\x1a\n"
            and embedded_digest == repository_digest
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    output = args.output if args.output.is_absolute() else ROOT / args.output
    if output.resolve() != DEFAULT_OUTPUT.resolve():
        raise RuntimeError("independent N0 audit permits only its registered output")
    if output.exists():
        raise RuntimeError("refusing to overwrite independent N0 audit")
    result = audit()
    temporary = output.with_name(output.name + ".tmp")
    if temporary.exists():
        raise RuntimeError("refusing stale independent-audit temporary")
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary.write_text(
        json.dumps(result, allow_nan=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    temporary.replace(output)
    print(json.dumps({"decision_agrees": result["decision_agrees"]}))


if __name__ == "__main__":
    main()
