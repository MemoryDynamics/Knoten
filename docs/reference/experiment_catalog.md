# Experimentkatalog

Stand: 2026-09-10.

Diese Seite ist ein kuratierter Wegweiser, kein Ergebnisjournal und keine
zweite Roadmap. Die einzige Arbeitsreihenfolge steht unter
[Projektprioritaeten](../status/project_priorities.md). Der vollstaendige
[Katalog bis 2026-09-09](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/docs/archive/reference/experiment_catalog_through_2026-09-09.md)
und der
[Report-Index](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/reports/README.md)
bewahren die Detailhistorie. Das
[Kuratierungsreview](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/reports/project/meta/reviews/repository_navigation_curation_review_2026-09-10.md)
dokumentiert die Trennung von Evidenz, offenen Fragen und Arbeitsreihenfolge.

## 1. Aktive Methodenkette

| Einheit | Stand | Evidenzgrenze |
| --- | --- | --- |
| P5-D-Produktionspfad | Versuch 3 `inconclusive`; targetfreier Produktionspfad reviewed | kein Ergebnis und keine Freigabe fuer Versuch 4 |
| Fixed-alpha-Rootadapter | implementiert und reviewed | Adapterbeleg, kein neu berechneter Root |
| Homotopie-/Intervalladapter | implementiert und reviewed | affine Deformation $F_a+s(F_b-F_a)$, kein kontinuierliches physisches $H$ und keine ausgewertete Kante |
| Lokaler Ausschlussadapter | implementiert und reviewed | vollstaendige dyadische Recordsemantik, aber keine registrierte Domain ausgewertet |
| Tailzertifikat | naechster targetfreier Block | noch kein unendlicher Root |
| Stabilitaets-/Trajektorienadapter | danach offen | vorhandene Kerne, aber noch keine v3-konforme LCG-/Recordabbildung |
| Backendkomposition und Readiness | geschlossen | kein Horizontlauf vor separatem Review |

