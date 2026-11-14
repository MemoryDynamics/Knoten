"""One authorized 120-degree supplement; never rerun the normal certificate."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

import numpy as np

from emergenz_knoten.fifo_oblique_probe import run_oblique_probe
from . import fifo_normal_anchor as anchor


REFERENCE_REVISION = "fdbd24fd437187a4db185d413f4c3bd022104b3b"
REFERENCE_PATH = (anchor.OUTPUT_REL / "panel_80.json").as_posix()
OUTPUT_REL = Path("reports/dynamics/rotation/fifo_oblique_120_control_2026-10-25")
SECONDS = 60
ABSOLUTE_TOLERANCE_OVER_RADIUS = 1e-11
RELATIVE_TOLERANCE = 1e-8


def load_reference(inputs: dict) -> tuple[dict, dict]:
    raw = anchor._git("cat-file", "blob", f"{REFERENCE_REVISION}:{REFERENCE_PATH}")
    record = json.loads(raw)
    anchor._validate_worker_result(record["result"], inputs, 80)
    probe = record["result"]["oblique_probe"]
    anchor._validate_probe_record(probe, inputs)
    if record["status"] != "completed" or probe["status"] != "completed":
        raise ValueError("completed archived reference required")
    if probe["result"]["numpy"] != np.__version__:
        raise ValueError("reference and control require the same NumPy version")
    return probe["result"], {
        "revision": REFERENCE_REVISION,
        "path": REFERENCE_PATH,
        "sha256_git_blob_bytes": hashlib.sha256(raw).hexdigest(),
    }


def compare_curves(control: dict, reference: dict) -> dict:
    for key in (
        "schema",
        "scope",
        "arithmetic",
        "numpy",
        "parameters",
        "radius",
        "theta",
        "sample_steps",
    ):
        if control[key] != reference[key]:
            raise ValueError(f"comparison mismatch: {key}")
    if control["settings"] != {**reference["settings"], "angles_degrees": [120]}:
        raise ValueError("comparison settings mismatch")
    if [(a["angle_degrees"], a["sign"]) for a in control["arms"]] != [
        (120, -1),
        (120, 1),
    ]:
        raise ValueError("expected exactly the two 120-degree signs")
    absolute = ABSOLUTE_TOLERANCE_OVER_RADIUS * reference["radius"]

    def differences(new, old):
        new, old = np.asarray(new, dtype=float), np.asarray(old, dtype=float)
        if new.shape != old.shape or new.shape != (len(reference["sample_steps"]),):
            raise ValueError("comparison sampling mismatch")
        if not (np.isfinite(new).all() and np.isfinite(old).all()):
            raise ValueError("nonfinite comparison data")
        error = np.abs(new - old)
        tolerance = absolute + RELATIVE_TOLERANCE * np.abs(old)
        return {
            "pass": bool(np.all(error <= tolerance)),
            "max_absolute_difference": float(np.max(error)),
            "max_fraction_of_tolerance": float(np.max(error / tolerance)),
        }

    pairs = []
    for arm in control["arms"]:
        matching = [
            a
            for a in reference["arms"]
            if a["angle_degrees"] == 60 and a["sign"] == -arm["sign"]
        ]
        if len(matching) != 1:
            raise ValueError("missing unique opposite-sign 60-degree reference")
        old = matching[0]
        pairs.append(
            {
                "sign_120": arm["sign"],
                "sign_60": old["sign"],
                "final_ratio_120": arm["final_ratio"],
                "final_ratio_60": old["final_ratio"],
                **differences(arm["distances"], old["distances"]),
            }
        )
    baseline = differences(
        control["baseline_distances"], reference["baseline_distances"]
    )
    passed = baseline["pass"] and all(pair["pass"] for pair in pairs)
    return {
        "decision": "mirror-control-pass" if passed else "mirror-control-mismatch",
        "absolute_tolerance": absolute,
        "relative_tolerance": RELATIVE_TOLERANCE,
        "pairs": pairs,
        "baseline": baseline,
        "claim_boundary": "Finite-window code/symmetry check only; no independent replication, general stability or physical validation.",
    }


def _capture(inputs: dict) -> dict:
    start = time.monotonic()
    record = {"status": "error", "started_utc": anchor._utc()}
    command = [
        sys.executable,
        "-m",
        "experiments.current.dynamics.rotation.fifo_oblique_120",
        "--worker",
    ]
    with subprocess.Popen(
        command,
        cwd=anchor.ROOT,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
    ) as process:
        try:
            stdout, stderr = process.communicate(
                json.dumps(inputs), timeout=max(0, SECONDS - (time.monotonic() - start))
            )
        except subprocess.TimeoutExpired:
            process.kill()
            stdout, stderr = process.communicate()
            record["status"] = "timeout"
        except BaseException:
            process.kill()
            process.wait()
            raise
    record.update(
        elapsed_seconds=time.monotonic() - start,
        finished_utc=anchor._utc(),
        returncode=process.returncode,
        stderr=stderr,
    )
    if record["status"] == "timeout" or process.returncode != 0:
        record["stdout"] = stdout
    else:
        try:
            record.update(status="completed", result=json.loads(stdout))
        except ValueError as error:
            record.update(error=str(error), stdout=stdout)
    return record


def execute_once(
    expected_revision: str, *, authorization_confirmed: bool = False
) -> dict:
    if authorization_confirmed is not True:
        raise PermissionError("explicit author approval required")
    metadata = anchor._execution_metadata(expected_revision)
    inputs, provenance = anchor.load_registered_input()
    reference, reference_source = load_reference(inputs)
    directory = anchor.ROOT / OUTPUT_REL
    directory.mkdir(parents=True, exist_ok=False)
    anchor._write_json(
        directory / "receipt.json",
        {
            "schema": "fifo-oblique-120-control-v1",
            "started_utc": anchor._utc(),
            "metadata": metadata,
            "inputs": inputs,
            "source": provenance,
            "reference": reference_source,
            "seconds": SECONDS,
            "authorization": "Author explicitly requested a 120-degree code/physical-plausibility control after attempt 1; two signs, unchanged anchor and window, no normal-certificate rerun.",
            "tolerances": {
                "absolute_over_radius": ABSOLUTE_TOLERANCE_OVER_RADIUS,
                "relative": RELATIVE_TOLERANCE,
            },
        },
    )
    try:
        record = _capture(inputs)
    except Exception as error:
        record = {"status": "error", "error": f"{type(error).__name__}: {error}"}
    anchor._write_json(directory / "probe.json", record)
    summary = {"decision": "technical-non-result", "status": record["status"]}
    if record["status"] == "completed":
        try:
            summary.update(compare_curves(record["result"], reference))
        except (ValueError, KeyError, TypeError) as error:
            summary["error"] = str(error)
    anchor._write_json(directory / "summary.json", summary)
    return summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execute-authorized", action="store_true")
    parser.add_argument("--expected-revision")
    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    if args.worker:
        anchor._check_module_origins()
        inputs = json.load(sys.stdin)
        result = run_oblique_probe(
            radius=float(inputs["radius"]),
            theta=float(inputs["theta"]),
            parameters=inputs["parameters"],
            angles=(120,),
        )
    else:
        if not args.execute_authorized or not args.expected_revision:
            parser.error("explicit approval and frozen revision required")
        result = execute_once(args.expected_revision, authorization_confirmed=True)
    print(json.dumps(result, indent=2, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
