from __future__ import annotations

import argparse
from dataclasses import replace
from datetime import UTC, datetime
import json
from pathlib import Path
import subprocess
import sys
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from emergenz_knoten import SimulationConfig, VectorMemoryConfig, simulate_vector_memory  # noqa: E402
from experiments.ar_mode_probe import (  # noqa: E402
    _fit_to_row,
    fit_ar_map,
    pca_project_series,
    standardize_feature_series,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Small vector-memory pilot around corrected scalar transition "
            "candidates. This is a diagnostic pilot, not a photon/boson claim."
        )
    )
    parser.add_argument("--steps", type=int, default=20000)
    parser.add_argument("--burn-in", type=int, default=0)
    parser.add_argument("--sample-every", type=int, default=50)
    parser.add_argument("--dim", type=int, default=2)
    parser.add_argument("--seeds", type=int, nargs="+", default=[1, 2, 3])
    parser.add_argument(
        "--amplitude-att",
        type=float,
        nargs="+",
        default=[0.35, 7.75, 8.0, 9.0, 20.0],
    )
    parser.add_argument("--eta-vector", type=float, nargs="+", default=[0.0, 0.01, 0.03])
    parser.add_argument("--force-mode", choices=["alignment", "transverse_2d"], default="transverse_2d")
    parser.add_argument("--epsilon", type=float, default=0.03)
    parser.add_argument("--eta", type=float, default=0.15)
    parser.add_argument("--alpha", type=float, default=0.01)
    parser.add_argument("--memory-mass", type=float, default=1.0)
    parser.add_argument("--lambda-vector", type=float, default=None)
    parser.add_argument("--vector-mass", type=float, default=1.0)
    parser.add_argument("--sigma-vector", type=float, default=1.0)
    parser.add_argument("--sigma-rep", type=float, default=1.0)
    parser.add_argument("--sigma-att", type=float, default=3.0)
    parser.add_argument("--amplitude-rep", type=float, default=1.0)
    parser.add_argument("--memory-factor", type=float, default=6.0)
    parser.add_argument("--max-memory", type=int, default=600)
    parser.add_argument("--lags", type=int, nargs="+", default=[1, 2, 5, 10])
    parser.add_argument("--pca-components", type=int, default=6)
    parser.add_argument("--ridge", type=float, default=1e-6)
    parser.add_argument("--imag-tol", type=float, default=1e-3)
    parser.add_argument("--unstable-tol", type=float, default=1.05)
    parser.add_argument("--slow-abs-min", type=float, default=0.2)
    parser.add_argument(
        "--output-json",
        type=str,
        default="data/processed/vector_memory_pilot/initial_2026-07-10/summary.json",
    )
    parser.add_argument(
        "--report",
        type=str,
        default="reports/vector_memory_pilot_initial_2026-07-10.md",
    )
    return parser.parse_args()


def _utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def _git_output(args: list[str]) -> str:
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=ROOT,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except (OSError, subprocess.CalledProcessError):
        return "unavailable"
    return completed.stdout.strip()


def _scalar_config(args: argparse.Namespace, *, amplitude_att: float) -> SimulationConfig:
    return SimulationConfig(
        steps=args.steps,
        dim=args.dim,
        epsilon=args.epsilon,
        eta=args.eta,
        alpha=args.alpha,
        memory_mass=args.memory_mass,
        sigma_rep=args.sigma_rep,
        sigma_att=args.sigma_att,
        amplitude_rep=args.amplitude_rep,
        amplitude_att=amplitude_att,
        memory_factor=args.memory_factor,
        max_memory=args.max_memory,
        burn_in=args.burn_in,
        sample_every=args.sample_every,
    )


def _vector_config(
    args: argparse.Namespace,
    *,
    amplitude_att: float,
    eta_vector: float,
) -> VectorMemoryConfig:
    return VectorMemoryConfig(
        scalar=_scalar_config(args, amplitude_att=amplitude_att),
        lambda_vector=args.lambda_vector,
        vector_mass=args.vector_mass,
        eta_vector=eta_vector,
        sigma_vector=args.sigma_vector,
        force_mode=args.force_mode,
    )


def _scenario_series(
    args: argparse.Namespace, *, amplitude_att: float, eta_vector: float
) -> tuple[list[np.ndarray], float]:
    series: list[np.ndarray] = []
    radii: list[float] = []
    for seed in args.seeds:
        result = simulate_vector_memory(
            _vector_config(args, amplitude_att=amplitude_att, eta_vector=eta_vector),
            seed=int(seed),
        )
        series.append(np.asarray(result["augmented_features"], dtype=float))
        samples = np.asarray(result["samples"], dtype=float)
        center = samples.mean(axis=0)
        radii.append(float(np.sqrt(np.mean(np.sum((samples - center) ** 2, axis=1)))))
    return series, float(np.median(radii))


