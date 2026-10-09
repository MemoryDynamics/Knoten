# Paper I: truncation and observable audit

The canonical nine-slice JSON is evaluated without new stochastic runs.
The causal unit-noise impulse is propagated through the linear native FIFO
update, including normalized centroid deposition and retirement of the oldest
position. Summed squared relative responses give the stationary variance
reference. The weighted second moment is propagated separately to obtain
the expected memory-cloud squared radius.

Before computing outputs, the script fixes a 0.1% radius tolerance and a
1e-10 relative variance convergence tolerance. Horizon-one and zero-gain
random-walk controls pass. Both 20000- and 40000-step impulse sums agree
within the numerical convergence tolerance. This is not a rigorous tail bound.

The maximum finite-H correction to the mass-corrected position-relative
AR(1) radius is 0.0073434%. This is below the declared 0.1% tolerance.

The more important issue is observable identity: production path_observables
and long_run_metastability compute weighted memory-cloud covariance, while
the AR(1) equation describes x minus centroid. The report stores medians of
cloud radii, which also differ from sqrt of an expected squared radius.
For the d=3, A_att=35 slice, the FIFO position RMS is 0.000207307 and the
memory-cloud RMS is 0.000208308, versus measured median 0.000208737.
This proximity is evidence of consistency, not an exact estimator match.

Next priority: match the cloud observable and its summary statistic before
upgrading radius agreement to validation. Preserve historical 0.76%/1.15%
numbers as historical comparisons, not new exact-theory errors.

Reproduction: experiments/current/dynamics/long_runs/paper_i_truncation_audit.py.
Machine-readable results: paper_i_truncation_audit_2026-10-09.json.
