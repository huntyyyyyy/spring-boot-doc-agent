---
title: Six quality papers (May–Aug 2026) — cross-domain transfer pack
status: RESEARCH COMPLETE — Spec Draft
date: '2026-08-10'
claim_tiers: Evidenced / Confirmed / Unknown
window: 2026-05-01 .. 2026-08-10
selection_rule: >-
  Each paper must (a) publish in window, (b) be primary arXiv/venue quality,
  (c) cross ≥2 taxonomy domains from the user science+SE list,
  (d) map to Embody/Adopt/Refuse + locked E-DYN1 transfers only.
---

# Six papers (May–August 2026) — cross-reference pack

Published dates verified via arXiv Atom API (`export.arxiv.org`) on 2026-08-10.

## Selected six

| # | arXiv | Published (UTC) | Title (short) | Primary domains crossed |
| --- | --- | --- | --- | --- |
| P1 | [2606.01385](https://arxiv.org/abs/2606.01385) | 2026-05-31 | Bridging Requirements and Architecture (MAAD) | RE, constraints, ATAM, frameworks, multi-agent |
| P2 | [2605.29013](https://arxiv.org/abs/2605.29013) | 2026-05-27 | Local observability + MHE training of FNNs | Control theory, observability, nonlinear DST, probability |
| P3 | [2606.22621](https://arxiv.org/abs/2606.22621) | 2026-06-21 | Multi-level resistive synapses / memristive IMC | Analog, in-memory, lin.alg., info theory, neuromorphic, physics |
| P4 | [2607.27341](https://arxiv.org/abs/2607.27341) | 2026-07-29 | Quantum vs classical erasure (Landauer) | Information theory, thermodynamics, physics, constraints (resource) |
| P5 | [2608.00484](https://arxiv.org/abs/2608.00484) | 2026-08-01 | Digital→physical RC via dynamics matching | Physical RC, nonlinear DST, control, physics |
| P6 | [2607.06341](https://arxiv.org/abs/2607.06341) | 2026-07-07 | Harnessing code agents for automatic software verification (Aria/Iris) | Formal frameworks, agentic verify loop, Rust/Iris proofs |

**Near-misses (also in window; cite if deepening):**  
2607.14504 RSA/sub-Nyquist reservoirs · 2607.23285 photonic RC networks ·  
2607.16183 thermodynamic computing blueprint · 2606.08431 neural-ODE controllability ·  
2607.27844 nanoparticle neuromorphic RC · 2607.05457 Gramian compression.

---

## Cross-reference matrix (paper × domain)

Legend: ● primary · ○ secondary · — absent

| Domain | P1 | P2 | P3 | P4 | P5 | P6 |
| --- | --- | --- | --- | --- | --- | --- |
| Information theory | — | — | ● | ● | ○ | — |
| Neuromorphic | — | — | ● | — | ○ | — |
| Physical reservoir computing | — | — | ○ | — | ● | — |
| Analog computing | — | — | ● | — | ○ | — |
| In-memory computing | — | — | ● | — | — | — |
| Linear algebra | — | ○ | ● | — | — | — |
| Statistical mechanics | — | — | ○ | ○ | — | — |
| Thermodynamics | — | — | ○ | ● | — | — |
| Probability | — | ● | ○ | ○ | ○ | — |
| Frameworks (SE/agent/proof) | ● | — | — | — | — | ● |
| Physics | — | ○ | ● | ● | ● | — |
| Control theory | — | ● | — | ○ | ● | — |
| Nonlinear dynamical systems | — | ● | ○ | — | ● | — |
| Requirements engineering | ● | — | — | — | — | ○ |
| Constraints engineering | ● | ○ | ○ | ● | ○ | ● |

Every selected domain appears in **≥2 papers** except IMC (P3 primary; deepen with 2607.29076 if needed) and pure stat-mech (covered secondarily via thermo/Langevin in P3/P4/near-miss 2607.16183).

---

## Transfer verdicts (locked E-DYN1)

| Paper | Steal (Adopt metaphor / process) | Refuse (tip SoT) |
| --- | --- | --- |
| **P1 MAAD** | RE→architecture workflow; Evaluator/ATAM report shape; mismatch analysis | Auto-generated architecture as merge SoT; LLM-as-architect without human Approve |
| **P2 Observability** | Observability + PE inputs as *language* for sensors/rate caps | Cover% PID; treating agent tip as controllable plant |
| **P3 Memristive IMC** | Capacity / noise / quantization as *remeasure cost language* | Analog/IMC hardware; non-hermetic substrate in CI |
| **P4 Landauer erasure** | Irreversibility & work-budget language for Green-AI | \(kT\ln 2\) as CI floor |
| **P5 Dynamics-matched PRC** | **climb→oracle ≈ reservoir→readout**; fixed nonlinear map + linear readout | Soft-robot / photonic / nanoparticle hardware as product |
| **P6 Aria/Iris** | Agent + **verification harness**; kernel-accepted proof only; reason→act→verify | Claiming product “proved” without in-repo artifacts; Iris as Java Stage-0 prover |

Allowed locked transfers only: saliency/debounce · advisory hysteresis · dual-sink noise discipline · remasure cost language · climb→oracle readout analogy.

---

## Mapping onto product layers (pre-code)

| Layer | Papers that inform | Pre-code artifact |
| --- | --- | --- |
| RE / QAS / ATAM | P1 | `03-requirements/`, `05-quality-architecture/` |
| Control / observability of sensors | P2, P5 | `08-verification/` rate caps; refuse Cover% PID |
| L3 proof / harness | P6 | `08-verification/l3-proof/`, proof-tour receipts |
| Science metaphor budget | P3, P4, P5 | `11-science-transfer/locked-transfers/` |
| RAG ≠ verify | P1 (mismatch), P6 (harness) | `10-rag-corpus/retrieval-contracts/` |

---

## Quality bar for this pack

- **Evidenced:** arXiv abs + published timestamp via API.
- **Confirmed (in this planning repo):** locked-transfer table already Accepted as product policy.
- **Unknown:** whether MAAD Evaluator quality transfers to *this* product’s plant envelope without Pilot — requires Spike, not Implement.

---

## Explicit refuse

- Treating any of P3–P5 as hardware roadmap.
- Using P4’s Landauer bound as a numeric gate threshold.
- Using P6’s Iris/Rust results to claim Spring DI “proved.”
- Expanding always-on agent context with full paper PDFs — retrieve via RAG pack only.
