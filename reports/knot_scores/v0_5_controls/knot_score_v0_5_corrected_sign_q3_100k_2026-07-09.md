# Knot Score v0.5 Report

Date: 2026-07-09T18:40:38Z.

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
| `baseline` | `1` | `0.071` | `0` | `0.078` | `n/a` | `1.274` | `0.184` | `0.318` | `0.870` | `0.0/0.0/0.0/0.5/0.0/0.0/0.0` |
| `baseline` | `2` | `0.071` | `0` | `0.078` | `n/a` | `1.334` | `0.090` | `0.185` | `0.647` | `0.0/0.0/0.0/0.5/0.0/0.0/0.0` |
| `baseline` | `3` | `0` | `0` | `0.076` | `n/a` | `1.236` | `0.134` | `0.291` | `0.954` | `0.0/0.0/0.0/0.0/0.0/0.0/0.0` |
| `baseline` | `4` | `0.071` | `0` | `0.110` | `n/a` | `1.387` | `0.102` | `0.125` | `0.458` | `0.0/0.0/0.0/0.5/0.0/0.0/0.0` |
| `baseline` | `5` | `0.143` | `0` | `0.063` | `n/a` | `1.632` | `0.109` | `0.197` | `0.631` | `0.0/0.0/0.0/1.0/0.0/0.0/0.0` |
| `rep_zero` | `1` | `0.357` | `1.250` | `1.552` | `0.500` | `1.581` | `1.408` | `1.386` | `1.106` | `0.0/0.0/1.0/1.0/0.0/0.5/0.0` |
| `rep_zero` | `2` | `0.214` | `1.700` | `1.553` | `0.118` | `1.490` | `1.378` | `1.257` | `1.175` | `0.0/0.0/0.0/0.5/0.0/0.5/0.5` |
| `rep_zero` | `3` | `0.429` | `0.933` | `1.552` | `0.429` | `1.691` | `1.424` | `1.391` | `1.165` | `0.0/0.0/1.0/1.0/0.0/0.5/0.5` |
| `rep_zero` | `4` | `0.357` | `0.545` | `1.551` | `0.333` | `1.604` | `1.485` | `1.282` | `1.103` | `0.0/0.0/1.0/1.0/0.0/0.5/0.0` |
| `rep_zero` | `5` | `0.429` | `0.750` | `1.545` | `0.289` | `1.707` | `1.397` | `1.330` | `1.278` | `0.0/0.0/1.0/1.0/0.0/0.5/0.5` |
| `single_scale` | `1` | `0` | `0` | `0.052` | `n/a` | `1.127` | `0.145` | `0.398` | `0.730` | `0.0/0.0/0.0/0.0/0.0/0.0/0.0` |
| `single_scale` | `2` | `0` | `0` | `0.061` | `n/a` | `1.069` | `0.074` | `0.149` | `0.572` | `0.0/0.0/0.0/0.0/0.0/0.0/0.0` |
| `single_scale` | `3` | `0` | `0` | `0.059` | `n/a` | `1.187` | `0.114` | `0.226` | `0.855` | `0.0/0.0/0.0/0.0/0.0/0.0/0.0` |
| `single_scale` | `4` | `0` | `0` | `0.055` | `n/a` | `1.195` | `0.088` | `0.121` | `0.430` | `0.0/0.0/0.0/0.0/0.0/0.0/0.0` |
| `single_scale` | `5` | `0.071` | `0` | `0.043` | `n/a` | `1.455` | `0.095` | `0.160` | `0.627` | `0.0/0.0/0.0/0.5/0.0/0.0/0.0` |

## Condition Summary

| condition | n | score mean | score median | residence gain median | sample compactness median | voxel stability median | D_occ median | memory compactness median | memory roundness gain median | memory dimension gain median |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `baseline` | `5` | `0.071` | `0.071` | `0` | `0.078` | `n/a` | `1.334` | `0.109` | `0.197` | `0.647` |
| `rep_zero` | `5` | `0.357` | `0.357` | `0.933` | `1.552` | `0.333` | `1.604` | `1.408` | `1.330` | `1.165` |
| `single_scale` | `5` | `0.014` | `0` | `0` | `0.055` | `n/a` | `1.187` | `0.095` | `0.160` | `0.627` |

## Shape Summary

| condition | sample dim med | sample roundness med | sample radius med | memory dim med | memory roundness med | memory radius med |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `baseline` | `1.807` | `0.339` | `58.731` | `1.325` | `0.067` | `5.724` |
| `eta_zero` | `2.051` | `0.419` | `5.167` | `1.903` | `0.380` | `0.622` |
| `rep_zero` | `2.068` | `0.424` | `3.327` | `2.375` | `0.505` | `0.445` |
| `single_scale` | `1.624` | `0.320` | `84.460` | `1.188` | `0.065` | `6.534` |

## Reading

- High score means the condition separates from the no-feedback
  `eta_zero` control for that seed under the selected score version.
- The score is an evidence scorecard, not a proof of a specific
  two-scale knot mechanism.
- Baseline minus `single_scale` score difference has median `0.071`;
  therefore this score still does not isolate the baseline two-scale
  kernel as necessary.
- Memory-cloud shape is explicit in v0.5, and residence is compared in raw updates.
  The raw sample path remains a reported diagnostic rather than the knot-shape criterion.
