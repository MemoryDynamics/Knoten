# Scalar-memory center inertial-port protocol

Date: 2026-08-16.

Status: center-output work, pulse family, prospective seeds, competing
signatures and thresholds fixed before implementation of center-work
instrumentation and before any seed-16--20 response was generated or
inspected.

Threshold calibration used only the closed-form continuum equations and the
already existing exact finite-H linear recursion. It did not use prospective
nonlinear formation data.

## Question and claim boundary

The preceding force/work gate used the current visible coordinate \(x\) as
the output and \(f\,dx\) as supplied work. It selected the overdamped-memory
signature and rejected a regular finite-mass interpretation of that
particular input/output port.

The same augmented local state contains the normalized memory center \(c\)
and relative coordinate \(r=x-c\). This protocol asks a different question:
does the force-to-center port, with \(f\,dc\) as work, realize a positive
effective inertial coordinate?

This is not a retrospective relabeling of the visible-\(x\) result. The
output observable and work pairing are changed prospectively. Even a positive
result establishes only a dimensionless effective center inertia in the
registered local scalar slice. It does not establish SI mass, a particle
interpretation, or uniqueness of this readout.

## Fixed input and center output

The microscopic force placement remains exactly the already registered
additive input

\[
x_{n+1}=x_n-\eta\nabla V_H(x_n)
          +\alpha f_n e+\varepsilon\xi_n.
\]

No force term is added directly to the memory center. The output is the
normalized finite-H center \(c_n\) already computed from the deposited
history. The relative state is \(r_n=x_n-c_n\).

For each branch, supplied center work is fixed as

\[
W_{c,N}=\sum_{n=0}^{N-1}
f_n e\cdot(c_{n+1}-c_n).
\]

Mirrored \(+f\) and \(-f\) branches share formation and continuation noise.
The registered forced work is their even average

\[
W_c^{\rm pair}={W_c^{(+)}+W_c^{(-)}\over2}.
\]

This removes the term linear in the common unforced center increment. The odd
center and relative responses are normalized by twice the impulse amplitude,
as in the preceding visible-port gate.

## Local positive-inertial candidate

With \(g=\chi\alpha\), \(\varepsilon^2=2D\alpha\),
\(\Gamma=1+\chi\), and \(t=\alpha n\), the local untruncated state satisfies

\[
dc=r\,dt,
\qquad
dr=(-\Gamma r+f)\,dt+\sqrt{2D}\,dW.
\]

Therefore

\[
\ddot c+\Gamma\dot c=f+\sqrt{2D}\,\dot W.
\]

Under the fixed input normalization this is the free inertial Langevin form

\[
m\ddot c+\gamma\dot c=f+\sqrt{2D}\,\dot W
\]

with registered predictions

\[
m=1,\qquad \gamma=\Gamma=5.
\]

The deterministic force-to-center-velocity transfer is

\[
{\dot C(s)\over F(s)}={1\over s+\Gamma},
\]

which has zero high-frequency feedthrough. Its positive storage

\[
E={1\over2}|r|^2
\]

satisfies

\[
\dot E=f\cdot\dot c-\Gamma|\dot c|^2.
\]

The visible coordinate remains

\[
x=c+r=c+\dot c,
\]

so its different transfer

\[
{\dot X(s)\over F(s)}={s+1\over s+\Gamma}
\]

and its preceding negative effective low-frequency mass are not changed by
this protocol.

## Resolved rectangular pulses and order of limits

A singular one-native-step impulse makes discrete endpoint work convention
dependent. This protocol therefore uses resolved rectangular pulses.

For width \(\delta\) and integrated input \(J\),

\[
f(t)={J\over\delta}
\quad(0\le t<\delta),\qquad f(t)=0\quad(t\ge\delta).
\]

At native cadence the profile is exactly \(1/\delta\) for
\(\delta/\alpha\) integer steps and zero afterwards, so that
\(\alpha\sum_n f_n=J\) without quadrature fitting.

The registered order is:

1. test \(\alpha\to0\) at fixed \(\delta_0=0.2\);
2. on the finest registered alpha, test the resolved width ladder
   \(\delta\in\{0.4,0.2,0.1,0.05\}\).

The smallest pulse still contains 20 native steps. The ladder is a
finite-resolution approach diagnostic, not a proof of a uniform double
limit.

