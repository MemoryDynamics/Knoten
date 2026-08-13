"""Order diagnostics for paired, nonparametric impulse responses."""

from __future__ import annotations

from dataclasses import dataclass
import math

import numpy as np
from scipy.optimize import least_squares


@dataclass(frozen=True)
class SharedRecurrenceFit:
    """One homogeneous recurrence shared by response panels and readouts."""

    order: int
    coefficients: np.ndarray
    poles: np.ndarray
    train_one_step_rmse: float
    test_one_step_rmse: float
    test_rollout_rmse: float
    test_zero_rmse: float
    test_persistence_rmse: float
    active_channels: int
    train_targets: int
    test_targets: int

    @property
    def stable(self) -> bool:
        return bool(np.max(np.abs(self.poles)) < 1.0)

    @property
    def rollout_ratio_to_zero(self) -> float:
        return self.test_rollout_rmse / max(
            self.test_zero_rmse,
            np.finfo(float).tiny,
        )


@dataclass(frozen=True)
class DampedSecondOrderFit:
    """Second-order recurrence restricted to a damped continuous oscillator."""

    coefficients: np.ndarray
    poles: np.ndarray
    damping_rate: float
    natural_frequency: float
    train_one_step_rmse: float
    test_one_step_rmse: float
    test_rollout_rmse: float
    test_zero_rmse: float
    test_persistence_rmse: float
    active_channels: int
    train_targets: int
    test_targets: int

    @property
    def stable(self) -> bool:
        return bool(np.max(np.abs(self.poles)) < 1.0)

    @property
    def underdamped(self) -> bool:
        return bool(self.natural_frequency > self.damping_rate)

    @property
    def rollout_ratio_to_zero(self) -> float:
        return self.test_rollout_rmse / max(
            self.test_zero_rmse,
            np.finfo(float).tiny,
        )


@dataclass(frozen=True)
class ImpulseHankelSpectrum:
    """Singular spectrum of a panel block-Hankel impulse matrix."""

    singular_values: np.ndarray
    stable_rank: float
    entropy_rank: float
    numerical_rank_1e3: int
    numerical_rank_1e6: int
    block_rows: int
    block_columns: int
    active_channels: int


@dataclass(frozen=True)
class _PreparedRecurrence:
    values: np.ndarray
    scales: np.ndarray
    predictors: np.ndarray
    targets: np.ndarray
    target_times: np.ndarray
    train_mask: np.ndarray
    test_mask: np.ndarray
    split_time: int


def _validate_response(response: np.ndarray) -> np.ndarray:
    values = np.asarray(response, dtype=float)
    if (
        values.ndim != 3
        or values.shape[0] < 12
        or values.shape[1] < 1
        or values.shape[2] < 1
        or not np.isfinite(values).all()
    ):
        raise ValueError(
            "response must be finite with shape (time, panel, readout)"
        )
    return values


def _prepare_recurrence(
    response: np.ndarray,
    *,
    order: int,
    train_fraction: float,
    start_index: int,
    relative_channel_floor: float,
) -> _PreparedRecurrence:
    values = _validate_response(response)
    if (
        isinstance(order, bool)
        or not isinstance(order, (int, np.integer))
        or order < 1
    ):
        raise ValueError("order must be a positive integer")
    if not 0.5 <= train_fraction < 1.0:
        raise ValueError("train_fraction must lie in [0.5, 1)")
    if (
        isinstance(start_index, bool)
        or not isinstance(start_index, (int, np.integer))
        or start_index < 0
    ):
        raise ValueError("start_index must be a non-negative integer")
    if not np.isfinite(relative_channel_floor) or not 0.0 <= relative_channel_floor < 1.0:
        raise ValueError("relative_channel_floor must lie in [0, 1)")

    split_time = int(math.floor(train_fraction * (values.shape[0] - 1)))
    first_target = max(int(start_index), int(order))
    target_times = np.arange(first_target, values.shape[0])
    train_mask = target_times <= split_time
    test_mask = target_times > split_time
    if np.count_nonzero(train_mask) < max(4, order + 1):
        raise ValueError("training window is too short for requested recurrence")
    if np.count_nonzero(test_mask) < 4:
        raise ValueError("holdout window is too short")

    training = values[: split_time + 1]
    scales = np.sqrt(np.mean(training * training, axis=0))
    maximum = float(np.max(scales))
    floor = max(
        relative_channel_floor * maximum,
        np.finfo(float).eps * max(1.0, float(np.max(np.abs(training)))),
    )
    active = scales > floor
    if not np.any(active):
        raise ValueError("no response channel clears the registered signal floor")
    flattened = values.reshape(values.shape[0], -1)[:, active.reshape(-1)]
    selected_scales = scales.reshape(-1)[active.reshape(-1)]
    standardized = flattened / selected_scales[None, :]

    predictors = np.stack(
        [standardized[target_times - lag] for lag in range(1, order + 1)],
        axis=2,
    )
    targets = standardized[target_times]
    return _PreparedRecurrence(
        values=standardized,
        scales=selected_scales,
        predictors=predictors,
        targets=targets,
        target_times=target_times,
        train_mask=train_mask,
        test_mask=test_mask,
        split_time=split_time,
    )


