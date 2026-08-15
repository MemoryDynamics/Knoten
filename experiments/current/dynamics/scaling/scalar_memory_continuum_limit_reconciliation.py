"""Run the preregistered scalar-memory continuum-limit reconciliation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any

import numpy as np


def _repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("repository root not found")


ROOT = _repo_root()
sys.path.insert(0, str(ROOT))

from experiments.current.dynamics.scaling import (
    scalar_memory_continuum_limit_gate as original,
)


DEFAULT_REPORT = Path(
    "reports/dynamics/limits/"
    "scalar_memory_continuum_limit_reconciliation_2026-08-15.md"
)
DEFAULT_SUMMARY = Path(
    "reports/dynamics/limits/"
    "scalar_memory_continuum_limit_reconciliation_2026-08-15.json"
)
DEFAULT_FIGURE = Path(
    "figures/draft/dynamics/limits/"
    "scalar_memory_continuum_limit_reconciliation_2026-08-15.png"
)
PREREGISTRATION = Path(
    "reports/project/meta/preregistration/"
    "scalar_memory_continuum_limit_reconciliation_protocol_2026-08-15.md"
)
ORIGINAL_REPORT = Path(
    "reports/dynamics/limits/scalar_memory_continuum_limit_gate_2026-08-15.md"
)
RECONCILIATION_SEEDS = (6, 7, 8, 9, 10)
LOCAL_RADIUS_LIMIT = 0.02
RADIUS_RATIO_BOUNDS = (0.95, 1.05)


def _median(values: list[float]) -> float:
    if not values or not np.isfinite(values).all():
        raise ValueError("registered diagnostic collection must be finite")
    return float(np.median(values))


def _evaluate_reconciliation_gates(
    cases: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    every = list(cases.values())
    even_values = [
        float(row["mirror_even_maximum"])
        for case in every
        for seed in case["seeds"]
        for row in seed["fractions"]
    ]
    strength_rms = [
        float(seed["strength_nonlinearity_rms"])
        for case in every
        for seed in case["seeds"]
    ]
    strength_max = [
        float(seed["strength_nonlinearity_maximum"])
        for case in every
        for seed in case["seeds"]
    ]
    seed_rows = [seed for case in every for seed in case["seeds"]]
    ratio_minima = [
        float(seed["minimum_simultaneous_branch_control_radius_ratio"])
        for seed in seed_rows
        if seed["minimum_simultaneous_branch_control_radius_ratio"] is not None
    ]
    ratio_maxima = [
        float(seed["maximum_simultaneous_branch_control_radius_ratio"])
        for seed in seed_rows
        if seed["maximum_simultaneous_branch_control_radius_ratio"] is not None
    ]
    all_radii_valid = all(
        bool(seed["all_memory_radii_positive_finite"]) for seed in seed_rows
    )
    all_ratios_available = (
        len(ratio_minima) == len(seed_rows) == len(ratio_maxima)
    )
    maximum_scaled_radius = max(
        float(seed["maximum_memory_radius"]) / original.SIGMA_REP
        for seed in seed_rows
    )
    minimum_ratio = min(ratio_minima) if ratio_minima else None
    maximum_ratio = max(ratio_maxima) if ratio_maxima else None
    g0_checks = {
        "analytic_reference": max(
            float(case["maximum_analytic_recurrence_residual"])
            for case in every
        )
        <= 1.0e-12,
        "mirror_even_median": _median(even_values) <= 1.0e-3,
        "mirror_even_maximum": max(even_values) <= 1.0e-2,
        "strength_median": _median(strength_rms) <= 1.0e-3,
        "strength_maximum": max(strength_max) <= 1.0e-2,
        "all_memory_radii_positive_finite": all_radii_valid,
        "local_radius_maximum": maximum_scaled_radius <= LOCAL_RADIUS_LIMIT,
        "simultaneous_radius_ratio_lower": bool(
            all_ratios_available
            and minimum_ratio is not None
            and minimum_ratio >= RADIUS_RATIO_BOUNDS[0]
        ),
        "simultaneous_radius_ratio_upper": bool(
            all_ratios_available
            and maximum_ratio is not None
            and maximum_ratio <= RADIUS_RATIO_BOUNDS[1]
        ),
    }
    g0 = all(g0_checks.values())

    original_components = original._evaluate_gates(cases)
    tail = original_components["finite_tail_convergence"]
    alpha = original_components["matched_alpha_convergence"]
    g1_components = bool(tail["component_checks_pass"])
    g2_components = bool(alpha["component_checks_pass"])
    g1 = g0 and g1_components
    g2 = g0 and g2_components

    if not g0:
        decision = "reconciliation-experiment-inadequate"
    elif g1 and g2:
        decision = "continuum-limit-supported-in-prospective-reconciliation"
    else:
        decision = "registered-continuum-limit-not-supported-in-reconciliation"

    return {
        "corrected_experimental_validity": {
            "pass": g0,
            "status": "pass" if g0 else "fail",
            "checks": g0_checks,
            "maximum_radius_over_sigma_rep": maximum_scaled_radius,
            "minimum_simultaneous_branch_control_radius_ratio": minimum_ratio,
            "maximum_simultaneous_branch_control_radius_ratio": maximum_ratio,
        },
        "finite_tail_convergence": {
            **tail,
            "pass": g1,
            "status": "blocked" if not g0 else ("pass" if g1_components else "fail"),
        },
        "matched_alpha_convergence": {
            **alpha,
            "pass": g2,
            "status": "blocked" if not g0 else ("pass" if g2_components else "fail"),
        },
        "decision": decision,
    }


def run_reconciliation() -> dict[str, Any]:
    """Run the unchanged physical gates with prospective seeds and corrected G0."""

    payload = original.run_audit(seeds=RECONCILIATION_SEEDS)
    payload["schema"] = "emergenz-knoten.scalar-memory-continuum-reconciliation"
    payload["schema_version"] = 1
    payload["preregistration"] = PREREGISTRATION.as_posix()
    payload["original_audit"] = ORIGINAL_REPORT.as_posix()
    payload["registration"]["formation_seeds"] = RECONCILIATION_SEEDS
    payload["registration"]["corrected_radius_gate"] = {
        "local_radius_limit_over_sigma_rep": LOCAL_RADIUS_LIMIT,
        "simultaneous_branch_control_ratio_bounds": RADIUS_RATIO_BOUNDS,
    }
    payload["gates"] = _evaluate_reconciliation_gates(payload["cases"])
    payload["decision"] = payload["gates"]["decision"]
    payload["reconciliation_scope"] = {
        "changed": "G0 radius comparator and prospective seeds only",
        "unchanged": "model, matched axes, G1, G2, holdout and thresholds",
        "original_decision_preserved": "experiment-inadequate",
    }
    return payload


def _fmt(value: float | None) -> str:
    if value is None:
        return "unavailable"
    number = float(value)
    if abs(number) < 1.0e-3 or abs(number) >= 1.0e4:
        return f"{number:.4e}"
    return f"{number:.6f}"


def _write_report(payload: dict[str, Any], path: Path, figure: Path) -> None:
    cases = payload["cases"]
    gates = payload["gates"]
    validity = gates["corrected_experimental_validity"]
    tail = gates["finite_tail_convergence"]
    alpha_gate = gates["matched_alpha_convergence"]
    lines = [
        "# Scalar-memory continuum-limit reconciliation",
        "",
        "Date: 2026-08-15.",
        "",
        "## Verdict",
        "",
        f"Decision: **`{payload['decision']}`**.",
        "",
        "| gate | status |",
        "|---|:---:|",
        f"| corrected experimental validity | {validity['status']} |",
        f"| finite-tail convergence | {tail['status']} |",
        f"| matched-alpha convergence | {alpha_gate['status']} |",
        "",
        "This prospective reconciliation preserves the original",
        "`experiment-inadequate` decision. It changes only the invalid",
        "across-time radius comparator: every displaced branch is now compared",
        "with its simultaneous common-noise control at every response sample.",
        "Seeds 6--10 were fixed before the corrected diagnostic was implemented.",
        "",
        "## Corrected validity diagnostics",
        "",
        "| case | mirror-even max | strength max | max R/sigma_rep | simultaneous branch/control range | descriptive control endpoint range |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for case in original.registered_cases():
        row = cases[original._case_key(case.alpha, case.tail_extent)]
        lines.append(
            "| "
            f"alpha={case.alpha:g}, C={case.tail_extent:g} | "
            f"{_fmt(row['maximum_mirror_even_maximum'])} | "
            f"{_fmt(row['maximum_strength_nonlinearity_maximum'])} | "
            f"{_fmt(row['maximum_memory_radius'] / original.SIGMA_REP)} | "
            f"{_fmt(row['minimum_simultaneous_branch_control_radius_ratio'])}.."
            f"{_fmt(row['maximum_simultaneous_branch_control_radius_ratio'])} | "
            f"{_fmt(row['minimum_control_radius_ratio'])}.."
            f"{_fmt(row['maximum_control_radius_ratio'])} |"
        )

    lines.extend(
        [
            "",
            "The last column is retained only to demonstrate why the original",
            "endpoint gate was non-discriminating; it has no gate role here.",
            "",
            "## Registered matched family",
            "",
            "| alpha | C | H | tail mass | exact-response fitted rate | observed rate | exact response error | continuum response error |",
            "|---:|---:|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for case in original.registered_cases():
        row = cases[original._case_key(case.alpha, case.tail_extent)]
        finite = row["case"]
        lines.append(
            "| "
            f"{case.alpha:.6f} | {case.tail_extent:.6f} | {case.horizon} | "
            f"{_fmt(finite['tail_mass_fraction'])} | "
            f"{_fmt(row['median_reference_fitted_rate'])} | "
            f"{_fmt(row['median_fitted_rate'])} | "
            f"{_fmt(row['median_normalized_rms_error_exact'])} | "
            f"{_fmt(row['median_normalized_rms_error_continuum'])} |"
        )

    lines.extend(
        [
            "",
            "## Figure",
            "",
            f"![Continuum-limit reconciliation]({original._relative(path, figure)})",
            "",
            "## Interpretation boundary",
            "",
            "Evidence: the prospective common-noise branches remain locally",
            "perturbative, the nonlinear finite-memory simulation agrees with",
            "the exact finite-H response, tail sensitivity contracts, and the",
            "matched-alpha family approaches the registered exponential.",
            "",
            "Inference conditional on a complete pass: this constructed local",
            "scalar memory-centre family has a controlled finite-tail and",
            "small-alpha limit under fixed chi, D and alpha*H.",
            "",
            "Not established: emergence or uniqueness of the scaling, physical",
            "mass, momentum, underdamped inertia, a force-work normalization,",
            "nonlinear knot persistence, or physical continuum time.",
            "",
            "## Provenance",
            "",
            f"- Reconciliation protocol: [{PREREGISTRATION.name}]({original._relative(path, original._resolve(PREREGISTRATION))}).",
            f"- Original audit: [{ORIGINAL_REPORT.name}]({original._relative(path, original._resolve(ORIGINAL_REPORT))}).",
            f"- Simulation revision: `{payload['simulation_revision']}`.",
            f"- Git status at execution: `{payload['git_status'] or 'clean'}`.",
            "- Five prospective formation seeds and Brownian-coarsened common noise.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--summary-json", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--figure", type=Path, default=DEFAULT_FIGURE)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = run_reconciliation()
    report = original._resolve(args.report)
    summary = original._resolve(args.summary_json)
    figure = original._resolve(args.figure)
    original._write_json(summary, payload)
    original._write_figure(payload, figure)
    _write_report(payload, report, figure)
    print(json.dumps({"decision": payload["decision"], "report": str(report)}))


if __name__ == "__main__":
    main()
