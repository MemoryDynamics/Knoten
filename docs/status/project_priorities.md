# Projektprioritaeten

Stand: 2026-09-05.

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
5. **Incident 3 reviewen und eine neue Remediation erst prospektiv entscheiden.**
   Zuerst den Typursprung, die Testluecke und die verlorene
   In-memory-Entscheidung dauerhaft als `p5d-inconclusive` festhalten. Falls
   P5-D fortgesetzt werden soll, braucht jede Codeaenderung zuvor ein neues,
   outcome-blindes Protokoll mit exakter produktionspfadnaher Off-Arm-Probe.
   Ohne diesen separaten Freeze direkt zu Schritt 6 gehen.
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
