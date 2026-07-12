# Knot Score v0.4 Report

Date: 2026-07-02T10:55:37Z.

## Scope

This report applies a scorecard-style knot criterion to matched long-run
JSON files. It does not rerun simulations and it does not claim a final
scalar knot definition.

The v0.4 score averages seven components against the matched
`eta_zero` seed control:

- residence gain over control, pass at `>=3`, partial at `>=2`;
- sample compactness gain, defined as `eta_zero radius / case radius`, pass at `>=5`, partial at `>=3`;
- voxel stability, defined as min/max residence across voxel sizes, pass at `>=0.25`, partial at `>=0.15`;
- internal occupancy dimension `D_occ`, pass at `>=1.5`, partial at `>=1.25`;
- memory-cloud compactness gain, pass at `>=3`, partial at `>=2`;
- memory-cloud roundness gain, pass at `>=1.5`, partial at `>=1.2`;
- memory-cloud shape-dimension gain, pass at `>=1.35`, partial at `>=1.15`.

The raw sample path remains reported diagnostics only. v0.4 treats the
weighted memory cloud as the candidate knot shape observable.

## Seed Scorecard

| condition | seed | score | residence gain | sample compactness | voxel stability | D_occ | memory compactness | memory roundness gain | memory dimension gain | components R/C/V/D/MC/MR/MD |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `baseline` | `1` | `0.857` | `1.868` | `14.774` | `0.475` | `1.961` | `6.778` | `4.138` | `1.820` | `0.0/1.0/1.0/1.0/1.0/1.0/1.0` |
| `baseline` | `2` | `0.857` | `0.574` | `14.716` | `0.799` | `1.846` | `8.885` | `1.863` | `1.480` | `0.0/1.0/1.0/1.0/1.0/1.0/1.0` |
| `baseline` | `3` | `0.929` | `2.430` | `14.722` | `0.280` | `1.961` | `5.208` | `2.110` | `1.536` | `0.5/1.0/1.0/1.0/1.0/1.0/1.0` |
| `baseline` | `4` | `0.929` | `2.150` | `14.740` | `0.264` | `1.834` | `5.004` | `1.940` | `1.634` | `0.5/1.0/1.0/1.0/1.0/1.0/1.0` |
| `baseline` | `5` | `0.929` | `2.160` | `14.751` | `0.451` | `1.773` | `4.486` | `2.641` | `1.770` | `0.5/1.0/1.0/1.0/1.0/1.0/1.0` |
| `single_scale` | `1` | `0.857` | `1.795` | `15.346` | `0.357` | `1.963` | `6.935` | `4.188` | `1.831` | `0.0/1.0/1.0/1.0/1.0/1.0/1.0` |
| `single_scale` | `2` | `0.857` | `0.600` | `15.286` | `0.606` | `1.847` | `9.077` | `1.865` | `1.481` | `0.0/1.0/1.0/1.0/1.0/1.0/1.0` |
| `single_scale` | `3` | `0.929` | `2.351` | `15.295` | `0.362` | `1.965` | `5.321` | `2.117` | `1.538` | `0.5/1.0/1.0/1.0/1.0/1.0/1.0` |
| `single_scale` | `4` | `0.857` | `1.843` | `15.314` | `0.254` | `1.837` | `5.096` | `1.947` | `1.637` | `0.0/1.0/1.0/1.0/1.0/1.0/1.0` |
| `single_scale` | `5` | `0.929` | `2.658` | `15.322` | `0.330` | `1.774` | `4.584` | `2.664` | `1.780` | `0.5/1.0/1.0/1.0/1.0/1.0/1.0` |

## Condition Summary

| condition | n | score mean | score median | residence gain median | sample compactness median | voxel stability median | D_occ median | memory compactness median | memory roundness gain median | memory dimension gain median |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `baseline` | `5` | `0.900` | `0.929` | `2.150` | `14.740` | `0.451` | `1.846` | `5.208` | `2.110` | `1.634` |
| `single_scale` | `5` | `0.886` | `0.857` | `1.843` | `15.314` | `0.357` | `1.847` | `5.321` | `2.117` | `1.637` |

## Shape Summary

| condition | sample dim med | sample roundness med | sample radius med | memory dim med | memory roundness med | memory radius med |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `baseline` | `2.005` | `0.323` | `1.090` | `2.678` | `0.642` | `0.098` |
| `eta_zero` | `2.001` | `0.318` | `16.098` | `1.639` | `0.331` | `0.508` |
| `single_scale` | `2.006` | `0.323` | `1.049` | `2.683` | `0.644` | `0.096` |

## Reading

- High score means the condition separates from the no-feedback
  `eta_zero` control for that seed under the selected score version.
- The score is an evidence scorecard, not a proof of a specific
  two-scale knot mechanism.
- Baseline minus `single_scale` score difference has median `0`;
  therefore this score still does not isolate the baseline two-scale
  kernel as necessary.
- Memory-cloud shape is now explicit in v0.4; the raw sample path remains
  a reported diagnostic rather than the knot-shape criterion.
