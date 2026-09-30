# Aktueller Stand

Stand: 2026-09-30.

Diese Seite berichtet nur den gegenwaertigen Befund. Die Arbeitsreihenfolge
steht ausschliesslich in den [Projektprioritaeten](project_priorities.md); der
vollstaendige vorherige Stand liegt im
[Repository-Archiv](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/docs/archive/status/current_status_through_2026-09-02.md).

## Evidenz

| Bereich | Reviewed Befund | Belastbare Lesart |
| --- | --- | --- |
| Paper 0 | technischer Anker | mathematischer Ausgangspunkt |
| Paper I, skalar | kontrollierte co-moving Relaxationswolke | lineare finite-memory Grobkoernung |
| Native Rotation | sieben lokal eindeutige finite-$H$-Roots; sechs zertifizierte Homotopiekanten verbinden G5 bei $H=2400$ mit dem endlichen G4-Kopf bei $H=3600$ | lokale finite Rootast-Verbindung und direkte numerische Stabilitaet bei exakt $H=2400$; separater lokaler $F_\infty$-Root, aber kein letzter Branchtransfer, keine globale Eindeutigkeit, $H\to\infty$-Stabilitaet oder generische Formation |
| P4-R-S | `p4rs-anchor-scale-transfer-pass` | Zwei-Zellen-Skalentransfer, keine Replikation |
| N0 | `n0-noise-stability-window-bracketed-reviewed-pass` | endliche numerische Robustheitsklammer, keine Planck-Kalibrierung |
| P5-D | `p5d-inconclusive`; drei eigene Produktionsaufrufe technisch verbraucht | keine Interaktionsevidenz; der separate G5-Pass ist ein Single-Loop-Stabilitaetsbefund und keine P5-D-Aussage |
| Source-Audit | `referee-source-ready-with-major-claim-restrictions` | publication source mit offenen Hardening-Auflagen |

## Was der Kreisnachweis genau sagt

Fuer den Anchor mit
`alpha=0.01`, `H=1200`, `eta=0.15`, `A_att=3.5` reduziert das Einsetzen von
$x_n=R e^{in\theta}$ die unveraenderte Grundgleichung exakt auf zwei endliche
Balancesummen. Ein prospektiver Krawczyk-Test schliesst in seinem registrierten
lokalen Kasten genau einen Root ein. Die direkte 2400-dimensionale
mitrotierende Voll-FIFO-Map reproduziert die vorbereitete Historie mit
maximalem Komponentenfehler $2.46\times10^{-15}$; lokale Stoerungen
kontrahieren numerisch. Am spaeteren L3-Kandidaten erreichen zudem zehn
registrierte nichtkreisfoermige Arme den zugehoerigen Orbit.

Fuer diesen vorbereiteten Rotating-wave-FIFO wurde kein KnotScore erhoben.
Das ist derzeit keine fehlende Erfolgszahl: KnotScore v0.5/v0.6 bewertet
kontrollierte Metastabilitaet, Residence und Shape-Stationaritaet, waehrend
Root-, Stabilitaets- und Attraction-Panels eine vorbereitete Kreisloesung
testen. Eine zulaessige gemeinsame Score-/Formationauswertung braeuchte
deshalb ein eigenes prospektives Design mit `eta_zero`-Kontrolle; die
Einordnung steht im
[Experimentkatalog](../reference/experiment_catalog.md).

Das ist der fuer P5 benoetigte kandidatenbezogene Existenz- und
Identitaetsnachweis. Es ist kein globaler Einzigkeitsbeweis: $+\theta$ und
$-\theta$ sind Chiralitaetspartner, globale Rotationen parametrisieren
dieselbe ambiente $SO(2)$-Gruppenbahn, und weitere entfernte Roots sind nicht
ausgeschlossen. P5 darf deshalb einen fest registrierten Kreis als Input
verwenden, aber nicht behaupten, die Parameter erzeugten global nur einen
Kreis.

