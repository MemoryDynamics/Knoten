import numpy as np
import pytest

import emergenz_knoten.rotating_wave_horizon_stability as horizon_stability
from emergenz_knoten.rotating_wave_stability import circular_history
from emergenz_knoten.rotating_wave_stability_gate import (
    ArnoldiPanel,
    RotatingWaveCandidate,
    StabilityThresholds,
)


THRESHOLDS = StabilityThresholds(
    eigen_residual=1e-8,
    symmetry_overlap=0.99,
    symmetry_eigenvalue=1e-7,
    leading_complex_agreement=1e-5,
    leading_modulus_agreement=1e-6,
    unstable_modulus=1.0 + 1e-6,
    stable_modulus=1.0 - 1e-4,
    perturbation_scale_fraction=1e-7,
    continuation_steps=5000,
    sample_every=10,
    stopping_radius_fraction=0.25,
    unstable_growth_minimum=100.0,
    stable_transient_growth_maximum=10.0,
    stable_final_ratio_maximum=0.1,
    exact_control_distance_maximum=1e-10,
)


def _candidate() -> RotatingWaveCandidate:
    return RotatingWaveCandidate(
        candidate_id="synthetic",
        radius=0.9,
        theta=0.03,
        alpha=0.1,
        horizon=3,
        memory_mass=1.0,
        eta=0.15,
        sigma_rep=1.0,
        sigma_att=3.0,
        amplitude_rep=1.0,
        amplitude_att=3.5,
    )


def _panel() -> ArnoldiPanel:
    return ArnoldiPanel("synthetic", 2, 4, 1e-10, 20, "external")


def test_explicit_start_reaches_solver_unchanged_and_vectors_are_recorded(
    monkeypatch,
) -> None:
    history = circular_history(radius=0.9, theta=0.03, horizon=3)
    explicit = np.asarray([1.0, -2.0, 3.0, -4.0, 5.0, -6.0])
    captured = {}

    def fake_eigs(jacobian, **kwargs):
        captured["start"] = kwargs["v0"].copy()
        return np.asarray([1.0 + 0.0j, 0.9 + 0.1j]), np.eye(6, 2, dtype=complex)

    monkeypatch.setattr(horizon_stability, "eigs", fake_eigs)
    result = horizon_stability.run_lcg_eigen_panel(
        np.eye(6),
        history,
        _candidate(),
        _panel(),
        THRESHOLDS,
        explicit_start=explicit,
    )

    np.testing.assert_array_equal(captured["start"], explicit)
    assert len(result["eigenpairs"]) == 2
    assert len(result["eigenpairs"][0]["vector"]) == 6
    assert result["eigenpairs"][0]["vector"][0] == [1.0, 0.0]


@pytest.mark.parametrize(
    "start",
    (
        np.ones(5),
        np.asarray([1.0, 1.0, 1.0, 1.0, 1.0, np.nan]),
        np.zeros(6),
        np.ones(6, dtype=complex),
    ),
)
def test_explicit_start_rejects_invalid_vectors(start) -> None:
    history = circular_history(radius=0.9, theta=0.03, horizon=3)

    with pytest.raises(ValueError, match="explicit Arnoldi start"):
        horizon_stability.run_lcg_eigen_panel(
            np.eye(6),
            history,
            _candidate(),
            _panel(),
            THRESHOLDS,
            explicit_start=start,
        )
