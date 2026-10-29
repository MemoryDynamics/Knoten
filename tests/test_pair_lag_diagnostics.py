"""Constructed paths and static archive arithmetic, never target integration."""

from dataclasses import asdict
from decimal import Decimal, localcontext
import hashlib
import json
from pathlib import Path

import numpy as np
import pytest

from emergenz_knoten.kernels import ScalarReadoutKernel, double_gaussian_gradient
from emergenz_knoten.pair_lag_diagnostics import (
    analyze_frozen_pair_window,
    gaussian_gradient_remainder,
)
from emergenz_knoten.state import (
    FiniteMemoryState,
    memory_centroid,
    place_finite_memory_state,
)


KERNEL = ScalarReadoutKernel(1.0, 2.0, 1.0, 3.0)


def _direct(target, source, separation, weights, start, stop):
    weights = np.asarray(weights) / np.sum(weights)
    return np.mean(
        [
            double_gaussian_gradient(
                separation + target[t],
                source[t - np.arange(len(weights))],
                weights,
                **asdict(KERNEL),
            )
            for t in range(start, stop)
        ],
        axis=0,
    )


@pytest.mark.parametrize("dim", [2, 5])
def test_nonstationary_unequal_histories_decompose_exactly_against_native_kernel(dim):
    times = np.arange(17)[:, None]
    axes = np.arange(1, dim + 1)[None, :]
    first = 0.13 * np.sin(times * axes / 3) + 0.004 * times**2
    second = 0.21 * np.cos(times / (axes + 1))
    separation = np.arange(1, dim + 1) / 4
    pa, pb = np.array([3, 2, 1]), np.array([5, 3, 2, 1, 0.5])
    start, stop = 5, 14
    result = analyze_frozen_pair_window(
        first,
        second,
        separation,
        pa,
        pb,
        start=start,
        stop=stop,
        kernel=KERNEL,
        product_block_size=2,
    )
    native = np.stack(
        (
            _direct(first, second, separation, pb, start, stop),
            _direct(second, first, -separation, pa, start, stop),
        )
    )
    product = np.mean(
        [
            double_gaussian_gradient(
                separation + point,
                second[start:stop],
                np.ones(stop - start) / (stop - start),
                **asdict(KERNEL),
            )
            for point in first[start:stop]
        ],
        axis=0,
    )
    np.testing.assert_allclose(result["mean_gradients"], native, atol=2e-15)
    np.testing.assert_allclose(result["product_gradient"], product, atol=2e-15)
    np.testing.assert_allclose(
        native - np.stack((product, -product)),
        result["linear_excess"] + result["nonlinear_excess"],
        atol=2e-15,
    )
    assert np.max(np.abs(result["linear_excess"])) > 0.001
    lag_products = []
    for target, source, r, weights in (
        (first, second, separation, pb),
        (second, first, -separation, pa),
    ):
        terms = []
        for point in target[start:stop]:
            terms.append(
                sum(
                    weight
                    * double_gaussian_gradient(
                        r + point,
                        source[start - lag : stop - lag],
                        np.ones(stop - start) / (stop - start),
                        **asdict(KERNEL),
                    )
                    for lag, weight in enumerate(weights / weights.sum())
                )
            )
        lag_products.append(np.mean(terms, axis=0))
    np.testing.assert_allclose(
        result["lag_matched_product_gradients"], lag_products, atol=2e-15
    )
    np.testing.assert_allclose(
        native - lag_products,
        result["lag_product_contrast"],
        atol=2e-15,
    )
    np.testing.assert_allclose(
        result["nonlinear_excess"],
        result["nonlinear_marginal_shift"] + result["lag_product_contrast"],
        atol=2e-15,
    )
    assert np.all(
        np.linalg.norm(result["nonlinear_excess"], axis=1)
        <= result["nonlinear_excess_bound"] + 1e-15
    )
    assert np.all(
        np.linalg.norm(result["lag_product_contrast"], axis=1)
        <= result["lag_product_contrast_bound"] + 1e-15
    )
    single_block = analyze_frozen_pair_window(
        first,
        second,
        separation,
        pa,
        pb,
        start=start,
        stop=stop,
        kernel=KERNEL,
        product_block_size=50,
    )
    np.testing.assert_allclose(
        single_block["nonlinear_excess"], result["nonlinear_excess"], atol=2e-15
    )


@pytest.mark.parametrize("phase", [0, 1])
def test_perfectly_locked_cycles_pass_linear_product_comparison_but_not_nonlinear(
    phase,
):
    cycle = 0.35 * np.array([[1, 0, 0], [0, 1, 0], [-1, 0, 0], [0, -1, 0]])
    first = cycle[np.arange(16) % 4]
    second = cycle[(np.arange(16) + phase) % 4]
    result = analyze_frozen_pair_window(
        first,
        second,
        [2, 0.4, 0.1],
        [0.5, 0.25],
        [0.5, 0.25],
        start=4,
        stop=12,
        kernel=KERNEL,
    )
    np.testing.assert_allclose(result["linear_excess"], 0, atol=1e-16)
    np.testing.assert_allclose(
        result["linear_means"],
        np.stack((result["linear_product"], -result["linear_product"])),
        atol=1e-16,
    )
    assert np.max(np.linalg.norm(result["nonlinear_excess"], axis=1)) > 1e-4
    np.testing.assert_allclose(result["nonlinear_marginal_shift"], 0, atol=1e-15)
    imbalance = np.sum(result["mean_gradients"], axis=0)
    if phase == 0:
        np.testing.assert_allclose(first, second)
        np.testing.assert_allclose(imbalance, 0, atol=1e-15)
    else:
        np.testing.assert_allclose(second[:-1], first[1:])
        assert np.linalg.norm(imbalance) > 1e-4


