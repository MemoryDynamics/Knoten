# Abbildungs-Index

Stand: 2026-07-28.

Abbildungen sind Darstellungen von Evidenz, nicht eigenstaendige Evidenz. Die
zugehoerige Hypothese, Kontrolle, Seedbasis und Claim-Grenze stehen im Report.

## Verzeichnisrollen

- `draft/`: reviewed oder historische Analyseabbildungen. Der Name bedeutet
  nicht automatisch `unreliable`, aber diese Dateien sind keine freigegebenen
  Paperfiguren.
- `paper/`: kanonische, von Paperquellen referenzierte Abbildungen.
- `external/`: kuratierte Kommunikationsvisuals; wissenschaftliche Aussagen
  muessen auf Reports oder Paper zurueckverweisen.

## Aktuelle Entscheidungsgrafiken

- `draft/kernels/core_2026-07-19/`: gematchter Kernel-Familienvergleich.
- `draft/kernels/core_2026-07-28/`: curvature-matched LoG-/Taylor-Vergleich
  mit lokaler Kraft und kumuliertem Kernelintegral.
- `draft/kernels/nonlinearity_2026-07-19/`: feste-`g`-Nichtlinearitaets- und
  Skalenpruefung.
- `draft/memory/low_mode_identity_audit_2026-07-20.png`: negatives
  Mode-Identity-Gate.
- `draft/response/one_way_interaction_age_N3M_2026-07-21.png`: Translation
  ohne kontrollgetrennte Shape-Dynamik.
- `draft/response/scalar_cross_readout_resolution_2026-07-21.png`: negatives
  statisches Skalar-Shape-Readout-Gate.
- `draft/response/oriented_history_current_audit_2026-07-21.png`: negatives
  Polar-/Bivektor-Gate gegen konditionale Vorzeichen-Nullen.
- `draft/response/oriented_vector_one_way_gate_2026-07-25.png`: 6/6-
  Pass des konstruierten persistenten Vektorkanals gegen Random-Sign- und
  Ein-Schritt-Kontrollen; keine Propagations- oder Teilchenevidenz.
- `draft/response/local_oriented_mediator_gate_2026-07-28.png`: beide
  eingesetzten lokalen Mediatorarchitekturen bestehen ihre Holdout-Gates;
  die Transportregel bleibt Modellinput.
- `draft/response/oriented_source_mediator_identifiability_2026-07-28.png`:
  6/6 autonome Sources sind spektral geeignet, die beiden Regeln zu trennen;
  nahezu gleicher Ein-Schritt-Kontrast zeigt keine Persistenzspezifitaet.
- `draft/response/dynamic_common_source_mediator_gate_2026-07-28.png`:
  Beide lokale Regeln erzeugen messbare, shape-bounded und abschwaechende
  Antworten, aber nur 4/6 Paare bestehen die vorregistrierte Modelltrennung
  gleichzeitig an allen drei Distanzen; negatives Diskriminationsgate, keine
  Feldgesetz-Auswahl.


Der kanonische Reportpfad fuer diese Entscheidungen steht in
`reports/README.md`.

## Aufnahmeregeln

- Keine Abbildung ohne erzeugendes Skript oder dokumentierte Provenienz.
- Keine handselektierten Best-Seed-Plots als primaere Evidenz.
- Achsen, Einheiten, Condition und Aggregation muessen lesbar sein.
- Bei gepaarten Tests aktive, freie und deaktivierte Kontrollen gemeinsam
  darstellen.
- Ersetzte Grafiken entweder im datierten historischen Ordner belassen oder
  zusammen mit ihrer Einordnung entfernen; keine unmarkierten `copy`-,
  `final2`- oder `latest`-Dateien.
- Paperfiguren werden bewusst kopiert, wenn ein selbstenthaltener LaTeX-Build
  dies erfordert. Solche inhaltlich identischen Kopien sind beabsichtigt und
  keine zweite Evidenzquelle.
