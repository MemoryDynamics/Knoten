# Knot Score v0.5 Report

Date: 2026-07-10T12:02:11Z.

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
| `baseline` | `1` | `0.857` | `0.990` | `42.852` | `0.830` | `2.018` | `11.939` | `5.116` | `2.054` | `0.0/1.0/1.0/1.0/1.0/1.0/1.0` |
| `baseline` | `2` | `0.857` | `0.779` | `42.580` | `0.689` | `1.945` | `14.881` | `2.026` | `1.508` | `0.0/1.0/1.0/1.0/1.0/1.0/1.0` |
| `baseline` | `3` | `0.857` | `1.040` | `42.745` | `0.435` | `2.023` | `8.674` | `2.347` | `1.590` | `0.0/1.0/1.0/1.0/1.0/1.0/1.0` |
| `baseline` | `4` | `0.857` | `1.820` | `42.933` | `0.468` | `1.889` | `8.038` | `2.217` | `1.730` | `0.0/1.0/1.0/1.0/1.0/1.0/1.0` |
| `baseline` | `5` | `0.929` | `4.732` | `42.768` | `0.155` | `1.929` | `7.840` | `3.376` | `2.027` | `1.0/1.0/0.5/1.0/1.0/1.0/1.0` |

## Condition Summary

| condition | n | score mean | score median | residence gain median | sample compactness median | voxel stability median | D_occ median | memory compactness median | memory roundness gain median | memory dimension gain median |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `baseline` | `5` | `0.871` | `0.857` | `1.040` | `42.768` | `0.468` | `1.945` | `8.674` | `2.347` | `1.730` |

## Shape Summary

| condition | sample dim med | sample roundness med | sample radius med | memory dim med | memory roundness med | memory radius med |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `baseline` | `2.041` | `0.336` | `0.376` | `2.868` | `0.772` | `0.060` |
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
