# Implemented equations and oscillator requirements

Status: 2026-08-11. This is a code-level equation ledger and scientific
decision note. Display equations use GitHub-rendered LaTeX.

## Executive decision

1. The mathematical augmented state is $z_n=(x_n,\rho_n)$. A finite point
   history is only one implementation of the truncated field.
2. The local one-node scalar reduction has only real multipliers. This is a
   local null result, not a global impossibility theorem for the full nonlinear
   finite-memory dynamics.
3. A reciprocal second node creates a new relative feedback channel. Together
   with two lagging memory centers it can, in principle, produce a complex mode
   pair. Reciprocal coupling alone does not guarantee oscillation.
4. For the synchronous local reciprocal reduction, a complex cross-gain window
   exists only for weak self gain

   $$
   g<\frac{\lambda}{1+\lambda}.
   $$

   The current compact-knot baseline is far outside this window. Instantaneous
   reciprocal coupling is therefore a useful null test; a delayed mediator,
   inertia, oriented coupling, or a nonlinear bifurcation may still be needed.
5. Fixed input parameters cannot select themselves during a long run. Long
   runs select states or attractor branches and estimate effective observables
   conditional on those inputs.

## 1. Canonical scalar model

Define

$$
q=1-\lambda,
\qquad 0<\lambda\leq 1.
$$

The general memory update is

$$
\rho_{n+1}(x)
=q\rho_n(x)+\beta G_\sigma(x-x_{n+1}). \tag{1}
$$

For normalized $G_\sigma$, the stationary memory mass is

$$
M_0=\frac{\beta}{\lambda}.
$$

The canonical package uses $M_0$ as input and hence

$$
\beta=\lambda M_0. \tag{2}
$$

Rolling out the memory recurrence gives

$$
\rho_n
=q^n\rho_0
+\lambda M_0\sum_{j=0}^{n-1}
q^jG_\sigma(\,\cdot-x_{n-j}). \tag{3}
$$

The memory-induced potential and visible update are

$$
\Phi_n(x)=(K*\rho_n)(x), \tag{4}
$$

$$
x_{n+1}
=x_n+\varepsilon\xi_n-\eta\nabla\Phi_n(x_n),
\qquad \xi_n\sim\mathcal N(0,I_d). \tag{5}
$$

The canonical scalar read kernel is

$$
K(r)
=A_{\mathrm{rep}}
\exp\!\left(-\frac{\lVert r\rVert^2}{2\sigma_{\mathrm{rep}}^2}\right)
-A_{\mathrm{att}}
\exp\!\left(-\frac{\lVert r\rVert^2}{2\sigma_{\mathrm{att}}^2}\right).
\tag{6}
$$

For Gaussian deposition the code evaluates the exact effective convolution
$W=K*G_\sigma$. For delta deposition, $W=K$.

## 2. Augmented state and finite-history backend

The paper-level Markov state is

$$
z_n=(x_n,\rho_n). \tag{7}
$$

The visible coordinate $x_n$ alone is generally non-Markovian. The augmented
state is Markov for fixed parameters and independent noise increments.

The production backend truncates the exponential history at

$$
H=min\!\left(
H_{\max},
\max\!\left(1,\left\lfloor\frac{f_{\mathrm{mem}}}{\lambda}\right\rfloor\right)
\right),
\qquad
w_j=\lambda M_0q^j. \tag{8}
$$

It evaluates

$$
\Phi_n^{(H)}(x)
=\sum_{j=0}^{H-1}w_jW(x-x_{n-j}). \tag{9}
$$

The actual ring buffer stores

$$
r_n^{(H)}=(x_n,x_{n-1},\ldots,x_{n-H+1}). \tag{10}
$$

If the current coordinate is already written separately, a nonredundant
history notation is

$$
z_n^{(H)}=(x_n,h_n^-),
\qquad
h_n^-=(x_{n-1},\ldots,x_{n-H+1}). \tag{11}
$$

Thus the previous notation $z_n=(x_n,h_n)$ with $h_n$ starting again at $x_n$
was redundant and inappropriate as the main state definition.

