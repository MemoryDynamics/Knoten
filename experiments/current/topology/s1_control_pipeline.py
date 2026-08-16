"""Candidate-independent persistent-homology controls for the S1 program.

This module is deliberately limited to synthetic method-development data.  It
does not define a candidate observable, persistence cutoff, classifier, or
confirmatory decision.  In particular, a noisy finite period-p orbit is kept
as a semantic rival: its point cloud can look circular although its invariant
set contains only p points.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from importlib.metadata import version
import json
import math
from pathlib import Path
import platform
from typing import Any

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray
from ripser import ripser


DEFAULT_COEFFICIENT_PRIME = 2
VALID_SPLITS = ("method-training", "method-validation")
DEFAULT_SPLIT_SEEDS = {
    "method-training": 20260816,
    "method-validation": 20260817,
}

PROJECT_ROOT = Path(__file__).resolve().parents[3]
REPORT_PATH = (
    PROJECT_ROOT / "reports" / "topology" / "s1_control_pipeline_2026-08-16.md"
)
JSON_PATH = REPORT_PATH.with_suffix(".json")
FIGURE_PATH = (
    PROJECT_ROOT
    / "figures"
    / "draft"
    / "topology"
    / "s1_control_pipeline_2026-08-16.png"
)


@dataclass(frozen=True)
class PersistenceSummary:
    """Scale-normalized Vietoris-Rips persistence summary."""

    name: str
    n_points: int
    ambient_dimension: int
    normalization_rms_radius: float
    coefficient_prime: int
    metric: str
    h0_connectivity_scale: float
    finite_h1_count: int
    essential_h1_count: int
    h1_lifetimes: tuple[float, ...]
    top_h1_lifetime: float
    second_h1_lifetime: float
    top_h1_gap: float
    top_h1_share: float
    top_to_second_ratio: float | None


@dataclass(frozen=True)
class ControlSuite:
    """One synthetic control split and its method diagnostics."""

    split: str
    seed: int
    coefficient_prime: int
    versions: dict[str, str]
    roles: dict[str, str]
    sampling: dict[str, dict[str, Any]]
    clouds: dict[str, NDArray[np.float64]]
    summaries: dict[str, PersistenceSummary]
    diagnostics: dict[str, float | None]

    def to_json_dict(self) -> dict[str, Any]:
        """Return a stable, finite JSON representation without raw clouds."""

        return {
            "status": "method-development-only-no-candidate-data",
            "split": self.split,
            "seed": self.seed,
            "coefficient_prime": self.coefficient_prime,
            "versions": self.versions,
            "roles": self.roles,
            "sampling": self.sampling,
            "summaries": {
                name: asdict(summary) for name, summary in self.summaries.items()
            },
            "diagnostics": self.diagnostics,
        }


def _is_prime(value: int) -> bool:
    if value < 2:
        return False
    return all(value % divisor for divisor in range(2, math.isqrt(value) + 1))


def validate_coefficient_prime(value: int) -> int:
    """Validate the prime coefficient required by ripser."""

    if not _is_prime(value):
        raise ValueError("coefficient must be prime")
    return value


def normalize_point_cloud(
    points: NDArray[np.floating[Any]],
) -> tuple[NDArray[np.float64], float]:
    """Center a synthetic cloud and set its RMS radius to one."""

    cloud = np.asarray(points, dtype=np.float64)
    if cloud.ndim != 2 or cloud.shape[0] < 4 or cloud.shape[1] < 1:
        raise ValueError("point cloud must have shape (n >= 4, d >= 1)")
    if not np.isfinite(cloud).all():
        raise ValueError("point cloud must contain only finite values")

    centered = cloud - np.mean(cloud, axis=0, keepdims=True)
    rms_radius = float(np.sqrt(np.mean(np.sum(centered * centered, axis=1))))
    if not np.isfinite(rms_radius) or rms_radius <= np.finfo(np.float64).eps:
        raise ValueError("point cloud has zero or invalid RMS radius")
    return centered / rms_radius, rms_radius


def _finite_lifetimes(diagram: NDArray[np.float64]) -> NDArray[np.float64]:
    if diagram.size == 0:
        return np.empty(0, dtype=np.float64)
    finite = diagram[np.isfinite(diagram[:, 1])]
    lifetimes = finite[:, 1] - finite[:, 0]
    return np.sort(lifetimes[lifetimes > 0.0])[::-1]


def persistent_h1_summary(
    name: str,
    points: NDArray[np.floating[Any]],
    *,
    coefficient_prime: int = DEFAULT_COEFFICIENT_PRIME,
) -> PersistenceSummary:
    """Compute full-cloud H0/H1 Vietoris-Rips persistence."""

    coefficient_prime = validate_coefficient_prime(coefficient_prime)
    normalized, rms_radius = normalize_point_cloud(points)
    result = ripser(
        normalized,
        maxdim=1,
        coeff=coefficient_prime,
        do_cocycles=False,
    )
    h0, h1 = (np.asarray(diagram, dtype=np.float64) for diagram in result["dgms"])

    h0_deaths = h0[np.isfinite(h0[:, 1]), 1]
    h0_connectivity_scale = float(np.max(h0_deaths, initial=0.0))
    lifetimes = _finite_lifetimes(h1)
    essential_h1_count = int(np.sum(~np.isfinite(h1[:, 1]))) if h1.size else 0

    top = float(lifetimes[0]) if lifetimes.size else 0.0
    second = float(lifetimes[1]) if lifetimes.size > 1 else 0.0
    total = float(np.sum(lifetimes))
    ratio = top / second if second > np.finfo(np.float64).eps else None

    return PersistenceSummary(
        name=name,
        n_points=int(normalized.shape[0]),
        ambient_dimension=int(normalized.shape[1]),
        normalization_rms_radius=rms_radius,
        coefficient_prime=coefficient_prime,
        metric="euclidean-after-centering-and-rms-radius-normalization",
        h0_connectivity_scale=h0_connectivity_scale,
        finite_h1_count=int(lifetimes.size),
        essential_h1_count=essential_h1_count,
        h1_lifetimes=tuple(float(value) for value in lifetimes),
        top_h1_lifetime=top,
        second_h1_lifetime=second,
        top_h1_gap=top - second,
        top_h1_share=top / total if total > 0.0 else 0.0,
        top_to_second_ratio=ratio,
    )


def noisy_circle(
    rng: np.random.Generator,
    *,
    n_points: int = 192,
    radial_noise: float = 0.025,
) -> NDArray[np.float64]:
    theta = np.linspace(0.0, 2.0 * np.pi, n_points, endpoint=False)
    radius = 1.0 + rng.normal(scale=radial_noise, size=n_points)
    cloud = np.column_stack((radius * np.cos(theta), radius * np.sin(theta)))
    return cloud + rng.normal(scale=radial_noise / 4.0, size=cloud.shape)


def stable_hopf_limit_cycle(
    *,
    n_points: int = 192,
    steps_per_sample: int = 4,
    dt: float = 0.01,
    omega: float = 2.0,
) -> NDArray[np.float64]:
    """Sample the stationary window of a deterministic supercritical Hopf flow."""

    total_samples = n_points + 400
    state = np.array([0.2, 0.0], dtype=np.float64)
    samples = np.empty((total_samples, 2), dtype=np.float64)

    def vector_field(value: NDArray[np.float64]) -> NDArray[np.float64]:
        radius_sq = float(value @ value)
        return np.array(
            [
                (1.0 - radius_sq) * value[0] - omega * value[1],
                omega * value[0] + (1.0 - radius_sq) * value[1],
            ]
        )

    for sample_index in range(total_samples):
        for _ in range(steps_per_sample):
            k1 = vector_field(state)
            k2 = vector_field(state + 0.5 * dt * k1)
            k3 = vector_field(state + 0.5 * dt * k2)
            k4 = vector_field(state + dt * k3)
            state = state + dt * (k1 + 2.0 * k2 + 2.0 * k3 + k4) / 6.0
        samples[sample_index] = state
    return samples[-n_points:]


def noisy_flat_torus(
    rng: np.random.Generator,
    *,
    n_major: int = 17,
    n_minor: int = 17,
    noise: float = 0.012,
) -> NDArray[np.float64]:
    """Sample S1 x S1 in its flat four-dimensional embedding."""

    u = np.linspace(0.0, 2.0 * np.pi, n_major, endpoint=False)
    v = np.linspace(0.0, 2.0 * np.pi, n_minor, endpoint=False)
    uu, vv = np.meshgrid(u, v, indexing="ij")
    cloud = np.column_stack(
        (
            np.cos(uu).ravel(),
            np.sin(uu).ravel(),
            np.cos(vv).ravel(),
            np.sin(vv).ravel(),
        )
    )
    return cloud + rng.normal(scale=noise, size=cloud.shape)


def filled_disk(
    rng: np.random.Generator,
    *,
    n_points: int = 224,
) -> NDArray[np.float64]:
    radius = np.sqrt(rng.uniform(size=n_points))
    theta = rng.uniform(0.0, 2.0 * np.pi, size=n_points)
    return np.column_stack((radius * np.cos(theta), radius * np.sin(theta)))


def noisy_interval(
    rng: np.random.Generator,
    *,
    n_points: int = 192,
    transverse_noise: float = 0.012,
) -> NDArray[np.float64]:
    coordinate = np.linspace(-1.0, 1.0, n_points)
    return np.column_stack(
        (
            coordinate,
            rng.normal(scale=transverse_noise, size=n_points),
        )
    )


def damped_spiral(
    rng: np.random.Generator,
    *,
    n_points: int = 224,
    turns: float = 4.0,
    decay: float = 0.08,
    noise: float = 0.008,
) -> NDArray[np.float64]:
    theta = np.linspace(0.0, turns * 2.0 * np.pi, n_points)
    radius = np.exp(-decay * theta)
    cloud = np.column_stack((radius * np.cos(theta), radius * np.sin(theta)))
    return cloud + rng.normal(scale=noise, size=cloud.shape)


def noisy_discrete_cycle(
    rng: np.random.Generator,
    *,
    period: int = 12,
    repeats: int = 16,
    noise: float = 0.012,
) -> NDArray[np.float64]:
    phase = 2.0 * np.pi * np.arange(period) / period
    support = np.column_stack((np.cos(phase), np.sin(phase)))
    cloud = np.repeat(support, repeats=repeats, axis=0)
    return cloud + rng.normal(scale=noise, size=cloud.shape)


def _rng(seed: int, stream: int) -> np.random.Generator:
    return np.random.default_rng(np.random.SeedSequence([seed, stream]))


def build_control_suite(
    *,
    split: str = "method-training",
    seed: int | None = None,
    coefficient_prime: int = DEFAULT_COEFFICIENT_PRIME,
) -> ControlSuite:
    """Generate one fixed synthetic split and compute descriptive summaries."""

    if split not in VALID_SPLITS:
        raise ValueError(f"split must be one of {VALID_SPLITS}")
    if seed is None:
        seed = DEFAULT_SPLIT_SEEDS[split]
    if seed < 0:
        raise ValueError("seed must be nonnegative")
    coefficient_prime = validate_coefficient_prime(coefficient_prime)

    clouds = {
        "noisy-circle": noisy_circle(_rng(seed, 1)),
        "stable-hopf-cycle": stable_hopf_limit_cycle(),
        "flat-torus": noisy_flat_torus(_rng(seed, 2)),
        "filled-disk": filled_disk(_rng(seed, 3)),
        "noisy-interval": noisy_interval(_rng(seed, 4)),
        "damped-spiral": damped_spiral(_rng(seed, 5)),
        "finite-12-cycle": noisy_discrete_cycle(_rng(seed, 6)),
    }
    roles = {
        "noisy-circle": "positive S1-like geometric control",
        "stable-hopf-cycle": "positive known stable continuous-time limit cycle",
        "flat-torus": "positive two-generator rival that must not be called one S1",
        "filled-disk": "contractible two-dimensional negative control",
        "noisy-interval": "one-dimensional-with-boundary negative control",
        "damped-spiral": "transient damped-focus rival",
        "finite-12-cycle": (
            "semantic rival: circular cloud, but the noiseless invariant set "
            "has twelve points rather than topology S1"
        ),
    }
    sampling: dict[str, dict[str, Any]] = {
        "noisy-circle": {"n_points": 192, "radial_noise": 0.025},
        "stable-hopf-cycle": {
            "n_points": 192,
            "steps_per_sample": 4,
            "dt": 0.01,
            "omega": 2.0,
            "stationary_window_after_samples": 400,
        },
        "flat-torus": {
            "n_major": 17,
            "n_minor": 17,
            "ambient_dimension": 4,
            "noise": 0.012,
        },
        "filled-disk": {"n_points": 224},
        "noisy-interval": {"n_points": 192, "transverse_noise": 0.012},
        "damped-spiral": {
            "n_points": 224,
            "turns": 4.0,
            "decay": 0.08,
            "noise": 0.008,
        },
        "finite-12-cycle": {"period": 12, "repeats": 16, "noise": 0.012},
    }
    summaries = {
        name: persistent_h1_summary(
            name,
            cloud,
            coefficient_prime=coefficient_prime,
        )
        for name, cloud in clouds.items()
    }

    permutation = _rng(seed, 99).permutation(clouds["noisy-circle"].shape[0])
    permuted_summary = persistent_h1_summary(
        "noisy-circle-permuted",
        clouds["noisy-circle"][permutation],
        coefficient_prime=coefficient_prime,
    )
    circle_lifetimes = np.asarray(
        summaries["noisy-circle"].h1_lifetimes,
        dtype=np.float64,
    )
    permuted_lifetimes = np.asarray(
        permuted_summary.h1_lifetimes,
        dtype=np.float64,
    )
    if circle_lifetimes.shape != permuted_lifetimes.shape:
        permutation_error = None
    else:
        permutation_error = float(
            np.max(np.abs(circle_lifetimes - permuted_lifetimes), initial=0.0)
        )

    def safe_ratio(numerator: float, denominator: float) -> float | None:
        if denominator <= np.finfo(np.float64).eps:
            return None
        return numerator / denominator

    diagnostics = {
        "point_order_max_h1_lifetime_error": permutation_error,
        "circle_top_to_disk_top": safe_ratio(
            summaries["noisy-circle"].top_h1_lifetime,
            summaries["filled-disk"].top_h1_lifetime,
        ),
        "circle_top_to_interval_top": safe_ratio(
            summaries["noisy-circle"].top_h1_lifetime,
            summaries["noisy-interval"].top_h1_lifetime,
        ),
        "torus_second_to_circle_second": safe_ratio(
            summaries["flat-torus"].second_h1_lifetime,
            summaries["noisy-circle"].second_h1_lifetime,
        ),
        "finite_cycle_top_to_circle_top": safe_ratio(
            summaries["finite-12-cycle"].top_h1_lifetime,
            summaries["noisy-circle"].top_h1_lifetime,
        ),
        "spiral_top_to_circle_top": safe_ratio(
            summaries["damped-spiral"].top_h1_lifetime,
            summaries["noisy-circle"].top_h1_lifetime,
        ),
    }
    versions = {
        "python": platform.python_version(),
        "numpy": version("numpy"),
        "matplotlib": version("matplotlib"),
        "ripser": version("ripser"),
        "scipy": version("scipy"),
        "scikit-learn": version("scikit-learn"),
    }
    return ControlSuite(
        split=split,
        seed=seed,
        coefficient_prime=coefficient_prime,
        versions=versions,
        roles=roles,
        sampling=sampling,
        clouds=clouds,
        summaries=summaries,
        diagnostics=diagnostics,
    )


def _project_for_display(cloud: NDArray[np.float64]) -> NDArray[np.float64]:
    centered = cloud - np.mean(cloud, axis=0, keepdims=True)
    if centered.shape[1] == 1:
        return np.column_stack((centered[:, 0], np.zeros(centered.shape[0])))
    _, _, right = np.linalg.svd(centered, full_matrices=False)
    return centered @ right[:2].T


def write_figure(suite: ControlSuite, path: Path = FIGURE_PATH) -> None:
    """Write a diagnostic projection; persistence uses the full cloud."""

    path.parent.mkdir(parents=True, exist_ok=True)
    figure, axes = plt.subplots(2, 4, figsize=(13.2, 6.7), constrained_layout=True)
    for axis, (name, cloud) in zip(axes.flat, suite.clouds.items(), strict=False):
        projection = _project_for_display(cloud)
        summary = suite.summaries[name]
        axis.scatter(
            projection[:, 0],
            projection[:, 1],
            s=7,
            alpha=0.70,
            linewidths=0,
        )
        axis.set_title(
            f"{name}\nH1 lifetimes: "
            f"{summary.top_h1_lifetime:.3f}, "
            f"{summary.second_h1_lifetime:.3f}",
            fontsize=9,
        )
        axis.set_aspect("equal", adjustable="datalim")
        axis.set_xticks([])
        axis.set_yticks([])
    for axis in axes.flat[len(suite.clouds) :]:
        axis.axis("off")
        axis.text(
            0.02,
            0.96,
            "Method control only\nNo candidate data\nNo decision cutoff",
            va="top",
            fontsize=11,
        )
    figure.suptitle(
        "Synthetic topology controls: display projections only",
        fontsize=13,
    )
    figure.savefig(path, dpi=180)
    plt.close(figure)


def _fmt(value: float | None) -> str:
    return "undefined" if value is None else f"{value:.6g}"


def write_report(suite: ControlSuite, path: Path = REPORT_PATH) -> None:
    """Write the human-readable method-development record."""

    path.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    for name, summary in suite.summaries.items():
        rows.append(
            "| "
            + " | ".join(
                (
                    name,
                    suite.roles[name],
                    str(summary.n_points),
                    str(summary.ambient_dimension),
                    f"{summary.top_h1_lifetime:.4f}",
                    f"{summary.second_h1_lifetime:.4f}",
                    f"{summary.top_h1_gap:.4f}",
                    f"{summary.top_h1_share:.4f}",
                )
            )
            + " |"
        )

    diagnostics = "\n".join(
        f"- {name}: {_fmt(value)}" for name, value in suite.diagnostics.items()
    )
    report = f"""# Candidate-independent S1 topology controls

