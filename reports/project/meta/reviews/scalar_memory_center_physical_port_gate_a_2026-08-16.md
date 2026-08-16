# Gate A: physical port of the scalar memory center

Date: 2026-08-16.

Decision: **physical center-port not identified; mathematical center-port
retained**.

Gate A was evaluated immediately after the
[claim-scoped P0 pass](../preregistration/scalar_memory_center_mechanics_p0_audit_2026-08-16.md).
No new response trace, seed or sealed parameter cell was opened. The result is
therefore an analytic non-identifiability result for the physical port, not a
failed numerical fit.

## Registered question

The charter requires an external interaction energy or virtual-work
principle that identifies the microscopic input recipient and derives

\[
F_c=-\partial_c U_{\rm ext},
\qquad
\delta W=F_c\cdot\delta c.
\]

Mathematical passivity of \((f,\dot c)\) alone was registered as insufficient
for physical mass. This audit applies that criterion to the frozen K0 center
without changing its dynamics or port normalization.

## 1. Which variable actually receives the input

In the registered local discrete model,

\[
x_{n+1}=x_n-g(x_n-c_n)+\alpha f_n+\varepsilon\xi_n.
\]

Thus the only implemented actuator term is added to the current **visible
state \(x\)**. The canonical model contains neither an external actuator
coordinate nor a registered interaction energy that says which displacement
is power-conjugate to its input.

This closes A0 positively: the microscopic recipient is known. It does not
close the desired center conjugacy. In a first-order state realization, the
equation receiving a force need not itself be the configuration coordinate:
a Newtonian force enters the velocity or momentum equation while its power is
\(F\cdot\dot q\). Input location alone therefore selects neither \(f\,dx\)
nor \(f\,dc\).

## 2. Two inequivalent physical-port hypotheses fit the same input term

The center and relative coordinate obey the identity

\[
x_n=c_n+r_n.
\]

If the additive input is independently declared to be a physical force
conjugate to \(x\), its virtual work transforms exactly as

\[
f_n\cdot\Delta x_n
=f_n\cdot\Delta c_n+f_n\cdot\Delta r_n.
\]

The center ledger used in the earlier numerical gate is only the first term.
The omitted term is not generally zero. Discrete summation by parts gives

\[
\sum_{n=0}^{N-1} f_n\cdot\Delta r_n
=f_{N-1}\cdot r_N-f_0\cdot r_0
-\sum_{n=1}^{N-1}(f_n-f_{n-1})\cdot r_n.
\]

For a constant force it reduces to an endpoint contribution; for a varying
force it also contains an explicit drive-history term. Smooth pulses,
multisines and chirps therefore do not permit this residual to be silently
renamed as center work. Counting both \(f\,dx\) and \(f\,dc\) as external
power would double-count their shared contribution. This is a valid
conditional ledger for an \(x\)-coupled actuator; it is not evidence that the
actuator must be \(x\)-coupled.

Conversely, restore memory time \(\tau\), input mobility \(\mu\) and local
relaxation \(\kappa\):

\[
\tau\dot c=r=x-c,
\qquad
\dot x=-\kappa r+\mu F.
\]

Writing \(v=\dot c=r/\tau\) gives

\[
{\tau\over\mu}\dot v
+{1+\kappa\tau\over\mu}v=F.
\]

Now stipulate an effective interaction \(U_{\rm ext}(c,Q)\) with an external
coordinate \(Q\), and define \(F=-\partial_cU_{\rm ext}\). The
Lagrange--d'Alembert equation for \(c\) is exactly the equation above. Under
the invertible state change \(x=c+\tau v\), it becomes

\[
\dot x=-\kappa(x-c)+\mu F,
\]

which is the registered continuum input law. Thus a center-conjugate force is
**dynamically realizable by the same additive \(x\)-equation**. This is the
usual situation in which force enters a velocity-like state equation. It
also shows why the code-level input location cannot choose between the
\(x\)- and \(c\)-work hypotheses.

## 3. Effective center ledger closes conditionally

For

\[
S={|r|^2\over2\mu\tau}
={1\over2}{\tau\over\mu}|\dot c|^2
\]

one obtains

\[
\dot S
=F\cdot\dot c
-{1+\kappa\tau\over\mu}|\dot c|^2.
\]

If the external coordinate \(Q\) is dynamical and receives the reciprocal
force \(-\partial_QU_{\rm ext}\), the derivative of center kinetic energy,
external energy and \(U_{\rm ext}\) closes with the displayed nonnegative
dissipation. If \(Q\) is prescribed, \(F\cdot\dot c\) is the actuator supply.
No simultaneous \(f\,dx\) ledger is then counted.

