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

**Owns:** nothing. This bounded context is **out** of the port product.

| Was | Now |
| --- | --- |
| Optional ACI / glue peer | **Refuse** |
| Spec Model Context Protocol host candidate | **Refuse** (was circular tip convenience) |
| PyO3 engine bridge default | **Refuse** as planning default |

**Engine / Spec corpus Model Context Protocol:** **Rust** (Architecture Decision
Record ADR-0007; Spike `SPIKE-SPEC-MCP-0`).

**IDE / presentation Model Context Protocol:** TypeScript (Architecture Decision
Record ADR-0010) — not Python.

Do not schedule product code, scaffolds, or tip-Python carry-over into this nest.
Historical “Python peer” language elsewhere is superseded by Architecture
Decision Record ADR-0001 amendment (2026-08-11).
