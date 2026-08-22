from decimal import Decimal
import json
import subprocess

from experiments.current.dynamics.rotation import (
    scalar_memory_rotating_wave_l3_stability_gate as l3,
)


def test_l3_registration_matches_the_frozen_cell_and_scaling():
    assert l3.CANDIDATE.candidate_id == l3.CANDIDATE_ID
    assert Decimal(str(l3.CANDIDATE.alpha)) * l3.CANDIDATE.horizon == Decimal(
        "12.000"
    )
    assert Decimal(str(l3.CANDIDATE.eta)) / Decimal(
        str(l3.CANDIDATE.alpha)
    ) == Decimal("15")
    assert l3.EXPECTED_JACOBIAN_SHAPE == (4800, 4800)
    assert l3.EXPECTED_JACOBIAN_NONZEROS == 8 * l3.CANDIDATE.horizon - 4
    assert [panel.start_id for panel in l3.PANELS] == ["S1", "S2"]


def test_frozen_l3_inputs_replay_without_opening_the_spectrum():
    checks, anchor_modulus, anchor_alpha = l3._load_frozen_inputs()

    assert checks["l3_foundation_replay"]["pass"]
    assert [row["precision_dps"] for row in checks["l3_interval_panels"]] == [
        80,
        120,
    ]
    assert 0.0 < anchor_modulus < 1.0
    assert anchor_alpha == 0.01


def test_frozen_protocol_and_dependency_git_blobs_are_unchanged():
    protocol_blob = l3._git_blob(l3.PROTOCOL.as_posix())
    assert protocol_blob == l3.PROTOCOL_BLOB
    assert all(
        l3._git_blob(path) == expected
        for path, expected in l3.EXPECTED_BLOBS.items()
    )
    result = subprocess.run(
        [
            "git",
            "diff",
            "--quiet",
            l3.FREEZE_REVISION,
            "HEAD",
            "--",
            l3.PROTOCOL.as_posix(),
        ],
        cwd=l3.ROOT,
        check=False,
    )
    assert result.returncode == 0


def test_unrelated_implementation_controls_pass_before_l3_is_opened():
    controls = l3._implementation_controls()

    assert controls["pass"]
    assert all(
        controls[name]["pass"]
        for name in ("finite_difference", "production_kernel", "d0_quotient")
    )


def test_committed_l3_result_retains_every_registered_pass():
    payload = json.loads((l3.ROOT / l3.DEFAULT_SUMMARY).read_text(encoding="utf-8"))

    assert payload["decision"] == "numerically-stable-source-pass"
    assert (
        payload["provenance"]["execution_revision"]
        == "8719f70273c29f7dbb2bcbab56610a0a706982c3"
    )
    assert payload["provenance"]["git_status_at_start"] == ""
    assert payload["provenance"]["pass"]
    assert all(
        row["pass"]
        for row in payload["provenance"]["dependency_blobs"].values()
    )
    assert payload["environment"]["numpy"] == "2.3.5"
    assert payload["environment"]["scipy"] == "1.17.1"
    assert payload["full_map_controls"]
    assert payload["implementation_controls"]["pass"]
    assert payload["analytic_symmetry_checks"]["pass"]
    assert payload["jacobian_shape"] == [4800, 4800]
    assert payload["jacobian_nonzero_entries"] == 19_196
    assert [panel["returned_eigenpairs"] for panel in payload["spectral_panels"]] == [
        32,
        48,
    ]
    assert all(panel["panel_pass"] for panel in payload["spectral_panels"])
    assert payload["panel_agreement"]["pass"]
    assert len(payload["continuations"]) == 7
    assert all(
        row["final_step"] == l3.THRESHOLDS.continuation_steps
        for row in payload["continuations"]
    )
    assert all(payload["gates"][name] for name in (
        "spectral_controls",
        "continuation_registration_complete",
        "stable_spectrum",
        "registered_perturbation_contraction",
        "exact_control_pass",
    ))
    assert not payload["gates"]["unstable_spectrum"]
    assert not payload["gates"]["registered_perturbation_growth"]
