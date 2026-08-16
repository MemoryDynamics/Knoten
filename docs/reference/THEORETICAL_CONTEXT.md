# Theoretical Context

Stand: 2026-08-16.

Diese Datei ist der kuratierte theoretische Kontext. Sie ersetzt die frueheren
Parallelseiten zur Non-Markovian Basis, Markov-Architektur und
Markov-Anforderungen.

## Modellhierarchie und harte Begriffsgrenze

Das Repository enthaelt inzwischen mehrere mathematische Modelle. Sie sind
nicht austauschbar. Insbesondere ist der inertiale Vektorfeld-Audit keine
weitere Schreibweise des Knotenkerns, sondern eine bislang ungekoppelte
konstitutive Erweiterung.

| Ebene | Zustand | Dynamik | wissenschaftlicher Status |
| --- | --- | --- | --- |
| K0: kanonischer Knotenkern | $z_n=(x_n,\rho_n)$ | stochastischer sichtbarer Update plus exponentielle Deposition | implementiertes Basismodell; Paper 0/I |
| K0-H: endliche numerische Darstellung | $z_n^{(H)}=(x_n,h_n^-)$ mit gespeicherten Punkten und Gewichten | truncierte Auswertung desselben $\rho_n$ | Rechenbackend, keine neue Physik |
| K1: passives orientiertes Memory | $(x_n,\rho_n,p_n,v_n)$ | Richtungstraeger und gerichtete Deposits; $x_n$ liest weiterhin nur $\rho_n$ | implementierter Diagnose-/One-Way-Pilot, kein Source-Selbstfeld |
| K2: inertiales aktives Vektorfeld | $(m(x,t),\pi(x,t))$ | Hamilton-artiger Austausch plus Daempfung | isolierter analytischer Vorschlag; nicht im Knotensimulator |
| K3: moegliche Kopplung | $(x,\rho,m,\pi)$ | noch nicht festgelegt | gesperrt, bis Herleitung oder Identifizierbarkeit besteht |

Ab hier bezeichnet $v_n$ ausschliesslich das passive gerichtete Memory und
$m(x,t)$ ausschliesslich den aktiven K2-Feldvorschlag. Aeltere Vektormemory-
Notizen verwendeten fuer beide den Buchstaben $m$; diese Notation ist
superseded. In der Implementierung heissen die K1-Groessen
`carrier_orientation` und `orientations`. Das K2-Feld erscheint nur in
`covariant_vector_field.py`; es ist kein Feld des `FiniteMemoryState` und
keine Variable von `SimulationConfig`.

### Variablenvertrag

| Symbol | Typ | Bedeutung | Status im Produktionspfad |
| --- | --- | --- | --- |
| $n$ | $\mathbb N_0$ | diskreter Updateindex, keine vorausgesetzte physikalische Zeit | kanonisch |
| $x_n\in\mathbb R^d$ | Vektor | sichtbare Position/Zustandsrepraesentant | kanonisch |
| $\xi_n$ | Zufallsvektor | unabhaengiges zentriertes Einheitsrauschen | kanonisch |
| $\varepsilon$ | Skalar | Rauschamplitude pro Update | kanonischer Input |
| $\rho_n(x)\geq0$ | skalares Feld/Measure | exponentiell gewichtete Occupancy-Historie | kanonisch |
| $\lambda_m$ | Skalar | vergessener Anteil pro Update | kanonischer Input; Codealias `alpha` |
| $\beta$ | Skalar | neu deponierte Masse pro Update | abgeleitet als $\lambda_mM_0$ im Paket |
| $M_0$ | Skalar | stationaere skalare Memory-Masse bei normiertem $G$ | kanonischer Input `memory_mass` |
| $G_\sigma$ | Kernel | nichtnegative lokale Deposition in $\rho$ | kanonischer Input |
| $K$ | Kernel | Readkernel des selbstinduzierten Potentials | kanonischer Input |
| $\Phi_n=K*\rho_n$ | skalares Feld | von $\rho_n$ gelesene potentielle Wirkung | abgeleitet |
| $\eta$ | Skalar | Gain der Kraft $-\nabla\Phi_n$ | kanonischer Input |
| $h_n^-$ | endliche Punktliste | truncierte Realisierung von $\rho_n$ ohne redundantes $x_n$ | Backend |
| $p_n$ | Vektor | tiefpassgefilterte Schrittrichtung | optionaler passiver Pilot |
| $v_n(x)$ | Vektorfeld | gerichtete K1-Deposits | optionaler passiver Pilot |
| $m(x,t)$ | Vektorfeld | aktiver, selbstdynamischer Feldvorschlag | nur K2-Postulat |
| $\pi(x,t)$ | Vektorfeld | unabhaengiger konjugierter Impuls zu $m$ | nur K2-Postulat |
| $I,\gamma,a,b_L,b_T,c,u$ | Skalare | Traegheit, Daempfung und aktive Feldenergiekoeffizienten | nur K2-Inputs; nicht aus K0 bestimmt |

Ein positiver K2-Strukturtest zeigt nur, dass die neu angesetzte Gleichung
einen klassischen gedaempften Oszillator enthalten kann. Er zeigt weder, dass
$(m,\pi)$ aus $(x,\rho)$ emergiert, noch Quantenmechanik: Es gibt hier keinen
Hilbertraum, keine Born-Regel, keine Kommutatoren, kein $\hbar$ und keine
hergeleitete Quantisierung.

Auch ein spaeter beobachtetes Polpaar $\mu_\pm=r e^{\pm i\theta}$ wuerde bei
Kadenz $\Delta n$ zuerst nur
$\Gamma=-\log(r)/\Delta n$, $\omega=\theta/\Delta n$ und damit
$\gamma/I=2\Gamma$, $D/I=\Gamma^2+\omega^2$ bestimmen. Die absolute Skala von
$I$, $\gamma$ und $D$ ist ohne unabhaengig normierte Response oder Energie
nicht identifizierbar.

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
`reports/memory/closure/eta_zero_raw_mode_null_audit_2026-07-31.md`.

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

