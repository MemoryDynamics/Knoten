"""Local four-cycle diagnostics and a sufficient interval instability test.

No target is selected or evaluated on import. A passed product test is not a
stability certificate; numerical eigenvalues remain illustrative only.
"""

from __future__ import annotations

from dataclasses import asdict
from fractions import Fraction

import numpy as np
from mpmath import iv, libmp

from .core import SimulationConfig, memory_horizon
from .kernels import double_gaussian_gradient, exponential_memory_weights
from .rotating_wave_interval import _interval_record, _strictly_positive
from .vector_memory import (
    VectorMemoryConfig,
    _lambda_vector,
    _validate_vector_config,
    _vector_horizon,
    alignment_history_head_jacobian,
    normalize_orientation,
    vector_gaussian_field,
)


PRECISION_DPS = 80
DIAGNOSTIC_TOLERANCE = 1e-9
SCHEMA = "flat-memory-local-stability-v1"
CERTIFIED = "form-instability-certified"
UNRESOLVED = "inconclusive"


def family_parameters(inputs: dict) -> tuple[Fraction, ...]:
    if type(inputs) is not dict or set(inputs) != {"f", "g", "q"}:
        raise ValueError("exactly f,g,q are required")
    if any(type(value) is not str or len(value) > 64 for value in inputs.values()):
        raise ValueError("short exact rational strings required")
    f, g, q = (Fraction(inputs[key]) for key in ("f", "g", "q"))
    if not (0 < f < g < 1 and 0 < q < 1 and g**4 > f**3 and g**2 < f):
        raise ValueError("inputs are outside the proved positive flat family")
    s = q * g * (g - f * q) / (f * (1 - g * q))
    delta = s**2 * (1 - g * q) - q**2 * (f - g * q)
    if not (0 < s < q and delta > 0):
        raise ValueError("positive-family algebra inconsistent")
    b = 1 / delta
    return f, g, q, s, b, b * (1 - g * q) / s


def form_product(b, s, g, q, radial, height):
    """Exact formula; arguments may be rationals or outward-rounded intervals."""
    gamma = 4 * height / (2 * radial + 4 * height)
    return (
        b**3
        * q**6
        * g**2
        * (s**2 * (1 - g * q) * (gamma - 4 * height) - 4 * q**3 * g * height)
    )


def classify_product(enclosure) -> str:
    lower, upper = enclosure._mpi_
    if lower[3] < 0 or upper[3] < 0:
        raise FloatingPointError("nonfinite product enclosure")
    outside = libmp.mpf_gt(lower, libmp.fone) or libmp.mpf_lt(upper, libmp.fnone)
    return CERTIFIED if outside else UNRESOLVED


def product_certificate(inputs: dict) -> dict:
    parameters = family_parameters(inputs)
    previous = iv.dps
    iv.dps = PRECISION_DPS
    try:
        f, g, q, s, b, _ = (
            iv.mpf(value.numerator) / iv.mpf(value.denominator) for value in parameters
        )
        radial, height = -iv.log(f) / 2, iv.log(f / g**2) / 4
        coefficient = form_product(b, s, g, q, radial, height)
        margin = 2 * height * radial / (radial + 4 * height) + iv.log(q)
        inside = _strictly_positive(margin)
        return {
            "inputs": dict(inputs),
            "precision_dps": PRECISION_DPS,
            "trust_basis": "analytic orbit and quotient identities; mpmath.iv",
            "form_product": _interval_record(coefficient, PRECISION_DPS),
            "interior_margin": _interval_record(margin, PRECISION_DPS),
            "interior_certified": inside,
            "decision": classify_product(coefficient) if inside else UNRESOLVED,
        }
    finally:
        iv.dps = previous


