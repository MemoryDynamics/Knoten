"""Finite-dimensional constituent-quark reference, not QCD or Memory emergence.

Inputs: three valence quarks, a symmetric spatial S wave, fundamental color,
spin-half quarks, u/d charges, and the symmetric spin-flavor ansatz. The
spin-half sector is selected algebraically, not by an energy Hamiltonian.
"""

from __future__ import annotations

import argparse
import hashlib
from itertools import permutations
import json
from pathlib import Path

import numpy as np


PDG_QUARK_MODEL = "https://pdg.lbl.gov/2025/reviews/rpp2025-rev-quark-model.pdf"
MEASURED_MOMENT_RATIO = -0.6849793  # PDG 2025, section 15.6; comparison only.
TOLERANCE = 5e-13


def pauli_matrices() -> tuple[np.ndarray, ...]:
    return (
        np.array([[0, 1], [1, 0]], dtype=complex),
        np.array([[0, -1j], [1j, 0]], dtype=complex),
        np.array([[1, 0], [0, -1]], dtype=complex),
    )


def tensor_sum(local: np.ndarray) -> np.ndarray:
    """Sum the same one-particle operator over three tensor factors."""
    identity = np.eye(local.shape[0])
    return (
        np.kron(np.kron(local, identity), identity)
        + np.kron(np.kron(identity, local), identity)
        + np.kron(np.kron(identity, identity), local)
    )


def symmetric_occupation(labels: tuple[int, int, int]) -> np.ndarray:
    """Normalized symmetrization in (u-up, u-down, d-up, d-down)^3."""
    distinct = sorted(set(permutations(labels)))
    state = np.zeros((4, 4, 4), dtype=complex)
    for label in distinct:
        state[label] = 1 / np.sqrt(len(distinct))
    return state.ravel()


