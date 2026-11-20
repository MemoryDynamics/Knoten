# Langmemory-Umlauf und kollektive Coulomb-Phase sind verschiedene Grenzen

Stand: 2026-11-05. Bedingte Analyse vorgegebener Historien und
Vergleichsensembles; **keine neue Dynamik oder Zielsimulation**.

## Entscheidungsrelevantes Ergebnis

Der [Altersfluss-Gegenbefund](collective_charge_constraints_2026-11-05.md)
hat einen begrenzten Ausweg: Eine vorgegebene periodische Historie mit
sehr langer Memory und kleinem Vergessen kann im Linienreadout einen
gleichgewichteten, divergenzfreien Umlauf ergeben. Die Reihenfolge der
Grenzgaenge ist wesentlich. Weder Existenz noch Stabilitaet solcher
nativer Bahnen ist nachgewiesen; der instabile alte FIFO-Anker wird
nicht rehabilitiert.

Auch ein idealer Umlauf genuegt nicht fuer die hier verglichene
klassische Coulomb-Phase. Fuer unabhaengig platzierte geschlossene
lokalisierte Fluesse mit endlichem geometrischem zweiten Moment
verschwindet die spektrale Amplitude mindestens quadratisch mit der
Wellenzahl. Die Coulomb-Referenz besitzt dagegen einen endlichen
transversalen Langwellenkoeffizienten. Ein auf seine Spur normiertes
Winkelbild kann diesen Unterschied verdecken.

Ein Ensemble kleiner unabhaengiger Knoten ist damit nicht schon das
benoetigte kollektive Medium. Ausgedehnte Strukturen oder ausreichend
starke kollektive Korrelationen koennten die folgenden Annahmen
verletzen, sind aber erst nachzuweisen.

## 1. Bedingter positiver Langmemory-Grenzfall

Seien $C_r(z)$ die exakten geglaetteten Linienfluesse der $P$ Segmente
einer vorgegebenen periodischen Polygonhistorie, in Altersreihenfolge.
Die Segmente schliessen einen Umlauf; die Historie wiederholt ihn
unbegrenzt. Fuer $q=1-\alpha$, $0<\alpha<1$, ergibt das native
geometrische Gewicht im **deklarierten Linienreadout** exakt

$$
F_\alpha(z)=M_0\alpha\sum_{j=0}^{\infty}q^j C_{j\bmod P}(z)
=M_0\sum_{r=0}^{P-1}p_r C_r(z),\qquad
p_r=\frac{q^r}{\sum_{s=0}^{P-1}q^s}.
$$

Dieses Objekt nutzt die geordnete Historie. Aus der skalaren Dichte
allein sind die Segmente und diese Stromdarstellung nicht automatisch
bestimmt.

Fuer festes $P$ und $\alpha\to0$ gilt $p_r\to1/P$, also

$$
F_0(z)=\frac{M_0}{P}\sum_{r=0}^{P-1}C_r(z),\qquad
\nabla\cdot F_0=0.
$$

Dieser bedingte Grenzfluss ist im Allgemeinen nicht null. Es gilt

$$
\sum_r|p_r-1/P|\leq
\delta_P(\alpha):=\min\{2,q^{-(P-1)}-1\},\qquad
\|F_\alpha-F_0\|\leq M_0\delta_P(\alpha)\max_r\|C_r\|.
$$

Begruendung: Der Mittelwert der Zahlen $q^r$ liegt zwischen $q^{P-1}$
und 1. Damit liegt $Pp_r$ zwischen $q^{P-1}$ und $q^{-(P-1)}$.
Fuer wachsendes $P$ ist $\alpha P\to0$ eine ausreichende Bedingung
fuer die Gewichtsgleichheit, nicht lediglich $\alpha\to0$.

Bei $N=mP$ behaltenen Segmenten, also $H=N+1$ Historienpunkten,
liefert dieselbe endliche geometrische Summe

$$
F_{\alpha,H}=(1-q^N)F_\alpha.
$$

