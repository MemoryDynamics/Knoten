"""Reduced-mode diagnostics for paired reciprocal knot continuations."""

from __future__ import annotations

from dataclasses import dataclass
import math

import numpy as np


@dataclass(frozen=True)
class IsotropicRelativeModeFit:
    """Affine two-state fit shared across all ambient coordinates."""

    transition: np.ndarray
    intercept: np.ndarray
    eigenvalues: np.ndarray
    design_condition: float
    residual_ratio: float

    @property
    def is_complex(self) -> bool:
        return bool(np.max(np.abs(self.eigenvalues.imag)) > 1e-8)

    @property
    def is_stable(self) -> bool:
        return bool(np.max(np.abs(self.eigenvalues)) < 1.0)

    @property
    def angular_frequency(self) -> float:
        """Positive phase advance per sampled update, or zero for real modes."""

        if not self.is_complex:
            return 0.0
        return float(np.max(np.abs(np.angle(self.eigenvalues))))

    @property
    def damping_rate(self) -> float:
        """Return ``-log(max |mu|)``; negative values denote growth."""

        radius = float(np.max(np.abs(self.eigenvalues)))
        if radius == 0.0:
            return math.inf
        return float(-math.log(radius))


@dataclass(frozen=True)
class PanelDelayModeFit:
    """Time-split panel VAR fit represented as a companion transition.

    Ambient coordinates are panels with a shared transition and separate
    training-window means. Features are standardized on the training window.
    The held-out score is evaluated only on the requested leading observables,
    so adding delayed state cannot improve the score through trivial shifts.
    """

    transition: np.ndarray
    coefficients: np.ndarray
    predictor_means: np.ndarray
    response_means: np.ndarray
    feature_scales: np.ndarray
    eigenvalues: np.ndarray
    design_condition: float
    train_score_rmse: float
    test_score_rmse: float
    test_persistence_rmse: float
    test_residual_ratio: float
    delay_depth: int
    score_features: int
    train_transitions: int
    test_transitions: int

    @property
    def stable_complex_eigenvalues(self) -> np.ndarray:
        values = self.eigenvalues
        return values[(np.abs(values.imag) > 1e-8) & (np.abs(values) < 1.0)]


@dataclass(frozen=True)
class ReducedRankHankelFit:
    """One fixed-rank fit within a common-window delay embedding."""

    retained_rank: int
    eigenvalues: np.ndarray
    retained_condition: float
    train_score_rmse: float
    test_score_rmse: float
    test_persistence_rmse: float
    test_residual_ratio: float

    @property
    def stable_complex_eigenvalues(self) -> np.ndarray:
        values = self.eigenvalues
        return values[(np.abs(values.imag) > 1e-8) & (np.abs(values) < 1.0)]


@dataclass(frozen=True)
class PanelHankelAudit:
    """Reduced-rank delay audit with common train and test target times."""

    delay_depth: int
    common_max_depth: int
    singular_values: np.ndarray
    stable_rank: float
    entropy_rank: float
    numerical_rank_1e6: int
    numerical_rank_1e8: int
    rank_fits: tuple[ReducedRankHankelFit, ...]
    train_transitions: int
    test_transitions: int


def correlated_pair_noise(
    common_noise: np.ndarray,
    relative_noise: np.ndarray,
    correlation: float,
) -> tuple[np.ndarray, np.ndarray]:
    """Mix independent innovations into equal-variance correlated node noise."""

    common = np.asarray(common_noise, dtype=float)
    relative = np.asarray(relative_noise, dtype=float)
    rho = float(correlation)
    if (
        common.shape != relative.shape
        or common.ndim != 2
        or not np.isfinite(common).all()
        or not np.isfinite(relative).all()
    ):
        raise ValueError("noise bases must be finite arrays of equal shape (time, dim)")
    if not math.isfinite(rho) or rho < -1.0 or rho > 1.0:
        raise ValueError("correlation must lie in [-1, 1]")
    common_scale = math.sqrt(0.5 * (1.0 + rho))
    relative_scale = math.sqrt(0.5 * (1.0 - rho))
    first = common_scale * common + relative_scale * relative
    second = common_scale * common - relative_scale * relative
    return first, second


