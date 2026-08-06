# Theoretical Context

Stand: 2026-08-04.

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

### Wie das skalare Gedaechtnis wirkt

Im urspruenglichen Modell besitzt `rho` keine eigenstaendige raeumliche
Selbstwechselwirkung. Direkt wirken nur Vergessen, neue Deposition und, in der
spektralen Erweiterung, eine lineare Glaettung:

```text
rho_n -> q rho_n + beta G(.-x_(n+1))
rho_hat_k -> exp(-nu k^2)[q rho_hat_k + beta G_hat_k exp(-i k x_(n+1))].
```

Die nichttriviale Formrueckkopplung ist daher durch `x` vermittelt:

```text
rho_n -> grad(K*rho_n)(x_n) -> x_(n+1) -> neue Deposition -> rho_(n+1).
```

Ohne Readout-Rueckkopplung (`eta=0`) bleibt ein getriebener linearer
Memory-Filter. Fuer eine rohe Fouriermode
`p_k=exp(-i k x_n)` gilt bei zentrierten Gauss-Inkrementen exakt

```text
E[p_(n+1) | p_n] = a_k p_n,
a_k = exp(-epsilon^2 k^2/2),
q_k = (1-lambda) exp(-nu k^2).
```

Der gemeinsame reelle Zustandsblock aus Real-/Imaginaerteil von `p_k` und
`rho_hat_k` hat nur die reellen Eigenwerte `a_k` und `q_k`, jeweils doppelt.
Subsampling potenziert diesen Block und erzeugt keine komplexe Mode. Komplexe
AR-Paare in mitbewegten, phasenausgerichteten Features koennen dagegen durch
die nichtlineare Koordinatenwahl, Projektion und endliche Fits entstehen. Der
N=1M-Nullaudit findet weder gepoolt noch seedweise komplexe Rohmoden; nur
`27/375` kurze, schlecht konditionierte Segmentfits lecken sehr kleine
Komplexanteile. Report:
`reports/memory/eta_zero_raw_mode_null_audit_2026-07-31.md`.

Die verfuegbaren Observablen muessen nach ihrer Abhaengigkeit getrennt werden:

| Ebene | Beispiele | Aussage |
| --- | --- | --- |
| direkt aus `rho` | Gesamtmasse, Schwerpunkt, Kovarianz-/Shape-Tensor, Radius, Anisotropie, Participation-Dimension, Fourierleistung/-phase, Autokorrelation | Zustand und Relaxation des Gedaechtnisses |
| Readout aus `rho` | `Phi=K*rho`, Kraft `-grad Phi(x)`, lokale Hessian-/OU-Skala | Wirkung des gespeicherten Feldes am sichtbaren Zustand |
| pfadvermittelt | Residence, `D_occ`, `D_cov`, Center-Drift, Drehimpuls- und Spin-Proxies | Eigenschaften der von `rho` beeinflussten Trajektorie; nicht intrinsisch `rho` |
| aktives Feld | Spektrum, Peakbreite, Feldenergie, PDE-Rest, Source-Field-Phase, Saettigung | zusaetzliche Observablen erst nach Einfuehrung eigener Felddynamik |

Damit lautet die knappe Antwort: Im Minimalmodell wirkt die Form von `rho`
auf sich selbst nur ueber `x`; Massenrelaxation und optionale lineare Glaettung
sind direkte, aber nicht selbstorganisierende `rho`-Dynamik. Erst die aktive
Felderweiterung fuegt echte Feld-auf-Feld-Terme hinzu.

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

Praezise kann man jedoch den gesamten Readkernel in einen signierten
Feldzustand verschieben:

```text
phi_n = K*rho_n,
phi_(n+1) = q phi_n + beta (K*G)(.-x_(n+1)).
```

Der Readoperator ist dann die Faltungsidentitaet `delta`, sodass `Phi=phi`.
Die konstante Funktion `K=1` ist nicht die Identitaet: Sie liefert nur
`Phi=int rho`, daher `grad Phi=0`. Die kollabierte Darstellung ist bei
linearem translationsinvariantem `K` exakt aequivalent, aber `phi` ist im
Allgemeinen signiert und keine nichtnegative Occupancy-Dichte. Eigene
Felddynamik entsteht erst, wenn der Update von `phi` weitere lokale Operatoren
oder Nichtlinearitaeten enthaelt.

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

