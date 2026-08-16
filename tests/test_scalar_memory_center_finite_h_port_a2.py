import math

import numpy as np
import pytest

from experiments.current.dynamics.scaling.scalar_memory_center_finite_h_port_a2 import (
    _finite_h_transfer_grid,
    certify_case,
    finite_h_parameters,
    truncated_geometric_mean_age,
)


def test_truncated_geometric_mean_age_matches_direct_sum():
    q = 0.8
    horizon = 7
    ages = np.arange(horizon, dtype=float)
    direct = float(np.sum(ages * q**ages) / np.sum(q**ages))

    assert truncated_geometric_mean_age(q=q, horizon=horizon) == pytest.approx(
        direct, rel=0.0, abs=1.0e-14
    )


def test_synthetic_finite_h_error_is_below_registered_analytic_bound():
    certificate = certify_case(alpha=0.1, tail_extent=6.0, chi=1.5)

    assert certificate.small_gain_stability_pass
    assert certificate.strict_positive_real_pass
    assert certificate.grid_bound_sanity_pass
    assert certificate.grid_maximum_transfer_error <= (
        certificate.finite_h_transfer_error_bound + 5.0e-13
    )


def test_grid_dc_gain_matches_closed_form_for_synthetic_case():
    alpha = 0.125
    q, horizon, tail, gain, root = finite_h_parameters(
        alpha=alpha, tail_extent=2.0, chi=1.0
    )
    grid = _finite_h_transfer_grid(
        alpha=alpha,
        horizon=horizon,
        q=q,
        tail=tail,
        gain=gain,
        root=root,
    )
    mean_age = truncated_geometric_mean_age(q=q, horizon=horizon)
    dc_gain = 1.0 / (1.0 + gain * mean_age)

    assert math.isfinite(grid["minimum_real_part"])
    assert grid["minimum_real_part"] <= dc_gain


@pytest.mark.parametrize(
    ("name", "value"),
    [("alpha", 1.0), ("tail_extent", 0.0), ("chi", -1.0)],
)
def test_invalid_synthetic_parameters_are_rejected(name, value):
    parameters = {"alpha": 0.1, "tail_extent": 3.0, "chi": 1.0}
    parameters[name] = value
    with pytest.raises(ValueError):
        certify_case(**parameters)
