# Axiale Antwort des nativen FIFO-Vierzyklus

Stand: 2026-11-21. Analytische Fortsetzung des
[nativen Vierzyklus](flat_memory_cycle_2026-11-16.md) und seiner
[aktiven Form](four_cycle_active_form_2026-11-21.md).
Keine Auswertung eines nativen Kandidaten oder einer Zielbahn.

**Ergebnis.** Hat der mitgedrehte Einschritt-Formblock weder
+1 noch -1 als Multiplikator,
setzt ein kleiner konstanter axialer Kopfinput den ruhenden
Vierzyklus lokal als relativ zweiperiodische Bewegung fort:
Nach zwei Schritten reproduziert sich die deformierte Historie
bis auf eine Drehung um dieselbe Achse und eine axiale Verschiebung.
Die Verschiebung pro Schritt ist ungerade im Input, die Korrektur
der Halbdrehung gerade. Die lineare axiale Antwort ist aus einem
3-mal-3-System bestimmbar. Ihr Betrag und Vorzeichen sind fuer keinen
nativen Vertreter hier ausgewertet. Ein stabiler, wandernder Traeger
ist damit nicht belegt.

## 1. Ansatz und minimale spektrale Bedingung

Sei $Y_*=(a_0,a_{-1},\ldots,a_{-4})$ die konsistente volle
Positionshistorie mit $a_j=S^j(r,0,h)^T$ und $r,h>0$. S ist
die Vierteldrehung um z, gefolgt von der Spiegelung von z.
F bezeichnet den rauschfreien nativen Schritt mit festem Skalar- und
Alignment-Memory, $H_s=H_v=4$. Am exakten Orbit gilt $F(Y_*)=S Y_*$.
Alle Schrittlaengen sind dort positiv, also ist die lokale Karte glatt.
Raumtransformationen wirken auf alle Orte gleichzeitig. Sei
$e=e_z$, $E=(e,0,0,0,0)$ und $T=(e,e,e,e,e)$. Wir deklarieren
einen **additiven** Kopfinput $b e$:

$$
F_b(Y)=F(Y)+b E .
$$

Nur der Kopf wird direkt verschoben. Die veraenderte Richtung
wird wie im nativen Schritt aus der wirklichen neuen Differenz
bestimmt. Dies ist kein Feldmodell und kein physikalischer Kraftport.

Setze $L=S^{-1}DF(Y_*)$. Wegen O(3)-Aequivarianz hat die relativ
zur halben Drehung zurueckgefuehrte Zweischrittkarte die Ableitung
$S^{-2}D(F^2)(Y_*)=L^2$. Im Tangentialraum der sechs euklidischen
Symmetrierichtungen transformiert L Translationen durch $S^{-1}$
und Winkelvektoren durch $(\det S)S^{-1}$.
Also gilt $LT=-T$. Der Tangent der axialen Drehung,
$W=(e\times a_0,\ldots,e\times a_{-4})$, erfuellt $LW=W$.
Auf den vier uebrigen Symmetrierichtungen ist $L^2=-I$.

Vorausgesetzt wird: **Der Quotient von L modulo diesen sechs
Richtungen hat weder +1 noch -1 als Eigenwert.** Der vergessene
Laengenfaktor null im Positionslift verletzt das nicht.
Die Bedingung ist schwaecher als strikte Formstabilitaet:
Ein Schur-Nachweis fuer den vollen Vierphasen-Formblock waere hinreichend,
aber andere instabile Multiplikatoren sind hier nicht ausgeschlossen.
Folglich ist Eigenwert 1 von $L^2$ semisimpel, und sein Eigenraum
ist genau span(T,W). Dieser Raum und das Bild von $L^2-I$ sind komplementaer.

## 2. Nichtlineare Zweischrittfortsetzung

Schreibe $R_z(\theta)$ fuer eine eigentliche Drehung um die z-Achse.
Da $S^2=R_z(\pi)$, ist der neue relative Fixpunkt durch

$$
S^{-2}F_b^2(Y_b)-R_z(\theta(b))Y_b-2v(b)T=0
$$

