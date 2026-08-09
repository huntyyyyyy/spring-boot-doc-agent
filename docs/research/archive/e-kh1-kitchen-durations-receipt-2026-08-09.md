# E-KH1 kitchen durations receipt (sensor, not SoT)

- Command: `pytest tests/doc_engine/test_kitchen_sink_ch*.py -q --durations=15`
- Result: **63 passed in 3.72s** (≤8s KH1-6 sensor; K7 closed)
- Scope: KH-S1 = **session** `kitchen` fixture; function-scoped scratch copies for faults
- Date: 2026-08-09
