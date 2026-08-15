# Scalar-memory force/work-port protocol

Date: 2026-08-16.

Status: force normalization, observables, seeds, alternatives and thresholds
fixed before implementation of the port and before any seed-11--15 response
was generated or inspected.

## Question and claim boundary

The preceding continuum audit supports a constructed local scalar
memory-relaxation limit but cannot identify mass because it has no
independently normalized input/work pair. This protocol adds a dimensionless
generalized force port to the existing visible-coordinate update and asks
whether its high-frequency input/output behavior is compatible with

1. the overdamped scalar-memory limit already derived, or
2. a regular finite-mass inertial coordinate driven by force through its
   acceleration equation.

The port fixes dimensionless force units. It does not supply a mapping to SI
energy or prove that the generalized force is a physical force. A result can
reject an inertial reading of this canonical port without proving a no-go for
all possible coarse grainings or extended states.

## Fixed port

For a force profile `f_n` along a fixed unit vector `e`, the nonlinear native
update is

\[
x_{n+1}=x_n-\eta\nabla V_H(x_n)
          +\alpha f_n e+\varepsilon\xi_n.
\]

The finite-memory deposition rule is unchanged. The coefficient of `f_n` is
fixed to `alpha` before observing a response; no response-fitted gain or mass
normalizes the input.

The discrete supplied work is fixed as the right-endpoint displacement work

\[
W_N=\sum_{n=0}^{N-1} f_n e\cdot(x_{n+1}-x_n).
\]

Mirrored `+f` and `-f` branches share formation and continuation noise. Their
odd response removes the common stochastic trajectory. Their even mean work
removes the term linear in the common unforced increment.

## Local continuum alternatives

With `r=x-c`, `g=chi alpha`, `epsilon^2=2D alpha` and
`Gamma=1+chi`, the registered local limit of the new port is

\[
dx=(-\chi r+f)dt+\sqrt{2D}\,dW,
\qquad
dc=r\,dt,
\qquad
dr=(-\Gamma r+f)dt+\sqrt{2D}\,dW.
\]

Its deterministic force-to-visible-velocity transfer is

\[
{\dot X(s)\over F(s)}={s+1\over s+\Gamma}.
\]

It has unit high-frequency feedthrough. By contrast, a regular passive
finite-mass coordinate

\[
m\ddot x+\gamma\dot x=f,
\qquad 0<m<\infty,
\]

has

\[
{\dot X(s)\over F(s)}={1\over ms+\gamma}\longrightarrow0
\quad(s\longrightarrow\infty).
\]

For deterministic trajectories the scalar-memory storage

\[
U={\chi\over2}|r|^2
\]

satisfies the continuous work balance

\[
\dot U=f\cdot\dot x-|\dot x|^2-\chi|\dot c|^2.
\]

This balance defines the work-ledger reference; its finite-step residual is
expected to converge to zero but is not forced to vanish for the native
explicit update.

## Fixed parameters and prospective data

The matched family is inherited unchanged from the continuum reconciliation:

- `d=3`, `chi=4`, `D=1e-4`, `C=alpha H=12`, `M0=1`;
- `A_rep=1`, `A_att=35`, `sigma_rep=1`, `sigma_att=3`;
- `alpha in {0.04, 0.02, 0.01, 0.005, 0.0025}`;
- formation duration `20` memory times;
- response duration `1.2` memory times at native cadence;
- new formation seeds `11..15`;
- fixed noise convention `20260816 + seed`;
- force axis equal to coordinate 1;
- exact Brownian coarsening from `alpha=0.0025` to every coarser cell.

Let

\[
R_{\rm cont}=\sqrt{dD/(1+\chi)}.
\]

The two registered impulse magnitudes are

```text
J/R_cont in {0.005, 0.01}.
```

Each pulse lasts exactly one native update and has

\[
f_0=J/\alpha,\qquad f_{n>0}=0,
\]

so its integrated input is `alpha sum(f_n)=J` at every alpha. The smaller
strength is not selected after seeing the larger response; both are used for
the perturbative-strength check.

## Fixed force-response predictions

For a unit positive impulse and `s=t-alpha>=0` measured after the pulse, the
continuum overdamped response is

\[
h_r(s)=e^{-\Gamma s},\qquad
h_x(s)={1+\chi e^{-\Gamma s}\over\Gamma},\qquad
h_c(s)={1-e^{-\Gamma s}\over\Gamma}.
\]

At native finite step the exact finite-`H` linear recursion, including its
dropped-tail term, is the primary implementation reference. The continuum
formula is a harder secondary comparison.

The one-step port gives the following high-frequency predictions before any
simulation:

