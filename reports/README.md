# Report-Index

Stand: 2026-08-04.

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
- [Checkpoint-/Holdout-Stabilitaetsgate](long_runs/stability/checkpoint_stability_gate_d10_A35_2026-07-30.md)
  - **supported, method-conditional:** 5/5 `d=10`, `A_att=35`-Seeds bestehen
    vier Alterscheckpoints bis `N=30M`, lokale Radiusfenster und den
    `N=300M`-Holdout. Keine erste Formationszeit, keine zeitaufgeloeste
    Shape-Stationaritaet und kein Teilchenclaim.
- [Feste-g-Skalenpruefung](kernels/nonlinearity/fixed_g_scale_reconciliation_d3_N300k_A26_2026-07-19.md)
  - **inconclusive:** kleine Superlinearitaet, aber kein Shape-Umschlag;
    Residence- und Score-Metriken sind auf dieser Radiusachse nicht
    diskriminierend.

Entscheidung: Das skalare Modell bleibt kontrollierte lineare Baseline. Keine
weitere reine Amplituden- oder Epsilon-Suche ohne neue Mechanismushypothese.

### 2. Dimension

- [Dimensionsclaim-Audit](dimensions/dimension_claim_audit_2026-07-15.md)
- [D_spec-Sensitivitaet](dimensions/dspec_sensitivity_2026-07-15.md)
- [Rohsnapshot-Retest](dimensions/dspec_raw_snapshot_retest_2026-07-16.md)
- [Dimensionen ueber N](dimensions/dimension_over_n_d10_A35_2026-07-30.md)
  - **reproduced, measurement convergence not evaluable:** `D_mem` bleibt fuer
    drei gematchte Seeds bei `8.857..9.268`; `D_cov` ist nichtmonoton. Das neue
    D_occ/D_win-Gate scheitert bereits an Trainingsrange/-trend und ist wegen
    Cadence-/Revisionswechsel sowie fruehen ungueltigen D_win-Fits nicht
    auswertbar. Der sichtbare Trend ist keine zertifizierte N-Abhaengigkeit.

Entscheidung: Shape-, Sample- und Heat-Trace-Dimension sind getrennte
Diagnostiken. Die vorhandenen Daten stuetzen keine ambient-unabhaengige
`d=3`-Selektion.

### 3. Memory-Feld und reduzierte Moden

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
- [Aktives skalares Delta-Quellfeld](kernels/field/active_scalar_delta_field_pilot_2026-07-31.md)
  - **supported, model-conditional:** Zeit-/Gitter-, cubic-off- und source-off-
    Gates bestehen; der kubisch gesaettigte aktive Arm bildet in drei Seeds
    einen beschraenkten Peak bei `k=1`.
  - `eta=0` traegt nahezu dasselbe Feld. Der Pass gilt fuer klassische
    Finite-k-Musterbildung, nicht fuer einen feedback-spezifischen Knoten,
    Quantisierung, QFT oder `d=3`.
- [Spektrale rho-Reprasentation](memory/spectral_rho_field_pilot_2026-07-19.md)
  - **structural + pipeline-only:** Historie, Masse, Kontraktion und Kraft sind fuer
    die getestete 1D-Reprasentation reconciliiert.
- [Relaxations-Diffusionsfeld](memory/relaxation_diffusion_field_pilot_2026-07-19.md)
  - **supported:** modeabhaengige Glaettung ist kontrolliert; kein
    Propagations- oder Metastabilitaetsclaim.
- [Mode-Identity-Audit](memory/low_mode_identity_audit_2026-07-20.md)
  - **negative:** weder ein stabiler einzelner Realmodus noch ein
    feedback-spezifischer komplexer Modus besteht das Segment-/Kontrollgate.
- [Eta-zero-Rohmoden-Null](memory/eta_zero_raw_mode_null_audit_2026-07-31.md)
  - **structural + negative:** Der rohe Fourier-Zustandsblock besitzt exakt
    nur reelle Multiplikatoren. Bei archivierter N=1M-Kadenz bleiben gepoolte
    und seedweise Fits reell; kleine Segmentleckage erreicht maximal
    `7.25e-4` Frequenz pro Memory-Zeit.
  - Die ausgerichteten komplexen AR-Paare werden damit als Darstellungs- und
    Fitmoden klassifiziert, nicht als physikalische Oszillation.

Entscheidung: Niedrige Moden sind nuetzliche Rechenfeatures, derzeit keine
identifizierten physikalischen Moden.

### 4. Referenzzustaende und externe Antwort

- [Reziprokes lokales Modengate](response/reciprocal_local_mode_gate_2026-08-04.md)
  - **structural:** Common-/Relative-Mode-Zerlegung und voller
    Vier-Zustands-Matrixabgleich ergeben ein stabiles komplexes Fenster nur
    fuer `g < lambda/(1+lambda)`; innerhalb des Fensters ist `c > g`
    notwendig. Die kompakte Baseline `g=0.4333`, `lambda=0.01` liegt weit
    ausserhalb der Schwelle `0.009901`.
  - Die komplexe Mode rotiert im Zustandsraum `(x_-,m_-)`, nicht automatisch
    im ambienten Raum. Der Befund ist kein Ladungs-, Flavor- oder
    `d=3`-Resultat.
