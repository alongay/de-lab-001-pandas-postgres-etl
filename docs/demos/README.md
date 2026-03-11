# Curriculum: Educational Demo Projects

This curriculum is designed to teach **enterprise-grade Data Engineering** by solving three distinct business problems using a unified architectural pattern.

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

### [**Demo 3: Streaming Event Platform**](03-streaming-platform/README.md) (**✅ Implemented**)
**The Pitch**: Handling **"Real-Time Velocity"** and stateful processing.
- **Challenge**: **Kafka-to-Spark** ingestion with real-time **Delta Lake** storage.
- **Logic**: Implements a **Medallion Architecture** (Bronze/Silver) with inline anomaly detection.
- **Chaos**: High-frequency outlier injection to prove real-time **Quarantine** logic.

### [**Demo 4: HR Applicant Intake**](03-hr-applicants/README.md) (**📅 Future**)
**The Pitch**: Handling **"Privacy"** and regulatory compliance.
- **Challenge**: **PII scrubbing** and data sovereignty.
- **Logic**: Enforces strict regex validation and redacts sensitive data.
- **Chaos**: Injects non-compliant jurisdiction data to prove the sovereignty gate.

---

## 🎓 The Standard Teaching Flow
Every demo in this curriculum follows the same **production-hardened lifecycle**:

- **Prepare Payload**: Generate synthetic partner data using reusable scripts.
- **Profile**: Interactively explore the unknown raw data in a **Jupyter Notebook**.
- **Execute**: Run the containerized ETL pipeline and verify successful ingestion.
- **Chaos Injection**: Intentionally corrupt the source data to trigger a **Quality Gate failure**.
- **Verify**: Identify the failure in the **GE logs**, recover the data, and run CI unit tests.
