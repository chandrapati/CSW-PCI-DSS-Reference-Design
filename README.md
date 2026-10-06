# Cisco Secure Workload — PCI DSS v4.0 Reference Design

![Visitors](https://visitor-badge.laobi.icu/badge?page_id=chandrapati.CSW-PCI-DSS-Reference-Design&left_text=visitors)

![Cisco Secure Workload compliance reference design](assets/hero.png)

![Framework](https://img.shields.io/badge/Framework-PCI%20DSS%20v4.0-003366)
![Platform](https://img.shields.io/badge/Platform-Cisco%20Secure%20Workload%204.0-1BA0D7)
![Type](https://img.shields.io/badge/Type-Reference%20Design-107C41)
![Evidence](https://img.shields.io/badge/Evidence-not%20attestation-C55A11)

> A step-by-step blueprint for building **Cisco Secure Workload (CSW)** so a merchant or service provider can **isolate its Cardholder Data Environment (CDE)** and **produce the machine-generated evidence** a QSA expects under PCI DSS v4.0 — segmentation, live flow maps, vulnerability reachability, logging, and change-drift detection.

CSW does **not** certify PCI compliance. It turns workload communication, process activity, and inventory into **evidence** that your team, your compliance function, and your QSA can review. This repo shows how to stand that evidence up and keep it current between assessments.

---

## What's in this repo

| Document | For | Use it to |
|---|---|---|
| **[Reference Design](CSW-PCI-DSS-Reference-Design.md)** | SE / platform / security engineering | Build CSW end-to-end: architecture, scopes, labels, ADM, enforcement, per-requirement evidence |
| **[Compliance Report](#the-compliance-report--what-your-assessor-gets)** ([PDF](CSW-PCI-DSS-Compliance-Report.pdf) · [DOCX](CSW-PCI-DSS-Compliance-Report.docx)) | Compliance team, QSA, exec | Hand to your assessor: color-coded control-by-control mapping + the exact evidence package (see showcase below) |
| **[Evidence Checklist](docs/evidence-checklist.md)** | Evidence owner | A printable, per-requirement "what to export, from where, how often" worklist |
| **[POV / Workshop Plan](docs/pov-plan.md)** | SE + customer | Run a 45-day proof-of-value on one CDE boundary |

---

## How CSW produces PCI evidence — the big picture

```mermaid
flowchart LR
    A[1. Coverage<br/>Agents + connectors<br/>label every CDE workload] --> B[2. Baseline<br/>ADM builds a live<br/>CDE flow map]
    B --> C[3. Policy<br/>Default-deny, allowlist,<br/>Simulation mode]
    C --> D[4. Operate<br/>Enforce + quarterly<br/>evidence pack]
    D -.refresh every 90 days.-> B
    style A fill:#003366,color:#fff
    style B fill:#1BA0D7,color:#fff
    style C fill:#C55A11,color:#fff
    style D fill:#107C41,color:#fff
```

Each phase produces a specific, exportable artifact. The **[Reference Design](CSW-PCI-DSS-Reference-Design.md)** maps every artifact to a PCI requirement.

---

## Reference architecture at a glance

```mermaid
flowchart TB
    subgraph CDE["CDE — strictest controls"]
        PAN[PAN Storage<br/>DB]
        PROC[Payment Processing]
        GW[Payment Gateways]
        HSM[HSM Servers]
    end
    subgraph CONN["CDE-Connected"]
        WEB[Web / payment pages]
        AUTH[Auth servers]
        LOG[Logging infra]
    end
    subgraph OOS["Out-of-Scope — proven isolated"]
        CORP[Corporate systems]
    end

    WEB -->|443 only| PROC
    PROC -->|encrypted DB| PAN
    AUTH -->|LDAPS 636| CDE
    CDE -. default-deny .- CORP

    CDE --> EV[(CSW evidence pipeline<br/>flows · process · vulns · policy · audit)]
    CONN --> EV
    EV --> SIEM[SIEM / long-term retention]
```

`default-deny` between CDE and out-of-scope is what lets you *prove* scope reduction to a QSA — not a claim, a logged, enforced fact.

---

## Coverage snapshot

CSW produces **direct** evidence for the workload-resident slice of PCI and **supporting** inputs elsewhere. It never replaces your QSA's judgement.

| PCI requirement area | CSW coverage | Primary CSW evidence |
|---|:--:|---|
| Req 1 — Network security controls / segmentation | 🟢 Direct | ADM flow map, enforced policy, denied connections |
| Req 6 — Vulnerability management | 🟢 Direct | CVE + reachability report, CVSS-ranked |
| Req 7 — Access control (workload tier) | 🟢 Direct | Scope-based allowlist, process audit |
| Req 10 — Logging & monitoring | 🟢 Direct | Flow + process telemetry, policy-violation log |
| Req 11 — Security testing | 🟠 Supporting | ADM baseline-deviation, pre/post-pentest diff |
| Req 2 — Secure configuration | 🟠 Supporting | Process/vuln signals feed hardening evidence |
| Reqs 3/4/8/9/12 (crypto, physical, policy, HR) | ⚪ Evidence Required | Supplied **outside CSW** — key mgmt / physical / HR / ASV scans |

**Coverage key**

- 🟢 **Direct** — CSW produces the **primary evidence** artifact for the requirement.
- 🟠 **Supporting** — CSW produces an **input that feeds or complements** another control's evidence.
- ⚪ **Evidence Required** *(supplied outside CSW)* — CSW produces **nothing** here. The requirement is **in scope for compliance but out of scope for CSW**; the customer supplies the evidence through **another control, tool, or process** (e.g. key management/HSM, physical access logs, HR/training records, signed vendor contracts, ASV scans). This marks a **boundary, not a gap or a failure.**

> Coverage describes what evidence CSW produces — **not** that a control is passed, and ⚪ never means a control is unsupported.

---

## The Compliance Report — what your assessor gets

The snapshot above is the teaser. The **[Compliance Report](CSW-PCI-DSS-Compliance-Report.pdf)** is the artifact you actually hand to a QSA — a control-by-control mapping that turns "we use Cisco Secure Workload" into a defensible, color-coded evidence story.

[![PCI DSS v4.0 Compliance Report preview — color-coded control mapping](assets/compliance-report-preview.png)](CSW-PCI-DSS-Compliance-Report.pdf)

*Every PCI requirement, the matching CSW implementation, and a color-coded coverage verdict — green (Direct), amber (Supporting), grey (Evidence Required — supplied outside CSW).* **[Open the full report →](CSW-PCI-DSS-Compliance-Report.pdf)**

### Why an assessor values it

- **Speaks the assessor's language.** Rows are keyed to **Req / Sub-Req** (1.2.1, 6.3.3, 10.2.1, 11.4.1, 12.3.2…) so a QSA can line it up against their RoC work-papers without translation.
- **One-glance coverage verdict.** The color-coded **Coverage** column shows instantly where CSW is the *primary* evidence source vs. a *supporting* input vs. where **other controls must supply the evidence** — no digging.
- **Names the exact artifact and where it lives.** The **QSA Evidence Package** table maps each requirement to a specific CSW export (e.g. *Investigate → Flow Search*, *Defend → Policy Workspaces*) and its collection cadence — so the assessor knows precisely what to request and can reproduce it.
- **Shows isolation as a fact, not a claim.** The CDE scope/segmentation view is backed by enforced default-deny policy and logged denied connections — evidence that the control *operates*, which v4.0's "in place and operating effectively" language demands.
- **It's honest — and that builds trust.** The report openly flags what CSW does **not** cover (crypto/key management, physical, HR, ASV scans). Assessors trust a vendor mapping far more when it marks its own boundaries instead of claiming everything.
- **Continuous, not a once-a-year snapshot.** Because every row points at a live, re-exportable CSW artifact, the same report regenerates each quarter — replacing stale annual Visio diagrams and firewall samples.

> It is **evidence**, not an attestation. The QSA still determines compliance status — this report just makes their job faster and your position defensible.

---

## Start here

1. Read the **[Reference Design](CSW-PCI-DSS-Reference-Design.md)** — Sections 1–2 (architecture + the 6-step build).
2. Confirm your **CDE scope** with your compliance team and QSA.
3. Run the **[POV plan](docs/pov-plan.md)** on one CDE boundary.
4. Track exports with the **[Evidence Checklist](docs/evidence-checklist.md)**.
5. Share the **[Compliance Report](CSW-PCI-DSS-Compliance-Report.pdf)** with your assessor.

---

## Disclaimer

This repository is for informational and planning purposes. It is **not** legal, regulatory, audit, or certification advice, and it is **not** a PCI attestation. Validate all requirement references against the current official [PCI DSS v4.0](https://www.pcisecuritystandards.org/) text, your environment, and your QSA. Replace any bracketed fields before customer delivery.

*Part of the Cisco Secure Workload compliance reference-design series. Umbrella index: [CSW-Compliance-Mapping](https://github.com/chandrapati/CSW-Compliance-Mapping).*
