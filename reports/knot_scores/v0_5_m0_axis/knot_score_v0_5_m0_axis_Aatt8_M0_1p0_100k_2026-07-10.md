# Knot Score v0.5 Report

Date: 2026-07-10T10:58:55Z.

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
| `baseline` | `1` | `0.357` | `0.700` | `2.042` | `0.429` | `1.778` | `1.470` | `1.463` | `1.127` | `0.0/0.0/1.0/1.0/0.0/0.5/0.0` |
| `baseline` | `2` | `0.214` | `0.433` | `1.840` | `0.513` | `1.470` | `1.308` | `1.171` | `1.046` | `0.0/0.0/1.0/0.5/0.0/0.0/0.0` |
| `baseline` | `3` | `0.286` | `0.613` | `1.801` | `0.543` | `1.847` | `1.185` | `0.998` | `1.094` | `0.0/0.0/1.0/1.0/0.0/0.0/0.0` |
| `baseline` | `4` | `0.214` | `0.461` | `1.923` | `0.377` | `1.419` | `1.027` | `1.051` | `1.129` | `0.0/0.0/1.0/0.5/0.0/0.0/0.0` |
| `baseline` | `5` | `0.429` | `0.955` | `1.878` | `0.571` | `1.672` | `1.386` | `1.433` | `1.318` | `0.0/0.0/1.0/1.0/0.0/0.5/0.5` |

## Condition Summary

| condition | n | score mean | score median | residence gain median | sample compactness median | voxel stability median | D_occ median | memory compactness median | memory roundness gain median | memory dimension gain median |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `baseline` | `5` | `0.300` | `0.286` | `0.613` | `1.878` | `0.513` | `1.672` | `1.308` | `1.171` | `1.127` |

## Shape Summary

| condition | sample dim med | sample roundness med | sample radius med | memory dim med | memory roundness med | memory radius med |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `baseline` | `1.701` | `0.309` | `3.132` | `2.103` | `0.434` | `0.405` |
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
