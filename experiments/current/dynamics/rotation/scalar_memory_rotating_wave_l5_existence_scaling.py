"""Execute the preregistered L5 rotating-wave existence and scaling gate."""

from __future__ import annotations

import argparse
from datetime import UTC, datetime
from decimal import Decimal
import hashlib
import json
from pathlib import Path
import subprocess
from typing import Any

from mpmath import mp

from emergenz_knoten.rotating_wave_interval import (
    IntervalRotatingWaveParameters,
    certify_rotating_wave_box,
    refine_rotating_wave_root,
)


def _repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("repository root not found")


ROOT = _repo_root()
PROTOCOL = Path(
    "reports/project/meta/preregistration/"
    "scalar_memory_rotating_wave_l5_existence_scaling_protocol_2026-08-21.md"
)
REFINEMENT_LADDER = Path(
    "reports/dynamics/rotation/"
    "scalar_memory_rotating_wave_refinement_ladder_2026-08-21.json"
)
FOUNDATION_AUDIT = Path(
    "reports/dynamics/rotation/"
    "scalar_memory_rotating_wave_foundation_audit_2026-08-21.json"
)
CONTINUUM_RECONCILIATION = Path(
    "reports/dynamics/rotation/"
    "scalar_memory_rotating_wave_continuum_reconciliation_2026-08-21.json"
)
DEFAULT_REPORT = Path(
    "reports/dynamics/rotation/"
    "scalar_memory_rotating_wave_l5_existence_scaling_2026-08-21.md"
)
DEFAULT_SUMMARY = Path(
    "reports/dynamics/rotation/"
    "scalar_memory_rotating_wave_l5_existence_scaling_2026-08-21.json"
)

EXPECTED_HASHES = {
    REFINEMENT_LADDER: (
        "1ba774daf0bf3395c1d0a356a31c8f5aab17eca76de7b32029f49b456cefb279"
    ),
    FOUNDATION_AUDIT: (
        "8ebc71a2e1f74a859e7aff4acc04bddade55617976ed13f8865826a1f2ad12ce"
    ),
    CONTINUUM_RECONCILIATION: (
        "8008f3846678e8920c1193468e1cacd078ff2c45b2903fbc4ac130431bd68658"
    ),
}
PROTOCOL_REVISION = "0add69c9898802f192984975786147429586fd8c"
LADDER_EXECUTION_REVISION = "b03ff433776ced084f8bf3d56b54b8fe7b1e5ef2"
FOUNDATION_EXECUTION_REVISION = "0bc74acf432f6a2f24cf5e78411441fc8dfa2555"

EXPECTED_LADDER_CELLS = (
    ("L0", "0.04", 300, "0.60"),
    ("L1", "0.02", 600, "0.30"),
    ("L2", "0.01", 1200, "0.15"),
    ("L3", "0.005", 2400, "0.075"),
    ("L4", "0.0025", 4800, "0.0375"),
)
L5_CELL = {"cell": "L5", "alpha": "0.00125", "horizon": 9600, "eta": "0.01875"}
PRECISION_PANELS = (80, 120)
NEWTON_ITERATIONS = 8
RADIUS_START = (
    "0.943957188362017621962796728889665465955595255173674745698318322703201904120534919460310738324071442073390305"
)
OMEGA_START = (
    "1.58345817054227476011136633656328035603531524285000037859953328942975445582475455451996353123520752489026474"
)
RADIUS_CORRIDOR = "0.01"
OMEGA_CORRIDOR = "0.01"
OUTER_RADIUS_HALF_WIDTH = "1e-6"
OUTER_OMEGA_HALF_WIDTH = "1e-6"
INNER_RADIUS_HALF_WIDTH = "1e-35"
INNER_OMEGA_HALF_WIDTH = "1e-35"
CROSS_PRECISION_TOLERANCE = "1e-55"
INNER_RADIUS_IMAGE_WIDTH_MAXIMUM = "1e-33"
INNER_OMEGA_IMAGE_WIDTH_MAXIMUM = "1e-33"

