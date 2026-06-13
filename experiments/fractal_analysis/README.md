# Fractal Analysis

Dieses Verzeichnis enthält fraktale Dimensionsanalysen und Box-Counting-Methoden.

Wichtige Dateien:
- `Fraktale/` mit `FD2.py`, `Fraktaldimension.py`, `fit_n_plot.py`
- `analyze_dimension_claim.py` fuer den seed-bewussten Audit von
  `Fraktale/resultsN.csv`
- `reproduce_dimension_pilot.py` fuer einen ressourcenschonenden
  seed-kontrollierten Pilotlauf mit Negativkontrollen

Ziel: Konsolidiere fraktale Analyse in diesem Bereich und verwende
datengetriebene Outputs aus `data/raw/`.

## Seed-bewusster Claim-Audit

```bash
python experiments/fractal_analysis/analyze_dimension_claim.py
```

Das Skript schreibt eine JSON-Zusammenfassung nach
`data/processed/fractal_analysis/dimension_claim_summary.json`.

## Ressourcen-Pilot mit Negativkontrollen

```bash
python experiments/fractal_analysis/reproduce_dimension_pilot.py
```

Der Standardlauf nutzt den historischen Fraktal-Parametersatz aus
`Fraktale/FD2.py`/`resultsN.csv`: `dim=5`, `epsilon=0.05`, `eta=2.0`,
`alpha=0.01`, `B=3.0`, `sigma_att=0.15`, `max_memory=300`, wenige Seeds und
eine kleine `N`-Leiter. Er vergleicht:

- `baseline`: historischer Double-Gaussian-Kernel
- `eta_zero`: ausgeschaltete Speicher-Kraft
- `single_scale`: keine attraktive zweite Skala
- `shuffled_memory`: Speicherpositionen bleiben erhalten, aber die
  Altersgewichtung wird pro Schritt randomisiert

Das Skript nutzt `numba`, falls es in der aktiven Umgebung installiert ist,
und faellt sonst auf eine vektorisierte NumPy-Implementierung zurueck. Ergebnisse
landen standardmaessig in
`data/processed/fractal_analysis/dimension_reproduction_pilot.json`.

## Theoretical Mapping

Siehe [docs/THEORETICAL_CONTEXT.md](../../docs/THEORETICAL_CONTEXT.md) — Fokus auf
"Knot occupancy" und fraktale Strukturdiagnostiken (`D_occ`, Box-Counting).
