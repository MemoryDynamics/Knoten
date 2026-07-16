# Canonical scalar reference-state checkpoints at N=100M

Date: 2026-07-16

## Decision

Two complete states of the implemented finite-memory dynamics were formed and
saved as reproducible branch points: one in ambient dimension `d=3` and one in
`d=10`. Both use formation seed 1 and `N=100,000,000` updates. They are
canonical development fixtures for paired continuation experiments, not
ensemble evidence and not proof of stationarity.

The checkpoints make the next comparison methodologically clean: every arm
starts from the same target state `z_N`, receives the same explicit future
noise, and differs only in the declared interaction.

## Formation slice

| Parameter | Value |
| --- | ---: |
| `N` | `100,000,000` |
| `epsilon` | `1e-4` |
| `eta` | `0.15` |
| `lambda_m = alpha` | `0.01` |
| `M0` | `1` |
| deposition | delta |
| `sigma_rep`, `sigma_att` | `1`, `3` |
| `A_rep`, `A_att` | `1`, `35` |
| memory horizon | `600` updates |
| stored memory mass | `0.9975949907` |
| formation revision | `e8f4af2ca23d6f264068dde971adb47a75d76eaa` |

The two dimensions ran concurrently from a clean worktree. The `d=3` job took
`3501.28 s` (`28,561.0` updates/s); the `d=10` job took `5272.74 s`
(`18,965.5` updates/s).

## State semantics

For the implemented truncated process, a checkpoint contains the complete
numerical Markov state: the visible position `x_N`, all 600 age-ordered memory
points, their weights, the simulation configuration, update index, formation
seed, Git revision, and SHA-256 digests of every array. Loading is
pickle-free and validates schema, shape, horizon, weights, youngest point, and
checksums.

"Complete" is deliberately limited to this finite-memory approximation. The
retained weight is `0.9975949907`; the omitted formal exponential tail has
weight `0.0024050093` (about `0.2405%`). The preceding visible trajectory and
the formation PRNG state are not part of `z_N` and are not needed to continue
the Markov dynamics. Paired arms instead use a new, explicit, shared future
noise array.

## Final-state geometry

| `d` | mean radius | RMS radius | `D_mem` | min/max axis ratio | `|x-c_mem|/R_rms` |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 3 | `1.9383e-4` | `2.1165e-4` | `2.8602` | `0.7548` | `0.6683` |
| 10 | `3.7503e-4` | `3.8337e-4` | `9.4307` | `0.6793` | `1.3839` |

`D_mem` is the participation dimension of the weighted memory covariance, not
an external or spectral dimension. At this instant the `d=10` memory cloud is
high-dimensional; it has not collapsed internally to three dimensions. This
strengthens the case for measuring a control-subtracted external response rank
rather than reading an external dimension directly from internal shape.

Absolute radii are not compared across ambient dimensions as physical lengths:
the norm and noise scaling are dimension dependent. Subsequent interaction
tests therefore use radii, separations, and response amplitudes in
dimensionless ratios and compare each perturbed arm with its seed-identical
free control.

## Integrity audit

Both files were reloaded with checksum validation. Common translation and an
orthogonal axis permutation were then applied to the complete state, followed
by an exact paired-branch replay with shared future noise.

| `d` | `x_N == memory[0]` | center placement error | shape equivariance error | gradient equivariance error | replay error |
| ---: | --- | ---: | ---: | ---: | ---: |
| 3 | exact | `5.66e-16` | `2.12e-22` | `8.70e-17` | `0` |
| 10 | exact | `8.95e-16` | `7.35e-22` | `7.39e-17` | `0` |

These checks validate serialization and deterministic continuation under a
specified future-noise realization. They do not validate metastability across
seeds or establish that `N=100M` is a stationary limit.

## Controlled continuation ladder

1. **Free target:** self-dynamics only, no cross interaction.
2. **Frozen cloned source:** a translated and orthogonally oriented clone of
   the target checkpoint acts on the target while its own state remains fixed.
3. **Frozen independent source:** replace the clone with a checkpoint from a
   different formation seed in the same basin/score class.
4. **One-way dynamic source:** source evolves independently while the target
   reads its field.
5. **Reciprocal pair:** both states evolve with separate memories and mutual
   cross coupling.

The first source test is calibrated at a few discrete separation and coupling
ratios. It is compared against `no source`, zero cross coupling, `eta_zero`,
and the already measured uniform-probe control. Shared memory is not used: it
would define a different model and obscure source/target identity.

Primary observables are the control-subtracted target memory-center response,
shape-tensor response, `D_mem` change, radius/destruction ratio, delayed
response rank, and source-target separation. A low external rank is only
interesting if it is stable across orientations, lags, probe strengths, and
independent seed pairs.

## Next gate

Implement the frozen-source runner against these two checkpoints. First use a
cloned source to isolate geometry and implementation; only after that passes
should at least six, preferably ten, independent source/target seed pairs be
formed for rank inference. The present two files are the reproducible starting
point for that development, not the final statistical sample.

## Artifacts

- Machine-readable index:
  `data/processed/reference_states/scalar_Aatt35_N100M_d3_d10_seed1_2026-07-16/reference_state_index.json`
- `d=3` checkpoint:
  `data/processed/reference_states/scalar_Aatt35_N100M_d3_d10_seed1_2026-07-16/scalar_Aatt35_d3_seed1_N100000000.npz`
- `d=10` checkpoint:
  `data/processed/reference_states/scalar_Aatt35_N100M_d3_d10_seed1_2026-07-16/scalar_Aatt35_d10_seed1_N100000000.npz`
