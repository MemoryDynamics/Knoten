# Zero-Mean Two-Scale Kernel Decision

Date: 2026-07-09.

## Motivation

A cleaner two-scale kernel normalization is to require the total kernel integral
to vanish:

```text
int K(x) dx = 0.
```

For the current unnormalized double-Gaussian convention

```text
K(r) = A_rep exp(-r^2/(2 L_rep^2))
     - A_att exp(-r^2/(2 L_att^2)),
```

on `R^d`, this gives

```text
A_rep L_rep^d = A_att L_att^d,
A_att = A_rep (L_rep/L_att)^d.
```

This is a compensated or Mexican-hat-style kernel: local structure without a
net DC offset from the total memory mass.

## Immediate consequence

The historical baseline `L_rep=1`, `L_att=3`, `A_rep=1`, `A_att=0.35` is not
zero-mean. In `d=3`, zero-mean would require

```text
A_att = 1/27 = 0.037037.
```

That is much weaker than the previous broad component. Therefore the old
baseline was not a compensated two-scale kernel.

A more discriminating first test is a closer scale ratio, for example
`L_att/L_rep=1.5`, where zero-mean gives

```text
A_att = 1/1.5^3 = 0.296296.
```

This keeps the attractive/broad component close to the historically used
amplitude while enforcing `int K=0`.

## Implementation decision

The condition `zero_mean_two_scale` now sets

```text
amplitude_att = amplitude_rep * (sigma_rep/sigma_att)^dim
```

for the current run configuration. This makes the condition reusable for
`--sigma-att 1.25`, `1.5`, `2.0`, or `3.0` without adding another parameter.

The condition is intentionally separate from deposition matching. The write
kernel remains the selected deposition mode (`delta` by default). A signed
`G=K` deposition would be a different, sign-changing or multi-channel memory
model and is not part of this condition.

## Priority

Run a short seed-matched pilot before any long run:

```powershell
python experiments/long_run_metastability.py `
  --steps 100000 `
  --seeds 1,2,3,4,5 `
  --conditions baseline,zero_mean_two_scale,matched_deposition_renormalized,eta_zero `
  --dim 3 `
  --alpha 0.01 `
  --sigma-rep 1.0 `
  --sigma-att 1.5 `
  --amplitude-rep 1.0 `
  --amplitude-att 0.35 `
  --sample-every 100 `
  --burn-in 10000 `
  --max-memory 600 `
  --allow-slow-python `
  --output-dir data/processed/long_run_metastability/zero_mean_matched_100k_seed1-5_2026-07-09
```

Interpretation guardrail: a positive result supports a compensated-kernel
hypothesis, not a proof of a unique knot mechanism. It must still separate from
`eta_zero`, from `single_scale`, and from matched-deposition controls over
longer runs.


## Pilot result

The first 100k seed-matched pilot at `sigma_att/sigma_rep=1.5` is reported in
`reports/zero_mean_matched_pilot_100k_2026-07-09.md`. Result: `baseline`,
`zero_mean_two_scale`, and `matched_deposition_renormalized` are nearly
indistinguishable at this horizon, while all active conditions remain compact
relative to `eta_zero`. This suggests the short-run geometry is dominated by
local effective curvature rather than the global zero-integral constraint.
