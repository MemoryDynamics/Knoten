# Emergenz Knoten

Arbeitsrepository fuer ein minimalistisches Weltmodell aus irreversibler
Speicherdynamik, metastabilen "Knoten" und emergenten effektiven Strukturen.

Stand: 2026-07-18.

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
- Der aktuelle kleine-Radius-Ast laesst sich auf einen attraktiven
  Ein-Kernel-Fall reduzieren: Die seed-gematchten (1,35)- und
  (0,26)-Varianten stimmen im N=300k-Slice bis etwa 1e-8 relativ ueberein.
- Der A_att=0..40-Scan ohne A_rep zeigt keinen endlichen Phasenuebergang.
  Fuer A_att>=5 folgt der dynamische Radius der linearen
  Memory-Center-Vorhersage mit 0.94 Prozent medianem Fehler.
- Die Paper-I-Evidenz ist deshalb als co-moving linear scalar relaxation-cloud
  evidence zu lesen: kein fixes absolutes Zentrum, kein isolierter
  nichtlinearer Knotenmechanismus und kein physikalischer Teilchenclaim.
- D_mem nahe drei im d=3-Embedding ist im aktuellen Taylor-Regime erwartete
  isotrope Gaussgeometrie und keine Evidenz emergenter Dreidimensionalitaet.
- Long-Run-Trace-AR findet komplexe Klassifikationen auch in `eta_zero`; es
  gibt daher keinen kontrollgetrennten skalaren Phasen-/Photonmodus.
- Feature-Closure stuetzt die skalare Grobkoernung fuer Shape-/Radius-Scalars,
  nicht fuer den Spin-Scalar.
- Der `A_att`-Uebergang fuer `d=3` und `d=10` zeigt eine Trennung von
  sichtbarer Sample-Geometrie (`D_cov`) und interner Memory-Shape (`D_mem`);
  die `beta=0`-Referenz ist als `M0=0`/`m0_zero` dokumentiert.
- Der Code unterscheidet `delta`, `gaussian` und `matched_gaussian`
  Deposition; `memory_mass=M0` ist als eigene Memory-Skala abgebildet.

Noch nicht belastbar:

- ein spezifisch zweiskaliger Baseline-Knotenmechanismus; die gematchte
  attraktive Ein-Kernel-Ablation ist im aktuellen Regime numerisch gleich;
- eindeutige externe d=3-Selektion; D_mem nahe der Ambient-Dimension ist
  im linearen isotropen Regime zu erwarten und kein Selektionssatz;
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

1. Vorhandene N=30M/300M-Daten gegen den analytischen linearen Relativradius
   reconciliieren; keine neue rohe A_att-, eta- oder M0-Suche.
2. Bei festem g=26/60 einen Fuenf-Seed-Slice mit gezieltem
   R_linear/L ungefaehr 0.03, 0.1 und 0.3 rechnen. Nur kontrollierte
   Abweichungen vom linearen Benchmark rechtfertigen einen nichtlinearen
   Knotenclaim.
3. Danach den vorbereiteten Relaxations-Diffusionsfeldzweig mit explizitem
   Feldzustand und Greenkernel-Kontrollen testen, falls der skalare Slice keine
   neue Struktur zeigt.
4. Mehrknoten-, signierte Cross- und Vektormemory-Gates bleiben Folgearbeit.
   Rekreuzung wird nicht als eigenes Ziel weiterverfolgt.