# Emergenz Knoten

Arbeitsrepository fuer ein minimalistisches Weltmodell aus irreversibler
Speicherdynamik, metastabilen "Knoten" und emergenten effektiven Strukturen.

Stand: 2026-07-10.

## Worum es geht

Das Projekt untersucht einen stochastischen Punktprozess mit relaxierendem
Gedaechtnis. Der sichtbare Prozess `x_n` ist im Allgemeinen nichtmarkovsch,
weil sein naechster Schritt von gespeicherter Vergangenheit abhaengt. Der
augmentierte Zustand aus Position und Speicher, z. B. `z_n=(x_n,rho_n)` oder
`z_n=(x_n,history_n)`, ist dagegen der natuerliche Markov-Zustand.

Die Uebergangsdynamik auf `z_n` definiert einen Markov-/Koopman-Operator auf
Observablen. Diese Sprache macht Knoten als metastabile Operatorstrukturen,
slow modes oder fast-invariante Mengen pruefbar.

Aktuelle Rollen:

- Paper 0: mathematischer Anker bzw. moegliches Supplement.
- Paper I: Minimalmodell plus Long-Run-Evidenz fuer metastabile Knoten.
- Paper II/III: Folgeprogramme fuer Propagation, Raumzeit, Quanten- und
  Standardmodellfragen.

## Aktueller Stand

- `main` ist die Arbeitslinie und tracked `origin/main`.
- Der Paketkern liegt unter `src/emergenz_knoten`.
- Die wichtigsten Entry-Points liegen unter `experiments/`.
- Tests liegen unter `tests/`.
- Die aktive Dokumentation ist auf sieben kuratierte Dokumente reduziert.

Belastbar derzeit:

- Paper 0 traegt als technischer Anker.
- Die Markov-/Transferoperator-Schicht existiert initial unter
  `src/emergenz_knoten/markov/` und ist getestet.
- Der Kernelgradient wurde korrigiert: `A_rep`/`A_att` sind jetzt wieder
  repulsiver/attraktiver Potentialkanal im Sinn der Paper-Gleichung.
- Der korrigierte q=3-Retest zeigt: die historische Baseline mit `A_att=0.35`
  dispergiert; kompakte Kandidaten entstehen erst im Amplitudenfenster
  `A_att=9..35` bei festem `A_rep=1`, sind aber noch keine Long-Run-Knoten.
- Der Grenzscan unterhalb `A_att=9` lokalisiert den korrigierten Umschlag bei
  `A_att ~= 7.9` bzw. `chi ~= 0.88`.
- Der erste Vektormemory-Pilot ist implementiert; sein Kurzlauf zeigt noch
  keinen isolierten vektorinduzierten Oszillator, weil komplexe AR-Moden
  bereits im `eta_v=0`-Kontrollzweig auftreten.
- Der Code unterscheidet `delta`, `gaussian` und `matched_gaussian`
  Deposition; `matched_deposition` ist ohne Steifigkeitsrenormierung breiter
  als die Delta-Baseline.

Noch nicht belastbar:

- ein spezifisch zweiskaliger Baseline-Knotenmechanismus, weil `single_scale`
  ebenfalls stark bleibt;
- eindeutige `d=3`-Selektion;
- harte endliche Signalgeschwindigkeit;
- physikalische Massen oder Standardmodellclaims.

## Schnellstart

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
result = run_simulation(config, seed=1, output_path=Path("results/simulation.npz"))

print(result["samples"].shape)
```

## Installation

Empfohlen in einer virtuellen Umgebung:

```bash
python -m pip install -r requirements.txt
python -m pip install -r requirements-dev.txt
python -m pip install -e .
```

Tests:

```bash
python -m pytest tests -q
```

## Dokumentation

Lokaler MkDocs-Build:

```bash
python -m pip install -r docs/requirements.txt
python -m mkdocs serve
python -m mkdocs build --strict
```

Aktive Einstiegspunkte:

- [Startseite](docs/index.md)
- [Aktueller Stand](docs/current_status.md)
- [Prioritaeten](docs/project_priorities.md)
- [Theoretical Context](docs/THEORETICAL_CONTEXT.md)
- [Repository Map](docs/repository_map.md)
- [Experiment-Katalog](docs/experiment_catalog.md) - enthaelt auch die Knotenscore-Referenz
- [Paper-Claims](docs/paper_claims.md)

## Experiment Entry Points

```bash
python experiments/cli.py --list
python experiments/cli.py reference --list
python experiments/cli.py reference --script reference_experiment.py
python experiments/cli.py dimension_selection --list
python experiments/cli.py dimension_selection --script DimensionsHeatmap.py
```

Direkter Referenzlauf:

```bash
python experiments/reference_experiment.py --seed 2 --steps 2000 --sample-every 20 --burn-in 100 --output data/processed/reference/reference_experiment.json
```

Long-Run-Metastabilitaet:

```bash
python experiments/long_run_metastability.py --steps 10000000 --seeds 1 --conditions baseline --dim 3 --alpha 0.01 --sample-every 1000 --burn-in 1000000 --max-memory 800 --output-dir data/processed/long_run_metastability/2026-06-29_initial
```

## Naechste Prioritaeten

1. Fuer skalare Paper-I-Haertung nur noch das enge Fenster `A_att=7.75..9`
   als Uebergang und `A_att=9..35` als Kompaktheitsbereich verwenden.
2. Fuer Paper III/Photon-/Wellenrichtung Vektor-, Phasen- oder Velocity-
   Memory weiter separat testen; der erste Vektorpilot ist ein Kontrollbefund,
   noch kein Oszillatorclaim.
3. Naechste Vektormemory-Kriterien: `alignment` vs. `transverse_2d`,
   `lambda_v`-Variation, shuffled-vector-Kontrolle und lag-stabile Slow-Modes.
4. Zero-Mean/Matched-Deposition erst unter korrigierter Sign-Konvention wieder
   aufnehmen, falls sie eine konkrete Mechanismusfrage klaeren.
