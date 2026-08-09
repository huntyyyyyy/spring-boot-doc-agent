## Summary

<!-- What changed and why (1–3 bullets). -->

## Spec / SoT check (coverage & gates)

- [ ] Spec → Implement → Verify → Archive; **one active tip writer** on this branch (no parallel SoT fork / force-push tip thrash)
- [ ] If dual-mode / Cover% touched: climb writes `coverage.climb.xml` only; oracle SoR remains `coverage.xml` (policy 16-A)
- [ ] Remeasured oracle on a salient trigger (climb batch / before PR / stale inventory) — not every micro-edit
- [ ] Did **not** treat climb Cover%, LLM-judge, or fuzzy “confidence of green” as the 98.7 floor

## Test plan

- [ ] Relevant unit / climb suites
- [ ] `doc-engine quality-gates` / pre-PR when path risk requires it
