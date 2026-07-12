# Kernel, Memory, and Photon-Track Decision Note

Date: 2026-07-07.

## Scope

This note curates the current interpretation after the 15-seed knot-score
extension and the corrected scalar ballistic probe. It is a project-decision
note, not a new physics claim.

## Kernel Decision

The GitHub-side kernel observation is important: in the current parameter
slice, the nominal two-scale baseline kernel is not empirically distinguished
from the `single_scale` condition. The 15-seed v0.4 score reports show equal
median scores for `baseline` and `single_scale` at both 1M and 100M updates.

The working conclusion is:

- do not claim that a two-scale kernel is necessary for Paper I;
- keep the canonical Paper-I mechanism as feedback confinement from an effective
  memory-induced kernel;
- retain two-scale kernels as optional extensions for bifurcation, shape control,
  or later multi-mode structure;
- use `amplitude_rep = 0` as a true dispersive ablation to test whether the
  locally restoring term is the whole confinement mechanism.

A useful technical simplification is to treat the current baseline as an
effective one-kernel model unless an ablation separates it. If
`sigma_att = sigma_rep`, the two-scale expression collapses algebraically to a
single Gaussian with amplitude `A_rep - A_att`, so equal or near-equal scales
should not be sold as a distinct two-scale mechanism.

## Naming Caveat

The current Gaussian-gradient implementation returns an outward vector away
from the memory cloud. Under the canonical overdamped update

```text
x[n+1] = x[n] - eta * grad
```

that outward gradient becomes locally restoring. Therefore labels such as
`repulsive` and `attractive` can be misleading unless the update sign is stated.
For future text, prefer operational names:

- local restoring component;
- long-scale correction component;
- dispersive ablation;
- feedback confinement.

## Memory Decision

Scalar memory density is sufficient for Paper 0 and Paper I. It gives a clean
Markovian embedding and measurable metastable confinement. It is probably not
sufficient for photon-like or oscillator-like dynamics.

For later photon or QFT-style tracks, use a multi-channel memory field, for
example

```text
rho[n+1]^a(x) = (1 - lambda_a) rho[n]^a(x) + beta_a q[n+1]^a G_sigma(x - x[n+1])
```

where `a` indexes internal channels such as phase quadratures, polarization-like
components, or velocity-coupled modes. The augmented state remains Markovian,
but the memory can now encode more than scalar occupancy.

Minimal candidate extensions:

1. second-order state: `(x_n, v_n, rho_n)` with velocity persistence;
2. phase memory: two channels for cosine/sine or real/imaginary phase;
3. vector memory: transverse components coupled through an antisymmetric or
   rotational response;
4. multi-knot response memory: separate internal and external observables for
   synchronization tests.

A harmonic oscillator requires either inertia or an antisymmetric/phase-like
component. A purely scalar overdamped gradient flow naturally produces real
relaxation modes, not sustained oscillation.

## Photon Initial Conditions

Prepared photon-like initial conditions are legitimate as experiments, but they
must be labelled as state preparation rather than spontaneous emergence. This is
analogous to fixing a seed or preparing a wave packet.

Recommended protocol:

- define a controlled initial state with direction, width, and phase/polarization
  channels;
- compare against random-seed and no-phase controls;
- require persistent ballistic propagation or a stable oscillatory observable
  before mapping to physical constants;
- only after a dimensionless regime exists, introduce scale maps such as
  `E = hbar omega` or `L/T = c`.

Do not calibrate parameters directly from `hbar nu`, `mc^2`, or large/small
number numerology until the dimensionless model already has the qualitative
mode being calibrated.

## Near-Term Priority

For the repository, the next clean branch of work is:

1. Paper I: simplify the claim to effective-kernel feedback confinement against
   `eta_zero`.
2. Kernel audit: run or curate `amplitude_rep = 0` as the dispersive ablation.
3. Photon track: open a separate extended-memory prototype with `(x, v, rho)`
   or phase/vector memory, using the scalar ballistic probe as a negative
   control.