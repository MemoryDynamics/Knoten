# Report-Index

Stand: 2026-07-21.

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
- [Long-Run-Reconciliation](long_runs/scalar_hardening/linear_long_run_reconciliation_2026-07-19.md)
  - **supported:** neun aktive `N=30M/300M`-Slices folgen dem linearen
    Finite-Memory-Radius bis maximal `1.16%` relativ.
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

Entscheidung: Shape-, Sample- und Heat-Trace-Dimension sind getrennte
Diagnostiken. Die vorhandenen Daten stuetzen keine ambient-unabhaengige
`d=3`-Selektion.

### 3. Memory-Feld und reduzierte Moden

- [Spektrale rho-Reprasentation](memory/spectral_rho_field_pilot_2026-07-19.md)
  - **structural + pipeline-only:** Historie, Masse, Kontraktion und Kraft sind fuer
    die getestete 1D-Reprasentation reconciliiert.
- [Relaxations-Diffusionsfeld](memory/relaxation_diffusion_field_pilot_2026-07-19.md)
  - **supported:** modeabhaengige Glaettung ist kontrolliert; kein
    Propagations- oder Metastabilitaetsclaim.
- [Mode-Identity-Audit](memory/low_mode_identity_audit_2026-07-20.md)
  - **negative:** weder ein stabiler einzelner Realmodus noch ein
    feedback-spezifischer komplexer Modus besteht das Segment-/Kontrollgate.

Entscheidung: Niedrige Moden sind nuetzliche Rechenfeatures, derzeit keine
identifizierten physikalischen Moden.

### 4. Referenzzustaende und externe Antwort

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

Entscheidung: Reziproke Kopplung bleibt gesperrt. Als naechster Mechanismus
wird orientiertes Vektor-/Strommemory vorregistriert. Ein lokaler/retardierter
Skalarmediator bleibt fuer eine getrennte Lokalitaetsfrage zurueckgestellt.

### 5. Governance und Kuration

- [Privacy and Control Plan](project/governance/privacy_and_control_plan_2026-07-08.md)
- [Repository-Cleanup 2026-07-09](project/meta/repository_cleanup_2026-07-09.md)
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
