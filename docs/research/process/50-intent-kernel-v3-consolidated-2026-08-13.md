---
title: E-IK0 — Intent Kernel v3 (consolidated draft)
status: DRAFT Spec — parked; not Approve; not Active tip
research date: 2026-08-13
supersedes_plans: v1 research-first; v2 spike-first
does_not_supersede: docs/research/process/49-intent-kernel-v2-spike-first-adversarial-review-2026-08-13.md
claim tiers: Evidenced / Confirmed / Unknown
product: proposed intent-kernel join (CAS + deny + receipt); not doc-engine Implement
bloom_gate: required-through-create
bloom_mcp:
  - llms_txt
related:
  - docs/research/process/49-intent-kernel-v2-spike-first-adversarial-review-2026-08-13.md
  - docs/design/intent-kernel-cas-apply-design-2026-08-13.md
  - docs/research/quality-backlog.md
  - docs/research/process/35-control-plane-closed-loop-2026.md
  - docs/research/process/37-operator-agent-surface-cli-mcp-rag-2026.md
do_not:
  - implement kernel or LiteLLM on this tip
  - treat nine epic items as the unblock bar
  - use ocs-api-service as spike DoD
  - install litellm from unpinned PyPI (GHSA-5mg7-485q-xm76)
  - add MCP write tools without Approve
spec_gate: DRAFT E-IK0 (2026-08-13) — unblock = D-00 + D-01 + five failing tests
sources:
  llms_txt:
    - https://ast-grep.github.io/llms.txt
    - https://docs.litellm.ai/llms.txt
  primary:
    - https://ast-grep.github.io/guide/rewrite-code.md
    - https://docs.openrewrite.org/concepts-and-explanations/lossless-semantic-trees
    - https://docs.litellm.ai/docs/tutorials/claude_responses_api
    - https://code.claude.com/docs/en/llm-gateway-connect
    - https://github.com/advisories/GHSA-5mg7-485q-xm76
    - https://arxiv.org/abs/2606.30970
    - https://arxiv.org/abs/2607.14890
---

# Intent Kernel v3

## 0. Verdict

**Not Approve. Not Reject. Blocked on two decisions plus the five tests.**

v2 cannot be Implement. The review was wrong that **nine** epic items must
land first. **Three** things block a spike: D-00, D-01, and the five-test spec
as named failing tests. Bake-off rubric, surviving RQs, ISA, and targeted
research are written **after** the spike. Writing them before specifies against
a system nobody has run — the v1 shape at one-fifth scale.

Ordering: **lock D-00/D-01 → write the five tests → run them → then rubric,
RQs, ISA.** No kernel code before the five tests exist as failing tests.

The review remains the evidence record (`process/49`). This file is the plan
that absorbed it. It does not tombstone the review.

```text
Iso: gate keyed on a correlate ≅ keyword-router / uncovered-line climb /
CORPUS count / unnamed-FR% → land as docs rule (name the denominator,
measure the property) | non-preserved: units and plant (LLM $ vs file
sha256 vs source count) | I5: no merge-SoT retype
```

## 1. Errors v2 shipped (on the record)

The defect being litigated *is* evidence discipline.

| v2 claim | Verified | Correction |
| --- | --- | --- |
| "15 `spring_drift_*` modules" | `ls src/doc_engine/tools/spring_drift_*.py` → **12** `[Confirmed]` | Overcounted. |
| "9 `run_manifest_*` modules" | `ls` → **9** `[Confirmed]` | Stands. |
| doc-agent "answers RQ-HASH-01" | ast-grep `expected_pre_hash` in `src/` → **0** `[Confirmed]` | Overclaimed the verb. Drift runs *after* the tree moved; CAS runs *before* a write. Granularity insight transfers; the mechanism does not. |
| Phase 0 answers D-01/D-02 | — | Contradiction. |
| Bake-off "≥90%" | — | Same defect as `CORPUS≥150`. |
| `ocs-api-service` as fixture | Artifactory; CI uses `harness/fixture-repo` `[Confirmed]` | Wrong DoD. |
| "measured p95s" as constraints | — | One op × one repo is a placeholder. Booleans have no p95. |
| "unhit ⇒ imagined" | — | Too strong. |
| "no telemetry exporter" + histogram | — | Local timer + JSONL in-test; no exporter. |

### Trust gap (closed this pass)

v3 took three review claims on trust. Re-derived:

| Claim | What the code does `[Confirmed]` |
| --- | --- |
| `certification.py` fail-closed | `load_certification` rejects missing file and schema before trusting `certified`. `verify_certification` **refolds** from stamped stage/gate rows; rejects `certified ∧ failures ≠ ∅`; rejects `generative_executor` `none`/`mock` without `--allow-mock`; exit 0 only when certified. Still a **doc-pipeline fold**, not policy-before-Java-write. |
| `Mutator._apply_structural` | Reads bytes before/after `ast-grep --update-all`. Exit code is not the witness (`scripts/ratchets/mutator.py`). Same quirk in `docs/process/tool-quirks.md`. |
| `dispatch_tool` confused-deputy | `args.pop("root", None)` then `_server_root()` (`src/doc_engine/query/mcp_tools.py`). OAS12 still Refuse MCP write. |

