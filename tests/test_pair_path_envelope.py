"""Small deterministic checks, no target replay or sampled noise ensemble."""

from dataclasses import replace

import numpy as np
import pytest

from emergenz_knoten import FiniteMemoryState, SimulationConfig
from emergenz_knoten.kernels import ScalarReadoutKernel, exponential_memory_weights
from emergenz_knoten.pair_path_envelope import (
    pair_path_envelope,
    truncated_contrast_budget,
)
from emergenz_knoten.reciprocal_nodes import reciprocal_pair_response


KERNEL = ScalarReadoutKernel(sigma_rep=1, sigma_att=2, amplitude_rep=1, amplitude_att=8)


def _input():
    histories = 1e-5 * np.sin(np.arange(180).reshape(2, 30, 3))
    points = 1e-5 * np.cos(np.arange(6).reshape(2, 3))
    return dict(
        points=points,
        histories=histories,
        alpha=0.2,
        eta=0.1,
        cross_eta=0.02,
        epsilon=1e-5,
        memory_mass=1.0,
        kernel=KERNEL,
        updates=7,
        diameter=0.01,
        gaussian_threshold=10.0,
    )


def test_closing_envelope_counts_entire_paths_not_independent_time_samples():
    args = _input()
    result = pair_path_envelope(**args)
    assert result["closes_numerically"]
    assert result["scalar_gaussian_count"] == 7 * 3 * 35
    longer = pair_path_envelope(**(args | {"updates": 70}))
    assert longer["closure_rhs"] == result["closure_rhs"]
    assert longer["failure_probability_bound"] == pytest.approx(
        10 * result["failure_probability_bound"]
    )


def test_positive_resolvents_and_covariance_against_finite_impulse_sums():
    args = _input()
    result = pair_path_envelope(**args)
    a = np.array(result["relative_matrix"])
    p = np.array(result["relative_covariance"])
    alpha, h, g = args["alpha"], result["cross_gain"], result["self_gain"]
    drive = np.array([1, alpha])
    inverse = np.linalg.inv(np.eye(2) - a)
    assert np.all(a >= 0)
    assert np.all(a.sum(axis=1) < 1)
    np.testing.assert_allclose(inverse @ drive, np.ones(2) / (2 * h))
    np.testing.assert_allclose(
        inverse[:, 1], np.array([g - h, g + h]) / (2 * alpha * h)
    )
    finite = np.zeros((2, 2))
    impulse = drive.copy()
    for _ in range(2000):
        finite += 2 * args["epsilon"] ** 2 * np.outer(impulse, impulse)
        impulse = a @ impulse
    np.testing.assert_allclose(finite, p, rtol=1e-12, atol=1e-24)
    np.testing.assert_allclose(
        p - a @ p @ a.T,
        2 * args["epsilon"] ** 2 * np.outer(drive, drive),
        rtol=1e-12,
        atol=1e-24,
    )


def test_common_lag_variance_matches_impulse_formula():
    args = _input()
    result = pair_path_envelope(**args)
    lam, alpha = result["common_multiplier"], args["alpha"]
    a0 = alpha / (1 - lam)
    a1 = 1 - a0
    weights = a0 + a1 * lam ** np.arange(1000)
    horizon = args["histories"].shape[1]
    explicit = (
        args["epsilon"] ** 2
        / 2
        * (
            np.sum(weights[:horizon] ** 2)
            + np.sum((weights[horizon:] - weights[:-horizon]) ** 2)
        )
    )
    assert explicit == pytest.approx(result["common_lag_variance_bound"], rel=1e-13)
    common, v = 0.0, 0.0
    for step in range(8):
        noise = float(step == 0)
        common += -(result["self_gain"] + result["cross_gain"]) * v + noise
        v = lam * v + (1 - alpha) * noise
        assert common == pytest.approx(weights[step], rel=1e-13)