REPLAY_DPS = 70
REPLAY_RESIDUAL_MAXIMUM = "1e-45"
REPLAY_GAIN_ERROR_MAXIMUM = "1e-40"
CONTINUUM_RADIUS = (
    "0.9431133067695436321754560922340476968548404654598893868057171376405795"
)
CONTINUUM_OMEGA = (
    "1.585570077717788706778975148699744358665285143773149240644121542575246"
)
SLOPE_MINIMUM = "0.8"
SLOPE_MAXIMUM = "1.2"
CONTRACTION_MINIMUM = "0.4"
CONTRACTION_MAXIMUM = "0.6"
RICHARDSON_RELATIVE_MAXIMUM = "0.1"


def _git_output(arguments: list[str]) -> str:
    result = subprocess.run(
        ["git", *arguments],
        cwd=ROOT,
        capture_output=True,
        check=True,
        text=True,
    )
    return result.stdout.strip()


def _git_blob_sha256(path: Path) -> str:
    result = subprocess.run(
        ["git", "cat-file", "blob", f"HEAD:{path.as_posix()}"],
        cwd=ROOT,
        capture_output=True,
        check=True,
    )
    return hashlib.sha256(result.stdout).hexdigest()


def _revision_is_ancestor(revision: str) -> bool:
    exists = subprocess.run(
        ["git", "cat-file", "-e", f"{revision}^{{commit}}"],
        cwd=ROOT,
        capture_output=True,
        check=False,
        text=True,
    )
    if exists.returncode != 0:
        return False
    ancestor = subprocess.run(
        ["git", "merge-base", "--is-ancestor", revision, "HEAD"],
        cwd=ROOT,
        capture_output=True,
        check=False,
        text=True,
    )
    return ancestor.returncode == 0


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def input_hash_audit() -> dict[str, Any]:
    """Verify the exact frozen Git blobs, independent of checkout line endings."""

    rows = []
    for path, expected in EXPECTED_HASHES.items():
        observed = _git_blob_sha256(path)
        rows.append(
            {
                "path": path.as_posix(),
                "hash_domain": "git-head-blob",
                "expected_sha256": expected,
                "observed_sha256": observed,
                "pass": observed == expected,
            }
        )
    return {
        "hash_domain": "git-head-blob",
        "rows": rows,
        "pass": all(row["pass"] for row in rows),
    }


def exact_decimal_scaling(*, alpha: Any, horizon: int, eta: Any) -> tuple[bool, bool]:
    """Check the registered matched scalings in exact base-ten arithmetic."""

    decimal_alpha = Decimal(str(alpha))
    decimal_eta = Decimal(str(eta))
    return (
        decimal_alpha * Decimal(horizon) == Decimal("12"),
        decimal_eta == Decimal("15") * decimal_alpha,
    )


def _expected_ladder_rows(ladder: dict[str, Any]) -> list[tuple[str, str, int, str]]:
    return [
        (
            str(cell["cell"]),
            str(cell["alpha"]),
            int(cell["horizon"]),
            str(cell["eta"]),
        )
        for cell in ladder["cells"]
    ]


