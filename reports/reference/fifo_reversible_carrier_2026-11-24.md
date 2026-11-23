# Reversibler FIFO-Schreibschritt mit Traeger und endlichem Taktimpuls

Stand: 2026-11-24. Referenz zum
[energiegleichen Kernel-Schreibschritt](fifo_kernel_paid_write_2026-11-24.md).
Ein idealer Grenzflaechenuebergang; keine native Regel,
kein autonomer Taktumlauf, keine Zieltrajektorie.

**Ergebnis.** Ein deklarierter Schreibschritt kann den alten Eintrag
behalten, den neuen Ortswert schreiben und Energie sowie raeumlichen
Gesamtimpuls erhalten. Ein endlicher Taktimpuls bezahlt die
Kraft- und Kinetikdifferenz. Der Schritt benoetigt jedoch einen
vorbereiteten Traeger. Die exakte Kopie ist im quantisierten
Register nur ein singulaerer Grenzfall. Der bisherige
phasentreue Oszillatortransfer ist fuer geometrieabhaengige
Schreibkosten nicht global kanonisch erweiterbar, solange
Geometrie, Aktionstranslation und Phase vorgeschrieben bleiben.

## 1. Warum Oszillatorflaeche nicht Gesamtflaeche ist

Sei $Q$ die bei einem Schreibereignis festgehaltene Geometrie
und $h(Q)=(F_{Y^+}-F_Y)/\omega$ der Aktionsbetrag
des frueheren Oszillatortransfers. In den alten und neuen
zentrierten Oszillatorcharts laesst sich die symplektische Form
mit passenden Geometrieimpulsen als

$$
\Omega=\sum_i dQ_i\wedge d\Pi_i+dJ\wedge d\theta
$$

schreiben. Der Zusatz zum Geometrieimpuls ist wichtig:
Aus $a=\alpha+a_Y(Q)$ folgt bereits auf Ebene der
kanonischen Einsform
$P\cdot dQ+p_a\,da=(P+p_a\nabla_Q a_Y)\cdot dQ+p_a\,d\alpha$.
Somit vergleicht man nach der Zentrierung nicht einfach
unveraenderte nackte Geometrieimpulse.

Der vorgeschriebene Transfer $Q'=Q$, $J'=J-h(Q)$,
$\theta'=\theta+\xi$ (feste Phasenverschiebung) erzeugt
im Oszillatorteil den zusaetzlichen Term $-dh\wedge d\theta$.
Ein kanonischer Lift muesste ihn kompensieren, also
$\partial_\theta\Pi_i'=\partial_i h$. Auf einem lokalen
Winkelchart funktioniert $\Pi'=\Pi+\theta\nabla h$.
Ueber den ganzen Winkelkreis erzeugt das jedoch den Sprung
$2\pi\nabla h$. Integration der notwendigen Gleichung
ueber eine Periode zeigt, dass ein glatter, einwertiger
Impuls auf dem Kreis nur bei konstanter Schreibarbeit
in Aktionseinheiten moeglich ist ($dh=0$).
Der Ausschluss gilt in diesem regulaeren Bereich mit
frei zulaessigem Winkel. Er verbietet weder andere
Schreibkarten noch einen zusaetzlichen Taktfreiheitsgrad.
Der lokale Lift allein schliesst auch keine Energiebilanz
mit kinetischen Geometrieimpulsen.

## 2. Eine translationsvertraegliche Registerabbildung

Seien $x$ der Kopf, $y_0,\ldots,y_{H-1}$ die Ortsregister
und $b$ der eingehende Traeger. Zu jedem Ort gehoert in
dieser Referenz ein kanonischer Impuls. Die lineare
Ortsabbildung $C$ setzt

$$
x'=x,\quad y_0'=x+b-y_{H-1},\quad
y_j'=y_{j-1}\ (1\le j<H),\quad b'=y_{H-1}.
$$

Der aelteste Eintrag kommt also in den ausgehenden
Traeger. Der eingehende Zustand ist aus dem neuen
rekonstruierbar, insbesondere $b=y_0'-x'+b'$.
Die kopierende Bedingung ist $b=y_{H-1}$, eine
relative Vorbereitung ohne bevorzugten Ursprung.
Bei Fehlpraeparation gilt exakt
$y_0'-x'=b-y_{H-1}$. Die direkte Wiederverwendung
des alten Traegers erfuellt die Bedingung im Allgemeinen
nicht; es gibt hier keine kostenlose Ruecksetzung.

Der zugehoerige Kotangentiallift ist $P'=C^{-T}P$:

$$
P_x'=P_x-P_b,\quad P_0'=P_b,\quad
P_j'=P_{j-1}\ (1\le j<H),\quad
P_b'=P_{H-1}+P_b.
$$

