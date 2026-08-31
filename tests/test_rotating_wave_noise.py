from __future__ import annotations

import math

import numpy as np
import pytest

from emergenz_knoten.rotating_wave_noise import (
    brownian_refinement_paths,
    dimensionless_noise_amplitude,
    grid_cell_decision,
    injection_resolution,
    ladder_decision,
    noisy_native_fifo_step,
    resolved_arm_pass,
    visible_orbit_observables,
)
from emergenz_knoten.rotating_wave_stability import (
    circular_history,
    native_fifo_step,
    rotation_matrix,
)


PARAMETERS = {
    "alpha": 0.08,
    "memory_mass": 1.0,
    "eta": 0.11,
    "sigma_rep": 1.0,
    "sigma_att": 3.0,
    "amplitude_rep": 1.0,
    "amplitude_att": 3.5,
}


def test_zero_noise_is_bitwise_native_and_old_slots_are_never_noised() -> None:
    history = circular_history(radius=0.9, theta=0.17, horizon=24)
    native = native_fifo_step(history, **PARAMETERS)
    zero = noisy_native_fifo_step(
        history, epsilon=0.0, noise=np.asarray([1.2, -0.4]), **PARAMETERS
    )
    assert np.array_equal(zero.history, native)
    assert np.array_equal(zero.effective_increment, np.zeros(2))

    noisy = noisy_native_fifo_step(
        history, epsilon=1.0e-4, noise=np.asarray([1.2, -0.4]), **PARAMETERS
    )
    assert np.array_equal(noisy.history[1:], native[1:])
    assert np.array_equal(noisy.effective_increment, noisy.history[0] - native[0])
    assert np.allclose(noisy.intended_increment, [1.2e-4, -4.0e-5])


def test_sub_ulp_innovation_is_reported_unresolved() -> None:
    history = circular_history(radius=0.9, theta=0.17, horizon=24)
    step = noisy_native_fifo_step(
        history, epsilon=1.0e-20, noise=np.ones(2), **PARAMETERS
    )
    resolution = injection_resolution(
        step.intended_increment[None, :], step.effective_increment[None, :]
    )
    assert resolution["classification"] == "unresolved"
    assert resolution["nonzero_fraction"] == 0.0


def test_noise_step_is_rotation_and_reflection_covariant() -> None:
    history = circular_history(radius=0.9, theta=0.17, horizon=24)
    noise = np.asarray([0.7, -0.2])
    rotation = rotation_matrix(0.43)
    base = noisy_native_fifo_step(
        history, epsilon=2.0e-5, noise=noise, **PARAMETERS
    )
    rotated = noisy_native_fifo_step(
        history @ rotation.T,
        epsilon=2.0e-5,
        noise=noise @ rotation.T,
        **PARAMETERS,
    )
    assert np.allclose(rotated.history, base.history @ rotation.T, atol=2e-16)

    reflection = np.diag([1.0, -1.0])
    mirrored = noisy_native_fifo_step(
        history @ reflection.T,
        epsilon=2.0e-5,
        noise=noise @ reflection.T,
        **PARAMETERS,
    )
    assert np.allclose(mirrored.history, base.history @ reflection.T, atol=2e-16)


def test_brownian_refinement_is_exact_and_reproducible() -> None:
    fine, coarse = brownian_refinement_paths(2026083101, fine_steps=10)
    repeated_fine, repeated_coarse = brownian_refinement_paths(
        2026083101, fine_steps=10
    )
    assert np.array_equal(fine, repeated_fine)
    assert np.array_equal(coarse, repeated_coarse)
    assert np.array_equal(coarse, (fine[0::2] + fine[1::2]) / math.sqrt(2.0))


def test_common_chi_maps_to_common_dimensionless_diffusion() -> None:
    chi = 1.0e-7
    epsilon_a = dimensionless_noise_amplitude(chi=chi, radius=0.94, alpha=0.01)
    epsilon_l3 = dimensionless_noise_amplitude(
        chi=chi, radius=0.95, alpha=0.005
    )
    assert epsilon_a**2 / (2.0 * 0.01 * 0.94**2) == pytest.approx(chi**2 / 2)
    assert epsilon_l3**2 / (2.0 * 0.005 * 0.95**2) == pytest.approx(
        chi**2 / 2
    )


def test_prepared_circle_edge_phase_recovers_theta() -> None:
    history = circular_history(radius=0.9, theta=0.17, horizon=24)
    observed = visible_orbit_observables(
        history, alpha=0.08, memory_mass=1.0, target_theta=0.17
    )
    assert observed["phase_increment"] == pytest.approx(0.17)
    assert observed["wrapped_phase_error"] == pytest.approx(0.0, abs=1e-15)
    assert observed["positive_chirality"] is True


def test_resolution_threshold_equalities_and_precedence() -> None:
    wanted = np.ones(10)
    unresolved = np.zeros(10)
    unresolved[0] = 1.0
    assert injection_resolution(wanted, unresolved)["classification"] == "unresolved"

    resolved = np.zeros(10)
    resolved[:5] = math.sqrt(2.0) / 2.0
    assert injection_resolution(wanted, resolved)["classification"] == "resolved"

    partial = np.zeros(10)
    partial[:4] = 1.0
    assert (
        injection_resolution(wanted, partial)["classification"]
        == "partially-resolved"
    )


def test_arm_grid_and_ladder_decisions_are_fail_closed() -> None:
    passing = {
        "completed": True,
        "finite": True,
        "maximum_d0_fraction": 0.10,
        "late_rms_d0_fraction": 0.05,
        "maximum_radius_relative_error": 0.05,
        "late_rms_phase_error_over_theta": 0.20,
        "positive_chirality_fraction": 0.99,
        "maximum_pair_growth": 10.0,
        "final_pair_ratio": 0.1,
        "stopped": False,
    }
    assert resolved_arm_pass(passing)
    failing = dict(passing, maximum_d0_fraction=0.1000001)
    assert not resolved_arm_pass(failing)
    assert grid_cell_decision([("resolved", True)] * 6) == "all-cell-stable"
    assert grid_cell_decision([("resolved", True), ("resolved", False)]) == "stress-fail"
    assert grid_cell_decision([("resolved", True), ("unresolved", True)]) == "inconclusive"
    assert (
        ladder_decision(
            ["inconclusive", "all-cell-stable", "all-cell-stable", "all-cell-stable", "stress-fail"]
        )
        == "n0-noise-stability-window-bracketed"
    )
    assert (
        ladder_decision(["all-cell-stable", "stress-fail", "all-cell-stable"])
        == "n0-inconclusive"
    )
    assert ladder_decision(["stress-fail"] * 3) == "n0-noise-robustness-fail"


def test_module_contains_no_registered_target_runner() -> None:
    import emergenz_knoten.rotating_wave_noise as module

    assert not hasattr(module, "run_registered_noise_stress")