Der FIFO ist dabei nur eine endliche Alterswarteschlange und schreibt keine
raeumliche Ringtopologie vor. Krawczyk-Balancen, der kollabierende
$\eta=0$-Arm und zehn anziehende nichtkreisfoermige P3-Historien widerlegen
die enge Ringspeicher-Tautologie. Der inzwischen positiv auditierte
G1--G3-Lauf verbindet bei festem $\alpha=0.01$ sieben lokale finite Roots
ueber sechs Krawczyk-Homotopiekanten bis zum endlichen G4-$H=3600$-Kopf.
G4 zertifiziert separat einen lokalen $F_\infty$-Root in derselben kleinen
Umgebung; ohne Homotopie $F_{3600}\to F_\infty$ bleibt dieser letzte
Branchtransfer offen. Ebenso ist nicht gezeigt, dass die direkte Stabilitaet
von $H=2400$ den Grenzfall $H\to\infty$ erreicht.

Das abschliessende Metareview vor Paper I urteilt deshalb
`finite-branch-paper-i-ready-with-explicit-infinity-gap`. Es fand keinen
Critical- oder Major-Implementierungsbefund, korrigierte aber vor der
Manuskriptarbeit den Major-Dokumentationsbefund, der den endlichen
$H=3600$-Endpunkt zu weitgehend mit dem separaten $F_\infty$-Root
identifiziert hatte.

Die Unendlichkeits-Astluecke ist inzwischen als eigener harter Ein-Box-Test
prospektiv spezifiziert. Die targetfreie Implementierung bildet
$F_s=F_{3600}+sT_{3600}$ auf $s\in[0,1]$ direkt ab und verlangt neben zwei
strikten 120-/160-dps-Krawczyk-Panels eine uniforme Schranke
$\sup\|I-YD F_s(X)\|_\infty<1$. Validator und getrennter
Standardbibliotheksauditor extrahieren die G1--G3-/G4-Endpoints erneut aus
sechs fest gehashten Git-Blobs. Zwei im Review gefundene Vertragsfehler bei
Snapshot-Rueckbindung und Decimal-Kontext sind vor einem Ziellauf behoben.
27 neue Tests, der relevante 284-Test-Horizontverbund und die vollstaendige
1226-Test-Repository-Matrix bestehen; das Urteil lautet
`g-infinity-branch-link-contract-implementation-pass-target-closed`.
Der exakte Implementierungscommit bestand danach auch die offizielle
Linux-CI mit Lint, Tests und strict Docs. Das Execution-Readinessreview bindet
Commit, CI und alle zwoelf geschuetzten Git-Blobs mit dem Urteil
`g-infinity-branch-link-implementation-ready-target-closed`. Der autorisierte
Attempt 1 wurde am 2026-09-30 verbraucht, aber vor jeder Publikation durch den
Validator mit `inward regularity bound` gestoppt. Das exklusive Receipt ist
erhalten; Resultat, Audit und Manifest existieren nicht. Der Befund lautet
`g-infinity-branch-link-attempt-1-inconclusive-regularity-serialization-failure`:
Er falsifiziert den Dezimalrecord, nicht den mathematischen Astlink. Vor
Attempt 2 waren exakte Binaer-zu-Dezimal-Endpunkte, ein eigenes Amendment,
Regressionstests, Review und neue CI erforderlich. Amendment und targetfreie
Remediation liegen inzwischen vor: Der Adapter bildet jedes mpmath-Tupel
$(s,m,e,b)$ ohne Praezisionskontext exakt auf $(-1)^s m2^e$ ab. 41
fokussierte Tests, das konstruktive Attempt-1-Gegenbeispiel, 1240 gesamte
Tests und der exakte Ruff-Scope bestehen. Das Reviewurteil lautet
`g-infinity-branch-link-attempt-2-remediation-pass-target-closed`.
Der exakte Implementierungscommit hat inzwischen auch die offizielle
Linux-CI mit Lint, 1240 Tests und strict Docs bestanden. Das
Execution-Readinessreview bindet Commit, CI, Attempt-1-Incident und 14
geschuetzte Blobs mit dem Urteil
`g-infinity-branch-link-attempt-2-implementation-ready-target-closed`.
Attempt-2-Governance wurde daraufhin einmalig geoeffnet. Der Zugriff wurde
verbraucht, aber erneut vor Publikation mit `inward regularity bound`
gestoppt. Die exakte Binaerendpunktkonvertierung war nicht die letzte
Rundungsstelle: `_row_norm_upper` addierte die langen `Decimal`-Werte im
28-stelligen Standardkontext. Ein targetfreies 29-stelliges Gegenbeispiel
beweist, dass diese Summe nach oben ueber ihren exakten Wert runden kann.
Attempt 2 lautet daher
`g-infinity-branch-link-attempt-2-inconclusive-decimal-context-failure`.
Nur das Receipt existiert; es gibt weiterhin keinen
Branch-Link-Resultatclaim.