In the canonical model, memory has no direct spatial self-dynamics. It relaxes,
receives trajectory deposits, and acts back on the trajectory. Direct memory
evolution appears only in separate extension modules below.

## 3. Spectral representation

The one-dimensional periodic spectral pilot uses

$$
k_m=\frac{2\pi m}{L}
$$

and updates

$$
\widehat\rho_{n+1,m}
=q\widehat\rho_{n,m}
+\lambda\frac{M_0}{L}
\exp\!\left(-\frac{\sigma_G^2k_m^2}{2}\right)
e^{-ik_mx_{n+1}}. \tag{12}
$$

The potential coefficients are

$$
\widehat\Phi_{n,m}=\widehat K_m\widehat\rho_{n,m}. \tag{13}
$$

Moving the read kernel into the stored field is an exact reparameterization:

$$
\widehat\phi_n=\widehat K\widehat\rho_n,
$$

$$
\widehat\phi_{n+1}
=q\widehat\phi_n
+\lambda\widehat K\widehat G_{x_{n+1}}. \tag{14}
$$

This changes occupancy memory into signed potential memory. It does not create
a self-dynamic field.

The optional relaxation-diffusion extension is

$$
\widehat\rho_{n+1,m}
=e^{-\nu k_m^2}
\left(q\widehat\rho_{n,m}
+\lambda\widehat G_m(x_{n+1})\right). \tag{15}
$$

Positive $\nu$ is additional dynamics; $\nu=0$ recovers exponential memory.

## 4. Optional vector and interaction pilots

The vector-memory pilot deposits the normalized step direction

$$
u_{n+1}
=\frac{x_{n+1}-x_n}{\lVert x_{n+1}-x_n\rVert} \tag{16}
$$

for nonzero displacement. Its local readout is

$$
V_n(x)
=\sum_j\lambda_vM_v(1-\lambda_v)^j
\exp\!\left(-\frac{\lVert x-y_{n-j}\rVert^2}{2\sigma_v^2}\right)
u_{n-j}. \tag{17}
$$

The optional trajectory coupling is

$$
x_{n+1}
=x_n+\varepsilon\xi_n-\eta\nabla\Phi_n(x_n)
+\eta_vV_n(x_n). \tag{18}
$$

The explicitly two-dimensional transverse pilot replaces $V_n$ by $JV_n$,
where

$$
J(v_1,v_2)=(-v_2,v_1).
$$

This assumes a selected plane and cannot establish emergent $d=3$.

The implemented scalar one-way source/target pilot is

$$
x^S_{n+1}
=x^S_n+\varepsilon_S\xi^S_n
-\eta_S\nabla\Phi^S_n(x^S_n)+d_n, \tag{19}
$$

$$
x^T_{n+1}
=x^T_n+\varepsilon_T\xi^T_n
-\eta_T\nabla\Phi^T_n(x^T_n)
-\eta_\times\nabla\Phi^S_n(x^T_n). \tag{20}
$$

The source does not read the target. This is not reciprocal interaction. The
signed cross-channel additionally multiplies the last term by externally
supplied labels $q_Sq_T\in\{-1,0,+1\}$; these are not emergent charges.

## 5. Active field and mediator pilots

The one-dimensional periodic active scalar field integrates

$$
\partial_t\phi
=-\left[1+a_2(-\partial_x^2)+a_4\partial_x^4\right]\phi
-u\phi^3+s\,\delta_L(x-X_t), \tag{21}
$$

$$
dX_t=-\eta\,\partial_x\phi(X_t)\,dt+\varepsilon\,dW_t. \tag{22}
$$

Its linear growth rate is real:

$$
\sigma(k)=-(1+a_2k^2+a_4k^4). \tag{23}
$$

For $a_2<0$, the preferred wavenumber is

$$
k_*=\sqrt{-\frac{a_2}{2a_4}}.
$$

This can select a spatial pattern but does not itself provide a temporal phase.
The existing $\eta=0$ control forms nearly the same field pattern.

The local relaxation-diffusion mediator is

$$
\partial_ta=D\partial_x^2a-\mu a+s. \tag{24}
$$

The telegraph mediator is

$$
\partial_t^2a+2\gamma\partial_ta+\omega_0^2a
=c^2\partial_x^2a+s. \tag{25}
$$

