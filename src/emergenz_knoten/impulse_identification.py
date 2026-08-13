"""Order diagnostics for paired, nonparametric impulse responses."""

from __future__ import annotations

from dataclasses import dataclass
import math

import numpy as np


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
class HeldOutReadoutRecurrenceFit:
    """Shared recurrence learned on one observable and scored on another."""

    order: int
    coefficients: np.ndarray
    poles: np.ndarray
    fit_train_one_step_rmse: float
    fit_test_rollout_rmse: float
    fit_test_zero_rmse: float
    readout_test_one_step_rmse: float
    readout_test_rollout_rmse: float
    readout_test_zero_rmse: float
    fit_channels: int
    readout_channels: int
    train_targets: int
    test_targets: int

    @property
    def stable(self) -> bool:
        return bool(np.max(np.abs(self.poles)) < 1.0)

    @property
    def readout_rollout_ratio_to_zero(self) -> float:
        return self.readout_test_rollout_rmse / max(
            self.readout_test_zero_rmse,
            np.finfo(float).tiny,
        )


@dataclass(frozen=True)
class ContinuousSecondOrderInterpretation:
    """Continuous-time interpretation of one real discrete AR(2) map.

    A stable real AR(2) with positive pole product already is the exact sample
    map of a damped second-order scalar equation. This object interprets the
    fitted coefficients; it is not an independently fitted model.
    """

    coefficients: np.ndarray
    poles: np.ndarray
    damping_rate: float
    natural_frequency: float
    angular_frequency: float
    classification: str
    embeddable: bool

    @property
    def stable(self) -> bool:
        return bool(np.max(np.abs(self.poles)) < 1.0)

    @property
    def underdamped(self) -> bool:
        return self.classification == "underdamped"


@dataclass(frozen=True)
class ConservativeOscillatorFit:
    """Undamped one-parameter AR(2) null with unit-modulus poles."""

    coefficient: float
    coefficients: np.ndarray
    poles: np.ndarray
    angular_frequency: float
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
        return bool(np.max(np.abs(self.poles)) <= 1.0 + 1e-12)

    @property
    def rollout_ratio_to_zero(self) -> float:
        return self.test_rollout_rmse / max(
            self.test_zero_rmse,
            np.finfo(float).tiny,
        )


@dataclass(frozen=True)
class DampedSecondOrderFit:
    """Compatibility view of AR(2) as a damped continuous equation.

    This is deliberately not a distinct fitted model. If the free AR(2) has
    a real stable continuous embedding, all prediction errors and coefficients
    are exactly those of that AR(2); only continuous-rate labels are added.
    """

    coefficients: np.ndarray
    poles: np.ndarray
    damping_rate: float
    natural_frequency: float
    angular_frequency: float
    classification: str
    embeddable: bool
    equivalent_to_unconstrained: bool
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
        return self.classification == "underdamped"

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


def fit_recurrence_with_held_out_readout(
    fit_response: np.ndarray,
    readout_response: np.ndarray,
    *,
    order: int,
    train_fraction: float = 0.6,
    start_index: int = 1,
    relative_channel_floor: float = 1e-6,
) -> HeldOutReadoutRecurrenceFit:
    """Learn shared poles from ``fit_response`` and score a held-out readout.

    Both arrays must use the same time and panel axes. Scaling and inactive
    channel filtering are learned separately on their common training window;
    no readout value contributes to the recurrence coefficients.
    """

    fit_values = _validate_response(fit_response)
    readout_values = _validate_response(readout_response)
    if fit_values.shape[:2] != readout_values.shape[:2]:
        raise ValueError("fit and readout responses must share time and panel axes")
    prepared_fit = _prepare_recurrence(
        fit_values,
        order=order,
        train_fraction=train_fraction,
        start_index=start_index,
        relative_channel_floor=relative_channel_floor,
    )
    prepared_readout = _prepare_recurrence(
        readout_values,
        order=order,
        train_fraction=train_fraction,
        start_index=start_index,
        relative_channel_floor=relative_channel_floor,
    )
    if not np.array_equal(prepared_fit.target_times, prepared_readout.target_times):
        raise RuntimeError("fit and readout target windows differ")
    design = prepared_fit.predictors[prepared_fit.train_mask].reshape(-1, order)
    target = prepared_fit.targets[prepared_fit.train_mask].reshape(-1)
    coefficients, _, _, _ = np.linalg.lstsq(design, target, rcond=None)
    fit_metrics = _recurrence_metrics(prepared_fit, coefficients)
    readout_metrics = _recurrence_metrics(prepared_readout, coefficients)
    poles = np.roots(np.concatenate(([1.0], -coefficients)))
    return HeldOutReadoutRecurrenceFit(
        order=int(order),
        coefficients=np.asarray(coefficients, dtype=float),
        poles=np.asarray(poles, dtype=np.complex128),
        fit_train_one_step_rmse=fit_metrics[0],
        fit_test_rollout_rmse=fit_metrics[2],
        fit_test_zero_rmse=fit_metrics[3],
        readout_test_one_step_rmse=readout_metrics[1],
        readout_test_rollout_rmse=readout_metrics[2],
        readout_test_zero_rmse=readout_metrics[3],
        fit_channels=int(prepared_fit.values.shape[1]),
        readout_channels=int(prepared_readout.values.shape[1]),
        train_targets=int(np.count_nonzero(prepared_fit.train_mask)),
        test_targets=int(np.count_nonzero(prepared_fit.test_mask)),
    )


