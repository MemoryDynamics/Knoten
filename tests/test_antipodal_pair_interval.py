"""Constructed small method fixtures only; no archived target evaluation."""

from dataclasses import replace

from mpmath import iv, mp
import numpy as np
import pytest

import emergenz_knoten.antipodal_pair_interval as pair
from emergenz_knoten.kernels import double_gaussian_gradient, double_gaussian_hessian
from emergenz_knoten.rotating_wave_interval import (
    IntervalRotatingWaveParameters,
    point_balance_and_jacobian,
)
from emergenz_knoten.rotating_wave_stability import (
    circular_history,
    finite_memory_weights,
)


def _parameters(cross="0.04", horizon=7):
    return pair.AntipodalPairParameters(
        IntervalRotatingWaveParameters(
            alpha="0.2",
            horizon=horizon,
            memory_mass="1.1",
            eta="0.07",
            sigma_rep="1",
            sigma_att="2.2",
            amplitude_rep="1",
            amplitude_att="4.2",
        ),
        cross_eta=cross,
    )


def _native_balance_and_slope(radius, theta, parameters):
    p = parameters.self_parameters
    kernel = {
        name: float(getattr(p, name))
        for name in ("sigma_rep", "sigma_att", "amplitude_rep", "amplitude_att")
    }
    weights = finite_memory_weights(
        alpha=float(p.alpha), horizon=p.horizon, memory_mass=float(p.memory_mass)
    )
    history = np.column_stack(
        (
            circular_history(radius=radius, theta=theta, horizon=p.horizon),
            np.zeros(p.horizon),
        )
    )
    x = history[0]
    drift = float(p.eta) * double_gaussian_gradient(x, history, weights, **kernel)
    drift += float(parameters.cross_eta) * double_gaussian_gradient(
        x, -history, weights, **kernel
    )
    moved = x - drift
    target = radius * np.array([np.cos(theta), np.sin(theta), 0])
    defect = (moved - target) / radius
    slope = 1.0
    for age in range(1, p.horizon):
        for gain, sources in (
            (float(p.eta), history),
            (float(parameters.cross_eta), -history),
        ):
            slope += (
                age
                * gain
                * double_gaussian_hessian(
                    x, sources[age : age + 1], weights[age : age + 1], **kernel
                )[2, 2]
            )
    return np.array([defect[0], -defect[1]]), slope


@pytest.mark.parametrize("horizon", [2, 7, 17])
def test_point_balance_jacobian_and_slope_match_native_kernel(horizon):
    p = _parameters(horizon=horizon)
    radius, theta = 0.9, 0.37
    result = pair.point_pair_balance_and_jacobian(
        radius=str(radius), theta=str(theta), parameters=p, precision_dps=70
    )
    expected, slope = _native_balance_and_slope(radius, theta, p)
    np.testing.assert_allclose(
        np.array(result["balance"], dtype=float), expected, atol=4e-16, rtol=0
    )
    assert float(result["common_normal_slope"]) == pytest.approx(slope, abs=4e-16)
    step = 1e-6
    finite_difference = np.column_stack(
        (
            (
                _native_balance_and_slope(radius + step, theta, p)[0]
                - _native_balance_and_slope(radius - step, theta, p)[0]
            )
            / (2 * step),
            (
                _native_balance_and_slope(radius, theta + step, p)[0]
                - _native_balance_and_slope(radius, theta - step, p)[0]
            )
            / (2 * step),
        )
    )
    np.testing.assert_allclose(
        np.array(result["jacobian"], dtype=float),
        finite_difference,
        atol=2e-10,
        rtol=2e-8,
    )


def test_zero_cross_gain_reduces_to_existing_single_balance():
    p = _parameters(cross="0")
    observed = pair.point_pair_balance_and_jacobian(
        radius="0.9", theta="0.37", parameters=p, precision_dps=70
    )
    expected = point_balance_and_jacobian(
        radius="0.9", theta="0.37", parameters=p.self_parameters, precision_dps=70
    )
    with mp.workdps(80):
        for actual, wanted in zip(
            observed["balance"], expected["balance"], strict=True
        ):
            assert abs(mp.mpf(actual) - mp.mpf(wanted)) < mp.mpf("1e-61")
        for actual_row, wanted_row in zip(
            observed["jacobian"], expected["jacobian"], strict=True
        ):
            for actual, wanted in zip(actual_row, wanted_row, strict=True):
                assert abs(mp.mpf(actual) - mp.mpf(wanted)) < mp.mpf("1e-61")


