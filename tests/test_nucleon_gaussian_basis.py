"""Target-free checks of the coupled spatial solver against analytic references."""

from itertools import permutations

import numpy as np
import pytest
from scipy.integrate import quad

from experiments.current.reference.nucleon_gaussian_basis import (
    Hamiltonian,
    JACOBI,
    PAIR_VECTORS,
    assemble,
    declared_al1,
    expectations,
    gaussian_integrals,
    internal_basis,
    positive_matrix,
    primitive_blocks,
    projected_blocks,
    proposed_exponents,
    ritz_ground,
    sector_data,
)
from experiments.current.reference.nucleon_spin_flavor_reference import (
    pauli_matrices,
    tensor_sum,
)
from experiments.current.reference.nucleon_spatial_preflight import al1_local_terms


A = np.array([[0.6, 0.13], [0.13, 0.9]])
B = np.array([[0.8, -0.11], [-0.11, 0.4]])


def test_jacobi_coordinates_remove_center_and_preserve_kinetic_metric():
    np.testing.assert_allclose(JACOBI @ JACOBI.T, np.eye(2), atol=1e-15)
    np.testing.assert_allclose(JACOBI @ np.ones(3), 0, atol=1e-15)
    positions = np.array([[1, 0, 2], [-1, 1, 0], [0, -1, -2]])
    x = JACOBI @ positions
    for w, (i, j) in zip(PAIR_VECTORS, ((0, 1), (0, 2), (1, 2)), strict=True):
        np.testing.assert_allclose(w @ x, positions[i] - positions[j], atol=1e-14)


@pytest.mark.parametrize(
    "sector,squared,size", [("nucleon", 0.75, 4), ("delta", 3.75, 1)]
)
def test_coupled_basis_has_required_spin_isospin_and_magnetic_sectors(
    sector, squared, size
):
    basis = internal_basis(sector)
    assert basis.shape == (64, size)
    np.testing.assert_allclose(basis.T @ basis, np.eye(size), atol=1e-14)
    for flavor_first in (True, False):
        operators = [
            tensor_sum(
                np.kron(s / 2, np.eye(2)) if flavor_first else np.kron(np.eye(2), s / 2)
            )
            for s in pauli_matrices()
        ]
        np.testing.assert_allclose(
            sum(s @ s for s in operators) @ basis, squared * basis, atol=1e-14
        )
        np.testing.assert_allclose(operators[2] @ basis, 0.5 * basis, atol=1e-14)


def test_overlap_and_kinetic_against_independent_two_dimensional_quadrature():
    nodes, weights = np.polynomial.hermite.hermgauss(48)
    x, y = np.meshgrid(nodes, nodes, indexing="ij")
    c = A + B
    integrand = np.exp(
        -(c[0, 0] - 1) * x * x - 2 * c[0, 1] * x * y - (c[1, 1] - 1) * y * y
    )
    weighted = integrand * np.outer(weights, weights)
    z = np.sum(weighted)
    normalization = (np.linalg.det(2 * A) * np.linalg.det(2 * B) / np.pi**4) ** 0.75
    overlap = normalization * z**3
    ket_laplacian = (
        3 * np.trace(B)
        - 6
        * np.sum(
            weighted
            * ((B[0, 0] * x + B[0, 1] * y) ** 2 + (B[1, 0] * x + B[1, 1] * y) ** 2)
        )
        / z
    )
    actual = gaussian_integrals(A, B)
    assert actual["overlap"] == pytest.approx(overlap, rel=1e-12)
    assert actual["kinetic_times_mass"] == pytest.approx(ket_laplacian, rel=1e-12)
    assert gaussian_integrals(A, A)["overlap"] == pytest.approx(1, abs=1e-14)


def test_pair_potential_integrals_against_radial_quadrature():
    actual = gaussian_integrals(A, B)
    for u, inverse, distance in zip(
        actual["pair_u"], actual["inverse_distance"], actual["distance"], strict=True
    ):

        def density(r):
            return 4 * np.pi * r * r * np.exp(-r * r / u) / (np.pi * u) ** 1.5

        assert quad(lambda r: density(r) / r, 0, np.inf)[0] == pytest.approx(
            inverse, rel=1e-12
        )
        assert quad(lambda r: density(r) * r, 0, np.inf)[0] == pytest.approx(
            distance, rel=1e-12
        )
        assert quad(lambda r: density(r) * np.exp(-((r / 0.7) ** 2)), 0, np.inf)[
            0
        ] == pytest.approx((1 + u / 0.7**2) ** -1.5, rel=1e-12)


def test_declared_al1_matches_existing_fixed_geometry_convention_without_solving_it():
    model = declared_al1()
    positions = np.array([[0, 0, 0], [1, 0, 0], [0.25, 1.25, 0]])
    distances = np.array(
        [
            np.linalg.norm(positions[i] - positions[j])
            for i, j in ((0, 1), (0, 2), (1, 2))
        ]
    )
    scalar, spin = al1_local_terms(positions)
    assert model.constant + np.sum(
        model.coulomb / distances + model.linear * distances
    ) == pytest.approx(scalar)
    np.testing.assert_allclose(
        model.spin_gaussian * np.exp(-((distances / model.spin_range) ** 2)),
        spin,
        rtol=1e-14,
    )