For \(z=\Gamma\delta\), the continuum predictions per unit impulse are

\[
{r(\delta)\over J}={1-e^{-z}\over z},
\]

\[
{\Delta c(\delta)\over J}
=\delta\,{z-1+e^{-z}\over z^2},
\]

and

\[
{W_c\over J^2}={z-1+e^{-z}\over z^2}.
\]

Thus, after the continuum limit,

\[
{r(\delta)\over J}\longrightarrow1,\qquad
{\Delta c(\delta)\over J}\longrightarrow0,\qquad
{W_c\over J^2}\longrightarrow{1\over2}
\]

as \(\delta\to0\). This is the regular finite-mass impulse signature.

## Fixed model family and prospective data

The main alpha family is inherited unchanged:

- \(d=3\), \(\chi=4\), \(D=10^{-4}\), \(\alpha H=12\), \(M_0=1\);
- \(A_{\rm rep}=1\), \(A_{\rm att}=35\),
  \(\sigma_{\rm rep}=1\), \(\sigma_{\rm att}=3\);
- \(\alpha\in\{0.04,0.02,0.01,0.005,0.0025\}\);
- formation duration 20 memory times;
- 1.2 memory times of free response after each pulse;
- new formation seeds 16--20;
- fixed noise convention 20260817 plus formation seed;
- force axis equal to coordinate 1;
- exact Brownian coarsening from \(\alpha=0.0025\) to every coarser cell.

Let

\[
R_{\rm cont}=\sqrt{dD/(1+\chi)}.
\]

Both registered impulse strengths are retained:

\[
J/R_{\rm cont}\in\{0.005,0.01\}.
\]

The main matched-alpha family uses \(\delta_0=0.2\). The full width ladder is
run at the holdout \(\alpha=0.0025\) for all five prospective formation
seeds and both strengths, with common noise prefixes.

The stationary center-MSD check uses only the holdout alpha, 65,536 local
linear paths, RNG seed 20260817, and the fixed fit window
\(t\in[2\alpha,16\alpha]\).

## Fixed references and estimators

The primary response reference is the exact native finite-H linear recursion
under the same rectangular force cells. The secondary reference is the
closed-form continuum rectangular-pulse response above.

The post-pulse rate \(\widehat\Gamma\) is fitted only after the force has
returned to zero. With pulse-end relative response \(v_\delta=r(\delta)/J\),
the registered input-gain, mass and damping estimators are

\[
\widehat B=
v_\delta\,{\widehat\Gamma\delta
\over1-e^{-\widehat\Gamma\delta}},
\qquad
\widehat m={1\over\widehat B},
\qquad
\widehat\gamma={\widehat\Gamma\over\widehat B}.
\]

No response coefficient is used to renormalize the applied force.

For the paired odd relative response \(h_r\), the discrete center ledger uses

\[
K_n/J^2={1\over2}|h_{r,n}|^2,
\]

\[
Q_n/J^2=
\Gamma\alpha\sum_{k<n}
{|h_{r,k}|^2+|h_{r,k+1}|^2\over2},
\]

and residual

\[
L_n/J^2=K_n-K_0-W_{c,n}/J^2+Q_n/J^2.
\]

The trapezoidal dissipation is fixed before execution. At finite alpha the
ledger need not vanish exactly but must converge.

For stationary \(r\), the continuum center MSD per ambient coordinate is

\[
\operatorname{MSD}_c(t)
={2D\over\Gamma^3}
\left(\Gamma t-1+e^{-\Gamma t}\right)
={D\over\Gamma}t^2+O(t^3).
\]

An overdamped position driven directly by white noise instead has a linear
short-time MSD.

## Recorded diagnostics

For every main alpha, seed and impulse strength:

1. integrated input and force-off clone residual;
2. odd center, relative and visible responses;
3. mirror-even leakage, cross-axis response and strength dependence;
4. simultaneous forced/control memory-radius ratios;
5. raw branch and paired-even center work;
6. identity between raw paired work and odd-response work;
7. errors against exact finite-H and continuum responses;
8. post-pulse rate, input gain, inferred mass and inferred damping;
9. center kinetic/work/dissipation ledger;
10. exact recurrence residual.

For the holdout width ladder:

