# Emergenz Knoten

Arbeitsrepository fuer ein minimalistisches Weltmodell aus irreversibler
Speicherdynamik, metastabilen "Knoten" und emergenten effektiven Strukturen.

Stand: 2026-06-29.

## Worum es geht

Das Projekt untersucht einen stochastischen Punktprozess mit endlichem,
relaxierendem Gedaechtnis. Der sichtbare Prozess `x_n` ist im Allgemeinen
nicht markovsch, weil sein naechster Schritt von gespeicherter Vergangenheit
abhaengt. Der augmentierte Zustand aus Position und Speicher,
z. B. `z_n = (x_n, rho_n)` oder `z_n = (x_n, history_n)`, ist dagegen der
natuerliche Markov-Zustand.

Damit besitzt das Modell bereits eine algebraische Grundschicht: Die
Uebergangsdynamik auf `z_n` definiert einen Markov-/Koopman-Operator auf
Observablen, dessen Iterationen eine vorwaertsgerichtete Halbgruppe bilden.
Diese Sprache ersetzt keine Simulation, macht aber Knoten als metastabile
Operatorstrukturen, slow modes oder fast-invariante Mengen pruefbar.

Diese Sicht ist der aktuelle inhaltliche Anker fuer die naechste Phase:

- Paper 0: Einordnung als finite-memory self-interacting process mit
  Markov-Einbettung und Transferoperator-/MSM-Anschluss.
- Paper I: schrittweise Ueberarbeitung des Minimalmodells, damit Zeit,
  Knoten, Relaxationsskalen und Mass-Proxies operationaler und weniger
  spekulativ formuliert sind.
- Paper II: Anschluss der Raum-/Lorentz-Kinematik an dieselbe
  Operator-Schicht; Lorentz-Symmetrie wird als effektiver Stabilisator des
  makroskopischen Propagationskegels gelesen, nicht als Mikropostulat.

## Aktueller Stand

- `main` ist die Arbeitslinie und tracked `origin/main`.
- Der Paketkern liegt unter `src/emergenz_knoten`.
- Die wichtigsten Entry-Points liegen unter `experiments/`.
- Tests liegen unter `tests/`.
- ReadTheDocs/MkDocs-Konfiguration ist vorbereitet:
  `.readthedocs.yaml`, `mkdocs.yml`, `docs/index.md`.
- Die historischen Chat-Notizen bleiben Rohmaterial; kuratierte Aussagen
  gehoeren in `docs/` und `reports/`.

Wissenschaftlich belastbar ist derzeit:

- Der archivierte Long-N-Finite-Size-Befund enthaelt ein Near-3-Signal:
  `embedding dim = 5`, `N = 60,000,000`, fuenf Runs,
  `mean D_occ = 2.810559`.
- Ein neuer reproduzierbarer Pfad koppelt bei kleineren/mittleren `N`
  plausibel an den Archivpfad an.
- Die Kurzlaeufe und Negativkontrollen zeigen noch keinen starken Near-3-Claim.
  Die robuste Formulierung ist daher: ein vielversprechender archivierter
  Dimensionsbefund, aber noch kein Nachweis einer eindeutigen 3D-Selektion.

Der wichtigste technische Gap fuer die Non-Markovian-Schiene:

- Die Simulation gibt bisher `samples`, `sample_steps`, finalen `memory` und
  `weights` zurueck.
- Fuer Transferoperatoren, MSM/PCCA oder HMM/PMM brauchen wir zusaetzlich
  Memory-Traces oder konsistente Memory-Summary-Features entlang der Trajektorie.
  Erst daraus lassen sich Operatoren auf `z_n` schaetzen.

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

Tests ausfuehren:

```bash
python -m pytest tests -q
```

Der oeffentliche Kernexport umfasst:

- `SimulationConfig`
- `simulate_finite_memory`
- `simulate_finite_memory_numba`
- `SimulationRunner`
- `run_simulation`
- `save_simulation_result`
- `load_simulation_result`
- `covariance_dimension`
- `occupancy_dimension`
- `spectral_dimension`
- `residence_statistics`

## Dokumentation

Lokaler MkDocs-Build:

```bash
python -m pip install -r docs/requirements.txt
python -m mkdocs serve
python -m mkdocs build
```

Wichtige Einstiegspunkte:

- [ReadTheDocs-Startseite](docs/index.md)
- [Aktueller Stand](docs/current_status.md)
- [Projektprioritaeten](docs/project_priorities.md)
- [Repository Map](docs/repository_map.md)
- [Non-Markovian Basis](docs/non_markovian_basis.md)
- [Markov-Architektur](docs/markov_architecture.md)
- [Markov-Anforderungen](docs/markov_requirements.md)
- [Projektkarte](docs/project_map.md)
- [Architekturuebersicht](docs/architecture_overview.md)
- [Experiment-Katalog](docs/experiment_catalog.md)
- [Reproduzierbarkeitsstatus](docs/reproducibility_status.md)
- [Paper-Claims](docs/paper_claims.md)
- [Haertungsplan](docs/hardening_plan.md)

## Experiment Entry Point

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

## Modellkern in einem Satz

Ein Punktprozess `x_n` in einem abstrakten Zustandsraum wird mit einer
endlichen, relaxierenden Speicherverteilung gekoppelt. Das Speicherupdate ist
irreversibel und macht den sichtbaren Prozess nichtmarkovsch; im augmentierten
Speicherzustand `z_n` entsteht jedoch eine saubere Markov-Einbettung, aus der
metastabile Strukturen, Relaxationsskalen und effektive Grobstrukturen
operational und operatorisch untersucht werden koennen.

## Naechste Prioritaeten

Die aktuelle konsolidierte Liste steht in
[docs/project_priorities.md](docs/project_priorities.md). Die technische
Einordnung steht in [docs/markov_architecture.md](docs/markov_architecture.md),
die Akzeptanzkriterien in
[docs/markov_requirements.md](docs/markov_requirements.md). Der wichtigste
naechste Schritt ist die Markov-/Transferoperator-Schicht als echte Paket- und
Teststruktur auf augmentierten Zustaenden.

Kurzfassung:

1. `src/emergenz_knoten/markov/` anlegen: Features, Lagged Dataset,
   Transition Counts, Operatoren, Validation.
2. Paper-0-Pipeline auf diese Schicht umstellen und eine kleine Evidenztabelle
   mit Seeds, Lag-Sensitivitaet und Negativkontrolle erzeugen.
3. Paper 0 auf Expert-Feedback-Niveau bringen: kompakter Theoremblock,
   Kernelklassen, Evidenztabelle.
4. Paper I mit Paper 0 abgleichen, besonders Memory-Normierung,
   Markov-Einbettung und Mass-Proxy-Sprache.
5. Archivierten `D_occ ~ 2.8`-Befund mit expliziten Seeds, groesseren `N`,
   Negativkontrollen und mehreren Diagnostiken haerten.
6. Paper II/III erst danach weiterziehen.
