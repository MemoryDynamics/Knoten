# FIFO-Regeneration: starre Rotation reicht fuer den 3D-Punktdefekt nicht

Stand: 2026-11-16. Analytische Fortsetzung des
[Defekt-/Kernvertrags](memory_defect_transport_2026-11-16.md).
Keine neue Zielbahn, Parametersuche, Simulationsregel oder Aenderung an Paper I.

## Ergebnis

**Ein gefuellter einzelner FIFO mit einer pro Schritt gemeinsam eigentlich
rotierenden Richtungshistorie kann in ungerader Dimension keinen regulaeren
Punktdefekt des nativen Vektorreadouts tragen.** Das gilt insbesondere in
3D, unabhaengig von Gains, positivem Vergessen und Kernelbreite. Es ist
eine Kompatibilitaetsbedingung des History-Shifts, kein neuer
Stabilitaetsbefund und kein Verbot aller gebundenen Memory-Strukturen.

Fuer den gegenwaertigen Punktdefekt-Kandidaten muessen wir deshalb
**innere Formdynamik oder mehrphasige Wiederkehr** zulassen, statt
Stabilitaet einer starr rotierenden Mehragentenstruktur direkt auf
eine einzelne Memory-Historie zu uebertragen. Wie viel Abweichung von
einer Ein-Schritt-Rotation mindestens erforderlich ist, laesst sich an
der absoluten Jacobian-Reserve des Defekts abschaetzen.

## 1. Der History-Shift ist eine zusaetzliche Gleichung

Der gefuellte Readout sei

$$
V(z)=\sum_{j=0}^{H-1}w_jp_jG_\ell(z-y_j),\quad
G_\ell(r)=e^{-|r|^2/(2\ell^2)},\quad
w_j>0,\quad W=\sum_jw_j>0.
$$

Die p_j sind die aus aufeinanderfolgenden Schritten gespeicherten
Einheitsrichtungen; bei einem Nullschritt gilt die native Nullkonvention.
Ein Schritt kopiert fuer j>=1 exakt p_j^+=p_{j-1}. Nehmen wir zugleich
eine starre gemeinsame Orientierungstransformation Q in O(d) an,
also p_j^+=Qp_j. Dann muss schon in der vorhandenen Historie gelten

$$
p_{j-1}=Qp_j,\qquad j=1,\ldots,H-1.
$$

Dies ist notwendig, auch wenn die neue Kopfdeposition und die native
Bewegungsgleichung noch gar nicht geprueft wurden. Ihre Erfuellung allein
beweist daher keinen Orbit. Eine gemeinsame Translation der Orte
aendert die Bedingung nicht. Eine Permutation der Alterslabels ist
nicht frei verfuegbar: Das Alter bestimmt den FIFO-Shift und das Gewicht.

Eine starre relative Gleichgewichtslage des **vollen** isotropen
rauschfreien Zustands wuerde diese Orientierungsbedingung erfuellen.
Die umgekehrte Richtung gilt nicht. Wir postulieren keine zwischen
den diskreten Updates fortgesetzte physikalische Rotation.

## 2. Fixraum-Hindernis fuer einen regulaeren Punktdefekt

Sei E=ker(I-Q), k=dim(E), und P_E die orthogonale Projektion auf E.
Fuer orthogonales Q gilt P_EQ=P_E. Somit ist

$$
P_Ep_j=a\quad\hbox{fuer alle }j,\qquad
P_EV(z)=a\sum_jw_jG_\ell(z-y_j).
$$

Die skalare Summe ist an jedem endlichen z strikt positiv.

1. Falls a ungleich null ist, kann V nirgends null werden. Die Richtung
   a ist ein gemeinsamer offener Halbraumzeuge.
2. Falls a=0 und k>0 ist, liegen alle Feldwerte und alle Spalten von DV
   in E-perp. Damit rank(DV)<=d-k<d: Kein regulaerer d-Punktdefekt.

