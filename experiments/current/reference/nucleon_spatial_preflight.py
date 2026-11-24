"""Fixed-geometry AL1 operator audit; no spatial eigenproblem or Memory run."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np

from experiments.current.reference import nucleon_spin_flavor_reference as algebra


PAIRS = ((0, 1), (0, 2), (1, 2))
MASS_GEV = 0.315
KAPPA = 0.5069
KAPPA_SPIN = 1.8609
STRING_GEV2 = 0.1653
OFFSET_GEV = 0.8321
A_GEV_B_MINUS_1 = 1.6553
B = 0.2204
C_GEV4 = 2.02e-3
SOURCE = "https://arxiv.org/html/2506.20555v2#A1"
UPSTREAM_COMMIT = "0c56c3442f2b5e120d80db790d670a4f9f2edc12"


def spin_pair_operators() -> tuple[np.ndarray, ...]:
    """sigma_i dot sigma_j, not s_i dot s_j, in the existing 4^3 basis."""
    result = []
    for i, j in PAIRS:
        operator = np.zeros((64, 64), dtype=complex)
        for sigma in algebra.pauli_matrices():
            factors = [np.eye(4, dtype=complex) for _ in range(3)]
            factors[i] = factors[j] = np.kron(np.eye(2), sigma)
            operator += np.kron(np.kron(factors[0], factors[1]), factors[2])
        result.append(operator)
    return tuple(result)


def al1_local_terms(positions: np.ndarray) -> tuple[float, np.ndarray]:
    """Color-singlet scalar and sigma-pair coefficients, in GeV; input GeV^-1.

    The scalar includes 3m and the published constant three-body term.
    There is no kinetic operator here. Coincident points are singular.
    """
    positions = np.asarray(positions, dtype=float)
    if positions.shape != (3, 3) or not np.all(np.isfinite(positions)):
        raise ValueError("positions must be finite with shape (3, 3)")
    distances = np.array(
        [np.linalg.norm(positions[i] - positions[j]) for i, j in PAIRS]
    )
    if np.any(distances == 0):
        raise ValueError("coincident quarks have a singular color-Coulomb term")
    r0 = A_GEV_B_MINUS_1 * MASS_GEV ** (-B)
    central = 0.5 * np.sum(-KAPPA / distances + STRING_GEV2 * distances - OFFSET_GEV)
    spin = (
        np.pi
        * KAPPA_SPIN
        / (3 * MASS_GEV**2)
        * np.exp(-((distances / r0) ** 2))
        / (np.pi**1.5 * r0**3)
    )
    return float(3 * MASS_GEV + central - C_GEV4 / MASS_GEV**3), spin


def local_matrix(positions: np.ndarray) -> np.ndarray:
    scalar, coefficients = al1_local_terms(positions)
    return scalar * np.eye(64) + sum(
        c * operator
        for c, operator in zip(coefficients, spin_pair_operators(), strict=True)
    )


def factorization_residual(coefficients: np.ndarray, species: str) -> dict[str, float]:
    """Test invariance of the one-vector spin/flavor ansatz, not time stability."""
    coefficients = np.asarray(coefficients, dtype=float)
    if coefficients.shape != (3,) or not np.all(np.isfinite(coefficients)):
        raise ValueError("three finite pair coefficients are required")
    _, state, alternative = algebra.spin_flavor_states(species)
    operator = sum(
        c * pair for c, pair in zip(coefficients, spin_pair_operators(), strict=True)
    )

    def residual_squared(vector: np.ndarray) -> float:
        mean = np.vdot(vector, operator @ vector) / np.vdot(vector, vector)
        return float(np.linalg.norm(operator @ vector - mean * vector) ** 2)

    return {
        "spin_half_residual_squared": residual_squared(state),
        "analytic_residual_squared": float(
            6 * np.sum((coefficients - coefficients.mean()) ** 2)
        ),
        "spin_three_half_control_squared": residual_squared(alternative),
    }


def run_preflight() -> dict[str, object]:
    # Synthetic noncoincident geometry, not an optimized nucleon shape.
    triangle = np.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.25, 1.25, 0.0]])
    _, coefficients = al1_local_terms(triangle)
    unequal = factorization_residual(coefficients, "proton")
    equal = factorization_residual(np.ones(3), "proton")
    neutron = factorization_residual(coefficients, "neutron")
    shift = -C_GEV4 / MASS_GEV**3
    checks = {
        "unequal_pair_coefficients_leave_fixed_ansatz": unequal[
            "spin_half_residual_squared"
        ]
        > 1e-8,
        "analytic_leakage_identity": bool(
            np.isclose(
                unequal["spin_half_residual_squared"],
                unequal["analytic_residual_squared"],
                rtol=1e-12,
                atol=1e-15,
            )
        ),
        "equilateral_control_closed": equal["spin_half_residual_squared"] < 1e-25,
        "spin_three_half_control_closed": unequal["spin_three_half_control_squared"]
        < 1e-25,
        "isospin_partner_same_residual": bool(
            np.isclose(
                unequal["spin_half_residual_squared"],
                neutron["spin_half_residual_squared"],
                rtol=1e-12,
                atol=1e-15,
            )
        ),
        "constant_offset_between_64_and_65_MeV": 64 < -1000 * shift < 65,
    }
    paths = (Path(__file__), Path(algebra.__file__))
    return {
        "schema": "emergenz-knoten.nucleon-spatial-preflight.v1",
        "claim_class": "assumed_reference_operator_audit_only",
        "decision": "coupled_spatial_spin_channels_required"
        if all(checks.values())
        else "preflight-fail",
        "source": SOURCE,
        "upstream_reviewed_commit": UPSTREAM_COMMIT,
        "parameters": {
            "mass_GeV": MASS_GEV,
            "kappa": KAPPA,
            "kappa_spin": KAPPA_SPIN,
            "string_GeV2": STRING_GEV2,
            "offset_GeV": OFFSET_GEV,
            "A_GeV_B_minus_1": A_GEV_B_MINUS_1,
            "B": B,
            "C_GeV4": C_GEV4,
        },
        "synthetic_positions_GeV_inverse": triangle.tolist(),
        "pair_order_zero_based": PAIRS,
        "spin_pair_coefficients_GeV": coefficients.tolist(),
        "nonseparable_control_GeV_squared": unequal,
        "equal_coefficient_control_dimensionless": equal,
        "constant_three_body_shift_GeV": shift,
        "not_computed": [
            "spatial_wavefunction_or_mass_eigenvalue",
            "charge_or_magnetic_form_factors",
            "hydrogen_spectrum",
            "DeepQuark_training_or_reproduction",
            "Memory_emergence",
        ],
        "checks": checks,
        "numpy_version": np.__version__,
        "script_sha256": {
            path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in paths
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    report = run_preflight()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump(report, stream, indent=2, allow_nan=False)
        stream.write("\n")
    print(json.dumps({"decision": report["decision"], "checks": report["checks"]}))
    if not all(report["checks"].values()):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
