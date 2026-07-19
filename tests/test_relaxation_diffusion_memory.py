from __future__ import annotations

import math

import numpy as np
import pytest

from emergenz_knoten.relaxation_diffusion_memory import (
    RelaxationDiffusionMemoryOperators,
)
from emergenz_knoten.spectral_memory_field import SpectralMemoryConfig
from emergenz_knoten.spectral_memory_runtime import SpectralMemoryOperators


def test_zero_diffusion_recovers_original_memory_update_exactly() -> None:
    config = SpectralMemoryConfig(n_modes=24, lambda_value=0.07)
    baseline = SpectralMemoryOperators(config)
    field = RelaxationDiffusionMemoryOperators(
        config,
        diffusion_per_update=0.0,
    )
    rho = baseline.deposition(7.0)

    expected = baseline.update_rho(rho, deposited_at=11.0)
    actual = field.update_rho(rho, deposited_at=11.0)

    np.testing.assert_array_equal(actual, expected)


def test_diffusion_preserves_mass_and_damps_nonzero_modes() -> None:
    config = SpectralMemoryConfig(n_modes=24, lambda_value=0.1, memory_mass=2.0)
    baseline = SpectralMemoryOperators(config)
    field = RelaxationDiffusionMemoryOperators(
        config,
        diffusion_per_update=0.03,
    )
    rho = baseline.deposition(7.0)
    baseline_new = baseline.update_rho(rho, deposited_at=11.0)
    field_new = field.update_rho(rho, deposited_at=11.0)

    assert math.isclose(
        config.box_length * field_new[0].real,
        config.memory_mass,
        rel_tol=0.0,
        abs_tol=2e-15,
    )
    assert np.all(np.abs(field_new[1:]) <= np.abs(baseline_new[1:]))
    assert np.any(np.abs(field_new[1:]) < np.abs(baseline_new[1:]))


def test_reported_diffusion_length_uses_memory_time() -> None:
    config = SpectralMemoryConfig(lambda_value=0.02)
    field = RelaxationDiffusionMemoryOperators(
        config,
        diffusion_per_update=0.09,
    )

    assert math.isclose(
        field.diffusion_length_per_memory_time,
        3.0,
        rel_tol=1e-15,
    )


@pytest.mark.parametrize("value", [-1.0, math.inf, math.nan])
def test_invalid_diffusion_is_rejected(value: float) -> None:
    with pytest.raises(ValueError, match="diffusion_per_update"):
        RelaxationDiffusionMemoryOperators(
            SpectralMemoryConfig(),
            diffusion_per_update=value,
        )
