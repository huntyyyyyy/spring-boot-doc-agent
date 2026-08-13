# Review pointer: Intent Kernel v2 (spike-first plan)

**Canonical memo:** [`docs/research/process/49-intent-kernel-v2-spike-first-adversarial-review-2026-08-13.md`](../research/process/49-intent-kernel-v2-spike-first-adversarial-review-2026-08-13.md)

**Parked epic:** **E-IK0** (Draft Spec — no Implement). Active tip remains #119 / E-COH1.

| Question | Answer |
| --- | --- |
| Approve v2 as Spec and Implement? | **No.** |
| Ordering correction vs v1 (measure before ISA pack)? | **Yes** — keep. |
| Invert SDD to “spike then spec”? | **No.** Spec **the spike** (five tests + D-00/D-01), then implement, then spec the ISA. |
| Harvest = CAS kernel? | **No.** Hash → admit/deny → provenance is structure; the modules are a read/certify pipeline. |
| ≥90% unnamed FR bake-off? | **Reject** — climb-Cover% as a product gate. Score the five-behaviour join. |

Blocking before any kernel code: **D-00** (this repo vs greenfield), **D-01** locked to match Phase 0 scope, hermetic `fixture-repo` not OCS-as-DoD, pin which hashline / which AgentBound.
