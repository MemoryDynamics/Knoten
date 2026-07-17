# Theoretical Context

Stand: 2026-07-17.

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

Implementationskonvention fuer den korrigierten Double-Gaussian-Kernel:
Der Paketkern berechnet jetzt den echten Potentialgradienten von
`K = A_rep G_rep - A_att G_att` und integriert
`x_{n+1}=x_n + epsilon xi_n - eta grad`. Damit ist `A_rep` ein lokaler
repulsiver Potentialkanal und `A_att` ein breiter attraktiver Potentialkanal.
Die lokale linearisierte repulsive Skala ist
`eta(A_rep/sigma_rep^2 - A_att/sigma_att^2)`. Vor dem Report
`reports/kernels/corrected_sign/kernel_sign_convention_correction_2026-07-09.md` erzeugte numerische
Evidenz gehoert zur `legacy-sign`-Konvention und muss fuer das korrigierte
Potentialmodell neu gerechnet werden.

Deposition-Konventionen:

- `delta`: alte Punktspur; `rho_n` ist eine gewichtete Liste vergangener Punkte.
- `gaussian`: normierter endlicher Depositionskernel mit expliziter Breite.
- `matched_gaussian`: normierte Gauss-Deposition mit derselben Breite wie die
  jeweilige Lesekomponente, gerechnet als effektiver Faltungskernel.

Fuer normierte Gauss-Deposition gilt bei `s=L`:

```text
L_eff = sqrt(2) L,
A_eff = A 2^{-d/2},
(A_eff/L_eff^2)/(A/L^2) = 2^{-(d/2+1)}.
```

In `d=3` reduziert Matching ohne Renormierung die lokale Steifigkeit um etwa
Faktor `5.66`. Deshalb ist der naechste faire Kerneltest nicht bloss
`matched_deposition`, sondern eine curvature-renormalized matched condition.

Zero-Mean-Zweiskalenkernel:

Fuer den unnormalisierten Double-Gaussian-Kernel

```text
K(r) = A_rep exp(-r^2/(2 L_rep^2)) - A_att exp(-r^2/(2 L_att^2))
```

ist `int K = 0` aequivalent zu

```text
A_att = A_rep (L_rep/L_att)^d.
```

Diese kompensierte Normierung entfernt den globalen DC-Anteil des Kernels und
ist eine eigene, sauber testbare Kernelhypothese. Sie ist nicht dasselbe wie ein
signierter Depositionskernel `G=K`.

## Self- and Cross-Interaction Channels

The current scalar memory is non-negative and the same two-scale kernel is used
for self-confinement and for the frozen-source cross-field. This gives every
source the same scalar sign. In the canonical `A_rep=1`, `A_att=35`,
`sigma_att/sigma_rep=3` slice,

```text
A_att / sigma_att^2 > A_rep / sigma_rep^2,
```

so the point-source potential has an attractive local minimum and no radial
force-sign crossing. This is a parameter consequence, not evidence for charge
neutrality or reciprocal two-knot attraction.

A radial scalar potential is parity-even. Charge sign is a separate internal
label; charge neutrality would remove a leading signed monopole rather than
produce universal attraction. The minimal controlled extension is therefore a
separate signed scalar cross-channel, for example

```text
x_i' = ... - eta_self grad Phi_i_self
           - eta_cross s_i s_j grad Phi_j_cross,
s_i in {-1, 0, +1}.
```

The sign convention and `K_cross` must be chosen explicitly; the labels must
not be called electric charge until interaction tests justify that language.
Required controls are `s_i=0`, `s_j=0`, one-label sign reversal, common-noise
pairing, and unchanged scalar self-confinement.

The self and cross kernels need not have the same resolution. For the current
`N=100M` checkpoints, the memory radius is only order `1e-4 sigma_rep`, so
the existing cross-kernel sees a point monopole and cannot read internal knot
shape. A narrower or moment-coupled cross-observable is a separate model choice.
Vector memory is reserved for orientation, phase, circulation, or polarization,
not introduced merely to provide a scalar sign.

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
| `vector_memory.py` | orientierte Memory-Features und kontrollierte Vektor-Pilotdynamik |
| `knot_score.py` | Scorecard-Helfer fuer Residence-, Kompaktheits- und Memory-Cloud-Evidenz |

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

- Residence-Zeiten in Updates und in Einheiten von `lambda_m^{-1}` bzw. `alpha^{-1}` in der normierten Konvention;
- Memory-Gewicht in einer Region;
- Autokorrelation und Rueckkehrzeiten;
- lokale OU-/Hessian-Approximationen;
- slow modes oder fast-invariante Mengen eines Transferoperators.

Relaxationsraten sind derzeit Stabilitaets- oder mass-like proxies, keine
physikalischen Massen.

## Aktuelle Evidenzgrenzen

- Die bisherigen `baseline`/`single_scale`-Confinement-Befunde vor dem
  Sign-Fix sind `legacy-sign`-Befunde und nicht als Evidenz fuer das
  korrigierte Potentialmodell zitierbar.
- Der korrigierte q=3-Retest zeigt repulsionsdominierte Dispersion bei
  `A_att=0.35`; die Amplitudenhierarchie findet kompakte Kurzlauf-Kandidaten
  bei `A_att=9..35`.
- Der erste AR-Modentest auf den skalaren Kandidaten findet nur reelle
  langsame Moden. Das stuetzt eine Relaxations-/Kompaktheitslesart des
  skalaren Memory-Modells, aber noch keine oszillatorische oder photonartige
  Dynamik.
- Der erste Vektormemory-Pilot zeigt komplexe AR-Moden bereits im
  `eta_v=0`-Fallback. Das ist nicht dasselbe wie `eta_s=0`: der skalare
  Potentialkanal war in diesem Pilot weiter aktiv. Ein echter Vektoreffekt
  muss sich gegen diesen Fallback und gegen reine `eta_s=eta_v=0`-
  Rauschkontrollen durchsetzen. Die erste `eta_s=eta_v=0`-Kontrolle zeigt
  bereits komplexe AR-Paare, also ist Komplexitaet allein kein Modenclaim.
- Komplexe AR-Eigenwerte einer reduzierten Feature-Projektion sind noch keine
  Schroedinger-Gleichung. Fuer eine quantenartige Lesart braucht es eine
  stabile Phasenstruktur, Norm-/Wahrscheinlichkeitserhaltung bzw. eine
  effektiv antihermitesche/hamiltonsche Komponente, die ueber Lags und
  Kontrollen reproduzierbar bleibt.
- Der archivierte `d~3`-Befund bleibt offen; daraus folgt noch keine
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