@pytest.mark.parametrize("distance", [0.1, 1e-4, 1e-8])
def test_expm1_remainder_matches_70_digit_control_at_small_displacement(distance):
    with localcontext() as ctx:
        ctx.prec = 70
        z = Decimal.from_float(distance)
        reference = -z * ((-z * z / 2).exp() - 1)
        reference += Decimal(3) / 4 * z * ((-z * z / 8).exp() - 1)
    actual = gaussian_gradient_remainder(np.array([distance]), KERNEL)[0]
    assert actual == pytest.approx(float(reference), rel=4e-15, abs=0)
    assert actual != 0


def test_nonlinear_lag_contrast_over_linear_signal_shrinks_quadratically():
    cycle = 0.35 * np.array([[1, 0, 0], [0, 1, 0], [-1, 0, 0], [0, -1, 0]])
    ratios = []
    for scale in (0.01, 0.001):
        result = analyze_frozen_pair_window(
            scale * cycle[np.arange(16) % 4],
            scale * cycle[(np.arange(16) + 1) % 4],
            scale * np.array([2, 0.4, 0.1]),
            [0.5, 0.25],
            [0.5, 0.25],
            start=4,
            stop=12,
            kernel=KERNEL,
        )
        ratios.append(
            np.linalg.norm(result["lag_product_contrast"][0])
            / np.linalg.norm(result["linear_product"])
        )
    assert ratios[1] / ratios[0] == pytest.approx(0.01, rel=0.001)


def test_saved_initial_snapshot_bound_matches_native_static_placement():
    root = Path(__file__).resolve().parents[1]
    report = json.loads(
        (
            root / "reports/reference/memory_pair_initial_readiness_2026-10-29.json"
        ).read_text(encoding="utf-8")
    )
    checkpoint = root / report["checkpoint"]
    assert (
        hashlib.sha256(checkpoint.read_bytes()).hexdigest()
        == report["checkpoint_sha256"]
    )
    source_report_text = (root / report["report"]).read_text(encoding="utf-8")
    assert (
        hashlib.sha256(source_report_text.encode("utf-8")).hexdigest()
        == report["report_sha256_utf8_lf"]
    )
    source_report = json.loads(source_report_text)
    with np.load(checkpoint, allow_pickle=False) as saved:
        state = FiniteMemoryState(saved["x"], saved["memory"], saved["weights"])
    separation = np.array(source_report["derived"]["initial_center_separation"])
    first = place_finite_memory_state(state, -separation / 2)
    second = place_finite_memory_state(
        state,
        separation / 2,
        rotation=source_report["derived"]["second_state_rotation"],
    )
    assert (
        report["claim_class"]
        == "initial_snapshot_bound_only_not_a_path_or_statistical_power_bound"
    )
    assert report["cubic_coefficient"] == pytest.approx(58 / 81)
    for target, source, row in zip(
        (first, second), (second, first), report["directions"], strict=True
    ):
        probabilities = source.weights / source.weights.sum()
        distances = np.linalg.norm(target.x - source.memory, axis=1)
        bound = (58 / 81) * np.dot(probabilities, distances**3)
        linear = (26 / 9) * (target.x - memory_centroid(source))
        gradient = double_gaussian_gradient(
            target.x,
            source.memory,
            probabilities,
            **report["effective_kernel"],
        )
        assert row["normalized_cubic_bound"] == pytest.approx(bound, rel=1e-12, abs=0)
        assert row["bound_over_linear_signal"] == pytest.approx(
            bound / np.linalg.norm(linear), rel=1e-12
        )
        assert np.linalg.norm(gradient - linear) <= bound


@pytest.mark.parametrize(
    "change", ["missing_past", "noninteger", "zero_weights", "nan", "bad_block"]
)
def test_invalid_window_inputs_fail_before_returning_a_diagnostic(change):
    kwargs = dict(
        first_inner=np.zeros((8, 2)),
        second_inner=np.zeros((8, 2)),
        separation=[1, 0],
        first_weights=[0.7, 0.3],
        second_weights=[0.4, 0.6],
        start=2,
        stop=7,
        kernel=KERNEL,
    )
    if change == "missing_past":
        kwargs["start"] = 0
    elif change == "noninteger":
        kwargs["stop"] = 7.5
    elif change == "zero_weights":
        kwargs["first_weights"] = [0, 0]
    elif change == "nan":
        kwargs["second_inner"][0, 0] = np.nan
    else:
        kwargs["product_block_size"] = 0
    with pytest.raises(ValueError):
        analyze_frozen_pair_window(**kwargs)
