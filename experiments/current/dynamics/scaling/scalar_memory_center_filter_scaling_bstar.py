"""Run the preregistered nonphysical scalar-memory filter-scaling B-star gate."""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
import hashlib
import itertools
import json
import math
from pathlib import Path
import subprocess
import sys
import time
from typing import Any, Iterable

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def _repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("repository root not found")


ROOT = _repo_root()
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from emergenz_knoten.continuum_limit import (  # noqa: E402
    _path_gradient,
    _weighted_center_and_radius,
)

try:
    from numba import njit
except ImportError:  # pragma: no cover

    def njit(*args: Any, **kwargs: Any) -> Any:
        def wrapper(function: Any) -> Any:
            return function

        return wrapper


DEFAULT_REPORT = Path(
    "reports/dynamics/limits/"
    "scalar_memory_center_filter_scaling_bstar_2026-08-16.md"
)
DEFAULT_SUMMARY = Path(
    "reports/dynamics/limits/"
    "scalar_memory_center_filter_scaling_bstar_2026-08-16.json"
)
DEFAULT_FIGURE = Path(
    "figures/draft/dynamics/limits/"
    "scalar_memory_center_filter_scaling_bstar_2026-08-16.png"
)
PREREGISTRATION = Path(
    "reports/project/meta/preregistration/"
    "scalar_memory_center_filter_scaling_bstar_protocol_2026-08-16.md"
)
A2_RESULT = Path(
    "reports/dynamics/limits/"
    "scalar_memory_center_finite_h_port_a2_2026-08-16.json"
)

TIME_STEP = 0.005
TAIL_EXTENT = 12.0
DIM = 3
DIFFUSION = 1.0e-4
REFERENCE_KAPPA = 4.0
REFERENCE_TAU = 1.0
REFERENCE_MOBILITY = 1.0
REFERENCE_MEMORY_MASS = 1.0

SIGMA_REP = 1.0
SIGMA_ATT = 3.0
AMPLITUDE_REP = 1.0
AMPLITUDE_ATT = 35.0
LOCAL_CURVATURE = (
    AMPLITUDE_ATT / SIGMA_ATT**2 - AMPLITUDE_REP / SIGMA_REP**2
)

FACTOR_LEVELS = (0.5, 2.0)
BASELINE_TUPLE = (1.0, 1.0, 1.0)
HOLDOUT_TUPLE = (2.0, 0.5, 2.0)
FORMATION_SEEDS = (26, 27, 28, 29, 30)
FORMATION_NOISE_BASE = 20_260_826
RESPONSE_NOISE_BASE = 20_260_827
STATE_MATCHED_FORMATION_TIME = 30.0
REFORMED_MEMORY_TIMES = 20.0
PULSE_WIDTH = 0.1
FREE_RESPONSE_TIME = 1.2
IMPULSE_AMPLITUDES = (5.0e-5, 1.0e-4)
AXIS = (1.0, 0.0, 0.0)

MASS_THEORY_TOLERANCE = 2.0e-3
NONLINEAR_MASS_TOLERANCE = 3.0e-2
NONLINEAR_DAMPING_TOLERANCE = 5.0e-2
EXPONENT_TOLERANCE = 8.0e-2
INTERCEPT_TOLERANCE = 5.0e-2
HOLDOUT_COMMON_LAW_TOLERANCE = 5.0e-2
HOLDOUT_FILTER_TOLERANCE = 3.0e-2
RIVAL_ERROR_RATIO_MAXIMUM = 1.0 / 3.0
MATCHED_REFORMED_TOLERANCE = 3.0e-2
MAXIMUM_LOCAL_RADIUS = 3.0e-2
RADIUS_RATIO_MINIMUM = 0.95
RADIUS_RATIO_MAXIMUM = 1.05
MAXIMUM_EVEN_LEAKAGE = 1.0e-2
MAXIMUM_STRENGTH_NONLINEARITY = 1.0e-2
MAXIMUM_FIT_CONDITION = 1.0e6
MAXIMUM_FIT_RESIDUAL = 2.0e-2


@dataclass(frozen=True)
class FilterScalingCase:
    """One independently parameterized finite-memory filter cell."""

    key: str
    tau: float
    input_mobility: float
    memory_mass: float
    time_step: float
    memory_fraction: float
    q: float
    horizon: int
    tail_fraction: float
    stored_memory_mass: float
    eta: float
    restoring_per_update: float
    local_kappa: float
    untruncated_relative_root: float
    deposition_fraction: float
    epsilon: float
    predicted_filter_mass: float
    predicted_discrete_damping: float
    predicted_continuum_damping: float
    predicted_discrete_rate: float
    predicted_continuum_rate: float
    predicted_linear_radius: float


@dataclass(frozen=True)
class InitialState:
    """A complete visible state and finite ordered-memory ring."""

    x: np.ndarray
    history: np.ndarray
    head: int
    source: str
    digest: str


def _positive_finite(name: str, value: float) -> float:
    number = float(value)
    if not math.isfinite(number) or number <= 0.0:
        raise ValueError(f"{name} must be positive and finite")
    return number


def _integer_steps(duration: float) -> int:
    value = _positive_finite("duration", duration) / TIME_STEP
    rounded = int(round(value))
    if not math.isclose(value, rounded, rel_tol=0.0, abs_tol=1.0e-10):
        raise ValueError("duration must be an integer number of time steps")
    return rounded


def _horizon(memory_fraction: float) -> int:
    return max(
        1,
        int(math.ceil(TAIL_EXTENT / memory_fraction - 1.0e-12)),
    )


def fixed_eta() -> float:
    """Return the one frozen coupling used without cellwise retuning."""

    memory_fraction = TIME_STEP / REFERENCE_TAU
    horizon = _horizon(memory_fraction)
    tail = (1.0 - memory_fraction) ** horizon
    stored_mass = REFERENCE_MEMORY_MASS * (1.0 - tail)
    return TIME_STEP * REFERENCE_KAPPA / (stored_mass * LOCAL_CURVATURE)


FIXED_ETA = fixed_eta()


def _number_key(value: float) -> str:
    return f"{value:g}".replace(".", "p")


