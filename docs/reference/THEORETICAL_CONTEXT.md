# Theoretical Context

Stand: 2026-07-19.

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

Write-/Read-Faktorisierung: Fuer homogene lineare Faltung gilt nach Ausrollen

```text
Phi_n = K * rho_n
      = initial term + beta sum_j q^j (K * G)(.-x_{n-j}),
W_eff = K * G.
```

Die sichtbare skalare Dynamik identifiziert daher nur `W_eff`, nicht `K`
und `G` getrennt. Weil Faltung kommutativ ist, erzeugt ein blosses Vertauschen
bei festem `W_eff` keine neue sichtbare Physik. Es ist auch semantisch
problematisch: Der attraktive/repulsive `K` ist vorzeichenbehaftet und weder
ein normierter noch ein nichtnegativer Depositionskernel. Die aktuelle
Delta-Deposition ist die maximal aufloesende Occupancy-Darstellung; die
fehlende Strukturantwort stammt im One-Way-Test vom breiten Cross-Lesekernel,
nicht von einer Glaettung beim Schreiben.

Fuer normierte Gauss-Deposition gilt bei `s=L`:

```text
L_eff = sqrt(2) L,
A_eff = A 2^{-d/2},
(A_eff/L_eff^2)/(A/L^2) = 2^{-(d/2+1)}.
```

In `d=3` reduziert Matching ohne Renormierung die lokale Steifigkeit um etwa
Faktor `5.66`. Deshalb ist der naechste faire Kerneltest nicht bloss
`matched_deposition`, sondern eine curvature-renormalized matched condition.

Zero-Mean- und lokale-Kruemmungs-Constraint:

Fuer den unnormalisierten Double-Gaussian-Kernel

```text
K(r) = A_rep exp(-r^2/(2 L_rep^2)) - A_att exp(-r^2/(2 L_att^2))
```

setze `q=L_att/L_rep>1` und `a=A_att/A_rep`. Dann ist `int K=0`
aequivalent zu

```text
a_zero = q^(-d).
```

Lokale einwaerts gerichtete lineare Rueckstellung um eine Punktdeposition
verlangt dagegen

```text
chi = a/q^2 > 1, also a > q^2.
```

Fuer jedes `q>1` und `d>=1` gilt `q^(-d)<1<q^2`. Globale Neutralitaet und
lokale Rueckstellung liegen fuer diese zweiskalige Reihenfolge deshalb in
disjunkten Parameterregionen. Insbesondere sind die kompakten q=3-Kandidaten
`A_att=20..35` nicht annaehend zero mean: Das integrierte Attraktions-/
Repulsionsverhaeltnis ist `a q^d`, also in d=3 bereits `540..945`.
Das ist ein exakter Kernel-Constraint, aber noch kein Knotensatz.

Eine minimale neutrale Erweiterung ist ein dritter, breiter positiver Anteil:

```text
K_3 = A_rep G(L_rep) - A_att G(L_att) + A_comp G(L_comp),
A_comp = (A_att L_att^d - A_rep L_rep^d) / L_comp^d.
```

Er nullt das Integral exakt. Sein lokaler Kruemmungsbeitrag ist
`-A_comp/L_comp^2` und kann fuer `L_comp >> L_att` klein bleiben. Der
kontrollierte `N=1M`-Test mit `q in {2,3,4}` bei festem `chi=35/9` zeigt
seedweise nur relative KPI-Spannen bis `1.65e-8`; zugleich ist
`R_mem/sigma_rep <=2e-4`. Der kompakte Ast sieht damit nur die lokale
Taylor-Kruemmung und identifiziert die zwei nominalen Breiten nicht getrennt.
Ein weiterer freier Zweiskalen-Sigma-Sweep ist in diesem Regime nicht
informativ. Der anschliessende breite Drei-Skalen-Pilot bei `q=3`,
`L_comp/L_rep=10`, `N=1M` und Seeds `1..5` nullt das Integral exakt und
erzeugt einen aeusseren Kraftwechsel bei `r/sigma_rep ~=10.91`. Ohne
Kruemmungsmatching aendern sich die lokalen KPIs seedgepaart um hoechstens
`0.238%`; mit exaktem Kruemmungsmatching um hoechstens `2.2e-11` relativ.
Damit sind globales Nullintegral und der bestehende kompakte lokale Ast
miteinander vertraeglich, aber noch keine physikalische Neutralitaet gezeigt.
Reports:
`reports/kernels/compensation/kernel_compensation_constraint_audit_2026-07-18.md`,
`reports/kernels/compensation/fixed_curvature_sigma_pilot_d3_N1M_2026-07-18.md`
und
`reports/kernels/compensation/three_scale_zero_mean_pilot_d3_N1M_2026-07-18.md`.

