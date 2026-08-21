"""Audit the immutable native rotating-wave evidence chain independently."""

from __future__ import annotations

import argparse
from collections.abc import Callable
from datetime import UTC, datetime
from decimal import Decimal
import hashlib
import json
import math
from pathlib import Path
import subprocess
from typing import Any

from mpmath import mp


def _repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("repository root not found")


ROOT = _repo_root()
PROTOCOL = Path(
    "reports/project/meta/preregistration/"
    "scalar_memory_rotating_wave_foundation_portability_reconciliation_protocol_"
    "2026-08-21.md"
)
DEFAULT_REPORT = Path(
    "reports/dynamics/rotation/"
    "scalar_memory_rotating_wave_foundation_audit_2026-08-21.md"
)
DEFAULT_SUMMARY = Path(
    "reports/dynamics/rotation/"
    "scalar_memory_rotating_wave_foundation_audit_2026-08-21.json"
)

DISCOVERY = Path(
    "reports/dynamics/rotation/"
    "scalar_memory_rotating_wave_discovery_2026-08-20.json"
)
INITIAL_STATE = Path(
    "reports/dynamics/rotation/"
    "scalar_memory_rotating_wave_initial_state_spec_2026-08-20.json"
)
P0_MANIFEST = Path(
    "reports/project/meta/preregistration/"
    "scalar_memory_rotating_wave_p0_manifest_2026-08-20.json"
)
P0_AUDIT = Path(
    "reports/project/meta/preregistration/"
    "scalar_memory_rotating_wave_p0_audit_2026-08-20.json"
)
D0_CONTRACT = Path(
    "reports/project/meta/preregistration/"
    "scalar_memory_rotating_wave_d0_contract_2026-08-20.md"
)
STABILITY = Path(
    "reports/dynamics/rotation/"
    "scalar_memory_rotating_wave_stability_2026-08-20.json"
)
INTERVAL_CERTIFICATE = Path(
    "reports/dynamics/rotation/"
    "scalar_memory_rotating_wave_interval_certificate_2026-08-21.json"
)
REFINEMENT_LADDER = Path(
    "reports/dynamics/rotation/"
    "scalar_memory_rotating_wave_refinement_ladder_2026-08-21.json"
)
CONTINUUM_RECONCILIATION = Path(
    "reports/dynamics/rotation/"
    "scalar_memory_rotating_wave_continuum_reconciliation_2026-08-21.json"
)

EXPECTED_HASHES = {
    DISCOVERY: "f9c6409fccd9b3e02c83497428a24ad2d5dfb78d2134bfe4314baaec9e13e830",
    INITIAL_STATE: "4ab3f657cfa68bcd38d73c0722cd718a94e413b33fc46c17bb995b3637808dd2",
    P0_MANIFEST: "3d89d2fe390c24765b23a834ad682b626f5ce3025b44f508afb1509b7fd6efb1",
    P0_AUDIT: "1ab03eddb4d19d41c14abb3d5e289a6b607e558ebc6d66bc2624c99c70d4329e",
    D0_CONTRACT: "4ad70cd38efb87e97509fe253987a6ac0a6dce9555cc37457eaba54a5f822bb2",
    STABILITY: "43b0d7f5e5ba81dc35d4a2e9d138d3663a3d98b67bcb09ed2d4572d5a01eb86f",
    INTERVAL_CERTIFICATE: (
        "63dc4158c0d8a9543230b656b7602feef76a48a2a75fbe6a6e001cb81082a840"
    ),
    REFINEMENT_LADDER: (
        "1ba774daf0bf3395c1d0a356a31c8f5aab17eca76de7b32029f49b456cefb279"
    ),
    CONTINUUM_RECONCILIATION: (
        "8008f3846678e8920c1193468e1cacd078ff2c45b2903fbc4ac130431bd68658"
    ),
}

CANDIDATE_ID = "k0h-rw-aatt3p5-alpha1e-2-h1200-eta0p15-v1"
EXPECTED_LADDER_CELLS = (
    ("L0", "0.04", 300, "0.60"),
    ("L1", "0.02", 600, "0.30"),
    ("L2", "0.01", 1200, "0.15"),
    ("L3", "0.005", 2400, "0.075"),
    ("L4", "0.0025", 4800, "0.0375"),
)
PUBLISHED_CONTINUUM_RADIUS = mp.mpf("0.9431133067695404")
PUBLISHED_CONTINUUM_OMEGA = mp.mpf("1.5855700777178037")
OLD_GUIDE_RADIUS = "0.9430108292781663"
OLD_GUIDE_OMEGA = "1.5868166272376472"
MP_DPS = 70
MP_NEWTON_ITERATIONS = 6
MP_MAXDEGREE = 10
MP_PARTITION = ("0", "2", "4", "6", "8", "10", "12")
MP_PANELS = (
    {"name": "mp-ts-70", "method": "tanh-sinh"},
    {"name": "mp-gl-70", "method": "gauss-legendre"},
)

