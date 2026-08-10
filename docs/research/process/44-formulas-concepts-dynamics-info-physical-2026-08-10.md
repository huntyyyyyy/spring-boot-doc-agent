---
title: Formulas & concepts — dynamics, information, thermo, physical computing
status: RESEARCH — mathematical companion to process/43 and process/20-theory
date: 2026-08-10
epic_seed: E-DYN1
claim_tiers: Evidenced / Confirmed / Unknown
related:
  - docs/research/process/43-physical-info-dynamics-computing-2026-08-10.md
  - docs/research/process/20-theory-domains-problem-first-gates-2026.md
  - docs/research/process/05-dynamics-neuromorphic.md
do_not:
  - use these formulas as fail_under / merge softeners
  - implement physical substrates from this memo
spec_gate: DRAFT E-DYN1 — concepts SoR; transfer still metaphor/sensor only
---

# Formulas & concepts (not just transfer tables)

Companion to [`43-…`](43-physical-info-dynamics-computing-2026-08-10.md) and
[`20-theory-…`](20-theory-domains-problem-first-gates-2026.md). This file is the
**math/physics content**: named objects + governing equations. Transfer to
doc-engine remains **metaphor / sensor / Refuse** as locked in those memos —
writing \(\kappa(A)\) here does **not** make \(\kappa\) a CI gate.

---

## 1. Dynamical systems

### 1.1 Continuous flow

State \(x \in \mathbb{R}^n\), vector field \(f\):

\[
\dot{x} = f(x),\qquad
\phi_t(x_0) = \text{flow through } x_0.
\]

Equilibrium: \(f(x_\star)=0\). **Lyapunov (asymptotic) stability:** for every
\(\varepsilon>0\) there is \(\delta>0\) so \(\|x(0)-x_\star\|<\delta\) implies
\(\|x(t)-x_\star\|<\varepsilon\) (and \(\to x_\star\) if asymptotic).

**Lyapunov function** \(V\) (strict): \(V>0\) near \(x_\star\) (except at
\(x_\star\)), \(\dot V = \nabla V\cdot f \le 0\) ( \(<0\) for asymptotic).

**LaSalle:** trajectories approach the largest invariant set in
\(\{\dot V=0\}\).

### 1.2 Discrete map / Poincaré

\[
x_{k+1} = F(x_k).
\]

Fixed point \(F(x_\star)=x_\star\). Linearization: Jacobian \(DF(x_\star)\);
spectral radius \(<1\) ⇒ local asymptotic stability (hyperbolic case).

### 1.3 Lyapunov exponents (chaos diagnostic)

For a trajectory, the **largest Lyapunov exponent**

\[
\lambda_{\max}
= \lim_{t\to\infty}\frac{1}{t}\ln\big\|D\phi_t(x)\,v\big\|
\]

(\(v\) generic tangent vector). \(\lambda_{\max}>0\) ⇒ sensitive dependence
(chaos candidate). Full spectrum via Oseledec multiplicative ergodic theorem
`[Evidenced — Skokos 0811.0882; Wilkinson 1608.02843]`.

### 1.4 Bifurcation (concept)

As parameter \(\mu\) varies, qualitative change of phase portrait at
\(\mu_c\) (e.g. Hopf: equilibrium loses stability, limit cycle born;
saddle-node: equilibria collide and vanish).

**doc-engine:** metaphor for policy flip soft→hard — not a Cover% ODE.

---

## 2. Information theory

### 2.1 Shannon entropy

Discrete random variable \(X\) with \(p(x)\):

\[
H(X) = -\sum_x p(x)\log p(x)
\quad(\text{bits if }\log_2).
\]

Joint / conditional:

\[
H(X,Y)=H(X)+H(Y\mid X),\qquad
H(Y\mid X)=-\sum_{x,y}p(x,y)\log p(y\mid x).
\]

### 2.2 Mutual information & channel capacity

\[
I(X;Y) = H(X)-H(X\mid Y) = H(Y)-H(Y\mid X) = H(X)+H(Y)-H(X,Y).
\]

Channel \(p(y\mid x)\):

\[
C = \max_{p(x)} I(X;Y).
\]

**Source coding (Shannon):** compress to \(\approx H(X)\) bits/symbol (i.i.d.).

### 2.3 Kolmogorov complexity

\(K(x) =\) length of shortest program that outputs \(x\) (up to \(O(1)\)).
**Uncomputable** in general — proxies only as sensors.