- [Reziprokes Vollknoten-Gate](response/reciprocal_full_knot_gate_2026-08-04.md)
  - **negative fuer komplexe Mode, supported fuer direkte Bindung:** Alle 60
    post-transienten 2x2-Segmentfits aus Channel-off, One-way und reziprok
    bleiben reell; kein Arm besitzt einen Kandidatenseed.
  - **Kontrolliert:** Kanal-aus ist bitgenau, reziproke Response und
    Shape-Huelle bestehen 5/5. Der Endabstand ist reziprok `0.31..0.88 R`
    gegen `2.78..9.21 R` ohne Kanal. Die fuenf Zukunftsrauschpfade stammen
    jedoch aus nur einem `N=100M`-Formationscheckpoint.
- [N100M-Referenzzustaende](reference_states/scalar_reference_checkpoints_N100M_2026-07-16.md)
  - **supported:** checksum-validierte Absprungbasis der implementierten
    finite-memory Approximation.
- [Weak-Probe-Kalibrierung](response/weak_probe_calibration_2026-07-16.md)
  - **negative:** Zentrumantwort ist isotrop voll ambient-rangig.
- [Frozen-Source-Feldaudit](response/frozen_source_field_audit_2026-07-17.md)
  und [Distanzleiter](response/frozen_source_distance_ladder_2026-07-17.md)
  - **supported:** positiver skalarer Punktmonopolkanal; keine interne Ladung
    oder Dimensionsselektion.
- [Signierter Cross-Channel](response/signed_scalar_cross_channel_pilot_2026-07-18.md)
  - **pipeline-only:** Null-, Produkt- und Label-Flip-Arme bestehen;
    Labels sind extern und unabhaengige Formationszustaende fehlen.
- [One-Way-Launch](response/one_way_launched_source_pilot_2026-07-20.md)
  - **negative:** Source bleibt radiusbeschraenkt, aber nicht durchgehend
    formkohaerent; Targetantwort bleibt sehr klein.
- [Interaction-Age bis N103M](response/one_way_interaction_age_N3M_2026-07-21.md)
  - **negative:** lineare Zentrumtranslation, `0/5` kontrollgetrennte
    Formmodifikation und keine wechselwirkungsinduzierte Oszillation.
- [Skalarer Cross-Readout-Aufloesungstest](response/scalar_cross_readout_resolution_2026-07-21.md)
  - **negative + pipeline-only:** Selbst- und Cross-Kernel sind getrennt und
    kalibriert; der 1%-Orientierungsschwellenwert wird in `d=3/10` vor der
    Distanzgrenze nicht erreicht.
- [Geordneter History-Current-Audit](response/oriented_history_current_audit_2026-07-21.md)
  - **negative + pipeline-only:** Weder polarer Verschiebungsstrom noch
    antisymmetrische Zirkulation ueberschreiten in `d=3/10` die konditionale
    99%-Random-Sign-Null; je ein Checkpoint pro Einbettung.
- [Eigenstaendiger orientierter One-Way-Kanal](response/oriented_vector_one_way_gate_2026-07-25.md)
  - **supported, model-conditional:** Das vorregistrierte Gate besteht in 6/6
    `d=3`-Formationsseeds. Persistent/random-q95 liegt bei `5.76..11.64`, der
    Ein-Schritt-Arm bei `1.40..2.04`, entsprechend einem Persistenzgewinn von
    `3.50..8.05`; Flip, Transversalitaet und Shape-Bounds bestehen.
  - Die Orientierung, ihr Zerfall und das instantane direkte Readout sind
    Modellinputs. Die stateweise Antwortnormalisierung und geklonten
    Source/Target-Zustaende erlauben noch keinen Propagations-, Wellen- oder
    Teilchenclaim.
- [Feste-Kopplung-/Distanzgate](response/oriented_vector_fixed_pair_distance_gate_2026-07-26.md)
  - **supported, model-conditional:** 6/6 zyklisch verschiedene Source/Target-
    Paare bestehen bei globalem `eta_v=5.079e-6` Nahantwort, Random-Sign-Null,
    Persistenz, Flip, Shape-Huelle und Distanzgate. Fern/Nah liegt bei
    `9.36e-4..2.80e-3`.
  - Das instantane Gauss-Readout und `sigma_v=2.5 R_source` sind gesetzt und
    erzeugen den Distanzabfall. Der Befund ist keine emergente Lokalitaets-,
    Propagations-, QFT- oder Teilchenevidenz.
- [Lokales Mediator-Holdout-Gate](response/local_oriented_mediator_gate_2026-07-28.md)
  - **pipeline-only, mechanism underdetermined:** Relaxations-Diffusion und
    Telegraph bestehen je `5/5` Holdout-Paare, die vorab festgelegten Lag- und
    Aufloesungsgates sowie Shape-/Flip-Kontrollen.
  - Die Transportgesetze sind Modellinputs. Der Pass validiert lokale
    Markov-Erweiterungen und feste Kopplung, entdeckt aber weder ein
    Propagationsgesetz noch endliche Kausalgeschwindigkeit oder `d=3`.
