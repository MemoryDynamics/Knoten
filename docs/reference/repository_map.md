# Repository Map

Stand: 2026-08-30.

Diese Seite ist die visuelle Orientierung fuer das Repository. Die Diagramme
sind grob, aber sie zeigen die aktive Struktur ohne die alten Parallel-Dokumente.

## Top-Level-Struktur

```mermaid
flowchart TD
    root["Emergenz_Knoten"]

    root --> src["src/emergenz_knoten<br/>kanonischer Paketkern"]
    root --> experiments["experiments<br/>reproduzierbare Entry-Points"]
    root --> tests["tests<br/>kleine deterministische Tests"]
    root --> docs["docs<br/>9 aktive Dokumente + Rohmaterial"]
    root --> paper["paper<br/>Paper 0, I, II, III und Kindle-PDFs"]
    root --> reports["reports<br/>datierte Evidenz + README-Index"]
    root --> data["data/processed<br/>generated outputs, ignored by default"]
    root --> figures["figures<br/>draft, paper, external + README-Index"]

    experiments --> sync_exp["synchronization/<br/>scalar, current, oriented and one-way gates"]
    experiments --> score_exp["knot_score_report.py<br/>reviewed scorecard reports"]
    experiments --> trace_exp["dynamic_center_trace_report.py<br/>co-moving trace and spin-proxy plots"]
    experiments --> vector_exp["vector_memory_pilot.py<br/>2D oriented-memory AR pilot"]
    experiments --> spectral_rho_exp["spectral_rho_field_pilot.py<br/>O(M) representation gate"]
    experiments --> diffusion_exp["relaxation_diffusion_field_pilot.py<br/>mode-dependent field gate"]
    experiments --> low_mode_exp["low_mode_ar_feature_closure.py<br/>real-space + AR control gate"]
    experiments --> reconcile_exp["reconcile_low_mode_ar_runs.py<br/>N=100k vs N=1M"]
    experiments --> identity_exp["low_mode_identity_audit.py<br/>seed + segment eigenvector matching"]
    experiments --> raw_null_exp["eta_zero_raw_mode_null_audit.py<br/>exact real null + cadence fit audit"]
    experiments --> metric_exp["carrier_memory_metric_comparison.py<br/>0/6 carrier-only metric closure"]
    experiments --> oriented_exp["oriented_vector_one_way_gate.py<br/>6/6 constructed vector gate"]
    experiments --> fixed_pair_exp["oriented_vector_fixed_pair_distance_gate.py<br/>6/6 global-coupling pair gate"]
    experiments --> mediator_exp["local_oriented_mediator_gate.py<br/>both architectures pass; mechanism open"]
    experiments --> mediator_id_exp["oriented_source_mediator_identifiability.py<br/>6/6 eligible; persistence nonspecific"]
    experiments --> dynamic_mediator_exp["dynamic_common_source_mediator_gate.py<br/>fixed-coupling response holdout"]
    experiments --> checkpoint_exp["reference_state_checkpoints.py<br/>clean-revision z_N formation"]
    experiments --> kernel_audit["kernel_compensation_audit.py<br/>zero-integral / curvature constraints"]
    experiments --> sigma_pilot["fixed_curvature_sigma_pilot.py<br/>one-axis q test at fixed chi"]
    experiments --> comp_pilot["three_scale_compensation_pilot.py<br/>exact zero integral + curvature match"]
    experiments --> signed_pilot["signed_cross_channel_pilot.py<br/>null/product/label-flip gate"]
    experiments --> one_way_exp["one_way_dynamic_source_pilot.py<br/>paired moving-source controls"]
    experiments --> reciprocal_exp["reciprocal_full_knot_gate.py<br/>direct binding; complex-mode null"]
    experiments --> retarded_reciprocal_exp["retarded_reciprocal_full_knot_gate.py<br/>operational channel; complex-mode null"]
    experiments --> same_law_jacobian["same_law_*_audit/gate.py<br/>Jacobian eligibility + affine no-go"]
    experiments --> continuity_gate["continuity_constrained_memory_gate.py<br/>density-current analytic gate"]
    experiments --> green_kernel_gate["dynamic_green_kernel_selection_gate.py<br/>separate adjoint-gradient mediator"]
    experiments --> quasistatic_pair_gate["quasistatic_two_knot_discrimination.py<br/>frozen full-memory discriminator"]
    experiments --> dynamic_pair_gate["dynamic_two_knot_mediator_gate.py<br/>P3.8d energy + dynamic controls"]
    experiments --> emergent_mode_gate["emergent_modal_state_gate.py<br/>historical P3.8e; superseded identification"]
    experiments --> emergent_mode_reconciliation["emergent_modal_state_reconciliation.py<br/>corrected poles / holdout / Hankel / input Gram"]
    experiments --> p38f_bundle["curate_p38f_state_bundle.py<br/>five complete hash-checked N3M states"]
    experiments --> p38f_write["p38f_canonical_write_gate.py<br/>seed shards + split G0/G1 aggregation"]
    experiments --> source_local_exp["source_local_linear_gate.py<br/>strict source locality; knot-loading null"]
    experiments --> core_audit["kernel_core_audit.py<br/>near-field force and matched ablation"]
    experiments --> att_scan["attractive_only_regime_scan.py<br/>dimensionless A-axis + linear benchmark"]
    experiments --> field_bridge["field_equation_bridge.py<br/>Gaussian heat map vs local mediator"]
    experiments --> field_operator["local_field_operator_audit.py<br/>k4 / zero-mean / finite-k / rank null"]
    experiments --> active_field_exp["active_scalar_delta_field_pilot.py<br/>ETD1 + six control arms"]
    experiments --> write_read["write_read_reparameterization_audit.py<br/>K*rho vs signed potential memory"]
    experiments --> stability_audit["stability_gate_audit.py<br/>4 checkpoints + late holdout"]
    experiments --> dimension_n["dimension_over_n_reproduction.py<br/>D_cov / D_occ / D_win / D_mem"]

    src --> core["core.py<br/>SimulationConfig, finite memory simulation"]
    src --> kernels["kernels.py<br/>Memory weights, Gaussian potentials and gradients"]
    src --> analytic["analytic.py<br/>dimensionless groups, modes, compact same-law no-go"]
    src --> field["field.py<br/>heat transfer + local operator expansion"]
    src --> diagnostics["diagnostics.py<br/>D_cov, D_occ, residence, geometry spectrum"]
    src --> impulse_id["impulse_identification.py<br/>shared AR, withheld readout, corrected panel Hankel"]
    src --> knot_score["knot_score.py<br/>scorecards v0.3-v0.6 + shape gates"]
    src --> stability["stability.py<br/>age, local-window and holdout gates"]
    src --> measurement_stability["measurement_stability.py<br/>D_occ cadence / estimator convergence"]
    src --> active_field["active_scalar_field.py<br/>real spectral delta-source field"]
    src --> experiments_api["experiments.py<br/>runner and serialization"]
    src --> markov["markov/<br/>augmented-state operator layer"]
    src --> anchor["anchor.py<br/>Paper-0 compatibility facade"]
    src --> state["state.py<br/>complete memory state; rigid placement"]
    src --> checkpoints["checkpoints.py<br/>versioned z_N + checksums"]
    src --> probe["weak_probe.py<br/>paired pulse + null path"]
    src --> finite_k["finite_k_response.py<br/>zero-centroid modal state impulses"]
    src --> canonical_write["canonical_write_port.py<br/>mirrored zero-net trajectory write"]
    src --> impulse_id["impulse_identification.py<br/>recursive AR / damped / Hankel gates"]
    src --> frozen["frozen_source.py<br/>localized fixed field + paired controls"]
    src --> coupled["coupled_nodes.py<br/>one-way source + relational/shape observables"]
    src --> reciprocal_nodes["reciprocal_nodes.py<br/>off / one-way / synchronous reciprocal"]
    src --> reciprocal_diag["reciprocal_diagnostics.py<br/>isotropic 2x2 mode + phase coherence"]
    src --> reciprocal_closure["reciprocal_parameter_closure.py<br/>G/C Hessians, A_minus + common-scale interval"]
    src --> signed["signed_cross_channel.py<br/>separate signed scalar cross coupling"]
    src --> continuation["_continuation.py<br/>shared Numba continuation primitives"]
    probe --> continuation
    frozen --> continuation
    coupled --> continuation
    signed --> continuation
    src --> sync["synchronization.py<br/>lag response; exact sign-flip rank"]
    src --> vector_memory["vector_memory.py<br/>oriented history/current, bivector and vector features"]
    src --> oriented_source["oriented_source.py<br/>persistent passive vector fibre + paired controls"]
    oriented_source --> continuation
    src --> local_mediator["local_mediator.py<br/>scalar/vector 1D diffusion + telegraph states"]
    src --> source_local_linear["source_local_linear.py<br/>exact source-local reciprocal spectrum"]
    src --> source_local_modal["source_local_modal.py<br/>structure-preserving channel reductions"]
    src --> mediator_id["mediator_identifiability.py<br/>segment power + complex transfer contrast"]
    src --> external_field["external_field_response.py<br/>paired active / flip / off target paths"]
    external_field --> continuation
    src --> spectral_rho["spectral_memory_field/runtime.py<br/>Fourier rho + cached O(M) operators"]
    src --> diffusion_rho["relaxation_diffusion_memory.py<br/>heat-semigroup field update"]
    src --> spectral_trace["spectral_memory_trace.py<br/>aligned and raw eta-zero Numba traces"]
    src --> memory_metrics["memory_metrics.py<br/>covariance, predictive and RKHS metrics"]
    src --> covariant_field["covariant_vector_field.py<br/>isolierter analytischer K2-Vorschlag; nicht im Knotensimulator"]
    src --> continuity_memory["continuity_memory.py<br/>innovation moments + longitudinal rho/j modes"]
    src --> gradient_mediator["gradient_mediator.py<br/>independent longitudinal m/p response"]
    src --> dynamic_gradient_mediator["dynamic_gradient_mediator.py<br/>modal m/p/R split dynamics + ledger"]
    src --> quasistatic_pair["quasistatic_pair.py<br/>memory-memory + symmetric visible-memory pairs"]
    spectral_trace --> raw_null_exp

    core --> state
    covariant_field --> analytic_boundary["K2 nur analytisch<br/>keine Laufzeitkopplung an (x,rho)"]
    continuity_memory --> continuity_boundary["P3.8a analytic candidate<br/>rho/j; not selected by scalar data"]
    gradient_mediator --> mediator_boundary["P3.8b analytic candidate<br/>new m/p state; not canonical rho"]
    gradient_mediator --> green_kernel_gate
    gradient_mediator --> dynamic_gradient_mediator
    dynamic_gradient_mediator --> dynamic_pair_gate
    quasistatic_pair --> quasistatic_pair_gate
    finite_k --> emergent_mode_gate
    checkpoints --> p38f_bundle
    canonical_write --> p38f_write
    p38f_bundle --> p38f_write
    impulse_id --> emergent_mode_gate
    emergent_mode_gate --> p38e_null["0/5 temporal pass<br/>canonical null not rejected"]
    p38e_null --> split_gates["G0 validity -> G1 identifiability<br/>G2 second state -> G3 phase"]
    split_gates -.last scalar check.-> write_port["P3.8f zero-net deposition pulse"]
    write_port --> write_result["G0 5/5 pass<br/>G1 0/5 inconclusive after translation removal"]
    write_result -.one preregistered repair.-> delayed_write["return kick after one memory time"]
    write_port -.conditional.-> pair_gate["G4 one-way two-node transfer"]

    markov --> closure_api["closure.py<br/>AR skill, eigenspaces + exact eta-zero null"]
    markov --> features["features.py<br/>memory-summary features"]
    markov --> dataset["dataset.py<br/>z_i samples and lagged pairs"]
    markov --> transition["transition.py<br/>labels, counts, transition matrices"]
    markov --> validation["validation.py<br/>rates, timescales, CK errors"]
    markov --> metastability["metastability.py<br/>slow modes, spectral gap"]
```

