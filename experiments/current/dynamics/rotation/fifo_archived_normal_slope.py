"""One authorized archive-only slope check per precision; no new model evaluations."""

from __future__ import annotations

import argparse
from decimal import Decimal, localcontext
from fractions import Fraction
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

from emergenz_knoten.fifo_normal_stability import normal_translation_slope

from . import fifo_normal_anchor as anchor


ARCHIVE_REVISION = "fdbd24fd437187a4db185d413f4c3bd022104b3b"
ARCHIVE_EXECUTION = "16f60f5a12281628a55eb5e591fe027418d21a3a"
ARCHIVE_PATH = "reports/dynamics/rotation/fifo_normal_anchor_attempt_1_2026-10-25"
OUTPUT_REL = Path("reports/dynamics/rotation/fifo_archived_normal_slope_2026-10-26")
PRECISIONS = (80, 120)
SECONDS = 30
CERTIFIED = "positive-real-normal-mode-certified"
UNRESOLVED = "not-established"
SCHEMA = "fifo-archived-normal-slope-v1"


def binary_fraction(raw: list[int]) -> Fraction:
    if type(raw) is not list or len(raw) != 4 or any(type(x) is not int for x in raw):
        raise ValueError("expected four integer binary endpoint fields")
    sign, mantissa, exponent, bitcount = raw
    if (
        sign not in (0, 1)
        or mantissa < 0
        or bitcount != mantissa.bit_length()
        or (mantissa == 0 and raw != [0, 0, 0, 0])
        or (mantissa != 0 and mantissa % 2 != 1)
        or abs(exponent) > 100_000
    ):
        raise ValueError("invalid, nonfinite or out-of-budget binary endpoint")
    return (-1 if sign else 1) * Fraction(mantissa) * Fraction(2) ** exponent


def interval_bounds(record: dict) -> tuple[Fraction, Fraction]:
    lower = binary_fraction(record["lower_binary"])
    upper = binary_fraction(record["upper_binary"])
    if lower > upper:
        raise ValueError("reversed interval bounds")
    return lower, upper


def fraction_record(value: Fraction) -> dict:
    with localcontext() as context:
        context.prec = 25
        approximate = str(Decimal(value.numerator) / Decimal(value.denominator))
    return {
        "numerator": str(value.numerator),
        "denominator": str(value.denominator),
        "approximate_decimal_not_used_for_decision": approximate,
    }


def read_fraction(record: dict) -> Fraction:
    return Fraction(int(record["numerator"]), int(record["denominator"]))


def evaluate_polynomial(records: list[dict]) -> dict:
    """Exact interval sum from descending [1, sum(c)-1, -c1, ...]."""
    if len(records) < 3:
        raise ValueError("expected at least one lag")
    bounds = [interval_bounds(record) for record in records]
    if bounds[0] != (1, 1):
        raise ValueError("expected exactly monic polynomial")
    couplings = [(-upper, -lower) for lower, upper in bounds[2:]]
    # b0 is dependent: use translation identity, not independent polynomial sums.
    dependent = (sum(c[0] for c in couplings) - 1, sum(c[1] for c in couplings) - 1)
    if max(dependent[0], bounds[1][0]) > min(dependent[1], bounds[1][1]):
        raise ValueError("coefficient box incompatible with translation identity")
    lower = normal_translation_slope([c[0] for c in couplings])
    upper = normal_translation_slope([c[1] for c in couplings])
    return {
        "decision": CERTIFIED if upper < 0 else UNRESOLVED,
        "lag_count": len(couplings),
        "slope": {"lower": fraction_record(lower), "upper": fraction_record(upper)},
        "arithmetic": "exact fractions of archived binary endpoints",
        "trust_basis": "archived root/coefficient enclosure from mpmath.iv; no recertification",
    }


def load_archive(name: str) -> tuple[dict, dict]:
    path = f"{ARCHIVE_PATH}/{name}"
    raw = anchor._git("cat-file", "blob", f"{ARCHIVE_REVISION}:{path}")
    return json.loads(raw), {
        "revision": ARCHIVE_REVISION,
        "path": path,
        "sha256_git_blob_bytes": hashlib.sha256(raw).hexdigest(),
    }


def validate_panel(panel: dict, inputs: dict, precision: int) -> dict:
    if panel.get("status") != "completed" or panel.get("precision_dps") != precision:
        raise ValueError("archive panel incomplete or precision mismatch")
    result = panel["result"]
    anchor._validate_worker_result(result, inputs, precision)
    if (
        result["decision"] != "inconclusive"
        or result["root_certificate"]["pass"] is not True
        or not result["root_certificate"]["gates"]
    ):
        raise ValueError(
            "expected the archived certified-root, inconclusive-Schur panel"
        )
    return result


