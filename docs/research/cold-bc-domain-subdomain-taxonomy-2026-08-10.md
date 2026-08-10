---
title: Cold BC domain/subdomain taxonomy — arXiv · GitHub · DeepWiki Bloom
status: ACTIVE research synthesis — Spec seeds DRAFT; no Implement without per-epic Approve
research date: 2026-08-10
claim tiers: Evidenced / Confirmed / Unknown
product: Python CLI doc-engine
related:
  - docs/research/cold-product-bc-research-map-2026-08-10.md
  - docs/research/stage0/d1-query-agent-retrieval-bc-research-2026-08-10.md
  - docs/research/stage0/d2-d3-certification-fact-stores-bc-research-2026-08-10.md
  - docs/research/stage0/d4-d5-d6-static-join-drift-cli-2026-08-10.md
  - docs/research/stage0/query-packet-bc-research-2026-08-10.md
  - docs/research/modularity/certification-fold-phase-runner-2026-08-10.md
  - docs/research/process/37-operator-agent-surface-cli-mcp-rag-2026.md
  - docs/research/quality-backlog.md
  - docs/research/se-quality-synthesis-2026-08-08.md
do_not:
  - implement from this taxonomy without named Spec Approve
  - treat DeepWiki / embeddings / star counts as merge SoR
  - unattended AI merge; embedding citation SoT; rich/OTel as CI SoT
human_review_floor: true
stars_as_of: 2026-08-10 (GitHub API verified)
arxiv_verified: 2026-08-10 (HTTP 200 sample of all cited IDs)
---

# Cold BC domain → subdomain taxonomy (2026-08-10)

**Question.** Categorize cold-product findings into **domains** and **subdomains**,
ground each with **≥3 arXiv papers**, **healthy high-★ repos** (prefer ~10k★,
recent push, changelog health) plus elegant smaller solutions, and raise
synthesis to Bloom **Evaluate / Create** via DeepWiki + primary docs.

**Method.** Portfolio map → per-domain packets → GitHub API star/push snapshot +
arXiv abs HTTP verify (2026-08-10) → DeepWiki cartography (Evaluate/Create only;
never Spec SoT).

**One-page verdict**

| Stance | Choice |
| --- | --- |
| **Embody** | Structure-first Stage-0 facts + typed query/packet; cert as derived projection; fixture plant = merge SoR; dual human/JSON operator sinks; human review floor |
| **Adopt** | SLSA-/in-toto-*shaped* honesty fields; MCP isolation patterns; oasdiff-class drift sensors; finite GHA OS×shell **campaign** matrix; Typer façade; OPA-like predicate *shape* without Rego dep |
| **Refuse** | Embedding citation SoT; LWW cert; Artifactory OCS as CI SoT; capacity/climb as 98.7 proof; MCP write/codegen; unattended AI merge; rich as CI SoT; star-count as architecture proof |

---

## 1. Domain / subdomain map → epics → packets

| Domain | Subdomains | Epic(s) | Full packet |
| --- | --- | --- | --- |
| **D1** Query & agent retrieval | D1.1 packets/compaction · D1.2 MCP isolation · D1.3 rank/freshness | E-QUERY0 (+ E-OAS0 surface) | [`stage0/d1-query-agent-retrieval-…`](stage0/d1-query-agent-retrieval-bc-research-2026-08-10.md) |
| **D2** Certification & attestation | D2.1 derived views · D2.2 SLSA honesty · D2.3 gate folding | E-CERT0 | [`stage0/d2-d3-…`](stage0/d2-d3-certification-fact-stores-bc-research-2026-08-10.md) §D2 |
| **D3** Fact stores & code KGs | D3.1 deterministic extract · D3.2 incremental index · D3.3 structure vs embedding | E-FACT0 | same packet §D3 |
| **D4** Static analysis join | D4.1 multi-backend · D4.2 QL↔OpenAPI↔facts · D4.3 campaign vs merge SoR | E-CQLJ0 | [`stage0/d4-d5-d6-…`](stage0/d4-d5-d6-static-join-drift-cli-2026-08-10.md) §D4 |
| **D5** Drift & capacity | D5.1 API drift · D5.2 scale preflight · D5.3 threshold honesty | E-TOOL4 slice | same packet §D5 |
| **D6** Operator CLI | D6.1 actionable errors · D6.2 multi-shell matrix | E-OAS0 (OAS16) | same packet §D6 + [`process/37-…`](process/37-operator-agent-surface-cli-mcp-rag-2026.md) |

Spec seeds (thin Approve lists): QUERY0 → `query-packet-bc-research-…`; CERT0 → `modularity/certification-fold-…`; OAS0 → design stub.

---

## 2. Paper inventory (≥3 per domain and subdomain)

*Titles abbreviated; full titles + relevance live in domain packets. All IDs HTTP-200 verified 2026-08-10 unless marked.*

### D1 Query & agent retrieval