## Aktive Doku-Struktur

```mermaid
flowchart TD
    index["index.md<br/>Frontdoor"]
    current["current_status.md<br/>Status und naechste Schritte"]
    priorities["project_priorities.md<br/>Arbeitsreihenfolge"]
    theory["THEORETICAL_CONTEXT.md<br/>Modell, Markov, Grenzen"]
    map["repository_map.md<br/>Bilder fuer Code/Datenfluss"]
    experiments_doc["experiment_catalog.md<br/>Entry-Points und Evidenz"]
    claims["paper_claims.md<br/>Claim-Register"]

    index --> current
    index --> priorities
    index --> theory
    index --> map
    index --> experiments_doc
    index --> claims

    priorities --> experiments_doc
    theory --> claims
    map --> experiments_doc
    experiments_doc --> claims
```

## Code- und Datenfluss

```mermaid
flowchart LR
    config["SimulationConfig"] --> sim["finite-memory simulation<br/>or augmented feature simulation"]

    sim --> samples["samples x_i"]
    sim --> steps["sample_steps n_i"]
    sim --> memory["memory buffer / weights"]
    memory --> fullstate["FiniteMemoryState<br/>x + complete retained memory"]
    fullstate --> checkpoint["versioned checkpoint<br/>config + N + seed + checksums"]
    fullstate --> orientedstate["OrientedMemoryState<br/>passive low-pass direction fibre"]
    orientedstate --> orientedgate["one-way active / flip / off / random-sign<br/>plus one-step control"]
    orientedgate --> orienteddiag["oriented_diagnostics.py<br/>paired response / shape / distance KPIs"]
    orientedstate --> source_trace["autonomous source trace<br/>persistent + one-step comparator"]
    source_trace --> source_power["two Hann segments<br/>vector non-DC power"]
    source_power --> identifiability["source-weighted complex<br/>transfer contrast"]
    local_transfer["frozen local mediator rules<br/>discrete impulse responses"] --> identifiability
    checkpoint --> reload["validated reload<br/>fresh common future noise"]
    reload --> rigid["rigid placement<br/>translation / orthogonal rotation"]
    rigid --> weakprobe["paired weak probe<br/>+delta / -delta / unprobed / eta_zero"]
    weakprobe --> response["response matrices<br/>energy rank + sign-flip rank"]
    sim --> zfeatures["augmented features z_i"]
    sim --> vfeatures["vector-memory features<br/>optional p_i summaries"]
    sim --> rhohat["spectral rho_hat<br/>explicit compact Markov state"]
    rhohat --> tracecore["Numba trace<br/>paired noise + final rho_hat"]
    tracecore --> lowmodes["phase-aligned low modes"]
    tracecore --> rawmodes["raw p_k + rho_hat_k<br/>exact eta-zero closure state"]
    tracecore --> realhistory["finite real-history force<br/>tail-bounded reference"]
    lowmodes --> closure["cross-seed AR closure<br/>persistence + shuffled controls"]
    rawmodes --> closure
    realhistory --> closure
    closure --> lagged

    samples --> geom["diagnostics.py<br/>D_cov, D_occ, residence"]
    geom --> score["knot_score.py<br/>v0.5 evidence + v0.6 stationarity eligibility"]
    zfeatures --> lagged["markov.dataset<br/>(z_i, z_i+ell)"]
    vfeatures --> lagged
    steps --> lagged

    lagged --> labels["markov.transition<br/>labels"]
    labels --> counts["transition counts"]
    counts --> matrix["row-stochastic matrix U_ell"]
    matrix --> validation["markov.validation<br/>eigenvalues, rates, CK"]
    matrix --> meta["markov.metastability<br/>slow modes"]

    geom --> reports["reports / paper tables"]
    score --> reports
    validation --> reports
    meta --> reports
    response --> reports
    orientedgate --> reports
    identifiability --> reports

    reports --> privacy["privacy_and_control_plan<br/>public sanitized policy"]
    reports --> paper0["Paper 0<br/>technical anchor"]
    reports --> paper1["Paper I<br/>minimal model and evidence"]
    paper1 -.later.-> paper2["Paper II<br/>propagation / c_eff"]
    paper2 -.later.-> paper3["Paper III<br/>internal modes / synchronization"]
```

