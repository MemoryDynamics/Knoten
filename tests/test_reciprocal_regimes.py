import numpy as np
import pytest

from emergenz_knoten.reciprocal_regimes import (
    classify_reciprocal_mode_regime,
    stable_complex_cross_gain_interval,
)


def test_weak_self_gain_interval_is_stable_complex_throughout() -> None:
    interval = stable_complex_cross_gain_interval(0.01, self_gain=0.0)
    assert interval is not None
    assert interval.lower == pytest.approx(0.001722, rel=1.0e-3)
    assert interval.upper == pytest.approx(0.056899, rel=1.0e-3)
    for cross_gain in np.linspace(interval.lower, interval.upper, 9)[1:-1]:
        assert (
            classify_reciprocal_mode_regime(
                0.01,
                self_gain=0.0,
                cross_gain=float(cross_gain),
            )
            == "complex_stable"
        )


def test_complex_interval_requires_cross_gain_above_self_gain() -> None:
    interval = stable_complex_cross_gain_interval(0.01, self_gain=0.005)
    assert interval is not None
    assert interval.lower >= 0.005 - 1.0e-12
    assert interval.upper < 1.0 - 0.005


def test_threshold_and_compact_baseline_have_no_complex_interval() -> None:
    lambda_value = 0.01
    threshold = lambda_value / (1.0 + lambda_value)
    assert stable_complex_cross_gain_interval(
        lambda_value,
        self_gain=threshold,
    ) is None
    current_gain = 0.15 * (35.0 / 9.0 - 1.0)
    assert stable_complex_cross_gain_interval(
        lambda_value,
        self_gain=current_gain,
    ) is None


def test_gain_sum_above_one_is_real_with_opposite_sign_multipliers() -> None:
    assert (
        classify_reciprocal_mode_regime(
            0.01,
            self_gain=0.4,
            cross_gain=0.7,
        )
        == "real_stable"
    )


@pytest.mark.parametrize("lambda_value", [0.0, -0.1, 1.1, np.nan])
def test_interval_rejects_invalid_lambda(lambda_value: float) -> None:
    with pytest.raises(ValueError):
        stable_complex_cross_gain_interval(lambda_value, self_gain=0.0)