**doc-engine:** \(H\)/`I` may advise diversity; never replace fail_under.

---

## 3. Statistical mechanics

### 3.1 Canonical ensemble

Energy levels \(E_i\), inverse temperature \(\beta=1/(k_B T)\):

\[
Z = \sum_i e^{-\beta E_i},
\qquad
p_i = \frac{e^{-\beta E_i}}{Z},
\qquad
F = -k_B T\ln Z
\quad\text{(Helmholtz free energy)}.
\]

Mean energy \(\langle E\rangle = -\partial_\beta\ln Z\).

### 3.2 Fluctuation–dissipation (idea)

Near equilibrium, response functions are tied to equilibrium correlation
functions (Onsager–Kubo lineage) `[Evidenced — 0803.0719]`. Far from
equilibrium, standard FDT breaks `[Evidenced — 0707.0751]`.

### 3.3 Order parameter / phase transition

Macroscopic observable \(m(\mu)\) (magnetization, density, …) changes
non-analytically at critical \(\mu_c\) in the \(N\to\infty\) limit.

**doc-engine:** “phase change” jargon for sudden flake storms — not FDT gates.

---

## 4. Linear algebra (substrate)

### 4.1 Eigen / SVD

\[
Av=\lambda v,
\qquad
A = U\Sigma V^\top,
\quad
\Sigma=\mathrm{diag}(\sigma_1\ge\cdots\ge\sigma_r>0).
\]

**Eckart–Young:** best rank-\(k\) approx in 2-norm/Frobenius is truncated SVD.

### 4.2 Condition number

\[
\kappa_2(A)=\frac{\sigma_{\max}(A)}{\sigma_{\min}(A)}
=\|A\|_2\,\|A^{-1}\|_2
\quad(A\text{ invertible}).
\]

Large \(\kappa\) ⇒ \(Ax=b\) amplifies relative input error.

### 4.3 Rank–nullity

\[
\dim\ker A + \mathrm{rank}\,A = n
\quad(A:\mathbb{R}^n\to\mathbb{R}^m).
\]

**doc-engine:** ambient numerics; refuse SVD-as-architecture.

---

## 5. Probability

### 5.1 Concentration (Hoeffding)

Independent bounded \(X_i\in[a_i,b_i]\), \(S=\sum X_i\):

\[
\mathbb{P}\big(S-\mathbb{E}S\ge t\big)
\le \exp\Big(-\frac{2t^2}{\sum_i(b_i-a_i)^2}\Big).
\]

Azuma–Hoeffding: same shape for martingale differences with bounded steps
`[Evidenced — 1212.4663, 1111.1977]`.

### 5.2 Large deviations (Cramér sketch)

For i.i.d. with log-moment generating function \(\Lambda(\theta)=\ln\mathbb{E}e^{\theta X}\),

\[
\mathbb{P}(\bar X_n \approx a)
\sim e^{-n I(a)},
\qquad
I(a)=\sup_\theta\big(\theta a-\Lambda(\theta)\big).
\]

**doc-engine:** flake CIs as sensors; refuse “probably ≥98.7” merge.

---

## 6. Thermodynamics of computation

### 6.1 Laws (macro)

1st: \(\Delta U = Q - W\) (sign convention varies).  
2nd (isolated): \(\Delta S \ge 0\).

### 6.2 Landauer bound

Idealized irreversible erase of one bit at temperature \(T\):

\[
\langle Q\rangle \ge k_B T\ln 2.
\]

Finite-time / nonequilibrium corrections raise the bound
`[Evidenced — 2506.10876; 2310.05449; Wolpert 1905.05669]`.

**doc-engine:** remesure *cost* language (Green AI); not a merge threshold.

---

## 7. Control theory

### 7.1 LTI state space

\[
\dot x = Ax+Bu,\qquad y=Cx.
\]

**Controllable** iff \(\mathrm{rank}[B\ AB\ \cdots\ A^{n-1}B]=n\) (Kalman).  
**Observable** iff \(\mathrm{rank}[C^\top\ A^\top C^\top\ \cdots]=n\).

### 7.2 PID (one controller form)

\[
u(t)=K_P e(t)+K_I\int_0^t e(\tau)\,d\tau+K_D\dot e(t),
\qquad e=r-y.
\]

Valid when \(y\) is a **regulated continuous plant** (e.g. queue length
`[2109.02514]`). **Category error:** set \(e=98.7-\mathrm{Cover\%}\) as merge law
(decision 25).

