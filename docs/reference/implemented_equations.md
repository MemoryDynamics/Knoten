# Implementierte Gleichungen

Stand: 2026-09-02. Gepruefte Produktionscode-Linie bis Commit `2fbdf08`.

Diese Rueckwaertsspezifikation beginnt beim ausgefuehrten Code und schreibt
ihn in lesbarer Mathematik aus. Sie ist keine neue Modellannahme. Wo eine
Formel nur eine Interpretation nahelegt, wird das ausdruecklich getrennt.

## 1. Grundgroessen und endliches Gedaechtnis

Sei $x_n\in\mathbb C\simeq\mathbb R^2$ die aktuelle sichtbare Position und
$Y_n=(y_{0,n},\ldots,y_{H-1,n})$ die FIFO-Historie mit $y_{0,n}=x_n$.
Bezogen auf den Modellkern ist dieser Schleifenast die Spezialisierung
$\lambda_{\rm m}=\alpha$, $\beta_\rho=\alpha M_0$ und $\varepsilon=0$.
Die allgemeine Depositionsbreite $\sigma$ ist hier Delta-spezialisiert; die
separaten $\sigma_{\rm rep}$ und $\sigma_{\rm att}$ gehoeren zum Readkernel.
Der Code verwendet

$$
q=1-\alpha,\qquad
w_j=\alpha M_0 q^j,\qquad j=0,\ldots,H-1,
$$

wobei $0<\alpha<1$ die Vergessensrate, $H$ die gespeicherte Tiefe und $M_0$
`memory_mass` ist. $N$ bezeichnet dagegen die Zahl ausgefuehrter Updates und
ist keine Massenskala.

Mit

$$
M_H=\sum_{j=0}^{H-1}w_j=M_0(1-q^H),
\qquad \bar w_j=\frac{w_j}{M_H}
$$

ist die kanonische endliche Center-Uebertragungsfunktion

$$
B_H(z)=\sum_{j=0}^{H-1}\bar w_jz^{-j}
=\frac{\alpha}{1-q^H}
\frac{1-(qz^{-1})^H}{1-qz^{-1}},
\qquad B_H(1)=1.
$$

Die rohe gewichtete Summe ist dagegen
$W_H(z)=M_HB_H(z)$. Diese Unterscheidung folgt dem
[Modellvokabular](model_vocabulary.md) und verhindert zwei verschiedene
DC-Normierungen fuer dasselbe Symbol.

## 2. Native FIFO-Dynamik

Fuer $r_j=|y_{0,n}-y_{j,n}|$ implementiert der Double-Gaussian-Kanal

$$
\phi(r)=-\frac{A_{\rm rep}}{\sigma_{\rm rep}^2}
e^{-r^2/(2\sigma_{\rm rep}^2)}
+\frac{A_{\rm att}}{\sigma_{\rm att}^2}
e^{-r^2/(2\sigma_{\rm att}^2)},
$$

$$
G(Y_n)=\sum_{j=0}^{H-1}w_j\,\phi(r_j)(y_{0,n}-y_{j,n}).
$$

Ein nativer Schritt ist exakt

$$
y_{0,n+1}=y_{0,n}-\eta G(Y_n),\qquad
y_{j,n+1}=y_{j-1,n}\quad(j\ge 1).
$$

$\eta$ ist damit der diskrete Driftgain. Eliminiert man nur formal den
sichtbaren ersten Slot, folgt

$$
\Delta^2x_n=-\eta\,[G(Y_n)-G(Y_{n-1})].
$$

Das ist eine diskrete Gleichung zweiter Differenz, aber noch keine
Newton-Gleichung $m\Delta^2x=F$: Die rechte Seite enthaelt die gesamte
Historie und die Differenz zweier interner Gradienten. Eine positive,
zustandsunabhaengige Masse ist daraus nicht abgeleitet.

## 3. Rotierende Loesung und notched Center

Der Kreis-Ansatz lautet

$$
x_n=R e^{in\theta},\qquad y_{j,n}=R e^{i(n-j)\theta}.
$$

Fuer eine gewaehlte Harmonische $s$ lautet die kanonische Schreibweise

$$
b_s=B_H(e^{is\theta})
=\sum_{j=0}^{H-1}\bar w_j e^{-is\theta j},
$$

$$
a_0^{(s)}=\frac{\bar w_0-b_s}{1-b_s},\qquad
a_j^{(s)}=\frac{\bar w_j}{1-b_s}\quad(j\ge1),
$$

und damit den notched Center

$$
C_s(Y)=\sum_{j=0}^{H-1}a_j^{(s)}y_j
=\frac{\sum_j\bar w_jy_j-b_s y_0}{1-b_s},
\qquad c_n^{(s)}=C_s(Y_n).
$$

Der Filter loescht die registrierte Harmonische algebraisch. Das ist eine
konstruierte Observable, keine topologische $S^1$-Zertifizierung. Das
aktuelle Codefeld `OrbitCenterReadout.beta` entspricht $b_s$; es ist nicht
die Paper-I-Depositionsstaerke $\beta_\rho$.

## 4. Center-konjugierter Schreibport

Fuer eine Center-Kraft $F\in\mathbb C$ schreibt der Port mit dem
konjugierten Koeffizienten

$$
u=\overline{a_0^{(s)}}F,\qquad
y_0^+=y_0^\star+\alpha u.
$$

Mit

$$
\gamma_{\rm w}=|a_0^{(s)}|^2,
\qquad \mu_{\rm w}=\alpha\gamma_{\rm w}
$$

folgt exakt

$$
c^{(s),+}-c^{(s),\star}=\mu_{\rm w}F.
$$