def worker(precision: int, inputs: dict) -> dict:
    panel, provenance = load_archive(f"panel_{precision}.json")
    result = validate_panel(panel, inputs, precision)
    return {
        "schema": SCHEMA,
        "precision_dps": precision,
        "source": provenance,
        "archived_schur_decision": result["decision"],
        **evaluate_polynomial(result["normal_polynomial"]),
    }


def capture(command: list[str], inputs: dict, *, seconds: float = SECONDS) -> dict:
    start = time.monotonic()
    record = {"status": "error", "started_utc": anchor._utc(), "result": None}
    try:
        with subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            cwd=anchor.ROOT,
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
                record["status"] = "timeout"
            except BaseException:
                process.kill()
                process.wait()
                raise
        record.update(returncode=process.returncode, stderr=stderr)
        if record["status"] == "timeout" or process.returncode != 0:
            record["stdout"] = stdout
        else:
            record.update(status="completed", result=json.loads(stdout))
    except Exception as error:
        record["error"] = f"{type(error).__name__}: {error}"
    record.update(elapsed_seconds=time.monotonic() - start, finished_utc=anchor._utc())
    return record


def classify(panels: list[dict]) -> str:
    if [p["precision_dps"] for p in panels] != list(PRECISIONS):
        raise ValueError("expected exactly ordered 80/120 panels")
    if any(p["status"] != "completed" for p in panels):
        return UNRESOLVED
    bounds = [
        tuple(read_fraction(p["result"]["slope"][key]) for key in ("lower", "upper"))
        for p in panels
    ]
    if max(b[0] for b in bounds) > min(b[1] for b in bounds):
        return "method-inconsistent"
    return CERTIFIED if all(b[1] < 0 for b in bounds) else UNRESOLVED


def execute_once(
    *, expected_revision: str, authorization_confirmed: bool = False
) -> dict:
    if authorization_confirmed is not True:
        raise PermissionError("explicit author approval required")
    metadata = anchor._execution_metadata(expected_revision)
    inputs, root_provenance = anchor.load_registered_input()
    old_receipt, provenance = load_archive("receipt.json")
    if (
        old_receipt["inputs"] != inputs
        or old_receipt["metadata"]["execution_revision"] != ARCHIVE_EXECUTION
        or old_receipt["metadata"]["git_status_at_start"] != ""
        or old_receipt["metadata"]["source"] != root_provenance
    ):
        raise ValueError("archive receipt provenance mismatch")
    directory = anchor.ROOT / OUTPUT_REL
    directory.mkdir(parents=True, exist_ok=False)
    receipt = {
        "schema": SCHEMA,
        "metadata": metadata,
        "inputs": inputs,
        "archive_receipt": provenance,
        "started_utc": anchor._utc(),
        "precision_panels": list(PRECISIONS),
        "seconds_per_panel": SECONDS,
        "authorization": "User approved only archived coefficients, once per 80/120 dataset, at most 30 seconds each; no simulation, search or retry.",
    }
    anchor._write_json(directory / "receipt.json", receipt)
    panels = []
    for precision in PRECISIONS:
        anchor._write_json(
            directory / f"panel_{precision}_started.json",
            {"precision_dps": precision, "started_utc": anchor._utc()},
        )
        command = [sys.executable, "-m", __spec__.name, "--worker", str(precision)]
        panel = capture(command, inputs)
        panel["precision_dps"] = precision
        if panel["status"] == "completed":
            result = panel["result"]
            if (
                result.get("schema") != SCHEMA
                or result.get("precision_dps") != precision
            ):
                panel.update(status="error", error="worker result identity mismatch")
        anchor._write_json(directory / f"panel_{precision}.json", panel)
        panels.append(panel)
    summary = {
        "schema": SCHEMA,
        "metadata": metadata,
        "decision": classify(panels),
        "panels": panels,
        "finished_utc": anchor._utc(),
        "claim_boundary": "S<0 certifies existence of a real normal form multiplier >1 at this archived circle, conditional on the original root/coefficient enclosure. No exact rate, nonlinear fate, formation or general-model conclusion. Other outcomes do not establish stability.",
    }
    anchor._write_json(directory / "summary.json", summary)
    return summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execute-authorized", action="store_true")
    parser.add_argument("--expected-revision")
    parser.add_argument(
        "--worker", type=int, choices=PRECISIONS, help=argparse.SUPPRESS
    )
    args = parser.parse_args(argv)
    if args.worker is not None:
        result = worker(args.worker, json.load(sys.stdin))
    else:
        if not args.execute_authorized or not args.expected_revision:
            parser.error(
                "requires explicit approval acknowledgement and frozen revision"
            )
        result = execute_once(
            expected_revision=args.expected_revision, authorization_confirmed=True
        )
    print(json.dumps(result, indent=2, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