Der Tail verschwindet bei $q^N\to0$; fuer $\alpha\to0$ erfordert dies
$\alpha N\to\infty$. Bei festem $H$ verschwindet stattdessen der
Fluss samt seiner nativen Gewichtssumme. Diese Reihenfolgen stimmen
mit der [Massennormierungsanalyse](fading_memory_limits_2026-11-04.md)
ueberein. $M_0/P$ ist Teil des Readouts, keine hergeleitete
Ladungseinheit. Ein physikalischer Zeitanschluss bei $P\to\infty$
muesste seine Normierung eigens festlegen.

Fuer endliches positives $\alpha$ bleiben Quellenreste im Allgemeinen
bestehen. Sogar der Fourierwert bei $k=0$ kann ungleich null sein:
$\widehat F_\alpha(0)=M_0\sum_r p_r\Delta y_r$, obwohl
$\sum_r\Delta y_r=0$. Der kleine-$k$-Grenzgang unten wird fuer den
idealen geschlossenen Umlauf ausgefuehrt; er darf nicht ohne
Fehlerbudget mit dem $\alpha$-Grenzgang vertauscht werden.

## 2. Kontrollierte Punkt-/Linienquadratur

Fuer einen geschlossenen Polygonzug mit Segmenten $v_r=b_r-a_r$, der
Fourierkonvention $e^{-ik\cdot x}$ und zunaechst ohne Glattung seien

$$
C_\Gamma(k)=\oint_\Gamma e^{-ik\cdot r}\,dr,\qquad
D_\Gamma(k)=\sum_r v_r e^{-ik\cdot b_r}.
$$

$D_\Gamma$ ist bis zur gemeinsamen Glattung und Normierung der
gleichgewichtete native **Verschiebungs**-Readout. Fuer
$L=\sum_r|v_r|$ und maximale Segmentlaenge $h$ gilt

$$
|D_\Gamma(k)-C_\Gamma(k)|
\leq\frac{|k|}{2}\sum_r|v_r|^2
\leq\frac{|k|Lh}{2}.
$$

Die erste Schranke folgt segmentweise aus
$|e^{-iu}-e^{-iv}|\leq|u-v|$ und Integration des Abstands zum neueren
Endpunkt. Normierte Gaussglattung multipliziert beide Seiten mit
$e^{-\sigma^2|k|^2/2}$. Das Produktionsfeld verwendet einen
unnormierten Gaussfaktor; dessen konstante Normierung ist gemeinsam
mitzufuehren und aendert die Fehlerordnung nicht.

Ein feiner Polygon-Grenzfall ist damit kontrollierbar. Es ist kein
Nachweis, dass native verrauschte Bahnen beschraenkte Laenge besitzen
oder diesen Grenzfall realisieren. Das `unit`-Orientierungsmodell ist
nicht ohne weitere Normierungs-/Parametrisierungspruefung derselbe
Readout. Produktionsfunktionen und Zeitparameter bleiben unveraendert.

## 3. Unabhaengige lokalisierte Umlaeufe verfehlen die Referenzphase

Betrachtet wird ein Vergleichsensemble im vorgegebenen aeusseren
3D-Raum, keine Memory-Vorhersage. Ein Loop $\Gamma$ sei ein
geschlossener rektifizierbarer Weg in euklidischem Raum, mit Laenge
$L$ und $|r|\leq R$ relativ zu einem mitgefuehrten Zentrum. Dann

$$
C_\Gamma(0)=0,\qquad k\cdot C_\Gamma(k)=0,\qquad
|C_\Gamma(k)|\leq |k|LR.
$$

Die Transversalitaet folgt durch Integration der totalen Ableitung
entlang des Wegs. Fuer die Schranke wird wegen $\oint dr=0$ im
Integranden 1 abgezogen. Mit $A=\tfrac12\oint r\times dr$ ergibt
Taylorentwicklung ausserdem

$$
C_\Gamma(k)=i k\times A+\mathcal R(k),\qquad
|\mathcal R(k)|\leq\frac{|k|^2LR^2}{2}.
$$