This proves more than an arbitrary second difference: a physically
realizable **effective** center-coupled architecture exists and uses the same
continuum state equation. It does not prove that the already registered K0
actuator was that architecture, because \(U_{\rm ext}\), \(Q\), reciprocity
and calibration were absent from its microscopic contract.

## 4. Finite-H microscopic coupling remains unclosed

With

\[
q=1-\alpha,
\qquad
b_H={\alpha\over1-q^H},
\]

the exact normalized finite-\(H\) center update has the form

\[
c_{n+1}=q c_n+b_H x_{n+1}-b_Hq^H x_{{\rm oldest},n}.
\]

Hence a virtual variation of \(c_H\) is distributed over the current and
retiring history samples. The continuum construction above does not by itself
specify how \(U_{\rm ext}(c_H,Q)\) acts on those finite-history variables, nor
does the old prescribed-force experiment contain the reciprocal \(Q\) ledger.
The native finite-H update and a center-coupled actuator agree in the tested
continuum response, but exact microscopic equivalence and its boundary power
term have not been derived. That missing contract is decisive for physical A.

## 5. The proposed phase/COM semantics do not repair A

In K0, \(x\), every stored history point and \(c\) all live in the same
Euclidean state space, which is why \(r=x-c\) is defined. Declaring \(x\) to
be an intrinsic phase and \(c\) a spatial material COM would require an
explicit map between different state spaces, periodic identification and a
new virtual-work law. No such map is present, and the separate S1 P0 has no
candidate. The semantic proposal is therefore a future architecture
hypothesis, not evidence that closes the current port.

## Gate table

| component | decision | reason |
|---|:---:|---|
| A0 microscopic input recipient | pass | additive term acts on current \(x\) |
| A1 competing \(x\)-work ledger | pass, conditional | exact residual \(f\,dr\) is retained |
| A2 effective \(U_{\rm ext}(c,Q)\) realization | pass, conditional | transforms to the same continuum \(x\)-input law |
| A3 mathematical center passivity | pass | positive storage and dissipation close |
| A4 microscopic port selection and finite-H boundary ledger | **fail** | absent from the frozen K0 external-system contract |
| overall physical center port | **not identified** | both port hypotheses fit the same input term; A4 is necessary |

The machine-readable decision is recorded in
[the Gate-A JSON](scalar_memory_center_physical_port_gate_a_2026-08-16.json).

## Prospective A2 follow-up

The subsequently frozen and executed
[finite-H A2 certificate](../../../dynamics/limits/scalar_memory_center_finite_h_port_a2_2026-08-16.md)
passes all registered cells. Its global Small-Gain/Positive-Real bound shows
that the exact retiring-history term admits a passive input/output
realization, and a newly declared discrete-gradient interaction closes a
reciprocal effective boundary ledger. The
[critical review](scalar_memory_center_finite_h_port_a2_review_2026-08-16.md)
checks the pole cancellation, the removable \(z=1\) singularity and the
claim boundary independently.

This narrows, but does not reverse, the Gate-A decision. A2 constructs a new
effective wrapper; it does not find that wrapper in the frozen microscopic
K0 contract or select it over the conditional \(x\)-work hypothesis. Thus the
finite-\(H\) mathematical objection is closed, while microscopic physical
port selection remains open.

## Stop-rule consequences

- The strongest surviving statement is a positive passive
  center-inertial **filter realization** under an explicit mathematical port.
- Physical B, C, the physical-work portion of E and an additive-mass F1 claim
  are blocked by A. Running their parameter panels now would not identify the
  missing microscopic port.
- A separately labelled filter-scaling robustness study could still test the
  prediction \(m_{\rm filter}=\tau/\mu\), but it would be system
  identification, not a physical-mass gate, and needs its own prospective
  protocol.
- D0--D5 remain sealed for the independent reason that no S1 candidate
  exists.

## Evidence, inference and hypothesis

- **Evidence:** the registered input is applied in the \(x\) state equation;
  an \(x\)-conjugate hypothesis leaves the exact \(f\,dr\) term; a
  center-conjugate effective potential transforms to the same continuum input
  equation; finite-\(H\) center coupling is distributed over history; the
  reduced center port is passive.
- **Inference:** the existing simulation supports an effective inertial
  readout but cannot identify which physical displacement is conjugate to the
  prescribed input.
- **Open hypothesis:** a newly specified reciprocal
  \(U_{\rm ext}(c_H,Q)\), including its finite-history boundary work, could
  make the center port physical. That is a new, prospectively tested actuator
  contract rather than a reinterpretation of the old input.
