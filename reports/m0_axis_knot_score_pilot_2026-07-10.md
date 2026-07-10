# M0 Axis KnotScore Pilot

Date: 2026-07-10.

## Scope

This pilot applies the Pareto rule from the KPI register: vary one parameter
axis, score it with the current scorecard, and decide whether it deserves a
larger long-run campaign.

Axis: `M0 in {0.5, 1.0, 2.0}`.

Fixed parameters: `N=100,000`, seeds `1..5`, `d=3`, `alpha=lambda_m=0.01`,
`epsilon=0.03`, `eta=0.15`, `sigma_rep=1`, `sigma_att=3`, `A_rep=1`,
`A_att=8`, `memory_factor=6`, `max_memory=600`, `burn_in=5,000`,
`sample_every=100`, deposition `delta`.

Each `M0` value is scored seedwise against a matched `eta_zero` control with
the same `M0`. The score version is KnotScore `v0.5`.

This is a short pilot near the corrected-sign attraction transition, not a
long-run metastability claim.

## Median Summary

| M0 | score med | residence gain med | sample compactness med | voxel stability med | D_occ med | memory compactness med | memory roundness gain med | memory dimension gain med | sample radius med | memory radius med | memory dim med |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `0.5` | `0.286` | `1.227` | `1.593` | `0.222` | `1.684` | `1.196` | `1.130` | `1.047` | `3.632` | `0.439` | `2.001` |
| `1.0` | `0.286` | `0.613` | `1.878` | `0.513` | `1.672` | `1.308` | `1.171` | `1.127` | `3.132` | `0.405` | `2.103` |
| `2.0` | `0.286` | `0.971` | `2.266` | `0.375` | `1.772` | `1.454` | `1.190` | `1.179` | `2.596` | `0.408` | `2.204` |

Score means were `0.257`, `0.300`, and `0.386` for `M0=0.5`, `1.0`, and
`2.0`, respectively. The higher mean at `M0=2.0` is driven by seed-level
shape and memory-dimension components, not by a robust residence pass.

## Reading

Increasing `M0` at fixed `A_att=8` makes the active trajectories more compact:
the median sample radius drops from `3.632` to `2.596`, and memory-shape
dimension increases from `2.001` to `2.204`.

The short pilot does not produce a strong v0.5 KnotScore. Median score remains
`0.286` for all three `M0` values because the pass-level components are not
simultaneously satisfied:

- median residence gain stays below the `>=2` partial threshold;
- median sample compactness stays below the `>=3` partial threshold;
- memory compactness improves but stays below the `>=2` partial threshold.

So `M0` is a real scale/coupling lever, but this pilot does not justify a broad
M0-only long-run sweep. It is better used as a controlled secondary axis once
the primary compact-candidate window has been selected.

## Decision

Do not expand this into a blind M0 scan yet.

Next scalar step: keep the corrected-sign candidate window and harden a small
set of amplitude candidates with KnotScore v0.5, using longer runs only where
the short pilot already separates from `eta_zero` on residence and compactness.

Next model step: continue vector-memory work only with controls that separate
mode signals from the already observed random-walk/feature-induced complex AR
pairs.

## Source Reports

- `reports/knot_score_v0_5_m0_axis_Aatt8_M0_0p5_100k_2026-07-10.md`
- `reports/knot_score_v0_5_m0_axis_Aatt8_M0_1p0_100k_2026-07-10.md`
- `reports/knot_score_v0_5_m0_axis_Aatt8_M0_2p0_100k_2026-07-10.md`
