"""Split-step relaxation-diffusion extension of spectral scalar memory."""

from __future__ import annotations

import math

import numpy as np

from .spectral_memory_field import SpectralMemoryConfig
from .spectral_memory_runtime import SpectralMemoryOperators


class RelaxationDiffusionMemoryOperators(SpectralMemoryOperators):
    """Apply exponential forgetting, deposition, then one heat-semigroup step.

    The update is

    ``rho_new_hat(k) = exp(-nu*k^2) * (q*rho_hat(k) + lambda*g_hat_x(k))``.

    Setting ``nu=0`` recovers the original spectral exponential-memory update
    exactly. Positive ``nu`` is a model extension, not a reparametrization.
    """

    def __init__(
        self,
        config: SpectralMemoryConfig,
        *,
        diffusion_per_update: float,
    ) -> None:
        if not math.isfinite(diffusion_per_update) or diffusion_per_update < 0.0:
            raise ValueError("diffusion_per_update must be non-negative and finite")
        super().__init__(config)
        self.diffusion_per_update = float(diffusion_per_update)
        self.heat_transfer = np.exp(-self.diffusion_per_update * self.k**2)
        self.heat_transfer.setflags(write=False)

    @property
    def diffusion_length_per_memory_time(self) -> float:
        """One-dimensional heat RMS length over ``lambda^-1`` updates."""

        return float(
            math.sqrt(
                2.0 * self.diffusion_per_update / self.config.lambda_value
            )
        )

    def update_rho(
        self,
        rho_coefficients: np.ndarray,
        *,
        deposited_at: float,
    ) -> np.ndarray:
        relaxed_and_deposited = super().update_rho(
            rho_coefficients,
            deposited_at=deposited_at,
        )
        return np.asarray(
            self.heat_transfer * relaxed_and_deposited,
            dtype=np.complex128,
        )
