# Raeumliche Nukleonreferenz

Stand: 2026-10-28. **Gekoppelter Solver synthetisch geprueft, noch kein
geloester raeumlicher AL1-Zustand.** Die
[Trennung von Referenz und Emergenz](matter_reference_contract.md) gilt
unveraendert. AL1 wird als erste reproduzierbare Constituent-Quarkreferenz
festgelegt, nicht als neue Memory-Regel oder als vollstaendige QCD.

## Zweck und gewaehlte Referenz

Gesucht ist ein gemeinsamer Vergleich fuer Nukleonenergie, raeumliche
Struktur und elektromagnetische Antwort, der an den
[Wasserstoffbenchmark](hydrogen_benchmark.md) anschliesst. Eine korrekte
Eigenwertrechnung allein identifiziert noch kein physikalisches Proton.

Fuer AL1 existieren raeumlich gekoppelte Rechnungen mittels Gaussian
Expansion Method (GEM) und eine aktuelle oeffentliche Implementierung,
DeepQuark. Als Methodenvergleich verwenden wir die CP-gerade Modellseite
von [Yamanaka und Hiyama, PRD 103, 035023 (2021), Abschnitt III und Tabelle I](https://arxiv.org/abs/2011.02531)
sowie [Wu, Meng und Zhu, PRL 136, 071901 (2026), Supplement A.1](https://arxiv.org/html/2506.20555v2#A1).
Der CP-verletzende Operator der ersten Arbeit gehoert **nicht** zu unserer
Referenz. Es wurde weder ein fremdes Trainingsprogramm gestartet noch
eine dort berichtete Nukleonenergie reproduziert.

Eine neue Gitter-QCD-Rechnung ist nicht Voraussetzung dieses
Methodenschritts. Als spaeterer physikalischer Vergleich kommen etwa die
Nukleonformfaktoren von
[Djukanovic et al., PRD 109, 094510 (2024)](https://arxiv.org/abs/2309.06590)
in Frage. Deren Resultate enthalten verbundene und unverbundene
Quarkbeitraege sowie Kontinuums-/Volumenkontrollen; ein Potentialmodell
hat diese Nachweisstaerke nicht. Diese Quellenbefunde sind keine eigenen
Simulationsergebnisse.

## Festgelegtes Eigenproblem

Wir verwenden natuerliche Einheiten $\hbar=c=1$, Laengen in
$\mathrm{GeV}^{-1}$, drei gleich schwere $u/d$-Constituent-Quarks und den
Farbsingulettsektor. Mit orthonormalen Jacobi-Koordinaten

$$
\boldsymbol\rho=(\boldsymbol r_1-\boldsymbol r_2)/\sqrt2,
\qquad
\boldsymbol\lambda=(\boldsymbol r_1+\boldsymbol r_2-2\boldsymbol r_3)/\sqrt6
$$

lautet das interne Problem

$$
H_{\rm int}=3m-\frac{\nabla_\rho^2+\nabla_\lambda^2}{2m}
+\sum_{i<j}\frac12\left[-\frac{\kappa}{r_{ij}}+b r_{ij}-\Lambda
+\frac{2\pi\kappa'}{3m^2}
\frac{e^{-r_{ij}^2/r_0^2}}{\pi^{3/2}r_0^3}
\boldsymbol\sigma_i\cdot\boldsymbol\sigma_j\right]
-\frac{C}{m^3},\qquad r_0=A m^{-B}.
$$

Der Faktor $1/2$ folgt aus
$\langle\boldsymbol\lambda_i^c\cdot\boldsymbol\lambda_j^c\rangle=-8/3$
und $-3/16$; $\boldsymbol\sigma=2\boldsymbol s$.
Die Jacobi-Koordinate $\boldsymbol\lambda$, die Farbmatrizen
$\boldsymbol\lambda^c$ und der Potentialparameter $b$ sind verschieden.
Es gibt hier keinen aeusseren Schwerpunktkaefig und keine klassische
Quarkbahn. Die stationaere Wellenfunktion ist bereits ein Quanteneingang.

| Eingabe | Wert |
| --- | --- |
| $m$ | $0.315\ \mathrm{GeV}$ |
| $\kappa$, $\kappa'$ | $0.5069$, $1.8609$ |
| $b$, $\Lambda$ | $0.1653\ \mathrm{GeV}^2$, $0.8321\ \mathrm{GeV}$ |
| $A$, $B$ | $1.6553\ \mathrm{GeV}^{B-1}$, $0.2204$ |
| $C$ | $2.02\,10^{-3}\ \mathrm{GeV}^4$ |

Die Zahlen sind aus Tabelle SM-I der genannten DeepQuark-Fassung
uebernommen, nicht an unseren Zielbenchmark angepasst. Unsere positive
$\Lambda$ steht mit Minuszeichen im Potential. Die Isospinsymmetrie
$m_u=m_d$ ohne elektromagnetische/ schwache Terme macht Proton und Neutron
hier massenentartet. Weder ihre Massendifferenz noch Betazerfall werden
damit beschrieben. Confinement und fermionische Quantenzustaende sind
eingesetzt, nicht emergiert. Die nichtrelativistische Naeherung fuer leichte
Quarks bleibt eine Modellannahme; kleine numerische Fehler kontrollieren
ihren physikalischen Fehler nicht.

## Warum ein fester Spinanteil nicht genuegt

Der bisherige Algebrarechner waehlt einen normierten, unter gemeinsamen
Spin-/Flavorpermutationen symmetrischen Nukleonzustand $\chi_N$. Ihn
einfach mit einer symmetrischen Ortsfunktion zu multiplizieren,
$\Psi=\phi(\rho,\lambda)\chi_N\chi_{\rm Farbe}$, liefert einen moeglichen
Variationsansatz, aber keinen unter diesem Hamiltonoperator abgeschlossenen
Loesungsraum.

**Eigene algebraische Ableitung:** Setze $A_a=\boldsymbol\sigma_i\cdot
\boldsymbol\sigma_j$ fuer die drei Paare, $O=\sum_a g_a A_a$ und
$P_N=|\chi_N\rangle\langle\chi_N|$. Im ausgewaehlten Zustand gelten

$$
\langle A_a\rangle=-1,\qquad
\langle A_a^2\rangle=5,\qquad
\left\langle\frac{A_aA_b+A_bA_a}{2}\right\rangle=-1\quad(a\ne b).
$$

Die erste Identitaet folgt aus Permutationssymmetrie und
$\sum_a A_a=2S^2-9/2=-3$ in $\hbar=1$-Einheiten. Fuer die zweite gilt
$A_a^2=3-2A_a$. Quadrieren der Summe ergibt die dritte. Folglich

$$
\|(1-P_N)O\chi_N\|^2
=\langle O^2\rangle-\langle O\rangle^2
=6\sum_{a=1}^3(g_a-\bar g)^2,
\qquad \bar g=\frac13\sum_a g_a.
$$

Die AL1-Koeffizienten $g_a$ haengen vom jeweiligen Paarabstand ab.
Ein ungleichseitiges Dreieck hat daher im Allgemeinen einen nichtnulligen
Rest ausserhalb dieses festen Ansatzes. Gleiche Koeffizienten bilden
eine besondere Kontrolle, keinen generischen Nachweis. Der symmetrische
Spin-$3/2$-Zustand hat fuer jedes Paar den Eigenwert $+1$ und bleibt auch
bei ungleichen Koeffizienten ein Eigenvektor von $O$.

Das begruendet einen gekoppelten Ansatz

$$
\Psi=\chi_{\rm Farbe}\sum_{s_{12},t_{12}=0,1}
\phi_{s_{12},t_{12}}(\rho,\lambda)
\chi_{s_{12};S=1/2}\xi_{t_{12};I=1/2},
$$

mit gemeinsamer Orts-/Spin-/Flavor-Permutationssymmetrie. Fuer Gesamt-
$L=0$ koennen die beiden Jacobi-Partialdrehimpulse dennoch ungleich null
sein. Ihre Kopplung und die zulaessige Paarsymmetrie muessen enthalten
sein; nur einen radialen Faktor zu verfeinern schliesst diese Luecke nicht.
Der Rest oben ist **kein** Energiebias, keine Zeitwachstumsrate und keine
Instabilitaet des Protons. Er widerlegt nur den exakten Abschluss dieses
festen Produktansatzes, nicht seine moegliche Brauchbarkeit als Naeherung.

Der neue [Operatortest](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/experiments/current/reference/nucleon_spatial_preflight.py)
prueft diese Identitaet unabhaengig mittels der vorhandenen $64\times64$-
Pauli-Matrizen. Die [archivierte Auswertung](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/nucleon_spatial_preflight_2026-10-28.json)
ergibt am **synthetischen**, nicht optimierten Dreieck
$(0,0,0),(1,0,0),(1/4,5/4,0)\ \mathrm{GeV}^{-1}$ einen Restquadratwert
$0.01226096890434217\ \mathrm{GeV}^2$, gegen analytisch
$0.012260968904342164\ \mathrm{GeV}^2$. Die gleichseitige Kontrolle und
Spin-$3/2$-Kontrolle verschwinden bis auf Rundung. 17 neue
[Softwaretests](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/tests/test_nucleon_spatial_preflight.py)
pruefen zudem Farbe, Normierung, Isospin, Rotation, Translation und
alle sechs Permutationen. Kein raeumlicher Eigenwert wurde geloest.

## Massenkonvention vor Reproduktion klaeren

Geprueft wurde der oeffentliche DeepQuark-Stand
[`0c56c3442f2b5e120d80db790d670a4f9f2edc12`](https://github.com/wlwuphy/DeepQuark/tree/0c56c3442f2b5e120d80db790d670a4f9f2edc12).
In [baryon/hi_op_.py](https://github.com/wlwuphy/DeepQuark/blob/0c56c3442f2b5e120d80db790d670a4f9f2edc12/baryon/hi_op_.py)
enthaelt `baryon_potential` Paarpotential, Ruhemasse und Confinement,
aber nicht $-C/(m_1m_2m_3)$. Auch
[config_.py](https://github.com/wlwuphy/DeepQuark/blob/0c56c3442f2b5e120d80db790d670a4f9f2edc12/config_.py)
fuehrt kein $C$; der generische Operator und
[baryon/train.py](https://github.com/wlwuphy/DeepQuark/blob/0c56c3442f2b5e120d80db790d670a4f9f2edc12/baryon/train.py)
addieren im gelesenen Ausfuehrungspfad keinen solchen Term.

Dies ist eine **statische Code-/Textabweichung**, keine Aussage, dass die
publizierten Zahlen falsch sind: Eine anderweitige Nachverarbeitung ist
damit nicht ausgeschlossen. Ein ungeaenderter Lauf dieses Pfads ist aber
ohne weitere Konventionsklaerung keine Reproduktion des angegebenen
Hamiltonoperators. Der konstante Unterschied betraegt fuer drei leichte
Quarks exakt nach den tabellierten Eingaben

$$
-C/m^3=-64.62784996420673\ \mathrm{MeV}.
$$

Eine Konstante verschiebt alle Eigenwerte desselben festen Massensektors,
aber keine Eigenfunktionen, Radien oder Energiedifferenzen. Daraus folgt
eine Kalibrierungsgrenze: Eine allein ueber einen solchen Offset passende
Protonmasse bestimmt weder die innere Groesse noch das magnetische Moment.
Der geerbte phenomenologische Offset ist kein unabhaengiger Massennachweis.
Die vollstaendige historische Fit-Stichprobe ist hier nicht auditiert;
die absolute Nukleonmasse bleibt deshalb Reproduktionsgroesse, kein als
unabhaengig deklarierter Vorhersagetest.

Der gelesene Trainingspfad enthaelt bis zu 2600 Optimierungsschritte plus
umfangreiche Monte-Carlo-Auswertung. Er wurde nicht importiert,
installiert oder ausgefuehrt. Ein Methodenvergleich soll vorhandene
Solver nutzen; vor Uebernahme sind Lizenz, Abhaengigkeiten, Laufgrenzen
und die oben genannte Energiekonvention zu klaeren.

## Anschluss an das Atom

Die Schnittstelle ist die **elektromagnetische Antwort desselben
Nukleonzustands**, nicht das Bild dreier Punktquarks im Atom.

| Groesse | Referenzauftrag und Grenze |
| --- | --- |
| Masse $M_N$ | Interner Eigenwert mit dokumentiertem Ruheenergie-/Offsetbezug; nicht $3m$ und kein erneuter Fit am Wasserstoff. |
| Ladung/Struktur | Im nichtrelativistischen Impulsansatz $F_E(\boldsymbol q)=\langle\sum_i(q_i/e)e^{i\boldsymbol q\cdot(\boldsymbol r_i-\boldsymbol R)}\rangle$. $F_E(0)$ ist ein Normierungscheck; die Steigung eine zu berechnende Groesse. |
| Magnetische Antwort | Strom-/Momentoperator und Masseneinheit festlegen; dieselbe gekoppelte Wellenfunktion verwenden. Alte $4/3,-1/3$-Gewichte nicht als raeumliches Ergebnis festschreiben. |
| Physikalische Formfaktoren | Nichtrelativistische Impulsantwort nicht ohne relativistische Strom-/Boostkontrolle mit exakten Sachs-Formfaktoren gleichsetzen. |
| Atomare Energie | Reduzierte Masse, Ladung und unabhaengig bestimmte Struktureingaben gemeinsam verwenden. Elektronenfeld und QED bleiben Referenzeingaben. |

Fuer den strukturellen Anschluss dient NRQED, also die effektive
Beschreibung nichtrelativistischer geladener Quantenfelder. Nach
[Hill und Paz, PRL 107, 160402 (2011), Gleichungen (2)--(4), (13)](https://arxiv.org/html/1103.4617v2)
gehen elastische Formfaktoren in Einphotonkopplungen ein; fuer
Zweiphotonbeitraege werden zusaetzliche Compton-/Kontaktinformationen
benoetigt. Masse, Radius und magnetisches Moment allein bestimmen deshalb
noch nicht die vollstaendige Lamb- oder Hyperfeinstruktur. Im fuehrenden
Ladungsradiusbeitrag gilt fuer Wasserstoff, mit Radius in denselben
natuerlichen Einheiten,

$$
\Delta E^{\rm radius}_{n\ell}
=\frac{2}{3}\frac{\alpha^4 m_r^3}{n^3}r_{E,p}^2\,\delta_{\ell0},
\qquad m_r=\frac{m_eM_p}{m_e+M_p}.
$$

Das ist eine Referenz-Matchingformel, keine hier berechnete Spektrallinie.
Ein eingesetzter experimenteller Radius prueft die Atomrechnung, nicht
das Quarkmodell. Ein aus dem Quarkmodell gelieferter Radius braucht
separat numerische und physikalische Fehler. Doppelzaehlung zwischen
Formfaktor-, Kontakt- und Strahlungskorrekturen ist zu vermeiden.

## Implementierte gekoppelte Gaussbasis

Der [Referenzsolver](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/experiments/current/reference/nucleon_gaussian_basis.py)
implementiert bekannte explizit korrelierte Gaussfunktionen, keine neue
Quantenmethode. Grundlage sind unter anderem
[Varga und Suzuki, PRC 52, 2885 (1995)](https://arxiv.org/abs/nucl-th/9508023)
und die direkt geprueften Formeln (8)--(10) in
[Fedorov et al., Few-Body Systems 65, 75 (2024)](https://link.springer.com/article/10.1007/s00601-024-01945-x).
Anders als bei stochastischer Variationsoptimierung werden hier die
Exponenten vorab festgelegt. Die lineare Diagonalisierung verwendet
[SciPy/LAPACK `eigh`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.eigh.html).
DeepQuark-Code wird nicht kopiert oder ausgefuehrt.

Fuer $x=(\rho,\lambda)$ und positiv definite reelle $2\times2$-Matrizen
ist $g_A(x)=N_A\exp(-x^TAx)$ normiert. Der Kreuzterm
$A_{12}\rho\cdot\lambda$ erlaubt korrelierte, insgesamt rotationsskalare
Ortsfunktionen. $L=0$ bedeutet hier nicht, beide Jacobi-Partialwellen auf
Null festzuhalten. Die vier inneren Nukleonkanaele werden gemeinsam mit
der Ortsfunktion durch $P=\frac16\sum_{\pi\in S_3}U_\pi$ symmetrisiert;
der separate Farbsingulettfaktor stellt die Gesamtantisymmetrie her.
Der Vergleichssektor $S=I=3/2$, $S_z=I_z=1/2$ hat einen inneren Kanal.

Mit $D=A+B$, $u=w^TD^{-1}w$ und $r=|w^Tx|$ gelten fuer normierte Gauss-
Ueberlappung $S_{AB}$ die analytischen Verhaeltnisse

$$
\frac{\langle g_A|T|g_B\rangle}{S_{AB}}
=\frac{3}{m}\operatorname{tr}(AB D^{-1}),\quad
\langle r^{-1}\rangle_{AB}=\frac{2}{\sqrt{\pi u}},\quad
\langle r\rangle_{AB}=2\sqrt{u/\pi},
$$

$$
\langle r^2\rangle_{AB}=\frac32u,\quad
\langle e^{-r^2/r_0^2}\rangle_{AB}=(1+u/r_0^2)^{-3/2},\quad
\langle e^{i\boldsymbol q\cdot w^Tx}\rangle_{AB}=e^{-q^2u/4}.
$$

Die Klammern mit Index $AB$ bezeichnen durch $S_{AB}$ dividierte
Matrixelemente, nicht bereits Erwartungen des Nukleongrundzustands.
Die ersten Integrale wurden gegen unabhaengige Gauss-Hermite- bzw.
Radialquadratur geprueft. Die einseitige Sechserprojektion stimmt fuer
alle implementierten Observablen mit der expliziten 36-Term-Bra-/Ket-
Projektion ueberein; die Wellenfunktion erfuellt alle sechs
Permutationsidentitaeten auch punktweise.

Das Ueberlappungsproblem wird ohne kuenstlichen Diagonalzusatz geloest:
Null- und sehr kleine Metrikrichtungen werden bei vorgegebenem relativem
Eigenwertcutoff entfernt. Rang, gesamtes Metrikspektrum, Kondition und
Matrixresiduum werden berichtet. Das Matrixresiduum kontrolliert nur
die endliche Rechnung, nicht den Rest ausserhalb der Basis. Ein Wechsel
des Cutoffs kann verschachtelte effektive Unterraeume zerstoeren; deshalb
werden beide Cutoffs und die Energie-Monotonie explizit verglichen.

Der [synthetische Preflight mit Zustandsarchiv](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/reference/nucleon_gaussian_readiness_with_state_2026-10-28.json)
verwendet **keine AL1-Eigenwertrechnung**, sondern
$H=T+\frac18(\rho^2+\lambda^2)+0.1$ bei $m=1$ in synthetischen Einheiten.
Der exakte Grundzustand hat $E_0=1.6$, mittleres Quarkradiusquadrat $2$,
Proton-Ladungsradiusquadrat $2$ und Neutron-Ladungsradiusquadrat $0$.
18 festgelegte Gaussfunktionen mit vier Kanaelen ergeben 72 rohe
Richtungen und Rang 51 bei beiden Cutoffs $10^{-10},10^{-12}$.
Die genannten Werte werden bis auf Rundung reproduziert; relatives
Matrixresiduum etwa $2.51\,10^{-16}$. Gemessene Laufzeit etwa 0.52 s
auf diesem Rechner, keine Garantie fuer den groesseren AL1-Lauf.

Die [27 neuen Tests](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/tests/test_nucleon_gaussian_basis.py)
zusammen mit den [Runner-Tests](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/tests/test_nucleon_gaussian_run.py)
decken auch beide Spinsektoren, Formfaktorsteigung, Metrikfehler,
Deadline und Nichtueberschreiben ab. Die Gesamtzahl bezieht sich auf
beide Testdateien. Der erste Preflight ohne Koeffizientenexport bleibt
im [Provenienz-Commit b09e553](https://github.com/MemoryDynamics/Knoten/tree/b09e553cf6d0e671f05d8f77400bc5317203e71d)
erhalten. Danach wurde nur der Zustandsexport ergaenzt und der
synthetische Preflight in eine neue Datei geschrieben.

Archiviert werden die Exponenten und normierten Ritz-Koeffizienten in
Gauss-major-Reihenfolge, innerhalb jeder Gaussfunktion
$(s_{12},t_{12})=(0,0),(0,1),(1,0),(1,1)$; im Delta-Sektor nur ein Kanal.
Damit sind Zustand und Observablen rekonstruierbar. Die Richtung einer
globalen reellen Phase ist physikalisch bedeutungslos.

## Numerische Abnahme und offener Ausfuehrungsumfang

Der physikalische Referenzoperator und der Solver sind spezifiziert.
Der [einmalige AL1-Ausfuehrungsvorschlag](https://github.com/MemoryDynamics/Knoten/blob/codex/paper-i-finalization/reports/project/meta/preregistration/nucleon_al1_reference_proposal_2026-10-28.md)
ist zur Autorenentscheidung vorbereitet, **noch nicht freigegeben**.
Die Abnahme muss mindestens enthalten:

- Schwerpunktfreie gekoppelte Basis, korrekte Paarsymmetrien und
  Hermitizitaet; kein willkuerlicher Coulomb-Abstandscutoff.
- Getrennte $S=I=1/2$- und $S=I=3/2$-Vergleiche, falls eine energetische
  Spinselektion behauptet wird. Das Loesen nur des gewaehlten Sektors
  waehlt seinen Spin nicht dynamisch aus.
- Vorab feste verschachtelte Basisverfeinerungen bzw. feste
  Variations-/Stichprobenkontrollen. Ein Energieplateau allein kontrolliert
  weder fehlende Kanaele noch Radius und magnetische Antwort.
- Eigenresiduen, Normierung, numerische Unsicherheit und Modellfehler
  getrennt; Variationsenergie ist nur innerhalb eines nachweislich
  zulaessigen Raums eine obere Schranke. Ein zweiter Methodenvergleich
  muss denselben Hamiltonoperator einschliesslich Offset verwenden.
- Keine Nachkalibrierung an Protonradius, Moment oder atomarem Spektrum;
  bekannte Fehlvorhersagen bleiben sichtbar. Bei fehlender Konvergenz
  `inconclusive`, keine automatische Ressourcenvergroesserung.

Reproduzierbar sind bisher die festen Operatortests und der synthetische
Solver-Preflight; kein AL1-Ziellauf:

```powershell
python -m experiments.current.reference.nucleon_spatial_preflight --output <neue-ausgabe.json>
python -m pytest tests/test_nucleon_spatial_preflight.py -q
$env:OPENBLAS_NUM_THREADS='1'
python -m experiments.current.reference.nucleon_gaussian_run --mode oscillator-preflight --output <neue-synthetische-ausgabe.json>
```

Die offene Arbeitsreihenfolge steht ausschliesslich in den
[Projektprioritaeten](../status/project_priorities.md). Der Memory-Zweig
bekommt durch diese Referenz keine Quark-, Spinor-, Confinement- oder
Quantenmessregel geschenkt. Sein gemeinsamer Kraft-/Arbeits-/Messanschluss
bleibt ein unabhaengiges Forschungsproblem.
