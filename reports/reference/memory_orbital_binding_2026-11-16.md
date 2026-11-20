# Von strikter Formstabilitaet zur lokalen Defektbindung

Stand: 2026-11-16. Bedingter analytischer Anschluss, **kein positiver
Stabilitaetsbefund** fuer einen Memory-Orbit. Der angefragte feste
Kandidat wird weder ausgewertet noch durch einen anderen ersetzt.
Keine neue Regel, Zielbahn, Parametersuche oder Aenderung an Paper I.

## Ergebnis

Fuer einen festen innenliegenden Vertreter der
[exakten Vierphasenfamilie](flat_memory_cycle_2026-11-16.md) gilt:
**Wenn alle acht verbleibenden Formmultiplikatoren strikt innerhalb des
Einheitskreises liegen, existiert eine kleine offene, vorwaertsinvariante
Umgebung der raeumlich verschobenen und gedrehten Vierzyklen.** Darin
konvergieren rauschfreie Historien orbital exponentiell, und ein regulaerer
+1-Defekt bleibt innerhalb der jeweils aktuellen Memory-Huelle gebunden.

Dies ist ein Implikationssatz. Seine entscheidende Spektralvoraussetzung
ist bisher fuer keinen positiven Vertreter nachgewiesen. Der Satz setzt
weder eine numerisch bestimmte Einzugsradiusgroesse noch eine physikalische
Ladung voraus oder liefert sie automatisch. Er schliesst die logische
Luecke zwischen einem kuenftigen strikten Spektralnachweis und lokaler
deterministischer Robustheit, nicht die bestehende Stabilitaetsluecke.

## 1. Neun nichtlineare Formkoordinaten, acht relevante Multiplikatoren

Der Zustand Y=(y0,...,y4) hat 15 Koordinaten. Die vier aktiv gewichteten
Schritte sind am Orbit alle von Laenge L>0. Die native Karte F ist daher
in einer Umgebung aller vier Phasen glatt; die Unstetigkeit der
Einheitsrichtung bei einem Nullschritt wird dort nicht beruehrt.
Alle Gains, Kernelbreiten und Retentionen bleiben bei Stoerungen fest.

Eine explizite Karte trennt nur die sechs echten SE(3)-Symmetrien ab:
Setze c=y0, e1=(y1-y0)/|y1-y0| und normiere den zu e1 orthogonalen
Anteil von y2-y0 zu e2. Mit e3=e1 cross e2 ist E=(e1,e2,e3) eine
eigentliche Rotation. Fuer z_j=E^T(y_j-c) gilt

$$
z_0=0,\quad z_1=(a,0,0),\quad z_2=(b,c_2,0),\quad
z_3=(d,e,f_3),\quad z_4=(g,h,i),\qquad a,c_2>0.
$$

Die neun Eintraege u=(a,b,c2,d,e,f3,g,h,i) bilden lokale Formkoordinaten.
Die Rekonstruktion y_j=c+E z_j ist glatt und eindeutig; an der
nichtplanaren Vierzyklusgeometrie ist f3 ungleich null. Keine
Alterspermutation wird als Symmetrie behandelt.

Die aelteste Schrittlaenge ist **keine weitere SE(3)-Symmetrie**.
Ihre radiale Variation kann vom naechsten nativen Update vollstaendig
vergessen werden, bezeichnet vorher aber einen anderen Zustand.
Der [lineare Acht-Formmoden-Quotient](memory_shape_quotient_2026-11-16.md)
darf diesen nachgewiesenen Nullfaktor fuer den Spektraltest entfernen.
Ein nichtlinearer Acht-Koordinaten-Abschluss folgt daraus nicht.
Hier bleibt die neunte, kontrahierende Nullrichtung deshalb erhalten.

Auch die uneigentliche Ein-Schritt-Symmetrie S wird nicht mit SO(3)
verwechselt. Eine Spiegelung kehrt in dieser Karte die beiden
e3-Komponenten f3 und i um. Die beiden Haendigkeitszweige werden nach
einem Schritt vertauscht; nach zwei Schritten kehrt die Bahn durch
eine eigentliche Rotation in denselben Zweig zurueck.
Die vierfache Karte P4=F^4 fixiert jeden Punkt
beider SE(3)-Gruppenorbits. Das sind diskrete Geometriephasen, kein
Spinorzeichen und keine elektrische Gegenladung; der Feldindex bleibt +1.