def build_history(inputs: dict) -> tuple[np.ndarray, np.ndarray, VectorMemoryConfig]:
    f, g, q, s, b, c_one = map(float, family_parameters(inputs))
    radius, height = np.sqrt(-np.log(f) / 2), np.sqrt(np.log(f / g**2) / 4)
    length = np.sqrt(2 * radius**2 + 4 * height**2)
    history = np.array(
        [
            [radius, 0, height],
            [0, -radius, -height],
            [-radius, 0, height],
            [0, radius, -height],
            [radius, 0, height],
        ]
    )
    symmetry = np.array([[0, -1, 0], [1, 0, 0], [0, 0, -1]])
    config = VectorMemoryConfig(
        scalar=SimulationConfig(
            steps=4,
            dim=3,
            epsilon=0,
            alpha=1 - s,
            memory_factor=4,
            max_memory=4,
            memory_mass=1,
            amplitude_rep=0,
            amplitude_att=1,
            sigma_rep=1,
            sigma_att=1,
            eta=c_one / ((1 - s) * g),
        ),
        lambda_vector=1 - q,
        vector_mass=1,
        eta_vector=float(b * length / (1 - q)),
        sigma_vector=1,
        vector_memory_factor=4,
        max_vector_memory=4,
    )
    return history, symmetry, config


def _native_map(history, config):
    scalar = config.scalar
    directions = np.array(
        [normalize_orientation(step) for step in history[:-1] - history[1:]]
    )
    gradient = double_gaussian_gradient(
        history[0],
        history[:4],
        exponential_memory_weights(scalar.alpha, 4, memory_mass=scalar.memory_mass),
        sigma_rep=scalar.sigma_rep,
        sigma_att=scalar.sigma_att,
        amplitude_rep=scalar.amplitude_rep,
        amplitude_att=scalar.amplitude_att,
        deposition_kernel=scalar.deposition_kernel,
        deposition_sigma=scalar.deposition_sigma,
    )
    field = vector_gaussian_field(
        history[0],
        history[:4],
        directions,
        exponential_memory_weights(
            _lambda_vector(config), 4, memory_mass=config.vector_mass
        ),
        sigma=config.sigma_vector,
    )
    head = history[0] - scalar.eta * gradient + config.eta_vector * field
    result = np.vstack([head, history[:-1]])
    if not np.isfinite(result).all():
        raise FloatingPointError("nonfinite local history map")
    return result


def _full_jacobian(history, config):
    blocks = alignment_history_head_jacobian(history, config)
    matrix = np.zeros((15, 15))
    matrix[:3] = np.concatenate(blocks, axis=1)
    matrix[3:, :-3] = np.eye(12)
    return matrix