Eine einparametrige abklingende Zero-Mean-Vervollstaendigung derselben lokalen
Taylor-Kruemmung ist der Laplacian-of-Gaussian-Kernel. Mit `u=r/L` gilt

```text
K_LoG(r) = B (u^2-d) exp(-u^2/2),
B = kappa L^2/(d+2).
```

Er besitzt exakt `int K_LoG dx=0` und `Hess K_LoG(0)=kappa I`. Fuer die
bisherige q=3-Referenz in d=3 ist `kappa=26/9` und bei `L=3` daher
`A_eff=kappa L^2=26`, `B=26/5=5.2` und die zentrale Tiefe `d B=15.6`.
Diese amplitudenartigen Zahlen haengen von der LoG-Normierung ab. Der
Volumenfaktor `q^d=27` und der rohe Wert `36=27+q^2` entstehen nur, wenn man
zusaetzlich und bislang unbegruendet `A_eff=q^d` setzt; die zweiskalige
Zero-Mean-Bedingung selbst verlangt umgekehrt `A_att=q^-d=1/27`.

Bei gleicher linearer Kruemmung unterscheiden sich die dimensionslosen ersten
nichtlinearen Kraftkoeffizienten bereits: `(1,35)` liefert `-23/26`, der
gematchte Ein-Kernel `1/2` und LoG in d=3 `7/10`. Der kompakte Ast liegt jedoch
bei `R_mem/L=6.47e-5` und kann diese Terme nicht identifizieren. LoG ist daher
eine feste analytische Nullfamilie, keine Herleitung der bisherigen Amplituden
und derzeit kein Anlass fuer einen weiteren blinden Lauf. Report:
`reports/kernels/core/log_taylor_kernel_audit_2026-07-28.md`.

## Lokale Feldoperatorentwicklung statt freier Kernelwahl

Unter Translation, `O(d)`-Isotropie, raeumlicher Paritaet und einem lokalen
skalaren Markov-Feld kann die lineare Antwort systematisch in Potenzen von
`-Delta` entwickelt werden. Eine bewusst eingeschraenkte Trunkierung lautet

```text
tau d_t phi = -c0 phi + c2 Delta phi - c4 Delta^2 phi
              - v phi^2 - u phi^3 + s0 rho - s2 Delta rho,
H(k,0) = (s0+s2 k^2)/(c0+c2 k^2+c4 k^4).
```

Dies ist keine vollstaendige EFT-Basis. Hoehere Quellderivate, gemischte
Feld-Gradient-Nichtlinearitaeten und komponentenuebergreifende Felder bleiben
ausgeschlossen, bis eine Observable sie verlangt. Raeumliche Paritaet
verbietet `phi^2` nicht; `v=0` waere eine zusaetzliche interne
Vorzeichensymmetrie.

Fuer `u=Lk` wird der normierte Gauss-Transfer bis vierter Ordnung durch
`1/(1+u^2/2+u^4/8)` reproduziert. Ein derivativer Quellkanal `s0=0` erzwingt
`H(0)=0` und damit Zero Mean. Beides sind analytische Nullfamilien, keine vom
Random Walk ausgewaehlten Koeffizienten.

Der erste neue lineare Musterbildungsmechanismus erscheint in
`P(u)=1+a2 u^2+u^4`. Fuer `a2<0` liegt das Minimum bei
`u*=sqrt(-a2/2)`; bei `a2=-2` wird es kritisch und fuer `a2<-2` linear
instabil. Ein positiver kubischer Term kann die Amplitude saettigen, garantiert
aber weder lokalisierte Knoten noch diskrete Aeste oder Quantisierung. Der
Audit zeigt ausserdem erneut: komponentenweiser Transfer `H I_d` erhaelt den
Ambient-Rang und kann kein `d=3` selektieren. Report:
`reports/kernels/field/local_field_operator_audit_2026-07-29.md`.

### Spaetere Vektor- und Chiralitaetsschiene

Eine moegliche lokale Vektorenergie lautet als Future-Work-Ansatz

```text
F[m;J] = int [
  a/2 |m|^2
  + b_L/2 (div m)^2
  + b_T/2 |grad wedge m|^2
  + c/2 |Delta m|^2
  + u/4 |m|^4
  - J dot m
  + chi m dot (curl m)
  + ...
] dx.
```

