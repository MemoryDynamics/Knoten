# Projektprioritaeten

Stand: 2026-10-27 (H=1200-Kreis normal linear instabil; Strukturpruefung trennt nun Bahn, Memory-Form und Raumdimension, keine weitere Ausfuehrungsfreigabe).

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

1. **Bestehende Regel ausschoepfen: FIFO-Strukturkandidat pruefen.** Auf
   Autorenwunsch steht die geeignete Struktur vor einer Feld- oder
   Teilcheninterpretation. Die
   [analytische Strukturauswahl](../reference/fifo_structure_candidate.md)
   identifiziert eine altersmarkierte Schleife mit abgeleitetem Rahmen,
   keinen bereits geschuetzten Knotentyp. In gewaehltem 3D sind die beiden
   ebenen Drehsinne durch Raumrotation verbunden. Die bedingte
   $SO(3)$-Wegtopologie endet an erlaubten Rahmenentartungen und traegt
   nicht bei frei zugaenglichem $d\geq4$. Der
   [Normalstabilitaets-Methodenvertrag](../reference/fifo_normal_stability_contract.md)
   trennt nun exakt drei Symmetriemoden und prueft den Formquotienten mit
   einer bekannten Schur-Rekursion; der Intervallprototyp besteht kleine
   synthetische Gegenchecks. Die Rootbox-Abbildung ist jetzt mit frischer
   Krawczyk-Pruefung und direkten binaeren Intervallen implementiert und
   an konstruierten stabilen/instabilen Normalfaellen geprueft. Der
   [begrenzte H=1200-Ankertest](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/project/meta/preregistration/fifo_normal_stability_anchor_proposal_2026-10-25.md)
   ist nach konkreter Autorenfreigabe samt schraegen Stoerungen einmalig
   ausgefuehrt und geschlossen. Der
   [Ergebnisbericht](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/dynamics/rotation/fifo_normal_anchor_attempt_1_2026-10-25/analysis.md)
   dokumentiert: Beide Rootzertifikate bestehen; beide Normaltests bleiben
   durch Intervallaufweitung unentschieden. Im festen 2000-Update-Fenster
   klingt die getestete planare Formstoerung ab, alle getesteten 30/45/60/90-
   Grad-Arme wachsen stark. Die anschliessend separat freigegebene
   [Archivauswertung](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/dynamics/rotation/fifo_archived_normal_slope_2026-10-26/report.md)
   schliesst die Modenfrage am Anker: Beide exakten 80-/120-dps-Intervalle
   fuer $S=1+\sum_{j=1}^{H-1}j c_j$ sind strikt negativ
   (etwa $-0.3276456990$). Damit ist eine reelle wachsende Normalformmode
   belegt, unter der Vertrauensbasis der archivierten Einschliessungen.
   **Dieser Kreis ist kein linear stabiler 3D-Baustein.** Keine weitere
   Ausfuehrung ist freigegeben. Die anschliessende
   [analytische Strukturpruefung](../reference/fifo_rigid_structure_limits.md)
   grenzt den starren 3D-Ast nun auf Punkt, Gerade, Kreis und Helix ein.
   Die Helix verlangt drei gleichzeitige Balancen; eine beliebig nahe
   Helixfortsetzung am aktuellen Kreis ist wegen $S\ne0$ ausgeschlossen.
   Ihre moegliche geometrische Haendigkeit waere keine geschuetzte Ladung.
   Die Rueckfrage des Autors erweitert die Strukturauswahl ausdruecklich:
   Bahn, Memory-/Feldform und Umgebungsdimension trennen; Kugel-/Torus-
   Verteilungen und mehrere Rotationsebenen nicht durch den starren
   3D-Ansatz ausschliessen. Naechster Schritt ist eine gemeinsame
   Zustands-/Formdefinition mit festen Kriterien fuer Lokalisation,
   Dimensionalitaet und Robustheit, bevor ein bestimmter Ast bevorzugt
   oder numerisch gesucht wird. Keine lokale Rettung des Kreises,
   Parametersuche oder neue Ziellaeufe. Ein nichttrivialer geschlossener
   Bahnknoten wuerde in 3D nichtstarre Dynamik benoetigen.
   Andere FIFO-Strukturen sind durch den Einzelbefund nicht
   ausgeschlossen. Der Autor hat zuvor separat die
   [120-Grad-Symmetriekontrolle](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/project/meta/preregistration/fifo_oblique_120_control_2026-10-25.md)
   angefordert. Diese Kontrolle ist inzwischen
   [bestanden](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/dynamics/rotation/fifo_oblique_120_control_2026-10-25/report.md):
   Beide 120-Grad-Arme stimmen mit den gespeicherten 60-Grad-Armen bei
   entgegengesetztem Vorzeichen an allen 201 Abtastpunkten auf Rundungsniveau
   ueberein. Kein neuer Normalzertifikatslauf, keine Verallgemeinerung des
   explorativen Wachstumsbefunds. Der spaetere Vorzeichenbeleg oben ist
   eine eigene Aussage, kein Ergebnis dieser Winkelkontrolle.
   Der bisherige 2D-G5-Pass deckt diese Normalmoden nicht ab; seine
   Ausfuehrungsfreigabe wird nicht wiederverwendet. Der begrenzte
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
   Luecke zu verdecken. Nach der abgeschlossenen 120-Grad-Kontrolle
   bleibt dies Bestandsarbeit ohne weitere Ziellaeufe; neue Modellregeln erfordern eine Richtungsentscheidung des
   Autors. Paper I kann als eigenstaendiger Publikationsstrang parallel
   weiterbearbeitet werden.
