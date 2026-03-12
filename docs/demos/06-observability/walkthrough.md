# Walkthrough: Demo 6 — Proactive Data Observability

## 🛠️ Demo: The Chaos Run
This section proves the platform's **Intelligence** by detecting statistical drift in a live ETL pipeline.

1.  **Inject Chaos**: Run the specialized drift simulation: `.\task.ps1 demo-observability`.
2.  **What is happening?**:
    *   The script first establishes a "Normal" baseline using clean payments data.
    *   It then injects a 10x shift in the transaction amounts (e.g., changing the mean from $50 to $500).
3.  **Detect Statistical Shift**: The ETL runner calculates the **Kolmogorov-Smirnov (KS) Test** p-value during the transformation phase.
4.  **Observe the Alert**: The terminal logs will scream `🚨 DATA DRIFT DETECTED: amount (KS p-value: 0.0000)`.
5.  **Audit the Hub**: Run the Observability Viewer: `docker compose -f docker-compose.observability.yml up`.
    *   The viewer will display the persistent alert in the central metadata store (`observability.db`).

> [!CAUTION]
> **Interview Point**: "Simple validation only catches 'wrong' data types. I implemented **Statistical Observability** that detects when the distribution of data changes. This catches subtle upstream bugs—like a currency conversion error or a malfunctioning promotional engine—that schema checks would miss entirely."

---

## ✅ Portfolio Verification
- **Baseline established**: Checked in `data/observability/baselines/`.
- **Drift Alert recorded**: Persisted in DuckDB `execution_metrics`.
- **Airflow Audit**: The `observability_audit_platform` DAG verifies platform-wide health.
