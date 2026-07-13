# Emergenz Knoten

Arbeitsrepository fuer ein minimalistisches Weltmodell aus irreversibler
Speicherdynamik, metastabilen "Knoten" und emergenten effektiven Strukturen.

Stand: 2026-07-13.

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
- Paper I: Minimalmodell plus kontrollierte Long-Run-Evidenz fuer scalar
  co-moving memory-cloud candidates.
- Paper II/III: Folgeprogramme fuer Propagation, Raumzeit, Quanten- und
  Standardmodellfragen; derzeit keine Claim-Basis.

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
- Nach korrigierter Sign-Konvention ist `A_att=35`, `epsilon=1e-4`, `N=30M`
  der aktuelle skalare Long-Run-Referenzkandidat. Gegen `eta_zero` trennt er
  sich in co-moving Radius, radiusnormalisierter Center-Drift, Memory-Dimension
  und Roundness.
- Die Paper-I-Evidenz ist als co-moving compact memory-cloud evidence zu lesen:
  kein fixes absolutes Zentrum, kein physikalischer Teilchenclaim.
- Long-Run-Trace-AR findet komplexe Klassifikationen auch in `eta_zero`; es
  gibt daher keinen kontrollgetrennten skalaren Phasen-/Photonmodus.
- Feature-Closure stuetzt die skalare Grobkoernung fuer Shape-/Radius-Scalars,
  nicht fuer den Spin-Scalar.
- Der Code unterscheidet `delta`, `gaussian` und `matched_gaussian`
  Deposition; `memory_mass=M0` ist als eigene Memory-Skala abgebildet.

Noch nicht belastbar:

- ein spezifisch zweiskaliger Baseline-Knotenmechanismus, weil `single_scale`
  historisch ebenfalls stark war;
- eindeutige externe `d=3`-Selektion; `D_mem ~2.94` ist aktuell eine lokale
  Memory-Cloud-Shape-Diagnostik im gewaehlten 3D-Embedding;
- stabile skalare Spin-, Phasen- oder Photonmoden;
- harte endliche Signalgeschwindigkeit;
- physikalische Massen, Lorentz-, Quanten- oder Standardmodellclaims.

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

Dokumentation:

```bash
python -m pip install -r docs/requirements.txt
python -m mkdocs build --strict
```

## Aktive Dokumentation

- [Startseite](docs/index.md)
- [Aktueller Stand](docs/status/current_status.md)
- [Prioritaeten](docs/status/project_priorities.md)
- [Theoretical Context](docs/reference/THEORETICAL_CONTEXT.md)
- [Repository Map](docs/reference/repository_map.md)
- [Experiment-Katalog](docs/reference/experiment_catalog.md) - enthaelt auch die Knotenscore-Referenz
- [Paper-Claims](docs/status/paper_claims.md)

## Experiment Entry Points

```bash
python experiments/cli.py --list
python experiments/cli.py reference --list
python experiments/cli.py reference --script current/reference/reference_experiment.py
python experiments/cli.py dynamics --list
python experiments/cli.py markov --list
```

Direkter Referenzlauf:

```bash
python experiments/current/reference/reference_experiment.py --seed 2 --steps 2000 --sample-every 20 --burn-in 100 --output data/processed/reference/reference_experiment.json
```

Long-Run-Metastabilitaet:

```bash
python experiments/current/dynamics/long_run_metastability.py --steps 10000000 --seeds 1 --conditions baseline --dim 3 --alpha 0.01 --sample-every 1000 --burn-in 1000000 --max-memory 800 --output-dir data/processed/long_run_metastability/2026-06-29_initial
```

## Naechste Prioritaeten

1. Paper-I-Text und Supplement auf Evidenztabelle, Feature-Closure und den
   seedweisen 3D-Memory-Shape-Befund synchronisieren.
2. Fuer skalare Paper-I-Haertung `A_att=35`, `epsilon=1e-4`, `N=30M` als
   aktuellen Referenzslice verwenden; weitere `lambda_m`/`sigma`/`M0`-Achsen
   erst nach Text-Synchronisierung.
3. Fuer Paper III/Photon-/Wellenrichtung Vektor-, Phasen- oder Velocity-Memory
   separat testen; der bisherige skalare Befund ist Relaxations-/Shape-Evidenz.
4. Paper II bleibt Future Work, bis Propagation, lokale Kopplung und
   Mehrknoten-Response mit Negativkontrollen tragen.