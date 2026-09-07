# Finite-H non-tautology and horizon-transfer audit

Date: 2026-09-07.

Verdict: **`finite-h-loop-nontautological-horizon-transfer-open`**.

The retained FIFO does not encode a spatial circle and the certified roots
are nontrivial rotating relative equilibria of the exact finite-$H$ map.
However, $H$ is a trajectory-tail truncation inherited from the numerical
backend, not a dynamical field derived by the Paper-I equations. Existing
matched-$H\alpha$ evidence does not establish persistence at
$H\to\infty$ for fixed $\alpha$. A broad mainline or Paper-I loop claim
therefore needs a separate prospective horizon-transfer gate.

This is a target-free equation and evidence audit. It does not evaluate a new
trajectory, change a parameter, authorize P5-D attempt 4 or reinterpret any
previous P5-D infrastructure incident.

## 1. Where H enters

The Paper-I memory law is

$$
\rho_{n+1}=q\rho_n+\alpha M_0\delta(\mathord\cdot-x_{n+1}),
\qquad q=1-\alpha.
$$

After $n$ updates, exact iteration gives

$$
\rho_n=q^n\rho_0+\sum_{j=0}^{n-1}\alpha M_0q^j
\delta(\mathord\cdot-x_{n-j}).
$$

For a stationary bi-infinite history, the decaying initial term is replaced
by the absolutely summable continuation over all $j\ge0$. Thus $\alpha$ sets
forgetting. The ideal recursion itself contains no finite horizon. The
production trajectory backend represents that history by

$$
\rho_n^{(H)}=\sum_{j=0}^{H-1}\alpha M_0q^j
\delta(\mathord\cdot-x_{n-j}),
$$

with

$$
H=\min\!\left(H_{\max},
\max\!\left[1,\left\lfloor C_{\rm mem}/\alpha\right\rfloor\right]
\right).
$$

$C_{\rm mem}$ and $H_{\max}$ are backend or experiment-design choices. They
are not new fields and are not selected by the dynamics. The rotating-wave
branch registers $H$ directly and calls the exact truncated system K0-H.

## 2. Why a ring-buffer implementation does not insert a spatial ring

Logical FIFO ages obey

$$
Y_n=(x_n,x_{n-1},\ldots,x_{n-H+1}),
$$

$$
Y_{n+1}=(x_{n+1},x_n,\ldots,x_{n-H+2}).
$$

The oldest point is discarded. It is not coupled back to the newest point.
A circular array index is only an implementation of this shift without
copying memory; it imposes no periodic boundary condition on $x$ and no
spatial relation between slots zero and $H-1$.

The same storage can contain a point, line, hook, ellipse, cloud or circular
history. On a proposed circle, the native nonlinear update still has to
satisfy two independent equations,

$$
F_R=\cos\theta-1+\eta A_H(R,\theta)=0,
\qquad
F_T=\sin\theta+\eta S_H(R,\theta)=0.
$$

Neither equation follows from the FIFO shift. The age-dependent kernel factor
also prevents the full force from reducing to the geometric center filter
$B_H(e^{i\theta})$.

## 3. Existing evidence against the narrow tautology

Three existing results discriminate a dynamically supported finite-$H$ loop
from a loop merely written into the initial buffer:

1. Krawczyk inclusions certify local zeros of both exact finite sums, not only
   the geometric construction of a circular history.
2. In the P3 $\eta=0$ control, the initially stored history collapses after
   one FIFO horizon and does not remain a loop. Memory replacement alone is
   therefore insufficient.
3. All ten registered chiral noncircular P3 arms approach the L3 rotating
   group orbit. Four arise from a wrong-rate ellipse and a damped hook that
   contain neither the target radius nor target angular increment. The
   exactly achiral collinear control remains collinear and does not form a
   chiral loop.

These facts rule out the claim that the positive finite-$H$ result is just a
circular initialization replay. They establish only a finite deterministic
ensemble, not generic formation or horizon independence.

## 4. What the exponential tail currently justifies

The omitted stationary memory mass is exact:

