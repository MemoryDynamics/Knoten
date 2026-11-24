"""Proposed one-shot antipodal existence test; author approval still required.

Import/help/--describe never evaluate the target. The execution flag records
the operator's acknowledgement, not human consent by itself. No old FIFO or
AL1 approval applies. The worker has no subprocesses or numerical threads.
"""

from __future__ import annotations

import argparse
from datetime import UTC, datetime
from decimal import Decimal
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from time import monotonic

import mpmath

from emergenz_knoten.antipodal_pair_interval import (
    AntipodalPairParameters,
    certify_antipodal_pair_box,
    refine_antipodal_pair_root,
)
from emergenz_knoten.rotating_wave_interval import IntervalRotatingWaveParameters


ROOT = Path(__file__).resolve().parents[4]
SOURCE_REVISION = "c297f0d8c7f1e118060b7ea845fbb6fa52dcf560"
SOURCE_PATH = "reports/dynamics/rotation/scalar_memory_rotating_wave_initial_state_spec_2026-08-20.json"
SOURCE_BLOB = "09ce359e085b8bb73d002e8c6e61f21717445e88"
OUTPUT_REL = Path("reports/dynamics/rotation/antipodal_pair_attempt_1")
SCHEMA = "antipodal-pair-existence-attempt-v1"
SECONDS = 300
THREAD_ENV = {
    name: "1"
    for name in (
        "OPENBLAS_NUM_THREADS",
        "OMP_NUM_THREADS",
        "MKL_NUM_THREADS",
        "NUMEXPR_NUM_THREADS",
    )
}
PROPOSAL = {
    "parameters": {
        "self_parameters": {
            "alpha": "0.01",
            "horizon": 1200,
            "memory_mass": "1.0",
            "eta": "0.15",
            "sigma_rep": "1.0",
            "sigma_att": "3.0",
            "amplitude_rep": "1.0",
            "amplitude_att": "3.5",
        },
        "cross_eta": "0.15",
    },
    "radius": "0.946517504804225",
    "theta": "0.015770381717135",
    "precision_dps": 80,
    "iterations": 12,
    "radius_half_width": "1e-30",
    "theta_half_width": "1e-30",
}
CLAIM_BOUNDARY = (
    "One prepared antipodal pair, fixed parameters and one seed/box. "
    "No stability pass, branch tracking, formation, lifetime, spin, charge, "
    "quark or quantum-field claim. Failure is inconclusive, not nonexistence. "
    "Additive total gain is 0.30, not the original single gain 0.15."
)


def _utc():
    return datetime.now(UTC).isoformat()


def _git(*arguments):
    return subprocess.run(
        ["git", *arguments], cwd=ROOT, capture_output=True, check=True, timeout=30
    ).stdout


def load_registered_source():
    raw = _git("cat-file", "blob", f"{SOURCE_REVISION}:{SOURCE_PATH}")
    blob = hashlib.sha1(
        b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw
    ).hexdigest()
    if blob != SOURCE_BLOB:
        raise ValueError("registered source blob mismatch")
    source = json.loads(raw, parse_float=Decimal)
    if source["candidate_id"] != "k0h-rw-aatt3p5-alpha1e-2-h1200-eta0p15-v1":
        raise ValueError("registered source identity mismatch")
    for name, value in PROPOSAL["parameters"]["self_parameters"].items():
        if Decimal(str(source["parameters"][name])) != Decimal(str(value)):
            raise ValueError("registered source parameter mismatch")
    if source["rotating_wave"]["radius"] != Decimal(PROPOSAL["radius"]) or source[
        "rotating_wave"
    ]["theta_per_update"] != Decimal(PROPOSAL["theta"]):
        raise ValueError("registered source seed mismatch")
    return {
        "revision": SOURCE_REVISION,
        "path": SOURCE_PATH,
        "git_blob": blob,
        "sha256": hashlib.sha256(raw).hexdigest(),
        "use": "stored seed and self parameters only, not a pair root certificate",
    }


def _module_origins():
    result = []
    for name in (
        "emergenz_knoten.antipodal_pair_interval",
        "emergenz_knoten.rotating_wave_interval",
    ):
        relative = Path("src") / Path(*name.split(".")).with_suffix(".py")
        if Path(sys.modules[name].__file__).resolve() != (ROOT / relative).resolve():
            raise ValueError("numerical module is outside the execution worktree")
        result.append(relative.as_posix())
    return result