Dieses Gate ist inzwischen prospektiv spezifiziert. Es haelt
$\alpha=0.01$, $\eta=0.15$, $M_0$, Kernel und $\varepsilon=0$ fest, trennt
die Vorwaertsleiter bis $H=3600$ von der unteren $H=900,600$-Belastung und
fordert einen Tail-Krawczyk-Einschluss fuer den lokalen Root von
$F_\infty$. Ein negatives Review fand sechs Luecken einschliesslich eines
konstruktiv falschen binary64-Vergleichs; die Amendierung schliesst sie. Das
Suffizienzurteil lautet
`rotating-wave-horizon-transfer-protocol-sufficient-implementation-closed`.
Ergebnisvertrag und rote targetfreie Tests wurden danach getrennt committed;
die kleinste Infrastruktur bestand 40 fokussierte und 985 gesamte Tests. Das
Infrastruktururteil lautet
`rotating-wave-horizon-transfer-contract-infrastructure-pass-runner-incomplete-horizon-run-closed`.
Ein nachfolgendes Negativreview zeigte, dass v1 mehrere registrierte
Abbruchpfade nicht wahrheitsgetreu serialisieren konnte; v2 schloss diese
Nullsemantik. Ein weiteres Negativreview zeigte jedoch, dass positive
Zertifikats-, Spektral- und Trajektorienbeziehungen noch nicht vollstaendig
rekonstruierbar waren. v3 schliesst diese Luecken. Eine erste Linux-CI
falsifizierte dabei native `sin`-/`cos`-Starts als plattformunabhaengig; die
vor jedem Zielzugriff amendierte portable LCG-Konstruktion besteht 59
fokussierte und 1004 gesamte Tests sowie die exakte Linux-CI. Das
Reviewurteil ist
`rotating-wave-horizon-transfer-contract-v3-pass-runner-red-open-target-closed`.
Die anschliessende pure Orchestrierung bestand ihre Stopptests. Ein neuer
Counterexample zeigte jedoch, dass ein einzelnes ausgeschlossenes Halbblatt
als vollstaendige lokale Ausschlussdomain akzeptiert wurde. Validator und
Auditor rekonstruieren deshalb nun unabhaengig Rootbindung, deterministische
dyadische Leafpfade, Praefixfreiheit und vollstaendige Bedeckung. Eine
vollstaendige Ausschlusspartition bei gleichzeitig zertifiziertem Zielroot
wird als Widerspruch verworfen. 70 fokussierte und 1015 gesamte Tests sowie
die exakte Linux-CI sind gruen. Der anschliessende Backend-Bestandsaudit
korrigiert die pauschale Fehlstellenbeschreibung: finite Residuen/Jacobians,
Punkt-Newton, lokale Krawczyk-Boxen sowie FIFO-Map/Jacobian und
Quotientdistanz sind als Bibliothekskerne vorhanden. Der finite-Rootadapter
nutzt den bestehenden Acht-Schritt-Newton-/Krawczyk-Kern. Der anschliessende
Homotopieadapter erweitert denselben Intervallkern auf volle geschlossene
Parameterscheiben und erzwingt 64 Scheiben, strikten Einschluss,
Nachbarueberlappung sowie fail-closed Praefixstopps. Seine CI besteht 1029
Tests; keine registrierte Horizontkante wurde ausgewertet. Der lokale
Ausschlussadapter verwendet denselben Residual-/Krawczyk-Kern und bildet die
feste normalisierte FIFO-Teilung bis Tiefe 20 in den rekonstruierten v3-Record
ab. Er wurde nur an kontrollierten Antworten getestet; keine registrierte
Domain ist ausgeschlossen oder als Rootdomain klassifiziert. Seine
FIFO-kuratierte Implementierungs-CI besteht 1038 Tests. Das anschliessende
Tailzertifikat erweitert das endliche Residuum und beide Jacobi-Spalten um
die registrierten analytischen Normbounds und verwendet danach denselben
outward-rounded Krawczyk-Kern. Null-Tail-Reproduktion, Intervallerweiterung,
Typfehler und Nichtinklusion sind targetfrei getestet. Das damalige
Reviewurteil lautete
`horizon-tail-krawczyk-adapter-target-free-pass-g4-unmeasured`: Zu diesem
Zeitpunkt war kein $H=3600$-Kandidat eingesetzt worden. Offen sind
LCG-Arnoldi, Trajektorienabbildung und Backendkomposition. Die explizite
Nutzerfreigabe vom 2026-09-13 zog einen isolierten G4-Komponentenlauf vor.
Nach gruenem Readiness-Commit und exakter CI startete dieser genau einmal,
brach aber bei der nachgeschalteten Recordvalidierung an einer unzulaessig
exakten Kontrolle der outward-gerundeten aeusseren Box ab. Der Codepfad
rief zuvor mindestens das erste Tailpanel auf; mangels publiziertem Record
ist weder Panelpass noch -fail verwertbar. Ergebnisartefakte und
unabhaengiger Ergebnisaudit entstanden nicht. Der Ausgang ist
`g4-experiment-invalid-outward-box-validation`, nicht G4-Fail.
Die Boxpruefung ist targetfrei auf garantierte Umschliessung plus eng
praezisionsgebundenen Serialisierungsueberschuss korrigiert. Der separat
preregistrierte Retry auf Commit `fb1cc7d` besteht anschliessend beide
strikten 120/160-dps-Tailpanels; ihre Krawczyk-Bilder ueberlappen. Der
Standardbibliothek-Auditor rekonstruiert alle acht Checks und urteilt
`g4-independent-audit-agrees`. Damit war G4 zunaechst nur als isolierte lokale
$F_\infty$-Komponente `pass`; die G1--G3-Branchverbindung und der
vollstaendige Horizontlauf waren zu diesem Zwischenstand noch nicht belegt.
P5-D bleibt weiterhin nicht belegt.

