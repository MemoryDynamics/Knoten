"""Constructed paths and finite probability spaces; no target integration."""

from dataclasses import asdict
from itertools import product
from math import comb

import numpy as np
import pytest

from emergenz_knoten.core import update_history
from emergenz_knoten.kernels import ScalarReadoutKernel, double_gaussian_gradient
from emergenz_knoten.pair_lag_diagnostics import analyze_frozen_pair_window
from emergenz_knoten.pair_path_diagnostics import (
    analyze_pair_geometry,
    fifo_centers,
    paired_replica_contrast,
    replica_hoeffding_half_width,
)


KERNEL = ScalarReadoutKernel(1.0, 2.0, 1.0, 3.0)


@pytest.mark.parametrize("horizon", [1, 3, 5])
def test_convolution_centers_match_explicit_fifo_with_arbitrary_initial_current_point(
    horizon,
):
    history = np.arange(horizon * 3, dtype=float).reshape(horizon, 3) / 9
    points = np.cos(np.arange(39).reshape(13, 3))
    weights = np.arange(1, horizon + 1, dtype=float)[::-1]
    actual = fifo_centers(history, points, weights)
    for step in range(len(points)):
        if step:
            history, _ = update_history(history, points[step], horizon)
        np.testing.assert_allclose(
            actual[step], np.average(history, weights=weights, axis=0), atol=2e-15
        )


@pytest.mark.parametrize("dim", [2, 5])
def test_geometry_split_and_bounds_match_full_native_gradients(dim):
    points = 0.2 * np.sin(np.arange(13 * 2 * dim).reshape(13, 2, dim) / 7)
    histories = [np.cos(np.arange(h * dim).reshape(h, dim)) / 10 for h in (3, 4)]
    weights = [np.array([3, 2, 1]), np.array([4, 3, 2, 1])]
    r = np.arange(1, dim + 1) / 10
    result = analyze_pair_geometry(
        points, histories, weights, r, start=5, stop=12, kernel=KERNEL
    )
    native = []
    for step in range(len(points)):
        if step:
            for node in (0, 1):
                histories[node], _ = update_history(
                    histories[node], points[step, node], len(weights[node])
                )
        if 5 <= step < 12:
            native.append(
                [
                    double_gaussian_gradient(
                        points[step, i],
                        histories[1 - i],
                        weights[1 - i] / weights[1 - i].sum(),
                        **asdict(KERNEL),
                    )
                    for i in (0, 1)
                ]
            )
    frozen = analyze_frozen_pair_window(
        result["inner"][:, 0],
        result["inner"][:, 1],
        r,
        *weights,
        start=5,
        stop=12,
        kernel=KERNEL,
    )
    for node, row in enumerate(result["directions"]):
        np.testing.assert_allclose(
            row["native_mean"], np.mean(native, axis=0)[node], atol=2e-15
        )
        np.testing.assert_allclose(
            row["frozen_mean"], frozen["mean_gradients"][node], atol=2e-15
        )
        np.testing.assert_allclose(
            row["native_mean"] - row["frozen_mean"],
            row["geometry_correction"],
            atol=2e-15,
        )
        assert (
            np.linalg.norm(row["geometry_correction"])
            <= row["full_gradient_bound"] + 1e-15
        )
        assert (
            np.linalg.norm(row["nonlinear_correction"])
            <= row["nonlinear_bound"] + 1e-15
        )


@pytest.mark.parametrize("speed", [0.0, 0.04])
def test_common_source_motion_is_not_erased_by_recentering(speed):
    r, velocity = np.array([0.8, 0.2]), np.array([speed, 0.3 * speed])
    origins = np.stack((r / 2, -r / 2))
    points = origins[None, :, :] + np.arange(10)[:, None, None] * velocity
    initial = [origin - np.arange(3)[:, None] * velocity for origin in origins]
    weights = [np.array([0.5, 0.3, 0.2])] * 2
    result = analyze_pair_geometry(
        points, initial, weights, r, start=3, stop=9, kernel=KERNEL
    )
    for row in result["directions"]:
        assert row["separation_motion_budget"] < 1e-15
        assert row["source_motion_budget"] == pytest.approx(
            0.7 * np.linalg.norm(velocity), abs=1e-15
        )
        if speed:
            assert np.linalg.norm(row["geometry_correction"]) > 1e-4
        else:
            np.testing.assert_allclose(row["geometry_correction"], 0, atol=1e-15)


