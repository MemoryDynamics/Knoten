# Eine konkrete Frage mitprüfen

[English version](https://github.com/MemoryDynamics/Knoten/blob/main/docs/outreach/contribute_review_en.md)

Stand: 2026-10-19. Diese Seite ist eine Einladung zur Diskussion und keine
zweite wissenschaftliche Prioritätenliste. Die verbindliche Reihenfolge
steht in den
[Projektprioritäten](https://github.com/MemoryDynamics/Knoten/blob/main/docs/status/project_priorities.md).
Die folgenden Einstiege betreffen vorhandene Quellen und Befunde. Sie
autorisieren keine weiteren gesperrten Zielauswertungen.

## Worum es geht

Memory Dynamics untersucht diskrete Dynamik mit relaxierendem Gedächtnis.
Projektwebsite: [MemoryDynamics.org](https://memorydynamics.org/).
Persönliche Motivation und eine mögliche spätere physikalische Deutung sind
von den geprüften Modellresultaten zu trennen. Ein Weltformel-, Teilchen-,
Masse-, Ladungs- oder Spin-Nachweis liegt nicht vor. Den zugänglichen
Hintergrund erzählen der
[deutsche Artikel](https://medium.com/@haukeh/ein-traum-von-knoten-9232412d4ff8)
und seine
[englische Fassung](https://github.com/MemoryDynamics/Knoten/blob/main/docs/outreach/medium_draft_en.md).
Die neuronale Deutung des Traums und ein möglicher KI-Nutzen bleiben
Hypothesen; die bisherigen Modellbefunde belegen weder Gehirnfunktionen
noch Lernfähigkeit.

Du musst weder die Grundidee teilen noch das ganze Repository lesen.
Eine einzelne überprüfbare Kritik oder Reproduktion genügt. Die unten
verlinkte Quellrevision ist eingefroren, damit sich die Review-Frage nicht
während der Prüfung verschiebt.

## Drei begrenzte Einstiege

| Einstieg | Konkrete Frage | Quellen an Revision `35ae7b0` | Hilfreiches Ergebnis |
| --- | --- | --- | --- |
| Herleitung | Folgt die endliche Kreisbalance aus der implementierten Gedächtnisdynamik, ohne Kreisgeometrie durch die Speicherstruktur vorauszusetzen? | [Implementierte Gleichungen](https://github.com/MemoryDynamics/Knoten/blob/35ae7b0eb7d7bb8cc57eaa2c2af80b32d955fb4f/docs/reference/implemented_equations.md), [Kreisreduktion](https://github.com/MemoryDynamics/Knoten/blob/35ae7b0eb7d7bb8cc57eaa2c2af80b32d955fb4f/docs/reference/rotating_wave_foundation.md) | Nachvollziehbare Ableitung oder ein konkreter widersprechender Term, Index oder Spezialfall. |
| Stabilitätsbefund | Tragen die gespeicherten G5-Daten den begrenzten lokalen numerischen Stabilitätsclaim? Welche alternative Erklärung bleibt offen? | [Ergebnis](https://github.com/MemoryDynamics/Knoten/blob/35ae7b0eb7d7bb8cc57eaa2c2af80b32d955fb4f/reports/dynamics/rotation/scalar_memory_rotating_wave_horizon_g5_component_attempt_3_2026-09-17.md), [Ergebnisreview](https://github.com/MemoryDynamics/Knoten/blob/35ae7b0eb7d7bb8cc57eaa2c2af80b32d955fb4f/reports/project/meta/reviews/scalar_memory_rotating_wave_horizon_g5_component_attempt_3_result_review_2026-09-17.md), [Portabilitätsgrenze](https://github.com/MemoryDynamics/Knoten/blob/35ae7b0eb7d7bb8cc57eaa2c2af80b32d955fb4f/reports/project/meta/reviews/scalar_memory_rotating_wave_horizon_g5_premerge_referee_review_2026-09-17.md) | Prüfung einer ausgewählten gespeicherten Relation mit Methode und Umgebung; Recordprüfung, numerische Reproduktion und Stabilitätsbeweis ausdrücklich unterscheiden. |
| Gegenmodell und Claim-Grenze | Welcher anschauliche Befund ist bereits durch lineare Relaxation oder vorbereitete Anfangsgeschichte erklärt? Wird irgendwo mehr behauptet, als die Daten tragen? | [Status](https://github.com/MemoryDynamics/Knoten/blob/35ae7b0eb7d7bb8cc57eaa2c2af80b32d955fb4f/docs/status/current_status.md), [Claim-Register](https://github.com/MemoryDynamics/Knoten/blob/35ae7b0eb7d7bb8cc57eaa2c2af80b32d955fb4f/docs/status/paper_claims.md) | Genaue Textstelle, einfachere Erklärung und gegebenenfalls ein unterscheidender Testvorschlag mit vorab benannter Widerlegung. |

Bei G5 sind Artefakthashes plattformunabhängig prüfbar. Der bitgenaue
semantische Audit des historischen Records hat eine dokumentierte
Plattformgrenze. Ein entsprechender Unterschied ist zunächst zu untersuchen
und weder automatisch ein neuer wissenschaftlicher Fehler noch ein Pass.
Interne Reviews und KI-gestützte Kontrollen ersetzen keine unabhängige
externe Replikation.

## Eine Rückmeldung festhalten

Nutze die
[Review-Vorlage für ein GitHub-Issue](https://github.com/MemoryDynamics/Knoten/issues/new?template=focused_review.md).
Die Vorlage fragt nach Behauptung und Quellrevision, Methode, beobachtetem
Ergebnis, Interpretation und verbleibenden Grenzen. Berichte auch negative
oder unvollständige Ergebnisse. Fehlende Prüfung ist kein bestandener Test.

Beschränke einen Beitrag möglichst auf eine Frage. Wenn sie beantwortet ist,
kann der Beitrag als abgegrenzt abgeschlossen gelten; daraus entsteht keine
Erwartung, das gesamte Projekt zu übernehmen. Vorschläge für neue Experimente
bleiben Vorschläge, bis sie in die bestehende Projektsteuerung eingeordnet
sind.

## Veröffentlichungen und Quellen

Der
[deutsche Artikel](https://medium.com/@haukeh/ein-traum-von-knoten-9232412d4ff8)
ist seit dem 19. Oktober 2026 frei lesbar auf Medium veröffentlicht.
Die [Quellfassung](https://github.com/MemoryDynamics/Knoten/blob/main/docs/outreach/medium_entwurf.md)
bleibt auf GitHub. Die englische Fassung ist weiterhin ein Entwurf.
Der Artikel ist kein begutachteter Fachartikel; der Sol6.1-Hinweis steht am
Anfang. Medium beschreibt den
[Import eines vorhandenen Artikels](https://help.medium.com/hc/en-us/articles/214550207-Importing-a-post-to-Medium)
und das
[Setzen eines Canonical-Links](https://help.medium.com/hc/en-us/articles/360033930293-Set-a-canonical-link);
alternativ lässt sich der Text manuell übernehmen.

Die Verbindung offener Materialien, Vorregistrierung und transparenter
Bewertung entspricht dem vom Center for Open Science beschriebenen
[Open-Science-Ansatz](https://www.cos.io/open-science). Ob dieser konkrete
Aufruf zusätzliche Mitwirkende erreicht, ist offen. Künftige eng begrenzte
Fachveröffentlichungen bleiben möglich.
