# Die zusaetzliche Formmode des Vierzyklus in 4D

Stand: 2026-11-21. Analytische Fortsetzung des
[3D-Formquotienten](memory_shape_quotient_2026-11-16.md).
Kein neuer Ziellauf und keine Auswertung des angefragten positiven
Stabilitaetskandidaten. Alle Modellparameter bleiben bei einer Stoerung fest.

## Ergebnis

Beim Einbetten des exakten raeumlichen Vierzyklus in eine weitere
**Ortsdimension** entsteht genau eine zusaetzliche lineare Formmode.
Vier andere neue Richtungen sind Translation und starre Kippungen,
keine neuen inneren Bewegungen. Die echte Formstoerung besitzt eine
geschlossene Rekursion:

$$
e_{n+1}=\mu_\perp e_n,\qquad
\mu_\perp=Bq^3g,\qquad e_n=z_n-z_{n-4}.
$$

z bezeichnet hier eine Auslenkung senkrecht zum bisherigen 3D-Raum,
nicht die Hoehe innerhalb dieses Raums. Nach vier Updates ist der
Formfaktor mu_perp^4. Eine zusaetzliche Raumdimension heilt also keine
3D-Instabilitaet, sondern bringt eine weitere Bedingung hinzu.
Ob diese Bedingung beim ausstehenden positiven Vertreter erfuellt ist,
wird hier nicht berechnet. Die Aussage betrifft nicht automatisch
vier innere Spinorkomponenten mit physikalischem 3D-Readout.

Auch abseits des Zyklus ist die Entwicklung des orientierten
Vierervolumens exakt bestimmbar. Ohne Rauschen multipliziert der
Koeffizient des aeltesten Vorgaengers dieses Volumen. Bei aktivem
Alignment und positiven Gaussgewichten bleibt der affine Rang vier
in jedem endlichen Schritt erhalten; eine moegliche Abflachung kann
dann nur asymptotisch sein.

## 1. Annahmen und vollstaendige Historie

Verwendet werden die rauschfreie native Skalar-/Alignment-Regel,
H_s=H_v=4, Delta-Deposition und ein nachgewiesener Vierzyklus

$$
y_0=(r,0,h),\ y_1=(0,-r,-h),\ y_2=(-r,0,h),\
y_3=(0,r,-h),\ y_4=y_0,\qquad r,h>0.
$$

Die vier Orte sind affin unabhaengig. Der fuenfte gespeicherte Ort
ist der Vorgaenger der aeltesten Einheitsrichtung. Im gestoerten
Zustand darf y_4 nicht mit y_0 identifiziert werden. Genau diese
faelschliche Identifikation wuerde die neue Formmode entfernen.

Bezeichnungen wie im [Existenzbericht](flat_memory_cycle_2026-11-16.md):
L^2=2r^2+4h^2, g=exp(-L^2/(2 sigma^2)), f=exp(-2r^2/sigma^2),
B=eta_v w0/L, Skalarretention s, Vektorretention q sowie die beiden
Skalarkoeffizienten C_1,C_2. Die native Kopfgleichung verlangt

$$
\Delta=s^2(1-gq)-q^2(f-gq),\quad
B\Delta=1,\quad C_1s=B(1-gq),\quad
C_2s^2=Bq(g-fq).
$$

Der folgende Normalfaktor benoetigt diese Kraftbilanzen, nicht eine
erneute Wahl der Gains bei jeder Stoerung. Eine Dimensionsaenderung
bei geglaetteter Deposition kann effektive Kernelparameter veraendern;
der hier verwendete unveraenderte Delta-Kernel vermeidet diese Vermischung.

## 2. Normalableitung und exakte Kuerzung

Die ungestoerten Abstands- und Schrittvektoren liegen in R3.
Ihre Laengen und Gaussfaktoren haben deshalb keine erste Variation
in einer neuen Normalrichtung. Die Einheitsrichtungen variieren aber
mit (z_j-z_{j+1})/L und duerfen nicht eingefroren werden. Fuer die
neue Kopfkoordinate folgt die Zeile (a_0,...,a_4):

$$
\begin{aligned}
a_0&=1-C_1(s+s^3)-C_2s^2+B,\\
a_1&=C_1s+B(gq-1),\\
a_2&=C_2s^2+B(fq^2-gq),\\
a_3&=C_1s^3+B(gq^3-fq^2),\\
a_4&=-Bgq^3.
\end{aligned}
$$

