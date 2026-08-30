# Report-Index

Stand: 2026-08-30.

Dieses Verzeichnis ist das datierte Evidenzarchiv. Ein Report dokumentiert
einen kontrollierten Zwischenstand; seine Existenz macht ihn nicht automatisch
zu einem aktuellen Claim. Die aktive Entscheidungsschiene steht unten.

## Statusvokabular

- **structural:** folgt aus Definition, Ableitung oder exaktem Kontrolltest.
- **supported:** numerisch ueber die dokumentierten Seeds und Kontrollen
  gestuetzt.
- **negative:** das vorregistrierte oder primaere Gate wurde nicht bestanden.
- **inconclusive:** Daten oder Metriken entscheiden die Hypothese nicht.
- **pipeline-only:** validiert Ausfuehrung oder Datenpfad, nicht den Claim.
- **legacy-sign:** verwendet die fruehere Kernelgradient-Konvention und ist nur
  Auditmaterial.
- **superseded:** durch eine spaetere kontrolliertere Auswertung ersetzt.

## Aktuelle Evidenzschiene

### 1. Skalarer Mechanismus

- [Kernel-Familienvergleich](kernels/core/kernel_family_comparison_d3_N300k_2026-07-19.md)
  - **supported:** Ein- und Zweiskalenkernel kollabieren bei gematchter lokaler
    Kruemmung auf `A_eff=A_att-9`.
- [LoG-/Taylor-Kernel-Audit](kernels/core/log_taylor_kernel_audit_2026-07-28.md)
  - **structural:** ein curvature-matched LoG ist exakt zero mean; er erklaert
    weder die bisherige Amplitude noch selektiert er `27`, `36` oder `d=3`.
- [Long-Run-Reconciliation](long_runs/scalar_hardening/linear_long_run_reconciliation_2026-07-19.md)
  - **supported:** neun aktive `N=30M/300M`-Slices folgen dem linearen
    Finite-Memory-Radius bis maximal `1.16%` relativ.
- [Skalarer Memory-Kontinuumsgrenztest](dynamics/limits/scalar_memory_continuum_limit_reconciliation_2026-08-15.md)
  - **supported, local and scaling-conditional:** Die prospektive Seed-6--10-
    Reconciliation besteht Validitaet, Finite-Tail und gematchte
    Alpha-Konvergenz. Der RMS-Kontinuumsfehler sinkt von `0.046095` bei
    `alpha=0.04` auf `0.003006` beim Holdout `alpha=0.0025`; die simulierte
    Antwort liegt etwa `1e-5` von der exakten Finite-H-Referenz entfernt.
  - Der [registrierte Erstlauf](dynamics/limits/scalar_memory_continuum_limit_gate_2026-08-15.md)
    bleibt formal `experiment-inadequate`: sein zeitversetzter Kontrollradius
    war kein interventionsspezifisches G0-Kriterium. Die Reconciliation aendert
    diese historische Entscheidung nicht rueckwirkend.
  - **Grenze:** bestaetigt ist eine konstruierte reelle Relaxationsgrenze bei
    festem `chi`, `D` und `alpha H`, keine emergente Masse, kein Impuls und
    keine unterdaempfte Mode. Siehe [kritisches Review](project/meta/reviews/scalar_memory_continuum_limit_review_2026-08-15.md).
- [Skalarer Force-/Work-Port](dynamics/limits/scalar_memory_force_work_port_gate_2026-08-16.md)
  - **supported overdamped, negative finite-inertial signature:** Der
    prospektive Port besteht G0, G1 und alle vier G2O-Komponenten; alle vier
    G2I-Komponenten scheitern. Am Holdout sind Feedthrough \(1.000000\),
    post-pulse Geschwindigkeit pro Impuls \(-3.990101\),
    \(\alpha W/J^2=1.000000\) und die Kurzzeit-MSD-Steigung \(0.959048\).
  - **Grenze:** Der direkte additive Kraftport testet eine dimensionslose
    lokale skalare Reduktion. Er verwirft positive endliche Traegheitsmasse
    fuer diesen Port, nicht jeden moeglichen erweiterten Impulszustand. Siehe
    [kritisches Review](project/meta/reviews/scalar_memory_force_work_port_review_2026-08-16.md).
- [Skalarer Center-Inertial-Port](dynamics/limits/scalar_memory_center_inertial_port_gate_2026-08-16.md)
  - **structural inertial representation plus supported local embedding;
    physical mass unresolved:** Der prospektive Seed-16--20-Lauf besteht G0,
    G1 und alle elf Center-Inertial-Komponenten; alle vier
    overdamped-Center-Komponenten scheitern. Am Holdout sind
    \(m=0.996239\), \(\gamma=5.002630\) und die Center-MSD-Steigung
    \(1.972302\). Diese Diagnosen sind konsistente Folgen desselben
    OU-Transfers, keine elf unabhaengigen Massebelege.
  - **Reconciliation:** Der sichtbare Ausgang \(x=c+r\) bleibt overdamped.
    Der reine normalisierte Memory-Center besitzt dagegen unter \(f\,dc\)
    positive Speicherbilanz, Null-Feedthrough und ballistische Kurzzeit-MSD.
    Das ist eine effektive Readout-/Port-Aussage, kein SI-Masse- oder
    Teilchenclaim. Siehe [Ergebnisreview](project/meta/reviews/scalar_memory_center_inertial_port_review_2026-08-16.md)
    und [Referee-Audit](project/meta/reviews/scalar_memory_center_mass_referee_audit_2026-08-16.md).
- [Checkpoint-/Holdout-Stabilitaetsgate](long_runs/stability/checkpoint_stability_gate_d10_A35_2026-07-30.md)
  - **supported, method-conditional:** 5/5 `d=10`, `A_att=35`-Seeds bestehen
    vier Alterscheckpoints bis `N=30M`, lokale Radiusfenster und den
    `N=300M`-Holdout. Keine erste Formationszeit, keine zeitaufgeloeste
    Shape-Stationaritaet und kein Teilchenclaim.
- [Feste-g-Skalenpruefung](kernels/nonlinearity/fixed_g_scale_reconciliation_d3_N300k_A26_2026-07-19.md)
  - **inconclusive:** kleine Superlinearitaet, aber kein Shape-Umschlag;
    Residence- und Score-Metriken sind auf dieser Radiusachse nicht
    diskriminierend.

Entscheidung: Der bisherige kompakte Ast bleibt eine kontrollierte lineare
Baseline mit scaling-konditionalem Kontinuumsgrenzwert. Daneben besitzt der
unveraenderte rauschfreie \(d=2\)-K0-H-Kern am separat prospektierten
Parameterpunkt \(A_{\rm att}=3.5\) nun eine lokal existenzzertifizierte
Folge aus sechs finite-Summen-Rootzellen und lokale numerische
Stabilitaetsevidenz am vorbereiteten Anchor sowie an L3. Ein separat implementierter
Foundation-Audit reproduziert die
historischen fuenf Roots, den Fixed-gain-Kontinuumsroot und die First-order-
Skalierung; der danach prospektierte L5-Holdout besteht die Krawczyk-,
direkten Summen- und signierten Skalierungsgates ohne Retuning. Der getrennt
eingefrorene L3-Test besteht seine zwei Arnoldi- und sechs gespiegelten
Perturbationspanels. Das ist kein Beleg fuer generische Formation,
Stabilitaet der ganzen Leiter, Robustheit oder eine interne Phase nach
\(SO(2)\)-Reduktion. Die
Portwahl entscheidet weiterhin die mechanische Realisierung: Der sichtbare
\(x\)-Port selektiert overdamped Memory, waehrend der aus dem Memory
abgeleitete Center \(c\) unter \(f\,dc\) eine positive passive
Inertialdarstellung besitzt. Zulaessig sind lokale mathematische Existenz-,
Stabilitaets- und Einbettungsclaims, nicht die Behauptung einer eindeutig
selektierten physischen Knotenposition oder emergierten physikalischen Masse.

