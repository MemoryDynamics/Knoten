# Knot Score v0.5 Report

Date: 2026-07-10T10:58:56Z.

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
| `baseline` | `1` | `0.286` | `1.800` | `1.710` | `0.222` | `1.809` | `1.311` | `1.272` | `1.040` | `0.0/0.0/0.5/1.0/0.0/0.5/0.0` |
| `baseline` | `2` | `0.143` | `1.333` | `1.599` | `0.125` | `1.654` | `1.196` | `1.130` | `1.047` | `0.0/0.0/0.0/1.0/0.0/0.0/0.0` |
| `baseline` | `3` | `0.286` | `0.771` | `1.532` | `0.541` | `1.765` | `1.107` | `0.971` | `1.041` | `0.0/0.0/1.0/1.0/0.0/0.0/0.0` |
| `baseline` | `4` | `0.143` | `0.913` | `1.579` | `0.190` | `1.492` | `1.034` | `1.037` | `1.072` | `0.0/0.0/0.5/0.5/0.0/0.0/0.0` |
| `baseline` | `5` | `0.429` | `1.227` | `1.593` | `0.556` | `1.684` | `1.276` | `1.315` | `1.246` | `0.0/0.0/1.0/1.0/0.0/0.5/0.5` |

## Condition Summary

| condition | n | score mean | score median | residence gain median | sample compactness median | voxel stability median | D_occ median | memory compactness median | memory roundness gain median | memory dimension gain median |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `baseline` | `5` | `0.257` | `0.286` | `1.227` | `1.593` | `0.222` | `1.684` | `1.196` | `1.130` | `1.047` |

## Shape Summary

| condition | sample dim med | sample roundness med | sample radius med | memory dim med | memory roundness med | memory radius med |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `baseline` | `1.714` | `0.320` | `3.632` | `2.001` | `0.403` | `0.439` |
| `eta_zero` | `1.441` | `0.247` | `5.806` | `1.923` | `0.415` | `0.560` |

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