def _recurrence_metrics(
    prepared: _PreparedRecurrence,
    coefficients: np.ndarray,
) -> tuple[float, float, float, float, float]:
    prediction = np.einsum("tco,o->tc", prepared.predictors, coefficients)
    train_residual = prepared.targets[prepared.train_mask] - prediction[
        prepared.train_mask
    ]
    test_residual = prepared.targets[prepared.test_mask] - prediction[
        prepared.test_mask
    ]

    rollout = prepared.values.copy()
    for time in range(prepared.split_time + 1, rollout.shape[0]):
        prediction = sum(
            coefficients[lag - 1] * rollout[time - lag]
            for lag in range(1, coefficients.size + 1)
        )
        rollout[time] = np.clip(
            np.nan_to_num(prediction, nan=0.0, posinf=1e100, neginf=-1e100),
            -1e100,
            1e100,
        )
    test_times = prepared.target_times[prepared.test_mask]
    rollout_residual = prepared.values[test_times] - rollout[test_times]
    zero_residual = prepared.values[test_times]
    persistence = np.broadcast_to(
        prepared.values[prepared.split_time],
        (test_times.size, prepared.values.shape[1]),
    )
    persistence_residual = prepared.values[test_times] - persistence
    return (
        float(np.sqrt(np.mean(train_residual * train_residual))),
        float(np.sqrt(np.mean(test_residual * test_residual))),
        float(np.sqrt(np.mean(rollout_residual * rollout_residual))),
        float(np.sqrt(np.mean(zero_residual * zero_residual))),
        float(np.sqrt(np.mean(persistence_residual * persistence_residual))),
    )


def fit_shared_recurrence(
    response: np.ndarray,
    *,
    order: int,
    train_fraction: float = 0.6,
    start_index: int = 1,
    relative_channel_floor: float = 1e-6,
) -> SharedRecurrenceFit:
    """Fit one no-intercept temporal recurrence and score recursive holdout."""

    prepared = _prepare_recurrence(
        response,
        order=order,
        train_fraction=train_fraction,
        start_index=start_index,
        relative_channel_floor=relative_channel_floor,
    )
    design = prepared.predictors[prepared.train_mask].reshape(-1, order)
    target = prepared.targets[prepared.train_mask].reshape(-1)
    coefficients, _, _, _ = np.linalg.lstsq(design, target, rcond=None)
    metrics = _recurrence_metrics(prepared, coefficients)
    poles = np.roots(np.concatenate(([1.0], -coefficients)))
    return SharedRecurrenceFit(
        order=int(order),
        coefficients=np.asarray(coefficients, dtype=float),
        poles=np.asarray(poles, dtype=np.complex128),
        train_one_step_rmse=metrics[0],
        test_one_step_rmse=metrics[1],
        test_rollout_rmse=metrics[2],
        test_zero_rmse=metrics[3],
        test_persistence_rmse=metrics[4],
        active_channels=int(prepared.values.shape[1]),
        train_targets=int(np.count_nonzero(prepared.train_mask)),
        test_targets=int(np.count_nonzero(prepared.test_mask)),
    )


def _damped_coefficients(
    log_rates: np.ndarray,
    sample_interval: float,
) -> tuple[np.ndarray, float, float]:
    damping = float(np.exp(log_rates[0]))
    frequency = float(np.exp(log_rates[1]))
    interval = float(sample_interval)
    difference = damping * damping - frequency * frequency
    envelope = math.exp(-damping * interval)
    if difference >= 0.0:
        argument = min(math.sqrt(difference) * interval, 700.0)
        coefficient_1 = 2.0 * envelope * math.cosh(argument)
    else:
        coefficient_1 = 2.0 * envelope * math.cos(
            math.sqrt(-difference) * interval
        )
    coefficient_2 = -(envelope * envelope)
    return np.asarray([coefficient_1, coefficient_2]), damping, frequency


