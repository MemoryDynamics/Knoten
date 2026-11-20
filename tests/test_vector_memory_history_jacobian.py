"""Fixed local derivatives of consistent histories; no orbit or gain search."""

from dataclasses import replace

import numpy as np
import pytest

from emergenz_knoten.core import SimulationConfig, memory_horizon
from emergenz_knoten.kernels import double_gaussian_gradient, exponential_memory_weights
from emergenz_knoten.vector_memory import (
    VectorMemoryConfig,
    _lambda_vector,
    _vector_horizon,
    alignment_history_head_jacobian,
    normalize_orientation,
    planar_alignment_normal_row,
    vector_memory_force,
)


def _config(dim=3, deposition="delta"):
    return VectorMemoryConfig(
        scalar=SimulationConfig(
            steps=4,
            dim=dim,
            epsilon=0,
            alpha=0.2,
            max_memory=4,
            deposition_kernel=deposition,
            deposition_sigma=0.3 if deposition == "gaussian" else 0,
            eta=0.3,
            amplitude_att=1.2,
            sigma_att=1.7,
        ),
        lambda_vector=0.3,
        max_vector_memory=5,
        eta_vector=0.4,
        vector_mass=0.8,
        sigma_vector=1.4,
    )


def _history(count, dim):
    ages = np.arange(count)[:, None]
    axes = np.arange(1, dim + 1)[None, :]
    return np.cos(0.43 * (ages + 1) * axes) + 0.07 * ages * axes


def _map(history, config):
    scalar = config.scalar
    hs = memory_horizon(scalar)
    head = history[0].copy()
    if scalar.eta != 0 and scalar.memory_mass != 0:
        head -= scalar.eta * double_gaussian_gradient(
            history[0],
            history[:hs],
            exponential_memory_weights(
                scalar.alpha, hs, memory_mass=scalar.memory_mass
            ),
            sigma_rep=scalar.sigma_rep,
            sigma_att=scalar.sigma_att,
            amplitude_rep=scalar.amplitude_rep,
            amplitude_att=scalar.amplitude_att,
            deposition_kernel=scalar.deposition_kernel,
            deposition_sigma=scalar.deposition_sigma,
        )
    if config.eta_vector != 0 and config.vector_mass != 0:
        hv = _vector_horizon(config)
        directions = np.array(
            [normalize_orientation(step) for step in history[:hv] - history[1 : hv + 1]]
        )
        head += config.eta_vector * vector_memory_force(
            history[0],
            history[:hv],
            directions,
            exponential_memory_weights(
                _lambda_vector(config), hv, memory_mass=config.vector_mass
            ),
            sigma=config.sigma_vector,
        )
    return np.vstack([head, history[:-1]])


def _jvp(blocks, tangent):
    return np.vstack([np.einsum("aij,aj->i", blocks, tangent), tangent[:-1]])


@pytest.mark.parametrize("dim", [2, 3, 5])
@pytest.mark.parametrize("deposition", ["delta", "gaussian", "matched_gaussian"])
def test_all_coordinates_and_rigid_symmetries(dim, deposition):
    config = _config(dim, deposition)
    history = _history(6, dim)
    original = history.copy()
    blocks = alignment_history_head_jacobian(history, config)
    assert blocks.shape == (6, dim, dim)
    np.testing.assert_allclose(blocks.sum(axis=0), np.eye(dim), atol=5e-16)
    step = 1e-6
    for age, axis in np.ndindex(history.shape):
        offset = np.zeros_like(history)
        offset[age, axis] = step
        derivative = (
            _map(history + offset, config) - _map(history - offset, config)
        ) / (2 * step)
        np.testing.assert_allclose(
            _jvp(blocks, offset / step), derivative, atol=4e-10, rtol=3e-7
        )
    for axis in range(1, dim):
        generator = np.zeros((dim, dim))
        generator[0, axis], generator[axis, 0] = 1, -1
        np.testing.assert_allclose(
            _jvp(blocks, history @ generator.T),
            _map(history, config) @ generator.T,
            atol=2e-15,
        )
    np.testing.assert_array_equal(history, original)


