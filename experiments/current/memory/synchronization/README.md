# Synchronization and External Response

Status: active measurement programme.

The package diagnostics live in `src/emergenz_knoten/synchronization.py`.
Complete retained-memory states and rigid placement are implemented in
`src/emergenz_knoten/state.py`; paired weak pulses live in
`src/emergenz_knoten/weak_probe.py`, and localized fixed-source continuation
lives in `src/emergenz_knoten/frozen_source.py`. One-way dynamic-source
continuation and relational orbital observables live in
`src/emergenz_knoten/coupled_nodes.py`. The separately relaxing
passive vector source and its paired one-way controls live in
`src/emergenz_knoten/oriented_source.py`. Synchronous off/one-way/reciprocal
full-knot continuations live in `src/emergenz_knoten/reciprocal_nodes.py`;
their constrained real 2 x 2 relative-state fit is implemented in
`src/emergenz_knoten/reciprocal_diagnostics.py`.

## Core Question

```text
Do two or more metastable knots develop reproducible collective modes in a
common low-dimensional external response sector?
```

This question replaces the weaker requirement that one trajectory or memory
cloud have an occupancy dimension near three. Exact rank three is not assumed.

## Experimental Ladder

1. Complete-state placement: transform visible position and every retained
   memory point together. Verify self-force and shape equivariance.
2. Uniform weak-probe calibration: `+delta`, `-delta`, and unprobed branches
   share future noise; `eta_zero` measures the bare direct response.
3. Frozen localized source: clone and translate a full source-knot state, then
   perturb its location while the target remains dynamic.
4. Static field and distance audit: measure potential, radial drift, parity
   residuals, kernel resolution, and target deformation before interpreting an
   apparent attraction.
5. Independent scalar cross-readout: separate the autonomous self-kernel from
   spatial cross-resolution and compare rigid source orientations with a point
   monopole at matched centre response.
6. Ordered-history current audit: derive polar displacement/unit currents and
   antisymmetric circulation from adjacent retained points; compare both with
   an independent-sign null before adding a new state.
7. Independent oriented state: low-pass the source step direction in a separate
   vector-memory fibre and test it against depositwise sign randomization plus
   a one-step-memory control.
8. Fixed-coupling independent pairs: cycle source/target formation seeds,
   prohibit pairwise calibration, and require a controlled distance decay.
9. Signed scalar cross-channel: separate source sign from the non-negative
   self-confining memory and require `q=0` plus sign-reversal controls.
10. One-way dynamic coupling: source evolves but does not read the target.
11. Nondestructive source transport: preserve source shape against a paired
    unlaunched continuation before interpreting target response.
12. Direct reciprocal coupling: compare off, one-way and synchronous arms
    under common node-specific future noise before opening retardation.
13. Shared memory only as a later, separately normalized model variant.

## Completed Uniform Calibration

The 2026-07-16 pilot reused the complete 600-point final memory buffers from
the `N=3M`, `A_att=35`, `epsilon=1e-4`, `d=3/10`, seeds `1..5` runs.

- probe displacement fractions: `0.03` and `0.10` initial memory radii;
- pulse duration: one memory time;
- lags: `0, 0.25, 1, 3, 10` memory times;
- maximum bare-position identity error: `4.7e-12`;
- maximum even probe-induced radius disturbance: `1.8e-6`;
- memory-centre residual: isotropic full rank (`3` in `d=3`, `10` in `d=10`);
- shape residual: no seed-reproducible sign-flip rank and decay to numerical
  scale by ten memory times.

This is a negative control for low-dimensional inference from a uniform force.
The direct field spans the supplied basis by construction. The first
relationally meaningful rank test is therefore the localized frozen source.

Report: `reports/response/calibration/weak_probe_calibration_2026-07-16.md`.

## Frozen-Source Implementation

`frozen_source_response.py` loads the checksum-validated `N=100M` checkpoints,
uses the same complete state as target and rigidly translated source, and places
one unperturbed source at a fixed reference offset. The complete source state is
then translated locally by `+delta/-delta` along each basis direction. Perturbed
branches, the baseline-source branch, and a free no-source branch share future
noise. Self-coupling `eta` and source cross-coupling `eta_cross` remain separate.
`eta_cross=0` must reproduce every free path exactly; `eta_zero` retains the
localized source force and provides the bare-response control. One fixed
interaction strength is calibrated from the baseline source force; two local
translation scales test finite-difference convergence before any independent-seed
or dynamic-source claim.


