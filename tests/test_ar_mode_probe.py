from __future__ import annotations

import sys
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from experiments.ar_mode_probe import classify_eigenvalues, fit_ar_map


def test_fit_ar_map_recovers_damped_rotation_modes() -> None:
    theta = 0.25
    radius = 0.92
    transition = radius * np.array(
        [
            [np.cos(theta), -np.sin(theta)],
            [np.sin(theta), np.cos(theta)],
        ]
    )
    values = [np.array([1.0, 0.0])]
    for _ in range(200):
        values.append(values[-1] @ transition)
    series = [np.asarray(values)]

    fit = fit_ar_map(series, lag=1, lag_updates=1, ridge=1e-10)

    assert fit.n_pairs == 200
    assert classify_eigenvalues(fit.eigenvalues) == "complex"
    assert np.isclose(abs(fit.eigenvalues[0]), radius, atol=1e-3)


def test_classify_eigenvalues_detects_negative_real_mode() -> None:
    assert classify_eigenvalues([-0.8, 0.2]) == "negative-real"
