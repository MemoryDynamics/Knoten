# Aktueller Stand

Stand: 2026-09-03.

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
| P5-D | `p5d-inconclusive` nach zwei nicht auswertbaren Zielaufrufen | keine Interaktionsevidenz |
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
adversarial geprueft. Das separate Readinessreview endet nach 929 lokalen
Tests und gruener CI fuer den exakten Implementierungscommit mit
`p5d-runner-ready-target-still-closed`. Eine neue prospektive Autorisierung
steht weiterhin aus; P5 bleibt deshalb geschlossen.

## Inferenz

Die Kreisloesungen sind eine geeignete Basis, um center-konjugierte Ports und
gegenseitige Kopplung mathematisch zu untersuchen. Aus den bisherigen
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

- [Implementierte Gleichungen](../reference/implemented_equations.md)
- [Native Rotating Waves](../reference/rotating_wave_foundation.md)
- [Kanonisches Modellvokabular](../reference/model_vocabulary.md)
- [P5-D Code-Review](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/reports/project/meta/reviews/scalar_memory_loop_p5d_code_review_2026-09-02.md)
- [P5-D Runner-Remediation-Protokoll](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/reports/project/meta/preregistration/scalar_memory_loop_p5d_runner_remediation_protocol_2026-09-03.md)
- [P5-D v2-Ergebnisvertrag](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/experiments/current/dynamics/rotation/scalar_memory_loop_p5d_result_schema_v2.json)
- [P5-D Implementierungs-Readiness](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/reports/project/meta/reviews/scalar_memory_loop_p5d_runner_implementation_readiness_2026-09-03.md)
- [Claim-Register](paper_claims.md)
