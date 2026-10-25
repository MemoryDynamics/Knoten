"""Fixed finite-time shape probes, not a spectral or nonlinear certificate."""

from __future__ import annotations

import numpy as np

from .kernels import double_gaussian_gradient
from .rotating_wave_stability import circular_history, finite_memory_weights


ANGLES_DEGREES = (0, 30, 45, 60, 90)
RELATIVE_AMPLITUDE = 1e-5
STEPS = 2000
SAMPLE_EVERY = 10
PROBE_SCOPE = "float64-fixed-pattern-finite-time-shape-only"


def shape_distance(first: np.ndarray, second: np.ndarray) -> float:
    """RMS distance after translation and proper rotation, keeping age labels."""
    left = first - first.mean(axis=0)
    right = second - second.mean(axis=0)
    u, _, vh = np.linalg.svd(left.T @ right)
    if np.linalg.det(u @ vh) < 0:
        u[:, -1] *= -1
    residual = left @ (u @ vh) - right
    return float(np.sqrt(np.mean(np.sum(residual**2, axis=1))))


def _unit_form(raw: np.ndarray, symmetries: np.ndarray) -> np.ndarray:
    if np.linalg.matrix_rank(symmetries) != symmetries.shape[1]:
        raise ValueError("degenerate symmetry basis")
    q, _ = np.linalg.qr(symmetries, mode="reduced")
    form = raw - q @ (q.T @ raw)
    norm = np.linalg.norm(form)
    if norm <= 1e-12 * max(1.0, np.linalg.norm(raw)):
        raise ValueError("degenerate form pattern")
    return form / norm


def form_directions(history: np.ndarray, theta: float) -> tuple[np.ndarray, np.ndarray]:
    """Unit-RMS planar/normal patterns orthogonal to rigid symmetry tangents."""
    count = len(history)
    phase = np.arange(count) * theta
    envelope = np.cos(2 * phase) + 0.3 * np.sin(3 * phase)
    radial = np.column_stack((np.cos(phase), -np.sin(phase)))
    translations = np.tile(np.eye(2), (count, 1))
    rotation = np.column_stack((-history[:, 1], history[:, 0])).ravel()
    planar = np.zeros_like(history)
    planar[:, :2] = _unit_form(
        (envelope[:, None] * radial).ravel(),
        np.column_stack((translations, rotation)),
    ).reshape(count, 2) * np.sqrt(count)
    normal = np.zeros_like(history)
    normal[:, 2] = _unit_form(
        envelope, np.column_stack((np.ones(count), history[:, :2]))
    ) * np.sqrt(count)
    return planar, normal


def mixed_direction(planar: np.ndarray, normal: np.ndarray, angle: int) -> np.ndarray:
    """Angle in the full unweighted history norm, not at each history node."""
    if angle not in ANGLES_DEGREES:
        raise ValueError("unregistered perturbation angle")
    if angle == 0:
        return planar.copy()
    if angle == 90:
        return normal.copy()
    radians = np.deg2rad(angle)
    return np.cos(radians) * planar + np.sin(radians) * normal


def _native_step(
    history: np.ndarray, weights: np.ndarray, eta: float, kernel: dict
) -> np.ndarray:
    gradient = double_gaussian_gradient(history[0], history, weights, **kernel)
    result = np.empty_like(history)
    result[0] = history[0] - eta * gradient
    result[1:] = history[:-1]
    if not np.isfinite(result).all():
        raise FloatingPointError("nonfinite FIFO state")
    return result


def describe_window(baseline_max: float, arms: list[dict]) -> str:
    """Predeclared descriptive thresholds, never an asymptotic stability gate."""
    if baseline_max >= 0.01 * min(arm["initial_distance"] for arm in arms):
        return "unresolved-baseline-drift"
    ratios = [arm["final_ratio"] for arm in arms]
    if any(ratio > 1.2 for ratio in ratios):
        return "growth-over-registered-window"
    if all(ratio < 0.8 for ratio in ratios):
        return "contraction-over-registered-window"
    return "unresolved-over-registered-window"


def run_oblique_probe(
    *,
    radius: float,
    theta: float,
    parameters: dict,
    steps: int = STEPS,
    sample_every: int = SAMPLE_EVERY,
) -> dict:
    """Run all fixed angles/signs once; small horizons/windows are for tests."""
    if (
        type(steps) is not int
        or type(sample_every) is not int
        or min(steps, sample_every) < 1
    ):
        raise ValueError("positive integer step and sampling counts required")
    horizon = parameters["horizon"]
    history = np.column_stack(
        (
            circular_history(radius=radius, theta=theta, horizon=horizon),
            np.zeros(horizon),
        )
    )
    planar, normal = form_directions(history, theta)
    alpha = float(parameters["alpha"])
    weights = finite_memory_weights(
        alpha=alpha, horizon=horizon, memory_mass=float(parameters["memory_mass"])
    )
    eta = float(parameters["eta"])
    kernel = {
        key: float(parameters[key])
        for key in ("sigma_rep", "sigma_att", "amplitude_rep", "amplitude_att")
    }
    amplitude = RELATIVE_AMPLITUDE * radius
    states = []
    arms = []
    for angle in ANGLES_DEGREES:
        direction = mixed_direction(planar, normal, angle)
        for sign in (-1, 1):
            states.append(history + sign * amplitude * direction)
            arms.append({"angle_degrees": angle, "sign": sign, "distances": []})
    baseline = history.copy()
    baseline_distances = []
    sample_steps = []
    with np.errstate(over="raise", invalid="raise", divide="raise"):
        for step in range(steps + 1):
            if step % sample_every == 0 or step == steps:
                sample_steps.append(step)
                baseline_distances.append(shape_distance(baseline, history))
                for arm, state in zip(arms, states, strict=True):
                    arm["distances"].append(shape_distance(state, baseline))
            if step < steps:
                baseline = _native_step(baseline, weights, eta, kernel)
                states = [_native_step(state, weights, eta, kernel) for state in states]
    for arm in arms:
        initial = arm["distances"][0]
        if not np.isfinite(initial) or initial <= 1e-12 * radius:
            raise FloatingPointError(
                "initial shape perturbation is numerically unresolved"
            )
        arm.update(
            initial_distance=initial,
            final_ratio=arm["distances"][-1] / initial,
            sampled_peak_ratio=max(arm["distances"]) / initial,
        )
    result = {
        "schema": "fifo-oblique-probe-v1",
        "scope": PROBE_SCOPE,
        "arithmetic": "float64",
        "numpy": np.__version__,
        "parameters": parameters,
        "radius": radius,
        "theta": theta,
        "settings": {
            "angles_degrees": list(ANGLES_DEGREES),
            "signs": [-1, 1],
            "relative_amplitude": RELATIVE_AMPLITUDE,
            "steps": steps,
            "sample_every": sample_every,
            "scaled_duration_alpha_n": alpha * steps,
        },
        "sample_steps": sample_steps,
        "baseline_distances": baseline_distances,
        "arms": arms,
        "decision": describe_window(max(baseline_distances), arms),
        "claim_boundary": "One spatial pattern and amplitude; sampled transients and finite-window shape change only. No all-mode, asymptotic, basin, lifetime or topology certificate.",
    }
    return result
