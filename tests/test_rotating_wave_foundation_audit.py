from mpmath import mp
import pytest

from emergenz_knoten.rotating_wave import (
    continuum_rotating_wave_balance,
    finite_h_rotating_wave_residual,
)
from experiments.current.dynamics.rotation import (
    scalar_memory_rotating_wave_foundation_audit as audit,
)


def test_frozen_foundation_input_hashes_match_repository():
    result = audit.input_hash_audit()

    assert result["pass"]
    assert result["hash_domain"] == "git-head-blob"
    assert len(result["rows"]) == 9
    assert {row["hash_domain"] for row in result["rows"]} == {"git-head-blob"}
    assert all(
        row["observed_sha256"] == row["expected_sha256"]
        for row in result["rows"]
    )


def test_independent_finite_sum_matches_project_residual_off_target():
    parameters = {
        "radius": 0.73,
        "theta": 0.11,
        "alpha": 0.07,
        "horizon": 17,
        "eta": 0.19,
        "memory_mass": 1.2,
        "sigma_rep": 0.9,
        "sigma_att": 2.4,
        "amplitude_rep": 1.1,
        "amplitude_att": 2.7,
    }
    with mp.workdps(50):
        radial, tangential, _, _ = audit.independent_finite_balance(**parameters)
    expected = finite_h_rotating_wave_residual(**parameters)

    assert float(radial) == pytest.approx(expected.real, abs=2.0e-15)
    assert float(tangential) == pytest.approx(expected.imag, abs=2.0e-15)


@pytest.mark.parametrize(
    ("alpha", "horizon", "eta"),
    [values[1:] for values in audit.EXPECTED_LADDER_CELLS],
)
def test_registered_scalings_use_exact_decimal_arithmetic(alpha, horizon, eta):
    assert audit.exact_decimal_scaling(
        alpha=alpha, horizon=horizon, eta=eta
    ) == (True, True)


def test_independent_continuum_balance_and_jacobian_match_off_target():
    parameters = {
        "radius": 0.71,
        "angular_frequency": 1.13,
        "eta_per_alpha": 15.0,
        "tail_extent": 12.0,
        "memory_mass": 1.0,
        "sigma_rep": 1.0,
        "sigma_att": 3.0,
        "amplitude_rep": 1.0,
        "amplitude_att": 3.5,
        "quadrature_order": 512,
        "quadrature_backend": "scipy",
    }
    expected = continuum_rotating_wave_balance(**parameters)
    with mp.workdps(35):
        residual, jacobian, _ = audit.independent_continuum_balance(
            parameters["radius"],
            parameters["angular_frequency"],
            method="tanh-sinh",
            maxdegree=7,
        )

    assert tuple(map(float, residual)) == pytest.approx(expected.residual, abs=2.0e-13)
    observed_jacobian = tuple(float(value) for row in jacobian for value in row)
    expected_jacobian = tuple(
        float(value) for row in expected.jacobian for value in row
    )
    assert observed_jacobian == pytest.approx(expected_jacobian, abs=2.0e-12)


def test_fixed_newton_uses_exact_registered_iteration_count():
    def balance(radius, omega):
        residual = (2 * radius + omega - 5, radius - omega - 1)
        jacobian = ((mp.mpf(2), mp.mpf(1)), (mp.mpf(1), mp.mpf(-1)))
        return residual, jacobian, (mp.zero, mp.zero)

    with mp.workdps(40):
        result = audit.fixed_newton(
            balance,
            radius_start="0.5",
            omega_start="0.5",
            iterations=3,
        )

    assert float(result["radius"]) == pytest.approx(2.0)
    assert float(result["omega"]) == pytest.approx(1.0)
    assert [row["iteration"] for row in result["iterates"]] == [0, 1, 2, 3]


def test_scaling_replay_accepts_exact_first_order_family():
    target_radius = mp.mpf("0.9")
    target_omega = mp.mpf("1.6")

    def cell(name, alpha, horizon, eta):
        radius = target_radius + mp.mpf("0.4") * mp.mpf(alpha)
        omega = target_omega - mp.mpf("0.7") * mp.mpf(alpha)
        return {
            "cell": name,
            "alpha": alpha,
            "horizon": horizon,
            "eta": eta,
            "panels": [
                {
                    "precision_dps": 120,
                    "refined": {"radius": mp.nstr(radius, 30)},
                    "omega": mp.nstr(omega, 30),
                }
            ],
        }

    cells = [cell(*values) for values in audit.EXPECTED_LADDER_CELLS]
    result = audit.scaling_replay(
        cells, target_radius=target_radius, target_omega=target_omega
    )

    assert result["pass"]
    assert float(result["radius_slope"]) == pytest.approx(1.0, abs=1.0e-12)
    assert float(result["omega_slope"]) == pytest.approx(1.0, abs=1.0e-12)


def test_failed_report_does_not_render_positive_reviewer_verdict():
    payload = {
        "generated_utc": "2026-08-21T00:00:00+00:00",
        "decision": "foundation-audit-portability-reconciliation-fail",
        "execution_revision": "deadbeef",
        "exception": None,
        "gates": {"synthetic_gate": False},
        "finite_ladder_replay": {"rows": []},
        "continuum_replay": {
            "panels": [],
            "cross_panel": {"radius_difference": "0", "omega_difference": "0"},
        },
        "scaling_replay": {
            "radius_slope": "1",
            "omega_slope": "1",
            "radius_fine_to_anchor_error_ratio": "0.25",
            "omega_fine_to_anchor_error_ratio": "0.25",
            "radius_richardson_relative_error": "0.01",
            "omega_richardson_relative_error": "0.01",
        },
    }

    report = audit.render_report(payload)

    assert "suitable as a **scoped" not in report
    assert "All nine immutable canonical Git-blob hashes match" not in report
    assert "Gate A and the machine-readable rows are authoritative" in report
    assert "No positive foundation verdict is authorized" in report
