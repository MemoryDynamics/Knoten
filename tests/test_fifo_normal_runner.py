"""Runner controls use pinned-source reads, stubs and tiny non-target workers."""

from copy import deepcopy
import io
import json
from pathlib import Path
import sys
import time

import pytest

from experiments.current.dynamics.rotation import fifo_normal_anchor as runner


def _inputs():
    return {
        "radius": "1.1",
        "theta": "0.13",
        "radius_half_width": "1e-20",
        "theta_half_width": "1e-20",
        "parameters": {**runner.PARAMETERS, "alpha": "0.5", "horizon": 4},
    }


def _result(precision=80, decision="strictly-schur"):
    inputs = _inputs()
    return {
        "schema": "normal-fifo-root-box-prototype-v1",
        "scope": "finite-H-local-linear-normal-form-only",
        "trust_basis": "mpmath.iv",
        "precision_dps": precision,
        "decision": decision,
        "parameters": inputs["parameters"],
        "root_inputs": {
            key: value for key, value in inputs.items() if key != "parameters"
        },
        "root_certificate": {"pass": True, "gates": {"synthetic": True}},
        "normal_polynomial": [{} for _ in range(5)],
        "quotient": [{}, {}],
        "remainder": [{"contains_zero": True} for _ in range(3)],
        "schur": {"degree": 1, "decision": decision},
    }


def _panel(precision, decision):
    status = decision if decision in ("error", "timeout") else "completed"
    return {
        "precision_dps": precision,
        "status": status,
        "elapsed_seconds": 0.01,
        "result": _result(precision, decision) if status == "completed" else None,
        "error": "synthetic control" if status != "completed" else None,
    }


def test_registered_input_is_read_from_pinned_git_blob_without_numerical_work(
    monkeypatch,
):
    def forbidden(**arguments):
        pytest.fail("source inspection must not evaluate the target")

    monkeypatch.setattr(runner, "certify_normal_fifo_box", forbidden)
    inputs, provenance = runner.load_registered_input()
    assert inputs["parameters"] == runner.PARAMETERS
    assert inputs["radius_half_width"] == inputs["theta_half_width"] == "1e-40"
    assert provenance["git_blob"] == runner.INPUT_BLOB
    assert provenance["revision"] == runner.INPUT_REVISION
    assert len(provenance["sha256_git_blob_bytes"]) == 64
    source = json.loads(
        runner._git("cat-file", "blob", f"{runner.INPUT_REVISION}:{runner.INPUT_PATH}")
    )
    selected = [panel for panel in source["panels"] if panel["precision_dps"] == 120][0]
    assert inputs["radius"] == selected["inner"]["center"]["radius"]
    assert inputs["theta"] == selected["inner"]["center"]["theta"]


def test_changed_git_blob_is_rejected_before_input_selection(monkeypatch):
    monkeypatch.setattr(runner, "_git", lambda *arguments: b"{}")
    with pytest.raises(ValueError, match="Git blob"):
        runner.load_registered_input()


@pytest.mark.parametrize(
    "mutation", ["identity", "parameter", "width", "duplicate", "center"]
)
def test_wrong_source_selection_is_rejected(mutation):
    source = json.loads((runner.ROOT / runner.INPUT_PATH).read_text(encoding="utf-8"))
    chosen = [panel for panel in source["panels"] if panel["precision_dps"] == 120][0]
    if mutation == "identity":
        source["candidate_id"] = "different"
    elif mutation == "parameter":
        source["parameters"]["eta"] = "0.16"
    elif mutation == "width":
        chosen["inner"]["half_width"]["theta"] = "1e-50"
    elif mutation == "duplicate":
        source["panels"].append(deepcopy(chosen))
    else:
        chosen["inner"]["center"]["theta"] = 0.1
    with pytest.raises(ValueError):
        runner._select_inputs(source)


def test_execution_requires_authorization_before_git_or_numeric_access(monkeypatch):
    monkeypatch.setattr(
        runner, "_git", lambda *arguments: pytest.fail("guard must run first")
    )
    with pytest.raises(PermissionError, match="approval"):
        runner.execute_once(expected_revision="a" * 40)


