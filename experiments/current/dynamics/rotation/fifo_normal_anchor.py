"""Bounded one-shot normal test; importing or showing help performs no target work.

The execution flag records the operator's acknowledgement, not human consent
by itself. Actual author approval is required before invoking the target entry.
The hidden worker is only a generic adapter subprocess with explicit stdin.
"""

from __future__ import annotations

import argparse
from datetime import UTC, datetime
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
from typing import Any

import mpmath

from emergenz_knoten.fifo_normal_stability import certify_normal_fifo_box
from emergenz_knoten.fifo_oblique_probe import (
    ANGLES_DEGREES,
    PROBE_SCOPE,
    RELATIVE_AMPLITUDE,
    SAMPLE_EVERY,
    STEPS,
    run_oblique_probe,
)
from emergenz_knoten.rotating_wave_interval import IntervalRotatingWaveParameters


ROOT = Path(__file__).resolve().parents[4]
INPUT_REVISION = "eb51fcf4ef3ab022112d523229be87b27d73f562"
INPUT_PATH = "reports/dynamics/rotation/scalar_memory_rotating_wave_interval_certificate_2026-08-21.json"
INPUT_BLOB = "fc6e816c6895e408693fbde176afdaee963c20b9"
SOURCE_EXECUTION = "8ce6c00713cbac24ebaec337bd339f1944dbcc35"
CANDIDATE_ID = "k0h-rw-aatt3p5-alpha1e-2-h1200-eta0p15-v1"
OUTPUT_REL = Path("reports/dynamics/rotation/fifo_normal_anchor_attempt_1_2026-10-25")
PRECISIONS = (80, 120)
PANEL_SECONDS = 300
PARAMETERS = {
    "alpha": "0.01",
    "horizon": 1200,
    "memory_mass": "1.0",
    "eta": "0.15",
    "sigma_rep": "1.0",
    "sigma_att": "3.0",
    "amplitude_rep": "1.0",
    "amplitude_att": "3.5",
}
ADAPTER_DECISIONS = {
    "strictly-schur",
    "not-strictly-schur",
    "inconclusive",
    "root-not-certified",
    "inconsistent-symmetry-factor",
}


def _utc() -> str:
    return datetime.now(UTC).isoformat()


def _git(*arguments: str) -> bytes:
    return subprocess.run(
        ["git", *arguments], cwd=ROOT, capture_output=True, check=True, timeout=30
    ).stdout


def _select_inputs(source: dict[str, Any]) -> dict[str, Any]:
    if (
        source.get("candidate_id") != CANDIDATE_ID
        or source.get("execution_revision") != SOURCE_EXECUTION
        or source.get("decision") != "interval-certified-unique-root-pass"
    ):
        raise ValueError("registered source identity mismatch")
    parameters = {name: source["parameters"][name] for name in PARAMETERS}
    if parameters != PARAMETERS or type(parameters["horizon"]) is not int:
        raise ValueError("registered parameters mismatch")
    panels = [panel for panel in source["panels"] if panel["precision_dps"] == 120]
    if len(panels) != 1:
        raise ValueError("expected exactly one source 120-dps panel")
    inner = panels[0]["inner"]
    if inner["half_width"] != {"radius": "1e-40", "theta": "1e-40"}:
        raise ValueError("registered root widths mismatch")
    center = inner["center"]
    if set(center) != {"radius", "theta"} or any(
        type(value) is not str for value in center.values()
    ):
        raise ValueError("expected exact source center strings")
    return {
        **center,
        "radius_half_width": inner["half_width"]["radius"],
        "theta_half_width": inner["half_width"]["theta"],
        "parameters": parameters,
    }


def load_registered_input() -> tuple[dict[str, Any], dict[str, Any]]:
    raw = _git("cat-file", "blob", f"{INPUT_REVISION}:{INPUT_PATH}")
    observed = hashlib.sha1(
        b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw
    ).hexdigest()
    if observed != INPUT_BLOB:
        raise ValueError("registered source Git blob mismatch")
    inputs = _select_inputs(json.loads(raw))
    return inputs, {
        "revision": INPUT_REVISION,
        "path": INPUT_PATH,
        "git_blob": observed,
        "sha256_git_blob_bytes": hashlib.sha256(raw).hexdigest(),
        "candidate_id": CANDIDATE_ID,
    }


