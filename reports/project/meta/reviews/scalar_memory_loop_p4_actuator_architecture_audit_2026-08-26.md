# P4 architecture audit: linear orbit-center source/write actuation

Date: 2026-08-26.

Decision: **select one source/write architecture for P4 preregistration; do
not promote the finite-memory records to autonomous massive carriers.**

The selected primitive coupling is exactly linear. The native L3 loop map
remains the full nonlinear finite-memory map. No Taylor truncation, second
difference, momentum variable or mass coefficient is inserted. Linearization
may later be used only as a weak-response comparator, not to establish the
actuator identity or its work ledger.

The audit also corrects an important coordinate issue. The raw normalized
memory readout $c_H=B_Hx$ is translation equivariant, but on the rotating wave
it rotates with nonzero amplitude. It is therefore not, by itself, a pure
orbit center. P4 will use an exact linear notch readout derived from the same
$B_H$, not reinterpret raw $c_H$ as a material center of mass.

## 1. Frozen native ingredients

Let the planar FIFO state be

$$
h_n=(h_{0,n},\ldots,h_{H-1,n}),\qquad h_{0,n}=x_n,
$$

with

$$
q=1-\alpha,\qquad
\bar w_j={\alpha q^j\over1-q^H},\qquad
c_n=\sum_{j=0}^{H-1}\bar w_jh_{j,n}.
$$

For chirality $s\in\{+1,-1\}$, the reviewed rotating history has the form

$$
h_{j,n}=C+R\exp\!\left[i(\phi_n-sj\theta)\right].
$$

Define the exact finite-sum response at the registered angular increment,

$$
\beta_s
=B_H(e^{is\theta})
=\sum_{j=0}^{H-1}\bar w_j e^{-isj\theta}.
$$

Then

$$
c_n=C+\beta_s(x_n-C).
$$

Thus raw $c_H$ contains both the common translation $C$ and the rotating
internal component. At L3, $|\beta_s|R=0.5058810073761263$, so this is not a
small correction.

## 2. Exact linear orbit-center readout

Because $\beta_s\ne1$, solve the preceding identity for the orbit center:

$$
C_{s,n}
={c_n-\beta_sx_n\over1-\beta_s}
=\sum_{j=0}^{H-1}a_{s,j}h_{j,n},
$$

where

$$
a_{s,0}={\bar w_0-\beta_s\over1-\beta_s},\qquad
a_{s,j}={\bar w_j\over1-\beta_s}\quad(j\ge1).
$$

Complex multiplication denotes the corresponding real $2\times2$ rotation-
scale matrix. Three identities are exact:

$$
\sum_j a_{s,j}=1,
$$

$$
A_s(1)=1,
\qquad
A_s(e^{is\theta})=0,
$$

for

$$
A_s(z)={B_H(z)-\beta_s\over1-\beta_s}.
$$

The readout therefore passes a common translation with unit gain and removes
the registered rotating component exactly. It uses $q,\alpha,H,B_H$ and the
already certified signed $\theta$; it uses neither a fitted response pole nor
the target radius.

For the positive L3 branch,

$$
\beta_+=0.28847300317511804-0.45107951349124853i,
$$

$$
a_{+,0}=0.002499571092111443+0.6323751736574267i,
\qquad |a_{+,0}|^2=0.3999046081139050.
$$

The negative branch is the complex conjugate. Applying the wrong-chirality
notch to the positive target leaves a rotating amplitude
$1.0117541055435313$, rather than zero; chirality is therefore an explicit
registered input, not silently optimized from the response.

## 3. Adjoint microscopic force and exact work identity

Let $M(a)$ be the real matrix representing multiplication by the complex
number $a$. A virtual variation obeys

$$
\delta C_s=\sum_jM(a_{s,j})\,\delta h_j.
$$

For a generalized orbit-center force $F_C$, the adjoint slot forces are

$$
f_j=M(a_{s,j})^TF_C.
$$

They satisfy both exact virtual work and force balance:

$$
\sum_jf_j\cdot\delta h_j=F_C\cdot\delta C_s,
\qquad
\sum_jf_j=F_C.
$$

The P4 source/write contract actuates only the new visible slot with the
positive first-order mobility

$$
h_{0,n+1}=\widetilde h_{0,n+1}+\alpha f_{0,n},
$$

