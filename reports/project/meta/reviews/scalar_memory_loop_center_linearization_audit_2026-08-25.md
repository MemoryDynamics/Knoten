# Critical audit: where the rotating-wave programme uses linearization

Date: 2026-08-25.

Verdict: **the prepared rotating wave is not created by a linearized
oscillator, but the present stability evidence is deliberately local and P1
uses linearization strongly.** The finite-$H$ rotating-wave balance and the
finite-amplitude continuation both evaluate the native nonlinear
Double-Gaussian FIFO map. The Arnoldi spectrum is the first derivative of that
map, and the registered continuation amplitude was small enough that it mainly
checks the same local regime. Formation and a finite basin remain untested.

The memory center has a different status. Its filter $B_H$ is an exact linear
readout of a prescribed trajectory history, not a Taylor approximation. The
scalar feedback $-g_H(x-c_H)$ is only a local collapsed-cloud approximation.
It is not admissible as the primary L3 loop model. The correct local linear
coupling at L3 is the full, matrix-valued tangent operator of the nonlinear
finite-radius loop.

## 1. Four statements that must not be conflated

| object | status | approximation actually used |
| --- | --- | --- |
| finite-$H$ circular balance for $(R,\theta)$ | exact conditional reduction of the native nonlinear map | no force Taylor expansion; the circular ansatz restricts the searched solution class |
| P1 Arnoldi multipliers | local linear stability evidence | first derivative $J_*=D\widetilde{\mathcal G}(Y_*)$ |
| P1 mirrored continuations | exact nonlinear-map evaluation | no linearized update, but only at $10^{-7}R$ and from a prepared circular history |
| $c_H=B_Hx$ | exact kinematic identity | none, once the finite FIFO is filled and normalized |
| $-\eta\nabla(K*\rho)(x)\simeq-g_H(x-c_H)$ | local scalar closure | Taylor expansion about a collapsed compact history |

Here $\widetilde{\mathcal G}$ is the complete FIFO map in the frame rotating
by $-\theta$ per update, and $Y_*$ is the certified prepared circular history.

The exact rotating-wave equation retains the radius-dependent factor

$$
\varphi\!\left(2R\left|\sin\frac{j\theta}{2}\right|\right)
$$

at every memory age $j$. This dependence selects the finite radius. Replacing
it by its value at zero would remove precisely the finite-amplitude mechanism
under test.

## 2. How much P1 depends on the tangent model

P1's spectral statement is completely local:

$$
\delta Y_{n+1}
=J_*\delta Y_n+O(\lVert\delta Y_n\rVert^2).
$$

The analytic Jacobian differentiates the nonlinear kernel at every chord of
the circular history. It is therefore not the scalar center approximation,
but it is still a linearization. The two Arnoldi panels sampled the leading
part of this $4800\times4800$ operator and did not enclose its full spectrum.

The six P1 perturbation arms used the complete nonlinear FIFO update for
$10000$ steps. This is an important check that the linear conclusion is not
immediately contradicted by the exact map. It is not a strong nonlinear-basin
test: the only amplitude was $10^{-7}R$, the initial histories were prepared
perturbations of $Y_*$, and the observed return can be expected when the
tangent spectrum is contracting. P1 therefore supports local numerical
transverse stability, not nonlinear formation or a finite basin.

## 3. Why the old scalar center closure cannot be transferred to L3

For Delta deposition the collapsed-cloud curvature used by the earlier
center reduction is

$$
\kappa_K
=\frac{A_{\rm att}}{\sigma_{\rm att}^2}
-\frac{A_{\rm rep}}{\sigma_{\rm rep}^2}.
$$

At the frozen L3 parameters this gives

$$
\kappa_K=\frac{3.5}{9}-1=-0.611111\ldots,
$$

$$
M_H=1-0.995^{2400}=0.999994037975\ldots,
$$

$$
g_H=\eta M_H\kappa_K=-0.045833060074\ldots .
$$

The untruncated scalar center pole would be

$$
a=q(1-g_H)=1.040603894773\ldots>1.
$$

Thus L3 lies outside the positive-$g_H$, stable local plants certified by the
former A2 and B-star gates. Applying their scalar transfer
$T_{f\to v^c,H}$ to L3 as a pass prediction would be an unjustified model
change. The sign is not a convention error: the origin is locally repulsive
for this kernel. The finite-radius loop is possible because older trajectory
points sample other kernel radii and directions.

This is already a falsification of the **scalar-origin merger**, before any
new response trace is opened. It does not falsify a local linear description
of perturbations around the finite-radius loop.

## 4. The locally appropriate linear coupling

For the rotating wave, the Hessian block contributed by age $j$ is

$$
H_j
=\varphi(r_j)I
+\frac{\varphi'(r_j)}{r_j}d_jd_j^{\mathsf T},
\qquad
d_j=x_*-x_{*-j}.
$$

Consequently the tangent feedback is distributed over all ages and is in
general anisotropic in radial and tangential directions. In the co-rotating
frame it is time independent:

$$
\delta Y_{n+1}=J_*\delta Y_n+E\alpha u_n,
\qquad
\delta c_n=C_H\delta Y_n,
$$

where $C_H$ contains the exact normalized geometric weights and $E$ injects
the declared effective probe into the visible update. Here $u_n$ is the input
expressed in the co-rotating frame; a laboratory-fixed input is transformed by
the known unforced phase before injection. The resulting exact tangent
transfer between co-rotating input and center velocity is

$$
\boxed{
T_{u\to v^c}^{\rm loop}(z)
=(z-1)C_H(zI-J_*)^{-1}E
}.
$$

The executable protocol uses the equivalent time-domain tangent recurrence.
No pole, gain or damping coefficient may be fitted to the L3 response in P2.

## 5. Is a globally linear coupling the better model?

There are two different answers.

1. **As a local effective response model: yes.** The full tangent coupling is
   the least assumptive predictor for sufficiently weak interventions around
   the already established loop. Its range of validity must be measured with
   an amplitude ladder and a quadratic-remainder test.
2. **As the generative loop law: no evidence supports that replacement.** A
   homogeneous passive scalar memory closure cannot select a stable nonzero
   radius. It either contracts, grows, or, at a neutral tuning, leaves the
   amplitude undetermined. The native kernel nonlinearity supplies the
   radius-dependent balance that a globally linear law lacks.

Using a linear law as the fundamental simulator would therefore bake in a
different mechanism. It is useful as a tangent theory, null model and reduced
description, not as independent evidence that inertia or a loop emerged.

## 6. Consequence for P2

The previous P2 wording is tightened as follows.

- The exact $B_H$ identity and rotation/translation covariance are structural
  controls, not pass evidence.
- The scalar positive-$g_H$ center transfer is recorded as analytically
  ineligible at L3, not rescued by refitting an effective $g$.
- The primary predictor is the frozen full FIFO Jacobian $J_*$ with the exact
  center readout $C_H$.
- Mirrored nonlinear runs at three amplitudes must converge to the tangent
  prediction, show a second-order remainder, and return in the quotient loop
  coordinates.
- A second zero-net waveform and rotated phase copies are holdouts.
- The probe remains the previously declared effective additive visible-state
  input. Gate A's microscopic port non-identifiability is unchanged, and no
  physical work or mass claim is tested here.

A pass would establish only a local matrix-valued Loop--Center response for
one prepared L3 loop. It would not transfer the earlier scalar filter mass to
that loop, prove formation, or identify a center-conjugate microscopic
actuator.
