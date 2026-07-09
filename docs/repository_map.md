# Repository Map

Stand: 2026-07-09.

Diese Seite ist die visuelle Orientierung fuer das Repository. Die Diagramme
sind grob, aber sie zeigen die aktive Struktur ohne die alten Parallel-Dokumente.

## Top-Level-Struktur

```mermaid
flowchart TD
    root["Emergenz_Knoten"]

    root --> src["src/emergenz_knoten<br/>kanonischer Paketkern"]
    root --> experiments["experiments<br/>reproduzierbare Entry-Points"]
    root --> tests["tests<br/>kleine deterministische Tests"]
    root --> docs["docs<br/>7 aktive Dokumente + Rohmaterial"]
    root --> paper["paper<br/>Paper 0, I, II, III und Kindle-PDFs"]
    root --> reports["reports<br/>datierte Reviews und Analyseberichte"]
    root --> data["data/processed<br/>generierte Outputs, ignoriert"]
    root --> figures["figures<br/>draft/result figures"]

    experiments --> sync_exp["synchronization/<br/>planned single-/multi-knot protocols"]

    src --> core["core.py<br/>SimulationConfig, finite memory simulation"]
    src --> kernels["kernels.py<br/>Memory weights, deposition modes, Gaussian kernels"]
    src --> diagnostics["diagnostics.py<br/>D_cov, D_occ, residence, geometry spectrum"]
    src --> experiments_api["experiments.py<br/>runner and serialization"]
    src --> markov["markov/<br/>augmented-state operator layer"]
    src --> anchor["anchor.py<br/>Paper-0 compatibility facade"]
    src --> sync["synchronization.py<br/>phase-lock, lag response, response rank"]

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
    sim --> zfeatures["augmented features z_i"]

    samples --> geom["diagnostics.py<br/>D_cov, D_occ, residence"]
    zfeatures --> lagged["markov.dataset<br/>(z_i, z_i+ell)"]
    steps --> lagged

    lagged --> labels["markov.transition<br/>labels"]
    labels --> counts["transition counts"]
    counts --> matrix["row-stochastic matrix U_ell"]
    matrix --> validation["markov.validation<br/>eigenvalues, rates, CK"]
    matrix --> meta["markov.metastability<br/>slow modes"]

    geom --> reports["reports / paper tables"]
    validation --> reports
    meta --> reports

    reports --> privacy["privacy_and_control_plan<br/>public sanitized policy"]
    reports --> paper0["Paper 0<br/>technical anchor"]
    reports --> paper1["Paper I<br/>minimal model and evidence"]
    paper1 -.later.-> paper2["Paper II<br/>propagation / c_eff"]
    paper2 -.later.-> paper3["Paper III<br/>internal modes / synchronization"]
```

## Long-Run-Schiene

```mermaid
flowchart TD
    plan["project_priorities.md<br/>P1 Long-Run controls"] --> runner["experiments/long_run_metastability.py"]
    runner --> local["data/processed/long_run_metastability<br/>ignored JSON outputs"]
    local --> review["manual review<br/>residence, controls, runtime"]
    review --> report["reports/<br/>committed result report"]
    report --> paper1["Paper I evidence table"]
```

## Leseregeln

- `src/emergenz_knoten` ist der belastbare Codekern; `synchronization.py` ist aktuell nur eine kleine Diagnostikschicht.
- `experiments/` sind Entry-Points, nicht automatisch stabile API.
- `docs/` enthaelt nur sieben aktive Arbeitsdokumente; historische Unterordner
  sind Rohmaterial.
- `reports/` sind datierte, zitierbare Zwischenstaende.
- `data/processed/` und `results/` bleiben generiert und werden nur nach
  Review ueber Reports zusammengefasst.

## Aufraeumregeln

- Die sieben MkDocs-Seiten sind die aktive Steuerzentrale. Neue Arbeitsnotizen
  sollen zuerst dort einsortiert werden, bevor neue Dokumente entstehen.
- `docs/EmergenteRaumzeit`, `docs/ChatGPT Chatverlaeufe`, `paper/*/archiv`
  und `experiments/legacy` sind Rohmaterial oder historische Referenz, keine
  aktive Quelle fuer Claims.
- Generierte Rohdaten unter `data/processed/` bleiben ignoriert. Nur reviewed
  JSON-Zusammenfassungen, Reports und Figuren werden gezielt committed.
- Top-level Buildprodukte wie `site/`, `results/`, Caches und lokale Venvs
  duerfen nicht als Projektstand gelesen werden.
