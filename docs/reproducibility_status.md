# Reproduzierbarkeitsstatus

Stand: 2026-06-14.

## Git

- Repository: `https://github.com/MemoryDynamics/Knoten`.
- Arbeitsbranch: `main`.
- `main` tracked `origin/main`.
- Der historische Branch `cleanup` bleibt als Referenz vorhanden.
- Der alte `master`-Branch sollte nicht mehr fuer neue Arbeit genutzt werden.

Lokal untracked sind aktuell zwei Chatverlaufs-Dateien zur Markov- und
Non-Markovian-Recherche. Sie gelten als Nutzer-/Rohkontext, nicht als
kuratierte Projektdokumentation.

## Python-Abhaengigkeiten

Gepinnte Projektdateien:

- `requirements.txt`
- `requirements-dev.txt`
- `docs/requirements.txt`

Kernabhaengigkeiten:

- `numpy`
- `matplotlib`
- `numba`
- `scipy`
- `pandas`
- `pytest`
- `mkdocs` fuer die ReadTheDocs/MkDocs-Dokumentation

Empfohlener Neuaufbau einer Projektumgebung:

```powershell
python -m venv .venv-local
.\.venv-local\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -r requirements-dev.txt
python -m pip install -e .
```

Tests:

```powershell
python -m pytest tests -q
```

Docs:

```powershell
python -m pip install -r docs/requirements.txt
python -m mkdocs build
python -m mkdocs serve
```

## Codex-Runtime

Fuer leichte Tests ist in Codex eine gebuendelte Python-Runtime vorhanden:

```text
C:\Users\Hauke\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe
```

Diese Runtime ist hilfreich fuer kleine NumPy-basierte Checks, aber sie ist
nicht die Zielumgebung fuer lange Numba- oder Matplotlib-Laeufe. Fuer die
vollen Reproduktionslaeufe sollte eine saubere lokale Projektumgebung mit den
gepinnten Requirements genutzt werden.

## Kanonische Smoke-Tests

Minimaler API-Test:

```powershell
$env:PYTHONPATH="src"
python -m pytest tests -q
```

Direkter Referenzlauf:

```powershell
$env:PYTHONPATH="src"
python experiments\reference_experiment.py --seed 2 --steps 2000 --sample-every 20 --burn-in 100 --output data\processed\reference\reference_experiment.json
```

Experiment-CLI:

```powershell
python experiments\cli.py --list
python experiments\cli.py reference --list
python experiments\cli.py reference --script reference_experiment.py
```

## Laufzeitrisiken

Mehrere historische Skripte sind fuer sehr lange Laeufe konfiguriert und
duerfen nicht unbedacht in Tests oder CI laufen:

- `experiments/dimension_selection/2SkalenKernel/emergent_3D_final.py`:
  sehr hohe `N_MAX`-Skalen.
- `experiments/dimension_selection/2SkalenKernel/SpecCovFrac.py`:
  historischer Double-Kernel-Long-Run.
- `experiments/knot_stability/knot_chi_scan.py`: lange Knoten-/Residence-Scans.
- `experiments/dimension_selection/DimensionsHeatmap4OptGPU.py`: GPU/Numba-CUDA.
- `experiments/legacy/scripts/highN_regime*.py`: reproduzierbare Legacy-Regime,
  aber nur mit bewusst kleinen Parametern als Pilot laufen lassen.

## Dimensionsreproduktion

Aktueller belastbarer Stand:

- Der archivierte `D_occ ~ 2.8`-Befund wurde in
  `reports/dimension_claim_seed_audit_2026-06-13.md` aus
  `experiments/fractal_analysis/Fraktale/resultsN.csv` nachvollzogen.
- Staerkster Gruppenbefund:
  `embedding dim = 5`, `N = 60,000,000`, fuenf Runs,
  `mean D_occ = 2.810559`.
- Der neue Reproduktionspfad
  `experiments/fractal_analysis/reproduce_dimension_pilot.py` koppelt bei
  `50k`, `100k` und `300k` plausibel an den historischen Pfad an.
- Kurzlauf-Kontrollen bei `N <= 60k` liefern noch keinen Near-3-Claim.

Naechster sinnvoller Lauf unter realistischer Numba-Umgebung:

```text
embedding dim = 5
N ladder = 1e6, 2.5e6, 6e6
seeds >= 3 initial, spaeter 10-20
conditions = baseline, shuffled_memory, eta_zero, single_scale
diagnostics = D_occ, D_cov, D_spec
```

## Reproduzierbarkeitsluecken

- Alte CSVs enthalten Wiederholungsindizes, aber nicht immer explizite Seeds.
- Lange historische Skripte haben teils hartkodierte Parameter und Pfade.
- Einige Diagnostiken sind empfindlich gegen Fitfenster, Downsampling,
  Voxelgroesse oder `min_count`.
- Der aktuelle Simulation-Output speichert keinen Memory-Trace entlang der
  gesamten Trajektorie.
- Ohne Memory-Traces ist eine echte Transferoperator-/MSM-Schiene nur ueber
  Delay- oder Summary-Features moeglich.

## Definition of Done fuer neue Experimente

Neue Experimente sollten mindestens speichern:

- Git-Revision oder Arbeitsbaumstatus;
- Skriptpfad und Parameter;
- Seed-Liste;
- Abhaengigkeits-/Runtime-Hinweis;
- Roh- oder Processed-Output-Pfad;
- Diagnostikversion und Fitfenster;
- Negativkontrollen oder klare Begruendung, warum sie noch fehlen.
