# Reproduzierbarkeitsstatus

Stand: 2026-06-13.

Update 2026-06-13: `main` ist die Arbeitslinie. Der ehemalige `cleanup`-Stand
wurde als `origin/main` gepusht und der GitHub-Default-Branch wurde vom Nutzer
auf `main` gesetzt.

Update 2026-06-01: Eine gebuendelte Codex-Python-Runtime ist verfuegbar und
reicht fuer kleine NumPy/Pandas-basierte Tests. Die lokale Projekt-`.venv`
bleibt defekt.

## Git

- Repository: `https://github.com/MemoryDynamics/Knoten`
- Arbeitsbranch: `main`
- Historischer Branch `cleanup` bleibt als Referenz vorhanden.
- Alter `master`-Branch zeigt nur auf den Baseline-Import und sollte nicht mehr
  fuer neue Arbeit verwendet werden.

## Lokale Tools

Verfuegbar:

- `pdftotext.exe` unter `C:\Tools\texlive\2025\bin\windows\pdftotext.exe`
- `pdfinfo.exe` unter `C:\Tools\texlive\2025\bin\windows\pdfinfo.exe`

PDF-Metadaten:

- `main-5.pdf`: TeX, 6 Seiten, erstellt 2026-03-22.
- `1-3.pdf`: TeX, 9 Seiten, erstellt 2026-03-20.
- `N_D29.pdf`: Matplotlib, 1 Seite, erstellt 2026-03-22.

## Python

Beim Audit wurde aus der Codex-Umgebung kein globales `python`/`py` auf PATH
gefunden. Der Nutzer meldet, dass
`experiments/fractal_analysis/reproduce_dimension_pilot.py` aus seiner
PowerShell heraus mit `numba` laeuft; diese Umgebung ist aus Codex heraus
aktuell nicht direkt sichtbar.

Die vorhandenen virtuellen Umgebungen sind nicht lauffaehig:

- `.venv\Scripts\python.exe` scheitert mit
  `ModuleNotFoundError: No module named 'encodings'`.
- `.venv1\Scripts\python.exe` verweist auf
  `C:\Users\Hauke\AppData\Local\Programs\Python\Python311\python.exe`,
  das nicht gestartet werden konnte.

Empfohlener Fix:

1. Python 3.11 oder 3.12 installieren bzw. Pfad reparieren.
2. Neue Umgebung anlegen.
3. `pip install -r requirements.txt`.
4. Import-Smoke-Test ausfuehren:

```powershell
python -c "import numpy, matplotlib, numba, scipy, pandas; print('ok')"
```

## Codex-Runtime

Verfuegbar fuer leichte Tests:

```text
C:\Users\Hauke\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe
```

Geprueft am 2026-06-13:

- Python 3.12.13
- `numpy` vorhanden
- `pandas` vorhanden
- `matplotlib` nicht vorhanden
- `scipy` nicht vorhanden
- `numba` nicht vorhanden

Ein kleines reproduzierbares Referenzskript wurde hinzugefuegt:
`scripts/reference_experiment.py`.
Es laesst sich mit dem Codex-Python-Interpreter ausfuehren und liefert
quantitative Diagnostik (inkl. `D_cov`, `D_occ` und residence statistics).

Beispiel:

```powershell
C:\Users\Hauke\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe scripts\reference_experiment.py --seed 2 --steps 2000 --sample-every 20 --burn-in 100 --output reference_experiment.json
```

Damit sind kleine Referenztests moeglich. Fuer die langen Fraktal- und
Dimensionslaeufe sollte die vom Nutzer genannte PowerShell/Numba-Umgebung
verwendet werden.

## Laufzeitrisiken

Mehrere Skripte sind fuer sehr lange Laeufe konfiguriert:

- `2SkalenKernel/emergent_3D_final.py`: `N_MAX = 2e8`
- `2SkalenKernel/SpecCovFrac.py`: `N = 150_000_000` mit `d=7`, `alpha=0.002`, `eta=0.15`, `epsilon=0.03`, `sigma_rep=1.0`, `sigma_att=3.0`, `A_rep=1.0`, `B_att=0.35`
- `knot_chi_scan.py`: `N_MAX = 50_000_000`
- `DimensionsHeatmap4OptGPU.py`: GPU/Numba-CUDA und `T = 1_500_000`

Ein neuer Pilot-Wrapper wurde hinzugefuegt: `scripts/highN_regime.py` reproduziert den historischen
`2SkalenKernel/SpecCovFrac.py`-Regime in der Referenzimplementierung.
Ein zusätzliches Validierungsskript `scripts/highN_regime_validation.py` bietet einen leichtgewichtigen, parametrisierten Einpunkttest nach dem gleichen 7D-Regime.
Ein kleines Pilotlauf mit `steps=20000` und `sample_every=2000` erreicht etwa `1000` Schritte/Sekunde.
Daraus ergibt sich eine realistische Laufzeitschätzung von ca. `40` bis `42` Stunden fuer `N=150_000_000` auf der aktuellen Maschine.

Ein neuerer Validierungslauf wurde mit `--steps 100000 --sample-every 200 --n-scales 15 --min-count 3` ausgefuehrt und in `highN_regime_validation_100k_200_details.json` gespeichert. Dabei ergaben sich fuer Seed 1:

- `D_cov ≈ 4.15`
- `D_occ ≈ 0.20`

Damit ist der Referenzpfad lauffaehig, aber die diagnostische Interpretation bleibt empfindlich gegen die gewaehlte Sampling-Dichte.

Diese Skripte sollten nicht direkt als Tests laufen. Fuer CI/Smoke-Tests
brauchen wir kleine Parameterprofile.

## Minimale Abhaengigkeiten

Aus den Imports ergeben sich mindestens:

- `numpy`
- `matplotlib`
- `numba`
- `scipy`
- `pandas`

Optional spaeter:

- `pytest` fuer Tests
- `ruff` fuer Format/Lint
- `pyyaml` oder `tomli` fuer Experiment-Manifeste

## Reproduzierbarkeitsluecken

- Seeds sind nicht ueberall explizit.
- Lange Runs schreiben teils direkt in relative Pfade.
- Parameter sind in Skripten hartkodiert.
- Ergebnisdaten haben keine durchgaengige Manifest-Verknuepfung.
- Einige Diagnostiken haben frei waehlbare Fenster, Voxel oder Fitbereiche.

Diese Luecken sind normal fuer eine gewachsene Exploration, aber vor
Paper-Haertung muessen sie geschlossen werden.
