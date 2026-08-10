# Root `skills/` mirror (legacy alias — retire Spec pending)

**System of record:** [`adapters/claude/skills/`](../adapters/claude/skills/).

Marketplace packaging uses `adapters/claude` (see `.claude-plugin/marketplace.json`).
This root tree remains a **byte-equal synced mirror** of product skills so Cursor/local
workflows that resolve `skills/…` keep working until an E-REPO retire Spec lands:

- `document-spring-repo` (includes `references/`)
- `capacity-preflight`
- `citation-coverage`
- `semantic-pipeline-eval` (includes `references/`)

Adapter-only skills (`directional-tests`, `tool-quirks`) are **not** mirrored here.

**Future-facing prune (E-REPO1-A / DOMAIN_MAP §4):** delete this mirror after
(1) retire Spec Approve, (2) equality-gate rewrite, (3) confirmed resolve-path
migration. Do **not** diverge intentionally before that — CI still requires
byte equality (`tests/adapters/test_adapter_layout.py`).

Edit the adapter copy first, then sync here.
