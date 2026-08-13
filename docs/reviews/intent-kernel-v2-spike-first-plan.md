# Review pointer: Intent Kernel (v3 parked) + code-intel stages

**Code intelligence program (implementable stages):** [`docs/design/code-intel/`](../design/code-intel/) — **E-CX0** (S0 / S1 / S2). Kernel writes are **not** in that program.

**C4 / SoS / repo tree:** [`docs/design/intent-kernel-cas-apply-design-2026-08-13.md`](../design/intent-kernel-cas-apply-design-2026-08-13.md) — historical / deferred.

**Plan SoT (kernel spike only):** [`docs/research/process/50-intent-kernel-v3-consolidated-2026-08-13.md`](../research/process/50-intent-kernel-v3-consolidated-2026-08-13.md)

**Evidence record:** [`docs/research/process/49-intent-kernel-v2-spike-first-adversarial-review-2026-08-13.md`](../research/process/49-intent-kernel-v2-spike-first-adversarial-review-2026-08-13.md)

**Parked epics:** **E-CX0** (Draft — stage specs). **E-IK0** (Draft — deferred indefinitely as program). Active tip remains #119 / E-COH1.

| Question | Answer |
| --- | --- |
| Approve E-CX0 / E-IK0 and Implement? | **No.** Stage specs and kernel spike plan are Draft. |
| Code-intel sequence | S0 (operator Serena) → S1 only on a named LSP miss → S2 verify-loop. Cuts: indices, SPO, cas-apply. |
| Kernel D-00 / D-01 | **Locked 2026-08-13:** home = greenfield (**B**); single-node + one match **(b)**. Five tests live there, not here. |
| Kernel unblock left | Five named failing tests in that repo (incl. 5c). Not nine epic gates. |
| Harvest = CAS kernel? | **No.** 12 `spring_drift_*`; 0 `expected_pre_hash` in `src/`. |
| Bake-off | Named behavioural denominator (the five). Not ≥90% of an unnamed list. |
| Model-access / LiteLLM | Same *rule* (measure the property), different *plant*. Not a spike dependency. Official image only if later Approved (GHSA-5mg7-485q-xm76). |
