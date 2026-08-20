# D0 contract: scalar-memory rotating relative equilibrium

Date: 2026-08-20.

Decision:

- **D0-pass** for the object
  translation-reduced spatial rotating-wave group orbit;
- **D0-not-established** for an internal phase that survives quotienting
  ambient \(SO(2)\) rotations.

This contract is frozen after the zero-defect rotating-wave P0 and before any
candidate-targeted Jacobian, perturbation trajectory or topology calculation.

## 1. Native state and translation reduction

The finite native state is

\[
z_n=(x_n,h_{n,0},\ldots,h_{n,H-1}),
\qquad h_{n,0}=x_n.
\]

Let

\[
c(z)=\sum_{j=0}^{H-1}\bar w_jh_j,
\qquad
\bar w_j=\frac{\alpha q^j}{1-q^H}.
\]

The registered raw observable removes only common translation:

\[
\Psi(z)
=
\left(
x-c,\,
h_1-c,\ldots,h_{H-1}-c
\right).
\]

The redundant \(h_0=x\) component is omitted from the observable.

No angle, time coordinate, delay embedding, candidate covariance whitening,
Hilbert transform or topology-optimized projection is used.

The fixed metric is

\[
d^2(\Psi,\Psi')
=\lVert(x-c)-(x'-c')\rVert^2
+
\sum_{j=1}^{H-1}
\bar w_j
\lVert(h_j-c)-(h'_j-c')\rVert^2.
\]

All components retain the native coordinate unit. The age weights are fixed
by \(\alpha,H\), not estimated from the candidate.

## 2. Symmetry action

A common translation leaves \(\Psi\) invariant. For \(O\in O(2)\),

\[
\Psi(Oz)=O\Psi(z)
\]

componentwise, so the metric is rotation- and reflection-invariant.
Reflection maps the \(+\theta\) rotating wave to its \(-\theta\) partner.

Ambient rotations are deliberately not quotiented in the primary object.
They are the spatial phase being tested. If one instead takes the
\(SO(2)\)-quotient, the entire group orbit below becomes a single point.

## 3. Claimed object

Let \(z_\ast\) be the frozen exact circular history at phase zero and let
\(\mathcal R_\varphi\) rotate every native coordinate. The candidate set is

\[
\Gamma
=
\left\{
\Psi(\mathcal R_\varphi z_\ast):
\varphi\in[0,2\pi)
\right\}.
\]

Because the age-ordered candidate has no nontrivial rotational isotropy,
\(\varphi\mapsto\Psi(\mathcal R_\varphi z_\ast)\) is continuous and
injective modulo \(2\pi\). Thus \(\Gamma\) is a symmetry-generated copy of
\(S^1\).

Rotational equivariance and the exact one-step residual imply

\[
\mathcal F\Gamma(\varphi)
=\Gamma(\varphi+\theta).
\]

The restricted map has degree \(+1\); the reflected partner has degree
\(-1\).

This analytic group-orbit statement is not evidence that the knot carries an
additional internal phase after spatial orientation is removed. It is the
topology of a rotating spatial relative equilibrium.

## 4. Authorized next test

The next authorized target calculation is only a rotating-wave source
stability gate:

1. linearize the complete \(2H\)-dimensional FIFO map in the frame rotating
   by \(-\theta\);
2. verify the symmetry-neutral translation and rotation directions;
3. estimate every potentially leading transverse multiplier with convergence
   checks;
4. run deterministic radial, tangential and generic full-history
   perturbations without noise;
5. classify stable, unstable or numerically inconclusive.

This gate may establish transverse stability of the relative equilibrium. It
does not open D1--D5 for an internal-phase claim. Data-driven topology,
external phase coupling, noise and the \(A_{\rm att}=7.0\) holdout remain
sealed.

## 5. Falsifiers

The rotating wave fails the source-stability gate if any of the following
occurs:

- a nonsymmetry multiplier has modulus at least one beyond numerical
  tolerance;
- the supposed symmetry modes are not reproduced by the linearization;
- leading multipliers do not converge with Arnoldi tolerance/subspace size;
- a small registered perturbation leaves the candidate neighborhood without
  bounded return;
- the exact orbit drifts at zero perturbation beyond accumulated
  floating-point error.

A stability failure does not invalidate the one-step residual root. It
reclassifies it as an unstable prepared solution with no demonstrated basin.
