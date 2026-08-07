# Vector-memory state and symmetry contract

Date: 2026-08-07.

## Decision

The active vector extension is the persistent-carrier model. The older
instantaneous-direction pilot remains a named comparison model and is not
silently merged with it.

The state stores every directed deposit inside the retained finite-memory
horizon. This is uncompressed within that horizon, but it is still a controlled
truncation of the infinite exponential tail.

## State and updates

Let the visible position be

\[
x_n\in\mathbb R^d.
\]

The scalar memory obeys

\[
\rho_{n+1}(y)
=
(1-\lambda_m)\rho_n(y)
+
\beta_m G_m(y-x_{n+1}).
\]

For stationary scalar mass \(M_0\), the normalized choice is

\[
\beta_m=\lambda_m M_0.
\]

The unit step direction is

\[
u_{n+1}
=
\begin{cases}
\dfrac{x_{n+1}-x_n}{\lVert x_{n+1}-x_n\rVert},
&x_{n+1}\ne x_n,\\
0,&x_{n+1}=x_n.
\end{cases}
\]

The persistent carrier and oriented memory field are

\[
p_{n+1}
=
(1-\kappa)p_n+\kappa u_{n+1},
\]

\[
m_{n+1}(y)
=
(1-\lambda_v)m_n(y)
+
\beta_v p_{n+1}G_v(y-x_{n+1}).
\]

For stationary vector-memory weight \(M_v\),

\[
\beta_v=\lambda_v M_v.
\]

The exact finite representation used by the code is the age-ordered set

\[
\left\{
(x_{n-j},p_{n-j},w_j^{(v)})
\right\}_{j=0}^{H-1},
\qquad
w_j^{(v)}=\lambda_v M_v(1-\lambda_v)^j.
\]

Its omitted normalized tail is

\[
\delta_H=(1-\lambda_v)^H.
\]

For the current primary values \(\lambda_v=0.01\) and \(H=600\),
\(\delta_H\approx2.4\times10^{-3}\).

## Readout boundary

A general local vector readout may be written

\[
B_n(x)
=
\int L_v(x-y)m_n(y)\,dy.
\]

The existing one-way tests use a Gaussian \(L_v\) and

\[
x^{(T)}_{n+1}
=
F_{\rm scalar}(x^{(T)}_n,\rho^{(T)}_n,\xi^{(T)}_n)
+
\eta_v B_n^{(S)}(x^{(T)}_n).
\]

This readout is instantaneous and phenomenological. The source itself still
obeys the scalar visible update

\[
x_{n+1}
=
x_n+\varepsilon\xi_n-\eta_s\nabla\Phi[\rho_n](x_n).
\]

Thus \(m_n\) does not yet exert a source self-force. Reciprocal coupling, local
propagation and a dynamical vector-field equation are separate future model
increments.

## Markov state

For the field formulation the augmented state is

\[
z_n=(x_n,\rho_n,p_n,m_n).
\]

For the implemented finite representation it is equivalently

\[
z_n=
\left(
x_n,
\{x_{n-j}\}_{j=0}^{H_s-1},
p_n,
\{p_{n-j}\}_{j=0}^{H_v-1}
\right).
\]

Given the next noise increment, this state determines the next update. A
carrier-only feature or a moment summary is not the Markov state.

## Symmetries and null limits

The implemented passive state has:

- translation equivariance;
- \(O(d)\) covariance:
  \(x\mapsto Ox+a\), \(p\mapsto Op\), \(m\mapsto Om\);
- a global vector-sign transformation:
  \(p,m\mapsto-p,-m\), which reverses a linear vector readout;
- exact scalar recovery for \(\eta_v=0\) or \(M_v=0\);
- a one-step comparison model at \(\lambda_v=\kappa=1\);
- a deposit-sign null that destroys coherent ordering while preserving
  positions, magnitudes, weights and the scalar trajectory.

In a linear one-way response, only the product of readout normalization,
\(M_v\), and \(\eta_v\) is directly identifiable. One factor must be fixed
before the others can be compared.

## Rotation-covariant observables

Using all retained vector deposits, define their weighted center

\[
c_v=\frac{1}{M_v^{(H)}}\sum_jw_j^{(v)}x_{n-j}.
\]

The polar moment is

\[
P_n
=
\frac{1}{M_v^{(H)}}\sum_jw_j^{(v)}p_{n-j}.
\]

The antisymmetric circulation moment is

\[
L_n
=
\frac{1}{M_v^{(H)}}\sum_jw_j^{(v)}
\left[
(x_{n-j}-c_v)\otimes p_{n-j}
-
p_{n-j}\otimes(x_{n-j}-c_v)
\right].
\]

Under \(O(d)\),

\[
P_n\mapsto OP_n,
\qquad
L_n\mapsto OL_nO^\mathsf T.
\]

In \(d=3\), \(L_n\) may be dualized to an axial vector. In general dimension it
is a bivector. Calling it quantum spin, assigning half-integer values, or
claiming angular-momentum conservation would require additional dynamics and
tests.

## What the state does not contain

A spatial polar vector does not by itself define a rotationally invariant
signed scalar charge. The present state also has no internal species index or
representation from which flavor could be inferred.

Therefore:

- polarization is defined;
- a spin-like circulation candidate is defined;
- charge is currently undefined, not merely unmeasured;
- flavor is currently undefined, not merely unmeasured.

A charge claim would require a signed source or flux law and a conservation
test. A flavor claim would require an explicit internal state space,
transformations and interaction invariants.

## Next falsifying gate

Before adding self-feedback or further fields, the six mature scalar source
states are continued under identical scalar dynamics. Polarization and
circulation are tested separately against depositwise random-sign nulls,
axis-identity and shape bounds. A polar pass mainly validates the inserted
persistent carrier. Only a circulation pass would make the bivector eligible
for a later interaction test; neither result would establish physical spin.