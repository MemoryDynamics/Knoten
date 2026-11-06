"""Conditional state envelopes and exact-rational checks of scalar reduction."""

from fractions import Fraction

import mpmath as mp
import numpy as np
import pytest

from paired_error_propagation import (
    audit_accumulation_contract,
    bounded_pairwise_mean,
    constant_defect_envelope,
    paired_block_input_error,
    propagate_split_error,
    uniform_split_envelope,
)
from paired_residual_precision import split_step


@pytest.mark.parametrize("count", [1, 3, 11])
@pytest.mark.parametrize("gain", [0.0, 0.1, 0.4])
def test_constant_envelope_matches_independent_matrix_resolvent(count, gain):
    weights = 0.4 * 0.6 ** np.arange(1, count + 1)
    defects = (np.arange(count) + 1) * 1e-8
    matrix = gain * np.outer(np.ones(count), weights)
    matrix[1:, :-1] += np.eye(count - 1)
    expected = np.linalg.solve(np.eye(count) - matrix, defects)
    result = constant_defect_envelope(weights, gain, defects)
    np.testing.assert_allclose(result, expected, rtol=5e-14, atol=1e-22)
    error = np.zeros(count)
    for _ in range(250):
        error = matrix @ error + defects
        assert np.all(error <= result * (1 + 1e-13))


def test_uniform_split_bound_is_invariant_and_includes_linear_cross_error():
    count = 8
    dw, dr = np.full(count, 1e-9), np.full(count, 2e-9)
    caps = np.sqrt(np.arange(1, count + 1))
    args = (0.3, 0.02, (1, 35, 1, 3))
    ew, er = uniform_split_envelope(dw, dr, caps, *args)
    nw, nr = propagate_split_error(ew, er, caps, dw, dr, *args)
    np.testing.assert_allclose(nw, ew, rtol=5e-14)
    np.testing.assert_allclose(nr, er, rtol=5e-14)
    gamma = 0.3 * 0.7 ** np.arange(1, count + 1)
    uncoupled = constant_defect_envelope(gamma, 0.02 * (1 + 35 / 9), dr)
    assert np.all(er > uncoupled)
    zero_w, no_cross = uniform_split_envelope(np.zeros(count), dr, caps, *args)
    np.testing.assert_array_equal(zero_w, np.zeros(count))
    np.testing.assert_allclose(no_cross, uncoupled)


def _mp_direct_split(w, r, xi, alpha, eta, epsilon, kernel):
    with mp.workdps(100):
        w, r = [[list(map(mp.mpf, row)) for row in a] for a in (w, r)]
        alpha, eta, eps = map(mp.mpf, (alpha, eta, epsilon))
        ar, aa, sr, sa = map(mp.mpf, kernel)
        kappa = aa / sa**2 - ar / sr**2
        gamma = [alpha * (1 - alpha) ** j for j in range(1, len(w) + 1)]
        dimension = len(w[0])
        wi = [
            mp.mpf(xi[c])
            - eta * kappa * mp.fsum(gamma[j] * w[j][c] for j in range(len(w)))
            for c in range(dimension)
        ]
        force = [mp.mpf(0)] * dimension
        for j in range(len(w)):
            lag = [eps * w[j][c] + eps**3 * r[j][c] for c in range(dimension)]
            radius = mp.fsum(v * v for v in lag)
            factor = aa / sa**2 * mp.exp(-radius / (2 * sa**2)) - ar / sr**2 * mp.exp(
                -radius / (2 * sr**2)
            )
            for c in range(dimension):
                force[c] += gamma[j] * factor * lag[c]
        ri = [
            (eps * mp.mpf(xi[c]) - eta * force[c] - eps * wi[c]) / eps**3
            for c in range(dimension)
        ]
        nw, nr = [wi], [ri]
        for j in range(1, len(w)):
            nw.append([wi[c] + w[j - 1][c] for c in range(dimension)])
            nr.append([ri[c] + r[j - 1][c] for c in range(dimension)])
        return nw, nr


