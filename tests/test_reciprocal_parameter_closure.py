import numpy as np
import pytest

from emergenz_knoten import (
    FiniteMemoryState,
    SimulationConfig,
    common_gain_scale_interval,
    double_gaussian_gradient,
    double_gaussian_hessian,
    finite_memory_gain_matrix,
    gaussian_gradient,
    gaussian_hessian,
    reciprocal_relative_mode_operator,
)
from emergenz_knoten.reciprocal_modes import reciprocal_scalar_memory_modes


def test_gaussian_hessian_matches_gradient_finite_difference() -> None:
    point = np.array([0.2, -0.1])
    memory = np.array([[0.0, 0.0], [0.7, -0.3]])
    weights = np.array([0.6, 0.4])
    step = 1.0e-6
    numerical = np.column_stack(
        [
            (
                gaussian_gradient(
                    point + step * np.eye(2)[axis],
                    memory,
                    weights,
                    sigma=1.3,
                    amplitude=2.1,
                )
                - gaussian_gradient(
                    point - step * np.eye(2)[axis],
                    memory,
                    weights,
                    sigma=1.3,
                    amplitude=2.1,
                )
            )
            / (2.0 * step)
            for axis in range(2)
        ]
    )
    analytic = gaussian_hessian(
        point,
        memory,
        weights,
        sigma=1.3,
        amplitude=2.1,
    )
    assert np.allclose(analytic, numerical, rtol=2.0e-10, atol=2.0e-10)
    assert np.allclose(analytic, analytic.T, atol=1.0e-15)


def test_double_gaussian_hessian_matches_gradient_finite_difference() -> None:
    point = np.array([0.15, 0.25, -0.05])
    memory = np.array([[0.0, 0.0, 0.0], [0.4, -0.2, 0.3]])
    weights = np.array([0.7, 0.2])
    step = 1.0e-6
    identity = np.eye(3)
    numerical = np.column_stack(
        [
            (
                double_gaussian_gradient(
                    point + step * identity[axis],
                    memory,
                    weights,
                    sigma_rep=1.0,
                    sigma_att=3.0,
                    amplitude_rep=1.0,
                    amplitude_att=35.0,
                )
                - double_gaussian_gradient(
                    point - step * identity[axis],
                    memory,
                    weights,
                    sigma_rep=1.0,
                    sigma_att=3.0,
                    amplitude_rep=1.0,
                    amplitude_att=35.0,
                )
            )
            / (2.0 * step)
            for axis in range(3)
        ]
    )
    analytic = double_gaussian_hessian(
        point,
        memory,
        weights,
        sigma_rep=1.0,
        sigma_att=3.0,
        amplitude_rep=1.0,
        amplitude_att=35.0,
    )
    assert np.allclose(analytic, numerical, rtol=2.0e-9, atol=2.0e-9)


def test_matrix_operator_reduces_to_scalar_modes() -> None:
    scalar = reciprocal_scalar_memory_modes(0.01, self_gain=0.005, cross_gain=0.02)
    matrix = reciprocal_relative_mode_operator(
        0.01,
        0.005 * np.eye(3),
        0.02 * np.eye(3),
    )
    expected = np.sort_complex(np.tile(scalar.relative_multipliers, 3))
    observed = np.sort_complex(matrix.eigenvalues)
    assert np.allclose(observed, expected, atol=1.0e-13)
    assert matrix.is_stable
    assert matrix.has_complex_pair
    assert matrix.has_stable_complex_pair


def test_matrix_operator_is_rotation_covariant() -> None:
    angle = 0.37
    rotation = np.array(
        [[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]]
    )
    self_gain = np.diag([0.003, 0.006])
    cross_gain = np.array([[0.018, 0.002], [0.002, 0.014]])
    original = reciprocal_relative_mode_operator(0.01, self_gain, cross_gain)
    rotated = reciprocal_relative_mode_operator(
        0.01,
        rotation @ self_gain @ rotation.T,
        rotation @ cross_gain @ rotation.T,
    )
    assert np.allclose(
        np.sort_complex(original.eigenvalues),
        np.sort_complex(rotated.eigenvalues),
        atol=1.0e-13,
    )


def test_finite_memory_gain_matrix_uses_readout_hessian_without_fit() -> None:
    state = FiniteMemoryState(
        x=np.zeros(2),
        memory=np.zeros((1, 2)),
        weights=np.ones(1),
    )
    config = SimulationConfig(
        dim=2,
        eta=0.1,
        amplitude_rep=0.0,
        amplitude_att=2.0,
        sigma_att=2.0,
    )
    gain = finite_memory_gain_matrix(state.x, state, config)
    assert gain == pytest.approx(0.05 * np.eye(2))


def test_common_scale_interval_contains_only_stable_complex_modes() -> None:
    interval = common_gain_scale_interval(
        0.01,
        base_self_gain=0.43229117,
        base_cross_gain=0.489318,
    )
    assert interval.exists
    scale = interval.geometric_midpoint
    mode = reciprocal_relative_mode_operator(
        0.01,
        scale * np.eye(1) * 0.43229117,
        scale * np.eye(1) * 0.489318,
    )
    assert interval.lower < scale < interval.upper
    assert mode.is_stable
    assert mode.has_complex_pair


@pytest.mark.parametrize(
    ("self_gain", "cross_gain"),
    [(0.4, 0.4), (0.4, 0.1), (0.4, 0.0)],
)
def test_common_scale_interval_rejects_missing_complex_window(
    self_gain: float,
    cross_gain: float,
) -> None:
    interval = common_gain_scale_interval(0.01, self_gain, cross_gain)
    assert not interval.exists
