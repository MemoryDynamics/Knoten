# Knot Score v0.3 Report

Date: 2026-07-02T07:47:07Z.

## Scope

This report applies a scorecard-style knot criterion to the existing
matched long-run JSON files. It does not rerun simulations and it does not
claim a final scalar knot definition.

The current score averages four available components against the matched
`eta_zero` seed control:

- residence gain over control, pass at `>=3`, partial at `>=2`;
- compactness gain, defined as `eta_zero radius / case radius`, pass at `>=5`, partial at `>=3`;
- voxel stability, defined as min/max residence across voxel sizes, pass at `>=0.25`, partial at `>=0.15`;
- internal occupancy dimension `D_occ`, pass at `>=1.5`, partial at `>=1.25`.

The `D_occ` component is an internal-dimensional-support signal, not an
external three-dimensionality criterion. Shape roundness is reported where
available, but it is not yet included in the scalar score; older JSON files
may report `n/a` for the newer center/shape diagnostics.

## Seed Scorecard

| condition | seed | score | residence gain | compactness gain | voxel stability | D_occ | roundness | best residence | radius | components R/C/V/D |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `baseline` | `1` | `0.750` | `1.868` | `14.774` | `0.475` | `1.961` | `0.312` | `48.571` | `1.090` | `0.0/1.0/1.0/1.0` |
| `baseline` | `2` | `0.750` | `0.574` | `14.716` | `0.799` | `1.846` | `0.323` | `21.818` | `1.042` | `0.0/1.0/1.0/1.0` |
| `baseline` | `3` | `0.875` | `2.430` | `14.722` | `0.280` | `1.961` | `0.474` | `48.591` | `0.996` | `0.5/1.0/1.0/1.0` |
| `baseline` | `4` | `0.875` | `2.150` | `14.740` | `0.264` | `1.834` | `0.301` | `55.889` | `1.434` | `0.5/1.0/1.0/1.0` |
| `baseline` | `5` | `0.875` | `2.160` | `14.751` | `0.451` | `1.773` | `0.337` | `82.071` | `1.266` | `0.5/1.0/1.0/1.0` |
| `single_scale` | `1` | `0.750` | `1.795` | `15.346` | `0.357` | `1.963` | `0.312` | `46.667` | `1.049` | `0.0/1.0/1.0/1.0` |
| `single_scale` | `2` | `0.750` | `0.600` | `15.286` | `0.606` | `1.847` | `0.323` | `22.818` | `1.003` | `0.0/1.0/1.0/1.0` |
| `single_scale` | `3` | `0.875` | `2.351` | `15.295` | `0.362` | `1.965` | `0.474` | `47.011` | `0.959` | `0.5/1.0/1.0/1.0` |
| `single_scale` | `4` | `0.750` | `1.843` | `15.314` | `0.254` | `1.837` | `0.301` | `47.913` | `1.380` | `0.0/1.0/1.0/1.0` |
| `single_scale` | `5` | `0.875` | `2.658` | `15.322` | `0.330` | `1.774` | `0.337` | `101.022` | `1.219` | `0.5/1.0/1.0/1.0` |

## Condition Summary

| condition | n | score mean | score median | residence gain median | compactness gain median | voxel stability median | D_occ median |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `baseline` | `5` | `0.825` | `0.875` | `2.150` | `14.740` | `0.451` | `1.846` |
| `single_scale` | `5` | `0.800` | `0.750` | `1.843` | `15.314` | `0.357` | `1.847` |

## Shape Summary

| condition | sample dim med | sample roundness med | sample radius med | memory dim med | memory roundness med | memory radius med |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `baseline` | `2.005` | `0.323` | `1.090` | `2.678` | `0.642` | `0.098` |
| `eta_zero` | `2.001` | `0.318` | `16.098` | `1.639` | `0.331` | `0.508` |
| `single_scale` | `2.006` | `0.323` | `1.049` | `2.683` | `0.644` | `0.096` |

## Reading

- High score means the condition separates from the no-feedback
  `eta_zero` control for that seed in residence, compactness, voxel
  stability, and non-collapsed internal occupancy dimension.
- This is a feedback-confinement plus internal-dimensional-support score,
  not yet a proof of a specific two-scale knot mechanism.
- Baseline minus `single_scale` score difference has median `0`;
  therefore the current score still does not isolate the baseline two-scale
  kernel as necessary.
- New long-run outputs include center/shape diagnostics; the next evidence
  step is to decide whether sample-shape, memory-cloud shape, or both
  deserve separate v0.4 score components.
