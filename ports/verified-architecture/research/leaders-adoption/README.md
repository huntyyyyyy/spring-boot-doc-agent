---
title: Leaders and GitHub adoption map
status: ACTIVE
date: '2026-08-10'
snapshot: GitHub API 2026-08-10
---

# Leaders vs implementers (adoption map)

Canonical narrative: `07-system-design/ARCHITECTURE_BRIEF.md` §2.

| Domain | Theory/standard lead | Shipping GitHub (stars ≈) |
| --- | --- | --- |
| RE / QAS form | ISO 29148, SEI ATAM | Method — not a repo |
| C4 / ADR | Simon Brown; Michael Nygard | c4model.com; adr practices |
| CST / patterns | tree-sitter (~26.6k); ast-grep (~15.5k) | Use both |
| Symbols | SCIP (scip-code/scip ~0.7k); scip-java (~131, active) | Consume indexes |
| Locks pattern | Shopify Packwerk (~1.9k) | Pattern Adopt |
| Graph queries | DataScript (~5.8k); Babashka (~4.6k) | Pilot |
| WASM host | Wasmtime (~18.5k); Extism (~5.7k) | Sandbox Pilot |
| SMT / MC | Z3 (~12.5k); Kani (~3.3k) | Phase 2+ |
| Agent ACI | SWE-agent (~20.0k) | Loop shape |
| CLI UX | Cobra (~44.4k); Bubble Tea (~44.3k) | Go Pilot patterns |
| Vectors | LanceDB (~11.1k) | RAG only |

Stars measure attention, not fitness for Spring DI resolve.
