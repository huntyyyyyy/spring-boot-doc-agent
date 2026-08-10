---
title: Freshness-bound receipt — Decision Matrix
status: DRAFT
date: '2026-08-10'
standard: docs/standards/decision-framework.md
icd: 07-system-design/icd/receipt.schema.json
related_gaps: [G-R1, G-R2]
---

# Freshness-bound receipt — Decision Matrix

## Six vectors

| Vector | Content |
| --- | --- |
| **Why** | “Tests passed” prose and stale commits are adversarial for agent verify; need authenticated, source-state-bound evidence that gates can refuse. |
| **What** | Receipt with β(E) source binding (`material_digest`, `head_hash`, `policy_digest`, `command_set_digest`) + ρ(E) step identity (`cmd`, `args`, `cwd`, `exit`, `output_digest`) + ban on llm/rag witnesses. |
| **Who** | `ReceiptWriter` harness mints; model never stamps; humans Accept offline tamper suite. |
| **How** | JSON Schema + optional later in-toto Statement envelope; compose with Supply-chain Levels for Software Artifacts — **do not rename** SLSA as Proof-or-Stop. |
| **When** | Draft schema now; Spike field set + tamper plants before Must Implement; review when Proof-or-Stop public engine appears. |
| **Where** | `icd/receipt.schema.json`; verify MCP `structuredContent`; planned `crates/engine/receipt/`. |

## Alternatives scored

| Option | Why | What | Who | How | Total | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| **A. PoS-shaped fields + Witness honesty + unsigned MVP** | 2 | 2 | 2 | 2 | **8** | **Chosen** |
| B. `git_commit` only as freshness | 0 | 0 | 1 | 1 | 2 | **Refuse** |
| C. Treat SLSA provenance as Proof-or-Stop | 1 | 0 | 1 | 1 | 3 | **Refuse** (compose, don’t rename) |
| D. Narrative message as witness | 0 | 0 | 0 | 0 | 0 | **Refuse** |
| E. Wait for Proof-or-Stop engine repo | 1 | 1 | 1 | 0 | 3 | **Pilot** fields; don’t block Spec |

Exact Proof-or-Stop engine public repos = **0** `[Evidenced — adoption audit]` → Embody gate semantics; Adopt Witness/in-toto shape.

## Fields to add (G-R1) — Spec delta

| Group | Fields | Gate |
| --- | --- | --- |
| β(E) | `material_digest` (have), `head_hash`, `story_files_hash?`, `policy_digest` (have), `command_set_digest` | Fresh + Complete |
| ρ(E) per executed step | `cmd`, `args`, `cwd`, `exit`, `output_digest` | ExecutionAttested |
| Identity | stable `step_id` key (Spike) | Diff honesty |
| Integrity (Could) | signature / key id | IntegrityVerified |

Canon: hash `git ls-tree` **excluding** lifecycle receipt paths so writeback does not invalidate binding.

## Tamper Accept suite (G-R2)

| Class | Expect |
| --- | --- |
| Stale material (edit source, reuse receipt) | fail `stale` |
| Empty `cmd` on executed step | fail `receipt_identity_incomplete` |
| `exit != 0` with `result=pass` | fail |
| Injected `llm_text` witness | fail schema / reject |
| Mutated `material_digest` without resign | fail (when signatures Pilot) |
| Incomplete β (missing `command_set_digest`) | fail `binding_incomplete` |
| Command set changed, receipt reused | fail `command_set_drift` |
| Empty `steps` | fail `build_proof_missing` |
| Non-64-hex `output_digest` | fail `digest_mismatch` |
| `exit=-1` when `kind=command` | fail `receipt_identity_incomplete` |

## Usage cases

| ID | Actor | Goal | Locus |
| --- | --- | --- | --- |
| UC-RCPT-01 | `verify` tool | Write receipt after LockCheck | MCP verify output + ICD-RCPT |
| UC-RCPT-02 | Continuous Integration | Offline verify; **recompute** digests | engine `receipt verify` |
| UC-RCPT-03 | Auditor | Replay step ρ(E) | receipt `steps[]` |
| UC-RCPT-04 | Hostile agent | Narrative pass only | minefield FX-MCP-03 |
| UC-RCPT-05 | Developer | Edit source, reuse yesterday receipt | must fail stale |
| UC-RCPT-06 | Release (Could) | Compose in-toto / SLSA envelope with receipt | mapping table — not rename |

## Schema enforcement note

When `kind` is `command`, JSON Schema **must** use `if`/`then` to require
`cmd`, `args`, `cwd`, `exit`, `output_digest` — prose-only requirements false-green.

## Still open

Normative ls-tree exclusion list; `step_id` stability Spike; in-toto mapping table (even if unsigned MVP).
