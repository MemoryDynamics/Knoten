from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np
import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = (
    ROOT
    / "experiments"
    / "current"
    / "memory"
    / "synchronization"
    / "oriented_source_mediator_identifiability.py"
)
SPEC = importlib.util.spec_from_file_location(
    "oriented_source_mediator_identifiability", SCRIPT
)
assert SPEC is not None and SPEC.loader is not None
audit = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(audit)


def _thresholds() -> dict[str, float]:
    return {
        "orientation_rms_min": 1e-3,
        "source_radius_max_change": 0.5,
        "source_spectrum_max_drift": 0.25,
        "weighted_contrast_min": 0.25,
        "distinguishable_power_min": 0.2,
        "transmitted_power_min": 0.01,
        "segment_drift_max": 0.25,
    }


def _distance_row(**updates: float) -> dict[str, object]:
    persistent = {
        "pooled_weighted_contrast": 0.5,
        "pooled_distinguishable_power_fraction": 0.7,
        "pooled_transmitted_power_fraction": 0.4,
        "weighted_contrast_segment_drift": 0.1,
    }
    persistent.update(updates)
    return {"persistent": persistent}


def test_relative_segment_drift_uses_range_over_mean() -> None:
    assert audit.relative_segment_drift(np.array([1.0, 1.2])) == pytest.approx(
        0.2 / 1.1
    )
    assert audit.relative_segment_drift(np.zeros(2)) == 0.0


def test_pair_gate_requires_every_inherited_distance() -> None:
    rows = [_distance_row(), _distance_row(), _distance_row()]
    passing = audit.pair_gate(
        rows,
        orientation_rms=0.1,
        radius_change=0.1,
        spectrum_drift=0.1,
        thresholds=_thresholds(),
    )
    rows[-1] = _distance_row(pooled_weighted_contrast=0.1)
    failing = audit.pair_gate(
        rows,
        orientation_rms=0.1,
        radius_change=0.1,
        spectrum_drift=0.1,
        thresholds=_thresholds(),
    )

    assert all(passing.values())
    assert not failing["weighted_contrast"]


def test_transfer_normalization_removes_static_amplitude() -> None:
    values = np.column_stack(
        (
            np.array([1.0, 0.5, 0.25, 0.125]),
            7.0 * np.array([1.0, 0.5, 0.25, 0.125]),
        )
    )

    normalized = audit._dc_normalized_transfer(values)

    np.testing.assert_allclose(normalized[0], 1.0)
    np.testing.assert_allclose(normalized[:, 0], normalized[:, 1])


def test_report_keeps_field_selection_and_three_dimensional_claims_closed(
    tmp_path: Path,
) -> None:
    metrics = {
        "pooled_weighted_contrast": 0.5,
        "pooled_distinguishable_power_fraction": 0.7,
        "pooled_transmitted_power_fraction": 0.4,
        "weighted_contrast_segment_drift": 0.1,
    }
    payload = {
        "generated_utc": "2026-07-28T00:00:00+00:00",
        "decision": {
            "status": "source_eligible_mechanism_still_underdetermined",
            "passing_pairs": 1,
            "pair_count": 1,
            "persistent_to_one_step_contrast_min": 0.9,
            "persistent_to_one_step_contrast_median": 1.0,
            "persistent_to_one_step_contrast_max": 1.1,
            "interpretation": "Eligibility only.",
        },
        "burn_memory_times": 20.0,
        "segments": 2,
        "segment_updates": 8192,
        "thresholds": {
            "minimum_frequency_contrast": 0.25,
            **_thresholds(),
        },
        "minimum_passing_pairs": 1,
        "rows": [
            {
                "source_seed": 1,
                "orientation_rms": 0.1,
                "source_radius_max_change": 0.1,
                "source_spectrum_max_drift": 0.1,
                "pair_pass": True,
                "distances": [
                    {
                        "distance_ratio_pair_radius": 2.5,
                        "persistent": metrics,
                        "one_step": metrics,
                    }
                ],
            }
        ],
        "mediator_summary": "reports/mediator.json",
        "source_reference": "reports/source.json",
        "git_revision": "abc",
        "git_status_at_start": "",
        "command": ["python", "audit.py"],
    }

    report = audit.build_report(
        payload, tmp_path / "report.md", tmp_path / "figure.png"
    )

    assert "cannot select a physical field law" in report
    assert "Fields do not select three dimensions" in report
    assert "A 3D field grid would assume that result" in report