def _norm_differences(left, right):
    with mp.workdps(100):
        return np.nextafter(
            np.array(
                [
                    float(
                        mp.sqrt(
                            mp.fsum(
                                (mp.mpf(a) - mp.mpf(b)) ** 2
                                for a, b in zip(x, y, strict=True)
                            )
                        )
                    )
                    for x, y in zip(left, right, strict=True)
                ]
            ),
            np.inf,
        )


@pytest.mark.parametrize("epsilon", [1e-12, 0.007, 0.3])
@pytest.mark.parametrize("kernel", [(0, 26, 1, 3), (1, 35, 1, 3)])
def test_one_step_envelope_against_full_force_at_high_precision(epsilon, kernel):
    w = np.array([[0.5, -0.25], [0.125, 0.75], [-0.25, 0.5]])
    r = w / 8
    wt = w + np.array([[1, -2], [3, 1], [-1, 2]]) * 1e-5
    rt = r + np.array([[-2, 1], [1, 3], [2, -1]]) * 2e-5
    xi, alpha, eta = np.array([0.25, -0.5]), 0.3, 0.02
    exact_w, exact_r = _mp_direct_split(w, r, xi, alpha, eta, epsilon, kernel)
    local_w, local_r = _mp_direct_split(wt, rt, xi, alpha, eta, epsilon, kernel)
    computed_w, computed_r = split_step(wt, rt[None], xi, alpha, eta, epsilon, [kernel])
    # Prescribed defects exercise correlated errors in every lag coordinate.
    computed_w += np.array([1, -1])[None] * 1e-8
    computed_r[0] += np.array([-1, 2])[None] * 1e-8
    dw, dr = (
        _norm_differences(computed_w, local_w),
        _norm_differences(computed_r[0], local_r),
    )
    ew, er = _norm_differences(wt, w), _norm_differences(rt, r)
    norms = np.linalg.norm(wt + epsilon**2 * rt, axis=1)
    bw, br = propagate_split_error(ew, er, norms, dw, dr, alpha, eta, kernel)
    assert np.all(_norm_differences(computed_w, exact_w) <= bw * (1 + 1e-12))
    assert np.all(_norm_differences(computed_r[0], exact_r) <= br * (1 + 1e-12))


@pytest.mark.parametrize("epsilon", [0.0, 4.4e-6, 0.3])
@pytest.mark.parametrize("sign", [-1, 1])
def test_paired_block_input_bound_against_exact_polynomial(epsilon, sign):
    w = np.array([1.0, 2.0, -0.5])
    r = np.array([[0.25, 0.5, -0.75], [-0.5, 0.25, 0.125]])
    dw = sign * np.array([1, -2, 1]) / 1024
    dr = sign * np.array([[1, 2, -1], [-2, 1, 1]]) / 2048
    length = 7
    bound = paired_block_input_error(
        w, r, np.linalg.norm(dw), np.linalg.norm(dr, axis=1), epsilon, length
    )
    with mp.workdps(80):

        def exact(a, b):
            a = list(map(mp.mpf, a))
            b = [list(map(mp.mpf, row)) for row in b]
            linear = 2 * mp.fsum(a[c] * (b[1][c] - b[0][c]) for c in range(3))
            quadratic = mp.mpf(epsilon) ** 2 * mp.fsum(
                b[1][c] ** 2 - b[0][c] ** 2 for c in range(3)
            )
            return (linear + quadratic) / (6 * length)

        difference = abs(exact(w + dw, r + dr) - exact(w, r))
        assert difference <= bound
    assert paired_block_input_error(w, r, 0, [0, 0], epsilon, length) == 0


