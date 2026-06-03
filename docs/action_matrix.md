# Action Matrix

Stand: 2026-06-01.

Diese Matrix beantwortet: Was kann Codex allein weiterziehen, und wofuer wird
Hauke gebraucht?

## Kann ich autonom erledigen

### Projektstruktur und Inventar

- lokale Skripte, PDFs, CSV/NPZ/NPY-Dateien weiter katalogisieren
- historische Skriptfamilien in Claim- und Experimentgruppen einordnen
- Querverweise zwischen Paper-Claims, Skripten und Ergebnisartefakten pflegen
- neue Strukturdateien, Reports und Tests im Workspace
  `C:\Users\Hauke\Documents\Emergenz_Knoten` anlegen

### Paper-nahe Arbeit

- Paper-I-Quelle `1.tex` lesen und auditieren
- konkrete Paper-Probleme als Report oder Patch-Vorschlag dokumentieren
- Claim-Sprache schaerfen: Definition / Observation / Conjecture trennen
- offene Formeln, unklare Diagnostiken und fehlende Datenbindung markieren

Wichtig: Direktes Editieren im Paper-Ordner
`C:\Users\Hauke\Documents\Hobby\Weltformel\EmergenteRaumzeit` braucht eine
separate Freigabe, weil dieser Ordner ausserhalb des aktuellen Workspace liegt.

### Reproduzierbarkeit

- mit der gebuendelten Codex-Python-Runtime kleine NumPy-basierte Tests laufen
  lassen
- pure-NumPy-Referenzimplementierungen fuer Kernel, Simulation und Diagnostik
  bauen
- Smoke-Tests und kleine Kontrolllaeufe erstellen
- vorhandene CSV-Dateien mit PowerShell/Python auswerten
- Ergebnisreports erzeugen

Aktuell verfuegbar:

- Codex Python: `C:\Users\Hauke\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe`
- vorhanden: `numpy`, `pandas`
- nicht vorhanden: `matplotlib`, `scipy`, `numba`

### Modellhaertung

- Tests fuer `D_cov`, `D_occ`, Residence/Knotenstatistiken schreiben
- negative Controls vorbereiten
- alte Diagnostiken in saubere Funktionen ueberfuehren
- kurze Parameterprofile bauen, die in Sekunden/Minuten laufen
- bestehende lange Fraktal-CSV-Spuren analysieren

## Brauche ich von Dir

### 1. Schreibfreigabe fuer den Paper-Ordner

Nur wenn ich `1.tex`, `references.bib` oder die dortigen Build-Artefakte direkt
aendern/builden soll. Ohne Freigabe arbeite ich read-only und schreibe Reports
ins Hauptrepo.

### 2. Git-Entscheidung

Das Repo hat noch keinen Commit. Sinnvolle Optionen:

- `baseline-all`: alles Historische inklusive PDFs/NPY/NPZ committen
- `baseline-code-docs`: zuerst Code/Dokumentation committen, grosse Daten
  separat kuratieren
- `no-commit-yet`: weiter lokal strukturieren, aber noch nichts committen

Meine Empfehlung: erst `baseline-code-docs`, danach Datenartefakte bewusst
kuratieren.

### 3. Python/Plotting/GPU

Fuer kleine Tests reicht die Codex-Runtime. Fuer volle Reproduktion der
historischen Skripte brauchen wir eine funktionierende lokale Umgebung mit:

- `numpy`
- `matplotlib`
- `numba`
- `scipy`
- `pandas`
- optional CUDA/Numba-CUDA fuer GPU-Laeufe

### 4. Prioritaet des ersten grossen Claims

Wenn Du nichts anderes sagst, nehme ich diese Reihenfolge:

1. `D_occ ~ 2.8/3` aus vorhandenen Fraktal-Laeufen reproduzierbar machen.
2. Paper-I-Formeln/Definitionen reparieren.
3. `c_eff`/Time-of-flight Experimente haerten.
4. 3D-Selektionsargument formal sortieren.

### 5. Externe Datenquellen

Falls wichtige Daten ausserhalb des Workspaces liegen, brauche ich nur Pfade.
Ich kann dann read-only inventarisieren und entscheiden, ob eine Kopie ins Repo
sinnvoll ist.

## Bereits umgesetzt am 2026-06-01

- Paper-I-Ordner gefunden und `1.tex` gelesen.
- Aktueller Paper-I-PDF-Build erkannt: 9 Seiten, erstellt am 2026-06-01.
- Gebuendelte Codex-Python-Runtime geprueft.
- Pure-NumPy-Referenzkern unter `src/emergenz_knoten` angelegt.
- Tests unter `tests/test_core.py` angelegt und erfolgreich ausgefuehrt.
- Smoke-Test unter `scripts/smoke_test.py` angelegt und erfolgreich ausgefuehrt.
