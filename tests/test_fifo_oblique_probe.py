"""Small target-free controls; never evaluate the registered H=1200 anchor."""

import numpy as np
import pytest

from emergenz_knoten import fifo_oblique_probe as probe
from emergenz_knoten.rotating_wave_stability import (
    circular_history,
    finite_memory_weights,
    native_fifo_step,
)


PARAMETERS = dict(
    alpha=0.13,
    horizon=17,
    memory_mass=1.0,
    eta=0.15,
    sigma_rep=1.0,
    sigma_att=2.0,
    amplitude_rep=1.0,
    amplitude_att=0.7,
)
KERNEL = {
    key: PARAMETERS[key]
    for key in ("sigma_rep", "sigma_att", "amplitude_rep", "amplitude_att")
}


def history():
    return np.column_stack(
        (circular_history(radius=1.2, theta=0.31, horizon=17), np.zeros(17))
    )


def test_alignment_removes_translation_and_proper_rotation_not_reflection():
    points = np.random.default_rng(923).normal(size=(17, 3))
    rotation, _ = np.linalg.qr(np.random.default_rng(19).normal(size=(3, 3)))
    assert np.linalg.det(rotation) > 0
    assert probe.shape_distance(points @ rotation + [2, 4, -7], points) < 1e-14
    assert probe.shape_distance(points * [-1, 1, 1], points) > 0.1


@pytest.mark.parametrize("angle", probe.ANGLES_DEGREES)
def test_directions_have_registered_norm_angle_and_remove_all_rigid_tangents(angle):
    h = history()
    p, n = probe.form_directions(h, 0.31)
    d = probe.mixed_direction(p, n, angle)
    assert np.mean(np.sum(d**2, axis=1)) == pytest.approx(1.0)
    assert np.linalg.norm(d[:, 2]) / np.linalg.norm(d) == pytest.approx(
        np.sin(np.deg2rad(angle)), abs=1e-14
    )
    np.testing.assert_allclose(d.sum(axis=0), 0, atol=1e-13)
    np.testing.assert_allclose(np.cross(h, d).sum(axis=0), 0, atol=1e-13)
    if angle == 0:
        assert np.count_nonzero(d[:, 2]) == 0
    if angle == 90:
        assert np.count_nonzero(d[:, :2]) == 0
    assert probe.shape_distance(h + 1e-6 * d, h) == pytest.approx(1e-6, rel=1e-8)


def test_native_3d_step_agrees_with_existing_planar_update():
    h = history()
    w = finite_memory_weights(alpha=0.13, horizon=17, memory_mass=1.0)
    actual = probe._native_step(h, w, 0.15, KERNEL)
    expected = native_fifo_step(
        h[:, :2], **{k: v for k, v in PARAMETERS.items() if k != "horizon"}
    )
    np.testing.assert_allclose(actual[:, :2], expected, atol=1e-15)
    assert np.count_nonzero(actual[:, 2]) == 0


def test_oblique_first_order_action_is_sum_of_planar_and_normal_actions():
    h = history()
    p, n = probe.form_directions(h, 0.31)
    w = finite_memory_weights(alpha=0.13, horizon=17, memory_mass=1.0)

    def action(direction):
        epsilon = 1e-5
        return (
            probe._native_step(h + epsilon * direction, w, 0.15, KERNEL)
            - probe._native_step(h - epsilon * direction, w, 0.15, KERNEL)
        ) / (2 * epsilon)

    planar_action, normal_action = action(p), action(n)
    np.testing.assert_allclose(planar_action[:, 2], 0, atol=1e-12)
    np.testing.assert_allclose(normal_action[:, :2], 0, atol=1e-12)
    for angle in (30, 45, 60):
        a = np.deg2rad(angle)
        np.testing.assert_allclose(
            action(probe.mixed_direction(p, n, angle)),
            np.cos(a) * planar_action + np.sin(a) * normal_action,
            atol=1e-9,
        )


