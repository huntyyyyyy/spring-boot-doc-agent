---
title: Layers of Truth
status: DRAFT
date: '2026-08-10'
---

# Layers of Truth

**Historical / evidence — not product SoT.** Vision sketch only — Must lives in
`docs/requirements/`. Stack locks: **Rust** engine; **Refuse Python**; WebAssembly
sandbox **Could** (≠ mathematical proof).

| Layer | Question | Primary containers |
| --- | --- | --- |
| L1 Where | Where is the symbol? | Engine + scip-java + tree-sitter |
| L1b Wire | Which bean binds? | WiringResolver + SQLite |
| L2 How | Is change allowed? | Lock IR (Ruby) + LockCheck (Rust/WebAssembly) |
| L3 Proof | Optional SMT/query proof | Deferred |
| Sandbox | Where does untrusted check run? | WebAssembly guest |

Source Code Index Protocol ≠ Spring Dependency Injection. WebAssembly ≠ proof.