## 2. Vorwaertsbeweis ohne Invertierbarkeit des FIFO

Schreibe den Zustand als (g,u), g in SE(3). Aequivarianz und die vorige
Koordinatenkarte geben lokal fuer die vierfache Karte exakt

$$
P_4(g,u)=(g H(u),T(u)),\qquad H(u_*)=\mathrm{id},\quad T(u_*)=u_*.
$$

Dies ist nur eine Darstellung der vorhandenen Karte, keine angehaengte
Rotationsregel. Ihre Ableitung hat die Blockform

$$
D P_4=\begin{pmatrix}I_6&B_{6\times9}\\0&A_9\end{pmatrix},
\qquad A_9=D T(u_*).
$$

Aus D(F^4)=M^4 und der bereits bewiesenen Faktorzerlegung von M folgt
mit algebraischen Vielfachheiten

$$
\operatorname{spec}(A_9)=\{0,\mu_1^4,\ldots,\mu_8^4\}.
$$

Weitere Nullwurzeln unter den mu_j bleiben dabei erhalten. Sind alle
|mu_j|<1, ist A9 Schur-stabil, auch wenn es singulaer oder nichtnormal
ist. Definiere die konvergente Reihe

$$
P=\sum_{k=0}^{\infty}(A_9^k)^T A_9^k>0,\qquad
A_9^T P A_9-P=-I.
$$

In der Norm |v|_P=(v^T P v)^(1/2) gilt
||A9||_P=kappa0=sqrt(1-1/lambda_max(P))<1. Stetigkeit von DT liefert
einen Radius rho>0 und kappa zwischen kappa0 und eins mit

$$
\sup_{|u-u_*|_P\leq\rho}\|D T(u)\|_P\leq\kappa<1.
$$

Die konvexe P-Kugel ist damit vorwaertsinvariant unter T, und
|u_k-u_*|_P<=kappa^k |u_0-u_*|_P. Ein bekannter Ableitungsrest
||DT(u)-A9||_P<=L_T |u-u_*|_P wuerde z.B. die hinreichende Grenze
kappa0+L_T rho<1 liefern. Ein solcher numerischer Rest und ein konkreter
Radius sind hier **nicht** bestimmt. Eine kleine Spektralradiuszahl
allein liefert keinen endlichen Stoerungsradius.

Weil H(u*)=id und H glatt ist, sind sowohl die Translationsinkremente
als auch ||R(H(u_k))-I|| durch C kappa^k |u0-u*|_P beschraenkt.
Ihre Summen konvergieren. Daher existiert ein endliches g_infty in
SE(3), und F^(4k)(Y0) konvergiert exponentiell zu g_infty Y*.
Die drei Zwischenphasen konvergieren durch Glattheit entsprechend
zu g_infty F^j(Y*). Es bleibt kein unkontrollierter saekularer Drift
aus den sechs neutralen Symmetrierichtungen.

Um eine unter **jedem** Schritt invariante Umgebung zu erhalten,
waehle eine offene sichere Phasenumgebung W und die obige
gruppengesattigte P-Kugel U0 so klein, dass F^4(U0) Teilmenge U0
und F^j(U0) Teilmenge W fuer j=0,...,3. Dann ist

$$
U=\bigcup_{j=0}^{3}\left[F^{-j}(U_0)\cap
\bigcap_{k=0}^{j-1}F^{-k}(W)\right]
$$

offen, enthaelt die ganze Vierphasen-Gruppenbahn und erfuellt
F(U) Teilmenge U. Die leere Schnittmenge fuer j=0 bedeutet den
ganzen lokalen Definitionsbereich. F^-j bezeichnet hier ein **Urbild**,
keine inverse Dynamik. Fuer j>0 sinkt die Rueckkehrzeit um eins;
fuer j=0 liefern die drei sicheren Zwischenphasen den j=3-Zweig.
Eine lokale Inverse oder ein Diffeomorphismus wird nirgends benoetigt.

