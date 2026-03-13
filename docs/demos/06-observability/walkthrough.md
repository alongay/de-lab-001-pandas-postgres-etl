# Walkthrough: Demo 6 — Proactive Data Observability

## 🛠️ Demo: The Chaos Run
This section proves the platform's **Intelligence** by detecting statistical drift in a live ETL pipeline.

1.  **Inject Chaos**: Run the specialized drift simulation:
    ```powershell
    .\scripts\payments\inject_payment_drift.ps1
    ```
2.  **What is happening?**:
    *   The script injects "Impossible High" amounts into the CSV source using a Power Curve distribution.
    *   It bypasses the Great Expectations quality gate (which would normally stop the "broken" data) to simulate a "silent" upstream error.
3.  **Run the ETL**: Trigger the **`payments_etl_pipeline`** DAG in Airflow.
    *   The ETL calculates the **Kolmogorov-Smirnov (KS) Test** during the transformation phase.
    *   Look for logs: `🚨 DATA DRIFT DETECTED in column amount (p-value: 0.0000)`.
4.  **The Auditor's Verdict**: Trigger the **`observability_audit_platform`** DAG.
    *   It audits the central **Metadata Lake (DuckDB)** and flags the breach.
    *   Log output: `🚨 ALERT: 1 data drift instances detected in the last 24h!`.

> [!CAUTION]
> **Interview Point**: "Simple validation only catches 'wrong' data types. I implemented **Statistical Observability** that detects when the distribution of data changes. This catches subtle upstream bugs—like a currency conversion error or a malfunctioning promotional engine—that schema checks would miss entirely."

---

## ✅ Portfolio Verification
- **Baseline established**: Checked in `data/observability/baselines/`.
- **Drift Alert recorded**: Persisted in DuckDB `execution_metrics`.
- **Airflow Audit**: The `observability_audit_platform` DAG verifies platform-wide health.