def run_pilot(args: argparse.Namespace) -> dict[str, Any]:
    scenarios: list[dict[str, Any]] = []
    for amplitude_att in args.amplitude_att:
        for eta_vector in args.eta_vector:
            raw_series, sample_radius = _scenario_series(
                args,
                amplitude_att=float(amplitude_att),
                eta_vector=float(eta_vector),
            )
            standardized, _, _ = standardize_feature_series(raw_series)
            projected, _, explained_ratio = pca_project_series(standardized, args.pca_components)
            rows = []
            for lag in args.lags:
                fit = fit_ar_map(
                    projected,
                    lag=int(lag),
                    lag_updates=int(lag * args.sample_every),
                    ridge=float(args.ridge),
                )
                rows.append(
                    _fit_to_row(
                        fit,
                        imag_tol=args.imag_tol,
                        unstable_tol=args.unstable_tol,
                        slow_abs_min=args.slow_abs_min,
                    )
                )
            scenarios.append(
                {
                    "amplitude_att": float(amplitude_att),
                    "eta_vector": float(eta_vector),
                    "force_mode": args.force_mode,
                    "sample_radius_median": sample_radius,

                    "feature_dim_raw": int(raw_series[0].shape[1]),
                    "feature_dim_projected": int(projected[0].shape[1]),
                    "pca_explained_ratio": [float(x) for x in explained_ratio],
                    "rows": rows,
                }
            )
    return {
        "description": "Initial vector-memory AR pilot.",
        "created_utc": _utc_now(),
        "git_revision": _git_output(["rev-parse", "HEAD"]),
        "git_status": _git_output(["status", "--short"]),
        "parameters": vars(args),
        "scenarios": scenarios,
    }


def _fmt(value: Any, digits: int = 4) -> str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return f"`{value}`"
    if not np.isfinite(number):
        return "`n/a`"
    return f"`{number:.{digits}g}`"


def build_report(payload: dict[str, Any]) -> str:
    params = payload["parameters"]
    lines = [
        "# Initial Vector-Memory Pilot",
        "",
        f"Date: {payload['created_utc']}.",
        "",
        "## Scope",
        "",
        "This pilot tests the first oriented-memory implementation. It is a",
        "mode diagnostic, not a photon, neutrino, boson, or Standard-Model claim.",
        "",
        "Burn-in is kept as an analysis cut, not a model assumption. The default",
        "pilot uses `burn_in=0` to preserve formation histories.",
        "",
        "## Parameters",
        "",
        f"- `amplitude_att`: `{params['amplitude_att']}`",
        f"- `eta_vector`: `{params['eta_vector']}`",
        f"- `force_mode`: `{params['force_mode']}`",
        f"- `alpha=lambda_s`: `{params['alpha']}`",
        f"- `lambda_vector`: `{params['lambda_vector']}` (`None` means `alpha`)",
        f"- `memory_mass=M0_s`: `{params['memory_mass']}`",
        f"- `vector_mass=M0_v`: `{params['vector_mass']}`",
        f"- `steps`: `{params['steps']}`, `seeds`: `{params['seeds']}`",
        "",
        "## AR Summary",
        "",
        "| A_att | eta_v | radius med | lag | class | leading abs | leading imag | residual | top eigenvalues |",
        "| ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | --- |",
    ]
    for scenario in payload["scenarios"]:
        for row in scenario["rows"]:
            lines.append(
                f"| `{scenario['amplitude_att']:.6g}` | `{scenario['eta_vector']:.6g}` | "
                f"{_fmt(scenario['sample_radius_median'])} | `{row['lag']}` | "
                f"`{row['classification']}` | {_fmt(row['leading_abs'])} | "
                f"{_fmt(row['leading_imag'])} | {_fmt(row['residual_rms'])} | "
                f"`{' ; '.join(row['top_eigenvalues'][:3])}` |"
            )
    lines.extend(
        [
            "",
            "## Immediate Reading",
            "",
            "- Complex AR classifications in this pilot are not by themselves evidence",
            "  for vector-induced oscillators, because `eta_vector=0` is included as",
            "  a scalar fallback control and can already show complex projected modes.",
            "- A vector effect requires a change relative to the `eta_vector=0` rows",
            "  that is stable across lag, seed, and feature choices.",
            "- The compact `A_att=20.0` reference should be read separately from the",
            "  transition band `7.75..9.0`; it tests over-confinement/relaxation, not",
            "  the boundary itself.",
            "",
            "## Reading Rules",
            "",
            "- `eta_vector=0` is the scalar fallback control.",
            "- A complex classification matters only if it is slow and stable across lags.",
            "- `A_att=0.35` is the weak-attraction historical reference; `7.75..9.0`",
            "  covers the corrected transition; `20.0` is the first compactness",
            "  reference inside the `9..35` window.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    args = parse_args()
    payload = run_pilot(args)
    output_json = ROOT / args.output_json
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    report = ROOT / args.report
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(build_report(payload), encoding="utf-8")
    print(f"wrote {output_json}")
    print(f"wrote {report}")


if __name__ == "__main__":
    main()
