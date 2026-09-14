# Review: targetfreie G5-Stabilitaetsadapter

Datum: 2026-09-14.

RED-Ausgangsrevision: `b5205a3`.

Verdict:
**`horizon-g5-adapters-target-free-pass-g5-unmeasured`**.

## 1. Scope

Geprueft und implementiert wurde ausschliesslich die Abbildung der
vorhandenen Voll-FIFO-Stabilitaetskerne in den v3-Horizontrecord. Weder der
registrierte H=2400-Root noch ein reales Arnoldi-Panel oder eine reale
Stoerungsfortsetzung wurde ausgewertet. Das Resultat ist Code- und
Vertragsevidenz, kein Stabilitaetsbefund.

## 2. Abgegrenzter Arnoldi-Kern

Die abgeschlossenen P3-, P4-, P4R- und P4RS-Protokolle frieren
`src/emergenz_knoten/rotating_wave_stability_gate.py` ueber Blob-Hashes ein.
Der erste Implementierungsversuch veraenderte diese Datei und war deshalb
architektonisch unzulaessig. Der historische Kern wurde exakt auf den
eingefrorenen Git-Blob `630beb9952abefea823d91388dcbb2de8f1a2927`
zurueckgesetzt.

Der neue, horizontspezifische Kern liegt stattdessen in
`src/emergenz_knoten/rotating_wave_horizon_stability.py`. Er verwendet die
gemeinsamen Datentypen und Symmetrieklassifikation, veraendert aber keine
historisch gebundene Quelldatei. Ein externer reeller Startvektor wird auf
Dimension, Endlichkeit und Nichtnullheit geprueft und unveraendert als `v0`
an ARPACK uebergeben. Zu jedem Ritzpaar werden alle 4800 komplexen
Vektorkomponenten gespeichert.

## 3. H=2400-Adapter

Der neue Adapter konstruiert aus dem einmal binary64-gerundeten Root die
Kreisgeschichte, die mitrotierende native FIFO-Map und deren gemeinsamen
sparse Jacobian. Vor Arnoldi gelten fail-closed:

- maximaler binary64-Fixed-Point-Fehler `1e-14`;
- Jacobianform `4800 x 4800` mit `19196` gespeicherten Eintraegen;
- analytische Translations-/Rotationsresiduen jeweils hoechstens `1e-10`;
- exakter SHA-256-Abgleich des uebergebenen LCG-Starts.

Die zwei Panelkonfigurationen bleiben unveraendert bei 24/96/`1e-10`/20000
und 36/144/`1e-12`/40000. Partielle, vektorlose, nichtendliche und
residualfehlerhafte Ausgaben werden in feste Slots mit Nullsuffix und einen
expliziten Nicht-Pass-Status abgebildet. Der gespeicherte Modul wird aus den
serialisierten Real-/Imaginaerteilen neu berechnet, damit der Validator
genau dieselben primitive Werte rekonstruiert.

## 4. Trajektorien und Entscheidungslogik

Radialer, tangentialer und vollhistorisch-transversaler Stoerungsvektor
werden vor der Fortsetzung bitgenau gegen die registrierte Konstruktion
geprueft. Der gemeinsame nichtlineare Fortsetzungskern erzeugt 501 feste
Sampleslots fuer Schritte `0,10,...,5000`; ein frueher Stopp behaelt nur das
tatsaechliche Praefix. Der exakte Arm verwendet denselben Kern mit dem
Nullvektor.

Fortsetzungen starten erst nach vollstaendiger 24/36-Kardinalitaet,
vorhandenen Ritzvektoren, Residuen hoechstens `1e-8`, bestandenen
Symmetriemoden, Panelmatch und korrekten LCG-Hashes. Ausserdem stuetzen Runner
und unabhaengiger Auditor Instabilitaet nun nur, wenn das tatsaechlich zum
primaeren Leitpaar gematchte Konvergenzpaar ebenfalls ueber `1+1e-6` liegt.
Ein beliebiges anderes instabiles Paar im zweiten Panel reicht nicht mehr.

