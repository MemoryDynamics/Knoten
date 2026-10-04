# Emergenz Knoten

Minimalistisches Forschungsmodell fuer diskrete Dynamik mit endlichem,
relaxierendem Gedaechtnis, metastabilen Strukturen und kontrollierten
Rotations-/Interaktionskandidaten.

Stand: 2026-10-04.

## Wissenschaftlicher Stand

- Paper 0 ist der mathematische Anker; Paper I traegt kontrollierte Evidenz
  fuer eine co-moving skalare Relaxationswolke, nicht fuer ein Teilchen.
- Der getrennte deterministische Ast besitzt sieben lokal zertifizierte
  finite-$H$-Kreisroots und sechs verbindende Homotopiekanten bei
  $\alpha=0.01$.
- Direkte lokale Stabilitaetsevidenz liegt fuer exakt $H=2400$ vor; ein
  vollstaendiger Intervallspektralbeweis fehlt.
- Ein lokaler $F_\infty$-Root ist zertifiziert. Die lokale Endpunktidentitaet
  ist post hoc ueber Krawczyk-Bildinklusion reconciliiert; Attempt 4 bleibt
  formal inconclusive und dynamische $H\to\infty$-Stabilitaet offen.
- Der P4-R-S-Anchor-Holdout bleibt ein Zwei-Zellen-Skalentransfer und ist
  keine Replikation; sein historischer Source-Audit bleibt
  `referee-source-ready-with-major-claim-restrictions`. P5-D bleibt nach drei
  verbrauchten Produktionsaufrufen `p5d-inconclusive`.
- Paper I besitzt eine eingefrorene, maschinenpruefbare
  [Claim-Evidenzspur](paper/paper_i/supplement/README.md), einen transitiven
  Hash-Lock und `CITATION.cff`; zweiter Intervallbackend und DOI bleiben offen.
- Interaktion, Ladung, Spin, Impuls, Traegheit und Masse sind Hypothesen, keine
  Ergebnisse dieses Repositorys.

## Orientierung

Die aktive Dokumentation folgt der 7x7-Regel: hoechstens sieben Eintraege je
Ebene und hoechstens sieben Ebenen. Es gibt genau eine aktive
Prioritaetenliste.

- [Dokumentationsstart](docs/index.md)
- [Aktueller Stand](docs/status/current_status.md)
- [Projektprioritaeten](docs/status/project_priorities.md)
- [Kanonisches Modellvokabular](docs/reference/model_vocabulary.md)
- [Implementierte Gleichungen](docs/reference/implemented_equations.md)
- [Repository Map](docs/reference/repository_map.md)
- [Kuratierter Report-Index](reports/README.md)

## Installation und Pruefung

```bash
python -m pip install --require-hashes -r requirements-lock.txt
python -m pip install --no-deps --no-build-isolation -e .
python -m pytest tests -q
python -m mkdocs build --strict
```

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

## Experimentzugang

```bash
python experiments/cli.py --list
python experiments/cli.py reference --list
python experiments/cli.py dynamics --list
python experiments/cli.py markov --list
```

Ergebnisberichte sind datierte Evidenzartefakte. Prospektive Reihenfolge und
Laufautorisierung stehen ausschliesslich in den
[Projektprioritaeten](docs/status/project_priorities.md).
