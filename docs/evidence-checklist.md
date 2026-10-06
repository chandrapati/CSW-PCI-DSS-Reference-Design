# PCI DSS v4.0 — CSW Evidence Checklist

A printable worklist for the evidence owner. For each item: **what** to export, **where** from in CSW, the **PCI requirement** it supports, and the **cadence**. Tick as you collect; file exports to immutable storage (not screenshots taken during audit week).

> Legend — 🟢 Direct · 🟠 Supporting. CSW evidence is an input to compliance, not an attestation.

---

## Phase 1 — Coverage (Days 1–10)

- [ ] In-scope host list reconciled to **CSW Inventory** (100% or documented exceptions) — *Req 12.5.2* 🟢
- [ ] Labels applied: `compliance:pci`, `data:chd`, `env:prod`, `app:*`, `owner:*`
- [ ] CSW scope tree created (CDE / CDE-Connected / Out-of-Scope / Third-Party)
- [ ] **Export:** inventory CSV + agent-status screenshot → `evidence/01-coverage/`

## Phase 2 — Baseline (Days 11–28)

- [ ] ADM running on the PCI scope for ≥ 2 weeks (full business cycle)
- [ ] Unexpected flows documented (shadow IT, vendor egress, scope creep)
- [ ] App owners signed the cluster-to-application mapping
- [ ] **Export:** ADM diagram + flow samples with process context → `evidence/02-baseline/` — *Req 1.2.1* 🟢

## Phase 3 — Policy (Days 29–45)

- [ ] Default-deny posture defined for the CDE scope
- [ ] ADM-imported rules refined; **Simulation** run ≥ 1 week
- [ ] Change tickets raised for false-positive fixes; exception register updated
- [ ] **Export:** policy export + simulation report → `evidence/03-policy/` — *Req 1, 7* 🟢

## Phase 4 — Operate (ongoing)

- [ ] Enforcement enabled on the CDE; negative test recorded in **Denied Connections**
- [ ] SIEM integration verified with sample events — *Req 10.3.1*
- [ ] Quarterly binder assembled (table below)
- [ ] **Export:** enforcement screenshot + quarterly binder → `evidence/04-operate/`

---

## Recurring evidence pack

| # | Evidence item | CSW location | Requirement | Cadence | Collected |
|---|---|---|---|---|:--:|
| 1 | CDE network policy export | Defend → Policy Workspaces | Req 1 | Per assessment | ☐ |
| 2 | CDE inbound/outbound flow log | Investigate → Flow Search | Req 1, 10 | Continuous | ☐ |
| 3 | Policy-violation report | Alerts → Triggered Events | Req 10 | Monthly | ☐ |
| 4 | Vulnerability + reachability (CDE) | Investigate → Vulnerability | Req 6, 11 | Weekly | ☐ |
| 5 | Scope-membership snapshot | Inventory → Export | Req 1, 7, 12.5.2 | Monthly | ☐ |
| 6 | Anomaly / baseline-deviation log | Alerts → Dashboard | Req 10, 11 | Monthly | ☐ |
| 7 | ADM dependency map (CDE) | Investigate → ADM | Req 1 | Quarterly | ☐ |
| 8 | Process audit log (CDE) | Investigate → Process Search | Req 10 | On-demand | ☐ |

---

## Suggested evidence folder layout

```
evidence/
├── 01-coverage/     inventory.csv, agent-status.png
├── 02-baseline/     adm-map.pdf, flow-samples.csv
├── 03-policy/       policy-export.json, simulation-report.pdf, exceptions.xlsx
└── 04-operate/      QYYYY-Qn/  (quarterly binder: items 1–8)
```

*Validate sufficiency of every item with your QSA. CSW does not replace ASV scans, key-management, physical, or HR evidence.*