def fit_panel_delay_mode(
    observations: np.ndarray,
    *,
    delay_depth: int = 1,
    train_fraction: float = 0.6,
    score_features: int | None = None,
) -> PanelDelayModeFit:
    """Fit a panel VAR with a chronological held-out prediction score.

    Observations have shape (time, panel, feature). The predictor stacks the
    current observation followed by delay_depth - 1 past observations. Its
    companion spectrum is an empirical delay-state spectrum, not proof that
    the selected observables form an exact Markov state.
    """

    values = np.asarray(observations, dtype=float)
    if (
        values.ndim != 3
        or values.shape[0] < 8
        or values.shape[1] < 1
        or values.shape[2] < 1
        or not np.isfinite(values).all()
    ):
        raise ValueError(
            "observations must be finite with shape (time, panel, feature)"
        )
    if (
        isinstance(delay_depth, bool)
        or not isinstance(delay_depth, (int, np.integer))
        or delay_depth < 1
    ):
        raise ValueError("delay_depth must be a positive integer")
    if not 0.5 <= train_fraction < 1.0:
        raise ValueError("train_fraction must lie in [0.5, 1)")
    n_features = values.shape[2]
    scored = n_features if score_features is None else int(score_features)
    if scored < 1 or scored > n_features:
        raise ValueError("score_features must select leading observation features")

    n_transitions = values.shape[0] - delay_depth
    if n_transitions < 6:
        raise ValueError("trace is too short for the requested delay depth")
    split_target = int(math.floor(train_fraction * (values.shape[0] - 1)))
    n_train = split_target - delay_depth + 1
    n_test = n_transitions - n_train
    if n_train < 3 or n_test < 3:
        raise ValueError("chronological split leaves too few transitions")

    predictors = np.concatenate(
        [
            values[delay_depth - 1 - lag : values.shape[0] - 1 - lag]
            for lag in range(delay_depth)
        ],
        axis=2,
    )
    responses = values[delay_depth:]
    predictor_means = np.mean(predictors[:n_train], axis=0)
    response_means = np.mean(responses[:n_train], axis=0)
    scale_training = values[: split_target + 1]
    scale_means = np.mean(scale_training, axis=0)
    centered_training = scale_training - scale_means[None, :, :]
    feature_scales = np.sqrt(
        np.mean(centered_training * centered_training, axis=(0, 1))
    )
    minimum_scale = np.finfo(float).eps * max(
        1.0, float(np.max(np.abs(values[: n_train + delay_depth])))
    )
    if np.any(feature_scales <= minimum_scale):
        raise ValueError("every fitted feature must vary on the training window")
    predictor_scales = np.tile(feature_scales, delay_depth)

    standardized_predictors = (
        predictors - predictor_means[None, :, :]
    ) / predictor_scales[None, None, :]
    standardized_responses = (responses - response_means[None, :, :]) / feature_scales[
        None, None, :
    ]
    train_predictors = standardized_predictors[:n_train].reshape(
        -1, delay_depth * n_features
    )
    train_responses = standardized_responses[:n_train].reshape(-1, n_features)
    test_predictors = standardized_predictors[n_train:].reshape(
        -1, delay_depth * n_features
    )
    test_responses = standardized_responses[n_train:].reshape(-1, n_features)

    coefficients, _, _, _ = np.linalg.lstsq(
        train_predictors,
        train_responses,
        rcond=None,
    )
    train_prediction = train_predictors @ coefficients
    test_prediction = test_predictors @ coefficients
    score_slice = slice(0, scored)
    train_residual = train_responses[:, score_slice] - train_prediction[:, score_slice]
    test_residual = test_responses[:, score_slice] - test_prediction[:, score_slice]
    raw_test_current = predictors[n_train:, :, :scored]
    persistence = (
        raw_test_current - response_means[None, :, :scored]
    ) / feature_scales[None, None, :scored]
    persistence = persistence.reshape(-1, scored)
    persistence_residual = test_responses[:, score_slice] - persistence
    train_rmse = float(np.sqrt(np.mean(train_residual * train_residual)))
    test_rmse = float(np.sqrt(np.mean(test_residual * test_residual)))
    persistence_rmse = float(
        np.sqrt(np.mean(persistence_residual * persistence_residual))
    )

    companion_size = delay_depth * n_features
    transition = np.zeros((companion_size, companion_size), dtype=float)
    transition[:n_features] = coefficients.T
    if delay_depth > 1:
        transition[n_features:, :-n_features] = np.eye((delay_depth - 1) * n_features)
    return PanelDelayModeFit(
        transition=transition,
        coefficients=np.asarray(coefficients, dtype=float),
        predictor_means=np.asarray(predictor_means, dtype=float),
        response_means=np.asarray(response_means, dtype=float),
        feature_scales=np.asarray(feature_scales, dtype=float),
        eigenvalues=np.asarray(np.linalg.eigvals(transition), dtype=np.complex128),
        design_condition=float(np.linalg.cond(train_predictors)),
        train_score_rmse=train_rmse,
        test_score_rmse=test_rmse,
        test_persistence_rmse=persistence_rmse,
        test_residual_ratio=test_rmse / max(persistence_rmse, np.finfo(float).tiny),
        delay_depth=int(delay_depth),
        score_features=scored,
        train_transitions=n_train * values.shape[1],
        test_transitions=n_test * values.shape[1],
    )