def provenance_audit(
    ladder: dict[str, Any],
    foundation: dict[str, Any],
    continuum: dict[str, Any],
) -> dict[str, Any]:
    hashes = input_hash_audit()
    revisions = {
        "protocol": PROTOCOL_REVISION,
        "ladder_execution": LADDER_EXECUTION_REVISION,
        "foundation_execution": FOUNDATION_EXECUTION_REVISION,
    }
    revision_rows = [
        {
            "stage": stage,
            "revision": revision,
            "exists_and_is_ancestor": _revision_is_ancestor(revision),
        }
        for stage, revision in revisions.items()
    ]
    l4 = next((cell for cell in ladder["cells"] if cell["cell"] == "L4"), None)
    if l4 is None:
        l4_start_match = False
    else:
        panel = max(l4["panels"], key=lambda row: row["precision_dps"])
        l4_start_match = bool(
            panel["refined"]["radius"] == RADIUS_START
            and panel["omega"] == OMEGA_START
        )
    continuum_panel = next(
        (
            panel
            for panel in foundation.get("continuum_replay", {}).get("panels", [])
            if panel.get("name") == "mp-gl-70"
        ),
        None,
    )
    tail_scaling, gain_scaling = exact_decimal_scaling(**{
        "alpha": L5_CELL["alpha"],
        "horizon": L5_CELL["horizon"],
        "eta": L5_CELL["eta"],
    })
    source_gates = {
        "ladder_execution_revision": (
            ladder.get("execution_revision") == LADDER_EXECUTION_REVISION
        ),
        "foundation_execution_revision": (
            foundation.get("execution_revision") == FOUNDATION_EXECUTION_REVISION
        ),
        "historical_ladder_preserved": bool(
            ladder.get("decision") == "certified-roots-nonconvergent"
            and ladder.get("all_cells_certified")
            and ladder.get("anchor_overlap")
        ),
        "ladder_cells_exact": (
            _expected_ladder_rows(ladder) == list(EXPECTED_LADDER_CELLS)
        ),
        "l4_transfer_center_exact": l4_start_match,
        "foundation_pass_scoped": bool(
            foundation.get("decision")
            == "foundation-audit-portability-reconciliation-pass-scoped"
            and foundation.get("stored_reconciliation_pass")
            and all(foundation.get("gates", {}).values())
        ),
        "l5_was_sealed": foundation.get("sealed_next_cell")
        == {
            "alpha": L5_CELL["alpha"],
            "eta": L5_CELL["eta"],
            "horizon": L5_CELL["horizon"],
            "status": "sealed-not-evaluated-by-foundation-audit",
        },
        "continuum_reconciliation_pass": bool(
            continuum.get("decision") == "fixed-gain-continuum-reconciliation-pass"
            and continuum.get("scaling", {}).get("pass")
        ),
        "continuum_target_exact": bool(
            continuum_panel is not None
            and continuum_panel.get("radius") == CONTINUUM_RADIUS
            and continuum_panel.get("omega") == CONTINUUM_OMEGA
        ),
        "l5_tail_scaling_exact": tail_scaling,
        "l5_gain_scaling_exact": gain_scaling,
    }
    return {
        "input_hashes": hashes,
        "revisions": revision_rows,
        "source_gates": source_gates,
        "pass": bool(
            hashes["pass"]
            and all(row["exists_and_is_ancestor"] for row in revision_rows)
            and all(source_gates.values())
        ),
    }


def _parameters() -> IntervalRotatingWaveParameters:
    return IntervalRotatingWaveParameters(
        alpha=L5_CELL["alpha"],
        horizon=L5_CELL["horizon"],
        memory_mass="1.0",
        eta=L5_CELL["eta"],
        sigma_rep="1.0",
        sigma_att="3.0",
        amplitude_rep="1.0",
        amplitude_att="3.5",
    )


def _scaled(value: str, alpha: str, precision: int = 180) -> str:
    with mp.workdps(precision):
        return mp.nstr(mp.mpf(value) * mp.mpf(alpha), precision - 20)


def _record_endpoints(record: dict[str, Any]) -> tuple[Any, Any]:
    lower = tuple(int(value) for value in record["lower_binary"])
    upper = tuple(int(value) for value in record["upper_binary"])
    return mp.make_mpf(lower), mp.make_mpf(upper)


def _records_overlap(first: dict[str, Any], second: dict[str, Any]) -> bool:
    with mp.workdps(180):
        first_lower, first_upper = _record_endpoints(first)
        second_lower, second_upper = _record_endpoints(second)
        return bool(max(first_lower, second_lower) <= min(first_upper, second_upper))


def _record_width_below(record: dict[str, Any], threshold: str) -> bool:
    with mp.workdps(180):
        lower, upper = _record_endpoints(record)
        return bool(upper - lower < mp.mpf(threshold))


def _record_omega_width_below(record: dict[str, Any], threshold: str) -> bool:
    with mp.workdps(180):
        lower, upper = _record_endpoints(record)
        return bool(
            (upper - lower) / mp.mpf(L5_CELL["alpha"]) < mp.mpf(threshold)
        )