### 2. Dimension

- [Dimensionsclaim-Audit](dimensions/claims/dimension_claim_audit_2026-07-15.md)
- [D_spec-Sensitivitaet](dimensions/sensitivity/dspec_sensitivity_2026-07-15.md)
- [Rohsnapshot-Retest](dimensions/raw_snapshots/dspec_raw_snapshot_retest_2026-07-16.md)
- [Dimensionen ueber N](dimensions/n_scaling/dimension_over_n_d10_A35_2026-07-30.md)
  - **reproduced, measurement convergence not evaluable:** `D_mem` bleibt fuer
    drei gematchte Seeds bei `8.857..9.268`; `D_cov` ist nichtmonoton. Das neue
    D_occ/D_win-Gate scheitert bereits an Trainingsrange/-trend und ist wegen
    Cadence-/Revisionswechsel sowie fruehen ungueltigen D_win-Fits nicht
    auswertbar. Der sichtbare Trend ist keine zertifizierte N-Abhaengigkeit.

Entscheidung: Shape-, Sample- und Heat-Trace-Dimension sind getrennte
Diagnostiken. Die vorhandenen Daten stuetzen keine ambient-unabhaengige
`d=3`-Selektion.

### 3. Memory-Feld und reduzierte Moden

- [S1-Phasen- und Masse-Falsifikationsprogramm](project/decisions/s1_phase_mass_falsification_program_2026-08-16.md)
  - **program charter; historischer Eintrittsstand:** Ein moeglicher neuer
    Oszillationssatz wird erst nach vollstaendiger Parameter- und
    Discovery-Provenienz als `P0` eingefroren. Zum Zeitpunkt dieses Audits lag
    noch kein eindeutiges neues Tupel vor. Alte komplex-eligible oder
    quench-ringing Punkte bleiben als konfirmatorische Kandidaten gesperrt.
  - Der [ausgefuehrte P0-Audit](project/meta/preregistration/s1_candidate_p0_audit_2026-08-16.md)
    findet keinen eindeutigen neuen Kandidaten- oder Discovery-Datensatz und
    endet mit 27 Manifestdefekten. Der maschinenlesbare Validator blockiert
    deshalb D0, D1 und jeden Ziellauf; dies ist ein Provenienz-Fail, kein
    negatives Topologieergebnis. Dieser historische Audit wird nicht
    rueckwirkend umgedeutet.
  - Die neue
    [prospektive Rotating-wave-Discovery](dynamics/rotation/scalar_memory_rotating_wave_discovery_2026-08-20.md)
    startet stattdessen aus einer vorab eingefrorenen analytischen
    Selbstkonsistenzgleichung und getrennten Kontrollen. Sie findet bei
    \(\alpha=0.01,H=1200,\eta=0.15,A_{\rm att}=3.5\)
    \(R=0.9465175\), \(\theta=0.01577038\) mit Residual
    \(4.53\,10^{-17}\); \(A_{\rm att}=0,9,35\) liefern in der registrierten
    Box keine zulaessige radiale Nullstelle. Das
    [Discovery-Review](project/meta/reviews/scalar_memory_rotating_wave_discovery_review_2026-08-20.md)
    begrenzt dies auf numerische Existenz.
  - Der kandidatspezifische
    [P0-Audit](project/meta/preregistration/scalar_memory_rotating_wave_p0_audit_2026-08-20.md)
    besteht mit null Defekten. Der
    [D0-Vertrag](project/meta/preregistration/scalar_memory_rotating_wave_d0_contract_2026-08-20.md)
    identifiziert exakt eine translationsreduzierte raeumliche
    \(SO(2)\)-Gruppenbahn. Nach Quotientieren der ambienten Rotation ist sie
    ein Punkt, keine nachgewiesene interne \(S^1\)-Phase.
  - Das prospektive
    [Voll-FIFO-Stabilitaetsgate](dynamics/rotation/scalar_memory_rotating_wave_stability_2026-08-20.md)
    besteht numerisch. Zwei Arnoldi-Panels stimmen fuer den fuehrenden
    transversalen Multiplikator
    \(|\lambda|=0.99306035\) ueberein; drei registrierte Stoerungen kehren
    ueber 5000 Updates zum Gleitkommafloor zurueck. Das
    [kritische Stabilitaetsreview](project/meta/reviews/scalar_memory_rotating_wave_stability_review_2026-08-20.md)
    fordert weiterhin Spektraleinschliessung, Horizon-/Alpha-Robustheit,
    Formation und Rauschen; Masse und Center-Arbeit bleiben getrennt.
  - Das lokale
    [Anchor-Intervallzertifikat](dynamics/rotation/scalar_memory_rotating_wave_interval_certificate_2026-08-21.md)
    und die
    [fuenfzellige Refinement-Leiter](dynamics/rotation/scalar_memory_rotating_wave_refinement_ladder_2026-08-21.md)
    zertifizieren lokal eindeutige finite-Summen-Roots bei
    \(H\alpha=12\) und \(\eta/\alpha=15\). Der Leiterentscheid bleibt formal
    `certified-roots-nonconvergent`, weil sein vorab fixierter Guide zu Gain
    15.016345 statt 15 gehoerte.
  - Die anschliessende
    [Fixed-gain-Reconciliation](dynamics/rotation/scalar_memory_rotating_wave_continuum_reconciliation_2026-08-21.md)
    besteht alle unveraenderten Skalierungsgates gegen den korrekt bei Gain 15
    definierten Kontinuumsroot, ohne den historischen Fail umzubenennen.
  - Der reviewertragende
    [Foundation-Audit](dynamics/rotation/scalar_memory_rotating_wave_foundation_audit_2026-08-21.md)
    reproduziert alle fuenf finite Summen mit Residuen unter
    \(8\times10^{-72}\), bestimmt den Kontinuumsroot unabhaengig mit
    Tanh--Sinh und Gauss--Legendre und wiederholt die First-order-Gates. Sein
    initialer binaerer Decimal-Vergleichsfehler bleibt im
    [historischen Pipeline-Fail](dynamics/rotation/scalar_memory_rotating_wave_foundation_audit_initial_implementation_fail_2026-08-21.md)
    sichtbar. Ein zweites
    [Portabilitaetsprotokoll](project/meta/preregistration/scalar_memory_rotating_wave_foundation_portability_reconciliation_protocol_2026-08-21.md)
    friert nach dem Linux-CI-Fund die kanonische Git-Blob-Hashdomaene und
    Vollhistorienpruefung ein. Nur der danach erneut vollstaendig gerechnete
    A--E-Re-Run traegt das scoped positive Urteil. Das kompakte
    [Rotations-Ledger](dynamics/rotation/README.md) ordnet alle Artefakte.
    Der [abschliessende kritische Review](project/meta/reviews/scalar_memory_rotating_wave_foundation_review_2026-08-21.md)
    empfiehlt Main-line-Aufnahme als Basis fuer vorbereitete Schleifen, nicht
    als Nachweis einer stabilen Familie, Formation oder Masse.
  - Der anschliessend separat
    [vorregistrierte L5-Test](project/meta/preregistration/scalar_memory_rotating_wave_l5_existence_scaling_protocol_2026-08-21.md)
    besteht bei
    \((\alpha,H,\eta)=(0.00125,9600,0.01875)\) beide lokalen
    [Krawczyk-Panels, den direkten Summen-Replay und alle signierten
    First-order-Gates](dynamics/rotation/scalar_memory_rotating_wave_l5_existence_scaling_2026-08-21.md).
    Die L5/L4-Fehlerquotienten sind 0.4993/0.4992. Das
    [kritische L5-Review](project/meta/reviews/scalar_memory_rotating_wave_l5_existence_scaling_review_2026-08-21.md)
    akzeptiert damit sechs lokale Rootzellen, markiert aber `mpmath.iv` als
    noch nicht durch einen zweiten Intervallbackend verifiziert.
  - Das danach separat
    [eingefrorene P1-L3-Protokoll](project/meta/preregistration/scalar_memory_rotating_wave_l3_stability_protocol_2026-08-22.md)
    und sein
    [Ergebnis](dynamics/rotation/scalar_memory_rotating_wave_l3_stability_2026-08-22.md)
    liefern `numerically-stable-source-pass`: beide Arnoldi-Panels stimmen bei
    \(|\lambda_\perp|=0.99649340\) ueberein, und alle sechs gespiegelten
    Stoerungsarme kontrahieren. Das
    [kritische Review](project/meta/reviews/scalar_memory_rotating_wave_l3_stability_review_2026-08-22.md)
    haelt nur lokale numerische Stabilitaet an dieser zweiten Skala aufrecht.
  - Das [P2-Ergebnis](dynamics/rotation/scalar_memory_loop_center_p2_2026-08-25.md)
    endet formal `loop-center-matrix-local-fail`, obwohl der volle
    FIFO-Jacobian die schwache nichtlineare Antwort mit grosser Marge
    beschreibt. Die outcome-informierte
    [P2-R-Verlaengerung](dynamics/rotation/scalar_memory_loop_center_p2r_long_recovery_2026-08-25.md)
    reproduziert den Fail und zeigt in allen 48 neuen Fenstern Rueckkehr bis
    20 Memory-Zeiten.
  - [P3](dynamics/rotation/scalar_memory_rotating_wave_p3_formation_basin_2026-08-26.md)
    besteht fuer zehn nichtkreisfoermige Arme aus fuenf Geometrien; das
    [Review](project/meta/reviews/scalar_memory_rotating_wave_p3_formation_basin_review_2026-08-26.md)
    erlaubt nur finite-ensemble attraction.
  - [P4](dynamics/rotation/scalar_memory_loop_p4_source_write_2026-08-26.md)
    schliesst den kompletten finite-H-Write-/Age-/Interaktionsledger des
    expliziten Ports, bleibt aber formal
    `p4-source-write-architecture-fail` und falsifiziert die skalare
    Geradeausantwort.
  - Der frische
    [P4-R-phi-Holdout](dynamics/rotation/scalar_memory_loop_p4r_phase_metrology_2026-08-26.md)
    besteht lokale Metrologie, Full-dot-Envelopes, Ledger und die diskrete
    Acht-Phasen-Chiral-Klassifikation. Das
    [Gate-Review](project/meta/reviews/scalar_memory_loop_p4r_phase_metrology_review_2026-08-27.md)
    haelt nur diesen engen Befund aufrecht; vier spiegelverschiedene
    Phasenpaare sind keine Replikationen.
  - Das
    [Publication-Source-Referee-Audit](project/meta/reviews/p4_publication_source_referee_audit_2026-08-27.md)
    liefert `referee-source-ready-with-major-claim-restrictions`: zwei
    NumPy/SciPy-Stacks reproduzieren alle wissenschaftlichen P4-R-Felder
    exakt, waehrend zweiter Intervallbackend, vollstaendiger Hash-Lock und
    Citation/Release offen bleiben. Der targetfreie
    [P4-R-S-Designaudit](project/meta/reviews/scalar_memory_loop_p4rs_anchor_scale_design_audit_2026-08-30.md)
    und das
    [Anchor-Protokoll](project/meta/preregistration/scalar_memory_loop_p4rs_anchor_scale_protocol_2026-08-30.md)
    frieren nun Memory-Zeit-Abbildung, kandidatenspezifischen Port, 48 Arme
    und `0.05`-Trace-/Profilgrenzen ein. Runner und Target fehlen weiterhin;
    P5, Spin, Impuls, Traegheit und Masse bleiben geschlossen.
  - Der getrennte [Center-Mechanik-P0](project/meta/preregistration/scalar_memory_center_mechanics_p0_audit_2026-08-16.md)
    besteht dagegen mit null Defekten und oeffnet ausschliesslich A. D0--D5
    bleiben als `sealed-no-s1-candidate` geschlossen.
  - [Gate A](project/meta/reviews/scalar_memory_center_physical_port_gate_a_2026-08-16.md)
    identifiziert aus dem vorhandenen additiven \(x\)-Input keinen eindeutigen
    physischen Port. Ein \(x\)-Port hat \(f\,dx=f\,dc+f\,dr\), aber ein
    effektives \(U_{\rm ext}(c,Q)\) erzeugt dieselbe Zustandsgleichung. Ohne
    mikroskopischen Aktuator- und finite-H-Grenzvertrag bleibt nur der
    mathematische passive Center-Port; physische B/C/E/F1 sind gestoppt.
  - Das [finite-H-A2-Protokoll](project/meta/preregistration/scalar_memory_center_finite_h_port_a2_protocol_2026-08-16.md)
    wurde aus einem sauberen prospektiven Commit ausgefuehrt. Der
    [A2-Ergebnisbericht](dynamics/limits/scalar_memory_center_finite_h_port_a2_2026-08-16.md)
    besteht alle fuenf globalen Small-Gain-/Positive-Real-Zellen; der
    Frequenzgrid ist nur Sanitycheck. Der
    [kritische A2-Review](project/meta/reviews/scalar_memory_center_finite_h_port_a2_review_2026-08-16.md)
    bestaetigt die Tail-Algebra, begrenzt den Pass aber auf einen reziprok
    realisierbaren effektiven Filter-Port. Nur B-star-Systemidentifikation ist
    geoeffnet; physisches B und der S1-Ast bleiben versiegelt.
  - Die [lesbare Center-Filter-Notationsbruecke](../docs/reference/scalar_memory_center_filter.md)
    schreibt \(B_H\) zuerst als normierte endliche geometrische Reihe aus,
    fuehrt \(q,M_H,g_H\) auf \(\alpha,\eta,H,M_0\) und die Kernelkruemmung
    zurueck und trennt \(H\) explizit von der blossen Laufzeit \(N\).
    Zusaetzlich dokumentiert sie den lokalen Rotations-No-go-Satz, die exakten
    radialen/tangentialen finite-\(H\)-Bedingungen, den aktuellen lokalen
    Stabilitaetspass und die offene mikroskopische Center-Aktuatorfrage.
  - Das [B-star-Skalierungsprotokoll](project/meta/preregistration/scalar_memory_center_filter_scaling_bstar_protocol_2026-08-16.md)
    wurde vom sauberen prospektiven Commit ausgefuehrt. Der
    [Ergebnisbericht](dynamics/limits/scalar_memory_center_filter_scaling_bstar_2026-08-16.md)
    besteht Trainingsgesetz und gemeinsame Holdout-Ecke fuer state-matched
    und neu formierte Zustaende: tau-Exponent 1, mu-Exponent -1,
    M0-Exponent 0 und Holdout-Masse 3.99997 statt 4. Der
    [kritische Review](project/meta/reviews/scalar_memory_center_filter_scaling_bstar_review_2026-08-16.md)
    ordnet die fast exakte Uebereinstimmung als lokalen Implementations- und
    Skalierungstest ein, nicht als unabhaengige Materieentdeckung. Seeds
    21--25, der P0-Transfer-Holdout und der S1-Zielast bleiben versiegelt;
    physisches B bleibt blockiert.
  - Der [zweite Referee-Pass](project/meta/reviews/s1_phase_mass_falsification_program_review_2026-08-16.md)
    korrigiert insbesondere den diskreten Periodenorbit-/\(S^1\)-Fehlschluss,
    Raw-cloud-Shuffle-Nulltest, Pseudoreplikation und die offene Impulsbilanz.
  - Die [synthetische Topologiekontrolle](topology/s1_control_pipeline_2026-08-16.md)
    ist der einzige gestartete Ast: Kreis/Hopf, Torus, Disk, Intervall,
    Dampfspirale und endlicher 12-Zyklus ohne Kandidatendaten oder Cutoff. Der
    12-Zyklus erzeugt absichtlich eine lange \(H^1\)-Klasse und falsifiziert
    damit einen naiven Persistent-Homology-gleich-Phase-Schluss.
  - Der \(S^1\)-Ast trennt rohe Topologie, out-of-sample Kreiskoordinate,
    autonome Phase und externe Phasenkopplung. A--F pruefen davon unabhaengig
    Port, Skalen, Komposition/Impuls, Transfer und Symmetrien. Vor dem
    Candidate-Freeze wird keine neue Zielsimulation ausgefuehrt; der separate
    Method-Validation-Split bleibt bis zur Freeze-Regel ungeoeffnet.
