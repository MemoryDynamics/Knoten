# Ein Vorzeichen aus vier FIFO-Plaetzen und seine Erhaltungsgrenze

Stand: 2026-11-23. Analytischer Anschluss an den
[Vorzeichentest zweier 4D-FIFOs](fifo_4d_relative_phase_2026-11-22.md).
Feste Algebra- und Ein-Schritt-Kontrollen, keine native Zielbahn.

**Ergebnis.** Der freie Vierplatz-FIFO besitzt ein exakt erhaltenes
orientiertes Volumen. Zwei vorbereitete nichtplanare Fenster koennen
entgegengesetzte Vorzeichen und dennoch dieselbe vollstaendige
ausgelesene 3D-Rahmenhistorie haben. Das relative Vorzeichen laesst
sich aus gemeinsamen radialen Slotvergleichen rekonstruieren. Aber
die bisherige Kreuzkopplung kann Volumen aus zwei Fenstern mit
Volumen null erzeugen, ohne Gegenbeitrag. Dieses Hindernis gilt
fuer jede auf dem betrachteten Abstandsintervall nichtkonstante
glatte radiale Kernelform mit demselben Schreibmechanismus.

## 1. Was der isolierte Speicher bewahrt

Schreibe das interne Fenster als Matrix mit vier Spalten,
$A=[a_0,a_1,a_2,a_3]$, die Koepfe und Eintraege sind reelle
normierte Vierervektoren ($a_0$ ist der Kopf). Setze

$$
Q(A)=\det A,\qquad F(A)=[-a_3,a_0,a_1,a_2].
$$

Der Viererzyklus der Spalten hat Vorzeichen $-1$ und die
Negation einer Spalte traegt ein zweites $-1$ bei.
Also gilt $Q(F(A))=Q(A)$ exakt. Unter einem gemeinsamen
orthogonalen Basiswechsel $U$ gilt dagegen
$Q(UA)=\det(U)Q(A)$. Das Einzelvorzeichen ist eine innere
Orientierungsgroesse, keine absolute Markierung im unorientierten
4D-Raum. Es ist auch nicht das 360-Grad-Minus:
$Q(-A)=Q(A)$. Der kohaerente 720-Grad-Kreis hat Rang zwei
und folglich $Q=0$. Vier Komponenten pro Kopf genuegen nicht;
vier unabhaengige gespeicherte Richtungen sind noetig.

Das einzelne Alter ist relevant: Negiert man nur einen Eintrag
eines vollrangigen Fensters, wechselt $Q$ sein Vorzeichen. Unter
$F$ werden diese relativen Eingabevorzeichen nur mitrotiert.
Weil das eingesetzte quadratische Readout $R(-u)=R(u)$ erfuellt,
sind alle 3D-Rahmen beider Fenster zu jeder freien Updatezeit
identisch. Der Nachweis trennt die Orientierung von der
ausgelesenen Spinrichtung; er liefert keine Teilchenzustaende.
Bei kontinuierlicher Deformation kann das Vorzeichen nur ueber
ein singulaeres Fenster wechseln. Nahe dem planaren Kreis gibt es
keinen positiven Mindestabstand zu solchen Fenstern. Das
Vorzeichen ist diskret, sein Betrag $|Q|$ ist es nicht.

## 2. Relatives Vorzeichen aus dem bestehenden Gauss-Vergleich

Die 16 einzelnen normierten Gausswerte bei bekannter Breite
$\sigma$ und gemeinsamen inneren Koordinaten genuegen:

$$
M_{ij}=a_i\cdot b_j=1+\sigma^2\log G_\sigma(a_i-b_j),
\qquad G_\sigma(v)=e^{-\|v\|^2/(2\sigma^2)},\qquad
\det M=Q(A)Q(B).
$$

Kein absolutes Orientierungszeichen oder Knotenlabel wird
eingesetzt. Bei gleichzeitiger Spiegelung bleibt das Produkt
gleich. Ein einziger negativer Spaltenlift an einer Seite
wechselt das Produkt, ohne die Rahmen zu aendern. Mit getrennt
waehlbaren lokalen Basen braucht der Kreuzvergleich weiterhin
eine gemeinsame Referenz oder einen Transport zwischen den
Basen. Aus der bereits aufsummierten Kopf-Abfrage wird die
16er-Matrix nicht automatisch gewonnen. Die Determinante ist
ein nichtlineares **Readout**, keine aus der Dynamik abgeleitete
Kraft oder Feldquelle.

## 3. Warum kein bloss anderer radialer Kernel die Erhaltung rettet

