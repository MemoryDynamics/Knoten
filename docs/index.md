# Memory Dynamics

Projektwebsite: [MemoryDynamics.org](https://memorydynamics.org/).

Stand: 2026-09-05.

Diese Seite ist die kurze Frontdoor. Die Navigation folgt der Projektregel:
hoechstens sieben Eintraege je Ebene und hoechstens sieben Ebenen. Historische
Zwischenstaende bleiben im Archiv, steuern die Arbeit aber nicht mehr.

## Persoenlicher Einstieg und offene Diskussion

Ergaenzt am 2026-10-19: Der
[Medium-Artikel auf Deutsch](https://medium.com/@haukeh/ein-traum-von-knoten-9232412d4ff8)
und die
[englische Fassung auf Medium](https://medium.com/@haukeh/a-dream-of-knots-177de95c35fe)
erzaehlen den Traum, den Weg zum Modell und die wissenschaftlichen Grenzen.
Beide Fassungen sind mit Bildern frei lesbar auf Medium veroeffentlicht.
Die
[Einladung zum Mitpruefen](https://github.com/MemoryDynamics/Knoten/blob/main/docs/outreach/mitpruefen.md)
ist ebenfalls
[auf Englisch verfuegbar](https://github.com/MemoryDynamics/Knoten/blob/main/docs/outreach/contribute_review_en.md)
und bietet drei begrenzte Aufgaben. Ein einzelner nachvollziehbarer Einwand oder
Reproduktionsbefund ist bereits ein Beitrag.

## Modell in einem Satz

Das Projekt untersucht diskrete Dynamik mit endlichem, relaxierendem
Gedaechtnis. Der sichtbare Prozess allein ist im Allgemeinen nichtmarkovsch;
Position plus vollstaendiger Memory-Zustand bilden die Markov-Einbettung.

## Evidenz

- Paper 0 ist der mathematische Anker.
- Der skalare Paper-I-Ast traegt kontrollierte Evidenz fuer eine co-moving
  Relaxationswolke, nicht fuer ein isoliertes Teilchen.
- Der native finite-$H$-Ast besitzt lokal zertifizierte Kreisloesungen und
  kontrollierte Stabilitaetsbefunde.
- Der P4-R-S-Anchor-Holdout bleibt
  `p4rs-anchor-scale-transfer-pass`; seine groesste registrierte
  Anchor--L3-Abweichung ist `0.00232715`.
- Das interne Source-Audit bleibt
  `referee-source-ready-with-major-claim-restrictions`.

## Aktuelle Grenze

P5-D endete nach drei Zielaufrufen jeweils vor einer auswertbaren
Ergebnisdatei. Versuch 3 berechnete zwar das eingefrorene Panel, scheiterte
aber vor jeder Publikation an einem produktionsspezifischen `numpy.float64` im
strikten v2-Schema. Daher gilt weiter `p5d-inconclusive`; die Einmalfreigabe
ist verbraucht und ein weiterer Lauf nicht autorisiert. Interaktionsevidenz
existiert weiterhin nicht.

Die fruehere Formulierung „P5-D-Design und ein getrenntes prospektives
Zielgate“ ist historisch: Design und Implementierung wurden zwar getrennt,
aber die Ergebnisstrecke erwies sich in drei Zielaufrufen als nicht belastbar.

## Einstieg

- [Aktueller Stand](status/current_status.md) trennt Evidenz, Inferenz und
  Hypothese.
- [Projektprioritaeten](status/project_priorities.md) ist die einzige aktive
  Arbeitsreihenfolge.
- [Kanonisches Modellvokabular](reference/model_vocabulary.md) trennt
  Grundparameter, abgeleitete Filtergroessen und Portgroessen.
- [Implementierte Gleichungen](reference/implemented_equations.md) bildet den
  Code rueckwaerts in lesbare Mathematik ab.
- [Repository Map](reference/repository_map.md) zeigt, wo Modell, Experimente,
  Tests und Evidenz liegen.

## Claims

Interaktion, Ladung, Spin, Impuls, Traegheit und Masse bleiben Hypothesen. Die
aktuellen Schleifenbefunde sind technische Resultate des definierten
Deterministikasts, keine Identifikation realer Physik.
