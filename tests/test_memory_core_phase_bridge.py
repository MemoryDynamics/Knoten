"""Constructed memory/field-reference checks; no target dynamics or fitted data."""

from fractions import Fraction
import math

import numpy as np
import pytest
from scipy.integrate import quad

from emergenz_knoten.state import FiniteMemoryState
from emergenz_knoten.vector_memory import oriented_history_from_state


def _state_from_deposits(deposits, w_zero, q):
    deposits = np.asarray(deposits, dtype=float)
    memory = np.zeros((len(deposits) + 1, deposits.shape[1]))
    memory[1:] = -np.cumsum(deposits, axis=0)
    return FiniteMemoryState(
        x=memory[0], memory=memory, weights=w_zero * q ** np.arange(len(memory))
    )


def _readout(state, omega):
    _, deposits, weights = oriented_history_from_state(state, mode="displacement")
    return (weights * np.exp(1j * omega * np.arange(len(deposits)))) @ deposits


@pytest.mark.parametrize("dim,length,q", [(2, 3, 0.5), (3, 6, 0.7), (7, 4, 0.9)])
def test_native_deposit_shift_matches_full_complex_boundary_balance(dim, length, q):
    deposits = np.sin(np.arange(length * dim).reshape(length, dim) + 0.3)
    w_zero, omega = 0.2, 0.7
    before = _state_from_deposits(deposits, w_zero, q)
    new_deposit = np.cos(np.arange(dim) + 0.1)
    after = FiniteMemoryState(
        x=before.x + new_deposit,
        memory=np.vstack([before.x + new_deposit, before.memory[:-1]]),
        weights=before.weights,
    )
    tail = w_zero * q**length * np.exp(1j * length * omega) * deposits[-1]
    predicted = (
        q * np.exp(1j * omega) * _readout(before, omega) + w_zero * new_deposit - tail
    )
    np.testing.assert_allclose(
        _readout(after, omega), predicted, rtol=1e-13, atol=2e-15
    )
    assert (
        np.linalg.norm(tail)
        <= w_zero * q**length * np.linalg.norm(deposits, axis=1).max()
    )


def test_equal_readout_and_new_input_do_not_close_finite_filter_exactly():
    # At omega=pi/2 use exact real/imaginary weights, not rounded exponentials.
    q = Fraction(1, 2)
    delta = (q**2, Fraction(0), Fraction(1))
    real_before, imag_before = delta[0] - q**2 * delta[2], q * delta[1]
    assert real_before == imag_before == 0
    shifted = (Fraction(0), delta[0], delta[1])
    real_after, imag_after = shifted[0] - q**2 * shifted[2], q * shifted[1]
    assert real_after == 0
    assert imag_after == Fraction(1, 8)


@pytest.mark.parametrize("dim", [2, 3, 7, 12])
def test_nonzero_complex_loop_contraction_lifts_to_native_real_histories(dim):
    q, w_zero, omega = 0.7, 0.3, 0.9
    angles = np.linspace(0, 2 * math.pi, 17)
    for s in np.linspace(0, math.pi / 2, 7):
        loop = []
        for angle in angles:
            target = np.zeros(dim, dtype=complex)
            target[0] = math.cos(s) * np.exp(1j * angle)
            target[1] = math.sin(s)
            deposits = np.zeros((4, dim))
            deposits[1] = target.imag / (w_zero * q * math.sin(omega))
            deposits[0] = (target.real - target.imag / math.tan(omega)) / w_zero
            state = _state_from_deposits(deposits, w_zero, q)
            actual = _readout(state, omega)
            np.testing.assert_allclose(actual, target, atol=3e-15)
            assert np.linalg.norm(actual) == pytest.approx(1, abs=3e-15)
            loop.append(actual)
        np.testing.assert_allclose(loop[0], loop[-1], atol=3e-15)
    # The endpoint is a constant loop, despite unit winding of component 0 initially.
    np.testing.assert_allclose(
        loop, np.tile(np.eye(dim)[1], (len(angles), 1)), atol=3e-15
    )