def make_case(
    *, tau: float, input_mobility: float, memory_mass: float
) -> FilterScalingCase:
    """Construct one B-star cell while keeping eta and the force scale fixed."""

    tau_value = _positive_finite("tau", tau)
    mobility = _positive_finite("input_mobility", input_mobility)
    mass = _positive_finite("memory_mass", memory_mass)
    memory_fraction = TIME_STEP / tau_value
    if memory_fraction >= 1.0:
        raise ValueError("time_step/tau must be smaller than one")
    q = 1.0 - memory_fraction
    horizon = _horizon(memory_fraction)
    tail = q**horizon
    stored_mass = mass * (1.0 - tail)
    restoring = FIXED_ETA * stored_mass * LOCAL_CURVATURE
    if not 0.0 < restoring < 1.0:
        raise ValueError("restoring_per_update must lie in (0, 1)")
    kappa = restoring / TIME_STEP
    root = q * (1.0 - restoring)
    if not 0.0 < root < 1.0:
        raise ValueError("untruncated relative root must lie in (0, 1)")
    predicted_mass = tau_value / mobility
    predicted_discrete_damping = (
        predicted_mass * (1.0 - root) / TIME_STEP
    )
    predicted_continuum_damping = (1.0 + kappa * tau_value) / mobility
    predicted_continuum_rate = kappa + 1.0 / tau_value
    key = (
        f"tau_{_number_key(tau_value)}_"
        f"mu_{_number_key(mobility)}_M0_{_number_key(mass)}"
    )
    return FilterScalingCase(
        key=key,
        tau=tau_value,
        input_mobility=mobility,
        memory_mass=mass,
        time_step=TIME_STEP,
        memory_fraction=memory_fraction,
        q=q,
        horizon=horizon,
        tail_fraction=tail,
        stored_memory_mass=stored_mass,
        eta=FIXED_ETA,
        restoring_per_update=restoring,
        local_kappa=kappa,
        untruncated_relative_root=root,
        deposition_fraction=memory_fraction / (1.0 - tail),
        epsilon=math.sqrt(2.0 * DIFFUSION * TIME_STEP),
        predicted_filter_mass=predicted_mass,
        predicted_discrete_damping=predicted_discrete_damping,
        predicted_continuum_damping=predicted_continuum_damping,
        predicted_discrete_rate=(1.0 - root) / TIME_STEP,
        predicted_continuum_rate=predicted_continuum_rate,
        predicted_linear_radius=math.sqrt(
            DIM * DIFFUSION / predicted_continuum_rate
        ),
    )


def registered_training_cases() -> list[FilterScalingCase]:
    """Return baseline plus seven factorial training corners."""

    cases = [
        make_case(
            tau=REFERENCE_TAU,
            input_mobility=REFERENCE_MOBILITY,
            memory_mass=REFERENCE_MEMORY_MASS,
        )
    ]
    for tau, mobility, mass in itertools.product(
        FACTOR_LEVELS, FACTOR_LEVELS, FACTOR_LEVELS
    ):
        if (tau, mobility, mass) == HOLDOUT_TUPLE:
            continue
        cases.append(
            make_case(
                tau=tau,
                input_mobility=mobility,
                memory_mass=mass,
            )
        )
    return cases


def registered_holdout_case() -> FilterScalingCase:
    """Return the single sealed joint factorial corner."""

    tau, mobility, mass = HOLDOUT_TUPLE
    return make_case(
        tau=tau,
        input_mobility=mobility,
        memory_mass=mass,
    )


def _weights(case: FilterScalingCase) -> np.ndarray:
    ages = np.arange(case.horizon, dtype=float)
    return (
        case.memory_mass
        * case.memory_fraction
        * np.power(case.q, ages)
    )


@njit(cache=True)
def _form_state_with_trace(
    noise: np.ndarray,
    weights: np.ndarray,
    epsilon: float,
    eta: float,
    sigma_rep2: float,
    sigma_att2: float,
    amplitude_rep: float,
    amplitude_att: float,
):
    dim = noise.shape[1]
    horizon = weights.shape[0]
    x = np.zeros(dim, np.float64)
    history = np.zeros((horizon, dim), np.float64)
    trace = np.empty((noise.shape[0], dim), np.float64)
    head = 0
    filled = 0
    for step in range(noise.shape[0]):
        gradient = _path_gradient(
            x,
            history,
            head,
            filled,
            weights,
            sigma_rep2,
            sigma_att2,
            amplitude_rep,
            amplitude_att,
        )
        for coord in range(dim):
            x[coord] += epsilon * noise[step, coord] - eta * gradient[coord]
            trace[step, coord] = x[coord]
        if filled == 0:
            head = 0
        else:
            head = (head - 1) % horizon
        history[head] = x
        if filled < horizon:
            filled += 1
    return x, history, head, filled, trace