Der Beweis benoetigt keine Annahme ueber die konkreten Speicherorte.
In ungerader Dimension besitzt jede eigentliche Rotation Q in SO(d)
einen nichttrivialen Fixraum: komplexe Eigenwerte kommen in Paaren,
und det(Q)=1 erzwingt mindestens einen reellen Eigenwert +1.
Damit folgt der angekuendigte Ausschluss.

In 3D hat eine nichttriviale eigentliche Rotation eine feste Achse.
Alle gespeicherten Richtungen muessen dieselbe Achsenprojektion haben.
Ist sie ungleich null, gibt es keinen Feldnullpunkt; ist sie null,
fehlt dem Readout die dritte Komponente. Auch ein translatorischer
Helix-Anteil umgeht diese Alternative nicht. Fuer Q=I ist E der ganze
Raum, also ist der Ausschluss noch staerker.

### Grenzen sind Teil des Resultats

- Gemeint ist der regulaere Punktdefekt dieses Vektorreadouts, nicht
  jede denkbare topologische Groesse, ein Linien-/Hopfdefekt oder
  elektrische Ladung im Allgemeinen.
- In gerader Dimension kann eine eigentliche Rotation ohne Fixvektor
  existieren. Der Satz liefert dort keinen Ausschluss; daraus folgt
  weder eine Dimensionsvorhersage noch native Stabilitaet.
- Eine uneigentliche Transformation mit det(Q)=-1 kann auch in 3D
  keinen Fixvektor haben. Sie ist keine eigentliche Raumrotation und
  keine Herleitung von Spin.
- Nichtstarre, mehrphasige, quasiperiodisch deformierende oder
  statistisch stationaere Historien werden nicht ausgeschlossen.
  Ein einzelnes Rauschfenster hat im Allgemeinen keine solche exakte
  Symmetrie; der Satz ist kein Rausch-Lebensdauertest.

## 3. Mehrphasige Wiederkehr braucht unterschiedliche zeitliche Klassen

Angenommen, nach m>=1 Schritten kehre die Richtungshistorie bis auf
dieselbe orthogonale Transformation Q wieder. Fuer j>=m bleiben alte
Eintraege im Speicher und erfuellen dann

$$
p_{j-m}=Qp_j.
$$

Die Projektionen a_j=P_Ep_j sind innerhalb jeder Altersrestklasse
j modulo m gleich. Es gibt hoechstens min(m,H) verschiedene a_j.
Eine regulaere Nullstelle von V verlangt, dass 0 im Inneren der
konvexen Huelle der Richtungen in R^d liegt. Denn ein Stuetzvektor
mit nichtnegativen Projektionen wuerde durch die strikt positive
Nullsumme alle Projektionen auf null zwingen und DV singulaer machen.

Die Projektion einer solchen inneren Umgebung auf E enthaelt eine
offene k-dimensionale Umgebung von 0. Eine konvexe Huelle von hoechstens
m Punkten hat Dimension hoechstens m-1. Notwendig ist folglich

$$
\min(m,H)\geq k+1,\qquad k=\dim\ker(I-Q).
$$

Dies sind **zeitliche Klassen vorhandener History-Eintraege**, keine
neuen unabhaengigen Felder, Teilchenarten oder Speicherkanaele.
In 3D gilt fuer eine nichttriviale eigentliche Rotation daher m>=2;
fuer echte Periodizitaet ohne Raumtransformation Q=I gilt m>=4.
Beides sind notwendige Bedingungen, keine ausreichenden Bauplaene.

Fuer m=2 und eine einzelne feste Achse muessen die beiden skalaren
Achsenprojektionen a_0,a_1 strikt entgegengesetzte Vorzeichen haben.
Am Defekt z_* muessen die **nativen** positiven Feldsummen

$$
C_r(z_*)=\sum_{j\equiv r\ ({\rm mod}\ 2)}w_jG_\ell(z_*-y_j)
$$

