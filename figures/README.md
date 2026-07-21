# Abbildungs-Index

Stand: 2026-07-21.

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
- `draft/kernels/nonlinearity_2026-07-19/`: feste-`g`-Nichtlinearitaets- und
  Skalenpruefung.
- `draft/memory/low_mode_identity_audit_2026-07-20.png`: negatives
  Mode-Identity-Gate.
- `draft/response/one_way_interaction_age_N3M_2026-07-21.png`: Translation
  ohne kontrollgetrennte Shape-Dynamik.

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
