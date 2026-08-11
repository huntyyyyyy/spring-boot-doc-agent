---
title: Adversarial review — cybernetic loop / control / information / AOS framing
status: REVIEW — metaphors useful; measures missing; not a new SoT
date: '2026-08-11'
claim_tiers: Evidenced / Confirmed / Unknown
look_first:
  - research/gaps/review-formal-vs-distilled-2026-08-11.md
  - research/gaps/four-dimensions-agent-os-spitball-2026-08-11.md
  - 08-verification/VERIFY_STACK.md
  - docs/adr/adr-0011-mcp-protocol-and-tool-surface.md
  - STATUS.md
accepted: false
---

# Review: “Deterministic cage around a probabilistic engine”

Pitch: brownfield AI work is a **nonlinear feedback loop**; apply Control,
Information, “Agent OS,” Transformer, and Model Context Protocol theories as
operational frameworks; synthesize a cybernetic loop (clean → plan → act →
stabilize → record).

**Verdict:** The **cage** slogan and the **feedback-loop** insistence are
right. Most of the named theories are **useful metaphors** for failures we
already named — not new Systems of Record, not proof the design is correct, and
not permission to Implement.

---

## Entailments

### Nonlinearity

**If** a one-character edit can change program behavior discontinuously,
**then** “output ∝ input” is a bad model of *software semantics* — agreed.

**If** that fact is used to demand an arbitrarily complex Brain/Guard,
**then** the leap is invalid. Nonlinearity motivates **re-check after change**
(Fresh, LockCheck, plants), not category theory or a heavier Clojure
orchestrator.

Disposition: **Embody** post-write / Fresh loops. **Refuse** “nonlinear ⇒
prior wireframes were too simple” as a blank check.

### Control theory (stability)

**If** setpoint = Accepted lock / invariant policy in git, and error =
violation / claim `affected`, and actuator = reject write or force re-plan,
**then** negative feedback is an accurate **description** of verify +
adversarial audit.

**If** there is no measured error signal, no stability margin, no plant model
of the “plant” (repo), **then** calling the Guard a “controller that dampens
oscillation” is analogy — it does not inherit control-theoretic guarantees.

Disposition: **Embody** setpoint/error/reject loop in Spec language (locks,
dispositions, receipts). **Refuse** stability theorems without plants.

### Information theory (noise / zoom)

**If** context windows are finite and whole-file dumps are low yield,
**then** multi-resolution views (skeleton → fold → atomic) are lossy
**compression for a channel** — fair operational reading of zoom.

**If** the pitch claims maximized mutual information without a defined
estimate or experiment, **then** “Information Theory” is prestige labeling of
“send less irrelevant text.”

Disposition: **Embody** zoom as token-efficiency Quality Attribute Scenario.
**Refuse** unmeasured mutual-information claims as SoT.

### “Agent OS theory” (resources / capabilities)

**If** the model must not hold raw disk authority, **then** privilege
separation via kernel-minted capabilities/handles is the right failure mode
to design against (matches Model Context Protocol handle pattern + STEAD-typed
ids).

**If** “Agent OS Theory” is presented as a settled field that justifies a
specific registry design, **then** that is branding. There is no single
normative “AOS” textbook this port Adopted.

Disposition: **Embody** CPU/I/O metaphor for propose vs decide. **Refuse**
AOS-as-authority.

### Transformer / agentic (intent protocol)

**If** models are weak at brittle line addresses and stronger at pattern-shaped
edits, **then** structural find/replace as the mutation protocol is an
**Embody** we already accepted as Pilot/Could.

**If** that is said to “align with attention mechanisms” inside the weights,
**then** the mechanism claim is **Unknown** — useful interface choice does not
require a neuroscience-of-transformers proof.

Disposition: **Embody** structural protocol. **Refuse** attention-alignment as
evidence.

### Model Context Protocol (interface)

**If** wire pin `2026-07-28` is already Adopted, **then** “MCP Theory solves
interoperability” restates an earned decision — good, not new.

**If** protocol adherence is used to justify Clojure “Reasoning” as a separate
always-on Brain above Rust execution, **then** decoupling is mis-assigned
(presentation vs engine vs optional query brain).

Disposition: **Adopt** remains on the wire. Topology owners stay per
Architecture Decision Records.

### Cybernetic synthesis diagram

**If** the loop is: compress context → model plans → capability-checked act →
policy feedback → record digests/claims, **then** that matches VERIFY_STACK +
Fresh + handles better than “prompt harder.”

**If** each arrow is labeled with a capital-T Theory to imply completeness,
**then** theory-stacking returns — five frameworks describing one harness loop.

Disposition: **Embody** the loop as the product story. **Demote** the theory
roster to footnotes, not milestones.

---

## What this framing gets right (plain)

1. Brownfield agent work is a **loop**, not a pipeline.  
2. Stochastic model output needs a **deterministic outer cage** (harness
   decides).  
3. Prompt-only agentic theory is the weakest layer in a large legacy tree.  
4. Zoom and structural edits attack **noise** and **brittle addressing**.  
5. Guards and claim Fresh attack **drift**, not “bad vibes.”

Those five sentences do not require Control / Information / AOS textbooks to
Authorize crates.

---

## What remains false or unfinished

| Claim | Gap |
| --- | --- |
| Nonlinear ⇒ need richer Brain | Need richer **checks**, not more orchestration ownership |
| Guard = proven stabilizing controller | No measured error dynamics |
| Zoom = max mutual information | No sensor defined |
| SOT/SCIP “records Truth” | Index is Index SoR; claims/receipts are derived; wiki advisory |
| Cage ⇒ production survival | Still need plants, Accept, Definition of Ready |

---

## Bottom line

**If** the gap was “people only prompt the model,” **then** yes — wrap it in
deterministic verify/Fresh/capability discipline.

**If** the gap was “we lacked Theory,” **then** no — we lacked **Accept +
plants + honest SoR**, not another framework map.

Keep the cybernetic **picture** in architecture visualization language.
Do **not** open a “Control Theory milestone” or rename Spec to Agent OS Theory.

**Implement:** still **Refuse**.