zudem a_0 C_0+a_1 C_1=0 erfuellen, also C_0/C_1=-a_1/a_0.
Ein bloss abwechselndes Vorzeichen reicht nicht: Die Feldbetraege,
Bewegungsbilanz, raeumliche Bindung und volle History-Stabilitaet
bleiben mitzubeweisen. Diese zwei zeitlichen Phasen sind insbesondere
kein Spin-1/2-Nachweis und kein Plus-/Minus-Ladungspaar.

### Bekannte native Gegenkontrolle statt eines neuen Kandidaten

Der [bereits zertifizierte negative-Gain-Vierzyklus](memory_defect_recurrence_2026-11-14.md)
besitzt die Transformation

$$
R=\begin{pmatrix}0&0&-1\\0&-1&0\\1&0&0\end{pmatrix},
\quad\det R=-1,\quad R^4=I.
$$

R hat keinen Fixvektor. Nach zwei Schritten ist Q=R^2 eine eigentliche
Halbdrehung mit einer festen Achse; die Richtungsprojektionen wechseln
zwischen den zwei Altersklassen ihr Vorzeichen. Der Vierzyklus ist
also mit dem neuen Satz vereinbar. Sein frueher bewiesener wachsender
Floquet-Multiplikator bleibt bestehen. Es wird weder ein neuer Lauf
gestartet noch dieser instabile Kontrollfall als Ladungstraeger reaktiviert.

### Minimaler offener Anschluss: zwei Phasen derselben Bahn

Die kleinste durch den Fixraumtest nicht ausgeschlossene Phasenzahl
bei einer nichttrivialen eigentlichen 3D-Rotation ist m=2. Das ist kein
Stabilitaetsresultat. Die Klasse laesst sich ohne zusaetzliche
Zustandsvariable formulieren. Sei
g(x)=Qx+t mit Q einer nichttrivialen eigentlichen 3D-Rotation. Fuer
zwei noch unbestimmte Orte a,b lautet die allgemeine zweiphasige
relative Wiederkehr

$$
x_{2k}=g^k(a),\qquad x_{2k+1}=g^k(b),\qquad k\in\mathbb Z.
$$

Alle Speicherorte und Richtungen stammen dann aus dieser **einen**
Bahn. Es werden weder zwei Teilchen noch zwei unabhaengige Agenten
eingefuehrt. Fuer die normierte feste Achse e sei h=e dot t und
Delta=e dot (b-a). Die beiden nichtverschwindenden Schrittlaengen sind
ell_a=|g(a)-b| und ell_b=|b-a|. Die beiden Achsenprojektionen der
Einheitsrichtungen lauten

$$
a_{\rm even}=\frac{h-\Delta}{\ell_a},\qquad
a_{\rm odd}=\frac{\Delta}{\ell_b}.
$$

Die notwendige Gegenzeichenbedingung wird Delta(h-Delta)<0.
Fuer raeumlich beschraenkte Wiederkehr ist h=0 erforderlich: Dann
liegen die beiden Teilfolgen auf zwei koaxialen Kreisen, eventuell
degenerierten, mit unterschiedlichen Achsenhoehen. Mit h ungleich
null entstehen Schraubbewegungen; auch dann gilt die Gegenzeichenhuerde.
Die Kreisform der Teilfolgen ist eine Konsequenz dieser Symmetrie,
keine neu gewaehlte Zielgeometrie oder Existenzbehauptung.

Seien Y_a und Y_b die daraus abgeleiteten vollen gefuellten Historien
an den Phasen a und b, einschliesslich aller Orientierungsvorgaenger.
Mit Psi als vorhandener rauschfreier nativer Kopfabbildung muessen
gleichzeitig die zwei Vektorgleichungen

$$
\Psi(Y_a)=b,\qquad \Psi(Y_b)=g(a)
$$