def test_default_cli_does_not_execute(capsys, monkeypatch):
    monkeypatch.setattr(
        runner, "execute_once", lambda **arguments: pytest.fail("no default execution")
    )
    with pytest.raises(SystemExit) as caught:
        runner.main([])
    assert caught.value.code == 2
    assert "approval acknowledgement" in capsys.readouterr().err


def test_numerical_modules_are_loaded_from_this_worktree(monkeypatch, tmp_path):
    assert runner._check_module_origins() == [
        "src/emergenz_knoten/fifo_normal_stability.py",
        "src/emergenz_knoten/rotating_wave_interval.py",
        "src/emergenz_knoten/fifo_oblique_probe.py",
    ]
    module = sys.modules[runner.certify_normal_fifo_box.__module__]
    monkeypatch.setattr(module, "__file__", str(tmp_path / "other-installation.py"))
    with pytest.raises(ValueError, match="execution worktree"):
        runner._check_module_origins()


def test_uncertified_root_cannot_carry_a_spectral_result():
    with pytest.raises(ValueError, match="uncertified root"):
        runner._validate_worker_result(
            _result(decision="root-not-certified"), _inputs(), 80
        )


@pytest.mark.parametrize(
    "revision,status,expected",
    [
        ("b" * 40, b"", "revision mismatch"),
        ("a" * 40, b" M changed", "clean worktree"),
        ("short", b"", "full frozen"),
    ],
)
def test_execution_revision_and_cleanliness_are_checked(
    monkeypatch, revision, status, expected
):
    monkeypatch.setattr(
        runner,
        "_git",
        lambda *arguments: b"a" * 40 if arguments[0] == "rev-parse" else status,
    )
    with pytest.raises(ValueError, match=expected):
        runner._execution_metadata(revision)


@pytest.mark.parametrize(
    "field,value",
    [
        ("precision_dps", 120),
        ("parameters", {}),
        ("root_inputs", {}),
        ("decision", "invented-pass"),
        ("quotient", []),
    ],
)
def test_worker_output_must_match_input_and_quotient(field, value):
    result = _result()
    result[field] = value
    with pytest.raises((ValueError, KeyError)):
        runner._validate_worker_result(result, _inputs(), 80)


@pytest.mark.parametrize(
    "first,second,expected",
    [
        ("strictly-schur", "strictly-schur", "strictly-schur"),
        ("not-strictly-schur", "not-strictly-schur", "not-strictly-schur"),
        ("strictly-schur", "not-strictly-schur", "method-inconsistent"),
        ("strictly-schur", "inconclusive", "inconclusive"),
        ("timeout", "strictly-schur", "inconclusive"),
        ("not-strictly-schur", "error", "inconclusive"),
        ("root-not-certified", "root-not-certified", "inconclusive"),
        ("inconsistent-symmetry-factor", "timeout", "method-inconsistent"),
    ],
)
def test_two_panel_decisions_do_not_promote_partial_results(first, second, expected):
    assert runner.classify_panels([_panel(80, first), _panel(120, second)]) == expected


def test_missing_or_reordered_panels_are_rejected():
    with pytest.raises(ValueError, match="ordered"):
        runner.classify_panels(
            [_panel(120, "strictly-schur"), _panel(80, "strictly-schur")]
        )
    with pytest.raises(ValueError, match="ordered"):
        runner.classify_panels([_panel(80, "strictly-schur")])


def test_real_worker_only_evaluates_a_small_nonroot_control():
    record = runner._run_worker(
        [sys.executable, str(Path(runner.__file__).resolve()), "--worker", "80"],
        _inputs(),
        80,
        seconds=20,
    )
    assert record["status"] == "completed", record
    assert record["result"]["decision"] == "root-not-certified"


def test_timeout_kills_worker_before_its_later_side_effect(tmp_path):
    marker = tmp_path / "must-not-exist.txt"
    code = f"import time; from pathlib import Path; print('worker-started', flush=True); time.sleep(2.5); Path({str(marker)!r}).write_text('late')"
    record = runner._run_worker(
        [sys.executable, "-c", code], _inputs(), 80, seconds=1.0
    )
    assert record["status"] == "timeout"
    assert "worker-started" in record["stdout"]
    assert record["result"] is None
    time.sleep(1.8)
    assert not marker.exists()


