"""Arithmetic on archived AL1 outputs only; no imports of any solver.

The observed changes below are not bounds on continuum or model errors.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path


HBARC_GEV_FM = 0.1973269804
HBARC_SOURCE = "https://physics.nist.gov/cgi-bin/cuu/Value?hbcmevf%7Csearch_for=c"
PDG_MOMENT_RATIO = -0.6849793
PDG_SOURCE = "https://pdg.lbl.gov/2025/reviews/rpp2025-rev-quark-model.pdf"


def summarize(report: dict) -> dict:
    if (
        report["mode"] != "al1"
        or report["claim_class"] != "assumed_quantum_reference_only"
        or report["sector"] not in ("nucleon", "delta")
        or [level["level"] for level in report["levels"]] != [0, 1, 2]
    ):
        raise ValueError("complete three-level AL1 reference archive required")
    rows = []
    for level in report["levels"]:
        if [s["relative_cutoff"] for s in level["solutions"]] != [1e-10, 1e-12]:
            raise ValueError("both frozen cutoffs required, in their original order")
        for solution in level["solutions"]:
            solver, obs = solution["solver"], solution["observables"]
            row = {
                "level": level["level"],
                "cutoff": solution["relative_cutoff"],
                "rank": solver["rank"],
                "raw_dimension": solver["raw_dimension"],
                "energy_MeV": 1000 * solver["energy"],
                "matter_rms_fm": HBARC_GEV_FM * math.sqrt(obs["matter_radius2"]),
                "charged_rms_NR_fm": HBARC_GEV_FM * math.sqrt(obs["charge_p_radius2"]),
                "neutral_radius2_NR_fm2": HBARC_GEV_FM**2 * obs["charge_n_radius2"],
                "up_spin": obs["up_spin"],
                "down_spin": obs["down_spin"],
                "mean_constituent_v2_proxy": obs["mean_constituent_v2_proxy"],
            }
            if report["sector"] == "nucleon":
                up, down = obs["up_spin"], obs["down_spin"]
                proton = (2 * up - down) / 3
                neutron = (2 * down - up) / 3
                row.update(
                    {
                        "mu_p_in_e_over_2m": proton,
                        "mu_n_in_e_over_2m": neutron,
                        "mu_n_over_mu_p": neutron / proton,
                        "moment_ratio_relative_difference_from_PDG": abs(
                            neutron / proton / PDG_MOMENT_RATIO - 1
                        ),
                    }
                )
            rows.append(row)
    last_change = abs(rows[4]["energy_MeV"] - rows[2]["energy_MeV"])
    cutoff_change = max(
        abs(rows[i]["energy_MeV"] - rows[i + 1]["energy_MeV"]) for i in (0, 2, 4)
    )
    return {
        "sector": report["sector"],
        "runner_decision": report["decision"],
        "elapsed_seconds": report["elapsed_seconds"],
        "rows": rows,
        "last_energy_change_MeV": last_change,
        "max_cutoff_energy_difference_MeV": cutoff_change,
        "max_relative_matrix_residual": max(
            s["solver"]["relative_matrix_residual"]
            for level in report["levels"]
            for s in level["solutions"]
        ),
    }


def compare(nucleon: dict, delta: dict) -> dict:
    if nucleon["sector"] != "nucleon" or delta["sector"] != "delta":
        raise ValueError("nucleon then delta archives required")
    if nucleon["hamiltonian"] != delta["hamiltonian"]:
        raise ValueError("cannot compare different Hamiltonians")
    if nucleon["script_sha256"] != delta["script_sha256"]:
        raise ValueError("cannot compare different solver versions")
    sectors = [summarize(nucleon), summarize(delta)]
    gap = sectors[1]["rows"][4]["energy_MeV"] - sectors[0]["rows"][4]["energy_MeV"]
    changes = sum(
        s["last_energy_change_MeV"] + s["max_cutoff_energy_difference_MeV"]
        for s in sectors
    )
    passed = all(
        s["runner_decision"] == "finite-basis-consistency-pass" for s in sectors
    )
    return {
        "claim_class": "archive_arithmetic_not_a_new_eigenproblem",
        "hbarc_GeV_fm": HBARC_GEV_FM,
        "hbarc_source": HBARC_SOURCE,
        "PDG_moment_ratio_comparison_only": PDG_MOMENT_RATIO,
        "PDG_source": PDG_SOURCE,
        "sectors": sectors,
        "delta_minus_nucleon_MeV": gap,
        "sum_observed_energy_changes_MeV_not_error_bound": changes,
        "finite_basis_ordering_separated": passed and gap > changes,
        "continuum_error_certified": False,
        "memory_emergence_claimed": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--nucleon", type=Path, required=True)
    parser.add_argument("--delta", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    paths = [args.nucleon, args.delta]
    contents = [path.read_bytes() for path in paths]
    result = compare(*(json.loads(content) for content in contents))
    result["input_sha256"] = {
        path.name: hashlib.sha256(content).hexdigest()
        for path, content in zip(paths, contents, strict=True)
    }
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, indent=2, allow_nan=False)
        stream.write("\n")
    print(json.dumps(result, allow_nan=False))


if __name__ == "__main__":
    main()
