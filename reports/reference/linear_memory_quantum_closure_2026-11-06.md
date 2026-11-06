# Mitlaufende lineare Memory und der Quantenabschluss

Stand: 2026-11-06. Fortsetzung des
[stochastischen Quantenabgleichs](stochastic_quantum_bridge_2026-11-06.md)
gegen Repository-Stand `69b5a92`. Analytischer Vergleich mit 18 kleinen
Softwarekontrollen; keine Zielsimulation, Parametersuche oder neue
Modellregel. Arbeitsfolge nur in den
[Projektprioritaeten](../../docs/status/project_priorities.md).

## Ergebnis

Das Mitfuehren des vorhandenen linearen Memory-Zentrums beseitigt die
Quantenluecke nicht automatisch. Zwei positive Gauss-Anfangsensembles
koennen dieselbe Ortsdichte und denselben Strom besitzen, aber sofort
verschiedene weitere Breitenentwicklung. Eine Zuordnung dieser beiden
Groessen zu **derselben reinen skalaren Wellenfunktion** schliesst daher
nicht auf der ganzen untersuchten Praeparationsklasse.

Zudem ist die Langzeitvarianz jeder festen translationskovarianten
linearen Ortsauslese in diesem stabilen Vergleich diffusiv, nicht die
quadratische freie Ausbreitung eines lokalisierten Quantenpakets mit
endlichen zweiten Momenten. Das betrifft auch das Memory-Zentrum.
Eine konstante Zeit-/Laengen-/Massenkalibrierung aendert diesen Unterschied
nicht. Keine allgemeine Aussage gegen nichtlineare, kollektive,
offen-quantendynamische oder andere Zustandsbeschreibungen.

## 1. Genau welches bestehende Modell geprueft wird

Der [lokale kontinuierliche Vergleich](../../docs/reference/memory_pair_reduction.md)
enthaelt fuer ein einzelnes ungekoppeltes System, jetzt mit Rauschen,

$$
dX_t=-a(X_t-C_t)\,dt+\sqrt{2D}\,dW_t,\qquad
dC_t=b(X_t-C_t)\,dt.
$$

$C$ ist das normierte exponentielle Memory-Zentrum, keine physikalische
Masse. Es gelten $b,D>0$, $a\in\mathbb R$ und $\lambda=a+b>0$.
Dies schliesst den attraktiven Fall $a\geq0$ ein; der relative Modus ist
stabil. Anfangszustaende sind unabhaengig von kuenftigen Wiener-Inkrementen.
Die praezisen Gausskontrollen unten verwenden zentrierte gemeinsame
Verteilungen von $(X_0,C_0)$ mit positiver Kovarianzmatrix.

Der Anschluss an die diskrete Referenz mit Schreibort $X_{n+1}$ lautet
$g=a h$, $\alpha=b h$, $\varepsilon=\sqrt{2Dh}$ und

$$
T_h=\begin{pmatrix}
1-a h&a h\\
b h(1-a h)&1-b h+a b h^2
\end{pmatrix}=I+hA+O(h^2),\qquad
A=\begin{pmatrix}-a&a\\b&-b\end{pmatrix}.
$$

Die diskrete Rauschrichtung ist $(1,\alpha)^T$, nicht $(1,0)^T$;
die gemeinsame Innovation des Write-Schritts verschwindet in der zweiten
Komponente erst im angegebenen kleinen-Schritt-Limit. Dies stimmt mit
dem bestehenden Zweizustands-Multiplikator $(1-\alpha)(1-g)$ ueberein.

**Grenzen:** Die Rechnung ist exakt fuer diesen linearen Vergleich.
Sie ist kein neuer Konvergenzsatz aus dem nichtlinearen Gauss-FIFO, kein
uniformer Langzeitfehlernachweis und keine Rechtfertigung, einen endlichen
physischen FIFO-Horizont wegzulassen. Die vorbereiteten Gauss-Ensembles
sind keine nachgewiesenen nativen Bildungsprodukte. Ihre Zulaessigkeit
wird fuer den hier geprueften Zustandsvertrag offen vorausgesetzt.

