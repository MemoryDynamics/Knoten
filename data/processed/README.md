# data/processed

This directory is for generated simulation outputs and reviewed machine-readable summaries.

Default policy:

- Raw run directories and bulk outputs remain ignored by Git.
- A result JSON is committed only after review, when a report or figure depends on it.
- Human-readable interpretation belongs in `reports/` or the active `docs/` pages.
- Use stable subdirectories by topic, for example `fractal_analysis/` and `long_run_metastability/`.

The `.gitignore` keeps this README visible while ignoring unreviewed generated outputs.