def _corridor_pass(iterates: list[dict[str, str]]) -> bool:
    with mp.workdps(180):
        alpha = mp.mpf(L5_CELL["alpha"])
        return all(
            abs(mp.mpf(row["radius"]) - mp.mpf(RADIUS_START))
            < mp.mpf(RADIUS_CORRIDOR)
            and abs(mp.mpf(row["theta"]) / alpha - mp.mpf(OMEGA_START))
            < mp.mpf(OMEGA_CORRIDOR)
            for row in iterates
        )


def _panel(precision_dps: int) -> dict[str, Any]:
    initial_theta = _scaled(OMEGA_START, L5_CELL["alpha"])
    refined = refine_rotating_wave_root(
        radius=RADIUS_START,
        theta=initial_theta,
        parameters=_parameters(),
        precision_dps=precision_dps,
        iterations=NEWTON_ITERATIONS,
    )
    outer = certify_rotating_wave_box(
        radius=refined["radius"],
        theta=refined["theta"],
        radius_half_width=OUTER_RADIUS_HALF_WIDTH,
        theta_half_width=_scaled(OUTER_OMEGA_HALF_WIDTH, L5_CELL["alpha"]),
        parameters=_parameters(),
        precision_dps=precision_dps,
    )
    inner = certify_rotating_wave_box(
        radius=refined["radius"],
        theta=refined["theta"],
        radius_half_width=INNER_RADIUS_HALF_WIDTH,
        theta_half_width=_scaled(INNER_OMEGA_HALF_WIDTH, L5_CELL["alpha"]),
        parameters=_parameters(),
        precision_dps=precision_dps,
    )
    with mp.workdps(180):
        omega = mp.mpf(refined["theta"]) / mp.mpf(L5_CELL["alpha"])
        residual_maximum = max(abs(mp.mpf(value)) for value in refined["balance"])
        residual_threshold = mp.mpf(10) ** (-(precision_dps - 20))
    gates = {
        "newton_corridor": _corridor_pass(refined["iterates"]),
        "outer_certificate": bool(outer["pass"]),
        "inner_certificate": bool(inner["pass"]),
        "point_residual": bool(residual_maximum <= residual_threshold),
        "inner_radius_image_width": _record_width_below(
            inner["krawczyk_image"][0], INNER_RADIUS_IMAGE_WIDTH_MAXIMUM
        ),
        "inner_omega_image_width": _record_omega_width_below(
            inner["krawczyk_image"][1], INNER_OMEGA_IMAGE_WIDTH_MAXIMUM
        ),
    }
    return {
        "precision_dps": precision_dps,
        "initial": {"radius": RADIUS_START, "theta": initial_theta},
        "refined": refined,
        "omega": mp.nstr(omega, precision_dps - 12),
        "point_residual_maximum": mp.nstr(residual_maximum, 20),
        "point_residual_threshold": mp.nstr(residual_threshold, 20),
        "outer": outer,
        "inner": inner,
        "gates": gates,
        "pass": all(gates.values()),
    }


def _cross_precision(panels: list[dict[str, Any]]) -> dict[str, Any]:
    with mp.workdps(180):
        radius_difference = abs(
            mp.mpf(panels[0]["refined"]["radius"])
            - mp.mpf(panels[1]["refined"]["radius"])
        )
        omega_difference = abs(
            mp.mpf(panels[0]["omega"]) - mp.mpf(panels[1]["omega"])
        )
        center_agreement = bool(
            radius_difference <= mp.mpf(CROSS_PRECISION_TOLERANCE)
            and omega_difference <= mp.mpf(CROSS_PRECISION_TOLERANCE)
        )
    enclosure_overlap = all(
        _records_overlap(
            panels[0]["inner"]["krawczyk_image"][index],
            panels[1]["inner"]["krawczyk_image"][index],
        )
        for index in range(2)
    )
    return {
        "radius_difference": mp.nstr(radius_difference, 20),
        "omega_difference": mp.nstr(omega_difference, 20),
        "center_agreement": center_agreement,
        "inner_enclosure_overlap": enclosure_overlap,
        "pass": bool(center_agreement and enclosure_overlap),
    }