FINITE_RESIDUAL_MAXIMUM = mp.mpf("1e-45")
FINITE_GAIN_ERROR_MAXIMUM = mp.mpf("1e-40")
CONTINUUM_RESIDUAL_MAXIMUM = mp.mpf("1e-45")
CONTINUUM_GAIN_ERROR_MAXIMUM = mp.mpf("1e-40")
CONTINUUM_PANEL_DIFFERENCE_MAXIMUM = mp.mpf("1e-40")
PUBLISHED_TARGET_DIFFERENCE_MAXIMUM = mp.mpf("5e-13")
JACOBIAN_DETERMINANT_MINIMUM = mp.mpf("0.1")
BRANCH_CORRIDOR = mp.mpf("0.05")
SLOPE_MINIMUM = mp.mpf("0.8")
SLOPE_MAXIMUM = mp.mpf("1.2")
FINE_TO_ANCHOR_MAXIMUM = mp.mpf("0.35")
RICHARDSON_RELATIVE_MAXIMUM = mp.mpf("0.1")


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
    """Hash the exact versioned ``HEAD:path`` blob, independent of checkout EOL."""
    result = subprocess.run(
        ["git", "cat-file", "blob", f"HEAD:{path.as_posix()}"],
        cwd=ROOT,
        capture_output=True,
        check=True,
    )
    return hashlib.sha256(result.stdout).hexdigest()


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def input_hash_audit() -> dict[str, Any]:
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


def revision_audit(artifacts: dict[str, dict[str, Any]]) -> dict[str, Any]:
    revisions = {
        "discovery": artifacts["discovery"]["simulation_revision"],
        "p0_manifest": artifacts["p0_manifest"]["code_revision"],
        "stability": artifacts["stability"]["execution_revision"],
        "interval": artifacts["interval"]["execution_revision"],
        "ladder": artifacts["ladder"]["execution_revision"],
        "continuum": artifacts["continuum"]["execution_revision"],
    }
    rows = [
        {
            "stage": stage,
            "revision": revision,
            "exists_and_is_ancestor": _revision_is_ancestor(revision),
        }
        for stage, revision in revisions.items()
    ]
    return {
        "rows": rows,
        "pass": all(row["exists_and_is_ancestor"] for row in rows),
    }


def _close(value: Any, expected: float, tolerance: float = 5.0e-13) -> bool:
    return math.isclose(
        float(value), float(expected), rel_tol=0.0, abs_tol=tolerance
    )


