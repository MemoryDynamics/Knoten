"""Exact-rational and interval controls; no archived candidate evaluations."""

from decimal import Decimal, localcontext
from fractions import Fraction
import json

from mpmath import iv
import numpy as np
import pytest

from emergenz_knoten.fifo_normal_stability import (
    interval_schur_test,
    normal_translation_slope,
    rotation_symmetry_division,
)


F = Fraction
COSINE = F(1, 2)
SYMMETRY = [F(1), F(-2), F(2), F(-1)]
POLYNOMIALS = [
    [F(1)],
    [F(1), F(0)],
    [F(1), F(-1, 2)],
    [F(1), F(-3, 4), F(1, 8)],
    [F(1), F(0), F(9, 16)],
    [F(1), F(-3, 2), F(9, 16)],
    [F(1), F(-5, 4)],
    [F(1), F(-1)],
    [F(1), F(1)],
    [F(1), F(0), F(1)],
    [F(1), F(-5, 2), F(1)],
    # (z-r)(z+1/2)(z^2+1/4), with r=3/4 and r=5/4.
    [F(1), F(-1, 4), F(-1, 8), F(-1, 16), F(-3, 32)],
    [F(1), F(-3, 4), F(-3, 8), F(-3, 16), F(-5, 32)],
]


def _decimal(value):
    with localcontext() as context:
        context.prec = 120
        result = str(Decimal(value.numerator) / Decimal(value.denominator))
    assert F(result) == value  # These inputs all have terminating decimal forms.
    return result


def _box(polynomial):
    return [(_decimal(value), _decimal(value)) for value in polynomial]


def _exact_schur(polynomial):
    current = list(polynomial)
    reflections = []
    while len(current) > 1:
        leading, trailing = current[0], current[-1]
        reflections.append(trailing / leading)
        if abs(trailing) >= abs(leading):
            return False, reflections
        # Unnormalized exact recursion, independent of the interval normalization.
        current = [
            leading * current[index] - trailing * current[-1 - index]
            for index in range(len(current) - 1)
        ]
    return True, reflections


def _binary_fraction(raw):
    sign, mantissa, exponent, _ = raw
    return (-1) ** sign * F(mantissa) * F(2) ** exponent


@pytest.mark.parametrize("quotient", POLYNOMIALS)
def test_translation_slope_matches_exact_derivative_and_shape_quotient(quotient):
    full = list(np.convolve(SYMMETRY, quotient))
    couplings = [-coefficient for coefficient in full[2:]]
    degree = len(full) - 1
    derivative = sum((degree - index) * value for index, value in enumerate(full))
    slope = normal_translation_slope(couplings)
    assert sum(full) == 0
    assert full[1] == sum(couplings) - 1
    assert slope == derivative == 2 * (1 - COSINE) * sum(quotient)


def test_negative_slope_has_known_real_unstable_mode_and_positive_upper_endpoint():
    root = F(5, 4)
    full = list(np.convolve(SYMMETRY, [F(1), -root]))
    couplings = [-coefficient for coefficient in full[2:]]
    assert normal_translation_slope(couplings) < 0
    upper = 1 + sum(abs(value) for value in couplings)
    assert 1 < root < upper
    scalar = (
        upper - 1 + sum(c * (1 - upper ** (-j)) for j, c in enumerate(couplings, 1))
    )
    assert scalar > 0


@pytest.mark.parametrize(
    "quotient",
    [
        [F(1), F(5, 4)],  # Negative unstable root.
        [F(1), F(0), F(25, 16)],  # Complex unstable conjugate pair.
        [F(1), F(-11, 4), F(15, 8)],  # Two positive unstable roots: 5/4 and 3/2.
    ],
)
def test_positive_slope_is_not_a_stability_certificate(quotient):
    full = list(np.convolve(SYMMETRY, quotient))
    assert normal_translation_slope([-value for value in full[2:]]) > 0
    assert _exact_schur(quotient)[0] is False