Die lineare Diffusionsstruktur hat bekannte Vorlaeufer. Der
[bereits abgeschlossene Aging-Volltextvergleich](../../paper/paper_i/research/aging_full_text_comparison_2026-10-25.md)
liefert den direkten Parameteranschluss an Meunier, Milisic und Roux,
einschliesslich unterschiedlicher Initialisierungen. In dessen Notation
ist der Quellkoeffizient $a_{\rm source}=-ab$ und die Brownian-Amplitude
$\sigma=\sqrt{2D}$; ein Modellvergleich muss auch die Anfangsmemory
festlegen. Dessen Quellenbefund wird hier nicht als neue
Literaturentdeckung oder eigene Prioritaet
ausgegeben; neu geprueft wird der Quantenanschluss dieser Referenz.

## 2. Gleiche Ortsdichte und gleicher Strom reichen nicht

Schreibe $s=\operatorname{Var}X$, $k=\operatorname{Cov}(X,C)$ und
$r=\operatorname{Var}C$. Ito-Algebra liefert

$$
\dot s=-2a(s-k)+2D,\qquad
\dot k=b s-(a+b)k+a r,\qquad
\dot r=2b(k-r).
$$

Gauss-Anfangsdaten bleiben gaussverteilt. Fuer die Ortsmarginale $p$
folgt aus der gemeinsamen Fokker-Planck-Gleichung der **marginale** Strom

$$
\frac{j(x,t)}{p(x,t)}
=\left[-a\left(1-\frac{k}{s}\right)+\frac D s\right]x
=\frac{\dot s}{2s}x.
$$

Dabei wird die Projektion nicht als Markov-Prozess behauptet. Insbesondere
ist ein aus ihr konstruierter Rueckwaertsdrift kein ungeprueftes
Beschleunigungsgesetz fuer den vollen Memory-Prozess.

Zwei Ensembles mit gleichem $s,k$, aber verschiedenem $r$ haben somit
das gleiche $p,j$. Ihre zweite Varianzableitung unterscheidet sich um

$$
\Delta\ddot s=2a^2\Delta r.
$$

Eine feste, analytisch konstruierte Kontrolle benutzt Einheiten mit
$a=1$, $b=D=1/2$ und

$$
\Sigma_1=\begin{pmatrix}1&1/2\\1/2&1/2\end{pmatrix},\qquad
\Sigma_2=\begin{pmatrix}1&1/2\\1/2&1\end{pmatrix}.
$$

Beide Matrizen sind positiv definit, mit Determinanten $1/4$ und $3/4$.
Beide liefern $s=1$, $\dot s=0$, also identische positive Gaussdichte
und verschwindenden Strom. Dennoch ist $\ddot s_1=1/2$ und
$\ddot s_2=3/2$. Sogar fuer jedes endliche $t>0$ gilt exakt

$$
s_2(t)-s_1(t)=\frac12
\left(\frac{1-e^{-3t/2}}{3/2}\right)^2>0.
$$

Das folgt aus $\Delta\Sigma(t)=T(t)\Delta\Sigma(0)T(t)^T$; der gleiche
Rausch-Kovarianzterm hebt sich beim Vergleich auf. Keine Monte-Carlo-
Streuung und keine Signifikanzschaetzung werden verwendet.

Fuer die gepruefte Zuordnung zu einem reinen Zustand
$\psi=\sqrt p\exp(iS/\hbar)$ mit $\partial_xS=mj/p$ sind beide
Anfangswellenfunktionen bis auf globale Phase gleich. Ein gemeinsamer
wohldefinierter linearer Hamiltonoperator kann daraus nicht zwei
verschiedene spaetere Ortsdichten erzeugen.

**Wichtige Grenze:** $p,j$ bestimmen keine allgemeine gemischte
Quantendichtematrix. Eine Zuordnung der versteckten Memory-Varianz zu
weiteren Quantenzustandsdaten, ein vergroesserter Zustandsraum oder eine
eingeschraenkte Praeparationsklasse sind durch dieses Gegenbeispiel nicht
ausgeschlossen. Sie sind aber zusaetzlich zu spezifizieren und dynamisch
zu begruenden; die blosse Phasenumschreibung liefert sie nicht.

