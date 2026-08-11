# Pre-code domain tree (BFS)

Industry-shaped nesting: **concern → problem → gap → decision**.  
Language scaffolds and product code are **out of scope** until
`12-delivery/no-code-gate/` is green for the active wave.

Authoritative classification memo:

→ [`research/pre-code-bfs/taxonomy-bfs-before-codegen-2026-08-10.md`](research/pre-code-bfs/taxonomy-bfs-before-codegen-2026-08-10.md)

| Level | Top folder | Purpose |
| --- | --- | --- |
| 0 | `00-governance/` | Definition of Ready/Definition of Done, claim tiers, promotion |
| 1 | `01-vision/`, `02-stakeholders/` | Problem + people |
| 2 | `03-requirements/`, `04-constraints/` | **SoT** for REQs ≠ constraints; Quality Attribute Scenario; open questions |
| 3 | `05-quality-architecture/`, `06-domain/` | Architecture Tradeoff Analysis Method + DDD (**stubs** until filled) |
| 4 | `07-system-design/` | Ports, Interface Control Document, options; C4 **brief** here |
| 5 | `08-verification/`, `09-product-tours/` | L1–L3; tours are **stubs** |
| 6 | `10-rag-corpus/`, `11-science-transfer/` | Retrieval contracts (**stubs**); science transfer notes |
| 7 | `12-delivery/` | Waves, spikes, no-code gate |

**Legacy flat `docs/`:** Architecture Decision Records + C4 levels + standards stay.
`docs/requirements/` and `docs/constraints/` are **pointers** to `03/` / `04/`.
`nests/` = language bounded contexts (nest 08 Python **REFUSED**).

**Principal architecture brief:**
[`07-system-design/ARCHITECTURE_BRIEF.md`](07-system-design/ARCHITECTURE_BRIEF.md)

**Architecture Decision Record index:** [`docs/adr/README.md`](docs/adr/README.md)