def test_permutation_projection_agrees_with_explicit_bra_and_ket_projection():
    data = sector_data("nucleon")
    model = Hamiltonian(
        mass=1.7,
        coulomb=-0.2,
        linear=0.3,
        spin_gaussian=0.17,
        spin_range=0.8,
        oscillator=0.4,
    )
    full = {}
    for da, ua in data["symmetries"]:
        for db, ub in data["symmetries"]:
            blocks = primitive_blocks(da.T @ A @ da, db.T @ B @ db, data, model, 0.2)
            for key, block in blocks.items():
                full[key] = full.get(key, np.zeros_like(block)) + ua.T @ block @ ub / 36
    actual = projected_blocks(A, B, data, model, 0.2)
    reverse = projected_blocks(B, A, data, model, 0.2)
    for key in actual:
        np.testing.assert_allclose(actual[key], full[key], atol=2e-14)
        np.testing.assert_allclose(actual[key], reverse[key].T, atol=2e-14)


def test_projected_wavefunction_is_pointwise_permutation_symmetric():
    data = sector_data("nucleon")
    x = np.array([[0.2, -0.3, 0.4], [0.5, 0.1, -0.2]])

    def wavefunction(x):
        return (
            sum(
                np.exp(-np.sum((d @ x) * (A @ d @ x))) * data["basis"] @ internal
                for d, internal in data["symmetries"]
            )
            / 6
        )

    value = wavefunction(x)
    for permutation in permutations(range(3)):
        d = JACOBI @ np.eye(3)[list(permutation)] @ JACOBI.T
        transformed = (
            wavefunction(d @ x)
            .reshape(4, 4, 4, 4)
            .transpose((*tuple(np.argsort(permutation)), 3))
            .reshape(64, 4)
        )
        np.testing.assert_allclose(transformed, value, atol=1e-14)


def test_generic_correlated_gaussian_keeps_four_channels_not_one():
    matrices = assemble([A], "nucleon", Hamiltonian(mass=1, oscillator=0.5))
    metric = np.linalg.eigvalsh(matrices["overlap"])
    assert np.sum(metric > 1e-12) == 4


@pytest.mark.parametrize("sector", ["nucleon", "delta"])
def test_exact_six_dimensional_oscillator_and_radii(sector):
    mass, omega = 1.3, 0.7
    exponent = mass * omega / 2 * np.eye(2)
    model = Hamiltonian(mass=mass, oscillator=mass * omega**2 / 2, constant=0.25)
    matrices = assemble([exponent, A, B], sector, model)
    result = ritz_ground(matrices["hamiltonian"], matrices["overlap"])
    observed = expectations(matrices, result["coefficients"])
    assert result["energy"] == pytest.approx(3 * omega + 0.25, abs=2e-11)
    assert result["metric_norm"] == pytest.approx(1, abs=1e-12)
    assert result["relative_matrix_residual"] < 1e-12
    assert observed["kinetic"] == pytest.approx(1.5 * omega, abs=1e-10)
    assert observed["matter_radius2"] == pytest.approx(1 / (mass * omega), abs=1e-10)
    assert observed["charge_p_radius2"] == pytest.approx(1 / (mass * omega), abs=1e-10)
    assert observed["charge_n_radius2"] == pytest.approx(0, abs=1e-10)
    assert observed["form_factor_p"] == pytest.approx(1, abs=1e-12)
    assert observed["form_factor_n"] == pytest.approx(0, abs=1e-12)
    if sector == "nucleon":
        assert observed["up_spin"] == pytest.approx(4 / 3, abs=1e-10)
        assert observed["down_spin"] == pytest.approx(-1 / 3, abs=1e-10)


def test_charge_radius_is_the_form_factor_slope_in_the_same_basis():
    model = Hamiltonian(mass=1, oscillator=0.5)
    exponents = [0.5 * np.eye(2), A]
    zero = assemble(exponents, "nucleon", model)
    q2 = 1e-5
    shifted = assemble(exponents, "nucleon", model, q_squared=q2)
    ground = ritz_ground(zero["hamiltonian"], zero["overlap"])
    obs0, obsq = (
        expectations(zero, ground["coefficients"]),
        expectations(shifted, ground["coefficients"]),
    )
    for species in ("p", "n"):
        slope = (
            -6 * (obsq[f"form_factor_{species}"] - obs0[f"form_factor_{species}"]) / q2
        )
        assert slope == pytest.approx(obs0[f"charge_{species}_radius2"], abs=1e-6)


def test_null_metric_directions_are_reported_not_regularized():
    h = np.diag([2.0, 6.0, 0.0])
    s = np.diag([1.0, 2.0, 0.0])
    result = ritz_ground(h, s)
    assert result["energy"] == pytest.approx(2)
    assert result["rank"] == 2
    assert result["raw_dimension"] == 3
    with pytest.raises(ValueError, match="positive semidefinite"):
        ritz_ground(h, np.diag([1, 2, -0.1]))
    with pytest.raises(ValueError, match="Hermitian"):
        ritz_ground([[1, 1], [0, 1]], np.eye(2))


def test_fixed_exponent_grids_are_nested_and_finite():
    previous = set()
    for level, size in enumerate((18, 50, 98)):
        exponents = proposed_exponents(level)
        assert len(exponents) == size
        current = {tuple(positive_matrix(a).ravel()) for a in exponents}
        assert previous <= current
        previous = current


@pytest.mark.parametrize(
    "bad", [np.zeros((2, 2)), [[1, 1], [0, 1]], np.full((2, 2), np.nan)]
)
def test_invalid_exponents_rejected(bad):
    with pytest.raises(ValueError):
        positive_matrix(bad)


def test_assembly_deadline_is_enforced_before_work():
    with pytest.raises(TimeoutError):
        assemble([A], "nucleon", Hamiltonian(mass=1), deadline=0)
