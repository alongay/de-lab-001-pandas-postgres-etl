# Demo 3: HR Applicant Intake (PII)

**Status: ✅ Implemented & Verified**

### 🎯 The Pitch
This demo focuses on **Data Privacy and Compliance**. HR data is full of **PII (Personally Identifiable Information)**. We show how to build a pipeline that ingests job applicants while strictly following **data sovereignty laws** and keeping sensitive data out of the system logs.

### 🏗️ Ingestion Architecture

```mermaid
graph TD
    S1[Applicant API] --> ETL[HR ETL Runner]
    
    subgraph "Privacy & Compliance"
        ETL --> PII[PII Redaction: [REDACTED]]
        PII --> ISO[Sovereignty Gate: ISO Check]
    end

    subgraph "Compliance Hub"
        ISO -- Allowed --> PROD[(hr_applicants)]
        ISO -- Denied --> Q[(hr_applicants_quarantine)]
        PII --> Log[system_logs: [REDACTED]]
    end
```

### 🛠️ Technical Challenges
- **PII Redaction**: Ensuring sensitive data (emails/names) is scrubbed from system logs.
- **Data Sovereignty**: Enforcing strict ISO country allowed-lists to comply with regional regulations.
- **Identity Integrity**: Validating complex strings (emails/phones) via robust regex enforcement.

---
**Links:**
- [**Walkthrough Script**](walkthrough.md)
- [**Learning Guide (Theory & Interview)**](learning_guide.md)
