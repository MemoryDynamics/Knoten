# Bilanzierter Volumentransfer und die Grenze planarer FIFO-Saaten

Stand: 2026-11-23. Anschluss an die
[Verletzung der Volumenbilanz durch den radialen Kreuzdrift](fifo_oriented_volume_2026-11-23.md).
Eine Referenzschreibregel und feste Kontrollen, keine native
Zieltrajektorie oder Parametersuche.

**Ergebnis.** Ohne neue Zustandsvariablen laesst sich der vorhandene
Gauss-Schreibvorschlag so korrigieren, dass zwei FIFO-Fenster
orientiertes Volumen austauschen, aber seine Summe exakt bewahren.
Die Erhaltung ist dabei eine eingesetzte Bedingung. Eine
allgemeinere Grenze gilt unabhaengig von diesem Beispiel:
**Von rein planaren Fenstern aus kann ein stetiges Ein-Kopf-Update
mit exakter Volumenerhaltung keine nichtplanaren Fenster bilden.**

## 1. Ein endlicher bilanzierter Schreibschritt

Fuer ein Fenster $A=[a_0,a_1,a_2,a_3]$ ist der freie neue
Kopf $u_A=-a_3$. Seine drei juengeren Eintraege werden unveraendert
weitergeschoben. Der Normalenvektor $n_A$ ist durch
$n_A\cdot h=\det[h,a_0,a_1,a_2]$ definiert. Fuer den zweiten
FIFO gelten dieselben Definitionen. Aus den alten Fenstern
folgen die beiden rohen Gauss-Schreibvorschlaege, anschliessend
wie bisher einzeln auf Laenge eins normiert. Nenne sie $y_i$
fuer $i=A,B$. Geaendert werden nur die zu schreibenden Koepfe.

Gesucht ist das Paar $h_i$ mit minimaler Summe
$\sum_i\|h_i-y_i\|^2$, unter

$$
\|h_i\|=1,\qquad n_A\cdot h_A+n_B\cdot h_B
=S:=n_A\cdot u_A+n_B\cdot u_B.
$$

Das ist eine gewaehlte euklidische Metrik, keine aus Memory
hergeleitete Wirkungsfunktion. Im regulaeren Fall lautet die
Loesung mit einem gemeinsamen skalaren Multiplikator $\mu$

$$
h_i(\mu)=\frac{y_i-\mu n_i}{\|y_i-\mu n_i\|}.
$$

Existiert ein $\mu$, das die Bilanzgleichung erfuellt, ist dies
das globale Minimum: Bei festen Normen wird die zu maximierende
Summe $\sum_i y_i\cdot h_i$ durch Abzug von $\mu S$ nur um eine
Konstante verschoben. Termweise maximiert jeweils $h_i(\mu)$
das Skalarprodukt mit $y_i-\mu n_i$.
Setze $N_i=\|n_i\|$, und zerlege $y_i$ in axiale Komponente
$\alpha_i$ und senkrechten Anteil der Laenge $\beta_i$. Dann ist

$$
n_i\cdot h_i(\mu)
=N_i\frac{\alpha_i-\mu N_i}
 {\sqrt{(\alpha_i-\mu N_i)^2+\beta_i^2}}.
$$

Fuer jedes aktive $N_i>0$ mit $\beta_i>0$ faellt dieser
Ausdruck streng. Die Summe reicht von $+\sum_i N_i$ bis
$-\sum_i N_i$ und liefert fuer innere $S$ genau eine Loesung.
$N_i=0$ entfernt die Bedingung am betreffenden Kopf und schaltet
dort keinen Austausch frei. Bei gesaettigter Gesamtsumme muessen
alle aktiven Koepfe in Richtung ihrer Normalen oder in die
gemeinsame Gegenrichtung zeigen. Bei nichttrivialen rein
axialen Zielkoepfen kann die Naechstpunktwahl mehrdeutig sein;
die Referenzimplementierung bleibt dort bewusst undefiniert,
soweit kein bereits zulaessiger Vorschlag oder Saettigungsfall
vorliegt. In Gleitkommaarithmetik werden numerisch nicht
aufloesbare Normalen als null behandelt; exakte Bilanz ist
eine Aussage ueber die Formel, nicht ueber bitgenaue Rundung.

Die Bedingung ist mit einem gemeinsamen orthogonalen
Basiswechsel (auch Spiegelung) vertraeglich: Alle orientierten
Volumina wechseln gegebenenfalls gemeinsam das Vorzeichen, die
Metrik nicht. Das Ergebnis ist ebenso vertraeglich mit einem
Tausch der Knoten. Weder ein absolutes Vorzeichen noch ein
neues Feld oder Teilchenlabel wurde eingegeben.

### Tatsaechlicher Transfer, nicht bloss Abschalten des Drifts

In erster Ordnung der gemeinsamen Kopplung $\lambda$ sei
$r_i$ der tangentiale Rohdrift am freien Kopf und
$v_i=n_i-(n_i\cdot u_i)u_i$. Fuer
$L=\|v_A\|^2+\|v_B\|^2>0$ verschiebt der Multiplikator den
rohen, unbilanzierten A-Beitrag auf

$$
\Delta Q_A
=\lambda
\frac{\|v_B\|^2 n_A\cdot r_A-\|v_A\|^2 n_B\cdot r_B}{L}
+O(\lambda^2)
=-\Delta Q_B.
$$

