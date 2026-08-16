# Preregistration: scalar-memory center filter scaling B-star

Date: 2026-08-16.

Status: **frozen before every registered seed and factorial response**. This
is a deliberately nonphysical system-identification branch. It is not Gate B
of the physical-mass claim ladder.

## 1. Dependency and claim scope

The prospective finite-\(H\) A2 certificate established a passive effective
center-port realization and authorized a separately labelled \(B^\ast\)
filter-scaling test. Physical Gate A nevertheless did not identify a natural
microscopic actuator. Therefore this protocol asks only:

> Under a newly declared effective center wrapper, does the weak nonlinear
> finite-memory response follow the filter coefficient
> \(m_{\rm filter}=\tau/\mu\) when memory time, input mobility and stored
> memory load are intervened on independently?

A pass is evidence about the implemented filter architecture. It cannot
establish material mass, a material center of mass, SI calibration, additive
momentum or an S1 mode.

The executable must verify the recorded A2 pass before opening a B-star
response. It must start from a clean Git revision.

## 2. Independently parameterized update

The physical/update time step is fixed at

\[
h=0.005.
\]

Memory time is varied through

\[
\lambda={h\over\tau},
\qquad
q=1-\lambda,
\qquad
H=\left\lceil{12\over\lambda}\right\rceil.
\]

The retained scalar-memory weights are

\[
w_j=M_0\lambda q^j,
\qquad j=0,\ldots,H-1,
\]

and the normalized finite-\(H\) center is read without a cellwise output
rescaling. The visible update is

\[
x_{n+1}
=x_n-\eta\nabla V_H(x_n)
+h\mu F_n e_1+\sqrt{2Dh}\,\xi_n.
\]

All cells use:

- \(D=10^{-4}\), dimension three and the fixed axis \(e_1\);
- \(A_{\rm rep}=1\), \(A_{\rm att}=35\),
  \(\sigma_{\rm rep}=1\), \(\sigma_{\rm att}=3\);
- one fixed \(\eta\), chosen once so that the baseline
  \((\tau,\mu,M_0)=(1,1,1)\) has local \(\kappa=4\);
- the same unit-area force rectangle of width 0.1;
- the same two absolute total-force impulses
  \(J\in\{5\,10^{-5},10^{-4}\}\);
- the same readout \(c_H\), coordinate unit and force unit.

In particular, \(\eta\), the applied force amplitudes and the readout scale
are not retuned after changing \(\tau\), \(\mu\) or \(M_0\).

At fixed \(\eta\), changing \(M_0\) changes the local relaxation
\(\kappa\). This is intentional. The filter prediction is

\[
m_{\rm filter}={\tau\over\mu},
\qquad
\gamma_{\rm filter}={1+\kappa\tau\over\mu},
\]

so \(M_0\) may change damping through \(\kappa\) while its exponent in the
inertial coefficient remains zero.

## 3. Generic estimator fixed before target data

For the untruncated local discrete plant, center velocity

\[
v_n={c_{n+1}-c_n\over h}
\]

obeys

\[
v_n=a v_{n-1}+bF_n,
\qquad
a=(1-\lambda)(1-h\kappa),
\qquad
b={h\mu\over\tau}.
\]

For every seed and impulse strength, ordinary least squares fits the generic
two-coefficient recurrence without inserting \(\tau\), \(\mu\) or \(M_0\).
The reported coefficients are

\[
\widehat m={h\over\widehat b},
\qquad
\widehat\gamma
=\widehat m\,{1-\widehat a\over h}.
\]

The exact normalized finite-\(H\) linear recurrence is evaluated separately.
It is an implementation reference, not a fitted rival. The finite-tail
normalization is allowed to perturb the two-coefficient reduction, but its
generic fit must remain within the registered tolerances below.

## 4. Factorial cells and sealed joint corner

The intervention levels are

\[
\tau,\mu,M_0\in\{0.5,2\}.
\]

The baseline \((1,1,1)\) and seven of the eight factorial corners form the
training panel. The single joint holdout is

\[
(\tau,\mu,M_0)_{\rm holdout}=(2,0.5,2).
\]

One common log-linear law is fitted on the eight training cells:

\[
\log\widehat m
=\beta_0+\beta_\tau\log\tau
+\beta_\mu\log\mu+\beta_M\log M_0.
\]

The filter predicts

\[
(\beta_0,\beta_\tau,\beta_\mu,\beta_M)=(0,1,-1,0).
\]

The holdout may be opened only after both training-estimand laws have been
computed. Fixed comparison predictions at the holdout are:

