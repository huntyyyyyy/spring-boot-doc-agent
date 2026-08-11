---
title: Whole-words glossary — full phrases required in prose
status: ACTIVE
audience: [agent, developer]
---

# Whole words

In sentences, tables, and prompts: prefer **full phrases**. Short labels allowed
inside `` `paths` ``, fenced code, or once after the full phrase
(`Architecture Decision Record ADR-0001`). Bare short form elsewhere is a
**style preference** (expand-on-first-use) — not a CI/hook reject. Cold-start
files may use short forms after first expansion; do not treat this glossary as
an unenforceable “reject” gate.

| Prefer | Avoid bare |
| --- | --- |
| Specification phase / specification artifacts | Spec |
| Definition of Ready | DoR |
| Definition of Done | DoD |
| Stakeholder Requirements Specification | StRS |
| Software Requirements Specification | SRS |
| Requirements Traceability Matrix | RTM |
| Quality Attribute Scenario | QAS |
| Interface Control Document | ICD |
| Verification and Validation | V&V |
| Retrieval-Augmented Generation | RAG |
| Cursor rule files (`.mdc`) | MDC |
| Model Context Protocol | MCP |
| Language Server Protocol | LSP |
| command-line interface | CLI |
| Architecture Tradeoff Analysis Method | ATAM |
| Architecture Decision Record | ADR |
| Decision Matrix / Selection Taxonomy / Decision Framework | bare “matrix” |
| First-Order Computation Tree Logic | FO-CTL |
| Stateful Tool-Enabled Agentic Deployment | STEAD |
| Artifact-Anchored Verification Memory (paper *EA-Graph*) | EA-Graph alone |
| Multi-Agent Orchestration with External Knowledge and Hierarchical Memory | MAAD |
| Proof-or-Stop | PoS |
| Cue-anchored working memory | Cue-WM |
| open question | OQ |
| Wave 0 / Wave 1 | W0 / W1 |
| System of Record / Source of Truth | SoR / SoT |
| Dependency Injection | DI |
| Intermediate Representation | IR |
| non-functional requirement | NFR |
| breadth-first search | BFS |
| minimum viable product | MVP |
| Concrete Syntax Tree | CST |
| Source Code Index Protocol (SCIP index) | SCIP alone |
| WebAssembly | WASM alone |
| Model Context Protocol SEP (numbered proposal) | SEP alone |
| Temporal Logic of Actions / TLA+ TLC model checker | TLC alone |
| Analytic Hierarchy Process | AHP |
| Multi-Criteria Decision Analysis | MCDA |
| Java Modelling Tools | JMT |
| bounded context | BC |
| large language model | LLM (expand on first use per file) |
| software development kit | SDK alone |
| TypeScript | TS alone in prose |
| Architecture Decision Records (plural) | ADRs |

## Paper titles (June–August 2026 set)

| Paper title | arXiv |
| --- | --- |
| Proof-or-Stop: Don't Trust the Agent, Trust the Evidence | 2607.14890 |
| From Prompts to Contracts: Harness Engineering for Auditable Enterprise LLM Agents | 2607.08028 |
| Delivery, Not Storage: Cue-Anchored Working Memory as a Harness Property for Coding Agents | 2607.20972 |
| EA-Graph: Artifact-Anchored Verification Memory for Coding Agents under Upstream Drift | 2608.04278 |
| Formal Verification of Agentic Systems over Operational Data (Stateful Tool-Enabled Agentic Deployments) | 2608.03609 |
| Harnessing Code Agents for Automatic Software Verification (Aria) | 2607.06341 |
| Bridging Requirements and Architecture: Multi-Agent Orchestration with External Knowledge and Hierarchical Memory | 2606.01385 |
| HyperTool: Beyond Step-Wise Tool Calls for Tool-Augmented Agents | 2606.13663 |
| DynamicMCPBench: A Trace-Grounded, Effect-Scored Benchmark for LLM Agents over Live MCP Servers | 2607.20531 |

Path short labels (e.g. `QAS-N-01-warm-resolve.md`): expand beside first mention
in that file.