@pytest.mark.parametrize("shift", [0.0, 0.3])
def test_seven_constructed_native_updates_respect_envelope_and_tail(shift):
    args = _input()
    args["points"] += shift
    args["histories"] += shift
    result = pair_path_envelope(**args)
    config = SimulationConfig(
        steps=7,
        dim=3,
        alpha=args["alpha"],
        eta=args["eta"],
        epsilon=args["epsilon"],
        memory_mass=1,
        sigma_rep=1,
        sigma_att=2,
        amplitude_rep=1,
        amplitude_att=8,
        max_memory=30,
        memory_factor=6,
        deposition_kernel="delta",
        deposition_sigma=0,
        burn_in=0,
        sample_every=1,
    )
    weights = exponential_memory_weights(config.alpha, 30, memory_mass=1)
    states = [
        FiniteMemoryState(args["points"][i], args["histories"][i], weights)
        for i in range(2)
    ]
    centers = np.einsum("h,ihd->id", weights / weights.sum(), args["histories"])
    noises = [np.sin(np.arange(21).reshape(7, 3) + phase) for phase in (0, 0.6)]
    native = reciprocal_pair_response(
        *states,
        config,
        initial_center_separation=centers[1] - centers[0],
        first_noise=noises[0],
        second_noise=noises[1],
        sample_steps=range(8),
        cross_eta=args["cross_eta"],
    )
    histories = args["histories"].copy()
    points, native_centers = native.positions[:, 2], native.memory_centers[:, 2]
    np.testing.assert_allclose(points[0], args["points"], atol=1e-16)
    for n in range(8):
        pool = np.concatenate([points[n], histories.reshape(-1, 3)])
        observed = np.max(np.linalg.norm(pool[:, None] - pool[None, :], axis=2))
        assert observed < result["closure_rhs"] < args["diameter"]
        assert (
            np.max(np.linalg.norm(points[n] - native_centers[n], axis=1))
            < result["inner_bound"]
        )
        if n < 7:
            tail = (
                native_centers[n + 1]
                - (1 - config.alpha) * native_centers[n]
                - config.alpha * points[n + 1]
            )
            assert np.max(np.linalg.norm(tail, axis=1)) <= result["tail_update_bound"]
            histories[:, 1:] = histories[:, :-1].copy()
            histories[:, 0] = points[n + 1]


def test_initial_current_point_need_not_equal_newest_deposit():
    args = _input()
    result = pair_path_envelope(**args)
    changed = pair_path_envelope(**(args | {"points": args["points"] + 0.0001}))
    assert changed["initial_common_inner"] > result["initial_common_inner"]
    assert changed["initial_common_offset"] > result["initial_common_offset"]
    assert changed["closure_rhs"] > result["closure_rhs"]


def test_nonclosing_diameter_is_reported_not_automatically_adjusted():
    result = pair_path_envelope(**(_input() | {"diameter": 1e-8}))
    assert not result["closes_numerically"]
    assert result["proposed_diameter"] == 1e-8
    with pytest.raises(ValueError, match="closing"):
        truncated_contrast_budget(result, 0.001, independent_pairs=2, family_size=6)


def test_truncation_width_and_unconditional_bias_count_disjoint_pairs():
    result = pair_path_envelope(**_input())
    budget = truncated_contrast_budget(
        result, 0.001, independent_pairs=2, family_size=6
    )
    more = truncated_contrast_budget(result, 0.001, independent_pairs=8, family_size=6)
    assert more["hoeffding_half_width"] == pytest.approx(
        budget["hoeffding_half_width"] / 2
    )
    assert (
        more["unconditional_truncation_bias_bound"]
        == budget["unconditional_truncation_bias_bound"]
    )
    assert budget["unconditional_truncation_bias_bound"] == pytest.approx(
        4 * result["global_gradient_bound"] * result["failure_probability_bound"]
    )
    assert not budget["includes_numerical_error"]


@pytest.mark.parametrize(
    "change",
    [
        {"alpha": 0},
        {"cross_eta": 0},
        {"cross_eta": 0.2},
        {"eta": 10},
        {"epsilon": -1},
        {"updates": True},
        {"updates": 2.5},
        {"diameter": np.nan},
        {"kernel": replace(KERNEL, sigma_att=0.5)},
        {"kernel": replace(KERNEL, amplitude_att=2)},
    ],
)
def test_outside_theorem_domain_is_rejected(change):
    with pytest.raises(ValueError):
        pair_path_envelope(**(_input() | change))
