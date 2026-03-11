# System Architecture: Fraud-Ready Payments ETL

This document outlines the high-level architecture of the **de-lab-001-pandas-postgres-etl** repository.

> [!IMPORTANT]
> Our guiding philosophy is **Container-First Parity**. By enforcing runtime environments strictly within Docker Compose, a developer's local laptop behaves exactly identically to our production servers and our CI testing suites.

---

## 1. Core Platform Components

### Transient ETL Runner (`etl`)
- **What it is**: A temporary Docker container modeled as an ephemeral batch task.
- **How it works**: It is invoked on-demand using `docker compose run --rm etl`.
- **Why we do this**: **Stateless design**. By destroying the container after execution, we guarantee the environment is sterile for the next run.

### Persistent Postgres Warehouse (`pde_postgres_15`)
- **What it is**: The local simulated Data Warehouse.
- **How it works**: Bound via Docker's internal networking mechanism. It persists data to a Docker Volume (`postgres_data`).
- **Why we do this**: Provides an enterprise-accurate relational target without costing money on a live cloud SQL instance.

### Interactive JupyterLab (`pde_jupyter_lab`)
- **What it is**: The Data Engineering exploration workspace.
- **How it works**: Bound to `127.0.0.1:8888`. It bind-mounts the local `notebooks/` and `src/` directories.
- **Why we do this**: Allows engineers to profile chaotic inbound feeds safely before cementing the logic into the strict ETL runner.

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