- [P3.8d dynamisches Zwei-Knoten-Mediatorgate](response/reciprocal/dynamic_two_knot_mediator_gate_2026-08-12.md)
  - **conditional dynamic existence pass:** Eine gemeinsame Energie liefert
    `(m,p,R)`-Dynamik mit geschlossener Source-work-/Daempfungsbilanz,
    Cross-off und zweiter Zeitschrittordnung. Zwei feste Starts erreichen das
    quasistatische Basin nahe `6.99 ell`; die erster-Ordnung-Kontrolle erreicht
    nahezu dieselbe Separation.
  - **nicht emergent:** Mediator, Koeffizienten, `nu=1` und Skalen sind gesetzt;
    Punktquench-Transienten sind UV- und Initialisierungs-sensitiv. Keine Ableitung aus `z=(x,rho)`,
    kein Orbit, Spin, Teilchen- oder Dimensionsclaim.

- [Lokaler Feldoperator-Audit](kernels/field/local_field_operator_audit_2026-07-29.md)
  - **structural:** Eine eingeschraenkte lokale Ableitungsentwicklung matcht
    den Gauss-Transfer bis `k^4`, realisiert Zero Mean mit `s0=0` und zeigt
    die Finite-k-Schwelle sowie die vollrangige `H I_d`-Null exakt.
  - `a2<0`, nichtlineare Saettigung, Quantisierung und `d=3` sind neue
    Annahmen bzw. offene Mechanismen, keine Auditresultate.
