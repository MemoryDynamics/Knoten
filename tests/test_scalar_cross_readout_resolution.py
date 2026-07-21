from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

import numpy as np
import pytest

from emergenz_knoten import FiniteMemoryState, SimulationConfig, memory_shape_tensor


SCRIPT_PATH = (
    Path(__file__).resolve().parents[1]
    / "experiments"
    / "current"
    / "memory"
    / "synchronization"
    / "scalar_cross_readout_resolution.py"
)
SPEC = importlib.util.spec_from_file_location(
    "scalar_cross_readout_resolution", SCRIPT_PATH
)
resolution = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = resolution
SPEC.loader.exec_module(resolution)


def _config() -> SimulationConfig:
    return SimulationConfig(
        steps=100,
        dim=2,
        epsilon=1e-4,
        eta=0.15,
        alpha=0.1,
        memory_mass=1.0,
        deposition_kernel="delta",
        deposition_sigma=0.0,
        sigma_rep=1.0,
        sigma_att=3.0,
        amplitude_rep=1.0,
        amplitude_att=35.0,
        memory_factor=4.0,
        max_memory=40,
        burn_in=0,
        sample_every=1,
    )


def _isotropic_state() -> FiniteMemoryState:
    return FiniteMemoryState(
        x=np.zeros(2),
        memory=np.array([[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]]),
        weights=np.full(4, 0.25),
    )


def _anisotropic_state() -> FiniteMemoryState:
    return FiniteMemoryState(
        x=np.zeros(2),
        memory=np.array([[-1.0, 0.0], [-0.3, 0.0], [0.3, 0.0], [1.0, 0.0]]),
        weights=np.full(4, 0.25),
    )


def test_resolution_ratio_parser_is_explicit_and_unique() -> None:
    assert resolution.parse_resolution_ratios("3,100,10") == [100.0, 10.0, 3.0]
    with pytest.raises(ValueError, match="duplicates"):
        resolution.parse_resolution_ratios("3,3")


def test_gate_classification_requires_consistent_embeddings() -> None:
    negative = [{"shape_onset_ratio": None}, {"shape_onset_ratio": None}]
    positive = [{"shape_onset_ratio": 3.0}, {"shape_onset_ratio": 2.5}]
    mixed = [{"shape_onset_ratio": 3.0}, {"shape_onset_ratio": None}]

    assert resolution.classify_resolution_gate(negative)["status"] == "fail"
    assert (
        resolution.classify_resolution_gate(negative)["selected_next_mechanism"]
        == "oriented_memory_or_current"
    )
    assert resolution.classify_resolution_gate(positive)["status"] == "pass"
    assert resolution.classify_resolution_gate(mixed)["status"] == "inconclusive"


def test_principal_rotations_align_each_axis_with_radial_axis() -> None:
    state = _anisotropic_state()
    _, eigenvectors = np.linalg.eigh(memory_shape_tensor(state))
    _, rotations = resolution.principal_axis_rotations(state)

    for selected, rotation in enumerate(rotations):
        np.testing.assert_allclose(rotation.T @ rotation, np.eye(2), atol=1e-14)
        np.testing.assert_allclose(rotation @ eigenvectors[:, selected], [1.0, 0.0])


def test_isotropic_source_has_no_principal_orientation_signal() -> None:
    row = resolution.evaluate_readout_resolution(
        _isotropic_state(),
        _config(),
        radius_ratio=3.0,
        response_fraction=0.03,
        shape_threshold=0.01,
        minimum_distinctness=1.0,
    )

    assert row["orientation_spread"] < 1e-14
    assert row["shape_resolved"] is False
    assert row["reconstructed_response_fraction"] == pytest.approx(0.03)


def test_narrow_readout_resolves_anisotropy_more_than_broad_readout() -> None:
    kwargs = {
        "response_fraction": 0.03,
        "shape_threshold": 0.001,
        "minimum_distinctness": 1.0,
    }
    broad = resolution.evaluate_readout_resolution(
        _anisotropic_state(), _config(), radius_ratio=100.0, **kwargs
    )
    narrow = resolution.evaluate_readout_resolution(
        _anisotropic_state(), _config(), radius_ratio=3.0, **kwargs
    )

    assert narrow["orientation_spread"] > 100.0 * broad["orientation_spread"]
    assert narrow["shape_resolved"] is True
    assert broad["shape_resolved"] is False