definiert. Der Faktor 2 definiert v als mittlere axiale Verschiebung
pro Update. Man fixiert z-Translation und axiale Phase, etwa durch
eine lineare Schnittkarte senkrecht zu T und W durch $Y_*$.
In den 13 Schnittrichtungen und den zwei Unbekannten $\theta,v$
hat das Residuum bei $b=0$ die Ableitung

$$
(u,\vartheta,w)\longmapsto(L^2-I)u-\vartheta W-2wT .
$$

Sie ist invertierbar: Das Bild der 13 Schnittrichtungen hat Rang 13
und T,W ergaenzen es. Der implizite Funktionensatz liefert eine
lokal eindeutige glatte Fortsetzung im Schnitt. Er braucht keine
Invertierbarkeit von F. Axiale Translation und Drehung kommutieren
mit $F_b$, daher reihen sich die Schritte exakt:

$$
F_b^{2k}(Y_b)=R_z(k(\pi+\theta(b)))Y_b+2 k v(b)T .
$$

Auch die ungeraden Phasen wiederholen sich entsprechend relativ.
Das ist keine Sammlung starr bewegter Kopien des *ungestoerten*
Vierzyklus. Die zwei Historienschritte der fortgesetzten Form
stammen aus derselben Kopf-/Shiftregel. Wenn v nicht null ist,
erzwingt der [Ueberlappungssatz](four_cycle_active_form_2026-11-21.md)
eine Abweichung von der urspruenglichen aktiven Form.

Da $F_{-b}S^{-1}=S^{-1}F_b$, erfuellt $S^{-1}F_b(Y_b)$ bei -b
die gleiche Gleichung mit $\theta$ und $-v$. Dieser Vertreter
liegt bei kleinem b nahe $Y_*$ und kann durch axiale Drehung und
Translation in denselben Schnitt gebracht werden. Die lokale
Eindeutigkeit liefert $\theta(-b)=\theta(b)$ und $v(-b)=-v(b)$.
Insbesondere ist $\theta(b)=O(b^2)$ und $v(b)=\chi b+O(b^3)$.

## 3. Lineare Drift durch genau einen Projektor

Sei $\ell$ der linke Eigenkovektor mit $\ell L=-\ell$
und $\ell T=1$. Er ist eindeutig unter obiger Bedingung, da
der z-Translationsmodus bei -1 einfach ist. Zudem $\ell W=0$.
Die Eingangsableitung der relativ zurueckgefuehrten Zweischrittkarte
lautet $(I-L)E$: Der erste Kopfinput durchlaeuft $DF(SY_*)$,
der zweite wird erst danach addiert, und $S^{-1}E=-E$.
Anwendung von $\ell$ auf das differenzierte Residuum ergibt

$$
2v'(0)=\ell(I-L)E=2\ell E,\qquad \chi=\ell E .
$$

Die Messgroesse ist die mittlere axiale Verschiebung pro Update
und pro konstantem Kopfinput, keine beschleunigende Reaktion und
keine Masse. $\chi=0$ bedeutet kein lineares Wandern, schliesst
aber einen Beitrag hoeherer Ordnung nicht aus.

### Gleichwertiger Test aus den realen Kopfableitungen

Seien $A_j$ die 3-mal-3-Bloecke der vollstaendigen nativen
Kopfableitung nach $y_j$, wie in der
[Historienableitung](memory_history_response_2026-11-16.md).
Insbesondere bleiben die Einheitsrichtungen nicht eingefroren.
Definiere

$$
M=-S-\sum_{j=0}^{4}A_j(-S)^{-j},
\qquad V=e+\sum_{j=0}^{4}j A_j e .
$$

Translationskovarianz ergibt $\sum_j A_j=I$ und damit $M e=0$.
Sei $\mathcal E$ die Einbettung eines beliebigen Vektors in den Kopf.
Fuer die rotierte Altersgeschichte $U(u)_j=(-S)^{-j}u$ und
die lineare axiale Rampe $K_j=-j e$ liefern die Shiftzeilen exakt

$$
(L+I)U(u)=-\mathcal E S^{-1}M u,
\qquad
(L+I)K+T=-\mathcal E S^{-1} V .
$$