## Clone-Pilot Result

At one effective `sigma_rep`, the calibrated source is thousands of target
memory radii away. The `d=3` and `d=10` center Jacobians are correspondingly
full ambient rank and split into one radial plus `d-1` nearly degenerate
transverse sectors. This is an isotropic scalar far-field response, not an
external-dimension measurement.

Report: `reports/response/calibration/frozen_source_pilot_2026-07-16.md`.

## Field Audit and Distance Ladder

The 2026-07-17 static audit evaluates the complete retained `N=100M` source
states. In the canonical `A_rep=1`, `A_att=35`, `sigma_att/sigma_rep=3` slice,
the attractive curvature dominates already at the origin and the point-source
force has no sign crossing. Every audited direction is inward from `5 R_mem`
through `1 sigma_rep`.

The source radius is only about `2.1e-4 sigma_rep` in `d=3` and
`3.8e-4 sigma_rep` in `d=10`. Directional, tangential, parity-odd, and
point-monopole residuals are at numerical scale even at `5 R_mem`. The current
read kernel therefore does not resolve the internal source shape.

The paired distance ladder calibrates every separation to the same realized
bare displacement (`0.03 R_mem` per memory time) under common future noise.
Center and shape Jacobians remain full ambient rank at all six distances.
Near-field target deformation is distance dependent but remains below `0.002`;
this is a small tidal/nonlinear target effect, not source-structure resolution
or an external-dimension signal. These are pathwise results from one canonical
checkpoint per dimension.

Reports: `reports/response/calibration/frozen_source_field_audit_2026-07-17.md` and
`reports/response/calibration/frozen_source_distance_ladder_2026-07-17.md`.

## Independent Cross-Readout Gate

The package now distinguishes the source self-kernel from an explicit
`ScalarReadoutKernel`. Omitting it is exactly backward compatible. Supplying a
different cross-readout changes only the target response; the autonomous source
path is unchanged. Every resolution is calibrated to the same bare centre
response, so readout width is not confounded with force magnitude.

The preregistered static ladder rotates the complete `N=100M` source along its
principal axes and compares its drift field with a point monopole. The primary
shape signal is the largest orientation-dependent drift difference divided by
the point drift. A 1% exploratory threshold and a minimum centre separation of
1.25 combined memory radii decide whether a scalar shape signal exists before
opening a local/retarded mediator or oriented-memory branch. This is a
pipeline gate from one checkpoint per dimension, not interaction evidence.

The clean 2026-07-21 run fails that gate in both audited embeddings. At the
closest eligible separation (`sigma_rep/R_mem=2.5`), orientation spread is
`1.96e-3` in `d=3` and `4.32e-4` in `d=10`; the corresponding calibrated
orientation-dependent displacements are `5.98e-5` and `1.52e-5 R_mem` per
memory time. The original self-readout remains pointlike at `2.15e-10` and
`3.01e-10`. No finite-source or orientation onset reaches 1% before the
chosen distinctness boundary.

Decision: the next relational-shape mechanism is an oriented memory/current
channel, not another direct scalar readout narrowing. A local or retarded
scalar mediator remains deferred for a separate locality or propagation-time
question. This pathwise result does not rule out scalar near-field structure
for other independently formed knots.

Report: `reports/response/scalar/scalar_cross_readout_resolution_2026-07-21.md`.

## Ordered-History Current Audit

Before adding a new state, the retained scalar history was tested as both a
polar adjacent-point current and an antisymmetric circulation bivector. The
conditional null independently flips current signs while preserving positions,
magnitudes, memory weights, read kernel, and checkpoint.

At the primary `sigma/R_mem=2.5`, polar coherence reaches only `0.474` and
`0.168` of the 99% sign-null threshold in `d=3/10`. Bivector coherence reaches
`0.626` and `0.743`. Directions remain stable toward `sigma/R_mem=5`, but
neither amplitude is null-separated. This is negative pipeline evidence from
one checkpoint per embedding, not a general no-go theorem.

Decision: the scalar history is not simply relabelled as a coherent vector
source. The next gate uses an independently evolving oriented state, at least
six formations, common future noise, channel-off and randomized-deposit
controls, and a relational angular/transverse primary observable.

