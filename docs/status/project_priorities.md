# Projektprioritaeten

Stand: 2026-10-23 (Fehlerbudget und ausloeschungsarme Restdarstellung; Langlauf-/Kostenentscheidung offen; keine neue Panel-/FIFO-/P5-Autorisierung).

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

1. **Architekturentscheidung aus R0/B1 treffen -- Vorlage liegt vor.** Der begrenzte
   [R0-Audit](../reference/foundation_feasibility.md) und die
   [B1-Bestandsanalyse](../reference/operational_contract.md) liegen vor:
   Die klassische Quellenantwort ist spezifiziert; ein gemeinsames
   physikalisches Mehrsystem-/Messgesetz ist aus Paper I nicht bestimmt.
   Direkter Fernzugriff und unabhaengiges Rauschen ergeben nicht automatisch
   Bell-Lokalitaet oder eine Quantentheorie. Die
   [Entscheidungsvorlage](architecture_decision.md) vergleicht die
   unveraenderte Regel, eine explizite klassische Erweiterung und eine
   vorausgesetzte Quantenstruktur samt ersten Gegenpruefungen. Empfehlung
   ist vorerst die unveraenderte Regel, ohne Erfolgsaussicht zu behaupten.
   Keine neue Mediatorgleichung oder Quantenmessregel einsetzen, um eine
   Luecke zu verdecken. Dies bleibt analytische Bestandsarbeit ohne
   Ziellaeufe; neue Modellregeln erfordern eine Richtungsentscheidung des
   Autors. Paper I kann als eigenstaendiger Publikationsstrang parallel
   weiterbearbeitet werden.