## Kernelreduktions- und Feldschiene

```mermaid
flowchart LR
    old["two-scale reference<br/>(A_rep,A_att)=(1,35)"] --> core["near-field audit<br/>R_mem / sigma_rep about 2e-4"]
    core --> matched["curvature match<br/>attractive-only (0,26)"]
    matched --> scan["A_att=0..40<br/>5 seeds, common eta=0"]
    scan --> family["family match<br/>A_eff = A_att - 9"]
    family --> linear["linear memory benchmark<br/>r_next=q(1-g)r+q epsilon xi"]
    linear --> longrun["N=30M/300M reconciliation<br/>max error 1.16 percent"]
    longrun --> nonlinear["fixed g gate<br/>R/L = 0.03, 0.1, 0.3"]
    nonlinear --> scaleaudit["scale audit<br/>voxel residence confounded"]
    scaleaudit --> decision["scalar control baseline<br/>no metastable branch isolated"]
    decision --> lognull["LoG null family<br/>zero mean, curvature matched"]
    lognull --> operator["local operator audit<br/>Gaussian k4 + H I_d rank null"]
    operator -.new assumption.-> finitek["finite-k candidate<br/>a2 negative, k4 stabilized"]
    decision --> spectral["spectral rho representation<br/>exact at nu=0; 64 modes"]
    spectral --> factorization["write/read identity gate<br/>phi = K rho; read = delta"]
    factorization -.new dynamics.-> activefield["active scalar field gate<br/>classical finite-k pass; eta-zero nonspecific"]
    spectral --> epsilon_gate["epsilon 1e-8..1e-4<br/>exact linear scaling"]
    epsilon_gate --> mediator["relaxation-diffusion extension<br/>q_k=(1-lambda) exp(-nu k^2)"]
    mediator --> smooth["pilot: smooth weakening<br/>no new branch"]
    smooth --> closure["low-mode AR closure<br/>real-space / nu=0 / eta=0 gates pass"]
    closure --> longmode["N=1M / 10,000 memory times"]
    longmode --> realmode["aggregate real rates<br/>N gate passes"]
    longmode --> complexfail["complex side modes<br/>eta=0 subspace overlap"]
    complexfail --> identity["mode identity complete<br/>no stable single eigenmode"]
```