def history_diagnostics(history, symmetry, config) -> dict:
    """Four local composition checks, not a trajectory or a stable verdict."""
    _validate_vector_config(config)
    history, symmetry = (
        np.asarray(history, dtype=float),
        np.asarray(symmetry, dtype=float),
    )
    if (
        history.shape != (5, 3)
        or symmetry.shape != (3, 3)
        or not np.isfinite(history).all()
        or not np.isfinite(symmetry).all()
        or config.scalar.dim != 3
        or memory_horizon(config.scalar) != 4
        or _vector_horizon(config) != 4
        or config.force_mode != "alignment"
        or config.scalar.epsilon != 0
        or config.eta_vector == 0
        or config.vector_mass == 0
    ):
        raise ValueError("active deterministic 3D H_s=H_v=4 history required")
    if not (
        np.allclose(symmetry.T @ symmetry, np.eye(3), atol=1e-14, rtol=0)
        and np.allclose(
            np.linalg.matrix_power(symmetry, 4), np.eye(3), atol=1e-14, rtol=0
        )
        and np.isclose(np.linalg.det(symmetry), -1, atol=1e-14, rtol=0)
        and np.isclose(np.trace(symmetry), -1, atol=1e-14, rtol=0)
    ):
        raise ValueError("improper quarter-turn required")
    scale = max(1.0, float(np.linalg.norm(history)))
    residual = 0.0
    for phase in range(4):
        state = history @ np.linalg.matrix_power(symmetry, phase).T
        residual = max(
            residual,
            float(np.max(np.abs(_native_map(state, config) - state @ symmetry.T)))
            / scale,
        )
    if not np.isfinite(residual) or residual > DIAGNOSTIC_TOLERANCE:
        return {
            "checks_passed": False,
            "reason": "orbit-residual",
            "orbit_residual": residual,
        }
    matrix = np.kron(np.eye(5), symmetry.T) @ _full_jacobian(history, config)
    columns = [np.tile(axis, 5) for axis in np.eye(3)]
    for first, second in [(0, 1), (0, 2), (1, 2)]:
        generator = np.zeros((3, 3))
        generator[first, second], generator[second, first] = 1, -1
        columns.append((history @ generator.T).ravel())
    redundant = np.zeros_like(history)
    redundant[-1] = history[-2] - history[-1]
    columns.append(redundant.ravel())
    basis, triangular = np.linalg.qr(np.column_stack(columns), mode="complete")
    if np.min(np.abs(np.diag(triangular[:7]))) <= 1e-12 * scale:
        return {"checks_passed": False, "reason": "degenerate-symmetry-basis"}
    transformed = basis.T @ matrix @ basis
    quotient = transformed[7:, 7:]
    state, actual_return = history.copy(), np.eye(15)
    for _ in range(4):
        actual_return = _full_jacobian(state, config) @ actual_return
        state = _native_map(state, config)
    matrix_scale = max(1.0, float(np.linalg.norm(matrix)))
    errors = {
        "orbit_residual": residual,
        "invariant_subspace_residual": float(np.max(np.abs(transformed[7:, :7])))
        / matrix_scale,
        "return_residual": float(
            np.max(np.abs(actual_return - np.linalg.matrix_power(matrix, 4)))
        )
        / max(1.0, float(np.linalg.norm(actual_return))),
        "form_trace_residual": abs(float(np.trace(quotient) - np.trace(matrix)))
        / matrix_scale,
    }
    if not all(
        np.isfinite(value) and value <= DIAGNOSTIC_TOLERANCE
        for value in errors.values()
    ):
        return {"checks_passed": False, "reason": "local-consistency", "errors": errors}
    eigenvalues = np.linalg.eigvals(quotient)
    if not np.isfinite(eigenvalues).all():
        raise FloatingPointError("nonfinite diagnostic eigenvalues")
    return {
        "checks_passed": True,
        "errors": errors,
        "arithmetic": "float64-diagnostic-only",
        "reduced_full_matrix": matrix.tolist(),
        "form_quotient": quotient.tolist(),
        "form_product_approximate": float(np.linalg.det(quotient)),
        "form_eigenvalues_approximate": [
            [float(value.real), float(value.imag)] for value in eigenvalues
        ],
        "spectral_radius_approximate": float(np.max(np.abs(eigenvalues))),
    }


def evaluate(inputs: dict) -> dict:
    certificate = product_certificate(inputs)
    history, symmetry, config = build_history(inputs)
    diagnostics = history_diagnostics(history, symmetry, config)
    consistent = diagnostics["checks_passed"] is True
    if consistent:
        midpoint = float(certificate["form_product"]["midpoint"])
        consistent = abs(
            diagnostics["form_product_approximate"] - midpoint
        ) <= DIAGNOSTIC_TOLERANCE * max(1.0, abs(midpoint))
    return {
        "schema": SCHEMA,
        "inputs": dict(inputs),
        "history": history.tolist(),
        "symmetry": symmetry.tolist(),
        "config": asdict(config),
        "scope": "analytic-real-parameter-orbit; float64 implementation diagnostics only",
        "certificate": certificate,
        "diagnostics": diagnostics,
        "method_consistent": bool(consistent),
        "decision": certificate["decision"] if consistent else "method-inconsistent",
        "claim_boundary": "Local deterministic shape instability only. No stable verdict from a passed product test or floating-point roots; no nonlinear fate, formation, lifetime, charge or particle identification.",
    }