- [Autonome Source-/Mediator-Identifizierbarkeit](response/oriented_source_mediator_identifiability_2026-07-28.md)
  - **pipeline-only, source eligible:** 6/6 geerbte Sources bestehen das
    vorregistrierte Zwei-Segment-Gate an allen 18 Distanzen. Minimaler
    sourcegewichteter komplexer Kontrast `1.064`, unterscheidbarer
    Output-Leistungsanteil mindestens `0.9969`, Segmentdrift maximal `0.1568`.
  - Persistenter/Ein-Schritt-Kontrast liegt jedoch nur bei `0.951..1.008`
    (Median `0.991`). Der Pass zeigt Breitband-Identifizierbarkeit der bewusst
    verschiedenen Regeln, nicht spezifische Evidenz fuer Vektorpersistenz,
    ein physikalisches Feldgesetz oder `d=3`.
- [Dynamisches Common-Source-Mediator-Gate](response/dynamic_common_source_mediator_gate_2026-07-28.md)
  - **negative, mechanism underdetermined:** Beide Regeln bestehen in 6/6
    Paaren Response-Fenster, Oddness, Source-/Target-Shape und
    Distanzabschwachung. Die vorregistrierte relative Trace-Trennung besteht
    jedoch nur fuer 4/6 statt 5/6 Paare gleichzeitig an allen drei Distanzen.
  - Im Nahfeld bestehen 4/6 Paare (`Delta_DT` Minimum `0.1874`), bei `5` und
    `10 R_pair` jeweils 6/6. Das Resultat rechtfertigt weder Retuning noch die
    Auswahl eines physikalischen Transportgesetzes; Reziprozitaet und `d=3`
    bleiben gesperrt.

- [Direktes reziprokes Vollknotengate](response/reciprocal_full_knot_gate_2026-08-04.md)
  - **negative mode gate, active binding:** Alle 60 rohen Segmentfits bleiben
    reell; Response und Shape-Huelle bestehen 5/5. Der direkte Endabstand liegt
    bei `0.31..0.88R` gegen Kanal-aus `2.78..9.21R`.
- [Retardiertes reziprokes Vollknotengate](response/retarded_reciprocal_full_knot_gate_2026-08-04.md)
  - **negative mode gate, operational channel:** Der feste DC-gematchte
    Telegraph-Arm besteht Mediator, Response und Shape 5/5, aber alle 80 rohen
    Segmentfits sind reell. Retardiert reziprok endet bei `0.58..1.21R` und
    bindet damit im Beobachtungsfenster schwaecher oder spaeter als direkt.
  - Der Eingang bleibt ein zielabhaengiger momentaner Cross-Gradient. Nur der
    Transportfilter ist lokal; keine quelllokale Feldtheorie oder physische
    Signalgeschwindigkeit ist gezeigt.

- [Review der relevanten Dynamik- und Modenmodule](project/meta/relevant_dynamics_code_review_2026-08-04.md)
  - **correctness + method boundary:** Ein Fixed-Effects-Fehler des isotropen
    `2 x 2`-Fits ist behoben. Saubere Reproduktionen bleiben bei `0/60` und
    `0/80` nichtreellen Segmentfits; der Befund gilt nur fuer den registrierten
    AR(1)-Readout, nicht fuer den verborgenen augmentierten Telegraph-Zustand.
  - Ein roher Epsilon-/Lambda-Sweep ist verworfen. Naechste Gates sind
    Mess-Closure und eine Rauschkorrelationsvariation bei festen
    Einzelknoten-Marginalen.

Entscheidung: Direkter und fest retardierter Skalararm bestaetigen die
Realmoden-Null bei kontrollierter Bindung/Relaxation. Weitere Gain-Suche ist
nicht priorisiert. P3.2a prueft zuerst die Mess-Closure des verborgenen
Mediatorzustands; danach folgt die relative Rauschfalsifikation bei festen
Einzelknoten-Marginalen. Erst dann kommt eine quelllokale Emissionsregel.
P3.3 bleibt gesperrt. Der komponentenweise Vektormediator besitzt weiterhin
nur den Ambient-Transfer `H I_d` und keinen Mechanismus fuer eindeutige
Rang-drei-Selektion; der negative dynamische Holdout waehlt keines der beiden
eingesetzten Transportgesetze.

### 5. Governance und Kuration

- [Privacy and Control Plan](project/governance/privacy_and_control_plan_2026-07-08.md)
- [Repository-Cleanup 2026-07-09](project/meta/repository_cleanup_2026-07-09.md)
- [Dynamik-/Moden-Code-Review 2026-08-04](project/meta/relevant_dynamics_code_review_2026-08-04.md)
- [Repository-Kuration 2026-07-21](project/meta/repository_curation_2026-07-21.md)

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
