# Demo 3: HR Applicant Intake (PII)

**Status: 📅 Future Extension**

### 🎯 The Pitch
This demo focuses on **Data Privacy and Compliance**. HR data is full of **PII (Personally Identifiable Information)**. We show how to build a pipeline that ingests job applicants while strictly following **data sovereignty laws** and keeping sensitive data out of the system logs.

### 🛠️ Technical Challenges
- **PII Redaction**: Implementing logic to ensure emails and names are scrubbed from console logs.
- **Data Sovereignty**: Enforcing strict **ISO country allowed-lists** to comply with regional regulations.
- **Identity Integrity**: Validating complex strings (phone numbers/emails) via **robust regex enforcement**.

### 🎓 Teaching Flow
- **PII Payload**: Generate applicant data containing names and emails.
- **Compliance Gate**: Set a **Great Expectations** rule for "ISO Country Codes."
- **Privacy Test**: Run the ETL and observe that `logs/etl.log` contains **zero PII**.
- **Chaos Run**: Inject a record from a non-compliant jurisdiction and watch the pipeline halt.
