"""Prepared one-shot local probe. Human approval is still required.

Import/help do not evaluate the registered target. The flag is an operator
acknowledgement, never a substitute for actual author consent.
"""

from __future__ import annotations

import argparse
from datetime import UTC, datetime
import hashlib
import json
import math
import os
from pathlib import Path
import re
import subprocess
import sys
import time

import mpmath
import numpy as np

from emergenz_knoten import flat_memory_stability as method
from .fifo_archived_normal_slope import interval_bounds


ROOT = Path(__file__).resolve().parents[4]
INPUTS = {"f": "1/2", "g": "2/3", "q": "99/100"}
OUTPUT_REL = Path("reports/reference/flat_memory_stability_attempt1_2026-11-16")
SECONDS = 30
THREAD_ENV = {
    key: "1"
    for key in (
        "OPENBLAS_NUM_THREADS",
        "OMP_NUM_THREADS",
        "MKL_NUM_THREADS",
        "BLIS_NUM_THREADS",
        "VECLIB_MAXIMUM_THREADS",
        "NUMEXPR_NUM_THREADS",
    )
}
SOURCE_MODULES = (
    __name__,
    "emergenz_knoten.flat_memory_stability",
    "emergenz_knoten.vector_memory",
    "emergenz_knoten.kernels",
    "emergenz_knoten.core",
    "emergenz_knoten.rotating_wave_interval",
    "experiments.current.dynamics.rotation.fifo_archived_normal_slope",
)


def _utc():
    return datetime.now(UTC).isoformat()


def _git(*arguments):
    return subprocess.run(
        ["git", *arguments], cwd=ROOT, capture_output=True, check=True, timeout=5
    ).stdout


def _sources():
    records = []
    for name in SOURCE_MODULES:
        module = sys.modules[name]
        path = Path(module.__file__).resolve()
        relative = path.relative_to(ROOT)
        if name == __name__:
            expected = Path(
                "experiments/current/dynamics/rotation/flat_memory_cycle_stability.py"
            )
        else:
            expected = Path(*name.split(".")).with_suffix(".py")
            if name.startswith("emergenz_knoten."):
                expected = Path("src") / expected
        if relative != expected:
            raise ValueError("module not loaded from the reviewed worktree")
        records.append(
            {
                "path": relative.as_posix(),
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            }
        )
    return records


def _metadata(expected_revision):
    if type(expected_revision) is not str or not re.fullmatch(
        r"[0-9a-f]{40}", expected_revision
    ):
        raise ValueError("full frozen execution revision required")
    if _git("rev-parse", "HEAD").decode().strip() != expected_revision:
        raise ValueError("execution revision mismatch")
    if _git("status", "--porcelain").strip():
        raise ValueError("clean worktree required")
    if mpmath.__version__ != "1.3.0":
        raise ValueError("reviewed interval runtime is mpmath 1.3.0")
    return {
        "revision": expected_revision,
        "sources": _sources(),
        "python": sys.version,
        "executable": sys.executable,
        "numpy": np.__version__,
        "mpmath": mpmath.__version__,
    }


def _write_json(path, payload):
    encoded = json.dumps(payload, sort_keys=True, indent=2, allow_nan=False) + "\n"
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(encoded)
        stream.flush()
        os.fsync(stream.fileno())


def capture(command, inputs, *, seconds=SECONDS):
    if not 0 < seconds <= SECONDS:
        raise ValueError("worker deadline must be positive and at most 30 seconds")
    start = time.monotonic()
    record = {"status": "error", "started_utc": _utc(), "result": None}
    try:
        with subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            cwd=ROOT,
            env={**os.environ, **THREAD_ENV},
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
        ) as process:
            try:
                stdout, stderr = process.communicate(
                    json.dumps(inputs, allow_nan=False),
                    timeout=max(0, seconds - (time.monotonic() - start)),
                )
            except subprocess.TimeoutExpired:
                process.kill()
                stdout, stderr = process.communicate()
                record["status"] = "timeout"
            except BaseException:
                process.kill()
                process.wait()
                raise
        record.update(returncode=process.returncode, stderr=stderr)
        if record["status"] == "timeout" or process.returncode != 0:
            record["stdout"] = stdout
        else:
            result = json.loads(stdout)
            json.dumps(result, allow_nan=False)
            record.update(status="completed", result=result)
    except Exception as error:
        record["error"] = f"{type(error).__name__}: {error}"
    record.update(elapsed_seconds=time.monotonic() - start, finished_utc=_utc())
    return record


