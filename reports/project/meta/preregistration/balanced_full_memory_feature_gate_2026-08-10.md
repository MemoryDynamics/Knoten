# Preregistration: balanced full-memory feature gate

Date: 2026-08-10.

## Question

Does the already deposited passive oriented memory possess a small temporal
subspace that is both reachable from trajectory deposition and observable in
an independently fixed spatial readout?

This gate does **not** search for oscillations and varies no physical model
parameter. It tests whether reducing the full oriented memory to a few modes
is empirically defensible before another memory metric or reciprocal coupling
is introduced.

## State and operators

For one ambient component, remove the duplicate age-zero orientation and use

\[
h_n=(p_n,m_{n,1},\ldots,m_{n,H-1})^\mathsf T.
\]

With \(q=1-\kappa\), the passive homogeneous update and trajectory input are

\[
p_{n+1}=q p_n+\kappa u_n,
\qquad
m_{n+1,1}=p_n,
\qquad
m_{n+1,j}=m_{n,j-1}.
\]

The finite-horizon controllability factor is

\[
R_T=[B,AB,\ldots,A^{T-1}B],
\qquad B=\kappa e_0.
\]

At each future sample, the fixed Gaussian probe supplies a row \(C_t\). The
observability factor stacks block-weighted rows \(C_tA^t\). Leading singular
values of \(O_TR_T\) and the reachable state images of its right singular
vectors define the balanced candidates. Ambient components are degenerate in
this passive model; this test cannot select spatial dimension.

## Fixed data and geometry

- the six existing mature `d=3`, `A_att=35`, `N=3M` scalar snapshots;
- cyclic independent target/source pair labels `1<-2,...,6<-1`;
- `lambda_vector=0.01`, `orientation_relaxation=0.01`, vector mass `1`;
- source centre at `2.5 R_pair` from the fixed near probe;
- inherited Gaussian readout width `2.5 R_source`;
- a fixed far holdout probe at `5 R_pair` from the initial source centre;
- two consecutive, non-overlapping segments whose starts differ by ten
  vector-memory times;
- horizons of five and ten vector-memory times;
- cadences of 1, 5 and 10 updates with endpoint block weights;
- at most 12 reported modes and candidate rank at most 8;
- no seedwise gain, kernel, radius, horizon, cutoff or rank retuning.

The source trajectory remains the existing passive scalar process. The
balanced input is the already implemented persistent-direction deposition,
not a newly simulated force channel.

## Controls

1. **Flat readout:** retain the exponential age weights but remove all spatial
   Gaussian factors. A pass here identifies generic delay-line compression.
2. **Age-shuffled geometry:** apply one fixed random permutation of the spatial
   factors across ages in each segment while retaining the correct age weights
   and marginal spatial-factor distribution. This removes space-age alignment
   without injecting samplewise temporal noise.
3. **Far holdout:** fit modes only with the near readout and evaluate output
   reconstruction at the unfit far probe.

## Fixed gates

For every target/source pair, all 12 actual-geometry evaluations (two
segments, two horizons, three cadences) must satisfy:

1. one common non-null rank \(r\le8\);
2. a singular-value gap \(s_r/s_{r+1}\ge3\);
3. at least 90% of the full estimated squared Hankel energy in the first
   \(r\) modes;
4. randomized tail-energy relative standard error at most 5%;
5. weakest principal cosine at least 0.90 against the pair's reference
   subspace;
6. far-probe randomized output error at most 15%.

The ensemble effective-closure gate requires at least five of six pair gates,
one common rank among passing pairs and weakest cross-pair principal cosine at
least 0.90.

A passing pair is called **geometry-specific** only when neither control has a
stable two-segment final-horizon/base-cadence subspace equivalent to the
actual one (same rank and principal cosine at least 0.90). The stronger
geometry-specific ensemble decision requires at least five such pairs.

## Decision rules

- **Fail:** the effective-closure gate fails. Close the adjoint-reciprocal
  vector branch in its current form; do not tune gains or lambda.
- **Constitutive-only:** effective closure passes but the controls reproduce
  it. The modes are useful compression of the imposed delay/readout, not
  knot-specific evidence.
- **Geometry-specific pass:** both ensemble gates pass. This authorizes only a
  reduced carrier-plus-field metric comparison and independent time-domain
  validation. It does not yet authorize a nonlinear reciprocal simulation.

Only after a metric-stable reduced state predicts a held-out trajectory may a
narrow analytically centered parameter test ask whether a complex pole is a
long-lived temporal oscillation. Complex eligibility by itself is not an
observed oscillation.