Der Code trennt beim FIFO-Altern die Center-Verschiebung

$$
\delta c_{\rm age}
=\sum_{j=1}^{H-1}a_j^{(s)}(y_{j-1}-y_j),
$$

so dass
$c^{(s),+}-c^{(s),-}=a_0^{(s)}(y_0^+-y_0^-)+\delta c_{\rm age}$.
Fuer den reellen euklidischen
Skalarproduktsanteil $\langle a,b\rangle=\operatorname{Re}(\bar a b)$ gilt

$$
W_{\rm write}=\langle\overline{a_0^{(s)}}F,y_0^+-y_0^-\rangle,
\quad W_{\rm age}=\langle F,\delta c_{\rm age}\rangle,
\quad W_C=\langle F,c^{(s),+}-c^{(s),-}\rangle,
$$

$$
W_{\rm write}+W_{\rm age}-W_C=0,
\qquad
\alpha|\overline{a_0^{(s)}}F|^2=\mu_{\rm w}|F|^2\ge0.
$$

Das positive Vorzeichen ist eine Eigenschaft des definierten Ports. Es ist
kein unabhaengiger Nachweis positiver physikalischer Masse.

## 5. Zwei Center und gegenseitige Kopplung

Mit $d=c_A^{(s)}-c_B^{(s)}$ verwendet der Code das explizit eingefuehrte
Potential

$$
U_{\kappa_{\rm pair}}(d)=\frac{\kappa_{\rm pair}}{2}|d|^2.
$$

Seien $d^-$ die Trennung vor und $d^\star$ die Trennung nach beiden nativen
Schritten. Fuer den reziproken impliziten Mittelpunktport gilt

$$
F_A=-\kappa_{\rm pair}\frac{d^-+d^\star}
{2+\kappa_{\rm pair}(\mu_{{\rm w},A}+\mu_{{\rm w},B})},
\qquad F_B=-F_A,
$$

aequivalent zu
$F_A=-\kappa_{\rm pair}(d^-+d^+)/2$. Die Einwegkontrollen sind

$$
A\to B:\quad
F_B=+\kappa_{\rm pair}
\frac{d^-+d^\star}{2+\kappa_{\rm pair}\mu_{{\rm w},B}},
\quad F_A=0,
$$

$$
B\to A:\quad
F_A=-\kappa_{\rm pair}
\frac{d^-+d^\star}{2+\kappa_{\rm pair}\mu_{{\rm w},A}},
\quad F_B=0.
$$

Ihre Reservoirkraefte sind jeweils entgegengesetzt zur eingekoppelten
Einwegkraft. Der registrierte Pair-Ledger prueft

$$
\Delta U+W_A+W_B+W_{\rm reservoir}=0.
$$

Die Vorzeichen dieser Gleichungen sind im statischen Review algebraisch
konsistent. Die Kopplung selbst ist jedoch gesetzt, nicht emergiert.

## 6. Gemessene Antwort und Entscheidungsschicht

Alle Antworten werden gegen den channel-off-Pfad subtrahiert:
$\delta d=d_{\rm active}-d_{\rm off}$. Mit
$e_0=d_{\rm off}(0)/|d_{\rm off}(0)|$ und Referenzabstand $D_0$ sind

$$
L=-\operatorname{sgn}(\kappa_{\rm pair})
\frac{\operatorname{Re}(\delta d\,\overline{e_0})}{D_0},
\qquad
T=\frac{\operatorname{Im}(\delta d\,\overline{e_0})}{D_0}.
$$

Der nichtadditive Rest wird als

$$
X=\delta d_{\rm reciprocal}-\delta d_{A\to B}-\delta d_{B\to A}
$$

gemessen. Das registrierte Panel umfasst 64 off-Arme und 768 aktive Arme.
Die Klassifikation ist eine endliche, vorab festgelegte Entscheidung fuer
dieses Panel; sie ist weder Ensemble-Replikation noch Kontinuumsgrenze.

## 7. Codeabbildung und Reviewgrenze

| Mathematik | Kanonische Implementierung |
| --- | --- |
| $w_j$, $\phi$, $G$, FIFO-Schritt | [`rotating_wave_stability.py`](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/src/emergenz_knoten/rotating_wave_stability.py) |
| $b_s$, $a_j^{(s)}$, $C_s$, $\gamma_{\rm w}$, $\mu_{\rm w}$ | [`orbit_center_actuator.py`](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/src/emergenz_knoten/orbit_center_actuator.py); aktuelle Codealiase stehen im Vokabular |
| Center-Port, Einweg-/Reziprokkraft, Ledger | [`mutual_center_coupling.py`](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/src/emergenz_knoten/mutual_center_coupling.py) |
| Panel, Antwort, Klassifikation, Ausgabe | [`scalar_memory_loop_p5d_mutual_center_gate.py`](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/experiments/current/dynamics/rotation/scalar_memory_loop_p5d_mutual_center_gate.py) |
| unabhaengige Ergebnisrekonstruktion | [`scalar_memory_loop_p5d_mutual_center_result_audit.py`](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/experiments/current/dynamics/rotation/scalar_memory_loop_p5d_mutual_center_result_audit.py) |

Evidenz: Die obige Algebra spiegelt die aktuelle Implementierung. Inferenz:
Der Port kann als kontrollierte Wechselwirkungsarchitektur untersucht werden.
Hypothese: Traegheit oder Masse emergieren erst, wenn eine robuste reduzierte
Bewegungsgleichung, ein positiver zustandsunabhaengiger Antwortkoeffizient und
diskriminierende Kontrollen dies tragen. P5-D hat diesen Nachweis nicht
erbracht.