- [Write-/Read-Reparametrisierung](kernels/field/write_read_reparameterization_audit_2026-07-30.md)
  - **structural:** Drei Seeds bestaetigen `phi=K*rho` mit
    Dirac-Identitaetsreadout fuer Pfad, Feld und Gradient bis maximal
    `1.43e-14`; ein konstantes `K=1` ist exakt kraftfrei.
  - Die Umformung macht aus nichtnegativem Occupancy-Memory ein signiertes
    Potentialmemory. Sie erzeugt keine selbstdynamische Feldgleichung.
- [Kovariante Vektorrueckkopplung und Parameter-Closure](project/decisions/covariant_vector_feedback_and_parameter_closure_2026-08-07.md)
  - **structural:** Der parity-even lokale Ein-Vektorfeld-Gradientenfluss
    zerfaellt in reelle longitudinale/transversale Raten. Eine endliche
    Wellenzahl wird nur bei b_hat_L oder b_hat_T < -2 instabil ausgewaehlt;
    Gradientendynamik allein erzeugt keine zeitliche Phase.
  - Das passive orientierte Mikro-Update hat homogen exakt den Faktor
    1-lambda_v und enthaelt keine raeumlichen Feldkoeffizienten. Solche Werte
    duerfen nur als skalen- und holdout-stabile effektive Closure-Koeffizienten
    oder als klar deklarierte neue Postulate auftreten.
- [Passiver orientierter Fourier-Closure-Audit](memory/closure/oriented_fourier_closure_audit_2026-08-07.md)
  - **structural null confirmed:** Nach exaktem Abzug von neuer Quelle und
    endlichem Tail bleibt in 6/6 reifen Sources nur 1-lambda_v. Der maximale
    q-Fehler betraegt 6.6e-15, der maximale gefittete k2-/k4-Koeffizient
    1.9e-15; longitudinal und transversal stimmen ueberein.
  - Dies ist Evidenz gegen bereits emergente aktive Raumrueckkopplung im
    passiven Update. Eine source-unaufgeloeste Closure waere nur eine
    effektive Beschreibung; ein aktives Feldgesetz waere ein neuer
    Mechanismus.
- [Adjungierte Reziprozitaet: Eligibility-Audit](memory/closure/adjoint_reciprocity_eligibility_audit_2026-08-07.md)
  - **conditional eligibility:** Der exakte diskrete Modentest liegt unter
    euklidischem Metrik-Kandidaten fuer mindestens 99.83% der gespeicherten
    Schritte aller sechs reifen Sources im komplexen Fenster.
  - Der Rueckkanal, das Memory-Metrik und seine relative Normierung sind neue,
    nicht identifizierte Modellteile. Der Audit beobachtet weder Oszillation
    noch Traegheit und sperrt einen freien Gain-/Metrik-Sweep.
