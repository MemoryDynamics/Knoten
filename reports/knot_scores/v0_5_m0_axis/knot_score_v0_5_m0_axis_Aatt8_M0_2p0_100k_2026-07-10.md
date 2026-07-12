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
| `baseline` | `1` | `0.500` | `0.971` | `2.513` | `0.412` | `1.772` | `1.646` | `1.676` | `1.288` | `0.0/0.0/1.0/1.0/0.0/1.0/0.5` |
| `baseline` | `2` | `0.286` | `0.569` | `2.091` | `0.293` | `1.597` | `1.454` | `1.190` | `1.029` | `0.0/0.0/1.0/1.0/0.0/0.0/0.0` |
| `baseline` | `3` | `0.286` | `0.667` | `2.132` | `0.375` | `1.866` | `1.274` | `1.070` | `1.146` | `0.0/0.0/1.0/1.0/0.0/0.0/0.0` |
| `baseline` | `4` | `0.286` | `2.348` | `2.420` | `0.065` | `1.649` | `1.018` | `1.096` | `1.179` | `0.5/0.0/0.0/1.0/0.0/0.0/0.5` |
| `baseline` | `5` | `0.571` | `1.045` | `2.266` | `0.391` | `1.789` | `1.495` | `1.522` | `1.352` | `0.0/0.0/1.0/1.0/0.0/1.0/1.0` |

## Condition Summary

| condition | n | score mean | score median | residence gain median | sample compactness median | voxel stability median | D_occ median | memory compactness median | memory roundness gain median | memory dimension gain median |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `baseline` | `5` | `0.386` | `0.286` | `0.971` | `2.266` | `0.375` | `1.772` | `1.454` | `1.190` | `1.179` |

## Shape Summary

| condition | sample dim med | sample roundness med | sample radius med | memory dim med | memory roundness med | memory radius med |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `baseline` | `1.706` | `0.343` | `2.596` | `2.204` | `0.497` | `0.408` |
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
