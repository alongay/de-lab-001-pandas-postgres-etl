# Curriculum: Educational Demo Projects

This hub outlines the enterprise-grade data engineering scenarios designed for this repository. Each demo introduces a unique domain challenge while leveraging the same core architecture.

---

## 🏗️ Demo Projects

### [Demo 1: Fraud-Ready Payments Intake](01-fraud-payments/walkthrough.md) (✅ Implemented)
*   **The Domain**: Handling secure financial transactions.
*   **Key Learnings**: Multi-source ingestion (API/CSV), "CSV Wins" logic, and Great Expectations gates.
*   **Chaos Engineering**: [Failure & Recovery Run](01-fraud-payments/chaos-run.md)

### [Demo 2: IoT Sensor Telemetry](02-iot-telemetry/) (⏳ Next Phase)
*   **The Domain**: High-volume machine data and physical constraints.
*   **Key Learnings**: Timeseries indexing, outlier detection, and unit-specific validation.

### [Demo 3: HR Applicant Intake](03-hr-applicants/) (📅 Future)
*   **The Domain**: PII privacy, compliance, and data sovereignty.
*   **Key Learnings**: Regex PII scrubbing, ISO country allowed-lists, and redaction logic.

---

## 🎓 Teaching Flow
1. **Prepare Payload**: Generate synthetic partner data.
2. **Profile**: Explore data interactively in Jupyter.
3. **Execute**: Run the containerized ETL pipeline.
4. **Chaos**: Intentionally corrupt data to trigger the quality gate.
5. **Verify**: Prove recovery and run CI unit tests.
