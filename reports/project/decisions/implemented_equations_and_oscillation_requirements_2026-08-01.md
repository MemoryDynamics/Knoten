# Implemented equations and oscillator requirements

Status: 2026-08-01. This is a code-level equation ledger and a scientific
decision note. It distinguishes the canonical model from exact
reparameterizations, optional pilot extensions, diagnostics, and unimplemented
hypotheses.

## Executive decision

1. The implemented canonical scalar model contains no demonstrated mechanism
   that selects rank three independently of the supplied ambient dimension.
2. Its minimal local scalar-memory reduction has only real multipliers. It can
   relax monotonically or with alternating signs, but it has no robust harmonic
   mode.
3. Rotation alone would not derive three dimensions. In any ambient dimension
   `d >= 2`, an elementary rotation acts in a two-dimensional plane. A possible
   route to effective rank three is a selected rotation plane plus one
   independent propagation axis, together with suppression of all remaining
   directions. That mechanism is not implemented or evidenced yet.
4. Fixed input parameters do not change or select themselves during a long
   run. Long runs can select an attractor branch and estimate effective
   observables conditional on the inputs. Parameter self-selection requires an
   additional adaptation, constraint, conservation, or coarse-graining law.

## 1. Canonical scalar finite-memory model

Let

```text
q = 1 - lambda,                 0 < lambda <= 1,
beta = lambda M0.
```

For a normalized deposition kernel `G_sigma`, the untruncated field equation is

```text
rho_(n+1)(x) = q rho_n(x) + beta G_sigma(x - x_(n+1)).        (1)
```

The more general form uses independent `beta`. Its stationary total memory
mass is `beta/lambda`. The canonical package instead takes `M0` as input and
therefore uses `beta=lambda M0`. This is a parametrization, not a new physical
law.

Rolling out (1) gives

```text
rho_n = q^n rho_0
        + lambda M0 sum_(j=0)^(n-1) q^j G_sigma(.-x_(n-j)).   (2)
```

The production backend stores the recent deposits directly. With

```text
H = min(max_memory, max(1, floor(memory_factor/lambda))),
w_j = lambda M0 q^j,
```

it evaluates the truncated effective potential

```text
Phi_n(x) = sum_(j=0)^(H-1) w_j W(x-x_(n-j)),
W = K * G_sigma,                                               (3)
```

over the available retained history. The visible update is

```text
x_(n+1) = x_n + epsilon xi_n - eta grad Phi_n(x_n),
xi_n ~ N(0,I_d).                                               (4)
```

The scalar read kernel is

```text
K(r) = A_rep exp(-|r|^2/(2 sigma_rep^2))
       - A_att exp(-|r|^2/(2 sigma_att^2)).                    (5)
```

For Gaussian deposition, the code uses the exact Gaussian convolution in
`W`; for delta deposition, `W=K`. The attractive-only branch is `A_rep=0`.
The update sign in (4), together with (5), is the canonical corrected sign
convention.

The augmented finite state

```text
z_n = (x_n,h_n),
h_n = (x_n, x_(n-1), ..., x_(n-H+1)).                         (6)
```

is Markov for fixed parameters and independent noise increments. The visible
coordinate alone is generally non-Markovian. The finite-history backend is an
explicit truncation of (1), not the exact infinite-memory field.

## 2. Exact spectral representation and reparameterization

The resource-bounded spectral pilot is one-dimensional and periodic. For
`k_m=2 pi m/L`, it stores

```text
rho_hat_(n+1,m)
  = q rho_hat_(n,m)
    + lambda (M0/L) exp(-sigma_G^2 k_m^2/2) exp(-i k_m x_(n+1)).   (7)
```

The potential and visible update are

```text
Phi_hat_(n,m) = K_hat_m rho_hat_(n,m),
x_(n+1) = [x_n + epsilon xi_n - eta d_x Phi_n(x_n)] mod L.     (8)
```

Moving the read kernel into the stored field is exact for this linear,
homogeneous convolution:

```text
phi_hat_n = K_hat rho_hat_n,
phi_hat_(n+1) = q phi_hat_n + lambda K_hat G_hat_(x_(n+1)),
x_(n+1) = [x_n + epsilon xi_n - eta d_x phi_n(x_n)] mod L.     (9)
```

Equation (9) changes the state interpretation from nonnegative occupancy
memory to a signed potential memory. It does not make the field self-dynamic.

The optional relaxation-diffusion extension adds

```text
rho_hat_(n+1,m)
  = exp(-nu k_m^2)
    [q rho_hat_(n,m) + lambda G_hat_m(x_(n+1))].                (10)
```

Positive `nu` is new dynamics; `nu=0` recovers (7).

## 3. Implemented optional vector-memory pilot

The vector-memory pilot writes the normalized step direction

