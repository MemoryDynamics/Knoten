# Kritisches Review: G1--G3-Horizontbrueckenprotokoll

Datum: 2026-09-27.

Gepruefte Revision:
`7112f438abcad8dc9036590f29da6361378d5c9b`.

Gepruefter Protokollblob:
`c7feabc67011a702f94ed44f40b5e8d03f3178dd`.

Verdict:
**`g1-g3-bridge-protocol-major-amendment-required-target-closed`**.

Das Protokoll bewahrt die seit 2026-09-08 eingefrorenen Leiter-, Homotopie-
und Driftparameter und vermeidet einen wissenschaftlich unnoetigen Re-Run der
bereits versiegelten G4-/G5-Komponenten. Die Trennung ist sachlich sinnvoll.
Vor Ergebnisvertrag oder Runnercode muessen jedoch die folgenden Punkte
geschlossen werden. Dieses Review autorisiert keinen Zugriff auf einen
registrierten Leiterroot.

## HGB-P01 -- kritisch: Praezisionspanel-Identitaet ist noch nicht bewiesen

Abschnitt 3 uebernimmt die alte Bedingung, dass sich die 80-/120-dps-
Innenbilder schneiden. Zwei einschliessende Intervalle koennen sich schneiden,
obwohl jedes einen anderen Root an einem anderen Rand enthaelt. Der Schnitt
allein ist daher kein Identitaetsbeweis.

Die in Abschnitt 6 fuer die versiegelten Endpunkte eingefuehrte Idee ist
richtig und muss auch innerhalb jedes neuen Rootpanels gelten: Jedes innere
Krawczyk-Bild muss vollstaendig in der aeusseren Eindeutigkeitsbox des jeweils
anderen Praezisionspanels liegen. Erst diese Kreuzinklusion legt beide
eingeschlossenen Roots in die Eindeutigkeitsdomain des anderen Panels.

Der Ergebnisvertrag muss die vier relevanten Box-/Bildpaare speichern; Runner,
Validator und Auditor muessen Kreuzinklusion aus Dezimalendpunkten
rekonstruieren. Ein gespeichertes Boolfeld genuegt nicht.

## HGB-P02 -- hoch: versiegelte Evidenz darf nicht scheinbar neu auditiert werden

Abschnitt 2 fordert eine erneute Rekonstruktion der jeweiligen Schemata und
Entscheidungen, unterscheidet aber nicht sauber zwischen Inhaltsidentitaet und
neuer numerischer Reproduktion. Insbesondere ist der G5-Rohrecord
`same-platform-binary64-transcendentals`; sein vollstaendiger semantischer
Audit ist auf einer anderen Plattform bereits nachweislich um eine ULP
gescheitert.

Die Amendierung muss deshalb zwei Ebenen trennen:

1. plattformuebergreifend exakte Datei- und Manifesthashes sowie minimale
   strukturelle Rekonstruktion der gebundenen Parameter, Entscheidung und
   Rootzertifikate;
2. keine erneute Rekonstruktion von G5-Eigenwertbetraegen, Trajektorien oder
   Transzendentalwerten im Brueckenlauf.

Da der gesamte Komponentenrecord an einen vorab eingefrorenen SHA-256 gebunden
ist, ist die minimale strukturelle Extraktion kein Vertrauen in frei
mutierbare Boolfelder. Jede Aenderung auch eines unberuehrten Zahlenfelds
bricht zuerst den Dateihash.

## HGB-P03 -- hoch: Endpunktanschluss muss jedes neue Praezisionspanel binden

Abschnitt 6 spricht vom geschnittenen neuen Innenbild. Wie bei HGB-P01 kann
ein Schnitt die Lage beider einzelnen eingeschlossenen Roots verdecken. Fuer
$H=2400$ und $H=3600$ muss daher gelten:

- die inneren Bilder beider neuen Praezisionspanels liegen jeweils in der
  aeusseren Komponentenbox;
- das innere Komponentenbild liegt jeweils in beiden neuen aeusseren Boxen.

Diese vier Kreuzinklusionen pro Endpunkt verwenden keine neue Toleranz. Sie
sind eine reine Ordnungspruefung outward-gerundeter Dezimalintervalle.

## HGB-P04 -- mittel: G6 ist nicht vollstaendig eingefroren

Die Aussage „fuer alle sieben Horizonte“ laesst die zwei nichtkreisfoermigen
Kontrollhorizonte und die exakten Fehlergrenzen des Ursprungsprotokolls aus.
Die Amendierung muss unveraendert festhalten:

- Shift/Circular fuer deterministische Nichtkreisgeschichten bei $H=17,257$;
- Shift/Circular fuer Kreisgeschichten bei allen sieben Leiterhorizonten;
- relativer Ein-Schritt-Fehler kleiner $5\times10^{-14}$;
- $\eta=0$ fuer jeweils $H+1$ Schritte und maximale Abweichung kleiner
  $10^{-14}$.

Ohne diese Details waere ein spaeterer Runner frei, eine schwaechere G6-
Kontrolle zu implementieren.

## HGB-P05 -- mittel: Artefaktzahl und Laufzeitvertrauen sind unscharf

Abschnitt 8 spricht von vier gebundenen G4-/G5-Inhaltshashes, waehrend
Abschnitt 2 bereits fuenf Artefakte bindet. Zudem ist nur fuer G4 ein
persistierter Auditoutput vorhanden; der G5-Audit ist durch Ergebnisreview,
Pre-Merge-Review und CI dokumentiert, aber nicht als eigener JSON-Output
publiziert.

Die Amendierung muss die fuenf Laufzeitinputs exakt benennen und darf keinen
nicht vorhandenen G5-Auditoutput suggerieren. Reviews koennen als
Governance-Provenienz gebunden werden, sind aber keine vom Runner zu
interpretierenden wissenschaftlichen Daten.

## HGB-P06 -- niedrig: lower-tail-Ausgang ueberdehnt den Ausschlussadapter

Der vorhandene lokale Ausschlussadapter ist nur fuer die vier
Vorwaertskanten registriert. Abschnitt 7 darf deshalb fuer den tieferen
Stressast keinen `registered-local-loss` versprechen. Zulaessig sind dort nur
`pass` oder `inconclusive`, solange kein separates prospektives
Lower-tail-Ausschlussprotokoll existiert.

## Positiver Kern und naechste Grenze

Unveraendert tragfaehig sind:

- feste Parameter, Leiter und Newtonstarts;
- 64 nichtadaptive Homotopiescheiben;
- outward-rounded Drift und alte Schwellen;
- der ausschliesslich nach Vorwaertsfehlern geoeffnete lokale Falsifikator;
- die hashgebundene Wiederverwendung versiegelter G4-/G5-Artefakte;
- die enge Claimgrenze ohne $H\to\infty$-Stabilitaet oder Physikclaim.

Nach Schliessung von HGB-P01--P06 ist nur ein Suffizienzreview der
Protokollamendierung zulaessig. Ergebnisvertrag, Tests und Runner bleiben bis
dahin geschlossen; der neue G1--G3-Targetzugriff bleibt in jedem Fall einer
spaeteren ausdruecklichen Freigabe vorbehalten.
