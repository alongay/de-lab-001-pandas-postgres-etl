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

### Verification: Sovereignty Gate
Postgres Audit (`hr_applicants_quarantine`):
| full_name | email | failure_reason |
|-----------|-------|----------------|
| John Doe  | [REDACTED] | FAILURE_ISO_SOVEREIGNTY |

---
Demo 3: HR Privacy & Compliance Lab is **Verified**.
