from decimal import Decimal
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