A Fourier mode is underdamped when

$$
\gamma^2<\omega_0^2+c^2k^2. \tag{26}
$$

The telegraph pilot can therefore carry damped oscillations, but only because
the second-order transport law was supplied as a model input.

## 6. One-node local mode null

For local restoring gain $g=\eta\kappa$, the minimal scalar center reduction is

$$
x_{n+1}=(1-g)x_n+g\bar x_n^\rho, \tag{27}
$$

$$
\bar x_{n+1}^\rho=\lambda x_{n+1}+q\bar x_n^\rho. \tag{28}
$$

Its multipliers are

$$
\mu_1=1,
\qquad
\mu_2=q(1-g). \tag{29}
$$

The relative mode is stable when

$$
\lvert q(1-g)\rvert<1. \tag{30}
$$

It relaxes monotonically for $q(1-g)>0$ and alternates for $q(1-g)<0$.
Alternation is not a harmonic phase.

For a frozen-memory Hessian eigenvalue $h_i$, the local multiplier is
$1-\eta h_i$, and stability requires

$$
0<\eta h_i<2. \tag{31}
$$

A genuine damped discrete oscillator requires

$$
\mu_\pm=re^{\pm i\theta},
\qquad
0<r<1,
\qquad
\theta\notin\{0,\pi\}. \tag{32}
$$

Equations (27)-(31) are not a global impossibility theorem for the full
finite-history nonlinear system. Delayed nonlinear feedback could still
produce a limit cycle or complex modes. Existing fitted candidates failed the
raw-mode, segment-identity, or $\eta=0$ controls.

## 7. Reciprocal two-node local mode test

Let two nodes read both their own and the other node's lagging memory center:

$$
x'_i=x_i-g(x_i-\bar x_i^\rho)-c(x_i-\bar x_j^\rho),
\qquad i\neq j, \tag{33}
$$

$$
{\bar x_i^\rho}'=q\bar x_i^\rho+\lambda x'_i. \tag{34}
$$

Here $g=\eta\kappa_{\rm self}$ and
$c=\eta_\times\kappa_\times$ are dimensionless gains per update. This is a
synchronous local reduction, not yet the full nonlinear reciprocal simulator.

For common variables $x_+=(x_1+x_2)/2$ and
$\bar x_+^\rho=(\bar x_1^\rho+\bar x_2^\rho)/2$, the multipliers remain real:

$$
\mu_+^{(1)}=1,
\qquad
\mu_+^{(2)}=q(1-g-c). \tag{35}
$$

For relative variables $x_-=(x_1-x_2)/2$ and
$\bar x_-^\rho=(\bar x_1^\rho-\bar x_2^\rho)/2$, the update matrix is

$$
A_-=
\begin{pmatrix}
1-g-c & g-c\\
\lambda(1-g-c) & q+\lambda(g-c)
\end{pmatrix}. \tag{36}
$$

Its trace and determinant are

$$
T=2-\lambda-qg-(1+\lambda)c, \tag{37}
$$

$$
D=q(1-g-c). \tag{38}
$$

The relative multipliers are

$$
\mu_-^{\pm}
=\frac{T\pm\sqrt{T^2-4D}}{2}. \tag{39}
$$

A stable oscillatory relative mode requires

$$
T^2<4D,
\qquad
0<D<1. \tag{40}
$$

Minimizing the discriminant over positive cross gain gives the exact necessary
condition for any complex window:

$$
g<\frac{\lambda}{1+\lambda}. \tag{41}
$$

For the compact two-scale baseline

$$
\lambda=0.01,
\quad
g=\eta M_0\left(
\frac{A_{\rm att}}{\sigma_{\rm att}^2}
-\frac{A_{\rm rep}}{\sigma_{\rm rep}^2}
\right)
=0.15\left(\frac{35}{9}-1\right)
\approx0.433, \tag{42}
$$

whereas

$$
\frac{\lambda}{1+\lambda}\approx0.00990. \tag{43}
$$

Thus the synchronous local return channel cannot generate a complex mode at
this baseline for any positive $c$. This result does not exclude nonlinear,
finite-separation, retarded, or oriented reciprocal dynamics.

