# Repository Map

Stand: 2026-06-29.

Diese Seite ist als visuelle Orientierung gedacht. Die Diagramme sind bewusst
grob: Sie zeigen, welche Teile des Repositories welche Rolle spielen und wie
Code, Experimente, Papers und Dokumentation zusammenhaengen.

## Top-Level-Struktur

```mermaid
flowchart TD
    root["Emergenz_Knoten"]

    root --> src["src/emergenz_knoten<br/>kanonischer Paketkern"]
    root --> experiments["experiments<br/>reproduzierbare Entry-Points"]
    root --> tests["tests<br/>kleine deterministische Tests"]
    root --> docs["docs<br/>kuratierte Projektdokumentation"]
    root --> paper["paper<br/>Paper 0, I, II, III und Kindle-PDFs"]
    root --> reports["reports<br/>datierte Reviews und Analyseberichte"]
    root --> data["data<br/>processed outputs, meist ignoriert"]
    root --> figures["figures<br/>draft/result figures"]
    root --> results["results<br/>lokale Pipeline-Ausgaben, ignoriert"]
    root --> tmp["tmp/site/cache<br/>lokale Build-Artefakte, ignoriert"]

    src --> core["core.py<br/>SimulationConfig, finite memory simulation"]
    src --> kernels["kernels.py<br/>Memory weights, Gaussian kernels"]
    src --> diagnostics["diagnostics.py<br/>D_cov, D_occ, residence, geometry spectrum"]
    src --> experiments_api["experiments.py<br/>runner and serialization"]
    src --> markov["markov/<br/>augmented-state operator layer"]
    src --> anchor["anchor.py<br/>Paper-0 compatibility facade"]

    markov --> features["features.py<br/>memory-summary features"]
    markov --> dataset["dataset.py<br/>z_i samples and lagged pairs"]
    markov --> transition["transition.py<br/>labels, counts, transition matrices"]
    markov --> validation["validation.py<br/>rates, timescales, CK errors"]
    markov --> metastability["metastability.py<br/>slow modes, spectral gap"]
```

## Code- und Datenfluss

```mermaid
flowchart LR
    config["SimulationConfig"] --> sim["simulate_finite_memory<br/>or simulate_augmented_features"]

    sim --> samples["samples x_i"]
    sim --> steps["sample_steps n_i"]
    sim --> memory["final memory / weights"]
    sim --> features["augmented_features z_i<br/>lossy summaries of z_n"]

    samples --> geom["diagnostics.py<br/>D_cov, D_occ, residence"]
    features --> lagged["markov.dataset<br/>(z_i, z_{i+ell})"]
    steps --> lagged

    lagged --> labels["markov.transition<br/>voxel labels"]
    labels --> counts["transition counts"]
    counts --> matrix["row-stochastic matrix U_ell"]
    matrix --> validation["markov.validation<br/>eigenvalues, rates, CK"]
    matrix --> meta["markov.metastability<br/>slow modes, spectral gaps"]

    geom --> report["reports / paper tables"]
    validation --> report
    meta --> report

    report --> paper0["Paper 0<br/>methodological anchor"]
    report --> paper1["Paper I<br/>minimal model"]
    report -.later.-> paper2["Paper II<br/>propagation / c_eff"]
```

## Paper- und Doku-Fluss

```mermaid
flowchart TD
    docs_front["docs/index.md<br/>front door"] --> priorities["project_priorities.md"]
    docs_front --> current["current_status.md"]
    docs_front --> nonmarkov["non_markovian_basis.md"]
    docs_front --> markov_arch["markov_architecture.md"]
    docs_front --> markov_req["markov_requirements.md"]
    docs_front --> repro["reproducibility_status.md"]
    docs_front --> claims["paper_claims.md"]

    priorities --> p0task["P0.1/P0.2<br/>Markov layer and sensitivity checks"]
    markov_arch --> p0task
    markov_req --> p0task
    repro --> p0task

    p0task --> paper0["paper/paper_0<br/>mathematical anchor"]
    paper0 --> paper1["paper/paper_i<br/>minimal dynamical foundation"]
    paper1 --> paper2["paper/paper_ii<br/>propagation and kinematics"]
    paper2 --> paper3["paper/paper_iii<br/>future quantum/SM roadmap"]

    claims --> paper0
    claims --> paper1
    claims -.future work.-> paper2
    claims -.future work.-> paper3

    reports["reports/<br/>dated reviews and audits"] --> docs_front
    reports --> paper0
```

## Leseregeln

- `src/emergenz_knoten` ist der belastbare Codekern.
- `experiments/` sind Entry-Points, nicht automatisch API.
- `docs/` und `reports/` sind kuratiert; historische Chatnotizen bleiben
  Rohmaterial.
- `paper/` darf nur Claims tragen, die durch Modell, Code oder klar markierte
  Future-Work-Sprache gedeckt sind.
- `data/processed/` und `results/` sind standardmaessig generiert und
  ignoriert; kleine Evidenzartefakte koennen gezielt committed werden.
