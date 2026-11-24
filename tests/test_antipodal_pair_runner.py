"""Runner controls: tiny constructed workers and pinned-source reads only."""

from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys

from mpmath import mp
import pytest

from experiments.current.dynamics.rotation import antipodal_pair_attempt as runner


def _small_inputs():
    with mp.workdps(100):
        k2 = -mp.exp(-1) + mp.exp(-mp.mpf(1) / 9) / 3
        k4 = -mp.exp(-2) + mp.exp(-mp.mpf(2) / 9) / 3
        cross = 1 / (k2 / 4 + k4 / 2)
        own = cross - 4 / k2
        return {
            "parameters": {
                "self_parameters": {
                    "alpha": "0.5",
                    "horizon": 2,
                    "memory_mass": "1",
                    "eta": mp.nstr(own, 90),
                    "sigma_rep": "1",
                    "sigma_att": "3",
                    "amplitude_rep": "1",
                    "amplitude_att": "3",
                },
                "cross_eta": mp.nstr(cross, 90),
            },
            "radius": "1.001",
            "theta": "1.57",
            "iterations": 6,
            "precision_dps": 80,
            "radius_half_width": "1e-25",
            "theta_half_width": "1e-25",
        }


@pytest.fixture(scope="module")
def small_result():
    return runner.calculate_panel(_small_inputs())


def test_constructed_panel_is_bound_and_never_classified_stable(small_result):
    runner.validate_worker_result(small_result, _small_inputs())
    assert small_result["decision"] == "certified_orbit_common_normal_unstable"
    assert small_result["certificate"]["stability_certified"] is False


@pytest.mark.parametrize(
    "mutation",
    [
        "inputs",
        "seed",
        "parameters",
        "budget",
        "trace",
        "precision",
        "width",
        "center",
        "stable",
        "gate",
        "root",
        "slope",
        "decision",
        "early_certificate",
    ],
)
def test_changed_or_inconsistent_results_fail_validation(small_result, mutation):
    result = deepcopy(small_result)
    refined = result["refinement"]
    certificate = result["certificate"]
    if mutation == "inputs":
        result["inputs"]["iterations"] = 7
    elif mutation == "seed":
        refined["iterates"][0]["radius"] = "2"
    elif mutation == "parameters":
        refined["parameters"]["cross_eta"] = "0"
    elif mutation == "budget":
        refined["requested_iterations"] = 7
    elif mutation == "trace":
        refined["iterates"].pop(2)
    elif mutation == "precision":
        certificate["precision_dps"] = 120
    elif mutation == "width":
        certificate["requested_half_widths"][0] = "1e-20"
    elif mutation == "center":
        certificate["requested_center"][0] = "1"
    elif mutation == "stable":
        certificate["stability_certified"] = True
    elif mutation == "gate":
        certificate["gates"]["unreviewed"] = True
    elif mutation == "root":
        certificate["root_certified"] = False
    elif mutation == "slope":
        certificate["common_normal_slope_strictly_negative"] = False
    elif mutation == "decision":
        result["decision"] = "stable"
    else:
        refined["status"] = "left_physical_domain"
    with pytest.raises(ValueError):
        runner.validate_worker_result(result, _small_inputs())


def test_early_newton_exit_does_not_invoke_certificate(monkeypatch, small_result):
    refined = deepcopy(small_result["refinement"])
    refined.update(
        status="left_physical_domain", iterates=refined["iterates"][:1], corrections=[]
    )
    refined.update(refined["iterates"][0])
    monkeypatch.setattr(runner, "refine_antipodal_pair_root", lambda **kw: refined)
    monkeypatch.setattr(
        runner,
        "certify_antipodal_pair_box",
        lambda **kw: pytest.fail("no certificate after exit"),
    )
    result = runner.calculate_panel(_small_inputs())
    runner.validate_worker_result(result, _small_inputs())
    assert result["certificate"] is None
    assert result["decision"] == "orbit_inconclusive"


def test_registered_source_is_only_read_not_evaluated(monkeypatch):
    def forbidden(*args, **kwargs):
        pytest.fail("no target calculation during source inspection")

    monkeypatch.setattr(runner, "refine_antipodal_pair_root", forbidden)
    monkeypatch.setattr(runner, "certify_antipodal_pair_box", forbidden)
    source = runner.load_registered_source()
    assert source["git_blob"] == runner.SOURCE_BLOB
    assert source["revision"] == runner.SOURCE_REVISION
    assert len(source["sha256"]) == 64


def test_changed_source_blob_is_rejected(monkeypatch):
    monkeypatch.setattr(runner, "_git", lambda *args: b"{}")
    with pytest.raises(ValueError, match="blob mismatch"):
        runner.load_registered_source()


@pytest.mark.parametrize(
    "confirmed,note", [(False, "yes"), (True, ""), (1, "yes"), (True, None)]
)
def test_approval_guard_precedes_all_work(monkeypatch, confirmed, note):
    monkeypatch.setattr(
        runner,
        "_execution_metadata",
        lambda *args: pytest.fail("approval must precede metadata"),
    )
    with pytest.raises(PermissionError):
        runner.execute_once(
            expected_revision="a" * 40,
            approval_note=note,
            authorization_confirmed=confirmed,
        )