def fit_conservative_recurrence_with_held_out_readout(
    fit_response: np.ndarray,
    readout_response: np.ndarray,
    *,
    train_fraction: float = 0.6,
    start_index: int = 2,
    relative_channel_floor: float = 1e-6,
) -> HeldOutReadoutRecurrenceFit:
    """Fit an undamped AR(2) on one observable and score another."""

    fit_values = _validate_response(fit_response)
    readout_values = _validate_response(readout_response)
    if fit_values.shape[:2] != readout_values.shape[:2]:
        raise ValueError("fit and readout responses must share time and panel axes")
    prepared_fit = _prepare_recurrence(
        fit_values,
        order=2,
        train_fraction=train_fraction,
        start_index=start_index,
        relative_channel_floor=relative_channel_floor,
    )
    prepared_readout = _prepare_recurrence(
        readout_values,
        order=2,
        train_fraction=train_fraction,
        start_index=start_index,
        relative_channel_floor=relative_channel_floor,
    )
    design = prepared_fit.predictors[prepared_fit.train_mask].reshape(-1, 2)
    target = prepared_fit.targets[prepared_fit.train_mask].reshape(-1)
    adjusted_target = target + design[:, 1]
    denominator = float(np.dot(design[:, 0], design[:, 0]))
    if denominator <= np.finfo(float).tiny:
        raise ValueError("leading lag has no training variation")
    coefficient = float(np.dot(design[:, 0], adjusted_target) / denominator)
    coefficients = np.asarray([np.clip(coefficient, -2.0, 2.0), -1.0])
    fit_metrics = _recurrence_metrics(prepared_fit, coefficients)
    readout_metrics = _recurrence_metrics(prepared_readout, coefficients)
    poles = np.roots(np.concatenate(([1.0], -coefficients)))
    return HeldOutReadoutRecurrenceFit(
        order=2,
        coefficients=coefficients,
        poles=np.asarray(poles, dtype=np.complex128),
        fit_train_one_step_rmse=fit_metrics[0],
        fit_test_rollout_rmse=fit_metrics[2],
        fit_test_zero_rmse=fit_metrics[3],
        readout_test_one_step_rmse=readout_metrics[1],
        readout_test_rollout_rmse=readout_metrics[2],
        readout_test_zero_rmse=readout_metrics[3],
        fit_channels=int(prepared_fit.values.shape[1]),
        readout_channels=int(prepared_readout.values.shape[1]),
        train_targets=int(np.count_nonzero(prepared_fit.train_mask)),
        test_targets=int(np.count_nonzero(prepared_fit.test_mask)),
    )


