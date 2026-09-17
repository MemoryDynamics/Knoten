import numpy as np

from emergenz_knoten.rotating_wave_stability import (
    circular_history,
    symmetry_tangent_vectors,
)
from emergenz_knoten.rotating_wave_stability_gate import (
    StabilityThresholds,
    deterministic_arnoldi_start,
    evaluate_decision,
    mirrored_diagnostics,
    registered_perturbations,
)


THRESHOLDS = StabilityThresholds(
    eigen_residual=1.0e-8,
    symmetry_overlap=0.99,
    symmetry_eigenvalue=1.0e-7,
    leading_complex_agreement=1.0e-5,
    leading_modulus_agreement=1.0e-6,
    unstable_modulus=1.0 + 1.0e-6,
    stable_modulus=1.0 - 1.0e-4,
    perturbation_scale_fraction=1.0e-7,
    continuation_steps=10_000,
    sample_every=20,
    stopping_radius_fraction=0.25,
    unstable_growth_minimum=100.0,
    stable_transient_growth_maximum=10.0,
    stable_final_ratio_maximum=0.1,
    exact_control_distance_maximum=1.0e-10,
)


def _panel(modulus: float) -> dict:
    row = {
        "real": modulus,
        "imag": 0.0,
        "modulus": modulus,
        "normalized_residual": 1.0e-12,
        "translation_overlap": 0.0,
        "rotation_overlap": 0.0,
        "classification": "transverse",
    }
    return {
        "panel_pass": True,
        "leading_transverse": row,
        "eigenpairs": [row],
    }


def _continuations(
    *,
    growth: float = 1.0,
    final_ratio: float = 0.05,
) -> list[dict]:
    rows = [
        {
            "name": "exact",
            "maximum_distance": 1.0e-12,
            "growth_factor": None,
            "final_ratio": None,
            "stopped": False,
            "initial_distance": 0.0,
            "final_distance": 1.0e-12,
            "final_step": THRESHOLDS.continuation_steps,
        }
    ]
    for stem in (
        "visible_radial",
        "visible_tangential",
        "full_history_transverse",
    ):
        for sign in ("plus", "minus"):
            rows.append(
                {
                    "name": f"{stem}_{sign}",
                    "maximum_distance": growth,
                    "growth_factor": growth,
                    "final_ratio": final_ratio,
                    "stopped": False,
                    "initial_distance": 1.0,
                    "final_distance": final_ratio,
                    "final_step": THRESHOLDS.continuation_steps,
                }
            )
    return rows


def test_two_frozen_arnoldi_starts_are_distinct_and_normalized():
    first = deterministic_arnoldi_start(480, "S1")
    second = deterministic_arnoldi_start(480, "S2")

    np.testing.assert_allclose(np.linalg.norm(first), 1.0, atol=2.0e-15)
    np.testing.assert_allclose(np.linalg.norm(second), 1.0, atol=2.0e-15)
    assert not np.array_equal(first, second)
    assert abs(float(first @ second)) < 0.1


def test_registered_perturbations_are_mirrored_and_transverse():
    history = circular_history(radius=0.9, theta=0.03, horizon=80)
    scale = 9.0e-8
    rows = registered_perturbations(history, scale=scale)

    assert set(rows) == {
        "exact",
        "visible_radial_plus",
        "visible_radial_minus",
        "visible_tangential_plus",
        "visible_tangential_minus",
        "full_history_transverse_plus",
        "full_history_transverse_minus",
    }
    np.testing.assert_array_equal(
        rows["visible_radial_plus"],
        -rows["visible_radial_minus"],
    )
    np.testing.assert_array_equal(
        rows["visible_tangential_plus"],
        -rows["visible_tangential_minus"],
    )
    np.testing.assert_array_equal(
        rows["full_history_transverse_plus"],
        -rows["full_history_transverse_minus"],
    )
    full = rows["full_history_transverse_plus"].ravel()
    np.testing.assert_allclose(np.linalg.norm(full), scale, rtol=2.0e-15)
    for tangent in symmetry_tangent_vectors(history).values():
        assert abs(float(full @ tangent)) <= 2.0e-17


