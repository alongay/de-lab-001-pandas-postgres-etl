# System Architecture: Fraud-Ready Payments ETL

This document outlines the high-level architecture of the **de-lab-001-pandas-postgres-etl** repository.

> [!IMPORTANT]
> Our guiding philosophy is **Container-First Parity**. By enforcing runtime environments strictly within Docker Compose, a developer's local laptop behaves exactly identically to our production servers and our CI testing suites.

---

## 1. Core Platform Components

### Isolated Domain Stacks (Disposable)
- **What they are**: Domain-specific Docker Compose files (e.g., `docker-compose.payments.yml`) that encapsulate the entire environment for a single demo.
- **How they work**: Invoked via `.\task.ps1 demo-<domain>`.
- **Why we do this**: **Infrastructure Symmetrization**. Each domain (Payments, IoT, HR) owns its own persistence layer and networking, preventing port collisions and cross-domain pollution.

### Core Lab Stack (Persistent)
- **What it is**: The `docker-compose.yml` file providing shared development services.
- **Components**: `pde_postgres_15` (Shared SQL playground) and `pde_jupyter_lab` (Exploration UI).
- **Service Binding**: Jupyter is bound to `127.0.0.1:8888` and bind-mounts the local `notebooks/` and `src/` directories.
- **Why we do this**: Allows engineers to profile chaotic inbound feeds safely before cementing the logic into the strict ETL runners.

---

## 2. Security & Network Isolation

- **Internal Routing**: The ETL container talks to the database using the Docker internal DNS name `postgres`.
- **Localhost Hardening**: Postgres and Jupyter ports are strictly bound to `127.0.0.1`.
- **No Hardcoded Credentials**: Connection tokens reside solely in the `.env` file.

---

## 3. The Functional Data Flow

When executing the pipeline, data flows linearly through decoupled modules:

1. **Extract**: Reaches out to the configured `INGEST_SOURCE` (Mock HTTP or Raw CSV).
2. **Transform**: Implements static typing, numeric precision with **decimal.Decimal**, and record hashing.
3. **Quality Gate**: Engages **Great Expectations**. If ANY payload violates strict logic, the pipeline crashes non-zero to protect the Warehouse.
4. **Load**: Uses an aggressive **Staging-First UPSERT** pattern. This implicitly guarantees **idempotency**.