- [Carrier-Memory-Metrikvergleich](memory/representations/carrier_memory_metric_comparison_2026-08-08.md)
  - **negative metric closure:** Das vorregistrierte Gate besteht `0/6`
    zyklische Paare. Kovarianz, Probe-Observability und isotrope RKHS-Metrik
    ergeben bei fester Kopplung systematisch instabile, ueberdaempfte und
    komplexe Regime statt einer gemeinsamen Klassifikation.
  - Finite-Differenz-Linearitaet und Predictive-Cadence-Stabilitaet bestehen;
    absolute Skala sowie teils Horizont- und Segmentform nicht. Kein
    nichtlinearer reziproker Pilot und kein Gain-Retuning.
- [Balancierte Vollmemory-Feature-Closure](memory/closure/balanced_full_memory_feature_gate_2026-08-10.md)
  - **negative, with structural compression:** Alle 72 Actual-Auswertungen
    waehlen seed-, segment-, horizon- und cadencestabil Rang 1 mit
    `96.6..97.8%` Energieanteil. Derselbe Modus ist jedoch mit Flat- und
    Age-Shuffle-Kontrolle praktisch identisch; der Fern-Holdoutfehler bleibt
    `0.501..0.862`.
  - Das ist generische exponentielle Delay-/Readoutkompression, keine
    knotenspezifische uebertragbare Mode. Kein Gain-/Lambda-Sweep und keine
    Optimierung vermeintlicher komplexer Schwingungen.
- [Inertial-reversibler Vektorfeld-Audit](memory/closure/inertial_vector_field_analytic_gate_2026-08-11.md)
  - **structural pass, constructive:** Das konjugierte Feldpaar liefert exakt
    `I s^2+gamma s+D_q(k)=0`; Wurzeln, O(d)-Kovarianz und Energiebilanz
    bestehen bis maximal `1.18e-13`.
  - Stabile gedaempfte Schwingungen sind mathematisch moeglich, aber durch die
    neue Impulsvariable konstruiert. Keine Parameteridentifikation, keine
    beobachtete Knotenschwingung und keine `d=3`-Selektion.
- [Modellhierarchie und Parameteridentifizierbarkeit](project/decisions/model_hierarchy_and_parameter_identifiability_2026-08-11.md)
  - **structural decision:** Der Inertial-Audit aendert den kanonischen
    `(x,rho)`-Simulator nicht. Die neuen Koeffizienten sind aus passiven
    Long Runs nicht als mikroskopische Konstanten identifizierbar.
  - Naechstes Gate ist erster- gegen zweiter-Ordnung-Holdout-Closure aus einer
    vorab fixierten Projektion kanonischer Variablen; Feldpilot und
    Schwingungsoptimierung bleiben gesperrt.
  - [P3.8e-Emergenzreview](project/meta/reviews/p38e_emergent_state_review_2026-08-13.md):
    modale Finite-`k`-Minimalrealisierung, power-konjugierte Passivitaet und
    Altersstationaritaet sind die festen Gates. Ein laengerer P3.8d-Lauf,
    globaler Rang 2 oder der uniforme `k=0`-Probe koennen `(m,p)` nicht
    selektieren.
- [P3.8e technische Reconciliation](memory/closure/emergent_modal_state_reconciliation_2026-08-13.md)
  - **null not rejected, memory-holdout-limited:** Die historische
    Identifikation ist superseded: freies/gedaempftes AR(2) war redundant und
    der Panel-Hankel-Aufbau konnte Rang aufblasen. Korrigiert bestehen 0/5
    `kR_mem`-Kanaele; alle gepoolten Pole sind reell, AR(2) verbessert das
    Holdout nicht und ein isolierter Hankel-Rang 2 fehlt.
  - **Grenze:** Das Memory-Holdout traegt nur `0.2%..0.8%` Energie und die
    Inputprofile sind stark kollinear. Dies ist kein skalares No-go.
  - [Korrekturprotokoll](project/meta/preregistration/p38e_identification_reconciliation_protocol_2026-08-13.md)
    und [Referee-/Codereview](project/meta/reviews/p38e_identification_reconciliation_review_2026-08-13.md).
  - [Historisches P3.8e-Gate](memory/closure/emergent_modal_state_gate_2026-08-13.md):
    Rohantwort bleibt Auditmaterial, Modellordnungsentscheidung ist
    `superseded-methodologically-inconclusive`.
  - [Vorregistrierung](project/meta/preregistration/p38e_finite_k_mechanism_closure_2026-08-13.md):
    Intervention, Projektion, Null, Holdouts und Schwellen wurden vor dem
    Fuenf-Seed-Lauf in Revision `2ecc081` fixiert.
  - [Rigoroses Ergebnis-/Codereview](project/meta/reviews/p38e_finite_k_gate_review_2026-08-13.md):
    historisches Review mit sichtbarem Korrektur-Addendum.
- [P3.8f-a kanonischer Trajektorien-Write-Port](memory/closure/p38f_canonical_write_gate_2026-08-15.md)
  - **G0 pass, G1 inconclusive:** Zwei Staerken, drei Achsen und fuenf reife
    N=3M-Formation-Seeds bestehen alle Zero-net-, `eta=0`-, Linearitaets-,
    Spiegel- und Shape-Kontrollen.
  - Nach Entfernung der globalen Translationsnullmode bleibt die relative
    Positions-/Selbstkraftantwort nur etwa `0.12 tau_mem` ueber `1e-3` ihres
    Peak-RMS; alle drei Holdouts liegen bei rund `8e-8` des
    fruehen Signals. Memory-Holdouts bestehen, Readout-Holdouts 0/3.
  - **Grenze:** G2/G3 sind blockiert, nicht negativ. Keine Parameter-, Pol-,
    Impuls- oder Phasenidentifikation. Eine einzige memory-time-separierte
    Port-Reparatur wird vor einem weiteren Lauf separat vorregistriert.
  - [Code-/Ergebnisreview](project/meta/reviews/p38f_canonical_write_gate_review_2026-08-15.md):
    dokumentiert die korrigierte Translationsnullmode, den harten
    Memory-Horizon-Ausschlag und die verbleibenden Stopregeln.
- [Kontinuitaetsbeschraenktes Memory-Gate](memory/closure/continuity_constrained_memory_gate_2026-08-11.md)
  - **structural pass with unresolved force balance:** Die kanonische
    Memory-Innovation ist bei stationaerer Masse monopolfrei und ihr Dipol ist
    durch `x-xbar_rho` festgelegt. Ein lokaler Dichte-Strom-Modus besitzt die
    exakte Schwelle `2 c_j k > |lambda_m-gamma_j|` fuer komplexe Pole.
  - Strom, Flussrelaxation und Steifigkeit bleiben neue Annahmen; statische
    Kraftbilanz, transversale Phase und `d=3` sind nicht geloest. Kein Pilot.
- [Dynamischer Green-Kernel und Skalenwahl](memory/closure/dynamic_green_kernel_selection_gate_2026-08-11.md)
  - **structural pass after correction, model candidate:** Der `k^2`-Kanal
    gehoert zu einem separaten adjungierten Gradientenmediator `(m,p)`, nicht
    zum kanonischen `rho` oder automatisch zum P3.8a-Strom. Eine gemeinsame
    Energie erzeugt Source und Readout.
  - Exakte Residueninversion und unabhaengige unendliche Quadratur stimmen bis
    `1.81e-15` ueberein; Barriere `3.91920 ell`, lineares Paarminimum
    `6.99092 ell`. Drei dimensionslose Gruppen bleiben Inputs.