$$
\sum_{j=H}^{\infty}\alpha M_0q^j=M_0q^H.
$$

At the registered matched extent $H\alpha=12$, it is

| cell | $\alpha$ | $H$ | $q^H$ |
| --- | ---: | ---: | ---: |
| Anchor | 0.01 | 1200 | $5.7841\times10^{-6}$ |
| L3 | 0.005 | 2400 | $5.9620\times10^{-6}$ |
| L5 | 0.00125 | 9600 | $6.0983\times10^{-6}$ |

For the registered Double-Gaussian kernel, the triangle inequality gives the
global gradient bound

$$
\sup_r\lVert\nabla K(r)\rVert
\le e^{-1/2}\left(
\frac{A_{\rm rep}}{\sigma_{\rm rep}}+
\frac{A_{\rm att}}{\sigma_{\rm att}}
\right).
$$

At $(A_{\rm rep},A_{\rm att},\sigma_{\rm rep},\sigma_{\rm att})
=(1,3.5,1,3)$ this upper bound is $1.31415$. Consequently one truncated
position update differs from the corresponding infinite-history update by at
most

$$
\eta M_0q^H\,1.31415,
$$

which is $1.15\times10^{-6}$ at the Anchor,
$5.88\times10^{-7}$ at L3 and $1.51\times10^{-7}$ at L5 after rounding the
bound upward.

This is a useful uniform truncation estimate. It is not yet a root-transfer
theorem: a small residual perturbation can move or destroy a poorly
conditioned zero, and stability of a growing-dimensional delay state needs
more than a one-step force bound.

## 5. What remains unproved

The existing refinement ladder keeps $H\alpha=12$ while changing $\alpha$.
It tests discrete-step refinement at one fixed retained tail extent. It does
not test either

$$
H\to\infty\quad\text{at fixed }\alpha,
$$

or

$$
C=H\alpha\to\infty.
$$

The discovery protocol chose $C=12$ prospectively; the equations did not
derive that number. Its nonselecting $C=6$ sensitivity result is adverse
evidence against casual claims of horizon independence, even though it did
not alter candidate selection.

Current evidence therefore supports exactly: locally certified and sampled-
attracting loops of specified finite-$H$ maps. It does not yet support: the
same loop branch of the untruncated exponential-memory equation.

## 6. Required horizon-transfer falsification gate

Before a horizon-independent Paper-I claim or a further P5-D target
authorization, a prospective protocol should freeze:

1. a fixed-$\alpha$ horizon ladder around and above the current Anchor or L3,
   with $\eta$, $M_0$ and every kernel parameter held fixed;
2. local continuation only in $(R,\theta)$, with no parameter retuning and an
   explicit branch-loss verdict;
3. direct finite-sum replay plus interval enclosures at every registered
   horizon;
4. an infinite-sum residual enclosure using the analytic $q^H$ force and
   derivative tails, strong enough to transfer a nondegenerate root;
5. at least one stability discriminator at a previously unopened larger
   horizon, or a rigorous operator-tail argument if a full spectrum is not
   computationally proportionate;
6. FIFO-shift versus circular-index implementation equivalence and the
   existing $\eta=0$ collapse control;
7. an outcome rule that distinguishes branch persistence, branch drift,
   branch loss and numerical inconclusiveness.

Synthetic or reduced-balance success cannot be counted as P5 interaction
evidence. Conversely, failure of horizon transfer would not erase the exact
finite-$H$ theorem; it would confine the loop and every downstream P5 claim
to the explicitly truncated model.

## 7. Consequence for the active P5 path

The already reviewed target-free P5 production-path remediation may proceed:
it changes representation boundaries only and freezes the scientific runner.
No new P5-D target should be authorized merely because that infrastructure is
repaired. The horizon-transfer protocol and its result must first determine
whether attempt 4 would test a robust mainline memory mechanism or only the
registered K0-H specialization.

This ordering keeps the engineering repair useful while preventing a
successful finite-$H$ interaction payload from being overread as evidence for
the untruncated Paper-I model.
