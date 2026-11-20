# FIFO in 4D und die 720-Grad-Wiederkehr

Stand: 2026-11-20. Analytische Konstruktion und Gegenpruefung zur
Autorenidee, einen FIFO in vier reelle Dimensionen zu setzen.
Kein neuer nativer Ziellauf, keine Parametersuche und keine
Auswertung des ausstehenden Stabilitaetskandidaten.

## Ergebnis in einem Bild

**Das gewuenschte Wiederkehrverhalten ist konstruierbar:** Ein reeller
4D-Zustand durchlaeuft einen Kreis, waehrend ein geeignetes quadratisches
3D-Richtungsreadout zweimal rotiert. Nach 360 Grad Readout-Drehung ist
die innere FIFO-Historie negiert; nach 720 Grad ist sie wieder identisch.
Die sichtbare Richtung selbst wiederholt sich bereits nach 360 Grad.

![Reelle 4D-FIFO-Historien bei null, 360 und 720 Grad des quadratischen 3D-Readouts. Drei Koordinaten sind raeumlich dargestellt, die vierte farblich. Nach 360 Grad ist die Historie negiert; das untere Richtungsreadout ist bereits gleich.](https://raw.githubusercontent.com/MemoryDynamics/Knoten/codex/paper-i-finalization/figures/draft/fifo_4d_spin_2026-11-20/fifo_4d_projection.png)

Der Umlauf und das quadratische Readout sind hier **eingesetzte
Referenzregeln**, nicht aus dem skalaren/vektoriellen Memory-Feedback
gewonnen. Die vier alten Eintraege werden gespeichert, beeinflussen
aber den vorgegebenen neuen Kopf nicht. Insbesondere ist dies kein
Nachweis eines selbstgetragenen nativen FIFO-Umlaufs.

## 1. Eine explizite rein reelle Konstruktion

Sei alpha der innere Umlaufwinkel und phi=pi/4 eine feste Anfangsphase.
Setze

$$
u(\alpha)=\frac{1}{\sqrt2}
\begin{pmatrix}
\cos(\phi-\alpha)\\ \sin(\phi-\alpha)\\
\cos(\phi+\alpha)\\ \sin(\phi+\alpha)
\end{pmatrix},\qquad
J_z=\begin{pmatrix}
0&1&0&0\\-1&0&0&0\\0&0&0&-1\\0&0&1&0
\end{pmatrix}.
$$

Dann sind alle Eintraege reell, J_z ist antisymmetrisch, J_z^2=-I und
du/dalpha=J_z u. Es gilt u(alpha)=exp(alpha J_z)u(0).
Diese einzelne Bahn ist ein Kreis in einer zweidimensionalen Ebene
des reellen Vierkomponentenraums; vier Koordinaten bedeuten nicht,
dass eine einzelne Bahn einen vierdimensionalen Bereich ausfuellt.

Fuer einen beliebigen von null verschiedenen reellen Vektor u=(a,b,c,d)
waehle das Readout

$$
B(u)=\frac{1}{a^2+b^2+c^2+d^2}
\begin{pmatrix}2(ac+bd)\\2(ad-bc)\\a^2+b^2-c^2-d^2\end{pmatrix}.
$$

Direktes Einsetzen, ohne komplexe Arithmetik, ergibt

$$
B(u(\alpha))=(\cos 2\alpha,\sin 2\alpha,0).
$$

Der Readout-Winkel theta=2 alpha folgt also aus der **gewaehlten**
quadratischen Abbildung; er wird nicht durch eine Beschriftung des
inneren Winkels verdoppelt. Zugleich ist B(-u)=B(u).
Dies ist die reelle Form des bekannten Bloch-/Hopf-Readouts. Die
Spinor-Quaternion-Abbildung und die Rotation mit doppeltem Winkel
stehen bei [Wharton und Koch, J. Phys. A 48, 235302 (2015), Abschnitte 2.1-2.2](https://arxiv.org/html/1411.4999v2).

**Keine Verwechslung zweier Abbildungen:** Das gesamte B:S3 nach S2
hat Kreisfasern, nicht nur zwei Urbilder. Das Vorzeichenpaar allein
beschreibt nicht alle Zustandsvektoren mit gleicher Richtung. Die
zweifache Ueberlagerung SU(2) nach SO(3) betrifft dagegen die ganzen
Rotationsoperatoren. Im gezeigten eindimensionalen Umlauf erzeugt B
die beschriebene doppelte Winkelwiederkehr.

Die implementierten drei reellen 4-mal-4-Generatoren erfuellen exakt
J_i J_j=-delta_ij I+epsilon_ijk J_k. Damit wirkt
U(n,theta)=cos(theta/2)I+sin(theta/2)sum n_i J_i auf das Readout als
die gewoehnliche 3D-Rotation um die Einheitsachse n. Das ist eine
vorhandene Spinordarstellung, keine Auswahl dieser Algebra durch Memory.

### Der ganze FIFO, nicht nur sein Kopf

Mit alpha_n=n pi/4 und vier Speicherplaetzen sei

$$
Q_n=(u(\alpha_n),u(\alpha_{n-1}),u(\alpha_{n-2}),u(\alpha_{n-3})).
$$

Die Shiftregel ist exakt erfuellt. Der vorgeschriebene Kopfoperator ist
exp((pi/4)J_z). Fuer alle n gilt

$$
Q_{n+4}=-Q_n,\qquad Q_{n+8}=Q_n,\qquad
B(Q_{n+4})=B(Q_n),
$$

wobei B eintragsweise wirkt. Das sind **vier Speicherplaetze, acht
verschiedene Umlaufphasen und vier Readout-Phasen**. Dies ist nicht
derselbe Orbit wie unser nativer Vierzyklus.

Eine lineare Koordinatenprojektion P verhaelt sich anders:
P(-u)=-P(u), nicht P(u). Die obere Bildreihe zeigt P(u)=(a,b,c) und
codiert d als Farbe. Die untere zeigt B. Erst die zweite Abbildung
besitzt hier die halbe Wiederkehrzeit. Keine Interferenzwahrscheinlichkeit,
Born-Regel oder Fermionenstatistik wird durch diese Konstruktion hergeleitet.

## 2. Was die unveraenderte Memory-Regel in 4D tut

Sei E(x)=(x,0) die isometrische Einbettung von R3 in R4. Fuer epsilon=0,
Delta-Deposition, dieselben radialen Kernelparameter, Gains und
Altersgewichte gilt fuer die vorhandene skalare/Alignment-Regel exakt

$$
F_4(EY)=E F_3(Y).
$$

Beweis: Abstaende bleiben gleich, skalare Gradienten sind gewichtete
Differenzvektoren, und gespeicherte Einheitsrichtungen werden durch E
erhalten. Deshalb sind beide Kopfkraefte mit E vertraeglich. Dasselbe
gilt fuer die FIFO-Shiftzeilen. Dies schliesst auch gekippte isometrische
Einbettungen ein. Bei einer dimensionsabhaengigen geglaetteten
Deposition muessen zuerst deren effektive Parameter abgeglichen werden.

Da E injektiv ist, bleibt die minimale diskrete Periode unveraendert.
Unser [nativer Vierzyklus](https://github.com/MemoryDynamics/Knoten/blob/a228649/reports/reference/flat_memory_cycle_2026-11-16.md)
wird durch eine zusaetzliche Ortskoordinate also nicht zum Achtzyklus.
Auch jede feste zustandsabhaengige Projektion der unveraenderten
vierperiodischen Historie ist spaetestens nach vier Schritten wieder
gleich. Sie kann ohne zusaetzlichen Zustand keine doppelte Periode erzeugen.

Vier unterschiedliche Orte haben unabhaengig vom Umgebungsraum
hoechstens drei affine Richtungen. Fuer eine exakte Vierperiode sind
auch alle gespeicherten Schritte in dieser affinen Huelle. Ohne
Rauschen oder eine zusaetzliche Kraft bleibt die vorhandene radiale
Skalar-/Alignment-Dynamik darin. Das schliesst weder allgemeine
nichtperiodische 4D-Historien noch andere Umlaufperioden aus.

### Der eingebettete Felddefekt

Fuer den gemeinsamen Gauss-Vektorlesekernel gilt bei Abfrage (z,w)

$$
V_4(z,w)=e^{-w^2/(2\sigma^2)}\,(V_3(z),0).
$$

Ein Nullpunkt z_* des alten Readouts wird deshalb zur ganzen Linie
(z_*,w). Der volle 4D-Jacobian ist dort singulaer: Die eingebettete
3D-Nullstelle ist **kein isolierter regulaerer 4D-Punktdefekt**.
Ihr bisheriger +1-Index darf nicht als 4D-Punktindex uebernommen werden.
Dieser Befund betrifft eine vierte **Ortsdimension** der nativen Regel,
nicht vier innere Komponenten mit einem weiterhin dreidimensionalen
physikalischen Readout. Beides sind verschiedene Modellvertraege.

## 3. Bedeutung fuer das Forschungsziel

Die Autorenidee liefert ein konkretes kinematisches Zielbild. Der offene
Memory-Anschluss ist nun genauer: geeignete vier reelle interne
Komponenten samt Generatoren und physikalischem quadratischem Readout
herleiten, statt bloss die Dimension des bestehenden Ortsarrays zu erhoehen.
Die vorgegebene Referenzrotation wird nicht in die native Regel eingebaut.
Stabile Bildung, relative Phasenbeobachtung und elektrische Quellenwirkung
bleiben eigenstaendige Anforderungen. Der ausstehende begrenzte native
Stabilitaetstest wird durch diese Referenz weder ausgefuehrt noch ersetzt.

Der [Generatorabgleich](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/memory_spin_generator_2026-11-20.md)
zeigt zusaetzlich: Verschiedene 4D-Generatoren erzeugen exakt dieselbe
Kreisgeschichte. Der native Umlauftensor erfasst nur deren Ebene;
eine quaternionische Vervollstaendigung ist algebraisch moeglich, aber
ihre komplementaere Wirkung noch nicht aus Memory hergeleitet.

## Reproduktion und Kontrolle

- [Skript](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/experiments/current/reference/fifo_4d_spin_projection.py)
- [19 feste Kontrollen](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/tests/test_fifo_4d_spin_projection.py)
- [PNG](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/figures/draft/fifo_4d_spin_2026-11-20/fifo_4d_projection.png), [SVG](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/figures/draft/fifo_4d_spin_2026-11-20/fifo_4d_projection.svg), [Provenienz](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/figures/draft/fifo_4d_spin_2026-11-20/provenance.json)

```bash
python -m experiments.current.reference.fifo_4d_spin_projection
pytest -q tests/test_fifo_4d_spin_projection.py
```

Die Kontrollen pruefen exakte ganzzahlige Generatorrelationen, mehrere
Rotationsachsen, den gesamten FIFO-Shift, die getrennten Perioden,
die gemeinsame Phasenfaser sowie statische native Kernelidentitaeten
an fest vorgegebenen Nicht-Orbits. Gleitkomma-Tests kontrollieren die
Implementierung; die allgemeinen Aussagen folgen aus den Formeln oben.
