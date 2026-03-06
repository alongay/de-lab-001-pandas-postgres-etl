CREATE OR REPLACE VIEW raw_payments_canonical AS
SELECT DISTINCT ON (txn_id)
  txn_id,
  partner_id,
  status,
  amount,
  currency,
  txn_ts,
  ingested_at
FROM raw_payments
ORDER BY
  txn_id,
  CASE WHEN partner_id = 'partner_csv' THEN 2 ELSE 1 END DESC,
  ingested_at DESC;
