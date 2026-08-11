# Model hierarchy and inertial-parameter identifiability

Date: 2026-08-11.

## Decision

The inertial vector-field gate is a consistency test of a proposed extension,
not a derivation from the canonical knot equations. No parameter optimization
or coupled field pilot is admissible yet.

## What is actually simulated

The canonical state is

\[
z_n=(x_n,\rho_n),
\]

with

\[
x_{n+1}
=x_n+\varepsilon\xi_n-\eta\nabla(K*\rho_n)(x_n),
\]

\[
\rho_{n+1}(x)
=(1-\lambda_m)\rho_n(x)+\beta G_\sigma(x-x_{n+1}),
\qquad \beta=\lambda_mM_0
\]

in the package normalization. `FiniteMemoryState` stores a controlled finite
point representation of this scalar field. It does not contain an inertial or
conjugate field variable.

The passive oriented extension records a carrier direction and directed
deposits. Its source trajectory is still advanced by the scalar force only.
It therefore adds observables and one-way response pilots, not a reversible
source self-field.

## What the inertial gate added

The separate analytic module proposes

\[
\partial_t m=\frac{\pi}{I},
\qquad
\partial_t\pi
=-\frac{\delta\mathcal F}{\delta m}
-\frac{\gamma}{I}\pi+J.
\]

For a linear longitudinal or transverse mode this gives

\[
Is^2+\gamma s+D_q(k)=0.
\]

The second state \(\pi\), inertia \(I\), damping \(\gamma\), field energy
\(\mathcal F\), source \(J\), and their coupling to \(x\) are absent from the
canonical update. The analytic pass is consequently constructive: a harmonic
mode appears because an independent conjugate state was introduced.

This is classical damped-field mechanics. It is not quantum mechanics and
does not establish quantization, spin, a photon, a particle or an emergent
oscillator.

## Identifiability result

Existing scalar or passive-vector long runs cannot identify

\[
(I,\gamma,a,b_L,b_T,c,u)
\]

as microscopic constants, because these coefficients do not occur in their
transition law. Defining \(\pi_n\) algebraically from present and lagged
passive memory also does not solve the problem: it only embeds the same
first-order state in delay coordinates and creates no independent conjugate
degree of freedom.

An effective second-order closure is admissible only after fixing, without
using the desired spectrum, a projection

\[
Y_n=\Psi(x_n,\rho_n)
\]

from the canonical state. On held-out trajectories it must then outperform a
first-order closure such as

\[
Y_{n+1}=A_1Y_n+e_{n+1}
\]

with a genuinely second-order model,

\[
Y_{n+1}=A_1Y_n+A_2Y_{n-1}+e_{n+1}.
\]

The resulting poles and dimensionless coefficients must remain stable across
seeds, time segments, sampling cadences, block sizes and prediction horizons.
They must also predict an independent response observable. A spectral peak or
a good in-sample harmonic fit is insufficient.

### What a successful mode could identify

For a cadence \(\Delta n\), let a stable fitted pair be

\[
\mu_\pm=r e^{\pm i\theta},
\qquad 0<r<1.
\]

After cadence/branch reconciliation, its continuous-generator representation
is

\[
s_\pm=-\Gamma\pm i\omega,
\qquad
\Gamma=-\frac{\log r}{\Delta n},
\qquad
\omega=\frac{\theta}{\Delta n}.
\]

Comparison with \(Is^2+\gamma s+D=0\) identifies only

\[
\frac{\gamma}{I}=2\Gamma,
\qquad
\frac{D}{I}=\Gamma^2+\omega^2.
\]

It does not identify \(I\), \(\gamma\), and \(D\) separately. Their common
scale is a gauge freedom of the homogeneous equation. Separating them requires
an independently normalized forcing/response susceptibility or an energy
calibration. If the source normalization is itself adjustable, even that
separation remains non-identifiable.

Likewise, a discrete AR(2) fit

\[
Y_{n+1}=A_1Y_n+A_2Y_{n-1}+e_{n+1}
\]

identifies its discrete poles directly. Mapping them to a continuous
\((\Gamma,\omega)\) is admissible only when the result is invariant under at
least two sampling cadences and no logarithm branch is selected to obtain a
preferred frequency.

The completed passive Fourier audit found only the exact real forgetting
factor. The metric comparison failed to reconcile classifications, and the
balanced full-memory gate found a generic rank-one delay/readout mode that was
indistinguishable from flat and age-shuffled controls. Current evidence
therefore does not supply a defensible \(\Psi\) with an independent conjugate
state.

## Consequence for the next step

P3.7 is changed from a coupled-field simulation to an identifiability/no-go
gate:

1. specify candidate \(\Psi(x,\rho)\) using only canonical variables;
2. preregister first- versus second-order held-out predictive comparison;
3. require pole identity across seeds, segments and coarse-graining;
4. require prediction of an independent response;
5. reject parameter estimation if these gates fail.

Only a pass may motivate deriving effective \(\gamma/I\) and \(D_q(k)/I\).
Absolute \(I,\gamma,D_q\) require an independent response normalization.
Otherwise the
inertial model remains a clearly labelled Paper-III comparison model, or its
extra state and coefficients must be declared new primitive assumptions.

The source/readout energy and a nonlinear field pilot remain downstream and
blocked. This prevents selecting parameters merely because they maximize a
desired oscillation.
