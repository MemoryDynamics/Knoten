# Wann ein zweiter FIFO das 360-Grad-Minus sehen kann

Stand: 2026-11-22. Analytische Gegenprobe zur
[aktiven 4D-FIFO-Referenz](../../docs/reference/fifo_4d_spin_projection.md).
Zwei vorbereitete Speicher, vorhandener skalarer Kernel als Auslese,
ergaenzt um einen internen Rueckkopplungstest ueber einen Umlauf.
Keine Rueckkopplung auf eine 3D-Bahn, keine native Zieltrajektorie.

**Ergebnis.** Eine 3D-Auslese, die nur die Rahmen der beiden FIFOs
empfaengt, ist fuer das relative Minus exakt blind. Im gemeinsamen
4D-Vergleichsraum kann der vorhandene Gauss-Kernel es dagegen sehen.
Fuer den kohaerenten Achtphasen-Umlauf ist diese Auslese genau dann bei
*allen* Abfragephasen blind, wenn antipodale Phasen dasselbe gefaltete
Altersgewicht haben. Gleichfoermige Zeitmittelung eines ruhenden
Empfaengers und ein mitlaufender Referenz-FIFO sind nicht gleichwertig.

## 1. Was die 3D-Rahmen nicht verraten

Der aktive FIFO hat $F^4 Q=-Q$. Der Rahmen $R(u)$ des einzelnen
4D-Eintrags erfuellt $R(-u)=R(u)$. Daher haben $Q_B$ und $-Q_B$
dieselbe ganze Rahmenfolge: $F$ ist linear und kommutiert mit der
Vorzeichenumkehr. Dasselbe gilt fuer jede Altersfunktion dieser
Rahmen und fuer die zugehoerige Pfeilprojektion. Haelt man die
aeusseren 3D-Orte fest, kann **keine** Auslese, die nur diese Daten
beider Knoten empfaengt, die beiden Faelle unterscheiden. Auch eine
adaptive Abfrage derselben Daten erzeugt keinen Unterschied.