### 7.3 Hysteresis / dead-band (ops analogue)

Switch on at \(\theta_\mathrm{hi}\), off at \(\theta_\mathrm{lo}<\theta_\mathrm{hi}\)
— suppresses flap (Nagios). **Adopt** for climb targeting / soft bands only.

---

## 8. Physical & unconventional computing

### 8.1 Mass-action kinetics (CRN)

Species concentrations \(c\in\mathbb{R}^s_{\ge 0}\), stoichiometry \(N\), rates \(v(c)\):

\[
\dot c = N\,v(c).
\]

Example unimolecular \(A\xrightarrow{k}B\): \(v=k\,c_A\).

### 8.2 Reaction–diffusion

\[
\partial_t c = N\,v(c) + D\nabla^2 c.
\]

Belousov–Zhabotinsky / Turing patterns: spatial structure as “compute.”
**Refuse** as tip substrate.

### 8.3 Molecular / DNA computing (concept)

Encode combinatorial objects as strands; “gates” = hybridization / strand
displacement (Adleman 1994 Hamiltonian path in DNA). Complexity lives in
**wet parallelism**, not pytest hermeticity.

### 8.4 Reservoir computing (echo-state)

Reservoir state \(r_t\), input \(u_t\), fixed random dynamics \(F\), trained readout \(W\):

\[
r_{t+1} = F(r_t, u_t),
\qquad
\hat y_t = W r_t
\quad(W\text{ trained; }F\text{ frozen}).
\]

**Echo-state property:** reservoir asymptotically forgets IC (fading memory)
(Jaeger 2001; Maass LSM 2002). Physical RC: \(F\) realized by memristors,
chemistry, ferrofluid, … `[2403.01827]`, Nature formose 2024,
`[2211.08152]`.

**Allowed analogy only:** climb/sensors = rich \(r_t\); oracle boolean = readout
constraint — never ship \(F\) hardware.

### 8.5 Neuromorphic / LIF sketch

Leaky integrate-and-fire membrane:

\[
\tau \dot V = -(V-V_\mathrm{rest}) + RI(t);
\quad
\text{if }V\ge V_\mathrm{th}\text{: spike, reset}.
\]

Event-driven chips (Loihi, BrainScaleS) exploit sparsity. SpikeSlicer uses
SNN saliency on DVS `[2410.02249]`. **Refuse** runtime; **Adopt** debounce
metaphor only.

### 8.6 In-memory / crossbar MAC

Ideal ohmic crossbar: voltages \(v\), conductances \(G\), currents

\[
i = G v
\]

implements matrix–vector multiply in place (memristor IMC). Addresses von
Neumann data-movement energy — irrelevant to citation SoT.

### 8.7 Ionic computing (concept)

Information carriers = ions in electrolytes / gels; dynamics closer to
Nernst–Planck electrodiffusion than CMOS FETs. Research substrate — **Refuse** tip.

---

## 9. Map: formula → doc-engine role

| Formula / concept | Role |
| --- | --- |
| \(\dot x=f(x)\), \(\lambda_{\max}\) | Metaphor (thrash / stability talk) |
| \(H\), \(I\), \(C\) | Optional diversity **sensor**; Refuse as floor |
| \(Z\), \(F\), FDT | Metaphor only |
| \(\kappa(A)\), SVD | Numeric substrate **Embody** |
| Hoeffding / LDP | Flake **sensor** language |
| \(k_B T\ln 2\) | Cost **language**; Refuse as gate |
| PID \(u(e)\) | Refuse for Cover%; caps/hysteresis OK |
| \(\dot c=Nv(c)\), RD PDE | Refuse tip |
| \(r_{t+1}=F(r_t,u_t),\ \hat y=Wr\) | Pattern analogy climb→oracle |
| LIF / \(i=Gv\) | Refuse tip |

---

## 10. References (formula sources)

Skokos `0811.0882` · Wilkinson `1608.02843` · Shannon 1948 · Kolmogorov 1965 ·
Marconi `0803.0719` · Zhang `1510.08532` · Raginsky–Sason `1212.4663` ·
Landauer 1961 · Chattopadhyay `2506.10876` · Wolpert `1905.05669` · Kalman ·
Simon `2109.02514` · Jaeger 2001 / Maass 2002 · Adleman Science 1994 ·
memristor RC `2403.01827` · SpikeSlicer `2410.02249`.

Local transfer locks: `05`, `20-theory-…`, `43-…`, decisions **25–28**.
