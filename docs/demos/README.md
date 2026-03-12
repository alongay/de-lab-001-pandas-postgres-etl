# Curriculum: Educational Demo Projects

This curriculum is designed to teach **enterprise-grade Data Engineering** by solving five distinct business problems using a unified architectural pattern.

---

## 🏗️ Demo Projects Overview

### [**Demo 1: Fraud-Ready Payments Intake**](01-fraud-payments/README.md) (**✅ Implemented**)
**The Pitch**: Handling **"Money"** with zero-tolerance for corruption.
- **Challenge**: Precise numeric casting and multi-source conflict resolution.
- **Logic**: Ingests API (JSON) and Batch (CSV) telemetry; enforces **"CSV Wins"** on conflict.
- **Chaos**: Intentionally corrupts transaction amounts to trigger pipeline failure.

### [**Demo 2: IoT Sensor Telemetry**](02-iot-telemetry/README.md) (**✅ Implemented**)
**The Pitch**: Handling **"Physical Reality"** and high-volume noise.
- **Challenge**: Outlier detection and physical bounds-checking with **Table Partitioning**.
- **Logic**: Time-series deduplication across `(device_id, reading_ts, metric)`.
- **Chaos**: Injects **"hardware drift"** signals to prove the quality gate blocks ghost data.

### [**Demo 3: HR Applicant Intake**](03-hr-applicants/walkthrough.md) (**✅ Implemented**)
**The Pitch**: Handling **"Privacy"** and regulatory compliance.
- **Challenge**: **PII scrubbing** and data sovereignty.
- **Logic**: Enforces strict regex validation, redacts sensitive data (Email/Name), and checks ISO country allowed-lists.
- **Chaos**: Injects non-compliant jurisdiction data to prove the sovereignty gate blocks entries.

### [**Demo 4: Enterprise Orchestration**](04-orchestration/walkthrough.md) (**✅ Implemented**)
**The Pitch**: Handling **"Operations"** and platform governance.
- **Challenge**: Pipeline scheduling, alerting, and SLA monitoring via **Apache Airflow**.
- **Logic**: Specialized DAGs for Batch, Streaming Health, and Quality Audits.
- **Chaos**: Simulates Kafka heart-beat loss and Delta log staleness.

### [**Demo 5: Streaming Event Platform**](03-streaming-platform/walkthrough.md) (**✅ Implemented**)
**The Pitch**: Handling **"Real-Time Velocity"** and stateful processing.
- **Challenge**: **Kafka-to-Spark** ingestion with real-time **Delta Lake** storage.
- **Logic**: Implements a **Medallion Architecture** (Bronze/Silver) with inline anomaly detection.
- **Chaos**: High-frequency outlier injection to prove real-time **Quarantine** logic.

---

## 🏗️ Infrastructure Isolation (Symmetrization Standard)
To align with enterprise best practices, every demo operates on its own isolated infrastructure stack. This prevents port collisions and ensures clean persistence boundaries:

| Demo | Domain | Compose File | DB Port | Network |
| :--- | :--- | :--- | :--- | :--- |
| **Demo 1** | Payments | `docker-compose.payments.yml` | `5433` | `pde_payments_net` |
| **Demo 2** | IoT Batch | `docker-compose.iot.yml` | `5434` | `pde_iot_net` |
| **Demo 3** | HR / PII | `docker-compose.hr.yml` | `5435` | `pde_hr_net` |
| **Demo 4** | Airflow | `docker-compose.orchestration.yml` | `5432` | `pde_platform_net` |
| **Demo 5** | Streaming | `docker-compose.streaming.yml` | N/A | `pde_streaming_net` |

---

## 🎓 The Standard Teaching Flow
Every demo in this curriculum follows the same **production-hardened lifecycle**:

- **Prepare Payload**: Generate synthetic partner data using reusable modular scripts in `scripts/`.
- **Profile**: Interactively explore the unknown raw data in a domain-specific **Jupyter Notebook**.
- **Execute**: Run the containerized ETL pipeline and verify successful ingestion / transformation.
- **Chaos Injection**: Intentionally corrupt the source data to trigger a **Quality Gate failure**.
- **Verify**: Identify the failure in the **Audit logs**, recover the data, and run CI unit tests.
