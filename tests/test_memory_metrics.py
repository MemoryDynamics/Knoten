from __future__ import annotations

import numpy as np
import pytest

from emergenz_knoten.memory_metrics import (
    covariance_precision_metric,
    exponential_block_weights,
    gaussian_rkhs_emission_norms,
    isotropic_rkhs_observability_metric,
    metric_pullback,
    observability_gramian,
    supported_subspace_overlap,
    trace_normalized_distance,
)


def test_covariance_precision_preserves_exact_null_direction() -> None:
    samples = np.column_stack((np.arange(6.0), 2.0 * np.arange(6.0), np.zeros(6)))
    estimate = covariance_precision_metric(samples, relative_cutoff=1e-10)
    assert estimate.rank == 1
    np.testing.assert_allclose(estimate.metric @ np.array([0.0, 0.0, 1.0]), 0.0)


def test_exponential_block_weights_are_cadence_consistent() -> None:
    fine = exponential_block_weights(np.arange(5), forgetting_factor=0.8)
    coarse = exponential_block_weights(np.array([0, 2, 4]), forgetting_factor=0.8)
    np.testing.assert_allclose(coarse, [fine[:2].sum(), fine[2:].sum()])


def test_observability_gramian_uses_output_scale() -> None:
    jacobians = np.zeros((3, 1, 2))
    jacobians[1:, 0] = [2.0, -1.0]
    gramian = observability_gramian(
        jacobians,
        np.array([0, 1, 2]),
        forgetting_factor=0.5,
        output_scale=2.0,
    )
    expected_weight = 0.5 + 0.25
    np.testing.assert_allclose(
        gramian,
        expected_weight * np.outer([1.0, -0.5], [1.0, -0.5]),
    )


def test_gaussian_rkhs_norm_matches_one_and_two_coincident_deposits() -> None:
    positions = np.zeros((3, 2))
    norms = gaussian_rkhs_emission_norms(
        positions,
        deposition_weight=0.2,
        carrier_decay=1.0,
        memory_decay=1.0,
        kernel_sigma=1.0,
    )
    np.testing.assert_allclose(norms, [0.0, 0.04, 0.16])


def test_isotropic_rkhs_metric_and_pullback_keep_longitudinal_null() -> None:
    metric = isotropic_rkhs_observability_metric(
        np.array([0.0, 1.0, 2.0]),
        np.array([0, 1, 2]),
        forgetting_factor=0.5,
        feature_dimension=3,
    )
    forward = np.diag([1.0, 1.0, 0.0])
    pullback = metric_pullback(forward, metric)
    np.testing.assert_allclose(pullback[2], 0.0)
    assert pullback[0, 0] == pytest.approx(pullback[1, 1])


def test_metric_shape_distance_and_supported_overlap() -> None:
    left = np.diag([2.0, 1.0, 0.0])
    scaled = 7.0 * left
    tilted = np.diag([0.0, 1.0, 2.0])
    assert trace_normalized_distance(left, scaled) == pytest.approx(0.0)
    assert supported_subspace_overlap(left, scaled) == pytest.approx(1.0)
    assert supported_subspace_overlap(left, tilted) == pytest.approx(0.5)
