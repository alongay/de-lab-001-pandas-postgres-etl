# Monitoring & Governance Hub

This directory tracks the operational health and data quality of the Enterprise Data Platform.

## Directory Structure

- `data_quality_reports/`: Automated Great Expectations (GE) validation snapshots.
- `logs/`: (Symlinked) Platform orchestration logs for Airflow.

## Governance Patterns

### 1. Data Quality Gates
Every pipeline run executes a physical validator gate. If quality rules are violated:
- The pipeline execution stops.
- Data is diverted to Quarantine or blocked from production.
- A platform alert is triggered.

### 2. Operational Alerting
Platform failures are routed through `scripts/monitoring/slack_mock.py`.
- **Severity HIGH**: Data quality violations or infrastructure failure.
- **Severity LOW**: Retries or delayed batches.

### 3. SLA Tracking
The `iot_streaming_monitor` DAG tracks the "Heartbeat" of real-time tables. 
An alarm triggers if the Silver Delta table hasn't committed new data within a 5-minute window.