Report: `reports/response/one_way/oriented_history_current_audit_2026-07-21.md`.

## Independent-Oriented-State Gate

`oriented_source.py` adds one passively generated state without changing the
scalar source trajectory:

```text
u[n+1] = (1-kappa) u[n] + kappa normalize(x[n+1]-x[n])
p[n+1] = (1-lambda_v) p[n] + lambda_v M_v u[n+1] G_v
x_T[n+1] = F_scalar(x_T[n], rho_T[n], xi_T[n]) + eta_v p[n](x_T[n])
```

The primary arm fixes `kappa=lambda_v=alpha=0.01`, `M_v=1`,
`sigma_v/R_mem=2.5`, source separation `2.5 R_mem`, and 20 vector-memory times.
Six independent `d=3`, `N=3M` formation states are continued with common
future source and target noise. Coupling is calibrated once per realized
formation, before continuation, to `0.03 R_mem` per persistent memory time.

Paired controls are an exact channel-off path, global vector-sign reversal,
16 depositwise random-sign paths, and a `kappa=lambda_v=1` one-step arm with
the same coupling and future noise. The primary statistic is active response
divided by the conditional random-sign q95. A seed passes only when that ratio
is at least 2, the persistent/one-step ratio is at least 1.25, response exceeds
`1e-3 R_mem`, sign reversal and transverse-fraction gates pass, and source and
target remain within the preregistered shape bounds. Overall pass requires 5/6
seeds.

The clean run at revision `4847040` passes in all six seeds. The persistent
active/random-q95 separation spans `5.76..11.64`, versus `1.40..2.04` for the
one-step arm; their ratio spans `3.50..8.05`. Active displacement is only
`0.0040..0.0076 R_mem`, global sign reversal is antiparallel to numerical
precision, and the tangential fraction is `0.584..0.953`. Relative target
radius/tensor disturbances stay below `2.6e-4`/`7.0e-4`; the autonomous source
radius and normalized shape-spectrum drifts remain below `0.129` and `0.132`.

This is a successful constructed-mechanism gate, not an emergence claim. The
orientation lifetime and instantaneous direct vector readout are inserted by
construction. The response was normalized by the same predefined formula for
each realized formation, and source/target are cloned within each seed. The
next test therefore fixes one global `eta_v`, pairs different formation seeds,
uses a larger randomized null, and applies a fixed distance ladder before any
local/retarded field extension. No reciprocal coupling, AR mode fit, photon,
spin, charge, or particle interpretation follows.

Report: `reports/response/oriented/oriented_vector_one_way_gate_2026-07-25.md`.

## Fixed-Coupling Independent-Pair Gate

The follow-up freezes `eta_v=5.079e-6` for every case and pairs the six
formation seeds cyclically (`1<-2`, ..., `6<-1`). It uses
`R_pair=(R_source+R_target)/2`, the fixed width rule
`sigma_v=2.5 R_source`, and distances `2.5, 5, 10 R_pair`. The 64 random-sign
paths, channel-off, global flip, and one-step arm share future noise and sign
realizations across distances.

The near gate retains response, random-null, persistence, flip, and shape
thresholds. Tangential fraction is diagnostic rather than a gate because an
independently formed source orientation has no required angle to the arbitrary
pair axis. The distance gate allows 10% monotonic tolerance and requires the
far/near response ratio to be at most 0.1; at least 5/6 pairs must pass.
No pairwise retuning is permitted. A pass opens only a local/retarded mediator
test, not reciprocal coupling or a QFT/particle interpretation.

The clean run at revision `3df1c94` passes all six cyclic pairs. Near active
response is `0.00177..0.00777 R_target`, active/random-q95 is `3.16..11.70`,
and persistence gain over the one-step arm is `2.25..8.64`. Far/near response
is `9.36e-4..2.80e-3`; flip and all source/target shape bounds pass. One pair
has tangential fraction `0.341`, confirming why angle to the arbitrary pair
axis is not a universal gate.

This result removes clone-specific and pairwise-coupling calibration as the
immediate explanations for the controlled response. It does not validate
locality: the instantaneous Gaussian readout already imposes the measured
distance decay, and `sigma_v=2.5 R_source` remains a state-scaled rule. The
next gate compares the full relaxation-diffusion peak law with the finite-front
onset of a damped wave/telegraph mediator on held-out pairs and distances.