@njit(cache=True)
def _paired_scaling_response(
    initial_x: np.ndarray,
    initial_history: np.ndarray,
    initial_head: int,
    weights: np.ndarray,
    noise: np.ndarray,
    impulse_amplitudes: np.ndarray,
    force_profile: np.ndarray,
    axis: np.ndarray,
    memory_fraction: float,
    time_step: float,
    input_mobility: float,
    epsilon: float,
    eta: float,
    sigma_rep2: float,
    sigma_att2: float,
    amplitude_rep: float,
    amplitude_att: float,
):
    n_impulses = impulse_amplitudes.shape[0]
    n_paths = 2 + 2 * n_impulses
    n_steps = noise.shape[0]
    dim = initial_x.shape[0]
    horizon = weights.shape[0]
    retained_mass = np.sum(weights)
    q = 1.0 - memory_fraction
    tail = q**horizon
    deposition_fraction = memory_fraction / (1.0 - tail)

    xs = np.empty((n_paths, dim), np.float64)
    histories = np.empty((n_paths, horizon, dim), np.float64)
    heads = np.empty(n_paths, np.int64)
    centers = np.empty((n_paths, dim), np.float64)
    base_center, initial_radius = _weighted_center_and_radius(
        initial_history,
        initial_head,
        weights,
        retained_mass,
    )
    base_second_moment = initial_radius * initial_radius
    for coord in range(dim):
        base_second_moment += base_center[coord] * base_center[coord]
    second_moments = np.empty(n_paths, np.float64)
    for path in range(n_paths):
        xs[path] = initial_x
        histories[path] = initial_history
        heads[path] = initial_head
        centers[path] = base_center
        second_moments[path] = base_second_moment

    positions = np.empty((n_steps + 1, n_paths, dim), np.float64)
    center_trace = np.empty((n_steps + 1, n_paths, dim), np.float64)
    relative = np.empty((n_steps + 1, n_paths, dim), np.float64)
    radii = np.empty((n_steps + 1, n_paths), np.float64)
    for path in range(n_paths):
        radii[0, path] = initial_radius
        for coord in range(dim):
            positions[0, path, coord] = xs[path, coord]
            center_trace[0, path, coord] = centers[path, coord]
            relative[0, path, coord] = xs[path, coord] - centers[path, coord]

    for step in range(n_steps):
        for path in range(n_paths):
            gradient = _path_gradient(
                xs[path],
                histories[path],
                heads[path],
                horizon,
                weights,
                sigma_rep2,
                sigma_att2,
                amplitude_rep,
                amplitude_att,
            )
            force_scalar = 0.0
            if path >= 2:
                impulse_index = (path - 2) // 2
                sign = 1.0 if (path - 2) % 2 == 0 else -1.0
                force_scalar = (
                    sign
                    * impulse_amplitudes[impulse_index]
                    * force_profile[step]
                )

            oldest_index = (heads[path] + horizon - 1) % horizon
            oldest = histories[path, oldest_index].copy()
            oldest_norm2 = 0.0
            for coord in range(dim):
                oldest_norm2 += oldest[coord] * oldest[coord]
                xs[path, coord] += (
                    epsilon * noise[step, coord]
                    - eta * gradient[coord]
                    + time_step
                    * input_mobility
                    * force_scalar
                    * axis[coord]
                )

            x_norm2 = 0.0
            for coord in range(dim):
                x_norm2 += xs[path, coord] * xs[path, coord]
                centers[path, coord] = (
                    q * centers[path, coord]
                    + deposition_fraction * xs[path, coord]
                    - deposition_fraction * tail * oldest[coord]
                )
            second_moments[path] = (
                q * second_moments[path]
                + deposition_fraction * x_norm2
                - deposition_fraction * tail * oldest_norm2
            )
            center_norm2 = 0.0
            for coord in range(dim):
                center_norm2 += centers[path, coord] * centers[path, coord]
            radii[step + 1, path] = np.sqrt(
                max(second_moments[path] - center_norm2, 0.0)
            )

            heads[path] = (heads[path] - 1) % horizon
            histories[path, heads[path]] = xs[path]
            for coord in range(dim):
                positions[step + 1, path, coord] = xs[path, coord]
                center_trace[step + 1, path, coord] = centers[path, coord]
                relative[step + 1, path, coord] = (
                    xs[path, coord] - centers[path, coord]
                )

    return positions, center_trace, relative, radii


def _state_digest(x: np.ndarray, history: np.ndarray, head: int) -> str:
    digest = hashlib.sha256()
    digest.update(np.ascontiguousarray(x, dtype="<f8").tobytes())
    digest.update(np.ascontiguousarray(history, dtype="<f8").tobytes())
    digest.update(int(head).to_bytes(8, byteorder="little", signed=True))
    return digest.hexdigest()


def _ordered_history(history: np.ndarray, head: int) -> np.ndarray:
    horizon = history.shape[0]
    indices = (int(head) + np.arange(horizon)) % horizon
    return np.asarray(history[indices], dtype=float).copy()


def form_state_matched_archives(
    cases: Iterable[FilterScalingCase],
) -> dict[int, np.ndarray]:
    """Form one baseline path per seed and retain enough history for every cell."""

    case_list = list(cases)
    maximum_horizon = max(case.horizon for case in case_list)
    baseline = make_case(
        tau=REFERENCE_TAU,
        input_mobility=REFERENCE_MOBILITY,
        memory_mass=REFERENCE_MEMORY_MASS,
    )
    n_steps = _integer_steps(STATE_MATCHED_FORMATION_TIME)
    if n_steps < maximum_horizon:
        raise RuntimeError("state-matched formation is shorter than maximum horizon")
    archives: dict[int, np.ndarray] = {}
    for seed in FORMATION_SEEDS:
        noise = np.random.default_rng(
            FORMATION_NOISE_BASE + int(seed)
        ).standard_normal((n_steps, DIM))
        _, _, _, _, trace = _form_state_with_trace(
            noise,
            _weights(baseline),
            baseline.epsilon,
            baseline.eta,
            SIGMA_REP**2,
            SIGMA_ATT**2,
            AMPLITUDE_REP,
            AMPLITUDE_ATT,
        )
        archives[int(seed)] = np.asarray(
            trace[-1 : -maximum_horizon - 1 : -1],
            dtype=float,
        ).copy()
    return archives


def state_matched_initial_state(
    case: FilterScalingCase,
    archive: np.ndarray,
) -> InitialState:
    """Reweight the same newest-first baseline checkpoint for one cell."""

    if archive.ndim != 2 or archive.shape[0] < case.horizon:
        raise ValueError("archive is shorter than the requested cell horizon")
    history = np.asarray(archive[: case.horizon], dtype=float).copy()
    x = np.asarray(history[0], dtype=float).copy()
    return InitialState(
        x=x,
        history=history,
        head=0,
        source="state-matched-baseline-archive",
        digest=_state_digest(x, history, 0),
    )


def reformed_initial_state(
    case: FilterScalingCase,
    *,
    seed: int,
) -> InitialState:
    """Form a stationary finite-memory state under the cell parameters."""

    n_steps = _integer_steps(REFORMED_MEMORY_TIMES * case.tau)
    if n_steps < case.horizon:
        raise RuntimeError("reformed formation is shorter than its horizon")
    noise = np.random.default_rng(
        FORMATION_NOISE_BASE + int(seed)
    ).standard_normal((n_steps, DIM))
    x, history, head, filled, _ = _form_state_with_trace(
        noise,
        _weights(case),
        case.epsilon,
        case.eta,
        SIGMA_REP**2,
        SIGMA_ATT**2,
        AMPLITUDE_REP,
        AMPLITUDE_ATT,
    )
    if int(filled) != case.horizon:
        raise RuntimeError("reformed state did not fill its horizon")
    ordered = _ordered_history(history, int(head))
    return InitialState(
        x=np.asarray(x, dtype=float).copy(),
        history=ordered,
        head=0,
        source="independently-reformed-cell-state",
        digest=_state_digest(x, ordered, 0),
    )