## 8. What could still generate oscillations?

The remaining discriminating mechanisms are:

1. **Retarded reciprocal coupling.** The memory or mediator must provide enough
   phase lag to cross a Hopf-type boundary.
2. **Momentum or inertia.** For

   $$
   v_{n+1}=(1-\gamma)v_n-\kappa r_n,
   \qquad
   r_{n+1}=r_n+v_{n+1}, \tag{44}
   $$

   a stable complex pair exists when

   $$
   0<\gamma<1,
   \qquad
   (2-\gamma-\kappa)^2<4(1-\gamma). \tag{45}
   $$

3. **Oriented antisymmetric coupling.** A block $A=aI+bJ$ with $J^2=-I$ has
   eigenvalues $a\pm ib$ and is stable for $a^2+b^2<1$.
4. **A nonlinear reciprocal bifurcation.** The full kernels may leave the local
   regime and create a limit cycle not present in (33)-(34). This must be shown
   against the local prediction, not inferred from a spectral peak alone.

Moving-center errors, cadence aliasing, finite-window AR leakage, non-normal
transients, and metastable switching can all resemble oscillations without a
stable complex mode.

## 9. Rotation and effective rank three

An elementary rotation in $\mathbb R^d$ occupies a two-plane. Pure rotation
therefore does not select three dimensions. A falsifiable route is

$$
\text{one coherent rotation plane}
+\text{one independent propagation axis}
\longrightarrow \text{effective rank }3. \tag{46}
$$

A future cross-ambient-dimension test must demonstrate:

1. one persistent, control-separated bivector plane;
2. one independent propagation or normal axis;
3. a stable eigengap after the third response direction;
4. the same rank across seeds, ambient dimensions, windows, and a held-out
   parameter slice;
5. loss of rank three when the phase-producing mechanism is disabled.

## 10. Parameter self-selection

The current parameter tuple

$$
\Theta=(\varepsilon,\eta,\lambda,M_0,K,G,\ldots) \tag{47}
$$

is fixed before a run. A long run samples $P_\Theta$ and may select an attractor
branch. It cannot update $\Theta$ without an additional law.

Parameter self-selection would require slow coupling dynamics, a conserved
resource, a constrained variational principle, population selection, or a
coarse-graining flow. Such a mechanism must be specified before looking for a
preferred value.

## 11. Inertial active-field proposal: explicit model boundary

The later P3.6 analytic gate introduced a separate active vector field and its
conjugate momentum,

$$
\partial_t m=\frac{\pi}{I},
\qquad
\partial_t\pi
=-\frac{\delta\mathcal F}{\delta m}
-\frac{\gamma}{I}\pi+J. \tag{48}
$$

Its channel poles solve

$$
Is^2+\gamma s+D_q(k)=0. \tag{49}
$$

This equation is not an alternative notation for Equations (1)-(5). The
variables $m$ and $\pi$, the source $J$, and the coefficients
$I,\gamma,a,b_L,b_T,c,u$ are absent from `SimulationConfig`,
`FiniteMemoryState`, and the canonical trajectory update. The code in
`covariant_vector_field.py` is an isolated analytic proposal and does not
advance a knot state.

The resulting harmonic mode is therefore constructed by the independent
conjugate state. It is a classical damped-field oscillator, not evidence of
emergence or quantum mechanics.

## 12. Current next gate

No oscillator-parameter sweep or coupled field simulation is currently
admissible. First fix a projection $Y_n=\Psi(x_n,\rho_n)$ from canonical
variables without using the desired spectral result. A second-order closure

$$
Y_{n+1}=A_1Y_n+A_2Y_{n-1}+e_{n+1} \tag{50}
$$

must beat a first-order control on held-out futures, retain pole identity over
seeds, time segments, cadences and coarse-graining, and predict an independent
response. The passive Fourier, metric-reconciliation and balanced-full-memory
results have not yet supplied such an independent conjugate state.

Only a pass can justify estimating effective $I$, $\gamma$ and $D_q(k)$.
Otherwise Equation (48) remains a declared Paper-III comparison model or its
extra state and constants must be accepted explicitly as new primitives.
