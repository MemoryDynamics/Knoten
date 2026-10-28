"""Bounded reference runner. AL1 target execution needs separate user approval.

The default mode solves only a synthetic oscillator; it never selects AL1.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict
import hashlib
import json
import os
from pathlib import Path
from time import monotonic

import numpy as np
import scipy

from experiments.current.reference import nucleon_gaussian_basis as basis


CUTOFFS = (1e-10, 1e-12)


def level_result(matrices) -> dict:
    solutions = []
    for cutoff in CUTOFFS:
        solution = basis.ritz_ground(
            matrices["hamiltonian"], matrices["overlap"], relative_cutoff=cutoff
        )
        coefficients = solution.pop("coefficients")
        observable = basis.expectations(matrices, coefficients)
        solution["coefficients"] = coefficients.tolist()
        solution["metric_eigenvalues"] = solution["metric_eigenvalues"].tolist()
        solutions.append(
            {"relative_cutoff": cutoff, "solver": solution, "observables": observable}
        )
    return {"solutions": solutions}


def finite_basis_checks(levels: list[dict]) -> dict[str, bool]:
    """Numerical consistency only: never a continuum or QCD accuracy certificate."""
    if len(levels) != 3:
        return {"all_three_levels_completed": False}
    leading = [level["solutions"][0] for level in levels]
    checks = {
        "all_three_levels_completed": True,
        "last_energy_change_under_1_MeV": abs(
            leading[-1]["solver"]["energy"] - leading[-2]["solver"]["energy"]
        )
        <= 0.001,
        "energies_do_not_increase_over_0p01_MeV": all(
            b["solver"]["energy"] <= a["solver"]["energy"] + 1e-5
            for a, b in zip(leading, leading[1:])
        ),
        "unit_metric_norms": all(
            abs(s["solver"]["metric_norm"] - 1) < 1e-8
            for level in levels
            for s in level["solutions"]
        ),
        "matrix_residuals_under_1e_minus_8": all(
            s["solver"]["relative_matrix_residual"] < 1e-8
            for level in levels
            for s in level["solutions"]
        ),
        "charge_normalization": all(
            abs(s["observables"]["form_factor_p"] - 1) < 1e-8
            and abs(s["observables"]["form_factor_n"]) < 1e-8
            for level in levels
            for s in level["solutions"]
        ),
        "cutoff_energy_sensitivity_under_0p05_MeV": all(
            abs(
                level["solutions"][0]["solver"]["energy"]
                - level["solutions"][1]["solver"]["energy"]
            )
            <= 5e-5
            for level in levels
        ),
    }
    for observable, tolerance in (
        ("matter_radius2", 0.05),
        ("charge_p_radius2", 0.05),
        ("charge_n_radius2", 0.05),
        ("up_spin", 0.002),
        ("down_spin", 0.002),
    ):
        checks[f"last_change_{observable}"] = (
            abs(
                leading[-1]["observables"][observable]
                - leading[-2]["observables"][observable]
            )
            <= tolerance
        )
        checks[f"cutoff_sensitivity_{observable}"] = all(
            abs(
                level["solutions"][0]["observables"][observable]
                - level["solutions"][1]["observables"][observable]
            )
            <= tolerance / 10
            for level in levels
        )
    return checks


def execute(mode: str, sector: str) -> dict:
    if mode not in ("oscillator-preflight", "al1") or sector not in (
        "nucleon",
        "delta",
    ):
        raise ValueError("unsupported execution mode or sector")
    start = monotonic()
    preflight = mode == "oscillator-preflight"
    budget = 30 if preflight else 300
    deadline = start + budget
    model = (
        basis.Hamiltonian(mass=1, oscillator=0.125, constant=0.1)
        if preflight
        else basis.declared_al1()
    )
    report = {
        "schema": "emergenz-knoten.coupled-gaussian-reference.v1",
        "claim_class": "synthetic_solver_verification"
        if preflight
        else "assumed_quantum_reference_only",
        "mode": mode,
        "sector": sector,
        "hamiltonian": asdict(model),
        "budget_seconds": budget,
        "cutoffs": CUTOFFS,
        "levels": [],
        "numpy_version": np.__version__,
        "scipy_version": scipy.__version__,
        "openblas_num_threads": os.environ.get("OPENBLAS_NUM_THREADS"),
        "decision": "inconclusive",
        "not_claimed": [
            "Memory_emergence",
            "full_QCD",
            "continuum_convergence_certificate",
            "hydrogen_spectrum",
        ],
    }
    try:
        for level in range(1 if preflight else 3):
            exponents = basis.proposed_exponents(level)
            matrices = basis.assemble(exponents, sector, model, deadline=deadline)
            if monotonic() >= deadline:
                raise TimeoutError("deadline before diagonalization")
            result = level_result(matrices)
            result.update(
                {
                    "level": level,
                    "gaussians": len(exponents),
                    "exponents": [a.tolist() for a in exponents],
                    "elapsed_seconds": monotonic() - start,
                }
            )
            if not preflight:
                for solution in result["solutions"]:
                    solution["observables"]["mean_constituent_v2_proxy"] = (
                        2 * solution["observables"]["kinetic"] / (3 * model.mass)
                    )
            report["levels"].append(result)
            if monotonic() >= deadline:
                raise TimeoutError("deadline after diagonalization")
        if preflight:
            solutions = report["levels"][0]["solutions"]
            checks = {
                "exact_energy": all(
                    abs(s["solver"]["energy"] - 1.6) < 1e-9 for s in solutions
                ),
                "exact_radius": all(
                    abs(s["observables"]["matter_radius2"] - 2) < 1e-7
                    for s in solutions
                ),
                "exact_charge_radius": all(
                    abs(s["observables"]["charge_p_radius2"] - 2) < 1e-7
                    and abs(s["observables"]["charge_n_radius2"]) < 1e-7
                    for s in solutions
                ),
                "metric_norm": all(
                    abs(s["solver"]["metric_norm"] - 1) < 1e-9 for s in solutions
                ),
            }
            report["decision"] = (
                "synthetic-preflight-pass"
                if all(checks.values())
                else "synthetic-preflight-fail"
            )
        else:
            checks = finite_basis_checks(report["levels"])
            report["decision"] = (
                "finite-basis-consistency-pass"
                if all(checks.values())
                else "inconclusive"
            )
        report["checks"] = checks
    except TimeoutError as error:
        report["stop_reason"] = str(error)
        report["checks"] = {"completed_within_fixed_budget": False}
    report["elapsed_seconds"] = monotonic() - start
    paths = (
        Path(__file__),
        Path(basis.__file__),
        Path(basis.al1.__file__),
        Path(basis.al1.algebra.__file__),
    )
    report["script_sha256"] = {
        path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in paths
    }
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--mode",
        choices=("oscillator-preflight", "al1"),
        default="oscillator-preflight",
    )
    parser.add_argument("--sector", choices=("nucleon", "delta"), default="nucleon")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if os.environ.get("OPENBLAS_NUM_THREADS") != "1":
        parser.error("set OPENBLAS_NUM_THREADS=1 before starting this bounded runner")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    # Reserve the output before computing; an existing attempt is never replaced.
    with args.output.open("x", encoding="utf-8") as stream:
        result = execute(args.mode, args.sector)
        json.dump(result, stream, indent=2, allow_nan=False)
        stream.write("\n")
    print(
        json.dumps(
            {
                key: result[key]
                for key in ("mode", "sector", "decision", "elapsed_seconds")
            }
        )
    )
    if result["decision"] not in (
        "synthetic-preflight-pass",
        "finite-basis-consistency-pass",
    ):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
