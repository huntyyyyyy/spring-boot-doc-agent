---
title: Registry SQL sketch
status: DRAFT
---

# SQLite registry (derived)

Derived only — wipe/rebuild OK. Never policy System of Record (locks stay in
git). Fail-mode: treating this DDL as merge authority without deterministic
engine LockCheck.

**Non-normative illustration:** comments like `-- bean|type|…` and unconstrained
`TEXT` columns for `evidence_strength` / `freshness` / `disposition` are
vocabulary sketches. Normative enums live in
`ea-graph-claims.schema.json` — do not treat this SQL as Acceptable without
CHECK constraints aligned to that schema (or an explicit “SQL is illustration
only” Accept).

```sql
-- nodes: beans, types, packages
-- kind comment vocabulary only — non-normative; no SQL CHECK
CREATE TABLE node (
  id TEXT PRIMARY KEY,
  kind TEXT NOT NULL, -- bean|type|package|file (illustration)
  symbol TEXT,
  file TEXT,
  meta_json TEXT
);

CREATE TABLE edge (
  id TEXT PRIMARY KEY,
  kind TEXT NOT NULL, -- injects|imports|depends|package_dep (illustration)
  src TEXT NOT NULL REFERENCES node(id),
  dst TEXT NOT NULL REFERENCES node(id),
  witness_file TEXT,
  witness_line INTEGER
);

-- claim.* TEXT unconstrained here; enums SoT = ea-graph-claims.schema.json
CREATE TABLE claim (
  claim_id TEXT PRIMARY KEY,
  kind TEXT NOT NULL,
  evidence_strength TEXT NOT NULL,
  freshness TEXT NOT NULL,
  disposition TEXT NOT NULL,
  payload_json TEXT
);

CREATE TABLE claim_anchor (
  claim_id TEXT REFERENCES claim(claim_id),
  artifact_id TEXT NOT NULL,
  content_digest TEXT NOT NULL,
  PRIMARY KEY (claim_id, artifact_id)
);
```