2. **Paper I als begrenzten Ausgangspunkt abschliessen -- R0-Einordnung liegt vor.**
   Die reproduzierbare Fassung vom 2026-10-09 bleibt eingefrorene Baseline,
   ist aber nicht als PRE-einreichungsreif eingestuft. Zuerst die konkrete
   Neuheit gegen Aging-Diffusionen, Autochemotaxis, exponentiell gewichtete
   Occupation-Masse sowie Sarkars PRE-"Memory engine" und Gaussian-Delay-
   Feedback pruefen; der reine Befund kompakter relativer Radien bei
   fortbestehender Diffusion ist kein ausreichender Neuheitsanspruch.
   Die bereits formale erste nichtlineare Korrektur als eigene
   Publikationshypothese samt Gueltigkeitsgrenze weiter pruefen; sie ist
   kein nachgewiesener Schritt zu Gravitation oder Standardmodell.
   Eine [neue analytische Notiz](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/paper/paper_i/research/finite_memory_stationarity_2026-10-21.md)
   begruendet stationaere relative Existenz fuer festes endliches $H$ und
   positives Rauschen. Ein exaktes Koexistenzbeispiel zeigt zugleich, dass
   lokale lineare Stabilitaet die globale Schwachrauschverteilung nicht
   festlegt. Die anschliessende
   [Kontraktionsnotiz](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/paper/paper_i/research/weak_noise_validity_2026-10-21.md)
   begruendet stationaere Momentkorrekturen unter einer strengeren globalen
   Bedingung, auch ohne Horizontkuerzung. Keine aktive archivierte Zelle
   erfuellt diese hinreichende Schranke. Eine ergaenzende positive
   Mittelungsdarstellung in der Stationaritaetsnotiz umfasst hingegen die
   archivierten Modellkoeffizienten fuer die Momententwicklung bei festem
   endlichem $H$. Ihre enormen Konstanten validieren weder das vorhandene
   endliche Rauschen noch den Transport. Der
   [Gegencheck des externen Reviews](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/paper/paper_i/research/external_review_audit_2026-10-22.md)
   reproduziert die Koeffizienten, findet aber im vorgeschlagenen
   Block-MSD-Panel eine Verwechslung von endlichem Lag und Langzeittransport.
   Die anschliessende
   [gepaarte Machbarkeitsrechnung](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/paper/paper_i/research/paired_transport_feasibility_2026-10-22.md)
   spezifiziert einen Zweilaengen-Schaetzer mit kontrolliertem
   Koeffizientenbias und berechnet die Langblock-Varianz einschliesslich
   des dritten Gauss-Chaos. Eine anschliessende
   [finite-Stichproben-Schranke](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/paper/paper_i/research/finite_block_transport_bound_2026-10-22.md)
   kontrolliert den fuehrenden Koeffizienten bei endlicher Blocklaenge,
   einschliesslich Block- und Koordinatenabhaengigkeit. Das neue
   [Gesamtfehlerbudget](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/paper/paper_i/research/finite_noise_transport_budget_2026-10-23.md)
   ergaenzt den zufaelligen nichtlinearen Schaetzerrest, den Transportrest
   und eine vollstaendig vorgefuellte flache Anfangshistorie. Fuer eine
   illustrative 10%-Grenze ergibt sich ein hinreichender Rauschbereich
   bis etwa $4.46\,10^{-6}$; dort ist der Kontrast nur etwa $9.54\,10^{-10}$
   des linearen Hintergrunds. Die anschliessende
   [exakte Restdarstellung](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/paper/paper_i/research/paired_residual_precision_2026-10-23.md)
   besteht kleine deterministische Historien- und H=600-Ein-Schritt-
   Gegenchecks gegen 80-/110-stellige Vollkraftrechnungen. Damit ist die
   kleine Differenz nicht schon ein numerisches Ausschlussargument. Der unoptimierte
   Referenzcode ergab jedoch etwa 0.261 ms pro Paarupdate, naiv seriell
   rund 145 Stunden fuer die diskutierte Paarzahl ohne RNG/Statistik/I/O.
   Das ist keine Laufzeitgarantie. Jetzt Akkumulation und Summation
   begrenzt pruefen und mit Kosten sowie Neuheitswert ueber einen
   vertretbaren Test entscheiden, nicht automatisch einen grossen Runner
   optimieren oder starten. Keine
   nachtraegliche Subtraktion grosser unabhaengig gerundeter Trajektorien
   als validierte Methode behandeln. Der vorgefuellte Start ist im
   Methodenprototyp abgebildet, nicht im Produktionsrunner; dessen leerer Start ist nicht
   abgedeckt. Das Budget ist kein Intervallzertifikat, Fachreview oder
   Neuheitsbeweis. Erst mit diesen Pruefungen und dem Literaturabgleich
   eine praktische Machbarkeitsentscheidung treffen.
   Die vorgeschlagenen acht Milliarden Updates sind nicht freigegeben.
   Der hergeleitete
   summierbare Rest begruendet nur im strengeren Kontraktionsbereich den
   Transport-Grenztausch und einen expliziten ungekuerzten Koeffizienten.
   Kopplungsperturbation
   nach Newman--Grima und die Small-delay-Approximation nach Kopp--Klapp
   als konkrete Vergleichsgrenzen fuehren; andere Grenzwerte allein sind
   kein Neuheitsbeweis. Vor jedem Panel globale stationaere
   Aussage und lokale bzw. endlichzeitige Branch-Aussage unterscheiden.
   Erst nach wissenschaftlicher Auswahl im Licht von R0/B1 ein
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