## 3. Explizite gemeinsame Feld- und Innenlagereserve

Sei Z eine Historie, deren fuenf Orte nach derselben starren Ausrichtung
je hoechstens delta vom Referenzorbit abweichen, delta<L/4. Alle Schritte
bleiben dann mindestens L-2 delta lang. Die elementare Normierungsgrenze
liefert |p_j(Z)-p_j(Y*)|<=4 delta/L. Mit W_v=sum_j w_j,
L1=1/(sigma sqrt(e)) und L2=1/sigma^2 folgen global in z

$$
\|V_Z-V_*\|_\infty\leq C_0\delta,\qquad
\|D V_Z-D V_*\|_\infty\leq C_1\delta,
$$

$$
C_0=W_v(4/L+L_1),\qquad C_1=W_v(4L_1/L+L_2),\qquad
\|D^2V_*\|_\infty\leq W_v L_2.
$$

Orte und Einheitsrichtungen werden gemeinsam variiert. Dies ist
keine unabhaengige Stoerung frei hinzugefuegter Richtungsfreiheitsgrade.
Die Schranken gelten auch bei aufgehobenem exaktem Ringschluss.

Am Referenzdefekt z* setze a_*=sigma_min(DV*(z*))>0. Fuer einen
festen Feldkugelradius b>0 genuegen

$$
\kappa_D=\frac{C_1\delta+W_v L_2 b}{a_*}<1,\qquad
\frac{C_0\delta}{a_*}+\kappa_D b<b.
$$

Denn z nach z-[DV*(z*)]^-1 V_Z(z) kontrahiert die abgeschlossene
b-Kugel um z* in ihr Inneres. Dort existiert genau eine Nullstelle,
ihr Jacobian bleibt regulaer, ihr Index ist +1, und

$$
|z(Z)-z_*|\leq\frac{C_0\delta}{a_*(1-\kappa_D)}<b.
$$

Dies konkretisiert den [Defektfortsetzungssatz](memory_defect_transport_2026-11-16.md)
fuer Stoerungen einer ganzen Historie, statt nur eines Quellen-/Tail-
Updates. Es behauptet keine globale Abwesenheit anderer ferner Defekte.

Fuer die abgeflachte Familie sind mit u_q=sigma^2 log q und
c_*=w0 G_sigma(z*-y0) bereits bekannt

$$
a_*=\frac{8c_*h^2}{\sigma^2 L},\qquad
\lambda_{\min}=\frac14+\frac{u_q}{8h^2}+\frac{u_q}{2r^2}>0.
$$

Alle vier baryzentrischen Koordinatengradienten haben Norm
sqrt(r^2+4h^2)/(4rh). Der Abstand zu der naechsten Huellenflaeche ist
daher exakt

$$
d_{\mathrm{core}}=\lambda_{\min}\frac{4rh}{\sqrt{r^2+4h^2}}>0.
$$

Wenn zusaetzlich b+delta<d_core, liegt die fortgesetzte Nullstelle
strikt in der gestoerten Memory-Huelle: Jede Stuetzfunktion der Huelle
aendert sich bei den Ortsstoerungen um hoechstens delta. Die Kugel
um z* mit Radius d_core-delta bleibt deshalb in der neuen Huelle.
Fuer jedes feste a_*>0 und d_core>0 lassen sich zuerst b und dann
delta positiv so klein waehlen, dass alle strikten Bedingungen gelten.
Die sichere Phasenumgebung W aus Abschnitt 2 kann darin liegen.

Damit ist der bedingte Bindungssatz bewiesen: Spektrale Kontraktion,
glatte nichtlineare Fortsetzung und geometrisch-feldtheoretische Reserve
wirken zusammen. Weder der Index allein noch eine eingefrorene
Feldableitung waere dafuer ausreichend. Die Reserven sind nicht uniform
bis h=0, q=1 oder bis zur Innenlagegrenze.

## 4. Was Robustheit hier nicht bedeutet

Der Satz gilt fuer hinreichend kleine Anfangsstoerungen bei epsilon=0,
festen Parametern und bereits gefuelltem Speicher. Er beweist keine
Entstehung aus leerer Memory, keinen globalen Attraktor und keine
endliche physikalische Masse oder Bindungsenergie. P ist eine lokale
Lyapunov-Metrik, kein hergeleiteter Energiebegriff.