Die Formel gilt bereits fuer die vorgeschriebene Geometrie ohne
Orbitannahme; dort duerfen keine Symmetriemultiplikatoren abgezogen
werden. Erst mit den Kraftbilanzen oben ergibt sich

$$
a_1=a_2=0,\quad a_3=B\Delta=1,\quad
a_0=-a_4=Bgq^3=\mu_\perp.
$$

Damit lauten der lineare Normalblock und sein charakteristisches Polynom

$$
N=\begin{pmatrix}
\mu_\perp&0&0&1&-\mu_\perp\\
1&0&0&0&0\\0&1&0&0&0\\0&0&1&0&0\\0&0&0&1&0
\end{pmatrix},\qquad
\det(\lambda I-N)=(\lambda^4-1)(\lambda-\mu_\perp).
$$

Insbesondere bleibt die FIFO-Randwirkung erhalten. Fuer das
Zeilenfunktional ell=(1,0,0,0,-1) gilt exakt ell N=mu_perp ell.
Die Rekursion im Ergebnis ist daher ein wirklicher linearer Quotient,
keine Projektion, die spaeter in andere Formrichtungen zurueckkoppelt.

## 3. Warum vier Faktoren Symmetrien sind

Jede infinitesimale Translation/Kippung in die neue Richtung hat
die Form z_j=t+c dot y_j. Wegen y_4=y_0 gilt e=0. Die affine
Unabhaengigkeit der vier Orte liefert vier unabhaengige solcher
Historien; sie fuellen genau den vierdimensionalen Kern von ell.
Umgekehrt ist jede Normalhistorie mit z_4=z_0 eine solche affine
Variation. Der ganze Kern ist somit Symmetrietangentialraum.

Auf diesem Raum verschiebt N die vier Phasen zyklisch. Seine
Multiplikatoren sind 1,-1,+i,-i, nach vier Schritten alle 1.
Die verbleibende skalare Richtung hat Faktor mu_perp. Bei
mu_perp=+1 oder -1 kann sie spektral mit einer Symmetrie kollidieren;
sie darf deshalb nicht ebenfalls als Symmetrie entfernt werden.

Fuer d>3 tritt derselbe Normalblock d-3-mal auf. Gemischte lineare
Bloecke zwischen den alten drei Koordinaten und den Normalrichtungen
verschwinden. Mit der Fortsetzung S_d=diag(S,I_(d-3)) des bisherigen
Rueckkehrrahmens gilt daher fuer die charakteristischen Polynome

$$
\chi_d(\lambda)=\chi_3(\lambda)
\big[(\lambda^4-1)(\lambda-\mu_\perp)\big]^{d-3}.
$$

Die acht bereits bekannten nichttrivialen 3D-Formmultiplikatoren
bleiben erhalten. Hinzu kommen d-3 Kopien von mu_perp; die alte
redundante Nullrichtung bleibt separat. Eine Vorzeichenumkehr des
gewaehlten Normalrahmens aendert gegebenenfalls das Vorzeichen des
Ein-Schritt-Faktors, nicht seinen Betrag oder den Vier-Schritt-Faktor.

## 4. Was dies fuer Stabilitaet und Dimension bedeutet

Fuer den neuen Normalquotienten gilt genau:

- |mu_perp|<1: lineare Kontraktion dieser zusaetzlichen Formmode.
- |mu_perp|>1: eine wachsende Formmode, auch wenn alle 3D-Moden stabil waeren.
- |mu_perp|=1: keine strikte Kontraktion; kein hinreichendes Stabilitaetsurteil.

Fuer die positive Existenzfamilie ist B=1/Delta>0. Die zusaetzliche
strikte Bedingung laesst sich ohne Eigenwertrechnung schreiben als

$$
Bq^3g<1
\quad\Longleftrightarrow\quad
s^2(1-gq)>fq^2.
$$

Im gleichbreiten rein attraktiven Teilfall mit
s=qg(g-fq)/(f(1-gq)) ist dies aequivalent zu

$$
g^2(g-fq)^2>f^3(1-gq).
$$

Es wird hier kein positiver Parametersatz eingesetzt oder nach
Bestehen dieser Ungleichung gesucht. Sie ist **zusaetzlich** zum
vollen 3D-Formtest erforderlich. Der bekannte negative Kontrollorbit
mit B=-24 und g=q=1/2 besitzt mu_perp=-3/2; dies kontrolliert die
Formel an einem bereits als instabil bekannten Fall.