Die drei abgeschlossenen Horizontadapter verwenden gemeinsame Newton-,
Krawczyk-, Residual- und Jacobianfunktionen. Der finale lokale
Ausschlussstand bestand
[1038 Tests in Linux-CI](https://github.com/MemoryDynamics/Knoten/actions/runs/34414798462).

## 2. Experimentfamilien

| Familie | Kanonischer Ort | Aktueller belastbarer Befund |
| --- | --- | --- |
| Skalarer Long-Run und Memory | `experiments/current/dynamics/long_runs/`, `dynamics/scaling/` | kompakte kontrollierte Memory-Clouds und effektive Center-Mechanik; keine physikalische Masse |
| Rotating waves und finite FIFO | `experiments/current/dynamics/rotation/` | sechs lokal eindeutige finite-$H$-Roots; lokale Stabilitaets- und endliche Formationsevidenz nur fuer ausgewaehlte Zellen |
| Center-Port und Mechanik | `experiments/current/dynamics/scaling/` | positiver effektiver Inertialport fuer $c$; sichtbares $x$ bleibt portabhaengig overdamped |
| Kopplung und Interaktion | `experiments/current/memory/synchronization/`, `dynamics/rotation/` | mehrere kontrollierte Null-/Relaxationsbefunde; P5-D bleibt `inconclusive` |
| Kernel und Felder | `experiments/current/kernels/` | lokale Kernel-/Feldbeziehungen und Kontrollen; kein universelles physisches Feldgesetz |
| Dimension und Topologie | `experiments/current/dimensions/`, `topology/` | diagnostische Dimensionen und vorbereitete Kreisgeometrie; keine ambient-unabhaengige 3D-Selektion oder interne $S^1$-Phase |
| Markov, Moden und Scores | `experiments/current/markov/`, `knot_stability/` | Scorecards und Modendiagnostik; keine kontrollgetrennte komplexe skalare Slow-Mode |

## 3. Offene Fragen, nicht weitere Prioritaeten

| Frage | Derzeitige Antwort | Was sie entscheiden wuerde |
| --- | --- | --- |
| Erzeugt die FIFO-Struktur den Kreis tautologisch? | Nein. Sie ordnet Alter; der Kreis folgt nur aus Kraftbalance und Dynamik. | finite-$H$-Audit, Rootzertifikat und Kontrollen |
| Wie hoch ist der KnotScore des Rotating-wave-FIFO? | Nicht erhoben und derzeit nicht entscheidungsfaehig. | gepaarte Formation aus nichtkreisfoermigen Starts plus `eta_zero`, Stationaritaet und vorregistrierte Scorecard |
| Ist der finite Kreis ein gebildeter Knoten? | Fuer zehn vorbereitete Nichtkreis-Arme gibt es endliche Attractionsevidenz, aber keinen offenen Basin- oder generischen Formationsbeweis. | eigenstaendiges Formation-/Basin-Protokoll |
| Ueberlebt der Root bei festem $\alpha$ fuer $H\to\infty$? | Offen. | Horizontgate einschliesslich Tailzertifikat |
| Besitzt das System eine interne $S^1$-Phase oder Spin? | Nicht gezeigt; die bisherige Bahn ist eine raeumliche $SO(2)$-Gruppenbahn. | interne Observable nach Quotientierung der Raumrotation |
| Ist $\mu$ physikalische Masse? | Nur eine effektive positive Center-Port-Darstellung ist belegt. | mikroskopischer Aktuator, Portinvarianz und Einheitenkalibrierung |
| Gibt es Knoteninteraktion? | P5-D ist technisch `inconclusive`. | erst abgeschlossene Remediation, dann separat autorisierter Lauf |

## 4. Scorecards und ihre Zustaendigkeit

| Scorecard | Frage | Darf nicht als Ersatz dienen fuer |
| --- | --- | --- |
| KnotScore v0.5/v0.6 | kontrollierte Metastabilitaet, Residence, Kompaktheit und Shape-Stationaritaet | Rootexistenz, interne Phase, Masse oder Interaktion |
| FormationScore | Entstehung aus nicht vorbereiteten Anfangszustaenden und Basin-Robustheit | lokale Stabilitaet eines vorbereiteten Orbits |
| ModeScore | kontrollgetrennte persistente oder intermittierende komplexe Moden | blosse raeumliche Rotation |
| PropagationScore | gerichtete, retardierte und kontrollgetrennte Antwort | statische oder instantane Kopplung |

Der Rotating-wave-Zweig wird deshalb momentan durch Existenz-, Stabilitaets-,
Attraction- und Horizontgates beurteilt, nicht durch einen nachtraeglichen
KnotScore. Falls Prioritaet 3 einen Formationsclaim verlangt, muessen
FormationScore und KnotScore gemeinsam prospektiv registriert werden.

## 5. Wiederverwendung und Ablage

Allgemeine Numerik liegt unter `src/emergenz_knoten/` und erhaelt direkte
Unit-Tests. Experimentparameter, Gatefolge und Serialisierung bleiben im
jeweiligen Runner. Aktuell wiederverwendet werden:

- finite Rotating-wave-Summen, analytische Jacobians und Newtonschritte;
- outward-rounded finite und parametrische Krawczyk-Auswertung;
- native und mitrotierende FIFO-Map samt Volljacobian;
- Quotientdistanz und vorhandene Trajektorienfortsetzung;
- Schema-, Manifest- und unabhaengige Auditbausteine.

Neue gemeinsame Bibliotheksabstraktionen entstehen nur bei nachgewiesen
semantikgleichen Anwendungen. Historische Ergebnisrecords sind keine
Backends und duerfen nicht als neue Evidenz kopiert werden.

## 6. Reproduzierbarkeit

1. Protokoll, RED-Test und Implementierung werden getrennt committed.
2. Ergebnisentscheidungen verwenden nur vorregistrierte Parameter und
   Schwellen.
3. Kontroll-, Abbruch- und Nullsemantik bleibt im Ergebnis rekonstruierbar.
4. Numerische Claims binden Code-, Daten- und Konfigurationsprovenienz.
5. Manifest und unabhaengiger Audit werden zuletzt erzeugt.
6. Ein technischer Pipelinepass ist keine wissenschaftliche Evidenz.
7. Historische Detailtabellen bleiben im Archiv statt auf aktiven Seiten.

## 7. Einstiegspunkte

- [Aktueller Status](../status/current_status.md)
- [Eine Prioritaetenliste](../status/project_priorities.md)
- [Paper-Claims](../status/paper_claims.md)
- [Implementierte Gleichungen](implemented_equations.md)
- [Modellvokabular](model_vocabulary.md)
- [Repository Map](repository_map.md)
- [Historischer Vollkatalog](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/docs/archive/reference/experiment_catalog_through_2026-09-09.md)
