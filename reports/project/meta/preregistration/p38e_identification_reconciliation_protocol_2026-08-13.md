# P3.8e identification reconciliation protocol

Date: 2026-08-13.

## Status

This is a **post-review technical correction protocol**, not a blind
preregistration. It was written after the historical P3.8e result exposed
identification defects. The correction rules below are fixed before rerunning
the canonical continuations. The historical raw simulation is retained, but
its model-order decision is reclassified as
`superseded-methodologically-inconclusive`.

## Defects that trigger reconciliation

1. The historical "damped AR(2)" and free AR(2) were not independent models.
   Every stable real AR(2) with a complex-conjugate pole pair has the exact
   sampled damped-oscillator representation

   \[
   a_1=2e^{-\gamma\Delta}\cos(\omega_d\Delta),\qquad
   a_2=-e^{-2\gamma\Delta}.
   \]

2. The historical primary response was `active - eta_zero`. A difference of
   two first-order responses can have order two and therefore cannot identify
   the order of the active canonical system.
3. AR(1), AR(2), and AR(8) did not use a common first target.
4. The chronological holdout began after almost all measured signal had
   vanished.
5. The visible coordinate contributed to the coefficient fit instead of being
   an independent readout.
6. Hankel rank was diagnostic only. In addition, the historical matrix placed
   seeds/directions in separate column families. Different residue vectors
   could therefore inflate rank even for one common temporal pole.
7. Formation ages used different future-noise realizations.
8. The five nominal finite-`k` input profiles are strongly correlated for the
   localized states and cannot automatically be interpreted as five
   independent spatial modes.

## Fixed cases and continuations

- canonical scalar-memory snapshots at `d=3`, `A_att=35`, `epsilon=1e-4`,
  `alpha=0.01`, `N=3e6`, formation seeds 1--5;
- the same registered dynamics at `N=1e8`, seed 1, only for an age comparison;
- `k R_mem in {0.5, 1, 2, 4, 8}`;
- central perturbation fractions `{0.005, 0.01}`;
- analysis horizon 600 updates, extinction check at 800 updates;
- output cadence 5 updates and explicit future-noise seed `20260813`;
- the `N=3e6` and `N=1e8` seed-1 cases use the same future-noise array.

The intervention, branch pairing, state constraints, and canonical transition
law remain unchanged. The intervention is still a valid state-space
deformation, not a canonical trajectory-deposition write pulse.

## Corrected identification

Active and `eta=0` arms are fitted separately. For one input `kR`, recurrence
coefficients are learned only from

\[
Y_\rho=(R_{mem}\operatorname{Re}\widehat\rho_c,
        R_{mem}\operatorname{Im}\widehat\rho_c).
\]

The visible relative coordinate

\[
Y_x=(x-\bar x_\rho)\cdot e
\]

is withheld from coefficient estimation and scored using the poles learned
from `Y_rho`. Every model uses targets beginning at sample 8 and the same
60/40 chronological split.

The compared models are AR(1), free AR(2), and AR(8). The genuinely distinct
undamped reference is

\[
y_n=a_1y_{n-1}-y_{n-2},\qquad |a_1|\le 2.
\]

It is reported as a diagnostic. Damping and frequency are interpretations of
the free AR(2) poles, not a second fit and not an additional goodness-of-fit
gate.

The corrected block-Hankel matrix treats every seed/direction/readout as one
component of a common output vector. Only chronological shifts form Hankel
columns. Thus different panel residues do not create artificial temporal
rank.

## Fixed gates

All numerical controls must pass:

- uniform immediate identity error `<=1e-10`;
- full `eta=0` response extinction at update 800 `<=1e-8`;
- strength-linearity error for both diagonal features and complete cross-`k`
  mode matrices: median `<=0.10`, maximum `<=0.25`;
- maximum radius-ratio disturbance `<=0.10`.

For one `kR`, all of the following are necessary:

- memory AR(2) recursive holdout RMSE at least 20% below AR(1);
- held-out visible AR(2) RMSE at least 20% below visible AR(1);
- AR(2) memory and visible RMSE each no more than 10% above AR(8);
- stable, continuously embeddable underdamped AR(2) poles;
- first-two Hankel singular-value energy `>=0.90` and `s3/s2<=0.50`;
- both memory and visible responses remain above 1% of peak into holdout and
  each contributes at least 5% of its scale-balanced energy in holdout;
- the same complete condition passes separately in at least four of five
  formation seeds.

At least four of five `kR` channels must pass for a temporal second-order
candidate. The `eta=0` AR(2)/AR(1) ratio is diagnostic only: passive finite
memory replacement can itself have multi-lag structure, whereas its visible
response is exactly zero.

## Age and spatial qualifications

For each channel, the seed-1 `N=3e6` to `N=1e8` pole shift must not exceed the
maximum pole spread among the five `N=3e6` seeds, and its response-norm ratio
must lie inside the corresponding seed range. Fewer than four age passes label
any temporal result `age-unresolved`; this single paired seed remains a
necessary check, not population evidence.

The weighted input-profile Gram matrix must have median condition number
`<=100` and maximum absolute off-diagonal entry `<=0.95` before the five inputs
can be treated as independent spatial modes. Failure labels any temporal
candidate `spatial-modes-unresolved`. Complete cross-wavenumber responses are
archived and their diagonal fraction remains a separate leakage diagnostic.

## Claim boundary

This reconciliation can select or reject a shared two-pole effective temporal
closure for the tested state intervention. It still cannot establish a
canonical write port, controllability, passivity, a positive storage metric,
microscopic momentum, cross-node mediation, spin, quantization, particle
identity, or dimension selection. Those questions remain separate tests even
if the corrected temporal gate passes.
