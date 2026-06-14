# Paper I: Notiz fuer Olaf

Stand: 2026-06-14.

## Kurzrahmung

Paper I ist jetzt als eigenstaendige Minimalmodell-Arbeit formuliert:

- sichtbarer Prozess `x_n` ist im Allgemeinen nichtmarkovsch;
- augmentierter Zustand `(x_n, rho_n)` ist die natuerliche Markov-Einbettung;
- `rho_n` ist ein endlicher, exponentiell relaxierender Speicher;
- die Update-Regel ist nichtinvertierbar und definiert eine Update-Richtung;
- `t = alpha n` ist eine interne, dimensionslose Grobkoernungsskala;
- dynamische Knoten werden operational ueber Residence, Relaxation und
  Stabilitaetsdiagnostik beschrieben;
- "mass" bleibt ein Relaxations-/Konfinierungsproxy, keine physikalisch
  kalibrierte Masse.

## Bitte gezielt sichten

Die wichtigste Frage ist nicht, ob daraus bereits Raumzeit, Standardmodell oder
Gravitation folgen. Die wichtigste Frage fuer Paper I ist:

> Ist dieses Minimalmodell als endlicher Speicherprozess mit Markov-Einbettung
> und metastabilen Relaxationsstrukturen mathematisch/physikalisch sauber genug
> formuliert, um als Fundament fuer spaetere Arbeiten zu dienen?

## Paper-0-Anker

Ein separates Paper 0 bleibt sinnvoll, aber muss Paper I nicht blockieren.
Paper 0 koennte die mathematische Nachbarschaft sauber aufarbeiten:

- self-interacting diffusions;
- self-repelling Brownian polymers;
- true/myopic self-avoiding walks;
- exponentiell vergessende nichtmarkovsche Prozesse;
- Markovian embeddings ueber explizite Gedaechtnis-/Feldvariablen.

Die Claim-Kette waere:

1. Bekannte Modelle koppeln Trajektorien an Besuchshistorien oder lokale Zeit.
2. Unser Modell ersetzt volles Langzeitgedaechtnis durch ein exponentiell
   relaxierendes Feld.
3. Dadurch ist `x_n` sichtbar nichtmarkovsch, aber `(x_n, rho_n)` markovsch.
4. Metastabile Knoten sind Kandidaten fuer metastabile Zustandsmengen dieses
   augmentierten Markov-Prozesses.

## Vorschlag fuer die Diskussion

Zuerst Paper I als Minimalmodell pruefen. Danach entscheiden, ob Paper 0 als
kurzes mathematisches Einordnungspaper vorgeschaltet oder parallel geschrieben
wird.
