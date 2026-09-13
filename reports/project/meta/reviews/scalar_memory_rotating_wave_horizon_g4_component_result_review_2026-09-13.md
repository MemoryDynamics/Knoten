# Ergebnisreview: isolierter G4-Komponenten-Retry

Datum: 2026-09-13.

Verdict:
**`g4-local-infinite-root-pass-reviewed`**.

## 1. Ausgefuehrter Vertrag

Der einmalige korrigierte Retry lief auf dem sauberen Commit
`fb1cc7d3f9fac5aa9cc2b5e3000ccf030df50c71` nach gruener exakter CI. Er
verwendete unveraendert $\alpha=0.01$, $q=0.99$, $M_0=1$, $\eta=0.15$,
$H=3600$ und den eingefrorenen Start
$(0.946517504804225,0.015770381717135)$. Es gab keine Parametersuche,
Boxanpassung oder Wiederholung.

## 2. Endlicher Root

Nach acht 120-dps-Newtonschritten lautet der verwendete endliche Root

$$
R=0.9465169194795053579645380758218160210\ldots,
$$

$$
\theta=0.01577045072365344306369453060049318016\ldots.
$$

Das gespeicherte Residuum ist in der ersten Komponente
$-2.84\times10^{-123}$ und in der zweiten Komponente exakt als null
serialisiert. Die endlichen $10^{-8}$- und $10^{-30}$-Krawczykboxen bestehen.

## 3. Tailbounds und strikter Einschluss

Fuer den ausgelassenen unendlichen Tail wurden in beiden
Praezisionspanels dieselben outward-gerundeten Bounds rekonstruiert:

| Groesse | Obergrenze |
| --- | ---: |
| Residuum | $8.062863536789153\times10^{-17}$ |
| Radius-Jacobispalte | $7.955008275963771\times10^{-17}$ |
| Winkel-Jacobispalte | $3.1096332698326035\times10^{-13}$ |

Beide Tail-Krawczyk-Bilder liegen strikt in der registrierten
$10^{-10}$-Box. Die kleinsten Abstaende zum Boxrand betragen etwa
$9.99973\times10^{-11}$ fuer $R$ und $9.99999\times10^{-11}$ fuer
$\theta$. Die Bildbreiten betragen nur $5.33\times10^{-15}$ beziehungsweise
$2.27\times10^{-16}$; der Pass ist damit nicht durch einen numerisch knappen
Randkontakt entstanden.

## 4. Praezisionspanel und Ueberlappung

Die getrennten 120- und 160-dps-Rechnungen bestehen beide den strikten
Einschluss. Ihre gespeicherten Bilder ueberlappen in beiden Koordinaten; der
Schnitt besitzt dieselben fuehrenden Breiten wie das engere 160-dps-Bild.
Das ist eine Praezisionskontrolle innerhalb desselben Backends, keine
unabhaengige Replikation.

## 5. Provenienz und unabhaengiger Recordaudit

Das Manifest bindet Ergebnis und Lesereport mit SHA-256 an den
Ausfuehrungscommit und den Hash des Retry-Protokolls. Der getrennte
Standardbibliothek-Auditor rekonstruiert alle acht Checks und urteilt
`g4-independent-audit-agrees`. Er importiert weder Runner noch Horizontgate,
ist aber kein zweiter Intervallbackend.

## 6. Wissenschaftlicher Befund

Unter den registrierten analytischen Tailbounds und der Trust Base
`mpmath.iv==1.3.0` zertifizieren die beiden strikten Krawczyk-Panels einen
lokalen Root von $F_\infty$ in der registrierten Box. Unter den verwendeten
Krawczyk-Voraussetzungen ist der Root dort lokal eindeutig.

Nicht gezeigt sind die Verbindung dieses Roots mit der gesamten endlichen
G1--G3-Horizontleiter, dynamische Stabilitaet G5, Attraktion oder Formation.
Insbesondere folgt weder Zwei-Schleifen-Transfer noch Interaktion, interne
$S^1$-Phase, Traegheit oder Masse.

## 7. Folgeentscheidung

Der isolierte G4-Komponentenblock ist abgeschlossen. Fuer den
vollstaendigen Fixed-$\alpha$-Horizontclaim bleiben G1--G3, G5 und G6 im
gemeinsamen Ergebnisvertrag erforderlich. Der naechste erlaubte
Remediationsbaustein ist daher targetfreie LCG-Arnoldi-/G5-Integration; ein
weiterer Ziel- oder P5-D-Lauf ist durch diesen Pass nicht autorisiert.