## Spektrale rho-Reprasentation und dynamische Felderweiterung

Auf einer periodischen 1D-Box der Laenge `L_box` kann dasselbe skalare Memory
mit endlich vielen Fourierkoeffizienten gespeichert werden. Fuer
`k_m=2 pi m/L_box` lautet das normierte Update

```text
rho_hat_(n+1,m) = (1-lambda) rho_hat_(n,m)
                  + lambda M0/L_box exp(-i k_m x_(n+1)).
```

Dies ist keine neue Physik, sondern die Galerkin-Reprasentation der bisherigen
exponentiell gewichteten Punktspur. Sie ist weiterhin ein expliziter
Markov-Zustand und kontrahiert bei gemeinsamem sichtbarem Pfad modeweise mit
`1-lambda`. `K_hat(0)=0` folgt aus `int K=0`, entfernt aber nur den konstanten
Potentialmodus. Da der sichtbare Update den Gradienten liest, ist dieser
Nullmodus ohnehin kraftfrei; Nullintegral ist keine Energieerhaltung.

Die erste echte Modellerweiterung fuegt einen Heat-Semigroup-Schritt hinzu:

```text
rho_hat_(n+1,m) = exp(-nu k_m^2)
                  [(1-lambda) rho_hat_(n,m)
                   + lambda M0/L_box exp(-i k_m x_(n+1))].
```

Die 1D-Diffusions-RMS-Laenge ueber eine Memory-Zeit `lambda^-1` ist
`sqrt(2 nu/lambda)`. `nu=0` stellt das alte Modell bitgenau wieder her.
Positive `nu` macht das Vergessen modeabhaengig und ist deshalb ein neuer
Feldmechanismus, keine blosse Umparametrisierung. Er ist weiterhin diffusiv
und besitzt keine harte endliche Signalgeschwindigkeit.

Der Ressourcenpilot behaelt 64 positive Moden plus Nullmode, also 1040 Bytes
pro komplexem Feldzustand. Fuer die geglaettete Kraft sind 32, 64 und 128
Moden im getesteten Slice numerisch konvergent. Eine Delta-Deposition besitzt
bei endlicher Fouriertrunkierung dagegen Gibbs-Loben und ist punktweise nicht
positiv. Dies ist ein Rekonstruktionsartefakt; fuer ein echtes positives
Bandfeld sind finite Depositionsbreite, Positivitaetsprojektion oder ein
lokaler konservativer Diskretisierer getrennte Modellentscheidungen.

Numerisch skaliert der relative Radius fuer `epsilon=1e-8..1e-4` exakt linear
mit epsilon. Der erste kontrollierte Feldpilot zeigt bei wachsender
Diffusionslaenge eine glatte Abschwaechung der Rueckstellung, aber keinen neuen
Ast oder Modus. Dieser Pilot motivierte die nachfolgende Low-Mode-/AR-
Diagnostik; fuer sich allein traegt er keinen Metastabilitaets- oder
Propagationsclaim.
Die Diagnostik verwendet einen translationsinvarianten reduzierten Zustand
aus relativer Position, aktueller Kraft, phasenausgerichteten niedrigen
Fourierkoeffizienten und symmetrischen/antisymmetrischen Realraum-Stuetzstellen.
Die Realraumwerte sind keine zweite Dynamik, sondern eine Rekonstruktion
derselben `rho_hat`. Zusaetzlich wird die Kraft direkt aus den letzten 2000
Positionen mit ihrem exponentiellen Gewicht berechnet. Der beobachtete maximale
Fehler `1.87e-9` entspricht der Ordnung des ausgelassenen Schwanzes
`(1-lambda)^2000`.

Leave-one-seed-out-AR-Modelle schlagen shuffled futures und in den
interpretierbaren Lags auch Persistence. Zwischen 1000 und 10,000 Memory-
Zeiten bleiben zwei aggregierte aktive Raten innerhalb des 10-Prozent-Gates.
Das stuetzt Vorhersagbarkeit des reduzierten Zustands, aber noch nicht die
Identitaet eines einzelnen dynamischen Eigenmodus.

