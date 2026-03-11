# Demo 3: HR Applicant Intake (PII)

**Status: 📅 Future Extension**

### 🎯 The Pitch
This demo focuses on **Data Privacy and Compliance**. HR data is full of PII (Personally Identifiable Information). We show how to build a pipeline that ingests job applicants while strictly following data sovereignty laws and keeping sensitive data out of the system logs.

### 🛠️ Technical Challenges
*   **PII Redaction**: Implementing logic to ensure emails, names, and phone numbers are scrubbed from console logs and triage files.
*   **Data Sovereignty**: Enforcing strict ISO country allowed-lists to comply with regional data processing regulations.
*   **Identity Integrity**: Validating complex strings (phone numbers/emails) via robust regex enforcement before landing in the warehouse.

### 🎓 Teaching Flow
1.  **PII Payload**: Generate applicant data containing names/emails.
2.  **Compliance Gate**: Set a Great Expectations rule for "ISO Country Codes."
3.  **Privacy Test**: Run the ETL and observe that `logs/etl.log` contains zero PII, while the `Postgres` table is populated securely.
4.  **Chaos Run**: Inject a record from a non-compliant jurisdiction and watch the pipeline halt for a regulatory review.
