# Stochastik und Quantenstruktur: begrenzter Anschlussaudit

Stand: 2026-11-06. Analytischer Referenzvergleich gegen Repository-Stand
`09c2d07`, keine neue Zielsimulation, kein neuer Modellast. Die
[Projektprioritaeten](../../docs/status/project_priorities.md) bleiben die
einzige Arbeitsreihenfolge. Dieser Bericht gehoert zum Anschluss an den
[Wasserstoff-Benchmark](../../docs/reference/hydrogen_benchmark.md), nicht
zu den nachgewiesenen Ergebnissen von Paper I.

## Ergebnis und Reichweite

Ein klassischer Coulomb-Grenzfall waere noch keine Wasserstofftheorie.
Auch Gaussrauschen, eine passende stationaere Dichte und komplexe
Schreibweise liefern fuer sich keine Quantenmechanik. Drei verschiedene
Verbindungen sind zu pruefen: Ensemblezustand und seine Dynamik,
globale Phasen-/Randbedingungen sowie eine gemeinsame Massen-/Wirkungs-
und Messbeschreibung. Keine davon wird hier als bereits emergent gesetzt.

Positiver Referenzbefund: Mit zusaetzlicher mechanischer Struktur gibt es
einen praezisen stochastischen Anschluss an die lokale Schroedinger-
Gleichung. Negativer Bestandsbefund: Diese Struktur ist aus unserer
FIFO-Regel nicht hergeleitet. Das ist kein allgemeiner Unmoeglichkeits-
beweis gegen stochastische oder kollektive Quantenmodelle.

## 1. Memory-Dichte ist keine Ensemble-Ortsdichte