def test_small_probe_is_deterministic_complete_and_does_not_certify_offroot_history():
    arguments = dict(
        radius=1.2, theta=0.31, parameters=PARAMETERS, steps=3, sample_every=2
    )
    first = probe.run_oblique_probe(**arguments)
    assert first == probe.run_oblique_probe(**arguments)
    assert first["sample_steps"] == [0, 2, 3]
    assert first["decision"] == "unresolved-baseline-drift"
    assert first["scope"] == probe.PROBE_SCOPE
    assert len(first["arms"]) == 10
    for arm in first["arms"]:
        assert len(arm["distances"]) == 3
        assert arm["sampled_peak_ratio"] >= 1


@pytest.mark.parametrize(
    "baseline,ratios,expected",
    [
        (0.02, [0.2, 0.3], "unresolved-baseline-drift"),
        (0, [0.7, 0.6], "contraction-over-registered-window"),
        (0, [0.2, 1.21], "growth-over-registered-window"),
        (0, [0.2, 1.0], "unresolved-over-registered-window"),
        (0, [0.8, 0.8], "unresolved-over-registered-window"),
        (0, [1.2, 1.2], "unresolved-over-registered-window"),
    ],
)
def test_window_descriptions_are_fixed_and_conservative(baseline, ratios, expected):
    assert (
        probe.describe_window(
            baseline, [{"initial_distance": 1, "final_ratio": r} for r in ratios]
        )
        == expected
    )


def test_nonfinite_state_is_a_technical_error(monkeypatch):
    monkeypatch.setattr(
        probe, "double_gaussian_gradient", lambda *args, **kwargs: np.full(3, np.nan)
    )
    with pytest.raises(FloatingPointError):
        probe._native_step(history(), np.ones(17), 0.15, KERNEL)


def test_degenerate_pattern_is_not_silently_normalized():
    with pytest.raises(ValueError, match="degenerate"):
        probe.form_directions(np.zeros((5, 3)), 0.2)


def test_120_initial_pattern_is_mirror_of_opposite_sign_60():
    h = history()
    p, n = probe.form_directions(h, 0.31)
    reflection = np.array([1, 1, -1])
    d60, d120 = [probe.mixed_direction(p, n, angle) for angle in (60, 120)]
    np.testing.assert_allclose(d120, -d60 * reflection, atol=1e-15)
    assert np.sum(d120 * p) / len(h) == pytest.approx(-0.5)
    assert np.sum(d120 * n) / len(h) == pytest.approx(np.sqrt(3) / 2)


def test_full_nonlinear_update_commutes_with_plane_reflection():
    h = history() + 0.07 * np.random.default_rng(381).normal(size=(17, 3))
    reflection = np.array([1, 1, -1])
    w = finite_memory_weights(alpha=0.13, horizon=17, memory_mass=1.0)
    np.testing.assert_allclose(
        probe._native_step(h * reflection, w, 0.15, KERNEL),
        probe._native_step(h, w, 0.15, KERNEL) * reflection,
        atol=1e-15,
    )
    other = h + np.random.default_rng(34).normal(size=(17, 3))
    assert probe.shape_distance(h * reflection, other * reflection) == pytest.approx(
        probe.shape_distance(h, other), abs=1e-14
    )


def test_small_120_and_60_trajectories_match_opposite_sign_curves():
    arguments = dict(
        radius=1.2, theta=0.31, parameters=PARAMETERS, steps=23, sample_every=2
    )
    reference = probe.run_oblique_probe(**arguments, angles=(60,))
    control = probe.run_oblique_probe(**arguments, angles=(120,))
    assert control["sample_steps"][-1] == 23
    assert len(control["arms"]) == 2
    for new, old in zip(control["arms"], reversed(reference["arms"]), strict=True):
        assert new["sign"] == -old["sign"]
        np.testing.assert_allclose(
            new["distances"], old["distances"], atol=1e-14, rtol=1e-10
        )


@pytest.mark.parametrize("angles", [(), (60, 60), (121,), (60.0,)])
def test_invalid_angle_selections_fail_before_integration(angles):
    with pytest.raises(ValueError, match="angles"):
        probe.run_oblique_probe(
            radius=1.2, theta=0.31, parameters=PARAMETERS, angles=angles
        )
