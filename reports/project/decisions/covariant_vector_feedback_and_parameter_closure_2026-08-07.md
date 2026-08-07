# Covariant vector feedback and parameter closure

Date: 2026-08-07.

## Decision

The next vector-memory step is an analytical and measurement-closure step, not
a coefficient sweep.

A simulation cannot determine constants that remain fixed external inputs.
Three categories must therefore be kept separate:

1. primitive coefficients that define a microscopic update;
2. normalization-redundant products that cannot be identified separately;
3. effective observables or coarse-grained coefficients that may be selected
   by the dynamics and estimated on held-out data.

Only the third category may be called emergent, and only after convergence
across initial conditions, seeds, coarse-graining scales and fit windows.

## Parity-even local vector family

For a polar vector field \(m:\mathbb R^d\to\mathbb R^d\), the isotropic
parity-even local energy through fourth spatial order is

\[
\mathcal F[m;J]
=
\int
\left[
\frac a2|m|^2
+\frac{b_L}{2}(\nabla\cdot m)^2
+\frac{b_T}{4}
(\partial_i m_j-\partial_jm_i)^2
+\frac c2|\Delta m|^2
+\frac u4|m|^4
-J\cdot m
\right]dx.
\]

In \(d=3\), the antisymmetric-gradient term is equivalent to the usual curl
term. The index form remains valid in arbitrary dimension.

Purely dissipative dynamics is

\[
\partial_t m
=
-\Gamma\frac{\delta\mathcal F}{\delta m}.
\]

After longitudinal/transverse Helmholtz decomposition, the two linear
denominators are

\[
D_L(k)=a+b_Lk^2+ck^4,
\qquad
D_T(k)=a+b_Tk^2+ck^4,
\]

and the growth rates are

\[
s_L(k)=-\Gamma D_L(k),
\qquad
s_T(k)=-\Gamma D_T(k).
\]

The Fourier operator is real symmetric and transforms as

\[
A(Ok)=OA(k)O^\mathsf T
\]

for every \(O\in O(d)\). Therefore all linear rates are real. A one-field
gradient flow may relax, become unstable or form a static texture, but it does
not provide a temporal phase or harmonic spin mode.

## Spatial scale selection

For either channel \(q\in\{L,T\}\), a finite-wavenumber preference requires

\[
b_q<0,\qquad c>0.
\]

Then

\[
k_{\ast,q}
=
\sqrt{\frac{-b_q}{2c}},
\qquad
D_q(k_{\ast,q})
=
a-\frac{b_q^2}{4c}.
\]

With \(a,c>0\), define

\[
\widehat b_q
=
\frac{b_q}{\sqrt{ac}}.
\]

The finite-wavenumber instability threshold is exactly

\[
\widehat b_q<-2.
\]

The nonlinear coefficient \(u>0\) can saturate growth, but the final amplitude
depends on pattern geometry and source statistics. It is not fixed by the
linear threshold alone.

Natural units remove three scale choices:

\[
\ell_0=(c/a)^{1/4},
\qquad
m_0=\sqrt{a/u},
\qquad
t_0=(\Gamma a)^{-1}.
\]

The irreducible linear shape parameters remain
\(\widehat b_L\) and \(\widehat b_T\). Nondimensionalization reduces parameter
redundancy; it does not explain these two numbers.

## Why the current passive memory cannot select these coefficients exactly

The implemented oriented memory obeys

\[
m_{n+1}(x)
=
(1-\lambda_v)m_n(x)
+
\lambda_vM_vp_{n+1}G_v(x-x_{n+1}).
\]

With the trajectory source held fixed, its homogeneous operator is simply

\[
m_{n+1}^{\rm hom}
=
(1-\lambda_v)m_n^{\rm hom}.
\]

It has no longitudinal/transverse splitting, spatial derivative term or
self-interaction. Thus the microscopic passive law contains no \(b_L\),
\(b_T\), \(c\) or \(u\) that a longer run could determine.

Trajectory correlations may nevertheless generate an approximate
coarse-grained closure. Such fitted coefficients would be effective
descriptors, not newly discovered microscopic constants.

## Oscillation requires a distinct state-space increment

A chiral energy term in \(d=3\),

\[
\chi\,m\cdot(\nabla\times m),
\]

explicitly distinguishes parity for a polar \(m\). Under gradient flow it
splits helical spatial channels but still belongs to an energy Hessian and does
not by itself create complex temporal eigenvalues.

The minimal rotational temporal block is instead

\[
\frac d{dt}
\begin{pmatrix}m\\q\end{pmatrix}
=
\begin{pmatrix}
-\gamma&-\omega\\
\omega&-\gamma
\end{pmatrix}
\begin{pmatrix}m\\q\end{pmatrix},
\]

applied identically to each ambient component. Its eigenvalues are

\[
-\gamma\pm i\omega.
\]

This construction is \(O(d)\)-covariant, but it introduces a second internal
vector \(q\) and an antisymmetric coupling \(\omega\). It is therefore a new
mechanism, not a consequence of passive vector memory. A second-order inertial
field is an equivalent state-space enlargement.

## Parameter-closure protocol

Before any active vector-field simulation, use the complete retained deposits
to construct exact Fourier features

\[
m_k(n)
=
\sum_jw_j^{(v)}p_{n-j}
e^{-ik\cdot(x_{n-j}-c_n)}.
\]

Then:

1. condition explicitly on the new trajectory source \(J_k(n+1)\);
2. fit longitudinal and transverse one-step operators separately;
3. test whether adding \(k^2\) and \(k^4\) terms improves held-out prediction
   beyond the exact homogeneous factor \(1-\lambda_v\);
4. repeat over seeds, time segments, wavevector shells and coarse-graining
   levels;
5. require coefficient sign and dimensionless ratios to remain stable without
   seedwise retuning;
6. test the implied \(k_\ast\) against an independently measured spectral peak.

If the fitted operator collapses to the homogeneous forgetting factor or its
coefficients drift with resolution, there is no evidence for emergent local
vector feedback. At that point the project must either retain passive vector
memory only or declare an active field law as a new primitive postulate.

## Consequences for parameter language

The following are currently inputs:

- \(\lambda_m,\lambda_v,\kappa\);
- noise and scalar-force scales;
- any future \(a,b_L,b_T,c,u,\Gamma,\chi,\omega\).

The following products are not separately identifiable in the existing linear
one-way channel:

\[
\eta_vM_v\times\text{readout normalization}.
\]

Potentially emergent quantities are:

- a stable coarse-grained \(k_\ast\) or length;
- saturated field amplitude;
- relaxation or oscillation rates;
- dimensionless effective ratios stable under coarse graining.

A parameter is not self-selected merely because one long trajectory approaches
a plateau. It must lose dependence on its initialization while remaining
stable under the measurement and holdout controls above.

## Next step

Implement the source-conditioned longitudinal/transverse Fourier closure on the
existing six mature vector-memory continuations. This is a measurement task,
not a new interaction simulation. Only a nontrivial, held-out-stable operator
may authorize an active covariant feedback pilot.