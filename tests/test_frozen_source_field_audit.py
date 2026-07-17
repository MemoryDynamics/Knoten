from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

import numpy as np

from emergenz_knoten import FiniteMemoryState, SimulationConfig, memory_shape_tensor


SCRIPT_PATH = (
    Path(__file__).resolve().parents[1]
    / "experiments"
    / "current"
    / "memory"
    / "synchronization"
    / "frozen_source_field_audit.py"
)
SPEC = importlib.util.spec_from_file_location("frozen_source_field_audit", SCRIPT_PATH)
field_audit = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = field_audit
SPEC.loader.exec_module(field_audit)


def _state() -> FiniteMemoryState:
    return FiniteMemoryState(
        x=np.zeros(2),
        memory=np.array(
            [
                [0.01, 0.0],
                [-0.01, 0.0],
                [0.0, 0.01],
                [0.0, -0.01],
            ]
        ),
        weights=np.full(4, 0.25),
    )


def _config() -> SimulationConfig:
    return SimulationConfig(
        steps=100,
        dim=2,
        epsilon=1e-4,
        eta=0.15,
        alpha=0.01,
        memory_mass=1.0,
        deposition_kernel="delta",
        deposition_sigma=0.0,
        sigma_rep=1.0,
        sigma_att=3.0,
        amplitude_rep=1.0,
        amplitude_att=35.0,
        memory_factor=6.0,
        max_memory=600,
        burn_in=0,
        sample_every=1,
    )


def _case(tmp_path: Path) -> field_audit.FieldCase:
    state = _state()
    radius = float(np.sqrt(np.trace(memory_shape_tensor(state))))
    return field_audit.FieldCase(
        path=tmp_path / "state.npz",
        seed=1,
        update_index=100,
        formation_revision="abc123",
        config=_config(),
        state=state,
        center=np.zeros(2),
        radius=radius,
        stored_mass=1.0,
    )


def test_paired_direction_set_contains_exact_parity_partners() -> None:
    directions = field_audit.paired_direction_set(
        _state(),
        random_pairs=3,
        seed=17,
    )

    assert directions.shape == (10, 2)
    np.testing.assert_allclose(np.linalg.norm(directions, axis=1), 1.0)
    np.testing.assert_array_equal(directions[5:], -directions[:5])


def test_symmetric_attractive_source_has_no_crossing_or_odd_field(
    tmp_path: Path,
) -> None:
    result = field_audit.evaluate_field_case(
        _case(tmp_path),
        radial_points=30,
        random_direction_pairs=4,
        direction_seed=17,
    )

    assert result["potential_curvature_at_origin"] > 0.0
    assert result["analytic_point_force_crossing"] is None
    assert result["measured_mean_force_crossings"] == []
    assert np.all(np.asarray(result["point_radial_force"]) < 0.0)
    assert np.all(np.asarray(result["radial_force_max"]) < 0.0)
    assert np.max(result["potential_parity_odd_fraction"]) < 1e-12
    far = np.asarray(result["radii_over_sigma_rep"]) >= 1.0
    assert np.max(np.asarray(result["monopole_force_relative_error"])[far]) < 1e-3


def test_report_separates_scalar_sign_from_charge_claim(tmp_path: Path) -> None:
    result = field_audit.evaluate_field_case(
        _case(tmp_path),
        radial_points=20,
        random_direction_pairs=2,
        direction_seed=17,
    )
    payload = {
        "generated_utc": "2026-07-17T00:00:00Z",
        "git_revision": "abc123",
        "command": ["python", "frozen_source_field_audit.py"],
        "summary_json": tmp_path / "summary.json",
        "case_results": [result],
        "landmark_rows": field_audit.landmark_rows([result]),
    }

    report = field_audit.build_report(
        payload,
        report_path=tmp_path / "report.md",
        figure_paths=(
            tmp_path / "potential.png",
            tmp_path / "force.png",
            tmp_path / "structure.png",
        ),
    )

    assert "no knot-specific charge sign" in report
    assert "signed scalar channel" in report
    assert "not evidence for reciprocal" in report
    assert "dimensionless distance ladder" not in report
    assert "5, 20, and 100 memory radii" in report
