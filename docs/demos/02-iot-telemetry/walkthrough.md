# IoT Telemetry Pipeline (Demo 2) - Walkthrough

This demo showcases a production-grade IoT data pipeline that prioritizes **Data Sovereignty**, **Physical Integrity**, and **Operational Resilience**.

## 🏗️ Architecture & Features

### 1. Ingestion & Standardization
- **Multi-Source**: Ingests from local CSVs and Mock APIs (JSON).
- **Contract Enforcement**: Standardizes sensors to **UTC timestamps** and ensures schema consistency.

### 2. High-Performance Storage (Senior DE Upgrade)
- **Declarative Partitioning**: `raw_sensor_readings` is partitioned by range on `reading_ts` (e.g., Monthly partitions).
- **Time-Series Indexing**: A composite index on `(device_id, reading_ts)` allows for **sub-second retrieval** of device history.

### 3. Physical Quality Gate (Great Expectations)
- **Laws of Physics**: Enforces realistic temperature (-40C to 85C) and humidity (0-100%).
- **Time-Series Integrity**: Ensures compound uniqueness for `(device_id, reading_ts, metric)`.

### 4. Batch Quarantine Pattern
- **Resilient Loading**: If a batch fails, it is routed to the **Quarantine Table**.
- **Auditability**: Validation reports are stored in `logs/` for every failure.

---

## ✅ Verification & Proof of Work

### Automated "One-Command" Demo
```powershell
.\task.ps1 demo-iot
```

> [!TIP]
> **Talk Track**: "This demo proves that our pipeline is **Physics-Aware**. We intentionally inject chaotic sensor data and watch the system automatically isolate it into a quarantine zone while keeping the clean production tables pristine."

### 📊 Proof Points:
- **Partition Verification**: We query `pg_stat_user_tables` to prove data landed in the **March 2026 partition**.
- **Quarantine Success**: The database confirms that 'Chaotic' records were diverted to the audit table.
- **Pytest Suite**: 100% pass rate for IoT data transformations and quality logic.

---

## 🔒 Security & Cost Model
- **Security**: Strict table isolation (**Clean vs. Quarantine**) and least-privilege DB access.
- **Cost**: **$0** (Runs entirely on local Docker/WSL2).