@pytest.mark.parametrize("deposition", ["delta", "gaussian", "matched_gaussian"])
def test_planar_projection_agrees_with_existing_normal_row(deposition):
    config = _config(5, deposition)
    planar = _history(6, 2)
    history = np.pad(planar, ((0, 0), (0, 3)))
    blocks = alignment_history_head_jacobian(history, config)
    np.testing.assert_allclose(
        blocks[:, 4, 4], planar_alignment_normal_row(planar, config), atol=3e-16
    )
    np.testing.assert_array_equal(blocks[:, :2, 4], 0)
    np.testing.assert_array_equal(blocks[:, 4, :2], 0)


def test_scalar_horizon_exceeds_vector_horizon():
    config = _config()
    config = replace(
        config, scalar=replace(config.scalar, max_memory=7), max_vector_memory=2
    )
    history = _history(7, 3)
    tangent = _history(7, 3)[:, ::-1]
    blocks = alignment_history_head_jacobian(history, config)
    derivative = (
        _map(history + 1e-6 * tangent, config) - _map(history - 1e-6 * tangent, config)
    ) / 2e-6
    np.testing.assert_allclose(_jvp(blocks, tangent), derivative, atol=3e-10)


@pytest.mark.parametrize("change", [{"eta_vector": 0.0}, {"vector_mass": 0.0}])
def test_passive_vector_needs_no_predecessor_or_nonzero_step(change):
    config = replace(_config(), **change)
    blocks = alignment_history_head_jacobian(np.zeros((4, 3)), config)
    assert blocks.shape == (4, 3, 3)
    np.testing.assert_allclose(blocks.sum(axis=0), np.eye(3), atol=2e-16)


def test_zero_weight_directions_are_not_differentiated():
    config = replace(_config(), lambda_vector=1.0)
    history = np.zeros((6, 3))
    history[0, 0] = 1
    blocks = alignment_history_head_jacobian(history, config)
    assert np.isfinite(blocks).all()
    np.testing.assert_allclose(blocks.sum(axis=0), np.eye(3), atol=2e-16)


def test_scalar_self_cancels_before_evaluating_a_singular_scale():
    config = _config()
    config = replace(
        config,
        eta_vector=0,
        scalar=replace(config.scalar, max_memory=1, sigma_rep=1e-100),
    )
    with np.errstate(all="raise"):
        blocks = alignment_history_head_jacobian(np.zeros((1, 3)), config)
    np.testing.assert_array_equal(blocks, np.eye(3)[None])


@pytest.mark.parametrize(
    "kind", ["short", "long", "dimension", "nan", "infinite", "zero_step"]
)
def test_invalid_history_is_rejected(kind):
    history = _history(6, 3)
    if kind == "short":
        history = history[:-1]
    elif kind == "long":
        history = np.vstack([history, history[-1]])
    elif kind == "dimension":
        history = history[:, :2]
    elif kind == "nan":
        history[2, 1] = np.nan
    elif kind == "infinite":
        history[2, 1] = np.inf
    else:
        history[2] = history[3]
    with pytest.raises(ValueError):
        alignment_history_head_jacobian(history, _config())


@pytest.mark.parametrize("kind", ["noise", "transverse", "invalid_sigma"])
def test_invalid_or_unsupported_config_is_rejected(kind):
    config = _config(2)
    if kind == "noise":
        config = replace(config, scalar=replace(config.scalar, epsilon=0.1))
    elif kind == "transverse":
        config = replace(config, force_mode="transverse_2d")
    else:
        config = replace(config, sigma_vector=0)
    with pytest.raises(ValueError):
        alignment_history_head_jacobian(_history(6, 2), config)


def test_two_step_derivative_uses_actual_intermediate_not_a_proposed_phase():
    config = _config()
    history, tangent = _history(6, 3), _history(6, 3)[:, ::-1]
    actual = _map(history, config)
    first = _jvp(alignment_history_head_jacobian(history, config), tangent)
    composed = _jvp(alignment_history_head_jacobian(actual, config), first)
    derivative = (
        _map(_map(history + 1e-6 * tangent, config), config)
        - _map(_map(history - 1e-6 * tangent, config), config)
    ) / 2e-6
    np.testing.assert_allclose(composed, derivative, atol=4e-10)
    proposed = actual.copy()
    proposed[0] += [0.4, -0.3, 0.2]
    wrong = _jvp(alignment_history_head_jacobian(proposed, config), first)
    assert np.linalg.norm(wrong - composed) > 1e-3
