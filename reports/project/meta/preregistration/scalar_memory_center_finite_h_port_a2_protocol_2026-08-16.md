# Preregistration: finite-H reciprocal center-port Gate A2

Date: 2026-08-16.

Status: frozen before evaluation of the registered finite-\(H\) transfer.
No stochastic target trace, new formation seed or sealed P0 transfer cell may
be opened by this protocol.

## Question and scope

The claim-scoped center P0 passed, while physical Gate A did not identify a
microscopic port. The same additive term in the \(x\) equation is compatible
with both a conditional \(x\)-work ledger and an effective center-conjugate
realization. This follow-up asks the narrower unresolved question:

> Does the native finite-\(H\) local center plant itself admit an exact passive
> input/output port with supply \(u_n\cdot(c_{n+1}-c_n)\), including its
> finite-memory tail, or is passivity only a continuum approximation?

A pass establishes a physically realizable **effective port wrapper**. It
does not select a natural microscopic actuator, turn the occupancy history
into conserved matter, or establish physical/additive mass.

## Frozen candidate and cells

- Candidate: `scalar-memory-center-effective-mechanics-v1`.
- Architecture tested internally: unchanged K0 scalar memory, linear local
  slice.
- External wrapper if the plant passes: reciprocal discrete-gradient
  interaction `new:K0-center-reciprocal-port-v1`.
- \(\alpha\in\{0.04,0.02,0.01,0.005,0.0025\}\).
- \(H=\lceil12/\alpha\rceil\), \(q=1-\alpha\), \(g=4\alpha\).
- No noise, nonlinear response, state formation or force profile is used.
- The P0 holdout \((\alpha,C,H)=(0.003125,15,4800)\) remains sealed.

The registered cells are already discovery cells. The test is analytic and
may not be used as confirmatory evidence for unseen-parameter transfer.

## Exact transfer

For

\[
B_H(z)={\alpha\over1-q^H}
{1-q^Hz^{-H}\over1-qz^{-1}},
\]

the transfer from the registered input \(u_n\) to native center velocity
\(y_n=(c_{n+1}-c_n)/\alpha\) is

\[
G_H(z)={(z-1)B_H(z)\over z-(1-g)-gB_H(z)}.
\]

The untruncated reference is

\[
G_\infty(z)={\alpha z\over z-a},
\qquad
a=q(1-g),
\]

with the global unit-circle bound

\[
\min_{|z|=1}\Re G_\infty(z)={\alpha\over1+a}>0,
\qquad
\max_{|z|=1}|G_\infty(z)|={\alpha\over1-a}.
\]

Write

\[
B_H=B_\infty(1+s),
\qquad
s={q^H(1-z^{-H})\over1-q^H}.
\]

Then

\[
{G_H\over G_\infty}={1+s\over1-R},
\qquad
R={gG_\infty s\over z-1}.
\]

The registered uniform bounds are

\[
|s|\le {2q^H\over1-q^H},
\]

\[
|R|\le r_H
={g\alpha\over1-a}{Hq^H\over1-q^H},
\]

and, if \(r_H<1\),

\[
|G_H-G_\infty|
\le {\alpha\over1-a}
{2q^H/(1-q^H)+r_H\over1-r_H}
=E_H.
\]

Therefore

\[
\Re G_H\ge {\alpha\over1+a}-E_H.
\]

The same \(r_H<1\) is a stable small-gain certificate for the finite-tail
feedback correction. It includes the delayed retiring-history term rather
than dropping it.

## Reciprocal external interaction

If the plant certificate passes, an external coordinate \(Q\) may be coupled
through a declared interaction \(U_{\rm ext}(c_H,Q)\) using a discrete
gradient. The discrete gradients are chosen so that

\[
\Delta U_{\rm ext}
=\bar\nabla_cU_{\rm ext}\cdot\Delta c_H
+\bar\nabla_QU_{\rm ext}\cdot\Delta Q.
\]

The center input and external generalized force are

\[
u_n=-\bar\nabla_cU_{\rm ext},
\qquad
F_{Q,n}=-\bar\nabla_QU_{\rm ext}.
\]

Thus interaction work cancels exactly between the two subsystems. For the
bilinear example \(U_{\rm ext}=-k c_H\cdot Q\), midpoint discrete gradients
give \(u_n=k\bar Q\) and \(F_{Q,n}=k\bar c_H\). This wrapper is an explicit
new external-system contract; it is not claimed to have been present in the
old prescribed-force experiment.

## Gates fixed before evaluation

For every registered alpha:

1. `small_gain_stability_pass`: \(r_H<1\);
2. `strict_positive_real_pass`:
   \(\alpha/(1+a)-E_H>0\);
3. `safety_factor_pass`:
   \([\alpha/(1+a)]/E_H\ge10\);
4. non-decisional numerical sanity checks on exactly 131073 equally spaced
   frequencies in \([0,\pi]\): the observed transfer error and loop gain may
   not exceed their analytic bounds by more than \(5\,10^{-13}\), and the
   sampled real part must remain positive.

The family passes only if every component passes for every alpha. The dense
frequency grid cannot rescue a failed analytic bound.

## Decision map

- **Pass:** exact finite-\(H\) passivity and a reciprocal effective wrapper are
  established for the local linear plant. This authorizes only a separately
  labelled \(B^\ast\) filter-scaling study.
- **Fail:** the center inertial port remains a continuum/local approximation;
  neither \(B^\ast\) nor physical B is opened by this route.
- **In either case:** physical B, C, physical-work E and additive-mass F1
  remain blocked because no natural microscopic actuator or material COM has
  been selected. D0--D5 remain sealed because no S1 candidate exists.

## Required outputs

The executable record must include the clean Git revision, every analytic
bound, the non-decisional grid diagnostics, the untouched-holdout flags and a
machine-readable downstream decision. Any threshold or formula change after
opening the registered transfer values makes the run exploratory.