def interpret_continuous_second_order(
    coefficients: np.ndarray,
    *,
    sample_interval: float = 1.0,
) -> ContinuousSecondOrderInterpretation:
    """Map a fitted AR(2) to continuous poles without refitting the data."""

    if not np.isfinite(sample_interval) or sample_interval <= 0.0:
        raise ValueError("sample_interval must be positive and finite")
    values = np.asarray(coefficients, dtype=float)
    if values.shape != (2,) or not np.isfinite(values).all():
        raise ValueError("coefficients must be two finite AR coefficients")
    poles = np.asarray(
        np.roots(np.concatenate(([1.0], -values))),
        dtype=np.complex128,
    )
    tolerance = 1e-10
    if abs(poles[0] - np.conjugate(poles[1])) <= tolerance:
        continuous = np.log(poles.astype(np.complex128)) / float(sample_interval)
        damping = float(-np.mean(continuous.real))
        angular = float(np.max(np.abs(continuous.imag)))
        natural = float(math.hypot(damping, angular))
        classification = "underdamped" if angular > tolerance else "real_repeated"
        embeddable = bool(damping >= -tolerance)
    elif np.all(np.abs(poles.imag) <= tolerance) and np.all(poles.real > 0.0):
        rates = np.log(poles.real) / float(sample_interval)
        damping = float(-0.5 * np.sum(rates))
        discriminant = float((0.5 * (rates[0] - rates[1])) ** 2)
        natural_squared = damping * damping - discriminant
        natural = float(math.sqrt(max(natural_squared, 0.0)))
        angular = 0.0
        classification = "overdamped" if abs(rates[0] - rates[1]) > tolerance else "critical"
        embeddable = bool(damping >= -tolerance and natural_squared >= -tolerance)
    else:
        damping = math.nan
        natural = math.nan
        angular = math.nan
        classification = "not_real_continuous_embedding"
        embeddable = False
    return ContinuousSecondOrderInterpretation(
        coefficients=values,
        poles=poles,
        damping_rate=damping,
        natural_frequency=natural,
        angular_frequency=angular,
        classification=classification,
        embeddable=embeddable,
    )


def fit_damped_second_order_recurrence(
    response: np.ndarray,
    *,
    sample_interval: float = 1.0,
    train_fraction: float = 0.6,
    start_index: int = 2,
    relative_channel_floor: float = 1e-6,
) -> DampedSecondOrderFit:
    """Compatibility helper: fit free AR(2), then interpret it continuously.

    This function is retained so historical P3.8e artifacts remain executable.
    It must not be counted as a separate model comparison against AR(2).
    """

    fit = fit_shared_recurrence(
        response,
        order=2,
        train_fraction=train_fraction,
        start_index=start_index,
        relative_channel_floor=relative_channel_floor,
    )
    interpretation = interpret_continuous_second_order(
        fit.coefficients,
        sample_interval=sample_interval,
    )
    return DampedSecondOrderFit(
        coefficients=fit.coefficients,
        poles=fit.poles,
        damping_rate=interpretation.damping_rate,
        natural_frequency=interpretation.natural_frequency,
        angular_frequency=interpretation.angular_frequency,
        classification=interpretation.classification,
        embeddable=interpretation.embeddable,
        equivalent_to_unconstrained=True,
        train_one_step_rmse=fit.train_one_step_rmse,
        test_one_step_rmse=fit.test_one_step_rmse,
        test_rollout_rmse=fit.test_rollout_rmse,
        test_zero_rmse=fit.test_zero_rmse,
        test_persistence_rmse=fit.test_persistence_rmse,
        active_channels=fit.active_channels,
        train_targets=fit.train_targets,
        test_targets=fit.test_targets,
    )


def fit_conservative_second_order_recurrence(
    response: np.ndarray,
    *,
    sample_interval: float = 1.0,
    train_fraction: float = 0.6,
    start_index: int = 2,
    relative_channel_floor: float = 1e-6,
) -> ConservativeOscillatorFit:
    """Fit the distinct undamped null ``y[n]=a y[n-1]-y[n-2]``."""

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
    adjusted_target = target + design[:, 1]
    denominator = float(np.dot(design[:, 0], design[:, 0]))
    if denominator <= np.finfo(float).tiny:
        raise ValueError("leading lag has no training variation")
    coefficient = float(np.dot(design[:, 0], adjusted_target) / denominator)
    coefficient = float(np.clip(coefficient, -2.0, 2.0))
    coefficients = np.asarray([coefficient, -1.0], dtype=float)
    metrics = _recurrence_metrics(prepared, coefficients)
    poles = np.asarray(
        np.roots(np.concatenate(([1.0], -coefficients))),
        dtype=np.complex128,
    )
    angular = float(math.acos(np.clip(0.5 * coefficient, -1.0, 1.0)))
    return ConservativeOscillatorFit(
        coefficient=coefficient,
        coefficients=coefficients,
        poles=poles,
        angular_frequency=angular / float(sample_interval),
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

    flattened = values.reshape(values.shape[0], -1)
    scales = np.sqrt(np.mean(flattened[:stop] * flattened[:stop], axis=0))
    maximum = float(np.max(scales))
    floor = max(
        relative_channel_floor * maximum,
        np.finfo(float).eps * max(1.0, float(np.max(np.abs(flattened[:stop])))),
    )
    active = scales > floor
    if not np.any(active):
        raise ValueError("no response channel clears the registered signal floor")
    standardized = flattened[:, active] / scales[active][None, :]
    columns = []
    for column in range(block_columns):
        block = standardized[
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