In the Taylor regime the normalized scalar-memory center $\bar x_n^\rho$ gives
the relative coordinate $r_n=x_n-\bar x_n^\rho$. The ideal untruncated scalar
reduction is

    r_(n+1) = q(1-g) r_n + q epsilon xi_n,

with real relative eigenvalue q(1-g) and stationary Euclidean RMS radius

    R_linear = sqrt(d) q epsilon / sqrt(1-q^2(1-g)^2).

For the matched small-step family
$g=\chi\alpha$, $\epsilon^2=2D\alpha$ and $t=\alpha n$, the local
untruncated limit with the independently normalized additive generalized-force
port is

\[
dx=(-\chi r+f)\,dt+\sqrt{2D}\,dW,\qquad
dc=r\,dt,\qquad
dr=-(1+\chi)r\,dt+f\,dt+\sqrt{2D}\,dW.
\]

The deterministic force-to-visible-velocity transfer is

\[
{\dot X(s)\over F(s)}={s+1\over s+1+\chi}.
\]

Eliminating the center therefore gives

\[
\ddot x+(1+\chi)\dot x=\dot f+f,
\]

not a Newtonian equation $m\ddot x+\gamma\dot x=f$. The force derivative is
the port-level signature of unit high-frequency feedthrough. For a one-native-
step impulse of fixed area $J$, this architecture predicts

\[
\Delta x/J=1,\qquad
\alpha W/J^2=1,\qquad
(x_2-x_1)/(\alpha J)\longrightarrow-\chi.
\]

The storage $U=\chi r^2/2$ satisfies

\[
\dot U=f\dot x-\dot x^2-\chi\dot c^2.
\]

The stationary visible short-time MSD remains
$2Dt+O(t^2)$ rather than the ballistic $t^2$ law of a regular finite-mass
position with finite velocity variance.

The prospectively registered force/work gate at $\chi=4$ passed port
validity, exact finite-H response closure and every overdamped-memory
component on new formation seeds 11--15. At the
$\alpha=0.0025$ holdout it measured feedthrough $1.000000$, first post-pulse
velocity per impulse $-3.990101$, $\alpha W/J^2=1.000000$, and visible-MSD
slope $0.959048$. All four preregistered positive finite-inertial components
failed. The defensible conclusion is therefore negative for finite positive
mass when the visible coordinate \(x\) is the output of this canonical
additive port.

Post hoc, the low-frequency expansion

\[
{s+1\over s+5}={1\over5}+{4\over25}s+O(s^2)
\]

could match $1/(ms+\gamma)$ through first order only with
$\gamma=5$ and $m=-4$, not a positive passive mass. This does not exclude a
separately derived momentum state. Adding such a state and applying force to
it would be a genuine model extension and would insert, rather than establish,
inertia unless its closure and coefficients were independently derived.

The same augmented state has a distinct center output. Since

\[
\dot c=r,\qquad \dot r=-5r+f+\sqrt{2D}\,\xi,
\]

the center obeys

\[
\ddot c+5\dot c=f+\sqrt{2D}\,\xi,
\qquad
{\dot C(s)\over F(s)}={1\over s+5}.
\]

With the prospectively fixed center work \(W_c=\int f\,dc\), the positive
storage \(E=|r|^2/2\) satisfies

\[
\dot E=f\cdot\dot c-5|\dot c|^2.
\]

The separate seed-16--20 center-port gate passed validity, finite-H and
continuum closure and every registered positive-inertial component. At the
\(\alpha=0.0025\) holdout it inferred \(m=0.996239\) and
\(\gamma=5.002630\); the center-MSD slope was 1.972302. The resolved
pulse-width ladder reduced \(\Delta c/J\) to 0.024288 while retaining a
positive first force-off velocity of 0.878808 and finite
\(W_c/J^2=0.485756\).

This is an output reconciliation, not a reversal: \(x=c+r=c+\dot c\) remains
the overdamped mixed readout, whereas \(c\) is a positive effective inertial
readout. More generally, for \(y_a=c+a r\),

\[
{\dot Y_a(s)\over F(s)}={1+a s\over s+5},
\]

so the pure center \(a=0\) is the only affine readout in this family with no
high-frequency feedthrough. This is a useful realization criterion, but it is
post hoc and unique only within the stated affine family. In dimensional
variables,

\[
\tau\dot c=x-c,
\qquad
\dot x=-\kappa(x-c)+\mu F+\sigma\xi
\]

implies

\[
{\tau\over\mu}\ddot c
+{1+\kappa\tau\over\mu}\dot c
=F+{\sigma\over\mu}\xi.
\]

Thus the apparent mass is \(m_{\rm eff}=\tau/\mu\). Its registered value one
comes from the dimensionless choices \(\tau=\mu=1\), not from spontaneous
parameter selection. Moreover, \(c\) is currently the centroid of an
occupancy-history field with source and decay, not yet the center of a
materially conserved mass. The canonical variable contract defines
\(x\in\mathbb R^d\) as a visible position/state representative, not as a
periodic phase. A phase/center-of-mass reading and physical work \(F\,dc\)
therefore require separate operational derivations.

