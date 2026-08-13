# Research SoR — domain map (forced entry)

**Before** weighing frameworks or writing Spec/Implement for design-shaped work,
read this map and open the matching domain memo. Soft skills are not enough;
Cursor look-first hooks inject this path and gate design-shaped writes.

| Domain | Path | Use when |
| --- | --- | --- |
| **Cross-cutting SoT** | [`quality-backlog.md`](quality-backlog.md) (Active tip + queues; Done ledger), [`archive/quality-backlog-ticket-ledger-2026-08-10.md`](archive/quality-backlog-ticket-ledger-2026-08-10.md) (frozen P-tables), [`se-quality-synthesis-2026-08-08.md`](se-quality-synthesis-2026-08-08.md), [`cold-product-bc-research-map-2026-08-10.md`](cold-product-bc-research-map-2026-08-10.md), [`cold-bc-domain-subdomain-taxonomy-2026-08-10.md`](cold-bc-domain-subdomain-taxonomy-2026-08-10.md), [`cold-bc-dimensional-mental-map-2026-08-10.md`](cold-bc-dimensional-mental-map-2026-08-10.md) | **One** Active tip; parked Drafts; Embody/Adopt/Refuse; cold BC portfolio; D1–D6; dimensional lattice; **polyglot BFS → [`process/39-…`](process/39-polyglot-cli-toolkit-bfs-2026-08-10.md)** |
| **findings/** | [`findings/`](findings/) | Stalker ledger entries (STK2) — compact events + gap IDs; not chat dumps |
| **process/** | [`process/`](process/) | SDD, foundational SE, frameworks, **dynamics** ([`05`](process/05-dynamics-neuromorphic.md), [`43` umbrella](process/43-physical-info-dynamics-computing-2026-08-10.md), [`21` physical A–I](process/21-physical-unconventional-computing-2026.md), [`45` isomorphisms](process/45-cross-domain-isomorphisms-structure-vs-substrate-2026-08-10.md), [`20` theory A–H](process/20-theory-domains-problem-first-gates-2026.md)), façade/research hooks, legacy remediation Spec, docs taxonomy, **watch/stalker agents**, **agent context (26–28: bloat · ★ discernment · algorithm-first build)**, **control-plane closed-loop (E-CPL0)**, **operator/agent surface CLI+MCP+retrieval (E-OAS0)**, **CLI DX/a11y/dual-sinks**, **polyglot BFS (E-POLY0/0b)**, **language excellence domains→subdomains (E-LANG0)**, **problem-first RAG/DS/CLI**, **lint/import resolution ruff vs ty (E-LINT0 [`46`](process/46-lint-import-resolution-ruff-vs-ty-2026-08-10.md))**, **MDC DevEx activation algebra (E-MDC0 [`47`](process/47-cursor-mdc-rules-devex-ai-repos-2026-08-10.md))**, **complete toolscape agent+repo+dev (E-TOOL0 [`48`](process/48-complete-toolscape-agent-repo-developer-2026-08-10.md))**, **intent-kernel spike review (E-IK0 [`49`](process/49-intent-kernel-v2-spike-first-adversarial-review-2026-08-13.md))** |
| **coverage-quality/** | [`coverage-quality/`](coverage-quality/) | Oracle vs climb, metrics, adequacy, suite-stalking; **Rust toolscape + release scans (Harn/Nimbus/noprop)** |
| **ci/** | [`ci/`](ci/) | Workflow modularity, CI UX, CodeQL signals skip |
| **kitchen/** | [`kitchen/`](kitchen/) | Kitchen harness modernization |
| **bounded-contexts/** | [`bounded-contexts/`](bounded-contexts/) | Product BC seams: Stage-0 ports, test-suite BCs, tools waves, AstGrepBackend split, **tach dependency blueprint**, **DDD repo-structure packet E-REPO0 (21–24)** + **E-REPO1-A first nest (25)** + **E-COH1 public-surface fitness (21-coh1)** + **certification-fold phase runner** — formerly misnamed `modularity/` |
| **stage0/** | [`stage0/`](stage0/) | Covering/absence/recall + claim-symbol ADRs; **tailored ast-grep packs (E-AST0)**; **D1 query (E-QUERY0)**; **D2–D3 cert+facts**; **D4–D6 join/drift/CLI**; fact-store next-phase seeds |
| **archive/** | [`archive/`](archive/) | Superseded WIP, receipts, [`claude-lore/`](archive/claude-lore/) — **not** Spec SoT |

## Rules (DOC1 / DOC10)

1. Domains are **≤2 levels** deep under `docs/research/`.
2. Epic IDs (`E-CM0`, `E-DOC0`, …) in frontmatter are the primary cross-ref — not ordinals.
3. If a domain exceeds ~**12** active memos or needs a third nesting level, **reshape** (merge / synthesis / new top-level domain) — do not deepen.
4. Chat transcripts and raw session lore are **refused** as research SoT.
5. Process logs live under [`docs/process/`](../process/) (session-log, tool-quirks, steering-prompts).
6. **Future-dev plans** (Spec Draft / epic Implement tickets): skill [`principal-se-research-epic`](../../.cursor/skills/principal-se-research-epic/SKILL.md) — Bloom **1→Create** with DeepWiki MCP `ask_question` + primary `llms.txt` **before** code. Set `bloom_gate: required-through-create` in frontmatter.

## Look-first (Cursor)

- `beforeSubmitPrompt` injects this map.
- Design-shaped `Write` / `StrReplace` requires a session Read of this file (receipt).
- Cloud agents: do **not** rely on `sessionStart` ([Cursor hooks](https://cursor.com/docs/hooks.md)).

Spec: [`process/18-docs-research-taxonomy-claude-consolidation-2026.md`](process/18-docs-research-taxonomy-claude-consolidation-2026.md).
Skill: `.cursor/skills/principal-se-research-epic/SKILL.md`.
