# Projektprioritaeten

Stand: 2026-09-09.

Dies ist die einzige aktive Prioritaetenliste des Repositorys. Statusseiten,
README und Reports duerfen Befunde oder Blocker nennen, aber keine zweite
Arbeitsreihenfolge fuehren. Der fruehere Verlauf ist im
[Repository-Archiv](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/docs/archive/status/project_priorities_through_2026-09-02.md)
erhalten.

## Voraussetzungen

P4-R-S bleibt `p4rs-anchor-scale-transfer-pass`, N0 bleibt
`n0-noise-stability-window-bracketed-reviewed-pass`, und das targetfreie
P5-Design bleibt `p5d-mutual-center-design-identifiable`. Diese Befunde
autorisieren keinen weiteren P5-Ziellauf.

## Eine Reihenfolge

1. **Notationsvertrag in die Remediation einfrieren.** Aktive Gleichungen auf
   die Paper-I-Grundsprache zurueckfuehren; mehrdeutige Code-/Schemafelder nur
   versioniert und mit Kompatibilitaetstests migrieren. Grundlage sind das
   [Modellvokabular](../reference/model_vocabulary.md) und der targetfreie
   Vokabularaudit. Kein Targetzugriff.
2. **P5-D Ergebnisstrecke schliessen und spezifizieren.** Der Code-Review ist
   als Blockerbasis eingefroren. Das neue targetfreie
   [Remediation-Protokoll](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/reports/project/meta/preregistration/scalar_memory_loop_p5d_runner_remediation_protocol_2026-09-03.md)
   spezifiziert exakte Payload-Schemata, fail-closed Typ-/Endlichkeitspruefung,
   Manifest-gebundene Ausgabesemantik und einen maschinenlesbaren
   Governancezustand. Das separate Review forderte exakt registrierte Pfade,
   ein getracktes Schema, einen fest konstruierten CI-Endpunkt und
   Manifestpruefung im Auditor; diese Punkte sind prospektiv amendiert und im
   separaten Suffizienzreview geschlossen. Damit darf nur Schritt 3 beginnen.
   Kein Targetzugriff.
3. **Remediation getrennt implementieren und adversarial testen.** Erst Tests
   fuer Off-Arme, nichtendliche NumPy-Skalare, unavailable response, zweiten
   Rename-Fehler, Commit-/CI-Bindung und Vokabularschema schreiben; dann
   minimal reparieren. Der erste kleine Schritt ist umgesetzt: ein getrackter
   geschlossener Governance-Datensatz bindet beide Incidents, und der Runner
   erzwingt ihn vor der alten Provenienzstrecke und vor jedem Targetzugriff.
   Die targetfreie Implementierung ist lokal abgeschlossen: `null` besitzt
   eine exakte Off-Arm-Semantik, unbekannte Typen schliessen fail-closed, das
   v2-Schema registriert die Produktionsstruktur, das Publikationsmanifest
   wird zuletzt geschrieben und die Lease bindet geschuetzte Blobs sowie
   offizielle CI-Metadaten. Injektions- und Vollpaneltests sind gruen. Das
   exakte Port-Nullmodell ist als Relaxation erster Ordnung festgehalten; ein
   gekoppelter harmonischer Oszillator bleibt ein nachgelagertes
   Diskriminationsgate und wird nicht in das eingefrorene P5-D-Estimand
   hineindefiniert. Naechster Schritt ist ausschliesslich Schritt 4.
4. **Unabhaengiges Readiness-Review und Versuch 3 abschliessen.** Produktionsschema lokal vollstaendig
   erzeugen und serialisieren, Ausgabeausfall injizieren und den geschlossenen
   Status technisch pruefen. Das Review ist mit
   `p5d-runner-ready-target-still-closed` abgeschlossen. Der danach einmalig
   autorisierte Versuch 3 scheiterte nach vollstaendiger In-memory-Auswertung
   vor Publikation an produktionsseitigen `numpy.float64`-Nullquotienten im
   strikten Schema. Das Receipt verbraucht die Freigabe; Ergebnis und Manifest
   fehlen. Der Incident falsifiziert die Readiness-Abdeckung und schliesst
   Targetzugriff erneut. Er autorisiert weder Patch noch Versuch 4.
