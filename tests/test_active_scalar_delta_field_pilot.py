from __future__ import annotations

from dataclasses import replace
import importlib.util
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = (
    ROOT / "experiments" / "current" / "kernels" / "field" / "active_scalar_delta_field_pilot.py"
)
SPEC = importlib.util.spec_from_file_location(
    "active_scalar_delta_field_pilot",
    SCRIPT,
)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_case_builder_keeps_preregistered_controls_distinct() -> None:
    base = MODULE.ActiveScalarFieldConfig(grid_points=64, steps=20)
    cases = MODULE.build_cases(base)

    assert cases["gaussian_null"].gradient_coefficient == 0.5
    assert cases["stable_finite_k"].gradient_coefficient == -1.8
    assert cases["active_finite_k"].gradient_coefficient == -2.2
    assert cases["active_finite_k"].cubic_saturation > 0.0
    assert cases["cubic_off"].cubic_saturation == 0.0
    assert not cases["source_off"].source_enabled
    assert cases["eta_zero"].eta == 0.0


def test_low_mode_error_ignores_grid_only_modes() -> None:
    coarse_config = MODULE.ActiveScalarFieldConfig(
        grid_points=64,
        steps=1,
        eta=0.0,
        epsilon=0.0,
    )
    fine_config = replace(coarse_config, grid_points=128)
    coarse = MODULE.simulate_active_scalar_delta_field(coarse_config)
    fine = MODULE.simulate_active_scalar_delta_field(fine_config)

    assert np.isfinite(MODULE._shared_low_mode_error(fine, coarse))


def test_report_keeps_claims_bounded() -> None:
    payload = {
        "question": "test",
        "equation": "test equation",
        "representation": "test representation",
        "summary": {
            name: {
                "completed_count": 1,
                "run_count": 1,
                "late_field_rms_median": 1.0,
                "late_field_rms_relative_change_median": 0.0,
                "dominant_wavenumber_median": 1.0,
                "half_power_peak_width_median": 0.0,
                "source_late_excursion_median": 0.0,
            }
            for name in (
                "gaussian_null",
                "stable_finite_k",
                "active_finite_k",
                "cubic_off",
                "source_off",
                "eta_zero",
            )
        },
        "numerical_audit": {
            "time_step_low_mode_errors_vs_dt_0p025": {"0.05": 0.0},
            "grid_low_mode_errors_vs_n512": {"256": 0.0},
            "gaussian_stationary_relative_error": 0.0,
            "stable_finite_k_stationary_relative_error": 0.0,
            "active_steady_equation_relative_residual": 0.0,
        },
        "decisions": {
            "numerical_gate_pass": True,
            "active_amplitude_bounded_pass": True,
            "cubic_saturation_discriminates_pass": True,
            "source_off_null_pass": True,
            "finite_wavenumber_peak_pass": True,
            "late_visible_source_bounded_pass": True,
            "eta_zero_pattern_similarity_pass": True,
            "exploratory_feedback_phase_relocation": True,
            "classical_finite_wavenumber_mechanism_gate_pass": True,
        },
        "git_revision": "abc",
        "git_status": "",
    }

    report = MODULE.render_report(
        payload,
        generated="2026-07-31T00:00:00Z",
        figure_link="figure.png",
        json_link="summary.json",
    )

    assert "classical finite-k pattern" in report
    assert "finite-k pattern does not require visible trajectory" in report
    assert "about half a wavelength" in report
    assert "Not established: ambient 3D selection" in report
