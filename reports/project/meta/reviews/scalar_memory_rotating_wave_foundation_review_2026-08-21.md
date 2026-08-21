# Critical review: native rotating-wave foundation

Date: 2026-08-21.

Verdict: **accept into the main line as a scoped foundation for prepared
spatial loops.** Do not describe the result as a family of demonstrated
stable knots. Five local finite-H existence statements are computer-assisted;
only the anchor has strong local numerical stability evidence, and no tested
history has formed the loop generically.

## 1. Algebra and model identity

The circular ansatz is not an inserted harmonic oscillator. Substitution of
\(x_n=Re^{in\theta}\) into the native scalar finite-memory update gives two
exact finite sums. The signs are fixed by the production convention:

\[
F_R=\cos\theta-1+\eta A_H=0,
\qquad
F_T=\sin\theta+\eta S_H=0,
\]

so positive gain requires \(A_H>0\) and \(S_H<0\). Unit tests compare the
compact formula with an explicit production-kernel history, and the new
independent multiprecision replay reproduces all five certified centers with
maximum residual below \(8\times10^{-72}\). This makes a shared sign, age or
weight bug across the original floating-point and interval paths unlikely.

The notation has one historical blemish: the first continuum protocol called
the auxiliary squared half-chord \(q(t)\), while \(q=1-\alpha\) already denotes
forgetting. Frozen protocols retain that text for provenance. Active code and
documentation now use \(\chi(t)=R^2[1-\cos(\Omega t)]\).

The geometric filter \(B_H\) remains useful but must not be oversold. It is an
exact finite geometric series for the normalized **linear center**. The full
rotating-wave force also contains the age-dependent nonlinear factor
\(\varphi(r_j)\), so the complete circle balance does not collapse to one
\(B_H(e^{i\theta})\) evaluation.

## 2. Selection and multiplicity

Discovery prospectively fixed amplitudes, search boxes, quadrature orders,
finite parameters and controls. It first enumerated sign-changing continuum
radial roots, sorted admissible initializers by proximity to the already fixed
\(\eta/\alpha=15\), and accepted the first native finite-H residual root. The
selected point was subsequently frozen through P0 before stability work.

This is legitimate candidate discovery, but it is not amplitude selection by
the dynamics. The inventory contains hundreds of continuum radial roots, and
the result neither counts global finite-H roots nor proves uniqueness outside
the registered local boxes. The amplitude \(A_{\rm att}=3.5\) is a tested
parameter, not an emergent constant. The \(A_{\rm att}=7\) holdout remains
sealed.

## 3. Existence claims

The Anchor and four matched cells satisfy strict Krawczyk inclusions in their
registered neighborhoods. Within the trust base of `mpmath.iv` 1.3.0, this
is an exact existence-and-local-uniqueness statement for the reduced finite
sums. Because the circular history was substituted algebraically into the
native update, each root defines a rotating relative equilibrium of that exact
finite-history model.

The certificate is local. It does not exclude other branches, root folds or
coexisting circles. Both precision panels use the same interval library; they
are convergence controls, not independent formal proof assistants.

## 4. Continuum and refinement

The scaling

\[
\theta=\alpha\Omega,
\quad \eta=\alpha\widehat\eta,
\quad H\alpha=C
\]

has a singular radial balance: the leading \(O(\alpha)\) history term must
vanish before the \(O(\alpha^2)\) chord increment enters. This correctly
produces \(I_R=0\) and
\(\Omega+\widehat\eta I_T=0\); it does not produce an inertial equation.

The historical five-cell ladder failed its formal target rule because its
frozen continuum guide visibly belonged to gain 15.016345 rather than the
finite ladder's exact gain 15. That protocol defect is preserved as
`certified-roots-nonconvergent`. The later prospective reconciliation
changed the target definition, not a threshold or model parameter.

The foundation audit now solves the corrected continuum system independently
with 70-digit Tanh--Sinh and Gauss--Legendre quadrature. Both return

