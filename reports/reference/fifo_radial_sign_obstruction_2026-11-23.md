# Der native Doppel-Gauss-Kernel reproduziert die Referenzbahnen nicht

Stand: 2026-11-23. Anschluss an den
[inversen radialen Referenzbenchmark](fifo_inverse_radial_pair_2026-11-23.md).
Feste Positionen, Vektorbreite und Retentionen, kein Kernel-Fit
und keine Zieltrajektorie.

**Befund.** Auf dem Plusumlauf muss der radiale skalare Kraftfaktor
in drei disjunkten Abstandsgruppen jeweils beide Vorzeichen
annehmen; auf dem Minusumlauf in zwei. Dies gilt fuer jeden
reellen Vektorgain, einschliesslich null. Keine Wahl von Amplituden
oder Breiten des nativen Doppel-Gauss-Kernels schliesst daher die
Kraftbilanz einer dieser zwei Geometrien. Der Plusumlauf scheitert
sogar fuer jede Summe aus hoechstens drei radialen Gauss-Terms.
Die Obstruktion betrifft diese Referenzgeometrien und ihre Umgebung,
nicht beliebige Bahnen oder Retentionen.

## 1. Aus der Kraftbilanz folgt eine endliche Vorzeichenbedingung

Wir verwenden die beiden rational fixierten Folgen von zehn
Orten, die skalare Retention $s=1/2$, Vektorretention $q=999/1000$,
Vektorbreite eins und $H_s=H_v=10$. In neueste-zuerst Ordnung
lautet die Bedingung fuer den Umlauf

$$
M c+\eta_v V=\Delta.
$$

Die Spalte $e$ von $M$ enthaelt die beiden altersgewichteten
Kraftbeitraege des jeweiligen Ortspaars. Der skalare
Kraftfaktor $c_e=f(D_e)$ am quadrierten Abstand $D_e$
absorbiert Gain, Memory-Normierung und den radialen
Gradientvorfaktor. $\Delta$ enthaelt die geforderten 40
Koordinateninkremente aller Phasen. $V$ ist der native
Gauss-Vektorreadout aus den normierten Schritten, noch
ohne den frei gelassenen Gain $\eta_v$.

Fuer eine Abstandsgruppe $I$, das Vorzeichen des Gains
$g\in\{-1,+1\}$ und ein gewuenschtes Kraftvorzeichen
$p\in\{-1,+1\}$ sei $y$ ein Testvektor mit

$$
\begin{aligned}
y^TM_e&=0 && (e\notin I),\\
y^TM_e&>0 && (e\in I),\\
p\,y^T\Delta&>0,\qquad & pg\,y^TV&<0 .
\end{aligned}
$$

Ist $g\eta_v\ge0$, folgt durch Multiplikation der
Kraftgleichung mit $p y^T$:

$$
p\sum_{e\in I}(y^TM_e)c_e
=p y^T\Delta-p\eta_v y^T V>0.
$$