where $\widetilde h_{n+1}$ is the exact nonlinear native FIFO update. The
archived-slot adjoint forces are constraint reactions carried by the explicit
age/source/sink substrate. Since

$$
h_{j,n+1}=h_{j-1,n}\quad(j\ge1),
$$

the finite-step center work splits without approximation:

$$
F_C\cdot\Delta C_s
=f_0\cdot(h_{0,n+1}-h_{0,n})
+\sum_{j=1}^{H-1}f_j\cdot(h_{j-1,n}-h_{j,n}).
$$

The first term is write-head work; the second is signed age/source/sink work.
Dropping the second term is precisely the finite-memory boundary-ledger error
that P4 must falsify. Merely defining $F\,dx$ or $F\,dc_H$ by fiat would not
close this identity.

## 4. Reciprocal external coordinate without inserted inertia

P4 will couple $C_s$ to one external actuator coordinate $Q$ through the
translation- and rotation-invariant harmonic interaction

$$
U(C_s,Q)={k\over2}|C_s-Q|^2.
$$

The midpoint discrete-gradient forces are

$$
F_C=-k\,{(C_{s,n+1}-Q_{n+1})+(C_{s,n}-Q_n)\over2},
\qquad F_Q=-F_C.
$$

The actuator itself is first order,

$$
Q_{n+1}=Q_n+\alpha\nu F_Q,
\qquad \nu=|a_{s,0}|^2>0.
$$

Because the write step changes $C_s$ by
$\alpha|a_{s,0}|^2F_C$, the implicit interaction has the unique closed form

$$
F_C=-{k\over 2+\alpha k(|a_{s,0}|^2+\nu)}
\left[(C_{s,n}-Q_n)+(\widetilde C_{s,n+1}-Q_n)\right].
$$

No nonlinear solve, fitted coefficient or second-order equation is hidden in
this step. With $W_Q=F_Q\cdot\Delta Q$, the discrete-gradient identity is

$$
\Delta U+W_{\rm write}+W_{\rm age/source/sink}+W_Q=0.
$$

The force pair is equal and opposite at the $(C_s,Q)$ port, while the slot
forces and substrate reactions expose where that generalized force enters the
FIFO. The positive mobilities also give nonnegative input-induced write and
actuator dissipation. The native loop remains an open source/sink system; the
audit does not assume its autonomous dynamics has a conserved Hamiltonian.

## 5. Why the alternative carrier architecture is not selected

Promoting all FIFO records to autonomous moving carriers would require new
carrier mobilities, deposition dynamics, constraints and an autonomous rule
for retirement. It would change the $k=0$ L3 map whose existence, local
stability and finite-ensemble attraction were just established. A
second-order carrier rule would also risk inserting the desired inertia.

The source/write architecture instead has four discriminating advantages:

1. $k=0$ is exactly the reviewed native L3 map.
2. The orbit-center readout and its adjoint are exact finite sums.
3. Every new dynamic equation is first order with positive mobility.
4. The missing age/retirement work appears as an explicit measured ledger,
   rather than being relabelled as center work or discarded.

This selection is methodological, not ontological. It does not prove that
nature uses a read/write substrate or that the stored records are matter.

## 6. Evidence, inference, hypothesis and stop rules

**Evidence:** the $B_H$ finite sum, the notch identities, adjoint force
balance, work decomposition and midpoint interaction ledger follow
algebraically. Raw $c_H$ carries a large rotating component at L3.

**Inference:** an exactly linear, chirality-conditioned orbit-center port is a
cleaner primitive for P4 than coupling an external coordinate directly to raw
$c_H$. It preserves the nonlinear loop map at zero coupling and makes every
finite-history boundary term observable.

**Hypothesis for prospective testing:** weak reciprocal coupling through this
port moves the orbit center while preserving the quotient loop and closes the
declared ledger on the full nonlinear L3 trajectory.

P4 must fail or remain ledger-only if the nonlinear loop is not preserved, if
the center does not respond above a frozen floor, or if any force/work,
translation, rotation, reflection, wrong-chirality or channel-off control
fails. Even a full P4 pass establishes only this actuator architecture and
its operational work coordinate. It does not establish material center of
mass, additive momentum, physical mass, a unique port, two-loop interaction
or an internal $S^1$.