Das anschliessende G4-zu-G5-Meta-Review bestaetigt diese enge Claimgrenze und
findet keinen neuen kritischen G4-Defekt. Die daraus abgeleiteten
LCG-Arnoldi- und Trajektorienadapter bestehen targetfrei: der LCG-Start wird
unveraendert an ARPACK weitergegeben, Ritzvektoren werden v3-konform
gespeichert, Fehler behalten Nullsuffixe, und Instabilitaet verlangt nun das
tatsaechlich gematchte Paar beider Panels. Fortsetzungen bleiben bis zu
vollstaendigen Residual-, Symmetrie-, Panel- und Hashchecks geschlossen.
Der anschliessende Grundgleichungs-Preflight bindet ausserdem $q$, $H$,
$M_0$, $\eta$, Depositionsgewicht, direkte Gewichtssumme, native
Kreiskovarianz, mitrotierenden Fixpunkt, Voll-Jacobian und Symmetrien an
einen kanonisch hashbaren Record. Er bestaetigt targetfrei die beabsichtigte
Architektur: Nur Arnoldi ist linearisiert; die Stoerungsarme iterieren die
nichtlineare Voll-FIFO-Grundgleichung. Nach zwei getrennten
Publikationsincidents schloss Attempt 3 die Recordluecke mit einer dichten
Vollschrittspur. Der einmalige Ziellauf besteht beide Arnoldi-Panels und alle
drei nichtlinearen Stoerungsarme; der unabhaengige Auditor rekonstruiert
Record, Entscheidung und Publikationshashes. Das Ergebnis lautet
`g5-local-direct-stability-pass` fuer exakt $H=2400$. Dies ist kein
Intervallbeweis des vollen Spektrums und keine Aussage ueber
$H\to\infty$, Formation oder Interaktion.

