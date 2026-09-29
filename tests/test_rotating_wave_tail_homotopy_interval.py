from __future__ import annotations

import pytest

from emergenz_knoten import rotating_wave_interval as interval


PARAMETERS = interval.IntervalRotatingWaveParameters(
    alpha="0.1",
    horizon=2,
    memory_mass="1",
    eta="0.2",
    sigma_rep="1",
    sigma_att="3",
    amplitude_rep="1",
    amplitude_att="2",
)


def _identity_balance(context, radius, theta, _parameters):
    zero = context.mpf(0)
    one = context.mpf(1)
    return (
        (radius - context.mpf("1"), theta - context.mpf("0.5")),
        ((one, zero), (zero, one)),
        (zero, zero),
    )


def _certificate(monkeypatch, **overrides):
    monkeypatch.setattr(interval, "_balance_and_jacobian", _identity_balance)
    values = {
        "radius": "1",
        "theta": "0.5",
        "radius_half_width": "0.1",
        "theta_half_width": "0.1",
        "tail_scale_interval": ("0", "1"),
        "parameters": PARAMETERS,
        "residual_tail_bound": "0.01",
        "jacobian_radius_tail_bound": "0.01",
        "jacobian_theta_tail_bound": "0.01",
        "precision_dps": 80,
    }
    values.update(overrides)
    return interval.certify_rotating_wave_tail_homotopy_box(**values)


def test_uniform_tail_homotopy_records_strict_inclusion_and_regularity(monkeypatch):
    certificate = _certificate(monkeypatch)

    assert certificate["tail_scale_interval"] == ["0", "1"]
    assert certificate["gates"] == {
        "physical_domain": True,
        "inverse_nonsingular": True,
        "function_box_contains_zero": True,
        "krawczyk_strict_interior": True,
        "uniform_regularity": True,
    }
    assert certificate["pass"] is True
    assert float(certificate["regularity_infinity_norm_upper"]) < 1.0
    assert certificate["preconditioned_jacobian_defect"]


def test_tail_homotopy_scale_must_be_ordered_and_inside_unit_interval(monkeypatch):
    for scale in (("-0.1", "1"), ("0", "1.1"), ("0.8", "0.2")):
        with pytest.raises(ValueError):
            _certificate(monkeypatch, tail_scale_interval=scale)


def test_uniform_regularity_gate_fails_closed(monkeypatch):
    certificate = _certificate(
        monkeypatch,
        jacobian_radius_tail_bound="2",
        jacobian_theta_tail_bound="2",
    )

    assert certificate["gates"]["uniform_regularity"] is False
    assert certificate["pass"] is False


def test_tail_homotopy_rejects_negative_or_nonfinite_bounds(monkeypatch):
    for value in ("-1e-4", "NaN", "Infinity"):
        with pytest.raises(ValueError):
            _certificate(monkeypatch, residual_tail_bound=value)


def test_tail_homotopy_restores_interval_precision_after_singularity(monkeypatch):
    def singular(context, radius, theta, _parameters):
        zero = context.mpf(0)
        return ((radius, theta), ((zero, zero), (zero, zero)), (zero, zero))

    monkeypatch.setattr(interval, "_balance_and_jacobian", singular)
    previous = interval.iv.dps
    with pytest.raises(ArithmeticError, match="singular"):
        interval.certify_rotating_wave_tail_homotopy_box(
            radius="1",
            theta="0.5",
            radius_half_width="0.1",
            theta_half_width="0.1",
            tail_scale_interval=("0", "1"),
            parameters=PARAMETERS,
            residual_tail_bound="0.01",
            jacobian_radius_tail_bound="0.01",
            jacobian_theta_tail_bound="0.01",
            precision_dps=80,
        )
    assert interval.iv.dps == previous
