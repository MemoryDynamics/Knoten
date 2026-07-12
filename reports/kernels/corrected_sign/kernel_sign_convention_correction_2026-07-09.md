# Kernel Sign-Convention Correction

Date: 2026-07-09.

## Decision

Correct the kernel gradient, not the amplitude labels and not the sign of
`eta`.

The model equation remains

```text
x[n+1] = x[n] + epsilon xi[n] - eta grad (K*rho[n])(x[n]), eta >= 0.
```

For a positive Gaussian potential term

```text
K(r) = A exp(-r^2/(2 sigma^2)), A > 0,
```

the true gradient is

```text
grad K(x-y) = - A exp(-|x-y|^2/(2 sigma^2)) (x-y)/sigma^2.
```

The previous package implementation returned the opposite vector for
`gaussian_gradient`. Therefore `A_rep` had acted as a local restoring drift
under `x <- x - eta grad`, and `A_att` had acted as a broad counter-channel.
This was internally reproducible but inconsistent with the paper equation and
with the labels `rep`/`att` as potential components.

## Correction

The corrected package convention is:

- `gaussian_gradient` returns the true gradient of a positive Gaussian
  potential and points toward the memory point.
- `double_gaussian_gradient` returns the gradient of
  `A_rep G_rep - A_att G_att`.
- The canonical update still subtracts `eta * grad`.
- `repulsive_gaussian_gradient` remains an explicit outward-vector helper for
  ballistic/self-repulsion probes; it is not `grad K` itself.

Consequences:

- `A_rep` is now a local repulsive potential channel.
- `A_att` is now a broad attractive potential channel.
- `single_scale` (`A_att=0`) is repulsion-only and should be dispersive.
- `rep_zero` (`A_rep=0`) is attraction-only and can confine/collapse depending
  on noise, memory, and amplitude.

## Status of Previous Reports

Reports produced before this correction are still useful for auditing the old
implementation, but they are `legacy-sign` evidence. They must not be cited as
numerical evidence for the corrected potential model without being rerun.

Affected especially:

- previous `baseline`/`single_scale` confinement reports;
- Zero-Mean and matched-deposition pilots;
- the q=3 force-component pilot that identified the sign issue.

## Retest Plan

1. Run short corrected-sign controls:
   `baseline`, `single_scale`, `rep_zero`, `eta_zero` at q=3.
2. Add force-component summaries to verify the direction of each channel.
3. Sweep attraction amplitudes over orders of magnitude at fixed repulsive core,
   for example `A_att in {0.35, 3.5, 9, 35, 350}` with `A_rep=1`,
   `sigma_rep=1`, `sigma_att=3`.
4. Only if a compact corrected-sign regime appears, run Score/Residence and
   then Block-Markov/AR mode tests.
5. If no compact scalar-memory regime appears, move earlier toward vector-valued
   memory or additional internal state before claiming knots.