`-J dot m` ist eine gerichtete Trajektorienquelle. Bei festem `J` bricht sie
`m -> -m`, waehrend die gemeinsame Transformation `(m,J)->(-m,-J)` erhalten
bleiben kann. Fuer einen einzelnen isotropen Vektor bestehen lokale
potentialartige Invarianten ohne Ableitungen aus Funktionen von `|m|^2`;
Ableitungsinvarianten sind deutlich zahlreicher.

`chi=0` ist die paritaetssymmetrische Null. Der Term
`m dot (curl m)` ist jedoch in dieser Form spezifisch fuer einen orientierten
dreidimensionalen Raum. Dimensionsallgemein ist `grad wedge m` eine
antisymmetrische Zweiform; eine chirale Kontraktion braucht zusaetzliche
Dimensions- und Orientierungsstruktur. Der Chiralitaetsterm darf deshalb
nicht in einen Test eingehen, der erst `d=3` selektieren soll.

Eine gespeicherte Punkttrajektorie ist zunaechst eine diskrete Weltlinie, kein
dynamischer String mit Weltflaeche, Spannung und Reparametrisierungsinvarianz.
Stringartige Linienfehler koennten spaeter als topologische Defekte eines
Vektor- oder komplexen Feldes auftreten. Das oeffnet Methoden aus String- und
Defekttheorie, liefert aber weder Quantisierung noch drei Raumdimensionen als
Abkuerzung.

