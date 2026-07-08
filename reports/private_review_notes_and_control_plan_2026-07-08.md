# Private Reviewer Material and M0/Alpha-One Control Plan

Date: 2026-07-08.

## Privacy decision

A public GitHub repository cannot contain private cleartext. If a file is
committed to a public repo, it should be treated as public, including old
commits and GitHub caches.

For private reviewer notes the viable options are:

1. Keep only sanitized public text in the public repository.
2. Keep the private note outside Git, for example under an ignored `private/`
   folder.
3. Commit only encrypted ciphertext to the public repository, for example an
   `age`/SOPS/git-crypt encrypted file. The decryption key must not be in the
   repository.
4. If a cleartext file must be made non-public, remove it from the public
   history with a history rewrite and force-push. This reduces exposure in the
   repo but cannot guarantee removal from already cloned copies or external
   caches.

Recommended project policy: use a public sanitized summary plus an encrypted or
ignored private source. Do not add further private reviewer cleartext to
`reports/`.

## Scientific controls

Two long-run controls are now defined:

- `m0_zero`: sets `memory_mass=0`. This is the clean zero-field control with the
  same stochastic update and code path. It should match an `eta_zero` trajectory
  distribution for the same seed up to implementation details.
- `alpha_one`: sets `alpha=1`. This is the one-step memory limit: only the most
  recent deposited event carries weight. For a symmetric kernel centered at the
  current position, its self-gradient vanishes, so this limit should behave as a
  negative control rather than a confined knot regime.

These controls fit the proposed Block-Markov/AR campaign:

1. Run matched seeds for `baseline,m0_zero,alpha_one` using the same sampling as
   the existing long-run evidence.
2. Compare residence, radius, memory-cloud shape, and score v0.4 against
   `eta_zero` and `single_scale`.
3. Reuse the resulting sampled trajectories for block states and AR spectra.
4. Treat complex slow modes as a necessary precondition before reopening a
   photon/wave interpretation inside the scalar model.

## Provenance guardrail

Long-run JSONs record `git_status`. Local private-note edits must stay ignored,
encrypted, or outside the repository before clean evidence runs are launched.

## Implementation status

Implemented conditions in `experiments/long_run_metastability.py`:

```powershell
python experiments/long_run_metastability.py `
  --steps 10000000 `
  --seeds 1,2,3,4,5 `
  --conditions baseline,m0_zero,alpha_one `
  --dim 3 `
  --alpha 0.01 `
  --memory-mass 1.0 `
  --sample-every 1000 `
  --burn-in 1000000 `
  --max-memory 800 `
  --output-dir data/processed/long_run_metastability/m0_alpha_one_10M_seed1-5_2026-07-08
```

A small non-Numba import/function smoke passed locally:

- `exponential_memory_weights(0.1, 3, memory_mass=0.0)` returns all-zero weights;
- `simulate_finite_memory` accepts `SimulationConfig(memory_mass=0.0)`;
- `_apply_condition(..., "m0_zero")` sets `memory_mass=0.0`;
- `_apply_condition(..., "alpha_one")` sets `alpha=1.0`.