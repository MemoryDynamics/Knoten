"""Manufactured square controls, never archived FIFO candidate evaluations."""

from dataclasses import replace
from fractions import Fraction
import json

from mpmath import iv, mp
import numpy as np
import pytest

from emergenz_knoten.fifo_normal_stability import (
    _normal_characteristic_polynomial,
    certify_normal_fifo_box,
)
from emergenz_knoten.kernels import double_gaussian_gradient
from emergenz_knoten.rotating_wave_interval import IntervalRotatingWaveParameters
from emergenz_knoten.rotating_wave_stability import finite_memory_weights


def _square_inputs(decay):
    # Solve the two kernel values algebraically; no root or parameter search.
    with mp.workdps(130):
        q = mp.mpf(decay)
        first = -1 / ((1 - q) * q * (1 - q**2))
        second = 1 / ((1 - q) * q**2 * (1 - q**2))
        x, y = mp.exp(-1), mp.exp(-mp.mpf(1) / 4)
        rep = (second * y - first * y**2) / (x * y**2 - x**2 * y)
        att = 4 * (first + rep * x) / y
        parameters = IntervalRotatingWaveParameters(
            alpha=mp.nstr(1 - q, 110),
            horizon=4,
            memory_mass="1",
            eta="1",
            sigma_rep="1",
            sigma_att="2",
            amplitude_rep=mp.nstr(rep, 110),
            amplitude_att=mp.nstr(att, 110),
        )
        return {
            "radius": "1",
            "theta": mp.nstr(mp.pi / 2, 110),
            "radius_half_width": "1e-25",
            "theta_half_width": "1e-25",
            "parameters": parameters,
        }


def _fraction(raw):
    sign, mantissa, exponent, _ = raw
    return (-1) ** sign * Fraction(mantissa) * Fraction(2) ** exponent


def _assert_contains(record, exact):
    assert _fraction(record["lower_binary"]) <= exact
    assert exact <= _fraction(record["upper_binary"])


@pytest.mark.parametrize("precision", [60, 90])
@pytest.mark.parametrize(
    "decay,expected", [("0.5", "strictly-schur"), ("0.75", "not-strictly-schur")]
)
def test_manufactured_square_root_is_certified_before_normal_classification(
    decay, expected, precision
):
    original_precision = iv.dps
    result = certify_normal_fifo_box(**_square_inputs(decay), precision_dps=precision)
    assert result["root_certificate"]["pass"]
    assert result["decision"] == expected
    assert result["schur"]["degree"] == 1
    assert all(record["contains_zero"] for record in result["remainder"])
    q = Fraction(decay)
    eigenvalue = q**2 / (1 - q**2)
    for record, coefficient in zip(result["quotient"], (1, -eigenvalue), strict=True):
        _assert_contains(record, coefficient)
    _assert_contains(result["cosine"], 0)
    assert json.loads(json.dumps(result, allow_nan=False))["decision"] == expected
    assert iv.dps == original_precision


def test_nonroot_box_does_not_reach_symmetry_division_or_schur_test():
    inputs = _square_inputs("0.5") | {"radius": "1.3"}
    result = certify_normal_fifo_box(**inputs, precision_dps=60)
    assert not result["root_certificate"]["pass"]
    assert result["decision"] == "root-not-certified"
    assert result["normal_polynomial"] is None
    assert result["quotient"] is None
    assert result["schur"] is None


@pytest.mark.parametrize("horizon", [3, 7, 17])
def test_coefficient_box_encloses_independent_chord_formula(horizon):
    parameters = replace(_square_inputs("0.5")["parameters"], horizon=horizon)
    previous_precision = iv.dps
    iv.dps = 70
    try:
        radius = iv.mpf(["1.09", "1.11"])
        theta = iv.mpf(["0.12", "0.14"])
        observed = _normal_characteristic_polynomial(radius, theta, parameters)
        with mp.workdps(100):
            # Different chord identity and direct age powers instead of recurrence.
            for r, angle in (("1.09", "0.12"), ("1.1", "0.13"), ("1.11", "0.14")):
                alpha = mp.mpf(parameters.alpha)
                couplings = []
                for age in range(1, horizon):
                    chord = 2 * mp.mpf(r) * mp.sin(age * mp.mpf(angle) / 2)
                    gradient = sum(
                        sign
                        * mp.mpf(amplitude)
                        / mp.mpf(sigma) ** 2
                        * mp.exp(-(chord**2) / (2 * mp.mpf(sigma) ** 2))
                        for sign, amplitude, sigma in (
                            (-1, parameters.amplitude_rep, parameters.sigma_rep),
                            (1, parameters.amplitude_att, parameters.sigma_att),
                        )
                    )
                    couplings.append(
                        mp.mpf(parameters.eta)
                        * alpha
                        * mp.mpf(parameters.memory_mass)
                        * (1 - alpha) ** age
                        * gradient
                    )
                expected = [mp.mpf(1), sum(couplings) - 1] + [-c for c in couplings]
                for interval, point in zip(observed, expected, strict=True):
                    assert _fraction(interval._mpi_[0]) <= _fraction(point._mpf_)
                    assert _fraction(point._mpf_) <= _fraction(interval._mpi_[1])
    finally:
        iv.dps = previous_precision


