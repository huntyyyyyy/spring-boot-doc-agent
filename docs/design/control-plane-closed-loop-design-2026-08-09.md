---
title: Control-plane closed-loop — Spec (E-CPL0)
status: DRAFT — pending Approve of CPL1–CPL12
date: 2026-08-09
epic: E-CPL0
research: docs/research/process/35-control-plane-closed-loop-2026.md
related:
  - docs/design/ddia-north-star/meta/effective-remedies.md
  - docs/research/process/24-codegen-quality-dimensions-mechanism-depth-2026.md
  - docs/research/process/28-local-stalker-telemetry-etl-2026.md
do_not:
  - implement CPL1-2+ fitness package before this Spec is APPROVED
  - Embody TEE/Nix/SLSA-L3 / Proof-or-Stop daemon as tip SoT
---

# Design Spec: control-plane closed-loop (E-CPL0)

## Goal

Install a **standing closed-loop invariant** on the merge/push control plane so
new gates cannot ship open-loop (empty observation, unstable plant, unlabeled
predicates).

## Decisions (CPL1–CPL12)

See research memo §5. Summary:

1. Closed-loop is a protected architectural characteristic (fitness).
2. Hard suites need non-empty receipts (or explicit skip receipts).
3. Success still surfaces WARNING/advisory excerpts.
4. Mutation harness must match `HEAD` or refuse.
5. `overall=pass` only from admissible hard receipts.
6. Advisory cannot authorize merge/push.
7. New gates register SoR|derived + plant map + receipt + witness.
8. Proof-or-Stop / Nidus = semantics only.
9. ≥10k★ for new external SoR; pytest/tach/ast-grep vehicles.
10. Expensive skip only via sealed fingerprint.
11. One tip writer; receipts bind this worktree HEAD.
12. Instance patches without expanding CPL fitness = Fail.

## CGQ3 Accept shape (required before E-CPL1)

| Concern | Remedy id | Depth cite | Witness |
| --- | --- | --- | --- |
| vacuous telemetry | fitness-function + adequacy-witness | process/35 §3.1–3.4; process/24 Ford/ArchUnit rows | `test_stalker_telemetry` + CPL empty-log hard fail |
| dirty harness plant | fitness-function + hermetic plant | process/35 §3.3 | mutation preflight tests |
| overall without proof | Proof-or-Stop semantics | process/35 §3.1; arXiv 2607.14890 | `pre_pr` overall admission tests |
| gate clone open-loop | sensor-ledger-spec + CPL7 registry | process/23 SOL6; process/35 CPL7 | claims / CONTRIBUTING gate registry |

## Implement epic (E-CPL1) — blocked on Approve

Tickets CPL1-1…CPL1-6 in research §6. **CPL1-1** (tee non-empty logs) may land
as E-TEL repair under already-Approved E-TEL0 without waiting — it restores a
landed witness, it does not invent a new SoT.

**Hook (landed):** `.cursor/hooks/inject_nonvacuous_test_witness.py` (postToolUse
on `tests/**`) injects the non-vacuous receipt rule when agents edit tests;
`require_hardened_tests` fails closed if control-plane files are staged without
`tests/ci/test_stalker_telemetry.py` markers (success WARNING excerpt + live
`getvalue`).

## Exit

Human sets `status: APPROVED E-CPL0` here and on research `spec_gate`. Then one
tip stream runs E-CPL1.