```text
u_(n+1) = (x_(n+1)-x_n)/|x_(n+1)-x_n|                         (11)
```

when the displacement is nonzero. Its local readout is

```text
V_n(x) = sum_j lambda_v M_v (1-lambda_v)^j
                 exp(-|x-y_(n-j)|^2/(2 sigma_v^2)) u_(n-j).   (12)
```

The optional trajectory coupling is

```text
x_(n+1) = x_n + epsilon xi_n - eta grad Phi_n(x_n)
          + eta_v V_n(x_n)                                   (13a)
```

for alignment, or

```text
x_(n+1) = ... + eta_v J V_n(x_n),
J(v_1,v_2)=(-v_2,v_1),                                       (13b)
```

for the explicitly two-dimensional transverse pilot. Equation (13b) assumes
a selected plane; it cannot demonstrate emergent `d=3`.

A separate one-way oriented-source pilot low-pass filters the carrier:

```text
p_(n+1) = (1-lambda_p) p_n + lambda_p u_(n+1).                (14)
```

The orientation law, its relaxation, and the one-way readout are inserted
model ingredients. They are not generated by the canonical scalar dynamics.

The implemented scalar one-way source/target pilot uses

```text
x^S_(n+1) = x^S_n + epsilon_S xi^S_n
             - eta_S grad Phi^S_n(x^S_n) + drive_n,
x^T_(n+1) = x^T_n + epsilon_T xi^T_n
             - eta_T grad Phi^T_n(x^T_n)
             - eta_cross grad Phi^S_n(x^T_n).                 (14b)
```

The source does not read the target, so this is not reciprocal interaction.
The signed cross-channel multiplies the last term by the externally supplied
label product `q_S q_T` with labels in `{-1,0,+1}`. Those labels are test
inputs, not emergent charges. Prescribed external-field tests add a supplied
displacement `+/- f_n` or exactly zero to otherwise paired target paths.

## 4. Implemented field and mediator pilots

### Active scalar field

The one-dimensional periodic active-field pilot integrates

```text
d_t phi = -[1 + a2(-d_x^2) + a4(d_x^4)] phi
           - u phi^3 + s delta_L(x-X_t),
dX_t = -eta d_x phi(X_t) dt + epsilon dW_t.                   (15)
```

Equivalently, the linear growth rate is

```text
sigma(k) = -(1 + a2 k^2 + a4 k^4).                            (16)
```

For `a2<0`, the preferred linear wavenumber is
`k_* = sqrt(-a2/(2a4))`. The cubic term can saturate a finite-`k` spatial
pattern. All linear rates in (16) are real, so this first-order scalar field
does not by itself supply a temporal harmonic mode. The existing `eta=0`
control forms nearly the same field pattern, hence the current pass is not
feedback-specific.

### Local mediator controls

The relaxation-diffusion control is

```text
d_t a = D d_xx a - mu a + s.                                  (17)
```

The telegraph control is

```text
d_tt a + 2 gamma d_t a + omega_0^2 a = c^2 d_xx a + s.        (18)
```

For one Fourier mode, (18) is underdamped exactly when

```text
gamma^2 < omega_0^2 + c^2 k^2.                                (19)
```

Thus the telegraph pilot can carry damped oscillations, but only because a
second-order wave law and its coefficients were supplied. It is currently a
transport architecture control, not a law derived from memory dynamics.

## 5. What is not implemented

The proposed vector-field functional

```text
F[m;J] = integral [a|m|^2/2 + b_L(div m)^2/2
                   + b_T|grad wedge m|^2/2 + c|Delta m|^2/2
                   + u|m|^4/4 - J dot m
                   + chi m dot curl m + ...] dx               (20)
```

is theoretical future work. In particular, `m dot curl m` in this form already
uses oriented three-dimensional structure; it cannot be used as evidence that
the model selected three dimensions.

No currently unified production equation couples (1)-(5), (15), a vector
functional such as (20), and a reciprocal multi-node mediator.

## 6. Why the minimal scalar reduction has no harmonic mode

For a local scalar memory center `m_n` and restoring gain `g=eta kappa`, the
minimal reduction is

```text
x_(n+1) = (1-g)x_n + g m_n,
m_(n+1) = lambda x_(n+1) + q m_n.                              (21)
```

Its multipliers are

```text
mu_1 = 1,
mu_2 = q(1-g).                                                 (22)
```

Both are real. The relative mode is stable when

```text
|q(1-g)| < 1.                                                  (23)
```

It is monotone for `q(1-g)>0` and sign-alternating for `q(1-g)<0`. The latter
is a discrete overshoot or near-period-two response, not a harmonic phase.

With frozen memory and Hessian eigenvalue `h_i`, the multiplier is
`1-eta h_i`; local stability requires

```text
0 < eta h_i < 2.                                               (24)
```

Again this gives monotone or alternating real relaxation.

