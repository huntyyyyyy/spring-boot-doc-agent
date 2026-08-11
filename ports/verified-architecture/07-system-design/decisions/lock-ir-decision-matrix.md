---
title: Lock Intermediate Representation — Decision Matrix
status: DRAFT
date: '2026-08-10'
standard: docs/standards/decision-framework.md
adr: docs/adr/adr-0003-packwerk-lock-ir.md
icd: 07-system-design/icd/lock-ir.schema.json
---

# Lock Intermediate Representation — Decision Matrix

## Six vectors

| Vector | Content |
| --- | --- |
| **Why** | Prose `.mdc` rules and agent “fixes” leave illegal package edges green in Continuous Integration; need executable Intermediate Representation with gradual debt. |
| **What** | Language-agnostic schema: package node, allowed dependencies, enforce mode (`true`/`strict`/`false`), todo debt with content-stable fingerprint, **edge_fidelity** stamped on every receipt. |
| **Who** | Humans own policy + todo allow; Ruby bounded context owns Packwerk-shaped DX (Architecture Decision Record ADR-0003); Rust `LockCheck` decides; agents propose only. |
| **How** | Adapters compile Ruby/Go/Java manifests → one Intermediate Representation; evaluate in engine; silent agent `update-todo` → reject. |
| **When** | Schema Draft now (open question 04); Accept after plant proves new illegal edge fails Continuous Integration; review when Packwerk major changes. |
| **Where** | Spec: `icd/lock-ir.schema.json`. Planned: `crates/engine/lockcheck/`; adapters under language bounded contexts; locks remain git System of Record. |

## Alternatives scored

| Option | Why | What | Who | How | When | Where | Total | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **A. Packwerk-shaped shared Intermediate Representation + fidelity** | 2 | 2 | 2 | 2 | 2 | 2 | **12** | **Working hypothesis (Draft)** — Packwerk *pattern* only; our JSON Intermediate Representation = Pilot |
| B. Per-language native checkers only (no shared IR) | 1 | 1 | 1 | 0 | 1 | 1 | 5 | **Refuse** as sole path |
| C. Method-call / full Dependency Injection graph as core edges | 1 | 0 | 1 | 0 | 1 | 1 | 4 | **Refuse** core (unproven vs Packwerk) |
| D. Prose `.mdc` locks without executable IR | 0 | 0 | 0 | 0 | 1 | 1 | 2 | **Refuse** |
| E. Agent auto `update-todo` on fail | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **Refuse** |

**Why A:** ≥5 genuine adjacent products (Packwerk, packs, tach, import-linter, dependency-cruiser, ArchUnit) `[Evidenced — adoption audit]`; shared IR keeps polyglot System of Record honest.

## Usage cases

| ID | Actor | Goal | Spec locus | Planned code | Why |
| --- | --- | --- | --- | --- | --- |
| UC-LOCK-01 | Developer | Add package dependency allowlist | lock-ir schema `dependencies` | adapter → git `package.yml` | Human-owned policy |
| UC-LOCK-02 | CI | Fail new illegal constant edge | `LockCheck` + fidelity | `crates/engine/lockcheck` | Static gate |
| UC-LOCK-03 | Human | Record gradual debt | `todo.fingerprint` | Packwerk-shaped todo file | Bankruptcy visible |
| UC-LOCK-04 | Agent | Propose fix | Model Context Protocol propose only | must not call update-todo | ST / harness |
| UC-LOCK-05 | Auditor | Know what was **not** checked | `edge_fidelity` on receipt | Interface Control Document ICD-RCPT bind | No false “modular” claim |
| UC-LOCK-06 | Adapter owner | Compile tach / dependency-cruiser → Intermediate Representation | `lock-ir.schema.json` | `adapters/` (planned) | One System of Record dialect |
| UC-LOCK-07 | Model Context Protocol host | `locks_list` → `lock_set_id` | `icd/mcp-tools.md` | `packages/mcp-server` | Handle mint |
| UC-LOCK-08 | Hostile agent | Enlarge todo via tool | reject `todo_mutation_forbidden` | harness | Debt not green path |
| UC-LOCK-09 | Continuous Integration | Validate acyclic **lock set** before check | Packwerk `validate` ≠ `check` | engine validate | Graph honesty |

## Document model

One Intermediate Representation file = **one package**. A **lock set** is many
package docs plus shared `edge_fidelity` stamped onto the receipt.
`privacy_legacy` in todo = import-only tombstone; **new** privacy enforcement is
**Refuse** (Packwerk 3.0 removed it as core).

**Also Refuse without Spike:** method-call edges as core; clean-todo ⇒
runtime-isolated without plant proof.

## Still open

Adapter mapping table per language (open question 04); stale-todo GC predicate plant.