def run_l5_cell() -> dict[str, Any]:
    panels = [_panel(precision) for precision in PRECISION_PANELS]
    cross_precision = _cross_precision(panels)
    return {
        **L5_CELL,
        "panels": panels,
        "cross_precision": cross_precision,
        "pass": bool(all(panel["pass"] for panel in panels) and cross_precision["pass"]),
    }


def independent_finite_balance(
    *,
    radius: Any,
    theta: Any,
    alpha: Any,
    horizon: int,
    eta: Any,
) -> tuple[Any, Any, Any, Any]:
    """Evaluate the frozen finite sums without importing a project evaluator."""

    radius = mp.mpf(radius)
    theta = mp.mpf(theta)
    alpha = mp.mpf(alpha)
    eta = mp.mpf(eta)
    forgetting_q = 1 - alpha
    weight = alpha
    radial_sum = mp.zero
    tangential_sum = mp.zero
    for age in range(1, int(horizon)):
        weight *= forgetting_q
        phase = age * theta
        chord_factor = 1 - mp.cos(phase)
        chi = radius**2 * chord_factor
        gradient_factor = -mp.exp(-chi) + mp.mpf("3.5") / 9 * mp.exp(-chi / 9)
        radial_sum += weight * gradient_factor * chord_factor
        tangential_sum += weight * gradient_factor * mp.sin(phase)
    radial_residual = mp.cos(theta) - 1 + eta * radial_sum
    tangential_residual = mp.sin(theta) + eta * tangential_sum
    return radial_residual, tangential_residual, radial_sum, tangential_sum


def independent_replay(cell: dict[str, Any]) -> dict[str, Any]:
    panel = max(cell["panels"], key=lambda row: row["precision_dps"])
    with mp.workdps(REPLAY_DPS):
        radius = mp.mpf(panel["refined"]["radius"])
        theta = mp.mpf(panel["refined"]["theta"])
        eta = mp.mpf(L5_CELL["eta"])
        residual_r, residual_t, radial_sum, tangential_sum = independent_finite_balance(
            radius=radius,
            theta=theta,
            alpha=L5_CELL["alpha"],
            horizon=L5_CELL["horizon"],
            eta=eta,
        )
        residual_maximum = max(abs(residual_r), abs(residual_t))
        radial_eta = (1 - mp.cos(theta)) / radial_sum
        tangential_eta = -mp.sin(theta) / tangential_sum
        gain_error = max(abs(radial_eta - eta), abs(tangential_eta - eta))
        tail_scaling, gain_scaling = exact_decimal_scaling(
            alpha=L5_CELL["alpha"],
            horizon=L5_CELL["horizon"],
            eta=L5_CELL["eta"],
        )
        gates = {
            "residual": residual_maximum <= mp.mpf(REPLAY_RESIDUAL_MAXIMUM),
            "physical_signs": radial_sum > 0 and tangential_sum < 0,
            "gain": gain_error <= mp.mpf(REPLAY_GAIN_ERROR_MAXIMUM),
            "tail_scaling": tail_scaling,
            "gain_scaling": gain_scaling,
        }
        return {
            "precision_dps": REPLAY_DPS,
            "radius": mp.nstr(radius, 40),
            "theta": mp.nstr(theta, 40),
            "radial_residual": mp.nstr(residual_r, 30),
            "tangential_residual": mp.nstr(residual_t, 30),
            "residual_maximum": mp.nstr(residual_maximum, 20),
            "radial_sum": mp.nstr(radial_sum, 30),
            "tangential_sum": mp.nstr(tangential_sum, 30),
            "radial_eta": mp.nstr(radial_eta, 30),
            "tangential_eta": mp.nstr(tangential_eta, 30),
            "gain_error_maximum": mp.nstr(gain_error, 20),
            "gates": gates,
            "pass": all(gates.values()),
            "semantics": "independent finite-sum replay, not a second interval proof",
        }


def _cell_center(cell: dict[str, Any]) -> tuple[Any, Any, Any]:
    panel = max(cell["panels"], key=lambda row: row["precision_dps"])
    return (
        mp.mpf(str(cell["alpha"])),
        mp.mpf(panel["refined"]["radius"]),
        mp.mpf(panel["omega"]),
    )