def fit_damped_second_order_recurrence(
    response: np.ndarray,
    *,
    sample_interval: float = 1.0,
    train_fraction: float = 0.6,
    start_index: int = 2,
    relative_channel_floor: float = 1e-6,
) -> DampedSecondOrderFit:
    """Fit the necessary damped-oscillator subset of stable AR(2) maps.

    This restriction supplies a passive reciprocal *temporal* candidate. It
    does not establish collocated power ports or a positive storage metric;
    those remain separate gates if this model wins on holdout.
    """

    if not np.isfinite(sample_interval) or sample_interval <= 0.0:
        raise ValueError("sample_interval must be positive and finite")
    prepared = _prepare_recurrence(
        response,
        order=2,
        train_fraction=train_fraction,
        start_index=start_index,
        relative_channel_floor=relative_channel_floor,
    )
    design = prepared.predictors[prepared.train_mask].reshape(-1, 2)
    target = prepared.targets[prepared.train_mask].reshape(-1)

    def residual(log_rates: np.ndarray) -> np.ndarray:
        coefficients, _, _ = _damped_coefficients(log_rates, sample_interval)
        return design @ coefficients - target

    inverse_interval = 1.0 / float(sample_interval)
    starts = (
        (0.01 * inverse_interval, 0.1 * inverse_interval),
        (0.1 * inverse_interval, 0.1 * inverse_interval),
        (0.1 * inverse_interval, 1.0 * inverse_interval),
        (1.0 * inverse_interval, 0.1 * inverse_interval),
        (1.0 * inverse_interval, 1.0 * inverse_interval),
    )
    best = None
    for damping, frequency in starts:
        candidate = least_squares(
            residual,
            np.log([damping, frequency]),
            bounds=(-30.0, 30.0),
        )
        if best is None or candidate.cost < best.cost:
            best = candidate
    if best is None:  # pragma: no cover
        raise RuntimeError("damped recurrence optimization did not run")
    coefficients, damping, frequency = _damped_coefficients(
        best.x,
        sample_interval,
    )
    metrics = _recurrence_metrics(prepared, coefficients)
    poles = np.roots(np.concatenate(([1.0], -coefficients)))
    return DampedSecondOrderFit(
        coefficients=coefficients,
        poles=np.asarray(poles, dtype=np.complex128),
        damping_rate=damping,
        natural_frequency=frequency,
        train_one_step_rmse=metrics[0],
        test_one_step_rmse=metrics[1],
        test_rollout_rmse=metrics[2],
        test_zero_rmse=metrics[3],
        test_persistence_rmse=metrics[4],
        active_channels=int(prepared.values.shape[1]),
        train_targets=int(np.count_nonzero(prepared.train_mask)),
        test_targets=int(np.count_nonzero(prepared.test_mask)),
    )


def impulse_hankel_spectrum(
    response: np.ndarray,
    *,
    block_rows: int,
    block_columns: int,
    start_index: int = 1,
    relative_channel_floor: float = 1e-6,
) -> ImpulseHankelSpectrum:
    """Return a scale-balanced panel block-Hankel singular spectrum."""

    values = _validate_response(response)
    for name, value in (("block_rows", block_rows), ("block_columns", block_columns)):
        if (
            isinstance(value, bool)
            or not isinstance(value, (int, np.integer))
            or value < 1
        ):
            raise ValueError(f"{name} must be a positive integer")
    if start_index < 0:
        raise ValueError("start_index must be non-negative")
    stop = int(start_index) + int(block_rows) + int(block_columns) - 1
    if stop > values.shape[0]:
        raise ValueError("response is too short for requested Hankel blocks")

    scales = np.sqrt(np.mean(values[:stop] * values[:stop], axis=0))
    maximum = float(np.max(scales))
    floor = max(
        relative_channel_floor * maximum,
        np.finfo(float).eps * max(1.0, float(np.max(np.abs(values[:stop])))),
    )
    active = scales > floor
    if not np.any(active):
        raise ValueError("no response channel clears the registered signal floor")
    columns = []
    for panel in range(values.shape[1]):
        channel_mask = active[panel]
        if not np.any(channel_mask):
            continue
        panel_values = values[:, panel, channel_mask] / scales[panel, channel_mask]
        for column in range(block_columns):
            block = panel_values[
                start_index + column : start_index + column + block_rows
            ]
            columns.append(block.reshape(-1))
    hankel = np.column_stack(columns)
    singular = np.linalg.svd(hankel, compute_uv=False)
    if singular.size == 0 or singular[0] <= 0.0:
        raise ValueError("impulse Hankel matrix has no non-zero singular value")
    relative = singular / singular[0]
    power = singular * singular
    stable_rank = float(np.sum(power) / power[0])
    probabilities = power / np.sum(power)
    positive = probabilities > 0.0
    entropy_rank = float(
        np.exp(-np.sum(probabilities[positive] * np.log(probabilities[positive])))
    )
    return ImpulseHankelSpectrum(
        singular_values=np.asarray(singular, dtype=float),
        stable_rank=stable_rank,
        entropy_rank=entropy_rank,
        numerical_rank_1e3=int(np.count_nonzero(relative >= 1e-3)),
        numerical_rank_1e6=int(np.count_nonzero(relative >= 1e-6)),
        block_rows=int(block_rows),
        block_columns=int(block_columns),
        active_channels=int(np.count_nonzero(active)),
    )