Der [native Schritt](https://github.com/MemoryDynamics/Knoten/blob/09c2d07/src/emergenz_knoten/core.py)
verwendet aktuelle Position und individuelle Historie. Fuer dieselbe
Position koennen verschiedene Historien verschiedene bedingte Drifts
liefern. Der augmentierte Zustand ist Markov; die Position allein hat
daher nicht ohne Weiteres eine geschlossene Markov-Dynamik.

Sei $p_n$ die Ortsverteilung ueber Wiederholungen. Bei voll gefuelltem
FIFO ist die Spur eines einzelnen Laufs schematisch

$$
\rho_n(z)=\sum_{j=0}^{H-1}w_jG(z-X_{n-j}),\qquad
\mathbb E\rho_n(z)=\sum_{j=0}^{H-1}w_j(G*p_{n-j})(z).
$$

Auch nach Mittelung ist dies eine geglaettete, altersgewichtete Mischung,
nicht allgemein $p_n$. Bei stationaeren Marginalen vereinfacht sie sich
zu $(\sum_jw_j)G*p$, aber ein einzelner endlicher Memory-Zustand ist
damit noch kein exaktes Ensemble. Normierung beseitigt diese Unterschiede
nicht. Eine Schroedinger-Herleitung darf deshalb nicht dieselbe Variable
abwechselnd fuer individuelle Spur und Born-Dichte einsetzen.

## 2. Was der Nelson-Vergleich voraussetzt

[Nelsons Autorenfassung des Buchs](https://web.math.princeton.edu/~nelson/books/bmotion.pdf),
Kapitel 11, 13 und 15, liefert einen konkreteren Vergleich als der zuvor
gelesene Abstract von 1966. Im betrachteten spinlosen Markov-Ansatz sind
Diffusion $D=\hbar/(2m)$ und das Kraftgesetz mit symmetrischer mittlerer
Beschleunigung Voraussetzungen, nicht Folgen beliebigen Rauschens:

$$
u=\frac{b-b_*}{2}=D\nabla\log p,\quad v=\frac{b+b_*}{2},\quad
a=\frac12(\mathcal D\mathcal D_*+\mathcal D_*\mathcal D)X,
\quad ma=-\nabla V.
$$

Dabei sind $b,b_*$ die bedingten Vorwaerts-/Rueckwaertsgeschwindigkeiten
und $\mathcal D,\mathcal D_*$ die entsprechenden mittleren Ableitungen.

Unter Regularitaet und lokalem Gradientenansatz $mv=\nabla S$ ergibt
$\psi=\sqrt p\exp(iS/\hbar)$ die lokale Schroedinger-Gleichung, bis auf
eine zeitabhaengige globale Phase. Hier hat $S$ Wirkungseinheiten;
Nelsons Kapitel 15 verwendet eine dimensionslose Phase. Die native
FIFO-Regel liefert weder dieses Beschleunigungsgesetz noch einen solchen
Ensembleabschluss. Vorwaerts-/Rueckwaertsdrift zu definieren allein
schliesst diese Luecke nicht.

Der Vergleich behandelt noch keine allgemeine globale Zustandsklasse,
Spin, Austauschstatistik oder physikalische Messoperationen. Fuer letztere
bleibt der getrennte [operationale Vertrag](../../docs/reference/operational_contract.md)
offen; die bedingte Bell-Schranke im
[Grundlagenaudit](../../docs/reference/foundation_feasibility.md) bleibt bestehen.

## 3. Eigene OU-Kontrolle: stationaere Form versus Zeitentwicklung

Betrachte als **deklarierte Referenz**, nicht als bewiesenen Abschluss
des vollen FIFO, den eindimensionalen Prozess

$$
dX=-\gamma X\,dt+\sqrt{2D}\,dW,\quad D,\gamma>0,\qquad
p_*(x)=\sqrt{\frac{\gamma}{2\pi D}}e^{-\gamma x^2/(2D)}.
$$

Mit gesetztem $D=\hbar/(2m)$ und $\Omega=\gamma$ ist $p_*$ die
Ortsdichte des Oszillatorgrundzustands. Das prueft eine stationaere
Funktion, keine Gleichheit der dynamischen Theorien.

Fuer den Vorwaertsgenerator $L^*p=D p''+\gamma(xp)'$ setze
$h=\sqrt{p_*}$ und $p=h\varphi$. Direktes Differenzieren ergibt

$$
h^{-1}L^*(h\varphi)
=D\varphi''+\left(\frac\gamma2-\frac{\gamma^2x^2}{4D}\right)\varphi
=-\frac{H_{\rm osc}-E_0}{\hbar}\varphi,
\quad E_0=\frac{\hbar\gamma}{2},
$$

$$
H_{\rm osc}=-\frac{\hbar^2}{2m}\partial_x^2+
\frac12m\gamma^2x^2.
$$

Das ist eine **Imaginarzeit-Entwicklung**. Auf den Oszillatormoden sind
die Faktoren $e^{-n\gamma t}$, nicht die unitaeren Faktoren
$e^{-in\gamma t}$. Die stationaere Mode stimmt ueberein; andere Moden
werden verschieden gewichtet. Normieren einer dissipierten Funktion
repariert deren veraenderte relative Amplituden nicht. Hier ist
$\varphi=p/h$ im Allgemeinen auch nicht die Born-Amplitude $\sqrt p$.
Ein Austausch reeller gegen imaginaere Zeit aendert die physikalische
Entwicklung und ist kein blosses Umbenennen der Dichte.

Eine zweite Kontrolle trennt diese Aussage von einem pauschalen
Nelson-Einwand. Fuer eine zentrierte OU-Gaussdichte mit Varianz $s(t)$
gilt $\dot s=2D-2\gamma s$. Einsetzen in die oben definierten
Geschwindigkeiten ergibt $u=-Dx/s$, $v=(D/s-\gamma)x$ und

$$
a=\partial_t v+v\partial_xv-u\partial_xu-D\partial_x^2u
=\left(\gamma^2-\frac{2D^2}{s^2}\right)x.
$$

Nur fuer $s=D/\gamma$ ist dies die Beschleunigung $-\gamma^2x$ des
gleichen Oszillatorpotentials. Der stationaere OU-Prozess ist also
kompatibel mit diesem Referenzzustand; beliebige OU-Transienten sind
nicht automatisch dessen Quantendynamik. Ein anders gewaehlter,
zustandsabhaengiger Drift ist durch diese Gegenprobe nicht ausgeschlossen.
Rohe Bahnkorrelationen werden hier nicht mit Quantenmesskorrelationen
gleichgesetzt.

## 4. Eigene Ringkontrolle: lokal richtig, global nicht ausreichend

Waehle einen spinlosen freien Ring mit Umfang $L$ und festem periodischem
Randsektor, ohne aeusseren Eichfluss. Dies ist eine konstruierte Referenz,
keine native FIFO-Bahn. Fuer jedes reelle $v_0$ sind

$$
p=1/L,\quad v=v_0,\quad u=0,\quad
S(s,t)=m v_0s-\frac12m v_0^2t
$$

stationaere lokale Stroemungsdaten mit $V=0$. Die lokale Funktion
$\psi=L^{-1/2}\exp(iS/\hbar)$ erfuellt die freie Schroedinger-Gleichung.
Die globale periodische Randbedingung verlangt aber zusaetzlich

$$
\frac{\psi(s+L,t)}{\psi(s,t)}=e^{imv_0L/\hbar}=1
\quad\Longleftrightarrow\quad
\frac{mv_0L}{2\pi\hbar}\in\mathbb Z.
$$

Die klassische Ringdiffusion mit konstantem Drift besitzt dagegen fuer
jedes $v_0$ die uniforme stationaere Dichte. Lokale Gleichungen und eine
eindeutige Dichte waehlen das Phasengitter also nicht allein aus. Ein
global reelles periodisches $S$ waere wiederum zu stark: Es wuerde die
nichtverschwindenden ganzzahligen Umlaeufe ausschliessen.

Ein anderer **fest gewaehlter** verdrehter Rand
$\psi(s+L)=e^{i\theta}\psi(s)$ erlaubt stattdessen
$mv_0L/(2\pi\hbar)\in\mathbb Z+\theta/(2\pi)$. Fuer jeden Zustand einen
neuen Randwinkel auszuwaehlen waere keine Herleitung einer gemeinsamen
festen Theorie. Die Kontrolle beweist weder ein No-go fuer andere
Zustandsraeume noch eine Aussage ueber Spinor-Randbedingungen.

Diese Vorsicht stimmt mit dem differenzierten Befund von
[Reddiger und Poirier, arXiv v1](https://arxiv.org/pdf/2207.11367v1)
ueberein: Proposition 2.1 beweist die Umlaufbedingung aus einer bereits
gegebenen nichtverschwindenden $C^1$-Wellenfunktion; Abschnitt 4.1 trennt
lokale Polardarstellungen von globalen Funktionen. Die Autoren behandeln
die allgemeine mathematische Vervollstaendigung nicht als erledigt oder
grundsaetzlich unmoeglich. Unsere Ringrechnung ersetzt nicht ihre
Analyse von Knotenstellen und schwachen Loesungen.

Als Gegenposition wurde auch [Hushwater, v4](https://arxiv.org/pdf/1005.2420v4)
geprueft. Sein Argument verwendet bei Gleichung (17) eine Darstellung
durch kartesische ebene Wellen. **Eigene Einordnung:** Diese Darstellung
bringt bereits globale Eindeutigkeit mit; aus dem nativen Memory-Update
ist ihre Zulaessigkeit nicht gewonnen. Sie beseitigt deshalb unseren
offenen Ableitungsschritt nicht. Das ist kein vollstaendiges Gutachten
ueber alle im Preprint diskutierten Singularitaeten.

## 5. Historische Aussagen und Wirkungsmasstab

Der [historische Chat](https://github.com/MemoryDynamics/Knoten/blob/09c2d07/docs/historical/chatgpt/topics/physics/TrajektorienZuSchroedinger.md)
enthaelt anfangs eine unberechtigte Zusage der Schroedinger-Herleitung
aus quadratischem Drift und Phasenumschreibung. **Im selben Chat** werden
spaeter der fehlende Massenfaktor und die Kalibrierung statt Herleitung
von $\hbar$ ausdruecklich erkannt. Diese spaetere Korrektur darf beim
Lesen nicht unterschlagen werden. Der Chat bleibt als Archiv unveraendert;
weder seine fruehe Zusage noch seine spaeteren Fixpunktvermutungen gelten
als heutiger Nachweis.

Algebraisch folgt aus $\tau_p=1/\alpha$ und einer fest kalibrierten
Proportionalitaet $\hbar=C\varepsilon^2/\alpha$ gerade
$\varepsilon^2=\hbar/(C\tau_p)$, nicht
$\hbar\tau_p/C$. Dabei ist $\tau_p$ zunaechst eine Schrittzahlskala.
Mit dimensionslosem $\alpha$ und $[\varepsilon]=L$ hat
$\varepsilon^2/\alpha$ die Einheit $L^2$, nicht Wirkung.

Erst eine physikalische Zeitskala $\Delta t$ liefert den bedingten
Inkrement-Diffusionsparameter $D=\varepsilon^2/(2\Delta t)$ pro
Koordinate. Die Nelson-Kalibrierung verlangt dann
$\hbar=m\varepsilon^2/\Delta t$. Eine Skalierung $t=\alpha n$ waehlt
eine Zeitkonvention; sie erzeugt keine unabhaengige physikalische Masse.
Die bedingte Inkrementvarianz ist $\varepsilon^2$, waehrend der bedingte
zweite Inkrementmoment auch das Driftquadrat enthaelt. Ein
Kontinuumslimit benoetigt daher eine erklaerte Drift-/Rauschskalierung.
Der Langzeit-Transportkoeffizient kann wegen Memory davon verschieden
sein. Keine dieser Groessen darf automatisch als dieselbe Diffusion
eines zukuenftigen Quantenabschlusses eingesetzt werden.

## 6. Quellenumfang und Anschlussentscheidung

Primaerquellenpruefung am 2026-11-06, keine systematische Literaturreview:

| Quelle | Tatsaechlich gepruefter Umfang |
| --- | --- |
| Nelson, *Dynamical Theories of Brownian Motion*, Autorenfassung, zweite Auflage August 2001 | Gleichung (11.15), Kapitel 13, Kapitel 15 bis zur lokalen Transformation; kein Vollgutachten des Buchs. |
| Nelson (1966), DOI [10.1103/PhysRev.150.1079](https://journals.aps.org/pr/abstract/10.1103/PhysRev.150.1079) | Bisheriger Abstractabgleich; der in dieser Recherche gefundene Original-PDF-Download blieb bei zwei Abrufen im Timeout. Buch nicht als gelesener Artikel ausgegeben. |
| Wallstrom (1994), DOI [10.1103/PhysRevA.49.1613](https://journals.aps.org/pra/abstract/10.1103/PhysRevA.49.1613) | Verlagsabstract; Originalvolltext weiterhin nicht geprueft. |
| Reddiger und Poirier, arXiv:2207.11367v1 (22.07.2022) | Abstract, Beitragsuebersicht, Proposition 2.1 und Beginn von 4.1; nicht die ganze 85-seitige Fassung oder die spaetere Verlagsfassung. |
| Hushwater, arXiv:1005.2420v4 (19.07.2010) | Argumentation Abschnitte I--III einschliesslich (17); Preprint, hier kein verifizierter Journalstatus. |

Fuer den nativen Wasserstoff-Anschluss fehlt weiterhin ein aus der
gleichen Regel hergeleitetes Ensemble-/Stromgesetz mit kontrolliertem
Rest, einem global konsistenten Phasensektor und gemeinsamer Wirkungs- und
Massenkalibrierung. Ein isolierter Grundzustandsfit waere kein Abnahmetest
dafuer. Zeitabhaengige Praeparationen muessen bei **gleichem** Potential
und gleichen Randbedingungen vorhersagbar sein. Fuer mehrere Komponenten
kommen gemeinsamer Zustandsraum, Austausch- und Messregel hinzu.

Im getrennten Referenzzweig duerfen diese Quantenstrukturen Inputs sein;
AL1 hat sie bereits vorausgesetzt. Sie im Emergenzzweig ebenfalls zu
setzen waere eine ausdrueckliche Richtungsentscheidung, die dieser
Bericht nicht trifft. Weder weitere Quarkmodell-Genauigkeit noch eine
klassische kollektive Coulomb-Antwort schliessen die Quantenluecke allein.

## Verifikation

[Konstruierte Tests](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/tests/test_stochastic_quantum_bridge.py)
pruefen den nativen Historienkontrast, den OU-Operator auf drei Moden,
stationaere Dichte, Zeitfaktoren, drei Gaussbreiten, fuenf Ringumlaeufe,
festen verdrehten Rand sowie Skalierungsalgebra. Kein Solver- oder
Zielprozess, kein Replay und keine Parametersuche. Die endlichen
Softwarekontrollen ersetzen die analytischen Argumente nicht.

Verifikation am 2026-11-06: **101 betroffene Tests bestanden in 6.71 s**,
darunter 16 neue Vergleichskontrollen und elf rein lesende AL1-Archivchecks.
Lint und strikter MkDocs-Bau bestehen. Dies ist keine vollstaendige
Repository-Testsuite. Die abgeschlossenen AL1-, FIFO- und P5-Freigaben
wurden nicht erneut verwendet; der historische Chat bleibt unveraendert.
