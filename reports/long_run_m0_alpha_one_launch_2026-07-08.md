# Long-Run Launch: M0=0 and Alpha-One Controls

Date: 2026-07-08.

## Purpose

Launch the missing control campaign for Paper-I knot evidence:

- `m0_zero`: zero memory-field mass with the same stochastic update path;
- `alpha_one`: one-step memory limit, testing whether the exponential tail is
  necessary for confinement.

Baseline is not rerun in this launch because 100M baseline/single-scale data
already exist for the current comparison context.

## Command

```powershell
$env:PYTHONPATH='C:\tmp\knoten-longrun-runtime-20260708;src'
C:\Users\Hauke\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe `
  experiments\long_run_metastability.py `
  --steps 100000000 `
  --seeds 1,2,3,4,5,6,7,8,9,10 `
  --conditions m0_zero,alpha_one `
  --dim 3 `
  --alpha 0.01 `
  --memory-mass 1.0 `
  --sample-every 1000 `
  --burn-in 1000000 `
  --max-memory 800 `
  --output-dir data\processed\long_run_metastability\m0_alpha_one_100M_seed1-10_2026-07-08
```

## Runtime

- Git HEAD at launch: `cfccc5a`.
- Background process PID observed after launch: `27864`.
- stdout log: `tmp/long_run_m0_alpha_one_100M_seed1-10_2026-07-08.out.log`.
- stderr log: `tmp/long_run_m0_alpha_one_100M_seed1-10_2026-07-08.err.log`.
- output directory: `data/processed/long_run_metastability/m0_alpha_one_100M_seed1-10_2026-07-08`.

First observed stdout line:

```text
running condition=m0_zero seed=1 steps=100000000 alpha=0.01 memory_mass=0 dim=3
```

## Notes

The public worktree was clean before launch. Private reviewer notes are ignored
or kept outside the public repository; they do not affect `git status --short`.