Report: `reports/response/oriented/oriented_vector_fixed_pair_distance_gate_2026-07-26.md`.

## Local-Mediator Gate Result

`local_mediator.py` now supplies two explicit local finite-difference Markov
extensions on the source-target axis. `external_field_response.py` applies a
prescribed time-dependent field to active, global-sign-flip, and exact
channel-off target branches under common future noise. The axis is a
resource-light relational transport channel, not an ambient-dimension model.

The first independent pair and nearest distance fix one absolute length
`R0`, one common correlation length `5 R0`, one nominal relaxation time of ten
memory times, and one coupling per mediator law. The remaining pair-distance
cases are holdouts; no pair-radius renormalization or coupling retuning is
allowed. A one-memory-time rectangular source pulse is observed for fifty
memory times. A factor-two spatial refinement with four mediator substeps per
target update is the resolution control.

The earlier shorthand `t_peak~r^2` requires correction once relaxation is
nonzero. For

```text
G(r,t) ~ t^(-1/2) exp[-r^2/(4Dt)-mu t]
```

the short-pulse peak is tested against

```text
t_peak ~= [sqrt(1 + 4 mu r^2/D) - 1]/(4 mu) + T_pulse/2,
```

which crosses from quadratic near-field to linear far-field behavior. The
telegraph arm instead tests its relative-threshold onset against `r/c`.
Passing either arm establishes only implementation and knot-envelope
compatibility: the corresponding transport behavior is inserted by the model.
A dynamic autonomous source waveform is needed before the laws can be
empirically discriminated, and reciprocal coupling stays closed.

The clean run at revision `64c2826` passes both inserted architectures. The
relaxation-diffusion arm has median/maximum holdout lag errors of
`1.12%/9.09%` and maximum primary/fine resolution drift `0.31%`; the
telegraph arm has `5.55%/7.88%` and `4.91%`. Both pass all five complete
holdout pairs. Across all target cases, final response is
`8.37e-4..8.96e-3 R_target`; paired shape and radius changes remain below
`3.72e-4` and `1.31e-4`.

Decision: **architecture pass, mechanism underdetermined**. A next dynamic
run is conditional on an identifiability audit: the autonomous oriented source
must have controlled spectral power in bands where the analytic diffusive and
telegraph transfer functions differ measurably. Otherwise both simulations
would merely replay behavior inserted by construction.

Report: `reports/response/oriented/local_oriented_mediator_gate_2026-07-28.md`.

Introducing a field does not select three dimensions. The current knot states
remain in the supplied `d=3` embedding while the mediator uses one relational
axis. A later dimension gate must freeze one law across several ambient `d` and
test whether a control-separated external response or slow-mode rank converges
to three while extra directions are suppressed.

## Autonomous-Source Identifiability Preregistration

`oriented_source_mediator_identifiability.py` is the stop gate before another
constructed propagation run. It continues each of the six inherited source
states autonomously after a 20-memory-time burn-in and estimates vector power
from two non-overlapping Hann-windowed segments of 8192 updates. The persistent
carrier is primary; unit one-step direction is a diagnostic comparator only.

The comparison uses exact discrete impulse responses from the already frozen
mediator grids at all 18 inherited distances. Each model-distance response is
normalized to unit finite-horizon DC gain, so no amplitude coupling is fitted.
Eligibility requires at every distance source-weighted complex transfer
contrast at least `0.25`, at least `0.20` of output power in frequency bins
with contrast at least `0.25`, transmitted power fraction at least `0.01`, and
two-segment contrast drift at most `0.25`. Carrier RMS and the established
source radius/shape bounds must also pass; overall pass requires 5/6 sources.

A pass means only that a common autonomous input can expose different model
predictions. It does not choose diffusion, Telegraph transport, persistent
memory, or a physical field law. A fail stops the dynamic comparison instead
of opening a source or mediator parameter sweep.

Canonical result at clean revision `3619401`: all six sources pass at every
inherited distance. Minimum weighted complex contrast is `1.064`, minimum
distinguishable output-power fraction `0.9969`, and maximum segment drift
`0.1568`. Persistent/one-step contrast is only `0.951..1.008` (median `0.991`).
The persistent state shifts power toward low frequencies but is not specifically
needed to distinguish these two deliberately different transfer rules.

