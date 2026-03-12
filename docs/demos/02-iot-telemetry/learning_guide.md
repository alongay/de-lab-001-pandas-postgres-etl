# IoT Chaos Run: Operational Resilience Test

This document details how to execute and verify the **Batch Quarantine Pattern** via chaos injection.

## 🧪 Experiment Objective
Verify that the pipeline correctly identifies and isolates a batch of sensor data containing physical impossibilities (Outliers) without losing the data.

## 🛠️ Execution Steps

### 1. Generate Chaos Data
Use the synthetic data generator with a high outlier rate (80%):

```powershell
# PowerShell
.\scripts\iot\create_iot_demo_data.ps1 -DeviceCount 10 -Minutes 30 -OutlierRate 0.8
```

```bash
# Bash
DEVICE_COUNT=10 MINUTES=30 OUTLIER_RATE=0.8 bash ./scripts/iot/create_iot_demo_data.sh
```

### 2. Run the Pipeline
Execute the IoT ETL module:

```powershell
docker compose run --rm -e PYTHONPATH=/app etl python -m src.iot.etl_run_iot
```

**Expected Result**: The pipeline should exit with an error code (non-zero) and log a Great Expectations failure.

### 3. Verify Isolation
Query the database to confirm data was redirected:

```sql
-- This should show 0 records from the latest batch
SELECT COUNT(*) FROM raw_sensor_readings WHERE ingested_at > NOW() - INTERVAL '5 minutes';

-- This should contain the quarantined records
SELECT metric, COUNT(*) FROM raw_sensor_readings_quarantine GROUP BY metric;
```

## 📊 Recovery Protocol
1. Review the GE validation result in `logs/ge_validation_*.json`.
2. Address the source of the outliers (sensor calibration or upstream provider).
3. Re-generate clean data and rerun the pipeline.