The reduced scalar trajectory identifies the product eta M0 A_att, not its
three raw factors separately. The matched kernel families and fixed-g gate
now close the scalar identification branch as a controlled relaxation
baseline with only a weak smooth finite-kernel correction. The field branch
is deliberately separate: the Gaussian heat-semigroup representation uses
an auxiliary coordinate, whereas a physical relaxation-diffusion field
changes the dynamics.

The local operator audit now makes this separation explicit: the Gaussian
low-k response fixes a positive `k^2/k^4` null family, while a preferred
finite wave number requires the additional sign choice `a2<0`. Independent
component transfer remains `H I_d` and therefore cannot select rank three.
The active delta-source implementation passes its numerical, cubic-off and
source-off gates, but eta-zero carries the same field pattern. It is therefore
a classical mechanism candidate, not yet a feedback-specific knot.

## Long-Run-Schiene

```mermaid
flowchart TD
    plan["project_priorities.md<br/>P1 Long-Run controls"] --> runner["experiments/current/dynamics/long_runs/long_run_metastability.py"]
    runner --> local["data/processed/long_run_metastability<br/>ignored bulk JSON outputs"]
    local --> trace_review["dynamic_center_trace_report.py<br/>log-trend radius/drift + local spin figures"]
    local --> stability_gate["stability_gate_audit.py<br/>4 age checkpoints + 1 late holdout"]
    stability_gate --> candidate["provisional candidate<br/>radius + endpoint shape"]
    candidate --> future["future runs<br/>local radius + shape windows"]
    local --> review["manual review<br/>residence, controls, runtime"]
    trace_review --> report["reports/<br/>committed result report"]
    stability_gate --> report
    review --> report["reports/<br/>committed result report"]
    report --> paper1["Paper I evidence table"]
```