2. **Paper I als begrenzten Ausgangspunkt abschliessen -- R0-Einordnung liegt vor.**
   Die reproduzierbare Fassung vom 2026-10-09 bleibt eingefrorene Baseline,
   ist aber nicht als PRE-einreichungsreif eingestuft. Zuerst die konkrete
   Neuheit gegen Aging-Diffusionen, Autochemotaxis, exponentiell gewichtete
   Occupation-Masse sowie Sarkars PRE-"Memory engine" und Gaussian-Delay-
   Feedback pruefen; der reine Befund kompakter relativer Radien bei
   fortbestehender Diffusion ist kein ausreichender Neuheitsanspruch.
   Der nun abgeschlossene
   [Aging-Volltextabgleich](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/paper/paper_i/research/aging_full_text_comparison_2026-10-25.md)
   liefert die exakte lineare Euler-Zuordnung samt Startkonventionen und
   skaliertem kontinuierlichem Transportgrenzwert. Die Quelle behandelt
   keine nichtlineare Schwachrauschentwicklung; daraus folgt keine
   Neuheitsbestaetigung. Die konkrete Gueltigkeitsleistung gegen rigorose
   Linearisierungs-/Antworttheorie und durch ein Fachreview bewerten.
   Die bereits formale erste nichtlineare Korrektur als eigene
   Publikationshypothese samt Gueltigkeitsgrenze weiter pruefen; sie ist
   kein nachgewiesener Schritt zu Gravitation oder Standardmodell.
   Der [Gaussprojektions-Audit vom 2026-10-24](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/paper/paper_i/research/gaussian_projection_audit_2026-10-24.md)
   reproduziert den gesamten ersten Transportkoeffizienten mit bekannter
   statistischer Linearisierung. Ein Mittelwerttest von $D_4$ unterscheidet
   diese Erklaerungen daher nicht. Jetzt den kontrollierten Gueltigkeits-
   und Grenzwertbeitrag fachlich bewerten. Der
   [begrenzte Satzvergleich](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/paper/paper_i/research/linear_response_scope_audit_2026-10-24.md)
   ist um einen direkten konkreten Poissonbeweis ergaenzt: Die
   Totalvariationsroute scheitert am vollen Historienzustand, aber die
   benoetigten Observablen, Korrelationen und der Rest lassen sich mit
   bekannten Antwortmethoden intern kontrollieren. Die Frage ist jetzt
   der wissenschaftliche Wert dieses kontrollierten Modellbeispiels,
   nicht eine neue allgemeine Methode. Kein Neuheitsbeweis oder Fachreview.
   Nicht automatisch auf $D_6$ ausweichen oder den Test vergroessern.
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
   Das ist keine Laufzeitgarantie. Die anschliessende
   [begrenzte Fehlerfortpflanzungspruefung](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/paper/paper_i/research/paired_error_propagation_2026-10-23.md)
   liefert bedingte Zustandsschranken und einen separat begrenzten
   Summationsbaum. Lokale Updatefehler, Laggrenzen und die vollstaendige
   Statistik-/Innovationsschnittstelle sind damit nicht validiert. Die
   [kurze Entscheidungsvorlage](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/paper/paper_i/research/paper_i_decision_brief_2026-10-23.md)
   verdichtet Hauptresultat, Literaturgrenzen und Nachweisaufwand fuer
   die fachliche Diskussion. Jetzt diesen Beitragskern bewerten, bevor
   weitere Runneroptimierung oder ein grosser Test beauftragt wird. Keine
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

Fuer den fundamentalen Pfad liegt nun ein konkreter FIFO-Strukturkandidat
samt Entartungsgegenbeispiel und analytischem Normalblock vor. Ein
targetfreier Pruefvertrag fuer die fehlenden 3D-Moden muss Symmetrien,
Gueltigkeitsbereich und Abbruchkriterium festlegen. Keine automatische
Auswertung archivierter Zielzellen, neue Rootsuche oder Modellergaenzung.

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
diskutierte Paarzahl teuer. Die neue bedingte Fehlerfortpflanzung begrenzt
die Verstaerkung vorgegebener lokaler Fehler, nicht deren tatsaechliche
Groesse im Simulator. Der Summationsbaum hat einen separaten Fehlervertrag.
Die Entscheidungsvorlage ist nun fuer die fachliche Diskussion vorbereitet:
Beitragskern und Gueltigkeitsargument bewerten, bevor weitere
Runnerimplementierung oder eine Rauschwahl festgelegt wird. Die bekannte
Gaussprojektion reproduziert inzwischen nachweislich denselben $D_4$;
ein reiner Mittelwertvergleich loest die Neuheitsfrage nicht. Der begrenzte
Satzvergleich und der ergaenzte konkrete Poissonbeweis praezisieren
inzwischen die verbleibende Frage nach dem Mehrwert des kontrollierten
Modellbeispiels; sie ersetzen keine fachliche Bewertung. Der gelieferte
Aging-Volltext ist nun auf Modellebene abgeglichen, mit dokumentierten
Vorzeichen-/Koeffizientenproblemen der gelieferten Fassung. Bernard--Wu
auf Satzebene und ein unabhaengiges Fachreview bleiben offen.
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
inzwischen auf Modellebene abgeglichen und deckt die lineare Euler-Regel
nach expliziter Parameterzuordnung ab. Die neue nichtlineare Rechnung
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
