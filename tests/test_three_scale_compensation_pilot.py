from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments" / "current" / "kernels"))
sys.path.insert(0, str(ROOT / "src"))

import three_scale_compensation_pilot as pilot  # noqa: E402


def _args() -> argparse.Namespace:
    return argparse.Namespace(
        steps=5_000,
        dim=3,
        epsilon=1.0e-4,
        eta=0.15,
        alpha=0.01,
        memory_mass=1.0,
        sigma_rep=1.0,
        sigma_att=3.0,
        sigma_comp=10.0,
        amplitude_rep=1.0,
        amplitude_att=35.0,
        memory_factor=6.0,
        max_memory=600,
        burn_in=0,
        sample_every=100,
    )


def test_build_variants_separates_integral_and_curvature_constraints() -> None:
    variants = pilot.build_variants(_args())
    baseline, raw, matched = variants

    assert baseline.integral_coefficient == pytest.approx(-944.0)
    assert baseline.radial_force_crossing is None
    assert raw.integral_coefficient == pytest.approx(0.0, abs=1e-10)
    assert raw.curvature_retention == pytest.approx(0.9967323076923077)
    assert raw.radial_force_crossing == pytest.approx(10.9130736242)
    assert matched.integral_coefficient == pytest.approx(0.0, abs=2e-10)
    assert matched.local_curvature == pytest.approx(baseline.local_curvature)
    assert matched.config.amplitude_att == pytest.approx(35.08516695570236)
    assert matched.amplitude_comp == pytest.approx(0.9462995078039638)


def test_paired_differences_compare_same_seed_to_two_scale() -> None:
    variants = pilot.build_variants(_args())
    rows = []
    for seed, baseline_radius, raw_radius, matched_radius in [
        (1, 1.0, 1.01, 1.0),
        (2, 2.0, 2.04, 2.0),
    ]:
        for variant, radius in zip(
            variants,
            [baseline_radius, raw_radius, matched_radius],
            strict=True,
        ):
            rows.append(
                {
                    "variant": variant.label,
                    "seed": seed,
                    "memory_radius": radius,
                }
            )

    differences = pilot._paired_differences(rows, variants)
    raw_radius = next(
        item
        for item in differences
        if item["variant"] == "zero_mean_raw" and item["metric"] == "memory_radius"
    )
    matched_radius = next(
        item
        for item in differences
        if item["variant"] == "zero_mean_curvature_matched"
        and item["metric"] == "memory_radius"
    )

    assert raw_radius["n_seeds"] == 2
    assert raw_radius["median_relative_difference"] == pytest.approx(0.015)
    assert raw_radius["max_relative_difference"] == pytest.approx(0.02)
    assert matched_radius["max_relative_difference"] == 0.0
