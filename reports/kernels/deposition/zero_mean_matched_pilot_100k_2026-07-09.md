# Zero-Mean and Renormalized Matched-Deposition Pilot

Date: 2026-07-09.

## Scope

This is a short technical pilot, not a long-run evidence campaign. It tests two
new targeted conditions against baseline and `eta_zero`:

- `zero_mean_two_scale`: sets `A_att = A_rep (sigma_rep/sigma_att)^d`, so the
  unnormalized two-Gaussian kernel has `int K = 0`.
- `matched_deposition_renormalized`: uses `matched_gaussian` deposition and
  multiplies raw amplitudes by `2^(d/2+1)` to preserve local Gaussian stiffness.

## Run

Source: `data/processed/long_run_metastability/zero_mean_matched_100k_seed1-5_2026-07-09`.
Score report: `reports/knot_scores/v0_5_controls/knot_score_v0_5_zero_mean_matched_100k_2026-07-09.md`.

Parameters:

| field | value |
| --- | --- |
| `N` | `100,000` |
| seeds | `1..5` |
| conditions | `baseline`, `zero_mean_two_scale`, `matched_deposition_renormalized`, `eta_zero` |
| `d` | `3` |
| `alpha` | `0.01` |
| `sigma_rep` | `1.0` |
| `sigma_att` | `1.5` |
| baseline `A_att` | `0.35` |
| zero-mean `A_att` | `0.296296` |
| `sample_every` / `burn_in` | `100` / `10,000` |
| provenance | `git_revision=da6ff08`, `git_status=""` |

## Result

| condition | score median | sample radius median | memory radius median | memory roundness median | `D_occ` median |
| --- | ---: | ---: | ---: | ---: | ---: |
| `baseline` | `0.857` | `0.408` | `0.103` | `0.766` | `1.902` |
| `matched_deposition_renormalized` | `0.857` | `0.404` | `0.103` | `0.765` | `1.823` |
| `zero_mean_two_scale` | `0.857` | `0.397` | `0.102` | `0.764` | `1.816` |
| `eta_zero` | `n/a` | `5.167` | `0.622` | `0.380` | `n/a` |

The three active conditions are nearly indistinguishable at this short horizon
and scale ratio. All separate clearly from `eta_zero` by compactness and memory
shape, but none isolates a unique kernel mechanism.

## Reading

For `sigma_att/sigma_rep=1.5`, zero-mean changes `A_att` only from `0.35` to
`0.296296`. The fact that `zero_mean_two_scale` and the baseline are almost
identical is therefore not surprising. More importantly, the renormalized
matched-deposition condition also collapses back onto the baseline metrics.
This suggests the short-run knot geometry is dominated by the local curvature
scale of the effective kernel, while the global integral condition is not yet
being sampled strongly.

This does not falsify the zero-mean idea. It narrows the next test:

1. run a small scale-ratio sweep, especially `sigma_att/sigma_rep in {2, 3}`;
2. include `single_scale` and `A_rep=0` when moving beyond smoke pilots;
3. only scale to 1M/100M if the short pilots show a separation beyond numerical
   noise and seed variation.

Paper-I language remains unchanged: feedback confinement is supported, but a
specific two-scale or compensated-kernel mechanism is not yet isolated.
