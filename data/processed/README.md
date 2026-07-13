# data/processed

This directory is for generated simulation outputs and reviewed machine-readable summaries.

Default policy:

- Raw run directories and bulk outputs remain ignored by Git.
- A result JSON is committed only after review, when a report, figure, or test fixture depends on it.
- Existing tracked JSON files under `data/processed/fractal_analysis/` and `data/processed/anchor_paper/` are archival reviewed snapshots, not the default pattern for new bulk runs.
- Human-readable interpretation belongs in `reports/` or the active `docs/` pages.
- Use stable subdirectories by topic, for example `fractal_analysis/` and `long_run_metastability/`.

The `.gitignore` keeps this README visible while ignoring unreviewed generated outputs. Use an explicit `git add -f` only for reviewed machine-readable snapshots that are referenced by committed reports or tests.