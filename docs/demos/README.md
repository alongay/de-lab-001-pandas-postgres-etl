# Curriculum: Educational Demo Projects

This curriculum is designed to teach enterprise-grade Data Engineering by solving three distinct business problems using a unified architectural pattern (Docker + Postgres + Python + Great Expectations).

---

## 🏗️ Demo Projects Overview

### [Demo 1: Fraud-Ready Payments Intake](01-fraud-payments/README.md) (✅ Implemented)
**The Pitch**: Handling "Money" with zero-tolerance for corruption.
- **Challenge**: Precise numeric casting and multi-source conflict resolution.
- **Logic**: Ingests API (JSON) and Batch (CSV) telemetry; enforces "CSV Wins" on conflict.
- **Chaos**: Intentionally corrupts transaction amounts to trigger pipeline failure.

### [Demo 2: IoT Sensor Telemetry](02-iot-telemetry/README.md) (⏳ Next Phase)
**The Pitch**: Handling "Physical Reality" and high-volume noise.
- **Challenge**: Outlier detection and physical bounds-checking (e.g. 150% humidity).
- **Logic**: Time-series deduplication across `(device_id, reading_ts, metric)`.
- **Chaos**: Injects "hardware drift" signals to prove the quality gate blocks ghost data.

### [Demo 3: HR Applicant Intake](03-hr-applicants/README.md) (📅 Future)
**The Pitch**: Handling "Privacy" and regulatory compliance.
- **Challenge**: PII scrubbing (emails/phones) and data sovereignty (ISO country lists).
- **Logic**: Enforces strict regex validation and redacts sensitive data from console logs.
- **Chaos**: Injects non-compliant jurisdiction data to prove the sovereignty gate works.

---

## 🎓 The Standard Teaching Flow
Every demo in this curriculum follows the same production-hardened lifecycle:

1.  **Prepare Payload**: Generate synthetic partner data using reusable scripts.
2.  **Profile**: Interactively explore the unknown raw data in a Jupyter Notebook.
3.  **Execute**: Run the containerized ETL pipeline and verify successful ingestion.
4.  **Chaos Injection**: Intentionally corrupt the source data to trigger a Quality Gate failure (non-zero exit).
5.  **Verify**: Identify the failure in the GE logs, recover the data, and run CI unit tests.