## 5. Zusaetzliche Vertragshaertung

Runner und Standardbibliothek-Auditor verwerfen nun negative Ritzresiduen,
unmoegliche Symmetrieueberlappungen sowie gespeicherte Nullvektoren. Der
synthetische Positivzeuge enthielt zuvor nur formale Nullvektoren; er wurde
zu nichttrivialen Einheitszeugen korrigiert. Diese Korrektur betrifft keinen
wissenschaftlichen Ergebnisrecord.

Die Tests decken LCG-Weitergabe bis zum gemockten Solver,
Vektorserialisierung, ungueltige Startvektoren, alle sechs Panelstatus,
mutierte Stoerungen, Trajektorien-Nullsuffixe, den exakten Arm, den
Fixed-Point-Guard und das gematchte Instabilitaetspaar ab. Ein frischer
Pythonprozess reproduziert beide LCG-Hashes und den Vollhistorien-
Stoerungshash auf derselben Plattform.

### CI-Falsifikation des ersten Entwurfs

Der Commit `bfd17ae` bestand lokal 1084 Tests, fiel in CI-Lauf
`34812975681` aber an vier historischen Blob-Sperren durch. Die Ursache war
nicht ein numerisches Zielresultat: Die Sperrtests lesen absichtlich den
committeten `HEAD`-Blob, waehrend der lokale Vorabtest noch den vorherigen
Commit mit nichtcommitteten Aenderungen verglich. Damit war das lokale Gruen
fuer genau diese Provenienzeigenschaft nicht aussagekraeftig. Die CI-
Falsifikation fuehrte zur oben beschriebenen Modultrennung; die vier
Provenienztests muessen deshalb nach dem Korrekturcommit erneut gegen `HEAD`
laufen.

Der exakte Repository-Lint, der strikte Dokumentationsbuild und die gesamte
Repositorytestsuite sind erst nach diesem Korrekturcommit erneut als Evidenz
zu werten. Die eng gefilterten G5-Tests werden zusaetzlich separat
ausgefuehrt.

## 6. Trust Base und offene Risiken

ARPACK/Scipy bleibt ein numerischer Eigensolver, keine vollstaendige
Spektraleinschliessung. Der Standardbibliothek-Auditor rekonstruiert
Ritzslots, Vektornichttrivialitaet, Residualschwellen, Symmetrieklassifikation
und Entscheidung, berechnet aber mangels eigenem sparse Numerikbackend
$Jv-\lambda v$ nicht neu. Die gespeicherten Residuen bleiben daher an den
Ausfuehrungskern gebunden.

Das trigonometrische Vollhistorienprofil ist nur im frischen Prozess auf
derselben Plattform bitgenau bestaetigt; Cross-OS-Portabilitaet ist offen.
Fixed-Point-, Jacobian- und analytische Symmetrieguards blockieren die
Ausfuehrung, ihre gemessenen Einzelwerte besitzt der gegenwaertige v3-Record
jedoch nicht. Diese Werte muessen vor Readiness in den komponierten
Nachweisrecord aufgenommen oder durch einen explizit gehashten Preflight-
Record gebunden werden.

## 7. Entscheidung und naechster Schritt

Die im Meta-Review geforderten Arnoldi- und Trajektorienadapter bestehen
targetfrei. G5 selbst bleibt ungemessen. Als naechstes ist ausschliesslich
die targetfreie Backendkomposition samt persistiertem Fixed-Point-/Jacobian-/
Symmetriepreflight und unabhaengigem Readinessreview zulaessig. Erst dieses
Review darf einen einzelnen H=2400-G5-Zugriff erwaegen. Vollstaendiger
Horizontlauf, P5-D-Versuch 4 und Zwei-Knoten-Transfer bleiben geschlossen.
