# Action Matrix

Stand: 2026-06-14.

Diese Matrix beantwortet: Was kann Codex autonom weiterziehen, und wofuer wird
Hauke gebraucht?

## Kann Codex autonom erledigen

### Dokumentation und Inventar

- ReadTheDocs/MkDocs pflegen.
- Projektkarte, Architektur, Experiment-Katalog und Claim-Register aktuell
  halten.
- Historische Skripte und Ergebnisartefakte fachlich einordnen.
- Reports fuer neue Laeufe oder Audits schreiben.

### Code und Reproduzierbarkeit

- Kleine NumPy-basierte Tests und Smoke-Tests ausfuehren.
- Paketkern unter `src/emergenz_knoten` erweitern.
- Tests unter `tests/` ergaenzen.
- Ergebnisformate und Manifeste standardisieren.
- Kurze Reproduktionslaeufe starten, sofern die lokale Umgebung die
  Abhaengigkeiten bereitstellt.

### Non-Markovian / Markov-Embedding Schicht

- Memory-Summary-Features entwerfen.
- Additive Module unter `src/emergenz_knoten/markov/` anlegen.
- Lagged-Dataset-, Transition-Count- und Validation-Funktionen bauen.
- Tests fuer synthetische Markov-Ketten und nichtmarkovsche Projektionen
  schreiben.
- Ergebnisse gegen Residence- und Dimensionsdiagnostiken querpruefen.

### Paper-nahe Arbeit

- Paper-I-Quelle lesen und gezielt patchen.
- Abschnitte zu Minimalmodell, emergenter Zeit, Knoten, Masse und Diagnostik
  mit der Non-Markovian-Basis abgleichen.
- Claim-Sprache schaerfen: Definition / numerical observation / conjecture.
- Patch-Reports oder direkte LaTeX-Edits im Workspace ausfuehren.

## Braucht Haukes Entscheidung

### Paper-Reihenfolge

Optionen:

- **Paper 0 zuerst:** Literatur- und Methodenbasis fuer finite-memory
  self-interacting processes, Markov-Einbettung, Transferoperatoren.
- **Paper I zuerst:** bestehendes Minimalmodell schrittweise haerten und
  Non-Markovian-Basis in die aktuelle Erzaehlung integrieren.

Empfehlung aus aktuellem Stand: Paper 0 ist strategisch stark, weil es die
Mathematik und Methodensprache klaert, bevor Paper I groessere Physikclaims
traegt.

### Rechenumgebung

Fuer lange Fraktal-/Dimensionslaeufe braucht es eine funktionierende lokale
Python/Numba-Umgebung mit:

- `numpy`
- `matplotlib`
- `numba`
- `scipy`
- `pandas`

Codex kann kleine Checks machen, aber die Millionen-/Zehnmillionen-Laeufe
sollten in einer bewusst eingerichteten Projektumgebung laufen.

### Claim-Prioritaet

Wenn nichts anderes gesagt wird, ist die Reihenfolge:

1. Non-Markovian Basis / Markov-Einbettung operationalisieren.
2. Archivierten `D_occ ~ 2.8`-Befund im Millionenbereich reproduzieren.
3. Paper I mit sauberer Claim-Sprache ueberarbeiten.
4. Propagation/`c_eff` und Paper II danach haerten.

## Aktuelle No-Gos

- Keine eindeutige 3D-Selektion behaupten, bevor Seed-Ensembles,
  Negativkontrollen und robuste Fitfenster vorliegen.
- `spectral_dimension` aus `diagnostics.py` nicht als Transferoperator-Spektrum
  formulieren.
- Historische Chatnotizen nicht als zitierfaehige Quelle behandeln.
- Long-Run-Skripte nicht als CI- oder Smoke-Tests starten.
- Alte Ergebnisdaten nicht ohne Parameter-/Seed-Kontext als neue Evidenz
  ausgeben.

## Sofort anschlussfaehige Tasks

1. `src/emergenz_knoten/markov/dataset.py` mit Delay- und
   Memory-Summary-Features.
2. `src/emergenz_knoten/markov/transition.py` mit Counts und
   zeilenstochastischen Matrizen.
3. `src/emergenz_knoten/markov/validation.py` mit implied timescales und
   einfachen CK-Fehlern.
4. Paper-I-Patch: sichtbarer nichtmarkovscher Prozess vs. augmentierter
   Markov-Zustand.
5. Numba-faehiger Millionenlauf fuer `embedding dim = 5` mit expliziten Seeds.
