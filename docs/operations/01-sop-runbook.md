# SOP / Runbook: Unified Data Engineering Lab

> [!NOTE]
> Welcome to the **Data Engineering ETL Pipeline**! This runbook is written to onboard you into our **container-first** environment. Our goal is to run enterprise-grade data engineering patterns directly on your local machine.

---

## 1. Secure Configuration (`.env`)
**What:** Duplicating the configuration template and assigning real, secure credentials.
**Why:** Enterprise environments strictly isolate secrets. The `.env` file is heavily **ignored** to prevent credential leaks.

- **Copy the template**:
  - **PowerShell**: `Copy-Item .env.example .env`
  - **Bash**: `cp .env.example .env`
- **Edit `.env` and configure**:
  - `POSTGRES_USER` & `POSTGRES_PASSWORD`
  - `JUPYTER_TOKEN` (Create a random secure phrase)
  - `INGEST_SOURCE` (Select `api`, `csv`, or `both`)

---

## 2. Start Central Lab (Development)
**What:** Booting up the core PostgreSQL and JupyterLab as persistent development services.

**PowerShell**:
```powershell
.\task.ps1 up
```

**Verify Health**:
Run `.\task.ps1 ps`. Expect `pde_postgres_15` to be **(healthy)** and `pde_jupyter_lab` to be **Up**.

---

## 3. Data Profiling (Jupyter)
**What:** Accessing the interactive data exploration UI.

- Open: `http://127.0.0.1:8888`
- Enter your **Jupyter Token**.

> [!TIP]
> If you forgot your token, run:
> `docker exec -it pde_jupyter_lab jupyter server list`

---

## 4. Run the ETL Pipeline (One-Command)
**What:** Executing a domain-specific ingestion script in an isolated environment.

**PowerShell**:
```powershell
.\task.ps1 demo-payments    # For Financial Demo
.\task.ps1 demo-iot         # For IoT Batch Demo
.\task.ps1 demo-hr          # For HR Compliance Demo
```

**Expected Output**:
Chronological logs confirming **Extraction** -> **Standardization** -> **Quality Gates** -> **Load**.
Should end with: `ETL pipeline finished successfully` (**Exit Code 0**).

---

## 5. IoT Operations (Time-Series)
**What:** Managing high-volume telemetry and physical partitions.

- **Deduplication**: The IoT pipeline uses a strict `(device_id, reading_ts, metric)` key to prevent double-counting.
- **Table Partitioning**: Data is automatically routed to child tables (e.g., `raw_sensor_readings_y2026`).
- **Verifying Partitions**:
  ```sql
  SELECT relname FROM pg_stat_user_tables WHERE relname LIKE 'raw_sensor_readings_y%';
  ```

---

## 6. Streaming Event Platform
**What:** Operating the **Kafka-Spark** real-time pipeline.

> [!NOTE]
> **Infrastructure Note**: We use the `bitnamilegacy/` repository for Kafka and Spark to ensure specific version compatibility. Do not revert to `bitnami/` unless migrating to the latest "rolling" tags.

- **Start Infrastructure**: `docker compose -f docker-compose.yml -f docker-compose.streaming.yml up -d iot-kafka iot-spark-master iot-spark-worker`
- **Launch Jobs & Producer**: `docker compose -f docker-compose.yml -f docker-compose.streaming.yml up -d iot-stream-producer iot-bronze-stream iot-silver-stream`
- **Data Lake (Medallion)**:
  - **Bronze**: `/app/data/delta/bronze` (Raw events)
  - **Silver**: `/app/data/delta/silver` (Cleaned readings)
  - **Quarantine**: `/app/data/delta/quarantine` (Physical outliers)

---

## 7. Teardown & Maintenance
**What:** Shutting down services to free up local resources.

**PowerShell**:
```powershell
.\task.ps1 down
```

> [!WARNING]
> To completely wipe the database and start fresh (destructive):
> `docker compose down -v`