Der Eigenvektor-/Segmentaudit verwendet reproduzierbar gesetzte stochastische
Seeds, nicht eine deterministische Modellgleichung. So koennen dieselben
Traces ohne Archivierungsartefakt in nichtueberlappende Zeitsegmente zerlegt
und Feature-Subraeume verglichen werden. Der aktive reelle Kandidat scheitert
dem kombinierten Match-/Ratenstabilitaetsgate. Komplexe aktive und `eta=0`-
Referenzsubraeume ueberlappen bei 0.2 und 1.0 Memory-Zeiten mit mehr als
0.9999. Der Feldzweig besitzt damit eine reproduzierbare reduzierte
Relaxationsbeschreibung, aber keinen identifizierten internen Phasen-,
Wellen- oder einzelnen Relaxationseigenmodus.

## Dimensionless Attractive-Only Reduction

The current core audit shows that the narrow positive Gaussian is not an
active repulsive core in the compact small-noise branch. For the long-run
reference (A_rep,A_att)=(1,35), sigma_rep=1 and sigma_att=3, removing A_rep
and setting A_att=26 preserves the point-deposit restoring curvature exactly.
The full seed-matched family comparison makes the mapping explicit. For
`sigma_rep=1`, `sigma_att=3`, and `A_rep=1`, local-curvature matching gives
exactly `A_eff=A_att-9`. Across 45 seed-matched pairs with `A_eff>=1`, the six
reported KPIs differ by at most `6.4e-6` relative and their effective-axis
curves collapse. This establishes dynamical equivalence only for the sampled
regime, not for trajectories that explore the kernel scales. The historical
drift flip near raw `A_att=7.9` used `epsilon=0.03` and a different force-
direction observable; it is not a universal attractive-only threshold near
six.

For the attractive-only model choose the reference length L=sigma_att and
define

    y = x/L,
    delta = epsilon/L,
    q = 1-lambda,
    g = eta M0 A_att/L^2.

At fixed lambda and kernel shape, the trajectory depends on eta, M0 and A_att
through their product. These three raw parameters are therefore structurally
non-identifiable from a one-kernel trajectory alone. In memory-time units the
corresponding drift and diffusion controls are g/lambda and
delta^2/(2 lambda).

In the Taylor regime the normalized memory center m_n gives the relative
coordinate r_n=x_n-m_n. The ideal untruncated scalar reduction is

    r_(n+1) = q(1-g) r_n + q epsilon xi_n,

with real relative eigenvalue q(1-g) and stationary Euclidean RMS radius

    R_linear = sqrt(d) q epsilon / sqrt(1-q^2(1-g)^2).

For the A_att=0..40 screening slice, g=A_att/60. The entire scan is below the
monotone/alternating boundary A_att=60. For A_att>=5 the measured dynamic
radius follows R_linear with median relative error 0.94 percent and maximum
error 3.44 percent. The raw KPIs vary smoothly; no finite-A phase transition
is detected. The A_att=0 null is bitwise identical to eta=0.

This changes the interpretation of the compact branch. It is robust evidence
for a controlled co-moving scalar relaxation cloud, but currently little
evidence for nonlinear metastability. In d=3 an isotropic linear Gaussian
cloud naturally has covariance participation dimension near three. The
observed D_mem near three is therefore not evidence that three dimensions
emerge; the ambient-dimension results, where D_mem grows with d, are consistent
with this guardrail.

The controlled fixed-g gate has now targeted `R_linear/L={0.03,0.1,0.3}` for
`A_att=26`, using `epsilon={0.0434,0.1447,0.4341}`, five paired seeds and
eta-zero controls. The measured endpoint radius grows `6.2%` more than the
linear prediction in the same direction for all seeds. This is comparable to
the `4.4%` loss of local Gaussian curvature at `R/L=0.3`; D_mem changes only
`0.0059` and roundness only `0.0106` in median. The pre-registered composite
rule remains `inconclusive` because KnotScore and fixed-voxel residence change.
A separate scale audit shows that those voxels range from `5.56 R` to `0.56 R`
at their finest scale, while co-moving residence is saturated for active and
eta-zero paths alike. The defensible reading is a weak smooth finite-kernel
correction without an isolated shape transition or metastable scalar branch.

