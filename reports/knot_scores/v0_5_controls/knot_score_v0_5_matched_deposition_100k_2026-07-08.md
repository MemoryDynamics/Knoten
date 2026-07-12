# Knot Score v0.5 Report

Date: 2026-07-08T19:19:16Z.

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
| `matched_deposition` | `1` | `0.643` | `1.559` | `3.345` | `0.608` | `1.729` | `2.609` | `2.156` | `1.207` | `0.0/0.5/1.0/1.0/0.5/1.0/0.5` |
| `matched_deposition` | `2` | `0.714` | `0.914` | `3.366` | `0.301` | `1.640` | `2.352` | `1.668` | `1.377` | `0.0/0.5/1.0/1.0/0.5/1.0/1.0` |
| `matched_deposition` | `3` | `0.714` | `1.130` | `3.353` | `0.442` | `1.646` | `2.704` | `2.363` | `1.538` | `0.0/0.5/1.0/1.0/0.5/1.0/1.0` |
| `matched_deposition` | `4` | `0.500` | `0.382` | `3.353` | `0.536` | `1.679` | `2.694` | `1.241` | `1.074` | `0.0/0.5/1.0/1.0/0.5/0.5/0.0` |
| `matched_deposition` | `5` | `0.714` | `0.439` | `3.304` | `0.418` | `1.731` | `2.551` | `1.890` | `1.513` | `0.0/0.5/1.0/1.0/0.5/1.0/1.0` |

## Condition Summary

| condition | n | score mean | score median | residence gain median | sample compactness median | voxel stability median | D_occ median | memory compactness median | memory roundness gain median | memory dimension gain median |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `baseline` | `5` | `0.800` | `0.857` | `0.425` | `14.275` | `0.735` | `1.805` | `6.564` | `2.106` | `1.509` |
| `matched_deposition` | `5` | `0.657` | `0.714` | `0.914` | `3.353` | `0.442` | `1.679` | `2.609` | `1.890` | `1.377` |

## Shape Summary

| condition | sample dim med | sample roundness med | sample radius med | memory dim med | memory roundness med | memory radius med |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `baseline` | `2.178` | `0.467` | `0.362` | `2.856` | `0.767` | `0.097` |
| `eta_zero` | `2.051` | `0.419` | `5.167` | `1.903` | `0.380` | `0.622` |
| `matched_deposition` | `2.090` | `0.430` | `1.535` | `2.678` | `0.668` | `0.244` |

## Reading

- High score means the condition separates from the no-feedback
  `eta_zero` control for that seed under the selected score version.
- The score is an evidence scorecard, not a proof of a specific
  two-scale knot mechanism.
- Baseline minus `single_scale` score difference has median `n/a`;
  therefore this score still does not isolate the baseline two-scale
  kernel as necessary.
- Memory-cloud shape is explicit in v0.5, and residence is compared in raw updates.
  The raw sample path remains a reported diagnostic rather than the knot-shape criterion.
