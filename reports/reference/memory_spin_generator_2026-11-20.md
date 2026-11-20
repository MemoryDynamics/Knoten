# Vom Memory-Umlauf zum Spinorgenerator

Stand: 2026-11-20. Analytischer Anschluss an die
[reelle 4D-FIFO-Referenz](../../docs/reference/fifo_4d_spin_projection.md).
Keine neue Zielbahn, Parametersuche oder Stabilitaetsauswertung.

## Ergebnis

**Derselbe FIFO-Kreis passt zu verschiedenen 4D-Rotationsgesetzen.**
Sie stimmen auf der Umlaufebene exakt ueberein, unterscheiden sich
aber in der dazu senkrechten Ebene. Selbst eine beliebig genau
beobachtete Kreisgeschichte waehlt daher den Spinorgenerator nicht aus.
Auch das vorgegebene quadratische Readout unterscheidet sie auf diesem
Kreis nicht: Alle liefern dasselbe 720-Grad-Bild.

Der bereits implementierte antisymmetrische Memory-Stromtensor liefert
fuer diesen Kreis nur die Rotation einer Ebene. Eine quaternionische
Vervollstaendigung laesst sich daraus **algebraisch konstruieren**. Ob
die native Dynamik diese Vervollstaendigung realisiert, ist eine andere,
offene Frage. Es werden dafuer weder neue Freiheitsgrade in den Simulator
eingefuehrt noch nicht vorhandene Querantworten angenommen.

## 1. Ein Umlauf bestimmt nicht den ganzen Generator

In den Koordinaten der Referenz seien

$$
p=\frac12(1,1,1,1)^T,\qquad
v=J_zp=\frac12(1,-1,-1,1)^T,\qquad
u(\alpha)=p\cos\alpha+v\sin\alpha.
$$

p und v sind orthonormal. Mit

$$
P=pp^T+vv^T,\qquad S=vp^T-pv^T
$$

gilt Sp=v, Sv=-p und S^2=-P. S erzeugt den Kreis, wirkt aber auf
der senkrechten Ebene als null. Alle seine Historieneintraege bleiben
in span(p,v), auch wenn jede einzelne Koordinate ungleich null ist.

Wir verwenden den euklidischen Hodge-Dualoperator mit Orientierung
epsilon_1234=+1. Fuer eine antisymmetrische Matrix A ist

$$
(*A)_{12}=A_{34},\quad (*A)_{13}=-A_{24},\quad
(*A)_{14}=A_{23},\quad
(*A)_{23}=A_{14},\quad (*A)_{24}=-A_{13},\quad (*A)_{34}=A_{12}.
$$

Dies setzt eine orientierte euklidische innere 4D-Metrik voraus,
keine Lorentzmetrik und keine vierte physikalische Ortsdimension.
Es folgen *(*A)=A, S(*S)=(*S)S=0 und (*S)^2=-(I-P).
Deshalb erfuellt fuer **jedes reelle kappa**

$$
A_\kappa=S+\kappa *S,\qquad
e^{\alpha A_\kappa}p=u(\alpha),\qquad
A_\kappa^2=-P-\kappa^2(I-P).
$$

Die gesamte gezeigte FIFO-Historie, nicht nur ihr Kopf, ist also fuer
alle kappa identisch. Nur bei kappa=+1 oder -1 gilt A_kappa^2=-I:
Dann drehen beide orthogonalen Ebenen gleich schnell, mit gleichem
oder entgegengesetztem Drehsinn. In unserer Konvention ist

$$
J_z=S-*S.
$$

Alle drei Referenzgeneratoren J_i liegen im selben anti-selbstdualen
Sektor, *J_i=-J_i. Ihre Quaternionrelationen sind bereits separat
geprueft. Ein einzelnes A_kappa^2=-I ersetzt diese gemeinsame
Dreigeneratorstruktur und ihre physikalische Rotationswirkung nicht.

Die Unterscheidung ist direkt messbar, sobald eine Antwort ausserhalb
der Umlaufebene definiert ist. Fuer r=(1,1,-1,-1)^T/2 gilt

$$
Pr=0,\qquad Sr=0,\qquad A_\kappa r=\kappa *Sr,\qquad |*Sr|=1.
$$

Das ist eine feste algebraische Gegenprobe, keine gemessene native
Stoerantwort. Sie zeigt, welche Information der Kreis nicht liefert.

## 2. Was der vorhandene Memory-Strom liefert

