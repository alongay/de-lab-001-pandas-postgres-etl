$ErrorActionPreference = "Stop"
$scriptDir = Split-Path $MyInvocation.MyCommand.Path
$repoDir = Split-Path $scriptDir
$paymentsDir = Join-Path $repoDir "data\payments"

if (-not (Test-Path $paymentsDir)) {
    New-Item -ItemType Directory -Force -Path $paymentsDir | Out-Null
}

$jsonPath = Join-Path $paymentsDir "transactions.json"
$csvPath = Join-Path $paymentsDir "transactions_daily.csv"

Write-Host "Creating JSON at $jsonPath..."
$jsonContent = @"
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
"@

$jsonContent | Out-File -FilePath $jsonPath -Encoding utf8

Write-Host "Creating CSV at $csvPath..."
$csvContent = @"
txn_id,account_id,amount,currency,status,txn_ts
TXN-30001,ACCT-9001,49.95,USD,CAPTURED,2026-03-01T12:34:56Z
TXN-30002,ACCT-9002,15.00,USD,CAPTURED,2026-03-01T12:35:56Z
TXN-30003,ACCT-9003,75.50,USD,DECLINED,2026-03-01T12:36:56Z
"@
$csvContent | Out-File -FilePath $csvPath -Encoding utf8

Write-Host "Done! Test data generated successfully."