@pytest.mark.parametrize("count", [1, 2, 3, 7, 31, 1001])
def test_pairwise_bounds_enclose_exact_rational_sum_and_mean(count):
    pattern = np.array([1e16, 1.0, -1e16, 2.0, -0.5, 1e-200, -1e-200])
    values = np.resize(pattern, count)
    result = bounded_pairwise_mean(values)
    exact = sum((Fraction.from_float(float(x)) for x in values), Fraction())
    assert abs(Fraction.from_float(result["sum"]) - exact) <= Fraction.from_float(
        result["sum_error_bound"]
    )
    assert abs(
        Fraction.from_float(result["mean"]) - exact / count
    ) <= Fraction.from_float(result["mean_error_bound"])
    exact_absolute = sum(
        (abs(Fraction.from_float(float(x))) for x in values), Fraction()
    )
    assert exact_absolute <= Fraction.from_float(result["absolute_input_sum_upper"])
    assert result["depth"] == (count - 1).bit_length()
    exact_gamma = Fraction(result["depth"], 2**53 - result["depth"])
    assert exact_gamma <= Fraction.from_float(result["gamma_upper"])


@pytest.mark.parametrize(
    "values", [[0.0], [0.0] * 17, [1.0, -1.0], [1e-200, -1e-200], [1.0] * 1001]
)
def test_pairwise_zero_and_exact_dyadic_controls(values):
    result = bounded_pairwise_mean(values)
    exact = sum((Fraction.from_float(float(x)) for x in values), Fraction())
    assert abs(
        Fraction.from_float(result["mean"]) - exact / len(values)
    ) <= Fraction.from_float(result["mean_error_bound"])
    if all(x == 0 for x in values):
        assert result["mean_error_bound"] == 0


@pytest.mark.parametrize(
    "values",
    [
        [],
        [np.nan],
        [np.inf],
        [np.nextafter(0.0, 1.0)],
        [np.finfo(float).max, np.finfo(float).max],
        [np.finfo(float).max, -np.finfo(float).max],
        [np.finfo(float).tiny] * 2,
    ],
)
def test_reducer_fails_closed_outside_checked_arithmetic(values):
    with pytest.raises(ValueError):
        bounded_pairwise_mean(values)


@pytest.mark.parametrize(
    "gain,defects",
    [(2.0, [1, 1]), (-1.0, [1, 1]), (0.1, [-1, 1]), (0.1, [1]), (np.inf, [1, 1])],
)
def test_invalid_constant_envelopes_rejected(gain, defects):
    with pytest.raises(ValueError):
        constant_defect_envelope([0.3, 0.2], gain, defects)


def test_invalid_shapes_and_unknown_caps_are_not_silently_filled():
    with pytest.raises(ValueError):
        uniform_split_envelope(
            [1, 1], [1, 1], [np.inf, np.inf], 0.3, 0.02, (1, 35, 1, 3)
        )
    with pytest.raises(ValueError):
        propagate_split_error(
            [1, 1], [1], [1, 1], [1, 1], [1, 1], 0.3, 0.02, (1, 35, 1, 3)
        )


@pytest.mark.parametrize("epsilon", [1e-200, -1.0, np.inf, np.nan, 1e200])
def test_block_bound_rejects_unresolved_noise_square(epsilon):
    with pytest.raises(ValueError):
        paired_block_input_error([1.0], [[1.0], [2.0]], 0.1, [0.1, 0.1], epsilon, 1)


def test_fixed_contract_reports_conditional_gains_not_simulator_certification():
    result = audit_accumulation_contract()
    assert "not validated local defects" in result["scope"]
    assert result["linear_uniform_unit_defect_increment_gain"] < 1.42
    assert (
        result[
            "residual_uniform_unit_defect_increment_gain_excluding_linear_cross_error"
        ]
        < 2
    )
    reducer = result["synthetic_cancellation_reducer"]
    assert result["synthetic_actual_sum_error"] <= reducer["sum_error_bound"]
    assert result["synthetic_exact_sum"] == 500
    assert reducer["sum"] == 400
    assert result["synthetic_actual_sum_error"] == 100
    assert result["one_million_values_tree_depth"] == 20
    assert result["one_million_values_gamma_upper"] < 2.23e-15