Die naechste mathematische Analogie ist daher vorerst nicht die fundamentale
Stringquantisierung, sondern ein feldtheoretischer Linienfehler wie der
[Nielsen-Olesen-Vortex](https://www.infomall.org/sites/dsc/jpac/QCDRef/1970s/Vortex-line%20models%20for%20dual%20strings%20-%20Nielsen%2C%20Olesen%20-%201973.pdf).
Polyakovs Weltflaechenformulierung setzt zusaetzliche Symmetrien voraus und
liefert fuer den bosonischen String die kritische Dimension 26, nicht drei
([Polyakov 1981](https://www.sciencedirect.com/science/article/pii/0370269381907437)).
Auch Stringfeldtheorie, etwa in Wittens kubischer offener Theorie, beginnt mit
einem bereits quantisierten Stringzustandsraum
([Witten 1986](https://inspirehep.net/literature/220076)). Sie kann spaeter
Methoden fuer Defekte, Moden und Wechselwirkungen liefern, ersetzt aber nicht
den hier noch fehlenden Nachweis von Feldordnung, Quantisierung oder
Dimensionsselektion.

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

For the one-dimensional impulse Green function of the relaxation-diffusion
law,

```text
G(r,t) proportional to t^(-1/2) exp[-r^2/(4 D_phi t)-mu_phi t],
```

the peak solves

```text
t_peak = [sqrt(1 + 4 mu_phi r^2/D_phi) - 1]/(4 mu_phi).
```

Thus `t_peak proportional to r^2` is only the weak-decay/near-field limit.
At large `r/sqrt(D_phi/mu_phi)`, even the diffusive peak crosses toward linear
distance scaling while the field still has instantaneous continuum support.
Peak-lag scaling alone therefore cannot establish a finite causal front. A
Telegraph model must instead be tested through its onset/front and resolution
behavior, not merely by fitting a linear peak lag.

The fixed-calibration local-mediator gate now implements both laws on a 1D
source-target axis while the knot states remain in the supplied d=3 ambient
space. Both inserted architectures pass all five complete holdout pairs and
their preregistered lag, resolution, flip, and shape gates. This is a
model-conditional pipeline result: each propagation behavior is generated by
the corresponding equation. It neither selects a physical mediator nor three
dimensions. The next useful question is input identifiability: whether an
autonomous oriented source has controlled spectral power where

```text
H_D(k,omega) = 1/(D k^2 + mu - i omega)
H_T(k,omega) = 1/(c^2 k^2 + omega_0^2 - omega^2 - 2 i gamma omega)
```

differ sufficiently in magnitude or phase. Without such source bandwidth, a
dynamic comparison cannot identify the mechanisms.

The preregistered identifiability audit does not assign an arbitrary
`k=1/r`. It computes the exact discrete finite-grid impulse response of both
frozen update laws at every inherited source-target distance, Fourier-
transforms those readouts, and normalizes each model-distance pair only by its
finite-horizon DC gain. For source-segment power `S_j(omega)` and normalized
complex responses `H_D`, `H_T`, its primary contrast is

```text
C_j^2 = sum_omega S_j |H_D-H_T|^2
        / sum_omega S_j (|H_D|^2+|H_T|^2)/2.
```

This is an input-eligibility statistic, not a likelihood ratio and not a
field-law estimator. A broadband stochastic source may make two deliberately
different transfer rules easy to distinguish even when no coherent mode is
present. The persistent carrier and normalized one-step direction are therefore
reported side by side; similar contrast would not validate the added
persistent state.

Nor does a field create a dimension-selection mechanism by itself. A local
field can be evolved in any supplied dimension, and the current mediator is a
one-dimensional relational channel. Evidence for three-dimensional selection
would require the same law and absolute dimensionless parameters across
ambient dimensions, followed by reproducible convergence of an external
response or slow-mode rank to three and suppression of the additional
directions. Running the field on a 3D grid would assume that conclusion.

The canonical six-source audit passes its preregistered eligibility thresholds:
minimum weighted complex contrast `1.064`, minimum distinguishable output-power
fraction `0.9969`, and maximum two-segment drift `0.1568`. This high separation
is not a coherent-mode result. The two deliberately different transfer rules
separate over nearly all powered frequencies, and persistent/one-step contrast
ratios span only `0.951..1.008` (median `0.991`). Thus the source can expose
different model predictions, but the audit neither validates persistent vector
memory nor selects a mediator law.

The opened dynamic holdout drives each ambient vector component through an
independent copy of the same relational mediator. This does not add spatial
dimensions to the transport grid; it is the linear vector extension of the
scalar channel. With paired active, sign-flipped and off target centers
`c_+(t), c_-(t), c_0(t)`, the primary post-settling response is

```text
R_rms = sqrt(mean_t ||c_+(t)-c_0(t)||^2) / R_target,
E_odd = rms[(c_+-c_0)+(c_--c_0)]
        / rms[(c_+-c_0)-(c_--c_0)].
```

This replaces an endpoint cosine, which becomes ill-conditioned when a
zero-mean source happens to end near zero response. The dynamic separation of
two model response traces `y_D,y_T` is

```text
Delta_DT = rms(y_D-y_T)
           / sqrt((rms(y_D)^2+rms(y_T)^2)/2).
```

The pulse-calibrated couplings, grid and mediator parameters remain fixed.
Response magnitude, oddness, source/target shape bounds, distance attenuation
and `Delta_DT` can falsify an architecture. They cannot select a physical law
without an independently observed target response.

The canonical dynamic gate is negative at the preregistered discrimination
stage. Both mediator branches pass response magnitude, oddness, shape and
attenuation for all six cyclic source-target pairs. The requirement that
`Delta_DT >= 0.25` at every distance holds for only four of six pairs, rather
than five. At the nearest distance `2.5 R_pair`, the minimum separation is
`0.1874`; at `5` and `10 R_pair`, all six pairs pass. This does not reject the
numerical viability of either inserted architecture. It rejects the stronger
claim that the present autonomous-source/target observable robustly selects
between them without retuning.

The same construction gives a structural null for ambient dimension
selection. For either component-wise vector mediator, Fourier transformation
in time and evaluation at a relational readout position `r` gives

```text
a_hat(r,omega) = H(r,omega) I_d s_hat(omega).
```

Consequently its ambient spectral covariance is

```text
S_a(r,omega) = |H(r,omega)|^2 S_s(omega),
rank S_a = rank S_s                         when H != 0.
```

Thus a full-rank isotropic source remains full-rank in the supplied ambient
space. The rule is `O(d)`-equivariant and contains neither a preferred
three-dimensional subspace nor a rank-three instability. A nonlinear target
may distort or transiently reduce an observed covariance rank, but the current
law gives no reason for that rank to be exactly three, seed-stable and
ambient-independent. Field formation and three-dimensional selection could
coincide only in a future model whose cross-component dynamics actually
suppresses additional directions; a field alone is insufficient.

Reports: reports/kernels/core/kernel_core_audit_2026-07-18.md,
reports/kernels/core/attractive_only_regime_scan_d3_N300k_2026-07-18.md,
reports/kernels/core/kernel_family_comparison_d3_N300k_2026-07-19.md,
reports/long_runs/scalar_hardening/linear_long_run_reconciliation_2026-07-19.md,
reports/kernels/nonlinearity/fixed_g_RL_d3_N300k_A26_2026-07-19.md,
reports/kernels/nonlinearity/fixed_g_scale_reconciliation_d3_N300k_A26_2026-07-19.md,
reports/kernels/field/field_equation_bridge_2026-07-18.md,
reports/response/local_oriented_mediator_gate_2026-07-28.md,
reports/response/oriented_source_mediator_identifiability_2026-07-28.md and
reports/response/dynamic_common_source_mediator_gate_2026-07-28.md.

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

For two synchronously and reciprocally coupled scalar memories, the local
relative-coordinate reduction is

```text
A_- = [[1-g-c,           g-c],
       [lambda(1-g-c), q+lambda(g-c)]],  q=1-lambda.
```

A real 2 x 2 matrix with a non-real conjugate eigenpair is real-similar to
`a E+b J`, `J=[[0,-1],[1,0]]`; `A_-` need not literally have this entry form
in the physical `(x_-,m_-)` coordinates. Its trace and determinant are

```text
T = 2-lambda-q g-(1+lambda)c,
D = q(1-g-c).
```

A stable complex cross-gain interval exists only for
`g < lambda/(1+lambda)` and requires `c>g` inside that interval. At
`lambda=0.01`, the compact baseline has finite-horizon `g=0.432291`, far
above the `0.009901` threshold. Increasing lambda would enlarge the analytic
existence region, but that is a new memory-timescale experiment, not an
explanation of the fixed-lambda result.

The registered direct complete-state reconciliation at `c=0.02` agrees with
this prediction: all 60 post-transient segment fits are real. The channel is
dynamically relevant, holding final centre separation to `0.31..0.88 R`
versus `2.78..9.21 R` without it, while preserving shape in 5/5 paths.

A second preregistered reconciliation passes the same cross-readout through a
fixed, statically unit-normalized Telegraph field/momentum filter. The
mediator, response, and shape gates pass 5/5, but all 80 raw segment fits are
again real. Retarded reciprocal separation `0.58..1.21 R` is larger than the
direct result, supporting delayed or weakened binding rather than an
observable `(x_-,m_-)` rotation. This remains one formation basin.

The filter input in P3.2 is still a target-specific instantaneous cross-gradient;
only the transport update is local. P3.2c therefore replaces it by emitter-only
signals. For `s=d=x-m`, the exact finite-grid channel is stable and contains a
complex pole near `omega=0.08294` per memory time, but its normalized
knot-to-knot residue is only `3.54e-5` and its relative generator shift from the
nearest one-way pole only `0.00622`. Three structure-preserving modal
reductions agree; the local step current loads the pole about one hundred times
less. This closes that scalar source-local offset/current mechanism without a
500k confirmation. The next stored-data test is one centered traceless shape
multipole, not a gain search. Vector memory remains reserved for orientation,
phase, circulation, or polarization, not introduced merely to provide a scalar
sign.

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
| `oriented_source.py` | passiv evolvierender orientierter Source-State mit One-Way-Kontrollen |
| `oriented_diagnostics.py` | gepaarte Response-, Shape-, Random-Sign- und Distanzmetriken |
| `local_mediator.py` | lokale 1D Relaxations-Diffusions- und Telegraph-Zustaende fuer Transporttests |
| `mediator_identifiability.py` | segmentierte Vektorleistung und sourcegewichteter komplexer Transferkontrast |
| `external_field_response.py` | gepaarte Target-Fortsetzung sowie Endpunkt- und dynamische RMS-/Oddness-Metriken fuer Aktiv-/Flip-/Kanal-aus-Felder |
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
- Der spaeter eingefuehrte persistente orientierte One-Way-Kanal besteht sein
  feste-Kopplungs-/Distanzgate in 6/6 unabhaengigen Paaren. Das zeigt, dass der
  kontrollgetrennte Response nicht nur aus geklonten Zustaenden oder
  seedweisem `eta_v`-Retuning stammt. Persistenz, instantanes Gauss-Readout und
  `sigma_v=2.5 R_source` sind jedoch gesetzt; insbesondere ist der gemessene
  Distanzabfall keine emergente Propagation.
- Knotenkriterium und Modenkriterium bleiben getrennt: Ein statistisch
  shape-gebundener Knoten darf begrenzt atmen oder rotieren. Zeitweilige
  harmonische Bursts in chaotischer Dynamik brauchen einen ereignisbasierten
  ModeScore mit Survival, Within-event Frequenz/Phase und Surrogatabstand,
  nicht eine nachtraeglich ausgewaehlte schoene Periode.
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