\[
{\Delta x_{\rm pulse}\over J}\longrightarrow1,
\qquad
{\alpha W\over J^2}\longrightarrow1,
\qquad
{x_2-x_1\over\alpha J}\longrightarrow-\chi=-4.
\]

The negative post-pulse motion is restoring relaxation, not continued
positive inertial motion.

For the stationary unforced local process, the exact visible MSD per ambient
coordinate is

\[
\begin{aligned}
{\rm MSD}_x(t)={}&{D\chi^2\over\Gamma^3}(1-e^{-\Gamma t})^2\\
&+{2D\over\Gamma^2}\left[
t+{2\chi\over\Gamma}(1-e^{-\Gamma t})
 +{\chi^2\over2\Gamma}(1-e^{-2\Gamma t})
\right],
\end{aligned}
\]

and therefore `MSD_x(t)=2Dt+O(t^2)`. A regular inertial position with finite
velocity variance instead has a ballistic `t^2` short-time law.

The MSD check uses only `alpha=0.0025`, `65,536` stationary local-linear
paths, fixed RNG seed `20260816`, and the preregistered fit window
`t in [2 alpha, 16 alpha]`.

## Recorded diagnostics

For every alpha, formation seed and impulse magnitude:

1. integrated force input and force-off clone residual;
2. odd position, memory-center and relative-coordinate responses;
3. mirror-even leakage and cross-axis response;
4. difference between the two normalized impulse-strength responses;
5. simultaneous displaced/control memory-radius ratios and maximum local
   radius;
6. even supplied work and `alpha W/J^2`;
7. error against the exact finite-`H` force response;
8. error against the registered continuum impulse response;
9. exact native storage/work/dissipation-ledger residual;
10. pulse-end feedthrough and first post-pulse velocity;
11. Monte Carlo and analytic stationary visible MSD and their log-log slopes.

## Gates fixed before execution

### G0: port, numerical and perturbative validity

All are required:

- integrated input error at most `1e-14`;
- force-off clone maximum state residual at most `1e-14`;
- exact forced finite-`H` recurrence residual at most `1e-12`;
- every `|alpha W/J^2-1|` at most `1e-10`;
- median mirror-even leakage at most `1e-3` and maximum at most `1e-2`;
- median strength-response difference at most `1e-3` and maximum at most
  `1e-2`;
- all memory radii finite and positive, with `max R/sigma_rep <= 0.02`;
- every simultaneous forced/control radius ratio in `[0.95, 1.05]`.

If G0 fails, every physical discrimination gate is blocked.

### G1: force-response and work-ledger closure

All are required:

- every alpha cell has median normalized RMS position and relative-response
  error at most `0.01` against the exact finite-`H` reference;
- every alpha cell has median relative fitted-rate error at most `0.01`
  against the exact finite-`H` response;
- at the `alpha=0.0025` holdout, median position and relative-response errors
  against the continuum impulse response are each at most `0.01`;
- the absolute native ledger residual divided by supplied work is at most
  `0.01` at the holdout and is smaller there than at `alpha=0.01`;
- the Monte Carlo MSD differs from its exact local-linear reference by at
  most `0.01` normalized RMS over the fixed fit window.

### G2O: overdamped-memory signature

All are required:

- holdout pulse-end feedthrough lies in `[0.95, 1.05]`;
- holdout first post-pulse velocity divided by impulse lies in `[-4.1,-3.5]`;
- holdout `alpha W/J^2` lies in `[0.99, 1.01]`;
- the stationary visible-MSD slope lies in `[0.9, 1.1]`.

### G2I: regular finite-inertial signature

All are required for an inertial candidate:

- holdout pulse-end feedthrough is at most `0.05`;
- holdout first post-pulse velocity divided by impulse is strictly positive;
- holdout `alpha W/J^2` is at most `0.05`, as required when impulse work
  remains finite while `alpha -> 0`;
- the stationary visible-MSD slope lies in `[1.8, 2.2]`.

G2I is an explicit competing signature, not the Boolean negation of G2O.
Mixed results are inconclusive.

## Decision language

- G0 and G1 pass, G2O passes and G2I fails:
  `force-port-supports-overdamped-memory-not-finite-inertial-mass`.
- G0 and G1 pass, G2I passes and G2O fails:
  `finite-inertial-port-signature-candidate`.
- G0 and G1 pass but neither alternative is uniquely selected:
  `force-port-discrimination-inconclusive`.
- G0 fails: `force-port-experiment-inadequate`.
- G0 passes and G1 fails: `force-port-reference-closure-failed`.

Even the inertial-candidate outcome would require an independent protocol,
new data and a physical unit map before any mass claim. The overdamped outcome
rejects only a finite-mass reading of this canonical additive-force port; it
does not rule out an extended momentum field inserted or derived elsewhere.