Bei einem gesondert begrenzten Fehler nu pro reduzierter Vierfachkarte
wuerde |u_next-u*|_P<=kappa |u-u*|_P+nu gelten. Nur wenn
nu<(1-kappa)rho und auch alle Zwischenphasen innerhalb ihrer
Sicherheitsreserven bleiben, folgt eine robuste Formroehre. Die Pose
muss dann nicht zu einem Grenzwert konvergieren. Diese Voraussetzung
ist keine Eigenschaft unbeschraenkt gaussischen Rauschens und keine
berechnete Lebensdauer. Kein neuer Rauschlauf wurde durchgefuehrt.

Ein gebundener +1-Defekt waere ein robuster **Indextraeger**, noch kein
elektrischer Ladungstraeger. Gegenladung, elektrischer Quellenport,
Wechselwirkungsbilanz und Quantenstruktur bleiben getrennte Huerden.

## 5. Literaturabgleich und Kontrolle

| Quelle und tatsaechlich gepruefter Umfang | Verwendung und Grenze |
| --- | --- |
| [Fiedler, Sandstede, Scheel und Wulff, Documenta Mathematica 1, 479-505 (1996)](https://ems.press/content/serial-article-files/25797?nt=1), S. 479-483, insbesondere Satz 1.1 | Primaerquelle zur Trennung von Gruppenbewegung und Form bei nichtkompakten Gruppen. Dort Fluesse; die diskrete Karte oben wird direkt in eigenen Koordinaten hergeleitet, nicht aus einem Flusssatz uebernommen. |
| [Peet, ASU, Lecture 4 (2022)](https://control.asu.edu/Classes/MAE509/509Lecture04.pdf), Folien 13-15, insbesondere Lemma 12 und Reihenbeweis | Autoren-Lehrquelle zum diskreten Lyapunov-Kriterium. Im Reihenbeweis auf Folie 15 steht irrtuemlich Hurwitz; gebraucht wird dort Schur wie in Lemma 12. Die eigene Herleitung oben setzt ausdruecklich Schur voraus. Keine neue Stabilitaetsmethode beansprucht. |
| [Berger und Bounemoura, arXiv:1109.3280v1](https://arxiv.org/pdf/1109.3280), Abschnitt 2, Satz 2.1 | Gegenpruefung der Voraussetzungen: Diffeomorphismus und kompakte invariante Untermannigfaltigkeit. Weder die singulaere FIFO-Karte noch die volle nichtkompakte Translationsbahn rechtfertigt einen ungeprueften direkten Transfer. |

16 neue feste Kontrollen in `tests/test_memory_orbital_binding.py`
pruefen die Koordinatenrekonstruktion, SE(3)-Invarianz, Spiegelungszweige,
Rang neun und die nicht wegquotientierte alte Schrittlaenge. Hinzu kommen
exakte nichtnormale singulaere Lyapunov-Gegenkontrollen, ein Gegenbeispiel
gegen beliebige endliche Radien, statische native Feldschranken und die
Huellenreserve. Die statischen Historien haben keine zugewiesenen
Orbit-Gains; kein nativer Bewegungs- oder Spektrallauf wird ausgewertet.
Endliche Tests kontrollieren die Rechnungen, nicht den universellen Satz.
Die endliche Differenzenprobe der Koordinatenableitung verwendet eine
aus Rundungs- und zentralem Trunkationsfehler skalierte Diagnosetoleranz;
ihre urspruenglich zu enge feste Toleranz wurde nach einem Grenzfehler
von 3.6e-10 korrigiert, nicht als analytischer Nachweis interpretiert.

469 Tests im betroffenen Panel und Lint bestehen; ebenso der strikte
Dokumentationsbau. Keine vollstaendige Repository-Testsuite.
Der konkrete Schur-Nachweis und ein numerischer gemeinsamer
Radius bleiben offen. Der naechste Entscheidungspunkt bleibt unveraendert
die angefragte begrenzte Zielpruefung; die einzige Arbeitsreihenfolge
steht in den [Projektprioritaeten](../../docs/status/project_priorities.md).
