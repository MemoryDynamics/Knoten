import math

import numpy as np
import pytest

from experiments.current.dynamics.scaling.scalar_memory_center_finite_h_port_a2 import (
    _finite_h_transfer_grid,
    certify_case,
    finite_h_parameters,
    truncated_geometric_mean_age,
)


@pytest.mark.parametrize(
    ("alpha", "horizon", "omega"),
    [
        (0.4, 1, 0.0),
        (0.1, 17, 0.37),
        (0.01, 1200, 1.4),
        (0.0025, 4800, math.pi),
    ],
)
def test_finite_memory_filter_is_normalized_geometric_sum(
    alpha, horizon, omega
):
    q = 1.0 - alpha
    z = np.exp(1j * omega)
    ages = np.arange(horizon, dtype=float)
    normalized_weights = alpha * q**ages / (1.0 - q**horizon)

    direct_sum = np.sum(normalized_weights * z ** (-ages))
    closed_form = (
        alpha
        / (1.0 - q**horizon)
        * (1.0 - q**horizon * z ** (-horizon))
        / (1.0 - q / z)
    )

    np.testing.assert_allclose(np.sum(normalized_weights), 1.0, atol=2.0e-15)
    np.testing.assert_allclose(direct_sum, closed_form, atol=2.0e-14)


def test_finite_memory_center_recurrence_keeps_retirement_term():
    alpha = 0.07
    q = 1.0 - alpha
    horizon = 23
    ages = np.arange(horizon)
    weights = alpha * q**ages / (1.0 - q**horizon)
    positions = np.random.default_rng(20260820).normal(size=horizon + 31)

    for n in range(horizon - 1, positions.size - 1):
        center = np.sum(weights * positions[n - ages])
        center_next = np.sum(weights * positions[n + 1 - ages])
        recurrence = (
            q * center
            + alpha / (1.0 - q**horizon) * positions[n + 1]
            - alpha * q**horizon / (1.0 - q**horizon) * positions[n - horizon + 1]
        )
        np.testing.assert_allclose(center_next, recurrence, atol=1.0e-14)


def test_untruncated_center_elimination_is_exactly_second_order():
    alpha = 0.03
    q = 1.0 - alpha
    gain = 0.12
    relative_root = q * (1.0 - gain)
    forces = np.random.default_rng(20260820).normal(size=200)
    x = 0.0
    center = 0.0
    previous_center = 0.0

    for force in forces:
        x_next = (1.0 - gain) * x + gain * center + alpha * force
        center_next = q * center + alpha * x_next
        residual = (
            center_next
            - center
            - relative_root * (center - previous_center)
            - alpha**2 * force
        )
        assert abs(residual) < 2.0e-15
        previous_center, center, x = center, center_next, x_next


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
