# 🗄️ BI SQL Catalog: executive-watchtower

This document contains the version-controlled SQL logic behind our Metabase dashboards. Storing these in git ensures logic parity between environments and provides a "Source of Truth" for our BI metrics.

---

## 🏗️ Dashboard: Executive Watchtower

### 1. Total Transaction volume (Finance)
**Purpose**: High-level financial throughput.
```sql
SELECT sum(amount_usd) as total_revenue, count(*) as transaction_count
FROM payments.transactions_daily
WHERE status = 'processed';
```

### 2. Talent Pipeline Funnel (HR)
**Purpose**: Visualize recruitment velocity.
```sql
SELECT status, count(*) as applicant_count
FROM hr.applications
GROUP BY status
ORDER BY applicant_count DESC;
```

### 3. IoT Fleet Status (Real-time Stream)
**Purpose**: Check health of connected sensors.
```sql
SELECT sensor_id, avg(temperature) as avg_temp, max(timestamp) as last_seen
FROM iot_telemetry_silver
GROUP BY sensor_id
ORDER BY last_seen DESC
LIMIT 10;
```

---

## 🛡️ Dashboard: Data Quality Hub

### 1. Quarantined IoT Anomalies
**Purpose**: Observability into the "Physics Quality Gate."
```sql
SELECT error_reason, count(*) as anomaly_count, avg(temperature) as rejected_temp
FROM iot_telemetry_quarantine
GROUP BY error_reason;
```

### 2. Batch Partition Audit
**Purpose**: Verify data storage efficiency.
```sql
SELECT partition_date, count(*) as record_count
FROM iot_telemetry_silver
GROUP BY partition_date
ORDER BY partition_date DESC;
```

---

## 🧪 Interview Perspective
"I don't just 'build' dashboards in the UI; I manage the **BI-as-Code**. Every metric in Metabase is backed by a version-controlled SQL script in our `sql_catalog.md`, ensuring that our business logic is auditable and reproducible."