def fit_panel_hankel_audit(
    observations: np.ndarray,
    *,
    delay_depth: int,
    retained_ranks: tuple[int, ...],
    common_max_depth: int | None = None,
    train_fraction: float = 0.6,
    score_features: int | None = None,
) -> PanelHankelAudit:
    """Fit fixed-rank Hankel/DMD models on common chronological windows.

    ``delay_depth`` controls the history represented in each Hankel row.
    ``common_max_depth`` fixes the first response time for every depth in a
    ladder, preventing shallower fits from receiving extra training targets.
    The returned DMD eigenvalues are empirical reduced-state poles; they are
    interpretable only when stable across ranks, depths, segments, and controls.
    """

    values = np.asarray(observations, dtype=float)
    if (
        values.ndim != 3
        or values.shape[0] < 8
        or values.shape[1] < 1
        or values.shape[2] < 1
        or not np.isfinite(values).all()
    ):
        raise ValueError(
            "observations must be finite with shape (time, panel, feature)"
        )
    if (
        isinstance(delay_depth, bool)
        or not isinstance(delay_depth, (int, np.integer))
        or delay_depth < 1
    ):
        raise ValueError("delay_depth must be a positive integer")
    maximum = delay_depth if common_max_depth is None else common_max_depth
    if (
        isinstance(maximum, bool)
        or not isinstance(maximum, (int, np.integer))
        or maximum < delay_depth
    ):
        raise ValueError("common_max_depth must be an integer >= delay_depth")
    ranks = tuple(int(rank) for rank in retained_ranks)
    if (
        not ranks
        or any(rank < 1 for rank in ranks)
        or tuple(sorted(set(ranks))) != ranks
    ):
        raise ValueError("retained_ranks must be unique increasing positive integers")
    if not 0.5 <= train_fraction < 1.0:
        raise ValueError("train_fraction must lie in [0.5, 1)")

    n_features = values.shape[2]
    scored = n_features if score_features is None else int(score_features)
    if scored < 1 or scored > n_features:
        raise ValueError("score_features must select leading observation features")
    split_target = int(math.floor(train_fraction * (values.shape[0] - 1)))
    response_indices = np.arange(maximum, values.shape[0])
    train_mask = response_indices <= split_target
    test_mask = ~train_mask
    if np.count_nonzero(train_mask) < 3 or np.count_nonzero(test_mask) < 3:
        raise ValueError("common delay window leaves too few train or test targets")

    predictors = np.concatenate(
        [
            values[maximum - 1 - lag : values.shape[0] - 1 - lag]
            for lag in range(delay_depth)
        ],
        axis=2,
    )
    next_states = np.concatenate(
        [values[maximum - lag : values.shape[0] - lag] for lag in range(delay_depth)],
        axis=2,
    )
    responses = values[maximum:]
    predictor_means = np.mean(predictors[train_mask], axis=0)
    response_means = np.mean(responses[train_mask], axis=0)
    scale_training = values[: split_target + 1]
    scale_means = np.mean(scale_training, axis=0)
    centered_training = scale_training - scale_means[None, :, :]
    feature_scales = np.sqrt(
        np.mean(centered_training * centered_training, axis=(0, 1))
    )
    minimum_scale = np.finfo(float).eps * max(
        1.0, float(np.max(np.abs(values[: split_target + 1])))
    )
    if np.any(feature_scales <= minimum_scale):
        raise ValueError("every fitted feature must vary on the training window")
    predictor_scales = np.tile(feature_scales, delay_depth)

    standardized_predictors = (
        predictors - predictor_means[None, :, :]
    ) / predictor_scales[None, None, :]
    standardized_next = (next_states - predictor_means[None, :, :]) / predictor_scales[
        None, None, :
    ]
    standardized_responses = (responses - response_means[None, :, :]) / feature_scales[
        None, None, :
    ]
    train_predictors = standardized_predictors[train_mask].reshape(
        -1, delay_depth * n_features
    )
    test_predictors = standardized_predictors[test_mask].reshape(
        -1, delay_depth * n_features
    )
    train_next = standardized_next[train_mask].reshape(-1, delay_depth * n_features)
    train_responses = standardized_responses[train_mask].reshape(-1, n_features)
    test_responses = standardized_responses[test_mask].reshape(-1, n_features)

    left, singular_values, right_t = np.linalg.svd(
        train_predictors, full_matrices=False
    )
    if singular_values.size == 0 or singular_values[0] <= 0.0:
        raise ValueError("training Hankel matrix has no non-zero singular value")
    tolerance = np.finfo(float).eps * max(train_predictors.shape) * singular_values[0]
    available_rank = int(np.count_nonzero(singular_values > tolerance))
    if ranks[-1] > available_rank:
        raise ValueError(
            f"retained rank {ranks[-1]} exceeds numerical rank {available_rank}"
        )

    power = singular_values * singular_values
    probabilities = power / np.sum(power)
    positive = probabilities > 0.0
    entropy_rank = float(
        np.exp(-np.sum(probabilities[positive] * np.log(probabilities[positive])))
    )
    stable_rank = float(np.sum(power) / power[0])
    raw_test_current = predictors[test_mask, :, :scored]
    persistence = (
        raw_test_current - response_means[None, :, :scored]
    ) / feature_scales[None, None, :scored]
    persistence = persistence.reshape(-1, scored)
    persistence_residual = test_responses[:, :scored] - persistence
    persistence_rmse = float(np.sqrt(np.mean(persistence_residual**2)))

    rank_fits = []
    for rank in ranks:
        left_rank = left[:, :rank]
        right_rank = right_t[:rank].T
        inverse_singular = 1.0 / singular_values[:rank]
        coefficients = (
            (right_rank * inverse_singular[None, :]) @ left_rank.T @ train_responses
        )
        train_prediction = train_predictors @ coefficients
        test_prediction = test_predictors @ coefficients
        train_residual = train_responses[:, :scored] - train_prediction[:, :scored]
        test_residual = test_responses[:, :scored] - test_prediction[:, :scored]
        reduced_transition = (
            right_rank.T @ train_next.T @ left_rank @ np.diag(inverse_singular)
        )
        train_rmse = float(np.sqrt(np.mean(train_residual**2)))
        test_rmse = float(np.sqrt(np.mean(test_residual**2)))
        rank_fits.append(
            ReducedRankHankelFit(
                retained_rank=rank,
                eigenvalues=np.asarray(
                    np.linalg.eigvals(reduced_transition), dtype=np.complex128
                ),
                retained_condition=float(
                    singular_values[0] / singular_values[rank - 1]
                ),
                train_score_rmse=train_rmse,
                test_score_rmse=test_rmse,
                test_persistence_rmse=persistence_rmse,
                test_residual_ratio=test_rmse
                / max(persistence_rmse, np.finfo(float).tiny),
            )
        )

    relative_singular = singular_values / singular_values[0]
    return PanelHankelAudit(
        delay_depth=int(delay_depth),
        common_max_depth=int(maximum),
        singular_values=np.asarray(singular_values, dtype=float),
        stable_rank=stable_rank,
        entropy_rank=entropy_rank,
        numerical_rank_1e6=int(np.count_nonzero(relative_singular >= 1e-6)),
        numerical_rank_1e8=int(np.count_nonzero(relative_singular >= 1e-8)),
        rank_fits=tuple(rank_fits),
        train_transitions=int(np.count_nonzero(train_mask) * values.shape[1]),
        test_transitions=int(np.count_nonzero(test_mask) * values.shape[1]),
    )


