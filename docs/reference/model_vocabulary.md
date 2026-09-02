# Kanonisches Modellvokabular

Stand: 2026-09-02.

Diese Seite ist die verbindliche Zielsprache fuer aktive Dokumentation, neue
Gleichungen und kuenftige Code-Remediation. Historische Reports und
gespeicherte Ergebnisfelder werden nicht rueckwirkend umbenannt. Ein Symbol
erhaelt durch seine Bezeichnung keine physikalische Interpretation.

Der zugehoerige
[targetfreie Vokabularaudit](https://github.com/MemoryDynamics/Knoten/blob/codex/p5-interaction-design/reports/project/meta/reviews/model_vocabulary_remediation_audit_2026-09-02.md)
dokumentiert die gefundenen Kollisionen und die Migrationsgrenze.

## 1. Grundregel

Der Modellkern wird immer zuerst in der Paper-I-Sprache angegeben:

$$
x_{n+1}=x_n+\varepsilon\xi_n-\eta\nabla\Phi_n(x_n),
\qquad \Phi_n=K\ast\rho_n,
$$

$$
\rho_{n+1}=(1-\lambda_{\rm m})\rho_n
+\beta_\rho G_\sigma(\mathord\cdot-x_{n+1}).
$$

Im normierten Spezialfall gilt
$\lambda_{\rm m}=\beta_\rho=\alpha$. Erweiterungen muessen ihre Groessen aus
diesen Grundgroessen ableiten oder als neue Annahme markieren; sie duerfen
den Kern nicht stillschweigend umbenennen.

## 2. Kanonische Grundgroessen

### Zustand und Update

| Symbol | Bedeutung | Codebezeichnung |
| --- | --- | --- |
| $n$ | diskreter Updateindex | Schleifenindex |
| $N$ | Zahl ausgefuehrter Updates | `steps` |
| $x_n$ | sichtbarer Zustand bzw. aktuelle Position | `position`, neuester History-Slot |
| $\rho_n$ | relaxierender Memory-Zustand | Feld oder endliche Historie |
| $\xi_n$ | dimensionsloses Einheitsrauschen | RNG-Innovation |
| $\varepsilon$ | Rauschamplitude pro Update | `epsilon` |
| $\eta$ | Gain des Memory-Drifts | `eta` |

### Memory und Kernel

| Symbol | Bedeutung | Codebezeichnung |
| --- | --- | --- |
| $\lambda_{\rm m}$ | allgemeiner vergessener Anteil | `alpha` |
| $\beta_\rho$ | allgemeine Depositionsstaerke | historisch oft `beta` |
| $\alpha$ | normierter Fall $\lambda_{\rm m}=\beta_\rho$ | `alpha` |
| $M_0$ | stationaere Memory-Masse bei normierter Deposition | `memory_mass` |
| $\sigma$ | Depositions-/Grobkoernungsbreite | `deposition_sigma` bzw. qualifizierte Breite |
| $K$, $\ell$ | Readkernel und seine Laengenskala | Kernelfamilie und qualifizierte Breiten |

$\beta$ ohne Qualifikator ist in neuer Dokumentation nicht zulaessig. Der
Index $\rho$ kennzeichnet die Deposition und verhindert die Kollision mit
Filterantworten oder Skalierungsexponenten.

## 3. Abgeleitete endliche Memory-Groessen

Fuer $q=1-\alpha$ und FIFO-Tiefe $H$ gelten

$$
w_j=\alpha M_0q^j,
\qquad M_H=M_0(1-q^H),
\qquad \bar w_j=\frac{w_j}{M_H}.
$$

Der Name $B_H$ ist ausschliesslich fuer den normierten Center-Filter
reserviert:

$$
B_H(z)=\sum_{j=0}^{H-1}\bar w_jz^{-j},
\qquad B_H(1)=1.
$$

Die rohe gewichtete Summe heisst $W_H(z)=M_HB_H(z)$, nicht ebenfalls $B_H$.
Der Gedächtnisschwerpunkt ist $c_n=B_H(L)x_n$; $c$ bleibt damit fuer eine
Centerkoordinate reserviert. $g_H$ bezeichnet nur den lokalen nativen
Rueckstellgain $g_H=\eta M_H\kappa_K$.

## 4. Kanonische Schleifen- und Portgroessen

Der Rotationsast darf neue abgeleitete Groessen verwenden, aber nur mit
eigenem Namensraum:

### Orbit und Readout

| Symbol | Bedeutung | aktueller Codealias |
| --- | --- | --- |
| $R,\theta,s$ | Radius, Phasenschritt, Harmonische | `radius`, `theta`, `harmonic` |
| $b_s=B_H(e^{is\theta})$ | komplexe Filterantwort der Harmonischen | `OrbitCenterReadout.beta` |
| $a_j^{(s)}$ | Koeffizienten des notched Center-Operators | `coefficients[j]` |
| $C_s$ | linearer notched Center-Operator | `orbit_center(...)` |
| $c_n^{(s)}=C_s(Y_n)$ | von $C_s$ gelesene Centerkoordinate | `center` |

### Port

| Symbol | Bedeutung | aktueller Codealias |
| --- | --- | --- |
| $\gamma_{\rm w}=|a_0^{(s)}|^2$ | dimensionsloser Write-Gain | `write_gain` |
| $\mu_{\rm w}=\alpha\gamma_{\rm w}$ | Center-Verschiebung pro Kraft | lokale Variable `mobility` |
| $\kappa_{\rm pair}$ | explizite Paarkopplungsstaerke | `coupling` |
| $F$ | Kraft am definierten Center-Port | `force` |

Damit sind $b_s$, $a_j^{(s)}$, $\gamma_{\rm w}$ und $\mu_{\rm w}$ klar als
abgeleitete Portgroessen erkennbar. Sie ersetzen weder $\alpha$,
$\varepsilon$, $\eta$, $\sigma$ noch $M_0$.

## 5. Numerische und physikalische Reservierungen

- Die Maschinenrundung heisst $u_{64}$ bzw. `unit_roundoff`, nicht
  $\varepsilon_{64}$ bzw. `epsilon64`; $\varepsilon$ bleibt der Rauschamplitude
  vorbehalten.
- $m$ oder $m_{\rm eff}$ wird nur nach einem operationalen Massegate benutzt.
  Eine Filtertraegheit bleibt $m_{\rm filter}$.
- $c_n$ ist eine Centerkoordinate; Koeffizienten tragen $a_j$ oder einen
  anderen qualifizierten Buchstaben.
- $g_H$ ist nativer Rueckstellgain; andere Gains erhalten einen Index oder
  einen beschreibenden Codenamen.
- $\kappa_K$, $\kappa_c$ und $\kappa_{\rm pair}$ trennen Kernelkruemmung,
  Centerrelaxation und explizite Paarkopplung.
- Gate-Namen wie „Gate B“ sind Prosa und keine mathematischen Symbole.

## 6. Code- und Schemamigration

Die aktuelle Implementierung und gespeicherte P5-Schemata enthalten noch
mehrdeutige Namen. Ihre Korrektur ist Teil der P5-Remediation:

| Altname | Zielname | Migrationsregel |
| --- | --- | --- |
| `OrbitCenterReadout.beta` | `notch_response` | Codealias erst mit Deprecation-Test entfernen |
| `beta_real/imag/abs` | `notch_response_real/imag/abs` | nur in neuer Schema-Version |
| `coefficients` ohne mathematischen Vertrag | `center_coefficients` | $a_j^{(s)}$ in Dokumentation |
| `write_gain` | bleibt beschreibender Codename | mathematisch $\gamma_{\rm w}$ |
| lokale `mobility` | `write_mobility` | mathematisch $\mu_{\rm w}$ |
| `epsilon64` | `unit_roundoff` | getrennt von Input `epsilon` |
| `epsilon_scale` als Toleranz | `scale_tolerance` | nur mit Protokoll-/Schema-Versionierung |

Historische JSON-Dateien, Reports, Hashes und Protokollzitate bleiben
unveraendert. Eine neue Ausgabe muss eine explizite Schema-Version und, falls
noetig, einen getesteten Lesekompatibilitaetsadapter besitzen.

Dieser Pass migriert die Paper-I-Kerngleichung, die Center-Filter-Seite und
die P5-Rueckwaertsspezifikation. Tiefere Modellabschnitte im theoretischen
Kontext verwenden teilweise noch lokale Koeffizienten namens $g$, $c$ oder
$\mu$ fuer andere Subsysteme. Sie sind dokumentierte Migrationsschuld und
muessen vor Wiederverwendung in Paper- oder Readiness-Sprache qualifiziert
werden; eine unmarkierte globale Textersetzung waere mathematisch unsicher.

## 7. Schreib- und Reviewregeln

1. Jede neue Gleichung beginnt mit den Grundgroessen oder verweist auf deren
   Ableitung.
2. Neue Symbole erscheinen vor der ersten Verwendung in einer Definition.
3. Derselbe Buchstabe bezeichnet innerhalb eines aktiven Dokuments nicht
   zwei verschiedene Groessen.
4. Codefelder bevorzugen beschreibende englische Namen; griechische
   Transliterationen bleiben auf stabile Grundparameter beschraenkt.
5. Historische Bezeichnungen werden als `historischer Alias` markiert, nicht
   still korrigiert.
6. Ein Notationswechsel aendert keinen wissenschaftlichen Gate-Status.
7. Der Notationsvertrag wird in Readiness-Reviews wie ein Schema geprueft.
