# Paper I: observable-matched linear relaxation

Stand: 2026-10-24.

## Wissenschaftlicher Reifegrad

Die PDF-Fassung vom 2026-10-09 bleibt als reproduzierbare Baseline erhalten.
Die abgeschlossene technische Checkliste bedeutet **nicht PRE-Einreichungsreife**.
Neuheitsabgrenzung, eine tragfaehige physikalische Hauptaussage und deren
gezielte Pruefung fehlen noch. Die verbindliche Reihenfolge steht in den
[Projektprioritaeten](../../../docs/status/project_priorities.md); der
[Neuheitsaudit](../research/pre_reassessment_2026-10-19.md) trennt bekannte
Resultate von der noch offenen nichtlinearen Arbeitshypothese. Die neuen
Forschungsrechnungen aendern weder die eingefrorenen PDFs noch die alten Daten.

Der neue [Gaussprojektions-Audit](../research/gaussian_projection_audit_2026-10-24.md)
reproduziert den gesamten ersten Transportkorrekturterm mit etablierter
statistischer Linearisierung. Der moegliche Mehrwert liegt damit im
kontrollierten Gueltigkeitsnachweis und dessen Behandlung von Gedaechtnis
und Langzeitgrenze, nicht in einer durch den $D_4$-Mittelwert abgrenzbaren
neuen Methode. Ein [begrenzter Satzvergleich](../research/linear_response_scope_audit_2026-10-24.md)
liegt nun vor: Die volle Historie erlaubt keinen direkten
Totalvariations-Satzimport; glatte Antworttheorie benoetigt noch eine
passende Norm- und Transportpruefung. Dies belegt keine Neuheit. Der
gesamte Literaturvergleich und die fachliche Beitragsbewertung bleiben
offen. Eine exakte lineare Reduktion folgt aus dem Projektionsbefund nicht.

Die [Stationaritaetsnotiz](../research/finite_memory_stationarity_2026-10-21.md)
schliesst einen begrenzten Existenzschritt bei festem endlichem Speicher
und positivem Rauschen. Dieser Existenzbeweis allein rechtfertigt keine
stationaere Schwachrauschentwicklung: Ein exaktes Koexistenzbeispiel trennt
lokale Stabilitaet von globaler Branch-Selektion. Die spaetere
Mittelungsergaenzung begruendet diese Momententwicklung bei festem
endlichem $H$ auch fuer die archivierten Modellkoeffizienten, aber ohne
brauchbare Fehlergrenzen fuer ihr endliches Rauschen und ohne Transport-
oder unendlichen Horizontgrenzwert. Eine separate
[Kontraktionsnotiz](../research/weak_noise_validity_2026-10-21.md) begruendet
die Momententwicklung unter einer strengeren globalen Bedingung, auch bei
ungekuerztem Gedaechtnis. Ihre Transporterweiterung kontrolliert zusaetzlich
den Rest in der unendlichen Kovarianzsumme und liefert einen expliziten
Diffusionskoeffizienten bis Ordnung $\varepsilon^4$. Keine aktive
archivierte Zelle erfuellt diese hinreichende Schranke; praktische
Fehlertoleranzen und der vollstaendige Neuheitsvergleich fehlen weiter.
Auch diese Forschungsbefunde stellen fuer sich keine ausreichende
Publikationsneuheit dar.

Das [externe Review und sein Gegencheck](../research/external_review_audit_2026-10-22.md)
liefern einen konkreten Testkandidaten, aber noch keine Panelreife:
Der vorgeschlagene Block-MSD stimmt nicht mit dem Langzeittransport
ueberein. Die anschliessende
[gepaarte Machbarkeitsnotiz](../research/paired_transport_feasibility_2026-10-22.md)
repariert den fuehrenden Bias durch einen bekannten Zweilaengen-Schaetzer
und berechnet die Langblock-Varianz samt kubischem Gauss-Chaos. Eine
[Ergaenzung](../research/finite_block_transport_bound_2026-10-22.md)
begrenzt die endliche Stichprobenunsicherheit des fuehrenden Koeffizienten,
ohne unabhaengige Bloecke anzunehmen. Das neue
[Gesamtfehlerbudget](../research/finite_noise_transport_budget_2026-10-23.md)
ergibt mit expliziten Schaetzer-/Transportresten und vollstaendig
vorgefuelltem Start einen hinreichenden kleinen Rauschbereich. Es
validiert keine Maschinenarithmetik: Der Kontrast am oberen Rand ist
nur etwa ein Milliardstel des linearen Hintergrunds. Eine
[exakte Restdarstellung](../research/paired_residual_precision_2026-10-23.md)
besteht inzwischen begrenzte Hochpraezisionschecks. Die anschliessende
[Fehlerfortpflanzungsnotiz](../research/paired_error_propagation_2026-10-23.md)
begrenzt die Verstaerkung vorgegebener lokaler Defekte und separat die
skalare Mittelung, nicht die gesamte Simulatorarithmetik. Die
[Entscheidungsvorlage](../research/paper_i_decision_brief_2026-10-23.md)
fasst den analytischen Beitragskern fuer eine fachliche Diskussion
zusammen. Vor Zielsimulationen bleiben validierte lokale Fehler und
Laggrenzen, eine vertretbare Kostenentscheidung, Fachreview und
Neuheitsvergleich erforderlich. Der bisherige
leere Speicherstart ist nicht abgedeckt. Die PDFs bleiben unveraendert.

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

## Geschlossene Baseline-Punkte

- [x] Point-deposition-Modell als Memory-Mass statt glatter Dichte formulieren.
- [x] Geordneten finite-H-Zustand und native Update-Reihenfolge angeben.
- [x] Positionsradius und Memory-Wolkenradius getrennt herleiten.
- [x] RMS-Statistik in Messung und Vorhersage identisch definieren.
- [x] Finite-H-Referenz per Impulsantwort und unabhaengigem Spektralintegral pruefen.
- [x] Neun aktive Slices und acht geteilte eta-zero-Kontrollen auswerten.
- [x] Alle 85 extrahierten terminalen Radius-Traces mit Quellhashes archivieren.
- [x] Abbildungen mit Seed-IQRs und vollstaendige Parametertabelle erzeugen.
- [x] Literaturstand der Baseline zu Aging, Markov-Einbettung, Walking Droplets und Autochemotaxis einordnen; die aktuelle Neuheitspruefung bleibt offen.
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
- [x] Versionierte GitHub-Fassung mit unveraenderlichem Datenverweis publizieren.

Vor einer formellen Einreichung entscheidet der Autor ueber Journal,
Autorenmetadaten, Offenlegung von KI-Unterstuetzung gemaess Journalregeln
und gegebenenfalls einen DOI fuer den Datenstand. Unabhaengig davon sind
die nun ausgewiesenen wissenschaftlichen Neuheits- und Evidenzluecken zu
schliessen; eine Autorenfreigabe allein ersetzt das nicht.
