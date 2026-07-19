"""Cached operators for resource-bounded spectral-memory simulations."""

from __future__ import annotations

import numpy as np

from .spectral_memory_field import (
    SpectralMemoryConfig,
    kernel_transfer,
    wavenumbers,
    wrap_periodic,
)


class SpectralMemoryOperators:
    """Precompute fixed arrays while leaving the model state explicit."""

    def __init__(self, config: SpectralMemoryConfig) -> None:
        self.config = config
        self.k = wavenumbers(config)
        self.transfer = kernel_transfer(config).astype(np.complex128)
        self.smoothing = np.exp(-0.5 * config.deposition_sigma**2 * self.k**2)
        for values in (self.k, self.transfer, self.smoothing):
            values.setflags(write=False)

    @property
    def state_bytes(self) -> int:
        """Memory used by one complex field state, excluding cached operators."""

        return int((self.config.n_modes + 1) * np.dtype(np.complex128).itemsize)

    def deposition(self, x: float) -> np.ndarray:
        x = wrap_periodic(x, self.config.box_length)
        coefficients = (
            self.config.memory_mass
            / self.config.box_length
            * self.smoothing
            * np.exp(-1j * self.k * x)
        )
        coefficients[0] = complex(
            self.config.memory_mass / self.config.box_length,
            0.0,
        )
        return np.asarray(coefficients, dtype=np.complex128)

    def gradient(self, rho_coefficients: np.ndarray, *, x: float) -> float:
        rho = np.asarray(rho_coefficients, dtype=np.complex128)
        if rho.shape != (self.config.n_modes + 1,):
            raise ValueError("rho coefficient shape does not match config")
        phases = np.exp(
            1j * self.k[1:] * wrap_periodic(x, self.config.box_length)
        )
        return float(
            2.0
            * np.real(
                np.sum(
                    1j
                    * self.k[1:]
                    * self.transfer[1:]
                    * rho[1:]
                    * phases
                )
            )
        )

    def update_rho(
        self,
        rho_coefficients: np.ndarray,
        *,
        deposited_at: float,
    ) -> np.ndarray:
        rho = np.asarray(rho_coefficients, dtype=np.complex128)
        if rho.shape != (self.config.n_modes + 1,):
            raise ValueError("rho coefficient shape does not match config")
        return np.asarray(
            (1.0 - self.config.lambda_value) * rho
            + self.config.lambda_value * self.deposition(deposited_at),
            dtype=np.complex128,
        )
