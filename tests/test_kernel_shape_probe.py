from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

import numpy as np
import pytest


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "experiments" / "kernel_shape_probe.py"
SPEC = importlib.util.spec_from_file_location("kernel_shape_probe", SCRIPT_PATH)
assert SPEC is not None
kernel_shape_probe = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = kernel_shape_probe
assert SPEC.loader is not None
SPEC.loader.exec_module(kernel_shape_probe)


def test_turn_cosine_reports_straight_path() -> None:
    samples = np.array([[0.0, 0.0], [1.0, 0.0], [2.0, 0.0], [3.0, 0.0]])

    turn = kernel_shape_probe._turn_cosine(samples)

    assert turn["mean"] == pytest.approx(1.0)
    assert turn["median"] == pytest.approx(1.0)


def test_pca_projection_returns_three_columns() -> None:
    samples = np.array(
        [
            [0.0, 0.0, 0.0, 1.0],
            [1.0, 0.0, 0.0, 1.0],
            [2.0, 0.0, 0.0, 1.0],
            [3.0, 0.0, 0.0, 1.0],
        ]
    )

    coords, energy = kernel_shape_probe._pca_projection(samples)

    assert coords.shape == (4, 3)
    assert energy[0] == pytest.approx(1.0)