def validate_result(result):
    json.dumps(result, allow_nan=False)
    if (
        type(result) is not dict
        or result.get("schema") != method.SCHEMA
        or result.get("inputs") != INPUTS
        or result.get("decision")
        not in {method.CERTIFIED, method.UNRESOLVED, "method-inconsistent"}
    ):
        raise ValueError("worker result identity mismatch")
    certificate = result["certificate"]
    if (
        certificate.get("inputs") != INPUTS
        or certificate.get("precision_dps") != method.PRECISION_DPS
    ):
        raise ValueError("certificate input or precision mismatch")
    if result["decision"] == method.CERTIFIED:
        lower, upper = interval_bounds(certificate["form_product"])
        interior_lower, _ = interval_bounds(certificate["interior_margin"])
        diagnostics = result["diagnostics"]
        midpoint = float((lower + upper) / 2)
        displayed_midpoint = float(certificate["form_product"]["midpoint"])
        if (
            not math.isfinite(midpoint)
            or not math.isfinite(displayed_midpoint)
            or not math.isclose(
                displayed_midpoint, midpoint, rel_tol=1e-12, abs_tol=1e-12
            )
            or result.get("method_consistent") is not True
            or certificate.get("decision") != method.CERTIFIED
            or certificate.get("interior_certified") is not True
            or interior_lower <= 0
            or not (lower > 1 or upper < -1)
            or diagnostics.get("checks_passed") is not True
            or abs(diagnostics["form_product_approximate"] - midpoint)
            > method.DIAGNOSTIC_TOLERANCE * max(1.0, abs(midpoint))
            or len(diagnostics.get("form_quotient", [])) != 8
            or any(len(row) != 8 for row in diagnostics["form_quotient"])
            or len(diagnostics.get("reduced_full_matrix", [])) != 15
            or any(len(row) != 15 for row in diagnostics["reduced_full_matrix"])
            or len(diagnostics.get("form_eigenvalues_approximate", [])) != 8
            or any(
                len(pair) != 2 for pair in diagnostics["form_eigenvalues_approximate"]
            )
            or set(diagnostics.get("errors", {}))
            != {
                "orbit_residual",
                "invariant_subspace_residual",
                "return_residual",
                "form_trace_residual",
            }
            or any(
                value < 0 or value > method.DIAGNOSTIC_TOLERANCE
                for value in diagnostics["errors"].values()
            )
        ):
            raise ValueError("uncertified or inconsistent instability claim")


def execute_once(*, expected_revision, authorization_confirmed=False):
    if authorization_confirmed is not True:
        raise PermissionError(
            "explicit author approval required before target execution"
        )
    metadata = _metadata(expected_revision)
    directory = ROOT / OUTPUT_REL
    directory.mkdir(parents=True, exist_ok=False)
    _write_json(
        directory / "receipt.json",
        {
            "schema": method.SCHEMA,
            "metadata": metadata,
            "inputs": INPUTS,
            "seconds": SECONDS,
            "thread_environment": THREAD_ENV,
            "started_utc": _utc(),
            "authorization_acknowledged_by_operator": True,
            "scope": "one fixed local 15-coordinate probe; no trajectory, scan, fit, retry or stable verdict from float64",
        },
    )
    command = [
        sys.executable,
        "-m",
        "experiments.current.dynamics.rotation.flat_memory_cycle_stability",
        "--worker",
    ]
    panel = capture(command, {"inputs": INPUTS, "sources": metadata["sources"]})
    if panel["status"] == "completed":
        try:
            if _sources() != metadata["sources"]:
                raise ValueError("source files changed during execution")
            validate_result(panel["result"])
        except Exception as error:
            panel.update(status="error", error=f"{type(error).__name__}: {error}")
    _write_json(directory / "panel.json", panel)
    summary = {
        "schema": method.SCHEMA,
        "metadata": metadata,
        "inputs": INPUTS,
        "status": panel["status"],
        "elapsed_seconds": panel["elapsed_seconds"],
        "decision": panel["result"]["decision"]
        if panel["status"] == "completed"
        else method.UNRESOLVED,
        "finished_utc": _utc(),
        "result_file": "panel.json",
        "claim_boundary": "One local deterministic fixed candidate only; no stable certificate, formation, lifetime, charge or particle claim.",
    }
    _write_json(directory / "summary.json", summary)
    return summary


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execute-authorized", action="store_true")
    parser.add_argument("--expected-revision")
    parser.add_argument(
        "--describe",
        action="store_true",
        help="show fixed inputs and source hashes without evaluating the target",
    )
    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    if args.describe:
        if args.worker or args.execute_authorized or args.expected_revision is not None:
            parser.error("description cannot be combined with execution options")
        print(
            json.dumps(
                {
                    "schema": method.SCHEMA,
                    "inputs": INPUTS,
                    "seconds": SECONDS,
                    "precision_dps": method.PRECISION_DPS,
                    "thread_environment": THREAD_ENV,
                    "sources": _sources(),
                    "target_evaluated": False,
                },
                allow_nan=False,
            )
        )
        return 0
    if args.worker:
        if args.execute_authorized or args.expected_revision is not None:
            parser.error("worker cannot carry parent execution options")
        payload = json.load(sys.stdin)
        if any(os.environ.get(key) != value for key, value in THREAD_ENV.items()):
            raise ValueError("single-thread worker environment required")
        if payload != {"inputs": INPUTS, "sources": _sources()}:
            raise ValueError("worker payload must match the frozen parent request")
        result = method.evaluate(payload["inputs"])
        if payload["sources"] != _sources():
            raise ValueError("source files changed during worker execution")
        print(json.dumps(result, allow_nan=False))
        return 0
    if not args.execute_authorized or args.expected_revision is None:
        parser.error("explicit approval acknowledgement and frozen revision required")
    result = execute_once(
        expected_revision=args.expected_revision, authorization_confirmed=True
    )
    print(json.dumps(result, allow_nan=False))
    return 0 if result["status"] == "completed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
