# Attempt 4: Runtimebindung und Import-vor-Receipt fuer den Unendlichkeits-Astlink

Datum: 2026-10-01.

Status: **vor jeder Attempt-4-Zielrechnung eingefroren**.

## 1. Anlass und unveraenderte Wissenschaft

Attempt 3 erreichte das mathematische Gate nicht. Nach Erzeugung des
exklusiven Receipts scheiterte bereits der Gate-Import an einer lokal
inkompatiblen Kombination aus NumPy 2.5 und Numba 0.63.1. Resultat, Audit und
Manifest wurden nicht erzeugt; bekannt sind nur Receipt, Importausnahme und
Incidentreview.

Attempt 4 behaelt Homotopie $F_s=F_{3600}+sT_{3600}$, Parameter,
Mittelpunkt, Halbbreite $10^{-10}$, Tailbounds, Praezisionen 120/160,
strikten Krawczyk-Einschluss, rationale Regularitaetsrelation
$\rho_\infty<1$, Ueberlappung und Klassifikation bytegleich bei. Es findet
keine wissenschaftliche Schwellen- oder Parameteranpassung statt.

## 2. Vollstaendige Runtimebindung

Die Autorisierung muss neben `requirements-dev.txt` auch
`requirements.txt` und `pyproject.toml` als Git-Blobs schuetzen. Vor jedem
Receipt werden exakt die folgenden installierten Direktversionen geprueft:

| Komponente | Version |
| --- | --- |
| Python | `3.12` |
| mpmath | `1.3.0` |
| NumPy | `2.3.5` |
| Matplotlib | `3.10.8` |
| Numba | `0.63.1` |
| SciPy | `1.17.1` |
| pandas | `3.0.3` |

Eine frische Laufumgebung wird in CI-Reihenfolge aus `requirements.txt` und
`requirements-dev.txt` aufgebaut. Abweichung oder fehlende Metadaten muessen
vor Receipt hart scheitern.

## 3. Import-vor-Receipt-Semantik

Nach erfolgreicher Governance-, Blob-, CI-, Upstream-, Cleanliness- und
Outputpfadpruefung, aber vor `_create_receipt`, muessen Gate und
Standardbibliotheksauditor ueber denselben Loader importiert werden, der auch
im spaeteren Lauf verwendet wird. Erst wenn beide Imports erfolgreich sind,
darf das exklusive Receipt atomar entstehen. Die bereits geladenen
Modulobjekte werden anschliessend fuer Zielrechnung, Publikation und
Verifikation weiterverwendet; kein zweiter Importpfad darf dazwischen liegen.

Modulimport ist targetfrei: Weder Gate noch Auditor duerfen beim Import eine
Zielrechnung, Publikation oder Zielpfadmutation ausfuehren.

## 4. Attempt-4-Identitaet und Provenienz

Attempt 4 verwendet ein v4-Schema mit `attempt=4`, eigene Governance und
eigene Receipt-, Resultat-, Report-, Audit- und Manifestpfade mit Kennung
`attempt_4_2026-10-01`. Die Receipts und Incidentreviews aller drei frueheren
Attempts werden als geschuetzte Provenienzinputs gebunden und niemals
ueberschrieben.

## 5. Falsifikationstests vor Autorisierung

Mindestens muessen bestehen:

1. Ein injizierter Gate-Importfehler erzeugt weder Receipt noch Zielartefakt.
2. Ein injizierter Auditor-Importfehler erzeugt weder Receipt noch
   Zielartefakt.
3. Bei erfolgreichen Imports ist die Reihenfolge
   `guard -> imports -> receipt -> target -> publish -> verify`; Gate und
   Auditor werden je genau einmal geladen.
4. Jede einzelne falsche oder fehlende Runtime-Version stoppt vor Import und
   Receipt.
5. `requirements.txt`, `requirements-dev.txt`, `pyproject.toml`, Package-
   Initializer und transitiv importierter Numba-Einstieg sind blobgebunden.
6. Attempt-3-Receipt und -Incident sind gebunden; alle Attempt-4-Zielpfade
   sind exklusiv und unbeschrieben.
7. Rationale Relations-, Endpoint- und inward-Manipulationstests aus Attempt
   3 bleiben unveraendert gruen.
8. Fokussierte und vollstaendige Tests, Ruff, strict Docs und offizielle CI
   bestehen in der gepinnten Runtime.

## 6. Claimgrenze

Ein Pass waere nur ein lokaler uniformer Rootast-Link
$F_{3600}\to F_\infty$. Er waere kein dynamischer
$H\to\infty$-Stabilitaetsbeweis und kein Claim zu globaler Eindeutigkeit,
Formation, Interaktion, Spin, Traegheit oder physikalischer Masse.

Dieses Protokoll autorisiert keinen Zielzugriff.