Ein kuenftiger gemeinsamer strikter Pass wuerde zunaechst volle
lineare Formstabilitaet modulo euklidische Symmetrien belegen. Ein
nichtlinearer Attraktionssatz samt endlicher Toleranz benoetigt seinen
eigenen Anschluss. Weder spontane Formation noch globale Auswahl
dreier Raumdimensionen folgen aus diesem lokalen Test. Die Neigung
des lokalen 3D-Unterraums bleibt eine Symmetrie, keine Rueckstellung
zu drei vorgegebenen Koordinatenachsen. Rauschen, endliche Lebensdauer,
Interaktion und eine physikalische Dimensionsinterpretation bleiben
gesonderte Fragen. Der eingebettete Felddefekt bleibt zudem eine
Nullstellenlinie in 4D, wie der
[Einbettungsaudit](../../docs/reference/fifo_4d_spin_projection.md) zeigt.

## 5. Exakte Volumenbilanz jenseits der Linearisierung

Fuer jede gefuellte konsistente Geschichte $Y=(y_0,\ldots,y_4)$ mit
nichtverschwindenden Schrittlaengen gilt in der gleichen Modellklasse
ohne Rauschen: Der neue Kopf $x^+$ ist eine affine Kombination der
fuenf Orte. Alle skalaren Kraefte sind Vielfache von $y_j-y_0$, alle
Alignment-Kraefte Vielfache von $y_j-y_{j+1}$. Sie addieren daher
zusammen mit dem alten Kopf Koeffizienten mit Summe eins. Ausschliesslich
die aelteste Einheitsrichtung enthaelt $y_4$; sein Koeffizient ist

$$
a_4(Y)=-\frac{\eta_v w_3}{|y_3-y_4|}
\exp\left(-\frac{|y_0-y_3|^2}{2\sigma^2}\right).
$$

Definiere das orientierte Vierervolumenelement, ohne den Faktor 1/4!,
durch

$$
W(Y)=(y_1-y_0)\wedge(y_2-y_0)\wedge(y_3-y_0)\wedge(y_4-y_0).
$$

In d=4 ist es eine vorzeichenbehaftete Determinante; fuer d>4
bestehen seine Komponenten aus allen Vier-mal-vier-Minoren. Fuer
$Y^+=(x^+,y_0,y_1,y_2,y_3)$ ist

$$
W(Y^+)=(y_1-y_0)\wedge(y_2-y_0)\wedge(y_3-y_0)\wedge(x^+-y_0)
      =a_4(Y) W(Y).
$$