- [Quasistatische Zwei-Knoten-Diskrimination](response/reciprocal/quasistatic_two_knot_discrimination_2026-08-12.md)
  - **conditional discriminability pass:** Zwei komplette starre N100M-
    Memory-Wolken liefern bei `R=5 ell` entgegengesetzte Kraftvorzeichen fuer
    statischen kompensierten Kernel und Gradientenmediator.
  - **Kein Dynamikpass:** nur ein nahezu punktfoermiger d3-Formationsseed,
    gesetztes Skalenmatching, kein Gain-Fit, keine Zustandsfortschreibung und
    keine Auswahl zwischen den Architekturen. Memory-Memory- und symmetrisierter
    Sichtpunkt-Memory-Cross-Readout behalten dieselben Vorzeichen, bleiben aber
    verschiedene Regeln; ihr `0.2411%`-Offset ist der endliche Tail-Masseneffekt.
- [Aktives skalares Delta-Quellfeld](kernels/field/active_scalar_delta_field_pilot_2026-07-31.md)
  - **supported, model-conditional:** Zeit-/Gitter-, cubic-off- und source-off-
    Gates bestehen; der kubisch gesaettigte aktive Arm bildet in drei Seeds
    einen beschraenkten Peak bei `k=1`.
  - `eta=0` traegt nahezu dasselbe Feld. Der Pass gilt fuer klassische
    Finite-k-Musterbildung, nicht fuer einen feedback-spezifischen Knoten,
    Quantisierung, QFT oder `d=3`.
- [Spektrale rho-Reprasentation](memory/representations/spectral_rho_field_pilot_2026-07-19.md)
  - **structural + pipeline-only:** Historie, Masse, Kontraktion und Kraft sind fuer
    die getestete 1D-Reprasentation reconciliiert.
- [Relaxations-Diffusionsfeld](memory/representations/relaxation_diffusion_field_pilot_2026-07-19.md)
  - **supported:** modeabhaengige Glaettung ist kontrolliert; kein
    Propagations- oder Metastabilitaetsclaim.
- [Mode-Identity-Audit](memory/closure/low_mode_identity_audit_2026-07-20.md)
  - **negative:** weder ein stabiler einzelner Realmodus noch ein
    feedback-spezifischer komplexer Modus besteht das Segment-/Kontrollgate.
- [Eta-zero-Rohmoden-Null](memory/closure/eta_zero_raw_mode_null_audit_2026-07-31.md)
  - **structural + negative:** Der rohe Fourier-Zustandsblock besitzt exakt
    nur reelle Multiplikatoren. Bei archivierter N=1M-Kadenz bleiben gepoolte
    und seedweise Fits reell; kleine Segmentleckage erreicht maximal
    `7.25e-4` Frequenz pro Memory-Zeit.
  - Die ausgerichteten komplexen AR-Paare werden damit als Darstellungs- und
    Fitmoden klassifiziert, nicht als physikalische Oszillation.

Entscheidung: Niedrige Moden sind nuetzliche Rechenfeatures, derzeit keine
identifizierten physikalischen Moden.

### 4. Referenzzustaende und externe Antwort

- [Reziprokes lokales Modengate](response/reciprocal/reciprocal_local_mode_gate_2026-08-04.md)
  - **structural:** Common-/Relative-Mode-Zerlegung und voller
    Vier-Zustands-Matrixabgleich ergeben ein stabiles komplexes Fenster nur
    fuer `g < lambda/(1+lambda)`; innerhalb des Fensters ist `c > g`
    notwendig. Die kompakte Baseline `g=0.4333`, `lambda=0.01` liegt weit
    ausserhalb der Schwelle `0.009901`.
  - Die komplexe Mode rotiert im Zustandsraum `(x_-,m_-)`, nicht automatisch
    im ambienten Raum. Der Befund ist kein Ladungs-, Flavor- oder
    `d=3`-Resultat.
- [Reziprokes Vollknoten-Gate](response/reciprocal/reciprocal_full_knot_gate_2026-08-04.md)
  - **negative fuer komplexe Mode, supported fuer direkte Bindung:** Alle 60
    post-transienten 2x2-Segmentfits aus Channel-off, One-way und reziprok
    bleiben reell; kein Arm besitzt einen Kandidatenseed.
  - **Kontrolliert:** Kanal-aus ist bitgenau, reziproke Response und
    Shape-Huelle bestehen 5/5. Der Endabstand ist reziprok `0.31..0.88 R`
    gegen `2.78..9.21 R` ohne Kanal. Die fuenf Zukunftsrauschpfade stammen
    jedoch aus nur einem `N=100M`-Formationscheckpoint.
- [Same-law-Jacobian-Audit](response/reciprocal/same_law_reciprocal_jacobian_audit_2026-08-11.md)
  - **inconclusive at the checkpoint gain:** Bei `eta=0.15` bleiben alle
    Vollmatrixmoden reell; `C-G` wechselt ueber die festen Distanzen das
    Vorzeichen. Die Hessians werden direkt aus vollstaendigen reifen
    Memory-Zustaenden berechnet, nicht aus einer Frequenzanpassung.
- [Same-law-Common-Scale-Folgeaudit](response/reciprocal/same_law_common_scale_followup_2026-08-11.md)
  - **conditional local eligibility:** Ein gemeinsames Self-/Cross-Eta besitzt
    bei `R=sigma_rep` das dimensions- und richtungsuebergreifende
    Stable-Complex-Intervall `0.0009965..0.0026549`; der feste Mittelpunkt
    besteht 13/13 Vollmatrixfaelle. Das ist lokale Kruemmung, keine
    stationaere oder persistente Schwingung.
- [Same-law-Affinbilanz-Gate](response/reciprocal/same_law_affine_balance_gate_2026-08-11.md)
  - **negative:** Kein komplex-eligibler Abstand ist kraftbilanziert (`0/13`
    je Abstand). Im kompakten Punktgrenzfall schliessen sich
    Self-Konfinierung und endlicher Pair-Kraftnullpunkt desselben
    Zweigauss-Kernels analytisch aus. Kein Low-g-Pilot oder Parameter-Retuning.
- [N100M-Referenzzustaende](reference_states/scalar_reference_checkpoints_N100M_2026-07-16.md)
  - **supported:** checksum-validierte Absprungbasis der implementierten
    finite-memory Approximation.
- [Weak-Probe-Kalibrierung](response/calibration/weak_probe_calibration_2026-07-16.md)
  - **negative:** Zentrumantwort ist isotrop voll ambient-rangig.
- [Frozen-Source-Feldaudit](response/calibration/frozen_source_field_audit_2026-07-17.md)
  und [Distanzleiter](response/calibration/frozen_source_distance_ladder_2026-07-17.md)
  - **supported:** positiver skalarer Punktmonopolkanal; keine interne Ladung
    oder Dimensionsselektion.
- [Signierter Cross-Channel](response/scalar/signed_scalar_cross_channel_pilot_2026-07-18.md)
  - **pipeline-only:** Null-, Produkt- und Label-Flip-Arme bestehen;
    Labels sind extern und unabhaengige Formationszustaende fehlen.
- [One-Way-Launch](response/one_way/one_way_launched_source_pilot_2026-07-20.md)
  - **negative:** Source bleibt radiusbeschraenkt, aber nicht durchgehend
    formkohaerent; Targetantwort bleibt sehr klein.
