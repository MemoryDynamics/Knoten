# Evidenz-Ledger: native rotating waves

Stand: 2026-08-26.

Dieses Verzeichnis ist das kanonische Artefaktledger des raeumlichen
Schleifenasts. Markdown-Dateien sind lesbare Reviews oder Reports; JSON-Dateien
sind die autoritativen maschinenlesbaren Entscheidungen.

## Entscheidungskette

1. `scalar_memory_rotating_wave_discovery_2026-08-20.{md,json}`
   - `finite-h-rotating-wave-candidate-found`;
   - ein Gleitkomma-Residualroot und unabhaengiger Produktionskernelcheck;
   - noch keine zertifizierte Existenz oder Stabilitaet.
2. `scalar_memory_rotating_wave_initial_state_spec_2026-08-20.json`
   - vollstaendige vorbereitete Kreisgeschichte fuer den Anchor.
3. `scalar_memory_rotating_wave_stability_2026-08-20.{md,json}`
   - `numerically-stable-source-pass` am Anchor;
   - lokale numerische, nicht vollstaendig spektralzertifizierte Aussage.
4. `scalar_memory_rotating_wave_interval_certificate_2026-08-21.{md,json}`
   - `interval-certified-unique-root-pass` in der registrierten lokalen Box.
5. `scalar_memory_rotating_wave_refinement_ladder_2026-08-21.{md,json}`
   - fuenf lokal zertifizierte Roots und Anchor-Ueberlapp;
   - formale historische Entscheidung `certified-roots-nonconvergent`, weil
     der eingefrorene Kontinuumsguide Gain 15.016345 statt 15 besass.
6. `scalar_memory_rotating_wave_continuum_reconciliation_2026-08-21.{md,json}`
   - `fixed-gain-continuum-reconciliation-pass`;
   - bewahrt die historische Leiterentscheidung explizit.
7. `scalar_memory_rotating_wave_foundation_audit_initial_implementation_fail_2026-08-21.{md,json}`
   - historischer Pipeline-Fail durch falschen binaeren Gleichheitstest;
   - vier von fuenf Composite-Gates und alle wissenschaftlichen finite-Summen-
     Kontrollen bestanden bereits;
   - der positive Markdown-Absatz wurde im alten Renderer faelschlich ohne
     Entscheidungsbedingung ausgegeben; die JSON-Failentscheidung ist autoritativ.
8. Versionierter Zwischenstand in Commit
   `68e926e93452242b9444d0fdbaacad51b8947dd9`
   - lokaler `foundation-audit-reconciliation-pass-scoped` nach exakter
     Dezimalkorrektur und vollstaendigem Re-Run;
   - nicht der aktuelle Abschluss: Linux-CI zeigte danach sechs
     arbeitsbaumabhaengige CRLF-Hashes und fehlende Historie im Shallow-Clone.
9. `scalar_memory_rotating_wave_foundation_audit_2026-08-21.{md,json}`
   - `foundation-audit-portability-reconciliation-pass-scoped` nach einem
     zweiten, separat eingefrorenen Portabilitaetsprotokoll;
   - alle A--E-Gates aus sauberem Commit neu gerechnet; aktuelle
     reviewertragende Foundation-Entscheidung.
10. `scalar_memory_rotating_wave_l5_existence_scaling_2026-08-21.{md,json}`
    - `l5-existence-scaling-pass` aus dem vorab publizierten Protokoll- und
      getrennten sauberen Ausfuehrungs-Commit;
    - sechster lokaler Krawczyk-Root, unabhaengiger finite-Summen-Replay und
      alle signierten First-order-Skalierungsgates ohne Retuning bestanden.
11. `scalar_memory_rotating_wave_l3_stability_2026-08-22.{md,json}`
    - `numerically-stable-source-pass` aus separat publiziertem Freeze- und
      Implementierungscommit;
    - zwei unterschiedliche Arnoldi-Panels stimmen bei
      \(|\lambda_\perp|=0.99649340\) ueberein, und sechs gespiegelte
      Stoerungsarme kontrahieren ueber 10000 Updates;
    - lokale numerische L3-Evidenz, keine vollstaendige Spektraleinschliessung
      oder stabile Familie.
12. `scalar_memory_loop_center_p2_2026-08-25.{md,json}`
    - `loop-center-matrix-local-fail` aus separat publiziertem Audit-, Freeze-
      und Implementierungscommit;
    - alle Kontrollen, Tangentenfehler, quadratischen Resttermgates und
      Amplitudenkollapse bestehen mit grosser Marge;
    - alle acht Response-Zeilen verfehlen ausschliesslich die absolute
      Tail-Slope-Grenze, obwohl die gespeicherten Tail-Samples post hoc
      monoton fallen; P3 bleibt in diesem historischen Lauf geschlossen.
13. `scalar_memory_loop_center_p2r_long_recovery_2026-08-25.{md,json}`
    - `p2r-sign-sensitive-long-recovery-pass` aus dem separat publizierten und
      vor weiterem Targetzugriff korrigierten Freeze;
    - exakter Replay aller 120 alten P2-Metriken und acht Checkpoints;
    - alle 48 neuen Fenster zeigen aufgeloeste Rueckkehr bis 20 Memory-Zeiten;
      outcome-informierte Reconciliation, keine Umbenennung des P2-Fails.
14. `scalar_memory_rotating_wave_p3_formation_basin_2026-08-26.{md,json}`
    - `p3-formation-basin-pass` aus separatem Protokoll-, Implementierungs- und
      Ergebniscommit;
    - alle sechs target-informierten und vier target-blinden Arme treten bis
      9.4 Memory-Zeiten ein und verweilen bis Memory-Zeit 60;
    - eta=0 kollabiert, der achirale Arm bleibt exakt kollinear; reviewed nur
      als finite-ensemble attraction, nicht generische Formation.
