from __future__ import annotations

import numpy as np
import pytest

from emergenz_knoten.stability import (
    checkpoint_stability_diagnostics,
    local_radius_stationarity_diagnostics,
    local_shape_stationarity_diagnostics,
    normalized_shape_eigenvalues,
)


def test_normalized_shape_eigenvalues_preserves_simplex_rows() -> None:
    spectra = normalized_shape_eigenvalues([[3.0, 1.0], [2.0, 2.0]])

    np.testing.assert_allclose(spectra.sum(axis=1), 1.0)
    np.testing.assert_allclose(spectra[0], [0.75, 0.25])


def test_checkpoint_gate_accepts_bounded_rotation_invariant_shape() -> None:
    updates = np.array([1e6, 3e6, 1e7, 3e7, 3e8])
    radii = np.array([1.00, 1.01, 0.99, 1.02, 1.01])
    eigenvalues = np.array(
        [
            [0.70, 0.20, 0.10],
            [0.69, 0.21, 0.10],
            [0.71, 0.19, 0.10],
            [0.70, 0.19, 0.11],
            [0.69, 0.20, 0.11],
        ]
    )

    result = checkpoint_stability_diagnostics(updates, radii, eigenvalues)

    assert result["checkpoint_stability_pass"]
    assert result["candidate_update"] == 30_000_000
    assert result["holdout_update"] == 300_000_000


def test_checkpoint_gate_rejects_slow_monotone_radius_trend() -> None:
    updates = np.array([1e6, 3e6, 1e7, 3e7, 3e8])
    radii = np.power(updates / updates[0], 0.08)
    eigenvalues = np.repeat([[0.7, 0.2, 0.1]], len(updates), axis=0)

    result = checkpoint_stability_diagnostics(updates, radii, eigenvalues)

    assert not result["training_radius_trend_pass"]
    assert not result["checkpoint_stability_pass"]


def test_checkpoint_gate_rejects_holdout_shape_change() -> None:
    updates = np.array([1e6, 3e6, 1e7, 3e7, 3e8])
    radii = np.ones(len(updates))
    eigenvalues = np.array(
        [
            [0.7, 0.2, 0.1],
            [0.7, 0.2, 0.1],
            [0.7, 0.2, 0.1],
            [0.7, 0.2, 0.1],
            [0.34, 0.33, 0.33],
        ]
    )

    result = checkpoint_stability_diagnostics(updates, radii, eigenvalues)

    assert not result["holdout_shape_pass"]
    assert not result["checkpoint_stability_pass"]


def test_local_radius_gate_uses_four_windows_plus_holdout() -> None:
    updates = np.arange(1, 501)
    radii = 1.0 + 0.01 * np.sin(updates / 7.0)

    result = local_radius_stationarity_diagnostics(
        updates,
        radii,
        window_updates=100,
    )

    assert result["local_radius_stationarity_pass"]
    assert result["window_sample_counts"] == [100] * 5


def test_local_radius_gate_rejects_drifting_holdout() -> None:
    updates = np.arange(1, 501)
    radii = np.ones(500)
    radii[-100:] = 1.3

    result = local_radius_stationarity_diagnostics(
        updates,
        radii,
        window_updates=100,
    )

    assert not result["holdout_radius_pass"]
    assert not result["local_radius_stationarity_pass"]


def test_checkpoint_gate_rejects_nonseparated_holdout() -> None:
    updates = np.array([1e6, 3e6, 1e7, 3e7, 6e7])
    radii = np.ones(len(updates))
    eigenvalues = np.repeat([[0.7, 0.2, 0.1]], len(updates), axis=0)

    result = checkpoint_stability_diagnostics(updates, radii, eigenvalues)

    assert not result["holdout_separation_pass"]


def test_local_radius_gate_requires_complete_windows() -> None:
    with pytest.raises(ValueError, match="enough radius samples"):
        local_radius_stationarity_diagnostics(
            np.arange(201, 301),
            np.ones(100),
            window_updates=30,
            minimum_samples_per_window=20,
        )


def test_local_radius_stationarity_allows_early_zero_radius() -> None:
    updates = np.arange(1, 122, dtype=float)
    radii = np.ones_like(updates)
    radii[:20] = 0.0

    result = local_radius_stationarity_diagnostics(
        updates,
        radii,
        window_updates=20,
        minimum_samples_per_window=20,
    )

    assert result["local_radius_stationarity_pass"] is True


def test_local_shape_stationarity_passes_bounded_spectra() -> None:
    updates = np.arange(1, 501)
    phase = np.sin(updates / 13.0)
    spectra = np.column_stack(
        [0.70 + 0.01 * phase, 0.20 - 0.005 * phase, 0.10 - 0.005 * phase]
    )

    result = local_shape_stationarity_diagnostics(
        updates,
        spectra,
        window_updates=100,
    )

    assert result["local_shape_stationarity_pass"] is True
    assert result["window_sample_counts"] == [100] * 5


def test_local_shape_stationarity_rejects_holdout_change() -> None:
    updates = np.arange(1, 501)
    spectra = np.repeat([[0.70, 0.20, 0.10]], 500, axis=0)
    spectra[-100:] = [0.34, 0.33, 0.33]

    result = local_shape_stationarity_diagnostics(
        updates,
        spectra,
        window_updates=100,
    )

    assert result["holdout_shape_pass"] is False
    assert result["local_shape_stationarity_pass"] is False