def _h(first, second):
    return np.mean(
        [
            double_gaussian_gradient(
                np.array([1, 0.2]) + first[t],
                second[t - np.arange(2)],
                np.array([0.7, 0.3]),
                **asdict(KERNEL),
            )
            for t in range(2, 7)
        ],
        axis=0,
    )


@pytest.mark.parametrize("coupled", [False, True])
def test_replica_contrast_is_unbiased_on_exact_finite_nonstationary_ensembles(coupled):
    signs = [(s, s) for s in (-1, 1)] if coupled else list(product((-1, 1), repeat=2))
    trend = np.arange(8)[:, None] ** 2 * np.array([[0.01, -0.005]])
    states = [
        (trend + a * np.array([0.25, 0]), trend + b * np.array([0.25, 0]))
        for a, b in signs
    ]
    diagnostics, product_means = [], []
    for (a1, b1), (a2, b2) in product(states, repeat=2):
        value = paired_replica_contrast(
            np.stack((a1, a2)),
            np.stack((b1, b2)),
            [1, 0.2],
            [[0.7, 0.3]] * 2,
            start=2,
            stop=7,
            kernel=KERNEL,
        )
        diagnostics.append(value["contrast"][0])
        product_means.append(_h(a1, b2))
        assert (
            np.linalg.norm(value["contrast"][0])
            <= value["global_norm_bound_per_direction"]
        )
        np.testing.assert_allclose(
            value["contrast"][0],
            (_h(a1, b1) + _h(a2, b2) - _h(a1, b2) - _h(a2, b1)) / 2,
            atol=2e-15,
        )
    expected = np.mean([_h(a, b) for a, b in states], axis=0) - np.mean(
        product_means, axis=0
    )
    np.testing.assert_allclose(np.mean(diagnostics, axis=0), expected, atol=2e-15)
    if coupled:
        assert np.linalg.norm(expected) > 1e-4
    else:
        np.testing.assert_allclose(expected, 0, atol=2e-15)


def test_common_trend_creates_time_product_contrast_but_not_replica_contrast():
    trend = np.arange(9)[:, None] ** 2 * np.array([[0.03, 0.01]])
    temporal = analyze_frozen_pair_window(
        trend, trend, [1, 0.2], [1], [1], start=2, stop=8, kernel=KERNEL
    )
    copies = np.stack((trend, trend))
    replicas = paired_replica_contrast(
        copies, copies, [1, 0.2], [[1], [1]], start=2, stop=8, kernel=KERNEL
    )
    assert np.linalg.norm(temporal["lag_product_contrast"]) > 1e-4
    np.testing.assert_array_equal(replicas["contrast"], 0)


def test_hoeffding_counting_multiplicity_and_exact_bounded_binomial_coverage():
    width = replica_hoeffding_half_width(2, KERNEL, family_size=6)
    assert replica_hoeffding_half_width(8, KERNEL, family_size=6) == pytest.approx(
        width / 2
    )
    assert replica_hoeffding_half_width(2, KERNEL, family_size=1) < width
    assert replica_hoeffding_half_width(2, KERNEL, family_size=6, alpha=0.01) > width
    bound = 2 * np.exp(-0.5) * (1 + 3 / 2)
    radius = replica_hoeffding_half_width(16, KERNEL, family_size=1, alpha=0.1)
    tail = (
        sum(comb(16, k) for k in range(17) if abs(bound * (2 * k / 16 - 1)) > radius)
        / 2**16
    )
    assert tail <= 0.1


@pytest.mark.parametrize("bad", [0, -1, 2.5, True])
def test_invalid_independent_pair_counts_are_rejected(bad):
    with pytest.raises(ValueError):
        replica_hoeffding_half_width(bad, KERNEL, family_size=6)


def test_geometry_rejects_window_before_complete_initial_history_replacement():
    with pytest.raises(ValueError, match="past support"):
        analyze_pair_geometry(
            np.zeros((6, 2, 2)),
            [np.zeros((3, 2))] * 2,
            [[1, 1, 1]] * 2,
            [1, 0],
            start=2,
            stop=6,
            kernel=KERNEL,
        )
