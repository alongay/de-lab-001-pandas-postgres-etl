# 🏙️ Global Platform Architecture

This document outlines the high-level architecture of the **Enterprise Data Engineering Demo Platform**.

> [!IMPORTANT]
> Our guiding philosophy is **Idempotent Hybrid Orchestration**. By blending isolated domain-specific containers with a centralized Airflow control plane, we achieve a balance of **development speed** and **production-grade resilience**.

---

## 1. Multi-Domain Persistence Layers

The platform implements a **Domain-Oriented Metadata Architecture**:

### 💳 Finance (Payments)
- **Engine**: PostgreSQL
- **Pattern**: Happy Path / Chaos Injection / Quarantine.
- **Goal**: High-integrity validation with **Great Expectations**.

### ⚕️ HR (Talent Compliance)
- **Engine**: PostgreSQL (Isolated Container)
- **Pattern**: PII Redaction & Audit Trail.
- **Goal**: Demonstrating data sovereignty and regulatory compliance (GDPR/SOC2 style).

### 🛰️ IoT (Streaming Telemetry)
- **Engine**: **Delta Lake** (Medallion: Bronze -> Silver)
- **Pattern**: Spark Structured Streaming + Kafka.
- **Goal**: Real-time anomaly routing and high-velocity storage.

---

## 2. Programmable Visibility Layer (BI-as-Code)

We treat Business Intelligence as a **First-Class Engineering Asset**:
- **Engine**: Metabase
- **GitOps Integration**: Dashboards are version-controlled via a custom **Python CLI Wrapper** over the Metabase API.
- **Zero-Manual-Setup**: Configurations are synchronized to ensure environment parity (Local vs Staging).

---

## 3. The Functional Data Flow (Senior Guardrails)

All data moving through the platform must pass through the **Senior Reliability Filter**:

1.  **Extract**: Source-agnostic connectors (Kafka, Mock HTTP, CSV, Parquet).
2.  **Transform**: Explicit schema enforcement and deterministic hashing.
3.  **Governance Gate**:
    - **Physical Rules**: Catching 500°C temperatures (Physics Quality Gates).
    - **Logic Rules**: Catching negative payment amounts.
4.  **Anomaly Routing**: Data that fails the gate is never lost; it is routed to a **Quarantine Delta Table** or Postgres Schema for later auditing.
5.  **Idempotent Load**: All write operations use **UPSERT** or **OVERWRITE** patterns to ensure the pipeline is safe to re-run after failure.

---

## 🛡️ Zero-Trust Security Posture

- **Shift-Left Security**: Secret scanning integrated into the `platform-up` command.
- **Image Hardening**: Automated CVE scanning for all Docker images.
- **Network Isolation**: All services communicate via internal Docker bridge networks with strictly mapped exports.

---

**Status: ARCHITECTURE CERTIFIED** 🚀🏙️💎🏁
