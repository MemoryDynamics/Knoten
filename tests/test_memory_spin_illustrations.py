"""Analytic plotting coordinates and an explicitly assumed spinor reference."""

import numpy as np
import pytest

from experiments.current.reference.memory_spin_illustrations import (
    memory_geometry,
    spin_observables,
    spinor,
)


@pytest.mark.parametrize("phase", range(4))
def test_displayed_memory_is_the_analytic_discrete_geometry(phase):
    points, zero = memory_geometry(phase)
    np.testing.assert_array_equal(points[0], points[4])
    steps = points[:-1] - points[1:]
    lengths = np.linalg.norm(steps, axis=1)
    np.testing.assert_allclose(lengths, lengths[0], atol=2e-16)
    weights = 0.01 * 0.99 ** np.arange(4)
    gaussian = np.exp(-np.sum((zero - points[:4]) ** 2, axis=1) / 2)
    np.testing.assert_allclose(
        (weights * gaussian) @ (steps / lengths[:, None]), 0, atol=1e-17
    )
    barycentric = np.linalg.solve(
        np.vstack([points[:4].T, np.ones(4)]), np.append(zero, 1)
    )
    assert np.min(barycentric) > 0


def test_phase_transform_is_discrete_and_improper_not_spinor_rotation():
    first, zero = memory_geometry(0)
    second, next_zero = memory_geometry(1)
    symmetry = np.array([[0, -1, 0], [1, 0, 0], [0, 0, -1]])
    assert np.linalg.det(symmetry) == -1
    np.testing.assert_allclose(second, first @ symmetry.T)
    np.testing.assert_allclose(next_zero, symmetry @ zero)
    with pytest.raises(ValueError):
        memory_geometry(0.5)


@pytest.mark.parametrize("degrees", [0, 90, 180, 270, 360, 540, 720])
def test_spinor_reference_projects_to_ordinary_three_dimensional_spin(degrees):
    theta = np.deg2rad(degrees)
    state = spinor(theta)
    assert np.vdot(state, state).real == pytest.approx(1)
    bloch, spin_p, interference_p = spin_observables(theta)
    np.testing.assert_allclose(bloch, [np.cos(theta), np.sin(theta), 0], atol=4e-16)
    assert spin_p == pytest.approx((1 + np.cos(theta)) / 2, abs=3e-16)
    assert interference_p == pytest.approx((1 + np.cos(theta / 2)) / 2, abs=3e-16)


def test_two_pi_changes_the_spinor_sign_but_not_its_density_matrix():
    initial, full, twice = spinor(0), spinor(2 * np.pi), spinor(4 * np.pi)
    np.testing.assert_allclose(full, -initial, atol=2e-16)
    np.testing.assert_allclose(twice, initial, atol=2e-16)
    np.testing.assert_allclose(
        np.outer(full, full.conjugate()),
        np.outer(initial, initial.conjugate()),
        atol=2e-16,
    )
    assert spin_observables(2 * np.pi)[2] == pytest.approx(0, abs=2e-16)
    assert spin_observables(4 * np.pi)[2] == pytest.approx(1)
