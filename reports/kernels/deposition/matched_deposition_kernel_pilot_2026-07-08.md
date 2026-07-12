# Matched Deposition Kernel Pilot

Date: 2026-07-08.

## Question

The current canonical backend was a point-memory model:

```text
rho_n = sum_k w_k delta(. - x[n-k])
grad Phi(x_n) = sum_k w_k grad K(x_n - x[n-k])
```

The modelling question is whether the deposition kernel and the read/trajectory
kernel should be matched, up to the update-time offset. This is plausible, but
it has to be specified carefully.

## Implemented convention

The implemented conservative variant keeps the memory density non-negative and
normalizes each deposited Gaussian to unit mass. For a Gaussian read kernel

```text
K_L(r) = A exp(-r^2/(2 L^2))
```

and a normalized Gaussian deposition kernel of width `s`, the force can be
computed without a grid by using the effective convolution kernel

```text
L_eff = sqrt(L^2 + s^2)
A_eff = A (L/L_eff)^d.
```

The new `matched_gaussian` mode sets `s=L` for each Gaussian component. In the
baseline `d=3` two-scale case this yields

| parameter | raw | matched effective |
| --- | ---: | ---: |
| `sigma_rep` | `1.000` | `1.414` |
| `sigma_att` | `3.000` | `4.243` |
| `amplitude_rep` | `1.000` | `0.354` |
| `amplitude_att` | `0.350` | `0.124` |

This is not the same as an exact signed `G=K` for the two-scale kernel. Exact
signed deposition would require signed or multi-channel memory and cross terms
between the Gaussian components. That remains a separate model variant.

## Implementation

- `SimulationConfig.deposition_kernel` now accepts `delta`, `gaussian`, and
  `matched_gaussian`.
- `SimulationConfig.deposition_sigma` sets the finite width only for the generic
  `gaussian` mode.
- `experiments/current/dynamics/long_run_metastability.py` now has the condition
  `matched_deposition`, which maps to `deposition_kernel="matched_gaussian"`.
- Long-run JSON payloads include `effective_kernel` so raw and convolved
  parameters are not confused.
- The long-run script remains Numba-first, but can run small technical pilots
  with `--allow-slow-python` when Numba is unavailable.

## 100k Slow-Python Pilot

Source run: `data/processed/long_run_metastability/matched_deposition_100k_seed1-5_2026-07-08`.
Score report: `reports/knot_scores/v0_5_controls/knot_score_v0_5_matched_deposition_100k_2026-07-08.md`.

Parameters: `N=100,000`, seeds `1..5`, conditions `baseline`,
`matched_deposition`, `eta_zero`, `d=3`, `alpha=0.01`, `M0=1`,
`sample_every=100`, `burn_in=10,000`, `max_memory=600`.

The run recorded clean provenance: `git_revision=9bc15b8`, `git_status=""`.
It is a technical pilot, not a Long-N evidence run.

| condition | score median | sample radius median | memory radius median | memory roundness median | `D_occ` median |
| --- | ---: | ---: | ---: | ---: | ---: |
| `baseline` | `0.857` | `0.362` | `0.097` | `0.767` | `1.805` |
| `matched_deposition` | `0.714` | `1.535` | `0.244` | `0.668` | `1.679` |
| `eta_zero` | `n/a` | `5.167` | `0.622` | `0.380` | `n/a` |

## Reading

The matched normalized deposition condition remains much more confined than
`eta_zero`, but it is weaker and broader than the delta baseline in this 100k
pilot. Therefore the current result does not support the claim that simply
matching write/read Gaussian widths immediately produces stronger or more
"real" knots.

The result is also not a disproof of the matched-kernel idea. With normalized
Gaussian deposition and `s=L`, the local curvature scale drops as

```text
(A_eff / L_eff^2) / (A / L^2) = 2^(-(d/2 + 1)).
```

In `d=3` this is about `0.177`, i.e. a factor `5.657` weaker. A fair matched
kernel test should therefore either keep this normalized-mass convention and
accept weaker local stiffness, or add a curvature-renormalized condition with
`eta` or amplitudes multiplied by `2^(d/2+1)`.

## Next Decision

Do not claim that the earlier two-scale ambiguity was caused by kernel mismatch.
The immediate next scientific test should be a curvature-renormalized matched
condition, followed by the same seed-matched comparison against `baseline` and
`eta_zero`. Only after that should a 1M or 100M matched-deposition run be
started.