Die bestehende Funktion
[`antisymmetric_current_tensor`](../../src/emergenz_knoten/vector_memory.py)
berechnet fuer Depositorte x_j, abgeleitete Richtungen d_j und Ursprung o

$$
C=\sum_j w_j\big[(x_j-o)d_j^T-d_j(x_j-o)^T\big].
$$

C ist derzeit ein Readout, **kein implementierter Kopfoperator**.
Eine Gleichsetzung mit einem dynamischen Generator braeuchte auch einen
abgeleiteten Zeit-/Kopplungsfaktor. Der folgende Test betrifft zunaechst
nur seine algebraische Form.

Setze x_j=u(alpha-j delta), delta=pi/4, o=0 und leite die Richtungen
aus genau dieser Historie ab:

$$
d_j=\frac{x_j-x_{j+1}}{|x_j-x_{j+1}|},\qquad
x_jd_j^T-d_jx_j^T=-\cos(\delta/2)S.
$$

Fuer jede feste positive Gewichtssumme W folgt damit exakt

$$
C=-W\cos(\delta/2)S,\qquad
\operatorname{rank}C=2.
$$

Kein nichtverschwindender skalarer Faktor macht daraus eine Matrix
mit Quadrat -I auf dem ganzen Vierkomponentenraum. Das liegt nicht
an einer unguenstigen Gewichts- oder Gainwahl. Auch bei Verschiebung
des Ursprungs innerhalb der Umlaufebene bleibt C dort unterstuetzt.

Positiv ist: Die bereits vorhandenen Daten erlauben bei gewaehlter
Orientierung die exakte algebraische Vervollstaendigung

$$
\frac{C-*C}{-W\cos(\delta/2)}=J_z.
$$

Diese Konstruktion fuegt die bisher unbeobachtete Rotation in der
komplementaeren Ebene hinzu. Die alternative Wahl C+*C liefert den
anderen Sektor; beide passen zum selben Kreis. Der Hodge-Operator
ist keine neue freie Komponente, aber seine Verwendung als
physikalischer Generator ist eine zusaetzliche, bisher nicht aus
dem Update hergeleitete Regel. Eine Definition als Diagnose ist
noch keine Memory-Emergenz und keine Auswahl von Teilchenchiralitaet.

Die Ranggrenze reicht etwas weiter: Bei einem exakten Vierzyklus in
R4 liegen seine vier Orte, alle Zyklusschritte und ein Ursprung in
ihrer affinen Huelle in hoechstens drei linearen Richtungen. C hat
dann eine Nullrichtung und als antisymmetrische 4-mal-4-Matrix Rang
hoechstens zwei. Das gilt nicht fuer beliebige vier Richtungsdeposits,
deren aelteste Richtung von einem fuenften unabhaengigen Ort stammt,
und nicht fuer beliebige laengere nichtplanare Historien.

### Welche Orientierung der Kreis nicht bereitstellt

Fuer die native radiale Skalar-/Alignment-Regel in vier **Ortsdimensionen**
gilt O(4)-Kovarianz: Normen, Skalarprodukte und Vektorsummen sind auch
mit Spiegelungen vertraeglich. Angenommen, ein allein aus der aktuellen
Historie gewonnenes antisymmetrisches 4-mal-4-Readout A soll dieselbe
Tensortransformation erfuellen,

$$
A(RY)=R A(Y)R^T,\qquad R\in O(4).
$$

Die Kreisgeschichte wird von allen orthogonalen Transformationen
festgehalten, die auf ihrer Ebene die Identitaet sind. Die Invarianz
unter dem Vorzeichenwechsel beider Normalrichtungen beseitigt alle
gemischten Matrixbloecke. Eine Spiegelung nur einer Normalrichtung
beseitigt den antisymmetrischen Normalblock. Daher ist zwingend
A(Y)=a(Y)S: Kein solches Readout waehlt die komplementaere Rotation aus.

Konkret fixiert R=I-2rr^T mit dem r aus Abschnitt 1 den gesamten Kreis,
aber R(*S)R^T=-*S. Es vertauscht S-*S und S+*S. Die Wahl einer
4D-Orientierung im Hodge-Operator reduziert hier die zugelassene
Kovarianz von O(4) auf SO(4); sie ist nicht durch den Kreis ausgezeichnet.
Das ist keine Behauptung ueber Raumparitaet realer Teilchen.