Das ist eine Aussage ueber den Informationszugang, nicht ueber
alle moeglichen 3D-Detektoren. In der Quantenreferenz wird der
Zugriff ueber die Rekombination kohaerenter Wege realisiert, siehe
[Rauch et al. (1975)](https://doi.org/10.1016/0375-9601(75)90798-7).
Der nachfolgende klassische Vergleich setzt keine Superposition
oder Born-Regel voraus.

## 2. Derselbe Gauss-Kernel mit Zugriff auf vier Komponenten

Schreibe $u(\alpha)=U(2\alpha)u_0$ fuer den normierten koharenten
Referenzumlauf und $\varphi=\pi/4$ fuer den inneren Fortschritt pro
Schritt. Im gemeinsamen internen Koordinatensystem vergleicht der
beobachtende Kopf $u(\delta)$ sich mit den Quellen des anderen
FIFO-Fensters $u(-j\varphi)$. Dann ist

$$
\|u(\delta)-u(-j\varphi)\|^2=2-2\cos(\delta+j\varphi).
$$

Ein Minus nur an der Quelle ersetzt $\delta$ durch $\delta+\pi$;
ein gemeinsames Minus beider Knoten aendert den Vergleich nicht. Setze
$W_r=\sum_{j\equiv r\,({\rm mod}\,8)}w_j$ fuer die pro Phase addierten
Altersgewichte, mit $W_r=0$ bei nicht belegten Restklassen.
Fuer eine endliche Summe effektiver radialer Gauss-Kernel lautet das
Ergebnis der Auslese

$$
C(\delta)=\sum_{r=0}^7 W_r K_*(\delta+r\varphi),\qquad
K_*(t)=\sum_\ell A_\ell e^{-\kappa_\ell}e^{\kappa_\ell\cos t},
\qquad \kappa_\ell=\sigma_\ell^{-2}>0.
$$

Das ist der vorhandene skalar-radiale Algorithmus, aber angewendet
auf **interne** Koordinaten statt auf 3D-Ortsdeposits. Dieser Zugriff
ist eine Hypothese, keine Eigenschaft der nativen Ortskopplung.

### Exaktes Kriterium

**Satz.** Fuehre man gleiche Breiten zusammen und entferne Terme
mit Amplitude null. Ist mindestens ein Term uebrig, gilt

$$
C(\delta+\pi)=C(\delta)\ \text{fuer alle }\delta
\quad\Longleftrightarrow\quad
W_r=W_{r+4}\quad (0\leq r<4).
$$

Die gleiche Bedingung gilt, wenn statt des Potentials nur seine
tangentiale Ableitung $C'$ ausgelesen wird.

**Beweis.** Symmetrische Gewichte paaren die antipodalen Quellen
und machen deren Tausch unsichtbar, sogar fuer den Feldwert und
vollen Gradienten an beliebigen Abfragepunkten. In Gegenrichtung
hat die $m$-te Winkelharmonische den Faktor
$\sum_r W_r e^{imr\varphi}$ mal
$b_m=\sum_\ell A_\ell e^{-\kappa_\ell}I_{|m|}(\kappa_\ell)$.
Hier ist $I_m$ die modifizierte Bessel-Funktion; siehe
[NIST DLMF 10.35.2](https://dlmf.nist.gov/10.35.E2).
Aus der [Potenzreihe](https://dlmf.nist.gov/10.25.E2) folgt fuer
festes $a>0$, dass $I_m(a)/[(a/2)^m/m!]\to1$:
Der normierte Rest ist hoechstens
$\exp(a^2/(4(m+1)))-1$. Somit dominiert fuer hinreichend grosse
$m$ die groesste verbleibende $\kappa_\ell$ auch bei gemischten
Vorzeichen. Der Koeffizient $b_m$ ist dann ungleich null.
$\pi$-Periodizitaet erzwingt daher in jeder der vier ungeraden
Restklassen modulo acht das Verschwinden des Gewichtsfaktors.
Diese vier diskreten Fourier-Koeffizienten sind genau die
Koeffizienten der antisymmetrischen Gewichtsdifferenz
$(W_r-W_{r+4})_{r\bmod 8}$ bis auf einen Faktor zwei.
Fourier-Inversion liefert die Behauptung. Die Ableitung
multipliziert die ungeraden Moden nur mit $im\ne0$.

Insbesondere ist das Vierplatzfenster mit positiven Gewichten
nicht blind, waehrend acht gleich gewichtete Phasen blind sind.
Ein einzelner gepruefter Winkel oder eine einzelne Harmonische
entscheidet das nicht. Zwei Breiten koennen die erste Harmonische
exakt ausloeschen und hoehere ungerade Harmonische uebrig lassen.
Umgekehrt garantiert der Satz keine praktisch aufloesbare
Signalstaerke.

## 3. Ruhender und mitlaufender Empfaenger

Bei festgehaltenem 4D-Abfragepunkt tauschen sich die Quellen nach
vier Updates genau gegen ihre negierten Varianten aus. Das Mittel
ueber einen kompletten Achtzyklus ist deshalb fuer $Q_B$ und
$-Q_B$ gleich, ebenso das gemittelte Gradientenreadout. Wenn der
zweite FIFO kohaerent mitrotiert, wenden dagegen **beide** Seiten
in jedem Schritt dieselbe orthogonale Matrix an. Alle von ihm
abgefragten Abstaende und damit $C(\delta)$ bleiben gleich.
Ein vorhandener relativer Kontrast bleibt im Mittel erhalten.
Beides sind Ausleseprotokolle, keine Aussage ueber spontane
Synchronisation unter Rueckkopplung oder Rauschen.

## 4. Konsequenz fuer den physikalischen Anschluss

### Antiparallele Spinrichtungen und Kernelvorzeichen getrennt pruefen

$(u,-u)$ beschreibt gleiche 3D-Richtungen, nicht antiparallele.
Fuer den getrennten Antiparallel-Kontrollfall drehen wir das
gesamte zweite Startfenster mit $U_z(\pi)$ und verwenden den
Startkopf mit Richtung $+e_x$. Dann liegen die beiden Richtungen
bei $+e_x$ und $-e_x$ und der interne Phasenversatz hat Betrag
$\pi/2$, nicht $\pi$. Die Orientierungen dienen hier
als Labels der ausgewaehlten 4D-Historien, nicht als Ladungen.

Am selben Paar werten wir in beiden Leserichtungen den rohen
Drift $f_A=-\nabla C_{A\leftarrow B}$ und $f_B$ analog aus,
einmal fuer $K=+G_1$ und einmal fuer $K=-G_1$, mit
$G_1(z)=\exp(-\|z\|^2/2)$ und Gewichten $(1,1/2,1/4,1/8)$.
Diese festen Kontrollwerte sind keine Parameterwahl fuer einen
Teilchenkandidaten. Der reine Kreuzbeitrag erster Ordnung zur
halben quadratischen Distanz der internen Koepfe ist
$D=(u_A-u_B)\cdot(f_A-f_B)$. Fuer $+G_1$ ergibt sich $D>0$,
fuer $-G_1$ ist es genau das negative $D<0$. Bei vollstaendiger
Vorzeichenumkehr wechselt jeder Kreuzdrift das Vorzeichen;
ob ein anderer Kernel oder ein anderer Abstand anzieht, bestimmt
der Gradient, nicht allein der Wert des Potentials. Das ist
keine Aussage ueber einen realen 3D-Abstand oder eine Bindung.
Ein nur von 3D-Ortsdeposits gespeister Kernel aendert sich bei
gleichbleibenden Ortsdaten mit keiner dieser Spinrichtungen.
Das Kernelvorzeichen bleibt fuer physikalische Kandidaten offen.

### Dynamischer Vorzeichentest ueber einen Umlauf

Der momentane Drift ist noch kein Test der verzoegerten Dynamik.
In einem begrenzten Referenzmodell wird zunaechst der aelteste
Eintrag negiert und als neuer Kopf vorgeschlagen. Auf diesen
Vorschlag wirkt der Gauss-Gradient des **bisherigen** Fensters
der jeweils anderen Seite. Beide Koepfe werden danach auf die
Einheitssphaere normiert und gleichzeitig uebernommen. Sonst
bleibt die FIFO-Regel unveraendert. Beide Lesrichtungen haben
dasselbe vorzeichenbehaftete Gewicht $\lambda$; Breite, Altersgewichte
und Startfenster sind fest. Getestet wird die gemeinsame Umkehr
beider Kreuzkopplungen, nicht ein Vorzeichenwechsel nur in einer
Leserichtung. Das ist ein gesetzter interner Vergleich, keine
native 3D-Wechselwirkung.

Alle Eintraege bleiben in derselben 4D-Umlaufebene. Sei
$\delta$ die innere Phase von B minus A und $\alpha_j=(j+1)\pi/4$;
der zusaetzliche Schritt in $\alpha_j$ kommt vom vorgeschlagenen
Kopf gegenueber dem alten Quellfenster. Die tangentiale
Korrektur pro neuem Kopf ergibt sich aus dem Skalarprodukt des
negativen Gradienten mit dem Tangentenvektor; die Normierung
entfernt in erster Ordnung nur den radialen Anteil.
Die Differenz der beiden Winkelkorrekturen ist $\lambda H(\delta)$
in erster Ordnung, mit

$$
H(\delta)=\sum_{j=0}^3 w_j
\left[
 e^{-1+\cos(\alpha_j+\delta)}\sin(\alpha_j+\delta)
 -
 e^{-1+\cos(\alpha_j-\delta)}\sin(\alpha_j-\delta)
\right].
$$

Die Negation eines alten Eintrags fuegt seiner Phase $\pi$ hinzu,
laesst aber einen bereits angesammelten Winkelfehler unveraendert.
In acht Schritten wird jeder Platz zweimal neu beschrieben. Auf
dem ungekoppelten, gemeinsam rotierenden Paar ist $H$ in allen
acht Schritten gleich. Mit $\delta_0=\pi/2$ lautet deshalb fuer
jeden der vier Plaetze die relative Phase nach einem Umlauf

$$
\delta_8-\frac{\pi}{2}
 = 2\lambda H(\pi/2)+O(\lambda^2)
 = \frac{4\lambda}{e}
 \left[\frac{w_0-w_2}{\sqrt{2}}\cosh(1/\sqrt{2})-w_3\right]
 +O(\lambda^2).
$$

Die Steigung ist bei den festen Gewichten etwa $0.800$.
Die Nullkontrolle kehrt exakt zurueck; bei kleiner positiver
Kopplung wachsen die Abstaende der entsprechenden **internen**
Eintraege, bei negativer schrumpfen sie. Trotzdem weichen die
ausgelesenen 3D-Pfeile in beiden Faellen vom antiparallelen Start
ab: Nahe $\delta=\pi/2$ ist ihr Winkel
$\pi-2|\delta-\pi/2|$. Der ungerichtete 3D-Winkel zeigt somit
die Abweichung, aber nicht ihr Vorzeichen in erster Ordnung.
Die feste Acht-Schritte-Kontrolle prueft $\lambda=0$ und
$\lambda=\pm10^{-5}$ gegen die analytische Steigung; sie sucht
weder nach stabilen Fenstern noch nach einem passenden Kernel.
Ein interner Abstandsverlust ist kein Nachweis einer 3D-Bindung
oder zweier entgegengesetzter Ladungen.

### Offene Herleitung

Der positive Kontrollfall hat bereits eine gemeinsame interne
Referenz zwischen den beiden Knoten eingebaut. Sollen lokale
Komponentenbasen getrennt waehlbar sein, waere ein gemischter
Skalar $u_A^T T_{AB}u_B$ nur dann basisunabhaengig, wenn
$T_{AB}$ bei Basiswechseln $u_k\mapsto U_k u_k$ als
$T_{AB}\mapsto U_A T_{AB}U_B^T$ mittransformiert. Das ist
eine Bedingung fuer diesen Vergleichsansatz, kein Nachweis
eines Transportfelds. Ein nur aus Einzelrahmen gebauter
Vergleich kann die fehlende Information nicht ersetzen.

Der naechste diskriminierende Schritt ist daher ein aus
gemeinsamer Memory-Dynamik hergeleiteter relativer Vergleich,
der nicht beim vorgesehenen physikalischen Grobkoernen
verschwindet. Erst dann waere zu testen, ob das Signal
auf die 3D-Dynamik zurueckwirkt. Der jetzige Vergleich
zeigt weder Bindung noch Quantisierung noch emergenten Spin.

Der [Vergleich gespeicherter 3D-Drehwege](fifo_relative_frame_lift_2026-11-22.md)
unterscheidet sich davon: Er braucht keine gemeinsame 4D-Basis,
aber nachweisbar verschiedene, aufgeloeste Rahmenfolgen. Er
unterscheidet nicht $Q_B$ von $-Q_B$ bei identischen Rahmenfolgen.

Die [festen Kontrollen](../../tests/test_fifo_4d_relative_phase.py)
werten vorhandene Potentiale und Gradienten direkt aus. Sie pruefen
beide Zeitmittel, das vollstaendige Rahmenbild, die antipodalen
Gewichte, die Ausloeschung nur der ersten Harmonischen, beide
Kernelvorzeichen fuer antiparallele Richtungen und den
dynamischen Vorzeichenwechsel nach einem Umlauf.
