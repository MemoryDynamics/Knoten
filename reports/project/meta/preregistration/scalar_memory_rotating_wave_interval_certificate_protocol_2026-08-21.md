# Prospective interval certificate: scalar-memory rotating wave

Date: 2026-08-21.

Status: prospective candidate-targeted existence protocol. It is frozen
after the floating-point discovery and local source-stability result, and
before evaluating any candidate interval box.

Post-execution presentation note: revision
8ce6c00713cbac24ebaec337bd339f1944dbcc35 is the authoritative frozen source
that was executed. Several LaTeX backslashes were lost while that Markdown
file was authored. They were restored after the result without changing any
word, number, box, precision, iteration count, formula or decision rule.

## 1. Scope and claim boundary

The sole target is candidate

\[
\text{k0h-rw-aatt3p5-alpha1e-2-h1200-eta0p15-v1}.
\]

The gate asks whether the two exact finite-\(H\) rotating-wave balance
equations have a unique zero near the published floating-point candidate.
It does not certify the 2400-dimensional stability spectrum, formation,
noise robustness, horizon robustness, an internal phase, work or mass.

## 2. Exact target function

Fix

\[
\alpha=0.01,\quad H=1200,\quad M_0=1,\quad\eta=0.15,
\]

\[
\sigma_{\rm rep}=1,\quad\sigma_{\rm att}=3,\quad
A_{\rm rep}=1,\quad A_{\rm att}=3.5.
\]

For \(p_j=j\theta\), define

\[
u_j=1-\cos p_j,\qquad
\phi_j=-e^{-R^2u_j}+\frac{3.5}{9}e^{-R^2u_j/9},
\]

\[
A_H=\sum_{j=1}^{H-1}\alpha(1-\alpha)^j\phi_j u_j,
\qquad
S_H=\sum_{j=1}^{H-1}\alpha(1-\alpha)^j\phi_j\sin p_j.
\]

The certified function is

\[
F(R,\theta)
=\begin{pmatrix}
1-\cos\theta-\eta A_H\\
\sin\theta+\eta S_H
\end{pmatrix}.
\]

Its full analytic \(2\times2\) Jacobian is evaluated term by term. No
finite-difference derivative, continuum approximation, trajectory fit or
truncated age sum is admitted.

## 3. Arithmetic and implementation controls

The implementation uses `mpmath==1.3.0`. Candidate certification uses the
`mpmath.iv` context, whose elementary operations and transcendental
functions return outward interval enclosures. Every serialized interval also
stores the exact internal binary endpoint tuples; decimal endpoints are for
readability.

Before candidate execution, tests must establish on unrelated inputs:

1. the multiprecision balance equals the existing native finite-\(H\)
   residual, with the declared first-component sign convention;
2. the analytic Jacobian matches a centered finite difference at \(H=17\);
3. interval function and Jacobian boxes enclose their independent point
   evaluations;
4. the generic two-dimensional Krawczyk implementation certifies a known
   polynomial root box;
5. invalid parameters are rejected.

## 4. Frozen boxes and precision panels

The published decimal center is

\[
R_0=0.946517504804225,\qquad
\theta_0=0.015770381717135.
\]

Two arithmetic panels are fixed at 80 and 120 decimal digits. In each panel:

1. certify the outer box

   \[
   X_{\rm out}
   =[R_0-10^{-10},R_0+10^{-10}]
   \times
   [\theta_0-10^{-10},\theta_0+10^{-10}];
   \]

2. starting exactly from \((R_0,\theta_0)\), perform eight analytic Newton
   iterations at the panel precision;
3. center an inner box of half-width \(10^{-40}\) in both coordinates on
   that fixed Newton result;
4. certify the inner box without changing its center, width, precision or
   iteration count.

No failed panel may be repaired by widening a box, increasing precision,
adding Newton steps or changing a native parameter. Such an outcome is
reported as inconclusive and requires a new protocol.

## 5. Krawczyk test

For a box \(X\) with center \(x_0\), interval Jacobian \(J(X)\), and the
point inverse \(C\approx J(x_0)^{-1}\), compute

\[
K(X)
=x_0-CF(x_0)+[I-CJ(X)](X-x_0).
\]

The inverse is represented as a directed-rounding point interval and its
determinant must exclude zero. Because \(F\) is analytic on the registered
physical box, the strict inclusion

\[
K(X)\subset\operatorname{int}X
\]

certifies existence and uniqueness of one zero in \(X\).

As consistency checks, both components of \(F(X)\) must contain zero,
\(A_H(X)>0\), \(S_H(X)<0\), and both independently required-gain intervals
must contain the frozen \(\eta=0.15\).

## 6. Decision rule

Decision is **interval-certified-unique-root-pass** only if all hold:

1. outer and inner boxes pass every Krawczyk and sign/gain control in both
   precision panels;
2. every inner box is a strict subset of its registered outer box;
3. the two refined centers agree coordinatewise within \(10^{-60}\);
4. each final point residual is at most \(10^{-(p-20)}\) at panel precision
   \(p\in\{80,120\}\);
5. the two inner certified enclosures overlap coordinatewise;
6. every inner Krawczyk-image width is below \(10^{-38}\).

Every other nonexceptional outcome is
**interval-certificate-inconclusive**. An arithmetic exception is
**interval-certificate-execution-fail** and does not count as evidence
against existence.

## 7. Sequential consequence

A pass upgrades the floating-point existence witness to a unique-root
certificate within the registered box. It opens only the prospective design
of a matched \((\alpha,H,\eta)\) refinement ladder with
\(H\alpha=12\) and \(\eta/\alpha=15\). The \(A_{\rm att}=7.0\) holdout,
noise, topology, basin/formation and mechanics branches remain sealed.
