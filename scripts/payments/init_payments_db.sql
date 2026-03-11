-- scripts/payments/init_payments_db.sql
-- Initialize the payments domain schema.

-- 1. Main table for ingested payments
CREATE TABLE IF NOT EXISTS raw_payments (
    txn_id VARCHAR(50) PRIMARY KEY,
    account_id VARCHAR(50) NOT NULL,
    amount DECIMAL(12, 2) NOT NULL,
    currency VARCHAR(10) NOT NULL,
    status VARCHAR(20) NOT NULL,
    txn_ts TIMESTAMP WITH TIME ZONE NOT NULL,
    ingested_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Index for common lookups
CREATE INDEX IF NOT EXISTS idx_raw_payments_account ON raw_payments(account_id);
CREATE INDEX IF NOT EXISTS idx_raw_payments_ts ON raw_payments(txn_ts);
