# Review: skalarer Memory-Grenztest

Date: 2026-08-15.

Status: kritisches Ergebnisreview nach dem registrierten Erstlauf und der
prospektiven Reconciliation. Die post-hoc Diagnosen in diesem Dokument
veraendern keine vorregistrierte Gateentscheidung.

## Kurzurteil

Der konstruierte lokale skalare Memory-Relativmodus besitzt in der getesteten
gematchten Familie einen kontrollierten diskreten Kontinuumsgrenzwert. Die
prospektive Reconciliation besteht ihr korrigiertes Validitaetsgate, das
Finite-Tail-Gate und das Alpha-Konvergenzgate.

Das ist kein Nachweis emergenter physikalischer Masse. Der Grenzmodus ist eine
reelle Relaxation, die Parameter legen nur eine Rate fest, und der sichtbare
Pfad bleibt unter der registrierten Rauschskalierung nicht differenzierbar.

## Analytische Referenz

Fuer unendliches exponentielles Memory und die lokale Kernlinearisierung gilt

\[
x_{n+1}=x_n-g(x_n-c_n)+\varepsilon\xi_n,
\qquad
c_{n+1}=(1-\alpha)c_n+\alpha x_{n+1}.
\]

Mit `r_n=x_n-c_n`, `g=chi alpha` und `q=1-alpha` folgt exakt

\[
r_{n+1}=q(1-g)r_n+q\varepsilon\xi_n.
\]

Der deterministische relative Pol ist daher

\[
\lambda_\alpha=(1-\alpha)(1-\chi\alpha).
\]

Die Elimination des Centers ergibt fuer die sichtbare Koordinate eine
diskrete Gleichung zweiter Ordnung,

\[
x_{n+2}-(1+\lambda_\alpha)x_{n+1}+\lambda_\alpha x_n
=\varepsilon(\xi_{n+1}-q\xi_n).
\]

Ihre deterministischen Wurzeln sind `1` und `lambda_alpha`: eine
Translationsnullmode und genau eine reelle abklingende Mode. Es entsteht kein
komplexes Polpaar und keine unterdaempfte Schwingung.

Unter `t=alpha n`, festem `chi=g/alpha` und
`D=epsilon^2/(2 alpha)` gilt

\[
\Gamma_\alpha=-{1\over\alpha}\log\lambda_\alpha
=(1+\chi)+{1+\chi^2\over2}\alpha+O(\alpha^2).
\]

Fuer `chi=4` ist die Grenzrate `5`, mit einer vorhersagbaren linearen
Diskretisierungskorrektur `8.5 alpha+O(alpha^2)`.

## Was numerisch getestet wurde

Die Familie hielt `chi=4`, `D=1e-4` und zunaechst `C=alpha H=12` fest:

| alpha | H | beobachtete Rate | Fehler zu Rate 5 | RMS-Fehler zu exp(-5t) |
|---:|---:|---:|---:|---:|
| 0.0400 | 300 | 5.379476 | 0.075895 relativ | 0.046095 |
| 0.0200 | 600 | 5.179293 | 0.035859 relativ | 0.023504 |
| 0.0100 | 1200 | 5.087306 | 0.017461 relativ | 0.011887 |
| 0.0050 | 2400 | 5.043121 | 0.008624 relativ | 0.005984 |
| 0.0025 | 4800 | 5.021457 | 0.004291 relativ | 0.003006 |

Der feinste Punkt `alpha=0.0025` war der vorregistrierte Holdout. Seine
Brownian-Inkremente wurden nicht neu gezogen, sondern die groben Inkremente
wurden exakt aus dem feinsten gemeinsamen Rauschpfad summiert.

Separat wurde bei `alpha=0.01` die Tail-Ausdehnung getestet:

| C | H | verbleibende Tail-Masse | beobachtete Rate |
|---:|---:|---:|---:|
| 6 | 600 | 0.002405 | 5.090199 |
| 9 | 900 | 1.1794e-4 | 5.087441 |
| 12 | 1200 | 5.7841e-6 | 5.087306 |

Die medianen Antworten des nichtlinearen Simulators weichen in allen sieben
Zellen nur etwa `9.65e-6..1.03e-5` RMS-relativ von der vollstaendigen exakten
Finite-`H`-Antwort ab.

## Gatechronologie

Der erste, vorregistrierte Seed-1--5-Lauf bleibt formal
`experiment-inadequate`. Sein Radiusgate verglich den spaeten ungestoerten
Kontrollradius mit dem fruehen Kontrollradius, obwohl zwischen beiden Zeiten
Brownian-Rauschen wirkte. G1 und G2 erfuellten ihre Komponenten, waren wegen
G0 aber formal blockiert.

Die Reconciliation wurde danach separat registriert und verwendete neue Seeds
6--10. Sie ersetzte nur den fehlerhaften Radiusvergleich:

