# Ein linear stabiles, treues FIFO-Sechseck

Stand: 2026-11-24. Vergleich zur
[instabilen Zweiphasen-Kompensation](fifo_compensated_hexagon_2026-11-24.md).
Dieselbe kanonische Schreibkarte, derselbe autonome Rotor,
eine algebraisch andere konservative Kopplung. Keine native
Zieltrajektorie und kein Parameterscan.

**Ergebnis.** Die schwerpunktsfreie erhaltene Mode liefert
bei gleichen Massen und Radius $1/25$ ein treues, exakt
geschlossenes Sechseck. Auf der Flaeche fester Gesamtenergie
sind nach Entfernen gemeinsamer Translation samt Gesamtimpuls
und nach Reduktion der Drehung in der Ebene alle inneren
linearen Stoerungen beschraenkt. Das schliesst sowohl den
vollen Rotor-Rueckkopplungsterm in der Ebene als auch die
Stoerungen senkrecht zur Ebene ein. Es ist kein Nachweis
nichtlinearer Bindung oder spontaner Knotenbildung.

## 1. Die andere algebraische Kopplungsrichtung

Wir arbeiten in Einheiten $m=\mu=\omega=M_s=L=1$.
Die sechs Schnittorte bleiben $x_n=\lambda^n X$,
$\lambda=e^{i\pi/3}$, mit $b_n=-x_n$ und
$y_{j,n}=\lambda^{-j-1}x_n$. Der relative Flug
dauert $T=\pi/3$. Geaendert wird der erhaltene
Schwerpunkt-Speicher-Kovektor im Koordinatenblock
$(c,y_0,y_1,y_2)$:

$$
n=(0,a,1,d)^T,\qquad
a=-\frac{1+\sqrt5}{2},\qquad d=-1-a.
$$

Er hat keinen Schwerpunktanteil. Weil $a+d+1=0$
und $a^2+a-1=0$, erfuellt er beide algebraischen
Reflexionsbedingungen des vorigen Berichts.
Die andere Wurzel des quadratischen Polynoms
ist hier nicht der Stabilitaetsnachweis.

Die Impulse sind durch den Write bestimmt. Mit
$D=2iX$, $K=a-\lambda+\lambda^2d$,
$\sigma=-(1+\lambda)D/(\lambda K)$ gilt

$$
p=P_b=\sigma K/2,\quad
A=P_{y_0}=(-p+\sigma a)/\lambda,\quad
B=P_{y_1}=(-A+\sigma)/\lambda,\quad
P_{y_2}=-p,\quad P_x=D+p .
$$

Der Schwerpunkt-Speicher-Impuls nach dem Write
ist $\mathsf U=(D,p,A,B)^T$. Er wird im Flug zu
$\mathsf V=-\mathsf U+\sigma n$: Der Anteil
entlang $n$ bleibt, die zwei dazu senkrechten
internen Komponenten kehren ihr Vorzeichen um.
Die Richtung $n$ vollendet bei Frequenz sechs
eine ganze Periode; die Translation hat Impuls null.

Die komplementaeren Kovektoren sind
$(1,-1/3,-1/3,-1/3)$ und $(0,1-d,d-a,a-1)$,
normiert in der inversen Massenmetrik.
In dieser Basis liefern die komplexen Orts- und
Impulswerte die beiden reellen Spaltenpaare
$\mathcal Q=(\Re q,\Im q)$ und
$\mathcal P=(\Re p_{\rm mod},\Im p_{\rm mod})$.
$\mathcal Q$ ist invertierbar. Die reale
Matrix $\mathcal P\mathcal Q^{-1}$ ist symmetrisch:
Kanonischer Write und starre Rotation erhalten
den Drehimpuls. Da der relative Teil seinen
Drehimpuls ebenfalls erhaelt und der
Schwerpunkt-Speicher-Ort im Flug an beiden
Enden gleich ist, hat die Impulsumkehr in
diesem Zweierraum keinen Drehimpulsgewinn.
Das ist genau die Symmetriebedingung fuer
$\mathcal P\mathcal Q^{-1}$.

Die beiden Eigenwerte $\eta_-<0<\eta_+$ geben
wie im vorigen Vergleich die eindeutigen Wurzeln
von $\Omega\tan(\Omega T/2)=\eta$ auf $(3,6)$
bzw. $(0,3)$. Hier sind sie ungefaehr
$5.4399284$ und $1.9236229$.
Die so definierten harmonischen Kopplungen
schliessen den vollen Registerzustand bis auf
eine Drehung. Invarianz der inneren Energie
erlaubt dem Rotor genau die gepruefte Zeit,
ohne Reset. Der Radius aendert die exakte
Schreibgeometrie nicht. Fuer die lineare
Pruefung unten wird er auf $1/25$ fixiert.

## 2. Die Uhr gehoert zur Ableitung

Sei $D_{\rm w}$ der kanonische Write im
Phasenraum, $H_{\rm int}$ die innere Energie
und $E$ die festgehaltene Gesamtenergie.
Die Dauer des folgenden Flugs ist nicht
fest vorgegeben, sondern

$$
T(Z)=\frac{M_sL}{\sqrt{2M_s[E-H_{\rm int}(D_{\rm w}Z)]}} .
$$

