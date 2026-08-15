# Review: skalarer Force-/Work-Port

Date: 2026-08-16.

Status: kritisches Ergebnisreview des prospektiv registrierten
Force-/Work-Port-Gates. Die analytische Niederfrequenzentwicklung unten ist
post hoc und veraendert keine Gateentscheidung.

## Kurzurteil

Der kanonische additive Kraftport entscheidet die registrierten Alternativen
eindeutig:

| Gate | Ergebnis |
|---|:---:|
| G0 Port- und Experimentvaliditaet | pass |
| G1 Antwort- und Arbeitsbilanz-Closure | pass |
| G2O overdamped scalar memory | pass |
| G2I regulaere positive endliche Traegheitsmasse | fail |

Alle vier Einzelkriterien von G2I scheitern. Der sichtbare Zustand reagiert
sofort auf den Impuls, bewegt sich danach rueckstellend statt mit positiver
Geschwindigkeit weiter, benoetigt bei festem Impuls divergierende
Ein-Schritt-Arbeit und besitzt im lokalen Kurzzeitfenster diffusive statt
ballistische MSD-Skalierung.

Damit ist eine positive endliche Masse fuer diesen Port nicht gestuetzt. Das
Ergebnis ist enger als ein allgemeines Masse-No-go: Es betrifft die lokale
skalare Reduktion mit Kraft direkt im sichtbaren Positionsupdate.

## Analytische Diskrimination

Mit \(r=x-c\), \(\Gamma=1+\chi\) und dem festgelegten Port gilt im lokalen
Grenzwert

\[
\dot x=-\chi r+f,\qquad
\dot c=r,\qquad
\dot r=-\Gamma r+f.
\]

Der deterministische Kraft-zu-Geschwindigkeit-Transfer ist daher

\[
{\dot X(s)\over F(s)}={s+1\over s+\Gamma}.
\]

Fuer \(\chi=4\) ist \(\Gamma=5\). Bei hoher Frequenz geht der Transfer gegen
eins; eine Kraftaenderung erscheint also unmittelbar in \(\dot x\). Eliminiert
man den Memory-Center, erhaelt man zwar formal eine Gleichung zweiter Ordnung,

\[
\ddot x+\Gamma\dot x=\dot f+f,
\]

aber gerade der Term \(\dot f\) unterscheidet sie von

\[
m\ddot x+\gamma\dot x=f,\qquad m>0.
\]

Die zweite Differenzordnung allein ist somit keine Newtonsche
Traegheitssignatur.

Fuer einen Ein-Schritt-Impuls \(f_0=J/\alpha\) folgen bereits aus der
Portdefinition

\[
{\Delta x\over J}=1,\qquad
{\alpha W\over J^2}=1,\qquad
{x_2-x_1\over\alpha J}\longrightarrow-\chi=-4.
\]

Eine regulaere endliche Masse hat dagegen keinen endlichen Positionssprung,
eine positive post-impulse Geschwindigkeit \(J/m\) und endliche
Impulsenergie. Auch der stationaere lokale sichtbare Prozess diskriminiert:

\[
\operatorname{MSD}_x(t)=2Dt+O(t^2),
\]

waehrend eine Position mit endlicher stationaerer
Geschwindigkeitsvarianz bei kurzen Zeiten proportional zu \(t^2\) waechst.

## Prospektive Ausfuehrung

Port, Arbeit, Alternativhypothesen, Schwellen, Alpha-Familie, Holdout,
Formation-Seeds 11--15 und MSD-Seed 20260816 wurden vor Implementierung und
vor Erzeugung dieser Antworten festgeschrieben. Der erste prospektive Lauf
erfolgte auf Revision e6a034b; die finale Wiederholung auf dem sauberen
Darstellungsstand 52bef2d aenderte keine Daten- oder Gatelogik.

Die Familie hielt \(\chi=4\), \(D=10^{-4}\), \(\alpha H=12\) und die
Kernparameter fest. Der vorregistrierte Holdout war \(\alpha=0.0025\).

| Diagnose | Ergebnis |
|---|---:|
| maximaler Force-off-Klonrest | 0 |
| maximaler exakter Rekurrenzrest | \(2.22\,10^{-16}\) |
| maximaler Fehler von \(\alpha W/J^2=1\) | \(7.05\,10^{-14}\) |
| groesster lokaler Radius \(R/\sigma_{\rm rep}\) | 0.010712 |
| simultane Forced/Control-Radiusspanne | 0.998677--1.001329 |
| groesster Finite-H-Ratenfehler | \(2.60\,10^{-5}\) |
| Holdout-Kontinuumsfehler, Position | 0.001367 |
| Holdout-Kontinuumsfehler, Relativkoordinate | 0.005083 |
| Holdout-Ledgerrest pro Arbeit | 0.005021 |
| Monte-Carlo-MSD-Fehler zur exakten diskreten Referenz | 0.001523 |

Die registrierten Hochfrequenzdiagnosen am Holdout waren

| Observable | Messwert | G2O | G2I |
|---|---:|:---:|:---:|
| direkter Feedthrough | 1.000000 | pass | fail |
| erste post-pulse Geschwindigkeit pro \(J\) | -3.990101 | pass | fail |
| \(\alpha W/J^2\) | 1.000000 | pass | fail |
| sichtbare MSD-Steigung | 0.959048 | pass | fail |