Nun seien die Loopzentren unabhaengig gleichverteilt in einer grossen
periodischen Box, die Formen und Staerken $g$ unabhaengig zwischen
Loops und unabhaengig von den Zentren. Nur euklidisch geschlossene,
nicht windende Loops werden verwendet. Fuer nichtverschwindende
reziproke Boxwellenzahlen entfallen die Kreuzterme durch den
Phasenmittelwert. Genauer definieren wir
$\widehat B(k)=\sum_a g_a e^{-ik\cdot x_a}C_{\Gamma_a}(k)$ und
$S(k)=V^{-1}\mathbb E[\widehat B(k)\widehat B(k)^\dagger]$ bei
Boxvolumen $V$. Bei Loopdichte $n$ folgt

$$
S(k)=n\,\mathbb E\left[g^2 C_\Gamma(k)C_\Gamma(k)^\dagger\right],
\qquad
\operatorname{tr}S(k)\leq n|k|^2\mathbb E[g^2L^2R^2].
$$

Vorausgesetzt werden endliche Dichte und ein im Grossvolumengrenzgang
gleichmaessig endliches Moment $\mathbb E[g^2L^2R^2]$. Eine endliche
mittlere Looplaenge allein reicht dafuer **nicht**. Bei einer festen
Form-/Staerkenverteilung mit isotropem Flaechenmoment
$\mathbb E[g^2 A A^{\mathsf T}]=a^2 I/3$ folgt durch dominierte
Konvergenz

$$
S_{ij}(k)=\frac{na^2}{3}
\left(|k|^2\delta_{ij}-k_i k_j\right)+o(|k|^2).
$$

Diese Herleitung setzt kein Paarpotential ein. Eine feste endliche
Gaussbreite multipliziert $S$ nur mit $e^{-\sigma^2|k|^2}$ und
entfernt die Unterdrueckung nicht.

Zum Vergleich ergibt eine **angenommene** isotrope klassische
Gaussverteilung mit Gewicht $\exp[-K\int |B|^2/2]$ und harter
Bedingung $\nabla\cdot B=0$ fuer jede von null verschiedene Mode

$$
S^{\rm C}_{ij}(k)=K^{-1}
\left(\delta_{ij}-\frac{k_i k_j}{|k|^2}\right),\qquad K>0.
$$