A genuine damped oscillator requires a conjugate pair

```text
mu_+/- = r exp(+/- i theta),  0 < r < 1,  theta not in {0,pi}. (25)
```

For a persistent neutral oscillation, `r=1`; with noise, a stationary
quasi-cycle normally needs a damped focus plus continuing stochastic drive.

Equations (21)-(24) are not a global impossibility theorem for the complete
finite-history nonlinear system. Its augmented state has many dimensions, and
delayed nonlinear feedback could in principle support a limit cycle or complex
modes. No general parameter inequality for such a branch has been derived,
however, and the fitted complex candidates observed so far failed the raw-mode,
segment-identity, or `eta=0` control gates.

## 7. Minimal mechanisms that could create complex modes

These are hypotheses to test, not current results:

1. **Momentum/inertia.** Add a second state per active direction. For the
   simple discrete update

   ```text
   v_(n+1) = (1-gamma)v_n - kappa r_n,
   r_(n+1) = r_n + v_(n+1),                                   (26)
   ```

   the linear block has determinant `1-gamma` and trace
   `2-gamma-kappa`. It has a stable complex pair when

   ```text
   0 < gamma < 1,
   (2-gamma-kappa)^2 < 4(1-gamma).                             (27)
   ```

2. **Oriented antisymmetric coupling.** A two-component block
   `A=a I+b J`, `J^2=-I`, has multipliers `a +/- ib`. It oscillates when
   `b != 0` and is stable when `a^2+b^2<1`. The origin of `J` must be derived
   or independently justified; inserting a 3D curl would presuppose the
   desired dimension.
3. **Retarded reciprocal coupling.** A delay or local mediator can provide the
   phase lag needed for a Hopf-type instability. It needs independent source
   and target states and controls that remove direct instantaneous readout.
4. **Coupled field components.** At least two fields with a non-symmetric or
   antisymmetric kinetic block can have complex modes. Multiple scalar fields
   with only symmetric gradient relaxation need not do so.

Non-normal transients, metastable switching, moving-center alignment, cadence
aliasing, and finite-window AR leakage can all look oscillatory without
satisfying (25). Existing raw-mode controls already demonstrate this risk.

## 8. Rotation and a falsifiable rank-three mechanism

Rotation does not generally produce three dimensions:

- an elementary rotation in `R^d` occupies a two-plane;
- a single circular orbit is rank two;
- in `d>3`, additional rotation planes and axis wandering are possible;
- an antisymmetric generator has even rank, so pure rotation does not
  naturally select rank three.

A concrete, dimension-independent hypothesis is instead:

```text
effective space = one coherent rotation plane
                  + one independent propagation/normal axis.                (28)
```

For ambient `d in {4,5,7,10,...}`, a future registered test would require:

1. one persistent bivector plane with control-separated coherence;
2. one propagation axis linearly independent of that plane;
3. a stable eigengap after the third response direction;
4. the same rank-three result across seeds, ambient dimensions, windows, and
   at least one held-out parameter slice;
5. failure of rank three when the antisymmetric or delayed coupling is turned
   off.

Without items 1-5, rotation is not a `d=3` explanation.

## 9. Can long runs select the parameters?

Not in the current equations. The tuple

```text
Theta = (epsilon, eta, lambda, M0, K, G, ...)
```

is fixed before simulation. A long run samples `P_Theta`, estimates an
invariant or metastable distribution, and may choose among coexisting
attractors through its initial condition and noise. That is state or branch
selection, not parameter selection.

Self-selection would require at least one additional layer:

- promote selected couplings to slow state variables with explicit update
  laws;
- derive amplitudes and length scales from a conserved resource or constrained
  variational problem;
- define a population/selection dynamics over nodes;
- derive scale-dependent effective couplings through coarse-graining and test
  convergence to a fixed point.

Each option still has inputs. The scientific target is not "no parameters",
but universality: broad microscopic inputs should flow to the same small set of
dimensionless effective observables. Adding adaptive laws merely to force a
desired frequency, dimension, or amplitude would be parameter fitting in
disguise.

## 10. Recommended next discriminating test

Do not launch another ungated scalar long run merely to search for oscillatory
plots. First define one minimal oscillator extension analytically, with the
canonical scalar model as the null. The lowest-assumption candidate is (26),
because it introduces one
missing state variable without assuming three-dimensional handedness.

Pre-register:

- the complex-mode region (27);
- `gamma=0`/`kappa=0` and canonical-scalar controls;
- frequency and damping from direct state-space fits, not only FFT peaks;
- segment identity, cadence stability, and surrogate separation;
- a cross-ambient-dimension rank test only after the oscillator gate passes.

Keep the existing long-run geometry data frozen as an independent baseline.
It remains valuable for scalar relaxation and shape diagnostics, but it cannot
answer a question whose required state variable is absent from the model.
