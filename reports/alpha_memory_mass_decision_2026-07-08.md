# Alpha, Memory Mass, and Ballistic Threshold Decision

Date: 2026-07-08.

## Decision

The general memory update used by the mathematical anchor is

```text
rho[n+1](x) = (1-lambda_m) rho[n](x) + beta G_sigma(x - x[n+1]).
```

For normalized `G_sigma`, the stationary memory mass is

```text
M0 = beta / lambda_m.
```

The clean working parametrization is therefore

```text
beta = lambda_m M0,
rho[n+1] = (1-lambda_m) rho[n] + lambda_m M0 G_sigma.
```

The previous package convention `beta=lambda_m=alpha` is retained as the
normalized special case `M0=1`. Existing reports should be read in that
convention unless they explicitly record a different `beta/alpha` or
`memory_mass`.

## Consequence for alpha scans

Raw alpha sweeps are confounded unless they control all three effects:

1. memory lifetime: `tau_mem ~ 1/lambda_m`;
2. finite-memory truncation: stored tail mass depends on `lambda_m` and horizon;
3. field mass/coupling: `M0=beta/lambda_m` changes the effective force scale.

So yes, alpha should be treated with the same discipline as the `eta=0`
control, but not as another blind one-parameter long-run sweep. The controlled
axes are:

- vary `lambda_m` at fixed `M0` and fixed tail-mass cutoff;
- vary `M0=beta/lambda_m` at fixed `lambda_m`;
- report an effective coupling such as `eta M0 a0` or the threshold ratio
  `eta/eta_c` where appropriate.

## Corrected ballistic threshold

For the effective one-kernel test with local curvature

```text
a0 = -w''(0) > 0,
```

the local ballistic threshold is

```text
eta_c = lambda_m / ((1-lambda_m) M0 a0).
```

The dimensionless self-consistency parameter remains

```text
gamma = eta lambda_m M0 a0,
gamma_c = lambda_m^2 / (1-lambda_m).
```

Thus `eta_c` and `gamma_c` are not the same number. For
`lambda_m=0.1`, `M0=1`, `a0=1`:

```text
gamma_c = 0.011111...
eta_c   = 0.111111...
```

The propagation-speed probe has been corrected to sweep `r=eta/eta_c`, while
checking the analytic residual with `gamma=eta lambda_m M0 a0`.

## Minimal scalar memory modes

The local two-variable scalar memory reduction

```text
x[n+1] = (1-g)x[n] + g m[n]
m[n+1] = (1-lambda_m)m[n] + lambda_m x[n+1]
```

has eigenvalues

```text
mu_1 = 1,
mu_2 = (1-lambda_m)(1-g).
```

The nontrivial mode is real. This supports the current guardrail: a photon-like
or harmonic mode is not automatic in the scalar overdamped memory model. It
must either emerge from richer field/multi-knot coarse graining or require an
extended memory channel such as velocity, phase, or vector memory.

## Code changes

- `SimulationConfig.memory_mass` was added with default `1.0`.
- `exponential_memory_weights(lambda_value, horizon, memory_mass=M0)` implements
  `lambda_m M0 (1-lambda_m)^k`.
- `exponential_weights(alpha, horizon)` remains a backward-compatible wrapper
  for `M0=1`.
- `analytic.py` now contains `critical_eta`, stationary mass helpers, scalar
  local modes, frozen Hessian stability labels, and two-scale force-crossing
  radius.
- `ballistic_kernel_probe.py` now sweeps `eta/eta_c` and records `eta_c`,
  `gamma`, and `gamma_c` separately.

## Next step

The next scientific step is not direct photon simulation. It is a cheap
coarse-graining reanalysis of existing long-run data:

1. build block states from memory-center, velocity, memory mass, radius,
   Hessian/shape proxies, and anisotropy;
2. fit `Y[m+1]-barY = A_B (Y[m]-barY) + noise` for block sizes around
   `1/lambda_m`, `2/lambda_m`, `5/lambda_m`, and `10/lambda_m`;
3. inspect whether slow eigenvalues are real, negative, or complex;
4. only if complex modes are stable across block size should the photon/wave
   track be reopened inside this model family.