def scaling_diagnostics(
    ladder_cells: list[dict[str, Any]], l5_cell: dict[str, Any]
) -> dict[str, Any]:
    """Evaluate only the preregistered L0--L5 scaling diagnostics."""

    with mp.workdps(REPLAY_DPS):
        cells = sorted(
            [*ladder_cells, l5_cell],
            key=lambda row: mp.mpf(str(row["alpha"])),
            reverse=True,
        )
        centers = [_cell_center(cell) for cell in cells]
        alphas = [center[0] for center in centers]
        radii = [center[1] for center in centers]
        omegas = [center[2] for center in centers]
        target_radius = mp.mpf(CONTINUUM_RADIUS)
        target_omega = mp.mpf(CONTINUUM_OMEGA)

        def diagnostics(values: list[Any], target: Any) -> dict[str, Any]:
            signed_errors = [value - target for value in values]
            errors = list(map(abs, signed_errors))
            fit = [
                (mp.log(alpha), mp.log(error))
                for alpha, error in zip(alphas, errors, strict=True)
                if alpha <= mp.mpf("0.02")
            ]
            mean_x = mp.fsum(row[0] for row in fit) / len(fit)
            mean_y = mp.fsum(row[1] for row in fit) / len(fit)
            slope = mp.fsum(
                (x - mean_x) * (y - mean_y) for x, y in fit
            ) / mp.fsum((x - mean_x) ** 2 for x, _ in fit)
            signed_error_contraction = signed_errors[-1] / signed_errors[-2]
            successive_difference_contraction = (
                (values[-1] - values[-2]) / (values[-2] - values[-3])
            )
            richardson = 2 * values[-1] - values[-2]
            richardson_relative = abs(richardson - target) / errors[-1]
            gates = {
                "positive_errors": all(error > 0 for error in errors),
                "strict_error_monotonicity": all(
                    latter < former for former, latter in zip(errors, errors[1:])
                ),
                "slope": mp.mpf(SLOPE_MINIMUM) <= slope <= mp.mpf(SLOPE_MAXIMUM),
                "signed_error_contraction": (
                    mp.mpf(CONTRACTION_MINIMUM)
                    <= signed_error_contraction
                    <= mp.mpf(CONTRACTION_MAXIMUM)
                ),
                "successive_difference_contraction": (
                    mp.mpf(CONTRACTION_MINIMUM)
                    <= successive_difference_contraction
                    <= mp.mpf(CONTRACTION_MAXIMUM)
                ),
                "richardson": (
                    richardson_relative <= mp.mpf(RICHARDSON_RELATIVE_MAXIMUM)
                ),
            }
            return {
                "signed_errors": signed_errors,
                "errors": errors,
                "slope": slope,
                "signed_error_contraction": signed_error_contraction,
                "successive_difference_contraction": successive_difference_contraction,
                "richardson": richardson,
                "richardson_relative_error": richardson_relative,
                "gates": gates,
                "pass": all(gates.values()),
            }

        radius = diagnostics(radii, target_radius)
        omega = diagnostics(omegas, target_omega)
        rows = [
            {
                "cell": cell["cell"],
                "alpha": mp.nstr(alphas[index], 20),
                "radius": mp.nstr(radii[index], 40),
                "omega": mp.nstr(omegas[index], 40),
                "radius_signed_error": mp.nstr(radius["signed_errors"][index], 25),
                "omega_signed_error": mp.nstr(omega["signed_errors"][index], 25),
                "radius_error": mp.nstr(radius["errors"][index], 25),
                "omega_error": mp.nstr(omega["errors"][index], 25),
            }
            for index, cell in enumerate(cells)
        ]

        def serialize(result: dict[str, Any]) -> dict[str, Any]:
            return {
                "slope": mp.nstr(result["slope"], 25),
                "signed_error_contraction": mp.nstr(
                    result["signed_error_contraction"], 25
                ),
                "successive_difference_contraction": mp.nstr(
                    result["successive_difference_contraction"], 25
                ),
                "richardson": mp.nstr(result["richardson"], 40),
                "richardson_relative_error": mp.nstr(
                    result["richardson_relative_error"], 25
                ),
                "gates": result["gates"],
                "pass": result["pass"],
            }

        return {
            "precision_dps": REPLAY_DPS,
            "target_radius": CONTINUUM_RADIUS,
            "target_omega": CONTINUUM_OMEGA,
            "rows": rows,
            "radius": serialize(radius),
            "omega": serialize(omega),
            "pass": bool(radius["pass"] and omega["pass"]),
        }


