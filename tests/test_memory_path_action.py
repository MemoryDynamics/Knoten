"""Fixed off-shell histories, no native trajectory or target parameters."""

import numpy as np
import pytest
from scipy.integrate import quad
from scipy.stats import norm

from emergenz_knoten.kernels import (
    gaussian_gradient,
    gaussian_hessian,
    gaussian_potential,
)


PATH = np.array([[0.1, 0.4], [0.3, -0.2], [0.8, 0.1], [0.2, 0.6], [-0.4, 0.2]])
WEIGHTS = np.array([0.5, 0.28, 0.13])
WIDTH = 0.9


def _read(path, time, kernel):
    history = path[max(0, time - len(WEIGHTS) + 1) : time + 1][::-1]
    return kernel(path[time], history, WEIGHTS[: len(history)], sigma=WIDTH)


def _retarded(path):
    return -np.stack(
        [_read(path, time, gaussian_gradient) for time in range(len(path))]
    )


def _jacobian(function, value):
    step = 1e-6
    shifts = np.eye(value.size).reshape((value.size, *value.shape))
    return np.stack(
        [
            (function(value + step * shift) - function(value - step * shift))
            / (2 * step)
            for shift in shifts
        ],
        axis=-1,
    )


@pytest.mark.parametrize(("past", "present"), [(1, 2), (1, 3)])
def test_retarded_history_force_has_nonzero_one_sided_mixed_derivative(past, present):
    jacobian = _jacobian(_retarded, PATH).reshape(5, 2, 5, 2)
    age = present - past
    expected = gaussian_hessian(
        PATH[present], PATH[past : past + 1], WEIGHTS[age : age + 1], sigma=WIDTH
    )
    np.testing.assert_allclose(jacobian[present, :, past, :], expected, atol=1e-10)
    assert np.linalg.norm(expected) > 0.05
    np.testing.assert_array_equal(jacobian[past, :, present, :], 0)


def test_varying_the_sum_of_read_potentials_adds_the_advanced_force():
    def potential(path):
        return sum(_read(path, time, gaussian_potential) for time in range(len(path)))

    gradient = _jacobian(potential, PATH).reshape(PATH.shape)
    retarded = _retarded(PATH)
    advanced = _retarded(PATH[::-1])[::-1]
    np.testing.assert_allclose(-gradient, retarded + advanced, atol=3e-10)
    assert np.linalg.norm(advanced) > 0.1


def test_explicit_noise_residual_has_unit_triangular_jacobian():
    def residual(suffix):
        path = np.concatenate((PATH[:1], suffix))
        return (np.diff(path, axis=0) - _retarded(path)[:-1]).ravel()

    jacobian = _jacobian(residual, PATH[1:])
    np.testing.assert_array_equal(np.triu(jacobian, k=1), 0)
    np.testing.assert_allclose(np.diag(jacobian), 1, atol=5e-11)
    assert np.linalg.det(jacobian) == pytest.approx(1, abs=2e-10)


def test_fourier_response_factor_reconstructs_positive_gaussian_weight():
    sigma = 0.61
    coordinates = PATH[:, :1]
    residuals = (np.diff(coordinates, axis=0) - _retarded(coordinates)[:-1]).ravel()
    for residual in residuals:
        integral, _ = quad(
            lambda q: np.cos(q * residual) * np.exp(-0.5 * sigma**2 * q**2),
            0,
            np.inf,
        )
        assert integral / np.pi == pytest.approx(
            norm.pdf(residual, scale=sigma), abs=1e-12
        )
