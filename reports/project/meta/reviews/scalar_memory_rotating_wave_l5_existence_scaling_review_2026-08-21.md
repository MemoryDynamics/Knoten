# Critical review: L5 rotating-wave existence and scaling

Date: 2026-08-21.

Verdict: **accept the registered L5 result as a scoped computer-assisted
continuation and scaling pass.** The sixth matched finite-memory cell has a
locally unique reduced balance root in every declared interval box, conditional
on the stated `mpmath.iv` trust base, and all prospective first-order
discriminators pass. This is not yet an independently verified interval proof,
a stable six-cell family, an internal phase or an interaction result.

## 1. Prospective and provenance integrity

The complete question, model, transfer center, branch corridor, Newton count,
precision panels, interval boxes, replay thresholds, continuum target, scaling
ratios and decision semantics were committed as revision
`0add69c9898802f192984975786147429586fd8c` before L5 was evaluated. Its CI
run `32524691166` passed. The protocol is byte-unchanged between that revision
and the execution revision.

The runner and eight synthetic or off-target tests were committed separately
as revision `a8787cdefd12b86e13928613790708883e2c55e1`. CI run `32525422539`
passed lint, the full test suite and strict documentation build before target
execution. The L5 run then began from exactly that clean revision and recorded
an empty start status.

All three immutable source objects match their canonical `HEAD:path` Git-blob
SHA-256 values. The historical L0--L4 and foundation execution revisions exist
as ancestors, the stored L4 center equals the registered transfer center, and
exact decimal arithmetic gives

$$
9600(0.00125)=12,
\qquad
0.01875/0.00125=15.
$$

No amplitude, kernel width, gain, horizon scaling, start, box, threshold or
iteration count changed after seeing L5.

## 2. Local finite-H existence result

Both precision panels converge to

$$
R_5=
0.9435346582358031088217231552950418443390740780038804564789135709628825
\ldots,
$$

$$
\theta_5=
0.00198064482941032663656202703595953628551222175482933927695406633501006
\ldots,
$$

or

$$
\Omega_5=\theta_5/\alpha=
1.584515863528261309249621628767629028409777403863471421563253068008048
\ldots.
$$

The 80- and 120-digit centers differ by
$2.50\times10^{-69}$ in radius and $5.20\times10^{-68}$ in angular
frequency, below the registered $10^{-55}$ tolerance. Point residual maxima
are $4.12\times10^{-84}$ and $1.13\times10^{-123}$.

Every outer and inner box passes the physical domain, nonsingular
preconditioner, balance containment, component signs, registered radial and
tangential gains, and strict Krawczyk interior inclusion. In the outer box,
the Krawczyk-image widths are only $2.11\times10^{-5}$ and
$8.16\times10^{-5}$ of the radius and angle box widths. The nearest image
boundary remains about $0.49996$ box widths from an outer boundary. Thus the
pass is not a rounding-level contact with the inclusion threshold.

The largest Newton excursions are $4.23\times10^{-4}$ in radius and
$1.06\times10^{-3}$ in frequency, versus registered corridor half-widths
$0.01$. No iterate approaches a branch-corridor boundary.

Strict Krawczyk inclusion establishes existence and uniqueness **inside each
declared local box** for the exact reduced finite sum. It neither counts nor
excludes roots elsewhere in parameter or state space.

## 3. Independent finite-sum replay

The separately coded 70-digit direct summation gives

$$
A_H=1.04612070874828306168124441027\times10^{-4}>0,
$$

$$
S_H=-0.105634321835422631753216815412<0.
$$

Its maximum balance residual is $1.30\times10^{-72}$ and the maximum error
of the two independently reconstructed gains relative to $0.01875$ is
$1.24\times10^{-68}$. An off-target unit test at $H=17$ agrees with the
native production residual convention. This makes a shared sign, age-index or
weight error between the interval evaluator and replay unlikely.

The replay is still point arithmetic using the same elementary-function
library. It is an implementation control, not a second interval certificate.

## 4. Prospective scaling discrimination