Die Aussage ist auf dieses Tensor-Readout und diese Transformation der
Komponenten beschraenkt. Zusaetzliche nichtplanare Memory-Struktur,
ein relativ orientierender Kontext oder eine anders hergeleitete interne
Darstellung sind nicht ausgeschlossen. Auch spontane Symmetriebrechung
wird nicht allgemein widerlegt; die exakt planare Historie allein
enthaelt das benoetigte unterscheidende Datum aber nicht.

## 3. Konsequenz fuer den Memory-Anschluss

Die Rechnung schliesst die Abkuerzung
"vier Koordinaten plus antisymmetrischer Umlauftensor ergeben Spin"
fuer diesen direkten Ansatz aus. Sie schliesst weder andere
Memory-Readouts noch eine kontrollierte effektive Vierkomponenten-
Dynamik oder emergenten Spin allgemein aus.

Ein kuenftiger Anschluss muss die vier internen Komponenten aus dem
vollstaendigen Zustand identifizieren und ihre Dynamik auch ausserhalb
eines einzigen Kreises herleiten. Erst dann ist entscheidbar, ob die
komplementaere Antwort den quaternionischen Generatoren entspricht,
ob die Reduktion geschlossen ist und ob das quadratische Readout eine
physikalische Beobachtung beschreibt. Ein Fit allein auf dem Kreis
kann diese Entscheidung prinzipiell nicht treffen.

Die [bestehende Arbeitsreihenfolge](../../docs/status/project_priorities.md)
bleibt unveraendert: zuerst die offene volle Formstabilitaet des
Memory-Ladungstraegers. Diese algebraische Gegenprobe ist kein Ersatz
dafuer und keine Freigabe eines neuen Zieltests. Paper I bleibt unberuehrt.

## 4. Literatur und Kontrolle

Gezielte Primaerquellenpruefung am 2026-11-20, kein systematischer Review.
Gesucht wurde nach quaternionischer 4D-Rotation und isoklinen Generatoren;
keine Neuheitsbehauptung fuer diese bekannte Algebra.

| Quelle und Umfang | Verwendeter Befund | Grenze fuer unser Modell |
| --- | --- | --- |
| [J. E. Mebius, arXiv:math/0501249v1 (2005)](https://arxiv.org/html/math/0501249v1), Abschnitte 2, 4.1-4.3 und 5; Preprint | Allgemeine 4D-Rotationen zerfallen in links-/rechts-isokline Quaternionrotationen; die beiden Arten sind geometrisch unterscheidbar. | Keine Memory-Dynamik, kein Teilchen- oder Quantisierungsnachweis. |
| [K. B. Wharton und D. Koch, J. Phys. A 48, 235302 (2015)](https://arxiv.org/html/1411.4999v2), Abschnitte 2.1-2.3 | Vier reelle Spinorkomponenten und die gewaehlte Hopf-Abbildung verbinden Quaternionwirkung und Bloch-Rotation. | Die Abbildung ist eine Darstellung vorhandener Quantenzustaende, keine Ableitung aus unserem FIFO. |

Die Hodge-Identitaeten, A_kappa-Familie und konkrete Memory-Stromformel
oben sind eigene direkte Rechnungen. Die beiden UPC-PDF-Treffer zur
Rotationsfaktorisierung waren beim Abruf nicht zugaenglich und werden
nicht als Beleg verwendet. Eine externe Begutachtung liegt nicht vor.

Die [festen Kontrollen](../../tests/test_memory_spin_generator.py)
pruefen exakte dyadische Matrixidentitaeten, vier verschiedene
Fortsetzungen derselben gesamten Historie, die Quer-/Spiegelprobe und den
vorhandenen Stromcode an drei festen Referenzphasen. Ein zusaetzliches
nichtplanares Vierpunktbeispiel kontrolliert die affine Ranggrenze.
Die allgemeinen Aussagen folgen aus den Formeln, nicht aus einer
Parametersuche oder gerundeten Rangentscheidung.

```bash
pytest -q tests/test_memory_spin_generator.py tests/test_fifo_4d_spin_projection.py
```

Verifikation: 77 Tests im betroffenen Panel bestanden in 2.94 s,
darunter 12 neue feste Kontrollen. Geprueft wurden ausserdem
`test_vector_memory.py`, `test_fifo_structure.py`,
`test_oriented_memory_contract.py` und `test_markdown_math.py`.
Die konfigurierte Ruff-Pruefung und der strikte MkDocs-Bau bestehen.
Keine vollstaendige Repository-Testsuite und keine neue native Simulation.
