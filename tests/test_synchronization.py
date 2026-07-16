import numpy as np
import pytest

from emergenz_knoten import (
    infer_reproducible_response_rank,
    lagged_cross_correlation,
    phase_locking_value,
    radius_from_shape,
    response_rank,
    shape_tensor,
)


def test_lagged_cross_correlation_recovers_delayed_response():
    rng = np.random.default_rng(17)
    driver = rng.normal(size=240)
    lag = 6
    responder = np.empty_like(driver)
    responder[:lag] = rng.normal(size=lag)
    responder[lag:] = driver[:-lag]

    result = lagged_cross_correlation(driver, responder, max_lag=12)

    assert result.best_lag == lag
    assert result.best_correlation > 0.95


def test_phase_locking_value_detects_constant_offset():
    phase = np.linspace(0.0, 10.0 * np.pi, 300)

    plv = phase_locking_value(phase, phase + 0.7)

    assert plv == pytest.approx(1.0)


def test_response_rank_uses_singular_value_energy():
    response = np.diag([3.0, 2.0, 0.0, 0.0])

    result = response_rank(response, energy_threshold=0.95)

    assert result.rank == 2
    assert result.singular_values.tolist() == [3.0, 2.0]
    assert result.cumulative_energy[-1] == pytest.approx(1.0)


def test_shape_tensor_and_radius_are_translation_invariant():
    points = np.array(
        [
            [10.0, -2.0],
            [12.0, -2.0],
            [10.0, 0.0],
            [12.0, 0.0],
        ]
    )
    shifted = points + np.array([100.0, -50.0])

    tensor = shape_tensor(points)
    shifted_tensor = shape_tensor(shifted)

    assert tensor.shape == (2, 2)
    np.testing.assert_allclose(tensor, shifted_tensor)
    assert radius_from_shape(tensor) == pytest.approx(np.sqrt(2.0))


def test_response_rank_inference_separates_energy_from_exact_significance():
    matrices = np.stack(
        [np.diag([3.0 + 0.1 * index, 2.0 - 0.05 * index, 0.0]) for index in range(5)]
    )

    exploratory = infer_reproducible_response_rank(matrices, confidence=0.90)
    conventional = infer_reproducible_response_rank(matrices, confidence=0.95)

    assert exploratory.energy_rank == 2
    assert exploratory.rank == 2
    assert exploratory.n_null == 16
    assert exploratory.minimum_attainable_p == pytest.approx(1.0 / 16.0)
    assert exploratory.p_values[:2].tolist() == pytest.approx([1.0 / 16.0, 1.0 / 16.0])
    assert conventional.energy_rank == 2
    assert conventional.rank == 0


def test_response_rank_inference_rejects_single_matrix():
    with pytest.raises(ValueError, match="n>=2"):
        infer_reproducible_response_rank(np.eye(3)[None, :, :])