Pro Fenster wird nur der neue Kopf geschrieben. Sei
$N_A(v)=\det[v,a_0,a_1,a_2]$ die lineare Normalenform.
Fuer beliebige beschriebene Koepfe $h_A,h_B$ nach eventueller
Normierung ist

$$
Q(A')-Q(A)=N_A(h_A+a_3).
$$

Eine additive Erhaltung zwischen zwei Fenstern verlangt daher,
dass sich die beiden Normalenbeitraege exakt ausgleichen.
Gleiches Vorzeichen und gleiche Staerke der Kreuzkopplung
reichen dafuer nicht.

**Gegenbeispiel fuer die ganze radiale Klasse.** Waehle
$A=[e_1,e_2,e_3,e_1]$ und vier gleiche Spalten
$b=t e_1+\beta e_4$ in $B$, mit $-1<t<1$ und
$\beta=\sqrt{1-t^2}$. Beide Volumina sind null. Der freie
Kopfvorschlag von A ist $-e_1$. Der radiale Potentialkern
sei $\psi(\|x-y\|^2)$, die Summe der positiven Altersgewichte
sei $W$ und die symmetrische Kopplung $\lambda$. Der
unnormierte Kopf $y_A$ nach dem negativen Kreuzgradienten
hat die vierte Komponente
$2\lambda W\psi'(2+2t)\beta$. Also

$$
Q(A')=-\frac{2\lambda W\psi'(2+2t)\beta}{\|y_A\|},
\qquad Q(B')=0.
$$

Die zweite Aussage folgt, weil drei gleiche alte Spalten in
B verbleiben, unabhaengig von seinem neuen Kopf. Die
Normierungen sind fuer hinreichend kleine Kopplung definiert.
$2+2t$ laeuft durch das ganze offene Intervall $(0,4)$
der zugaenglichen quadrierten Abstaende. Ist $\psi$ dort
nicht konstant, gibt es ein $t$ mit $\psi'(2+2t)\ne0$.
Dann scheitert die Erhaltung fuer jedes hinreichend kleine
nichtverschwindende $\lambda$ beider Vorzeichen. Eine
kleine vollrangige Stoerung beider Fenster behaelt die
Verletzung wegen Stetigkeit bei. Man kann auch das
Anfangsvorzeichen von A entgegen dem des neuen Fensters
waehlen und so bei beliebig kleiner Kopplung in der Naehe
der singulaeren Fenster einen diskreten Vorzeichenwechsel
erzeugen. Ein Vorzeichenwechsel des Kernels kehrt hier die
Erzeugung um; er beseitigt sie nicht.

## 4. Konsequenz und Vergleich

Das ist eine positive Konstruktion eines relativen
Orientierungslabels und ein negativer Test seiner Eignung
als erhaltene Paarladung unter dem vorliegenden
Kopfschreiben. Es gibt weder eine Ableitung von U(1) noch
ein Gauss-Gesetz, einen Ortskraftkanal oder eine Aussage
ueber Bindung. Das Hindernis betrifft diese Klasse von
radialen Kopf-Updates, nicht beliebige Memory-Dynamik.
Wird ein kuenftiger Mechanismus als Quellendynamik
vorgeschlagen, muss er eine lokale Bilanz fuer die
Normalenbeitraege herleiten (gegebenenfalls einschliesslich
eines separaten Feldflusses), nicht bloss ein attraktives
Kernelvorzeichen einsetzen.

[Harris, Kamien und Lubensky, PRL 78, 1476 (1997)](https://arxiv.org/abs/cond-mat/9607084v3)
konstruieren in einem anderen Modell ein geometrisches
Chiralitaetsmass und leiten daraus zusammen mit mikroskopischen
Korrelationen einen Beitrag zum cholesterischen Pitch ab.
Der Vergleich ist methodisch: Ein vorzeichenbehaftetes
Geometriemass und sein dynamischer Kopplungskanal sind
getrennte Nachweise. Die Rechnung dort liefert weder die
hier verwendete FIFO-Bilanz noch einen Ladungsnachweis.

Die [festen Kontrollen](../../tests/test_fifo_4d_relative_phase.py)
pruefen Erhaltung und vollstaendige Rahmenblindheit, die
Kreuzrekonstruktion bei gemeinsamer Spiegelung und den
Gauss-Ein-Schritt-Gegenfall samt Vorzeichenwechsel. Die
Allgemeinheit in der radialen Klasse folgt aus der
Formel fuer $\psi'$, nicht aus Stichproben einer Kernelfamilie.
