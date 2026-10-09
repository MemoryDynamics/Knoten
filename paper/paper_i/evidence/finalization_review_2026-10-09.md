# Paper I finalization review

Date: 2026-10-09. This is an internal authoring audit, not an external referee report.

## Scientific result

The observable mismatch has been closed. The archived cloud statistic was
a median instantaneous width; the earlier theory predicted stationary
current-position RMS. The replacement computes temporal RMS first and
aggregates matching measured/predicted ratios over five seeds second.

Across nine active slices the memory-cloud discrepancies have median
0.0760369784% and maximum 0.9838709275%. Position-relative discrepancies
have median 0.0896306290% and maximum 0.7607552868%. The eight shared
no-feedback control slices have maximum cloud discrepancy 2.1223297249%.
The historical 0.76%/1.15% comparison is not retained as model validation.

The reference uses the native finite-history timing, normalized centroid,
retained force mass and oldest-position retirement. Two independent
implementations (causal impulse response and frequency integral) agree
within 6e-12 relatively for the three reported gain cells. The maximum
observed doubling error is below 3e-12. Neither check is a rigorous tail
bound or an interval existence/stability certificate.

The exact untruncated relation between expected cloud variance and
position-relative variance is E[Q]=E[|r|^2]/q for point deposition. The
finite-cloud spectral numerator is 1-|B_H|^2, whereas the position-relative
numerator is |1-B_H|^2. The translation mode remains unpinned. The
diffusion formula is an analytical linear-model result, not a radius fit
or a new transport measurement.

## Evidence and reproduction

- 85 seed-condition terminal traces are committed, with original-file hashes.
- Every terminal window has 10001 consecutive samples spanning 10000 updates.
- All common kernel, memory, deposition and update conventions are checked
  during extraction; gain is computed from actual archived configurations.
- Rebuilding uses the committed extract and legacy control summaries; no new
  nonlinear simulation is required or claimed.
- The fixed evidence snapshot is commit
  `5ce71e3a44f505351ca883803ece17991c70ae8c`.
- Eight focused tests pass: independent spectral comparison at four parameter
  cells, horizon-one limit, random-walk pairwise covariance, untruncated
  cloud/position identity and terminal-selection validation.
- The new scripts pass Ruff, and the modified documentation builds with
  `mkdocs build --strict`. A scoped GitHub workflow also runs the reference
  tests and evidence rebuild on Paper I changes.
- Source inspection checked that the original simulator records both cloud
  covariance radius and current-position-to-centroid distance after deposition.

## Literature check

The manuscript positions exponential memory and Markov embedding as
established constructions rather than its novelty claim. The comparisons
were checked against primary publication records:

- [Benaim and Raimond, symmetric interactions](https://arxiv.org/abs/math/0309356):
  cumulative occupation averaging and free-energy convergence.
- [Milisic, Meunier and Roux, aging](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6659876):
  linear history interactions and an exponential-memory case; cited as a preprint.
- [Jaganathan and Valani](https://doi.org/10.1016/j.cnsns.2025.109540):
  spectral Markov embedding. Bibliographic year corrected to 2026, volume 154,
  article 109540, despite the 2025 DOI string.
- [Oza, Rosales and Bush](https://doi.org/10.1017/jfm.2013.581):
  moving source and decaying wave-field feedback with inertial droplet motion.
- [Grima](https://doi.org/10.1103/PhysRevLett.95.128103):
  stochastic autochemotactic feedback and the distinction between local
  self-attraction and long-time transport in that model.

The specific contribution is the observable-matched diagnostic and its
archived-data test, not a first exponential-memory model or first Markov embedding.

## Manuscript and PDF audit

- Shared main text keeps the full and compact versions synchronized.
- The full version supplies variance/filter derivations and method limitations.
- Rotating-wave/noise-bracket results are excluded from the Paper I evidence chain.
- The point-measure model matches delta deposition; no unproved smooth density
  assumption or strict information-loss argument remains.
- Both XeLaTeX/BibTeX builds pass, with no undefined citations/references or
  overfull boxes. The remaining nameref/REVTeX label warning and underfull
  line warnings do not affect displayed references or produce clipping.
- Twenty distinct equation/figure/table labels and their twenty explicit
  references were checked; all citation keys exist.
- All pages of both five-page PDFs were rendered and visually inspected.
  Figures, captions, equations and table fit within their bounds.
- The PDF dataset hyperlink resolves to the immutable evidence snapshot.

## Limits retained in the paper

The comparison is post-hoc and uses short terminal windows after long runs.
Samples are correlated; seed IQRs are not confidence intervals. No new
prospective holdout, statistical equivalence, global confinement, nonlinear
stationary-distribution theorem, metastable phase or general dimension
selection is claimed. The half-window results remain in the JSON to expose
finite-window variability. The fixed-gain gate remains inconclusive.

These limits do not block the scoped manuscript, but restrict how it may be
described. Journal acceptance and broader novelty remain editorial judgments.
Before formal submission the author confirms journal and author metadata.
