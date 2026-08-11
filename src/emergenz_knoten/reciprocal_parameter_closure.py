"""Independent local-gain closure for reciprocal scalar-memory knots."""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Iterable

import numpy as np

from .core import SimulationConfig, validate_simulation_config
from .kernels import (
    ScalarReadoutKernel,
    double_gaussian_hessian,
    resolve_scalar_readout_kernel,
)
from .state import FiniteMemoryState


@dataclass(frozen=True)
class ReciprocalMatrixModeResult:
    """Relative ``(x_minus, memory-centre-minus)`` linear mode result."""

    lambda_value: float
    self_gain: np.ndarray
    cross_gain: np.ndarray
    transition: np.ndarray
    eigenvalues: np.ndarray

    @property
    def is_stable(self) -> bool:
        return bool(np.max(np.abs(self.eigenvalues)) < 1.0)

    @property
    def has_complex_pair(self) -> bool:
        return bool(np.max(np.abs(self.eigenvalues.imag)) > 1.0e-10)

    @property
    def has_stable_complex_pair(self) -> bool:
        values = self.eigenvalues
        return bool(np.any((np.abs(values.imag) > 1.0e-10) & (np.abs(values) < 1.0)))


@dataclass(frozen=True)
class CommonGainScaleInterval:
    """Open common-scale interval for a scalar reciprocal relative mode."""

    lower: float
    upper: float

    @property
    def exists(self) -> bool:
        return bool(
            math.isfinite(self.lower)
            and math.isfinite(self.upper)
            and 0.0 <= self.lower < self.upper
        )

    @property
    def geometric_midpoint(self) -> float:
        if not self.exists or self.lower <= 0.0:
            return math.nan
        return math.sqrt(self.lower * self.upper)


def common_gain_scale_interval(
    lambda_value: float,
    base_self_gain: float,
    base_cross_gain: float,
) -> CommonGainScaleInterval:
    r"""Return scales yielding a stable complex scalar ``A_-`` mode.

    Both gains are multiplied by the same non-negative scale. The returned
    bounds are open because a zero discriminant is a repeated real pole.
    """

    values = (lambda_value, base_self_gain, base_cross_gain)
    if not all(math.isfinite(value) for value in values):
        raise ValueError("lambda_value and gains must be finite")
    if not 0.0 < lambda_value <= 1.0:
        raise ValueError("lambda_value must lie in (0, 1]")
    if base_self_gain < 0.0 or base_cross_gain < 0.0:
        raise ValueError("base gains must be non-negative")
    if base_cross_gain <= base_self_gain:
        return CommonGainScaleInterval(math.nan, math.nan)

    q = 1.0 - lambda_value
    gain_sum = base_self_gain + base_cross_gain
    if q == 0.0 or gain_sum == 0.0:
        return CommonGainScaleInterval(math.nan, math.nan)

    trace_slope = q * base_self_gain + (1.0 + lambda_value) * base_cross_gain
    coefficients = np.array(
        [
            trace_slope**2,
            -2.0 * (2.0 - lambda_value) * trace_slope + 4.0 * q * gain_sum,
            lambda_value**2,
        ],
        dtype=float,
    )
    roots = np.roots(coefficients)
    real_roots = sorted(
        float(root.real)
        for root in roots
        if abs(float(root.imag)) <= 1.0e-10 and float(root.real) > 0.0
    )
    if len(real_roots) != 2:
        return CommonGainScaleInterval(math.nan, math.nan)

    stability_upper = 1.0 / gain_sum
    lower = max(0.0, real_roots[0])
    upper = min(real_roots[1], stability_upper)
    if not lower < upper:
        return CommonGainScaleInterval(math.nan, math.nan)
    return CommonGainScaleInterval(lower, upper)


def reciprocal_relative_mode_operator(
    lambda_value: float,
    self_gain: Iterable[Iterable[float]],
    cross_gain: Iterable[Iterable[float]],
) -> ReciprocalMatrixModeResult:
    r"""Build the exact matrix-valued extension of the scalar ``A_-`` block.

    ``G`` and ``C`` are the dimensionless Jacobian gains of the self and cross
    potential readouts. The state is ``Y_-=(x_-, xbar_rho_-)``. Neither ``Y_-``
    nor the returned transition matrix is an additional microscopic parameter.
    """

    if not math.isfinite(lambda_value) or not 0.0 < lambda_value <= 1.0:
        raise ValueError("lambda_value must lie in (0, 1]")
    self_matrix = np.asarray(self_gain, dtype=float)
    cross_matrix = np.asarray(cross_gain, dtype=float)
    if (
        self_matrix.ndim != 2
        or self_matrix.shape[0] < 1
        or self_matrix.shape[0] != self_matrix.shape[1]
        or cross_matrix.shape != self_matrix.shape
        or not np.isfinite(self_matrix).all()
        or not np.isfinite(cross_matrix).all()
    ):
        raise ValueError("self_gain and cross_gain must be finite equal square matrices")

    dim = self_matrix.shape[0]
    identity = np.eye(dim, dtype=float)
    q = 1.0 - lambda_value
    top_left = identity - self_matrix - cross_matrix
    top_right = self_matrix - cross_matrix
    transition = np.block(
        [
            [top_left, top_right],
            [lambda_value * top_left, q * identity + lambda_value * top_right],
        ]
    )
    return ReciprocalMatrixModeResult(
        lambda_value=float(lambda_value),
        self_gain=self_matrix.copy(),
        cross_gain=cross_matrix.copy(),
        transition=transition,
        eigenvalues=np.asarray(np.linalg.eigvals(transition), dtype=np.complex128),
    )


def finite_memory_gain_matrix(
    evaluation_point: Iterable[float],
    source_state: FiniteMemoryState,
    config: SimulationConfig,
    *,
    coupling_eta: float | None = None,
    readout: ScalarReadoutKernel | None = None,
) -> np.ndarray:
    r"""Return ``eta_coupling Hessian(K_cross * rho)`` without fitting a path."""

    validate_simulation_config(config)
    point = np.asarray(evaluation_point, dtype=float)
    if point.shape != (source_state.dim,) or not np.isfinite(point).all():
        raise ValueError("evaluation_point must be finite and match source dimension")
    if config.dim != source_state.dim:
        raise ValueError("config and source_state dimensions must match")
    eta_value = config.eta if coupling_eta is None else float(coupling_eta)
    if not np.isfinite(eta_value):
        raise ValueError("coupling_eta must be finite")
    kernel = resolve_scalar_readout_kernel(
        readout,
        sigma_rep=config.sigma_rep,
        sigma_att=config.sigma_att,
        amplitude_rep=config.amplitude_rep,
        amplitude_att=config.amplitude_att,
    )
    hessian = double_gaussian_hessian(
        point,
        source_state.memory,
        source_state.weights,
        sigma_rep=kernel.sigma_rep,
        sigma_att=kernel.sigma_att,
        amplitude_rep=kernel.amplitude_rep,
        amplitude_att=kernel.amplitude_att,
        deposition_kernel=config.deposition_kernel,
        deposition_sigma=config.deposition_sigma,
    )
    return eta_value * hessian
