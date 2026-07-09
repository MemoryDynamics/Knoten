# Knot Score v0.5 Report

Date: 2026-07-09T05:32:46Z.

## Scope

This report applies a scorecard-style knot criterion to matched long-run
JSON files. It does not rerun simulations and it does not claim a final
scalar knot definition.

The v0.5 score is the control-safe variant for mixed-alpha comparisons.
It keeps the seven v0.4 components but changes two conventions:

- residence gain is compared in raw update counts, not in `alpha^{-1}` units;
- memory-cloud compactness only scores when the case has nondegenerate
  memory roundness and memory dimension diagnostics.

This prevents the `alpha=1` one-point memory limit from looking
artificially long-lived or compact merely because its memory time is one
update and its active memory cloud is degenerate.

## Seed Scorecard

| condition | seed | score | residence gain | sample compactness | voxel stability | D_occ | memory compactness | memory roundness gain | memory dimension gain | components R/C/V/D/MC/MR/MD |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `baseline` | `1` | `0.857` | `11.137` | `14.043` | `0.069` | `1.806` | `8.072` | `3.992` | `1.509` | `1.0/1.0/0.0/1.0/1.0/1.0/1.0` |
| `baseline` | `2` | `0.786` | `0.425` | `14.275` | `0.639` | `1.943` | `4.971` | `1.563` | `1.341` | `0.0/1.0/1.0/1.0/1.0/1.0/0.5` |
| `baseline` | `3` | `0.857` | `0.595` | `14.429` | `0.735` | `1.761` | `7.662` | `3.370` | `1.854` | `0.0/1.0/1.0/1.0/1.0/1.0/1.0` |
| `baseline` | `4` | `0.643` | `0.224` | `14.517` | `0.775` | `1.805` | `6.234` | `1.423` | `1.146` | `0.0/1.0/1.0/1.0/1.0/0.5/0.0` |
| `baseline` | `5` | `0.857` | `0.157` | `13.611` | `0.882` | `1.775` | `6.564` | `2.106` | `1.565` | `0.0/1.0/1.0/1.0/1.0/1.0/1.0` |
| `rep_zero` | `1` | `0.214` | `1.125` | `0.480` | `0.333` | `1.327` | `0.606` | `0.593` | `0.781` | `0.0/0.0/1.0/0.5/0.0/0.0/0.0` |
| `rep_zero` | `2` | `0.214` | `0.450` | `0.481` | `0.556` | `1.289` | `0.600` | `0.689` | `0.838` | `0.0/0.0/1.0/0.5/0.0/0.0/0.0` |
| `rep_zero` | `3` | `0.214` | `1.000` | `0.483` | `0.300` | `1.425` | `0.576` | `0.609` | `0.869` | `0.0/0.0/1.0/0.5/0.0/0.0/0.0` |
| `rep_zero` | `4` | `0.214` | `0.545` | `0.494` | `0.333` | `1.351` | `0.523` | `0.468` | `0.594` | `0.0/0.0/1.0/0.5/0.0/0.0/0.0` |
| `rep_zero` | `5` | `0.143` | `0.850` | `0.491` | `0.176` | `1.480` | `0.629` | `0.606` | `0.699` | `0.0/0.0/0.5/0.5/0.0/0.0/0.0` |
| `single_scale` | `1` | `0.857` | `11.137` | `14.562` | `0.063` | `1.931` | `8.286` | `3.991` | `1.509` | `1.0/1.0/0.0/1.0/1.0/1.0/1.0` |
| `single_scale` | `2` | `0.786` | `0.439` | `14.810` | `0.702` | `1.937` | `5.061` | `1.558` | `1.339` | `0.0/1.0/1.0/1.0/1.0/1.0/0.5` |
| `single_scale` | `3` | `0.857` | `0.545` | `14.976` | `0.706` | `1.764` | `7.832` | `3.378` | `1.857` | `0.0/1.0/1.0/1.0/1.0/1.0/1.0` |
| `single_scale` | `4` | `0.643` | `0.226` | `15.070` | `0.725` | `1.812` | `6.357` | `1.434` | `1.148` | `0.0/1.0/1.0/1.0/1.0/0.5/0.0` |
| `single_scale` | `5` | `0.857` | `0.156` | `14.096` | `0.923` | `1.773` | `6.698` | `2.110` | `1.566` | `0.0/1.0/1.0/1.0/1.0/1.0/1.0` |

## Condition Summary

| condition | n | score mean | score median | residence gain median | sample compactness median | voxel stability median | D_occ median | memory compactness median | memory roundness gain median | memory dimension gain median |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `baseline` | `5` | `0.800` | `0.857` | `0.425` | `14.275` | `0.735` | `1.805` | `6.564` | `2.106` | `1.509` |
| `rep_zero` | `5` | `0.200` | `0.214` | `0.850` | `0.483` | `0.333` | `1.351` | `0.600` | `0.606` | `0.781` |
| `single_scale` | `5` | `0.800` | `0.857` | `0.439` | `14.810` | `0.706` | `1.812` | `6.698` | `2.110` | `1.509` |

## Shape Summary

| condition | sample dim med | sample roundness med | sample radius med | memory dim med | memory roundness med | memory radius med |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `baseline` | `2.178` | `0.467` | `0.362` | `2.856` | `0.767` | `0.097` |
| `eta_zero` | `2.051` | `0.419` | `5.167` | `1.903` | `0.380` | `0.622` |
| `rep_zero` | `1.952` | `0.391` | `10.742` | `1.481` | `0.230` | `1.156` |
| `single_scale` | `2.183` | `0.469` | `0.349` | `2.863` | `0.772` | `0.095` |

## Reading

- High score means the condition separates from the no-feedback
  `eta_zero` control for that seed under the selected score version.
- The score is an evidence scorecard, not a proof of a specific
  two-scale knot mechanism.
- Baseline minus `single_scale` score difference has median `0`;
  therefore this score still does not isolate the baseline two-scale
  kernel as necessary.
- Memory-cloud shape is explicit in v0.5, and residence is compared in raw updates.
  The raw sample path remains a reported diagnostic rather than the knot-shape criterion.