def _execution_metadata(expected_revision: str) -> dict[str, Any]:
    if not re.fullmatch(r"[0-9a-f]{40}", expected_revision):
        raise ValueError("expected a full frozen execution revision")
    revision = _git("rev-parse", "HEAD").decode().strip()
    if revision != expected_revision:
        raise ValueError("execution revision mismatch")
    if _git("status", "--porcelain").strip():
        raise ValueError("execution requires a clean worktree")
    if sys.version_info[:2] != (3, 12) or mpmath.__version__ != "1.3.0":
        raise ValueError("reviewed runtime is Python 3.12 and mpmath 1.3.0")
    origins = _check_module_origins()
    return {
        "execution_revision": revision,
        "git_status_at_start": "",
        "python": sys.version,
        "mpmath": mpmath.__version__,
        "executable": sys.executable,
        "local_modules": origins,
    }


def _check_module_origins() -> list[str]:
    paths = []
    for module_name in (
        certify_normal_fifo_box.__module__,
        IntervalRotatingWaveParameters.__module__,
        run_oblique_probe.__module__,
    ):
        relative = Path("src") / Path(*module_name.split(".")).with_suffix(".py")
        actual = Path(sys.modules[module_name].__file__).resolve()
        if actual != (ROOT / relative).resolve():
            raise ValueError(
                "numerical module was not loaded from the execution worktree"
            )
        paths.append(relative.as_posix())
    return paths


def _validate_worker_result(result: Any, inputs: dict, precision: int) -> None:
    if not isinstance(result, dict):
        raise ValueError("worker did not return an object")
    if (
        result.get("schema") != "normal-fifo-root-box-prototype-v1"
        or result.get("scope") != "finite-H-local-linear-normal-form-only"
        or result.get("trust_basis") != "mpmath.iv"
        or result.get("precision_dps") != precision
        or type(result.get("precision_dps")) is not int
        or result.get("parameters") != inputs["parameters"]
        or result.get("root_inputs")
        != {key: value for key, value in inputs.items() if key != "parameters"}
        or result.get("decision") not in ADAPTER_DECISIONS
    ):
        raise ValueError("worker result is not bound to the requested input")
    decision = result["decision"]
    if decision == "root-not-certified":
        if (
            result["root_certificate"]["pass"] is not False
            or result["schur"] is not None
        ):
            raise ValueError("uncertified root must not carry a Schur result")
    if decision in {"strictly-schur", "not-strictly-schur", "inconclusive"}:
        root = result["root_certificate"]
        horizon = inputs["parameters"]["horizon"]
        if (
            root["pass"] is not True
            or not all(value is True for value in root["gates"].values())
            or len(result["normal_polynomial"]) != horizon + 1
            or len(result["quotient"]) != horizon - 2
            or len(result["remainder"]) != 3
            or not all(
                record["contains_zero"] is True for record in result["remainder"]
            )
            or result["schur"]["degree"] != horizon - 3
            or result["schur"]["decision"] != decision
        ):
            raise ValueError("worker result has inconsistent certificate or quotient")


def _run_worker(
    command: list[str], inputs: dict, precision: int, *, seconds: float
) -> dict:
    start = time.monotonic()
    record = {
        "precision_dps": precision,
        "started_utc": _utc(),
        "status": "error",
        "result": None,
    }
    try:
        with subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            cwd=ROOT,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
        ) as process:
            try:
                stdout, stderr = process.communicate(
                    json.dumps(inputs, allow_nan=False),
                    timeout=max(0.0, seconds - (time.monotonic() - start)),
                )
            except subprocess.TimeoutExpired:
                process.kill()
                stdout, stderr = process.communicate()
                record.update(status="timeout", stdout=stdout, stderr=stderr)
            except BaseException:
                process.kill()
                process.wait()
                raise
        record.update(returncode=process.returncode, stderr=stderr)
        if record["status"] == "timeout":
            pass
        elif process.returncode != 0:
            record["stdout"] = stdout
            record["error"] = "worker exited unsuccessfully"
        else:
            try:
                result = json.loads(stdout)
                _validate_worker_result(result, inputs, precision)
                if "--oblique-probe" in command:
                    _validate_probe_record(result.get("oblique_probe"), inputs)
            except (ValueError, KeyError, TypeError) as error:
                record.update(error=str(error), stdout=stdout)
            else:
                record.update(status="completed", result=result)
    except Exception as error:
        record["error"] = f"{type(error).__name__}: {error}"
    record["elapsed_seconds"] = time.monotonic() - start
    record["finished_utc"] = _utc()
    return record


