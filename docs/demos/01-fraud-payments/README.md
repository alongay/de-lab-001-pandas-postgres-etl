# Demo 1: Fraud-Ready Payments Intake

**Status: ✅ Implemented & Verified**

### 🎯 The Pitch
This demo focuses on **Financial Integrity**. When handling payments, there is zero room for error. We demonstrate how to ingest financial data from multiple partners (API and CSV) while ensuring that the data warehouse only ever reflects the most accurate, clean version of a transaction.

### 🛠️ Technical Challenges
*   **Precision Money Handling**: Ensuring currency amounts are cast correctly without float-point rounding errors.
*   **Canonical Conflict Resolution**: Implementing "CSV Wins" logic via SQL views to handle cases where two data sources disagree on a payment status.
*   **Strict Quality Gating**: Using Great Expectations to block negative payment amounts, invalid currencies, and impossible transaction statuses.

### 🎓 Teaching Flow
1.  **Data Mocking**: Create CSV and JSON files simulating partner API pings.
2.  **Ingestion**: Run the ETL in Docker to land data into `raw_payments`.
3.  **Conflict Test**: Show how the `raw_payments_canonical` view picks the CSV record over the API record for the same ID.
4.  **Chaos Run**: Change one transaction amount to `-75.50` and watch the GE gate stop the entire pipeline.
5.  **Recovery**: Fix the CSV, rerun, and verify the pipeline succeeds.

---
**Links:**
- [Walkthrough Script](walkthrough.md)
- [Chaos Run Execution](chaos-run.md)