| Slice | arXiv (≥3) |
| --- | --- |
| Domain | 2602.03442 · 2605.27123 · 2601.08773 · 2603.27277 · 2310.05736 · 2601.17549 |
| D1.1 | 2310.05736 · 2310.06839 · 2403.12968 · 2501.16214 · 2510.05381 · 2606.26105 · 2307.03172 |
| D1.2 | 2601.17549 · 2604.05969 · 2604.07551 · 2603.20953 · 2606.28679 |
| D1.3 | 2604.14227 · 2607.04281 · 2601.17824 · 2509.17486 · 2406.04744 |

### D2 Certification & attestation

| Slice | arXiv (≥3) |
| --- | --- |
| Domain | 2310.06300 · 2409.05014 · 2602.23193 |
| D2.1 | 2602.23193 · 2203.16684 · 2404.16486 · 2603.27775 |
| D2.2 | 2409.05014 · 2310.06300 · 2605.08363 · 2603.02512 |
| D2.3 | 2511.20313 · 2507.10584 · 2310.06300 |

### D3 Fact stores & code KGs

| Slice | arXiv (≥3) |
| --- | --- |
| Domain | 2601.08773 · 2603.27277 · 2604.26523 |
| D3.1 | 2601.08773 · 2603.27277 · 2604.26523 |
| D3.2 | 2308.09660 · 2603.27277 · 2604.26523 |
| D3.3 | 2601.08773 · 2509.16112 · 2602.11671 |

### D4 Static analysis join

| Slice | arXiv (≥3) |
| --- | --- |
| D4.1 | 2504.16057 · 2511.08462 · 2405.17238 · 2601.10865 |
| D4.2 | 2410.23873 · 2601.12735 · 2504.16833 · 2403.05986 · 2306.05057 |
| D4.3 | 2309.06229 · 2403.09219 · 2402.02961 · 2410.00752 |

### D5 Drift & capacity

| Slice | arXiv (≥3) |
| --- | --- |
| D5.1 | 2008.12808 · 2311.08175 · 2605.24397 · 2605.28148 |
| D5.2 | 2308.09660 · 2401.01571 · 2501.03440 · 2604.12673 · 2605.07900 |
| D5.3 | 1803.04585 · 2309.02395 · 2212.06118 · 2310.09144 · 2608.03535 |

### D6 Operator CLI

| Slice | arXiv (≥3) |
| --- | --- |
| D6.1 | 1608.08219 · 2210.11630 · 2307.10793 · 2209.07365 · 2605.31104 |
| D6.2 | 2212.00908 · 2111.03382 · 2401.15788 · 2602.02307 |

---

## 3. Repository health board (~10k★ prefer; elegant &lt;10k noted)

| Repo | ★ | Pushed | Changelog / health | Domains | Stance |
| --- | ---: | --- | --- | --- | --- |
| modelcontextprotocol/servers | 89383 | 2026-08-10 | releases 2026.7.x | D1 | Adopt read patterns; Refuse write tools |
| colbymchenry/codegraph | 65600 | 2026-08-08 | v1.5.0 | D1/D3 | Adopt tool kinds; Refuse dep / embedding SoT |
| Textualize/rich | 57044 | (active) | healthy | D6 | Adopt TTY; Refuse CI SoT |
| astral-sh/ruff | 49120 | 2026-08-09 | 0.16.x | D6 | Embody actionable codes |
| Aider-AI/aider | 48087 | 2026-05-22 | v0.86.0; slower push | D1/D3 | Adopt RepoMap *idea* |
| langchain-ai/langgraph | 39331 | 2026-08-09 | healthy | D1 | Adopt HITL pattern; Refuse merge SoT |
| continuedev/continue | 35414 | 2026-08-09 | VS Code releases | D1 | Adopt adapter split; Refuse vector SoT |
| getzep/graphiti | 29718 | 2026-08-07 | healthy | D1.3 | Adopt freshness-aware edges |
| PrefectHQ/fastmcp | 27142 | 2026-08-10 | active | D1.2 | Adopt stdio discipline |
| OpenAPITools/openapi-generator | 26659 | 2026-08-10 | healthy | D4/D5 | Adopt OAS ecosystem patterns |
| tree-sitter/tree-sitter | 26591 | 2026-08-09 | v0.26.x | D3/D1 | Embody structure-first (via ast-grep) |
| modelcontextprotocol/python-sdk | 23954 | 2026-08-07 | v2.0.0 | D1 | Explicit Defer pin |
| fastapi/typer | ~19.9k | active | 0.27.x | D6 | Adopt thin grade façade |
| pallets/click | ~17.6k | active | healthy | D6 | Ecosystem under Typer |
| semgrep/semgrep | 16163 | 2026-08-10 | healthy | D4 | Embody-continue Stage-0 twin |
| ast-grep/ast-grep | 15461 | 2026-08-09 | healthy | D4/D3 | Embody structural Stage-0 |
| pytest-dev/pytest | 14398 | 2026-08-10 | 9.x | D6 | Embody failure locality |
| open-policy-agent/opa | 12086 | 2026-08-09 | v1.19.x | D2 | Adopt predicate *shape*; Refuse Rego runtime |
| github/codeql | 9923 | 2026-08-07 | no GH Releases (monorepo OK) | D3/D4/D5 | Embody optional pack; ~10k bar |
| sigstore/cosign | 6196 | 2026-08-07 | v3.x dual-track | D2 | Adopt honesty shape; Defer signing gate |
| oasdiff/oasdiff | 1309 | 2026-08-09 | active | D4/D5 | **Elegant** domain-best OpenAPI diff |
| joernio/joern | 3404 | 2026-08-08 | active | D4 | Elegant CPG; Refuse second merge engine |
| in-toto/attestation | 361 | 2026-08-04 | v1.2.0 | D2 | **Elegant** statement/predicate SoT |
| scip-code/scip | ~0.7k | 2026-08 | active | D3 | Elegant symbol index protocol |