def test_certificate_to_coefficient_bridge_never_reuses_displayed_decimals(monkeypatch):
    import emergenz_knoten.fifo_normal_stability as module

    inputs = _square_inputs("0.5")
    expected = certify_normal_fifo_box(**inputs, precision_dps=60)
    real_certificate = module.certify_rotating_wave_box

    def unreadable_display(**arguments):
        certificate = real_certificate(**arguments)
        for record in certificate["box"]:
            record["lower"] = "display-only"
            record["upper"] = "display-only"
            record["midpoint"] = "display-only"
        return certificate

    monkeypatch.setattr(module, "certify_rotating_wave_box", unreadable_display)
    observed = certify_normal_fifo_box(**inputs, precision_dps=60)
    assert observed["normal_polynomial"] == expected["normal_polynomial"]
    assert observed["quotient"] == expected["quotient"]
    assert observed["decision"] == expected["decision"]


@pytest.mark.parametrize("horizon", [4, 7])
def test_coefficient_builder_matches_native_kernel_normal_derivative(horizon):
    parameters = replace(_square_inputs("0.5")["parameters"], horizon=horizon)
    ages = np.arange(horizon)
    history = np.column_stack(
        (1.1 * np.cos(0.31 * ages), -1.1 * np.sin(0.31 * ages), np.zeros(horizon))
    )
    weights = finite_memory_weights(alpha=0.5, memory_mass=1.0, horizon=horizon)

    def new_height(points):
        gradient = double_gaussian_gradient(
            points[0],
            points,
            weights,
            sigma_rep=1.0,
            sigma_att=2.0,
            amplitude_rep=float(parameters.amplitude_rep),
            amplitude_att=float(parameters.amplitude_att),
        )
        return (points[0] - gradient)[2]

    row = []
    for column in range(horizon):
        delta = np.zeros_like(history)
        delta[column, 2] = 1e-6
        row.append((new_height(history + delta) - new_height(history - delta)) / 2e-6)
    previous_precision = iv.dps
    iv.dps = 60
    try:
        polynomial = _normal_characteristic_polynomial(
            iv.mpf("1.1"), iv.mpf("0.31"), parameters
        )
        observed = [float(value.mid) for value in polynomial]
    finally:
        iv.dps = previous_precision
    np.testing.assert_allclose(
        observed, np.r_[1.0, -np.asarray(row)], rtol=1e-10, atol=1e-10
    )


def test_inconsistent_factor_is_reported_as_method_error_not_physical_instability(
    monkeypatch,
):
    import emergenz_knoten.fifo_normal_stability as module

    real_polynomial = module._normal_characteristic_polynomial

    def wrong_constant(*arguments):
        polynomial = real_polynomial(*arguments)
        polynomial[-1] += 1
        return polynomial

    monkeypatch.setattr(module, "_normal_characteristic_polynomial", wrong_constant)
    result = certify_normal_fifo_box(**_square_inputs("0.5"), precision_dps=60)
    assert result["root_certificate"]["pass"]
    assert result["decision"] == "inconsistent-symmetry-factor"
    assert result["schur"] is None


def test_adapter_restores_precision_after_internal_failure(monkeypatch):
    import emergenz_knoten.fifo_normal_stability as module

    original_precision = iv.dps

    def fail(*arguments):
        raise RuntimeError("synthetic failure")

    monkeypatch.setattr(module, "rotation_symmetry_division", fail)
    with pytest.raises(RuntimeError, match="synthetic failure"):
        certify_normal_fifo_box(**_square_inputs("0.5"), precision_dps=60)
    assert iv.dps == original_precision


def test_companion_spectrum_of_manufactured_square_has_known_non_symmetry_mode():
    result = certify_normal_fifo_box(**_square_inputs("0.75"), precision_dps=60)
    coefficients = np.array(
        [float(record["midpoint"]) for record in result["normal_polynomial"]]
    )
    roots = np.roots(coefficients)
    for expected in (1, 1j, -1j, 9 / 7):
        assert np.min(np.abs(roots - expected)) < 2e-14


@pytest.mark.parametrize("precision", [True, 49, 60.5])
def test_adapter_rejects_invalid_precision(precision):
    with pytest.raises(ValueError, match="precision_dps"):
        certify_normal_fifo_box(**_square_inputs("0.5"), precision_dps=precision)


@pytest.mark.parametrize(
    "field,value,error",
    [
        ("radius", 1.0, TypeError),
        ("theta", "nan", ValueError),
        ("radius_half_width", "0", ValueError),
        ("theta_half_width", "not-a-number", ValueError),
    ],
)
def test_adapter_rejects_invalid_root_inputs(field, value, error):
    inputs = _square_inputs("0.5") | {field: value}
    with pytest.raises(error):
        certify_normal_fifo_box(**inputs, precision_dps=60)


def test_adapter_requires_three_independent_symmetry_vectors():
    inputs = _square_inputs("0.5")
    inputs["parameters"] = replace(inputs["parameters"], horizon=2)
    with pytest.raises(ValueError, match="horizon"):
        certify_normal_fifo_box(**inputs, precision_dps=60)


def test_adapter_does_not_silently_turn_float_parameters_into_exact_decimals():
    inputs = _square_inputs("0.5")
    inputs["parameters"] = replace(inputs["parameters"], eta=1.0)
    with pytest.raises(TypeError, match="eta"):
        certify_normal_fifo_box(**inputs, precision_dps=60)