def force_profile() -> np.ndarray:
    """Return the fixed unit-area physical-force rectangle."""

    pulse_steps = _integer_steps(PULSE_WIDTH)
    total_steps = _integer_steps(PULSE_WIDTH + FREE_RESPONSE_TIME)
    profile = np.zeros(total_steps, dtype=float)
    profile[:pulse_steps] = 1.0 / PULSE_WIDTH
    if not math.isclose(
        TIME_STEP * float(np.sum(profile)),
        1.0,
        rel_tol=0.0,
        abs_tol=1.0e-14,
    ):
        raise RuntimeError("force profile does not have unit area")
    return profile


def fit_discrete_impedance(
    center_response: Iterable[float],
    profile: Iterable[float],
    *,
    time_step: float = TIME_STEP,
) -> dict[str, float | int | bool]:
    """Fit the generic recurrence v_n=a*v_(n-1)+b*F_n without using tau or mu."""

    center = np.asarray(list(center_response), dtype=float)
    force = np.asarray(list(profile), dtype=float)
    step = _positive_finite("time_step", time_step)
    if (
        center.ndim != 1
        or force.ndim != 1
        or center.size != force.size + 1
        or force.size < 4
        or not np.isfinite(center).all()
        or not np.isfinite(force).all()
    ):
        raise ValueError("center response and force profile must be finite and align")
    velocity = np.diff(center) / step
    design = np.column_stack((velocity[:-1], force[1:]))
    target = velocity[1:]
    coefficients, _, rank, singular_values = np.linalg.lstsq(
        design,
        target,
        rcond=None,
    )
    a = float(coefficients[0])
    b = float(coefficients[1])
    fitted = design @ coefficients
    target_scale = max(float(np.linalg.norm(target)), 1.0e-30)
    residual = float(np.linalg.norm(target - fitted) / target_scale)
    condition = (
        float(singular_values[0] / singular_values[-1])
        if singular_values.size == 2 and singular_values[-1] > 0.0
        else math.inf
    )
    valid = bool(
        int(rank) == 2
        and 0.0 < a < 1.0
        and b > 0.0
        and math.isfinite(condition)
    )
    mass = step / b if valid else math.nan
    damping = mass * (1.0 - a) / step if valid else math.nan
    return {
        "relative_root": a,
        "force_coefficient": b,
        "inferred_mass": mass,
        "inferred_discrete_damping": damping,
        "inferred_discrete_rate": (1.0 - a) / step if valid else math.nan,
        "normalized_fit_residual": residual,
        "design_condition": condition,
        "fit_rank": int(rank),
        "valid": valid,
    }


def exact_finite_h_response(
    case: FilterScalingCase,
    profile: Iterable[float] | None = None,
) -> dict[str, Any]:
    """Return the exact local finite-H response under the fixed physical force."""

    force = force_profile() if profile is None else np.asarray(list(profile), dtype=float)
    history = np.zeros(case.horizon, dtype=float)
    head = 0
    x = 0.0
    center = 0.0
    centers = np.empty(force.size + 1, dtype=float)
    centers[0] = 0.0
    for step, force_value in enumerate(force):
        x_next = (
            (1.0 - case.restoring_per_update) * x
            + case.restoring_per_update * center
            + TIME_STEP * case.input_mobility * float(force_value)
        )
        oldest = history[(head + case.horizon - 1) % case.horizon]
        center_next = (
            case.q * center
            + case.deposition_fraction * x_next
            - case.deposition_fraction * case.tail_fraction * oldest
        )
        head = (head - 1) % case.horizon
        history[head] = x_next
        x = x_next
        center = center_next
        centers[step + 1] = center
    fit = fit_discrete_impedance(centers, force)
    return {
        "fit": fit,
        "center_response": centers,
        "mass_relative_error_theory": abs(
            float(fit["inferred_mass"]) - case.predicted_filter_mass
        )
        / case.predicted_filter_mass,
        "damping_relative_error_theory": abs(
            float(fit["inferred_discrete_damping"])
            - case.predicted_discrete_damping
        )
        / case.predicted_discrete_damping,
    }


def _normalized_rms_difference(first: np.ndarray, second: np.ndarray) -> float:
    scale = max(
        float(np.sqrt(np.mean(first * first))),
        float(np.sqrt(np.mean(second * second))),
        1.0e-30,
    )
    return float(np.sqrt(np.mean((first - second) ** 2)) / scale)


