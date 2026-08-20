# Prospective source-stability gate: scalar-memory rotating wave

Date: 2026-08-20.

Status: prospective candidate-targeted numerical stability protocol. It is
frozen after P0 and D0, and before evaluating the candidate Jacobian or any
perturbation continuation.

## 1. Scope

The sole target is candidate

\[
\text{k0h-rw-aatt3p5-alpha1e-2-h1200-eta0p15-v1}.
\]

The gate tests transverse stability of its rotating relative equilibrium in
the complete native FIFO state. It does not test data-driven topology,
internal phase after the \(SO(2)\) quotient, noise robustness, external
coupling, physical work or mass. The \(A_{\rm att}=7.0\) holdout remains
sealed.

## 2. Co-rotating full map

Let

\[
Y_n=(x_n,x_{n-1},\ldots,x_{n-H+1})\in\mathbb R^{2H}.
\]

If \(\mathcal F\) is the native deterministic FIFO update, define

\[
\mathcal G_\theta(Y)
=\mathcal R(-\theta)\mathcal F(Y),
\]

where the same rotation is applied to every two-vector block. The prepared
circular history \(Y_\ast\) must be a fixed point of \(\mathcal G_\theta\).

The Jacobian is assembled analytically. For age \(j\geq1\), let \(H_j\) be
the Hessian of \(K(x-h_j)\). The first native row has blocks

\[
J_{00}^{\rm native}
=I-\eta\sum_{j=1}^{H-1}w_jH_j,
\qquad
J_{0j}^{\rm native}
=\eta w_jH_j.
\]

The remaining rows are the FIFO shift. Every output block is then multiplied
by \(\mathcal R(-\theta)\). No finite-difference Jacobian is used for the
candidate spectrum.

## 3. Mandatory implementation controls

Before execution, unit tests must establish:

1. the candidate is fixed by the co-rotating full map to absolute component
   error at most \(4\,10^{-15}\);
2. the sparse analytic Jacobian agrees with a centered finite difference on a
   synthetic \(H=17\) state to relative tolerance \(2\,10^{-9}\);
3. the rotation tangent has multiplier one to relative residual below
   \(2\,10^{-14}\);
4. the two common-translation tangents transform exactly by
   \(\mathcal R(-\theta)\);
5. the D0 distance removes a common translation and proper rotation to
   absolute error below \(4\,10^{-15}\).

Failure of any control blocks candidate execution.

## 4. Spectral panels

The \(2400\times2400\) sparse Jacobian is evaluated by deterministic ARPACK
starts. The start vector is fixed from elementary sine/cosine functions of
the state index and contains no random seed.

| panel | requested eigenpairs | Arnoldi subspace | tolerance | max iterations |
| --- | ---: | ---: | ---: | ---: |
| primary | 24 | 96 | \(10^{-10}\) | 20000 |
| convergence | 36 | 144 | \(10^{-12}\) | 40000 |

Both panels request largest-modulus eigenvalues. Every returned eigenpair
must have normalized residual at most \(10^{-8}\).

The known symmetry subspace is fixed before the spectrum:

- two common translations, with multipliers \(e^{\pm i\theta}\);
- the global rotation tangent, with multiplier \(1\).

An eigenvector is symmetry-labelled only if its normalized projection on the
corresponding analytic subspace is at least \(0.99\). All other returned
eigenvalues are transverse.

The leading transverse eigenvalues from the two panels must match within
\(10^{-5}\) in the complex plane and \(10^{-6}\) in modulus. ARPACK
nonconvergence, missing symmetry modes or panel disagreement gives
inconclusive, not pass.

## 5. Frozen perturbation panel

Four co-rotating continuations are run for at most 5000 updates and sampled
every 10 updates:

1. exact unperturbed history;
2. visible radial displacement \(+10^{-7}R\,e_x\), history otherwise fixed;
3. visible tangential displacement \(+10^{-7}R\,e_y\), history otherwise
   fixed;
4. a deterministic full-history vector built from
   \(\sin(0.37k)+\cos(0.11k)\), projected orthogonally away from the three
   analytic symmetry tangents and scaled to Euclidean norm \(10^{-7}R\).

Distance is the frozen D0 metric after optimal common translation and proper
rotation. A perturbed continuation stops if this quotient distance exceeds
\(0.25\) times the D0 norm of the reference or becomes nonfinite. No
perturbation amplitude, direction, duration or sampling cadence may be
changed after seeing a result.

## 6. Decision rule

Decision is **unstable-source-fail** if all hold:

1. both spectral panels converge and pass residual/symmetry controls;
2. both contain a matched nonsymmetry multiplier with
   \(|\lambda|>1+10^{-6}\);
3. at least one registered perturbation grows by a factor of at least 100 in
   D0 quotient distance before stopping.

Decision is **numerically-stable-source-pass** only if all hold:

1. both spectral panels converge and pass residual/symmetry controls;
2. every returned transverse multiplier satisfies
   \(|\lambda|<1-10^{-4}\);
3. every registered nonzero perturbation ends below \(0.1\) times its initial
   quotient distance without crossing the stopping radius;
4. the exact control remains below quotient distance \(10^{-10}\).

Every other outcome is **source-stability-inconclusive**.

Even a numerical pass is not an interval proof that no omitted eigenvalue
lies outside the unit circle. A later publication-grade positive claim would
require a spectral enclosure or an independently justified characteristic
root bound.
