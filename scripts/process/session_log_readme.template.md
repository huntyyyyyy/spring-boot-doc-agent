# Session log (nested)

Append-only record of commits that move assumptions in
`docs/process/steering-prompts/` (see `CLAUDE.md`). **Not** research SoT;
**not** a chat dump.

## Layout

| Path | Role |
| --- | --- |
| [`../session-log.md`](../session-log.md) | Stable stub (claims / old links) |
| `START__slug.md` / `START__END__slug.md` | LOC-budget shards (see naming) |
| This README | Index + append recipe + algorithm |

## Naming / sort key

Filenames are **date-first** (so `ls` stays chronological) plus a **content slug**
from the first entry title (`## YYYY-MM-DD — title` → kebab-case):

| Pattern | When |
| --- | --- |
| `YYYY-MM-DD__topic-slug.md` | Single-day shard |
| `YYYY-MM-DD__YYYY-MM-DD__topic-slug.md` | Multi-day pack |
| `…__topic-slug-2.md` | Collision on the same span+slug |

The slug is a look-first hint, not a full abstract — open the file for entries.

## Packing algorithm

**Target:** each shard ≤ **{target}** lines (header + entries).

1. Parse entry blocks at `## YYYY-MM-DD` (**preserve original order**).
2. **Greedy pack:** add the next entry while
   `header_lines + sum(entry_lines) ≤ {target}`.
3. If the next entry would exceed the budget, flush and start a new shard.
4. Never split an entry. A single oversize entry may exceed the target alone.
5. **Name** with date-first span + first-entry **content slug** (`START__slug.md`).

Month/week calendars alone are **refused** as the size SoT.

Maintainer re-pack: `python3 scripts/process/pack_session_log.py`
(`--from-git HEAD:docs/process/session-log.md` for monolith rebuild;
`--index-only` after appending to an existing shard). Chronology SoT for
re-reads is `session-log/.pack-order` (not `ls` alpha).

## Shards (live)

| File | Span | Lead title | Entries | Lines |
| --- | --- | --- | ---: | ---: |
{rows}

**Totals:** {entry_count} entries → {shard_count} shards; max {max_lines} lines;
over-budget {over}.

## How to append

1. Open the **latest** shard (last row above). If it is near **{target}** lines,
   create `YYYY-MM-DD__your-topic.md` instead.
2. Append one distilled entry at the **bottom**.
3. Do **not** rewrite older shards to tidy dates/SHAs.
4. Do **not** append to [`../session-log.md`](../session-log.md).

### Entry template

```
## <YYYY-MM-DD> — <short description>
Commit: <short sha, or "uncommitted" if writing before commit>
Tests: <pass/fail summary, or "not run">
Assumptions affected:
- `<prompt or doc>` — "<assumption>" — [Resolved — …] / [Still accurate] / [New info — …]
Files touched: <comma-separated list>
```

## Refuse

- Chat transcripts as research SoT
- Rewriting historical entries for tidy dates/SHAs
- Calendar-only splits that ignore LOC
- Reviving a multi-thousand-line `session-log.md` body