@pytest.mark.parametrize(
    "bounds,strict_negative", [(("-2", "-1.9"), True), (("-1.1", "-0.9"), False)]
)
def test_interval_slope_preserves_uncertainty(bounds, strict_negative):
    previous = iv.dps
    iv.dps = 60
    try:
        value = normal_translation_slope([iv.mpf(list(bounds))])
        assert _binary_fraction(value._mpi_[0]) <= 1 + F(bounds[0])
        assert _binary_fraction(value._mpi_[1]) >= 1 + F(bounds[1])
        assert (_binary_fraction(value._mpi_[1]) < 0) is strict_negative
    finally:
        iv.dps = previous


def test_translation_slope_rejects_missing_lags():
    with pytest.raises(ValueError, match="lag coupling"):
        normal_translation_slope([])


@pytest.mark.parametrize("precision", [50, 90])
@pytest.mark.parametrize("polynomial", POLYNOMIALS)
def test_interval_schur_agrees_with_exact_rational_recursion(polynomial, precision):
    stable, expected = _exact_schur(polynomial)
    result = interval_schur_test(_box(polynomial), precision_dps=precision)
    assert result["decision"] == ("strictly-schur" if stable else "not-strictly-schur")
    assert len(result["reflections"]) == len(expected)
    for record, value in zip(result["reflections"], expected, strict=True):
        interval = record["coefficient"]
        assert _binary_fraction(interval["lower_binary"]) <= value
        assert value <= _binary_fraction(interval["upper_binary"])
    assert (
        json.loads(json.dumps(result, allow_nan=False))["decision"]
        == result["decision"]
    )


@pytest.mark.parametrize("quotient", POLYNOMIALS)
def test_exact_symmetry_division_preserves_every_additional_mode(quotient):
    full = list(np.convolve(SYMMETRY, quotient))
    recovered, remainder = rotation_symmetry_division(full, COSINE)
    assert recovered == quotient
    assert remainder == [0, 0, 0]


@pytest.mark.parametrize("root", [F(1), F(1025, 1024), F(1023, 1024)])
def test_additional_near_neutral_mode_is_not_deleted_as_a_symmetry(root):
    full = list(np.convolve(SYMMETRY, [F(1), -root]))
    quotient, remainder = rotation_symmetry_division(full, COSINE)
    assert remainder == [0, 0, 0]
    assert quotient == [1, -root]
    result = interval_schur_test(_box(quotient), precision_dps=50)
    expected = "strictly-schur" if root < 1 else "not-strictly-schur"
    assert result["decision"] == expected


def test_nonzero_division_remainder_is_preserved():
    full = list(np.convolve(SYMMETRY, [F(1), F(-1, 2)]))
    full[-1] += F(1, 1024)
    quotient, remainder = rotation_symmetry_division(full, COSINE)
    assert quotient == [1, F(-1, 2)]
    assert remainder == [0, 0, F(1, 1024)]


def test_interval_division_encloses_exact_quotients_and_remainders():
    center = list(np.convolve(SYMMETRY, [F(1), F(-3, 4), F(1, 8)]))
    width = F(1, 1024)
    previous_precision = iv.dps
    iv.dps = 60
    try:
        coefficients = [iv.mpf(1)] + [
            iv.mpf([_decimal(value - width), _decimal(value + width)])
            for value in center[1:]
        ]
        cosine = iv.mpf([_decimal(COSINE - width), _decimal(COSINE + width)])
        quotient, remainder = rotation_symmetry_division(coefficients, cosine)
        for sign in (-1, 0, 1):
            sample = [F(1)] + [
                value + (-1) ** index * sign * width
                for index, value in enumerate(center[1:])
            ]
            exact_q, exact_r = rotation_symmetry_division(sample, COSINE + sign * width)
            for interval, exact in zip(
                quotient + remainder, exact_q + exact_r, strict=True
            ):
                assert _binary_fraction(interval._mpi_[0]) <= exact
                assert exact <= _binary_fraction(interval._mpi_[1])
    finally:
        iv.dps = previous_precision


@pytest.mark.parametrize("polynomial", [[], [1, 0, 0], [2, 0, 0, 0]])
def test_symmetry_division_rejects_wrong_degree_or_leading_coefficient(polynomial):
    with pytest.raises(ValueError, match="monic polynomial"):
        rotation_symmetry_division(polynomial, COSINE)


