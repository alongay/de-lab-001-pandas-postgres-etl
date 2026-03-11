-- Database Schema for Demo 2 (IoT Sensor Telemetry)
-- Optimized for High-Volume Time-Series Data

-- Wipe existing to allow transition from flat to partitioned
DROP TABLE IF EXISTS raw_sensor_readings CASCADE;

-- 1. Raw Production Table (Clean Data)
-- We use Declarative Range Partitioning on reading_ts for performance and scalability.
CREATE TABLE IF NOT EXISTS raw_sensor_readings (
    partner_id VARCHAR(50) NOT NULL,
    device_id VARCHAR(50) NOT NULL,
    reading_ts TIMESTAMPTZ NOT NULL,
    metric VARCHAR(50) NOT NULL,
    value DOUBLE PRECISION,
    unit VARCHAR(20),
    ingested_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (partner_id, device_id, reading_ts, metric)
) PARTITION BY RANGE (reading_ts);

-- 2. Initial Partitions (Demo Context: March 2026)
CREATE TABLE IF NOT EXISTS raw_sensor_readings_y2026m03 PARTITION OF raw_sensor_readings
    FOR VALUES FROM ('2026-03-01 00:00:00+00') TO ('2026-04-01 00:00:00+00');

-- Create a 'future' partition to show production scaling intent
CREATE TABLE IF NOT EXISTS raw_sensor_readings_y2026m04 PARTITION OF raw_sensor_readings
    FOR VALUES FROM ('2026-04-01 00:00:00+00') TO ('2026-05-01 00:00:00+00');

-- 3. Quarantine Table (Faulty/Noisy Data Audit)
-- Quarantine tables are often NOT partitioned unless the volume of bad data is massive.
CREATE TABLE IF NOT EXISTS raw_sensor_readings_quarantine (
    partner_id VARCHAR(50),
    device_id VARCHAR(50),
    reading_ts TIMESTAMPTZ,
    metric VARCHAR(50),
    value DOUBLE PRECISION,
    unit VARCHAR(20),
    ingested_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- 4. Advanced Time-Series Indexing
-- Composite index for fast device-history range queries
CREATE INDEX IF NOT EXISTS idx_iot_device_ts ON raw_sensor_readings(device_id, reading_ts);

-- Index on partition key specifically (though redundant with PK, good for partitioned scans)
CREATE INDEX IF NOT EXISTS idx_iot_ts ON raw_sensor_readings(reading_ts);
