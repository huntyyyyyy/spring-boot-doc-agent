---
title: Locked science transfers (E-DYN1)
status: ACTIVE
date: '2026-08-10'
---

# Locked transfers

Only rows below may leave the lab. Anything else as tip kernel / merge gate /
CI floor → reject.

## Theory → product

| Field | Failure addressed | Allowed here | Forbidden |
| --- | --- | --- | --- |
| Nonlinear dynamical systems | Tip thrash / long-horizon instability | Metaphor for thrash | Gate plant |
| Information theory | Sensor≠Source of Truth confusion | Label sensors; refuse entropy-as-merge | Entropy CI floor |
| Statistical mechanics | Soft→hard threshold language | Metaphor only | — |
| Linear algebra / probability | Flake / rare-event language | Flake wording | Probabilistic “green” |
| Thermodynamics | Remeasure / green-AI cost | Cost language | \(kT\ln 2\) as CI floor |
| Control theory | Observability + rate caps | Those | Cover% PID |

## Physical / unconventional computing

| Substrate | Verdict |
| --- | --- |
| DNA / molecular | **Refuse tip** |
| Far-from-eq / CRN reservoirs | **Refuse**; work-budget metaphor OK |
| Ionic / iontronic | **Refuse** |
| Neuromorphic (Loihi, …) | **Refuse runtime**; Adopt saliency debounce only |
| Physical reservoir / memristor / ferrofluid | **Refuse hardware**; Adopt climb→oracle ≈ reservoir→readout |
| Analog NN / in-memory / reaction-diffusion | **Refuse** (non-hermetic / wrong category) |

## Enhancement-lane languages (not tip kernels)

| Family | Allowed role | Refuse |
| --- | --- | --- |
| Go | Daemon/watch, dual-sink UX, SARIF hosts | Rewriting product tip in Go |
| Ruby | Packwerk-shaped lock vocab, Asciidoctor/SARIF | Ruby tip kernel |
| Clojure | Malli/Spec, DataScript facts, bb ops | Merge authority |

Stack locks elsewhere: Rust Spec corpus Model Context Protocol host; TypeScript
IDE presentation only; WebAssembly LockCheck Could / Wave-3.