5. **P5-D-Produktionspfad targetfrei beweisen.** Incident 3 ist dauerhaft als
   `p5d-inconclusive` dokumentiert. Das neue outcome-blinde
   [Produktionspfad-Protokoll](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/reports/project/meta/preregistration/scalar_memory_loop_p5d_production_path_preflight_protocol_2026-09-06.md)
   wurde nach negativem Erstreview amendiert und im separaten
   [Suffizienzreview](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/reports/project/meta/reviews/scalar_memory_loop_p5d_production_path_preflight_protocol_sufficiency_review_2026-09-06.md)
   als `p5d-production-preflight-protocol-sufficient-target-closed` bewertet.
   Die zunaechst roten, target-gesperrten Tests und die kleinste P5-lokale
   Typgrenzenkorrektur sind implementiert; das separate
   [Readinessreview](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/reports/project/meta/reviews/scalar_memory_loop_p5d_production_path_readiness_review_2026-09-07.md)
   endet nach 945 lokalen Tests und gruener Implementierungs-CI mit
   `p5d-production-boundary-ready-target-closed-horizon-transfer-required`.
   Python-Standardbibliothek traegt Vertrag, Hashes und Publikation; NumPy
   bleibt in der Numerik. Eine gemeinsame Projektbibliothek setzt erst drei
   nachweislich semantikgleiche Pipelines voraus. Die Grundgleichungen und 41
   wissenschaftlichen Runner-Symbole blieben eingefroren. Das im
   [Finite-H-Audit](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/reports/project/meta/reviews/scalar_memory_finite_h_non_tautology_audit_2026-09-07.md)
   geforderte Horizont-Transfergate ist nun im
   [Fixed-alpha-Protokoll](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/reports/project/meta/preregistration/scalar_memory_rotating_wave_horizon_transfer_protocol_2026-09-08.md)
   eingefroren, nach negativem Review amendiert und im separaten
   [Suffizienzreview](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/reports/project/meta/reviews/scalar_memory_rotating_wave_horizon_transfer_protocol_sufficiency_review_2026-09-08.md)
   als `rotating-wave-horizon-transfer-protocol-sufficient-implementation-closed`
   bewertet. Der FIFO erzwingt keinen Kreis, aber die bisherige
   $H\alpha=12$-Leiter beweist auch keinen festen-$\alpha$-Grenzwert
   $H\to\infty$. Ergebnisvertrag und RED-Tests wurden vor der targetfreien
   Implementierung committed. Das
   [Infrastrukturreview](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/reports/project/meta/reviews/scalar_memory_rotating_wave_horizon_transfer_contract_infrastructure_review_2026-09-08.md)
   bindet 40 fokussierte, 985 gesamte Tests und gruene CI mit Verdict
   `rotating-wave-horizon-transfer-contract-infrastructure-pass-runner-incomplete-horizon-run-closed`.
   Ein spaeteres Negativreview fand unabbildbare fruehe Abbrueche; v2 schloss
   deren Nullsemantik. Das naechste Negativreview fand noch nicht
   rekonstruierbare positive Zertifikats-, Spektral- und
   Trajektorienbeziehungen. v3 schliesst sie. Seine erste Linux-CI
   falsifizierte native `sin`-/`cos`-Starts als plattformunabhaengig; eine vor
   jedem Zielzugriff amendierte 32-bit-LCG ersetzt sie portabel. Das
   [v3-Vertragsreview](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/reports/project/meta/reviews/scalar_memory_rotating_wave_horizon_transfer_contract_v3_review_2026-09-09.md)
   bindet 59 fokussierte, 1004 gesamte Tests und gruene exakte Linux-CI mit
   Verdict
   `rotating-wave-horizon-transfer-contract-v3-pass-runner-red-open-target-closed`.
   Die pure Runner-Orchestrierung besteht inzwischen Reihenfolge-, Rootstopp-,
   Homotopiestopp-, Tail-, Arnoldi- und Trajektorien-Falsifikatoren. Ein dabei
   gefundener Halbblatt-Counterexample korrigierte das v3-Review: Validator
   und Auditor beweisen nun die dyadische Ausschlusspartition und verwerfen
   den Widerspruch zu einem vorhandenen Zielroot. Das
   [Orchestrierungsreview](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/reports/project/meta/reviews/scalar_memory_rotating_wave_horizon_transfer_runner_orchestration_review_2026-09-09.md)
   bindet 70 fokussierte, 1015 gesamte Tests und gruene exakte Linux-CI mit
   Verdict
   `rotating-wave-horizon-orchestration-pass-scientific-backends-incomplete-target-closed`.
   Der anschliessende
   [Katalog-/Backend-Audit](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/reports/project/meta/reviews/scalar_memory_rotating_wave_horizon_backend_reuse_audit_2026-09-09.md)
   zeigt, dass finite
   Residuen/Jacobians, Punkt-Newton, lokale Krawczyk-Boxen,
   Voll-FIFO-Jacobian und Quotientdistanz bereits als Bibliothekskerne
   vorliegen. Der schmale v3-Rootadapter verwendet diese Kerne fuer die feste
   Acht-Schritt-Newtonfolge und beide Krawczyk-Boxen. Homotopieschlauch und
   gemeinsamer Intervallauswerter sind ebenfalls targetfrei implementiert:
   volle outward-rounded Parameterscheiben, exakt 64 Scheiben, strikter
   Einschluss, Nachbarueberlappung und fail-closed Praefixstopps. Das
   [Homotopie-/Intervallreview](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/reports/project/meta/reviews/scalar_memory_rotating_wave_horizon_homotopy_interval_review_2026-09-09.md)
   bindet 1029 gruene CI-Tests, aber keine ausgewertete Horizontkante. Der
   anschliessende
   [lokale Ausschlussadapter](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/reports/project/meta/reviews/scalar_memory_rotating_wave_horizon_local_exclusion_review_2026-09-09.md)
   verwendet exakt denselben Intervallkern und die vorregistrierte
   normalisierte FIFO-Teilung bis Tiefe 20; keine registrierte Domain wurde
   ausgewertet, seine CI besteht 1038 Tests. Naechster Schritt ist das
   tail-augmentierte Zertifikat;
   danach folgen LCG-Arnoldi, Trajektorienabbildung und Backendkomposition.
   Kein historischer
   Ergebnisrecord darf als neue Evidenz kopiert werden. Noch kein
   Horizontlauf und kein Versuch 4.
6. **Paper I konsolidieren.** Modellkern, skalare Evidenz, Rotationsast und die
   P5-Abgrenzung in einheitlicher Papersprache zusammenfuehren, ohne
   Interaktions-, Spin-, Traegheits- oder Masseclaim.
7. **Zertifikats- und Release-Hardening.** Zweiten Intervallbackend,
   Wheel-/Hash-Lock, `CITATION.cff` und eine zitierbare Release parallel
   abschliessen; sie ersetzen kein wissenschaftliches Gate.

## Laufstatus

**P5-D Versuch 3 technisch inconclusive: Pipeline geschlossen.**

Erstaufruf und Ersatzlauf endeten vor einer auswertbaren Payload an
NumPy-Bool beziehungsweise nichtendlichem Off-Sentinel. Der prospektiv
autorisierte Versuch 3 endete nach vollstaendiger In-memory-Auswertung am
strikten Typvertrag fuer sechs produktionsspezifische NumPy-Float-Nullen. Alle
drei Aufrufe sind Infrastrukturereignisse, keine negativen
Interaktionsexperimente. Die Attempt-3-Lease ist verbraucht.
