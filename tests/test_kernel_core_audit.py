from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments" / "current" / "kernels"))
sys.path.insert(0, str(ROOT / "src"))

import kernel_core_audit as audit  # noqa: E402


def _args() -> argparse.Namespace:
    return argparse.Namespace(
        sigma_rep=1.0,
        sigma_att=3.0,
        amplitude_rep=1.0,
        amplitude_att=35.0,
    )


def test_attractive_only_kernel_matches_current_curvature() -> None:
    current, attractive_only = audit.build_specs(_args())

    assert current.curvature == pytest.approx(26.0 / 9.0)
    assert attractive_only.amplitude_rep == 0.0
    assert attractive_only.amplitude_att == pytest.approx(26.0)
    assert attractive_only.curvature == pytest.approx(current.curvature)


def test_current_kernel_has_no_repulsive_near_origin_force() -> None:
    current, _ = audit.build_specs(_args())
    profile = audit.radial_components(np.array([1.0e-8, 1.0e-4]), current)
    assert np.all(profile["force_over_radius_rep"] > 0.0)
    assert np.all(profile["force_over_radius_att"] < 0.0)
    assert np.all(profile["force_over_radius"] < 0.0)
    assert np.all(profile["restoring_stiffness"] > 0.0)