Die verbleibende G1--G3-Branchverbindung ist inzwischen als eigene, engere
Komponente preregistriert und targetfrei implementiert. Sie rechnet G4 und G5
nicht erneut, sondern bindet deren fuenf versiegelte Artefakte und fordert
gegenseitige Krawczyk-Inklusionen an $H=2400$ und $H=3600$. Ein
Implementierungsreview verwarf zunaechst freie G0-/G6-Boolfelder; der
amendierte Vertrag speichert direkte 70-dps-Summenresiduen,
FIFO-Fehlerwerte und erwartete/beobachtete Altersfolgenhashes. Validator und
getrennter Standardbibliotheksauditor rekonstruieren Root-, Homotopie-,
Drift-, Ausschluss-, Endpunkt- und Entscheidungssemantik. Manifest-last-
Publikation und One-shot-Guard sind targetfrei geprueft; die Governance ist
geschlossen. Der erste offizielle CI-Lauf fand einen plattformabhaengigen
CRLF-Hash des G4-Audits; die outcome-blinde Remediation bindet nun alle fuenf
Inputs an kanonische Git-Blobs. Der Folgelauf besteht Ruff, 1194 Tests und
strikten Docs-Bau. Zu diesem Readiness-Zwischenstand gab es noch keinen
G1--G3-Befund. Der spaeter autorisierte Attempt 1
erreichte die nachgeschaltete Homotopievalidierung, scheiterte dort aber vor
Audit und Publikation an einer exakten Mittelpunktforderung fuer eine
outward-gerundete Box. Nur das exklusive Receipt entstand. Der Versuch ist ein
verbrauchter Pipeline-Incident ohne G1--G3-Befund; ein Retry ist nicht
autorisiert. Die vierte outcome-blinde Amendierung versioniert den Vertrag als
v2 und ersetzt exakte Mittelpunkt-/Breitenidentitaet durch eine beidseitig
beschraenkte Outward-Containment-Pruefung. Einwaertsschrumpfung und
uebermaessige Aufweitung bleiben harte Fehler. Produktionsvalidator und
getrennter Standardbibliotheksauditor bestehen die targetfreien
Falsifikationstests; neue `attempt_2`-Pfade schuetzen das alte Receipt. Das
kritische Remediationreview findet keinen Major- oder Critical-Codebefund.
Der exakte Implementierungscommit besteht 1199 lokale Tests, den CI-genauen
Ruff-Scope, strict Docs und die offizielle Linux-CI. Das neue Review endet mit
`g1-g3-implementation-ready-target-closed`. Der danach einmalig autorisierte
Attempt 2 publiziert sieben lokal eindeutige 80-/120-dps-Rootpanels, sechs
vollstaendige 64-Scheiben-Homotopien, direkte Summenreplays, fallende
outward-rounded Drift und positive gegenseitige Endpunktinklusionen zu G5
bei $H=2400$ und G4 bei $H=3600$. Alle Gates bestehen; der unabhaengige
Auditor stimmt zu. Das Ergebnisreview urteilt
`g1-g3-local-fixed-alpha-root-branch-connected-reviewed-pass`. Zulassbar ist
damit die lokale Rootast-Verbindung mit direkter Stabilitaetsstuetzung bei
exakt $H=2400$. Nicht belegt sind $H\to\infty$-Stabilitaet, globale
Eindeutigkeit, Formation, Interaktion, Spin, Traegheit oder Masse. Die
Attempt-2-Autorisierung ist verbraucht und Governance wieder geschlossen.

## P5-D Code-Review und Remediation

Das Review trennte eine algebraisch konsistente Center-/Port-Konstruktion von
einer nicht belastbaren Ergebnisstrecke. Es reproduzierte folgende Blocker:

- Der Provenienzguard akzeptiert den inzwischen geschlossenen Ast weiterhin.
- Off-Arme erzeugen konstruktiv nichtendliche Sentinelwerte.
- Endlichkeitspruefung und Auditor sind fuer unbekannte Skalartypen fail-open.
- Die behauptete atomare Ausgabe zweier Dateien ist nicht paarweise atomar.
- Der Renderer setzt Diagnostik auch dann voraus, wenn die Antwort als nicht
  verfuegbar registriert wurde.
