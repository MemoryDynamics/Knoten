from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import UTC, datetime
import json
from pathlib import Path
import subprocess
import sys
from typing import Any, Iterable

import numpy as np

def _repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("repository root not found")


ROOT = _repo_root()

sys.path.insert(0, str(ROOT / "src"))

from emergenz_knoten import SimulationConfig  # noqa: E402
from emergenz_knoten.markov import simulate_augmented_features  # noqa: E402


@dataclass(frozen=True)
class ARFit:
    lag: int
    lag_updates: int
    matrix: np.ndarray
    eigenvalues: np.ndarray
    n_pairs: int
    residual_rms: float


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Fit coarse-grained linear AR mode maps on reduced augmented-state "
            "features. This is a mode-classification probe, not a proof of a "
            "closed effective dynamics."
        )
    )
    parser.add_argument("--steps", type=int, default=50000)
    parser.add_argument("--burn-in", type=int, default=5000)
    parser.add_argument("--sample-every", type=int, default=100)
    parser.add_argument("--dim", type=int, default=3)
    parser.add_argument("--seeds", type=int, nargs="+", default=[1, 2, 3])
    parser.add_argument("--amplitude-att", type=float, nargs="+", default=[9.0, 35.0])
    parser.add_argument("--epsilon", type=float, default=0.03)
    parser.add_argument("--eta", type=float, default=0.15)
    parser.add_argument("--alpha", type=float, default=0.01)
    parser.add_argument("--memory-mass", type=float, default=1.0)
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
        default="data/processed/ar_mode_probe/corrected_candidates_2026-07-09/summary.json",
    )
    parser.add_argument(
        "--report",
        type=str,
        default="reports/kernels/mode_probes/ar_mode_probe_corrected_candidates_2026-07-09.md",
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


def _config(args: argparse.Namespace, *, amplitude_att: float) -> SimulationConfig:
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


def standardize_feature_series(series: list[np.ndarray]) -> tuple[list[np.ndarray], np.ndarray, np.ndarray]:
    if not series:
        raise ValueError("series must not be empty")
    stacked = np.vstack(series).astype(float)
    mean = stacked.mean(axis=0)
    scale = stacked.std(axis=0)
    scale[scale == 0.0] = 1.0
    return [((arr - mean) / scale) for arr in series], mean, scale


def pca_project_series(series: list[np.ndarray], components: int) -> tuple[list[np.ndarray], np.ndarray, np.ndarray]:
    if components <= 0:
        dim = series[0].shape[1]
        return series, np.eye(dim), np.ones(dim)
    stacked = np.vstack(series)
    _, singular, vt = np.linalg.svd(stacked, full_matrices=False)
    k = min(int(components), vt.shape[0])
    basis = vt[:k].T
    denom = max(stacked.shape[0] - 1, 1)
    explained = (singular[:k] ** 2) / denom
    total = float(np.sum((singular**2) / denom))
    ratio = explained / total if total > 0.0 else np.zeros_like(explained)
    return [arr @ basis for arr in series], basis, ratio


def fit_ar_map(series: list[np.ndarray], *, lag: int, lag_updates: int, ridge: float) -> ARFit:
    if lag < 1:
        raise ValueError("lag must be positive")
    currents: list[np.ndarray] = []
    futures: list[np.ndarray] = []
    for arr in series:
        if arr.shape[0] <= lag:
            continue
        currents.append(arr[:-lag])
        futures.append(arr[lag:])
    if not currents:
        raise ValueError("not enough rows for requested lag")
    x = np.vstack(currents)
    y = np.vstack(futures)
    gram = x.T @ x
    regularized = gram + float(ridge) * np.eye(gram.shape[0])
    coef = np.linalg.solve(regularized, x.T @ y)
    pred = x @ coef
    residual = y - pred
    rms = float(np.sqrt(np.mean(residual * residual)))
    eig = np.linalg.eigvals(coef)
    order = np.argsort(-np.abs(eig))
    return ARFit(
        lag=int(lag),
        lag_updates=int(lag_updates),
        matrix=coef,
        eigenvalues=eig[order],
        n_pairs=int(x.shape[0]),
        residual_rms=rms,
    )


def classify_eigenvalues(
    eigenvalues: Iterable[complex],
    *,
    imag_tol: float = 1e-3,
    unstable_tol: float = 1.05,
    slow_abs_min: float = 0.2,
) -> str:
    values = np.asarray(list(eigenvalues), dtype=complex)
    if values.size == 0:
        return "empty"
    ordered = values[np.argsort(-np.abs(values))]
    slow = ordered[np.abs(ordered) >= slow_abs_min]
    leading = slow[: min(4, slow.size)] if slow.size else ordered[:1]
    if np.max(np.abs(leading)) > unstable_tol:
        return "unstable"
    if np.any(np.abs(np.imag(leading)) > imag_tol):
        return "complex"
    if float(np.real(leading[0])) < -imag_tol:
        return "negative-real"
    return "real"


def _fmt_complex(value: complex) -> str:
    z = complex(value)
    if abs(z.imag) < 5e-5:
        return f"{z.real:.4f}"
    sign = "+" if z.imag >= 0 else "-"
    return f"{z.real:.4f}{sign}{abs(z.imag):.4f}i"


def _fit_to_row(
    fit: ARFit, *, imag_tol: float, unstable_tol: float, slow_abs_min: float
) -> dict[str, Any]:
    eig = fit.eigenvalues
    leading = eig[0] if eig.size else complex(np.nan)
    return {
        "lag": fit.lag,
        "lag_updates": fit.lag_updates,
        "n_pairs": fit.n_pairs,
        "residual_rms": fit.residual_rms,
        "classification": classify_eigenvalues(
            eig,
            imag_tol=imag_tol,
            unstable_tol=unstable_tol,
            slow_abs_min=slow_abs_min,
        ),
        "leading_abs": float(abs(leading)) if eig.size else None,
        "leading_real": float(np.real(leading)) if eig.size else None,
        "leading_imag": float(np.imag(leading)) if eig.size else None,
        "top_eigenvalues": [_fmt_complex(v) for v in eig[:6]],
    }


def run_probe(args: argparse.Namespace) -> dict[str, Any]:
    results: list[dict[str, Any]] = []
    for amplitude_att in args.amplitude_att:
        raw_series: list[np.ndarray] = []
        sample_counts: list[int] = []
        for seed in args.seeds:
            cfg = _config(args, amplitude_att=float(amplitude_att))
            traj = simulate_augmented_features(cfg, seed=int(seed))
            features = np.asarray(traj["augmented_features"], dtype=float)
            raw_series.append(features)
            sample_counts.append(int(features.shape[0]))
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
        results.append(
            {
                "amplitude_att": float(amplitude_att),
                "feature_dim_raw": int(raw_series[0].shape[1]),
                "feature_dim_projected": int(projected[0].shape[1]),
                "pca_explained_ratio": [float(x) for x in explained_ratio],
                "sample_counts": sample_counts,
                "rows": rows,
            }
        )
    return {
        "description": "Corrected-sign AR mode probe on reduced augmented features.",
        "created_utc": _utc_now(),
        "git_revision": _git_output(["rev-parse", "HEAD"]),
        "git_status": _git_output(["status", "--short"]),
        "parameters": vars(args),
        "results": results,
    }


def _fmt(value: Any, digits: int = 4) -> str:
    if value is None:
        return "`n/a`"
    try:
        number = float(value)
    except (TypeError, ValueError):
        return f"`{value}`"
    if not np.isfinite(number):
        return "`n/a`"
    if number == 0.0:
        text = "0"
    elif abs(number) < 1e-3 or abs(number) >= 1e4:
        text = f"{number:.{digits}e}"
    else:
        text = f"{number:.{digits}f}"
    return f"`{text}`"


def build_report(payload: dict[str, Any]) -> str:
    lines = [
        "# AR Mode Probe on Corrected Candidates",
        "",
        f"Date: {payload['created_utc']}.",
        "",
        "## Scope",
        "",
        "This report fits linear autoregressive maps on PCA-reduced augmented-state",
        "features for the corrected-sign compact candidates. It is a coarse-grained",
        "mode diagnostic, not evidence that the selected variables are closed.",
        "",
        "A complex conjugate pair would be an empirical reason to pursue a phase- or",
        "wave-like effective model. Purely real modes support a relaxation-only",
        "reading for the scalar memory model.",
        "",
        "## Parameters",
        "",
    ]
    params = payload["parameters"]
    for key in [
        "steps",
        "burn_in",
        "sample_every",
        "seeds",
        "amplitude_att",
        "alpha",
        "memory_mass",
        "sigma_rep",
        "sigma_att",
        "amplitude_rep",
        "lags",
        "pca_components",
        "ridge",
        "slow_abs_min",
    ]:
        lines.append(f"- `{key}`: `{params[key]}`")
    lines.extend(["", "## Mode Summary", ""])
    lines.append(
        "| A_att | lag samples | lag updates | class | leading | |leading| | residual rms | n pairs | top eigenvalues |"
    )
    lines.append("| ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: | --- |")
    for result in payload["results"]:
        for row in result["rows"]:
            leading = complex(row["leading_real"] or 0.0, row["leading_imag"] or 0.0)
            lines.append(
                f"| `{result['amplitude_att']:.6g}` | `{row['lag']}` | `{row['lag_updates']}` | "
                f"`{row['classification']}` | `{_fmt_complex(leading)}` | "
                f"{_fmt(row['leading_abs'])} | {_fmt(row['residual_rms'])} | "
                f"`{row['n_pairs']}` | `{' ; '.join(row['top_eigenvalues'])}` |"
            )
    lines.extend(["", "## PCA Coverage", ""])
    lines.append("| A_att | raw dim | projected dim | explained ratio first components |")
    lines.append("| ---: | ---: | ---: | --- |")
    for result in payload["results"]:
        ratios = ", ".join(f"{x:.3f}" for x in result["pca_explained_ratio"])
        lines.append(
            f"| `{result['amplitude_att']:.6g}` | `{result['feature_dim_raw']}` | "
            f"`{result['feature_dim_projected']}` | `{ratios}` |"
        )
    lines.extend(
        [
            "",
            "## Reading",
            "",
            "- Treat classifications as lag- and feature-dependent diagnostics.",
            "- A classification is meaningful only if it is stable across several lags.",
            "- Fast complex residues below `slow_abs_min` are reported in the eigenvalue",
            "  list but do not make the slow-mode classification complex.",
            "- If the corrected scalar candidates show only real modes, the current",
            "  scalar memory model supports relaxation/confinement more directly than",
            "  oscillator or photon analogies.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    args = parse_args()
    payload = run_probe(args)
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
