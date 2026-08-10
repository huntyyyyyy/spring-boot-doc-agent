---
title: ATAM Quality Attribute Scenario standard
status: ACTIVE
date: '2026-08-10'
---

# Quality Attribute Scenario (QAS) standard

From SEI ATAM: a non-functional need may influence Design **only** as a
six-part scenario.

| Field | Meaning |
| --- | --- |
| Stimulus source | Who/what triggers |
| Stimulus | Exact event |
| Environment | Load / mode / failure / peak |
| Artifact | Component that responds |
| Response | Observable behavior |
| Response measure | Quantitative pass/fail + how measured |

**Incomplete:** “p95 ≤ 2s” alone.  
**Complete:** all six fields; measure method named; MEASURE-TBD only pre-Spike.

Live scenarios: [`../requirements/qas.md`](../requirements/qas.md).