The smallest width contains only 20 native steps; its work is 5.4 percent
above the finite-width continuum reference. Also, \(\alpha H=12\) is fixed,
so \(H\to\infty\) along the alpha ladder is not independently the
untruncated-memory limit. The result supports a local passive center-inertial
representation and its nonlinear finite-\(H\) embedding, not an SI mass, a
material center of mass or a uniform multiple limit. The dedicated
[referee audit](https://github.com/MemoryDynamics/Knoten/blob/main/reports/project/meta/reviews/scalar_memory_center_mass_referee_audit_2026-08-16.md)
records the claim boundary and the required falsification tests.

The subsequent claim-scoped program now makes that boundary executable. The
center candidate passes its provenance freeze, but physical-port Gate A
cannot identify the existing actuator. An \(x\)-conjugate hypothesis gives
\(F\,dx=F\,dc+F\,dr\), whereas an effective
\(U_{\rm ext}(c,Q)\) transforms to the same additive \(x\)-state equation.
The frozen contract contains neither a reciprocal actuator nor the exact
finite-history boundary-work rule needed to choose between them. The
mathematical passive center port therefore survives, while physical mass
gates remain blocked. This center result has no bearing on S1: the independent
topology P0 still has no candidate.

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
reports/response/oriented/local_oriented_mediator_gate_2026-07-28.md,
reports/response/oriented/oriented_source_mediator_identifiability_2026-07-28.md and
reports/response/oriented/dynamic_common_source_mediator_gate_2026-07-28.md.

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
relative-coordinate reduction uses the scalar-memory centres
$\bar x_i^\rho$ and the half-difference variables

$$
x_- = \frac{x_1-x_2}{2},
\qquad
\bar x_-^\rho = \frac{\bar x_1^\rho-\bar x_2^\rho}{2},
\qquad
Y_-=
\begin{pmatrix}
x_-\\
\bar x_-^\rho
\end{pmatrix}.
$$

Here $Y_-$ is a reduced observable constructed from the canonical two-node
state; it is not an additional field or fit parameter. Linearizing the self
and cross potentials gives the dimensionless gain matrices

$$
G=\eta\,\nabla_x^2(K_{\rm self}*\rho_i)(x_i),
\qquad
C(R)=\eta_\times\,\nabla_x^2(K_{\rm cross}*\rho_j)(x_i),
$$

where $R=\lVert\bar x_i^\rho-\bar x_j^\rho\rVert$. The retained memory mass,
deposition/read convolution, knot shape and evaluation distance are already
contained in these Hessians. In the isotropic commuting approximation,

$$
G\simeq gI_d,
\qquad
C\simeq cI_d.
$$

Thus $g$ is the local self-return gain per update and $c$ the local reciprocal
cross-return gain per update. They are not raw kernel amplitudes. They must be
computed from the independently specified force law or measured by a local
response/Jacobian audit before fitting any oscillation. The matrix-valued
relative operator is

$$
A_-(G,C,\lambda)=
\begin{pmatrix}
I-G-C & G-C\\
\lambda(I-G-C) & (1-\lambda)I+\lambda(G-C)
\end{pmatrix},
$$

For an expansion about a reference geometry $Y_{-,\ast}$, the complete local
form is

\[
Y_{-,n+1}-Y_{-,\ast}
=A_-(Y_{-,n}-Y_{-,\ast})+b_\ast+\zeta_{-,n}+O(\|Y_--Y_{-,\ast}\|^2),
\]

where $b_\ast=F(Y_{-,\ast})-Y_{-,\ast}$ is the affine residual drift. A
normal-mode interpretation requires $b_\ast=0$, or an independently justified
co-moving reference on which that residual is removed. A complex spectrum of
$A_-$ at a nonstationary geometry is only transient local curvature.
$A_-$ is therefore derived, not a further parameter. Its scalar isotropic form
is

```text
A_- = [[1-g-c,           g-c],
       [lambda(1-g-c), q+lambda(g-c)]],  q=1-lambda.
```

The remaining quantities that affect an observed stochastic mode are:

- $\lambda$: memory relaxation per update;
- the relative-noise covariance $Q_-$; for equal amplitudes $\varepsilon$ and
  innovation correlation $\rho_\xi$,
  $\operatorname{Cov}(\zeta_x)=\varepsilon^2(1-\rho_\xi)I_d/2$ under the
  half-difference convention;
- separation $R$, orientation and knot shape through $C(R)$;
- nonlinear Hessian variation over the sampled amplitude, which controls the
  validity of the local operator.

The eigenvalues $\mu_j(A_-)$, damping, frequency and quality factor are output
observables. They are not independent tuning parameters. For anisotropic or
noncommuting $G$ and $C$, the full $2d\times2d$ operator must be used instead
of assigning one scalar pair $(g,c)$.

A real 2 x 2 matrix with a non-real conjugate eigenpair is real-similar to
`a E+b J`, `J=[[0,-1],[1,0]]`; `A_-` need not literally have this entry form
in the physical `(x_-,xbar_-^rho)` coordinates. Its trace and determinant are

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

The necessary inequality `c>g` is also a mechanism test. If one common
source/readout law with `eta_cross=eta` gives `C(R)<=G` in every relevant
direction, changing the common gain cannot create this complex branch. A
cross-enhancement, self-screening, different channel geometry or delayed
mechanism would then be an additional assumption, not a selected parameter.

For the compact point-deposit limit there is a sharper same-law obstruction.
With

\[
K(r)=A_{\rm rep}e^{-r^2/(2L_{\rm rep}^2)}
-A_{\rm att}e^{-r^2/(2L_{\rm att}^2)},
\qquad L_{\rm att}>L_{\rm rep},
\]

local self-confinement at the deposited point requires

\[
\frac{A_{\rm att}}{L_{\rm att}^2}
>
\frac{A_{\rm rep}}{L_{\rm rep}^2}.
\]

A positive radial force-zero radius exists only under the strict reverse
inequality. At that radius the radial cross curvature is positive, but the
self curvature at the origin is then negative. Hence one compact scalar
two-Gaussian law cannot simultaneously provide point-like self-confinement
and a finite pair equilibrium. Distributed/noncompact memory can invalidate
the point approximation, but that must be demonstrated rather than assumed.
For the current compact checkpoints the complete-state affine audit agrees
with the point result: no tested complex-Jacobian geometry is force balanced.

The registered direct complete-state reconciliation at `c=0.02` agrees with
this prediction: all 60 post-transient segment fits are real. The channel is
dynamically relevant, holding final centre separation to `0.31..0.88 R`
versus `2.78..9.21 R` without it, while preserving shape in 5/5 paths.

A second preregistered reconciliation passes the same cross-readout through a
fixed, statically unit-normalized Telegraph field/momentum filter. The
mediator, response, and shape gates pass 5/5, but all 80 raw segment fits are
again real. Retarded reciprocal separation `0.58..1.21 R` is larger than the
direct result, supporting delayed or weakened binding rather than an
observable `(x_-,xbar_-^rho)` rotation. This remains one formation basin.

The filter input in P3.2 is still a target-specific instantaneous cross-gradient;
only the transport update is local. P3.2c therefore replaces it by emitter-only
signals. For `s=d=x-xbar_rho`, the exact finite-grid channel is stable and contains a
complex pole near `omega=0.08294` per memory time, but its normalized
knot-to-knot residue is only `3.54e-5` and its relative generator shift from the
nearest one-way pole only `0.00622`. Three structure-preserving modal
reductions agree; the local step current loads the pole about one hundred times
less. This closes that scalar source-local offset/current mechanism without a
500k confirmation. The subsequent preregistered shape-multipole gate required a
minimal autonomous checkpoint continuation because the old traces had not
persisted the full tensor. All five baseline paths remained shape-bounded, but
neither the centered traceless tensor (`0/5`) nor its rate (`0/5`) produced a
segment-stable source candidate. The low-frequency tensor peak was stronger in
the `eta=0` control, which produced `2/5` single-path candidates. No tensor
mediator is authorized. Vector memory remains reserved for orientation, phase,
circulation, or polarization and must be formulated as an explicit model
extension with its own null limits before another mechanism run.

## Kontinuitaetsbeschraenktes Dichte-Strom-Memory

Ein durch bestehende Struktur begruendeter aktiver Erweiterungskandidat ist
kein frei gewaehltes Knotenlabel, sondern ein lokaler Memory-Strom
$\mathbf j$. Der bestehende skalare Datensatz selektiert diesen Kandidaten
jedoch nicht gegen andere Erweiterungen. Aus dem kanonischen Update folgt
zunaechst die Innovation

\[
S_n(y)=\rho_{n+1}(y)-\rho_n(y)
=\lambda_m\left[M_0G_\sigma(y-x_{n+1})-\rho_n(y)\right].
\]

Bei $\int\rho_n=M_0$ besitzt sie kein Monopol und den ersten Moment

\[
\int yS_n(y)\,dy
=\lambda_mM_0(x_{n+1}-\bar x_n^\rho).
\]

Zudem gilt exakt $\sum_{r=0}^{B-1}S_{n+r}=\rho_{n+B}-\rho_n$. Die Innovation
ist daher ein zeitlicher Coboundary: Ein beschraenktes stationaeres Memory
liefert daraus allein keine statische DC-Ladung. Endliche numerische
Memory-Trunkierung kann einen kleinen, direkt messbaren Monopolrest erzeugen;
dieser darf nicht als Physik interpretiert werden.

Die minimale lokale aktive Erweiterung lautet im Kontinuum

\[
\partial_t\rho=-\lambda_m\rho-\nabla\cdot\mathbf j+S_x,
\qquad
\partial_t\mathbf j=-\gamma_j\mathbf j-c_j^2\nabla\rho.
\]

Der Strom ist damit durch lokalen Transport orientiert, nicht durch ein
knotenspezifisches Vorzeichen oder eine vorgegebene Achse. Fuer einen
longitudinalen Fouriermodus gilt

\[
(s+\lambda_m)(s+\gamma_j)+c_j^2k^2=0,
\]

und ein komplexes Polpaar existiert genau fuer

\[
2c_jk>|\lambda_m-\gamma_j|.
\]

Diese Erweiterung ist klassisch und O(d)-kovariant. Sie fuehrt den neuen
Zustand $\mathbf j$ sowie die konstitutiven Parameter $\gamma_j,c_j$ ein; sie
ist nicht aus bisherigen skalaren Long Runs identifiziert. Der minimale Strom
traegt nur longitudinale Dichtewellen. Transversale Stroeme relaxieren, sodass
weder Spin noch Haendigkeit folgt. Vor allem ersetzt die Kontinuitaetsgleichung
nicht das P3.7b-Kraftbilanzgate: Eine Mode um eine driftende Geometrie ist noch
kein Knotenorbit. Eine gemeinsame Source-/Readout-Energie und ein Affin- oder
Limit-Cycle-Gate sind deshalb zwingend vor einer Simulation.

### Separater Gradientenmediator und Skalenwahl

Die rigorose Nachpruefung trennt diesen Ansatz von der vorherigen
Dichte-Strom-Gleichung. Der folgende `k^2`-Kanal entsteht nicht durch additive
Deposition in das kanonische $\rho$ und auch nicht automatisch aus dem
P3.8a-Strom $\mathbf j$. Er erfordert einen neuen longitudinalen Vektormediator
$\mathbf m$ mit konjugierter Geschwindigkeit $\mathbf p$:

\[
\partial_t\mathbf m=\mathbf p,
\qquad
\partial_t\mathbf p=-(\lambda_m+\gamma_p)\mathbf p
-[\lambda_m\gamma_p+(-\Delta)D(-\Delta)]\mathbf m
+g\nabla q.
\]

Hier ist $q$ eine skalare Quelldichte. Die einzige Kopplungsenergie

\[
H_{\rm int}[\mathbf m,q]
=-g\int \mathbf m(x)\cdot\nabla q(x)\,dx
\]

liefert sowohl die Gradientenquelle als auch das adjungierte reziproke
Readout. Fuer den longitudinalen konstitutiven Operator

\[
D(k)=a+b k^2+c k^4,
\qquad a,c>0,
\]

lautet die lineare eliminierte Antwort

\[
\widehat K_{\rm eff}(k,\omega)
=\frac{g^2k^2}
{(-i\omega+\lambda_m)(-i\omega+\gamma_p)+k^2D(k)}.
\]

Das Quadrat $g^2$ folgt daraus, dass derselbe adjungierte Kanal schreibt und
liest. Der Faktor $k^2$ nullt die homogene Mode exakt; ein Zero-Mean-Kernel
wird damit zur Operatorfolge und nicht zur Balance frei gesetzter
Gaussamplituden. Eine direkte skalare Kopplung ohne Gradienten ist die
Nullkontrolle und besitzt diesen Faktor nicht.

Mit

\[
\ell=(c/a)^{1/4},\quad
u=k\ell,\quad
\delta=\frac b{\sqrt{ac}},\quad
\mu=\frac{\lambda_m\gamma_p\sqrt c}{a^{3/2}},\quad
r_\gamma=\frac{\max(\lambda_m,\gamma_p)}{\min(\lambda_m,\gamma_p)}\geq1
\]

reduziert sich der statische Nenner auf

\[
P(u)=\mu+u^2+\delta u^4+u^6.
\]

Die gradientengekoppelte Antwort $u^2/P(u)$ besitzt ihr positives Maximum bei
$y_*=u_*^2$ mit

\[
2y_*^3+\delta y_*^2-\mu=0.
\]

Damit werden effektive Wellenlaenge und Schalenradien aus der Feldantwort
bestimmt, nicht als Zielwert eingesetzt. Dies ist Skalenwahl, aber noch keine
Selbstauswahl der drei dimensionslosen Operatorgruppen. Eine Simulation kann
Konstanten ohne eigene Updategleichung nicht erzeugen. Wissenschaftlich
zulaessig ist zunaechst nur deren grobgekoernte Identifikation. Mit
$y=u^2$ und
$\kappa_y=-\partial_y^2\log H(y)|_{y_*}>0$ gilt gainunabhaengig

\[
\delta=
\frac{y_*[6-\kappa_y(1+3y_*^2)]}{2(\kappa_y y_*^2-1)},
\qquad
\mu=2y_*^3+\delta y_*^2.
\]

Da die beiden Zerfallsraten nur ueber Summe und Produkt eingehen, sind ihre
Namen vertauschbar; $r_\gamma$ bezeichnet deshalb das kanonische groessere-
zu-kleinerem-Verhaeltnis. Peaklage und lokale Log-Kruemmung identifizieren
damit $(\delta,\mu)$ unter
der Modellannahme; zeitliche Daempfung/Phase am selben Peak testet
$r_\gamma$, und ein unabhaengig kalibrierter Weak-Response-Gain bestimmt die
verbleibende Amplitude. Die Werte
muessen ueber Seeds, Segmente, Aufloesungen und eine unabhaengige Paarantwort
stabil bleiben.

Der feste analytische Existenzpunkt
$(\delta,\mu,r_\gamma)=(-1.9,0.3,1)$ liegt mit
$1-\delta^2/4=0.0975>0$ noch in der positiv definiten konstitutiven Familie.
Er waehlt $u_*=1.03869$ und traegt einen stabilen komplexen zeitlichen Modus.
Die dreidimensionale Fourier-Inversion wird exakt als Summe dreier
Yukawa-Residuen berechnet und stimmt am festen Witness bis $1.81\times10^{-15}$
mit einer unabhaengigen unendlichen oszillatorischen Quadratur ueberein. Fuer
die Konvention $U_{\rm pair}=-K_{\rm eff}$ liegt die erste Energiebarriere bei
$r/\ell=3.91920$ und das erste getrennte lokale Minimum bei
$r/\ell=6.99092$.

Der nachfolgende quasistatische P3.8c-Test setzt zwei starre Kopien des
vollstaendigen `d=3`, Seed-1, `N=100M`-Memoryzustands ein. Bei $R=5\ell$
prognostiziert der bisherige kompensierte statische Kernel eine einwaertige,
der Gradientenmediator eine auswaertige Kraft. Die komplette Memory-Wolke
reproduziert die beiden Gradientenmediator-Radien innerhalb der erwarteten
Punktgrenze und erfuellt Action/Reaction sowie $F=-\partial_R E$. Das ist ein
Diskriminierbarkeitstest, keine Mechanismusselektion: $R_{\rm mem}/\ell$ ist
nur $2.12\times10^{-4}$, $\ell=\sigma_{\rm rep}$ wurde gesetzt, nur ein
Formationsseed wurde verwendet und kein Zustand fortgeschrieben.
Die primaere Paarenergie ist eine reziproke Memory-Dichte-zu-Memory-Dichte-
Kopplung und damit eine neue Cross-Architektur. Ein separat aus dem
kanonischen Sichtpunkt-zu-Fremdmemory-Readout energiesymmetrisierter Vergleich
behaelt bei $R=5\ell$ dieselben Kraftvorzeichen. Das ist wegen der extremen
Kompaktheit erwartbar und keine Gleichsetzung beider Regeln. Der gemeinsame
Amplitudenversatz von $0.2411\%$ wird durch die endliche Tail-Masse erklaert:
Im Punktlimit skalieren die beiden Definitionen wie $M_H^2$ beziehungsweise
$M_H$ mit $M_H=0.997595$.

Vor einer dynamischen Fortsetzung muss eine diskrete `(m,p)`-Regel dieselbe
Energie reproduzieren. Bei bewegter Quelle enthaelt die Bilanz neben
Mediator-Daempfung explizite Source-Arbeit. Zeitschritt-Konvergenz, Cross-off,
Action/Reaction und eine erster-Ordnung-Kontrolle sind daher Pflicht. Ein
reiner `reversible-off`-Vergleich ist im statischen Gate nicht diskriminierend,
weil verschiedene Zeitordnungen dieselbe Gleichgewichtssuszeptibilitaet haben
koennen. Weder P3.8b noch P3.8c selektiert `d=3`, Ladung, Spin oder QFT.

### Diskrete dynamische Realisierung des Gradientenmediators

P3.8d untersucht eine konkrete, aber weiterhin zusaetzliche Dynamik. Zwei
identische skalare Punktquellen liegen symmetrisch bei `+-R/2`. Nach einer
isotropen 3D-Fourierquadratur werden der longitudinale Feldzustand und seine
konjugierte Geschwindigkeit durch reelle Moden `m,p` repraesentiert. Mit der
Quellladung `B(R)` und einer positiven diagonalen Rueckstellmatrix `A` gilt

\[
\dot{\mathbf m}=\mathbf p,
\qquad
\dot{\mathbf p}=-\Gamma\mathbf p-A\mathbf m+B(R),
\qquad
\dot R=\nu\,\partial_R B(R)\cdot\mathbf m.
\]

Die gemeinsame Energie ist

\[
E(R,\mathbf m,\mathbf p)
=\frac12\|\mathbf p\|^2
+\frac12\mathbf m^T A\mathbf m
-B(R)\cdot\mathbf m,
\]

und besitzt die exakte kontinuierliche Bilanz

\[
\dot E
=-\Gamma\|\mathbf p\|^2
-\frac{\dot R^2}{\nu}
\le 0.
\]

Damit wird dem sichtbaren Zentrum keine inertiale Masse hinzugefuegt; `R`
bleibt overdamped. Die diskrete Implementierung splittet symmetrisch in
Source-/Feld-/Source-Schritte. Bei fester Quelle wird der gedaempfte lineare
Feldschritt analytisch ausgewertet. Fuer den Source-Schritt wird der skalare
diskrete Gradient

\[
\overline{\partial_R B}
=\frac{B(R_{n+1})-B(R_n)}{R_{n+1}-R_n}
\]

verwendet. Dadurch ist die diskrete Source-work-Bilanz bis zur nichtlinearen
Loesetoleranz exakt. Ein erster-Ordnung-Kontrollarm

\[
\Gamma\dot{\mathbf m}=-A\mathbf m+B(R)
\]

hat dieselbe statische Suszeptibilitaet `A^-1`, aber keinen reversiblen
konjugierten Zustand. Das ist die passende dynamische Kontrolle; ein rein
statischer Vergleich kann die Zeitordnungen nicht unterscheiden.

Am festen Existenzpunkt und ohne Parametersweep konvergieren die Starts
`R/ell=5` und `8` in beiden Zeitordnungen zum getrennten Basin nahe
`R/ell=6.99`. Die zweiter-Ordnung-Moden besitzen einen kurzen gedaempften
Overshoot; das Separationsergebnis bleibt jedoch nahe an der erster-Ordnung-
Kontrolle. Die fruehe Kraftantwort eines abrupt eingeschalteten Punktquellen-
feldes ist UV-Cutoff-sensitiv. Startet das Feld stattdessen bereits im
statischen Gleichgewicht des Anfangsabstands, bleibt das getrennte Basin
erhalten, aber die Kraftvorzeichenwechsel verschwinden. Das Ringing ist daher
kein initialisierungsunabhaengiger Paarmodus. Die Lyapunov-Bilanz verbietet fuer diese
autonome gedaempfte Reduktion einen nichtabklingenden Limit-Cycle.

P3.8d ist deshalb ein Konsistenz- und Existenzresultat fuer einen konstruierten
Mediator, keine Herleitung aus dem kanonischen `z=(x,rho)`. Insbesondere sind
`delta`, `mu`, `r_gamma`, `nu`, die Skalenidentifikation und der Zustand
`(m,p)` noch nicht durch die Knotendaten geschlossen. Eine belastbare
Fortsetzung muss diese Groessen auf kanonischen Daten und unabhaengigen
Response-Holdouts identifizieren oder den Kandidaten verwerfen; ein
Koeffizientensweep wuerde nur seine Einstellbarkeit demonstrieren.

### Was ein emergentes `(m,p)` rigoros bedeuten wuerde

Eine zulaessige Grobkoernung fuegt nicht zuerst `p` hinzu und sucht danach
passende Schwingungen. Sie beginnt mit einer vorab festgelegten Observable
`Y=Psi(x,rho)` und dem Markov-/Koopman-Operator `U` des kanonischen Zustands.
Eine Projektion auf `Y` liefert lokal eine exakte verallgemeinerte
Langevin-/Memory-Gleichung. In einer linearen resolved/unresolved-Zerlegung

\[
\begin{pmatrix}Y_{n+1}\\W_{n+1}\end{pmatrix}
=
\begin{pmatrix}A&B\\C&D\end{pmatrix}
\begin{pmatrix}Y_n\\W_n\end{pmatrix}
\]

ist die eliminierte Gleichung

\[
Y_{n+1}
=AY_n
+\sum_{j=0}^{n-1}BD^jC\,Y_{n-1-j}
+BD^nW_0.
\]

Der Kernel `K_j=BD^jC` wird damit aus der kanonischen Dynamik abgeleitet. Erst
wenn seine unabhaengig gemessene Input-Output-Antwort eine minimale
zweidimensionale, passive und reziproke Realisierung **pro registrierter
Raum-/Symmetriemode** verlangt, darf diese in Koordinaten `(m,p)` geschrieben
werden. Eine solche Realisierung ist nur bis
auf invertierbare Zustandswechsel eindeutig. Physikalisch invariant sind
Pole, Nullstellen, Residuen und die vollstaendige Transferfunktion; `m`, `p`
und ihre gemeinsame Normierung sind es nicht.

Fuer stochastische Einzelpfade kommt ein orthogonaler Fluktuations-/
Innovationsterm hinzu. Nur bei einer passenden Conditional-Expectation-
Konstruktion ist er eine Martingaldifferenz; fuer eine generische
Mori-Zwanzig-Projektion gilt das nicht automatisch. Die Blockelimination ist
fuer den vollstaendig zerlegten linearisierten Conditional-Mean-Operator
exakt; sie behauptet kein endliches deterministisches AR-Gesetz fuer jede
Trajektorie. Ebenso kann eine Projektion keinen kausalen Cross-Kanal erzeugen,
der im kanonischen Uebergangskern fehlt.
Einzelknoten-K0-Daten koennen daher hoechstens einen internen effektiven Modus
selektieren. Der P3.8d-Mediator zwischen Quellen benoetigt vor der Projektion
eine registrierte gemeinsame Feld-/Mehrquellendynamik oder bleibt eine
explizite Modellerweiterung.

`p` ist daher zunaechst nur der zweite, fuer Zukunftsvorhersage notwendige
Zustand neben `m`, nicht der Impuls des sichtbaren `x`. Erst die folgende
robuste reversible Struktur erlaubt die staerkere Bezeichnung als Phasen- oder
konjugierte Koordinate. Diese verlangt zusaetzlich eine positive gemeinsame
Speichermetrik, ein darin reproduzierbares reversibles Generatorstueck,
adjungierte Source-/Readout-Kopplung und eine geschlossene Energiebilanz auf
Holdout-Antworten. Das Passivitaetsgate muss leistungskonjugierte Ports wie
Kraft und Geschwindigkeit verwenden; Kraft und Auslenkung allein genuegen
nicht. Rang-2, komplexe Fitpole oder ein Lyapunov-Fit allein reichen nicht.

Auch zwei verschiedene reelle Relaxationspole besitzen Minimalordnung zwei
und koennen in Begleitform geschrieben werden. Das begruendet noch keinen
konjugierten Impuls. Erst ein ueber die zulaessigen Speichermetriken robuster
reversibler Kopplungsanteil rechtfertigt diese Deutung; ein stabiles komplexes
Polpaar weist zusaetzlich ein unterdaempftes Regime nach.

Bei `r` aufgeloesten Raumoden besitzt ein erster-Ordnung-Feld mindestens `r`,
ein `(m,p)`-Feld typischerweise `2r` Zustaende. Ein globaler Rang-2-Fit waere
daher noch keine Feld- oder Dispersionsidentifikation. Der fruehere uniforme
Weak-Probe prueft ausserdem die homogene `k=0`-Antwort. Diese wird im P3.8b/d-
Gradientenkanal durch den `k^2`-Zaehler exakt genullt. Fuer die
Mechanismus-Closure sind vorregistrierte lokalisierte oder zero-mean
Finite-`k`-Impulse erforderlich. Fuer das P3.8d-Polynom mit den drei
Raumkoeffizienten `a,b,c` braucht es mindestens drei Trainingskanaele und
einen unangetasteten Dispersions-Holdout. Ist das Produkt der Zerfallsraten
nicht unabhaengig festgelegt, kommt mindestens ein weiterer Kanal hinzu.

Langzeitdaten pruefen in diesem Schritt, ob Suszeptibilitaet, Pole und
Residuen mit dem Formationsalter ein Plateau erreichen. Das autonome P3.8d-
System selbst kann durch laengere Laufzeit keine zweite Zeitordnung
selektieren: Seine Lyapunov-Bilanz fuehrt erster- und zweiter-Ordnung-Arme zu
denselben stationaeren Gleichungen. Der derzeitige Quotient
`R_mem/ell=2.12e-4` bedeutet zudem, dass Fernantworten fast nur die
Punkt-/Monopolgrenze sehen. Aehnliche Kernel- und Knotenpotentiale sind dort
eine plausible Grobkoernungshypothese, aber noch keine Evidenz fuer denselben
inneren Mechanismus.

### P3.8e: kanonische Finite-`k`-Antwort

Das vorregistrierte P3.8e-Gate stoert den vollstaendigen reifen
Finite-Memory-Zustand longitudinal bei

\[
kR_{\rm mem}\in\{0.5,1,2,4,8\}.
\]

Die gepaarten Profile erfuellen `f_k(r_0)=0`, haben verschwindende gewichtete
Translation und Einheits-RMS. Damit bleiben sichtbarer Zustand, Memory-Masse,
Altersgewichte und Memory-Zentrum bei der Intervention unveraendert. Die
anschliessende Fortsetzung verwendet ausschliesslich den kanonischen
`(x,rho)`-Uebergang und common random numbers. Das feste Readout besteht aus
der longitudinalen Relativkoordinate `x-xbar_rho` sowie Real- und Imaginaerteil
der zentrierten skalaren Fouriermode.

Der erste Auswerter bildete active minus `eta=0`, mischte Memory und sichtbares
Readout im Fit und verglich freie mit "gedaempften" AR(2)-Modellen. Letztere
sind fuer stabile komplexe Pole exakt dieselbe Modellklasse. Zusaetzlich
ordnete die alte Hankelmatrix Seeds/Richtungen als separate Spaltenfamilien an,
sodass unterschiedliche Residuen kuenstlich Rang erzeugen konnten. Dieses
historische Ergebnis ist deshalb `superseded-methodologically-inconclusive`.

Die technische Reconciliation trennt active und `eta=0`, verwendet fuer alle
Ordnungen dieselben Zielzeiten, lernt Koeffizienten nur aus Real-/Imaginaerteil
der Memorymode und haelt die sichtbare Relativkoordinate als Readout zurueck.
Alle Panelreadouts bilden nun gemeinsam den Hankel-Ausgabevektor; nur
Zeitverschiebungen bilden Spalten. Die echte ungedaempfte Nebenhypothese hat
`a_2=-1`; Daempfung und Frequenz werden nur aus freien AR(2)-Polen interpretiert.

Alle technischen Kontrollen bestehen weiterhin, aber korrigiert besteht kein
`kR_mem`-Kanal das vollstaendige Gate (`0/5`, gefordert `>=4/5`). Alle
gepoolten aktiven AR(2)-Pole sind reell, AR(2) liefert keinen Holdout-Vorteil,
und der ungedaempfte Oszillator ist deutlich schlechter. Die korrigierten
Hankel-Spektren besitzen `s3/s2=0.557..0.695` statt einer isolierten Rang-2-
Struktur. Das Memory-Holdout enthaelt allerdings nur `0.2%..0.8%` seiner
skalenbalancierten Energie. Ausserdem sind die fuenf Eingangsprofile mit
medianer Gram-Kondition `15867` stark kollinear. Die korrekte Einordnung ist
deshalb `null-not-rejected-memory-holdout-limited`, nicht skalares No-go.

P3.8e ist eine gueltige State-Suszeptibilitaetsmessung, aber kein durch die
sichtbare Trajektorie erzeugter kanonischer Write-Port. P3.8f-a schliesst genau
diese technische Luecke mit einem gespiegelt gepaarten zero-net
`(+delta,-delta)`-Puls. Pro ambienter Achse existiert ein bekannter Input; das
Memory-Zentrum und die zentrierten Kanaele bei `kR={0.5,1,2,4,8}` sind
Outputs. Der P3.8e-Gramrang darf deshalb nicht als P3.8f-Kontrollierbarkeitsrang
interpretiert werden.

Alle schwachen Interventionskontrollen bestehen in 5/5 reifen N=3M-
Zustaenden. Die absolute Positionsantwort enthaelt jedoch eine globale
Translationsnullmode und ist kein interner Knotenzustand. Mit dem korrekten
Readout `x-m_rho` plus Selbstkraft bleibt die relative Antwort nur etwa
`0.12 tau_mem` oberhalb von `1e-3` ihres Peak-RMS; in den
Holdouts erreicht sie nur rund `8e-8` ihres fruehen RMS. Das Memory-Signal
selbst bleibt messbar. Somit gilt `G0=pass`, `G1=inconclusive` und
`G2/G3=blocked`. Es wurde weder eine zweite Ordnung verworfen noch `(m,p)`
identifiziert.

Eine einzige mechanistisch begruendete Port-Reparatur bleibt offen: derselbe
zero-net Rueckkick nach genau einer durch `lambda_m` gegebenen Memory-Zeit
statt im direkt folgenden Update. Diese Aenderung staerkt die Deposition ohne
Kernel-, Gain- oder Noise-Retuning. Erst ein informativer G1-Pass erlaubt den
Vergleich effektiver Modellordnungen. Andernfalls ist `(m,p)` keine emergente
Closure des kanonischen skalaren Modells; orientiertes/current Memory oder ein
gemeinsames Mehrquellenfeld waeren explizite neue Zustandsannahmen.

Die Auswertung verwendet ab P3.8f eine Abhaengigkeitshierarchie statt eines
Composite-Booleans. Experimentelle Gueltigkeit (`G0`) und Input-Output-
Identifizierbarkeit (`G1`) gehen der physikalischen Modellordnungsfrage voraus.
Ein nichtinformatives Holdout ist `inconclusive`; es darf nicht als Scheitern
eines zweiten Zustands verbucht werden. `G2` selektiert eine stabile effektive
zweite Ordnung und erlaubt ausdruecklich zwei reelle, ueberdaempfte Pole. Erst
`G3` fragt nach einem komplexen Polpaar und damit nach einem Phasenmodus.
Source-Target-Transfer und Dispersion sind nachgelagerte Zwei-Knoten-Gates.

Fuer die alten fuenf direkt geschriebenen P3.8e-Profile zeigt eine
Mittelwert-Gramian zwar
fuenf Richtungen oberhalb `1e-2` des groessten Eigenwerts. Eine Whitening-Basis
mit allen fuenf Richtungen erreicht in einzelnen Seed-/Achsenfaellen jedoch
eine Kondition von etwa `5.2e3`. Der groesste gemeinsame Prefix mit maximaler
Sample-Kondition `100` hat Rang 4 und bleibt unter `31`. Diese robuste
Rangreduktion ersetzt weder ein Signalgate noch eine Zustandsidentifikation;
sie verhindert nur die Verstaerkung einer nahezu unidentifizierbaren
Eingangsrichtung. Diese Diagnose gilt nicht fuer den einzelnen kanonischen
Trajektorieninput von P3.8f.

Unterschiedliche transiente Basinwahl durch Ueberschreiten einer Separatrix
bleibt bei zweiter Ordnung moeglich und kann mit einer festen
Anfangszustandsleiter getestet werden. Auch ein positiver Befund waere jedoch
eine Folge des angenommenen `(m,p)`-Kanals, nicht dessen Herleitung.

Eine echte Parameterselbstkonsistenz waere ein Fixpunkt zwischen gemessenen
Knotenobservablen `theta`, ihrer schwachen Suszeptibilitaet und der daraus
minimal realisierten effektiven Dynamik. Ohne einen aus `z=(x,rho)` folgenden
Rueckkanal bleibt dies eine offline bestimmte effektive Closure und keine
spontane mikroskopische Parameterauswahl.

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
| `finite_k_response.py` | zentrumserhaltende Finite-`k`-Stoerungen vollstaendiger skalarer Memory-Zustaende und zentrierte Fourier-Readouts |
| `impulse_identification.py` | gemeinsame rekursive AR-, gedaempfte zweite-Ordnungs- und Block-Hankel-Holdoutdiagnostik |
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