def _validate_probe_record(record: Any, inputs: dict) -> None:
    if not isinstance(record, dict) or record.get("status") not in {
        "completed",
        "error",
        "not-run",
    }:
        raise ValueError("missing oblique probe record")
    if record["status"] != "completed":
        return
    result = record["result"]
    if (
        result.get("schema") != "fifo-oblique-probe-v1"
        or result.get("scope") != PROBE_SCOPE
        or result.get("arithmetic") != "float64"
        or result.get("parameters") != inputs["parameters"]
        or result.get("radius") != float(inputs["radius"])
        or result.get("theta") != float(inputs["theta"])
        or result.get("settings")
        != {
            "angles_degrees": list(ANGLES_DEGREES),
            "signs": [-1, 1],
            "relative_amplitude": RELATIVE_AMPLITUDE,
            "steps": STEPS,
            "sample_every": SAMPLE_EVERY,
            "scaled_duration_alpha_n": float(inputs["parameters"]["alpha"]) * STEPS,
        }
        or [(arm["angle_degrees"], arm["sign"]) for arm in result["arms"]]
        != [(angle, sign) for angle in ANGLES_DEGREES for sign in (-1, 1)]
    ):
        raise ValueError("oblique probe does not match registered inputs/settings")


def classify_panels(panels: list[dict]) -> str:
    if [panel["precision_dps"] for panel in panels] != list(PRECISIONS):
        raise ValueError("expected exactly the ordered 80/120-dps panels")
    decisions = [
        panel["result"]["decision"]
        for panel in panels
        if panel["status"] == "completed"
    ]
    if "inconsistent-symmetry-factor" in decisions or set(decisions) == {
        "strictly-schur",
        "not-strictly-schur",
    }:
        return "method-inconsistent"
    if (
        len(decisions) == 2
        and len(set(decisions)) == 1
        and decisions[0] in {"strictly-schur", "not-strictly-schur"}
    ):
        return decisions[0]
    return "inconclusive"


def _write_json(path: Path, payload: Any) -> None:
    encoded = json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n"
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(encoded)
        stream.flush()
        os.fsync(stream.fileno())


