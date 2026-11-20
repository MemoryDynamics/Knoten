"""Synthetic runner and comparator checks; never run the H=1200 control."""

from copy import deepcopy
import json

import pytest

from experiments.current.dynamics.rotation import fifo_oblique_120 as runner


def pair():
    reference = {
        "schema": "synthetic",
        "scope": "synthetic",
        "arithmetic": "float64",
        "numpy": "synthetic",
        "parameters": {},
        "radius": 1.0,
        "theta": 0.3,
        "sample_steps": [0, 10],
        "settings": {"angles_degrees": [60]},
        "baseline_distances": [0, 1e-15],
        "arms": [
            {
                "angle_degrees": 60,
                "sign": sign,
                "distances": [1e-5, value],
                "final_ratio": value / 1e-5,
            }
            for sign, value in ((-1, 0.01), (1, 0.02))
        ],
    }
    control = deepcopy(reference)
    control["settings"]["angles_degrees"] = [120]
    for new, old in zip(control["arms"], reversed(reference["arms"]), strict=True):
        new.update(
            angle_degrees=120,
            distances=old["distances"],
            final_ratio=old["final_ratio"],
        )
    return control, reference


def test_comparator_uses_opposite_sign_and_every_sample():
    control, reference = pair()
    result = runner.compare_curves(control, reference)
    assert result["decision"] == "mirror-control-pass"
    assert [(p["sign_120"], p["sign_60"]) for p in result["pairs"]] == [
        (-1, 1),
        (1, -1),
    ]
    control["arms"][0]["distances"] = [1.01e-5, 0.02]
    assert (
        runner.compare_curves(control, reference)["decision"]
        == "mirror-control-mismatch"
    )


def test_same_sign_matching_would_not_pass():
    control, reference = pair()
    for new, old in zip(control["arms"], reference["arms"], strict=True):
        new["distances"] = old["distances"]
    assert (
        runner.compare_curves(control, reference)["decision"]
        == "mirror-control-mismatch"
    )


@pytest.mark.parametrize(
    "key,value",
    [("radius", 2.0), ("parameters", {"eta": 2}), ("sample_steps", [0, 20])],
)
def test_comparator_rejects_incompatible_inputs(key, value):
    control, reference = pair()
    control[key] = value
    with pytest.raises(ValueError, match="mismatch"):
        runner.compare_curves(control, reference)


def test_bad_sampling_and_nonfinite_data_are_not_symmetry_failures():
    control, reference = pair()
    control["arms"][0]["distances"] = [1e-5]
    with pytest.raises(ValueError, match="sampling"):
        runner.compare_curves(control, reference)
    control["arms"][0]["distances"] = [1e-5, float("nan")]
    with pytest.raises(ValueError, match="nonfinite"):
        runner.compare_curves(control, reference)


def test_no_default_execution_or_reused_approval(capsys, monkeypatch):
    monkeypatch.setattr(
        runner.anchor,
        "_execution_metadata",
        lambda *args: pytest.fail("guard must run first"),
    )
    with pytest.raises(PermissionError):
        runner.execute_once("a" * 40)
    with pytest.raises(SystemExit) as error:
        runner.main([])
    assert error.value.code == 2
    assert "approval" in capsys.readouterr().err


def test_zero_budget_kills_worker_without_any_target_input(monkeypatch):
    monkeypatch.setattr(runner, "SECONDS", 0)
    record = runner._capture({})
    assert record["status"] == "timeout"
    assert record["returncode"] is not None
    assert "result" not in record


def test_attempt_persists_once_without_rerunning_old_panels(tmp_path, monkeypatch):
    control, reference = pair()
    calls = []
    monkeypatch.setattr(runner.anchor, "ROOT", tmp_path)
    monkeypatch.setattr(
        runner.anchor, "_execution_metadata", lambda *args: {"synthetic": True}
    )
    monkeypatch.setattr(runner.anchor, "load_registered_input", lambda: ({}, {}))
    monkeypatch.setattr(runner, "load_reference", lambda inputs: (reference, {}))

    def capture(inputs):
        calls.append(inputs)
        assert (tmp_path / runner.OUTPUT_REL / "receipt.json").exists()
        return {"status": "completed", "result": control}

    monkeypatch.setattr(runner, "_capture", capture)
    assert (
        runner.execute_once("a" * 40, authorization_confirmed=True)["decision"]
        == "mirror-control-pass"
    )
    with pytest.raises(FileExistsError):
        runner.execute_once("a" * 40, authorization_confirmed=True)
    assert len(calls) == 1
    saved = json.loads((tmp_path / runner.OUTPUT_REL / "probe.json").read_text())
    assert saved["result"] == control
