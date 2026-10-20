# Projektprioritaeten

Stand: 2026-10-21 (Gesamtprogramm vor Publikationsoptimierung; keine neue FIFO-/P5-Autorisierung).

Dies ist die einzige aktive Arbeitsreihenfolge des Repositorys. Der
[Stand bis 2026-09-09](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/docs/archive/status/project_priorities_through_2026-09-09.md)
ist archiviert. Katalog, Status und Reports duerfen Befunde und Blocker
nennen, aber keine zweite Prioritaetenliste fuehren. Die
[Forschungsroadmap](research_roadmap.md) beschreibt Ziel und Abhaengigkeiten,
keine zweite Aufgabenliste. Der [Stand vom 2026-10-19](https://github.com/MemoryDynamics/Knoten/blob/b43fc11af4dcda82058a64e0d2e0e013c9aba585/docs/status/project_priorities.md)
bewahrt die vorherige Arbeitsreihenfolge.

Eingefrorene Voraussetzungen bleiben
`p4rs-anchor-scale-transfer-pass`,
`n0-noise-stability-window-bracketed-reviewed-pass` und
`p5d-mutual-center-design-identifiable`.
**P5-D Versuch 3 technisch inconclusive: Pipeline geschlossen**; die
**Attempt-3-Lease ist verbraucht**.
Diese Befunde ordnen Prioritaet 3 ein, sind aber keine weiteren Arbeitspunkte.

## Eine Liste

1. **Gemeinsamen Machbarkeitscheck erstellen -- jetzt.** Fuer die unveraenderte
   Mikrodynamik eine kompakte Matrix aus Input, abgeleitetem Resultat, offener
   Annahme und moeglichem Gegenbefund erstellen. Drei Fragen bearbeiten:
   Welche effektiven Freiheitsgrade bleiben nach Symmetriereduktion? Welche
   Lokalitaets-/Propagationsstruktur erlaubt das Modell? Welche Voraussetzungen
   einer Quantenbeschreibung sind vorhanden oder fehlen? Die Quantenfrage
   wird parallel zur klassischen Modenanalyse geprueft, nicht erst nach
   erfolgreichen Mehrknotentests. Ergebnis: eine begruendete Auswahl genau
   eines naechsten Brueckennachweises oder ein dokumentierter Blocker.
   Zunaechst Literatur-, Gleichungs- und Bestandsanalyse, keine neuen Ziellaeufe.
   Erweiterungen getrennt kennzeichnen; neue Modellregeln und groessere
   Simulationsprogramme brauchen eine Richtungsentscheidung des Autors.
2. **Paper I als begrenzten Ausgangspunkt abschliessen -- nach Einordnung aus 1.**
   Die reproduzierbare Fassung vom 2026-10-09 bleibt eingefrorene Baseline,
   ist aber nicht als PRE-einreichungsreif eingestuft. Zuerst die konkrete
   Neuheit gegen Aging-Diffusionen, Autochemotaxis, exponentiell gewichtete
   Occupation-Masse sowie Sarkars PRE-"Memory engine" und Gaussian-Delay-
   Feedback pruefen; der reine Befund kompakter relativer Radien bei
   fortbestehender Diffusion ist kein ausreichender Neuheitsanspruch.
   Die bereits formale erste nichtlineare Korrektur als eigene
   Publikationshypothese samt Gueltigkeitsgrenze weiter pruefen; sie ist
   kein nachgewiesener Schritt zu Gravitation oder Standardmodell.
   Erst nach Punkt 1 und begruendeter wissenschaftlicher Auswahl ein
   prospektives, begrenztes Transport-/Skalenpanel
   mit gematchten Kerneln, Autokorrelation, Seed-Unsicherheit und explizitem
   Falsifikationskriterium einfrieren. Kein weiterer 30M/300M-Radiuslauf nur
   zur Praezisionssteigerung. Bei fehlender neuer Aussage Baseline als
   technischen Anker behalten; Manuskriptziel und Journal dann neu entscheiden.
   Der [PRE-Neuheitsaudit](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/paper/paper_i/research/pre_reassessment_2026-10-19.md)
   dokumentiert Evidenz, offene Literaturfragen und die bedingte Arbeitshypothese.
3. **Fixed-alpha-Horizontgate vervollstaendigen -- nach Einordnung aus 1.**
   Im separaten FIFO-Arm bestehen G4 fuer lokale $F_\infty$-Existenz und
   G5 fuer lokale numerische Stabilitaet bei exakt $H=2400$. Offen bleiben
   die G1--G3-Branchverbindung und der vollstaendige Horizonttransfer;
   insbesondere ist Stabilitaet bei unendlichem Horizont nicht belegt.
   Vor neuer Ausfuehrung die damit entscheidbare Aussage festhalten.
   G5-Ausfuehrungsautorisierung verbraucht; P5-D bleibt nach Versuch 3
   geschlossen. Technische Versuchschronik im oben verlinkten Stand vom
   2026-10-19, aktuelle Evidenz im Experimentkatalog.
4. **FIFO-Paper eigenstaendig bearbeiten -- getrennt von 2, nach 3.** Existenz und
   lokale Stabilitaet vorbereiteter Orbits mit der jeweils geprueften
   Vertrauensbasis berichten. Paper I benoetigt keinen Formationsclaim.
   Ein Formation-/KnotScore-Protokoll bleibt ein separates prospektives
   Projektgate. Ein Score auf einer vorbereiteten exakten Kreisgeschichte
   ohne `eta_zero`- und Formationskontrolle wird nicht nachgetragen.
5. **Zertifikats- und Release-Hardening -- nach 3, parallel zu 2/4.** Einen
   zweiten unabhaengigen Intervallbackend, reproduzierbare Dependency-Hashes,
   `CITATION.cff` und eine zitierbare Release vorbereiten. Diese Punkte
   erhoehen Pruefbarkeit, ersetzen aber kein wissenschaftliches Gate.
6. **Interaktionsprogramm nur bei begruendetem Brueckenziel neu autorisieren -- nach 1 und 3.** P5-D bleibt
   `inconclusive`. Ein weiterer Ziellauf braucht ein separates
   outcome-blindes Protokoll, eine neue explizite Freigabe und einen sauberen
   Readiness-Commit. Vorher ist nur targetfreie Methodenarbeit erlaubt.
   Das Ziel muss aus dem Machbarkeitscheck folgen: Observable, Nullmodell,
   Gueltigkeitsbereich und Abbruchkriterium vorab festlegen, ohne ein
   gewuenschtes Feldgesetz oder Teilchenlabel als Ergebnis einzubauen.
7. **Repository und Roadmap fortlaufend kuratieren -- bei jedem abgeschlossenen Block.**
   Aktive Seiten auf hoechstens sieben gleichrangige Elemente begrenzen,
   historische Detailregister ins Archiv verschieben, Standardbibliotheken
   erweitern statt Runnerlogik zu duplizieren und Status/Claims nach jedem
   Review synchronisieren. Nur neue Evidenz oder eine explizite
   Richtungsentscheidung aendert den Status einer Bruecke. Technische
   Reparaturen zaehlen nicht als neue Physikevidenz.

## Naechstes abnehmbares Ergebnis

Ein kurzer Machbarkeitsbericht mit einer Annahmen-/Resultatmatrix fuer das
Minimalmodell und getrennt gekennzeichneten Erweiterungen. Er muss fuer jede
der drei Fragen aus Punkt 1 mindestens einen entscheidenden Nachweis oder
ein begruendetes Hindernis benennen. Am Ende steht eine Empfehlung mit
Alternativen und Entscheidungskriterium, kein automatisch gestarteter Scan.
Das ist eine endliche Bestandspruefung, kein Auftrag, bereits Quantenmechanik
oder Gravitation herzuleiten. Diese Planungsanpassung erteilt keine neue
FIFO-/P5-Zielautorisierung.

## Aktueller Haltepunkt

Paper I ist als Baseline redaktionell und reproduktionstechnisch geschlossen,
aber die wissenschaftliche PRE-Reife ist offen. Der Neuheitsaudit identifiziert
bereits bestehende Transport-/Memory-Architekturen; die volle Aging-Arbeit ist
noch nicht im Gleichungsdetail abgeglichen. Die neue nichtlineare Rechnung
ist eine formale lokale Vorhersage, keine gemessene Evidenz und kein Beweis
einer stationaeren nichtlinearen Verteilung. Neue Zielsimulationen sind in
diesem Arbeitsblock nicht gelaufen.

### Separater FIFO-Haltepunkt

Der isolierte G4-Komponentenblock ist mit unabhaengig auditiertem lokalem
Pass abgeschlossen; G5-Adapter und Grundgleichungs-Preflight sind targetfrei
reviewed. Ergebnisvertrag, Backendkomposition, persistierter Preflight und
unabhaengiger Auditor sowie der Execution-Context-Guard sind targetfrei
implementiert und reviewed. G5-Attempts 1 und 2 sind als getrennte
Pipeline-Incidents ohne Ergebnis verbraucht. Attempt 2 falsifizierte die
Trajektorien-Vertragsabdeckung; Attempt 3 schliesst sie mit auditierter
dichter Spur und endet als `g5-local-direct-stability-pass`. Die einmalige
Autorisierung ist verbraucht. Als naechste Horizontluecke bleibt die
G1--G3-Verbindung zwischen den isolierten G4- und G5-Befunden. Der aktuelle
methodische Stand und die Evidenzgrenzen stehen im
[Experimentkatalog](../reference/experiment_catalog.md).