## Referenzzustands- und Interaktionsschiene

```mermaid
flowchart LR
    clean["clean Git revision"] --> formation["final-state formation<br/>N=1e8; no trajectory storage"]
    formation --> z3["checkpoint d=3<br/>x_N + 600 memory points"]
    formation --> z10["checkpoint d=10<br/>x_N + 600 memory points"]
    z3 --> paired["paired branches<br/>same z_N + same future noise"]
    z10 --> paired
    paired --> free["free self-dynamics<br/>no cross coupling"]
    paired --> probe["weak localized frozen source"]
    probe --> fieldaudit["static potential / force audit<br/>sign, parity, monopole error"]
    probe --> ladder["calibrated distance ladder<br/>target deformation / response rank"]
    fieldaudit --> compgate["kernel compensation gate<br/>exact zero integral + curvature match complete"]
    ladder --> compgate
    ladder --> crossreadout["independent scalar readout<br/>shape gate fails"]
    crossreadout --> historycurrent["ordered-history current<br/>random-sign gate fails"]
    historycurrent --> orientedgate2["independent oriented state<br/>6/6 one-way gate pass"]
    orientedgate2 --> fixedpair["fixed eta_v + independent pairs<br/>6/6 distance-gate pass"]
    fixedpair --> mediatorgate["local mediator holdout<br/>both inserted rules pass"]
    mediatorgate --> sourceid["autonomous-source identifiability<br/>6/6 source eligibility pass"]
    sourceid --> dynamicgate["dynamic common-source holdout<br/>model separation only 4/6: fail"]
    dynamicgate --> ranknull["ambient rank null<br/>component-wise transfer H I_d"]
    ranknull -.new symmetry-breaking mechanism required.-> transport
    compgate --> channel["signed scalar cross-channel complete<br/>exact nulls + product reversal"]
    channel --> seeds["later: 6-10 independent states<br/>no retuning"]
    channel --> one_way["one-way source v0.6<br/>pre-launch stationarity + paired shape gate"]
    one_way --> launch["paired point launch<br/>source deforms; target sub-threshold"]
    launch --> transport["next: coherent whole-state or<br/>local / retarded transport"]
    transport --> reciprocal["direct synchronous reciprocal<br/>binding pass; complex-mode null"]
    reciprocal --> retarded["next: one fixed retarded return<br/>no gain retuning"]
    reciprocal --> jacobian["same-law G/C Jacobian audit<br/>fixed eta remains real"]
    jacobian --> commonscale["one common eta<br/>local complex eligibility"]
    commonscale --> affinebalance["affine balance 0/13<br/>compact two-scale no-go"]
    affinebalance --> continuitymemory["continuity-constrained rho/j gate<br/>longitudinal phase; force balance open"]
    continuitymemory -.same pole polynomial only.-> commonenergy["separate m/p mediator<br/>adjoint gradient energy"]
    commonenergy --> pairdiscrimination["frozen full-memory discriminator<br/>conditional pass; no dynamics"]
    pairdiscrimination --> energydiscretization["next: discrete source-work / damping gate<br/>before one dynamic pilot"]
    retarded --> source_local["emitter-only offset/current<br/>stable channel; knot-loading null"]
    source_local --> shape_source["autonomous shape multipole<br/>segment/control gate null"]
    shape_source --> vector_form["next: formal vector-memory extension<br/>equations + null limits before run"]
    seeds -.independent formation holdout.-> retarded
    free --> delta["control-subtracted changes<br/>geometry, response rank, stability"]
    probe --> delta
    one_way --> delta
    launch --> delta
```

