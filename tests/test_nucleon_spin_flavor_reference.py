"""Reference quantum algebra; no inference about the native Memory model."""

from __future__ import annotations

from itertools import permutations
import json

import numpy as np
import pytest
from scipy.linalg import expm

from experiments.current.reference.nucleon_spin_flavor_reference import (
    color_generators,
    color_singlet,
    nucleon_observables,
    pauli_matrices,
    run_reference,
    spin_flavor_states,
    tensor_sum,
)


@pytest.mark.parametrize("species,charge,n_up", [("proton", 1, 2), ("neutron", 0, 1)])
def test_quantum_numbers_in_selected_sector(species, charge, n_up):
    data = nucleon_observables(species)
    assert data["norm_squared"] == pytest.approx(1)
    assert data["up_count"] == pytest.approx(n_up)
    assert data["charge_over_e"] == pytest.approx(charge, abs=1e-14)
    assert data["spin_squared_hbar2"] == pytest.approx(0.75)
    assert data["spin_z_hbar"] == pytest.approx(0.5)
    assert data["isospin_squared"] == pytest.approx(0.75)
    np.testing.assert_allclose(
        data["spin_squared_candidates_hbar2"], [0.75, 3.75], atol=1e-14
    )
    assert data["spin_three_half_control_residual"] < 1e-14


@pytest.mark.parametrize(
    "species,up,down", [("proton", 4 / 3, -1 / 3), ("neutron", -1 / 3, 4 / 3)]
)
def test_magnetic_weights_are_expectations_not_assigned_outputs(species, up, down):
    data = nucleon_observables(species)
    assert data["up_spin_weight"] == pytest.approx(up)
    assert data["down_spin_weight"] == pytest.approx(down)
    assert data["up_spin_weight"] + data["down_spin_weight"] == pytest.approx(1)


def test_color_generators_are_orthonormal_traceless_and_annihilate_singlet():
    generators = color_generators()
    color = color_singlet()
    assert np.vdot(color, color) == pytest.approx(1)
    for i, a in enumerate(generators):
        np.testing.assert_allclose(a, a.conj().T, atol=1e-15)
        assert np.trace(a) == pytest.approx(0, abs=1e-15)
        np.testing.assert_allclose(tensor_sum(a) @ color, 0, atol=1e-15)
        for j, b in enumerate(generators):
            assert np.trace(a @ b) == pytest.approx(0.5 if i == j else 0, abs=1e-15)


def test_color_singlet_invariant_under_fixed_nontrivial_SU3_rotation():
    generators = color_generators()
    rotation = expm(1j * (0.3 * generators[0] - 0.7 * generators[3] + generators[7]))
    assert np.linalg.det(rotation) == pytest.approx(1)
    action = np.kron(np.kron(rotation, rotation), rotation)
    np.testing.assert_allclose(action @ color_singlet(), color_singlet(), atol=1e-14)


@pytest.mark.parametrize("species", ["proton", "neutron"])
def test_full_color_spin_flavor_state_has_fermionic_exchange_sign(species):
    _, state, _ = spin_flavor_states(species)
    state = state.reshape(4, 4, 4)
    color = color_singlet().reshape(3, 3, 3)
    for permutation in permutations(range(3)):
        parity = (-1) ** sum(
            permutation[i] > permutation[j] for i in range(3) for j in range(i + 1, 3)
        )
        np.testing.assert_allclose(state.transpose(permutation), state, atol=1e-14)
        np.testing.assert_allclose(
            color.transpose(permutation), parity * color, atol=1e-14
        )


@pytest.mark.parametrize("species", ["proton", "neutron"])
def test_quantum_rotation_sign_is_present_only_after_spin_representation_input(species):
    _, state, _ = spin_flavor_states(species)
    spin_x = tensor_sum(np.kron(np.eye(2), pauli_matrices()[0] / 2))
    np.testing.assert_allclose(expm(-2j * np.pi * spin_x) @ state, -state, atol=1e-14)
    np.testing.assert_allclose(expm(-4j * np.pi * spin_x) @ state, state, atol=1e-14)


def test_reference_pass_is_not_experimental_agreement_or_emergence():
    result = run_reference()
    assert result["decision"] == "reference-algebra-pass"
    assert all(result["checks"].values())
    assert result["claim_class"] == "assumed_quantum_reference_only"
    assert result["color"]["rgb_product_control_residual"] > 0.1
    assert result["moment_ratio"]["prediction"] == pytest.approx(-2 / 3)
    assert 0.026 < result["moment_ratio"]["relative_absolute_discrepancy"] < 0.028
    assert result["moment_ratio"]["used_for_fit"] is False
    assert result["moment_ratio"]["experimental_agreement_claimed"] is False
    assert "spin_half_sector_selection_not_energy_selection" in result["inputs"]
    assert "FIFO_or_Memory_emergence" in result["not_computed"]
    assert "spatial_binding_or_confinement" in result["not_computed"]
    json.dumps(result, allow_nan=False)


def test_unsupported_species_rejected():
    with pytest.raises(ValueError, match="species"):
        spin_flavor_states("electron")
