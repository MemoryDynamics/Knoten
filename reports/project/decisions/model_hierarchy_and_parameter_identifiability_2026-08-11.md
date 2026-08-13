# Model hierarchy and inertial-parameter identifiability

Date: 2026-08-11; P3.8e mechanism-closure addendum: 2026-08-13.

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

## Rigorous route from canonical memory to an effective `(m,p)`

The admissible claim is not that a new microscopic momentum has appeared.
It is that the canonical Markov process admits, for a preregistered observable
and response experiment, a minimal effective realization with two predictive
states.

Let \(U\) be the Markov/Koopman operator of \(z=(x,\rho)\), let
\(Y=\Psi(z)\) be fixed without inspecting the desired spectrum, and let
\(P\) be the linear \(L^2\) projection onto the resolved observables under a
mature quasi-stationary ensemble. For the local linear response, decompose the
resolved and unresolved action as

\[
\begin{pmatrix}Y_{n+1}\\W_{n+1}\end{pmatrix}
=
\begin{pmatrix}A&B\\C&D\end{pmatrix}
\begin{pmatrix}Y_n\\W_n\end{pmatrix}.
\]

Eliminating \(W\) gives the exact finite-time projected relation

\[
Y_{n+1}
=AY_n
+\sum_{j=0}^{n-1}BD^jC\,Y_{n-1-j}
+BD^nW_0.
\]

Thus the reduced memory kernel \(K_j=BD^jC\) is an output of the canonical
dynamics and the chosen projection. It must be estimated before selecting a
mechanical ansatz. The corresponding nonlinear statement is the
Mori-Zwanzig generalized Langevin equation; the block formula above is the
local linear-response version needed by the present project.
For realized stochastic paths an orthogonal fluctuating-force/innovation term
must additionally be retained. It is a martingale difference only for an
appropriate conditional-expectation construction, not for a generic
Mori-Zwanzig projection. The displayed identity is exact for the linearized
conditional-mean operator with a complete resolved/unresolved decomposition;
it is not a claim that a finite deterministic AR model exactly describes the
canonical sample paths.

A projection also cannot create a causal cross-channel absent from the
canonical transition kernel. Single-knot `K0` data can at most select an
effective internal mode. Identifying the P3.8d source-to-source mediator
requires a preregistered canonical shared-field or multi-source transition law
before projection. Without such a law, `(m,p)` remains an explicit extension
even if it is a useful realization of a separately measured response.

Only if the independently measured source-to-readout transfer function has a
stable second-order minimal realization in one preregistered spatial or
symmetry mode, and a first-order realization fails on holdout responses, may
that modal state be written in oscillator coordinates. For one mode these
coordinates can be chosen as

\[
\dot m=p,
\qquad
\dot p=-2\Gamma p-\Omega^2m+b\,u.
\]

Minimal state coordinates are unique only up to an invertible similarity
transformation. Therefore \(m\), \(p\), their separate norms and their common
energy scale are not observables. Poles, zeros, residues and the complete
input-output map are invariant. Calling the second coordinate `p` is justified
only after all of the following hold:

1. the second-order modal realization is selected by a Hankel/realization-rank
   gap and out-of-sample prediction, not by a harmonic fit;
2. the inferred continuous poles agree across sampling cadences, horizons,
   seeds, time segments and spatial resolutions;
3. after fixing power-conjugate ports, for example generalized force and
   generalized velocity rather than force and displacement, one positive
   storage metric makes the fitted write/read pair passive and reciprocal on
   independent responses;
4. the reversible part in the resulting port-Hamiltonian decomposition is
   nonzero and reproducible over the admissible storage metrics, while the
   dissipative part accounts for measured damping;
5. the same realization predicts a withheld force, phase and pair response
   without gain or timescale retuning.

Under those gates, `m` denotes the resolved field-like coordinate and `p` its
additional predictive state. Only a storage-metric-robust reversible coupling
licenses the stronger name phase or conjugate coordinate. It is still not the
momentum of the visible point \(x\), and it is not evidence of quantization.
Two distinct real relaxation poles can also have minimal order two and be
written in companion form. They do not by themselves establish a conjugate
momentum. The passive reciprocal realization must contain a storage-metric-
robust reversible coupling. A stable complex pair additionally identifies an
underdamped regime, but complex poles are not required for second-order
minimality.

For a field this comparison is modal, not globally rank one versus rank two.
If \(r\) independently observable spatial modes are retained, a first-order
field has at least \(r\) states and an `(m,p)` field generically has \(2r\).
Several fixed finite-wavenumber channels are therefore required to establish
the P3.8d dispersion; one global rank-two fit would show only one coarse mode.
The previous spatially uniform weak probe is a pipeline control, not an
identification input for the gradient mediator: its \(k=0\) response is
annihilated by the registered \(k^2\) numerator. P3.8e needs a fixed localized
or zero-mean finite-\(k\) perturbation and a separate withheld readout.

### Long-time and self-consistency boundary

Running the already constructed P3.8d system for longer cannot select this
state. Its strict Lyapunov balance and the matched static susceptibility imply
that first- and second-order arms approach the same stationary equations.
Longer autonomous runs can test numerical convergence, basin stability or,
after a separately justified noise law, escape statistics. They cannot derive
the dynamic order. Inertia can in principle carry the second-order arm across
a separatrix and thereby change basin capture for some initial states. A
registered basin map could test that consequence, but it would still test an
assumed `(m,p)` mechanism rather than establish its emergence.