@pytest.mark.parametrize("ratio", [0.1, 0.5, 0.9])
def test_phase_error_bound_includes_tangent_extremizer(ratio):
    base = 0.7 * np.exp(0.8j)
    phases = np.linspace(-math.pi, math.pi, 101)
    perturbations = abs(base) * ratio * np.exp(1j * phases)
    errors = np.abs(np.angle((base + perturbations) / base))
    assert np.max(errors) <= math.asin(ratio) + 3e-15
    relative_tangent = -(ratio**2) + 1j * ratio * math.sqrt(1 - ratio**2)
    assert abs(relative_tangent) == pytest.approx(ratio)
    assert np.angle(1 + relative_tangent) == pytest.approx(math.asin(ratio))


@pytest.mark.parametrize(
    "lambda_one,lambda_two,beta,v_one_sq,v_two_sq",
    [(4, 2, 2, 1, 1), (2, 3, 2, 2, 1), (3, 4, 3, 3, 2)],
)
def test_reference_vacuum_axis_comparison_and_mass_gap(
    lambda_one, lambda_two, beta, v_one_sq, v_two_sq
):
    determinant = Fraction(lambda_one * lambda_two, 4) - beta**2
    alternate_energy = Fraction(lambda_one * v_one_sq**2 - lambda_two * v_two_sq**2, 4)
    core_mass_sq = beta * v_one_sq - Fraction(lambda_two * v_two_sq, 2)
    assert determinant < 0
    assert alternate_energy > 0
    assert core_mass_sq > 0
    # Finite controls supplement, not prove, the analytic quadrant-minimum argument.
    for x in (0, Fraction(1, 3), v_one_sq, 2 * v_one_sq):
        for y in (0, Fraction(1, 2), v_two_sq, 2 * v_two_sq):
            potential = (
                Fraction(lambda_one, 4) * (x - v_one_sq) ** 2
                + Fraction(lambda_two, 4) * (y - v_two_sq) ** 2
                + beta * x * y
                - Fraction(lambda_two * v_two_sq**2, 4)
            )
            assert potential >= 0


def test_local_positive_core_mass_does_not_select_global_vacuum():
    lambda_one, lambda_two, beta = 1, 4, 3
    assert 4 * beta**2 > lambda_one * lambda_two
    assert beta - Fraction(lambda_two, 2) > 0
    alternate_energy = Fraction(lambda_one - lambda_two, 4)
    assert alternate_energy < 0


@pytest.mark.parametrize("width,trial_radius", [(0.3, 1.0), (2.0, 1.0), (1.0, 0.4)])
def test_reference_core_rayleigh_formula_against_independent_radial_quadrature(
    width, trial_radius
):
    mass_well, exterior_shift = 2.0, 3.0

    def radial_norm(r):
        return 2 * math.pi * r * math.exp(-((r / trial_radius) ** 2))

    norm = quad(radial_norm, 0, np.inf, epsabs=1e-11)[0]
    kinetic = quad(
        lambda r: radial_norm(r) * r**2 / trial_radius**4, 0, np.inf, epsabs=1e-11
    )[0]
    inside = quad(lambda r: -mass_well * radial_norm(r), 0, width, epsabs=1e-11)[0]
    outside = quad(
        lambda r: (exterior_shift - mass_well) * radial_norm(r),
        width,
        np.inf,
        epsabs=1e-11,
    )[0]
    direct = (kinetic + inside + outside) / norm
    formula = (
        1 / trial_radius**2
        + exterior_shift * math.exp(-((width / trial_radius) ** 2))
        - mass_well
    )
    assert direct == pytest.approx(formula, abs=2e-11)
    if width == 2:
        assert direct < 0
    else:
        assert direct > 0  # Inconclusive about the true lowest eigenvalue.


def test_global_amplitude_charge_and_mass_calibration_are_different_operations():
    # Fixed-shape classical source integral: Qcal=2*omega*integral(|psi|^2).
    omega, profile_norm = Fraction(2, 3), Fraction(5, 2)
    charge_number = 2 * omega * profile_norm
    assert charge_number == Fraction(10, 3)
    for scale in (Fraction(1, 7), Fraction(5), Fraction(1000)):
        scaled_charge = 2 * (scale * omega) * (scale**2 * profile_norm / scale**3)
        assert scaled_charge == charge_number
        assert (scale * Fraction(7)) * (Fraction(3) / scale) == 21
    # Shape-amplitude changes can change Q; no discreteness follows from a classical source.
    assert 2 * omega * (profile_norm / 4) == charge_number / 4
