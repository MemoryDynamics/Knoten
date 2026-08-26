# Prospective P2 gate: local Loop--Center response at L3

Date: 2026-08-25.

Status: **frozen before any forced L3 Loop--Center response is opened.**

This protocol follows the linearization audit dated 2026-08-25. It tests the
full nonlinear finite-memory map against its independently constructed tangent
response at the already frozen L3 rotating wave. It does not test the
analytically ineligible scalar-origin center closure.

## 1. Question and claim boundary

Primary question:

> Does the exact nonlinear L3 loop have a phase-covariant, locally linear
> center response under the declared weak effective port while its quotient
> loop state remains bounded and returns after the probe?

A pass establishes a local matrix-valued Loop--Center compatibility result for
one prepared relative equilibrium. It does not establish formation, a finite
basin, a microscopic center-conjugate actuator, physical work, material mass,
an internal $S^1$, or interaction between two loops.

The exact identity $c_H=B_Hx$, group covariance, and agreement of a
differentiable map with its derivative as amplitude tends to zero are not
alone scientific pass evidence. The decisional content is the preregistered
finite amplitude window, waveform holdout, nonlinear remainder scaling and
recovery of the loop-relative state without fitting response parameters.

## 2. Frozen provenance and candidate

The candidate is the P1 L3 cell, without retuning:

$$
(\alpha,H,\eta)=(0.005,2400,0.075),
\qquad M_0=1,
$$

$$
(\sigma_{\rm rep},\sigma_{\rm att})=(1,3),
\qquad
(A_{\rm rep},A_{\rm att})=(1,3.5),
$$

$$
R=0.944805811705743656419366118422595657454474452804188781825799206245348464567689511866917417017911971955244464,
$$

$$
\theta=0.00790666146243552374938496703030974246197803459527409259815696583141708245813094145986593003659167675765833059.
$$

The selection base is main revision
`b5a6af5d717903d8111608b776dfefd39ab6541e`. The runner must require the P1
result, its reviewed pass decision, the candidate decimals and the native
map/Jacobian source blobs to match frozen hashes. A dirty pre-run worktree,
changed dependency, or changed candidate makes the target run invalid.

No L3 force-response trace, amplitude comparison, center-response transfer or
quotient recovery panel may be inspected before the protocol freeze commit is
published.

## 3. Exact readout and rejected scalar comparator

The normalized finite-memory center is

$$
c_H(Y)=C_HY
=\sum_{j=0}^{H-1}
\frac{\alpha q^j}{1-q^H}x_{n-j},
\qquad q=1-\alpha.
$$

The runner must record the direct finite sum and independent retiring-sample
recurrence error. This is a structural control only.

Before any target response, the runner must evaluate

$$
\kappa_K=\frac{A_{\rm att}}{\sigma_{\rm att}^2}
-\frac{A_{\rm rep}}{\sigma_{\rm rep}^2},
\qquad
g_H=\eta M_0(1-q^H)\kappa_K,
$$

$$
a_0=q(1-g_H).
$$

The scalar-origin comparator is eligible only if $0<g_H<1$ and
$|a_0|<1$. Its failure at the frozen parameters is an analytic
`scalar-origin-ineligible` result and may not be repaired by fitting a new
$g_H$ to the target trace.

## 4. Declared effective input

The only probe is the additive input already used by the center programme:

$$
x_{n+1}
=x_n-\eta\sum_{j=0}^{H-1}w_j
\nabla K(x_n-x_{n-j})+\alpha f_n.
$$

It is causal and acts on the visible update. For this P2 gate it is a declared
effective input; Gate A showed that the same state equation does not identify
whether microscopic work is conjugate to $x$ or $c_H$. No work ledger is a
P2 decision observable.

The laboratory probe direction is fixed during a run. Two initial
orientations are tested: radial and tangential relative to the visible point
of the unforced loop. In the co-rotating implementation the corresponding
input at update $n$ is

$$
u_n=\mathcal R(-(n+1)\theta)f_n.
$$

The extra one-step rotation follows from adding $\alpha f_n$ before the
output history is rotated into frame $n+1$. No measured phase or
response-dependent alignment is used.

## 5. Frozen waveforms, amplitudes and duration

The primary zero-sum waveform has $L_p=400$ updates:

$$
s_n=\sin\left(\frac{2\pi(n+1/2)}{L_p}\right),
\qquad 0\le n<L_p.
$$

The waveform holdout is the concatenation of a positive and negative
half-sine-squared lobe of 200 updates each:

$$
h_k=\sin^2\left(\frac{\pi(k+1/2)}{200}\right),
\qquad
s=(h_0,\ldots,h_{199},-h_0,\ldots,-h_{199}).
$$

Both sums must be below $10^{-13}$ in absolute binary64 arithmetic after
construction. The force is

