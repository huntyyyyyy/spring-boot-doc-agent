---
title: STATUS — single pointer for cold agents
status: ACTIVE
last_reviewed: '2026-08-10'
---

# STATUS

## Phase

**Spec / gap-fill** — planning corpus only. **Implement = Refuse.**

## Product one-liner (draft — human Accept still open on OQ-01)

A **local developer tool** that builds a virtual dependency/DI graph, evaluates
git-versioned locks, and emits proof-tour receipts — Unknown over wrong.
See `01-vision/problem-frame/BOUNDARY.md`.

**Architecture decisions (draft):** monorepo *after* Spec; ship CLI (+ later
LSP); refuse org SaaS MVP. Full brief:
`07-system-design/ARCHITECTURE_BRIEF.md`.

## Next tasks for any agent (do in order)

1. **Human review** `ARCHITECTURE_BRIEF.md` + `BOUNDARY.md` → Accept or amend OQ-01
2. **Write Must QAS files** (`03-requirements/qas/`) from incomplete NFRs — or demote
3. **Fill ICD drafts** listed in `07-system-design/icd/README.md` (lock-ir, registry SQL, resolve-result)
4. **Mark OQ-02…05** SPIKE→CLOSED when SoR/ports/receipt drafts Accepted
5. **OQ-08** wave-1 BC set (likely: engine+registry+locks only)
6. Ask human for **wave-1 / W0 Approve** when DoR rows move

## Do not do next

- Create `core-engine/` / `Cargo.toml` / nine-language scaffolds
- Treat LanceDB/Phi/Kuzu as symbol or verify SoR
- Skip QAS and jump to “latest frameworks” codegen

## Gate references

- Brief: `07-system-design/ARCHITECTURE_BRIEF.md`
- Bootstrap: `AGENT_BOOTSTRAP.md`
- Leaders/stars: `research/leaders-adoption/`
- DoR: `00-governance/dor-dod/DEFINITION_OF_READY.md`
- Waves: `12-delivery/waves/`