def run_gate() -> dict[str, Any]:
    start_status = _git_output(["status", "--short"])
    if start_status:
        raise RuntimeError("L5 gate requires a clean prospective execution revision")
    execution_revision = _git_output(["rev-parse", "HEAD"])
    try:
        ladder = _load_json(REFINEMENT_LADDER)
        foundation = _load_json(FOUNDATION_AUDIT)
        continuum = _load_json(CONTINUUM_RECONCILIATION)
        provenance = provenance_audit(ladder, foundation, continuum)
        if not provenance["pass"]:
            raise RuntimeError("frozen provenance or input gate failed")
        l5 = run_l5_cell()
        replay = independent_replay(l5)
        scaling = scaling_diagnostics(ladder["cells"], l5)
        existence_pass = bool(l5["pass"] and replay["pass"])
        if existence_pass and scaling["pass"]:
            decision = "l5-existence-scaling-pass"
        elif existence_pass:
            decision = "l5-existence-pass-scaling-fail"
        else:
            decision = "l5-existence-inconclusive"
        exception = None
    except Exception as error:  # pragma: no cover - result-path safeguard
        provenance = locals().get("provenance")
        l5 = locals().get("l5")
        replay = locals().get("replay")
        scaling = locals().get("scaling")
        existence_pass = False
        decision = "l5-existence-inconclusive"
        exception = f"{type(error).__name__}: {error}"

    return {
        "schema": "emergenz-knoten.scalar-memory-rotating-wave-l5-existence-scaling",
        "schema_version": 1,
        "generated_utc": datetime.now(UTC).isoformat(),
        "execution_revision": execution_revision,
        "git_status_at_start": start_status,
        "protocol": PROTOCOL.as_posix(),
        "protocol_revision": PROTOCOL_REVISION,
        "registration": {
            "cell": L5_CELL,
            "precision_panels_dps": list(PRECISION_PANELS),
            "newton_iterations": NEWTON_ITERATIONS,
            "radius_start": RADIUS_START,
            "omega_start": OMEGA_START,
            "radius_corridor": RADIUS_CORRIDOR,
            "omega_corridor": OMEGA_CORRIDOR,
            "outer_radius_half_width": OUTER_RADIUS_HALF_WIDTH,
            "outer_omega_half_width": OUTER_OMEGA_HALF_WIDTH,
            "inner_radius_half_width": INNER_RADIUS_HALF_WIDTH,
            "inner_omega_half_width": INNER_OMEGA_HALF_WIDTH,
            "independent_replay_dps": REPLAY_DPS,
            "continuum_radius": CONTINUUM_RADIUS,
            "continuum_omega": CONTINUUM_OMEGA,
            "sealed_amplitude_holdout": 7.0,
            "stability_opened": False,
            "topology_opened": False,
            "interactions_opened": False,
        },
        "provenance": provenance,
        "l5_cell": l5,
        "independent_replay": replay,
        "scaling": scaling,
        "existence_pass": existence_pass,
        "decision": decision,
        "exception": exception,
        "claim_boundary": {
            "established_if_pass": (
                "one locally unique L5 finite-H balance root in each declared "
                "box, conditional on the mpmath.iv Krawczyk trust base, and "
                "finite L0-L5 first-order numerical scaling evidence"
            ),
            "not_established": (
                "all-alpha convergence, global uniqueness, non-anchor stability, "
                "generic formation, internal S1, torus, intrinsic spin, work, "
                "inertia, mass, or interactions"
            ),
        },
    }


