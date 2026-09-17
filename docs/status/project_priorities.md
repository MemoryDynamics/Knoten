# Projektprioritaeten

Stand: 2026-09-17.

Dies ist die einzige aktive Arbeitsreihenfolge des Repositorys. Der
[Stand bis 2026-09-09](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/docs/archive/status/project_priorities_through_2026-09-09.md)
ist archiviert. Katalog, Status und Reports duerfen Befunde und Blocker
nennen, aber keine zweite Prioritaetenliste fuehren.

Eingefrorene Voraussetzungen bleiben
`p4rs-anchor-scale-transfer-pass`,
`n0-noise-stability-window-bracketed-reviewed-pass` und
`p5d-mutual-center-design-identifiable`.
**P5-D Versuch 3 technisch inconclusive: Pipeline geschlossen**; die
**Attempt-3-Lease ist verbraucht**.
Diese Befunde ordnen Prioritaet 1 ein, sind aber keine weiteren Arbeitspunkte.

## Eine Liste

1. **Remediation abschliessen -- in Arbeit.** Der P5-D-Produktionspfad bleibt
   nach Versuch 3 geschlossen. Root-, Homotopie- und lokaler
   Ausschlussadapter des vorgeschalteten Fixed-alpha-Horizontgates sind
   targetfrei reviewed; das tail-augmentierte Krawczyk-Zertifikat ist nun
   ebenfalls targetfrei reviewed. Der erste isolierte G4-Komponentenlauf
   brach bei der nachgeschalteten Recordvalidierung an einer unzulaessig
   exakten Kontrolle der outward-gerundeten Box ab; kein verwertbares
   Ergebnis entstand und G4 bleibt ungemessen. Die Boxpruefung ist nun
   targetfrei remediated und mit 1063 lokalen Repositorytests geprueft.
   Der separat preregistrierte Retry besteht G4 mit zwei strikten,
   ueberlappenden 120/160-dps-Tailpanels; der unabhaengige Recordaudit stimmt
   zu. Das ist lokale $F_\infty$-Existenz, noch kein vollstaendiger
   Horizonttransfer. LCG-Arnoldi- und Trajektorienadapter bestehen nun
   targetfrei; dabei wurden Instabilitaet auf dasselbe gematchte Ritzpaar
   verschaerft und Fortsetzungen fail-closed hinter Panelchecks gelegt. Eine
   erste Aenderung am historisch eingefrorenen Stabilitaetskern wurde durch
   dessen CI-Blob-Sperren falsifiziert; der korrigierte G5-Kern ist nun
   getrennt, waehrend der Altblob exakt erhalten bleibt. Der gemeinsame
   Grundgleichungs-Preflight ist nun targetfrei implementiert und erzeugt
   einen hashbaren Record fuer Gewichtssumme, native Kreiskovarianz,
   Fixpunkt, Voll-Jacobian und Symmetrien. Der eingefrorene isolierte
   G5-Ergebnisvertrag, seine fail-closed Backendkomposition sowie ein
   standardbibliotheksbasierter Record-/Publikationsauditor bestehen nun
   targetfrei. Attempt 1 erreichte nach Root und Preflight die Arnoldi-Panels,
   scheiterte aber vor Publikation an einem ungeclippten binary64-Overlap
   ausserhalb des exakten Intervalls $[0,1]$. Es existiert kein G5-Ergebnis;
   der Versuch ist verbraucht und kein Retry autorisiert. Die
   Overlap-Recordgrenze ist inzwischen mit dimensionsskalierter
   binary64-Kanonisierung und Falsifikationstests targetfrei remediiert. Als
   prospektive Attempt-2-Protokoll und das neue Readinessreview bestanden
   targetfrei. Attempt 2 erreichte die nichtlinearen Fortsetzungen, scheiterte
   aber vor Publikation: Der Integrator bildet das Maximum ueber jeden Schritt,
   waehrend der Validator es aus dem Zehnersampling rekonstruiert. Das ist ein
   zweiter Pipeline-Incident, kein G5-Befund. Attempt 2 ist verbraucht; kein
   Attempt 3 war nicht automatisch autorisiert. Die Vollschrittspur ist nun
   targetfrei rekonstruktiv validiert; 1145 Tests, Lint und Docs bestehen. Das
   Readinessreview erlaubt nach expliziter Nutzerfreigabe genau einen
   Governance-only-Autorisierungscommit und einen Attempt-3-Lauf. Bis zu diesem
   Commit bleibt das Target geschlossen. G5, vollstaendiger Horizontlauf und
   P5-D-Versuch 4 bleiben ungemessen.
2. **Paper I konsolidieren -- nach 1.** Modellkern, skalare Evidenz,
   Rotating-wave-Ast und Abgrenzungen in der Sprache von $q$, $g$, $H$,
   $B_H$, $c$ und $\mu$ zusammenfuehren. Zulaessig sind nur lokal oder
   kontrolliert belegte Existenz-, Stabilitaets-, Skalierungs- und
   Center-Port-Aussagen; interne Phase, physikalische Masse und Interaktion
   bleiben getrennte Hypothesen.
3. **Vorbereiteten Orbit und gebildeten Knoten trennen -- nach 2.** Festlegen,
   ob Paper I ueberhaupt einen Formationsclaim benoetigt. Erst dann darf ein
   gepaartes Formation-/KnotScore-Protokoll fuer den Rotating-wave-FIFO
   entstehen. Ein Score auf einer vorbereiteten exakten Kreisgeschichte ohne
   `eta_zero`- und Formationskontrolle waere nicht entscheidend und wird nicht
   nachgetragen.
4. **Zertifikats- und Release-Hardening -- nach 1, parallel zu 2/3.** Einen
   zweiten unabhaengigen Intervallbackend, reproduzierbare Dependency-Hashes,
   `CITATION.cff` und eine zitierbare Release vorbereiten. Diese Punkte
   erhoehen Pruefbarkeit, ersetzen aber kein wissenschaftliches Gate.
5. **Interaktionsprogramm neu autorisieren -- erst nach 1.** P5-D bleibt
   `inconclusive`. Ein weiterer Ziellauf braucht ein separates
   outcome-blindes Protokoll, eine neue explizite Freigabe und einen sauberen
   Readiness-Commit. Vorher ist nur targetfreie Methodenarbeit erlaubt.
6. **Repository fortlaufend kuratieren -- bei jedem abgeschlossenen Block.**
   Aktive Seiten auf hoechstens sieben gleichrangige Elemente begrenzen,
   historische Detailregister ins Archiv verschieben, Standardbibliotheken
   erweitern statt Runnerlogik zu duplizieren und Status/Claims nach jedem
   Review synchronisieren.

## Aktueller Haltepunkt

Der isolierte G4-Komponentenblock ist mit unabhaengig auditiertem lokalem
Pass abgeschlossen; G5-Adapter und Grundgleichungs-Preflight sind targetfrei
reviewed. Ergebnisvertrag, Backendkomposition, persistierter Preflight und
unabhaengiger Auditor sowie der Execution-Context-Guard sind targetfrei
implementiert und reviewed. G5-Attempts 1 und 2 sind als getrennte
Pipeline-Incidents ohne Ergebnis verbraucht. Attempt 2 falsifizierte die
Trajektorien-Vertragsabdeckung; die dichte, rekonstruktive Recordsemantik ist
nun targetfrei reviewed und CI-gruen. Attempt 3 bleibt bis zum separaten
Governance-only-Commit technisch geschlossen. Der aktuelle
methodische Stand und die Evidenzgrenzen stehen im
[Experimentkatalog](../reference/experiment_catalog.md).