- Das Modellvokabular kollidiert zwischen Paper-I-Deposition, Centerfilter,
  Portgroessen und Maschinenrundung; der kanonische Notationsvertrag ist
  deshalb Teil der Remediation.

Die Recovery-Autorisierung ist verbraucht. Inzwischen bildet ein getrackter
maschinenlesbarer Governancezustand diese Schliessung ab; der Runner prueft
ihn vor der alten Provenienzstrecke und vor jeder Arm-Auswertung. Die zweite
targetfreie Teilkorrektur verwendet `null` fuer die nicht anwendbare
Off-Arm-Mobilitaetsmetrik, lehnt unbekannte Typen fail-closed ab und rendert
eine unverfuegbare Antwort ohne Diagnostikzugriff. Das exakte v2-Payloadschema,
die Manifest-zuletzt-Publikation, eine unabhaengige Manifestpruefung sowie die
einmalige CI-/Commit-gebundene Lease sind targetfrei implementiert und
adversarial geprueft. Das separate Readinessreview endete nach 929 lokalen
Tests und gruener CI fuer den exakten Implementierungscommit mit
`p5d-runner-ready-target-still-closed`. Eine danach ausdruecklich und einmalig
autorisierte dritte Ausfuehrung berechnete Panel, Response und Klassifikation,
scheiterte jedoch vor JSON-Encoding am strikten v2-Typvertrag: Die
Channel-off-Energieskala `numpy.finfo(float).tiny` wandelte sechs native
Nullquotienten in `numpy.float64` um. Receipt 3 existiert, Ergebnis, Report,
Manifest und Audit nicht. Damit ist auch dieser Lauf `p5d-inconclusive`, die
Readiness-Abdeckung falsifiziert und die Einmalfreigabe verbraucht. P5 bleibt
geschlossen.

Das danach getrennt geschriebene Produktionspfad-Protokoll wurde in einem
ersten Review wegen sechs Spezifikationsluecken abgelehnt, anschliessend
amendiert und im separaten Suffizienzreview als
`p5d-production-preflight-protocol-sufficient-target-closed` bewertet. Die
Amendierung friert neben drei wissenschaftlichen Quell-Blobs 41
wissenschaftliche Runner-Symbole per AST-Digest ein und oeffnet nur
target-gesperrte Fehltests sowie eine minimale P5-lokale Korrektur an der
vorhandenen Record-Grenze. Python-Standardbibliothek traegt den Datenvertrag;
NumPy-Skalare duerfen die numerische Schicht nicht ungeprueft verlassen. Eine
gemeinsame Projektbibliothek bleibt bis zu einem dokumentierten
Drei-Pipelines-Semantikvergleich gesperrt.

Diese Korrektur ist nun targetfrei abgeschlossen. Der echte Rueckgabepfad
konvertiert nur registrierte NumPy-Skalare werttreu in native Recordtypen und
validiert jeden vollstaendigen Off-/Aktivarm sofort gegen das v2-Schema. Der
reproduzierte Versuch-3-Nullquotient, ein adversariales Typenfeld, ein
synthetisches 64+768-Vollpanel, Publikation und unabhaengiger Auditor sind
gruen; ebenso 945 lokale Tests und CI fuer den exakten Implementierungscommit.
Das neue Review endet mit
`p5d-production-boundary-ready-target-closed-horizon-transfer-required`.
Das ist Infrastruktur-Readiness, keine Interaktionsevidenz und keine
Autorisierung fuer Versuch 4.

## Inferenz

Die Kreisloesungen sind eine geeignete Basis, um center-konjugierte Ports und
gegenseitige Kopplung mathematisch zu untersuchen. Aus den drei bisherigen
Ziellaeufen folgt jedoch nichts ueber reale Wechselwirkung oder Masse.

## Hypothesen