- alle Memory-Radien blieben positiv und endlich;
- `max R/sigma_rep = 0.010524 < 0.02`;
- jeder gestoerte Zweig blieb an jedem nativen Antwortsample relativ zu
  seiner simultanen Common-Noise-Kontrolle in
  `0.999606..1.000398`;
- Mirror-even-Leakage blieb unter `4.7e-8`;
- Offset-Staerken-Nichtlinearitaet blieb unter `9.8e-11`.

Damit bestehen G0R, G1R und G2R. Dieser Pass aendert die historische
Erstentscheidung nicht rueckwirkend.

## Post-hoc Konvergenzdiagnosen

Diese Werte waren keine zusaetzlichen registrierten Gates:

- Die lokalen log2-Ordnungen des RMS-Fehlers bei Alpha-Halbierung liegen bei
  etwa `0.97..0.99`.
- Die entsprechenden Ordnungen des Ratenfehlers liegen bei etwa
  `1.01..1.08`.
- Die absolute Ratenverschiebung kontrahiert von `C=6 -> 9` zu `C=9 -> 12`
  um den Faktor `0.0489`; fuer eine exponentielle Tail-Verkleinerung um drei
  Memory-Zeiten ist `exp(-3)=0.0498` die natuerliche Referenz.

Das ist konsistent mit erstordentlicher Schrittfehlerkonvergenz und
exponentieller Tail-Konvergenz. Es ist keine unabhaengige Replikation dieser
Ordnungszahlen.

## Strenge Claim-Grenze

### Evidenz

- Der implementierte nichtlineare Finite-Memory-Simulator reproduziert im
  kleinen lokalen Offsetfenster seine exakte diskrete Referenz.
- Bei festem `chi`, `D` und `C` konvergiert die diskrete Antwort gegen die
  registrierte Exponentialantwort.
- Die separate `C`-Achse zeigt die erwartete kontrahierende Tail-Sensitivitaet.

### Inferenz

Die konstruierte lokale skalare Memory-Center-Familie besitzt einen
kontrollierten kleinen-Schritt- und langen-Horizont-Grenzwert. Hierbei ist
`alpha=0.01` kein privilegierter Wert, sondern nur ein Mitglied der gematchten
Familie.

### Nicht gezeigt

- Bei festem `C` gilt `q^H -> exp(-C)`, nicht null. Der volle unendliche
  Memory-Tail erfordert zusaetzlich `C -> infinity`; die drei getesteten
  C-Werte stuetzen diese zweite Grenze, beweisen aber keine uniforme
  Doppelgrenze.
- Die Skalierung `eta proportional alpha`, `epsilon proportional sqrt(alpha)`
  und `H proportional 1/alpha` wurde konstruiert. Der Test zeigt ihre
  Konsistenz, nicht ihre Emergenz, Einzigartigkeit oder physische Auswahl.
- Fuenf prospektive Seeds pruefen Hintergruende und Nichtlinearitaet, liefern
  aber keine populationsweite statistische Aussage. Common Noise reduziert
  bewusst die Antwortvarianz.
- Es gibt keinen unabhaengig normierten Kraft-/Arbeitsport. Aus einer
  Relaxationsrate ist nur ein Verhaeltnis wie `gamma/m` identifizierbar, nicht
  `m` selbst.
- Wegen `epsilon proportional sqrt(alpha)` ist `x(t)` diffusionsartig und
  nicht klassisch zweimal differenzierbar. Die diskrete zweite Differenz ist
  daher keine regulare Newtonsche Beschleunigung.

## Naechster diskriminierender Test

Mehr Punkte bei kleinerem Alpha wuerden vor allem die bereits analytisch
eingebaute Konvergenz bestaetigen. Fuer einen Masse-/Traegheitsclaim ist ein
falsifizierenderer Schritt noetig:

1. einen unabhaengig normierten externen Kraft-/Arbeitsport festlegen;
2. Impulsantwort und Kurzzeit-MSD vorregistriert gegen diffusive
   `MSD proportional t`- und ballistische `MSD proportional t^2`-Nullen
   testen;
3. pruefen, ob Daempfung und eine zweite dynamische Skala getrennt
   identifizierbar sind und auf ungesehenen Protokollen transferieren.

Ohne diese Trennung sollte die beobachtete Groesse als Memory-Relaxationszeit,
nicht als emergente Masse bezeichnet werden.

## Referenzen

- [Originales Protokoll](../preregistration/scalar_memory_continuum_limit_protocol_2026-08-15.md)
- [Originaler Ergebnisbericht](../../../dynamics/limits/scalar_memory_continuum_limit_gate_2026-08-15.md)
- [Reconciliation-Protokoll](../preregistration/scalar_memory_continuum_limit_reconciliation_protocol_2026-08-15.md)
- [Prospektiver Ergebnisbericht](../../../dynamics/limits/scalar_memory_continuum_limit_reconciliation_2026-08-15.md)
