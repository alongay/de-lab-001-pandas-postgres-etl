# 🎓 Hands-on Mastery Guide: Data Engineering Platform

Welcome to the PDE (Production Data Engineering) Mastery Guide. This document is a structured, progressive learning path designed to move you from **"I can run a script"** to **"I can design resilient, production-ready data systems."**

---

## 🛠️ Prerequisites
- **Git** installed.
- **Docker Desktop** running.
- **PowerShell** (for the `task.ps1` runner).
- **Python 3.10+** (local env recommended for notebooks).

---

## 🧪 Lab 1: Platform Command & Control
**Objective**: Master the task runner and environment state.

### Steps:
1.  **Initialize Environment**:
    ```powershell
    Copy-Item .env.example .env
    .\task.ps1 platform-init
    ```
2.  **Verify Orchestration**:
    ```powershell
    .\task.ps1 platform-up
    .\task.ps1 platform-status
    ```
3.  **The "Global Smoke"**: Run a quick verification of the core ETL container.
    ```powershell
    .\task.ps1 smoke
    ```

**Learning Point**: In production, we don't `docker-compose up` manually every time. We use orchestration wrappers (`task.ps1`) to ensure consistency.

---

## 💰 Lab 2: "Zero-Tolerance" Payments ETL
**Objective**: Learn Quality Gates with **Great Expectations**.

### The Challenge:
Ingest payment data from two sources (API & CSV). The business rules demand precise amounts and "CSV Wins" on duplicate ID conflicts.

### Steps:
1.  **Run the automated lab**:
    ```powershell
    .\task.ps1 demo-payments
    ```
2.  **Analyze the Chaos**:
    - During the run, watch for "Expected Failure".
    - Open `artifacts/latest_chaos_failure.json`.
    - Observe how the pipeline detected a negative amount (`-75.50`) and halted.
3.  **Manual Recovery**: 
    - Fix the data in `data/payments/transactions_daily.csv`.
    - Re-run just the ETL part: `.\task.ps1 etl` with `env:DOMAIN="payments"`.

**Learning Point**: ETL isn't just about moving data; it's about **defending** the warehouse against corrupted payloads.

---

## 📡 Lab 3: Resilient IoT Partitioning
**Objective**: Master Table Partitioning and the **Quarantine Pattern**.

### The Challenge:
Handling high-volume sensor telemetry where incoming timestamps are noisy but physically bounded.

### Steps:
1.  **Execute the IoT Lab**:
    ```powershell
    .\task.ps1 demo-iot
    ```
2.  **Inspect the "Quarantine Zone"**:
    - Connect to the IoT Postgres (`Port 5434`).
    - Run: `SELECT * FROM raw_sensor_readings_quarantine;`
    - Why were these records rejected? (Hint: Check the `metric` bounds in the source).
3.  **Verify Partitioning**:
    - Notice that `raw_sensor_readings` is partitioned by year.
    - Check the system catalog to see the sub-tables created on the fly.

**Learning Point**: Scalability requires partitioning. Resilience requires a "safe place" (Quarantine) for rejected data to be audited without breaking the pipeline.

---

## 🌊 Lab 4: Real-time Medallion (Streaming)
**Objective**: Master **Kafka**, **Spark**, and **Delta Lake**.

### The Challenge:
Build a real-time anomaly detection engine using the industry-standard "Medallion Architecture" (Bronze -> Silver).

### Steps:
1.  **Spin up the Data Bus**:
    ```powershell
    .\task.ps1 demo-iot-stream
    ```
2.  **Follow the Stream**:
    - Observe data entering **Kafka** via the producer.
    - Watch **Spark** ingest it into the **Bronze Delta Table** (Raw).
    - Watch the second Spark job refine it into **Silver** (Cleaned).
3.  **Verify Immutability**:
    - Explore `data/streaming/delta/silver`.
    - Notice the `_delta_log` folder—this provides ACID transactions for our stream.

**Learning Point**: Streams are fast, but they must be consistent. Medallion architecture ensures every byte is traceable.

---

## 🏛️ Lab 5: Orchestration & SLA Governance
**Objective**: Master **Apache Airflow** as the Control Plane.

### Steps:
1.  **Launch Airflow**:
    ```powershell
    .\task.ps1 demo-orchestration
    ```
2.  **Navigate to `localhost:8088`** (admin/admin).
3.  **Trigger the `payments_main_v1` DAG**.
4.  **Simulate a Breach**: 
    - Manually stop the `iot-postgres` container.
    - Watch the Airflow sensor catch the failure and trigger a retry/alert.

**Learning Point**: Orchestration is the "brains" of the platform. It handles the "When", "Why", and "What if it fails?".

---

## 📈 Lab 6: Statistical Observability
**Objective**: Detect **Silent Data Drift** using metadata auditing.

### Steps:
1.  **Run the Audit Lab**:
    ```powershell
    .\task.ps1 demo-observability
    ```
2.  **Inspect the Audit Hub**:
    - The lab uses **DuckDB** to analyze trends in transformation logs.
    - Look for "Drift Detected!" in the output—this happens when the *distribution* of data changes, even if the individual records are "valid".

**Learning Point**: Quality Gates catch broken data. Observability catches **drifting** data.

---

## 🏆 Graduation Task
Create a new demo in `src/` and `scripts/` called `shipping/`. 
- Implement a basic ETL.
- Add a Great Expectations suite.
- Create a `shipping-postgres` service in a new `docker-compose.shipping.yml`.
- Add a `demo-shipping` command to `task.ps1`.

**If you can do this, you are a Platform Data Engineer.**