Der Kern von $L+I$ ist span(T), also ist der Kern von M span(e).
Der Kopfkovektor $-\ell\mathcal E S^{-1}$ annulliert M,
liefert auf V den Wert 1 und auf e den Wert $\chi$.
Damit ist das folgende System invertierbar:

$$
M e_x u_x + M e_y u_y + V\chi=e .
$$

Insbesondere

$$
\chi=\frac{\det[M e_x,M e_y,e]}{\det[M e_x,M e_y,V]} .
$$

Der Zaehler entscheidet, ob der deklarierte Input bereits linear
eine axiale Drift erzeugt; eine Nulldrift ist bei invertierbarem
Nenner aequivalent dazu, dass die beiden Formspalten den Input
aufnehmen koennen. Aus der Loesung $u=(u_x,u_y,0)$ ergibt sich
auch die Formantwort: $U(u)+\chi K$ ist, bis auf T und W,
die Ableitung $Y'_0$. Denn Anwendung von $L+I$ ergibt
$E-\chi T$, und anschliessend Anwendung von $L-I$ liefert
das differenzierte Zweischrittresiduum bei $\theta'(0)=0$.
Die beiden Formspalten enthalten die in der Ebene gegenlaeufige
erste Phasenstoerung und K die axiale Altersrampe. Nenner und
Zaehler werden hier nicht an einem nativen Orbit berechnet.
Ein spaeterer verifizierter Test muss auch die spektrale
Bedingung fuer die Fortsetzung separat kontrollieren.

## 4. Was der Befund fuer eine Wechselwirkung liefert

War der regulaere +1-Nullpunkt an beiden Ausgangsphasen strikt
innerhalb der aktiven tetraedrischen Huelle, bleibt er dort fuer
hinreichend kleine b auf der fortgesetzten Bahn: Der
implizite Feldnullpunkt ist glatt und die baryzentrischen
Reserven sind strikt. Feld und Huelle gehen nach zwei Schritten
in dieselbe gedrehte und verschobene Lage ueber; ihr mittlerer
axialer Versatz betraegt ebenfalls $2v$ pro Zweierphase.
Das beweist Erhaltung auf dieser bedingten Bahn, keine Anziehung
benachbarter Historien unter Antrieb.

Die Daten fuer einen spaeteren diskriminierenden Paarvergleich sind
damit benannt: Konfiguration bei festem nativen Parametersatz,
vorzeichenbehaftete axiale Antwort, Veraenderung der aktiven Form,
und Bindung des Nullpunkts. Keine transversale oder zeitabhaengige
Antwort, Reziprozitaet, eigenstaendige physikalische Kopplung oder
Gravitation folgt aus dem vorgegebenen konstanten Input.

## Literatur und Kontrolle

[Wulff, Documenta Math. 5 (2000), 227-274, Satz 2.3](https://ems.press/content/serial-article-files/25858)
behandelt verwandte relative Fortsetzung bei periodisch getriebenen
kontinuierlichen Systemen. [Wulff und Schebesch, SIADS 5 (2006), 435-475](https://doi.org/10.1137/050637170)
nutzen Symmetrie bei der numerischen Fortsetzung von ODE-Orbits.
Der implizite Schnitt ist daher keine neue allgemeine Methode.
Hier werden ein konstantes Eingangssignal, die konkrete singulaere
FIFO-Karte und ihre Gleichungen fuer die axiale Antwort behandelt.
Die allgemeinen kontinuierlichen Theoreme werden nicht auf den
Shift angewandt.

Die [drei festen Kontrollen](../../tests/test_four_cycle_axial_response.py)
verwenden kuenstliche lagekovariante Kopfableitungen, pruefen
Eingangsvorzeichen, die 3-mal-3-Reduktion und den axialen
Projektor gegen den vollen 15-Koordinaten-Schnitt.
Sie unterscheiden positive, negative und singulaere Antwort;
die Vorzeichenbeispiele gelten nicht fuer den nativen Kernel.
101 Tests im betroffenen Panel bestehen.
Keine native Zielhistorie, kein Stabilitaetslauf und keine
Parametersuche wurden gestartet.
