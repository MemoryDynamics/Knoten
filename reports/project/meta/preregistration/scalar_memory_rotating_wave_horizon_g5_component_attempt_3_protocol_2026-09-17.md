# Prospektives Protokoll: isolierte G5-Direktsimulation, Attempt 3

Datum: 2026-09-17.

Status: **outcome-blind eingefroren vor Attempt 3**.

## 1. Anlass und Evidenzgrenze

Attempts 1 und 2 sind verbrauchte Pipeline-Incidents ohne publiziertes
G5-Ergebnis. Attempt 1 scheiterte an einer binary64-Recordgrenze. Attempt 2
erreichte die nichtlinearen Fortsetzungen, konnte ihren Record aber nicht
publizieren: Der Integrator bildete das Laufmaximum ueber jeden Schritt, der
Validator rekonstruierte es nur aus jedem zehnten Sample.

Attempt 3 wiederholt unveraendert die wissenschaftliche Untersuchung des
[Erstprotokolls](scalar_memory_rotating_wave_horizon_g5_component_protocol_2026-09-14.md)
und des
[Attempt-2-Protokolls](scalar_memory_rotating_wave_horizon_g5_component_retry_protocol_2026-09-16.md).
Parameter, Grundgleichung, FIFO-Shift, Newtonstart, Krawczykboxen,
Arnoldi-Panels, LCG-Starts, Stoerungsrichtungen, Amplitude, Laufzeit,
Stopregeln, Klassifikationsschwellen und Claimgrenze bleiben unveraendert.
Es gibt keinen Scan, keinen alternativen Root und kein Retuning nach den
nicht persistierten Zielwerten.

## 2. Eingefrorene Trajektoriensemantik

Der v2-Record behaelt das lesbare Zehnersampling und ergaenzt fuer jeden Arm
eine dichte **skalare** Distanzspur

$$
D=(d_0,d_1,\ldots,d_N),\qquad 0\leq N\leq5000.
$$

Sie wird als Array der festen Laenge 5001 mit zusammenhaengendem endlichem
Praefix und anschliessendem `null`-Suffix gespeichert. Damit gelten
rekonstruierbar und bitweise exakt:

$$
d_{\rm initial}=d_0,\qquad
d_{\rm final}=d_N,\qquad
d_{\rm max}=\max_{0\leq n\leq N}d_n,
$$

$$
n_{\rm max}=\min\{n:d_n=d_{\rm max}\},\qquad
g=d_{\rm max}/d_0,\qquad
r=d_N/d_0.
$$

Jedes publizierte Zehnersample muss exakt mit `D[step]` uebereinstimmen. Ein
eventueller letzter off-grid Abbruchpunkt muss ebenfalls als Sample und als
letztes Element des dichten Praefixes erscheinen. Ein vollstaendiger Arm hat
exakt 5001 dichte Werte und 501 Samples. Die exakte Kontrolltrajektorie
verwendet dieselbe dichte Semantik.

Es werden keine vollen 4800-dimensionalen Zwischenzustaende dupliziert. Eine
Toleranz zwischen Vollschrittmaximum und Samplemaximum ist unzulaessig, weil
beide unterschiedliche mathematische Groessen sind.

## 3. Implementierung und Falsifikation

Vor Zielzugriff muessen mindestens folgende targetfreie Tests bestehen:

1. Ein synthetisches Maximum bei Schritt 1 bei Samples 0 und 10 falsifiziert
   die alte Sample-Rekonstruktion und besteht nur mit der dichten Spur.
2. Loch im Praefix, nichtendlicher oder negativer Abstand, falsche feste
   Laenge und Wert nach dem `null`-Suffix werden verworfen.
3. Manipulierte Anfangs-, End-, Maximums-, Maximumsschritt-, Wachstums- und
   Endquotienten werden verworfen.
4. Sample und dichte Spur muessen fuer jeden publizierten Schritt exakt
   uebereinstimmen.
5. Backend, Komponentenvalidator und unabhaengiger Auditor rekonstruieren die
   Beziehungen getrennt.
6. Attempt-1-, Attempt-2- und Attempt-3-Pfade sind disjunkt; falsche
   Attemptnummer, Blobdrift, rote CI, gemischter Governancecommit und bereits
   vorhandene Attempt-3-Zielpfade stoppen vor Receipt und Zielnumerik.

Die allgemeine Fortsetzungsbibliothek darf die dichte skalare Spur einmalig
erzeugen. Experimentadapter duerfen die Dynamik nicht duplizieren. Der neue
v2-Vertrag ersetzt fuer Attempt 3 den v1-Vertrag; historische v1-Artefakte
bleiben unveraendert.

## 4. Attempt-3-Artefakte

- Receipt:
  `scalar_memory_rotating_wave_horizon_g5_component_attempt_3_receipt.json`;
- Ergebnis:
  `scalar_memory_rotating_wave_horizon_g5_component_attempt_3_2026-09-17.json`;
- gleichnamiger Lesereport und manifest-zuletzt-Publikationsrecord;
- Ergebnisvertrag:
  `scalar_memory_rotating_wave_horizon_g5_component_result_schema_v2.json`.

Der Guard bindet Attempt 3, Implementierungscommit, exakte erfolgreiche CI,
Readinessreview, Dependencyversionen, geschuetzte Blobs, sauberen Upstream
und leere Attempt-3-Zielpfade. Die Receipt entsteht atomar vor jeder
Zielnumerik. Jeder spaetere Fehler verbraucht Attempt 3.

## 5. Entscheidung und Stopregel

Zulaessig bleiben ausschliesslich lokaler Stabilitaetspass, reproduzierbar
gestuetzte lokale Instabilitaet, `inconclusive` oder bei Vertrags- und
Provenienzfehlern `experiment-invalid`. Kein Ausgang begruendet globale
Stabilitaet, Formation, Interaktion, Traegheit oder physikalische Masse.

Ein Major-/Critical-Befund, rote exakte CI, unvollstaendiges Review,
schmutziger Arbeitsbaum oder ungeklaerte Abweichung stoppt vor Zielzugriff.
Sind RED-Test, Implementierung, unabhaengiger Auditor, Meta-Review und CI
gruen, erlaubt die ausdrueckliche Nutzerentscheidung vom 2026-09-17 genau
einen Governance-only-Autorisierungscommit und genau einen Attempt-3-Lauf.
Es gibt keinen automatischen Attempt 4.