def _constructed_quarter_turn_parameters():
    # Prescribed r=1, theta=pi/2, H=2. Gains follow algebraically, not a scan.
    # k(2)<0 and w1*k(2)+w0*k(4)>0 give positive gains and S_+<0.
    with mp.workdps(100):
        k2 = -mp.exp(-1) + mp.exp(-mp.mpf(1) / 9) / 3
        k4 = -mp.exp(-2) + mp.exp(-mp.mpf(2) / 9) / 3
        chi = 1 / (k2 / 4 + k4 / 2)
        eta = chi - 4 / k2
        return pair.AntipodalPairParameters(
            IntervalRotatingWaveParameters(
                alpha="0.5",
                horizon=2,
                memory_mass="1",
                eta=mp.nstr(eta, 90),
                sigma_rep="1",
                sigma_att="3",
                amplitude_rep="1",
                amplitude_att="3",
            ),
            cross_eta=mp.nstr(chi, 90),
        )


def test_constructed_native_orbit_is_certified_but_unstable():
    p = _constructed_quarter_turn_parameters()
    previous = (mp.dps, iv.dps)
    refined = pair.refine_antipodal_pair_root(
        radius="1.001", theta="1.57", parameters=p, precision_dps=80, iterations=6
    )
    assert refined["status"] == "iteration_budget_completed"
    assert not refined["root_certified"]
    assert len(refined["iterates"]) == 7
    assert len(refined["corrections"]) == 6
    assert float(refined["radius"]) == pytest.approx(1, abs=1e-14)
    assert float(refined["theta"]) == pytest.approx(np.pi / 2, abs=1e-14)
    result = pair.certify_antipodal_pair_box(
        radius=refined["radius"],
        theta=refined["theta"],
        radius_half_width="1e-25",
        theta_half_width="1e-25",
        parameters=p,
        precision_dps=80,
    )
    assert all(result["gates"].values())
    assert result["root_certified"]
    assert result["classification"] == "certified_orbit_common_normal_unstable"
    assert not result["stability_certified"]
    assert result["common_normal_slope_strictly_negative"]
    assert (mp.dps, iv.dps) == previous


def test_cross_age_zero_supplies_required_radial_force():
    p = _constructed_quarter_turn_parameters()
    with mp.workdps(80):
        theta = mp.nstr(mp.pi / 2, 75)
        result = pair.point_pair_balance_and_jacobian(
            radius="1", theta=theta, parameters=p, precision_dps=80
        )
        assert abs(mp.mpf(result["balance"][0])) < mp.mpf("1e-70")
        assert abs(mp.mpf(result["balance"][1])) < mp.mpf("1e-70")
        k4 = -mp.exp(-2) + mp.exp(-mp.mpf(2) / 9) / 3
        missing_force = mp.mpf(p.cross_eta) * k4
        assert missing_force > 1  # Omitting cross age zero cannot pass this fixture.


def test_interval_box_encloses_independent_interior_points():
    p = _parameters()
    result = pair.certify_antipodal_pair_box(
        radius="0.9",
        theta="0.37",
        radius_half_width="+0.01",
        theta_half_width="0.02",
        parameters=p,
        precision_dps=70,
    )
    assert not result["root_certified"]
    assert result["classification"] == "orbit_inconclusive"
    with mp.workdps(100):
        for radius, theta in (("0.9", "0.37"), ("0.891", "0.351"), ("0.909", "0.389")):
            point = pair.point_pair_balance_and_jacobian(
                radius=radius, theta=theta, parameters=p, precision_dps=90
            )
            intervals = (
                result["function_box"]
                + sum(result["jacobian_box"], [])
                + [result["common_normal_slope"]]
            )
            values = (
                point["balance"]
                + sum(point["jacobian"], [])
                + [point["common_normal_slope"]]
            )
            for interval, value in zip(intervals, values, strict=True):
                assert mp.make_mpf(tuple(interval["lower_binary"])) < mp.mpf(value)
                assert mp.mpf(value) < mp.make_mpf(tuple(interval["upper_binary"]))


@pytest.mark.parametrize("slope", [-1, 0, 1])
def test_classification_requires_root_and_never_claims_stability(monkeypatch, slope):
    def affine(context, radius, theta, parameters):
        return (
            (radius - 1, theta - 1),
            ((context.mpf(1), context.mpf(0)), (context.mpf(0), context.mpf(1))),
            context.mpf(slope),
        )

    monkeypatch.setattr(pair, "_pair_balance_and_jacobian", affine)
    arguments = dict(
        radius="1",
        theta="1",
        radius_half_width="0.01",
        theta_half_width="0.01",
        parameters=_parameters(),
        precision_dps=60,
    )
    result = pair.certify_antipodal_pair_box(**arguments)
    assert result["root_certified"]
    assert result["classification"] == (
        "certified_orbit_common_normal_unstable"
        if slope < 0
        else "certified_orbit_stability_unresolved"
    )
    assert not result["stability_certified"]
    arguments["radius"] = "2"
    failed = pair.certify_antipodal_pair_box(**arguments)
    assert failed["classification"] == "orbit_inconclusive"