def parameter_and_semantics_audit(
    artifacts: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    discovery = artifacts["discovery"]
    p0_manifest = artifacts["p0_manifest"]
    p0_audit = artifacts["p0_audit"]
    stability = artifacts["stability"]
    interval = artifacts["interval"]
    ladder = artifacts["ladder"]
    continuum = artifacts["continuum"]

    selected = discovery["selected_candidate"]
    memory = p0_manifest["full_parameter_tuple"]["memory"]
    kernel = p0_manifest["full_parameter_tuple"]["kernel"]
    coupling = p0_manifest["full_parameter_tuple"]["coupling"]
    integration = p0_manifest["full_parameter_tuple"]["integration"]
    horizon = p0_manifest["full_parameter_tuple"]["horizon_and_boundary"]
    stable_candidate = stability["candidate"]
    certified_parameters = interval["parameters"]

    identifiers = {
        p0_manifest["candidate_id"],
        stability["candidate_id"],
        interval["candidate_id"],
    }
    parameter_checks = {
        "candidate_id": identifiers == {CANDIDATE_ID},
        "discovery_accepted": bool(selected["accepted"]),
        "dimension": (
            selected["dimension"] == 2
            and integration["dimension"] == 2
        ),
        "noise_off": (
            _close(selected["epsilon"], 0.0)
            and _close(stable_candidate["epsilon"], 0.0)
        ),
        "alpha": all(
            _close(value, 0.01)
            for value in (
                selected["alpha"],
                memory["alpha"],
                stable_candidate["alpha"],
                certified_parameters["alpha"],
            )
        ),
        "q": _close(memory["q"], 0.99),
        "horizon": all(
            int(value) == 1200
            for value in (
                selected["horizon"],
                horizon["horizon_H"],
                stable_candidate["horizon"],
                certified_parameters["horizon"],
            )
        ),
        "memory_mass": all(
            _close(value, 1.0)
            for value in (
                selected["memory_mass"],
                memory["memory_mass_M0"],
                stable_candidate["memory_mass"],
                certified_parameters["memory_mass"],
            )
        ),
        "eta": all(
            _close(value, 0.15)
            for value in (
                selected["eta"],
                coupling["eta"],
                stable_candidate["eta"],
                certified_parameters["eta"],
            )
        ),
        "kernel": all(
            (
                _close(source["sigma_rep"], 1.0)
                and _close(source["sigma_att"], 3.0)
                and _close(source["amplitude_rep"], 1.0)
                and _close(source["amplitude_att"], 3.5)
            )
            for source in (
                selected,
                kernel,
                stable_candidate,
                certified_parameters,
            )
        ),
        "p0_frozen_clean_zero_defect": (
            p0_manifest["manifest_status"] == "frozen"
            and p0_manifest["working_tree_status"] == "clean"
            and p0_audit["decision"] == "pass"
            and p0_audit["issue_count"] == 0
        ),
    }

    stability_gates = stability["gates"]
    interval_semantics = {
        "decision": (
            interval["decision"] == "interval-certified-unique-root-pass"
        ),
        "all_controls": bool(interval["all_controls"]),
        "all_panels": all(panel["pass"] for panel in interval["panels"]),
        "cross_panel": bool(interval["cross_panel"]["pass"]),
    }
    ladder_cells = [
        (cell["cell"], str(cell["alpha"]), cell["horizon"], str(cell["eta"]))
        for cell in ladder["cells"]
    ]
    evidence_semantics = {
        "discovery_decision": (
            discovery["decision"] == "finite-h-rotating-wave-candidate-found"
        ),
        "stability_decision": (
            stability["decision"] == "numerically-stable-source-pass"
        ),
        "stability_registered_controls": (
            stability_gates["spectral_controls"]
            and stability_gates["stable_spectrum"]
            and not stability_gates["unstable_spectrum"]
            and stability_gates["registered_perturbation_contraction"]
            and not stability_gates["registered_perturbation_growth"]
            and stability_gates["exact_control_pass"]
            and stability["panel_agreement"]["pass"]
        ),
        "interval_semantics": all(interval_semantics.values()),
        "historical_ladder_preserved": (
            ladder["decision"] == "certified-roots-nonconvergent"
            and ladder["all_cells_certified"]
            and ladder["anchor_overlap"]
            and ladder_cells == list(EXPECTED_LADDER_CELLS)
        ),
        "continuum_reconciliation_preserves_history": (
            continuum["decision"] == "fixed-gain-continuum-reconciliation-pass"
            and continuum["historical_ladder_decision"]
            == "certified-roots-nonconvergent"
        ),
        "sealed_controls_preserved": (
            not stability["registration"]["noise_opened"]
            and not stability["registration"]["topology_opened"]
            and _close(stability["registration"]["sealed_amplitude_holdout"], 7.0)
            and _close(
                continuum["registration"]["sealed_amplitude_holdout"], 7.0
            )
        ),
    }
    return {
        "parameter_checks": parameter_checks,
        "interval_semantics": interval_semantics,
        "evidence_semantics": evidence_semantics,
        "stability_classification": "anchor-local-numerical",
        "topology_classification": "ambient-SO2-group-orbit",
        "pass": bool(
            all(parameter_checks.values()) and all(evidence_semantics.values())
        ),
    }


def independent_finite_balance(
    *,
    radius: Any,
    theta: Any,
    alpha: Any,
    horizon: int,
    eta: Any,
    memory_mass: Any = "1",
    sigma_rep: Any = "1",
    sigma_att: Any = "3",
    amplitude_rep: Any = "1",
    amplitude_att: Any = "3.5",
) -> tuple[Any, Any, Any, Any]:
    """Evaluate the finite sums without importing either project evaluator."""

    radius = mp.mpf(radius)
    theta = mp.mpf(theta)
    alpha = mp.mpf(alpha)
    eta = mp.mpf(eta)
    memory_mass = mp.mpf(memory_mass)
    sigma_rep = mp.mpf(sigma_rep)
    sigma_att = mp.mpf(sigma_att)
    amplitude_rep = mp.mpf(amplitude_rep)
    amplitude_att = mp.mpf(amplitude_att)
    forgetting_q = 1 - alpha
    weight = alpha * memory_mass
    radial_sum = mp.zero
    tangential_sum = mp.zero
    for age in range(1, int(horizon)):
        weight *= forgetting_q
        phase = theta * age
        phase_sine = mp.sin(phase)
        radial_chord_factor = 1 - mp.cos(phase)
        chord_half_squared = radius**2 * radial_chord_factor
        gradient_factor = (
            -amplitude_rep
            / sigma_rep**2
            * mp.exp(-chord_half_squared / sigma_rep**2)
            + amplitude_att
            / sigma_att**2
            * mp.exp(-chord_half_squared / sigma_att**2)
        )
        radial_sum += weight * gradient_factor * radial_chord_factor
        tangential_sum += weight * gradient_factor * phase_sine
    radial_residual = mp.cos(theta) - 1 + eta * radial_sum
    tangential_residual = mp.sin(theta) + eta * tangential_sum
    return radial_residual, tangential_residual, radial_sum, tangential_sum


def exact_decimal_scaling(*, alpha: Any, horizon: int, eta: Any) -> tuple[bool, bool]:
    """Check the registered products in exact base-ten arithmetic."""

    decimal_alpha = Decimal(str(alpha))
    decimal_eta = Decimal(str(eta))
    tail_scaling = decimal_alpha * Decimal(horizon) == Decimal("12")
    gain_scaling = decimal_eta == Decimal("15") * decimal_alpha
    return tail_scaling, gain_scaling


def finite_ladder_replay(ladder: dict[str, Any]) -> dict[str, Any]:
    rows = []
    with mp.workdps(MP_DPS):
        for cell in ladder["cells"]:
            panel = max(cell["panels"], key=lambda row: row["precision_dps"])
            radius = mp.mpf(panel["refined"]["radius"])
            theta = mp.mpf(panel["refined"]["theta"])
            alpha = mp.mpf(str(cell["alpha"]))
            eta = mp.mpf(str(cell["eta"]))
            values = independent_finite_balance(
                radius=radius,
                theta=theta,
                alpha=alpha,
                horizon=cell["horizon"],
                eta=eta,
            )
            radial_residual, tangential_residual, radial_sum, tangential_sum = (
                values
            )
            residual_maximum = max(
                abs(radial_residual), abs(tangential_residual)
            )
            radial_eta = (1 - mp.cos(theta)) / radial_sum
            tangential_eta = -mp.sin(theta) / tangential_sum
            gain_error = max(abs(radial_eta - eta), abs(tangential_eta - eta))
            tail_scaling, gain_scaling = exact_decimal_scaling(
                alpha=cell["alpha"], horizon=cell["horizon"], eta=cell["eta"]
            )
            gates = {
                "residual": residual_maximum <= FINITE_RESIDUAL_MAXIMUM,
                "physical_signs": radial_sum > 0 and tangential_sum < 0,
                "gain": gain_error <= FINITE_GAIN_ERROR_MAXIMUM,
                "tail_scaling": tail_scaling,
                "gain_scaling": gain_scaling,
            }
            rows.append(
                {
                    "cell": cell["cell"],
                    "alpha": mp.nstr(alpha, 20),
                    "horizon": cell["horizon"],
                    "eta": mp.nstr(eta, 20),
                    "radius": mp.nstr(radius, 30),
                    "theta": mp.nstr(theta, 30),
                    "radial_residual": mp.nstr(radial_residual, 20),
                    "tangential_residual": mp.nstr(tangential_residual, 20),
                    "residual_maximum": mp.nstr(residual_maximum, 20),
                    "radial_sum": mp.nstr(radial_sum, 20),
                    "tangential_sum": mp.nstr(tangential_sum, 20),
                    "radial_eta": mp.nstr(radial_eta, 20),
                    "tangential_eta": mp.nstr(tangential_eta, 20),
                    "gain_error_maximum": mp.nstr(gain_error, 20),
                    "gates": gates,
                    "pass": all(gates.values()),
                }
            )
    return {"precision_dps": MP_DPS, "rows": rows, "pass": all(row["pass"] for row in rows)}


def _mp_integral(
    function: Callable[[Any], Any], *, method: str, maxdegree: int
) -> Any:
    partition = [mp.mpf(value) for value in MP_PARTITION]
    return mp.quad(function, partition, method=method, maxdegree=maxdegree)


def independent_continuum_balance(
    radius: Any,
    omega: Any,
    *,
    method: str,
    maxdegree: int = MP_MAXDEGREE,
) -> tuple[tuple[Any, Any], tuple[tuple[Any, Any], tuple[Any, Any]], tuple[Any, Any]]:
    """Evaluate continuum residual and Jacobian in an independent backend."""

    radius = mp.mpf(radius)
    omega = mp.mpf(omega)
    gain = mp.mpf("15")

    def pieces(time: Any) -> tuple[Any, ...]:
        phase = omega * time
        phase_sine = mp.sin(phase)
        phase_cosine = mp.cos(phase)
        radial_chord_factor = 1 - phase_cosine
        chord_half_squared = radius**2 * radial_chord_factor
        rep_exponential = mp.exp(-chord_half_squared)
        att_exponential = mp.exp(-chord_half_squared / 9)
        gradient_factor = -rep_exponential + mp.mpf("3.5") / 9 * att_exponential
        gradient_factor_chi = rep_exponential - mp.mpf("3.5") / 81 * att_exponential
        gradient_factor_radius = (
            gradient_factor_chi * 2 * radius * radial_chord_factor
        )
        gradient_factor_omega = (
            gradient_factor_chi * radius**2 * time * phase_sine
        )
        memory_weight = mp.exp(-time)
        return (
            memory_weight * gradient_factor * radial_chord_factor,
            memory_weight * gradient_factor * phase_sine,
            memory_weight * gradient_factor_radius * radial_chord_factor,
            memory_weight
            * (
                gradient_factor_omega * radial_chord_factor
                + gradient_factor * time * phase_sine
            ),
            memory_weight * gradient_factor_radius * phase_sine,
            memory_weight
            * (
                gradient_factor_omega * phase_sine
                + gradient_factor * time * phase_cosine
            ),
        )

    integrals = tuple(
        _mp_integral(
            lambda time, index=index: pieces(time)[index],
            method=method,
            maxdegree=maxdegree,
        )
        for index in range(6)
    )
    radial, tangential, radial_radius, radial_omega, tangential_radius, tangential_omega = integrals
    residual = (radial, omega + gain * tangential)
    jacobian = (
        (radial_radius, radial_omega),
        (gain * tangential_radius, 1 + gain * tangential_omega),
    )
    return residual, jacobian, (radial, tangential)


def fixed_newton(
    balance: Callable[[Any, Any], tuple[Any, Any]],
    *,
    radius_start: Any,
    omega_start: Any,
    iterations: int,
) -> dict[str, Any]:
    """Run a fixed number of undamped two-variable Newton steps."""

    radius = mp.mpf(radius_start)
    omega = mp.mpf(omega_start)
    iterates = []
    for iteration in range(iterations + 1):
        residual, jacobian, components = balance(radius, omega)
        determinant = (
            jacobian[0][0] * jacobian[1][1]
            - jacobian[0][1] * jacobian[1][0]
        )
        row = {
            "iteration": iteration,
            "radius": mp.nstr(radius, MP_DPS),
            "omega": mp.nstr(omega, MP_DPS),
            "residual": [mp.nstr(value, 30) for value in residual],
            "residual_maximum": mp.nstr(max(map(abs, residual)), 20),
            "jacobian_determinant": mp.nstr(determinant, 30),
        }
        iterates.append(row)
        if iteration == iterations:
            break
        radial_step = (
            residual[0] * jacobian[1][1]
            - residual[1] * jacobian[0][1]
        ) / determinant
        omega_step = (
            jacobian[0][0] * residual[1]
            - jacobian[1][0] * residual[0]
        ) / determinant
        radius -= radial_step
        omega -= omega_step
    return {
        "radius": radius,
        "omega": omega,
        "residual": residual,
        "jacobian": jacobian,
        "components": components,
        "iterates": iterates,
    }


def _continuum_panel(panel: dict[str, str]) -> dict[str, Any]:
    with mp.workdps(MP_DPS):
        result = fixed_newton(
            lambda radius, omega: independent_continuum_balance(
                radius,
                omega,
                method=panel["method"],
                maxdegree=MP_MAXDEGREE,
            ),
            radius_start=OLD_GUIDE_RADIUS,
            omega_start=OLD_GUIDE_OMEGA,
            iterations=MP_NEWTON_ITERATIONS,
        )
        radius = result["radius"]
        omega = result["omega"]
        residual_maximum = max(map(abs, result["residual"]))
        tangential = result["components"][1]
        required_gain = -omega / tangential
        determinant = (
            result["jacobian"][0][0] * result["jacobian"][1][1]
            - result["jacobian"][0][1] * result["jacobian"][1][0]
        )
        corridor = all(
            abs(mp.mpf(row[name]) - mp.mpf(start)) < BRANCH_CORRIDOR
            for row in result["iterates"]
            for name, start in (
                ("radius", OLD_GUIDE_RADIUS),
                ("omega", OLD_GUIDE_OMEGA),
            )
        )
        target_radius_difference = abs(radius - PUBLISHED_CONTINUUM_RADIUS)
        target_omega_difference = abs(omega - PUBLISHED_CONTINUUM_OMEGA)
        gates = {
            "branch_corridor": corridor,
            "positive_geometry": radius > 0 and omega > 0,
            "negative_tangential_integral": tangential < 0,
            "residual": residual_maximum <= CONTINUUM_RESIDUAL_MAXIMUM,
            "required_gain": (
                abs(required_gain - 15) <= CONTINUUM_GAIN_ERROR_MAXIMUM
            ),
            "jacobian_determinant": abs(determinant)
            >= JACOBIAN_DETERMINANT_MINIMUM,
            "published_target": (
                target_radius_difference <= PUBLISHED_TARGET_DIFFERENCE_MAXIMUM
                and target_omega_difference
                <= PUBLISHED_TARGET_DIFFERENCE_MAXIMUM
            ),
        }
        return {
            "name": panel["name"],
            "method": panel["method"],
            "precision_dps": MP_DPS,
            "maximum_degree": MP_MAXDEGREE,
            "newton_iterations": MP_NEWTON_ITERATIONS,
            "radius": mp.nstr(radius, MP_DPS),
            "omega": mp.nstr(omega, MP_DPS),
            "residual": [mp.nstr(value, 30) for value in result["residual"]],
            "residual_maximum": mp.nstr(residual_maximum, 20),
            "tangential_integral": mp.nstr(tangential, 30),
            "required_eta_per_alpha": mp.nstr(required_gain, 30),
            "jacobian_determinant": mp.nstr(determinant, 30),
            "published_radius_difference": mp.nstr(target_radius_difference, 20),
            "published_omega_difference": mp.nstr(target_omega_difference, 20),
            "iterates": result["iterates"],
            "gates": gates,
            "pass": all(gates.values()),
        }


def continuum_replay() -> dict[str, Any]:
    panels = [_continuum_panel(panel) for panel in MP_PANELS]
    with mp.workdps(MP_DPS):
        radius_difference = abs(
            mp.mpf(panels[0]["radius"]) - mp.mpf(panels[1]["radius"])
        )
        omega_difference = abs(
            mp.mpf(panels[0]["omega"]) - mp.mpf(panels[1]["omega"])
        )
        agreement = bool(
            radius_difference <= CONTINUUM_PANEL_DIFFERENCE_MAXIMUM
            and omega_difference <= CONTINUUM_PANEL_DIFFERENCE_MAXIMUM
        )
    return {
        "panels": panels,
        "cross_panel": {
            "radius_difference": mp.nstr(radius_difference, 20),
            "omega_difference": mp.nstr(omega_difference, 20),
            "pass": agreement,
        },
        "pass": bool(all(panel["pass"] for panel in panels) and agreement),
    }


def scaling_replay(
    cells: list[dict[str, Any]], *, target_radius: Any, target_omega: Any
) -> dict[str, Any]:
    with mp.workdps(MP_DPS):
        ordered = sorted(cells, key=lambda row: mp.mpf(str(row["alpha"])), reverse=True)
        alphas = [mp.mpf(str(row["alpha"])) for row in ordered]
        radii = [
            mp.mpf(max(row["panels"], key=lambda panel: panel["precision_dps"])["refined"]["radius"])
            for row in ordered
        ]
        omegas = [
            mp.mpf(max(row["panels"], key=lambda panel: panel["precision_dps"])["omega"])
            for row in ordered
        ]
        target_radius = mp.mpf(target_radius)
        target_omega = mp.mpf(target_omega)
        radius_errors = [abs(value - target_radius) for value in radii]
        omega_errors = [abs(value - target_omega) for value in omegas]

        def slope(errors: list[Any]) -> Any:
            points = [
                (mp.log(alpha), mp.log(error))
                for alpha, error in zip(alphas, errors, strict=True)
                if alpha <= mp.mpf("0.02")
            ]
            mean_x = mp.fsum(point[0] for point in points) / len(points)
            mean_y = mp.fsum(point[1] for point in points) / len(points)
            return mp.fsum(
                (x - mean_x) * (y - mean_y) for x, y in points
            ) / mp.fsum((x - mean_x) ** 2 for x, _ in points)

        radius_slope = slope(radius_errors)
        omega_slope = slope(omega_errors)
        anchor_index = next(
            index for index, row in enumerate(ordered) if row["cell"] == "L2"
        )
        radius_fine_ratio = radius_errors[-1] / radius_errors[anchor_index]
        omega_fine_ratio = omega_errors[-1] / omega_errors[anchor_index]
        radius_richardson = 2 * radii[-1] - radii[-2]
        omega_richardson = 2 * omegas[-1] - omegas[-2]
        radius_richardson_relative = (
            abs(radius_richardson - target_radius) / radius_errors[-1]
        )
        omega_richardson_relative = (
            abs(omega_richardson - target_omega) / omega_errors[-1]
        )
        gates = {
            "positive_errors": all(
                value > 0 for value in (*radius_errors, *omega_errors)
            ),
            "radius_error_monotone": all(
                latter < former
                for former, latter in zip(radius_errors, radius_errors[1:])
            ),
            "omega_error_monotone": all(
                latter < former
                for former, latter in zip(omega_errors, omega_errors[1:])
            ),
            "radius_slope": SLOPE_MINIMUM <= radius_slope <= SLOPE_MAXIMUM,
            "omega_slope": SLOPE_MINIMUM <= omega_slope <= SLOPE_MAXIMUM,
            "radius_fine_to_anchor": radius_fine_ratio <= FINE_TO_ANCHOR_MAXIMUM,
            "omega_fine_to_anchor": omega_fine_ratio <= FINE_TO_ANCHOR_MAXIMUM,
            "radius_richardson": (
                radius_richardson_relative <= RICHARDSON_RELATIVE_MAXIMUM
            ),
            "omega_richardson": (
                omega_richardson_relative <= RICHARDSON_RELATIVE_MAXIMUM
            ),
        }
        return {
            "target_radius": mp.nstr(target_radius, 40),
            "target_omega": mp.nstr(target_omega, 40),
            "rows": [
                {
                    "cell": row["cell"],
                    "alpha": mp.nstr(alphas[index], 20),
                    "radius": mp.nstr(radii[index], 30),
                    "omega": mp.nstr(omegas[index], 30),
                    "radius_error": mp.nstr(radius_errors[index], 20),
                    "omega_error": mp.nstr(omega_errors[index], 20),
                }
                for index, row in enumerate(ordered)
            ],
            "radius_slope": mp.nstr(radius_slope, 20),
            "omega_slope": mp.nstr(omega_slope, 20),
            "radius_fine_to_anchor_error_ratio": mp.nstr(radius_fine_ratio, 20),
            "omega_fine_to_anchor_error_ratio": mp.nstr(omega_fine_ratio, 20),
            "radius_richardson_relative_error": mp.nstr(
                radius_richardson_relative, 20
            ),
            "omega_richardson_relative_error": mp.nstr(
                omega_richardson_relative, 20
            ),
            "gates": gates,
            "pass": all(gates.values()),
        }


def _load_artifacts() -> dict[str, dict[str, Any]]:
    return {
        "discovery": _load_json(DISCOVERY),
        "p0_manifest": _load_json(P0_MANIFEST),
        "p0_audit": _load_json(P0_AUDIT),
        "stability": _load_json(STABILITY),
        "interval": _load_json(INTERVAL_CERTIFICATE),
        "ladder": _load_json(REFINEMENT_LADDER),
        "continuum": _load_json(CONTINUUM_RECONCILIATION),
    }


def run_audit() -> dict[str, Any]:
    start_status = _git_output(["status", "--short"])
    if start_status:
        raise RuntimeError("foundation audit requires a clean prospective revision")
    execution_revision = _git_output(["rev-parse", "HEAD"])
    try:
        artifacts = _load_artifacts()
        hashes = input_hash_audit()
        revisions = revision_audit(artifacts)
        semantics = parameter_and_semantics_audit(artifacts)
        finite_replay = finite_ladder_replay(artifacts["ladder"])
        continuum = continuum_replay()
        target_panel = next(
            panel for panel in continuum["panels"] if panel["name"] == "mp-gl-70"
        )
        scaling = scaling_replay(
            artifacts["ladder"]["cells"],
            target_radius=target_panel["radius"],
            target_omega=target_panel["omega"],
        )
        stored_continuum = artifacts["continuum"]
        stored_reconciliation_pass = bool(
            stored_continuum["decision"]
            == "fixed-gain-continuum-reconciliation-pass"
            and stored_continuum["all_panels_pass"]
            and stored_continuum["continuum_pass"]
            and stored_continuum["inputs_pass"]
            and stored_continuum["panel_agreement"]["pass"]
            and stored_continuum["ladder_integrity"]["pass"]
            and stored_continuum["source_audit"]["pass"]
            and stored_continuum["scaling"]["pass"]
        )
        gates = {
            "A_provenance_parameter_closure": bool(
                hashes["pass"] and revisions["pass"] and semantics["pass"]
            ),
            "B_independent_finite_sum_replay": bool(finite_replay["pass"]),
            "C_certificate_and_stability_semantics": bool(
                semantics["evidence_semantics"]["stability_registered_controls"]
                and semantics["evidence_semantics"]["interval_semantics"]
                and semantics["evidence_semantics"]["historical_ladder_preserved"]
            ),
            "D_independent_continuum_replay": bool(continuum["pass"]),
            "E_scaling_replay": bool(
                scaling["pass"] and stored_reconciliation_pass
            ),
        }
        decision = (
            "foundation-audit-portability-reconciliation-pass-scoped"
            if all(gates.values())
            else "foundation-audit-portability-reconciliation-fail"
        )
        exception = None
    except Exception as error:  # pragma: no cover - result-path safeguard
        hashes = None
        revisions = None
        semantics = None
        finite_replay = None
        continuum = None
        scaling = None
        stored_reconciliation_pass = False
        gates = {}
        decision = "foundation-audit-portability-reconciliation-inconclusive"
        exception = f"{type(error).__name__}: {error}"

    return {
        "schema": "emergenz-knoten.scalar-memory-rotating-wave-foundation-audit",
        "schema_version": 3,
        "generated_utc": datetime.now(UTC).isoformat(),
        "execution_revision": execution_revision,
        "git_status_at_start": start_status,
        "protocol": PROTOCOL.as_posix(),
        "input_hashes": hashes,
        "revisions": revisions,
        "parameter_and_semantics": semantics,
        "finite_ladder_replay": finite_replay,
        "continuum_replay": continuum,
        "scaling_replay": scaling,
        "stored_reconciliation_pass": stored_reconciliation_pass,
        "gates": gates,
        "decision": decision,
        "exception": exception,
        "sealed_next_cell": {
            "alpha": "0.00125",
            "horizon": 9600,
            "eta": "0.01875",
            "status": "sealed-not-evaluated-by-foundation-audit",
        },
        "claim_boundary": {
            "established_if_pass": (
                "an exact prepared-circle reduction, five locally unique "
                "finite-H roots, independent fixed-gain continuum/scaling "
                "replay, and anchor-local numerical stability"
            ),
            "not_established": (
                "global uniqueness, complete spectral stability, generic "
                "formation, basin size, noise robustness, chirality "
                "selection, internal S1 after SO2 quotient, work, inertia, "
                "mass, or a material knot"
            ),
        },
    }


def _fmt(value: Any) -> str:
    try:
        return f"{float(value):.9g}"
    except (TypeError, ValueError):
        return str(value)


def render_report(payload: dict[str, Any]) -> str:
    lines = [
        "# Critical foundation audit: native scalar-memory rotating waves",
        "",
        f"Generated: {payload['generated_utc']}.",
        "",
        f"Decision: **{payload['decision']}**.",
        "",
        "The audit ran from clean prospective revision",
        f"`{payload['execution_revision']}`.",
        "",
    ]
    if payload["exception"] is not None:
        lines.extend(["Execution exception:", "", payload["exception"], ""])
        return "\n".join(lines)

    lines.extend(
        [
            "## Composite gates",
            "",
            "| gate | result |",
            "| --- | --- |",
        ]
    )
    lines.extend(
        f"| {name} | {'pass' if passed else 'fail'} |"
        for name, passed in payload["gates"].items()
    )
    lines.extend(
        [
            "",
            "All nine immutable canonical Git-blob hashes match, and every recorded",
            "execution revision exists in the ancestry of this audit.",
            "",
            "## Independent finite-sum replay",
            "",
            "| cell | alpha | H | eta | max residual | max gain error | result |",
            "| --- | ---: | ---: | ---: | ---: | ---: | --- |",
        ]
    )
    for row in payload["finite_ladder_replay"]["rows"]:
        lines.append(
            f"| {row['cell']} | {_fmt(row['alpha'])} | {row['horizon']} | "
            f"{_fmt(row['eta'])} | {_fmt(row['residual_maximum'])} | "
            f"{_fmt(row['gain_error_maximum'])} | "
            f"{'pass' if row['pass'] else 'fail'} |"
        )
    lines.extend(
        [
            "",
            "This replay uses a separate multiprecision sum and imports no",
            "project rotating-wave evaluator. It checks signs, ages, weights,",
            "both residual components and both inferred gains; it is not a",
            "second interval proof.",
            "",
            "## Independent continuum replay",
            "",
            "| panel | method | R | Omega | max residual | target dR | target dOmega | result |",
            "| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |",
        ]
    )
    for panel in payload["continuum_replay"]["panels"]:
        lines.append(
            f"| {panel['name']} | {panel['method']} | {_fmt(panel['radius'])} | "
            f"{_fmt(panel['omega'])} | {_fmt(panel['residual_maximum'])} | "
            f"{_fmt(panel['published_radius_difference'])} | "
            f"{_fmt(panel['published_omega_difference'])} | "
            f"{'pass' if panel['pass'] else 'fail'} |"
        )
    cross = payload["continuum_replay"]["cross_panel"]
    scaling = payload["scaling_replay"]
    lines.extend(
        [
            "",
            "The two multiprecision quadratures agree to",
            f"dR={_fmt(cross['radius_difference'])} and "
            f"dOmega={_fmt(cross['omega_difference'])}.",
            "They are independent numerical controls, not continuum interval",
            "enclosures.",
            "",
            "## Scaling replay",
            "",
            f"Radius slope: `{_fmt(scaling['radius_slope'])}`; Omega slope: "
            f"`{_fmt(scaling['omega_slope'])}`.",
            "",
            f"Fine/anchor error ratios: R=`{_fmt(scaling['radius_fine_to_anchor_error_ratio'])}`, "
            f"Omega=`{_fmt(scaling['omega_fine_to_anchor_error_ratio'])}`.",
            "",
            f"Richardson relative errors: R=`{_fmt(scaling['radius_richardson_relative_error'])}`, "
            f"Omega=`{_fmt(scaling['omega_richardson_relative_error'])}`.",
            "",
        ]
    )
    lines.extend(["", "## Reviewer verdict", ""])
    if (
        payload["decision"]
        == "foundation-audit-portability-reconciliation-pass-scoped"
    ):
        lines.extend(
            [
                "The evidence chain is suitable as a **scoped mathematical and",
                "numerical foundation for prepared spatial loops**. Exact local",
                "finite-H existence is certified in five cells, and the fixed-gain",
                "continuum/scaling result survives a separate multiprecision",
                "implementation.",
                "",
                "The word *stable* remains narrower: only the anchor has strong",
                "local numerical spectral and perturbative evidence, without a",
                "complete spectral enclosure. No generic history has formed a",
                "loop. D0 identifies the circle as an ambient SO(2) group orbit",
                "that becomes a point in the symmetry quotient, not an internal",
                "S1. No work, inertia or mass claim follows.",
            ]
        )
    else:
        lines.extend(
            [
                "No positive foundation verdict is authorized because the",
                "composite reconciliation did not pass. The machine-readable",
                "decision and individual gates are authoritative.",
            ]
        )
    lines.extend(
        [
            "",
            "The next refinement cell remains sealed and was not evaluated by",
            "this audit.",
        ]
    )
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = run_audit()
    report_path = ROOT / args.report
    summary_path = ROOT / args.summary
    report_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(render_report(payload) + "\n", encoding="utf-8")
    summary_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"decision={payload['decision']}")
    print(f"report={report_path.relative_to(ROOT).as_posix()}")
    print(f"summary={summary_path.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    main()
