---
title: Nest 08 — Python ACI peer — REFUSED
status: REFUSED — 2026-08-11
doc_role: nest
freeze_class: frozen
accepted: false
corpus_version: '2026-08-11'
look_first:
  - ../../docs/adr/adr-0001-polyglot-first-product.md
  - ../../docs/adr/adr-0007-rust-owns-engine.md
do_not:
  - Revive Python Spec Model Context Protocol host
  - Revive Python ACI as product container
  - PyO3 as default engine bridge for this port
---

# Nest: Python — REFUSED

**Owns:** nothing — out of the port product.

**Fail closed:** any new file here except this tombstone, any `nest.mdc`, any
tip-Python Spec/ACI/PyO3 scaffold → reject (Architecture Decision Record
ADR-0001 amended 2026-08-11).

| Path attempted | Disposition |
| --- | --- |
| Spec Model Context Protocol host | **Refuse** → Rust (`SPIKE-SPEC-MCP-0`, ADR-0007) |
| ACI / glue peer container | **Refuse** |
| PyO3 as default engine bridge | **Refuse** as planning default |
| IDE / presentation MCP | TypeScript only (ADR-0010) — not Python |

**Now:** this README only. Historical “Python peer” prose elsewhere is
superseded by ADR-0001 amendment.