- [Interaction-Age bis N103M](response/one_way/one_way_interaction_age_N3M_2026-07-21.md)
  - **negative:** lineare Zentrumtranslation, `0/5` kontrollgetrennte
    Formmodifikation und keine wechselwirkungsinduzierte Oszillation.
- [Skalarer Cross-Readout-Aufloesungstest](response/scalar/scalar_cross_readout_resolution_2026-07-21.md)
  - **negative + pipeline-only:** Selbst- und Cross-Kernel sind getrennt und
    kalibriert; der 1%-Orientierungsschwellenwert wird in `d=3/10` vor der
    Distanzgrenze nicht erreicht.
- [Geordneter History-Current-Audit](response/one_way/oriented_history_current_audit_2026-07-21.md)
  - **negative + pipeline-only:** Weder polarer Verschiebungsstrom noch
    antisymmetrische Zirkulation ueberschreiten in `d=3/10` die konditionale
    99%-Random-Sign-Null; je ein Checkpoint pro Einbettung.
- [Source-lokales Vollmemory-Gate](response/oriented/oriented_memory_source_eligibility_gate_2026-08-07.md)
  - **negative:** Die Polarisation liegt in allen sechs reifen d=3-Sources
    ueber der depositweisen q99-Random-Sign-Null (Faktor 3.42..4.49), verliert
    aber ihre spaete Achsenidentitaet; Gesamtpass 0/6.
  - Der antisymmetrische Zirkulations-Bivektor bleibt in allen Seeds unter
    derselben Null (Faktor 0.54..0.76); ebenfalls 0/6. Alle Source-Shape-Bounds
    bestehen. Passive persistente Orientierung ist damit ein gerichteter
    Kanalinput, aber kein stabiler intrinsischer Spin-/Zirkulationskandidat.
- [Eigenstaendiger orientierter One-Way-Kanal](response/oriented/oriented_vector_one_way_gate_2026-07-25.md)
  - **supported, model-conditional:** Das vorregistrierte Gate besteht in 6/6
    `d=3`-Formationsseeds. Persistent/random-q95 liegt bei `5.76..11.64`, der
    Ein-Schritt-Arm bei `1.40..2.04`, entsprechend einem Persistenzgewinn von
    `3.50..8.05`; Flip, Transversalitaet und Shape-Bounds bestehen.
  - Die Orientierung, ihr Zerfall und das instantane direkte Readout sind
    Modellinputs. Die stateweise Antwortnormalisierung und geklonten
    Source/Target-Zustaende erlauben noch keinen Propagations-, Wellen- oder
    Teilchenclaim.
- [Feste-Kopplung-/Distanzgate](response/oriented/oriented_vector_fixed_pair_distance_gate_2026-07-26.md)
  - **supported, model-conditional:** 6/6 zyklisch verschiedene Source/Target-
    Paare bestehen bei globalem `eta_v=5.079e-6` Nahantwort, Random-Sign-Null,
    Persistenz, Flip, Shape-Huelle und Distanzgate. Fern/Nah liegt bei
    `9.36e-4..2.80e-3`.
  - Das instantane Gauss-Readout und `sigma_v=2.5 R_source` sind gesetzt und
    erzeugen den Distanzabfall. Der Befund ist keine emergente Lokalitaets-,
    Propagations-, QFT- oder Teilchenevidenz.
- [Lokales Mediator-Holdout-Gate](response/oriented/local_oriented_mediator_gate_2026-07-28.md)
  - **pipeline-only, mechanism underdetermined:** Relaxations-Diffusion und
    Telegraph bestehen je `5/5` Holdout-Paare, die vorab festgelegten Lag- und
    Aufloesungsgates sowie Shape-/Flip-Kontrollen.
  - Die Transportgesetze sind Modellinputs. Der Pass validiert lokale
    Markov-Erweiterungen und feste Kopplung, entdeckt aber weder ein
    Propagationsgesetz noch endliche Kausalgeschwindigkeit oder `d=3`.
- [Autonome Source-/Mediator-Identifizierbarkeit](response/oriented/oriented_source_mediator_identifiability_2026-07-28.md)
  - **pipeline-only, source eligible:** 6/6 geerbte Sources bestehen das
    vorregistrierte Zwei-Segment-Gate an allen 18 Distanzen. Minimaler
    sourcegewichteter komplexer Kontrast `1.064`, unterscheidbarer
    Output-Leistungsanteil mindestens `0.9969`, Segmentdrift maximal `0.1568`.
  - Persistenter/Ein-Schritt-Kontrast liegt jedoch nur bei `0.951..1.008`
    (Median `0.991`). Der Pass zeigt Breitband-Identifizierbarkeit der bewusst
    verschiedenen Regeln, nicht spezifische Evidenz fuer Vektorpersistenz,
    ein physikalisches Feldgesetz oder `d=3`.
- [Dynamisches Common-Source-Mediator-Gate](response/oriented/dynamic_common_source_mediator_gate_2026-07-28.md)
  - **negative, mechanism underdetermined:** Beide Regeln bestehen in 6/6
    Paaren Response-Fenster, Oddness, Source-/Target-Shape und
    Distanzabschwachung. Die vorregistrierte relative Trace-Trennung besteht
    jedoch nur fuer 4/6 statt 5/6 Paare gleichzeitig an allen drei Distanzen.
  - Im Nahfeld bestehen 4/6 Paare (`Delta_DT` Minimum `0.1874`), bei `5` und
    `10 R_pair` jeweils 6/6. Das Resultat rechtfertigt weder Retuning noch die
    Auswahl eines physikalischen Transportgesetzes; Reziprozitaet und `d=3`
    bleiben gesperrt.

- [Direktes reziprokes Vollknotengate](response/reciprocal/reciprocal_full_knot_gate_2026-08-04.md)
  - **negative mode gate, active binding:** Alle 60 rohen Segmentfits bleiben
    reell; Response und Shape-Huelle bestehen 5/5. Der direkte Endabstand liegt
    bei `0.31..0.88R` gegen Kanal-aus `2.78..9.21R`.
- [Retardiertes reziprokes Vollknotengate](response/reciprocal/retarded_reciprocal_full_knot_gate_2026-08-04.md)
  - **negative mode gate, operational channel:** Der feste DC-gematchte
    Telegraph-Arm besteht Mediator, Response und Shape 5/5, aber alle 80 rohen
    Segmentfits sind reell. Retardiert reziprok endet bei `0.58..1.21R` und
    bindet damit im Beobachtungsfenster schwaecher oder spaeter als direkt.
  - Der Eingang bleibt ein zielabhaengiger momentaner Cross-Gradient. Nur der
    Transportfilter ist lokal; keine quelllokale Feldtheorie oder physische
    Signalgeschwindigkeit ist gezeigt.

- [Mess-Closure und relative Rauschfalsifikation](response/reciprocal/measurement_closure_relative_noise_gate_2026-08-04.md)
  - **predictive closure, augmented spectrum non-identifiable:** Der sichtbare
    Delayzustand ist in 9/9 Faellen gut konditioniert und ohne stabiles
    komplexes Segmentmatching. Feld plus Impuls bringen hoechstens `0.20%`
    Holdout-Gewinn, aber Konditionszahlen um `1e16`.
  - Feste Knotenmarginalen und `rho={0,0.9,0.99}` bestaetigen die erwartete
    relative Rauschleiter. Kleinere relative Diffusion bindet staerker, legt
    aber keinen kontrollgetrennten Modus frei.