Report: `reports/response/oriented/oriented_source_mediator_identifiability_2026-07-28.md`.

## Dynamic Common-Source Gate

`dynamic_common_source_mediator_gate.py` uses the eligibility pass without
opening another coupling or source sweep. Each ambient source-vector component
drives an independent copy of the same relational 1D mediator. The six cyclic
pairs, three distances, mediator grids and pulse-calibrated couplings are
inherited unchanged.

Source, mediator and target evolve for 20 memory times before a 50-memory-time
analysis window. Persistent and unit one-step inputs are run with common target
noise; the one-step amplitude is deliberately not matched after seeing data.
Active, global flip and exact off branches define RMS response, pathwise odd
residual and paired radius/shape disturbance. Persistent response must remain
between `1e-4` and `0.1 R_target`, far/near at most `0.5`, and the two model
response traces must differ by at least `0.25` relative RMS at every distance.
At least 5/6 pairs are required.

The gate can reject dynamic architectures. Without an independent measured
target trajectory, it cannot promote a surviving architecture to a physical
field law or open reciprocal coupling.

Canonical result: both rules pass response, oddness, source/target shape and
attenuation in all 6/6 pairs. The stricter cross-model trace-separation gate
is passed at all three distances by only 4/6 pairs, below the preregistered
5/6. The nearest distance is limiting; all six pairs separate at `5` and
`10 R_pair`.
The result is therefore negative for robust mechanism discrimination, not a
failure of either numerical field implementation. No coupling is retuned.

Because the implementation applies the same scalar transfer independently to
every ambient component, its component-space transfer is `H I_d`. It preserves
the rank of a full-rank source covariance wherever `H` is nonzero and therefore
cannot by itself select three directions from a larger supplied ambient space.

Report: `reports/response/oriented/dynamic_common_source_mediator_gate_2026-07-28.md`.

## Interaction-Sign Decision

The implemented memory weights are non-negative. The current cross-field is
therefore an unsigned scalar monopole and has no knot-specific charge label.
This is parity-even, not parity-free: spatial parity and charge sign are
different symmetries. Charge neutrality would suppress a signed monopole; it
would not explain the universal attraction measured here.

The minimal charge-like test is a separate signed scalar cross-channel while
the established scalar self-confinement channel stays unchanged. Vector memory
is reserved for observables that actually require orientation, phase,
circulation, or polarization.

## Completed Signed-Channel Architecture Gate

`signed_cross_channel.py` implements an externally assigned
`s_target*s_source` factor only in the frozen-source cross force. The cross
potential uses the broad zero-integral, curvature-matched third scale; the
target self-channel remains the canonical non-negative scalar memory.

The 2026-07-18 pilot on the checksum-validated `N=100M` checkpoints in `d=3`
and `d=10` gives:

- bitwise identity of source-zero, target-zero, and explicit free paths;
- bitwise identity for equal label products;
- pulse-response reversal when the label product changes sign;
- maximum radius disturbance below `4.5e-5`;
- active pulse displacement about `0.00136 R_mem` versus the calibrated
  `eta=0` displacement about `0.03 R_mem`.

This validates the software and control architecture only. There is one
checkpoint per dimension, the labels are inputs rather than emergent
observables, and the source is frozen. The next gates are 6-10 independent
states without retuning and fixed-coupling distances below and above the
compensated force crossing.

Report: `reports/response/scalar/signed_scalar_cross_channel_pilot_2026-07-18.md`.

## One-Way Dynamic-Source Gate

`one_way_dynamic_source_pilot.py` continues one autonomous source and four
common-target-noise paths: dynamic source, frozen source, free target, and
eta-zero target. Relative velocity is decomposed into radial and tangential
components; the antisymmetric tensor `r wedge v` measures orientation without
assuming three dimensions.

The autonomous source moves only `1.6..4.5` internal radii in 200 memory
times, while one `sigma_rep` is about 4724 radii. Dynamic-minus-frozen target
motion remains `2.1e-5..6.8e-5` radii, and angular coherence and dephasing do
not separate from the free control.

A paired point launch of `0.1 sigma_rep` over ten memory times produces
`10.944` radii of additional source-centre displacement, but only
`3.137e-4` radii of target response. Its source radius differs from the
identical unlaunched continuation by `46..59%`. The imposed drive therefore
does not transport an intact knot. This blocks a positive source-transport
interpretation. A later direct reciprocal arm is opened only as an analytically
registered real-mode null and nonlinear reconciliation test.