def run_response_from_state(
    case: FilterScalingCase,
    state: InitialState,
    *,
    seed: int,
) -> dict[str, Any]:
    """Run the fixed mirrored weak-force panel from one complete initial state."""

    profile = force_profile()
    response_noise = np.random.default_rng(
        RESPONSE_NOISE_BASE + int(seed)
    ).standard_normal((profile.size, DIM))
    positions, centers, relative, radii = _paired_scaling_response(
        state.x,
        state.history,
        state.head,
        _weights(case),
        response_noise,
        np.asarray(IMPULSE_AMPLITUDES, dtype=float),
        profile,
        np.asarray(AXIS, dtype=float),
        case.memory_fraction,
        TIME_STEP,
        case.input_mobility,
        case.epsilon,
        case.eta,
        SIGMA_REP**2,
        SIGMA_ATT**2,
        AMPLITUDE_REP,
        AMPLITUDE_ATT,
    )
    fits: list[dict[str, Any]] = []
    center_responses: list[np.ndarray] = []
    relative_responses: list[np.ndarray] = []
    even_maxima: list[float] = []
    for impulse_index, impulse in enumerate(IMPULSE_AMPLITUDES):
        plus = 2 + 2 * impulse_index
        minus = plus + 1
        scale = 2.0 * impulse
        center_response = (centers[:, plus, 0] - centers[:, minus, 0]) / scale
        relative_response = (
            relative[:, plus, 0] - relative[:, minus, 0]
        ) / scale
        position_even = (
            positions[:, plus] + positions[:, minus] - 2.0 * positions[:, 0]
        ) / scale
        center_even = (
            centers[:, plus] + centers[:, minus] - 2.0 * centers[:, 0]
        ) / scale
        relative_even = (
            relative[:, plus] + relative[:, minus] - 2.0 * relative[:, 0]
        ) / scale
        fit = fit_discrete_impedance(center_response, profile)
        fit["impulse_amplitude"] = float(impulse)
        fits.append(fit)
        center_responses.append(center_response)
        relative_responses.append(relative_response)
        even_maxima.append(
            max(
                float(np.max(np.linalg.norm(position_even, axis=1))),
                float(np.max(np.linalg.norm(center_even, axis=1))),
                float(np.max(np.linalg.norm(relative_even, axis=1))),
            )
        )

    control_radius = radii[:, 0]
    forced_radii = radii[:, 2:]
    radius_ratios = forced_radii / control_radius[:, None]
    force_off_residual = max(
        float(np.max(np.abs(positions[:, 0] - positions[:, 1]))),
        float(np.max(np.abs(centers[:, 0] - centers[:, 1]))),
        float(np.max(np.abs(relative[:, 0] - relative[:, 1]))),
        float(np.max(np.abs(radii[:, 0] - radii[:, 1]))),
    )
    return {
        "seed": int(seed),
        "state_source": state.source,
        "state_digest": state.digest,
        "initial_radius": float(control_radius[0]),
        "minimum_radius": float(np.min(radii)),
        "maximum_radius": float(np.max(radii)),
        "minimum_forced_control_radius_ratio": float(np.min(radius_ratios)),
        "maximum_forced_control_radius_ratio": float(np.max(radius_ratios)),
        "force_off_maximum_residual": force_off_residual,
        "maximum_even_leakage": max(even_maxima),
        "strength_nonlinearity_center": _normalized_rms_difference(
            center_responses[0],
            center_responses[1],
        ),
        "strength_nonlinearity_relative": _normalized_rms_difference(
            relative_responses[0],
            relative_responses[1],
        ),
        "fits": fits,
    }


def _aggregate_estimand(
    rows: list[dict[str, Any]],
    exact: dict[str, Any],
) -> dict[str, Any]:
    fits = [fit for row in rows for fit in row["fits"]]
    masses = np.asarray([fit["inferred_mass"] for fit in fits], dtype=float)
    damping = np.asarray(
        [fit["inferred_discrete_damping"] for fit in fits],
        dtype=float,
    )
    seed_masses = [
        float(np.median([fit["inferred_mass"] for fit in row["fits"]]))
        for row in rows
    ]
    exact_mass = float(exact["fit"]["inferred_mass"])
    exact_damping = float(exact["fit"]["inferred_discrete_damping"])
    return {
        "median_inferred_mass": float(np.median(masses)),
        "median_inferred_discrete_damping": float(np.median(damping)),
        "seed_median_masses": seed_masses,
        "mass_median_absolute_deviation": float(
            np.median(np.abs(masses - np.median(masses)))
        ),
        "maximum_mass_relative_error_exact": float(
            np.max(np.abs(masses - exact_mass) / exact_mass)
        ),
        "maximum_damping_relative_error_exact": float(
            np.max(np.abs(damping - exact_damping) / exact_damping)
        ),
        "all_fits_valid": all(bool(fit["valid"]) for fit in fits),
        "maximum_fit_condition": max(
            float(fit["design_condition"]) for fit in fits
        ),
        "maximum_fit_residual": max(
            float(fit["normalized_fit_residual"]) for fit in fits
        ),
        "maximum_initial_radius": max(row["initial_radius"] for row in rows),
        "minimum_radius": min(row["minimum_radius"] for row in rows),
        "maximum_radius": max(row["maximum_radius"] for row in rows),
        "minimum_forced_control_radius_ratio": min(
            row["minimum_forced_control_radius_ratio"] for row in rows
        ),
        "maximum_forced_control_radius_ratio": max(
            row["maximum_forced_control_radius_ratio"] for row in rows
        ),
        "maximum_force_off_residual": max(
            row["force_off_maximum_residual"] for row in rows
        ),
        "maximum_even_leakage": max(
            row["maximum_even_leakage"] for row in rows
        ),
        "maximum_strength_nonlinearity": max(
            max(
                row["strength_nonlinearity_center"],
                row["strength_nonlinearity_relative"],
            )
            for row in rows
        ),
        "rows": rows,
    }


def run_cell(
    case: FilterScalingCase,
    archives: dict[int, np.ndarray],
) -> dict[str, Any]:
    """Run exact, state-matched and reformed estimands for one cell."""

    exact = exact_finite_h_response(case)
    exact_record = {
        "fit": exact["fit"],
        "mass_relative_error_theory": exact["mass_relative_error_theory"],
        "damping_relative_error_theory": exact[
            "damping_relative_error_theory"
        ],
    }
    matched_rows: list[dict[str, Any]] = []
    reformed_rows: list[dict[str, Any]] = []
    for seed in FORMATION_SEEDS:
        matched_state = state_matched_initial_state(
            case,
            archives[int(seed)],
        )
        matched_rows.append(
            run_response_from_state(case, matched_state, seed=int(seed))
        )
        reformed_state = reformed_initial_state(case, seed=int(seed))
        reformed_rows.append(
            run_response_from_state(case, reformed_state, seed=int(seed))
        )
    return {
        "case": asdict(case),
        "exact": exact_record,
        "state_matched": _aggregate_estimand(matched_rows, exact_record),
        "reformed": _aggregate_estimand(reformed_rows, exact_record),
    }


