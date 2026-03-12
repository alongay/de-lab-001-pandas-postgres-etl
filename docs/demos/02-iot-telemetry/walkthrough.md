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

### 🛠️ Demo: The Chaos Run
This section proves the platform's **Data Guard** capabilities by simulating sensor malfunction.

1.  **Inject Chaos**: Run the integrated demo command: `.\task.ps1 demo-iot`.
2.  **Observe Failure**: The pipeline detects "out of bounds" temperature readings (e.g., 500°C) during the **Great Expectations** audit.
3.  **Automated Divergence**: Instead of crashing the whole pipeline, the script routes only the corrupted batch to the `iot_sensor_quarantine` table.
4.  **Verification**: Querying the database shows the main tables remain clean while the quarantine table contains the evidence of the chaos.

> [!CAUTION]
> **Interview Point**: "This is the **Physical Gate** pattern. By isolating anomalies at the batch level into a quarantine partition, we maintain a 'High-Trust' production lake while still preserving the 'Bad' data for forensic analysis by hardware teams."

---

## 🔒 Security & Cost Model
- **Security**: Strict table isolation (**Clean vs. Quarantine**) and least-privilege DB access.
- **Cost**: **$0** (Runs entirely on local Docker/WSL2).