Reports: `reports/response/one_way/one_way_dynamic_source_pilot_2026-07-20.md` and
`reports/response/one_way/one_way_launched_source_pilot_2026-07-20.md`.


## Direct Reciprocal Full-Knot Gate

`reciprocal_full_knot_gate.py` tests the analytic local-mode prediction on the
complete `d=3`, `N=100M` finite-memory checkpoint. Two rigid copies start at
`2.5 R_pair`; five independent future-noise pairs are shared across
channel-off, one-way and synchronously reciprocal conditions. The registered
finite-horizon cross gain is `c=0.02` (`cross_eta=0.006939767`) and is not
calibrated per future seed.

After a 100-memory-time exclusion, four non-overlapping segments per arm fit
one isotropic real 2 x 2 map to `(x_-,m_-)`. All 60 segment fits are real.
Thus `0/5` seeds in every arm pass the complex-mode identity gate. This is not
a threshold artifact: there are no raw non-real segment pairs to filter.

The channel is nevertheless active and nondestructive under the registered
shape bounds. Reciprocal response and shape gates pass 5/5; final reciprocal
centre separation is `0.31..0.88 R`, versus `2.78..9.21 R` for channel-off.
The supported reading is direct scalar binding/relaxation, not oscillation,
orbit, spin or dimension selection. The five paths share one formation basin;
independent mature formations remain necessary for a basin-level claim.

Report: `reports/response/reciprocal/reciprocal_full_knot_gate_2026-08-04.md`.

## Retarded Reciprocal Full-Knot Gate (P3.2)

`retarded_reciprocal_full_knot_gate.py` inserts exactly one previously tested
local mediator into the P3.1 cross-readout: the Telegraph field/momentum law.
The choice is fixed before the result because it has an explicit local
propagation state; the parabolic relaxation-diffusion alternative has
instantaneous continuum tails. This is a model-selection convention for the
test, not evidence that the Telegraph law is physical.

The P3.1 gain remains `c=0.02`. In inherited dimensionless units the channel
uses correlation length `5R`, relaxation time `10` memory times, grid spacing
`0.25R`, and fixed readout distance `2.5R`. Its finite-grid stationary readout
is solved and normalized to unity, so no response matching or gain retuning is
performed. Channel-off, the exact instantaneous reciprocal P3.1 arm, and a
retarded one-way arm are common-noise controls.

The mediator input is nevertheless the target-specific instantaneous
cross-gradient evaluated from the current source memory. The experiment makes
only the inserted transport/filter state local; it is not yet a fully local
source-emission field theory.

The primary gate is still the observable relative `(x_-,m_-)` fit across four
post-transient segments and five future-noise continuations. Complex internal
Telegraph poles are present by construction and do not count. The fixed
one-dimensional relation axis carries vectors in supplied `d=3`; it does not
select dimension or prove a continuum causal speed.

The canonical five-seed, 500-memory-time run is operational but negative for
the primary mode hypothesis. Mediator response, knot response, and the shape
envelope pass 5/5. All 80 raw segment fits across off, direct reciprocal,
retarded one-way, and retarded reciprocal arms are real. Final separation is
`0.58..1.21R` with retardation versus `0.31..0.88R` directly. Thus the fixed
delay weakens or postpones binding but does not create an observable AR(1)
rotation in this formation basin.

Report: `reports/response/reciprocal/retarded_reciprocal_full_knot_gate_2026-08-04.md`.


## Measurement-Closure and Relative-Noise Gate (P3.2a/b)

`measurement_closure_relative_noise_gate.py` keeps the P3.2 checkpoint,
kernel, `lambda`, `epsilon`, gain, distance, and Telegraph mediator fixed.
It changes measurement and excitation only:

- target field and conjugate-momentum readouts augment `(x_-,m_-)`;
- one panel transition is shared across ambient coordinates with
  coordinate-specific fixed effects;
- closure samples are spaced by 50 updates, or 0.5 memory times;
- delay depths are `1,2,5,10,20`, with a chronological 60/40 train/test
  split and one common held-out target window across all depths;
- only held-out prediction of `(x_-,m_-)` is scored against persistence;
- the pure `(x_-,m_-)` delay ladder, the readout-augmented ladder, and a
  separate full `2d x 2d` ambient AR(1) fit remain distinct diagnostics.