Fuer $A=[e_1,e_2,e_3,e_1]$, $B=[e_1,e_4,e_2,e_1]$ sind
beide Anfangsvolumina null. Die Normale von A ist $-e_4$,
die von B $-e_3$. Bei Gauss-Breite eins und Gewichten
$(1,1/2,1/4,1/8)$ haben die rohen Volumenaenderungen die
Steigungen $w_1/e$ und $w_2/e$ mit **demselben** Vorzeichen.
Die korrigierten Steigungen sind
$+(w_1-w_2)/(2e)$ und $-(w_1-w_2)/(2e)$.
Der Austausch ist also nicht null. Dasselbe Anfangspaar
$(Q_A,Q_B)=(0,0)$ kann bei anderer Fenstergeometrie einen
anderen oder gar keinen Strom liefern, etwa bei zwei
identischen Fenstern. Die Volumina allein liefern keine
geschlossene Stromgleichung.

## 2. Reichweite: Stetigkeit sperrt die Entstehung aus planaren Fenstern

**Satz.** Betrachte beliebig viele Vierplatzfenster
mit Einheitskoepfen. Pro Fenster darf jeweils nur der neue
Kopf gesetzt werden; die drei juengeren Eintraege werden
unveraendert weitergeschoben. Sei das Update in den Fenstern
stetig und erhalte die Summe aller Determinanten fuer jede
Eingabe. Haben alle Ausgangsfenster Rang hoechstens zwei,
bleibt nach dem Update jedes Fenster in seiner eigenen alten
linearen Huelle und damit von Rang hoechstens zwei.

**Beweis.** Fixiere alle Fenster bis auf eines, $A$.
Die festgehaltenen Fenster haben je eine abhaengige
zurueckbleibende Dreiergruppe. Ihre Determinanten bleiben
bei beliebigem neuen Kopf null. Also muss schon die
Determinante von $A$ einzeln erhalten bleiben, auch wenn
nur $A$ ein wenig gestoert wird.
Sei $V$ die lineare Huelle seiner drei zurueckbleibenden
Vektoren. Bei Rang zwei kann man fuer jede Richtung
$n\perp V$ einen der drei abhaengigen Vektoren so kippen,
dass die aufgespannte Dreiebene in $n^\perp$ liegt und ihre
Normale in Richtung $n$ zeigt. Bei Rang eins kippt man
dazu zwei Vektoren in zwei unabhaengige Richtungen innerhalb
von $n^\perp$ und ausserhalb der alten Gerade. Die Vektoren
lassen sich dabei auf Laenge eins halten.
Fuer jede solche Stoerung erzwingt die einzelne Erhaltung
$n\cdot(h_A+a_3)=0$. Im stetigen Grenzuebergang gilt das
fuer jede Normale zu $V$. Also $h_A+a_3\in V$, insbesondere
liegt $h_A$ in der alten Fensterhuelle. Dasselbe gilt fuer
jedes der anderen Fenster.

Der Naechstpunkt-Referenzschritt kann diese Einschraenkung
nicht umgehen, ohne am Rangwechsel unstetig zu werden.
Ein fester Gegenfall ist $B=[e_4,e_4,e_4,e_4]$ und
$A=[e_1,e_2,\sqrt{1-\varepsilon^2}e_1+\varepsilon e_3,e_1]$.
Fuer jedes $\varepsilon>0$ muss A seine $e_4$-Komponente
beim Schreiben auf null halten: B kann kein Gegengewicht
tragen. Im exakten Fall $\varepsilon=0$ verschwinden beide
Normalen. Dann laesst die Referenz den rohen Gauss-Vorschlag
zu, der bei nichtverschwindender Kopplung eine $e_4$-Komponente
hat. Der Sprung ist somit kein reines Rundungsproblem.

## 3. Bedeutung fuer den Anschluss

Der bilanzierte Schritt ist ein positiver Referenztest fuer
Transfer zwischen geeigneten, vorbereiteten Historien,
**kein Bildungsmechanismus eines Ladungstraegers**.
Die planare Sperre ist allgemeiner als der Gauss-Kernel und
der euklidische Naechstpunkt. Wer auf diesem Weg eine stetige
Entstehung aus planaren Saaten beansprucht, muss mindestens
eine Voraussetzung konkret aendern: bereits nichtplanare
Memory bereitstellen, mehrere Eintraege pro Update schreiben
oder eine andere Gesamtbilanz mit dynamischem Feldbeitrag
herleiten. Keine davon wurde hier als Physik vorausgesetzt.
Es folgen insbesondere keine Bindung, Quantisierung oder
langreichweitige Ortskraft aus der Bilanz.

Die [native 4D-Gegenprobe](native_fifo_four_volume_rotation_2026-11-23.md)
liefert eine exakte vollrangige Fuenfperiode ohne eingesetzte
Bilanzbedingung. Sie ist analytisch instabil und kein
Bildungsnachweis aus planaren Saaten.

Die Verwendung eines Multiplikators zum exakten Erfuellen
einer Nebenbedingung ist aus der Molekulardynamik bekannt,
beispielsweise bei
[Andersen, RATTLE (1983)](https://doi.org/10.1016/0021-9991(83)90014-1).
Dort ist die Nebenbedingung ebenfalls ein Input; das
Verlet-Verfahren und seine mechanischen Eigenschaften werden
hier nicht uebernommen.

[Referenzcode](../../experiments/current/reference/fifo_balanced_volume.py)
und [feste Kontrollen](../../tests/test_fifo_balanced_volume.py)
pruefen die endliche Loesung gegen eine geschlossene
Paarformel, die lineare Steigung, nichtneutrale Anfangssummen,
Spiegelung, Knotentausch, Nullkopplung, fehlende Aufnahme,
Saettigung und den Grenzfall numerisch aufgeloester Rangwechsel.
Der allgemeine Stetigkeitssatz ist analytisch bewiesen.
