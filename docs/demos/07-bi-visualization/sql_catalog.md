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

## 📈 Advanced Analytics (Window Functions & Trends)

### 1. Daily Revenue Growth % (Finance)
**Purpose**: Trend analysis for executive reporting.
```sql
SELECT 
    transaction_date, 
    daily_revenue,
    100 * (daily_revenue - LAG(daily_revenue) OVER (ORDER BY transaction_date)) / LAG(daily_revenue) OVER (ORDER BY transaction_date) as growth_percentage
FROM (
    SELECT date(transaction_date) as transaction_date, sum(amount_usd) as daily_revenue
    FROM payments.transactions_daily
    GROUP BY 1
) subquery;
```

### 2. Applicant Aging (HR Velocity)
**Purpose**: Identify bottlenecks in the hiring pipeline.
```sql
SELECT 
    full_name, 
    status, 
    CURRENT_DATE - date(application_date) as days_in_pipeline
FROM hr.applications
WHERE status NOT IN ('hired', 'rejected')
ORDER BY days_in_pipeline DESC;
```

### 3. IoT Sensor Moving Average (Smoothing)
**Purpose**: Filter noise from real-time streams for better alerts.
```sql
SELECT 
    timestamp, 
    sensor_id, 
    temperature,
    AVG(temperature) OVER (PARTITION BY sensor_id ORDER BY timestamp ROWS BETWEEN 5 PRECEDING AND CURRENT ROW) as filtered_temp
FROM iot_telemetry_silver;
```

---

## 🛡️ Cross-Domain Quality Monitoring

### 1. Global Pipeline Integrity (The "Master Audit")
**Purpose**: A single metric summarizing health across all domains.
```sql
SELECT 'IoT' as domain, count(*) as record_count, 'Quarantined' as status FROM iot_telemetry_quarantine
UNION ALL
SELECT 'IoT' as domain, count(*) as record_count, 'Production' as status FROM iot_telemetry_silver
UNION ALL
SELECT 'HR' as domain, count(*) as record_count, 'Clean' as status FROM hr.applications
UNION ALL
SELECT 'Payments' as domain, count(*) as record_count, 'Processed' as status FROM payments.transactions_daily;
```

---

## 🧪 Interview Perspective
"I don't just 'build' dashboards in the UI; I manage the **BI-as-Code**. Every metric in Metabase is backed by a version-controlled SQL script in our `sql_catalog.md`, ensuring that our business logic is auditable and reproducible. By using **Window Functions** in SQL, I provide deeper insights like moving averages and growth trends rather than just raw counts."