Predictive closure requires at least 10% improvement over persistence and a
depth-10/20 residual change no larger than 10%. Spectral identifiability is a
separate gate because a predictive high-dimensional delay fit can remain too
ill-conditioned for eigenvalue interpretation. A complex candidate must be
stable across depths `5,10,20` and at least three of four time segments.

The relative-noise ladder uses `rho={0,0.9,0.99}` for three future seeds:

```text
xi_1 = sqrt((1+rho)/2) xi_c + sqrt((1-rho)/2) xi_r
xi_2 = sqrt((1+rho)/2) xi_c - sqrt((1-rho)/2) xi_r
```

Each node therefore retains unit innovation variance while the relative
half-noise scales as `sqrt(1-rho)`. Channel-off, instantaneous reciprocal,
and retarded one-way remain controls. A passed readout-delay gate is only
empirical predictive closure at this cadence and horizon: the full mediator
grid remains hidden, and no exact Markov, spin, dimension, or particle claim
follows.


The canonical three-seed result is **predictive closure with a
non-identifiable augmented spectrum**. The visible delay state is
well-conditioned (`kappa=46.8..81.0`) and has no depth-stable matching
segments. Adding field and momentum changes held-out error by only
`-1.94%..+0.20%`, while its delay matrix has
`kappa=1.55e16..1.93e16`. Complex poles matched in 33/36 augmented
segments therefore remain inserted-mediator/rank-deficiency artefacts, not
knot modes. Lower relative noise tightens reciprocal binding but reveals no
control-separated mode.

Report:
`reports/response/reciprocal/measurement_closure_relative_noise_gate_2026-08-04.md`.

### Registered long-horizon follow-up

The short ladder changes both predictor count and available training targets.
Its slight increase in held-out RMSE/persistence therefore cannot be
extrapolated as physical persistence. The registered follow-up uses the same
fixed P3.2 model with `N=150000`, seeds `1,2,3`, `rho={0,0.9,0.99}`, 100
memory-times burn-in, and unchanged 50-update cadence. Delay depths
`{20,50,100,150,200,250}` span 1000..12500 updates. Every depth predicts the
same train and holdout target times.

Visible and field/momentum-augmented states are fitted at fixed truncated
Hankel ranks `{2,4,8,16,32}` in retarded reciprocal and one-way-control arms.
A material trend requires median terminal-minus-initial RMSE/persistence of at
least `0.02` in magnitude and 80% path/rank sign agreement. This stage tests
long-history predictive benefit and rank growth only. Reduced DMD poles are
stored but cannot pass a mode gate until they are stable across ranks, depths,
time segments, and the one-way control.

Preregistration:
`reports/project/meta/preregistration/long_horizon_hankel_preregistration_2026-08-04.md`.

The canonical clean-start result classifies **longer history as degrading
held-out prediction**. All 45 paired seed/rho/rank design-cell deltas from
1000 to 12500 updates are positive, as are all three independent seed medians;
the cell median is `+0.1203`. Median visible stable/entropy rank
grows from `1.67/6.62` to `5.87/49.4` instead of plateauing. At retained ranks
16 and 32, the terminal reciprocal-minus-one-way ratio difference remains
within `-0.00366..+0.00244`. Field/momentum augmentation does not reverse the
degradation. This supports fixed-rank information dilution under accumulating
stochastic history, not a longer physical persistence scale or oscillatory
closure.

Result:
`reports/response/reciprocal/long_horizon_hankel_gate_2026-08-04.md`.

### Stored-pole identity stoptest

The preregistered postprocessor tests only the well-conditioned visible-state
poles at ranks `{8,16,32}` and depths `{100,150,200,250}`. A track needs at
least 10/12 matching cells, two independent seeds at every paired noise
correlation, and fewer than 6/12 matches in the retarded one-way arm.

Seeds 1 and 2 contain a recurring pole near `omega=0.103` per memory time, but
the same pole matches 6..8/12 one-way cells. Seed 3 reaches only 9/12 reciprocal
cells. Four cross-correlation candidates survive identity matching and zero
survive the control gate. P3.2 therefore closed without authorizing a 500,000-update confirmation. A
later user-requested two-path accumulation control was nevertheless run. It
found large off-subtracted path divergence in the reciprocal arm, but nearly
the same divergence in the one-way control; the registered accumulation and
complex-mode gates both fail. This does not reopen P3.2. A 500,000-update run
remains the minimum confirmation horizon for a later mechanism that first
passes its stored-data or analytic control gate.