def fit_isotropic_relative_mode(
    relative_positions: np.ndarray,
    relative_memory_centers: np.ndarray,
    *,
    lag: int = 1,
) -> IsotropicRelativeModeFit:
    r"""Fit one real 2x2 map to the relative visible/memory coordinates.

    Each ambient coordinate supplies another realization of
    ``(x_-, m_-)``. The fit includes an affine intercept but constrains the
    same transition matrix across coordinates, as required by an isotropic
    local reduction. Each coordinate has its own intercept because a fixed
    separation vector gives different coordinate-wise equilibria.
    """

    positions = np.asarray(relative_positions, dtype=float)
    centers = np.asarray(relative_memory_centers, dtype=float)
    if (
        positions.ndim != 2
        or positions.shape != centers.shape
        or positions.shape[0] < 4
        or positions.shape[1] < 1
        or not np.isfinite(positions).all()
        or not np.isfinite(centers).all()
    ):
        raise ValueError("relative traces must be finite arrays of shape (time, dim)")
    if isinstance(lag, bool) or not isinstance(lag, (int, np.integer)) or lag < 1:
        raise ValueError("lag must be a positive integer")
    if positions.shape[0] <= lag + 2:
        raise ValueError("relative traces are too short for the requested lag")

    state = np.stack((positions, centers), axis=-1)
    predictors_by_coordinate = state[:-lag]
    responses_by_coordinate = state[lag:]
    predictor_mean = np.mean(predictors_by_coordinate, axis=0)
    response_mean = np.mean(responses_by_coordinate, axis=0)
    centered_predictors = (
        predictors_by_coordinate - predictor_mean[None, :, :]
    ).reshape(-1, 2)
    centered_responses = (responses_by_coordinate - response_mean[None, :, :]).reshape(
        -1, 2
    )
    coefficients, _, _, _ = np.linalg.lstsq(
        centered_predictors,
        centered_responses,
        rcond=None,
    )
    transition = coefficients.T
    intercept = response_mean - predictor_mean @ transition.T
    predictors = predictors_by_coordinate.reshape(-1, 2)
    responses = responses_by_coordinate.reshape(-1, 2)
    repeated_intercept = np.broadcast_to(
        intercept[None, :, :], responses_by_coordinate.shape
    ).reshape(-1, 2)
    residual = responses - (predictors @ transition.T + repeated_intercept)
    response_scale = float(np.sqrt(np.mean(centered_responses * centered_responses)))
    residual_scale = float(np.sqrt(np.mean(residual * residual)))
    residual_ratio = residual_scale / max(response_scale, np.finfo(float).tiny)
    design_condition = float(np.linalg.cond(centered_predictors))
    eigenvalues = np.linalg.eigvals(transition)
    return IsotropicRelativeModeFit(
        transition=np.asarray(transition, dtype=float),
        intercept=np.asarray(intercept, dtype=float),
        eigenvalues=np.asarray(eigenvalues, dtype=np.complex128),
        design_condition=design_condition,
        residual_ratio=float(residual_ratio),
    )


