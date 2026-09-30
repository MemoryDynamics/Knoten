# Attempt 3: rationale Regularitaetsrelation fuer den Unendlichkeits-Astlink

Datum: 2026-09-30.

Status: **vor jeder Attempt-3-Zielrechnung eingefroren**.

## 1. Anlass und unveraenderte Wissenschaft

Attempt 2 bestaetigte, dass die exakte Binaer-zu-Dezimal-Abbildung allein
nicht genuegt: Der nachgelagerte Validator addierte lange Dezimalendpunkte im
globalen 28-stelligen `Decimal`-Kontext. Kein Panel- oder Entscheidungsrecord
wurde publiziert. Bekannt sind nur Receipt und Abbruchrelation.

Attempt 3 behaelt Homotopie, Parameter, Mittelpunkt, Halbbreite $10^{-10}$,
Tailbounds, Praezisionen 120/160, strikten Krawczyk-Einschluss,
$\rho_\infty<1$, Ueberlappung und Klassifikation unveraendert bei.

## 2. Exakte Relationsarithmetik

Jeder bereits exakt serialisierte Dezimaltext wird mittels

```python
Fraction(Decimal(text))
```

als exakte rationale Zahl interpretiert. Fuer jede Defektzeile ist

\[
r_i=\sum_j\max(|\underline d_{ij}|,|\overline d_{ij}|)
\]

vollstaendig in `Fraction`-Arithmetik zu berechnen. Auch die gespeicherte
Zeilensummenobergrenze wird als `Fraction` verglichen. Kein globaler oder
lokaler `Decimal`-Praezisionskontext darf diese Relation beeinflussen.

Die gespeicherte Regularitaetszusammenfassung bleibt der groesste exakte
Dezimalendpunkt der beiden Zeilensummenintervalle und muss weiterhin strikt
kleiner als eins sein. Produktionsvalidator und unabhaengiger Auditor
implementieren die rationale Relation getrennt.

## 3. Attempt-3-Identitaet

Attempt 3 verwendet ein v3-Schema mit `attempt=3`, eigene Governance und
eigene Receipt-, Resultat-, Report-, Audit- und Manifestpfade mit Kennung
`attempt_3_2026-09-30`. Beide frueheren Receipts und Incidentreviews werden
als geschuetzte Provenienzinputs gebunden und niemals ueberschrieben.

## 4. Falsifikationstests

Vor einer Autorisierung muessen mindestens bestehen:

1. das synthetische Gegenbeispiel
   $2\cdot0.12345678901234567890123456789$ gegen seinen exakten Summenwert;
2. Invarianz derselben Relation unter Aenderung des globalen
   `Decimal`-Kontexts auf kleine Praezisionen und verschiedene Rundungsmodi;
3. Zurueckweisung einer um die kleinste Dezimaleinheit inward manipulierten
   Zeilensummenobergrenze in Produktionsvalidator und Auditor;
4. die Attempt-2-Endpointtests einschliesslich malformer Binaertupel;
5. geschlossene Governance, exklusive neue Pfade, v3-Attemptbindung und
   geschuetzte Incidentkette;
6. fokussierter und vollstaendiger Test, Ruff, strict Docs und offizielle CI.

## 5. Claimgrenze

Die Entscheidungsbezeichnungen und erlaubte Sprache bleiben identisch. Ein
Pass waere nur ein lokaler uniformer Rootast-Link
$F_{3600}\to F_\infty$. Er waere kein dynamischer
$H\to\infty$-Stabilitaetsbeweis und kein Claim zu globaler Eindeutigkeit,
Formation, Interaktion, Spin, Traegheit oder physikalischer Masse.

Dieses Protokoll autorisiert keinen Zielzugriff.
