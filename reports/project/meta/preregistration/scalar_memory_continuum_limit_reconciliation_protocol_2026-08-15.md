# Scalar-memory continuum-limit reconciliation protocol

Date: 2026-08-15.

Status: fixed after the registered seed-1--5 audit, but before implementation
of the corrected radius diagnostic and before any seed-6--10 result was
generated or inspected.

## Purpose and non-retrospective boundary

The original registered audit returned `experiment-inadequate`. Its G0 radius
check divided the final unshifted-control radius by the initial control radius
while Brownian noise continued to drive the system. Across the registered
cells that ratio ranged from approximately `0.798` to `1.140`, although the
paired mirror and offset-strength residuals were respectively of order
`1e-8` and `1e-10`. The radius check therefore mixed ordinary stochastic
radius evolution with damage caused by the intervention.

This reconciliation changes only that invalid comparator. It does not alter
or reinterpret the original decision, and it is not an independent
preregistration of the full hypothesis: its design is explicitly informed by
the first audit. It uses new, previously uninspected noise streams to test the
corrected validity condition prospectively.

## Fixed model and matched family

The model, scaling and claim boundary are identical to the original protocol:

\[
q=1-\alpha,\qquad
\chi={g_H\over\alpha}=4,\qquad
D={\varepsilon^2\over2\alpha}=10^{-4},\qquad
C=\alpha H,
\]

with

\[
H=\lceil C/\alpha\rceil,\qquad
\eta={\chi\alpha\over M_H\kappa},\qquad
\varepsilon=\sqrt{2D\alpha}.
\]

All of the following remain fixed:

- `d=3`, `M0=1`;
- `A_rep=1`, `A_att=35`, `sigma_rep=1`, `sigma_att=3`;
- formation duration `20` memory times and response duration `1.2` memory
  times;
- mirrored offsets `delta/R_cont in {0.005, 0.01}` along coordinate 1;
- tail axis `C in {6, 9, 12}` at `alpha=0.01`;
- alpha axis `alpha in {0.04, 0.02, 0.01, 0.005, 0.0025}` at `C=12`;
- `alpha=0.0025` as the continuum holdout;
- exact Brownian coarsening from the finest cadence;
- the exact finite-`H` linear response as the primary implementation
  reference and `exp(-5t)` as the continuum reference.

The prospective formation seeds are `6..10`. Their random streams use the
same fixed generator convention `20260815 + seed`; no seed from the original
audit is reused.

## Corrected radius diagnostic

At every native response sample, including the pre-response sample, record the
weighted finite-memory RMS radius for the unshifted control and for every
mirrored displaced branch. Let `R_b(t)` denote a displaced-branch radius and
`R_0(t)` the simultaneous common-noise control radius.

The intervention-preservation comparison is

\[
{R_b(t)\over R_0(t)},
\]

not `R_0(t_final)/R_0(t_initial)`. The latter quantity remains available only
as a descriptive stochastic-drift diagnostic and has no gate role.

## Gates fixed before reconciliation execution

### G0R: numerical, local and perturbative validity

All are required:

- exact analytic finite-`H` reference identities close below `1e-12`;
- median mirror-even leakage at most `1e-3` and maximum at most `1e-2`;
- median response difference between offset strengths at most `1e-3` and
  maximum at most `1e-2`;
- every recorded control and displaced-branch memory radius is finite and
  strictly positive;
- every recorded memory radius satisfies `R/sigma_rep <= 0.02`;
- every simultaneous displaced/control radius ratio lies in `[0.95, 1.05]`.

The local-radius threshold corresponds to a squared scale ratio no larger
than `4e-4`; the mirror and strength checks independently test whether the
actual response remains in the linear perturbative slice.

If G0R fails, G1R and G2R are blocked and the reconciliation is inadequate.

### G1R: finite-tail convergence

The original G1 thresholds are unchanged. At `alpha=0.01` all are required:

- every `C` cell has median normalized RMS error at most `0.01` against its
  exact finite-`H` reference;
- the median fitted-rate error at `C=12` is at most `0.01` relative;
- the absolute median fitted-rate change from `C=9` to `C=12` is no larger
  than the change from `C=6` to `C=9`, up to additive tolerance `0.005`.

### G2R: matched-alpha convergence

The original G2 thresholds are unchanged. At `C=12` all are required:

- every alpha cell has median normalized RMS error at most `0.01` against its
  exact finite-`H` reference;
- every alpha cell has median fitted-rate error at most `0.01` relative to the
  exact finite-step rate;
- the holdout `alpha=0.0025` median rate is within `0.01` relative of `5`;
- the holdout median normalized RMS error against `exp(-5t)` is at most
  `0.01`;
- the absolute continuum-rate error at the holdout is smaller than at
  `alpha=0.01`.

## Decision language

- G0R, G1R and G2R pass:
  `continuum-limit-supported-in-prospective-reconciliation`.
- G0R passes but G1R or G2R fails:
  `registered-continuum-limit-not-supported-in-reconciliation`.
- G0R fails: `reconciliation-experiment-inadequate`.

A complete pass supports only the constructed local scalar memory-relaxation
limit. It does not establish physical mass, momentum, underdamped inertia, a
force-work normalization, nonlinear knot persistence, uniqueness of this
scaling, or the physical interpretation of coarse time.
