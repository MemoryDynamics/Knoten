# Model-vocabulary remediation audit

Date: 2026-09-02

Verdict: **`notation-contract-required-before-p5-remediation`**

## Scope

This target-free audit compares the active Paper-I model language, center
filter documentation, P5 reverse specification, production field names and
serialized P5 keys. It does not change production dynamics or authorize a
target run.

## Evidence

Five material collisions are present:

1. $\beta$ is the general Paper-I deposition strength, while
   `OrbitCenterReadout.beta` is a complex notch response.
2. $c_n$ is the memory center, while the initial P5 reverse specification
   used $c_j$ for notch-filter coefficients.
3. $g_H$ is the native local restoring gain, while an unqualified $g$ was
   introduced for the write gain.
4. $\mu$ is used in the established center-mechanics reduction, while P5 used
   it without a qualifier for write mobility.
5. $\varepsilon$ is the stochastic displacement amplitude, while
   `epsilon64` denotes binary64 unit roundoff and `epsilon_scale` denotes a
   tolerance.

The reverse specification also used $B_H$ once for the raw finite sum with
$B_H(1)=1-q^H$, whereas the established center-filter page reserves $B_H$ for
the normalized readout with $B_H(1)=1$. This is a genuine equation-language
inconsistency, not merely typography.

Deeper sections of the active theoretical context additionally reuse local
$g$, $c$ and $\mu$ coefficients across distinct subsystem proposals. Those
sections require a model-by-model qualification pass; bulk replacement would
risk changing mathematical meaning.

## Canonical resolution

The active contract reserves the Paper-I core symbols
$(\alpha,\varepsilon,\eta,\sigma,M_0,H,N)$ and the qualified general
deposition strength $\beta_\rho$. The normalized center filter is $B_H$; its
raw sum is $W_H=M_HB_H$. The loop/port layer uses $b_s$, $a_j^{(s)}$,
$\gamma_{\rm w}$, $\mu_{\rm w}$ and $\kappa_{\rm pair}$. The older
center-mechanics port is qualified separately by $\mu_F$ and $\kappa_c$.
Binary64 roundoff is $u_{64}$.

## Migration boundary

Active prose and equations may adopt the contract immediately. Production
fields and serialized keys must not be bulk-renamed: P5 provenance hashes,
protocols, incidents and potential readers depend on the existing names. A
code migration therefore requires a new schema version, compatibility tests
and explicit review together with the other P5 remediation work.

## Scientific consequence

The collision does not falsify the algebra already checked, but it weakens
traceability from Paper I to P5 and makes dimensional or physical
misinterpretation easier. Resolving names is necessary for reviewability; it
does not create evidence for interaction, inertia or mass.

## Decision

The notation contract is a blocking input to P5 remediation. No target access
is opened. Historical artifacts remain immutable; all new active equations,
tests and schema proposals must use or explicitly map to the canonical
vocabulary.
