# Aktueller Stand

Stand: 2026-09-09.

Diese Seite berichtet nur den gegenwaertigen Befund. Die Arbeitsreihenfolge
steht ausschliesslich in den [Projektprioritaeten](project_priorities.md); der
vollstaendige vorherige Stand liegt im
[Repository-Archiv](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/docs/archive/status/current_status_through_2026-09-02.md).

## Evidenz

| Bereich | Reviewed Befund | Belastbare Lesart |
| --- | --- | --- |
| Paper 0 | technischer Anker | mathematischer Ausgangspunkt |
| Paper I, skalar | kontrollierte co-moving Relaxationswolke | lineare finite-memory Grobkoernung |
| Native Rotation | sechs lokal eindeutige finite-$H$-Roots; direkte Voll-FIFO-, Stabilitaets- und Attraction-Panels fuer ausgewaehlte Zellen | vorbereitete Kreisloesungen, keine globale Eindeutigkeit oder generische Formation |
| P4-R-S | `p4rs-anchor-scale-transfer-pass` | Zwei-Zellen-Skalentransfer, keine Replikation |
| N0 | `n0-noise-stability-window-bracketed-reviewed-pass` | endliche numerische Robustheitsklammer, keine Planck-Kalibrierung |
| P5-D | `p5d-inconclusive`; Horizontorchestrierung targetfrei reviewed | keine Interaktionsevidenz; wissenschaftliche Adapter, Horizonttransfer und neue Zielautorisierung bleiben offen |
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
die enge Ringspeicher-Tautologie. Offen bleibt der staerkere Transfer: Die
registrierte Leiter haelt $H\alpha=12$ fest und zeigt nicht, dass Root und
Stabilitaet bei festem $\alpha$ den Grenzfall $H\to\infty$ erreichen. Deshalb
steht vor einer neuen P5-Zielautorisierung ein separates Horizontgate.

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
Quotientdistanz sind als Bibliothekskerne vorhanden. Offen sind die strikten
v3-Adapter, der Homotopieschlauch, der Ausschlussbaum, das tail-augmentierte
Zertifikat und die Durchleitung des vorgeschriebenen LCG-Starts bis ARPACK.
Ein Horizontlauf ist nicht autorisiert.

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
- [Claim-Register](paper_claims.md)
