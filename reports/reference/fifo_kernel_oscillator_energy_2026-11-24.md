# Ein schwingender FIFO-Kernel mit eigener Energiebilanz

Stand: 2026-11-24. Deterministischer Skalarvergleich,
aufbauend auf der [nativen Potentialbilanz](../../docs/reference/memory_pair_energy.md).
Keine Aenderung der Produktionsdynamik, kein
Zieltrajektorienlauf, kein thermischer oder Quanten-Nachweis.

**Ergebnis.** Die Modulation des Kernels kann ihre
Energie reziprok mit einem Oszillator austauschen.
Beim nativen FIFO-Schreiben bleibt daneben ein eigener
Arbeitsterm offen. Ein konstanter repulsiver Kernel kann
eine gleichfoermige Zweiplatz-Loesung unterhalten, bei der
die gespeicherte Energie exakt konstant ist, aber pro
Schritt positive Arbeit ins Lesepotential fliesst.
An einem eingefrorenen Gleichgewicht kann ein passiver
Oszillator negative statische Kruemmung nicht durch seine
Frequenz stabilisieren.

## 1. Kontrollmodell und diskrete Buchung

Sei $Y=(y_0,\ldots,y_{H-1})$ eine gefuellte Historie,
juengster Eintrag zuerst. $U_0(x;Y)$ und $U_1(x;Y)$
seien zwei gewichtete Gauss-Potentiale mit
$w_j=(1-q)q^j$, $0\le q<1$. Der
zeitabhaengige Kernel entsteht aus $K_0+aK_1$.
Fuer dieses deklarierte Referenzmodell gilt

$$
E(x,Y,a,p)=U_0(x;Y)+aU_1(x;Y)
         +\frac{p^2}{2I}+\frac{\kappa a^2}{2},
\qquad I,\kappa>0.
$$

Die beiden Gauss-Komponenten gehen bei grossem
Abstand gegen null. Diese Festlegung ist relevant:
Ein nur von $a$ abhaengiger Zusatz zum Potential
wuerde die Kraft auf $a$ aendern, obwohl er den
Gradienten in $x$ nicht aendert.

Der [Referenzschritt](../../experiments/current/reference/fifo_kernel_oscillator.py)
zerlegt exakt in drei Teiloperationen:

1. **Bewegung.** Mit festem $Y,a,p$ wird der
   native rauschfreie Gradienten-Schritt
   $x'=x-\eta\nabla_x(U_0+aU_1)$ gesetzt.
   Die Potentialaenderung heisst $W_x$.
   Mit einer uniformen Hesse-Schranke $L$ und
   $\eta L<2$ ist $W_x\le0$, strikt negativ
   bei nichtverschwindender Bewegung. Die
   Implementierung weist groessere Schritte
   zurueck, statt moegliches Ueberschwingen
   als Energiebefund zu werten.