Dies erhaelt die kanonische Einsform exakt.
Eine gemeinsame Translation aller Positionen
kommutiert mit $C$, und die Summe der raeumlichen
Impulse bleibt unveraendert. Der Kopf behaelt zwar
seinen Ort beim Schreiben, im Allgemeinen aber
nicht seinen Impuls. Die Impuls- und Energiewirkung
der Praeparation bleibt getrennt von der Karte.
Der [aeltere Trajektorien-Write-Port](../memory/closure/p38f_canonical_write_gate_2026-08-15.md)
verwendet kanonisch im Sinn der festgelegten nativen
Deposition; er ist kein Nachweis dieses symplektischen Lifts.

## 3. Wer die Schreibarbeit bezahlt

Eine separate Taktkoordinate $s$ mit Impuls $\pi_s$
und Masse $M_s>0$ erreicht die Flaeche $s=0$.
Im gemeinsamen Geometriechart hat die deklarierte
Hamiltonfunktion auf beiden Seiten die Form
$\pi_s^2/(2M_s)+E_\pm(Q,P)$. Auf der Plusseite steht
im gemeinsamen Chart $E_+(CQ,C^{-T}P)$, weil dort
die Registerrollen durch $C$ bezeichnet werden.
Die ideale unstetige Grenzflaeche ist nur im Takt
normal. Fuer eine nichtstreifende Passage bleiben
die tangentialen Variablen im gemeinsamen Chart
kontinuierlich; die Taktenergie bilanziert den Sprung.
In den benannten Registerkoordinaten ist der
transmittierte Schreibschritt folglich $C$ und
sein Kotangentiallift, mit

$$
W=E_+(Q',P')-E_-(Q,P),\qquad
\pi_s'=\operatorname{sgn}(\pi_s)
\sqrt{\pi_s^2-2M_sW}.
$$

Bei umgekehrter Passage werden beide Seiten getauscht
und die inverse Karte benutzt. $W$ enthaelt die
gesamte interne Energiedifferenz, also auch die
kinetischen Aenderungen des Impulsuebertrags.
Reicht die Taktenergie nicht, reflektiert der
Taktimpuls und es wird nichts geschrieben.
Der streifende Schwellenfall wird nicht modelliert.
Im Code wird dieselbe Energiefunktion in beiden
jeweiligen Registercharts eingesetzt.
Die Summe aus Takt- und Registerenergie ist beim
Uebergang erhalten, und bei umgekehrten Impulsen
laesst sich die Passage fuer einen impulsgeraden
Register-Hamiltonian exakt rueckgaengig machen.

[Afshar und Domke (2015)](https://papers.neurips.cc/paper/5801-reflection-refraction-and-hamiltonian-monte-carlo.pdf)
verwenden Reflexion und Brechung an Energiespruengen.
Hier kommen die Registerkarte und der alte
gespeicherte Eintrag hinzu. Geprueft wird die
Abbildung der Schnittflaechen, nicht eine volle
glatte Kollisionsdynamik oder ein wiederkehrender
autonomer Takt. Der Energievorrat ist endlich;
die neuen Praeparationen und der Taktumlauf
werden nicht hergeleitet.

## 4. Was davon in einem Quantenvergleich uebrig bleibt

Der lineare Registerteil laesst sich als
Koordinatenwechsel auf $L^2$ **quantisieren**.
Wegen $|\det C|=1$ ist
$(U_C\psi)(Q')=\psi(C^{-1}Q')$ unitaer.
Das ist eine eingesetzte Quantisierung dieser
Karte, keine Herleitung der Quantenmechanik und
keine quantisierte Grenzflaechenstreuung.
Die Struktur aehnelt der quadraturbezogenen
Rueckwirkung des
[SUM-Gatters von Yoshikawa et al. (2008)](https://arxiv.org/abs/0808.0551).

In einer Raumkomponente ist der Schreibfehler
$e=y_0'-x'=b-y_{H-1}$ und
$[e,P_b]=i\hbar$. Somit
$\Delta e\,\Delta P_b\ge\hbar/2$,
auch bei Korrelationen zwischen den Registern.
Beschraenkt man die mittlere kinetische
Traegerenergie auf $E_b$ bei Traegermasse $m_b$,
folgt

$$
\Delta e\ \ge\ \frac{\hbar}{\sqrt{8m_b E_b}}.
$$

Der zur Praezision benoetigte Impuls ist gerade
derjenige, der auf den Kopf zurueckwirkt. Eine
exakte Ortskopie mit endlichem kinetischem Budget
ist daher keine zulaessige Quantenpraeparation.
Das unterscheidet die reversible klassische Karte
von einem kostenlosen Quanten-FIFO.

[Referenzcode](../../experiments/current/reference/fifo_reversible_carrier.py)
und [feste Kontrollen](../../tests/test_fifo_reversible_carrier.py)
pruefen die inverse Karte, die Kotangentialidentitaet,
Gesamtimpuls und Praeparationsfehler, Transmission,
Rueckkehr, Reflexion sowie den lokalen Winkellift.
Naechster Pruefstein: ein autonom wiederkehrender
Takt mit endlicher Registerpraeparation. Keine Aussage
ueber gebundene Knoten, Gravitation oder spontane
Quantendynamik.
