#!/usr/bin/env bash
set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
REPO_DIR="$(dirname "$(dirname "$DIR")")"
PAYMENTS_DIR="$REPO_DIR/data/payments"

mkdir -p "$PAYMENTS_DIR"

JSON_PATH="$PAYMENTS_DIR/transactions.json"
CSV_PATH="$PAYMENTS_DIR/transactions_daily.csv"

echo "Creating JSON at $JSON_PATH..."
cat << 'EOF' > "$JSON_PATH"
[
  {
    "txnId": "TXN-30001",
    "accountId": "ACCT-9001",
    "amount": 49.95,
    "currency": "USD",
    "status": "AUTHORIZED",
    "txnTs": "2026-03-01T12:34:56Z"
  },
  {
    "txnId": "TXN-30002",
    "accountId": "ACCT-9002",
    "amount": 15.00,
    "currency": "USD",
    "status": "CAPTURED",
    "txnTs": "2026-03-01T12:35:56Z"
  },
  {
    "txnId": "TXN-30003",
    "accountId": "ACCT-9003",
    "amount": 75.50,
    "currency": "USD",
    "status": "DECLINED",
    "txnTs": "2026-03-01T12:36:56Z"
  }
]
EOF

echo "Creating CSV at $CSV_PATH..."
cat << 'EOF' > "$CSV_PATH"
txn_id,account_id,amount,currency,status,txn_ts
TXN-30001,ACCT-9001,49.95,USD,CAPTURED,2026-03-01T12:34:56Z
TXN-30002,ACCT-9002,15.00,USD,CAPTURED,2026-03-01T12:35:56Z
TXN-30003,ACCT-9003,75.50,USD,DECLINED,2026-03-01T12:36:56Z
EOF

echo "Done! Test data generated successfully."