The checkpoint is complete for the implemented finite-memory approximation.
It deliberately does not contain the preceding `1e8` positions or a PRNG state:
the Markov branch comparison supplies a fresh explicit common future-noise
array. Independent seeds remain necessary for inferential claims.

## Gemeinsamer Modellkern und Brueckenstrategie

```mermaid
flowchart LR
    paperlaw["Paper-I transition law<br/>z=(x,rho), epsilon xi"]
    finiteh["finite-H specialization<br/>Y=(x_n,...,x_n-H+1)"]
    deterministic["deterministic skeleton<br/>epsilon=0"]
    stochastic["stochastic lifting<br/>epsilon greater than 0"]
    longrun["scalar long-run null<br/>linear relaxation cloud"]
    loops["prepared rotating waves<br/>Anchor + L3"]
    n0["N0 reviewed bracket<br/>1e-4 stable / 1e-3 fail"]
    p5d["P5-D implementation present<br/>readiness pending; target closed"]
    p5c["P5-C common-noise<br/>paired cancellation"]
    p5i["P5-I independent noise<br/>robustness"]
    fields["field / mediator extensions<br/>new dynamics"]

    paperlaw --> finiteh
    paperlaw --> longrun
    finiteh --> deterministic --> loops --> n0
    finiteh --> stochastic --> n0
    n0 -.reviewed bracket required.-> p5d
    p5d -.reviewed interaction required.-> p5c
    p5c -.reviewed common-noise pass.-> p5i
    paperlaw -.additional law.-> fields
```

