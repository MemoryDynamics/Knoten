# Ballistic Kernel Probe Report

Date: 2026-07-07.

## Goal

This probe checks whether the scalar finite-memory model can produce a
photon-like ballistic mode in the simplest dimensionless setting. It is a
technical diagnostic, not a physical photon simulation.

The tested update is

```text
x[n+1] = x[n] + eta * grad_repulsive_memory(x[n]) + epsilon * xi[n]
```

where `grad_repulsive_memory` points away from the weighted memory cloud. This
uses the opposite drift sign from the current overdamped confinement model,
because the canonical `x <- x - eta * gradient` convention is locally
restoring for the current Gaussian-gradient implementation.

## Protocol

The corrected sweep uses:

- `d = 1`
- `A = L = beta = 1`
- `lambda in {0.05, 0.10, 0.20}` as the actual exponential memory rate
- `r = gamma/gamma_c(lambda) in {0.90, 0.95, 0.98, 1.00, 1.02, 1.05, 1.10}`
- `delta = epsilon/L in {0, 1e-4, 1e-3, 1e-2}`
- `steps = 4000`, `burn_in = 100`, `sample_every = 5`

The critical reference is

```text
gamma_c(lambda) = lambda^2 / (1 - lambda)
```

and the measured diagnostic is the log-log slope of the mean-squared
displacement over lags 5..40. Ballistic motion would require a stable slope
near 2 over a nontrivial window.

## Result

The corrected scalar one-kernel sweep does not show a robust ballistic regime.

| delta | finite cases | median MSD slope | max MSD slope | reading |
| ---: | ---: | ---: | ---: | --- |
| `0` | `21` | `0.043` | `0.109` | deterministic seeded motion relaxes or stalls |
| `1e-4` | `21` | `1.130` | `1.138` | noise-driven, not ballistic |
| `1e-3` | `21` | `1.130` | `1.138` | noise-driven, not ballistic |
| `1e-2` | `21` | `1.130` | `1.138` | noise-driven, not ballistic |

The largest observed slope is about `1.138`, far below the ballistic target
`2`. The scalar memory model therefore does not currently support the photon
analogy in this minimal one-dimensional one-kernel test.

## Interpretation

This supports the concern that scalar overdamped memory alone is too weak a
structure for a harmonic oscillator or photon-like mode. A photon programme
would likely need at least one additional structural ingredient: an inertial or
second-order state, a phase/vector memory component, a transverse/polarization
observable, or a coupled two-field construction. Physical constants such as
`hbar nu` and `m c^2` can guide scale estimates only after a dimensionless
ballistic or oscillatory regime exists.

## Next Steps

1. Keep this as a negative control for scalar one-kernel photon analogies.
2. Do not tune physical constants against this model until a dimensionless
   oscillatory or ballistic observable has been demonstrated.
3. If the photon track continues, test a minimal extended state with velocity
   or phase memory before returning to two-scale kernels.