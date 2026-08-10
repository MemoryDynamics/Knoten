# Vector-memory source eligibility preregistration

Date: 2026-08-07.

## Question

Does the full retained persistent oriented-memory fibre of mature scalar source
states contain a bounded polar moment or antisymmetric circulation moment that
is separated from depositwise random signs and keeps a stable late-time axis?

This is a source-local eligibility gate. It is not a spin, charge, flavor,
particle, wave or QFT test.

## Frozen inputs

- six independent baseline checkpoints in \(d=3\), formed to \(N=3{,}000{,}000\);
- scalar formation parameters unchanged;
- \(\lambda_v=\kappa=\alpha=0.01\);
- \(M_v=1\);
- 20 vector-memory times, equal to 2,000 updates;
- 100 linear trace intervals including both endpoints;
- 256 independent deposit-sign randomizations per sampled state;
- random-null quantile \(q=0.99\);
- late window: final half of the continuation.

All retained positions, orientations and weights enter each observable.
Carrier-only summaries are insufficient.

## Observables

The two primary channels are:

\[
P_n=M_H^{-1}\sum_j w_jp_{n-j},
\]

\[
L_n=M_H^{-1}\sum_jw_j
\left[
r_j\otimes p_{n-j}-p_{n-j}\otimes r_j
\right],
\qquad
r_j=x_{n-j}-c_v.
\]

For each channel report:

1. median late-time observed coherence divided by its statewise random-sign
   \(q=0.99\);
2. cosine between mean axes in the first and second halves of the late window;
3. coefficient of variation of the moment norm in the late window;
4. source vector-radius drift and scalar shape-spectrum drift.

## Fixed gates

A seed passes a channel only if all conditions hold:

\[
\operatorname{median}
\left(
\frac{C_{\rm observed}}{C_{\rm null,q99}}
\right)
\ge2,
\]

\[
\cos(\bar A_{\rm late,1},\bar A_{\rm late,2})\ge0.8,
\]

\[
\mathrm{CV}(\lVert A\rVert)_{\rm late}\le0.5,
\]

\[
\max\left|R_v/R_{v,0}-1\right|\le0.5,
\qquad
\max\lVert s_n-s_0\rVert_2\le0.25.
\]

Polarization and circulation are decided separately. A channel passes the
campaign at 5/6 passing seeds.

## Interpretation and stop rules

- Polarization pass: the explicitly inserted persistent carrier is a viable
  directed source state under these controls.
- Circulation pass: the full-memory bivector is eligible for a later
  interaction experiment.
- Channel fail: do not tune \(\lambda_v\), \(\kappa\), \(M_v\), thresholds or
  seeds post hoc. Revisit the update law before another campaign.
- No outcome authorizes physical spin, charge or flavor language.
- No self-force, reciprocal coupling or vector-field PDE is added in this
  gate.