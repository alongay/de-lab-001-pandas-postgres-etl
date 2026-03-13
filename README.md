# 🏗️ Enterprise Data Engineering & Observability Platform
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Stack: Medallion](https://img.shields.io/badge/Architecture-Medallion-orange.svg)](#-architectural-pillars)
[![Security: Zero--Trust](https://img.shields.io/badge/Security-Zero--Trust-green.svg)](#-hardened-security-posture)
[![Ops: Idempotent](https://img.shields.io/badge/Ops-Idempotent-brightgreen.svg)](#-operational-rigor)

A production-grade data engineering repository showcasing the **senior-level orchestration** of multi-domain data pipelines. This platform demonstrates the transition from simple ETL to a **hardened, observable, and programmable data ecosystem.**

---

## 🏛️ Architectural Pillars

This platform is built on four non-negotiable engineering principles:

1.  **Medallion Architecture (Bronze/Silver/Delta)**: Structured data lifecycle ensuring 100% auditability and 100% downstream quality.
2.  **Programmable Visibility (BI-as-Code)**: Treating dashboards as version-controlled assets, synchronized via custom Python wrappers over the Metabase API.
3.  **Zero-Trust Security**: Automated pre-flight secret scrubbing and bi-weekly container vulnerability (CVE) orchestration.
4.  **Idempotent Operations**: A centralized PowerShell control plane (`task.ps1`) ensuring deterministic environment state across local and cloud environments.

---

## 🎡 The Platform Experience

The platform is organized into three distinct "Worlds" (Domains) overseen by a unified control plane:

- **💳 Finance (Payments)**: High-integrity batch ETL with strict **Great Expectations** fraud-style validation gates.
- **🏥 HR (Talent)**: Privacy-aware compliance pipelines demonstrating PII redaction and audit trails.
- **🛰️ IoT (Telemetry)**: High-velocity **Spark Structured Streaming** with Kafka ingestion and real-time anomaly routing.

---

## 🔭 The Executive Watchtower (BI-as-Code)
*Integrated Metabase Suite — Access at [http://localhost:3010](http://localhost:3010)*

| Dashboard | Domain | Purpose | Senior Proof Point |
| :--- | :--- | :--- | :--- |
| **Executive Watchtower** | Business | Global KPI visibility | Advanced SQL window functions for trend analysis. |
| **Talent Insights** | HR | Hiring funnel observability | Aggregated metrics over sensitive redacted data. |
| **IoT Pulse** | Telemetry | Real-time sensor health | Visualizing Spark streaming throughput and heat-maps. |
| **Data Quality Hub** | Ops | **The Data Police** | Real-time visualization of the `Quarantine` layer vs Production. |

---

## 🛡️ Hardened Security Posture

Data engineering doesn't stop at the code level. This platform implements:
- **Pre-Flight Secret Scanning**: Integrated into `platform-up` to ensure no credentials hit remote logs.
- **Vulnerability Scanning**: Automated scripts to audit Docker images for high-risk CVEs and privileged root execution.
- **Least-Privilege RBAC**: Isolated database users for each domain to prevent lateral data movement.

---

## 🛠️ Operational Rigor

The platform is managed via an **Idempotent Task Runner** (`task.ps1`). 

```powershell
# Bring up the entire hardened platform
./task.ps1 platform-up

# Clean environment to a deterministic state
./task.ps1 clean

# Run domain-specific demos with auditing enabled
./task.ps1 demo-payments
```

---

## 🧭 Onboarding & Mastery Guide

If you are a reviewer or a student, follow the [Hands-on Mastery Guide](docs/operations/hands-on-mastery-guide.md). It contains 8 curated labs designed to take you from environment basics to **Chaos Auditing** and **BI-as-Code Synchronization**.

---

## 📦 Repository Structure

```text
.
├── src/                    # Core logic (Domain-isolated ETL)
├── docs/                   # The "Library" (Demos, Architecture, Operations)
├── orchestration/          # The "Conductor" (Airflow DAGs)
├── scripts/                # The "Automation" (Security, Cleanup, Generation)
├── task.ps1                # The "Remote Control" (Idempotent Platform Runner)
└── docker-compose.yml      # The "Blueprint" (Service containerization)
```

---

## 💡 Interview War Stories
*Featured in [docs/my notes](docs/%22my%20notes%22)*
- **The "Invisible Data" Incident**: How GX Quarantine gates caught impossible 500°C IoT data.
- **The "Light Switch" Deployment**: Why Idempotency is the silent killer of production bugs.
- **The "Programmable Dashboard"**: Transitioning from Click-Ops to Git-Ops in BI.

---

**Status: PRODUCTION-READY** 🚀🏙️💎🏁👑
