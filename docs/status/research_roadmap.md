# Forschungsroadmap

Stand: 2026-10-21. Grobe, schrittweise zu verfeinernde Zielarchitektur.
Die Ausfuehrungsreihenfolge steht ausschliesslich in den
[Projektprioritaeten](project_priorities.md).

## Ziel und Status

Langfristige Forschungsfrage: Kann eine gemeinsame Mikrodynamik eine
effektive Beschreibung tragen, die sowohl Gravitation als auch die
Quantenfelder und Wechselwirkungen des Standardmodells reproduziert?
Das ist eine Hypothese des Programms, kein durch bisherige Ergebnisse
gestuetztes Erfolgsversprechen. Eine GUT im engeren Sinn betrifft die
Vereinigung der starken und elektroschwachen Wechselwirkungen; das Ziel
einschliesslich Gravitation geht darueber hinaus.

Der gepruefte skalare Zweig liefert eine klassische Relaxationsbaseline.
Der separate FIFO-Zweig liefert lokale Existenz- und Stabilitaetsbefunde
vorbereiteter Rotation. Weder Zweig etabliert derzeit Quantenmechanik,
relativistische Gravitation oder Standardmodellteilchen. Nahe Literatur
ist Ausgangswissen, kein Beleg fuer diese weitergehenden Verbindungen.

## Stufen und Entscheidungspunkte

Die Stufen beschreiben Abhaengigkeiten, keine zugesicherte Erfolgsfolge.
Die Quanten-Machbarkeit wird bereits in R0 geprueft.

| Stufe | Frage und gefordertes Ergebnis | Status / Entscheidungspunkt |
| --- | --- | --- |
| R0: Annahmen und Machbarkeit | Was ist eingebaut, was abgeleitet, was fehlt? Gemeinsame Matrix fuer Freiheitsgrade, Lokalitaet und Quantenfaehigkeit. | Begrenzter [Audit](../reference/foundation_feasibility.md) abgeschlossen: bedingte Grenzen und Gegenargumente dokumentiert, kein allgemeines Go oder No-go. |
| R1: Kontrolliertes Minimalmodell | Definierte Dynamik, reproduzierbare Observablen, bekannte Grenzfaelle und Grenzen. Nichtlineare Struktur von linearer Relaxation unterscheiden. | Paper 0/I liefern Teile; FIFO ergaenzt einen separaten nichtlinearen Ast. Publikationsneuheit und fundamentale Relevanz getrennt bewerten. |
| R2: Gemeinsame effektive Beschreibung | Langlebige Freiheitsgrade nach Symmetriereduktion; abgeleitete Bewegung, Kopplungen und Erhaltung bzw. Bilanzierung. Gueltigkeit unter Skalenwechsel testen. | Offen. [B1](../reference/operational_contract.md) spezifiziert die vorhandene klassische Quellenantwort; die physikalische Wahl oder Herleitung eines Mehrsystem-/Messgesetzes fehlt. Eine Erweiterung braucht eine Richtungsentscheidung. Ein erweiterter Zustand oder Fit allein ist keine geschlossene effektive Theorie. |
| R3: Relativistische und quantenmechanische Verbindungen | Gemeinsame Propagationsstruktur und Kontrolle eines bevorzugten Bezugsrahmens; separat eine konsistente Quanten-/Messbeschreibung mit nichtklassischen Korrelationen. | Beide Verbindungen offen und frueh auf Vertraeglichkeit zu pruefen. Ein Lichtkegel beweist weder Lorentz-Invarianz der ganzen Dynamik noch Quantisierung. |
| R4: Gravitation und Standardmodell | Gravitation: dynamische Geometrie, universelle Kopplung und kontrollierter Einstein-Grenzfall. Standardmodell: passende Eichstruktur, chirale Fermionen, Statistik und konsistente Wechselwirkungen. | Langfristige Ziele fuer II/III. Symmetrienamen oder attraktive Kraefte genuegen nicht. Klassische Gravitationstests brauchen nicht vorab eine vollstaendige Quantentheorie. |
| R5: Gemeinsame Physik und Vorhersagen | Beide Sektoren aus kompatiblen Annahmen und demselben Skalengrenzfall verbinden; unabhaengige quantitative Vorhersagen gegen Beobachtungen pruefen. | Noch keine belastbare Route. Widerspruechliche Annahmen zwischen II und III schliessen eine gemeinsame Herleitung aus, auch wenn Einzelanalogien funktionieren. |