Against the independently reconciled fixed-gain continuum root, the L4-to-L5
absolute errors contract as follows:

| observable | L4 error | L5 error | signed error ratio | successive-difference ratio |
| --- | ---: | ---: | ---: | ---: |
| $R$ | $8.43882\times10^{-4}$ | $4.21351\times10^{-4}$ | 0.499302 | 0.497901 |
| $\Omega$ | $2.11191\times10^{-3}$ | $1.05421\times10^{-3}$ | 0.499176 | 0.497532 |

Errors decrease strictly across L0--L5. The L1--L5 log-log slopes are
1.00738 for radius and 1.00862 for frequency. Last-pair Richardson relative
errors are 0.00280 and 0.00330. Every value lies comfortably within its
prospective interval; in particular, the signed gates exclude a hidden target
crossing.

This is strong finite-sequence evidence for first-order approach along the
registered $H\alpha=12$, $\eta/\alpha=15$ path. Six cells do not prove an
all-$\alpha$ asymptotic theorem. Fixed $H\alpha=12$ also does not test either
$H\to\infty$ at fixed $\alpha$ or tail extent $C=H\alpha\to\infty$.

## 5. Is the Krawczyk certificate itself verified?

There are three distinct levels and only the first two are present:

1. **The theorem condition is checked:** exact binary interval endpoints are
   archived, the analytic interval Jacobian is evaluated on each box, the
   point preconditioner is nonsingular, and
   $K(X)\subset\operatorname{int}(X)$ is strict.
2. **The implementation has controls:** the analytic Jacobian, native
   residual convention, point-in-interval enclosure and a known polynomial
   Krawczyk example have regression tests; two precisions and a separate
   finite-sum replay agree.
3. **The trust base is not independently verified:** both certificate panels
   use `mpmath.iv` 1.3.0 and the same analytic code. There is no Lean/Coq
   proof, standalone certificate checker, or replay in Arb/MPFI/another
   outward-rounded interval library.

Consequently, “computer-assisted local proof conditional on `mpmath.iv`” is
accurate. “Formally verified Krawczyk proof” or “independently certified
theorem” is not. A publication-strength hardening step should replay at least
the L5 outer and inner boxes in a second validated interval backend while
retaining these exact binary endpoints and formulas. This limitation does not
change the registered project decision, but it constrains its wording.

The continuum target is also a two-quadrature 70-digit numerical root, not an
interval enclosure. The target-independent difference-ratio gate reduces but
does not eliminate that separate trust dependency.

## 6. Topology, spin language and interactions

An additional internal $S^1$ is not a prerequisite for the current existence
or scaling statement. The demonstrated object is a rotating relative
equilibrium whose continuous family of rotated copies is the ambient
$SO(2)$ group orbit; after quotienting that symmetry, the registered D0 object
is a point.

A torus would not remove topology: it is $S^1\times S^1$ and requires two
independent windings plus an embedding or field architecture that preserves
them. A periodic field or a visual “circle on a circle” does not by itself
establish an invariant torus, confinement or stability. The tokamak analogy
also imports externally maintained fields and currents absent from the native
scalar-memory model.

The current evidence may be described as a prepared chiral spatial loop or
rotating relative equilibrium. Calling it intrinsic spin would require a
quotient-space observable and transformation law not yet demonstrated.
Interactions remain sealed: adding a second loop now would confound source
existence, stability, formation and coupling.

## 7. Sequential recommendation

The machine decision `l5-existence-scaling-pass` is upheld. Repository status
may advance from five to six locally existence-certified matched cells.

The next scientific gate is exactly one prospectively selected non-Anchor
stability cell. The cell choice, Arnoldi panels, perturbations, horizon,
failure semantics and computational stopping rules must be frozen before any
new spectrum is evaluated. A pass would remain local numerical stability
unless the full spectrum is enclosed.

Second-backend interval replay is a parallel publication-hardening task, not
permission to skip that stability sequence. Formation and basin tests remain
downstream of non-Anchor stability; topology, toroidal architecture, mechanics
and interactions remain separate programs.