Date: 2026-08-16.

Status: method development only. This run contains no knot candidate data and
defines no topology threshold, classifier, candidate metric, observable,
embedding, or confirmatory decision.

## Frozen method facts for this control run

- split: {suite.split}
- seed: {suite.seed}
- metric: Euclidean after centering and RMS-radius normalization
- filtration: full-cloud Vietoris-Rips through H1
- coefficient field: F_{suite.coefficient_prime}
- essential H1 handling: counted separately; no essential class is converted
  into a finite lifetime
- ripser: {suite.versions["ripser"]}
- Python: {suite.versions["python"]}
- numpy: {suite.versions["numpy"]}
- matplotlib: {suite.versions["matplotlib"]}
- scipy: {suite.versions["scipy"]}
- scikit-learn: {suite.versions["scikit-learn"]}

The normalization is a synthetic-control convention, not a candidate
observable contract. A distinct method-validation seed is preassigned, but its
realization is intentionally not generated or inspected here. No cutoff may be
inferred from this single training split.

## Descriptive results

| control | role | n | ambient d | top H1 | second H1 | gap | top share |
|---|---|---:|---:|---:|---:|---:|---:|
{chr(10).join(rows)}

Diagnostics:

{diagnostics}

The raw-cloud point-order permutation is an invariance test: it must leave
persistence unchanged. It is not a negative topology control. The finite
12-cycle is deliberately more dangerous: its cloud can carry a long H1 bar,
but the underlying noiseless invariant set is twelve points, not S1. Persistent
homology therefore cannot by itself distinguish an invariant circle from a
high-period discrete orbit.