The merge is at the transition-law and state-contract level, not by declaring
all evidence regimes equivalent. Paper I already writes
`x_next=x+epsilon*xi-eta*grad(Phi)` and updates memory from the new position.
The rotating-wave FIFO state is the ordered finite-H specialization of that
law. `epsilon=0` defines its deterministic skeleton; positive epsilon is an
explicit stochastic lifting, not a different force law.

N0 now distinguishes a genuinely injected innovation from a binary64
perturbation that rounds away. Anchor and L3 were compared at common memory
time using `chi=epsilon/(R sqrt(alpha))`, so that `D/R^2=chi^2/2` is matched.
The reviewed finite-time result is unresolved through `chi=1e-16`, stable
from `1e-15` through `1e-4`, and phase-/chirality-failing at `1e-3` and
`1e-2`. The target-free P5-D design and its separate protocol are now frozen;
Pair-step, runner, independent result auditor and synthetic falsifiers are
implemented without opening the target. Every registered pair trajectory
remains closed pending readiness review. Relaxation-diffusion, Telegraph and other mediator equations remain
separate model extensions until they are derived from or selected against the
common transition law.

## Native Rotating-wave-Schiene

```mermaid
flowchart LR
    equations["rotating_wave.py<br/>finite-H + continuum balance"]
    discovery["discovery<br/>candidate + controls"]
    p0d0["P0 / D0<br/>provenance + SO(2) object"]
    stability["rotating_wave_stability.py<br/>anchor local numerical"]
    interval["rotating_wave_interval.py<br/>Krawczyk certificates"]
    ladder["L0--L4<br/>five local roots"]
    reconcile["fixed-gain continuum<br/>historical target preserved"]
    audit["foundation audit<br/>independent sums + quadratures"]
    l5["L5 pass<br/>sixth local root + scaling"]
    frontdoor["rotating_wave_foundation.md<br/>evidence + claim boundary"]
    center["scalar_memory_center_filter.md<br/>B_H + effective center port"]
    nonanchor["P1 L3 pass<br/>second local numerical scale"]
    bridge["P2 formal fail<br/>strong local matrix response"]
    p2r["P2-R pass<br/>resolved long recovery"]
    formation["P3 pass<br/>finite-ensemble attraction"]
    mechanics["P4 formal fail<br/>ledger pass + transverse response"]
    p4rphi["P4-R-phi reviewed pass<br/>discrete phase response"]
    referee["source referee<br/>restricted pass"]
    p4rs["P4-R-S reviewed pass<br/>two-cell scale transfer"]
    noise["N0 reviewed pass<br/>resolved finite-time bracket"]
    interaction["P5 implementation present<br/>readiness pending; target closed"]

    equations --> discovery --> p0d0
    p0d0 --> stability
    p0d0 --> interval --> ladder --> reconcile --> audit --> l5 --> frontdoor
    stability --> audit
    frontdoor --> nonanchor
    nonanchor --> bridge
    center -.independent input.-> bridge
    bridge --> p2r --> formation --> mechanics
    mechanics --> p4rphi
    p4rphi --> referee
    referee --> p4rs
    p4rs --> noise
    noise -.reviewed bracket required.-> interaction
```

