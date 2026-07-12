# Knot Score v0.5 Report

Date: 2026-07-10T12:02:06Z.

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
| `baseline` | `1` | `0.643` | `1.462` | `2.512` | `0.263` | `1.722` | `2.117` | `1.963` | `1.393` | `0.0/0.0/1.0/1.0/0.5/1.0/1.0` |
| `baseline` | `2` | `0.643` | `0.667` | `2.456` | `0.474` | `1.752` | `2.618` | `1.775` | `1.446` | `0.0/0.0/1.0/1.0/0.5/1.0/1.0` |
| `baseline` | `3` | `0.500` | `1.450` | `2.523` | `0.345` | `1.804` | `1.485` | `1.550` | `1.306` | `0.0/0.0/1.0/1.0/0.0/1.0/0.5` |
| `baseline` | `4` | `0.429` | `1.692` | `2.684` | `0.227` | `1.758` | `1.701` | `1.511` | `1.286` | `0.0/0.0/0.5/1.0/0.0/1.0/0.5` |
| `baseline` | `5` | `0.500` | `0.895` | `2.445` | `0.353` | `1.739` | `1.495` | `1.739` | `1.331` | `0.0/0.0/1.0/1.0/0.0/1.0/0.5` |

## Condition Summary

| condition | n | score mean | score median | residence gain median | sample compactness median | voxel stability median | D_occ median | memory compactness median | memory roundness gain median | memory dimension gain median |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `baseline` | `5` | `0.543` | `0.500` | `1.450` | `2.512` | `0.345` | `1.752` | `1.701` | `1.739` | `1.331` |

## Shape Summary

| condition | sample dim med | sample roundness med | sample radius med | memory dim med | memory roundness med | memory radius med |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `baseline` | `1.987` | `0.325` | `6.409` | `2.107` | `0.500` | `0.329` |
| `eta_zero` | `2.001` | `0.318` | `16.098` | `1.639` | `0.331` | `0.508` |

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