Die Vorlage fuer den fundamentalen Pfad ist zur Autorenentscheidung bereit.
Sie ersetzt weder eine Modellwahl noch deren spaetere wissenschaftliche
Pruefung. Waehrend diese offen ist, kann die Paper-I-Neuheits- und
Gueltigkeitspruefung weitergehen: Den nun hinreichend kontrollierten
Moment-/Transportbereich gegen die Literatur bewerten und entscheiden, ob
die wissenschaftliche Frage damit beantwortbar ist. Die neue
Mittelungsdarstellung schliesst die asymptotische Momentluecke bei den
archivierten Modellkoeffizienten und festem $H$, nicht die praktische
Fehlertoleranz oder den Transport dort. Das externe Modellreview ist
ausgewertet; seine Nachweisstaerke ist fuer den vorgeschlagenen Schaetzer
nicht bestaetigt. Ein passender Zweilaengen-Schaetzer und die gepaarte
Langblock-Kovarianz sind analytisch bestimmt; fuer den fuehrenden
Koeffizienten liegt nun auch eine konservative endliche Stichprobengrenze
vor. Das explizite Gesamtfehlerbudget schliesst die analytische Uebertragung
auf endliches Rauschen bei festem $H$ und vollstaendig vorgefuelltem Start,
nicht die Maschinenarithmetik. Die exakte ausloeschungsarme Darstellung
besteht begrenzte Hochpraezisionschecks; der Referenzcode ist fuer die
diskutierte Paarzahl teuer. Als naechstes die verbleibende
Akkumulations-/Summationskontrolle und den wissenschaftlichen Nutzen in
eine begrenzte Machbarkeitsentscheidung ueberfuehren, bevor weitere
Implementierungsarbeit oder eine Rauschwahl festgelegt wird. Der Volltextabgleich
der Aging-Arbeit und ein unabhaengiges Fachreview bleiben ebenfalls offen.
Ein Datenpanel wird dadurch nicht automatisch
festgelegt. Keine neue FIFO-/P5-Zielautorisierung.

## Aktueller Haltepunkt

R0 und B1 sind als begrenzte Bestandspruefungen abgeschlossen, nicht als
allgemeines Machbarkeitsurteil. Die bisherige Einzelprozessregel definiert
keine zwei unabhaengig einstellbaren Messstationen; konstruierte
Kopplungsports sind Erweiterungen. B1 liefert fuer den Frozen-Source-Zweig
die bedingte Uebergangsverteilung und Ein-Schritt-Antwort; fuenf zusaetzliche
synthetische Checks sichern die Zuordnung zum vorhandenen Runner. Daraus
folgt weder eine autonome Mehrsystemtheorie noch eine physikalische
Ueberlichtkommunikation. Paper-II-Alttext und Paper-III-Planung muessen an
diese Grenze angepasst gelesen werden; ihre READMEs markieren den offenen
Anschluss.

Paper I ist als Baseline redaktionell und reproduktionstechnisch geschlossen,
aber die wissenschaftliche PRE-Reife ist offen. Der Neuheitsaudit identifiziert
bereits bestehende Transport-/Memory-Architekturen; die volle Aging-Arbeit ist
noch nicht im Gleichungsdetail abgeglichen. Die neue nichtlineare Rechnung
ist keine gemessene Evidenz. Stationaere
relative Existenz ist nun fuer festes endliches $H$ und positives Rauschen
analytisch begruendet. Positive Mittelung rechtfertigt zusaetzlich die
stationaere Momententwicklung bei den archivierten Modellkoeffizienten,
aber nur asymptotisch bei festem $H$ und ohne brauchbare Fehlerkonstanten.
Eine separate globale Kontraktionsbedingung
kontrolliert die Momententwicklung und den Horizontfehler in einem engeren
Bereich, der keine aktive archivierte Zelle umfasst. Ein summierbarer
Kopplungsrest schliesst dort auch den nichtlinearen Transport-Grenztausch,
nicht jedoch die allgemeine Gueltigkeitsluecke oder den Neuheitsvergleich.
Neue Zielsimulationen sind in diesem Arbeitsblock nicht gelaufen.
Der externe Panelvorschlag hat noch keinen Readiness-Status: Am festen
Review-Punkt ergibt die lineare Referenz einen Block-MSD-Bias von 37.17%
und die korrigierte unabhaengige Groessenabschaetzung etwa 2.32 statt
13.5 Standardabweichungen. Das ist kein Unmoeglichkeitsbeweis fuer gepaarte
Tests und kein neuer Datenbefund.

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