def spin_flavor_states(species: str) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return S^2 eigenvalues and spin-half/three-half states at S_z=+1/2."""
    if species == "proton":
        occupations = ((0, 0, 3), (0, 1, 2))
    elif species == "neutron":
        occupations = ((2, 2, 1), (2, 3, 0))
    else:
        raise ValueError("species must be proton or neutron")
    basis = np.column_stack([symmetric_occupation(labels) for labels in occupations])
    spin = [tensor_sum(np.kron(np.eye(2), sigma / 2)) for sigma in pauli_matrices()]
    spin_squared = sum(operator @ operator for operator in spin)
    values, vectors = np.linalg.eigh(basis.conj().T @ spin_squared @ basis)
    states = basis @ vectors
    return values, states[:, 0], states[:, 1]


def color_singlet() -> np.ndarray:
    """Normalized epsilon_abc color wavefunction; an explicit model input."""
    state = np.zeros((3, 3, 3), dtype=complex)
    for labels in permutations(range(3)):
        inversions = sum(
            labels[i] > labels[j] for i in range(3) for j in range(i + 1, 3)
        )
        state[labels] = (-1) ** inversions / np.sqrt(6)
    return state.ravel()


def color_generators() -> tuple[np.ndarray, ...]:
    """Fundamental SU(3) generators with tr(T_a T_b)=delta_ab/2."""
    matrices = []
    for i, j in ((0, 1), (0, 2), (1, 2)):
        real = np.zeros((3, 3), dtype=complex)
        real[i, j] = real[j, i] = 0.5
        imaginary = np.zeros((3, 3), dtype=complex)
        imaginary[i, j], imaginary[j, i] = -0.5j, 0.5j
        matrices.extend((real, imaginary))
    matrices.extend(
        (np.diag([0.5, -0.5, 0.0]), np.diag([1.0, 1.0, -2.0]) / np.sqrt(12))
    )
    return tuple(matrices)


def _expectation(state: np.ndarray, operator: np.ndarray) -> float:
    return float(np.vdot(state, operator @ state).real)


def nucleon_observables(species: str) -> dict[str, object]:
    values, state, alternative = spin_flavor_states(species)
    spin = [tensor_sum(np.kron(np.eye(2), sigma / 2)) for sigma in pauli_matrices()]
    isospin = [tensor_sum(np.kron(sigma / 2, np.eye(2))) for sigma in pauli_matrices()]
    spin_squared = sum(operator @ operator for operator in spin)
    isospin_squared = sum(operator @ operator for operator in isospin)
    up_spin = tensor_sum(np.diag([1.0, -1.0, 0.0, 0.0]))
    down_spin = tensor_sum(np.diag([0.0, 0.0, 1.0, -1.0]))
    moment = (2 / 3) * up_spin - (1 / 3) * down_spin
    return {
        "sector_selection": "lowest_S_squared_not_lowest_energy",
        "basis_dimension": 64,
        "selected_symmetric_subspace_dimension": 2,
        "spin_squared_candidates_hbar2": values.tolist(),
        "norm_squared": float(np.vdot(state, state).real),
        "up_count": _expectation(state, tensor_sum(np.diag([1.0, 1.0, 0.0, 0.0]))),
        "charge_over_e": _expectation(
            state, tensor_sum(np.diag([2 / 3, 2 / 3, -1 / 3, -1 / 3]))
        ),
        "spin_squared_hbar2": _expectation(state, spin_squared),
        "spin_z_hbar": _expectation(state, spin[2]),
        "isospin_squared": _expectation(state, isospin_squared),
        "spin_half_eigenstate_residual": float(
            np.linalg.norm(spin_squared @ state - 0.75 * state)
        ),
        "spin_three_half_control_residual": float(
            np.linalg.norm(spin_squared @ alternative - 3.75 * alternative)
        ),
        "up_spin_weight": _expectation(state, up_spin),
        "down_spin_weight": _expectation(state, down_spin),
        "moment_in_common_constituent_magneton": _expectation(state, moment),
        "spin_flavor_exchange_residual": max(
            float(np.linalg.norm(state.reshape(4, 4, 4).swapaxes(i, j).ravel() - state))
            for i, j in ((0, 1), (0, 2), (1, 2))
        ),
    }


def run_reference() -> dict[str, object]:
    proton, neutron = nucleon_observables("proton"), nucleon_observables("neutron")
    color = color_singlet()
    color_residual = max(
        float(np.linalg.norm(tensor_sum(t) @ color)) for t in color_generators()
    )
    color_exchange = max(
        float(np.linalg.norm(color.reshape(3, 3, 3).swapaxes(i, j).ravel() + color))
        for i, j in ((0, 1), (0, 2), (1, 2))
    )
    product_color = np.zeros(27)
    product_color[np.ravel_multi_index((0, 1, 2), (3, 3, 3))] = 1.0
    product_residual = max(
        float(np.linalg.norm(tensor_sum(t) @ product_color)) for t in color_generators()
    )
    ratio = (
        neutron["moment_in_common_constituent_magneton"]
        / proton["moment_in_common_constituent_magneton"]
    )
    checks = {
        "color_singlet_annihilated_by_all_generators": color_residual < TOLERANCE,
        "color_is_antisymmetric": color_exchange < TOLERANCE,
        "rgb_product_is_not_a_singlet": product_residual > 0.1,
        "proton_charge": abs(proton["charge_over_e"] - 1) < TOLERANCE,
        "neutron_charge": abs(neutron["charge_over_e"]) < TOLERANCE,
        "two_spin_sectors": all(
            np.allclose(
                data["spin_squared_candidates_hbar2"],
                [0.75, 3.75],
                atol=TOLERANCE,
                rtol=0,
            )
            for data in (proton, neutron)
        ),
        "spin_half_and_exchange": all(
            data["spin_half_eigenstate_residual"] < TOLERANCE
            and data["spin_flavor_exchange_residual"] < TOLERANCE
            for data in (proton, neutron)
        ),
        "known_equal_constituent_mass_moment_ratio": abs(ratio + 2 / 3) < TOLERANCE,
    }
    return {
        "schema": "emergenz-knoten.nucleon-reference.v1",
        "claim_class": "assumed_quantum_reference_only",
        "decision": "reference-algebra-pass"
        if all(checks.values())
        else "reference-algebra-fail",
        "inputs": [
            "three_valence_quarks",
            "u_d_flavor_and_fractional_charges",
            "spin_half_quarks_and_quantum_tensor_product",
            "fundamental_SU3_color_and_antisymmetric_singlet",
            "symmetric_spatial_S_wave_and_spin_flavor_ansatz",
            "spin_half_sector_selection_not_energy_selection",
            "equal_constituent_u_d_masses_for_moment_ratio",
            "additive_Dirac_quark_moments",
        ],
        "not_computed": [
            "spatial_binding_or_confinement",
            "proton_or_neutron_mass_or_radius",
            "gluon_and_sea_quark_dynamics",
            "beta_decay_or_weak_interaction",
            "electron_field_or_hydrogen_spectrum",
            "FIFO_or_Memory_emergence",
        ],
        "proton": proton,
        "neutron": neutron,
        "color": {
            "dimension": 27,
            "generator_residual": color_residual,
            "exchange_residual": color_exchange,
            "rgb_product_control_residual": product_residual,
        },
        "moment_ratio": {
            "prediction": ratio,
            "pdg_2025_comparison": MEASURED_MOMENT_RATIO,
            "relative_absolute_discrepancy": abs(ratio / MEASURED_MOMENT_RATIO - 1),
            "used_for_fit": False,
            "experimental_agreement_claimed": False,
        },
        "checks": checks,
        "source": PDG_QUARK_MODEL,
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run_reference()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, indent=2, allow_nan=False)
        stream.write("\n")
    print(
        json.dumps(
            {"decision": result["decision"], "moment_ratio": result["moment_ratio"]}
        )
    )
    if not all(result["checks"].values()):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