A Gaussian convolution still has an exact local heat-semigroup generator in
an auxiliary smoothing coordinate s, with s=L^2/(2D). This is a mathematical
kernel representation, not physical update time. A physical local mediator,

    tau_phi partial_t phi = D_phi Delta phi - mu_phi phi + g_phi rho,

has stationary transfer g_phi/(mu_phi+D_phi k^2), agrees with the Gaussian
only at low wave number, and has a Yukawa/Helmholtz rather than Gaussian Green
kernel. It is therefore a genuine model extension. The field must be included
in the augmented Markov state and its source sign fixed for attraction before
it can replace K. A diffusive mediator also does not provide a hard finite
propagation speed; a hyperbolic model remains a later, separately tested step.

Reports: reports/kernels/core/kernel_core_audit_2026-07-18.md,
reports/kernels/core/attractive_only_regime_scan_d3_N300k_2026-07-18.md,
reports/kernels/core/kernel_family_comparison_d3_N300k_2026-07-19.md,
reports/long_runs/scalar_hardening/linear_long_run_reconciliation_2026-07-19.md,
reports/kernels/nonlinearity/fixed_g_RL_d3_N300k_A26_2026-07-19.md,
reports/kernels/nonlinearity/fixed_g_scale_reconciliation_d3_N300k_A26_2026-07-19.md
and reports/kernels/field/field_equation_bridge_2026-07-18.md.

## Self- and Cross-Interaction Channels

The current scalar memory is non-negative. The historical long-run and
frozen-source reference used the same two-scale kernel for self-confinement and
cross interaction, while the attractive-only reduction is now the simpler
scalar self-baseline pending the nonlinear-radius gate. Either unsigned scalar
choice gives every source the same sign. In the canonical `A_rep=1`, `A_att=35`,
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

This minimal channel is now implemented with the compensated cross-kernel and
tested on the checksum-validated `N=100M` checkpoints in `d=3` and `d=10`.
Zero-label and free branches agree bitwise, equal label products produce
identical paths, and changing `s_i s_j` reverses the pulse response. The active
self-coupled target responds at pulse end by only about `0.00136 R_mem`,
compared with the calibrated `eta=0` response of `0.03 R_mem`; radius
disturbances remain below `4.5e-5`. This is an architecture result from one
checkpoint per dimension. The labels are externally assigned and are neither
emergent nor identified with charge.

The self and cross kernels need not have the same resolution. For the current
`N=100M` checkpoints, the memory radius is only order `1e-4 sigma_rep`, so
the existing cross-kernel sees a point monopole and cannot read internal knot
shape. A narrower or moment-coupled cross-observable is a separate model choice.

A one-way dynamic-source test is the necessary intermediate step between a
frozen source and reciprocal coupling. It keeps the source autonomous while
four target paths share the same future noise: dynamic source, frozen source,
free target, and an eta-zero target. Relative centre velocity is decomposed
into radial and tangential parts, and orientation is measured by the
antisymmetric tensor `r wedge v`; amplitude without control-separated
orientation persistence is not an orbit or spin.

For the current scalar checkpoint, autonomous source motion is tiny on the
cross-kernel scale. At alpha=0.01 the 200-memory-time continuation contains
20,000 updates and begins from N=100 million, but age alone is not treated as
stationarity evidence. A 50-memory-time pre-launch window now tests radius and
the trace-normalized shape-tensor eigenvalue spectrum; all five future-noise
continuations pass the provisional eligibility gate.

An imposed point launch shifts the source relative to its unlaunched control
and remains radius-bounded by a factor below two, but three of five seeds fail
the q95 spectral-shape coherence threshold. The target response remains
sub-threshold. Thus the result is bounded but not continuously shape-coherent,
not literal destruction and not rigid shape preservation. Reciprocal coupling
is not yet identifiable: the next mechanism must transport a source with
bounded coherent shape dynamics, or introduce a local/retarded field channel
whose delay is itself measurable.

A sustained one-way age audit from N=100 million to N=103 million sharpens
this negative result. Across five future-noise continuations, the target
centre response accumulates almost linearly while radius and rotation-
invariant shape remain indistinguishable from the paired free control. The
apparent absolute shape reversal is shared with that control: dynamic and
free shape dimensions correlate at 0.999953, and the paired-difference span
is only 0.142 percent of the absolute dynamic span. This supports scalar
far-field translation, not a slowly forming interaction-specific knot type
or a cross-induced half oscillation.

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