## 3. Ein momentaner Treffer ist kein invarianter Quanten-Sektor

Fuer eine positive zentrierte Gaussdichte mit Varianz $s(t)$ und dem
obigen Strom ist die Kontinuitaetsgleichung bereits erfuellt. Die
Schroedinger-Gleichung mit festem
$V(x)=m\Omega^2x^2/2$ verlangt zusaetzlich, mit
$d_Q=\hbar/(2m)>0$,

$$
\mathcal R_Q(t):=
\frac12s\ddot s-\frac14\dot s^2+\Omega^2s^2-d_Q^2=0.
$$

Einsetzen von $v=(\dot s/2s)x$ und
$\sqrt p\propto e^{-x^2/(4s)}$ in die Quanten-Hamilton-Jacobi-Gleichung
beweist die Identitaet direkt. Sie prueft die Form-/Stromdynamik;
eine rein zeitabhaengige globale Phase bleibt frei. Es wird weder
$d_Q=D$ noch $d_Q=D_{\rm eff}$ als native Identitaet angenommen.

In der konstruierten Kontrolle oben waehle fuer die **Referenz**
$\Omega=0$ und $d_Q=1/2$. Ensemble 1 hat dann
$\mathcal R_Q(0)=0$: Breite, Strom und erste Breitenbeschleunigung passen.
Aber die exakten Momentgleichungen geben

$$
\dddot s_1(0)=-7/4,\qquad
\dot{\mathcal R}_Q(0)=-7/8\ne0.
$$

Der scheinbar passende Anfangspunkt bleibt also nicht auf der
Quanten-Breitenbedingung. Ensemble 2 hat schon
$\mathcal R_Q(0)=1/2$. Dies sind gewaehlt einfache Gegenkontrollen,
keine gefundenen physikalischen Parameter oder angepassten Ziellaeufe.
Eine bloss anfangs erzwungene Relation $r=f(s,k)$ genuegt nicht: Sie muss
unter der gleichen Dynamik invariant oder mit kontrolliertem Fehler
geschlossen sein und die erforderlichen Praeparationen umfassen.

## 4. Freie Ausbreitung: auch das Memory-Zentrum hilft hier nicht

Da $A^2=-\lambda A$, ist

$$
T(t)=e^{At}=I+\frac{1-e^{-\lambda t}}\lambda A.
$$

Fuer eine feste lineare Ortsauslese $Y=\ell_xX+\ell_cC$ fordert
Translationskovarianz $\ell_x+\ell_c=1$. Ihre Rauschantwort ist

$$
\ell^T T(t)e_1=u+v e^{-\lambda t},\qquad
u=\frac b\lambda,\quad v=\frac{a\ell_x-b\ell_c}\lambda.
$$

Fuer jede Anfangskovarianz $\Sigma_0$ mit endlichen Eintraegen ergibt sich

$$
\operatorname{Var}Y_t=
\ell^T T(t)\Sigma_0T(t)^T\ell+
2D\left[u^2t+\frac{2uv}{\lambda}(1-e^{-\lambda t})
+\frac{v^2}{2\lambda}(1-e^{-2\lambda t})\right].
$$

$T(t)$ ist beschraenkt. Somit gilt fuer alle diese Auslesen, auch
$Y=X$ und $Y=C$,

$$
\operatorname{Var}Y_t=2D_{\rm eff}t+O(1),\qquad
D_{\rm eff}=D\left(\frac b{a+b}\right)^2>0.
$$

Die absolute Varianz ist gemeint, nicht die stationaere innere
Relativvarianz oder ein inkrementelles MSD. Auch eine nichtgaussische
Anfangsverteilung mit endlicher Kovarianz aendert diesen Schluss nicht.
Der $O(1)$-Rest ist bei festen Parametern und fester Anfangskovarianz
beschraenkt; keine Uniformitaet beim kritischen Grenzgang $\lambda\to0$.

Zum Vergleich liefert der freie Quanten-Hamiltonoperator $P^2/(2m)$

$$
\operatorname{Var}Q_t=\operatorname{Var}Q_0+
\frac{2t}{m}\operatorname{Cov}_{\rm sym}(Q,P)_0+
\frac{t^2}{m^2}\operatorname{Var}P_0.
$$