Im ersten Schritt wurde die Orientierung durch eine gerade zyklische
Permutation der fuenf Ecken gesetzt. Im zweiten verschwinden alle
Terme mit bereits vorhandenem Basisvektor. Das ist eine exakte
Identitaet fuer beliebig grosse Stoerungen, solange die angegebenen
Updateannahmen gelten. Die elementare Volumengeometrie ist bekannt:
[Romanowska, Smith und Zamojska-Dzienio, arXiv:2312.00828v2, Abschnitt 6.1](https://arxiv.org/html/2312.00828v2)
geben die affinen Koordinaten als Verhaeltnisse orientierter
Simplexvolumina an. Der FIFO-spezifische Koeffizient folgt hier
aus der nativen Kopfregel, nicht aus der Literatur.

Am exakten Zyklus gilt $a_4=-\mu_\perp$. Das Minuszeichen im
Volumenelement widerspricht dem linearen Faktor aus Abschnitt 2 nicht:
Die orientierte alte 3D-Basis wechselt mit det S=-1 ihr Vorzeichen.
Nach vier Updates liefern beide Beschreibungen denselben Faktor.
Eine alternierende Volumenorientierung ist kein Spinorzeichen.

**Bedingte Abflachung.** Gilt entlang einer Geschichte dauerhaft
$|a_4(Y_n)|\leq\rho<1$, dann
$\|W(Y_n)\|\leq\rho^n\|W(Y_0)\|$. Wenn zusaetzlich das
Dreivolumen der vier juengsten Orte einheitlich nach unten beschraenkt
ist, sinkt auch der Abstand des aeltesten Vorgaengers zu ihrer affinen
Huelle mit dieser Schranke bis auf einen konstanten Faktor.
Weder diese Dreivolumenreserve noch das Verbleiben in einem
kontrahierenden Bereich folgt allein aus der Vierervolumenformel.
Bei $a_4\ne0$ bleibt der gesamte affine Span jedes einzelnen
deterministischen Updates unveraendert: $y_4$ kann aus der neuen
affinen Kombination zurueckgeloest werden. Das behauptet keine
Invertierbarkeit der vollen nichtlinearen Zustandsabbildung.

**Mit additivem Rauschen.** Ersetze den neuen Kopf durch
$x^++\varepsilon\xi_n$ und nenne das Dreivolumenelement der vier
juengsten Orte $T(Y)$. Die exakte Bilanz erhaelt den additiven Term
$\varepsilon T(Y_n)\wedge\xi_n$. In d=4 hat dieser Term bei
unabhaengigem standardnormalem $\xi_n$ bedingt auf $Y_n$ Mittelwert
null und Varianz $\varepsilon^2\|T(Y_n)\|^2$. Insbesondere wird
ein nichtdegenerierter 3D-Span bei nichtentartetem Rauschen sofort
fast sicher verlassen. In d=4 liefern zwei gegebene 3D-Historien
$Y$ und $2Y$ dasselbe $W=0$. Ihre Rauschvarianzen im naechsten
Schritt unterscheiden sich aber um den Faktor $2^6$, da T vom Grad
drei ist. Es gibt also keinen gemeinsamen Markov-Uebergangskern allein
fuer W, der fuer **alle** deterministischen Anfangshistorien gilt.
Das gesamte endliche FIFO bleibt dagegen der augmentierte Zustand.
Der Befund schliesst keinen speziellen effektiven Abschluss unter
weiteren Annahmen aus und liefert keine stationaere Lebensdauer.

## 6. Kontrolle und Literaturabgleich

Die [festen Tests](../../tests/test_four_cycle_extra_dimensions.py)
vergleichen die volle native Kopfableitung in 4D/5D mit der allgemeinen
Normalzeile und zentralen Differenzen. Die eingesetzten Gains liefern
ausdruecklich **keine** selbstreproduzierende Bahn. Eine schraege
Einbettung kontrolliert, dass der Befund nicht an der vierten
Koordinatenachse haengt. Rationale formale Begleitmatrizen pruefen
den Quotienten, die Polynomidentitaet und alle vier Symmetrierichtungen,
einschliesslich der Kollisionen mu_perp=+1,-1. Diese formalen Werte
sind keine Stabilitaetsauswertungen positiver Memory-Kandidaten.
Sieben zusaetzliche feste Kontrollen vergleichen alle Vierervolumen-
Minoren eines nativen Updates in 4D und 5D fuer beide Kopplungsvorzeichen
und ausgeschaltetes Alignment. Eine vorgegebene Kopfauslenkung prueft
den additiven Volumenterm ohne Zufallslauf.

Die universelle Faktorisierung folgt aus der Kuerzung in Abschnitt 2
und der Symmetrieidentifikation, nicht aus einer numerischen Rang-
oder Eigenwertentscheidung. Keine neue Produktionsfunktion oder
Modellregel wird eingefuehrt.

Der gezielte Primaerquellenabgleich umfasst ausserdem:
[Sidorenko/Thunberg, arXiv:2610.28341v1](https://arxiv.org/html/2610.28341v1),
Abschnitt 4.2.3 unmittelbar vor Beispiel 4, grenzt die nachgewiesene
3D-Attraktion ausdruecklich von den ungeprueften Zusatzrichtungen bei
d>3 ab. Anhang B.1 trennt gemeinsame Rotation von Formmoden. Das
bestaetigt die methodische Notwendigkeit eines separaten Tests,
liefert aber weder unseren Faktor noch eine FIFO-Stabilitaet.
Die Arbeit ist ein Preprint ueber normierte Agenten; keine Kopplung,
Quantisierung oder Dimensionsauswahl wird daraus importiert.

```bash
pytest -q tests/test_four_cycle_extra_dimensions.py
```

Verifikation: 92 betroffene Tests bestanden in 24.11 s, darunter
19 neue feste Kontrollen. Das Panel umfasst ausserdem die volle
History-Kopfableitung, den 3D-Formquotienten, die 4D-Spinreferenz,
deren Generatorabgleich und die Markdown-Formelkontrollen.
Die konfigurierte Ruff-Pruefung und der strikte MkDocs-Bau bestanden.
Keine vollstaendige Repository-Testsuite und keine neue Zielsimulation.

Die aktive [Arbeitsreihenfolge](../../docs/status/project_priorities.md)
bleibt beim vollen 3D-Formtest. Die hier abgeleitete zusaetzliche
Raumbedingung ersetzt ihn nicht und erweitert keine offene Freigabe.
