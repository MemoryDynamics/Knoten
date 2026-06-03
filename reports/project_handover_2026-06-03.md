# Project Handover

Datum: 2026-06-03

## Status

- `python >= 3.11` ist die Ziel-Umgebung.
- Der Paketkern liegt sauber unter `src/emergenz_knoten`.
- Die Unit-Tests in `tests/test_core.py` laufen lokal sauber durch: `8 passed`.
- `requirements.txt` definiert die Laufzeitabhängigkeiten.
- `requirements-dev.txt` enthält die Test-Abhängigkeit `pytest`.

## Wichtigste Codepfade

- `src/emergenz_knoten/__init__.py` — zentrale API-Exports
- `src/emergenz_knoten/core.py` — finite-memory Simulation, Konfiguration, Numba-optimierte Implementierung
- `src/emergenz_knoten/diagnostics.py` — Dimensions- und Residence-Diagnostiken
- `src/emergenz_knoten/experiments.py` — Ergebnis-Serialisierung und `SimulationRunner`
- `src/emergenz_knoten/kernels.py` — Gradientenkern und Memory-Gewichte

## Empfohlener Einstieg

1. virtuelle Umgebung aktivieren

```powershell
python -m venv .venv
& .\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pip install -r requirements-dev.txt
```

2. Tests ausführen

```powershell
& .\.venv\Scripts\python.exe -m pytest tests -q
```

3. Beispielsimulation

```python
from pathlib import Path
from emergenz_knoten import SimulationConfig, run_simulation

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

Alternativ kann das fertige Demo-Skript direkt gestartet werden:

```powershell
python experiments/demo_simulation.py
```

Dieses Skript erzeugt aktuell die Datei `results/demo_simulation.npz`.

## Aktuelle Erkenntnisse

- Der Hauptkern ist reproduzierbar und modular aufgebaut.
- `simulate_finite_memory` liefert eine einfache, interpretierbare Simulation mit exponentiellen Gewichten.
- `simulate_finite_memory_numba` funktioniert, falls `numba` installiert ist.
- Die `experiments/`-Ordnerstruktur enthält historische Explorationsskripte; der robuste Kern liegt in `src/`.

## Offene Punkte für Olaf

1. `experiments/cli.py` und die experimentellen Skripte sollten als nächster Schritt auf eine gemeinsame Pipeline einheitlich abgestimmt werden.
2. Es gibt noch keinen kanonischen Referenzlauf für die behauptete Dimensionsmessung `D_occ ≈ 2.8`; das ist die wichtigste Reproduktionsfrage.
3. Eine zentrale Ausgabe- und Datenablagestruktur fehlt noch (z. B. `data/processed` als systematischer Ergebnisordner).
4. Dokumentation und Projektkarte sind vorhanden, aber ein explizites Übergabedokument mit Aufgaben- und Verantwortlichkeitsmatrix könnte noch ergänzt werden.

## Übergabe-Empfehlung

- `reports/paper1_delivery_package_2026-06-01.md` für die Paper-Übergabe an Olaf nutzen.
- Dieses Projektpaket ergänzt das um den aktuellen Code- und Testzustand.
- Ergänzende Dokumente:
  - `docs/architecture_overview.md`
  - `reports/project_open_points_2026-06-03.md`
- Als nächster Schritt empfiehlt sich ein kurzes Review mit Olaf, in dem die folgenden Fragen geklärt werden:
  - Validität des aktuellen Kernmodells für die angestrebten dimensionellen Befunde
  - Priorisierung historischer Experimente vs. Neustrukturierung in `src/`
  - Weitere Dokumentationsbedarfe für reproduzierbare Ausführung
