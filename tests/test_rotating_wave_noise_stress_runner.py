from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from emergenz_knoten.rotating_wave_stability_gate import RotatingWaveCandidate
from experiments.current.dynamics.rotation import (
    scalar_memory_rotating_wave_noise_stress as noise_gate,
)


def _small_candidate() -> RotatingWaveCandidate:
    return RotatingWaveCandidate(
        candidate_id="synthetic-noise-runner-only",
        radius=0.9,
        theta=0.17,
        alpha=0.08,
        horizon=24,
        memory_mass=1.0,
        eta=0.11,
        sigma_rep=1.0,
        sigma_att=3.0,
        amplitude_rep=1.0,
        amplitude_att=3.5,
    )


def test_registration_constants_match_protocol() -> None:
    assert noise_gate.CHI_GRID == (0.0,) + tuple(
        10.0**exponent for exponent in range(-22, -1)
    )
    assert noise_gate.SEEDS == (2026083101, 2026083102, 2026083103)
    assert [row[0] for row in noise_gate.CANDIDATES] == ["Anchor", "L3"]
    assert [row[4:] for row in noise_gate.CANDIDATES] == [(2000, 5), (4000, 10)]


def test_small_synthetic_cell_records_every_sample_without_target_grid() -> None:
    result = noise_gate.run_candidate_cell(
        candidate=_small_candidate(),
        chi=0.0,
        noise=np.zeros((2, 2)),
        seed=1,
        steps=2,
        sample_every=1,
    )
    assert result["steps_completed"] == 2
    assert len(result["trace"]) == 3
    assert result["bitwise_native_zero"] is True
    assert result["resolutions"]["base"]["classification"] == (
        "deterministic-control"
    )
    assert result["resolutions"]["pair"]["classification"] == (
        "deterministic-control"
    )
    assert all(
        len(row["newest"]) == 2 and np.isfinite(row["newest"]).all()
        for row in result["trace"]
    )


def test_runner_rejects_unregistered_output_paths(tmp_path: Path) -> None:
    with pytest.raises(RuntimeError, match="registered output paths"):
        noise_gate._validate_paths(
            tmp_path / "result.json",
            noise_gate.DEFAULT_REPORT,
            noise_gate.DEFAULT_FIGURE,
        )


def test_one_arm_stop_does_not_stop_the_other(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    original = noise_gate._sample_base_metrics
    calls = 0

    def forced_crossing(*args: object, **kwargs: object) -> dict[str, object]:
        nonlocal calls
        row = original(*args, **kwargs)
        calls += 1
        if calls >= 2:
            row["d0_fraction"] = 0.3
        return row

    monkeypatch.setattr(noise_gate, "_sample_base_metrics", forced_crossing)
    result = noise_gate.run_candidate_cell(
        candidate=_small_candidate(),
        chi=0.0,
        noise=np.zeros((4, 2)),
        seed=1,
        steps=4,
        sample_every=1,
    )
    assert result["arm_steps_completed"]["base"] == 1
    assert result["arm_steps_completed"]["pair"] == 4
    assert result["stop_reason"]["base"] == "quotient-stop-threshold"
    assert result["stop_reason"]["pair"] == "completed"


def test_registered_figure_can_render_to_temporary_suffix(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    candidate = _small_candidate()
    monkeypatch.setattr(
        noise_gate,
        "CANDIDATES",
        (("tiny", candidate, "0.9", "0.17", 2, 1),),
    )
    monkeypatch.setattr(noise_gate, "CHI_GRID", (0.0, 1.0e-3))
    monkeypatch.setattr(noise_gate, "SEEDS", (1,))
    result = {
        "candidate_name": "tiny",
        "chi": 1.0e-3,
        "seed": 1,
        "metrics": {
            "late_rms_d0_fraction": 1.0e-4,
            "maximum_radius_relative_error": 2.0e-4,
            "late_rms_phase_error_over_theta": 3.0e-4,
        },
        "resolutions": {
            "base": {
                "effective_to_intended_rms": 1.0,
                "nonzero_fraction": 1.0,
            }
        },
        "trace": [
            {"newest": [0.9, 0.0]},
            {"newest": [0.0, 0.9]},
            {"newest": [-0.9, 0.0]},
        ],
    }
    payload = {
        "decision": "n0-noise-stable-through-grid",
        "grid": [{"chi": 1.0e-3, "decision": "all-cell-stable"}],
        "results": [result],
    }
    output = tmp_path / "figure.png.tmp"
    noise_gate.render_figure(payload, output)
    assert output.read_bytes().startswith(b"\x89PNG\r\n\x1a\n")


def test_source_tests_do_not_call_registered_gate() -> None:
    source = Path(noise_gate.__file__).read_text(encoding="utf-8")
    test_source = Path(__file__).read_text(encoding="utf-8")
    function_call = "run_" + "gate()"
    assert f"def {function_call}" in source
    assert function_call not in test_source