@pytest.mark.parametrize(
    "arguments", [[], ["--help"], ["--describe"], ["--execute-authorized"]]
)
def test_cli_without_complete_authorization_cannot_run(arguments, monkeypatch, capsys):
    monkeypatch.setattr(
        runner, "execute_once", lambda **kw: pytest.fail("unexpected execution")
    )
    monkeypatch.setattr(
        runner, "calculate_panel", lambda *args: pytest.fail("unexpected calculation")
    )
    if arguments == ["--describe"]:
        assert runner.main(arguments) == 0
        assert json.loads(capsys.readouterr().out)["approval_status"] == "proposal_only"
    else:
        with pytest.raises(SystemExit) as caught:
            runner.main(arguments)
        assert caught.value.code == (0 if arguments == ["--help"] else 2)


@pytest.mark.parametrize(
    "revision,status,message",
    [
        ("short", b"", "full frozen"),
        ("b" * 40, b"", "revision mismatch"),
        ("a" * 40, b" M changed", "clean worktree"),
    ],
)
def test_revision_and_cleanliness_guards(monkeypatch, revision, status, message):
    monkeypatch.setattr(
        runner, "_git", lambda *args: b"a" * 40 if args[0] == "rev-parse" else status
    )
    with pytest.raises(ValueError, match=message):
        runner._execution_metadata(revision)


def test_external_module_origin_is_rejected(monkeypatch, tmp_path):
    assert len(runner._module_origins()) == 2
    module = sys.modules[runner.refine_antipodal_pair_root.__module__]
    monkeypatch.setattr(module, "__file__", str(tmp_path / "other.py"))
    with pytest.raises(ValueError, match="outside"):
        runner._module_origins()


@pytest.mark.parametrize("status", ["completed", "timeout", "error"])
def test_attempt_is_consumed_once_for_every_outcome(
    tmp_path, monkeypatch, small_result, status
):
    calls = []

    def worker(command, inputs, seconds):
        calls.append((command, inputs, seconds))
        return {
            "status": status,
            "result": small_result if status == "completed" else None,
            "elapsed_seconds": 0.1,
        }

    monkeypatch.setattr(runner, "_bounded_process", worker)
    directory = tmp_path / "one_attempt"
    summary = runner._run_attempt(
        directory, _small_inputs(), {"test": True}, "synthetic authorization test"
    )
    assert summary["decision"] == (
        small_result["decision"] if status == "completed" else "orbit_inconclusive"
    )
    assert len(calls) == 1
    assert calls[0][2] == 300
    receipt = json.loads((directory / "receipt.json").read_text())
    assert receipt["inputs"] == _small_inputs()
    with pytest.raises(FileExistsError):
        runner._run_attempt(directory, _small_inputs(), {}, "do not repeat")
    assert len(calls) == 1


def test_interruption_retains_consumed_directory(tmp_path, monkeypatch):
    def interrupt(*args):
        raise KeyboardInterrupt

    monkeypatch.setattr(runner, "_bounded_process", interrupt)
    directory = tmp_path / "interrupted"
    with pytest.raises(KeyboardInterrupt):
        runner._run_attempt(directory, _small_inputs(), {}, "synthetic control")
    assert (directory / "receipt.json").exists()
    with pytest.raises(FileExistsError):
        runner._run_attempt(directory, _small_inputs(), {}, "do not repeat")


def test_real_small_worker_uses_reviewed_runtime_and_threads():
    result = runner._bounded_process(
        [sys.executable, str(Path(runner.__file__).resolve()), "--worker"],
        _small_inputs(),
        20,
    )
    assert result["status"] == "completed", result
    assert result["returncode"] == 0
    assert result["result"]["worker_runtime"]["thread_environment"] == runner.THREAD_ENV
    assert result["result"]["decision"] == "certified_orbit_common_normal_unstable"


def test_real_tiny_sleep_worker_is_terminated_and_reaped(monkeypatch):
    real_popen = subprocess.Popen
    handles = []

    def tracked(*args, **kwargs):
        process = real_popen(*args, **kwargs)
        handles.append(process)
        return process

    monkeypatch.setattr(runner.subprocess, "Popen", tracked)
    result = runner._bounded_process(
        [sys.executable, "-c", "import time; time.sleep(30)"], {}, 0.15
    )
    assert result["status"] == "timeout"
    assert len(handles) == 1
    assert handles[0].poll() is not None
    assert result["result"] is None


@pytest.mark.parametrize("code", ["raise SystemExit(2)", "print('invalid JSON')"])
def test_real_failed_worker_is_not_retried(code):
    result = runner._bounded_process([sys.executable, "-c", code], {}, 10)
    assert result["status"] == "error"
    assert result["result"] is None


def test_record_writer_refuses_overwrite(tmp_path):
    path = tmp_path / "receipt.json"
    runner._write_json(path, {"first": True})
    with pytest.raises(FileExistsError):
        runner._write_json(path, {"second": True})
    assert json.loads(path.read_text()) == {"first": True}


def test_invalid_json_does_not_create_an_empty_result_file(tmp_path):
    path = tmp_path / "invalid.json"
    with pytest.raises(ValueError):
        runner._write_json(path, {"invalid": float("nan")})
    assert not path.exists()
