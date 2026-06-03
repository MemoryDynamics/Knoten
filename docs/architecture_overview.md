# Architekturübersicht

Dieses Projekt besteht aus drei Hauptschichten:

1. Kernbibliothek (`src/emergenz_knoten`)
2. Experiment-Entry-Points (`experiments/`)
3. Dokumentation und Audit-Berichte (`docs/`, `reports/`)

## 1. Kernbibliothek

- `src/emergenz_knoten/__init__.py`
  - Exportiert den öffentlichen API-Kern.
- `src/emergenz_knoten/core.py`
  - Definiert `SimulationConfig` und die finite-memory Simulation.
  - Enthält die Numba-optimierte Variante `simulate_finite_memory_numba`.
- `src/emergenz_knoten/kernels.py`
  - Berechnet die attraktiven/repulsiven Gradientenkraftkomponenten und die exponentiellen Memory-Gewichte.
- `src/emergenz_knoten/diagnostics.py`
  - Misst Dimensionswerte (`covariance_dimension`, `occupancy_dimension`, `spectral_dimension`).
  - Berechnet `residence_statistics` und Bootstrap-Konfidenzintervalle.
- `src/emergenz_knoten/experiments.py`
  - Serialisiert Simulationsergebnisse in `.npz`- und `.json`-Formate.
  - Bietet `SimulationRunner` für wiederholbare Ausführung.

## 2. Experiment-Entry-Points

- `experiments/cli.py`
  - Kategorisiert historische Auswertungsskripte und startet sie reproduzierbar.
- `experiments/demo_simulation.py`
  - Kleines Starter-Demo für einen schnellen funktionalen Proof-of-Concept.
- `experiments/legacy/`
  - Historische Explorationsskripte, die bisher nicht in die modulare Bibliothek migriert wurden.

## 3. Dokumentation und Audit

- `README.md`
  - Projektübersicht, Schnellstart und Installationsanleitung.
- `docs/`
  - Projektkarte, Haertungsplan, Experimentkatalog und theoretischer Kontext.
- `reports/`
  - Datierte Audits, Paper-Übergabedokumente und jetzt auch die Projektübergabe.

## Daten- und Ergebnisfluss

1. `SimulationConfig` definieren.
2. `simulate_finite_memory` oder `run_simulation` aufrufen.
3. Ergebnisse mit `save_simulation_result` in `.npz` oder `.json` speichern.
4. Diagnosen mit `diagnostics.py` berechnen.
5. Optional: Skripte aus `experiments/` nutzen, um historische Auswertungen zu reproduzieren.

## Wichtige Annahmen

- Das Modell verwendet eine endliche Gedächtnisspanne mit exponentiell fallenden Gewichten.
- Der Speicherhorizont wird aus `config.memory_factor / config.alpha` und `config.max_memory` berechnet.
- Zufallsgeneratoren werden über `seed` wiederholbar gemacht.
- `numba` ist optional, aber empfohlen für beschleunigte Simulationen.

## Empfehlung

Der nächste Schritt ist, die historische Experimentstruktur in der `experiments/`-Ebenen systematisch auf `src/` zurückzuführen und einen klaren Referenzworkflow für die Dimensionsanalyse zu definieren.
