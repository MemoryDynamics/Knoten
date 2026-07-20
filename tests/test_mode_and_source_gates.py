from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]


def _load_script(name: str, relative_path: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative_path)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


mode_audit = _load_script(
    "low_mode_identity_audit",
    "experiments/current/memory/low_mode_identity_audit.py",
)
source_pilot = _load_script(
    "one_way_dynamic_source_pilot",
    "experiments/current/memory/synchronization/one_way_dynamic_source_pilot.py",
)


def _mode_row(
    arm: str,
    kind: str,
    lag: float,
    *,
    match_fraction: float = 1.0,
    rate_mad: float = 0.1,
    frequency_mad: float = 0.1,
    quality: float = 1.0,
    vector: np.ndarray | None = None,
) -> dict:
    values = np.array([1.0, 1.0j]) if vector is None else np.asarray(vector)
    return {
        "arm": arm,
        "kind": kind,
        "lag_memory_times": lag,
        "reference_present": True,
        "reference_vector": {
            "real": values.real.tolist(),
            "imag": values.imag.tolist(),
        },
        "match_fraction": match_fraction,
        "overlap_median": 1.0,
        "rate_relative_mad": rate_mad,
        "frequency_relative_mad": frequency_mad,
        "quality_factor_median": quality,
    }


def test_mode_gate_rejects_control_aligned_complex_subspace() -> None:
    rows = []
    for lag in (0.2, 1.0):
        rows.append(_mode_row("active_nu03", "real", lag))
        rows.append(_mode_row("active_nu03", "complex", lag))
        rows.append(_mode_row("eta_zero_nu03", "complex", lag))

    gate = mode_audit._gate_summary(rows)

    assert gate["real_mode_identity_pass"]
    assert gate["complex_segment_identity_pass"]
    assert not gate["complex_control_separation_pass"]
    assert not gate["oscillatory_mode_supported"]


def test_source_gate_rejects_unbounded_subthreshold_launch() -> None:
    orbital = {
        "angular_orientation_coherence": 0.8,
        "tangential_fraction_median": 0.9,
        "dephasing_memory_times": 20.0,
    }
    free = {
        "angular_orientation_coherence": 0.1,
        "tangential_fraction_median": 0.8,
        "dephasing_memory_times": 0.2,
    }
    rows = [
        {
            "source_launch_sigma_rep": 0.1,
            "dynamic_minus_frozen_final_radii": 0.2,
            "launch_specific_source_displacement_radii": 10.0,
            "launch_specific_target_response_radii": 1e-3,
            "source_stationarity": {
                "stationary_shape_pass": True,
                "radius_relative_drift": 0.01,
                "shape_spectrum_total_variation": 0.01,
            },
            "source_shape_response": {
                "shape_bounded_pass": False,
                "shape_coherent_pass": True,
                "max_radius_factor": 2.1,
                "shape_spectrum_distance_median": 0.01,
            },
            "target_shape_response": {
                "shape_bounded_pass": True,
                "shape_coherent_pass": True,
            },
            "orbital_metrics": {
                "dynamic_source": orbital,
                "free": free,
            },
        }
        for _ in range(3)
    ]

    gate = source_pilot._gate(rows, null_error=0.0)

    assert gate["dynamic_source_readout_pass"]
    assert not gate["launch_specific_target_readout_pass"]
    assert gate["stationary_source_shape_pass"]
    assert gate["target_shape_bounded_coherent_pass"]
    assert not gate["source_shape_bounded_coherent_pass"]
    assert not gate["relational_phase_candidate_pass"]
