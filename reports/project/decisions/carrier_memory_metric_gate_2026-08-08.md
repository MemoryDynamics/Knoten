# Carrier-memory metric gate

Date: 2026-08-08.

## Decision

The next reciprocal-memory step compares covariance, predictive and kernel
metrics before any nonlinear reciprocal simulation. All three metrics act on
the same reduced feature

\[
h_n=p_n\in\mathbb R^3,
\]

the persistent carrier. This is not the full Markov memory state
\((x_n,\rho_n,p_n,m_n)\). A pass may nominate an effective carrier metric; it
cannot establish a microscopic memory geometry.

## Why prediction uses a probe

In the implemented passive source, oriented memory does not affect its own
visible trajectory. Its self-observability Gramian is therefore exactly zero.
Using a reciprocal self-response here would assume the backchannel that the
metric is meant to constrain.

The predictive metric instead uses the previously fixed one-way response of an
independent probe knot:

\[
G_{\rm pred}(T)
=
\sum_{\tau\le T}w_\tau
J_\tau^\mathsf T J_\tau/R_T^2,
\qquad
J_\tau=
\frac{\partial x^{(T)}_{n+\tau}}{\partial p_n}.
\]

The Jacobian is measured by paired central finite differences with common
source and target noise. A second perturbation amplitude is a linearity control.

## Compared metrics

The covariance metric is

\[
G_{\rm cov}=\operatorname{Cov}(p_n)^+.
\]

It uses a truncated pseudoinverse. Unsupported directions remain null; no ridge
may turn an unobserved direction into a stiff one.

The kernel metric propagates one carrier perturbation through the passive
carrier and vector-memory updates and measures the emitted Gaussian field in
the associated normalized RKHS:

\[
G_{\rm kernel}(T)
=
\sum_{\tau\le T}w_\tau
\lVert\delta m_{n+\tau}\rVert_{\mathcal H_K}^2 I.
\]

It inherits the already fixed Gaussian readout width and is not a kernel-free
result.

For all metrics, exact exponential block masses

\[
w_{[a,b]}=q^a-q^b
\]

make different observation cadences comparable without renormalizing every
finite horizon to unit mass.

## Fixed design

- mature d=3 formation seeds 1 through 6;
- cyclic independent pairs \(1\leftarrow2,\ldots,6\leftarrow1\);
- two non-overlapping segment starts separated by ten memory times;
- horizons 1, 2, 5 and 10 memory times;
- cadences 1, 5 and 10 updates;
- carrier perturbations \(10^{-4}\) and \(5\times10^{-5}\);
- inherited global `vector_eta=5.079e-6`;
- distance `2.5 R_pair` and Gaussian width `2.5 R_source`, fixed from the
  original pair state and not recomputed for the second segment;
- no seedwise gain, metric, cutoff, distance or kernel retuning.

## Gates

Per pair:

1. finite-difference linearity error at most 5%;
2. predictive metric scale drift across cadences at most 20%;
3. predictive metric-shape drift across cadences at most 10%;
4. maximum metric-shape drift across two segments at most 25%;
5. metric-trace drift from five to ten memory times at most 25%;
6. supported metric-subspace overlap across metrics at least 0.90;
7. reciprocal classifications stable across both segments;
8. at least 90% of all supported update modes in every final segment/metric
   belong to one reciprocal regime;
9. covariance, predictive and kernel metrics give the same final reciprocal
   classification signature.

At least five of six pairs must pass. The last criterion is deliberately
strong: agreement only after trace normalization would leave the unresolved
overall metric scale untouched.

## Interpretation rules

A pass authorizes one nonlinear holdout pilot with the selected reduced metric.
It does not prove inertia, oscillation, spin or physical parameter selection.

A fail means that the Euclidean eligibility result is representation- or
normalization-sensitive. No gain sweep follows. The next decision must then be
whether to retain the metric as an explicit effective constitutive choice or to
enlarge the measured memory feature beyond the carrier.

The normalized-direction Jacobian always has one longitudinal null and two
transverse directions in d=3. High subspace overlap can therefore be structural
and is not sufficient evidence for an emergent three-dimensional geometry.

## Protocol correction before accepted execution

The first execution exposed a protocol error before its output was accepted,
committed or interpreted. It classified each segment with the single source
step immediately before the segment start. Since

\[
B_n=\kappa(I-u_nu_n^\mathsf T)/\lVert\Delta x_n\rVert
\]

depends strongly on the instantaneous step length, this sampled neither a
representative knot state nor a segment-level mode distribution. Those outputs
were deleted and are not evidence.

The corrected protocol evaluates \(B_n\) at every update in each segment. It
reports regime fractions over all non-null transverse modes and assigns a
dominant label only when its fraction is at least 0.90. Structural longitudinal
null modes are reported separately. Metric-shape and supported-subspace gates
are evaluated directly in the common carrier coordinates, not through one
arbitrarily selected pullback. All previously fixed seeds, horizons, cadences,
perturbations, gains, kernels and numerical tolerances remain unchanged.

## Outcome

The corrected clean-revision execution fails the preregistered gate in all six
cyclic pairs. Across the 12 final segment evaluations, covariance classifies
all as unstable, the predictive metric classifies 11 as overdamped and one as
mixed, and the isotropic RKHS metric classifies all as complex. Finite-
difference linearity and predictive cadence tests pass in every pair, so the
failure is not attributable to an unresolved tangent or sampling cadence.
Absolute metric scale, several horizon/segment checks and cross-metric
classification do not reconcile.

No nonlinear reciprocal pilot, gain retuning or lambda sweep is authorized.
The next discriminating step is a matrix-free balanced feature test on the
already deposited oriented full-memory state. It must demonstrate a stable
controllable-and-observable low-rank subspace before any reduced metric or
quadratic field energy is promoted beyond an explicit constitutive model.
