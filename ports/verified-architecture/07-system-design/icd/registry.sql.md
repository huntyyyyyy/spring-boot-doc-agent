---
title: Registry SQL sketch
status: DRAFT
---

# ICD-REG — SQLite registry (sketch)

Derived only. Wipe/rebuild OK.

```sql
-- nodes: beans, types, packages
CREATE TABLE node (
  id TEXT PRIMARY KEY,
  kind TEXT NOT NULL, -- bean|type|package|file
  symbol TEXT,
  file TEXT,
  meta_json TEXT
);

CREATE TABLE edge (
  id TEXT PRIMARY KEY,
  kind TEXT NOT NULL, -- injects|imports|depends|package_dep
  src TEXT NOT NULL REFERENCES node(id),
  dst TEXT NOT NULL REFERENCES node(id),
  witness_file TEXT,
  witness_line INTEGER
);

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
