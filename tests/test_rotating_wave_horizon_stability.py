import numpy as np
import pytest
from scipy.sparse import csr_matrix

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


def _preflight_jacobian() -> csr_matrix:
    dense = np.zeros((6, 6))
    dense.ravel()[:20] = np.arange(1.0, 21.0)
    return csr_matrix(dense)


def _patch_preflight_dependencies(monkeypatch, *, fixed_drift: float = 0.0) -> None:
    monkeypatch.setattr(
        horizon_stability,
        "native_fifo_step",
        lambda history, **kwargs: history
        @ horizon_stability.rotation_matrix(_candidate().theta).T,
    )
    monkeypatch.setattr(
        horizon_stability,
        "co_rotating_fifo_step",
        lambda history, **kwargs: history + fixed_drift,
    )
    monkeypatch.setattr(
        horizon_stability,
        "co_rotating_fifo_jacobian",
        lambda history, **kwargs: _preflight_jacobian(),
    )
    monkeypatch.setattr(
        horizon_stability,
        "analytic_symmetry_checks",
        lambda *args, **kwargs: {
            "pass": True,
            "rotation_relative_residual": 1e-15,
            "translation_x_relative_residual": 2e-15,
            "translation_y_relative_residual": 3e-15,
        },
    )


def test_full_fifo_preflight_binds_ground_equation_and_structure(monkeypatch) -> None:
    _patch_preflight_dependencies(monkeypatch)

    prepared = horizon_stability.build_full_fifo_preflight(
        _candidate(),
        fixed_point_maximum=1e-14,
        symmetry_residual_maximum=1e-10,
    )
    record = prepared.record

    assert record["schema"] == horizon_stability.PREFLIGHT_SCHEMA
    assert record["equation"]["equation_id"] == horizon_stability.EQUATION_ID
    assert record["equation"]["noise_amplitude"] == 0.0
    assert record["equation"]["q"] == 0.9
    assert record["equation"]["deposition_weight"] == 0.1
    assert record["jacobian"]["shape"] == [6, 6]
    assert record["jacobian"]["nnz"] == 20
    assert record["gates"]["pass"] is True
    assert len(record["orbit"]["history_sha256"]) == 64
    assert len(record["jacobian"]["sha256"]) == 64
    assert len(horizon_stability.preflight_sha256(record)) == 64


def test_full_fifo_preflight_fails_closed_on_direct_map_drift(monkeypatch) -> None:
    _patch_preflight_dependencies(monkeypatch, fixed_drift=2e-14)

    with pytest.raises(ArithmeticError, match="fixed_point"):
        horizon_stability.build_full_fifo_preflight(
            _candidate(),
            fixed_point_maximum=1e-14,
            symmetry_residual_maximum=1e-10,
        )


@pytest.mark.parametrize(
    ("mutation", "failed_gate"),
    (
        ("native-circle", "native_circle_covariance"),
        ("weight-sum", "weight_identity"),
        ("jacobian", "jacobian_structure"),
        ("symmetry", "symmetries"),
    ),
)
def test_full_fifo_preflight_rejects_ground_equation_mutations(
    monkeypatch, mutation: str, failed_gate: str
) -> None:
    _patch_preflight_dependencies(monkeypatch)
    if mutation == "native-circle":
        monkeypatch.setattr(
            horizon_stability,
            "native_fifo_step",
            lambda history, **kwargs: history
            @ horizon_stability.rotation_matrix(_candidate().theta).T
            + 2e-14,
        )
    elif mutation == "weight-sum":
        monkeypatch.setattr(
            horizon_stability,
            "finite_memory_weights",
            lambda **kwargs: np.zeros(3),
        )
    elif mutation == "jacobian":
        monkeypatch.setattr(
            horizon_stability,
            "co_rotating_fifo_jacobian",
            lambda history, **kwargs: csr_matrix(np.eye(6)),
        )
    else:
        monkeypatch.setattr(
            horizon_stability,
            "analytic_symmetry_checks",
            lambda *args, **kwargs: {
                "pass": False,
                "rotation_relative_residual": 2e-10,
                "translation_x_relative_residual": 2e-10,
                "translation_y_relative_residual": 2e-10,
            },
        )

    with pytest.raises(ArithmeticError, match=failed_gate):
        horizon_stability.build_full_fifo_preflight(
            _candidate(),
            fixed_point_maximum=1e-14,
            symmetry_residual_maximum=1e-10,
        )


@pytest.mark.parametrize(
    ("fixed_threshold", "symmetry_threshold"),
    ((-1.0, 1e-10), (1e-14, float("nan"))),
)
def test_full_fifo_preflight_rejects_invalid_thresholds(
    fixed_threshold: float, symmetry_threshold: float
) -> None:
    with pytest.raises(ValueError, match="threshold"):
        horizon_stability.build_full_fifo_preflight(
            _candidate(),
            fixed_point_maximum=fixed_threshold,
            symmetry_residual_maximum=symmetry_threshold,
        )


def test_preflight_hash_is_independent_of_dictionary_insertion_order() -> None:
    first = {"schema": "v1", "nested": {"b": 2, "a": 1}}
    second = {"nested": {"a": 1, "b": 2}, "schema": "v1"}

    assert horizon_stability.preflight_sha256(
        first
    ) == horizon_stability.preflight_sha256(second)


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


def test_projection_overlap_canonicalizes_only_binary64_boundary_drift() -> None:
    epsilon = np.finfo(np.float64).eps

    assert horizon_stability._canonical_projection_overlap(
        1.0 + epsilon, dimension=4800
    ) == 1.0
    assert horizon_stability._canonical_projection_overlap(
        -epsilon, dimension=4800
    ) == 0.0
    assert horizon_stability._canonical_projection_overlap(
        0.25, dimension=4800
    ) == 0.25


@pytest.mark.parametrize("overlap", (-1e-8, 1.0 + 1e-8, np.nan, np.inf))
def test_projection_overlap_rejects_non_roundoff_violations(overlap: float) -> None:
    with pytest.raises(ArithmeticError, match="projection bound"):
        horizon_stability._canonical_projection_overlap(overlap, dimension=4800)


def test_eigen_panel_serializes_roundoff_overlap_at_exact_boundary(monkeypatch) -> None:
    history = circular_history(radius=0.9, theta=0.03, horizon=3)
    translation = np.zeros((6, 2))
    translation[0, 0] = np.nextafter(1.0, 2.0)
    translation[1, 1] = 1.0
    rotation = np.zeros(6)
    rotation[2] = 1.0

    monkeypatch.setattr(
        horizon_stability,
        "symmetry_basis",
        lambda _history: (translation, rotation),
    )
    monkeypatch.setattr(
        horizon_stability,
        "eigs",
        lambda jacobian, **kwargs: (
            np.asarray([1.0 + 0.0j, 0.9 + 0.1j]),
            np.eye(6, 2, dtype=complex),
        ),
    )

    result = horizon_stability.run_lcg_eigen_panel(
        np.eye(6),
        history,
        _candidate(),
        _panel(),
        THRESHOLDS,
        explicit_start=np.ones(6),
    )

    assert result["eigenpairs"][0]["translation_overlap"] == 1.0


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