Long-time canonical data are useful for a different question: whether the
identified transfer function becomes independent of knot age. Let \(\theta\)
contain measured knot observables such as memory radius, covariance shape,
local restoring spectrum and relaxation time. The non-circular closure is

\[
\theta
\longmapsto \chi_\theta(k,\omega)
\longmapsto \vartheta(\theta)
\longmapsto \mathcal C(\theta,\vartheta),
\]

where \(\chi_\theta\) is a measured weak-response susceptibility,
\(\vartheta\) is its minimal passive realization, and \(\mathcal C\) is the
coarse evolution of the knot observables. Self-selected effective parameters
require a stable fixed point of the composite map

\[
\mathcal F(\theta):=\mathcal C(\theta,\vartheta(\theta)),
\qquad
\theta_*=\mathcal F(\theta_*),
\qquad
\rho(D\mathcal F(\theta_*))<1.
\]

This fixed-point test treats apparent parameters as state-dependent response
coefficients. If the inferred mediator is not fed back by the canonical
transition law, it remains an offline effective closure rather than a
spontaneously selected microscopic mechanism.

The current mature checkpoint has \(R_{\rm mem}/\ell\simeq2.12\times10^{-4}\).
Its far response is consequently dominated by the point/monopole limit, so a
similar knot and kernel potential is expected for many inequivalent internal
models. Internal feedback requires either probes with \(kR_{\rm mem}=O(1)\)
or preregistered mature knots of at least two resolved sizes. More elapsed
updates alone do not remove this scale-separation ambiguity.

## Consequence for the next step

P3.7 is changed from a coupled-field simulation to an identifiability/no-go
gate:

1. specify candidate \(\Psi(x,\rho)\) using only canonical variables;
2. preregister first- versus second-order held-out predictive comparison;
3. require pole identity across seeds, segments and coarse-graining;
4. require prediction of an independent response;
5. reject parameter estimation if these gates fail.

The first implementation must estimate a nonparametric finite-\(k\) weak
impulse response before fitting P3.8d. For each registered mode it then
compares four fixed candidates on common holdouts: first order, unconstrained
second order, passive reciprocal second order, and a nonparametric delay
kernel. Formation-age windows test coefficient stationarity; they are not
separate tuning datasets. The passivity test uses the power-conjugate response
channel; the displacement susceptibility remains a separate prediction
target. The P3.8d spatial polynomial contains the three coefficients
\(a,b,c\). At least four fixed finite-\(k\) channels are therefore required:
no fewer than three training channels and at least one untouched dispersion
holdout. If the decay-rate product is not independently fixed, one additional
channel is required.

## P3.8e outcome addendum (2026-08-13)

The historical finite-`k` identification is
`superseded-methodologically-inconclusive`. Free and "damped" AR(2) were the
same model for the reported stable conjugate poles, active-minus-`eta=0` could
itself create second-order behavior, and the old panel-Hankel layout could
inflate rank through differing residues.

The corrected analysis fits active and `eta=0` separately, withholds the
visible readout, uses common target windows, and stacks all panel readouts into
one Hankel output vector. Technical controls pass, but zero of five channels
passes the complete requirement. All pooled active AR(2) poles are real,
AR(2) has no recursive holdout advantage, and `s3/s2=0.557..0.695` does not
isolate rank two. The genuinely undamped reference is distinctly worse.

This remains holdout-limited rather than a universal scalar-memory no-go:
only `0.2%..0.8%` of scale-balanced memory energy lies in holdout, and the
five input profiles have median Gram condition `15867`. In addition, the
intervention initializes a valid memory-state deformation rather than writing
through the trajectory-deposition map. The only admissible scalar follow-up
is therefore a preregistered zero-net visible pulse through the canonical
write port, using a weighted-orthogonalized or explicitly rank-reduced input
basis and blocked signal-window validation. Failure there closes the scalar
route to `(m,p)`; an oriented/current memory or shared multi-source field must
then be declared a new model state.

## Method anchors

- Mori's projection formalism derives generalized Langevin dynamics and
  linear response from selected observables:
  <https://doi.org/10.1143/PTP.33.423>.
- Lin, Tian, Anghel and Livescu give a data-driven Mori-Zwanzig/Koopman
  operator construction with explicit Markov, memory and orthogonal terms:
  <https://arxiv.org/abs/2101.05873>.
- Juang and Pappa's eigensystem realization algorithm obtains minimum-order
  modal realizations from impulse-response Hankel matrices and supplies mode
  accuracy indicators: <https://ntrs.nasa.gov/citations/19850064186>.
- Discrete/continuous positive-real state-space inequalities provide the
  passivity/storage test; they do not themselves select model order:
  <https://arxiv.org/abs/2008.04635>.

Only a pass may motivate deriving effective \(\gamma/I\) and \(D_q(k)/I\).
Absolute \(I,\gamma,D_q\) require an independent response normalization.
Otherwise the
inertial model remains a clearly labelled Paper-III comparison model, or its
extra state and coefficients must be declared new primitive assumptions.

The source/readout energy and a nonlinear field pilot remain downstream and
blocked. This prevents selecting parameters merely because they maximize a
desired oscillation.