gelten. Erst dann liefert die Euklid-Aequivarianz die weiteren Phasen
ohne phasenweise umgeschaltete Kraefte. Eine freie Wahl der beiden
Kopfinkremente oder nur eine gemittelte Kreisbalance waere unzureichend.
Q,t,a,b und die Modellparameter sind hier **nicht** ausgewaehlt oder
geloest worden. m=2 ist in dieser Symmetrieklasse minimal zulaessig, kein
bewiesenes Minimum stabiler Traeger und keine Festlegung auf sie.

Bei erfuellter Existenz ist die korrekte lineare Formpruefung die
volle History-Ableitung von g^{-1}F^2, also
(I_history tensor Q^{-1}) DF(Y_b) DF(Y_a), nicht das Spektrum eines
eingefrorenen Feldes. Die Orientierungsableitungen gehoeren dazu;
starre Symmetriemoden sind von Formmoden zu trennen. Anschliessend
muss an beiden Phasen der lokale Defekt-/Kernvertrag erfuellt sein.
Diese Gleichungen sind ein diskriminierender Anschluss, kein neuer
Solverauftrag, Parametersuchraum oder bereits erteilter Stabilitaetspass.

## 4. Quantitative Huerde fuer beinahe starre Ein-Schritt-Rotation

Fixiere irgendein orthogonales Q mit k>0 und definiere die axialen
Shift-Residuen

$$
r_j=p_{j-1}-Qp_j,\qquad
\mathcal E_Q=\sum_{j=1}^{H-1}|P_Er_j|.
$$

Der Wert ist eine beobachtbare Kompatibilitaetsabweichung, keine nachfitte
Kopplung. Sei z_* eine regulaere Nullstelle, J=DV(z_*). Dann gilt

$$
\sigma_{\min}(J)\leq
\frac{W}{\ell\sqrt e}\mathcal E_Q.
$$

Beweis: Setze a_j=P_Ep_j und
beta_j=w_jG_ell(z_*-y_j)/sum_i w_iG_ell(z_*-y_i). Die beta_j sind
positiv, summieren sich zu eins und erfuellen sum_j beta_j a_j=0.
Teleskopieren liefert |a_j-a_i|<=E_Q, deshalb
|a_j|=|sum_i beta_i(a_j-a_i)|<=E_Q fuer jedes j. Somit

$$
\|P_EJ\|\leq\sum_j w_j|a_j|\,|\nabla G_\ell(z_*-y_j)|
\leq\frac{W}{\ell\sqrt e}\mathcal E_Q.
$$

Fuer einen beliebigen Einheitsvektor e_0 in E ist
sigma_min(J)=sigma_min(J^T)<=|J^T e_0|<=||P_EJ||. Das beweist die Grenze.
Bei einer gesicherten Reserve sigma_min(J)>=a>0 ist also notwendig

$$
\mathcal E_Q\geq\frac{a\ell\sqrt e}{W}.
$$

Fuer H>1 folgt ausserdem
max_j |r_j|>=a ell sqrt(e)/(W(H-1)). Der Satz gilt fuer **jedes**
solche Q; es wird kein Rotations-Fit ausgefuehrt. Eine gemeinsame
positive Amplitudenskalierung von V skaliert a und W gleich und
umgeht diese dimensionslose notwendige Huerde nicht.

Die Grenze misst erforderliche Abweichung von starrer Ein-Schritt-
Regeneration. Sie beweist weder eine genuegende Rueckstellkraft noch
eine pro Schritt erzeugte Instabilitaet. Bei kleinem a/W kann die
erforderliche Abweichung klein sein; ein bloss voller numerischer Rang
ohne kontrollierte Singulaerwertreserve reicht daher nicht.

## 5. Literatur: Stabilitaet ja, direkter FIFO-Transfer nein

Gezielter Abgleich, keine systematische Uebersicht. Geprueft am 16.11.2026.

