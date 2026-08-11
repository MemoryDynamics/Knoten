from __future__ import annotations

import numpy as np
import pytest

from emergenz_knoten.continuity_memory import (
    continuity_memory_mode,
    continuity_memory_mode_operator,
    continuity_oscillation_threshold,
    memory_innovation_moments,
)


def test_stationary_memory_innovation_has_zero_monopole_and_canonical_dipole() -> None:
    result = memory_innovation_moments(
        memory_relaxation=0.1,
        target_mass=2.0,
        current_mass=2.0,
        current_centroid=np.array([1.0, -2.0]),
        deposited_position=np.array([4.0, 3.0]),
    )
    assert result.monopole == pytest.approx(0.0)
    np.testing.assert_allclose(result.first_moment, [0.6, 1.0])


def test_truncated_mass_residual_is_explicit_not_silently_normalized() -> None:
    result = memory_innovation_moments(
        memory_relaxation=0.01,
        target_mass=1.0,
        current_mass=0.997,
        current_centroid=np.zeros(1),
        deposited_position=np.ones(1),
    )
    assert result.monopole == pytest.approx(3.0e-5)


@pytest.mark.parametrize("wavenumber", [0.0, 0.2, 1.0, 3.0])
def test_mode_formula_matches_numerical_operator(wavenumber: float) -> None:
    kwargs = {
        "memory_relaxation": 0.1,
        "flux_relaxation": 0.3,
        "stiffness": 2.0,
    }
    mode = continuity_memory_mode(wavenumber, **kwargs)
    numerical = np.sort_complex(
        np.linalg.eigvals(continuity_memory_mode_operator(wavenumber, **kwargs))
    )
    np.testing.assert_allclose(np.sort_complex(mode.eigenvalues), numerical)


def test_continuity_mode_crosses_exact_oscillation_threshold() -> None:
    kwargs = {
        "memory_relaxation": 0.1,
        "flux_relaxation": 0.5,
        "stiffness": 4.0,
    }
    threshold = continuity_oscillation_threshold(**kwargs)
    assert threshold == pytest.approx(0.1)
    assert not continuity_memory_mode(0.99 * threshold, **kwargs).oscillatory
    above = continuity_memory_mode(1.01 * threshold, **kwargs)
    assert above.oscillatory
    assert above.asymptotically_stable


def test_zero_stiffness_is_first_order_negative_control() -> None:
    kwargs = {
        "memory_relaxation": 0.1,
        "flux_relaxation": 0.5,
        "stiffness": 0.0,
    }
    assert np.isinf(continuity_oscillation_threshold(**kwargs))
    mode = continuity_memory_mode(10.0, **kwargs)
    assert mode.classification == "stable_real"
    np.testing.assert_allclose(np.sort_complex(mode.eigenvalues), [-0.5, -0.1])


def test_negative_stiffness_exposes_instability() -> None:
    mode = continuity_memory_mode(
        1.0,
        memory_relaxation=0.1,
        flux_relaxation=0.2,
        stiffness=-1.0,
    )
    assert mode.classification == "unstable"


@pytest.mark.parametrize(
    ("argument", "value"),
    [("memory_relaxation", -0.1), ("flux_relaxation", -0.1)],
)
def test_invalid_relaxation_is_rejected(argument: str, value: float) -> None:
    kwargs = {
        "memory_relaxation": 0.1,
        "flux_relaxation": 0.2,
        "stiffness": 1.0,
    }
    kwargs[argument] = value
    with pytest.raises(ValueError):
        continuity_memory_mode(1.0, **kwargs)
