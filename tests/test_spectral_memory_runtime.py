from __future__ import annotations

import math

import numpy as np

from emergenz_knoten.spectral_memory_field import (
    SpectralMemoryConfig,
    deposition_coefficients,
    potential_gradient,
    update_rho,
)
from emergenz_knoten.spectral_memory_runtime import SpectralMemoryOperators


def test_cached_operators_match_reference_functions() -> None:
    config = SpectralMemoryConfig(n_modes=16, deposition_sigma=0.2)
    operators = SpectralMemoryOperators(config)
    rho = deposition_coefficients(config, 13.0)

    np.testing.assert_allclose(
        operators.deposition(7.5),
        deposition_coefficients(config, 7.5),
    )
    np.testing.assert_allclose(
        operators.update_rho(rho, deposited_at=7.5),
        update_rho(config, rho, deposited_at=7.5),
    )
    assert math.isclose(
        operators.gradient(rho, x=14.0),
        potential_gradient(config, rho, x=14.0),
        rel_tol=2e-15,
        abs_tol=2e-15,
    )
    assert operators.state_bytes == 17 * np.dtype(np.complex128).itemsize