def fit_log_scaling_law(
    cells: Iterable[dict[str, Any]],
    *,
    estimand: str,
) -> dict[str, Any]:
    """Fit one common log-linear mass law across the training cells."""

    rows = list(cells)
    design = np.asarray(
        [
            [
                1.0,
                math.log(row["case"]["tau"]),
                math.log(row["case"]["input_mobility"]),
                math.log(row["case"]["memory_mass"]),
            ]
            for row in rows
        ],
        dtype=float,
    )
    masses = np.asarray(
        [row[estimand]["median_inferred_mass"] for row in rows],
        dtype=float,
    )
    target = np.log(masses)
    coefficients, _, rank, singular_values = np.linalg.lstsq(
        design,
        target,
        rcond=None,
    )
    fitted = design @ coefficients

    filter_prediction = np.asarray(
        [
            row["case"]["tau"] / row["case"]["input_mobility"]
            for row in rows
        ],
        dtype=float,
    )
    constant_prediction = np.ones_like(filter_prediction)
    material_prediction = np.asarray(
        [row["case"]["memory_mass"] for row in rows],
        dtype=float,
    )
    loaded_filter_prediction = filter_prediction * material_prediction

    def log_rmse(prediction: np.ndarray) -> float:
        return float(
            np.sqrt(np.mean((target - np.log(prediction)) ** 2))
        )

    condition = (
        float(singular_values[0] / singular_values[-1])
        if singular_values.size == 4 and singular_values[-1] > 0.0
        else math.inf
    )
    return {
        "estimand": estimand,
        "intercept": float(coefficients[0]),
        "tau_exponent": float(coefficients[1]),
        "mobility_exponent": float(coefficients[2]),
        "memory_mass_exponent": float(coefficients[3]),
        "rank": int(rank),
        "condition": condition,
        "training_log_rmse_common_law": float(
            np.sqrt(np.mean((target - fitted) ** 2))
        ),
        "training_log_rmse_filter": log_rmse(filter_prediction),
        "training_log_rmse_constant": log_rmse(constant_prediction),
        "training_log_rmse_material": log_rmse(material_prediction),
        "training_log_rmse_loaded_filter": log_rmse(
            loaded_filter_prediction
        ),
    }


def common_law_prediction(
    fit: dict[str, Any],
    case: dict[str, Any],
) -> float:
    """Evaluate a fitted common scaling law at one held-out cell."""

    log_mass = (
        fit["intercept"]
        + fit["tau_exponent"] * math.log(case["tau"])
        + fit["mobility_exponent"]
        * math.log(case["input_mobility"])
        + fit["memory_mass_exponent"] * math.log(case["memory_mass"])
    )
    return float(math.exp(log_mass))


def _relative_error(observed: float, expected: float) -> float:
    return abs(float(observed) - float(expected)) / abs(float(expected))