- constant filter mass: \(m=1\);
- material-load proportional: \(m=M_0\);
- loaded filter: \(m=\tau M_0/\mu\);
- registered filter: \(m=\tau/\mu\).

These are falsification references, not an exhaustive catalogue of material
models.

## 5. Two separately reported estimands

New B-star formation seeds are 26--30. The already sealed P0-M seeds 21--25
and the untouched P0 transfer cell
\((\alpha,C,H)=(0.003125,15,4800)\) remain unopened.

### State-matched estimand

For each seed, a baseline \((1,1,1)\) path is formed for 30 physical time
units. Its newest 4800 positions are retained procedurally. Every parameter
cell starts from the same current point and the newest \(H\) positions of
that seed, reweighted only according to the declared cell. No checkpoint is
selected by a response diagnostic.

### Reformed estimand

Each cell is independently formed from zero for 20 of its own memory times
under its own \((\tau,M_0)\), using common-random-number seed labels only for
variance reduction. The formation exceeds the 12-memory-time retained
horizon. A nonfinite, zero or nonlocal memory radius is a regime/validity
failure and is not removed from the regression.

Both estimands use mirrored plus/minus forces and common response noise.
Their odd response is divided by the actual fixed physical-force impulse.

## 6. Gates frozen before registered execution

Every threshold applies simultaneously to training and holdout unless stated
otherwise.

### V0: exact and numerical validity

- exact finite-\(H\) fitted mass and discrete damping each agree with the
  untruncated registered coefficient within 0.002;
- every OLS fit has rank two, \(0<a<1\), \(b>0\), condition number at most
  \(10^6\), and normalized residual at most 0.02;
- force-off cloned paths agree within \(10^{-14}\);
- all radii are positive and at most 0.03 in the fixed
  \(\sigma_{\rm rep}=1\) unit;
- every forced/control radius ratio lies in \([0.95,1.05]\);
- maximum mirrored even leakage is at most 0.01;
- maximum normalized difference between the two impulse-strength responses
  is at most 0.01.

A V0 failure is reported as invalid or regime-changing. The affected cell is
not dropped.

### V1: nonlinear finite-H embedding

For both estimands and every seed/strength/cell:

- inferred mass differs from the exact finite-\(H\) fit by at most 0.03;
- inferred discrete damping differs by at most 0.05.

### S: common scaling and joint holdout

For both estimands:

- training design rank is four;
- \(|\beta_0|\le0.05\);
- \(|\beta_\tau-1|\le0.08\);
- \(|\beta_\mu+1|\le0.08\);
- \(|\beta_M|\le0.08\);
- common-law holdout relative error is at most 0.05;
- fixed-filter holdout relative error is at most 0.03;
- fixed-filter holdout log-error is at most one third of the smallest log
  error among the three fixed rivals.

The state-matched and reformed median masses must also agree within 0.03 in
every cell.

## 7. Decision map and stop rules

- **B-star filter-scaling pass:** V0, V1 and S all pass.
- **B-star filter-scaling fail:** V0 and V1 pass but S fails.
- **B-star nonlinear-embedding fail:** V0 passes but V1 fails.
- **B-star regime-change-or-invalid:** V0 fails; no invalid cell is silently
  excluded.

In every outcome, physical B remains blocked by missing Gate-A microscopic
port selection. C, physical-work E and additive-mass F1 are not opened. The
S1 branch remains sealed because no S1 candidate exists.

## 8. Pre-freeze method-development disclosure

Before this protocol was frozen, only the following non-target method checks
were opened:

- ten unit tests covering parameter decoupling, invalid inputs, generic
  recurrence recovery, a nonregistered exact finite-\(H\) cell, common-law
  recovery, ring ordering and factorial rank;
- one nonlinear non-target pilot at
  \((\tau,\mu,M_0)=(0.8,1.25,0.7)\), seed 3.

That pilot returned theoretical mass 0.64, exact finite-\(H\) mass
0.6399964, nonlinear estimates 0.6399965, maximum fit residual
\(4.30\,10^{-8}\), radii 0.00642--0.00902 and forced/control radius ratios
0.99966--1.00036. It is method-training evidence only and is excluded from
every registered fit and decision.

No registered factorial response, seed 26--30, physical P0 holdout, S1
candidate trace or S1 method-validation holdout was opened before freeze.

## 9. Required record

The executable record must contain the clean revision, A2 dependency,
complete cell tuple, fixed thresholds, state digests, per-seed/strength fits,
training coefficients, fixed-rival errors, holdout results, old-seal flags
and the downstream claim boundary. Any change to cells, thresholds,
estimator, seed handling or decision logic after target execution makes the
result exploratory.