The torus control tests a different failure mode. A procedure that reports
only the longest bar can conceal its second independent H1 generator and
mislabel S1 x S1 as one circle. Conversely, the filled disk, interval and
damped spiral show why persistence, intrinsic dimension, boundary, stationarity
and temporal dynamics must remain separate gates.

![Synthetic control projections](../../figures/draft/topology/s1_control_pipeline_2026-08-16.png)

The figure uses two-dimensional display projections only. Persistence was
computed in the full listed ambient space.

## Decision

This is a software and semantic smoke test, not calibration. It authorizes no
candidate run and supplies no D2 pass threshold. The next candidate-independent
step is to freeze a training-only threshold-selection rule and additional
matched temporal null families; the untouched method-validation split must
then audit that frozen rule. Candidate analysis remains blocked by P0.

Machine-readable record:
[JSON](s1_control_pipeline_2026-08-16.json).

## Reproduction

Run the registered method-training realization and its focused tests with:

    python experiments/current/topology/s1_control_pipeline.py --split method-training
    python -m pytest tests/test_s1_topology_controls.py -q
"""
    path.write_text(report, encoding="utf-8")


def write_json(suite: ControlSuite, path: Path = JSON_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            suite.to_json_dict(),
            indent=2,
            sort_keys=True,
            allow_nan=False,
        )
        + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--split", choices=VALID_SPLITS, default="method-training")
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="override the registered seed for the chosen split",
    )
    parser.add_argument(
        "--coefficient-prime",
        type=int,
        default=DEFAULT_COEFFICIENT_PRIME,
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    suite = build_control_suite(
        split=args.split,
        seed=args.seed,
        coefficient_prime=args.coefficient_prime,
    )
    write_figure(suite)
    write_report(suite)
    write_json(suite)
    print(f"Wrote {REPORT_PATH.relative_to(PROJECT_ROOT)}")
    print(f"Wrote {JSON_PATH.relative_to(PROJECT_ROOT)}")
    print(f"Wrote {FIGURE_PATH.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