Code und Programme liegen in `src/emergenz_knoten/rotating_wave*.py` und
`experiments/current/dynamics/rotation/`. Das kompakte Artefaktledger liegt
in `reports/dynamics/rotation/README.md`. Die durchgezogenen Pfeile markieren
die historische Gatefolge samt unveraendertem P2- und P4-Fail; sie bedeuten
nicht, dass jeder Zwischenlauf bestanden hat. P2-R und P3 liefern die eng
reviewed Rueckkehr- beziehungsweise finite-ensemble-Attraktionsevidenz. Der
P4-Fail schloss den direkten P5-Pfad. P4-R-phi besteht danach den diskreten
Acht-Phasen-Chiraltest; Gate-Review und internes Source-Referee-Audit halten
den engen Port-/Ledger-/Antwortbefund mit Major-Claim-Restriktionen aufrecht.
Die Folge benennt den historischen P4-Befund nicht um. Der nach targetfreiem
Design-, Protokoll- und Implementierungsfreeze unveraendert ausgefuehrte
P4-R-S-Anchor-Holdout uebertraegt den registrierten Antworttyp auf eine zweite
vorbereitete Skala: maximale Anchor--L3-Abweichung `0.00232715` gegen die
vorab fixierte Grenze `0.05`. Ein unabhaengig implementierter Auditor stimmt
ohne Feldabweichung zu. Das Ergebnisreview hatte ausschliesslich P5-Design und
prospektive Protokollierung geoeffnet; vor diesen Pfad ist nun N0 eingeschoben.
N0 prueft danach die Paper-I-Innovation und trennt numerisch weggerundetes
Rauschen von aufgeloester orbitaler Stabilitaet. Das reviewte Ergebnis traegt
eine finite-time Klammer: `chi=1e-4` besteht, `chi=1e-3` scheitert am
Phasen-/Chiralitaetsgate. P5-D-Design und ein getrenntes Protokoll sind nun
targetfrei eingefroren. Sie waehlen eine lineare gegenseitige
notched-Center-/adjungierte Write-Architektur und einen Closed-loop-Kontrast
gegen beide Einwegantworten. Implementierung ist der naechste versiegelte
Schritt; Targetzugriff und Interaktionsevidenz bleiben geschlossen. Die acht
P4-R-Phasenknoten enthalten
vier spiegelverschiedene Paare und sind keine Replikationen; zwei Zellen
liefern keine Konvergenzordnung.

## Leseregeln

- `src/emergenz_knoten` ist der belastbare Codekern. Der externe Response-
  Pfad liegt in `state.py`, `checkpoints.py`, `weak_probe.py`,
  `frozen_source.py`, `coupled_nodes.py`, `signed_cross_channel.py`,
  `oriented_source.py`, `local_mediator.py`, `source_local_linear.py`,
  `source_local_modal.py`, `external_field_response.py`,
  `autonomous_trace.py`, `memory_metrics.py`, `gradient_mediator.py`,
  `quasistatic_pair.py` und `synchronization.py`.
- `spectral_memory_field.py` ist eine kompakte Reprasentation des alten
  Memory. `relaxation_diffusion_memory.py` aendert mit modeabhaengigem
  Zerfall die Dynamik; `spectral_memory_trace.py` validiert niedrige Moden
  gegen eine endliche Realraumhistorie.
- `experiments/` sind Entry-Points, nicht automatisch stabile API. Reports
  werden erst nach Kontroll- und Reproduzierbarkeitspruefung Evidenz.
- `docs/` enthaelt nur neun aktive Arbeitsdokumente; historische Unterordner
  sind Rohmaterial.
- `reports/` sind datierte Zwischenstaende; `reports/README.md` markiert die aktuelle Evidenzschiene und den Status jedes Gate-Typs.
- `data/processed/` und `results/` bleiben generiert und werden nur nach
  Review ueber Reports zusammengefasst. Einzelne getrackte JSONs unter
  `data/processed/` sind kuratierte Snapshots oder Test-/Report-Fixtures, nicht
  das Muster fuer neue Bulk-Laeufe.

## Aufraeumregeln

- Die neun MkDocs-Seiten sind die aktive Steuerzentrale. Neue Arbeitsnotizen
  sollen zuerst dort einsortiert werden, bevor neue Dokumente entstehen.
- `docs/archive/emergente_raumzeit`, `docs/historical/chatgpt/topics`, `paper/*/archiv`
  und `experiments/archive/legacy` sind Rohmaterial oder historische Referenz, keine
  aktive Quelle fuer Claims.
- Generierte Rohdaten unter `data/processed/` bleiben standardmaessig ignoriert.
  Nur reviewed JSON-Zusammenfassungen, Reports und Figuren werden gezielt
  committed; fuer neue Snapshots ist ein explizites `git add -f` erforderlich.
- Top-level Buildprodukte wie `site/`, `results/`, `tmp/`, Caches und lokale Venvs
  duerfen nicht als Projektstand gelesen werden.