Preregistration and result:
`reports/project/meta/preregistration/hankel_pole_identity_preregistration_2026-08-04.md` and
`reports/response/reciprocal/hankel_pole_identity_audit_2026-08-06.md`.

### Source-local linear emission gate (P3.2c)

The preregistered linear stoptest removes the hidden target dependence from the
P3.2 source. It emits only quantities available at the source: constant memory
mass as a dynamic null, the translation-invariant offset `d=x-m`, and the local
step current `d/q-d_previous`. The target only reads the fixed Telegraph field
at its endpoint. The positive update sign is the reporting primary; the opposite sign is a
symmetry control. Both fail by wide margins, so the conclusion is sign-invariant.

The exact 598-state finite-grid channel and source/readout-ranked Dirichlet
reductions of orders 8, 16, and 32 are stable. The primary offset has a complex
pole near `omega=0.08294` per memory time, but normalized knot residue is only
`3.54e-5` and relative generator shift from the nearest one-way channel pole is
only `0.00622`, versus registered thresholds of `0.1`. Current emission is
about two orders of magnitude weaker. Thus this is an inserted channel pole,
not a materially loaded reciprocal knot mode. No 500,000-update confirmation
is authorized for this mechanism.

Preregistration and result:
`reports/project/meta/preregistration/source_local_linear_gate_preregistration_2026-08-06.md`
and `reports/response/source_local/source_local_linear_gate_2026-08-06.md`.

### Autonomous shape-multipole eligibility (P3.2d)

The older traces did not persist the full time-dependent shape tensor, so the
registered stored-data question required one minimal autonomous reproduction
from the mature `d=3`, `N=100M` checkpoint. No interaction channel or mediator
was inserted. Five paired future-noise paths compare the scalar baseline with
`eta=0`; a one-memory-time block-shuffle supplies a second null.

All five baseline paths remain shape-bounded. The normalized centered
traceless tensor `Q` has strong low-frequency power near the lower analysis
boundary, but its peak frequency fails segment identity in every baseline
path. The same low-frequency structure is stronger under `eta=0`, where two
single paths pass. The rate `Delta Q/Delta tau` passes in no baseline path.
Thus neither source passes the registered seed/segment/control gate, and no
tensor mediator is authorized.

Preregistration and result:
`reports/project/meta/preregistration/p32d_shape_multipole_preregistration_2026-08-06.md` and
`reports/response/source_local/p32d_shape_multipole_gate_2026-08-06.md`.

## Observables

A target knot provides:

- co-moving visible and memory centres;
- weighted memory shape tensor and radius;
- delayed centre and shape response matrices;
- odd central response `(+delta - -delta)/(2 delta)`;
- even disturbance `(+delta + -delta)/2` against the unprobed path;
- residence or identity-loss diagnostics for later multi-knot runs.

Response rank has two distinct meanings:

- descriptive energy rank from the singular-value spectrum;
- seed-reproducible rank against an exact sign-flip or bootstrap null.

Five seeds have only 16 unique two-sided singular-value sign patterns, so
`p_min=1/16=0.0625`. The uniform pilot uses 90% only as an exploratory gate.
The source-knot validation needs at least six and preferably ten independent
seed states for a conventional 5% decision.

## Frozen-Source Acceptance Criteria

- target and source identities remain distinct;
- response is linear over at least two small source perturbations;
- source-on effects separate from no-source and `eta_zero` controls;
- rank and singular subspace are stable over lag and basis rotation;
- cloned-state calibration is followed by independent-seed validation;
- distance and cross-coupling are scaled by knot radius, kernel range, and
  displacement per memory time rather than selected by a broad blind scan.

## Guardrails

- Do not call a uniform-force rank an emergent spatial dimension.
- Do not call synchronized modes quantum fields.
- Do not call internal labels charge, color, or flavor until they remain stable
  under controlled interactions.
- Do not require internal embedding dimension three.
- Do not infer neutrality from universal attraction in an unsigned scalar
  channel.
- Treat seeds as basin samplers and avoid counting multiple times from one seed
  as independent evidence.
