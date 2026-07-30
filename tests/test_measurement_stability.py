from __future__ import annotations

import numpy as np

from emergenz_knoten.measurement_stability import (
    occupancy_measurement_convergence_diagnostics,
)


UPDATES = np.array([1e6, 3e6, 1e7, 3e7, 3e8])


def test_occupancy_measurement_gate_passes_stable_protocol() -> None:
    result = occupancy_measurement_convergence_diagnostics(
        UPDATES,
        [1.80, 1.82, 1.84, 1.83, 1.85],
        [True] * 5,
        [1000] * 5,
        ["v1"] * 5,
    )

    assert result["measurement_convergence_evaluable"] is True
    assert result["occupancy_measurement_convergence_pass"] is True


def test_occupancy_measurement_gate_rejects_slow_growth() -> None:
    result = occupancy_measurement_convergence_diagnostics(
        UPDATES,
        [1.2, 1.4, 1.6, 1.9, 2.2],
        [True] * 5,
        [1000] * 5,
        ["v1"] * 5,
    )

    assert result["training_dimension_range_pass"] is False
    assert result["training_dimension_trend_pass"] is False
    assert result["occupancy_measurement_convergence_pass"] is False


def test_occupancy_measurement_gate_is_not_evaluable_after_cadence_change() -> None:
    result = occupancy_measurement_convergence_diagnostics(
        UPDATES,
        [1.8, 1.82, 1.84, 1.83, 1.85],
        [True] * 5,
        [1000, 1000, 1000, 1000, 10000],
        ["v1"] * 5,
    )

    assert result["sampling_cadence_pass"] is False
    assert result["measurement_convergence_evaluable"] is False
    assert result["occupancy_measurement_convergence_pass"] is False


def test_occupancy_measurement_gate_is_not_evaluable_with_invalid_fit() -> None:
    result = occupancy_measurement_convergence_diagnostics(
        UPDATES,
        [1.8, np.nan, 1.84, 1.83, 1.85],
        [True, False, True, True, True],
        [1000] * 5,
        ["v1"] * 5,
    )

    assert result["fit_validity_pass"] is False
    assert result["training_dimension_range_pass"] is False
    assert result["measurement_convergence_evaluable"] is False


def test_occupancy_measurement_gate_requires_same_estimator() -> None:
    result = occupancy_measurement_convergence_diagnostics(
        UPDATES,
        [1.8, 1.82, 1.84, 1.83, 1.85],
        [True] * 5,
        [1000] * 5,
        ["v1", "v1", "v1", "v1", "v2"],
    )

    assert result["estimator_identity_pass"] is False
    assert result["measurement_convergence_evaluable"] is False
