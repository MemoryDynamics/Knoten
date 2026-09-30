# Unendlichkeits-Astlink Attempt 2: Decimal-Kontext-Incident

Datum: 2026-09-30.

Verdict: **`g-infinity-branch-link-attempt-2-inconclusive-decimal-context-failure`**.

## Ausgefuehrter Zugriff

Attempt 2 war an Implementierungsrevision
`4e751cf991621ad4fa89db76079e1d3a72c54e02`, Governance-Revision
`4d78de49a03ec5dfe6846f7c55741e7556704d75`, CI-Run `36778524389` und
Autorisierungs-ID `633fcbc2-cfaa-4d90-a926-e6e13b93e8d4` gebunden. Das
exklusive Receipt wurde erzeugt:

- Pfad: `reports/dynamics/rotation/scalar_memory_rotating_wave_horizon_infinity_branch_link_attempt_2_receipt_2026-09-30.json`;
- SHA-256: `dc3cfc986aec67c0cac6d4e227454dec109ed5396ac6769a6d69bf7ef0700ead`.

Der Zugriff ist verbraucht und wird nicht wiederholt.

## Abbruch und Artefaktlage

Wie in Attempt 1 stoppte die interne Produktionsvalidierung vor Publikation
mit

```text
ValueError: $.homotopy.panels: inward regularity bound
```

Attempt-2-Resultat, Report, unabhaengiger Audit und Manifest existieren
nicht. Nur das exklusive Receipt ist erhalten.

## Neue kausale Diagnose

Die Attempt-2-Remediation rekonstruiert die binaeren Intervallendpunkte exakt
als Dezimaltexte. Die nachfolgende Funktion `_row_norm_upper` addiert diese
langen `Decimal`-Werte jedoch ausserhalb eines expliziten Kontextes. Damit
verwendet Python den globalen 28-stelligen Standardkontext und rundet eine
eigentlich exakte Summe erneut.

Das folgende targetfreie Gegenbeispiel reproduziert den Fehler:

```text
x = 0.12345678901234567890123456789
Decimal(x) + Decimal(x) = 0.2469135780246913578024691358
exact(x + x)             = 0.24691357802469135780246913578
```

Die standardmaessig gerundete `Decimal`-Summe ist groesser als die exakte
Summe. Ein exakt korrekter gespeicherter Zeilensummenendpunkt kann deshalb
erneut faelschlich als inward erscheinen. Derselbe Summationspfad existiert
im Produktionsvalidator und im getrennten Auditor.

## Befundtrennung

**Evidenz:** Attempt 2 erreichte nach erfolgreicher Binaerendpunktkonvertierung
erneut die Regularitaetsrelationspruefung und publizierte keinen Record.

**Gesicherte Methodendiagnose:** Das obige kurze Gegenbeispiel beweist, dass
der verwendete `Decimal`-Summationspfad die Ordnungsrelation ohne
Zielrechnung verletzen kann.

**Nicht belegt:** Weder Bestehen noch Scheitern von Krawczyk-Einschluss oder
uniformer Regularitaet ist aus Attempt 2 ableitbar. Der Incident ist kein
wissenschaftliches Negativergebnis.

## Enge Folgeremediation

Ein Attempt 3 darf erneut keine wissenschaftliche Groesse veraendern. Er
muss lediglich alle Summen und Vergleiche entscheidungsrelevanter
Dezimalendpunkte als exakte rationale Zahlen auswerten, etwa mittels
`fractions.Fraction(Decimal(text))`. Das oben angegebene 29-stellige
Gegenbeispiel muss in Produktionsvalidator und Auditor als Regressionstest
gebunden werden. Neue Pfade, Schema-/Attemptbindung, Review, CI und
Einmalautorisierung bleiben Pflicht.
