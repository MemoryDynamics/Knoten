"""Synthetic operator checks, not a spatial nucleon simulation."""

from fractions import Fraction
from itertools import permutations

import numpy as np
import pytest

from experiments.current.reference.nucleon_spatial_preflight import (
    C_GEV4,
    MASS_GEV,
    PAIRS,
    al1_local_terms,
    factorization_residual,
    local_matrix,
    run_preflight,
    spin_pair_operators,
)
from experiments.current.reference.nucleon_spin_flavor_reference import (
    color_generators,
    color_singlet,
    pauli_matrices,
    spin_flavor_states,
    tensor_sum,
)


TRIANGLE = np.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.25, 1.25, 0.0]])


def test_color_pair_factor_is_half_in_baryon_not_one_as_in_meson():
    for i, j in PAIRS:
        pair = np.zeros((27, 27), dtype=complex)
        for generator in color_generators():
            factors = [np.eye(3) for _ in range(3)]
            factors[i] = factors[j] = 2 * generator
            pair += np.kron(np.kron(factors[0], factors[1]), factors[2])
        np.testing.assert_allclose(
            -3 / 16 * pair @ color_singlet(), 0.5 * color_singlet(), atol=1e-14
        )


def test_pair_operators_have_pauli_not_spin_half_normalization():
    for operator in spin_pair_operators():
        np.testing.assert_allclose(
            operator @ operator, 3 * np.eye(64) - 2 * operator, atol=1e-14
        )
        np.testing.assert_allclose(operator, operator.conj().T, atol=1e-14)
    spin = [tensor_sum(np.kron(np.eye(2), sigma / 2)) for sigma in pauli_matrices()]
    np.testing.assert_allclose(
        sum(spin_pair_operators()), 2 * sum(s @ s for s in spin) - 4.5 * np.eye(64)
    )


@pytest.mark.parametrize("species", ["proton", "neutron"])
@pytest.mark.parametrize("coefficients", [[1, 1, 1], [1, 2, 3], [-1, 0, 2]])
def test_factorization_residual_matches_analytic_variance(species, coefficients):
    result = factorization_residual(coefficients, species)
    assert result["spin_half_residual_squared"] == pytest.approx(
        result["analytic_residual_squared"], abs=1e-13
    )
    assert result["spin_three_half_control_squared"] < 1e-26
    if coefficients == [1, 2, 3]:
        assert result["spin_half_residual_squared"] == pytest.approx(12)


def test_spin_flavor_second_moments_underlying_leakage_formula():
    _, state, _ = spin_flavor_states("proton")
    pairs = spin_pair_operators()
    for i, a in enumerate(pairs):
        assert np.vdot(state, a @ state) == pytest.approx(-1)
        for j, b in enumerate(pairs):
            assert np.vdot(state, (a @ b + b @ a) @ state / 2) == pytest.approx(
                5 if i == j else -1
            )


def test_equilateral_geometry_is_special_not_generic():
    equilateral = np.array([[0, 0, 0], [1, 0, 0], [0.5, np.sqrt(3) / 2, 0]])
    _, equal = al1_local_terms(equilateral)
    _, unequal = al1_local_terms(TRIANGLE)
    assert factorization_residual(equal, "proton")["spin_half_residual_squared"] < 1e-26
    assert (
        factorization_residual(unequal, "proton")["spin_half_residual_squared"] > 1e-8
    )


def test_local_operator_preserves_spin_isospin_and_charge_sectors():
    potential = local_matrix(TRIANGLE)
    np.testing.assert_allclose(potential, potential.conj().T, atol=1e-14)
    spin = [tensor_sum(np.kron(np.eye(2), s / 2)) for s in pauli_matrices()]
    isospin = [tensor_sum(np.kron(s / 2, np.eye(2))) for s in pauli_matrices()]
    for operator in [
        sum(s @ s for s in spin),
        sum(t @ t for t in isospin),
        spin[2],
        isospin[2],
    ]:
        np.testing.assert_allclose(
            potential @ operator, operator @ potential, atol=1e-14
        )


def test_local_operator_is_translation_rotation_and_permutation_covariant():
    potential = local_matrix(TRIANGLE)
    rotation = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]])
    np.testing.assert_allclose(
        local_matrix(TRIANGLE @ rotation.T + [3, -2, 1]), potential, atol=1e-14
    )
    for permutation in permutations(range(3)):
        axes = permutation + tuple(i + 3 for i in permutation)
        permuted = potential.reshape((4,) * 6).transpose(axes).reshape(64, 64)
        np.testing.assert_allclose(
            local_matrix(TRIANGLE[list(permutation)]), permuted, atol=1e-14
        )


def test_constant_term_changes_energy_not_shape_or_gaps():
    potential = local_matrix(TRIANGLE)
    offset = -C_GEV4 / MASS_GEV**3
    exact_mev = 1000 * Fraction(101, 50000) / Fraction(63, 200) ** 3
    assert -1000 * offset == pytest.approx(float(exact_mev), rel=1e-14)
    values, vectors = np.linalg.eigh(potential)
    without = potential - offset * np.eye(64)
    np.testing.assert_allclose(
        without @ vectors, vectors * (values - offset), atol=1e-14
    )
    np.testing.assert_allclose(
        np.diff(np.linalg.eigvalsh(without)), np.diff(values), atol=1e-14
    )


@pytest.mark.parametrize(
    "bad", [np.zeros((3, 3)), np.zeros((2, 3)), np.full((3, 3), np.nan)]
)
def test_invalid_geometries_rejected_without_cutoff_substitution(bad):
    with pytest.raises(ValueError):
        al1_local_terms(bad)


def test_preflight_does_not_report_a_solved_spatial_state():
    report = run_preflight()
    assert all(report["checks"].values())
    assert report["decision"] == "coupled_spatial_spin_channels_required"
    assert report["claim_class"] == "assumed_reference_operator_audit_only"
    assert "spatial_wavefunction_or_mass_eigenvalue" in report["not_computed"]
