# Critical review: P2-R sign-sensitive L3 long recovery

Date: 2026-08-25.

Verdict: **uphold `p2r-sign-sensitive-long-recovery-pass` as an
outcome-informed reconciliation of the P2 tail, without changing the
historical `loop-center-matrix-local-fail`.** All sixteen signed branches
continue to recover through 20 memory times. Every one of the 48 prospective
late windows has negative D0 slope, positive log-decay rate, a decreasing
ten-update envelope and large final-ratio margin.

Together with the original tangent and quadratic-remainder panels, this
supports a local matrix-valued Loop--Center response and return of one prepared
L3 loop. It does not transfer the scalar B-star filter mass, identify a
microscopic actuator, prove formation or provide an independent replication.

## 1. Prospective and historical integrity

The P2-R protocol was published before any L3 branch was advanced beyond the
old endpoint at update 2400. During implementation review, and still before
target access, a tautological reference to a future full-run peak was replaced
by the already published P2 checkpoint peak. The final protocol freeze is
revision `76145d7bd8ede06d5ae4f3a4166a452794a9e3ae`; the clean implementation
revision is `d5bedacd99f63fbe977943a16df92d8ff1f6f919`.

Before target access, 759 repository tests passed. The run used Python
3.12.13, NumPy 2.3.5 and SciPy 1.17.1, matching P1/P2. Candidate, kernel,
amplitudes, waveforms, signs, directions, drive length and port were unchanged.

The P2-R JSON has SHA-256
`484d0c614471980f81a242e3656ccea7793bd4c832f6138621cee575c36c1423`.
The original P2 JSON hash and decision are embedded unchanged.

## 2. Replay controls

The unchanged old P2 runner was executed first. All 120 scalar controls and
decision metrics reproduce exactly: the maximum error-to-tolerance ratio is
zero, and the replay again returns `loop-center-matrix-local-fail`.

The separately advanced long-recovery paths also reproduce maximum D0,
2400-update final/peak ratio and old absolute tail slope in all eight response
rows with zero recorded error. The extended probe-off D0 is
$1.89\times10^{-14}$ against a $9.45\times10^{-11}$ bound.

These are strong deterministic provenance controls. They are not independent
code implementations: both paths reuse the published native FIFO and D0
routines.

## 3. Prospective late-window result

There are two signs for each of eight response rows and three disjoint late
windows, hence 48 decisional windows. Their extrema are:

| window | signed slope per memory time | log-decay rate per memory time | largest ten-update change |
| --- | ---: | ---: | ---: |
| W1, updates 3201--3600 | $-1.1715\times10^{-4}$ to $-8.1168\times10^{-5}$ | 0.6358--0.6957 | $-2.5448\times10^{-2}$ to $-2.5021\times10^{-2}$ |
| W2, updates 3601--4000 | $-3.0233\times10^{-5}$ to $-2.2330\times10^{-5}$ | 0.7735--0.7771 | $-2.6260\times10^{-2}$ to $-2.4687\times10^{-2}$ |
| W3, updates 4001--4400 | $-5.7113\times10^{-6}$ to $-4.7129\times10^{-6}$ | 0.6529--0.6688 | $-2.4985\times10^{-2}$ to $-2.4768\times10^{-2}$ |

Every slope is negative. Every stored ten-update change is also negative, not
merely below the allowed 1% increase. The log rates remain inside the frozen
0.2--1.5 interval with wide margin.

At update 4400 the final D0 ratios are only

$$
3.5287\times10^{-6}
\le \frac{D_{4400}}{D_{\max,2400}}
\le 4.4103\times10^{-6},
$$

against a $5\times10^{-4}$ ceiling. The smallest W3 signal is still
$3.53\times10^{-6}$ of the checkpoint peak, 353 times the registered
$10^{-8}$ numerical floor. No decision is a threshold contact.

## 4. Relation to P1 and to linearization

The late log rates 0.636--0.777 bracket the independently measured P1 leading
transverse memory-time rate 0.702553. This is compatible with stable mode
decay but does not identify one unique pole: the W1, W2 and W3 ranges differ
systematically, as expected for a mixture of delayed modes and a norm rather
than a signed eigen-coordinate.

The result therefore strengthens the local stability/response reading, not a
single second-order mass law. The original P2 already showed that the
single-sign nonlinear remainder is quadratic and at most
$7.4\times10^{-5}$ relative. P2-R extends only the recovery time; it adds no
larger-amplitude or noncircular initial condition.

## 5. Why this is not sixteen independent confirmations

The model is deterministic. The three primary amplitudes lie in a regime that
collapsed to the same normalized response, plus/minus branches are symmetry
controls, and both directions share one prepared history. Counting 16 arms as
independent samples would be incorrect.

The genuine additions are narrower:

- three previously unseen time windows beyond the failed endpoint;
- a sign-sensitive distinction between convergence and outward drift;
- a waveform holdout under the same extended observation;
- a numerical-floor check that keeps the final sign measurement resolved.

Because the follow-up was motivated by the observed negative P2 tail, it is
outcome-informed. It should be reported as reconciliation, not fresh
validation or a successful rerun of the original gate.

## 6. Surviving falsifiers and claim boundary

1. Every run begins from the exact prepared circle. P2-R says nothing about
   attraction from a noncircular history or chirality selection.
2. The amplitude ceiling is $10^{-4}R$. A larger but still bounded response
   regime and a finite basin remain unmeasured.
3. The tangent transfer is matrix valued and anisotropic. It does not equal
   the former positive-$g_H$ scalar Center plant; at L3 the origin gain is
   negative.
4. The additive visible-state input is only an effective port. Gate A's
   microscopic work ambiguity remains.
5. The full FIFO spectrum is not enclosed, and other certified ladder cells
   remain stability- and response-untested.
6. No noise, formation holdout, second interval backend, physical time or SI
   calibration is added.

## 7. Reviewer decision and downstream consequence

No replay, numerical-floor or scientific recovery gate fails. The P2-R pass
is upheld with the exact statement:

> Conditional on the already prepared L3 rotating wave and the declared weak
> effective input, all registered signed branches continue to return in D0
> through 20 recovery memory times, with negative late slopes and resolved
> positive log-decay rates in all prospective windows.

The historical P2 fail remains part of the evidence record: its endpoint was
not flat enough under the original absolute-slope rule. P2-R resolves the
scientific drift-versus-decay ambiguity but does not rewrite that protocol.

Under the updated project sequence, P3 may now be designed for formation and
a bounded basin at the unchanged L3 parameters. This authorization concerns
the prepared-loop programme only. Physical Center conjugacy, filter-mass
transfer, work and interaction remain sealed.
