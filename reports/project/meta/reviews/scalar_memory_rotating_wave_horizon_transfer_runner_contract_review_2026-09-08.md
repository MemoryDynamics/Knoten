# Negativreview: Runner-Vollstaendigkeit des Horizonttransfer-Vertrags

Datum: 2026-09-08.

Gepruefte Revision:
`6e86f06ee91f490552d3330478f39e9af37805b3`.

Verdict:
**`rotating-wave-horizon-transfer-runner-contract-fail-null-semantics-amendment-required`**.

Der targetfreie Infrastrukturstand ist intern getestet, kann aber die im
Protokoll ausdruecklich vorgesehenen fruehen Abbrueche und partiellen
numerischen Ausgaben nicht wahrheitsgetreu serialisieren. Der
wissenschaftliche Runner darf deshalb noch nicht implementiert oder
ausgefuehrt werden. Horizontlauf und P5-D bleiben geschlossen.

## 1. Methode

Der Ergebnisvertrag wurde nicht nur gegen einen vollstaendigen Pass-Witness,
sondern gegen jeden im Protokoll geforderten fail-closed Pfad gelesen. Dabei
wurde fuer jeden Pfad gefragt, ob der Runner nach dem vorgeschriebenen Stopp
einen schema-gueltigen Record erzeugen kann, ohne nicht berechnete Werte zu
erfinden, alte Werte als neue Evidenz auszugeben oder verbotenerweise nach
dem Stopp weiterzurechnen.

Es wurden keine registrierten Roots, Homotopien, Arnoldi-Panels,
Trajektorien oder Ergebnispfade ausgewertet.

## 2. Blockierende Befunde

### HT-RC01: Rootleiter kann einen fruehen Stopp nicht abbilden

`root_panels` verlangt exakt sieben nicht-null Panels. Scheitert ein
Vorwaerts- oder Rueckwaertsschritt, existieren fuer die davon abhaengigen
Horizonte keine erlaubten Newtonstarts und somit keine ehrlichen Panels.
Der Vertrag zwingt dennoch zur Erfindung vollstaendiger Root-, Jacobian- und
Zertifikatswerte.

### HT-RC02: Homotopie-Stopp widerspricht fester Vollbelegung

Jede der sechs Homotopien verlangt exakt 64 nicht-null Scheiben. Das
Protokoll verbietet jedoch das Ueberspringen eines fehlgeschlagenen
Abschnitts. Nach dem ersten Krawczyk-Fehler sind spaetere Scheiben keine
zulaessige Fortsetzungsevidenz. Der aktuelle Vertrag besitzt fuer diese
Slots keine `null`-Semantik.

### HT-RC03: Partielle Arnoldi-Ausgabe ist strukturell unmoeglich

Die Statuswerte `arpack-no-convergence`, `wrong-cardinality`,
`missing-vectors`, `nonfinite` und `residual-fail` sind registriert. Beide
Panels verlangen trotzdem exakt 24 beziehungsweise 36 vollstaendige
Eigenpaare mit jeweils 4800 komplexen Vektorkomponenten. Damit kann eine
partielle ARPACK-Ausgabe nicht gespeichert werden, obwohl das Protokoll
gerade deren fail-closed Erhalt fordert.

### HT-RC04: Trajektorienstopp ist strukturell unmoeglich

Jeder der drei Stoerungsarme und der exakte Arm verlangt exakt 501
Messpunkte. Bei einem nichtendlichen Abstand oder einem registrierten
Stoppradius endet die Rechnung vorher. `stopped=true` ist zwar vorhanden,
aber die fehlenden spaeteren Samples duerfen weder erfunden noch durch den
letzten Wert aufgefuellt werden.

### HT-RC05: Abhaengige Drift- und Tailstufen besitzen keinen Nullpfad

Ohne die erforderlichen Rootintervalle koennen die zwei Driftzeilen nicht
berechnet werden. Ohne den H=3600-Root koennen die beiden
Tail-Krawczyk-Panels nicht berechnet werden. Der Vertrag verlangt alle diese
Objekte dennoch nicht-null.

## 3. Erforderliche prospektive Remediation

Der mathematische Inhalt und die Entscheidungsrangfolge bleiben
unveraendert. Vor Runnercode ist eine rein strukturelle Amendierung
erforderlich:

1. feste, positionsgebundene Arrays bleiben erhalten, ihre noch nicht
   ausgewerteten Eintraege werden jedoch explizit `null`;
2. Rootpanels, Homotopien, Homotopiescheiben, Driftzeilen,
   Tail-Zertifikatpanels und Trajektorienarme erhalten diese
   Abbruchsemantik;
3. Arnoldi-Panels behalten ihre feste Slotzahl, erlauben aber `null` fuer
   nicht zurueckgegebene Eigenpaare und `null` fuer einen fehlenden Vektor;
4. Trajektoriensamples behalten 501 feste Slots; nach einem ehrlichen Stopp
   sind alle spaeteren Slots `null` und duerfen nicht wieder nicht-null
   werden;
5. Validator und unabhaengiger Auditor muessen Nullmuster, Statuskonsistenz,
   praefixfoermige Auswertung und Gatefolge rekonstruieren;
6. Mutationstests muessen erfundene Werte nach einem Stopp, innere
   Null-Locher und eine `complete`-Kennzeichnung bei unvollstaendigen Slots
   ablehnen.

Ein Pass-Witness allein reicht danach nicht. Mindestens Branchabbruch,
Homotopieabbruch, partielles Arnoldi und frueher Trajektorienstopp muessen als
vollstaendige schema-gueltige Negativ-Witnesses getestet werden.

## 4. Claimgrenze

Dieser Befund widerruft nicht die bereits getesteten Formeln, q- und
Taildarstellungen, FIFO-Kontrollen oder Entscheidungsrangfolge. Er zeigt
enger, dass der gegenwaertige Publikationsvertrag nur den Idealfall, nicht
aber das registrierte Experiment als Ganzes abbildet.

Bis zu einer separat committed, getesteten und reviewten Amendierung gilt:
**kein wissenschaftlich ausfuehrbarer Runner, kein Readiness-Pass, kein
Horizontlauf und keine Oeffnung von P5-D**.
