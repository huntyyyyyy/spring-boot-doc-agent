---
title: Layers of Truth
status: DRAFT
date: '2026-08-10'
---

# Layers of Truth

| Layer | Question | Primary containers |
| --- | --- | --- |
| L1 Where | Where is the symbol? | Engine + scip-java + tree-sitter |
| L1b Wire | Which bean binds? | WiringResolver + SQLite |
| L2 How | Is change allowed? | Lock IR (Ruby) + LockCheck (Rust/WASM) |
| L3 Proof | Optional SMT/query proof | Deferred |
| Sandbox | Where does untrusted check run? | WASM guest |

SCIP ≠ Spring DI. WASM ≠ mathematical proof.
