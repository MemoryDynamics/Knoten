# P3.2 Long-Horizon Hankel Preregistration

Date: 2026-08-04.
Status: preregistered before the canonical run.

## Question

The short measurement-closure ladder shows a small increase in held-out
RMSE relative to persistence as delay depth grows. That curve is confounded:
deeper full-OLS models receive more regressors and fewer training targets.
The follow-up asks whether the trend survives fixed train/test target times and
fixed reduced ranks beyond a 10000-update history horizon.

## Frozen dynamics

The P3.2 checkpoint, kernel, `lambda=0.01`, `epsilon=1e-4`, reciprocal gain,
distance, Telegraph mediator, grid, and 50-update closure cadence remain
unchanged. No gain, lambda, epsilon, kernel, or ridge parameter is fitted.

- formation checkpoint: scalar `d=3`, seed 1, `N=100000000`;
- future-noise seeds: `1,2,3`;
- noise correlations: `rho={0,0.9,0.99}` with fixed node marginals;
- updates: `150000` after checkpoint continuation;
- analysis burn-in: 100 memory times = 10000 updates;
- arms: retarded reciprocal and retarded one-way control;
- observables: visible `(x_-,m_-)` and field/momentum-augmented state.

## Registered measurement

At 50-update cadence, delay depths

```text
{20, 50, 100, 150, 200, 250}
```

represent history horizons

```text
{1000, 2500, 5000, 7500, 10000, 12500} updates.
```

Every depth uses the same response-target indices. With 2801 post-burn
samples and a chronological 60/40 split, all models use response targets
250..1680 for training and 1681..2800 for holdout. Ambient coordinates remain
fixed-effect panels.

The truncated Hankel ranks are fixed at

```text
{2, 4, 8, 16, 32}.
```

For each depth the report stores singular values, stable rank, entropy rank,
numerical ranks at relative thresholds `1e-6` and `1e-8`, retained-rank
conditioning, held-out RMSE/persistence, and reduced DMD eigenvalues.

## Primary decision

For every seed, rho, and fixed rank, define

```text
Delta = ratio(depth=250) - ratio(depth=20),
ratio = held-out RMSE / persistence RMSE.
```

Classification is:

- longer history degrades prediction if median `Delta >= 0.02` and at least
  80% of path/rank deltas are positive;
- longer history improves prediction if median `Delta <= -0.02` and at least
  80% are negative;
- otherwise no rank-robust material long-history trend.

The one-way arm is a mechanistic control and the augmented state is reported
separately. A ratio below one only beats one-step persistence at this cadence;
it is not a Markov theorem.

## Claim boundary

This run decides prediction trend and numerical rank only. Reduced DMD poles
are persisted for audit but cannot establish an oscillatory mode. A pole would
still need identity across fixed ranks, delay depths, non-overlapping time
segments, and separation from the one-way control. No spin, particle, photon,
`d=3`, Lorentz, QFT, or Standard-Model claim follows.

## Planned outputs

- `reports/response/long_horizon_hankel_gate_2026-08-04.md`;
- `reports/response/long_horizon_hankel_gate_2026-08-04.json`;
- `figures/draft/response/long_horizon_hankel_gate_2026-08-04.png`.