$$
f_n=\epsilon R s_n d,
$$

with $d$ the registered laboratory unit direction. The primary amplitude
fractions are

$$
\epsilon\in\{10^{-5},3\times10^{-5},10^{-4}\}.
$$

Both signs are run independently. The waveform holdout uses only
$\epsilon=3\times10^{-5}$ and both directions/signs. Every branch runs 400
driven updates plus 2000 probe-off recovery updates. The exact probe-off clone
is advanced alongside all branches. Metrics use every update; the report may
thin displayed traces to every tenth update.

## 6. Predictor fixed before target data

Let

$$
J_*=D\widetilde{\mathcal G}(Y_*)
$$

be the analytic full-FIFO Jacobian already used by P1. For the known input
sequence, the prediction is generated only by

$$
\delta Y_{n+1}^{\rm lin}
=J_*\delta Y_n^{\rm lin}+E\alpha u_n,
\qquad
\delta Y_0^{\rm lin}=0,
$$

and

$$
\delta c_n^{\rm lin}=C_H\delta Y_n^{\rm lin}.
$$

No coefficient, pole, phase, gain, damping rate, time shift or normalization
is estimated from a nonlinear target branch. The nonlinear and tangent paths
must share only the frozen equations and inputs.

## 7. Structural and implementation controls

All controls are necessary:

1. unforced co-rotating fixed-point error at most $10^{-14}$ per component;
2. analytic Jacobian versus centered finite difference in the unrelated
   $H=17$ control, relative error at most $2\times10^{-9}$;
3. direct center versus the finite-$H$ retiring-sample recurrence, maximum
   error at most $5\times10^{-13}R$;
4. native forced-update rotation covariance at phases
   $0,\pi/2,\pi,3\pi/2$, maximum normalized mismatch at most $10^{-11}$;
5. probe-off quotient distance at the final update at most $10^{-10}R$;
6. finite values and complete traces for every registered branch.

The phase panel rotates initial history, laboratory probe and measured center
together. It checks covariance, not isotropy. Radial-versus-tangential
differences remain allowed and are reported.

## 8. Decisional response metrics

For mirrored branches define, relative to the numerical probe-off clone,

$$
\delta Y_{\rm odd}
=\frac{Y_+-Y_-}{2},
\qquad
\delta Y_{\rm even}
=\frac{Y_++Y_-}{2}-Y_0.
$$

State RMS values use the normalized finite-memory weights, with the visible
sample included once. Center velocity is the first difference of the
probe-induced laboratory center displacement divided by $\alpha$.

For both directions and all primary amplitudes:

- tangent error of the odd state response at most `0.005` relative RMS;
- tangent error of the odd center-velocity response at most `0.005` relative
  RMS;
- even state leakage at most `0.02` of the odd state RMS;
- single-sign first-order remainder at most `0.02` of the tangent state RMS;
- normalized odd-response collapse across the three amplitudes at most
  `0.005` relative RMS;
- center-velocity tangent signal at the smallest amplitude at least
  $10^{-3}\epsilon R$ RMS, otherwise the corresponding channel is
  `inconclusive` rather than pass.

For each direction, fit no model parameter but compute the log--log secant
slope of the single-sign state remainder between the two largest amplitudes.
It must lie in $[1.5,2.5]$, consistent with a leading quadratic remainder.

The waveform holdout must meet tangent errors at most `0.01`, even leakage at
most `0.03`, and finite complete traces. It is not used to change any primary
threshold.

## 9. Loop preservation and recovery

At every update compute the established D0 proper-rotation/translation
quotient distance from the unforced circular history. For every nonzero arm:

- maximum D0 distance at most $0.01R$;
- final D0 distance at most `0.05` times that arm's maximum D0 distance;
- absolute slope over the final 400 updates at most $10^{-3}$ of the arm's
  maximum D0 distance per memory time.

A permanent common translation is not a failure because D0 quotients it out.
A persistent relative deformation, phase-unquotiented reflection or secular
relative drift is a failure.

## 10. Decision semantics

- **`loop-center-matrix-local-pass`:** every control, primary metric, holdout
  metric and recovery gate passes.
- **`loop-center-matrix-local-fail`:** all required traces are valid but at
  least one decisional tangent, remainder, covariance or recovery criterion
  fails.
- **`loop-center-matrix-local-inconclusive`:** missing/nonfinite branches,
  signal below the registered floor, provenance failure or numerical control
  failure prevents a scientific decision.

The scalar-origin decision is reported separately as either eligible or
`scalar-origin-ineligible`. A matrix-local pass cannot convert that scalar
decision into a pass and cannot transfer the B-star filter-mass claim to L3.

Only a reviewed matrix-local pass may advance the prepared-loop branch to P3
formation/Basin testing. P4 remains responsible for a microscopic reciprocal
center-conjugate actuator and its work ledger.