- [Vorregistrierung des Langhorizont-/Hankel-Audits](project/meta/preregistration/long_horizon_hankel_preregistration_2026-08-04.md)
- [Langhorizont-/Hankel-Ergebnis](response/reciprocal/long_horizon_hankel_gate_2026-08-04.md)
  - **negative long-history closure trend:** Alle 45 gepaarten Designzellen und
    alle drei unabhaengigen Seed-Mediane sind positiv; Zellmedian `+0.1203` von
    1000 auf 12500 Updates. Der effektive Rang waechst ohne Plateau,
    Feld/Impuls hilft nicht, und Rang 16/32 ist nicht kontrollgetrennt.
- [Vorregistrierung des DMD-Pol-Identity-Stoptests](project/meta/preregistration/hankel_pole_identity_preregistration_2026-08-04.md)
- [DMD-Pol-Identity-Ergebnis](response/reciprocal/hankel_pole_identity_audit_2026-08-06.md)
  - **kein kontrollgetrennter Pol:** Seeds 1/2 tragen einen Kandidaten um
    `omega=0.103`, doch 6..8/12 Einwegzellen enthalten denselben Pol; Seed 3
    erreicht nur 9/12 reziprok. Vier korrelationsuebergreifende Kandidaten,
    null Ueberlebende des Kontrollgates.

- [P3.2-Code-/Artefaktreview](project/meta/reviews/p32_relevant_code_review_2026-08-06.md)
- [Vorregistrierung der 500k-Akkumulationskontrolle](project/meta/preregistration/p32_accumulation_control_preregistration_2026-08-06.md)
- [P3.2-500k-Akkumulationskontrolle](response/reciprocal/p32_accumulation_control_N500k_2026-08-06.md)
  - **kein kontrollgetrennter Akkumulationseffekt:** Die reziproken
    late-minus-early Abweichungen `19.14R/10.51R` werden durch die
    Einwegkontrolle `19.03R/10.31R` erklaert; beide Shapes bleiben gueltig.

- [P3.2d-Vorregistrierung: Shape-Multipol](project/meta/preregistration/p32d_shape_multipole_preregistration_2026-08-06.md)
- [P3.2d-Ergebnis: Shape-Multipol](response/source_local/p32d_shape_multipole_gate_2026-08-06.md)
  - **kein kontrollgetrennter autonomer Shape-Modus:** `Q` und
    `Delta Q/Delta tau` bestehen in `0/5` Baseline-Pfaden; der langsame
    `Q`-Peak ist segmentinstabil und in `eta=0` staerker.
- [Review der relevanten Dynamik- und Modenmodule](project/meta/reviews/relevant_dynamics_code_review_2026-08-04.md)
  - **correctness + method boundary:** Ein Fixed-Effects-Fehler des isotropen
    `2 x 2`-Fits ist behoben. Saubere Reproduktionen bleiben bei `0/60` und
    `0/80` nichtreellen Segmentfits; der Befund gilt nur fuer den registrierten
    AR(1)-Readout, nicht fuer den verborgenen augmentierten Telegraph-Zustand.
  - P3.2a/b bestaetigt sichtbare Delay-Closure ohne Modenpass und verwirft
    Rausch-Unmasking. Das augmentierte Feld-/Impulsspektrum bleibt wegen
    Rangdefizienz unbestimmt; naechster Schritt ist Reduced-Rank, kein Sweep.

Entscheidung: Direkter und fest retardierter Skalararm zeigen kontrollierte
Bindung/Relaxation. Der sichtbare Delayzustand bleibt ohne komplexen Modenpass;
das augmentierte Spektrum ist nicht identifizierbar. Weitere Gain-Suche ist
nicht priorisiert. Langhorizont und Pol-Identity sind negativ. Ein spaeter
ausgefuehrter 500k-Akkumulationskontrolllauf bleibt ebenfalls negativ, weil
der Einwegarm dieselbe sensitive Pfaddivergenz zeigt. P3.2 bleibt geschlossen.
P3.2c erzwingt nun echte Source-Lokalitaet,
bleibt aber ebenfalls negativ: Der Offset laedt nur `3.54e-5` normiertes
Knot-Residuum in den stabilen Telegraphpol, der Schrittstrom noch weniger.
P3.2d ist ebenfalls negativ: Der autonome spurlose Shape-Tensor hat keinen
segmentstabilen, gegen `eta=0` getrennten Modus; seine Aenderung ebenfalls
nicht. Eine Tensor-Mediatorregel ist nicht autorisiert. Als naechstes wird die
explizite Vektormemory-Erweiterung formal gehaertet, bevor neue
Mechanismussimulationen beginnen. P3.3 bleibt gesperrt. Der komponentenweise
Vektormediator besitzt weiterhin
nur den Ambient-Transfer `H I_d` und keinen Mechanismus fuer eindeutige
Rang-drei-Selektion; der negative dynamische Holdout waehlt keines der beiden
eingesetzten Transportgesetze.

### 5. Governance und Kuration

- [Privacy and Control Plan](project/governance/privacy_and_control_plan_2026-07-08.md)
- [Repository-Cleanup 2026-07-09](project/meta/operations/repository_cleanup_2026-07-09.md)
- [Dynamik-/Moden-Code-Review 2026-08-04](project/meta/reviews/relevant_dynamics_code_review_2026-08-04.md)
- [P3.8 Physik-/Code-Review 2026-08-12](project/meta/reviews/p38_rigorous_review_2026-08-12.md)
- [Repository-Kuration 2026-07-21](project/meta/operations/repository_curation_2026-07-21.md)

## Historische Bereiche

- `kernels/corrected_sign/`: dokumentiert die Vorzeichenkorrektur und ihre
  Folgen.
- `long_runs/` und `knot_scores/`: enthalten auch fruehere Score- und
  Residence-Lesarten; vor der Signkorrektur nur als `legacy-sign` lesen.
- `dimensions/fractal_archive/` und `dimensions/reproduction/`: historische
  Dimensionspfade und Reproduktionsaudits.
- `vector_memory/`: fruehe orientierte Piloten; komplexe Moden treten bereits
  in Kontrollen auf.
- `project/`: Entscheidungen, Governance, Paper- und Repository-Audits.

## Aufnahmeregeln

Ein neuer Report wird nur committed, wenn er mindestens nennt:

1. Hypothese und Status (`supported`, `negative`, `inconclusive` oder
   `pipeline-only`).
2. Parameter, Seeds, Git-Revision und Arbeitsbaumstatus.
3. Negativkontrolle und primaere Observable.
4. Lauflaenge, Burn-in, Sampling und Runtime.
5. Pfad zur maschinenlesbaren Summary, sofern vorhanden.
6. Claim-Grenze und naechste falsifizierende Entscheidung.

Neue Reports werden hier nur dann in die aktive Evidenzschiene aufgenommen,
wenn sie eine Projektentscheidung aendern. Andernfalls bleiben sie datierte
Auditspur.