@pytest.mark.parametrize("mode", ["singular", "domain", "nonfinite"])
def test_newton_exit_has_no_retry_or_existence_claim(monkeypatch, mode):
    calls = []

    def evaluation(context, radius, theta, parameters):
        calls.append((radius, theta))
        one, zero = context.mpf(1), context.mpf(0)
        j = (
            ((zero, zero), (zero, zero))
            if mode == "singular"
            else ((one, zero), (zero, one))
        )
        f = (
            (context.mpf("inf"), zero)
            if mode == "nonfinite"
            else (context.mpf(2), zero)
        )
        return f, j, one

    monkeypatch.setattr(pair, "_pair_balance_and_jacobian", evaluation)
    result = pair.refine_antipodal_pair_root(
        radius="1", theta="1", parameters=_parameters(), precision_dps=60, iterations=3
    )
    assert len(calls) == 1
    assert len(result["iterates"]) == 1
    assert not result["root_certified"]
    assert (
        result["status"]
        == {
            "singular": "singular_point_jacobian",
            "domain": "left_physical_domain",
            "nonfinite": "nonfinite_evaluation",
        }[mode]
    )


def test_singular_certificate_is_inconclusive_and_precision_restored(monkeypatch):
    def singular(context, radius, theta, parameters):
        zero = context.mpf(0)
        return (zero, zero), ((zero, zero), (zero, zero)), context.mpf(-1)

    monkeypatch.setattr(pair, "_pair_balance_and_jacobian", singular)
    previous = iv.dps
    result = pair.certify_antipodal_pair_box(
        radius="1",
        theta="1",
        radius_half_width="0.01",
        theta_half_width="0.01",
        parameters=_parameters(),
        precision_dps=60,
    )
    assert result["classification"] == "orbit_inconclusive"
    assert result["krawczyk_image"] is None
    assert iv.dps == previous


def test_interval_precision_restored_on_error(monkeypatch):
    def fail(*args):
        raise RuntimeError("constructed failure")

    monkeypatch.setattr(pair, "_pair_balance_and_jacobian", fail)
    previous = iv.dps
    with pytest.raises(RuntimeError, match="constructed failure"):
        pair.certify_antipodal_pair_box(
            radius="1",
            theta="1",
            radius_half_width="0.01",
            theta_half_width="0.01",
            parameters=_parameters(),
            precision_dps=60,
        )
    assert iv.dps == previous


@pytest.mark.parametrize("value", ["-1", "nan", "inf", "junk", 0.04, True])
def test_cross_gain_rejects_invalid_input(value):
    with pytest.raises((TypeError, ValueError)):
        _parameters(cross=value)


@pytest.mark.parametrize(
    "field,value",
    [
        ("radius", "0"),
        ("radius", "nan"),
        ("theta", "0"),
        ("theta", "3.2"),
        ("precision_dps", True),
        ("precision_dps", 49),
        ("precision_dps", 60.5),
    ],
)
def test_point_rejects_invalid_arguments(field, value):
    arguments = dict(radius="1", theta="1", parameters=_parameters(), precision_dps=60)
    arguments[field] = value
    with pytest.raises((TypeError, ValueError)):
        pair.point_pair_balance_and_jacobian(**arguments)


@pytest.mark.parametrize("iterations", [0, True, 1.5])
def test_newton_rejects_invalid_budget(iterations):
    with pytest.raises(ValueError, match="positive integer"):
        pair.refine_antipodal_pair_root(
            radius="1",
            theta="1",
            parameters=_parameters(),
            precision_dps=60,
            iterations=iterations,
        )


def test_parameter_composition_does_not_change_original_schema():
    p = _parameters()
    assert "cross_eta" not in p.self_parameters.__dataclass_fields__
    with pytest.raises(TypeError):
        replace(p, self_parameters={})
    with pytest.raises(TypeError, match="decimal string"):
        replace(p, self_parameters=replace(p.self_parameters, eta=0.07))


@pytest.mark.parametrize("width", ["0", "-0.01", "nan", "inf"])
def test_certificate_rejects_invalid_width(width):
    with pytest.raises(ValueError):
        pair.certify_antipodal_pair_box(
            radius="1",
            theta="1",
            radius_half_width=width,
            theta_half_width="0.01",
            parameters=_parameters(),
            precision_dps=60,
        )


def test_box_crossing_radius_zero_cannot_certify_physical_orbit():
    result = pair.certify_antipodal_pair_box(
        radius="0.1",
        theta="1",
        radius_half_width="0.2",
        theta_half_width="0.01",
        parameters=_parameters(),
        precision_dps=60,
    )
    assert not result["gates"]["physical_box"]
    assert not result["root_certified"]
    assert result["parameters"]["cross_eta"] == "0.04"
