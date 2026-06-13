# Fractal Analysis

Dieses Verzeichnis enthält fraktale Dimensionsanalysen und Box-Counting-Methoden.

Wichtige Dateien:
- `Fraktale/` mit `FD2.py`, `Fraktaldimension.py`, `fit_n_plot.py`
- `analyze_dimension_claim.py` fuer den seed-bewussten Audit von
  `Fraktale/resultsN.csv`

Ziel: Konsolidiere fraktale Analyse in diesem Bereich und verwende
datengetriebene Outputs aus `data/raw/`.

## Seed-bewusster Claim-Audit

```bash
python experiments/fractal_analysis/analyze_dimension_claim.py
```

Das Skript schreibt eine JSON-Zusammenfassung nach
`data/processed/fractal_analysis/dimension_claim_summary.json`.

## Theoretical Mapping

Siehe [docs/THEORETICAL_CONTEXT.md](../../docs/THEORETICAL_CONTEXT.md) — Fokus auf
"Knot occupancy" und fraktale Strukturdiagnostiken (`D_occ`, Box-Counting).
