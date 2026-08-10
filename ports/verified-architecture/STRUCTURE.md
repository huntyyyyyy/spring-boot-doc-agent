---
title: Repository structure visual
status: ACTIVE
---

# Structure visual

## Tree (what you push as the new repo root)

```text
verified-architecture/          ← make THIS the git root
│
├── AGENT_BOOTSTRAP.md          ★ cold start #1
├── STATUS.md                   ★ cold start #2
├── AGENT_WALKTHROUGH.md        ★ sequential chain + mermaid
├── STRUCTURE.md                ★ this file
├── PRECODE_MAP.md
├── HOW_TO_PRIME_AGENTS.md
├── AGENTS.md                   (thin Cloud ingest)
├── CONTRIBUTING.md
├── EXPORT.md
├── README.md
├── PROVENANCE.md
│
├── .cursor/
│   ├── rules/                  (≤2 alwaysApply; rest globs/requested)
│   └── skills/                 cold-start, fill-wave-gap, rag-retrieve, promote-claim
│
├── 00-governance/              DoR, claim tiers, promotion
├── 01-vision/                  BOUNDARY.md
├── 02-stakeholders/            actors, opscon, signoff
├── 03-requirements/            strs, srs, qas, rtm, use-cases
├── 04-constraints/             CON + OQ-01…08
├── 05-quality-architecture/    ATAM, tactics, tradeoffs, formal
├── 06-domain/                  ubiquity, BCs, info model, UNKNOWN-TAXONOMY
├── 07-system-design/           ARCHITECTURE_BRIEF, ports, icd, adr, options, c4
├── 08-verification/            ★ VERIFY_STACK + L1/L2/L3 + receipts + claim-memory + stead
├── 09-product-tours/           proof-tour, lsp, ghost, lock-sync, polyglot-bell
├── 10-rag-corpus/              catalog, packs, retrieval contracts, eval
├── 11-science-transfer/        locked transfers / refuse substrates
├── 12-delivery/                waves, spikes, no-code-gate, pilot-before-refuse
│
├── research/                   evidence (retrieve one pack — never always-load)
│   ├── INDEX.md
│   ├── adversarial/            incl. july-august-2026-overturn-review.md
│   ├── papers-2026-may-aug/
│   ├── leaders-adoption/
│   ├── pre-code-bfs/
│   ├── mdc-devex/
│   ├── polyglot/ atam-formal/ layers-of-truth/
│   └── …
│
├── docs/                       LEGACY flat RE/C4/ADR (prefer 00–12 for new work)
└── nests/                      LEGACY language placeholders → prefer 07/.../options/
```

## Authority layers

```mermaid
flowchart TB
  subgraph always [Always-on]
    R0[00-constitution.mdc]
    R1[01-rag-progressive-disclosure.mdc]
  end

  subgraph entry [Entry — read in order]
    B[AGENT_BOOTSTRAP]
    S[STATUS]
    W[AGENT_WALKTHROUGH]
    P[PRECODE_MAP]
  end

  subgraph law [Product law — Spec]
    V[08 VERIFY_STACK]
    EG[claim-memory EA-Graph]
    ST[stead STEAD constraints]
    AR[ARCHITECTURE_BRIEF]
  end

  subgraph evidence [Evidence — retrieve one]
    RX[research/INDEX → one pack]
  end

  subgraph legacy [Legacy — do not prefer]
    D[docs/]
    N[nests/]
  end

  always --> entry
  entry --> law
  law --> evidence
  entry -.-> legacy
```

## Verify stack (Must — not graph alone)

```mermaid
flowchart LR
  L1[L1 Index/SCIP] --> L2[L2 Graph + LockCheck]
  L2 --> L2b[L2b EA-Graph claims]
  L2b --> R[Receipts]
  R --> T[STEAD tool constraints]
  A[Agent proposes] --> L2
  A --> T
```