1. pulse-end center displacement and relative velocity per impulse;
2. first force-off center velocity;
3. center-work coefficient;
4. inferred mass and damping;
5. monotonic approach toward the impulse predictions.

The MSD arm records Monte Carlo, exact discrete covariance and continuum
center MSDs and their fixed-window log-log slopes.

## Gates fixed before prospective execution

### G0: port, numerical and perturbative validity

All are required:

- integrated input error at most \(10^{-14}\);
- force-off clone maximum state and work residual at most \(10^{-14}\);
- exact forced finite-H recurrence residual at most \(10^{-12}\);
- raw paired center work and odd-response center work agree within
  \(10^{-12}\) relative;
- median mirror-even leakage at most \(10^{-3}\) and maximum at most
  \(10^{-2}\);
- median strength-response difference at most \(10^{-3}\) and maximum at
  most \(10^{-2}\);
- all memory radii finite and positive with
  \(\max R/\sigma_{\rm rep}\le0.02\);
- every simultaneous forced/control radius ratio lies in \([0.95,1.05]\);
- every registered pulse width is an exact integer number of native steps.

If G0 fails, every physical discrimination gate is blocked.

### G1: center-response, work and reference closure

All are required:

- every main alpha cell has median normalized RMS center- and
  relative-response error at most 0.01 against the exact finite-H reference;
- every main alpha cell has median relative post-pulse rate error at most
  0.01 against the exact finite-H response;
- every main alpha cell has median center-work error at most 0.01 against the
  exact finite-H reference;
- at the \(\alpha=0.0025\) holdout, median center- and relative-response errors
  against the continuum pulse are each at most 0.01;
- holdout center-work error against the continuum pulse is at most 0.03;
- the exact finite-H ledger residual per work is at most 0.02 at the holdout
  and smaller there than at \(\alpha=0.01\);
- the paired nonlinear ledger residual per work is at most 0.03 at the
  holdout and smaller there than at \(\alpha=0.01\);
- Monte Carlo center MSD differs from its exact discrete reference by at most
  0.01 normalized RMS on the fixed window;
- exact discrete center MSD differs from the continuum reference by at most
  0.02 normalized RMS on the fixed window.

### G2I: positive center-inertial signature

All are required:

- holdout main-pulse inferred mass lies in \([0.95,1.05]\);
- holdout main-pulse inferred damping lies in \([4.8,5.2]\);
- every width-ladder pulse has positive pulse-end and first force-off center
  velocity;
- center displacement per impulse strictly decreases as pulse width
  decreases;
- pulse-end velocity per impulse and center-work coefficient strictly
  increase as pulse width decreases;
- at \(\delta=0.05\), center displacement per impulse is at most 0.03;
- at \(\delta=0.05\), first force-off center velocity per impulse lies in
  \([0.84,0.93]\);
- at \(\delta=0.05\), center work satisfies
  \(W_c/J^2\in[0.44,0.52]\);
- the stationary center-MSD slope lies in \([1.9,2.1]\).

### G2O: competing overdamped-center signature

For the registered overdamped alternative
\(\Gamma\dot c=f+\) white noise, all are required:

- at \(\delta=0.05\), center displacement per impulse lies in
  \([0.15,0.25]\);
- the magnitude of the first force-off center velocity per impulse is at
  most 0.05;
- at \(\delta=0.05\),
  \(\delta W_c/J^2\in[0.15,0.25]\);
- the stationary center-MSD slope lies in \([0.9,1.1]\).

G2O is an explicit competing signature, not the Boolean negation of G2I.
Mixed outcomes are inconclusive.

## Decision language

- G0 and G1 pass, G2I passes and G2O fails:
  center-port-supports-positive-effective-inertia.
- G0 and G1 pass, G2O passes and G2I fails:
  center-port-supports-overdamped-position.
- G0 and G1 pass but neither alternative is uniquely selected:
  center-port-discrimination-inconclusive.
- G0 fails: center-port-experiment-inadequate.
- G0 passes and G1 fails: center-port-reference-closure-failed.

Even the positive-inertial outcome remains a port- and observable-conditional
effective result. A physical mass claim would require an independent unit
map, justification that \(c\) is the physical coordinate conjugate to the
applied force, robustness beyond the local Taylor slice, and transfer to
unseen force profiles.