## Rollen der Paper

- **Paper 0:** mathematische Definitionen und technische Voraussetzungen.
- **Paper I:** geprueftes Minimalmodell, Literaturvergleich, Baseline und
  Grenzen. Sein Nutzen setzt keine PRE-Annahme voraus; eine Einreichung
  braucht dennoch einen eigenstaendigen wissenschaftlichen Beitrag.
- **FIFO-Paper:** eigener nichtlinearer Ast mit getrennten Aussagen zu
  vorbereiteter Existenz, Stabilitaet, Horizonttransfer und Formation.
- **Paper-II-Programm:** zuerst Propagation und Kinematik; die eigentliche
  Gravitationsdynamik bleibt eine zusaetzliche offene Aufgabe.
- **Paper-III-Programm:** zuerst Quanten-Machbarkeit und geeignete effektive
  Freiheitsgrade; erst danach Standardmodellstruktur. Synchronisation
  allein ersetzt keine dieser Herleitungen.

Paper-Nummern legen keine starre Forschungsreihenfolge fest. II und III
muessen kompatible Annahmen und eine gemeinsame effektive Grundlage nutzen.
Ob weitere Paper noetig sind, entscheidet der tatsaechliche Befund.

Der naechste Arbeitsabschnitt konkretisiert nur den ersten offenen
Uebergang. B1 fuehrt zur [Architekturentscheidung](architecture_decision.md); Paper I
bleibt daneben ein eigenstaendiger Publikationsstrang. Die spaeteren Stufen
bleiben grob, bis ein belastbares Ergebnis ihre Verfeinerung rechtfertigt.

## Leitplanken

Raum, euklidische Abstandsmessung, Update-Reihenfolge, Rauschgesetz und Kernel
sind im Minimalmodell Inputs. Eine effektive Geometrie muss gegen diese
Inputs abgegrenzt werden. Niedriger Rang in einem Fenster oder eine in 3D
kompakte Wolke beweist keine Dimensionsemergenz.

Exponentielles Gedaechtnis erzeugt allein keine harte kausale Schranke bei
direkter Fernkopplung. Gedaechtnis hebt auch Bell-/Clauser-Horne-Schranken
nicht automatisch auf: Unter lokaler Faktorisierung und messwahlunabhaengiger
Zustandsverteilung bleibt der erweiterte klassische Zustand beschraenkt.
Eine alternative Architektur muss ihre abweichenden Annahmen und
beobachtbare Signallokalitaet erklaeren. Das ist ein Pruefauftrag, kein
pauschaler Unmoeglichkeitssatz fuer alle denkbaren Erweiterungen.

Fuer jeden konkretisierten Uebergang werden fuenf Punkte ergaenzt:
Inputannahmen, benoetigte Aussage, kleinster entscheidender Test oder Beweis,
Gegenbefund/Abbruchkriterium und naechste Entscheidung. Ein negatives
Ergebnis darf den Pfad beenden; es fuehrt nicht automatisch zu Parameter-
oder Modellanpassung. Neue Modellregeln und groessere Simulationsprogramme
gehen zur Richtungsentscheidung an den Autor. Bestehende Ausfuehrungssperren
bleiben bestehen.

## Pflege und Quellen

Nach jedem wissenschaftlichen Abschluss werden nur betroffene Stufen
aktualisiert: belegt, bedingt, offen oder im untersuchten Bereich widerlegt,
jeweils mit Evidenzlink und Geltungsbereich. Keine Prozentzahl fuer den
Fortschritt zur Weltformel und keine Termine fuer ungesicherte Durchbrueche.
Technische Reparaturen aendern den Forschungsstatus nicht.

Projektbasis: [Claim-Register](paper_claims.md),
[aktueller Stand](current_status.md),
[PRE-Neuheitsaudit](https://github.com/MemoryDynamics/Knoten/blob/b43fc11af4dcda82058a64e0d2e0e013c9aba585/paper/paper_i/research/pre_reassessment_2026-10-19.md).
Physikalische Referenzpunkte: [PDG: Grand Unified Theories](https://pdg.lbl.gov/2023/reviews/rpp2023-rev-guts.pdf),
[Clauser und Horne (1974)](https://journals.aps.org/prd/abstract/10.1103/PhysRevD.10.526).
Diese Quellen belegen Anforderungen und Vergleichsrahmen, nicht die
Tragfaehigkeit unseres Ansatzes.
