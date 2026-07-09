# Corrected-Sign Attraction-Amplitude Hierarchy

Date: 2026-07-09.

## Scope

This pilot tests whether the corrected two-scale potential can move from
repulsion-dominated dispersion to attraction-dominated confinement by increasing
only the broad attractive amplitude. It keeps the repulsive core fixed.

Fixed parameters: `N=100,000`, seeds `1..5`, `d=3`, `alpha=0.01`, `M0=1`,
`sigma_rep=1`, `sigma_att=3`, `A_rep=1`, `epsilon=0.03`, `eta=0.15`,
`sample_every=100`, `burn_in=10,000`, `max_memory=600`, condition `baseline`,
with force-component diagnostics.

`A_att=0.35` is reused from
`data/processed/long_run_metastability/corrected_sign_q3_100k_seed1-5_2026-07-09`.
The additional amplitude directories are
`data/processed/long_run_metastability/amplitude_hierarchy_q3_Aatt_*_100k_seed1-5_2026-07-09`.

The score is computed seedwise against the existing corrected-sign `eta_zero`
control from the q=3 pilot. This aggregation is custom because the raw case
condition remains `baseline` for every amplitude.

## Median Summary

| A_att | score med | candidate seeds | best residence med | sample radius med | memory radius med | memory dim med | memory roundness med | rep/att med | net cos med |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `0.35` | `0.071` | `0/5` | `0` | `58.731` | `5.724` | `1.325` | `0.067` | `5.536` | `-0.921` |
| `1` | `0.286` | `0/5` | `1.5` | `21.996` | `2.472` | `1.617` | `0.193` | `2.222` | `-0.684` |
| `2` | `0.286` | `0/5` | `2` | `7.087` | `1.613` | `1.943` | `0.327` | `1.471` | `-0.558` |
| `3.5` | `0.286` | `0/5` | `3` | `4.782` | `1.154` | `2.134` | `0.400` | `1.210` | `-0.532` |
| `9` | `0.500` | `3/5` | `11.579` | `2.313` | `0.330` | `2.618` | `0.639` | `0.933` | `0.975` |
| `35` | `0.857` | `2/5` | `5.667` | `0.132` | `0.059` | `2.913` | `0.805` | `0.256` | `0.659` |
| `350` | `0.500` | `0/5` | `1` | `2.724` | `2.781` | `2.958` | `0.865` | `0.00082` | `-0.999` |

Cosines use the same convention as the q=3 report: positive values move toward
the weighted memory center, negative values move away.

## Reading

The amplitude scan is not random parameter fishing; it tests the force-balance
prediction created by the sign correction.

Findings:

- The historical `A_att=0.35` baseline is repulsion dominated and dispersive.
- Increasing `A_att` monotonically reduces sample and memory radii up to the
  compact band around `A_att=9..35`.
- The net drift flips from outward to inward between `A_att=3.5` and `A_att=9`.
- `A_att=35` gives the tightest and roundest memory cloud in this short pilot,
  but residence is still modest; this is a compact candidate, not a proven
  metastable knot.
- `A_att=350` is overdriven. The attractive channel dominates so strongly that
  the sampled dynamics no longer improves the score or residence; the negative
  net cosine is consistent with overshoot/instability rather than a clean knot.

## Consequence

The corrected scalar model can produce compact memory clouds, but only after the
broad attractive amplitude is raised by one to two orders of magnitude relative
to the historical baseline. The useful next window is not arbitrary: it is the
transition region `A_att in [6, 40]`, especially around `9` and `35`.

Do not run mode tests on the old q=3 baseline. The next AR/Transfer-operator
mode test should use corrected-sign compact candidates, initially `A_att=9` and
`A_att=35`, and should report whether the slow modes are real, negative, or a
complex conjugate pair. If all slow scalar-memory modes remain real, the vector
memory track remains the likely next model extension.