def relative_mode_phase_coherence(
    relative_positions: np.ndarray,
    relative_memory_centers: np.ndarray,
    fit: IsotropicRelativeModeFit,
    *,
    lag: int = 1,
) -> float:
    """Return phase-increment coherence of a fitted complex relative mode.

    A left eigenvector turns each ambient-coordinate trace into one complex
    modal coordinate. The circular resultant compares observed phase
    increments with the fitted eigenvalue phase and lies in ``[0, 1]``.
    """

    if not fit.is_complex:
        return 0.0
    positions = np.asarray(relative_positions, dtype=float)
    centers = np.asarray(relative_memory_centers, dtype=float)
    if positions.ndim != 2 or positions.shape != centers.shape:
        raise ValueError("relative traces must share shape (time, dim)")
    if isinstance(lag, bool) or not isinstance(lag, (int, np.integer)) or lag < 1:
        raise ValueError("lag must be a positive integer")
    if positions.shape[0] <= lag:
        raise ValueError("relative traces are too short for the requested lag")

    eigenvalues, left_vectors = np.linalg.eig(fit.transition.T)
    candidates = np.flatnonzero(eigenvalues.imag > 1e-8)
    if candidates.size != 1:
        return 0.0
    index = int(candidates[0])
    state = np.stack((positions, centers), axis=-1)
    intercept = np.asarray(fit.intercept, dtype=float)
    if intercept.shape == (2,):
        intercept = np.broadcast_to(intercept, (positions.shape[1], 2))
    if intercept.shape != (positions.shape[1], 2):
        raise ValueError("fit intercepts must match the ambient dimension")
    equilibrium = np.linalg.lstsq(
        np.eye(2) - fit.transition,
        intercept.T,
        rcond=None,
    )[0].T
    state = state - equilibrium[None, :, :]
    modal = np.einsum("tds,s->td", state, left_vectors[:, index])
    earlier = modal[:-lag]
    later = modal[lag:]
    amplitude = np.abs(earlier) * np.abs(later)
    positive = amplitude > 0.0
    if not np.any(positive):
        return 0.0
    threshold = float(np.quantile(amplitude[positive], 0.25))
    selected = positive & (amplitude >= threshold)
    increments = np.angle(later[selected] * np.conjugate(earlier[selected]))
    expected = float(np.angle(eigenvalues[index]))
    return float(abs(np.mean(np.exp(1j * (increments - expected)))))