\[
R_\infty=0.9431133067695436321754560922\ldots,
\]

\[
\Omega_\infty=1.5855700777177887067789751487\ldots,
\]

and all original scaling gates pass. This strongly reduces quadrature and
implementation risk. It is still a numerical continuum root, not an interval
enclosure, and five cells do not prove convergence for all \(\alpha\).

Keeping \(H\alpha=12\) tests step refinement at one finite tail extent. It
does not establish the distinct limits \(H\to\infty\) at fixed \(\alpha\) or
\(C\to\infty\). The earlier nonselecting \(C=6\) mismatch remains adverse
evidence against casual horizon-independence language.

## 5. Stability claim

At the Anchor, the analytic sparse Jacobian of the full 2400-dimensional
co-rotating FIFO map reproduces the rotation and translation symmetry
directions. Two frozen Arnoldi panels agree on the leading reported
transverse pair,

\[
|\lambda_\perp|=0.993060347711\ldots<1,
\]

and three registered \(10^{-7}R\)-scale perturbations return to the numerical
floor. This is strong evidence for local transverse numerical attraction of
the prepared Anchor.

It is not a spectral theorem. ARPACK returned 24 and 36 largest-modulus Ritz
pairs rather than an enclosure of all 2400 multipliers. A non-normal delayed
map can also show transient behavior not summarized by eigenvalue moduli, and
only one deterministic full-history direction was continued. None of L0,
L1, L3 or L4 has a stability result.

Consequently, publication text may say “locally numerically stable prepared
Anchor” and “five locally existence-certified cells.” It may not say “five
stable loops” or “stable loop phase.”

## 6. Formation, topology and mechanics

Every stability trajectory begins near the exact prepared circular history.
No compact, random or noncircular memory has formed the orbit. Basin size,
chirality selection and noise robustness are unknown. The historical noisy
\(d=3,A_{\rm att}=3.5\) dispersive branch is not the same experiment, but it
remains adverse prior evidence against generic formation.

The continuous circle of globally rotated copies is the ambient \(SO(2)\)
group orbit. D0 correctly identifies that its symmetry quotient is a point.
Persistent homology of the unquotiented trajectory would rediscover this
known spatial symmetry and cannot establish an additional internal \(S^1\).

Finally, deposition and forgetting make the model an open source/sink system.
The rotating balance has no reciprocal actuator, work ledger, momentum or
mass normalization. A positive circle result neither proves center work nor
emergent inertia; the Center-port branch remains logically separate.

## 7. Audit-pipeline correction

The first foundation audit formally failed only because its implementation
compared binary `mpmath` values for exact equality in
\(\eta/\alpha=15\), contrary to the frozen requirement of exact decimal
arithmetic. Its numerical finite-sum, continuum and scaling checks all passed.
Its Markdown renderer also printed a positive paragraph unconditionally; the
JSON fail decision is authoritative.

Both defects are preserved in the initial implementation-fail artifacts. A
new protocol froze one computational correction, exact `Decimal` cross
products, plus a conditional rendering safeguard. The entire audit then ran
again from clean revision
`8e1cf13083d343cdebb0d7d315d34a017164c827` and all five composite gates
passed. No scientific threshold changed. This is an acceptable transparent
pipeline reconciliation, not a retroactive pass.

## 8. Main-line and publication recommendation

Main-line integration is scientifically justified with the claim boundaries
above. The result is already a credible hook for a technical publication on
computer-assisted rotating relative equilibria in a nonlinear finite-memory
map. A stronger word such as *stable family* should wait for at least one
prospective non-Anchor stability gate; a formation or phase claim needs a
separate basin experiment.

The next authorized computation is one prospective L5 existence/scaling cell

\[
(\alpha,H,\eta)=(0.00125,9600,0.01875).
\]

Only after an L5 existence pass should one preselect a non-Anchor stability
cell. Formation, noise, internal topology and mechanics remain downstream and
sequential.