---

## 4. DeepWiki & primary-doc Evaluate synthesis (cross-domain)

**Floor:** DeepWiki = cartography only. Human review before Embody lands in Spec.
**Refuse** DeepWiki prose / embeddings / LLM-judge as citation or 98.7 proof.

| Repo | DeepWiki | Evaluate (for Stage-0 Python CLI) | Create (pattern without dep) | Embody / Adopt / Refuse |
| --- | --- | --- | --- | --- |
| open-policy-agent/opa | hit | Decision∖enforcement split is right *shape*; Rego/WASM wrong *weight* | Pure-Python predicate registry over JSON facts | Embody split · Adopt feature stamps · Refuse OPA runtime |
| tree-sitter/tree-sitter | hit | Incremental CST gold standard; tip already pins ast-grep | Grammar-aware patterns + zero≠absent | Embody via ast-grep · Refuse second parser farm |
| github/codeql | hit | Extract→DB→declarative queries excellent; heavy for default Stage-0 | Models-as-data + fixture corpus SoT | Embody fixture rule coverage · Adopt optional CodeQL · Refuse DB as default SoT |
| modelcontextprotocol/python-sdk (+ servers) | hit | Transport-agnostic tools clean; servers are educational | Stable `dispatch_tool` + thin MCP shell | Embody library SoR · Adopt MCP adapter · Refuse MCP as Stage-0 SoT |
| sigstore/cosign / in-toto/attestation | hit | Cosign strong supply-chain UX, wrong default dep; in-toto elegant Spec→bindings | `certification.json` as subject+predicate+digest | Embody attestation *shape* · Refuse Fulcio/Rekor merge gates |
| astral-sh/ruff / pytest-dev/pytest | hit | Actionable codes + nodeids = operator-error gold | Stable gate codes + path:line + fix hint; no pipe-masked exits | Embody UX · Refuse lint-as-analysis-kernel |
| colbymchenry/codegraph | hit | Structure-first KG→MCP is right *story*; ★≠ necessity | Typed query kinds (callers/blast) without embedding SoT | Adopt kinds · Refuse CodeGraph dep as evidence |
| facebook/sapling (optional) | hit | Incremental/sparse WC patterns | PathCohesion + refuse cross-worktree coverage combine | Adopt git worktree ops · Refuse Eden dep |

### Elegant under-10k (architecture &gt; stars)

in-toto/attestation · DSSE · pluggy · py-tree-sitter · oasdiff · joern (campaign-only) · scip

---

## 5. Cross-domain Bloom (Evaluate → Create)

| Evaluate | Create |
| --- | --- |
| Where tip already matches external best practice (dispatch_tool, derived cert, fixture≠campaign, freshness labels) | Named Spec decisions Q0 / C0 / CQLJ / TOOL4 / OAS16 with Acceptances |
| Where high-★ products tempt wrong SoT (embeddings, LangGraph, rich CI, Cosign merge) | Explicit Refuse table + human_review_floor |
| Where elegant &lt;10k beats megarepos (in-toto, oasdiff, SCIP) | Prefer *shape* over pin; Spike before any new runtime SoR (≥10k bar still binds *if* we pin) |

---

## 6. Ordered Spec → Implement (unchanged portfolio discipline)

1. **E-QUERY0** Approve Q0-1–Q0-10 (D1 packet)  
2. **E-CERT0** Approve C0-* (D2)  
3. **E-FACT0** Spec promote (D3)  
4. **E-CQLJ0** join contracts (D4)  
5. **E-TOOL4** drift/capacity honesty (D5)  
6. **E-OAS0** including OAS16 matrix (D6) — parallel Spec OK; **one** Implement tip stream after Approves  

Invariants: fail_under **98.7** · complexipy **≤5** · LOC **≤225** · no `utils/` · policy **16-A** · Spec → Implement → Verify → Archive.

---

## 7. Adversarial checklist

- [ ] Every subdomain has ≥3 real arXiv IDs (verified)?  
- [ ] Star/push stamped with date; elegant &lt;10k called out without shame?  
- [ ] DeepWiki used only at Evaluate/Create — never as citation SoT?  
- [ ] Embedding / LWW cert / OCS-as-CI / capacity-as-Cover% still Refuse?  
- [ ] Human review floor + no unattended AI merge?  
- [ ] No Implement ticket opened from this memo alone?

---

## Exit

This taxonomy is the **forced index** for cold BC research. Detail lives in D1/D2–D3/D4–D6 packets. Next human action: Approve Spec seeds in epic order — not code.