def evaluate_gates(
    training_cells: list[dict[str, Any]],
    holdout: dict[str, Any],
    scaling_fits: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """Apply only the thresholds frozen in the B-star protocol."""

    all_cells = training_cells + [holdout]
    validity_checks: dict[str, bool] = {
        "exact_finite_h_mass": all(
            cell["exact"]["mass_relative_error_theory"]
            <= MASS_THEORY_TOLERANCE
            for cell in all_cells
        ),
        "exact_finite_h_damping": all(
            cell["exact"]["damping_relative_error_theory"]
            <= MASS_THEORY_TOLERANCE
            for cell in all_cells
        ),
    }
    for estimand in ("state_matched", "reformed"):
        values = [cell[estimand] for cell in all_cells]
        validity_checks[f"{estimand}_all_fits_valid"] = all(
            value["all_fits_valid"] for value in values
        )
        validity_checks[f"{estimand}_fit_condition"] = max(
            value["maximum_fit_condition"] for value in values
        ) <= MAXIMUM_FIT_CONDITION
        validity_checks[f"{estimand}_fit_residual"] = max(
            value["maximum_fit_residual"] for value in values
        ) <= MAXIMUM_FIT_RESIDUAL
        validity_checks[f"{estimand}_force_off"] = max(
            value["maximum_force_off_residual"] for value in values
        ) <= 1.0e-14
        validity_checks[f"{estimand}_positive_radii"] = min(
            value["minimum_radius"] for value in values
        ) > 0.0
        validity_checks[f"{estimand}_local_radius"] = max(
            value["maximum_radius"] for value in values
        ) <= MAXIMUM_LOCAL_RADIUS
        validity_checks[f"{estimand}_radius_lower"] = min(
            value["minimum_forced_control_radius_ratio"] for value in values
        ) >= RADIUS_RATIO_MINIMUM
        validity_checks[f"{estimand}_radius_upper"] = max(
            value["maximum_forced_control_radius_ratio"] for value in values
        ) <= RADIUS_RATIO_MAXIMUM
        validity_checks[f"{estimand}_even_leakage"] = max(
            value["maximum_even_leakage"] for value in values
        ) <= MAXIMUM_EVEN_LEAKAGE
        validity_checks[f"{estimand}_strength_linearity"] = max(
            value["maximum_strength_nonlinearity"] for value in values
        ) <= MAXIMUM_STRENGTH_NONLINEARITY
    validity_pass = all(validity_checks.values())

    embedding_checks: dict[str, bool] = {}
    for estimand in ("state_matched", "reformed"):
        embedding_checks[f"{estimand}_mass_exact"] = max(
            cell[estimand]["maximum_mass_relative_error_exact"]
            for cell in all_cells
        ) <= NONLINEAR_MASS_TOLERANCE
        embedding_checks[f"{estimand}_damping_exact"] = max(
            cell[estimand]["maximum_damping_relative_error_exact"]
            for cell in all_cells
        ) <= NONLINEAR_DAMPING_TOLERANCE
    embedding_pass = all(embedding_checks.values())

    scaling_checks: dict[str, bool] = {}
    holdout_metrics: dict[str, Any] = {}
    for estimand, fit in scaling_fits.items():
        observed = float(holdout[estimand]["median_inferred_mass"])
        filter_prediction = float(holdout["case"]["predicted_filter_mass"])
        common_prediction = common_law_prediction(fit, holdout["case"])
        alternatives = {
            "constant": 1.0,
            "material_M0": float(holdout["case"]["memory_mass"]),
            "loaded_filter": (
                filter_prediction * float(holdout["case"]["memory_mass"])
            ),
        }
        filter_log_error = abs(math.log(observed / filter_prediction))
        rival_log_errors = {
            name: abs(math.log(observed / prediction))
            for name, prediction in alternatives.items()
        }
        holdout_metrics[estimand] = {
            "observed_mass": observed,
            "filter_prediction": filter_prediction,
            "common_law_prediction": common_prediction,
            "filter_relative_error": _relative_error(
                observed,
                filter_prediction,
            ),
            "common_law_relative_error": _relative_error(
                observed,
                common_prediction,
            ),
            "filter_log_error": filter_log_error,
            "rival_predictions": alternatives,
            "rival_log_errors": rival_log_errors,
            "filter_to_best_rival_error_ratio": (
                filter_log_error / min(rival_log_errors.values())
            ),
        }
        prefix = estimand
        scaling_checks[f"{prefix}_full_rank"] = fit["rank"] == 4
        scaling_checks[f"{prefix}_intercept"] = (
            abs(fit["intercept"]) <= INTERCEPT_TOLERANCE
        )
        scaling_checks[f"{prefix}_tau_exponent"] = (
            abs(fit["tau_exponent"] - 1.0) <= EXPONENT_TOLERANCE
        )
        scaling_checks[f"{prefix}_mobility_exponent"] = (
            abs(fit["mobility_exponent"] + 1.0) <= EXPONENT_TOLERANCE
        )
        scaling_checks[f"{prefix}_memory_mass_exponent"] = (
            abs(fit["memory_mass_exponent"]) <= EXPONENT_TOLERANCE
        )
        scaling_checks[f"{prefix}_holdout_common_law"] = (
            holdout_metrics[estimand]["common_law_relative_error"]
            <= HOLDOUT_COMMON_LAW_TOLERANCE
        )
        scaling_checks[f"{prefix}_holdout_filter"] = (
            holdout_metrics[estimand]["filter_relative_error"]
            <= HOLDOUT_FILTER_TOLERANCE
        )
        scaling_checks[f"{prefix}_holdout_rivals"] = (
            holdout_metrics[estimand]["filter_to_best_rival_error_ratio"]
            <= RIVAL_ERROR_RATIO_MAXIMUM
        )
    scaling_checks["matched_reformed_all_cells"] = max(
        _relative_error(
            cell["state_matched"]["median_inferred_mass"],
            cell["reformed"]["median_inferred_mass"],
        )
        for cell in all_cells
    ) <= MATCHED_REFORMED_TOLERANCE
    scaling_pass = all(scaling_checks.values())

    if not validity_pass:
        decision = "bstar-regime-change-or-invalid"
    elif not embedding_pass:
        decision = "bstar-nonlinear-embedding-fail"
    elif scaling_pass:
        decision = "bstar-filter-scaling-pass"
    else:
        decision = "bstar-filter-scaling-fail"
    return {
        "validity_checks": validity_checks,
        "embedding_checks": embedding_checks,
        "scaling_checks": scaling_checks,
        "validity_pass": validity_pass,
        "embedding_pass": embedding_pass,
        "scaling_pass": scaling_pass,
        "holdout_metrics": holdout_metrics,
        "decision": decision,
    }


def _git_output(arguments: list[str]) -> str:
    completed = subprocess.run(
        ["git", *arguments],
        cwd=ROOT,
        capture_output=True,
        check=True,
        text=True,
    )
    return completed.stdout.strip()


def _load_a2_dependency() -> dict[str, Any]:
    payload = json.loads((ROOT / A2_RESULT).read_text(encoding="utf-8"))
    if payload.get("decision") != "finite-h-effective-center-port-pass":
        raise RuntimeError("A2 effective-port pass is required before B-star")
    return payload


def run_gate() -> dict[str, Any]:
    """Execute training first and open the registered joint holdout only afterward."""

    start = time.perf_counter()
    revision = _git_output(["rev-parse", "HEAD"])
    pre_run_status = _git_output(["status", "--short"])
    if pre_run_status:
        raise RuntimeError("B-star target run requires a clean working tree")
    a2 = _load_a2_dependency()

    training_cases = registered_training_cases()
    holdout_case = registered_holdout_case()
    all_cases = training_cases + [holdout_case]
    archives = form_state_matched_archives(all_cases)

    training_results = [
        run_cell(case, archives)
        for case in training_cases
    ]
    scaling_fits = {
        estimand: fit_log_scaling_law(
            training_results,
            estimand=estimand,
        )
        for estimand in ("state_matched", "reformed")
    }

    holdout_result = run_cell(holdout_case, archives)
    gates = evaluate_gates(
        training_results,
        holdout_result,
        scaling_fits,
    )
    return {
        "schema": "emergenz-knoten.scalar-memory-center-filter-scaling-bstar",
        "schema_version": 1,
        "generated_utc": datetime.now(UTC).isoformat(),
        "simulation_revision": revision,
        "git_status_before_run": pre_run_status,
        "runtime_seconds": time.perf_counter() - start,
        "preregistration": PREREGISTRATION.as_posix(),
        "a2_dependency": {
            "path": A2_RESULT.as_posix(),
            "decision": a2["decision"],
            "simulation_revision": a2["simulation_revision"],
        },
        "registration": {
            "time_step": TIME_STEP,
            "tail_extent": TAIL_EXTENT,
            "fixed_eta": FIXED_ETA,
            "force_profile": {
                "pulse_width": PULSE_WIDTH,
                "free_response_time": FREE_RESPONSE_TIME,
                "impulse_amplitudes": IMPULSE_AMPLITUDES,
            },
            "factor_levels": FACTOR_LEVELS,
            "baseline_tuple": BASELINE_TUPLE,
            "holdout_tuple": HOLDOUT_TUPLE,
            "formation_seeds": FORMATION_SEEDS,
            "p0_confirmatory_seeds_21_25_opened": False,
            "p0_transfer_holdout_opened": False,
            "s1_target_data_opened": False,
            "physical_gate_b_opened": False,
            "estimands": (
                "state_matched",
                "independently_reformed",
            ),
        },
        "training_cells": training_results,
        "scaling_fits": scaling_fits,
        "holdout_cell": holdout_result,
        "gates": gates,
        "decision": gates["decision"],
        "claim_boundary": {
            "established_if_pass": (
                "the local finite-H nonlinear center filter follows the "
                "system-identification scaling m_filter=tau/mu in the "
                "registered weak-response panel"
            ),
            "not_established": (
                "physical mass, material center of mass, natural microscopic "
                "actuator, additive momentum, SI calibration, or S1 topology"
            ),
            "physical_gate_b": "blocked-gate-a-port-selection",
            "s1_branch": "sealed-no-s1-candidate",
        },
    }


def _fmt(value: float) -> str:
    return f"{float(value):.6g}"


def render_report(payload: dict[str, Any]) -> str:
    gates = payload["gates"]
    lines = [
        "# Scalar-memory center filter scaling B-star",
        "",
        f"Generated: {payload['generated_utc']}.",
        "",
        f"Decision: **{payload['decision']}**.",
        "",
        "This is a nonphysical system-identification branch. The run does not",
        "count as physical Gate B and does not open the S1 branch.",
        "",
        "## Registered cells",
        "",
        "| cell | split | tau | mu | M0 | filter mass | exact finite-H | state-matched | reformed |",
        "|---|:---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    rows = [
        (cell, "train") for cell in payload["training_cells"]
    ] + [(payload["holdout_cell"], "holdout")]
    for cell, split in rows:
        case = cell["case"]
        lines.append(
            "| "
            f"{case['key']} | {split} | {_fmt(case['tau'])} | "
            f"{_fmt(case['input_mobility'])} | "
            f"{_fmt(case['memory_mass'])} | "
            f"{_fmt(case['predicted_filter_mass'])} | "
            f"{_fmt(cell['exact']['fit']['inferred_mass'])} | "
            f"{_fmt(cell['state_matched']['median_inferred_mass'])} | "
            f"{_fmt(cell['reformed']['median_inferred_mass'])} |"
        )
    lines.extend(
        [
            "",
            "The applied physical-force profile, eta and center readout scale",
            "are fixed across cells. M0 changes the local damping because eta",
            "is not retuned; the filter prediction still assigns no M0 factor",
            "to the inertial coefficient.",
            "",
            "## Common training law",
            "",
            "| estimand | intercept | tau exponent | mu exponent | M0 exponent | filter log-RMSE |",
            "|---|---:|---:|---:|---:|---:|",
        ]
    )
    for fit in payload["scaling_fits"].values():
        lines.append(
            "| "
            f"{fit['estimand']} | {_fmt(fit['intercept'])} | "
            f"{_fmt(fit['tau_exponent'])} | "
            f"{_fmt(fit['mobility_exponent'])} | "
            f"{_fmt(fit['memory_mass_exponent'])} | "
            f"{_fmt(fit['training_log_rmse_filter'])} |"
        )
    lines.extend(["", "## Joint holdout", ""])
    for estimand, metric in gates["holdout_metrics"].items():
        lines.append(
            f"- {estimand}: observed mass {_fmt(metric['observed_mass'])}, "
            f"filter prediction {_fmt(metric['filter_prediction'])}, "
            f"relative error {_fmt(metric['filter_relative_error'])}, "
            "filter-to-best-rival log-error ratio "
            f"{_fmt(metric['filter_to_best_rival_error_ratio'])}."
        )
    lines.extend(
        [
            "",
            "## Gate summary",
            "",
            f"- validity: {gates['validity_pass']};",
            f"- nonlinear finite-H embedding: {gates['embedding_pass']};",
            f"- held-out scaling: {gates['scaling_pass']}.",
            "",
            "## Claim boundary",
            "",
            "A pass shows that the registered local nonlinear finite-memory",
            "filter follows m_filter=tau/mu under the engineered effective",
            "center port. It does not identify material mass or a natural",
            "microscopic force recipient. Physical B remains blocked by Gate A,",
            "and D0--D5 remain sealed because no S1 candidate exists.",
            "",
        ]
    )
    return "\n".join(lines)


def render_figure(payload: dict[str, Any], output: Path) -> None:
    rows = payload["training_cells"] + [payload["holdout_cell"]]
    figure, axes = plt.subplots(1, 2, figsize=(10.5, 4.2))
    colors = {"state_matched": "#2563eb", "reformed": "#ea580c"}
    labels = {"state_matched": "state matched", "reformed": "reformed"}
    for estimand in ("state_matched", "reformed"):
        expected = np.asarray(
            [row["case"]["predicted_filter_mass"] for row in rows],
            dtype=float,
        )
        observed = np.asarray(
            [row[estimand]["median_inferred_mass"] for row in rows],
            dtype=float,
        )
        axes[0].scatter(
            expected[:-1],
            observed[:-1],
            color=colors[estimand],
            label=labels[estimand],
            alpha=0.85,
        )
        axes[0].scatter(
            expected[-1],
            observed[-1],
            facecolors="none",
            edgecolors=colors[estimand],
            s=90,
            linewidths=2.0,
        )
        axes[1].plot(
            np.arange(len(rows)),
            observed / expected,
            marker="o",
            color=colors[estimand],
            label=labels[estimand],
        )
    limits = [0.2, 5.0]
    axes[0].plot(limits, limits, color="black", linewidth=1.0, linestyle="--")
    axes[0].set_xscale("log")
    axes[0].set_yscale("log")
    axes[0].set_xlim(limits)
    axes[0].set_ylim(limits)
    axes[0].set_xlabel("registered tau / mu")
    axes[0].set_ylabel("inferred filter mass")
    axes[0].legend(frameon=False)
    axes[0].set_title("Joint holdout is open marker")
    axes[1].axhline(1.0, color="black", linewidth=1.0, linestyle="--")
    axes[1].axvline(len(rows) - 1.5, color="#6b7280", linewidth=1.0)
    axes[1].set_xlabel("training cells, then holdout")
    axes[1].set_ylabel("inferred / filter prediction")
    axes[1].legend(frameon=False)
    axes[1].set_title("No M0 factor in inertial coefficient")
    figure.tight_layout()
    output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output, dpi=180)
    plt.close(figure)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--figure", type=Path, default=DEFAULT_FIGURE)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = run_gate()
    report_path = ROOT / args.report
    summary_path = ROOT / args.summary
    figure_path = ROOT / args.figure
    report_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(render_report(payload), encoding="utf-8")
    summary_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    render_figure(payload, figure_path)
    print(f"Decision: {payload['decision']}")
    print(f"Report: {report_path.relative_to(ROOT)}")
    print(f"Summary: {summary_path.relative_to(ROOT)}")
    print(f"Figure: {figure_path.relative_to(ROOT)}")
    raise SystemExit(
        0 if payload["decision"] == "bstar-filter-scaling-pass" else 1
    )


if __name__ == "__main__":
    main()