Die MSD-Referenzen lagen bei 0.959136 fuer die exakte diskrete Kovarianz und
0.959317 fuer den Kontinuumsprozess. Die Abweichung von eins ist daher
ueberwiegend der endlichen, vorab fixierten Fitspanne geschuldet und kein
Hinweis auf einen Zwischenexponenten.

## Was strukturell ist und was numerisch geprueft wurde

### Strukturell

- Der direkte Feedthrough folgt aus dem additiven Term \(\alpha f_n\).
- Die Ein-Schritt-Skalierung \(W=J^2/\alpha\) folgt aus Port und
  Rechtsendpunkt-Arbeitskonvention.
- Die negative post-pulse Antwort und der Transfer
  \((s+1)/(s+5)\) folgen aus der lokalen linearen Reduktion.
- Die lineare Kurzzeit-MSD folgt aus dem direkt in \(x\) eintretenden
  Brownian-Term.

Diese vier Punkte wurden durch die Simulation nicht entdeckt. Sie definieren
die vorab formulierte overdamped Alternative.

### Numerisch

- Der vollstaendige nichtlineare Finite-H-Simulator reproduziert seine
  lineare Referenz im kleinen lokalen Fenster.
- Mirroring, zwei Impulsstaerken und simultane Common-Noise-Kontrollen zeigen,
  dass die Antwort weder Even-Leakage noch relevante Nichtlinearitaet oder
  Radiusdeformation nutzt.
- Der Finite-H-Fehler bleibt klein, der Holdout naehert sich der
  Kontinuumsantwort, und der diskrete Arbeitsledger konvergiert in die
  erwartete Richtung.
- Die Monte-Carlo-MSD reproduziert die exakte diskrete Kovarianz.

Die numerischen Gates validieren damit die Einbettung und die
Grenzwertrechnung. Sie sind keine unabhaengige empirische Entdeckung von
Overdamping.

## Kritische Grenzen

1. **Portabhaengigkeit.** Kraft wurde direkt zu \(x\) addiert. Eine Kopplung
   an einen separat eingefuehrten Impulszustand haette absichtlich keinen
   direkten Feedthrough und wuerde Traegheit in die Architektur einsetzen.
2. **Dimensionslose Normierung.** Generalisierte Kraft und Arbeit besitzen
   keine SI-Abbildung. Es wurde nur die interne Portkonsistenz getestet.
3. **Arbeitskonvention.** Der exakte Koeffizient eins verwendet
   Rechtsendpunktarbeit. Eine andere Impulsregularisierung kann den
   Vorfaktor aendern; die Divergenz \(W\propto1/\alpha\) und damit die
   Diskrimination gegen endliche Impulsenergie bleibt bestehen.
4. **Lokaler Slice.** Impulse sind nur 0.5 und 1 Prozent des
   Kontinuumsradius. Der MSD-Arm simuliert die stationaere lokale lineare
   Reduktion, nicht einen vollstaendigen nichtlinearen Long-Run-Knoten.
5. **Seedrolle.** Fuenf neue Formationsseeds pruefen die lokale nichtlineare
   Einbettung. Common Noise und Odd-Mirroring entfernen absichtlich fast die
   gesamte stochastische Antwortvarianz; dies ist kein Populationstest.
6. **Singulaerer Input.** Bei festem \(J\) waechst die
   Ein-Schritt-Kraft wie \(1/\alpha\), waehrend die Zustandsverschiebung
   klein bleibt. Additive Ports besitzen keine Kraftsaettigung; eine solche
   Erweiterung wurde nicht getestet.

## Post-hoc Niederfrequenzcheck

Dieser Check war kein Gate. Fuer den beobachteten Transfer gilt

\[
{s+1\over s+5}={1\over5}+{4\over25}s+O(s^2).
\]

Die freie inertiale Mobilitaet expandiert als

\[
{1\over ms+\gamma}={1\over\gamma}-{m\over\gamma^2}s+O(s^2).
\]

Ein Match der beiden ersten Koeffizienten verlangte
\(\gamma=5\) und \(m=-4\). Auch im Niederfrequenzfenster entspricht der
Korrekturterm daher keiner positiven passiven Masse.

## Konsequenz

Die sichtbare diskrete DGL zweiter Ordnung ist unter dem kanonischen
konjugierten Port eine eliminierte Memory-Relaxationsgleichung, keine
Newtonsche Bewegungsgleichung. Weitere reine Alpha-Verfeinerung wuerde diese
strukturelle Aussage nur erneut bestaetigen.

Ein neuer Massekandidat muesste einen unabhaengig abgeleiteten Zustand mit
fehlendem Hochfrequenz-Feedthrough, positiver Speicherfunktion,
passiver Kraft-/Arbeitsbilanz und transferierbaren Holdouts liefern. Wird ein
Momentumfeld lediglich postuliert und die Kraft dort angelegt, waere die
Traegheit konstruiert, nicht aus dem bisherigen skalaren Memory emergiert.

## Referenzen

- [Preregistriertes Force-/Work-Protokoll](../preregistration/scalar_memory_force_work_port_protocol_2026-08-16.md)
- [Ergebnisbericht](../../../dynamics/limits/scalar_memory_force_work_port_gate_2026-08-16.md)
- [Vorheriges Kontinuumsreview](scalar_memory_continuum_limit_review_2026-08-15.md)