def _execution_metadata(expected_revision):
    if not re.fullmatch(r"[0-9a-f]{40}", expected_revision or ""):
        raise ValueError("expected a full frozen execution revision")
    if _git("rev-parse", "HEAD").decode().strip() != expected_revision:
        raise ValueError("execution revision mismatch")
    if _git("status", "--porcelain").strip():
        raise ValueError("execution requires a clean worktree")
    if sys.version_info[:2] != (3, 12) or mpmath.__version__ != "1.3.0":
        raise ValueError("reviewed runtime is Python 3.12 and mpmath 1.3.0")
    return {
        "execution_revision": expected_revision,
        "git_status_at_start": "",
        "python": sys.version,
        "executable": sys.executable,
        "mpmath": mpmath.__version__,
        "mpmath_backend": mpmath.libmp.BACKEND,
        "local_modules": _module_origins(),
        "source": load_registered_source(),
    }


def calculate_panel(inputs):
    """Generic worker calculation; tests supply only constructed small inputs."""
    parameters = AntipodalPairParameters(
        IntervalRotatingWaveParameters(**inputs["parameters"]["self_parameters"]),
        cross_eta=inputs["parameters"]["cross_eta"],
    )
    refined = refine_antipodal_pair_root(
        radius=inputs["radius"],
        theta=inputs["theta"],
        parameters=parameters,
        precision_dps=inputs["precision_dps"],
        iterations=inputs["iterations"],
    )
    certificate = None
    if refined["status"] == "iteration_budget_completed":
        certificate = certify_antipodal_pair_box(
            radius=refined["radius"],
            theta=refined["theta"],
            radius_half_width=inputs["radius_half_width"],
            theta_half_width=inputs["theta_half_width"],
            parameters=parameters,
            precision_dps=inputs["precision_dps"],
        )
    return {
        "schema": SCHEMA,
        "inputs": inputs,
        "refinement": refined,
        "certificate": certificate,
        "decision": certificate["classification"]
        if certificate
        else "orbit_inconclusive",
    }


def validate_worker_result(result, inputs):
    if (
        not isinstance(result, dict)
        or result.get("schema") != SCHEMA
        or result.get("inputs") != inputs
    ):
        raise ValueError("worker result is not bound to the requested input")
    refined = result["refinement"]
    if (
        refined["parameters"] != inputs["parameters"]
        or refined["precision_dps"] != inputs["precision_dps"]
        or refined["requested_iterations"] != inputs["iterations"]
        or refined["root_certified"] is not False
        or len(refined["corrections"]) > inputs["iterations"]
        or len(refined["iterates"]) > inputs["iterations"] + 1
        or refined["iterates"][-1] != {key: refined[key] for key in ("radius", "theta")}
    ):
        raise ValueError("inconsistent Newton result")
    for key in ("radius", "theta"):
        if Decimal(refined["iterates"][0][key]) != Decimal(inputs[key]):
            raise ValueError("worker changed the Newton seed")
    certificate = result["certificate"]
    if refined["status"] != "iteration_budget_completed":
        if (
            refined["status"]
            not in {
                "nonfinite_evaluation",
                "nonfinite_step",
                "left_physical_domain",
                "singular_point_jacobian",
            }
            or certificate is not None
            or result["decision"] != "orbit_inconclusive"
        ):
            raise ValueError("failed refinement cannot carry a certificate")
        return
    if (
        len(refined["iterates"]) != inputs["iterations"] + 1
        or len(refined["corrections"]) != inputs["iterations"]
    ):
        raise ValueError("completed refinement changed the iteration budget")
    if (
        certificate["parameters"] != inputs["parameters"]
        or certificate["precision_dps"] != inputs["precision_dps"]
        or certificate["requested_center"] != [refined["radius"], refined["theta"]]
        or certificate["requested_half_widths"]
        != [inputs["radius_half_width"], inputs["theta_half_width"]]
        or certificate["stability_certified"] is not False
        or set(certificate["gates"])
        != {
            "physical_box",
            "balance_contains_zero",
            "jacobian_nonsingular",
            "preconditioner_nonsingular",
            "krawczyk_strict_interior",
        }
        or any(type(value) is not bool for value in certificate["gates"].values())
        or certificate["root_certified"] is not all(certificate["gates"].values())
    ):
        raise ValueError("inconsistent orbit certificate")
    upper = tuple(certificate["common_normal_slope"]["upper_binary"])
    negative = bool(mpmath.libmp.mpf_lt(upper, mpmath.libmp.fzero))
    if certificate["common_normal_slope_strictly_negative"] is not negative:
        raise ValueError("slope sign disagrees with the binary endpoint")
    expected = (
        "orbit_inconclusive"
        if not certificate["root_certified"]
        else "certified_orbit_common_normal_unstable"
        if negative
        else "certified_orbit_stability_unresolved"
    )
    if certificate["classification"] != expected or result["decision"] != expected:
        raise ValueError("unsupported worker classification")


