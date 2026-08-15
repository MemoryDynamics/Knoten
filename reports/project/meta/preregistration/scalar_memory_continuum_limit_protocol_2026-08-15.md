# Scalar-memory continuum-limit protocol

Date: 2026-08-15.

Status: fixed before implementation and before any numerical result from this
audit was generated.

## Question and claim boundary

The audit asks whether the local scalar memory-centre reduction has a
well-defined joint long-memory and small-step limit when comparisons keep the
dimensionless coarse-time controls fixed. It does not test physical mass,
momentum, an energy normalization, a force-work port, nonlinear knot
existence, or an underdamped mode.

Write

\[
q=1-\alpha,\qquad
\kappa={A_{\rm att}\over \sigma_{\rm att}^2}
       -{A_{\rm rep}\over \sigma_{\rm rep}^2},
\]

and, for a retained horizon `H`,

\[
M_H=M_0(1-q^H),\qquad g_H=\eta M_H\kappa.
\]

The matched continuum family fixes

\[
\chi={g_H\over\alpha},\qquad
D={\varepsilon^2\over2\alpha},\qquad
C=\alpha H,
\]

by setting

\[
H=\lceil C/\alpha\rceil,\qquad
\eta={\chi\alpha\over M_H\kappa},\qquad
\varepsilon=\sqrt{2D\alpha}.
\]

The untruncated linear prediction is

\[
\lambda_\alpha=(1-\alpha)(1-\chi\alpha),\qquad
\Gamma_\alpha=-{\log\lambda_\alpha\over\alpha}
\longrightarrow 1+\chi.
\]

The implementation comparison uses the exact finite-`H` centroid recursion,
including the dropped-tail term. The continuum exponential is a second,
strictly harder comparison and does not replace that discrete reference.

## Fixed parameters

- ambient dimension: `d=3`;
- `A_rep=1`, `A_att=35`, `sigma_rep=1`, `sigma_att=3`;
- stationary memory mass `M0=1` and delta deposition;
- coarse restoring ratio `chi=4`;
- coarse diffusion `D=1e-4`;
- formation duration `20` memory times;
- response duration `1.2` memory times;
- formation seeds `1..5`;
- mirrored visible-state offsets along the first supplied coordinate with
  `delta/R_cont in {0.005, 0.01}`;
- all response samples retained at the native update cadence.

Here

\[
R_{\rm cont}=\sqrt{dD/(1+\chi)}.
\]

The offset changes the visible coordinate only and leaves the complete memory
state untouched. It is a controlled initial-state response, not a canonical
trajectory write-port or an external-force experiment.

## Registered axes

Tail axis at `alpha=0.01`:

```text
C in {6, 9, 12}
```

Alpha axis at `C=12`:

```text
alpha in {0.04, 0.02, 0.01, 0.005, 0.0025}
```

The `alpha=0.0025` cell is the continuum holdout. Brownian increments are
generated at this finest cadence and summed exactly for coarser alpha values.
Tail cells at common alpha use identical formation and continuation noise.

## Recorded diagnostics

For every seed and offset strength the audit records:

1. the paired odd relative-coordinate response
   `(x-c)_plus-(x-c)_minus`, normalized by `2 delta`;
2. the paired self-drift response;
3. mirror-even leakage relative to the common unshifted control;
4. response-strength nonlinearity between the two registered offsets;
5. initial and final control memory radii;
6. error against the exact finite-`H` linear response;
7. error against `exp(-(1+chi)t)`;
8. a one-step pole and coarse-time decay rate, fitted only where the exact
   response remains at least `1e-3` of its initial magnitude.

No parameter is fitted and then reused as a prediction. The fitted pole is a
diagnostic checked against the coefficient fixed by the input parameters.

## Gates fixed before execution

### G0: numerical and perturbative validity

All are required:

- exact analytic finite-`H` reference identities close below `1e-12`;
- median mirror-even leakage at most `1e-3` and maximum at most `1e-2`;
- median response difference between offset strengths at most `1e-3` and
  maximum at most `1e-2`;
- every control memory-radius ratio remains in `[0.95, 1.05]`.

If G0 fails, the result is `experiment-inadequate` and physical gates are not
evaluated.

### G1: finite-tail convergence

At `alpha=0.01` all are required:

- every `C` cell has median normalized RMS error at most `0.01` against its
  exact finite-`H` reference;
- the median fitted-rate error at `C=12` is at most `0.01` relative;
- the absolute median fitted-rate change from `C=9` to `C=12` is no larger
  than the change from `C=6` to `C=9`, up to an additive tolerance `0.005`.

### G2: matched-alpha convergence

At `C=12` all are required:

- every alpha cell has median normalized RMS error at most `0.01` against its
  exact finite-`H` reference;
- every alpha cell has median fitted-rate error at most `0.01` relative to the
  exact finite-step rate;
- the holdout `alpha=0.0025` median rate is within `0.01` relative of
  `1+chi=5`;
- the holdout median normalized RMS error against `exp(-5t)` is at most
  `0.01`;
- the absolute continuum-rate error at the holdout is smaller than at
  `alpha=0.01`.

## Decision language

- G0, G1 and G2 pass: `continuum-limit-supported-in-local-linear-slice`.
- G0 passes but G1 or G2 fails with supported signal:
  `registered-continuum-limit-not-supported`.
- G0 passes but a registered comparison lacks numerical support:
  `continuum-limit-inconclusive`.
- G0 fails: `experiment-inadequate`.

Even a complete pass establishes only convergence of a real scalar
memory-relaxation law and its finite-history implementation. It does not
identify an inertial mass because the equation fixes only a relaxation ratio,
the stochastic second derivative is not a regular pathwise acceleration, and
no independently normalized force-work port is present.
