import json

import numpy as np
import pytest

from experiments.current.topology.s1_control_pipeline import (
    DEFAULT_SPLIT_SEEDS,
    build_control_suite,
    noisy_circle,
    normalize_point_cloud,
    persistent_h1_summary,
    validate_coefficient_prime,
)


@pytest.fixture(scope="module")
def training_suite():
    return build_control_suite()


def test_registered_control_splits_have_distinct_seeds_without_opening_holdout():
    assert (
        DEFAULT_SPLIT_SEEDS["method-training"]
        != DEFAULT_SPLIT_SEEDS["method-validation"]
    )


def test_synthetic_normalization_is_translation_and_scale_invariant():
    points = noisy_circle(np.random.default_rng(421), n_points=64)
    normalized, _ = normalize_point_cloud(points)
    transformed, _ = normalize_point_cloud(3.7 * points + np.array([8.0, -2.5]))
    np.testing.assert_allclose(normalized, transformed, rtol=0.0, atol=2e-15)

    original_summary = persistent_h1_summary("original", points)
    transformed_summary = persistent_h1_summary("transformed", 3.7 * points + 5.0)
    np.testing.assert_allclose(
        original_summary.h1_lifetimes,
        transformed_summary.h1_lifetimes,
        rtol=0.0,
        atol=2e-6,
    )


@pytest.mark.parametrize("coefficient", [-1, 0, 1, 4, 6, 9])
def test_coefficient_must_be_prime(coefficient):
    with pytest.raises(ValueError, match="prime"):
        validate_coefficient_prime(coefficient)


@pytest.mark.parametrize(
    "points",
    [
        np.zeros((3, 2)),
        np.zeros((4, 0)),
        np.zeros((4, 2)),
        np.array([[0.0], [1.0], [2.0], [np.nan]]),
    ],
)
def test_invalid_point_clouds_are_rejected(points):
    with pytest.raises(ValueError):
        normalize_point_cloud(points)


def test_full_cloud_persistence_is_point_order_invariant(training_suite):
    error = training_suite.diagnostics["point_order_max_h1_lifetime_error"]
    assert error is not None
    assert error < 1e-12


def test_controls_expose_one_and_two_generator_cases(training_suite):
    circle = training_suite.summaries["noisy-circle"]
    hopf = training_suite.summaries["stable-hopf-cycle"]
    torus = training_suite.summaries["flat-torus"]
    disk = training_suite.summaries["filled-disk"]
    interval = training_suite.summaries["noisy-interval"]

    assert circle.top_h1_lifetime > 3.0 * disk.top_h1_lifetime
    assert circle.top_h1_lifetime > 20.0 * interval.top_h1_lifetime
    assert hopf.top_h1_lifetime > 1.0
    assert torus.second_h1_lifetime > 0.5
    assert torus.top_h1_gap < 0.1
    assert all(
        summary.essential_h1_count == 0 for summary in training_suite.summaries.values()
    )


def test_finite_discrete_cycle_is_a_deliberately_dangerous_semantic_rival(
    training_suite,
):
    circle = training_suite.summaries["noisy-circle"]
    finite_cycle = training_suite.summaries["finite-12-cycle"]

    assert finite_cycle.top_h1_lifetime > 0.5 * circle.top_h1_lifetime
    assert finite_cycle.top_h1_share > 0.9
    assert (
        "twelve points rather than topology S1"
        in training_suite.roles["finite-12-cycle"]
    )


def test_machine_record_is_finite_json_and_excludes_raw_clouds(training_suite):
    record = training_suite.to_json_dict()
    assert "clouds" not in record
    encoded = json.dumps(record, allow_nan=False)
    assert "method-development-only-no-candidate-data" in encoded