Diese allgemeine Formel, einschliesslich anfaenglicher Kontraktion,
steht bei [Robinett, Doncheski und Bassett, v1, Abschnitt II](https://arxiv.org/pdf/quant-ph/0502097v1).
Bei endlicher nichtverschwindender Ortsvarianz und $\hbar>0$ erzwingt
die Unschaerferelation positive Impulsvarianz. Im hier betrachteten
endlichen Momentbereich dominiert deshalb langfristig der $t^2$-Term.
Die Operatoridentitaet gilt durch Linearitaet auch fuer gemischte
Zustaende mit endlichen zweiten Momenten.

Damit gibt es unter festem linearem Orts-/Zeitreadout und festen
positiven Kalibrierungen keine exakte Identifikation dieses stabilen
linearen Memory-Modells mit der geschlossenen freien Teilchendynamik
fuer alle Zeiten. Ein isoliertes Intervall mit kleiner Abweichung,
singulaere Skalierungsgrenzen, nichtlineare Readouts oder ein offenes
Quantensystem mit Bad sind andere Behauptungen und hier nicht widerlegt.
Eine nichtlineare Zeitumparametrisierung waere ebenfalls ein anderer
physikalischer Vertrag, keine nachtraegliche Einheitenumrechnung.

Umgekehrt ist auch $t^2$-Ausbreitung **kein Quantennachweis**. Eine
klassische freie Phasenraum-Gausswolke mit passend gewaehlter Kovarianz
hat dieselbe Breitenentwicklung. Die Tests enthalten diesen positiven
Vergleich: Er besteht die notwendige Quanten-Breitenidentitaet, ohne
Interferenz, Born-Regel oder Messoperatoren herzuleiten.

## Quellenumfang, Verifikation und Konsequenz

Am 2026-11-06 wurden native lineare Hilfsformeln, der Paper-I-Anhang,
die Paarreduktion und der bestehende Aging-Abgleich erneut gelesen.
Frisch extern geprueft: Robinett, Doncheski und Bassett,
arXiv:quant-ph/0502097v1 (Metadatum 15.02.2005), Einleitung und
Abschnitt II, besonders Gleichungen (11), (13) und (15). Kein
Vollgutachten der 25-seitigen Arbeit oder ihrer Verlagsfassung.
Die freie Varianzformel ist bekannt, keine beanspruchte Neuerung.

[18 konstruierte Tests](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/tests/test_memory_quantum_closure.py)
pruefen diskrete Schreibreihenfolge, Matrixexponential und unabhaengige
Kovarianzquadratur, den Doppel-Praeparationskontrast, die nichtinvariante
Anfangsanpassung, vier lineare Ortsauslesen und drei freie Gausskontrollen.
Keine dieser Kontrollen ist eine neue Zieltrajektorie oder ein Beweis
des nichtlinearen Modelltransfers.

Verifikation am 2026-11-06: 72 betroffene Modell-/Dokumentationstests
bestanden in 2.81 s; zusaetzlich 20 bestehende Aging-Kontrollen in 0.79 s.
Lint und strikter MkDocs-Bau bestehen. Keine vollstaendige Repository-
Testsuite und keine Wiederholung eines AL1-, FIFO- oder P5-Ziellaufs.

**Konsequenz fuer das Ziel:** Den direkten linearen Quantenanschluss
nicht durch weitere Radius-, Rausch- oder Massenfits verfolgen. Ein
weiterer Kandidat muss einen bestimmten zusaetzlichen Mechanismus im
Bestand nachweisen oder als Erweiterung deklarieren: insbesondere einen
dynamisch geschlossenen Praeparations-/Zustandsraum und eine gemeinsame
Zeitentwicklung. Die benoetigte nichtlineare oder kollektive Struktur
ist durch diesen Bericht weder gefunden noch ausgeschlossen. Die
offene Autorenentscheidung wird nicht stellvertretend getroffen;
Referenz-Quantenaxiome bleiben getrennte Inputs. Paper I und die
geschlossenen AL1-/FIFO-/P5-Ausfuehrungen bleiben unveraendert.
