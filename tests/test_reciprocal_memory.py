from __future__ import annotations

import numpy as np
import pytest

from emergenz_knoten import (
    metric_adjoint,
    normalized_direction_jacobian,
    reciprocal_memory_operator,
    reciprocal_memory_spectrum,
)


def test_metric_adjoint_satisfies_defining_inner_product() -> None:
    forward = np.array([[1.0, -0.5], [0.2, 2.0], [-1.0, 0.3]])
    visible_metric = np.array([[2.0, 0.2], [0.2, 1.0]])
    memory_metric = np.diag([0.5, 1.5, 3.0])
    visible = np.array([0.7, -1.2])
    memory = np.array([1.1, -0.4, 0.8])

    adjoint = metric_adjoint(
        forward,
        visible_metric=visible_metric,
        memory_metric=memory_metric,
    )

    left = (forward @ visible) @ memory_metric @ memory
    right = visible @ visible_metric @ (adjoint @ memory)
    assert left == pytest.approx(right)


def test_operator_spectrum_matches_exact_singular_mode_roots() -> None:
    forward = np.diag([0.4, 1.3])
    q = 0.83
    coupling = 0.7
    operator = reciprocal_memory_operator(
        forward,
        forgetting_factor=q,
        coupling=coupling,
    )
    expected = reciprocal_memory_spectrum(
        forward,
        forgetting_factor=q,
        coupling=coupling,
    )
    numerical = np.linalg.eigvals(operator)
    analytical = np.array(
        [value for mode in expected.modes for value in mode.eigenvalues]
    )
    np.testing.assert_allclose(
        np.sort_complex(numerical), np.sort_complex(analytical), atol=1e-12
    )


def test_complex_window_has_modulus_sqrt_q() -> None:
    q = 0.99
    lower = (1.0 - np.sqrt(q)) ** 2
    upper = (1.0 + np.sqrt(q)) ** 2
    dimensionless = np.sqrt(lower * upper)
    spectrum = reciprocal_memory_spectrum(
        np.array([[np.sqrt(dimensionless)]]),
        forgetting_factor=q,
        coupling=1.0,
    )
    [mode] = spectrum.modes
    assert mode.classification == "damped_rotation"
    assert mode.stable
    np.testing.assert_allclose(np.abs(mode.eigenvalues), np.sqrt(q))


def test_direction_jacobian_is_longitudinal_null_and_transverse_degenerate() -> None:
    displacement = np.array([3.0, -4.0, 0.0])
    direction = displacement / np.linalg.norm(displacement)
    jacobian = normalized_direction_jacobian(displacement, relaxation=0.2)
    np.testing.assert_allclose(jacobian @ direction, 0.0, atol=1e-16)
    np.testing.assert_allclose(
        np.linalg.eigvalsh(jacobian), [0.0, 0.04, 0.04], atol=1e-16
    )


def test_direction_jacobian_is_orthogonally_covariant() -> None:
    displacement = np.array([0.3, -0.2, 0.7])
    rotation, _ = np.linalg.qr(
        np.array([[1.0, 2.0, 0.4], [-0.2, 0.8, 1.1], [0.7, -0.3, 0.5]])
    )
    original = normalized_direction_jacobian(displacement, relaxation=0.1)
    transformed = normalized_direction_jacobian(
        rotation @ displacement, relaxation=0.1
    )
    np.testing.assert_allclose(transformed, rotation @ original @ rotation.T)


def test_memory_metric_normalization_changes_mode_classification() -> None:
    forward = np.array([[1.0]])
    q = 0.99
    gain = 1e-3
    small = reciprocal_memory_spectrum(
        forward,
        forgetting_factor=q,
        coupling=gain,
        memory_metric=np.array([[1e-3]]),
    )
    large = reciprocal_memory_spectrum(
        forward,
        forgetting_factor=q,
        coupling=gain,
        memory_metric=np.array([[1e4]]),
    )
    assert small.modes[0].classification == "overdamped"
    assert large.modes[0].classification == "flip_unstable"


@pytest.mark.parametrize("displacement", [np.zeros(2), np.array([np.nan, 1.0])])
def test_direction_jacobian_rejects_undefined_steps(displacement: np.ndarray) -> None:
    with pytest.raises(ValueError):
        normalized_direction_jacobian(displacement, relaxation=0.1)
