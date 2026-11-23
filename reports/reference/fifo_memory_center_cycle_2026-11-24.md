# Eine konservative Kraft aus dem FIFO-Zentrum

Stand: 2026-11-24. Fortsetzung des
[autonomen Taktvergleichs](fifo_carrier_clock_cycle_2026-11-24.md).
Klassische Hamilton-Referenz mit idealem Schreibschnitt, keine
Aenderung der nativen Regel und kein Zieltrajektorienlauf.

**Ergebnis.** Eine reziproke Kraft aus den gespeicherten Orten
erhaelt den exakten vorbereiteten Zwei-Write-Zyklus. Sie aendert
die Querantwort, macht die Bahn aber nicht stabil. Das Mittel der
beiden juengsten Orte gibt fuer jede ungerade Laenge ab drei
einen wachsenden Querort mit Faktor ueber zwei je Write.
Jedes kompatible konvexe Zentrum mit positivem Gewicht des
juengsten Orts ist instabil. Fuer eine Laenge von drei ist
auch die einzige uebrige Wahl nicht linear beschraenkt.

## 1. Kraft, Gegenimpuls und exakte Rueckkehr

Mit $y_0$ als juengstem Eintrag sei $M=\sum_{j=0}^{H-1}w_j y_j$,
mit $w_j\ge0$ und $\sum_j w_j=1$. Waehrend eines Flugs setzen wir
statt der direkten Relativfeder

$$
E_{\rm int}=
\frac{|P_x|^2+|P_b|^2}{2m}
+\frac{m\omega^2}{2}\left(|x-M|^2+|b-M|^2\right).
$$

Kopf und Traeger schwingen um dasselbe ausgelesene Zentrum.
Es gibt keinen ortsfesten externen Anker. Die Speicherorte
stehen im Flug still, weil $E_{\rm int}$ keine Speicherimpulse
enthaelt. Sie nehmen aber die Gegenimpulse auf:
$\dot P_{y_j}=-w_j(\dot P_x+\dot P_b)$. Dies erhaelt den
Gesamtimpuls. Das Potential ist translations- und
rotationsinvariant. Die fehlende Bewegung der Speicherorte
ist weiter eine Modellannahme, keine endliche Traegheit.
Der freie Rotor und die reversible Schreibkarte bleiben
unveraendert; der Rotor bezahlt weiterhin einen etwaigen
Energiesprung an der Schreibflaeche.

Fuer ungerades $H\ge3$ und ausgeglichene Paritaetsgewichte
$\sum_j(-1)^j w_j=0$ ist $M=0$ auf der frueheren Grundbahn:
$x=A$, $b=-A$, $y_j=(-1)^{j+1}A$, alle Impulse null.
Der Kopf schreibt exakt und der Traeger behaelt den alten
letzten Eintrag. Der Write wechselt das Vorzeichen aller
Registerorte, nicht das von $x$ oder $b$, und laesst $M=0$.
Er kostet hier keine Arbeit.
Waehlt man den freien Rotor wie zuvor fuer die Halbperiode
$T=\pi/\omega$, tauschen $x$ und $b$. Die Speicherimpulse
kehren auf diesem Flug ebenfalls auf null zurueck. Nach dem
zweiten Write und Flug ist der ganze Zustand wiederhergestellt.
Das zeigt Existenz fuer die vorbereitete Bahn, nicht deren
autonome Herstellung aus generischen Anfangsdaten.

## 2. Der Querblock liest das Gedaechtnis

Auf der kollinearen Grundbahn aendert ein Querfehler die
Arbeit am Write und damit die Rotorflugzeit erst in zweiter
Ordnung. Die Querableitung ist daher die kanonische Schreibkarte
gefolgt von einem Flug bei der Halbperiode. Bezeichne den
alten letzten Eintrag mit $t=y_{H-1}$ und die geschriebenen
Register mit $y'_0=x+b-t$, $y'_j=y_{j-1}$ fuer $j\ge1$.
Das gelesene Zentrum ist jetzt $M'=\sum_j w_j y'_j$.
Bei der Halbperiode sind Kopf- und Traegerort an $M'$
gespiegelt. Der Ortsblock $B$ der Querableitung lautet

$$
x_{\rm neu}=2M'-x,\qquad
b_{\rm neu}=2M'-t,\qquad
(y_j)_{\rm neu}=y'_j.
$$

