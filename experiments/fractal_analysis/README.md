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

Historischer Alpha-Sweep mit bewusst beibehaltenem `max_memory=300` und
historischer Kopplung:

```bash
python experiments/fractal_analysis/reproduce_dimension_pilot.py ^
  --dims 3,4,5,6 ^
  --alpha-list 0.005,0.0075,0.01,0.015,0.02 ^
  --steps-list 300000,1000000,2500000 ^
  --conditions baseline ^
  --engine auto
```

Entkoppelter Kontroll-Sweep mit konstantem `eta*alpha` und Speicherhorizont
nach 95 Prozent Gewichtsmasse:

```bash
python experiments/fractal_analysis/reproduce_dimension_pilot.py ^
  --dims 3,4,5,6 ^
  --alpha-list 0.005,0.0075,0.01,0.015,0.02 ^
  --steps-list 300000,1000000 ^
  --conditions baseline ^
  --coupling-mode fixed-eta-alpha ^
  --eta-alpha-target 0.02 ^
  --memory-mode tail-mass ^
  --memory-tail-mass 0.95 ^
  --engine auto
```

Jede Ergebniszeile dokumentiert `alpha`, `eta`, `eta_alpha`,
`uncapped_horizon`, `used_horizon` und `stored_weight_mass`, damit Alpha nicht
unbemerkt als mehrere Parameter zugleich interpretiert wird.

## Theoretical Mapping

Siehe [docs/THEORETICAL_CONTEXT.md](../../docs/THEORETICAL_CONTEXT.md) — Fokus auf
"Knot occupancy" und fraktale Strukturdiagnostiken (`D_occ`, Box-Counting).
