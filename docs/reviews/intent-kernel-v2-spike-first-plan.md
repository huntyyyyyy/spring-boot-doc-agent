# Review pointer: Intent Kernel (v3 parked)

**C4 / SoS / repo tree:** [`docs/design/intent-kernel-cas-apply-design-2026-08-13.md`](../design/intent-kernel-cas-apply-design-2026-08-13.md)

**Plan SoT:** [`docs/research/process/50-intent-kernel-v3-consolidated-2026-08-13.md`](../research/process/50-intent-kernel-v3-consolidated-2026-08-13.md)

**Evidence record:** [`docs/research/process/49-intent-kernel-v2-spike-first-adversarial-review-2026-08-13.md`](../research/process/49-intent-kernel-v2-spike-first-adversarial-review-2026-08-13.md)

**Parked epic:** **E-IK0** (Draft — no Implement). Active tip remains #119 / E-COH1.

| Question | Answer |
| --- | --- |
| Approve as Spec and Implement? | **No.** |
| Unblock bar | **Three items:** D-00, D-01, five named failing tests. Not nine epic gates. |
| Harvest = CAS kernel? | **No.** 12 `spring_drift_*`; 0 `expected_pre_hash` in `src/`. |
| Bake-off | Named behavioural denominator (the five). Not ≥90% of an unnamed list. |
| Model-access / LiteLLM | Same *rule* (measure the property), different *plant*. Not a spike dependency. Official image only if later Approved (GHSA-5mg7-485q-xm76). |