Mindestens ein $c_e$ in dieser Gruppe hat somit das
Vorzeichen $p$. Die Methode ist eine lineare
Trennung im Sinne eines
[Farkas-Zertifikats](https://www.mit.edu/~gfarina/2024/67220s24_L04B_separation/L04B.pdf).
Die konkrete Altersabhaengigkeit und Abstandsgruppierung
stammen aus den FIFO-Kraftgleichungen.

## 2. Zertifizierte Gruppen und Mindestresiduen

In jeder unten stehenden Gruppe existieren die vier
Testvektoren fuer $(g,p)\in\{+1,-1\}^2$. Die
Gruppen liegen in **quadrierten** Abstaenden.

| Umlauf | Disjunkte offene Intervalle fuer $D$ | Mindestens notwendige Vorzeichenwechsel |
| --- | --- | ---: |
| Plus | $(2.25,2.75)$, $(23.25,23.75)$, $(62.25,62.75)$ | 3 |
| Minus | $(2.25,2.75)$, $(20,101)$ | 2 |

Die [Zertifikatsdatei](../../tests/fifo_radial_sign_certificates.json)
speichert rationale Koordinaten der freien Anteile von $y$.
Die uebrigen Koordinaten sind durch die exakten
Nullgleichungen ausserhalb der Gruppe eindeutig definiert.
Der [Verifier](../../tests/test_fifo_radial_sign_certificates.py)
rekonstruiert sie mit rationaler Elimination und prueft
alle Spaltenvorzeichen und Nullgleichungen exakt.
Nur $y^TV$ benoetigt transzendente Funktionen; das
Vorzeichen wird mit 50-stelliger Intervallarithmetik
einschliesslich Normierung und Gausswert eingeschlossen.
Ein lineares Programm diente zum Finden der Vektoren;
der Nachweis wiederholt oder vertraut diesem Loeser
nicht.

Die strikten Ungleichungen liefern auch eine Restschranke.
Fehlt das jeweilige Vorzeichen $p$ in einer Gruppe, dann
hat das Inkrementresiduum $R=Mc+\eta_vV-\Delta$ die Schranke

$$
\|R\|_\infty\ge \frac{-p y^TR}{\|y\|_1}
\ge \frac{p y^T\Delta}{\|y\|_1}.
$$

Die letzte Zahl ist fuer alle Pluszertifikate strikt
groesser als $1.7\cdot10^{-6}$ und fuer alle
Minuszertifikate strikt groesser als $4.6\cdot10^{-6}$,
jeweils in den Ortseinheiten des Referenzmodells.
Das sind garantierte Untergrenzen fuer mindestens
eine Kopfkoordinate, keine Angaben zur besten
Doppel-Gauss-Anpassung.

## 3. Warum keine Breiten- oder Amplitudensuche noetig ist

Beim nativen radialen Doppel-Gauss-Kernel ist
$f(D)=a e^{-\lambda D}+b e^{-\mu D}$, auch nach
isotroper Gauss-Deposition mit ihren effektiven Breiten.
Die Koeffizienten duerfen beliebige Vorzeichen haben.
Allgemein hat eine nichtverschwindende Summe von
$N$ Exponentialtermen mit verschiedenen reellen Exponenten
hoechstens $N-1$ verschiedene reelle Nullstellen.
Zum Beweis klammert man eine Exponentialfunktion aus,
so dass ein Term konstant ist. Ableiten laesst hoechstens
$N-1$ Terme uebrig, und Rolle liefert per Induktion den
Nullstellenschranke. Zusammenfallende Breiten reduzieren
die Termzahl. Die Nullfunktion erfuellt die
zertifizierten Vorzeichen ebenfalls nicht.

Da jedes Intervall einen positiven und einen negativen
Wert verlangt, ist je eine Nullstelle darin notwendig.
Somit braucht Plus mindestens vier verschiedene
Gauss-Skalen und Minus mindestens drei, falls das
Profil ueberhaupt als endliche Gauss-Summe dargestellt
wird. Das sind notwendige Bedingungen, keine
Existenz- oder Stabilitaetsbefunde fuer diese Termzahlen.
Insbesondere sind der Doppel-Gauss-Kernel fuer beide
Umlaeufe und ein kompensierter Dreifach-Gauss-Kernel
fuer den Plusumlauf ausgeschlossen.

Ganze weitere Umlaeufe im skalaren oder vektoriellen
FIFO aendern jeweils nur den gemeinsamen positiven
Vorfaktor des Kanals und fallen unter denselben Beweis.
Fuer hinreichend kleine gleichzeitige Aenderungen von
Geometrie, Retentionen und Vektorbreite besteht der
qualitative Ausschluss bei festen Horizonten fort:
Die Systeme fuer die abhaengigen Koordinaten bleiben
invertierbar; ihre stetige Loesung setzt die Nullgewichte
ausserhalb der Gruppen weiterhin exakt. Alle anderen
Ungleichungen sind strikt. Die Groesse dieser offenen
Umgebung wurde nicht bestimmt.

**Konsequenz.** Der invers konstruierte gemeinsame
Kernel testet die algebraische Freiheit des FIFO-Schritts,
nicht die Eignung des nativen Doppel-Gauss-Ansatzes.
Mehr Feintuning seiner Breiten hilft bei diesen
Bahnen nicht. Der naechste native Vergleich braucht
eine anders organisierte Bahngeometrie oder eine
begruendete neue Kopplung, statt mehr Anpassungswerte
am gleichen inversen Paar. Stabilitaet, spontane Bildung
und Wechselwirkung sind damit weiterhin nicht gezeigt.
