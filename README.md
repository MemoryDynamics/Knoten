# Emergenz Knoten

Arbeitsrepository fuer ein minimalistisches Weltmodell aus irreversibler
Speicherdynamik, metastabilen "Knoten" und emergenten effektiven Strukturen.

Stand dieses ersten Audits: 2026-05-22.

## Schnellstart

```python
from pathlib import Path
from emergenz_knoten import SimulationConfig, run_simulation, save_simulation_result

config = SimulationConfig(
    steps=5000,
    dim=3,
    alpha=0.005,
    sample_every=50,
    max_memory=200,
)
result = run_simulation(config, seed=1, output_path=Path('results/simulation.npz'))

print(result['samples'].shape)
```

## Installation

Empfohlen in einer virtuellen Umgebung:

```bash
python -m pip install -r requirements.txt
python -m pip install -r requirements-dev.txt
```

Zum Entwickeln und Paketieren:

```bash
python -m pip install -e .
```

Tests ausführen:

```bash
python -m pytest tests -q
```

Der Kernexport umfasst:

- `SimulationConfig`
- `simulate_finite_memory`
- `simulate_finite_memory_numba`
- `SimulationRunner`
- `run_simulation`
- `save_simulation_result`
- `load_simulation_result`

## Experiment Entry Point

Für reproduzierbare Experimente steht ein zentrales CLI-Skript zur Verfügung:

```bash
python experiments/cli.py --list
python experiments/cli.py dimension_selection --list
python experiments/cli.py dimension_selection --script DimensionsHeatmap.py
```

Ein kleines Starter-Demo ist ebenfalls vorhanden:

```bash
python experiments/demo_simulation.py
```

## Startpunkte

- [Projektkarte](docs/project_map.md): Was liegt wo, welche historischen
  Skriptfamilien gibt es, und welche Zielstruktur ist sinnvoll.
- [Architekturübersicht](docs/architecture_overview.md): Kernkomponenten und
  Datenfluss des aktuellen Projektzustands.
- [Paper-Claims](docs/paper_claims.md): Extrahierte Kernaussagen aus den
  aktuellen Paper-Drafts und ihr aktueller Haertungsstatus.
- [Haertungsplan](docs/hardening_plan.md): Konkrete Tests, Gegenproben und
  Reproduzierbarkeitskriterien.
- [Experiment-Katalog](docs/experiment_catalog.md): Bestehende Skripte und
  Ergebnisartefakte nach Thema.
- [Reproduzierbarkeitsstatus](docs/reproducibility_status.md): Aktueller
  technischer Zustand, inklusive Python-Umgebung.
- [Initial Audit](reports/initial_audit_2026-05-22.md): Kurze Diagnose der
  groessten Staerken, Risiken und naechsten Schritte.
- [Fractal Results Quicklook](reports/fractal_results_quicklook_2026-05-22.md):
  erster Reality Check zu vorhandenen `D_occ ~ 2.8` CSV-Spuren.
- [Action Matrix](docs/action_matrix.md): Was Codex autonom weiterziehen kann
  und wofuer Hauke gebraucht wird.
- [Paper I Source Audit](reports/paper1_source_audit_2026-06-01.md):
  erster Audit der aktuellen `1.tex` Quelle.
 - [Theoretical Context](docs/THEORETICAL_CONTEXT.md): kurze, zusammenfassende
   Kontext- und Claim-Mapping-Datei, die die Chat-basierten Notizen mit den
   Experiment-Entry-Points verknüpft.

## Modellkern in einem Satz

Ein Punktprozess `x_n` in einem abstrakten Zustandsraum wird mit einer
endlichen, relaxierenden Speicherverteilung `rho_n` gekoppelt. Die
Nicht-Invertierbarkeit des Speicherupdates erzeugt eine Update-Richtung; unter
geeigneter Grobkoernung koennen metastabile, lokalisierte Strukturen entstehen,
deren effektive Dimension, Relaxationsskalen und Signalantworten als Kandidaten
fuer Raum, Zeit und Kinematik untersucht werden.

## Arbeitsregel ab jetzt

Die bestehenden Skripte bleiben zunaechst unangetastet, weil sie historische
Explorationslaeufe und relative Ausgabepfade enthalten. Neue Arbeit sollte in
einer sauberen Zielstruktur entstehen und nur dann alte Skripte ersetzen, wenn
ein reproduzierbarer Vergleich vorliegt.

Empfohlene Zielstruktur fuer die naechste Refactor-Runde:

```text
src/emergenz_knoten/        # kanonischer Modellkern und Diagnostiken
experiments/                # reproduzierbare Experiment-Entry-Points
data/raw/                   # unveraenderte Rohresultate
data/processed/             # kuratierte Auswertungen
figures/                    # paperfaehige Abbildungen
paper/                      # LaTeX/Prism-Quellen, wenn verfuegbar
docs/                       # Claim-Register, Projektkarte, Haertung
reports/                    # datierte Audits und Ergebnisberichte
```

## Naechste technische Prioritaeten

1. Eine funktionierende Python-Umgebung wiederherstellen.
2. Einen ersten Baseline-Commit der historischen Artefakte erstellen.
3. Den Modellkern aus den Explorationsskripten in ein testbares Paket
   extrahieren.
4. Den wichtigsten Befund, insbesondere die behauptete Naehe zu effektiver
   Dimension ca. 2.8/3, mit Seeds, Konfidenzintervallen und Negativkontrollen
   reproduzieren.

## Aktueller Fortschritt 2026-06-01

Ein erster leichter Referenzkern liegt unter `src/emergenz_knoten`.
Er umfasst Kernelgradienten, eine kleine finite-memory Simulation und
Diagnostiken fuer Kovarianzdimension, Occupancy-Dimension, Residence und
Bootstrap-CI. Zum reproduzierbaren Referenzlauf steht auch `scripts/reference_experiment.py` bereit.
Die Tests laufen mit der gebuendelten Codex-Python-Runtime:

```powershell
& "C:\Users\Hauke\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" tests\test_core.py
& "C:\Users\Hauke\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" scripts\smoke_test.py
& "C:\Users\Hauke\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" scripts\reference_experiment.py --seed 2 --steps 2000 --sample-every 20 --burn-in 100 --output reference_experiment.json
& "C:\Users\Hauke\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" scripts\highN_regime.py --steps 20000 --sample-every 2000 --output highN_regime.json
& "C:\Users\Hauke\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" scripts\highN_regime_validation.py --steps 20000 --sample-every 2000 --output highN_regime_validation.json
```
