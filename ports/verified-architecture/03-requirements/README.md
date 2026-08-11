# 03-requirements

Authoritative requirements tree (flat `docs/requirements/` is pointers only — do not edit those).

| Artifact | Path | State |
| --- | --- | --- |
| Stakeholder Requirements Specification | `strs/strs-wave1.md` | Draft — no human Accept |
| Software Requirements Specification | `srs/srs-wave1.md` | Draft — language-free Must/Should/Could/Won’t |
| Quality Attribute Scenarios | `qas/` | N-05…N-08 measurable; **N-01/N-02 latency T/U Spike-blocked** |
| Requirements Traceability Matrix | `rtm/rtm-wave1.md` | Draft — OPEN plants / Interface Control Document gaps |

| Stub | Missing artifact |
| --- | --- |
| `moscow-waves/` | Wave MoSCoW cut file (only `.gitkeep`) — MoSCoW lives inside `srs-wave1.md` until extracted |
| `use-cases/` | Numbered use-case files (only `.gitkeep`) — Model Context Protocol cases live under system-design until authored here |

Refuse: product code from Draft rows. Engine/Specification corpus host stays **Rust**; **Refuse Python** runtime (Architecture Decision Record ADR-0001). Map: [PRECODE_MAP.md](../PRECODE_MAP.md).