Interaktion, Ladung und Felder sowie Spin, Impuls, Traegheit und Masse bleiben
offen. Insbesondere ist eine zweite Differenz im sichtbaren Pfad noch kein
Nachweis einer positiven, zustandsunabhaengigen Masse. Der reziproke P5-D-Port
besitzt bei angehaltener nativer Centerbewegung exakt ein Relaxationsmodell
erster Ordnung. Ein gekoppelter harmonischer Oszillator ist daher ein
nachgelagerter Falsifikator fuer eine zusaetzliche, gedaechtnisinduzierte
Zustandsdimension und kein bereits eingebautes P5-D-Ergebnis.

## Claim-Grenze

Zulaessig ist: lokal zertifizierte bzw. numerisch kontrollierte Schleifen und
eine algebraisch definierte gegenseitige Center-Kopplung. Nicht zulaessig ist:
eine physikalische Deutung der P5-D-Infrastrukturfehler als positives oder
negatives Interaktionsergebnis.

## Quellen

- Modellreferenz: [Gleichungen](../reference/implemented_equations.md),
  [Rotating Waves](../reference/rotating_wave_foundation.md) und
  [Vokabular](../reference/model_vocabulary.md)
- [P5-D v2-Ergebnisvertrag](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/experiments/current/dynamics/rotation/scalar_memory_loop_p5d_result_schema_v2.json)
- [P5-D Versuch-3-Incident](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/reports/project/meta/reviews/scalar_memory_loop_p5d_attempt3_numpy_float_schema_failure_2026-09-05.md)
- [P5-D Produktionspfad-Protokoll](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/reports/project/meta/preregistration/scalar_memory_loop_p5d_production_path_preflight_protocol_2026-09-06.md)
- P5-D Protokollreviews:
  [negatives Erstreview](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/reports/project/meta/reviews/scalar_memory_loop_p5d_production_path_preflight_protocol_review_2026-09-06.md)
  und
  [Suffizienzreview](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/reports/project/meta/reviews/scalar_memory_loop_p5d_production_path_preflight_protocol_sufficiency_review_2026-09-06.md), danach das
  [Produktionsgrenzen-Readinessreview](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/reports/project/meta/reviews/scalar_memory_loop_p5d_production_path_readiness_review_2026-09-07.md)
- Horizontkette:
  [Finite-H Non-Tautology-/Horizont-Audit](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/reports/project/meta/reviews/scalar_memory_finite_h_non_tautology_audit_2026-09-07.md),
  [amendiertes Protokoll](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/reports/project/meta/preregistration/scalar_memory_rotating_wave_horizon_transfer_protocol_2026-09-08.md),
  [negatives Review](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/reports/project/meta/reviews/scalar_memory_rotating_wave_horizon_transfer_protocol_review_2026-09-08.md)
  und
  [Suffizienzreview](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/reports/project/meta/reviews/scalar_memory_rotating_wave_horizon_transfer_protocol_sufficiency_review_2026-09-08.md), danach
  [RED-Review](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/reports/project/meta/reviews/scalar_memory_rotating_wave_horizon_transfer_red_contract_review_2026-09-08.md)
  und
  [Infrastrukturreview](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/reports/project/meta/reviews/scalar_memory_rotating_wave_horizon_transfer_contract_infrastructure_review_2026-09-08.md)
  sowie das
  [v3-Vertragsreview](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/reports/project/meta/reviews/scalar_memory_rotating_wave_horizon_transfer_contract_v3_review_2026-09-09.md)
  und das korrigierende
  [Orchestrierungsreview](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/reports/project/meta/reviews/scalar_memory_rotating_wave_horizon_transfer_runner_orchestration_review_2026-09-09.md)
  sowie den
  [Backend-Bestandsaudit](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/reports/project/meta/reviews/scalar_memory_rotating_wave_horizon_backend_reuse_audit_2026-09-09.md)
  und das
  [finite-Rootadapter-Review](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/reports/project/meta/reviews/scalar_memory_rotating_wave_horizon_finite_root_adapter_review_2026-09-09.md)
  sowie das
  [Homotopie-/Intervallreview](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/reports/project/meta/reviews/scalar_memory_rotating_wave_horizon_homotopy_interval_review_2026-09-09.md)
  und das
  [lokale Ausschlussreview](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/reports/project/meta/reviews/scalar_memory_rotating_wave_horizon_local_exclusion_review_2026-09-09.md)
- [Claim-Register](paper_claims.md)