15. `scalar_memory_loop_p4_source_write_2026-08-26.{md,json}`
    - unveraenderlicher `p4-source-write-architecture-fail` aus getrenntem
      Architektur-, Freeze-, Implementierungs- und Ergebniscommit;
    - der exakte Write-/Age-/Interaktionsledger besteht, waehrend zwei direkt
      subtrahierte Readout-Residuen in allen Armen an einer unter-binary64
      skalierten Grenze scheitern;
    - alle 24 Arme verfehlen unabhaengig die Orthogonalgrenze mit einer
      spiegelkonsistenten chirality-odd Querantwort. Kein P5-, Spin-, Impuls-
      oder Masseclaim.

## Zugehoerige Protokolle und Reviews

Die unveraenderlichen P0-/D0-, Gate- und Reviewdateien liegen unter:

- `reports/project/meta/preregistration/scalar_memory_rotating_wave_*`;
- `reports/project/meta/reviews/scalar_memory_rotating_wave_*`.

Der Foundation-Audit hasht die kanonischen `HEAD:path`-Git-Blobs von
Discovery, Initial State, P0, D0, Stabilitaet, Intervallzertifikat, Leiter und
Kontinuums-Reconciliation bytegenau. Ein sauberer Arbeitsbaum und die
vollstaendige Historie werden separat verlangt. Alte Artefakte duerfen deshalb
nicht still editiert werden.

Der Foundation-Referee-Text ist
`reports/project/meta/reviews/scalar_memory_rotating_wave_foundation_review_2026-08-21.md`.
Das nachgelagerte L5-Urteil steht in
`reports/project/meta/reviews/scalar_memory_rotating_wave_l5_existence_scaling_review_2026-08-21.md`.
Das anschliessende P1-Urteil steht in
`reports/project/meta/reviews/scalar_memory_rotating_wave_l3_stability_review_2026-08-22.md`.
Das P2-Linearisierungs-Audit und der Review des formalen Tail-Fails stehen in
`reports/project/meta/reviews/scalar_memory_loop_center_linearization_audit_2026-08-25.md`
beziehungsweise
`reports/project/meta/reviews/scalar_memory_loop_center_p2_review_2026-08-25.md`.
Das nachgelagerte P2-R-Urteil steht in
`reports/project/meta/reviews/scalar_memory_loop_center_p2r_long_recovery_review_2026-08-25.md`.
Das P3-Urteil steht in
`reports/project/meta/reviews/scalar_memory_rotating_wave_p3_formation_basin_review_2026-08-26.md`.
Das P4-Architekturaudit, Freeze und kritische Ergebnisurteil stehen in
`reports/project/meta/reviews/scalar_memory_loop_p4_actuator_architecture_audit_2026-08-26.md`,
`reports/project/meta/preregistration/scalar_memory_loop_p4_source_write_protocol_2026-08-26.md`
beziehungsweise
`reports/project/meta/reviews/scalar_memory_loop_p4_source_write_review_2026-08-26.md`.
Die Reviews erlauben nur die enge Formulierung „vorbereitete raeumliche
Schleifenbasis mit lokaler numerischer Stabilitaetsevidenz an zwei getesteten
Skalen“. P2 fuegt starke lokale matrixwertige Kleinsignalevidenz hinzu und
bleibt formal gescheitert; P2-R belegt nur die fortgesetzte Rueckkehr derselben
vorbereiteten Kleinsignalarme. P3 erweitert die getestete Attraktion auf zehn
nichtkreisfoermige Arme, bleibt aber ein endliches deterministisches Ensemble.
Der fehlende zweite Intervallbackend und die unvollstaendige
Spektraleinschliessung bleiben ausdruecklich markiert.

## Aktuelle Lesart

Belastbar sind sechs lokal existenzzertifizierte finite-Summen-Rootzellen mit
numerisch reconciliertem First-order-Kontinuumsast. Die Zertifikate bleiben
auf den `mpmath.iv`-Trust-Base konditional; ein unabhaengiger Intervallbackend
fehlt. Anchor und L3 besitzen lokale numerische Stabilitaetsevidenz in ihren
registrierten Panels; daraus folgt keine stabile sechs-zellige Familie. Der
Kreis ist eine ambiente \(SO(2)\)-Gruppenbahn und nach Symmetriereduktion ein
Punkt. Der lokale Loop--Center-Tangentenvergleich ist numerisch stark, aber
sein registriertes Tail-Gate formal fehlgeschlagen. Die outcome-informierte
P2-R-Verlaengerung zeigt danach aufgeloeste Rueckkehr in allen 48 neuen
Fenstern durch 20 Memory-Zeiten. P3 besteht fuer fuenf nichtkreisfoermige
Geometrien in beiden gesetzten Chiralitaeten und oeffnet nur P4. Internes S1,
Arbeit, Traegheit und Masse bleiben offen. Der nachgelagerte P4-Lauf schliesst
zwar den Ledger der explizit konstruierten Source-/Write-Architektur, besteht
aber das Gesamtgate nicht. Seine robuste chirality-odd Querantwort ist nur eine
neue, startphasenkonditionierte Matrixsuszeptibilitaets-Hypothese. Der erste
prospektive Nachtest ist P4-R-phi mit acht neuen History-Phasen; selbst ein
reviewed Chiral-Pass braucht danach ein kompatibles Referee-/Source-Audit und
oeffnet nur einen Anchor-Skalenholdout. P5 bleibt geschlossen.