Die Orte haengen in diesem Flug nicht von Impulsen ab und
umgekehrt. Zusammen mit dem kanonischen Write ist der volle
Querblock somit $\operatorname{diag}(B,B^{-T})$. Bei beiden
Halbzyklen ist er gleich, die volle Rueckkehr hat sein Quadrat.
Die Symmetriereduktion einer periodischen Rueckkehr ist ein
bekannter Vergleichspunkt
([Lamb und Wulff](https://arxiv.org/abs/patt-sol/9704002));
die Matrix hier enthaelt ausdruecklich den Schreibschritt.

Zur charakteristischen Gleichung: Fuer $\lambda\ne0$ eliminiere
die Shift-Zeilen mittels $y_j=\lambda^{-j}y_0$. Mit
$S(\lambda)=\sum_jw_j\lambda^{-j}$ gilt $M'=\lambda S(\lambda)y_0$,
weil alle geschriebenen Register Eigenvektorgleichungen erfuellen.
Die drei verbleibenden Zeilen sind
$(\lambda+1)x=2\lambda S(\lambda)y_0$,
$\lambda b=2\lambda S(\lambda)y_0-t$ und
$\lambda y_0=x+b-t$.
Die Determinante dieser drei Zeilen, multipliziert mit dem
bei der Elimination erhaltenen Faktor $\lambda^{H-1}$,
ergibt das monische Polynom

$$
p_H(\lambda)=
\lambda^{H+1}(\lambda+1)
-2\lambda(2\lambda+1)\sum_{j=0}^{H-1}w_j\lambda^{H-1-j}
+(\lambda+1)^2 .
$$

Insbesondere ist $p_H(0)=1$. Ein wachsender Ortsmodus ist
nicht nur formal: Wuerde sein Schreibfehler $e=b-t$
verschwinden, folgte aus der Traegerzeile
$2M'=(\lambda+1)t$. Die Kopfzeile ergaebe $x=t$ fuer
$\lambda\ne-1$. Die Schreibzeile wuerde dann $\lambda^H=1$
erzwingen (oder der Eigenvektor waere null). Jeder Ortsmodus
mit $|\lambda|>1$ wird also im realen Quer-Kopierfehler
sichtbar, gegebenenfalls als Oszillation eines komplexen Paars.

## 3. Zwei Ausschluesse und ein Grenzfall

- **Mittel der zwei juengsten Orte.** Fuer $w_0=w_1=1/2$ und
  alle anderen Gewichte null faktorisiert das Polynom zu
  $(\lambda+1)[\lambda^{H-1}(\lambda^2-2\lambda-1)+\lambda+1]$.
  Die eckige Klammer ist bei $2$ gleich $3-2^{H-1}<0$,
  bei $1+\sqrt{2}$ positiv. Die reelle Wurzel dazwischen
  laesst auch den Querort des Kopfs wachsen. Der Faktor
  der vollen Zwei-Write-Rueckkehr ist groesser als vier.
- **Beliebiges positives Gewicht am juengsten Ort.** Laegen
  alle Nullstellen auf dem Einheitskreis, waere das reelle,
  monische Polynom mit konstantem Term eins reziprok:
  Inversion bildet dann jede Wurzel auf ihre komplex
  Konjugierte ab. Der Vergleich der Koeffizienten an
  $\lambda^{H+1}$ und $\lambda$ verlangt
  $1-4w_0=2-2w_{H-1}$, also $w_{H-1}=1/2+2w_0$.
  Wegen der ausgeglichenen Paritaet und nichtnegativer
  Gewichte ist aber $w_{H-1}\le1/2$. Fuer $w_0>0$
  folgt also mindestens eine Nullstelle ausserhalb
  des Einheitskreises, da das Betragsprodukt eins ist.
- **Der verbleibende Dreiplatzfall.** Fuer $H=3$ bleibt nur
  $(w_0,w_1,w_2)=(0,1/2,1/2)$. Hier ist
  $p_3=(\lambda+1)^3(\lambda-1)^2$: Kein Multiplikator liegt
  ausserhalb des Einheitskreises. Dennoch waechst die
  lineare Querstoerung $v=(5,-3,1,0,1)^T$ in der Ortsordnung
  $(x,y_0,y_1,y_2,b)$. Fuer $N=B+I$ ist $N^3v=0$,
  und $e(v)=1$, $e(Nv)=-2$, $e(N^2v)=0$.
  Folglich ist $e(B^n v)=(-1)^n(1+2n)$. Dieser Fehler
  misst zwei verschiedene Positionen, die auf der gesamten
  ungestoerten Bahn am Schreibschnitt zusammenfallen.
  Er ist keine gemeinsame Translation oder Rotation.

## 4. Reichweite und Kontrollen

Die Instabilitaet sitzt jetzt in einem direkt beobachtbaren
Ort, nicht nur in einem Impuls der vorigen Referenz. Ein
konservatives Auslesen und ein zugehoeriger Gegenimpuls
reichen hier also nicht. Gewichte mit $w_0=0$ bei laengeren
FIFO-Fenstern sind nicht vollstaendig klassifiziert. Andere
Kraftformen und nichtkollineare Orbits werden ebenfalls nicht
ausgeschlossen. Ein naechster struktureller Vergleich waere
eine endliche Traegheit fuer Eintraege: Dann kann der beim
Auslesen uebertragene Impuls die Position vor dem naechsten
Write aendern. Die wiederkehrende Schreibgeometrie muesste
dabei neu hergeleitet werden.

[Referenzcode](../../experiments/current/reference/fifo_carrier_clock_cycle.py)
und [feste Kontrollen](../../tests/test_fifo_memory_center_cycle.py)
pruefen exakte Wiederkehr, Gegenimpuls, Energie und Drehimpuls,
den vollen Querblock, das charakteristische Polynom und den
linearen Kopierfehler. Die Ausschluesse folgen aus der Algebra,
nicht aus einem Gewichts- oder Laengenscan.