| Primaerquelle und Stand | Tatsaechlich geprueft | Relevanz und Grenze |
|---|---|---|
| J. Thunberg, G. Sidorenko, *Projection-based discrete-time consensus on the unit sphere*, Automatica 188, 112927 (2026), [DOI](https://doi.org/10.1016/j.automatica.2026.112927) | Verlagsabstract und Publikationsmetadaten | Konvergenzaussagen mit Symmetrie-/Gewichtsbedingungen; kein allgemeiner FIFO-Satz. Kein Volltext- oder Beweisreview dieser Arbeit. |
| G. Sidorenko, J. Thunberg, *Attracting Rotations Obstruct Almost-Global Consensus on Spheres over Strongly Connected Graphs*, [arXiv:2610.28341v1](https://arxiv.org/html/2610.28341v1), 20.10.2026 | Abschnitte 1, 2.1-2.2, 4.1-4.2, Satz 3, Beispiele und Tabelle 1 | Gerichtete normierte Mehragentenkopplung erlaubt laut Satz 3 anziehende vollrangige Rotationen in d=2,3. Die sechs 3D-Agenten liegen auf zwei Breitenkreisen und den Polen. Stabilitaet gilt modulo gemeinsamer Rotation. |

Der zweite Text ist ein Preprint ohne Journalnachweis auf der gelesenen
arXiv-Seite. Anhaenge und Intervallzertifikat nicht unabhaengig reproduziert.
Enge Titel-/Identifier-Suchen nach Erratum/Korrektur ergaben keinen Treffer;
das ist keine umfassende Garantie. Aus dem Literaturbefund folgt gerade
**kein pauschales Zerfalls- oder Konsenstheorem fuer gerichtetes Alignment**.

Unser Transferhindernis folgt dagegen aus Abschnitt 1: Unabhaengige
Agenten duerfen verschiedene Projektionen auf die feste Rotationsachse
haben; ein einziger starr fortgeschobener FIFO darf das nicht. Die
Literaturgewichte sind keine hergeleiteten Alters-/Gaussgewichte.
Auch das Kopieren eines Literatur-Spektrums oder Aufteilen des Speichers
in unabhaengige Agenten waere kein nativer Emergenznachweis.

## 6. Verifikation und verbleibender Schritt

Die 27 festen Kontrollen in `tests/test_memory_rigid_regeneration.py`
pruefen History-Shift und Fixraumprojektion, die Nullstellen-/Rang-
Alternative, den vorhandenen uneigentlichen Vierzyklus und seine
Zweiklassenbilanz, die quantitative Reserve an bekannten Simplex-
Readouts, die zweiphasige Schraub-/Achsenbilanz sowie die Grenze in
gerader Dimension. Das sind geometrische
und algebraische Methodenkontrollen, keine neue stabile Zielstruktur.

27 neue Kontrollen und 277 Tests im betroffenen Panel bestanden, ebenso
Ruff im konfigurierten Code-/Testbereich und strikter MkDocs-Bau. Das
Panel umfasst die bisherigen Defekt-, Rekurrenz-, Vektormemory-,
Normalantwort-, Strom-/Phasen- und Zustandskontrollen sowie Markdown-
Mathematik. Keine vollstaendige Repository-Testsuite, kein unabhaengiger
mathematischer Review und kein neues numerisches Intervallzertifikat.

Der neue notwendige Filter kommt vor einer erneuten Orbitwahl: Eine
behauptete vollrangige Regeneration muss zur FIFO-Altersverschiebung
passen und eine positive Jacobian-Reserve mit echter innerer Form-
oder Phasendynamik vereinbaren. Danach bleiben der volle native
Existenz-/Stabilitaetsnachweis und die Kopplung an eine erhaltene
physikalische Quelle offen. Ein Literaturerfolg ersetzt keinen dieser
Schritte; ebenso rechtfertigt unser begrenzter Ausschluss kein neues Feld.
