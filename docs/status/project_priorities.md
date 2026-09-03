# Projektprioritaeten

Stand: 2026-09-03.

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
   minimal reparieren.
4. **Unabhaengiges Readiness-Review.** Produktionsschema lokal vollstaendig
   erzeugen und serialisieren, Ausgabeausfall injizieren und den geschlossenen
   Status technisch pruefen. Ein neuer Prospektivlauf benoetigt danach eine
   neue ausdrueckliche Autorisierung; die P5-D-Recovery bleibt abgeschlossen
   und die bisherige Pipeline geschlossen.
5. **Paper I konsolidieren.** Modellkern, skalare Evidenz, Rotationsast und die
   P5-Abgrenzung in einheitlicher Papersprache zusammenfuehren, ohne
   Interaktions-, Spin-, Traegheits- oder Masseclaim.
6. **Zertifikats- und Release-Hardening.** Zweiten Intervallbackend,
   Wheel-/Hash-Lock, `CITATION.cff` und eine zitierbare Release parallel
   abschliessen; sie ersetzen kein wissenschaftliches Gate.

## Laufstatus

**P5-D-Recovery abgeschlossen: Pipeline geschlossen.**

`P5 first target -> serializer inconclusive`; der autorisierte Ersatzlauf
endete ebenfalls vor einer auswertbaren Payload an nichtendlichen Werten.
Beide Aufrufe sind Infrastrukturereignisse, keine negativen
Interaktionsexperimente.
