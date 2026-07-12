# Knot Score v0.4 Report

Date: 2026-07-07T21:39:04Z.

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
| `baseline` | `1` | `1.000` | `3.077` | `14.748` | `0.416` | `1.680` | `6.778` | `4.138` | `1.820` | `1.0/1.0/1.0/1.0/1.0/1.0/1.0` |
| `baseline` | `2` | `0.857` | `1.500` | `14.667` | `0.852` | `1.699` | `8.885` | `1.863` | `1.480` | `0.0/1.0/1.0/1.0/1.0/1.0/1.0` |
| `baseline` | `3` | `1.000` | `3.368` | `14.717` | `0.713` | `1.814` | `5.208` | `2.110` | `1.536` | `1.0/1.0/1.0/1.0/1.0/1.0/1.0` |
| `baseline` | `4` | `1.000` | `5.150` | `14.708` | `0.350` | `1.638` | `5.004` | `1.940` | `1.634` | `1.0/1.0/1.0/1.0/1.0/1.0/1.0` |
| `baseline` | `5` | `1.000` | `7.092` | `14.760` | `0.423` | `1.538` | `4.486` | `2.641` | `1.770` | `1.0/1.0/1.0/1.0/1.0/1.0/1.0` |
| `baseline` | `6` | `0.929` | `11.750` | `14.740` | `0.153` | `1.668` | `5.729` | `1.737` | `1.602` | `1.0/1.0/0.5/1.0/1.0/1.0/1.0` |
| `baseline` | `7` | `0.714` | `3.540` | `14.681` | `0.289` | `1.822` | `4.046` | `1.139` | `1.063` | `1.0/1.0/1.0/1.0/1.0/0.0/0.0` |
| `baseline` | `8` | `0.786` | `6.476` | `14.733` | `0.529` | `1.653` | `5.310` | `1.212` | `1.075` | `1.0/1.0/1.0/1.0/1.0/0.5/0.0` |
| `baseline` | `9` | `0.857` | `11.500` | `14.753` | `0.145` | `1.518` | `5.862` | `2.108` | `1.423` | `1.0/1.0/0.0/1.0/1.0/1.0/1.0` |
| `baseline` | `10` | `0.857` | `1.780` | `14.752` | `0.602` | `1.712` | `8.701` | `3.313` | `1.983` | `0.0/1.0/1.0/1.0/1.0/1.0/1.0` |
| `baseline` | `11` | `0.857` | `7.896` | `14.726` | `0.148` | `1.796` | `4.701` | `1.867` | `1.456` | `1.0/1.0/0.0/1.0/1.0/1.0/1.0` |
| `baseline` | `12` | `0.929` | `3.500` | `14.736` | `0.333` | `1.431` | `4.773` | `1.967` | `1.468` | `1.0/1.0/1.0/0.5/1.0/1.0/1.0` |
| `baseline` | `13` | `0.929` | `9.125` | `14.725` | `0.178` | `1.701` | `4.336` | `1.897` | `1.508` | `1.0/1.0/0.5/1.0/1.0/1.0/1.0` |
| `baseline` | `14` | `0.786` | `2.500` | `14.748` | `0.775` | `1.284` | `4.972` | `1.569` | `1.212` | `0.5/1.0/1.0/0.5/1.0/1.0/0.5` |
| `baseline` | `15` | `0.857` | `1.711` | `14.635` | `0.994` | `1.783` | `7.123` | `2.004` | `1.739` | `0.0/1.0/1.0/1.0/1.0/1.0/1.0` |
| `single_scale` | `1` | `1.000` | `3.064` | `15.320` | `0.555` | `1.684` | `6.935` | `4.188` | `1.831` | `1.0/1.0/1.0/1.0/1.0/1.0/1.0` |
| `single_scale` | `2` | `0.857` | `1.453` | `15.234` | `0.705` | `1.696` | `9.077` | `1.865` | `1.481` | `0.0/1.0/1.0/1.0/1.0/1.0/1.0` |
| `single_scale` | `3` | `1.000` | `3.368` | `15.290` | `0.468` | `1.817` | `5.321` | `2.117` | `1.538` | `1.0/1.0/1.0/1.0/1.0/1.0/1.0` |
| `single_scale` | `4` | `1.000` | `5.550` | `15.281` | `0.288` | `1.654` | `5.096` | `1.947` | `1.637` | `1.0/1.0/1.0/1.0/1.0/1.0/1.0` |
| `single_scale` | `5` | `1.000` | `7.583` | `15.332` | `0.396` | `1.536` | `4.584` | `2.664` | `1.780` | `1.0/1.0/1.0/1.0/1.0/1.0/1.0` |
| `single_scale` | `6` | `0.929` | `6.571` | `15.315` | `0.156` | `1.585` | `5.860` | `1.744` | `1.604` | `1.0/1.0/0.5/1.0/1.0/1.0/1.0` |
| `single_scale` | `7` | `0.643` | `3.213` | `15.254` | `0.246` | `1.826` | `4.116` | `1.142` | `1.063` | `1.0/1.0/0.5/1.0/1.0/0.0/0.0` |
| `single_scale` | `8` | `0.714` | `6.476` | `15.305` | `0.254` | `1.313` | `5.424` | `1.220` | `1.077` | `1.0/1.0/1.0/0.5/1.0/0.5/0.0` |
| `single_scale` | `9` | `0.929` | `11.667` | `15.327` | `0.200` | `1.523` | `5.997` | `2.122` | `1.426` | `1.0/1.0/0.5/1.0/1.0/1.0/1.0` |
| `single_scale` | `10` | `0.857` | `1.942` | `15.325` | `0.691` | `1.711` | `8.934` | `3.317` | `1.983` | `0.0/1.0/1.0/1.0/1.0/1.0/1.0` |
| `single_scale` | `11` | `0.857` | `5.750` | `15.297` | `0.143` | `1.794` | `4.788` | `1.861` | `1.455` | `1.0/1.0/0.0/1.0/1.0/1.0/1.0` |
| `single_scale` | `12` | `0.857` | `8.000` | `15.312` | `0.177` | `1.430` | `4.866` | `1.985` | `1.474` | `1.0/1.0/0.5/0.5/1.0/1.0/1.0` |
| `single_scale` | `13` | `0.929` | `9.125` | `15.297` | `0.192` | `1.700` | `4.418` | `1.907` | `1.511` | `1.0/1.0/0.5/1.0/1.0/1.0/1.0` |
| `single_scale` | `14` | `0.857` | `4.643` | `15.324` | `0.754` | `1.279` | `5.073` | `1.584` | `1.216` | `1.0/1.0/1.0/0.5/1.0/1.0/0.5` |
| `single_scale` | `15` | `0.857` | `1.578` | `15.201` | `0.592` | `1.777` | `7.275` | `2.026` | `1.745` | `0.0/1.0/1.0/1.0/1.0/1.0/1.0` |

## Condition Summary

| condition | n | score mean | score median | residence gain median | sample compactness median | voxel stability median | D_occ median | memory compactness median | memory roundness gain median | memory dimension gain median |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `baseline` | `15` | `0.890` | `0.857` | `3.540` | `14.733` | `0.416` | `1.680` | `5.208` | `1.940` | `1.508` |
| `single_scale` | `15` | `0.886` | `0.857` | `5.550` | `15.305` | `0.288` | `1.684` | `5.321` | `1.947` | `1.511` |

## Shape Summary

| condition | sample dim med | sample roundness med | sample radius med | memory dim med | memory roundness med | memory radius med |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `baseline` | `1.678` | `0.303` | `1.119` | `2.786` | `0.705` | `0.099` |
| `eta_zero` | `1.657` | `0.298` | `16.473` | `1.845` | `0.340` | `0.508` |
| `single_scale` | `1.679` | `0.303` | `1.077` | `2.795` | `0.710` | `0.097` |

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
