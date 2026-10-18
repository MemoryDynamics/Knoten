# Ein Traum von Knoten

*Wie ein Kindheitstraum zum Ausgangspunkt eines Forschungsprojekts wurde.*

*Entwurf für Medium · 19. Oktober 2026 · [English version](https://github.com/MemoryDynamics/Knoten/blob/main/docs/outreach/medium_draft_en.md)*

Als Kleinkind hatte ich einen Traum. Ich flog frei umher, bog etwas ab und
verfing mich in meiner eigenen Flugbahn. So sehr, dass ich irgendwann in
komplexen Knoten festhing.

Das war ein fast albtraumartiger Moment. Oft fand ich wieder heraus. Als
ich endlich wieder frei war, wurde es irgendwann langweilig. Ich bog etwas
ab, und das Ganze begann von Neuem.

Genau dieser Traum war der Ansatz für das, woran ich heute arbeite: eine
Trajektorie mit Gedächtnis. Eine Bewegung, deren Vergangenheit auf ihren
weiteren Verlauf zurückwirkt. Daraus kamen später auch die Fragen nach
Wechselwirkungen und danach, ob auf diese Weise beständige Strukturen
entstehen könnten.

Das ist sehr persönlich. Es erklärt meine Motivation, auch wenn es noch
keine Antwort darauf gibt, ob die Idee wissenschaftlich trägt.

## Wie daraus ein Modell wurde

Wir sind schrittweise über philosophische Fragen zum heutigen Stand
gekommen. Dabei ging es auch darum, was man eigentlich als Zustand eines
Systems beschreibt. Reicht der Ort, an dem sich etwas gerade befindet?
Oder gehört seine Vergangenheit dazu?

Über solche Fragen kamen wir zum Begriff „markovsch“. Im Modell reicht der
sichtbare Ort allein im Allgemeinen nicht aus, um die Wahrscheinlichkeit
des nächsten Schritts zu bestimmen. Die gespeicherte Vergangenheit spielt
mit hinein. Nimmt man den vollständigen Gedächtniszustand dazu, bekommt
man eine Markov-Beschreibung.

Das klingt erst einmal abstrakt. Die Vorstellung dahinter ist einfacher:
Ein Punkt bewegt sich, hinterlässt eine verblassende Spur und reagiert
anschließend auf diese Spur. Im Rechner speichern wir dafür eine endliche
Zahl vergangener Positionen.

Das Projekt heißt **Emergenz Knoten**. Die große Hoffnung dahinter war und
ist, auf diesem Weg etwas über die Entstehung physikalischer Strukturen
zu verstehen. Da liegt das Wort „Weltformel“ natürlich nahe. Bislang haben
wir ein mathematisches Modell und eine Reihe von Ergebnissen, deren
Reichweite wir prüfen müssen.

## Wo wir stehen

Manche zunächst auffälligen Strukturen im Modell lassen sich schon durch
lineare Relaxation erklären. In einem getrennten Modellzweig gibt es für
bestimmte vorbereitete Kreisbahnen computerassistierte lokale
Existenzzertifikate. Dazu kommen numerische Tests, in denen kleine
Störungen unter festgelegten Bedingungen wieder abklingen.

Das sind begrenzte Ergebnisse. Sie zeigen bisher weder reale Teilchen noch
physikalische Masse, Ladung oder Spin. Auch eine Kreisbahn ist noch kein
topologischer Knoten. Wie weit die Befunde über die untersuchten
Anfangszustände und Parameter hinausreichen, bleibt zu prüfen.

Die Gleichungen, der Code und die Auswertungen stehen im
[GitHub-Repository](https://github.com/MemoryDynamics/Knoten).

Vielleicht habe ich im Traum auch „nur“ meine Neuronen beim Vernetzen
erlebt. Das ist eine persönliche Deutung, die ich aus der Erinnerung nicht
belegen kann. Trotzdem finde ich den Gedanken interessant. Vielleicht
führt die Frage nach einer Dynamik mit Gedächtnis auch zu etwas, das in
der KI-Entwicklung nützlich sein könnte.

Dafür müsste man eigene Aufgaben und Vergleiche entwickeln. Bislang haben
wir weder eine Erklärung des Gehirns noch einen Nachweis, dass das Modell
lernt oder für KI einen Vorteil bringt. Diese Frage könnte man aber auch
dann verfolgen, wenn sich die große physikalische Hoffnung nicht erfüllt.

## Warum ich darüber schreibe

Das Projekt ist zu groß für mich geworden. Und Menschen zu finden, die
Zeit für ein Review haben, wird schwieriger.

Ich frage mich deshalb, ob wir die Diskussion früher und informeller
öffnen sollten. Vielleicht gibt es andere, die von ähnlich persönlichen
Fragen angetrieben werden und hier etwas wiedererkennen. Oder jemanden,
der eine Gleichung sieht und sofort sagen kann, wo der Fehler liegt.
Beides wäre ein guter Anfang für ein Gespräch.

Fachjournale bleiben für einzelne Ergebnisse eine Möglichkeit. Aber ich
möchte mit der Diskussion nicht warten, bis sich das ganze Projekt in
eine fertige Geschichte bringen lässt.

Niemand muss dafür das gesamte Repository durcharbeiten. Eine Herleitung
prüfen, eine Rechnung nachvollziehen oder eine einfachere Erklärung
vorschlagen wäre schon hilfreich. Wir haben dafür
[drei überschaubare Einstiege](https://github.com/MemoryDynamics/Knoten/blob/main/docs/outreach/mitpruefen.md)
zusammengestellt. Rückmeldungen lassen sich als
[GitHub-Issue](https://github.com/MemoryDynamics/Knoten/issues/new?template=focused_review.md)
festhalten.

Wie weit die Idee trägt, die aus dem Traum entstanden ist, würde ich gern
gemeinsam herausfinden.

---

Zum Nachlesen: [Wissenschaftlicher Stand](https://github.com/MemoryDynamics/Knoten/blob/35ae7b0eb7d7bb8cc57eaa2c2af80b32d955fb4f/docs/status/current_status.md),
[lokaler Stabilitätsbefund](https://github.com/MemoryDynamics/Knoten/blob/35ae7b0eb7d7bb8cc57eaa2c2af80b32d955fb4f/reports/project/meta/reviews/scalar_memory_rotating_wave_horizon_g5_component_attempt_3_result_review_2026-09-17.md)
und [internes Review](https://github.com/MemoryDynamics/Knoten/blob/35ae7b0eb7d7bb8cc57eaa2c2af80b32d955fb4f/reports/project/meta/reviews/scalar_memory_rotating_wave_horizon_g5_premerge_referee_review_2026-09-17.md).
Die internen Prüfungen sind keine unabhängige externe Replikation.

*Hinweis: Dieser Text entstand mit Unterstützung von Sol6.1 (KI) bei
Struktur, Formulierung und Übersetzung. Die Traumschilderung und die
persönliche Motivation stammen von mir.*