Auf dem betrachteten Referenzzustand ist
die Wurzel strikt positiv. Ein zeitvariabler
Flug dieser speziellen Form bleibt symplektisch:
Er ist der Einheitszeitfluss des Hamiltonians
$f(H_{\rm int})$ mit $f'(h)=T(h)$, angewandt
nach $D_{\rm w}$. Auch der Wechsel in den um
$-\pi/3$ mitgedrehten Rahmen ist kanonisch.

Sei $J$ der feste Querblock aus nominalem
Flug und Write, $R_{-\theta}$ die Drehung in
der Ebene mit $\theta=\pi/3$. Die lineare
Rueckkehr in der Ebene ist

$$
J_{\parallel}=J\otimes R_{-\theta}
+\frac{T}{2E_{\rm Rotor}}\,
{\rm vec}(X_{H_{\rm int}}(Z_*))\,
\nabla[H_{\rm int}(D_{\rm w}Z_*)]^T .
$$

$Z_*$ ist der vorbereitete Zustand; bei unserer
Normierung ist $T/(2E_{\rm Rotor})=T^3$.
Der zweite Term ist die Rueckwirkung des Rotors
und wird mit Differenzen auf der echten
Energieflaeche gegengeprueft. Senkrecht zur
Ebene verschwindet der lineare Zeitterm, weil
die Energie quadratisch und isotrop ist.
Gemeinsamer Translationsdrift speist nur die
Translationsrichtung und aendert das reduzierte
Spektrum nicht.

## 3. Ein Intervallnachweis fuer beide Stoerungsrichtungen

Fuer einen symplektischen Block schreiben wir
das charakteristische Polynom mit
$u=\xi+\xi^{-1}$. Die Symmetriefaktoren sind
analytisch, nicht aus gerundeten Eigenwerten:

- Senkrecht zur Ebene liefert Translation samt
  Gesamtimpuls $u-2$. Die vorbereitete Rotation
  liefert $u-1$; dieses einfache Paar bleibt in
  der Querpruefung enthalten und ist beschraenkt.
- In der mitgedrehten Ebene gibt die gemeinsame
  Translation samt Gesamtimpuls $(u-1)^2$.
  Die planare Drehung bei festem Drehimpuls gibt
  $u-2$. Ihr Paar wird auf der Drehimpulsflaeche
  modulo Drehung entfernt.

Die [Intervallkontrolle](../../tests/test_fifo_center_free_hexagon.py)
verifiziert die Wurzelklammern der Frequenzen,
bildet massennormierte Spektralprojektoren und
berechnet reziproke Polynomkoeffizienten aus
Spuren. Sie prueft die Vorzeichen nach Abzug
der exakten Faktoren an den folgenden
disjunkten Intervallen:

| Block | Isolierte $u$-Wurzeln |
| --- | --- |
| Quer, ohne Translation und ohne das separat gepruefte Paar $u=1$ | $(-1.83,-1.80)$, $(0.41,0.43)$, $(1.02,1.05)$ |
| Ebene, mit voller Rotorableitung und ohne Symmetriefaktoren | $(-1.70,-1.66)$, $(-1.61,-1.57)$, $(-1.06,-1.02)$, $(-0.70,-0.66)$, $(0.39,0.43)$, $(1.005,1.017)$, $(1.98,1.995)$ |

Es gibt je einen strikten Vorzeichenwechsel
und genau so viele Intervalle wie der Restgrad.
Also sind alle diese Wurzeln einfach und in
$(-2,2)$. Die zugehoerigen Eigenwerte liegen
auf dem Einheitskreis. Im relevanten reduzierten
Raum sind die Bloecke diagonalisierbar; auch
Potenzen der Sechs-Schritt-Ableitung bleiben
beschraenkt. In drei Dimensionen decken die
beiden Bloecke alle linearen inneren Richtungen
ab. Weitere senkrechte Koordinaten liefern
identische, entkoppelte Bloecke. Die strikten
Vorzeichen bleiben auch fuer eine offene
Umgebung des Referenzradius erhalten, ohne
dass hier ihre Breite festgestellt wird.

## 4. Reichweite und naechster Pruefstein

[Code](../../experiments/current/reference/fifo_center_free_hexagon.py)
und [Kontrollen](../../tests/test_fifo_center_free_hexagon.py)
verifizieren einen ganzen Umlauf, die
energiegebundene Rotorableitung und die
beiden reduzierten Spektren ohne Rundungsannahme
an den Symmetrie-Eigenwerten.

Das ist ein linear stabiles Referenz-Sechseck,
kein bereits robust gebundener Knoten der
nativen Dynamik. Lineare Elliptizitaet allein
belegt keine nichtlineare Bindung; Untersuchungen
elliptischer Fixpunkte wie bei
[Eliasson, Fayad und Krikorian](https://arxiv.org/abs/1401.5748)
benoetigen dazu weitere Nichtresonanz- und
Normalformbedingungen. Der naechste
Diskriminator ist eine nichtlineare
Stoerungs- oder Normalformpruefung mit treuer
Historie und positiver Rotorreserve. Erst
danach waere die Kopplung zweier solcher
Referenzknoten als naechster physikalischer
Benchmark aussagekraeftig.