`compute_file_signature` is sha256 of raw file bytes (`src/doc_engine/core/walk.py`).

## 2. Where the review overreached (kept)

**Nine gates to authorize one spike.** Three are load-bearing. IK0-4…IK0-8
describe a system that does not exist yet. Sequence them post-spike.

**Notation cost.** Claim tags stay where they earn a boolean (this table).
Bloom section-headers and a glossary of E-/OAS-* IDs are not load-bearing
for the findings. This file is written so a reader outside the repo can
audit the spike bar without them.

**The 5×N fix is the named denominator, not the integer.** 5/5 vs ≤2/5 is
still a threshold on a small set. Keep the property: the denominator is
**named, public, and behavioural**. The integer is incidental.

**SDD framing.** "Spec the spike, implement, then spec the ISA" is v2's
ordering with local vocabulary. Not a conflict. M3 (spike-first is not a
licence to skip the spike's spec) is kept.

## 3. Blocking decisions

### D-00 — Product home *(org question; no technical default)*

**(A)** New bounded context inside `spring-boot-doc-agent` — inherits the
wheel, CI floors, OAS12 refuse-on-MCP-write, one-Active-tip rule.
**(B)** Greenfield repo citing this tree as prior art — harvest is citation,
not copy.

**Consequence:** the five failing tests have to live *somewhere*. Committing
them here implies (A). (B) means they live in the other repo. That is why
this is blocking, not ceremonial.

### D-01 — Node cardinality *(lock before Phase 0)*

- **(a)** ISA carries `expected_pre_hashes[]`; kernel is a transaction coordinator.
- **(b)** Intents are single-node; a planner above owns cross-intent consistency.

**Recommend (b).** Smaller, and it concedes the kernel alone does not deliver
safe refactoring (weakens standalone RQ-H01, correctly).

Pin: `ast-grep --update-all` rewrites **every** match. Intra-file multi-site
is not D-01 solved. Phase 0 constrains to **one match** in one file, or
states multi-site behaviour and still calls D-01 open.

### D-02 — Failure atomicity *(spec now; test is 5c)*

Adopt `_write_json_atomic` (temp + `os.replace`) for single-file publish.
Do not bake off journal vs git-index on one `match_rewrite`. Crash-mid-apply
is a required test.

### D-03 — Naming *(decided)*

`verified-architecture` → `intent-kernel`. CAS + policy + receipts is
transactional integrity and provenance, not proof of refactor correctness.

## 4. The five behaviours (this is the spec)

Witness is **pre/post file sha256**, never a process exit code. Fixture:
`spring-signals/harness/fixture-repo/`. Hash primitive:
`compute_file_signature` (file sha256). Not short "hashline" hashes.

JSONL timers with conditions live **in these tests** (not a later protocol
doc). Values are **probes**, not SLOs.

1. **Apply** — one intent, one node, one match; post-hash matches predicted.
2. **Drift** — stale `expected_pre_hash` → `DRIFT`, tree byte-identical.
3. **Deny** — one fail-closed policy rule → `POLICY_VIOLATION`, tree byte-identical.
4. **Receipt** — every terminal state emits `intent_id`, `pre_hash`,
   `post_hash`, `policy_pack_hash`, `operation_id`. Bind command + digest +
   HEAD (Proof-or-Stop shape). If git identity cannot be established, **fail
   closed** (do not emit a receipt that pretends to bind HEAD). If the tree
   is dirty, **record `dirty=true`** and still apply when the target file
   matches `expected_pre_hash` (see 5a). Dirty ≠ missing git.
5. **Dirty tree — split:**
   - **5a.** Unrelated uncommitted edits; target still matches pre-hash → apply correct; receipt records dirty.
   - **5b.** Re-run the **same** intent after success → **`DRIFT`**. The tree no longer matches the original `expected_pre_hash`. Idempotent success is a *different* intent (refreshed pre-hash or "desired post-state already present") — not this test.
   - **5c.** Crash mid-apply (kill between temp write and `os.replace`) → tree is pre-state or post-state, never partial. This is D-02's actual test.

## 5. Bake-off — named denominator (hypotheses until run)

For each of the five, can the candidate **alone** produce it with a witness?
Rows below are **hypotheses**, not measurements.

| | Moderne / OpenRewrite | hashline *(pin a SHA)* | OPA | AgentBound (2606.30970) | AgentBoundary (jamjet) |
| --- | --- | --- | --- | --- | --- |
| 1 Apply | likely yes | no | no | no | no |
| 2 Drift | no | maybe | no | no | no |
| 3 Deny | no | no | shape only | paper only | no |
| 4 Receipt | no | no | no | fields | fields |
| 5 Crash-safe | unknown | temp+rename in some | no | no | no |

Read: **all five with witnesses → integration layer, stop.** **Few or none →
the gap is the kernel.** **Partial → spec only the join.** Partial is the
likely interesting case. The property to preserve is the named behavioural
denominator, not a magic integer.

**Homonym hazard — pin before filling:** AgentBound (arXiv:2606.30970,
three-authority + receipts), AgentBound (FSE, MCP sandbox), agentboundary
(jamjet, portable receipt spec) are three objects. Pin: 2606.30970 for
decision algebra, jamjet for receipt fields, FSE for MCP sandbox. Hashline
is a **family** — pin a git SHA or drop it.

Fill this matrix **after** the spike. The empty table with named rows can
exist now; scoring cannot.

## 6. Surviving research (~25 sources, after the spike)

`RQ-REC-01`, `RQ-POL-01`, `RQ-H01`, `RQ-MCP-01`, and — if D-00 = A or an MCP
surface survives — **`RQ-MCP-WRITE-01`** (containment, server-pinned root, no
caller path). That last one exists because confused-deputy is **confirmed in
this tree**, not because a spike hit it.

Terminal states: `answered` | `refuted` | `blocking + named waiver`. No
`unknown-deferred`. No CORPUS floor. No research-process CI.

## 7. Measurement discipline

- Local timers → JSONL inside the five tests. No OTel exporter at Phase 0.
- Record **probes with conditions**, never SLOs.
- Promotion probe → `C-*` requires bake-off plus a named plant.
- Boolean constraints are proven by a passing test, not by citing a number.

## 8. Model-access layer (same *rule*, different *plant*)

**Not a spike dependency.** Unblock does not wait on a gateway.

The routing evidence and the kernel review share a **structure**: a gate
keyed on a correlate instead of the property. Confirmed instances here:
`CORPUS≥150`, `coverage_climb` uncovered-line rank, `≥90%` of an unnamed FR
list. `[Confirmed]`

Claimed routing numbers (~98% flip under keyword injection; ~100% of trivial
coding queries to the strong model) are **`[Unknown]`** until a citation is
named. Public hits for "98" in this neighbourhood are a **98× latency**
result (arXiv:2603.12646), which is a different quantity. The isomorphic
*rule* does not need those numbers to hold.

**Do not merge plants.** Spike JSONL is hash/latency of one `match_rewrite`
on `fixture-repo`. Gateway JSONL is model/cost/cache-hit of LLM calls.
Same shape (probes with conditions); different denominator. Folding them
as one project because both say "JSONL" is the substrate collapse this
repo already refuses.

If a **separate** DevEx effort is later Approved (not this tip):

- **Build:** LiteLLM **official proxy image**, pinned. Claude Code
  `ANTHROPIC_BASE_URL` / `ANTHROPIC_AUTH_TOKEN` is documented.
  `[Evidenced]` LiteLLM tutorial + [Anthropic gateway](https://code.claude.com/docs/en/llm-gateway-connect).
- **Why the image, not `pip install litellm`:** GHSA-5mg7-485q-xm76 —
  PyPI 1.82.7/1.82.8 shipped credential-harvesting malware. Maintainer
  note: official proxy image users were not impacted; 1.82.8's `.pth`
  was in the wheel RECORD, so `pip install --require-hashes` would still
  have passed. `[Evidenced]` Pin + image digest, not a vibe.
- **Skip:** mitmproxy; standalone Semantic Router; personal proxy of
  corporate DLP; Elsevier-class sources to a third party without an
  enterprise agreement.
- **Select models manually per task** until an eval (10–20 real backlog
  tasks) shows cost ≥20% down *and* pass-rate within 2 points of
  always-strong, with no coding-eval regression.

## 9. Refuse

v2 as Implement on this tip · nine pre-spike epic items as the unblock bar ·
`CORPUS≥150` · `unknown-deferred` · `≥90%` of an unnamed checklist · short
content hashes as CAS SoR · `verified-architecture` · OCS/Artifactory as
spike DoD · OTel exporter at Phase 0 · spec sections for unexercised stages
except confirmed in-repo hazards · MCP write tools without Approve ·
research-process CI · mitmproxy · standalone Semantic Router · unpinned
LiteLLM PyPI · corporate code to unsanctioned third-party models · kernel
Implement before D-00/D-01/five failing tests · gateway work on the Active
tip.

## 10. Definition of done

**This document:** Draft, parked, not on the Active tip (#119 / E-COH1).

**Unblocked when (three items):**

1. D-00 written (A or B), including where the pytest files live.
2. D-01 locked (recommend b) with the one-match pin.
3. The five behaviours exist as **named failing tests** against
   `harness/fixture-repo`, including 5c, with sha256 witnesses and in-test
   JSONL probes.

**Spike done when:** those tests pass, including 5c.

**Then and only then:** fill the bake-off matrix, surviving RQs, ISA.
Confirmed in-repo hazards (RQ-MCP-WRITE-01) survive without being hit.

No document count and no source count in this DoD. Deliberate.
