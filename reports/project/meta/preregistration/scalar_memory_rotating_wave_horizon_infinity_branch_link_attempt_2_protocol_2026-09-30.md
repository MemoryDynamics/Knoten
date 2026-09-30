# Attempt 2: exakte Endpunktserialisierung fuer den Unendlichkeits-Astlink

Datum: 2026-09-30.

Status: **vor jeder Attempt-2-Zielrechnung eingefroren**.

## 1. Anlass und Outcome-Blindheit

Attempt 1 endete nach Erzeugung seines exklusiven Receipts, aber vor jeder
Publikation, mit `inward regularity bound`. Es wurde kein Panel-, Gate- oder
Entscheidungsrecord erhalten. Bekannt ist nur, dass mindestens eine aus den
gerenderten Defektmatrixeintraegen rekonstruierte Zeilennorm groesser als die
separat gerenderte Zeilensummenobergrenze war.

Attempt 2 darf deshalb ausschliesslich die Serialisierung reparieren. Box,
Tail-Homotopie, Mittelpunkt, Tailbounds, Praezisionen, Krawczyk-Operator,
Regularitaetsschwelle und Klassifikation aus dem Erstprotokoll bleiben
byte- beziehungsweise wertgleich.

## 2. Exakte Binaer-zu-Dezimal-Abbildung

Ein endlicher `mpmath`-Endpunkt liegt als Tupel $(s,m,e,b)$ vor, wobei
$s\in\{0,1\}$ das Vorzeichen, $m\ge0$ die Mantisse und $e\in\mathbb Z$ den
Binaerexponenten bezeichnet. Sein exakter Wert ist

\[
(-1)^s m2^e.
\]

Der Produktionsadapter muss daraus ohne Gleitkomma- oder
Praezisionskontext einen kanonischen endlichen Dezimaltext erzeugen:

- fuer $m=0$: `0`;
- fuer $e\ge0$: die ganze Zahl $(-1)^s(m\ll e)$;
- fuer $e=-k<0$: $(-1)^s(m5^k)10^{-k}$ mit exakt gesetztem Dezimalpunkt;
- abschliessende Nachkommastellen `0` und danach ein leerer Dezimalpunkt
  werden entfernt; negative Null ist verboten.

Der Adapter muss Tupellaenge, echte Integerfelder (keine Booleans),
$s\in\{0,1\}$, $m\ge0$, $b=m.\mathrm{bit\_length}()$ fuer $m>0$ und eine
registrierte Exponentengrenze validieren. Malforme oder uebergrosse Tupel
sind harte Vertragsfehler.

Die bisherigen gerenderten `lower`-/`upper`-Felder duerfen nur diagnostisch
existieren. Alle entscheidungsrelevanten Dezimalintervalle werden aus
`lower_binary` und `upper_binary` rekonstruiert. Dadurch sind Defekteintraege
und Zeilensummen exakte Darstellungen derselben outward-gerundeten binaeren
Intervallrechnung.

## 3. Unveraenderte wissenschaftliche Spezifikation

Attempt 2 verwendet weiterhin exakt

\[
F_s=F_{3600}+sT_{3600},\qquad s\in[0,1],
\]

den versiegelten G4-Mittelpunkt, $h_R=h_\theta=10^{-10}$, die Panels bei
120 und 160 Dezimalstellen sowie die Gates U0--U6 des Erstprotokolls. Es gibt
keine Slabs, Boxanpassung, zusaetzliche Praezision, Parametersuche oder
Schwellenverschiebung.

## 4. Attempt-2-Provenienz und Pfade

Attempt 1 bleibt ueber Governance-Revision, Receipt und Incidentreview
unveraendert erhalten. Attempt 2 erhaelt:

- ein v2-Ergebnisschema mit `attempt=2`;
- eine eigene geschlossene Attempt-2-Governance;
- ein eigenes exklusives Receipt;
- eigene Resultat-, Report-, Audit- und Manifestpfade mit Kennung
  `attempt_2_2026-09-30`;
- eine neue Implementierungsrevision, offizielle CI, Readinessreview und
  Einmalautorisierung.

Kein Attempt-2-Pfad darf einen Attempt-1- oder frueheren Record
ueberschreiben.

## 5. Falsifikationstests

Vor einer Autorisierung muessen mindestens folgende targetfreie Tests
bestehen:

1. exakte Konvertierung fuer positive und negative Exponenten, Vorzeichen,
   Null und Mantissen mit fuehrenden Dezimalnullen;
2. Zuruecklesen jedes kanonischen Texts als `Decimal` ergibt exakt den durch
   das Binaertupel bezeichneten rationalen Wert;
3. Booleans, falsche Tupellaenge, negatives $m$, ungueltiges $s$ oder $b$
   und uebergrosse Exponenten werden verworfen;
4. ein konstruiertes Rundungsgegenbeispiel, bei dem gerenderte Texte eine
   inward Zeilensumme erzeugen, besteht nach Rekonstruktion aus den exakten
   Binaerendpunkten;
5. eine wirklich inward manipulierte Zeilensumme wird weiterhin von
   Produktionsvalidator und unabhaengigem Auditor verworfen;
6. Attempt-1-Receipt sowie alle Attempt-2-Exklusivpfade werden fail-closed
   geprueft;
7. Schema, Attemptnummer, geschuetzte Blobs und Governance duerfen nicht
   driften.

## 6. Entscheidung und Claimgrenze

Entscheidungen und erlaubte Sprache bleiben unveraendert. Ein valider Pass
belegt nur die lokale, uniforme Rootast-Verbindung
$F_{3600}\to F_\infty$. Er belegt weiterhin keine dynamische Stabilitaet fuer
$H\to\infty$, globale Eindeutigkeit, Formation, Interaktion, Spin,
Traegheit oder physikalische Masse.

Dieses Amendment autorisiert selbst keinen Zielzugriff.