Das ist der langwellige statistische Referenzansatz bei
[Huse et al., Gl. (3)-(4)](https://arxiv.org/pdf/cond-mat/0305318v3),
keine auf Memory uebertragene Gleichgewichtsannahme. Seine zwei
transversalen Eigenwerte bleiben endlich; beim obigen Loopensemble
verschwinden sie. Es geht nicht um den Photonpropagator oder die
Quanten-Vakuumkorrelation. Auch passende statische Korrelationen
wuerden ohne Antwort-/Energieanschluss noch keine elektrische
Wechselwirkung beweisen.

**Fehlpositivkontrolle:** Nach Normierung durch $\operatorname{tr}S$
liefern beide fuehrenden Ausdruecke fuer $a^2>0$ dasselbe Winkelmuster.
Ein automatisch normiertes Bild kann den Amplitudenfehler verbergen;
eine nachtraegliche transversale Projektion kann zusaetzlich einen
Longitudinalfehler entfernen. Beides ersetzt keine native Bilanz. Ein spaeterer
Vergleich braucht die unnormierte, volumenkontrollierte Amplitude und
den kleine-$k$-Bereich; hier wird kein Ziellauf vorbereitet.

Der Ausschluss gilt nur unter den genannten Ensemble- und
Momentannahmen. Makroskopische Winding-Loops, breite Groessenverteilungen
mit divergierendem Moment oder kollektive Kreuzkorrelationen sind
nicht erfasst. Eine auf dem Torus geschlossene windende Linie ist in
ihrem euklidischen Lift offen und kann einen nichtverschwindenden
Nullmodus besitzen. Kein allgemeines No-go fuer kollektive Memory-Phasen.

## 4. Literaturabgleich

Jaubert, Haque und Moessner, *Analysis of a Fully Packed Loop Model
Arising in a Magnetic Coulomb Phase*, PRL 107, 177202 (2011),
untersuchen ein dicht gepacktes Zweifarben-Loopmodell des Spin Ice.
Sie finden makroskopisch windende Loops, obwohl die ueber Loops
gemittelte Laenge endlich bleibt. Das illustriert, weshalb unser
staerkeres Momentkriterium und die Winding-Unterscheidung notwendig
sind. Ihre Farbloops werden von alternierenden Flusswegen
unterschieden; nicht jede Darstellung ist unser $C_\Gamma$. Dies
sind keine Messungen an Memory.
[Primaervolltext](https://arxiv.org/pdf/1103.5397v1),
[Publikation](https://doi.org/10.1103/PhysRevLett.107.177202).

Sena Watanabe, Yukitoshi Motome und Haruki Watanabe, *Topological
Phase Transitions and Their Thermodynamic Fate in Arbitrary-S
Classical Pyrochlore Spin Ice*, PRX 16, 041016, erschienen am
**14.10.2026**, trennen ebenfalls eine Phase lokaler geschlossener
Anregungen von kollektiven Coulomb-Regimen. Ihr Modell setzt Gitter,
diskrete Spinwerte und Boltzmann-Gewichte voraus. Die streng
monopolfreie Grenze wird vom thermischen Defektanteil getrennt; im
behandelten kleinen-w-Coulomb-Regime fuehren solche Defekte zu
Abschirmung. Das unterstreicht die Bedeutung der Grenzfolge, liefert
aber keine Memory-Temperatur oder Spinquantisierung. Andere
Phasenuebergaenge dieser Arbeit werden hier nicht bewertet.
[Primaervolltext](https://journals.aps.org/prx/pdf/10.1103/bkkq-q1v9).

## 5. Konsequenz und Verifikation

Der positive Umlauf-Grenzfall bleibt erhalten, aber nicht als
Teilchen-/Feldnachweis. Ein weiterer Anschluss muesste zugleich
native Bahn-/Zustandskontrolle und eine kollektive Antwort jenseits
des unabhaengigen endlichen Loopensembles liefern. Mehr Umlaeufe
desselben alten Ankers oder Spektralnormierung schliessen diese
Luecke nicht. Keine neue physikalische Regel wird ausgewaehlt;
die Autorenentscheidung bleibt offen. Die einzige Arbeitsreihenfolge
steht in den [Projektprioritaeten](../../docs/status/project_priorities.md).

Die [konstruierten Kontrollen](../../tests/test_loop_flux_limits.py)
pruefen geometrische Summen mit nativen Gewichten, endlichen Tail,
ungleichgewichteten Nullmodus, Punkt-/Linienquadratur, Flaechenentwicklung,
verschleiernde Spektralnormierung, Gaussglattung und ein Winding-
Gegenbeispiel. Kein Zufallslauf, keine Parameteranpassung und keine
neue Produktionsdynamik.

Verifikation am 2026-11-05: **91 betroffene Tests bestanden in 2.32 s**,
darunter 12 neue konstruierte Kontrollen. Ruff, strikter MkDocs-Bau
und Whitespacepruefung bestehen. Keine vollstaendige Repository-
Testsuite, kein formales Beweiszertifikat und keine eigene Reproduktion
der Literatur-Simulationen. Die bestehenden Zielpanels bleiben geschlossen.

Quellenumfang: Jaubert et al. arXiv-v1 vom 28.03.2011, Einleitung,
Loopdefinition, Verteilungs-/Winding-/Mittellaengenanalyse bis S. 3;
Journal/DOI und Publikationsdatum ueber APS bestaetigt. Watanabe et al.
in der veroeffentlichten PDF-Fassung: Abstract, Modell in Abschnitt II,
kleines-w-Regime in III B und einschlaegige Passagen in VI/VI A.
Kein vollstaendiger Audit der Klassifikation, Zusatzmaterialien oder
Numerik. Huse et al. wie im vorigen Bericht, Gl. (3)-(4).
Die gezielte Literatur- und DOI-Korrektursuche am 2026-11-05 ist kein
systematischer Review; kein einschlaegiges Erratum wurde gefunden.
