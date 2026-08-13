# P3.8e finite-k mechanism-closure preregistration

Date: 2026-08-13. This document fixes the first executable P3.8e gate before
the canonical response data are generated.

## Question and null

Does the mature canonical scalar state `z=(x,rho)` have a feedback-specific
finite-wavenumber impulse response that requires a stable underdamped second
temporal state on chronological holdout?

Primary null: the canonical responses do **not** require a stable reversible
second-order modal realization. Rejecting this null would admit a second
predictive state only up to similarity transformation. It would not establish
microscopic momentum, passivity, a cross-node mediator or physical inertia.

## Fixed data

- mature `d=3`, `A_att=35`, `epsilon=1e-4`, `alpha=0.01` scalar-memory
  snapshots at `N=3e6`, formation seeds 1--5;
- the same registered model and seed 1 at `N=1e8` as a formation-age check;
- every retained memory point and canonical age weight, not compressed
  features, initialize each continuation;
- 20 memory times, a five-update output cadence and fresh explicit common
  random numbers fixed by noise seed `20260813`.

The `N=1e8` row is an age diagnostic, not a sixth independent seed.

## Intervention

For each coordinate direction `e` and each

```text
k R_mem in {0.5, 1, 2, 4, 8},
```

the complete retained path is initialized as

\[
r_j^\pm=r_j\pm\delta e f_k(r_j).
\]

The sinusoidal longitudinal profile is corrected and normalized so that

\[
f_k(r_0)=0,
\qquad
\sum_j w_j f_k(r_j)=0,
\qquad
\frac{1}{M}\sum_jw_j f_k(r_j)^2=1.
\]

Thus `x=r_0`, total memory mass, age weights and weighted memory centroid are
unchanged at intervention. The paired strengths are

```text
delta / R_mem in {0.005, 0.01}.
```

After initialization, both signs and the unperturbed branch use the unchanged
canonical transition law and the same future noise. The exact `eta=0` arm is
run from the same states. The prior uniform weak probe is retained only as the
`k=0` immediate-identity pipeline control.

## Fixed projection

No target pole or frequency is used. For each input channel the readout is

\[
Y_k=\left(
(x-\bar x_\rho)\cdot e,
R_{\rm mem}\Re\widehat\rho_c(k e),
R_{\rm mem}\Im\widehat\rho_c(k e)
\right),
\]

where `rho_c` is centered on its instantaneous weighted centroid. The primary
response is the paired central derivative in the active arm minus the same
derivative in the `eta=0` arm. The full cross-wavenumber Fourier response is
retained to diagnose mode leakage; model order is scored on the same-`k`
readout fixed above.

## Models and holdout

For each `kR`, all five seeds, three directions and three readout components
form one panel. On the same chronological 60/40 split compare:

1. a shared homogeneous AR(1) recurrence;
2. an unconstrained shared AR(2) recurrence;
3. AR(2) restricted to the exact sampling of a damped continuous oscillator;
4. a shared AR(8) delay recurrence.

Scores are recursive holdout rollouts, not teacher-forced one-step fits. A
scale-balanced block-Hankel spectrum with 30 row and 30 column blocks is a
nonparametric diagnostic. `kR=2` is withheld from any later spatial-dispersion
fit; no dispersion fit is authorized unless the temporal gate passes first.

## Fixed gates

Pipeline and perturbation validity require all of:

- uniform immediate identity error `<=1e-10`;
- final dimensionless `eta=0` modal response `<=1e-8` after the retained
  perturbation has left the memory horizon;
- strength-linearity error median `<=0.10` and maximum `<=0.25`;
- maximum paired radius-ratio change `<=0.10`;
- median norm of `(active-eta_zero)` divided by active response `>=0.05`.

For one `kR` channel, the necessary temporal pass requires all of:

- AR(2) recursive holdout RMSE at least 20 percent below AR(1);
- damped AR(2) RMSE no more than 10 percent above unconstrained AR(2);
- AR(2) RMSE no more than 10 percent above AR(8);
- stable unconstrained and damped poles;
- an underdamped damped-AR(2) solution.

At least four of five `kR` channels must pass. Failing this gate retains the
canonical null and keeps P3.8d classified as a constructed model extension.
Passing only authorizes pole/residue, cadence, age, dispersion-holdout,
power-port and positive-storage tests without gain retuning.

## Claim boundary

This experiment can identify a useful second predictive state in the tested
projection. It cannot by itself establish a field at every spatial point,
cross-node causation, conserved momentum, spin, quantization, particle
identity, ambient dimension selection or a fundamental physical constant.