2. **Oszillator.** Mit festem $x',Y$ gilt
   $\dot a=p/I$, $\dot p=-\kappa a-U_1(x';Y)$.
   Dies ist ein exakt integrierbarer harmonischer
   Umlauf um $a_*=-U_1(x';Y)/\kappa$.
   Die Modulationsarbeit
   $W_K=(a'-a)U_1(x';Y)$ ist exakt das Negative
   der Aenderung der nackten Oszillatorenergie
   $p^2/(2I)+\kappa a^2/2$.
3. **Schreiben.** Bei festem $x',a',p'$ werden
   $x'$ geschrieben und die alten Positionen
   um einen Platz verschoben. Der entstehende
   Potentialterm $W_{\rm FIFO}$ wird getrennt
   gebucht. Es ist **nicht** festgelegt, welche
   physikalische Quelle ihn bezahlt.

Die Gueltigkeit der Hesse-Schranke in Teil 1
folgt fuer jede Gauss-Komponente aus
$\|D^2 G_\sigma\|\le1/\sigma^2$. Die
Summenschranke ist die Summe der Gewichte
mal der Summe beider absoluten
Amplituden durch die jeweiligen Breitenquadrate.
Der Oszillatorschritt ist analytisch, kein
Rueckschluss aus einer kleinen Residualzahl.
Fuer volle Referenzschritte lautet die Bilanz
$E'-E=W_x+W_{\rm FIFO}$.
Wird der Kernel stattdessen von aussen
vorgegeben, ist $W_K$ eine separate
Parameterarbeit, ohne den Gegenposten im Oszillator.

## 2. Welche Arbeit das FIFO-Schreiben leistet

Schreibe $K=K_0+a'K_1$ beim Schreiben und
setze $\delta w_j=w_j-w_{j+1}$ mit $w_H=0$,
letzteres nur fuer die Randbuchung. Dann gilt

$$
W_{\rm FIFO}=\sum_{j=0}^{H-1}
 \delta w_j\,[K(0)-K(x'-y_j)].
$$

Die Gewichtsverluste sind nichtnegativ und
summieren sich zu $w_0$. Der Ausdruck ist die
Selbstkanal-Spezialisierung der aelteren Bilanz
fuer Schreiben, Altern und Ausscheiden.
Er zeigt zusaetzlich das Vorzeichen direkt:
Bei globalem Maximum von $K$ im Ursprung
kann der Schreibschritt das Lesepotential nur
erhoehen oder unveraendert lassen; bei Minimum
nur absenken oder unveraendert lassen.
Das gilt phasenweise auch fuer einen schwingenden
Kernel. Abwechselnde Vorzeichen von $a$
erzwingen keine Summe null, da die gelesenen
Abstaende ebenfalls wechseln.

### Nativer konstanter Kernel: positiver Durchsatz ohne Energiespeicherung

Bei $H=2$ und rein repulsivem $K=A G_\sigma$,
$A>0$, ist $x_{n+1}=x_n+d$ eine exakte
rauschfreie Loesung, falls

$$
g=e^{-\|d\|^2/(2\sigma^2)},\qquad
\eta A w_1g/\sigma^2=1,\qquad d\ne0.
$$

Sie existiert fuer $\eta A w_1/\sigma^2>1$.
Das gefuellte Fenster am Anfang ist
$(x_n,x_n-d)$. Das bedingte Lesepotential
faellt beim Schritt von $A(w_0+w_1g)$
auf $A(w_0g+w_1g^4)$: Beide Abstaende
wachsen, obgleich die allgemeine Hesse-Schranke
fuer diese Loesung nicht klein genug ist.
Das Schreiben stellt exakt den Ausgangswert her.
Somit

$$
W_{\rm FIFO}=-W_x
=A\left[w_0(1-g)+w_1(g-g^4)\right]>0 .
$$

Die gespeicherte Energie bleibt endlich und konstant,
der kumulierte Schreibbeitrag waechst linear mit der
Schrittzahl. Das ist ein exakter Gegencheck zur
Interpretation, unendlicher Durchsatz muesse
unbeschraenkt gespeicherte Energie bedeuten.
Der Zweiplatzfall belegt weder gebundene
Knoten noch eine mikroskopische Energiequelle;
es ist eine analytische Substitution, kein
neu gestarteter nativer Lauf.

Bei periodischer Bewegung der relativen Geometrie
und wiederkehrendem Oszillator ist dagegen
$\sum W_{\rm FIFO}=-\sum W_x$ **notwendig**
in der hier bilanzierten ueberdaempften Regel.
Ohne Schreiben, oder wenn das Schreiben durchweg
nur Energie abgibt, kann ein solcher Zyklus
mit striktem Bewegungsverlust nicht periodisch sein.

## 3. Der Oszillator ist nicht automatisch eine Stabilisierung

Bei eingefrorenem $Y$ minimiert der statische
Oszillator die Energie bei $a=-U_1/\kappa$, $p=0$.
Sein statischer Gegenvergleich ist daher

$$
U_{\rm eff}(x;Y)=U_0(x;Y)-U_1(x;Y)^2/(2\kappa).
$$

Dies ist bei mehreren Deposits im Allgemeinen
kein neuer linearer Gauss-Kernel: Das Quadrat
enthaelt Produkte verschiedener Depositbeitraege.
An einem Gleichgewicht seien
$A=D_x^2(U_0+a_*U_1)$ und $c=\nabla_x U_1$.
Die effektive Hesse-Matrix ist
$A-cc^T/\kappa$. Bei $\mu>0$ als
ueberdaempfter Mobilitaet und optionaler
Oszillatorreibung $\gamma\ge0$ liefert
eine reell wachsende Mode mit Rate $\lambda>0$
nach Eliminieren von $a$ die Bedingung

$$
\left(\frac{\lambda}{\mu}I_d+A-
 \frac{cc^T}{\kappa+\gamma\lambda+I\lambda^2}\right)u=0.
$$

Hat die statische Matrix eine negative Richtung,
dann ist der kleinste Eigenwert des symmetrischen
Ausdrucks bei null negativ und bei grossem
$\lambda$ positiv. Also gibt es einen reell
positiven Wachstumswert unabhaengig von $I$.
Wahl der Eigenfrequenz rettet diese statische
Instabilitaet nicht. Bei strikt positiver
statischer Matrix ist die quadratische
Gesamtenergie positiv und dissipativ, also
gibt es keine wachsende lineare Mode.
Entkoppelte neutrale Oszillationen sind
ohne Reibung damit nicht ausgeschlossen.
Der Beweis gilt bei **eingefrorener**
Historie, nicht fuer die volle
verzoegerte oder eine extern getaktete Regel.

Die festen Gauss-Kontrollen enthalten ein
Gleichgewicht mit positiver Kruemmung bei
festgehaltenem $a$, aber negativer effektiver
Kruemmung, sowie einen stabilen Gegenfall.
Die freie Modulation darf deshalb fuer einen
spaeteren Vergleich nicht nur gegen $K_0$,
sondern auch gegen $U_{\rm eff}$ getestet werden.

## 4. Was ein Zufallstest testen muss

Schon ohne weitere Innovation ist das
ausgeblendete $a$ ein Memory-Freiheitsgrad:
Eliminieren des ungedaempften Oszillators
liefert neben seiner freien Anfangsschwingung
die Antwort

$$
a(t)=a_{\rm frei}(t)-
 \frac{1}{I\omega}\int_0^t\sin[\omega(t-\tau)]
 U_1(x(\tau);Y(\tau))\,d\tau,\qquad
\omega=\sqrt{\kappa/I},
$$

fuer die kontinuierliche Variante, in der der
Oszillatorzustand bei FIFO-Spruengen nicht
zurueckgesetzt wird. Zufallswerte nur am
Anfang erzeugen korrelierte Schwankungen, nicht
laufende neue Energiezufuhr. Frische zufaellige
Kernel-Updates oder ein dissipativer stochastischer
Oszillator benoetigen dagegen eine gebuchte
Antriebs- bzw. Badkopplung. Kein Zufallstest
oder Stabilisierungslauf wird hier behauptet.

**Literatur und Umfang.** [Sekimoto (1997)](https://www.jstage.jst.go.jp/article/jpsj/66/5/66_5_1234/_article/-char/en)
liefert den Begriff der stochastischen Energetik;
[Kopp und Klapp (2024)](https://arxiv.org/abs/2408.03316)
untersuchen Waermeproduktion bei verzoegerter
repulsiver Rueckkopplung in einer anderen
Langevin-Dynamik. [Zwanzig (1973)](https://doi.org/10.1007/BF01008729)
leitet Memory-Antworten aus angekoppelten
harmonischen Baedern ab. Die diskrete FIFO-Bilanz,
der Zweiplatz-Durchsatz und die angegebene
Stabilitaetsschranke sind Rechnungen fuer
die hiesigen Annahmen, keine Uebertragung
der dortigen Thermodynamik oder eines
Fluktuations-Dissipationssatzes auf das FIFO.

[Kontrollen](../../tests/test_fifo_kernel_oscillator.py):
die reziproke Einzeloperation, der explizite
Schreibterm fuer beide Vorzeichen, das
exakte Zweiplatz-Inkrement und die
lineare eingefrorene Antwort. Naechste
Entscheidung: erst die Energiequelle oder
Rueckbuchung des Schreibens spezifizieren,
dann deterministische und stochastische
Modulation bei gleicher Bilanz vergleichen.
