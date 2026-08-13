---
title: E-CX0-S2 — Verification-in-the-loop
status: DRAFT Spec — parked; after S0 (and S1 only if built)
research date: 2026-08-13
spec_gate: DRAFT E-CX0-S2
bloom_gate: required-through-create
parent: docs/design/code-intel/README.md
do_not:
  - build a new verifier when an existing CLI already decides the property
  - unfreeze the task bank after seeing scores
  - treat provenance tags as loop success without ablation
  - change fail_under or certification fold
sources:
  primary:
    - src/doc_engine/pipeline/live_gates.py
    - src/doc_engine/tools/check_pipeline_output.py
    - src/doc_engine/tools/certification.py
    - https://arxiv.org/abs/2406.11497
---

# S2 — Verification-in-the-loop

**Goal:** The agent **invokes** tools that already know the answer (pipeline
gates, CodeQL, ArchUnit/build on the plant), then cites `file:line`. This is
rank-1 of the program. It is not an index and not a tag product.

```text
Iso: control loop observe → act → remeasure ≅ tool invoke + re-read
exit code | I3: pass-rate points ≠ coverage % | I5: certification fold
and fail_under stay boolean
```

## Bloom

| Level | Evidence |
| --- | --- |
| Remember | `doc-engine pipeline gates` / `check_pipeline_output` / `certification.py` already fold run artifacts `[Confirmed — live_gates.py, certification.py]`. CodeQL pack + `--allow-codeql-build` `[Confirmed — spring_signal_scan.py]`. Serena `execute_shell_command` exists but S0 forbids it as DoD; S2 **does** want a shell/CLI invoke of **named** verifiers. |
| Understand | “Verification in the loop” means the **same predicate** the gate uses, executed again, not a second description of the gate. Tags (`VERIFIED`) are audit labels. CrAM (arXiv:2406.11497) is **attention modification**, not in-prompt badges — do not cite −7.5/+16.7 EM as proof that our tags work. |
| Apply | Skill/prompt: for each frozen task, run the named command, paste exit + one `file:line`. Stay CLI/Skill if tool-definition tokens would exceed 10k. |
| Analyze | **Embody** existing gates. **Adopt** the loop structure. **Refuse** planner/SPO. **Refuse** LiteLLM in this epic. |
| Evaluate | § False-green |
| Create | Tickets below |

## Frozen task bank (N ≥ 20)

Write the list **before** A/B. Migration-shaped, Spring-heavy, answerable by
a verifier or a citation. Examples of *shape* (not the bank — the bank is an
operator artifact dated like S0 T2):

- Does this handler’s effective mapping match the OpenAPI path?
- Is this method transactional after interface inheritance?
- Does `pipeline gates` fail on a stray write in a gitignored path? (known gate)
- Does CodeQL `api_surface__controller` include this `@RestController`?

A/B arms: **(A)** Serena + grep only **(B)** A + forced verifier invoke
(and S1 facts if S1 shipped). Same model, same bank, same plant.

**Pass-rate delta:** **(B) − (A) ≥ 15 points** on the frozen N, or **abandon**
the extra loop (keep Serena; do not add infrastructure).

## FR / NFR

| ID | Requirement | Acceptance |
| --- | --- | --- |
| **FR-S2-01 Invoke** | Skill names the exact CLIs (pipeline gates, CodeQL query, plant `test`/`ArchUnit`). No “search docs instead”. | Skill file quotes the commands. |
| **FR-S2-02 Cite** | Success row includes `file:line` **or** gate id + exit code when the property is run-level. | Score sheet columns. |
| **FR-S2-03 Freeze** | ≥20 tasks frozen before first scored run. | Timestamp like S0. |
| **FR-S2-04 Delta** | Report (B)−(A) on that N. | ≥15 points or abandon memo. |
| **FR-S2-05 Ablation** | Same N, three tag conditions: none / human-only provenance / `VERIFIED` in prompt. | If tags do not help **or** increase over-trust errors, drop Context Compiler premise. |
| **NFR-S2-01** | Tool-definition payload under 10k tokens, else CLI/Skill only (no new MCP zoo). | Count at ship time. |
| **NFR-S2-02** | Does not modify `fail_under`, certification schema, or OAS12. | Diff empty on those. |
| **NFR-S2-03** | Plant tests are E-OCS operator, not CI fixture theater. | Score sheet path. |

## Tickets

| ID | Title | Acceptance |
| --- | --- | --- |
| **CX0-S2-1** | Skill: invoke named verifiers + cite | FR-S2-01, FR-S2-02, NFR-S2-01 |
| **CX0-S2-2** | Freeze ≥20 tasks | FR-S2-03 |
| **CX0-S2-3** | A/B vs Serena+grep | FR-S2-04, NFR-S2-03 |
| **CX0-S2-4** | Tagging ablation | FR-S2-05 |
| **CX0-S2-5** | Invariants untouched | NFR-S2-02 |

## False-green

| Failure | Bite |
| --- | --- |
| Bank edited after scores | FR-S2-03 |
| Different questions on arm B | Same N |
| Pass-rate on 5 tasks called “15 points” | N ≥ 20; points = percentage points on that N |
| Tags shipped as product without ablation | FR-S2-05 |
| Coverage % or LLM-judge as gate proof | constitution |
| New MCP server to wrap `gradle test` | NFR-S2-01 |

## Definition of Done

Score sheet + abandon-or-keep memo. Keep = skill in-tree. Abandon = S0
stands, S2 does not grow. Neither outcome implements E-IK0.