def _run_attempt(directory: Path, inputs: dict, metadata: dict) -> dict:
    directory.mkdir(parents=True, exist_ok=False)
    receipt = {
        "schema": "fifo-normal-anchor-attempt-v1",
        "started_utc": _utc(),
        "inputs": inputs,
        "metadata": metadata,
        "precision_panels": list(PRECISIONS),
        "seconds_per_panel": PANEL_SECONDS,
        "authorization_acknowledged_by_operator": True,
        "authorization_scope": "Author approved the two bounded panels and requested oblique perturbations before execution; fixed supplementary probes run only in the 80-dps worker, within its existing deadline.",
    }
    _write_json(directory / "receipt.json", receipt)
    panels = []
    for precision in PRECISIONS:
        _write_json(
            directory / f"panel_{precision}_started.json",
            {"started_utc": _utc(), "precision_dps": precision},
        )
        command = [
            sys.executable,
            str(Path(__file__).resolve()),
            "--worker",
            str(precision),
        ]
        if precision == 80:
            command.append("--oblique-probe")
        panel = _run_worker(
            command,
            inputs,
            precision,
            seconds=PANEL_SECONDS,
        )
        _write_json(directory / f"panel_{precision}.json", panel)
        panels.append(panel)
    probe = (panels[0]["result"] or {}).get(
        "oblique_probe", {"status": "not-available"}
    )
    summary = {
        "schema": receipt["schema"],
        "metadata": metadata,
        "finished_utc": _utc(),
        "decision": classify_panels(panels),
        "oblique_probe": {
            "status": probe["status"],
            "decision": probe.get("result", {}).get("decision"),
            "result_file": "panel_80.json",
        },
        "panels": [
            {key: panel[key] for key in ("precision_dps", "status", "elapsed_seconds")}
            | {
                "decision": panel["result"]["decision"]
                if panel["result"] is not None
                else None,
                "result_file": f"panel_{panel['precision_dps']}.json",
            }
            for panel in panels
        ],
        "claim_boundary": "The main decision is normal-only. Supplementary float64 oblique probes describe one fixed finite window, not full 3D stability. No planar proof, formation, lifetime, topology or quantum claim.",
    }
    _write_json(directory / "summary.json", summary)
    lines = [
        "# FIFO normal anchor attempt 1",
        "",
        f"Normal-only decision: **{summary['decision']}**.",
        "",
        "| dps | status | decision | seconds |",
        "| ---: | --- | --- | ---: |",
    ]
    for panel in summary["panels"]:
        lines.append(
            f"| {panel['precision_dps']} | {panel['status']} | {panel['decision']} | {panel['elapsed_seconds']:.3f} |"
        )
    lines += [
        "",
        "## Supplementary oblique probes",
        "",
        f"Status: {probe['status']}. Decision: {probe.get('result', {}).get('decision')}.",
        "",
    ]
    if probe["status"] == "completed":
        lines += [
            "Float64; proper-rotation/translation aligned, age-labelled shape RMS. Angles are in history-state norm.",
            "",
            "| angle | sign | initial RMS | final / initial | sampled peak / initial |",
            "| ---: | ---: | ---: | ---: | ---: |",
        ]
        for arm in probe["result"]["arms"]:
            lines.append(
                f"| {arm['angle_degrees']} | {arm['sign']} | {arm['initial_distance']:.9g} | {arm['final_ratio']:.9g} | {arm['sampled_peak_ratio']:.9g} |"
            )
        lines += [
            "",
            f"Maximum sampled baseline shape drift: {max(probe['result']['baseline_distances']):.9g}.",
            "",
        ]
    lines += [
        summary["claim_boundary"],
        "",
        "Exact inputs and provenance: receipt.json. Full intervals and failures: panel_80.json and panel_120.json.",
        "",
    ]
    with (directory / "report.md").open("x", encoding="utf-8", newline="\n") as stream:
        stream.write("\n".join(lines))
    return summary


def execute_once(
    *, expected_revision: str, authorization_confirmed: bool = False
) -> dict:
    if authorization_confirmed is not True:
        raise PermissionError(
            "explicit author approval is required before target execution"
        )
    metadata = _execution_metadata(expected_revision)
    inputs, provenance = load_registered_input()
    metadata["source"] = provenance
    return _run_attempt(ROOT / OUTPUT_REL, inputs, metadata)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execute-authorized", action="store_true")
    parser.add_argument("--expected-revision")
    parser.add_argument("--oblique-probe", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument(
        "--worker", type=int, choices=PRECISIONS, help=argparse.SUPPRESS
    )
    args = parser.parse_args(argv)
    if args.oblique_probe and args.worker != 80:
        parser.error("oblique probes belong only to the 80-dps worker budget")
    if args.worker is not None:
        _check_module_origins()
        payload = json.load(sys.stdin)
        inputs = dict(payload)
        parameters = IntervalRotatingWaveParameters(**payload.pop("parameters"))
        result = certify_normal_fifo_box(
            **payload, parameters=parameters, precision_dps=args.worker
        )
        if args.oblique_probe:
            probe = {"status": "not-run", "reason": "root not certified"}
            if result["root_certificate"]["pass"]:
                start = time.monotonic()
                try:
                    probe = {
                        "status": "completed",
                        "result": run_oblique_probe(
                            radius=float(inputs["radius"]),
                            theta=float(inputs["theta"]),
                            parameters=inputs["parameters"],
                        ),
                    }
                except Exception as error:
                    probe = {
                        "status": "error",
                        "error": f"{type(error).__name__}: {error}",
                    }
                probe["elapsed_seconds"] = time.monotonic() - start
            result["oblique_probe"] = probe
        print(json.dumps(result, allow_nan=False))
        return 0
    if not args.execute_authorized or not args.expected_revision:
        parser.error(
            "target execution requires approval acknowledgement and a frozen revision"
        )
    summary = execute_once(
        expected_revision=args.expected_revision, authorization_confirmed=True
    )
    print(json.dumps(summary, indent=2, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
