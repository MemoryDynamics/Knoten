# Paper I: observable-matched linear relaxation

Stand: 2026-10-09.

Paper I behandelt den kontrollierten stochastischen Relaxationsbefund.
Die eigenstaendige FIFO-/Rotating-Wave-Arbeit behandelt nichtlineare
vorbereitete Relativgleichgewichte. Existenz- und Stabilitaetsclaims dieses
anderen Arms sind keine Voraussetzung und keine Evidenz fuer Paper I.

## Kanonische Fassungen

- `main.tex`: vollstaendige Lesefassung mit Herleitungen und Methodenanhang.
- `main_compact.tex`: derselbe Haupttext ohne Anhang.
- `content.tex`: gemeinsamer Modell-, Theorie- und Evidenztext.
- `appendix.tex`: Herleitungen, Stabilitaetsvoraussetzungen, Reproduktion.

Beide PDFs stehen nach dem Build in `../release/`. Das PRE-Layout legt die
fachliche Richtung fest, ist aber weder eine Einreichung noch eine Zusage
ueber Journalannahme.

## Inhaltlich geschlossene Punkte

- [x] Point-deposition-Modell als Memory-Mass statt glatter Dichte formulieren.
- [x] Geordneten finite-H-Zustand und native Update-Reihenfolge angeben.
- [x] Positionsradius und Memory-Wolkenradius getrennt herleiten.
- [x] RMS-Statistik in Messung und Vorhersage identisch definieren.
- [x] Finite-H-Referenz per Impulsantwort und unabhaengigem Spektralintegral pruefen.
- [x] Neun aktive Slices und acht geteilte eta-zero-Kontrollen auswerten.
- [x] Alle 85 extrahierten terminalen Radius-Traces mit Quellhashes archivieren.
- [x] Abbildungen mit Seed-IQRs und vollstaendige Parametertabelle erzeugen.
- [x] Literatur zu Aging, Markov-Einbettung, Walking Droplets und Autochemotaxis abgrenzen.
- [x] Kernel-Kollaps und feste-Gain-Kontrolle sichtbar einbinden.
- [x] Unbelegte Informationsverlust-, Metastabilitaets- und Zeitclaims entfernen.
- [x] FIFO-Rotationsbefunde aus der Evidenzlinie von Paper I herausnehmen.

## Befund und Grenze

Primaer ist der Median ueber fuenf Seeds des Verhaeltnisses aus terminalem
zeitlichem RMS und fester linearer finite-H-Vorhersage. Fuer den
Memory-Wolkenradius ergeben sich 0.076% mediane und 0.984% maximale
Abweichung ueber neun aktive Slices. Der Positionsradius liefert 0.090%
beziehungsweise 0.761%. Der maximale Memory-Radiusfehler der acht
eta-zero-Kontrollen ist 2.122%.

Die 10001 terminalen Messungen umfassen nur 10000 Updates, also 100
Memory-Persistenzzeiten, auch bei N=300M. Seed-IQRs sind Streuungen, keine
Konfidenzintervalle. Die Auswertung ist post-hoc und keine neue prospektive
Replikation. Langzeitlaufdauer ist keine unabhaengige Stichprobengroesse.

Die historischen Fehlerzahlen 0.76% und 1.15% vergleichen unterschiedliche
Observablen und Mittelungskonventionen. Sie sind durch die neue Analyse
ersetzt, nicht als neue exakte Theoriefehler umetikettiert worden.

## Reproduktion

Im Repository-Hauptverzeichnis:

```powershell
python -m pip install -r paper/paper_i/scripts/requirements-finalization.txt
python paper/paper_i/scripts/finalize_evidence.py
python -m pytest paper/paper_i/scripts/test_finalization.py -q
cd paper/paper_i/manuscript
latexmk -xelatex main.tex
latexmk -xelatex main_compact.tex
```

Der Rebuild verwendet nur den eingecheckten Radius-Extrakt und die ebenfalls
eingecheckten Kernel-Kontrollsummaries. Die optionale `--extract-from`-Option
liest die historischen Originaloutputs neu; sie ist fuer den normalen
Rebuild nicht erforderlich. Der Extrakt ersetzt kein Vollarchiv aller
urspruenglichen Trajektorienkoordinaten.

## Abschlusspruefung

- [x] Endgueltige Manuskripte bauen und Warnungen pruefen.
- [x] Alle PDF-Seiten visuell pruefen.
- [x] Claim-, Formel-, Tabellen-, Literatur- und Bildreferenz-Audit abschliessen.
- [ ] Versionierte GitHub-Fassung mit unveraenderlichem Datenverweis publizieren.

Vor einer formellen Einreichung entscheidet der Autor ueber Journal,
Autorenmetadaten, Offenlegung von KI-Unterstuetzung gemaess Journalregeln
und gegebenenfalls einen DOI fuer den Datenstand. Das sind keine neuen
wissenschaftlichen Simulationsgates.