@pytest.mark.parametrize("quotient", [[F(1), F(-3, 4), F(1, 8)], [F(1), F(-5, 4)]])
def test_symmetry_quotient_matches_orthogonal_matrix_reduction(quotient):
    full = np.asarray(np.convolve(SYMMETRY, quotient), dtype=float)
    size = len(full) - 1
    companion = np.zeros((size, size))
    companion[0] = -full[1:]
    companion[1:, :-1] = np.eye(size - 1)
    angle = np.arccos(float(COSINE))
    ages = np.arange(size)
    symmetry = np.column_stack(
        (np.ones(size), np.cos(ages * angle), np.sin(ages * angle))
    )
    basis, _ = np.linalg.qr(symmetry, mode="complete")
    reduced = basis.T @ companion @ basis
    np.testing.assert_allclose(reduced[3:, :3], 0.0, atol=2e-15)
    np.testing.assert_allclose(
        np.sort_complex(np.linalg.eigvals(reduced[3:, 3:])),
        np.sort_complex(np.roots(np.asarray(quotient, dtype=float))),
        atol=3e-14,
    )


def test_strict_spectral_stability_does_not_require_one_step_norm_contraction():
    polynomial = [F(1), F(-1), F(1, 4)]
    result = interval_schur_test(_box(polynomial), precision_dps=50)
    assert result["decision"] == "strictly-schur"
    companion = np.asarray([[1.0, -0.25], [1.0, 0.0]])
    assert np.linalg.norm(companion, 2) > 1.4
    assert np.linalg.norm(np.linalg.matrix_power(companion, 50), 2) < 1e-10


def test_equality_case_is_not_automatically_marginal():
    polynomial = [F(1), F(-5, 2), F(1)]  # Roots 2 and 1/2, not unit roots.
    result = interval_schur_test(_box(polynomial), precision_dps=50)
    assert result["decision"] == "not-strictly-schur"
    assert len(result["reflections"]) == 1
    np.testing.assert_allclose(np.sort(np.roots(polynomial)), [0.5, 2.0])


@pytest.mark.parametrize(
    "tail,decision",
    [
        (("-0.75", "-0.5"), "strictly-schur"),
        (("-1.1", "-1.01"), "not-strictly-schur"),
        (("-1.01", "-0.99"), "inconclusive"),
    ],
)
def test_interval_uncertainty_is_not_relabelled_as_physics(tail, decision):
    result = interval_schur_test([("1", "1"), tail], precision_dps=50)
    assert result["decision"] == decision


def test_near_boundary_rounding_requires_resolution_and_restores_context():
    tail = "-0." + "9" * 80
    original_precision = iv.dps
    coarse = interval_schur_test([("1", "1"), (tail, tail)], precision_dps=50)
    fine = interval_schur_test([("1", "1"), (tail, tail)], precision_dps=100)
    assert coarse["decision"] == "inconclusive"
    assert fine["decision"] == "strictly-schur"
    assert iv.dps == original_precision


@pytest.mark.parametrize(
    "coefficients",
    [
        [],
        [("0", "0")],
        [("0.99", "1")],
        [("1", "1"), ("nan", "nan")],
        [("1", "1"), ("-inf", "1")],
        [
            ("1", "1"),
            ("0.1", "0.09999999999999999999999999999999999999999999999999999999"),
        ],
        [("1", "1"), ("not-a-decimal", "0")],
    ],
)
def test_invalid_coefficient_boxes_are_rejected(coefficients):
    with pytest.raises(ValueError):
        interval_schur_test(coefficients, precision_dps=50)


@pytest.mark.parametrize("precision", [True, 49, 60.5])
def test_invalid_precision_is_rejected(precision):
    with pytest.raises(ValueError, match="precision_dps"):
        interval_schur_test([("1", "1")], precision_dps=precision)


def test_numeric_instead_of_decimal_endpoints_are_rejected():
    with pytest.raises(TypeError, match="decimal strings"):
        interval_schur_test([(1, 1)], precision_dps=50)
