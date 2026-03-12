# Walkthrough: Demo 3 — HR Applicant Intake (PII & Compliance)

## 🎯 Objective
This demo demonstrates **Data Privacy and Compliance** within a production-ready data platform. It focuses on:
1. **PII Redaction**: Ensuring sensitive data (emails/names) is scrubbed from system logs.
2. **Data Sovereignty**: Enforcing strict ISO country allowed-lists to comply with regional regulations.
3. **Identity Integrity**: Validating complex strings (emails/phones) via robust regex enforcement.

## 🛠️ Implementation Highlights

### 1. Isolated Infrastructure
- **Isolated Compose**: Uses `docker-compose.hr.yml` to prevent project naming collisions and ensure a clean environment.
- **Dedicated Database**: Ingests into `hr_applicants` and `hr_applicants_quarantine`.

### 2. Privacy Controls
- **Transform Logic**: `src/hr/transform_hr.py` includes a `redact_pii` utility that scrubs sensitive fields before any logging occurs.
- **Audit Logs**: Verified via `logs/etl.log`.

### 3. Compliance Gates
- **Sovereignty Rules**: Applicant data from non-ISO allowed countries is automatically routed to a `quarantine` table with a `FAILURE_ISO_SOVEREIGNTY` reason.

## 🧪 Proof of Life

### HR ETL Execution
When running `.\task.ps1 demo-hr`, the following steps are executed:
1. **Start Isolation**: Spin up `pde_hr_postgres` and `pde_hr_etl_runner`.
2. **Data Generation**: Generate payloads with PII and compliant/non-compliant country codes.
3. **Compliance Audit**:
    - **Valid**: Loaded into `hr_applicants`.
    - **Quarantined**: Loaded into `hr_applicants_quarantine` (e.g., if country is 'XY' or email is invalid).

### Verification: PII Redaction
Audit log Check (`logs/etl.log`):
```text
2026-03-12 ... - INFO - Starting HR Transformation...
2026-03-12 ... - INFO - Processing applicant data. Sample email: [REDACTED]
```

### 🛠️ Demo: The Chaos Run
This section proves the platform's **Privacy Compliance** by simulating an intake of non-compliant data.

1.  **Inject Chaos**: Run the integrated demo command: `.\task.ps1 demo-hr`.
2.  **Observe Compliance Logic**: The system detects an applicant from a country not on the approved ISO list (e.g., 'XY').
3.  **PII Sanitization**: Simultaneously, the system scrubs the `email` and `full_name` from all logs to ensure no PII is leaked in plain text.
4.  **Verification**: 
    *   `hr_applicants` (Clean table) will NOT contain the non-compliant record.
    *   `hr_applicants_quarantine` will contain the record, marked with `FAILURE_ISO_SOVEREIGNTY`.
    *   System logs (`logs/etl.log`) will show `[REDACTED]` instead of real names.

> [!CAUTION]
> **Interview Point**: "This demo proves **Data Sovereignty by Design**. By routing non-compliant data to a dedicated quarantine store and redacting PII from logs at the ingestion boundary, we ensure the platform remains GDPR/CCPA ready without manual oversight."

---
Demo 3: HR Privacy & Compliance Lab is **Verified**.