def _bounded_process(command, inputs, seconds):
    started = monotonic()
    environment = os.environ.copy()
    environment.update(THREAD_ENV)
    # Put this worktree first; the worker independently verifies module origins.
    environment["PYTHONPATH"] = (
        str(ROOT / "src") + os.pathsep + environment.get("PYTHONPATH", "")
    )
    record = {"status": "error", "result": None, "started_utc": _utc()}
    try:
        with subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            cwd=ROOT,
            env=environment,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
        ) as process:
            try:
                stdout, stderr = process.communicate(
                    json.dumps(inputs, allow_nan=False),
                    timeout=max(0, seconds - (monotonic() - started)),
                )
            except subprocess.TimeoutExpired:
                process.kill()
                stdout, stderr = process.communicate()
                record["status"] = "timeout"
            except BaseException:
                process.kill()
                process.wait()
                raise
        record.update(returncode=process.returncode, stdout=stdout, stderr=stderr)
        if record["status"] == "timeout":
            pass
        elif process.returncode != 0:
            record["error"] = "worker exited unsuccessfully"
        else:
            result = json.loads(stdout)
            validate_worker_result(result, inputs)
            if result.get("worker_runtime") != {
                "python_major_minor": [3, 12],
                "mpmath": "1.3.0",
                "thread_environment": THREAD_ENV,
                "local_modules": _module_origins(),
            }:
                raise ValueError("worker runtime mismatch")
            record.update(status="completed", result=result)
    except Exception as error:
        record["error"] = f"{type(error).__name__}: {error}"
    record.update(elapsed_seconds=monotonic() - started, finished_utc=_utc())
    return record


def _write_json(path, content):
    encoded = json.dumps(content, indent=2, sort_keys=True, allow_nan=False) + "\n"
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(encoded)
        stream.flush()
        os.fsync(stream.fileno())


def _run_attempt(directory, inputs, metadata, approval_note):
    directory.mkdir(parents=True, exist_ok=False)
    _write_json(
        directory / "receipt.json",
        {
            "schema": SCHEMA,
            "started_utc": _utc(),
            "inputs": inputs,
            "metadata": metadata,
            "seconds": SECONDS,
            "thread_environment": THREAD_ENV,
            "authorization_acknowledged_by_operator": True,
            "approval_note": approval_note,
            "lease_policy": "directory creation consumes this attempt even on interruption or error",
        },
    )
    panel = _bounded_process(
        [sys.executable, str(Path(__file__).resolve()), "--worker"], inputs, SECONDS
    )
    _write_json(directory / "panel.json", panel)
    summary = {
        "schema": SCHEMA,
        "finished_utc": _utc(),
        "metadata": metadata,
        "decision": panel["result"]["decision"]
        if panel["status"] == "completed"
        else "orbit_inconclusive",
        "worker_status": panel["status"],
        "elapsed_seconds": panel["elapsed_seconds"],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    _write_json(directory / "summary.json", summary)
    return summary


def execute_once(*, expected_revision, approval_note, authorization_confirmed=False):
    if (
        authorization_confirmed is not True
        or not isinstance(approval_note, str)
        or not approval_note.strip()
    ):
        raise PermissionError(
            "explicit author approval and an approval note are required"
        )
    metadata = _execution_metadata(expected_revision)
    return _run_attempt(ROOT / OUTPUT_REL, PROPOSAL, metadata, approval_note)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--describe", action="store_true")
    action.add_argument("--execute-authorized", action="store_true")
    action.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--expected-revision")
    parser.add_argument("--approval-note")
    args = parser.parse_args(argv)
    if args.describe:
        output = {
            "approval_status": "proposal_only",
            "inputs": PROPOSAL,
            "seconds": SECONDS,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    elif args.worker:
        runtime = {
            "python_major_minor": list(sys.version_info[:2]),
            "mpmath": mpmath.__version__,
            "thread_environment": {name: os.environ.get(name) for name in THREAD_ENV},
            "local_modules": _module_origins(),
        }
        if (
            runtime["thread_environment"] != THREAD_ENV
            or runtime["python_major_minor"] != [3, 12]
            or runtime["mpmath"] != "1.3.0"
        ):
            raise ValueError(
                "worker requires reviewed runtime and one-thread environment"
            )
        output = calculate_panel(json.load(sys.stdin))
        output["worker_runtime"] = runtime
    else:
        if not args.expected_revision or not args.approval_note:
            parser.error("execution requires a frozen revision and an approval note")
        output = execute_once(
            expected_revision=args.expected_revision,
            approval_note=args.approval_note,
            authorization_confirmed=True,
        )
    print(json.dumps(output, indent=2, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