def test_frozen_decision_semantics_separate_pass_fail_and_inconclusive():
    stable_row = _panel(0.99)["leading_transverse"]
    stable_agreement = {
        "pass": True,
        "primary": stable_row,
        "matched_convergence": stable_row,
    }

    decision, gates = evaluate_decision(
        full_map_controls=True,
        panels=[_panel(0.99), _panel(0.99)],
        agreement=stable_agreement,
        continuations=_continuations(),
        thresholds=THRESHOLDS,
    )
    assert decision == "numerically-stable-source-pass"
    assert gates["stable_spectrum"]
    assert gates["registered_perturbation_contraction"]

    unstable_row = _panel(1.01)["leading_transverse"]
    unstable_agreement = {
        "pass": True,
        "primary": unstable_row,
        "matched_convergence": unstable_row,
    }
    decision, gates = evaluate_decision(
        full_map_controls=True,
        panels=[_panel(1.01), _panel(1.01)],
        agreement=unstable_agreement,
        continuations=_continuations(growth=100.0, final_ratio=100.0),
        thresholds=THRESHOLDS,
    )
    assert decision == "unstable-source-fail"
    assert gates["unstable_spectrum"]
    assert gates["registered_perturbation_growth"]

    decision, gates = evaluate_decision(
        full_map_controls=True,
        panels=[_panel(0.99), _panel(0.99)],
        agreement=stable_agreement,
        continuations=_continuations(growth=10.01),
        thresholds=THRESHOLDS,
    )
    assert decision == "source-stability-inconclusive"
    assert gates["stable_spectrum"]
    assert not gates["registered_perturbation_contraction"]


def test_instability_requires_the_matched_pair_to_cross_the_threshold():
    panels = [_panel(1.01), _panel(1.01)]
    primary = {**panels[0]["leading_transverse"], "modulus": 1.0000011}
    matched = {**panels[1]["leading_transverse"], "modulus": 1.0000005}

    decision, gates = evaluate_decision(
        full_map_controls=True,
        panels=panels,
        agreement={
            "pass": True,
            "primary": primary,
            "matched_convergence": matched,
        },
        continuations=_continuations(growth=100.0, final_ratio=100.0),
        thresholds=THRESHOLDS,
    )

    assert decision == "source-stability-inconclusive"
    assert not gates["unstable_spectrum"]


def test_incomplete_or_stopped_controls_cannot_pass():
    stable_row = _panel(0.99)["leading_transverse"]
    agreement = {
        "pass": True,
        "primary": stable_row,
        "matched_convergence": stable_row,
    }
    incomplete = _continuations()[:-1]
    decision, gates = evaluate_decision(
        full_map_controls=True,
        panels=[_panel(0.99), _panel(0.99)],
        agreement=agreement,
        continuations=incomplete,
        thresholds=THRESHOLDS,
    )
    assert decision == "source-stability-inconclusive"
    assert not gates["continuation_registration_complete"]

    stopped = _continuations()
    stopped[0].update(
        {
            "stopped": True,
            "final_step": 7,
            "maximum_distance": float("nan"),
        }
    )
    decision, gates = evaluate_decision(
        full_map_controls=True,
        panels=[_panel(0.99), _panel(0.99)],
        agreement=agreement,
        continuations=stopped,
        thresholds=THRESHOLDS,
    )
    assert decision == "source-stability-inconclusive"
    assert not gates["exact_control_pass"]


def test_mirrored_diagnostics_are_zero_for_identical_pairs():
    diagnostics = mirrored_diagnostics(_continuations())

    assert len(diagnostics) == 3
    assert all(row["initial_absolute_difference"] == 0.0 for row in diagnostics)
    assert all(row["maximum_relative_difference"] == 0.0 for row in diagnostics)
    assert all(row["final_relative_difference"] == 0.0 for row in diagnostics)