@pytest.mark.parametrize(
    "code,expected",
    [
        ("print('not-json')", "not-json"),
        ("import sys; print('partial'); sys.exit(4)", "partial"),
    ],
)
def test_bad_worker_outputs_remain_technical_errors(code, expected):
    record = runner._run_worker([sys.executable, "-c", code], _inputs(), 80, seconds=10)
    assert record["status"] == "error"
    assert expected in record["stdout"]
    assert record["result"] is None


def test_attempt_persists_each_panel_and_cannot_overwrite_or_retry(
    tmp_path, monkeypatch
):
    directory = tmp_path / "attempt"
    calls = []

    def fake_worker(command, inputs, precision, *, seconds):
        assert (directory / "receipt.json").exists()
        assert (directory / f"panel_{precision}_started.json").exists()
        if precision == 120:
            assert (directory / "panel_80.json").exists()
        assert seconds == 300
        assert ("--oblique-probe" in command) == (precision == 80)
        calls.append(precision)
        return _panel(precision, "strictly-schur" if precision == 80 else "timeout")

    monkeypatch.setattr(runner, "_run_worker", fake_worker)
    summary = runner._run_attempt(directory, _inputs(), {"synthetic": True})
    assert summary["decision"] == "inconclusive"
    assert summary["oblique_probe"]["status"] == "not-available"
    assert calls == [80, 120]
    saved = {path.name: path.read_bytes() for path in directory.iterdir()}
    assert json.loads(saved["panel_120.json"])["status"] == "timeout"
    assert b"inconclusive" in saved["report.md"]
    with pytest.raises(FileExistsError):
        runner._run_attempt(directory, _inputs(), {"synthetic": True})
    assert calls == [80, 120]
    assert saved == {path.name: path.read_bytes() for path in directory.iterdir()}


def test_output_serialization_failure_does_not_create_a_false_result(tmp_path):
    path = tmp_path / "invalid.json"
    with pytest.raises(ValueError):
        runner._write_json(path, {"bad": float("nan")})
    assert not path.exists()


def test_probe_record_missing_or_wrong_inputs_cannot_pass():
    with pytest.raises(ValueError, match="missing oblique"):
        runner._validate_probe_record(None, _inputs())
    with pytest.raises(ValueError, match="registered inputs"):
        runner._validate_probe_record({"status": "completed", "result": {}}, _inputs())


def test_mixed_growth_does_not_change_normal_only_classification():
    panels = [_panel(80, "strictly-schur"), _panel(120, "strictly-schur")]
    panels[0]["result"]["oblique_probe"] = {
        "status": "completed",
        "result": {"decision": "growth-over-registered-window"},
    }
    assert runner.classify_panels(panels) == "strictly-schur"


def test_probe_flag_cannot_add_work_to_second_panel(capsys):
    with pytest.raises(SystemExit) as caught:
        runner.main(["--worker", "120", "--oblique-probe"])
    assert caught.value.code == 2
    assert "80-dps worker budget" in capsys.readouterr().err


@pytest.mark.parametrize("fails", [False, True])
def test_worker_keeps_probe_arithmetic_and_failures_separate(
    monkeypatch, capsys, fails
):
    monkeypatch.setattr(runner, "_check_module_origins", lambda: [])
    monkeypatch.setattr(runner, "certify_normal_fifo_box", lambda **kwargs: _result())
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(_inputs())))
    calls = []

    def small_probe(**kwargs):
        calls.append(kwargs)
        if fails:
            raise FloatingPointError("synthetic failure")
        return {"decision": "growth-over-registered-window"}

    monkeypatch.setattr(runner, "run_oblique_probe", small_probe)
    assert runner.main(["--worker", "80", "--oblique-probe"]) == 0
    result = json.loads(capsys.readouterr().out)
    assert result["decision"] == "strictly-schur"
    assert result["oblique_probe"]["status"] == ("error" if fails else "completed")
    assert calls == [
        {"radius": 1.1, "theta": 0.13, "parameters": _inputs()["parameters"]}
    ]
