# Theoretical Context

Stand: 2026-06-30.

Diese Datei ist der kuratierte theoretische Kontext. Sie ersetzt die frueheren
Parallelseiten zur Non-Markovian Basis, Markov-Architektur und
Markov-Anforderungen.

## Minimaler Modellkern

Das Modell beschreibt eine sichtbare Zustandsvariable `x_n` und ein explizites
Gedaechtnisfeld oder eine endliche Memory-Reprasentation.

Sichtbarer Update:

```text
x_{n+1} = x_n + epsilon xi_n - eta grad (K * rho_n)(x_n)
```

Allgemeines Memory-Update:

```text
rho_{n+1}(x) = (1 - lambda_m) rho_n(x) + beta G_sigma(x - x_{n+1})
```

mit `0 < lambda_m < 1` und `beta >= 0`. Die oft verwendete Paper-I-Konvention
ist der normierte Spezialfall `lambda_m = beta = alpha`. Dann bleibt die
Memory-Masse bei normiertem `G_sigma` und normiertem Anfangszustand konstant.

Ausgerollt ergibt das eine exponentiell gewichtete Vergangenheit. Die
charakteristische Speicherpersistenz liegt in der normierten Konvention bei
`alpha^{-1}` Updates.

## Markov-Einbettung

Der sichtbare Prozess `x_n` ist im Allgemeinen nichtmarkovsch, weil der
naechste Schritt vom gespeicherten Feld abhaengt. Der augmentierte Zustand

```text
z_n = (x_n, rho_n)
```

bzw. eine konkrete Memory-Reprasentation ist dagegen die natuerliche
Markov-Einbettung. Formal gibt es einen Uebergangskern

```text
P(z, A) = Prob(z_{n+1} in A | z_n = z)
```

und einen positiven, unitalen Operator auf Observablen

```text
(U f)(z) = E[f(z_{n+1}) | z_n = z].
```

Die Iterationen bilden eine vorwaertsgerichtete Halbgruppe. Das ist im
stochastischen Fall im Allgemeinen kein deterministischer Algebra-
Automorphismus und keine reversible Gruppenwirkung.

Wichtig: Das affine Memory-Update ist bei bekanntem Depositionsort formal in
`rho_n` invertierbar, solange `lambda_m != 1`. Die Irreversibilitaet liegt
nicht in dieser einzelnen algebraischen Abbildung, sondern darin, dass der
aktuelle Zustand die vollstaendige geordnete Vergangenheit im Allgemeinen
nicht kodiert.

## Kontraktive Memory-Faser

Fuer denselben sichtbaren Pfad gilt

```text
rho_{n+1} - rho'_{n+1} = (1 - lambda_m)(rho_n - rho'_n).
```

Damit kontrahiert die Memory-Faser pfadweise exponentiell. Die volle Dynamik
kann trotzdem komplex sein, weil `rho_n` auf die sichtbare Bewegung
zurueckwirkt.

## Numerische Operator-Schicht

Die implementierte Schicht unter `src/emergenz_knoten/markov/` operationalisiert
diese Theorie:

| Modul | Rolle |
| --- | --- |
| `features.py` | verlustbehaftete Memory-Summary-Features fuer `z_n` |
| `dataset.py` | Sample-Trajektorien und Lagged Pairs `(z_i,z_{i+ell})` |
| `transition.py` | Labels, Transition Counts, row-stochastic matrices |
| `validation.py` | implied rates, timescales, CK-Fehler, Autokorrelation |
| `metastability.py` | slow modes und einfache spectral gaps |

Begriffliche Hygiene:

- `n` ist der Update-Index.
- `i` ist der Index gespeicherter Samples.
- `z_n` ist der mathematische augmentierte Zustand.
- `z_i` ist eine gespeicherte, meist reduzierte Feature-Reprasentation.
- `lag_time` ist nur ein numerischer Nenner fuer Raten, keine physikalische
  Zeit.

Reduzierte Features beweisen nicht, dass die Projektion exakt markovsch ist.
Sie liefern eine praktische Operatorapproximation, die gegen Residence,
Autokorrelation, CK-Fehler und Kontrollen getestet werden muss.

## Metastabilitaet

Ein Knoten ist im aktuellen Projekt kein fundamentales Teilchen und kein
exakter Fixpunkt. Er ist ein Kandidat fuer ein langlebiges Rueckkopplungsregime.
Diagnostiken:

- Residence-Zeiten in Updates und in Einheiten von `alpha^{-1}`;
- Memory-Gewicht in einer Region;
- Autokorrelation und Rueckkehrzeiten;
- lokale OU-/Hessian-Approximationen;
- slow modes oder fast-invariante Mengen eines Transferoperators.

Relaxationsraten sind derzeit Stabilitaets- oder mass-like proxies, keine
physikalischen Massen.

## Aktuelle Evidenzgrenzen

- Ein Baseline-Long-Run mit `n=10^7` zeigt ein starkes Residence-Signal.
- Ohne `eta_zero`, `single_scale`, weitere Seeds und Sensitivitaeten ist das
  kein robuster Paper-I-Befund.
- Der archivierte Near-3-Dimensionsbefund ist vielversprechend, aber keine
  allgemeine `d=3`-Ableitung.
- Endliche Signalgeschwindigkeit folgt nicht aus exponentiellem Memory allein;
  dafuer braucht es lokale Reichweite, mehrstufige Uebertragung und keine
  direkte Fernkopplung.

## Sprachregel

- `We define` fuer Modellannahmen und Diagnostiken.
- `We prove` nur fuer direkte strukturelle Aussagen wie Markov-Einbettung oder
  pfadweise Memory-Kontraktion.
- `We observe numerically` fuer reproduzierbare Simulationsergebnisse.
- `We conjecture` fuer Raumzeit-, Lorentz-, Quanten- oder Standardmodell-
  Bruecken.
