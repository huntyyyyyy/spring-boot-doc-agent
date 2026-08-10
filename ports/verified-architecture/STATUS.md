---
title: STATUS — single pointer for cold agents
status: ACTIVE
last_reviewed: '2026-08-10'
---

# STATUS

## Phase

**Spec / gap-fill** — planning corpus only. **Implement = Refuse.**

## Product one-liner (draft — confirm via OQ-01)

Local-first **verified architecture** engine: build a virtual dependency/DI
graph, enforce git-versioned locks, emit proof-tour receipts; prefer
Unknown over wrong. Polyglot peers are **options**, not a pre-built monorepo.
RAG retrieves this corpus; RAG is **not** the verify witness.

## Next tasks for any agent (do in order)

1. **Close or spike OQ-01** — single product boundary sentence (`04-constraints/open-questions/OQ-01.md`) → write `01-vision/problem-frame/BOUNDARY.md`
2. **Rewrite Must NFRs as six-part QAS** using `03-requirements/qas/TEMPLATE.md` (or demote from Must)
3. **Draft SoR vs derived matrix** → `08-verification/` + OQ-02
4. **Stub ports/ICD** for Index, Registry, Resolve, LockCheck, Receipt → `07-system-design/ports-and-adapters/`, `icd/`
5. **Receipt schema draft** → `08-verification/receipts/` + `09-product-tours/proof-tour/` (OQ-05)
6. Only after OQ-01…08 closed/waived → ask human for **wave-1 Approve**

## Do not do next

- Create `core-engine/` / `Cargo.toml` / language monorepo scaffolds
- Treat `nests/*-rust|go|…` as Approved Design
- Implement Phi/Ollama/Lance/Kuzu from inbound AI RE drafts
- Always-apply new mega `.mdc` essays

## Gate references

- Bootstrap: `AGENT_BOOTSTRAP.md`
- Tree: `PRECODE_MAP.md`
- No-code: `12-delivery/no-code-gate/README.md`
- DoR: `00-governance/dor-dod/DEFINITION_OF_READY.md`
- Papers (May–Aug 2026): `research/papers-2026-may-aug/`
- Locked science: `11-science-transfer/locked-transfers/`
