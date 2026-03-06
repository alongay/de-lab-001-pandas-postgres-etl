# System Architecture: Fraud-Ready Payments ETL

This document outlines the high-level architecture of the `de-lab-001-pandas-postgres-etl` repository. 

Our guiding philosophy is **Container-First Parity**. By enforcing runtime environments strictly within Docker Compose, a developer's local laptopbehaves exactly identically to our production servers and our CI testing suites.

---

## 1. Core Platform Components

### Transient ETL Runner (`etl`)
*   **What it is:** A temporary Docker container modeled as an ephemeral batch task.
*   **How it works:** It is invoked on-demand using `docker compose run --rm etl`. It spins up, reads environment config, executes the ingestion logic (`src/etl_run.py`), and then instantly terminates.
*   **Why we do this:** Stateless design. By destroying the container after execution, we absolutely guarantee the environment is sterile for the next run. There are no dangling files or memory leaks.

### Persistent Postgres Warehouse (`pde_postgres_15`)
*   **What it is:** The local simulated Data Warehouse.
*   **How it works:** Bound primarily via Docker's internal networking mechanism. It persists data to a Docker Volume (`postgres_data`) on the host disk so the database survives reboots.
*   **Why we do this:** Provides an enterprise-accurate relational target for our staged UPSERT logic testing without costing money on a live cloud SQL instance overhead.

### Interactive JupyterLab (`pde_jupyter_lab`)
*   **What it is:** The Data Engineering exploration workspace.
*   **How it works:** Bound to `127.0.0.1:8888`. It bind-mounts the local `notebooks/` and `src/` directories, meaning any Python modules updated locally instantly reflect in the interactive notebooks.
*   **Why we do this:** Allows engineers to profile chaotic inbound Partner API feeds safely before cementing the logic into the strict ETL runner.

---

## 2. Security & Network Isolation

*   **Internal Routing:** The ETL container talks to the database using the Docker internal DNS name `postgres`. It does not route out to the internet or bounce back through `localhost`, significantly increasing security.
*   **Localhost Hardening:** Postgres port `5432` and Jupyter port `8888` are strictly bound to `127.0.0.1` (localhost). No one else on your local WiFi or corporate LAN can access your lab.
*   **No Hardcoded Credentials:** The connection string logic inherently assumes credentials reside in `.env`.

---

## 3. The Functional Data Flow

When executing the pipeline, data flows linearly through cleanly decoupled modules:

1.  **Extract (`src/extract_partner_api.py` & `src/extract_partner_csv.py`):** Reaches out to the configured `INGEST_SOURCE` (fetching the mock HTTP endpoint or reading the raw CSV file from disk).
2.  **Transform (`src/transform_payments.py`):** Implements static typing. Upgrades floats to strict `decimal.Decimal` objects, normalizes currency cases, and calculates a deterministic MD5 `record_hash`.
3.  **Quality Gate (`src/quality_ge_payments.py`):** Engages Great Expectations. If ANY payload violates strict logic (e.g., negative balances, broken schemas, illegal statuses like "PENDING"), the entire pipeline crashes non-zero, generating an Audit Artifact in `logs/` and explicitly halting the script to protect Postgres from corrupted data.
4.  **Load (`src/load_payments.py`):** Uses an aggressive Staging-First UPSERT pattern. It writes to a temporary `raw_payments_stg` table, then executes a native PostgreSQL `INSERT ... ON CONFLICT (partner_id, txn_id) DO UPDATE` query to merge state completely atomically into `raw_payments`. This implicitly guarantees idempotency.
