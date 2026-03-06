SELECT txn_id, partner_id, status, amount
FROM raw_payments_canonical
WHERE txn_id IN ('TXN-30001', 'TXN-30002', 'TXN-30003')
ORDER BY txn_id;