def _fmt(value: Any) -> str:
    if value is None:
        return "--"
    try:
        return f"{float(value):.10g}"
    except (TypeError, ValueError):
        return str(value)


def render_report(payload: dict[str, Any]) -> str:
    lines = [
        "# Scalar-memory rotating-wave L5 existence and scaling gate",
        "",
        f"Generated: {payload['generated_utc']}.",
        "",
        f"Decision: **{payload['decision']}**.",
        "",
        f"Execution revision: `{payload['execution_revision']}`.",
        f"Frozen protocol revision: `{payload['protocol_revision']}`.",
        "",
    ]
    if payload["exception"] is not None:
        lines.extend(
            [
                "## Inconclusive execution",
                "",
                payload["exception"],
                "",
                "No positive existence or scaling claim is authorized.",
                "",
            ]
        )
        return "\n".join(lines)

    l5 = payload["l5_cell"]
    replay = payload["independent_replay"]
    scaling = payload["scaling"]
    lines.extend(
        [
            "## Provenance",
            "",
            f"Frozen input/protocol gate: **{payload['provenance']['pass']}**.",
            "The hash domain is the exact versioned `HEAD:path` Git blob.",
            "",
            "## L5 interval panels",
            "",
            "| dps | R | Omega | point residual | outer | inner | panel |",
            "| ---: | ---: | ---: | ---: | :---: | :---: | :---: |",
        ]
    )
    for panel in l5["panels"]:
        lines.append(
            "| "
            f"{panel['precision_dps']} | {_fmt(panel['refined']['radius'])} | "
            f"{_fmt(panel['omega'])} | {_fmt(panel['point_residual_maximum'])} | "
            f"{panel['outer']['pass']} | {panel['inner']['pass']} | "
            f"{panel['pass']} |"
        )
    lines.extend(
        [
            "",
            f"Cross-precision agreement and enclosure overlap: **{l5['cross_precision']['pass']}**.",
            "",
            "Strict Krawczyk interior inclusion is the local existence and",
            "box-uniqueness certificate. The two precision panels are not",
            "independent interval implementations or a proof-assistant check.",
            "",
            "## Independent finite-sum replay",
            "",
            f"Replay pass: **{replay['pass']}**.",
            "",
            f"- maximum residual: `{replay['residual_maximum']}`",
            f"- maximum gain error: `{replay['gain_error_maximum']}`",
            f"- radial/tangential signs: `{replay['gates']['physical_signs']}`",
            "",
            "This replay checks signs, indexing and arithmetic; it is not a",
            "second interval proof.",
            "",
            "## L0--L5 scaling",
            "",
            "| cell | alpha | R error | Omega error |",
            "| --- | ---: | ---: | ---: |",
        ]
    )
    for row in scaling["rows"]:
        lines.append(
            f"| {row['cell']} | {row['alpha']} | "
            f"{_fmt(row['radius_error'])} | {_fmt(row['omega_error'])} |"
        )
    lines.extend(
        [
            "",
            "| observable | slope | signed error ratio | difference ratio | Richardson rel. | pass |",
            "| --- | ---: | ---: | ---: | ---: | :---: |",
        ]
    )
    for name in ("radius", "omega"):
        row = scaling[name]
        lines.append(
            f"| {name} | {_fmt(row['slope'])} | "
            f"{_fmt(row['signed_error_contraction'])} | "
            f"{_fmt(row['successive_difference_contraction'])} | "
            f"{_fmt(row['richardson_relative_error'])} | {row['pass']} |"
        )
    lines.extend(
        [
            "",
            "## Claim boundary",
            "",
            "A full pass supports one locally unique L5 prepared-loop balance",
            "root in the declared boxes and finite L0--L5 first-order scaling.",
            "It does not establish a stable family, spontaneous formation, an",
            "internal phase or torus, intrinsic spin, mechanics or interactions.",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = run_gate()
    report_path = ROOT / args.report
    summary_path = ROOT / args.summary
    report_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(render_report(payload), encoding="utf-8")
    summary_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    print(f"Decision: {payload['decision']}")
    print(f"Report: {report_path.relative_to(ROOT)}")
    print(f"Summary: {summary_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
